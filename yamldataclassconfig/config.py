"""This module implements abstract config class."""

from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from dataclasses import field

# Reason: Following error occurs without this import:
#     self.__dict__.update(self.__class__.schema().load(dictionary_config).__dict__)  # noqa: ERA001
#                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   NameError: name 'Path' is not defined
from pathlib import Path  # noqa: TC003
from typing import Any
from typing import Self
from typing import cast
from typing import get_type_hints

import yaml
from dataclasses_json import DataClassJsonMixin

from yamldataclassconfig.config_property import create_property_descriptors
from yamldataclassconfig.factory import KeyArguments
from yamldataclassconfig.field_processor import apply_automatic_defaults
from yamldataclassconfig.utility import build_path
from yamldataclassconfig.utility import metadata_dataclasses_json
from yamldataclassconfig.validation import validate_config_if_needed

__all__ = [
    "YamlDataClassConfig",
]


@dataclass
class YamlDataClassConfig(DataClassJsonMixin, metaclass=ABCMeta):
    """This class implements YAML file load function with built-in validation."""

    # Reason: pylint bug.
    # @see https://github.com/PyCQA/pylint/issues/2698
    # pylint: disable=invalid-name
    FILE_PATH: Path = field(default=build_path("config.yml"), init=False, metadata=metadata_dataclasses_json)
    _loaded: bool = field(default=False, init=False)

    @classmethod
    def create(cls, **kwargs: Any) -> Self:  # noqa: ANN401
        """Create an instance without requiring all fields.

        This is a factory method that allows instantiation of config classes
        without providing all required fields. Values will be set when load() is called.

        Args:
            **kwargs: Optional field values to set

        Returns:
            Instance with default/placeholder values for missing fields
        """
        key_args = KeyArguments(cls, **kwargs)
        key_args.build_init_kwargs()
        return cls(**key_args.init_kwargs)

    def __init_subclass__(cls, **kwargs: Any) -> None:  # noqa: ANN401
        """Automatically add property validation and default values to subclasses."""
        super().__init_subclass__(**kwargs)

        # Automatically apply defaults to prevent mypy positional argument warnings
        apply_automatic_defaults(cls)

        # Add property descriptors for validation
        create_property_descriptors(cls)

    def load(self, path: Path | str | None = None, *, path_is_absolute: bool = False) -> None:
        """This method loads from YAML file to properties of self instance with validation.

        Why doesn't load when __init__ is to make the following requirements compatible:
        1. Access config as global
        2. Independent on config for development or use config for unit testing when unit testing
        """
        config_path = self._resolve_config_path(path, path_is_absolute=path_is_absolute)
        dictionary_config = self._load_yaml_content(config_path)

        type_hints = get_type_hints(self.__class__)
        validate_config_if_needed(dictionary_config, type_hints)

        self._load_and_apply_config(dictionary_config)

    def _resolve_config_path(self, path: Path | str | None, *, path_is_absolute: bool) -> Path:
        """Resolve the configuration file path."""
        if path is None:
            path = self.FILE_PATH
        return build_path(path, path_is_absolute=path_is_absolute)

    def _load_yaml_content(self, config_path: Path) -> dict[str, Any]:
        """Load YAML content from file."""
        return cast("dict[str, Any]", yaml.full_load(config_path.read_text(encoding="UTF-8")))

    def _load_and_apply_config(self, dictionary_config: dict[str, Any]) -> None:
        """Load configuration using marshmallow and apply to instance."""
        loaded_config = self.__class__.schema().load(dictionary_config)

        # Set loaded flag first to prevent ConfigNotLoadedError during property access
        self._loaded = True

        # Update instance with loaded values
        self.__dict__.update(loaded_config.__dict__)
