from pathlib import Path
import pytest
from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder

from yourproduct import CONFIG


ConfigDeployer = DeployerFactory.create(YamlConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent))


@pytest.fixture
def yaml_config():
    ConfigDeployer.setup()
    CONFIG.load()
    yield
    ConfigDeployer.teardown()


def test_something(yaml_config):
    """test something"""
