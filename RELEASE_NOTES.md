# Release Notes - cognitive-0.3.32


## Associative Memory READ/UPDATE integration diagram

- Added a canonical explanatory diagram for the hybrid Associative Memory implementation.
- Clarified that GraphRAG components operate inside READ and do not directly define Memory State.
- Documented spreading activation, Dynamic Memory State, explicit Memory Vector projection, Integrated Evaluation placement, and the separate UPDATE-only modification path.
- Added the diagram source as a release asset and included it in modular HTML and PDF documentation.

## Scope

This release refines the practical implementation model for Associative Memory and corrects the action-priority heuristic. Clear architectural conclusions are canonicalized; unresolved implementation choices are explicitly recorded as discussion items requiring experimental evidence.

## Accepted changes

- Vector retrieval remains a fast semantic candidate-search mechanism but is not sufficient as Associative Memory.
- Typed graph relations complement vector similarity with explicit dependency, blocking, enabling, temporal, and causal-hypothesis structure.
- Associative READ integrates vector candidates, graph evidence, exact content, and transient activation before producing a Memory Vector.
- Graph labels do not establish causality without provenance and supporting evidence.
- The earlier ratio `PracticalUtility x FutureOptionValue / (Cost x Risk x Irreversibility)` is no longer a canonical decision rule.
- Action selection now uses admissibility constraints, normalized estimates, bounded planning, and final Integrated Evaluation.
- Catastrophic or prohibited risk is handled as a hard gate; residual risk remains part of comparison among admissible alternatives.
- Future-option estimates must be temporally attributed and bounded by the Planning Budget.

## Recorded open questions

- Relative weighting of vector similarity, graph evidence, and dynamic activation.
- Representation and validation of causal confidence.
- Preferred normalization and aggregation method for heterogeneous action estimates.
- Temporal discount function and objective-class dependence.
- Minimum practical-utility threshold and context-switching cost model.
- Context-dependent maximum planning horizon.

## Compatibility

The canonical learning loop, explicit READ/UPDATE asymmetry, Transformer-mediated learning, fixed runtime semantic dimensionality, YAML Single Source of Truth, and modular documentation policy remain unchanged.
