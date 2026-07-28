# Architectural Evolution of Long-Lived Cognitive Systems

This repository is a working engineering implementation of a research program for long-lived cognitive systems. It does not claim to implement general intelligence or subjective consciousness. It implements the infrastructure and executable mechanisms that can be built now and tested before deeper integration is attempted.

The project originated through a long research dialogue between a human systems engineer with a background in applied mathematics, physics, and software engineering and an OpenAI language model. The consolidated architecture is therefore a product of joint cognitive work rather than a transcript, a one-sided manuscript, or a conventional author-editor workflow.

## Implemented components

The repository contains four operational layers.

1. **Canonical Research State**
   - Restricted YAML profile.
   - Formal `T_PascalCaseIdentifier` Token registry.
   - Atomic Tokens as axioms and derived Tokens expressed only through earlier Atomic Tokens.
   - Principles, hypotheses, architecture decisions, open questions, roadmap, and chapter state.
   - Latest-only semantic consolidation record; Git is intended to carry prior records through commits.

2. **Research tooling**
   - YAML profile enforcement: no aliases, anchors, custom tags, duplicate keys, or implicit dates.
   - JSON Schema validation plus semantic validation.
   - Canonical formatting for Git-friendly diffs.
   - Change-proposal application.
   - Structural three-way merge with an explicit semantic-conflict report.
   - Token dependency graph generation.

3. **Generated documentation**
   - Twelve English chapters generated from Research State.
   - Semantic HTML and an ISO/RFC/W3C-inspired stylesheet.
   - Stable Up, Previous, Contents, and Next navigation.
   - Separate rendering for Tokens, definitions, hypotheses, observations, examples, notes, warnings, formulas, and principles.

4. **Executable cognitive-runtime prototypes**
   - Objective-driven world models.
   - Working and lossy long-term memory.
   - Asynchronous-style consolidation and iterative architecture selection.
   - Partial serialization, deserialization, clarification, model integration, and conflict detection.
   - Trainable integrated multichannel evaluation.
   - Trainable allocation among neural, algorithmic, and hybrid computation.
   - Cognitive lineages with champion cloning inside lineages and diversity preservation across lineages.

## Repository structure

```text
cognitive-systems-lab/
├── assets/                 Documentation stylesheet
├── docs/                   Generated HTML; never the canonical source
├── examples/               Change proposals, merge examples, runtime demo
├── schemas/                JSON Schema
├── scripts/                Bootstrap and release scripts
├── spec/                   Formal engineering specifications
├── src/cogsys/             Research State tooling
│   └── runtime/            Executable cognitive prototypes
├── state/                  Canonical Research State
│   └── content/            Structured chapter content
└── tests/                  Validation and runtime tests
```

## Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation
```

## Core commands

```bash
cogstate validate state --schema schemas/research-state.schema.json
cogstate format state
cogstate build state --output docs --assets assets
cogstate graph state --output docs/token-graph.dot
python -m cogsys.runtime.demo
pytest
```

The generated documentation entry point is `docs/index.html`.

## Semantic change workflow

A human reviewer comments on generated documentation or the model. The comments are converted into a `T_ChangeProposal`. The proposal updates canonical Research State and, for semantic changes, replaces `state/consolidation.yaml:latest` with the record describing that transition. Documentation is regenerated from the new state.

```bash
cogstate apply state examples/change-proposal.yaml
cogstate validate state --schema schemas/research-state.schema.json
cogstate build state --output docs --assets assets
```

Generated HTML is not manually edited. It is a partial serialization of canonical Research State for a human audience.

## Semantic merge workflow

Git preserves file history and branches. The project tool performs a structural three-way merge and writes unresolved semantic conflicts to a separate report.

```bash
cogstate merge \
  examples/merge/base.yaml \
  examples/merge/ours.yaml \
  examples/merge/theirs.yaml \
  --output examples/merge/merged.yaml \
  --report examples/merge/conflicts.yaml
```

The tool intentionally does not pretend that every textual merge is a semantic consolidation. A true consolidation may produce a state that belongs to neither input branch.

## Engineering status

The Research State toolchain and runtime demonstrations are executable. The integrated holographic representation, persistent functional Self, and general emergence of higher-level behavior remain working hypotheses and research targets. The repository keeps these categories explicit.

## Language and licensing

All project artifacts are canonical in English. No public license is granted by this draft repository. Select and add a license before public distribution or group contribution.
