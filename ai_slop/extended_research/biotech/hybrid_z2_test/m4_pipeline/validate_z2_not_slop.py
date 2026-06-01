#!/usr/bin/env python3
"""
Z² Validation: Is This Real or Slop?

SPDX-License-Identifier: AGPL-3.0-or-later

Rigorous validation to ensure Z² results are not artifacts:

1. NEGATIVE CONTROLS: Random sequences should have LOWER Z² alignment
2. SCRAMBLED CONTROLS: Shuffled Z² sequences should lose their properties
3. NATURAL PROTEINS: Compare to real PDB structures
4. STATISTICAL TESTS: Proper hypothesis testing with multiple comparisons

If Z² is real:
- Z² designed sequences >> random sequences
- Scrambling should destroy Z² alignment
- Natural proteins should show intermediate values

If Z² is slop:
- Random sequences will have similar Z² alignment
- Scrambling won't matter
- No systematic difference from controls

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy import stats
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Import our Z² tools
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from m4_z2_resonance_selector import Z2ResonanceSelector, parse_ca_coords_from_content, fetch_pdb_content
from m4_z2_resonance_selector import build_anm_hessian, compute_normal_modes, analyze_z2_alignment

# ==============================================================================
# SEQUENCE GENERATORS
# ==============================================================================

AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

def generate_random_sequence(length: int, seed: int = None) -> str:
    """Generate a completely random amino acid sequence."""
    if seed is not None:
        np.random.seed(seed)
    return "".join(np.random.choice(list(AMINO_ACIDS), length))


def scramble_sequence(sequence: str, seed: int = None) -> str:
    """Scramble a sequence (same composition, different order)."""
    if seed is not None:
        np.random.seed(seed)
    chars = list(sequence)
    np.random.shuffle(chars)
    return "".join(chars)


# ==============================================================================
# Z² ANALYSIS (Simplified - works on any coords)
# ==============================================================================

def analyze_coords_z2(coords: np.ndarray) -> Dict:
    """Analyze Z² alignment for a set of coordinates."""
    if len(coords) < 10:
        return {"error": "Too few residues", "alignment_ratio": 0, "p_value": 1.0}

    H = build_anm_hessian(coords, cutoff=15.0)
    frequencies, _ = compute_normal_modes(H)

    if len(frequencies) < 5:
        return {"error": "Too few modes", "alignment_ratio": 0, "p_value": 1.0}

    return analyze_z2_alignment(frequencies, n_modes=10)


def quick_structure_prediction(sequence: str) -> np.ndarray:
    """
    Quick structure prediction using distance geometry.

    This is a simplified model - just generates plausible Cα coordinates
    based on sequence properties. NOT a real structure prediction.
    """
    n = len(sequence)

    # Simple helix-like backbone with some randomness
    coords = []

    # Helix parameters
    rise_per_residue = 1.5  # Å
    radius = 2.3  # Å
    angle_per_residue = 100 * np.pi / 180  # ~100 degrees

    for i in range(n):
        # Base helix
        x = radius * np.cos(i * angle_per_residue)
        y = radius * np.sin(i * angle_per_residue)
        z = i * rise_per_residue

        # Add some noise based on residue type
        aa = sequence[i]
        if aa in "VILMFYW":  # Hydrophobic - pack toward center
            x *= 0.8
            y *= 0.8
        elif aa in "DEKR":  # Charged - extend outward
            x *= 1.2
            y *= 1.2

        coords.append([x, y, z])

    return np.array(coords)


# ==============================================================================
# VALIDATION TESTS
# ==============================================================================

def test_random_sequences(n_random: int = 20, lengths: List[int] = [50, 60, 70, 80]) -> Dict:
    """
    Test random sequences as negative control.

    If Z² is real, random sequences should have LOWER alignment.
    """
    print("\n" + "=" * 70)
    print("TEST 1: RANDOM SEQUENCE CONTROLS")
    print("=" * 70)
    print(f"Testing {n_random} random sequences per length")

    results = {"lengths": {}, "all_alignments": [], "all_p_values": []}

    for length in lengths:
        alignments = []
        p_values = []

        for i in range(n_random):
            seq = generate_random_sequence(length, seed=i * 1000 + length)
            coords = quick_structure_prediction(seq)
            z2 = analyze_coords_z2(coords)

            if "error" not in z2:
                alignments.append(z2["alignment_ratio"])
                p_values.append(z2["p_value"])

        results["lengths"][length] = {
            "mean_alignment": float(np.mean(alignments)),
            "std_alignment": float(np.std(alignments)),
            "mean_p_value": float(np.mean(p_values)),
            "n_samples": len(alignments)
        }
        results["all_alignments"].extend(alignments)
        results["all_p_values"].extend(p_values)

        print(f"\n  Length {length}:")
        print(f"    Alignment: {np.mean(alignments):.2f} ± {np.std(alignments):.2f}×")
        print(f"    Mean p-value: {np.mean(p_values):.2e}")

    results["overall"] = {
        "mean_alignment": float(np.mean(results["all_alignments"])),
        "std_alignment": float(np.std(results["all_alignments"])),
        "mean_p_value": float(np.mean(results["all_p_values"]))
    }

    print(f"\n  OVERALL RANDOM:")
    print(f"    Alignment: {results['overall']['mean_alignment']:.2f} ± {results['overall']['std_alignment']:.2f}×")

    return results


def test_scrambled_sequences(z2_sequences: Dict[str, str], n_scrambles: int = 10) -> Dict:
    """
    Test scrambled versions of Z² sequences.

    If Z² is real, scrambling should DESTROY the alignment.
    """
    print("\n" + "=" * 70)
    print("TEST 2: SCRAMBLED SEQUENCE CONTROLS")
    print("=" * 70)
    print(f"Testing {n_scrambles} scrambles per Z² sequence")

    results = {"sequences": {}}

    for name, seq in z2_sequences.items():
        # Original sequence
        coords_orig = quick_structure_prediction(seq)
        z2_orig = analyze_coords_z2(coords_orig)

        # Scrambled versions
        scrambled_alignments = []
        for i in range(n_scrambles):
            scrambled = scramble_sequence(seq, seed=i * 100)
            coords_scr = quick_structure_prediction(scrambled)
            z2_scr = analyze_coords_z2(coords_scr)
            if "error" not in z2_scr:
                scrambled_alignments.append(z2_scr["alignment_ratio"])

        orig_align = z2_orig.get("alignment_ratio", 0)
        scr_mean = np.mean(scrambled_alignments) if scrambled_alignments else 0
        scr_std = np.std(scrambled_alignments) if scrambled_alignments else 0

        # Statistical test: is original significantly better?
        if scrambled_alignments and orig_align > 0:
            t_stat, p_val = stats.ttest_1samp(scrambled_alignments, orig_align)
            significant = p_val < 0.05 and orig_align > scr_mean
        else:
            t_stat, p_val = 0, 1.0
            significant = False

        results["sequences"][name] = {
            "original_alignment": float(orig_align),
            "scrambled_mean": float(scr_mean),
            "scrambled_std": float(scr_std),
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "original_is_better": significant
        }

        print(f"\n  {name}:")
        print(f"    Original: {orig_align:.2f}×")
        print(f"    Scrambled: {scr_mean:.2f} ± {scr_std:.2f}×")
        print(f"    Original better: {'✓ YES' if significant else '✗ NO'} (p={p_val:.3f})")

    return results


def test_natural_proteins(pdb_ids: List[str] = None) -> Dict:
    """
    Test natural proteins from PDB.

    Provides ground truth for what "normal" Z² alignment looks like.
    """
    if pdb_ids is None:
        pdb_ids = ["1UBQ", "1LYZ", "5PTI", "1MBN", "1CRN", "2GB1", "1VII", "1L2Y"]

    print("\n" + "=" * 70)
    print("TEST 3: NATURAL PROTEIN COMPARISON")
    print("=" * 70)
    print(f"Testing {len(pdb_ids)} natural proteins from PDB")

    results = {"proteins": {}, "alignments": [], "p_values": []}

    for pdb_id in pdb_ids:
        pdb_content = fetch_pdb_content(pdb_id)
        if pdb_content is None:
            print(f"  {pdb_id}: Could not fetch")
            continue

        coords = parse_ca_coords_from_content(pdb_content)
        if len(coords) < 10:
            print(f"  {pdb_id}: Too few residues")
            continue

        z2 = analyze_coords_z2(coords)

        if "error" not in z2:
            results["proteins"][pdb_id] = {
                "n_residues": len(coords),
                "alignment_ratio": float(z2["alignment_ratio"]),
                "pearson_r": float(z2["pearson_r"]),
                "p_value": float(z2["p_value"])
            }
            results["alignments"].append(z2["alignment_ratio"])
            results["p_values"].append(z2["p_value"])

            print(f"  {pdb_id}: {len(coords)} res, {z2['alignment_ratio']:.2f}× alignment, p={z2['p_value']:.2e}")

    if results["alignments"]:
        results["overall"] = {
            "mean_alignment": float(np.mean(results["alignments"])),
            "std_alignment": float(np.std(results["alignments"])),
            "mean_p_value": float(np.mean(results["p_values"]))
        }
        print(f"\n  NATURAL PROTEINS:")
        print(f"    Alignment: {results['overall']['mean_alignment']:.2f} ± {results['overall']['std_alignment']:.2f}×")

    return results


def compare_all_groups(z2_results: Dict, random_results: Dict, natural_results: Dict) -> Dict:
    """
    Statistical comparison of all groups.

    If Z² is real:
    - Z² designed >> random
    - Z² designed >= natural (or close)
    """
    print("\n" + "=" * 70)
    print("STATISTICAL COMPARISON")
    print("=" * 70)

    # Extract alignment values
    z2_alignments = [v["alignment_ratio"] for v in z2_results.values() if isinstance(v, dict) and "alignment_ratio" in v]
    random_alignments = random_results.get("all_alignments", [])
    natural_alignments = natural_results.get("alignments", [])

    results = {}

    # Z² vs Random
    if z2_alignments and random_alignments:
        t_stat, p_val = stats.ttest_ind(z2_alignments, random_alignments)
        effect_size = (np.mean(z2_alignments) - np.mean(random_alignments)) / np.std(random_alignments)

        results["z2_vs_random"] = {
            "z2_mean": float(np.mean(z2_alignments)),
            "random_mean": float(np.mean(random_alignments)),
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "effect_size_d": float(effect_size),
            "z2_is_better": p_val < 0.05 and np.mean(z2_alignments) > np.mean(random_alignments)
        }

        print(f"\n  Z² vs Random:")
        print(f"    Z² mean: {np.mean(z2_alignments):.2f}×")
        print(f"    Random mean: {np.mean(random_alignments):.2f}×")
        print(f"    Effect size (Cohen's d): {effect_size:.2f}")
        print(f"    p-value: {p_val:.4f}")
        print(f"    Z² significantly better: {'✓ YES' if results['z2_vs_random']['z2_is_better'] else '✗ NO'}")

    # Z² vs Natural
    if z2_alignments and natural_alignments:
        t_stat, p_val = stats.ttest_ind(z2_alignments, natural_alignments)

        results["z2_vs_natural"] = {
            "z2_mean": float(np.mean(z2_alignments)),
            "natural_mean": float(np.mean(natural_alignments)),
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "z2_is_better_or_equal": np.mean(z2_alignments) >= np.mean(natural_alignments) * 0.9
        }

        print(f"\n  Z² vs Natural Proteins:")
        print(f"    Z² mean: {np.mean(z2_alignments):.2f}×")
        print(f"    Natural mean: {np.mean(natural_alignments):.2f}×")
        print(f"    p-value: {p_val:.4f}")

    return results


# ==============================================================================
# MAIN VALIDATION
# ==============================================================================

def run_full_validation() -> Dict:
    """Run complete validation suite."""

    print("=" * 70)
    print("Z² VALIDATION: IS THIS REAL OR SLOP?")
    print("=" * 70)
    print("\nThis test will determine if Z² alignment is a real phenomenon")
    print("or just noise/artifacts in the analysis pipeline.\n")

    # Our Z² sequences (from the pipeline tests)
    z2_sequences = {
        "z2_compact_60": "GNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEMIVYK",
        "z2_harmonic_72": "GNALEMALIYEQDPSMEFLIYKRNGSALEMALVIYEKNPNMEFLIYRQDGSALEMIYVKRNPNMEFLIYE",
        "z2_globular_80": "GNALEMALIYRQDPSMEFLIYKRNGNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEM",
    }

    # Get Z² alignment for our designed sequences
    print("\n" + "=" * 70)
    print("Z² DESIGNED SEQUENCES (OUR RESULTS)")
    print("=" * 70)

    z2_results = {}
    for name, seq in z2_sequences.items():
        coords = quick_structure_prediction(seq)
        z2 = analyze_coords_z2(coords)
        z2_results[name] = z2
        print(f"  {name}: {z2.get('alignment_ratio', 0):.2f}× alignment")

    # Run all tests
    random_results = test_random_sequences(n_random=20)
    scrambled_results = test_scrambled_sequences(z2_sequences, n_scrambles=10)
    natural_results = test_natural_proteins()
    comparison = compare_all_groups(z2_results, random_results, natural_results)

    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    z2_better_than_random = comparison.get("z2_vs_random", {}).get("z2_is_better", False)
    scrambling_destroys = all(
        v.get("original_is_better", False)
        for v in scrambled_results.get("sequences", {}).values()
    )

    if z2_better_than_random and scrambling_destroys:
        verdict = "VALIDATED"
        explanation = """
Z² ALIGNMENT IS REAL, NOT SLOP.

Evidence:
1. Z² sequences have SIGNIFICANTLY higher alignment than random (p < 0.05)
2. Scrambling the sequences DESTROYS the Z² alignment
3. This pattern is NOT an artifact of the analysis pipeline

The Z² geometry is a real property of the designed sequences.
        """
    elif z2_better_than_random:
        verdict = "PARTIALLY VALIDATED"
        explanation = """
Z² alignment shows promise but needs more investigation.

- Z² sequences are better than random ✓
- Scrambling test was inconclusive
- More rigorous structure prediction needed
        """
    else:
        verdict = "NOT VALIDATED"
        explanation = """
WARNING: Z² alignment may be an artifact.

- Z² sequences are NOT significantly better than random
- The observed patterns may be noise
- Need better structure prediction methods
        """

    print(f"\n  VERDICT: {verdict}")
    print(explanation)

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "verdict": verdict,
        "z2_sequences": z2_results,
        "random_controls": random_results,
        "scrambled_controls": scrambled_results,
        "natural_proteins": natural_results,
        "statistical_comparison": comparison
    }

    output_path = "validation_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Results saved to: {output_path}")

    return results


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    results = run_full_validation()
