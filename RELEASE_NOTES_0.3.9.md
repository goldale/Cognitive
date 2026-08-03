# Cognitive 0.3.9 Release Notes

## Documentation

- Added Section 10.6, **Associative Memory Implementation Candidates and Gaps**.
- Compared existing associative-memory, vector-search, graph, and key-value technologies with the complete Cognitive memory contract.
- Added a recommended hybrid implementation path and a precise list of missing mechanisms.
- Added **Alphabetical Index** to the same navigation row as Previous, Contents, and Next at both the top and bottom of every generated page.
- Regenerated YAML-derived HTML and Chapter 19.

## Preserved architectural invariants

- Memory Vector is produced exclusively by explicit READ.
- Answer feedback changes Associative Memory only and produces no new Memory Vector.
- Previously rejected concepts and analogies remain absent.
- Internal discussion history remains excluded from the public specification.
