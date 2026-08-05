# Release Notes — cognitive-0.3.46

## Canonical changes

- Removed the separate Sequential Multiplexer from the Stage-1 input path. The Linear / Circular Input Buffer is the mutex-protected queue.
- Defined Sequence lifetime through successful commit to LTM-2 and advancement of the circular-buffer beginning.
- Introduced the canonical vertex model: Concept Identity, owned Bounded Edge List with Local Edge Search, and owned Usage Statistics.
- Defined sleep-time Edge List maintenance as the primary mechanism for restoring free memory capacity.
- Added conservative Associative Dictionary evolution through Concept Differentiation and Concept Generalization.
- Required long-accumulated statistics across many Logical Episodes and multiple sleep cycles before dictionary modification.
- Added explicit alphabetical-index entries for LTM and STM.
- Checked canonical source and generated documentation for duplicate and conflicting definitions.
