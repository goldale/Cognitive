# Changes

## cognitive-0.3.47 — 2026-08-05

- Renamed Episode Boundary Transformer to Sequencer and located it in the Input / STM subsystem.
- Added the master information-lifecycle diagram and explicit runtime/offline interaction path.
- Kept one physical LTM with LTM-1 and LTM-2 logical domains.
- Synchronized generated documentation and index data from YAML.

## cognitive-0.3.46 — 2026-08-05

- Canonical vertex-owned associative memory model and conservative dictionary evolution.
- Stage-1 Input Buffer and STM Sequence-lifetime corrections.
- LTM and STM added to the alphabetical index.


## cognitive-0.3.45 — 2026-08-05

- Defined logical episode start and end as semantic boundaries independent of physical Input Buffer boundaries.
- Added the specialized Episode Boundary Transformer with main-Transformer fallback for uncertain segmentation.
- Redefined Sequence as the directed linear STM reflection of the selected Input Buffer segment.
- Separated temporal Sequence topology from Transformer-defined causal episode-graph topology.
- Replaced the physical two-LTM interpretation with one physical LTM vertex and connection array.
- Defined MSG1 and MSG2 as orthogonal message-mediated processes within the same LTM.
- Added orthogonal message-specific state subspaces and concurrent independent associative retrieval waves.
- Extended MN-0001 with the cross-stream causal-dependency failure of independent parallel segmentation.
- Regenerated all YAML-derived HTML and the alphabetical index.

## cognitive-0.3.43 — 2026-08-05

- Added canonical Section 10.14 for directed episode graph storage and Connection Trace Lists.
- Defined associative search as repeated matching over lists of trace structures stored on physical connections.
- Defined one complete per-element Transformer vector stored once in each episode-graph vertex.
- Defined graph orientation as causality.
- Added Progressive Virtual Contraction and one final switch-fabric reconfiguration.
- Required Transformer-guided semantic forgetting because Trace Lists grow with distinguishable history.
- Added RS-0011 and MN-0002 without duplicating canonical definitions.
- Regenerated all documentation and the alphabetical index from canonical YAML.

## cognitive-0.3.40 — 2026-08-05

- Added the sequential multimodal Input Buffer before STM.
- Added the mutex-protected Sequential Input Multiplexer with no semantic routing.
- Added fixed eight-dimensional input-element state as a working Stage-1 dimensionality.
- Reserved one vector coordinate for Transmission Context.
- Required one-to-one permanent physical Input Buffer-to-STM projections.
- Defined implicit temporal order from sequential Input Buffer insertion.
- Added Margin Notes as a typed non-normative documentation object.
- Added MN-0001 documenting the deferred parallel input-processor pool and its causality problem.
- Regenerated human-readable HTML and the complete alphabetical index from YAML.

- Added Stage-1 STM and Semantic LTM architecture.
- Defined STM as physically fully connected, non-directed, and semantically neutral.
- Defined sequences as transient directed causal activation graphs embedded in STM.
- Added permanent physical STM-node projections to Semantic LTM inputs without addresses or lookup.
- Deferred the second LTM until consolidation from STM is specified.
- Preserved Context Selector and overlapping-trajectory documentation from the prior clean build.

## cognitive-0.3.35 — 2026-08-04

- Added topology-oriented heterogeneous Associative Memory stages.
- Added dedicated-hardware-per-topology architectural guidance.
- Added biological node-population ratios as initial hardware-sizing evidence.
- Corrected processing depth to the 4–8 layer working hypothesis.
- Added reproducible 0.5 diagram scaling for Sections 12.6 and 13.1.
- Corrected and uniformly formatted the Section 14.1 comparison table.

## cognitive-0.3.33 — 2026-08-04

- Corrected every generated **A–Z Index** navigation target.
- Removed the obsolete hard-coded `chapter24/index.html` default from the navigation generator.
- Made `index_href` an explicit generator input derived from the current alphabetical-index chapter order.
- Added semantic documentation validation requiring every `a.alphabetical-index` link to resolve to the canonical A–Z Index page.
- Added a regression test preventing recurrence when chapter ordering changes.
- Preserved the canonical operations `READ(Memory State, Query)` and `UPDATE(Memory State, Semantic Representation)` without architectural changes.



## Associative Memory READ/UPDATE integration diagram

- Added a canonical explanatory diagram for the hybrid Associative Memory implementation.
- Clarified that GraphRAG components operate inside READ and do not directly define Memory State.
- Documented spreading activation, Dynamic Memory State, explicit Memory Vector projection, Integrated Evaluation placement, and the separate UPDATE-only modification path.
- Added the diagram source as a release asset and included it in modular HTML and PDF documentation.

- Clarified that vector search and embeddings are candidate-retrieval accelerators, not a complete Associative Memory.
- Required explicit typed graph relations for dependency, blocking, enabling, temporal structure, and causal hypotheses.
- Clarified that a labelled graph edge is not proof of causality and requires provenance, confidence, and supporting evidence.
- Defined the initial memory implementation as a hybrid of vector retrieval, graph relations, exact storage, dynamic associative activation, and explicit READ projection.
- Preserved strict READ/UPDATE separation and Transformer-mediated memory learning.
- Replaced the earlier multiplicative priority ratio as a canonical decision rule.
- Added admissibility gates for catastrophic, prohibited, unauthorized, or insufficiently reversible actions before ranking.
- Added normalized multi-criteria estimation with explicit residual risk, effective cost, delay cost, and temporally discounted future options.
- Clarified that action scores are inputs to Integrated Evaluation rather than autonomous decisions.
- Recorded unresolved weighting, normalization, causal-confidence, discounting, and planning-horizon choices as open questions requiring experiments.

## Canonical terminology retained

- Semantic Teacher remains the Transformer role that produces Semantic Representation.
- Semantic Feedback Learning Pipeline remains the validated path carrying Semantic Representation to UPDATE.


- Added RN-0003 on episode-specific relational-temporal reinstatement.
- Added a working offline replay hypothesis based on distributed Event States and context-compatible transitions.
- Added a conventional-hardware prototype proposal using vector search, bidirectional transition storage, and streaming context-boundary detection.
- Preserved Vector DB and graph technologies as READ-stage implementation components only.
