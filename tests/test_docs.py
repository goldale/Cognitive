from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

from cogsys.docs import DocumentationBuilder
from cogsys.state import ResearchState


ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value:
                    self.links.append(value)


def test_generated_documentation_has_no_broken_local_links(tmp_path: Path) -> None:
    state = ResearchState.load(ROOT / "state")
    DocumentationBuilder(state, ROOT / "assets").build(tmp_path)
    for html_file in tmp_path.rglob("*.html"):
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (html_file.parent / href.split("#", 1)[0]).resolve()
            assert target.exists(), f"Broken link in {html_file}: {href}"


def test_body_text_has_left_indent() -> None:
    css = (ROOT / "assets" / "cognitive.css").read_text(encoding="utf-8")
    assert "--text-indent" in css
    assert "main {" in css


def test_section_10_1_feedback_does_not_generate_memory_vector() -> None:
    import yaml

    content = yaml.safe_load((ROOT / "state" / "content" / "10_01.yaml").read_text(encoding="utf-8"))
    diagram = next(block for block in content["blocks"] if block.get("type") == "diagram")
    feedback_edges = [edge for edge in diagram["edges"] if edge.get("flow") == "feedback"]
    assert any(edge["from"] == "internal_observation" and edge["to"] == "memory" for edge in feedback_edges)
    assert not any(edge["to"] in {"projection", "vector", "transformer"} for edge in feedback_edges)
    prose = " ".join(block.get("text", "") for block in content["blocks"])
    assert "does not generate a new Memory Vector" in prose
    assert "exclusively by a subsequent explicit READ operation" in prose


def test_progressive_training_and_memory_maturity_are_preserved() -> None:
    import yaml

    staged = yaml.safe_load((ROOT / "state" / "content" / "12_06.yaml").read_text(encoding="utf-8"))
    maturity = yaml.safe_load((ROOT / "state" / "content" / "12_07.yaml").read_text(encoding="utf-8"))
    staged_text = " ".join(block.get("text", "") for block in staged["blocks"])
    maturity_text = " ".join(block.get("text", "") for block in maturity["blocks"])
    assert "fixed canonical null Memory Vector" in staged_text
    assert "force Memory Vector utilization" in staged_text
    assert "differently worded but equal in meaning" in maturity_text
    assert "different languages" in maturity_text
    assert "Semantic invariance must be paired with semantic discrimination" in maturity_text

    state = ResearchState.load(ROOT / "state")
    terms = {entry["token"].removeprefix("T_") for entry in state.token_entries()}
    required = {
        "StagedTraining", "NullMemoryVector", "ForcedMemoryUtilization",
        "AssociativeMemoryMaturity", "SemanticEquivalenceClass",
        "SemanticInvariance", "SemanticDiscrimination", "MultilingualConsistency",
        "IntraClassDistance", "InterClassDistance",
    }
    assert required <= terms

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        DocumentationBuilder(state, ROOT / "assets").build(Path(tmp))
        index_html = (Path(tmp) / "chapter19" / "index.html").read_text(encoding="utf-8")
        for label in [
            "Memory Vector", "Staged Training", "Null Memory Vector",
            "Forced Memory Utilization", "Associative Memory Maturity",
            "Semantic Invariance", "Semantic Discrimination",
            "Multilingual Consistency", "Intra Class Distance", "Inter Class Distance",
        ]:
            assert label in index_html


def test_diagram_readability_is_enforced() -> None:
    import yaml

    for path in sorted((ROOT / "state" / "content").glob("*.yaml")):
        content = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for diagram in (block for block in content.get("blocks", []) if block.get("type") == "diagram"):
            assert diagram.get("size") == "standard"
            assert diagram.get("readability_priority") is True
            assert diagram.get("proportionality_priority") is True

    css = (ROOT / "assets" / "cognitive.css").read_text(encoding="utf-8")
    assert ".diagram-size-standard" in css or ".architecture-diagram" in css
    assert "min-height: 12rem" in css
    source = (ROOT / "src" / "cogsys" / "docs.py").read_text(encoding="utf-8")
    assert '"standard": 12' in source
    assert "diagram-size-{size}" in source


def test_sequential_memory_vector_normalization_is_preserved() -> None:
    import yaml
    chapter_data = yaml.safe_load((ROOT / "state" / "chapters.yaml").read_text(encoding="utf-8"))
    chapter11 = next(ch for ch in chapter_data["chapters"] if ch.get("id") == "C_11")
    assert any(section.get("id") == "S_11_06" for section in chapter11["sections"])
    content = yaml.safe_load((ROOT / "state" / "content" / "11_06.yaml").read_text(encoding="utf-8"))
    rendered = " ".join(str(block) for block in content["blocks"])
    for phrase in [
        "Length Normalization",
        "semantic stabilization",
        "Covariance Analysis",
        "Orthogonal Coordinate Transformation",
        "Sparse Basis Rotation",
        "Semantic preservation invariant",
    ]:
        assert phrase.lower() in rendered.lower()
    token_data = yaml.safe_load((ROOT / "state" / "tokens.yaml").read_text(encoding="utf-8"))
    tokens = token_data["tokens"]
    required = {
        "T_SequentialMemoryVectorNormalization",
        "T_LengthNormalizationStage",
        "T_StatisticalOrthogonalizationStage",
        "T_SparseRotationStage",
    }
    assert required.issubset({token.get("token") for token in tokens})


def test_associative_memory_implementation_gap_analysis_is_preserved() -> None:
    import yaml
    chapter_data = yaml.safe_load((ROOT / "state" / "chapters.yaml").read_text(encoding="utf-8"))
    chapter10 = next(ch for ch in chapter_data["chapters"] if ch.get("id") == "C_10")
    assert any(section.get("id") == "S_10_06" for section in chapter10["sections"])
    content = yaml.safe_load((ROOT / "state" / "content" / "10_06.yaml").read_text(encoding="utf-8"))
    rendered = " ".join(str(block) for block in content["blocks"])
    for phrase in [
        "Hopfield", "Dense Associative Memory", "Sparse Distributed Memory",
        "Vector Search", "Graph", "Key–Value", "Recommended Initial Hybrid",
        "READ-only Memory Vector generation",
    ]:
        assert phrase.lower() in rendered.lower()


def test_every_generated_page_has_unified_alphabetical_index_navigation(tmp_path: Path) -> None:
    state = ResearchState.load(ROOT / "state")
    DocumentationBuilder(state, ROOT / "assets").build(tmp_path)
    for html_file in tmp_path.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        assert text.count("A–Z Index") >= 2, html_file
        assert 'class="page-navigation"' in text


def test_navigation_is_single_line_and_uses_short_index_label(tmp_path: Path) -> None:
    state = ResearchState.load(ROOT / "state")
    DocumentationBuilder(state, ROOT / "assets").build(tmp_path)
    css = (tmp_path / "cognitive.css").read_text(encoding="utf-8")
    assert "white-space: nowrap" in css
    assert "max-content max-content 1fr max-content max-content" in css
    for html_file in tmp_path.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")
        assert "A–Z Alphabetical Index" not in text, html_file
        assert text.count("A–Z Index") >= 2, html_file
