from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


@dataclass
class TrainingResult:
    loss: float
    positive_score: float
    negative_score: float


class MultiChannelEvaluator:
    """Small trainable network mapping heterogeneous channels to one scalar evaluation.

    It is intentionally framework-free. Pairwise preference examples provide the initial
    and lifelong training signal proposed in the architecture document.
    """

    def __init__(
        self,
        channel_sizes: Mapping[str, int],
        hidden_size: int = 16,
        seed: int = 7,
    ) -> None:
        if not channel_sizes:
            raise ValueError("At least one input channel is required")
        if any(size <= 0 for size in channel_sizes.values()):
            raise ValueError("Every channel size must be positive")
        self.channel_sizes = dict(channel_sizes)
        self.channel_names = tuple(sorted(self.channel_sizes))
        input_size = sum(self.channel_sizes.values())
        rng = np.random.default_rng(seed)
        self.w1 = rng.normal(0.0, 1.0 / np.sqrt(input_size), (hidden_size, input_size))
        self.b1 = np.zeros(hidden_size)
        self.w2 = rng.normal(0.0, 1.0 / np.sqrt(hidden_size), hidden_size)
        self.b2 = 0.0

    def encode(self, channels: Mapping[str, Sequence[float]]) -> np.ndarray:
        vectors: list[np.ndarray] = []
        for name in self.channel_names:
            if name not in channels:
                raise ValueError(f"Missing evaluator channel: {name}")
            vector = np.asarray(channels[name], dtype=float)
            expected = self.channel_sizes[name]
            if vector.shape != (expected,):
                raise ValueError(f"Channel {name} must have shape ({expected},), got {vector.shape}")
            vectors.append(vector)
        return np.concatenate(vectors)

    def _forward_vector(self, x: np.ndarray) -> tuple[float, np.ndarray]:
        hidden = np.tanh(self.w1 @ x + self.b1)
        score = float(self.w2 @ hidden + self.b2)
        return score, hidden

    def score(self, channels: Mapping[str, Sequence[float]]) -> float:
        score, _ = self._forward_vector(self.encode(channels))
        return score

    def train_pairwise(
        self,
        preferred: Mapping[str, Sequence[float]],
        rejected: Mapping[str, Sequence[float]],
        learning_rate: float = 0.01,
    ) -> TrainingResult:
        """Train with logistic pairwise ranking loss: -log(sigmoid(s+ - s-))."""
        xp = self.encode(preferred)
        xn = self.encode(rejected)
        sp, hp = self._forward_vector(xp)
        sn, hn = self._forward_vector(xn)
        delta = np.clip(sp - sn, -60.0, 60.0)
        sigmoid = 1.0 / (1.0 + np.exp(-delta))
        loss = float(-np.log(max(sigmoid, 1e-12)))
        gradient_delta = sigmoid - 1.0

        old_w2 = self.w2.copy()
        grad_w2 = gradient_delta * (hp - hn)
        grad_b2 = 0.0  # Cancels in a pairwise difference.
        grad_hp = gradient_delta * old_w2
        grad_hn = -gradient_delta * old_w2
        grad_zp = grad_hp * (1.0 - hp * hp)
        grad_zn = grad_hn * (1.0 - hn * hn)
        grad_w1 = np.outer(grad_zp, xp) + np.outer(grad_zn, xn)
        grad_b1 = grad_zp + grad_zn

        self.w2 -= learning_rate * grad_w2
        self.b2 -= learning_rate * grad_b2
        self.w1 -= learning_rate * grad_w1
        self.b1 -= learning_rate * grad_b1
        return TrainingResult(loss=loss, positive_score=sp, negative_score=sn)

    def state_dict(self) -> dict[str, object]:
        return {
            "channel_sizes": self.channel_sizes,
            "w1": self.w1.tolist(),
            "b1": self.b1.tolist(),
            "w2": self.w2.tolist(),
            "b2": self.b2,
        }

    @classmethod
    def from_state_dict(cls, state: Mapping[str, object]) -> "MultiChannelEvaluator":
        channel_sizes = state["channel_sizes"]
        if not isinstance(channel_sizes, Mapping):
            raise ValueError("Invalid evaluator state")
        w1 = np.asarray(state["w1"], dtype=float)
        instance = cls({str(k): int(v) for k, v in channel_sizes.items()}, hidden_size=w1.shape[0])
        instance.w1 = w1
        instance.b1 = np.asarray(state["b1"], dtype=float)
        instance.w2 = np.asarray(state["w2"], dtype=float)
        instance.b2 = float(state["b2"])
        return instance
