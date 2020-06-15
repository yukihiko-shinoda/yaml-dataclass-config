"""This module implements helpers to import config file writen by YAML to Python Data Classes."""
import os
from dataclasses import field
from pathlib import Path
from typing import Union

__version__ = "1.3.4"


def create_file_path_field(path: Union[Path, str], path_is_absolute: bool = False) -> Path:
    """
    This function build and return FILE_PATH on YamlDataClassConfig class
    :param path: path to YAML config file
    :param path_is_absolute: if True, use path as absolute
    :return: Path (dataclasses.Field) instance for FILE_PATH on YamlDataClassConfig class
    """
    default_path = build_path(path, path_is_absolute)
    # noinspection Mypy
    field_instance: Path = field(default=default_path, init=False, metadata={"dataclasses_json": {"mm_field": Path}})
    return field_instance


def build_path(path: Union[Path, str], path_is_absolute: bool = False) -> Path:
    """
    This function build Path instance from arguments and returns it.
    :param path: path
    :param path_is_absolute: if True, use path as absolute
    :return: Path instance
    """
    if not path_is_absolute:
        return Path(os.getcwd()) / path
    if isinstance(path, str):
        return Path(path)
    return path
