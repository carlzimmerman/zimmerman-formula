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

__all__ = [
    # Ergon Flow
    "ActionDeriver",
    "ActionDerivation",
    "LAGRANGIAN_TEMPLATES",
]
