# Release Notes — cognitive-0.3.47

## Architecture

- Preserves one physical Long-Term Memory with LTM-1 and LTM-2 as orthogonal logical domains.
- Introduces **Sequencer** as the canonical Input / STM component for ordering, normalization, and Logical Episode boundary proposals.
- Removes the architectural term *Episode Boundary Transformer*. Difficult boundary cases may use a lightweight Transformer only as an internal fallback implementation.
- Adds the first generated **Cognitive Master Information Lifecycle** diagram.
- Represents Offline Adaptation as a mode affecting the same Associative Memory, not as a separate subsystem.
- Uses two equal external channels: **Language / Messages** and **Stream Input**.

## Documentation and consistency

- Regenerates HTML from canonical YAML.
- Refreshes the alphabetical index and token documentation.
- Retains version numbers only in release-management artifacts.
- Verifies YAML syntax, generated-document links, identifiers, terminology, and duplicate definitions.
