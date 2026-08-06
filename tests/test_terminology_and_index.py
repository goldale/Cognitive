from pathlib import Path
import re

from cogsys.docs import DocumentationBuilder
from cogsys.state import ResearchState

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_memory_and_message_names_are_uniform():
    extensions = {".md", ".yaml", ".yml", ".html", ".py", ".json", ".toml", ".txt", ".dot"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions or any(part in {".git", "dist", ".pytest_cache"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        forbidden = [
            "LTM" + "-1", "LTM" + "-2",
            "msg" + "1", "msg" + "2",
            "msg" + "-1", "msg" + "-2",
        ]
        assert not any(value in text for value in forbidden), path


def test_index_links_to_text_definitions_and_token_rows(tmp_path: Path):
    state = ResearchState.load(ROOT / "state")
    DocumentationBuilder(state, ROOT / "assets").build(tmp_path)
    index = (tmp_path / "chapter27" / "index.html").read_text(encoding="utf-8")
    chapter = (tmp_path / "chapter12" / "12_11.html").read_text(encoding="utf-8")
    tokens = (tmp_path / "tokens.html").read_text(encoding="utf-8")
    assert '../chapter12/11_11.html#definition-LTM2' in index
    assert '<aside class="definition" id="definition-LTM2"><h4>LTM2</h4>' in chapter
    assert '../tokens.html#token-long-term-memory' in index
    assert 'id="token-long-term-memory"' in tokens
