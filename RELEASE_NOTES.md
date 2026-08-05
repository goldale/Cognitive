# Release Notes — cognitive-0.3.45

Release date: **2026-08-05**.

## Logical Episode boundaries

- Added semantic start and end boundaries independent of physical Input Buffer boundaries.
- Added a specialized Episode Boundary Transformer with delegation to the main Transformer when confidence is insufficient.
- Separated repeated boundary detection from final whole-episode Transformer processing.

## Sequence and causal graph

- Redefined Sequence as a directed linear STM activation graph directly reflecting the selected Input Buffer segment.
- Required Sequence direction to preserve temporal order rather than causality.
- Defined the completed Sequence as selecting episode vertices while the main Transformer determines the possibly branched causal graph topology.

## One physical LTM and two message types

- Defined one physical LTM array of interacting vertices and connections.
- Added MSG1 for element-semantic processing and MSG2 for completed-episode graph integration.
- Partitioned vertex and connection state into orthogonal message-specific subspaces.
- Allowed independent MSG1 and MSG2 associative retrieval waves to operate concurrently in the same physical LTM.

## MN-0001

- Added cross-stream causal dependencies as a primary failure mode of independent parallel input segmentation.

## Documentation

- Updated canonical YAML, regenerated modular HTML, and rebuilt the alphabetical index.
