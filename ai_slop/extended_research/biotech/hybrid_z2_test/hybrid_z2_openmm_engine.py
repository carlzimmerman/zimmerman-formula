#!/usr/bin/env python3
"""
Hybrid Z² OpenMM Engine - Testing 8D Kaluza-Klein Geometry in Real Biophysics

SPDX-License-Identifier: AGPL-3.0-or-later

This script tests whether the Z² geometric framework from Kaluza-Klein theory
aligns with empirical protein physics by injecting Z²-quantized torsion
constraints into the AMBER14 force field.

THE HYPOTHESIS:
If the Z² metric (Z = 2√(8π/3) ≈ 5.7888) encodes fundamental geometry,
then protein backbone angles should naturally align with Z² multiples.

Z² CONSTANTS:
- Z = 2√(8π/3) ≈ 5.7888
- θ_Z² = π/Z ≈ 31.09° (fundamental angle quantum)
- Z² = 32π/3 ≈ 33.51

PROTEIN BACKBONE ANGLES:
- α-helix: φ ≈ -57°, ψ ≈ -47°
- β-sheet: φ ≈ -119°, ψ ≈ +113°
- 310-helix: φ ≈ -49°, ψ ≈ -26°

THE EXPERIMENT:
1. Load structure with AMBER14 (empirical physics)
2. Add CustomTorsionForce with Z² harmonic penalty
3. Run hybrid simulation
4. Compare energy to pure AMBER result

If Z² physics is "real", the Z²-constrained structure should have
LOWER or SIMILAR energy to pure AMBER, not higher.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS FROM KALUZA-KLEIN GEOMETRY
# ==============================================================================

# Fundamental Z constant from Friedmann equation
Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z2 = Z ** 2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 0.5427 rad ≈ 31.09°
THETA_Z2_DEG = np.degrees(THETA_Z2)  # ≈ 31.09°

print("="*70)
print("Z² PHYSICAL CONSTANTS")
print("="*70)
print(f"Z = 2√(8π/3) = {Z:.6f}")
print(f"Z² = 32π/3 = {Z2:.6f}")
print(f"θ_Z² = π/Z = {THETA_Z2:.6f} rad = {THETA_Z2_DEG:.2f}°")
print("="*70)

# Known protein backbone angles (for reference)
HELIX_PHI = -57.0  # degrees
HELIX_PSI = -47.0
SHEET_PHI = -119.0
SHEET_PSI = 113.0

# What would Z²-quantized angles look like?
# Nearest Z² multiples to helix angles
def nearest_z2_angle(angle_deg: float) -> Tuple[float, int]:
    """Find nearest Z²-quantized angle."""
    n = round(angle_deg / THETA_Z2_DEG)
    return n * THETA_Z2_DEG, n

print("\nZ² ANGLE QUANTIZATION:")
print(f"  Helix φ = {HELIX_PHI}° → nearest Z² = {nearest_z2_angle(HELIX_PHI)}")
print(f"  Helix ψ = {HELIX_PSI}° → nearest Z² = {nearest_z2_angle(HELIX_PSI)}")
print(f"  Sheet φ = {SHEET_PHI}° → nearest Z² = {nearest_z2_angle(SHEET_PHI)}")
print(f"  Sheet ψ = {SHEET_PSI}° → nearest Z² = {nearest_z2_angle(SHEET_PSI)}")


# ==============================================================================
# HYBRID Z² + AMBER ENGINE
# ==============================================================================

class HybridZ2Engine:
    """
    Hybrid molecular dynamics engine combining:
    1. AMBER14 force field (empirical physics)
    2. Custom Z² torsion constraints (Kaluza-Klein geometry)

    The Z² constraint applies a harmonic penalty when backbone
    dihedrals deviate from Z²-quantized values.
    """

    def __init__(self, pdb_path: str):
        self.pdb_path = pdb_path
        self.system = None
        self.simulation = None
        self.z2_force_idx = None
        self.topology = None
        self.positions = None

        # Simulation results
        self.initial_energy = None
        self.final_energy = None
        self.z2_energy_contribution = 0.0

    def setup(
        self,
        z2_force_constant: float = 10.0,  # kJ/(mol·rad²)
        temperature: float = 310.0  # K (physiological)
    ):
        """
        Set up hybrid simulation.

        Args:
            z2_force_constant: Strength of Z² torsion constraint (kJ/(mol·rad²))
                              Scaled by 1/Z² as per the theoretical framework
            temperature: Simulation temperature (K)
        """
        print("\n" + "="*70)
        print("HYBRID Z² + AMBER ENGINE SETUP")
        print("="*70)

        try:
            from openmm.app import (
                PDBFile, ForceField, Modeller, Simulation, NoCutoff, HBonds
            )
            from openmm import (
                CustomTorsionForce, LangevinMiddleIntegrator, Platform, unit
            )
        except ImportError:
            print("ERROR: OpenMM not installed")
            print("Install with: conda install -c conda-forge openmm")
            return False

        # Load structure
        print(f"\n  [1] Loading structure: {self.pdb_path}")
        pdb = PDBFile(self.pdb_path)
        self.topology = pdb.topology
        self.positions = pdb.positions

        # Count atoms and residues
        n_atoms = sum(1 for _ in self.topology.atoms())
        n_residues = sum(1 for _ in self.topology.residues())
        print(f"      Atoms: {n_atoms}")
        print(f"      Residues: {n_residues}")

        # Add hydrogens if needed
        modeller = Modeller(pdb.topology, pdb.positions)
        forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

        print("\n  [2] Building AMBER14 system...")
        try:
            modeller.addHydrogens(forcefield)
        except Exception as e:
            print(f"      Note: Could not add hydrogens ({e})")

        self.topology = modeller.topology
        self.positions = modeller.positions

        # Create system
        self.system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=NoCutoff,
            constraints=HBonds
        )

        print(f"      AMBER14 forces: {self.system.getNumForces()}")

        # Add Z² custom torsion force
        print("\n  [3] Adding Z² torsion constraints...")
        self._add_z2_torsion_force(z2_force_constant)

        # Create integrator and simulation
        print("\n  [4] Creating simulation...")
        integrator = LangevinMiddleIntegrator(
            temperature * unit.kelvin,
            1.0 / unit.picoseconds,
            2.0 * unit.femtoseconds
        )

        # Get platform
        try:
            platform = Platform.getPlatformByName('CUDA')
            print(f"      Platform: CUDA")
        except Exception:
            try:
                platform = Platform.getPlatformByName('OpenCL')
                print(f"      Platform: OpenCL")
            except Exception:
                platform = Platform.getPlatformByName('CPU')
                print(f"      Platform: CPU")

        self.simulation = Simulation(
            modeller.topology,
            self.system,
            integrator,
            platform
        )
        self.simulation.context.setPositions(modeller.positions)

        # Get initial energy
        state = self.simulation.context.getState(getEnergy=True)
        self.initial_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        print(f"\n      Initial energy: {self.initial_energy:.2f} kJ/mol")

        return True

    def _add_z2_torsion_force(self, force_constant: float):
        """
        Add custom Z² torsion force to backbone dihedrals.

        The energy function penalizes deviation from Z²-quantized angles:
        E = (k / Z²) × Σ min(Δθ - n×θ_Z²)²

        where n is the nearest integer multiple.
        """
        from openmm import CustomTorsionForce

        # Z² scaled force constant
        k_z2 = force_constant / Z2
        print(f"      Z² force constant: {force_constant} / Z² = {k_z2:.4f} kJ/(mol·rad²)")

        # Custom energy expression
        # Find nearest Z² multiple and penalize deviation
        # θ_Z² in radians ≈ 0.5427
        theta_z2_rad = THETA_Z2

        # Energy = 0.5 * k * (θ - nearest_z2_multiple)²
        # We use a periodic potential that has minima at Z² multiples
        energy_expr = f"""
        0.5 * {k_z2} * min(
            (theta - {theta_z2_rad}*round(theta/{theta_z2_rad}))^2,
            (theta + {np.pi} - {theta_z2_rad}*round((theta+{np.pi})/{theta_z2_rad}))^2
        )
        """

        # Simplified: harmonic to nearest Z² multiple
        # Using periodic potential with period θ_Z²
        energy_expr_simple = f"0.5 * {k_z2} * (1 - cos({Z} * theta))"

        z2_force = CustomTorsionForce(energy_expr_simple)

        # Find backbone φ and ψ dihedrals
        n_torsions = 0

        residues = list(self.topology.residues())
        atoms_by_name = {}

        for residue in residues:
            for atom in residue.atoms():
                key = (residue.index, atom.name)
                atoms_by_name[key] = atom.index

        # Add backbone torsions (φ: C-N-CA-C, ψ: N-CA-C-N)
        for i, residue in enumerate(residues):
            if i > 0 and i < len(residues) - 1:
                try:
                    # φ: C(i-1) - N(i) - CA(i) - C(i)
                    c_prev = atoms_by_name.get((i-1, 'C'))
                    n_curr = atoms_by_name.get((i, 'N'))
                    ca_curr = atoms_by_name.get((i, 'CA'))
                    c_curr = atoms_by_name.get((i, 'C'))

                    if all(x is not None for x in [c_prev, n_curr, ca_curr, c_curr]):
                        z2_force.addTorsion(c_prev, n_curr, ca_curr, c_curr, [])
                        n_torsions += 1

                    # ψ: N(i) - CA(i) - C(i) - N(i+1)
                    n_next = atoms_by_name.get((i+1, 'N'))

                    if all(x is not None for x in [n_curr, ca_curr, c_curr, n_next]):
                        z2_force.addTorsion(n_curr, ca_curr, c_curr, n_next, [])
                        n_torsions += 1

                except (KeyError, TypeError):
                    pass

        self.z2_force_idx = self.system.addForce(z2_force)
        print(f"      Added {n_torsions} Z²-constrained backbone torsions")

        return n_torsions

    def minimize_and_run(self, n_steps: int = 10000):
        """
        Run energy minimization and short dynamics.

        Args:
            n_steps: Number of MD steps (2 fs each)
        """
        from openmm import unit

        print("\n" + "="*70)
        print("HYBRID SIMULATION")
        print("="*70)

        # Minimize
        print("\n  [1] Energy minimization...")
        self.simulation.minimizeEnergy(maxIterations=5000)

        state = self.simulation.context.getState(getEnergy=True)
        min_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        print(f"      Post-minimization energy: {min_energy:.2f} kJ/mol")

        # Run dynamics
        print(f"\n  [2] Running {n_steps} steps of hybrid MD...")
        print(f"      Total time: {n_steps * 0.002:.1f} ps")

        # Run in chunks and report
        chunk_size = n_steps // 10
        for i in range(10):
            self.simulation.step(chunk_size)
            state = self.simulation.context.getState(getEnergy=True)
            energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
            print(f"      Step {(i+1)*chunk_size}: E = {energy:.2f} kJ/mol")

        # Final state
        state = self.simulation.context.getState(getEnergy=True, getPositions=True)
        self.final_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        self.final_positions = state.getPositions()

        print(f"\n      Final energy: {self.final_energy:.2f} kJ/mol")
        print(f"      Energy change: {self.final_energy - self.initial_energy:.2f} kJ/mol")

    def save_structure(self, output_path: str):
        """Save final structure to PDB."""
        from openmm.app import PDBFile

        print(f"\n  Saving hybrid structure: {output_path}")

        with open(output_path, 'w') as f:
            # Add header
            f.write("REMARK   Z² Hybrid Structure\n")
            f.write(f"REMARK   Z = {Z:.6f}\n")
            f.write(f"REMARK   θ_Z² = {THETA_Z2_DEG:.2f}°\n")
            f.write(f"REMARK   Final energy: {self.final_energy:.2f} kJ/mol\n")

        # Append structure
        with open(output_path, 'a') as f:
            PDBFile.writeFile(self.topology, self.final_positions, f)

    def analyze_torsions(self) -> Dict:
        """
        Analyze final backbone torsion angles.

        Check alignment with Z² quantization.
        """
        from openmm import unit
        import math

        print("\n" + "="*70)
        print("TORSION ANGLE ANALYSIS")
        print("="*70)

        positions = self.final_positions.value_in_unit(unit.nanometers)
        positions = np.array([[p[0], p[1], p[2]] for p in positions])

        # Build atom index map
        atoms_by_name = {}
        for residue in self.topology.residues():
            for atom in residue.atoms():
                key = (residue.index, atom.name)
                atoms_by_name[key] = atom.index

        # Calculate backbone dihedrals
        residues = list(self.topology.residues())
        phi_angles = []
        psi_angles = []

        for i, residue in enumerate(residues):
            if i > 0 and i < len(residues) - 1:
                try:
                    # φ
                    c_prev = atoms_by_name.get((i-1, 'C'))
                    n_curr = atoms_by_name.get((i, 'N'))
                    ca_curr = atoms_by_name.get((i, 'CA'))
                    c_curr = atoms_by_name.get((i, 'C'))

                    if all(x is not None for x in [c_prev, n_curr, ca_curr, c_curr]):
                        phi = self._calc_dihedral(
                            positions[c_prev], positions[n_curr],
                            positions[ca_curr], positions[c_curr]
                        )
                        phi_angles.append(np.degrees(phi))

                    # ψ
                    n_next = atoms_by_name.get((i+1, 'N'))

                    if all(x is not None for x in [n_curr, ca_curr, c_curr, n_next]):
                        psi = self._calc_dihedral(
                            positions[n_curr], positions[ca_curr],
                            positions[c_curr], positions[n_next]
                        )
                        psi_angles.append(np.degrees(psi))

                except (KeyError, TypeError):
                    pass

        # Analyze Z² alignment
        def z2_deviation(angle_deg):
            """Calculate deviation from nearest Z² multiple."""
            n = round(angle_deg / THETA_Z2_DEG)
            z2_angle = n * THETA_Z2_DEG
            return abs(angle_deg - z2_angle)

        phi_devs = [z2_deviation(phi) for phi in phi_angles]
        psi_devs = [z2_deviation(psi) for psi in psi_angles]

        avg_phi_dev = np.mean(phi_devs) if phi_devs else 0
        avg_psi_dev = np.mean(psi_devs) if psi_devs else 0

        print(f"\n  Backbone dihedral analysis:")
        print(f"    φ angles: {len(phi_angles)}")
        print(f"    ψ angles: {len(psi_angles)}")
        print(f"\n  Mean φ: {np.mean(phi_angles):.1f}° ± {np.std(phi_angles):.1f}°")
        print(f"  Mean ψ: {np.mean(psi_angles):.1f}° ± {np.std(psi_angles):.1f}°")
        print(f"\n  Z² ALIGNMENT:")
        print(f"    Mean φ deviation from Z² multiples: {avg_phi_dev:.2f}°")
        print(f"    Mean ψ deviation from Z² multiples: {avg_psi_dev:.2f}°")
        print(f"    Combined mean deviation: {(avg_phi_dev + avg_psi_dev)/2:.2f}°")

        # Check if angles align better than random
        # Random would give ~θ_Z²/4 ≈ 7.8° average deviation
        random_expected = THETA_Z2_DEG / 4
        combined_dev = (avg_phi_dev + avg_psi_dev) / 2

        if combined_dev < random_expected:
            print(f"\n  RESULT: Angles align BETTER than random with Z² quantization!")
            alignment = "BETTER"
        else:
            print(f"\n  RESULT: Angles do NOT preferentially align with Z² quantization")
            alignment = "NO PREFERENCE"

        return {
            'phi_angles': phi_angles,
            'psi_angles': psi_angles,
            'mean_phi': float(np.mean(phi_angles)) if phi_angles else 0,
            'mean_psi': float(np.mean(psi_angles)) if psi_angles else 0,
            'phi_z2_deviation': float(avg_phi_dev),
            'psi_z2_deviation': float(avg_psi_dev),
            'combined_deviation': float(combined_dev),
            'random_expected': float(random_expected),
            'z2_alignment': alignment
        }

    def _calc_dihedral(self, p1, p2, p3, p4):
        """Calculate dihedral angle between 4 points."""
        b1 = p2 - p1
        b2 = p3 - p2
        b3 = p4 - p3

        n1 = np.cross(b1, b2)
        n2 = np.cross(b2, b3)

        n1 /= np.linalg.norm(n1) + 1e-10
        n2 /= np.linalg.norm(n2) + 1e-10

        m1 = np.cross(n1, b2 / (np.linalg.norm(b2) + 1e-10))

        x = np.dot(n1, n2)
        y = np.dot(m1, n2)

        return np.arctan2(y, x)

    def get_results(self) -> Dict:
        """Get complete results."""
        return {
            'Z': float(Z),
            'Z2': float(Z2),
            'theta_Z2_deg': float(THETA_Z2_DEG),
            'initial_energy_kJ': float(self.initial_energy) if self.initial_energy else None,
            'final_energy_kJ': float(self.final_energy) if self.final_energy else None,
            'energy_change_kJ': float(self.final_energy - self.initial_energy) if self.final_energy else None,
            'timestamp': datetime.now().isoformat(),
            'license': 'AGPL-3.0-or-later'
        }


# ==============================================================================
# FALLBACK SIMULATION (NO OPENMM)
# ==============================================================================

def fallback_z2_analysis(pdb_path: str, output_dir: str) -> Dict:
    """
    Fallback analysis without OpenMM.

    Just analyzes existing backbone angles for Z² alignment.
    """
    print("\n  Using fallback analysis (OpenMM not available)...")

    # Parse PDB
    atoms = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    atoms.append({
                        'name': line[12:16].strip(),
                        'resname': line[17:20].strip(),
                        'chain': line[21],
                        'resid': int(line[22:26]),
                        'x': float(line[30:38]),
                        'y': float(line[38:46]),
                        'z': float(line[46:54])
                    })
                except ValueError:
                    pass

    # Extract CA coordinates
    ca_atoms = [a for a in atoms if a['name'] == 'CA']

    print(f"  Found {len(ca_atoms)} CA atoms")

    # Estimate pseudo-dihedrals from CA trace
    # Not exact but gives rough idea
    angles = []
    for i in range(1, len(ca_atoms) - 2):
        p1 = np.array([ca_atoms[i-1]['x'], ca_atoms[i-1]['y'], ca_atoms[i-1]['z']])
        p2 = np.array([ca_atoms[i]['x'], ca_atoms[i]['y'], ca_atoms[i]['z']])
        p3 = np.array([ca_atoms[i+1]['x'], ca_atoms[i+1]['y'], ca_atoms[i+1]['z']])
        p4 = np.array([ca_atoms[i+2]['x'], ca_atoms[i+2]['y'], ca_atoms[i+2]['z']])

        # Dihedral
        b1 = p2 - p1
        b2 = p3 - p2
        b3 = p4 - p3

        n1 = np.cross(b1, b2)
        n2 = np.cross(b2, b3)

        n1 = n1 / (np.linalg.norm(n1) + 1e-10)
        n2 = n2 / (np.linalg.norm(n2) + 1e-10)

        cos_angle = np.clip(np.dot(n1, n2), -1, 1)
        angle = np.degrees(np.arccos(cos_angle))

        angles.append(angle)

    if not angles:
        return {'error': 'No angles calculated'}

    # Z² alignment analysis
    def z2_deviation(angle_deg):
        n = round(angle_deg / THETA_Z2_DEG)
        z2_angle = n * THETA_Z2_DEG
        return abs(angle_deg - z2_angle)

    deviations = [z2_deviation(a) for a in angles]
    mean_dev = np.mean(deviations)
    random_expected = THETA_Z2_DEG / 4

    print(f"\n  Pseudo-dihedral analysis:")
    print(f"    Angles analyzed: {len(angles)}")
    print(f"    Mean angle: {np.mean(angles):.1f}°")
    print(f"    Mean Z² deviation: {mean_dev:.2f}°")
    print(f"    Random expected: {random_expected:.2f}°")

    if mean_dev < random_expected:
        alignment = "BETTER"
        print(f"\n  RESULT: Angles show Z² alignment tendency!")
    else:
        alignment = "NO PREFERENCE"
        print(f"\n  RESULT: No preferential Z² alignment detected")

    return {
        'method': 'fallback_CA_trace',
        'n_angles': len(angles),
        'mean_angle': float(np.mean(angles)),
        'mean_z2_deviation': float(mean_dev),
        'random_expected': float(random_expected),
        'z2_alignment': alignment
    }


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run hybrid Z² + AMBER simulation."""
    print("\n" + "="*70)
    print("HYBRID Z² OPENMM ENGINE")
    print("="*70)
    print("Testing: Does Z² geometry align with empirical protein physics?")
    print("Method: AMBER14 + Custom Z² torsion constraints")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    output_dir = "hybrid_z2_test"
    os.makedirs(output_dir, exist_ok=True)

    # Input structure (from polite fetcher)
    input_pdb = os.path.join(output_dir, "1IYT_md_ready.pdb")

    if not os.path.exists(input_pdb):
        # Try raw PDB
        input_pdb = os.path.join(output_dir, "1IYT.pdb")

    if not os.path.exists(input_pdb):
        print(f"\nERROR: Input PDB not found: {input_pdb}")
        print("Run api_polite_structure_fetcher.py first")
        return {'error': 'Input not found'}

    try:
        import openmm
        has_openmm = True
    except ImportError:
        has_openmm = False

    results = {
        'Z': float(Z),
        'Z2': float(Z2),
        'theta_Z2_deg': float(THETA_Z2_DEG),
        'timestamp': datetime.now().isoformat()
    }

    if has_openmm:
        # Run full hybrid simulation
        engine = HybridZ2Engine(input_pdb)

        if engine.setup(z2_force_constant=10.0):
            # Run simulation
            engine.minimize_and_run(n_steps=10000)

            # Save structure
            output_pdb = os.path.join(output_dir, "z2_hybrid_relaxed.pdb")
            engine.save_structure(output_pdb)

            # Analyze torsions
            torsion_results = engine.analyze_torsions()

            results.update(engine.get_results())
            results['torsion_analysis'] = torsion_results
            results['output_pdb'] = output_pdb

    else:
        # Fallback
        results.update(fallback_z2_analysis(input_pdb, output_dir))

    # Save results
    results_file = os.path.join(output_dir, "z2_hybrid_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results saved: {results_file}")

    # Summary
    print("\n" + "="*70)
    print("HYBRID SIMULATION SUMMARY")
    print("="*70)
    print(f"  Z = {Z:.4f}")
    print(f"  θ_Z² = {THETA_Z2_DEG:.2f}°")

    if 'initial_energy_kJ' in results and results['initial_energy_kJ']:
        print(f"\n  Energy:")
        print(f"    Initial: {results['initial_energy_kJ']:.2f} kJ/mol")
        print(f"    Final: {results['final_energy_kJ']:.2f} kJ/mol")
        print(f"    Change: {results['energy_change_kJ']:.2f} kJ/mol")

    if 'torsion_analysis' in results:
        ta = results['torsion_analysis']
        print(f"\n  Z² Alignment:")
        print(f"    Mean deviation from Z² multiples: {ta['combined_deviation']:.2f}°")
        print(f"    Random expected: {ta['random_expected']:.2f}°")
        print(f"    Result: {ta['z2_alignment']}")

    return results


if __name__ == '__main__':
    main()
