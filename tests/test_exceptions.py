"""Tests for yamldataclassconfig.exceptions module."""

from __future__ import annotations

import pytest

from yamldataclassconfig.exceptions import ConfigNotLoadedError
from yamldataclassconfig.exceptions import ConfigValidationError


class TestConfigNotLoadedError:
    """Test ConfigNotLoadedError exception."""

    def test_config_not_loaded_error_creation(self) -> None:
        """Test ConfigNotLoadedError can be created with message."""
        msg = "Test error message"
        error = ConfigNotLoadedError(msg)
        assert str(error) == msg

    def test_config_not_loaded_error_raise(self) -> None:
        """Test ConfigNotLoadedError can be raised and caught."""
        msg = "Configuration not loaded"
        with pytest.raises(ConfigNotLoadedError, match=msg):
            raise ConfigNotLoadedError(msg)


class TestConfigValidationError:
    """Test ConfigValidationError exception."""

    def test_config_validation_error_creation(self) -> None:
        """Test ConfigValidationError can be created with message."""
        msg = "Validation failed"
        error = ConfigValidationError(msg)
        assert str(error) == msg

    def test_config_validation_error_raise(self) -> None:
        """Test ConfigValidationError can be raised and caught."""
        msg = "Type mismatch"
        with pytest.raises(ConfigValidationError, match=msg):
            raise ConfigValidationError(msg)
