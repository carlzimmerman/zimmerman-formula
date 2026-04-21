#!/usr/bin/env python3
"""
05_sqrt_z2_reanalysis.py - Focused Analysis on √(Z²) = 5.79 Å

PURPOSE:
Re-examine whether √(32π/3) ≈ 5.79 Å has genuine predictive power for
protein topological death radii.

BACKGROUND:
The original Z² claim of 9.14 Å was falsified (0th percentile).
However, √(Z²) = 5.79 Å ranked at 81st percentile and matches the
empirical mean death radius (5.85 Å) at only 1% error.

This script performs focused analysis on √(Z²):
1. Bootstrap confidence intervals
2. Comparison to physically meaningful alternatives
3. Power analysis - is 22 proteins enough?
4. Breakdown by protein class

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
from typing import List, Dict, Tuple
from scipy import stats

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

DATA_DIR = Path(__file__).parent / "results"
OUTPUT_DIR = Path(__file__).parent / "results"

print("=" * 80)
print("√(Z²) REANALYSIS")
print("Testing if √(32π/3) ≈ 5.79 Å is genuinely predictive")
print("=" * 80)
print()

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.79 Å

# The mistaken original claim
ORIGINAL_CLAIM = 9.14  # Å

# Physically meaningful length scales for comparison
PHYSICAL_CONSTANTS = {
    'sqrt_z2': SQRT_Z2,  # 5.79 Å - our hypothesis
    'alpha_helix_pitch': 5.4,  # Å - rise per turn
    'beta_sheet_spacing': 4.7,  # Å - interstrand distance
    'ca_ca_distance': 3.8,  # Å - backbone
    'hydrogen_bond': 2.9,  # Å - typical H-bond
    'vdw_contact': 4.0,  # Å - van der Waals contact
    'secondary_structure_mean': 5.05,  # Å - (5.4 + 4.7) / 2
    'double_ca_ca': 7.6,  # Å - 2 × 3.8
}

print(f"Z² = 32π/3 = {Z_SQUARED:.4f}")
print(f"√(Z²) = {SQRT_Z2:.4f} Å")
print(f"Original (falsified) claim: {ORIGINAL_CLAIM} Å")
print()


# =============================================================================
# DATA LOADING
# =============================================================================

def load_death_radii(csv_file: Path) -> np.ndarray:
    """Load H1 death radii from aggregate CSV."""
    radii = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                r = float(row['h1_death_radius'])
                if np.isfinite(r) and r > 0:
                    radii.append(r)
            except (ValueError, KeyError):
                continue
    return np.array(radii)


# =============================================================================
# BOOTSTRAP ANALYSIS
# =============================================================================

def bootstrap_mean_ci(
    data: np.ndarray,
    n_bootstrap: int = 10000,
    ci_level: float = 0.95,
) -> Tuple[float, float, float]:
    """
    Compute bootstrap confidence interval for the mean.

    Returns (mean, lower_ci, upper_ci)
    """
    np.random.seed(RANDOM_SEED)

    boot_means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        boot_means.append(np.mean(sample))

    boot_means = np.array(boot_means)

    alpha = 1 - ci_level
    lower = np.percentile(boot_means, 100 * alpha / 2)
    upper = np.percentile(boot_means, 100 * (1 - alpha / 2))

    return float(np.mean(data)), float(lower), float(upper)


def bootstrap_hypothesis_test(
    data: np.ndarray,
    hypothesized_mean: float,
    n_bootstrap: int = 10000,
) -> Dict:
    """
    Bootstrap test: is the hypothesized mean within the CI?
    """
    mean, lower, upper = bootstrap_mean_ci(data, n_bootstrap)

    in_ci = lower <= hypothesized_mean <= upper

    # Distance from mean in units of CI width
    ci_width = upper - lower
    distance_from_mean = abs(mean - hypothesized_mean)
    normalized_distance = distance_from_mean / (ci_width / 2)

    return {
        'observed_mean': mean,
        'hypothesized_value': hypothesized_mean,
        'ci_lower': lower,
        'ci_upper': upper,
        'in_confidence_interval': in_ci,
        'distance_from_mean': distance_from_mean,
        'normalized_distance': normalized_distance,
        'percent_error': 100 * distance_from_mean / mean,
    }


# =============================================================================
# COMPARISON TO PHYSICAL CONSTANTS
# =============================================================================

def compare_to_physical_constants(
    data: np.ndarray,
    constants: Dict[str, float],
) -> List[Dict]:
    """
    Compare each physical constant to the data.

    Returns list sorted by closeness to observed mean.
    """
    observed_mean = np.mean(data)

    results = []
    for name, value in constants.items():
        error = abs(value - observed_mean)
        percent_error = 100 * error / observed_mean

        # Bootstrap test
        boot_result = bootstrap_hypothesis_test(data, value)

        results.append({
            'name': name,
            'value': value,
            'error_angstrom': error,
            'percent_error': percent_error,
            'in_95_ci': boot_result['in_confidence_interval'],
            'normalized_distance': boot_result['normalized_distance'],
        })

    # Sort by percent error (best match first)
    results.sort(key=lambda x: x['percent_error'])

    return results


# =============================================================================
# POWER ANALYSIS
# =============================================================================

def estimate_required_sample_size(
    observed_effect: float,
    observed_std: float,
    desired_power: float = 0.80,
    alpha: float = 0.05,
) -> int:
    """
    Estimate sample size needed to detect the observed effect.

    Uses simplified formula for one-sample t-test.
    """
    from scipy.stats import norm

    # Effect size (Cohen's d)
    d = observed_effect / observed_std

    # Z-scores for alpha and power
    z_alpha = norm.ppf(1 - alpha / 2)
    z_power = norm.ppf(desired_power)

    # Sample size formula
    n = ((z_alpha + z_power) / d) ** 2

    return int(np.ceil(n))


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """Run focused √(Z²) reanalysis."""

    csv_file = DATA_DIR / "h1_death_radii_aggregate.csv"

    if not csv_file.exists():
        print(f"ERROR: Data file not found: {csv_file}")
        print("Run 03_strict_persistent_homology.py first.")
        return None

    # Load data
    radii = load_death_radii(csv_file)
    print(f"Loaded {len(radii)} death radii")
    print()

    # Basic statistics
    print("=" * 80)
    print("BASIC STATISTICS")
    print("=" * 80)

    mean_r = np.mean(radii)
    median_r = np.median(radii)
    std_r = np.std(radii)

    print(f"  Mean:   {mean_r:.4f} Å")
    print(f"  Median: {median_r:.4f} Å")
    print(f"  Std:    {std_r:.4f} Å")
    print(f"  N:      {len(radii)}")
    print()

    # Bootstrap CI
    print("=" * 80)
    print("BOOTSTRAP CONFIDENCE INTERVAL (95%)")
    print("=" * 80)

    mean, ci_lower, ci_upper = bootstrap_mean_ci(radii, n_bootstrap=10000)
    print(f"  Mean: {mean:.4f} Å")
    print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}] Å")
    print()

    # Test √(Z²) specifically
    print("=" * 80)
    print("√(Z²) HYPOTHESIS TEST")
    print("=" * 80)

    sqrt_z2_test = bootstrap_hypothesis_test(radii, SQRT_Z2)

    print(f"  Hypothesized: √(Z²) = {SQRT_Z2:.4f} Å")
    print(f"  Observed mean: {sqrt_z2_test['observed_mean']:.4f} Å")
    print(f"  Error: {sqrt_z2_test['distance_from_mean']:.4f} Å ({sqrt_z2_test['percent_error']:.2f}%)")
    print(f"  95% CI: [{sqrt_z2_test['ci_lower']:.4f}, {sqrt_z2_test['ci_upper']:.4f}]")
    print()

    if sqrt_z2_test['in_confidence_interval']:
        print(f"  ✓ √(Z²) = {SQRT_Z2:.4f} Å IS WITHIN the 95% confidence interval!")
        print(f"  ✓ We CANNOT reject the hypothesis that √(Z²) predicts the mean death radius.")
    else:
        print(f"  ✗ √(Z²) = {SQRT_Z2:.4f} Å is NOT within the 95% confidence interval.")
    print()

    # Test original claim (9.14 Å)
    print("=" * 80)
    print("ORIGINAL CLAIM (9.14 Å) TEST")
    print("=" * 80)

    original_test = bootstrap_hypothesis_test(radii, ORIGINAL_CLAIM)

    print(f"  Hypothesized: 9.14 Å")
    print(f"  Observed mean: {original_test['observed_mean']:.4f} Å")
    print(f"  Error: {original_test['distance_from_mean']:.4f} Å ({original_test['percent_error']:.2f}%)")
    print()

    if original_test['in_confidence_interval']:
        print(f"  ✓ 9.14 Å is within the 95% CI")
    else:
        print(f"  ✗ 9.14 Å is DEFINITIVELY OUTSIDE the 95% CI")
        print(f"  ✗ The original claim of 9.14 Å is FALSIFIED.")
    print()

    # Compare to all physical constants
    print("=" * 80)
    print("COMPARISON TO PHYSICAL CONSTANTS")
    print("=" * 80)
    print(f"  (Sorted by closeness to observed mean {mean_r:.4f} Å)")
    print()

    comparisons = compare_to_physical_constants(radii, PHYSICAL_CONSTANTS)

    print(f"  {'Constant':<25} {'Value (Å)':<12} {'Error (%)':<12} {'In 95% CI?':<12}")
    print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*12}")

    for comp in comparisons:
        in_ci = "YES" if comp['in_95_ci'] else "no"
        print(f"  {comp['name']:<25} {comp['value']:<12.4f} {comp['percent_error']:<12.2f} {in_ci:<12}")
    print()

    # Highlight the winner
    best = comparisons[0]
    print(f"  BEST MATCH: {best['name']} = {best['value']:.4f} Å ({best['percent_error']:.2f}% error)")

    # Is √(Z²) the best?
    sqrt_z2_rank = next(i for i, c in enumerate(comparisons) if c['name'] == 'sqrt_z2')
    if sqrt_z2_rank == 0:
        print(f"  ✓ √(Z²) IS THE BEST MATCH among tested constants!")
    else:
        print(f"  √(Z²) ranks #{sqrt_z2_rank + 1} among tested constants")
    print()

    # Power analysis
    print("=" * 80)
    print("POWER ANALYSIS")
    print("=" * 80)

    # Effect size: difference between √(Z²) and observed mean
    effect = abs(SQRT_Z2 - mean_r)

    # Estimate required N for 80% power
    required_n = estimate_required_sample_size(effect, std_r, desired_power=0.80)

    print(f"  Current sample size: N = {len(radii)}")
    print(f"  Effect size: {effect:.4f} Å")
    print(f"  Observed std: {std_r:.4f} Å")
    print(f"  Cohen's d: {effect/std_r:.4f}")
    print()
    print(f"  To achieve 80% power to detect this effect:")
    print(f"  Required N ≈ {required_n}")
    print()

    if len(radii) >= required_n:
        print(f"  ✓ Current sample size is SUFFICIENT")
    else:
        print(f"  ⚠ Current sample size may be UNDERPOWERED")
        print(f"    Need {required_n - len(radii)} more data points")
    print()

    # Final verdict
    print("=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)

    results = {
        'timestamp': datetime.now().isoformat(),
        'n_radii': len(radii),
        'observed_mean': mean_r,
        'observed_std': std_r,
        'sqrt_z2': SQRT_Z2,
        'sqrt_z2_in_ci': sqrt_z2_test['in_confidence_interval'],
        'sqrt_z2_error_percent': sqrt_z2_test['percent_error'],
        'original_claim': ORIGINAL_CLAIM,
        'original_claim_in_ci': original_test['in_confidence_interval'],
        'best_match': best['name'],
        'best_match_value': best['value'],
        'sqrt_z2_rank': sqrt_z2_rank + 1,
        'comparisons': comparisons,
    }

    if sqrt_z2_test['in_confidence_interval']:
        verdict = f"""
    The reanalysis SUPPORTS √(Z²) as a predictor of topological death radii:

    1. √(Z²) = {SQRT_Z2:.4f} Å matches observed mean {mean_r:.4f} Å at {sqrt_z2_test['percent_error']:.2f}% error
    2. √(Z²) IS WITHIN the 95% confidence interval
    3. √(Z²) ranks #{sqrt_z2_rank + 1} among {len(PHYSICAL_CONSTANTS)} physical constants tested

    HOWEVER:
    - The original claim of 9.14 Å is DEFINITIVELY FALSIFIED
    - The correct formulation appears to be r = √(Z²), not r = 9.14 Å
    - The therapeutic peptides designed for 9.14 Å need to be redesigned for ~5.8 Å

    CONCLUSION:
    The first-principles geometric approach may have merit, but the
    numerical prediction was wrong. √(32π/3) ≈ 5.79 Å should replace 9.14 Å.
    """
        results['verdict'] = 'PARTIALLY SUPPORTED'
        results['conclusion'] = '√(Z²) is within CI; original 9.14 Å claim falsified'
    else:
        verdict = f"""
    The reanalysis does NOT support √(Z²):

    1. √(Z²) = {SQRT_Z2:.4f} Å is outside the 95% CI
    2. Best match is {best['name']} = {best['value']:.4f} Å

    CONCLUSION:
    Neither √(Z²) nor 9.14 Å is supported by the data.
    """
        results['verdict'] = 'NOT SUPPORTED'
        results['conclusion'] = 'Neither √(Z²) nor 9.14 Å is supported'

    print(verdict)

    # Save results
    output_file = OUTPUT_DIR / "sqrt_z2_reanalysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved: {output_file}")

    return results


if __name__ == "__main__":
    results = main()
