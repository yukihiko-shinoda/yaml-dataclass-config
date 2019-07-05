from dataclasses import dataclass
from pathlib import Path

from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class Config(YamlDataClassConfig):
    some_property: str = None
    # ...

    FILE_PATH: Path = create_file_path_field(Path(__file__).parent.parent / 'config.yml')
