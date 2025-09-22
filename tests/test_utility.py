"""Tests to achieve 100% coverage for remaining modules."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Union

import pytest

from yamldataclassconfig import build_path
from yamldataclassconfig.utility import create_file_path_field
from yamldataclassconfig.utility import resolve_path


class TestFunctions:
    """Tests for functions."""

    @staticmethod
    def test_create_file_path_field() -> None:
        """TODO."""

    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [
            ("config.yml", Path.cwd() / "config.yml"),
            ("config_a.yml", Path.cwd() / "config_a.yml"),
            ("../config.yml", Path.cwd() / "../config.yml"),
            ("../config_a.yml", Path.cwd() / "../config_a.yml"),
            (Path("config.yml"), Path.cwd() / "config.yml"),
            (Path("config_a.yml"), Path.cwd() / "config_a.yml"),
            (Path("../config.yml"), Path.cwd() / "../config.yml"),
            (Path("../config_a.yml"), Path.cwd() / "../config_a.yml"),
        ],
    )
    # Reason: Ruff's bug
    def test_build_path_relative(argument: Union[Path, str], expected: Path) -> None:  # noqa: UP007
        """Function should return Path object by argument as relative path."""
        assert build_path(argument) == str(expected)

    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "expected"),
        [
            (f"{Path.cwd()}/config.yml", Path.cwd() / "config.yml"),
            (f"{Path.cwd()}/config_a.yml", Path.cwd() / "config_a.yml"),
            (f"{Path.cwd()}/../config.yml", Path.cwd() / "../config.yml"),
            (f"{Path.cwd()}/../config_a.yml", Path.cwd() / "../config_a.yml"),
            (Path.cwd() / "config.yml", Path.cwd() / "config.yml"),
            (Path.cwd() / "config_a.yml", Path.cwd() / "config_a.yml"),
            (Path.cwd() / "../config.yml", Path.cwd() / "../config.yml"),
            (Path.cwd() / "../config_a.yml", Path.cwd() / "../config_a.yml"),
        ],
    )
    # Reason: Ruff's bug
    def test_build_path_absolute(argument: Union[Path, str], expected: Path) -> None:  # noqa: UP007
        """Function should return Path object by argument as absolute path."""
        assert build_path(argument, path_is_absolute=True) == str(expected)


class TestUtilityCoverage:
    """Test utility.py coverage for lines 20-23."""

    def test_create_file_path_field_with_absolute_path(self) -> None:
        """Test create_file_path_field with absolute path - covers utility.py lines 20-23."""
        # This exercises the build_path call and field creation in lines 20-23
        absolute_path = str(Path("/absolute/path/config.yml"))
        field_instance = create_file_path_field(absolute_path, path_is_absolute=True)

        # Verify field was created correctly
        assert field_instance.default == absolute_path  # type: ignore[attr-defined]
        assert field_instance.init is False  # type: ignore[attr-defined]
        assert field_instance.metadata is not None  # type: ignore[attr-defined]

    def test_create_file_path_field_with_relative_path(self) -> None:
        """Test create_file_path_field with relative path."""
        relative_path = "relative/config.yml"
        field_instance = create_file_path_field(relative_path, path_is_absolute=False)

        # Verify field was created correctly
        assert isinstance(field_instance.default, str)  # type: ignore[attr-defined]
        assert field_instance.init is False  # type: ignore[attr-defined]
        assert field_instance.metadata is not None  # type: ignore[attr-defined]


class TestResolvePath:
    """Test resolve_path function for missing coverage."""

    def test_resolve_path_absolute_string(self) -> None:
        """Test resolve_path with absolute string path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            absolute_path = f"{temp_dir}/config.yml"
            result = resolve_path(absolute_path, path_is_absolute=True)

            assert result == Path(absolute_path)
            assert isinstance(result, Path)

    def test_resolve_path_absolute_path_object(self) -> None:
        """Test resolve_path with absolute Path object."""
        with tempfile.TemporaryDirectory() as temp_dir:
            absolute_path = Path(temp_dir) / "config.yml"
            result = resolve_path(absolute_path, path_is_absolute=True)

            assert result == absolute_path
            assert isinstance(result, Path)

    def test_resolve_path_relative(self) -> None:
        """Test resolve_path with relative path (already covered but for completeness)."""
        relative_path = "config.yml"
        result = resolve_path(relative_path, path_is_absolute=False)

        expected = Path.cwd() / relative_path
        assert result == expected
        assert isinstance(result, Path)
