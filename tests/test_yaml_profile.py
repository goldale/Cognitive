from __future__ import annotations

import pytest

from cogsys import yaml_profile
from cogsys.errors import YamlProfileError


def test_rejects_aliases() -> None:
    with pytest.raises(YamlProfileError):
        yaml_profile.loads("a: &x [1, 2]\nb: *x\n")


def test_rejects_duplicate_keys() -> None:
    with pytest.raises(YamlProfileError):
        yaml_profile.loads("a: 1\na: 2\n")


def test_rejects_implicit_dates() -> None:
    with pytest.raises(YamlProfileError):
        yaml_profile.loads("date: 2026-07-28\n")


def test_allows_basic_profile() -> None:
    assert yaml_profile.loads("name: test\nvalues:\n  - 1\n  - true\n") == {
        "name": "test",
        "values": [1, True],
    }
