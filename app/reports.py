#!/usr/bin/env python3
"""
app/reports.py — Generación de reportes por iteración

Genera los reportes obligatorios (§3.2):
- corpus_inventory.csv
- chunking_report.md
- index_report.md

Uso:
    python -m app.reports
    make reports
"""

import csv
import json
import sys
from pathlib import Path

from app.utils import (
    load_config,
    require_pdfs,
    sha256_file,
    ensure_dir,
    print_header,
    PROJECT_ROOT,
)


def generate_corpus_inventory() -> str:
    """Genera reports/corpus_inventory.csv."""
    config = load_config()
    raw_dir = PROJECT_ROOT / config["paths"]["raw_pdfs"]
    reports_dir = ensure_dir(PROJECT_ROOT / "reports")
    output = reports_dir / "corpus_inventory.csv"

    rows = []
    if raw_dir.exists():
        for pdf in sorted(raw_dir.glob("*.pdf")):
            stat = pdf.stat()
            rows.append({
                "archivo": pdf.name,
                "tamaño_kb": round(stat.st_size / 1024, 1),
                "hash_sha256": sha256_file(pdf)[:16] + "...",
                "idioma": "por determinar",
                "paginas": "por determinar",
                "fecha_ingesta": "",
                "flags": "",
            })

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "archivo", "tamaño_kb", "hash_sha256", "idioma",
            "paginas", "fecha_ingesta", "flags",
        ])
        writer.writeheader()
        writer.writerows(rows)

    return str(output)


def generate_chunking_report() -> str:
    """Genera reports/chunking_report.md."""
    config = load_config()
    chunks_path = PROJECT_ROOT / config["paths"]["chunks"] / "chunks.jsonl"
    qa_path = PROJECT_ROOT / config["paths"]["chunks"] / "chunks_qa.json"
    reports_dir = ensure_dir(PROJECT_ROOT / "reports")
    output = reports_dir / "chunking_report.md"

    lines = ["# Reporte de Chunking\n"]

    if not chunks_path.exists():
        lines.append("No hay chunks generados todavía.\n")
        lines.append("Ejecute: `make chunk`\n")
    else:
        # Cargar chunks
        chunks = []
        with open(chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    chunks.append(json.loads(line))

        token_counts = [c.get("tokens_est", 0) for c in chunks]

        lines.append(f"**Fecha**: generado automáticamente\n")
        lines.append(f"## Resumen\n")
        lines.append(f"- Total de chunks: **{len(chunks)}**\n")
        lines.append(f"- Tokens promedio: **{sum(token_counts) // max(len(token_counts), 1)}**\n")
        lines.append(f"- Tokens mínimo: **{min(token_counts, default=0)}**\n")
        lines.append(f"- Tokens máximo: **{max(token_counts, default=0)}**\n")

        # Distribución por tipo de documento
        by_type = {}
        for c in chunks:
            dt = c.get("doc_type", "unknown")
            by_type[dt] = by_type.get(dt, 0) + 1

        lines.append(f"\n## Distribución por tipo de documento\n")
        lines.append("| Tipo | Chunks |\n|------|--------|\n")
        for dt, count in sorted(by_type.items()):
            lines.append(f"| {dt} | {count} |\n")

        # Distribución por idioma
        by_lang = {}
        for c in chunks:
            lang = c.get("lang", "unknown")
            by_lang[lang] = by_lang.get(lang, 0) + 1

        lines.append(f"\n## Distribución por idioma\n")
        lines.append("| Idioma | Chunks |\n|--------|--------|\n")
        for lang, count in sorted(by_lang.items()):
            lines.append(f"| {lang} | {count} |\n")

        # Distribución de tamaños
        lines.append(f"\n## Distribución de tamaños (tokens estimados)\n")
        ranges = [(0, 100), (100, 300), (300, 600), (600, 900), (900, float("inf"))]
        labels = ["<100", "100-300", "300-600", "600-900", ">900"]
        for (lo, hi), label in zip(ranges, labels):
            count = sum(1 for t in token_counts if lo <= t < hi)
            lines.append(f"- {label}: {count} chunks\n")

    with open(output, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return str(output)


def generate_index_report() -> str:
    """Genera reports/index_report.md."""
    config = load_config()
    reports_dir = ensure_dir(PROJECT_ROOT / "reports")
    output = reports_dir / "index_report.md"

    lines = ["# Reporte de Indexación\n"]

    vector_path = PROJECT_ROOT / config["paths"]["vector_index"] / "index.faiss"
    bm25_path = PROJECT_ROOT / config["paths"]["bm25_index"] / "bm25_index.pkl"

    if not vector_path.exists():
        lines.append("No hay índices generados todavía.\n")
        lines.append("Ejecute: `make index`\n")
    else:
        size_mb = vector_path.stat().st_size / 1024 / 1024
        lines.append(f"## Índice vectorial (FAISS)\n")
        lines.append(f"- Archivo: `index.faiss`\n")
        lines.append(f"- Tamaño: **{size_mb:.2f} MB**\n")
        lines.append(f"- Hash: `{sha256_file(vector_path)[:16]}...`\n")

        emb_config = config.get("embeddings", {})
        lines.append(f"- Modelo: `{emb_config.get('model_name', 'n/d')}`\n")
        lines.append(f"- Dimensión: {emb_config.get('dimension', 'n/d')}\n")

    if bm25_path.exists():
        size_mb = bm25_path.stat().st_size / 1024 / 1024
        lines.append(f"\n## Índice BM25\n")
        lines.append(f"- Archivo: `bm25_index.pkl`\n")
        lines.append(f"- Tamaño: **{size_mb:.2f} MB**\n")

    # Configuración de retrieval
    import yaml
    retrieval_path = PROJECT_ROOT / "configs" / "retrieval.yml"
    if retrieval_path.exists():
        with open(retrieval_path, "r") as f:
            retrieval = yaml.safe_load(f)
        search = retrieval.get("search", {})
        lines.append(f"\n## Parámetros de búsqueda\n")
        lines.append(f"- Modo: `{search.get('mode', 'n/d')}`\n")
        lines.append(f"- Top-K: {search.get('top_k', 'n/d')}\n")
        lines.append(f"- Umbral mínimo: {search.get('min_score', 'n/d')}\n")

    with open(output, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return str(output)


def main():
    print_header("GENERACIÓN DE REPORTES")
    require_pdfs("generación de reportes")

    inv = generate_corpus_inventory()
    print(f"  ✓ Inventario: {inv}")

    chunk_rpt = generate_chunking_report()
    print(f"  ✓ Chunking: {chunk_rpt}")

    idx_rpt = generate_index_report()
    print(f"  ✓ Indexación: {idx_rpt}")

    print("\n  Reportes generados en reports/")


if __name__ == "__main__":
    main()
