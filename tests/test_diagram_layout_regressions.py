from pathlib import Path
import yaml

def diagram(section):
    data=yaml.safe_load(Path(f"state/content/{section}.yaml").read_text())
    return next(block for block in data["blocks"] if block.get("type")=="diagram")

def test_section_11_04_uses_balanced_two_row_layout():
    d=diagram("11_04")
    assert d["direction"] == "TB"
    assert d["size"] == "standard"
    assert d["rank_groups"] == [["samples", "cov", "white"], ["canonical", "sparse", "orth"]]

def test_section_11_06_uses_balanced_two_row_layout():
    d=diagram("11_06")
    assert d["direction"] == "TB"
    assert d["size"] == "standard"
    assert d["rank_groups"] == [["raw", "l2", "stable"], ["canonical", "rotate", "orth"]]

def test_section_07_03_feedback_loop_uses_balanced_two_row_layout():
    d=diagram("07_03")
    assert d["direction"] == "TB"
    assert d["size"] == "standard"
    assert d["rank_groups"] == [["representation", "evaluation", "behavior"], ["memory", "consequence", "world"]]
    assert d["readability_priority"] is True

def test_diagram_dsl_supports_rank_groups():
    source=Path("src/cogsys/docs.py").read_text()
    assert 'block.get("rank_groups", [])' in source
