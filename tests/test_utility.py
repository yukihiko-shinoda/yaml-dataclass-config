"""Tests to achieve 100% coverage for remaining modules."""

from __future__ import annotations

from pathlib import Path

import pytest

from yamldataclassconfig import build_path
from yamldataclassconfig.utility import create_file_path_field


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
    def test_build_path_relative(argument: Path | str, expected: Path) -> None:
        """Function should return Path object by argument as relative path."""
        assert build_path(argument) == expected

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
    def test_build_path_absolute(argument: Path | str, expected: Path) -> None:
        """Function should return Path object by argument as absolute path."""
        assert build_path(argument, path_is_absolute=True) == expected


class TestUtilityCoverage:
    """Test utility.py coverage for lines 20-23."""

    def test_create_file_path_field_with_absolute_path(self) -> None:
        """Test create_file_path_field with absolute path - covers utility.py lines 20-23."""
        # This exercises the build_path call and field creation in lines 20-23
        absolute_path = "/absolute/path/config.yml"
        field_instance = create_file_path_field(absolute_path, path_is_absolute=True)

        # Verify field was created correctly
        assert field_instance.default == Path(absolute_path)  # type: ignore[attr-defined]
        assert field_instance.init is False  # type: ignore[attr-defined]
        assert field_instance.metadata is not None  # type: ignore[attr-defined]

    def test_create_file_path_field_with_relative_path(self) -> None:
        """Test create_file_path_field with relative path."""
        relative_path = "relative/config.yml"
        field_instance = create_file_path_field(relative_path, path_is_absolute=False)

        # Verify field was created correctly
        assert isinstance(field_instance.default, Path)  # type: ignore[attr-defined]
        assert field_instance.init is False  # type: ignore[attr-defined]
        assert field_instance.metadata is not None  # type: ignore[attr-defined]
