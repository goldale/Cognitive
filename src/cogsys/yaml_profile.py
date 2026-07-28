from __future__ import annotations

from datetime import date, datetime
from math import isfinite
from pathlib import Path
from typing import Any

import yaml
from yaml.events import AliasEvent, CollectionStartEvent, ScalarEvent

from .errors import YamlProfileError


class RestrictedLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(loader: RestrictedLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise YamlProfileError(f"YAML mapping keys must be strings; got {type(key).__name__}")
        if key in mapping:
            raise YamlProfileError(f"Duplicate YAML mapping key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


RestrictedLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def _scan_syntax(text: str, source: str) -> None:
    try:
        for event in yaml.parse(text):
            if isinstance(event, AliasEvent):
                raise YamlProfileError(f"{source}: YAML aliases are prohibited")
            if isinstance(event, CollectionStartEvent) and event.anchor is not None:
                raise YamlProfileError(f"{source}: YAML anchors are prohibited")
            if isinstance(event, ScalarEvent):
                if event.anchor is not None:
                    raise YamlProfileError(f"{source}: YAML anchors are prohibited")
                # Explicit tags make parsing depend on YAML-specific behavior and are disallowed.
                if event.tag is not None:
                    raise YamlProfileError(f"{source}: explicit YAML tags are prohibited")
    except yaml.YAMLError as exc:
        raise YamlProfileError(f"{source}: invalid YAML: {exc}") from exc


def _validate_value(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not isfinite(value):
            raise YamlProfileError(f"{path}: non-finite floating-point values are prohibited")
        return
    if isinstance(value, (date, datetime)):
        raise YamlProfileError(f"{path}: implicit date/time values are prohibited; quote them as strings")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_value(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise YamlProfileError(f"{path}: YAML mapping keys must be strings")
            _validate_value(item, f"{path}.{key}")
        return
    raise YamlProfileError(f"{path}: unsupported YAML value type {type(value).__name__}")


def loads(text: str, source: str = "<string>") -> Any:
    _scan_syntax(text, source)
    try:
        value = yaml.load(text, Loader=RestrictedLoader)
    except YamlProfileError:
        raise
    except yaml.YAMLError as exc:
        raise YamlProfileError(f"{source}: invalid YAML: {exc}") from exc
    _validate_value(value)
    return value


def load(path: str | Path) -> Any:
    file_path = Path(path)
    return loads(file_path.read_text(encoding="utf-8"), str(file_path))


def dumps(value: Any) -> str:
    _validate_value(value)
    return yaml.safe_dump(
        value,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
        indent=2,
    )


def dump(value: Any, path: str | Path) -> None:
    Path(path).write_text(dumps(value), encoding="utf-8")
