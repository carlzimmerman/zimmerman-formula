#!/usr/bin/env python3
"""
02_null_hypothesis_testing.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

02_null_hypothesis_testing.py - Rigorous Statistical Controls

PURPOSE:
Implement Gemini's "Null Hypothesis & Baseline Testing" prompt.

METHODOLOGY:
1. Generate 100+ scrambled "decoy" peptides for each candidate
2. Run IDENTICAL scoring on candidates AND decoys
3. Calculate z-scores and p-values
4. Definitively answer: Is performance better than random with p<0.05?

CRITICAL RULES:
- NO mock data
- Explicit random seeds for reproducibility
- Raw float outputs only (no interpretation)
- Strict statistical thresholds

Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
from typing import List, Dict, Tuple
import sys

# Set random seed for STRICT REPRODUCIBILITY
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("NULL HYPOTHESIS TESTING FRAMEWORK")
print("Rigorous Statistical Controls for Peptide Scoring")
print("=" * 80)
print(f"Random seed: {RANDOM_SEED}")
print()


# =============================================================================
# AMINO ACID PROPERTIES (VALIDATED FROM LITERATURE)
# =============================================================================

# Kyte-Doolittle hydropathy scale (J. Mol. Biol. 157:105-132, 1982)
HYDROPATHY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5,
}

# Chou-Fasman beta-sheet propensity (Adv. Enzymol. 47:45-148, 1978)
BETA_PROPENSITY = {
    'V': 1.70, 'I': 1.60, 'Y': 1.47, 'F': 1.38, 'W': 1.37,
    'L': 1.30, 'T': 1.19, 'C': 1.19, 'M': 1.05, 'Q': 1.10,
    'R': 0.93, 'N': 0.89, 'H': 0.87, 'A': 0.83, 'S': 0.75,
    'G': 0.75, 'K': 0.74, 'D': 0.54, 'P': 0.55, 'E': 0.37,
}

# Molecular weights (Da)
MW = {
    'A': 89, 'R': 174, 'N': 132, 'D': 133, 'C': 121,
    'E': 147, 'Q': 146, 'G': 75, 'H': 155, 'I': 131,
    'L': 131, 'K': 146, 'M': 149, 'F': 165, 'P': 115,
    'S': 105, 'T': 119, 'W': 204, 'Y': 181, 'V': 117,
}

AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'


# =============================================================================
# DECOY GENERATOR
# =============================================================================

def generate_scrambled_decoys(sequence: str, n_decoys: int = 100) -> List[str]:
    """
    Generate scrambled decoy peptides with IDENTICAL composition.

    The decoys have:
    - Same length
    - Same amino acid composition
    - Random order

    This is a STRICT control: any property based on composition
    will be identical, only sequence-dependent properties differ.
    """
    seq_list = list(sequence.upper())
    decoys = []

    for i in range(n_decoys):
        # Use deterministic shuffling with seed offset
        np.random.seed(RANDOM_SEED + i + 1)
        shuffled = seq_list.copy()
        np.random.shuffle(shuffled)
        decoys.append(''.join(shuffled))

    # Reset seed
    np.random.seed(RANDOM_SEED)

    return decoys


def generate_random_peptides(length: int, n_peptides: int = 100) -> List[str]:
    """
    Generate completely random peptides of specified length.

    This is a WEAKER control: composition also varies.
    """
    peptides = []

    for i in range(n_peptides):
        np.random.seed(RANDOM_SEED + i + 1000)
        seq = ''.join(np.random.choice(list(AMINO_ACIDS)) for _ in range(length))
        peptides.append(seq)

    np.random.seed(RANDOM_SEED)
    return peptides


# =============================================================================
# SCORING FUNCTIONS (RAW, NO INTERPRETATION)
# =============================================================================

def compute_raw_features(sequence: str) -> Dict[str, float]:
    """
    Compute raw numerical features for a peptide.

    Returns RAW FLOATS only. No "scores" or interpretations.
    """
    seq = sequence.upper()

    # Validate input
    for aa in seq:
        if aa not in AMINO_ACIDS:
            raise ValueError(f"Invalid amino acid: {aa}")

    # Raw features
    features = {}

    # Hydropathy
    hydro_values = [HYDROPATHY[aa] for aa in seq]
    features['hydropathy_mean'] = float(np.mean(hydro_values))
    features['hydropathy_std'] = float(np.std(hydro_values))
    features['hydropathy_sum'] = float(np.sum(hydro_values))

    # Beta propensity
    beta_values = [BETA_PROPENSITY[aa] for aa in seq]
    features['beta_mean'] = float(np.mean(beta_values))
    features['beta_std'] = float(np.std(beta_values))

    # Composition counts (raw integers converted to float for consistency)
    features['n_aromatic'] = float(sum(seq.count(aa) for aa in 'FWY'))
    features['n_charged'] = float(sum(seq.count(aa) for aa in 'DEKR'))
    features['n_hydrophobic'] = float(sum(seq.count(aa) for aa in 'AVILMFYW'))
    features['n_proline'] = float(seq.count('P'))
    features['n_glycine'] = float(seq.count('G'))

    # Molecular weight
    features['mw'] = float(sum(MW[aa] for aa in seq))

    # Length
    features['length'] = float(len(seq))

    # Charge at pH 7 (approximate)
    n_positive = seq.count('K') + seq.count('R') + 0.1 * seq.count('H')
    n_negative = seq.count('D') + seq.count('E')
    features['net_charge'] = float(n_positive - n_negative)

    # Isoelectric point approximation
    features['charge_ratio'] = float(n_positive / (n_negative + 0.1))

    return features


def compute_z2_geometric_features(sequence: str) -> Dict[str, float]:
    """
    Compute Z² geometric features WITHOUT hardcoding Z² value.

    Uses ONLY sequence-derived properties, not the 9.14 Å constant.
    """
    seq = sequence.upper()

    # Extended length (Å) - using standard peptide geometry
    # C-alpha to C-alpha distance ~3.8 Å in extended conformation
    CA_DISTANCE = 3.8  # Å - this is a physical constant, not Z²
    extended_length = len(seq) * CA_DISTANCE

    features = {}
    features['extended_length_angstrom'] = float(extended_length)

    # Gyration radius estimate (for random coil)
    # Rg ~ 2.0 * N^0.6 for unfolded peptides (Flory scaling)
    features['rg_estimate'] = float(2.0 * (len(seq) ** 0.6))

    # End-to-end distance estimate
    # <R²> = C_∞ * n * l² where C_∞ ≈ 9 for peptides
    features['end_to_end_estimate'] = float(np.sqrt(9 * len(seq) * (CA_DISTANCE ** 2)))

    return features


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def compute_statistics(candidate_value: float, decoy_values: List[float]) -> Dict:
    """
    Compute rigorous statistics comparing candidate to decoys.

    Returns z-score, p-value, and percentile.
    """
    decoy_array = np.array(decoy_values)

    mean = float(np.mean(decoy_array))
    std = float(np.std(decoy_array))

    # Z-score
    if std > 0:
        z_score = (candidate_value - mean) / std
    else:
        z_score = 0.0

    # P-value (two-tailed)
    # Using empirical distribution
    n_more_extreme = np.sum(np.abs(decoy_array - mean) >= np.abs(candidate_value - mean))
    p_value_empirical = (n_more_extreme + 1) / (len(decoy_array) + 1)

    # Percentile
    percentile = float(100 * np.mean(decoy_array < candidate_value))

    return {
        'candidate_value': float(candidate_value),
        'decoy_mean': mean,
        'decoy_std': std,
        'z_score': float(z_score),
        'p_value': float(p_value_empirical),
        'percentile': percentile,
        'n_decoys': len(decoy_values),
    }


# =============================================================================
# NULL HYPOTHESIS TEST
# =============================================================================

def run_null_hypothesis_test(
    candidate_sequence: str,
    candidate_name: str,
    n_decoys: int = 100,
) -> Dict:
    """
    Run complete null hypothesis test for a single candidate.

    Tests whether candidate performs significantly better than random
    scrambled sequences with the same composition.
    """
    print(f"\nTesting: {candidate_name} ({candidate_sequence})")
    print(f"  Generating {n_decoys} scrambled decoys...")

    # Generate decoys
    scrambled_decoys = generate_scrambled_decoys(candidate_sequence, n_decoys)
    random_decoys = generate_random_peptides(len(candidate_sequence), n_decoys)

    # Compute features for candidate
    candidate_features = compute_raw_features(candidate_sequence)
    candidate_z2 = compute_z2_geometric_features(candidate_sequence)

    # Compute features for all decoys
    scrambled_features = [compute_raw_features(d) for d in scrambled_decoys]
    random_features = [compute_raw_features(d) for d in random_decoys]

    # Statistical comparison for each feature
    results = {
        'candidate_name': candidate_name,
        'candidate_sequence': candidate_sequence,
        'n_decoys': n_decoys,
        'scrambled_comparisons': {},
        'random_comparisons': {},
    }

    print("  Computing statistics...")

    # Compare each feature
    feature_names = list(candidate_features.keys())

    for feature in feature_names:
        cand_val = candidate_features[feature]

        # Against scrambled
        scrambled_vals = [sf[feature] for sf in scrambled_features]
        results['scrambled_comparisons'][feature] = compute_statistics(cand_val, scrambled_vals)

        # Against random
        random_vals = [rf[feature] for rf in random_features]
        results['random_comparisons'][feature] = compute_statistics(cand_val, random_vals)

    # Summary: how many features are significant at p<0.05?
    scrambled_sig = sum(
        1 for f, stats in results['scrambled_comparisons'].items()
        if stats['p_value'] < 0.05
    )
    random_sig = sum(
        1 for f, stats in results['random_comparisons'].items()
        if stats['p_value'] < 0.05
    )

    results['n_features'] = len(feature_names)
    results['n_significant_vs_scrambled'] = scrambled_sig
    results['n_significant_vs_random'] = random_sig

    # Bonferroni correction
    bonferroni_threshold = 0.05 / len(feature_names)
    results['bonferroni_threshold'] = bonferroni_threshold

    scrambled_sig_corrected = sum(
        1 for f, stats in results['scrambled_comparisons'].items()
        if stats['p_value'] < bonferroni_threshold
    )
    results['n_significant_bonferroni'] = scrambled_sig_corrected

    print(f"  Features significant vs scrambled: {scrambled_sig}/{len(feature_names)}")
    print(f"  Features significant vs random: {random_sig}/{len(feature_names)}")
    print(f"  Bonferroni-corrected significant: {scrambled_sig_corrected}")

    return results


# =============================================================================
# BATCH TESTING
# =============================================================================

def test_peptide_set(peptides: List[Tuple[str, str]], n_decoys: int = 100) -> Dict:
    """
    Test a set of peptides against null hypothesis.

    Returns comprehensive results for all peptides.
    """
    all_results = []

    for name, sequence in peptides:
        try:
            result = run_null_hypothesis_test(sequence, name, n_decoys)
            all_results.append(result)
        except Exception as e:
            print(f"  ERROR testing {name}: {e}")
            all_results.append({
                'candidate_name': name,
                'candidate_sequence': sequence,
                'error': str(e),
            })

    # Aggregate statistics
    n_tested = len([r for r in all_results if 'error' not in r])
    avg_sig_scrambled = np.mean([
        r['n_significant_vs_scrambled'] for r in all_results if 'error' not in r
    ]) if n_tested > 0 else 0

    return {
        'timestamp': datetime.now().isoformat(),
        'n_peptides': len(peptides),
        'n_decoys_per_peptide': n_decoys,
        'random_seed': RANDOM_SEED,
        'avg_significant_features': float(avg_sig_scrambled),
        'results': all_results,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution with our designed peptides."""

    # Peptides from our therapeutic pipelines
    DESIGNED_PEPTIDES = [
        # Alpha-synuclein breakers
        ('ZIM-SYN-013', 'FFPFFG'),
        ('ZIM-SYN-034', 'FFFFF'),
        ('ZIM-SYN-004', 'FPF'),
        ('ZIM-SYN-007', 'WPW'),

        # Rhodopsin chaperones
        ('ZIM-RHO-040', 'WFWFW'),
        ('ZIM-RHO-043', 'YFYFY'),
        ('ZIM-RHO-049', 'PMYVL'),

        # CFTR chaperones
        ('ZIM-CF-001', 'WFF'),
        ('ZIM-CF-004', 'RFFR'),

        # Alzheimer's breakers
        ('ZIM-ALZ-003', 'LPFFD'),
        ('ZIM-ALZ-005', 'FPF'),
    ]

    print("=" * 80)
    print("TESTING DESIGNED PEPTIDES AGAINST NULL HYPOTHESIS")
    print("=" * 80)

    results = test_peptide_set(DESIGNED_PEPTIDES, n_decoys=100)

    # Save raw results
    output_file = OUTPUT_DIR / "null_hypothesis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Save CSV of key metrics
    csv_file = OUTPUT_DIR / "null_hypothesis_summary.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'peptide_name', 'sequence', 'n_features',
            'n_sig_scrambled', 'n_sig_random', 'n_sig_bonferroni'
        ])

        for r in results['results']:
            if 'error' not in r:
                writer.writerow([
                    r['candidate_name'],
                    r['candidate_sequence'],
                    r['n_features'],
                    r['n_significant_vs_scrambled'],
                    r['n_significant_vs_random'],
                    r['n_significant_bonferroni'],
                ])

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nResults saved to:")
    print(f"  JSON: {output_file}")
    print(f"  CSV:  {csv_file}")

    print("\n" + "=" * 80)
    print("INTERPRETATION GUIDE")
    print("=" * 80)
    print("""
    If n_sig_scrambled = 0 for a peptide:
      → The peptide has NO features that distinguish it from random
        scrambled sequences. The "design" adds nothing.

    If n_sig_bonferroni > 0:
      → After rigorous multiple testing correction, the peptide still
        shows significant differences from random. This is meaningful.

    If n_sig_random >> n_sig_scrambled:
      → The peptide differs from random sequences, but this is due to
        COMPOSITION, not sequence order. The "design" adds nothing.

    EXPECTED for truly random design: ~5% features significant by chance.
    For {len(DESIGNED_PEPTIDES[0][1]) if DESIGNED_PEPTIDES else 0} residue peptides
    with {results['results'][0]['n_features'] if results['results'] else 0} features:
      → Expect ~{0.05 * (results['results'][0]['n_features'] if results['results'] else 13):.1f} significant by chance.
    """)

    return results


if __name__ == "__main__":
    results = main()
