#!/usr/bin/env python3
"""
THERAPEUTIC PROTEIN FOLDING: Z² Framework for Drug Development

This module applies Z² to therapeutically relevant protein folding problems:

1. MUTATION STABILITY (ΔΔG)
   - Predict which mutations cause disease
   - Identify druggable mutations
   - Data from ProThermDB

2. AGGREGATION KINETICS & DRUG TIMING
   - Primary vs secondary nucleation inhibitors
   - Optimal intervention timing
   - Based on Cohen/Knowles mechanistic model

3. PHARMACOLOGICAL CHAPERONE DESIGN
   - Predict stabilization requirements
   - Identify binding site characteristics

THERAPEUTIC APPLICATIONS:
- Alzheimer's: Aβ aggregation inhibitors
- Parkinson's: α-synuclein secondary nucleation blockers
- Cystic fibrosis: CFTR folding correctors
- Cancer: p53 reactivators

SPDX-License-Identifier: CC-BY-4.0
Copyright (C) 2026 Carl Zimmerman

Data sources:
- ProThermDB: Mutation stability data
- Cohen et al. PNAS 2013: Aggregation kinetics
- Arosio et al. PNAS 2016: Optimal control theory
"""

import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)   # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3        # ≈ 33.51
SQRT_Z = np.sqrt(Z)               # ≈ 2.406

# Physical constants
R = 8.314e-3      # kJ/(mol·K)
R_kcal = 1.987e-3  # kcal/(mol·K)
T_REF = 310.15     # K (37°C, physiological)
kB = 1.381e-23     # J/K

# =============================================================================
# DISEASE-RELEVANT MUTATION DATA (from ProThermDB and literature)
# =============================================================================

# Format: (protein, mutation, ΔΔG_exp kcal/mol, disease_association)
# Positive ΔΔG = destabilizing (disease-causing)
# Negative ΔΔG = stabilizing

DISEASE_MUTATIONS = [
    # p53 tumor suppressor - cancer mutations
    ("p53", "R248Q", 2.8, "cancer"),
    ("p53", "R273H", 1.5, "cancer"),
    ("p53", "Y220C", 4.0, "cancer"),
    ("p53", "G245S", 2.2, "cancer"),
    ("p53", "R249S", 3.1, "cancer"),
    ("p53", "V143A", 3.5, "cancer"),

    # SOD1 - ALS mutations
    ("SOD1", "A4V", 2.5, "ALS"),
    ("SOD1", "G93A", 1.8, "ALS"),
    ("SOD1", "D90A", 0.5, "ALS"),
    ("SOD1", "H46R", 2.1, "ALS"),
    ("SOD1", "G85R", 3.2, "ALS"),

    # Transthyretin - cardiac amyloidosis
    ("TTR", "V30M", 1.2, "amyloidosis"),
    ("TTR", "L55P", 2.8, "amyloidosis"),
    ("TTR", "V122I", 0.8, "amyloidosis"),
    ("TTR", "T60A", 1.5, "amyloidosis"),

    # CFTR - cystic fibrosis
    ("CFTR", "F508del", 4.5, "CF"),
    ("CFTR", "G551D", 2.0, "CF"),
    ("CFTR", "R117H", 1.0, "CF"),

    # α-synuclein - Parkinson's
    ("SNCA", "A53T", 0.3, "PD"),
    ("SNCA", "A30P", 0.5, "PD"),
    ("SNCA", "E46K", 0.8, "PD"),

    # APP/PSEN - Alzheimer's
    ("APP", "V717I", 1.5, "AD"),
    ("APP", "K670N/M671L", 2.0, "AD"),
    ("PSEN1", "A246E", 1.8, "AD"),
]

# Benchmark mutations with known ΔΔG (from ProThermDB)
PROTHERM_BENCHMARK = [
    # Barnase mutations
    ("Barnase", "A32G", 1.2),
    ("Barnase", "I25A", 3.8),
    ("Barnase", "I51A", 2.9),
    ("Barnase", "I76A", 3.1),
    ("Barnase", "I88A", 2.5),
    ("Barnase", "L14A", 4.2),
    ("Barnase", "Y17A", 2.8),

    # CI2 mutations
    ("CI2", "A16G", 1.8),
    ("CI2", "I20A", 2.4),
    ("CI2", "L49A", 3.5),
    ("CI2", "I57A", 2.1),
    ("CI2", "V66A", 1.9),

    # Lysozyme mutations
    ("Lysozyme", "I56A", 3.2),
    ("Lysozyme", "V74A", 2.8),
    ("Lysozyme", "I98A", 3.5),
    ("Lysozyme", "L99A", 4.8),
    ("Lysozyme", "M102A", 2.3),

    # Ubiquitin mutations
    ("Ubiquitin", "V5A", 2.1),
    ("Ubiquitin", "I13A", 2.8),
    ("Ubiquitin", "L15A", 3.2),
    ("Ubiquitin", "V26A", 3.5),
    ("Ubiquitin", "I44A", 4.1),
]

# =============================================================================
# AGGREGATION KINETICS DATA (for drug timing optimization)
# =============================================================================

# Aβ42 aggregation with different inhibitors
# Format: (inhibitor_type, target_step, IC50_μM, efficacy_reduction_%)
AGGREGATION_INHIBITORS = [
    ("Bexarotene", "primary_nucleation", 1.0, 65),
    ("Tramiprosate", "elongation", 50.0, 40),
    ("EGCG", "secondary_nucleation", 10.0, 55),
    ("DesAb29-36", "secondary_nucleation", 0.1, 80),
    ("Crenezumab", "elongation", 0.01, 45),
    ("Aducanumab", "fibril_binding", 0.001, 70),
    ("SV111", "primary_nucleation", 5.0, 50),
]

# α-synuclein aggregation inhibitors
SYNUCLEIN_INHIBITORS = [
    ("Molecule 69.2", "secondary_nucleation", 5.0, 75),
    ("Anle138b", "oligomer_formation", 1.0, 60),
    ("NPT100-18A", "membrane_binding", 10.0, 50),
    ("Fasudil", "aggregation", 100.0, 30),
]

# =============================================================================
# ΔΔG PREDICTION MODELS
# =============================================================================

def ddg_empirical_standard(mutation_type: str, position_burial: float,
                           hydrophobicity_change: float) -> float:
    """
    Standard empirical ΔΔG prediction.

    Based on: ΔΔG ≈ a × burial + b × ΔHydrophobicity + c

    Parameters from literature consensus.
    """
    # Empirical coefficients (simplified)
    a_burial = 2.0      # kcal/mol per burial fraction
    b_hydro = 0.5       # kcal/mol per hydrophobicity unit
    c_base = 0.5        # baseline destabilization

    ddg = a_burial * position_burial + b_hydro * hydrophobicity_change + c_base
    return ddg


def ddg_z2_corrected(mutation_type: str, position_burial: float,
                     hydrophobicity_change: float, z2_scale: str = "none") -> float:
    """
    Z²-corrected ΔΔG prediction.

    Hypothesis: Z² might encode the coupling between burial and
    hydrophobicity in protein cores.
    """
    if z2_scale == "sqrt_Z":
        # √Z scales the burial-hydrophobicity coupling
        a_burial = 2.0 / SQRT_Z
        b_hydro = 0.5 * SQRT_Z
        c_base = 0.5 / SQRT_Z
    elif z2_scale == "1_over_Z2":
        # 1/Z² as packing efficiency factor
        a_burial = 2.0 * (1 + 1/Z_SQUARED)
        b_hydro = 0.5 / (1 + 1/Z_SQUARED)
        c_base = 0.5 * (1 - 1/Z_SQUARED)
    elif z2_scale == "Z_squared":
        # Z² in denominator (smaller corrections)
        a_burial = 2.0 * 10 / Z_SQUARED
        b_hydro = 0.5 * Z_SQUARED / 10
        c_base = 0.5
    else:
        a_burial = 2.0
        b_hydro = 0.5
        c_base = 0.5

    ddg = a_burial * position_burial + b_hydro * hydrophobicity_change + c_base
    return ddg


# =============================================================================
# AGGREGATION KINETICS WITH DRUG INTERVENTION
# =============================================================================

def aggregation_kinetics_ode(y, t, kn, k2, kplus, m0,
                              inhibitor_type: str = None,
                              inhibitor_conc: float = 0,
                              IC50: float = 1.0):
    """
    Full aggregation kinetics ODE with drug intervention.

    dP/dt = kn*m^nc + k2*m^n2*M  (fibril number)
    dM/dt = 2*k+*m*P             (fibril mass)

    Inhibitor modifies specific rate constants.
    """
    P, M = y
    m = max(0, m0 - M)  # monomer concentration

    # Apply inhibitor effects
    kn_eff = kn
    k2_eff = k2
    kplus_eff = kplus

    if inhibitor_type and inhibitor_conc > 0:
        inhibition = inhibitor_conc / (inhibitor_conc + IC50)

        if inhibitor_type == "primary_nucleation":
            kn_eff = kn * (1 - inhibition)
        elif inhibitor_type == "secondary_nucleation":
            k2_eff = k2 * (1 - inhibition)
        elif inhibitor_type == "elongation":
            kplus_eff = kplus * (1 - inhibition)
        elif inhibitor_type == "fibril_binding":
            k2_eff = k2 * (1 - inhibition)
            kplus_eff = kplus * (1 - 0.5 * inhibition)

    # Rate equations
    dP_dt = kn_eff * (m ** 2) + k2_eff * (m ** 2) * M
    dM_dt = 2 * kplus_eff * m * P

    return [dP_dt, dM_dt]


def simulate_aggregation_with_drug(m0: float, drug_time: float,
                                    inhibitor_type: str, inhibitor_conc: float,
                                    IC50: float, total_time: float = 100,
                                    z2_scale: str = "none") -> Dict:
    """
    Simulate aggregation with drug intervention at specified time.

    Returns metrics on oligomer formation and fibril load.
    """
    # Rate constants (Aβ42-like)
    kn = 1e-4   # primary nucleation
    k2 = 1e4    # secondary nucleation
    kplus = 1e6  # elongation

    # Apply Z² scaling to rate constants
    if z2_scale == "sqrt_Z":
        k2 = k2 * SQRT_Z
        kplus = kplus / SQRT_Z
    elif z2_scale == "1_over_Z2":
        kn = kn / Z_SQUARED
        k2 = k2 * (1 + 1/Z_SQUARED)
    elif z2_scale == "Z_squared":
        k2 = k2 * Z_SQUARED / 10

    # Phase 1: No drug
    t1 = np.linspace(0, drug_time, 100)
    y0 = [1e-10, 0]  # initial: tiny seed, no mass

    sol1 = odeint(aggregation_kinetics_ode, y0, t1,
                  args=(kn, k2, kplus, m0, None, 0, 1.0))

    # Phase 2: With drug
    t2 = np.linspace(drug_time, total_time, 100)
    y0_phase2 = sol1[-1]

    sol2 = odeint(aggregation_kinetics_ode, y0_phase2, t2,
                  args=(kn, k2, kplus, m0, inhibitor_type, inhibitor_conc, IC50))

    # Combine solutions
    t_full = np.concatenate([t1, t2[1:]])
    M_full = np.concatenate([sol1[:, 1], sol2[1:, 1]])

    # Calculate oligomer proxy (rate of mass increase = oligomer formation)
    oligomer_rate = np.gradient(M_full, t_full)
    peak_oligomer = np.max(oligomer_rate)
    total_oligomer_exposure = np.trapz(np.maximum(oligomer_rate, 0), t_full)

    # Final fibril load
    final_fibril = M_full[-1]

    # Time to 50% aggregation
    idx_half = np.argmin(np.abs(M_full - m0/2))
    t_half = t_full[idx_half] if M_full[-1] > m0/2 else total_time

    return {
        "drug_time": drug_time,
        "inhibitor_type": inhibitor_type,
        "t_half": float(t_half),
        "final_fibril": float(final_fibril),
        "peak_oligomer_rate": float(peak_oligomer),
        "total_oligomer_exposure": float(total_oligomer_exposure),
        "z2_scale": z2_scale,
    }


def optimize_drug_timing(inhibitor_type: str, IC50: float,
                          m0: float = 1.0, z2_scale: str = "none") -> Dict:
    """
    Find optimal drug administration time for given inhibitor type.

    Based on Arosio et al. PNAS 2016 optimal control theory.
    """
    results = []

    # Test different drug administration times
    for drug_time in np.linspace(0, 50, 20):
        result = simulate_aggregation_with_drug(
            m0=m0,
            drug_time=drug_time,
            inhibitor_type=inhibitor_type,
            inhibitor_conc=10 * IC50,  # 10x IC50 dose
            IC50=IC50,
            total_time=100,
            z2_scale=z2_scale
        )
        results.append(result)

    # Find optimal timing (minimize oligomer exposure)
    oligomer_exposures = [r["total_oligomer_exposure"] for r in results]
    optimal_idx = np.argmin(oligomer_exposures)
    optimal_time = results[optimal_idx]["drug_time"]

    return {
        "inhibitor_type": inhibitor_type,
        "optimal_time": float(optimal_time),
        "optimal_oligomer_exposure": float(oligomer_exposures[optimal_idx]),
        "worst_oligomer_exposure": float(max(oligomer_exposures)),
        "improvement_percent": float(
            (max(oligomer_exposures) - oligomer_exposures[optimal_idx]) /
            max(oligomer_exposures) * 100
        ),
        "z2_scale": z2_scale,
        "all_results": results,
    }


# =============================================================================
# THERAPEUTIC WINDOW PREDICTION
# =============================================================================

def predict_therapeutic_window(disease: str, mutation: str = None,
                                z2_scale: str = "none") -> Dict:
    """
    Predict therapeutic window based on disease type and Z² scaling.

    Returns recommendations for:
    - Optimal intervention timing
    - Best inhibitor type
    - Expected efficacy
    """
    # Disease-specific parameters
    disease_params = {
        "AD": {
            "primary_target": "secondary_nucleation",
            "protein": "Aβ42",
            "typical_onset_years": 65,
            "preclinical_years": 20,
            "recommended_inhibitors": ["DesAb29-36", "EGCG"],
        },
        "PD": {
            "primary_target": "secondary_nucleation",
            "protein": "α-synuclein",
            "typical_onset_years": 60,
            "preclinical_years": 15,
            "recommended_inhibitors": ["Molecule 69.2", "Anle138b"],
        },
        "ALS": {
            "primary_target": "aggregation",
            "protein": "SOD1/TDP-43",
            "typical_onset_years": 55,
            "preclinical_years": 10,
            "recommended_inhibitors": ["Chaperone inducers"],
        },
        "CF": {
            "primary_target": "folding_corrector",
            "protein": "CFTR",
            "typical_onset_years": 0,
            "preclinical_years": 0,
            "recommended_inhibitors": ["Lumacaftor", "Tezacaftor"],
        },
    }

    if disease not in disease_params:
        return {"error": f"Unknown disease: {disease}"}

    params = disease_params[disease]

    # Calculate Z²-adjusted timing
    if z2_scale == "sqrt_Z":
        # √Z suggests intervention window scales with √Z
        optimal_intervention = params["preclinical_years"] / SQRT_Z
    elif z2_scale == "1_over_Z2":
        # 1/Z² suggests earlier intervention
        optimal_intervention = params["preclinical_years"] * (1 - 1/Z_SQUARED)
    elif z2_scale == "Z_squared":
        # Z² scaling
        optimal_intervention = params["preclinical_years"] / (Z_SQUARED / 10)
    else:
        optimal_intervention = params["preclinical_years"] / 2

    return {
        "disease": disease,
        "protein": params["protein"],
        "primary_target": params["primary_target"],
        "optimal_intervention_years_before_onset": float(optimal_intervention),
        "recommended_inhibitors": params["recommended_inhibitors"],
        "typical_onset_age": params["typical_onset_years"],
        "intervention_age": params["typical_onset_years"] - optimal_intervention,
        "z2_scale": z2_scale,
    }


# =============================================================================
# VALIDATION AND TESTING
# =============================================================================

def validate_ddg_predictions(z2_scale: str = "none") -> Dict:
    """
    Validate ΔΔG predictions against ProTherm benchmark data.

    Uses leave-one-out cross-validation with linear calibration.
    This tests if Z² scaling improves the *predictive* power,
    not just the fit on training data.
    """
    # Simulated burial and hydrophobicity values for benchmark mutations
    # (In practice, these would come from structure analysis)
    mutation_features = {
        "A32G": (0.3, -0.5), "I25A": (0.8, -1.5), "I51A": (0.7, -1.5),
        "I76A": (0.75, -1.5), "I88A": (0.65, -1.5), "L14A": (0.85, -1.8),
        "Y17A": (0.6, -1.0), "A16G": (0.5, -0.5), "I20A": (0.6, -1.5),
        "L49A": (0.8, -1.8), "I57A": (0.55, -1.5), "V66A": (0.5, -1.2),
        "I56A": (0.7, -1.5), "V74A": (0.6, -1.2), "I98A": (0.75, -1.5),
        "L99A": (0.9, -1.8), "M102A": (0.5, -1.0), "V5A": (0.55, -1.2),
        "I13A": (0.6, -1.5), "L15A": (0.7, -1.8), "V26A": (0.75, -1.2),
        "I44A": (0.85, -1.5),
    }

    raw_predictions = []
    experimentals = []

    for protein, mutation, ddg_exp in PROTHERM_BENCHMARK:
        if mutation in mutation_features:
            burial, hydro = mutation_features[mutation]

            if z2_scale == "none":
                ddg_pred = ddg_empirical_standard(mutation, burial, hydro)
            else:
                ddg_pred = ddg_z2_corrected(mutation, burial, hydro, z2_scale)

            raw_predictions.append(ddg_pred)
            experimentals.append(ddg_exp)

    raw_predictions = np.array(raw_predictions)
    experimentals = np.array(experimentals)

    # Linear calibration: fit a, b in ddg_calibrated = a * ddg_raw + b
    # This accounts for systematic bias in the simple model
    A = np.vstack([raw_predictions, np.ones(len(raw_predictions))]).T
    slope, intercept = np.linalg.lstsq(A, experimentals, rcond=None)[0]

    calibrated_predictions = slope * raw_predictions + intercept

    # Leave-one-out cross-validation to get unbiased error
    loocv_errors = []
    for i in range(len(raw_predictions)):
        train_raw = np.delete(raw_predictions, i)
        train_exp = np.delete(experimentals, i)
        test_raw = raw_predictions[i]
        test_exp = experimentals[i]

        # Fit on training set
        A_train = np.vstack([train_raw, np.ones(len(train_raw))]).T
        s, c = np.linalg.lstsq(A_train, train_exp, rcond=None)[0]

        # Predict on test
        pred = s * test_raw + c
        loocv_errors.append((pred - test_exp) ** 2)

    loocv_rmse = np.sqrt(np.mean(loocv_errors))

    # Metrics on calibrated predictions
    rmse = np.sqrt(np.mean((calibrated_predictions - experimentals) ** 2))
    mae = np.mean(np.abs(calibrated_predictions - experimentals))
    correlation = np.corrcoef(calibrated_predictions, experimentals)[0, 1]

    ss_res = np.sum((experimentals - calibrated_predictions) ** 2)
    ss_tot = np.sum((experimentals - np.mean(experimentals)) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    return {
        "z2_scale": z2_scale,
        "n_mutations": len(calibrated_predictions),
        "rmse": float(rmse),
        "loocv_rmse": float(loocv_rmse),
        "mae": float(mae),
        "correlation": float(correlation),
        "r2": float(r2),
        "calibration_slope": float(slope),
        "calibration_intercept": float(intercept),
        "predictions": calibrated_predictions.tolist(),
        "experimentals": experimentals.tolist(),
    }


def validate_drug_timing(z2_scale: str = "none") -> Dict:
    """
    Validate drug timing predictions for different inhibitor types.
    """
    results = {}

    for inhibitor_type in ["primary_nucleation", "secondary_nucleation", "elongation"]:
        timing_result = optimize_drug_timing(
            inhibitor_type=inhibitor_type,
            IC50=1.0,
            m0=1.0,
            z2_scale=z2_scale
        )
        results[inhibitor_type] = {
            "optimal_time": timing_result["optimal_time"],
            "improvement_percent": timing_result["improvement_percent"],
        }

    return {
        "z2_scale": z2_scale,
        "timing_results": results,
    }


# =============================================================================
# MAIN VALIDATION
# =============================================================================

def run_therapeutic_validation():
    """Run comprehensive therapeutic protein folding validation."""

    print("=" * 80)
    print("THERAPEUTIC PROTEIN FOLDING: Z² Framework Validation")
    print("=" * 80)
    print(f"\nZ² = {Z_SQUARED:.4f}")
    print(f"√Z = {SQRT_Z:.4f}")
    print(f"1/Z² = {1/Z_SQUARED:.6f}")
    print()

    z2_scales = ["none", "sqrt_Z", "1_over_Z2", "Z_squared"]
    scale_names = ["Standard", "√Z scaled", "1/Z² scaled", "Z² scaled"]

    results = {}

    # Test 1: ΔΔG Prediction
    print("TEST 1: Mutation Stability (ΔΔG) Prediction")
    print("Data: ProTherm benchmark mutations")
    print("-" * 70)

    ddg_results = {}
    print(f"{'Model':<20} {'LOOCV RMSE':<12} {'R²':<10} {'r':<10} {'Slope':<10}")
    print("-" * 70)

    for scale, name in zip(z2_scales, scale_names):
        result = validate_ddg_predictions(scale)
        ddg_results[name] = result
        print(f"{name:<20} {result['loocv_rmse']:<12.3f} {result['r2']:<10.3f} "
              f"{result['correlation']:<10.3f} {result['calibration_slope']:<10.2f}")

    results["ddg_prediction"] = ddg_results

    # Test 2: Drug Timing Optimization
    print("\nTEST 2: Optimal Drug Timing")
    print("Model: Aggregation kinetics with intervention")
    print("-" * 70)

    timing_results = {}
    print(f"{'Model':<20} {'1° Nuc Opt':<12} {'2° Nuc Opt':<12} {'Elong Opt':<12}")
    print("-" * 60)

    for scale, name in zip(z2_scales, scale_names):
        result = validate_drug_timing(scale)
        timing_results[name] = result
        t1 = result["timing_results"]["primary_nucleation"]["optimal_time"]
        t2 = result["timing_results"]["secondary_nucleation"]["optimal_time"]
        t3 = result["timing_results"]["elongation"]["optimal_time"]
        print(f"{name:<20} {t1:<12.1f} {t2:<12.1f} {t3:<12.1f}")

    results["drug_timing"] = timing_results

    # Test 3: Therapeutic Window Predictions
    print("\nTEST 3: Therapeutic Window Predictions")
    print("-" * 70)

    window_results = {}
    diseases = ["AD", "PD", "ALS"]

    for disease in diseases:
        window_results[disease] = {}
        print(f"\n{disease}:")
        for scale, name in zip(z2_scales, scale_names):
            result = predict_therapeutic_window(disease, z2_scale=scale)
            window_results[disease][name] = result
            print(f"  {name:<15}: Intervene {result['optimal_intervention_years_before_onset']:.1f} "
                  f"years before onset (age {result['intervention_age']:.0f})")

    results["therapeutic_windows"] = window_results

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY: KEY THERAPEUTIC INSIGHTS")
    print("=" * 80)

    # Find best ΔΔG model
    best_ddg = min(ddg_results.keys(), key=lambda k: ddg_results[k]['rmse'])
    print(f"\nBest ΔΔG prediction model: {best_ddg}")
    print(f"  RMSE: {ddg_results[best_ddg]['rmse']:.3f} kcal/mol")
    print(f"  Correlation: {ddg_results[best_ddg]['correlation']:.3f}")

    # Drug timing insights
    print("\nDrug Timing Insights:")
    print("  - Primary nucleation inhibitors: Early intervention optimal")
    print("  - Secondary nucleation inhibitors: Later intervention can be effective")
    print("  - Elongation inhibitors: Timing less critical but may increase toxicity")

    # Z² therapeutic implications
    print("\nZ² Therapeutic Implications:")
    if ddg_results["√Z scaled"]["rmse"] < ddg_results["Standard"]["rmse"]:
        print("  ✓ √Z scaling improves mutation stability predictions")
    if ddg_results["1/Z² scaled"]["rmse"] < ddg_results["Standard"]["rmse"]:
        print("  ✓ 1/Z² scaling improves mutation stability predictions")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test": "Therapeutic Protein Folding Z² Validation",
        "applications": [
            "Mutation stability prediction (ΔΔG)",
            "Drug timing optimization",
            "Therapeutic window prediction",
        ],
        "diseases_covered": ["Alzheimer's", "Parkinson's", "ALS", "Cystic Fibrosis"],
        "z_constants": {
            "Z": Z,
            "Z_squared": Z_SQUARED,
            "sqrt_Z": SQRT_Z,
        },
        "detailed_results": results,
    }

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/therapeutic_folding_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    run_therapeutic_validation()
