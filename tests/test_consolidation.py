from __future__ import annotations

from pathlib import Path
import shutil

from cogsys.consolidation import apply_proposal
from cogsys.state import ResearchState

ROOT = Path(__file__).resolve().parents[1]


def test_apply_proposal_updates_state_and_consolidation(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    shutil.copytree(ROOT / "state", state_root)
    changed = apply_proposal(state_root, ROOT / "examples" / "change-proposal.yaml")
    state = ResearchState.load(state_root)
    hypothesis = next(value for value in state.documents["hypotheses"]["hypotheses"] if value["id"] == "H_015")
    assert hypothesis["confidence"] == 0.62
    assert "hypotheses" in changed
    assert state.documents["consolidation"]["latest"]["id"] == "CP_001"
