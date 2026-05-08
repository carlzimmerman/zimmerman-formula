#!/usr/bin/env python3
"""
OLYMPUSFLOW - Centralized Constants
====================================

Single source of truth for all Z² related constants and thresholds.
Import from this module to ensure consistency across all components.

Z² = 32π/3 ≈ 33.510321638291124

This is the fundamental constant of the Zimmerman Formula that appears
in physical ratios across multiple domains when reality is viewed as
constraint-based rather than dynamics-based.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import math

# =============================================================================
# FUNDAMENTAL Z² CONSTANTS
# =============================================================================

# The Zimmerman Constant: Z² = 32π/3
Z2 = 32 * math.pi / 3  # ≈ 33.510321638291124

# Square root of Z²
Z = math.sqrt(Z2)  # ≈ 5.788810099304589

# Golden ratio (related through Z²)
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.6180339887498949

# Inverse golden ratio
INV_PHI = 1 / PHI  # ≈ 0.6180339887498949

# Pi
PI = math.pi  # ≈ 3.141592653589793

# Euler's number
E = math.e  # ≈ 2.718281828459045

# =============================================================================
# DERIVED Z² TARGETS
# =============================================================================

# Common Z² patterns found in empirical data
Z2_TARGETS = {
    "Z²": Z2,              # 33.510...
    "Z": Z,                # 5.788...
    "Z²/10": Z2 / 10,      # 3.351...
    "Z²/π": Z2 / math.pi,  # 10.666... = 32/3
    "Z/π": Z / math.pi,    # 1.842...
    "φ": PHI,              # 1.618...
    "1/φ": INV_PHI,        # 0.618...
    "π": PI,               # 3.141...
    "e": E,                # 2.718...
    "√2": math.sqrt(2),    # 1.414...
    "√3": math.sqrt(3),    # 1.732...
}

# =============================================================================
# HRM (HYGIENIC RIGOR MEASURE) THRESHOLDS
# =============================================================================

class HRMThresholds:
    """Thresholds for HRM assessment across the pipeline."""

    # Status assignment thresholds
    VALIDATED = 0.8          # Score >= 0.8 → VALIDATED status
    SPECULATIVE = 0.5        # Score >= 0.5 → SPECULATIVE status
    PENDING = 0.3            # Score >= 0.3 → PENDING status
    # Score < 0.3 → REJECTED status

    # Deepening trigger thresholds
    HIGHLY_SIGNIFICANT = 0.8   # Immediate deepening
    MODERATELY_SIGNIFICANT = 0.5  # Batch deepening

    # Training thresholds
    MIN_FOR_TRAINING = 0.6   # Minimum score to include in training data

    # Graduation thresholds (MnemosyneLake → training)
    MIN_FOR_GRADUATION = 0.7  # Minimum score to graduate to training

# =============================================================================
# PATTERN MATCHING THRESHOLDS
# =============================================================================

class PatternThresholds:
    """Thresholds for pattern detection."""

    # Maximum percent error to consider a match
    SIGNIFICANT_ERROR = 5.0   # < 5% error is significant
    REMARKABLE_ERROR = 1.0    # < 1% error is remarkable
    EXACT_ERROR = 0.1         # < 0.1% error is exact

    # Minimum sample size
    MIN_SAMPLES = 30          # Statistical significance

    # Coefficient of variation significance
    CV_SIGNIFICANT = 0.5      # CV matching target within CV_SIGNIFICANT is notable

# =============================================================================
# VALIDATION THRESHOLDS
# =============================================================================

class ValidationThresholds:
    """Thresholds for data validation."""

    # Minimum data quality
    MIN_DATA_POINTS = 30
    MIN_COLUMNS = 2

    # Authority scoring
    AUTHORITATIVE_SCORE = 0.9   # .gov, .edu, known institutions
    INSTITUTIONAL_SCORE = 0.7   # Universities, labs
    SECONDARY_SCORE = 0.5       # Compilations, encyclopedias
    UNVERIFIED_SCORE = 0.3      # Unknown provenance

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_target(name: str) -> float:
    """Get a Z² target value by name."""
    return Z2_TARGETS.get(name, 0.0)


def matches_z2_target(value: float, max_error: float = 5.0) -> tuple:
    """
    Check if a value matches any Z² target.

    Returns:
        Tuple of (matched, target_name, target_value, percent_error)
    """
    for name, target in Z2_TARGETS.items():
        if target > 0:
            error = abs(value - target) / target * 100
            if error < max_error:
                return (True, name, target, error)
    return (False, None, None, None)


def hrm_to_status(hrm_score: float) -> str:
    """Convert HRM score to status string."""
    if hrm_score >= HRMThresholds.VALIDATED:
        return "validated"
    elif hrm_score >= HRMThresholds.SPECULATIVE:
        return "speculative"
    elif hrm_score >= HRMThresholds.PENDING:
        return "pending"
    else:
        return "rejected"


# =============================================================================
# MODULE INFO
# =============================================================================

__version__ = "3.0.0"
__all__ = [
    "Z2", "Z", "PHI", "INV_PHI", "PI", "E",
    "Z2_TARGETS",
    "HRMThresholds", "PatternThresholds", "ValidationThresholds",
    "get_target", "matches_z2_target", "hrm_to_status"
]


if __name__ == "__main__":
    print("OlympusFlow Constants")
    print("=" * 50)
    print(f"Z² = 32π/3 = {Z2:.10f}")
    print(f"Z  = √(Z²) = {Z:.10f}")
    print(f"φ  = (1+√5)/2 = {PHI:.10f}")
    print()
    print("Z² Targets:")
    for name, value in Z2_TARGETS.items():
        print(f"  {name:8} = {value:.6f}")
