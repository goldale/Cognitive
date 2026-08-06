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


def test_section_10_1_defines_dialogue_aware_read_update_cycle() -> None:
    import yaml

    content = yaml.safe_load((ROOT / "state" / "content" / "10_01.yaml").read_text(encoding="utf-8"))
    rendered = " ".join(str(block) for block in content["blocks"])
    for phrase in [
        "first exchange",
        "without memory READ",
        "D-Context",
        "Serialized Memory Message",
        "internal language",
        "UPDATE",
    ]:
        assert phrase.lower() in rendered.lower()
    assert "canonical null Serialized Memory Message" not in rendered

def test_progressive_training_and_memory_maturity_use_transformer_internal_language() -> None:
    import yaml

    staged = yaml.safe_load((ROOT / "state" / "content" / "12_06.yaml").read_text(encoding="utf-8"))
    maturity = yaml.safe_load((ROOT / "state" / "content" / "12_07.yaml").read_text(encoding="utf-8"))
    staged_text = " ".join(block.get("text", "") for block in staged["blocks"])
    maturity_text = " ".join(block.get("text", "") for block in maturity["blocks"])
    assert "Transformer is trained first" in staged_text
    assert "internal language" in staged_text
    assert "second language" in staged_text
    assert "Different external formulations with the same meaning" in maturity_text
    assert "Paraphrases + Languages" in " ".join(str(block) for block in maturity["blocks"])
    assert "Semantic discrimination" in " ".join(str(block) for block in maturity["blocks"])
    assert "fixed canonical null Serialized Memory Message" not in staged_text

def test_diagram_readability_is_enforced() -> None:
    import yaml

    for path in sorted((ROOT / "state" / "content").glob("*.yaml")):
        content = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for diagram in (block for block in content.get("blocks", []) if block.get("type") == "diagram"):
            expected = "extra-large" if diagram.get("title") in {"Transformer-Centric Memory Architecture", "The Internal Language at the Center of Cognitive", "Asymmetric Transformer–Memory Interface", "One Possible READ/UPDATE Integration inside a Transformer"} else "standard"
            assert diagram.get("size") == expected
            assert diagram.get("readability_priority") is True
            assert diagram.get("proportionality_priority") is True

    css = (ROOT / "assets" / "cognitive.css").read_text(encoding="utf-8")
    assert ".diagram-size-standard" in css or ".architecture-diagram" in css
    assert "min-height: 12rem" not in css
    assert "max-width: calc(100% * var(--diagram-scale, 1))" in css
    source = (ROOT / "src" / "cogsys" / "docs.py").read_text(encoding="utf-8")
    assert '"standard": 12' in source
    assert "diagram-size-{size}" in source


def test_obsolete_vector_interface_canonicalization_is_removed() -> None:
    import yaml
    chapter_data = yaml.safe_load((ROOT / "state" / "chapters.yaml").read_text(encoding="utf-8"))
    chapter11 = next(ch for ch in chapter_data["chapters"] if ch.get("id") == "C_11")
    assert not any(section.get("id") == "S_11_06" for section in chapter11["sections"])
    combined = " ".join(path.read_text(encoding="utf-8") for path in (ROOT / "state").rglob("*.yaml"))
    for phrase in [
        "Orthogonal Coordinate Transformation",
        "Sparse Basis Rotation",
        "canonical null Serialized Memory Message",
        "Sequential Serialized Memory Message Normalization",
    ]:
        assert phrase.lower() not in combined.lower()

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
        "READ-only Serialized Memory Message generation",
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


def test_all_alphabetical_index_links_target_canonical_index(tmp_path):
    import re
    from pathlib import Path
    from cogsys.state import ResearchState
    from cogsys.docs import DocumentationBuilder

    state = ResearchState.load(Path("state"))
    DocumentationBuilder(state, Path("assets")).build(tmp_path)
    expected = (tmp_path / "chapter26" / "index.html").resolve()
    html_files = sorted(tmp_path.rglob("*.html"))
    assert html_files
    for html_file in html_files:
        source = html_file.read_text(encoding="utf-8")
        hrefs = re.findall(
            r'<a\b(?=[^>]*\bclass=["\'][^"\']*\balphabetical-index\b[^"\']*["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>',
            source,
            re.I,
        )
        assert len(hrefs) >= 2, html_file
        for href in hrefs:
            assert (html_file.parent / href.split("#", 1)[0]).resolve() == expected, (html_file, href)


def test_generated_html_contains_no_document_version_metadata(tmp_path: Path) -> None:
    state = ResearchState.load(ROOT / "state")
    DocumentationBuilder(state, ROOT / "assets").build(tmp_path)
    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert '<p class="subtitle">Version ' not in index
    assert "schema_version" not in index


def test_canonical_yaml_contains_no_version_metadata() -> None:
    import yaml

    forbidden = {"schema_version", "version", "release", "revision", "build_number"}
    for path in sorted((ROOT / "state").rglob("*.yaml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(document, dict):
            assert forbidden.isdisjoint(document), path


def test_logical_episode_and_git_version_policy_are_documented():
    root = Path(__file__).resolve().parents[1]
    canonical = (root / "state/content/10_13.yaml").read_text(encoding="utf-8")
    research = (root / "state/content/23_12.yaml").read_text(encoding="utf-8")
    policy = (root / "state/content/24_04.yaml").read_text(encoding="utf-8")
    assert "Canonical consolidation unit" in canonical
    assert "RS-0010" in research
    assert "Git is the version authority" in policy


def test_changelog_has_no_duplicate_release_heading():
    root = Path(__file__).resolve().parents[1]
    changes = (root / "CHANGES.md").read_text(encoding="utf-8")
    assert changes.count("## cognitive-0.3.40 — 2026-08-05") == 1
