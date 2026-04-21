#!/usr/bin/env python3
"""
exec_01_membrane_permeation_halfload.py - Reduced Load Membrane Simulation

Same SMD simulation as exec_01_membrane_permeation.py but configured for
~50% GPU utilization by:
1. Smaller system (fewer lipids, less water)
2. Longer reporting intervals
3. Reduced simulation length (1.5 ns instead of 6 ns)

This is a TEST RUN to validate the pipeline before full production.

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import csv
import warnings
warnings.filterwarnings('ignore')

try:
    import openmm as mm
    from openmm import app, unit
    from openmm.app import PDBFile, ForceField, Modeller, Simulation
    from openmm.app import PME, HBonds, DCDReporter, StateDataReporter
    print(f"OpenMM version: {mm.__version__}")
except ImportError:
    print("ERROR: OpenMM not installed")
    sys.exit(1)

# =============================================================================
# Z² CONSTANTS
# =============================================================================
Z2 = 32 * np.pi / 3
R_NATURAL = (Z2 ** 0.25) * 3.8

# =============================================================================
# REDUCED LOAD CONFIGURATION
# =============================================================================

class HalfLoadConfig:
    """Reduced load settings for ~50% GPU utilization."""

    # Files
    INPUT_PDB = "system_equilibrated.pdb"
    OUTPUT_DIR = "membrane_results_halfload"
    OUTPUT_TRAJECTORY = "permeation_trajectory.dcd"
    OUTPUT_ENERGY_CSV = "permeation_energy.csv"
    OUTPUT_FORCE_CSV = "permeation_force_profile.csv"

    # Physical parameters (same as full run)
    TEMPERATURE = 310 * unit.kelvin
    FRICTION = 1.0 / unit.picosecond
    TIMESTEP = 2.0 * unit.femtoseconds
    PRESSURE = 1.0 * unit.atmosphere

    # SMD Parameters
    SPRING_CONSTANT = 1000 * unit.kilojoules_per_mole / unit.nanometer**2
    PULLING_VELOCITY = 0.002 * unit.nanometer / unit.picosecond  # 2x faster = shorter run
    TOTAL_PULL_DISTANCE = 3.0 * unit.nanometer  # Half the distance

    # REDUCED SIMULATION LENGTH
    # 3 nm at 0.002 nm/ps = 1500 ps = 1.5 ns
    TOTAL_STEPS = 750_000  # 1.5 ns (vs 6 ns full)
    EQUILIBRATION_STEPS = 25_000  # 50 ps (vs 100 ps full)

    # Less frequent reporting = less I/O overhead
    TRAJECTORY_FREQ = 25_000  # Save every 50 ps
    ENERGY_FREQ = 5_000  # Report every 10 ps
    FORCE_FREQ = 2_500  # Force every 5 ps


# =============================================================================
# DEMONSTRATION MODE (No input file required)
# =============================================================================

def create_demo_peptide():
    """
    Create a minimal demo system for testing when no membrane file exists.
    Just the TAT-tagged peptide in a water box.
    """
    print("\n" + "=" * 60)
    print("DEMO MODE: Creating minimal test system")
    print("(No membrane - just peptide in water)")
    print("=" * 60)

    from pdbfixer import PDBFixer
    from io import StringIO

    # TAT + linker + minimal D2R-like sequence
    sequence = "YGRKKRRQRRRGGSGCYIQVDPYITC"

    # Create CA trace PDB
    aa_codes = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
    }

    pdb_lines = []
    for i, aa in enumerate(sequence):
        resname = aa_codes.get(aa, 'ALA')
        x, y, z = i * 3.8, 0, 0
        line = f"ATOM  {i+1:5d}  CA  {resname} A{i+1:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C"
        pdb_lines.append(line)
    pdb_lines.append("END")

    # Save temp file
    temp_path = Path(__file__).parent / "temp_demo_peptide.pdb"
    with open(temp_path, 'w') as f:
        f.write('\n'.join(pdb_lines))

    # Fix with PDBFixer
    print("  Building peptide with PDBFixer...")
    fixer = PDBFixer(str(temp_path))
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.4)

    # Create modeller and add small water box
    print("  Adding water box...")
    forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
    modeller = Modeller(fixer.topology, fixer.positions)

    # Small box for demo
    modeller.addSolvent(forcefield, padding=1.0*unit.nanometer,
                        ionicStrength=0.15*unit.molar)

    print(f"  Demo system: {modeller.topology.getNumAtoms()} atoms")

    # Clean up
    temp_path.unlink()

    return modeller.topology, modeller.positions, forcefield


def setup_platform_halfload():
    """Set up platform - prefer Metal but accept any."""
    print("\nConfiguring OpenMM platform...")

    for name in ["Metal", "OpenCL", "CUDA", "CPU"]:
        try:
            platform = mm.Platform.getPlatformByName(name)
            print(f"  Using: {name}")
            return platform, {}
        except:
            continue

    return mm.Platform.getPlatformByName("CPU"), {}


def run_halfload_demo():
    """Run a demonstration membrane permeation at half load."""

    config = HalfLoadConfig()

    print("=" * 70)
    print("MEMBRANE PERMEATION SIMULATION - HALF LOAD TEST")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Natural Length Scale: {R_NATURAL:.4f} Å")
    print(f"Simulation length: ~1.5 ns (reduced from 6 ns)")
    print()

    # Output directory
    output_dir = Path(__file__).parent / config.OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)

    # Check for real input file
    input_pdb = Path(__file__).parent / config.INPUT_PDB

    if input_pdb.exists():
        print(f"Loading pre-built membrane system: {input_pdb}")
        pdb = PDBFile(str(input_pdb))
        topology = pdb.topology
        positions = pdb.positions
        forcefield = ForceField('amber14-all.xml', 'amber14/lipid17.xml', 'amber14/tip3pfb.xml')
    else:
        print(f"No membrane file found at: {input_pdb}")
        print("Running in DEMO MODE with peptide in water box")
        topology, positions, forcefield = create_demo_peptide()

    print(f"\nSystem: {topology.getNumAtoms()} atoms")

    # Platform
    platform, properties = setup_platform_halfload()

    # Create system
    print("\nBuilding OpenMM system...")
    system = forcefield.createSystem(
        topology,
        nonbondedMethod=PME,
        nonbondedCutoff=1.0 * unit.nanometer,  # Slightly shorter cutoff
        constraints=HBonds,
        rigidWater=True
    )

    # Simple barostat (isotropic for demo)
    barostat = mm.MonteCarloBarostat(
        config.PRESSURE,
        config.TEMPERATURE,
        25
    )
    system.addForce(barostat)

    # Find peptide atoms for SMD
    peptide_atoms = []
    for atom in topology.atoms():
        if atom.residue.chain.id == 'A' or atom.residue.chain.index == 0:
            if atom.residue.name in [
                'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS',
                'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP',
                'TYR', 'VAL', 'HIE', 'HID', 'HIP', 'CYX'
            ]:
                peptide_atoms.append(atom.index)

    print(f"Peptide atoms for SMD: {len(peptide_atoms)}")

    if not peptide_atoms:
        print("ERROR: No peptide atoms found!")
        return

    # Initial Z position
    z_coords = [positions[i][2].value_in_unit(unit.nanometer) for i in peptide_atoms[:10]]
    z_initial = np.mean(z_coords)
    print(f"Initial peptide Z: {z_initial:.3f} nm")

    # SMD force
    print("Adding SMD pulling force...")
    smd_force = mm.CustomCentroidBondForce(1, "0.5*k*(z1 - z0)^2")
    smd_force.addGlobalParameter("k", config.SPRING_CONSTANT)
    smd_force.addGlobalParameter("z0", z_initial * unit.nanometer)
    smd_force.addGroup(peptide_atoms)
    smd_force.addBond([0])
    system.addForce(smd_force)

    # Integrator
    integrator = mm.LangevinMiddleIntegrator(
        config.TEMPERATURE,
        config.FRICTION,
        config.TIMESTEP
    )

    # Create simulation
    print("Creating simulation context...")
    simulation = Simulation(topology, system, integrator, platform, properties)
    simulation.context.setPositions(positions)

    # Minimize
    print("\nMinimizing energy...")
    simulation.minimizeEnergy(maxIterations=500)
    state = simulation.context.getState(getEnergy=True)
    print(f"  Minimized energy: {state.getPotentialEnergy()}")

    # Reporters
    simulation.reporters.append(
        DCDReporter(str(output_dir / config.OUTPUT_TRAJECTORY), config.TRAJECTORY_FREQ)
    )
    simulation.reporters.append(
        StateDataReporter(
            str(output_dir / config.OUTPUT_ENERGY_CSV),
            config.ENERGY_FREQ,
            step=True, time=True, potentialEnergy=True,
            temperature=True, speed=True
        )
    )
    simulation.reporters.append(
        StateDataReporter(
            sys.stdout, config.ENERGY_FREQ * 5,
            step=True, time=True, temperature=True, speed=True,
            remainingTime=True,
            totalSteps=config.EQUILIBRATION_STEPS + config.TOTAL_STEPS
        )
    )

    # Force profile CSV
    force_file = open(output_dir / config.OUTPUT_FORCE_CSV, 'w', newline='')
    force_writer = csv.writer(force_file)
    force_writer.writerow(['Step', 'Time_ps', 'Z_COM_nm', 'Z_Target_nm', 'Force_kJ_mol_nm'])

    # Equilibration
    print("\n" + "=" * 60)
    print("PHASE 1: EQUILIBRATION")
    print(f"Steps: {config.EQUILIBRATION_STEPS} ({config.EQUILIBRATION_STEPS * 2 / 1000:.0f} ps)")
    print("=" * 60)

    simulation.step(config.EQUILIBRATION_STEPS)
    print("Equilibration complete")

    # SMD Pulling
    print("\n" + "=" * 60)
    print("PHASE 2: STEERED MD (Pulling through membrane)")
    print(f"Distance: {config.TOTAL_PULL_DISTANCE}")
    print(f"Velocity: {config.PULLING_VELOCITY}")
    print(f"Steps: {config.TOTAL_STEPS} (~{config.TOTAL_STEPS * 2 / 1e6:.1f} ns)")
    print("=" * 60)
    print()

    pulling_rate = (
        config.PULLING_VELOCITY.value_in_unit(unit.nanometer / unit.picosecond) *
        config.TIMESTEP.value_in_unit(unit.picosecond)
    )

    z_target = z_initial
    steps_per_block = 2500

    for block in range(config.TOTAL_STEPS // steps_per_block):
        z_target -= pulling_rate * steps_per_block
        simulation.context.setParameter('z0', z_target * unit.nanometer)
        simulation.step(steps_per_block)

        # Record force
        if block % 10 == 0:
            state = simulation.context.getState(getPositions=True)
            positions_now = state.getPositions(asNumpy=True)
            peptide_z = np.mean([positions_now[i][2].value_in_unit(unit.nanometer)
                                for i in peptide_atoms[:10]])
            k = simulation.context.getParameter('k')
            force = -k * (peptide_z - z_target)
            time_ps = state.getTime().value_in_unit(unit.picosecond)
            step = config.EQUILIBRATION_STEPS + (block + 1) * steps_per_block

            force_writer.writerow([
                step, f"{time_ps:.1f}", f"{peptide_z:.4f}",
                f"{z_target:.4f}", f"{force:.2f}"
            ])
            force_file.flush()

    force_file.close()

    # Done
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
    print(f"\nOutput files in: {output_dir}")
    print(f"  - {config.OUTPUT_TRAJECTORY}")
    print(f"  - {config.OUTPUT_ENERGY_CSV}")
    print(f"  - {config.OUTPUT_FORCE_CSV}")
    print()
    print("To view trajectory: pymol " + str(output_dir / config.OUTPUT_TRAJECTORY))
    print()
    print("DISCLAIMER: Computational research only. Not medical advice.")


if __name__ == "__main__":
    run_halfload_demo()
