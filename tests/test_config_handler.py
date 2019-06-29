import os
import shutil
from pathlib import Path

from yamldataclassconfig.config_handler import YamlDataClassConfigHandler


class TestYamlDataClassConfigHandler:
    PATH_CURRENT_DIRECTORY = Path(os.getcwd())
    PATH_TARGET: Path = PATH_CURRENT_DIRECTORY
    FILE_TARGET: Path = PATH_TARGET / 'config.yml'
    FILE_BACKUP: Path = PATH_TARGET / 'config.yml.bak'
    FILE_BACKUP_FOR_TEST: Path = PATH_TARGET / 'config.yml.test.bak'

    def setup_method(self, method):
        if self.FILE_TARGET.is_file():
            shutil.move(str(self.FILE_TARGET), str(self.FILE_BACKUP_FOR_TEST))
        if self.FILE_BACKUP.exists():
            os.unlink(str(self.FILE_BACKUP))

    def teardown_method(self, method):
        if not self.FILE_BACKUP_FOR_TEST.is_file():
            return
        if self.FILE_TARGET.is_file():
            os.unlink(str(self.FILE_TARGET))
        shutil.move(str(self.FILE_BACKUP_FOR_TEST), str(self.FILE_TARGET))

    def test_set_up_case_target_file_exists(self):
        file_content_target_file = self._create_target_file()
        YamlDataClassConfigHandler.set_up()
        with self.FILE_BACKUP.open('r') as file_target:
            assert file_target.read() == file_content_target_file
        with self.FILE_TARGET.open('r') as file_target:
            assert file_target.read() == 'file content config.yml.dist'

    def test_set_up_case_target_file_does_not_exist(self):
        YamlDataClassConfigHandler.set_up()
        with self.FILE_TARGET.open('r') as file_target:
            assert file_target.read() == 'file content config.yml.dist'

    def test_do_cleanups_case_backup_file_does_not_exist(self):
        file_content_target_file = self._create_target_file()
        YamlDataClassConfigHandler.do_cleanups()
        with self.FILE_TARGET.open('r') as file_target:
            assert file_target.read() == file_content_target_file

    def test_do_cleanups_case_backup_file_exists(self):
        self._create_target_file()
        file_content_backup_file = self._create_backup_file()
        YamlDataClassConfigHandler.do_cleanups()
        with self.FILE_TARGET.open('r') as file_target:
            assert file_target.read() == file_content_backup_file
        assert not self.FILE_BACKUP.exists()

    def _create_target_file(self):
        return self._create_file('file content target file', self.FILE_TARGET)

    def _create_backup_file(self):
        return self._create_file('file content backup file', self.FILE_BACKUP)

    @staticmethod
    def _create_file(file_content, path_to_file):
        with path_to_file.open('w') as file:
            file.write(file_content)
        return file_content
