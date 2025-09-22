"""Exception classes for yamldataclassconfig."""

from __future__ import annotations

__all__ = [
    "ConfigNotLoadedError",
    "ConfigValidationError",
]


class ConfigNotLoadedError(Exception):
    """Raised when accessing a property before the config is loaded."""


class ConfigValidationError(Exception):
    """Raised when there are type validation errors during config loading."""
