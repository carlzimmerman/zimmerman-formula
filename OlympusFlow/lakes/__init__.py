"""
OLYMPUSFLOW LAKES - Unified Data Storage Layer
===============================================

All data lakes are now submodules of OlympusFlow.

Lakes:
    - aletheia: Permanent ground truths (immutable)
    - mnemosyne: Session working memory (temporary)
    - helicon: Data source registry

Usage:
    from OlympusFlow.lakes import AletheiaLake, MnemosyneLake, HeliconLake
    # OR
    from OlympusFlow.lakes.aletheia import AletheiaLake, Z2Truth
"""

from .aletheia import (
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

from .mnemosyne import (
    MnemosyneLake,
    VerifiedTruth,
    TruthExporter,
    TruthStatus,
    TruthDomain,
)

from .helicon import (
    HeliconLake,
    SourceEntry,
)

__all__ = [
    # Aletheia Lake
    "AletheiaLake",
    "Z2Truth",
    "ValidationResult",
    "DerivationLevel",
    "SourceTier",
    "ValidationStatus",
    "Z2_SQUARED",
    "Z",
    "PHI",
    # Mnemosyne Lake
    "MnemosyneLake",
    "VerifiedTruth",
    "TruthExporter",
    "TruthStatus",
    "TruthDomain",
    # Helicon Lake
    "HeliconLake",
    "SourceEntry",
]
