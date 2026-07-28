from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


_MISSING = object()


@dataclass
class MergeConflict:
    path: str
    base: Any
    ours: Any
    theirs: Any


@dataclass
class MergeResult:
    value: Any
    conflicts: list[MergeConflict] = field(default_factory=list)


def _identity_key(items: list[Any]) -> str | None:
    if items and all(isinstance(item, dict) for item in items):
        for key in ("token", "id"):
            if all(isinstance(item.get(key), str) for item in items):
                return key
    return None


def three_way_merge(base: Any, ours: Any, theirs: Any, path: str = "$") -> MergeResult:
    if ours == theirs:
        return MergeResult(deepcopy(ours))
    if ours == base:
        return MergeResult(deepcopy(theirs))
    if theirs == base:
        return MergeResult(deepcopy(ours))

    if isinstance(base, dict) and isinstance(ours, dict) and isinstance(theirs, dict):
        result: dict[str, Any] = {}
        conflicts: list[MergeConflict] = []
        for key in sorted(set(base) | set(ours) | set(theirs)):
            b = base.get(key, _MISSING)
            o = ours.get(key, _MISSING)
            t = theirs.get(key, _MISSING)
            child_path = f"{path}.{key}"
            if o is _MISSING and t is _MISSING:
                continue
            if o is _MISSING:
                if b is _MISSING:
                    result[key] = deepcopy(t)
                    continue
                if t == b:
                    continue
                conflicts.append(MergeConflict(child_path, b, None, t))
                result[key] = deepcopy(t)
                continue
            if t is _MISSING:
                if b is _MISSING:
                    result[key] = deepcopy(o)
                    continue
                if o == b:
                    continue
                conflicts.append(MergeConflict(child_path, b, o, None))
                result[key] = deepcopy(o)
                continue
            child = three_way_merge(None if b is _MISSING else b, o, t, child_path)
            result[key] = child.value
            conflicts.extend(child.conflicts)
        return MergeResult(result, conflicts)

    if isinstance(base, list) and isinstance(ours, list) and isinstance(theirs, list):
        identity = _identity_key(base + ours + theirs)
        if identity:
            b_map = {item[identity]: item for item in base}
            o_map = {item[identity]: item for item in ours}
            t_map = {item[identity]: item for item in theirs}
            merged = three_way_merge(b_map, o_map, t_map, path)
            values = list(merged.value.values())
            values.sort(key=lambda item: (item.get("order", 10**9), item[identity]))
            return MergeResult(values, merged.conflicts)

    return MergeResult(
        deepcopy(ours),
        [MergeConflict(path=path, base=deepcopy(base), ours=deepcopy(ours), theirs=deepcopy(theirs))],
    )
