#!/usr/bin/env python3
"""
FORMULA GENERATOR - Expanded Z² Formula Search
===============================================

Generates candidate formulas for Z² derivations using multiple strategies:
1. Simple fractions (a/b) - finds patterns like 3/13 for sin²θ_W
2. Integer + Z² combinations (aZ² + b) - finds patterns like 4Z² + 3 for α⁻¹
3. Geometric functions (arccos, arctan)
4. π-based expressions
5. Compound expressions

Author: Carl Zimmerman
Date: May 6, 2026
Version: 2.0.0
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable
from enum import Enum
import sympy as sp


# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * math.pi / 3  # ≈ 33.510...
Z = math.sqrt(Z_SQUARED)       # ≈ 5.7888...
PHI = (1 + math.sqrt(5)) / 2   # Golden ratio


class FormulaType(Enum):
    """Types of formulas we can generate."""
    SIMPLE_FRACTION = "simple_fraction"      # a/b
    Z_POLYNOMIAL = "z_polynomial"            # aZ + b, aZ² + b
    Z_FRACTION = "z_fraction"                # a/Z, a/Z²
    PI_BASED = "pi_based"                    # π/a, aπ
    GEOMETRIC = "geometric"                   # arccos(a/b), arctan(a/b)
    COMPOUND = "compound"                     # (aZ + b)/(cZ + d)
    INTEGER_Z2 = "integer_z2"                # aZ² + b (integers)
    KNOWN_FIRST_PRINCIPLES = "known_first_principles"


@dataclass
class FormulaCandidate:
    """A candidate formula with its evaluation."""
    formula_str: str
    formula_type: FormulaType
    computed_value: float
    target_value: float
    percent_error: float
    parameters: Dict[str, float] = field(default_factory=dict)
    latex: str = ""
    physical_hint: str = ""

    def __post_init__(self):
        if not self.latex:
            self.latex = self.formula_str


@dataclass
class FormulaSearchResult:
    """Result of a formula search."""
    target_value: float
    candidates: List[FormulaCandidate]
    best_match: Optional[FormulaCandidate]
    search_stats: Dict[str, int] = field(default_factory=dict)


# =============================================================================
# FORMULA GENERATOR
# =============================================================================

class FormulaGenerator:
    """
    Generates candidate formulas for Z² derivations.

    Searches multiple formula spaces to find expressions that match
    a target value. Prioritizes simple, physically meaningful formulas.
    """

    def __init__(self, max_error: float = 1.0, verbose: bool = False):
        """
        Initialize the formula generator.

        Args:
            max_error: Maximum percent error to accept (default 1%)
            verbose: Print progress information
        """
        self.max_error = max_error
        self.verbose = verbose

        # Track search statistics
        self.stats = {
            "simple_fractions_tried": 0,
            "z_polynomials_tried": 0,
            "integer_z2_tried": 0,
            "geometric_tried": 0,
            "pi_based_tried": 0,
            "compound_tried": 0,
            "total_matches": 0
        }

        # Known first-principles formulas (from verified derivations)
        self.known_formulas = {
            "sin2_theta_w": ("3/13", 3/13, "Weak mixing angle from gauge coupling"),
            "omega_lambda": ("13/19", 13/19, "Dark energy fraction from holographic"),
            "alpha_inverse": ("4*Z² + 3", 4 * Z_SQUARED + 3, "Fine structure from geometry"),
            "gamma_heat": ("5/3", 5/3, "Heat capacity from DOF"),
            "tetrahedral": ("arccos(-1/3)", math.degrees(math.acos(-1/3)), "Tetrahedral from geometry"),
            "tensor_to_scalar_r": ("1/(2Z²)", 1/(2*Z_SQUARED), "CMB tensor-to-scalar ratio"),
            "omega_matter": ("6/19", 6/19, "Matter fraction from holographic"),
            "pmns_theta12": ("arcsin(1/√3)", math.degrees(math.asin(1/math.sqrt(3))), "PMNS solar angle"),
            "pmns_theta23": ("45°", 45.0, "PMNS atmospheric angle (maximal)"),
            "pmns_theta13": ("arcsin(1/√(2Z²))", math.degrees(math.asin(1/math.sqrt(2*Z_SQUARED))), "PMNS reactor angle"),
        }

    def search(self, target: float, exhaustive: bool = False) -> FormulaSearchResult:
        """
        Search for formulas matching the target value.

        Args:
            target: Target value to match
            exhaustive: If True, search all formula spaces

        Returns:
            FormulaSearchResult with candidates
        """
        candidates = []

        # Reset stats
        for key in self.stats:
            self.stats[key] = 0

        # Strategy 1: Check known first-principles formulas
        known = self._check_known_formulas(target)
        candidates.extend(known)

        # Strategy 2: Simple fractions (highest priority for elegance)
        fractions = self._search_simple_fractions(target)
        candidates.extend(fractions)

        # Strategy 3: Integer + Z² combinations
        int_z2 = self._search_integer_z2(target)
        candidates.extend(int_z2)

        # Strategy 4: Z polynomials (aZ + b)
        z_poly = self._search_z_polynomials(target)
        candidates.extend(z_poly)

        # Strategy 5: Geometric functions
        geometric = self._search_geometric(target)
        candidates.extend(geometric)

        # Strategy 6: π-based expressions
        pi_based = self._search_pi_based(target)
        candidates.extend(pi_based)

        # Strategy 7: Compound expressions (if exhaustive)
        if exhaustive:
            compound = self._search_compound(target)
            candidates.extend(compound)

        # Sort by error (best first)
        candidates.sort(key=lambda c: abs(c.percent_error))

        # Find best match
        best = candidates[0] if candidates else None

        self.stats["total_matches"] = len(candidates)

        return FormulaSearchResult(
            target_value=target,
            candidates=candidates,
            best_match=best,
            search_stats=self.stats.copy()
        )

    def _check_known_formulas(self, target: float) -> List[FormulaCandidate]:
        """Check against known first-principles formulas."""
        candidates = []

        for name, (formula, value, hint) in self.known_formulas.items():
            error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100
            if error <= self.max_error:
                candidates.append(FormulaCandidate(
                    formula_str=formula,
                    formula_type=FormulaType.KNOWN_FIRST_PRINCIPLES,
                    computed_value=value,
                    target_value=target,
                    percent_error=error,
                    parameters={"known_name": name},
                    physical_hint=hint
                ))

        return candidates

    def _search_simple_fractions(self, target: float, max_denom: int = 50) -> List[FormulaCandidate]:
        """
        Search simple fractions a/b.

        This finds elegant formulas like 3/13 for sin²θ_W.
        """
        candidates = []

        for b in range(1, max_denom + 1):
            for a in range(1, max_denom + 1):
                self.stats["simple_fractions_tried"] += 1

                value = a / b
                error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                if error <= self.max_error:
                    # Check if fraction is in lowest terms
                    gcd = math.gcd(a, b)
                    if gcd == 1:  # Already reduced
                        candidates.append(FormulaCandidate(
                            formula_str=f"{a}/{b}",
                            formula_type=FormulaType.SIMPLE_FRACTION,
                            computed_value=value,
                            target_value=target,
                            percent_error=error,
                            parameters={"a": a, "b": b},
                            latex=f"\\frac{{{a}}}{{{b}}}"
                        ))

        return candidates

    def _search_integer_z2(self, target: float) -> List[FormulaCandidate]:
        """
        Search integer + Z² combinations: aZ² + b

        This finds formulas like 4Z² + 3 ≈ 137.04 for α⁻¹.
        """
        candidates = []

        for a in range(-10, 11):
            for b in range(-50, 51):
                self.stats["integer_z2_tried"] += 1

                if a == 0:
                    continue

                value = a * Z_SQUARED + b
                if value == 0:
                    continue

                error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                if error <= self.max_error:
                    # Format nicely
                    if b == 0:
                        formula = f"{a}Z²" if a != 1 else "Z²"
                    elif b > 0:
                        formula = f"{a}Z² + {b}" if a != 1 else f"Z² + {b}"
                    else:
                        formula = f"{a}Z² - {abs(b)}" if a != 1 else f"Z² - {abs(b)}"

                    candidates.append(FormulaCandidate(
                        formula_str=formula,
                        formula_type=FormulaType.INTEGER_Z2,
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        parameters={"a": a, "b": b},
                        latex=formula.replace("Z²", "Z^2")
                    ))

        return candidates

    def _search_z_polynomials(self, target: float) -> List[FormulaCandidate]:
        """
        Search Z polynomials: aZ + b, a/Z, etc.
        """
        candidates = []

        # aZ + b
        for a in range(-10, 11):
            for b in range(-30, 31):
                self.stats["z_polynomials_tried"] += 1

                if a == 0:
                    continue

                value = a * Z + b

                error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                if error <= self.max_error:
                    if b == 0:
                        formula = f"{a}Z" if a != 1 else "Z"
                    elif b > 0:
                        formula = f"{a}Z + {b}" if a != 1 else f"Z + {b}"
                    else:
                        formula = f"{a}Z - {abs(b)}" if a != 1 else f"Z - {abs(b)}"

                    candidates.append(FormulaCandidate(
                        formula_str=formula,
                        formula_type=FormulaType.Z_POLYNOMIAL,
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        parameters={"a": a, "b": b}
                    ))

        # a/Z and a/Z²
        for a in range(1, 100):
            for z_power in [1, 2]:
                self.stats["z_polynomials_tried"] += 1

                z_val = Z if z_power == 1 else Z_SQUARED
                value = a / z_val

                error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                if error <= self.max_error:
                    z_str = "Z" if z_power == 1 else "Z²"
                    formula = f"{a}/{z_str}"

                    candidates.append(FormulaCandidate(
                        formula_str=formula,
                        formula_type=FormulaType.Z_FRACTION,
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        parameters={"a": a, "z_power": z_power}
                    ))

        # 1/(aZ) and 1/(aZ²) - for small values like r = 1/(2Z²)
        for a in range(1, 20):
            for z_power in [1, 2]:
                self.stats["z_polynomials_tried"] += 1

                z_val = Z if z_power == 1 else Z_SQUARED
                value = 1 / (a * z_val)

                error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                if error <= self.max_error:
                    z_str = "Z" if z_power == 1 else "Z²"
                    if a == 1:
                        formula = f"1/{z_str}"
                    else:
                        formula = f"1/({a}{z_str})"

                    candidates.append(FormulaCandidate(
                        formula_str=formula,
                        formula_type=FormulaType.Z_FRACTION,
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        parameters={"a": a, "z_power": z_power, "form": "inverse"},
                        physical_hint=f"Inverse Z² scaling with factor {a}"
                    ))

        return candidates

    def _search_geometric(self, target: float) -> List[FormulaCandidate]:
        """
        Search geometric functions: arccos(a/b), arctan(a/b).

        This finds formulas like arccos(-1/3) ≈ 109.47° for tetrahedral angle.
        """
        candidates = []

        # Determine if target is in degrees or radians
        # If target > 2π, probably degrees
        is_degrees = abs(target) > 2 * math.pi

        for a in range(-10, 11):
            for b in range(1, 20):
                self.stats["geometric_tried"] += 1

                ratio = a / b

                # arccos (only valid for |ratio| <= 1)
                if abs(ratio) <= 1:
                    try:
                        rad_value = math.acos(ratio)
                        deg_value = math.degrees(rad_value)

                        value = deg_value if is_degrees else rad_value
                        error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                        if error <= self.max_error:
                            if a >= 0:
                                formula = f"arccos({a}/{b})"
                            else:
                                formula = f"arccos(-{abs(a)}/{b})"

                            candidates.append(FormulaCandidate(
                                formula_str=formula,
                                formula_type=FormulaType.GEOMETRIC,
                                computed_value=value,
                                target_value=target,
                                percent_error=error,
                                parameters={"a": a, "b": b, "func": "arccos"},
                                latex=f"\\arccos\\left(\\frac{{{a}}}{{{b}}}\\right)"
                            ))
                    except ValueError:
                        pass

                # arctan (always valid)
                try:
                    rad_value = math.atan(ratio)
                    deg_value = math.degrees(rad_value)

                    value = deg_value if is_degrees else rad_value
                    error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                    if error <= self.max_error:
                        formula = f"arctan({a}/{b})"

                        candidates.append(FormulaCandidate(
                            formula_str=formula,
                            formula_type=FormulaType.GEOMETRIC,
                            computed_value=value,
                            target_value=target,
                            percent_error=error,
                            parameters={"a": a, "b": b, "func": "arctan"}
                        ))
                except ValueError:
                    pass

        return candidates

    def _search_pi_based(self, target: float) -> List[FormulaCandidate]:
        """
        Search π-based expressions: π/a, aπ, etc.
        """
        candidates = []

        for a in range(1, 50):
            self.stats["pi_based_tried"] += 1

            # π/a
            value = math.pi / a
            error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100
            if error <= self.max_error:
                candidates.append(FormulaCandidate(
                    formula_str=f"π/{a}",
                    formula_type=FormulaType.PI_BASED,
                    computed_value=value,
                    target_value=target,
                    percent_error=error,
                    parameters={"a": a, "form": "pi_over_a"},
                    latex=f"\\frac{{\\pi}}{{{a}}}"
                ))

            # a/π
            value = a / math.pi
            error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100
            if error <= self.max_error:
                candidates.append(FormulaCandidate(
                    formula_str=f"{a}/π",
                    formula_type=FormulaType.PI_BASED,
                    computed_value=value,
                    target_value=target,
                    percent_error=error,
                    parameters={"a": a, "form": "a_over_pi"},
                    latex=f"\\frac{{{a}}}{{\\pi}}"
                ))

            # aπ
            value = a * math.pi
            error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100
            if error <= self.max_error:
                candidates.append(FormulaCandidate(
                    formula_str=f"{a}π",
                    formula_type=FormulaType.PI_BASED,
                    computed_value=value,
                    target_value=target,
                    percent_error=error,
                    parameters={"a": a, "form": "a_times_pi"},
                    latex=f"{a}\\pi"
                ))

        return candidates

    def _search_compound(self, target: float) -> List[FormulaCandidate]:
        """
        Search compound expressions: (aZ + b)/(cZ + d), a/(bZ² + c), etc.

        More expensive but finds complex patterns.
        """
        candidates = []

        # (aZ + b)/(cZ + d)
        for a in range(-5, 6):
            for b in range(-10, 11):
                for c in range(-5, 6):
                    for d in range(-10, 11):
                        self.stats["compound_tried"] += 1

                        if c == 0 and d == 0:
                            continue

                        denom = c * Z + d
                        if abs(denom) < 0.001:
                            continue

                        value = (a * Z + b) / denom
                        error = abs(value - target) / abs(target) * 100 if target != 0 else abs(value) * 100

                        if error <= self.max_error:
                            formula = f"({a}Z + {b})/({c}Z + {d})"
                            candidates.append(FormulaCandidate(
                                formula_str=formula,
                                formula_type=FormulaType.COMPOUND,
                                computed_value=value,
                                target_value=target,
                                percent_error=error,
                                parameters={"a": a, "b": b, "c": c, "d": d}
                            ))

        return candidates

    def find_best(self, target: float, prefer_simple: bool = True) -> Optional[FormulaCandidate]:
        """
        Find the best formula for a target value.

        Args:
            target: Target value to match
            prefer_simple: If True, prefer simpler formulas over complex ones

        Returns:
            Best FormulaCandidate or None
        """
        result = self.search(target, exhaustive=not prefer_simple)

        if not result.candidates:
            return None

        if prefer_simple:
            # Rank by simplicity: known > fraction > integer_z2 > geometric > z_poly > compound
            type_priority = {
                FormulaType.KNOWN_FIRST_PRINCIPLES: 0,
                FormulaType.SIMPLE_FRACTION: 1,
                FormulaType.INTEGER_Z2: 2,
                FormulaType.GEOMETRIC: 3,
                FormulaType.PI_BASED: 4,
                FormulaType.Z_POLYNOMIAL: 5,
                FormulaType.Z_FRACTION: 6,
                FormulaType.COMPOUND: 7
            }

            # Sort by (type_priority, error)
            result.candidates.sort(
                key=lambda c: (type_priority.get(c.formula_type, 10), abs(c.percent_error))
            )

        return result.candidates[0]


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def find_formula(target: float, max_error: float = 1.0) -> Optional[FormulaCandidate]:
    """
    Find a formula matching the target value.

    Args:
        target: Value to match
        max_error: Maximum percent error

    Returns:
        Best FormulaCandidate or None
    """
    generator = FormulaGenerator(max_error=max_error)
    return generator.find_best(target)


def test_known_constants():
    """Test the generator on known Z² constants."""
    generator = FormulaGenerator(max_error=1.0, verbose=True)

    test_cases = [
        ("sin²θ_W", 0.23122, "3/13"),
        ("α⁻¹", 137.036, "4Z² + 3"),
        ("Ω_Λ", 0.685, "13/19"),
        ("Tetrahedral angle", 109.4712, "arccos(-1/3)"),
        ("γ (heat capacity)", 5/3, "5/3"),
        ("Golden ratio", 1.618, "φ or (1+√5)/2"),
    ]

    print("=" * 70)
    print("FORMULA GENERATOR TEST")
    print("=" * 70)

    for name, target, expected in test_cases:
        result = generator.search(target)
        best = result.best_match

        print(f"\n{name} = {target}")
        print(f"  Expected: {expected}")
        if best:
            print(f"  Found: {best.formula_str} = {best.computed_value:.6f}")
            print(f"  Error: {best.percent_error:.4f}%")
            print(f"  Type: {best.formula_type.value}")
        else:
            print("  Not found!")

        print(f"  Candidates: {len(result.candidates)}")
        print(f"  Stats: {result.search_stats}")


if __name__ == "__main__":
    test_known_constants()
