#!/usr/bin/env python3
"""
Turing Evaluation Node - Z² Framework Validation Gatekeeper
=============================================================

This script acts as the final gatekeeper for Z² derivations.
When LegomenaLLM generates a new geometric proof, this script
intercepts and validates it against the established Z² axioms.

The Turing Evaluator checks:
1. Does the proof violate Z² = 32π/3?
2. Does it violate the 12 = 8+3+1 edge partition?
3. Does it introduce variables not derived from those constraints?
4. Is the numerical prediction within experimental bounds?
5. Is there a physical mechanism (HRM > 0.7)?

If any check fails, the proof is rejected to failed_attempts/.

Author: Carl Zimmerman
License: AGPL-3.0
"""

import re
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import json
import sympy as sp
from datetime import datetime

# ============================================================================
# FUNDAMENTAL Z² AXIOMS (IMMUTABLE)
# ============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.510321638291124
Z = np.sqrt(Z2)       # ≈ 5.788817455565272

# Derived topological constants
CUBE_VERTICES = 8
CUBE_EDGES = 12
CUBE_FACES = 6

# Gauge partition (edges)
GAUGE_PARTITION = {
    "SU3_gluons": 8,
    "SU2_weak": 3,
    "U1_photon": 1,
    "total": 12
}

# Cosmological fractions (from partition function)
OMEGA_LAMBDA = 13/19  # ≈ 0.6842
OMEGA_MATTER = 6/19   # ≈ 0.3158

# Bekenstein dimension
BEKENSTEIN = 4  # Macroscopic spacetime dimensions

# Generations
N_GEN = 3  # Number of fermion generations

# Spectral dimension limits
D_S_PLANCK = 2  # At Planck scale
D_S_MACRO = 4   # At macroscopic scales


class ValidationError(Exception):
    """Raised when a derivation violates Z² axioms."""
    pass


class NumerologyError(ValidationError):
    """Raised when a derivation is deemed numerological."""
    pass


class TheoreticalViolationError(ValidationError):
    """Raised when a derivation violates fundamental Z² constraints."""
    pass


@dataclass
class ValidationResult:
    """Result of Turing evaluation."""
    passed: bool
    derivation_name: str
    z2_consistent: bool
    gauge_consistent: bool
    numerical_match: bool
    hrm_score: float
    violations: List[str]
    warnings: List[str]
    formula: str
    predicted_value: float
    experimental_value: float
    percent_error: float
    timestamp: str


class TuringEvaluator:
    """
    Turing Evaluation Node for Z² derivations.

    Validates that all derivations conform to the fundamental
    axioms of the Z² unified framework.
    """

    def __init__(self, strict_mode: bool = True):
        """
        Initialize the Turing Evaluator.

        Args:
            strict_mode: If True, any violation causes rejection.
                        If False, warnings are issued but derivation continues.
        """
        self.strict_mode = strict_mode
        self.allowed_constants = self._build_allowed_constants()
        self.allowed_symbols = self._build_allowed_symbols()

    def _build_allowed_constants(self) -> Dict[str, float]:
        """Build dictionary of allowed Z² constants."""
        return {
            "Z2": Z2,
            "Z": Z,
            "Z_squared": Z2,
            "pi": np.pi,
            "e": np.e,
            "phi": (1 + np.sqrt(5)) / 2,  # Golden ratio (geometrically derived)
            "cube_vertices": 8,
            "cube_edges": 12,
            "cube_faces": 6,
            "octahedron_vertices": 6,
            "octahedron_edges": 12,
            "octahedron_faces": 8,
            "bekenstein": 4,
            "n_gen": 3,
            "gauge_total": 12,
            "su3_dim": 8,
            "su2_dim": 3,
            "u1_dim": 1,
            "omega_lambda": 13/19,
            "omega_matter": 6/19,
            "d_s_planck": 2,
            "d_s_macro": 4,
        }

    def _build_allowed_symbols(self) -> set:
        """Build set of allowed symbolic variables."""
        return {
            # Geometric
            "Z", "Z2", "Z_squared", "pi", "phi",
            # Topological
            "n_vertices", "n_edges", "n_faces", "n_gen", "d",
            # Cosmological
            "Omega_Lambda", "Omega_m", "H0", "a0",
            # Gauge
            "GAUGE", "SU3", "SU2", "U1", "g1", "g2", "g3",
            # Standard allowed physics
            "c", "hbar", "G", "k_B", "alpha", "sin_theta_W",
        }

    def validate_derivation(self, derivation: Dict[str, Any]) -> ValidationResult:
        """
        Validate a derivation against Z² axioms.

        Args:
            derivation: Dictionary containing:
                - name: Name of the constant/quantity
                - formula: The Z² formula (string or SymPy)
                - predicted: Numerical prediction
                - experimental: Experimental value
                - uncertainty: Experimental uncertainty
                - reasoning: Physical reasoning (for HRM)

        Returns:
            ValidationResult with pass/fail status and details
        """
        violations = []
        warnings = []

        name = derivation.get("name", "unknown")
        formula = derivation.get("formula", "")
        predicted = derivation.get("predicted", 0)
        experimental = derivation.get("experimental", 0)
        uncertainty = derivation.get("uncertainty", 0)
        reasoning = derivation.get("reasoning", "")

        # 1. Check Z² consistency
        z2_consistent = self._check_z2_consistency(formula, violations)

        # 2. Check gauge partition consistency
        gauge_consistent = self._check_gauge_consistency(formula, violations)

        # 3. Check for forbidden symbols
        self._check_forbidden_symbols(formula, violations, warnings)

        # 4. Check numerical match
        numerical_match, percent_error = self._check_numerical_match(
            predicted, experimental, uncertainty, violations
        )

        # 5. Calculate HRM score
        hrm_score = self._calculate_hrm_score(
            formula, reasoning, numerical_match, percent_error
        )

        # Determine pass/fail
        if self.strict_mode:
            passed = (len(violations) == 0 and hrm_score >= 0.7)
        else:
            passed = (hrm_score >= 0.5 and numerical_match)

        return ValidationResult(
            passed=passed,
            derivation_name=name,
            z2_consistent=z2_consistent,
            gauge_consistent=gauge_consistent,
            numerical_match=numerical_match,
            hrm_score=hrm_score,
            violations=violations,
            warnings=warnings,
            formula=str(formula),
            predicted_value=predicted,
            experimental_value=experimental,
            percent_error=percent_error,
            timestamp=datetime.now().isoformat()
        )

    def _check_z2_consistency(self, formula: str, violations: List[str]) -> bool:
        """
        Check if formula uses Z² = 32π/3 correctly.

        Returns True if consistent, False otherwise.
        """
        # Convert to string if needed
        formula_str = str(formula).lower()

        # Check if Z² is used
        has_z2 = any(z in formula_str for z in ['z2', 'z²', 'z^2', 'z_squared', '32*pi/3', '32π/3'])

        # If formula claims to use Z² but uses wrong value
        if has_z2:
            # Try to extract numerical coefficient
            z2_matches = re.findall(r'(\d+(?:\.\d+)?)\s*[\*×]\s*(?:z2|z²|z\^2)', formula_str)
            for match in z2_matches:
                coeff = float(match)
                # Check if coefficient makes sense geometrically
                if coeff not in [1, 2, 3, 4, 6, 8, 12, 1/2, 1/3, 1/4, 1/6, 1/8, 1/12]:
                    violations.append(f"Non-geometric coefficient {coeff} multiplying Z²")

        return len([v for v in violations if "Z²" in v]) == 0

    def _check_gauge_consistency(self, formula: str, violations: List[str]) -> bool:
        """
        Check if formula respects 12 = 8+3+1 gauge partition.

        Returns True if consistent, False otherwise.
        """
        formula_str = str(formula).lower()

        # Check for gauge structure references
        gauge_numbers = re.findall(r'\b(8|3|1|12|11|13)\b', formula_str)

        # 11 is suspicious - should be 12
        if '11' in gauge_numbers and '12' not in gauge_numbers:
            violations.append("Used 11 instead of GAUGE=12 (8+3+1)")

        # 13 is valid in two contexts:
        # 1. 13/19 for Ω_Λ (dark energy)
        # 2. 13 = 12+1 for gauge + hypercharge (sin²θ_W = 3/13)
        if '13' in gauge_numbers:
            valid_13_use = ('19' in formula_str or  # Ω_Λ = 13/19
                           '3/13' in formula_str or  # sin²θ_W = 3/13
                           '12' in gauge_numbers)    # 13 = 12+1 explicit
            if not valid_13_use:
                violations.append("Used 13 in unclear context (valid: 13/19 for Ω_Λ or 3/13 for sin²θ_W)")

        return len([v for v in violations if "gauge" in v.lower()]) == 0

    def _check_forbidden_symbols(
        self, formula: str, violations: List[str], warnings: List[str]
    ):
        """
        Check for symbols not derivable from Z² geometry.
        """
        formula_str = str(formula)

        # Extract all variable names
        variables = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', formula_str))

        # Remove common math functions
        math_funcs = {'sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'arcsin', 'arccos',
                      'arctan', 'sinh', 'cosh', 'tanh', 'abs', 'pi'}
        variables -= math_funcs

        # Check each variable
        for var in variables:
            if var.lower() not in {k.lower() for k in self.allowed_constants}:
                if var.lower() not in {s.lower() for s in self.allowed_symbols}:
                    if self.strict_mode:
                        violations.append(f"Forbidden symbol: {var}")
                    else:
                        warnings.append(f"Unrecognized symbol: {var}")

    def _check_numerical_match(
        self,
        predicted: float,
        experimental: float,
        uncertainty: float,
        violations: List[str]
    ) -> Tuple[bool, float]:
        """
        Check if predicted value matches experimental within uncertainty.

        Returns (match_status, percent_error).
        """
        if experimental == 0:
            if predicted == 0:
                return True, 0.0
            else:
                violations.append("Experimental value is 0 but prediction is non-zero")
                return False, float('inf')

        percent_error = abs(predicted - experimental) / abs(experimental) * 100

        if uncertainty > 0:
            sigma_tension = abs(predicted - experimental) / uncertainty
            if sigma_tension > 5:
                violations.append(f"Prediction {sigma_tension:.1f}σ away from experiment")
                return False, percent_error
        else:
            # No uncertainty given - use 1% threshold
            if percent_error > 1.0:
                violations.append(f"Prediction error {percent_error:.2f}% exceeds 1%")
                return False, percent_error

        return True, percent_error

    def _calculate_hrm_score(
        self,
        formula: str,
        reasoning: str,
        numerical_match: bool,
        percent_error: float
    ) -> float:
        """
        Calculate Hypothesis Rigor Metric (HRM) score.

        Components:
        - Numerical match: 30%
        - Formula simplicity: 20%
        - Physical mechanism: 30%
        - Z² connection strength: 20%

        Returns score in [0, 1].
        """
        score = 0.0

        # 1. Numerical match (30%)
        if numerical_match:
            if percent_error < 0.1:
                score += 0.30
            elif percent_error < 1.0:
                score += 0.25
            elif percent_error < 5.0:
                score += 0.15
            else:
                score += 0.05

        # 2. Formula simplicity (20%)
        formula_str = str(formula)
        # Simpler formulas get higher scores
        n_operations = len(re.findall(r'[\+\-\*\/\^\(\)]', formula_str))
        if n_operations <= 3:
            score += 0.20
        elif n_operations <= 6:
            score += 0.15
        elif n_operations <= 10:
            score += 0.10
        else:
            score += 0.05

        # 3. Physical mechanism (30%)
        reasoning_lower = reasoning.lower()
        mechanism_keywords = [
            'geometry', 'topology', 'symmetry', 'gauge', 'dimension',
            'vertex', 'edge', 'face', 'cube', 'sphere', 'holography',
            'bekenstein', 'entropy', 'horizon', 'planck', 'partition'
        ]
        keyword_count = sum(1 for kw in mechanism_keywords if kw in reasoning_lower)
        if keyword_count >= 5:
            score += 0.30
        elif keyword_count >= 3:
            score += 0.20
        elif keyword_count >= 1:
            score += 0.10

        # 4. Z² connection strength (20%)
        formula_lower = formula_str.lower()
        z2_indicators = ['z2', 'z²', '32*pi/3', '32π/3', 'z_squared']
        if any(ind in formula_lower for ind in z2_indicators):
            # Direct Z² usage
            score += 0.20
        elif any(str(int(x)) in formula_str for x in [8, 12, 6]):
            # Uses cube numbers
            score += 0.15
        elif '13/19' in formula_str or '6/19' in formula_str:
            # Uses cosmological fractions
            score += 0.15
        elif 'pi' in formula_lower:
            # Uses π (geometrically connected)
            score += 0.10

        return min(1.0, score)

    def validate_against_known_truths(
        self, derivation: Dict[str, Any], truths_file: str
    ) -> bool:
        """
        Cross-validate derivation against known Z² truths.

        Args:
            derivation: The derivation to validate
            truths_file: Path to JSON file with verified truths

        Returns:
            True if consistent with known truths, False otherwise
        """
        try:
            with open(truths_file, 'r') as f:
                known_truths = json.load(f)
        except FileNotFoundError:
            return True  # No truths file = can't cross-validate

        name = derivation.get("name", "")
        predicted = derivation.get("predicted", 0)

        for truth in known_truths.get("verified", []):
            if truth.get("name") == name:
                truth_value = truth.get("value")
                if abs(predicted - truth_value) / truth_value > 0.01:
                    return False  # Contradicts known truth

        return True


def run_evaluation(derivation: Dict[str, Any], strict: bool = True) -> ValidationResult:
    """
    Run Turing evaluation on a derivation.

    Args:
        derivation: Derivation dictionary
        strict: Whether to use strict mode

    Returns:
        ValidationResult
    """
    evaluator = TuringEvaluator(strict_mode=strict)
    return evaluator.validate_derivation(derivation)


def example_derivations():
    """Test the evaluator with example derivations."""
    print("=" * 70)
    print("TURING EVALUATOR - EXAMPLE DERIVATIONS")
    print("=" * 70)

    evaluator = TuringEvaluator(strict_mode=True)

    # Good derivation: Weak mixing angle
    good_derivation = {
        "name": "sin²θ_W (weak mixing angle)",
        "formula": "3/13",
        "predicted": 3/13,
        "experimental": 0.23122,
        "uncertainty": 0.0004,
        "reasoning": """
        The weak mixing angle arises from the gauge structure.
        The 12 edges partition as 8+3+1.
        SU(2) has 3 generators, total gauge has 12+1=13.
        sin²θ_W = 3/13 from this partition.
        This is a direct consequence of cube geometry.
        """
    }

    result = evaluator.validate_derivation(good_derivation)
    print(f"\n{result.derivation_name}")
    print(f"  Passed: {result.passed}")
    print(f"  HRM Score: {result.hrm_score:.2f}")
    print(f"  Predicted: {result.predicted_value:.6f}")
    print(f"  Experimental: {result.experimental_value:.6f}")
    print(f"  Error: {result.percent_error:.4f}%")
    print(f"  Violations: {result.violations}")

    # Good derivation: Dark energy fraction
    good_derivation_2 = {
        "name": "Ω_Λ (dark energy fraction)",
        "formula": "13/19",
        "predicted": 13/19,
        "experimental": 0.6847,
        "uncertainty": 0.007,
        "reasoning": """
        From the cosmic partition function.
        13 = 8+5 relates to gauge + golden ratio structure.
        19 = 12+7 relates to edges + critical dimension.
        This emerges from holographic entropy counting on the
        cosmological horizon, constrained by Z² geometry.
        """
    }

    result = evaluator.validate_derivation(good_derivation_2)
    print(f"\n{result.derivation_name}")
    print(f"  Passed: {result.passed}")
    print(f"  HRM Score: {result.hrm_score:.2f}")
    print(f"  Error: {result.percent_error:.4f}%")

    # Bad derivation: Numerology
    bad_derivation = {
        "name": "random_constant",
        "formula": "1.337 * something_arbitrary",
        "predicted": 1.337,
        "experimental": 1.340,
        "uncertainty": 0.001,
        "reasoning": "I just found this number matches."
    }

    result = evaluator.validate_derivation(bad_derivation)
    print(f"\n{result.derivation_name}")
    print(f"  Passed: {result.passed}")
    print(f"  HRM Score: {result.hrm_score:.2f}")
    print(f"  Violations: {result.violations}")

    # PMNS derivation
    pmns_derivation = {
        "name": "sin²θ₁₃ (reactor angle)",
        "formula": "1/(Z² + 12)",
        "predicted": 1/(Z2 + 12),
        "experimental": 0.0220,
        "uncertainty": 0.0007,
        "reasoning": """
        The reactor angle arises from symmetry breaking.
        Z² = 32π/3 provides the geometric suppression.
        GAUGE = 12 edges provides additional suppression.
        Together: sin²θ₁₃ = 1/(Z² + 12).
        This explains why θ₁₃ is small but non-zero.
        """
    }

    result = evaluator.validate_derivation(pmns_derivation)
    print(f"\n{result.derivation_name}")
    print(f"  Passed: {result.passed}")
    print(f"  HRM Score: {result.hrm_score:.2f}")
    print(f"  Predicted: {result.predicted_value:.6f}")
    print(f"  Experimental: {result.experimental_value:.6f}")
    print(f"  Error: {result.percent_error:.4f}%")


if __name__ == "__main__":
    example_derivations()
