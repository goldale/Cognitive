from __future__ import annotations

from pathlib import Path

from cogsys.state import ResearchState
from cogsys.validation import StateValidator


ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_state_is_valid() -> None:
    state = ResearchState.load(ROOT / "state")
    report = StateValidator(ROOT / "schemas" / "research-state.schema.json").validate(state)
    assert report.ok, "\n".join(f"{issue.code}: {issue.message}" for issue in report.errors)
    assert report.metrics["token_count"] >= 70
    assert report.metrics["atomic_token_count"] > 0


def test_derived_tokens_reference_atomic_tokens_only() -> None:
    state = ResearchState.load(ROOT / "state")
    token_map = state.token_map()
    for token in state.token_entries():
        if token["atomic"]:
            continue
        expression = token["expression"]
        refs = [expression["operator"], *expression["arguments"]]
        assert all(token_map[reference]["atomic"] for reference in refs)


def test_bootstrap_scripts_do_not_generate_document_versions() -> None:
    forbidden = ("schema_version", "manifest['version']", 'manifest["version"]')
    for relative in (
        "scripts/bootstrap_chapters.py",
        "scripts/bootstrap_state.py",
        "scripts/generate_stage2.py",
    ):
        source = (ROOT / relative).read_text(encoding="utf-8")
        for marker in forbidden:
            assert marker not in source, f"{relative} still generates {marker}"


def test_release_scripts_do_not_hardcode_project_version() -> None:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    script = (ROOT / "scripts" / "build_release.sh").read_text(encoding="utf-8")
    assert "cognitive-0.3.40.tgz" not in makefile
    assert "cognitive-0.3.40.tgz" not in script
    assert "RELEASE_ARCHIVE ?= dist/cognitive.tgz" in makefile
    assert "OUTPUT=${1:-dist/cognitive.tgz}" in script
