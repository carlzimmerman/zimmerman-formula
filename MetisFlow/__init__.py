#!/usr/bin/env python3
"""
METISFLOW - The Wisdom Engine
==============================

Research-driven derivation framework that thinks before acting.

Metis was the Titan goddess of wisdom, prudent counsel, and deep thought.
She was the first wife of Zeus and the mother of Athena.

MetisFlow embodies the principle of "research before derivation" -
understanding HOW constants have been derived in literature before
attempting our own Z² derivation.

Pipeline Position:
    AlpheusFlow (Queue) → MetisFlow (Research) → OlympusFlow (Execute)

Author: Carl Zimmerman
Date: May 5, 2026
"""

from .derivation_strategy import (
    DerivationStrategy,
    DerivationApproach,
    DerivationFramework,
    ZSquaredRelevance,
    LiteratureSource,
    MetisResearchResult
)

from .literature_searcher import LiteratureSearcher

from .metis_engine import MetisEngine

__all__ = [
    # Core engine
    "MetisEngine",

    # Strategy contracts
    "DerivationStrategy",
    "DerivationApproach",
    "DerivationFramework",
    "ZSquaredRelevance",
    "LiteratureSource",
    "MetisResearchResult",

    # Searcher
    "LiteratureSearcher"
]

__version__ = "1.0.0"
