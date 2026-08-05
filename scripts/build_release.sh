#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
PYTHONPATH=src python3 -m cogsys.cli validate state --schema schemas/research-state.schema.json
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m cogsys.cli build state --output docs --assets assets
PYTHONPATH=src python3 -m cogsys.cli graph state --output docs/token-graph.dot
if command -v dot >/dev/null 2>&1; then dot -Tsvg docs/token-graph.dot -o docs/token-graph.svg; fi
mkdir -p dist
OUTPUT=${1:-dist/cognitive.tgz}
PYTHONPATH=src python3 -m cogsys.cli release . --output "$OUTPUT"
