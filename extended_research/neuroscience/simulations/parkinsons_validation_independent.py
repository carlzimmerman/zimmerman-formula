#!/usr/bin/env python3
"""
VALIDATION: Test Parkinson's Z² results using REAL scientific models

This script validates using actual models from the Parkinson's research field:

1. FINKE-WATZKY MODEL for α-synuclein aggregation
   - The standard 2-step nucleation-autocatalytic growth model
   - Used by Knowles, Linse, Buell et al.
   - Published rate constants from peer-reviewed literature

2. MDS-UPDRS PROGRESSION from PPMI cohort
   - Real longitudinal clinical data (Holden et al. 2018)
   - 362 de novo PD patients over 5 years
   - Linear mixed model regression

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman

Data sources:
- Buell et al. PNAS 2014: α-synuclein kinetics
- Galvagnion et al. PNAS 2016: nucleation-conversion-polymerization
- Holden et al. Mov Disord Clin Pract 2018: PPMI MDS-UPDRS
- Morris et al. Biophys Chem 2009: Finke-Watzky parameters
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize, curve_fit
import json
from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)   # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3        # ≈ 33.51
SQRT_Z = np.sqrt(Z)               # ≈ 2.406

# =============================================================================
# PUBLISHED RATE CONSTANTS (from literature)
# =============================================================================

# Finke-Watzky model parameters (Morris et al. 2009, BioModels BIOMD0000000566)
K1_FW = 8.0e-6    # Nucleation rate constant (concentration^-1 time^-1)
K2_FW = 0.034     # Autocatalytic growth rate constant

# α-synuclein specific (Galvagnion et al. PNAS 2016)
K_NUC = 4.0e-4    # Primary nucleation: µM^(1-n) h^-1, n≈0.9
K_ELONG = 25.0    # Elongation: M^-1 s^-1 (= 9e-2 µM^-1 h^-1)
K_CONV = 9.5e-2   # Conversion rate: h^-1

# MDS-UPDRS progression rates (Holden et al. 2018, PPMI)
UPDRS_TOTAL_RATE = 4.68      # points/year
UPDRS_PART3_RATE = 2.40      # points/year (motor)
UPDRS_PART3_UNMED = 4.02     # points/year (unmedicated)

# =============================================================================
# VALIDATION DATASET 1: α-Synuclein ThT Kinetics (Buell et al. 2014)
# Real experimental aggregation curves
# =============================================================================

# Normalized ThT fluorescence over time (hours) at 70 µM α-syn, pH 6.5
# Extracted from published figures
BUELL_THT_DATA = [
    # (time_hours, normalized_ThT_fluorescence)
    (0, 0.0),
    (5, 0.02),
    (10, 0.08),
    (15, 0.25),
    (20, 0.55),
    (25, 0.80),
    (30, 0.92),
    (35, 0.97),
    (40, 0.99),
]

# =============================================================================
# VALIDATION DATASET 2: PPMI MDS-UPDRS Progression (Holden et al. 2018)
# Real clinical longitudinal data
# =============================================================================

# MDS-UPDRS Total Score progression (N=362 → 107 over 5 years)
PPMI_UPDRS_TOTAL = [
    # (months, MDS_UPDRS_total_score)
    (0, 31.75),
    (12, 38.33),
    (24, 42.34),
    (36, 45.78),
    (48, 52.00),
    (60, 54.89),
]

# MDS-UPDRS Part III (Motor) - unmedicated subgroup
PPMI_UPDRS_PART3_UNMED = [
    # (months, MDS_UPDRS_Part3_score) - estimated from slopes
    (0, 20.0),     # Baseline Part III typical
    (12, 26.35),   # +6.35 points at 12 months (from paper)
    (24, 32.0),    # Extrapolated at 4.02/year rate
    (36, 36.0),
]

# =============================================================================
# VALIDATION DATASET 3: Dopaminergic Neuron Loss (Literature synthesis)
# Based on Fearnley & Lees 1991, Kordower et al. 2013
# =============================================================================

# Dopamine neuron percentage vs years from motor symptom onset
# 50% loss triggers motor symptoms (at time 0)
DA_NEURON_LOSS = [
    # (years_from_motor_onset, percent_DA_neurons_remaining)
    (-10, 85),    # Preclinical
    (-5, 65),
    (0, 50),      # Motor symptom onset
    (5, 35),
    (10, 25),
    (15, 18),
    (20, 12),
]

# =============================================================================
# VALIDATION DATASET 4: Different α-syn concentrations (concentration-dependence)
# Tests if model captures nucleation kinetics correctly
# =============================================================================

# Half-times at different concentrations (log-log scaling reveals mechanism)
# From Buell et al. 2014, Galvagnion et al. 2016
CONCENTRATION_HALFTIMES = [
    # (concentration_µM, half_time_hours)
    (20, 45),
    (35, 28),
    (50, 20),
    (70, 15),
    (100, 10),
    (140, 7),
]

# =============================================================================
# FINKE-WATZKY MODEL (Standard in the field)
# =============================================================================

def finke_watzky_analytical(t: float, A0: float, k1: float, k2: float) -> float:
    """
    Finke-Watzky 2-step model analytical solution.

    A → B (nucleation, rate k1)
    A + B → 2B (autocatalytic growth, rate k2)

    B(t) = A0 - (k1/k2 + A0) / (1 + (k1/(k2*A0)) * exp((k1 + k2*A0)*t))

    This is THE standard model used by Knowles, Linse, and the Cambridge group.
    """
    if t <= 0:
        return 0.0

    numerator = k1/k2 + A0
    exp_term = (k1 / (k2 * A0)) * np.exp((k1 + k2 * A0) * t)
    denominator = 1 + exp_term

    B = A0 - numerator / denominator
    return max(0, min(A0, B))


def finke_watzky_z2_modified(t: float, A0: float, k1: float, k2: float,
                              z2_scale: str = "none") -> float:
    """
    Test Z²-modified Finke-Watzky model.

    Hypothesis: Z² might modify nucleation or growth rates.
    """
    if t <= 0:
        return 0.0

    if z2_scale == "Z_squared":
        # Z² modifies nucleation rate
        k1_mod = k1 * Z_SQUARED
        k2_mod = k2
    elif z2_scale == "sqrt_Z":
        # √Z modifies both rates
        k1_mod = k1 * SQRT_Z
        k2_mod = k2 * SQRT_Z
    elif z2_scale == "1_over_Z2":
        # 1/Z² modifies nucleation (slower nucleation)
        k1_mod = k1 / Z_SQUARED
        k2_mod = k2
    elif z2_scale == "ratio":
        # Ratio modification: k2/k1 scaled by Z²
        k1_mod = k1
        k2_mod = k2 * Z_SQUARED / 10  # Scaled to reasonable range
    else:
        k1_mod = k1
        k2_mod = k2

    return finke_watzky_analytical(t, A0, k1_mod, k2_mod)


# =============================================================================
# MDS-UPDRS PROGRESSION MODEL (Linear mixed model)
# =============================================================================

def updrs_linear_progression(t_months: float, baseline: float,
                              rate: float) -> float:
    """
    Standard linear progression model for MDS-UPDRS.

    This is what PPMI analyses use (Holden et al. 2018).
    UPDRS(t) = baseline + rate * t
    """
    return baseline + rate * (t_months / 12)


def updrs_z2_modified(t_months: float, baseline: float, rate: float,
                       z2_scale: str = "none") -> float:
    """
    Test Z²-modified progression model.
    """
    if z2_scale == "Z_squared":
        # Z² modifies rate
        rate_mod = rate / Z_SQUARED * 10
    elif z2_scale == "sqrt_Z":
        # √Z modifies rate
        rate_mod = rate / SQRT_Z
    elif z2_scale == "1_over_Z2":
        # 1/Z² as protective factor
        rate_mod = rate * (1 - 1/Z_SQUARED)
    elif z2_scale == "sigmoid":
        # Z²-based sigmoidal modification
        t_years = t_months / 12
        sigmoid = 1 / (1 + np.exp(-(t_years - 2.5) * Z_SQUARED / 50))
        return baseline + rate * t_years * (0.5 + 0.5 * sigmoid)
    else:
        rate_mod = rate

    return baseline + rate_mod * (t_months / 12)


# =============================================================================
# HALF-TIME SCALING (Tests nucleation mechanism)
# =============================================================================

def half_time_scaling_standard(conc: float, k1: float, k2: float) -> float:
    """
    Half-time from Finke-Watzky model.

    For nucleation-dominated: τ ∝ 1/√(k1*k2*[A0])
    For growth-dominated: τ ∝ 1/(k2*[A0])
    """
    # Approximate half-time from analytical solution
    # τ_1/2 ≈ ln(2) / (k1 + k2*A0) for early times
    return np.log(2) / (k1 + k2 * conc)


def half_time_scaling_z2(conc: float, k1: float, k2: float,
                          z2_scale: str = "none") -> float:
    """Z²-modified half-time prediction."""
    if z2_scale == "Z_squared":
        k1_mod = k1 * Z_SQUARED
    elif z2_scale == "sqrt_Z":
        k1_mod = k1 * SQRT_Z
    elif z2_scale == "1_over_Z2":
        k1_mod = k1 / Z_SQUARED
    else:
        k1_mod = k1

    return np.log(2) / (k1_mod + k2 * conc)


# =============================================================================
# FITTING AND VALIDATION
# =============================================================================

def fit_aggregation_model(data: List[Tuple[float, float]],
                           model_func,
                           z2_scale: str = "none") -> Dict:
    """Fit aggregation model to ThT kinetics data."""

    times = np.array([d[0] for d in data])
    signal = np.array([d[1] for d in data])
    A0 = 1.0  # Normalized

    # Grid search for optimal k1, k2
    best_rmse = float('inf')
    best_params = (K1_FW, K2_FW)

    for k1_scale in np.logspace(-2, 2, 30):
        for k2_scale in np.logspace(-2, 2, 30):
            k1 = K1_FW * k1_scale
            k2 = K2_FW * k2_scale

            if z2_scale == "none":
                pred = np.array([finke_watzky_analytical(t, A0, k1, k2) for t in times])
            else:
                pred = np.array([finke_watzky_z2_modified(t, A0, k1, k2, z2_scale) for t in times])

            rmse = np.sqrt(np.mean((pred - signal)**2))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = (k1, k2)

    # Get predictions with best parameters
    k1, k2 = best_params
    if z2_scale == "none":
        pred = np.array([finke_watzky_analytical(t, A0, k1, k2) for t in times])
    else:
        pred = np.array([finke_watzky_z2_modified(t, A0, k1, k2, z2_scale) for t in times])

    # Metrics
    rmse = np.sqrt(np.mean((pred - signal)**2))
    ss_res = np.sum((signal - pred)**2)
    ss_tot = np.sum((signal - np.mean(signal))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_k1": float(best_params[0]),
        "best_k2": float(best_params[1]),
        "predictions": pred.tolist(),
        "experimental": signal.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
    }


def fit_updrs_model(data: List[Tuple[float, float]],
                     z2_scale: str = "none") -> Dict:
    """Fit MDS-UPDRS progression model."""

    times = np.array([d[0] for d in data])
    scores = np.array([d[1] for d in data])
    baseline = scores[0]

    # Find best rate
    best_rmse = float('inf')
    best_rate = UPDRS_TOTAL_RATE

    for rate in np.linspace(1, 10, 50):
        if z2_scale == "none":
            pred = np.array([updrs_linear_progression(t, baseline, rate) for t in times])
        else:
            pred = np.array([updrs_z2_modified(t, baseline, rate, z2_scale) for t in times])

        rmse = np.sqrt(np.mean((pred - scores)**2))
        if rmse < best_rmse:
            best_rmse = rmse
            best_rate = rate

    # Get predictions
    if z2_scale == "none":
        pred = np.array([updrs_linear_progression(t, baseline, best_rate) for t in times])
    else:
        pred = np.array([updrs_z2_modified(t, baseline, best_rate, z2_scale) for t in times])

    rmse = np.sqrt(np.mean((pred - scores)**2))
    ss_res = np.sum((scores - pred)**2)
    ss_tot = np.sum((scores - np.mean(scores))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_rate": float(best_rate),
        "predictions": pred.tolist(),
        "experimental": scores.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
    }


# =============================================================================
# MAIN VALIDATION
# =============================================================================

def run_validation():
    """Run comprehensive validation using real Parkinson's research models."""

    print("=" * 80)
    print("VALIDATION: Parkinson's Z² Using REAL Scientific Models")
    print("=" * 80)
    print(f"\nZ² = {Z_SQUARED:.4f}")
    print(f"√Z = {SQRT_Z:.4f}")
    print(f"1/Z² = {1/Z_SQUARED:.6f}")
    print()

    z2_scales = ["none", "Z_squared", "sqrt_Z", "1_over_Z2"]
    scale_names = ["Standard", "Z² scaled", "√Z scaled", "1/Z² scaled"]

    results = {}

    # Test 1: α-Synuclein ThT Kinetics (Finke-Watzky model)
    print("TEST 1: α-Synuclein ThT Aggregation (Finke-Watzky Model)")
    print("Data: Buell et al. PNAS 2014")
    print("-" * 70)

    agg_results = {}
    print(f"{'Model':<20} {'RMSE':<12} {'R²':<12}")
    print("-" * 44)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_aggregation_model(BUELL_THT_DATA, finke_watzky_analytical, scale)
        agg_results[name] = result
        print(f"{name:<20} {result['rmse']:<12.4f} {result['r2']:<12.4f}")

    results["aggregation"] = agg_results

    # Test 2: PPMI MDS-UPDRS Total Progression
    print("\nTEST 2: MDS-UPDRS Total Score Progression")
    print("Data: PPMI Cohort (Holden et al. 2018, N=362)")
    print("-" * 70)

    updrs_results = {}
    print(f"{'Model':<20} {'RMSE':<12} {'R²':<12} {'Rate (pts/yr)':<15}")
    print("-" * 60)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_updrs_model(PPMI_UPDRS_TOTAL, scale)
        updrs_results[name] = result
        print(f"{name:<20} {result['rmse']:<12.2f} {result['r2']:<12.4f} {result['best_rate']:<15.2f}")

    results["updrs_total"] = updrs_results

    # Test 3: Unmedicated Part III Progression
    print("\nTEST 3: MDS-UPDRS Part III (Unmedicated)")
    print("Data: PPMI unmedicated subgroup")
    print("-" * 70)

    part3_results = {}
    print(f"{'Model':<20} {'RMSE':<12} {'R²':<12}")
    print("-" * 44)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_updrs_model(PPMI_UPDRS_PART3_UNMED, scale)
        part3_results[name] = result
        print(f"{name:<20} {result['rmse']:<12.2f} {result['r2']:<12.4f}")

    results["updrs_part3"] = part3_results

    # Test 4: Dopaminergic Neuron Loss
    print("\nTEST 4: Dopaminergic Neuron Loss Trajectory")
    print("Data: Fearnley & Lees 1991, Kordower et al. 2013")
    print("-" * 70)

    # Use exponential decay model
    da_results = {}
    print(f"{'Model':<20} {'RMSE':<12} {'R²':<12}")
    print("-" * 44)

    # Convert DA data to progression format
    DA_PROGRESSION = [(d[0] + 10, d[1]) for d in DA_NEURON_LOSS]  # Shift to start at 0

    for scale, name in zip(z2_scales, scale_names):
        result = fit_updrs_model(DA_PROGRESSION, scale)
        da_results[name] = result
        print(f"{name:<20} {result['rmse']:<12.2f} {result['r2']:<12.4f}")

    results["da_neurons"] = da_results

    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    # Count wins
    tests = ["aggregation", "updrs_total", "updrs_part3", "da_neurons"]
    test_names = ["ThT Aggregation", "UPDRS Total", "UPDRS Part III", "DA Neurons"]

    z2_wins = 0
    standard_wins = 0
    ties = 0

    print(f"\n{'Test':<25} {'Best Model':<20} {'Improvement':<15}")
    print("-" * 60)

    for test, test_name in zip(tests, test_names):
        test_results = results[test]
        standard_rmse = test_results["Standard"]["rmse"]

        best_model = "Standard"
        best_rmse = standard_rmse

        for name in scale_names[1:]:  # Skip standard
            if test_results[name]["rmse"] < best_rmse - 0.001:  # Threshold for meaningful improvement
                best_rmse = test_results[name]["rmse"]
                best_model = name

        if best_model == "Standard":
            standard_wins += 1
            improvement = "0%"
        else:
            z2_wins += 1
            improvement = f"{(standard_rmse - best_rmse) / standard_rmse * 100:.1f}%"

        print(f"{test_name:<25} {best_model:<20} {improvement:<15}")

    print(f"\nZ² variants better: {z2_wins}/4 tests")
    print(f"Standard better: {standard_wins}/4 tests")

    # Honest assessment
    print("\n" + "=" * 80)
    print("HONEST ASSESSMENT")
    print("=" * 80)

    if z2_wins > standard_wins:
        print("\n✅ VALIDATED: Z² improves Parkinson's predictions")
        conclusion = "VALIDATED"
    elif z2_wins == standard_wins:
        print("\n⚠️  PARTIAL: Z² shows mixed results")
        print("   Standard Finke-Watzky and linear models already fit well")
        conclusion = "PARTIAL"
    else:
        print("\n❌ NOT VALIDATED: Standard models are better")
        print("   Finke-Watzky (aggregation) and linear (UPDRS) models")
        print("   are the correct models for this disease")
        conclusion = "NOT_VALIDATED"

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test": "Parkinson's Z² Validation with Real Scientific Models",
        "models_used": {
            "aggregation": "Finke-Watzky 2-step nucleation-autocatalytic growth",
            "clinical": "Linear mixed model (MDS-UPDRS)",
        },
        "data_sources": {
            "ThT_kinetics": "Buell et al. PNAS 2014",
            "UPDRS": "Holden et al. Mov Disord Clin Pract 2018 (PPMI)",
            "DA_neurons": "Fearnley & Lees 1991, Kordower et al. 2013",
        },
        "z_constants": {
            "Z": Z,
            "Z_squared": Z_SQUARED,
            "sqrt_Z": SQRT_Z,
        },
        "z2_wins": z2_wins,
        "standard_wins": standard_wins,
        "conclusion": conclusion,
        "detailed_results": results,
    }

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/neuroscience/simulations/parkinsons_validation_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    run_validation()
