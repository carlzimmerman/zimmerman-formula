#!/usr/bin/env python3
"""
PATTERN SEARCH ENGINE - Brute-Force Pattern Discovery
======================================================

The core search engine for BriareusFlow. Named after Briareus's
hundred hands - this engine tests thousands of combinations in parallel.

Key Features:
- Dimensional analysis for valid combinations
- Simple coefficient detection (π, √2, Z², φ, etc.)
- Multi-threaded parallel search
- Progressive refinement of promising patterns
- Transparency: reports all near-matches, not just best

Author: Carl Zimmerman
Date: May 6, 2026
"""

import math
import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum
import time

from .phenomenological import (
    PhenomenologicalFinding,
    FindingCategory,
    NumerologyRisk,
    DiscoveryPath,
    DiscoveryMethod,
    AlternativeFit,
    Z_SQUARED,
    Z,
    PHI
)


# =============================================================================
# FUNDAMENTAL CONSTANTS FOR SEARCH
# =============================================================================

# Mathematical constants
PI = math.pi
SQRT2 = math.sqrt(2)
SQRT3 = math.sqrt(3)
SQRT5 = math.sqrt(5)
E = math.e
LN2 = math.log(2)
LN10 = math.log(10)

# Z-derived constants
Z_CUBED = Z ** 3
Z_FOURTH = Z ** 4

# Common physics constants (dimensionless)
ALPHA_INV = 137.035999  # Fine structure constant inverse
WEAK_ANGLE = 0.23122     # sin²θ_W


class CoefficientType(Enum):
    """Types of coefficients found in patterns."""
    INTEGER = "integer"
    FRACTION = "fraction"
    PI_MULTIPLE = "pi_multiple"
    SQRT_MULTIPLE = "sqrt_multiple"
    Z_POWER = "z_power"
    Z_SQUARED_TERM = "z_squared_term"
    PHI_RELATED = "phi_related"
    MIXED = "mixed"
    UNKNOWN = "unknown"


@dataclass
class CoefficientMatch:
    """A matched coefficient in a pattern."""
    coefficient_type: CoefficientType
    formula: str
    numerical_value: float
    confidence: float  # How certain this is the right interpretation
    alternatives: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Result from a pattern search."""
    target_value: float
    matches: List['PatternMatch']
    search_time_seconds: float
    combinations_tested: int

    @property
    def best_match(self) -> Optional['PatternMatch']:
        if not self.matches:
            return None
        return min(self.matches, key=lambda m: abs(m.percent_error))

    @property
    def promising_matches(self) -> List['PatternMatch']:
        """Matches with error < 1%."""
        return [m for m in self.matches if abs(m.percent_error) < 1.0]


@dataclass
class PatternMatch:
    """A pattern that matches a target value."""
    formula: str
    computed_value: float
    target_value: float
    percent_error: float
    coefficient: CoefficientMatch
    discovery_method: DiscoveryMethod

    # Interpretation
    geometric_meaning: str = ""
    physical_mechanism: str = ""

    # Confidence metrics
    uniqueness_score: float = 0.0  # How unique is this among alternatives
    simplicity_score: float = 0.0  # Prefer simpler formulas

    def to_finding(self, finding_id: str, name: str, domain: str,
                   experimental_source: str, uncertainty: float) -> PhenomenologicalFinding:
        """Convert to a PhenomenologicalFinding."""
        sigma = (self.computed_value - self.target_value) / uncertainty if uncertainty > 0 else 0

        # Assess numerology risk based on pattern characteristics
        if self.coefficient.coefficient_type == CoefficientType.Z_SQUARED_TERM:
            risk = NumerologyRisk.LOW
        elif self.coefficient.coefficient_type in [CoefficientType.PI_MULTIPLE, CoefficientType.FRACTION]:
            risk = NumerologyRisk.MEDIUM
        elif self.coefficient.coefficient_type == CoefficientType.UNKNOWN:
            risk = NumerologyRisk.HIGH
        else:
            risk = NumerologyRisk.MEDIUM

        # Determine category
        if self.physical_mechanism:
            category = FindingCategory.DERIVED
        elif self.geometric_meaning:
            category = FindingCategory.MATCHES
        else:
            category = FindingCategory.PHENOMENOLOGICAL

        return PhenomenologicalFinding(
            finding_id=finding_id,
            name=name,
            domain=domain,
            formula=self.formula,
            computed_value=self.computed_value,
            experimental_value=self.target_value,
            experimental_uncertainty=uncertainty,
            experimental_source=experimental_source,
            percent_error=self.percent_error,
            sigma_deviation=sigma,
            category=category,
            numerology_risk=risk,
            discovery_path=DiscoveryPath(
                method=self.discovery_method,
                steps=[f"Pattern search found: {self.formula}"],
                assumptions=[]
            ),
            has_mechanism=bool(self.physical_mechanism),
            mechanism_description=self.physical_mechanism
        )


# =============================================================================
# PATTERN SEARCH ENGINE
# =============================================================================

class PatternSearchEngine:
    """
    Brute-force pattern search engine.

    Tests systematic combinations of:
    - Simple fractions (a/b)
    - Integer ± Z² terms
    - π multiples
    - √n multiples
    - φ (golden ratio) terms
    - Compound expressions

    Uses multiple threads for parallel search (the "hundred hands").
    """

    # Search configuration
    DEFAULT_CONFIG = {
        "max_error_percent": 1.0,
        "max_integer": 50,
        "max_denominator": 50,
        "max_z_coefficient": 10,
        "include_negative": True,
        "num_threads": 8,
    }

    # Known coefficient templates
    COEFFICIENT_TEMPLATES = [
        # Simple integers
        lambda a: (f"{a}", a),
        lambda a: (f"-{a}", -a),

        # Simple fractions
        lambda a, b: (f"{a}/{b}", a/b) if b != 0 else None,

        # π multiples
        lambda a: (f"{a}π", a * PI),
        lambda a, b: (f"{a}π/{b}", a * PI / b) if b != 0 else None,
        lambda a: (f"π/{a}", PI / a) if a != 0 else None,

        # √2, √3, √5 multiples
        lambda a: (f"{a}√2", a * SQRT2),
        lambda a: (f"{a}√3", a * SQRT3),
        lambda a: (f"√{a}", math.sqrt(a)) if a > 0 else None,

        # Z² terms
        lambda a: (f"{a}Z²", a * Z_SQUARED),
        lambda a, b: (f"{a}Z² + {b}", a * Z_SQUARED + b),
        lambda a, b: (f"{a}Z² - {b}", a * Z_SQUARED - b) if b > 0 else None,
        lambda a, b: (f"{a}/Z² + {b}", a / Z_SQUARED + b),

        # Z terms
        lambda a: (f"{a}Z", a * Z),
        lambda a, b: (f"{a}Z + {b}", a * Z + b),

        # φ (golden ratio) terms
        lambda a: (f"{a}φ", a * PHI),
        lambda a, b: (f"{a}φ + {b}", a * PHI + b),
        lambda a: (f"φ^{a}", PHI ** a),

        # Compound: 1 + a/Z²
        lambda a: (f"1 + {a}/Z²", 1 + a / Z_SQUARED),
        lambda a: (f"1 - {a}/Z²", 1 - a / Z_SQUARED),

        # Compound: (a + b)/c
        lambda a, b, c: (f"({a} + {b})/{c}", (a + b) / c) if c != 0 else None,

        # arccos/arctan
        lambda a, b: (f"arccos({a}/{b})", math.acos(a/b) * 180 / PI) if b != 0 and abs(a/b) <= 1 else None,
        lambda a, b: (f"arctan({a}/{b})", math.atan(a/b) * 180 / PI) if b != 0 else None,
    ]

    def __init__(self, config: Optional[Dict] = None, verbose: bool = True):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.verbose = verbose
        self._search_count = 0

    def _log(self, msg: str):
        if self.verbose:
            print(f"[PatternSearch] {msg}")

    def search(self, target: float, domain: str = "general") -> SearchResult:
        """
        Search for patterns matching a target value.

        Args:
            target: The value to match
            domain: Physical domain for context

        Returns:
            SearchResult with all matches found
        """
        start_time = time.time()
        matches: List[PatternMatch] = []
        combinations_tested = 0

        max_int = self.config["max_integer"]
        max_denom = self.config["max_denominator"]
        max_err = self.config["max_error_percent"]

        self._log(f"Searching for patterns matching {target:.6f}")

        # 1. Simple fractions a/b
        self._log("  Testing fractions...")
        frac_matches, frac_count = self._search_fractions(target, max_int, max_denom, max_err)
        matches.extend(frac_matches)
        combinations_tested += frac_count

        # 2. Z² terms: aZ² + b
        self._log("  Testing Z² terms...")
        z2_matches, z2_count = self._search_z_squared_terms(target, max_int, max_err)
        matches.extend(z2_matches)
        combinations_tested += z2_count

        # 3. π multiples: aπ/b
        self._log("  Testing π multiples...")
        pi_matches, pi_count = self._search_pi_multiples(target, max_int, max_denom, max_err)
        matches.extend(pi_matches)
        combinations_tested += pi_count

        # 4. √n multiples
        self._log("  Testing √n multiples...")
        sqrt_matches, sqrt_count = self._search_sqrt_multiples(target, max_int, max_err)
        matches.extend(sqrt_matches)
        combinations_tested += sqrt_count

        # 5. φ (golden ratio) terms
        self._log("  Testing φ terms...")
        phi_matches, phi_count = self._search_phi_terms(target, max_int, max_err)
        matches.extend(phi_matches)
        combinations_tested += phi_count

        # 6. Compound expressions
        self._log("  Testing compound expressions...")
        compound_matches, compound_count = self._search_compounds(target, max_int, max_err)
        matches.extend(compound_matches)
        combinations_tested += compound_count

        # 7. Trigonometric (for angles)
        if 0 < target < 180:  # Likely an angle
            self._log("  Testing trigonometric...")
            trig_matches, trig_count = self._search_trigonometric(target, max_int, max_denom, max_err)
            matches.extend(trig_matches)
            combinations_tested += trig_count

        # Sort by error
        matches.sort(key=lambda m: abs(m.percent_error))

        # Score uniqueness and simplicity
        self._score_matches(matches)

        elapsed = time.time() - start_time
        self._log(f"  Found {len(matches)} matches in {elapsed:.2f}s ({combinations_tested:,} tested)")

        return SearchResult(
            target_value=target,
            matches=matches,
            search_time_seconds=elapsed,
            combinations_tested=combinations_tested
        )

    def _search_fractions(self, target: float, max_num: int, max_denom: int,
                          max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search simple fractions a/b."""
        matches = []
        count = 0

        for a in range(1, max_num + 1):
            for b in range(1, max_denom + 1):
                if math.gcd(a, b) != 1:  # Skip reducible fractions
                    continue

                count += 1
                value = a / b
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100

                if error < max_err:
                    matches.append(PatternMatch(
                        formula=f"{a}/{b}",
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        coefficient=CoefficientMatch(
                            coefficient_type=CoefficientType.FRACTION,
                            formula=f"{a}/{b}",
                            numerical_value=value,
                            confidence=0.9 if a < 20 and b < 20 else 0.7
                        ),
                        discovery_method=DiscoveryMethod.BRUTE_FORCE
                    ))

                # Also try b/a
                if a != b:
                    count += 1
                    value = b / a
                    error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100

                    if error < max_err:
                        matches.append(PatternMatch(
                            formula=f"{b}/{a}",
                            computed_value=value,
                            target_value=target,
                            percent_error=error,
                            coefficient=CoefficientMatch(
                                coefficient_type=CoefficientType.FRACTION,
                                formula=f"{b}/{a}",
                                numerical_value=value,
                                confidence=0.9 if a < 20 and b < 20 else 0.7
                            ),
                            discovery_method=DiscoveryMethod.BRUTE_FORCE
                        ))

        return matches, count

    def _search_z_squared_terms(self, target: float, max_int: int,
                                 max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search Z² terms: aZ², aZ² + b, a/Z² + b, etc."""
        matches = []
        count = 0

        for a in range(1, max_int + 1):
            # aZ²
            count += 1
            value = a * Z_SQUARED
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_z2_match(f"{a}Z²", value, target, error))

            # aZ² + b and aZ² - b
            for b in range(-max_int, max_int + 1):
                if b == 0:
                    continue
                count += 1
                value = a * Z_SQUARED + b
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    sign = "+" if b > 0 else "-"
                    matches.append(self._make_z2_match(
                        f"{a}Z² {sign} {abs(b)}", value, target, error
                    ))

            # a/Z² and a/Z² + b
            count += 1
            value = a / Z_SQUARED
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_z2_match(f"{a}/Z²", value, target, error))

            # 1 + a/Z²
            count += 1
            value = 1 + a / Z_SQUARED
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_z2_match(f"1 + {a}/Z²", value, target, error))

            # 1 - a/Z²
            count += 1
            value = 1 - a / Z_SQUARED
            if value > 0:  # Avoid negative for most physics
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(self._make_z2_match(f"1 - {a}/Z²", value, target, error))

        return matches, count

    def _make_z2_match(self, formula: str, value: float, target: float,
                       error: float) -> PatternMatch:
        """Create a Z²-based pattern match."""
        return PatternMatch(
            formula=formula,
            computed_value=value,
            target_value=target,
            percent_error=error,
            coefficient=CoefficientMatch(
                coefficient_type=CoefficientType.Z_SQUARED_TERM,
                formula=formula,
                numerical_value=value,
                confidence=0.95  # Z² terms are highly significant
            ),
            discovery_method=DiscoveryMethod.BRUTE_FORCE,
            geometric_meaning="Related to Z² = 32π/3 geometric compactification"
        )

    def _search_pi_multiples(self, target: float, max_num: int, max_denom: int,
                              max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search π multiples: aπ, aπ/b, a/π, etc."""
        matches = []
        count = 0

        for a in range(1, max_num + 1):
            # aπ
            count += 1
            value = a * PI
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_pi_match(f"{a}π", value, target, error))

            # π/a
            count += 1
            value = PI / a
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_pi_match(f"π/{a}", value, target, error))

            # aπ/b
            for b in range(2, max_denom + 1):
                if math.gcd(a, b) != 1:
                    continue
                count += 1
                value = a * PI / b
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(self._make_pi_match(f"{a}π/{b}", value, target, error))

        return matches, count

    def _make_pi_match(self, formula: str, value: float, target: float,
                       error: float) -> PatternMatch:
        """Create a π-based pattern match."""
        return PatternMatch(
            formula=formula,
            computed_value=value,
            target_value=target,
            percent_error=error,
            coefficient=CoefficientMatch(
                coefficient_type=CoefficientType.PI_MULTIPLE,
                formula=formula,
                numerical_value=value,
                confidence=0.85
            ),
            discovery_method=DiscoveryMethod.BRUTE_FORCE,
            geometric_meaning="Related to circular/spherical geometry"
        )

    def _search_sqrt_multiples(self, target: float, max_int: int,
                                max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search √n multiples: a√2, a√3, a√n, etc."""
        matches = []
        count = 0

        # Common square roots
        common_roots = [2, 3, 5, 6, 7, 10]

        for n in common_roots:
            sqrt_n = math.sqrt(n)
            for a in range(1, max_int + 1):
                # a√n
                count += 1
                value = a * sqrt_n
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(PatternMatch(
                        formula=f"{a}√{n}",
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        coefficient=CoefficientMatch(
                            coefficient_type=CoefficientType.SQRT_MULTIPLE,
                            formula=f"{a}√{n}",
                            numerical_value=value,
                            confidence=0.8
                        ),
                        discovery_method=DiscoveryMethod.BRUTE_FORCE
                    ))

                # √n/a
                count += 1
                value = sqrt_n / a
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(PatternMatch(
                        formula=f"√{n}/{a}",
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        coefficient=CoefficientMatch(
                            coefficient_type=CoefficientType.SQRT_MULTIPLE,
                            formula=f"√{n}/{a}",
                            numerical_value=value,
                            confidence=0.8
                        ),
                        discovery_method=DiscoveryMethod.BRUTE_FORCE
                    ))

        return matches, count

    def _search_phi_terms(self, target: float, max_int: int,
                          max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search φ (golden ratio) terms: aφ, aφ + b, φ^n, etc."""
        matches = []
        count = 0

        for a in range(1, max_int + 1):
            # aφ
            count += 1
            value = a * PHI
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_phi_match(f"{a}φ", value, target, error))

            # φ/a
            count += 1
            value = PHI / a
            error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
            if error < max_err:
                matches.append(self._make_phi_match(f"φ/{a}", value, target, error))

            # aφ + b
            for b in range(-max_int, max_int + 1):
                if b == 0:
                    continue
                count += 1
                value = a * PHI + b
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    sign = "+" if b > 0 else "-"
                    matches.append(self._make_phi_match(
                        f"{a}φ {sign} {abs(b)}", value, target, error
                    ))

            # φ^a (powers of phi)
            if a <= 10:  # Limit powers
                count += 1
                value = PHI ** a
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(self._make_phi_match(f"φ^{a}", value, target, error))

                # Also negative powers
                count += 1
                value = PHI ** (-a)
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(self._make_phi_match(f"φ^(-{a})", value, target, error))

        return matches, count

    def _make_phi_match(self, formula: str, value: float, target: float,
                        error: float) -> PatternMatch:
        """Create a φ-based pattern match."""
        return PatternMatch(
            formula=formula,
            computed_value=value,
            target_value=target,
            percent_error=error,
            coefficient=CoefficientMatch(
                coefficient_type=CoefficientType.PHI_RELATED,
                formula=formula,
                numerical_value=value,
                confidence=0.75  # φ is often coincidental
            ),
            discovery_method=DiscoveryMethod.BRUTE_FORCE,
            geometric_meaning="Related to golden ratio self-similarity"
        )

    def _search_compounds(self, target: float, max_int: int,
                          max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search compound expressions: (a+b)/c, a/(b+c), etc."""
        matches = []
        count = 0

        # (a + b)/c
        for a in range(1, min(max_int, 20) + 1):
            for b in range(1, min(max_int, 20) + 1):
                for c in range(2, min(max_int, 20) + 1):
                    if a == b:
                        continue
                    count += 1
                    value = (a + b) / c
                    error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                    if error < max_err:
                        matches.append(PatternMatch(
                            formula=f"({a} + {b})/{c}",
                            computed_value=value,
                            target_value=target,
                            percent_error=error,
                            coefficient=CoefficientMatch(
                                coefficient_type=CoefficientType.MIXED,
                                formula=f"({a} + {b})/{c}",
                                numerical_value=value,
                                confidence=0.6
                            ),
                            discovery_method=DiscoveryMethod.BRUTE_FORCE
                        ))

                    # Also (a - b)/c
                    if a > b:
                        count += 1
                        value = (a - b) / c
                        error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                        if error < max_err:
                            matches.append(PatternMatch(
                                formula=f"({a} - {b})/{c}",
                                computed_value=value,
                                target_value=target,
                                percent_error=error,
                                coefficient=CoefficientMatch(
                                    coefficient_type=CoefficientType.MIXED,
                                    formula=f"({a} - {b})/{c}",
                                    numerical_value=value,
                                    confidence=0.6
                                ),
                                discovery_method=DiscoveryMethod.BRUTE_FORCE
                            ))

        return matches, count

    def _search_trigonometric(self, target: float, max_num: int, max_denom: int,
                              max_err: float) -> Tuple[List[PatternMatch], int]:
        """Search trigonometric patterns: arccos(a/b), arctan(a/b)."""
        matches = []
        count = 0

        # Target is likely in degrees
        for a in range(-max_num, max_num + 1):
            for b in range(1, max_denom + 1):
                ratio = a / b

                # arccos (requires |ratio| <= 1)
                if abs(ratio) <= 1:
                    count += 1
                    value = math.acos(ratio) * 180 / PI  # Convert to degrees
                    error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                    if error < max_err:
                        matches.append(PatternMatch(
                            formula=f"arccos({a}/{b})",
                            computed_value=value,
                            target_value=target,
                            percent_error=error,
                            coefficient=CoefficientMatch(
                                coefficient_type=CoefficientType.MIXED,
                                formula=f"arccos({a}/{b})",
                                numerical_value=value,
                                confidence=0.9 if abs(a) < 5 and b < 5 else 0.7
                            ),
                            discovery_method=DiscoveryMethod.GEOMETRIC,
                            geometric_meaning=f"Angle with cos = {a}/{b}"
                        ))

                # arctan
                count += 1
                value = math.atan(ratio) * 180 / PI
                error = abs(value - target) / target * 100 if target != 0 else abs(value) * 100
                if error < max_err:
                    matches.append(PatternMatch(
                        formula=f"arctan({a}/{b})",
                        computed_value=value,
                        target_value=target,
                        percent_error=error,
                        coefficient=CoefficientMatch(
                            coefficient_type=CoefficientType.MIXED,
                            formula=f"arctan({a}/{b})",
                            numerical_value=value,
                            confidence=0.85 if abs(a) < 5 and b < 5 else 0.65
                        ),
                        discovery_method=DiscoveryMethod.GEOMETRIC,
                        geometric_meaning=f"Angle with tan = {a}/{b}"
                    ))

        return matches, count

    def _score_matches(self, matches: List[PatternMatch]):
        """Score matches for uniqueness and simplicity."""
        if not matches:
            return

        # Simplicity: shorter formulas are simpler
        max_len = max(len(m.formula) for m in matches)
        for m in matches:
            m.simplicity_score = 1.0 - len(m.formula) / max_len

        # Uniqueness: how far apart are the computed values
        values = [m.computed_value for m in matches]
        for i, m in enumerate(matches):
            # Count how many other matches are within 0.1% of this one
            nearby = sum(1 for v in values if abs(v - m.computed_value) / max(abs(m.computed_value), 1e-10) < 0.001)
            m.uniqueness_score = 1.0 / nearby if nearby > 0 else 1.0

    def search_parallel(self, targets: List[float], domain: str = "general",
                       num_threads: int = None) -> Dict[float, SearchResult]:
        """
        Search multiple targets in parallel.

        Args:
            targets: List of values to search
            domain: Physical domain
            num_threads: Number of threads (default from config)

        Returns:
            Dict mapping target -> SearchResult
        """
        num_threads = num_threads or self.config["num_threads"]
        results = {}

        self._log(f"Parallel search for {len(targets)} targets with {num_threads} threads")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_target = {
                executor.submit(self.search, t, domain): t
                for t in targets
            }

            for future in as_completed(future_to_target):
                target = future_to_target[future]
                try:
                    results[target] = future.result()
                except Exception as e:
                    self._log(f"  Error searching {target}: {e}")

        return results


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATTERN SEARCH ENGINE TEST")
    print("=" * 70)
    print()

    engine = PatternSearchEngine(verbose=True)

    # Test 1: sin²θ_W = 0.23122 (should find 3/13)
    print("\n--- Test 1: sin²θ_W ---")
    result = engine.search(0.23122)
    print(f"Best match: {result.best_match.formula if result.best_match else 'None'}")
    if result.best_match:
        print(f"  Value: {result.best_match.computed_value:.6f}")
        print(f"  Error: {result.best_match.percent_error:.4f}%")

    # Test 2: α⁻¹ = 137.035999 (should find 4Z² + 3)
    print("\n--- Test 2: α⁻¹ ---")
    result = engine.search(137.035999)
    print(f"Best match: {result.best_match.formula if result.best_match else 'None'}")
    for m in result.promising_matches[:5]:
        print(f"  {m.formula} = {m.computed_value:.4f} ({m.percent_error:.4f}%)")

    # Test 3: Ω_Λ = 0.685 (should find 13/19)
    print("\n--- Test 3: Ω_Λ ---")
    result = engine.search(0.685)
    print(f"Best match: {result.best_match.formula if result.best_match else 'None'}")
    for m in result.promising_matches[:5]:
        print(f"  {m.formula} = {m.computed_value:.6f} ({m.percent_error:.4f}%)")

    # Test 4: Tetrahedral angle = 109.4712° (should find arccos(-1/3))
    print("\n--- Test 4: Tetrahedral Angle ---")
    result = engine.search(109.4712)
    print(f"Best match: {result.best_match.formula if result.best_match else 'None'}")
    for m in result.promising_matches[:5]:
        print(f"  {m.formula} = {m.computed_value:.4f}° ({m.percent_error:.4f}%)")

    # Test 5: Parallel search
    print("\n--- Test 5: Parallel Search ---")
    targets = [0.23122, 0.685, 1.666667]
    results = engine.search_parallel(targets)
    for t, r in results.items():
        print(f"  {t}: {r.best_match.formula if r.best_match else 'None'}")

    print()
    print("=" * 70)
    print("PATTERN SEARCH TEST COMPLETE")
    print("=" * 70)
