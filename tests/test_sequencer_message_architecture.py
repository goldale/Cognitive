from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def text(path):
    return path.read_text(encoding="utf-8")

def test_draft05_latent_architecture():
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "state").rglob("*.yaml"))
    forbidden = "Information " + "Sequencer"
    assert forbidden not in corpus
    assert "LTM1 Associative Vector Codebook" in corpus
    assert "Internal Latent Interface" in corpus
    assert "dual-width" in corpus
    assert "D-Context" in corpus

def test_release_version():
    assert 'version = "0.5.1"' in text(ROOT / "pyproject.toml")
    assert '"release": "Cognitive_0.5.09"' in text(ROOT / "RELEASE_MANIFEST.json")
