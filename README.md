# YAML Data Class Config

[![Test](https://github.com/yukihiko-shinoda/yaml-dataclass-config/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/yaml-dataclass-config/actions?query=workflow%3ATest)
[![CodeQL](https://github.com/yukihiko-shinoda/yaml-dataclass-config/workflows/CodeQL/badge.svg)](https://github.com/yukihiko-shinoda/yaml-dataclass-config/actions?query=workflow%3ACodeQL)
[![Code Coverage](https://qlty.sh/gh/yukihiko-shinoda/projects/yaml-dataclass-config/coverage.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/yaml-dataclass-config)
[![Maintainability](https://qlty.sh/gh/yukihiko-shinoda/projects/yaml-dataclass-config/maintainability.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/yaml-dataclass-config)
[![Dependabot](https://flat.badgen.net/github/dependabot/yukihiko-shinoda/yaml-dataclass-config?icon=dependabot)](https://github.com/yukihiko-shinoda/yaml-dataclass-config/security/dependabot)
[![Python versions](https://img.shields.io/pypi/pyversions/yamldataclassconfig)](https://pypi.org/project/yamldataclassconfig/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/yamldataclassconfig)](https://pypi.org/project/yamldataclassconfig/)
[![X URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Fyaml-dataclass-config)](https://x.com/intent/post?text=YAML%20Data%20Class%20Config&url=https%3A%2F%2Fpypi.org%2Fproject%2Fyamldataclassconfig%2F&hashtags=python)

This project helps you to import config file writen by YAML to
Python [Data Classes](https://docs.python.org/3/library/dataclasses.html).

## 📖 Migration Guide

Upgrading from version 1.x? See the [Migration Guide](docs/migration-1-to-2.md) for step-by-step instructions to migrate to version 2.x.

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

## Modern Python Features

This library leverages modern Python features for better type safety and developer experience:

- **Modern Union Syntax**: Uses `str | None` instead of `Union[str, None]` (Python 3.10+)
- **Future Annotations**: Uses `from __future__ import annotations` for improved type hint evaluation
- **Keyword-Only Arguments**: Functions use `*` to enforce keyword-only arguments for better API clarity
- **Type Safety**: Full mypy compliance with strict mode enabled
- **Runtime Type Checking**: Proper handling of type annotations at runtime for dataclass serialization

## Quickstart

### 1. Install

```console
pip install yamldataclassconfig
```

### 2. Prepare config YAML file

Put `config.yml`
YAML Data class Config loads `config.yml` on Python execution directory by default.

```yaml
property_a: 1
property_b: '2'
part_config:
  property_c: '2019-06-25 13:33:30'
```

### 3. Create config class

Anywhere is OK, for example, I prefer to place on `myproduct/config.py`

```python
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from dataclasses_json import DataClassJsonMixin
from marshmallow import fields

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
    property_a: int
    property_b: str
    part_config: PartConfig = field(
        metadata={"dataclasses_json": {"mm_field": PartConfig}},
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


def main() -> None:
    CONFIG.load()
    print(CONFIG.property_a)
    print(CONFIG.property_b)
    if CONFIG.part_config is not None:
        print(CONFIG.part_config.property_c)


if __name__ == '__main__':
    main()
```

<!-- markdownlint-disable no-trailing-punctuation -->
## How do I...
<!-- markdownlint-enable no-trailing-punctuation -->

<!-- markdownlint-disable no-trailing-punctuation -->
### Fix path to yaml file independent on the Python execution directory?
<!-- markdownlint-enable no-trailing-punctuation -->

override `FILE_PATH` property.

Ex:

```python
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from yamldataclassconfig import build_path
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class Config(YamlDataClassConfig):
    some_property: str
    # ...

    FILE_PATH: str = field(
        init=False,
        default=build_path(Path(__file__).parent / "config.yml"),
    )
```

<!-- markdownlint-disable no-trailing-punctuation -->
### Switch target YAML config file to the one for unit testing?
<!-- markdownlint-enable no-trailing-punctuation -->

When setup on unit testing, you can call `Config.load()` with argument.

**Note**: The `path_is_absolute` parameter must now be passed as a keyword argument due to API improvements in version 1.5.0.

Case when unittest:

```python
from pathlib import Path
import unittest

from yourproduct import CONFIG

class ConfigurableTestCase(unittest.TestCase):
    def setUp(self) -> None:
        CONFIG.load(Path('path/to/yaml'))
```

Case when pytest:

```python
from pathlib import Path
from typing import Generator

import pytest

from yourproduct import CONFIG

@pytest.fixture
def yaml_config() -> Generator[None, None, None]:
    CONFIG.load(Path('path/to/yaml'))
    yield

def test_something(yaml_config: None) -> None:
    """test something"""
```

<!-- markdownlint-disable no-trailing-punctuation -->
### Use path to YAML config file as same as production when test?
<!-- markdownlint-enable no-trailing-punctuation -->

[fixturefilehandler](https://pypi.org/project/fixturefilehandler/)
can replace config.yml with tests/config.yml.dist easily.
Please call all `DeployerFactory.create` with `YamlConfigFilePathBuilder` instance argument
to create ConfigDeployer.
Then, set target directory which config.yml should be placed into `path_target_directory`.

Case when unittest:

```python
from pathlib import Path
import unittest

from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder

from yourproduct import CONFIG


ConfigDeployer = DeployerFactory.create(YamlConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent))


class ConfigurableTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ConfigDeployer.setup()
        CONFIG.load()

    def doCleanups(self) -> None:
        ConfigDeployer.teardown()
```

Case when pytest:

```python
from pathlib import Path
from typing import Generator

import pytest
from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder

from yourproduct import CONFIG


ConfigDeployer = DeployerFactory.create(YamlConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent))


@pytest.fixture
def yaml_config() -> Generator[None, None, None]:
    ConfigDeployer.setup()
    CONFIG.load()
    yield
    ConfigDeployer.teardown()


def test_something(yaml_config: None) -> None:
    """test something"""
```
