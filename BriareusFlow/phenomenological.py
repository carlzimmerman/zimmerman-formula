#!/usr/bin/env python3
"""
PHENOMENOLOGICAL FINDINGS - Data Structures
============================================

Data structures for representing phenomenological findings:
discoveries that match observational data but may not have
complete first-principles derivations.

Key Classifications:
- FIRST_PRINCIPLES: Rigorous logical derivation from axioms
- DERIVED: Logically derived from other truths
- MATCHES: Empirical agreement but incomplete derivation
- EMPIRICAL: Strong data support without mechanism
- NUMEROLOGY: Pattern matching without physics (flagged!)

Author: Carl Zimmerman
Date: May 6, 2026
"""

import math
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from enum import Enum


# Fundamental constants
Z_SQUARED = 32 * math.pi / 3  # ≈ 33.5103
Z = math.sqrt(Z_SQUARED)       # ≈ 5.7888
PHI = (1 + math.sqrt(5)) / 2   # Golden ratio


class FindingCategory(Enum):
    """
    Classification of phenomenological findings.

    From most rigorous to least:
    """
    FIRST_PRINCIPLES = "first_principles"  # Derived directly from Z² axioms
    DERIVED = "derived"                     # Logically derived from other truths
    MATCHES = "matches"                     # Matches observation, derivation partial
    EMPIRICAL = "empirical"                 # Strong empirical support
    PHENOMENOLOGICAL = "phenomenological"   # Pattern found, needs investigation
    NUMEROLOGY = "numerology"               # Pure pattern matching, no physics


class NumerologyRisk(Enum):
    """
    Risk level that a finding is coincidental numerology.
    """
    LOW = "low"           # Strong physical mechanism
    MEDIUM = "medium"     # Plausible mechanism, needs validation
    HIGH = "high"         # Likely coincidence
    VERY_HIGH = "very_high"  # Almost certainly coincidence
    UNKNOWN = "unknown"   # Not yet assessed


class DiscoveryMethod(Enum):
    """
    How the pattern was discovered.
    """
    BRUTE_FORCE = "brute_force"         # Exhaustive search
    DIMENSIONAL_ANALYSIS = "dimensional"  # Dimensional consistency
    GEOMETRIC = "geometric"              # Geometric interpretation
    ALGEBRAIC = "algebraic"              # Algebraic manipulation
    CROSS_DOMAIN = "cross_domain"        # Pattern from another domain
    LLM_SUGGESTED = "llm_suggested"      # Suggested by Legomena
    HUMAN_INSIGHT = "human_insight"      # Carl's intuition


@dataclass
class DiscoveryPath:
    """
    Documents how a finding was discovered.

    This is critical for transparency - shows exactly how
    we arrived at a formula, preventing hidden assumptions.
    """
    method: DiscoveryMethod
    steps: List[str]                  # Step-by-step derivation
    assumptions: List[str]            # Explicit assumptions made
    alternatives_tested: int = 0      # How many alternatives were tried
    search_space_size: int = 0        # Total search space
    discovery_time: str = ""          # When discovered

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["method"] = self.method.value
        return d


@dataclass
class AlternativeFit:
    """
    An alternative formula that also fits the data.

    Critical for honesty - if multiple formulas fit,
    we must disclose this.
    """
    formula: str
    computed_value: float
    percent_error: float
    has_mechanism: bool = False
    mechanism_description: str = ""


@dataclass
class PhenomenologicalFinding:
    """
    A phenomenological finding - pattern that matches data
    but may not have a complete derivation.

    This is the core data structure for BriareusFlow.
    """
    # Identity
    finding_id: str
    name: str
    domain: str

    # The pattern found
    formula: str
    computed_value: float

    # Comparison to data
    experimental_value: float
    experimental_uncertainty: float
    experimental_source: str
    percent_error: float
    sigma_deviation: float  # (computed - experimental) / uncertainty

    # Classification
    category: FindingCategory
    numerology_risk: NumerologyRisk

    # Discovery documentation
    discovery_path: DiscoveryPath

    # Transparency
    alternative_fits: List[AlternativeFit] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Physical interpretation
    has_mechanism: bool = False
    mechanism_description: str = ""
    testable_predictions: List[str] = field(default_factory=list)
    falsification_conditions: List[str] = field(default_factory=list)

    # Metadata
    timestamp: str = ""
    validated_by_olympus: bool = False
    olympus_result: Optional[Dict] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

        # Auto-generate warnings based on risk
        self._generate_warnings()

    def _generate_warnings(self):
        """Generate transparency warnings based on finding characteristics."""
        if self.numerology_risk in [NumerologyRisk.HIGH, NumerologyRisk.VERY_HIGH]:
            self.warnings.append(
                f"HIGH NUMEROLOGY RISK: This pattern may be coincidental"
            )

        if len(self.alternative_fits) > 2:
            self.warnings.append(
                f"MULTIPLE FITS: {len(self.alternative_fits)} other formulas "
                f"also match within similar error"
            )

        if not self.has_mechanism:
            self.warnings.append(
                "NO MECHANISM: No physical explanation for this pattern yet"
            )

        if self.category == FindingCategory.NUMEROLOGY:
            self.warnings.append(
                "NUMEROLOGY FLAG: This appears to be pure pattern matching"
            )

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        d["category"] = self.category.value
        d["numerology_risk"] = self.numerology_risk.value
        d["discovery_path"] = self.discovery_path.to_dict()
        return d

    @property
    def is_promising(self) -> bool:
        """Check if finding is worth pursuing."""
        return (
            self.percent_error < 1.0 and
            self.numerology_risk in [NumerologyRisk.LOW, NumerologyRisk.MEDIUM] and
            self.category in [
                FindingCategory.FIRST_PRINCIPLES,
                FindingCategory.DERIVED,
                FindingCategory.MATCHES
            ]
        )

    @property
    def needs_validation(self) -> bool:
        """Check if finding needs OlympusFlow validation."""
        return (
            not self.validated_by_olympus and
            self.category != FindingCategory.NUMEROLOGY and
            self.percent_error < 5.0
        )

    def add_alternative(self, formula: str, value: float, error: float,
                       has_mechanism: bool = False, mechanism: str = ""):
        """Add an alternative fit for transparency."""
        self.alternative_fits.append(AlternativeFit(
            formula=formula,
            computed_value=value,
            percent_error=error,
            has_mechanism=has_mechanism,
            mechanism_description=mechanism
        ))
        self._generate_warnings()  # Regenerate warnings

    def summary(self) -> str:
        """Generate human-readable summary."""
        lines = [
            f"Finding: {self.name}",
            f"Domain: {self.domain}",
            f"Formula: {self.formula}",
            f"Computed: {self.computed_value:.6f}",
            f"Experimental: {self.experimental_value:.6f} ± {self.experimental_uncertainty:.6f}",
            f"Error: {self.percent_error:.4f}%",
            f"Category: {self.category.value}",
            f"Numerology Risk: {self.numerology_risk.value}",
        ]

        if self.warnings:
            lines.append("WARNINGS:")
            for w in self.warnings:
                lines.append(f"  ! {w}")

        if self.has_mechanism:
            lines.append(f"Mechanism: {self.mechanism_description}")

        return "\n".join(lines)


@dataclass
class FindingBatch:
    """
    A batch of phenomenological findings from a search run.
    """
    batch_id: str
    search_config: Dict
    total_combinations_tested: int
    runtime_seconds: float
    findings: List[PhenomenologicalFinding]

    # Statistics
    first_principles_count: int = 0
    matches_count: int = 0
    numerology_count: int = 0

    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

        # Compute statistics
        for f in self.findings:
            if f.category == FindingCategory.FIRST_PRINCIPLES:
                self.first_principles_count += 1
            elif f.category == FindingCategory.MATCHES:
                self.matches_count += 1
            elif f.category == FindingCategory.NUMEROLOGY:
                self.numerology_count += 1

    @property
    def promising_findings(self) -> List[PhenomenologicalFinding]:
        """Get findings worth pursuing."""
        return [f for f in self.findings if f.is_promising]

    @property
    def needs_validation(self) -> List[PhenomenologicalFinding]:
        """Get findings that need OlympusFlow validation."""
        return [f for f in self.findings if f.needs_validation]

    def summary(self) -> str:
        """Generate batch summary."""
        return (
            f"Batch {self.batch_id}\n"
            f"Combinations tested: {self.total_combinations_tested:,}\n"
            f"Runtime: {self.runtime_seconds:.1f}s\n"
            f"Total findings: {len(self.findings)}\n"
            f"  First principles: {self.first_principles_count}\n"
            f"  Matches: {self.matches_count}\n"
            f"  Numerology: {self.numerology_count}\n"
            f"Promising: {len(self.promising_findings)}\n"
            f"Need validation: {len(self.needs_validation)}"
        )


# =============================================================================
# KNOWN PHENOMENOLOGICAL PATTERNS
# =============================================================================

# These are patterns discovered through brute force that need investigation
KNOWN_PHENOMENOLOGICAL = {
    "z2_sphere_cube": {
        "formula": "8 × (4π/3)",
        "value": Z_SQUARED,
        "description": "Cube vertices × sphere volume = Z²",
        "status": "FIRST_PRINCIPLES",
        "mechanism": "Compactification geometry"
    },
    "friedmann_z2": {
        "formula": "4 × (8π/3)",
        "value": Z_SQUARED,
        "description": "Dimensions × Friedmann coefficient",
        "status": "FIRST_PRINCIPLES",
        "mechanism": "Spacetime curvature"
    },
    "al_lensing": {
        "formula": "1 + 6/Z²",
        "value": 1 + 6/Z_SQUARED,
        "description": "CMB lensing amplitude",
        "status": "PHENOMENOLOGICAL",
        "mechanism": None,
        "warning": "Multiple formulas fit within 1σ"
    }
}


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PHENOMENOLOGICAL FINDING TEST")
    print("=" * 70)
    print()

    # Create a test finding
    finding = PhenomenologicalFinding(
        finding_id="test_001",
        name="sin²θ_W",
        domain="particle_physics",
        formula="3/13",
        computed_value=3/13,
        experimental_value=0.23122,
        experimental_uncertainty=0.00003,
        experimental_source="PDG 2024",
        percent_error=abs(3/13 - 0.23122) / 0.23122 * 100,
        sigma_deviation=(3/13 - 0.23122) / 0.00003,
        category=FindingCategory.FIRST_PRINCIPLES,
        numerology_risk=NumerologyRisk.LOW,
        discovery_path=DiscoveryPath(
            method=DiscoveryMethod.BRUTE_FORCE,
            steps=[
                "Searched simple fractions a/b for a,b in [1,50]",
                "Found 3/13 = 0.230769",
                "Error to experimental: 0.195%"
            ],
            assumptions=["Electroweak mixing angle is fundamental"],
            alternatives_tested=2500,
            search_space_size=2500
        ),
        has_mechanism=True,
        mechanism_description="Electroweak gauge coupling ratio from SU(2)×U(1)",
        testable_predictions=[
            "cos²θ_W = 10/13",
            "M_W/M_Z = √(10/13)"
        ]
    )

    # Add an alternative
    finding.add_alternative(
        formula="arctan(4/17)",
        value=math.atan(4/17),
        error=0.056,
        has_mechanism=False
    )

    print(finding.summary())
    print()

    print(f"Is promising: {finding.is_promising}")
    print(f"Needs validation: {finding.needs_validation}")
    print()

    # Test batch
    batch = FindingBatch(
        batch_id="overnight_001",
        search_config={"max_error": 1.0, "search_type": "fractions"},
        total_combinations_tested=50000,
        runtime_seconds=3600,
        findings=[finding]
    )

    print(batch.summary())
    print()

    print("=" * 70)
    print("PHENOMENOLOGICAL TEST COMPLETE")
    print("=" * 70)
