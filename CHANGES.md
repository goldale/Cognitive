# CHANGES — cognitive 0.3.15

This incremental release introduces a complete architectural refactoring around Semantic Feedback Learning.

## Architectural changes

- **Transformer as Semantic Teacher** — The Transformer performs semantic reasoning and acts as the Semantic Teacher of Associative Memory.
- **Semantic feedback learning** — Associative Memory learns from Semantic Representations produced by the Transformer rather than from raw external observations.
- **Self-learning as an architectural object** — The Semantic Feedback Learning Pipeline is a first-class architectural object with explicit stages, contracts, invariants, and extension points.
- **READ and UPDATE asymmetry** — READ may produce a Memory Vector without modifying Memory State; UPDATE may modify Memory State but never produces a Memory Vector.
- **Explicit retrieval after learning** — A Memory Vector is generated only by a subsequent explicit READ operation; UPDATE never triggers an implicit READ.

## Interface changes

- `READ(Memory State, Query) -> Memory Vector` is explicitly non-mutating.
- `UPDATE(Memory State, Semantic Representation) -> Updated Memory State` modifies only Memory State.
- UPDATE no longer has Question, Answer, hidden state, or Memory Vector as canonical outputs.

## Generated documentation

- Chapter 2 is regenerated from canonical YAML.
- Section 10.1 is completely rewritten.
- HTML navigation and the A–Z Index are regenerated.
- Component and canonical-model references are regenerated.
