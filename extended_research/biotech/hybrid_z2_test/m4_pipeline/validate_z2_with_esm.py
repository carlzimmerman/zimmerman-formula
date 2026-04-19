#!/usr/bin/env python3
"""
Z² Validation Using Actual ESM-2 Predictions

SPDX-License-Identifier: AGPL-3.0-or-later

The previous validation used a toy helix model. This validation uses
the ACTUAL ESM-2 pipeline to compare Z² designed sequences against
random sequences.

If Z² is real:
- Z² sequences should have HIGHER alignment than random sequences
  when BOTH are predicted by ESM-2.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy import stats
import json
import os
from datetime import datetime
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Import our actual pipeline tools
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from m4_esm_predictor import predict_and_validate
from m4_z2_resonance_selector import Z2ResonanceSelector

# ==============================================================================
# CONSTANTS
# ==============================================================================

AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

Z2_SEQUENCES = {
    "z2_compact_60": "GNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEMIVYK",
    "z2_harmonic_72": "GNALEMALIYEQDPSMEFLIYKRNGSALEMALVIYEKNPNMEFLIYRQDGSALEMIYVKRNPNMEFLIYE",
    "z2_globular_80": "GNALEMALIYRQDPSMEFLIYKRNGNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEM",
}

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
# VALIDATION
# ==============================================================================

def run_esm_validation():
    """Run validation using actual ESM-2 predictions."""

    print("=" * 70)
    print("Z² VALIDATION WITH ACTUAL ESM-2 PREDICTIONS")
    print("=" * 70)
    print("\nThis uses the REAL ESM-2 pipeline, not toy models.\n")

    selector = Z2ResonanceSelector()

    results = {
        "timestamp": datetime.now().isoformat(),
        "z2_sequences": {},
        "random_sequences": {},
        "scrambled_sequences": {},
    }

    # Test Z² designed sequences
    print("\n" + "=" * 70)
    print("Z² DESIGNED SEQUENCES")
    print("=" * 70)

    z2_alignments = []
    z2_contacts = []

    for name, seq in Z2_SEQUENCES.items():
        output_dir = f"validation_esm/{name}"
        os.makedirs(output_dir, exist_ok=True)

        try:
            pred_result = predict_and_validate(seq, name, output_dir)

            # Check if there was an error
            if "error" in pred_result:
                print(f"  {name}: FAILED - {pred_result['error']}")
                continue

            # Get the PDB path (constructed from output_dir and name)
            pdb_path = os.path.join(output_dir, f"{name}_esm.pdb")

            if os.path.exists(pdb_path):
                z2_result = selector.evaluate_pdb(pdb_path)

                # Access nested z2_analysis
                z2_analysis = z2_result.get("z2_analysis", {})
                align = z2_analysis.get("alignment_ratio", 0)
                p_val = z2_analysis.get("p_value", 1.0)
                contacts = pred_result.get("z2_geometry", {}).get("mean_contacts", 0)

                z2_alignments.append(align)
                z2_contacts.append(contacts)

                results["z2_sequences"][name] = {
                    "alignment": float(align),
                    "contacts": float(contacts),
                    "p_value": float(p_val),
                    "length": len(seq)
                }

                print(f"  {name}: {align:.2f}× alignment, {contacts:.1f} contacts, p={p_val:.2e}")
            else:
                print(f"  {name}: PDB not found at {pdb_path}")

        except Exception as e:
            print(f"  {name}: ERROR - {e}")

    # Test random sequences (same lengths as Z² sequences)
    print("\n" + "=" * 70)
    print("RANDOM SEQUENCE CONTROLS")
    print("=" * 70)

    random_alignments = []
    random_contacts = []

    for i, (z2_name, z2_seq) in enumerate(Z2_SEQUENCES.items()):
        length = len(z2_seq)
        name = f"random_{length}_{i}"
        seq = generate_random_sequence(length, seed=42 + i * 1000)

        output_dir = f"validation_esm/{name}"
        os.makedirs(output_dir, exist_ok=True)

        try:
            pred_result = predict_and_validate(seq, name, output_dir)

            if "error" in pred_result:
                print(f"  {name}: FAILED - {pred_result['error']}")
                continue

            pdb_path = os.path.join(output_dir, f"{name}_esm.pdb")

            if os.path.exists(pdb_path):
                z2_result = selector.evaluate_pdb(pdb_path)

                # Access nested z2_analysis
                z2_analysis = z2_result.get("z2_analysis", {})
                align = z2_analysis.get("alignment_ratio", 0)
                p_val = z2_analysis.get("p_value", 1.0)
                contacts = pred_result.get("z2_geometry", {}).get("mean_contacts", 0)

                random_alignments.append(align)
                random_contacts.append(contacts)

                results["random_sequences"][name] = {
                    "alignment": float(align),
                    "contacts": float(contacts),
                    "p_value": float(p_val),
                    "length": length
                }

                print(f"  {name}: {align:.2f}× alignment, {contacts:.1f} contacts, p={p_val:.2e}")

        except Exception as e:
            print(f"  {name}: ERROR - {e}")

    # Test scrambled Z² sequences
    print("\n" + "=" * 70)
    print("SCRAMBLED Z² SEQUENCES")
    print("=" * 70)

    scrambled_alignments = []

    for z2_name, z2_seq in Z2_SEQUENCES.items():
        scrambled_seq = scramble_sequence(z2_seq, seed=123)
        name = f"scrambled_{z2_name}"

        output_dir = f"validation_esm/{name}"
        os.makedirs(output_dir, exist_ok=True)

        try:
            pred_result = predict_and_validate(scrambled_seq, name, output_dir)

            if "error" in pred_result:
                print(f"  {name}: FAILED - {pred_result['error']}")
                continue

            pdb_path = os.path.join(output_dir, f"{name}_esm.pdb")

            if os.path.exists(pdb_path):
                z2_result = selector.evaluate_pdb(pdb_path)

                # Access nested z2_analysis
                z2_analysis = z2_result.get("z2_analysis", {})
                align = z2_analysis.get("alignment_ratio", 0)
                p_val = z2_analysis.get("p_value", 1.0)
                contacts = pred_result.get("z2_geometry", {}).get("mean_contacts", 0)

                scrambled_alignments.append(align)

                results["scrambled_sequences"][name] = {
                    "alignment": float(align),
                    "contacts": float(contacts),
                    "p_value": float(p_val),
                }

                print(f"  {name}: {align:.2f}× alignment, {contacts:.1f} contacts")

        except Exception as e:
            print(f"  {name}: ERROR - {e}")

    # Statistical comparison
    print("\n" + "=" * 70)
    print("STATISTICAL COMPARISON")
    print("=" * 70)

    if z2_alignments and random_alignments:
        z2_mean = np.mean(z2_alignments)
        random_mean = np.mean(random_alignments)
        scrambled_mean = np.mean(scrambled_alignments) if scrambled_alignments else 0

        # T-test: Z² vs Random
        if len(z2_alignments) >= 2 and len(random_alignments) >= 2:
            t_stat, p_val = stats.ttest_ind(z2_alignments, random_alignments)
        else:
            t_stat, p_val = 0, 1.0

        ratio = z2_mean / random_mean if random_mean > 0 else float('inf')

        results["comparison"] = {
            "z2_mean": float(z2_mean),
            "random_mean": float(random_mean),
            "scrambled_mean": float(scrambled_mean),
            "ratio": float(ratio),
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
        }

        print(f"\n  Z² designed mean: {z2_mean:.2f}×")
        print(f"  Random mean: {random_mean:.2f}×")
        print(f"  Scrambled mean: {scrambled_mean:.2f}×")
        print(f"  Z²/Random ratio: {ratio:.2f}")
        print(f"  T-test p-value: {p_val:.4f}")

    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    z2_mean = results.get("comparison", {}).get("z2_mean", 0)
    random_mean = results.get("comparison", {}).get("random_mean", 0)
    ratio = results.get("comparison", {}).get("ratio", 1.0)

    if ratio > 1.2:
        verdict = "VALIDATED"
        explanation = f"""
Z² ALIGNMENT IS REAL, NOT SLOP.

Evidence:
1. Z² sequences: {z2_mean:.2f}× average alignment
2. Random sequences: {random_mean:.2f}× average alignment
3. Z² is {(ratio-1)*100:.0f}% BETTER than random

The Z² geometry creates sequences with measurably higher
harmonic alignment than random amino acid sequences.
        """
    elif ratio > 1.0:
        verdict = "PARTIALLY VALIDATED"
        explanation = f"""
Z² shows modest improvement over random ({(ratio-1)*100:.0f}% better).
More samples may be needed to confirm statistical significance.
        """
    else:
        verdict = "NOT VALIDATED"
        explanation = f"""
Z² sequences ({z2_mean:.2f}×) are not better than random ({random_mean:.2f}×).
The Z² effect may be an artifact.
        """

    results["verdict"] = verdict

    print(f"\n  VERDICT: {verdict}")
    print(explanation)

    # Save results
    output_path = "validation_esm_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to: {output_path}")

    return results


if __name__ == "__main__":
    run_esm_validation()
