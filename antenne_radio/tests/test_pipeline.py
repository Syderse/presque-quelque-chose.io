import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import pipeline  # noqa: E402


def tmp_paths(tmp_path):
    return pipeline.PipelinePaths(
        sources_path=tmp_path / "config" / "sources.yaml",
        keywords_path=tmp_path / "config" / "keywords.yaml",
        scoring_path=tmp_path / "config" / "scoring.yaml",
        rss_raw_path=tmp_path / "data" / "raw" / "rss_latest.json",
        hal_raw_path=tmp_path / "data" / "raw" / "hal_latest.json",
        crossref_raw_path=tmp_path / "data" / "raw" / "crossref_latest.json",
        openalex_raw_path=tmp_path / "data" / "raw" / "openalex_latest.json",
        db_path=tmp_path / "data" / "normalized" / "db.json",
        export_dir=tmp_path / "data" / "exports",
        api_log_path=tmp_path / "data" / "logs" / "api.log",
        pipeline_log_path=tmp_path / "data" / "logs" / "pipeline.log",
    )


def fake_functions(events):
    def step(name):
        def run(**kwargs):
            events.append((name, kwargs))
            return {"step": name}

        return run

    return pipeline.PipelineFunctions(
        ingest_rss=step("ingest_rss"),
        ingest_hal=step("ingest_hal"),
        ingest_crossref=step("ingest_crossref"),
        ingest_openalex=step("ingest_openalex"),
        normalize=step("normalize"),
        prune=step("prune"),
        scoring=step("scoring"),
        export_obsidian=step("export_obsidian"),
    )


def test_pipeline_runs_steps_in_order_and_logs(tmp_path):
    events = []
    result = pipeline.run_pipeline(paths=tmp_paths(tmp_path), functions=fake_functions(events))

    assert result["status"] == "ok"
    assert [name for name, _ in events] == [
        "ingest_rss",
        "ingest_hal",
        "ingest_crossref",
        "ingest_openalex",
        "normalize",
        "prune",
        "scoring",
        "export_obsidian",
    ]
    log = (tmp_path / "data" / "logs" / "pipeline.log").read_text(encoding="utf-8")
    assert "START ingest_rss" in log
    assert "OK export_obsidian" in log
    assert "PIPELINE END status=ok" in log


def test_pipeline_continues_after_failed_step(tmp_path):
    events = []

    def broken_rss(**kwargs):
        events.append(("ingest_rss", kwargs))
        raise RuntimeError("rss down")

    functions = fake_functions(events)
    functions = pipeline.PipelineFunctions(
        ingest_rss=broken_rss,
        ingest_hal=functions.ingest_hal,
        ingest_crossref=functions.ingest_crossref,
        ingest_openalex=functions.ingest_openalex,
        normalize=functions.normalize,
        prune=functions.prune,
        scoring=functions.scoring,
        export_obsidian=functions.export_obsidian,
    )

    result = pipeline.run_pipeline(paths=tmp_paths(tmp_path), functions=functions)

    assert result["status"] == "failed"
    assert result["failed_steps"] == ["ingest_rss"]
    assert [name for name, _ in events] == [
        "ingest_rss",
        "ingest_hal",
        "ingest_crossref",
        "ingest_openalex",
        "normalize",
        "prune",
        "scoring",
        "export_obsidian",
    ]
    log = (tmp_path / "data" / "logs" / "pipeline.log").read_text(encoding="utf-8")
    assert "ERROR ingest_rss: RuntimeError: rss down" in log
    assert "OK export_obsidian" in log


def test_pipeline_skip_flags_skip_ingestions_and_export(tmp_path):
    events = []
    result = pipeline.run_pipeline(
        paths=tmp_paths(tmp_path),
        functions=fake_functions(events),
        skip_rss=True,
        skip_hal=True,
        skip_crossref=True,
        skip_openalex=True,
        skip_export=True,
    )

    assert result["status"] == "ok"
    assert [name for name, _ in events] == ["normalize", "prune", "scoring"]
    assert [step["status"] for step in result["steps"]] == [
        "skipped",
        "skipped",
        "skipped",
        "skipped",
        "ok",
        "ok",
        "ok",
        "skipped",
    ]
    log = (tmp_path / "data" / "logs" / "pipeline.log").read_text(encoding="utf-8")
    assert "SKIP ingest_rss" in log
    assert "SKIP ingest_hal" in log
    assert "SKIP ingest_crossref" in log
    assert "SKIP ingest_openalex" in log
    assert "SKIP export_obsidian" in log


def test_mark_exported_is_passed_to_export_step(tmp_path):
    events = []

    result = pipeline.run_pipeline(
        paths=tmp_paths(tmp_path),
        functions=fake_functions(events),
        mark_exported=True,
    )

    assert result["status"] == "ok"
    export_kwargs = events[-1][1]
    assert export_kwargs["mark_exported"] is True
