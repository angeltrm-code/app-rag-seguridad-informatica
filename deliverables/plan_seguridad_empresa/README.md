# Plan de Seguridad Empresa — Entregable PDF

## Descripción

Genera un PDF corporativo profesional a partir de `Plan_Seguridad_Empresa.md` usando **WeasyPrint** (Python + CSS).

## Herramienta utilizada

**WeasyPrint 68.1** — Seleccionada porque:
- Pandoc/LaTeX/Typst no estaban disponibles en el sistema
- Se instala via pip dentro del venv del proyecto (sin dependencias globales)
- Soporta CSS paginado (@page, headers/footers, page counters)
- Genera PDFs de calidad corporativa con tablas, portadas y tipografía controlada

## Regenerar el PDF

```bash
# Desde la raíz del repo:
make plan-pdf

# O directamente:
.venv/bin/python deliverables/plan_seguridad_empresa/build_pdf.py
```

## Regenerar solo HTML (debug)

```bash
.venv/bin/python deliverables/plan_seguridad_empresa/build_pdf.py --html-only
```

## Personalizar

### Cliente, autor y versión
Editar los placeholders `{CLIENTE}`, `{AUTOR}`, `{VERSIÓN}`, `{CONFIDENCIALIDAD}` en:
1. `Plan_Seguridad_Empresa.md` — contenido
2. `templates/template.css` — cabeceras/pies de página (`@page` rules)

### Logo
Reemplazar `assets/logo_placeholder.txt` con un archivo de imagen (`logo.png` o `logo.svg`) y actualizar la referencia en `build_pdf.py` → `build_cover_html()`.

### Estilos
Editar `templates/template.css`:
- Colores corporativos: buscar `#1e40af` (azul principal) y `#f59e0b` (dorado)
- Tipografía: buscar `font-family`
- Márgenes: ajustar `@page { margin: ... }`

## Estructura de archivos

```
deliverables/plan_seguridad_empresa/
├── Plan_Seguridad_Empresa.pdf    ← PDF final
├── Plan_Seguridad_Empresa.md     ← Markdown master
├── build_pdf.py                  ← Script generador
├── assets/                       ← Logo y recursos
│   └── logo_placeholder.txt
├── templates/                    ← Plantillas CSS
│   └── template.css
└── README.md                     ← Este archivo
```

## Dependencias

```
pip install weasyprint markdown
```

Ambas se instalan dentro del venv del proyecto con `make bootstrap` o manualmente.
