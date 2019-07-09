from pathlib import Path
import unittest2 as unittest
from fixturefilehandler.factories import DeployerFactory
from fixturefilehandler.file_paths import YamlConfigFilePathBuilder

from yourproduct import CONFIG


ConfigDeployer = DeployerFactory.create(YamlConfigFilePathBuilder(path_target_directory=Path(__file__).parent.parent))


class ConfigurableTestCase(unittest.TestCase):
    def setUp(self):
        ConfigDeployer.setup()
        CONFIG.load()

    def doCleanups(self):
        ConfigDeployer.teardown()
