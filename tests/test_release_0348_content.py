from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def test_read_contract_0348():
    c=yaml.safe_load((ROOT/"state/canonical/contracts.yaml").read_text())
    read=next(x for x in c["operations"] if x["id"]=="OP_READ")
    joined=" ".join(read["stages"])
    assert "MSG2(amplitude, sequence_number, READ)" in joined
    assert "persistent LTM1 associative graph" in joined
    assert set(read["candidate_readout_operators"])=={"MAX","SUM"}
    assert "entropy" in read["selection_metric"]

def test_master_diagram_0348():
    d=yaml.safe_load((ROOT/"state/master-architecture-diagram.yaml").read_text())["diagram"]
    ids={n["id"] for n in d["nodes"]}
    assert len(ids)==len(d["nodes"])
    assert all(e["from"] in ids and e["to"] in ids for e in d["edges"])
    assert d["visual_generation_policy"]["generated_in_this_release"]==[]
