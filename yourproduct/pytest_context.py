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
