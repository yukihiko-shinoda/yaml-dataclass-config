"""Comprehensive tests for validation.py to achieve 100% coverage."""

from __future__ import annotations

import dataclasses
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Union

import pytest

import yamldataclassconfig.validation as validation_module
from tests.conftest import SimpleTestConfig
from yamldataclassconfig.exceptions import ConfigValidationError
from yamldataclassconfig.validation import ExpectedType
from yamldataclassconfig.validation import Validation
from yamldataclassconfig.validation import YamlFieldValidations
from yamldataclassconfig.validation import validate_config_if_needed

# Reason: ExceptionGroup is only available in Python 3.11+.
if sys.version_info < (3, 11):  # pragma nocover
    # pylint: disable-next=import-error,redefined-builtin
    from exceptiongroup import ExceptionGroup  # type: ignore[import-not-found]


class TestExpectedType:
    """Test ExpectedType class for comprehensive coverage."""

    def test_get_actual_simple_type(self) -> None:
        """Test get_actual with simple non-nullable type."""
        expected_type = ExpectedType(str)
        assert expected_type.get_actual() is str

    def test_get_actual_nullable_type(self) -> None:
        """Test get_actual with nullable type Union[str, None]."""
        expected_type = ExpectedType(Union[str, None])  # type: ignore[arg-type]
        assert expected_type.get_actual() is str

    def test_get_actual_type_without_args(self) -> None:
        """Test get_actual with type that appears nullable but has no __args__."""

        class FakeType:  # pylint: disable=too-few-public-methods
            """Fake type that looks nullable but has no __args__."""

            def __init__(self) -> None:
                pass

        fake_type = FakeType()
        expected_type = ExpectedType(fake_type)  # type: ignore[arg-type]
        assert expected_type.get_actual() == fake_type  # type: ignore[comparison-overlap]

    def test_get_actual_non_nullable_type_with_args(self) -> None:
        """Test get_actual with non-nullable type that has __args__ - covers line 27."""
        # Using list[str] which has __args__ but is not nullable
        expected_type = ExpectedType(List[str])
        result = expected_type.get_actual()
        assert result == List[str]  # Should return type as-is since it's not nullable

    def test_get_actual_nullable_type_without_args(self) -> None:
        """Test get_actual with nullable type that somehow has no __args__ - covers line 27."""

        class FakeNullableType:  # pylint: disable=too-few-public-methods
            """Fake nullable type without __args__."""

            def __init__(self) -> None:
                pass

        # This will go through the nullable check but then return early due to no __args__
        fake_type = FakeNullableType()
        expected_type = ExpectedType(fake_type)  # type: ignore[arg-type]

        # Patch is_nullable_type to return True for our fake type
        original_is_nullable = validation_module.is_nullable_type  # type: ignore[attr-defined]

        def mock_is_nullable(t: Any) -> bool:  # noqa: ANN401
            if isinstance(t, FakeNullableType):
                return True
            return original_is_nullable(t)

        validation_module.is_nullable_type = mock_is_nullable  # type: ignore[assignment,attr-defined]
        try:
            result = expected_type.get_actual()
            # Should return original type (line 27)
            assert result == fake_type  # type: ignore[comparison-overlap]
        finally:
            validation_module.is_nullable_type = original_is_nullable  # type: ignore[attr-defined]

    def test_get_type_args_none(self) -> None:
        """Test _get_type_args when args is None."""

        class TypeWithoutArgs:  # pylint: disable=too-few-public-methods
            """Type without __args__ attribute."""

            def __init__(self) -> None:
                pass

        expected_type = ExpectedType(TypeWithoutArgs())  # type: ignore[arg-type]
        assert expected_type.get_actual()

    def test_get_type_args_not_iterable(self) -> None:
        """Test _get_type_args when args is not iterable."""

        class TypeWithNonIterableArgs:  # pylint: disable=too-few-public-methods
            """Type with non-iterable __args__."""

            def __init__(self) -> None:
                self.__args__ = 42  # Not iterable

        expected_type = ExpectedType(TypeWithNonIterableArgs())  # type: ignore[arg-type]
        assert expected_type.get_actual()

    def test_get_single_non_none_type_multiple_types(self) -> None:
        """Test _get_single_non_none_type with multiple non-None types."""
        args = [str, int, bool]
        fallback = object
        result = ExpectedType.get_single_non_none_type(args, fallback)
        assert result == fallback


class TestValidation:
    """Test Validation class for comprehensive coverage."""

    def test_validate_valid_field(self) -> None:
        """Test validation of a valid field."""
        validation = Validation("name", "test", str)
        result = validation.validate()
        assert result is None

    def test_validate_invalid_field(self) -> None:
        """Test validation of an invalid field."""
        validation = Validation("age", "not_an_int", int)
        result = validation.validate()
        assert isinstance(result, ConfigValidationError)
        assert "Field 'age' expected int, got str" in str(result)

    def test_validate_none_value(self) -> None:
        """Test validation with None value (should pass)."""
        validation = Validation("optional_field", None, str)
        result = validation.validate()
        assert result is None

    def test_validate_dataclass_field(self) -> None:
        """Test validation of a dataclass field (should be skipped)."""
        validation = Validation("config", {"name": "test", "age": 25}, SimpleTestConfig)
        result = validation.validate()
        assert result is None

    def test_is_dataclass_type_true(self) -> None:
        """Test is_dataclass_type with actual dataclass."""
        assert Validation.is_dataclass_type(SimpleTestConfig) is True

    def test_is_dataclass_type_false(self) -> None:
        """Test is_dataclass_type with non-dataclass."""
        assert Validation.is_dataclass_type(str) is False

    def test_is_dataclass_type_error_handling(self) -> None:
        """Test is_dataclass_type error handling for TypeError and AttributeError - covers lines 77-78."""
        # Test with object that causes TypeError when passed to dataclasses.is_dataclass
        assert Validation.is_dataclass_type(42) is False  # type: ignore[arg-type]

        # Test with object that causes AttributeError by patching dataclasses.is_dataclass

        original_is_dataclass = dataclasses.is_dataclass

        def mock_is_dataclass_with_error(obj: Any) -> bool:  # noqa: ANN401
            if isinstance(obj, str) and obj == "trigger_attribute_error":
                msg = "Simulated AttributeError"
                raise AttributeError(msg)
            return original_is_dataclass(obj)

        dataclasses.is_dataclass = mock_is_dataclass_with_error  # type: ignore[assignment]
        try:
            # This should trigger the AttributeError exception path (lines 77-78)
            assert Validation.is_dataclass_type("trigger_attribute_error") is False  # type: ignore[arg-type]
        finally:
            dataclasses.is_dataclass = original_is_dataclass

    def test_get_type_args_returns_none_for_nullable_type(self) -> None:
        """Test case where _get_type_args returns None for a nullable type - covers line 31."""

        class NullableTypeWithBadArgs:  # pylint: disable=too-few-public-methods
            """Nullable type with non-iterable __args__."""

            def __init__(self) -> None:
                self.__args__ = "not_iterable"  # String is not tuple/list

        fake_type = NullableTypeWithBadArgs()

        # Patch is_nullable_type to return True for our fake type
        original_is_nullable = validation_module.is_nullable_type  # type: ignore[attr-defined]

        def mock_is_nullable(t: Any) -> bool:  # noqa: ANN401
            if isinstance(t, NullableTypeWithBadArgs):
                return True
            return original_is_nullable(t)

        validation_module.is_nullable_type = mock_is_nullable  # type: ignore[assignment,attr-defined]
        try:
            expected_type = ExpectedType(fake_type)  # type: ignore[arg-type]
            result = expected_type.get_actual()
            # Should return original type (line 31)
            assert result == fake_type  # type: ignore[comparison-overlap]
        finally:
            validation_module.is_nullable_type = original_is_nullable  # type: ignore[attr-defined]


class TestYamlFieldValidations:
    """Test YamlFieldValidations class for comprehensive coverage."""

    def test_validate_all_valid(self) -> None:
        """Test validation when all fields are valid."""
        config = {"name": "test", "age": 25}
        type_hints = {"name": str, "age": int}

        validations = YamlFieldValidations(config, type_hints)
        # Should not raise any exception
        validations.validate()

    def test_validate_with_errors(self) -> None:
        """Test validation when fields have errors."""
        config = {"name": 123, "age": "not_int"}
        type_hints = {"name": str, "age": int}

        validations = YamlFieldValidations(config, type_hints)
        with pytest.raises(ExceptionGroup) as exc_info:
            validations.validate()

        assert "Configuration validation failed" in str(exc_info.value)
        expected_exception_count = 2
        assert len(exc_info.value.exceptions) == expected_exception_count

    def test_validate_skip_missing_type_hints(self) -> None:
        """Test that fields without type hints are skipped."""
        config = {"name": "test", "extra_field": "value"}
        # Reason: Ruff's bug
        type_hints: Dict[str, Type[Any]] = {"name": str}  # noqa: UP006

        validations = YamlFieldValidations(config, type_hints)
        # Should not raise any exception (extra_field is ignored)
        validations.validate()


class TestValidateConfigIfNeeded:
    """Test validate_config_if_needed function for comprehensive coverage."""

    def test_validate_config_empty_type_hints(self) -> None:
        """Test with empty type hints (should return early)."""
        config = {"name": "test"}
        # Reason: Ruff's bug
        type_hints: Dict[str, Any] = {}  # noqa: UP006

        # Should not raise any exception
        validate_config_if_needed(config, type_hints)

    def test_validate_config_only_file_path(self) -> None:
        """Test with only FILE_PATH in type hints (should return early)."""
        config = {"name": "test"}
        type_hints = {"FILE_PATH": str}

        # Should not raise any exception
        validate_config_if_needed(config, type_hints)

    def test_validate_config_with_validation_errors(self) -> None:
        """Test with validation errors (should raise ExceptionGroup)."""
        config = {"name": 123}
        type_hints = {"name": str}

        with pytest.raises(ExceptionGroup):
            validate_config_if_needed(config, type_hints)

    def test_validate_config_valid_fields(self) -> None:
        """Test with valid fields."""
        config = {"name": "test", "age": 25}
        type_hints = {"name": str, "age": int, "FILE_PATH": str}

        # Should not raise any exception
        validate_config_if_needed(config, type_hints)
