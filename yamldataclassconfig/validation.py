"""Validation utilities for YAML dataclass configuration."""

from __future__ import annotations

import dataclasses
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from yamldataclassconfig.exceptions import ConfigValidationError
from yamldataclassconfig.nullable import is_nullable_type

# Reason: ExceptionGroup is only available in Python 3.11+.
if sys.version_info < (3, 11):  # pragma nocover
    # pylint: disable-next=import-error,redefined-builtin
    from exceptiongroup import ExceptionGroup  # type: ignore[import-not-found]


class ExpectedType:
    """Represents the expected type of a YAML field."""

    # Reason: Ruff's bug
    def __init__(self, expected_type: Type[Any]) -> None:  # noqa: UP006
        self.expected_type = expected_type

    # Reason: Ruff's bug
    def get_actual(self) -> Type[Any]:  # noqa: UP006
        """Get the actual expected type, handling nullable types."""
        if not is_nullable_type(self.expected_type):
            return self.expected_type
        # Guard clause: Check if the type has __args__ attribute using type narrowing
        if not hasattr(self.expected_type, "__args__"):
            return self.expected_type

        args = self._get_type_args()
        if args is None:
            return self.expected_type

        return self.get_single_non_none_type(args, self.expected_type)

    # Reason: Ruff's bug
    def _get_type_args(self) -> Optional[Union[Tuple[Any, ...], List[Any]]]:  # noqa: UP006,UP007,UP045
        """Get type arguments from a type if they exist and are iterable."""
        args = getattr(self.expected_type, "__args__", None)
        if args is None or not isinstance(args, (tuple, list)):
            return None
        return args  # type: ignore[no-any-return]

    @staticmethod
    # Reason: Ruff's bug
    def get_single_non_none_type(args: Union[Tuple[Any, ...], List[Any]], fallback_type: Type[Any]) -> Type[Any]:  # noqa: UP006,UP007
        """Extract single non-None type from args, return fallback if not exactly one."""
        non_none_types = [arg for arg in args if arg is not type(None)]
        if len(non_none_types) == 1:
            return non_none_types[0]  # type: ignore[no-any-return]
        return fallback_type


@dataclasses.dataclass
class Validation:
    """Represents the validation state of a YAML field."""

    field_name: str
    yaml_value: Any
    # Reason: Ruff's bug
    expected_type: Type[Any]  # noqa: UP006

    # Reason: Ruff's bug
    def validate(self) -> Optional[ConfigValidationError]:  # noqa: UP045
        """Validate the YAML field against its expected type."""
        actual_expected_type = ExpectedType(self.expected_type).get_actual()

        # Skip validation for dataclass types - they'll be handled by marshmallow
        if self.is_dataclass_type(actual_expected_type):
            return None

        if self.yaml_value is not None and not isinstance(self.yaml_value, actual_expected_type):
            msg = f"Field '{self.field_name}' expected {actual_expected_type.__name__}, got {type(self.yaml_value).__name__}"
            return ConfigValidationError(msg)
        return None

    @staticmethod
    def is_dataclass_type(field_type: type) -> bool:
        """Check if the field type is a dataclass."""
        try:
            return dataclasses.is_dataclass(field_type)
        except (TypeError, AttributeError):
            return False


class YamlFieldValidations:
    """Represents the validation state of YAML fields."""

    # Reason: Ruff's bug
    def __init__(self, dictionary_config: Dict[str, Any], type_hints: Dict[str, Type[Any]]) -> None:  # noqa: UP006
        self.validations = (
            Validation(field_name, yaml_value, type_hints[field_name])
            for field_name, yaml_value in dictionary_config.items()
            if field_name in type_hints
        )

    def validate(self) -> None:
        """Validate YAML fields against their expected types."""
        errors = [error for error in (validation.validate() for validation in self.validations) if error]
        if errors:
            group_msg = "Configuration validation failed"
            raise ExceptionGroup(group_msg, errors)


# Reason: Ruff's bug
def validate_config_if_needed(dictionary_config: Dict[str, Any], type_hints: Dict[str, Any]) -> None:  # noqa: UP006
    """Validate configuration if type hints are present."""
    if not type_hints or not any(name != "FILE_PATH" for name in type_hints):
        return
    YamlFieldValidations(dictionary_config, type_hints).validate()
