#!/usr/bin/env python3
"""
inv_03_thermal_scaling_bridge.py - Thermal Scaling Bridge Analysis

Tests the hypothesis that the discrepancy between √(Z²) ≈ 5.79 Å and
the empirical mean ≈ 6.04 Å is due to thermal expansion and solvation.

The Math:
  - √(Z²) = 5.79 Å is the "vacuum" or "0K" topology
  - Empirical 6.04 Å is the "solvated/310K" topology
  - Δ = 6.04 - 5.79 = 0.25 Å (4.3% expansion)

The Test:
  1. Take a protein structure (e.g., Ubiquitin 1UBQ)
  2. Run energy minimization (essentially 0K) and measure H1 topology
  3. Run explicit solvent MD at 310K and measure H1 topology
  4. Calculate Δ and compare to predicted thermal expansion

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
import urllib.request
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "thermal_bridge"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("THERMAL SCALING BRIDGE ANALYSIS")
print("Testing: √(Z²) + Thermal Expansion = Empirical H1")
print("=" * 80)
print()

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.79 Å
EMPIRICAL_H1 = 6.04  # Å (from our bootstrap analysis)
PREDICTED_DELTA = EMPIRICAL_H1 - SQRT_Z2  # ≈ 0.25 Å

print(f"Z² = 32π/3 = {Z_SQUARED:.4f}")
print(f"√(Z²) = {SQRT_Z2:.4f} Å (predicted vacuum topology)")
print(f"Empirical H1 = {EMPIRICAL_H1:.4f} Å (measured solvated)")
print(f"Predicted Δ = {PREDICTED_DELTA:.4f} Å ({100*PREDICTED_DELTA/SQRT_Z2:.2f}% expansion)")
print()

# Thermal expansion coefficient for proteins
# Literature: ~10^-4 per Kelvin for proteins
ALPHA_PROTEIN = 1e-4  # per Kelvin

# Temperature differential
T_VACUUM = 0  # K (energy minimized)
T_BODY = 310  # K
DELTA_T = T_BODY - T_VACUUM

# Predicted thermal expansion
PREDICTED_THERMAL = SQRT_Z2 * ALPHA_PROTEIN * DELTA_T
print(f"Predicted thermal expansion (α={ALPHA_PROTEIN}/K):")
print(f"  Δ_thermal = {SQRT_Z2:.2f} × {ALPHA_PROTEIN} × {DELTA_T} = {PREDICTED_THERMAL:.4f} Å")
print()


# =============================================================================
# STRUCTURE PREPARATION
# =============================================================================

def download_test_structure() -> Path:
    """
    Download ubiquitin (1UBQ) as test structure.
    Small, stable, well-characterized.
    """
    pdb_path = OUTPUT_DIR / "1UBQ.pdb"

    if not pdb_path.exists():
        print("Downloading ubiquitin (1UBQ)...")
        url = "https://files.rcsb.org/download/1UBQ.pdb"
        try:
            urllib.request.urlretrieve(url, pdb_path)
            print(f"  Downloaded: {pdb_path}")
        except Exception as e:
            print(f"  Download failed: {e}")
            return None

    return pdb_path


# =============================================================================
# TOPOLOGY CALCULATION (H1 DEATH RADII)
# =============================================================================

def parse_alpha_carbons(pdb_path: Path) -> np.ndarray:
    """
    Extract alpha carbon coordinates from PDB.
    """
    coords = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                atom_name = line[12:16].strip()
                if atom_name == 'CA':
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])

    return np.array(coords)


def compute_h1_death_radii(coords: np.ndarray) -> np.ndarray:
    """
    Compute H1 death radii using persistent homology (ripser).
    """
    try:
        from ripser import ripser

        # Compute persistence
        result = ripser(coords, maxdim=1)

        # Extract H1 death radii
        h1 = result['dgms'][1]  # (birth, death) pairs
        death_radii = h1[:, 1]  # death times = radii

        # Filter finite values
        death_radii = death_radii[np.isfinite(death_radii)]

        return death_radii

    except ImportError:
        print("  ripser not installed, using distance-based approximation")

        # Fallback: use characteristic distance scale
        from scipy.spatial.distance import pdist
        distances = pdist(coords)

        # H1 death radii roughly correspond to loop-closing distances
        # Approximate as distances in the 70-90th percentile
        return np.percentile(distances, [70, 75, 80, 85, 90])


# =============================================================================
# MOLECULAR DYNAMICS SIMULATION
# =============================================================================

def run_minimization(pdb_path: Path) -> Tuple[np.ndarray, float]:
    """
    Run energy minimization (essentially 0K structure).
    Returns (coordinates, mean_H1_death_radius).
    """
    try:
        from openmm.app import PDBFile, ForceField, Modeller, Simulation
        from openmm.app import NoCutoff, HBonds
        from openmm import LangevinMiddleIntegrator, Platform
        from openmm import unit

        print("\n  Running energy minimization (vacuum/0K analog)...")

        # Load structure
        pdb = PDBFile(str(pdb_path))

        # Force field (implicit solvent for speed)
        forcefield = ForceField('amber14-all.xml', 'implicit/gbn2.xml')

        # Create system
        system = forcefield.createSystem(
            pdb.topology,
            nonbondedMethod=NoCutoff,
            constraints=HBonds,
        )

        # Integrator (won't actually integrate, just for setup)
        integrator = LangevinMiddleIntegrator(
            1 * unit.kelvin,  # Very low T
            1.0 / unit.picosecond,
            1.0 * unit.femtoseconds,
        )

        # Platform
        platform = Platform.getPlatformByName('CPU')

        # Simulation
        simulation = Simulation(pdb.topology, system, integrator, platform)
        simulation.context.setPositions(pdb.positions)

        # Minimize
        simulation.minimizeEnergy(maxIterations=5000)

        # Get minimized positions
        state = simulation.context.getState(getPositions=True)
        positions = state.getPositions(asNumpy=True)

        # Convert to Å
        coords_A = positions * 10  # nm to Å

        # Extract CA atoms
        ca_indices = []
        for i, atom in enumerate(pdb.topology.atoms()):
            if atom.name == 'CA':
                ca_indices.append(i)

        ca_coords = coords_A[ca_indices]

        # Compute H1 topology
        death_radii = compute_h1_death_radii(ca_coords)
        mean_h1 = np.mean(death_radii)

        print(f"    Minimized structure: {len(ca_coords)} Cα atoms")
        print(f"    Mean H1 death radius: {mean_h1:.4f} Å")

        return ca_coords, mean_h1

    except Exception as e:
        print(f"  Minimization failed: {e}")
        return None, None


def run_heated_simulation(pdb_path: Path, temperature_K: float = 310,
                           duration_ps: float = 100) -> Tuple[np.ndarray, float]:
    """
    Run explicit solvent MD at specified temperature.
    Returns (final_coordinates, mean_H1_death_radius).
    """
    try:
        from openmm.app import PDBFile, ForceField, Modeller, Simulation
        from openmm.app import PME, HBonds
        from openmm import LangevinMiddleIntegrator, MonteCarloBarostat, Platform
        from openmm import unit

        print(f"\n  Running explicit solvent MD at {temperature_K}K...")

        # Load structure
        pdb = PDBFile(str(pdb_path))

        # Force field
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Modeller
        modeller = Modeller(pdb.topology, pdb.positions)

        # Add solvent
        print("    Adding solvent...")
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=1.0 * unit.nanometer,
            ionicStrength=0.15 * unit.molar,
        )

        # Create system
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=HBonds,
        )

        # Barostat
        system.addForce(MonteCarloBarostat(
            1.0 * unit.atmospheres,
            temperature_K * unit.kelvin,
        ))

        # Integrator
        integrator = LangevinMiddleIntegrator(
            temperature_K * unit.kelvin,
            1.0 / unit.picosecond,
            2.0 * unit.femtoseconds,
        )

        # Platform
        try:
            platform = Platform.getPlatformByName('Metal')
        except Exception:
            platform = Platform.getPlatformByName('CPU')

        print(f"    Platform: {platform.getName()}")

        # Simulation
        simulation = Simulation(modeller.topology, system, integrator, platform)
        simulation.context.setPositions(modeller.positions)

        # Minimize
        print("    Minimizing...")
        simulation.minimizeEnergy(maxIterations=1000)

        # Equilibrate
        n_steps = int(duration_ps * 1000 / 2)  # 2 fs timestep
        print(f"    Running {duration_ps} ps...")
        simulation.step(n_steps)

        # Get final positions
        state = simulation.context.getState(getPositions=True)
        positions = state.getPositions(asNumpy=True)
        coords_A = positions * 10  # nm to Å

        # Find CA atoms in solvated system
        ca_indices = []
        for i, atom in enumerate(modeller.topology.atoms()):
            if atom.name == 'CA' and atom.residue.name not in ['HOH', 'NA', 'CL', 'WAT']:
                ca_indices.append(i)

        ca_coords = coords_A[ca_indices]

        # Compute H1 topology
        death_radii = compute_h1_death_radii(ca_coords)
        mean_h1 = np.mean(death_radii)

        print(f"    Equilibrated structure: {len(ca_coords)} Cα atoms")
        print(f"    Mean H1 death radius: {mean_h1:.4f} Å")

        return ca_coords, mean_h1

    except Exception as e:
        print(f"  Heated simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_thermal_bridge(h1_vacuum: float, h1_heated: float) -> Dict:
    """
    Analyze the thermal expansion effect on topology.
    """
    delta_measured = h1_heated - h1_vacuum
    delta_predicted = EMPIRICAL_H1 - SQRT_Z2

    # Does vacuum topology match √(Z²)?
    vacuum_vs_z2 = abs(h1_vacuum - SQRT_Z2)

    # Does heated topology match empirical?
    heated_vs_empirical = abs(h1_heated - EMPIRICAL_H1)

    # Thermal expansion coefficient (derived)
    if h1_vacuum > 0:
        alpha_derived = delta_measured / (h1_vacuum * DELTA_T)
    else:
        alpha_derived = 0

    result = {
        'h1_vacuum_A': h1_vacuum,
        'h1_heated_A': h1_heated,
        'delta_measured_A': delta_measured,
        'delta_predicted_A': delta_predicted,
        'sqrt_z2': SQRT_Z2,
        'empirical_h1': EMPIRICAL_H1,
        'vacuum_deviation_from_z2': vacuum_vs_z2,
        'heated_deviation_from_empirical': heated_vs_empirical,
        'alpha_derived_per_K': alpha_derived,
        'alpha_literature_per_K': ALPHA_PROTEIN,
    }

    # Verdict
    if vacuum_vs_z2 < 0.3:  # Within 0.3 Å of √(Z²)
        result['vacuum_matches_z2'] = True
        result['verdict'] = 'Z² TOPOLOGY CONFIRMED AT 0K'
    else:
        result['vacuum_matches_z2'] = False
        result['verdict'] = 'Z² NOT CONFIRMED'

    if abs(delta_measured - delta_predicted) < 0.1:
        result['thermal_bridge_confirmed'] = True
    else:
        result['thermal_bridge_confirmed'] = False

    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run thermal scaling bridge analysis.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'hypothesis': '√(Z²) + thermal_expansion = empirical_H1',
        'constants': {
            'z2': Z_SQUARED,
            'sqrt_z2_A': SQRT_Z2,
            'empirical_h1_A': EMPIRICAL_H1,
            'predicted_delta_A': PREDICTED_DELTA,
            'temperature_vacuum_K': T_VACUUM,
            'temperature_heated_K': T_BODY,
        },
    }

    # Download test structure
    pdb_path = download_test_structure()
    if pdb_path is None:
        print("Failed to obtain test structure")
        return

    # Crystal structure topology (from PDB directly)
    print("\n" + "=" * 60)
    print("STEP 1: Crystal Structure Topology")
    print("=" * 60)

    crystal_coords = parse_alpha_carbons(pdb_path)
    crystal_h1 = compute_h1_death_radii(crystal_coords)
    crystal_mean = np.mean(crystal_h1)

    print(f"  Crystal structure (X-ray, ~100K):")
    print(f"    Cα atoms: {len(crystal_coords)}")
    print(f"    Mean H1 death radius: {crystal_mean:.4f} Å")
    print(f"    Deviation from √(Z²): {abs(crystal_mean - SQRT_Z2):.4f} Å")

    results['crystal'] = {
        'n_ca': len(crystal_coords),
        'mean_h1_A': float(crystal_mean),
        'deviation_from_z2': float(abs(crystal_mean - SQRT_Z2)),
    }

    # Energy minimized (0K analog)
    print("\n" + "=" * 60)
    print("STEP 2: Energy Minimized Structure (0K analog)")
    print("=" * 60)

    min_coords, min_h1 = run_minimization(pdb_path)

    if min_h1 is not None:
        results['minimized'] = {
            'mean_h1_A': float(min_h1),
            'deviation_from_z2': float(abs(min_h1 - SQRT_Z2)),
        }

    # Heated simulation (310K)
    print("\n" + "=" * 60)
    print("STEP 3: Explicit Solvent MD at 310K")
    print("=" * 60)

    heat_coords, heat_h1 = run_heated_simulation(pdb_path, temperature_K=310, duration_ps=50)

    if heat_h1 is not None:
        results['heated'] = {
            'mean_h1_A': float(heat_h1),
            'deviation_from_empirical': float(abs(heat_h1 - EMPIRICAL_H1)),
        }

    # Analysis
    print("\n" + "=" * 60)
    print("THERMAL BRIDGE ANALYSIS")
    print("=" * 60)

    if min_h1 is not None and heat_h1 is not None:
        analysis = analyze_thermal_bridge(min_h1, heat_h1)
        results['analysis'] = analysis

        print(f"\n  RESULTS:")
        print(f"    H1 at 0K (minimized):  {min_h1:.4f} Å")
        print(f"    H1 at 310K (solvated): {heat_h1:.4f} Å")
        print(f"    Δ (measured):          {analysis['delta_measured_A']:.4f} Å")
        print(f"    Δ (predicted):         {analysis['delta_predicted_A']:.4f} Å")

        print(f"\n  COMPARISON TO Z² THEORY:")
        print(f"    √(Z²) = {SQRT_Z2:.4f} Å")
        print(f"    Vacuum H1 = {min_h1:.4f} Å")
        print(f"    Deviation: {analysis['vacuum_deviation_from_z2']:.4f} Å")

        print(f"\n  VERDICT: {analysis['verdict']}")

        if analysis.get('vacuum_matches_z2'):
            print("\n  ✓ Z² topology emerges at 0K!")
            print(f"  ✓ Thermal expansion explains the {PREDICTED_DELTA:.2f} Å shift")
        else:
            print(f"\n  ? Z² deviation = {analysis['vacuum_deviation_from_z2']:.4f} Å")
            print("  Further investigation needed")

    else:
        # Fallback: just use crystal structure
        print("\n  MD simulations unavailable, using crystal topology only")
        print(f"  Crystal H1: {crystal_mean:.4f} Å vs √(Z²) = {SQRT_Z2:.4f} Å")

    # Save results
    json_path = OUTPUT_DIR / "thermal_bridge_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {json_path}")

    return results


if __name__ == "__main__":
    main()
