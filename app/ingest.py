#!/usr/bin/env python3
"""
app/ingest.py — Pipeline de ingesta de PDFs

Detecta PDFs nuevos en data/incoming_pdfs/, los valida y mueve
a data/01_raw_pdfs/ para su procesamiento.

Uso:
    python -m app.ingest
    make ingest
"""

import shutil
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


def validate_pdf(filepath: Path) -> bool:
    """Valida que un archivo sea un PDF válido (magic bytes)."""
    try:
        with open(filepath, "rb") as f:
            header = f.read(5)
        return header == b"%PDF-"
    except Exception as e:
        print(f"  [WARN] No se pudo leer {filepath.name}: {e}")
        return False


def ingest_pdfs() -> list[dict]:
    """
    Procesa PDFs desde incoming_pdfs/ hacia 01_raw_pdfs/.

    Returns:
        Lista de diccionarios con info de archivos procesados.
    """
    config = load_config()
    incoming = PROJECT_ROOT / config["paths"]["incoming_pdfs"]
    raw_dir = PROJECT_ROOT / config["paths"]["raw_pdfs"]
    ensure_dir(raw_dir)

    pdfs = sorted(
        list(incoming.glob("*.pdf")) + list(incoming.glob("*.PDF"))
    )

    if not pdfs:
        print("  No hay PDFs nuevos en incoming_pdfs/.")
        return []

    results = []
    print(f"  Encontrados {len(pdfs)} PDF(s) nuevos.\n")

    for pdf in pdfs:
        print(f"  📄 {pdf.name}")

        # Validar
        if not validate_pdf(pdf):
            print(f"    ✗ No es un PDF válido. Omitido.")
            results.append({
                "file": pdf.name,
                "status": "invalid",
                "reason": "No es un PDF válido",
            })
            continue

        # Calcular hash
        file_hash = sha256_file(pdf)
        dest = raw_dir / pdf.name

        # Comprobar duplicados
        if dest.exists():
            existing_hash = sha256_file(dest)
            if existing_hash == file_hash:
                print(f"    ⚠ Ya existe (mismo hash). Omitido.")
                # Eliminar de incoming para no reprocesar
                pdf.unlink()
                results.append({
                    "file": pdf.name,
                    "status": "duplicate",
                    "hash": file_hash,
                })
                continue
            else:
                # Archivo con mismo nombre pero contenido diferente
                stem = pdf.stem
                suffix = pdf.suffix
                ts = timestamp()
                dest = raw_dir / f"{stem}_{ts}{suffix}"
                print(f"    ℹ Nombre duplicado, renombrado a: {dest.name}")

        # Mover
        shutil.move(str(pdf), str(dest))
        size_kb = dest.stat().st_size / 1024
        print(f"    ✓ Movido a 01_raw_pdfs/ ({size_kb:.1f} KB, hash: {file_hash[:12]}...)")

        results.append({
            "file": dest.name,
            "status": "ingested",
            "hash": file_hash,
            "size_bytes": dest.stat().st_size,
            "destination": str(dest.relative_to(PROJECT_ROOT)),
        })

    return results


def main():
    print_header("INGESTA DE PDFs")
    require_pdfs("ingesta")
    results = ingest_pdfs()

    # Resumen
    ingested = sum(1 for r in results if r["status"] == "ingested")
    skipped = sum(1 for r in results if r["status"] != "ingested")
    print(f"\n  Resultado: {ingested} ingresado(s), {skipped} omitido(s).")
    print("  Siguiente paso: make extract")


if __name__ == "__main__":
    main()
