"""
OLYMPUSFLOW FLOWS - Unified Processing Pipelines
=================================================

All research flows are now submodules of OlympusFlow.

Flows:
    - ergon: Action principle derivations (Lagrangians)
    - briareus: Pattern search engine
    - truth: Validation pipeline
    - metis: Literature research
    - cyllene: Learning and deepening
    - alpheus: Queue management
    - hermes: Web research agent

Usage:
    from OlympusFlow.flows import ErgonFlow, BriareusFlow, TruthFlow
    # OR
    from OlympusFlow.flows.ergon import ActionDeriver
"""

# Import flows as they are migrated
from .ergon import ActionDeriver, ActionDerivation, LAGRANGIAN_TEMPLATES
from .metis import MetisEngine, ZSquaredRelevance, DerivationStrategy
from .briareus import (
    BriareusController, PatternSearchEngine, GeometricInterpreter,
    SearchConfig, SearchTarget, SearchPriority, OlympusBridge
)
from .truth import TruthEngine, FormulaGenerator, Prediction, Discovery
from .cyllene import (
    TruthStore, TrainingGenerator, ModelUpdater, IterationRunner,
    Deepener, BatchDeepener, ResearchQuestion, DeepeningDecision
)

__all__ = [
    # Ergon Flow
    "ActionDeriver",
    "ActionDerivation",
    "LAGRANGIAN_TEMPLATES",
    # Metis Flow
    "MetisEngine",
    "ZSquaredRelevance",
    "DerivationStrategy",
    # Briareus Flow
    "BriareusController",
    "PatternSearchEngine",
    "GeometricInterpreter",
    "SearchConfig",
    "SearchTarget",
    "SearchPriority",
    "OlympusBridge",
    # Truth Flow
    "TruthEngine",
    "FormulaGenerator",
    "Prediction",
    "Discovery",
    # Cyllene Flow
    "TruthStore",
    "TrainingGenerator",
    "ModelUpdater",
    "IterationRunner",
    "Deepener",
    "BatchDeepener",
    "ResearchQuestion",
    "DeepeningDecision",
]
