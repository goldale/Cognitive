# Chapter 2 — Transformer-Centric Architecture

The trained Transformer defines the shared internal language at a selected intermediate representation. Associative Memory begins empty and develops specifically for that Transformer.

```text
External Input -> Transformer Internal Language -> STM -> READ/UPDATE -> LTM1/LTM2
                                             ^                         |
                                             |--- serialized relevance-|
```

## Dialogue-aware cycle

- First exchange: no READ; UPDATE creates Dialogue Context.
- Continuing exchange: READ returns previous Dialogue content plus its projection onto long-term memory.
- UPDATE stores the new internal state produced during Transformer processing.

Memory does not generate a separate Memory Vector language. It selects relevant information and serializes it in the shared internal language.
