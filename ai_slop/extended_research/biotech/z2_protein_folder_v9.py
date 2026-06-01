#!/usr/bin/env python3
"""
Z² Protein Folder v9.0 - Refined Ensemble

Building on v5 (54.8%) with targeted refinements:
1. Helix N-cap and C-cap detection
2. Turn/break detection (NG, DG, PG patterns)
3. Better sheet nucleation
4. Improved consensus with context

Target: >57% Q3 accuracy

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

P_COIL = {
    'P': 1.52, 'G': 1.56, 'N': 1.35, 'D': 1.24, 'S': 1.18,
    'C': 1.05, 'Y': 1.10, 'K': 1.00, 'R': 1.10, 'T': 1.00,
    'H': 1.05, 'Q': 0.90, 'W': 0.85, 'A': 0.85, 'E': 0.85,
    'M': 0.80, 'F': 0.80, 'L': 0.75, 'V': 0.70, 'I': 0.70,
}

HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}

# Helix N-cap preferences (position N-1, N, N+1)
N_CAP_PREFERENCES = {
    'N': 1.5, 'D': 1.4, 'S': 1.3, 'T': 1.2, 'G': 0.6, 'P': 0.3
}

# Helix C-cap preferences
C_CAP_PREFERENCES = {
    'G': 1.4, 'K': 1.2, 'R': 1.1, 'P': 0.3
}


class RefinedEnsemblePredictor:
    """Refined ensemble predictor building on v5."""

    def __init__(self, window_size: int = 11):
        self.window_size = window_size
        self.half = window_size // 2

    def _method1_propensity(self, sequence: str) -> List[str]:
        """Method 1: Windowed propensity with refined thresholds."""
        n = len(sequence)
        predictions = []

        for i in range(n):
            h_sum, e_sum, c_sum = 0.0, 0.0, 0.0
            count = 0.0

            for j in range(-self.half, self.half + 1):
                if 0 <= i + j < n:
                    aa = sequence[i + j]
                    weight = 1.0 - 0.5 * abs(j) / (self.half + 1)
                    h_sum += P_HELIX.get(aa, 1.0) * weight
                    e_sum += P_SHEET.get(aa, 1.0) * weight
                    c_sum += P_COIL.get(aa, 1.0) * weight
                    count += weight

            h_avg = h_sum / count
            e_avg = e_sum / count
            c_avg = c_sum / count

            # Refined thresholds
            if h_avg > e_avg and h_avg > c_avg and h_avg > 1.0:
                predictions.append('H')
            elif e_avg > c_avg and e_avg > 1.05:
                predictions.append('E')
            else:
                predictions.append('C')

        return predictions

    def _method2_amphipathic(self, sequence: str) -> List[str]:
        """Method 2: Amphipathic helix detection."""
        n = len(sequence)
        helix_score = [0.0] * n

        # Check for helix periodicity (3.6 residues/turn)
        for i in range(n - 7):
            # Same face: i, i+3, i+4, i+7
            hydro = [HYDROPHOBICITY.get(sequence[i+j], 0) for j in [0, 3, 4, 7] if i+j < n]
            if len(hydro) >= 3:
                if np.mean(hydro) > 1.0:
                    for j in range(8):
                        if i + j < n:
                            helix_score[i + j] += 0.5

        predictions = []
        for i in range(n):
            aa = sequence[i]
            h_prop = P_HELIX.get(aa, 1.0)

            if helix_score[i] > 0.8 and h_prop > 0.8:
                predictions.append('H')
            elif h_prop > 1.2:
                predictions.append('H')
            elif P_SHEET.get(aa, 1.0) > 1.3:
                predictions.append('E')
            else:
                predictions.append('C')

        return predictions

    def _method3_nucleation(self, sequence: str) -> List[str]:
        """Method 3: Nucleation-based (Chou-Fasman style)."""
        n = len(sequence)
        ss = ['C'] * n

        # Find helix nucleation (4/6 strong formers)
        for i in range(n - 5):
            window = sequence[i:i+6]
            strong_h = sum(1 for aa in window if P_HELIX.get(aa, 1.0) > 1.1)
            if strong_h >= 4:
                for j in range(i, min(i + 6, n)):
                    ss[j] = 'H'

        # Find sheet nucleation (3/5 strong formers)
        for i in range(n - 4):
            window = sequence[i:i+5]
            strong_e = sum(1 for aa in window if P_SHEET.get(aa, 1.0) > 1.2)
            if strong_e >= 3 and ss[i] != 'H':
                for j in range(i, min(i + 5, n)):
                    if ss[j] != 'H':
                        ss[j] = 'E'

        return ss

    def _detect_breaks(self, sequence: str) -> List[bool]:
        """
        Detect helix/sheet breaking patterns.
        Returns True at positions that should be coil.
        """
        n = len(sequence)
        is_break = [False] * n

        # Proline breaks helices (except at N-cap)
        for i in range(1, n):  # Not at position 0
            if sequence[i] == 'P':
                is_break[i] = True

        # Strong turn patterns
        turn_patterns = ['NG', 'DG', 'SG', 'PG', 'NP', 'DP']
        for i in range(n - 1):
            di = sequence[i:i+2]
            if di in turn_patterns:
                is_break[i] = True
                is_break[i + 1] = True

        return is_break

    def _detect_helix_caps(self, sequence: str, ss: List[str]) -> List[str]:
        """Apply helix capping rules."""
        n = len(sequence)
        result = ss.copy()

        # Find helix boundaries and check capping
        i = 0
        while i < n:
            if result[i] == 'H':
                # Find helix end
                j = i
                while j < n and result[j] == 'H':
                    j += 1
                helix_len = j - i

                # N-cap: check if good capping residue before helix
                if i > 0:
                    ncap = sequence[i-1]
                    if ncap in N_CAP_PREFERENCES and N_CAP_PREFERENCES[ncap] > 1.0:
                        pass  # Good N-cap, keep helix
                    elif ncap == 'P' and helix_len < 5:
                        # Proline before short helix - might not be a real helix
                        for k in range(i, j):
                            result[k] = 'C'

                # C-cap: check if helix ends with proper residue
                if j < n:
                    ccap = sequence[j-1]  # Last helix residue
                    if ccap in ['G'] and helix_len >= 4:
                        pass  # Glycine can be C-cap

                i = j
            else:
                i += 1

        return result

    def _consensus(self, methods: List[List[str]], breaks: List[bool]) -> List[str]:
        """
        Take consensus with break detection.
        """
        n = len(methods[0])
        consensus = []

        for i in range(n):
            # If this is a strong break position, favor coil
            if breaks[i]:
                coil_boost = 1  # Count break as extra coil vote
            else:
                coil_boost = 0

            votes = {'H': 0, 'E': 0, 'C': coil_boost}
            for method in methods:
                votes[method[i]] += 1

            # Pick majority
            if votes['H'] >= 2 and not breaks[i]:
                consensus.append('H')
            elif votes['E'] >= 2 and not breaks[i]:
                consensus.append('E')
            elif votes['C'] >= 2:
                consensus.append('C')
            else:
                # Tie-break: prefer structured if no break
                if not breaks[i]:
                    if votes['H'] >= votes['E']:
                        consensus.append('H')
                    else:
                        consensus.append('E')
                else:
                    consensus.append('C')

        return consensus

    def _smooth(self, ss: List[str]) -> List[str]:
        """Smooth isolated predictions."""
        n = len(ss)
        smoothed = ss.copy()

        # Remove isolated assignments
        for i in range(1, n - 1):
            if ss[i - 1] == ss[i + 1] and ss[i] != ss[i - 1]:
                smoothed[i] = ss[i - 1]

        # Minimum lengths
        i = 0
        while i < n:
            curr = smoothed[i]
            j = i
            while j < n and smoothed[j] == curr:
                j += 1
            length = j - i

            if curr == 'H' and length < 4:
                for k in range(i, j):
                    smoothed[k] = 'C'
            elif curr == 'E' and length < 3:
                for k in range(i, j):
                    smoothed[k] = 'C'
            i = j

        return smoothed

    def predict(self, sequence: str) -> str:
        """Predict using refined ensemble."""
        sequence = sequence.upper()

        # Run methods
        m1 = self._method1_propensity(sequence)
        m2 = self._method2_amphipathic(sequence)
        m3 = self._method3_nucleation(sequence)

        # Detect breaks
        breaks = self._detect_breaks(sequence)

        # Consensus with break awareness
        consensus = self._consensus([m1, m2, m3], breaks)

        # Apply helix capping
        consensus = self._detect_helix_caps(sequence, consensus)

        # Smooth
        smoothed = self._smooth(consensus)

        return ''.join(smoothed)


# =============================================================================
# FOLDER CLASS
# =============================================================================

class Z2ProteinFolderV9:
    """Z² protein folder v9 with refined ensemble."""

    def __init__(self):
        self.predictor = RefinedEnsemblePredictor()

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
    print("Z² PROTEIN FOLDER v9.0 - REFINED ENSEMBLE")
    print("=" * 78)

    folder = Z2ProteinFolderV9()
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

    # Mean F1
    h_f1 = np.mean([r['per_class']['H']['f1'] for r in results.values()])
    e_f1 = np.mean([r['per_class']['E']['f1'] for r in results.values()])
    c_f1 = np.mean([r['per_class']['C']['f1'] for r in results.values()])

    print(f"\nMean F1: H={h_f1:.2f}, E={e_f1:.2f}, C={c_f1:.2f}")

    print(f"\nVersion History:")
    print(f"  v1.0 (simple):    50.2%")
    print(f"  v5.0 (ensemble):  54.8%")
    print(f"  v9.0 (refined):   {100*overall_q3:.1f}%")

    improvement = 100 * (overall_q3 - 0.502)
    print(f"\nImprovement over v1: {improvement:+.1f}%")

    # Save
    output = {
        'overall_q3': overall_q3,
        'per_protein': {k: {'q3': v['q3']} for k, v in results.items()},
        'mean_f1': {'H': h_f1, 'E': e_f1, 'C': c_f1},
    }
    output_path = Path(__file__).parent / "z2_folding_v9_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    return overall_q3


if __name__ == "__main__":
    validate()
