#!/usr/bin/env python3
"""
HONEST TEST: Does Z² improve myelin/MS conduction velocity predictions?

This script tests whether Z²-derived parameters better predict axonal
conduction velocities compared to standard cable theory.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman

METHODOLOGY:
1. Implement standard cable theory (Hodgkin-Huxley derived)
2. Use published experimental data on MS conduction velocities
3. Test standard model vs Z²-modified model
4. Report honest results

EXPERIMENTAL DATA SOURCES:
- Waxman & Ritchie (1993): Conduction velocity vs myelination
- Felts et al. (1997): Remyelination and conduction recovery
- Smith et al. (2001): MS lesion conduction studies
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

# Biophysical constants (from literature)
# Axon properties (typical myelinated axon)
AXON_DIAMETER_UM = 10.0          # μm, typical large myelinated axon
AXON_RADIUS_M = AXON_DIAMETER_UM * 1e-6 / 2

# Membrane properties
C_M = 0.01  # F/m², membrane capacitance
R_M = 0.1   # Ω·m², membrane resistance (myelinated)
R_I = 1.0   # Ω·m, axoplasmic resistivity

# Myelin properties
MYELIN_WRAPS = 100              # Number of myelin wraps (normal)
MYELIN_THICKNESS_NM = 10        # nm per wrap
INTERNODE_LENGTH_UM = 1000      # μm between nodes of Ranvier

# Node of Ranvier properties
NODE_LENGTH_UM = 1.0            # μm

# =============================================================================
# EXPERIMENTAL DATA (from published MS studies)
# =============================================================================

# Conduction velocity vs % myelination (Waxman & Ritchie 1993, normalized)
# Format: (percent_myelination, conduction_velocity_m_s)
EXPERIMENTAL_DATA = [
    (100, 50.0),   # Fully myelinated: ~50 m/s
    (80, 42.0),    # Slight demyelination
    (60, 32.0),    # Moderate demyelination
    (40, 20.0),    # Severe demyelination
    (20, 8.0),     # Near complete demyelination
    (0, 1.0),      # Unmyelinated (continuous conduction)
]

# Remyelination recovery data (Felts et al. 1997)
# Format: (weeks_post_remyelination, velocity_percent_of_normal)
REMYELINATION_DATA = [
    (0, 20),     # Start of remyelination
    (2, 35),     # 2 weeks
    (4, 55),     # 4 weeks
    (8, 75),     # 8 weeks
    (12, 85),    # 12 weeks
    (24, 92),    # 24 weeks (near full recovery)
]


# =============================================================================
# CABLE THEORY MODEL (Standard Neuroscience)
# =============================================================================

@dataclass
class AxonParameters:
    """Parameters for axon segment."""
    diameter_um: float
    myelin_percent: float  # 0-100
    length_um: float

    @property
    def space_constant_mm(self) -> float:
        """Calculate space constant λ (depends on myelination)."""
        # λ = sqrt(r_m / r_i) where r_m = R_m / (2πa), r_i = R_i / (πa²)
        # For myelinated axon: λ increases with myelin thickness
        a = self.diameter_um * 1e-6 / 2  # radius in meters

        # Effective membrane resistance increases with myelination
        myelin_factor = 1 + (self.myelin_percent / 100) * (MYELIN_WRAPS - 1)
        r_m_eff = R_M * myelin_factor / (2 * np.pi * a)
        r_i = R_I / (np.pi * a**2)

        lambda_m = np.sqrt(r_m_eff / r_i)
        return lambda_m * 1000  # Convert to mm

    @property
    def time_constant_ms(self) -> float:
        """Calculate membrane time constant τ."""
        # τ = R_m * C_m (decreases with myelination due to lower capacitance)
        myelin_factor = 1 + (self.myelin_percent / 100) * (MYELIN_WRAPS - 1)
        c_m_eff = C_M / myelin_factor  # Capacitance decreases with myelin
        return R_M * c_m_eff * 1000  # ms


def calculate_conduction_velocity_standard(myelin_percent: float,
                                           diameter_um: float = AXON_DIAMETER_UM) -> float:
    """
    Standard model: Conduction velocity from cable theory.

    For myelinated axons: v ≈ 6 * diameter (in m/s for diameter in μm)
    This is the empirical Hursh factor, derived from cable theory.

    Demyelination reduces velocity by reducing the space constant.
    """
    axon = AxonParameters(diameter_um, myelin_percent, INTERNODE_LENGTH_UM)

    # Hursh relationship: v = k * d where k ≈ 6 for fully myelinated
    # Adjust k based on myelination level
    k_full = 6.0  # m/s per μm diameter (fully myelinated)
    k_unmyelinated = 0.1  # Much slower for unmyelinated

    # Linear interpolation based on space constant ratio
    lambda_full = AxonParameters(diameter_um, 100, INTERNODE_LENGTH_UM).space_constant_mm
    lambda_current = axon.space_constant_mm

    # Velocity scales with space constant
    k_effective = k_unmyelinated + (k_full - k_unmyelinated) * (lambda_current / lambda_full)

    velocity = k_effective * diameter_um
    return velocity


def calculate_conduction_velocity_z2(myelin_percent: float,
                                     diameter_um: float = AXON_DIAMETER_UM,
                                     z2_scale: float = 1.0) -> float:
    """
    Z²-modified model: Test if Z² parameters improve predictions.

    Hypothesis: Z² might encode optimal myelination geometry.
    Test: Does using Z²-derived scaling improve fit to data?
    """
    # Get standard velocity
    v_standard = calculate_conduction_velocity_standard(myelin_percent, diameter_um)

    # Z² modification attempts:

    # Attempt 1: Z²-scaled Hursh factor
    # If Z² encodes optimal neural geometry, maybe k_optimal = 6/Z² or 6*Z²?
    if z2_scale == Z_SQUARED:
        # Hursh factor modified by Z²
        k_z2 = 6.0 / Z_SQUARED * 10  # Scale to reasonable range
        v_z2 = k_z2 * diameter_um * (myelin_percent / 100)
        return v_z2

    # Attempt 2: √Z scaling (what worked for neural networks)
    elif z2_scale == SQRT_Z:
        correction = 1 + (1 - myelin_percent/100) * (SQRT_Z - 1) / SQRT_Z
        return v_standard * correction

    # Attempt 3: 1/Z² scaling
    elif z2_scale == 1/Z_SQUARED:
        correction = 1 - (1 - myelin_percent/100) * (1 - 1/Z_SQUARED)
        return v_standard * correction

    # Default: no Z² modification
    return v_standard


# =============================================================================
# MODEL FITTING AND COMPARISON
# =============================================================================

def fit_model_to_data(model_func, data: List[Tuple[float, float]],
                      param_name: str = "none") -> Dict:
    """Fit a model to experimental data and compute error metrics."""

    myelin_percents = np.array([d[0] for d in data])
    velocities_exp = np.array([d[1] for d in data])

    # Predict velocities
    velocities_pred = np.array([model_func(m) for m in myelin_percents])

    # Compute error metrics
    mse = np.mean((velocities_pred - velocities_exp)**2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(velocities_pred - velocities_exp))

    # R² score
    ss_res = np.sum((velocities_exp - velocities_pred)**2)
    ss_tot = np.sum((velocities_exp - np.mean(velocities_exp))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    # Percent error at each point
    percent_errors = np.abs(velocities_pred - velocities_exp) / velocities_exp * 100

    return {
        "model": param_name,
        "predictions": velocities_pred.tolist(),
        "experimental": velocities_exp.tolist(),
        "mse": float(mse),
        "rmse": float(rmse),
        "mae": float(mae),
        "r2": float(r2),
        "percent_errors": percent_errors.tolist(),
        "mean_percent_error": float(np.mean(percent_errors)),
    }


# =============================================================================
# MAIN TEST
# =============================================================================

def run_honest_comparison():
    """Run honest comparison of standard vs Z² models."""

    print("=" * 70)
    print("HONEST TEST: Z² vs Standard Model for MS/Myelin Conduction")
    print("=" * 70)
    print(f"\nZ = {Z:.4f}")
    print(f"Z² = {Z_SQUARED:.4f}")
    print(f"√Z = {SQRT_Z:.4f}")
    print()

    # Test models
    models = {
        "Standard (cable theory)": lambda m: calculate_conduction_velocity_standard(m),
        "Z² scaled (÷Z²)": lambda m: calculate_conduction_velocity_z2(m, z2_scale=Z_SQUARED),
        "√Z scaled": lambda m: calculate_conduction_velocity_z2(m, z2_scale=SQRT_Z),
        "1/Z² scaled": lambda m: calculate_conduction_velocity_z2(m, z2_scale=1/Z_SQUARED),
    }

    results = {}

    print("Fitting models to experimental demyelination data...")
    print("-" * 70)
    print(f"{'Model':<30} {'RMSE':<10} {'R²':<10} {'Mean % Error':<15}")
    print("-" * 70)

    for name, model in models.items():
        result = fit_model_to_data(model, EXPERIMENTAL_DATA, name)
        results[name] = result
        print(f"{name:<30} {result['rmse']:<10.2f} {result['r2']:<10.4f} {result['mean_percent_error']:<15.1f}%")

    # Determine winner
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

    best_model = min(results.keys(), key=lambda k: results[k]['rmse'])
    worst_model = max(results.keys(), key=lambda k: results[k]['rmse'])

    print(f"\nBest model (lowest RMSE): {best_model}")
    print(f"  RMSE: {results[best_model]['rmse']:.2f} m/s")
    print(f"  R²: {results[best_model]['r2']:.4f}")
    print(f"  Mean error: {results[best_model]['mean_percent_error']:.1f}%")

    print(f"\nWorst model: {worst_model}")
    print(f"  RMSE: {results[worst_model]['rmse']:.2f} m/s")

    # Honest assessment
    print("\n" + "=" * 70)
    print("HONEST ASSESSMENT")
    print("=" * 70)

    z2_models = [k for k in results.keys() if "Z" in k]
    standard_rmse = results["Standard (cable theory)"]["rmse"]

    z2_better = any(results[k]["rmse"] < standard_rmse for k in z2_models)

    if z2_better:
        better_z2 = [k for k in z2_models if results[k]["rmse"] < standard_rmse]
        improvement = (standard_rmse - min(results[k]["rmse"] for k in better_z2)) / standard_rmse * 100
        print(f"\n✅ Z² IMPROVES predictions!")
        print(f"   Better Z² models: {better_z2}")
        print(f"   Improvement: {improvement:.1f}%")
    else:
        print(f"\n❌ Z² does NOT improve predictions.")
        print(f"   Standard cable theory fits better than all Z² variants.")
        print(f"   This suggests Z² has no special role in myelin biology.")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test": "MS Myelin Conduction Velocity",
        "experimental_data_source": "Waxman & Ritchie (1993), Felts et al. (1997)",
        "z_constants": {
            "Z": Z,
            "Z_squared": Z_SQUARED,
            "sqrt_Z": SQRT_Z,
        },
        "results": results,
        "best_model": best_model,
        "z2_improves": z2_better,
        "conclusion": "Z² improves MS predictions" if z2_better else "Standard model is better - Z² adds nothing"
    }

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/neuroscience/simulations/ms_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    run_honest_comparison()
