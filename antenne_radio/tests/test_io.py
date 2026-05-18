import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.core.io import append_log, read_json, write_json  # noqa: E402


def test_json_file_is_written_and_read(tmp_path):
    path = tmp_path / "nested" / "db.json"
    payload = {"title": "Radio libre", "score": 6, "tags": ["radio", "archive"]}

    write_json(path, payload)

    assert path.exists()
    assert read_json(path, default={}) == payload


def test_write_json_preserves_japanese_characters(tmp_path):
    path = tmp_path / "exports" / "item.json"
    payload = {"title": "ラジオ研究", "language": "ja"}

    write_json(path, payload)

    content = path.read_text(encoding="utf-8")
    assert "ラジオ研究" in content
    assert "\\u30e9" not in content


def test_read_json_returns_default_for_missing_file(tmp_path):
    assert read_json(tmp_path / "missing.json", default=[]) == []


def test_append_log_creates_log_file(tmp_path):
    path = tmp_path / "logs" / "run.log"

    append_log(path, "configuration loaded", level="debug")

    content = path.read_text(encoding="utf-8")
    assert "[DEBUG] configuration loaded" in content
