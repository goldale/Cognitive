# Research State Language Specification

## 1. Status

Version 0.1 is an executable bootstrap specification. It is intentionally smaller than the future self-hosted language.

## 2. Token syntax

A Token is case-sensitive and matches:

```ebnf
Token = "T_", PascalCaseIdentifier ;
```

Examples:

```text
T_Token
T_ModelIntegration
T_LongTermMemory
```

A Token never changes semantic identity. Refinement may narrow ambiguity or express the same meaning through a better formal composition. Semantic replacement requires a new Token. The old Token may become `T_Deprecated`.

## 3. Atomic Tokens

Only Atomic Tokens have short English natural-language definitions. Atomic Tokens are the current axioms of the language.

Every non-atomic Token is defined by an expression whose operator and arguments are Atomic Tokens declared earlier in `state/tokens.yaml`.

The language evolves primarily through composition. Reduction of the Atomic Token count without reduced expressive power is a positive maturity signal.

## 4. Entity identity

Research entities use stable identifiers such as `H_001`, `P_004`, or `A_002`. Git stores version history. Identifiers do not encode versions.

## 5. Semantic categories

The bootstrap state supports:

- `T_Principle`
- `T_Hypothesis`
- `T_ArchitectureDecision`
- `T_OpenQuestion`
- `T_RoadmapItem`
- `T_Chapter`
- `T_Section`
- `T_ConsolidationRecord`

New categories must be introduced through the same Token rules.

## 6. Natural-language boundary

Natural language remains necessary for Atomic Token definitions, hypothesis statements, evidence, falsifiers, rationale, and human documentation. The optimization direction is to reduce uncontrolled natural-language semantics inside formal definitions, not to eliminate explanatory prose from the project.
