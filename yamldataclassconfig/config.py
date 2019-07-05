"""This module implements abstract config class."""
from abc import ABCMeta
from dataclasses import dataclass
from pathlib import Path

import yaml
from dataclasses_json import DataClassJsonMixin

from yamldataclassconfig import create_file_path_field


@dataclass
class YamlDataClassConfig(DataClassJsonMixin, metaclass=ABCMeta):
    """This class implements YAML file load function."""
    FILE_PATH: Path = create_file_path_field('config.yml')

    def load(self):
        """
        This method loads from YAML file to properties of self instance.
        Why doesn't load when __init__ is to make the following requirements compatible:
        1. Access config as global
        2. Independent on config for development or use config for unit testing when unit testing
        """
        with self.FILE_PATH.open('r', encoding='UTF-8') as yml:
            dictionary_config = yaml.full_load(yml)
        self.__dict__.update(self.__class__.schema().load(dictionary_config).__dict__)
