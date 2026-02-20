#!/usr/bin/env python3
"""
app/clean.py — Limpieza y normalización de Markdown

Aplica reglas anti-ruido (§4.1) al Markdown extraído:
- Elimina dot leaders (índices con puntos)
- Colapsa espacios/tabs/saltos múltiples inútiles
- Elimina cabeceras/pies repetitivos
- Repara guiones de salto de línea
- Preserva bloques de código, rutas, CVEs, comandos (§4.2)

Uso:
    python -m app.clean
    make clean
"""

import re
import sys
from pathlib import Path
from collections import Counter

from app.utils import (
    load_config,
    require_pdfs,
    ensure_dir,
    print_header,
    PROJECT_ROOT,
)


# ── Patrones anti-ruido ────────────────────────────────────

# Dot leaders: "CAPÍTULO 3 .................................. 45"
RE_DOT_LEADERS = re.compile(
    r"^.*?\.{4,}\s*\d*\s*$", re.MULTILINE
)

# Secuencias de espacios inútiles (más de 3 espacios seguidos)
RE_EXCESS_SPACES = re.compile(r"[ \t]{4,}")

# Múltiples líneas en blanco (más de 2)
RE_EXCESS_NEWLINES = re.compile(r"\n{4,}")

# Guiones de salto de línea: "imple-\nmentación" → "implementación"
RE_HYPHEN_BREAK = re.compile(r"(\w)-\n(\w)")

# Líneas que son solo espacios/tabs
RE_BLANK_LINES = re.compile(r"^[ \t]+$", re.MULTILINE)

# Numeración de página suelta: solo un número en una línea
RE_PAGE_NUMBER = re.compile(r"^\s*\d{1,4}\s*$", re.MULTILINE)


def detect_repeated_headers_footers(text: str, threshold: int = 3) -> list[str]:
    """
    Detecta líneas que se repiten demasiadas veces (cabeceras/pies).

    Args:
        text: Texto completo del documento.
        threshold: Número mínimo de repeticiones para considerar ruido.

    Returns:
        Lista de líneas repetitivas a eliminar.
    """
    lines = text.split("\n")
    counter = Counter()

    for line in lines:
        stripped = line.strip()
        # Solo contar líneas no vacías y que no sean headers Markdown
        if stripped and not stripped.startswith("#") and not stripped.startswith("<!--"):
            counter[stripped] += 1

    # Líneas que aparecen más veces que el umbral
    repeated = [line for line, count in counter.items() if count >= threshold]
    return repeated


def is_code_block(lines: list[str], idx: int) -> bool:
    """Determina si la línea está dentro de un bloque de código."""
    in_code = False
    for i in range(idx):
        if lines[i].strip().startswith("```"):
            in_code = not in_code
    return in_code


def clean_markdown(text: str) -> tuple[str, dict]:
    """
    Aplica reglas de limpieza al texto Markdown.

    Returns:
        Tupla de (texto limpio, métricas de limpieza).
    """
    original_len = len(text)
    metrics = {
        "original_chars": original_len,
        "dot_leaders_removed": 0,
        "repeated_lines_removed": 0,
        "hyphen_breaks_fixed": 0,
        "excess_spaces_collapsed": 0,
    }

    # 1. Eliminar dot leaders
    matches = RE_DOT_LEADERS.findall(text)
    metrics["dot_leaders_removed"] = len(matches)
    text = RE_DOT_LEADERS.sub("", text)

    # 2. Detectar y eliminar headers/footers repetitivos
    repeated = detect_repeated_headers_footers(text)
    for line in repeated:
        count_before = text.count(line)
        text = text.replace(line + "\n", "")
        metrics["repeated_lines_removed"] += count_before

    # 3. Reparar guiones de salto de línea
    fixed = RE_HYPHEN_BREAK.findall(text)
    metrics["hyphen_breaks_fixed"] = len(fixed)
    text = RE_HYPHEN_BREAK.sub(r"\1\2", text)

    # 4. Colapsar espacios excesivos (fuera de bloques de código)
    lines = text.split("\n")
    cleaned_lines = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code:
            new_line = RE_EXCESS_SPACES.sub(" ", line)
            if new_line != line:
                metrics["excess_spaces_collapsed"] += 1
            line = new_line
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)

    # 5. Limpiar líneas que son solo espacios
    text = RE_BLANK_LINES.sub("", text)

    # 6. Eliminar números de página sueltos
    text = RE_PAGE_NUMBER.sub("", text)

    # 7. Colapsar saltos de línea excesivos
    text = RE_EXCESS_NEWLINES.sub("\n\n\n", text)

    # 8. Trim final
    text = text.strip() + "\n"

    metrics["clean_chars"] = len(text)
    metrics["reduction_percent"] = round(
        (1 - len(text) / max(original_len, 1)) * 100, 1
    )

    return text, metrics


def main():
    print_header("LIMPIEZA DE MARKDOWN")
    require_pdfs("limpieza")

    config = load_config()
    input_dir = PROJECT_ROOT / config["paths"]["extracted_md"]
    output_dir = PROJECT_ROOT / config["paths"]["clean_md"]
    ensure_dir(output_dir)

    md_files = sorted(input_dir.glob("*.md"))

    if not md_files:
        print("  No hay archivos Markdown en 02_extracted_md/ para limpiar.")
        print("  Ejecute primero: make extract")
        return

    print(f"  Procesando {len(md_files)} archivo(s)...\n")

    all_metrics = []
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            text = f.read()

        clean_text, metrics = clean_markdown(text)
        metrics["file"] = md_file.name

        output_file = output_dir / md_file.name
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(clean_text)

        print(f"  📝 {md_file.name}: {metrics['reduction_percent']}% reducido "
              f"({metrics['dot_leaders_removed']} dot-leaders, "
              f"{metrics['hyphen_breaks_fixed']} guiones reparados)")

        all_metrics.append(metrics)

    # Resumen
    total_reduction = sum(m["reduction_percent"] for m in all_metrics) / max(len(all_metrics), 1)
    print(f"\n  Reducción media: {total_reduction:.1f}%")
    print("  Siguiente paso: make chunk")


if __name__ == "__main__":
    main()
