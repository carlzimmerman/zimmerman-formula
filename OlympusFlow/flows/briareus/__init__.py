"""
BRIAREUSFLOW - The Hundred-Handed Phenomenological Discovery Engine
====================================================================

Named after Briareus (Aegaeon), the hundred-handed giant of Greek mythology.
Fitting for a multi-threaded brute-force search engine.

BriareusFlow is the PUBLIC equivalent of the private BruteFlow.
It systematically explores phenomenological patterns:

1. Takes findings with empirical evidence but incomplete proofs
2. Brute-force searches for mathematical patterns
3. Tests dimensional consistency
4. Identifies simple coefficients (π, √2, Z², etc.)
5. Classifies by derivation level (PHENOMENOLOGICAL vs FIRST_PRINCIPLES)
6. Feeds discoveries to OlympusFlow for rigorous validation

Key Difference from OlympusFlow:
- OlympusFlow REJECTS numerology (requires physical mechanism)
- BriareusFlow EXPLORES phenomenological patterns that MIGHT have mechanisms
- BriareusFlow is exploratory; OlympusFlow is validating

Author: Carl Zimmerman
Date: May 6, 2026
Version: 1.0.0
"""

from .phenomenological import (
    PhenomenologicalFinding,
    FindingCategory,
    DiscoveryPath,
    DiscoveryMethod,
    NumerologyRisk,
    AlternativeFit,
    FindingBatch,
    Z_SQUARED,
    Z,
    PHI
)

from .pattern_search import (
    PatternSearchEngine,
    SearchResult,
    CoefficientMatch,
    PatternMatch,
    CoefficientType
)

from .geometric_interpreter import (
    GeometricInterpreter,
    GeometricInterpretation,
    GeometryType
)

from .briareus_controller import (
    BriareusController,
    SearchConfig,
    SearchTarget,
    SearchPriority,
    BriareusResult,
    STANDARD_PHYSICS_TARGETS
)

from .olympus_bridge import (
    OlympusBridge,
    BridgeConfig,
    integrate_with_olympusflow
)

__version__ = "1.0.0"
__all__ = [
    # Phenomenological
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
    # Pattern search
    "PatternSearchEngine",
    "SearchResult",
    "CoefficientMatch",
    "PatternMatch",
    "CoefficientType",
    # Geometric interpreter
    "GeometricInterpreter",
    "GeometricInterpretation",
    "GeometryType",
    # Controller
    "BriareusController",
    "SearchConfig",
    "SearchTarget",
    "SearchPriority",
    "BriareusResult",
    "STANDARD_PHYSICS_TARGETS",
    # OlympusFlow bridge
    "OlympusBridge",
    "BridgeConfig",
    "integrate_with_olympusflow"
]
