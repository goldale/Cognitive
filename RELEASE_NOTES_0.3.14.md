# Cognitive 0.3.14 Release Notes

This patch release restores previously discussed examples and corrects the high-level memory feedback diagram while reducing duplicated explanation across the specification.

## Restored examples

- Section 3.3: repeated reading of the same book, including rereading it many years later.
- Section 3.4: the hypothesis that emotion-like dynamics may emerge through persistent group interaction.
- Section 3.5: the shared-context phrase “We will meet as usual.”
- Section 6.5: failure to act may allow the system carrier to cease to exist.
- Section 8.1: bounded planning illustrated by choosing a chess move.

## Memory architecture correction

Section 9.1 now shows Transformer output returning to Memory State as an internal observation. This feedback changes memory state only and does not invoke Projection or generate a new Memory Vector. Memory Vectors remain exclusive products of explicit READ operations.

## Deduplication

Exact repeated explanatory blocks were removed. Detailed treatment remains in the most appropriate chapter, while related chapters now use concise cross-references.
