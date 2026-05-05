#!/usr/bin/env python3
"""
TRUTHFLOW - Z² Validation Pipeline
====================================

Self-discovering validation system that accumulates empirical evidence
for Z² predictions against official measurements.

Features:
1. Formula discovery - search for Z² relationships
2. Data fetching - get real measurements from databases
3. Script generation - create verification code
4. Accumulation - validated predictions added to framework
5. Falsification tracking - failures are logged honestly

Author: Carl Zimmerman
Date: May 3, 2026
"""

__version__ = "1.0.0"

from .truth_engine import (
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
