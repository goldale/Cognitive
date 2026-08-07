# Cognitive 0.5.09 — Second Edition Editorial Rewrite (Incremental Build)

This archive contains the completed Second Edition rewrite of the opening chapter, **Project Goal**. The chapter is generated from YAML as a continuous narrative without a numbered subsection heading. Its first figure is the conceptual Cognitive Architecture diagram: Transformer THINKS, Associative Memory REMEMBERS, connected through a Shared Internal Language.

All remaining chapters are inherited from the 0.5.01 baseline and will be reorganized in subsequent editorial steps.

# Cognitive 0.5.09 — Idea-First Documentation

## Primary objective

A technically competent new reader should understand the central architectural innovation within the first ten pages.

## Major changes

- Reorganized the opening documentation around the latent Transformer–Associative Memory interface.
- Removed the obsolete standalone sequencing component without replacement.
- Recast Reasoning, Planning, Temporal Organization, Semantic Representation, and Integrated Evaluation as cognitive functions rather than independent physical modules.
- Adopted **LTM1 Associative Vector Codebook** as the preferred Draft 05 name, with exact mechanics explicitly marked for discussion.
- Presented a dual-width Layer N READ/UPDATE interface as a research proposal under RS-0011, not as a frozen implementation.
- Clarified that READ and UPDATE are native latent interactions, not textual, JSON, RPC, or network messages.

# Cognitive 0.5.09

## Diagram generator

The generator now wraps labels before Graphviz layout, automatically recomposes over-wide diagrams without splitting them, and assigns landscape page orientation only to exceptional cases that remain wider than the portrait limit. Post-layout font scaling is prohibited.

This corrective release adds figure numbers directly to the visible title of every diagram and imported figure. The same number and title are used in the global List of Figures.

## 0.5.09 editorial cleanup

- Removed obsolete Input Buffer terminology from the canonical model and generated documentation.
- Removed obsolete standalone sequencing terminology from the documentation.
- Removed obsolete dedicated episode-boundary mechanism terminology.
- Added red ARCHITECTURAL DECISION REQUIRED markers where removal leaves an unresolved architectural responsibility.
- Added Russian and English Dynamic Associative Memory Transformer LaTeX research documents under `docs/`.
