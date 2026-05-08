"""
BRIAREUSFLOW - The Hundred-Handed Phenomenological Discovery Engine
====================================================================

DEPRECATED: This module has moved to OlympusFlow.flows.briareus

Please update imports:
    OLD: from BriareusFlow import BriareusController
    NEW: from OlympusFlow.flows.briareus import BriareusController

    OR: from OlympusFlow.flows import BriareusController

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "BriareusFlow has moved to OlympusFlow.flows.briareus. "
    "Please update imports: from OlympusFlow.flows.briareus import BriareusController",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from OlympusFlow.flows.briareus import (
    # Phenomenological
    PhenomenologicalFinding,
    FindingCategory,
    DiscoveryPath,
    DiscoveryMethod,
    NumerologyRisk,
    AlternativeFit,
    FindingBatch,
    Z_SQUARED,
    Z,
    PHI,
    # Pattern search
    PatternSearchEngine,
    SearchResult,
    CoefficientMatch,
    PatternMatch,
    CoefficientType,
    # Geometric interpreter
    GeometricInterpreter,
    GeometricInterpretation,
    GeometryType,
    # Controller
    BriareusController,
    SearchConfig,
    SearchTarget,
    SearchPriority,
    BriareusResult,
    STANDARD_PHYSICS_TARGETS,
    # OlympusFlow bridge
    OlympusBridge,
    BridgeConfig,
    integrate_with_olympusflow,
)

__version__ = "3.0.0"
__all__ = [
    "PhenomenologicalFinding",
    "FindingCategory",
    "DiscoveryPath",
    "DiscoveryMethod",
    "NumerologyRisk",
    "AlternativeFit",
    "FindingBatch",
    "Z_SQUARED",
    "Z",
    "PHI",
    "PatternSearchEngine",
    "SearchResult",
    "CoefficientMatch",
    "PatternMatch",
    "CoefficientType",
    "GeometricInterpreter",
    "GeometricInterpretation",
    "GeometryType",
    "BriareusController",
    "SearchConfig",
    "SearchTarget",
    "SearchPriority",
    "BriareusResult",
    "STANDARD_PHYSICS_TARGETS",
    "OlympusBridge",
    "BridgeConfig",
    "integrate_with_olympusflow",
]
