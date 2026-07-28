# Restricted YAML Profile

Research State uses a deliberately small YAML subset.

## Allowed

- mappings with string keys;
- sequences;
- strings;
- booleans;
- finite integers and floating-point numbers;
- null.

## Prohibited

- anchors;
- aliases;
- merge keys;
- custom or explicit tags;
- duplicate mapping keys;
- binary objects;
- implicit date and time values;
- non-finite floating-point values;
- non-string mapping keys.

The profile preserves YAML readability while removing features that create parser-dependent meaning or obscure local changes.

Canonical formatting uses stable key ordering and deterministic entity ordering. Token declaration order remains semantically significant because derived Tokens may refer only to previously declared Atomic Tokens.
