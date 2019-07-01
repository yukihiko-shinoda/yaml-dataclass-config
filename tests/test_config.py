import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pytest
from dataclasses_json import DataClassJsonMixin
from marshmallow import fields, ValidationError

from yamldataclassconfig import build_file_path
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class PartConfigA(DataClassJsonMixin):
    variable_a: int
    variable_b: str


@dataclass
class PartConfigB(DataClassJsonMixin):
    variable_c: datetime = field(metadata={'dataclasses_json': {
        'encoder': datetime.isoformat,
        'decoder': datetime.fromisoformat,
        'mm_field': fields.DateTime(format='iso')
    }})


@dataclass
class DataClassConfigSuccess(YamlDataClassConfig):
    part_config_a: PartConfigA = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigA}}
    )
    part_config_b: PartConfigB = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigB}}
    )


@dataclass
class DataClassConfigSuccessSpecifyFilePath(YamlDataClassConfig):
    FILE_PATH: Path = build_file_path('testconfigsuccessspecifyfilepath/config.yml')

    part_config_a: PartConfigA = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigA}}
    )
    part_config_b: PartConfigB = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigB}}
    )


@dataclass
class DataClassConfigFail(YamlDataClassConfig):
    part_config_a: PartConfigA = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigA}}
    )


@dataclass
class DataClassConfigSuccessSpecifyAbsoluteFilePath(YamlDataClassConfig):
    FILE_PATH: Path = build_file_path(Path(os.getcwd()) / 'testconfigsuccessspecifyabsolutefilepath/config.yml', True)

    part_config_a: PartConfigA = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigA}}
    )
    part_config_b: PartConfigB = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigB}}
    )


class TestYamlDataClassConfig:
    def test_config_success(self):
        # noinspection PyPep8Naming
        CONFIG = DataClassConfigSuccess()
        CONFIG.load()
        assert CONFIG.part_config_a.variable_a == 1
        assert CONFIG.part_config_a.variable_b == '2'
        assert CONFIG.part_config_b.variable_c == datetime(2019, 6, 25, 13, 33, 30)

    def test_config_success_specify_file_path(self):
        # noinspection PyPep8Naming
        CONFIG = DataClassConfigSuccessSpecifyFilePath()
        CONFIG.load()
        assert CONFIG.part_config_a.variable_a == 1
        assert CONFIG.part_config_a.variable_b == '2'
        assert CONFIG.part_config_b.variable_c == datetime(2019, 6, 25, 13, 33, 30)

    def test_config_success_specify_absolute_file_path(self):
        # noinspection PyPep8Naming
        CONFIG = DataClassConfigSuccessSpecifyAbsoluteFilePath()
        CONFIG.load()
        assert CONFIG.part_config_a.variable_a == 1
        assert CONFIG.part_config_a.variable_b == '2'
        assert CONFIG.part_config_b.variable_c == datetime(2019, 6, 25, 13, 33, 30)

    def test_config_fail(self):
        # noinspection PyPep8Naming
        CONFIG = DataClassConfigFail()
        with pytest.raises(ValidationError) as error:
            CONFIG.load()
        validation_error: ValidationError = error.value
        actual = ValidationError(
            {'part_config_b': ['Unknown field.']},
        )
        assert validation_error.messages == actual.messages
