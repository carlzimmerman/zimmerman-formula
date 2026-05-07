"""
MNEMOSYNE LAKE - Truth Datalake for Z2 Research
================================================

Named after Mnemosyne, the Greek goddess of memory and mother of the Muses.

This module provides a datalake for storing computationally verified truths
discovered through the autonomous research workflow. Truths are:

1. COMPUTATIONAL - Verified through real data analysis, not speculation
2. PERSISTENT - Stored for aggregation and pattern discovery
3. TRAINABLE - Exportable for Legomena training via CylleneFlow
4. VERSIONED - Tracked over time as measurements improve

Architecture:
- MnemosyneLake: Main storage and retrieval interface
- VerifiedTruth: Schema for truth records
- TruthExporter: Export truths for training

Integration:
- HermesFlow discovers data
- TruthFlow validates findings
- MnemosyneLake stores verified truths
- CylleneFlow exports for training

Usage:
    from OlympusFlow.lakes.mnemosyne import MnemosyneLake, VerifiedTruth

    lake = MnemosyneLake(session_id="research_session")
    lake.add_truth(truth)
    validated = lake.graduate_to_training()
"""

from .lake import (
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
