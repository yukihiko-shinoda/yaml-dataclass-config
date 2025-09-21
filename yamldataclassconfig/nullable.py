"""This module implements nullable dataclass functionality."""

from __future__ import annotations

from typing import Any
from typing import Union

__all__ = [
    "is_nullable_type",
]


def is_nullable_type(tp: Any) -> bool:  # noqa: ANN401
    """Check if a type annotation already includes None."""
    # Handle Union types
    origin = getattr(tp, "__origin__", None)
    if origin is Union:
        return type(None) in tp.__args__

    # Handle Python 3.10+ union syntax (X | Y)
    if hasattr(tp, "__class__") and tp.__class__.__name__ == "UnionType":
        return type(None) in tp.__args__

    return False
