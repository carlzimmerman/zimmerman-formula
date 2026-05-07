"""
ERGONFLOW - Action Principle Derivations
=========================================

DEPRECATED: This module has moved to OlympusFlow.flows.ergon

Please update imports:
    OLD: from ErgonFlow import ActionDeriver
    NEW: from OlympusFlow.flows.ergon import ActionDeriver

    OR: from OlympusFlow.flows import ActionDeriver

This file re-exports from the new location for backward compatibility.
"""

import warnings

warnings.warn(
    "ErgonFlow has moved to OlympusFlow.flows.ergon. "
    "Please update imports: from OlympusFlow.flows.ergon import ActionDeriver",
    DeprecationWarning,
    stacklevel=2
)

# Re-export from new location
from OlympusFlow.flows.ergon import (
    ActionDeriver,
    ActionDerivation,
    LAGRANGIAN_TEMPLATES,
    LagrangianTemplate,
    PhysicsFramework,
    get_templates_for_domain,
    get_template_with_z2_potential,
)

__version__ = "1.0.0"
__all__ = [
    "ActionDeriver",
    "ActionDerivation",
    "LAGRANGIAN_TEMPLATES",
    "LagrangianTemplate",
    "PhysicsFramework",
    "get_templates_for_domain",
    "get_template_with_z2_potential",
]
