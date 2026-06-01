"""
TRUTHFLOW - Z2 Validation Pipeline
===================================

DEPRECATED: This module has moved to OlympusFlow.flows.truth

Please update imports:
    OLD: from TruthFlow import TruthEngine
    NEW: from OlympusFlow.flows.truth import TruthEngine

    OR: from OlympusFlow.flows import TruthEngine

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "TruthFlow has moved to OlympusFlow.flows.truth. "
    "Please update imports: from OlympusFlow.flows.truth import TruthEngine",
    DeprecationWarning,
    stacklevel=2
)

__version__ = "1.0.0"

# Re-export from new location
from OlympusFlow.flows.truth import (
    TruthEngine,
    FormulaGenerator,
    Prediction,
    Discovery,
    safe_eval,
    Z2, Z,
    MEASUREMENT_DB,
    MATH_CONTEXT
)

__all__ = [
    "__version__",
    "TruthEngine",
    "FormulaGenerator",
    "Prediction",
    "Discovery",
    "safe_eval",
    "Z2", "Z",
    "MEASUREMENT_DB",
    "MATH_CONTEXT"
]
