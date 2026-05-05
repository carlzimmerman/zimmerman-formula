"""
ALETHEIALAKE - Permanent Ground Truth Storage
=============================================

Named after Aletheia, Greek goddess of truth and disclosure.

This lake stores the IMMUTABLE ground truths of the Z² framework.
These are derived predictions that have been empirically validated
and should NEVER be modified or challenged during research loops.

Architecture:
    AletheiaLake (this) ← Ground truths, never changes
         ↑
    Validate against
         |
    MnemosyneLake     ← Temporary working memory for HermesFlow
         |
    graduate_to_training() → Training data for Legomena
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
]
