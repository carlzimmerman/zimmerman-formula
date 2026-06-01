#!/usr/bin/env python3
"""
TruthFlow Assessor - Bayesian Honesty Assessment
=================================================
Validates Z² predictions against empirical data.

The Validation Protocol:
- σ < 2: VALIDATED (consistent with measurement)
- 2 ≤ σ < 3: TENSION (needs investigation)
- σ ≥ 3: FAILED (either Z² wrong OR measurement error)

Author: Carl Zimmerman
Date: May 2, 2026
"""

import json
import os
import sys
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path

# Add compute directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "03_compute"))
from z2_engine import (
    Z_SQUARED, Z,
    predict_alpha_inverse, predict_sin2_theta_W,
    predict_omega_lambda, predict_omega_matter,
    predict_hierarchy_ratio, predict_tensor_to_scalar,
    compute_sigma_tension, validate_prediction
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ValidationResult:
    """Result of validating a Z² prediction."""
    prediction_name: str
    z2_formula: str
    z2_prediction: float
    empirical_value: float
    empirical_uncertainty: float
    empirical_source: str
    sigma_tension: float
    status: str  # VALIDATED, TENSION, FAILED
    timestamp: str
    notes: str


@dataclass
class ValidationReport:
    """Full validation report."""
    timestamp: str
    z2_constant: float
    total_predictions: int
    validated: int
    tension: int
    failed: int
    results: List[ValidationResult]
    summary: str


# ============================================================================
# Z² PREDICTIONS TO VALIDATE
# ============================================================================

Z2_PREDICTIONS = {
    "alpha_inverse": {
        "formula": "4Z² + 3",
        "compute": lambda: 4 * Z_SQUARED + 3,
        "description": "Inverse fine structure constant",
    },
    "sin2_theta_W": {
        "formula": "3/13",
        "compute": lambda: 3/13,
        "description": "Weak mixing angle (Weinberg angle)",
    },
    "Omega_Lambda": {
        "formula": "13/19",
        "compute": lambda: 13/19,
        "description": "Dark energy density parameter",
    },
    "Omega_m": {
        "formula": "6/19",
        "compute": lambda: 6/19,
        "description": "Matter density parameter",
    },
    "hierarchy_ratio": {
        "formula": "2 × Z^(43/2)",
        "compute": lambda: 2 * (Z ** 21.5),
        "description": "M_Planck / v_Higgs ratio",
    },
    "tensor_scalar_r": {
        "formula": "1/(2Z²) = 3/(64π)",
        "compute": lambda: 1 / (2 * Z_SQUARED),
        "description": "Tensor-to-scalar ratio (CMB)",
    },
}

# Known empirical values (from PDG, Planck, CODATA)
KNOWN_EMPIRICAL = {
    "alpha_inverse": {
        "value": 137.035999084,
        "uncertainty": 0.000000021,
        "source": "CODATA 2022",
    },
    "sin2_theta_W": {
        "value": 0.23121,
        "uncertainty": 0.00004,
        "source": "PDG 2024",
    },
    "Omega_Lambda": {
        "value": 0.685,
        "uncertainty": 0.007,
        "source": "Planck 2018 + BAO",
    },
    "Omega_m": {
        "value": 0.315,
        "uncertainty": 0.007,
        "source": "Planck 2018 + BAO",
    },
    "hierarchy_ratio": {
        "value": 1.220890e19 / 246.22,  # M_Pl / v
        "uncertainty": 1e14,  # ~0.1% relative
        "source": "PDG 2024",
    },
    "tensor_scalar_r": {
        "value": None,  # Not yet measured
        "uncertainty": None,
        "source": "TBD: LiteBIRD 2027-2028",
    },
}


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_single(name: str, empirical: Optional[Dict] = None) -> ValidationResult:
    """
    Validate a single Z² prediction.

    Args:
        name: Prediction name (key in Z2_PREDICTIONS)
        empirical: Optional override for empirical value

    Returns: ValidationResult
    """
    pred_info = Z2_PREDICTIONS[name]
    z2_value = pred_info["compute"]()

    # Get empirical data
    if empirical is None:
        empirical = KNOWN_EMPIRICAL.get(name, {})

    emp_value = empirical.get("value")
    emp_uncertainty = empirical.get("uncertainty")
    emp_source = empirical.get("source", "Unknown")

    # Handle missing empirical data
    if emp_value is None:
        return ValidationResult(
            prediction_name=name,
            z2_formula=pred_info["formula"],
            z2_prediction=z2_value,
            empirical_value=0,
            empirical_uncertainty=0,
            empirical_source=emp_source,
            sigma_tension=0,
            status="PENDING",
            timestamp=datetime.now().isoformat(),
            notes="No empirical measurement available yet"
        )

    # Compute tension
    sigma = compute_sigma_tension(z2_value, emp_value, emp_uncertainty)

    # Determine status
    if sigma < 2:
        status = "VALIDATED"
    elif sigma < 3:
        status = "TENSION"
    else:
        status = "FAILED"

    return ValidationResult(
        prediction_name=name,
        z2_formula=pred_info["formula"],
        z2_prediction=z2_value,
        empirical_value=emp_value,
        empirical_uncertainty=emp_uncertainty,
        empirical_source=emp_source,
        sigma_tension=sigma,
        status=status,
        timestamp=datetime.now().isoformat(),
        notes=pred_info["description"]
    )


def validate_all() -> ValidationReport:
    """
    Validate all Z² predictions against known empirical values.
    """
    results = []
    validated = 0
    tension = 0
    failed = 0
    pending = 0

    for name in Z2_PREDICTIONS:
        result = validate_single(name)
        results.append(result)

        if result.status == "VALIDATED":
            validated += 1
        elif result.status == "TENSION":
            tension += 1
        elif result.status == "FAILED":
            failed += 1
        else:
            pending += 1

    # Generate summary
    total = len(results) - pending
    if total > 0:
        success_rate = (validated / total) * 100
        summary = f"{validated}/{total} predictions validated ({success_rate:.1f}%)"
        if tension > 0:
            summary += f", {tension} in tension"
        if failed > 0:
            summary += f", {failed} FAILED"
        if pending > 0:
            summary += f", {pending} awaiting measurement"
    else:
        summary = "No predictions could be validated (no empirical data)"

    return ValidationReport(
        timestamp=datetime.now().isoformat(),
        z2_constant=Z_SQUARED,
        total_predictions=len(results),
        validated=validated,
        tension=tension,
        failed=failed,
        results=results,
        summary=summary
    )


def validate_with_extracted_data(extracted_dir: str) -> ValidationReport:
    """
    Validate Z² predictions using freshly extracted empirical data.
    """
    # Load extracted data
    extracted = {}
    extracted_path = Path(extracted_dir)

    for json_file in extracted_path.glob("*_empirical.json"):
        with open(json_file) as f:
            data = json.load(f)

        quantity = data["quantity"]
        if data["values"]:
            # Take highest-confidence value
            best = max(data["values"],
                      key=lambda x: {"high": 3, "medium": 2, "low": 1}.get(x.get("confidence", "low"), 0))
            extracted[quantity] = {
                "value": best["value"],
                "uncertainty": best.get("uncertainty", best["value"] * 0.01),
                "source": best.get("source", "arXiv extraction")
            }

    # Validate using extracted data where available
    results = []
    for name in Z2_PREDICTIONS:
        if name in extracted:
            result = validate_single(name, extracted[name])
        else:
            result = validate_single(name)
        results.append(result)

    # Generate report
    validated = sum(1 for r in results if r.status == "VALIDATED")
    tension = sum(1 for r in results if r.status == "TENSION")
    failed = sum(1 for r in results if r.status == "FAILED")

    return ValidationReport(
        timestamp=datetime.now().isoformat(),
        z2_constant=Z_SQUARED,
        total_predictions=len(results),
        validated=validated,
        tension=tension,
        failed=failed,
        results=results,
        summary=f"Validated {validated} predictions using extracted data"
    )


# ============================================================================
# OUTPUT FUNCTIONS
# ============================================================================

def save_report(report: ValidationReport, output_dir: str):
    """Save validation report to appropriate folder."""
    # Save to validated_truths or failed_attempts
    if report.failed > 0:
        folder = os.path.join(output_dir, "..", "failed_attempts")
    else:
        folder = os.path.join(output_dir, "..", "validated_truths")

    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"validation_report_{timestamp}.json"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:
        json.dump(asdict(report), f, indent=2, default=str)

    print(f"Report saved to: {filepath}")
    return filepath


def generate_markdown_report(report: ValidationReport) -> str:
    """Generate human-readable markdown report."""
    lines = [
        "# Z² Framework Validation Report",
        f"\n**Generated:** {report.timestamp}",
        f"**Z² = 32π/3 =** {report.z2_constant:.6f}",
        "",
        "## Summary",
        "",
        report.summary,
        "",
        "| Prediction | Formula | Z² | Empirical | σ | Status |",
        "|------------|---------|-----|-----------|---|--------|",
    ]

    for r in report.results:
        if r.status == "PENDING":
            lines.append(f"| {r.prediction_name} | {r.z2_formula} | {r.z2_prediction:.6g} | TBD | - | ⏳ |")
        else:
            status_emoji = {"VALIDATED": "✅", "TENSION": "⚠️", "FAILED": "❌"}.get(r.status, "?")
            lines.append(
                f"| {r.prediction_name} | {r.z2_formula} | "
                f"{r.z2_prediction:.6g} | {r.empirical_value:.6g} ± {r.empirical_uncertainty:.2g} | "
                f"{r.sigma_tension:.2f} | {status_emoji} |"
            )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- **σ < 2**: Prediction consistent with measurement (VALIDATED)",
        "- **2 ≤ σ < 3**: Tension that needs investigation",
        "- **σ ≥ 3**: Prediction inconsistent (FAILED or measurement error)",
        "",
        "---",
        "*Generated by TruthFlow - Z² Validation Pipeline*"
    ])

    return "\n".join(lines)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TRUTHFLOW ASSESSOR - Z² Validation")
    print("=" * 60)
    print(f"\nFundamental constant: Z² = 32π/3 = {Z_SQUARED:.6f}")
    print()

    # Run validation
    report = validate_all()

    # Print results
    print("-" * 60)
    print("VALIDATION RESULTS")
    print("-" * 60)

    for r in report.results:
        status_symbol = {
            "VALIDATED": "✓",
            "TENSION": "~",
            "FAILED": "✗",
            "PENDING": "?"
        }.get(r.status, "?")

        if r.status == "PENDING":
            print(f"[{status_symbol}] {r.prediction_name}: {r.z2_prediction:.6g} (awaiting measurement)")
        else:
            print(f"[{status_symbol}] {r.prediction_name}: {r.z2_prediction:.6g} vs {r.empirical_value:.6g} (σ = {r.sigma_tension:.2f})")

    print()
    print("-" * 60)
    print(f"SUMMARY: {report.summary}")
    print("-" * 60)

    # Save report
    output_dir = os.path.dirname(__file__)
    filepath = save_report(report, output_dir)

    # Generate and save markdown
    md_report = generate_markdown_report(report)
    md_path = filepath.replace(".json", ".md")
    with open(md_path, "w") as f:
        f.write(md_report)
    print(f"Markdown report: {md_path}")
