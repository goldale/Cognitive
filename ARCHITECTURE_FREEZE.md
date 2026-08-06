# Architecture Freeze — cognitive-0.5.05

The canonical source is the Master Architecture YAML and canonical state files.

Release-blocking points:

- `MSG2(amplitude, activation_position, operation)` carries local `READ` or `UPDATE`.
- Only STM-node activation emits `MSG2`.
- All MSG2 excitation propagates exclusively through the persistent `LTM1` graph.
- UPDATE writes to `LTM2` only after confirmed associative match.
- Controlled LTM1 selection plus repeated MAX/SUM Serialized Memory Message readout exports LTM1 associative atoms as the native language consumed by Transformer.
- Native-language export is not defined as serialization of all LTM1.
