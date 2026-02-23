# Resumen Técnico del Proyecto

## ¿Qué es?

**app-rag-seguridad-informatica** es un sistema **RAG (Retrieval-Augmented Generation) 100% local** para la creación automatizada de planes de seguridad informática empresarial. Toma como entrada documentos PDF de referencia (guías CCN-CERT, INCIBE, NIST, CIS Benchmarks) y produce como salida informes profesionales de seguridad con trazabilidad completa a las fuentes.

---

## ¿Qué hace?

1. **Ingesta y procesamiento** de PDFs de seguridad informática (154 documentos)
2. **Indexación semántica** del corpus para búsqueda híbrida vectorial + léxica
3. **Generación de planes de seguridad** fundamentados exclusivamente en el corpus (SSoT)
4. **Producción de entregables PDF y DOCX** corporativos listos para cliente

---

## ¿Cómo lo hace?

### Pipeline de datos (6 etapas)

```
PDF → Extract → Clean → Chunk → Index → Query/Generate
```

| Etapa | Script | Qué hace |
|-------|--------|----------|
| **Ingest** | `app/ingest.py` | Valida PDFs, calcula hashes SHA-256, detecta duplicados, mueve a `01_raw_pdfs/` |
| **Extract** | `app/extract.py` | Extrae texto de PDFs a Markdown con PyMuPDF (preserva estructura de páginas) |
| **Clean** | `app/clean.py` | Elimina ruido de OCR: dot-leaders, guiones rotos inter-línea, espaciado excesivo (8.5% reducción media) |
| **Chunk** | `app/chunk.py` | Fragmenta por secciones Markdown respetando límites semánticos → 15.139 chunks en JSONL |
| **Index** | `app/index.py` | Genera embeddings con `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, crea índice FAISS (15.139 vectores) + BM25 léxico |
| **Query** | `app/rag_engine.py` | Búsqueda híbrida con fusión RRF (Reciprocal Rank Fusion), genera respuestas con LLM local opcional |

### Arquitectura de retrieval

```
                    ┌──────────────┐
     query ────────►│  Embedder    │──── FAISS (vector search)──┐
                    │  MiniLM-L12  │                            │
                    └──────────────┘                            ├─ RRF fusion ─► top-K chunks
                                                                │
     query ────────► BM25 (léxico) ─────────────────────────────┘
```

- **FAISS**: similitud coseno sobre 384-dim embeddings multilingües
- **BM25**: frecuencia de término con `rank-bm25`
- **RRF** (k=60): fusiona ambos rankings en uno solo

### Generación de informes

`app/plan_generator.py` consulta el índice con **~40 queries** agrupadas en **12 dominios de seguridad**, extrae los fragmentos más relevantes con citas, y los compila en un plan estructurado.

### Pipeline de PDF

```
Markdown → Python (markdown lib) → HTML + CSS (@page) → WeasyPrint → PDF
```

- CSS con `@page` para portada, cabeceras/pies, numeración, márgenes
- Priority badges (CRÍTICA/ALTA/MEDIA/NORMAL) como `<span>` con colores
- ToC generado programáticamente desde headings H1/H2

### Stack tecnológico

| Componente | Tecnología |
|------------|-----------|
| Extracción PDF | PyMuPDF (fitz) |
| Embeddings | sentence-transformers (MiniLM-L12-v2) |
| Índice vectorial | FAISS (faiss-cpu) |
| Índice léxico | rank-bm25 |
| LLM local (opcional) | llama-cpp-python |
| Generación PDF | WeasyPrint + CSS paginado |
| Configs | YAML (configs/) |
| CLI | argparse (app/cli.py) |
| Orquestación | Makefile (22 targets) |

### Estructura del repo

```
app-rag-seguridad-informatica/
├── app/                          # 14 scripts Python
├── configs/                      # 3 YAMLs (pipeline, chunking, retrieval)
├── data/
│   ├── 01_raw_pdfs/              # 154 PDFs consolidados
│   ├── 02_extracted_md/          # Markdown crudo
│   ├── 03_clean_md/              # Markdown limpio
│   └── 04_chunks/                # chunks.jsonl (15.139 fragmentos)
├── indexes/                      # FAISS (~22 MB) + BM25
├── deliverables/
│   ├── plan_seguridad_empresa_cliente/   # PDF vendible (sin citas)
│   └── plan_seguridad_empresa_interno/   # PDF con trazabilidad
├── reports/                      # Plan original + evidencia JSON
├── prompts/                      # Templates para modos RAG
└── Makefile                      # 22 targets reproducibles
```

### Métricas del corpus actual

| Métrica | Valor |
|---------|-------|
| Documentos | 154 PDFs |
| Chunks indexados | 15.139 |
| Índice vectorial | ~22 MB (384-dim) |
| Reducción por limpieza | 8.5% media |
