"""Field processing utilities for automatic defaults."""

from __future__ import annotations

import dataclasses
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Tuple
from typing import cast
from typing import get_type_hints

from yamldataclassconfig.type_defaults import get_default_for_type

if TYPE_CHECKING:
    from dataclasses import Field
    from typing import Any


class TypeHint:
    """Represents a type hint for a dataclass field."""

    # Reason: Ruff's bug
    def __init__(self, type_hints: Dict[str, Any], field_name: str) -> None:  # noqa: UP006
        self.field_name = field_name
        self.field_type = type_hints.get(field_name)
        self.default = None

    def try_to_get_default_value(self) -> bool:
        if not self.field_type:
            return False
        self.default = get_default_for_type(self.field_type)
        return self.default is not None

    def get_automatic_default(self) -> Field[Any]:
        return cast(
            "Field[Any]",
            field(default_factory=self.default) if callable(self.default) else field(default=self.default),  # pylint: disable=invalid-field-call
        )


class DataClass:
    """Represents a dataclass with automatic default values."""

    def __init__(self, cls: type) -> None:
        # Only process if this is a dataclass
        if not dataclasses.is_dataclass(cls):
            msg = "Provided class is not a dataclass"
            raise ValueError(msg)
        self.cls = cls
        # Get type hints for this class
        self.type_hints = get_type_hints(cls)

    def apply_automatic_defaults(self) -> None:
        """Apply automatic defaults to all fields without defaults to prevent mypy warnings."""
        processable_fields = self._get_processable_fields()
        valid_type_hints = self._filter_valid_type_hints(processable_fields)
        self._apply_defaults_to_fields(valid_type_hints)

    # Reason: Ruff's bug
    def _get_processable_fields(self) -> List[Tuple[str, Field[Any]]]:  # noqa: UP006
        """Get fields that can be processed for automatic defaults."""
        return [
            (field_name, field_obj)
            for field_name, field_obj in self.cls.__dataclass_fields__.items()
            if not self.is_already_processed(field_obj)
        ]

    # Reason: Ruff's bug
    def _filter_valid_type_hints(self, fields: List[Tuple[str, Field[Any]]]) -> List[TypeHint]:  # noqa: UP006
        """Filter type hints that can have default values applied."""
        type_hints = [TypeHint(self.type_hints, field_name) for field_name, _ in fields]
        return [hint for hint in type_hints if hint.try_to_get_default_value()]

    # Reason: Ruff's bug
    def _apply_defaults_to_fields(self, type_hints: List[TypeHint]) -> None:  # noqa: UP006
        """Apply automatic defaults to the specified type hints."""
        for type_hint in type_hints:
            self.cls.__dataclass_fields__[type_hint.field_name] = type_hint.get_automatic_default()

    def is_already_processed(self, field_obj: Field[Any]) -> bool:
        """To skip fields that already have defaults or are not included in init."""
        return (
            field_obj.default is not dataclasses.MISSING
            or field_obj.default_factory is not dataclasses.MISSING
            or not field_obj.init
        )


def apply_automatic_defaults(cls: type) -> None:
    """Apply automatic defaults to all fields without defaults to prevent mypy warnings."""
    dataclass = DataClass(cls)
    dataclass.apply_automatic_defaults()
