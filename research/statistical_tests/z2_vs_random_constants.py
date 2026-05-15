#!/usr/bin/env python3
"""
Statistical Test: Is Z² Special or Just Numerology?
====================================================

This script tests whether Z² = 32π/3 produces better matches to observed
physics constants than random mathematical constants would by chance.

The null hypothesis is: Z² is not special; similar matches could be achieved
with randomly generated constants.

Carl Zimmerman | May 2026
"""

import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import List, Tuple, Callable
import random

# Seed for reproducibility
np.random.seed(42)

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321
Z = np.sqrt(Z_SQUARED)       # = 5.788943

# =============================================================================
# OBSERVED VALUES TO MATCH
# =============================================================================

@dataclass
class ObservedValue:
    """An observed physical value to match"""
    name: str
    value: float
    uncertainty: float  # Fractional uncertainty
    description: str


OBSERVED_VALUES = [
    # 'Oumuamua acceleration ratio
    ObservedValue(
        name="a_ng/a_solar",
        value=8.26e-4,
        uncertainty=0.10,  # ~10% measurement uncertainty
        description="'Oumuamua non-gravitational acceleration ratio"
    ),
    # Velocity anomaly ratio
    ObservedValue(
        name="Δv/v_Earth",
        value=5.71e-4,
        uncertainty=0.05,  # ~5% uncertainty
        description="'Oumuamua velocity anomaly ratio"
    ),
    # Fine structure constant
    ObservedValue(
        name="α⁻¹",
        value=137.036,
        uncertainty=0.0001,  # Very precisely known
        description="Inverse fine structure constant"
    ),
    # Dark energy fraction
    ObservedValue(
        name="Ω_Λ",
        value=0.685,
        uncertainty=0.01,  # ~1% from Planck
        description="Dark energy density parameter"
    ),
    # Weak mixing angle
    ObservedValue(
        name="sin²θ_W",
        value=0.2312,
        uncertainty=0.001,  # ~0.1% precision
        description="Weak mixing angle (MS-bar)"
    ),
]


# =============================================================================
# Z² PREDICTIONS
# =============================================================================

def z2_predictions() -> dict:
    """Calculate Z² framework predictions for each observed value"""

    alpha = 1 / (4 * Z_SQUARED + 3)

    return {
        "a_ng/a_solar": 4 * alpha / Z_SQUARED,  # = 8.71e-4
        "Δv/v_Earth": Z * 1e-4,                  # = 5.79e-4
        "α⁻¹": 4 * Z_SQUARED + 3,                # = 137.04
        "Ω_Λ": 13 / 19,                          # = 0.6842
        "sin²θ_W": 3 / 13,                       # = 0.2308
    }


def calculate_match(predicted: float, observed: float) -> float:
    """Calculate match percentage (100% = perfect)"""
    if observed == 0:
        return 0
    return 100 * (1 - abs(predicted - observed) / observed)


# =============================================================================
# RANDOM CONSTANT GENERATORS
# =============================================================================

def generate_random_constant(min_val: float = 1, max_val: float = 100) -> float:
    """Generate a random constant in a reasonable range"""
    return np.random.uniform(min_val, max_val)


def generate_pi_based_constant() -> float:
    """Generate a constant involving π"""
    a = np.random.randint(1, 20)
    b = np.random.randint(1, 20)
    operations = [
        lambda a, b: a * np.pi / b,
        lambda a, b: a * np.pi * b,
        lambda a, b: a / (b * np.pi),
        lambda a, b: np.sqrt(a * np.pi / b),
        lambda a, b: (a * np.pi + b),
        lambda a, b: (a * np.pi - b) if a * np.pi > b else (b - a * np.pi),
    ]
    return random.choice(operations)(a, b)


def generate_integer_fraction() -> float:
    """Generate a simple integer fraction"""
    a = np.random.randint(1, 30)
    b = np.random.randint(1, 30)
    return a / b


# =============================================================================
# FORMULA GENERATORS FOR MATCHING
# =============================================================================

def generate_random_formula_for_target(target: float, X: float) -> Tuple[float, str]:
    """
    Try to generate a formula involving constant X that matches target.
    Returns (predicted_value, formula_string)
    """
    formulas = [
        (X, "X"),
        (1/X, "1/X"),
        (X**2, "X²"),
        (np.sqrt(X), "√X"),
        (X/np.pi, "X/π"),
        (X*np.pi, "X×π"),
        (4*X, "4X"),
        (X/4, "X/4"),
        (X + 3, "X+3"),
        (X - 3, "X-3"),
        (4*X + 3, "4X+3"),
        (X * 1e-4, "X×10⁻⁴"),
        (X**2 * 1e-4, "X²×10⁻⁴"),
        (1/(4*X**2 + 3) * 4 / X**2, "4α/X² where α⁻¹=4X²+3"),
        (3/13, "3/13"),  # Fixed fraction
        (13/19, "13/19"),  # Fixed fraction
    ]

    best_match = -1000
    best_formula = ""
    best_value = 0

    for value, formula in formulas:
        if value > 0 and np.isfinite(value):
            match = calculate_match(value, target)
            if match > best_match:
                best_match = match
                best_formula = formula
                best_value = value

    return best_value, best_formula, best_match


# =============================================================================
# MONTE CARLO TEST
# =============================================================================

def monte_carlo_test(n_trials: int = 10000) -> dict:
    """
    Test whether random constants can match observed values as well as Z².

    For each observed value, we:
    1. Calculate Z²'s match percentage
    2. Generate n_trials random constants
    3. Find the best formula for each random constant
    4. Count how many random constants beat Z²
    5. Calculate p-value
    """

    z2_preds = z2_predictions()
    results = {}

    print("=" * 70)
    print("MONTE CARLO TEST: Z² vs RANDOM CONSTANTS")
    print("=" * 70)
    print(f"\nNumber of trials: {n_trials:,}")
    print(f"Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"Z = √(Z²) = {Z:.6f}")

    for obs in OBSERVED_VALUES:
        print(f"\n{'─' * 70}")
        print(f"Testing: {obs.name} = {obs.value}")
        print(f"{'─' * 70}")

        # Z² prediction and match
        z2_pred = z2_preds[obs.name]
        z2_match = calculate_match(z2_pred, obs.value)

        print(f"  Z² prediction: {z2_pred:.6e}")
        print(f"  Z² match: {z2_match:.2f}%")

        # Test random constants
        beats_z2 = 0
        best_random_match = -1000
        best_random_constant = 0
        best_random_formula = ""

        all_matches = []

        for _ in range(n_trials):
            # Generate random constant
            X = generate_pi_based_constant()

            # Find best formula
            _, formula, match = generate_random_formula_for_target(obs.value, X)
            all_matches.append(match)

            if match >= z2_match:
                beats_z2 += 1

            if match > best_random_match:
                best_random_match = match
                best_random_constant = X
                best_random_formula = formula

        # Calculate p-value
        p_value = beats_z2 / n_trials

        # Statistics
        mean_match = np.mean(all_matches)
        std_match = np.std(all_matches)
        percentile_z2 = stats.percentileofscore(all_matches, z2_match)

        print(f"\n  Random constant results:")
        print(f"    Mean match: {mean_match:.2f}% ± {std_match:.2f}%")
        print(f"    Best random: {best_random_match:.2f}% (X={best_random_constant:.4f}, {best_random_formula})")
        print(f"    Z² percentile: {percentile_z2:.1f}%")
        print(f"    p-value (random ≥ Z²): {p_value:.4f}")

        if p_value < 0.05:
            print(f"    ★ Z² is SIGNIFICANTLY better than random (p < 0.05)")
        elif p_value < 0.10:
            print(f"    ◆ Z² is marginally better than random (p < 0.10)")
        else:
            print(f"    ✗ Z² is NOT significantly better than random")

        results[obs.name] = {
            "z2_match": z2_match,
            "p_value": p_value,
            "percentile": percentile_z2,
            "mean_random": mean_match,
            "std_random": std_match,
            "best_random": best_random_match,
            "significant": p_value < 0.05
        }

    return results


def combined_significance_test(results: dict) -> float:
    """
    Calculate combined p-value using Fisher's method.
    Tests whether Z² is special across ALL predictions.
    """

    print("\n" + "=" * 70)
    print("COMBINED SIGNIFICANCE TEST (Fisher's Method)")
    print("=" * 70)

    p_values = [r["p_value"] for r in results.values() if r["p_value"] > 0]

    # Fisher's method: χ² = -2 Σ ln(p_i)
    chi2_stat = -2 * sum(np.log(p) for p in p_values)
    df = 2 * len(p_values)
    combined_p = 1 - stats.chi2.cdf(chi2_stat, df)

    print(f"\nIndividual p-values: {[f'{p:.4f}' for p in p_values]}")
    print(f"χ² statistic: {chi2_stat:.2f}")
    print(f"Degrees of freedom: {df}")
    print(f"Combined p-value: {combined_p:.6f}")

    if combined_p < 0.001:
        print("\n★★★ HIGHLY SIGNIFICANT: Z² is very unlikely to be random (p < 0.001)")
    elif combined_p < 0.01:
        print("\n★★ SIGNIFICANT: Z² is unlikely to be random (p < 0.01)")
    elif combined_p < 0.05:
        print("\n★ MARGINALLY SIGNIFICANT: Z² might not be random (p < 0.05)")
    else:
        print("\n✗ NOT SIGNIFICANT: Z² could easily be random (p ≥ 0.05)")

    return combined_p


def check_for_overfitting():
    """
    Check whether we're overfitting by having too many free formula choices.
    """

    print("\n" + "=" * 70)
    print("OVERFITTING CHECK")
    print("=" * 70)

    print("""
    WARNING: The Z² framework uses multiple formula types:

    For α⁻¹:      4Z² + 3          (3 free parameters: coefficient 4, constant 3, Z²)
    For Ω_Λ:      13/19            (2 free parameters: 13, 19) - NOT Z² dependent!
    For sin²θ_W:  3/13             (2 free parameters: 3, 13) - NOT Z² dependent!
    For a_ng:     4α/Z²            (uses α which depends on Z²)
    For Δv:       Z × 10⁻⁴         (1 free parameter: 10⁻⁴)

    CRITICAL OBSERVATION:
    - Ω_Λ = 13/19 and sin²θ_W = 3/13 don't actually use Z² at all!
    - They use the numbers 13 and 19 which appear in the "19 degrees of freedom"
    - But 13 and 19 are INDEPENDENTLY chosen to fit the data

    This is a form of overfitting: we have enough free parameters
    (Z², plus integers 3, 4, 13, 19) to fit multiple targets.

    A truly predictive framework would derive 13/19 FROM Z², not state it separately.
    """)

    # Calculate degrees of freedom vs. data points
    n_data = 5  # Number of values we're trying to match
    n_params = 5  # Z², plus the integers 3, 4, 13, 19

    print(f"Data points being fit: {n_data}")
    print(f"Approximate free parameters: {n_params}")
    print(f"Effective degrees of freedom: {n_data - n_params}")

    if n_params >= n_data:
        print("\n⚠ WARNING: More parameters than data points = OVERFITTING RISK")


def test_specific_claims():
    """
    Test specific Z² claims individually with focused analysis.
    """

    print("\n" + "=" * 70)
    print("INDIVIDUAL CLAIM ANALYSIS")
    print("=" * 70)

    claims = [
        {
            "name": "Fine structure constant",
            "formula": "α⁻¹ = 4Z² + 3",
            "predicted": 4 * Z_SQUARED + 3,
            "observed": 137.035999084,
            "precision": "±0.000000021"
        },
        {
            "name": "Acceleration ratio",
            "formula": "a_ng/a_solar = 4α/Z²",
            "predicted": 4 * (1/(4*Z_SQUARED+3)) / Z_SQUARED,
            "observed": 8.26e-4,
            "precision": "±10%"
        },
        {
            "name": "Velocity anomaly",
            "formula": "Δv/v_Earth = Z × 10⁻⁴",
            "predicted": Z * 1e-4,
            "observed": 5.71e-4,
            "precision": "±5%"
        },
        {
            "name": "Dark energy",
            "formula": "Ω_Λ = 13/19",
            "predicted": 13/19,
            "observed": 0.685,
            "precision": "±1%"
        },
        {
            "name": "Weak mixing angle",
            "formula": "sin²θ_W = 3/13",
            "predicted": 3/13,
            "observed": 0.2312,
            "precision": "±0.1%"
        },
    ]

    for claim in claims:
        match = calculate_match(claim["predicted"], claim["observed"])
        residual = claim["predicted"] - claim["observed"]
        sigma = abs(residual) / (claim["observed"] * 0.01)  # Assuming 1% as baseline

        print(f"\n{claim['name']}:")
        print(f"  Formula: {claim['formula']}")
        print(f"  Predicted: {claim['predicted']:.6f}")
        print(f"  Observed: {claim['observed']:.6f} {claim['precision']}")
        print(f"  Match: {match:.2f}%")
        print(f"  Residual: {residual:+.6f}")

        # Is it a Z²-derived prediction or an independent fit?
        if "Z" in claim["formula"]:
            print(f"  Status: Uses Z² ✓")
        else:
            print(f"  Status: DOES NOT USE Z² (independent fraction)")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("Z² STATISTICAL SIGNIFICANCE TEST")
    print("=" * 70)
    print("""
    Purpose: Determine whether Z² = 32π/3 produces significantly better
    matches to observed physics constants than random constants.

    Null hypothesis: Z² is not special; random constants do equally well.
    Alternative: Z² produces systematically better predictions.
    """)

    # Run Monte Carlo test
    results = monte_carlo_test(n_trials=10000)

    # Combined significance
    combined_p = combined_significance_test(results)

    # Check for overfitting
    check_for_overfitting()

    # Analyze specific claims
    test_specific_claims()

    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    significant_count = sum(1 for r in results.values() if r["significant"])

    print(f"\nResults:")
    print(f"  Predictions tested: {len(results)}")
    print(f"  Statistically significant (p<0.05): {significant_count}")
    print(f"  Combined p-value: {combined_p:.6f}")

    print("\nConclusion:")
    if combined_p < 0.01 and significant_count >= 3:
        print("  Z² appears to be genuinely predictive for multiple phenomena.")
        print("  The matches are unlikely to be coincidental.")
    elif combined_p < 0.05:
        print("  Z² shows some evidence of being special, but not overwhelming.")
        print("  More data is needed to confirm or refute.")
    else:
        print("  Z² does NOT show statistically significant predictive power.")
        print("  The observed matches could easily arise by chance with random constants.")

    print("""

    CRITICAL CAVEAT:
    This test assumes the Z² formulas were chosen BEFORE seeing the data.
    If formulas were adjusted to fit the data (post hoc), the true p-values
    are much higher (less significant) than calculated here.

    The strongest evidence for Z² would be:
    1. Predictions made BEFORE observations (e.g., for 4I, 5I)
    2. Deriving all formulas from FIRST PRINCIPLES, not fitting
    3. No cherry-picking of which constants to predict
    """)


if __name__ == "__main__":
    main()
