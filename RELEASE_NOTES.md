# Release Notes — cognitive-0.3.50

## Native LTM1 language and local MSG2 operations

- `MSG2` is now canonically `MSG2(amplitude, sequence_number, operation)`.
- Initial operations are `READ` and `UPDATE`; operation is interpreted locally by the receiving `LTM1` node.
- STM-node activation remains the only mechanism that emits `MSG2`.
- READ and UPDATE may coexist within one STM structure.
- Both operations excite and propagate exclusively through the persistent `LTM1` graph.
- UPDATE is match-gated: an UPDATE message requests associative matching and may reach `LTM2` only after a confirmed match.
- Transformer constructs UPDATE STM chains directly; Sequencer is not used because starts, ends, ordering, context, previous, and next are already determined.
- A dedicated architecture section defines how controlled `LTM1` activity and repeated MAX/SUM Memory Vector readouts export the native associative-atom language to Transformer.
- The export mechanism is explicitly distinguished from serialization of the complete `LTM1` state.
- Canonical YAML, terminology, contracts, invariants, HTML documentation, and index are regenerated and consistency-audited.
