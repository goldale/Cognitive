# Release Notes - cognitive-0.3.20

## Scope

This release refines the canonical semantic-coordinate optimization model while preserving all stable Cognitive Architecture invariants from cognitive-0.3.19.

## Changes

- Replaced Section 11.5 with **Self-Organizing Semantic Coordinate System**.
- Retained a one-time global basis initialization after Memory State stabilization.
- Added continuous localized basis maintenance driven by the maintained correlation matrix.
- Each refinement selects the strongest-correlated semantic pair and uses the remaining axis having the weakest statistical correlation with that pair as the reference rotation axis.
- Each refinement modifies exactly two semantic-vector elements; all other coordinates remain unchanged.
- Clarified that basis optimization belongs exclusively to Offline Consolidation (Sleep), minimizing Transformer adaptation and preserving semantic continuity.
- Regenerated HTML, PDF, cross-references, and the A-Z Index from canonical YAML.
