from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .communication import CommunicationEngine
from .evaluator import MultiChannelEvaluator
from .lineages import CognitiveLineageManager
from .memory import KnowledgeItem, MemorySystem
from .meta_architect import MetaArchitect, TaskDescriptor
from .world_model import ObjectiveDrivenWorldModel


@dataclass
class DemoAgent:
    name: str
    fitness: float
    signature: np.ndarray


def run_demo() -> dict[str, object]:
    scientist = ObjectiveDrivenWorldModel(
        ["prediction", "survival", "beauty"],
        [1.0, 0.2, 0.1],
    )
    predator = ObjectiveDrivenWorldModel(
        ["prediction", "survival", "beauty"],
        [0.2, 1.0, 0.0],
    )
    scientist.upsert_fact("forest.temperature", "mild", [0.9, 0.2, 0.1], 0.9)
    scientist.upsert_fact("forest.prey", "deer", [0.3, 0.9, 0.0], 0.8, dependencies={"forest.temperature"})
    predator.upsert_fact("forest.temperature", "mild", [0.9, 0.2, 0.1], 0.7)

    memory = MemorySystem(predator)
    channel = CommunicationEngine()
    packet = channel.partial_serialize(scientist, predator, "share forest model")
    result = channel.integrate(packet, predator, memory)
    consolidation = memory.consolidate()

    evaluator = MultiChannelEvaluator({"sensory": 3, "social": 2}, hidden_size=8)
    preferred = {"sensory": [1.0, 0.5, 0.2], "social": [0.8, 0.2]}
    rejected = {"sensory": [0.1, 0.1, 0.7], "social": [0.0, 0.1]}
    training = None
    for _ in range(100):
        training = evaluator.train_pairwise(preferred, rejected, learning_rate=0.03)

    meta = MetaArchitect()
    decision = meta.select(
        TaskDescriptor(
            objective_defined=0.6,
            examples_available=0.9,
            noise=0.7,
            state_discrete=0.4,
            interpretability_required=0.8,
            safety_critical=0.9,
            latency_pressure=0.5,
            distribution_shift=0.6,
        )
    )

    lineages = CognitiveLineageManager[DemoAgent](minimum_lineages=3)
    lineages.add_lineage("scientific", [DemoAgent("s1", 0.9, np.asarray([1.0, 0.2, 0.1]))])
    lineages.add_lineage("predatory", [DemoAgent("p1", 0.85, np.asarray([0.2, 1.0, 0.0]))])
    lineages.add_lineage("artistic", [DemoAgent("a1", 0.8, np.asarray([0.2, 0.1, 1.0]))])

    return {
        "communication": {
            "integrated": result.integrated,
            "clarifications": [request.__dict__ for request in result.clarifications],
            "conflicts": [conflict.__dict__ for conflict in result.conflicts],
        },
        "consolidation": consolidation.__dict__,
        "evaluator": {
            "preferred_score": evaluator.score(preferred),
            "rejected_score": evaluator.score(rejected),
            "final_loss": training.loss if training else None,
        },
        "meta_architect": {
            "mode": decision.mode.value,
            "scores": {mode.value: score for mode, score in decision.scores.items()},
            "rationale": decision.rationale,
        },
        "lineages": {
            "count": len(lineages.lineages),
            "diversity": lineages.diversity(),
            "resilient": lineages.population_is_resilient(0.5),
        },
    }


def main() -> int:
    import json

    print(json.dumps(run_demo(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
