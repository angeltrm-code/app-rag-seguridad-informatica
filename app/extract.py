#!/usr/bin/env python3
"""
app/extract.py — Extracción de PDF a Markdown

Convierte PDFs de data/01_raw_pdfs/ a Markdown en data/02_extracted_md/.
Usa PyMuPDF (fitz) para extracción de texto con metadata de páginas.

Uso:
    python -m app.extract
    make extract
"""

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


def extract_pdf_to_markdown(pdf_path: Path, output_dir: Path) -> dict:
    """
    Extrae texto de un PDF y lo guarda como Markdown.

    Args:
        pdf_path: Ruta al archivo PDF.
        output_dir: Directorio de salida para el Markdown.

    Returns:
        Diccionario con metadatos de la extracción.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("[ERROR] PyMuPDF no instalado. Ejecute: pip install pymupdf")
        sys.exit(1)

    output_file = output_dir / f"{pdf_path.stem}.md"
    metadata = {
        "source_file": pdf_path.name,
        "output_file": output_file.name,
        "pages": 0,
        "characters": 0,
        "status": "pending",
    }

    try:
        doc = fitz.open(str(pdf_path))
        metadata["pages"] = len(doc)

        lines = []
        lines.append(f"# {pdf_path.stem}\n")
        lines.append(f"<!-- source: {pdf_path.name} -->\n")
        lines.append(f"<!-- pages: {len(doc)} -->\n")
        lines.append(f"<!-- hash: {sha256_file(pdf_path)} -->\n\n")

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")

            if text.strip():
                lines.append(f"<!-- page: {page_num + 1} -->\n")
                lines.append(f"## Página {page_num + 1}\n\n")
                lines.append(text)
                lines.append("\n\n")

        doc.close()

        content = "".join(lines)
        metadata["characters"] = len(content)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        metadata["status"] = "ok"
        print(f"    ✓ {pdf_path.name} → {output_file.name} "
              f"({metadata['pages']} págs, {metadata['characters']} chars)")

    except Exception as e:
        metadata["status"] = "error"
        metadata["error"] = str(e)
        print(f"    ✗ {pdf_path.name}: {e}")

    return metadata


def main():
    print_header("EXTRACCIÓN PDF → MARKDOWN")
    require_pdfs("extracción")

    config = load_config()
    raw_dir = PROJECT_ROOT / config["paths"]["raw_pdfs"]
    output_dir = PROJECT_ROOT / config["paths"]["extracted_md"]
    ensure_dir(output_dir)

    pdfs = sorted(
        list(raw_dir.glob("*.pdf")) + list(raw_dir.glob("*.PDF"))
    )

    if not pdfs:
        print("  No hay PDFs en 01_raw_pdfs/ para extraer.")
        print("  Ejecute primero: make ingest")
        return

    print(f"  Procesando {len(pdfs)} PDF(s)...\n")

    results = []
    for pdf in pdfs:
        result = extract_pdf_to_markdown(pdf, output_dir)
        results.append(result)

    # Resumen
    ok = sum(1 for r in results if r["status"] == "ok")
    errors = sum(1 for r in results if r["status"] == "error")
    print(f"\n  Resultado: {ok} extraído(s), {errors} error(es).")
    print("  Siguiente paso: make clean")


if __name__ == "__main__":
    main()
