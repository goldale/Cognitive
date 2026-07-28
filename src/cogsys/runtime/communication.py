from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .memory import KnowledgeItem, MemorySystem
from .world_model import ObjectiveDrivenWorldModel


@dataclass
class SerializedFact:
    key: str
    value: str
    features: list[float]
    confidence: float
    dependencies: list[str]


@dataclass
class SerializedPacket:
    sender_revision: int
    assumed_background: list[str]
    facts: list[SerializedFact]
    purpose: str


@dataclass
class ClarificationRequest:
    missing_background: list[str]
    ambiguous_facts: list[str]
    question: str


@dataclass
class ModelConflict:
    key: str
    existing_value: str
    received_value: str
    existing_confidence: float
    received_confidence: float


@dataclass
class IntegrationResult:
    integrated: list[str] = field(default_factory=list)
    clarifications: list[ClarificationRequest] = field(default_factory=list)
    conflicts: list[ModelConflict] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return not self.clarifications and not self.conflicts


class CommunicationEngine:
    """Partial serialization, deserialization, and iterative model integration."""

    def partial_serialize(
        self,
        sender: ObjectiveDrivenWorldModel,
        recipient: ObjectiveDrivenWorldModel,
        purpose: str,
        limit: int = 8,
    ) -> SerializedPacket:
        recipient_keys = set(recipient.facts)
        candidates = [fact for fact in sender.ranked_facts() if fact.key not in recipient_keys or recipient.facts[fact.key].value != fact.value]
        selected = candidates[:limit]
        assumed_background = sorted(set().union(*(fact.dependencies for fact in selected))) if selected else []
        return SerializedPacket(
            sender_revision=sender.revision,
            assumed_background=assumed_background,
            purpose=purpose,
            facts=[
                SerializedFact(
                    key=fact.key,
                    value=fact.value,
                    features=fact.features.tolist(),
                    confidence=fact.confidence,
                    dependencies=sorted(fact.dependencies),
                )
                for fact in selected
            ],
        )

    @staticmethod
    def deserialize(payload: dict[str, Any]) -> SerializedPacket:
        required = {"sender_revision", "assumed_background", "purpose", "facts"}
        missing = sorted(required - set(payload))
        if missing:
            raise ValueError(f"Serialized packet is missing fields: {', '.join(missing)}")
        facts = []
        for raw in payload["facts"]:
            facts.append(
                SerializedFact(
                    key=str(raw["key"]),
                    value=str(raw["value"]),
                    features=[float(value) for value in raw["features"]],
                    confidence=float(raw["confidence"]),
                    dependencies=[str(value) for value in raw.get("dependencies", [])],
                )
            )
        return SerializedPacket(
            sender_revision=int(payload["sender_revision"]),
            assumed_background=[str(value) for value in payload["assumed_background"]],
            purpose=str(payload["purpose"]),
            facts=facts,
        )

    def integrate(
        self,
        packet: SerializedPacket,
        receiver_model: ObjectiveDrivenWorldModel,
        receiver_memory: MemorySystem,
        conflict_threshold: float = 0.65,
    ) -> IntegrationResult:
        result = IntegrationResult()
        known_keys = set(receiver_model.facts)
        packet_keys = {fact.key for fact in packet.facts}
        missing_background = sorted(set(packet.assumed_background) - known_keys - packet_keys)
        if missing_background:
            result.clarifications.append(
                ClarificationRequest(
                    missing_background=missing_background,
                    ambiguous_facts=[],
                    question="Provide the missing background required by the serialized packet.",
                )
            )

        for fact in packet.facts:
            missing_dependencies = sorted(set(fact.dependencies) - known_keys - packet_keys)
            if missing_dependencies:
                result.clarifications.append(
                    ClarificationRequest(
                        missing_background=missing_dependencies,
                        ambiguous_facts=[fact.key],
                        question=f"Provide dependencies required to integrate {fact.key}.",
                    )
                )
                continue
            existing = receiver_model.facts.get(fact.key)
            if existing and existing.value != fact.value:
                combined_confidence = existing.confidence * fact.confidence
                if combined_confidence >= conflict_threshold:
                    result.conflicts.append(
                        ModelConflict(
                            key=fact.key,
                            existing_value=existing.value,
                            received_value=fact.value,
                            existing_confidence=existing.confidence,
                            received_confidence=fact.confidence,
                        )
                    )
                    continue
            receiver_model.upsert_fact(
                fact.key,
                fact.value,
                fact.features,
                confidence=fact.confidence,
                source="communication",
                dependencies=set(fact.dependencies),
            )
            receiver_memory.observe(
                KnowledgeItem.create(
                    fact.key,
                    fact.value,
                    fact.features,
                    confidence=fact.confidence,
                    dependencies=fact.dependencies,
                )
            )
            result.integrated.append(fact.key)
            known_keys.add(fact.key)
        return result
