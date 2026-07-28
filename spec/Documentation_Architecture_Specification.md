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
chapter02/
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
