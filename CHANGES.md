# CHANGES — cognitive 0.3.16

This release documents the authoritative future evolution path of the Cognitive architecture while preserving the architectural baseline established in 0.3.15.

## Added: Part V — Architectural Evolution

- Chapter 20 — Architectural Evolution Roadmap.
- Chapter 21 — Research Agenda.
- Chapter 22 — Long-Term Vision.
- Chapter 23 — Open Research Questions.
- The A–Z Index is moved from Chapter 19 to Chapter 24.

## Canonical development order

1. Importance Estimation.
2. Offline Consolidation and Sleep.
3. Replay.
4. Forgetting and Memory Pruning.
5. Structural Plasticity.
6. Global Evaluation.
7. Multi-Agent Semantic Learning.

## Preserved architectural invariants

- Associative Memory learns exclusively from Transformer-produced Semantic Representations through the Semantic Feedback Learning Pipeline.
- READ never modifies Memory State.
- UPDATE modifies only Memory State, performs no implicit READ, and never produces a Memory Vector.
- Replay does not bypass the Transformer or the Semantic Feedback Learning Pipeline.

## Documentation model

The roadmap distinguishes architectural direction from implementation status. Future mechanisms are explicitly marked as planned research and are generated from the canonical YAML Research State.
