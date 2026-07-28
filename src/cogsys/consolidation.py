from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
import shutil

from .errors import ProposalError
from .state import ResearchState
from . import yaml_profile
from .canonical import canonicalize
from .validation import StateValidator


def _find_entity(collection: list[Any], selector: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    matches: list[tuple[int, dict[str, Any]]] = []
    for index, item in enumerate(collection):
        if isinstance(item, dict) and all(item.get(key) == value for key, value in selector.items()):
            matches.append((index, item))
    if len(matches) != 1:
        raise ProposalError(f"Selector {selector} matched {len(matches)} entities; expected exactly one")
    return matches[0]


def _resolve_collection(document: dict[str, Any], collection_name: str) -> list[Any]:
    collection = document.get(collection_name)
    if not isinstance(collection, list):
        raise ProposalError(f"Collection does not exist or is not a sequence: {collection_name}")
    return collection


def _apply_to_staged(state: ResearchState, proposal: dict[str, Any]) -> set[str]:
    operations = proposal.get("operations")
    if not isinstance(operations, list) or not operations:
        raise ProposalError("Proposal requires at least one operation")
    staged: dict[str, Any] = {role: deepcopy(document) for role, document in state.documents.items()}
    changed_roles: set[str] = set()

    for operation in operations:
        if not isinstance(operation, dict):
            raise ProposalError("Every operation must be a mapping")
        op = operation.get("op")
        role = operation.get("role")
        collection_name = operation.get("collection")
        if not isinstance(role, str) or role not in staged:
            raise ProposalError(f"Unknown role in operation: {role}")
        document = staged[role]
        if not isinstance(document, dict) or not isinstance(collection_name, str):
            raise ProposalError("Operation requires a mapping document and collection")
        collection = _resolve_collection(document, collection_name)

        if op == "add":
            value = operation.get("value")
            if not isinstance(value, dict):
                raise ProposalError("add operation requires mapping value")
            collection.append(deepcopy(value))
        elif op == "update":
            selector = operation.get("selector")
            changes = operation.get("changes")
            if not isinstance(selector, dict) or not isinstance(changes, dict):
                raise ProposalError("update operation requires selector and changes mappings")
            index, entity = _find_entity(collection, selector)
            updated = deepcopy(entity)
            updated.update(deepcopy(changes))
            collection[index] = updated
        elif op == "deprecate":
            selector = operation.get("selector")
            if not isinstance(selector, dict):
                raise ProposalError("deprecate operation requires selector")
            index, entity = _find_entity(collection, selector)
            updated = deepcopy(entity)
            updated["status"] = "T_Deprecated"
            collection[index] = updated
        elif op == "remove":
            selector = operation.get("selector")
            if not isinstance(selector, dict):
                raise ProposalError("remove operation requires selector")
            index, _ = _find_entity(collection, selector)
            collection.pop(index)
        else:
            raise ProposalError(f"Unsupported proposal operation: {op}")
        changed_roles.add(role)

    if bool(proposal.get("semantic_change", True)):
        consolidation = staged.get("consolidation")
        if not isinstance(consolidation, dict):
            raise ProposalError("Consolidation document is missing")
        consolidation["latest"] = {
            "id": proposal.get("id", "CR_Unknown"),
            "kind": "T_ConsolidationRecord",
            "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "summary": proposal.get("summary", "Applied change proposal."),
            "semantic_change": True,
            "inputs": proposal.get("inputs", []),
            "changed_roles": sorted(changed_roles),
            "alternatives": proposal.get("alternatives", []),
            "rationale": proposal.get("rationale", ""),
            "open_questions": proposal.get("open_questions", []),
        }
        changed_roles.add("consolidation")

    for role in sorted(changed_roles):
        state.write_role(role, canonicalize(staged[role]))
    return changed_roles


def apply_proposal(state_root: str | Path, proposal_path: str | Path) -> list[str]:
    original_root = Path(state_root).resolve()
    proposal = yaml_profile.load(proposal_path)
    if not isinstance(proposal, dict):
        raise ProposalError("Proposal must be a mapping")

    with TemporaryDirectory(prefix="cogstate-proposal-") as temporary:
        staged_root = Path(temporary) / "state"
        shutil.copytree(original_root, staged_root)
        staged_state = ResearchState.load(staged_root)
        changed_roles = _apply_to_staged(staged_state, proposal)
        report = StateValidator().validate(ResearchState.load(staged_root))
        if not report.ok:
            details = "; ".join(f"{issue.code}: {issue.message}" for issue in report.errors)
            raise ProposalError(f"Proposal would produce invalid Research State: {details}")

        original_state = ResearchState.load(original_root)
        staged_state = ResearchState.load(staged_root)
        for role in sorted(changed_roles):
            source = staged_state.path_for(role)
            destination = original_state.path_for(role)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return sorted(changed_roles)
