# Architecture Freeze — Cognitive 0.3.15

**Status:** FROZEN FOR DOCUMENTATION REFACTORING  
**Date:** 2026-08-03  
**Baseline:** Cognitive canonical architecture

## Fundamental change

The Transformer is both the Semantic Reasoning Engine and the Semantic Teacher of Associative Memory. Associative Memory learns from Transformer-produced Semantic Representations rather than raw external observations. The complete self-learning cycle is represented by the first-class **Semantic Feedback Learning Pipeline**.

## Frozen contracts

```text
READ(Memory State, Query) -> Memory Vector
UPDATE(Memory State, Semantic Representation) -> Updated Memory State
```

UPDATE modifies only Memory State. UPDATE never returns a Memory Vector and never performs an implicit READ. A new Memory Vector can be produced only by a later explicit READ.

## Canonical files

- `state/canonical/principles.yaml`
- `state/canonical/components.yaml`
- `state/canonical/contracts.yaml`
- `state/canonical/invariants.yaml`
- `state/canonical/terminology.yaml`
- `state/canonical/ownership.yaml`
- `state/canonical/generation.yaml`

## Generation boundary

Canonical YAML is edited directly. HTML, Chapter 2 renderings, CHANGES.md, diagrams, and the A–Z Index are derived artifacts and must be regenerated.

## Release gate

Any later artifact that contradicts an invariant in `state/canonical/invariants.yaml` is release-blocking.
