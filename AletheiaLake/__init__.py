"""
ALETHEIALAKE - Permanent Ground Truth Storage
=============================================

DEPRECATED: This module has moved to OlympusFlow.lakes.aletheia

Please update imports:
    OLD: from AletheiaLake import AletheiaLake
    NEW: from OlympusFlow.lakes.aletheia import AletheiaLake

    OR: from OlympusFlow.lakes import AletheiaLake

This file re-exports from the new location for backward compatibility.
"""

import warnings

# Issue deprecation warning (but don't spam - only once per session)
warnings.warn(
    "AletheiaLake has moved to OlympusFlow.lakes.aletheia. "
    "Please update imports: from OlympusFlow.lakes import AletheiaLake",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from OlympusFlow.lakes.aletheia import (
    AletheiaLake,
    Z2Truth,
    ValidationResult,
    DerivationLevel,
    SourceTier,
    ValidationStatus,
    Z2_SQUARED,
    Z,
    PHI,
    get_z2_predictions,
    validate_measurement,
)

__all__ = [
    "AletheiaLake",
    "Z2Truth",
    "ValidationResult",
    "DerivationLevel",
    "SourceTier",
    "ValidationStatus",
    "Z2_SQUARED",
    "Z",
    "PHI",
    "get_z2_predictions",
    "validate_measurement",
]
