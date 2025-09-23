"""Pytest test to reproduce and verify dataclasses-json warnings."""

import warnings
from dataclasses import dataclass

import pytest

from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class TestWarningsConfig(YamlDataClassConfig):
    """Simple test config to reproduce warnings."""
    name: str = "test"


def test_no_dataclasses_json_warnings():
    """Test that verifies NO dataclasses-json warnings are present."""
    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")

        config = TestWarningsConfig()
        # This should NOT trigger warnings about unknown types for base class fields
        schema = config.schema()

        # Filter for the specific warnings we want to eliminate
        dataclasses_json_warnings = [
            w for w in warning_list
            if "Unknown type" in str(w.message)
            and "mm_field" in str(w.message)
            and any(field in str(w.message) for field in ["FILE_PATH", "_loaded", "_needs_property_descriptors"])
        ]

        # Print all warnings for debugging
        print(f"Total warnings: {len(warning_list)}")
        for w in warning_list:
            print(f"Warning: {w.message}")

        # Print the specific warnings we're checking
        print(f"Dataclasses-json warnings for base fields: {len(dataclasses_json_warnings)}")
        for w in dataclasses_json_warnings:
            print(f"Base field warning: {w.message}")

        # Assert that we have NO warnings for the base class fields
        assert len(dataclasses_json_warnings) == 0, f"Found {len(dataclasses_json_warnings)} warnings for base class fields that should be fixed"


