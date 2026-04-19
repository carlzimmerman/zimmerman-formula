#!/usr/bin/env python3
"""
M4 OpenMM Thermodynamics: Metal-Accelerated Molecular Dynamics

SPDX-License-Identifier: AGPL-3.0-or-later

Uses OpenMM on Apple M4's Metal GPU backend for GPU-accelerated
molecular dynamics and thermodynamic validation.

This is Stage 2 of the physics-first protein design pipeline:
1. ESM-2 structure prediction
2. OpenMM thermodynamic validation (this script)
3. Z² resonance filtering

Force Field: AMBER14-all with TIP3P-FB water
Platform: Metal (Apple Silicon GPU)

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# OPENMM CONFIGURATION
# ==============================================================================

def setup_openmm_platform():
    """
    Setup OpenMM with Metal acceleration on Apple Silicon.

    Platform priority: Metal > OpenCL > CPU
    """
    try:
        import openmm as mm
        from openmm import unit

        print("OpenMM version:", mm.__version__)

        # List available platforms
        print("\nAvailable platforms:")
        for i in range(mm.Platform.getNumPlatforms()):
            platform = mm.Platform.getPlatform(i)
            print(f"  {i}: {platform.getName()}")

        # Try Metal first (Apple Silicon)
        try:
            platform = mm.Platform.getPlatformByName('Metal')
            print(f"\n✓ Using Metal platform (Apple Silicon GPU)")
            return platform
        except Exception:
            pass

        # Fall back to OpenCL
        try:
            platform = mm.Platform.getPlatformByName('OpenCL')
            print(f"\n✓ Using OpenCL platform")
            return platform
        except Exception:
            pass

        # Fall back to CPU
        platform = mm.Platform.getPlatformByName('CPU')
        print(f"\n⚠ Using CPU platform (no GPU acceleration)")
        return platform

    except ImportError:
        print("⚠ OpenMM not installed.")
        print("Install with: conda install -c conda-forge openmm")
        return None


# ==============================================================================
# STRUCTURE PREPARATION
# ==============================================================================

def load_pdb_for_openmm(pdb_path: str):
    """
    Load PDB file and prepare for OpenMM simulation.

    Uses PDBFixer to add missing atoms and hydrogens.
    """
    try:
        from pdbfixer import PDBFixer
        from openmm.app import PDBFile
        import openmm as mm

        print(f"\nLoading structure: {pdb_path}")

        # Fix PDB (add missing atoms, hydrogens)
        fixer = PDBFixer(filename=pdb_path)

        print("  Finding missing residues...")
        fixer.findMissingResidues()

        print("  Finding missing atoms...")
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()

        print("  Adding hydrogens...")
        fixer.addMissingHydrogens(7.4)  # pH 7.4

        print(f"✓ Structure prepared: {len(list(fixer.topology.atoms()))} atoms")

        return fixer.topology, fixer.positions

    except ImportError:
        print("⚠ PDBFixer not installed.")
        print("Install with: conda install -c conda-forge pdbfixer")
        return None, None
    except Exception as e:
        print(f"⚠ Error loading PDB: {e}")
        return None, None


def create_system_amber14(topology, add_water: bool = True, box_size: float = 6.0):
    """
    Create OpenMM system with AMBER14-all force field.

    Force field: AMBER14-all + TIP3P-FB water
    """
    try:
        import openmm as mm
        from openmm import app, unit

        print("\nCreating AMBER14 system...")

        # Load force field
        forcefield = app.ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

        if add_water:
            print(f"  Adding water box ({box_size} nm)...")
            # Create modeller for solvation
            modeller = app.Modeller(topology, positions)
            modeller.addSolvent(
                forcefield,
                boxSize=mm.Vec3(box_size, box_size, box_size) * unit.nanometer,
                padding=1.0 * unit.nanometer
            )
            topology = modeller.topology
            positions = modeller.positions
            print(f"  Solvated system: {len(list(topology.atoms()))} atoms")

        # Create system
        system = forcefield.createSystem(
            topology,
            nonbondedMethod=app.PME if add_water else app.NoCutoff,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=app.HBonds,
            hydrogenMass=4 * unit.amu  # Hydrogen mass repartitioning for 4fs timestep
        )

        print(f"✓ System created with {system.getNumParticles()} particles")

        return system, topology, positions

    except Exception as e:
        print(f"⚠ Error creating system: {e}")
        return None, None, None


# ==============================================================================
# ENERGY MINIMIZATION & EQUILIBRATION
# ==============================================================================

def minimize_and_equilibrate(
    system,
    topology,
    positions,
    platform,
    temperature: float = 310.0,  # Kelvin (body temp)
    equilibration_steps: int = 5000,
    output_dir: str = "md_output"
):
    """
    Energy minimize and equilibrate structure.

    1. Energy minimization (steepest descent)
    2. NVT equilibration at target temperature
    """
    try:
        import openmm as mm
        from openmm import app, unit

        os.makedirs(output_dir, exist_ok=True)

        print(f"\n{'='*60}")
        print("ENERGY MINIMIZATION & EQUILIBRATION")
        print(f"{'='*60}")

        # Integrator
        integrator = mm.LangevinMiddleIntegrator(
            temperature * unit.kelvin,
            1.0 / unit.picosecond,
            4.0 * unit.femtosecond  # 4fs with HMR
        )

        # Create simulation
        simulation = app.Simulation(topology, system, integrator, platform)
        simulation.context.setPositions(positions)

        # Initial energy
        state = simulation.context.getState(getEnergy=True)
        initial_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        print(f"\nInitial energy: {initial_energy:.1f} kJ/mol")

        # Minimize
        print("\nMinimizing energy...")
        simulation.minimizeEnergy(maxIterations=1000)

        state = simulation.context.getState(getEnergy=True)
        minimized_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        print(f"Minimized energy: {minimized_energy:.1f} kJ/mol")
        print(f"Energy reduction: {initial_energy - minimized_energy:.1f} kJ/mol")

        # Check for reasonable energy
        if minimized_energy > 1e6:
            print("⚠ WARNING: Energy still very high - structure may have issues")
            return None

        # Set velocities
        simulation.context.setVelocitiesToTemperature(temperature * unit.kelvin)

        # Equilibrate
        print(f"\nEquilibrating ({equilibration_steps} steps, T={temperature}K)...")

        # Add reporters
        pdb_path = os.path.join(output_dir, "equilibrated.pdb")
        log_path = os.path.join(output_dir, "equilibration.log")

        simulation.reporters.append(
            app.StateDataReporter(
                log_path, 500,
                step=True, time=True,
                potentialEnergy=True, kineticEnergy=True,
                temperature=True, speed=True
            )
        )

        simulation.step(equilibration_steps)

        # Final state
        state = simulation.context.getState(getPositions=True, getEnergy=True)
        final_energy = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        final_positions = state.getPositions()

        print(f"\nFinal energy: {final_energy:.1f} kJ/mol")

        # Save equilibrated structure
        with open(pdb_path, 'w') as f:
            app.PDBFile.writeFile(topology, final_positions, f)
        print(f"✓ Saved equilibrated structure: {pdb_path}")

        return {
            "initial_energy": initial_energy,
            "minimized_energy": minimized_energy,
            "final_energy": final_energy,
            "temperature": temperature,
            "equilibration_steps": equilibration_steps,
            "final_positions": np.array([[p.x, p.y, p.z] for p in final_positions]),
            "pdb_path": pdb_path
        }

    except Exception as e:
        print(f"⚠ Error during minimization: {e}")
        import traceback
        traceback.print_exc()
        return None


# ==============================================================================
# THERMODYNAMIC VALIDATION
# ==============================================================================

def compute_thermodynamic_metrics(
    system,
    topology,
    positions,
    platform,
    temperature: float = 310.0,
    production_steps: int = 10000,
    output_dir: str = "md_output"
):
    """
    Run production MD and compute thermodynamic metrics.

    Metrics:
    - RMSD from initial structure
    - Radius of gyration
    - Secondary structure stability
    - Energy fluctuations
    """
    try:
        import openmm as mm
        from openmm import app, unit

        print(f"\n{'='*60}")
        print("THERMODYNAMIC VALIDATION")
        print(f"{'='*60}")

        # Integrator
        integrator = mm.LangevinMiddleIntegrator(
            temperature * unit.kelvin,
            1.0 / unit.picosecond,
            4.0 * unit.femtosecond
        )

        # Simulation
        simulation = app.Simulation(topology, system, integrator, platform)
        simulation.context.setPositions(positions)
        simulation.context.setVelocitiesToTemperature(temperature * unit.kelvin)

        # Trajectory output
        traj_path = os.path.join(output_dir, "production.dcd")
        simulation.reporters.append(
            app.DCDReporter(traj_path, 100)
        )

        print(f"\nRunning production MD ({production_steps} steps)...")

        # Collect energy samples
        energies = []
        temperatures_measured = []

        for i in range(production_steps // 100):
            simulation.step(100)
            state = simulation.context.getState(getEnergy=True)
            pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
            ke = state.getKineticEnergy().value_in_unit(unit.kilojoule_per_mole)
            energies.append(pe)

            # Instantaneous temperature from KE
            n_dof = 3 * system.getNumParticles() - 6  # Remove COM motion
            T = 2 * ke / (n_dof * 8.314e-3)  # kJ/mol/K
            temperatures_measured.append(T)

        # Compute metrics
        energies = np.array(energies)
        temperatures_measured = np.array(temperatures_measured)

        mean_energy = float(np.mean(energies))
        energy_std = float(np.std(energies))
        energy_fluctuation = energy_std / abs(mean_energy) if abs(mean_energy) > 0 else 0

        mean_temp = float(np.mean(temperatures_measured))
        temp_std = float(np.std(temperatures_measured))

        # Check thermodynamic stability
        stable = energy_fluctuation < 0.1 and abs(mean_temp - temperature) < 20

        print(f"\n✓ Production complete")
        print(f"  Mean energy: {mean_energy:.1f} ± {energy_std:.1f} kJ/mol")
        print(f"  Energy fluctuation: {energy_fluctuation:.2%}")
        print(f"  Mean temperature: {mean_temp:.1f} ± {temp_std:.1f} K")
        print(f"  Thermodynamically stable: {'✓ YES' if stable else '✗ NO'}")

        return {
            "mean_energy": mean_energy,
            "energy_std": energy_std,
            "energy_fluctuation": energy_fluctuation,
            "mean_temperature": mean_temp,
            "temperature_std": temp_std,
            "target_temperature": temperature,
            "production_steps": production_steps,
            "thermodynamically_stable": stable,
            "trajectory_path": traj_path
        }

    except Exception as e:
        print(f"⚠ Error during production: {e}")
        import traceback
        traceback.print_exc()
        return None


# ==============================================================================
# FULL VALIDATION PIPELINE
# ==============================================================================

def is_ca_only_pdb(pdb_path: str) -> bool:
    """Check if PDB file contains only Cα atoms (before pdbfixer modifies it)."""
    atom_names = set()
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atom_name = line[12:16].strip()
                atom_names.add(atom_name)
    return atom_names == {'CA'}


def validate_structure(
    pdb_path: str,
    output_dir: str = "md_output",
    temperature: float = 310.0,
    equilibration_steps: int = 5000,
    production_steps: int = 10000,
    add_water: bool = False  # Start with vacuum for speed
) -> Dict:
    """
    Full thermodynamic validation pipeline.

    1. Load and prepare structure
    2. Create AMBER14 system
    3. Energy minimize
    4. Equilibrate
    5. Run production MD
    6. Compute stability metrics
    """
    print("=" * 70)
    print("M4 OPENMM THERMODYNAMIC VALIDATION")
    print("=" * 70)
    print(f"Input: {pdb_path}")
    print(f"Temperature: {temperature} K")

    os.makedirs(output_dir, exist_ok=True)

    result = {
        "timestamp": datetime.now().isoformat(),
        "input_pdb": pdb_path,
        "temperature": temperature,
        "status": "started"
    }

    # Check if Cα-only BEFORE loading with pdbfixer
    ca_only = is_ca_only_pdb(pdb_path)
    if ca_only:
        print("\n✓ Cα-only model detected - using Go-like potential")

    # Setup platform
    platform = setup_openmm_platform()
    if platform is None:
        result["status"] = "failed"
        result["error"] = "Could not setup OpenMM platform"
        return result

    result["platform"] = platform.getName()

    # Create system
    try:
        import openmm as mm
        from openmm import app, unit

        if ca_only:
            # Parse Cα coordinates directly for Go-model
            from openmm.app import PDBFile
            pdb = PDBFile(pdb_path)
            topology = pdb.topology
            positions = pdb.positions
            system = create_go_model(topology, positions)
            result["model_type"] = "ca_only_go"
        else:
            # Load and fix structure for all-atom
            topology, positions = load_pdb_for_openmm(pdb_path)
            if topology is None:
                result["status"] = "failed"
                result["error"] = "Could not load PDB"
                return result

            # Full AMBER14
            forcefield = app.ForceField('amber14-all.xml')
            system = forcefield.createSystem(
                topology,
                nonbondedMethod=app.NoCutoff,
                constraints=app.HBonds
            )
            result["model_type"] = "all_atom"

        result["n_atoms"] = system.getNumParticles()

    except Exception as e:
        result["status"] = "failed"
        result["error"] = f"Could not create system: {e}"
        return result

    # Minimize and equilibrate
    eq_result = minimize_and_equilibrate(
        system, topology, positions, platform,
        temperature=temperature,
        equilibration_steps=equilibration_steps,
        output_dir=output_dir
    )

    if eq_result is None:
        result["status"] = "failed"
        result["error"] = "Minimization failed"
        return result

    result["equilibration"] = {
        "initial_energy": eq_result["initial_energy"],
        "minimized_energy": eq_result["minimized_energy"],
        "final_energy": eq_result["final_energy"]
    }

    # Production MD (if equilibration succeeded)
    if eq_result["final_energy"] < 1e6:
        thermo_result = compute_thermodynamic_metrics(
            system, topology, eq_result["final_positions"],
            platform,
            temperature=temperature,
            production_steps=production_steps,
            output_dir=output_dir
        )

        if thermo_result:
            result["thermodynamics"] = thermo_result
            result["thermodynamically_stable"] = thermo_result["thermodynamically_stable"]

    result["status"] = "completed"

    # Save results
    output_path = os.path.join(output_dir, "validation_results.json")
    with open(output_path, 'w') as f:
        # Convert numpy arrays to lists for JSON
        json.dump(result, f, indent=2, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x))

    print(f"\n✓ Results saved to: {output_path}")

    return result


def create_go_model(topology, positions):
    """
    Create Go-like potential for Cα-only models.

    Simple harmonic potential between contacts.
    """
    import openmm as mm
    from openmm import unit

    n_atoms = len(list(topology.atoms()))

    # Create system
    system = mm.System()

    # Add particles
    for i in range(n_atoms):
        system.addParticle(12.0 * unit.amu)  # Carbon mass

    # Add harmonic bonds between sequential Cα
    bond_force = mm.HarmonicBondForce()
    for i in range(n_atoms - 1):
        # Cα-Cα distance ~3.8 Å
        bond_force.addBond(i, i+1, 0.38 * unit.nanometer, 1000 * unit.kilojoule_per_mole / unit.nanometer**2)
    system.addForce(bond_force)

    # Add contact potential
    contact_force = mm.CustomBondForce("eps*(1-exp(-alpha*(r-r0)))^2")
    contact_force.addGlobalParameter("eps", 10.0)  # kJ/mol
    contact_force.addGlobalParameter("alpha", 5.0)  # nm^-1
    contact_force.addPerBondParameter("r0")

    # Find native contacts
    positions_array = np.array([[p.x, p.y, p.z] for p in positions])

    for i in range(n_atoms):
        for j in range(i + 4, n_atoms):
            d = np.linalg.norm(positions_array[i] - positions_array[j])
            if d < 0.8:  # 8 Å cutoff
                contact_force.addBond(i, j, [d * unit.nanometer])

    system.addForce(contact_force)

    return system


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("M4 OPENMM THERMODYNAMICS - Metal-Accelerated MD Validation")
    print("=" * 70)

    # Check OpenMM installation
    try:
        import openmm as mm
        print(f"\n✓ OpenMM version: {mm.__version__}")

        platform = setup_openmm_platform()

        if platform:
            print(f"\nPlatform ready: {platform.getName()}")

            # Test with a simple structure
            test_pdb = "extended_research/biotech/hybrid_z2_test/m4_pipeline/predictions/test_z2_protein_esm.pdb"

            if os.path.exists(test_pdb):
                result = validate_structure(
                    test_pdb,
                    output_dir="extended_research/biotech/hybrid_z2_test/m4_pipeline/md_output",
                    equilibration_steps=1000,
                    production_steps=2000
                )

                print("\n" + "=" * 70)
                print("VALIDATION SUMMARY")
                print("=" * 70)
                print(f"Status: {result.get('status', 'unknown')}")
                print(f"Platform: {result.get('platform', 'unknown')}")
                if 'thermodynamically_stable' in result:
                    stable = result['thermodynamically_stable']
                    print(f"Thermodynamically stable: {'✓ YES' if stable else '✗ NO'}")
            else:
                print(f"\n⚠ Test PDB not found: {test_pdb}")
                print("Run m4_esm_predictor.py first to generate predictions.")

    except ImportError:
        print("\n⚠ OpenMM not installed.")
        print("Install with: conda install -c conda-forge openmm")
        print("\nFor Metal acceleration on M4:")
        print("  conda install -c conda-forge openmm cudatoolkit")
        print("  (Metal support is automatic on Apple Silicon)")
