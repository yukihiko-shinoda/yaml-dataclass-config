"""Type default handling for automatic field defaults."""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import Type

__all__ = [
    "get_default_for_type",
]


# UP006: Ruff's bug
def get_default_for_type(field_type: Type[Any]) -> Any:  # noqa: ANN401,UP006
    """Get appropriate default value for a field type.

    Returns None if no appropriate default can be determined, or a callable for mutable types (to be used with
    default_factory).
    """
    # Handle basic immutable types
    basic_defaults = {
        int: 0,
        str: "",
        bool: False,
        float: 0.0,
    }

    if field_type in basic_defaults:
        return basic_defaults[field_type]

    # Handle generic types (return callables for mutable types)
    if hasattr(field_type, "__origin__"):
        origin = field_type.__origin__
        mutable_defaults = {
            list: list,
            dict: dict,
            set: set,
            List: list,
            Dict: dict,
            Set: set,
        }
        if origin in mutable_defaults:
            return mutable_defaults[origin]

    # For unknown types, return None (field will keep no default)
    return None
