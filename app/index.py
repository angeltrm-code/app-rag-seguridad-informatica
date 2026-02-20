#!/usr/bin/env python3
"""
app/index.py — Indexación vectorial (FAISS) y BM25

Construye índices a partir de chunks.jsonl para búsqueda RAG.

Uso:
    python -m app.index
    make index
"""

import json
import pickle
import sys
import time
from pathlib import Path

import numpy as np

from app.utils import (
    load_config,
    require_pdfs,
    ensure_dir,
    print_header,
    PROJECT_ROOT,
)


def load_chunks(chunks_path: Path) -> list[dict]:
    """Carga chunks desde JSONL."""
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def build_vector_index(chunks: list[dict], config: dict) -> dict:
    """
    Construye índice FAISS con sentence-transformers.

    Returns:
        dict con estadísticas.
    """
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
    except ImportError as e:
        print(f"[ERROR] Dependencia no instalada: {e}")
        print("  Ejecute: pip install sentence-transformers faiss-cpu")
        sys.exit(1)

    emb_config = config.get("embeddings", {})
    model_name = emb_config.get("model_name",
                                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    device = emb_config.get("device", "cpu")
    batch_size = emb_config.get("batch_size", 64)
    dimension = emb_config.get("dimension", 384)

    print(f"  Modelo: {model_name}")
    print(f"  Dispositivo: {device}")
    print(f"  Chunks a indexar: {len(chunks)}")

    # Cargar modelo
    print("  Cargando modelo de embeddings...")
    t0 = time.time()
    model = SentenceTransformer(model_name, device=device)
    load_time = time.time() - t0
    print(f"  Modelo cargado en {load_time:.1f}s")

    # Generar embeddings
    texts = [c["content"] for c in chunks]
    print(f"  Generando embeddings (batch_size={batch_size})...")
    t0 = time.time()
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=emb_config.get("normalize", True),
    )
    embed_time = time.time() - t0
    print(f"  Embeddings generados en {embed_time:.1f}s")

    # Construir índice FAISS
    print("  Construyendo índice FAISS...")
    embeddings_np = np.array(embeddings, dtype="float32")
    index = faiss.IndexFlatIP(embeddings_np.shape[1])  # Inner product (coseno si normalizado)
    index.add(embeddings_np)

    # Guardar
    vector_dir = ensure_dir(PROJECT_ROOT / config["paths"]["vector_index"])
    faiss.write_index(index, str(vector_dir / "index.faiss"))

    # Guardar mapping chunk_id → posición
    chunk_ids = [c["chunk_id"] for c in chunks]
    with open(vector_dir / "chunk_ids.pkl", "wb") as f:
        pickle.dump(chunk_ids, f)

    # Guardar metadatos de chunks
    meta_dir = ensure_dir(PROJECT_ROOT / config["paths"]["metadata_store"])
    chunk_metadata = {c["chunk_id"]: {k: v for k, v in c.items() if k != "content"}
                      for c in chunks}
    with open(meta_dir / "chunks_metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunk_metadata, f, indent=2, ensure_ascii=False)

    stats = {
        "model": model_name,
        "dimension": embeddings_np.shape[1],
        "num_vectors": index.ntotal,
        "load_time_s": round(load_time, 1),
        "embed_time_s": round(embed_time, 1),
        "index_size_mb": round(
            (vector_dir / "index.faiss").stat().st_size / 1024 / 1024, 2
        ),
    }

    return stats


def build_bm25_index(chunks: list[dict], config: dict) -> dict | None:
    """Construye índice BM25 (opcional)."""
    try:
        from rank_bm25 import BM25Okapi
    except ImportError:
        print("  [INFO] rank-bm25 no instalado. BM25 omitido.")
        return None

    print("  Construyendo índice BM25...")
    t0 = time.time()

    # Tokenizar por espacios (simple)
    corpus = [c["content"].lower().split() for c in chunks]
    bm25 = BM25Okapi(corpus)

    bm25_dir = ensure_dir(PROJECT_ROOT / config["paths"]["bm25_index"])
    with open(bm25_dir / "bm25_index.pkl", "wb") as f:
        pickle.dump(bm25, f)

    # Guardar chunk_ids en orden
    chunk_ids = [c["chunk_id"] for c in chunks]
    with open(bm25_dir / "chunk_ids.pkl", "wb") as f:
        pickle.dump(chunk_ids, f)

    bm25_time = time.time() - t0
    print(f"  BM25 construido en {bm25_time:.1f}s")

    return {
        "num_documents": len(chunks),
        "build_time_s": round(bm25_time, 1),
    }


def main():
    print_header("INDEXACIÓN VECTORIAL + BM25")
    require_pdfs("indexación")

    config = load_config()
    chunks_path = PROJECT_ROOT / config["paths"]["chunks"] / "chunks.jsonl"

    if not chunks_path.exists():
        print("  No se encontró chunks.jsonl.")
        print("  Ejecute primero: make chunk")
        return

    chunks = load_chunks(chunks_path)
    if not chunks:
        print("  chunks.jsonl está vacío.")
        return

    print(f"  Cargados {len(chunks)} chunks.\n")

    # Vector index
    vector_stats = build_vector_index(chunks, config)
    print(f"\n  ✓ Índice vectorial: {vector_stats['num_vectors']} vectores, "
          f"{vector_stats['index_size_mb']} MB")

    # BM25 (opcional)
    retrieval_config_path = PROJECT_ROOT / "configs" / "retrieval.yml"
    import yaml
    with open(retrieval_config_path, "r") as f:
        retrieval_config = yaml.safe_load(f)

    mode = retrieval_config.get("search", {}).get("mode", "vector")
    bm25_stats = None
    if mode in ("bm25", "hybrid"):
        bm25_stats = build_bm25_index(chunks, config)
        if bm25_stats:
            print(f"  ✓ Índice BM25: {bm25_stats['num_documents']} documentos")

    print("\n  Indexación completada.")
    print("  Siguiente paso: make reports  (o  make serve  para usar)")


if __name__ == "__main__":
    main()
