#!/usr/bin/env python3
"""
Empirical OpenMM Thermodynamic Relaxation Engine

SPDX-License-Identifier: AGPL-3.0-or-later

This script uses OpenMM with AMBER14 force fields to relax predicted protein
structures into their true thermodynamic ground states.

Key Features:
- AMBER14 force field (peer-reviewed empirical parameters)
- TIP3P-FB explicit water or OBC2 implicit solvent
- L-BFGS energy minimization
- NVT equilibration at physiological temperature (310K / 37°C)
- Real PDB structure fetching from RCSB
- Proper hydrogen atom placement

Physics:
- Coulomb electrostatics with PME
- Lennard-Jones van der Waals
- Harmonic bond/angle potentials
- Periodic dihedral potentials

References:
- Maier et al. (2015) JCTC: AMBER ff14SB
- Eastman et al. (2017) PLoS Comp Bio: OpenMM

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import requests
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# REAL DATA SOURCES
# ==============================================================================

PDB_API_URL = "https://files.rcsb.org/download/{}.pdb"
UNIPROT_API_URL = "https://rest.uniprot.org/uniprotkb/{}.fasta"

# ==============================================================================
# DATA FETCHING
# ==============================================================================

def fetch_pdb_structure(pdb_id: str, output_dir: str = ".") -> str:
    """
    Fetch real PDB structure from RCSB Protein Data Bank.

    Args:
        pdb_id: 4-letter PDB ID (e.g., "1UBQ", "1AKI")
        output_dir: Directory to save PDB file

    Returns:
        Path to downloaded PDB file
    """
    pdb_id = pdb_id.upper()
    url = PDB_API_URL.format(pdb_id)

    print(f"  Fetching PDB structure: {pdb_id}")
    print(f"  URL: {url}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        pdb_content = response.text

        os.makedirs(output_dir, exist_ok=True)
        pdb_path = os.path.join(output_dir, f"{pdb_id}.pdb")

        with open(pdb_path, 'w') as f:
            f.write(pdb_content)

        print(f"  Downloaded: {pdb_path}")
        return pdb_path

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch PDB {pdb_id}: {e}")


def fetch_uniprot_sequence(uniprot_id: str) -> str:
    """
    Fetch protein sequence from UniProt.

    Args:
        uniprot_id: UniProt accession (e.g., "P0A9Q1")

    Returns:
        FASTA sequence string
    """
    url = UNIPROT_API_URL.format(uniprot_id)

    print(f"  Fetching UniProt sequence: {uniprot_id}")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch UniProt {uniprot_id}: {e}")


# ==============================================================================
# OPENMM RELAXATION ENGINE
# ==============================================================================

class OpenMMRelaxationEngine:
    """
    Thermodynamic relaxation using OpenMM and AMBER force fields.

    Performs:
    1. Hydrogen addition
    2. Solvation (explicit or implicit)
    3. Energy minimization
    4. NVT equilibration
    """

    def __init__(self, pdb_path: str, use_explicit_water: bool = False):
        """
        Initialize relaxation engine.

        Args:
            pdb_path: Path to input PDB file
            use_explicit_water: Use TIP3P-FB (True) or OBC2 implicit (False)
        """
        self.pdb_path = pdb_path
        self.use_explicit_water = use_explicit_water
        self.simulation = None
        self.topology = None
        self.positions = None
        self.energy_history = []

    def setup(self):
        """Set up the simulation system."""
        print("\n  [1] Setting up simulation...")

        try:
            from openmm.app import (
                PDBFile, ForceField, Modeller, Simulation,
                PME, NoCutoff, HBonds, DCDReporter, StateDataReporter
            )
            from openmm import (
                LangevinMiddleIntegrator, Platform, unit
            )
        except ImportError:
            print("\n  ERROR: OpenMM not installed")
            print("  Install with: conda install -c conda-forge openmm")
            return False

        # Load PDB
        print("  Loading PDB structure...")
        pdb = PDBFile(self.pdb_path)
        self.topology = pdb.topology
        self.positions = pdb.positions

        # Create modeller for adding hydrogens
        modeller = Modeller(pdb.topology, pdb.positions)

        # Load AMBER14 force field
        print("  Loading AMBER14 force field...")

        if self.use_explicit_water:
            # Explicit water with TIP3P-FB
            forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

            # Add hydrogens
            print("  Adding hydrogens...")
            modeller.addHydrogens(forcefield)

            # Add water box (10 Å padding)
            print("  Building water box (10 Å padding)...")
            modeller.addSolvent(
                forcefield,
                model='tip3p',
                padding=1.0 * unit.nanometers
            )

            self.topology = modeller.topology
            self.positions = modeller.positions

            # Create system
            print("  Creating simulation system...")
            system = forcefield.createSystem(
                modeller.topology,
                nonbondedMethod=PME,
                nonbondedCutoff=1.0 * unit.nanometers,
                constraints=HBonds
            )

        else:
            # Implicit solvent with OBC2
            forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

            # Add hydrogens
            print("  Adding hydrogens...")
            modeller.addHydrogens(forcefield)

            self.topology = modeller.topology
            self.positions = modeller.positions

            # Create system
            print("  Creating simulation system (implicit OBC2 solvent)...")
            system = forcefield.createSystem(
                modeller.topology,
                nonbondedMethod=NoCutoff,
                constraints=HBonds
            )

        # Create integrator (Langevin at 310K = 37°C)
        temperature = 310 * unit.kelvin
        friction = 1.0 / unit.picoseconds
        timestep = 2.0 * unit.femtoseconds

        integrator = LangevinMiddleIntegrator(temperature, friction, timestep)

        # Get best platform
        try:
            platform = Platform.getPlatformByName('CUDA')
            print("  Using CUDA platform (GPU)")
        except Exception:
            try:
                platform = Platform.getPlatformByName('OpenCL')
                print("  Using OpenCL platform")
            except Exception:
                platform = Platform.getPlatformByName('CPU')
                print("  Using CPU platform")

        # Create simulation
        self.simulation = Simulation(
            modeller.topology,
            system,
            integrator,
            platform
        )
        self.simulation.context.setPositions(modeller.positions)

        print(f"  System contains {system.getNumParticles()} atoms")

        return True

    def minimize_energy(self, max_iterations: int = 50000, tolerance: float = 10.0):
        """
        Run L-BFGS energy minimization.

        Args:
            max_iterations: Maximum minimization steps
            tolerance: Energy tolerance (kJ/mol/nm)
        """
        from openmm import unit

        print(f"\n  [2] Running energy minimization...")
        print(f"      Max iterations: {max_iterations}")
        print(f"      Tolerance: {tolerance} kJ/mol/nm")

        # Get initial energy
        state = self.simulation.context.getState(getEnergy=True)
        initial_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        print(f"      Initial energy: {initial_energy:.2f} kJ/mol")

        self.energy_history = [initial_energy]

        # Run minimization
        self.simulation.minimizeEnergy(
            maxIterations=max_iterations,
            tolerance=tolerance * unit.kilojoules_per_mole / unit.nanometers
        )

        # Get final energy
        state = self.simulation.context.getState(getEnergy=True, getPositions=True)
        final_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
        self.positions = state.getPositions()

        self.energy_history.append(final_energy)

        print(f"      Final energy: {final_energy:.2f} kJ/mol")
        print(f"      Energy change: {final_energy - initial_energy:.2f} kJ/mol")

        return final_energy

    def equilibrate(self, n_steps: int = 10000, report_interval: int = 1000):
        """
        Run NVT equilibration at 310K (37°C).

        Args:
            n_steps: Number of MD steps (2 fs each)
            report_interval: Interval for energy reporting
        """
        from openmm import unit

        print(f"\n  [3] Running NVT equilibration at 310K...")
        print(f"      Steps: {n_steps} (= {n_steps * 0.002:.1f} ps)")
        print(f"      Temperature: 310 K (37°C)")

        # Run equilibration
        for i in range(n_steps // report_interval):
            self.simulation.step(report_interval)

            state = self.simulation.context.getState(getEnergy=True, getPositions=True)
            energy = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
            self.energy_history.append(energy)

            if (i + 1) % 5 == 0:
                print(f"      Step {(i+1)*report_interval}: E = {energy:.2f} kJ/mol")

        # Get final state
        state = self.simulation.context.getState(getPositions=True)
        self.positions = state.getPositions()

        print(f"      Equilibration complete")

    def save_structure(self, output_path: str):
        """Save relaxed structure to PDB."""
        from openmm.app import PDBFile

        print(f"\n  Saving relaxed structure: {output_path}")

        with open(output_path, 'w') as f:
            PDBFile.writeFile(
                self.topology,
                self.positions,
                f
            )

    def save_energy_plot(self, output_path: str, name: str = "protein"):
        """Save energy descent plot."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.plot(self.energy_history, 'b-', linewidth=1.5)
            ax.axhline(y=self.energy_history[-1], color='r', linestyle='--',
                      label=f'Final: {self.energy_history[-1]:.1f} kJ/mol')

            ax.set_xlabel('Step')
            ax.set_ylabel('Potential Energy (kJ/mol)')
            ax.set_title(f'{name} - Thermodynamic Relaxation')
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(output_path, dpi=150)
            plt.close()

            print(f"  Energy plot saved: {output_path}")

        except ImportError:
            print("  WARNING: matplotlib not available")


# ==============================================================================
# FALLBACK RELAXATION (NO OPENMM)
# ==============================================================================

def fallback_relaxation(pdb_path: str, output_dir: str, name: str) -> Dict:
    """
    Fallback relaxation without OpenMM.

    Uses simple gradient descent on a pseudo-energy function.
    """
    print("\n  Using fallback relaxation (OpenMM not available)...")

    # Read coordinates
    coords = []
    atoms = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
                    atoms.append(line[:30])
                except ValueError:
                    pass

    if not coords:
        raise ValueError("No atoms found in PDB file")

    coords = np.array(coords)
    n_atoms = len(coords)

    print(f"  Loaded {n_atoms} atoms")

    # Simple energy minimization
    energy_history = []

    for step in range(100):
        forces = np.zeros_like(coords)

        # Pseudo-Lennard-Jones
        for i in range(n_atoms):
            for j in range(i + 1, n_atoms):
                r = coords[j] - coords[i]
                d = np.linalg.norm(r) + 1e-8
                r_hat = r / d

                # Repulsive at close range
                if d < 2.5:
                    f = -10 * (2.5 - d)
                    forces[i] += f * r_hat
                    forces[j] -= f * r_hat

        # Bond constraints (sequential atoms)
        for i in range(n_atoms - 1):
            r = coords[i+1] - coords[i]
            d = np.linalg.norm(r)
            if d < 100:  # Only if reasonably connected
                r_hat = r / (d + 1e-8)
                f = (d - 3.8) * r_hat
                forces[i] += f
                forces[i+1] -= f

        # Update
        coords += 0.01 * forces
        coords -= coords.mean(axis=0)

        # Compute pseudo-energy
        energy = np.sum(forces**2)
        energy_history.append(energy)

    # Save relaxed structure
    output_path = os.path.join(output_dir, f"{name}_relaxed.pdb")

    with open(output_path, 'w') as f:
        f.write("REMARK   Fallback relaxation (no OpenMM)\n")
        for i, (atom_line, coord) in enumerate(zip(atoms, coords)):
            x, y, z = coord
            f.write(f"{atom_line}{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00\n")
        f.write("END\n")

    print(f"  Saved: {output_path}")

    return {
        'output_pdb': output_path,
        'energy_history': energy_history,
        'method': 'Fallback gradient descent'
    }


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def relax_structure(
    pdb_source: str,
    name: str = "protein",
    output_dir: str = "relaxed_structures",
    use_explicit_water: bool = False,
    min_steps: int = 50000,
    equil_steps: int = 10000
) -> Dict:
    """
    Main relaxation pipeline.

    Args:
        pdb_source: PDB file path OR 4-letter PDB ID to fetch
        name: Protein name
        output_dir: Output directory
        use_explicit_water: Use explicit water (slower, more accurate)
        min_steps: Minimization steps
        equil_steps: Equilibration steps

    Returns:
        Dictionary with relaxation results
    """
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "="*70)
    print("OPENMM THERMODYNAMIC RELAXATION")
    print("="*70)
    print(f"Protein: {name}")
    print(f"Force Field: AMBER14")
    print(f"Solvent: {'TIP3P-FB (explicit)' if use_explicit_water else 'OBC2 (implicit)'}")
    print("="*70)

    # Get PDB file
    if len(pdb_source) == 4 and pdb_source.isalnum():
        # Looks like a PDB ID - fetch from RCSB
        pdb_path = fetch_pdb_structure(pdb_source, output_dir)
    else:
        # Local file path
        pdb_path = pdb_source
        if not os.path.exists(pdb_path):
            raise FileNotFoundError(f"PDB file not found: {pdb_path}")

    # Try OpenMM, fall back if not available
    try:
        import openmm
        has_openmm = True
    except ImportError:
        has_openmm = False

    if has_openmm:
        engine = OpenMMRelaxationEngine(pdb_path, use_explicit_water)

        if not engine.setup():
            return fallback_relaxation(pdb_path, output_dir, name)

        # Minimize
        final_energy = engine.minimize_energy(max_iterations=min_steps)

        # Equilibrate
        engine.equilibrate(n_steps=equil_steps)

        # Save outputs
        output_pdb = os.path.join(output_dir, f"{name}_relaxed.pdb")
        engine.save_structure(output_pdb)

        plot_path = os.path.join(output_dir, f"{name}_energy.png")
        engine.save_energy_plot(plot_path, name)

        return {
            'name': name,
            'input_pdb': pdb_path,
            'output_pdb': output_pdb,
            'energy_plot': plot_path,
            'final_energy_kj': final_energy,
            'energy_history': engine.energy_history,
            'method': 'OpenMM AMBER14',
            'solvent': 'TIP3P-FB' if use_explicit_water else 'OBC2 implicit',
            'timestamp': datetime.now().isoformat()
        }

    else:
        return fallback_relaxation(pdb_path, output_dir, name)


# ==============================================================================
# TEST STRUCTURES (REAL PDB IDs)
# ==============================================================================

REAL_PDB_IDS = {
    'ubiquitin': '1UBQ',      # Human ubiquitin (76 residues)
    'lysozyme': '1AKI',       # Hen egg-white lysozyme (129 residues)
    'insulin': '4INS',        # Porcine insulin (51 residues)
    'myoglobin': '1MBN',      # Sperm whale myoglobin (153 residues)
    'chymotrypsin': '1CGI',   # Bovine chymotrypsin inhibitor
    'gb1': '1PGB',            # Protein G B1 domain
    'villin': '1VII'          # Villin headpiece (35 residues)
}


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Run relaxation on real PDB structures."""
    print("\n" + "="*70)
    print("EMPIRICAL OPENMM RELAXATION PIPELINE")
    print("="*70)
    print("Force Field: AMBER14 (peer-reviewed empirical parameters)")
    print("Data Source: RCSB Protein Data Bank")
    print("License: AGPL-3.0-or-later")
    print("="*70)

    output_dir = "openmm_relaxed"

    # Test with ubiquitin (small, fast)
    test_id = 'ubiquitin'
    pdb_id = REAL_PDB_IDS[test_id]

    print(f"\nTesting with {test_id} (PDB: {pdb_id})")

    try:
        result = relax_structure(
            pdb_id,
            name=test_id,
            output_dir=output_dir,
            use_explicit_water=False,  # Implicit for speed
            min_steps=10000,
            equil_steps=5000
        )

        print("\n" + "="*70)
        print("RESULTS")
        print("="*70)
        print(f"  Input: {result.get('input_pdb', 'N/A')}")
        print(f"  Output: {result.get('output_pdb', 'N/A')}")
        print(f"  Method: {result.get('method', 'N/A')}")
        print(f"  Final Energy: {result.get('final_energy_kj', 'N/A'):.2f} kJ/mol")

        # Save metadata
        meta_path = os.path.join(output_dir, f"{test_id}_relaxation.json")
        with open(meta_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"  Metadata: {meta_path}")

        return result

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTo install OpenMM:")
        print("  conda install -c conda-forge openmm")
        return {'error': str(e)}


if __name__ == '__main__':
    main()
