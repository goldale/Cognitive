# Release Notes — cognitive-0.3.40

Release date: **2026-08-05**.

## Sequential multimodal Input Buffer

- Added a modality-neutral Input Buffer between input sources and STM.
- Defined a simple sequential multiplexer as a mutex-protected queue with no semantic routing, prioritization, lookup, or destination selection.
- Defined linear or circular filling: the next available event is written into the next Input Buffer element.
- Defined each Input Buffer element as a fixed-dimensional activation vector; the Stage-1 working dimensionality is eight.
- Reserved one coordinate for Transmission Context, initially preserving signal source or transmission mode without encoding Item identity.
- Required equality between Input Buffer element count and STM node count, and equality of their per-element runtime vector dimensionality.
- Added one permanent physical projection from every Input Buffer element to its corresponding STM node.
- Defined Input Buffer insertion order as implicit system-observed time and clarified that order alone is not proof of external causality.

## Margin Notes

- Added Margin Notes as an official non-normative documentation object.
- Added **MN-0001 — Alternative parallel input processing**.
- Recorded the processor-pool alternative as deferred because parallel completion can invert observation order and damage the Stage-1 causal interpretation.
- Added Margin Notes to generated HTML and the alphabetical index.

## Architectural status

This release extends the working Stage-1 hypothesis. The Input Buffer mechanism is canonical for this release; the parallel processor-pool alternative remains explicitly non-canonical. READ/UPDATE separation and all prior baseline invariants remain in force.
