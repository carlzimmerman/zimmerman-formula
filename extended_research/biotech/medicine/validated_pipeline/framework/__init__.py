"""
ZUGF Systematic Computational Biology Framework

A rigorous, honest approach to computational drug discovery.
No heuristics. No slop. Physics-based validation only.

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

__version__ = "1.0.0"
__author__ = "Carl Zimmerman"

# Validation tiers
TIER_0_LITERATURE = 0      # Data from external sources
TIER_1_CHEMISTRY = 1       # RDKit validated
TIER_2_STRUCTURE = 2       # ESMFold/AlphaFold predicted
TIER_3_DOCKED = 3          # AutoDock Vina scored
TIER_4_MD_STABLE = 4       # 50ns MD stable
TIER_5_BINDING_ENERGY = 5  # MM-PBSA calculated
TIER_6_EXPERIMENTAL = 6    # SPR/ITC measured

TIER_NAMES = {
    0: "Literature/Database",
    1: "Chemically Valid",
    2: "Structure Predicted",
    3: "Docked",
    4: "MD Stable",
    5: "Binding Energy Calculated",
    6: "Experimentally Validated"
}
