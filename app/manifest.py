#!/usr/bin/env python3
"""
app/manifest.py — Generación de manifiestos versionados por iteración

Genera un manifiesto JSON con la foto completa del estado del corpus:
archivos, hashes, versiones de config, parámetros, etc.

Uso:
    python -m app.manifest
    make manifest
"""

import json
import sys
from pathlib import Path

from app.utils import (
    load_config,
    require_pdfs,
    sha256_file,
    timestamp,
    ensure_dir,
    print_header,
    PROJECT_ROOT,
)


def generate_manifest() -> dict:
    """Genera un manifiesto completo del estado actual del sistema."""
    config = load_config()
    ts = timestamp()

    manifest = {
        "manifest_id": f"manifest-{ts}",
        "timestamp": ts,
        "project_version": config.get("project", {}).get("version", "0.1.0"),
        "corpus": {
            "raw_pdfs": [],
            "extracted_md": [],
            "clean_md": [],
            "chunks": None,
        },
        "indexes": {
            "vector": None,
            "bm25": None,
        },
        "config_hashes": {},
        "parameters": {
            "chunking": {},
            "retrieval": {},
            "embeddings": config.get("embeddings", {}),
            "llm": {k: v for k, v in config.get("llm", {}).items()
                    if k != "model_path"},
        },
    }

    # Inventariar PDFs crudos
    raw_dir = PROJECT_ROOT / config["paths"]["raw_pdfs"]
    if raw_dir.exists():
        for pdf in sorted(raw_dir.glob("*.pdf")):
            manifest["corpus"]["raw_pdfs"].append({
                "file": pdf.name,
                "size_bytes": pdf.stat().st_size,
                "hash": sha256_file(pdf),
            })

    # Inventariar Markdown extraído
    ext_dir = PROJECT_ROOT / config["paths"]["extracted_md"]
    if ext_dir.exists():
        for md in sorted(ext_dir.glob("*.md")):
            manifest["corpus"]["extracted_md"].append({
                "file": md.name,
                "size_bytes": md.stat().st_size,
                "hash": sha256_file(md),
            })

    # Inventariar Markdown limpio
    clean_dir = PROJECT_ROOT / config["paths"]["clean_md"]
    if clean_dir.exists():
        for md in sorted(clean_dir.glob("*.md")):
            manifest["corpus"]["clean_md"].append({
                "file": md.name,
                "size_bytes": md.stat().st_size,
                "hash": sha256_file(md),
            })

    # Chunks
    chunks_path = PROJECT_ROOT / config["paths"]["chunks"] / "chunks.jsonl"
    if chunks_path.exists():
        with open(chunks_path, "r", encoding="utf-8") as f:
            num_chunks = sum(1 for line in f if line.strip())
        manifest["corpus"]["chunks"] = {
            "file": "chunks.jsonl",
            "size_bytes": chunks_path.stat().st_size,
            "hash": sha256_file(chunks_path),
            "num_chunks": num_chunks,
        }

    # Índices
    vector_path = PROJECT_ROOT / config["paths"]["vector_index"] / "index.faiss"
    if vector_path.exists():
        manifest["indexes"]["vector"] = {
            "file": "index.faiss",
            "size_bytes": vector_path.stat().st_size,
            "hash": sha256_file(vector_path),
        }

    bm25_path = PROJECT_ROOT / config["paths"]["bm25_index"] / "bm25_index.pkl"
    if bm25_path.exists():
        manifest["indexes"]["bm25"] = {
            "file": "bm25_index.pkl",
            "size_bytes": bm25_path.stat().st_size,
            "hash": sha256_file(bm25_path),
        }

    # Hashes de configuración
    for config_file in (PROJECT_ROOT / "configs").glob("*.yml"):
        manifest["config_hashes"][config_file.name] = sha256_file(config_file)

    # Parámetros de chunking y retrieval
    import yaml
    for name in ["chunking", "retrieval"]:
        cfg_path = PROJECT_ROOT / "configs" / f"{name}.yml"
        if cfg_path.exists():
            with open(cfg_path, "r", encoding="utf-8") as f:
                manifest["parameters"][name] = yaml.safe_load(f)

    return manifest


def main():
    print_header("GENERACIÓN DE MANIFIESTO")
    require_pdfs("generación de manifiesto")

    manifest = generate_manifest()
    ts = manifest["timestamp"]

    # Guardar
    manifests_dir = ensure_dir(PROJECT_ROOT / "manifests")
    output_path = manifests_dir / f"manifest-{ts}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Resumen
    n_pdfs = len(manifest["corpus"]["raw_pdfs"])
    n_chunks = manifest["corpus"]["chunks"]["num_chunks"] if manifest["corpus"]["chunks"] else 0
    has_vector = manifest["indexes"]["vector"] is not None

    print(f"  📋 Manifiesto: {output_path.name}")
    print(f"     PDFs: {n_pdfs}")
    print(f"     Chunks: {n_chunks}")
    print(f"     Índice vectorial: {'✓' if has_vector else '✗'}")


if __name__ == "__main__":
    main()
