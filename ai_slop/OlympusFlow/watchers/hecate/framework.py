"""
FRAMEWORK VALIDATOR - Z² Alignment Checker
============================================

Validates that derivations and claims align with the Z² = 32π/3
geometric framework and don't contradict AletheiaLake ground truths.
"""

import math
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from ..contracts import FrameworkCheck


# Z² Constants
Z2 = 32 * math.pi / 3  # ≈ 33.510321638
Z = math.sqrt(Z2)       # ≈ 5.78881
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio


class FrameworkValidator:
    """
    Validates claims against Z² framework principles.

    Checks:
    1. Does the derivation start from Z² = 32π/3?
    2. Is there a geometric basis (not arbitrary)?
    3. Is there a physical mechanism (not numerology)?
    4. Does it conflict with AletheiaLake ground truths?
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

        # Load AletheiaLake ground truths
        self.ground_truths = self._load_ground_truths()

        # Known valid Z² expressions
        self.valid_expressions = {
            "Z²": Z2,
            "Z": Z,
            "4Z² + 3": 4 * Z2 + 3,
            "4Z² + 2": 4 * Z2 + 2,
            "3/13": 3/13,
            "13/19": 13/19,
            "6/19": 6/19,
            "Z²/2": Z2 / 2,
            "Z/6": Z / 6,
            "1/Z⁴": 1 / (Z2 ** 2),
            "3Z + 16": 3 * Z + 16,
            "4Z + 19": 4 * Z + 19,
            "2Z - 3": 2 * Z - 3,
        }

        # Suspicious patterns (numerology red flags)
        self.numerology_patterns = [
            r'\d+\.\d{4,}',  # Too many decimal places in constant
            r'fitting parameter',
            r'best fit',
            r'empirical',
            r'observed to be',
            r'happens to equal',
            r'numerical coincidence',
        ]

        # Hidden assumption indicators
        self.hidden_assumptions = [
            r'dark matter',
            r'dark halo',
            r'NFW profile',
            r'ΛCDM',
            r'lambda-CDM',
            r'cosmological constant.*problem',
            r'fine.?tuning',
            r'anthropic',
            r'multiverse',
        ]

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[FrameworkValidator {ts}] {msg}")

    def _load_ground_truths(self) -> Dict:
        """Load AletheiaLake ground truths for validation."""
        try:
            from OlympusFlow.lakes.aletheia import AletheiaLake
            lake = AletheiaLake()
            truths = {}
            for t in lake.get_all_truths():
                truths[t.name] = {
                    "formula": t.formula,
                    "z2_prediction": t.z2_prediction,
                    "experimental_value": t.experimental_value,
                    "experimental_uncertainty": t.experimental_uncertainty
                }
            return truths
        except Exception:
            # Fallback to minimal ground truths
            return {
                "omega_lambda": {"z2_prediction": 13/19},
                "sin2_theta_w": {"z2_prediction": 3/13},
                "alpha_inverse": {"z2_prediction": 4 * Z2 + 3},
            }

    def validate(self, formula: str, computed_value: float,
                 target_value: float = None,
                 claim: str = "") -> FrameworkCheck:
        """
        Validate a formula/claim against Z² framework.

        Returns FrameworkCheck with detailed assessment.
        """
        self._log(f"Validating: {formula}")

        # Check if formula references Z²
        uses_z2 = self._check_z2_reference(formula)

        # Check for geometric basis
        geometric_basis = self._find_geometric_basis(formula, claim)

        # Check for physical mechanism
        physical_mechanism = self._find_physical_mechanism(claim)

        # Check against AletheiaLake
        aletheia_match, aletheia_name, aletheia_dev = \
            self._check_aletheia(computed_value)

        # Detect hidden assumptions
        assumptions = self._detect_assumptions(claim)
        problematic = self._identify_problematic_assumptions(assumptions)

        # Check for numerology red flags
        is_numerology = self._check_numerology(formula, claim, computed_value)

        # Calculate framework score
        score = self._calculate_score(
            uses_z2, geometric_basis, physical_mechanism,
            aletheia_match, problematic, is_numerology
        )

        return FrameworkCheck(
            claim=claim or f"{formula} = {computed_value}",
            formula=formula,
            computed_value=computed_value,
            uses_z2_constant=uses_z2,
            has_geometric_basis=bool(geometric_basis),
            has_physical_mechanism=bool(physical_mechanism),
            aletheia_match=aletheia_match,
            aletheia_truth_name=aletheia_name,
            aletheia_deviation=aletheia_dev,
            assumptions_detected=assumptions,
            problematic_assumptions=problematic,
            framework_score=score
        )

    def _check_z2_reference(self, formula: str) -> bool:
        """Check if formula references Z² or related constants."""
        z2_patterns = [
            r'Z²', r'Z\^2', r'Z2', r'32π/3', r'32\*pi/3',
            r'Z\s*=', r'\bZ\b', r'φ', r'phi', r'golden'
        ]
        formula_lower = formula.lower()
        for pattern in z2_patterns:
            if re.search(pattern, formula, re.IGNORECASE):
                return True

        # Also check for known Z² values
        for expr, val in self.valid_expressions.items():
            if expr.lower() in formula_lower:
                return True

        return False

    def _find_geometric_basis(self, formula: str, claim: str) -> Optional[str]:
        """Find geometric interpretation if present."""
        geometric_keywords = {
            "sphere": "spherical geometry",
            "cube": "cubic tessellation",
            "tetrahed": "tetrahedral structure",
            "octahed": "octahedral symmetry",
            "dodecahed": "dodecahedral geometry",
            "icosahed": "icosahedral symmetry",
            "solid angle": "solid angle geometry",
            "4π": "full solid angle",
            "8/3": "sphere-in-cube ratio",
            "packing": "sphere packing",
            "tessellation": "space tessellation",
            "manifold": "geometric manifold",
            "boundary": "holographic boundary",
            "surface": "surface geometry"
        }

        combined = f"{formula} {claim}".lower()
        for keyword, description in geometric_keywords.items():
            if keyword in combined:
                return description

        return None

    def _find_physical_mechanism(self, claim: str) -> Optional[str]:
        """Find physical mechanism if described."""
        mechanism_patterns = [
            (r'gauge\s+coupling', "gauge coupling mechanism"),
            (r'symmetry\s+breaking', "symmetry breaking"),
            (r'electroweak', "electroweak unification"),
            (r'holographic', "holographic principle"),
            (r'renormalization', "renormalization flow"),
            (r'running\s+coupling', "running coupling"),
            (r'QCD', "QCD dynamics"),
            (r'gravitational', "gravitational mechanism"),
            (r'cosmological', "cosmological mechanism"),
            (r'phase\s+transition', "phase transition"),
            (r'spontaneous', "spontaneous process"),
        ]

        claim_lower = claim.lower()
        for pattern, description in mechanism_patterns:
            if re.search(pattern, claim_lower):
                return description

        return None

    def _check_aletheia(self, computed_value: float) -> Tuple[bool, str, float]:
        """Check if value matches any AletheiaLake ground truth."""
        best_match = None
        best_deviation = float('inf')

        for name, truth in self.ground_truths.items():
            z2_pred = truth.get("z2_prediction")
            if z2_pred is None:
                continue

            # Calculate deviation
            if computed_value != 0:
                rel_diff = abs(computed_value - z2_pred) / abs(z2_pred)
            else:
                rel_diff = abs(z2_pred)

            # Check experimental uncertainty if available
            unc = truth.get("experimental_uncertainty")
            if unc and unc > 0:
                sigma_dev = abs(computed_value - z2_pred) / unc
            else:
                sigma_dev = rel_diff * 100  # Use percent as proxy

            if sigma_dev < best_deviation:
                best_deviation = sigma_dev
                best_match = name

        # Match if within 3 sigma
        if best_match and best_deviation < 3.0:
            return True, best_match, best_deviation

        return False, "", best_deviation if best_match else float('inf')

    def _detect_assumptions(self, claim: str) -> List[str]:
        """Detect assumptions in the claim."""
        assumptions = []
        claim_lower = claim.lower()

        for pattern in self.hidden_assumptions:
            if re.search(pattern, claim_lower):
                assumptions.append(pattern.replace(r'\.', '.').replace(r'\?', '?'))

        return assumptions

    def _identify_problematic_assumptions(self, assumptions: List[str]) -> List[str]:
        """Identify which assumptions are problematic for Z² framework."""
        problematic = []

        problematic_patterns = [
            'dark matter',
            'dark halo',
            'NFW',
            'ΛCDM',
            'lambda-CDM',
            'fine.?tuning',
        ]

        for assumption in assumptions:
            for problem in problematic_patterns:
                if re.search(problem, assumption, re.IGNORECASE):
                    problematic.append(assumption)
                    break

        return problematic

    def _check_numerology(self, formula: str, claim: str,
                          computed_value: float) -> bool:
        """Check for numerology red flags."""
        combined = f"{formula} {claim}".lower()

        # Check explicit numerology patterns
        for pattern in self.numerology_patterns:
            if re.search(pattern, combined):
                return True

        # Check if it's just a decimal approximation
        if not self._check_z2_reference(formula):
            # No Z² reference + random number = numerology
            known_z2_values = [Z2, Z, PHI, 3/13, 13/19, 6/19, 4*Z2+3, Z/6]
            for val in known_z2_values:
                if abs(computed_value - val) / max(abs(val), 0.001) < 0.01:
                    # Close to known value but no Z² reference
                    return True

        return False

    def _calculate_score(self, uses_z2: bool, geometric_basis: Optional[str],
                         physical_mechanism: Optional[str],
                         aletheia_match: bool, problematic: List[str],
                         is_numerology: bool) -> float:
        """Calculate overall framework alignment score."""
        score = 0.0

        # Positive factors
        if uses_z2:
            score += 0.25
        if geometric_basis:
            score += 0.20
        if physical_mechanism:
            score += 0.20
        if aletheia_match:
            score += 0.20

        # Negative factors
        if problematic:
            score -= 0.15 * len(problematic)
        if is_numerology:
            score -= 0.30

        # Clamp to [0, 1]
        return max(0.0, min(1.0, score + 0.15))  # Base score of 0.15

    def quick_check(self, value: float) -> Optional[str]:
        """
        Quick check if a value matches any known Z² expression.

        Returns the matching expression or None.
        """
        tolerance = 0.001  # 0.1%

        for expr, val in self.valid_expressions.items():
            if abs(value - val) / max(abs(val), 0.001) < tolerance:
                return expr

        return None
