from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path

from dataclasses_json import DataClassJsonMixin
from marshmallow import fields

from yamldataclassconfig import build_path
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class PartConfig(DataClassJsonMixin):
    property_c: datetime = field(
        metadata={
            "dataclasses_json": {
                "encoder": datetime.isoformat,
                "decoder": datetime.fromisoformat,
                "mm_field": fields.DateTime(format="iso"),
            },
        },
    )


@dataclass
class Config(YamlDataClassConfig):
    some_property: str
    property_a: int
    property_b: str
    part_config: PartConfig = field(metadata={"dataclasses_json": {"mm_field": PartConfig}})

    FILE_PATH: str = field(
        init=False,
        default=build_path(Path(__file__).parent / "config.yml"),
    )
