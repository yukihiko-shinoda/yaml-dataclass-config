"""Tests for YamlDataClassConfig."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
from typing import Type
from typing import Union

import pytest
from dataclasses_json import DataClassJsonMixin
from marshmallow import ValidationError

from tests.conftest import DataClassConfigA
from tests.conftest import DataClassConfigB
from tests.conftest import PartConfigA
from tests.conftest import create_metadata_dataclasses_json_datetime
from yamldataclassconfig.config import YamlDataClassConfig

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class PartConfig(DataClassJsonMixin):
    """For test."""

    property_c: datetime = field(metadata=create_metadata_dataclasses_json_datetime())


@dataclass
class DataClassConfigSuccess(YamlDataClassConfig):
    """For test."""

    part_config: PartConfig = field(metadata={"dataclasses_json": {"mm_field": PartConfig}})
    property_a: int
    property_b: str


@dataclass
class DataClassConfigFail(YamlDataClassConfig):
    """For test."""

    # Reason: Ruff's bug
    property_a: Optional[int] = None  # noqa: UP045
    property_b: Optional[str] = None  # noqa: UP045
    part_config_a: Optional[PartConfigA] = field(  # noqa: UP045
        default=None,
        metadata={"dataclasses_json": {"mm_field": PartConfigA}},
    )


class TestYamlDataClassConfig:
    """Tests for YamlDataClassConfig."""

    @staticmethod
    def test_config_success() -> None:
        """Int should be int.

        String should be str. Hash should be object. Datetime string should be datetime.
        """
        config = DataClassConfigSuccess.create()
        config.load()
        assert config.property_a == 1
        assert config.property_b == "2"
        # pylint: disable=no-member
        assert config.part_config is not None
        assert config.part_config.property_c == datetime(2019, 6, 25, 13, 33, 30)  # noqa: DTZ001

    def test_config_success_specify_file_path_argument(self, resource_path_root: Path) -> None:
        """Specified YAML file should be loaded."""
        config = DataClassConfigA.create()
        config.load(resource_path_root / "config_a.yml")
        self.assert_that_config_a_is_loaded(config)

    def test_config_success_specify_file_path_property(
        self,
        dataclass_config_success_specify_file_path: DataClassConfigA,
    ) -> None:
        """Specified YAML file should be loaded."""
        config = dataclass_config_success_specify_file_path.create()
        config.load()
        self.assert_that_config_a_is_loaded(config)

    @staticmethod
    def assert_that_config_a_is_loaded(config: DataClassConfigA) -> None:
        # pylint: disable=no-member
        TestYamlDataClassConfig.check_part_config_a(config, PartConfigA(property_a=1, property_b="2"))
        assert config.part_config_b is not None
        assert config.part_config_b.property_c == datetime(2019, 6, 25, 13, 33, 30)  # noqa: DTZ001

    def test_config_success_specify_absolute_file_path_argument(self, resource_path_root: Path) -> None:
        """Specified YAML file by absolute path should be loaded."""
        config = DataClassConfigB()
        config.load(resource_path_root / "config_b.yml", path_is_absolute=True)
        self.assert_that_config_b_is_loaded(config, PartConfigA(property_a=1, property_b="2"))

    def test_config_lack(self, resource_path_root: Path) -> None:
        """Specified YAML file by absolute path should be loaded."""
        config = DataClassConfigB()
        config.load(resource_path_root / "config_c.yml", path_is_absolute=True)
        self.assert_that_config_b_is_loaded(config, None)

    def test_config_success_specify_absolute_file_path_property(
        self,
        # Reason: Ruff's bug
        dataclass_config_success_specify_absolute_file_path: Type[DataClassConfigB],  # noqa: UP006
    ) -> None:
        """Specified YAML file by absolute path should be loaded."""
        config = dataclass_config_success_specify_absolute_file_path()
        config.load()
        self.assert_that_config_b_is_loaded(config, PartConfigA(property_a=1, property_b="2"))

    @classmethod
    def assert_that_config_b_is_loaded(
        cls,
        config: DataClassConfigB,
        # Reason: Ruff's bug
        expected_part_config_a: Optional[PartConfigA],  # noqa: UP045
    ) -> None:
        cls.check_part_config_a(config, expected_part_config_a)
        expected_property_c = 3
        assert config.property_c == expected_property_c
        assert config.property_d == "4"

    @staticmethod
    def check_part_config_a(
        # Reason: Ruff's bug
        config: Union[DataClassConfigA, DataClassConfigB],  # noqa: UP007
        expected_part_config_a: Optional[PartConfigA],  # noqa: UP045
    ) -> None:
        if expected_part_config_a is None:
            assert config.part_config_a is None
            return
        assert config.part_config_a is not None
        assert config.part_config_a.property_a == expected_part_config_a.property_a
        assert config.part_config_a.property_b == expected_part_config_a.property_b

    @staticmethod
    def test_config_fail() -> None:
        """ValidationError should be raised when YAML structure is different from config class structure."""
        config = DataClassConfigFail()
        with pytest.raises(ValidationError) as error:
            config.load()
        validation_error: ValidationError = error.value
        actual = ValidationError(
            {"part_config": ["Unknown field."]},
        )
        assert validation_error.messages == actual.messages
