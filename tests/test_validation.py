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
