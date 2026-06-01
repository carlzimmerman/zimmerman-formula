#!/usr/bin/env python3
"""
Z² Protein Folding v4: CODON GEOMETRY FIRST

SPDX-License-Identifier: AGPL-3.0-or-later

v1 BruteFlow: 48.6% Q3 (best so far!)
v2: 32.7% (too complex)
v3: 45.2% (better but not best)

v4 Strategy: MAXIMIZE codon geometry usage:
- Codon geometry predicts SS (not just propensity)
- Codon geometry predicts contacts
- Z² angles constrain backbone

KEY HYPOTHESIS:
===============
The genetic code evolved with protein folding in mind.
Codons that are close in Z² space might encode residues
that have similar structural properties.

This is UNIQUE information that no other method uses!

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.optimize import minimize
from scipy.spatial.distance import pdist, squareform
from multiprocessing import Pool, cpu_count
import json
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2
THETA_Z2 = np.pi / Z
CA_CA = 3.8

print("="*80)
print("Z² FOLDING v4: CODON GEOMETRY FIRST")
print("="*80)
print(f"Z = {Z:.4f} | θ_Z² = {np.degrees(THETA_Z2):.2f}° | CPUs = {cpu_count()}")

# ==============================================================================
# GENETIC CODE
# ==============================================================================

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

# Amino acid properties
HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# ==============================================================================
# Z² CODON SPACE
# ==============================================================================

class Z2CodonSpace:
    """
    Maps codons and amino acids to Z² geometric space.

    The Z² codon space is a 3D representation where:
    - Each base position contributes an angle multiple of θ_Z²
    - Similar codons are close in space
    - Similar amino acids cluster together
    """

    def __init__(self):
        self.base_map = {'T': 0, 'C': 1, 'A': 2, 'G': 3}
        self._build_space()

    def _build_space(self):
        """Build the Z² codon space."""
        self.codon_vec = {}
        self.aa_vec = {}
        self.aa_codons = {}

        # Map each codon to 3D space
        for codon, aa in GENETIC_CODE.items():
            if aa == '*':
                continue

            b1, b2, b3 = [self.base_map[b] for b in codon]

            # Z² angular embedding
            theta1 = b1 * THETA_Z2
            theta2 = b2 * THETA_Z2
            theta3 = b3 * THETA_Z2 / 2  # Wobble position has less weight

            # Spherical-like coordinates
            x = np.cos(theta1) * np.sin(theta2 + theta3)
            y = np.sin(theta1) * np.sin(theta2 + theta3)
            z = np.cos(theta2 + theta3)

            self.codon_vec[codon] = np.array([x, y, z]) * Z

            # Group by amino acid
            if aa not in self.aa_codons:
                self.aa_codons[aa] = []
            self.aa_codons[aa].append(codon)

        # Average position for each amino acid
        for aa, codons in self.aa_codons.items():
            self.aa_vec[aa] = np.mean([self.codon_vec[c] for c in codons], axis=0)

        # Compute pairwise AA distances in Z² space
        self.aa_dist = {}
        for aa1 in self.aa_vec:
            for aa2 in self.aa_vec:
                d = np.linalg.norm(self.aa_vec[aa1] - self.aa_vec[aa2])
                self.aa_dist[(aa1, aa2)] = d

        # Compute SS propensity from Z² geometry
        self._compute_z2_propensity()

    def _compute_z2_propensity(self):
        """
        Derive SS propensity from Z² position.

        Hypothesis: Position in Z² space correlates with SS preference.
        - Higher z-component → helix (stacking)
        - Lower z-component → sheet (planar)
        """
        self.helix_prop = {}
        self.sheet_prop = {}

        z_coords = {aa: self.aa_vec[aa][2] for aa in self.aa_vec}
        z_min, z_max = min(z_coords.values()), max(z_coords.values())

        for aa in self.aa_vec:
            z_norm = (z_coords[aa] - z_min) / (z_max - z_min + 1e-8)

            # Helix prefers intermediate z (amphipathic)
            self.helix_prop[aa] = 1.0 - 2 * abs(z_norm - 0.5)

            # Sheet prefers low z (extended)
            self.sheet_prop[aa] = 1.0 - z_norm

            # Add hydrophobicity contribution
            h = HYDROPHOBICITY.get(aa, 0) / 4.5  # normalize
            self.helix_prop[aa] += 0.3 * h
            self.sheet_prop[aa] += 0.2 * abs(h)  # both hydrophobic and polar can sheet

    def contact_score(self, aa1, aa2):
        """Score contact likelihood from Z² distance."""
        if aa1 not in self.aa_vec or aa2 not in self.aa_vec:
            return 0.5

        # Closer in Z² space → more likely to contact
        d = self.aa_dist.get((aa1, aa2), Z)
        return np.exp(-d / Z) + 0.3


# ==============================================================================
# SS PREDICTOR USING Z² GEOMETRY
# ==============================================================================

class Z2SSPredictor:
    """SS prediction using Z² codon geometry."""

    def __init__(self, sequence, z2space):
        self.seq = sequence
        self.n = len(sequence)
        self.z2 = z2space

    def predict(self):
        """Predict secondary structure."""
        # Get Z²-derived propensities
        h_z2 = np.array([self.z2.helix_prop.get(aa, 0.5) for aa in self.seq])
        e_z2 = np.array([self.z2.sheet_prop.get(aa, 0.5) for aa in self.seq])

        # Window smoothing
        window = 5
        h_smooth = np.convolve(h_z2, np.ones(window)/window, mode='same')
        e_smooth = np.convolve(e_z2, np.ones(window)/window, mode='same')

        # Detect helical periodicity (3.6 residue)
        helix_signal = self._helix_periodicity()

        # Detect sheet alternation (2 residue)
        sheet_signal = self._sheet_alternation()

        # Combine
        h_score = h_smooth + 0.3 * helix_signal
        e_score = e_smooth + 0.3 * sheet_signal

        # Assign SS
        ss = []
        for i in range(self.n):
            # Special cases
            if self.seq[i] == 'P':  # Proline breaks helix
                h_score[i] *= 0.4
            if self.seq[i] == 'G':  # Glycine is flexible
                h_score[i] *= 0.7
                e_score[i] *= 0.8

            # Decision
            if h_score[i] > e_score[i] + 0.05 and h_score[i] > 0.5:
                ss.append('H')
            elif e_score[i] > h_score[i] + 0.05 and e_score[i] > 0.55:
                ss.append('E')
            elif h_score[i] > 0.45 and h_score[i] > e_score[i]:
                ss.append('H')
            elif e_score[i] > 0.5:
                ss.append('E')
            else:
                ss.append('C')

        # Smooth short segments
        ss = self._smooth(ss)

        return ''.join(ss)

    def _helix_periodicity(self):
        """Detect 3.6-residue hydrophobic periodicity."""
        hydro = np.array([HYDROPHOBICITY.get(aa, 0) for aa in self.seq])
        signal = np.zeros(self.n)

        for i in range(self.n):
            score = 0
            count = 0
            for offset in range(-7, 8):
                j = i + offset
                if 0 <= j < self.n and offset != 0:
                    # 3.6-residue period
                    phase = 2 * np.pi * offset / 3.6
                    score += hydro[j] * np.cos(phase)
                    count += 1
            if count > 0:
                signal[i] = max(0, score / count)  # Only positive signal

        # Normalize
        if signal.max() > 0:
            signal = signal / signal.max()

        return signal

    def _sheet_alternation(self):
        """Detect alternating hydrophobic/polar pattern."""
        hydro = np.array([HYDROPHOBICITY.get(aa, 0) for aa in self.seq])
        signal = np.zeros(self.n)

        for i in range(1, self.n - 1):
            # Alternating pattern
            if (hydro[i-1] > 0) != (hydro[i] > 0):
                signal[i] += 0.3
            if (hydro[i] > 0) != (hydro[i+1] > 0):
                signal[i] += 0.3

        return signal

    def _smooth(self, ss):
        """Remove short isolated segments."""
        ss = list(ss)

        # Pass 1: isolated residues
        for i in range(1, self.n - 1):
            if ss[i] != ss[i-1] and ss[i] != ss[i+1]:
                ss[i] = 'C'

        # Pass 2: require 3+ consecutive for H/E
        i = 0
        while i < self.n:
            if ss[i] in 'HE':
                # Count segment
                j = i
                while j < self.n and ss[j] == ss[i]:
                    j += 1
                if j - i < 3:
                    for k in range(i, j):
                        ss[k] = 'C'
                i = j
            else:
                i += 1

        return ss


# ==============================================================================
# CONTACT PREDICTOR
# ==============================================================================

class Z2ContactPredictor:
    """Predict contacts using Z² codon geometry."""

    def __init__(self, sequence, z2space, ss_string):
        self.seq = sequence
        self.n = len(sequence)
        self.z2 = z2space
        self.ss = ss_string

    def predict(self):
        """Predict contact probability matrix."""
        contacts = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(i + 4, self.n):  # Minimum sequence separation
                # Z² geometry score
                z2_score = self.z2.contact_score(self.seq[i], self.seq[j])

                # Hydrophobic interaction
                h_i = HYDROPHOBICITY.get(self.seq[i], 0)
                h_j = HYDROPHOBICITY.get(self.seq[j], 0)
                if h_i > 0 and h_j > 0:  # Both hydrophobic
                    hydro_score = 0.3 * (h_i + h_j) / 9.0
                elif h_i < -2 and h_j < -2:  # Both charged (salt bridge)
                    if (h_i < 0) != (h_j < 0):  # Opposite charge
                        hydro_score = 0.2
                    else:
                        hydro_score = -0.1  # Same charge repels
                else:
                    hydro_score = 0

                # SS compatibility
                ss_i, ss_j = self.ss[i], self.ss[j]
                ss_score = 0.5
                if ss_i == 'E' and ss_j == 'E':
                    # Sheet-sheet contacts (beta hairpin/strand pairing)
                    ss_score = 0.8
                elif ss_i == 'H' and ss_j == 'H':
                    # Helix-helix packing
                    ss_score = 0.6
                elif ss_i == 'C' or ss_j == 'C':
                    # Loops are flexible
                    ss_score = 0.4

                # Sequence separation penalty
                sep = j - i
                sep_factor = np.exp(-sep / Z2) + 0.2 * np.exp(-sep / 15)

                # Combine
                score = z2_score * (1 + hydro_score) * ss_score * sep_factor
                contacts[i, j] = contacts[j, i] = max(0, min(1, score))

        return contacts


# ==============================================================================
# STRUCTURE BUILDER
# ==============================================================================

class Z2StructureBuilder:
    """Build 3D structure with Z² constraints."""

    def __init__(self, sequence, ss, contacts):
        self.seq = sequence
        self.ss = ss
        self.contacts = contacts
        self.n = len(sequence)

    def build(self, n_models=20):
        """Build and optimize structure."""
        best_coords = None
        best_energy = float('inf')

        for model in range(n_models):
            coords = self._init_structure(model)
            result = self._optimize(coords)

            if result['energy'] < best_energy:
                best_energy = result['energy']
                best_coords = result['coords']

        return best_coords, best_energy

    def _init_structure(self, seed):
        """Initialize from SS."""
        np.random.seed(seed)
        coords = np.zeros((self.n, 3))

        pos = np.zeros(3)
        direction = np.array([1.0, 0.0, 0.0])

        for i in range(self.n):
            coords[i] = pos.copy()

            if self.ss[i] == 'H':
                # Helix geometry
                angle = 2 * np.pi / 3.6
                rise = 1.5
                c, s = np.cos(angle), np.sin(angle)
                direction = np.array([c * direction[0] - s * direction[1],
                                     s * direction[0] + c * direction[1], 0])
                pos = pos + direction * 2.3 + np.array([0, 0, rise])

            elif self.ss[i] == 'E':
                # Sheet geometry
                if i % 2 == 0:
                    pos = pos + np.array([CA_CA * 0.95, 0.15, 0])
                else:
                    pos = pos + np.array([CA_CA * 0.95, -0.15, 0])

            else:
                # Coil
                angle = np.random.uniform(-0.5, 0.5)
                c, s = np.cos(angle), np.sin(angle)
                direction = np.array([c * direction[0] - s * direction[1],
                                     s * direction[0] + c * direction[1],
                                     direction[2] + np.random.uniform(-0.2, 0.2)])
                direction = direction / (np.linalg.norm(direction) + 1e-8)
                pos = pos + direction * CA_CA

        # Add diversity
        coords += np.random.randn(self.n, 3) * (1 + seed * 0.2)

        return coords

    def _optimize(self, coords_init):
        """Energy minimization."""

        def energy(flat):
            coords = flat.reshape(-1, 3)
            dist = squareform(pdist(coords))

            E = 0

            # Bond lengths
            for i in range(self.n - 1):
                E += 100 * (dist[i, i+1] - CA_CA)**2

            # Contacts with Z-quantized distances
            for i in range(self.n):
                for j in range(i + 4, self.n):
                    d = dist[i, j]
                    p = self.contacts[i, j]

                    if p > 0.5:
                        E += 10 * p * (d - Z)**2  # Contact at Z distance
                    elif p > 0.3:
                        E += 5 * p * (d - Z * np.sqrt(2))**2

            # Steric clashes
            for i in range(self.n):
                for j in range(i + 2, self.n):
                    if dist[i, j] < 3.2:
                        E += 200 * (3.2 - dist[i, j])**2

            # Compactness
            com = coords.mean(axis=0)
            rg = np.sqrt(np.mean(np.sum((coords - com)**2, axis=1)))
            rg_target = 2.2 * (self.n ** 0.38)
            E += 20 * (rg - rg_target)**2

            # Helix geometry
            for i in range(self.n - 4):
                if self.ss[i] == 'H' and self.ss[i+4] == 'H':
                    E += 10 * (dist[i, i+4] - 5.4)**2

            return E

        result = minimize(energy, coords_init.flatten(), method='L-BFGS-B',
                         options={'maxiter': 3000})

        return {'coords': result.x.reshape(-1, 3), 'energy': result.fun}


# ==============================================================================
# MAIN FOLDER
# ==============================================================================

class Z2FolderV4:
    """Main folding class."""

    def __init__(self, sequence, name='protein'):
        self.seq = sequence
        self.name = name
        self.n = len(sequence)
        self.z2space = Z2CodonSpace()

    def fold(self, verbose=True):
        """Fold the protein."""
        start = time.time()

        if verbose:
            print(f"\nFolding {self.name} ({self.n} residues)...")

        # SS prediction
        ss_pred = Z2SSPredictor(self.seq, self.z2space)
        ss = ss_pred.predict()
        if verbose:
            print(f"  SS: {ss}")

        # Contact prediction
        contact_pred = Z2ContactPredictor(self.seq, self.z2space, ss)
        contacts = contact_pred.predict()

        # Structure building
        builder = Z2StructureBuilder(self.seq, ss, contacts)
        coords, energy = builder.build(n_models=25)

        elapsed = time.time() - start

        com = coords.mean(axis=0)
        rg = np.sqrt(np.mean(np.sum((coords - com)**2, axis=1)))

        return {
            'name': self.name,
            'sequence': self.seq,
            'length': self.n,
            'ss': ss,
            'coords': coords,
            'energy': energy,
            'rg': rg,
            'time': elapsed
        }


# ==============================================================================
# EVALUATION
# ==============================================================================

def q3_accuracy(pred, known):
    """Compute Q3."""
    if len(pred) != len(known):
        return 0.0

    def norm(s):
        return ''.join('H' if c in 'HG' else 'E' if c in 'EB' else 'C' for c in s.upper())

    p, k = norm(pred), norm(known)
    return 100 * sum(a == b for a, b in zip(p, k)) / len(k)


# ==============================================================================
# TEST
# ==============================================================================

PROTEINS = {
    'villin_hp35': {
        'seq': 'LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF',
        'ss': 'CHHHHHHHHHHCCHHHHHHHHHHHHHHHHHHHHHC'
    },
    'gb1': {
        'seq': 'MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE',
        'ss': 'CEEEEEECCCCCCEEEEEECCCCHHHHHHHHHCCCCCEEEEEECCCCCEEEEEEEC'
    },
    'insulin_b': {
        'seq': 'FVNQHLCGSHLVEALYLVCGERGFFYTPKT',
        'ss': 'CCCCHHHHHHHHHHHHHHHHHCCEEEEECC'
    },
    'ubiquitin': {
        'seq': 'MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG',
        'ss': 'CEEEEEECCCCCEEEEECCCCCEEEEEECCCCCCEEEECCCCCCCCCCCCCEEEEEEECCCCCCCCEEEEEEEECC'
    },
    'trp_cage': {
        'seq': 'NLYIQWLKDGGPSSGRPPPS',
        'ss': 'CCHHHHHHHHCCCCCCHHHC'
    },
    'ww_domain': {
        'seq': 'KLPPGWEKRMSRSSGRVYYFNHITNASQWERPS',
        'ss': 'CCCCCEEEECCCCEEEECCCCCCEEEECCCCCC'
    }
}


def main():
    print("\n" + "="*80)
    print("Z² FOLDING v4 - CODON GEOMETRY FIRST")
    print("="*80)

    results = {}

    for name, data in PROTEINS.items():
        print(f"\n{'─'*60}")
        print(f"Protein: {name}")

        folder = Z2FolderV4(data['seq'], name)
        result = folder.fold(verbose=True)

        q3 = q3_accuracy(result['ss'], data['ss'])
        result['known_ss'] = data['ss']
        result['q3'] = q3

        print(f"  Known: {data['ss']}")
        print(f"  Q3:    {q3:.1f}%")
        print(f"  Rg:    {result['rg']:.1f} Å")
        print(f"  Time:  {result['time']:.1f}s")

        results[name] = {
            'pred_ss': result['ss'],
            'known_ss': data['ss'],
            'q3': q3,
            'rg': result['rg'],
            'energy': result['energy'],
            'time': result['time']
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
    with open('z2_folding_v4_results.json', 'w') as f:
        json.dump({
            'framework': 'Z² Folding v4',
            'timestamp': datetime.now().isoformat(),
            'Z2': Z2,
            'results': results
        }, f, indent=2)

    print("\nSaved to z2_folding_v4_results.json")
    return results


if __name__ == '__main__':
    main()
