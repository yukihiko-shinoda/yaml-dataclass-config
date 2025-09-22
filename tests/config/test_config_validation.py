"""Tests for the new validate_config_dataclass functionality."""

from __future__ import annotations

import sys
import textwrap
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from yamldataclassconfig.config import YamlDataClassConfig
from yamldataclassconfig.exceptions import ConfigNotLoadedError
from yamldataclassconfig.exceptions import ConfigValidationError

# Reason: ExceptionGroup is only available in Python 3.11+.
if sys.version_info < (3, 11):  # pragma nocover
    # pylint: disable-next=import-error,redefined-builtin
    from exceptiongroup import ExceptionGroup  # type: ignore[import-not-found]
if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class ValidatedTestConfig(YamlDataClassConfig):
    """Config class for testing validation scenarios."""

    name: str
    age: int
    active: bool


class TestValidateConfig:
    """Tests for validate_config_dataclass decorator."""

    def test_access_before_load_raises_error(self) -> None:
        """Test that accessing properties before load raises ConfigNotLoadedError."""
        config = ValidatedTestConfig.create()

        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'name'"):
            _ = config.name

        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'age'"):
            _ = config.age

        with pytest.raises(ConfigNotLoadedError, match="Configuration must be loaded before accessing 'active'"):
            _ = config.active

    def test_successful_load_and_access(self, resource_path_root: Path) -> None:
        """Test that after successful load, properties can be accessed."""
        config = ValidatedTestConfig.create()
        config.load(resource_path_root / "validated_config.yml")

        # Should work without errors after loading
        assert config.name == "hello"
        expected_age = 42
        assert config.age == expected_age
        assert config.active is True

    @pytest.mark.parametrize(
        "content",
        [
            textwrap.dedent(
                """
                name: "hello"
                age: "not_an_int"
                active: true
                """,
            ),
        ],
    )
    def test_type_validation_single_error(self, temporary_yaml_file: Path) -> None:
        """Test that type validation catches single type errors."""
        config = ValidatedTestConfig.create()
        with pytest.raises(ExceptionGroup) as exc_info:
            config.load(temporary_yaml_file)

        # Check that we got the expected validation error
        assert len(exc_info.value.exceptions) == 1
        assert isinstance(exc_info.value.exceptions[0], ConfigValidationError)
        assert "Field 'age' expected int, got str" in str(exc_info.value.exceptions[0])

    @pytest.mark.parametrize(
        "content",
        [
            textwrap.dedent(
                """
                name: 123
                age: "not_an_int"
                active: "not_a_bool"
                """,
            ),
        ],
    )
    def test_type_validation_multiple_errors(self, temporary_yaml_file: Path) -> None:
        """Test that type validation collects multiple errors."""
        config = ValidatedTestConfig.create()
        with pytest.raises(ExceptionGroup) as exc_info:
            config.load(temporary_yaml_file)

        # Verify we got the expected validation errors
        expected_error_count = 3
        assert len(exc_info.value.exceptions) == expected_error_count
        error_messages = [str(e) for e in exc_info.value.exceptions]
        expected_errors = [
            "Field 'name' expected str, got int",
            "Field 'age' expected int, got str",
            "Field 'active' expected bool, got str",
        ]
        for expected_error in expected_errors:
            assert any(expected_error in msg for msg in error_messages)

    @pytest.mark.parametrize(
        "content",
        [
            textwrap.dedent(
                """
                name: "test"
                age: 25
                active: false
                """,
            ),
        ],
    )
    def test_no_nullable_types_required(self, temporary_yaml_file: Path) -> None:
        """Test that properties don't require | None annotations."""
        config = ValidatedTestConfig.create()
        config.load(temporary_yaml_file)

        self._verify_nullable_config_values(config)

    def _verify_nullable_config_values(self, config: ValidatedTestConfig) -> None:
        """Verify that config has correct types and values for nullable test."""
        self._verify_config_types(config)
        self._verify_config_content(config)

    def _verify_config_types(self, config: ValidatedTestConfig) -> None:
        """Verify that config fields have correct types."""
        assert isinstance(config.name, str)
        assert isinstance(config.age, int)
        assert isinstance(config.active, bool)

    def _verify_config_content(self, config: ValidatedTestConfig) -> None:
        """Verify that config fields have correct values."""
        assert config.name == "test"
        expected_test_age = 25
        assert config.age == expected_test_age
        assert config.active is False
