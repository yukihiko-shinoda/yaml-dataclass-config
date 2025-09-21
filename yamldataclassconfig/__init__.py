"""This module implements helpers to import config file writen by YAML to Python Data Classes."""

from __future__ import annotations

# Reason: ExceptionGroup is only available in Python 3.11+.
from yamldataclassconfig.config import *  # noqa: F403  # pylint: disable=redefined-builtin
from yamldataclassconfig.nullable import *  # noqa: F403
from yamldataclassconfig.type_defaults import *  # noqa: F403
from yamldataclassconfig.utility import *  # noqa: F403

__version__ = "1.5.0"

__all__: list[str] = []
# pylint: disable=undefined-variable
__all__ += config.__all__  # type: ignore[name-defined]  # noqa: F405
__all__ += nullable.__all__  # type: ignore[name-defined]  # noqa: F405
__all__ += type_defaults.__all__  # type: ignore[name-defined]  # noqa: F405
__all__ += utility.__all__  # type: ignore[name-defined]  # noqa: F405
