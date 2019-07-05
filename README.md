# YAML Data Class Config

This project helps you to import config file writen by YAML to
Python [Data Classes](https://docs.python.org/3/library/dataclasses.html).

## Advantage

1. Type safe import from YAML to Data Classes
2. Global access and easy unit testing

### 1. Type safe import from YAML to Data classes

When using pyyaml to import YAML, values be dict and list objects.
Using dict or list object will cause such confuses:

- Reference non exist properties for unexpected instance type
- Typo of index or key name

To prevent these confuse, one of good way is to use object as model,
and python has a good module
[Data Classes](https://docs.python.org/3/library/dataclasses.html) for this purpose.

### 2. Global access and easy unit testing

You will want to refer config as global
because it's troublesome to pass config value as argument over and over like a bucket brigade.

However, when unit testing,
if YAML file was loaded automatically on importing global definition,
you will face problem that
you can't replace config YAML file with the one for unit testing.
YAML Data Class Config can divide timings between definition global instance and
loading YAML file so you can replace YAML file for unit testing.

## Quickstart

#### 1. Install
`pip install yamldataclassconfig`

#### 2. Prepare config YAML file.

Put `config.yml`
YAML Data class Config loads `config.yml` on Python execution directory by default.

```yaml
property_a: 1
property_b: '2'
part_config:
  property_c: '2019-06-25 13:33:30'
```

#### 3. Create config class

Anywhere is OK, for example, I prefer to place on `myproduct/config.py`

```python
from dataclasses import dataclass, field
from datetime import datetime
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
    property_a: int = None
    property_b: str = None
    part_config: PartConfig = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfig}}
    )
```

### 4. Define as global

Also, anywhere is OK, for example, I prefer to place on `myproduct/__init__.py`

```python
from myproduct.config import Config

CONFIG: Config = Config()
```

### 5. Call load before reference config value

```python
from myproduct import CONFIG


def main():
    CONFIG.load()
    print(CONFIG.property_a)
    print(CONFIG.property_b)
    print(CONFIG.part_config.property_c)


if __name__ == '__main__':
    main()
```

## How do I...

### Fix path to yaml file independent on the Python execution directory?

override `FILE_PATH` property.

Ex:

```python
from dataclasses import dataclass
from pathlib import Path

from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class Config(YamlDataClassConfig):
    some_property: str = None
    # ...

    FILE_PATH: Path = create_file_path_field(Path(__file__).parent.parent / 'config.yml')
```


### Use path to YAML config file as same as production when test?

`YamlDataClassConfigHandler` can replace config.yml with tests/config.yml.dist easily.
By default, `YamlDataClassConfigHandler` works with Python execution directory as target directory.
To change this behavior,
create `YamlDataClassConfigHandler` inherited class and override `CONFIG_FILE_PATH` constant.

Case when unittest:

```python
from pathlib import Path
import unittest2 as unittest

from yamldataclassconfig.config_handler import YamlDataClassConfigHandler, ConfigFilePathBuilder

from yourproduct import CONFIG


class ConfigHandler(YamlDataClassConfigHandler):
    CONFIG_FILE_PATH = ConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent)


class ConfigurableTestCase(unittest.TestCase):
    def setUp(self):
        ConfigHandler.set_up()
        CONFIG.load()

    def doCleanups(self):
        ConfigHandler.do_cleanups()
```

Case when pytest:

```python
from pathlib import Path
import pytest

from yamldataclassconfig.config_handler import YamlDataClassConfigHandler, ConfigFilePathBuilder

from yourproduct import CONFIG


class ConfigHandler(YamlDataClassConfigHandler):
    CONFIG_FILE_PATH = ConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent)


@pytest.fixture
def yaml_config():
    ConfigHandler.set_up()
    CONFIG.load()
    yield
    ConfigHandler.do_cleanups()


def test_something(yaml_config):
    """test something"""
```

## Known issue

Dependency [dataclasses-json](https://pypi.org/project/dataclasses-json/)
depends on [marshmallow](https://pypi.org/project/marshmallow/#history) pre release version.

When you use Pipenv, use `--pre` option with command or add following lines into Pipfile:

```
[pipenv]
allow_prereleases = true
```
