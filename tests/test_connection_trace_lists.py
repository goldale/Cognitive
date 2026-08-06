from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_section_10_14_is_single_canonical_owner():
    chapters = yaml.safe_load((ROOT / "state/chapters.yaml").read_text())
    ch10 = next(c for c in chapters["chapters"] if c["order"] == 11)
    secs = [s for s in ch10["sections"] if s["id"] == "S_11_14"]
    assert len(secs) == 1
    ownership = yaml.safe_load((ROOT / "state/canonical/ownership.yaml").read_text())
    assert {"canonical_location": "Section 10.14", "concept": "Connection Trace Lists"} in ownership["ownership"]

def test_connection_trace_list_contract():
    doc = yaml.safe_load((ROOT / "state/content/11_14.yaml").read_text())
    text = "\n".join(str(b.get("text", "")) for b in doc["blocks"]) + "\n" + "\n".join(str(b.get("items", "")) for b in doc["blocks"])
    assert "Trace List(e) = [trace₁, trace₂, …, traceₙ]" in text
    assert "Trace-list match → transition" in text
    assert "special initial search-signal state" in text
    assert "switch-fabric operation" in text
    assert "Transformer" in text and "forgetting" in text.lower()

def test_release_has_no_duplicate_new_heading():
    changes = (ROOT / "CHANGES.md").read_text()
    assert changes.count("## cognitive-0.3.43 — 2026-08-05") == 1

def test_research_record_points_to_canonical_owner():
    rs = (ROOT / "state/content/24_13.yaml").read_text()
    assert "Canonical owner: Section 10.14" in rs
