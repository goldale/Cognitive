# Cognitive 0.4.06

This corrective release removes the obsolete Section 2.1 diagram representation and retains one canonical Transformer-Centric Memory Architecture diagram. The diagram is stored as a standalone SVG and referenced once from Section 2.1.

This release restructures the opening documentation around the Architectural Manifesto and architectural motivation. It enlarges and redesigns the central Internal Language and asymmetric Transformer–Memory diagrams; introduces Atom S-Context (Semantic Context); and rewrites Dialogue-centered Memory Serialization.

The canonical protocol is now explicit: Transformer formulates and sends READ; Memory performs information retrieval and serialization using the current Dialogue Context from STM; READ content returns as a serialized message in the Internal Language; Transformer formulates and sends UPDATE in the Internal Language; STM updates Dialogue Context and changes Memory state.

# cognitive-0.4.06 Release Notes

## Central architectural revision

This release rebuilds Cognitive around a internal language derived from a selected intermediate representation of the trained Transformer. Associative Memory begins empty, receives no raw external semantic input, and develops as a Transformer-specific long-term model of experienced reality.

## Major changes

- Added a dedicated chapter: **Internal Language**.
- Replaced the native-LTM1-language hypothesis with one Transformer-defined language across Transformer, STM, LTM1, and LTM2.
- Reworked READ and UPDATE as Dialogue-aware phases of one cognitive cycle.
- Added **Dialogue**, **Dialogue Context**, and **Dialogue Projection** as basic concepts.
- Defined the first Dialogue exchange as memory-independent; the first UPDATE creates memory context.
- Replaced Serialized Memory Message generation with relevant-memory selection and internal-language serialization.
- Updated YAML, diagrams, terminology, invariants, and architecture decisions.
- Fully regenerated and audited the alphabetical index.
- Audited duplicate terms, sections, object IDs, and links.

- Added distinct Internal-Language Extraction Point and deeper Memory Reinjection Point; serialized memory bypasses early external-form interpretation.
- Recorded the 20–30% later reinjection depth as an experimental hypothesis rather than a fixed architectural constant.
