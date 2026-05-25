from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from dateutil.relativedelta import relativedelta


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, utc_now_iso  # noqa: E402
from scripts.core.models import RadioWatchItem, WatchStatus  # noqa: E402

DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_LOG = ROOT / "data" / "logs" / "pipeline.log"
RETENTION_MONTHS = 18


def _item_date(item: RadioWatchItem) -> datetime:
    date_value = item.published_at or item.discovered_at
    if date_value.tzinfo is None:
        return date_value.replace(tzinfo=timezone.utc)
    return date_value.astimezone(timezone.utc)


def prune_old_items(
    items: list[RadioWatchItem],
    *,
    retention_months: int = RETENTION_MONTHS,
    now: datetime | None = None,
) -> tuple[list[RadioWatchItem], int]:
    """Remove items older than retention_months, except status=exported.

    Returns (kept_items, pruned_count).
    """
    effective_now = now or datetime.now(timezone.utc)
    if effective_now.tzinfo is None:
        effective_now = effective_now.replace(tzinfo=timezone.utc)
    cutoff = effective_now - relativedelta(months=retention_months)

    kept: list[RadioWatchItem] = []
    pruned = 0
    for item in items:
        if item.status == WatchStatus.exported:
            kept.append(item)
            continue
        if _item_date(item) >= cutoff:
            kept.append(item)
        else:
            pruned += 1

    return kept, pruned


def prune_db(
    *,
    db_path: str | Path = DEFAULT_DB,
    log_path: str | Path = DEFAULT_LOG,
    retention_months: int = RETENTION_MONTHS,
    now: datetime | None = None,
) -> dict:
    from scripts.core.normalize import load_existing_db, save_db

    items = load_existing_db(db_path, log_path=log_path)
    kept, pruned_count = prune_old_items(items, retention_months=retention_months, now=now)

    if pruned_count > 0:
        save_db(db_path, kept)
        append_log(
            log_path,
            f"PRUNE removed {pruned_count} item(s) older than {retention_months} months (exported preserved)",
        )

    return {
        "generated_at": utc_now_iso(),
        "total_before": len(items),
        "kept_count": len(kept),
        "pruned_count": pruned_count,
        "retention_months": retention_months,
        "db_path": str(db_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prune db.json items older than the retention window.")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to db.json.")
    parser.add_argument("--months", type=int, default=RETENTION_MONTHS, help="Retention window in months.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = prune_db(db_path=args.db, retention_months=args.months)
    print(
        f"Prune: {result['total_before']} → {result['kept_count']} items "
        f"({result['pruned_count']} supprimés, rétention {result['retention_months']} mois)"
    )


if __name__ == "__main__":
    main()
