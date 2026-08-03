# Cognitive 0.3.16 — Release Certificate

**Release date:** 2026-08-03  
**Release type:** Architectural evolution roadmap  
**Canonical source:** YAML under `state/`  
**Status:** RELEASED

## Certified additions

1. Part V — Architectural Evolution is introduced.
2. Chapter 20 defines the authoritative Architectural Evolution Roadmap.
3. Chapter 21 defines the Research Agenda and falsifiable experiments.
4. Chapter 22 defines the Long-Term Vision.
5. Chapter 23 records Open Research Questions.
6. The A–Z Index is moved to Chapter 24 and regenerated.

## Certified development order

1. Importance Estimation.
2. Offline Consolidation and Sleep.
3. Replay.
4. Forgetting and Memory Pruning.
5. Structural Plasticity.
6. Global Evaluation.
7. Multi-Agent Semantic Learning.

## Preserved invariants

- Associative Memory learns exclusively from Transformer-produced Semantic Representations through the Semantic Feedback Learning Pipeline.
- READ never modifies Memory State.
- UPDATE modifies only Memory State, performs no implicit READ, and never produces a Memory Vector.
- Replay must not bypass the Transformer or the Semantic Feedback Learning Pipeline.

## Validation summary

| Gate | Result |
|---|---:|
| Research State validation | PASS |
| HTML generation | 149 files |
| Project tests | 32 / 32 |
| A–Z Index navigation | PASS |
| Roadmap priority order | PASS |

This certificate applies to the archive identified by `cognitive-0.3.16.tgz.sha256`.
