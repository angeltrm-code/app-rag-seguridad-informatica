# RAG Seguridad Informática

Sistema **RAG (Retrieval-Augmented Generation) 100% local** para creación y auditoría de sistemas de seguridad informática empresarial.

## 🎯 Objetivo

Asistir en el **diseño**, **generación de entregables** y **auditoría** de sistemas de seguridad, basándose exclusivamente en documentación indexada (PDF → Markdown → Vector Index).

**Regla de oro:** toda recomendación debe estar respaldada por evidencia en el corpus indexado. Si no hay evidencia, el sistema se abstiene.

## 📋 Requisitos

- Python 3.11+
- ~4 GB RAM (embeddings + FAISS)
- ~8 GB RAM (con LLM local via llama.cpp)

## 🚀 Inicio rápido

```bash
# 1. Crear entorno virtual e instalar dependencias
make bootstrap
source .venv/bin/activate

# 2. Descargar modelo LLM (opcional, para generación)
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF \
  mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir models/

# 3. Colocar PDFs en la carpeta de entrada
cp mis_documentos/*.pdf data/incoming_pdfs/

# 4. Ejecutar pipeline completo
make pipeline

# 5. Consultar
make query Q="¿Cómo configurar MFA en Active Directory?"
```

## 📂 Estructura del proyecto

```
├── data/
│   ├── incoming_pdfs/       ← Colocar PDFs aquí
│   ├── 01_raw_pdfs/         PDFs validados
│   ├── 02_extracted_md/     Markdown extraído
│   ├── 03_clean_md/         Markdown limpio
│   └── 04_chunks/           chunks.jsonl + QA
├── indexes/
│   ├── vector/              FAISS
│   ├── bm25/                BM25 (opcional)
│   └── metadata/            Metadatos
├── models/                  Modelos locales (GGUF)
├── configs/                 Configuración YAML
├── prompts/                 Plantillas de prompts
├── app/                     Pipeline y motor RAG
├── reports/                 Inventarios y reportes
├── manifests/               Manifiestos por iteración
├── backups/                 Copias de seguridad
└── tests/                   Tests
```

## 🔧 Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `make status` | Estado del sistema |
| `make pipeline` | Pipeline completo |
| `make ingest` | Ingestar PDFs nuevos |
| `make extract` | PDF → Markdown |
| `make clean` | Limpiar Markdown |
| `make chunk` | Chunking → JSONL |
| `make index` | Indexar (FAISS + BM25) |
| `make query Q="..."` | Consulta RAG |
| `make backup STAGE=full` | Crear backup |
| `make backup-list` | Listar backups |
| `make restore ID=xxx` | Restaurar backup |
| `make reports` | Generar reportes |
| `make evals` | Evaluación con golden set |
| `make manifest` | Generar manifiesto |

## 🔄 Pipeline por iteración

```
incoming_pdfs/ → ingest → extract → clean → chunk → index
                  ↓                                    ↓
               backup                        reports + manifest
```

Cada iteración genera:
- Backup incremental con timestamp
- Manifiesto con hashes de todos los archivos
- Reportes: inventario, chunking, indexación, evals

## 🏗️ Modos de operación

1. **Consulta (Q&A):** pregunta técnica → respuesta con fuentes
2. **Diseño (Blueprint):** contexto empresa → plan de seguridad por fases
3. **Auditoría (Assessment):** cuestionario → evaluación AS-IS + plan TO-BE

## ⚙️ Configuración

- `configs/CONFIG.yml` — Modelos, rutas, parámetros generales
- `configs/chunking.yml` — Tamaños de chunk, overlap, reglas
- `configs/retrieval.yml` — Top-K, umbral, modo híbrido, filtros

## 🔒 Restricciones

- **100% local**: sin APIs externas
- **Grounding estricto**: solo responde con evidencia del corpus
- **Citación obligatoria**: fuente + páginas en toda respuesta
- **Anti-injection**: documentos son datos, no instrucciones
