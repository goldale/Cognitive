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
