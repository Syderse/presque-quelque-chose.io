#!/usr/bin/env python3
"""Rapport hebdomadaire : récapitulatif de la base + scan anti-fuite sur l'index public."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DB_PATH = ROOT / "data" / "normalized" / "db.json"
INDEX_PATH = SITE_ROOT / "static" / "antenne-radio" / "index.json"

FORBIDDEN_KEYS = {
    "raw",
    "abstract",
    "logs",
    "notes",
    "status",
    "relevance_score",
    "score_explanation",
    "keywords_matched",
    "negative_keywords_matched",
    "discovered_at",
    "source_feed",
    "source_api",
    "title_original",
    "errors",
    "raw_responses",
    "tags",
}
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
# Correspond uniquement aux chemins locaux (pas aux URLs http/https)
LOCAL_PATH_RE = re.compile(r"(?:/Users/[^/]|/home/[a-z][^/]|/var/folders/|C:\\)")

# Emails intentionnellement publics (bloc « À propos / contact »)
ALLOWED_EMAILS: frozenset[str] = frozenset({"mathieu.allag@gmail.com"})


def _scan_leaks(value: object, path: str = "") -> list[str]:
    issues: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_KEYS:
                issues.append(f"[CLÉ INTERDITE] '{key}' à {path}")
            issues.extend(_scan_leaks(nested, f"{path}.{key}"))
    elif isinstance(value, list):
        for i, nested in enumerate(value):
            issues.extend(_scan_leaks(nested, f"{path}[{i}]"))
    elif isinstance(value, str):
        for match in EMAIL_RE.finditer(value):
            email = match.group()
            if email not in ALLOWED_EMAILS:
                issues.append(f"[FUITE EMAIL] '{email}' à {path}")
        # Ignorer les URLs HTTP(S) pour la détection de chemins locaux
        if not value.startswith(("http://", "https://")) and LOCAL_PATH_RE.search(value):
            issues.append(f"[CHEMIN LOCAL] dans '{value[:80]}' à {path}")
    return issues


def _doi_duplicates(items: list[dict]) -> int:
    dois = [item["doi"] for item in items if item.get("doi")]
    return len(dois) - len(set(dois))


def main(
    db_path: str | Path = DB_PATH,
    index_path: str | Path = INDEX_PATH,
) -> int:
    db_path = Path(db_path)
    index_path = Path(index_path)

    # --- Base locale ---
    try:
        db_raw = json.loads(db_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERREUR] db.json introuvable : {db_path}", file=sys.stderr)
        return 1

    db_items = db_raw.get("items", db_raw) if isinstance(db_raw, dict) else db_raw
    db_items = [i for i in db_items if isinstance(i, dict)]
    status_counts = Counter(i.get("status", "?") for i in db_items)
    total_db = len(db_items)
    doi_dupes = _doi_duplicates(db_items)

    # --- Index public ---
    try:
        index_raw = json.loads(index_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERREUR] index.json introuvable : {index_path}", file=sys.stderr)
        return 1

    public_items = index_raw.get("items", [])
    public_count = len(public_items)
    sources = {item.get("source_name") for item in public_items}
    source_count = len(sources)

    # --- Affichage récapitulatif ---
    print("")
    print("╔══════════════════════════════════════════════════╗")
    print("║  RÉCAPITULATIF — Antenne Radio                   ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Base locale (db.json)    : {total_db:>5} items           ║")
    for status_key in ("to_read", "candidate", "exported", "ignored", "new"):
        count = status_counts.get(status_key, 0)
        print(f"║    {status_key:<16} : {count:>5}                   ║")
    print(f"║  Doublons DOI             : {doi_dupes:>5}                   ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Index public (index.json): {public_count:>5} items publics  ║")
    print(f"║  Sources distinctes       : {source_count:>5}                   ║")
    print("╚══════════════════════════════════════════════════╝")

    if doi_dupes > 0:
        print(f"\n⚠  {doi_dupes} doublon(s) DOI dans db.json — vérifier la déduplication.", file=sys.stderr)

    # --- Scan anti-fuite ---
    print("")
    print("── Scan anti-fuite (index.json) ──")
    issues = _scan_leaks(index_raw, path="index")
    if issues:
        for issue in issues:
            print(f"  {issue}")
        print(f"\n[ÉCHEC] {len(issues)} problème(s) détecté(s). Publication BLOQUÉE.", file=sys.stderr)
        return 2

    print("  OK — 0 clé interdite, 0 fuite e-mail, 0 chemin local.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
