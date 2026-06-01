#!/usr/bin/env python3
"""
Z² Protein Folder v4.0 - Full Chou-Fasman + Z² Angles

Implements the complete Chou-Fasman algorithm with:
1. Nucleation sites (4/6 helix formers, 3/5 sheet formers)
2. Extension rules
3. Boundary determination
4. Overlap resolution
5. Z² angle assignment for final structure

Copyright (C) 2026 Carl Zimmerman
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from pathlib import Path

# =============================================================================
# Z² ANGLES (VALIDATED)
# =============================================================================

Z2_ANGLES = {
    "H": {"phi": -57.0, "psi": -47.0},
    "E": {"phi": -129.0, "psi": 135.0},
    "C": {"phi": -70.0, "psi": 145.0},
}

# =============================================================================
# CHOU-FASMAN PROPENSITY PARAMETERS
# =============================================================================

# Helix propensity Pα
P_HELIX = {
    'E': 1.53, 'A': 1.45, 'L': 1.34, 'H': 1.24, 'M': 1.20,
    'Q': 1.17, 'W': 1.14, 'V': 1.14, 'F': 1.12, 'K': 1.07,
    'I': 1.00, 'D': 0.98, 'T': 0.82, 'S': 0.79, 'R': 0.79,
    'C': 0.77, 'N': 0.73, 'Y': 0.61, 'P': 0.59, 'G': 0.53,
}

# Sheet propensity Pβ
P_SHEET = {
    'M': 1.67, 'V': 1.65, 'I': 1.60, 'C': 1.30, 'Y': 1.29,
    'F': 1.28, 'Q': 1.23, 'L': 1.22, 'T': 1.20, 'W': 1.19,
    'A': 0.97, 'R': 0.90, 'G': 0.81, 'D': 0.80, 'K': 0.74,
    'S': 0.72, 'H': 0.71, 'N': 0.65, 'P': 0.62, 'E': 0.26,
}

# Turn propensity Pt
P_TURN = {
    'N': 1.56, 'G': 1.56, 'P': 1.52, 'D': 1.46, 'S': 1.43,
    'C': 1.19, 'Y': 1.14, 'K': 1.01, 'Q': 0.98, 'W': 0.96,
    'T': 0.96, 'R': 0.95, 'H': 0.95, 'E': 0.74, 'A': 0.66,
    'M': 0.60, 'F': 0.60, 'L': 0.59, 'V': 0.50, 'I': 0.47,
}

# Classification
HELIX_FORMERS = set(['E', 'A', 'L', 'H', 'M', 'Q', 'W', 'V', 'F'])
HELIX_INDIFFERENT = set(['K', 'I', 'D', 'T', 'S', 'R', 'C'])
HELIX_BREAKERS = set(['N', 'Y', 'P', 'G'])

SHEET_FORMERS = set(['M', 'V', 'I', 'C', 'Y', 'F', 'Q', 'L', 'T', 'W'])
SHEET_INDIFFERENT = set(['A', 'R', 'G', 'D', 'K', 'S', 'H'])
SHEET_BREAKERS = set(['N', 'P', 'E'])


# =============================================================================
# CHOU-FASMAN ALGORITHM
# =============================================================================

@dataclass
class Region:
    """A secondary structure region."""
    start: int
    end: int
    ss_type: str  # 'H', 'E', 'C'
    score: float


class ChouFasmanPredictor:
    """
    Full Chou-Fasman algorithm implementation.

    Steps:
    1. Find helix nucleation sites (4+ formers in 6 residue window)
    2. Extend helices until breakers
    3. Find sheet nucleation sites (3+ formers in 5 residue window)
    4. Extend sheets until breakers
    5. Resolve overlaps (higher Pα or Pβ wins)
    6. Assign remaining as coil
    """

    def __init__(self):
        self.min_helix_length = 4
        self.min_sheet_length = 3

    def _find_helix_nucleations(self, sequence: str) -> List[Tuple[int, int]]:
        """Find helix nucleation sites: 4+ helix formers in window of 6."""
        nucleations = []
        n = len(sequence)

        for i in range(n - 5):
            window = sequence[i:i+6]
            formers = sum(1 for aa in window if aa in HELIX_FORMERS)
            breakers = sum(1 for aa in window if aa in HELIX_BREAKERS)

            # Nucleation: 4+ formers and no more than 1 breaker
            if formers >= 4 and breakers <= 1:
                nucleations.append((i, i + 5))

        # Merge overlapping nucleations
        return self._merge_regions(nucleations)

    def _find_sheet_nucleations(self, sequence: str) -> List[Tuple[int, int]]:
        """Find sheet nucleation sites: 3+ sheet formers in window of 5."""
        nucleations = []
        n = len(sequence)

        for i in range(n - 4):
            window = sequence[i:i+5]
            formers = sum(1 for aa in window if aa in SHEET_FORMERS)
            breakers = sum(1 for aa in window if aa in SHEET_BREAKERS)

            # Nucleation: 3+ formers and no breakers
            if formers >= 3 and breakers == 0:
                nucleations.append((i, i + 4))

        return self._merge_regions(nucleations)

    def _merge_regions(self, regions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Merge overlapping regions."""
        if not regions:
            return []

        regions = sorted(regions)
        merged = [regions[0]]

        for start, end in regions[1:]:
            if start <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        return merged

    def _extend_helix(self, sequence: str, start: int, end: int) -> Tuple[int, int]:
        """Extend helix in both directions until broken."""
        n = len(sequence)

        # Extend left
        new_start = start
        while new_start > 0:
            aa = sequence[new_start - 1]
            # Stop if strong breaker or average Pα < 1.0
            if aa in HELIX_BREAKERS and aa not in ['N']:  # N can start helix
                break
            if P_HELIX.get(aa, 1.0) < 0.8:
                break
            new_start -= 1

        # Extend right
        new_end = end
        while new_end < n - 1:
            aa = sequence[new_end + 1]
            if aa in HELIX_BREAKERS:
                break
            if P_HELIX.get(aa, 1.0) < 0.8:
                break
            new_end += 1

        # Check overall Pα > 1.0
        region_seq = sequence[new_start:new_end+1]
        avg_p = np.mean([P_HELIX.get(aa, 1.0) for aa in region_seq])

        if avg_p < 1.0:
            return start, end  # Don't extend

        return new_start, new_end

    def _extend_sheet(self, sequence: str, start: int, end: int) -> Tuple[int, int]:
        """Extend sheet in both directions."""
        n = len(sequence)

        # Extend left
        new_start = start
        while new_start > 0:
            aa = sequence[new_start - 1]
            if aa in SHEET_BREAKERS:
                break
            if P_SHEET.get(aa, 1.0) < 0.8:
                break
            new_start -= 1

        # Extend right
        new_end = end
        while new_end < n - 1:
            aa = sequence[new_end + 1]
            if aa in SHEET_BREAKERS:
                break
            if P_SHEET.get(aa, 1.0) < 0.8:
                break
            new_end += 1

        # Check overall Pβ > 1.0
        region_seq = sequence[new_start:new_end+1]
        avg_p = np.mean([P_SHEET.get(aa, 1.0) for aa in region_seq])

        if avg_p < 1.0:
            return start, end

        return new_start, new_end

    def _resolve_overlaps(self, sequence: str, helix_regions: List[Region],
                          sheet_regions: List[Region]) -> List[Region]:
        """Resolve overlapping helix/sheet assignments."""
        n = len(sequence)
        assignment = ['C'] * n

        # Assign non-overlapping regions first
        for region in helix_regions + sheet_regions:
            for i in range(region.start, region.end + 1):
                if assignment[i] == 'C':
                    assignment[i] = region.ss_type

        # For overlaps, use higher propensity
        all_regions = helix_regions + sheet_regions
        for i in range(n):
            overlapping = [r for r in all_regions if r.start <= i <= r.end]
            if len(overlapping) > 1:
                # Compare propensities
                aa = sequence[i]
                p_h = P_HELIX.get(aa, 1.0)
                p_e = P_SHEET.get(aa, 1.0)

                if p_h > p_e:
                    assignment[i] = 'H'
                else:
                    assignment[i] = 'E'

        # Convert back to regions
        final_regions = []
        i = 0
        while i < n:
            ss = assignment[i]
            j = i
            while j < n and assignment[j] == ss:
                j += 1

            # Calculate average propensity for this region
            region_seq = sequence[i:j]
            if ss == 'H':
                score = np.mean([P_HELIX.get(aa, 1.0) for aa in region_seq])
            elif ss == 'E':
                score = np.mean([P_SHEET.get(aa, 1.0) for aa in region_seq])
            else:
                score = np.mean([P_TURN.get(aa, 1.0) for aa in region_seq])

            final_regions.append(Region(i, j - 1, ss, score))
            i = j

        return final_regions

    def _apply_length_rules(self, regions: List[Region]) -> List[Region]:
        """Apply minimum length rules."""
        refined = []
        for region in regions:
            length = region.end - region.start + 1
            if region.ss_type == 'H' and length < self.min_helix_length:
                refined.append(Region(region.start, region.end, 'C', region.score))
            elif region.ss_type == 'E' and length < self.min_sheet_length:
                refined.append(Region(region.start, region.end, 'C', region.score))
            else:
                refined.append(region)
        return refined

    def predict(self, sequence: str) -> str:
        """Predict secondary structure using Chou-Fasman algorithm."""
        sequence = sequence.upper()
        n = len(sequence)

        # Step 1: Find helix nucleation sites
        helix_nucs = self._find_helix_nucleations(sequence)

        # Step 2: Extend helices
        helix_regions = []
        for start, end in helix_nucs:
            new_start, new_end = self._extend_helix(sequence, start, end)
            region_seq = sequence[new_start:new_end+1]
            score = np.mean([P_HELIX.get(aa, 1.0) for aa in region_seq])
            helix_regions.append(Region(new_start, new_end, 'H', score))

        # Step 3: Find sheet nucleation sites
        sheet_nucs = self._find_sheet_nucleations(sequence)

        # Step 4: Extend sheets
        sheet_regions = []
        for start, end in sheet_nucs:
            new_start, new_end = self._extend_sheet(sequence, start, end)
            region_seq = sequence[new_start:new_end+1]
            score = np.mean([P_SHEET.get(aa, 1.0) for aa in region_seq])
            sheet_regions.append(Region(new_start, new_end, 'E', score))

        # Step 5: Resolve overlaps
        all_regions = self._resolve_overlaps(sequence, helix_regions, sheet_regions)

        # Step 6: Apply length rules
        all_regions = self._apply_length_rules(all_regions)

        # Convert to string
        ss = ['C'] * n
        for region in all_regions:
            for i in range(region.start, region.end + 1):
                ss[i] = region.ss_type

        return ''.join(ss)


# =============================================================================
# Z² PROTEIN FOLDER V4
# =============================================================================

class Z2ProteinFolderV4:
    """Z² protein folder using full Chou-Fasman + Z² angles."""

    def __init__(self):
        self.cf_predictor = ChouFasmanPredictor()

    def fold(self, sequence: str, name: str = "protein") -> dict:
        """Fold protein with Chou-Fasman + Z² geometry."""
        sequence = sequence.upper()

        # Get secondary structure
        ss_string = self.cf_predictor.predict(sequence)

        # Build predictions with Z² angles
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

        ss_counts = {
            'H': ss_string.count('H'),
            'E': ss_string.count('E'),
            'C': ss_string.count('C'),
        }

        return {
            'name': name,
            'sequence': sequence,
            'length': len(sequence),
            'secondary_structure': ss_string,
            'ss_composition': ss_counts,
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
    """Calculate Q3 accuracy."""
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
        metrics[ss] = {'precision': precision, 'recall': recall, 'f1': f1}

    return {'q3': q3, 'n': len(predicted), 'correct': correct, 'per_class': metrics,
            'predicted': predicted, 'actual': actual}


def validate():
    """Run validation."""
    print("=" * 78)
    print("Z² PROTEIN FOLDER v4.0 - FULL CHOU-FASMAN")
    print("=" * 78)

    folder = Z2ProteinFolderV4()
    total_correct, total_residues = 0, 0

    for name, data in VALIDATION_SET.items():
        result = folder.fold(data['sequence'], name)
        acc = calculate_accuracy(result['secondary_structure'], data['dssp'])

        total_correct += acc['correct']
        total_residues += acc['n']

        print(f"\n{name}:")
        print(f"  Q3: {100*acc['q3']:.1f}%")
        print(f"  H F1: {acc['per_class']['H']['f1']:.2f}, "
              f"E F1: {acc['per_class']['E']['f1']:.2f}")
        print(f"  Pred: {acc['predicted'][:50]}...")
        print(f"  True: {acc['actual'][:50]}...")

    overall_q3 = total_correct / total_residues

    print(f"\n{'='*78}")
    print(f"OVERALL Q3: {100*overall_q3:.1f}%")
    print(f"{'='*78}")

    print(f"\nComparison to previous versions:")
    print(f"  v1.0 (simple): 50.2%")
    print(f"  v4.0 (full CF): {100*overall_q3:.1f}%")

    return overall_q3


if __name__ == "__main__":
    validate()
