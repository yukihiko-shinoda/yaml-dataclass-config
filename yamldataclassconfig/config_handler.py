"""This module implements YAML config file handler."""
import os
import shutil
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Union, NoReturn

from deprecated import deprecated


@deprecated(reason="This module was extracted to independent package.")
class ConfigFilePathInterface:
    """This interface defines properties which is used by YamlDataClassConfigHandler"""
    @property
    @abstractmethod
    def target(self) -> Path:
        """This property return path to target file"""
    @property
    @abstractmethod
    def source(self) -> Path:
        """This property return path to source file"""
    @property
    @abstractmethod
    def backup(self) -> Path:
        """This property return path to backup file"""


@deprecated(reason="This module was extracted to independent package.")
@dataclass
class ConfigFilePathBuilder(ConfigFilePathInterface):
    """
    This class builds file path for config file.
    Default value is maybe suitable for standard directory structure of python project.
    """
    path_target_directory: Path = Path(os.getcwd())
    path_test_directory: Path = Path('tests')
    file_target: Path = Path('config.yml')
    file_source: Path = Path('config.yml.dist')
    file_backup: Path = Path('config.yml.bak')

    @property
    def target(self) -> Path:
        return self.path_target_directory / self.file_target

    @property
    def source(self) -> Path:
        return self._path_source_directory / self.file_source

    @property
    def backup(self) -> Path:
        return self.path_target_directory / self.file_backup

    @property
    def _path_source_directory(self) -> Path:
        return self.path_target_directory / self.path_test_directory


@deprecated(reason="This module was extracted to independent package.")
class YamlDataClassConfigHandler:
    """This class handles YAML config file."""
    CONFIG_FILE_PATH: ConfigFilePathInterface = ConfigFilePathBuilder()

    @classmethod
    def set_up(cls, file_source: Union[Path, str] = None) -> NoReturn:
        """
        This method replace config file by file_source.
        If file already exists, process backs up existing file.
        :param file_source: replace source file
        :return: No return
        """
        if file_source is None:
            file_source = cls.CONFIG_FILE_PATH.source
        if cls.CONFIG_FILE_PATH.target.is_file():
            shutil.move(str(cls.CONFIG_FILE_PATH.target), str(cls.CONFIG_FILE_PATH.backup))
        shutil.copy(str(file_source), str(cls.CONFIG_FILE_PATH.target))

    @classmethod
    def do_cleanups(cls) -> NoReturn:
        """
        This method replace config file by backup file if backup file is exist.
        :return: No return
        """
        if cls.CONFIG_FILE_PATH.backup.is_file():
            os.unlink(str(cls.CONFIG_FILE_PATH.target))
            shutil.move(str(cls.CONFIG_FILE_PATH.backup), str(cls.CONFIG_FILE_PATH.target))
