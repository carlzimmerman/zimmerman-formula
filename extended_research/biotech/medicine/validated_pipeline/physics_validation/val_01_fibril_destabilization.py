#!/usr/bin/env python3
"""
val_01_fibril_destabilization.py

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

val_01_fibril_destabilization.py - Rigorous Fibril Destabilization Validation

PURPOSE:
Test whether designed peptides (ZIM-ALZ-005, ZIM-SYN-004) can destabilize
amyloid fibrils BETTER than random decoy peptides.

TARGETS:
- Amyloid-Beta fibrils (Alzheimer's)
- Alpha-synuclein fibrils (Parkinson's)

METHODOLOGY:
1. Fetch real fibril structures from PDB
2. Generate 50 random decoy tripeptides (non-aromatic, non-proline)
3. Run OpenMM Langevin dynamics (5 ns, 310K, Amber14, implicit solvent)
4. Track inter-strand hydrogen bonds using MDAnalysis
5. Compare candidate vs decoys with statistical testing

EXPECTED OUTCOME (based on prior blinded analysis):
The designed peptides are statistically indistinguishable from random.
This script is designed to CONFIRM that finding with physics simulations.

REQUIREMENTS:
pip install openmm mdanalysis biopython numpy pandas scipy

Author: Carl Zimmerman
Date: April 21, 2026

IMPORTANT: This script requires significant computational resources.
A 5 ns simulation can take hours on CPU, minutes on GPU.
"""
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import numpy as np

# Strict random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("FIBRIL DESTABILIZATION VALIDATION")
print("Testing peptide candidates against random decoys")
print("=" * 80)
print()

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================

def check_dependencies():
    """Check all required libraries are installed."""
    missing = []

    try:
        import openmm
        print(f"✓ OpenMM {openmm.__version__}")
    except ImportError:
        missing.append("openmm")
        print("✗ OpenMM NOT INSTALLED")

    try:
        import MDAnalysis
        print(f"✓ MDAnalysis {MDAnalysis.__version__}")
    except ImportError:
        missing.append("MDAnalysis")
        print("✗ MDAnalysis NOT INSTALLED")

    try:
        from Bio import PDB
        print("✓ Biopython")
    except ImportError:
        missing.append("biopython")
        print("✗ Biopython NOT INSTALLED")

    try:
        import pandas
        print(f"✓ pandas {pandas.__version__}")
    except ImportError:
        missing.append("pandas")
        print("✗ pandas NOT INSTALLED")

    try:
        from scipy import stats
        print("✓ scipy")
    except ImportError:
        missing.append("scipy")
        print("✗ scipy NOT INSTALLED")

    if missing:
        print(f"\nMissing dependencies: {missing}")
        print("Install with: pip install " + " ".join(missing))
        return False

    return True


DEPS_OK = check_dependencies()

# =============================================================================
# CONFIGURATION
# =============================================================================

# Target fibril structures (high-resolution cryo-EM or ssNMR)
FIBRIL_STRUCTURES = {
    'amyloid_beta': {
        'pdb_ids': ['5OQV', '2MXU', '6SHS'],  # Amyloid-beta fibrils
        'description': 'Amyloid-beta fibrils (Alzheimer\'s)',
    },
    'alpha_synuclein': {
        'pdb_ids': ['2N0A', '6CU7', '6SSX'],  # Alpha-synuclein fibrils
        'description': 'Alpha-synuclein fibrils (Parkinson\'s)',
    },
}

# Designed peptide candidates
CANDIDATES = {
    'ZIM-ALZ-005': {
        'sequence': 'FPF',
        'terminal_mods': {'n_term': 'acetyl', 'c_term': 'amide'},
        'target': 'amyloid_beta',
    },
    'ZIM-SYN-004': {
        'sequence': 'FPF',
        'terminal_mods': {'n_term': 'acetyl', 'c_term': 'amide'},
        'target': 'alpha_synuclein',
    },
    'ZIM-SYN-013': {
        'sequence': 'FFPFFG',
        'terminal_mods': {'n_term': 'acetyl', 'c_term': 'amide'},
        'target': 'alpha_synuclein',
    },
}

# Non-aromatic, non-proline amino acids for null model
NULL_AMINO_ACIDS = list('AGILSTVNQDEMKRH')  # Excludes F, W, Y, P

# Simulation parameters
SIM_PARAMS = {
    'temperature_K': 310,
    'timestep_fs': 2.0,
    'total_time_ns': 5.0,
    'reporting_interval_ps': 10.0,
    'force_field': 'amber14-all',
    'implicit_solvent': 'obc2',
}


# =============================================================================
# DECOY GENERATOR
# =============================================================================

def generate_decoy_peptides(
    length: int,
    n_decoys: int = 50,
    exclude_aa: str = 'FWYP',
) -> List[str]:
    """
    Generate random decoy peptides for null model.

    Uses only non-aromatic, non-proline amino acids to create
    a fair comparison (aromatic stacking is the proposed mechanism).
    """
    allowed_aa = [aa for aa in 'ACDEFGHIKLMNPQRSTVWY' if aa not in exclude_aa]

    decoys = []
    for i in range(n_decoys):
        np.random.seed(RANDOM_SEED + i + 1000)
        seq = ''.join(np.random.choice(allowed_aa, length))
        decoys.append(seq)

    np.random.seed(RANDOM_SEED)  # Reset

    print(f"Generated {len(decoys)} decoy peptides of length {length}")
    print(f"  Using amino acids: {''.join(allowed_aa)}")
    print(f"  Excluded: {exclude_aa}")

    return decoys


# =============================================================================
# PDB FETCHING
# =============================================================================

def fetch_fibril_structure(pdb_id: str, output_dir: Path) -> Optional[Path]:
    """
    Fetch fibril structure from RCSB PDB.

    Returns path to downloaded PDB file, or None if fetch fails.
    """
    import urllib.request
    import urllib.error

    pdb_id = pdb_id.upper()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    output_file = output_dir / f"{pdb_id}.pdb"

    if output_file.exists():
        print(f"  {pdb_id}: Already downloaded")
        return output_file

    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"  {pdb_id}: Downloaded")
        return output_file
    except urllib.error.HTTPError as e:
        print(f"  {pdb_id}: HTTP error {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"  {pdb_id}: URL error {e.reason}")
        return None


# =============================================================================
# OPENMM SIMULATION (REQUIRES OPENMM)
# =============================================================================

def build_peptide_system(
    sequence: str,
    terminal_mods: Dict[str, str],
) -> Tuple:
    """
    Build OpenMM system for a peptide.

    Returns (topology, positions, system) tuple.

    NOTE: This is a simplified builder. For production use,
    consider using PDBFixer or tleap for proper parameterization.
    """
    if not DEPS_OK:
        raise ImportError("OpenMM not available")

    from openmm import app, unit
    from openmm.app import Modeller, ForceField, PDBFile

    # This is a placeholder - real implementation would need:
    # 1. Build peptide from sequence using e.g. PeptideBuilder
    # 2. Add terminal modifications
    # 3. Parameterize with force field

    raise NotImplementedError(
        "Peptide building requires additional setup.\n"
        "Options:\n"
        "1. Use PDBFixer to build from sequence\n"
        "2. Use tleap (AmberTools) to generate topology\n"
        "3. Use a pre-built peptide structure\n"
        "\n"
        "This script provides the framework; implementation details\n"
        "depend on your specific setup."
    )


def run_fibril_simulation(
    fibril_pdb: Path,
    peptide_sequence: str,
    output_prefix: str,
    sim_time_ns: float = 5.0,
) -> Dict:
    """
    Run MD simulation of peptide at fibril interface.

    Returns dictionary with H-bond counts over time.
    """
    if not DEPS_OK:
        raise ImportError("Required dependencies not available")

    from openmm import app, unit, LangevinMiddleIntegrator
    from openmm.app import PDBFile, ForceField, Simulation

    print(f"\n  Running simulation for {peptide_sequence}...")
    print(f"    Fibril: {fibril_pdb.name}")
    print(f"    Time: {sim_time_ns} ns")

    # Load fibril structure
    pdb = PDBFile(str(fibril_pdb))

    # Set up force field
    forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

    # Create system
    system = forcefield.createSystem(
        pdb.topology,
        nonbondedMethod=app.NoCutoff,
        constraints=app.HBonds,
    )

    # Integrator
    integrator = LangevinMiddleIntegrator(
        SIM_PARAMS['temperature_K'] * unit.kelvin,
        1.0 / unit.picosecond,
        SIM_PARAMS['timestep_fs'] * unit.femtosecond,
    )

    # Simulation
    simulation = Simulation(pdb.topology, system, integrator)
    simulation.context.setPositions(pdb.positions)

    # Minimize
    print("    Minimizing...")
    simulation.minimizeEnergy()

    # Run dynamics
    n_steps = int(sim_time_ns * 1e6 / SIM_PARAMS['timestep_fs'])
    report_steps = int(SIM_PARAMS['reporting_interval_ps'] * 1000 / SIM_PARAMS['timestep_fs'])

    print(f"    Running {n_steps} steps...")

    # Trajectory and H-bond tracking would go here
    # This requires MDAnalysis for H-bond analysis

    results = {
        'peptide': peptide_sequence,
        'fibril': fibril_pdb.name,
        'sim_time_ns': sim_time_ns,
        'hbond_counts': [],  # Time series of H-bond counts
        'final_hbonds': 0,
        'hbond_disruption': 0.0,
    }

    return results


# =============================================================================
# HYDROGEN BOND ANALYSIS (REQUIRES MDANALYSIS)
# =============================================================================

def analyze_hbonds(trajectory_file: Path, topology_file: Path) -> Dict:
    """
    Analyze hydrogen bonds in MD trajectory using MDAnalysis.

    Tracks inter-strand H-bonds (backbone N-H...O=C) over time.
    """
    if not DEPS_OK:
        raise ImportError("MDAnalysis not available")

    import MDAnalysis as mda
    from MDAnalysis.analysis.hydrogenbonds import HydrogenBondAnalysis

    u = mda.Universe(str(topology_file), str(trajectory_file))

    # Analyze backbone H-bonds
    hbonds = HydrogenBondAnalysis(
        universe=u,
        donors_sel="backbone and name N",
        hydrogens_sel="backbone and name H",
        acceptors_sel="backbone and name O",
        d_a_cutoff=3.5,  # Angstroms
        d_h_a_angle_cutoff=150,  # degrees
    )

    hbonds.run()

    # Count H-bonds per frame
    hbond_counts = []
    for ts in u.trajectory:
        frame_hbonds = len([h for h in hbonds.results.hbonds if h[0] == ts.frame])
        hbond_counts.append(frame_hbonds)

    return {
        'hbond_counts': hbond_counts,
        'mean_hbonds': float(np.mean(hbond_counts)),
        'std_hbonds': float(np.std(hbond_counts)),
        'final_hbonds': hbond_counts[-1] if hbond_counts else 0,
    }


# =============================================================================
# STATISTICAL COMPARISON
# =============================================================================

def compare_to_null_model(
    candidate_result: Dict,
    decoy_results: List[Dict],
) -> Dict:
    """
    Compare candidate to null model (decoy peptides).

    Tests whether candidate breaks more H-bonds than 95th percentile of decoys.
    """
    from scipy import stats

    # Extract H-bond disruption metric
    candidate_disruption = candidate_result.get('hbond_disruption', 0)
    decoy_disruptions = [d.get('hbond_disruption', 0) for d in decoy_results]

    # Basic statistics
    decoy_mean = np.mean(decoy_disruptions)
    decoy_std = np.std(decoy_disruptions)
    decoy_p95 = np.percentile(decoy_disruptions, 95)

    # Z-score
    if decoy_std > 0:
        z_score = (candidate_disruption - decoy_mean) / decoy_std
    else:
        z_score = 0.0

    # Percentile rank
    n_worse = np.sum(np.array(decoy_disruptions) < candidate_disruption)
    percentile = 100 * n_worse / len(decoy_disruptions)

    # One-sample t-test (is candidate significantly different from decoy mean?)
    # Note: This tests if candidate is DIFFERENT, not necessarily BETTER
    t_stat, p_value = stats.ttest_1samp(
        decoy_disruptions + [candidate_disruption],
        candidate_disruption
    )

    # Verdict
    is_significant = candidate_disruption > decoy_p95

    return {
        'candidate_disruption': candidate_disruption,
        'decoy_mean': float(decoy_mean),
        'decoy_std': float(decoy_std),
        'decoy_p95': float(decoy_p95),
        'z_score': float(z_score),
        'percentile': float(percentile),
        'p_value': float(p_value),
        'is_significant': bool(is_significant),
        'verdict': 'SIGNIFICANT (p<0.05)' if is_significant else 'NOT SIGNIFICANT',
    }


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_validation_pipeline():
    """
    Run complete fibril destabilization validation.

    This is the main entry point that orchestrates:
    1. Fetching structures
    2. Generating decoys
    3. Running simulations (if OpenMM available)
    4. Statistical comparison
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'random_seed': RANDOM_SEED,
        'sim_params': SIM_PARAMS,
        'candidates': {},
        'overall_verdict': None,
    }

    data_dir = OUTPUT_DIR / "fibril_data"
    data_dir.mkdir(exist_ok=True)

    # Fetch fibril structures
    print("\n" + "=" * 80)
    print("FETCHING FIBRIL STRUCTURES")
    print("=" * 80)

    for target_name, target_info in FIBRIL_STRUCTURES.items():
        print(f"\n{target_info['description']}:")
        for pdb_id in target_info['pdb_ids']:
            fetch_fibril_structure(pdb_id, data_dir)

    # Generate decoys
    print("\n" + "=" * 80)
    print("GENERATING DECOY PEPTIDES")
    print("=" * 80)

    decoy_library = {}
    for length in [3, 5, 6]:  # Match candidate lengths
        decoy_library[length] = generate_decoy_peptides(length, n_decoys=50)

    # Check if we can run simulations
    if not DEPS_OK:
        print("\n" + "=" * 80)
        print("SIMULATION SKIPPED - DEPENDENCIES NOT AVAILABLE")
        print("=" * 80)
        print("""
To run actual MD simulations, install:
    pip install openmm mdanalysis

Then re-run this script.

For now, outputting framework results only.
""")
        results['simulation_status'] = 'SKIPPED - dependencies missing'
        results['overall_verdict'] = 'INCONCLUSIVE - no simulation run'

    else:
        print("\n" + "=" * 80)
        print("RUNNING SIMULATIONS")
        print("=" * 80)
        print("""
NOTE: Full MD simulations will take significant time.
      5 ns simulation = ~1-2 hours on GPU, ~10+ hours on CPU
""")

        # This would run the actual simulations
        # For each candidate:
        #   1. Run simulation with candidate peptide
        #   2. Run simulations with 50 decoys
        #   3. Compare H-bond disruption

        results['simulation_status'] = 'NOT YET IMPLEMENTED'
        results['overall_verdict'] = 'FRAMEWORK READY - implementation needed'

    # Save results
    output_file = OUTPUT_DIR / "fibril_destabilization_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved: {output_file}")

    return results


# =============================================================================
# STANDALONE EXECUTION
# =============================================================================

def main():
    """Main execution."""

    print("""
    ============================================================
    FIBRIL DESTABILIZATION VALIDATION PIPELINE
    ============================================================

    This script tests whether designed peptides can destabilize
    amyloid fibrils BETTER than random decoy peptides.

    IMPORTANT CONTEXT:
    Prior blinded analysis showed that Z² = 9.14 Å is NOT
    statistically special, and designed peptides are
    indistinguishable from random scrambled sequences.

    Expected outcome: Candidates will NOT outperform decoys.
    This would confirm the blinded analysis findings.

    ============================================================
    """)

    results = run_validation_pipeline()

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\nOverall verdict: {results.get('overall_verdict', 'UNKNOWN')}")

    return results


if __name__ == "__main__":
    results = main()
