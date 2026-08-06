from pathlib import Path
import yaml


def diagrams(section):
    data = yaml.safe_load(Path(f"state/content/{section}.yaml").read_text())
    return [block for block in data["blocks"] if block.get("type") == "diagram"]


def test_asymmetric_transformer_memory_interface_has_two_entry_points():
    d = next(x for x in diagrams("03_02") if x.get("title") == "Asymmetric Transformer–Memory Interface")
    assert d["direction"] == "LR"
    assert d["size"] == "extra-large"
    node_ids = {node["id"] for node in d["nodes"]}
    assert {"early", "read", "stm", "memory", "serialize", "readmsg", "deep", "update"} <= node_ids
    assert any(e["from"] == "read" and e["to"] == "memory" for e in d["edges"])
    assert any(e["from"] == "readmsg" and e["to"] == "deep" for e in d["edges"])
    assert any(e.get("label") == "D-Context defines subset" for e in d["edges"])


def test_section_11_04_models_bounded_serialization():
    d = diagrams("11_04")[0]
    assert d["direction"] == "TB"
    assert d["size"] == "standard"
    labels = {node["label"] for node in d["nodes"]}
    assert "Relevant Candidate Content" in labels
    assert "Serialization Completion" in labels


def test_section_07_03_feedback_loop_uses_balanced_two_row_layout():
    d = diagrams("07_03")[0]
    assert d["direction"] == "TB"
    assert d["size"] == "standard"
    assert d["rank_groups"] == [["representation", "evaluation", "behavior"], ["memory", "consequence", "world"]]
    assert d["readability_priority"] is True


def test_diagram_dsl_supports_rank_groups():
    source = Path("src/cogsys/docs.py").read_text()
    assert 'block.get("rank_groups", [])' in source
