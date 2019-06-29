import os
import shutil
from pathlib import Path


class YamlDataClassConfigHandler:
    """This class handles config.yml."""
    PATH_CURRENT_DIRECTORY = Path(os.getcwd())
    PATH_TARGET: Path = PATH_CURRENT_DIRECTORY
    PATH_SOURCE: Path = PATH_CURRENT_DIRECTORY / 'tests'
    FILE_TARGET: Path = PATH_TARGET / 'config.yml'
    FILE_SOURCE: Path = PATH_SOURCE / 'config.yml.dist'
    FILE_BACKUP: Path = PATH_TARGET / 'config.yml.bak'

    @classmethod
    def set_up(cls, file_source=FILE_SOURCE):
        """This function set up config.yml."""
        if cls.FILE_TARGET.is_file():
            shutil.move(str(cls.FILE_TARGET), str(cls.FILE_BACKUP))
        shutil.copy(str(file_source), str(cls.FILE_TARGET))

    @classmethod
    def do_cleanups(cls):
        """This function clean up config.yml."""
        if cls.FILE_BACKUP.is_file():
            os.unlink(str(cls.FILE_TARGET))
            shutil.move(str(cls.FILE_BACKUP), str(cls.FILE_TARGET))
