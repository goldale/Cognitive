from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]


def test_read_contract_0401():
    c=yaml.safe_load((ROOT/"state/canonical/contracts.yaml").read_text())
    read=next(x for x in c["operations"] if x["id"]=="OP_READ")
    joined=" ".join(read["stages"])
    assert "MSG2(amplitude, sequence_number, READ)" in joined
    assert "persistent LTM1" in joined
    assert "Dialogue" in joined
    assert "internal language" in joined
    assert read["outputs"] == ["Serialized Memory Message"]
    assert "candidate_readout_operators" not in read
    assert "selection_metric" not in read


def test_master_diagram_0401():
    d=yaml.safe_load((ROOT/"state/master-architecture-diagram.yaml").read_text())["diagram"]
    ids={n["id"] for n in d["nodes"]}
    assert len(ids)==len(d["nodes"])
    assert all(e["from"] in ids and e["to"] in ids for e in d["edges"])
