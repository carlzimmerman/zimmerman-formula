"""
TRUTHFLOW - Z2 Validation Pipeline
===================================

Self-discovering validation system that accumulates empirical evidence
for Z2 predictions against official measurements.

Features:
1. Formula discovery - search for Z2 relationships
2. Data fetching - get real measurements from databases
3. Script generation - create verification code
4. Accumulation - validated predictions added to framework
5. Falsification tracking - failures are logged honestly

Submodules:
- 01_fetcher: Fetch papers from arXiv
- 02_parser: Extract empirical values
- 03_compute: HRM validation and Z2 engine
- 04_assessor: Validate Z2 predictions
- 05_assessor: Turing evaluation

Usage:
    from OlympusFlow.flows.truth import TruthEngine, FormulaGenerator

    engine = TruthEngine()
    predictions = engine.discover("fine_structure_constant")
"""

__version__ = "3.0.0"

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
