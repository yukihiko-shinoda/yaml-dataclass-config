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
