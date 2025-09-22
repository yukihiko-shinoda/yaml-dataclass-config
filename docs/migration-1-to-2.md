# Migration Guide: yamldataclassconfig 1.x to 2.x

This guide helps you migrate from yamldataclassconfig version 1.x to 2.x. Version 2.0 introduces several breaking changes to improve type safety, code organization, and developer experience based on extensive refactoring and modern Python features.

## Overview of Changes

### 🔄 Breaking Changes

- **New factory method**: `Config.create()` replaces direct instantiation for better initialization
- **File path configuration**: `create_file_path_field` usage pattern changed significantly
- **Type safety improvements**: Required fields no longer use nullable defaults (`= None`)
- **API improvements**: Keyword-only arguments for better API clarity (`path_is_absolute=True`)
- **Code formatting**: Standardized on double quotes and modern Python formatting

### ✨ New Features

- **Modern Python Features**: Leverages Python 3.10+ union syntax and type hints
- **Enhanced validation**: Comprehensive YAML validation with `ExceptionGroup` for multiple errors
- **Better Type Safety**: Full mypy compliance with strict mode enabled
- **Runtime Type Checking**: Proper handling of type annotations at runtime

## Step-by-Step Migration

### 1. Update Installation

```bash
pip install yamldataclassconfig>=2.0.0
```

### 2. Update Config Class Instantiation

**⚠️ CRITICAL BREAKING CHANGE**
**Before (v1.x):**

```python
from myproduct.config import Config

CONFIG: Config = Config()
```

**After (v2.x):**

```python
from myproduct.config import Config

CONFIG: Config = Config.create()
```

**Why this change?**
The `create()` factory method provides better handling of required fields and validates the config structure at instantiation time.

### 3. Update File Path Configuration

**⚠️ MAJOR BREAKING CHANGE**
**Before (v1.x):**

```python
from pathlib import Path
from yamldataclassconfig import create_file_path_field

@dataclass
class Config(YamlDataClassConfig):
    some_property: str = None

    FILE_PATH: Path = create_file_path_field(Path(__file__).parent / 'config.yml')
```

**After (v2.x):**

```python
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from yamldataclassconfig import build_path
from yamldataclassconfig.config import YamlDataClassConfig

@dataclass
class Config(YamlDataClassConfig):
    some_property: str

    FILE_PATH: str = field(
        init=False,
        default=build_path(Path(__file__).parent / "config.yml"),
    )
```

**Key changes:**

- `create_file_path_field()` → `build_path()` with explicit `field()` wrapper
- `FILE_PATH` type changed from `Path` → `str`

### 4. Update Type Annotations and Defaults

**Before (v1.x):**

```python
@dataclass
class Config(YamlDataClassConfig):
    property_a: int = None
    property_b: str = None
    part_config: PartConfig = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': PartConfig}}
    )
```

**After (v2.x):**

```python
@dataclass
class Config(YamlDataClassConfig):
    property_a: int
    property_b: str
    part_config: PartConfig = field(
        metadata={"dataclasses_json": {"mm_field": PartConfig}},
    )
```

**Benefits:**

- Required fields are truly required (no more `= None`)
- Better type safety and IDE support
- Runtime validation ensures all required fields are present

### 8. Update API Arguments - Keyword-Only Parameters

**⚠️ BREAKING CHANGE**
**Before (v1.x):**

```python
CONFIG.load(path, True)  # Positional argument
build_path(path, True)   # Positional argument
```

**After (v2.x):**

```python
CONFIG.load(path, path_is_absolute=True)  # Keyword argument
build_path(path, path_is_absolute=True)   # Keyword argument
```

### 9. Update Error Handling

**Before (v1.x):**

```python
try:
    CONFIG.load()
except Exception as e:
    print(f"Config error: {e}")
```

**After (v2.x):**

```python
# Enhanced validation with ExceptionGroup for multiple errors
from exceptiongroup import ExceptionGroup

try:
    CONFIG.load()
except ExceptionGroup as eg:
    print("Configuration validation failed:")
    for error in eg.exceptions:
        print(f"  - {error}")
except Exception as e:
    print(f"Config error: {e}")
```

## Testing Updates

## Compatibility Notes

### Python Version Support

- **Minimum Python version**: 3.7+ (unchanged)
- **Recommended Python version**: 3.10+ for best modern union syntax support

### Dependencies

- `dataclasses-json`: No version change required
- `PyYAML`: No version change required
- `marshmallow`: No version change required
- `exceptiongroup`: Automatically installed for Python < 3.11

## Troubleshooting Common Issues

### Issue: `TypeError: Config() missing required arguments`

**Problem**: Direct instantiation fails due to required fields

```python
CONFIG = Config()  # ❌ Fails in v2.x
```

**Solution**: Use the factory method

```python
CONFIG = Config.create()  # ✅ Works in v2.x
```

### Issue: `ImportError: cannot import name 'create_file_path_field'`

**Problem**: Function still exists but some linting tools warns

```python
FILE_PATH: Path = create_file_path_field(Path(__file__).parent / 'config.yml')  # ❌ Old pattern
```

**Solution**: Use new pattern with `build_path` and explicit `field()`

```python
FILE_PATH: str = field(
    init=False,
    default=build_path(Path(__file__).parent / "config.yml"),
)  # ✅ New pattern
```

### Issue: `TypeError: unexpected keyword argument 'path_is_absolute'`

**Problem**: Positional argument used for keyword-only parameter

```python
CONFIG.load(path, True)  # ❌ Positional argument
```

**Solution**: Use keyword argument

```python
CONFIG.load(path, path_is_absolute=True)  # ✅ Keyword argument
```

### Issue: Type checker warnings about nullable access

**Problem**: Direct access to potentially None values

```python
print(CONFIG.part_config.property_c)  # ❌ May be None
```

**Solution**: Add null checks

```python
if CONFIG.part_config is not None:
    print(CONFIG.part_config.property_c)  # ✅ Safe access
```

### Issue: Configuration not loaded error

**Problem**: Accessing properties before calling `load()`

```python
config = Config.create()
print(config.property_a)  # ❌ ConfigNotLoadedError
```

**Solution**: Always load before accessing

```python
config = Config.create()
config.load()
print(config.property_a)  # ✅ Works
```

## Benefits of Upgrading

1. **Better Type Safety**: Non-nullable required fields prevent runtime errors
2. **Enhanced Validation**: `ExceptionGroup` shows all validation errors at once
3. **Modern Python Features**: Support for Python 3.10+ union syntax and type hints
4. **Improved Code Quality**: Standardized formatting and import organization
5. **Better API Design**: Keyword-only arguments prevent parameter mistakes
6. **Enhanced Developer Experience**: Better IDE support and type checking
7. **Cleaner Architecture**: Separated validation logic for better maintainability

## Rollback Plan

If you encounter issues, you can rollback to v1.x:

```bash
pip install "yamldataclassconfig<2.0.0"
```

Then revert the code changes mentioned in this guide.

## Support

If you encounter issues during migration:

1. Check the [GitHub Issues](https://github.com/yukihiko-shinoda/yaml-dataclass-config/issues)
2. Review the [API documentation](https://github.com/yukihiko-shinoda/yaml-dataclass-config)
3. Create a new issue with your migration problem

---

<!-- markdownlint-disable no-emphasis-as-heading -->
## Happy migrating! 🚀
<!-- markdownlint-enable no-emphasis-as-heading -->
