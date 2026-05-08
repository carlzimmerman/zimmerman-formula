"""
ERGONFLOW - Action Principle Derivations
=========================================

Named after Ergon, the Greek word for work/action.

This flow derives Lagrangians and action principles that REQUIRE
Z2 relationships to be true. The goal is to show that Z2 emerges
from fundamental physics, not just numerology.

Architecture:
- ActionDeriver: Main derivation engine
- LagrangianTemplates: Standard physics templates
- Z2 potential terms added to Lagrangians

Usage:
    from OlympusFlow.flows.ergon import ActionDeriver, ActionDerivation

    deriver = ActionDeriver()
    result = deriver.derive_action("electromagnetism", target_constant=137.036)
"""

from .action_deriver import ActionDeriver, ActionDerivation
from .lagrangian_templates import (
    LAGRANGIAN_TEMPLATES,
    LagrangianTemplate,
    PhysicsFramework,
    get_templates_for_domain,
    get_template_with_z2_potential,
)

__version__ = "3.0.0"
__all__ = [
    "ActionDeriver",
    "ActionDerivation",
    "LAGRANGIAN_TEMPLATES",
    "LagrangianTemplate",
    "PhysicsFramework",
    "get_templates_for_domain",
    "get_template_with_z2_potential",
]
