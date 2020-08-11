"""This module implements abstract config class."""
from abc import ABCMeta
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union

import yaml
from dataclasses_json import DataClassJsonMixin

from yamldataclassconfig import build_path, metadata_dataclasses_json


@dataclass
class YamlDataClassConfig(DataClassJsonMixin, metaclass=ABCMeta):
    """This class implements YAML file load function."""

    # Reason: pylint bug.
    # @see https://github.com/PyCQA/pylint/issues/2698
    # pylint: disable=invalid-name
    FILE_PATH: Path = field(default=build_path("config.yml"), init=False, metadata=metadata_dataclasses_json)

    def load(self, path: Union[Path, str] = None, path_is_absolute: bool = False):
        """
        This method loads from YAML file to properties of self instance.
        Why doesn't load when __init__ is to make the following requirements compatible:
        1. Access config as global
        2. Independent on config for development or use config for unit testing when unit testing
        """
        if path is None:
            path = self.FILE_PATH
        built_path = build_path(path, path_is_absolute)
        # pylint: disable=no-member
        with built_path.open("r", encoding="UTF-8") as yml:
            dictionary_config = yaml.full_load(yml)
        self.__dict__.update(self.__class__.schema().load(dictionary_config).__dict__)
