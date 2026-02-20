#!/usr/bin/env python3
"""
app/plan_generator.py — Genera un plan de seguridad completo
usando solo el corpus indexado como SSoT (sin LLM).

Consulta el índice FAISS+BM25 por cada dominio de seguridad,
recupera los chunks más relevantes, y compila un plan con citas.

Uso:
    python -m app.plan_generator
"""

import json
import pickle
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np
import yaml

from app.utils import load_config, print_header, PROJECT_ROOT


class CorpusRetriever:
    """Retriever ligero sin LLM — solo búsqueda vectorial + BM25."""

    def __init__(self):
        self.config = load_config()
        self._load_retrieval_config()
        self._load_indexes()
        self._load_embedder()

    def _load_retrieval_config(self):
        path = PROJECT_ROOT / "configs" / "retrieval.yml"
        with open(path, "r", encoding="utf-8") as f:
            self.retrieval_config = yaml.safe_load(f)

    def _load_indexes(self):
        import faiss
        vector_dir = PROJECT_ROOT / self.config["paths"]["vector_index"]
        self.vector_index = faiss.read_index(str(vector_dir / "index.faiss"))
        with open(vector_dir / "chunk_ids.pkl", "rb") as f:
            self.chunk_ids_vector = pickle.load(f)

        bm25_dir = PROJECT_ROOT / self.config["paths"]["bm25_index"]
        bm25_path = bm25_dir / "bm25_index.pkl"
        self.bm25_index = None
        self.chunk_ids_bm25 = None
        if bm25_path.exists():
            with open(bm25_path, "rb") as f:
                self.bm25_index = pickle.load(f)
            with open(bm25_dir / "chunk_ids.pkl", "rb") as f:
                self.chunk_ids_bm25 = pickle.load(f)

        meta_dir = PROJECT_ROOT / self.config["paths"]["metadata_store"]
        with open(meta_dir / "chunks_metadata.json", "r", encoding="utf-8") as f:
            self.chunks_metadata = json.load(f)

        self.chunks_content = {}
        chunks_path = PROJECT_ROOT / self.config["paths"]["chunks"] / "chunks.jsonl"
        with open(chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                c = json.loads(line.strip())
                self.chunks_content[c["chunk_id"]] = c["content"]

    def _load_embedder(self):
        from sentence_transformers import SentenceTransformer
        emb = self.config.get("embeddings", {})
        self.embedder = SentenceTransformer(
            emb.get("model_name", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"),
            device=emb.get("device", "cpu"),
        )

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """Búsqueda híbrida RRF."""
        # Vector
        qe = self.embedder.encode([query], normalize_embeddings=True)
        qnp = np.array(qe, dtype="float32")
        scores_v, indices_v = self.vector_index.search(qnp, top_k * 2)
        vector_results = []
        for s, i in zip(scores_v[0], indices_v[0]):
            if i < len(self.chunk_ids_vector):
                vector_results.append((self.chunk_ids_vector[i], float(s)))

        # BM25
        bm25_results = []
        if self.bm25_index and self.chunk_ids_bm25:
            tokens = query.lower().split()
            bm25_scores = self.bm25_index.get_scores(tokens)
            top_idx = np.argsort(bm25_scores)[::-1][:top_k * 2]
            for idx in top_idx:
                if bm25_scores[idx] > 0 and idx < len(self.chunk_ids_bm25):
                    bm25_results.append((self.chunk_ids_bm25[idx], float(bm25_scores[idx])))

        # RRF
        k = 60
        rrf = {}
        for rank, (cid, _) in enumerate(vector_results):
            rrf[cid] = rrf.get(cid, 0) + 1.0 / (k + rank + 1)
        for rank, (cid, _) in enumerate(bm25_results):
            rrf[cid] = rrf.get(cid, 0) + 1.0 / (k + rank + 1)

        sorted_r = sorted(rrf.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for cid, score in sorted_r:
            meta = self.chunks_metadata.get(cid, {})
            results.append({
                "chunk_id": cid,
                "score": round(score, 4),
                "content": self.chunks_content.get(cid, ""),
                "source_file": meta.get("source_file", "n/d"),
                "section_path": meta.get("section_path", ""),
                "page_start": meta.get("page_start", "n/d"),
                "page_end": meta.get("page_end", "n/d"),
                "doc_type": meta.get("doc_type", ""),
                "frameworks": meta.get("frameworks", []),
            })
        return results


# Queries por dominio de seguridad
DOMAINS = {
    "gobernanza": [
        "política de seguridad de la información gobernanza roles responsabilidades",
        "marco de gobernanza ciberseguridad estructura organizativa",
        "gestión de riesgos análisis de riesgos metodología",
        "plan director de seguridad fases implementación",
    ],
    "normativa_cumplimiento": [
        "Esquema Nacional de Seguridad ENS medidas implantación categorías",
        "RGPD protección de datos cumplimiento legal obligaciones",
        "NIST Cybersecurity Framework funciones categorías",
        "declaración de aplicabilidad controles",
    ],
    "identidad_acceso": [
        "autenticación multifactor MFA gestión de identidades control de acceso",
        "gestión de contraseñas políticas credenciales",
        "identidad digital certificados electrónicos",
    ],
    "endpoint_hardening": [
        "hardening bastionado configuración segura servidores estaciones",
        "endpoint seguro configuración segura Windows",
        "CIS benchmark Windows 11 configuración seguridad",
        "seguridad macOS configuración bastionado Apple",
    ],
    "red_perimetro": [
        "cortafuegos firewall protección perimetral segmentación red",
        "HTTPS TLS certificados cifrado comunicaciones",
        "protección DDoS denegación de servicio mitigación",
        "CDN seguridad redes de distribución de contenido",
        "seguridad WiFi redes inalámbricas WPA3",
    ],
    "correo_navegadores": [
        "seguridad correo electrónico SPF DKIM DMARC anti-phishing",
        "navegadores web seguridad configuración Chrome Firefox Edge",
    ],
    "dispositivos_moviles": [
        "seguridad dispositivos móviles MDM gestión Android iOS",
        "BYOD política dispositivos móviles empresa",
    ],
    "nube_virtualizacion": [
        "seguridad cloud nube protección datos soberanía",
        "virtualización seguridad hipervisor contenedores",
        "Kubernetes seguridad contenedores orquestación",
        "almacenamiento seguro copias respaldo nube",
    ],
    "desarrollo_seguro": [
        "desarrollo seguro SDLC SSDLC OWASP buenas prácticas",
        "seguridad aplicaciones web vulnerabilidades CMS Drupal",
        "seguridad bases de datos BBDD hardening SQL",
    ],
    "respuesta_incidentes": [
        "respuesta incidentes seguridad gestión cibercrisis procedimiento",
        "ransomware prevención respuesta recuperación",
        "fuga información datos clasificación prevención DLP",
        "plan continuidad negocio BCP DRP recuperación desastres",
    ],
    "concienciacion_iot": [
        "concienciación formación seguridad empleados ingeniería social",
        "seguridad Internet de las Cosas IoT dispositivos conectados",
        "redes sociales seguridad privacidad empresa",
    ],
    "monitorizacion_amenazas": [
        "ciberamenazas panorama amenazas tendencias riesgos",
        "inteligencia artificial ciberseguridad machine learning detección",
        "cryptojacking minería criptomonedas detección prevención",
        "desinformación manipulación información ciberespacio",
    ],
}


def extract_key_points(content: str, max_points: int = 5) -> list[str]:
    """Extrae puntos clave de un chunk (heurística por frases)."""
    import re
    # Buscar items de lista o frases con verbos de acción
    items = re.findall(r'(?:^|\n)\s*[-•*]\s*(.+?)(?:\n|$)', content)
    if items:
        return [i.strip() for i in items[:max_points] if len(i.strip()) > 20]

    # Buscar frases relevantes
    sentences = re.split(r'[.]\s+', content)
    relevant = []
    keywords = ['debe', 'recomienda', 'necesario', 'importante', 'obligatorio',
                'implementar', 'configurar', 'verificar', 'proteger', 'garantizar',
                'should', 'must', 'implement', 'configure', 'ensure', 'require']
    for s in sentences:
        if any(kw in s.lower() for kw in keywords) and len(s.strip()) > 30:
            relevant.append(s.strip())
        if len(relevant) >= max_points:
            break
    return relevant


def format_citation(r: dict) -> str:
    """Formatea una cita."""
    src = r["source_file"]
    sec = r["section_path"]
    p1 = r["page_start"]
    p2 = r["page_end"]
    return f"`{src}` — `{sec}` — pp. `{p1}-{p2}`"


def generate_plan(retriever: CorpusRetriever) -> str:
    """Genera el plan de seguridad completo."""
    all_sources = set()
    sections = []

    for domain_name, queries in DOMAINS.items():
        domain_results = []
        seen_chunks = set()

        for q in queries:
            results = retriever.search(q, top_k=6)
            for r in results:
                if r["chunk_id"] not in seen_chunks:
                    domain_results.append(r)
                    seen_chunks.add(r["chunk_id"])
                    all_sources.add(r["source_file"])

        sections.append((domain_name, domain_results))

    return sections, all_sources


def main():
    print_header("GENERANDO PLAN DE SEGURIDAD DESDE CORPUS")
    print("  Cargando índices y modelo de embeddings...")

    retriever = CorpusRetriever()
    print(f"  ✓ {retriever.vector_index.ntotal} chunks indexados")
    print(f"  Consultando {len(DOMAINS)} dominios de seguridad...\n")

    sections, all_sources = generate_plan(retriever)

    # Guardar resultados raw para uso posterior
    output_dir = PROJECT_ROOT / "reports"
    raw_output = output_dir / "plan_evidence.json"

    evidence = {}
    for domain_name, results in sections:
        evidence[domain_name] = []
        for r in results:
            evidence[domain_name].append({
                "source_file": r["source_file"],
                "section_path": r["section_path"],
                "page_start": r["page_start"],
                "page_end": r["page_end"],
                "score": r["score"],
                "content_preview": r["content"][:300],
                "key_points": extract_key_points(r["content"]),
                "frameworks": r.get("frameworks", []),
            })

    with open(raw_output, "w", encoding="utf-8") as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)

    print(f"\n  ✓ Evidencia extraída → {raw_output}")
    print(f"  ✓ Fuentes consultadas: {len(all_sources)} documentos")

    # Stats por dominio
    for domain_name, results in sections:
        label = domain_name.replace("_", " ").title()
        print(f"    📋 {label}: {len(results)} fragmentos relevantes")


if __name__ == "__main__":
    main()
