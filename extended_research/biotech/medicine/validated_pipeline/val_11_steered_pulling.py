#!/usr/bin/env python3
"""
val_11_steered_pulling.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

val_11_steered_pulling.py - Steered Molecular Dynamics (SMD) Pulling Engine

Generates umbrella sampling windows by pulling peptide away from receptor
using a harmonic spring attached to a moving reference point.

This is the precursor to WHAM analysis for absolute binding free energy (ΔG).

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "smd_pulling"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("STEERED MOLECULAR DYNAMICS (SMD) PULLING ENGINE")
print("Umbrella Sampling Window Generator")
print("=" * 80)
print()

# =============================================================================
# SMD PARAMETERS
# =============================================================================

# Pulling parameters
PULL_VELOCITY = 0.001  # nm/ps = 1 Å/ns (slow, quasi-equilibrium)
SPRING_CONSTANT = 1000.0  # kJ/mol/nm² (stiff spring)
PULL_DISTANCE = 2.0  # nm = 20 Å total pull distance
WINDOW_SPACING = 0.1  # nm = 1 Å between windows

# Simulation parameters
TEMPERATURE = 310  # K
TIMESTEP_FS = 2.0
STEPS_PER_WINDOW = 5000  # Steps before saving each window

# Calculate total windows
N_WINDOWS = int(PULL_DISTANCE / WINDOW_SPACING) + 1
print(f"Pull configuration:")
print(f"  Pull distance: {PULL_DISTANCE} nm ({PULL_DISTANCE * 10:.0f} Å)")
print(f"  Window spacing: {WINDOW_SPACING} nm ({WINDOW_SPACING * 10:.1f} Å)")
print(f"  Total windows: {N_WINDOWS}")
print(f"  Pull velocity: {PULL_VELOCITY} nm/ps")
print(f"  Spring constant: {SPRING_CONSTANT} kJ/mol/nm²")
print()

# =============================================================================
# TEST SYSTEMS (peptide-receptor complexes)
# =============================================================================

# For now, we'll demonstrate with isolated peptides
# Real implementation requires pre-docked peptide-receptor complexes
TEST_SYSTEMS = {
    "ZIM-SYN-004_ASYN": {
        "peptide": "FPF",
        "receptor": "Alpha-synuclein",
        "complex_pdb": None,  # Will need docked structure
        "pull_vector": [0, 0, 1],  # Pull along Z-axis
    },
    "ZIM-ADD-003_nAChR": {
        "peptide": "RWWFWR",
        "receptor": "α3β4 nAChR",
        "complex_pdb": None,
        "pull_vector": [0, 0, 1],
    },
}


# =============================================================================
# SMD FORCE IMPLEMENTATION
# =============================================================================

def create_smd_system(peptide_indices: List[int], receptor_indices: List[int],
                      pull_vector: np.ndarray, system) -> 'System':
    """
    Add SMD pulling force to an OpenMM system.

    The force acts on the center of mass of the peptide, pulling it
    along the specified vector relative to the receptor.

    Physics:
    F = k * (r - r0(t))
    where r0(t) = r0_initial + v * t

    We implement this as a CustomCentroidBondForce.
    """
    from openmm import CustomCentroidBondForce, CustomExternalForce

    # Normalize pull vector
    pull_vector = np.array(pull_vector, dtype=float)
    pull_vector = pull_vector / np.linalg.norm(pull_vector)

    # Create centroid-based pulling force
    # This creates a "spring" between peptide COM and a moving reference point

    # Energy = 0.5 * k * (distance - target)²
    # where distance = projection of (peptide_COM - receptor_COM) onto pull vector
    # and target increases with time

    # For umbrella sampling, we use a simpler approach:
    # Apply a harmonic restraint to the peptide COM at increasing distances

    smd_force = CustomCentroidBondForce(2, "0.5*k*(distance(g1,g2) - r0)^2")
    smd_force.addPerBondParameter("k")
    smd_force.addPerBondParameter("r0")

    # Group 1: Peptide atoms
    smd_force.addGroup(peptide_indices)

    # Group 2: Receptor atoms (anchor)
    smd_force.addGroup(receptor_indices)

    # Initial restraint (will be updated during pulling)
    smd_force.addBond([0, 1], [SPRING_CONSTANT, 0.0])

    system.addForce(smd_force)

    return system, smd_force


def create_directional_smd_force(peptide_indices: List[int],
                                  anchor_position: np.ndarray,
                                  pull_vector: np.ndarray,
                                  system) -> Tuple:
    """
    Alternative SMD implementation using CustomExternalForce.

    Applies force to each peptide atom proportionally, pulling
    the peptide COM along a specific vector.
    """
    from openmm import CustomExternalForce

    # Normalize pull vector
    pv = np.array(pull_vector, dtype=float)
    pv = pv / np.linalg.norm(pv)

    # Force = -k * (projection - target)
    # Projection = (x - ax)*px + (y - ay)*py + (z - az)*pz
    # where (ax, ay, az) is anchor and (px, py, pz) is pull vector

    force_expression = f"""
    0.5 * k * (proj - target)^2;
    proj = (x - ax)*{pv[0]} + (y - ay)*{pv[1]} + (z - az)*{pv[2]}
    """

    smd_force = CustomExternalForce(force_expression)
    smd_force.addGlobalParameter("k", SPRING_CONSTANT)
    smd_force.addGlobalParameter("target", 0.0)
    smd_force.addGlobalParameter("ax", anchor_position[0])
    smd_force.addGlobalParameter("ay", anchor_position[1])
    smd_force.addGlobalParameter("az", anchor_position[2])

    # Apply to all peptide atoms
    for idx in peptide_indices:
        smd_force.addParticle(idx, [])

    system.addForce(smd_force)

    return system, smd_force


# =============================================================================
# WINDOW GENERATION
# =============================================================================

def run_smd_pulling(pdb_path: Path, peptide_id: str, pull_vector: List[float]) -> Dict:
    """
    Run steered MD and save window structures for umbrella sampling.
    """
    from openmm.app import PDBFile, ForceField, Modeller, Simulation
    from openmm.app import PME, HBonds, StateDataReporter
    from openmm import LangevinMiddleIntegrator, MonteCarloBarostat
    from openmm import unit, Platform

    print(f"\nStarting SMD pulling for {peptide_id}...")

    result = {
        'peptide_id': peptide_id,
        'timestamp': datetime.now().isoformat(),
        'windows': [],
    }

    try:
        # Load structure
        pdb = PDBFile(str(pdb_path))
        print(f"  Loaded: {pdb.topology.getNumAtoms()} atoms")

        # Force field
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Create modeller and solvate
        modeller = Modeller(pdb.topology, pdb.positions)
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=1.5 * unit.nanometer,  # Extra padding for pulling
            ionicStrength=0.15 * unit.molar,
        )

        print(f"  Solvated system: {modeller.topology.getNumAtoms()} atoms")

        # Identify peptide atoms (non-water, non-ion)
        peptide_indices = []
        for atom in modeller.topology.atoms():
            if atom.residue.name not in ['HOH', 'NA', 'CL', 'WAT']:
                peptide_indices.append(atom.index)

        print(f"  Peptide atoms: {len(peptide_indices)}")

        # Create system
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=HBonds,
        )

        # Add barostat
        system.addForce(MonteCarloBarostat(
            1.0 * unit.atmospheres,
            TEMPERATURE * unit.kelvin,
        ))

        # Calculate initial peptide COM for anchor
        positions = modeller.positions
        pos_array = np.array([[p.x, p.y, p.z] for p in positions])
        peptide_com = np.mean(pos_array[peptide_indices], axis=0)

        print(f"  Initial peptide COM: ({peptide_com[0]:.3f}, {peptide_com[1]:.3f}, {peptide_com[2]:.3f}) nm")

        # Add SMD force
        system, smd_force = create_directional_smd_force(
            peptide_indices,
            peptide_com,
            pull_vector,
            system,
        )

        # Integrator
        integrator = LangevinMiddleIntegrator(
            TEMPERATURE * unit.kelvin,
            1.0 / unit.picosecond,
            TIMESTEP_FS * unit.femtoseconds,
        )

        # Platform
        try:
            platform = Platform.getPlatformByName('Metal')
            properties = {'Precision': 'mixed'}
        except Exception:
            platform = Platform.getPlatformByName('CPU')
            properties = {}

        print(f"  Platform: {platform.getName()}")

        # Create simulation
        simulation = Simulation(
            modeller.topology,
            system,
            integrator,
            platform,
            properties,
        )
        simulation.context.setPositions(modeller.positions)

        # Minimize
        print("  Minimizing energy...")
        simulation.minimizeEnergy(maxIterations=1000)

        # Equilibrate
        print("  Equilibrating (10 ps)...")
        simulation.step(5000)

        # Create window directory
        window_dir = OUTPUT_DIR / f"{peptide_id}_windows"
        window_dir.mkdir(exist_ok=True)

        # Pull and save windows
        print(f"\n  Pulling along vector {pull_vector}...")
        print(f"  Saving {N_WINDOWS} windows...")

        for window_idx in range(N_WINDOWS):
            target_distance = window_idx * WINDOW_SPACING

            # Update target
            simulation.context.setParameter("target", target_distance)

            # Equilibrate at this window
            simulation.step(STEPS_PER_WINDOW)

            # Get current state
            state = simulation.context.getState(getPositions=True, getEnergy=True)
            current_positions = state.getPositions()
            potential_energy = state.getPotentialEnergy()

            # Calculate current peptide COM
            pos_array = np.array([[p.x, p.y, p.z] for p in current_positions])
            current_com = np.mean(pos_array[peptide_indices], axis=0)

            # Actual displacement
            displacement = np.dot(current_com - peptide_com, np.array(pull_vector))

            # Save window PDB
            window_pdb = window_dir / f"window_{window_idx:03d}_{target_distance:.2f}nm.pdb"
            with open(window_pdb, 'w') as f:
                PDBFile.writeFile(
                    simulation.topology,
                    current_positions,
                    f,
                )

            window_info = {
                'window_idx': window_idx,
                'target_nm': float(target_distance),
                'actual_nm': float(displacement),
                'potential_kJ': float(potential_energy._value),
                'pdb_path': str(window_pdb),
            }
            result['windows'].append(window_info)

            if window_idx % 5 == 0:
                print(f"    Window {window_idx:3d}: target={target_distance:.2f} nm, "
                      f"actual={displacement:.3f} nm, E={potential_energy._value/1000:.1f} kJ/mol")

        result['success'] = True
        result['n_windows'] = N_WINDOWS
        result['window_dir'] = str(window_dir)
        print(f"\n  ✓ SMD pulling complete: {N_WINDOWS} windows saved")

    except Exception as e:
        print(f"\n  ✗ SMD failed: {e}")
        result['success'] = False
        result['error'] = str(e)
        import traceback
        traceback.print_exc()

    return result


# =============================================================================
# UMBRELLA SAMPLING METADATA
# =============================================================================

def generate_umbrella_metadata(result: Dict) -> Path:
    """
    Generate metadata file for WHAM analysis.
    """
    if not result.get('success'):
        return None

    peptide_id = result['peptide_id']
    metadata_path = OUTPUT_DIR / f"{peptide_id}_umbrella_metadata.txt"

    with open(metadata_path, 'w') as f:
        f.write(f"# Umbrella sampling metadata for {peptide_id}\n")
        f.write(f"# Generated: {datetime.now().isoformat()}\n")
        f.write(f"# Spring constant: {SPRING_CONSTANT} kJ/mol/nm²\n")
        f.write(f"# Temperature: {TEMPERATURE} K\n")
        f.write("#\n")
        f.write("# window_pdb  target_nm  spring_k\n")

        for w in result['windows']:
            f.write(f"{w['pdb_path']}  {w['target_nm']:.4f}  {SPRING_CONSTANT}\n")

    print(f"  Umbrella metadata: {metadata_path}")
    return metadata_path


# =============================================================================
# MOCK COMPLEX BUILDER (for testing without actual receptor)
# =============================================================================

def build_mock_complex(peptide_sequence: str, peptide_id: str) -> Path:
    """
    Build a mock peptide structure for testing SMD.
    In production, this would be a docked peptide-receptor complex.
    """
    from pdbfixer import PDBFixer
    from openmm.app import PDBFile
    import tempfile

    aa_3letter = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
    }

    # Create backbone
    pdb_content = "HEADER    SMD TEST PEPTIDE\n"
    atom_num = 1

    for i, aa in enumerate(peptide_sequence):
        res_name = aa_3letter.get(aa, 'ALA')
        res_num = i + 1
        x_offset = i * 3.8

        pdb_content += f"ATOM  {atom_num:5d}  N   {res_name} A{res_num:4d}    {x_offset - 0.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           N\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  CA  {res_name} A{res_num:4d}    {x_offset:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  C   {res_name} A{res_num:4d}    {x_offset + 1.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  O   {res_name} A{res_num:4d}    {x_offset + 2.0:8.3f}{1.0:8.3f}{0.0:8.3f}  1.00  0.00           O\n"
        atom_num += 1

    pdb_content += "END\n"

    # Save and fix
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as f:
        f.write(pdb_content)
        temp_path = f.name

    fixer = PDBFixer(temp_path)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.4)

    output_path = OUTPUT_DIR / f"{peptide_id}_mock_complex.pdb"
    with open(output_path, 'w') as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)

    Path(temp_path).unlink()

    print(f"  Built mock complex: {output_path}")
    return output_path


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run SMD pulling on test systems.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Steered Molecular Dynamics (SMD)',
        'parameters': {
            'pull_velocity_nm_ps': PULL_VELOCITY,
            'spring_constant_kJ_mol_nm2': SPRING_CONSTANT,
            'pull_distance_nm': PULL_DISTANCE,
            'window_spacing_nm': WINDOW_SPACING,
            'n_windows': N_WINDOWS,
        },
        'systems': {},
    }

    for system_id, info in TEST_SYSTEMS.items():
        print(f"\n{'=' * 60}")
        print(f"System: {system_id}")
        print(f"  Peptide: {info['peptide']}")
        print(f"  Target: {info['receptor']}")
        print(f"{'=' * 60}")

        # Build mock complex (replace with actual docked structure in production)
        if info.get('complex_pdb') is None:
            print("\n  Building mock complex for testing...")
            pdb_path = build_mock_complex(info['peptide'], system_id)
        else:
            pdb_path = Path(info['complex_pdb'])

        # Run SMD
        smd_result = run_smd_pulling(pdb_path, system_id, info['pull_vector'])
        results['systems'][system_id] = smd_result

        # Generate umbrella metadata
        if smd_result.get('success'):
            metadata_path = generate_umbrella_metadata(smd_result)
            smd_result['umbrella_metadata'] = str(metadata_path)

    # Summary
    print("\n" + "=" * 80)
    print("SMD PULLING SUMMARY")
    print("=" * 80)

    successful = sum(1 for r in results['systems'].values() if r.get('success'))
    total = len(results['systems'])
    print(f"\n  Successful: {successful}/{total}")

    for sid, res in results['systems'].items():
        if res.get('success'):
            print(f"    ✓ {sid}: {res['n_windows']} windows")
        else:
            print(f"    ✗ {sid}: FAILED")

    # Save results
    output_json = OUTPUT_DIR / "smd_pulling_results.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {output_json}")
    print("\n  NEXT STEP: Run umbrella sampling on each window,")
    print("  then use WHAM to calculate ΔG binding free energy.")

    return results


if __name__ == "__main__":
    main()
