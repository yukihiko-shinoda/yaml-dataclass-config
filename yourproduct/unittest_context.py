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
