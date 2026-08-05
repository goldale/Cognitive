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
    assert any("Sequencer is not invoked" in x for x in update["stages"])

def test_native_language_section_and_diagram():
    s=load("state/content/10_15.yaml")
    text=" ".join(str(x) for x in s["blocks"])
    assert "native communication language" in text.lower()
    assert "repeated Memory Vector" in text
    assert "not a requirement to serialize the complete state of LTM1" in text
    d=load("state/master-architecture-diagram.yaml")["diagram"]
    assert d["version"]=="0.3.50"
    msg=next(n for n in d["nodes"] if n["id"]=="MSG2")
    assert "operation" in msg["label"]

def test_no_global_stm_operation_mode():
    files=[ROOT/"state/canonical/contracts.yaml",ROOT/"state/content/10_11.yaml",ROOT/"state/content/02_01_architecture_overview.yaml"]
    text=" ".join(p.read_text() for p in files)
    assert "Set operation mode to READ" not in text
    assert "Transformer UPDATE mode" not in text
