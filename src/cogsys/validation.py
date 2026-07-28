from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from .state import ResearchState


TOKEN_PATTERN = re.compile(r"^T_(?:[A-Z][a-z0-9]*)+$")
ENTITY_ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*_[0-9]{3,}$")
TOKEN_IN_TEXT_PATTERN = re.compile(r"\bT_(?:[A-Z][A-Za-z0-9]*)+\b")


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    path: str
    message: str


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(self, severity: str, code: str, path: str, message: str) -> None:
        self.issues.append(ValidationIssue(severity, code, path, message))


class StateValidator:
    def __init__(self, schema_path: str | Path | None = None):
        self.schema_path = Path(schema_path) if schema_path else None

    def validate(self, state: ResearchState) -> ValidationReport:
        report = ValidationReport()
        self._validate_json_schema(state, report)
        token_map, atomic_tokens = self._validate_tokens(state, report)
        self._validate_entities(state, token_map, report)
        self._validate_chapters(state, report)
        self._validate_consolidation(state, report)
        report.metrics.update(
            token_count=len(token_map),
            atomic_token_count=len(atomic_tokens),
            derived_token_count=len(token_map) - len(atomic_tokens),
        )
        return report

    def _validate_json_schema(self, state: ResearchState, report: ValidationReport) -> None:
        if self.schema_path is None or not self.schema_path.is_file():
            return
        schema = json.loads(self.schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for role, document in state.documents.items():
            envelope = {"role": role, "document": document}
            for error in validator.iter_errors(envelope):
                location = ".".join(str(part) for part in error.absolute_path)
                report.add("error", "SCHEMA", f"{role}:{location}", error.message)

    def _validate_tokens(
        self, state: ResearchState, report: ValidationReport
    ) -> tuple[dict[str, dict[str, Any]], set[str]]:
        token_map: dict[str, dict[str, Any]] = {}
        atomic_tokens: set[str] = set()
        seen_order: set[str] = set()
        for index, entry in enumerate(state.token_entries()):
            path = f"tokens.tokens[{index}]"
            if not isinstance(entry, dict):
                report.add("error", "TOKEN_ENTRY", path, "Token entry must be a mapping")
                continue
            token = entry.get("token")
            if not isinstance(token, str) or not TOKEN_PATTERN.fullmatch(token):
                report.add("error", "TOKEN_NAME", f"{path}.token", "Token must match T_<PascalCaseIdentifier>")
                continue
            if token in token_map:
                report.add("error", "TOKEN_DUPLICATE", f"{path}.token", f"Duplicate token {token}")
                continue
            token_map[token] = entry
            atomic = entry.get("atomic") is True
            if atomic:
                atomic_tokens.add(token)
                definition = entry.get("definition")
                if not isinstance(definition, str) or not definition.strip():
                    report.add("error", "ATOMIC_DEFINITION", path, "Atomic Token requires a natural-language definition")
                if "expression" in entry:
                    report.add("error", "ATOMIC_EXPRESSION", path, "Atomic Token must not have an expression")
            else:
                if "definition" in entry:
                    report.add("error", "DERIVED_NATURAL_DEFINITION", path, "Derived Token must not have a natural-language definition")
                expression = entry.get("expression")
                if not isinstance(expression, dict):
                    report.add("error", "DERIVED_EXPRESSION", path, "Derived Token requires an expression")
                else:
                    references = self._expression_references(expression)
                    for reference in references:
                        if reference not in seen_order:
                            report.add("error", "TOKEN_FORWARD_REFERENCE", path, f"Derived Token references token not defined earlier: {reference}")
                        elif reference not in atomic_tokens:
                            report.add("error", "TOKEN_NONATOMIC_REFERENCE", path, f"Derived Token definitions may reference Atomic Tokens only: {reference}")
            seen_order.add(token)
        return token_map, atomic_tokens

    @staticmethod
    def _expression_references(expression: dict[str, Any]) -> list[str]:
        refs: list[str] = []
        operator = expression.get("operator")
        if isinstance(operator, str):
            refs.append(operator)
        arguments = expression.get("arguments", [])
        if isinstance(arguments, list):
            refs.extend(arg for arg in arguments if isinstance(arg, str))
        return refs

    def _validate_entities(
        self,
        state: ResearchState,
        token_map: dict[str, dict[str, Any]],
        report: ValidationReport,
    ) -> None:
        ids: dict[str, str] = {}
        for role, entity in state.iter_entities():
            entity_id = entity.get("id")
            path = f"{role}:{entity_id or '<missing>'}"
            if not isinstance(entity_id, str) or not ENTITY_ID_PATTERN.fullmatch(entity_id):
                report.add("error", "ENTITY_ID", path, "Entity id must use PREFIX_### format")
            elif entity_id in ids:
                report.add("error", "ENTITY_DUPLICATE", path, f"Entity id already used in {ids[entity_id]}")
            else:
                ids[entity_id] = role
            kind = entity.get("kind")
            if not isinstance(kind, str) or kind not in token_map:
                report.add("error", "ENTITY_KIND", path, f"Unknown entity kind token: {kind}")
            for reference in self._find_token_references(entity):
                if reference not in token_map:
                    report.add("error", "TOKEN_REFERENCE", path, f"Unknown token reference: {reference}")

    def _validate_chapters(self, state: ResearchState, report: ValidationReport) -> None:
        document = state.documents.get("chapters", {})
        chapters = document.get("chapters", []) if isinstance(document, dict) else []
        if not isinstance(chapters, list):
            report.add("error", "CHAPTERS", "chapters", "chapters must be a sequence")
            return
        orders: set[int] = set()
        for ci, chapter in enumerate(chapters):
            path = f"chapters.chapters[{ci}]"
            if not isinstance(chapter, dict):
                report.add("error", "CHAPTER", path, "Chapter must be a mapping")
                continue
            order = chapter.get("order")
            if not isinstance(order, int) or order < 1:
                report.add("error", "CHAPTER_ORDER", path, "Chapter order must be a positive integer")
            elif order in orders:
                report.add("error", "CHAPTER_ORDER_DUPLICATE", path, f"Duplicate chapter order {order}")
            else:
                orders.add(order)
            layout = chapter.get("layout")
            if layout not in {"single", "directory"}:
                report.add("error", "CHAPTER_LAYOUT", path, "Chapter layout must be single or directory")
            sections = chapter.get("sections", [])
            if not isinstance(sections, list) or not sections:
                report.add("error", "CHAPTER_SECTIONS", path, "Chapter requires at least one section")
                continue
            for si, section in enumerate(sections):
                section_path = f"{path}.sections[{si}]"
                if not isinstance(section, dict):
                    report.add("error", "SECTION", section_path, "Section must be a mapping")
                    continue
                content_file = section.get("content_file")
                if not isinstance(content_file, str):
                    report.add("error", "CONTENT_FILE", section_path, "Section requires content_file")
                else:
                    candidate = (state.root / content_file).resolve()
                    if not candidate.is_file():
                        report.add("error", "CONTENT_MISSING", section_path, f"Content file not found: {content_file}")

    def _validate_consolidation(self, state: ResearchState, report: ValidationReport) -> None:
        document = state.documents.get("consolidation")
        if not isinstance(document, dict):
            report.add("error", "CONSOLIDATION", "consolidation", "Consolidation document must be a mapping")
            return
        record = document.get("latest")
        if not isinstance(record, dict):
            report.add("error", "CONSOLIDATION_LATEST", "consolidation.latest", "latest record is required")
            return
        for field in ("id", "kind", "summary", "semantic_change"):
            if field not in record:
                report.add("error", "CONSOLIDATION_FIELD", f"consolidation.latest.{field}", f"Missing field {field}")

    @staticmethod
    def _find_token_references(value: Any) -> Iterable[str]:
        if isinstance(value, str):
            yield from TOKEN_IN_TEXT_PATTERN.findall(value)
        elif isinstance(value, list):
            for item in value:
                yield from StateValidator._find_token_references(item)
        elif isinstance(value, dict):
            for item in value.values():
                yield from StateValidator._find_token_references(item)
