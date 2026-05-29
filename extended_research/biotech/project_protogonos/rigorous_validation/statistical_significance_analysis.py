#!/usr/bin/env python3
"""
================================================================================
STATISTICAL SIGNIFICANCE ANALYSIS: Are the Z² Coincidences Meaningful?
================================================================================

KEY QUESTION: Is finding two length scales (FeS₂ lattice, helix pitch) within
              7% of Z = 5.79 Å actually surprising, or expected by chance?

APPROACH:
  1. Survey all common mineral lattice parameters
  2. Survey all key biological length scales
  3. Calculate the probability of finding N matches within X% of ANY value
  4. Determine if Z is special or if any constant would show similar matches

This is the DECISIVE statistical test.

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Dict, List, Tuple
import json
import os
from scipy import stats

# Z² Constants
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888 Å

# =============================================================================
# COMPREHENSIVE MINERAL DATABASE
# =============================================================================

# Lattice parameters of common minerals (Å)
# Source: AMCSD, Mindat, ICSD databases
MINERAL_LATTICE_PARAMETERS = {
    # Sulfides
    'Pyrite (FeS₂)': 5.417,
    'Galena (PbS)': 5.936,
    'Sphalerite (ZnS)': 5.409,
    'Cinnabar (HgS)': 4.149,
    'Chalcopyrite (CuFeS₂)': 5.289,  # a parameter
    'Pyrrhotite (Fe₇S₈)': 3.446,
    'Molybdenite (MoS₂)': 3.161,
    'Covellite (CuS)': 3.794,
    'Arsenopyrite (FeAsS)': 5.761,
    'Pentlandite ((Fe,Ni)₉S₈)': 10.07,

    # Oxides
    'Quartz (SiO₂)': 4.913,
    'Rutile (TiO₂)': 4.593,
    'Corundum (Al₂O₃)': 4.758,  # a parameter
    'Magnetite (Fe₃O₄)': 8.396,
    'Hematite (Fe₂O₃)': 5.035,  # a parameter
    'Periclase (MgO)': 4.212,
    'Wüstite (FeO)': 4.326,
    'Cuprite (Cu₂O)': 4.267,
    'Cassiterite (SnO₂)': 4.738,
    'Zincite (ZnO)': 3.250,  # a parameter

    # Carbonates
    'Calcite (CaCO₃)': 4.990,  # a parameter
    'Dolomite (CaMg(CO₃)₂)': 4.807,
    'Siderite (FeCO₃)': 4.689,
    'Magnesite (MgCO₃)': 4.633,
    'Rhodochrosite (MnCO₃)': 4.777,
    'Aragonite (CaCO₃)': 4.959,  # a parameter

    # Silicates
    'Olivine (Mg₂SiO₄)': 4.756,  # a parameter
    'Orthopyroxene': 5.238,  # a parameter
    'Feldspar (KAlSi₃O₈)': 8.564,
    'Muscovite': 5.189,  # a parameter
    'Biotite': 5.315,  # a parameter
    'Garnet (Mg₃Al₂Si₃O₁₂)': 11.459,

    # Halides
    'Halite (NaCl)': 5.640,
    'Fluorite (CaF₂)': 5.463,
    'Sylvite (KCl)': 6.293,

    # Phosphates
    'Apatite (Ca₅(PO₄)₃OH)': 9.424,
    'Monazite (CePO₄)': 6.790,

    # Native elements
    'Gold (Au)': 4.078,
    'Silver (Ag)': 4.086,
    'Copper (Cu)': 3.615,
    'Iron (α-Fe)': 2.867,
    'Nickel (Ni)': 3.524,

    # Clays (basal spacing)
    'Montmorillonite': 9.6,  # variable, 9.6-12.3
    'Kaolinite': 7.15,
    'Illite': 10.0,
}

# =============================================================================
# COMPREHENSIVE BIOLOGICAL LENGTH SCALES
# =============================================================================

# Important biological distances (Å)
BIOLOGICAL_LENGTH_SCALES = {
    # Protein structure
    'α-helix pitch': 5.4,
    'α-helix diameter': 12.0,
    'β-sheet strand spacing': 4.7,
    'Residue rise (helix)': 1.5,
    'Residue rise (β-strand)': 3.4,
    'C-C bond length': 1.54,
    'C-N bond length': 1.47,
    'C=O bond length': 1.23,
    'N-H bond length': 1.01,
    'H-bond (N-H...O)': 2.9,
    'van der Waals radius (C)': 1.7,
    'van der Waals radius (N)': 1.55,
    'van der Waals radius (O)': 1.52,

    # DNA/RNA structure
    'B-DNA base pair rise': 3.4,
    'B-DNA helix pitch': 34.0,
    'B-DNA diameter': 20.0,
    'A-DNA base pair rise': 2.6,
    'DNA minor groove width': 5.7,
    'DNA major groove width': 11.7,
    'Base stacking distance': 3.4,

    # Membrane structure
    'Lipid bilayer thickness': 47.0,
    'Headgroup region': 8.5,
    'Hydrocarbon core': 30.0,
    'Lipid lateral spacing': 5.5,
    'Cholesterol length': 17.0,

    # Other key distances
    'ATP length': 16.0,
    'Ribosome diameter': 250.0,
    'Virus capsid (small)': 200.0,
    'Water molecule size': 2.8,
    'π-π stacking (observed)': 3.4,
}

# =============================================================================
# STATISTICAL ANALYSIS FUNCTIONS
# =============================================================================

def count_matches_within_percentage(values: Dict[str, float], target: float, tolerance_pct: float) -> List[str]:
    """Count how many values are within tolerance_pct of target."""
    matches = []
    for name, value in values.items():
        error = abs(value - target) / target * 100
        if error <= tolerance_pct:
            matches.append((name, value, error))
    return matches


def calculate_match_probability(values: Dict[str, float], tolerance_pct: float) -> Dict[str, float]:
    """
    For a randomly chosen target in the range [min, max], what's the probability
    of finding at least N matches within tolerance_pct?

    This tests whether Z is special or if any constant would work.
    """
    all_values = np.array(list(values.values()))
    min_val, max_val = all_values.min(), all_values.max()

    # Monte Carlo: try 10000 random target values
    n_trials = 10000
    np.random.seed(42)
    random_targets = np.random.uniform(min_val * 0.8, max_val * 1.2, n_trials)

    match_counts = []
    for target in random_targets:
        matches = count_matches_within_percentage(values, target, tolerance_pct)
        match_counts.append(len(matches))

    match_counts = np.array(match_counts)

    # Calculate statistics
    results = {
        'mean_matches': np.mean(match_counts),
        'std_matches': np.std(match_counts),
        'max_matches': np.max(match_counts),
        'min_matches': np.min(match_counts),
        'prob_0_matches': np.mean(match_counts == 0),
        'prob_1_match': np.mean(match_counts == 1),
        'prob_2_matches': np.mean(match_counts >= 2),
        'prob_3_matches': np.mean(match_counts >= 3),
    }

    return results


def analyze_z_matches():
    """Analyze matches to Z constant."""

    print("="*70)
    print("STATISTICAL SIGNIFICANCE ANALYSIS")
    print("="*70)
    print(f"\nZ constant: {Z_CONSTANT:.4f} Å")

    # 1. MINERAL ANALYSIS
    print("\n" + "-"*70)
    print("1. MINERAL LATTICE PARAMETERS")
    print("-"*70)

    tolerances = [5, 7, 10, 15]

    for tol in tolerances:
        matches = count_matches_within_percentage(MINERAL_LATTICE_PARAMETERS, Z_CONSTANT, tol)
        print(f"\n  Minerals within {tol}% of Z = {Z_CONSTANT:.3f} Å:")
        if matches:
            for name, value, error in sorted(matches, key=lambda x: x[2]):
                print(f"    {name:30s}: {value:.3f} Å ({error:.1f}% error)")
        else:
            print(f"    None")

    # How special is Z for minerals?
    print(f"\n  Statistical test: How special is Z for minerals?")
    mineral_stats = calculate_match_probability(MINERAL_LATTICE_PARAMETERS, 7)
    print(f"    For a RANDOM target value (7% tolerance):")
    print(f"      Mean matches: {mineral_stats['mean_matches']:.2f}")
    print(f"      P(≥1 match): {1 - mineral_stats['prob_0_matches']:.1%}")
    print(f"      P(≥2 matches): {mineral_stats['prob_2_matches']:.1%}")

    z_mineral_matches = count_matches_within_percentage(MINERAL_LATTICE_PARAMETERS, Z_CONSTANT, 7)
    n_z_matches = len(z_mineral_matches)
    print(f"\n    Z has {n_z_matches} mineral matches within 7%")
    print(f"    This is {'TYPICAL' if n_z_matches <= mineral_stats['mean_matches'] + mineral_stats['std_matches'] else 'UNUSUAL'}")

    # 2. BIOLOGICAL ANALYSIS
    print("\n" + "-"*70)
    print("2. BIOLOGICAL LENGTH SCALES")
    print("-"*70)

    for tol in tolerances:
        matches = count_matches_within_percentage(BIOLOGICAL_LENGTH_SCALES, Z_CONSTANT, tol)
        print(f"\n  Biological scales within {tol}% of Z = {Z_CONSTANT:.3f} Å:")
        if matches:
            for name, value, error in sorted(matches, key=lambda x: x[2]):
                print(f"    {name:30s}: {value:.3f} Å ({error:.1f}% error)")
        else:
            print(f"    None")

    # How special is Z for biology?
    print(f"\n  Statistical test: How special is Z for biology?")
    bio_stats = calculate_match_probability(BIOLOGICAL_LENGTH_SCALES, 7)
    print(f"    For a RANDOM target value (7% tolerance):")
    print(f"      Mean matches: {bio_stats['mean_matches']:.2f}")
    print(f"      P(≥1 match): {1 - bio_stats['prob_0_matches']:.1%}")
    print(f"      P(≥2 matches): {bio_stats['prob_2_matches']:.1%}")

    z_bio_matches = count_matches_within_percentage(BIOLOGICAL_LENGTH_SCALES, Z_CONSTANT, 7)
    n_z_bio = len(z_bio_matches)
    print(f"\n    Z has {n_z_bio} biological matches within 7%")
    print(f"    This is {'TYPICAL' if n_z_bio <= bio_stats['mean_matches'] + bio_stats['std_matches'] else 'UNUSUAL'}")

    # 3. COMBINED ANALYSIS
    print("\n" + "-"*70)
    print("3. COMBINED ANALYSIS: Is Z special?")
    print("-"*70)

    all_scales = {**MINERAL_LATTICE_PARAMETERS, **BIOLOGICAL_LENGTH_SCALES}

    print(f"\n  Total data points: {len(all_scales)}")
    print(f"    Minerals: {len(MINERAL_LATTICE_PARAMETERS)}")
    print(f"    Biological: {len(BIOLOGICAL_LENGTH_SCALES)}")

    all_stats = calculate_match_probability(all_scales, 7)
    z_all_matches = count_matches_within_percentage(all_scales, Z_CONSTANT, 7)

    print(f"\n  For a RANDOM target (7% tolerance):")
    print(f"    Expected matches: {all_stats['mean_matches']:.2f} ± {all_stats['std_matches']:.2f}")
    print(f"    Z actual matches: {len(z_all_matches)}")

    # Z-score
    z_score = (len(z_all_matches) - all_stats['mean_matches']) / all_stats['std_matches']
    p_value = 1 - stats.norm.cdf(z_score) if z_score > 0 else stats.norm.cdf(z_score)

    print(f"\n  Z-score: {z_score:.2f}")
    print(f"  P-value (one-tailed): {p_value:.4f}")

    if p_value < 0.05:
        print(f"\n  ⚠️ RESULT: Z has SIGNIFICANTLY MORE matches than expected by chance (p < 0.05)")
    else:
        print(f"\n  RESULT: Z has a TYPICAL number of matches. Not statistically special.")

    # 4. THE KEY QUESTION
    print("\n" + "-"*70)
    print("4. THE DECISIVE QUESTION")
    print("-"*70)

    print("""
  The claimed Z² matches are:
    1. FeS₂ pyrite: 5.417 Å (6.4% from Z)
    2. α-helix pitch: 5.4 Å (6.7% from Z)

  Question: Is finding 2 matches within 7% of Z surprising?
    """)

    # What's the probability of finding at least 2 matches in BOTH categories?
    mineral_p_1plus = 1 - mineral_stats['prob_0_matches']
    bio_p_1plus = 1 - bio_stats['prob_0_matches']

    # Probability of at least 1 mineral AND at least 1 biological match
    p_both = mineral_p_1plus * bio_p_1plus

    print(f"  P(at least 1 mineral match): {mineral_p_1plus:.1%}")
    print(f"  P(at least 1 biological match): {bio_p_1plus:.1%}")
    print(f"  P(both categories match): {p_both:.1%}")

    if p_both > 0.20:
        conclusion = "EXPECTED BY CHANCE"
        verdict = "NOT SPECIAL"
    elif p_both > 0.05:
        conclusion = "MODERATELY UNLIKELY"
        verdict = "WORTH NOTING"
    else:
        conclusion = "UNLIKELY BY CHANCE"
        verdict = "POTENTIALLY INTERESTING"

    print(f"\n  CONCLUSION: {conclusion}")
    print(f"  VERDICT: Z is {verdict}")

    return {
        'z_constant': Z_CONSTANT,
        'mineral_matches_7pct': len(z_mineral_matches),
        'bio_matches_7pct': len(z_bio_matches),
        'total_matches_7pct': len(z_all_matches),
        'expected_matches': all_stats['mean_matches'],
        'p_value': p_value,
        'p_both_categories': p_both,
        'conclusion': verdict
    }


def find_better_constants():
    """
    Search for constants that match MORE length scales than Z.
    This tests whether Z is special or if we just cherry-picked it.
    """
    print("\n" + "="*70)
    print("5. SEARCHING FOR BETTER CONSTANTS")
    print("="*70)

    all_scales = {**MINERAL_LATTICE_PARAMETERS, **BIOLOGICAL_LENGTH_SCALES}

    # Search for the constant that maximizes matches
    test_values = np.linspace(3.0, 12.0, 1000)
    best_value = Z_CONSTANT
    best_count = 0

    results = []
    for test in test_values:
        matches = count_matches_within_percentage(all_scales, test, 7)
        if len(matches) > best_count:
            best_count = len(matches)
            best_value = test
        results.append((test, len(matches)))

    print(f"\n  Searching values from 3.0 to 12.0 Å...")
    print(f"\n  Best constant found: {best_value:.3f} Å")
    print(f"  Number of matches (7%): {best_count}")
    print(f"\n  Z = {Z_CONSTANT:.3f} Å has {len(count_matches_within_percentage(all_scales, Z_CONSTANT, 7))} matches")

    # Find all "peaks" (local maxima in match count)
    peaks = []
    results_arr = np.array([r[1] for r in results])
    for i in range(1, len(results)-1):
        if results_arr[i] > results_arr[i-1] and results_arr[i] > results_arr[i+1] and results_arr[i] >= 3:
            peaks.append((results[i][0], results[i][1]))

    print(f"\n  Other good constants (≥3 matches within 7%):")
    peaks_sorted = sorted(peaks, key=lambda x: -x[1])[:10]
    for val, count in peaks_sorted:
        z_match = " ← Z!" if abs(val - Z_CONSTANT) < 0.1 else ""
        print(f"    {val:.3f} Å: {count} matches{z_match}")

    if best_value != Z_CONSTANT and abs(best_value - Z_CONSTANT) > 0.5:
        print(f"\n  ⚠️ A BETTER constant exists! Z is not optimal.")
    else:
        print(f"\n  Z is among the best constants for matching length scales.")


def main():
    """Run complete statistical analysis."""

    results = analyze_z_matches()
    find_better_constants()

    # Final summary
    print("\n" + "="*70)
    print("FINAL STATISTICAL SUMMARY")
    print("="*70)

    print(f"""
  Z = {Z_CONSTANT:.4f} Å

  MATCHES FOUND (within 7%):
    - Minerals: {results['mineral_matches_7pct']}
    - Biological: {results['bio_matches_7pct']}
    - Total: {results['total_matches_7pct']}

  STATISTICAL SIGNIFICANCE:
    - Expected matches (random): {results['expected_matches']:.1f}
    - P-value: {results['p_value']:.3f}
    - P(both categories): {results['p_both_categories']:.1%}

  CONCLUSION: {results['conclusion']}

  INTERPRETATION:
    If P > 0.20: The coincidences are EXPECTED by chance. Not meaningful.
    If 0.05 < P < 0.20: Mildly interesting but not significant.
    If P < 0.05: Statistically significant, worth investigating.

  The two claimed matches (FeS₂ and helix pitch) have probability
  {results['p_both_categories']:.1%} of occurring by chance.

  This means: {'THE COINCIDENCES ARE LIKELY RANDOM.' if results['p_both_categories'] > 0.20 else 'THE COINCIDENCES MAY BE MEANINGFUL.' if results['p_both_categories'] < 0.05 else 'THE COINCIDENCES ARE SUGGESTIVE BUT NOT DEFINITIVE.'}
    """)

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'statistical_significance_results.json')

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  Results saved to: {output_file}")


if __name__ == "__main__":
    main()
