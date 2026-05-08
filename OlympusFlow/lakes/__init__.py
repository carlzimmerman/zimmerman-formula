"""
OLYMPUSFLOW LAKES - Unified Data Storage Layer
===============================================

All data lakes are now submodules of OlympusFlow.

Lakes:
    TRUTH LAKES (for verified/working findings):
    - aletheia: Permanent ground truths (immutable)
    - mnemosyne: Session working memory (temporary)
    - helicon: Data source registry

    BANISHMENT LAKES (for failed/rejected findings):
    - tartarus: Empirical failures (logic sound, data doesn't match)
    - lethe: Hallucinations & sycophancy (consensus defaults, not Z²)
    - labyrinth: Logical dead-ends (stuck but potentially valuable)

Hecate decides which banishment lake to cast failed findings into.

Usage:
    from OlympusFlow.lakes import AletheiaLake, MnemosyneLake, HeliconLake
    from OlympusFlow.lakes import TartarusLake, LetheLake, LabyrinthLake
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

# Banishment Lakes (Hecate's underworld)
from .banishment import (
    BaseBanishmentLake,
    BanishedEntry,
    HecateBanishmentNote,
    BanishmentType,
    BanishmentSeverity,
)

from .tartarus import TartarusLake
from .lethe import LetheLake
from .labyrinth import LabyrinthLake

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
    # Banishment Lakes
    "BaseBanishmentLake",
    "BanishedEntry",
    "HecateBanishmentNote",
    "BanishmentType",
    "BanishmentSeverity",
    "TartarusLake",
    "LetheLake",
    "LabyrinthLake",
]
