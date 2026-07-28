from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

import numpy as np


@dataclass
class WorldFact:
    key: str
    value: str
    features: np.ndarray
    confidence: float = 0.5
    importance: float = 0.5
    source: str = "observation"
    dependencies: set[str] = field(default_factory=set)


class ObjectiveDrivenWorldModel:
    """Finite world model whose organization is explicitly objective-dependent."""

    def __init__(self, objective_names: Sequence[str], objective_weights: Sequence[float]) -> None:
        if len(objective_names) != len(objective_weights) or not objective_names:
            raise ValueError("Objective names and weights must have equal non-zero length")
        self.objective_names = tuple(objective_names)
        self.objective_weights = np.asarray(objective_weights, dtype=float)
        self.facts: dict[str, WorldFact] = {}
        self.revision = 0

    def objective_score(self, features: Sequence[float]) -> float:
        vector = np.asarray(features, dtype=float)
        if vector.shape != self.objective_weights.shape:
            raise ValueError(f"Feature vector must have shape {self.objective_weights.shape}")
        norm = np.linalg.norm(self.objective_weights)
        if norm == 0:
            return 0.0
        return float(self.objective_weights @ vector / norm)

    def upsert_fact(
        self,
        key: str,
        value: str,
        features: Sequence[float],
        confidence: float = 0.5,
        source: str = "observation",
        dependencies: set[str] | None = None,
    ) -> WorldFact:
        vector = np.asarray(features, dtype=float)
        score = self.objective_score(vector)
        importance = float(1.0 / (1.0 + np.exp(-score)))
        fact = WorldFact(
            key=key,
            value=value,
            features=vector,
            confidence=float(np.clip(confidence, 0.0, 1.0)),
            importance=importance,
            source=source,
            dependencies=set(dependencies or ()),
        )
        self.facts[key] = fact
        self.revision += 1
        return fact

    def update_objectives(self, objective_weights: Sequence[float]) -> None:
        vector = np.asarray(objective_weights, dtype=float)
        if vector.shape != self.objective_weights.shape:
            raise ValueError(f"Objective vector must have shape {self.objective_weights.shape}")
        self.objective_weights = vector
        for fact in self.facts.values():
            score = self.objective_score(fact.features)
            fact.importance = float(1.0 / (1.0 + np.exp(-score)))
        self.revision += 1

    def ranked_facts(self) -> list[WorldFact]:
        return sorted(
            self.facts.values(),
            key=lambda fact: (fact.importance * fact.confidence, fact.key),
            reverse=True,
        )

    def fingerprint(self) -> dict[str, float]:
        return {fact.key: round(fact.importance * fact.confidence, 6) for fact in self.ranked_facts()}

    def overlap(self, other: "ObjectiveDrivenWorldModel") -> float:
        keys = set(self.facts) | set(other.facts)
        if not keys:
            return 1.0
        common = 0.0
        total = 0.0
        for key in keys:
            left = self.facts.get(key)
            right = other.facts.get(key)
            left_weight = left.importance * left.confidence if left else 0.0
            right_weight = right.importance * right.confidence if right else 0.0
            common += min(left_weight, right_weight)
            total += max(left_weight, right_weight)
        return common / total if total else 1.0
