"""
METISFLOW - Literature Research and Strategy
=============================================

Named after Metis, the Titan goddess of wisdom, prudent counsel, and deep thought.

This flow researches HOW constants have been derived in literature before
attempting our own Z2 derivation. It embodies "thinking before acting."

Components:
- MetisEngine: Main research engine
- LiteratureSearcher: Searches papers and sources
- DerivationStrategy: Analyzes approaches and Z2 relevance

Usage:
    from OlympusFlow.flows.metis import MetisEngine, ZSquaredRelevance

    engine = MetisEngine()
    result = engine.research("fine_structure_constant")
"""

from .metis_engine import MetisEngine
from .derivation_strategy import (
    DerivationStrategy,
    DerivationApproach,
    DerivationFramework,
    ZSquaredRelevance,
    LiteratureSource,
    MetisResearchResult,
)
from .literature_searcher import LiteratureSearcher

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
