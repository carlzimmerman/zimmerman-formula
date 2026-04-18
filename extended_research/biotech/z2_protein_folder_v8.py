#!/usr/bin/env python3
"""
Z² Protein Folder v8.0 - Meta-Ensemble

Key insight: Different methods excel at different structures.
- Method A (helix-tuned): Good at detecting alpha helices
- Method B (sheet-tuned): Good at detecting beta sheets
- Method C (propensity): Good baseline

Combine with confidence-weighted voting.

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
# PROPENSITIES
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


class MetaEnsemblePredictor:
    """Meta-ensemble combining multiple specialized predictors."""

    def __init__(self):
        self.window = 11
        self.half = self.window // 2

    def _method_helix_tuned(self, sequence: str) -> List[Tuple[str, float]]:
        """
        Helix-tuned predictor (from v5 logic).
        Returns (prediction, confidence) tuples.
        """
        n = len(sequence)
        results = []

        # Calculate helix propensity scores
        for i in range(n):
            h_score = 0.0
            e_score = 0.0
            count = 0.0

            for j in range(-self.half, self.half + 1):
                if 0 <= i + j < n:
                    aa = sequence[i + j]
                    w = 1.0 - 0.5 * abs(j) / (self.half + 1)
                    h_score += P_HELIX.get(aa, 1.0) * w
                    e_score += P_SHEET.get(aa, 1.0) * w
                    count += w

            h_avg = h_score / count
            e_avg = e_score / count

            # Helix-biased decision
            if h_avg > 1.1 and h_avg > e_avg:
                conf = min((h_avg - 1.0) / 0.5, 1.0)  # Confidence
                results.append(('H', conf))
            elif e_avg > 1.15:
                results.append(('E', 0.5))  # Lower confidence for sheet in helix-tuned
            else:
                results.append(('C', 0.6))

        return results

    def _method_sheet_tuned(self, sequence: str) -> List[Tuple[str, float]]:
        """
        Sheet-tuned predictor.
        Uses alternating hydrophobic pattern detection.
        """
        n = len(sequence)
        results = []

        # Sheet pattern scores
        sheet_signal = [0.0] * n

        # Alternating hydrophobic detection
        for i in range(n - 4):
            face_even = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [0, 2, 4] if i+j < n]
            face_odd = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [1, 3] if i+j < n]

            if len(face_even) >= 2 and len(face_odd) >= 2:
                # Alternating pattern
                if (np.mean(face_even) > 2.0 and np.mean(face_odd) < 0) or \
                   (np.mean(face_odd) > 2.0 and np.mean(face_even) < 0):
                    for j in range(5):
                        if i + j < n:
                            sheet_signal[i + j] += 0.5

                # Exposed strand (all hydrophobic)
                if np.mean(face_even) > 1.5 and np.mean(face_odd) > 1.5:
                    for j in range(5):
                        if i + j < n:
                            sheet_signal[i + j] += 0.3

        # Strong beta formers
        sheet_strong = {'V', 'I', 'Y', 'F', 'W', 'T', 'L', 'C', 'M'}
        for i in range(n - 2):
            count = sum(1 for aa in sequence[i:i+3] if aa in sheet_strong)
            if count >= 2:
                for j in range(3):
                    if i + j < n:
                        sheet_signal[i + j] += 0.3

        # Make predictions
        for i in range(n):
            e_prop = 0.0
            count = 0.0
            for j in range(-self.half, self.half + 1):
                if 0 <= i + j < n:
                    w = 1.0 - 0.5 * abs(j) / (self.half + 1)
                    e_prop += P_SHEET.get(sequence[i + j], 1.0) * w
                    count += w
            e_avg = e_prop / count

            total_e = e_avg + sheet_signal[i]

            if total_e > 1.3:
                conf = min((total_e - 1.0) / 0.5, 1.0)
                results.append(('E', conf))
            elif sheet_signal[i] > 0.5:
                results.append(('E', 0.6))
            elif P_HELIX.get(sequence[i], 1.0) > 1.2:
                results.append(('H', 0.5))  # Lower conf for helix in sheet-tuned
            else:
                results.append(('C', 0.6))

        return results

    def _method_propensity(self, sequence: str) -> List[Tuple[str, float]]:
        """Basic propensity method."""
        n = len(sequence)
        results = []

        for i in range(n):
            h_score, e_score, count = 0.0, 0.0, 0.0

            for j in range(-self.half, self.half + 1):
                if 0 <= i + j < n:
                    aa = sequence[i + j]
                    w = 1.0 - 0.5 * abs(j) / (self.half + 1)
                    h_score += P_HELIX.get(aa, 1.0) * w
                    e_score += P_SHEET.get(aa, 1.0) * w
                    count += w

            h_avg = h_score / count
            e_avg = e_score / count

            if h_avg > e_avg and h_avg > 1.05:
                results.append(('H', 0.7))
            elif e_avg > 1.1:
                results.append(('E', 0.7))
            else:
                results.append(('C', 0.7))

        return results

    def _combine_predictions(self, methods: List[List[Tuple[str, float]]]) -> List[str]:
        """
        Combine predictions using confidence-weighted voting.
        """
        n = len(methods[0])
        combined = []

        for i in range(n):
            votes = {'H': 0.0, 'E': 0.0, 'C': 0.0}

            for method in methods:
                pred, conf = method[i]
                votes[pred] += conf

            # Pick highest weighted vote
            best = max(votes.keys(), key=lambda k: votes[k])
            combined.append(best)

        return combined

    def _smooth(self, ss: List[str]) -> List[str]:
        """Smooth isolated predictions."""
        n = len(ss)
        result = ss.copy()

        # Remove single isolated residues
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

            if curr == 'H' and length < 4:
                for k in range(i, j):
                    result[k] = 'C'
            elif curr == 'E' and length < 2:
                for k in range(i, j):
                    result[k] = 'C'

            i = j

        return result

    def predict(self, sequence: str) -> str:
        """Make meta-ensemble prediction."""
        sequence = sequence.upper()

        # Run all methods
        m_helix = self._method_helix_tuned(sequence)
        m_sheet = self._method_sheet_tuned(sequence)
        m_prop = self._method_propensity(sequence)

        # Combine with confidence weighting
        combined = self._combine_predictions([m_helix, m_sheet, m_prop])

        # Post-process
        combined = self._smooth(combined)
        combined = self._enforce_lengths(combined)

        return ''.join(combined)


# =============================================================================
# FOLDER CLASS
# =============================================================================

class Z2ProteinFolderV8:
    """Z² protein folder v8 with meta-ensemble."""

    def __init__(self):
        self.predictor = MetaEnsemblePredictor()

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
    print("Z² PROTEIN FOLDER v8.0 - META-ENSEMBLE")
    print("=" * 78)

    folder = Z2ProteinFolderV8()
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
    print(f"  v1.0 (simple):       50.2%")
    print(f"  v5.0 (ensemble):     54.8%")
    print(f"  v7.0 (balanced):     50.4%")
    print(f"  v8.0 (meta-ens):     {100*overall_q3:.1f}%")

    improvement = 100 * (overall_q3 - 0.502)
    print(f"\nImprovement over v1: {improvement:+.1f}%")

    # Save
    output = {
        'overall_q3': overall_q3,
        'per_protein': {k: {'q3': v['q3']} for k, v in results.items()},
        'mean_f1': {'H': h_f1, 'E': e_f1, 'C': c_f1},
    }
    output_path = Path(__file__).parent / "z2_folding_v8_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    return overall_q3


if __name__ == "__main__":
    validate()
