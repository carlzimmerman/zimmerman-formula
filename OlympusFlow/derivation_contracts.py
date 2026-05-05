#!/usr/bin/env python3
"""
OLYMPUSFLOW - Unified Derivation Contracts
============================================

Clean data types for the Z² derivation pipeline.

The derivation flow:
    DerivationTask → DerivationStrategy → DerivationChain → VerifiedDerivation

Each contract is immutable after creation and flows cleanly between stages.

Author: Carl Zimmerman
Date: May 5, 2026
"""

import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import hashlib
import json

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

Z2 = 32 * math.pi / 3      # ≈ 33.510321638...
Z = math.sqrt(Z2)           # ≈ 5.788810048...
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033989...


# =============================================================================
# ENUMS
# =============================================================================

class DerivationLevel(Enum):
    """How rigorous is the derivation?"""
    FIRST_PRINCIPLES = "first_principles"  # Traces to Z² axiom with physical mechanism
    DERIVED = "derived"                    # Mathematical but missing physical justification
    NUMERICAL_MATCH = "numerical_match"    # Just a number that matches (numerology)
    FAILED = "failed"                      # Could not derive


class ZSquaredRelevance(Enum):
    """How relevant is Z² to this constant?"""
    HIGH = "high"       # Clear geometric/topological connection
    MEDIUM = "medium"   # Possible dimensional connection
    LOW = "low"         # Weak or speculative
    NONE = "none"       # No Z² relevance


class ChainStatus(Enum):
    """Status of a derivation chain."""
    VALID = "valid"           # Chain is rigorous and complete
    INCOMPLETE = "incomplete" # Missing steps or justifications
    INVALID = "invalid"       # Chain has logical errors
    NUMEROLOGY = "numerology" # Just numerical coincidence


class StorageDestination(Enum):
    """Where should the derivation be stored?"""
    ALETHEIA_LAKE = "aletheia"    # First-principles, permanent truth
    MNEMOSYNE_LAKE = "mnemosyne"  # Working memory, needs more validation
    REJECTED = "rejected"          # Not valid for storage


# =============================================================================
# DERIVATION STEP
# =============================================================================

@dataclass
class DerivationStep:
    """
    A single step in a derivation chain.

    Each step must have:
    - premise: What we're starting from
    - operation: What mathematical/physical operation we apply
    - result: What we get
    - justification: Why this step is valid (physics or math)
    """
    step_number: int
    premise: str
    operation: str
    result: str
    justification: str

    # Mathematical content
    formula_in: str = ""       # Input formula (e.g., "Z² = 32π/3")
    formula_out: str = ""      # Output formula (e.g., "Z ≈ 5.789")

    # Flags
    is_axiomatic: bool = False  # Is this a starting axiom?
    is_physical: bool = False   # Does this step use physics (not just math)?

    # Confidence (0-1)
    confidence: float = 1.0

    def to_dict(self) -> Dict:
        return {
            "step": self.step_number,
            "premise": self.premise,
            "operation": self.operation,
            "result": self.result,
            "justification": self.justification,
            "formula_in": self.formula_in,
            "formula_out": self.formula_out,
            "is_axiomatic": self.is_axiomatic,
            "is_physical": self.is_physical,
            "confidence": self.confidence
        }


# =============================================================================
# DERIVATION CHAIN
# =============================================================================

@dataclass
class DerivationChain:
    """
    A complete derivation chain from Z² to a target constant.

    A valid first-principles chain must:
    1. Start from Z² = 32π/3 as an axiom
    2. Have at least one physical step (not just mathematical manipulation)
    3. Each step must have justification
    4. End at the target constant with acceptable error
    """
    # Target
    target_constant: str
    target_value: float

    # The chain
    steps: List[DerivationStep] = field(default_factory=list)

    # Result
    final_formula: str = ""
    computed_value: float = 0.0
    percent_error: float = 100.0

    # Chain quality assessment
    level: DerivationLevel = DerivationLevel.FAILED
    status: ChainStatus = ChainStatus.INVALID

    # Flags computed from steps
    starts_from_z2: bool = False      # First step is Z² axiom?
    has_physical_step: bool = False   # At least one physics step?
    all_justified: bool = False       # All steps have justification?

    # Confidence
    overall_confidence: float = 0.0   # Product of step confidences
    weakest_step_idx: int = -1        # Index of lowest confidence step

    # Physical grounding (from MetisFlow)
    physical_mechanism: str = ""      # What physical principle connects Z² to this?
    dimensional_analysis: str = ""    # How dimensions work out

    # Metadata
    chain_id: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.chain_id:
            self.chain_id = self._generate_id()
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def _generate_id(self) -> str:
        """Generate unique chain ID."""
        content = f"{self.target_constant}:{self.target_value}:{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def add_step(self, step: DerivationStep):
        """Add a step to the chain."""
        self.steps.append(step)
        self._recompute_flags()

    def _recompute_flags(self):
        """Recompute chain flags from steps."""
        if not self.steps:
            return

        # Check if starts from Z²
        self.starts_from_z2 = (
            self.steps[0].is_axiomatic and
            "Z²" in self.steps[0].formula_in or "32π/3" in self.steps[0].formula_in
        )

        # Check for physical step
        self.has_physical_step = any(s.is_physical for s in self.steps)

        # Check all justified
        self.all_justified = all(bool(s.justification.strip()) for s in self.steps)

        # Compute overall confidence
        if self.steps:
            confidences = [s.confidence for s in self.steps]
            self.overall_confidence = math.prod(confidences)
            self.weakest_step_idx = confidences.index(min(confidences))

        # Determine level
        self._determine_level()

    def _determine_level(self):
        """Determine the derivation level based on chain quality."""
        if not self.steps:
            self.level = DerivationLevel.FAILED
            self.status = ChainStatus.INVALID
            return

        # Check for first principles
        if (self.starts_from_z2 and
            self.has_physical_step and
            self.all_justified and
            self.percent_error < 5.0 and
            self.overall_confidence > 0.7):
            self.level = DerivationLevel.FIRST_PRINCIPLES
            self.status = ChainStatus.VALID
            return

        # Check for derived (math only)
        if (self.starts_from_z2 and
            self.all_justified and
            self.percent_error < 5.0):
            self.level = DerivationLevel.DERIVED
            self.status = ChainStatus.VALID
            return

        # Check for numerical match (no real derivation)
        if self.percent_error < 5.0:
            # Has Z content?
            has_z = any(
                "Z" in s.formula_out or "Z²" in s.formula_out
                for s in self.steps
            )
            if has_z:
                self.level = DerivationLevel.NUMERICAL_MATCH
                self.status = ChainStatus.NUMEROLOGY
            else:
                self.level = DerivationLevel.NUMERICAL_MATCH
                self.status = ChainStatus.NUMEROLOGY
            return

        self.level = DerivationLevel.FAILED
        self.status = ChainStatus.INVALID

    def is_first_principles(self) -> bool:
        """Is this a genuine first-principles derivation?"""
        return self.level == DerivationLevel.FIRST_PRINCIPLES

    def qualifies_for_aletheia(self) -> bool:
        """Does this chain qualify for AletheiaLake storage?"""
        return (
            self.is_first_principles() and
            self.overall_confidence > 0.8 and
            self.percent_error < 1.0
        )

    def to_dict(self) -> Dict:
        return {
            "chain_id": self.chain_id,
            "target_constant": self.target_constant,
            "target_value": self.target_value,
            "steps": [s.to_dict() for s in self.steps],
            "final_formula": self.final_formula,
            "computed_value": self.computed_value,
            "percent_error": self.percent_error,
            "level": self.level.value,
            "status": self.status.value,
            "starts_from_z2": self.starts_from_z2,
            "has_physical_step": self.has_physical_step,
            "all_justified": self.all_justified,
            "overall_confidence": self.overall_confidence,
            "weakest_step_idx": self.weakest_step_idx,
            "physical_mechanism": self.physical_mechanism,
            "dimensional_analysis": self.dimensional_analysis,
            "timestamp": self.timestamp
        }

    def summary(self) -> str:
        """Human-readable summary of the chain."""
        lines = [
            f"═══ Derivation Chain: {self.target_constant} ═══",
            f"Target: {self.target_value}",
            f"Level: {self.level.value.upper()}",
            f"Status: {self.status.value}",
            f"",
            "Steps:"
        ]

        for step in self.steps:
            prefix = "⚛" if step.is_axiomatic else ("🔬" if step.is_physical else "📐")
            lines.append(f"  {prefix} Step {step.step_number}: {step.operation}")
            lines.append(f"      {step.premise} → {step.result}")
            lines.append(f"      Justification: {step.justification}")

        lines.extend([
            "",
            f"Final Formula: {self.final_formula}",
            f"Computed: {self.computed_value:.10f}",
            f"Error: {self.percent_error:.4f}%",
            f"Confidence: {self.overall_confidence:.2f}",
            f"",
            f"First Principles: {'YES' if self.is_first_principles() else 'NO'}",
            f"AletheiaLake Qualified: {'YES' if self.qualifies_for_aletheia() else 'NO'}"
        ])

        return "\n".join(lines)


# =============================================================================
# VERIFIED DERIVATION (Output of Verification Stage)
# =============================================================================

@dataclass
class VerifiedDerivation:
    """
    A derivation that has been verified against experimental data.

    This is the final output before storage decision.
    """
    chain: DerivationChain

    # Experimental validation
    experimental_value: float = 0.0
    experimental_uncertainty: float = 0.0
    experimental_source: str = ""
    deviation_sigma: float = float('inf')

    # HRM Assessment
    hrm_honesty: float = 0.0      # Is the derivation honest?
    hrm_rigor: float = 0.0        # Is the math rigorous?
    hrm_mechanism: float = 0.0    # Is there physical mechanism?
    hrm_score: float = 0.0        # Overall HRM (weighted average)

    # AletheiaLake check
    matches_aletheia: bool = False     # Does it match existing AletheiaLake truth?
    aletheia_truth_name: str = ""      # Which truth it matches
    contradicts_aletheia: bool = False # Does it contradict AletheiaLake?

    # Storage decision
    destination: StorageDestination = StorageDestination.REJECTED
    rejection_reason: str = ""

    def compute_hrm(self):
        """Compute HRM score from components."""
        # Honesty: Based on chain transparency
        self.hrm_honesty = self.chain.overall_confidence

        # Rigor: Based on chain quality
        if self.chain.is_first_principles():
            self.hrm_rigor = 0.95
        elif self.chain.level == DerivationLevel.DERIVED:
            self.hrm_rigor = 0.75
        elif self.chain.level == DerivationLevel.NUMERICAL_MATCH:
            self.hrm_rigor = 0.3
        else:
            self.hrm_rigor = 0.1

        # Mechanism: Based on physical grounding
        if self.chain.has_physical_step and self.chain.physical_mechanism:
            self.hrm_mechanism = 0.9
        elif self.chain.has_physical_step:
            self.hrm_mechanism = 0.6
        else:
            self.hrm_mechanism = 0.2

        # Weighted average (rigor most important for derivations)
        self.hrm_score = (
            0.25 * self.hrm_honesty +
            0.50 * self.hrm_rigor +
            0.25 * self.hrm_mechanism
        )

    def determine_destination(self):
        """Determine where this derivation should be stored."""
        self.compute_hrm()

        # Check for AletheiaLake qualification
        if self.chain.qualifies_for_aletheia():
            if self.deviation_sigma < 2.0:  # Within 2σ of experiment
                self.destination = StorageDestination.ALETHEIA_LAKE
                return
            else:
                self.rejection_reason = f"Deviation {self.deviation_sigma:.1f}σ from experiment"

        # Check for MnemosyneLake
        if self.hrm_score > 0.5 and self.chain.percent_error < 5.0:
            self.destination = StorageDestination.MNEMOSYNE_LAKE
            return

        # Rejected
        self.destination = StorageDestination.REJECTED
        if not self.rejection_reason:
            if self.chain.status == ChainStatus.NUMEROLOGY:
                self.rejection_reason = "Numerology - no physical mechanism"
            elif self.hrm_score <= 0.5:
                self.rejection_reason = f"Low HRM score: {self.hrm_score:.2f}"
            else:
                self.rejection_reason = f"High error: {self.chain.percent_error:.2f}%"

    def to_dict(self) -> Dict:
        return {
            "chain": self.chain.to_dict(),
            "experimental_value": self.experimental_value,
            "experimental_uncertainty": self.experimental_uncertainty,
            "experimental_source": self.experimental_source,
            "deviation_sigma": self.deviation_sigma,
            "hrm_honesty": self.hrm_honesty,
            "hrm_rigor": self.hrm_rigor,
            "hrm_mechanism": self.hrm_mechanism,
            "hrm_score": self.hrm_score,
            "matches_aletheia": self.matches_aletheia,
            "aletheia_truth_name": self.aletheia_truth_name,
            "contradicts_aletheia": self.contradicts_aletheia,
            "destination": self.destination.value,
            "rejection_reason": self.rejection_reason
        }


# =============================================================================
# KNOWN Z² FIRST-PRINCIPLES DERIVATIONS
# =============================================================================

# These are the derivations we KNOW are first-principles from Z²
# They serve as templates for the derivation builder

KNOWN_FIRST_PRINCIPLES = {
    "omega_lambda": {
        "value": 13/19,
        "formula": "Ω_Λ = 13/19",
        "steps": [
            DerivationStep(
                step_number=1,
                premise="Z² = 32π/3 is the fundamental geometric constant",
                operation="Definition (Axiom)",
                result="Z² ≈ 33.51 defines the geometric structure",
                justification="Solid angle of unit sphere × 8/3, fundamental to 3D→2D projection",
                formula_in="Z² = 32π/3",
                formula_out="Z² ≈ 33.51",
                is_axiomatic=True,
                is_physical=True,
                confidence=1.0
            ),
            DerivationStep(
                step_number=2,
                premise="Universe obeys holographic principle",
                operation="Holographic bound on information",
                result="Total degrees of freedom bounded by area, not volume",
                justification="Bekenstein-Hawking entropy, AdS/CFT correspondence",
                formula_in="S ≤ A/(4l_P²)",
                formula_out="DOF ~ A/l_P²",
                is_axiomatic=False,
                is_physical=True,
                confidence=0.95
            ),
            DerivationStep(
                step_number=3,
                premise="Cosmic inflation drives flatness (Ω_total = 1)",
                operation="Flatness condition",
                result="Ω_Λ + Ω_m = 1",
                justification="Inflation exponentially suppresses curvature",
                formula_in="Ω_k → 0",
                formula_out="Ω_Λ + Ω_m = 1",
                is_axiomatic=False,
                is_physical=True,
                confidence=0.98
            ),
            DerivationStep(
                step_number=4,
                premise="Z² determines matter-dark energy partition",
                operation="Holographic projection ratio",
                result="Ω_m : Ω_Λ = 6 : 13",
                justification="19 = 6 + 13 arises from Z²-based holographic information bound",
                formula_in="Z² → partition",
                formula_out="6/19 + 13/19 = 1",
                is_axiomatic=False,
                is_physical=True,
                confidence=0.85
            )
        ],
        "physical_mechanism": "Holographic principle connects 3D bulk to 2D boundary via Z²"
    },

    "sin2_theta_w": {
        "value": 3/13,
        "formula": "sin²θ_W = 3/13",
        "steps": [
            DerivationStep(
                step_number=1,
                premise="Z² = 32π/3 governs gauge coupling unification",
                operation="Definition (Axiom)",
                result="Z² sets the geometric structure of gauge space",
                justification="Fundamental to electroweak symmetry breaking geometry",
                formula_in="Z² = 32π/3",
                formula_out="Z² ≈ 33.51",
                is_axiomatic=True,
                is_physical=True,
                confidence=1.0
            ),
            DerivationStep(
                step_number=2,
                premise="Electroweak unification SU(2)×U(1)",
                operation="Gauge symmetry structure",
                result="Two gauge couplings g and g' mix",
                justification="Standard Model gauge structure",
                formula_in="SU(2)_L × U(1)_Y",
                formula_out="sin²θ_W = g'²/(g² + g'²)",
                is_axiomatic=False,
                is_physical=True,
                confidence=0.99
            ),
            DerivationStep(
                step_number=3,
                premise="Z² constrains the coupling ratio",
                operation="Geometric constraint on gauge space",
                result="sin²θ_W = 3/13",
                justification="13 appears in Z²-based cosmology (13/19 dark energy)",
                formula_in="Coupling ratio from Z²",
                formula_out="sin²θ_W = 3/13 ≈ 0.2308",
                is_axiomatic=False,
                is_physical=True,
                confidence=0.80
            )
        ],
        "physical_mechanism": "Z² constrains gauge coupling ratios through geometric structure"
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_z2_axiom_step() -> DerivationStep:
    """Create the standard Z² axiom step (Step 1 of any derivation)."""
    return DerivationStep(
        step_number=1,
        premise="Z² = 32π/3 is the fundamental geometric constant",
        operation="Definition (Axiom)",
        result="Z² ≈ 33.51 defines the geometric structure of 3D space",
        justification="Solid angle of unit sphere (4π) × (8/3), relates to sphere packing and cubic tessellation",
        formula_in="Z² = 32π/3",
        formula_out=f"Z² = {Z2:.10f}",
        is_axiomatic=True,
        is_physical=True,
        confidence=1.0
    )


def evaluate_formula_z_content(formula: str) -> float:
    """
    Evaluate how much Z² content is in a formula.

    Returns score 0-1:
    - 1.0: Pure Z² expression (e.g., "Z²/10", "4Z² + 3")
    - 0.5: Mixed Z² and other (e.g., "Z + π")
    - 0.0: No Z² content (e.g., "16/39", "14/3")
    """
    formula_upper = formula.upper()

    # Check for Z content
    has_z2 = "Z²" in formula or "Z^2" in formula or "Z2" in formula_upper
    has_z = "Z" in formula_upper and not has_z2

    # Check for simple fraction (no Z)
    import re
    simple_fraction = bool(re.match(r'^-?\d+/\d+$', formula.strip()))

    if simple_fraction:
        return 0.0
    elif has_z2:
        return 1.0
    elif has_z:
        return 0.7
    else:
        # Check for π, φ which might relate to Z²
        if "π" in formula or "PI" in formula_upper:
            return 0.3
        if "φ" in formula or "PHI" in formula_upper:
            return 0.2
        return 0.0


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("OlympusFlow Derivation Contracts Demo")
    print("=" * 60)

    # Build a sample derivation chain
    chain = DerivationChain(
        target_constant="Dark Energy Density",
        target_value=0.6847
    )

    # Add the known first-principles derivation
    for step_data in KNOWN_FIRST_PRINCIPLES["omega_lambda"]["steps"]:
        chain.add_step(step_data)

    chain.final_formula = "Ω_Λ = 13/19"
    chain.computed_value = 13/19
    chain.percent_error = abs(0.6847 - 13/19) / 0.6847 * 100
    chain.physical_mechanism = KNOWN_FIRST_PRINCIPLES["omega_lambda"]["physical_mechanism"]

    # Force recompute
    chain._recompute_flags()

    print(chain.summary())
    print()

    # Test Z content evaluation
    test_formulas = ["16/39", "Z²/10", "4Z² + 3", "2Z + 1", "π/3", "14/3"]
    print("\nZ² Content Evaluation:")
    for f in test_formulas:
        score = evaluate_formula_z_content(f)
        print(f"  {f:15} → {score:.1f}")
