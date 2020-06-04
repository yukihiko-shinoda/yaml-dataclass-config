"""Tests for __init__ module."""
import os
from pathlib import Path
from typing import Union

import pytest  # type: ignore

from yamldataclassconfig import build_path


class TestFunctions:
    """Tests for functions."""

    @staticmethod
    def test_create_file_path_field():
        """TODO """

    @staticmethod
    @pytest.mark.parametrize(
        "argument, expected",
        [
            ("config.yml", Path(os.getcwd()) / "config.yml"),
            ("config_a.yml", Path(os.getcwd()) / "config_a.yml"),
            ("../config.yml", Path(os.getcwd()) / "../config.yml"),
            ("../config_a.yml", Path(os.getcwd()) / "../config_a.yml"),
            (Path("config.yml"), Path(os.getcwd()) / "config.yml"),
            (Path("config_a.yml"), Path(os.getcwd()) / "config_a.yml"),
            (Path("../config.yml"), Path(os.getcwd()) / "../config.yml"),
            (Path("../config_a.yml"), Path(os.getcwd()) / "../config_a.yml"),
        ],
    )
    def test_build_path_relative(argument: Union[Path, str], expected: Path):
        """Function should return Path object by argument as relative path."""
        assert build_path(argument) == expected

    @staticmethod
    @pytest.mark.parametrize(
        "argument, expected",
        [
            (f"{os.getcwd()}/config.yml", Path(os.getcwd()) / "config.yml"),
            (f"{os.getcwd()}/config_a.yml", Path(os.getcwd()) / "config_a.yml"),
            (f"{os.getcwd()}/../config.yml", Path(os.getcwd()) / "../config.yml"),
            (f"{os.getcwd()}/../config_a.yml", Path(os.getcwd()) / "../config_a.yml"),
            (Path(os.getcwd()) / "config.yml", Path(os.getcwd()) / "config.yml"),
            (Path(os.getcwd()) / "config_a.yml", Path(os.getcwd()) / "config_a.yml"),
            (Path(os.getcwd()) / "../config.yml", Path(os.getcwd()) / "../config.yml"),
            (Path(os.getcwd()) / "../config_a.yml", Path(os.getcwd()) / "../config_a.yml"),
        ],
    )
    def test_build_path_absolute(argument: Union[Path, str], expected: Path):
        """Function should return Path object by argument as absolute path."""
        assert build_path(argument, True) == expected
