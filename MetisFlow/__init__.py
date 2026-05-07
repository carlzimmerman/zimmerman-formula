"""
METISFLOW - Literature Research and Strategy
=============================================

DEPRECATED: This module has moved to OlympusFlow.flows.metis

Please update imports:
    OLD: from MetisFlow import MetisEngine
    NEW: from OlympusFlow.flows.metis import MetisEngine

    OR: from OlympusFlow.flows import MetisEngine

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "MetisFlow has moved to OlympusFlow.flows.metis. "
    "Please update imports: from OlympusFlow.flows.metis import MetisEngine",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from OlympusFlow.flows.metis import (
    MetisEngine,
    DerivationStrategy,
    DerivationApproach,
    DerivationFramework,
    ZSquaredRelevance,
    LiteratureSource,
    MetisResearchResult,
    LiteratureSearcher,
)

__version__ = "1.0.0"
__all__ = [
    "MetisEngine",
    "DerivationStrategy",
    "DerivationApproach",
    "DerivationFramework",
    "ZSquaredRelevance",
    "LiteratureSource",
    "MetisResearchResult",
    "LiteratureSearcher",
]
