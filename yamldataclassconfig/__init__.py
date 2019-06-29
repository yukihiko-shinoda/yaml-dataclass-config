#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from dataclasses import field
from pathlib import Path
from typing import Union


def build_file_path(path: Union[Path, str]):
    return field(
        default=Path(os.getcwd()) / path,
        init=False,
        metadata={'dataclasses_json': {'mm_field': None}}
    )
