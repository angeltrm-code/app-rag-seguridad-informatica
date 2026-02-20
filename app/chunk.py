#!/usr/bin/env python3
"""
app/chunk.py — Chunking de Markdown a JSONL

Divide documentos Markdown limpios en chunks con metadatos,
respetando las reglas de integridad estructural (§6).

Salida: data/04_chunks/chunks.jsonl

Uso:
    python -m app.chunk
    make chunk
"""

import json
import re
import sys
import uuid
from pathlib import Path

import yaml

from app.utils import (
    load_config,
    require_pdfs,
    sha256_text,
    ensure_dir,
    print_header,
    PROJECT_ROOT,
)


# ── Patrones ────────────────────────────────────────────────

RE_HEADER = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
RE_PAGE_MARKER = re.compile(r"<!--\s*page:\s*(\d+)\s*-->")
RE_CODE_BLOCK = re.compile(r"```[\s\S]*?```")
RE_TABLE_ROW = re.compile(r"^\|.*\|$")
RE_LIST_ITEM = re.compile(r"^\s*[-*+]\s+|^\s*\d+\.\s+")

# Patrones para tags de seguridad
RE_CVE = re.compile(r"CVE-\d{4}-\d{4,}")
RE_ATTACK = re.compile(r"T\d{4}(?:\.\d{3})?")


def load_chunking_config() -> dict:
    """Carga la configuración de chunking."""
    config_path = PROJECT_ROOT / "configs" / "chunking.yml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def estimate_tokens(text: str) -> int:
    """Estimación rápida de tokens (1 token ≈ 4 chars para español)."""
    return max(1, len(text) // 4)


def extract_page_numbers(text: str) -> tuple[int | None, int | None]:
    """Extrae números de página del texto (de marcadores <!-- page: N -->)."""
    pages = [int(m) for m in RE_PAGE_MARKER.findall(text)]
    if not pages:
        return None, None
    return min(pages), max(pages)


def detect_language(text: str) -> str:
    """Detecta idioma básico (ES/EN) por heurística."""
    es_words = {"de", "en", "la", "el", "los", "las", "del", "que", "para", "por",
                "con", "una", "se", "es", "al", "como", "más", "pero", "su", "ya"}
    words = set(text.lower().split()[:200])
    es_count = len(words & es_words)
    return "es" if es_count > 5 else "en"


def detect_doc_type(text: str, filename: str) -> str:
    """Intenta inferir el tipo de documento."""
    lower = (text[:2000] + filename).lower()
    type_hints = {
        "política": "politica",
        "policy": "politica",
        "runbook": "runbook",
        "procedimiento": "procedimiento",
        "procedure": "procedimiento",
        "guía": "guia",
        "guide": "guia",
        "manual": "guia",
        "norma": "normativa",
        "reglamento": "normativa",
        "regulation": "normativa",
        "estándar": "normativa",
        "standard": "normativa",
        "informe": "reporte",
        "report": "reporte",
    }
    for keyword, doc_type in type_hints.items():
        if keyword in lower:
            return doc_type
    return "guia"  # default


def extract_security_tags(text: str) -> list[str]:
    """Extrae tags de seguridad (CVE, ATT&CK, etc.)."""
    tags = []
    tags.extend(RE_CVE.findall(text))
    tags.extend(RE_ATTACK.findall(text))
    return list(set(tags))


def detect_frameworks(text: str) -> list[str]:
    """Detecta marcos de seguridad mencionados."""
    frameworks_patterns = {
        "ENS": r"\bENS\b",
        "CCN-STIC": r"\bCCN[-\s]?STIC\b",
        "NIST": r"\bNIST\b",
        "CIS": r"\bCIS\b",
        "OWASP": r"\bOWASP\b",
        "ISO 27001": r"\bISO\s*27001\b",
        "ISO 27002": r"\bISO\s*27002\b",
        "ENISA": r"\bENISA\b",
        "RGPD": r"\bRGPD\b|GDPR",
        "NIS2": r"\bNIS\s*2\b",
        "CISA": r"\bCISA\b",
    }
    found = []
    for name, pattern in frameworks_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found.append(name)
    return found


def split_by_headers(text: str) -> list[dict]:
    """
    Divide texto por encabezados Markdown, preservando la jerarquía.

    Returns:
        Lista de {'header': str, 'level': int, 'content': str, 'breadcrumb': str}
    """
    sections = []
    lines = text.split("\n")
    current_section = {"header": "", "level": 0, "lines": [], "breadcrumb": ""}
    breadcrumb_stack = []

    for line in lines:
        match = RE_HEADER.match(line)
        if match:
            # Guardar sección anterior
            if current_section["lines"]:
                current_section["content"] = "\n".join(current_section["lines"])
                sections.append(current_section)

            level = len(match.group(1))
            header = match.group(2).strip()

            # Actualizar breadcrumb
            while breadcrumb_stack and breadcrumb_stack[-1][0] >= level:
                breadcrumb_stack.pop()
            breadcrumb_stack.append((level, header))
            breadcrumb = " > ".join(h for _, h in breadcrumb_stack)

            current_section = {
                "header": header,
                "level": level,
                "lines": [],
                "breadcrumb": breadcrumb,
            }
        else:
            current_section["lines"].append(line)

    # Última sección
    if current_section["lines"]:
        current_section["content"] = "\n".join(current_section["lines"])
        sections.append(current_section)

    return sections


def should_merge_section(section: dict, config: dict) -> bool:
    """Determina si una sección es demasiado pequeña y debería fusionarse."""
    tokens = estimate_tokens(section.get("content", ""))
    return tokens < config.get("min_tokens", 300) // 2


def create_chunks(sections: list[dict], doc_id: str, source_file: str,
                  config: dict) -> list[dict]:
    """
    Crea chunks a partir de secciones, respetando tamaños y reglas de integridad.
    """
    max_tokens = config.get("max_tokens", 900)
    min_tokens = config.get("min_tokens", 300)
    overlap_tokens = config.get("overlap_tokens", 100)

    chunks = []
    buffer_text = ""
    buffer_breadcrumb = ""

    for section in sections:
        content = section.get("content", "").strip()
        if not content:
            continue

        breadcrumb = section.get("breadcrumb", "")
        tokens = estimate_tokens(content)

        # Si el buffer + sección cabe en max_tokens, acumular
        if buffer_text:
            combined_tokens = estimate_tokens(buffer_text + "\n\n" + content)
            if combined_tokens <= max_tokens:
                buffer_text += "\n\n" + content
                continue

            # Emitir buffer como chunk
            page_start, page_end = extract_page_numbers(buffer_text)
            chunk = {
                "doc_id": doc_id,
                "chunk_id": str(uuid.uuid4())[:12],
                "source_file": source_file,
                "section_path": buffer_breadcrumb,
                "page_start": page_start,
                "page_end": page_end,
                "lang": detect_language(buffer_text),
                "content": buffer_text.strip(),
                "tokens_est": estimate_tokens(buffer_text),
            }
            chunks.append(chunk)
            buffer_text = ""

        # Si la sección es muy pequeña, bufferizar
        if tokens < min_tokens:
            buffer_text = content
            buffer_breadcrumb = breadcrumb
            continue

        # Si la sección cabe en max_tokens, emitir directamente
        if tokens <= max_tokens:
            page_start, page_end = extract_page_numbers(content)
            chunk = {
                "doc_id": doc_id,
                "chunk_id": str(uuid.uuid4())[:12],
                "source_file": source_file,
                "section_path": breadcrumb,
                "page_start": page_start,
                "page_end": page_end,
                "lang": detect_language(content),
                "content": content.strip(),
                "tokens_est": tokens,
            }
            chunks.append(chunk)
        else:
            # Sección demasiado grande: dividir por párrafos
            paragraphs = content.split("\n\n")
            current_chunk_text = ""

            for para in paragraphs:
                para_tokens = estimate_tokens(para)
                current_tokens = estimate_tokens(current_chunk_text)

                if current_tokens + para_tokens <= max_tokens:
                    current_chunk_text += ("\n\n" if current_chunk_text else "") + para
                else:
                    if current_chunk_text.strip():
                        page_start, page_end = extract_page_numbers(current_chunk_text)
                        chunk = {
                            "doc_id": doc_id,
                            "chunk_id": str(uuid.uuid4())[:12],
                            "source_file": source_file,
                            "section_path": breadcrumb,
                            "page_start": page_start,
                            "page_end": page_end,
                            "lang": detect_language(current_chunk_text),
                            "content": current_chunk_text.strip(),
                            "tokens_est": estimate_tokens(current_chunk_text),
                        }
                        chunks.append(chunk)

                    current_chunk_text = para

            # Último fragmento
            if current_chunk_text.strip():
                page_start, page_end = extract_page_numbers(current_chunk_text)
                chunk = {
                    "doc_id": doc_id,
                    "chunk_id": str(uuid.uuid4())[:12],
                    "source_file": source_file,
                    "section_path": breadcrumb,
                    "page_start": page_start,
                    "page_end": page_end,
                    "lang": detect_language(current_chunk_text),
                    "content": current_chunk_text.strip(),
                    "tokens_est": estimate_tokens(current_chunk_text),
                }
                chunks.append(chunk)

    # Emitir buffer restante
    if buffer_text.strip():
        page_start, page_end = extract_page_numbers(buffer_text)
        chunk = {
            "doc_id": doc_id,
            "chunk_id": str(uuid.uuid4())[:12],
            "source_file": source_file,
            "section_path": buffer_breadcrumb,
            "page_start": page_start,
            "page_end": page_end,
            "lang": detect_language(buffer_text),
            "content": buffer_text.strip(),
            "tokens_est": estimate_tokens(buffer_text),
        }
        chunks.append(chunk)

    # Enriquecer con metadatos
    full_text = "\n".join(s.get("content", "") for s in sections)
    doc_type = detect_doc_type(full_text, source_file)
    frameworks = detect_frameworks(full_text)

    for chunk in chunks:
        chunk["doc_type"] = doc_type
        chunk["frameworks"] = frameworks if frameworks else []
        chunk["security_tags"] = extract_security_tags(chunk["content"])
        chunk["version"] = "1.0"

    return chunks


def main():
    print_header("CHUNKING DE MARKDOWN")
    require_pdfs("chunking")

    config = load_config()
    chunking_config = load_chunking_config()
    defaults = chunking_config.get("defaults", {})

    input_dir = PROJECT_ROOT / config["paths"]["clean_md"]
    output_dir = PROJECT_ROOT / config["paths"]["chunks"]
    ensure_dir(output_dir)

    md_files = sorted(input_dir.glob("*.md"))

    if not md_files:
        print("  No hay archivos Markdown en 03_clean_md/ para chunkear.")
        print("  Ejecute primero: make clean")
        return

    print(f"  Procesando {len(md_files)} archivo(s)...\n")

    all_chunks = []
    chunks_output = output_dir / "chunks.jsonl"

    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            text = f.read()

        doc_id = sha256_text(md_file.name)[:16]
        doc_type = detect_doc_type(text, md_file.name)

        # Seleccionar config por tipo de documento
        type_config = chunking_config.get("by_doc_type", {}).get(doc_type, defaults)

        sections = split_by_headers(text)
        chunks = create_chunks(sections, doc_id, md_file.name, type_config)

        print(f"  📦 {md_file.name}: {len(chunks)} chunks "
              f"(tipo: {doc_type}, tokens: "
              f"{sum(c['tokens_est'] for c in chunks)})")

        all_chunks.extend(chunks)

    # Escribir JSONL
    with open(chunks_output, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"\n  Total: {len(all_chunks)} chunks → {chunks_output.name}")

    # Escribir métricas QA
    qa_output = output_dir / "chunks_qa.json"
    qa_data = {
        "total_chunks": len(all_chunks),
        "files_processed": len(md_files),
        "avg_tokens": round(sum(c["tokens_est"] for c in all_chunks) / max(len(all_chunks), 1)),
        "min_tokens": min((c["tokens_est"] for c in all_chunks), default=0),
        "max_tokens": max((c["tokens_est"] for c in all_chunks), default=0),
        "by_doc_type": {},
        "by_language": {},
    }

    for chunk in all_chunks:
        dt = chunk.get("doc_type", "unknown")
        qa_data["by_doc_type"][dt] = qa_data["by_doc_type"].get(dt, 0) + 1
        lang = chunk.get("lang", "unknown")
        qa_data["by_language"][lang] = qa_data["by_language"].get(lang, 0) + 1

    with open(qa_output, "w", encoding="utf-8") as f:
        json.dump(qa_data, f, indent=2, ensure_ascii=False)

    print(f"  Métricas QA → {qa_output.name}")
    print("  Siguiente paso: make index")


if __name__ == "__main__":
    main()
