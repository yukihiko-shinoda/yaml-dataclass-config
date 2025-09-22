"""Tests for factory.py."""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Set

from tests.conftest import ComplexNonConfigDataclass
from tests.conftest import NonDataclassForTesting
from tests.conftest import SimpleTestConfig
from yamldataclassconfig.factory import KeyArguments
from yamldataclassconfig.factory import _get_type_default


class TestFactoryModule:
    """Test factory.py for 100% coverage."""

    def test_get_type_default_basic_types(self) -> None:
        """Test _get_type_default with basic types - covers lines 17-25."""
        assert _get_type_default(int) == 0
        assert _get_type_default(str) == ""
        assert _get_type_default(bool) is False
        assert _get_type_default(float) == 0.0

    def test_get_type_default_generic_types(self) -> None:
        """Test _get_type_default with generic types - covers lines 27-35."""
        assert _get_type_default(List[str]) == []
        assert _get_type_default(Dict[str, int]) == {}
        assert _get_type_default(Set[str]) == set()

    def test_get_type_default_unknown_type(self) -> None:
        """Test _get_type_default with unknown type - covers line 37."""
        assert _get_type_default(object) is None

    def test_key_arguments_non_dataclass(self) -> None:
        """Test KeyArguments with non-dataclass - covers line 53."""
        key_args = KeyArguments(NonDataclassForTesting)
        key_args.build_init_kwargs()
        # Should return early without building kwargs
        assert key_args.init_kwargs == {}  # pylint: disable=use-implicit-booleaness-not-comparison

    def test_key_arguments_with_user_provided_kwargs(self) -> None:
        """Test KeyArguments.get_kwarg when field_name in kwargs - covers line 64."""
        expected_age = 30
        key_args = KeyArguments(SimpleTestConfig, name="provided_name", age=expected_age)
        key_args.build_init_kwargs()

        # Should use provided kwargs
        assert key_args.init_kwargs["name"] == "provided_name"
        assert key_args.init_kwargs["age"] == expected_age

    def test_key_arguments_with_default_factory(self) -> None:
        """Test KeyArguments.get_kwarg with default_factory - covers lines 67-68."""
        key_args = KeyArguments(ComplexNonConfigDataclass)
        # Pylint's bug: doesn't recognize __dataclass_fields__ on dataclasses
        field_obj = ComplexNonConfigDataclass.__dataclass_fields__["dynamic_list"]  # pylint: disable=no-member
        result = key_args.get_kwarg("dynamic_list", field_obj)

        # Should use default_factory result
        assert result == []

    def test_key_arguments_with_type_default(self) -> None:
        """Test KeyArguments.get_kwarg falling back to type default - covers lines 70-73."""
        key_args = KeyArguments(ComplexNonConfigDataclass)

        # Test field without default or default_factory
        # Pylint's bug: doesn't recognize __dataclass_fields__ on dataclasses
        field_obj = ComplexNonConfigDataclass.__dataclass_fields__["count"]  # pylint: disable=no-member
        result = key_args.get_kwarg("count", field_obj)
        assert result == 0  # int default

        # Pylint's bug: doesn't recognize __dataclass_fields__ on dataclasses
        field_obj = ComplexNonConfigDataclass.__dataclass_fields__["message"]  # pylint: disable=no-member
        result = key_args.get_kwarg("message", field_obj)
        assert result == ""  # str default

    def test_key_arguments_no_field_type(self) -> None:
        """Test KeyArguments.get_kwarg with no field type - covers line 73."""
        # Create KeyArguments without type hints for the field
        key_args = KeyArguments(ComplexNonConfigDataclass)
        key_args.type_hints = {}  # Remove type hints

        # Pylint's bug: doesn't recognize __dataclass_fields__ on dataclasses
        field_obj = ComplexNonConfigDataclass.__dataclass_fields__["count"]  # pylint: disable=no-member
        result = key_args.get_kwarg("count", field_obj)
        assert result is None  # Should return None when no type hint
