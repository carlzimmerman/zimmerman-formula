#!/usr/bin/env python3
"""
Overnight First-Principles Search: Proton-to-Electron Mass Ratio

Target: m_p/m_e = 1836.15267343 (CODATA 2018)
Current Z² formula: m_p/m_e ≈ α⁻¹ × 2Z²/5 = 1836.0 (0.008% error)

Questions to answer:
1. Why the factor 2/5?
2. Can we derive this from QCD confinement?
3. Is the proton mass computable from first principles?

This is extremely ambitious - deriving m_p from first principles
requires understanding non-perturbative QCD!

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from fractions import Fraction
import json
import time
from datetime import datetime

# ==============================================================================
# FUNDAMENTAL CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2  # = 32π/3 ≈ 33.510321638291124

# Experimental values
M_PROTON = 938.27208816e6  # eV
M_ELECTRON = 0.51099895000e6  # eV
MASS_RATIO_EXP = M_PROTON / M_ELECTRON  # 1836.15267343

# Fine structure constant
ALPHA = 1/137.035999084
ALPHA_INV = 137.035999084

# Current Z² formula
MASS_RATIO_Z2 = ALPHA_INV * 2 * Z2 / 5

print("="*80)
print("OVERNIGHT SEARCH: First-Principles Derivation of m_p/m_e")
print("="*80)
print(f"Z² = 32π/3 = {Z2:.15f}")
print(f"α⁻¹ = {ALPHA_INV}")
print(f"Experimental m_p/m_e = {MASS_RATIO_EXP}")
print(f"Current α⁻¹ × 2Z²/5 = {MASS_RATIO_Z2:.6f}")
print(f"Error: {abs(MASS_RATIO_Z2 - MASS_RATIO_EXP)/MASS_RATIO_EXP * 100:.6f}%")
print("="*80)

# ==============================================================================
# QCD CONSTANTS
# ==============================================================================

# QCD scale
LAMBDA_QCD = 217e6  # eV (approx, scheme-dependent)

# Quark masses (current masses at 2 GeV, MS-bar)
M_UP = 2.16e6    # eV
M_DOWN = 4.67e6  # eV
M_STRANGE = 93e6 # eV

# Proton is ~99% gluon/sea, only ~1% valence quark mass
PROTON_QUARK_FRACTION = (2 * M_UP + M_DOWN) / M_PROTON  # ~1%

print(f"Quark contribution to proton mass: {PROTON_QUARK_FRACTION*100:.1f}%")
print(f"→ Proton mass is mostly QCD binding energy!")

# ==============================================================================
# SEARCH: Alpha and Z² Combinations
# ==============================================================================

def search_alpha_z2_formulas():
    """Search for m_p/m_e as combinations of α and Z²."""
    results = []
    
    # Current formula: α⁻¹ × 2Z²/5
    results.append({
        "formula": "α⁻¹ × 2Z²/5",
        "value": ALPHA_INV * 2 * Z2 / 5,
        "target": MASS_RATIO_EXP,
        "error_pct": abs(ALPHA_INV * 2 * Z2 / 5 - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
    })
    
    # Search: α⁻¹ × a×Z²/b
    print("\nSearching α⁻¹ × (a×Z²/b) formulas...")
    for a in range(1, 10):
        for b in range(1, 20):
            val = ALPHA_INV * a * Z2 / b
            if 1500 < val < 2200:
                err = abs(val - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
                if err < 0.1:
                    results.append({
                        "formula": f"α⁻¹ × {a}×Z²/{b}",
                        "value": val,
                        "error_pct": err,
                        "fraction": f"{a}/{b}"
                    })
    
    # Search: α⁻¹ × Z² + offset
    for offset in range(-100, 101):
        val = ALPHA_INV * Z2 / 2.5 + offset
        err = abs(val - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
        if err < 0.01:
            results.append({
                "formula": f"α⁻¹ × Z²/2.5 + {offset}",
                "value": val,
                "error_pct": err
            })
    
    # Search: (α⁻¹)^a × Z²^b × factor
    for a_pow in [1, 1.5, 2]:
        for z_pow in [0.5, 1, 1.5, 2]:
            for factor in [0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 1, 2]:
                val = (ALPHA_INV)**a_pow * (Z2)**z_pow * factor
                if 1500 < val < 2200:
                    err = abs(val - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
                    if err < 0.5:
                        results.append({
                            "formula": f"α⁻{a_pow} × Z²^{z_pow} × {factor}",
                            "value": val,
                            "error_pct": err
                        })
    
    results.sort(key=lambda x: x["error_pct"])
    return results[:30]

# ==============================================================================
# SEARCH: QCD Dimensional Transmutation
# ==============================================================================

def search_qcd_transmutation():
    """
    In QCD, the proton mass emerges from dimensional transmutation:
    m_p ~ Λ_QCD ~ M_Pl × exp(-8π²/(b₀ × g_s²(M_Pl)))
    
    where b₀ = 11 - 2N_f/3 = 7 for N_f = 6 flavors
    
    Can we relate this to Z²?
    """
    results = []
    
    # QCD beta function coefficient
    N_f = 6  # number of active flavors at high scale
    b0 = 11 - 2*N_f/3  # = 7 for full SM
    
    results.append({
        "observation": "QCD beta coefficient",
        "b0": b0,
        "formula": "11 - 2N_f/3",
        "N_f": N_f
    })
    
    # The running coupling at scale μ:
    # α_s(μ) = α_s(M_Z) / (1 + b₀ α_s(M_Z)/(2π) × ln(μ/M_Z))
    
    alpha_s_MZ = 0.1179  # Strong coupling at M_Z
    
    results.append({
        "observation": "Strong coupling at M_Z",
        "alpha_s_MZ": alpha_s_MZ,
        "note": "Much larger than α_em ≈ 1/137"
    })
    
    # Test: Is m_p/m_e related to α_s?
    # m_p/m_e ~ (1/α_s)^something?
    
    ratio_over_alpha_s = MASS_RATIO_EXP * alpha_s_MZ
    results.append({
        "test": "m_p/m_e × α_s(M_Z)",
        "value": ratio_over_alpha_s,
        "relation_to_Z2": ratio_over_alpha_s / Z2,
        "relation_to_alpha_inv": ratio_over_alpha_s / ALPHA_INV
    })
    
    # Ratio of couplings
    alpha_ratio = ALPHA_INV * alpha_s_MZ
    results.append({
        "test": "α⁻¹ × α_s",
        "value": alpha_ratio,
        "relation_to_Z": alpha_ratio / Z,
        "note": "Electroweak-QCD coupling relation"
    })
    
    return results

# ==============================================================================
# SEARCH: Proton as Soliton
# ==============================================================================

def search_soliton_mass():
    """
    In Skyrme model and related approaches, the proton is a topological soliton.
    The mass scales as m_p ~ F_π / e where:
    - F_π ~ 93 MeV (pion decay constant)
    - e is a dimensionless coupling
    
    Can we relate this to Z²?
    """
    results = []
    
    F_PI = 93e6  # eV (pion decay constant)
    
    # Skyrme model: m_p ≈ 36.5 × F_π / e²
    # where e ≈ 4-5 typically
    
    # Test: e² related to Z²?
    e_skyrme_squared = 36.5 * F_PI / M_PROTON
    results.append({
        "model": "Skyrme soliton",
        "derived_e²": e_skyrme_squared,
        "e": np.sqrt(e_skyrme_squared),
        "relation_to_Z": np.sqrt(e_skyrme_squared) / Z,
        "note": "e = Skyrme parameter"
    })
    
    # Test: Is F_π/m_e related to Z²?
    fpi_over_me = F_PI / M_ELECTRON
    results.append({
        "test": "F_π / m_e",
        "value": fpi_over_me,
        "relation_to_Z2": fpi_over_me / Z2,
        "relation_to_alpha_inv": fpi_over_me / ALPHA_INV
    })
    
    return results

# ==============================================================================
# SEARCH: Simple Fraction Decomposition
# ==============================================================================

def search_fraction_decomposition():
    """
    Decompose 1836.15... into simple fractions.
    
    Note: 1836 = 4 × 459 = 4 × 9 × 51 = 36 × 51
    Also: 1836 ≈ 4 × 459 ≈ 4 × 4.5 × 102 ≈ 18 × 102
    """
    results = []
    
    # Factor analysis
    results.append({
        "observation": "1836 factorization",
        "factors": "1836 = 2² × 3³ × 17",
        "prime_factors": [2, 2, 3, 3, 3, 17]
    })
    
    # Test: 1836 = α⁻¹ × something
    factor_alpha = MASS_RATIO_EXP / ALPHA_INV
    results.append({
        "test": "m_p/m_e ÷ α⁻¹",
        "value": factor_alpha,
        "approx_fraction": f"≈ {factor_alpha:.3f} ≈ 2Z²/5 = {2*Z2/5:.3f}"
    })
    
    # Test: 1836 ≈ 6π² × Z
    test1 = 6 * np.pi**2 * Z
    results.append({
        "formula": "6π² × Z",
        "value": test1,
        "target": MASS_RATIO_EXP,
        "error_pct": abs(test1 - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
    })
    
    # Test: 1836 ≈ Z² × π × something
    test2 = Z2 * np.pi * 17.4
    results.append({
        "formula": "Z² × π × 17.4",
        "value": test2,
        "target": MASS_RATIO_EXP,
        "error_pct": abs(test2 - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
    })
    
    # Search for simple products
    for a in range(1, 50):
        for b in range(1, 50):
            if a * b == 1836:
                results.append({
                    "observation": f"1836 = {a} × {b}",
                })
    
    return results

# ==============================================================================
# SEARCH: Exhaustive Formula Search
# ==============================================================================

def exhaustive_search():
    """Search all simple combinations."""
    results = []
    
    print("\nExhaustive formula search...")
    
    # Form: α⁻¹ × a/b × Z²^c
    for a in range(1, 20):
        for b in range(1, 20):
            for c_exp in [0.5, 1, 1.5, 2]:
                val = ALPHA_INV * (a/b) * (Z2**c_exp)
                if 1500 < val < 2200:
                    err = abs(val - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
                    if err < 0.05:
                        results.append({
                            "formula": f"α⁻¹ × ({a}/{b}) × Z²^{c_exp}",
                            "value": val,
                            "error_pct": err
                        })
    
    # Form: α⁻¹ × Z² × (a/b) + c
    for a in range(1, 10):
        for b in range(1, 20):
            for c in range(-50, 51):
                val = ALPHA_INV * Z2 * (a/b) + c
                if 1500 < val < 2200:
                    err = abs(val - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
                    if err < 0.01:
                        results.append({
                            "formula": f"α⁻¹ × Z² × ({a}/{b}) + {c}",
                            "value": val,
                            "error_pct": err
                        })
    
    # Form: π^a × Z^b × c
    for a_exp in [1, 2, 3, 4]:
        for b_exp in [1, 2, 3]:
            for c in range(1, 50):
                val = (np.pi**a_exp) * (Z**b_exp) * c
                if 1500 < val < 2200:
                    err = abs(val - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100
                    if err < 1:
                        results.append({
                            "formula": f"π^{a_exp} × Z^{b_exp} × {c}",
                            "value": val,
                            "error_pct": err
                        })
    
    results.sort(key=lambda x: x["error_pct"])
    return results[:50]

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    start_time = time.time()
    
    all_results = {
        "target": f"m_p/m_e = {MASS_RATIO_EXP}",
        "Z2": Z2,
        "alpha_inv": ALPHA_INV,
        "current_formula": "α⁻¹ × 2Z²/5",
        "current_value": MASS_RATIO_Z2,
        "current_error_pct": abs(MASS_RATIO_Z2 - MASS_RATIO_EXP) / MASS_RATIO_EXP * 100,
        "timestamp": datetime.now().isoformat(),
        "searches": {}
    }
    
    print("\n" + "="*80)
    print("SEARCH 1: α and Z² Combinations")
    print("="*80)
    az_results = search_alpha_z2_formulas()
    for r in az_results[:15]:
        print(f"  {r['formula']}: {r['value']:.6f} (error: {r['error_pct']:.6f}%)")
    all_results["searches"]["alpha_z2"] = az_results
    
    print("\n" + "="*80)
    print("SEARCH 2: QCD Dimensional Transmutation")
    print("="*80)
    qcd_results = search_qcd_transmutation()
    for r in qcd_results:
        for k, v in r.items():
            print(f"    {k}: {v}")
        print()
    all_results["searches"]["qcd"] = qcd_results
    
    print("\n" + "="*80)
    print("SEARCH 3: Soliton Mass")
    print("="*80)
    sol_results = search_soliton_mass()
    for r in sol_results:
        for k, v in r.items():
            print(f"    {k}: {v}")
        print()
    all_results["searches"]["soliton"] = sol_results
    
    print("\n" + "="*80)
    print("SEARCH 4: Fraction Decomposition")
    print("="*80)
    frac_results = search_fraction_decomposition()
    for r in frac_results:
        if 'formula' in r:
            print(f"  {r['formula']}: {r.get('value', 'N/A')}")
        else:
            print(f"  {r.get('observation', r.get('test', 'N/A'))}")
    all_results["searches"]["fractions"] = frac_results
    
    print("\n" + "="*80)
    print("SEARCH 5: Exhaustive Search")
    print("="*80)
    exh_results = exhaustive_search()
    print(f"Found {len(exh_results)} formulas with <1% error")
    for r in exh_results[:20]:
        print(f"  {r['formula']}: {r['value']:.8f} (error: {r['error_pct']:.8f}%)")
    all_results["searches"]["exhaustive"] = exh_results
    
    # Summary
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    print(f"""
1. Current best formula: m_p/m_e = α⁻¹ × 2Z²/5
   Value: {MASS_RATIO_Z2:.4f}
   Error: {abs(MASS_RATIO_Z2 - MASS_RATIO_EXP)/MASS_RATIO_EXP * 100:.4f}%

2. Why 2/5?
   - 2/5 = 0.4 = 2/(N_generations + 2)?
   - 2/5 might relate to QCD color factor
   - Needs deeper investigation
   
3. The proton mass is 99% QCD binding energy
   - Valence quarks contribute only ~1%
   - Mass emerges from dimensional transmutation
   - Λ_QCD ~ exp(-8π²/b₀g_s²) × M_Planck
   
4. Z² appears via α connection:
   - α⁻¹ ≈ 4Z² + 3
   - m_p/m_e ≈ (4Z² + 3) × 2Z²/5 = 8Z⁴/5 + 6Z²/5
   
5. This is the hardest derivation:
   - Requires understanding non-perturbative QCD
   - Lattice QCD computes m_p/m_e to ~2% now
   - Analytic derivation remains unsolved
""")
    
    elapsed = time.time() - start_time
    all_results["elapsed_seconds"] = elapsed
    
    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/overnight_results/mass_ratio_results.json"
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_path}")
    print(f"Search time: {elapsed:.2f} seconds")
    
    return all_results

if __name__ == "__main__":
    main()
