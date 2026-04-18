#!/usr/bin/env python3
"""
Z² Protein Folder v6.0 - Enhanced Beta Detection

Fixes from v5:
- Much better beta-sheet nucleation and extension
- Alternating hydrophobic pattern detection for sheets
- Improved consensus weighting
- Beta-turn detection

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
# PROPENSITIES (Chou-Fasman)
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

P_TURN = {
    'N': 1.56, 'G': 1.56, 'P': 1.52, 'D': 1.46, 'S': 1.43,
    'C': 1.19, 'Y': 1.14, 'K': 1.01, 'Q': 0.98, 'W': 0.96,
    'T': 0.96, 'R': 0.95, 'H': 0.95, 'E': 0.74, 'A': 0.66,
    'M': 0.60, 'L': 0.59, 'F': 0.58, 'V': 0.50, 'I': 0.47,
}

HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}


# =============================================================================
# ENHANCED PREDICTOR
# =============================================================================

class EnhancedPredictor:
    """Enhanced secondary structure predictor with improved beta detection."""

    def __init__(self, window_size: int = 11):
        self.window_size = window_size
        self.half = window_size // 2

    def _score_propensity(self, sequence: str) -> Tuple[List[float], List[float], List[float]]:
        """Calculate windowed propensity scores."""
        n = len(sequence)
        h_scores = []
        e_scores = []
        c_scores = []

        for i in range(n):
            h_sum, e_sum, count = 0.0, 0.0, 0.0

            for j in range(-self.half, self.half + 1):
                if 0 <= i + j < n:
                    aa = sequence[i + j]
                    # Center-weighted
                    weight = 1.0 - 0.4 * abs(j) / (self.half + 1)
                    h_sum += P_HELIX.get(aa, 1.0) * weight
                    e_sum += P_SHEET.get(aa, 1.0) * weight
                    count += weight

            h_avg = h_sum / count
            e_avg = e_sum / count
            c_avg = 1.0  # Baseline

            h_scores.append(h_avg)
            e_scores.append(e_avg)
            c_scores.append(c_avg)

        return h_scores, e_scores, c_scores

    def _detect_alternating_hydrophobic(self, sequence: str) -> List[float]:
        """
        Detect alternating hydrophobic pattern (characteristic of beta strands).
        In beta sheets, every other residue faces the same direction.
        """
        n = len(sequence)
        sheet_signal = [0.0] * n

        # Look for alternating hydrophobic pattern
        for i in range(n - 4):
            # Check positions i, i+2, i+4 (same face of sheet)
            face1 = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [0, 2, 4] if i+j < n]
            # Positions i+1, i+3 (opposite face)
            face2 = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [1, 3] if i+j < n]

            if len(face1) >= 2 and len(face2) >= 2:
                # Strong signal if one face is hydrophobic, other is mixed/polar
                mean1 = np.mean(face1)
                mean2 = np.mean(face2)

                # Pattern 1: Exposed strand (all similar)
                if abs(mean1) > 1.5 and abs(mean2) > 1.5:
                    for j in range(5):
                        if i + j < n:
                            sheet_signal[i + j] += 0.3

                # Pattern 2: Buried strand (alternating)
                if mean1 > 1.5 and mean2 < 0:
                    for j in range(5):
                        if i + j < n:
                            sheet_signal[i + j] += 0.5

                if mean2 > 1.5 and mean1 < 0:
                    for j in range(5):
                        if i + j < n:
                            sheet_signal[i + j] += 0.5

        return sheet_signal

    def _find_beta_nucleation(self, sequence: str, e_scores: List[float]) -> List[str]:
        """Find beta-sheet nucleation sites with improved sensitivity."""
        n = len(sequence)
        ss = ['C'] * n

        # Method 1: High propensity regions
        for i in range(n - 2):
            # 3-residue nucleation (very common in real beta sheets)
            if all(e_scores[i+j] > 1.1 for j in range(3) if i+j < n):
                for j in range(3):
                    if i + j < n:
                        ss[i + j] = 'E'

        # Method 2: Strong beta formers
        beta_strong = {'V', 'I', 'Y', 'F', 'W', 'L', 'T', 'C', 'M'}
        for i in range(n - 2):
            window = sequence[i:i+3]
            strong_count = sum(1 for aa in window if aa in beta_strong)
            if strong_count >= 2:
                for j in range(3):
                    if i + j < n and ss[i + j] == 'C':
                        ss[i + j] = 'E'

        return ss

    def _find_helix_nucleation(self, sequence: str, h_scores: List[float]) -> List[str]:
        """Find helix nucleation sites."""
        n = len(sequence)
        ss = ['C'] * n

        # Helix formers
        helix_strong = {'A', 'E', 'L', 'M', 'Q', 'K', 'R', 'H'}

        # Need 4 out of 6 strong helix formers
        for i in range(n - 5):
            window = sequence[i:i+6]
            strong_h = sum(1 for aa in window if aa in helix_strong or P_HELIX.get(aa, 1.0) > 1.1)
            if strong_h >= 4:
                for j in range(6):
                    if i + j < n:
                        ss[i + j] = 'H'

        return ss

    def _detect_turns(self, sequence: str) -> List[float]:
        """Detect turn regions (break regular structure)."""
        n = len(sequence)
        turn_score = [0.0] * n

        # Turn formers break helices and sheets
        turn_formers = {'P', 'G', 'N', 'D', 'S'}

        for i in range(n - 3):
            window = sequence[i:i+4]
            # Classic type I and II turns
            turn_signal = sum(1 for aa in window if aa in turn_formers)
            if turn_signal >= 2:
                for j in range(4):
                    if i + j < n:
                        turn_score[i + j] += 0.5

            # Proline at position i+1 is very common in turns
            if i + 1 < n and sequence[i + 1] == 'P':
                for j in range(4):
                    if i + j < n:
                        turn_score[i + j] += 0.3

        return turn_score

    def predict(self, sequence: str) -> str:
        """Predict secondary structure with enhanced beta detection."""
        sequence = sequence.upper()
        n = len(sequence)

        # Get base scores
        h_scores, e_scores, c_scores = self._score_propensity(sequence)

        # Beta-specific signals
        alt_hydro = self._detect_alternating_hydrophobic(sequence)

        # Turn detection
        turn_scores = self._detect_turns(sequence)

        # Nucleation sites
        helix_nuc = self._find_helix_nucleation(sequence, h_scores)
        beta_nuc = self._find_beta_nucleation(sequence, e_scores)

        # Combine all signals
        predictions = []
        for i in range(n):
            h_total = h_scores[i]
            e_total = e_scores[i] + alt_hydro[i]  # Add beta signal
            c_total = 1.0 + turn_scores[i]  # Turns promote coil

            # Nucleation boost
            if helix_nuc[i] == 'H':
                h_total += 0.3
            if beta_nuc[i] == 'E':
                e_total += 0.3

            # Proline and glycine rules
            aa = sequence[i]
            if aa == 'P':
                h_total *= 0.5  # Proline is helix breaker
                e_total *= 0.7  # Also disfavors sheet
            if aa == 'G':
                h_total *= 0.7
                e_total *= 0.7

            # Decision with calibrated thresholds
            if h_total > e_total and h_total > c_total and h_total > 1.05:
                predictions.append('H')
            elif e_total > c_total and e_total > 0.95:  # Lower threshold for beta
                predictions.append('E')
            else:
                predictions.append('C')

        # Post-processing
        predictions = self._smooth(predictions)
        predictions = self._enforce_minimum_lengths(predictions)

        return ''.join(predictions)

    def _smooth(self, ss: List[str]) -> List[str]:
        """Smooth isolated predictions."""
        n = len(ss)
        smoothed = ss.copy()

        # Remove single isolated residues
        for i in range(1, n - 1):
            if ss[i - 1] == ss[i + 1] and ss[i] != ss[i - 1]:
                smoothed[i] = ss[i - 1]

        return smoothed

    def _enforce_minimum_lengths(self, ss: List[str]) -> List[str]:
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

            # Helix minimum: 4 residues
            if curr == 'H' and length < 4:
                for k in range(i, j):
                    result[k] = 'C'
            # Sheet minimum: 2 residues (allowing short strands)
            elif curr == 'E' and length < 2:
                for k in range(i, j):
                    result[k] = 'C'

            i = j

        return result


# =============================================================================
# FOLDER CLASS
# =============================================================================

class Z2ProteinFolderV6:
    """Z² protein folder v6 with enhanced beta detection."""

    def __init__(self):
        self.predictor = EnhancedPredictor()

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
    print("Z² PROTEIN FOLDER v6.0 - ENHANCED BETA DETECTION")
    print("=" * 78)

    folder = Z2ProteinFolderV6()
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
    print(f"  v1.0 (simple):        50.2%")
    print(f"  v4.0 (full CF):       51.1%")
    print(f"  v5.0 (ensemble):      54.8%")
    print(f"  v6.0 (beta-enhanced): {100*overall_q3:.1f}%")

    improvement = 100 * (overall_q3 - 0.502)
    print(f"\nImprovement over v1: {improvement:+.1f}%")

    # Save
    output = {
        'overall_q3': overall_q3,
        'per_protein': {k: {'q3': v['q3']} for k, v in results.items()},
        'mean_f1': {'H': h_f1, 'E': e_f1, 'C': c_f1},
    }
    output_path = Path(__file__).parent / "z2_folding_v6_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    return overall_q3


if __name__ == "__main__":
    validate()
