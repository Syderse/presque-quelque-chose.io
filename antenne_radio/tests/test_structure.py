from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_expected_v01_tree_exists():
    expected_dirs = [
        "config",
        "scripts/core",
        "scripts/ingest",
        "scripts/export",
        "data/raw",
        "data/normalized",
        "data/exports",
        "data/logs",
        "tests",
    ]

    missing = [path for path in expected_dirs if not (ROOT / path).is_dir()]

    assert missing == []
