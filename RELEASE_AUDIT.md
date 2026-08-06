# Release Audit — cognitive-0.4.14

- release: 0.4.14
- date: 2026-08-05
- schema_validation: passed
- tests: 52 passed
- documentation_generation: passed
- canonical_naming: passed
- MSG2_contract: MSG2(amplitude, sequence_number, operation)
- operations: ['READ', 'UPDATE']
- exact_long_text_duplicates: 5

## Consistency checks

- No global STM READ/UPDATE mode in canonical contracts
- STM-node activation is sole MSG2 emission mechanism
- READ and UPDATE propagate exclusively through LTM1
- UPDATE is gated by confirmed associative match
- Sequencer excluded from Transformer-constructed UPDATE chains
- Native LTM1 language export distinguished from full LTM1 serialization

## Exact long-text duplicate audit

Found **5** exact repeated long text blocks. These are listed in `RELEASE_AUDIT.json` for review; no conflicting duplicate MSG2 contracts remain.
