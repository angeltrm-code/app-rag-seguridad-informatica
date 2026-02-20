#!/usr/bin/env python3
"""
app/backup.py — Sistema de backups incrementales por iteración

Genera copias de seguridad con timestamp, etiqueta de etapa y hash.
Permite restauración a un backup específico.

Uso:
    python -m app.backup create --stage ingest
    python -m app.backup list
    python -m app.backup restore --id 20260220-091000_ingest
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

from app.utils import (
    load_config,
    sha256_file,
    timestamp,
    ensure_dir,
    print_header,
    PROJECT_ROOT,
)


# Directorios a respaldar según la etapa
STAGE_DIRS = {
    "ingest": ["data/01_raw_pdfs"],
    "clean": ["data/02_extracted_md", "data/03_clean_md"],
    "chunking": ["data/04_chunks"],
    "indexing": ["indexes"],
    "prompts": ["prompts"],
    "configs": ["configs"],
    "full": [
        "data/01_raw_pdfs", "data/02_extracted_md", "data/03_clean_md",
        "data/04_chunks", "indexes", "prompts", "configs",
    ],
}


def create_backup(stage: str, label: str = "") -> dict:
    """
    Crea un backup incremental para la etapa indicada.

    Args:
        stage: Etapa del pipeline (ingest, clean, chunking, indexing, etc.)
        label: Etiqueta adicional opcional.

    Returns:
        Diccionario con metadatos del backup.
    """
    config = load_config()
    retention = config.get("backup", {}).get("retention_count", 10)

    if stage not in STAGE_DIRS:
        print(f"[ERROR] Etapa desconocida: {stage}")
        print(f"  Etapas válidas: {', '.join(STAGE_DIRS.keys())}")
        sys.exit(1)

    ts = timestamp()
    backup_name = f"{ts}_{stage}"
    if label:
        backup_name += f"_{label}"

    backup_dir = ensure_dir(PROJECT_ROOT / "backups" / backup_name)

    manifest = {
        "backup_id": backup_name,
        "timestamp": ts,
        "stage": stage,
        "label": label,
        "files": [],
        "total_size_bytes": 0,
    }

    dirs_to_backup = STAGE_DIRS[stage]
    total_files = 0

    for rel_dir in dirs_to_backup:
        source_dir = PROJECT_ROOT / rel_dir
        if not source_dir.exists():
            continue

        dest_dir = backup_dir / rel_dir
        ensure_dir(dest_dir)

        for filepath in sorted(source_dir.rglob("*")):
            if filepath.is_file() and filepath.name != ".gitkeep":
                rel_path = filepath.relative_to(PROJECT_ROOT)
                dest_path = backup_dir / rel_path
                ensure_dir(dest_path.parent)
                shutil.copy2(str(filepath), str(dest_path))

                file_info = {
                    "path": str(rel_path),
                    "size": filepath.stat().st_size,
                    "hash": sha256_file(filepath),
                }
                manifest["files"].append(file_info)
                manifest["total_size_bytes"] += filepath.stat().st_size
                total_files += 1

    # Guardar manifest del backup
    manifest_path = backup_dir / "backup_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Limpiar backups antiguos (retención)
    cleanup_old_backups(retention)

    size_mb = manifest["total_size_bytes"] / 1024 / 1024
    print(f"  ✓ Backup creado: {backup_name}")
    print(f"    Archivos: {total_files}, Tamaño: {size_mb:.2f} MB")

    return manifest


def list_backups() -> list[dict]:
    """Lista todos los backups disponibles."""
    backups_dir = PROJECT_ROOT / "backups"
    if not backups_dir.exists():
        return []

    backups = []
    for d in sorted(backups_dir.iterdir()):
        if d.is_dir() and d.name != ".gitkeep":
            manifest_path = d / "backup_manifest.json"
            if manifest_path.exists():
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                backups.append(manifest)
            else:
                backups.append({
                    "backup_id": d.name,
                    "timestamp": "unknown",
                    "stage": "unknown",
                    "files": [],
                    "total_size_bytes": 0,
                })

    return backups


def restore_backup(backup_id: str, force: bool = False) -> bool:
    """
    Restaura un backup específico.

    Args:
        backup_id: ID del backup (nombre de la carpeta).
        force: Si True, sobrescribe sin preguntar.
    """
    backup_dir = PROJECT_ROOT / "backups" / backup_id
    if not backup_dir.exists():
        print(f"[ERROR] Backup no encontrado: {backup_id}")
        return False

    manifest_path = backup_dir / "backup_manifest.json"
    if not manifest_path.exists():
        print(f"[ERROR] Manifest no encontrado en backup: {backup_id}")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    if not force:
        print(f"  Backup: {backup_id}")
        print(f"  Etapa: {manifest.get('stage', 'unknown')}")
        print(f"  Archivos: {len(manifest.get('files', []))}")
        print(f"  ¿Restaurar? Ejecute con --force para confirmar.")
        return False

    # Restaurar archivos
    restored = 0
    for file_info in manifest.get("files", []):
        src = backup_dir / file_info["path"]
        dest = PROJECT_ROOT / file_info["path"]

        if src.exists():
            ensure_dir(dest.parent)
            shutil.copy2(str(src), str(dest))
            restored += 1

    print(f"  ✓ Restaurados {restored} archivo(s) desde backup '{backup_id}'")
    return True


def cleanup_old_backups(retention: int = 10):
    """Elimina backups antiguos que excedan la retención."""
    backups_dir = PROJECT_ROOT / "backups"
    if not backups_dir.exists():
        return

    backup_dirs = sorted(
        [d for d in backups_dir.iterdir() if d.is_dir() and d.name != ".gitkeep"],
        key=lambda d: d.name,
    )

    if len(backup_dirs) > retention:
        to_remove = backup_dirs[:len(backup_dirs) - retention]
        for d in to_remove:
            shutil.rmtree(d)
            print(f"  🗑 Backup antiguo eliminado: {d.name}")


def main():
    parser = argparse.ArgumentParser(description="Sistema de backups")
    sub = parser.add_subparsers(dest="action")

    create_parser = sub.add_parser("create", help="Crear backup")
    create_parser.add_argument("--stage", required=True,
                               choices=list(STAGE_DIRS.keys()),
                               help="Etapa del pipeline")
    create_parser.add_argument("--label", default="",
                               help="Etiqueta adicional")

    sub.add_parser("list", help="Listar backups")

    restore_parser = sub.add_parser("restore", help="Restaurar backup")
    restore_parser.add_argument("--id", required=True,
                                help="ID del backup")
    restore_parser.add_argument("--force", action="store_true",
                                help="Confirmar restauración")

    args = parser.parse_args()

    if args.action == "create":
        print_header("CREAR BACKUP")
        create_backup(args.stage, args.label)

    elif args.action == "list":
        print_header("BACKUPS DISPONIBLES")
        backups = list_backups()
        if not backups:
            print("  No hay backups.")
        else:
            for b in backups:
                size_mb = b.get("total_size_bytes", 0) / 1024 / 1024
                print(f"  📦 {b['backup_id']} | etapa: {b.get('stage', '?')} | "
                      f"archivos: {len(b.get('files', []))} | {size_mb:.2f} MB")

    elif args.action == "restore":
        print_header("RESTAURAR BACKUP")
        restore_backup(args.id, args.force)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
