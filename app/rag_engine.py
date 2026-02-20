#!/usr/bin/env python3
"""
app/rag_engine.py — Motor RAG principal

Retrieval híbrido (FAISS vector + BM25) con generación local via llama.cpp.
Implementa los modos: consulta, diseño y auditoría.

Uso:
    python -m app.rag_engine query "¿Cómo configurar MFA?"
    python -m app.rag_engine --mode audit
    python -m app.rag_engine --mode design
"""

import argparse
import json
import pickle
import sys
from pathlib import Path

from app.utils import (
    load_config,
    require_pdfs,
    print_header,
    PROJECT_ROOT,
)


class RAGEngine:
    """Motor RAG con retrieval híbrido y generación local."""

    def __init__(self):
        self.config = load_config()
        self.retrieval_config = self._load_retrieval_config()
        self.vector_index = None
        self.bm25_index = None
        self.chunk_ids_vector = None
        self.chunk_ids_bm25 = None
        self.chunks_metadata = None
        self.chunks_content = {}
        self.embedder = None
        self.llm = None

    def _load_retrieval_config(self) -> dict:
        import yaml
        path = PROJECT_ROOT / "configs" / "retrieval.yml"
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_indexes(self):
        """Carga índices vectorial y BM25 desde disco."""
        try:
            import faiss
        except ImportError:
            print("[ERROR] faiss-cpu no instalado.")
            sys.exit(1)

        vector_dir = PROJECT_ROOT / self.config["paths"]["vector_index"]
        index_path = vector_dir / "index.faiss"

        if not index_path.exists():
            print("[ERROR] Índice vectorial no encontrado. Ejecute: make index")
            sys.exit(1)

        self.vector_index = faiss.read_index(str(index_path))

        with open(vector_dir / "chunk_ids.pkl", "rb") as f:
            self.chunk_ids_vector = pickle.load(f)

        # BM25 (opcional)
        bm25_dir = PROJECT_ROOT / self.config["paths"]["bm25_index"]
        bm25_path = bm25_dir / "bm25_index.pkl"
        if bm25_path.exists():
            with open(bm25_path, "rb") as f:
                self.bm25_index = pickle.load(f)
            with open(bm25_dir / "chunk_ids.pkl", "rb") as f:
                self.chunk_ids_bm25 = pickle.load(f)

        # Metadatos
        meta_dir = PROJECT_ROOT / self.config["paths"]["metadata_store"]
        meta_path = meta_dir / "chunks_metadata.json"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                self.chunks_metadata = json.load(f)

        # Contenido de chunks
        chunks_path = PROJECT_ROOT / self.config["paths"]["chunks"] / "chunks.jsonl"
        if chunks_path.exists():
            with open(chunks_path, "r", encoding="utf-8") as f:
                for line in f:
                    chunk = json.loads(line.strip())
                    self.chunks_content[chunk["chunk_id"]] = chunk["content"]

        print(f"  Índices cargados: {self.vector_index.ntotal} vectores")
        if self.bm25_index:
            print(f"  BM25 cargado: {len(self.chunk_ids_bm25)} documentos")

    def load_embedder(self):
        """Carga modelo de embeddings."""
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            print("[ERROR] sentence-transformers no instalado.")
            sys.exit(1)

        emb_config = self.config.get("embeddings", {})
        model_name = emb_config.get("model_name",
                                    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        device = emb_config.get("device", "cpu")

        self.embedder = SentenceTransformer(model_name, device=device)

    def load_llm(self):
        """Carga LLM local via llama-cpp-python."""
        try:
            from llama_cpp import Llama
        except ImportError:
            print("[ERROR] llama-cpp-python no instalado.")
            print("  pip install llama-cpp-python")
            sys.exit(1)

        llm_config = self.config.get("llm", {})
        model_path = PROJECT_ROOT / llm_config.get("model_path", "models/model.gguf")

        if not model_path.exists():
            print(f"[ERROR] Modelo LLM no encontrado en: {model_path}")
            print("  Descargue un modelo GGUF y colóquelo en models/")
            sys.exit(1)

        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=llm_config.get("context_length", 4096),
            n_gpu_layers=llm_config.get("n_gpu_layers", 0),
            n_threads=llm_config.get("n_threads", 4),
            verbose=False,
        )

    def search_vector(self, query: str, top_k: int = 8) -> list[tuple[str, float]]:
        """Búsqueda vectorial por similitud."""
        if self.embedder is None:
            self.load_embedder()

        query_embedding = self.embedder.encode(
            [query],
            normalize_embeddings=self.config.get("embeddings", {}).get("normalize", True),
        )
        import numpy as np
        query_np = np.array(query_embedding, dtype="float32")

        scores, indices = self.vector_index.search(query_np, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunk_ids_vector):
                chunk_id = self.chunk_ids_vector[idx]
                results.append((chunk_id, float(score)))

        return results

    def search_bm25(self, query: str, top_k: int = 8) -> list[tuple[str, float]]:
        """Búsqueda BM25."""
        if self.bm25_index is None:
            return []

        tokens = query.lower().split()
        scores = self.bm25_index.get_scores(tokens)

        # Top-K
        import numpy as np
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            if scores[idx] > 0 and idx < len(self.chunk_ids_bm25):
                chunk_id = self.chunk_ids_bm25[idx]
                results.append((chunk_id, float(scores[idx])))

        return results

    def hybrid_search(self, query: str) -> list[dict]:
        """
        Búsqueda híbrida con Reciprocal Rank Fusion (RRF).
        """
        search_config = self.retrieval_config.get("search", {})
        hybrid_config = self.retrieval_config.get("hybrid", {})
        top_k = search_config.get("top_k", 8)
        final_k = search_config.get("final_k", 5)
        min_score = search_config.get("min_score", 0.25)
        mode = search_config.get("mode", "hybrid")

        vector_results = []
        bm25_results = []

        if mode in ("vector", "hybrid"):
            vector_results = self.search_vector(query, top_k)
        if mode in ("bm25", "hybrid") and self.bm25_index:
            bm25_results = self.search_bm25(query, top_k)

        if mode == "vector":
            combined = {cid: score for cid, score in vector_results}
        elif mode == "bm25":
            combined = {cid: score for cid, score in bm25_results}
        else:
            # RRF fusion
            k = 60  # RRF constant
            rrf_scores = {}

            for rank, (cid, _) in enumerate(vector_results):
                rrf_scores[cid] = rrf_scores.get(cid, 0) + 1.0 / (k + rank + 1)
            for rank, (cid, _) in enumerate(bm25_results):
                rrf_scores[cid] = rrf_scores.get(cid, 0) + 1.0 / (k + rank + 1)

            combined = rrf_scores

        # Ordenar y filtrar
        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)

        results = []
        for chunk_id, score in sorted_results[:final_k]:
            if score < min_score and mode == "vector":
                continue

            content = self.chunks_content.get(chunk_id, "")
            metadata = self.chunks_metadata.get(chunk_id, {}) if self.chunks_metadata else {}

            results.append({
                "chunk_id": chunk_id,
                "score": round(score, 4),
                "content": content,
                "metadata": metadata,
            })

        return results

    def format_context(self, results: list[dict]) -> str:
        """Formatea resultados de búsqueda como contexto para el LLM."""
        ctx_config = self.retrieval_config.get("context", {})
        separator = ctx_config.get("separator", "\n---\n")
        include_meta = ctx_config.get("include_metadata", True)

        parts = []
        for i, r in enumerate(results, 1):
            meta = r.get("metadata", {})
            header = f"[Fragmento {i}]"
            if include_meta:
                source = meta.get("source_file", "n/d")
                section = meta.get("section_path", "")
                pages = f"pp. {meta.get('page_start', 'n/d')}-{meta.get('page_end', 'n/d')}"
                header += f" Fuente: {source} | {section} | {pages}"

            parts.append(f"{header}\n{r['content']}")

        return separator.join(parts)

    def format_citations(self, results: list[dict]) -> str:
        """Formatea las citas en formato Markdown según §7."""
        lines = ["\n**Fuentes**\n"]
        for r in results:
            meta = r.get("metadata", {})
            source = meta.get("source_file", "n/d")
            section = meta.get("section_path", "")
            page_start = meta.get("page_start", "n/d")
            page_end = meta.get("page_end", "n/d")
            lines.append(f"* `{source}` — `{section}` — páginas `{page_start}-{page_end}`")
        return "\n".join(lines)

    def generate_answer(self, query: str, context: str, mode: str = "query") -> str:
        """Genera respuesta con el LLM local."""
        if self.llm is None:
            self.load_llm()

        # Cargar prompt template
        prompt_files = {
            "query": "rag_answer.md",
            "audit": "audit_mode.md",
            "design": "design_mode.md",
        }
        prompt_file = PROJECT_ROOT / "prompts" / prompt_files.get(mode, "rag_answer.md")
        system_prompt_file = PROJECT_ROOT / "prompts" / "system.md"

        system_prompt = ""
        if system_prompt_file.exists():
            system_prompt = system_prompt_file.read_text(encoding="utf-8")

        template = ""
        if prompt_file.exists():
            template = prompt_file.read_text(encoding="utf-8")

        # Sustituir placeholders
        prompt = template.replace("{context}", context).replace("{query}", query)

        llm_config = self.config.get("llm", {})
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=llm_config.get("max_tokens", 1024),
            temperature=llm_config.get("temperature", 0.1),
            top_p=llm_config.get("top_p", 0.9),
        )

        return response["choices"][0]["message"]["content"]

    def query(self, question: str, mode: str = "query") -> dict:
        """
        Pipeline completo: búsqueda → contexto → generación → citación.
        """
        # 1. Búsqueda
        results = self.hybrid_search(question)

        if not results:
            return {
                "answer": ("No encuentro evidencia suficiente en la documentación "
                           "indexada para responder a esta consulta."),
                "sources": [],
                "mode": mode,
            }

        # 2. Contexto
        context = self.format_context(results)

        # 3. Generación
        answer = self.generate_answer(question, context, mode)

        # 4. Citación
        citations = self.format_citations(results)

        return {
            "answer": answer + "\n" + citations,
            "sources": [r["metadata"] for r in results],
            "mode": mode,
            "num_results": len(results),
        }


def main():
    parser = argparse.ArgumentParser(description="Motor RAG — Seguridad Informática")
    parser.add_argument("action", choices=["query", "status"],
                        help="Acción a ejecutar")
    parser.add_argument("question", nargs="?", default=None,
                        help="Pregunta (para acción 'query')")
    parser.add_argument("--mode", choices=["query", "audit", "design"],
                        default="query", help="Modo de operación")
    parser.add_argument("--top-k", type=int, default=None,
                        help="Número de resultados")
    parser.add_argument("--json", action="store_true",
                        help="Salida en formato JSON")
    args = parser.parse_args()

    if args.action == "status":
        print_header("ESTADO DEL SISTEMA RAG")
        config = load_config()

        # Comprobar componentes
        checks = {
            "PDFs en incoming": len(list((PROJECT_ROOT / config["paths"]["incoming_pdfs"]).glob("*.pdf"))),
            "PDFs consolidados": len(list((PROJECT_ROOT / config["paths"]["raw_pdfs"]).glob("*.pdf"))),
            "Markdown extraído": len(list((PROJECT_ROOT / config["paths"]["extracted_md"]).glob("*.md"))),
            "Markdown limpio": len(list((PROJECT_ROOT / config["paths"]["clean_md"]).glob("*.md"))),
            "Chunks JSONL": (PROJECT_ROOT / config["paths"]["chunks"] / "chunks.jsonl").exists(),
            "Índice vectorial": (PROJECT_ROOT / config["paths"]["vector_index"] / "index.faiss").exists(),
            "Índice BM25": (PROJECT_ROOT / config["paths"]["bm25_index"] / "bm25_index.pkl").exists(),
            "Modelo LLM": Path(PROJECT_ROOT / config["llm"]["model_path"]).exists(),
        }

        for name, value in checks.items():
            icon = "✓" if value else "✗"
            print(f"  {icon} {name}: {value}")

        if not any(v for v in checks.values()):
            print("\n  ⏳ ESPERANDO PDFs EN data/incoming_pdfs/")

        return

    if args.action == "query":
        if not args.question:
            print("[ERROR] Debe proporcionar una pregunta.")
            print("  Uso: python -m app.rag_engine query \"¿Mi pregunta?\"")
            sys.exit(1)

        require_pdfs("consultas RAG")

        engine = RAGEngine()
        engine.load_indexes()
        result = engine.query(args.question, args.mode)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result["answer"])


if __name__ == "__main__":
    main()
