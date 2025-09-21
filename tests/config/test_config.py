"""Tests for YamlDataClassConfig."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING

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

    property_a: int | None = None
    property_b: str | None = None
    part_config_a: PartConfigA | None = field(
        default=None,
        metadata={"dataclasses_json": {"mm_field": PartConfigA}},
    )

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
        DataClassConfigFail.check_part_config_a(config)
        assert config.part_config_b is not None
        assert config.part_config_b.property_c == datetime(2019, 6, 25, 13, 33, 30)  # noqa: DTZ001

    def test_config_success_specify_absolute_file_path_argument(self, resource_path_root: Path) -> None:
        """Specified YAML file by absolute path should be loaded."""
        config = DataClassConfigB()
        config.load(resource_path_root / "config_b.yml", path_is_absolute=True)
        self.assert_that_config_b_is_loaded(config)

    def test_config_success_specify_absolute_file_path_property(
        self,
        dataclass_config_success_specify_absolute_file_path: type[DataClassConfigB],
    ) -> None:
        """Specified YAML file by absolute path should be loaded."""
        config = dataclass_config_success_specify_absolute_file_path()
        config.load()
        self.assert_that_config_b_is_loaded(config)

    @staticmethod
    def assert_that_config_b_is_loaded(config: DataClassConfigB) -> None:
        # pylint: disable=no-member
        DataClassConfigFail.check_part_config_a(config)
        expected_property_c = 3
        assert config.property_c == expected_property_c
        assert config.property_d == "4"

    @staticmethod
    def check_part_config_a(config: DataClassConfigA | DataClassConfigB) -> None:
        assert config.part_config_a is not None
        assert config.part_config_a.property_a == 1
        assert config.part_config_a.property_b == "2"

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
