import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.models import RadioWatchItem, SourceType, WatchStatus  # noqa: E402
from scripts.core.prune import RETENTION_MONTHS, prune_old_items, prune_db  # noqa: E402

NOW = datetime(2026, 5, 25, tzinfo=timezone.utc)
RECENT = datetime(2025, 11, 25, tzinfo=timezone.utc)   # 6 months before NOW → within window
OLD = datetime(2024, 10, 1, tzinfo=timezone.utc)       # 19 months before NOW → outside window


def make_item(**overrides) -> RadioWatchItem:
    defaults = {
        "id": "test:001",
        "title": "Test item",
        "source_name": "Radio Survivor",
        "source_type": SourceType.blog,
        "language": "en",
        "status": WatchStatus.candidate,
        "discovered_at": NOW,
        "published_at": RECENT,
    }
    defaults.update(overrides)
    return RadioWatchItem(**defaults)


# --- Core pruning logic ---

def test_recent_item_is_kept():
    item = make_item(published_at=RECENT, status=WatchStatus.candidate)
    kept, pruned = prune_old_items([item], now=NOW)
    assert len(kept) == 1
    assert pruned == 0


def test_old_non_exported_item_is_pruned():
    item = make_item(published_at=OLD, status=WatchStatus.candidate)
    kept, pruned = prune_old_items([item], now=NOW)
    assert len(kept) == 0
    assert pruned == 1


def test_old_exported_item_is_always_kept():
    item = make_item(published_at=OLD, status=WatchStatus.exported)
    kept, pruned = prune_old_items([item], now=NOW)
    assert len(kept) == 1
    assert pruned == 0


def test_mixed_batch():
    items = [
        make_item(id="a", published_at=RECENT, status=WatchStatus.to_read),
        make_item(id="b", published_at=OLD, status=WatchStatus.candidate),
        make_item(id="c", published_at=OLD, status=WatchStatus.exported),
        make_item(id="d", published_at=OLD, status=WatchStatus.ignored),
    ]
    kept, pruned = prune_old_items(items, now=NOW)
    kept_ids = {i.id for i in kept}
    assert kept_ids == {"a", "c"}
    assert pruned == 2


def test_empty_list():
    kept, pruned = prune_old_items([], now=NOW)
    assert kept == []
    assert pruned == 0


def test_uses_discovered_at_when_published_at_is_none():
    item = make_item(published_at=None, discovered_at=OLD, status=WatchStatus.candidate)
    kept, pruned = prune_old_items([item], now=NOW)
    assert len(kept) == 0
    assert pruned == 1


# --- File-level prune_db ---

def _write_db(path: Path, items: list[RadioWatchItem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([json.loads(item.model_dump_json()) for item in items], ensure_ascii=False),
        encoding="utf-8",
    )


def test_prune_db_removes_old_items(tmp_path):
    db_path = tmp_path / "db.json"
    log_path = tmp_path / "pipeline.log"
    items = [
        make_item(id="keep", published_at=RECENT, status=WatchStatus.candidate),
        make_item(id="drop", published_at=OLD, status=WatchStatus.candidate),
        make_item(id="keep_exported", published_at=OLD, status=WatchStatus.exported),
    ]
    _write_db(db_path, items)

    result = prune_db(db_path=db_path, log_path=log_path, now=NOW)

    assert result["pruned_count"] == 1
    assert result["kept_count"] == 2
    assert result["total_before"] == 3

    saved = json.loads(db_path.read_text(encoding="utf-8"))
    saved_items = saved.get("items", saved) if isinstance(saved, dict) else saved
    saved_ids = {i["id"] for i in saved_items}
    assert "drop" not in saved_ids
    assert "keep" in saved_ids
    assert "keep_exported" in saved_ids


def test_prune_db_no_change_when_all_recent(tmp_path):
    db_path = tmp_path / "db.json"
    log_path = tmp_path / "pipeline.log"
    items = [make_item(id="a", published_at=RECENT)]
    original_text = json.dumps([json.loads(items[0].model_dump_json())], ensure_ascii=False)
    _write_db(db_path, items)
    original_mtime = db_path.stat().st_mtime

    result = prune_db(db_path=db_path, log_path=log_path, now=NOW)

    assert result["pruned_count"] == 0
    assert db_path.stat().st_mtime == original_mtime
