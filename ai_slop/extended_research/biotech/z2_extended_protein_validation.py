#!/usr/bin/env python3
"""
Z² Extended Protein Validation

Test Z² relationships against a broader set of proteins from UniProt.
This includes:
1. Additional target system proteins
2. Non-target system proteins (controls)
3. Random sample to test if pattern is universal or specific

Copyright (C) 2026 Carl Zimmerman
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
from typing import Dict, List, Tuple
import json
from pathlib import Path

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)
Z_SQUARED = 32 * np.pi / 3
THETA_Z2_DEG = np.degrees(np.pi / Z)
PHI_GOLDEN = (1 + np.sqrt(5)) / 2

# =============================================================================
# EXTENDED PROTEIN DATABASE
# =============================================================================

# All lengths from UniProt canonical sequences

# target system proteins (neurodegenerative)
DISEASE_PROTEINS = {
    # Alzheimer's
    "APP": 770,
    "PSEN1": 467,
    "PSEN2": 448,
    "MAPT_4R": 441,  # Tau
    "APOE": 317,
    "TREM2": 230,
    "CLU": 449,
    "ABCA7": 2146,

    # Parkinson's
    "SNCA": 140,  # alpha-synuclein
    "LRRK2": 2527,
    "PARK7": 189,  # DJ-1
    "PINK1": 581,
    "PRKN": 465,  # Parkin
    "GBA": 536,
    "VPS35": 796,

    # Huntington's / PolyQ
    "HTT": 3144,
    "ATXN1": 815,  # SCA1
    "ATXN2": 1313,  # SCA2
    "ATXN3": 376,   # SCA3
    "CACNA1A": 2505,  # SCA6
    "ATXN7": 892,   # SCA7
    "ATN1": 1190,   # DRPLA
    "AR": 919,      # SBMA

    # ALS
    "SOD1": 153,
    "TARDBP": 414,  # TDP-43
    "FUS": 526,
    "C9orf72": 481,
    "OPTN": 577,
    "VCP": 806,
    "UBQLN2": 624,
    "ANG": 147,

    # Prion
    "PRNP": 253,

    # MS-related
    "MBP": 170,  # Classic isoform
    "PLP1": 276,
    "MOG": 247,
    "MAG": 626,

    # Other neurodegeneration
    "ATXN10": 475,  # SCA10
    "PPP2R2B": 443,  # SCA12
    "KCND3": 654,   # SCA19
    "FXN": 210,     # Friedreich's
}

# Control proteins (essential, non-target system)
CONTROL_PROTEINS = {
    "ACTB": 375,    # Actin
    "TUBB": 444,    # Tubulin
    "GAPDH": 335,   # Housekeeping
    "TP53": 393,    # p53
    "EGFR": 1210,   # Growth factor receptor
    "INS": 110,     # Insulin
    "HBB": 146,     # Hemoglobin beta
    "ALB": 609,     # Albumin
    "MYC": 439,     # Transcription factor
    "BRCA1": 1863,  # DNA repair
    "BRCA2": 3418,  # DNA repair
    "AKT1": 480,    # Kinase
    "MTOR": 2549,   # mTOR
    "KRAS": 189,    # Oncogene
    "BRAF": 766,    # Kinase
}

# Ribosomal proteins (highly conserved, structural)
RIBOSOMAL_PROTEINS = {
    "RPS3": 243,
    "RPS4X": 263,
    "RPS5": 204,
    "RPS6": 249,
    "RPS8": 208,
    "RPL3": 403,
    "RPL4": 427,
    "RPL5": 297,
    "RPL7": 248,
    "RPL8": 257,
}

# Histones (nucleosome proteins, very conserved)
HISTONE_PROTEINS = {
    "H2A": 130,
    "H2B": 126,
    "H3": 136,
    "H4": 103,
    "H1": 219,
}


def find_best_z2_fit(length: int) -> Tuple[str, float, float]:
    """Find best Z² formula fit for a protein length."""

    best_formula = ""
    best_predicted = 0
    best_error = float('inf')

    # Try: n×Z² + m for integer n, small m
    for n in range(1, 100):
        for m in range(-10, 11):
            pred = n * Z_SQUARED + m
            if pred > 0:
                error = abs(length - pred) / length * 100
                if error < best_error:
                    best_error = error
                    best_predicted = pred
                    if m == 0:
                        best_formula = f"{n}Z²"
                    elif m > 0:
                        best_formula = f"{n}Z² + {m}"
                    else:
                        best_formula = f"{n}Z² - {-m}"

    # Try: n×θ_Z² formulas
    for n in range(1, 20):
        for d in range(1, 10):
            pred = n * THETA_Z2_DEG / d
            if pred > 0:
                error = abs(length - pred) / length * 100
                if error < best_error:
                    best_error = error
                    best_predicted = pred
                    best_formula = f"{n}θ_Z²/{d}"

    return best_formula, best_predicted, best_error


def analyze_protein_set(proteins: Dict[str, int], name: str) -> Dict:
    """Analyze a set of proteins for Z² relationships."""

    results = []
    errors = []

    for protein, length in proteins.items():
        formula, predicted, error = find_best_z2_fit(length)
        results.append({
            "protein": protein,
            "length": length,
            "formula": formula,
            "predicted": predicted,
            "error": error,
        })
        errors.append(error)

    # Sort by error
    results.sort(key=lambda x: x["error"])

    # Statistics
    stats = {
        "name": name,
        "n_proteins": len(proteins),
        "mean_error": np.mean(errors),
        "median_error": np.median(errors),
        "std_error": np.std(errors),
        "min_error": np.min(errors),
        "max_error": np.max(errors),
        "n_below_1pct": sum(1 for e in errors if e < 1.0),
        "n_below_0.5pct": sum(1 for e in errors if e < 0.5),
    }

    return {"results": results, "stats": stats}


def run_extended_validation():
    """Run validation across all protein sets."""

    print("=" * 78)
    print("Z² EXTENDED PROTEIN VALIDATION")
    print("=" * 78)
    print(f"\nZ² = {Z_SQUARED:.6f}")
    print(f"θ_Z² = {THETA_Z2_DEG:.2f}°")
    print("\nTesting Z² relationships against extended protein databases.")
    print("If Z² is real, target system proteins should match better than controls.\n")

    all_results = {}

    # Analyze each set
    protein_sets = [
        (DISEASE_PROTEINS, "target system Proteins"),
        (CONTROL_PROTEINS, "Control Proteins"),
        (RIBOSOMAL_PROTEINS, "Ribosomal Proteins"),
        (HISTONE_PROTEINS, "Histone Proteins"),
    ]

    for proteins, name in protein_sets:
        analysis = analyze_protein_set(proteins, name)
        all_results[name] = analysis

        print("=" * 70)
        print(f"{name.upper()}")
        print("=" * 70)

        stats = analysis["stats"]
        print(f"\nN = {stats['n_proteins']}")
        print(f"Mean error: {stats['mean_error']:.2f}%")
        print(f"Median error: {stats['median_error']:.2f}%")
        print(f"Std error: {stats['std_error']:.2f}%")
        print(f"Matches <1%: {stats['n_below_1pct']}/{stats['n_proteins']}")
        print(f"Matches <0.5%: {stats['n_below_0.5pct']}/{stats['n_proteins']}")

        print(f"\nTop 10 matches:")
        print("-" * 60)
        for r in analysis["results"][:10]:
            print(f"  {r['protein']:12} {r['length']:5} ≈ {r['formula']:12} ({r['error']:.2f}%)")

    # Comparative analysis
    print("\n" + "=" * 78)
    print("COMPARATIVE ANALYSIS")
    print("=" * 78)

    print("\nIf Z² is specific to target system proteins, we expect:")
    print("  target system proteins: lower mean error, more <1% matches")
    print("  Control proteins: higher mean error, fewer <1% matches")
    print()

    print(f"{'Set':<25} {'N':>5} {'Mean%':>8} {'Median%':>8} {'<1%':>6} {'<0.5%':>6}")
    print("-" * 65)

    for name in ["target system Proteins", "Control Proteins", "Ribosomal Proteins", "Histone Proteins"]:
        stats = all_results[name]["stats"]
        print(f"{name:<25} {stats['n_proteins']:>5} {stats['mean_error']:>8.2f} "
              f"{stats['median_error']:>8.2f} {stats['n_below_1pct']:>6} {stats['n_below_0.5pct']:>6}")

    # Statistical test: Are target system proteins significantly better fits?
    disease_errors = [r["error"] for r in all_results["target system Proteins"]["results"]]
    control_errors = [r["error"] for r in all_results["Control Proteins"]["results"]]

    from scipy import stats as scipy_stats
    t_stat, p_value = scipy_stats.ttest_ind(disease_errors, control_errors)

    print(f"\nT-test (target system vs Control):")
    print(f"  t-statistic: {t_stat:.3f}")
    print(f"  p-value: {p_value:.4f}")

    if p_value < 0.05:
        if np.mean(disease_errors) < np.mean(control_errors):
            print("  ** SIGNIFICANT: target system proteins fit Z² BETTER than controls **")
        else:
            print("  * Significant but controls fit better - Z² may be general *")
    else:
        print("  Not significant - Z² fits equally well for both sets")

    # Look for patterns in target system proteins
    print("\n" + "=" * 78)
    print("target system PROTEIN PATTERNS")
    print("=" * 78)

    # Group by target system category
    disease_categories = {
        "Alzheimer's": ["APP", "PSEN1", "PSEN2", "MAPT_4R", "APOE", "TREM2", "CLU", "ABCA7"],
        "Parkinson's": ["SNCA", "LRRK2", "PARK7", "PINK1", "PRKN", "GBA", "VPS35"],
        "PolyQ": ["HTT", "ATXN1", "ATXN2", "ATXN3", "CACNA1A", "ATXN7", "ATN1", "AR"],
        "ALS": ["SOD1", "TARDBP", "FUS", "C9orf72", "OPTN", "VCP", "UBQLN2", "ANG"],
        "Other": ["PRNP", "MBP", "PLP1", "MOG", "MAG", "ATXN10", "PPP2R2B", "KCND3", "FXN"],
    }

    print("\nMean error by target system category:")
    print("-" * 50)

    for category, proteins in disease_categories.items():
        category_errors = []
        for r in all_results["target system Proteins"]["results"]:
            if r["protein"] in proteins:
                category_errors.append(r["error"])

        if category_errors:
            mean_err = np.mean(category_errors)
            n_good = sum(1 for e in category_errors if e < 1.0)
            print(f"  {category:<15} mean={mean_err:.2f}%, {n_good}/{len(category_errors)} <1%")

    # Special analysis: PolyQ target system thresholds
    print("\n" + "=" * 78)
    print("POLYQ target system THRESHOLD ANALYSIS")
    print("=" * 78)

    polyq_thresholds = {
        "Huntington's (HTT)": 36,
        "SCA1 (ATXN1)": 39,
        "SCA2 (ATXN2)": 32,
        "SCA3 (ATXN3)": 55,
        "SCA6 (CACNA1A)": 19,
        "SCA7 (ATXN7)": 34,
        "DRPLA (ATN1)": 48,
        "SBMA (AR)": 38,
    }

    print("\nDisease thresholds vs Z² predictions:")
    print("-" * 60)

    threshold_errors = []
    for target system, threshold in polyq_thresholds.items():
        formula, predicted, error = find_best_z2_fit(threshold)
        threshold_errors.append(error)
        match = "✓" if error < 3 else ""
        print(f"  {target system:<25} {threshold:>3} ≈ {predicted:.1f} ({error:.1f}%) {match}")

    print(f"\nMean threshold error: {np.mean(threshold_errors):.2f}%")
    print(f"All thresholds <5%: {sum(1 for e in threshold_errors if e < 5)}/{len(threshold_errors)}")

    # HONEST ASSESSMENT
    print("\n" + "=" * 78)
    print("HONEST ASSESSMENT")
    print("=" * 78)

    disease_mean = np.mean(disease_errors)
    control_mean = np.mean(control_errors)

    print(f"""
WHAT THE DATA SHOWS:
- target system proteins mean error: {disease_mean:.2f}%
- Control proteins mean error: {control_mean:.2f}%
- Difference: {abs(disease_mean - control_mean):.2f}%

INTERPRETATION:
""")

    if disease_mean < control_mean and p_value < 0.05:
        print("""
POSITIVE RESULT: target system proteins fit Z² significantly better than controls.
This suggests Z² may encode something real about target system protein geometry.

HOWEVER:
- The effect size is modest
- Both sets have many good fits (proteins are integer-length, so some will fit)
- Need mechanistic explanation for WHY target system proteins follow Z²
""")
    elif disease_mean >= control_mean:
        print("""
NEUTRAL/NEGATIVE RESULT: Control proteins fit as well or better than target system proteins.
This suggests Z² may be a general mathematical property of protein lengths,
not specific to target system.

ALTERNATIVE INTERPRETATION:
- All proteins may have evolved lengths near Z² multiples
- This could reflect fundamental constraints on protein size
- target system proteins aren't special in this regard
""")
    else:
        print("""
INCONCLUSIVE: No significant difference between target system and control proteins.
More data needed to determine if Z² relationships are real or coincidental.
""")

    # Save results
    output = {
        "disease_proteins": all_results["target system Proteins"],
        "control_proteins": all_results["Control Proteins"],
        "ribosomal_proteins": all_results["Ribosomal Proteins"],
        "histone_proteins": all_results["Histone Proteins"],
        "statistical_test": {
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "disease_mean_error": float(disease_mean),
            "control_mean_error": float(control_mean),
        },
        "constants": {
            "Z_squared": Z_SQUARED,
            "theta_Z2_deg": THETA_Z2_DEG,
        }
    }

    output_path = Path(__file__).parent / "z2_extended_validation_results.json"

    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(v) for v in obj]
        elif isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        else:
            return obj

    with open(output_path, 'w') as f:
        json.dump(make_serializable(output), f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


if __name__ == "__main__":
    results = run_extended_validation()
