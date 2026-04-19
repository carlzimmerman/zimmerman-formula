#!/usr/bin/env python3
"""
Overnight First-Principles Search: Weinberg Angle θ_W

Target: sin²θ_W = 0.23122 ± 0.00003 (experimental, MS-bar at M_Z)
Current Z² formula: sin²θ_W ≈ 3/13 = 0.2308 (0.2% error)

Questions to answer:
1. Why 3/13? (gauge group ratios?)
2. Can this emerge from grand unification embedding?
3. How does Z² factor in?

Approach:
- Search SU(5), SO(10), E₆ embeddings
- Look for group theory coefficients
- Examine hypercharge normalization

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
SIN2_TW_EXP = 0.23122  # MS-bar scheme at M_Z
SIN2_TW_ON_SHELL = 0.22290  # On-shell scheme

print("="*80)
print("OVERNIGHT SEARCH: First-Principles Derivation of sin²θ_W")
print("="*80)
print(f"Z² = 32π/3 = {Z2:.15f}")
print(f"Experimental sin²θ_W (MS-bar) = {SIN2_TW_EXP}")
print(f"Current approximation 3/13 = {3/13:.10f}")
print(f"Error: {abs(3/13 - SIN2_TW_EXP)/SIN2_TW_EXP * 100:.6f}%")
print("="*80)

# ==============================================================================
# GRAND UNIFICATION PREDICTIONS
# ==============================================================================

GUT_PREDICTIONS = {
    "SU5_tree": 3/8,  # sin²θ_W = 3/8 at GUT scale
    "SU5_low": 0.21,  # After RG running to M_Z
    "SO10_tree": 3/8,
    "E6_tree": 3/8,
    "Pati_Salam": 1/4,  # SU(2)_L × SU(2)_R × SU(4)_C
}

def search_gut_embeddings():
    """Search for sin²θ_W from GUT structure."""
    results = []
    
    # Tree-level GUT prediction
    gut_tree = 3/8
    results.append({
        "formula": "sin²θ_W(GUT) = 3/8",
        "value": gut_tree,
        "target": SIN2_TW_EXP,
        "error_pct": abs(gut_tree - SIN2_TW_EXP) / SIN2_TW_EXP * 100,
        "note": "Tree-level SU(5), SO(10), E₆"
    })
    
    # Test Z²-corrected GUT
    gut_z2_corrected = gut_tree * (1 - 1/Z2)
    results.append({
        "formula": "(3/8) × (1 - 1/Z²)",
        "value": gut_z2_corrected,
        "target": SIN2_TW_EXP,
        "error_pct": abs(gut_z2_corrected - SIN2_TW_EXP) / SIN2_TW_EXP * 100,
    })
    
    # Test: 3/(8 + N_gen) = 3/11
    three_over_11 = 3/11
    results.append({
        "formula": "3/(8 + N_gen) = 3/11",
        "value": three_over_11,
        "target": SIN2_TW_EXP,
        "error_pct": abs(three_over_11 - SIN2_TW_EXP) / SIN2_TW_EXP * 100,
    })
    
    # Test: 3/13 (the current approximation)
    three_over_13 = 3/13
    results.append({
        "formula": "3/13",
        "value": three_over_13,
        "target": SIN2_TW_EXP,
        "error_pct": abs(three_over_13 - SIN2_TW_EXP) / SIN2_TW_EXP * 100,
        "note": "13 = 8 + 3 + 1 + 1 = dim(SU3) + dim(SU2) + 2×dim(U1)?"
    })
    
    # Test: 3/(8 + dim(SU2) + 2) = 3/13
    results.append({
        "formula": "3/(dim(SU3) + dim(SU2) + 2) = 3/(8+3+2)",
        "value": 3/13,
        "interpretation": "Sum of SM gauge group dimensions + 2 (hypercharge normalization)"
    })
    
    return results

# ==============================================================================
# SEARCH: Simple Fractions
# ==============================================================================

def search_simple_fractions():
    """Search for sin²θ_W as simple fractions."""
    results = []
    
    print("\nSearching simple fractions...")
    
    for num in range(1, 20):
        for denom in range(2, 50):
            if np.gcd(num, denom) == 1:  # Reduced fractions only
                val = num / denom
                if 0.15 < val < 0.35:  # Reasonable range
                    error = abs(val - SIN2_TW_EXP) / SIN2_TW_EXP * 100
                    if error < 1:  # Within 1%
                        results.append({
                            "formula": f"{num}/{denom}",
                            "value": val,
                            "error_pct": error,
                            "decimal": f"{val:.10f}"
                        })
    
    results.sort(key=lambda x: x["error_pct"])
    return results[:20]

# ==============================================================================
# SEARCH: Z² Related Formulas
# ==============================================================================

def search_z2_formulas():
    """Search for sin²θ_W involving Z²."""
    results = []
    
    # Form: a/(b×Z² + c)
    for a in range(1, 10):
        for b in range(-3, 4):
            for c in range(-20, 21):
                if b == 0 and c == 0:
                    continue
                denom = b * Z2 + c
                if abs(denom) > 0.1:
                    val = a / denom
                    if 0.15 < val < 0.35:
                        error = abs(val - SIN2_TW_EXP) / SIN2_TW_EXP * 100
                        if error < 0.1:
                            results.append({
                                "formula": f"{a}/({b}×Z² + {c})",
                                "value": val,
                                "error_pct": error
                            })
    
    # Form: a/b - c/Z²
    for a in range(1, 10):
        for b in range(2, 20):
            for c in range(-5, 6):
                if c == 0:
                    continue
                val = a/b - c/Z2
                if 0.15 < val < 0.35:
                    error = abs(val - SIN2_TW_EXP) / SIN2_TW_EXP * 100
                    if error < 0.1:
                        results.append({
                            "formula": f"{a}/{b} - {c}/Z²",
                            "value": val,
                            "error_pct": error
                        })
    
    # Form: (a + b/Z²) / c
    for a in range(0, 5):
        for b in range(-10, 11):
            for c in range(5, 30):
                if b == 0 and a == 0:
                    continue
                val = (a + b/Z2) / c
                if 0.15 < val < 0.35:
                    error = abs(val - SIN2_TW_EXP) / SIN2_TW_EXP * 100
                    if error < 0.1:
                        results.append({
                            "formula": f"({a} + {b}/Z²) / {c}",
                            "value": val,
                            "error_pct": error
                        })
    
    results.sort(key=lambda x: x["error_pct"])
    return results[:30]

# ==============================================================================
# SEARCH: Hypercharge Normalization
# ==============================================================================

def search_hypercharge():
    """
    The Weinberg angle relates to hypercharge normalization.
    
    In SU(5): sin²θ_W = g'²/(g² + g'²) = 3/8 at tree level
    The factor comes from: Tr(Y²) / Tr(T₃²) normalization
    """
    results = []
    
    # Standard hypercharge normalization
    # sin²θ_W = (5/3) × g₁² / (g₂² + (5/3)g₁²)
    # At GUT scale: g₁ = g₂ → sin²θ_W = (5/3)/(1 + 5/3) = 5/8 × 3/5 = 3/8
    
    results.append({
        "formula": "SU(5) normalization: (5/3)/(1 + 5/3) = 3/8",
        "value": 3/8,
        "note": "Tree-level GUT prediction"
    })
    
    # Test: Different normalizations
    for k in [1, 5/3, 2, 3, 4]:
        val = k / (1 + k)
        results.append({
            "formula": f"k/(1+k) with k = {k}",
            "value": val,
            "error_pct": abs(val - SIN2_TW_EXP) / SIN2_TW_EXP * 100
        })
    
    # Test: Weinberg angle from Z² structure
    # If sin²θ_W = 3/(8 + 5) = 3/13, what does 5 represent?
    # 5 could be: dim(SU5 coset), or related to hypercharge
    
    results.append({
        "observation": "13 = 8 + 5 = dim(SU3) + ???",
        "interpretation": "The +5 correction to tree-level 3/8 needs explanation"
    })
    
    return results

# ==============================================================================
# SEARCH: RG Running Connection
# ==============================================================================

def search_rg_running():
    """
    sin²θ_W runs with energy due to RG evolution.
    At GUT scale: 3/8 = 0.375
    At M_Z: ~0.231
    
    Can we derive the running from Z²?
    """
    results = []
    
    # Running from GUT to M_Z
    # Δsin²θ_W ≈ 0.375 - 0.231 = 0.144
    
    delta = 3/8 - SIN2_TW_EXP
    results.append({
        "observation": "RG running Δsin²θ_W",
        "value": delta,
        "ratio_to_tree": delta / (3/8),
        "percent_shift": delta / (3/8) * 100
    })
    
    # Test: Is the shift related to Z²?
    shift_over_z2 = delta / Z2
    results.append({
        "formula": "(3/8 - sin²θ_W) / Z²",
        "value": shift_over_z2,
        "note": "Looking for simple coefficient"
    })
    
    # Test: sin²θ_W = (3/8) × (1 - running_factor)
    running_factor = 1 - SIN2_TW_EXP / (3/8)
    results.append({
        "formula": "sin²θ_W = (3/8) × (1 - f) where f = ",
        "running_factor": running_factor,
        "f_times_Z2": running_factor * Z2
    })
    
    # Test: Does f ≈ 1/Z or some simple form?
    results.append({
        "test": "Is running factor 1/Z?",
        "1/Z": 1/Z,
        "actual_f": running_factor,
        "match": np.isclose(running_factor, 1/Z, rtol=0.1)
    })
    
    return results

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    start_time = time.time()
    
    all_results = {
        "target": "sin²θ_W = 0.23122",
        "Z2": Z2,
        "current_approximation": "3/13",
        "current_value": 3/13,
        "current_error_pct": abs(3/13 - SIN2_TW_EXP) / SIN2_TW_EXP * 100,
        "timestamp": datetime.now().isoformat(),
        "searches": {}
    }
    
    print("\n" + "="*80)
    print("SEARCH 1: GUT Embeddings")
    print("="*80)
    gut_results = search_gut_embeddings()
    for r in gut_results:
        print(f"  {r.get('formula', r.get('observation', 'N/A'))}")
        if 'value' in r:
            print(f"    Value: {r['value']:.10f}")
        if 'error_pct' in r:
            print(f"    Error: {r['error_pct']:.6f}%")
        if 'note' in r:
            print(f"    Note: {r['note']}")
    all_results["searches"]["gut_embeddings"] = gut_results
    
    print("\n" + "="*80)
    print("SEARCH 2: Simple Fractions")
    print("="*80)
    frac_results = search_simple_fractions()
    for r in frac_results[:10]:
        print(f"  {r['formula']}: {r['value']:.10f} (error: {r['error_pct']:.6f}%)")
    all_results["searches"]["simple_fractions"] = frac_results
    
    print("\n" + "="*80)
    print("SEARCH 3: Z² Related Formulas")
    print("="*80)
    z2_results = search_z2_formulas()
    print(f"Found {len(z2_results)} formulas within 0.1% of target")
    for r in z2_results[:15]:
        print(f"  {r['formula']}: {r['value']:.10f} (error: {r['error_pct']:.6f}%)")
    all_results["searches"]["z2_formulas"] = z2_results
    
    print("\n" + "="*80)
    print("SEARCH 4: Hypercharge Normalization")
    print("="*80)
    hyper_results = search_hypercharge()
    for r in hyper_results:
        for k, v in r.items():
            print(f"    {k}: {v}")
        print()
    all_results["searches"]["hypercharge"] = hyper_results
    
    print("\n" + "="*80)
    print("SEARCH 5: RG Running")
    print("="*80)
    rg_results = search_rg_running()
    for r in rg_results:
        for k, v in r.items():
            print(f"    {k}: {v}")
        print()
    all_results["searches"]["rg_running"] = rg_results
    
    # Summary
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    print("""
1. Tree-level GUT prediction: sin²θ_W = 3/8 = 0.375
   - From SU(5), SO(10), E₆ hypercharge normalization
   
2. Current approximation: 3/13 ≈ 0.2308
   - 13 = 8 + 3 + 2 = dim(SU3) + dim(SU2) + 2
   - Or: 13 = 8 + 5 where 5 is related to SU(5) coset
   
3. RG running accounts for tree → low energy evolution
   - Shift of ~0.144 (38% reduction from tree level)
   
4. Z² connection is not yet clear for Weinberg angle
   - Unlike α⁻¹ = 4Z² + 3, no obvious Z² formula here
   - The structure seems more group-theoretic than geometric
""")
    
    elapsed = time.time() - start_time
    all_results["elapsed_seconds"] = elapsed
    
    output_path = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/overnight_results/weinberg_angle_results.json"
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nResults saved to: {output_path}")
    print(f"Search time: {elapsed:.2f} seconds")
    
    return all_results

if __name__ == "__main__":
    main()
