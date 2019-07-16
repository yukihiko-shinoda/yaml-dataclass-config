from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import DataClassJsonMixin
from marshmallow import fields
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class PartConfig(DataClassJsonMixin):
    property_c: datetime = field(metadata={'dataclasses_json': {
        'encoder': datetime.isoformat,
        'decoder': datetime.fromisoformat,
        'mm_field': fields.DateTime(format='iso')
    }})


@dataclass
class Config(YamlDataClassConfig):
    property_a: Optional[int] = None
    property_b: Optional[str] = None
    part_config: Optional[PartConfig] = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfig}}
    )
