"""Final test to achieve 100% total coverage - targeting config.py line 114."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from yamldataclassconfig.config import YamlDataClassConfig

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class DefaultPathTestConfig(YamlDataClassConfig):
    """Config that uses default FILE_PATH."""

    test_field: str


@pytest.mark.parametrize("content", ['test_field: "default_path_test"'])
def test_line_89_default_file_path(temporary_yaml_file: Path) -> None:
    """Test to ensure config.py line 89 (default FILE_PATH usage) is executed."""
    # Create config instance with FILE_PATH set
    config = DefaultPathTestConfig.create()
    config.FILE_PATH = temporary_yaml_file

    # Call load without path parameter - this should trigger line 89: path = self.FILE_PATH
    config.load()

    # Verify it worked
    assert config.test_field == "default_path_test"
