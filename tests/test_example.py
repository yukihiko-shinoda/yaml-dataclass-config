"""Tests for README.md examples."""

from __future__ import annotations

import pytest

from myproduct import my_project
from yourproduct import CONFIG
from yourproduct.pytest_context import yaml_config  # noqa: F401 pylint: disable=unused-import
from yourproduct.unittest_context import ConfigurableTestCase


class TestYamlDataClassConfig:
    """Tests for YamlDataClassConfig."""

    @staticmethod
    def test_scenario_readme(capsys: pytest.CaptureFixture[str]) -> None:
        """Values on YAML file should be printed."""
        my_project.main()
        captured = capsys.readouterr()
        assert (
            captured.out
            == """1
2
2019-06-25 13:33:30
"""
        )


class TestConfigHandlerPytest:
    """Tests for pytest scenario."""

    @staticmethod
    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("yaml_config")
    def test_config_handler_pytest() -> None:
        """Config file for test should be loaded."""
        assert CONFIG.some_property == "test value"


class TestConfigHandlerUnittest(ConfigurableTestCase):
    """Tests for unittest scenario."""

    def test_config_handler_unittest(self) -> None:
        """Config file for test should be loaded."""
        assert CONFIG.some_property == "test value"
