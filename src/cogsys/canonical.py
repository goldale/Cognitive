from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from . import yaml_profile


PREFERRED_KEYS = (
    "kind",
    "id",
    "token",
    "atomic",
    "title",
    "definition",
    "expression",
    "statement",
    "status",
    "confidence",
    "order",
    "summary",
    "rationale",
    "evidence",
    "falsifiers",
    "related_tokens",
    "relations",
    "files",
    "chapters",
    "sections",
    "blocks",
)
_KEY_RANK = {key: index for index, key in enumerate(PREFERRED_KEYS)}


def _key_sort(key: str) -> tuple[int, str]:
    return (_KEY_RANK.get(key, len(_KEY_RANK)), key)


def canonicalize(value: Any, parent_key: str | None = None) -> Any:
    if isinstance(value, Mapping):
        return {
            key: canonicalize(value[key], key)
            for key in sorted(value.keys(), key=_key_sort)
        }
    if isinstance(value, list):
        items = [canonicalize(item, parent_key) for item in value]
        if items and all(isinstance(item, dict) for item in items):
            if all("order" in item for item in items):
                return sorted(items, key=lambda item: (item["order"], item.get("id", "")))
            if parent_key in {"tokens"} and all("token" in item for item in items):
                # Token declaration order is semantically significant. Preserve it.
                return items
            if parent_key not in {"blocks", "operations", "arguments"}:
                if all("id" in item for item in items):
                    return sorted(items, key=lambda item: item["id"])
        return items
    return value


def format_file(path: str | Path) -> bool:
    file_path = Path(path)
    original = file_path.read_text(encoding="utf-8")
    value = yaml_profile.loads(original, str(file_path))
    formatted = yaml_profile.dumps(canonicalize(value))
    if original != formatted:
        file_path.write_text(formatted, encoding="utf-8")
        return True
    return False
