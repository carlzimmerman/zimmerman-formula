#!/usr/bin/env python3
"""
GEOMETRIC INTERPRETER - Pattern Meaning Discovery
==================================================

Provides geometric and physical interpretations for patterns
discovered by the PatternSearchEngine. This is critical for
distinguishing real physics from coincidental numerology.

Key Interpretations:
- Z² = 32π/3: Cube vertices × sphere volume (8 × 4π/3)
- Fractions a/b: Ratio of discrete quantities
- π multiples: Circular/spherical geometry
- √n: Diagonal/projection geometry
- φ: Self-similar recursion

Author: Carl Zimmerman
Date: May 6, 2026
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum

from .phenomenological import Z_SQUARED, Z, PHI


class GeometryType(Enum):
    """Types of geometric interpretations."""
    COMPACTIFICATION = "compactification"   # Extra dimension geometry
    SPHERICAL = "spherical"                 # Sphere-related
    CUBIC = "cubic"                         # Cube-related
    PROJECTION = "projection"               # Dimensional projection
    RATIO = "ratio"                         # Discrete ratio
    SYMMETRY = "symmetry"                   # Symmetry group
    SELF_SIMILAR = "self_similar"           # Fractal/recursive
    ANGULAR = "angular"                     # Angle-related
    COMBINATORIAL = "combinatorial"         # Counting argument
    TOPOLOGICAL = "topological"             # Topology-related
    UNKNOWN = "unknown"


@dataclass
class GeometricInterpretation:
    """A geometric interpretation of a pattern."""
    pattern: str
    geometry_type: GeometryType
    description: str
    confidence: float  # 0-1, how confident we are this is real

    # Physical connection
    physical_domain: str = ""
    physical_mechanism: str = ""

    # Supporting evidence
    related_patterns: List[str] = field(default_factory=list)
    dimensional_analysis: str = ""

    # Risk assessment
    numerology_risk: str = "unknown"  # low/medium/high


class GeometricInterpreter:
    """
    Interprets patterns geometrically.

    This is essential for BriareusFlow's mission: finding patterns
    that might have physical meaning, not just numerical coincidences.
    """

    # Known Z² interpretations
    Z_SQUARED_INTERPRETATIONS = {
        "Z²": {
            "geometry": GeometryType.COMPACTIFICATION,
            "description": "Z² = 32π/3 = 8 × (4π/3): Cube vertices × sphere volume",
            "mechanism": "Extra-dimensional compactification on 7-sphere inside 8-cube",
            "confidence": 0.98
        },
        "Z": {
            "geometry": GeometryType.COMPACTIFICATION,
            "description": "Z = √(32π/3): Square root of compactification constant",
            "mechanism": "Linear scale of compactification geometry",
            "confidence": 0.95
        },
        "4Z² + 3": {
            "geometry": GeometryType.COMPACTIFICATION,
            "description": "α⁻¹ = 4Z² + 3: Fine structure from geometric quantization",
            "mechanism": "Charge quantization from holonomy on compactified manifold",
            "confidence": 0.90
        },
    }

    # Known fraction interpretations
    FRACTION_INTERPRETATIONS = {
        "3/13": {
            "geometry": GeometryType.RATIO,
            "description": "sin²θ_W = 3/13: Electroweak mixing from gauge coupling ratio",
            "mechanism": "SU(2)×U(1) gauge symmetry breaking",
            "domains": ["particle_physics"],
            "confidence": 0.92
        },
        "10/13": {
            "geometry": GeometryType.RATIO,
            "description": "cos²θ_W = 10/13: Complementary to sin²θ_W",
            "mechanism": "Electroweak gauge coupling structure",
            "domains": ["particle_physics"],
            "confidence": 0.92
        },
        "13/19": {
            "geometry": GeometryType.RATIO,
            "description": "Ω_Λ = 13/19: Dark energy fraction from holographic bound",
            "mechanism": "Holographic principle constraint on vacuum energy",
            "domains": ["cosmology"],
            "confidence": 0.75
        },
        "5/3": {
            "geometry": GeometryType.RATIO,
            "description": "γ = 5/3 = (D+2)/D for D=3: Heat capacity ratio",
            "mechanism": "Degrees of freedom in 3D space",
            "domains": ["thermodynamics"],
            "confidence": 0.99
        },
        "4/3": {
            "geometry": GeometryType.SPHERICAL,
            "description": "4/3: Coefficient in sphere volume (4πr³/3)",
            "mechanism": "Spherical geometry integration",
            "domains": ["geometry"],
            "confidence": 0.99
        },
        "1/3": {
            "geometry": GeometryType.PROJECTION,
            "description": "1/3: Average projection factor in 3D",
            "mechanism": "Isotropic angular average",
            "domains": ["geometry", "particle_physics"],
            "confidence": 0.90
        },
    }

    # Pi-related interpretations
    PI_INTERPRETATIONS = {
        "π": {
            "geometry": GeometryType.SPHERICAL,
            "description": "π: Fundamental circular/spherical constant",
            "mechanism": "Euclidean circle ratio",
            "confidence": 1.0
        },
        "2π": {
            "geometry": GeometryType.SPHERICAL,
            "description": "2π: Full rotation angle, sphere circumference",
            "mechanism": "Periodic boundary conditions",
            "confidence": 1.0
        },
        "4π": {
            "geometry": GeometryType.SPHERICAL,
            "description": "4π: Solid angle of full sphere",
            "mechanism": "Surface area of unit sphere",
            "confidence": 1.0
        },
        "4π/3": {
            "geometry": GeometryType.SPHERICAL,
            "description": "4π/3: Volume of unit sphere",
            "mechanism": "3D spherical integration",
            "confidence": 1.0
        },
        "8π/3": {
            "geometry": GeometryType.COMPACTIFICATION,
            "description": "8π/3 = Z²/4: Friedmann equation coefficient",
            "mechanism": "Einstein gravity in FLRW spacetime",
            "confidence": 0.95
        },
    }

    # Arccos/arctan interpretations
    TRIGONOMETRIC_INTERPRETATIONS = {
        "arccos(-1/3)": {
            "geometry": GeometryType.ANGULAR,
            "description": "Tetrahedral bond angle ≈ 109.47°",
            "mechanism": "Four equivalent sp³ hybrid orbitals",
            "domains": ["chemistry", "geometry"],
            "confidence": 0.99
        },
        "arccos(1/3)": {
            "geometry": GeometryType.ANGULAR,
            "description": "Octahedral edge angle ≈ 70.53°",
            "mechanism": "Six equivalent vertices on sphere",
            "domains": ["geometry"],
            "confidence": 0.99
        },
        "arctan(1)": {
            "geometry": GeometryType.ANGULAR,
            "description": "45° angle: Equal x and y components",
            "mechanism": "Diagonal of square",
            "confidence": 1.0
        },
    }

    # Sqrt interpretations
    SQRT_INTERPRETATIONS = {
        "√2": {
            "geometry": GeometryType.PROJECTION,
            "description": "√2: Diagonal of unit square",
            "mechanism": "Pythagorean theorem in 2D",
            "confidence": 1.0
        },
        "√3": {
            "geometry": GeometryType.PROJECTION,
            "description": "√3: Diagonal of unit cube face, equilateral height",
            "mechanism": "3D diagonal projection",
            "confidence": 1.0
        },
        "√5": {
            "geometry": GeometryType.SELF_SIMILAR,
            "description": "√5: Golden ratio denominator (φ = (1+√5)/2)",
            "mechanism": "Pentagon/icosahedron diagonal",
            "confidence": 0.95
        },
    }

    # Phi interpretations
    PHI_INTERPRETATIONS = {
        "φ": {
            "geometry": GeometryType.SELF_SIMILAR,
            "description": "φ = (1+√5)/2 ≈ 1.618: Golden ratio",
            "mechanism": "Self-similar recursive structure",
            "confidence": 0.85  # Lower because often coincidental
        },
        "φ²": {
            "geometry": GeometryType.SELF_SIMILAR,
            "description": "φ² = φ + 1: Golden ratio squared",
            "mechanism": "Fibonacci recursion",
            "confidence": 0.80
        },
        "1/φ": {
            "geometry": GeometryType.SELF_SIMILAR,
            "description": "1/φ = φ - 1: Golden ratio reciprocal",
            "mechanism": "Self-similarity inverse",
            "confidence": 0.80
        },
    }

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self._build_lookup_tables()

    def _log(self, msg: str):
        if self.verbose:
            print(f"[GeometricInterpreter] {msg}")

    def _build_lookup_tables(self):
        """Build numerical lookup tables for quick matching."""
        self.numerical_lookup: Dict[float, GeometricInterpretation] = {}

        # Add Z² values
        self.numerical_lookup[Z_SQUARED] = GeometricInterpretation(
            pattern="Z²",
            geometry_type=GeometryType.COMPACTIFICATION,
            description="Z² = 32π/3 = 8 × (4π/3): Cube vertices × sphere volume",
            confidence=0.98,
            physical_domain="fundamental",
            physical_mechanism="Extra-dimensional compactification",
            numerology_risk="low"
        )

        self.numerical_lookup[Z] = GeometricInterpretation(
            pattern="Z",
            geometry_type=GeometryType.COMPACTIFICATION,
            description="Z = √(32π/3): Linear compactification scale",
            confidence=0.95,
            physical_domain="fundamental",
            physical_mechanism="Compactification radius",
            numerology_risk="low"
        )

        # Add fractions
        for frac, info in self.FRACTION_INTERPRETATIONS.items():
            parts = frac.split("/")
            if len(parts) == 2:
                value = int(parts[0]) / int(parts[1])
                self.numerical_lookup[value] = GeometricInterpretation(
                    pattern=frac,
                    geometry_type=info["geometry"],
                    description=info["description"],
                    confidence=info["confidence"],
                    physical_domain=info.get("domains", [""])[0],
                    physical_mechanism=info["mechanism"],
                    numerology_risk="low" if info["confidence"] > 0.9 else "medium"
                )

        # Add π values
        for expr, info in self.PI_INTERPRETATIONS.items():
            # Properly handle π expressions
            pi_expr = expr.replace("π", "*math.pi").lstrip("*")
            if pi_expr.startswith("math.pi"):
                pi_expr = pi_expr  # Just π
            value = eval(pi_expr)
            self.numerical_lookup[value] = GeometricInterpretation(
                pattern=expr,
                geometry_type=info["geometry"],
                description=info["description"],
                confidence=info["confidence"],
                physical_domain="geometry",
                physical_mechanism=info["mechanism"],
                numerology_risk="low"
            )

    def interpret(self, formula: str, value: float,
                  domain: str = "general") -> Optional[GeometricInterpretation]:
        """
        Interpret a formula geometrically.

        Args:
            formula: The formula string (e.g., "4Z² + 3")
            value: The numerical value
            domain: Physical domain for context

        Returns:
            GeometricInterpretation if found, None otherwise
        """
        # Check direct lookup
        for known_val, interp in self.numerical_lookup.items():
            if abs(value - known_val) / max(abs(known_val), 1e-10) < 0.001:
                return interp

        # Check formula patterns
        formula_clean = formula.replace(" ", "")

        # Z² patterns
        if "Z²" in formula or "Z^2" in formula:
            return self._interpret_z_squared(formula, value, domain)

        # Fraction patterns
        if "/" in formula and "Z" not in formula and "π" not in formula:
            return self._interpret_fraction(formula, value, domain)

        # π patterns
        if "π" in formula:
            return self._interpret_pi(formula, value, domain)

        # √ patterns
        if "√" in formula:
            return self._interpret_sqrt(formula, value, domain)

        # φ patterns
        if "φ" in formula:
            return self._interpret_phi(formula, value, domain)

        # arccos/arctan patterns
        if "arccos" in formula or "arctan" in formula:
            return self._interpret_trigonometric(formula, value, domain)

        return None

    def _interpret_z_squared(self, formula: str, value: float,
                              domain: str) -> GeometricInterpretation:
        """Interpret Z²-containing formulas."""
        # Parse coefficient
        if formula in self.Z_SQUARED_INTERPRETATIONS:
            info = self.Z_SQUARED_INTERPRETATIONS[formula]
            return GeometricInterpretation(
                pattern=formula,
                geometry_type=info["geometry"],
                description=info["description"],
                confidence=info["confidence"],
                physical_domain=domain,
                physical_mechanism=info["mechanism"],
                numerology_risk="low"
            )

        # Generic Z² pattern
        return GeometricInterpretation(
            pattern=formula,
            geometry_type=GeometryType.COMPACTIFICATION,
            description=f"{formula}: Expression involving Z² = 32π/3",
            confidence=0.70,
            physical_domain=domain,
            physical_mechanism="Geometric compactification structure",
            numerology_risk="medium"
        )

    def _interpret_fraction(self, formula: str, value: float,
                            domain: str) -> GeometricInterpretation:
        """Interpret simple fractions."""
        if formula in self.FRACTION_INTERPRETATIONS:
            info = self.FRACTION_INTERPRETATIONS[formula]
            return GeometricInterpretation(
                pattern=formula,
                geometry_type=info["geometry"],
                description=info["description"],
                confidence=info["confidence"],
                physical_domain=domain,
                physical_mechanism=info["mechanism"],
                numerology_risk="low"
            )

        # Parse fraction
        try:
            parts = formula.replace("(", "").replace(")", "").split("/")
            if len(parts) == 2:
                num = int(parts[0])
                denom = int(parts[1])

                # Simple ratios have geometric meaning
                if num < 20 and denom < 20:
                    return GeometricInterpretation(
                        pattern=formula,
                        geometry_type=GeometryType.RATIO,
                        description=f"{formula} = {value:.6f}: Ratio of {num} to {denom}",
                        confidence=0.5 if num < 10 and denom < 10 else 0.3,
                        physical_domain=domain,
                        physical_mechanism="Discrete quantity ratio",
                        numerology_risk="medium" if num < 15 else "high"
                    )
        except (ValueError, IndexError):
            pass

        return GeometricInterpretation(
            pattern=formula,
            geometry_type=GeometryType.RATIO,
            description=f"{formula} = {value:.6f}",
            confidence=0.3,
            physical_domain=domain,
            numerology_risk="high"
        )

    def _interpret_pi(self, formula: str, value: float,
                      domain: str) -> GeometricInterpretation:
        """Interpret π-containing formulas."""
        formula_clean = formula.replace(" ", "")

        if formula_clean in self.PI_INTERPRETATIONS:
            info = self.PI_INTERPRETATIONS[formula_clean]
            return GeometricInterpretation(
                pattern=formula,
                geometry_type=info["geometry"],
                description=info["description"],
                confidence=info["confidence"],
                physical_domain=domain,
                physical_mechanism=info["mechanism"],
                numerology_risk="low"
            )

        # Generic π pattern
        return GeometricInterpretation(
            pattern=formula,
            geometry_type=GeometryType.SPHERICAL,
            description=f"{formula}: Expression involving π",
            confidence=0.6,
            physical_domain=domain,
            physical_mechanism="Circular/spherical geometry",
            numerology_risk="medium"
        )

    def _interpret_sqrt(self, formula: str, value: float,
                        domain: str) -> GeometricInterpretation:
        """Interpret √n formulas."""
        # Extract the number under the root
        for n in [2, 3, 5, 6, 7, 10]:
            if f"√{n}" in formula:
                info = self.SQRT_INTERPRETATIONS.get(f"√{n}", {})
                return GeometricInterpretation(
                    pattern=formula,
                    geometry_type=info.get("geometry", GeometryType.PROJECTION),
                    description=info.get("description", f"Expression involving √{n}"),
                    confidence=info.get("confidence", 0.7),
                    physical_domain=domain,
                    physical_mechanism=info.get("mechanism", "Pythagorean/diagonal geometry"),
                    numerology_risk="low" if n in [2, 3] else "medium"
                )

        return GeometricInterpretation(
            pattern=formula,
            geometry_type=GeometryType.PROJECTION,
            description=f"{formula}: Square root expression",
            confidence=0.5,
            physical_domain=domain,
            numerology_risk="medium"
        )

    def _interpret_phi(self, formula: str, value: float,
                       domain: str) -> GeometricInterpretation:
        """Interpret φ (golden ratio) formulas."""
        # φ is often coincidental - higher numerology risk
        return GeometricInterpretation(
            pattern=formula,
            geometry_type=GeometryType.SELF_SIMILAR,
            description=f"{formula}: Golden ratio expression",
            confidence=0.5,  # Lower confidence - often coincidental
            physical_domain=domain,
            physical_mechanism="Self-similar recursive structure (needs verification)",
            numerology_risk="medium"  # φ often appears coincidentally
        )

    def _interpret_trigonometric(self, formula: str, value: float,
                                  domain: str) -> GeometricInterpretation:
        """Interpret arccos/arctan formulas."""
        formula_clean = formula.replace(" ", "")

        # Check known angles
        for pattern, info in self.TRIGONOMETRIC_INTERPRETATIONS.items():
            if pattern in formula_clean:
                return GeometricInterpretation(
                    pattern=formula,
                    geometry_type=info["geometry"],
                    description=info["description"],
                    confidence=info["confidence"],
                    physical_domain=domain,
                    physical_mechanism=info["mechanism"],
                    numerology_risk="low"
                )

        # Generic trig interpretation
        return GeometricInterpretation(
            pattern=formula,
            geometry_type=GeometryType.ANGULAR,
            description=f"{formula} = {value:.4f}°: Geometric angle",
            confidence=0.6,
            physical_domain=domain,
            physical_mechanism="Angular geometry",
            numerology_risk="medium"
        )

    def batch_interpret(self, patterns: List[Tuple[str, float]],
                        domain: str = "general") -> List[Optional[GeometricInterpretation]]:
        """Interpret a batch of patterns."""
        return [self.interpret(formula, value, domain) for formula, value in patterns]

    def get_z_squared_chain(self, value: float) -> List[str]:
        """
        Get the Z² derivation chain for a value.

        Shows how a value relates to Z² geometrically.
        """
        chains = []

        # Direct Z² relationship
        if abs(value - Z_SQUARED) / Z_SQUARED < 0.001:
            chains.append("value = Z² = 32π/3 = 8 × (4π/3) = cube_vertices × sphere_volume")

        # Integer multiple
        for n in range(1, 11):
            if abs(value - n * Z_SQUARED) / (n * Z_SQUARED) < 0.001:
                chains.append(f"value = {n}Z² = {n} × 32π/3")

        # Integer addition
        for n in range(-20, 21):
            if abs(value - (Z_SQUARED + n)) / max(abs(Z_SQUARED + n), 1) < 0.001:
                chains.append(f"value = Z² + {n} = 32π/3 + {n}")

        # aZ² + b pattern
        for a in range(1, 11):
            for b in range(-20, 21):
                target = a * Z_SQUARED + b
                if target > 0 and abs(value - target) / target < 0.001:
                    chains.append(f"value = {a}Z² + {b} = {a}×32π/3 + {b}")

        return chains

    def assess_numerology_risk(self, formula: str, value: float,
                                alternatives_count: int = 0) -> str:
        """
        Assess numerology risk for a pattern.

        Returns: "low", "medium", "high", "very_high"
        """
        risk_score = 0

        # Z² patterns are lower risk
        if "Z²" in formula or "Z^2" in formula:
            risk_score -= 2

        # Simple fractions with small numbers are lower risk
        if "/" in formula:
            try:
                parts = formula.replace("(", "").replace(")", "").split("/")
                if len(parts) == 2:
                    num = abs(int(parts[0]))
                    denom = abs(int(parts[1]))
                    if num < 10 and denom < 10:
                        risk_score -= 1
                    elif num > 30 or denom > 30:
                        risk_score += 2
            except ValueError:
                pass

        # φ is often coincidental
        if "φ" in formula:
            risk_score += 1

        # Many alternatives = higher risk
        if alternatives_count > 5:
            risk_score += 2
        elif alternatives_count > 2:
            risk_score += 1

        # Complex formulas with multiple terms
        if "+" in formula or "-" in formula:
            if formula.count("+") + formula.count("-") > 2:
                risk_score += 1

        # Map score to risk level
        if risk_score <= -2:
            return "low"
        elif risk_score <= 0:
            return "medium"
        elif risk_score <= 2:
            return "high"
        else:
            return "very_high"


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GEOMETRIC INTERPRETER TEST")
    print("=" * 70)
    print()

    interpreter = GeometricInterpreter(verbose=True)

    # Test patterns
    test_patterns = [
        ("Z²", Z_SQUARED, "fundamental"),
        ("4Z² + 3", 4 * Z_SQUARED + 3, "particle_physics"),
        ("3/13", 3/13, "particle_physics"),
        ("5/3", 5/3, "thermodynamics"),
        ("4π/3", 4 * math.pi / 3, "geometry"),
        ("arccos(-1/3)", math.acos(-1/3) * 180 / math.pi, "chemistry"),
        ("φ/7", PHI / 7, "unknown"),
        ("√2", math.sqrt(2), "geometry"),
    ]

    for formula, value, domain in test_patterns:
        print(f"\n--- {formula} = {value:.6f} ---")
        interp = interpreter.interpret(formula, value, domain)
        if interp:
            print(f"  Type: {interp.geometry_type.value}")
            print(f"  Description: {interp.description}")
            print(f"  Confidence: {interp.confidence:.2f}")
            print(f"  Mechanism: {interp.physical_mechanism}")
            print(f"  Risk: {interp.numerology_risk}")
        else:
            print("  No interpretation found")

    # Test Z² chain
    print("\n--- Z² Chain for α⁻¹ ≈ 137.036 ---")
    chains = interpreter.get_z_squared_chain(137.036)
    for chain in chains:
        print(f"  {chain}")

    print()
    print("=" * 70)
    print("GEOMETRIC INTERPRETER TEST COMPLETE")
    print("=" * 70)
