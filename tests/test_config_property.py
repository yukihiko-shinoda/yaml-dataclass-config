"""Tests for yamldataclassconfig.config_property module."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig.config_property import ConfigProperty
from yamldataclassconfig.config_property import create_property_descriptors
from yamldataclassconfig.exceptions import ConfigNotLoadedError


@dataclass
class ConfigExample:
    """Test config class for config_property testing."""

    name: str
    age: int


class TestConfigProperty:
    """Test ConfigProperty descriptor."""

    def test_config_property_creation(self) -> None:
        """Test ConfigProperty can be created."""
        prop = ConfigProperty("test_field")
        assert prop.name == "test_field"

    def test_config_property_get_not_loaded(self) -> None:
        """Test ConfigProperty __get__ when config is not loaded."""

        @dataclass
        class RealConfig(YamlDataClassConfig):
            """Real config class for testing."""

            name: str = ""

        # Create instance - this will have the property descriptors already applied
        # By default, _loaded is False when created
        config = RealConfig.create()

        # Test accessing before loaded - should raise error since _loaded is False by default
        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'name'"):
            _ = config.name

    def test_config_property_get_with_real_object(self) -> None:
        """Test ConfigProperty __get__ with real config object using only public properties."""

        @dataclass
        class RealConfig(YamlDataClassConfig):
            """Real config class for testing."""

            name: str = ""

        # Create instance - this will have the property descriptors already applied
        config = RealConfig.create()

        # Test accessing before loaded - should raise error since _loaded is False by default
        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'name'"):
            _ = config.name

        # Create a simple YAML file content and load it to set loaded state properly
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as temp_file:
            temp_file.write("name: test_value\n")
            temp_file.flush()

            # Load the config properly which sets _loaded = True
            config.load(Path(temp_file.name))

            # Test accessing after loaded - should return value
            result = config.name
            assert result == "test_value"


class TestCreatePropertyDescriptors:
    """Test create_property_descriptors function."""

    def test_create_property_descriptors(self) -> None:
        """Test create_property_descriptors creates descriptors for all fields."""
        # Apply the descriptors to the class
        create_property_descriptors(ConfigExample)

        # Check that descriptors were created
        self.check_name("name")
        self.check_name("age")

    @staticmethod
    def check_name(attr_name: str) -> None:
        """Check that the attribute name is correct."""
        assert hasattr(ConfigExample, attr_name)
        assert isinstance(getattr(ConfigExample, attr_name), ConfigProperty)
        assert getattr(ConfigExample, attr_name).name == attr_name
