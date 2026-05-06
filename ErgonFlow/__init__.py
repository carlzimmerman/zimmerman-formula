"""
ErgonFlow - Action Principle Derivation Engine
==============================================

Derives the physical action principles (Lagrangians) that REQUIRE
Z² relationships to be true.

Named after Ergon (Greek: work/action) - the fundamental quantity
in the principle of least action.

Components:
- ActionDeriver: Main derivation engine
- LagrangianTemplates: Standard physics Lagrangians
- DomainAnalyzer: Maps domains to physics frameworks
- ProofVerifier: Checks mathematical rigor
- Z2Interpreter: Geometric meanings of Z²

Author: Carl Zimmerman
Date: May 6, 2026
Version: 1.0.0
"""

from pathlib import Path

__version__ = "1.0.0"
__author__ = "Carl Zimmerman"

# Module directory
ERGON_DIR = Path(__file__).parent

# Try to import main components (will be added incrementally)
try:
    from ErgonFlow.action_deriver import ActionDeriver, ActionDerivation
except ImportError:
    ActionDeriver = None
    ActionDerivation = None

try:
    from ErgonFlow.lagrangian_templates import LAGRANGIAN_TEMPLATES
except ImportError:
    LAGRANGIAN_TEMPLATES = {}

__all__ = [
    "ActionDeriver",
    "ActionDerivation",
    "LAGRANGIAN_TEMPLATES",
    "__version__",
]
