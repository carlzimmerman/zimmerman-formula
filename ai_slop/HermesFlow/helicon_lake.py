"""
HeliconLake - Data Source Registry
==================================

DEPRECATED: This module has moved to OlympusFlow.lakes.helicon

Please update imports:
    OLD: from HermesFlow.helicon_lake import HeliconLake
    NEW: from OlympusFlow.lakes.helicon import HeliconLake

    OR: from OlympusFlow.lakes import HeliconLake

This file re-exports from the new location for backward compatibility.
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "HermesFlow.helicon_lake has moved to OlympusFlow.lakes.helicon. "
    "Please update imports: from OlympusFlow.lakes import HeliconLake",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from OlympusFlow.lakes.helicon import HeliconLake, SourceEntry

__all__ = ["HeliconLake", "SourceEntry"]
