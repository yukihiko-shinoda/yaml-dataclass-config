"""Tests for YamlDataClassConfigHandler."""
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from yamldataclassconfig.config_handler import YamlDataClassConfigHandler, ConfigFilePathInterface,\
    ConfigFilePathBuilder

PATH_REFERENCE_DIRECTORY_EXAMPLE = Path(__file__).parent / 'testsetupcasetargetoverridepathcurrentdirectory'


class PathOverWrittenYamlDataClassConfigHandler(YamlDataClassConfigHandler):
    """for test"""
    CONFIG_FILE_PATH: ConfigFilePathInterface = ConfigFilePathBuilder(
        path_target_directory=PATH_REFERENCE_DIRECTORY_EXAMPLE
    )


@dataclass
class ConfigFilePathBuilderForTest:
    """This class builds file path for config file."""
    path_reference_directory: Path = Path(os.getcwd())
    file_target: Path = 'config.yml'
    file_backup: Path = 'config.yml.bak'
    file_backup_for_test: Path = 'config.yml.test.bak'

    @property
    def target(self) -> Path:
        """This method return path to target file"""
        return self.path_reference_directory / self.file_target

    @property
    def backup(self) -> Path:
        """This method return path to backup file"""
        return self.path_reference_directory / self.file_backup

    @property
    def backup_for_test(self) -> Path:
        """This method return path to backup file for test"""
        return self.path_reference_directory / self.file_backup_for_test


class TestConfigFilePathBuilder:
    """Tests for ConfigFilePathBuilder."""
    @staticmethod
    def test_config_file_path_builder_default():
        """Each property returns appropriate path based on python execution directory."""
        config_path_builder = ConfigFilePathBuilder()
        assert config_path_builder.source == Path(os.getcwd()) / 'tests' / 'config.yml.dist'
        assert config_path_builder.target == Path(os.getcwd()) / 'config.yml'
        assert config_path_builder.backup == Path(os.getcwd()) / 'config.yml.bak'

    @staticmethod
    def test_config_file_path_builder_specify_target_directory():
        """Each property returns appropriate path based on specific directory."""
        config_path_builder = ConfigFilePathBuilder(path_target_directory=Path(__file__))
        assert config_path_builder.source == Path(__file__) / 'tests' / 'config.yml.dist'
        assert config_path_builder.target == Path(__file__) / 'config.yml'
        assert config_path_builder.backup == Path(__file__) / 'config.yml.bak'


class TestYamlDataClassConfigHandler:
    """Tests for YamlDataClassConfigHandler."""
    CONFIG_FILE_PATH = ConfigFilePathBuilderForTest()
    OVERRIDE_CONFIG_FILE_PATH = ConfigFilePathBuilderForTest(path_reference_directory=PATH_REFERENCE_DIRECTORY_EXAMPLE)

    def setup_method(self):
        """This method evacuate target file and clean up backup file."""
        if self.CONFIG_FILE_PATH.target.is_file():
            shutil.move(str(self.CONFIG_FILE_PATH.target), str(self.CONFIG_FILE_PATH.backup_for_test))
        if self.CONFIG_FILE_PATH.backup.exists():
            os.unlink(str(self.CONFIG_FILE_PATH.backup))

    def teardown_method(self):
        """This method rolls back target file with backup file."""
        if not self.CONFIG_FILE_PATH.backup_for_test.is_file():
            return
        if self.CONFIG_FILE_PATH.target.is_file():
            os.unlink(str(self.CONFIG_FILE_PATH.target))
        shutil.move(str(self.CONFIG_FILE_PATH.backup_for_test), str(self.CONFIG_FILE_PATH.target))

    def test_set_up_case_target_file_exists(self):
        """
        Target file should back up.
        Target file should replace with source file.
        """
        file_content_target_file = self._create_target_file()
        YamlDataClassConfigHandler.set_up()
        with self.CONFIG_FILE_PATH.backup.open('r') as file_backup:
            assert file_backup.read() == file_content_target_file
        with self.CONFIG_FILE_PATH.target.open('r') as file_target:
            assert file_target.read() == 'file content config.yml.dist'

    def test_set_up_case_target_file_does_not_exist(self):
        """
        Target file should replace with source file.
        """
        YamlDataClassConfigHandler.set_up()
        with self.CONFIG_FILE_PATH.target.open('r') as file_target:
            assert file_target.read() == 'file content config.yml.dist'

    def test_set_up_case_target_override_path_current_directory(self):
        """
        Target file should back up.
        Target file should replace with source file.
        """
        file_content_target_file = self._create_target_file(self.OVERRIDE_CONFIG_FILE_PATH.target)
        PathOverWrittenYamlDataClassConfigHandler.set_up()
        with self.OVERRIDE_CONFIG_FILE_PATH.backup.open('r') as file_backup:
            assert file_backup.read() == file_content_target_file
        with self.OVERRIDE_CONFIG_FILE_PATH.target.open('r') as file_target:
            assert file_target.read() == (
                'file content config.yml.dist in testsetupcasetargetoverridepathcurrentdirectory'
            )

    def test_do_cleanups_case_backup_file_does_not_exist(self):
        """
        Target file should replace with backup file.
        """
        file_content_target_file = self._create_target_file()
        YamlDataClassConfigHandler.do_cleanups()
        with self.CONFIG_FILE_PATH.target.open('r') as file_target:
            assert file_target.read() == file_content_target_file

    def test_do_cleanups_case_backup_file_exists(self):
        """
        Target file should replace with backup file.
        Backup file should not exist.
        """
        self._create_target_file()
        file_content_backup_file = self._create_backup_file()
        YamlDataClassConfigHandler.do_cleanups()
        with self.CONFIG_FILE_PATH.target.open('r') as file_target:
            assert file_target.read() == file_content_backup_file
        assert not self.CONFIG_FILE_PATH.backup.exists()

    def _create_target_file(self, file_target: Path = None):
        if file_target is None:
            file_target = self.CONFIG_FILE_PATH.target
        return self._create_file('file content target file', file_target)

    def _create_backup_file(self, file_backup: Path = None):
        if file_backup is None:
            file_backup = self.CONFIG_FILE_PATH.backup
        return self._create_file('file content backup file', file_backup)

    @staticmethod
    def _create_file(file_content, path_to_file):
        with path_to_file.open('w') as file:
            file.write(file_content)
        return file_content
