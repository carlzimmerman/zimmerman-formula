#!/usr/bin/env python3
"""
Z² Protein Folding v2: Multi-Method Geometric Approach

SPDX-License-Identifier: AGPL-3.0-or-later

The first BruteFlow attempt achieved 48.6% Q3. We need better approaches.

KEY INSIGHT: Z² geometry appears in protein structure at multiple scales:

1. DISTANCE SCALE:
   Z ≈ 5.79 Å - remarkably close to:
   - Typical Cα contact distance (6-8 Å)
   - α-helix pitch (5.4 Å)
   - 1.5 × Cα-Cα bond length (3.8 × 1.5 = 5.7 Å)

2. ANGLE SCALE:
   θ_Z² = π/Z ≈ 31.09°
   - 2×θ_Z² ≈ 62° ~ |φ_helix| = 57°
   - 4×θ_Z² ≈ 124° ~ |φ_sheet| = 120°
   - The Ramachandran plot might be QUANTIZED in θ_Z² units!

3. PERIODICITY:
   α-helix: 3.6 residues/turn
   Z/θ_Z² in radians = Z/(π/Z) = Z²/π ≈ 10.67
   10.67/3 ≈ 3.56 ~ 3.6 residues/turn!

NEW APPROACHES:
==============
A) Z² Distance Geometry - Use Z as fundamental contact distance
B) Z² Ramachandran Quantization - Quantize backbone angles
C) Z² Hydrophobicity Waves - Model hydrophobic burial with Z² periodicity
D) Z² Fragment Assembly - Score fragments by Z² compatibility
E) Z² Energy Minimization - Add Z² terms to physics potential

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.spatial.distance import pdist, squareform
from multiprocessing import Pool, cpu_count
import json
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² FUNDAMENTAL CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2  # = 32π/3 ≈ 33.510321638291124
THETA_Z2 = np.pi / Z  # ≈ 0.5426 rad ≈ 31.09°
THETA_Z2_DEG = np.degrees(THETA_Z2)

# Protein structure constants
CA_CA_BOND = 3.8  # Å - Cα-Cα virtual bond length
CONTACT_THRESHOLD = 8.0  # Å - typical contact definition

# Ramachandran basins (degrees)
HELIX_PHI, HELIX_PSI = -57.0, -47.0
SHEET_PHI, SHEET_PSI = -120.0, 120.0
COIL_PHI, COIL_PSI = -60.0, 140.0  # PPII-like

print("="*80)
print("Z² PROTEIN FOLDING v2: Multi-Method Geometric Approach")
print("="*80)
print(f"Z = {Z:.6f} Å (fundamental distance)")
print(f"θ_Z² = {THETA_Z2_DEG:.2f}° (fundamental angle)")
print(f"Z²/π = {Z2/np.pi:.4f} (angle periodicity)")
print(f"CPUs: {cpu_count()}")
print("="*80)

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Kyte-Doolittle hydrophobicity scale
HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# Secondary structure propensities (Chou-Fasman)
HELIX_PROPENSITY = {
    'A': 1.42, 'R': 0.98, 'N': 0.67, 'D': 1.01, 'C': 0.70,
    'Q': 1.11, 'E': 1.51, 'G': 0.57, 'H': 1.00, 'I': 1.08,
    'L': 1.21, 'K': 1.16, 'M': 1.45, 'F': 1.13, 'P': 0.57,
    'S': 0.77, 'T': 0.83, 'W': 1.08, 'Y': 0.69, 'V': 1.06
}

SHEET_PROPENSITY = {
    'A': 0.83, 'R': 0.93, 'N': 0.89, 'D': 0.54, 'C': 1.19,
    'Q': 1.10, 'E': 0.37, 'G': 0.75, 'H': 0.87, 'I': 1.60,
    'L': 1.30, 'K': 0.74, 'M': 1.05, 'F': 1.38, 'P': 0.55,
    'S': 0.75, 'T': 1.19, 'W': 1.37, 'Y': 1.47, 'V': 1.70
}

# ==============================================================================
# METHOD A: Z² DISTANCE GEOMETRY
# ==============================================================================

class Z2DistanceGeometry:
    """
    Hypothesis: Contact distances are quantized in units of Z.

    Contact distance = n × Z where n ∈ {1, √2, √3, 2, ...}

    This mirrors crystallographic packing where distances are
    quantized by the unit cell.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

        # Z-quantized distance levels
        self.Z_LEVELS = [
            Z,                    # 5.79 Å - closest contact
            Z * np.sqrt(2),       # 8.19 Å - diagonal
            Z * np.sqrt(3),       # 10.03 Å - body diagonal
            Z * 2,                # 11.58 Å - double
        ]

    def predict_contacts(self, min_seq_sep=4):
        """Predict contacts using Z²-quantized distances."""
        contacts = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(i + min_seq_sep, self.n):
                # Contact probability based on sequence features
                h_i = HYDROPHOBICITY.get(self.sequence[i], 0)
                h_j = HYDROPHOBICITY.get(self.sequence[j], 0)

                # Hydrophobic residues contact each other
                hydrophobic_score = (h_i + h_j) / 9.0  # normalize to ~1

                # Sequence separation penalty (longer range = less likely)
                sep = j - i
                sep_factor = np.exp(-sep / (2 * Z))  # Z as characteristic length

                # Periodicity: contacts every Z residues more likely
                period_factor = 1.0 + 0.5 * np.cos(2 * np.pi * sep / Z)

                prob = (0.3 + 0.7 * max(0, hydrophobic_score)) * sep_factor * period_factor
                contacts[i, j] = contacts[j, i] = prob

        return contacts

    def build_structure(self, contacts, n_attempts=100):
        """Build 3D structure satisfying contact constraints."""
        best_coords = None
        best_score = float('inf')

        for attempt in range(n_attempts):
            # Initialize with helix-like structure
            coords = np.zeros((self.n, 3))
            for i in range(self.n):
                t = i * 2 * np.pi / 3.6  # helix parameter
                coords[i] = [
                    2.3 * np.cos(t),  # radius
                    2.3 * np.sin(t),
                    i * 1.5  # rise per residue
                ]

            # Add random perturbation
            coords += np.random.randn(self.n, 3) * (attempt / n_attempts) * 5

            # Optimize to match contacts
            def objective(flat_coords):
                c = flat_coords.reshape(-1, 3)
                dist_matrix = squareform(pdist(c))

                # Bond length constraint
                bond_penalty = 0
                for i in range(self.n - 1):
                    bond_penalty += (dist_matrix[i, i+1] - CA_CA_BOND)**2

                # Contact satisfaction
                contact_penalty = 0
                for i in range(self.n):
                    for j in range(i + 4, self.n):
                        d = dist_matrix[i, j]
                        p = contacts[i, j]

                        if p > 0.5:  # predicted contact
                            # Should be at Z distance
                            contact_penalty += p * min((d - Z)**2, (d - Z*np.sqrt(2))**2)
                        else:  # not contact
                            # Should be far
                            if d < Z * 1.5:
                                contact_penalty += (1 - p) * (Z * 1.5 - d)**2

                return bond_penalty * 10 + contact_penalty

            result = minimize(objective, coords.flatten(), method='L-BFGS-B',
                            options={'maxiter': 500})

            if result.fun < best_score:
                best_score = result.fun
                best_coords = result.x.reshape(-1, 3)

        return best_coords


# ==============================================================================
# METHOD B: Z² RAMACHANDRAN QUANTIZATION
# ==============================================================================

class Z2RamachandranQuantization:
    """
    Hypothesis: Backbone dihedral angles are quantized in θ_Z² units.

    α-helix: φ ≈ -2θ_Z² = -62°, ψ ≈ -1.5θ_Z² = -47°
    β-sheet: φ ≈ -4θ_Z² = -124°, ψ ≈ +4θ_Z² = +124°

    The Ramachandran plot has discrete Z²-allowed basins!
    """

    # Z²-quantized angle basins
    BASINS = {
        'H': (-2 * THETA_Z2_DEG, -1.5 * THETA_Z2_DEG),  # helix
        'E': (-4 * THETA_Z2_DEG, +4 * THETA_Z2_DEG),     # sheet
        'C': (-2 * THETA_Z2_DEG, +4.5 * THETA_Z2_DEG),   # coil/PPII
    }

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def predict_ss(self):
        """Predict secondary structure using propensities."""
        ss = []
        window = 5

        for i in range(self.n):
            # Get window
            start = max(0, i - window//2)
            end = min(self.n, i + window//2 + 1)
            window_seq = self.sequence[start:end]

            # Average propensities
            h_score = np.mean([HELIX_PROPENSITY.get(aa, 1.0) for aa in window_seq])
            e_score = np.mean([SHEET_PROPENSITY.get(aa, 1.0) for aa in window_seq])

            # Z² periodicity boost for helices (i, i+3, i+4 pattern)
            if i >= 3:
                same_hydrophobic = (
                    HYDROPHOBICITY.get(self.sequence[i], 0) > 0 and
                    HYDROPHOBICITY.get(self.sequence[i-3], 0) > 0
                )
                if same_hydrophobic:
                    h_score *= 1.2

            if h_score > e_score and h_score > 1.0:
                ss.append('H')
            elif e_score > h_score and e_score > 1.1:
                ss.append('E')
            else:
                ss.append('C')

        # Smooth: require 3+ consecutive for helix/sheet
        ss = list(ss)
        for i in range(1, self.n - 1):
            if ss[i] != ss[i-1] and ss[i] != ss[i+1]:
                ss[i] = 'C'

        return ''.join(ss)

    def get_angles(self, ss_string):
        """Convert SS string to Z²-quantized phi/psi angles."""
        phi = np.zeros(self.n)
        psi = np.zeros(self.n)

        for i, ss in enumerate(ss_string):
            basin = self.BASINS.get(ss, self.BASINS['C'])
            phi[i] = np.radians(basin[0])
            psi[i] = np.radians(basin[1])

        return phi, psi

    def build_backbone(self, phi, psi):
        """Build backbone coordinates from phi/psi angles."""
        # Use idealized bond geometry
        N_CA = 1.46  # N-Cα bond
        CA_C = 1.52  # Cα-C bond
        C_N = 1.33   # C-N bond (peptide)

        coords = []
        pos = np.array([0.0, 0.0, 0.0])
        direction = np.array([1.0, 0.0, 0.0])

        for i in range(self.n):
            # Simplified: just place Cα atoms
            coords.append(pos.copy())

            # Move to next residue using phi/psi
            # This is simplified - real geometry is more complex
            rotation_angle = phi[i] + psi[i]
            c, s = np.cos(rotation_angle), np.sin(rotation_angle)

            # Rotate direction
            new_dir = np.array([
                c * direction[0] - s * direction[1],
                s * direction[0] + c * direction[1],
                direction[2] + 0.3 * np.sin(i * THETA_Z2)  # Z² rise
            ])
            direction = new_dir / np.linalg.norm(new_dir)

            # Step forward
            pos = pos + CA_CA_BOND * direction

        return np.array(coords)


# ==============================================================================
# METHOD C: Z² HYDROPHOBIC WAVES
# ==============================================================================

class Z2HydrophobicWaves:
    """
    Hypothesis: Hydrophobic burial follows Z² periodicity.

    In helices: hydrophobic face every 3.6 residues ≈ Z²/π × (π/3)
    In sheets: alternating pattern with Z-dependent spacing

    The protein folds to bury hydrophobic residues at Z²-periodic intervals.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)
        self.hydrophobicity = np.array([
            HYDROPHOBICITY.get(aa, 0) for aa in sequence
        ])

    def analyze_periodicity(self):
        """Find dominant periodicities in hydrophobicity."""
        # FFT of hydrophobicity
        fft = np.fft.fft(self.hydrophobicity)
        freqs = np.fft.fftfreq(self.n)

        # Power spectrum
        power = np.abs(fft)**2

        # Find peaks
        peaks = []
        for i in range(1, self.n//2):
            if power[i] > power[i-1] and power[i] > power[i+1]:
                period = 1.0 / freqs[i] if freqs[i] != 0 else np.inf
                if 2 < period < 10:  # relevant range
                    peaks.append((period, power[i]))

        return sorted(peaks, key=lambda x: -x[1])

    def compute_burial_potential(self):
        """Compute burial potential using Z² periodicity."""
        burial = np.zeros(self.n)

        # Helix periodicity (3.6 residues)
        helix_period = Z2 / np.pi / 3  # ≈ 3.56

        # Sheet periodicity (2 residues)
        sheet_period = 2.0

        for i in range(self.n):
            # Helix-like burial (amphipathic)
            helix_contrib = 0
            for j in range(max(0, i-7), min(self.n, i+8)):
                if j != i:
                    phase = 2 * np.pi * (j - i) / helix_period
                    helix_contrib += self.hydrophobicity[j] * np.cos(phase)

            # Sheet-like burial (alternating)
            sheet_contrib = 0
            for j in range(max(0, i-5), min(self.n, i+6)):
                if j != i:
                    phase = np.pi * (j - i)  # alternating
                    sheet_contrib += self.hydrophobicity[j] * np.cos(phase)

            burial[i] = self.hydrophobicity[i] * (helix_contrib + 0.5 * sheet_contrib)

        return burial

    def predict_core_residues(self):
        """Predict which residues form the hydrophobic core."""
        burial = self.compute_burial_potential()
        threshold = np.percentile(burial, 70)
        return burial > threshold


# ==============================================================================
# METHOD D: COMBINED Z² FOLDER
# ==============================================================================

class Z2FolderV2:
    """Combined approach using all Z² methods."""

    def __init__(self, sequence, name="protein"):
        self.sequence = sequence
        self.name = name
        self.n = len(sequence)

        # Initialize all methods
        self.dist_geom = Z2DistanceGeometry(sequence)
        self.rama_quant = Z2RamachandranQuantization(sequence)
        self.hydro_waves = Z2HydrophobicWaves(sequence)

    def predict(self, n_models=10, verbose=True):
        """Generate structure prediction."""
        start = time.time()

        if verbose:
            print(f"\nPredicting structure for {self.name} ({self.n} residues)")

        # Step 1: Secondary structure
        ss = self.rama_quant.predict_ss()
        if verbose:
            print(f"  SS prediction: {ss}")

        # Step 2: Get backbone angles
        phi, psi = self.rama_quant.get_angles(ss)

        # Step 3: Predict contacts
        contacts = self.dist_geom.predict_contacts()

        # Step 4: Identify core residues
        core = self.hydro_waves.predict_core_residues()

        # Step 5: Build and refine structure
        best_coords = None
        best_energy = float('inf')

        for model in range(n_models):
            # Build initial backbone
            coords = self.rama_quant.build_backbone(phi, psi)

            # Refine with contact constraints
            def energy(flat_coords):
                c = flat_coords.reshape(-1, 3)
                dist_matrix = squareform(pdist(c))

                E = 0.0

                # Bond lengths
                for i in range(self.n - 1):
                    E += 100 * (dist_matrix[i, i+1] - CA_CA_BOND)**2

                # Contact satisfaction
                for i in range(self.n):
                    for j in range(i + 4, self.n):
                        d = dist_matrix[i, j]
                        p = contacts[i, j]

                        # Z-quantized contacts
                        if p > 0.3:
                            d_target = Z if p > 0.6 else Z * np.sqrt(2)
                            E += p * (d - d_target)**2

                # Core burial (hydrophobic residues should be close)
                for i in range(self.n):
                    if core[i]:
                        for j in range(i + 1, self.n):
                            if core[j]:
                                E -= 0.5 / (1 + dist_matrix[i, j] / Z)

                # Compactness
                rg = np.sqrt(np.mean(np.sum((c - c.mean(axis=0))**2, axis=1)))
                rg_ideal = 2.5 * (self.n ** 0.4)  # empirical scaling
                E += 10 * (rg - rg_ideal)**2

                return E

            # Add noise for diversity
            coords_init = coords + np.random.randn(self.n, 3) * (model * 0.5)

            result = minimize(energy, coords_init.flatten(), method='L-BFGS-B',
                            options={'maxiter': 1000})

            if result.fun < best_energy:
                best_energy = result.fun
                best_coords = result.x.reshape(-1, 3)

        elapsed = time.time() - start

        return {
            'name': self.name,
            'sequence': self.sequence,
            'length': self.n,
            'secondary_structure': ss,
            'coordinates': best_coords,
            'energy': best_energy,
            'elapsed_seconds': elapsed
        }


# ==============================================================================
# METHOD E: Z² TORSION ANGLE NEURAL POTENTIAL
# ==============================================================================

class Z2TorsionPotential:
    """
    Physics-based potential with Z² geometric terms.

    E_total = E_bond + E_angle + E_torsion + E_vdw + E_Z2

    where E_Z2 encodes Z²-specific geometric preferences.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def compute_Z2_potential(self, coords):
        """Compute Z²-specific energy terms."""
        E_Z2 = 0.0

        dist_matrix = squareform(pdist(coords))

        # Term 1: Distance quantization
        # Contacts should be at Z, √2·Z, √3·Z, or 2Z
        for i in range(self.n):
            for j in range(i + 4, self.n):
                d = dist_matrix[i, j]
                if d < 2 * Z:  # within interaction range
                    # Distance to nearest Z-level
                    levels = [Z, Z*np.sqrt(2), Z*np.sqrt(3), 2*Z]
                    min_dev = min(abs(d - l) for l in levels)
                    E_Z2 += 0.5 * min_dev**2

        # Term 2: Angle relationships
        # Consecutive Cα triplets should have angles related to θ_Z²
        for i in range(self.n - 2):
            v1 = coords[i+1] - coords[i]
            v2 = coords[i+2] - coords[i+1]
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
            angle = np.arccos(np.clip(cos_angle, -1, 1))

            # Should be multiple of θ_Z²
            n_theta = angle / THETA_Z2
            nearest_int = round(n_theta)
            E_Z2 += 0.1 * (n_theta - nearest_int)**2

        # Term 3: Helix periodicity
        # Every 3.6 residues should be on same face
        helix_period = Z2 / np.pi / 3  # ≈ 3.56
        for i in range(self.n - 4):
            d_i_i4 = dist_matrix[i, i+4]
            # In helix, i and i+4 are close (≈5.4 Å)
            if d_i_i4 < Z:  # helix-like
                # Check Z² periodicity
                expected_d = 5.4  # helix contact
                E_Z2 += 0.2 * (d_i_i4 - expected_d)**2

        return E_Z2


# ==============================================================================
# EVALUATION
# ==============================================================================

def compute_q3_accuracy(predicted_ss, known_ss):
    """Compute Q3 accuracy."""
    if len(predicted_ss) != len(known_ss):
        return 0.0

    # Normalize: H=helix, E=sheet, C=coil
    def normalize(ss):
        result = []
        for c in ss.upper():
            if c in 'HG':  # 3-10 helix counts as helix
                result.append('H')
            elif c in 'EB':  # bridge counts as sheet
                result.append('E')
            else:
                result.append('C')
        return ''.join(result)

    pred = normalize(predicted_ss)
    known = normalize(known_ss)

    correct = sum(p == k for p, k in zip(pred, known))
    return 100.0 * correct / len(known)


def compute_tm_score_approx(coords1, coords2):
    """Approximate TM-score (simplified)."""
    n = len(coords1)
    if n != len(coords2):
        return 0.0

    d0 = 1.24 * (n - 15)**(1/3) - 1.8
    d0 = max(d0, 0.5)

    # Simple RMSD-based approximation
    diff = coords1 - coords2
    rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))

    # TM-score approximation
    tm = np.mean(1.0 / (1.0 + (rmsd / d0)**2))
    return tm


# ==============================================================================
# TEST PROTEINS
# ==============================================================================

TEST_PROTEINS = {
    'villin_hp35': {
        'sequence': 'LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF',
        'known_ss': 'CHHHHHHHHHHCCHHHHHHHHHHHHHHHHHHHHHC',
        'description': '35-residue all-helix protein'
    },
    'gb1': {
        'sequence': 'MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE',
        'known_ss': 'CEEEEEECCCCCCCEEEEEECCCCHHHHHHHHHCCCCCEEEEEECCCCCEEEEEEEC',
        'description': '56-residue alpha/beta protein'
    },
    'insulin_b': {
        'sequence': 'FVNQHLCGSHLVEALYLVCGERGFFYTPKT',
        'known_ss': 'CCCCHHHHHHHHHHHHHHHHHCCEEEEECC',
        'description': '30-residue mixed protein'
    },
    'ubiquitin': {
        'sequence': 'MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG',
        'known_ss': 'CEEEEEECCCCCEEEEECCCCCEEEEEECCCCCCEEEECCCCCCCCCCCCCEEEEEECCCCCCCCEEEEEEEECC',
        'description': '76-residue alpha/beta protein'
    },
    'trp_cage': {
        'sequence': 'NLYIQWLKDGGPSSGRPPPS',
        'known_ss': 'CCHHHHHHHHCCCCCCHHHC',
        'description': '20-residue mini-protein'
    },
    'ww_domain': {
        'sequence': 'KLPPGWEKRMSRSSGRVYYFNHITNASQWERPS',
        'known_ss': 'CCCCCEEEECCCCEEEECCCCCCEEEECCCCCC',
        'description': '33-residue all-beta protein'
    }
}


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("\n" + "="*80)
    print("RUNNING Z² FOLDING v2 ON TEST PROTEINS")
    print("="*80)

    results = {}

    for name, data in TEST_PROTEINS.items():
        print(f"\n{'='*60}")
        print(f"Protein: {name}")
        print(f"Description: {data['description']}")
        print(f"Sequence: {data['sequence']}")
        print(f"Known SS: {data['known_ss']}")
        print('='*60)

        folder = Z2FolderV2(data['sequence'], name)
        result = folder.predict(n_models=5, verbose=True)

        # Evaluate SS
        q3 = compute_q3_accuracy(result['secondary_structure'], data['known_ss'])
        result['known_ss'] = data['known_ss']
        result['q3_accuracy'] = q3

        print(f"\n  Predicted SS: {result['secondary_structure']}")
        print(f"  Known SS:     {data['known_ss']}")
        print(f"  Q3 Accuracy:  {q3:.1f}%")
        print(f"  Energy:       {result['energy']:.2f}")
        print(f"  Time:         {result['elapsed_seconds']:.2f}s")

        # Store (excluding numpy arrays for JSON)
        results[name] = {
            'name': name,
            'length': result['length'],
            'predicted_ss': result['secondary_structure'],
            'known_ss': data['known_ss'],
            'q3_accuracy': q3,
            'energy': result['energy'],
            'elapsed_seconds': result['elapsed_seconds']
        }

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    q3_scores = [r['q3_accuracy'] for r in results.values()]
    print(f"\nQ3 Accuracy by protein:")
    for name, r in results.items():
        print(f"  {name:15s}: {r['q3_accuracy']:5.1f}%")

    print(f"\nAverage Q3: {np.mean(q3_scores):.1f}%")
    print(f"Best Q3:    {max(q3_scores):.1f}%")
    print(f"Worst Q3:   {min(q3_scores):.1f}%")

    # Save results
    output = {
        'framework': 'Z² Folding v2',
        'timestamp': datetime.now().isoformat(),
        'Z2': Z2,
        'theta_Z2_deg': THETA_Z2_DEG,
        'methods': ['distance_geometry', 'ramachandran_quantization', 'hydrophobic_waves'],
        'predictions': results
    }

    with open('z2_folding_v2_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to z2_folding_v2_results.json")

    return results


if __name__ == '__main__':
    main()
