#!/usr/bin/env python3
"""
HONEST TEST: Does Z² improve Alzheimer's amyloid-β predictions?

This script tests whether Z²-derived parameters better predict amyloid-β
plaque formation and cognitive decline compared to standard models.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman

METHODOLOGY:
1. Implement standard amyloid cascade model
2. Use published experimental data on Aβ accumulation and cognitive decline
3. Test standard model vs Z²-modified model
4. Report honest results

EXPERIMENTAL DATA SOURCES:
- Jack et al. (2010): Biomarker model of AD progression
- Villain et al. (2012): Aβ-PET longitudinal data
- Bateman et al. (2012): Dominantly inherited AD network
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple

# =============================================================================
# CONSTANTS
# =============================================================================

# Z² Framework constants
Z = 2 * np.sqrt(8 * np.pi / 3)   # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3        # ≈ 33.51
SQRT_Z = np.sqrt(Z)               # ≈ 2.406

# Amyloid-β parameters (from literature)
AB_PRODUCTION_RATE = 0.1          # ng/mL/day, Aβ production
AB_CLEARANCE_RATE = 0.05          # day⁻¹, normal clearance
AB_AGGREGATION_RATE = 0.01        # day⁻¹, aggregation rate
PLAQUE_THRESHOLD = 50             # ng/mL, threshold for plaque formation


# =============================================================================
# EXPERIMENTAL DATA (from published Alzheimer's studies)
# =============================================================================

# Aβ-PET SUVR progression (Jack et al. 2010, Villain et al. 2012)
# Format: (years_before_symptom_onset, Aβ_SUVR_normalized_percent)
# SUVR normalized: 0 = no Aβ, 100 = maximum plaque load
AB_ACCUMULATION_DATA = [
    (-20, 5),     # 20 years before symptoms
    (-15, 15),
    (-10, 35),
    (-5, 60),
    (0, 80),      # Symptom onset
    (5, 92),
    (10, 98),     # Near saturation
]

# Cognitive decline (MMSE scores normalized, Bateman et al. 2012)
# Format: (years_from_symptom_onset, cognitive_score_percent)
COGNITIVE_DECLINE_DATA = [
    (-10, 100),   # Normal cognition
    (-5, 98),
    (0, 85),      # Symptom onset (mild cognitive impairment)
    (2, 70),
    (4, 55),
    (6, 40),
    (8, 28),
    (10, 18),
]

# Tau accumulation (follows Aβ with lag, Bateman et al. 2012)
# Format: (years_from_symptom_onset, tau_PET_normalized_percent)
TAU_ACCUMULATION_DATA = [
    (-15, 5),
    (-10, 10),
    (-5, 25),
    (0, 50),
    (5, 75),
    (10, 90),
]


# =============================================================================
# AMYLOID CASCADE MODEL (Standard Neuroscience)
# =============================================================================

def amyloid_accumulation_standard(t_years: float,
                                   k_prod: float = AB_PRODUCTION_RATE,
                                   k_clear: float = AB_CLEARANCE_RATE,
                                   k_agg: float = AB_AGGREGATION_RATE) -> float:
    """
    Standard amyloid cascade model.

    Sigmoidal accumulation due to:
    1. Constant production
    2. Saturable clearance
    3. Self-seeding aggregation

    Model: dAβ/dt = k_prod + k_agg*Aβ - k_clear*Aβ/(1 + Aβ/K_m)
    """
    # Simplified sigmoidal model (common in AD literature)
    # Accounts for the ~20 year preclinical phase

    # Parameters tuned to match Jack et al. biomarker model
    t_half = -10  # Years before symptoms when Aβ is at 50%
    steepness = 0.15  # Controls slope of sigmoid

    # Standard logistic model
    ab_percent = 100 / (1 + np.exp(-steepness * (t_years - t_half)))

    return ab_percent


def amyloid_accumulation_z2(t_years: float,
                            k_prod: float = AB_PRODUCTION_RATE,
                            k_clear: float = AB_CLEARANCE_RATE,
                            k_agg: float = AB_AGGREGATION_RATE,
                            z2_scale: str = "none") -> float:
    """
    Z²-modified amyloid accumulation model.

    Hypothesis: Z² might encode a clearance threshold or aggregation rate.
    """
    t_half = -10
    steepness = 0.15

    if z2_scale == "Z_squared":
        # Z² modifies steepness
        steepness_z = steepness * Z_SQUARED / 10
        ab_percent = 100 / (1 + np.exp(-steepness_z * (t_years - t_half)))

    elif z2_scale == "sqrt_Z":
        # √Z modifies the time scale
        t_half_z = t_half / SQRT_Z
        steepness_z = steepness * SQRT_Z
        ab_percent = 100 / (1 + np.exp(-steepness_z * (t_years - t_half_z)))

    elif z2_scale == "1_over_Z2":
        # 1/Z² as clearance enhancement factor
        clearance_boost = 1 + 1/Z_SQUARED
        steepness_z = steepness / clearance_boost
        ab_percent = 100 / (1 + np.exp(-steepness_z * (t_years - t_half)))

    elif z2_scale == "threshold":
        # Z²-based threshold effect
        # Below threshold, Aβ is cleared; above, it accumulates
        threshold_time = t_half - Z_SQUARED/10
        if t_years < threshold_time:
            ab_percent = 5  # Minimal baseline
        else:
            ab_percent = 100 / (1 + np.exp(-steepness * (t_years - t_half)))

    else:
        ab_percent = 100 / (1 + np.exp(-steepness * (t_years - t_half)))

    return ab_percent


def cognitive_decline_standard(t_years: float, ab_level: float = None,
                                k_decline: float = 0.12) -> float:
    """
    Standard cognitive decline model.

    Cognitive decline follows Aβ accumulation with a lag.
    """
    # Decline onset at symptom start (t=0)
    if t_years < -10:
        return 100  # Normal cognition

    # Exponential decline after prodromal phase
    t_effective = max(0, t_years + 5)  # Decline starts ~5 years before symptoms
    cog_score = 100 * np.exp(-k_decline * t_effective)

    return max(cog_score, 10)  # Floor at 10% (severe dementia)


def cognitive_decline_z2(t_years: float, ab_level: float = None,
                         k_decline: float = 0.12,
                         z2_scale: str = "none") -> float:
    """
    Z²-modified cognitive decline model.
    """
    if t_years < -10:
        return 100

    t_effective = max(0, t_years + 5)

    if z2_scale == "Z_squared":
        k_eff = k_decline / Z_SQUARED * 10
        cog_score = 100 * np.exp(-k_eff * t_effective)

    elif z2_scale == "sqrt_Z":
        # √Z scaling (worked for ALS)
        k_eff = k_decline / SQRT_Z
        cog_score = 100 * np.exp(-k_eff * t_effective * SQRT_Z)

    elif z2_scale == "1_over_Z2":
        # 1/Z² provides cognitive reserve
        reserve = 1/Z_SQUARED  # ~3% reserve
        k_eff = k_decline * (1 - reserve)
        cog_score = 100 * np.exp(-k_eff * t_effective) + reserve * 100

    elif z2_scale == "threshold":
        # Z²-based cognitive threshold
        cog_floor = 100 / Z_SQUARED  # ~3% preserved function
        cog_score = max(100 * np.exp(-k_decline * t_effective), cog_floor * 100)

    else:
        cog_score = 100 * np.exp(-k_decline * t_effective)

    return max(cog_score, 10)


# =============================================================================
# MODEL FITTING
# =============================================================================

def fit_amyloid_model(data: List[Tuple[float, float]],
                      model_func, z2_scale: str = "none") -> Dict:
    """Fit amyloid accumulation model to PET data."""

    times = np.array([d[0] for d in data])
    ab_exp = np.array([d[1] for d in data])

    # Find optimal parameters
    best_rmse = float('inf')
    best_params = {}

    for steepness in np.linspace(0.05, 0.3, 25):
        for t_half in np.linspace(-15, -5, 25):
            if z2_scale == "none":
                # Modify the model call to use these params
                ab_pred = np.array([
                    100 / (1 + np.exp(-steepness * (t - t_half)))
                    for t in times
                ])
            else:
                ab_pred = np.array([
                    model_func(t, z2_scale=z2_scale)
                    for t in times
                ])

            rmse = np.sqrt(np.mean((ab_pred - ab_exp)**2))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = {"steepness": steepness, "t_half": t_half}

    # Get predictions with best parameters
    if z2_scale == "none":
        ab_pred = np.array([
            100 / (1 + np.exp(-best_params["steepness"] * (t - best_params["t_half"])))
            for t in times
        ])
    else:
        ab_pred = np.array([model_func(t, z2_scale=z2_scale) for t in times])

    # Metrics
    mse = np.mean((ab_pred - ab_exp)**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(ab_pred - ab_exp))

    ss_res = np.sum((ab_exp - ab_pred)**2)
    ss_tot = np.sum((ab_exp - np.mean(ab_exp))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_params": best_params,
        "predictions": ab_pred.tolist(),
        "experimental": ab_exp.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
        "mae": float(mae),
    }


def fit_cognitive_model(data: List[Tuple[float, float]],
                        model_func, z2_scale: str = "none") -> Dict:
    """Fit cognitive decline model to clinical data."""

    times = np.array([d[0] for d in data])
    cog_exp = np.array([d[1] for d in data])

    # Find optimal k_decline
    best_k = 0.12
    best_rmse = float('inf')

    for k in np.linspace(0.05, 0.25, 50):
        if z2_scale == "none":
            cog_pred = np.array([cognitive_decline_standard(t, k_decline=k) for t in times])
        else:
            cog_pred = np.array([cognitive_decline_z2(t, k_decline=k, z2_scale=z2_scale)
                                 for t in times])

        rmse = np.sqrt(np.mean((cog_pred - cog_exp)**2))
        if rmse < best_rmse:
            best_rmse = rmse
            best_k = k

    # Get predictions with best k
    if z2_scale == "none":
        cog_pred = np.array([cognitive_decline_standard(t, k_decline=best_k) for t in times])
    else:
        cog_pred = np.array([cognitive_decline_z2(t, k_decline=best_k, z2_scale=z2_scale)
                             for t in times])

    # Metrics
    mse = np.mean((cog_pred - cog_exp)**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(cog_pred - cog_exp))

    ss_res = np.sum((cog_exp - cog_pred)**2)
    ss_tot = np.sum((cog_exp - np.mean(cog_exp))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_k_decline": float(best_k),
        "predictions": cog_pred.tolist(),
        "experimental": cog_exp.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
        "mae": float(mae),
    }


# =============================================================================
# MAIN TEST
# =============================================================================

def run_honest_comparison():
    """Run honest comparison of standard vs Z² models."""

    print("=" * 70)
    print("HONEST TEST: Z² vs Standard Model for Alzheimer's Amyloid-β")
    print("=" * 70)
    print(f"\nZ = {Z:.4f}")
    print(f"Z² = {Z_SQUARED:.4f}")
    print(f"√Z = {SQRT_Z:.4f}")
    print()

    z2_scales = ["none", "Z_squared", "sqrt_Z", "1_over_Z2", "threshold"]
    scale_names = ["Standard", "Z² scaled", "√Z scaled", "1/Z² scaled", "Z² threshold"]

    # Test amyloid accumulation
    print("Testing on Aβ-PET Accumulation (Jack et al. 2010)")
    print("-" * 70)

    ab_results = {}
    print(f"{'Model':<20} {'RMSE':<10} {'R²':<10}")
    print("-" * 40)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_amyloid_model(AB_ACCUMULATION_DATA,
                                    amyloid_accumulation_standard if scale == "none"
                                    else amyloid_accumulation_z2,
                                    scale)
        ab_results[name] = result
        print(f"{name:<20} {result['rmse']:<10.2f} {result['r2']:<10.4f}")

    # Test cognitive decline
    print("\nTesting on Cognitive Decline (Bateman et al. 2012)")
    print("-" * 70)

    cog_results = {}
    print(f"{'Model':<20} {'RMSE':<10} {'R²':<10} {'Best k':<10}")
    print("-" * 50)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_cognitive_model(COGNITIVE_DECLINE_DATA,
                                      cognitive_decline_standard if scale == "none"
                                      else cognitive_decline_z2,
                                      scale)
        cog_results[name] = result
        print(f"{name:<20} {result['rmse']:<10.2f} {result['r2']:<10.4f} {result['best_k_decline']:<10.4f}")

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    best_ab = min(ab_results.keys(), key=lambda k: ab_results[k]['rmse'])
    best_cog = min(cog_results.keys(), key=lambda k: cog_results[k]['rmse'])

    print(f"\nBest model for Aβ accumulation: {best_ab}")
    print(f"  RMSE: {ab_results[best_ab]['rmse']:.2f}")
    print(f"  R²: {ab_results[best_ab]['r2']:.4f}")

    print(f"\nBest model for cognitive decline: {best_cog}")
    print(f"  RMSE: {cog_results[best_cog]['rmse']:.2f}")
    print(f"  R²: {cog_results[best_cog]['r2']:.4f}")

    # Honest assessment
    print("\n" + "=" * 70)
    print("HONEST ASSESSMENT")
    print("=" * 70)

    z2_models = [k for k in ab_results.keys() if k != "Standard"]
    standard_ab_rmse = ab_results["Standard"]["rmse"]
    standard_cog_rmse = cog_results["Standard"]["rmse"]

    z2_better_ab = any(ab_results[k]["rmse"] < standard_ab_rmse for k in z2_models)
    z2_better_cog = any(cog_results[k]["rmse"] < standard_cog_rmse for k in z2_models)

    if z2_better_ab and z2_better_cog:
        print("\nZ² IMPROVES predictions for BOTH Aβ accumulation AND cognitive decline!")
    elif z2_better_ab or z2_better_cog:
        if z2_better_ab:
            print("\nZ² improves Aβ accumulation predictions only")
        else:
            print("\nZ² improves cognitive decline predictions only")
    else:
        print("\nZ² does NOT improve predictions. Standard model is better.")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test": "Alzheimer's Amyloid-β Accumulation",
        "z_constants": {
            "Z": Z,
            "Z_squared": Z_SQUARED,
            "sqrt_Z": SQRT_Z,
        },
        "amyloid_results": ab_results,
        "cognitive_results": cog_results,
        "best_amyloid_model": best_ab,
        "best_cognitive_model": best_cog,
        "z2_improves_amyloid": z2_better_ab,
        "z2_improves_cognition": z2_better_cog,
    }

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/neuroscience/simulations/alzheimers_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    run_honest_comparison()
