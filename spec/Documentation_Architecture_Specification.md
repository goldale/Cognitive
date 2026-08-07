# Documentation Architecture Specification

## 1. Source of truth

Generated documentation is not a source of truth. It is a human-oriented partial serialization of canonical Research State.

## 2. Language

All project artifacts are written in English. Additional natural-language editions must be generated independently from Research State rather than translated line by line from another edition.

## 3. File organization

A small chapter may be one file:

```text
chapter01.html
```

A large chapter is a directory:

```text
chapter03/
  index.html
  02_01.html
  02_02.html
```

Names are zero-padded.

## 4. Navigation

Every document contains the same navigation at the top and bottom:

- Up;
- Previous;
- Contents;
- Next.

Up moves one logical level. Contents opens the global documentation index.

## 5. Semantic HTML and CSS

HTML expresses document structure. CSS expresses presentation. Semantic classes include:

- `.token`
- `.definition`
- `.hypothesis`
- `.observation`
- `.example`
- `.note`
- `.warning`
- `.principle`
- `.formula`
- `.diagram`

The stylesheet uses a restrained ISO/RFC/W3C-inspired layout. Headings form a left axis; body text has a small additional left indent and limited line width.

## 6. Complete-document output

The complete-document typesetting target is LaTeX. When a single full-document artifact is required, the documentation generator should emit `.tex` from canonical Research State rather than treating PDF as a primary generated format.

PDF is an optional derived artifact and may be produced explicitly by compiling the generated LaTeX when requested. The English and Russian `Dynamic_Associative_Memory_Transformer_*.tex` research files are stored at the project root, outside the disposable generated `docs/` tree. They are preserved as source material for external articles and as retained research information; they are not the generated primary Cognitive documentation.

Generated full-document LaTeX is retained in Git. Its text representation keeps documentation changes diffable, mergeable, and reviewable in version history. Derived PDF output is not retained as the standard versioned documentation artifact.
