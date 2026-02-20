#!/usr/bin/env python3
"""
app/evals.py — Suite de evaluación con golden set

Evalúa la calidad del RAG con preguntas predefinidas.
Genera reports/evals_report.md.

Uso:
    python -m app.evals
    make evals
"""

import json
import sys
import time
from pathlib import Path
from app.utils import load_config, require_pdfs, ensure_dir, print_header, PROJECT_ROOT

GOLDEN_SET = [
    {"id": "eval_001", "query": "¿Qué es la autenticación multifactor (MFA)?",
     "expected_keywords": ["multifactor", "MFA", "autenticación"], "domain": "IAM"},
    {"id": "eval_002", "query": "¿Controles de hardening para Linux?",
     "expected_keywords": ["hardening", "linux", "control"], "domain": "Endpoint"},
    {"id": "eval_003", "query": "¿Pasos ante un incidente de seguridad?",
     "expected_keywords": ["incidente", "respuesta", "contención"], "domain": "IR"},
    {"id": "eval_004", "query": "¿Qué es el ENS?",
     "expected_keywords": ["ENS", "esquema", "nacional"], "domain": "Gobernanza"},
    {"id": "eval_005", "query": "¿Plan de continuidad de negocio?",
     "expected_keywords": ["continuidad", "negocio", "plan"], "domain": "BCP/DR"},
]


def evaluate_retrieval(engine, query, expected_kw):
    results = engine.hybrid_search(query)
    all_content = " ".join(r.get("content", "").lower() for r in results)
    hits = sum(1 for kw in expected_kw if kw.lower() in all_content)
    coverage = hits / max(len(expected_kw), 1)
    return {
        "has_results": len(results) > 0, "num_results": len(results),
        "keyword_coverage": round(coverage, 3), "keyword_hits": hits,
        "top_score": results[0]["score"] if results else 0.0,
    }


def main():
    print_header("EVALUACIÓN DEL RAG (EVALS)")
    require_pdfs("evaluación")

    from app.rag_engine import RAGEngine
    engine = RAGEngine()
    engine.load_indexes()
    engine.load_embedder()

    results = []
    t0 = time.time()
    for q in GOLDEN_SET:
        print(f"  🔍 [{q['id']}] {q['query'][:50]}...")
        r = evaluate_retrieval(engine, q["query"], q["expected_keywords"])
        r.update({"id": q["id"], "domain": q["domain"]})
        results.append(r)
        s = "✓" if r["keyword_coverage"] > 0.5 else "⚠"
        print(f"    {s} cobertura: {r['keyword_coverage']:.0%}")

    total_time = time.time() - t0
    avg_cov = sum(r["keyword_coverage"] for r in results) / max(len(results), 1)
    pass_rate = sum(1 for r in results if r["keyword_coverage"] > 0.5) / max(len(results), 1)

    # Write report
    reports_dir = ensure_dir(PROJECT_ROOT / "reports")
    lines = [
        "# Reporte de Evaluación\n\n",
        f"- Preguntas: **{len(results)}**\n",
        f"- Cobertura media: **{avg_cov:.0%}**\n",
        f"- Tasa aprobación: **{pass_rate:.0%}**\n",
        f"- Tiempo: **{total_time:.1f}s**\n\n",
        "| ID | Dominio | Cobertura | Resultados | Estado |\n",
        "|-----|---------|-----------|------------|--------|\n",
    ]
    for r in results:
        st = "✅" if r["keyword_coverage"] > 0.5 else "⚠️"
        lines.append(f"| {r['id']} | {r['domain']} | {r['keyword_coverage']:.0%} | {r['num_results']} | {st} |\n")

    with open(reports_dir / "evals_report.md", "w", encoding="utf-8") as f:
        f.writelines(lines)
    with open(reports_dir / "evals_report.json", "w", encoding="utf-8") as f:
        json.dump({"results": results, "avg_coverage": avg_cov, "pass_rate": pass_rate}, f, indent=2, ensure_ascii=False)

    print(f"\n  📊 Cobertura: {avg_cov:.0%} | Aprobación: {pass_rate:.0%}")


if __name__ == "__main__":
    main()
