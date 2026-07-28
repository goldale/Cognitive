from __future__ import annotations

from cogsys.semantic_merge import three_way_merge


def test_independent_changes_merge() -> None:
    base = {"a": 1, "b": 1}
    ours = {"a": 2, "b": 1}
    theirs = {"a": 1, "b": 3}
    result = three_way_merge(base, ours, theirs)
    assert result.value == {"a": 2, "b": 3}
    assert not result.conflicts


def test_conflicting_scalar_is_reported() -> None:
    result = three_way_merge({"a": 1}, {"a": 2}, {"a": 3})
    assert result.value["a"] == 2
    assert len(result.conflicts) == 1
    assert result.conflicts[0].path == "$.a"


def test_entity_lists_merge_by_id() -> None:
    base = {"items": [{"id": "H_001", "confidence": 0.5}]}
    ours = {"items": [{"id": "H_001", "confidence": 0.6}]}
    theirs = {"items": [{"id": "H_001", "confidence": 0.5, "note": "new"}]}
    result = three_way_merge(base, ours, theirs)
    assert result.value["items"][0] == {"id": "H_001", "confidence": 0.6, "note": "new"}
    assert not result.conflicts
