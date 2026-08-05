# Release Notes — cognitive-0.3.48

## LTM-2 READ and Memory Vector generation

- Defines the complete Stage-1 algorithm that generates the Memory Vector from the latest sequenced STM event.
- The Sequencer assigns a position number to every node in the linear STM Sequence.
- Every Sequence node emits `msg2(amplitude, sequence_number)` through its permanent projection to the corresponding LTM input node.
- Every `msg2` propagates exclusively through the persistent associative graph stored in LTM-1. READ creates no temporary associative connections.
- LTM-2 has no independent propagation graph or propagation logic; it uses the LTM-1 associative structure as its computational substrate while maintaining an orthogonal MSG2-specific state subspace.
- The resulting distributed response is reduced to the fixed-dimensional Memory Vector through a configurable readout operator.
- The initial implementation compares MAX and SUM readout operators under identical conditions.
- For deterministic READ, the operator producing the higher non-degenerate Memory Vector entropy over representative memory states and events is preferred. For stochastic READ, mutual information is required to distinguish signal entropy from noise.

## Master Architecture Diagram

- Updates the canonical Master Architecture Diagram YAML and verifies its internal consistency.
- Generates an A3 PDF because PDF generation was explicitly requested.
- Does not regenerate PNG or SVG visualizations.

## Release quality

- Audits duplicate files, YAML identifiers, index entries, repeated definitions, and conflicting architectural rules.
- Preserves one physical LTM with LTM-1 and LTM-2 as orthogonal logical domains.
