#!/usr/bin/env python3
"""
M4 AMBER Production MD: Rigorous Thermodynamic Equilibration

SPDX-License-Identifier: AGPL-3.0-or-later

Publication-quality molecular dynamics protocol:
1. Energy minimization (L-BFGS, 50,000 steps)
2. NVT equilibration (100 ps, heat to 310K)
3. NPT equilibration (100 ps, 1 atm)
4. Production MD (configurable, default 1 ns)

Force Field: AMBER14-all + TIP3P-FB water
Platform: OpenCL (Apple M4 GPU)

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import os
import sys
import json
import numpy as np
from datetime import datetime
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')


def run_production_md(
    solvated_pdb: str,
    output_dir: str = "production_md",
    temperature: float = 310.0,  # K (body temperature)
    pressure: float = 1.0,  # atm
    minimization_steps: int = 50000,
    nvt_steps: int = 50000,  # 100 ps at 2 fs timestep
    npt_steps: int = 50000,  # 100 ps
    production_steps: int = 500000,  # 1 ns at 2 fs timestep
    save_frequency: int = 5000,  # Every 10 ps
    timestep: float = 2.0  # fs
) -> Dict:
    """
    Run rigorous equilibration and production MD.

    Protocol:
    1. Energy minimization (L-BFGS)
    2. NVT equilibration (constant volume, heat to target T)
    3. NPT equilibration (constant pressure, establish density)
    4. Production MD (data collection)

    Args:
        solvated_pdb: Path to solvated system PDB
        output_dir: Output directory
        temperature: Target temperature in K
        pressure: Target pressure in atm
        minimization_steps: L-BFGS minimization steps
        nvt_steps: NVT equilibration steps
        npt_steps: NPT equilibration steps
        production_steps: Production MD steps
        save_frequency: Trajectory save frequency (steps)
        timestep: Integration timestep in fs

    Returns:
        Dictionary with simulation results
    """
    print("=" * 70)
    print("M4 AMBER PRODUCTION MD")
    print("Rigorous Thermodynamic Protocol")
    print("=" * 70)
    print(f"Input: {solvated_pdb}")
    print(f"Temperature: {temperature} K")
    print(f"Pressure: {pressure} atm")
    print(f"Timestep: {timestep} fs")

    os.makedirs(output_dir, exist_ok=True)

    result = {
        "timestamp": datetime.now().isoformat(),
        "input_pdb": solvated_pdb,
        "temperature_K": temperature,
        "pressure_atm": pressure,
        "timestep_fs": timestep,
        "protocol": {
            "minimization_steps": minimization_steps,
            "nvt_steps": nvt_steps,
            "npt_steps": npt_steps,
            "production_steps": production_steps
        },
        "status": "started"
    }

    try:
        import openmm as mm
        from openmm import app, unit
        from openmm.app import PDBFile, ForceField, Simulation, StateDataReporter, DCDReporter

        # =====================================================================
        # SETUP
        # =====================================================================
        print(f"\n{'='*60}")
        print("SYSTEM SETUP")
        print("=" * 60)

        # Load solvated system
        print(f"\nLoading system: {solvated_pdb}")
        pdb = PDBFile(solvated_pdb)

        n_atoms = len(list(pdb.topology.atoms()))
        print(f"  Total atoms: {n_atoms:,}")
        result["n_atoms"] = n_atoms

        # Load force field
        print("\nLoading AMBER14 force field...")
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

        # Create system
        print("Creating system...")
        system = forcefield.createSystem(
            pdb.topology,
            nonbondedMethod=app.PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=app.HBonds,
            hydrogenMass=4 * unit.amu  # HMR for larger timestep
        )

        # Setup platform
        print("\nSetting up compute platform...")
        try:
            platform = mm.Platform.getPlatformByName('OpenCL')
            print(f"  ✓ Using OpenCL (GPU acceleration)")
        except Exception:
            platform = mm.Platform.getPlatformByName('CPU')
            print(f"  ⚠ Using CPU (no GPU)")

        result["platform"] = platform.getName()

        # =====================================================================
        # PHASE 1: ENERGY MINIMIZATION
        # =====================================================================
        print(f"\n{'='*60}")
        print("PHASE 1: ENERGY MINIMIZATION")
        print(f"{'='*60}")
        print(f"Method: L-BFGS")
        print(f"Max iterations: {minimization_steps:,}")

        # Create integrator for minimization
        integrator = mm.LangevinMiddleIntegrator(
            temperature * unit.kelvin,
            1.0 / unit.picosecond,
            timestep * unit.femtosecond
        )

        simulation = Simulation(pdb.topology, system, integrator, platform)
        simulation.context.setPositions(pdb.positions)

        # Initial energy
        state = simulation.context.getState(getEnergy=True)
        initial_pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        print(f"\nInitial potential energy: {initial_pe:,.1f} kJ/mol")

        # Minimize
        print("\nMinimizing...")
        simulation.minimizeEnergy(maxIterations=minimization_steps)

        # Final energy
        state = simulation.context.getState(getEnergy=True)
        minimized_pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        print(f"Minimized potential energy: {minimized_pe:,.1f} kJ/mol")
        print(f"Energy reduction: {initial_pe - minimized_pe:,.1f} kJ/mol")

        result["minimization"] = {
            "initial_energy_kJ": initial_pe,
            "final_energy_kJ": minimized_pe,
            "reduction_kJ": initial_pe - minimized_pe
        }

        # Save minimized structure
        minimized_pdb = os.path.join(output_dir, "minimized.pdb")
        state = simulation.context.getState(getPositions=True)
        with open(minimized_pdb, 'w') as f:
            PDBFile.writeFile(pdb.topology, state.getPositions(), f)
        print(f"✓ Saved: {minimized_pdb}")

        # =====================================================================
        # PHASE 2: NVT EQUILIBRATION
        # =====================================================================
        print(f"\n{'='*60}")
        print("PHASE 2: NVT EQUILIBRATION (Constant Volume)")
        print(f"{'='*60}")
        nvt_time_ps = nvt_steps * timestep / 1000
        print(f"Duration: {nvt_time_ps:.1f} ps ({nvt_steps:,} steps)")
        print(f"Target temperature: {temperature} K")

        # Set velocities to target temperature
        simulation.context.setVelocitiesToTemperature(temperature * unit.kelvin)

        # Add reporter for NVT
        nvt_log = os.path.join(output_dir, "nvt_equilibration.log")
        simulation.reporters.append(
            StateDataReporter(
                nvt_log, 1000,
                step=True, time=True,
                potentialEnergy=True, kineticEnergy=True,
                temperature=True, speed=True
            )
        )

        print("\nRunning NVT equilibration...")
        simulation.step(nvt_steps)

        state = simulation.context.getState(getEnergy=True)
        nvt_pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        print(f"✓ NVT complete. Final PE: {nvt_pe:,.1f} kJ/mol")

        result["nvt_equilibration"] = {
            "duration_ps": nvt_time_ps,
            "final_energy_kJ": nvt_pe
        }

        # Clear reporters
        simulation.reporters.clear()

        # =====================================================================
        # PHASE 3: NPT EQUILIBRATION
        # =====================================================================
        print(f"\n{'='*60}")
        print("PHASE 3: NPT EQUILIBRATION (Constant Pressure)")
        print(f"{'='*60}")
        npt_time_ps = npt_steps * timestep / 1000
        print(f"Duration: {npt_time_ps:.1f} ps ({npt_steps:,} steps)")
        print(f"Target pressure: {pressure} atm")

        # Add barostat for NPT
        barostat = mm.MonteCarloBarostat(
            pressure * unit.atmosphere,
            temperature * unit.kelvin,
            25  # Frequency of volume moves
        )
        system.addForce(barostat)

        # Reinitialize context with barostat
        simulation.context.reinitialize(preserveState=True)

        # Add reporter for NPT
        npt_log = os.path.join(output_dir, "npt_equilibration.log")
        simulation.reporters.append(
            StateDataReporter(
                npt_log, 1000,
                step=True, time=True,
                potentialEnergy=True, kineticEnergy=True,
                temperature=True, density=True, speed=True
            )
        )

        print("\nRunning NPT equilibration...")
        simulation.step(npt_steps)

        state = simulation.context.getState(getEnergy=True)
        npt_pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
        print(f"✓ NPT complete. Final PE: {npt_pe:,.1f} kJ/mol")

        # Save equilibrated structure
        equilibrated_pdb = os.path.join(output_dir, "equilibrated.pdb")
        state = simulation.context.getState(getPositions=True)
        with open(equilibrated_pdb, 'w') as f:
            PDBFile.writeFile(pdb.topology, state.getPositions(), f)
        print(f"✓ Saved: {equilibrated_pdb}")

        result["npt_equilibration"] = {
            "duration_ps": npt_time_ps,
            "final_energy_kJ": npt_pe
        }

        # Clear reporters
        simulation.reporters.clear()

        # =====================================================================
        # PHASE 4: PRODUCTION MD
        # =====================================================================
        print(f"\n{'='*60}")
        print("PHASE 4: PRODUCTION MD")
        print(f"{'='*60}")
        production_time_ns = production_steps * timestep / 1e6
        save_interval_ps = save_frequency * timestep / 1000
        print(f"Duration: {production_time_ns:.2f} ns ({production_steps:,} steps)")
        print(f"Trajectory save interval: {save_interval_ps:.1f} ps")

        # Add trajectory reporter
        trajectory_file = os.path.join(output_dir, "production_trajectory.dcd")
        simulation.reporters.append(
            DCDReporter(trajectory_file, save_frequency)
        )

        # Add log reporter
        production_log = os.path.join(output_dir, "production.log")
        simulation.reporters.append(
            StateDataReporter(
                production_log, save_frequency,
                step=True, time=True,
                potentialEnergy=True, kineticEnergy=True,
                totalEnergy=True, temperature=True,
                density=True, speed=True
            )
        )

        print("\nRunning production MD...")
        print("(This may take a while for large systems)")

        # Run in chunks to show progress
        chunk_size = production_steps // 10
        for i in range(10):
            simulation.step(chunk_size)
            progress = (i + 1) * 10
            state = simulation.context.getState(getEnergy=True)
            current_pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)
            print(f"  {progress}% complete - PE: {current_pe:,.1f} kJ/mol")

        print(f"\n✓ Production complete!")
        print(f"✓ Trajectory saved: {trajectory_file}")

        # Get final statistics
        state = simulation.context.getState(getEnergy=True, getPositions=True)
        final_pe = state.getPotentialEnergy().value_in_unit(unit.kilojoule_per_mole)

        result["production"] = {
            "duration_ns": production_time_ns,
            "n_frames": production_steps // save_frequency,
            "trajectory_file": trajectory_file,
            "final_energy_kJ": final_pe
        }

        # Save final structure
        final_pdb = os.path.join(output_dir, "production_final.pdb")
        with open(final_pdb, 'w') as f:
            PDBFile.writeFile(pdb.topology, state.getPositions(), f)
        print(f"✓ Final structure: {final_pdb}")

        result["status"] = "success"

        # =====================================================================
        # SUMMARY
        # =====================================================================
        print(f"\n{'='*70}")
        print("SIMULATION COMPLETE")
        print("=" * 70)
        print(f"""
Protocol Summary:
  - Minimization: {minimization_steps:,} steps
  - NVT equilibration: {nvt_time_ps:.1f} ps
  - NPT equilibration: {npt_time_ps:.1f} ps
  - Production: {production_time_ns:.2f} ns

Energy Evolution:
  - Initial: {initial_pe:,.1f} kJ/mol
  - After minimization: {minimized_pe:,.1f} kJ/mol
  - After NVT: {nvt_pe:,.1f} kJ/mol
  - After NPT: {npt_pe:,.1f} kJ/mol
  - Final: {final_pe:,.1f} kJ/mol

Output Files:
  - Trajectory: {trajectory_file}
  - Final structure: {final_pdb}
  - Equilibrated structure: {equilibrated_pdb}

This trajectory is ready for analysis (RMSD, Rg, H-bonds).
        """)

        # Save results
        results_path = os.path.join(output_dir, "simulation_results.json")
        with open(results_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        return result

    except ImportError as e:
        print(f"\n✗ Missing dependency: {e}")
        result["status"] = "failed"
        result["error"] = str(e)
        return result

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        result["status"] = "failed"
        result["error"] = str(e)
        return result


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("M4 AMBER PRODUCTION MD ENGINE")
    print("Publication-Quality Molecular Dynamics")
    print("=" * 70)

    # Test with solvated system
    test_pdb = "all_atom_system/system_solvated.pdb"

    if os.path.exists(test_pdb):
        # For testing, use shorter simulation
        result = run_production_md(
            test_pdb,
            output_dir="production_md",
            minimization_steps=10000,  # Reduced for testing
            nvt_steps=10000,           # 20 ps
            npt_steps=10000,           # 20 ps
            production_steps=50000,    # 100 ps
            save_frequency=1000        # Every 2 ps
        )

        if result["status"] == "success":
            print(f"\n✓ Simulation complete!")
            print(f"Trajectory: {result['production']['trajectory_file']}")
        else:
            print(f"\n✗ Simulation failed: {result.get('error', 'unknown')}")
    else:
        print(f"\n⚠ Solvated system not found: {test_pdb}")
        print("Run m4_all_atom_builder.py first to prepare the system.")
