from __future__ import annotations

from pathlib import Path

from .state import ResearchState


def write_token_graph(state: ResearchState, output_path: str | Path) -> None:
    lines = ["digraph TokenGraph {", "  rankdir=LR;", '  node [shape=box, fontname="Helvetica"];']
    for entry in state.token_entries():
        token = entry["token"]
        shape = "ellipse" if entry.get("atomic") else "box"
        lines.append(f'  "{token}" [shape={shape}];')
        expression = entry.get("expression", {})
        if isinstance(expression, dict):
            for reference in [expression.get("operator"), *expression.get("arguments", [])]:
                if isinstance(reference, str):
                    lines.append(f'  "{reference}" -> "{token}";')
    lines.append("}")
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
