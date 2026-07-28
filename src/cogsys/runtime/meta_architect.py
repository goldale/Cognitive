from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

import numpy as np


class ExecutionMode(str, Enum):
    ALGORITHMIC = "algorithmic"
    NEURAL = "neural"
    HYBRID = "hybrid"


@dataclass(frozen=True)
class TaskDescriptor:
    objective_defined: float
    examples_available: float
    noise: float
    state_discrete: float
    interpretability_required: float
    safety_critical: float
    latency_pressure: float
    distribution_shift: float

    def vector(self) -> np.ndarray:
        values = np.asarray(
            [
                self.objective_defined,
                self.examples_available,
                self.noise,
                self.state_discrete,
                self.interpretability_required,
                self.safety_critical,
                self.latency_pressure,
                self.distribution_shift,
                1.0,
            ],
            dtype=float,
        )
        return np.clip(values, 0.0, 1.0)


@dataclass
class ArchitectureDecision:
    mode: ExecutionMode
    scores: dict[ExecutionMode, float]
    rationale: list[str]


class MetaArchitect:
    """Learns how to allocate tasks among algorithmic, neural, and hybrid execution."""

    def __init__(self, ridge: float = 0.5) -> None:
        self.ridge = ridge
        self.dimension = 9
        self._a = {mode: np.eye(self.dimension) * ridge for mode in ExecutionMode}
        self._b = {mode: np.zeros(self.dimension) for mode in ExecutionMode}
        # Engineering priors; online outcomes subsequently dominate them.
        self._prior = {
            ExecutionMode.ALGORITHMIC: np.asarray([1.2, -0.2, -1.0, 1.0, 0.9, 0.8, 0.4, -0.7, 0.0]),
            ExecutionMode.NEURAL: np.asarray([-0.6, 1.1, 0.9, -0.5, -0.8, -0.5, 0.0, 0.7, 0.0]),
            ExecutionMode.HYBRID: np.asarray([0.5, 0.7, 0.4, 0.5, 0.6, 0.7, -0.1, 0.5, 0.1]),
        }

    def select(self, task: TaskDescriptor, exploration: float = 0.15) -> ArchitectureDecision:
        x = task.vector()
        scores: dict[ExecutionMode, float] = {}
        for mode in ExecutionMode:
            inv = np.linalg.inv(self._a[mode])
            learned = inv @ self._b[mode]
            mean = float((learned + self._prior[mode]) @ x)
            uncertainty = float(np.sqrt(x @ inv @ x))
            scores[mode] = mean + exploration * uncertainty
        mode = max(scores, key=scores.get)
        rationale = self._rationale(task, mode)
        return ArchitectureDecision(mode=mode, scores=scores, rationale=rationale)

    def record_outcome(self, task: TaskDescriptor, mode: ExecutionMode, utility: float) -> None:
        x = task.vector()
        self._a[mode] += np.outer(x, x)
        self._b[mode] += float(utility) * x

    @staticmethod
    def _rationale(task: TaskDescriptor, mode: ExecutionMode) -> list[str]:
        reasons: list[str] = []
        if mode == ExecutionMode.ALGORITHMIC:
            if task.objective_defined > 0.7:
                reasons.append("The objective function is well defined.")
            if task.state_discrete > 0.7:
                reasons.append("The state space is predominantly discrete.")
            if task.interpretability_required > 0.7:
                reasons.append("Interpretability requirements favor explicit algorithms.")
        elif mode == ExecutionMode.NEURAL:
            if task.examples_available > 0.7:
                reasons.append("A large example library is available.")
            if task.noise > 0.6:
                reasons.append("Noisy observations favor probabilistic inference.")
            if task.objective_defined < 0.4:
                reasons.append("The objective is represented mainly by evaluated examples.")
        else:
            reasons.append("The task contains both formal and under-specified subproblems.")
            if task.safety_critical > 0.6:
                reasons.append("A deterministic safety envelope should constrain neural components.")
        return reasons or ["The decision follows the learned utility model."]

    def split_pipeline(self, stages: Mapping[str, TaskDescriptor]) -> dict[str, ArchitectureDecision]:
        return {name: self.select(task) for name, task in stages.items()}
