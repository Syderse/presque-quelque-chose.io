from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core import normalize, scoring  # noqa: E402
from scripts.core.io import append_log, utc_now_iso  # noqa: E402
from scripts.export import export_obsidian  # noqa: E402
from scripts.ingest import ingest_crossref, ingest_hal, ingest_rss  # noqa: E402


DEFAULT_SOURCES = ROOT / "config" / "sources.yaml"
DEFAULT_KEYWORDS = ROOT / "config" / "keywords.yaml"
DEFAULT_SCORING = ROOT / "config" / "scoring.yaml"
DEFAULT_RSS_RAW = ROOT / "data" / "raw" / "rss_latest.json"
DEFAULT_HAL_RAW = ROOT / "data" / "raw" / "hal_latest.json"
DEFAULT_CROSSREF_RAW = ROOT / "data" / "raw" / "crossref_latest.json"
DEFAULT_DB = ROOT / "data" / "normalized" / "db.json"
DEFAULT_EXPORT_DIR = ROOT / "data" / "exports"
DEFAULT_API_LOG = ROOT / "data" / "logs" / "api.log"
DEFAULT_PIPELINE_LOG = ROOT / "data" / "logs" / "pipeline.log"

StepCallable = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class PipelinePaths:
    sources_path: Path = DEFAULT_SOURCES
    keywords_path: Path = DEFAULT_KEYWORDS
    scoring_path: Path = DEFAULT_SCORING
    rss_raw_path: Path = DEFAULT_RSS_RAW
    hal_raw_path: Path = DEFAULT_HAL_RAW
    crossref_raw_path: Path = DEFAULT_CROSSREF_RAW
    db_path: Path = DEFAULT_DB
    export_dir: Path = DEFAULT_EXPORT_DIR
    api_log_path: Path = DEFAULT_API_LOG
    pipeline_log_path: Path = DEFAULT_PIPELINE_LOG


@dataclass(frozen=True)
class PipelineFunctions:
    ingest_rss: StepCallable = ingest_rss.ingest_rss
    ingest_hal: StepCallable = ingest_hal.ingest_hal
    ingest_crossref: StepCallable = ingest_crossref.ingest_crossref
    normalize: StepCallable = normalize.normalize_latest_dumps
    scoring: StepCallable = scoring.score_db
    export_obsidian: StepCallable = export_obsidian.export_weekly_report


def _coerce_paths(paths: PipelinePaths | None = None) -> PipelinePaths:
    if paths is None:
        return PipelinePaths()

    return PipelinePaths(
        sources_path=Path(paths.sources_path),
        keywords_path=Path(paths.keywords_path),
        scoring_path=Path(paths.scoring_path),
        rss_raw_path=Path(paths.rss_raw_path),
        hal_raw_path=Path(paths.hal_raw_path),
        crossref_raw_path=Path(paths.crossref_raw_path),
        db_path=Path(paths.db_path),
        export_dir=Path(paths.export_dir),
        api_log_path=Path(paths.api_log_path),
        pipeline_log_path=Path(paths.pipeline_log_path),
    )


def _short_result(result: dict[str, Any]) -> str:
    interesting_keys = (
        "entry_count",
        "result_count",
        "added_count",
        "saved_count",
        "scored_count",
        "skipped_count",
        "items_to_read",
        "items_candidate",
        "marked_exported",
        "export_path",
    )
    parts = [f"{key}={result[key]}" for key in interesting_keys if key in result]
    return ", ".join(parts) if parts else "done"


def _run_step(name: str, func: Callable[[], dict[str, Any]], *, log_path: Path) -> dict[str, Any]:
    append_log(log_path, f"START {name}")
    try:
        result = func()
    except Exception as exc:  # noqa: BLE001 - pipeline must continue after a step failure.
        append_log(log_path, f"ERROR {name}: {type(exc).__name__}: {exc}", level="ERROR")
        return {
            "name": name,
            "status": "failed",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }

    append_log(log_path, f"OK {name}: {_short_result(result)}")
    return {"name": name, "status": "ok", "result": result}


def _skip_step(name: str, *, log_path: Path) -> dict[str, Any]:
    append_log(log_path, f"SKIP {name}")
    return {"name": name, "status": "skipped"}


def run_pipeline(
    *,
    skip_rss: bool = False,
    skip_hal: bool = False,
    skip_crossref: bool = False,
    skip_export: bool = False,
    mark_exported: bool = False,
    paths: PipelinePaths | None = None,
    functions: PipelineFunctions | None = None,
) -> dict[str, Any]:
    paths = _coerce_paths(paths)
    functions = functions or PipelineFunctions()
    steps: list[dict[str, Any]] = []

    append_log(paths.pipeline_log_path, "PIPELINE START")

    if skip_rss:
        steps.append(_skip_step("ingest_rss", log_path=paths.pipeline_log_path))
    else:
        steps.append(
            _run_step(
                "ingest_rss",
                lambda: functions.ingest_rss(
                    config_path=paths.sources_path,
                    output_path=paths.rss_raw_path,
                    log_path=paths.api_log_path,
                ),
                log_path=paths.pipeline_log_path,
            )
        )

    if skip_hal:
        steps.append(_skip_step("ingest_hal", log_path=paths.pipeline_log_path))
    else:
        steps.append(
            _run_step(
                "ingest_hal",
                lambda: functions.ingest_hal(
                    config_path=paths.sources_path,
                    keywords_path=paths.keywords_path,
                    output_path=paths.hal_raw_path,
                    log_path=paths.api_log_path,
                ),
                log_path=paths.pipeline_log_path,
            )
        )

    if skip_crossref:
        steps.append(_skip_step("ingest_crossref", log_path=paths.pipeline_log_path))
    else:
        steps.append(
            _run_step(
                "ingest_crossref",
                lambda: functions.ingest_crossref(
                    config_path=paths.sources_path,
                    output_path=paths.crossref_raw_path,
                    log_path=paths.api_log_path,
                ),
                log_path=paths.pipeline_log_path,
            )
        )

    steps.append(
        _run_step(
            "normalize",
            lambda: functions.normalize(
                rss_raw_path=paths.rss_raw_path,
                hal_raw_path=paths.hal_raw_path,
                crossref_raw_path=paths.crossref_raw_path,
                db_path=paths.db_path,
                log_path=paths.api_log_path,
            ),
            log_path=paths.pipeline_log_path,
        )
    )
    steps.append(
        _run_step(
            "scoring",
            lambda: functions.scoring(
                db_path=paths.db_path,
                keywords_path=paths.keywords_path,
                scoring_path=paths.scoring_path,
            ),
            log_path=paths.pipeline_log_path,
        )
    )

    if skip_export:
        steps.append(_skip_step("export_obsidian", log_path=paths.pipeline_log_path))
    else:
        steps.append(
            _run_step(
                "export_obsidian",
                lambda: functions.export_obsidian(
                    db_path=paths.db_path,
                    export_dir=paths.export_dir,
                    mark_exported=mark_exported,
                ),
                log_path=paths.pipeline_log_path,
            )
        )

    failed_steps = [step["name"] for step in steps if step["status"] == "failed"]
    status = "failed" if failed_steps else "ok"
    append_log(paths.pipeline_log_path, f"PIPELINE END status={status} failed_steps={','.join(failed_steps) or 'none'}")

    return {
        "generated_at": utc_now_iso(),
        "status": status,
        "failed_steps": failed_steps,
        "steps": steps,
        "pipeline_log_path": str(paths.pipeline_log_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local radio-watch v0.1 pipeline.")
    parser.add_argument("--skip-rss", action="store_true", help="Skip RSS/Atom ingestion and reuse existing raw dump.")
    parser.add_argument("--skip-hal", action="store_true", help="Skip HAL ingestion and reuse existing raw dump.")
    parser.add_argument("--skip-crossref", action="store_true", help="Skip Crossref ingestion and reuse existing raw dump.")
    parser.add_argument("--skip-export", action="store_true", help="Skip Markdown export.")
    parser.add_argument("--mark-exported", action="store_true", help="Mark exported to_read items as exported.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_pipeline(
        skip_rss=args.skip_rss,
        skip_hal=args.skip_hal,
        skip_crossref=args.skip_crossref,
        skip_export=args.skip_export,
        mark_exported=args.mark_exported,
    )
    failed = ", ".join(result["failed_steps"]) or "none"
    print(f"Pipeline {result['status']}; failed_steps={failed}; log={result['pipeline_log_path']}")


if __name__ == "__main__":
    main()
