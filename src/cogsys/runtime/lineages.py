from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, Iterable, Protocol, TypeVar

import numpy as np


class Evolvable(Protocol):
    fitness: float
    signature: np.ndarray


T = TypeVar("T", bound=Evolvable)


@dataclass
class CognitiveLineage(Generic[T]):
    lineage_id: str
    members: list[T] = field(default_factory=list)

    def champion(self) -> T:
        if not self.members:
            raise ValueError(f"Lineage {self.lineage_id} has no members")
        return max(self.members, key=lambda member: member.fitness)


class CognitiveLineageManager(Generic[T]):
    """Clones champions within diverse lineages rather than globally homogenizing a population."""

    def __init__(self, minimum_lineages: int = 3) -> None:
        self.minimum_lineages = minimum_lineages
        self.lineages: dict[str, CognitiveLineage[T]] = {}

    def add_lineage(self, lineage_id: str, members: Iterable[T]) -> None:
        values = list(members)
        if not values:
            raise ValueError("A lineage must contain at least one member")
        self.lineages[lineage_id] = CognitiveLineage(lineage_id, values)

    def clone_champions(self, target_size_per_lineage: int) -> dict[str, list[T]]:
        result: dict[str, list[T]] = {}
        for lineage_id, lineage in self.lineages.items():
            champion = lineage.champion()
            result[lineage_id] = [deepcopy(champion) for _ in range(target_size_per_lineage)]
        return result

    def diversity(self) -> float:
        champions = [lineage.champion() for lineage in self.lineages.values()]
        if len(champions) < 2:
            return 0.0
        distances = []
        for left_index, left in enumerate(champions):
            for right in champions[left_index + 1 :]:
                distances.append(float(np.linalg.norm(left.signature - right.signature)))
        return float(np.mean(distances))

    def population_is_resilient(self, minimum_diversity: float) -> bool:
        return len(self.lineages) >= self.minimum_lineages and self.diversity() >= minimum_diversity
