# ============================================================
# Makefile — RAG Seguridad Informática
# ============================================================
# Pipeline reproducible: make pipeline
# Ayuda: make help
# ============================================================

PYTHON := python3
APP := $(PYTHON) -m app

.PHONY: help bootstrap ingest extract clean chunk index pipeline \
        backup backup-list restore reports evals manifest \
        status serve lint plan-pdf plan-docx plan-cliente plan-interno

# ── Ayuda ───────────────────────────────────────────────────
help: ## Mostrar esta ayuda
	@echo ""
	@echo "  RAG Seguridad Informática — Comandos disponibles"
	@echo "  ================================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── Setup ───────────────────────────────────────────────────
bootstrap: ## Crear entorno virtual e instalar dependencias
	$(PYTHON) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "  ✓ Entorno creado. Active con: source .venv/bin/activate"
	@echo "  ⏳ Coloque PDFs en data/incoming_pdfs/ y ejecute: make pipeline"

# ── Pipeline individual ────────────────────────────────────
status: ## Estado del sistema
	$(APP).cli status

ingest: ## Ingestar PDFs nuevos desde incoming_pdfs/
	$(APP).cli ingest

extract: ## Extraer PDF → Markdown
	$(APP).cli extract

clean: ## Limpiar Markdown (anti-ruido)
	$(APP).cli clean

chunk: ## Chunkear Markdown → JSONL
	$(APP).cli chunk

index: ## Indexar (FAISS + BM25)
	$(APP).cli index

# ── Pipeline completo ──────────────────────────────────────
pipeline: ## Pipeline completo (backup→ingest→extract→clean→chunk→index→reports→manifest)
	$(APP).cli pipeline

# ── Consultas ──────────────────────────────────────────────
query: ## Consulta RAG (uso: make query Q="mi pregunta")
	$(APP).cli query "$(Q)"

query-audit: ## Consulta modo auditoría
	$(APP).cli query "$(Q)" --mode audit

query-design: ## Consulta modo diseño
	$(APP).cli query "$(Q)" --mode design

# ── Backups ────────────────────────────────────────────────
backup: ## Backup completo (uso: make backup STAGE=full)
	$(APP).cli backup --stage $(or $(STAGE),full)

backup-list: ## Listar backups disponibles
	$(APP).cli backup-list

restore: ## Restaurar backup (uso: make restore ID=xxx --force)
	$(APP).cli restore --id $(ID) $(if $(FORCE),--force)

# ── Reportes y evaluación ──────────────────────────────────
reports: ## Generar reportes (inventario, chunking, index)
	$(APP).cli reports

evals: ## Evaluación con golden set
	$(APP).cli evals

manifest: ## Generar manifiesto de iteración
	$(APP).cli manifest

# ── Entregables ────────────────────────────────────────────
plan-pdf: ## Generar Plan de Seguridad en PDF
	.venv/bin/python deliverables/plan_seguridad_empresa/build_pdf.py

plan-docx: ## Generar Plan de Seguridad en DOCX (requiere pandoc)
	@which pandoc > /dev/null 2>&1 || (echo "  [ERROR] pandoc no instalado"; exit 1)
	pandoc deliverables/plan_seguridad_empresa/Plan_Seguridad_Empresa.md \
		-o deliverables/plan_seguridad_empresa/Plan_Seguridad_Empresa.docx \
		--toc --number-sections
	@echo "  ✓ DOCX generado"

plan-cliente: ## Generar Plan de Seguridad PDF (versión cliente, sin citas)
	.venv/bin/python deliverables/plan_seguridad_empresa_cliente/build_pdf.py

plan-interno: ## Generar Plan de Seguridad PDF (versión interna, con trazabilidad)
	.venv/bin/python deliverables/plan_seguridad_empresa_interno/build_pdf.py

# ── Desarrollo ─────────────────────────────────────────────
lint: ## Verificar sintaxis Python
	$(PYTHON) -m py_compile app/utils.py
	$(PYTHON) -m py_compile app/ingest.py
	$(PYTHON) -m py_compile app/extract.py
	$(PYTHON) -m py_compile app/clean.py
	$(PYTHON) -m py_compile app/chunk.py
	$(PYTHON) -m py_compile app/index.py
	$(PYTHON) -m py_compile app/rag_engine.py
	$(PYTHON) -m py_compile app/backup.py
	$(PYTHON) -m py_compile app/manifest.py
	$(PYTHON) -m py_compile app/reports.py
	$(PYTHON) -m py_compile app/evals.py
	$(PYTHON) -m py_compile app/cli.py
	@echo "  ✓ Todos los archivos compilan correctamente"
