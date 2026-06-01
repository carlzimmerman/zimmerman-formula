#!/usr/bin/env python3
"""
Z² Framework Empirical Validation Engine
=========================================

A rigorous computational pipeline for validating the Z² unified framework
against 100 empirical physics targets.

Features:
- Exact sigma tension calculations with asymmetric errors
- Bayesian tier weighting system
- Cryptographic hash verification
- Color-coded terminal output
- Automated report generation

Author: Z² Framework Team
Date: May 2, 2026
Version: 1.0.0
"""

import json
import math
import hashlib
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum
import os

# =============================================================================
# ANSI Color Codes for Terminal
# =============================================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# =============================================================================
# Z² Framework Constants
# =============================================================================

Z_SQUARED = 32 * math.pi / 3  # 33.510321638291124
Z = math.sqrt(Z_SQUARED)       # 5.788810036466141

# Physical constants
C = 2.998e8  # m/s
MPC_TO_M = 3.086e22  # meters per Megaparsec

# Derived predictions
OMEGA_LAMBDA = 13 / 19  # 0.6842105263157895
OMEGA_M = 6 / 19        # 0.3157894736842105
SIN2_THETA_W = 3 / 13   # 0.23076923076923078
ALPHA_INV = 4 * Z_SQUARED + 3  # 137.04128655316451
H0_PREDICTED = 71.5     # km/s/Mpc
A0_PREDICTED = C * (H0_PREDICTED * 1000 / MPC_TO_M) / Z  # 1.1999e-10 m/s²

# =============================================================================
# Data Classes
# =============================================================================

class TensionLevel(Enum):
    EXCELLENT = "excellent"      # < 1σ
    GOOD = "good"               # 1-2σ
    MILD_TENSION = "mild"       # 2-3σ
    SIGNIFICANT = "significant"  # 3-5σ
    CRITICAL = "critical"        # > 5σ
    FUTURE = "future"           # No data yet
    NO_PREDICTION = "no_pred"   # Z² makes no prediction

@dataclass
class ValidationResult:
    target_id: int
    experiment: str
    parameter: str
    category: str
    observed: Optional[float]
    predicted: Optional[float]
    sigma_tension: Optional[float]
    percent_error: Optional[float]
    tension_level: TensionLevel
    tier: int
    weight: int
    weighted_score: float
    notes: str

# =============================================================================
# Sigma Calculator with Asymmetric Errors
# =============================================================================

def calculate_sigma(observed: float, predicted: float,
                   err_plus: float, err_minus: float) -> Tuple[float, float]:
    """
    Calculate sigma tension with proper asymmetric error handling.

    Returns: (sigma_tension, percent_error)
    """
    if observed is None or predicted is None:
        return (None, None)

    if err_plus is None or err_minus is None:
        return (None, None)

    diff = predicted - observed

    # Use appropriate error based on direction
    if diff > 0:
        # Prediction is higher than observation
        sigma = abs(diff) / err_plus if err_plus > 0 else float('inf')
    else:
        # Prediction is lower than observation
        sigma = abs(diff) / err_minus if err_minus > 0 else float('inf')

    # Percent error
    if observed != 0:
        percent = 100 * abs(diff) / abs(observed)
    else:
        percent = 0 if predicted == 0 else float('inf')

    return (sigma, percent)

def classify_tension(sigma: Optional[float], has_prediction: bool,
                    is_future: bool) -> TensionLevel:
    """Classify tension level based on sigma value."""
    if is_future:
        return TensionLevel.FUTURE
    if not has_prediction:
        return TensionLevel.NO_PREDICTION
    if sigma is None:
        return TensionLevel.NO_PREDICTION

    if sigma < 1.0:
        return TensionLevel.EXCELLENT
    elif sigma < 2.0:
        return TensionLevel.GOOD
    elif sigma < 3.0:
        return TensionLevel.MILD_TENSION
    elif sigma < 5.0:
        return TensionLevel.SIGNIFICANT
    else:
        return TensionLevel.CRITICAL

# =============================================================================
# Bayesian Weighting System
# =============================================================================

def calculate_weighted_score(sigma: Optional[float], weight: int,
                            tension_level: TensionLevel) -> float:
    """
    Calculate weighted score for Bayesian assessment.

    Scoring:
    - Excellent (<1σ): +1.0 × weight
    - Good (1-2σ): +0.8 × weight
    - Mild (2-3σ): +0.5 × weight
    - Significant (3-5σ): -0.5 × weight
    - Critical (>5σ): -1.0 × weight
    - Future/No Prediction: 0
    """
    if tension_level in [TensionLevel.FUTURE, TensionLevel.NO_PREDICTION]:
        return 0.0

    if tension_level == TensionLevel.EXCELLENT:
        return 1.0 * weight
    elif tension_level == TensionLevel.GOOD:
        return 0.8 * weight
    elif tension_level == TensionLevel.MILD_TENSION:
        return 0.5 * weight
    elif tension_level == TensionLevel.SIGNIFICANT:
        return -0.5 * weight
    elif tension_level == TensionLevel.CRITICAL:
        return -1.0 * weight
    return 0.0

# =============================================================================
# Main Validation Engine
# =============================================================================

class Z2ValidationEngine:
    def __init__(self, targets_file: str):
        """Initialize engine with targets JSON file."""
        with open(targets_file, 'r') as f:
            data = json.load(f)

        self.metadata = data['metadata']
        self.targets = data['targets']
        self.results: List[ValidationResult] = []

    def validate_all(self) -> List[ValidationResult]:
        """Run validation on all targets."""
        self.results = []

        for target in self.targets:
            result = self._validate_target(target)
            self.results.append(result)

        return self.results

    def _validate_target(self, target: dict) -> ValidationResult:
        """Validate a single target."""
        target_id = target['target_id']
        experiment = target['experiment']
        parameter = target['parameter']
        category = target['category']
        observed = target.get('observed_value')
        predicted = target.get('z2_predicted_value')
        err_plus = target.get('uncertainty_plus')
        err_minus = target.get('uncertainty_minus')
        tier = target.get('tier', 3)
        weight = target.get('weight', 1)
        notes = target.get('notes', '')
        is_future = target.get('status') == 'future'
        has_prediction = predicted is not None

        # Handle null results (DM searches)
        if observed == 0.0 and predicted == 0.0:
            sigma = 0.0
            percent = 0.0
        else:
            sigma, percent = calculate_sigma(observed, predicted,
                                            err_plus or 0, err_minus or 0)

        tension = classify_tension(sigma, has_prediction, is_future)
        weighted = calculate_weighted_score(sigma, weight, tension)

        return ValidationResult(
            target_id=target_id,
            experiment=experiment,
            parameter=parameter,
            category=category,
            observed=observed,
            predicted=predicted,
            sigma_tension=sigma,
            percent_error=percent,
            tension_level=tension,
            tier=tier,
            weight=weight,
            weighted_score=weighted,
            notes=notes
        )

    def print_results(self):
        """Print color-coded results to terminal."""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}Z² FRAMEWORK EMPIRICAL VALIDATION ENGINE{Colors.END}")
        print(f"{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"\nZ² = 32π/3 = {Z_SQUARED:.10f}")
        print(f"Z  = √(32π/3) = {Z:.10f}")
        print(f"\n{Colors.BOLD}Processing {len(self.targets)} targets...{Colors.END}\n")

        # Group by category
        categories = {}
        for r in self.results:
            if r.category not in categories:
                categories[r.category] = []
            categories[r.category].append(r)

        for cat, results in categories.items():
            print(f"\n{Colors.CYAN}{Colors.BOLD}=== {cat.upper()} ==={Colors.END}")
            print(f"{'ID':<4} {'Experiment':<25} {'σ':<8} {'%Err':<10} {'Status':<15} {'Weight':<8}")
            print("-" * 75)

            for r in results:
                color = self._get_color(r.tension_level)
                sigma_str = f"{r.sigma_tension:.2f}" if r.sigma_tension is not None else "N/A"
                pct_str = f"{r.percent_error:.4f}" if r.percent_error is not None else "N/A"
                status = r.tension_level.value.upper()

                print(f"{color}{r.target_id:<4} {r.experiment[:25]:<25} {sigma_str:<8} {pct_str:<10} {status:<15} {r.weight:<8}{Colors.END}")

    def _get_color(self, level: TensionLevel) -> str:
        """Get ANSI color for tension level."""
        if level == TensionLevel.EXCELLENT:
            return Colors.GREEN
        elif level == TensionLevel.GOOD:
            return Colors.GREEN
        elif level == TensionLevel.MILD_TENSION:
            return Colors.YELLOW
        elif level == TensionLevel.SIGNIFICANT:
            return Colors.YELLOW
        elif level == TensionLevel.CRITICAL:
            return Colors.RED
        elif level == TensionLevel.FUTURE:
            return Colors.CYAN
        return Colors.WHITE

    def compute_bayesian_score(self) -> Dict:
        """Compute overall Bayesian assessment."""
        total_weighted = sum(r.weighted_score for r in self.results)
        max_possible = sum(r.weight for r in self.results
                         if r.tension_level not in [TensionLevel.FUTURE, TensionLevel.NO_PREDICTION])

        # Count by tier
        tier_scores = {1: 0, 2: 0, 3: 0}
        tier_max = {1: 0, 2: 0, 3: 0}

        for r in self.results:
            if r.tension_level not in [TensionLevel.FUTURE, TensionLevel.NO_PREDICTION]:
                tier_scores[r.tier] = tier_scores.get(r.tier, 0) + r.weighted_score
                tier_max[r.tier] = tier_max.get(r.tier, 0) + r.weight

        # Count by status
        status_counts = {}
        for r in self.results:
            level = r.tension_level.value
            status_counts[level] = status_counts.get(level, 0) + 1

        return {
            'total_weighted_score': total_weighted,
            'max_possible_score': max_possible,
            'percentage': 100 * total_weighted / max_possible if max_possible > 0 else 0,
            'tier_scores': tier_scores,
            'tier_max': tier_max,
            'status_counts': status_counts,
            'total_targets': len(self.results)
        }

    def generate_report(self, output_path: str):
        """Generate markdown validation report."""
        bayes = self.compute_bayesian_score()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Compute hash of results for integrity
        results_str = json.dumps([{
            'id': r.target_id,
            'sigma': r.sigma_tension,
            'score': r.weighted_score
        } for r in self.results], sort_keys=True)
        result_hash = hashlib.sha256(results_str.encode()).hexdigest()[:16]

        report = f"""# Z² Framework Computational Validation Report

**Generated:** {timestamp}
**Integrity Hash:** `{result_hash}`
**Framework Version:** 7.0.0

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Targets | {bayes['total_targets']} |
| Weighted Score | {bayes['total_weighted_score']:.1f} / {bayes['max_possible_score']:.1f} |
| **Framework Validity** | **{bayes['percentage']:.1f}%** |

## Tension Distribution

| Level | Count | Description |
|-------|-------|-------------|
| Excellent (<1σ) | {bayes['status_counts'].get('excellent', 0)} | Perfect match |
| Good (1-2σ) | {bayes['status_counts'].get('good', 0)} | Strong confirmation |
| Mild (2-3σ) | {bayes['status_counts'].get('mild', 0)} | Minor tension |
| Significant (3-5σ) | {bayes['status_counts'].get('significant', 0)} | Notable tension |
| Critical (>5σ) | {bayes['status_counts'].get('critical', 0)} | **Potential falsifier** |
| Future Test | {bayes['status_counts'].get('future', 0)} | Awaiting data |
| No Prediction | {bayes['status_counts'].get('no_pred', 0)} | N/A |

## Tier Analysis (Bayesian Weighting)

| Tier | Description | Score | Max | Percentage |
|------|-------------|-------|-----|------------|
| 1 | Fundamental (×100) | {bayes['tier_scores'].get(1, 0):.0f} | {bayes['tier_max'].get(1, 0)} | {100*bayes['tier_scores'].get(1,0)/bayes['tier_max'].get(1,1):.1f}% |
| 2 | Clean Dynamics (×10) | {bayes['tier_scores'].get(2, 0):.0f} | {bayes['tier_max'].get(2, 0)} | {100*bayes['tier_scores'].get(2,0)/bayes['tier_max'].get(2,1):.1f}% |
| 3 | Messy Astrophysics (×1) | {bayes['tier_scores'].get(3, 0):.0f} | {bayes['tier_max'].get(3, 0)} | {100*bayes['tier_scores'].get(3,0)/max(bayes['tier_max'].get(3,1),1):.1f}% |

---

## Detailed Results by Category

"""
        # Add detailed results
        categories = {}
        for r in self.results:
            if r.category not in categories:
                categories[r.category] = []
            categories[r.category].append(r)

        for cat, results in sorted(categories.items()):
            report += f"\n### {cat.replace('_', ' ').title()}\n\n"
            report += "| ID | Experiment | σ | % Error | Status | Tier |\n"
            report += "|----|-----------|----|---------|--------|------|\n"

            for r in results:
                sigma_str = f"{r.sigma_tension:.2f}" if r.sigma_tension is not None else "N/A"
                pct_str = f"{r.percent_error:.4f}" if r.percent_error is not None else "N/A"
                status = r.tension_level.value
                status_icon = self._get_icon(r.tension_level)

                report += f"| {r.target_id} | {r.experiment} | {sigma_str} | {pct_str}% | {status_icon} {status} | {r.tier} |\n"

        # Critical tensions section
        critical = [r for r in self.results if r.tension_level == TensionLevel.CRITICAL]
        if critical:
            report += "\n---\n\n## CRITICAL TENSIONS (Potential Falsifiers)\n\n"
            for r in critical:
                report += f"- **Target {r.target_id}: {r.experiment}** - {r.sigma_tension:.1f}σ tension\n"
                report += f"  - Observed: {r.observed}\n"
                report += f"  - Predicted: {r.predicted}\n"
                report += f"  - Note: {r.notes}\n\n"

        # Future tests section
        future = [r for r in self.results if r.tension_level == TensionLevel.FUTURE]
        if future:
            report += "\n---\n\n## FUTURE TESTS (Flags Planted)\n\n"
            for r in future:
                report += f"- **Target {r.target_id}: {r.experiment}**\n"
                report += f"  - Z² Predicts: {r.predicted}\n"
                report += f"  - Note: {r.notes}\n\n"

        report += f"""
---

## Cryptographic Verification

This report's integrity can be verified using the hash:

```
SHA256: {result_hash}
```

Computed from the sorted JSON of all (target_id, sigma_tension, weighted_score) tuples.

---

## Conclusion

The Z² framework achieves a **{bayes['percentage']:.1f}% weighted validation score** across {bayes['total_targets']} empirical targets.

- **Tier 1 (Fundamental):** {100*bayes['tier_scores'].get(1,0)/bayes['tier_max'].get(1,1):.0f}% success rate
- **Critical Tensions:** {bayes['status_counts'].get('critical', 0)} targets require investigation
- **Future Tests:** {bayes['status_counts'].get('future', 0)} predictions await experimental data

---

*Generated by Z² Empirical Validation Engine v1.0.0*
*{timestamp}*
"""

        with open(output_path, 'w') as f:
            f.write(report)

        print(f"\n{Colors.GREEN}Report generated: {output_path}{Colors.END}")
        print(f"Integrity hash: {result_hash}")

        return result_hash

    def _get_icon(self, level: TensionLevel) -> str:
        """Get status icon for markdown."""
        icons = {
            TensionLevel.EXCELLENT: "✅",
            TensionLevel.GOOD: "✅",
            TensionLevel.MILD_TENSION: "⚠️",
            TensionLevel.SIGNIFICANT: "⚠️",
            TensionLevel.CRITICAL: "❌",
            TensionLevel.FUTURE: "⏳",
            TensionLevel.NO_PREDICTION: "➖"
        }
        return icons.get(level, "")

    def export_json(self, output_path: str):
        """Export results to JSON for further analysis."""
        output = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'framework_version': '7.0.0',
                'Z_squared': Z_SQUARED,
                'Z': Z
            },
            'bayesian_assessment': self.compute_bayesian_score(),
            'results': [{
                'target_id': r.target_id,
                'experiment': r.experiment,
                'parameter': r.parameter,
                'category': r.category,
                'observed': r.observed,
                'predicted': r.predicted,
                'sigma_tension': r.sigma_tension,
                'percent_error': r.percent_error,
                'tension_level': r.tension_level.value,
                'tier': r.tier,
                'weight': r.weight,
                'weighted_score': r.weighted_score,
                'notes': r.notes
            } for r in self.results]
        }

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"{Colors.GREEN}JSON exported: {output_path}{Colors.END}")

# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Z² Framework Empirical Validation Engine'
    )
    parser.add_argument(
        '--targets', '-t',
        default='targets.json',
        help='Path to targets JSON file'
    )
    parser.add_argument(
        '--output', '-o',
        default='COMPUTATIONAL_VALIDATION_LEDGER.md',
        help='Output report path'
    )
    parser.add_argument(
        '--json', '-j',
        default='validation_results.json',
        help='JSON output path'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress terminal output'
    )

    args = parser.parse_args()

    # Find targets file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    targets_path = os.path.join(script_dir, args.targets)

    if not os.path.exists(targets_path):
        print(f"{Colors.RED}Error: targets file not found: {targets_path}{Colors.END}")
        return 1

    # Run validation
    engine = Z2ValidationEngine(targets_path)
    engine.validate_all()

    if not args.quiet:
        engine.print_results()

        # Print Bayesian summary
        bayes = engine.compute_bayesian_score()
        print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}BAYESIAN ASSESSMENT{Colors.END}")
        print(f"{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"\nTotal Weighted Score: {bayes['total_weighted_score']:.1f} / {bayes['max_possible_score']:.1f}")
        print(f"Framework Validity: {Colors.BOLD}{bayes['percentage']:.1f}%{Colors.END}")
        print(f"\nStatus Distribution:")
        for status, count in sorted(bayes['status_counts'].items()):
            print(f"  {status}: {count}")

    # Generate outputs
    report_path = os.path.join(script_dir, args.output)
    json_path = os.path.join(script_dir, args.json)

    engine.generate_report(report_path)
    engine.export_json(json_path)

    return 0

if __name__ == '__main__':
    exit(main())
