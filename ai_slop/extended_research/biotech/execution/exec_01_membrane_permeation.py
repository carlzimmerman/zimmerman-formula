#!/usr/bin/env python3
"""
exec_01_membrane_permeation.py - Heavy-Compute BBB Permeation Simulation

Steered Molecular Dynamics (SMD) simulation of TAT-tagged ZIM-D2R-001 peptide
crossing a POPC lipid bilayer using OpenMM with Apple Silicon Metal acceleration.

PHYSICS OVERVIEW:
This script simulates the physical process of a cell-penetrating peptide (CPP)
dragging our therapeutic peptide through a lipid membrane. We use a harmonic
"tractor beam" potential that moves along the Z-axis, pulling the peptide's
center of mass through the bilayer while calculating the resistance force at
every step.

The result: A Potential of Mean Force (PMF) profile showing the thermodynamic
energy barrier (ΔG) for membrane permeation.

COMPUTATIONAL REQUIREMENTS:
- Apple M4 Max GPU via Metal API
- Multi-hour runtime (5-50 ns simulation)
- ~50,000-100,000 atoms (peptide + lipids + water + ions)
- Sustained 100% GPU utilization

INPUTS REQUIRED:
- system_equilibrated.pdb: Pre-built membrane system from CHARMM-GUI containing:
  - TAT-tagged ZIM-D2R-001 peptide positioned above bilayer
  - POPC lipid bilayer (128+ lipids)
  - TIP3P water box
  - 0.15M NaCl ions

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Computational research only. Not peer reviewed. Not medical advice.
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import csv
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# OpenMM IMPORTS
# =============================================================================
try:
    import openmm as mm
    from openmm import app, unit
    from openmm.app import PDBFile, ForceField, Modeller, Simulation
    from openmm.app import PME, HBonds, DCDReporter, StateDataReporter
    print(f"OpenMM version: {mm.__version__}")
except ImportError:
    print("ERROR: OpenMM not installed. Run: mamba install -c conda-forge openmm")
    sys.exit(1)

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

class SimulationConfig:
    """Configuration for membrane permeation SMD simulation."""

    # Input/Output files
    INPUT_PDB = "system_equilibrated.pdb"
    OUTPUT_TRAJECTORY = "permeation_trajectory.dcd"
    OUTPUT_ENERGY_CSV = "permeation_energy.csv"
    OUTPUT_FORCE_CSV = "permeation_force_profile.csv"
    CHECKPOINT_FILE = "permeation_checkpoint.chk"

    # Physical parameters
    TEMPERATURE = 310 * unit.kelvin  # Human body temperature
    FRICTION = 1.0 / unit.picosecond  # Langevin friction coefficient
    TIMESTEP = 2.0 * unit.femtoseconds  # Integration timestep

    # Pressure coupling (for membrane stability)
    PRESSURE = 1.0 * unit.atmosphere
    BAROSTAT_FREQUENCY = 25  # Steps between pressure rescaling

    # SMD Parameters (the "tractor beam")
    SPRING_CONSTANT = 1000 * unit.kilojoules_per_mole / unit.nanometer**2  # Stiff spring
    PULLING_VELOCITY = 0.001 * unit.nanometer / unit.picosecond  # 1 nm/ns = slow pulling
    TOTAL_PULL_DISTANCE = 6.0 * unit.nanometer  # Distance to traverse bilayer

    # Simulation length
    # At 0.001 nm/ps velocity, traversing 6 nm takes 6000 ps = 6 ns
    # With 2 fs timestep, that's 3,000,000 steps
    TOTAL_STEPS = 3_000_000  # ~6 ns of pulling
    EQUILIBRATION_STEPS = 50_000  # 100 ps equilibration before pulling

    # Reporting frequencies
    TRAJECTORY_FREQ = 10_000  # Save coordinates every 20 ps
    ENERGY_FREQ = 1_000  # Report energy every 2 ps
    FORCE_FREQ = 500  # Record force every 1 ps

    # Platform selection (Apple Silicon optimization)
    PREFERRED_PLATFORM = "Metal"  # M4 Max GPU
    FALLBACK_PLATFORMS = ["OpenCL", "CUDA", "CPU"]


# =============================================================================
# PLATFORM SETUP (Apple Silicon Optimization)
# =============================================================================

def setup_platform():
    """
    Configure OpenMM platform for maximum performance on Apple Silicon.
    Prefers Metal, falls back to OpenCL, then CUDA, then CPU.
    """
    config = SimulationConfig()

    # List available platforms
    print("Available OpenMM platforms:")
    for i in range(mm.Platform.getNumPlatforms()):
        platform = mm.Platform.getPlatform(i)
        print(f"  [{i}] {platform.getName()}")

    # Try preferred platform first
    platforms_to_try = [config.PREFERRED_PLATFORM] + config.FALLBACK_PLATFORMS

    for platform_name in platforms_to_try:
        try:
            platform = mm.Platform.getPlatformByName(platform_name)
            print(f"\nSelected platform: {platform_name}")

            # Platform-specific properties
            properties = {}

            if platform_name == "Metal":
                # Metal-specific optimizations
                print("  Using Apple Metal API for M4 Max GPU acceleration")

            elif platform_name == "CUDA":
                properties["CudaPrecision"] = "mixed"
                properties["CudaDeviceIndex"] = "0"
                print("  Using CUDA with mixed precision")

            elif platform_name == "OpenCL":
                properties["OpenCLPrecision"] = "mixed"
                print("  Using OpenCL with mixed precision")

            return platform, properties

        except Exception as e:
            print(f"  Platform {platform_name} not available: {e}")
            continue

    # Fallback to CPU
    print("\nWARNING: No GPU platform available. Using CPU (will be very slow)")
    return mm.Platform.getPlatformByName("CPU"), {}


# =============================================================================
# SYSTEM LOADING AND FORCE FIELD
# =============================================================================

def load_system(pdb_path: Path):
    """
    Load the pre-equilibrated membrane system.

    Expects a PDB file from CHARMM-GUI containing:
    - TAT-tagged peptide
    - POPC lipid bilayer
    - Water and ions
    """
    print(f"\nLoading system from: {pdb_path}")

    if not pdb_path.exists():
        print(f"ERROR: Input file not found: {pdb_path}")
        print("\nTo create this file:")
        print("1. Go to https://charmm-gui.org")
        print("2. Use 'Membrane Builder' module")
        print("3. Upload your TAT-tagged ZIM-D2R-001 structure")
        print("4. Build POPC bilayer + solvate + add ions")
        print("5. Download and save as 'system_equilibrated.pdb'")
        sys.exit(1)

    pdb = PDBFile(str(pdb_path))

    print(f"  Loaded {pdb.topology.getNumAtoms()} atoms")
    print(f"  Loaded {pdb.topology.getNumResidues()} residues")
    print(f"  Loaded {pdb.topology.getNumChains()} chains")

    return pdb


def setup_forcefield_and_system(pdb):
    """
    Set up AMBER force field for membrane simulations.

    Uses:
    - amber14-all.xml: Protein parameters
    - lipid17.xml: POPC lipid parameters
    - tip3pfb.xml: Water model
    """
    print("\nSetting up force field...")

    # AMBER14 with Lipid17 and TIP3P-FB water
    forcefield = ForceField(
        'amber14-all.xml',
        'amber14/lipid17.xml',
        'amber14/tip3pfb.xml'
    )

    print("  Force fields loaded: AMBER14 + Lipid17 + TIP3P-FB")

    # Create system
    print("  Creating OpenMM system...")

    system = forcefield.createSystem(
        pdb.topology,
        nonbondedMethod=PME,
        nonbondedCutoff=1.2 * unit.nanometer,
        constraints=HBonds,
        rigidWater=True,
        ewaldErrorTolerance=0.0005,
        hydrogenMass=1.5 * unit.amu  # Hydrogen mass repartitioning for larger timestep
    )

    print(f"  System has {system.getNumParticles()} particles")
    print(f"  System has {system.getNumForces()} forces")

    return system, forcefield


# =============================================================================
# STEERED MOLECULAR DYNAMICS (SMD) SETUP
# =============================================================================

def identify_peptide_atoms(pdb, peptide_chain_id='A'):
    """
    Identify atoms belonging to the peptide for center-of-mass pulling.

    Returns list of atom indices for the peptide.
    """
    print(f"\nIdentifying peptide atoms (chain {peptide_chain_id})...")

    peptide_atoms = []
    peptide_mass = 0.0

    for atom in pdb.topology.atoms():
        if atom.residue.chain.id == peptide_chain_id:
            # Check if it's a protein residue (not water/lipid)
            if atom.residue.name in [
                'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS',
                'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP',
                'TYR', 'VAL', 'HIE', 'HID', 'HIP', 'CYX'
            ]:
                peptide_atoms.append(atom.index)

    print(f"  Found {len(peptide_atoms)} peptide atoms")

    return peptide_atoms


def add_smd_force(system, peptide_atoms, positions, config: SimulationConfig):
    """
    Add Steered Molecular Dynamics force (the "tractor beam").

    Creates a harmonic potential that moves along the Z-axis:
    E = 0.5 * k * (z_com - z_target(t))^2

    where z_target(t) = z_initial - v * t

    This pulls the peptide's center of mass straight down through the membrane.
    """
    print("\nSetting up SMD pulling force...")

    # Calculate initial center of mass of peptide
    peptide_positions = [positions[i] for i in peptide_atoms]
    z_coords = [pos[2].value_in_unit(unit.nanometer) for pos in peptide_positions]
    z_initial = np.mean(z_coords)

    print(f"  Initial peptide COM Z-position: {z_initial:.3f} nm")

    # The SMD force: harmonic potential centered on a moving target
    # We implement this as a CustomCentroidBondForce that acts on the peptide COM

    # Define groups for the force
    # Group 0: peptide atoms (we'll apply force to their COM)

    # Energy expression: 0.5 * k * (z - z0)^2
    # z0 is updated externally each step
    smd_force = mm.CustomCentroidBondForce(1, "0.5*k*(z1 - z0)^2")

    smd_force.addGlobalParameter("k", config.SPRING_CONSTANT)
    smd_force.addGlobalParameter("z0", z_initial * unit.nanometer)

    # Add peptide group
    smd_force.addGroup(peptide_atoms)
    smd_force.addBond([0])  # Bond referencing group 0

    # Add force to system
    force_index = system.addForce(smd_force)

    print(f"  SMD force added (force index: {force_index})")
    print(f"  Spring constant: {config.SPRING_CONSTANT}")
    print(f"  Pulling velocity: {config.PULLING_VELOCITY}")

    return smd_force, z_initial


def add_membrane_restraints(system, pdb):
    """
    Add weak restraints to keep the membrane centered (optional).

    This prevents the entire system from drifting during long simulations.
    """
    print("\nAdding membrane center-of-mass restraint...")

    # Find phosphorus atoms (lipid head groups)
    phosphorus_atoms = []
    for atom in pdb.topology.atoms():
        if atom.name == 'P' and atom.residue.name in ['POPC', 'POPE', 'DPPC']:
            phosphorus_atoms.append(atom.index)

    if phosphorus_atoms:
        # Weak Z-restraint on membrane center
        restraint = mm.CustomExternalForce("0.5*k_mem*(z-z_mem)^2")
        restraint.addGlobalParameter("k_mem", 10.0)  # Weak
        restraint.addGlobalParameter("z_mem", 0.0)  # Will be set to membrane center
        restraint.addPerParticleParameter("dummy")

        for atom_idx in phosphorus_atoms[:10]:  # Only a few atoms
            restraint.addParticle(atom_idx, [0.0])

        system.addForce(restraint)
        print(f"  Added weak restraint on {len(phosphorus_atoms)} lipid P atoms")


# =============================================================================
# CUSTOM FORCE REPORTER
# =============================================================================

class ForceReporter:
    """
    Custom reporter to track the SMD pulling force over the trajectory.

    Records: step, time, z_com, z_target, force, work
    """

    def __init__(self, file_path, peptide_atoms, report_interval):
        self.file = open(file_path, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            'Step', 'Time_ps', 'Z_COM_nm', 'Z_Target_nm',
            'Force_kJ_mol_nm', 'Cumulative_Work_kJ_mol'
        ])
        self.peptide_atoms = peptide_atoms
        self.report_interval = report_interval
        self.cumulative_work = 0.0
        self.last_z = None
        self.last_force = None

    def report(self, simulation, state, step, z_target):
        """Record force data at current step."""
        if step % self.report_interval != 0:
            return

        # Get positions
        positions = state.getPositions(asNumpy=True)
        peptide_z = np.mean([positions[i][2].value_in_unit(unit.nanometer)
                            for i in self.peptide_atoms])

        # Get spring constant
        k = simulation.context.getParameter('k')

        # Calculate force: F = -k * (z - z0)
        displacement = peptide_z - z_target
        force = -k * displacement  # kJ/mol/nm

        # Integrate work: W = integral(F * dz)
        if self.last_z is not None:
            dz = peptide_z - self.last_z
            avg_force = (force + self.last_force) / 2
            self.cumulative_work += avg_force * dz

        time_ps = state.getTime().value_in_unit(unit.picosecond)

        self.writer.writerow([
            step, f"{time_ps:.3f}", f"{peptide_z:.4f}", f"{z_target:.4f}",
            f"{force:.4f}", f"{self.cumulative_work:.4f}"
        ])
        self.file.flush()

        self.last_z = peptide_z
        self.last_force = force

    def close(self):
        self.file.close()


# =============================================================================
# MAIN SIMULATION
# =============================================================================

def run_membrane_permeation():
    """
    Main execution: Run the complete membrane permeation SMD simulation.
    """
    config = SimulationConfig()

    print("=" * 80)
    print("MEMBRANE PERMEATION SIMULATION")
    print("Steered Molecular Dynamics - TAT-tagged ZIM-D2R-001 through POPC Bilayer")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Set up output directory
    output_dir = Path(__file__).parent / "membrane_results"
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Get platform
    platform, properties = setup_platform()

    # Load system
    input_pdb = Path(__file__).parent / config.INPUT_PDB
    pdb = load_system(input_pdb)

    # Set up force field and system
    system, forcefield = setup_forcefield_and_system(pdb)

    # Add pressure coupling (semi-isotropic for membrane)
    print("\nAdding pressure coupling...")
    barostat = mm.MonteCarloMembraneBarostat(
        config.PRESSURE,
        0.0 * unit.bar * unit.nanometer,  # Surface tension
        config.TEMPERATURE,
        mm.MonteCarloMembraneBarostat.XYIsotropic,
        mm.MonteCarloMembraneBarostat.ZFree,
        config.BAROSTAT_FREQUENCY
    )
    system.addForce(barostat)
    print("  MonteCarloMembraneBarostat added (XY-isotropic, Z-free)")

    # Identify peptide and add SMD force
    peptide_atoms = identify_peptide_atoms(pdb)
    smd_force, z_initial = add_smd_force(system, peptide_atoms, pdb.positions, config)

    # Create integrator
    print("\nSetting up Langevin integrator...")
    integrator = mm.LangevinMiddleIntegrator(
        config.TEMPERATURE,
        config.FRICTION,
        config.TIMESTEP
    )
    print(f"  Temperature: {config.TEMPERATURE}")
    print(f"  Friction: {config.FRICTION}")
    print(f"  Timestep: {config.TIMESTEP}")

    # Create simulation
    print("\nCreating simulation context...")
    simulation = Simulation(
        pdb.topology,
        system,
        integrator,
        platform,
        properties
    )
    simulation.context.setPositions(pdb.positions)

    # Initial minimization
    print("\nPerforming energy minimization...")
    print("  (This may take a few minutes)")
    simulation.minimizeEnergy(maxIterations=1000)
    print("  Minimization complete")

    # Get minimized state
    state = simulation.context.getState(getEnergy=True)
    print(f"  Potential energy: {state.getPotentialEnergy()}")

    # Set up reporters
    print("\nSetting up reporters...")

    # Trajectory reporter (DCD format for VMD/PyMOL)
    trajectory_path = output_dir / config.OUTPUT_TRAJECTORY
    simulation.reporters.append(
        DCDReporter(str(trajectory_path), config.TRAJECTORY_FREQ)
    )
    print(f"  Trajectory: {trajectory_path} (every {config.TRAJECTORY_FREQ} steps)")

    # Energy reporter
    energy_path = output_dir / config.OUTPUT_ENERGY_CSV
    simulation.reporters.append(
        StateDataReporter(
            str(energy_path),
            config.ENERGY_FREQ,
            step=True,
            time=True,
            potentialEnergy=True,
            kineticEnergy=True,
            temperature=True,
            volume=True,
            speed=True
        )
    )
    print(f"  Energy log: {energy_path}")

    # Custom force reporter
    force_path = output_dir / config.OUTPUT_FORCE_CSV
    force_reporter = ForceReporter(str(force_path), peptide_atoms, config.FORCE_FREQ)
    print(f"  Force profile: {force_path}")

    # Also report to stdout
    simulation.reporters.append(
        StateDataReporter(
            sys.stdout,
            config.ENERGY_FREQ * 10,
            step=True,
            time=True,
            temperature=True,
            speed=True,
            remainingTime=True,
            totalSteps=config.EQUILIBRATION_STEPS + config.TOTAL_STEPS
        )
    )

    # ==========================================================================
    # PHASE 1: EQUILIBRATION (no pulling)
    # ==========================================================================
    print("\n" + "=" * 80)
    print("PHASE 1: EQUILIBRATION")
    print(f"Running {config.EQUILIBRATION_STEPS} steps ({config.EQUILIBRATION_STEPS * 2 / 1000:.1f} ps)")
    print("=" * 80)

    simulation.step(config.EQUILIBRATION_STEPS)

    print("Equilibration complete")

    # Save checkpoint
    checkpoint_path = output_dir / config.CHECKPOINT_FILE
    simulation.saveCheckpoint(str(checkpoint_path))
    print(f"Checkpoint saved: {checkpoint_path}")

    # ==========================================================================
    # PHASE 2: STEERED MD (pulling through membrane)
    # ==========================================================================
    print("\n" + "=" * 80)
    print("PHASE 2: STEERED MOLECULAR DYNAMICS")
    print(f"Pulling peptide {config.TOTAL_PULL_DISTANCE} through membrane")
    print(f"Velocity: {config.PULLING_VELOCITY}")
    print(f"Total steps: {config.TOTAL_STEPS} ({config.TOTAL_STEPS * 2 / 1e6:.1f} ns)")
    print("=" * 80)
    print()
    print("Starting heavy computation - GPU at full load")
    print("-" * 80)

    # Pulling loop
    pulling_velocity_nm_per_step = (
        config.PULLING_VELOCITY.value_in_unit(unit.nanometer / unit.picosecond) *
        config.TIMESTEP.value_in_unit(unit.picosecond)
    )

    z_target = z_initial

    steps_per_block = 1000
    n_blocks = config.TOTAL_STEPS // steps_per_block

    for block in range(n_blocks):
        # Update pulling target
        z_target -= pulling_velocity_nm_per_step * steps_per_block
        simulation.context.setParameter('z0', z_target * unit.nanometer)

        # Run block
        simulation.step(steps_per_block)

        # Report force
        current_step = config.EQUILIBRATION_STEPS + (block + 1) * steps_per_block
        state = simulation.context.getState(getPositions=True)
        force_reporter.report(simulation, state, current_step, z_target)

        # Periodic checkpoint
        if block % 1000 == 0 and block > 0:
            simulation.saveCheckpoint(str(checkpoint_path))

    # ==========================================================================
    # FINISH
    # ==========================================================================
    print("\n" + "=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)

    # Final state
    state = simulation.context.getState(getEnergy=True, getPositions=True)
    print(f"Final potential energy: {state.getPotentialEnergy()}")

    # Close force reporter
    force_reporter.close()

    # Save final checkpoint
    simulation.saveCheckpoint(str(checkpoint_path))

    # Summary
    print(f"\nOutput files saved to: {output_dir}")
    print(f"  - {config.OUTPUT_TRAJECTORY}: Atomic trajectory (view in PyMOL/VMD)")
    print(f"  - {config.OUTPUT_ENERGY_CSV}: Energy/temperature log")
    print(f"  - {config.OUTPUT_FORCE_CSV}: SMD force profile")
    print(f"  - {config.CHECKPOINT_FILE}: Restart checkpoint")

    print("\n" + "=" * 80)
    print("POST-ANALYSIS")
    print("=" * 80)
    print("""
To calculate the Potential of Mean Force (PMF):

1. Load force profile into numpy:
   data = np.loadtxt('permeation_force_profile.csv', delimiter=',', skiprows=1)

2. Integrate force over Z to get free energy:
   z = data[:, 2]  # Z coordinate
   force = data[:, 4]  # Applied force
   pmf = cumulative_trapezoid(-force, z, initial=0)

3. The maximum of the PMF is the activation barrier (ΔG‡) for membrane crossing.

4. Visualize trajectory:
   pymol permeation_trajectory.dcd
   """)

    print("\nDISCLAIMER: This is computational research only. Results require")
    print("experimental validation before any therapeutic application.")
    print("=" * 80)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_membrane_permeation()
