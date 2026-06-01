#!/usr/bin/env python3
"""
Z² Voronoi Rotamer Packing

SPDX-License-Identifier: AGPL-3.0-or-later

PATHWAY 3: Z²-QUANTIZED SIDE-CHAIN PACKING

Replace empirical rotamer libraries with Z² geometric constraints.
Side chains occupy Voronoi cells in chi-angle space, with cell boundaries
determined by the Z² metric tensor.

MATHEMATICAL FOUNDATION:
========================
The chi-angle space for each residue type is a torus T^n where n = 1-4
depending on the number of rotatable bonds. The Z² metric imposes:

    ds² = (1/Z²) Σᵢ dχᵢ²

This creates NATURAL QUANTIZATION where rotamers occupy Voronoi cells
centered on Z²-harmonic points.

PHYSICAL PRINCIPLE:
==================
Dunbrack rotamer libraries are EMERGENT, not fundamental.
The true rotamer positions arise from:
1. Steric exclusion (van der Waals)
2. Quantum zero-point motion in χ-space
3. Z² boundary conditions on the conformational torus

The Voronoi tessellation in Z²-scaled space gives the "correct"
rotamer library without training on PDB data.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial.distance import cdist
from itertools import product
import json
from datetime import datetime

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.79
Z2 = Z**2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 31.09° ≈ 0.543 rad

print("="*80)
print("Z² VORONOI ROTAMER PACKING")
print("="*80)
print(f"Z = {Z:.4f} | Z² = {Z2:.4f} | θ_Z² = {np.degrees(THETA_Z2):.2f}°")
print("="*80)

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Number of chi angles per residue
N_CHI = {
    'G': 0, 'A': 0,  # No rotatable bonds
    'S': 1, 'C': 1, 'V': 1, 'T': 1, 'P': 1,  # 1 chi angle
    'I': 2, 'L': 2, 'D': 2, 'N': 2, 'F': 2, 'Y': 2, 'H': 2, 'W': 2,  # 2 chi
    'M': 3, 'E': 3, 'Q': 3,  # 3 chi angles
    'K': 4, 'R': 4  # 4 chi angles
}

# Van der Waals radii for steric calculations
VDW_RADII = {
    'C': 1.70, 'N': 1.55, 'O': 1.52, 'S': 1.80, 'H': 1.20
}

# Side chain atom types (simplified)
SIDE_CHAIN_ATOMS = {
    'A': ['CB'],
    'V': ['CB', 'CG1', 'CG2'],
    'L': ['CB', 'CG', 'CD1', 'CD2'],
    'I': ['CB', 'CG1', 'CG2', 'CD1'],
    'M': ['CB', 'CG', 'SD', 'CE'],
    'F': ['CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'Y': ['CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'OH'],
    'W': ['CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'],
    'S': ['CB', 'OG'],
    'T': ['CB', 'OG1', 'CG2'],
    'C': ['CB', 'SG'],
    'N': ['CB', 'CG', 'OD1', 'ND2'],
    'Q': ['CB', 'CG', 'CD', 'OE1', 'NE2'],
    'D': ['CB', 'CG', 'OD1', 'OD2'],
    'E': ['CB', 'CG', 'CD', 'OE1', 'OE2'],
    'K': ['CB', 'CG', 'CD', 'CE', 'NZ'],
    'R': ['CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'],
    'H': ['CB', 'CG', 'ND1', 'CD2', 'CE1', 'NE2'],
    'P': ['CB', 'CG', 'CD'],
    'G': []
}

# ==============================================================================
# Z² ROTAMER SPACE
# ==============================================================================

class Z2RotamerSpace:
    """
    Model chi-angle space with Z² metric.

    The torus T^n of chi angles is equipped with metric
    ds² = (1/Z²) Σᵢ dχᵢ²

    This creates natural quantization at Z²-harmonic positions.
    """

    def __init__(self, n_chi):
        """
        Initialize rotamer space for residue with n_chi angles.

        Args:
            n_chi: Number of chi angles (1-4)
        """
        self.n_chi = n_chi
        if n_chi == 0:
            self.grid_points = None
            self.voronoi = None
            return

        # Generate Z²-harmonic grid points
        self.grid_points = self._generate_z2_grid()

        # Compute Voronoi tessellation
        if len(self.grid_points) > n_chi + 1:
            self.voronoi = self._compute_voronoi()
        else:
            self.voronoi = None

    def _generate_z2_grid(self):
        """
        Generate Z²-harmonic points in chi space.

        Points are placed at multiples of θ_Z² = π/Z
        """
        # Number of points per dimension
        n_per_dim = int(2 * np.pi / THETA_Z2) + 1  # ≈ 12 points

        # Generate 1D grid
        chi_values = np.linspace(-np.pi, np.pi, n_per_dim, endpoint=False)

        # Create n-dimensional grid
        if self.n_chi == 1:
            return chi_values.reshape(-1, 1)
        else:
            grids = [chi_values] * self.n_chi
            mesh = np.meshgrid(*grids, indexing='ij')
            points = np.stack([m.ravel() for m in mesh], axis=1)
            return points

    def _compute_voronoi(self):
        """
        Compute Voronoi tessellation in Z²-scaled space.

        The Z² metric scales distances, affecting cell boundaries.
        """
        # Scale points by 1/Z for proper metric
        scaled_points = self.grid_points / Z

        # For periodic boundary (torus), we need to replicate points
        # This is a simplified version - full implementation would use
        # periodic Voronoi
        try:
            vor = Voronoi(scaled_points)
            return vor
        except:
            return None

    def get_nearest_rotamer(self, chi_angles):
        """
        Find the nearest Z²-quantized rotamer.

        Args:
            chi_angles: Array of chi angles

        Returns:
            Nearest rotamer (quantized chi angles)
        """
        if self.grid_points is None:
            return np.array([])

        chi_angles = np.array(chi_angles).flatten()[:self.n_chi]

        # Compute distances to all grid points
        # Use Z²-scaled metric
        diff = self.grid_points - chi_angles

        # Wrap to [-π, π]
        diff = np.mod(diff + np.pi, 2*np.pi) - np.pi

        # Z²-scaled distance
        distances = np.sqrt(np.sum(diff**2, axis=1)) / Z

        # Return nearest
        nearest_idx = np.argmin(distances)
        return self.grid_points[nearest_idx]

    def get_rotamer_library(self, steric_filter=True):
        """
        Generate Z²-derived rotamer library.

        Args:
            steric_filter: If True, remove sterically forbidden rotamers

        Returns:
            List of (chi_angles, probability) tuples
        """
        if self.grid_points is None:
            return [(np.array([]), 1.0)]

        rotamers = []

        for point in self.grid_points:
            # Probability based on Z² distance from harmonic positions
            # Harmonic positions are multiples of 2π/Z
            harmonic_dist = self._distance_to_harmonic(point)
            prob = np.exp(-harmonic_dist**2 / (2 * THETA_Z2**2))

            if steric_filter:
                # Check for obvious steric clashes
                if self._is_sterically_allowed(point):
                    rotamers.append((point, prob))
            else:
                rotamers.append((point, prob))

        # Normalize probabilities
        if rotamers:
            total_prob = sum(p for _, p in rotamers)
            rotamers = [(chi, p/total_prob) for chi, p in rotamers]

        return sorted(rotamers, key=lambda x: -x[1])

    def _distance_to_harmonic(self, chi_angles):
        """Distance to nearest Z²-harmonic point."""
        harmonic_spacing = 2 * np.pi / Z
        dist = 0
        for chi in chi_angles:
            # Nearest harmonic multiple
            n = np.round(chi / harmonic_spacing)
            harmonic = n * harmonic_spacing
            dist += (chi - harmonic)**2
        return np.sqrt(dist)

    def _is_sterically_allowed(self, chi_angles):
        """
        Check if rotamer is sterically allowed.

        Uses simplified steric check based on eclipsing.
        """
        for chi in chi_angles:
            # Eclipsed conformations (0°, ±120°) are disfavored
            chi_deg = np.degrees(chi)
            chi_mod = chi_deg % 120
            if chi_mod < 15 or chi_mod > 105:
                return False
        return True


# ==============================================================================
# VORONOI PACKING ENGINE
# ==============================================================================

class Z2VoronoiPacker:
    """
    Pack side chains using Z² Voronoi tessellation.

    This replaces empirical rotamer libraries with geometric
    constraints derived from the Z² metric.
    """

    def __init__(self, sequence, backbone_coords):
        """
        Initialize packer.

        Args:
            sequence: Amino acid sequence
            backbone_coords: Cα coordinates (N x 3)
        """
        self.sequence = sequence
        self.n = len(sequence)
        self.backbone = backbone_coords.copy()

        # Initialize rotamer spaces for each residue type
        self.rotamer_spaces = {}
        for aa in set(sequence):
            n_chi = N_CHI.get(aa, 0)
            self.rotamer_spaces[aa] = Z2RotamerSpace(n_chi)

        # Store packed chi angles
        self.chi_angles = [None] * self.n

        # Store side chain coordinates
        self.side_chain_coords = [None] * self.n

    def pack_all(self, method='greedy'):
        """
        Pack all side chains.

        Args:
            method: 'greedy' or 'monte_carlo'
        """
        if method == 'greedy':
            self._pack_greedy()
        elif method == 'monte_carlo':
            self._pack_monte_carlo()
        else:
            self._pack_greedy()

    def _pack_greedy(self):
        """
        Greedy packing: place each side chain in best rotamer.
        """
        # Order residues by number of contacts (most constrained first)
        contact_count = self._compute_contact_counts()
        order = np.argsort(-contact_count)

        for idx in order:
            aa = self.sequence[idx]

            if N_CHI.get(aa, 0) == 0:
                continue

            # Get rotamer library
            space = self.rotamer_spaces[aa]
            rotamers = space.get_rotamer_library()

            # Find best rotamer (least clashes)
            best_rotamer = None
            best_score = float('inf')

            for chi, prob in rotamers[:20]:  # Top 20 rotamers
                # Build side chain
                coords = self._build_side_chain(idx, chi)

                # Score clashes
                clash_score = self._score_clashes(idx, coords)

                # Total score (prefer high probability, low clashes)
                score = clash_score - np.log(prob + 1e-10)

                if score < best_score:
                    best_score = score
                    best_rotamer = chi
                    best_coords = coords

            self.chi_angles[idx] = best_rotamer
            self.side_chain_coords[idx] = best_coords

    def _pack_monte_carlo(self, n_steps=1000, temperature=1.0):
        """
        Monte Carlo packing: sample rotamer space.
        """
        # Initialize with greedy
        self._pack_greedy()

        # Current energy
        current_energy = self._total_energy()

        for step in range(n_steps):
            # Pick random residue
            idx = np.random.randint(self.n)
            aa = self.sequence[idx]

            if N_CHI.get(aa, 0) == 0:
                continue

            # Current chi
            old_chi = self.chi_angles[idx]
            old_coords = self.side_chain_coords[idx]

            # Sample new rotamer
            space = self.rotamer_spaces[aa]
            rotamers = space.get_rotamer_library()

            if not rotamers:
                continue

            # Random selection weighted by probability
            probs = np.array([p for _, p in rotamers])
            probs = probs / probs.sum()
            choice = np.random.choice(len(rotamers), p=probs)
            new_chi = rotamers[choice][0]

            # Build new side chain
            new_coords = self._build_side_chain(idx, new_chi)

            # New energy
            self.chi_angles[idx] = new_chi
            self.side_chain_coords[idx] = new_coords
            new_energy = self._total_energy()

            # Metropolis criterion
            dE = new_energy - current_energy
            if dE < 0 or np.random.random() < np.exp(-dE / temperature):
                current_energy = new_energy
            else:
                # Revert
                self.chi_angles[idx] = old_chi
                self.side_chain_coords[idx] = old_coords

            # Adaptive temperature
            temperature *= 0.995

    def _compute_contact_counts(self):
        """Count backbone contacts for each residue."""
        counts = np.zeros(self.n)

        for i in range(self.n):
            for j in range(i + 4, self.n):
                d = np.linalg.norm(self.backbone[i] - self.backbone[j])
                if d < Z:  # Within Z distance
                    counts[i] += 1
                    counts[j] += 1

        return counts

    def _build_side_chain(self, idx, chi_angles):
        """
        Build side chain coordinates from chi angles.

        This is a simplified model using ideal geometry.
        """
        aa = self.sequence[idx]
        atoms = SIDE_CHAIN_ATOMS.get(aa, [])

        if not atoms or chi_angles is None:
            return np.zeros((0, 3))

        coords = []

        # Start from Cα
        ca = self.backbone[idx]

        # Get local frame from backbone
        if idx > 0 and idx < self.n - 1:
            v1 = self.backbone[idx] - self.backbone[idx-1]
            v2 = self.backbone[idx+1] - self.backbone[idx]
            n = np.cross(v1, v2)
            n = n / (np.linalg.norm(n) + 1e-10)
        else:
            n = np.array([0, 0, 1])

        # Build atoms along side chain
        current_pos = ca.copy()
        bond_length = 1.54  # C-C bond

        for i, atom in enumerate(atoms):
            if i < len(chi_angles):
                chi = chi_angles[i]
            else:
                chi = 0

            # Rotate and extend
            direction = np.array([
                np.cos(chi),
                np.sin(chi) * np.cos(THETA_Z2),
                np.sin(chi) * np.sin(THETA_Z2)
            ])

            current_pos = current_pos + bond_length * direction
            coords.append(current_pos.copy())

        return np.array(coords) if coords else np.zeros((0, 3))

    def _score_clashes(self, idx, coords):
        """Score steric clashes for side chain."""
        if coords.size == 0:
            return 0

        score = 0

        # Check against backbone
        for i in range(self.n):
            if abs(i - idx) <= 1:
                continue
            d = np.min(np.linalg.norm(coords - self.backbone[i], axis=1))
            if d < 2.5:
                score += (2.5 - d)**2

        # Check against other side chains
        for i in range(self.n):
            if i == idx:
                continue
            if self.side_chain_coords[i] is not None and self.side_chain_coords[i].size > 0:
                d = cdist(coords, self.side_chain_coords[i]).min()
                if d < 2.5:
                    score += (2.5 - d)**2

        return score

    def _total_energy(self):
        """Compute total energy of packed structure."""
        energy = 0

        for i in range(self.n):
            if self.side_chain_coords[i] is not None:
                energy += self._score_clashes(i, self.side_chain_coords[i])

        return energy

    def get_packing_statistics(self):
        """Compute packing statistics."""
        stats = {
            'n_residues': self.n,
            'n_packed': sum(1 for c in self.chi_angles if c is not None),
            'total_energy': self._total_energy(),
            'clashes': 0,
            'z2_quantization_rmsd': 0
        }

        # Count clashes
        for i in range(self.n):
            if self.side_chain_coords[i] is not None:
                clash = self._score_clashes(i, self.side_chain_coords[i])
                if clash > 0.5:
                    stats['clashes'] += 1

        # Measure Z² quantization
        quantization_errors = []
        for i in range(self.n):
            if self.chi_angles[i] is not None:
                space = self.rotamer_spaces[self.sequence[i]]
                quantized = space.get_nearest_rotamer(self.chi_angles[i])
                error = np.linalg.norm(self.chi_angles[i] - quantized)
                quantization_errors.append(error)

        if quantization_errors:
            stats['z2_quantization_rmsd'] = np.sqrt(np.mean(np.array(quantization_errors)**2))

        return stats


# ==============================================================================
# Z² ROTAMER LIBRARY GENERATOR
# ==============================================================================

def generate_z2_rotamer_library():
    """
    Generate complete Z²-derived rotamer library.

    This replaces Dunbrack library with geometric constraints.
    """
    library = {}

    for aa, n_chi in N_CHI.items():
        if n_chi == 0:
            library[aa] = []
            continue

        space = Z2RotamerSpace(n_chi)
        rotamers = space.get_rotamer_library(steric_filter=True)

        # Convert to list format
        library[aa] = [
            {
                'chi': chi.tolist() if hasattr(chi, 'tolist') else list(chi),
                'probability': float(prob)
            }
            for chi, prob in rotamers[:12]  # Top 12 rotamers
        ]

    return library


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # Test on insulin B-chain (diabetes treatment target)
    INSULIN_B = "FVNQHLCGSHLVEALYLVCGERGFFYTPKT"

    print(f"\nAnalyzing: Insulin B-chain ({len(INSULIN_B)} residues)")
    print(f"Sequence: {INSULIN_B}")
    print("="*80)

    # Generate Z² rotamer library
    print("\nGenerating Z² Rotamer Library...")
    library = generate_z2_rotamer_library()

    print("\nZ² Rotamer counts per residue type:")
    for aa in sorted(library.keys()):
        n_rot = len(library[aa])
        n_chi = N_CHI.get(aa, 0)
        print(f"  {aa}: {n_rot} rotamers ({n_chi} chi angles)")

    # Create mock backbone (extended then collapsed)
    n = len(INSULIN_B)
    backbone = np.zeros((n, 3))

    # Create compact structure
    for i in range(n):
        # Helical arrangement
        theta = i * THETA_Z2
        r = Z * 1.5
        backbone[i] = [
            r * np.cos(theta),
            r * np.sin(theta),
            i * 1.5  # Rise per residue
        ]

    # Pack side chains
    print("\nPacking side chains with Z² Voronoi method...")
    packer = Z2VoronoiPacker(INSULIN_B, backbone)
    packer.pack_all(method='monte_carlo')

    # Get statistics
    stats = packer.get_packing_statistics()

    print("\nPacking Results:")
    print(f"  Residues packed: {stats['n_packed']}/{stats['n_residues']}")
    print(f"  Total energy: {stats['total_energy']:.2f}")
    print(f"  Clash count: {stats['clashes']}")
    print(f"  Z² quantization RMSD: {stats['z2_quantization_rmsd']:.3f} rad")

    # Analyze chi angle distribution
    print("\nChi angle analysis:")
    chi_by_type = {}
    for i in range(n):
        aa = INSULIN_B[i]
        if packer.chi_angles[i] is not None:
            if aa not in chi_by_type:
                chi_by_type[aa] = []
            chi_by_type[aa].append(packer.chi_angles[i])

    for aa in sorted(chi_by_type.keys()):
        chis = chi_by_type[aa]
        if chis:
            mean_chi1 = np.mean([c[0] for c in chis])
            print(f"  {aa}: n={len(chis)}, mean χ1={np.degrees(mean_chi1):.1f}°")

    # Save results
    results = {
        'framework': 'Z² Voronoi Rotamer Packing',
        'timestamp': datetime.now().isoformat(),
        'Z2': Z2,
        'theta_Z2_deg': np.degrees(THETA_Z2),
        'sequence': INSULIN_B,
        'packing_stats': stats,
        'rotamer_library': library,
        'chi_angles': [
            c.tolist() if c is not None and hasattr(c, 'tolist') else None
            for c in packer.chi_angles
        ]
    }

    with open('z2_voronoi_packing_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nSaved to z2_voronoi_packing_results.json")

    # Compare with standard rotamer positions
    print("\n" + "="*80)
    print("VALIDATION: Z² vs Standard Rotamer Positions")
    print("="*80)

    # Standard gauche+, trans, gauche- for χ1
    standard_chi1 = [-60, 180, 60]  # degrees
    z2_chi1 = np.degrees(THETA_Z2 * np.arange(-6, 7))  # Z² harmonic positions

    print("\nStandard χ1 rotamers: -60°, 180°, 60°")
    print(f"Z² harmonic positions (θ_Z² = {np.degrees(THETA_Z2):.1f}°):")

    for std in standard_chi1:
        nearest_z2 = min(z2_chi1, key=lambda x: abs(x - std))
        print(f"  Standard {std:4d}° → Z² {nearest_z2:6.1f}° (Δ = {abs(std - nearest_z2):.1f}°)")

    return results


if __name__ == '__main__':
    main()
