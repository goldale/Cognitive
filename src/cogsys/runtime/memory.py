from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, Sequence

import numpy as np

from .world_model import ObjectiveDrivenWorldModel


@dataclass
class KnowledgeItem:
    key: str
    value: str
    features: np.ndarray
    confidence: float = 0.5
    utility: float = 0.5
    activation: float = 0.5
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dependencies: set[str] = field(default_factory=set)
    repetitions: int = 1

    @classmethod
    def create(
        cls,
        key: str,
        value: str,
        features: Sequence[float],
        confidence: float = 0.5,
        dependencies: Iterable[str] = (),
    ) -> "KnowledgeItem":
        return cls(
            key=key,
            value=value,
            features=np.asarray(features, dtype=float),
            confidence=confidence,
            dependencies=set(dependencies),
        )


@dataclass
class ConsolidationReport:
    processed: int
    promoted: int
    merged: int
    forgotten: int
    architecture_before: str
    architecture_after: str
    score_before: float
    score_after: float


class MemorySystem:
    """Working and lossy long-term memory with iterative architecture search."""

    def __init__(self, model: ObjectiveDrivenWorldModel, working_capacity: int = 32) -> None:
        self.model = model
        self.working = deque(maxlen=working_capacity)
        self.long_term: dict[str, KnowledgeItem] = {}
        self.architecture = "flat"
        self.clusters: dict[str, set[str]] = {}

    def observe(self, item: KnowledgeItem) -> None:
        item.utility = float(1.0 / (1.0 + np.exp(-self.model.objective_score(item.features))))
        item.activation = min(1.0, 0.5 * item.activation + 0.5 * item.utility)
        self.working.append(item)

    def retrieve(self, query_features: Sequence[float], limit: int = 5) -> list[KnowledgeItem]:
        query = np.asarray(query_features, dtype=float)
        candidates = list(self.long_term.values()) + list(self.working)
        scored: list[tuple[float, KnowledgeItem]] = []
        for item in candidates:
            denominator = np.linalg.norm(query) * np.linalg.norm(item.features)
            similarity = float(query @ item.features / denominator) if denominator else 0.0
            score = 0.45 * similarity + 0.3 * item.utility + 0.15 * item.confidence + 0.1 * item.activation
            scored.append((score, item))
        scored.sort(key=lambda pair: (pair[0], pair[1].key), reverse=True)
        return [item for _, item in scored[:limit]]

    def consolidate(self, forgetting_threshold: float = 0.12) -> ConsolidationReport:
        before_architecture = self.architecture
        before_score = self._architecture_score(before_architecture)
        promoted = merged = 0
        while self.working:
            item = self.working.popleft()
            existing = self.long_term.get(item.key)
            if existing and existing.value == item.value:
                total = existing.repetitions + item.repetitions
                existing.features = (existing.features * existing.repetitions + item.features * item.repetitions) / total
                existing.confidence = min(1.0, 0.7 * existing.confidence + 0.3 * item.confidence + 0.03)
                existing.utility = 0.7 * existing.utility + 0.3 * item.utility
                existing.activation = min(1.0, existing.activation + 0.1)
                existing.repetitions = total
                existing.dependencies |= item.dependencies
                merged += 1
            else:
                self.long_term[item.key] = item
                promoted += 1

        # Lossy compression: retain functional relevance rather than exact archival detail.
        forgotten = 0
        for key in list(self.long_term):
            item = self.long_term[key]
            item.activation *= 0.97
            retention = item.utility * item.confidence * (0.5 + 0.5 * item.activation)
            if retention < forgetting_threshold:
                del self.long_term[key]
                forgotten += 1

        candidate_architectures = ("flat", "clustered", "hybrid")
        current = self.architecture
        current_score = self._architecture_score(current)
        # Iterative search; only adopt a candidate that improves the functional score.
        for candidate in candidate_architectures:
            score = self._architecture_score(candidate)
            if score > current_score + 1e-9:
                current = candidate
                current_score = score
        self.architecture = current
        self._rebuild_clusters()
        return ConsolidationReport(
            processed=promoted + merged,
            promoted=promoted,
            merged=merged,
            forgotten=forgotten,
            architecture_before=before_architecture,
            architecture_after=self.architecture,
            score_before=before_score,
            score_after=current_score,
        )

    def _architecture_score(self, architecture: str) -> float:
        count = len(self.long_term)
        if count == 0:
            return 0.0
        mean_utility = float(np.mean([item.utility * item.confidence for item in self.long_term.values()]))
        dependency_density = sum(len(item.dependencies) for item in self.long_term.values()) / max(count, 1)
        if architecture == "flat":
            complexity = 0.02 * count
            retrieval_bonus = 0.25 if count < 12 else 0.0
        elif architecture == "clustered":
            complexity = 0.08 * np.sqrt(count)
            retrieval_bonus = 0.18 * min(1.0, dependency_density)
        elif architecture == "hybrid":
            complexity = 0.12 * np.log2(count + 1)
            retrieval_bonus = 0.2 * min(1.0, dependency_density) + (0.1 if count >= 10 else -0.05)
        else:
            raise ValueError(f"Unknown architecture: {architecture}")
        return mean_utility + retrieval_bonus - complexity

    def _rebuild_clusters(self) -> None:
        self.clusters.clear()
        if self.architecture == "flat":
            return
        for key, item in self.long_term.items():
            if item.dependencies:
                cluster = sorted(item.dependencies)[0]
            else:
                cluster = f"feature-{int(np.argmax(np.abs(item.features)))}"
            self.clusters.setdefault(cluster, set()).add(key)
