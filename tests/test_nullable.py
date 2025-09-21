"""Tests for yamldataclassconfig.nullable module."""

from __future__ import annotations

import sys
from typing import Union

import pytest

from yamldataclassconfig.nullable import is_nullable_type


class TestIsNullableType:
    """Test is_nullable_type function."""

    def test_is_nullable_type_union_with_none(self) -> None:
        """Test is_nullable_type returns True for Union with None."""
        result = is_nullable_type(Union[str, None])
        assert result is True

    def test_is_nullable_type_union_without_none(self) -> None:
        """Test is_nullable_type returns False for Union without None."""
        result = is_nullable_type(Union[str, int])
        assert result is False

    def test_is_nullable_type_simple_type(self) -> None:
        """Test is_nullable_type returns False for simple type."""
        result = is_nullable_type(str)
        assert result is False

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
    def test_is_nullable_type_modern_union_with_none(self) -> None:
        """Test is_nullable_type returns True for modern union syntax with None."""
        # Use eval to create the union type to avoid syntax errors on older Python
        union_type = eval("str | None")  # pylint: disable=eval-used
        result = is_nullable_type(union_type)
        assert result is True

    @pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
    def test_is_nullable_type_modern_union_without_none(self) -> None:
        """Test is_nullable_type returns False for modern union syntax without None."""
        # Use eval to create the union type to avoid syntax errors on older Python
        union_type = eval("str | int")  # pylint: disable=eval-used
        result = is_nullable_type(union_type)
        assert result is False
