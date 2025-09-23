"""Pytest test to reproduce and verify dataclasses-json warnings."""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from logging import getLogger

from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class TestWarningsConfig(YamlDataClassConfig):
    """Simple test config to reproduce warnings."""

    name: str = "test"


class LoggerWarnings:
    """Logger for warnings."""

    def __init__(self) -> None:
        self.logger = getLogger(__name__)

    def log_warning_list(self, warning_list: list[warnings.WarningMessage]) -> None:
        """Print all warnings for debugging."""
        self.logger.debug("Total warnings: %d", len(warning_list))
        for w in warning_list:
            self.logger.debug("Warning: %s", w.message)

    def log_dataclasses_json_warnings(self, warning_messages: list[warnings.WarningMessage]) -> None:
        """Print dataclasses-json warnings for debugging."""
        self.logger.debug("Dataclasses-json warnings: %d", len(warning_messages))
        for w in warning_messages:
            self.logger.debug("Dataclasses-json warning: %s", w.message)


class TestNoDataclassesJsonWarnings:
    """Test that verifies NO dataclasses-json warnings are present."""

    def test_no_dataclasses_json_warnings(self, recwarn: list[warnings.WarningMessage]) -> None:
        """Test that verifies NO dataclasses-json warnings are present."""
        warnings.simplefilter("always")

        config = TestWarningsConfig()
        # This should NOT trigger warnings about unknown types for base class fields
        config.schema()

        # Filter for the specific warnings we want to eliminate
        dataclasses_json_warnings = self.get_dataclasses_json_warnings(recwarn)

        logger = LoggerWarnings()
        logger.log_warning_list(recwarn)
        logger.log_dataclasses_json_warnings(dataclasses_json_warnings)

        # Assert that we have NO warnings for the base class fields
        assert len(dataclasses_json_warnings) == 0, (
            f"Found {len(dataclasses_json_warnings)} warnings for base class fields that should be fixed"
        )

    def get_dataclasses_json_warnings(self, recwarn: list[warnings.WarningMessage]) -> list[warnings.WarningMessage]:
        """Extract dataclasses-json warnings from the recorded warnings."""
        return [w for w in recwarn if self.filter_by_target_keywords(w)]

    def filter_by_target_keywords(self, warning_message: warnings.WarningMessage) -> bool:
        """Filter warnings by keywords."""
        return (
            "Unknown type" in str(warning_message)
            and "mm_field" in str(warning_message)
            and any(field in str(warning_message) for field in ["FILE_PATH", "_loaded", "_needs_property_descriptors"])
        )
