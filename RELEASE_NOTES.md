# Release Notes — cognitive-0.3.43

Release date: **2026-08-05**.

## Directed episode graph storage

- Added the canonical working architecture for storing logically completed directed episode graphs.
- Defined one Transformer-produced contextual data vector for every episode element.
- Required the full vector to be stored exactly once in its episode-graph vertex.
- Defined graph orientation as causality rather than physical connection or signal direction.

## Associative search on connections

- Defined a Trace List on every participating physical LTM connection.
- Defined associative retrieval as repeated matching over connection-local Trace Lists followed by one local transition.
- Excluded global graph lookup, episode IDs, cognitive addresses, stored routes, and special initial search state from the minimal trace contract.
- Added Progressive Virtual Contraction with one final switch-fabric reconfiguration only after the target is reached.

## Scale and forgetting

- Recorded large Trace Lists as the expected cost of exact distinguishable associative history.
- Required Transformer participation in semantic forgetting, consolidation, and destructive deletion.
- Added MN-0002 for deferred compressed or superposed Trace storage.

## Documentation quality

- Added Section 10.14 as the single canonical owner of these decisions.
- Added RS-0011 as a non-duplicating research record.
- Removed duplicate normative formulations and regenerated YAML-derived HTML and the alphabetical index.
