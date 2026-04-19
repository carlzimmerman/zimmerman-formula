#!/usr/bin/env python3
"""
Z² Protein Folding v3: AGGRESSIVE Geometric Approach

SPDX-License-Identifier: AGPL-3.0-or-later

v1 BruteFlow: 48.6% Q3
v2 Multi-method: 32.7% Q3 (worse!)

v3 Strategy: FOCUS on what Z² uniquely provides:
1. Codon geometry → contact prediction (keep from v1)
2. Z² angle quantization → backbone constraints
3. Aggressive parallel search

The key insight: single-sequence methods max out ~55-60% Q3.
To beat AlphaFold (~90%), we need MSA. But for orphan proteins
(no homologs), AlphaFold drops to ~70%.

TARGET: Beat AlphaFold on orphan-like conditions (single sequence).

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.optimize import minimize, basinhopping
from scipy.spatial.distance import pdist, squareform
from scipy.signal import find_peaks
from multiprocessing import Pool, cpu_count
import json
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² FUNDAMENTAL CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.79
Z2 = Z**2  # = 32π/3 ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 31.09°
THETA_Z2_DEG = np.degrees(THETA_Z2)

CA_CA = 3.8  # Å

print("="*80)
print("Z² PROTEIN FOLDING v3: AGGRESSIVE GEOMETRIC APPROACH")
print("="*80)
print(f"Z = {Z:.4f} Å | θ_Z² = {THETA_Z2_DEG:.2f}° | CPUs = {cpu_count()}")
print("="*80)

# ==============================================================================
# AMINO ACID DATA
# ==============================================================================

# GOR method-like parameters (simplified)
# These capture local sequence preferences for secondary structure
SS_PARAMS = {
    'H': {  # Helix formers
        'A': 1.4, 'E': 1.5, 'L': 1.2, 'M': 1.4, 'Q': 1.1, 'K': 1.2,
        'R': 1.0, 'F': 1.1, 'W': 1.1, 'I': 1.1, 'V': 1.0, 'D': 1.0,
        'H': 1.0, 'N': 0.7, 'T': 0.8, 'S': 0.8, 'C': 0.7, 'Y': 0.7,
        'G': 0.6, 'P': 0.6
    },
    'E': {  # Sheet formers
        'V': 1.7, 'I': 1.6, 'Y': 1.5, 'F': 1.4, 'W': 1.4, 'T': 1.2,
        'C': 1.2, 'L': 1.3, 'M': 1.1, 'Q': 1.1, 'A': 0.8, 'R': 0.9,
        'G': 0.8, 'K': 0.7, 'S': 0.8, 'N': 0.9, 'H': 0.9, 'D': 0.5,
        'E': 0.4, 'P': 0.6
    }
}

HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# Codon table for Z² geometry
GENETIC_CODE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}


# ==============================================================================
# Z² CODON GEOMETRY (from BruteFlow v1 - this worked!)
# ==============================================================================

class Z2CodonGeometry:
    """Map amino acids to Z² space via their codons."""

    def __init__(self):
        self.base_map = {'T': 0, 'C': 1, 'A': 2, 'G': 3}
        self.codon_vectors = {}
        self.aa_vectors = {}
        self._build_codon_space()

    def _build_codon_space(self):
        """Map codons to 3D Z² space."""
        for codon, aa in GENETIC_CODE.items():
            if aa == '*':
                continue

            b1 = self.base_map[codon[0]]
            b2 = self.base_map[codon[1]]
            b3 = self.base_map[codon[2]]

            theta1 = b1 * THETA_Z2
            theta2 = b2 * THETA_Z2
            theta3 = b3 * THETA_Z2 / 2  # Wobble

            x = np.cos(theta1) * np.sin(theta2 + theta3)
            y = np.sin(theta1) * np.sin(theta2 + theta3)
            z = np.cos(theta2 + theta3)

            self.codon_vectors[codon] = np.array([x, y, z]) * Z

        # Average over synonymous codons
        for aa in set(GENETIC_CODE.values()):
            if aa == '*':
                continue
            codons = [c for c, a in GENETIC_CODE.items() if a == aa]
            self.aa_vectors[aa] = np.mean([self.codon_vectors[c] for c in codons], axis=0)

    def get_contact_score(self, aa1, aa2):
        """Score contact likelihood from codon geometry."""
        if aa1 not in self.aa_vectors or aa2 not in self.aa_vectors:
            return 0.5
        v1 = self.aa_vectors[aa1]
        v2 = self.aa_vectors[aa2]
        # Dot product normalized by Z
        return np.dot(v1, v2) / (Z * Z)


# ==============================================================================
# IMPROVED SECONDARY STRUCTURE PREDICTOR
# ==============================================================================

class Z2SSPredictor:
    """
    Secondary structure prediction using:
    1. Local sequence propensities (GOR-like)
    2. Z² hydrophobic periodicity detection
    3. Helix/sheet nucleation patterns
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)
        self.codon_geom = Z2CodonGeometry()

    def predict(self):
        """Predict SS with multiple signals."""
        # Signal 1: Local propensities
        h_score, e_score = self._propensity_scores()

        # Signal 2: Hydrophobic periodicity (helix = 3.6, sheet = 2)
        helix_period = self._detect_periodicity(3.6)
        sheet_period = self._detect_periodicity(2.0)

        # Signal 3: Codon geometry clustering
        codon_signal = self._codon_clustering()

        # Combine signals
        ss = []
        for i in range(self.n):
            # Only BOOST from periodicity, never suppress (use max with 0)
            h = h_score[i] * (1 + 0.2 * max(0, helix_period[i]))
            e = e_score[i] * (1 + 0.2 * max(0, sheet_period[i]))

            # Codon geometry boost (only positive)
            h += 0.05 * max(0, codon_signal[i])
            e += 0.03 * max(0, codon_signal[i])

            # Proline breaks helix
            if self.sequence[i] == 'P':
                h *= 0.3

            # Glycine is flexible
            if self.sequence[i] == 'G':
                h *= 0.6
                e *= 0.8

            # Threshold decisions (calibrated from BruteFlow v1)
            if h > 1.02 and h > e * 1.1:
                ss.append('H')
            elif e > 1.05 and e > h * 1.1:
                ss.append('E')
            elif h > 0.98 and h > e:
                ss.append('H')
            elif e > 1.0 and e > h:
                ss.append('E')
            else:
                ss.append('C')

        # Post-processing: smooth short segments
        ss = self._smooth_ss(ss)

        return ''.join(ss)

    def _propensity_scores(self):
        """Window-based propensity calculation."""
        h_score = np.ones(self.n)
        e_score = np.ones(self.n)
        window = 7

        for i in range(self.n):
            start = max(0, i - window//2)
            end = min(self.n, i + window//2 + 1)

            h_vals = [SS_PARAMS['H'].get(self.sequence[j], 1.0)
                     for j in range(start, end)]
            e_vals = [SS_PARAMS['E'].get(self.sequence[j], 1.0)
                     for j in range(start, end)]

            h_score[i] = np.mean(h_vals)
            e_score[i] = np.mean(e_vals)

        return h_score, e_score

    def _detect_periodicity(self, period):
        """Detect hydrophobic periodicity at given period."""
        signal = np.zeros(self.n)
        hydro = np.array([HYDROPHOBICITY.get(aa, 0) for aa in self.sequence])

        for i in range(self.n):
            # Correlation with periodic pattern
            score = 0
            count = 0
            for offset in range(-8, 9):
                j = i + offset
                if 0 <= j < self.n and offset != 0:
                    phase = 2 * np.pi * offset / period
                    score += hydro[j] * np.cos(phase)
                    count += 1
            if count > 0:
                signal[i] = score / count

        # Normalize
        if signal.std() > 0:
            signal = (signal - signal.mean()) / signal.std()

        return np.clip(signal, -1, 1)

    def _codon_clustering(self):
        """Score based on codon geometry similarity."""
        signal = np.zeros(self.n)

        for i in range(self.n):
            score = 0
            for j in range(max(0, i-4), min(self.n, i+5)):
                if j != i:
                    score += self.codon_geom.get_contact_score(
                        self.sequence[i], self.sequence[j]
                    )
            signal[i] = score

        if signal.std() > 0:
            signal = (signal - signal.mean()) / signal.std()

        return signal

    def _smooth_ss(self, ss):
        """Remove isolated SS assignments."""
        ss = list(ss)

        # Pass 1: Remove isolated single residues
        for i in range(1, self.n - 1):
            if ss[i] != ss[i-1] and ss[i] != ss[i+1]:
                ss[i] = 'C'

        # Pass 2: Require 3+ for H/E
        for i in range(self.n):
            if ss[i] in 'HE':
                # Count consecutive
                count = 1
                for j in range(i-1, -1, -1):
                    if ss[j] == ss[i]:
                        count += 1
                    else:
                        break
                for j in range(i+1, self.n):
                    if ss[j] == ss[i]:
                        count += 1
                    else:
                        break

                if count < 3:
                    ss[i] = 'C'

        return ss


# ==============================================================================
# CONTACT PREDICTION USING Z² GEOMETRY
# ==============================================================================

class Z2ContactPredictor:
    """Predict contacts using codon geometry and hydrophobicity."""

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)
        self.codon_geom = Z2CodonGeometry()

    def predict(self, ss_string):
        """Predict contact matrix."""
        contacts = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(i + 4, self.n):
                # Base: codon geometry
                codon_score = self.codon_geom.get_contact_score(
                    self.sequence[i], self.sequence[j]
                )

                # Hydrophobic attraction
                h_i = HYDROPHOBICITY.get(self.sequence[i], 0)
                h_j = HYDROPHOBICITY.get(self.sequence[j], 0)
                hydro_score = (h_i + h_j) / 9.0

                # SS compatibility
                ss_i, ss_j = ss_string[i], ss_string[j]
                ss_score = 1.0
                if ss_i == ss_j == 'E':  # Sheet-sheet contacts
                    ss_score = 1.5
                elif ss_i == 'H' and ss_j == 'H':  # Helix-helix
                    ss_score = 1.2
                elif ss_i == 'C' or ss_j == 'C':  # Coil involved
                    ss_score = 0.8

                # Sequence separation factor
                sep = j - i
                sep_factor = np.exp(-sep / Z2) + 0.3 * np.exp(-sep / 10)

                # Combine
                score = (codon_score + 0.5) * (hydro_score + 0.5) * ss_score * sep_factor
                contacts[i, j] = contacts[j, i] = max(0, score)

        # Normalize
        if contacts.max() > 0:
            contacts = contacts / contacts.max()

        return contacts


# ==============================================================================
# STRUCTURE BUILDER WITH Z² CONSTRAINTS
# ==============================================================================

class Z2StructureBuilder:
    """Build 3D structure with Z² geometric constraints."""

    def __init__(self, sequence, ss_string, contacts):
        self.sequence = sequence
        self.ss = ss_string
        self.contacts = contacts
        self.n = len(sequence)

    def build(self, n_attempts=20):
        """Build structure using optimization."""
        best_coords = None
        best_energy = float('inf')
        self.n_attempts = n_attempts

        for attempt in range(n_attempts):
            # Initialize based on SS
            coords = self._initialize_structure(attempt)

            # Optimize
            result = self._optimize(coords)

            if result['energy'] < best_energy:
                best_energy = result['energy']
                best_coords = result['coords']

        return best_coords, best_energy

    def _initialize_structure(self, seed):
        """Initialize backbone coordinates from SS."""
        np.random.seed(seed)
        coords = np.zeros((self.n, 3))

        # Build sequentially following SS
        pos = np.zeros(3)
        direction = np.array([1.0, 0.0, 0.0])

        for i in range(self.n):
            coords[i] = pos.copy()

            # Next step depends on SS
            if self.ss[i] == 'H':
                # Helix: rotate and rise
                angle = 2 * np.pi / 3.6  # 100° per residue
                rise = 1.5

                # Rotation matrix around z
                c, s = np.cos(angle), np.sin(angle)
                direction = np.array([
                    c * direction[0] - s * direction[1],
                    s * direction[0] + c * direction[1],
                    0.0
                ])

                pos = pos + direction * 2.3 + np.array([0, 0, rise])

            elif self.ss[i] == 'E':
                # Sheet: extended, zigzag
                if i % 2 == 0:
                    pos = pos + np.array([CA_CA * 0.95, 0.2, 0])
                else:
                    pos = pos + np.array([CA_CA * 0.95, -0.2, 0])

            else:
                # Coil: somewhat random
                angle = np.random.uniform(-np.pi/2, np.pi/2)
                c, s = np.cos(angle), np.sin(angle)
                direction = np.array([
                    c * direction[0] - s * direction[1],
                    s * direction[0] + c * direction[1],
                    direction[2] + np.random.uniform(-0.3, 0.3)
                ])
                direction = direction / np.linalg.norm(direction)
                pos = pos + direction * CA_CA

        # Add noise for diversity
        coords += np.random.randn(self.n, 3) * (seed / self.n_attempts) * 3

        return coords

    def _optimize(self, coords_init):
        """Optimize structure with physics + Z² energy."""

        def energy(flat):
            coords = flat.reshape(-1, 3)
            dist = squareform(pdist(coords))

            E = 0.0

            # Bond lengths
            for i in range(self.n - 1):
                E += 50 * (dist[i, i+1] - CA_CA)**2

            # Contact satisfaction with Z-quantized distances
            for i in range(self.n):
                for j in range(i + 4, self.n):
                    d = dist[i, j]
                    p = self.contacts[i, j]

                    if p > 0.5:  # Strong predicted contact
                        # Target Z distance
                        E += 5 * p * (d - Z)**2
                    elif p > 0.3:  # Weak contact
                        # Target √2 × Z
                        E += 2 * p * (d - Z * np.sqrt(2))**2

            # Excluded volume (no clashes)
            for i in range(self.n):
                for j in range(i + 2, self.n):
                    if dist[i, j] < 3.0:
                        E += 100 * (3.0 - dist[i, j])**2

            # Compactness (radius of gyration)
            com = coords.mean(axis=0)
            rg = np.sqrt(np.mean(np.sum((coords - com)**2, axis=1)))
            rg_ideal = 2.2 * (self.n ** 0.38)
            E += 10 * (rg - rg_ideal)**2

            # Helix geometry: i to i+4 contact at ~5.4 Å
            for i in range(self.n - 4):
                if self.ss[i] == 'H' and self.ss[i+4] == 'H':
                    d_i4 = dist[i, i+4]
                    E += 5 * (d_i4 - 5.4)**2

            # Sheet geometry: parallel strands
            for i in range(self.n):
                if self.ss[i] == 'E':
                    for j in range(i + 4, self.n):
                        if self.ss[j] == 'E' and self.contacts[i, j] > 0.4:
                            # Sheet contact should be ~4.7-5.0 Å
                            E += 3 * (dist[i, j] - 4.8)**2

            return E

        # Optimize
        result = minimize(energy, coords_init.flatten(), method='L-BFGS-B',
                         options={'maxiter': 2000, 'ftol': 1e-8})

        return {
            'coords': result.x.reshape(-1, 3),
            'energy': result.fun
        }


# ==============================================================================
# MAIN FOLDER CLASS
# ==============================================================================

class Z2FolderV3:
    """Main folding class combining all components."""

    def __init__(self, sequence, name='protein'):
        self.sequence = sequence
        self.name = name
        self.n = len(sequence)

    def fold(self, verbose=True):
        """Perform structure prediction."""
        start = time.time()

        if verbose:
            print(f"\nFolding {self.name} ({self.n} residues)...")

        # Step 1: SS prediction
        ss_pred = Z2SSPredictor(self.sequence)
        ss = ss_pred.predict()
        if verbose:
            print(f"  SS: {ss}")

        # Step 2: Contact prediction
        contact_pred = Z2ContactPredictor(self.sequence)
        contacts = contact_pred.predict(ss)

        # Step 3: Structure building
        builder = Z2StructureBuilder(self.sequence, ss, contacts)
        coords, energy = builder.build(n_attempts=15)

        elapsed = time.time() - start

        # Compute radius of gyration
        com = coords.mean(axis=0)
        rg = np.sqrt(np.mean(np.sum((coords - com)**2, axis=1)))

        return {
            'name': self.name,
            'sequence': self.sequence,
            'length': self.n,
            'secondary_structure': ss,
            'coordinates': coords,
            'energy': energy,
            'radius_of_gyration': rg,
            'elapsed_seconds': elapsed
        }


# ==============================================================================
# EVALUATION
# ==============================================================================

def compute_q3(pred_ss, known_ss):
    """Compute Q3 accuracy."""
    if len(pred_ss) != len(known_ss):
        return 0.0

    def normalize(s):
        return ''.join('H' if c in 'HG' else 'E' if c in 'EB' else 'C' for c in s.upper())

    p, k = normalize(pred_ss), normalize(known_ss)
    return 100.0 * sum(a == b for a, b in zip(p, k)) / len(k)


# ==============================================================================
# TEST SET
# ==============================================================================

PROTEINS = {
    'villin_hp35': {
        'seq': 'LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF',
        'ss': 'CHHHHHHHHHHCCHHHHHHHHHHHHHHHHHHHHHC'  # 35 residues
    },
    'gb1': {
        'seq': 'MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE',
        'ss': 'CEEEEEECCCCCCEEEEEECCCCHHHHHHHHHCCCCCEEEEEECCCCCEEEEEEEC'  # 56 residues
    },
    'insulin_b': {
        'seq': 'FVNQHLCGSHLVEALYLVCGERGFFYTPKT',
        'ss': 'CCCCHHHHHHHHHHHHHHHHHCCEEEEECC'  # 30 residues
    },
    'ubiquitin': {
        'seq': 'MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG',
        'ss': 'CEEEEEECCCCCEEEEECCCCCEEEEEECCCCCCEEEECCCCCCCCCCCCCEEEEEEECCCCCCCCEEEEEEEECC'  # 76 residues
    },
    'trp_cage': {
        'seq': 'NLYIQWLKDGGPSSGRPPPS',
        'ss': 'CCHHHHHHHHCCCCCCHHHC'  # 20 residues
    },
    'ww_domain': {
        'seq': 'KLPPGWEKRMSRSSGRVYYFNHITNASQWERPS',
        'ss': 'CCCCCEEEECCCCEEEECCCCCCEEEECCCCCC'  # 33 residues
    }
}


def main():
    print("\n" + "="*80)
    print("Z² FOLDING v3 - AGGRESSIVE RUN")
    print("="*80)

    results = {}

    for name, data in PROTEINS.items():
        print(f"\n{'─'*60}")
        print(f"Protein: {name}")

        folder = Z2FolderV3(data['seq'], name)
        result = folder.fold(verbose=True)

        q3 = compute_q3(result['secondary_structure'], data['ss'])
        result['known_ss'] = data['ss']
        result['q3'] = q3

        print(f"  Known:     {data['ss']}")
        print(f"  Q3:        {q3:.1f}%")
        print(f"  Rg:        {result['radius_of_gyration']:.1f} Å")
        print(f"  Time:      {result['elapsed_seconds']:.1f}s")

        results[name] = {
            'name': name,
            'pred_ss': result['secondary_structure'],
            'known_ss': data['ss'],
            'q3': q3,
            'rg': result['radius_of_gyration'],
            'energy': result['energy'],
            'time': result['elapsed_seconds']
        }

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    q3s = [r['q3'] for r in results.values()]
    for name, r in results.items():
        print(f"  {name:15s}: {r['q3']:5.1f}%")

    print(f"\n  Average Q3: {np.mean(q3s):.1f}%")
    print(f"  Best:       {max(q3s):.1f}%")
    print(f"  Worst:      {min(q3s):.1f}%")

    # Save
    output = {
        'framework': 'Z² Folding v3',
        'timestamp': datetime.now().isoformat(),
        'Z2': Z2,
        'results': results
    }

    with open('z2_folding_v3_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\nSaved to z2_folding_v3_results.json")

    return results


if __name__ == '__main__':
    main()
