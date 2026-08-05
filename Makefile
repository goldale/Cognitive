PYTHON ?= python3
STATE := state
DOCS := docs
SCHEMA := schemas/research-state.schema.json

.PHONY: install validate format docs graph demo test release clean

install:
	$(PYTHON) -m pip install -e '.[dev]'

validate:
	PYTHONPATH=src $(PYTHON) -m cogsys.cli validate $(STATE) --schema $(SCHEMA)

format:
	PYTHONPATH=src $(PYTHON) -m cogsys.cli format $(STATE)

docs:
	PYTHONPATH=src $(PYTHON) -m cogsys.cli build $(STATE) --output $(DOCS) --assets assets

graph:
	PYTHONPATH=src $(PYTHON) -m cogsys.cli graph $(STATE) --output docs/token-graph.dot
	@if command -v dot >/dev/null 2>&1; then dot -Tsvg docs/token-graph.dot -o docs/token-graph.svg; fi

demo:
	PYTHONPATH=src $(PYTHON) -m cogsys.runtime.demo

test:
	PYTHONPATH=src $(PYTHON) -m pytest

release: validate test docs graph
	mkdir -p dist
	PYTHONPATH=src $(PYTHON) -m cogsys.cli release . --output dist/cognitive-0.3.40.tgz

clean:
	rm -rf docs/* dist/* .pytest_cache
