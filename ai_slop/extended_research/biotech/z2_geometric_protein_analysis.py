#!/usr/bin/env python3
"""
Z² Geometric Protein Analysis Framework

SPDX-License-Identifier: AGPL-3.0-or-later

THE KEY INSIGHT: Before folding, we must UNDERSTAND the protein geometrically.

This framework analyzes a protein sequence through multiple Z² geometric lenses:
1. CODON GEOMETRY - Where does each residue sit in Z² space?
2. LOCAL GEOMETRY - What are the preferred backbone angles?
3. CONTACT GEOMETRY - What patterns emerge from residue relationships?
4. TOPOLOGICAL GEOMETRY - What constraints does the chain impose?
5. THERMODYNAMIC GEOMETRY - What is the folding funnel shape?

After analysis, we can fold using the Z² constraints we've discovered.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from collections import defaultdict
import json
from datetime import datetime

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.79
Z2 = Z**2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 31.09° ≈ 0.543 rad
CA_CA = 3.8  # Cα-Cα distance in Å

print("="*80)
print("Z² GEOMETRIC PROTEIN ANALYSIS FRAMEWORK")
print("="*80)
print(f"Z = {Z:.6f} Å")
print(f"Z² = {Z2:.6f}")
print(f"θ_Z² = {np.degrees(THETA_Z2):.2f}°")
print("="*80)

# ==============================================================================
# AMINO ACID DATA
# ==============================================================================

# Genetic code
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

# Physical properties
HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

VOLUME = {  # Å³
    'A': 88.6, 'R': 173.4, 'N': 114.1, 'D': 111.1, 'C': 108.5,
    'Q': 143.8, 'E': 138.4, 'G': 60.1, 'H': 153.2, 'I': 166.7,
    'L': 166.7, 'K': 168.6, 'M': 162.9, 'F': 189.9, 'P': 112.7,
    'S': 89.0, 'T': 116.1, 'W': 227.8, 'Y': 193.6, 'V': 140.0
}

CHARGE = {
    'A': 0, 'R': 1, 'N': 0, 'D': -1, 'C': 0,
    'Q': 0, 'E': -1, 'G': 0, 'H': 0.5, 'I': 0,
    'L': 0, 'K': 1, 'M': 0, 'F': 0, 'P': 0,
    'S': 0, 'T': 0, 'W': 0, 'Y': 0, 'V': 0
}


# ==============================================================================
# 1. CODON GEOMETRY ANALYSIS
# ==============================================================================

class CodonGeometryAnalysis:
    """
    Analyze protein sequence through the lens of codon geometry in Z² space.

    Key questions:
    - Where does each amino acid sit in the Z² codon manifold?
    - Do neighboring residues cluster in Z² space?
    - Can we identify Z² patterns that predict structure?
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)
        self._build_codon_space()

    def _build_codon_space(self):
        """Build Z² codon space embedding."""
        base_map = {'T': 0, 'C': 1, 'A': 2, 'G': 3}

        self.codon_vec = {}
        self.aa_vecs = defaultdict(list)

        for codon, aa in GENETIC_CODE.items():
            if aa == '*':
                continue

            b1, b2, b3 = [base_map[b] for b in codon]

            # Z² angular embedding
            theta1 = b1 * THETA_Z2
            theta2 = b2 * THETA_Z2
            theta3 = b3 * THETA_Z2 / 2  # Wobble

            # 3D unit sphere embedding scaled by Z
            x = np.cos(theta1) * np.sin(theta2 + theta3)
            y = np.sin(theta1) * np.sin(theta2 + theta3)
            z = np.cos(theta2 + theta3)

            vec = np.array([x, y, z]) * Z
            self.codon_vec[codon] = vec
            self.aa_vecs[aa].append(vec)

        # Mean position for each AA
        self.aa_mean = {aa: np.mean(vecs, axis=0) for aa, vecs in self.aa_vecs.items()}

    def get_z2_trajectory(self):
        """Get the Z² space trajectory of the protein."""
        trajectory = np.zeros((self.n, 3))
        for i, aa in enumerate(self.sequence):
            trajectory[i] = self.aa_mean.get(aa, np.zeros(3))
        return trajectory

    def compute_z2_distances(self):
        """Compute pairwise Z² distances between residues."""
        traj = self.get_z2_trajectory()
        return squareform(pdist(traj))

    def find_z2_clusters(self, threshold=Z/2):
        """Find clusters of residues that are close in Z² space."""
        dist = self.compute_z2_distances()
        clusters = []

        visited = set()
        for i in range(self.n):
            if i in visited:
                continue
            cluster = [i]
            visited.add(i)
            for j in range(i+1, self.n):
                if j not in visited and dist[i, j] < threshold:
                    cluster.append(j)
                    visited.add(j)
            if len(cluster) > 1:
                clusters.append(cluster)

        return clusters

    def analyze_z2_periodicity(self):
        """Analyze periodic patterns in Z² trajectory."""
        traj = self.get_z2_trajectory()

        # Compute autocorrelation for each dimension
        periods = {}
        for dim, name in enumerate(['x', 'y', 'z']):
            signal = traj[:, dim]

            # FFT
            spectrum = np.abs(fft(signal))
            freqs = fftfreq(self.n)

            # Find peaks
            peaks, _ = find_peaks(spectrum[:self.n//2])
            if len(peaks) > 0:
                dominant_peak = peaks[np.argmax(spectrum[peaks])]
                if freqs[dominant_peak] > 0:
                    periods[name] = 1 / freqs[dominant_peak]

        return periods

    def compute_z2_contact_potential(self):
        """
        Compute contact potential from Z² geometry.

        Residues close in Z² space may prefer to contact.
        """
        dist = self.compute_z2_distances()
        potential = np.exp(-dist / Z)

        # Apply sequence separation filter
        for i in range(self.n):
            for j in range(self.n):
                if abs(i - j) < 4:
                    potential[i, j] = 0

        return potential


# ==============================================================================
# 2. LOCAL BACKBONE GEOMETRY ANALYSIS
# ==============================================================================

class LocalGeometryAnalysis:
    """
    Analyze local backbone geometry preferences using Z² angles.

    Key hypothesis: Backbone angles are quantized in units of θ_Z².
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def predict_phi_psi(self):
        """
        Predict φ/ψ angles using Z² quantization.

        α-helix: φ ≈ -57° ≈ -1.83 × θ_Z²
        β-sheet: φ ≈ -120° ≈ -3.86 × θ_Z²

        We use Z²-derived propensities to predict which angles.
        """
        # Get SS propensities
        h_prop = np.zeros(self.n)
        e_prop = np.zeros(self.n)

        for i, aa in enumerate(self.sequence):
            # Z²-derived propensity (simplified)
            h = HYDROPHOBICITY.get(aa, 0)
            v = VOLUME.get(aa, 100)

            # Helix formers: intermediate hydrophobicity, smaller
            h_prop[i] = 1.0 if -1 < h < 3 and v < 150 else 0.5

            # Sheet formers: hydrophobic, larger
            e_prop[i] = 1.0 if h > 0 and v > 130 else 0.5

        # Window smoothing
        window = 5
        h_smooth = np.convolve(h_prop, np.ones(window)/window, mode='same')
        e_smooth = np.convolve(e_prop, np.ones(window)/window, mode='same')

        # Assign angles
        phi = np.zeros(self.n)
        psi = np.zeros(self.n)

        for i in range(self.n):
            if self.sequence[i] == 'P':
                # Proline: restricted
                phi[i] = -75
                psi[i] = 150
            elif self.sequence[i] == 'G':
                # Glycine: flexible
                phi[i] = -60
                psi[i] = -30
            elif h_smooth[i] > e_smooth[i]:
                # Helix-like: quantize to nearest θ_Z² multiple
                phi[i] = -2 * np.degrees(THETA_Z2)  # ≈ -62°
                psi[i] = -1.5 * np.degrees(THETA_Z2)  # ≈ -47°
            elif e_smooth[i] > h_smooth[i]:
                # Sheet-like
                phi[i] = -4 * np.degrees(THETA_Z2)  # ≈ -124°
                psi[i] = 4 * np.degrees(THETA_Z2)   # ≈ +124°
            else:
                # Coil
                phi[i] = -2 * np.degrees(THETA_Z2)
                psi[i] = 4.5 * np.degrees(THETA_Z2)

        return phi, psi

    def check_angle_quantization(self, phi, psi):
        """
        Check how well angles quantize to θ_Z² multiples.
        """
        deviations = []

        for i in range(self.n):
            # Phi quantization
            n_phi = phi[i] / np.degrees(THETA_Z2)
            dev_phi = abs(n_phi - round(n_phi))

            # Psi quantization
            n_psi = psi[i] / np.degrees(THETA_Z2)
            dev_psi = abs(n_psi - round(n_psi))

            deviations.append((dev_phi + dev_psi) / 2)

        return np.array(deviations)


# ==============================================================================
# 3. CONTACT GEOMETRY ANALYSIS
# ==============================================================================

class ContactGeometryAnalysis:
    """
    Analyze contact patterns using Z² geometric principles.

    Key insight: Contact distances should be quantized in units of Z.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def predict_contact_distances(self):
        """
        Predict preferred contact distances using Z quantization.

        Level 0: Z ≈ 5.79 Å (closest contact)
        Level 1: √2 × Z ≈ 8.2 Å (diagonal)
        Level 2: √3 × Z ≈ 10.0 Å (body diagonal)
        Level 3: 2 × Z ≈ 11.6 Å (double)
        """
        # Distance levels
        levels = [Z, Z * np.sqrt(2), Z * np.sqrt(3), 2 * Z]

        # For each residue pair, assign preferred distance
        preferred = {}

        for i in range(self.n):
            for j in range(i + 4, self.n):
                # Determine level based on properties
                h_i = HYDROPHOBICITY.get(self.sequence[i], 0)
                h_j = HYDROPHOBICITY.get(self.sequence[j], 0)

                if h_i > 0 and h_j > 0:
                    # Both hydrophobic: close contact
                    preferred[(i, j)] = levels[0]
                elif CHARGE.get(self.sequence[i], 0) * CHARGE.get(self.sequence[j], 0) < 0:
                    # Opposite charges: salt bridge
                    preferred[(i, j)] = levels[0]
                elif h_i > 0 or h_j > 0:
                    # One hydrophobic: intermediate
                    preferred[(i, j)] = levels[1]
                else:
                    # Both polar: farther
                    preferred[(i, j)] = levels[2]

        return preferred

    def compute_contact_matrix(self):
        """
        Compute full contact probability matrix.
        """
        matrix = np.zeros((self.n, self.n))
        codon_analysis = CodonGeometryAnalysis(self.sequence)
        z2_potential = codon_analysis.compute_z2_contact_potential()

        for i in range(self.n):
            for j in range(i + 4, self.n):
                # Base: Z² potential
                p = z2_potential[i, j]

                # Modifiers
                h_i = HYDROPHOBICITY.get(self.sequence[i], 0)
                h_j = HYDROPHOBICITY.get(self.sequence[j], 0)

                # Hydrophobic interaction
                if h_i > 0 and h_j > 0:
                    p *= 1.5

                # Sequence separation
                sep = j - i
                p *= np.exp(-sep / Z2) + 0.3 * np.exp(-sep / 15)

                matrix[i, j] = matrix[j, i] = min(1.0, p)

        return matrix


# ==============================================================================
# 4. TOPOLOGICAL GEOMETRY ANALYSIS
# ==============================================================================

class TopologicalGeometryAnalysis:
    """
    Analyze topological constraints from the chain geometry.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def compute_contact_order(self, contacts):
        """
        Compute contact order (CO) - average sequence separation of contacts.

        Low CO → fast folding (local contacts)
        High CO → slow folding (long-range contacts)
        """
        if not contacts:
            return 0

        total_sep = sum(abs(j - i) for i, j, _ in contacts)
        return total_sep / (len(contacts) * self.n)

    def predict_folding_rate(self, contact_order):
        """
        Predict folding rate from contact order.

        ln(k_f) ∝ -CO × Z²

        The Z² factor comes from the extra-dimensional folding funnel.
        """
        ln_k = -15 * contact_order * np.sqrt(Z2 / self.n)
        return np.exp(ln_k)

    def identify_nucleation_sites(self, contacts):
        """
        Identify potential folding nucleation sites.

        These are residues with many local contacts that can
        form early in folding.
        """
        local_density = np.zeros(self.n)

        for i, j, p in contacts:
            if abs(j - i) < 10:  # Local contact
                local_density[i] += p
                local_density[j] += p

        # Find peaks
        peaks, _ = find_peaks(local_density, height=np.mean(local_density))
        return peaks.tolist()


# ==============================================================================
# 5. THERMODYNAMIC GEOMETRY ANALYSIS
# ==============================================================================

class ThermodynamicGeometryAnalysis:
    """
    Analyze the thermodynamic folding funnel using Z² geometry.

    The folding funnel is the energy landscape of protein folding.
    Z² geometry suggests the funnel is a GEODESIC in the orbifold.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        self.n = len(sequence)

    def compute_energy_surface_curvature(self):
        """
        Estimate local curvature of the energy surface.

        Regions of high curvature are folding "decision points".
        """
        # Use hydrophobicity gradient as proxy for energy
        hydro = np.array([HYDROPHOBICITY.get(aa, 0) for aa in self.sequence])

        # Second derivative (curvature)
        curvature = np.zeros(self.n)
        for i in range(1, self.n - 1):
            curvature[i] = hydro[i-1] - 2*hydro[i] + hydro[i+1]

        return curvature

    def estimate_folding_funnel_depth(self):
        """
        Estimate the depth of the folding funnel.

        Deeper funnel → more stable fold
        """
        # Total hydrophobic burial potential
        hydro = np.array([HYDROPHOBICITY.get(aa, 0) for aa in self.sequence])

        # Funnel depth proportional to hydrophobic content
        buried_energy = np.sum(hydro[hydro > 0])

        # Z²-scaled depth
        depth = buried_energy / Z2

        return depth

    def compute_cooperativity(self):
        """
        Compute folding cooperativity.

        High cooperativity → two-state folder
        Low cooperativity → molten globule intermediate
        """
        # Cooperativity from volume heterogeneity
        volumes = np.array([VOLUME.get(aa, 100) for aa in self.sequence])

        # Coefficient of variation
        cv = np.std(volumes) / np.mean(volumes)

        # Lower CV → more cooperative
        cooperativity = np.exp(-cv * Z)

        return cooperativity


# ==============================================================================
# MASTER ANALYSIS CLASS
# ==============================================================================

class Z2ProteinGeometricAnalysis:
    """
    Complete geometric analysis of a protein using Z² framework.
    """

    def __init__(self, sequence, name="protein"):
        self.sequence = sequence
        self.name = name
        self.n = len(sequence)

        # Initialize all analysis modules
        self.codon = CodonGeometryAnalysis(sequence)
        self.local = LocalGeometryAnalysis(sequence)
        self.contact = ContactGeometryAnalysis(sequence)
        self.topology = TopologicalGeometryAnalysis(sequence)
        self.thermo = ThermodynamicGeometryAnalysis(sequence)

    def run_full_analysis(self):
        """Run complete geometric analysis."""
        print(f"\n{'='*60}")
        print(f"Z² GEOMETRIC ANALYSIS: {self.name}")
        print(f"Sequence ({self.n} residues): {self.sequence}")
        print(f"{'='*60}")

        results = {
            'name': self.name,
            'sequence': self.sequence,
            'length': self.n
        }

        # 1. Codon geometry
        print("\n[1] CODON GEOMETRY")
        z2_dist = self.codon.compute_z2_distances()
        z2_clusters = self.codon.find_z2_clusters()
        z2_periods = self.codon.analyze_z2_periodicity()

        print(f"    Mean Z² distance: {np.mean(z2_dist):.2f} Å")
        print(f"    Z² clusters found: {len(z2_clusters)}")
        print(f"    Z² periodicities: {z2_periods}")

        results['codon'] = {
            'mean_z2_distance': float(np.mean(z2_dist)),
            'n_clusters': len(z2_clusters),
            'periodicities': {k: float(v) for k, v in z2_periods.items()}
        }

        # 2. Local backbone geometry
        print("\n[2] LOCAL BACKBONE GEOMETRY")
        phi, psi = self.local.predict_phi_psi()
        quantization = self.local.check_angle_quantization(phi, psi)

        print(f"    Mean φ: {np.mean(phi):.1f}°")
        print(f"    Mean ψ: {np.mean(psi):.1f}°")
        print(f"    θ_Z² quantization error: {np.mean(quantization):.3f}")

        results['local'] = {
            'mean_phi': float(np.mean(phi)),
            'mean_psi': float(np.mean(psi)),
            'quantization_error': float(np.mean(quantization))
        }

        # 3. Contact geometry
        print("\n[3] CONTACT GEOMETRY")
        contact_matrix = self.contact.compute_contact_matrix()
        n_contacts = np.sum(contact_matrix > 0.3) // 2
        contact_list = [(i, j, contact_matrix[i,j])
                        for i in range(self.n)
                        for j in range(i+4, self.n)
                        if contact_matrix[i,j] > 0.3]

        print(f"    Predicted contacts (p>0.3): {n_contacts}")
        print(f"    Top contacts: {[(i,j,f'{p:.2f}') for i,j,p in sorted(contact_list, key=lambda x:-x[2])[:5]]}")

        results['contact'] = {
            'n_contacts': int(n_contacts),
            'top_contacts': [(int(i), int(j), float(p)) for i, j, p in sorted(contact_list, key=lambda x:-x[2])[:20]]
        }

        # 4. Topological geometry
        print("\n[4] TOPOLOGICAL GEOMETRY")
        contact_order = self.topology.compute_contact_order(contact_list)
        folding_rate = self.topology.predict_folding_rate(contact_order)
        nucleation = self.topology.identify_nucleation_sites(contact_list)

        print(f"    Contact order: {contact_order:.3f}")
        print(f"    Predicted folding rate: {folding_rate:.2e} s⁻¹")
        print(f"    Nucleation sites: {nucleation}")

        results['topology'] = {
            'contact_order': float(contact_order),
            'folding_rate': float(folding_rate),
            'nucleation_sites': nucleation
        }

        # 5. Thermodynamic geometry
        print("\n[5] THERMODYNAMIC GEOMETRY")
        funnel_depth = self.thermo.estimate_folding_funnel_depth()
        cooperativity = self.thermo.compute_cooperativity()
        curvature = self.thermo.compute_energy_surface_curvature()

        print(f"    Funnel depth: {funnel_depth:.2f} Z² units")
        print(f"    Cooperativity: {cooperativity:.3f}")
        print(f"    High curvature positions: {np.where(np.abs(curvature) > 1)[0].tolist()}")

        results['thermo'] = {
            'funnel_depth': float(funnel_depth),
            'cooperativity': float(cooperativity),
            'high_curvature_positions': np.where(np.abs(curvature) > 1)[0].tolist()
        }

        # Summary
        print(f"\n{'='*60}")
        print("GEOMETRIC SUMMARY")
        print(f"{'='*60}")
        print(f"  Z² clustering: {'Strong' if len(z2_clusters) > 3 else 'Weak'}")
        print(f"  Backbone geometry: {'Helical' if np.mean(phi) > -80 else 'Extended'}")
        print(f"  Folding: {'Fast (local)' if contact_order < 0.1 else 'Slow (non-local)'}")
        print(f"  Cooperativity: {'Two-state' if cooperativity > 0.5 else 'Multi-state'}")

        results['summary'] = {
            'z2_clustering': 'strong' if len(z2_clusters) > 3 else 'weak',
            'backbone_type': 'helical' if np.mean(phi) > -80 else 'extended',
            'folding_type': 'fast' if contact_order < 0.1 else 'slow',
            'cooperativity_type': 'two-state' if cooperativity > 0.5 else 'multi-state'
        }

        return results


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # Test proteins
    proteins = {
        'villin': ('LSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF', 'all-helix'),
        'gb1': ('MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE', 'alpha/beta'),
        'ww': ('KLPPGWEKRMSRSSGRVYYFNHITNASQWERPS', 'all-beta'),
        'trp_cage': ('NLYIQWLKDGGPSSGRPPPS', 'mini-protein')
    }

    all_results = {}

    for name, (seq, desc) in proteins.items():
        analysis = Z2ProteinGeometricAnalysis(seq, f"{name} ({desc})")
        results = analysis.run_full_analysis()
        all_results[name] = results

    # Save
    output = {
        'framework': 'Z² Geometric Protein Analysis',
        'timestamp': datetime.now().isoformat(),
        'Z2': Z2,
        'theta_Z2_deg': np.degrees(THETA_Z2),
        'proteins': all_results
    }

    with open('z2_geometric_analysis_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\n" + "="*60)
    print("Saved to z2_geometric_analysis_results.json")

    return all_results


if __name__ == '__main__':
    main()
