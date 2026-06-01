#!/usr/bin/env python3
"""
Z² Protein Folder v7.0 - Balanced Hybrid

Combines signals from multiple methods with careful calibration:
1. Propensity-based scoring (windowed)
2. Pattern recognition (helix i,i+4 / sheet alternating)
3. Nucleation rules with balanced thresholds
4. Secondary voting with confidence weighting

Key insight: We need to balance helix/beta, not just boost one.

Target: >60% Q3 accuracy

Copyright (C) 2026 Carl Zimmerman
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
from typing import Dict, List, Tuple
import json
from pathlib import Path

# =============================================================================
# Z² ANGLES
# =============================================================================

Z2_ANGLES = {
    "H": {"phi": -57.0, "psi": -47.0},
    "E": {"phi": -129.0, "psi": 135.0},
    "C": {"phi": -70.0, "psi": 145.0},
}

# =============================================================================
# PROPENSITIES (Chou-Fasman, original)
# =============================================================================

P_HELIX = {
    'E': 1.53, 'A': 1.45, 'L': 1.34, 'H': 1.24, 'M': 1.20,
    'Q': 1.17, 'W': 1.14, 'V': 1.14, 'F': 1.12, 'K': 1.07,
    'I': 1.00, 'D': 0.98, 'T': 0.82, 'S': 0.79, 'R': 0.79,
    'C': 0.77, 'N': 0.73, 'Y': 0.61, 'P': 0.59, 'G': 0.53,
}

P_SHEET = {
    'M': 1.67, 'V': 1.65, 'I': 1.60, 'C': 1.30, 'Y': 1.29,
    'F': 1.28, 'Q': 1.23, 'L': 1.22, 'T': 1.20, 'W': 1.19,
    'A': 0.97, 'R': 0.90, 'G': 0.81, 'D': 0.80, 'K': 0.74,
    'S': 0.72, 'H': 0.71, 'N': 0.65, 'P': 0.62, 'E': 0.26,
}

HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}


class BalancedPredictor:
    """Balanced secondary structure predictor."""

    def __init__(self):
        self.window = 9

    def _get_propensity_scores(self, sequence: str) -> List[Tuple[float, float, float]]:
        """Calculate smoothed propensity scores with proper normalization."""
        n = len(sequence)
        half = self.window // 2
        scores = []

        for i in range(n):
            h_sum, e_sum, weight_sum = 0.0, 0.0, 0.0

            for j in range(-half, half + 1):
                if 0 <= i + j < n:
                    aa = sequence[i + j]
                    # Gaussian-ish weighting
                    w = np.exp(-0.5 * (j / (half/2))**2)
                    h_sum += P_HELIX.get(aa, 1.0) * w
                    e_sum += P_SHEET.get(aa, 1.0) * w
                    weight_sum += w

            h_avg = h_sum / weight_sum
            e_avg = e_sum / weight_sum

            # Normalize to ~1.0 baseline
            scores.append((h_avg, e_avg, 1.0))

        return scores

    def _helix_pattern_score(self, sequence: str) -> List[float]:
        """Detect helix patterns: i,i+3,i+4 periodicity (3.6 residues/turn)."""
        n = len(sequence)
        helix_signal = [0.0] * n

        # Check for hydrophobic moment at helix periodicity
        for i in range(n - 7):
            # Residues on same face of helix
            same_face = [i, i+3, i+4, i+7]
            valid = [j for j in same_face if j < n]

            hydro = [HYDROPHOBICITY.get(sequence[j], 0) for j in valid]
            if len(hydro) >= 3 and np.mean(hydro) > 1.5:
                for j in range(8):
                    if i + j < n:
                        helix_signal[i + j] += 0.15

        # Also check for consecutive helix formers
        helix_strong = {'A', 'E', 'L', 'M', 'K', 'R', 'Q'}
        for i in range(n - 3):
            count = sum(1 for aa in sequence[i:i+4] if aa in helix_strong)
            if count >= 3:
                for j in range(4):
                    if i + j < n:
                        helix_signal[i + j] += 0.1

        return helix_signal

    def _sheet_pattern_score(self, sequence: str) -> List[float]:
        """Detect sheet patterns: alternating hydrophobic (i,i+2 same face)."""
        n = len(sequence)
        sheet_signal = [0.0] * n

        # Alternating pattern check
        for i in range(n - 4):
            # Same face: i, i+2, i+4
            face_even = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [0, 2, 4] if i+j < n]
            # Opposite face: i+1, i+3
            face_odd = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [1, 3] if i+j < n]

            if len(face_even) >= 2 and len(face_odd) >= 2:
                # Strong sheet signal if one face is hydrophobic
                if np.mean(face_even) > 2.0 or np.mean(face_odd) > 2.0:
                    for j in range(5):
                        if i + j < n:
                            sheet_signal[i + j] += 0.15

        # Also check for consecutive sheet formers
        sheet_strong = {'V', 'I', 'Y', 'F', 'W', 'T', 'L', 'C'}
        for i in range(n - 2):
            count = sum(1 for aa in sequence[i:i+3] if aa in sheet_strong)
            if count >= 2:
                for j in range(3):
                    if i + j < n:
                        sheet_signal[i + j] += 0.1

        return sheet_signal

    def _apply_breaker_rules(self, sequence: str, h_boost: List[float], e_boost: List[float]) -> Tuple[List[float], List[float]]:
        """Apply helix/sheet breaker rules."""
        n = len(sequence)
        h_mod = h_boost.copy()
        e_mod = e_boost.copy()

        for i, aa in enumerate(sequence):
            # Proline is a strong helix breaker (except at N-cap)
            if aa == 'P':
                h_mod[i] *= 0.5
                # But also breaks sheets
                e_mod[i] *= 0.8

            # Glycine destabilizes regular structure
            if aa == 'G':
                h_mod[i] *= 0.7
                e_mod[i] *= 0.8

        return h_mod, e_mod

    def predict(self, sequence: str) -> str:
        """Make balanced prediction."""
        sequence = sequence.upper()
        n = len(sequence)

        # Get all signals
        propensity_scores = self._get_propensity_scores(sequence)
        helix_pattern = self._helix_pattern_score(sequence)
        sheet_pattern = self._sheet_pattern_score(sequence)

        # Apply breaker rules
        helix_pattern, sheet_pattern = self._apply_breaker_rules(
            sequence, helix_pattern, sheet_pattern
        )

        # Combine scores
        predictions = []
        for i in range(n):
            h_prop, e_prop, c_prop = propensity_scores[i]

            # Total score = propensity + pattern boost
            h_total = h_prop + helix_pattern[i]
            e_total = e_prop + sheet_pattern[i]
            c_total = c_prop

            # Decision thresholds (calibrated)
            # Need clear winner for helix or sheet
            if h_total > e_total and h_total > c_total and h_total > 1.08:
                predictions.append('H')
            elif e_total > h_total * 0.95 and e_total > c_total and e_total > 1.12:
                # Slightly higher threshold for beta to avoid over-prediction
                predictions.append('E')
            else:
                predictions.append('C')

        # Smooth and enforce minimums
        predictions = self._smooth(predictions)
        predictions = self._enforce_lengths(predictions)

        return ''.join(predictions)

    def _smooth(self, ss: List[str]) -> List[str]:
        """Remove isolated predictions."""
        n = len(ss)
        result = ss.copy()

        for i in range(1, n - 1):
            if ss[i - 1] == ss[i + 1] and ss[i] != ss[i - 1]:
                result[i] = ss[i - 1]

        return result

    def _enforce_lengths(self, ss: List[str]) -> List[str]:
        """Enforce minimum segment lengths."""
        n = len(ss)
        result = ss.copy()

        i = 0
        while i < n:
            curr = result[i]
            j = i
            while j < n and result[j] == curr:
                j += 1
            length = j - i

            # Helix: min 4, Sheet: min 2
            if curr == 'H' and length < 4:
                for k in range(i, j):
                    result[k] = 'C'
            elif curr == 'E' and length < 2:
                for k in range(i, j):
                    result[k] = 'C'

            i = j

        return result


# =============================================================================
# FOLDER CLASS
# =============================================================================

class Z2ProteinFolderV7:
    """Z² protein folder v7 with balanced prediction."""

    def __init__(self):
        self.predictor = BalancedPredictor()

    def fold(self, sequence: str, name: str = "protein") -> dict:
        """Fold protein sequence."""
        sequence = sequence.upper()
        ss_string = self.predictor.predict(sequence)

        predictions = []
        for i, (aa, ss) in enumerate(zip(sequence, ss_string)):
            angles = Z2_ANGLES[ss]
            predictions.append({
                'residue': aa,
                'position': i,
                'ss_type': ss,
                'phi': angles['phi'] + np.random.normal(0, 5),
                'psi': angles['psi'] + np.random.normal(0, 5),
            })

        return {
            'name': name,
            'sequence': sequence,
            'length': len(sequence),
            'secondary_structure': ss_string,
            'predictions': predictions,
        }


# =============================================================================
# VALIDATION
# =============================================================================

VALIDATION_SET = {
    "lysozyme": {
        "sequence": "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGS"
                   "TDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVS"
                   "DGNGMNAWVAWRNRCKGTDVQAWIRGCRL",
        "dssp": "CEEECHHHHHHHHHHCCCCCCCCEEEECCHHHHCCCCEECCCCCCCCCCEE"
               "EEEEEECCEEEEEECCCCCCCCCHHHHHCCCCCCHHHHHHHHHCCCEEEECC"
               "EEECCCEEEECCEECCCC",
    },
    "insulin_b": {
        "sequence": "FVNQHLCGSHLVEALYLVCGERGFFYTPKT",
        "dssp": "CCCCHHHHHHHHHHHHHHHCCCCCCCCCC",
    },
    "myoglobin_frag": {
        "sequence": "VLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHL"
                   "KTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHK",
        "dssp": "CCHHHHHHHHHHHHHHHCCCCCCHHHHHHHHHHHCCCCHHHHHHHHHHCC"
               "CCCHHHHHHHHHHHHHHHHHCCCCHHHHHHHHHHHHHHHHHHHHHHHHC",
    },
    "sh3_domain": {
        "sequence": "AEETFYDAVDPTYFKDYAEAIKEDLQTHIGKNIFVDEYYFEVFGKPAAD"
                   "GLLDIKQVEGKPGWPVGPLRKN",
        "dssp": "CCEEEEEECCCCCCCEEEEEECCCCEEECCCCCCCEEEEEEEECCCCCCCC"
               "CCEEEEEEEECCCCCC",
    },
    "alpha_syn_nterm": {
        "sequence": "MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVH",
        "dssp": "CHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHC",
    },
    "abeta42_fibril": {
        "sequence": "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIA",
        "dssp": "CCCCCCCCCCCCCCCCEEEEECCCCCCCCCEEEEEEEEEEE",
    },
    "prion_helix": {
        "sequence": "HRYPNQVYYRPMDEYSNQNNFVHDCVNITIKQHTVTTTTKGENFTETDVK",
        "dssp": "HHHHHHHCCCCCCCCCCCCCCCHHHHHHHHHHHCCCCCCCCHHHHHHHHH",
    },
}


def calculate_accuracy(predicted: str, actual: str) -> dict:
    """Calculate accuracy metrics."""
    min_len = min(len(predicted), len(actual))
    predicted = predicted[:min_len]
    actual = actual[:min_len]

    correct = sum(p == a for p, a in zip(predicted, actual))
    q3 = correct / len(predicted)

    metrics = {}
    for ss in ['H', 'E', 'C']:
        tp = sum(1 for p, a in zip(predicted, actual) if p == ss and a == ss)
        fp = sum(1 for p, a in zip(predicted, actual) if p == ss and a != ss)
        fn = sum(1 for p, a in zip(predicted, actual) if p != ss and a == ss)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        metrics[ss] = {'f1': f1, 'precision': precision, 'recall': recall}

    return {'q3': q3, 'n': len(predicted), 'per_class': metrics,
            'predicted': predicted, 'actual': actual}


def validate():
    """Run validation."""
    print("=" * 78)
    print("Z² PROTEIN FOLDER v7.0 - BALANCED HYBRID")
    print("=" * 78)

    folder = Z2ProteinFolderV7()
    total_correct, total_n = 0, 0
    results = {}

    for name, data in VALIDATION_SET.items():
        result = folder.fold(data['sequence'], name)
        acc = calculate_accuracy(result['secondary_structure'], data['dssp'])
        results[name] = acc

        total_correct += int(acc['q3'] * acc['n'])
        total_n += acc['n']

        print(f"\n{name}: Q3 = {100*acc['q3']:.1f}%")
        print(f"  H F1: {acc['per_class']['H']['f1']:.2f}, E F1: {acc['per_class']['E']['f1']:.2f}")
        print(f"  Pred: {acc['predicted'][:50]}...")
        print(f"  True: {acc['actual'][:50]}...")

    overall_q3 = total_correct / total_n

    print(f"\n{'='*78}")
    print(f"OVERALL Q3: {100*overall_q3:.1f}%")
    print(f"{'='*78}")

    # Mean F1 per class
    h_f1 = np.mean([r['per_class']['H']['f1'] for r in results.values()])
    e_f1 = np.mean([r['per_class']['E']['f1'] for r in results.values()])
    c_f1 = np.mean([r['per_class']['C']['f1'] for r in results.values()])

    print(f"\nMean F1: H={h_f1:.2f}, E={e_f1:.2f}, C={c_f1:.2f}")

    print(f"\nVersion History:")
    print(f"  v1.0 (simple):     50.2%")
    print(f"  v5.0 (ensemble):   54.8%")
    print(f"  v6.0 (beta-heavy): 35.5%")
    print(f"  v7.0 (balanced):   {100*overall_q3:.1f}%")

    improvement = 100 * (overall_q3 - 0.502)
    print(f"\nImprovement over v1: {improvement:+.1f}%")

    # Save
    output = {
        'overall_q3': overall_q3,
        'per_protein': {k: {'q3': v['q3']} for k, v in results.items()},
        'mean_f1': {'H': h_f1, 'E': e_f1, 'C': c_f1},
    }
    output_path = Path(__file__).parent / "z2_folding_v7_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    return overall_q3


if __name__ == "__main__":
    validate()
