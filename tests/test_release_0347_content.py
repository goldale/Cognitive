from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def text(path):
    return path.read_text(encoding="utf-8")

def test_release_0347_architecture():
    s13 = text(ROOT / "state/content/10_13.yaml")
    s14 = text(ROOT / "state/content/10_14.yaml")
    s12 = text(ROOT / "state/content/10_12.yaml")
    assert "Sequencer" in s13
    assert "A completed Sequence determines" in s13
    assert "Single physical LTM" in s14
    assert "MSG1 — Element-semantic message" in s14
    assert "MSG2 — STM-emitted operation message" in s14
    assert "orthogonal message-specific state subspaces" in s14.lower()
    assert "may propagate concurrently" in s14
    assert "cross-stream causal" in s12.lower()

def test_release_version():
    assert 'version = "0.3.50"' in text(ROOT / "pyproject.toml")
    assert "cognitive-0.3.46" in text(ROOT / "CHANGES.md")
