# Chapter 2 — Architecture Overview and Design Principles

## 2.1 Canonical Architecture Overview

The Transformer is both the **Semantic Reasoning Engine** and the **Semantic Teacher** of Associative Memory.

```text
External Input -> READ -> Memory Vector -> Transformer
                                  |
                                  v
                      Semantic Representation
                                  |
                                  v
                               UPDATE
                                  |
                                  v
                            Memory State
```

## Canonical operation contracts

| Operation | Inputs | Output | State effect |
|---|---|---|---|
| READ | Memory State, Query | Memory Vector | None |
| UPDATE | Memory State, Semantic Representation | Updated Memory State | Modifies only Memory State |

> UPDATE never produces a Memory Vector. A new Memory Vector is generated only by a subsequent explicit READ.
