# Architecture Freeze — cognitive-0.4.14

The canonical source is the Master Architecture YAML and canonical state files.

Release-blocking points:

- `MSG2(amplitude, sequence_number, operation)` carries local `READ` or `UPDATE`.
- Only STM-node activation emits `MSG2`.
- All MSG2 excitation propagates exclusively through the persistent `LTM1` graph.
- UPDATE writes to `LTM2` only after confirmed associative match.
- Transformer directly constructs UPDATE STM chains; Sequencer is not invoked.
- Controlled LTM1 selection plus repeated MAX/SUM Serialized Memory Message readout exports LTM1 associative atoms as the native language consumed by Transformer.
- Native-language export is not defined as serialization of all LTM1.
