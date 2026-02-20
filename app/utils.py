#!/usr/bin/env python3
"""
app/utils.py — Utilidades compartidas

Funciones auxiliares usadas por múltiples módulos del pipeline.
"""

import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime

import yaml


# ── Constantes ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"
INCOMING_DIR = DATA_DIR / "incoming_pdfs"


def load_config(name: str = "CONFIG.yml") -> dict:
    """Carga un archivo YAML de configuración desde configs/."""
    path = CONFIGS_DIR / name
    if not path.exists():
        print(f"[ERROR] Archivo de configuración no encontrado: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_pdfs_available() -> bool:
    """Comprueba si hay PDFs en data/incoming_pdfs/ o data/01_raw_pdfs/."""
    incoming = DATA_DIR / "incoming_pdfs"
    raw = DATA_DIR / "01_raw_pdfs"
    for d in [incoming, raw]:
        if d.exists():
            pdfs = list(d.glob("*.pdf")) + list(d.glob("*.PDF"))
            if pdfs:
                return True
    return False


def require_pdfs(action: str = "esta acción"):
    """Aborta con mensaje claro si no hay PDFs disponibles."""
    if not check_pdfs_available():
        print()
        print("=" * 60)
        print("  ⏳ ESPERANDO PDFs EN data/incoming_pdfs/")
        print("=" * 60)
        print()
        print(f"  No se puede ejecutar {action}.")
        print("  Coloque archivos PDF en la carpeta:")
        print(f"    {DATA_DIR / 'incoming_pdfs'}/")
        print()
        print("  Luego ejecute de nuevo el comando.")
        print("=" * 60)
        sys.exit(0)


def sha256_file(filepath: str | Path) -> str:
    """Calcula el hash SHA-256 de un archivo."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    """Calcula el hash SHA-256 de un string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def timestamp() -> str:
    """Genera un timestamp en formato YYYYMMDD-HHMMSS."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def ensure_dir(path: Path) -> Path:
    """Crea un directorio si no existe y lo devuelve."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def count_pdfs(directory: Path) -> int:
    """Cuenta archivos PDF en un directorio."""
    if not directory.exists():
        return 0
    return len(list(directory.glob("*.pdf")) + list(directory.glob("*.PDF")))


def print_header(title: str):
    """Imprime un encabezado formateado."""
    width = max(len(title) + 4, 50)
    print()
    print("═" * width)
    print(f"  {title}")
    print("═" * width)
    print()
