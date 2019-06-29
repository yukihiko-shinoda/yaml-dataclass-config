#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABCMeta
from dataclasses import dataclass
from pathlib import Path

import yaml
from dataclasses_json import DataClassJsonMixin

from yamldataclassconfig import build_file_path


@dataclass
class YamlDataClassConfig(DataClassJsonMixin, metaclass=ABCMeta):
    """This class implements configuration wrapping."""
    # dictionary_part_config: Dict[AbstractPartKey, Type[PartConfig]]
    FILE_PATH: Path = build_file_path('config.yml')

    def load(self):
        """
        This method creates instance by dict.
        Why doesn't load when __init__ is to make the following requirements compatible:
        1. Access config as global
        2. Independent on config for development or use config for test when test
        """
        with self.FILE_PATH.open('r', encoding='UTF-8') as yml:
            dictionary_config = yaml.full_load(yml)
        self.__dict__.update(self.__class__.schema().load(dictionary_config).__dict__)
