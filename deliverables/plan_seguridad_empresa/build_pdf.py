#!/usr/bin/env python3
"""
build_pdf.py — Genera Plan_Seguridad_Empresa.pdf desde Markdown
Usa: WeasyPrint (Python, sin dependencias externas fuera del venv)

Proceso:
  1. Lee Plan_Seguridad_Empresa.md
  2. Añade portada corporativa HTML
  3. Convierte Markdown → HTML con tabla de contenidos
  4. Aplica template.css
  5. Genera PDF con WeasyPrint

Uso:
    python build_pdf.py
    python build_pdf.py --output Plan_Seguridad_Empresa.pdf
"""

import argparse
import re
import sys
from pathlib import Path


def build_cover_html() -> str:
    """Genera la portada corporativa en HTML."""
    return """
<div class="cover-page">
  <div class="cover-top-bar"></div>
  <div class="cover-content">
    <div class="cover-logo-area">
      <div class="cover-logo-placeholder">LOGO {CLIENTE}</div>
    </div>
    <h1 class="cover-title">Plan de Seguridad<br>Informática Integral</h1>
    <p class="cover-subtitle">
      Diseño, implementación y auditoría del sistema<br>
      de seguridad de la información para {CLIENTE}
    </p>
    <div class="cover-meta-grid">
      <div class="cover-meta-item">
        <div class="cover-meta-label">Cliente</div>
        <div class="cover-meta-value">{CLIENTE}</div>
      </div>
      <div class="cover-meta-item">
        <div class="cover-meta-label">Versión</div>
        <div class="cover-meta-value">{VERSIÓN}</div>
      </div>
      <div class="cover-meta-item">
        <div class="cover-meta-label">Fecha</div>
        <div class="cover-meta-value">2026-02-20</div>
      </div>
      <div class="cover-meta-item">
        <div class="cover-meta-label">Clasificación</div>
        <div class="cover-meta-value">{CONFIDENCIALIDAD}</div>
      </div>
      <div class="cover-meta-item">
        <div class="cover-meta-label">Autor</div>
        <div class="cover-meta-value">{AUTOR}</div>
      </div>
      <div class="cover-meta-item">
        <div class="cover-meta-label">Fuentes</div>
        <div class="cover-meta-value">59 documentos / 8.580 fragmentos</div>
      </div>
    </div>
  </div>
  <div class="cover-bottom-bar"></div>
</div>
"""


def build_control_table_html() -> str:
    """Genera la tabla de control de cambios."""
    return """
<div class="page-break"></div>
<h1>Control de Cambios</h1>
<div class="control-table">
<table>
<thead>
<tr><th>Versión</th><th>Fecha</th><th>Autor</th><th>Descripción</th></tr>
</thead>
<tbody>
<tr>
  <td>1.0</td>
  <td>2026-02-20</td>
  <td>{AUTOR}</td>
  <td>Versión inicial — generada desde corpus RAG (70 PDFs, 8.580 chunks)</td>
</tr>
</tbody>
</table>
</div>
"""


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    """Genera tabla de contenidos HTML."""
    lines = ['<div class="page-break toc-page">', '<h1>Índice</h1>', '<ul class="toc-list">']
    for level, text, anchor in headings:
        cls = "toc-l1" if level == 1 else "toc-l2"
        lines.append(f'  <li class="{cls}"><a href="#{anchor}">{text}</a></li>')
    lines.append('</ul></div>')
    return '\n'.join(lines)


def replace_priority_emojis(html: str) -> str:
    """Reemplaza emojis de prioridad por badges HTML."""
    replacements = [
        ('🔴 Crítica', '<span class="prio-critica">CRÍTICA</span>'),
        ('🟠 Alta', '<span class="prio-alta">ALTA</span>'),
        ('🟡 Media', '<span class="prio-media">MEDIA</span>'),
        ('🟢 Normal', '<span class="prio-normal">NORMAL</span>'),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    return html


def wrap_fuentes_sections(html: str) -> str:
    """Envuelve secciones 'Fuentes:' en un div estilizado."""
    # Pattern: <p><strong>Fuentes:</strong></p> followed by <ul>...</ul>
    pattern = r'(<p><strong>Fuentes:?</strong></p>\s*<ul>.*?</ul>)'
    html = re.sub(pattern, r'<div class="fuentes-section">\1</div>', html, flags=re.DOTALL)

    # Also handle cases like <p><strong>Fuentes</strong></p>
    pattern2 = r'(<p><strong>Fuentes</strong></p>\s*<ul>.*?</ul>)'
    html = re.sub(pattern2, r'<div class="fuentes-section">\1</div>', html, flags=re.DOTALL)

    return html


def replace_check_marks(html: str) -> str:
    """Reemplaza ✅ y ⚠️ con spans coloreados."""
    html = html.replace('✅', '<span class="mark-ok">✔</span>')
    html = html.replace('⚠️', '<span class="mark-warn">⚠</span>')
    html = html.replace('✗', '<span class="mark-fail">✗</span>')
    html = html.replace('✓', '<span class="mark-ok">✓</span>')
    return html


def extract_headings(html: str) -> list[tuple[int, str, str]]:
    """Extrae headings del HTML y les asigna IDs."""
    headings = []
    counter = [0, 0]  # h1, h2

    def replace_heading(match):
        level = int(match.group(1))
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        if level == 1:
            counter[0] += 1
            counter[1] = 0
            num = str(counter[0])
        else:
            counter[1] += 1
            num = f"{counter[0]}.{counter[1]}"
        anchor = f"sec-{num.replace('.', '-')}"
        headings.append((level, f"{num}. {text}", anchor))
        return f'<h{level} id="{anchor}">{num}. {text}</h{level}>'

    # Only process h1 and h2 for TOC, but add IDs to all
    processed = re.sub(r'<h([12])>(.*?)</h\1>', replace_heading, html)
    return headings, processed


def md_to_html(md_text: str) -> str:
    """Convierte Markdown a HTML."""
    import markdown
    extensions = ['tables', 'fenced_code', 'toc', 'smarty']
    html = markdown.markdown(md_text, extensions=extensions)
    return html


def build_full_html(md_path: Path, css_path: Path) -> str:
    """Construye el HTML completo con portada, ToC, y contenido."""
    md_text = md_path.read_text(encoding='utf-8')

    # Remove the original H1 title and metadata block (we have the cover for that)
    md_text = re.sub(r'^# Plan de Seguridad Informática Integral.*?---', '', md_text,
                     count=1, flags=re.DOTALL)

    # Convert MD → HTML
    content_html = md_to_html(md_text)

    # Post-processing
    content_html = replace_priority_emojis(content_html)
    content_html = replace_check_marks(content_html)
    content_html = wrap_fuentes_sections(content_html)

    # Add section breaks before h1
    content_html = content_html.replace('<h1>', '<div class="page-break"></div>\n<h1>')

    # Extract headings and add IDs
    headings, content_html = extract_headings(content_html)

    # Build ToC
    toc_html = build_toc(headings)

    # Read CSS
    css_text = css_path.read_text(encoding='utf-8')

    # Assemble
    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<style>
{css_text}
</style>
</head>
<body>
{build_cover_html()}
{build_control_table_html()}
{toc_html}
{content_html}
</body>
</html>"""

    return full_html


def main():
    parser = argparse.ArgumentParser(description='Genera PDF del Plan de Seguridad')
    parser.add_argument('--output', '-o', default='Plan_Seguridad_Empresa.pdf',
                        help='Nombre del archivo PDF de salida')
    parser.add_argument('--html-only', action='store_true',
                        help='Solo generar HTML (debug)')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    md_path = script_dir / 'Plan_Seguridad_Empresa.md'
    css_path = script_dir / 'templates' / 'template.css'
    output_path = script_dir / args.output

    if not md_path.exists():
        print(f"[ERROR] No se encontró: {md_path}")
        sys.exit(1)
    if not css_path.exists():
        print(f"[ERROR] No se encontró: {css_path}")
        sys.exit(1)

    print("  Construyendo HTML...")
    full_html = build_full_html(md_path, css_path)

    if args.html_only:
        html_out = script_dir / 'Plan_Seguridad_Empresa.html'
        html_out.write_text(full_html, encoding='utf-8')
        print(f"  ✓ HTML generado → {html_out}")
        return

    print("  Generando PDF con WeasyPrint...")
    try:
        from weasyprint import HTML
    except ImportError:
        print("[ERROR] weasyprint no instalado: pip install weasyprint")
        sys.exit(1)

    HTML(string=full_html, base_url=str(script_dir)).write_pdf(str(output_path))
    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"  ✓ PDF generado → {output_path.name} ({size_mb:.1f} MB)")


if __name__ == '__main__':
    main()
