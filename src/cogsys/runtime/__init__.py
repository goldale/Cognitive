"""Executable research prototypes for long-lived cognitive systems."""

from .communication import CommunicationEngine, IntegrationResult
from .evaluator import MultiChannelEvaluator
from .lineages import CognitiveLineageManager
from .memory import KnowledgeItem, MemorySystem
from .meta_architect import ExecutionMode, MetaArchitect, TaskDescriptor
from .world_model import ObjectiveDrivenWorldModel

__all__ = [
    "CommunicationEngine",
    "IntegrationResult",
    "MultiChannelEvaluator",
    "CognitiveLineageManager",
    "KnowledgeItem",
    "MemorySystem",
    "ExecutionMode",
    "MetaArchitect",
    "TaskDescriptor",
    "ObjectiveDrivenWorldModel",
]
