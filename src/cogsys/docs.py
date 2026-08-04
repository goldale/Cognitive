from __future__ import annotations

import html
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .state import ResearchState


TOKEN_RE = re.compile(r"\bT_(?:[A-Z][A-Za-z0-9]*)+\b")
CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
EM_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


@dataclass(frozen=True)
class PageRef:
    chapter_index: int
    section_index: int
    path: str
    chapter_title: str
    section_title: str


def _humanize_token_label(token: str) -> str:
    label = token.removeprefix("T_")
    label = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", label)
    label = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", label)
    return label


def _render_inline(text: str) -> str:
    protected: list[str] = []

    def protect_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(1), quote=True)
        href = html.escape(match.group(2), quote=True)
        rendered = f'<a href="{href}">{label}</a>'
        protected.append(rendered)
        return f"\x00{len(protected)-1}\x00"

    text = LINK_RE.sub(protect_link, text)
    escaped = html.escape(text, quote=True)

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
    if block_type == "formula":
        return f'<pre class="formula">{html.escape(str(block.get("text", "")))}</pre>'
    if block_type == "diagram":
        if block.get("nodes"):
            return _render_structured_diagram(block)
        return f'<pre class="diagram diagram-fallback">{html.escape(str(block.get("text", "")))}</pre>'
    if block_type == "quote":
        return f"<blockquote>{_render_inline(str(block.get('text', '')))}</blockquote>"
    if block_type in {"definition", "hypothesis", "observation", "example", "note", "warning", "principle"}:
        title = block.get("title") or block_type.capitalize()
        body = _render_inline(str(block.get("text", "")))
        extra = ""
        if block_type == "hypothesis" and block.get("confidence") is not None:
            extra = f'<p class="metadata">Confidence: {html.escape(str(block["confidence"]))}</p>'
        object_id = str(block.get("object_id", "")).strip()
        id_attr = f' id="{html.escape(object_id, quote=True)}"' if object_id else ""
        return (
            f'<aside class="{block_type}"{id_attr}><h4>{_render_inline(str(title))}</h4>'
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


def _dot_quote(value: Any) -> str:
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def _render_structured_diagram(block: dict[str, Any]) -> str:
    title = str(block.get("title", "Architecture diagram"))
    description = str(block.get("description", title))
    direction = str(block.get("direction", "TB"))
    size = str(block.get("size", "standard"))
    if size not in {"compact", "standard", "medium", "large", "extra-large"}:
        size = "standard"
    if direction not in {"TB", "BT", "LR", "RL"}:
        direction = "TB"

    shape_by_kind = {
        "external": "oval",
        "data": "note",
        "state": "box3d",
        "storage": "cylinder",
        "interface": "component",
        "control": "hexagon",
        "subsystem": "box",
    }
    fill_by_kind = {
        "external": "#f8fafc",
        "data": "#f7f7fb",
        "state": "#eef6fb",
        "storage": "#f1f7f2",
        "interface": "#fff8e8",
        "control": "#fff3ed",
        "subsystem": "#f3f7fa",
    }
    color_by_flow = {
        "information": "#174a7e",
        "interface": "#8a6415",
        "evaluation": "#9a5a12",
        "control": "#a33e32",
        "learning": "#277448",
        "optimization": "#6b4fa1",
        "feedback": "#53606b",
        "context": "#53606b",
    }

    node_fontsize = {"compact": 11.5, "standard": 12, "medium": 13, "large": 15, "extra-large": 17}[size]
    edge_fontsize = {"compact": 9.5, "standard": 10, "medium": 10.5, "large": 12, "extra-large": 14}[size]
    node_margin = {"compact": "0.12,0.07", "standard": "0.16,0.10", "medium": "0.19,0.12", "large": "0.24,0.16", "extra-large": "0.30,0.20"}[size]
    nodesep = {"compact": "0.32", "standard": "0.48", "medium": "0.56", "large": "0.72", "extra-large": "0.90"}[size]
    ranksep = {"compact": "0.42", "standard": "0.72", "medium": "0.82", "large": "1.05", "extra-large": "1.25"}[size]

    lines = [
        "digraph G {",
        f"rankdir={direction};",
        f'graph [bgcolor="transparent", pad="0.34", nodesep="{nodesep}", ranksep="{ranksep}", splines="ortho", outputorder="edgesfirst"];',
        f'node [fontname="Arial", fontsize="{node_fontsize}", color="#365b78", fontcolor="#202124", penwidth="1.3", style="rounded,filled", margin="{node_margin}"];',
        f'edge [fontname="Arial", fontsize="{edge_fontsize}", color="#174a7e", fontcolor="#4f5962", penwidth="1.45", arrowsize="0.82"];',
    ]
    for node in block.get("nodes", []):
        node_id = str(node.get("id", ""))
        label = str(node.get("label", node_id))
        kind = str(node.get("kind", "subsystem"))
        status = str(node.get("status", "current"))
        attrs = {
            "label": label,
            "shape": shape_by_kind.get(kind, "box"),
            "fillcolor": fill_by_kind.get(kind, "#f3f7fa"),
        }
        if status == "future":
            attrs["style"] = "rounded,dashed,filled"
            attrs["color"] = "#7c7f83"
        rendered = ", ".join(f"{key}={_dot_quote(value)}" for key, value in attrs.items())
        lines.append(f"{_dot_quote(node_id)} [{rendered}];")
    for group in block.get("rank_groups", []):
        members = "; ".join(_dot_quote(node_id) for node_id in group)
        if members:
            lines.append(f"{{ rank=same; {members}; }}")
    for edge in block.get("edges", []):
        source = _dot_quote(edge.get("from", ""))
        target = _dot_quote(edge.get("to", ""))
        flow = str(edge.get("flow", "information"))
        attrs: dict[str, Any] = {"color": color_by_flow.get(flow, "#174a7e")}
        if edge.get("label"):
            attrs["label"] = str(edge["label"])
        if flow in {"feedback", "context"}:
            attrs["style"] = "dashed"
        rendered = ", ".join(f"{key}={_dot_quote(value)}" for key, value in attrs.items())
        lines.append(f"{source} -> {target} [{rendered}];")
    lines.append("}")
    dot = "\n".join(lines)
    try:
        result = subprocess.run(
            ["dot", "-Tsvg"],
            input=dot,
            text=True,
            capture_output=True,
            check=True,
            timeout=10,
        )
        svg = result.stdout
        svg = re.sub(r"<\?xml[^>]*>\s*", "", svg)
        svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
        # Graphviz restarts SVG element IDs for every diagram. Namespace them so
        # multiple diagrams can coexist on one generated HTML page without duplicate IDs.
        diagram_prefix = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "diagram"
        svg = re.sub(
            r'id="([^"]+)"',
            lambda match: f'id="{diagram_prefix}-{match.group(1)}"',
            svg,
        )
        svg = svg.replace("<svg ", '<svg role="img" aria-label="' + html.escape(description, quote=True) + '" ' , 1)
        return (
            f'<figure class="architecture-diagram diagram-size-{size}">'
            f'<div class="diagram-heading"><strong>{_render_inline(title)}</strong></div>'
            f'<div class="diagram-canvas">{svg}</div>'
            f'<figcaption>{_render_inline(description)}</figcaption>'
            '</figure>'
        )
    except (OSError, subprocess.SubprocessError):
        labels = " → ".join(str(node.get("label", node.get("id", ""))) for node in block.get("nodes", []))
        return (
            f'<figure class="architecture-diagram diagram-size-{size}">'
            f'<div class="diagram-heading"><strong>{_render_inline(title)}</strong></div>'
            f'<pre class="diagram diagram-fallback">{html.escape(labels)}</pre>'
            f'<figcaption>{_render_inline(description)}</figcaption>'
            '</figure>'
        )


def _nav(up_href: str, up_label: str, previous: tuple[str, str] | None, contents_href: str, next_page: tuple[str, str] | None, index_href: str = "chapter24/index.html") -> str:
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
        f'<a class="alphabetical-index" href="{html.escape(index_href)}">A–Z Index</a>'
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
<footer>{navigation}</footer>
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
        self.index_order = max((chapter["order"] for chapter in self.chapters), default=0) + 1

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
        created.extend(self._build_canonical_reference(output))
        created.extend(self._build_alphabetical_index(output))
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
        chapter_items.append(
            f'<li><a href="chapter{self.index_order:02d}/index.html">Chapter {self.index_order}: Alphabetical Index</a>'
            '<p>Alphabetical access to chapters, sections, typed knowledge objects, and canonical terms.</p></li>'
        )
        body = (
            '<section class="document-summary"><p>'
            'A practical engineering architecture for long-lived cognitive systems, '
            'continuous memory consolidation, objective-driven world models, communication, '
            'hybrid computation, persistent memory, and controlled architectural evolution.'
            '</p></section>'
            '<h2>Chapters</h2><ol class="chapter-list">' + "".join(chapter_items) + "</ol>"
            '<h2>Project References</h2><ul>'
            '<li><a href="tokens.html">Token Registry</a></li>'
            '<li><a href="research-state.html">Canonical YAML Model</a></li>'
            '<li><a href="style-guide.html">Documentation Style Guide</a></li>'
            '</ul>'
        )
        nav = _nav("index.html", "Documentation", None, "index.html", None)
        page = _page(
            "Cognitive Architecture Specification",
            "cognitive.css",
            nav,
            f'<h1>Cognitive Architecture Specification</h1><p class="subtitle">Version {html.escape(str(self.state.manifest.get("schema_version", self.state.manifest.get("version", "unknown"))))}</p><p class="document-author"><strong>Author</strong><br>Alex Goldenstein</p>',
            body,
            "Canonical English architecture specification generated from validated YAML.",
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
        elif chapter_index == len(self.chapters) - 1:
            next_page = (prefix + f"chapter{self.index_order:02d}/index.html", f"Chapter {self.index_order}")
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
        index_nav = _nav("../index.html", "Documentation", previous_chapter, "index.html", next_chapter, f"../chapter{self.index_order:02d}/index.html")
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
            nav = _nav("index.html", "Up", previous, "../index.html", next_page, f"../chapter{self.index_order:02d}/index.html")
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

    def _build_alphabetical_index(self, output: Path) -> list[Path]:
        entries: list[tuple[str, str, str]] = []
        for chapter in self.chapters:
            chapter_href = (f"../chapter{chapter['order']:02d}.html" if chapter["layout"] == "single" else f"../chapter{chapter['order']:02d}/index.html")
            entries.append((chapter["title"], chapter_href, f"Chapter {chapter['order']}"))
            for section in sorted(chapter["sections"], key=lambda value: value["order"]):
                if chapter["layout"] == "single":
                    href = chapter_href + f"#section-{section['order']}"
                else:
                    href = f"../chapter{chapter['order']:02d}/{chapter['order']:02d}_{section['order']:02d}.html"
                entries.append((section["title"], href, f"Section {chapter['order']}.{section['order']}"))
        for chapter in self.chapters:
            for section in chapter["sections"]:
                content = self.state.load_content(section["content_file"])
                for block in content.get("blocks", []):
                    object_id = str(block.get("object_id", "")).strip()
                    if not object_id:
                        continue
                    if chapter["layout"] == "single":
                        href = f"../chapter{chapter['order']:02d}.html#" + object_id
                    else:
                        href = f"../chapter{chapter['order']:02d}/{chapter['order']:02d}_{section['order']:02d}.html#" + object_id
                    object_kind = {"RN": "Research Note", "AN": "Architectural Note", "IN": "Implementation Note", "HP": "Historical Perspective"}.get(object_id.split("-", 1)[0], "Typed knowledge object")
                    entries.append((str(block.get("title", object_id)), href, object_kind))
        for token in self.state.token_entries():
            label = _humanize_token_label(token["token"])
            entries.append((label, token.get("index_target", "../tokens.html"), "Canonical term"))
        canonical_dir = self.state.root / 'canonical'
        terminology_path = canonical_dir / 'terminology.yaml'
        if terminology_path.is_file():
            from . import yaml_profile
            terminology = yaml_profile.load(terminology_path)
            for item in terminology.get('terms', []):
                entries.append((str(item.get('term', '')), '../canonical-model.html#term-' + re.sub(r'[^a-z0-9]+', '-', str(item.get('term', '')).lower()).strip('-'), 'Canonical architecture term'))
        entries.sort(key=lambda item: item[0].casefold())
        groups: dict[str, list[tuple[str, str, str]]] = {}
        for entry in entries:
            key = entry[0][0].upper() if entry[0] else "#"
            groups.setdefault(key, []).append(entry)
        jump = " ".join(f'<a href="#index-{html.escape(letter)}">{html.escape(letter)}</a>' for letter in groups)
        sections = [f'<nav class="index-jump" aria-label="Alphabetical index letters">{jump}</nav>']
        for letter, values in groups.items():
            items = "".join(f'<li><a href="{html.escape(href)}">{html.escape(label)}</a><span class="index-kind">{html.escape(kind)}</span></li>' for label, href, kind in values)
            sections.append(f'<section class="alphabetical-group" id="index-{html.escape(letter)}"><h2>{html.escape(letter)}</h2><ul>{items}</ul></section>')

        directory = output / f"chapter{self.index_order:02d}"
        directory.mkdir()
        previous_chapter = self.chapters[-1]
        previous_target = (
            f"../chapter{previous_chapter['order']:02d}.html"
            if previous_chapter["layout"] == "single"
            else f"../chapter{previous_chapter['order']:02d}/index.html"
        )
        nav = _nav("../index.html", "Documentation", (previous_target, f"Chapter {previous_chapter['order']}"), "../index.html", None, "index.html")
        page = _page(
            f"Chapter {self.index_order} · Alphabetical Index",
            "../cognitive.css",
            nav,
            f'<p class="chapter-label">Chapter {self.index_order}</p><h1>Alphabetical Index</h1><p class="subtitle">Chapters, sections, typed knowledge objects, and canonical terms</p>',
            "".join(sections),
            f"Chapter {self.index_order} · Generated from the canonical specification model.",
        )
        chapter_path = directory / "index.html"
        chapter_path.write_text(page, encoding="utf-8")

        compatibility = _page(
            "Alphabetical Index",
            "cognitive.css",
            _nav("index.html", "Documentation", None, "index.html", (f"chapter{self.index_order:02d}/index.html", f"Chapter {self.index_order}")),
            '<h1>Alphabetical Index</h1>',
            f'<p>The Alphabetical Index is now <a href="chapter{self.index_order:02d}/index.html">Chapter {self.index_order} of the main documentation</a>.</p>',
            "Compatibility entry point.",
        )
        compatibility_path = output / "alphabetical-index.html"
        compatibility_path.write_text(compatibility, encoding="utf-8")
        return [chapter_path, compatibility_path]


    def _build_canonical_reference(self, output: Path) -> list[Path]:
        from . import yaml_profile
        canonical_dir = self.state.root / "canonical"
        if not canonical_dir.is_dir():
            return []
        nav = _nav("index.html", "Documentation", None, "index.html", None)
        parts = ["<h2>Canonical Components</h2>"]
        components = yaml_profile.load(canonical_dir / "components.yaml").get("components", [])
        rows = "".join(f"<tr><td>{html.escape(str(c.get('name','')))}</td><td>{html.escape(', '.join(c.get('roles', [])))}</td></tr>" for c in components)
        parts.append("<table><thead><tr><th>Component</th><th>Roles</th></tr></thead><tbody>" + rows + "</tbody></table>")
        parts.append("<h2>Operation Contracts</h2>")
        operations = yaml_profile.load(canonical_dir / "contracts.yaml").get("operations", [])
        rows = "".join(f"<tr><td><strong>{html.escape(str(o.get('name','')))}</strong></td><td>{html.escape(', '.join(o.get('inputs', [])))}</td><td>{html.escape(', '.join(o.get('outputs', [])))}</td></tr>" for o in operations)
        parts.append("<table><thead><tr><th>Operation</th><th>Inputs</th><th>Outputs</th></tr></thead><tbody>" + rows + "</tbody></table>")
        parts.append("<h2>Canonical Terminology</h2>")
        terms = yaml_profile.load(canonical_dir / "terminology.yaml").get("terms", [])
        for item in terms:
            anchor = re.sub(r"[^a-z0-9]+", "-", str(item.get("term", "")).lower()).strip("-")
            parts.append(f'<section id="term-{anchor}"><h3>{html.escape(str(item.get("term", "")))}</h3><p>{html.escape(str(item.get("definition", "")))}</p></section>')
        page = _page("Canonical Architecture Model", "cognitive.css", nav, "<h1>Canonical Architecture Model</h1>", "".join(parts), "Generated from state/canonical/*.yaml.")
        path = output / "canonical-model.html"
        path.write_text(page, encoding="utf-8")
        return [path]

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
            "Canonical YAML Model",
            "cognitive.css",
            nav,
            "<h1>Canonical YAML Model</h1>",
            '<p>The canonical YAML model is the implementation-independent source from which this specification is generated.</p>'
            '<table><thead><tr><th>Role</th><th>Entity count</th></tr></thead><tbody>' + "".join(summaries) + "</tbody></table>",
            "Generated canonical-model overview.",
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
