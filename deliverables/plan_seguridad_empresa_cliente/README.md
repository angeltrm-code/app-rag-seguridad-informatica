# Plan de Seguridad — Entregable Cliente

## Descripción

Informe final corporativo para entrega a cliente. Sin citas granulares, sin fragmentos,
sin referencias por sección. Solo contenido de negocio, limpio y vendible.

## Regenerar el PDF

```bash
# Desde la raíz del repositorio:
make plan-cliente

# O directamente:
.venv/bin/python deliverables/plan_seguridad_empresa_cliente/build_pdf.py
```

## Personalizar

### Datos del cliente

Editar las constantes al inicio de `build_pdf.py`:
```python
CLIENT_NAME = "Nombre del Cliente"
VERSION = "v1.0"
AUTHOR = "Tu nombre"
DATE = "Marzo 2026"
CLASSIFICATION = "Confidencial"
```

Después regenerar con `make plan-cliente`.

### Logo

Sustituir el placeholder en `build_pdf.py` → `build_cover_html()` por una etiqueta `<img>` con el logo del cliente o de la consultora.

### Colores

En `template.css`, buscar y reemplazar:
- `#2563eb` — azul principal
- `#7c3aed` — púrpura de acento
- `#0f172a` — fondo oscuro

## Herramienta

**WeasyPrint** (Python + CSS paginado, instalado en el venv del proyecto).

## Estructura

```
plan_seguridad_empresa_cliente/
├── Plan_Seguridad_Empresa_CLIENTE.pdf   ← PDF final para cliente
├── Plan_Seguridad_Empresa_CLIENTE.md    ← Markdown master
├── build_pdf.py                         ← Script generador
├── template.css                         ← Plantilla CSS
├── assets/                              ← Logo y recursos
│   └── logo_placeholder.txt
└── README.md                            ← Este archivo
```

## Dependencias

```bash
pip install weasyprint markdown
```

(Ya incluidas en el venv del proyecto.)
