# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `yamldataclassconfig`, a Python library that enables type-safe importing of YAML configuration files into Python dataclasses. The library bridges YAML configuration files with Python's dataclass system, providing global config access and testability.

## Architecture

### Core Components

- **`yamldataclassconfig/config.py`**: Contains `YamlDataClassConfig` - the main abstract base class that users inherit from to create config classes
- **`yamldataclassconfig/utility.py`**: Utility functions for path handling (`build_path`, `create_file_path_field`) and dataclass metadata
- **`yamldataclassconfig/__init__.py`**: Package entry point that exposes all public APIs

### Key Design Patterns

- **Delayed Loading**: Config classes are instantiated globally but YAML files are loaded explicitly via `load()` method to support testing
- **Path Resolution**: Supports both relative (to current working directory) and absolute paths for config files
- **Type Safety**: Uses `dataclasses-json` and marshmallow for type-safe YAML to dataclass conversion

## Development Commands

The project uses `uv` as the package manager and `invoke` for task automation:

### Testing
```bash
uv run invoke test           # Run fast tests (excludes @pytest.mark.slow)
uv run invoke test.all       # Run all tests including slow ones
uv run invoke test.coverage  # Run tests with coverage report
uv run pytest path/to/test   # Run specific test file
```

### Linting & Code Quality
```bash
uv run invoke lint           # Fast linting (xenon, ruff, bandit, dodgy, flake8, pydocstyle)
uv run invoke lint.deep      # Slow but thorough linting (mypy, pylint, semgrep)
uv run invoke lint.mypy      # Type checking only
uv run invoke lint.ruff      # Ruff linting only
```

### Code Formatting
```bash
uv run invoke style          # Format code with docformatter and Ruff
uv run invoke style --check  # Check formatting without making changes
```

### Building & Distribution
```bash
uv run invoke dist           # Build source and wheel packages
uv run invoke clean.all      # Clean all build artifacts
```

## Project Structure

```
yamldataclassconfig/          # Main package
├── __init__.py              # Public API exports
├── config.py                # YamlDataClassConfig base class
├── utility.py               # Path utilities and helpers
└── py.typed                 # PEP 561 typing marker

tests/                       # Test suite
├── conftest.py             # pytest configuration
├── test_*.py               # Test modules
└── testresources/          # Test fixtures and resources

docs/                       # Documentation
└── CONTRIBUTING.md         # Contribution guidelines
```

## Code Conventions

- Uses Python 3.7+ type hints throughout
- Follows dataclasses pattern with `@dataclass` decorator
- Uses `dataclasses-json` for serialization/deserialization
- Line length: 119 characters (configured for Black compatibility)
- Import style: Force single-line imports (ruff configured)
- Documentation: Google docstring style
- Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
- Function arguments requires to have type annotations.
- Use Guard Clauses to reduce nesting and improve readability.

### Import Guidelines

#### Import Placement

- **ALL imports MUST be at the top-level of the file**, immediately after any module comments and docstrings, and before module globals and constants
- **NEVER place imports inside functions, methods, or classes** - this violates PEP 8 and makes dependencies unclear
- **NEVER use conditional imports inside functions** unless absolutely necessary for optional dependencies

#### Import Organization

1. Standard library imports
2. Third-party library imports
3. Local application/library imports

#### Prohibited Patterns

```python
# ❌ NEVER DO THIS - imports inside methods
def test_something():
    import os  # WRONG!
    from pathlib import Path  # WRONG!

# ❌ NEVER DO THIS - imports inside classes
class TestClass:
    def method(self):
        import tempfile  # WRONG!

# ✅ CORRECT - all imports at top
import os
import tempfile
from pathlib import Path

def test_something():
    # Use the imports here
```

Exceptions

- Only use local imports when dealing with circular dependencies or optional dependencies that may not be available
- If you must use local imports, document the reason with a comment

## Configuration

The project has comprehensive tooling configuration in `pyproject.toml`:
- **Ruff**: Linting and formatting with ALL rules enabled, specific ignores for docstring requirements
- **mypy**: Strict mode enabled
- **pytest**: Slow test markers configured
- **coverage**: Source tracking for `yamldataclassconfig` package

## Claude Code Integration

- **Auto-linting**: Files are automatically linted after edits via hooks
- **Permissions**: Pre-configured to allow editing main package and test files
- **Git operations**: Commit and push operations are restricted to prevent accidental changes

## Testing Philosophy

- Fast tests run by default, slow tests marked with `@pytest.mark.slow`
- Uses fixture files for configuration testing scenarios
- Tests cover both unittest and pytest patterns for config loading
- Test resources stored in `tests/testresources/` for isolation