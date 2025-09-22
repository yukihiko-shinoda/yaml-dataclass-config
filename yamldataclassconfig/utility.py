"""Utilities."""

from __future__ import annotations

from dataclasses import field
from pathlib import Path
from typing import Union

__all__ = ["build_path", "create_file_path_field"]


# Reason: Ruff's bug
def create_file_path_field(path: Union[Path, str], *, path_is_absolute: bool = False) -> str:  # noqa: UP007
    """This function build and return FILE_PATH on YamlDataClassConfig class.

    :param path: path to YAML config file
    :param path_is_absolute: if True, use path as absolute
    :return: Path (dataclasses.Field) instance for FILE_PATH on YamlDataClassConfig class.
    """
    default_path = build_path(path, path_is_absolute=path_is_absolute)
    # pylint: disable=invalid-field-call
    field_instance: str = field(default=default_path, init=False)
    return field_instance


# Reason: Ruff's bug
def build_path(path: Union[Path, str], *, path_is_absolute: bool = False) -> str:  # noqa: UP007
    """This function build Path instance from arguments and returns it.

    :param path: path
    :param path_is_absolute: if True, use path as absolute
    :return: Path instance
    """
    if not path_is_absolute:
        return str(Path.cwd() / path)
    if isinstance(path, str):
        return str(Path(path))
    return str(path)


# Reason: Ruff's bug
def resolve_path(path: Union[Path, str], *, path_is_absolute: bool = False) -> Path:  # noqa: UP007
    """Resolve the given path to an absolute Path object.

    :param path: The path to resolve.
    :param path_is_absolute: If True, the path is treated as absolute.
    :return: The resolved Path object.
    """
    if not path_is_absolute:
        return Path.cwd() / path
    if isinstance(path, str):
        return Path(path)
    return path
