from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]


def load(p): return yaml.safe_load((ROOT/p).read_text())


def test_message_two_local_operation_contract():
    c=load("state/canonical/contracts.yaml")
    read=next(x for x in c["operations"] if x["id"]=="OP_READ")
    update=next(x for x in c["operations"] if x["id"]=="OP_UPDATE")
    assert "MSG2 operation = READ" in read["inputs"]
    assert "MSG2 operation = UPDATE" in update["inputs"]
    assert any("confirmed associative matches" in x for x in update["effects"])
    assert any("Propagate exclusively through persistent LTM1" in x for x in read["stages"])
    assert any("Propagate exclusively through persistent LTM1" in x for x in update["stages"])
    assert "Serialized Memory Message" in read["outputs"]


def test_transformer_defined_language_and_conservative_ltm1():
    s=load("state/content/11_15.yaml")
    text=" ".join(str(x) for x in s["blocks"])
    assert "Transformer-defined vocabulary" in text
    assert "does not invent a separate native" in text
    assert "serializes it in the internal language" in text
    assert "Sleep-only structural change" in text
    d=load("state/master-architecture-diagram.yaml")["diagram"]
    msg=next(n for n in d["nodes"] if n["id"]=="MSG2")
    assert "operation" in msg["label"]


def test_no_global_stm_operation_mode():
    files=[ROOT/"state/canonical/contracts.yaml",ROOT/"state/content/11_11.yaml",ROOT/"state/content/03_01_architecture_overview.yaml"]
    text=" ".join(p.read_text() for p in files)
    assert "Set operation mode to READ" not in text
    assert "Transformer UPDATE mode" not in text
