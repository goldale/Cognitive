from __future__ import annotations

from cogsys.runtime.demo import run_demo
from cogsys.runtime.evaluator import MultiChannelEvaluator
from cogsys.runtime.meta_architect import ExecutionMode, MetaArchitect, TaskDescriptor


def test_demo_executes() -> None:
    result = run_demo()
    assert result["communication"]["integrated"]
    assert result["evaluator"]["preferred_score"] > result["evaluator"]["rejected_score"]
    assert result["lineages"]["resilient"] is True


def test_evaluator_learns_pairwise_preference() -> None:
    evaluator = MultiChannelEvaluator({"a": 2}, hidden_size=4, seed=1)
    preferred = {"a": [1.0, 0.0]}
    rejected = {"a": [0.0, 1.0]}
    for _ in range(200):
        evaluator.train_pairwise(preferred, rejected, learning_rate=0.03)
    assert evaluator.score(preferred) > evaluator.score(rejected)


def test_meta_architect_prefers_algorithm_for_formal_discrete_task() -> None:
    architect = MetaArchitect()
    decision = architect.select(
        TaskDescriptor(
            objective_defined=1.0,
            examples_available=0.1,
            noise=0.0,
            state_discrete=1.0,
            interpretability_required=1.0,
            safety_critical=0.8,
            latency_pressure=0.5,
            distribution_shift=0.0,
        ),
        exploration=0.0,
    )
    assert decision.mode == ExecutionMode.ALGORITHMIC
