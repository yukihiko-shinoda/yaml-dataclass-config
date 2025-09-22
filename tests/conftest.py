"""Configuration for pytest."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Generator
from typing import Optional
from typing import Type

import pytest
from dataclasses_json import DataClassJsonMixin
from marshmallow import fields

from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig.utility import build_path

collect_ignore = ["setup.py"]


@pytest.fixture
def temporary_yaml_file(content: str) -> Generator[Path, None, None]:
    """Create a temporary YAML file that gets cleaned up automatically."""
    # NamedTemporaryFile causes PermissionError in Windows:
    # - Windows environment: When reopening a file created with `NamedTemporaryFile`, a `PermissionError` occurs #Python - Qiita
    #   https://qiita.com/yuji38kwmt/items/c6f50e1fc03dafdcdda0
    with tempfile.TemporaryDirectory() as str_temp_dir:
        path = Path(str_temp_dir) / "temp.yml"
        path.write_text(content)
        yield path


@dataclass
class SimpleTestConfig(YamlDataClassConfig):
    """Simple config class for testing basic functionality."""

    name: str
    age: int


@dataclass
class MinimalTestConfig(YamlDataClassConfig):
    """Minimal config for line coverage testing."""

    simple_field: str


# Non-dataclass for testing edge cases
class NonDataclassForTesting:  # pylint: disable=too-few-public-methods
    """Regular class (not a dataclass) for testing edge cases."""

    def __init__(self) -> None:
        self.value = "test"


@dataclass
class ComplexNonConfigDataclass:  # pylint: disable=too-many-instance-attributes
    """Complex dataclass with various field types (not inheriting from YamlDataClassConfig)."""

    # Basic types
    count: int
    message: str
    enabled: bool
    score: float

    # Generic types
    items: list[str]
    mapping: dict[str, int]
    tags: set[str]

    # Fields with defaults
    optional_field: str = "default"

    # Field with default_factory
    dynamic_list: list[int] = field(default_factory=list)

    # Init=False field
    computed: str = field(init=False, default="computed")


@dataclass
class PartConfigA(DataClassJsonMixin):
    """For test."""

    property_a: int
    property_b: str


def create_metadata_dataclasses_json_datetime() -> dict[str, Any]:
    """Create metadata for datetime fields."""
    return {
        "dataclasses_json": {
            "encoder": datetime.isoformat,
            "decoder": datetime.fromisoformat,
            "mm_field": fields.DateTime(format="iso"),
        },
    }


@dataclass
class PartConfigB(DataClassJsonMixin):
    """For test."""

    property_c: datetime = field(metadata=create_metadata_dataclasses_json_datetime())


@dataclass
class DataClassConfigA(YamlDataClassConfig):
    """For test."""

    part_config_a: PartConfigA = field(metadata={"dataclasses_json": {"mm_field": PartConfigA}})
    part_config_b: PartConfigB = field(metadata={"dataclasses_json": {"mm_field": PartConfigB}})


@dataclass
class DataClassConfigB(YamlDataClassConfig):
    """For test."""

    # Reason: Ruff's bug
    part_config_a: Optional[PartConfigA] = field(  # noqa: UP045
        default=None,
        metadata={"dataclasses_json": {"mm_field": PartConfigA}},
    )
    # Reason: Ruff's bug
    property_c: Optional[int] = None  # noqa: UP045
    property_d: Optional[str] = None  # noqa: UP045


@pytest.fixture
# Reason: Ruff's bug
def dataclass_config_success_specify_absolute_file_path(resource_path_root: Path) -> Type[DataClassConfigB]:  # noqa: UP006
    """Fixture for absolute file path."""

    @dataclass
    class DataClassConfigSuccessSpecifyAbsoluteFilePath(DataClassConfigB):
        """For test."""

        FILE_PATH: str = field(
            init=False,
            default=build_path(
                resource_path_root / "config_b.yml",
                path_is_absolute=True,
            ),
        )

    return DataClassConfigSuccessSpecifyAbsoluteFilePath


@pytest.fixture
# Reason: Ruff's bug
def dataclass_config_success_specify_file_path(resource_path_root: Path) -> Type[DataClassConfigA]:  # noqa: UP006
    """Fixture for file path."""

    @dataclass
    class DataClassConfigSuccessSpecifyFilePath(DataClassConfigA):
        """For test."""

        FILE_PATH: str = field(
            init=False,
            default=build_path(resource_path_root / "config_a.yml"),
        )

    return DataClassConfigSuccessSpecifyFilePath
