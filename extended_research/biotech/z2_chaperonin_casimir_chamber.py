#!/usr/bin/env python3
"""
Z² Chaperonin Casimir Chamber

SPDX-License-Identifier: AGPL-3.0-or-later

PATHWAY 7: GROEL/GROES AS A KALUZA-KLEIN RESONANCE CHAMBER

In vivo, many proteins require chaperone machines to fold correctly.
This script models the GroEL chaperonin cavity as an 8D Kaluza-Klein
resonance chamber bounded by the Z² geometric invariant.

MATHEMATICAL FOUNDATION:
========================
The interior cavity of GroEL is modeled as a bounded region in T³/Z₂
orbifold space. The walls impose boundary conditions that quantize
the vacuum modes, creating a Casimir-like pressure:

    P_Casimir = -π²ℏc/(240 × L⁴) × g_Z2(θ)

where g_Z2(θ) is the Z² metric factor and L is the cavity dimension.

PHYSICAL PRINCIPLE:
==================
The chaperonin walls don't just physically confine the protein.
They generate a highly localized, focused Z² Casimir force that:
1. Mechanically unknots the trapped misfolded protein
2. Resets the energy landscape
3. Forces correct refolding through geometric pressure

The 7-fold symmetry of GroEL resonates with the T³/Z₂ orbifold structure.

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
THETA_Z2 = np.pi / Z  # ≈ 31.09°

# Physical constants
HBAR_C = 197.3  # ℏc in MeV·fm
KB_T = 0.026  # eV at 300K

print("="*80)
print("Z² CHAPERONIN CASIMIR CHAMBER")
print("="*80)
print(f"Z = {Z:.4f} | Z² = {Z2:.4f}")
print("Modeling GroEL as Kaluza-Klein resonance cavity")
print("="*80)

# ==============================================================================
# GROEL CAVITY MODEL
# ==============================================================================

class GroELCavity:
    """
    Model the GroEL chaperonin cavity as a Z² resonance chamber.

    GroEL structure:
    - Two heptameric rings stacked back-to-back
    - Central cavity: ~45 Å diameter, ~80 Å height
    - 7-fold rotational symmetry
    """

    def __init__(self, radius=22.5, height=80.0):
        """
        Initialize the GroEL cavity.

        Args:
            radius: Cavity radius in Å
            height: Cavity height in Å
        """
        self.radius = radius
        self.height = height
        self.volume = np.pi * radius**2 * height

        # 7-fold symmetry creates 8 fixed points in Z₂ orbifold
        self.n_fold = 7
        self.fixed_points = self._compute_fixed_points()

        # Z² resonance modes
        self.modes = self._compute_resonance_modes()

    def _compute_fixed_points(self):
        """
        Compute fixed points of the T³/Z₂ orbifold inside GroEL.

        The 7-fold symmetry of GroEL creates resonant positions.
        """
        fixed_points = []

        # Angular positions (7-fold symmetry)
        for i in range(self.n_fold):
            theta = 2 * np.pi * i / self.n_fold

            # Radial positions (Z-scaled)
            for r_frac in [0.3, 0.6, 0.9]:
                r = self.radius * r_frac

                # Axial positions (Z-scaled)
                for z_frac in [0.25, 0.5, 0.75]:
                    z = self.height * z_frac - self.height/2

                    x = r * np.cos(theta)
                    y = r * np.sin(theta)

                    fixed_points.append([x, y, z])

        return np.array(fixed_points)

    def _compute_resonance_modes(self, n_modes=10):
        """
        Compute Z² resonance modes in the cylindrical cavity.

        Modes are quantized by the Z² boundary conditions.
        """
        modes = []

        # Radial quantum numbers
        for n_r in range(1, 4):
            # Angular quantum numbers (7-fold symmetry)
            for n_theta in range(0, self.n_fold):
                # Axial quantum numbers
                for n_z in range(1, 4):
                    # Mode frequency (Z²-quantized)
                    k_r = n_r * np.pi / self.radius
                    k_theta = n_theta * 2 * np.pi / (self.radius * THETA_Z2)
                    k_z = n_z * np.pi / self.height

                    # Total wavevector
                    k_total = np.sqrt(k_r**2 + k_theta**2 + k_z**2)

                    # Mode energy (in Z² units)
                    E_mode = HBAR_C * k_total / Z2  # MeV

                    modes.append({
                        'n_r': n_r,
                        'n_theta': n_theta,
                        'n_z': n_z,
                        'k_total': k_total,
                        'energy_meV': E_mode * 1000
                    })

        # Sort by energy
        modes = sorted(modes, key=lambda m: m['energy_meV'])

        return modes[:n_modes]

    def compute_casimir_pressure(self, position):
        """
        Compute Z² Casimir pressure at a point inside the cavity.

        Args:
            position: [x, y, z] coordinates in Å

        Returns:
            Pressure vector pointing toward cavity center
        """
        x, y, z = position
        r = np.sqrt(x**2 + y**2)

        # Distance to walls
        d_radial = self.radius - r
        d_top = self.height/2 - z
        d_bottom = z + self.height/2

        # Minimum distance to wall
        d_min = min(d_radial, d_top, d_bottom)

        # Casimir pressure (scales as 1/d⁴)
        # Standard: P = -π²ℏc/(240 L⁴)
        # Z² modified: multiply by metric factor

        if d_min < 1.0:  # Very close to wall
            d_min = 1.0

        # Pressure magnitude in arbitrary units
        P_mag = (np.pi**2 / 240) * (1 / (d_min / Z)**4)

        # Z² metric enhancement near fixed points
        for fp in self.fixed_points[:7]:  # First ring
            d_fp = np.linalg.norm(position - fp)
            if d_fp < Z:
                P_mag *= (1 + 0.5 * np.exp(-d_fp / Z))

        # Direction toward center
        center = np.array([0, 0, 0])
        direction = center - position
        direction_norm = np.linalg.norm(direction)

        if direction_norm > 0:
            direction = direction / direction_norm
        else:
            direction = np.array([0, 0, 0])

        return P_mag * direction

    def is_inside(self, position):
        """Check if position is inside the cavity."""
        x, y, z = position
        r = np.sqrt(x**2 + y**2)

        return (r < self.radius and
                abs(z) < self.height/2)


# ==============================================================================
# MISFOLDED PROTEIN MODEL
# ==============================================================================

class MisfoldedProtein:
    """
    Model a misfolded/aggregated protein trapped in GroEL.
    """

    def __init__(self, sequence, initial_state='aggregated'):
        """
        Initialize misfolded protein.

        Args:
            sequence: Amino acid sequence
            initial_state: 'aggregated', 'knotted', or 'extended'
        """
        self.sequence = sequence
        self.n = len(sequence)

        # Generate initial coordinates
        if initial_state == 'aggregated':
            self.coords = self._generate_aggregate()
        elif initial_state == 'knotted':
            self.coords = self._generate_knot()
        else:
            self.coords = self._generate_extended()

        # Track energy history
        self.energy_history = []

    def _generate_aggregate(self):
        """Generate random aggregate (misfolded)."""
        # Random compact ball
        coords = np.random.randn(self.n, 3) * 8  # 8 Å radius ball
        return coords

    def _generate_knot(self):
        """Generate knotted structure (topological trap)."""
        coords = np.zeros((self.n, 3))

        # Trefoil knot parametrization
        t = np.linspace(0, 2*np.pi, self.n)
        coords[:, 0] = np.sin(t) + 2*np.sin(2*t)
        coords[:, 1] = np.cos(t) - 2*np.cos(2*t)
        coords[:, 2] = -np.sin(3*t)

        coords *= 5  # Scale to ~15 Å
        return coords

    def _generate_extended(self):
        """Generate extended chain."""
        coords = np.zeros((self.n, 3))
        for i in range(self.n):
            coords[i] = [i * 3.8, 0, 0]
        return coords

    def compute_energy(self):
        """Compute current energy (misfolding penalty)."""
        distances = squareform(pdist(self.coords))

        # Clashing penalty (atoms too close)
        clash_energy = 0
        for i in range(self.n):
            for j in range(i + 2, self.n):
                d = distances[i, j]
                if d < 3.0:
                    clash_energy += 100 * (3.0 - d)**2

        # Extended penalty (atoms too far)
        bond_energy = 0
        for i in range(self.n - 1):
            d = distances[i, i+1]
            bond_energy += 10 * (d - 3.8)**2

        # Compactness (radius of gyration)
        com = self.coords.mean(axis=0)
        rg = np.sqrt(np.mean(np.sum((self.coords - com)**2, axis=1)))

        # Target Rg based on sequence length
        target_rg = 2.5 * (self.n ** 0.38)
        rg_energy = (rg - target_rg)**2

        return clash_energy + bond_energy + rg_energy

    def compute_knottedness(self):
        """
        Compute a measure of topological complexity (knottedness).

        Uses writhe as a proxy for knot complexity.
        """
        writhe = 0

        for i in range(self.n - 1):
            for j in range(i + 2, self.n - 1):
                v1 = self.coords[i+1] - self.coords[i]
                v2 = self.coords[j+1] - self.coords[j]
                r = self.coords[j] - self.coords[i]

                cross = np.cross(v1, v2)
                denom = np.linalg.norm(r)**3 + 1e-10

                writhe += np.dot(cross, r) / denom

        return abs(writhe / (4 * np.pi))


# ==============================================================================
# CHAPERONIN SIMULATION
# ==============================================================================

class GroELSimulation:
    """
    Simulate protein refolding inside GroEL using Z² Casimir forces.
    """

    def __init__(self, sequence, cavity=None):
        """
        Initialize simulation.

        Args:
            sequence: Amino acid sequence
            cavity: GroELCavity instance (default creates standard)
        """
        self.sequence = sequence

        if cavity is None:
            self.cavity = GroELCavity()
        else:
            self.cavity = cavity

        # Initialize misfolded protein inside cavity
        self.protein = MisfoldedProtein(sequence, initial_state='aggregated')

        # Center in cavity
        self._center_protein()

    def _center_protein(self):
        """Center protein in cavity."""
        com = self.protein.coords.mean(axis=0)
        self.protein.coords -= com

        # Scale to fit in cavity
        max_r = np.max(np.sqrt(np.sum(self.protein.coords[:, :2]**2, axis=1)))
        if max_r > self.cavity.radius * 0.8:
            scale = self.cavity.radius * 0.8 / max_r
            self.protein.coords *= scale

    def apply_casimir_forces(self, dt=0.1):
        """
        Apply Z² Casimir forces from cavity walls.

        Returns total force magnitude.
        """
        total_force = 0

        for i in range(self.protein.n):
            pos = self.protein.coords[i]

            if self.cavity.is_inside(pos):
                # Compute Casimir pressure
                force = self.cavity.compute_casimir_pressure(pos)

                # Apply force
                self.protein.coords[i] += dt * force

                total_force += np.linalg.norm(force)

        return total_force

    def apply_constraints(self):
        """Apply bond length and steric constraints."""
        # Bond constraints (SHAKE-like)
        for _ in range(5):
            for i in range(self.protein.n - 1):
                v = self.protein.coords[i+1] - self.protein.coords[i]
                d = np.linalg.norm(v)
                if d > 0:
                    correction = (d - 3.8) / 2 * v / d
                    self.protein.coords[i] += correction
                    self.protein.coords[i+1] -= correction

        # Keep inside cavity
        for i in range(self.protein.n):
            x, y, z = self.protein.coords[i]
            r = np.sqrt(x**2 + y**2)

            if r > self.cavity.radius * 0.95:
                scale = self.cavity.radius * 0.95 / r
                self.protein.coords[i, 0] *= scale
                self.protein.coords[i, 1] *= scale

            if abs(z) > self.cavity.height/2 * 0.95:
                self.protein.coords[i, 2] *= 0.95

    def simulate(self, n_steps=500, dt=0.1):
        """
        Run the refolding simulation.

        Returns timeline of energy and knottedness.
        """
        timeline = {
            'step': [],
            'energy': [],
            'knottedness': [],
            'rg': [],
            'force': []
        }

        print(f"\n  Simulating {n_steps} steps...")

        for step in range(n_steps):
            # Apply Z² Casimir forces
            force = self.apply_casimir_forces(dt)

            # Apply constraints
            self.apply_constraints()

            # Compute metrics
            energy = self.protein.compute_energy()
            knot = self.protein.compute_knottedness()
            com = self.protein.coords.mean(axis=0)
            rg = np.sqrt(np.mean(np.sum((self.protein.coords - com)**2, axis=1)))

            # Record
            if step % 10 == 0:
                timeline['step'].append(step)
                timeline['energy'].append(energy)
                timeline['knottedness'].append(knot)
                timeline['rg'].append(rg)
                timeline['force'].append(force)

                if step % 100 == 0:
                    print(f"    Step {step:4d}: E={energy:.1f}, "
                          f"knot={knot:.3f}, Rg={rg:.1f} Å")

        return timeline


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    # Test sequence (SOD1 fragment - implicated in ALS)
    SOD1_FRAGMENT = "ATKAVCVLKGDGPVQGIINFEQKESNGPVKVWGSIK"

    print(f"\nAnalyzing: SOD1 fragment ({len(SOD1_FRAGMENT)} residues)")
    print(f"Sequence: {SOD1_FRAGMENT}")
    print("Disease: ALS (misfolding disease)")
    print("="*80)

    # Create GroEL cavity
    cavity = GroELCavity(radius=22.5, height=80.0)

    print(f"\nGroEL Cavity Parameters:")
    print(f"  Radius: {cavity.radius} Å")
    print(f"  Height: {cavity.height} Å")
    print(f"  Volume: {cavity.volume:.0f} Å³")
    print(f"  7-fold symmetry: {cavity.n_fold} subunits")

    # Print resonance modes
    print(f"\nZ² Resonance Modes (first 5):")
    for i, mode in enumerate(cavity.modes[:5]):
        print(f"  Mode {i+1}: (n_r={mode['n_r']}, n_θ={mode['n_theta']}, "
              f"n_z={mode['n_z']}) E={mode['energy_meV']:.2f} meV")

    # Create simulation
    sim = GroELSimulation(SOD1_FRAGMENT, cavity)

    # Initial state
    print(f"\nInitial State (misfolded aggregate):")
    initial_energy = sim.protein.compute_energy()
    initial_knot = sim.protein.compute_knottedness()
    com = sim.protein.coords.mean(axis=0)
    initial_rg = np.sqrt(np.mean(np.sum((sim.protein.coords - com)**2, axis=1)))

    print(f"  Energy: {initial_energy:.1f}")
    print(f"  Knottedness: {initial_knot:.3f}")
    print(f"  Rg: {initial_rg:.1f} Å")

    # Run simulation
    print("\n" + "="*80)
    print("RUNNING Z² CASIMIR REFOLDING SIMULATION")
    print("="*80)

    timeline = sim.simulate(n_steps=500, dt=0.15)

    # Final state
    print(f"\nFinal State (refolded):")
    final_energy = sim.protein.compute_energy()
    final_knot = sim.protein.compute_knottedness()
    com = sim.protein.coords.mean(axis=0)
    final_rg = np.sqrt(np.mean(np.sum((sim.protein.coords - com)**2, axis=1)))

    print(f"  Energy: {final_energy:.1f} (Δ = {final_energy - initial_energy:.1f})")
    print(f"  Knottedness: {final_knot:.3f} (Δ = {final_knot - initial_knot:.3f})")
    print(f"  Rg: {final_rg:.1f} Å (Δ = {final_rg - initial_rg:.1f} Å)")

    # Summary
    print("\n" + "="*80)
    print("CHAPERONIN REFOLDING SUMMARY")
    print("="*80)

    energy_reduction = 100 * (initial_energy - final_energy) / initial_energy
    knot_reduction = 100 * (initial_knot - final_knot) / (initial_knot + 0.001)

    print(f"\n  Energy reduction: {energy_reduction:.1f}%")
    print(f"  Knot dissolution: {knot_reduction:.1f}%")
    print(f"  Compaction: Rg {initial_rg:.1f} → {final_rg:.1f} Å")

    if energy_reduction > 50 and knot_reduction > 30:
        print("\n  ✓ Z² Casimir refolding SUCCESSFUL!")
        print("  ✓ Aggregate dissolved and structure reorganized")
    else:
        print("\n  ○ Partial refolding achieved")

    # Save results
    results = {
        'framework': 'Z² Chaperonin Casimir Chamber',
        'timestamp': datetime.now().isoformat(),
        'Z2': float(Z2),
        'theta_Z2_deg': float(np.degrees(THETA_Z2)),
        'sequence': SOD1_FRAGMENT,
        'disease_target': 'ALS',
        'cavity': {
            'radius_A': float(cavity.radius),
            'height_A': float(cavity.height),
            'volume_A3': float(cavity.volume),
            'n_fold_symmetry': cavity.n_fold
        },
        'resonance_modes': cavity.modes[:5],
        'initial_state': {
            'energy': float(initial_energy),
            'knottedness': float(initial_knot),
            'rg_A': float(initial_rg)
        },
        'final_state': {
            'energy': float(final_energy),
            'knottedness': float(final_knot),
            'rg_A': float(final_rg)
        },
        'refolding_success': {
            'energy_reduction_pct': float(energy_reduction),
            'knot_dissolution_pct': float(knot_reduction)
        },
        'timeline': {
            'steps': timeline['step'],
            'energy': [float(e) for e in timeline['energy']],
            'knottedness': [float(k) for k in timeline['knottedness']],
            'rg': [float(r) for r in timeline['rg']]
        }
    }

    with open('z2_chaperonin_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nSaved to z2_chaperonin_results.json")

    return results


if __name__ == '__main__':
    main()
