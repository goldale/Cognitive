# Semantic Consolidation Protocol

## 1. Responsibility split

Git stores file history, branches, rollback points, and transport. Research State stores the current consolidated model. The latest `T_ConsolidationRecord` explains the semantic transition that created the current version.

## 2. Latest-record rule

Each Research State version stores only the latest consolidation record. It does not accumulate all prior records. Earlier consolidation records remain available in earlier Git commits.

When a commit contains no semantic change, `consolidation.yaml` may remain unchanged.

## 3. Required record fields

A semantic consolidation record identifies:

- the transition identifier;
- timestamp;
- summary;
- input sources;
- changed Research State roles;
- alternatives considered;
- rationale;
- remaining open questions.

## 4. Branch consolidation

A semantic consolidation is not equivalent to Git merge. It may:

- accept one branch;
- combine independent changes;
- reject both conflicting formulations;
- create a third model;
- reduce confidence rather than selecting one claim;
- preserve explicit unresolved alternatives.

The deterministic merge tool resolves structural non-conflicts and emits a conflict report. Human-model review produces the actual semantic consolidation.
