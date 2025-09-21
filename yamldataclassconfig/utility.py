"""Utilities."""

from __future__ import annotations

from dataclasses import field
from pathlib import Path

__all__ = ["build_path", "create_file_path_field", "metadata_dataclasses_json"]

metadata_dataclasses_json = {"dataclasses_json": {"mm_field": Path}}


def create_file_path_field(path: Path | str, *, path_is_absolute: bool = False) -> Path:
    """This function build and return FILE_PATH on YamlDataClassConfig class.

    :param path: path to YAML config file
    :param path_is_absolute: if True, use path as absolute
    :return: Path (dataclasses.Field) instance for FILE_PATH on YamlDataClassConfig class.
    """
    default_path = build_path(path, path_is_absolute=path_is_absolute)
    # pylint: disable=invalid-field-call
    field_instance: Path = field(default=default_path, init=False, metadata=metadata_dataclasses_json)
    return field_instance


def build_path(path: Path | str, *, path_is_absolute: bool = False) -> Path:
    """This function build Path instance from arguments and returns it.

    :param path: path
    :param path_is_absolute: if True, use path as absolute
    :return: Path instance
    """
    if not path_is_absolute:
        return Path.cwd() / path
    if isinstance(path, str):
        return Path(path)
    return path
