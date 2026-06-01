"""
MNEMOSYNE LAKE - Truth Datalake for Z2 Research
================================================

DEPRECATED: This module has moved to OlympusFlow.lakes.mnemosyne

Please update imports:
    OLD: from MnemosyneLake import MnemosyneLake
    NEW: from OlympusFlow.lakes.mnemosyne import MnemosyneLake

    OR: from OlympusFlow.lakes import MnemosyneLake

This file re-exports from the new location for backward compatibility.
"""

import warnings

# Issue deprecation warning (but don't spam - only once per session)
warnings.warn(
    "MnemosyneLake has moved to OlympusFlow.lakes.mnemosyne. "
    "Please update imports: from OlympusFlow.lakes import MnemosyneLake",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from OlympusFlow.lakes.mnemosyne import (
    MnemosyneLake,
    VerifiedTruth,
    TruthExporter,
    TruthStatus,
    TruthDomain,
)

__version__ = "1.0.0"
__all__ = [
    "MnemosyneLake",
    "VerifiedTruth",
    "TruthExporter",
    "TruthStatus",
    "TruthDomain",
]
