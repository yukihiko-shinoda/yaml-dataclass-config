"""Tests for yamldataclassconfig.config_property module."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from yamldataclassconfig.config_property import ConfigProperty
from yamldataclassconfig.config_property import create_property_descriptors
from yamldataclassconfig.exceptions import ConfigNotLoadedError


@dataclass
class TestConfig:
    """Test config class for config_property testing."""

    name: str
    age: int


class TestConfigProperty:
    """Test ConfigProperty descriptor."""

    def test_config_property_creation(self) -> None:
        """Test ConfigProperty can be created."""
        prop = ConfigProperty("test_field")
        assert prop.name == "test_field"

    def test_config_property_get_loaded(self) -> None:
        """Test ConfigProperty __get__ when config is loaded."""
        prop = ConfigProperty("name")

        # Create a mock object with loaded state
        class MockConfig:
            def __init__(self) -> None:
                self._loaded = True
                setattr(self, "__name", "test_value")

        mock_config = MockConfig()
        result = prop.__get__(mock_config, type(mock_config))
        assert result == "test_value"

    def test_config_property_get_not_loaded(self) -> None:
        """Test ConfigProperty __get__ when config is not loaded."""
        prop = ConfigProperty("name")

        # Create a mock object with not loaded state
        class MockConfig:
            def __init__(self) -> None:
                self._loaded = False

        mock_config = MockConfig()
        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'name'"):
            prop.__get__(mock_config, type(mock_config))


class TestCreatePropertyDescriptors:
    """Test create_property_descriptors function."""

    def test_create_property_descriptors(self) -> None:
        """Test create_property_descriptors creates descriptors for all fields."""
        # Apply the descriptors to the class
        create_property_descriptors(TestConfig)

        # Check that descriptors were created
        assert hasattr(TestConfig, "name")
        assert hasattr(TestConfig, "age")
        assert isinstance(TestConfig.name, ConfigProperty)
        assert isinstance(TestConfig.age, ConfigProperty)
        assert TestConfig.name.name == "name"
        assert TestConfig.age.name == "age"