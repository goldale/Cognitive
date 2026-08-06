from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "state" / "content"


def load(name):
    return yaml.safe_load((CONTENT / name).read_text())


def texts(name):
    return "\n".join(str(b.get("text", "")) for b in load(name).get("blocks", []))


def test_shared_language_communication_contract():
    assert "same internal language" in texts("03_03.yaml")
    assert "never enter LTM1 or LTM2" in texts("03_03.yaml")
    assert "reconstruction of a compatible cognitive state" in texts("03_03.yaml")
    assert "Memory does not generate an aggregated Memory Vector" in texts("03_04.yaml")
    assert "first exchange" in texts("03_05.yaml")


def test_time_critical_and_chess_examples():
    assert "carrier of the cognitive system may cease to exist" in texts("06_05.yaml")
    assert "chess move" in texts("08_01.yaml")


def test_memory_architecture_shared_language_cycle():
    data = load("09_01.yaml")
    diagram = next(b for b in data["blocks"] if b.get("type") == "diagram")
    edges = {(e["from"], e["to"]): e for e in diagram["edges"]}
    assert ("serialization", "transformer") in edges
    assert edges[("serialization", "transformer")]["label"] == "shared internal language"
    assert ("transformer", "update") in edges
    assert ("update", "dialogue") in edges
    assert "same Transformer-derived internal language" in texts("09_01.yaml")


def test_no_exact_duplicate_long_content_blocks():
    seen = {}
    duplicates = []
    for path in sorted(CONTENT.glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        for index, block in enumerate(data.get("blocks", [])):
            text = block.get("text")
            if not isinstance(text, str) or len(text) <= 80:
                continue
            normalized = re.sub(r"\s+", " ", text.strip().lower())
            if normalized in seen:
                duplicates.append((seen[normalized], (path.name, index)))
            else:
                seen[normalized] = (path.name, index)
    assert duplicates == []
