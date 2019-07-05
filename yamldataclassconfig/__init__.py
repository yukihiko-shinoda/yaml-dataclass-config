#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module implements helpers to import config file writen by YAML to Python Data Classes.
"""
import os
from dataclasses import field, Field
from pathlib import Path
from typing import Union


def create_file_path_field(path: Union[Path, str], path_is_absolute: bool = False) -> Field:
    """
    This function build and return FILE_PATH on YamlDataClassConfig class
    :param path: path to YAML config file
    :param path_is_absolute: if True, use path as absolute
    :return: dataclasses.Field instance for FILE_PATH on YamlDataClassConfig class
    """
    return field(
        default=(path if path_is_absolute else Path(os.getcwd()) / path),
        init=False,
        metadata={'dataclasses_json': {'mm_field': None}}
    )
