from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .errors import CogsysError
from . import yaml_profile


@dataclass
class ResearchState:
    root: Path
    manifest: dict[str, Any]
    documents: dict[str, Any]

    @classmethod
    def load(cls, root: str | Path) -> "ResearchState":
        root_path = Path(root).resolve()
        manifest_path = root_path / "manifest.yaml"
        if not manifest_path.is_file():
            raise CogsysError(f"Research State manifest not found: {manifest_path}")
        manifest = yaml_profile.load(manifest_path)
        if not isinstance(manifest, dict):
            raise CogsysError("manifest.yaml must contain a mapping")
        file_map = manifest.get("files", {})
        if not isinstance(file_map, dict):
            raise CogsysError("manifest.files must be a mapping")
        documents: dict[str, Any] = {"manifest": manifest}
        for role, relative in file_map.items():
            if role in {"content_directory", "documentation_output"}:
                continue
            if not isinstance(relative, str):
                raise CogsysError(f"manifest.files.{role} must be a string path")
            path = cls._safe_path(root_path, relative)
            if not path.is_file():
                raise CogsysError(f"Required Research State file not found: {path}")
            documents[role] = yaml_profile.load(path)
        return cls(root=root_path, manifest=manifest, documents=documents)

    @staticmethod
    def _safe_path(root: Path, relative: str) -> Path:
        candidate = (root / relative).resolve()
        if candidate != root and root not in candidate.parents:
            raise CogsysError(f"Path escapes Research State root: {relative}")
        return candidate

    def path_for(self, role: str) -> Path:
        if role == "manifest":
            return self.root / "manifest.yaml"
        relative = self.manifest["files"].get(role)
        if not isinstance(relative, str):
            raise CogsysError(f"Unknown Research State role: {role}")
        return self._safe_path(self.root, relative)

    def content_directory(self) -> Path:
        relative = self.manifest["files"].get("content_directory", "content")
        return self._safe_path(self.root, relative)

    def documentation_output(self) -> Path:
        relative = self.manifest["files"].get("documentation_output", "../docs")
        return self._safe_path(self.root, relative)

    def token_entries(self) -> list[dict[str, Any]]:
        registry = self.documents.get("tokens", {})
        entries = registry.get("tokens", []) if isinstance(registry, dict) else []
        return entries if isinstance(entries, list) else []

    def token_map(self) -> dict[str, dict[str, Any]]:
        return {
            entry["token"]: entry
            for entry in self.token_entries()
            if isinstance(entry, dict) and isinstance(entry.get("token"), str)
        }

    def iter_entities(self) -> Iterator[tuple[str, dict[str, Any]]]:
        for role, document in self.documents.items():
            if role in {"manifest", "tokens", "consolidation", "chapters"}:
                continue
            if not isinstance(document, dict):
                continue
            for value in document.values():
                if isinstance(value, list):
                    for entity in value:
                        if isinstance(entity, dict):
                            yield role, entity

    def load_content(self, relative: str) -> dict[str, Any]:
        path = self._safe_path(self.root, relative)
        value = yaml_profile.load(path)
        if not isinstance(value, dict):
            raise CogsysError(f"Content file must contain a mapping: {path}")
        return value

    def write_role(self, role: str, value: Any) -> None:
        yaml_profile.dump(value, self.path_for(role))
        self.documents[role] = value
