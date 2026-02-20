#!/usr/bin/env python3
"""
build_pdf.py — Genera Plan_Seguridad_Empresa_INTERNO.pdf
Incluye el plan completo + anexo de trazabilidad/evidencia.
Usa WeasyPrint (Python + CSS paginado).

Uso:
    python build_pdf.py
    python build_pdf.py --output otro_nombre.pdf
    python build_pdf.py --html-only
"""

import argparse
import re
import sys
from pathlib import Path

# ────────────────────────────────────────────────────────────
# Configuration — placeholders for client branding
# ────────────────────────────────────────────────────────────
CLIENT_NAME = "________________"
VERSION = "v0.1"
AUTHOR = "________________"
DATE = "Febrero 2026"
CLASSIFICATION = "Confidencial"


def build_cover_html() -> str:
    return f"""
<div class="cover-page">
  <div class="cover-accent-top"></div>
  <div class="cover-body">
    <div class="cover-logo-area">
      <div class="cover-logo-box">Logo</div>
    </div>
    <div class="cover-title-block">
      <h1 class="cover-title">Plan de Seguridad<br>Informática Integral</h1>
      <p class="cover-subtitle">
        Diseño, implementación y auditoría del sistema de seguridad de la información
      </p>
    </div>
    <div class="cover-meta">
      <div class="cover-meta-row">
        <div class="cover-meta-item">
          <div class="cover-meta-label">Cliente</div>
          <div class="cover-meta-value">{CLIENT_NAME}</div>
        </div>
        <div class="cover-meta-item">
          <div class="cover-meta-label">Versión</div>
          <div class="cover-meta-value">{VERSION}</div>
        </div>
      </div>
      <div class="cover-meta-row">
        <div class="cover-meta-item">
          <div class="cover-meta-label">Fecha</div>
          <div class="cover-meta-value">{DATE}</div>
        </div>
        <div class="cover-meta-item">
          <div class="cover-meta-label">Clasificación</div>
          <div class="cover-meta-value">{CLASSIFICATION}</div>
        </div>
      </div>
      <div class="cover-meta-row">
        <div class="cover-meta-item">
          <div class="cover-meta-label">Autor</div>
          <div class="cover-meta-value">{AUTHOR}</div>
        </div>
        <div class="cover-meta-item">
          <div class="cover-meta-label">Referencia</div>
          <div class="cover-meta-value">PSI-{DATE[:4]}-001</div>
        </div>
      </div>
    </div>
  </div>
  <div class="cover-accent-bottom"></div>
</div>
"""


def build_control_table_html() -> str:
    return f"""
<div class="page-break"></div>
<h1>Control de Cambios</h1>
<table>
<thead>
<tr><th>Versión</th><th>Fecha</th><th>Autor</th><th>Descripción</th></tr>
</thead>
<tbody>
<tr><td>{VERSION}</td><td>{DATE}</td><td>{AUTHOR}</td><td>Versión inicial</td></tr>
</tbody>
</table>

<h1 style="margin-top: 15mm;">Distribución</h1>
<table>
<thead>
<tr><th>Nombre</th><th>Puesto</th><th>Copia</th></tr>
</thead>
<tbody>
<tr><td>{CLIENT_NAME} — Dirección</td><td>Dirección General</td><td>Electrónica</td></tr>
<tr><td>{CLIENT_NAME} — TI</td><td>Responsable de TI</td><td>Electrónica</td></tr>
<tr><td>{AUTHOR}</td><td>Consultor de seguridad</td><td>Electrónica</td></tr>
</tbody>
</table>
"""


def build_toc(headings: list) -> str:
    lines = [
        '<div class="page-break toc-page">',
        '<h1 class="toc-heading">Índice</h1>',
        '<ul class="toc-list">'
    ]
    for level, text, anchor in headings:
        cls = "toc-l1" if level == 1 else "toc-l2"
        lines.append(f'  <li class="{cls}"><a href="#{anchor}">{text}</a></li>')
    lines.append('</ul></div>')
    return '\n'.join(lines)


def extract_and_number_headings(html: str):
    headings = []
    counter = [0, 0]

    def repl(m):
        lvl = int(m.group(1))
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if lvl == 1:
            counter[0] += 1
            counter[1] = 0
            num = str(counter[0])
        else:
            counter[1] += 1
            num = f"{counter[0]}.{counter[1]}"
        anchor = f"sec-{num.replace('.', '-')}"
        headings.append((lvl, f"{num}. {text}", anchor))
        return f'<h{lvl} id="{anchor}">{num}. {text}</h{lvl}>'

    processed = re.sub(r'<h([12])>(.*?)</h\1>', repl, html)
    return headings, processed


def style_priorities(html: str) -> str:
    for old, cls in [
        ('CRÍTICA', 'prio-critica'), ('ALTA', 'prio-alta'),
        ('MEDIA', 'prio-media'), ('NORMAL', 'prio-normal'),
    ]:
        html = html.replace(f'<td>{old}</td>',
                            f'<td><span class="{cls}">{old}</span></td>')
    return html


def md_to_html(md_text: str) -> str:
    import markdown
    return markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'smarty'])


def build_full_html(md_path: Path, css_path: Path) -> str:
    md_text = md_path.read_text(encoding='utf-8')
    # Remove the top H1 (covered by cover page)
    md_text = re.sub(r'^# .+?\n', '', md_text, count=1)

    # Append evidence annex if exists
    annex_path = md_path.parent / 'ANNEX_evidence.md'
    if annex_path.exists():
        annex_text = annex_path.read_text(encoding='utf-8')
        md_text += '\n\n---\n\n' + annex_text

    content = md_to_html(md_text)
    content = style_priorities(content)

    # Page breaks before H1
    content = content.replace('<h1>', '<div class="page-break"></div>\n<h1>')

    headings, content = extract_and_number_headings(content)
    toc = build_toc(headings)

    css = css_path.read_text(encoding='utf-8')
    # Inject client name into CSS for headers/footers
    css = css.replace('__CLIENT__', CLIENT_NAME)
    css = css.replace('__VERSION__', VERSION)
    css = css.replace('__CLASSIFICATION__', CLASSIFICATION)

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8">
<style>{css}</style>
</head>
<body>
{build_cover_html()}
{build_control_table_html()}
{toc}
{content}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='Plan_Seguridad_Empresa_INTERNO.pdf')
    parser.add_argument('--html-only', action='store_true')
    args = parser.parse_args()

    here = Path(__file__).parent
    md = here / 'Plan_Seguridad_Empresa_INTERNO.md'
    css = here / 'template.css'
    out = here / args.output

    if not md.exists():
        print(f"ERROR: {md}"); sys.exit(1)
    if not css.exists():
        print(f"ERROR: {css}"); sys.exit(1)

    print("  Construyendo HTML...")
    html = build_full_html(md, css)

    if args.html_only:
        (here / 'debug.html').write_text(html, encoding='utf-8')
        print("  ✓ HTML → debug.html"); return

    print("  Generando PDF con WeasyPrint...")
    from weasyprint import HTML
    HTML(string=html, base_url=str(here)).write_pdf(str(out))
    mb = out.stat().st_size / 1048576
    print(f"  ✓ PDF generado → {out.name} ({mb:.1f} MB)")


if __name__ == '__main__':
    main()
