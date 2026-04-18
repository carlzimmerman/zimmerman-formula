#!/usr/bin/env python3
"""
VALIDATION: Test Z² Framework on Protein Folding Kinetics

This script validates using actual models from the protein folding field:

1. CONTACT ORDER MODEL (Plaxco, Simons, Baker 1998)
   - log(kf) = a - b × CO
   - Strong negative correlation (~-0.8) between contact order and folding rate

2. SPEED LIMIT MODEL (Kubelka, Hofrichter, Eaton 2004)
   - τ_min ≈ N/100 μs for N-residue protein
   - k_max ≈ 10^8 / N s^-1

3. KRAMERS/EYRING TRANSITION STATE THEORY
   - k = (kT/h) × exp(-ΔG‡/RT)
   - Barrier heights typically 2-20 kcal/mol

4. TWO-STATE FOLDING KINETICS
   - U ⇌ N with rates kf (folding) and ku (unfolding)

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman

Data sources:
- Plaxco et al. J Mol Biol 1998: Contact order correlation
- Kubelka et al. Curr Opin Struct Biol 2004: Speed limit
- Jackson & Fersht 1991: CI2 folding
- Fersht lab: Barnase, CI2, protein L
- Gruebele lab: λ-repressor, WW domain
"""

import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.stats import pearsonr
import json
from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)   # ≈ 5.7888
Z_SQUARED = 32 * np.pi / 3        # ≈ 33.51
SQRT_Z = np.sqrt(Z)               # ≈ 2.406

# Physical constants
R = 8.314      # J/(mol·K)
R_kcal = 1.987e-3  # kcal/(mol·K)
h = 6.626e-34  # J·s
kB = 1.381e-23 # J/K
T_REF = 298.15 # K (25°C)

# =============================================================================
# PUBLISHED PROTEIN FOLDING DATA
# Curated from literature: Plaxco 1998, Fersht lab, Gruebele lab, etc.
# =============================================================================

# Format: (protein_name, length_residues, contact_order, kf_s-1, stability_kcal/mol)
# Contact order from Plaxco et al. 1998, J Mol Biol
# Folding rates from various experimental sources

PROTEIN_FOLDING_DATA = [
    # Two-state folders with published contact order and rates
    # (name, length, relative_contact_order, kf (s^-1), ΔG_folding kcal/mol)

    # Ultrafast folders
    ("Villin headpiece HP35", 35, 0.08, 1.4e6, -3.5),
    ("Trp-cage TC5b", 20, 0.05, 4.0e6, -2.0),
    ("WW domain Pin1", 34, 0.10, 1.3e4, -3.0),
    ("BBA5", 23, 0.07, 1.0e5, -2.5),

    # Fast folders (millisecond)
    ("λ-repressor", 80, 0.12, 3.0e4, -5.0),
    ("CI2", 64, 0.10, 50.0, -7.0),
    ("CI2 R48F mutant", 64, 0.10, 2270.0, -5.5),
    ("Protein L", 64, 0.11, 200.0, -5.0),
    ("Protein G", 56, 0.13, 1500.0, -6.0),
    ("Fyn SH3", 67, 0.14, 94.3, -6.0),
    ("Src SH3", 64, 0.14, 50.0, -4.0),
    ("Spectrin SH3", 62, 0.15, 8.5, -4.5),

    # Moderate folders
    ("Ubiquitin", 76, 0.13, 1500.0, -8.5),
    ("ACBP", 86, 0.11, 1300.0, -6.5),
    ("Cytochrome c", 104, 0.12, 6000.0, -7.0),

    # Slow folders
    ("Barnase", 110, 0.16, 13.0, -10.0),
    ("Barstar", 89, 0.14, 25.0, -5.5),
    ("CheY", 129, 0.18, 3.0, -7.0),
    ("Im7", 87, 0.13, 1000.0, -4.5),
    ("Im9", 86, 0.12, 300.0, -5.0),

    # Very slow folders
    ("Lysozyme", 129, 0.15, 0.5, -9.0),
    ("α-Lactalbumin", 123, 0.17, 0.4, -4.0),
    ("Myoglobin", 153, 0.16, 0.1, -10.0),
]

# Activation energies for select proteins (kcal/mol)
# From temperature-dependent folding studies
ACTIVATION_ENERGIES = {
    "Villin headpiece HP35": 1.5,
    "CI2": 10.0,
    "Protein L": 16.0,
    "Barnase": 18.0,
    "Ubiquitin": 12.0,
    "Cytochrome c": 8.0,
    "λ-repressor": 5.0,
    "Fyn SH3": 14.0,
}

# =============================================================================
# CONTACT ORDER MODEL (Plaxco et al. 1998)
# =============================================================================

def contact_order_model_standard(co: float, a: float, b: float) -> float:
    """
    Standard contact order correlation.

    log10(kf) = a - b × CO

    Plaxco et al. found a ≈ 5.0, b ≈ 15-20 for two-state folders.
    """
    return a - b * co


def contact_order_model_z2(co: float, a: float, b: float, z2_scale: str = "none") -> float:
    """
    Z²-modified contact order model.

    Hypothesis: Z² might modify the contact order coefficient.
    """
    if z2_scale == "Z_squared":
        # Z² scales the contact order effect
        b_mod = b * Z_SQUARED / 10
    elif z2_scale == "sqrt_Z":
        # √Z modification
        b_mod = b * SQRT_Z
    elif z2_scale == "1_over_Z2":
        # 1/Z² modification
        b_mod = b / SQRT_Z
    elif z2_scale == "Z_offset":
        # Z as offset
        a_mod = a + np.log10(Z)
        return a_mod - b * co
    else:
        b_mod = b

    return a - b_mod * co


# =============================================================================
# SPEED LIMIT MODEL (Kubelka et al. 2004)
# =============================================================================

def speed_limit_standard(n_residues: int) -> float:
    """
    Standard protein folding speed limit.

    τ_min ≈ N/100 μs, so k_max ≈ 10^8 / N s^-1

    From Kubelka, Hofrichter, Eaton 2004.
    """
    return 1e8 / n_residues


def speed_limit_z2(n_residues: int, z2_scale: str = "none") -> float:
    """
    Z²-modified speed limit.

    Hypothesis: Z² might appear in the prefactor.
    """
    if z2_scale == "Z_squared":
        # Z² in numerator
        return Z_SQUARED * 1e7 / n_residues
    elif z2_scale == "sqrt_Z":
        # √Z modification
        return SQRT_Z * 1e8 / n_residues
    elif z2_scale == "1_over_Z2":
        # 1/Z² in prefactor
        return 1e8 / (Z_SQUARED * n_residues / 10)
    elif z2_scale == "Z_exponent":
        # Z in exponent scaling
        return 1e8 / (n_residues ** (1/SQRT_Z))
    else:
        return 1e8 / n_residues


# =============================================================================
# KRAMERS/EYRING TRANSITION STATE MODEL
# =============================================================================

def eyring_rate_standard(dg_barrier: float, T: float = T_REF) -> float:
    """
    Eyring transition state theory rate.

    k = (kT/h) × exp(-ΔG‡/RT)

    ΔG‡ in kcal/mol
    """
    prefactor = kB * T / h  # ~6.2 × 10^12 s^-1 at 298 K
    exponent = -dg_barrier / (R_kcal * T)
    return prefactor * np.exp(exponent)


def eyring_rate_z2(dg_barrier: float, T: float = T_REF, z2_scale: str = "none") -> float:
    """
    Z²-modified Eyring rate.

    Hypothesis: Z² might modify the prefactor or barrier.
    """
    prefactor = kB * T / h

    if z2_scale == "Z_squared":
        # Z² modifies barrier
        dg_mod = dg_barrier / Z_SQUARED * 10
    elif z2_scale == "sqrt_Z":
        # √Z modifies barrier
        dg_mod = dg_barrier / SQRT_Z
    elif z2_scale == "1_over_Z2":
        # 1/Z² as prefactor modifier
        prefactor = prefactor / Z_SQUARED
        dg_mod = dg_barrier
    elif z2_scale == "Z_prefactor":
        # Z in prefactor
        prefactor = prefactor * Z
        dg_mod = dg_barrier
    else:
        dg_mod = dg_barrier

    exponent = -dg_mod / (R_kcal * T)
    return prefactor * np.exp(exponent)


# =============================================================================
# COMBINED FOLDING RATE MODEL
# =============================================================================

def combined_folding_rate_standard(n_residues: int, co: float,
                                    a: float = 6.0, b: float = 17.0) -> float:
    """
    Combined model: Contact order with length correction.

    log10(kf) = a - b × CO - c × log10(N)

    Incorporates both topology and size effects.
    """
    log_kf = a - b * co - 0.5 * np.log10(n_residues)
    return 10 ** log_kf


def combined_folding_rate_z2(n_residues: int, co: float,
                              a: float = 6.0, b: float = 17.0,
                              z2_scale: str = "none") -> float:
    """
    Z²-modified combined model.
    """
    if z2_scale == "Z_squared":
        b_mod = b / SQRT_Z
        c_mod = 0.5 / SQRT_Z
    elif z2_scale == "sqrt_Z":
        b_mod = b * SQRT_Z / 2
        c_mod = 0.5
    elif z2_scale == "1_over_Z2":
        b_mod = b * (1 + 1/Z_SQUARED)
        c_mod = 0.5 * (1 + 1/Z_SQUARED)
    elif z2_scale == "Z_offset":
        a_mod = a + np.log10(Z_SQUARED) / 2
        log_kf = a_mod - b * co - 0.5 * np.log10(n_residues)
        return 10 ** log_kf
    else:
        b_mod = b
        c_mod = 0.5

    log_kf = a - b_mod * co - c_mod * np.log10(n_residues)
    return 10 ** log_kf


# =============================================================================
# FITTING AND VALIDATION
# =============================================================================

def fit_contact_order_model(data: List[Tuple], z2_scale: str = "none") -> Dict:
    """Fit contact order model to folding rate data."""

    cos = np.array([d[2] for d in data])
    log_kfs = np.log10(np.array([d[3] for d in data]))

    # Grid search for optimal a, b
    best_rmse = float('inf')
    best_params = {"a": 6.0, "b": 17.0}

    for a in np.linspace(4.0, 8.0, 40):
        for b in np.linspace(10.0, 30.0, 40):
            if z2_scale == "none":
                pred = np.array([contact_order_model_standard(co, a, b) for co in cos])
            else:
                pred = np.array([contact_order_model_z2(co, a, b, z2_scale) for co in cos])

            rmse = np.sqrt(np.mean((pred - log_kfs)**2))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = {"a": a, "b": b}

    # Get predictions with best parameters
    a, b = best_params["a"], best_params["b"]
    if z2_scale == "none":
        pred = np.array([contact_order_model_standard(co, a, b) for co in cos])
    else:
        pred = np.array([contact_order_model_z2(co, a, b, z2_scale) for co in cos])

    # Correlation coefficient
    r, p_value = pearsonr(pred, log_kfs)

    # Metrics
    rmse = np.sqrt(np.mean((pred - log_kfs)**2))
    ss_res = np.sum((log_kfs - pred)**2)
    ss_tot = np.sum((log_kfs - np.mean(log_kfs))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_a": float(best_params["a"]),
        "best_b": float(best_params["b"]),
        "predictions": pred.tolist(),
        "experimental": log_kfs.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
        "correlation": float(r),
        "p_value": float(p_value),
    }


def fit_speed_limit_model(data: List[Tuple], z2_scale: str = "none") -> Dict:
    """Compare folding rates to speed limit predictions."""

    lengths = np.array([d[1] for d in data])
    kfs = np.array([d[3] for d in data])

    # Calculate speed limits
    if z2_scale == "none":
        k_max = np.array([speed_limit_standard(n) for n in lengths])
    else:
        k_max = np.array([speed_limit_z2(n, z2_scale) for n in lengths])

    # Ratio of actual rate to speed limit
    ratios = kfs / k_max

    # How many proteins are within 10x of speed limit?
    near_limit = np.sum(ratios > 0.1)

    # Log-space correlation
    log_kf = np.log10(kfs)
    log_kmax = np.log10(k_max)

    r, p_value = pearsonr(log_kf, log_kmax)

    # RMSE in log space
    rmse = np.sqrt(np.mean((log_kf - log_kmax)**2))

    return {
        "z2_scale": z2_scale,
        "log_kf": log_kf.tolist(),
        "log_kmax": log_kmax.tolist(),
        "ratios": ratios.tolist(),
        "near_limit_count": int(near_limit),
        "correlation": float(r),
        "rmse_log": float(rmse),
    }


def fit_eyring_model(data: Dict, z2_scale: str = "none") -> Dict:
    """Fit Eyring model to proteins with known activation energies."""

    proteins = []
    for name, ea in data.items():
        # Find protein in main data
        for p in PROTEIN_FOLDING_DATA:
            if p[0] == name:
                proteins.append((name, p[3], ea))
                break

    if len(proteins) < 3:
        return {"error": "Not enough proteins with activation energy data"}

    kf_exp = np.array([p[1] for p in proteins])
    eas = np.array([p[2] for p in proteins])

    # Calculate predicted rates from Eyring
    if z2_scale == "none":
        kf_pred = np.array([eyring_rate_standard(ea) for ea in eas])
    else:
        kf_pred = np.array([eyring_rate_z2(ea, z2_scale=z2_scale) for ea in eas])

    # Log-space comparison
    log_exp = np.log10(kf_exp)
    log_pred = np.log10(kf_pred)

    r, p_value = pearsonr(log_exp, log_pred)
    rmse = np.sqrt(np.mean((log_exp - log_pred)**2))

    return {
        "z2_scale": z2_scale,
        "proteins": [p[0] for p in proteins],
        "log_kf_exp": log_exp.tolist(),
        "log_kf_pred": log_pred.tolist(),
        "correlation": float(r),
        "rmse_log": float(rmse),
    }


def fit_combined_model(data: List[Tuple], z2_scale: str = "none") -> Dict:
    """Fit combined contact order + length model."""

    lengths = np.array([d[1] for d in data])
    cos = np.array([d[2] for d in data])
    log_kfs = np.log10(np.array([d[3] for d in data]))

    # Grid search
    best_rmse = float('inf')
    best_params = {"a": 6.0, "b": 17.0}

    for a in np.linspace(5.0, 9.0, 40):
        for b in np.linspace(10.0, 25.0, 40):
            if z2_scale == "none":
                pred = np.array([
                    np.log10(combined_folding_rate_standard(n, co, a, b))
                    for n, co in zip(lengths, cos)
                ])
            else:
                pred = np.array([
                    np.log10(combined_folding_rate_z2(n, co, a, b, z2_scale))
                    for n, co in zip(lengths, cos)
                ])

            rmse = np.sqrt(np.mean((pred - log_kfs)**2))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = {"a": a, "b": b}

    # Get predictions
    a, b = best_params["a"], best_params["b"]
    if z2_scale == "none":
        pred = np.array([
            np.log10(combined_folding_rate_standard(n, co, a, b))
            for n, co in zip(lengths, cos)
        ])
    else:
        pred = np.array([
            np.log10(combined_folding_rate_z2(n, co, a, b, z2_scale))
            for n, co in zip(lengths, cos)
        ])

    r, p_value = pearsonr(pred, log_kfs)
    rmse = np.sqrt(np.mean((pred - log_kfs)**2))
    ss_res = np.sum((log_kfs - pred)**2)
    ss_tot = np.sum((log_kfs - np.mean(log_kfs))**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    return {
        "z2_scale": z2_scale,
        "best_a": float(best_params["a"]),
        "best_b": float(best_params["b"]),
        "predictions": pred.tolist(),
        "experimental": log_kfs.tolist(),
        "rmse": float(rmse),
        "r2": float(r2),
        "correlation": float(r),
    }


# =============================================================================
# MAIN VALIDATION
# =============================================================================

def run_validation():
    """Run comprehensive validation on protein folding data."""

    print("=" * 80)
    print("VALIDATION: Protein Folding Z² Using REAL Scientific Models")
    print("=" * 80)
    print(f"\nZ² = {Z_SQUARED:.4f}")
    print(f"√Z = {SQRT_Z:.4f}")
    print(f"1/Z² = {1/Z_SQUARED:.6f}")
    print(f"\nProteins in dataset: {len(PROTEIN_FOLDING_DATA)}")
    print()

    z2_scales = ["none", "Z_squared", "sqrt_Z", "1_over_Z2", "Z_offset"]
    scale_names = ["Standard", "Z² scaled", "√Z scaled", "1/Z² scaled", "Z offset"]

    results = {}

    # Test 1: Contact Order Model (Plaxco et al.)
    print("TEST 1: Contact Order Correlation (Plaxco et al. 1998)")
    print("Model: log10(kf) = a - b × CO")
    print("-" * 70)

    co_results = {}
    print(f"{'Model':<20} {'RMSE':<10} {'R²':<10} {'r':<10}")
    print("-" * 50)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_contact_order_model(PROTEIN_FOLDING_DATA, scale)
        co_results[name] = result
        print(f"{name:<20} {result['rmse']:<10.3f} {result['r2']:<10.4f} {result['correlation']:<10.3f}")

    results["contact_order"] = co_results

    # Test 2: Speed Limit Model (Kubelka et al.)
    print("\nTEST 2: Speed Limit Comparison (Kubelka et al. 2004)")
    print("Model: k_max = 10^8 / N  s^-1")
    print("-" * 70)

    sl_results = {}
    print(f"{'Model':<20} {'RMSE(log)':<12} {'r':<10} {'Near limit':<12}")
    print("-" * 55)

    for scale, name in zip(z2_scales[:4], scale_names[:4]):  # Skip Z_offset for speed limit
        result = fit_speed_limit_model(PROTEIN_FOLDING_DATA, scale)
        sl_results[name] = result
        print(f"{name:<20} {result['rmse_log']:<12.2f} {result['correlation']:<10.3f} {result['near_limit_count']:<12}")

    results["speed_limit"] = sl_results

    # Test 3: Eyring Transition State Model
    print("\nTEST 3: Eyring/Arrhenius Model")
    print("Model: k = (kT/h) × exp(-Ea/RT)")
    print("-" * 70)

    ey_results = {}
    print(f"{'Model':<20} {'RMSE(log)':<12} {'r':<10}")
    print("-" * 42)

    for scale, name in zip(z2_scales[:4], scale_names[:4]):
        result = fit_eyring_model(ACTIVATION_ENERGIES, scale)
        if "error" not in result:
            ey_results[name] = result
            print(f"{name:<20} {result['rmse_log']:<12.2f} {result['correlation']:<10.3f}")

    results["eyring"] = ey_results

    # Test 4: Combined Model (CO + Length)
    print("\nTEST 4: Combined Model (Contact Order + Length)")
    print("Model: log10(kf) = a - b×CO - c×log10(N)")
    print("-" * 70)

    comb_results = {}
    print(f"{'Model':<20} {'RMSE':<10} {'R²':<10} {'r':<10}")
    print("-" * 50)

    for scale, name in zip(z2_scales, scale_names):
        result = fit_combined_model(PROTEIN_FOLDING_DATA, scale)
        comb_results[name] = result
        print(f"{name:<20} {result['rmse']:<10.3f} {result['r2']:<10.4f} {result['correlation']:<10.3f}")

    results["combined"] = comb_results

    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    tests = ["contact_order", "combined"]
    test_names = ["Contact Order", "Combined Model"]

    z2_wins = 0
    standard_wins = 0

    print(f"\n{'Test':<25} {'Best Model':<20} {'Improvement':<15}")
    print("-" * 60)

    for test, test_name in zip(tests, test_names):
        test_results = results[test]
        standard_rmse = test_results["Standard"]["rmse"]

        best_model = "Standard"
        best_rmse = standard_rmse

        for name in scale_names[1:]:
            if name in test_results and test_results[name]["rmse"] < best_rmse - 0.001:
                best_rmse = test_results[name]["rmse"]
                best_model = name

        if best_model == "Standard":
            standard_wins += 1
            improvement = "0%"
        else:
            z2_wins += 1
            improvement = f"{(standard_rmse - best_rmse) / standard_rmse * 100:.1f}%"

        print(f"{test_name:<25} {best_model:<20} {improvement:<15}")

    # Check speed limit and Eyring separately (different metric)
    print("\nAdditional Tests:")

    if results["speed_limit"]["Standard"]["rmse_log"] > results["speed_limit"].get("Z² scaled", {}).get("rmse_log", float('inf')):
        print("  Speed Limit: Z² variants show improvement")
        z2_wins += 1
    else:
        print("  Speed Limit: Standard model better")
        standard_wins += 1

    if "Standard" in results["eyring"] and "√Z scaled" in results["eyring"]:
        if results["eyring"]["Standard"]["rmse_log"] > results["eyring"]["√Z scaled"]["rmse_log"]:
            print("  Eyring Model: Z² variants show improvement")
            z2_wins += 1
        else:
            print("  Eyring Model: Standard model better")
            standard_wins += 1

    print(f"\nZ² variants better: {z2_wins}/4 tests")
    print(f"Standard better: {standard_wins}/4 tests")

    # Honest assessment
    print("\n" + "=" * 80)
    print("HONEST ASSESSMENT")
    print("=" * 80)

    if z2_wins > standard_wins:
        print("\n✅ VALIDATED: Z² improves protein folding predictions")
        conclusion = "VALIDATED"
    elif z2_wins == standard_wins:
        print("\n⚠️  PARTIAL: Z² shows mixed results")
        print("   Standard models already capture topology-rate correlation well")
        conclusion = "PARTIAL"
    else:
        print("\n❌ NOT VALIDATED: Standard models are better")
        print("   Contact order correlation is already well-established")
        print("   Plaxco et al. (1998) model is robust")
        conclusion = "NOT_VALIDATED"

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test": "Protein Folding Z² Validation",
        "models_used": {
            "contact_order": "Plaxco et al. J Mol Biol 1998",
            "speed_limit": "Kubelka et al. Curr Opin Struct Biol 2004",
            "eyring": "Transition state theory (Eyring 1935)",
            "combined": "Contact order + chain length",
        },
        "data_sources": {
            "proteins": f"{len(PROTEIN_FOLDING_DATA)} two-state folders",
            "references": "Plaxco 1998, Fersht lab, Gruebele lab, Baker lab",
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

    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/protein_folding_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    run_validation()
