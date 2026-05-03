#!/usr/bin/env python3
"""
HRM Validator - Honesty, Rigor, Methodology
============================================
Full HRM validation of Z² predictions against empirical data.

This is the CORE of TruthFlow's validation philosophy:
- Every value must come from a cited source
- Every prediction must be classified by derivation level
- Every comparison must compute sigma tension
- Every failure must be documented

Author: Carl Zimmerman
Date: May 2, 2026
"""

import json
import numpy as np
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from enum import Enum
from datetime import datetime


# ============================================================================
# ENUMS AND DATA STRUCTURES
# ============================================================================

class DerivationLevel(Enum):
    """How rigorously is this prediction derived?"""
    DERIVED = "DERIVED"           # From first principles (geometry)
    PARTIAL = "PARTIAL"           # Mechanism works but WHY unknown
    MATCHES = "MATCHES"           # Numerically matches, no derivation
    SPECULATION = "SPECULATION"   # Pattern matching only


class SourceTier(Enum):
    """Quality of empirical source."""
    TIER_1 = 1  # Official databases (CODATA, PDG, Planck)
    TIER_2 = 2  # Peer-reviewed papers
    TIER_3 = 3  # Preprints (arXiv without journal)
    TIER_4 = 4  # Community data


class ValidationStatus(Enum):
    """Result of sigma tension comparison."""
    VALIDATED = "VALIDATED"   # σ < 2
    TENSION = "TENSION"       # 2 ≤ σ < 3
    FAILED = "FAILED"         # σ ≥ 3
    PENDING = "PENDING"       # No measurement yet


@dataclass
class HRMResult:
    """Complete HRM assessment of a single prediction."""
    # Identity
    name: str
    z2_formula: str

    # HONESTY
    derivation_level: str
    mechanism_known: bool
    is_speculative: bool

    # RIGOR
    z2_prediction: float
    empirical_value: Optional[float]
    uncertainty: Optional[float]
    source: str
    source_tier: int
    arxiv: Optional[str]
    citation: str

    # METHODOLOGY
    sigma_tension: Optional[float]
    percent_error: Optional[float]
    status: str
    falsifiable: bool
    falsification_test: Optional[str]
    next_experiment: Optional[str]

    # Meta
    timestamp: str
    notes: str


# ============================================================================
# Z² PREDICTIONS WITH HRM CLASSIFICATION
# ============================================================================

Z2_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z2_SQUARED)       # ≈ 5.79

Z2_PREDICTIONS = {
    "Omega_Lambda": {
        "formula": "13/19",
        "compute": lambda: 13/19,
        "derivation": DerivationLevel.PARTIAL,
        "mechanism_known": False,
        "notes": "DOF partition works, but WHY 13 and 19?",
        "falsifiable": True,
        "falsification_test": "|Ω_Λ - 0.6842| > 0.01 at >3σ",
        "next_experiment": "Euclid"
    },
    "Omega_m": {
        "formula": "6/19",
        "compute": lambda: 6/19,
        "derivation": DerivationLevel.PARTIAL,
        "mechanism_known": False,
        "notes": "Complementary to Ω_Λ",
        "falsifiable": True,
        "falsification_test": "|Ω_m - 0.316| > 0.01 at >3σ",
        "next_experiment": "Euclid"
    },
    "alpha_inverse": {
        "formula": "4Z² + 3",
        "compute": lambda: 4 * Z2_SQUARED + 3,
        "derivation": DerivationLevel.MATCHES,
        "mechanism_known": False,
        "notes": "WHY 4 and 3? Remarkable match but no derivation",
        "falsifiable": False,
        "falsification_test": None,
        "next_experiment": None
    },
    "sin2_theta_W": {
        "formula": "3/13",
        "compute": lambda: 3/13,
        "derivation": DerivationLevel.MATCHES,
        "mechanism_known": False,
        "notes": "WHY 3 and 13? Matches to 0.19%",
        "falsifiable": True,
        "falsification_test": "MOLLER measurement differs by >3σ",
        "next_experiment": "MOLLER"
    },
    "a0_mond": {
        "formula": "c*H0/Z",
        "compute": lambda: (3e8 * 67.4/3.086e19) / Z,  # c*H0/Z
        "derivation": DerivationLevel.DERIVED,
        "mechanism_known": True,
        "notes": "Genuine derivation from holographic/MOND connection",
        "falsifiable": True,
        "falsification_test": "MOND fails in wide binaries",
        "next_experiment": "Gaia DR4"
    },
    "hierarchy_ratio": {
        "formula": "2 × Z^(43/2)",
        "compute": lambda: 2 * (Z ** 21.5),
        "derivation": DerivationLevel.PARTIAL,
        "mechanism_known": False,
        "notes": "43 = 64-19-2 decomposition works, mechanism unclear",
        "falsifiable": False,
        "falsification_test": None,
        "next_experiment": None
    },
    "tensor_scalar_r": {
        "formula": "1/(2Z²) = 3/(64π)",
        "compute": lambda: 1 / (2 * Z2_SQUARED),
        "derivation": DerivationLevel.PARTIAL,
        "mechanism_known": False,
        "notes": "Inflation prediction, not yet measured",
        "falsifiable": True,
        "falsification_test": "r < 0.005 OR r > 0.025",
        "next_experiment": "LiteBIRD"
    },
    "gauge_bosons": {
        "formula": "GAUGE = 12 (cube edges)",
        "compute": lambda: 12,
        "derivation": DerivationLevel.DERIVED,
        "mechanism_known": True,
        "notes": "Cube has 12 edges, matches SM gauge boson count",
        "falsifiable": False,
        "falsification_test": None,
        "next_experiment": None
    },
    "generations": {
        "formula": "b₁(T³) = 3",
        "compute": lambda: 3,
        "derivation": DerivationLevel.DERIVED,
        "mechanism_known": True,
        "notes": "First Betti number of 3-torus",
        "falsifiable": True,
        "falsification_test": "4th generation discovered",
        "next_experiment": "LHC/FCC"
    },
    "w0_dark_energy": {
        "formula": "-1 exactly",
        "compute": lambda: -1.0,
        "derivation": DerivationLevel.DERIVED,
        "mechanism_known": True,
        "notes": "Cosmological constant, not quintessence",
        "falsifiable": True,
        "falsification_test": "|w₀ + 1| > 0.05",
        "next_experiment": "DESI Y5"
    },
}


# ============================================================================
# LOAD EMPIRICAL DATA
# ============================================================================

def load_empirical_sources() -> Dict:
    """Load empirical data from JSON."""
    sources_file = Path(__file__).parent / "empirical_sources.json"
    with open(sources_file, 'r') as f:
        return json.load(f)


def get_empirical_value(name: str, sources: Dict) -> Tuple[Optional[float], Optional[float], str, int, Optional[str]]:
    """
    Get empirical value for a prediction.

    Returns: (value, uncertainty, source_name, tier, arxiv)
    """
    # Map prediction names to source locations
    mapping = {
        "Omega_Lambda": ("cosmology", "Omega_Lambda"),
        "Omega_m": ("cosmology", "Omega_m"),
        "alpha_inverse": ("particle_physics", "alpha_inverse"),
        "sin2_theta_W": ("particle_physics", "sin2_theta_W"),
        "a0_mond": ("mond_dynamics", "a0"),
        "hierarchy_ratio": ("particle_physics", "hierarchy_ratio"),
        "tensor_scalar_r": ("cosmology", "tensor_scalar_r"),
        "gauge_bosons": ("particle_physics", "gauge_bosons"),
        "generations": ("particle_physics", "generations"),
        "w0_dark_energy": ("cosmology", "w0"),
    }

    if name not in mapping:
        return None, None, "Unknown", 4, None

    category, key = mapping[name]
    data = sources.get(category, {}).get(key, {})

    value = data.get("value")
    uncertainty = data.get("uncertainty", 0)
    source = data.get("source", "Unknown")
    arxiv = data.get("arxiv")

    # Determine tier
    tier_map = {
        "CODATA_2022": 1,
        "PDG_2024": 1,
        "Planck_2020": 1,
        "McGaugh_2016": 2,
        "DESI_2024": 2,
        "Standard Model": 1,
    }
    tier = tier_map.get(source, 3)

    return value, uncertainty, source, tier, arxiv


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def compute_sigma_tension(prediction: float, measurement: float, uncertainty: float) -> float:
    """Compute sigma tension."""
    if uncertainty == 0 or uncertainty is None:
        return 0.0
    return abs(prediction - measurement) / uncertainty


def compute_percent_error(prediction: float, measurement: float) -> float:
    """Compute percent error."""
    if measurement == 0:
        return 0.0
    return abs(prediction - measurement) / abs(measurement) * 100


def classify_status(sigma: Optional[float]) -> ValidationStatus:
    """Classify validation status based on sigma."""
    if sigma is None:
        return ValidationStatus.PENDING
    if sigma < 2:
        return ValidationStatus.VALIDATED
    if sigma < 3:
        return ValidationStatus.TENSION
    return ValidationStatus.FAILED


def format_citation(source: str, arxiv: Optional[str]) -> str:
    """Format a proper citation."""
    if arxiv:
        return f"{source} (arXiv:{arxiv})"
    return source


# ============================================================================
# MAIN HRM VALIDATION
# ============================================================================

def validate_single(name: str, sources: Dict) -> HRMResult:
    """
    Perform full HRM validation of a single prediction.
    """
    pred_info = Z2_PREDICTIONS[name]
    z2_value = pred_info["compute"]()

    # Get empirical data
    emp_value, emp_unc, source, tier, arxiv = get_empirical_value(name, sources)

    # Compute metrics
    if emp_value is not None and emp_unc is not None and emp_unc > 0:
        sigma = compute_sigma_tension(z2_value, emp_value, emp_unc)
        pct_error = compute_percent_error(z2_value, emp_value)
        status = classify_status(sigma)
    else:
        sigma = None
        pct_error = None
        status = ValidationStatus.PENDING

    return HRMResult(
        # Identity
        name=name,
        z2_formula=pred_info["formula"],

        # HONESTY
        derivation_level=pred_info["derivation"].value,
        mechanism_known=pred_info["mechanism_known"],
        is_speculative=(pred_info["derivation"] == DerivationLevel.SPECULATION),

        # RIGOR
        z2_prediction=z2_value,
        empirical_value=emp_value,
        uncertainty=emp_unc,
        source=source,
        source_tier=tier,
        arxiv=arxiv,
        citation=format_citation(source, arxiv),

        # METHODOLOGY
        sigma_tension=sigma,
        percent_error=pct_error,
        status=status.value,
        falsifiable=pred_info["falsifiable"],
        falsification_test=pred_info.get("falsification_test"),
        next_experiment=pred_info.get("next_experiment"),

        # Meta
        timestamp=datetime.now().isoformat(),
        notes=pred_info["notes"]
    )


def validate_all() -> List[HRMResult]:
    """Validate all Z² predictions with full HRM methodology."""
    sources = load_empirical_sources()
    results = []

    for name in Z2_PREDICTIONS:
        result = validate_single(name, sources)
        results.append(result)

    return results


def generate_hrm_report(results: List[HRMResult]) -> str:
    """Generate human-readable HRM report."""
    lines = [
        "# HRM Validation Report",
        f"\n**Generated:** {datetime.now().isoformat()}",
        f"**Framework:** Z² = 32π/3 = {Z2_SQUARED:.6f}",
        "",
        "## Honesty Summary",
        "",
        "| Prediction | Derivation Level | Mechanism Known |",
        "|------------|------------------|-----------------|",
    ]

    for r in results:
        mech = "✓" if r.mechanism_known else "✗"
        lines.append(f"| {r.name} | {r.derivation_level} | {mech} |")

    lines.extend([
        "",
        "## Rigor Summary",
        "",
        "| Prediction | Z² | Empirical | σ | Error | Status |",
        "|------------|-----|-----------|---|-------|--------|",
    ])

    for r in results:
        if r.status == "PENDING":
            lines.append(f"| {r.name} | {r.z2_prediction:.6g} | TBD | - | - | ⏳ |")
        else:
            status_emoji = {"VALIDATED": "✅", "TENSION": "⚠️", "FAILED": "❌"}.get(r.status, "?")
            sigma_str = f"{r.sigma_tension:.2f}" if r.sigma_tension else "-"
            error_str = f"{r.percent_error:.4f}%" if r.percent_error else "-"
            emp_str = f"{r.empirical_value:.6g}" if r.empirical_value else "TBD"
            lines.append(
                f"| {r.name} | {r.z2_prediction:.6g} | "
                f"{emp_str} | "
                f"{sigma_str} | {error_str} | {status_emoji} |"
            )

    lines.extend([
        "",
        "## Source Citations",
        "",
    ])

    for r in results:
        lines.append(f"- **{r.name}**: {r.citation}")

    lines.extend([
        "",
        "## Falsification Tests",
        "",
        "| Prediction | Falsifiable | Test | Next Experiment |",
        "|------------|-------------|------|-----------------|",
    ])

    for r in results:
        fals = "✓" if r.falsifiable else "✗"
        test = r.falsification_test or "-"
        exp = r.next_experiment or "-"
        lines.append(f"| {r.name} | {fals} | {test[:30]}... | {exp} |")

    # Summary statistics
    derived = sum(1 for r in results if r.derivation_level == "DERIVED")
    partial = sum(1 for r in results if r.derivation_level == "PARTIAL")
    matches = sum(1 for r in results if r.derivation_level == "MATCHES")
    validated = sum(1 for r in results if r.status == "VALIDATED")
    falsifiable = sum(1 for r in results if r.falsifiable)

    lines.extend([
        "",
        "## Summary Statistics",
        "",
        f"- **DERIVED predictions:** {derived}",
        f"- **PARTIAL derivations:** {partial}",
        f"- **MATCHES (no derivation):** {matches}",
        f"- **VALIDATED (σ<2):** {validated}/{len(results)}",
        f"- **Falsifiable:** {falsifiable}/{len(results)}",
        "",
        "---",
        "*HRM: Honesty, Rigor, Methodology*",
        "*TruthFlow Validation System*"
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("HRM VALIDATOR - Full Methodology Assessment")
    print("=" * 60)
    print(f"\nZ² = 32π/3 = {Z2_SQUARED:.6f}")
    print()

    results = validate_all()

    # Print summary
    print("-" * 60)
    print("RESULTS")
    print("-" * 60)

    for r in results:
        status_sym = {"VALIDATED": "✓", "TENSION": "~", "FAILED": "✗", "PENDING": "?"}.get(r.status, "?")
        deriv_sym = {"DERIVED": "D", "PARTIAL": "P", "MATCHES": "M", "SPECULATION": "S"}.get(r.derivation_level, "?")

        if r.status == "PENDING":
            print(f"[{status_sym}][{deriv_sym}] {r.name}: {r.z2_prediction:.6g} (awaiting measurement)")
        else:
            sigma_val = r.sigma_tension if r.sigma_tension else 0
            error_val = r.percent_error if r.percent_error else 0
            print(f"[{status_sym}][{deriv_sym}] {r.name}: {r.z2_prediction:.6g} vs {r.empirical_value:.6g} | "
                  f"σ={sigma_val:.2f} | {error_val:.4f}% error")

    # Generate and save report
    report = generate_hrm_report(results)
    output_dir = Path(__file__).parent.parent / "validated_truths"
    output_dir.mkdir(exist_ok=True)

    report_file = output_dir / f"hrm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n✓ Report saved to: {report_file}")

    # Also save JSON
    json_file = report_file.with_suffix('.json')
    with open(json_file, 'w') as f:
        json.dump([asdict(r) for r in results], f, indent=2, default=str)

    print(f"✓ JSON saved to: {json_file}")
