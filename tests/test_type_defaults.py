"""Tests for type_defaults.py."""

from __future__ import annotations

from yamldataclassconfig.type_defaults import get_default_for_type


class TestTypeDefaultsModule:
    """Test type_defaults.py for 100% coverage."""

    def test_get_default_for_type_basic_types(self) -> None:
        """Test get_default_for_type with basic types - covers lines 19-27."""
        assert get_default_for_type(int) == 0
        assert get_default_for_type(str) == ""
        assert get_default_for_type(bool) is False
        assert get_default_for_type(float) == 0.0

    def test_get_default_for_type_generic_types(self) -> None:
        """Test get_default_for_type with generic types - covers lines 29-38."""
        # These should return callable factories for mutable types
        assert get_default_for_type(list[str]) is list
        assert get_default_for_type(dict[str, int]) is dict
        assert get_default_for_type(set[str]) is set

    def test_get_default_for_type_unknown_type(self) -> None:
        """Test get_default_for_type with unknown type - covers lines 40-41."""
        assert get_default_for_type(object) is None
