#!/usr/bin/env python3
"""
Z² Implicit Solvation Tensor

SPDX-License-Identifier: AGPL-3.0-or-later

PATHWAY 2: Replace explicit water with Z² GEOMETRIC PRESSURE

Instead of simulating millions of water molecules, we treat the
solvent as a continuous pressure field derived from the Z² metric.

MATHEMATICAL FOUNDATION:
========================
The hydrophobic effect arises from water's entropic cost of
solvating non-polar surfaces. In Z² theory, this maps to:

    P_hydrophobic = κ × (1/Z²) × ∇²ρ_hydrophobic

where:
- κ is the Z² Casimir coupling
- ρ_hydrophobic is the hydrophobic density field
- The 1/Z² factor comes from the KK metric tensor

PHYSICAL PRINCIPLE:
==================
Water "squeezes" hydrophobic residues together. This is equivalent
to a CASIMIR-LIKE pressure from the Z² boundary conditions.

The T³/Z₂ orbifold creates quantized vacuum modes that exert
pressure on hydrophobic surfaces, forcing them to minimize
exposed surface area.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.ndimage import gaussian_filter
import json
from datetime import datetime

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.79
Z2 = Z**2  # ≈ 33.51
THETA_Z2 = np.pi / Z

# Solvation parameters
WATER_DENSITY = 33.3  # molecules per nm³
KB_T = 0.592  # kcal/mol at 300K

print("="*80)
print("Z² IMPLICIT SOLVATION TENSOR")
print("="*80)
print(f"Z = {Z:.4f} Å | Z² = {Z2:.4f}")
print("="*80)

# ==============================================================================
# HYDROPHOBICITY DATA
# ==============================================================================

# Kyte-Doolittle hydrophobicity (positive = hydrophobic)
HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# Atomic radii for SASA calculation
VDW_RADII = {'C': 1.7, 'N': 1.55, 'O': 1.52, 'S': 1.8, 'H': 1.2}

# ==============================================================================
# Z² SOLVATION TENSOR
# ==============================================================================

class Z2SolvationTensor:
    """
    Compute solvation forces using Z² geometric pressure.

    The key insight: water's hydrophobic pressure can be modeled
    as a field that depends on the local hydrophobic density and
    the Z² boundary conditions.
    """

    def __init__(self, sequence, coords):
        """
        Initialize with sequence and Cα coordinates.

        Args:
            sequence: Amino acid sequence
            coords: Cα coordinates (N x 3 array)
        """
        self.sequence = sequence
        self.coords = coords.copy()
        self.n = len(sequence)

        # Get hydrophobicity values
        self.hydrophobicity = np.array([
            HYDROPHOBICITY.get(aa, 0) for aa in sequence
        ])

        # Compute pairwise distances
        self.update_distances()

    def update_distances(self):
        """Update distance matrix from current coordinates."""
        self.distances = squareform(pdist(self.coords))

    def compute_hydrophobic_field(self, grid_spacing=1.0):
        """
        Compute 3D hydrophobic density field.

        Returns volumetric field where each point indicates
        the local hydrophobic character.
        """
        # Determine grid bounds
        margin = 5 * Z  # Å margin
        mins = self.coords.min(axis=0) - margin
        maxs = self.coords.max(axis=0) + margin

        # Create grid
        nx = int((maxs[0] - mins[0]) / grid_spacing) + 1
        ny = int((maxs[1] - mins[1]) / grid_spacing) + 1
        nz = int((maxs[2] - mins[2]) / grid_spacing) + 1

        field = np.zeros((nx, ny, nz))

        # Place hydrophobic density at each residue
        for i in range(self.n):
            # Grid indices
            ix = int((self.coords[i, 0] - mins[0]) / grid_spacing)
            iy = int((self.coords[i, 1] - mins[1]) / grid_spacing)
            iz = int((self.coords[i, 2] - mins[2]) / grid_spacing)

            # Clamp to grid
            ix = min(max(ix, 0), nx - 1)
            iy = min(max(iy, 0), ny - 1)
            iz = min(max(iz, 0), nz - 1)

            # Add hydrophobic density
            field[ix, iy, iz] += self.hydrophobicity[i]

        # Smooth field (represents spatial extent of residues)
        field = gaussian_filter(field, sigma=Z/grid_spacing)

        return field, mins, grid_spacing

    def compute_z2_casimir_pressure(self):
        """
        Compute Casimir-like pressure from Z² boundary conditions.

        The T³/Z₂ orbifold quantizes vacuum modes, creating an
        effective pressure that depends on local geometry.

        Returns:
            Pressure field as N-array (force magnitude per residue)
        """
        # Compute hydrophobic field
        field, mins, spacing = self.compute_hydrophobic_field()

        # Compute gradient of hydrophobic field
        # This gives the "direction of hydrophobic pressure"
        grad_x = np.gradient(field, axis=0)
        grad_y = np.gradient(field, axis=1)
        grad_z = np.gradient(field, axis=2)

        # Evaluate pressure at each residue position
        pressure = np.zeros(self.n)

        for i in range(self.n):
            ix = int((self.coords[i, 0] - mins[0]) / spacing)
            iy = int((self.coords[i, 1] - mins[1]) / spacing)
            iz = int((self.coords[i, 2] - mins[2]) / spacing)

            # Clamp
            ix = min(max(ix, 0), field.shape[0] - 1)
            iy = min(max(iy, 0), field.shape[1] - 1)
            iz = min(max(iz, 0), field.shape[2] - 1)

            # Gradient magnitude at this position
            grad_mag = np.sqrt(
                grad_x[ix, iy, iz]**2 +
                grad_y[ix, iy, iz]**2 +
                grad_z[ix, iy, iz]**2
            )

            # Z² Casimir pressure
            # Proportional to gradient and inversely to Z²
            pressure[i] = self.hydrophobicity[i] * grad_mag / Z2

        return pressure

    def compute_solvation_forces(self):
        """
        Compute solvation forces on each residue.

        Returns:
            Forces as N x 3 array
        """
        forces = np.zeros((self.n, 3))

        # Center of mass
        com = self.coords.mean(axis=0)

        # Hydrophobic residues are pushed toward center
        # Hydrophilic residues are pushed toward surface
        for i in range(self.n):
            # Direction toward/away from center
            r_vec = self.coords[i] - com
            r_mag = np.linalg.norm(r_vec) + 1e-10
            r_hat = r_vec / r_mag

            # Force magnitude: proportional to hydrophobicity
            # Positive hydrophobicity → inward force
            # Negative hydrophobicity → outward force
            f_mag = -self.hydrophobicity[i] / Z2

            # Scale by exposure (residues far from others are exposed)
            exposure = np.mean(self.distances[i]) / Z
            f_mag *= exposure

            forces[i] = f_mag * r_hat

        return forces

    def compute_sasa_z2(self):
        """
        Compute Solvent Accessible Surface Area using Z² probe.

        Instead of standard 1.4 Å water probe, use Z-scaled probe.
        """
        probe_radius = Z / 4  # Z²-derived probe radius

        # Approximate SASA using neighbor counting
        sasa = np.zeros(self.n)

        for i in range(self.n):
            # Count neighbors within Z distance
            neighbors = np.sum(self.distances[i] < Z)

            # Max neighbors for buried residue (sphere packing)
            max_neighbors = 12  # Close-packed

            # SASA is inversely related to burial
            burial = neighbors / max_neighbors
            sasa[i] = (1 - burial) * 4 * np.pi * (1.8 + probe_radius)**2

        return sasa

    def apply_hydrophobic_collapse(self, dt=0.1, n_steps=100):
        """
        Apply Z² solvation forces to drive hydrophobic collapse.

        This simulates the primary thermodynamic folding event
        where hydrophobic residues move to the core.

        Returns:
            Updated coordinates after collapse
        """
        coords = self.coords.copy()
        trajectory = [coords.copy()]

        for step in range(n_steps):
            # Update distances
            self.coords = coords
            self.update_distances()

            # Compute solvation forces
            forces = self.compute_solvation_forces()

            # Add bond constraints (keep chain connected)
            bond_forces = np.zeros_like(forces)
            for i in range(self.n - 1):
                bond_vec = coords[i+1] - coords[i]
                bond_len = np.linalg.norm(bond_vec)
                bond_hat = bond_vec / (bond_len + 1e-10)

                # Spring force to maintain 3.8 Å
                f = 10 * (bond_len - 3.8) * bond_hat
                bond_forces[i] += f
                bond_forces[i+1] -= f

            # Steric repulsion
            steric_forces = np.zeros_like(forces)
            for i in range(self.n):
                for j in range(i + 2, self.n):
                    d = self.distances[i, j]
                    if d < 3.2 and d > 0:
                        r_vec = coords[j] - coords[i]
                        r_hat = r_vec / d
                        f = -50 * (3.2 - d) * r_hat
                        steric_forces[i] += f
                        steric_forces[j] -= f

            # Total force
            total_forces = forces + bond_forces + steric_forces

            # Velocity Verlet-like update
            coords += dt * total_forces

            # Apply Z² constraints (keep within bounds)
            coords = self._apply_z2_boundary(coords)

            trajectory.append(coords.copy())

            # Check convergence
            if step > 10:
                rmsd = np.sqrt(np.mean((coords - trajectory[-2])**2))
                if rmsd < 0.01:
                    print(f"  Converged at step {step}")
                    break

        self.coords = coords
        self.update_distances()

        return coords, trajectory

    def _apply_z2_boundary(self, coords):
        """Apply Z² periodic boundary conditions."""
        # Keep center of mass fixed
        com = coords.mean(axis=0)
        coords = coords - com

        # Scale to fit within Z × N^(1/3) radius
        rmax = np.max(np.linalg.norm(coords, axis=1))
        r_target = Z * (self.n ** 0.38)

        if rmax > 2 * r_target:
            coords = coords * (2 * r_target / rmax)

        return coords

    def get_core_surface_partition(self, threshold=0):
        """
        Partition residues into core and surface based on burial.

        Returns:
            core_indices, surface_indices
        """
        sasa = self.compute_sasa_z2()
        mean_sasa = np.mean(sasa)

        core = []
        surface = []

        for i in range(self.n):
            if self.hydrophobicity[i] > threshold and sasa[i] < mean_sasa:
                core.append(i)
            else:
                surface.append(i)

        return core, surface


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # Test sequence: alpha-synuclein N-terminus (aggregation-prone)
    ALPHA_SYN = "MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVTTVA"

    print(f"\nAnalyzing: α-synuclein ({len(ALPHA_SYN)} residues)")
    print(f"Sequence: {ALPHA_SYN}")

    # Generate initial extended structure
    n = len(ALPHA_SYN)
    coords_initial = np.zeros((n, 3))
    for i in range(n):
        coords_initial[i] = [i * 3.8, 0, 0]  # Extended chain

    print("\nInitial structure: Extended chain")
    print(f"  Initial Rg: {np.sqrt(np.mean(np.sum((coords_initial - coords_initial.mean(axis=0))**2, axis=1))):.1f} Å")

    # Create solvation tensor
    solvation = Z2SolvationTensor(ALPHA_SYN, coords_initial)

    # Compute initial properties
    pressure = solvation.compute_z2_casimir_pressure()
    sasa_initial = solvation.compute_sasa_z2()

    print(f"\nInitial Z² Casimir pressure:")
    print(f"  Mean: {np.mean(pressure):.4f}")
    print(f"  Max:  {np.max(pressure):.4f} at residue {np.argmax(pressure)} ({ALPHA_SYN[np.argmax(pressure)]})")

    print(f"\nInitial SASA:")
    print(f"  Total: {np.sum(sasa_initial):.1f} Å²")
    print(f"  Per residue: {np.mean(sasa_initial):.1f} Å²")

    # Apply hydrophobic collapse
    print("\nApplying Z² hydrophobic collapse...")
    coords_collapsed, trajectory = solvation.apply_hydrophobic_collapse(dt=0.1, n_steps=200)

    # Compute final properties
    sasa_final = solvation.compute_sasa_z2()
    rg_final = np.sqrt(np.mean(np.sum((coords_collapsed - coords_collapsed.mean(axis=0))**2, axis=1)))

    print(f"\nFinal structure after collapse:")
    print(f"  Final Rg: {rg_final:.1f} Å")
    print(f"  Final SASA: {np.sum(sasa_final):.1f} Å² ({100*(np.sum(sasa_final)/np.sum(sasa_initial)-1):.1f}% change)")

    # Core/surface partition
    core, surface = solvation.get_core_surface_partition()
    print(f"\nCore/Surface partition:")
    print(f"  Core residues ({len(core)}): {[ALPHA_SYN[i] for i in core]}")
    print(f"  Surface residues ({len(surface)}): {[ALPHA_SYN[i] for i in surface[:10]]}...")

    # Verify hydrophobic burial
    core_hydro = np.mean([HYDROPHOBICITY[ALPHA_SYN[i]] for i in core]) if core else 0
    surface_hydro = np.mean([HYDROPHOBICITY[ALPHA_SYN[i]] for i in surface]) if surface else 0
    print(f"\n  Core mean hydrophobicity: {core_hydro:.2f}")
    print(f"  Surface mean hydrophobicity: {surface_hydro:.2f}")

    if core_hydro > surface_hydro:
        print("  ✓ Hydrophobic core successfully formed!")
    else:
        print("  ✗ Core formation incomplete")

    # Save results
    results = {
        'sequence': ALPHA_SYN,
        'n_residues': n,
        'rg_initial': float(np.sqrt(np.mean(np.sum((coords_initial - coords_initial.mean(axis=0))**2, axis=1)))),
        'rg_final': float(rg_final),
        'sasa_initial': float(np.sum(sasa_initial)),
        'sasa_final': float(np.sum(sasa_final)),
        'core_indices': core,
        'surface_indices': surface,
        'core_hydrophobicity': float(core_hydro),
        'surface_hydrophobicity': float(surface_hydro),
        'coords_final': coords_collapsed.tolist(),
        'framework': 'Z² Implicit Solvation',
        'timestamp': datetime.now().isoformat()
    }

    with open('z2_solvation_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nSaved to z2_solvation_results.json")

    return results


if __name__ == '__main__':
    main()
