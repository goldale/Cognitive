# Release Audit — cognitive-0.3.47

- Base archive: `cognitive-0.3.46-ltm-domains.tgz`
- Canonical YAML files parsed: 169
- Schema validation: passed
- Documentation generated from YAML: 181 files
- Internal HTML links checked: 2,234
- Broken links or anchors: 0
- Duplicate token IDs: 0
- Duplicate token labels: 0
- Duplicate canonical terminology entries: 0
- Duplicate HTML IDs: 0
- Obsolete terminology (`Episode Boundary Transformer`, `Information Sequencer`, `Semantic LTM`): 0
- Release-version references in architecture documentation: 0
- Exact duplicate files are limited to two intentional generated copies of source assets in `docs/`.

## Architectural changes

- `Sequencer` is the canonical Input / STM component.
- One physical LTM contains the LTM-1 and LTM-2 logical domains.
- The Master Information Lifecycle diagram is generated from canonical YAML.
- Offline adaptation is represented as a mode modifying the same Associative Memory.
