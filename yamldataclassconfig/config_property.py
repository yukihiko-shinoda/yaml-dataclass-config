"""This module implements property descriptors for config validation."""

from __future__ import annotations

import threading
from dataclasses import MISSING
from dataclasses import fields
from typing import Any
from typing import Optional

from yamldataclassconfig.exceptions import ConfigNotLoadedError

# Thread-local storage for deserialization context
_local = threading.local()


class ConfigProperty:
    """A property descriptor that checks if config is loaded before access."""

    def __init__(self, name: str, original_default: Any = MISSING) -> None:  # noqa: ANN401
        self.name = name
        self.private_name = f"__{name}"
        self.original_default = original_default

    # UP045: Ruff's bug
    def __get__(self, obj: Any, objtype: Optional[type] = None) -> Any:  # noqa: ANN401,UP045
        if obj is None:
            # When accessed on the class (not an instance), return the original default
            # This happens during schema generation
            if self.original_default is not MISSING:
                return self.original_default
            return self

        if not getattr(obj, "_loaded", False):
            # Check if we're in deserialization context
            if getattr(_local, "in_deserialization", False):
                # During deserialization, return field defaults to allow dataclasses-json to work
                return self._get_field_default(obj.__class__)
            # Normal access before load should raise error
            msg = f"Configuration must be loaded before accessing '{self.name}'. Call load() first."
            raise ConfigNotLoadedError(msg)

        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: Any) -> None:  # noqa: ANN401
        setattr(obj, self.private_name, value)

    def _get_field_default(self, cls: type) -> Any:  # noqa: ANN401
        """Get the default value for this field from the dataclass definition."""
        for field in fields(cls):
            if field.name == self.name:
                if field.default is not MISSING:
                    return field.default
                if field.default_factory is not MISSING:
                    return field.default_factory()
                # Field has no default, raise the original error
                msg = f"Configuration must be loaded before accessing '{self.name}'. Call load() first."
                raise ConfigNotLoadedError(msg)

        # Field not found (shouldn't happen), raise the original error
        msg = f"Configuration must be loaded before accessing '{self.name}'. Call load() first."
        raise ConfigNotLoadedError(msg)


def set_deserialization_context(*, value: bool) -> None:
    """Set the deserialization context flag."""
    _local.in_deserialization = value


def create_property_descriptors(cls: type) -> None:
    """Create property descriptors for class annotations."""
    annotations = getattr(cls, "__annotations__", {})

    # Create property descriptors with original defaults preserved
    for field_name in (field_name for field_name in annotations if field_name != "FILE_PATH"):
        setattr(cls, field_name, ConfigProperty(field_name, getattr(cls, field_name, MISSING)))
