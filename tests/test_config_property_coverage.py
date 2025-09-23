"""Tests for config_property module to achieve 100% coverage."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List

import pytest
from marshmallow import ValidationError

from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig.config_property import DataclassType
from yamldataclassconfig.config_property import set_deserialization_context
from yamldataclassconfig.exceptions import ConfigNotLoadedError

# Constants to avoid magic numbers
DEFAULT_COUNT = 42


@dataclass
class ConfigWithDefaultFactory(YamlDataClassConfig):
    """Config class with default_factory field for testing."""

    name: str
    # Reason: Ruff's bug
    items: List[str] = field(default_factory=list)  # noqa: UP006


@dataclass
class ConfigWithRegularDefault(YamlDataClassConfig):
    """Config class with regular default value for testing."""

    name: str
    count: int = DEFAULT_COUNT


@dataclass
class ConfigWithNoDefaults(YamlDataClassConfig):
    """Config class with no defaults for testing."""

    name: str
    age: int


# Removed unused fixture - content is now inline in tests


class TestDataclassTypeCoverage:
    """Test DataclassType class for missing coverage."""

    def test_dataclass_type_init(self) -> None:
        """Test DataclassType initialization."""
        dt = DataclassType(ConfigWithRegularDefault)
        assert dt.cls == ConfigWithRegularDefault

    def test_get_field_default_with_regular_default(self) -> None:
        """Test getting field default with regular default value."""
        dt = DataclassType(ConfigWithRegularDefault)
        default_value = dt.get_field_default("count")
        assert default_value == DEFAULT_COUNT

    def test_get_field_default_with_default_factory(self) -> None:
        """Test getting field default with default_factory."""
        dt = DataclassType(ConfigWithDefaultFactory)
        default_value = dt.get_field_default("items")
        assert default_value == []

    def test_get_field_default_no_default_raises_error(self) -> None:
        """Test getting field default when field has no default raises ConfigNotLoadedError."""
        dt = DataclassType(ConfigWithNoDefaults)
        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'name'"):
            dt.get_field_default("name")

    def test_get_field_default_nonexistent_field_raises_error(self) -> None:
        """Test getting field default for nonexistent field raises ConfigNotLoadedError."""
        dt = DataclassType(ConfigWithRegularDefault)
        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'nonexistent'"):
            dt.get_field_default("nonexistent")


class TestConfigPropertyDeserialization:
    """Test ConfigProperty during deserialization context."""

    def test_deserialization_context_with_default_factory(self, tmp_path: Any) -> None:  # noqa: ANN401
        """Test property access during deserialization with default_factory field."""
        # Create config file
        config_file = tmp_path / "config.yml"
        config_file.write_text('name: "test"')

        # Test loading config with missing field that has default_factory
        config = ConfigWithDefaultFactory.create()
        config.load(config_file, path_is_absolute=True)

        # This should work and return the default factory value
        assert not config.items

    def test_deserialization_context_with_regular_default(self, tmp_path: Any) -> None:  # noqa: ANN401
        """Test property access during deserialization with regular default field."""
        # Create config file
        config_file = tmp_path / "config.yml"
        config_file.write_text('name: "test"')

        # Test loading config with missing field that has regular default
        config = ConfigWithRegularDefault.create()
        config.load(config_file, path_is_absolute=True)

        # This should work and return the default value
        assert config.count == DEFAULT_COUNT

    def test_deserialization_context_no_default_raises_error(self, tmp_path: Any) -> None:  # noqa: ANN401
        """Test property access during deserialization with no default raises error."""
        # Create config file with missing required field
        config_file = tmp_path / "config.yml"
        config_file.write_text("name: test")

        config = ConfigWithNoDefaults.create()

        # This should fail during load because 'age' field has no default
        with pytest.raises(ValidationError, match="Missing data for required field"):
            config.load(config_file, path_is_absolute=True)

    def test_manual_deserialization_context(self) -> None:
        """Test manual deserialization context management."""
        config = ConfigWithRegularDefault.create()

        # Set deserialization context manually
        set_deserialization_context(value=True)
        try:
            # During deserialization, should return default value
            assert config.count == DEFAULT_COUNT
        finally:
            # Always reset context
            set_deserialization_context(value=False)

        # After context is reset, should raise error for unloaded config
        with pytest.raises(ConfigNotLoadedError):
            _ = config.count
