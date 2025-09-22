"""Factory methods for creating YamlDataClassConfig instances."""

from __future__ import annotations

import dataclasses
from typing import Any
from typing import Generic
from typing import Type
from typing import TypeVar
from typing import get_type_hints

T = TypeVar("T")


# UP006: Ruff's bug
def _get_type_default(field_type: Type[Any]) -> Any:  # noqa: ANN401,UP006
    """Get default value for a field type."""
    # Handle basic types
    type_defaults = {
        int: 0,
        str: "",
        bool: False,
        float: 0.0,
    }

    if field_type in type_defaults:
        return type_defaults[field_type]

    # Handle generic types
    if hasattr(field_type, "__origin__"):
        origin = field_type.__origin__
        origin_defaults: dict[type, Any] = {
            list: [],
            dict: {},
            set: set(),
        }
        return origin_defaults.get(origin)

    return None


class KeyArguments(Generic[T]):
    """Class to hold keyword arguments for config creation."""

    # UP006: Ruff's bug
    def __init__(self, cls: Type[T], **kwargs: Any) -> None:  # noqa: ANN401,UP006
        self.init_kwargs: dict[str, Any] = {}
        self.cls = cls
        self.type_hints = get_type_hints(self.cls)
        self.kwargs = kwargs

    def build_init_kwargs(self) -> None:
        """Builds initialization keyword arguments for the dataclass."""
        # Check if this is a dataclass
        if not dataclasses.is_dataclass(self.cls):
            return
        # Get type hints to identify all expected fields
        for field_name, field_obj in self.cls.__dataclass_fields__.items():
            if not field_obj.init:
                # Skip init=False fields
                continue
            self.init_kwargs[field_name] = self.get_kwarg(field_name, field_obj)

    def get_kwarg(self, field_name: str, field_obj: dataclasses.Field[Any]) -> Any:  # noqa: ANN401
        """Gets the keyword argument value for a field."""
        if field_name in self.kwargs:
            return self.kwargs[field_name]
        if field_obj.default is not dataclasses.MISSING:
            return field_obj.default
        if field_obj.default_factory is not dataclasses.MISSING:
            return field_obj.default_factory()
        # Set appropriate default based on type
        field_type = self.type_hints.get(field_name)
        if field_type:
            return _get_type_default(field_type)
        return None
