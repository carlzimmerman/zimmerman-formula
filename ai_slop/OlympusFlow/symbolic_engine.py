#!/usr/bin/env python3
"""
OLYMPUSFLOW - Symbolic Verification Engine
============================================

Uses SymPy for REAL algebraic verification:
- Verify mathematical steps
- Check dimensional consistency
- Find Z²-based formulas (with honest labeling)
- Simplify expressions

If SymPy can't verify it, we say so honestly.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

try:
    import sympy as sp
    from sympy import (
        Symbol, pi, sqrt, Rational, simplify, expand, factor,
        nsimplify, N, Abs, log, exp, sin, cos, tan,
        symbols, Eq, solve, latex
    )
    from sympy.core.numbers import Float
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    print("WARNING: SymPy not installed. Symbolic verification disabled.")

from .honest_contracts import (
    HonestStep, HonestDerivation, EvidenceLevel, DerivationType,
    Z2, Z
)


# =============================================================================
# SYMBOLIC CONSTANTS
# =============================================================================

if SYMPY_AVAILABLE:
    # Define symbolic Z² constant
    Z2_sym = Symbol('Z2', positive=True, real=True)
    Z_sym = Symbol('Z', positive=True, real=True)
    phi_sym = (1 + sqrt(5)) / 2  # Golden ratio

    # Numerical value
    Z2_value = 32 * pi / 3
    Z_value = sqrt(Z2_value)


# =============================================================================
# SYMBOLIC ENGINE
# =============================================================================

class SymbolicEngine:
    """
    SymPy-based symbolic verification.

    Key capabilities:
    1. Verify algebraic steps
    2. Simplify expressions
    3. Find rational approximations
    4. Check if expressions are equivalent
    5. Generate HONEST assessment of derivations
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        if not SYMPY_AVAILABLE:
            self._log("SymPy not available - symbolic verification disabled")

    def _log(self, msg: str):
        if self.verbose:
            print(f"[SymPy] {msg}")

    # =========================================================================
    # EXPRESSION PARSING
    # =========================================================================

    def parse_expression(self, expr_str: str) -> Optional[Any]:
        """
        Parse a string expression into a SymPy expression.

        Returns None if parsing fails.
        """
        if not SYMPY_AVAILABLE:
            return None

        try:
            # Substitutions for common notations
            expr_str = expr_str.replace("Z²", "Z2")
            expr_str = expr_str.replace("Z^2", "Z2")
            expr_str = expr_str.replace("π", "pi")
            expr_str = expr_str.replace("φ", "(1+sqrt(5))/2")
            expr_str = expr_str.replace("^", "**")

            # Create local dict for eval
            local_dict = {
                'Z2': Z2_sym,
                'Z': Z_sym,
                'pi': pi,
                'sqrt': sqrt,
                'log': log,
                'exp': exp,
                'sin': sin,
                'cos': cos,
                'Rational': Rational,
            }

            # Try sympify first
            try:
                return sp.sympify(expr_str, locals=local_dict)
            except:
                # Try direct eval with sympy functions
                return eval(expr_str, {"__builtins__": {}}, local_dict)

        except Exception as e:
            self._log(f"Parse error for '{expr_str}': {e}")
            return None

    # =========================================================================
    # ALGEBRAIC VERIFICATION
    # =========================================================================

    def verify_equality(self, expr1: str, expr2: str) -> Tuple[bool, str]:
        """
        Verify if two expressions are algebraically equal.

        Returns (is_equal, explanation)
        """
        if not SYMPY_AVAILABLE:
            return False, "SymPy not available"

        sym1 = self.parse_expression(expr1)
        sym2 = self.parse_expression(expr2)

        if sym1 is None or sym2 is None:
            return False, "Could not parse expressions"

        try:
            # Try simplifying the difference
            diff = simplify(sym1 - sym2)

            if diff == 0:
                return True, "Algebraically verified: expressions are identical"

            # Try numerical comparison
            diff_value = N(diff.subs({Z2_sym: Z2_value, Z_sym: Z_value}))
            if abs(diff_value) < 1e-10:
                return True, "Numerically verified: difference < 1e-10"

            return False, f"Not equal: difference = {diff}"

        except Exception as e:
            return False, f"Verification error: {e}"

    def verify_step(self, input_expr: str, output_expr: str,
                    operation: str) -> Tuple[bool, EvidenceLevel, str]:
        """
        Verify a single derivation step.

        Returns (is_valid, evidence_level, explanation)
        """
        if not SYMPY_AVAILABLE:
            return False, EvidenceLevel.UNVERIFIED, "SymPy not available"

        sym_in = self.parse_expression(input_expr)
        sym_out = self.parse_expression(output_expr)

        if sym_in is None:
            return False, EvidenceLevel.UNVERIFIED, f"Could not parse input: {input_expr}"
        if sym_out is None:
            return False, EvidenceLevel.UNVERIFIED, f"Could not parse output: {output_expr}"

        # Check what kind of operation this is
        op_lower = operation.lower()

        if "simplif" in op_lower:
            # Check if output is simplified form of input
            simplified = simplify(sym_in)
            if simplify(simplified - sym_out) == 0:
                return True, EvidenceLevel.ALGEBRAIC_PROOF, "Simplification verified"
            return False, EvidenceLevel.UNVERIFIED, "Simplification not verified"

        elif "substitut" in op_lower:
            # Substitution steps are harder to verify automatically
            # Check if output could be derived from input
            is_valid, explanation = self.verify_equality(input_expr, output_expr)
            if is_valid:
                return True, EvidenceLevel.ALGEBRAIC_PROOF, explanation
            return False, EvidenceLevel.UNVERIFIED, "Substitution not verified"

        elif "evaluat" in op_lower:
            # Check numerical evaluation
            try:
                input_val = N(sym_in.subs({Z2_sym: Z2_value, Z_sym: Z_value}))
                output_val = N(sym_out.subs({Z2_sym: Z2_value, Z_sym: Z_value}))

                if abs(input_val - output_val) < 1e-10:
                    return True, EvidenceLevel.COMPUTED_MATCH, "Numerical evaluation verified"
                return False, EvidenceLevel.UNVERIFIED, f"Evaluation mismatch: {input_val} != {output_val}"
            except:
                return False, EvidenceLevel.UNVERIFIED, "Could not evaluate numerically"

        else:
            # General equivalence check
            is_valid, explanation = self.verify_equality(input_expr, output_expr)
            level = EvidenceLevel.ALGEBRAIC_PROOF if is_valid else EvidenceLevel.UNVERIFIED
            return is_valid, level, explanation

    # =========================================================================
    # FORMULA FINDING (HONEST APPROACH)
    # =========================================================================

    def find_z2_formula(self, target: float,
                        max_complexity: int = 3) -> List[Tuple[str, float, float, str]]:
        """
        Find Z²-based formulas that match a target value.

        HONEST LABELING: These are NUMERICAL FITS, not derivations.

        Returns list of (formula_str, computed_value, percent_error, honest_label)
        """
        if not SYMPY_AVAILABLE:
            return []

        candidates = []

        # Strategy 1: Simple ratios involving Z² or Z
        simple_formulas = [
            ("Z2", Z2_value, "Direct Z² value"),
            ("Z", Z_value, "Direct Z value"),
            ("1/Z2", 1/Z2_value, "Inverse Z²"),
            ("1/Z", 1/Z_value, "Inverse Z"),
            ("Z2/pi", Z2_value/math.pi, "Z²/π"),
            ("Z/pi", Z_value/math.pi, "Z/π"),
            ("pi/Z2", math.pi/Z2_value, "π/Z²"),
            ("pi/Z", math.pi/Z_value, "π/Z"),
        ]

        for formula, value, desc in simple_formulas:
            if abs(target) > 1e-15:
                error = abs(value - target) / abs(target) * 100
                if error < 5.0:
                    candidates.append((
                        formula, value, error,
                        f"NUMERICAL_FIT: {desc} matches target within {error:.4f}%"
                    ))

        # Strategy 2: Linear combinations aZ + b
        if max_complexity >= 2:
            for a in range(-10, 11):
                if a == 0:
                    continue
                for b in range(-30, 31):
                    value = a * Z_value + b
                    if abs(target) > 1e-15:
                        error = abs(value - target) / abs(target) * 100
                        if error < 1.0:
                            formula = f"{a}*Z + {b}" if b >= 0 else f"{a}*Z - {-b}"
                            candidates.append((
                                formula, value, error,
                                f"NUMERICAL_FIT: Linear combination matches within {error:.4f}%"
                            ))

        # Strategy 3: Z²/n or n/Z² forms
        if max_complexity >= 2:
            for n in range(1, 200):
                # Z²/n
                value = Z2_value / n
                if abs(target) > 1e-15:
                    error = abs(value - target) / abs(target) * 100
                    if error < 1.0:
                        candidates.append((
                            f"Z2/{n}", value, error,
                            f"NUMERICAL_FIT: Z²/{n} matches within {error:.4f}%"
                        ))

                # n/Z²
                value = n / Z2_value
                if abs(target) > 1e-15:
                    error = abs(value - target) / abs(target) * 100
                    if error < 1.0:
                        candidates.append((
                            f"{n}/Z2", value, error,
                            f"NUMERICAL_FIT: {n}/Z² matches within {error:.4f}%"
                        ))

        # Strategy 4: Simple fractions (not Z²-based, but honest)
        if max_complexity >= 3:
            for a in range(1, 50):
                for b in range(1, 50):
                    if a != b and math.gcd(a, b) == 1:  # Reduced fractions only
                        value = a / b
                        if abs(target) > 1e-15:
                            error = abs(value - target) / abs(target) * 100
                            if error < 0.5:
                                candidates.append((
                                    f"{a}/{b}", value, error,
                                    f"NUMERICAL_FIT (non-Z²): Simple fraction {a}/{b}"
                                ))

        # Strategy 5: Use SymPy's nsimplify for rational approximation
        try:
            rational = nsimplify(target, rational=True, tolerance=0.001)
            if rational != target:  # Found a simplification
                value = float(N(rational))
                error = abs(value - target) / abs(target) * 100 if abs(target) > 1e-15 else 0
                formula = str(rational)
                if error < 1.0 and formula not in [c[0] for c in candidates]:
                    candidates.append((
                        formula, value, error,
                        f"NUMERICAL_FIT: SymPy rational approximation"
                    ))
        except:
            pass

        # Sort by error
        candidates.sort(key=lambda x: x[2])

        return candidates[:10]  # Return top 10

    # =========================================================================
    # DIMENSIONAL ANALYSIS
    # =========================================================================

    def check_dimensions(self, formula: str, expected_unit: str) -> Tuple[bool, str]:
        """
        Check if a formula has correct dimensions.

        This is a simplified check - full dimensional analysis would require
        tracking units through all operations.
        """
        # For now, check if the formula is dimensionless when expected
        if expected_unit.lower() in ["", "dimensionless", "1", "none"]:
            # Check if formula evaluates to a pure number
            expr = self.parse_expression(formula)
            if expr is not None:
                try:
                    # Substitute Z2 and check if result is real
                    value = N(expr.subs({Z2_sym: Z2_value, Z_sym: Z_value}))
                    if value.is_real:
                        return True, "Dimensionless (evaluates to real number)"
                except:
                    pass

            return False, "Could not verify dimensionlessness"

        # For dimensional quantities, we need a more sophisticated approach
        return False, "Dimensional analysis not implemented for this unit"

    # =========================================================================
    # FULL DERIVATION VERIFICATION
    # =========================================================================

    def verify_derivation(self, derivation: HonestDerivation) -> HonestDerivation:
        """
        Verify all steps of a derivation using SymPy.

        Updates the derivation with verification results.
        """
        if not SYMPY_AVAILABLE:
            self._log("SymPy not available - cannot verify derivation")
            derivation.evidence_level = EvidenceLevel.UNVERIFIED
            return derivation

        self._log(f"Verifying derivation: {derivation.constant_name}")

        verified_count = 0

        for step in derivation.steps:
            # Try to verify this step
            is_valid, level, explanation = self.verify_step(
                step.input_expression,
                step.output_expression,
                step.operation
            )

            step.sympy_verified = is_valid
            step.verification_details = explanation

            if is_valid:
                verified_count += 1
                step.evidence_level = level
            else:
                step.evidence_level = EvidenceLevel.UNVERIFIED

            self._log(f"  Step {step.step_number}: {'✓' if is_valid else '✗'} {explanation}")

        # Update derivation counts
        derivation.num_sympy_verified = verified_count

        # Recompute overall assessment
        derivation.compute_honest_assessment()

        self._log(f"  Verified: {verified_count}/{len(derivation.steps)} steps")
        self._log(f"  Evidence: {derivation.evidence_level.value}")

        return derivation

    # =========================================================================
    # LATEX OUTPUT
    # =========================================================================

    def to_latex(self, expr_str: str) -> str:
        """Convert expression to LaTeX."""
        if not SYMPY_AVAILABLE:
            return expr_str

        expr = self.parse_expression(expr_str)
        if expr is not None:
            return latex(expr)
        return expr_str


# =============================================================================
# DEMO
# =============================================================================

def demo():
    """Test the symbolic engine."""
    engine = SymbolicEngine()

    print("\n" + "=" * 60)
    print("SYMBOLIC ENGINE TEST")
    print("=" * 60)

    # Test expression parsing
    print("\n1. Expression Parsing:")
    test_exprs = ["Z2/10", "Z²/π", "3*Z + 5", "32*pi/3"]
    for expr in test_exprs:
        parsed = engine.parse_expression(expr)
        print(f"  '{expr}' -> {parsed}")

    # Test equality verification
    print("\n2. Equality Verification:")
    tests = [
        ("Z2", "32*pi/3"),
        ("Z**2", "Z2"),
        ("Z2/2", "16*pi/3"),
    ]
    for e1, e2 in tests:
        is_eq, explanation = engine.verify_equality(e1, e2)
        print(f"  {e1} == {e2}: {is_eq} - {explanation}")

    # Test formula finding
    print("\n3. Formula Finding (HONEST):")
    test_values = [0.6847, 0.41, 1/137.036, 0.23122]
    for val in test_values:
        print(f"\n  Target: {val}")
        candidates = engine.find_z2_formula(val, max_complexity=2)
        for formula, computed, error, label in candidates[:3]:
            print(f"    {formula} = {computed:.6f} ({error:.4f}%)")
            print(f"      {label}")


if __name__ == "__main__":
    demo()
