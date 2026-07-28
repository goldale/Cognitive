from __future__ import annotations


class CogsysError(Exception):
    """Base exception for the project."""


class YamlProfileError(CogsysError):
    """Raised when a file violates the restricted YAML profile."""


class ValidationFailure(CogsysError):
    """Raised when Research State validation fails."""


class ProposalError(CogsysError):
    """Raised when a change proposal cannot be applied."""
