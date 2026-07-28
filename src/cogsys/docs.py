from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .state import ResearchState


TOKEN_RE = re.compile(r"\bT_(?:[A-Z][A-Za-z0-9]*)+\b")
CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
EM_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")


@dataclass(frozen=True)
class PageRef:
    chapter_index: int
    section_index: int
    path: str
    chapter_title: str
    section_title: str


def _render_inline(text: str) -> str:
    escaped = html.escape(text, quote=True)
    protected: list[str] = []

    def protect_code(match: re.Match[str]) -> str:
        value = match.group(1)
        if TOKEN_RE.fullmatch(value):
            rendered = f'<span class="token">{value}</span>'
        else:
            rendered = f"<code>{value}</code>"
        protected.append(rendered)
        return f"\x00{len(protected)-1}\x00"

    escaped = CODE_RE.sub(protect_code, escaped)
    escaped = BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = EM_RE.sub(r"<em>\1</em>", escaped)
    escaped = TOKEN_RE.sub(lambda match: f'<span class="token">{match.group(0)}</span>', escaped)
    for index, value in enumerate(protected):
        escaped = escaped.replace(f"\x00{index}\x00", value)
    return escaped


def _render_block(block: dict[str, Any]) -> str:
    block_type = block.get("type")
    if block_type == "paragraph":
        return f"<p>{_render_inline(str(block.get('text', '')))}</p>"
    if block_type == "heading":
        level = int(block.get("level", 3))
        level = min(6, max(2, level))
        return f"<h{level}>{_render_inline(str(block.get('text', '')))}</h{level}>"
    if block_type == "list":
        tag = "ol" if block.get("ordered") else "ul"
        items = "".join(f"<li>{_render_inline(str(item))}</li>" for item in block.get("items", []))
        return f"<{tag}>{items}</{tag}>"
    if block_type in {"formula", "diagram"}:
        class_name = "formula" if block_type == "formula" else "diagram"
        return f'<pre class="{class_name}">{html.escape(str(block.get("text", "")))}</pre>'
    if block_type == "quote":
        return f"<blockquote>{_render_inline(str(block.get('text', '')))}</blockquote>"
    if block_type in {"definition", "hypothesis", "observation", "example", "note", "warning", "principle"}:
        title = block.get("title") or block_type.capitalize()
        body = _render_inline(str(block.get("text", "")))
        extra = ""
        if block_type == "hypothesis" and block.get("confidence") is not None:
            extra = f'<p class="metadata">Confidence: {html.escape(str(block["confidence"]))}</p>'
        return (
            f'<aside class="{block_type}"><h4>{_render_inline(str(title))}</h4>'
            f"<p>{body}</p>{extra}</aside>"
        )
    if block_type == "code":
        language = html.escape(str(block.get("language", "text")))
        return f'<pre class="code"><code data-language="{language}">{html.escape(str(block.get("text", "")))}</code></pre>'
    if block_type == "table":
        headers = block.get("headers", [])
        rows = block.get("rows", [])
        head = "".join(f"<th>{_render_inline(str(cell))}</th>" for cell in headers)
        body = "".join(
            "<tr>" + "".join(f"<td>{_render_inline(str(cell))}</td>" for cell in row) + "</tr>"
            for row in rows
        )
        return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"
    raise ValueError(f"Unsupported content block type: {block_type}")


def _nav(up_href: str, up_label: str, previous: tuple[str, str] | None, contents_href: str, next_page: tuple[str, str] | None) -> str:
    previous_html = (
        f'<a rel="prev" href="{html.escape(previous[0])}">← {html.escape(previous[1])}</a>'
        if previous
        else '<span class="disabled">← Previous</span>'
    )
    next_html = (
        f'<a rel="next" href="{html.escape(next_page[0])}">{html.escape(next_page[1])} →</a>'
        if next_page
        else '<span class="disabled">Next →</span>'
    )
    return (
        '<nav class="page-navigation" aria-label="Page navigation">'
        f'<a class="up" href="{html.escape(up_href)}">↑ {html.escape(up_label)}</a>'
        f"{previous_html}"
        f'<a class="contents" href="{html.escape(contents_href)}">☰ Contents</a>'
        f"{next_html}"
        "</nav>"
    )


def _page(title: str, stylesheet_href: str, navigation: str, heading_html: str, body_html: str, footer_text: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{html.escape(stylesheet_href)}">
</head>
<body>
<div class="container">
{navigation}
<header>{heading_html}</header>
<main>{body_html}</main>
<footer><p>{html.escape(footer_text)}</p>{navigation}</footer>
</div>
</body>
</html>
"""


class DocumentationBuilder:
    def __init__(self, state: ResearchState, assets_dir: str | Path):
        self.state = state
        self.assets_dir = Path(assets_dir)
        chapter_document = state.documents.get("chapters", {})
        self.chapters = sorted(chapter_document.get("chapters", []), key=lambda value: value["order"])

    def build(self, output_dir: str | Path) -> list[Path]:
        output = Path(output_dir)
        if output.exists():
            shutil.rmtree(output)
        output.mkdir(parents=True)
        shutil.copy2(self.assets_dir / "cognitive.css", output / "cognitive.css")
        created = [output / "cognitive.css"]
        pages = self._page_sequence()
        created.extend(self._build_global_index(output))
        for chapter_index, chapter in enumerate(self.chapters):
            if chapter["layout"] == "single":
                created.append(self._build_single_chapter(output, chapter_index, chapter))
            else:
                created.extend(self._build_directory_chapter(output, chapter_index, chapter, pages))
        created.extend(self._build_reference_pages(output))
        return created

    def _page_sequence(self) -> list[PageRef]:
        refs: list[PageRef] = []
        for ci, chapter in enumerate(self.chapters):
            for si, section in enumerate(sorted(chapter["sections"], key=lambda value: value["order"])):
                if chapter["layout"] == "single":
                    path = f"chapter{chapter['order']:02d}.html"
                else:
                    path = f"chapter{chapter['order']:02d}/{chapter['order']:02d}_{section['order']:02d}.html"
                refs.append(PageRef(ci, si, path, chapter["title"], section["title"]))
        return refs

    def _build_global_index(self, output: Path) -> list[Path]:
        chapter_items = []
        for chapter in self.chapters:
            if chapter["layout"] == "single":
                href = f"chapter{chapter['order']:02d}.html"
            else:
                href = f"chapter{chapter['order']:02d}/index.html"
            chapter_items.append(
                f'<li><a href="{href}">Chapter {chapter["order"]}: {html.escape(chapter["title"])}</a>'
                f'<p>{_render_inline(chapter.get("summary", ""))}</p></li>'
            )
        body = (
            '<section class="document-summary"><p>'
            'A practical engineering architecture for long-lived cognitive systems, '
            'continuous memory consolidation, objective-driven world models, communication, '
            'hybrid computation, and persistent Research State.'
            '</p></section>'
            '<h2>Chapters</h2><ol class="chapter-list">' + "".join(chapter_items) + "</ol>"
            '<h2>Project References</h2><ul>'
            '<li><a href="tokens.html">Token Registry</a></li>'
            '<li><a href="research-state.html">Research State Summary</a></li>'
            '<li><a href="style-guide.html">Documentation Style Guide</a></li>'
            '</ul>'
        )
        nav = _nav("index.html", "Documentation", None, "index.html", None)
        page = _page(
            "Architectural Evolution of Long-Lived Cognitive Systems",
            "cognitive.css",
            nav,
            '<h1>Architectural Evolution of Long-Lived Cognitive Systems</h1><p class="subtitle">Engineering Research Draft 0.1</p>',
            body,
            "Canonical English documentation generated from Research State.",
        )
        path = output / "index.html"
        path.write_text(page, encoding="utf-8")
        return [path]

    def _chapter_links(self, chapter_index: int, from_directory: bool) -> tuple[tuple[str, str] | None, tuple[str, str] | None]:
        prefix = "../" if from_directory else ""
        previous = None
        next_page = None
        if chapter_index > 0:
            chapter = self.chapters[chapter_index - 1]
            target = f"chapter{chapter['order']:02d}.html" if chapter["layout"] == "single" else f"chapter{chapter['order']:02d}/index.html"
            previous = (prefix + target, f"Chapter {chapter['order']}")
        if chapter_index + 1 < len(self.chapters):
            chapter = self.chapters[chapter_index + 1]
            target = f"chapter{chapter['order']:02d}.html" if chapter["layout"] == "single" else f"chapter{chapter['order']:02d}/index.html"
            next_page = (prefix + target, f"Chapter {chapter['order']}")
        return previous, next_page

    def _build_single_chapter(self, output: Path, chapter_index: int, chapter: dict[str, Any]) -> Path:
        sections = sorted(chapter["sections"], key=lambda value: value["order"])
        body_parts = []
        for section in sections:
            content = self.state.load_content(section["content_file"])
            body_parts.append(f'<section id="section-{section["order"]}"><h2>{chapter["order"]}.{section["order"]} {html.escape(section["title"])}</h2>')
            body_parts.extend(_render_block(block) for block in content.get("blocks", []))
            body_parts.append("</section>")
        previous, next_page = self._chapter_links(chapter_index, False)
        nav = _nav("index.html", "Documentation", previous, "index.html", next_page)
        page = _page(
            f"Chapter {chapter['order']} · {chapter['title']}",
            "cognitive.css",
            nav,
            f'<h1>Chapter {chapter["order"]}</h1><h2>{html.escape(chapter["title"])}</h2>',
            "".join(body_parts),
            f"Chapter {chapter['order']} · {chapter['title']}",
        )
        path = output / f"chapter{chapter['order']:02d}.html"
        path.write_text(page, encoding="utf-8")
        return path

    def _build_directory_chapter(self, output: Path, chapter_index: int, chapter: dict[str, Any], pages: list[PageRef]) -> list[Path]:
        directory = output / f"chapter{chapter['order']:02d}"
        directory.mkdir()
        created: list[Path] = []
        sections = sorted(chapter["sections"], key=lambda value: value["order"])
        previous_chapter, next_chapter = self._chapter_links(chapter_index, True)
        index_nav = _nav("../index.html", "Documentation", previous_chapter, "index.html", next_chapter)
        items = "".join(
            f'<li><a href="{chapter["order"]:02d}_{section["order"]:02d}.html">'
            f'{chapter["order"]}.{section["order"]} {html.escape(section["title"])}</a></li>'
            for section in sections
        )
        index_page = _page(
            f"Chapter {chapter['order']} · {chapter['title']}",
            "../cognitive.css",
            index_nav,
            f'<h1>Chapter {chapter["order"]}</h1><h2>{html.escape(chapter["title"])}</h2><p>{_render_inline(chapter.get("summary", ""))}</p>',
            f'<h3>Contents</h3><ol class="section-list">{items}</ol>',
            f"Chapter {chapter['order']} contents.",
        )
        index_path = directory / "index.html"
        index_path.write_text(index_page, encoding="utf-8")
        created.append(index_path)

        chapter_refs = [ref for ref in pages if ref.chapter_index == chapter_index]
        for local_index, section in enumerate(sections):
            content = self.state.load_content(section["content_file"])
            previous = None
            next_page = None
            if local_index > 0:
                prev = sections[local_index - 1]
                previous = (f'{chapter["order"]:02d}_{prev["order"]:02d}.html', "Previous")
            if local_index + 1 < len(sections):
                nxt = sections[local_index + 1]
                next_page = (f'{chapter["order"]:02d}_{nxt["order"]:02d}.html', "Next")
            nav = _nav("index.html", "Up", previous, "../index.html", next_page)
            body = "".join(_render_block(block) for block in content.get("blocks", []))
            page = _page(
                f"Chapter {chapter['order']} · Section {chapter['order']}.{section['order']} · {section['title']}",
                "../cognitive.css",
                nav,
                (
                    f'<p class="chapter-label">Chapter {chapter["order"]}</p>'
                    f'<h1>{html.escape(chapter["title"])}</h1>'
                    f'<p class="section-label">Section {chapter["order"]}.{section["order"]}</p>'
                    f'<h2>{html.escape(section["title"])}</h2>'
                ),
                body,
                f"Section {chapter['order']}.{section['order']} · {section['title']}",
            )
            path = directory / f'{chapter["order"]:02d}_{section["order"]:02d}.html'
            path.write_text(page, encoding="utf-8")
            created.append(path)
        return created

    def _build_reference_pages(self, output: Path) -> list[Path]:
        created: list[Path] = []
        nav = _nav("index.html", "Documentation", None, "index.html", None)

        token_rows = []
        for token in self.state.token_entries():
            if token.get("atomic"):
                definition = token.get("definition", "")
                form = "Atomic"
            else:
                expression = token.get("expression", {})
                definition = f"{expression.get('operator')}({', '.join(expression.get('arguments', []))})"
                form = "Derived"
            token_rows.append(
                f'<tr><td><span class="token">{html.escape(token["token"])}</span></td>'
                f'<td>{form}</td><td>{_render_inline(str(definition))}</td></tr>'
            )
        token_page = _page(
            "Token Registry",
            "cognitive.css",
            nav,
            "<h1>Token Registry</h1>",
            '<table><thead><tr><th>Token</th><th>Class</th><th>Definition</th></tr></thead><tbody>' + "".join(token_rows) + "</tbody></table>",
            "Generated from state/tokens.yaml.",
        )
        token_path = output / "tokens.html"
        token_path.write_text(token_page, encoding="utf-8")
        created.append(token_path)

        summaries = []
        for role, document in self.state.documents.items():
            if isinstance(document, dict):
                count = sum(len(value) for value in document.values() if isinstance(value, list))
            else:
                count = 0
            summaries.append(f"<tr><td>{html.escape(role)}</td><td>{count}</td></tr>")
        state_page = _page(
            "Research State Summary",
            "cognitive.css",
            nav,
            "<h1>Research State Summary</h1>",
            '<p>The Research State is the canonical, implementation-independent project state from which documentation is generated.</p>'
            '<table><thead><tr><th>Role</th><th>Entity count</th></tr></thead><tbody>' + "".join(summaries) + "</tbody></table>",
            "Generated Research State overview.",
        )
        state_path = output / "research-state.html"
        state_path.write_text(state_page, encoding="utf-8")
        created.append(state_path)

        style_blocks = [
            ("Token", '<span class="token">T_ModelIntegration</span>'),
            ("Definition", '<aside class="definition"><h4>Definition</h4><p>A formal project definition.</p></aside>'),
            ("Hypothesis", '<aside class="hypothesis"><h4>Working Hypothesis</h4><p>A falsifiable architectural claim.</p></aside>'),
            ("Observation", '<aside class="observation"><h4>Observation</h4><p>An observed property used as evidence.</p></aside>'),
            ("Example", '<aside class="example"><h4>Example</h4><p>A concrete illustration.</p></aside>'),
        ]
        style_body = "".join(f"<h2>{title}</h2>{sample}" for title, sample in style_blocks)
        style_page = _page(
            "Documentation Style Guide",
            "cognitive.css",
            nav,
            "<h1>Documentation Style Guide</h1>",
            '<p>The documentation uses semantic HTML and a restrained ISO/RFC/W3C-inspired presentation.</p>' + style_body,
            "Documentation Architecture Specification preview.",
        )
        style_path = output / "style-guide.html"
        style_path.write_text(style_page, encoding="utf-8")
        created.append(style_path)
        return created
