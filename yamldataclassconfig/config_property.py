"""This module implements property descriptors for config validation."""

from __future__ import annotations

from typing import Any
from typing import Optional

from yamldataclassconfig.exceptions import ConfigNotLoadedError


class ConfigProperty:
    """A property descriptor that checks if config is loaded before access."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.private_name = f"__{name}"

    # UP045: Ruff's bug
    def __get__(self, obj: Any, objtype: Optional[type] = None) -> Any:  # noqa: ANN401,UP045
        if obj is None:
            return self

        if not getattr(obj, "_loaded", False):
            msg = f"Configuration must be loaded before accessing '{self.name}'. Call load() first."
            raise ConfigNotLoadedError(msg)

        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: Any) -> None:  # noqa: ANN401
        setattr(obj, self.private_name, value)


def create_property_descriptors(cls: type) -> None:
    """Create property descriptors for class annotations."""
    annotations = getattr(cls, "__annotations__", {})
    for field_name in (field_name for field_name in annotations if field_name != "FILE_PATH"):
        setattr(cls, field_name, ConfigProperty(field_name))
