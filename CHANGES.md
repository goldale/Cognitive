# Changes

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

 - cognitive 0.3.33


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

## 0.3.35 — 2026-08-04

- Added RN-0003 on episode-specific relational-temporal reinstatement.
- Added a working offline replay hypothesis based on distributed Event States and context-compatible transitions.
- Added a conventional-hardware prototype proposal using vector search, bidirectional transition storage, and streaming context-boundary detection.
- Preserved Vector DB and graph technologies as READ-stage implementation components only.
