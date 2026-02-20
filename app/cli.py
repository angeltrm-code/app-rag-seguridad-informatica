#!/usr/bin/env python3
"""
app/cli.py — Entry point CLI del sistema RAG

Subcomandos: ingest, extract, clean, chunk, index, pipeline,
             query, status, backup, restore, reports, evals, manifest

Uso:
    python -m app.cli status
    python -m app.cli pipeline
    python -m app.cli query "¿Cómo configurar MFA?"
"""

import argparse
import sys
from app.utils import print_header, check_pdfs_available, require_pdfs


def cmd_status(args):
    from app.rag_engine import main as rag_status
    sys.argv = ["rag_engine", "status"]
    rag_status()


def cmd_ingest(args):
    from app.ingest import main
    main()


def cmd_extract(args):
    from app.extract import main
    main()


def cmd_clean(args):
    from app.clean import main
    main()


def cmd_chunk(args):
    from app.chunk import main
    main()


def cmd_index(args):
    from app.index import main
    main()


def cmd_pipeline(args):
    """Ejecuta el pipeline completo: backup → ingest → extract → clean → chunk → index → reports → manifest."""
    require_pdfs("pipeline completo")
    print_header("PIPELINE COMPLETO")

    from app.backup import create_backup
    print("── Paso 1/8: Backup ──")
    create_backup("full", "pre-pipeline")

    print("\n── Paso 2/8: Ingesta ──")
    from app.ingest import main as ingest_main
    ingest_main()

    print("\n── Paso 3/8: Extracción ──")
    from app.extract import main as extract_main
    extract_main()

    print("\n── Paso 4/8: Limpieza ──")
    from app.clean import main as clean_main
    clean_main()

    print("\n── Paso 5/8: Chunking ──")
    from app.chunk import main as chunk_main
    chunk_main()

    print("\n── Paso 6/8: Indexación ──")
    from app.index import main as index_main
    index_main()

    print("\n── Paso 7/8: Reportes ──")
    from app.reports import main as reports_main
    reports_main()

    print("\n── Paso 8/8: Manifiesto ──")
    from app.manifest import main as manifest_main
    manifest_main()

    print_header("PIPELINE COMPLETADO ✓")


def cmd_query(args):
    if not args.question:
        print("[ERROR] Proporcione una pregunta.")
        sys.exit(1)
    sys.argv = ["rag_engine", "query", args.question, "--mode", args.mode]
    if args.json:
        sys.argv.append("--json")
    from app.rag_engine import main
    main()


def cmd_backup(args):
    from app.backup import main
    sys.argv = ["backup", "create", "--stage", args.stage]
    if args.label:
        sys.argv.extend(["--label", args.label])
    main()


def cmd_backup_list(args):
    from app.backup import main
    sys.argv = ["backup", "list"]
    main()


def cmd_restore(args):
    from app.backup import main
    sys.argv = ["backup", "restore", "--id", args.id]
    if args.force:
        sys.argv.append("--force")
    main()


def cmd_reports(args):
    from app.reports import main
    main()


def cmd_evals(args):
    from app.evals import main
    main()


def cmd_manifest(args):
    from app.manifest import main
    main()


def main():
    parser = argparse.ArgumentParser(
        description="RAG Seguridad Informática — CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo: python -m app.cli status"
    )
    sub = parser.add_subparsers(dest="command", help="Comando")

    sub.add_parser("status", help="Estado del sistema")
    sub.add_parser("ingest", help="Ingestar PDFs nuevos")
    sub.add_parser("extract", help="Extraer PDF → Markdown")
    sub.add_parser("clean", help="Limpiar Markdown")
    sub.add_parser("chunk", help="Chunkear Markdown")
    sub.add_parser("index", help="Indexar (FAISS + BM25)")
    sub.add_parser("pipeline", help="Pipeline completo")

    q_parser = sub.add_parser("query", help="Consulta RAG")
    q_parser.add_argument("question", help="Pregunta")
    q_parser.add_argument("--mode", default="query", choices=["query", "audit", "design"])
    q_parser.add_argument("--json", action="store_true")

    b_parser = sub.add_parser("backup", help="Crear backup")
    b_parser.add_argument("--stage", required=True)
    b_parser.add_argument("--label", default="")

    sub.add_parser("backup-list", help="Listar backups")

    r_parser = sub.add_parser("restore", help="Restaurar backup")
    r_parser.add_argument("--id", required=True)
    r_parser.add_argument("--force", action="store_true")

    sub.add_parser("reports", help="Generar reportes")
    sub.add_parser("evals", help="Evaluación con golden set")
    sub.add_parser("manifest", help="Generar manifiesto")

    args = parser.parse_args()

    commands = {
        "status": cmd_status, "ingest": cmd_ingest, "extract": cmd_extract,
        "clean": cmd_clean, "chunk": cmd_chunk, "index": cmd_index,
        "pipeline": cmd_pipeline, "query": cmd_query, "backup": cmd_backup,
        "backup-list": cmd_backup_list, "restore": cmd_restore,
        "reports": cmd_reports, "evals": cmd_evals, "manifest": cmd_manifest,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        if not check_pdfs_available():
            print("\n" + "=" * 60)
            print("  ⏳ ESPERANDO PDFs EN data/incoming_pdfs/")
            print("=" * 60)


if __name__ == "__main__":
    main()
