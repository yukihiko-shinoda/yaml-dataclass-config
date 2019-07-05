"""Tests for YamlDataClassConfig."""
import os

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pytest
from dataclasses_json import DataClassJsonMixin
from marshmallow import fields, ValidationError

from myproduct import my_project
from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class PartConfig(DataClassJsonMixin):
    """for test"""
    property_c: datetime = field(metadata={'dataclasses_json': {
        'encoder': datetime.isoformat,
        'decoder': datetime.fromisoformat,
        'mm_field': fields.DateTime(format='iso')
    }})


@dataclass
class PartConfigA(DataClassJsonMixin):
    """for test"""
    property_a: int
    property_b: str


@dataclass
class PartConfigB(DataClassJsonMixin):
    """for test"""
    property_c: datetime = field(metadata={'dataclasses_json': {
        'encoder': datetime.isoformat,
        'decoder': datetime.fromisoformat,
        'mm_field': fields.DateTime(format='iso')
    }})


@dataclass
class DataClassConfigSuccess(YamlDataClassConfig):
    """for test"""
    property_a: int = None
    property_b: str = None
    part_config: PartConfig = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfig}}
    )


@dataclass
class DataClassConfigSuccessSpecifyFilePath(YamlDataClassConfig):
    """for test"""
    FILE_PATH: Path = create_file_path_field('testconfigsuccessspecifyfilepath/config.yml')

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
    """for test"""
    property_a: int = None
    property_b: str = None
    part_config_a: PartConfigA = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigA}}
    )


@dataclass
class DataClassConfigSuccessSpecifyAbsoluteFilePath(YamlDataClassConfig):
    """for test"""
    FILE_PATH: Path = create_file_path_field(
        Path(os.getcwd()) / 'testconfigsuccessspecifyabsolutefilepath/config.yml',
        True
    )

    part_config_a: PartConfigA = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfigA}}
    )
    property_c: int = None
    property_d: str = None


class TestYamlDataClassConfig:
    """Tests for YamlDataClassConfig."""
    @staticmethod
    def test_scenario_readme(capsys):
        """Values on YAML file should be printed."""
        my_project.main()
        captured = capsys.readouterr()
        assert captured.out == '''1
2
2019-06-25 13:33:30
'''

    @staticmethod
    def test_config_success():
        """
        Int should be int.
        String should be str.
        Hash should be object.
        Datetime string should be datetime.
        """
        config = DataClassConfigSuccess()
        config.load()
        assert config.property_a == 1
        assert config.property_b == '2'
        # pylint: disable=no-member
        assert config.part_config.property_c == datetime(2019, 6, 25, 13, 33, 30)

    @staticmethod
    def test_config_success_specify_file_path():
        """Specified YAML file should be loaded."""
        config = DataClassConfigSuccessSpecifyFilePath()
        config.load()
        # pylint: disable=no-member
        assert config.part_config_a.property_a == 1
        assert config.part_config_a.property_b == '2'
        assert config.part_config_b.property_c == datetime(2019, 6, 25, 13, 33, 30)

    @staticmethod
    def test_config_success_specify_absolute_file_path():
        """Specified YAML file by absolute path should be loaded."""
        config = DataClassConfigSuccessSpecifyAbsoluteFilePath()
        config.load()
        # pylint: disable=no-member
        assert config.part_config_a.property_a == 1
        assert config.part_config_a.property_b == '2'
        assert config.property_c == 3
        assert config.property_d == '4'

    @staticmethod
    def test_config_fail():
        """
        ValidationError should be raised when YAML structure is different from config class structure.
        """
        config = DataClassConfigFail()
        with pytest.raises(ValidationError) as error:
            config.load()
        validation_error: ValidationError = error.value
        actual = ValidationError(
            {'part_config': ['Unknown field.']},
        )
        assert validation_error.messages == actual.messages
