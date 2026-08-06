# cognitive-0.4.01 Release Notes

## Central architectural revision

This release rebuilds Cognitive around a shared internal language derived from a selected intermediate representation of the trained Transformer. Associative Memory begins empty, receives no raw external semantic input, and develops as a Transformer-specific long-term model of experienced reality.

## Major changes

- Added a dedicated chapter: **Shared Internal Language**.
- Replaced the native-LTM1-language hypothesis with one Transformer-defined language across Transformer, STM, LTM1, and LTM2.
- Reworked READ and UPDATE as Dialogue-aware phases of one cognitive cycle.
- Added **Dialogue**, **Dialogue Context**, and **Dialogue Projection** as basic concepts.
- Defined the first Dialogue exchange as memory-independent; the first UPDATE creates memory context.
- Replaced Memory Vector generation with relevant-memory selection and internal-language serialization.
- Updated YAML, diagrams, terminology, invariants, and architecture decisions.
- Fully regenerated and audited the alphabetical index.
- Audited duplicate terms, sections, object IDs, and links.

- Added distinct Internal-Language Extraction Point and deeper Memory Reinjection Point; serialized memory bypasses early external-form interpretation.
- Recorded the 20–30% later reinjection depth as an experimental hypothesis rather than a fixed architectural constant.
