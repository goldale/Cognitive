from __future__ import annotations

import argparse
import re
import json
import shutil
import sys
import tarfile
from pathlib import Path

from . import __version__, yaml_profile
from .canonical import format_file
from .consolidation import apply_proposal
from .docs import DocumentationBuilder
from .graph import write_token_graph
from .semantic_merge import three_way_merge
from .state import ResearchState
from .validation import StateValidator


def _state_root(value: str) -> Path:
    path = Path(value).resolve()
    if not (path / "manifest.yaml").is_file():
        raise argparse.ArgumentTypeError(f"Not a Research State directory: {path}")
    return path


def cmd_validate(args: argparse.Namespace) -> int:
    state = ResearchState.load(args.state)
    schema = Path(args.schema) if args.schema else Path(__file__).resolve().parents[2] / "schemas" / "research-state.schema.json"
    report = StateValidator(schema).validate(state)
    for issue in report.issues:
        print(f"{issue.severity.upper():7} {issue.code:28} {issue.path}: {issue.message}")
    print(json.dumps(report.metrics, indent=2))
    return 0 if report.ok else 1


def cmd_format(args: argparse.Namespace) -> int:
    state = ResearchState.load(args.state)
    changed = []
    for path in sorted(state.root.rglob("*.yaml")):
        if format_file(path):
            changed.append(path.relative_to(state.root))
    for path in changed:
        print(path)
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    state = ResearchState.load(args.state)
    assets = Path(args.assets) if args.assets else Path(__file__).resolve().parents[2] / "assets"
    output = Path(args.output).resolve()
    created = DocumentationBuilder(state, assets).build(output)
    print(f"Generated {len(created)} files in {output}")
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    state = ResearchState.load(args.state)
    write_token_graph(state, args.output)
    print(args.output)
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    changed = apply_proposal(args.state, args.proposal)
    print("Changed roles:", ", ".join(changed))
    return 0


def cmd_merge(args: argparse.Namespace) -> int:
    base = yaml_profile.load(args.base)
    ours = yaml_profile.load(args.ours)
    theirs = yaml_profile.load(args.theirs)
    result = three_way_merge(base, ours, theirs)
    yaml_profile.dump(result.value, args.output)
    report = {
        "kind": "T_SemanticMergeReport",
        "conflicts": [
            {"path": conflict.path, "base": conflict.base, "ours": conflict.ours, "theirs": conflict.theirs}
            for conflict in result.conflicts
        ],
    }
    yaml_profile.dump(report, args.report)
    print(f"Merged output: {args.output}")
    print(f"Conflict report: {args.report} ({len(result.conflicts)} conflicts)")
    return 2 if result.conflicts else 0


def cmd_release(args: argparse.Namespace) -> int:
    root = Path(args.project).resolve()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if not str(output).endswith((".tar.gz", ".tgz")):
        output = output.with_suffix(output.suffix + ".tar.gz" if output.suffix else ".tar.gz")
    excluded_directories = {".git", ".venv", ".pytest_cache", "__pycache__", "dist", "build"}
    excluded_suffixes = {".pyc", ".pyo"}

    def excluded_release_artifact(relative: Path) -> bool:
        # Stage-gate generators, validators, and reports are build/validation
        # artifacts, not release content. Match at any directory depth and
        # without case sensitivity (for example STAGE3_*, validate_stage3_*).
        if re.search(r"stage[0-9]+_", relative.name, flags=re.IGNORECASE):
            return True
        # Git and release archives use one unversioned release-notes file.
        # Any versioned RELEASE_NOTES_*.md file is a stale release artifact.
        if len(relative.parts) == 1 and relative.name.startswith("RELEASE_NOTES_"):
            return True
        return False

    with tarfile.open(output, "w:gz") as archive:
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            if any(part in excluded_directories or part.endswith(".egg-info") for part in relative.parts):
                continue
            if path.suffix in excluded_suffixes or excluded_release_artifact(relative):
                continue
            archive.add(path, arcname=Path(root.name) / relative, recursive=False)
    print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cogstate", description="Research State engineering tools")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate", help="Validate a Research State")
    p.add_argument("state", type=_state_root)
    p.add_argument("--schema")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("format", help="Canonicalize all YAML files")
    p.add_argument("state", type=_state_root)
    p.set_defaults(func=cmd_format)

    p = sub.add_parser("build", help="Generate HTML documentation")
    p.add_argument("state", type=_state_root)
    p.add_argument("--output", required=True)
    p.add_argument("--assets")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("graph", help="Generate a Graphviz token graph")
    p.add_argument("state", type=_state_root)
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_graph)

    p = sub.add_parser("apply", help="Apply a semantic change proposal")
    p.add_argument("state", type=_state_root)
    p.add_argument("proposal")
    p.set_defaults(func=cmd_apply)

    p = sub.add_parser("merge", help="Perform a structural three-way merge")
    p.add_argument("base")
    p.add_argument("ours")
    p.add_argument("theirs")
    p.add_argument("--output", required=True)
    p.add_argument("--report", required=True)
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("release", help="Create a tar.gz project snapshot")
    p.add_argument("project")
    p.add_argument("--output", required=True)
    p.set_defaults(func=cmd_release)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:  # CLI boundary; individual modules retain typed exceptions.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
