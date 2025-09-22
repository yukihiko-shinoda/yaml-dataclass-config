"""Tests for field_processor.py."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Dict

import pytest

from tests.conftest import NonDataclassForTesting
from yamldataclassconfig.field_processor import DataClass
from yamldataclassconfig.field_processor import TypeHint
from yamldataclassconfig.field_processor import apply_automatic_defaults


class TestFieldProcessorModule:
    """Test field_processor.py for 100% coverage."""

    def test_type_hint_init(self) -> None:
        """Test TypeHint.__init__ - covers lines 22-24."""
        type_hints = {"name": str, "age": int}
        hint = TypeHint(type_hints, "name")

        assert hint.field_name == "name"
        assert hint.field_type is str
        assert hint.default is None

    def test_type_hint_no_field_type(self) -> None:
        """Test TypeHint.try_to_get_default_value with missing field type - covers lines 27-28."""
        # Reason: Ruff's bug
        type_hints: Dict[str, Any] = {}  # noqa: UP006
        hint = TypeHint(type_hints, "unknown_field")

        result = hint.try_to_get_default_value()
        assert result is False

    def test_type_hint_try_to_get_default_value_success(self) -> None:
        """Test TypeHint.try_to_get_default_value success path - covers lines 29-30."""
        type_hints = {"count": int}
        hint = TypeHint(type_hints, "count")

        result = hint.try_to_get_default_value()
        assert result is True
        assert hint.default == 0

    def test_type_hint_get_automatic_default(self) -> None:
        """Test TypeHint.get_automatic_default - covers lines 33-35."""
        type_hints = {"message": str}
        hint = TypeHint(type_hints, "message")
        hint.try_to_get_default_value()

        field_obj = hint.get_automatic_default()
        assert field_obj.default == ""

    def test_apply_automatic_defaults_direct_call(self) -> None:
        """Test apply_automatic_defaults function directly - covers line 75."""

        @dataclass
        class TestClass:
            # This will test the processor
            basic_field: str
            numeric_field: int

        # Apply automatic defaults
        apply_automatic_defaults(TestClass)

        # Verify that the fields now have defaults
        # Pylint's bug: doesn't recognize __dataclass_fields__ on dataclasses
        basic_field = TestClass.__dataclass_fields__["basic_field"]  # pylint: disable=no-member
        numeric_field = TestClass.__dataclass_fields__["numeric_field"]  # pylint: disable=no-member

        # Fields should now have defaults
        assert basic_field.default == ""
        assert numeric_field.default == 0

    def test_data_class_non_dataclass(self) -> None:
        """Test DataClass constructor with non-dataclass - covers lines 47-48."""
        # This should raise ValueError for non-dataclass
        with pytest.raises(ValueError, match="Provided class is not a dataclass"):
            DataClass(NonDataclassForTesting)
