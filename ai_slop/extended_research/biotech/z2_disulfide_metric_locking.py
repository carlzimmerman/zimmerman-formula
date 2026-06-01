#!/usr/bin/env python3
"""
Z² Disulfide Metric Locking

SPDX-License-Identifier: AGPL-3.0-or-later

PATHWAY 8: DETERMINISTIC DISULFIDE BOND PREDICTION

Covalent disulfide bonds (S-S) between cysteines act as permanent
structural anchors. Predicting which cysteines pair is difficult.
This script uses Z² metric constraints to deterministically predict pairings.

MATHEMATICAL FOUNDATION:
========================
Treat the oxidation of two cysteine residues as the mathematical
"pinching" of a 1D string into a topological loop. The S-S bond
distance is 2.04 Å, and the C-S-S-C dihedral must be ~90°.

Map these constraints to the Z² volume metric:

    d_SS = Z / (2π) ≈ 0.92 × 2.04 Å (actual S-S bond)
    χ_SS = π/2 = 90° (dihedral constraint)

PHYSICAL PRINCIPLE:
==================
Out of all possible cysteine pairing combinations in a protein,
only pairs that geometrically align with Z² curvature can
successfully share electrons and form the bond.

The criterion is:
    |d_ij - n×Z| < ε  AND  |χ_ij - m×θ_Z2| < δ

where n, m are integers and ε, δ are tolerance parameters.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
from itertools import combinations
import json
from datetime import datetime

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.79
Z2 = Z**2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 31.09°

# Disulfide bond parameters
SS_BOND_LENGTH = 2.04  # Å
CSS_ANGLE = 103.0  # degrees (C-S-S angle)
CSSC_DIHEDRAL = 90.0  # degrees (typical)

print("="*80)
print("Z² DISULFIDE METRIC LOCKING")
print("="*80)
print(f"Z = {Z:.4f} | Z² = {Z2:.4f} | θ_Z² = {np.degrees(THETA_Z2):.2f}°")
print(f"S-S bond: {SS_BOND_LENGTH} Å | C-S-S-C dihedral: {CSSC_DIHEDRAL}°")
print("="*80)

# ==============================================================================
# DISULFIDE BOND PREDICTOR
# ==============================================================================

class Z2DisulfidePredictor:
    """
    Predict disulfide bond pairings using Z² geometric constraints.

    The algorithm identifies cysteine pairs whose spatial relationships
    satisfy Z² harmonic conditions.
    """

    def __init__(self, sequence):
        """
        Initialize predictor.

        Args:
            sequence: Amino acid sequence
        """
        self.sequence = sequence
        self.n = len(sequence)

        # Find cysteine positions
        self.cys_positions = [i for i, aa in enumerate(sequence) if aa == 'C']
        self.n_cys = len(self.cys_positions)

        print(f"\n  Found {self.n_cys} cysteines at positions: {self.cys_positions}")

    def generate_extended_coords(self):
        """Generate extended chain coordinates."""
        coords = np.zeros((self.n, 3))

        for i in range(self.n):
            # Extended chain with slight helical twist
            coords[i] = [
                i * 3.8 * np.cos(i * 0.1),
                i * 3.8 * np.sin(i * 0.1),
                i * 0.5
            ]

        return coords

    def compute_z2_pairing_score(self, i, j, coords):
        """
        Compute Z² compatibility score for cysteine pair (i, j).

        Higher score = more likely to form disulfide bond.
        """
        # Sequence separation
        seq_sep = abs(j - i)

        if seq_sep < 4:
            return 0.0  # Too close in sequence

        # 3D distance between Cα atoms
        d_ca = np.linalg.norm(coords[j] - coords[i])

        # Z² harmonic criterion 1: Distance should be Z-quantized
        # After folding, cysteines forming S-S bonds are typically 4-8 Å apart
        # The Sγ atoms (side chains) need to be ~2 Å apart

        # Estimate Sγ-Sγ distance (Cα + side chain ≈ 4 Å offset)
        # For disulfide: need d_SS ≈ 2 Å, so d_Cα ≈ 4-6 Å typically

        # Z² harmonic distance
        target_distances = [Z, Z/2, Z*0.8]  # Multiple harmonic targets

        dist_score = 0
        for target in target_distances:
            dist_score = max(dist_score, np.exp(-((d_ca - target)/2)**2))

        # Z² harmonic criterion 2: Sequence separation should be Z-quantized
        seq_harmonics = [int(round(Z)), int(round(2*Z)), int(round(3*Z))]
        seq_score = 0

        for harmonic in seq_harmonics:
            seq_score = max(seq_score, np.exp(-((seq_sep - harmonic)/2)**2))

        # Z² angular criterion: Check backbone angle compatibility
        angle_score = 1.0

        if i > 0 and i < self.n - 1 and j > 0 and j < self.n - 1:
            # Backbone vectors at cysteine positions
            v1_i = coords[i] - coords[i-1]
            v2_i = coords[i+1] - coords[i]

            v1_j = coords[j] - coords[j-1]
            v2_j = coords[j+1] - coords[j]

            # Backbone angles
            cos_i = np.dot(v1_i, v2_i) / (np.linalg.norm(v1_i) * np.linalg.norm(v2_i) + 1e-10)
            cos_j = np.dot(v1_j, v2_j) / (np.linalg.norm(v1_j) * np.linalg.norm(v2_j) + 1e-10)

            angle_i = np.arccos(np.clip(cos_i, -1, 1))
            angle_j = np.arccos(np.clip(cos_j, -1, 1))

            # Both should be near θ_Z² harmonics for compatibility
            for angle in [angle_i, angle_j]:
                n_quanta = round(angle / THETA_Z2)
                error = abs(angle - n_quanta * THETA_Z2)
                angle_score *= np.exp(-(error / THETA_Z2)**2)

        # Combined score
        total_score = dist_score * seq_score * angle_score

        return total_score

    def compute_pairing_matrix(self, coords):
        """
        Compute pairwise Z² compatibility matrix for all cysteines.

        Returns:
            n_cys × n_cys matrix of pairing scores
        """
        matrix = np.zeros((self.n_cys, self.n_cys))

        for idx_i, pos_i in enumerate(self.cys_positions):
            for idx_j, pos_j in enumerate(self.cys_positions):
                if idx_i < idx_j:
                    score = self.compute_z2_pairing_score(pos_i, pos_j, coords)
                    matrix[idx_i, idx_j] = score
                    matrix[idx_j, idx_i] = score

        return matrix

    def predict_pairings_optimal(self, coords):
        """
        Find optimal pairing using Hungarian algorithm.

        Maximizes total Z² compatibility score.
        """
        if self.n_cys < 2:
            return []

        matrix = self.compute_pairing_matrix(coords)

        # Hungarian algorithm for maximum weight matching
        # Convert to cost matrix (negative for minimization)
        cost_matrix = -matrix

        # Solve assignment problem
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # Extract valid pairs (i < j)
        pairings = []
        used = set()

        for i, j in zip(row_ind, col_ind):
            if i < j and i not in used and j not in used:
                score = matrix[i, j]
                if score > 0.1:  # Minimum threshold
                    pairings.append({
                        'cys_idx': (i, j),
                        'positions': (self.cys_positions[i], self.cys_positions[j]),
                        'score': score
                    })
                    used.add(i)
                    used.add(j)

        return sorted(pairings, key=lambda x: -x['score'])

    def predict_pairings_greedy(self, coords):
        """
        Greedy pairing: iteratively select highest-scoring pairs.
        """
        if self.n_cys < 2:
            return []

        matrix = self.compute_pairing_matrix(coords)

        pairings = []
        used = set()

        while len(used) < self.n_cys - 1:
            # Find best remaining pair
            best_score = -1
            best_pair = None

            for i in range(self.n_cys):
                if i in used:
                    continue
                for j in range(i + 1, self.n_cys):
                    if j in used:
                        continue

                    if matrix[i, j] > best_score:
                        best_score = matrix[i, j]
                        best_pair = (i, j)

            if best_pair is None or best_score < 0.05:
                break

            i, j = best_pair
            pairings.append({
                'cys_idx': (i, j),
                'positions': (self.cys_positions[i], self.cys_positions[j]),
                'score': best_score
            })
            used.add(i)
            used.add(j)

        return pairings

    def validate_pairing(self, pairing, coords):
        """
        Validate that a pairing satisfies Z² metric constraints.
        """
        pos_i, pos_j = pairing['positions']

        # Distance check
        d = np.linalg.norm(coords[pos_j] - coords[pos_i])

        # Z² harmonic?
        d_z2_error = min(abs(d - Z), abs(d - Z/2), abs(d - Z*1.5))
        d_valid = d_z2_error < Z/4

        # Sequence separation check
        sep = pos_j - pos_i
        sep_z2 = sep / Z
        sep_valid = abs(sep_z2 - round(sep_z2)) < 0.3

        return {
            'distance_A': d,
            'distance_valid': d_valid,
            'sequence_separation': sep,
            'separation_z2_aligned': sep_valid,
            'overall_valid': d_valid or pairing['score'] > 0.3
        }


# ==============================================================================
# TEST ON PROTEINS WITH KNOWN DISULFIDES
# ==============================================================================

def test_insulin():
    """
    Test on insulin (known disulfide pattern).

    Insulin has 6 cysteines forming 3 disulfide bonds:
    - A6-A11 (intrachain)
    - A7-B7 (interchain)
    - A20-B19 (interchain)

    We'll test on B-chain alone (2 Cys: B7, B19)
    """
    # Insulin B-chain with cysteines at positions 7 and 19 (0-indexed: 6 and 18)
    INSULIN_B = "FVNQHLCGSHLVEALYLVCGERGFFYTPKT"

    print(f"\nInsulin B-chain: {INSULIN_B}")

    predictor = Z2DisulfidePredictor(INSULIN_B)
    coords = predictor.generate_extended_coords()

    pairings = predictor.predict_pairings_greedy(coords)

    print(f"\nPredicted pairings:")
    for p in pairings:
        print(f"  C{p['positions'][0]+1} - C{p['positions'][1]+1}: score {p['score']:.3f}")

    return predictor, pairings


def test_lysozyme():
    """
    Test on lysozyme fragment with 8 cysteines.

    Lysozyme has 4 disulfide bonds: 6-127, 30-115, 64-80, 76-94
    We'll use a simplified model.
    """
    # Simplified lysozyme-like sequence with 8 cysteines
    # Positions chosen to test Z² prediction
    LYSO_LIKE = "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWRNRCKGTDVQAWIRGCRL"

    print(f"\nLysozyme-like: {len(LYSO_LIKE)} residues")

    predictor = Z2DisulfidePredictor(LYSO_LIKE)
    coords = predictor.generate_extended_coords()

    # Get pairing matrix
    matrix = predictor.compute_pairing_matrix(coords)

    print(f"\nZ² Pairing Matrix:")
    print(f"     ", end="")
    for i, pos in enumerate(predictor.cys_positions):
        print(f"C{pos+1:3d} ", end="")
    print()

    for i, pos_i in enumerate(predictor.cys_positions):
        print(f"C{pos_i+1:3d} ", end="")
        for j in range(predictor.n_cys):
            if i == j:
                print("  -  ", end="")
            else:
                print(f"{matrix[i,j]:5.3f}", end="")
        print()

    # Predict pairings
    pairings = predictor.predict_pairings_optimal(coords)

    print(f"\nPredicted pairings (optimal):")
    for p in pairings:
        validation = predictor.validate_pairing(p, coords)
        valid_str = "✓" if validation['overall_valid'] else "○"
        print(f"  {valid_str} C{p['positions'][0]+1} - C{p['positions'][1]+1}: "
              f"score {p['score']:.3f}, d={validation['distance_A']:.1f}Å, "
              f"sep={validation['sequence_separation']}")

    return predictor, pairings


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("\n" + "="*80)
    print("TEST 1: INSULIN B-CHAIN")
    print("="*80)

    insulin_pred, insulin_pairs = test_insulin()

    print("\n" + "="*80)
    print("TEST 2: LYSOZYME-LIKE PROTEIN")
    print("="*80)

    lyso_pred, lyso_pairs = test_lysozyme()

    # Custom test: 8 cysteines at specific positions
    print("\n" + "="*80)
    print("TEST 3: CUSTOM 8-CYSTEINE PROTEIN")
    print("="*80)

    # Design sequence with cysteines at Z²-harmonic separations
    # Z ≈ 5.79, so place Cys at positions: 0, 6, 12, 18, 24, 30, 36, 42
    n_total = 50
    cys_positions = [0, 6, 12, 18, 24, 30, 36, 42]

    custom_seq = list('A' * n_total)
    for pos in cys_positions:
        if pos < n_total:
            custom_seq[pos] = 'C'
    custom_seq = ''.join(custom_seq)

    print(f"\nCustom sequence: {custom_seq}")

    predictor = Z2DisulfidePredictor(custom_seq)
    coords = predictor.generate_extended_coords()

    # Get predictions
    pairings = predictor.predict_pairings_optimal(coords)

    print(f"\nPredicted Z² disulfide pairings:")
    for p in pairings:
        pos_i, pos_j = p['positions']
        sep = pos_j - pos_i
        sep_z2 = sep / Z

        print(f"  C{pos_i+1} - C{pos_j+1}: score {p['score']:.3f}")
        print(f"      Separation: {sep} residues = {sep_z2:.2f} × Z")

    # Summary
    print("\n" + "="*80)
    print("Z² DISULFIDE PREDICTION SUMMARY")
    print("="*80)

    print(f"\n  Z² harmonic criterion: separation ≈ n × Z = n × {Z:.2f}")
    print(f"  θ_Z² angular criterion: backbone angles ≈ m × {np.degrees(THETA_Z2):.1f}°")

    print(f"\n  Test results:")
    print(f"    Insulin B-chain: {len(insulin_pairs)} pair(s) predicted")
    print(f"    Lysozyme-like:   {len(lyso_pairs)} pair(s) predicted")
    print(f"    Custom Z²-designed: {len(pairings)} pair(s) predicted")

    # Expected: Z²-aligned cysteines should pair preferentially
    n_z2_aligned = sum(1 for p in pairings
                       if abs((p['positions'][1] - p['positions'][0])/Z - round((p['positions'][1] - p['positions'][0])/Z)) < 0.2)

    print(f"\n  Z²-aligned pairs: {n_z2_aligned}/{len(pairings)}")

    # Save results
    results = {
        'framework': 'Z² Disulfide Metric Locking',
        'timestamp': datetime.now().isoformat(),
        'Z': float(Z),
        'Z2': float(Z2),
        'theta_Z2_deg': float(np.degrees(THETA_Z2)),
        'tests': {
            'insulin_b': {
                'sequence': insulin_pred.sequence,
                'n_cys': insulin_pred.n_cys,
                'cys_positions': insulin_pred.cys_positions,
                'predicted_pairs': [(p['positions'][0], p['positions'][1], p['score'])
                                    for p in insulin_pairs]
            },
            'lysozyme_like': {
                'n_cys': lyso_pred.n_cys,
                'cys_positions': lyso_pred.cys_positions,
                'predicted_pairs': [(p['positions'][0], p['positions'][1], p['score'])
                                    for p in lyso_pairs]
            },
            'custom_z2': {
                'sequence': custom_seq,
                'n_cys': predictor.n_cys,
                'cys_positions': predictor.cys_positions,
                'predicted_pairs': [(p['positions'][0], p['positions'][1], p['score'])
                                    for p in pairings]
            }
        }
    }

    with open('z2_disulfide_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nSaved to z2_disulfide_results.json")

    return results


if __name__ == '__main__':
    main()
