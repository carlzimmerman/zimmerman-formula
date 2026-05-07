"""
CYLLENEFLOW - Iterative Learning Layer
======================================

DEPRECATED: This module has moved to OlympusFlow.flows.cyllene

Please update imports:
    OLD: from CylleneFlow import IterationRunner
    NEW: from OlympusFlow.flows.cyllene import IterationRunner

    OR: from OlympusFlow.flows import IterationRunner

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "CylleneFlow has moved to OlympusFlow.flows.cyllene. "
    "Please update imports: from OlympusFlow.flows.cyllene import IterationRunner",
    DeprecationWarning,
    stacklevel=2
)

__version__ = "1.3.0"

# Re-export from new location
from OlympusFlow.flows.cyllene import (
    TruthStore,
    TrainingGenerator,
    ModelUpdater,
    IterationRunner,
    Deepener,
    BatchDeepener,
    ResearchQuestion,
    DeepeningDecision
)

__all__ = [
    "__version__",
    "TruthStore",
    "TrainingGenerator",
    "ModelUpdater",
    "IterationRunner",
    "Deepener",
    "BatchDeepener",
    "ResearchQuestion",
    "DeepeningDecision"
]
