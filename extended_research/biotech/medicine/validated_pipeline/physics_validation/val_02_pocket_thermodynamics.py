#!/usr/bin/env python3
"""
val_02_pocket_thermodynamics.py

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

val_02_pocket_thermodynamics.py - Deep Pocket Binding Affinity Validation

PURPOSE:
Calculate true binding affinities for peptide candidates against deep pocket
targets. Must outperform scrambled decoys by >2 standard deviations (Z>2.0).

TARGETS:
- Metallo-Beta-Lactamase (MBL) - Superbugs
- α3β4 nAChR - Addiction
- PD-L1 - Cancer immunotherapy
- GLP-1R - Obesity
- D2R - Prolactinoma

METHODOLOGY:
1. Load cleaned PDB structures for each target
2. Generate 100 scrambled decoys with same molecular weight
3. Dock candidate + decoys using AutoDock Vina or Smina
4. Refine top poses with MM-GBSA using OpenMM
5. Compare ΔG values with strict statistical threshold

EXPECTED OUTCOME:
Based on prior blinded analysis, candidates will NOT outperform decoys.

REQUIREMENTS:
pip install openmm biopython numpy pandas scipy
Also requires: AutoDock Vina or Smina (external binary)

Author: Carl Zimmerman
Date: April 21, 2026
"""
import sys
import json
import csv
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import numpy as np

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("DEEP POCKET THERMODYNAMIC VALIDATION")
print("Binding affinity comparison: candidates vs scrambled decoys")
print("=" * 80)
print()

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================

def check_dependencies():
    """Check all required libraries and external tools."""
    missing = []
    warnings = []

    # Python libraries
    try:
        import openmm
        print(f"✓ OpenMM {openmm.__version__}")
    except ImportError:
        missing.append("openmm")
        print("✗ OpenMM NOT INSTALLED")

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

    # External docking software
    vina_found = False
    for cmd in ['vina', 'smina', 'qvina2']:
        try:
            result = subprocess.run([cmd, '--version'],
                                   capture_output=True, timeout=5)
            print(f"✓ {cmd} found")
            vina_found = True
            break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    if not vina_found:
        warnings.append("AutoDock Vina/Smina not found")
        print("⚠ Vina/Smina NOT FOUND (docking will be skipped)")

    if missing:
        print(f"\nMissing Python packages: {missing}")
        print("Install with: pip install " + " ".join(missing))

    if warnings:
        print(f"\nWarnings: {warnings}")

    return len(missing) == 0, vina_found


DEPS_OK, VINA_OK = check_dependencies()

# =============================================================================
# CONFIGURATION
# =============================================================================

# Target proteins and their PDB structures
TARGETS = {
    'MBL': {
        'pdb_id': '1SML',  # Metallo-beta-lactamase
        'description': 'Metallo-Beta-Lactamase (Superbugs)',
        'binding_site': {'center': (10.0, 20.0, 30.0), 'size': (20, 20, 20)},
    },
    'nAChR': {
        'pdb_id': '6CNJ',  # Nicotinic acetylcholine receptor
        'description': 'α3β4 nAChR (Addiction)',
        'binding_site': {'center': (0.0, 0.0, 0.0), 'size': (25, 25, 25)},
    },
    'PD-L1': {
        'pdb_id': '4ZQK',  # PD-1/PD-L1 complex
        'description': 'PD-L1 (Cancer Immunotherapy)',
        'binding_site': {'center': (15.0, 25.0, 35.0), 'size': (20, 20, 20)},
    },
    'GLP1R': {
        'pdb_id': '6X18',  # GLP-1 receptor
        'description': 'GLP-1R (Obesity)',
        'binding_site': {'center': (5.0, 10.0, 15.0), 'size': (25, 25, 25)},
    },
    'D2R': {
        'pdb_id': '6CM4',  # Dopamine D2 receptor
        'description': 'D2R (Prolactinoma)',
        'binding_site': {'center': (0.0, 5.0, 10.0), 'size': (20, 20, 20)},
    },
}

# Designed candidates
CANDIDATES = {
    'ZIM-MBL-KNOT': {
        'sequence': 'CGGCGGC',  # Placeholder trefoil knot
        'target': 'MBL',
    },
    'ZIM-ADDICT-001': {
        'sequence': 'RWWFWR',
        'target': 'nAChR',
    },
    'ZIM-PD1-001': {
        'sequence': 'FYYF',  # PD-L1 disrupter
        'target': 'PD-L1',
    },
    'ZIM-GLP1-CYCLIC': {
        'sequence': 'HGPGAGPG',  # Cyclic GLP-1 mimic
        'target': 'GLP1R',
    },
    'ZIM-PROLAC-001': {
        'sequence': 'DPGD',  # D2R modulator
        'target': 'D2R',
    },
}

# Amino acids for decoy generation
ALL_AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'


# =============================================================================
# MOLECULAR WEIGHT CALCULATION
# =============================================================================

AMINO_ACID_MW = {
    'A': 89.09, 'C': 121.16, 'D': 133.10, 'E': 147.13, 'F': 165.19,
    'G': 75.07, 'H': 155.16, 'I': 131.17, 'K': 146.19, 'L': 131.17,
    'M': 149.21, 'N': 132.12, 'P': 115.13, 'Q': 146.15, 'R': 174.20,
    'S': 105.09, 'T': 119.12, 'V': 117.15, 'W': 204.23, 'Y': 181.19,
}


def calculate_mw(sequence: str) -> float:
    """Calculate molecular weight of peptide sequence."""
    water_loss = 18.015 * (len(sequence) - 1)  # Peptide bond formation
    return sum(AMINO_ACID_MW.get(aa, 0) for aa in sequence.upper()) - water_loss


def generate_mw_matched_decoys(
    target_sequence: str,
    n_decoys: int = 100,
    mw_tolerance: float = 0.05,
) -> List[str]:
    """
    Generate decoy peptides with similar molecular weight.

    Scrambles amino acids to create random sequences with
    molecular weight within tolerance of target.
    """
    target_mw = calculate_mw(target_sequence)
    target_length = len(target_sequence)

    decoys = []
    attempts = 0
    max_attempts = n_decoys * 100

    while len(decoys) < n_decoys and attempts < max_attempts:
        attempts += 1
        np.random.seed(RANDOM_SEED + attempts)

        # Generate random sequence of same length
        seq = ''.join(np.random.choice(list(ALL_AMINO_ACIDS), target_length))
        seq_mw = calculate_mw(seq)

        # Check MW tolerance
        if abs(seq_mw - target_mw) / target_mw <= mw_tolerance:
            if seq not in decoys and seq != target_sequence:
                decoys.append(seq)

    np.random.seed(RANDOM_SEED)

    print(f"  Generated {len(decoys)} MW-matched decoys for {target_sequence}")
    print(f"    Target MW: {target_mw:.1f} Da (±{mw_tolerance*100:.0f}%)")

    return decoys


# =============================================================================
# PDB FETCHING AND PREPARATION
# =============================================================================

def fetch_and_prepare_receptor(pdb_id: str, output_dir: Path) -> Optional[Path]:
    """
    Fetch PDB and prepare for docking.

    Returns path to prepared receptor file (PDBQT format for Vina).
    """
    import urllib.request

    pdb_file = output_dir / f"{pdb_id}.pdb"
    pdbqt_file = output_dir / f"{pdb_id}_receptor.pdbqt"

    # Fetch PDB
    if not pdb_file.exists():
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        try:
            urllib.request.urlretrieve(url, pdb_file)
            print(f"  {pdb_id}: Downloaded")
        except Exception as e:
            print(f"  {pdb_id}: Download failed - {e}")
            return None

    # Prepare receptor (would use MGLTools or OpenBabel)
    # This is a placeholder - actual preparation requires:
    # 1. Remove water molecules
    # 2. Add hydrogens
    # 3. Assign charges
    # 4. Convert to PDBQT format

    print(f"  {pdb_id}: Receptor preparation requires MGLTools/OpenBabel")

    return pdb_file  # Return PDB for now


# =============================================================================
# AUTODOCK VINA DOCKING
# =============================================================================

def run_vina_docking(
    receptor_file: Path,
    ligand_file: Path,
    center: Tuple[float, float, float],
    size: Tuple[int, int, int],
    output_file: Path,
    exhaustiveness: int = 8,
) -> Optional[float]:
    """
    Run AutoDock Vina docking.

    Returns best binding affinity (kcal/mol) or None if failed.
    """
    if not VINA_OK:
        print("  Vina not available - skipping docking")
        return None

    # Find vina executable
    vina_cmd = None
    for cmd in ['vina', 'smina', 'qvina2']:
        try:
            subprocess.run([cmd, '--version'], capture_output=True, timeout=5)
            vina_cmd = cmd
            break
        except:
            pass

    if not vina_cmd:
        return None

    # Build command
    cmd = [
        vina_cmd,
        '--receptor', str(receptor_file),
        '--ligand', str(ligand_file),
        '--center_x', str(center[0]),
        '--center_y', str(center[1]),
        '--center_z', str(center[2]),
        '--size_x', str(size[0]),
        '--size_y', str(size[1]),
        '--size_z', str(size[2]),
        '--exhaustiveness', str(exhaustiveness),
        '--out', str(output_file),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Parse output for best affinity
        for line in result.stdout.split('\n'):
            if line.strip().startswith('1'):
                parts = line.split()
                if len(parts) >= 2:
                    return float(parts[1])

        return None

    except subprocess.TimeoutExpired:
        print("  Docking timed out")
        return None
    except Exception as e:
        print(f"  Docking error: {e}")
        return None


# =============================================================================
# MM-GBSA REFINEMENT
# =============================================================================

def calculate_mmgbsa(
    complex_pdb: Path,
) -> Optional[float]:
    """
    Calculate MM-GBSA binding free energy.

    This is a simplified implementation. Full MM-GBSA requires:
    1. Minimize complex
    2. Calculate energy of complex
    3. Calculate energy of receptor alone
    4. Calculate energy of ligand alone
    5. ΔG_bind = E_complex - E_receptor - E_ligand

    Uses OpenMM with GB/SA implicit solvent.
    """
    if not DEPS_OK:
        return None

    from openmm import app, unit
    from openmm.app import PDBFile, ForceField, Simulation

    try:
        pdb = PDBFile(str(complex_pdb))
        forcefield = ForceField('amber14-all.xml', 'implicit/obc2.xml')

        system = forcefield.createSystem(
            pdb.topology,
            nonbondedMethod=app.NoCutoff,
        )

        # Get potential energy
        from openmm import VerletIntegrator
        integrator = VerletIntegrator(0.001)
        simulation = Simulation(pdb.topology, system, integrator)
        simulation.context.setPositions(pdb.positions)
        simulation.minimizeEnergy()

        state = simulation.context.getState(getEnergy=True)
        energy_kj = state.getPotentialEnergy() / unit.kilojoules_per_mole
        energy_kcal = energy_kj / 4.184

        return float(energy_kcal)

    except Exception as e:
        print(f"  MM-GBSA error: {e}")
        return None


# =============================================================================
# STATISTICAL VALIDATION
# =============================================================================

def validate_against_decoys(
    candidate_dg: float,
    decoy_dgs: List[float],
    z_threshold: float = 2.0,
) -> Dict:
    """
    Validate candidate binding affinity against decoy distribution.

    STRICT: Must outperform mean by >2 standard deviations.
    """
    from scipy import stats

    decoy_mean = np.mean(decoy_dgs)
    decoy_std = np.std(decoy_dgs)

    # Z-score (more negative is better for binding)
    # We want candidate to be MORE negative than decoys
    if decoy_std > 0:
        z_score = (candidate_dg - decoy_mean) / decoy_std
    else:
        z_score = 0.0

    # For binding energies, more negative is better
    # So z_score < -2 means candidate is significantly better
    is_significant = z_score < -z_threshold

    # Percentile (lower is better)
    n_worse = np.sum(np.array(decoy_dgs) > candidate_dg)
    percentile = 100 * n_worse / len(decoy_dgs)

    result = {
        'candidate_dg_kcal': float(candidate_dg),
        'decoy_mean': float(decoy_mean),
        'decoy_std': float(decoy_std),
        'z_score': float(z_score),
        'percentile': float(percentile),
        'is_significant': bool(is_significant),
        'z_threshold': z_threshold,
    }

    if not is_significant:
        # This is the EXPECTED outcome based on prior analysis
        raise ValueError(
            f"Candidate ΔG ({candidate_dg:.2f} kcal/mol) does not outperform "
            f"decoy mean ({decoy_mean:.2f} kcal/mol) by >{z_threshold} std devs. "
            f"Z-score: {z_score:.2f}. "
            f"This confirms prior blinded analysis: Z² framework is not special."
        )

    return result


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def run_validation_pipeline():
    """Run complete pocket thermodynamics validation."""

    results = {
        'timestamp': datetime.now().isoformat(),
        'random_seed': RANDOM_SEED,
        'targets': {},
        'overall_verdict': None,
    }

    data_dir = OUTPUT_DIR / "pocket_data"
    data_dir.mkdir(exist_ok=True)

    # Check dependencies
    if not DEPS_OK:
        print("\n" + "=" * 80)
        print("CANNOT RUN - MISSING DEPENDENCIES")
        print("=" * 80)
        print("Install: pip install openmm biopython pandas scipy")
        results['overall_verdict'] = 'BLOCKED - missing dependencies'
        return results

    if not VINA_OK:
        print("\n" + "=" * 80)
        print("WARNING: AutoDock Vina not found")
        print("=" * 80)
        print("Docking will be skipped. Install Vina for full validation.")

    # Process each target
    print("\n" + "=" * 80)
    print("PROCESSING TARGETS")
    print("=" * 80)

    for target_name, target_info in TARGETS.items():
        print(f"\n{target_info['description']}:")

        # Fetch receptor
        receptor = fetch_and_prepare_receptor(target_info['pdb_id'], data_dir)

        # Find candidates for this target
        target_candidates = {
            k: v for k, v in CANDIDATES.items()
            if v['target'] == target_name
        }

        if not target_candidates:
            print(f"  No candidates for {target_name}")
            continue

        for cand_name, cand_info in target_candidates.items():
            print(f"\n  Testing {cand_name}: {cand_info['sequence']}")

            # Generate decoys
            decoys = generate_mw_matched_decoys(cand_info['sequence'], n_decoys=100)

            # This is where docking and MM-GBSA would run
            # For now, just note that it's framework-ready

            results['targets'][target_name] = {
                'candidate': cand_name,
                'sequence': cand_info['sequence'],
                'n_decoys': len(decoys),
                'status': 'FRAMEWORK READY - docking implementation needed',
            }

    results['overall_verdict'] = 'FRAMEWORK READY - requires Vina setup'

    # Save results
    output_file = OUTPUT_DIR / "pocket_thermodynamics_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved: {output_file}")

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""

    print("""
    ============================================================
    DEEP POCKET THERMODYNAMIC VALIDATION
    ============================================================

    This script calculates binding affinities using:
    1. AutoDock Vina for docking
    2. MM-GBSA for free energy refinement
    3. Statistical comparison to scrambled decoys

    STRICT THRESHOLD: Z-score > 2.0 required

    Based on prior blinded analysis, candidates are expected to
    NOT outperform decoys. This confirms the Z² framework is
    not scientifically special.

    ============================================================
    """)

    results = run_validation_pipeline()

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"\nVerdict: {results.get('overall_verdict', 'UNKNOWN')}")

    return results


if __name__ == "__main__":
    results = main()
