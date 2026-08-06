from pathlib import Path

import yaml


def test_section_11_01_uses_reference_layout():
    data = yaml.safe_load(Path("state/content/12_01.yaml").read_text())
    diagram = next(block for block in data["blocks"] if block.get("type") == "diagram")
    assert diagram["direction"] == "LR"
    assert diagram["size"] == "standard"
    assert diagram.get("readability_priority") is True
    assert diagram.get("proportionality_priority") is True
