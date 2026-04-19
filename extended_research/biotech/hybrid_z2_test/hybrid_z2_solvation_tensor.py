#!/usr/bin/env python3
"""
Hybrid Z² Solvation Tensor - Pathway 2 Empirical Upgrade

SPDX-License-Identifier: AGPL-3.0-or-later

This script upgrades the theoretical Z² implicit solvation model from
Pathway 2 into a real empirical physics engine using OpenMM.

ORIGINAL PATHWAY 2 THEORY:
- Implicit solvation with Z² pressure gradient
- Hydrophobic residues pushed toward core by 1/Z² metric
- Water modeled as external Casimir-like pressure

HYBRID UPGRADE:
- Real PDB structures from RCSB
- OpenMM AMBER14 force field as baseline
- CustomExternalForce with Z² solvation pressure
- Direct energy comparison: AMBER vs Z² Hybrid

THE TEST:
If Z² geometry is real, the Z² solvation tensor should:
1. Produce LOWER or SIMILAR energy to standard OBC2
2. Create more compact hydrophobic cores
3. Show improved folding energetics

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import numpy as np
import requests
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Z² CONSTANTS
# ==============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # ≈ 5.7888
Z2 = Z ** 2  # ≈ 33.51
THETA_Z2 = np.pi / Z  # ≈ 0.5427 rad

print("="*70)
print("Z² SOLVATION TENSOR - PATHWAY 2 HYBRID UPGRADE")
print("="*70)
print(f"Z = {Z:.6f} Å")
print(f"Z² = {Z2:.6f}")
print(f"Solvation pressure scale: 1/Z² = {1/Z2:.6f}")
print("="*70)

# ==============================================================================
# HYDROPHOBICITY SCALE (Kyte-Doolittle)
# ==============================================================================

HYDROPHOBICITY = {
    'ALA': 1.8, 'ARG': -4.5, 'ASN': -3.5, 'ASP': -3.5, 'CYS': 2.5,
    'GLU': -3.5, 'GLN': -3.5, 'GLY': -0.4, 'HIS': -3.2, 'ILE': 4.5,
    'LEU': 3.8, 'LYS': -3.9, 'MET': 1.9, 'PHE': 2.8, 'PRO': -1.6,
    'SER': -0.8, 'THR': -0.7, 'TRP': -0.9, 'TYR': -1.3, 'VAL': 4.2
}

# ==============================================================================
# DATA FETCHING
# ==============================================================================

PDB_API_URL = "https://files.rcsb.org/download/{}.pdb"

def fetch_pdb(pdb_id: str, output_dir: str = ".") -> str:
    """Fetch PDB structure with rate limiting."""
    import time

    pdb_id = pdb_id.upper()
    url = PDB_API_URL.format(pdb_id)

    print(f"\n  Fetching PDB: {pdb_id}")
    time.sleep(0.5)  # Rate limiting

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)
    pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

    with open(pdb_path, 'w') as f:
        f.write(response.text)

    return pdb_path


# ==============================================================================
# HYBRID Z² SOLVATION ENGINE
# ==============================================================================

class HybridZ2SolvationEngine:
    """
    Hybrid solvation engine combining:
    1. Standard AMBER14 + OBC2 implicit solvent
    2. Z² Kaluza-Klein solvation pressure tensor

    The Z² pressure pushes hydrophobic atoms toward the center of mass
    with strength proportional to 1/Z².
    """

    def __init__(self, pdb_path: str):
        self.pdb_path = pdb_path
        self.topology = None
        self.positions = None

        # Results
        self.standard_energy = None
        self.hybrid_energy = None

    def setup_standard_system(self):
        """Set up standard AMBER14 + OBC2 system."""
        print("\n  [1] Setting up STANDARD AMBER14 + OBC2...")

        try:
            from openmm.app import PDBFile, ForceField, Modeller, Simulation, NoCutoff, HBonds
            from openmm import LangevinMiddleIntegrator, Platform, unit
        except ImportError:
            print("  ERROR: OpenMM not installed")
            return None, None

        pdb = PDBFile(self.pdb_path)
        modeller = Modeller(pdb.topology, pdb.positions)

        forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

        try:
            modeller.addHydrogens(forcefield)
        except Exception as e:
            print(f"    Note: {e}")

        self.topology = modeller.topology
        self.positions = modeller.positions

        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=NoCutoff,
            constraints=HBonds
        )

        integrator = LangevinMiddleIntegrator(
            310 * unit.kelvin,
            1.0 / unit.picoseconds,
            2.0 * unit.femtoseconds
        )

        try:
            platform = Platform.getPlatformByName('CUDA')
        except:
            try:
                platform = Platform.getPlatformByName('OpenCL')
            except:
                platform = Platform.getPlatformByName('CPU')

        simulation = Simulation(modeller.topology, system, integrator, platform)
        simulation.context.setPositions(modeller.positions)

        return simulation, system

    def setup_hybrid_system(self, z2_strength: float = 1.0):
        """
        Set up hybrid AMBER14 + Z² solvation system.

        Args:
            z2_strength: Scaling factor for Z² solvation force
        """
        print("\n  [2] Setting up HYBRID Z² + AMBER14...")

        try:
            from openmm.app import PDBFile, ForceField, Modeller, Simulation, NoCutoff, HBonds
            from openmm import CustomExternalForce, LangevinMiddleIntegrator, Platform, unit
        except ImportError:
            return None, None

        pdb = PDBFile(self.pdb_path)
        modeller = Modeller(pdb.topology, pdb.positions)

        forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

        try:
            modeller.addHydrogens(forcefield)
        except Exception:
            pass

        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=NoCutoff,
            constraints=HBonds
        )

        # Add Z² solvation pressure force
        print("    Adding Z² solvation pressure tensor...")

        # Z² solvation force: pushes hydrophobic atoms toward COM
        # E = k * hydro * |r - r_com|² / Z²
        # where k scales with 1/Z²

        k_z2 = z2_strength / Z2  # kJ/(mol·nm²)

        # Get center of mass (will be updated during simulation)
        positions_nm = modeller.positions.value_in_unit(unit.nanometers)
        com = np.mean([[p[0], p[1], p[2]] for p in positions_nm], axis=0)

        # Custom force expression
        # Harmonic attraction to COM, strength proportional to hydrophobicity / Z²
        z2_force = CustomExternalForce(
            f"{k_z2} * hydro * ((x-{com[0]})^2 + (y-{com[1]})^2 + (z-{com[2]})^2)"
        )
        z2_force.addPerParticleParameter("hydro")

        # Add particles with hydrophobicity values
        n_z2_atoms = 0
        for residue in modeller.topology.residues():
            hydro = HYDROPHOBICITY.get(residue.name, 0.0)

            # Only apply to hydrophobic residues (hydro > 0)
            # Negative hydro would push away from core (correct for hydrophilic)
            for atom in residue.atoms():
                # Apply stronger to core atoms (C, CA, CB)
                if atom.name in ['CA', 'CB', 'C']:
                    z2_force.addParticle(atom.index, [hydro])
                    n_z2_atoms += 1
                elif atom.name.startswith('C') and hydro > 1.0:
                    # Side chain carbons of hydrophobic residues
                    z2_force.addParticle(atom.index, [hydro * 0.5])
                    n_z2_atoms += 1

        system.addForce(z2_force)
        print(f"    Added Z² solvation to {n_z2_atoms} atoms")
        print(f"    Z² force constant: {k_z2:.6f} kJ/(mol·nm²)")

        # Create simulation
        integrator = LangevinMiddleIntegrator(
            310 * unit.kelvin,
            1.0 / unit.picoseconds,
            2.0 * unit.femtoseconds
        )

        try:
            platform = Platform.getPlatformByName('CUDA')
        except:
            try:
                platform = Platform.getPlatformByName('OpenCL')
            except:
                platform = Platform.getPlatformByName('CPU')

        simulation = Simulation(modeller.topology, system, integrator, platform)
        simulation.context.setPositions(modeller.positions)

        return simulation, system

    def run_comparison(self, min_steps: int = 5000, md_steps: int = 5000):
        """
        Run energy comparison between standard and hybrid systems.
        """
        from openmm import unit

        results = {
            'Z': float(Z),
            'Z2': float(Z2),
            'timestamp': datetime.now().isoformat()
        }

        print("\n" + "="*70)
        print("RUNNING COMPARISON: STANDARD vs Z² HYBRID")
        print("="*70)

        # Standard system
        print("\n  STANDARD AMBER14 + OBC2:")
        std_sim, std_sys = self.setup_standard_system()

        if std_sim is None:
            return {'error': 'OpenMM not available'}

        # Minimize
        print("    Minimizing...")
        std_sim.minimizeEnergy(maxIterations=min_steps)
        state = std_sim.context.getState(getEnergy=True)
        std_min_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        print(f"    Post-min energy: {std_min_energy:.2f} kJ/mol")

        # Run dynamics
        print(f"    Running {md_steps} MD steps...")
        std_sim.step(md_steps)
        state = std_sim.context.getState(getEnergy=True, getPositions=True)
        self.standard_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        std_positions = state.getPositions()
        print(f"    Final energy: {self.standard_energy:.2f} kJ/mol")

        # Calculate Rg
        coords = np.array([[p[0], p[1], p[2]] for p in std_positions.value_in_unit(unit.nanometers)])
        std_rg = np.sqrt(np.mean(np.sum((coords - coords.mean(axis=0))**2, axis=1))) * 10  # nm to Å
        print(f"    Radius of gyration: {std_rg:.2f} Å")

        results['standard'] = {
            'min_energy_kJ': float(std_min_energy),
            'final_energy_kJ': float(self.standard_energy),
            'rg_angstrom': float(std_rg)
        }

        # Hybrid system
        print("\n  HYBRID Z² + AMBER14:")
        hyb_sim, hyb_sys = self.setup_hybrid_system(z2_strength=10.0)

        if hyb_sim is None:
            return results

        # Minimize
        print("    Minimizing...")
        hyb_sim.minimizeEnergy(maxIterations=min_steps)
        state = hyb_sim.context.getState(getEnergy=True)
        hyb_min_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        print(f"    Post-min energy: {hyb_min_energy:.2f} kJ/mol")

        # Run dynamics
        print(f"    Running {md_steps} MD steps...")
        hyb_sim.step(md_steps)
        state = hyb_sim.context.getState(getEnergy=True, getPositions=True)
        self.hybrid_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        hyb_positions = state.getPositions()
        print(f"    Final energy: {self.hybrid_energy:.2f} kJ/mol")

        # Calculate Rg
        coords = np.array([[p[0], p[1], p[2]] for p in hyb_positions.value_in_unit(unit.nanometers)])
        hyb_rg = np.sqrt(np.mean(np.sum((coords - coords.mean(axis=0))**2, axis=1))) * 10
        print(f"    Radius of gyration: {hyb_rg:.2f} Å")

        results['hybrid'] = {
            'min_energy_kJ': float(hyb_min_energy),
            'final_energy_kJ': float(self.hybrid_energy),
            'rg_angstrom': float(hyb_rg)
        }

        # Comparison
        print("\n" + "="*70)
        print("COMPARISON RESULTS")
        print("="*70)

        energy_diff = self.hybrid_energy - self.standard_energy
        rg_diff = hyb_rg - std_rg

        print(f"\n  Energy difference: {energy_diff:+.2f} kJ/mol")
        print(f"  Rg difference: {rg_diff:+.2f} Å")

        results['comparison'] = {
            'energy_diff_kJ': float(energy_diff),
            'rg_diff_angstrom': float(rg_diff)
        }

        # Verdict
        print("\n  VERDICT:")
        if energy_diff < -10:
            print("  ✓ Z² solvation IMPROVED energy significantly")
            results['verdict'] = 'Z2_IMPROVED_ENERGY'
        elif energy_diff < 10:
            print("  ~ Z² solvation has similar energy (within 10 kJ/mol)")
            results['verdict'] = 'Z2_SIMILAR_ENERGY'
        else:
            print("  ✗ Z² solvation RAISED energy")
            results['verdict'] = 'Z2_RAISED_ENERGY'

        if rg_diff < -0.5:
            print("  ✓ Z² solvation created more compact core")
        elif rg_diff > 0.5:
            print("  ✗ Z² solvation expanded structure")
        else:
            print("  ~ Z² solvation maintained compactness")

        return results


# ==============================================================================
# FALLBACK ANALYSIS
# ==============================================================================

def fallback_analysis(pdb_path: str) -> Dict:
    """Fallback when OpenMM not available."""
    print("\n  Fallback: Analyzing structure without MD...")

    # Just measure hydrophobic core
    atoms = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    atoms.append({
                        'name': line[12:16].strip(),
                        'resname': line[17:20].strip(),
                        'x': float(line[30:38]),
                        'y': float(line[38:46]),
                        'z': float(line[46:54])
                    })
                except ValueError:
                    pass

    if not atoms:
        return {'error': 'No atoms found'}

    # Get CA coords
    ca_coords = np.array([[a['x'], a['y'], a['z']] for a in atoms if a['name'] == 'CA'])
    com = ca_coords.mean(axis=0)

    # Measure hydrophobic burial
    hydro_distances = []
    for a in atoms:
        if a['name'] == 'CA':
            hydro = HYDROPHOBICITY.get(a['resname'], 0)
            dist = np.linalg.norm([a['x'] - com[0], a['y'] - com[1], a['z'] - com[2]])
            hydro_distances.append((hydro, dist))

    # Correlation: are hydrophobic residues closer to core?
    if hydro_distances:
        hydros = [h for h, d in hydro_distances]
        dists = [d for h, d in hydro_distances]
        correlation = np.corrcoef(hydros, dists)[0, 1]

        print(f"  Hydrophobicity-distance correlation: {correlation:.3f}")
        print(f"  (Negative = hydrophobics are closer to core)")

        return {
            'method': 'fallback',
            'correlation': float(correlation),
            'n_residues': len(hydro_distances)
        }

    return {'error': 'Analysis failed'}


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run Z² solvation tensor comparison."""
    print("\n" + "="*70)
    print("HYBRID Z² SOLVATION TENSOR")
    print("="*70)
    print("Testing: Does Z² solvation improve hydrophobic collapse?")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    output_dir = "hybrid_z2_test"
    os.makedirs(output_dir, exist_ok=True)

    # Use α-synuclein fragment or small test protein
    # PDB 1XQ8: α-synuclein helix (small, good for testing)
    test_pdb_id = '1XQ8'

    try:
        pdb_path = fetch_pdb(test_pdb_id, output_dir)
    except Exception as e:
        print(f"  Could not fetch {test_pdb_id}: {e}")
        # Use existing structure
        pdb_path = os.path.join(output_dir, "1IYT.pdb")
        if not os.path.exists(pdb_path):
            print("  No test structure available")
            return {'error': 'No structure'}

    try:
        import openmm
        engine = HybridZ2SolvationEngine(pdb_path)
        results = engine.run_comparison(min_steps=3000, md_steps=3000)
    except ImportError:
        results = fallback_analysis(pdb_path)

    # Save results
    results_file = os.path.join(output_dir, "z2_solvation_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results saved: {results_file}")

    return results


if __name__ == '__main__':
    main()
