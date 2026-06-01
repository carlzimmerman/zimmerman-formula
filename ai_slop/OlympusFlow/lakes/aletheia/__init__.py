"""
ALETHEIALAKE - Permanent Ground Truth Storage
=============================================

Named after Aletheia, Greek goddess of truth and disclosure.

This lake stores the IMMUTABLE ground truths of the Z2 framework.
These are derived predictions that have been empirically validated
and should NEVER be modified or challenged during research loops.

Architecture:
    AletheiaLake (this) <- Ground truths, never changes
         ^
    Validate against
         |
    MnemosyneLake     <- Temporary working memory for HermesFlow
         |
    graduate_to_training() -> Training data for Legomena

Usage:
    from OlympusFlow.lakes.aletheia import AletheiaLake, Z2Truth

    lake = AletheiaLake()
    truth = lake.get_truth("omega_lambda")
    result = lake.validate("omega_lambda", 0.685, 0.007, "Planck 2018", 1)
"""

from .lake import (
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
