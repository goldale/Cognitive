# CHANGES — cognitive 0.3.17

This incremental release adds the first reference internal architecture for dynamic Associative Memory while preserving every canonical invariant established in cognitive-0.3.16.

## Added

- Dynamic reconstruction of a transient Memory Tensor with shape `1024 × 1024 × 8` (`8,388,608` scalar elements).
- Sparse Associative Index and Latent Aggregator.
- Modern Hopfield retrieval as a local attractor mechanism after scalable candidate selection.
- Tensor Reconstruction Engine for READ.
- Latent Compression Engine for validated UPDATE.
- Explicit Encoder/Decoder operational asymmetry.
- Staging Area and round-trip semantic validation.
- Reference single-server implementation guidance and benchmark policy.

## Preserved invariants

- Associative Memory never learns directly from external observations.
- The Transformer acts as Semantic Teacher; learning occurs only from Transformer-produced Semantic Representations through the Semantic Feedback Learning Pipeline.
- READ never modifies Memory State.
- UPDATE performs no implicit READ and never produces a Memory Vector.
- READ-generated or interpolated tensors cannot be written back directly.

## Documentation

The new material is canonicalized in Chapter 10, Sections 10.7–10.10 and is included in generated HTML and the A–Z Index.

## Canonical interface contracts

- `READ(Memory State, Query) → Memory Vector`
- `UPDATE(Memory State, Semantic Representation) → Updated Memory State`
