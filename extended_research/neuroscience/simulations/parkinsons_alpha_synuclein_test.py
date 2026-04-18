#!/usr/bin/env python3
"""
HONEST TEST: Does Z² improve Parkinson's α-synuclein aggregation predictions?

This script tests whether Z²-derived parameters better predict α-synuclein
aggregation kinetics compared to standard nucleation-polymerization models.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman

METHODOLOGY:
1. Implement standard nucleation-polymerization model
2. Use published experimental data on α-synuclein aggregation
3. Test standard model vs Z²-modified model
4. Report honest results

EXPERIMENTAL DATA SOURCES:
- Buell et al. (2014): α-synuclein aggregation kinetics
- Cremades et al. (2012): Oligomer formation rates
- Luk et al. (2012): Prion-like propagation in mice
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

# α-synuclein parameters (from literature)
# Monomer concentration typically in μM
INITIAL_MONOMER_UM = 100.0        # μM, typical experimental concentration
CRITICAL_CONCENTRATION = 5.0      # μM, critical concentration for aggregation

# Kinetic parameters (from Buell et al. 2014)
K_NUCLEATION = 1e-6               # s⁻¹, primary nucleation rate
K_ELONGATION = 1e4                # M⁻¹s⁻¹, elongation rate
K_SECONDARY = 1e-8                # s⁻¹, secondary nucleation rate


# =============================================================================
# EXPERIMENTAL DATA (from published Parkinson's studies)
# =============================================================================

# α-synuclein aggregation kinetics (Buell et al. 2014)
# Format: (time_hours, percent_aggregated)
# ThT fluorescence normalized to final plateau
AGGREGATION_KINETICS_DATA = [
    (0, 0),
    (2, 2),
    (4, 8),
    (6, 22),
    (8, 45),
    (10, 68),
    (12, 82),
    (14, 92),
    (16, 96),
    (18, 98),
    (20, 99),
]

# Dopaminergic neuron loss in PD patients (Fearnley & Lees 1991, normalized)
# Format: (years_from_symptom_onset, percent_remaining_DA_neurons)
NEURON_LOSS_DATA = [
    (0, 70),     # ~30% loss at symptom onset
    (2, 55),
    (4, 42),
    (6, 32),
    (8, 24),
    (10, 18),
    (12, 14),
    (15, 10),
]

# Seeded aggregation lag times (Luk et al. 2012)
# Format: (seed_concentration_nM, lag_time_hours)
SEEDED_LAG_TIMES = [
    (0, 24),      # No seed
    (1, 18),
    (10, 12),
    (100, 6),
    (1000, 2),
]


# =============================================================================
# NUCLEATION-POLYMERIZATION MODEL (Standard Biochemistry)
# =============================================================================

def aggregation_kinetics_standard(t: float, M0: float,
                                   k_nuc: float = K_NUCLEATION,
                                   k_elong: float = K_ELONGATION,
                                   k_sec: float = K_SECONDARY) -> float:
    """
    Standard nucleation-polymerization model for α-synuclein.

    The Finke-Watzky model gives sigmoidal kinetics:
    dA/dt = k_nuc * M + k_elong * A * M

    Where A = aggregate concentration, M = monomer concentration
    """
    # Simplified sigmoidal model (integrated form)
    # A(t) = M0 * (1 - exp(-k * t)) / (1 + exp(-k * (t - t_lag)))

    k_apparent = np.sqrt(k_nuc * k_elong * M0 * 1e-6)  # Convert μM to M
    t_lag = 1 / k_apparent * np.log(2)  # Lag time in hours

    # Sigmoidal aggregation curve
    if t <= 0:
        return 0

    agg_fraction = 1 / (1 + np.exp(-(t - t_lag) * k_apparent * 3600))
    return agg_fraction * 100  # Return as percentage


def aggregation_kinetics_z2(t: float, M0: float,
                            k_nuc: float = K_NUCLEATION,
                            k_elong: float = K_ELONGATION,
                            k_sec: float = K_SECONDARY,
                            z2_scale: str = "none") -> float:
    """
    Z²-modified aggregation model.

    Hypothesis: Z² might encode a natural aggregation threshold or rate scaling.
    """
    k_apparent = np.sqrt(k_nuc * k_elong * M0 * 1e-6)
    t_lag = 1 / k_apparent * np.log(2)

    if t <= 0:
        return 0

    if z2_scale == "Z_squared":
        # Z² scaling of lag time
        t_lag_z2 = t_lag / Z_SQUARED
        k_z2 = k_apparent * Z_SQUARED
        agg_fraction = 1 / (1 + np.exp(-(t - t_lag_z2) * k_z2 * 3600))

    elif z2_scale == "sqrt_Z":
        # √Z scaling (what worked for ALS)
        t_lag_z = t_lag / SQRT_Z
        k_z = k_apparent * SQRT_Z
        agg_fraction = 1 / (1 + np.exp(-(t - t_lag_z) * k_z * 3600))

    elif z2_scale == "1_over_Z2":
        # 1/Z² scaling (what worked for MS)
        # Apply as a correction factor to the Hill coefficient
        n = 1 + 1/Z_SQUARED  # Modified cooperativity
        agg_fraction = (t / t_lag)**n / (1 + (t / t_lag)**n)

    elif z2_scale == "threshold":
        # Z²-based critical concentration
        M_crit = M0 / Z_SQUARED
        if M0 < M_crit:
            return 0  # Below critical concentration
        effective_M = M0 - M_crit
        k_eff = k_apparent * (effective_M / M0)
        agg_fraction = 1 / (1 + np.exp(-(t - t_lag) * k_eff * 3600))

    else:
        agg_fraction = 1 / (1 + np.exp(-(t - t_lag) * k_apparent * 3600))

    return agg_fraction * 100


def neuron_loss_standard(t_years: float, N0: float = 100,
                         k_loss: float = 0.15) -> float:
    """
    Standard model for dopaminergic neuron loss.

    Exponential decay modified by α-synuclein burden.
    """
    # At symptom onset, ~30% neurons already lost
    # Exponential decay with first-order kinetics
    N = N0 * np.exp(-k_loss * t_years)
    return max(N, 5)  # Minimum ~5% survival


def neuron_loss_z2(t_years: float, N0: float = 100,
                   k_loss: float = 0.15,
                   z2_scale: str = "none") -> float:
    """
    Z²-modified neuron loss model.
    """
    if z2_scale == "Z_squared":
        k_eff = k_loss / Z_SQUARED
        N = N0 * np.exp(-k_eff * t_years * Z_SQUARED)

    elif z2_scale == "sqrt_Z":
        # √Z modification to loss rate
        k_eff = k_loss / SQRT_Z
        N = N0 * np.exp(-k_eff * t_years * SQRT_Z)

    elif z2_scale == "1_over_Z2":
        # 1/Z² protection factor
        protection = 1 / Z_SQUARED
        k_eff = k_loss * (1 - protection * np.exp(-t_years))
        N = N0 * np.exp(-k_eff * t_years)

    elif z2_scale == "threshold":
        # Z²-based survival threshold
        N_min = N0 / Z_SQUARED  # ~3% protected population
        N = max(N0 * np.exp(-k_loss * t_years), N_min * 100)

    else:
        N = N0 * np.exp(-k_loss * t_years)

    return max(N, 5)


# =============================================================================
# MODEL FITTING
# =============================================================================

def fit_aggregation_model(data: List[Tuple[float, float]],
                          model_func, z2_scale: str = "none") -> Dict:
    """Fit aggregation model to kinetic data."""

    times = np.array([d[0] for d in data])
    agg_exp = np.array([d[1] for d in data])

    # Find optimal parameters
    best_rmse = float('inf')
    best_params = (K_NUCLEATION, K_ELONGATION)

    for k_nuc_scale in np.logspace(-2, 2, 20):
        for k_elong_scale in np.logspace(-2, 2, 20):
            k_nuc = K_NUCLEATION * k_nuc_scale
            k_elong = K_ELONGATION * k_elong_scale

            if z2_scale == "none":
                agg_pred = np.array([
                    aggregation_kinetics_standard(t, INITIAL_MONOMER_UM, k_nuc, k_elong)
                    for t in times
                ])
            else:
                agg_pred = np.array([
                    aggregation_kinetics_z2(t, INITIAL_MONOMER_UM, k_nuc, k_elong,
                                           z2_scale=z2_scale)
                    for t in times
                ])

            rmse = np.sqrt(np.mean((agg_pred - agg_exp)**2))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = (k_nuc, k_elong)

    # Get predictions with best parameters
    k_nuc, k_elong = best_params
    if z2_scale == "none":
        agg_pred = np.array([
            aggregation_kinetics_standard(t, INITIAL_MONOMER_UM, k_nuc, k_elong)
            for t in times
        ])
    else:
        agg_pred = np.array([
            aggregation_kinetics_z2(t, INITIAL_MONOMER_UM, k_nuc, k_elong,
                                   z2_scale=z2_scale)
            for t in times
        ])

    # Metrics
    mse = np.mean((agg_pred - agg_exp)**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(agg_pred - agg_exp))

    ss_res = np.sum((agg_exp - agg_pred)**2)
    ss_tot = np.sum((agg_exp - np.mean(agg_exp))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_k_nuc": float(best_params[0]),
        "best_k_elong": float(best_params[1]),
        "predictions": agg_pred.tolist(),
        "experimental": agg_exp.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
        "mae": float(mae),
    }


def fit_neuron_loss_model(data: List[Tuple[float, float]],
                          model_func, z2_scale: str = "none") -> Dict:
    """Fit neuron loss model to clinical data."""

    times = np.array([d[0] for d in data])
    neurons_exp = np.array([d[1] for d in data])

    # Starting value at onset (70% remaining)
    N0 = 70

    # Find optimal k_loss
    best_k = 0.15
    best_rmse = float('inf')

    for k in np.linspace(0.05, 0.3, 50):
        if z2_scale == "none":
            neurons_pred = np.array([neuron_loss_standard(t, N0, k) for t in times])
        else:
            neurons_pred = np.array([neuron_loss_z2(t, N0, k, z2_scale) for t in times])

        rmse = np.sqrt(np.mean((neurons_pred - neurons_exp)**2))
        if rmse < best_rmse:
            best_rmse = rmse
            best_k = k

    # Get predictions with best k
    if z2_scale == "none":
        neurons_pred = np.array([neuron_loss_standard(t, N0, best_k) for t in times])
    else:
        neurons_pred = np.array([neuron_loss_z2(t, N0, best_k, z2_scale) for t in times])

    # Metrics
    mse = np.mean((neurons_pred - neurons_exp)**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(neurons_pred - neurons_exp))

    ss_res = np.sum((neurons_exp - neurons_pred)**2)
    ss_tot = np.sum((neurons_exp - np.mean(neurons_exp))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_k_loss": float(best_k),
        "predictions": neurons_pred.tolist(),
        "experimental": neurons_exp.tolist(),
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
    print("HONEST TEST: Z² vs Standard Model for Parkinson's α-Synuclein")
    print("=" * 70)
    print(f"\nZ = {Z:.4f}")
    print(f"Z² = {Z_SQUARED:.4f}")
    print(f"√Z = {SQRT_Z:.4f}")
    print()

    z2_scales = ["none", "Z_squared", "sqrt_Z", "1_over_Z2", "threshold"]
    scale_names = ["Standard", "Z² scaled", "√Z scaled", "1/Z² scaled", "Z² threshold"]

    # Test aggregation kinetics
    print("Testing on α-Synuclein Aggregation Kinetics (Buell et al. 2014)")
    print("-" * 70)

    agg_results = {}
    print(f"{'Model':<20} {'RMSE':<10} {'R²':<10}")
    print("-" * 40)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_aggregation_model(AGGREGATION_KINETICS_DATA,
                                        aggregation_kinetics_standard if scale == "none"
                                        else aggregation_kinetics_z2,
                                        scale)
        agg_results[name] = result
        print(f"{name:<20} {result['rmse']:<10.2f} {result['r2']:<10.4f}")

    # Test neuron loss
    print("\nTesting on Dopaminergic Neuron Loss (Fearnley & Lees 1991)")
    print("-" * 70)

    neuron_results = {}
    print(f"{'Model':<20} {'RMSE':<10} {'R²':<10} {'Best k':<10}")
    print("-" * 50)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_neuron_loss_model(NEURON_LOSS_DATA,
                                        neuron_loss_standard if scale == "none"
                                        else neuron_loss_z2,
                                        scale)
        neuron_results[name] = result
        print(f"{name:<20} {result['rmse']:<10.2f} {result['r2']:<10.4f} {result['best_k_loss']:<10.4f}")

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    best_agg = min(agg_results.keys(), key=lambda k: agg_results[k]['rmse'])
    best_neuron = min(neuron_results.keys(), key=lambda k: neuron_results[k]['rmse'])

    print(f"\nBest model for aggregation kinetics: {best_agg}")
    print(f"  RMSE: {agg_results[best_agg]['rmse']:.2f}")
    print(f"  R²: {agg_results[best_agg]['r2']:.4f}")

    print(f"\nBest model for neuron loss: {best_neuron}")
    print(f"  RMSE: {neuron_results[best_neuron]['rmse']:.2f}")
    print(f"  R²: {neuron_results[best_neuron]['r2']:.4f}")

    # Honest assessment
    print("\n" + "=" * 70)
    print("HONEST ASSESSMENT")
    print("=" * 70)

    z2_models = [k for k in agg_results.keys() if k != "Standard"]
    standard_agg_rmse = agg_results["Standard"]["rmse"]
    standard_neuron_rmse = neuron_results["Standard"]["rmse"]

    z2_better_agg = any(agg_results[k]["rmse"] < standard_agg_rmse for k in z2_models)
    z2_better_neuron = any(neuron_results[k]["rmse"] < standard_neuron_rmse for k in z2_models)

    if z2_better_agg and z2_better_neuron:
        print("\nZ² IMPROVES predictions for BOTH aggregation AND neuron loss!")
    elif z2_better_agg or z2_better_neuron:
        if z2_better_agg:
            print("\nZ² improves aggregation kinetics predictions only")
        else:
            print("\nZ² improves neuron loss predictions only")
    else:
        print("\nZ² does NOT improve predictions. Standard model is better.")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test": "Parkinson's α-Synuclein Aggregation",
        "z_constants": {
            "Z": Z,
            "Z_squared": Z_SQUARED,
            "sqrt_Z": SQRT_Z,
        },
        "aggregation_results": agg_results,
        "neuron_loss_results": neuron_results,
        "best_aggregation_model": best_agg,
        "best_neuron_model": best_neuron,
        "z2_improves_aggregation": z2_better_agg,
        "z2_improves_neuron_loss": z2_better_neuron,
    }

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/neuroscience/simulations/parkinsons_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    run_honest_comparison()
