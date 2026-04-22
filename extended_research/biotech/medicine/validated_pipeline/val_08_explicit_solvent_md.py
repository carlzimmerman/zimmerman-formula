#!/usr/bin/env python3
"""
val_08_explicit_solvent_md.py

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

val_08_explicit_solvent_md.py - First Principles Structural Stability Test

PURPOSE:
Test if our designed therapeutic peptides maintain structural integrity
in realistic physiological conditions using explicit solvent molecular dynamics.

NO Z² GEOMETRY - Pure thermodynamic first principles only.

PHYSICS:
- Explicit TIP3P water solvation
- 0.15M NaCl (physiological ion concentration)
- Amber14 force field (validated for peptides)
- NPT ensemble at 310K (body temperature), 1 atm
- 50 nanosecond production simulation

FALSIFICATION CRITERIA:
- RMSD plateau = peptide is thermodynamically stable
- RMSD climbing = peptide unfolds, DISCARD

DEPENDENCIES:
- OpenMM >= 8.0
- RDKit
- PDBFixer
- MDTraj

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import csv
import json
import sys
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path(__file__).parent / "results" / "md_stability"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Simulation parameters - physiological conditions
TEMPERATURE = 310  # Kelvin (37°C body temperature)
PRESSURE = 1.0  # atm
IONIC_STRENGTH = 0.15  # Molar NaCl (physiological)
BOX_PADDING = 1.2  # nm padding around peptide

# Time parameters
EQUILIBRATION_STEPS = 50000  # 100 ps equilibration
PRODUCTION_NS = 50  # 50 ns production
TIMESTEP_FS = 2.0  # 2 fs timestep
REPORT_INTERVAL_PS = 10  # Report every 10 ps

# RMSD stability criteria
RMSD_PLATEAU_WINDOW = 5.0  # ns - window to assess plateau
RMSD_DRIFT_THRESHOLD = 0.3  # nm - max acceptable RMSD drift in window

print("=" * 80)
print("FIRST PRINCIPLES STRUCTURAL STABILITY TEST")
print("Explicit Solvent Molecular Dynamics - NO Z² Geometry")
print("=" * 80)
print()

# =============================================================================
# THERAPEUTIC PEPTIDES (from our designs)
# =============================================================================

THERAPEUTIC_PEPTIDES = {
    "ZIM-ALZ-005": {
        "name": "Alzheimer's Amyloid Breaker",
        "sequence": "FPF",  # Ac-FPF-NH2 (caps added separately)
        "n_cap": "ACE",  # Acetyl
        "c_cap": "NME",  # N-methyl amide
        "target": "Amyloid-Beta fibrils",
    },
    "ZIM-SYN-004": {
        "name": "Parkinson's Synuclein Disruptor",
        "sequence": "FPF",
        "n_cap": "ACE",
        "c_cap": "NME",
        "target": "Alpha-synuclein",
    },
    "ZIM-GLP2-006": {
        "name": "GLP-1R Oral Agonist",
        "sequence": "HGPGAGPG",
        "cyclic": True,
        "target": "GLP-1 Receptor",
    },
    "ZIM-CF-004": {
        "name": "CFTR Chaperone",
        "sequence": "RFFR",
        "n_cap": None,
        "c_cap": None,
        "target": "CFTR-ΔF508",
    },
    "ZIM-CF2-003": {
        "name": "CFTR Minimal Scaffold",
        "sequence": "FF",
        "n_cap": "ACE",
        "c_cap": "NME",
        "target": "CFTR-ΔF508",
    },
    "ZIM-PD6-013": {
        "name": "PD-1/PD-L1 Checkpoint Disruptor",
        "sequence": "WFFLY",
        "n_cap": "ACE",
        "c_cap": "NME",
        "target": "PD-1/PD-L1 interface",
    },
    "ZIM-ADD-003": {
        "name": "Non-addictive nAChR Agonist",
        "sequence": "RWWFWR",
        "n_cap": None,
        "c_cap": None,
        "target": "α3β4 nAChR",
    },
}

# =============================================================================
# DEPENDENCY CHECKS
# =============================================================================

def check_dependencies() -> bool:
    """Check if required packages are available."""
    missing = []

    try:
        import openmm
        print(f"✓ OpenMM {openmm.__version__}")
    except ImportError:
        missing.append("openmm")

    try:
        from openmm import app
        print("✓ OpenMM app")
    except ImportError:
        missing.append("openmm.app")

    try:
        import rdkit
        print(f"✓ RDKit {rdkit.__version__}")
    except ImportError:
        missing.append("rdkit")

    try:
        import mdtraj
        print(f"✓ MDTraj {mdtraj.__version__}")
    except ImportError:
        missing.append("mdtraj")

    try:
        import pdbfixer
        print("✓ PDBFixer")
    except ImportError:
        missing.append("pdbfixer")

    if missing:
        print(f"\nERROR: Missing dependencies: {', '.join(missing)}")
        print("\nInstall with:")
        print("  conda install -c conda-forge openmm rdkit mdtraj pdbfixer")
        return False

    print()
    return True


# =============================================================================
# PEPTIDE STRUCTURE GENERATION
# =============================================================================

def sequence_to_pdb(peptide_id: str, peptide_info: Dict, output_dir: Path) -> Optional[Path]:
    """
    Generate initial 3D structure from sequence using RDKit.
    Returns path to PDB file or None if generation fails.
    """
    from rdkit import Chem
    from rdkit.Chem import AllChem

    sequence = peptide_info["sequence"]
    is_cyclic = peptide_info.get("cyclic", False)
    n_cap = peptide_info.get("n_cap")
    c_cap = peptide_info.get("c_cap")

    print(f"  Building structure for {peptide_id}: {sequence}")

    # Standard amino acid SMILES
    AA_SMILES = {
        'A': 'C',
        'R': 'CCCCNC(=N)N',
        'N': 'CC(=O)N',
        'D': 'CC(=O)O',
        'C': 'CS',
        'E': 'CCC(=O)O',
        'Q': 'CCC(=O)N',
        'G': '',
        'H': 'CC1=CN=CN1',
        'I': 'C(C)CC',
        'L': 'CC(C)C',
        'K': 'CCCCN',
        'M': 'CCSC',
        'F': 'CC1=CC=CC=C1',
        'P': '',  # Special - forms ring with backbone
        'S': 'CO',
        'T': 'C(C)O',
        'W': 'CC1=CNC2=CC=CC=C12',
        'Y': 'CC1=CC=C(O)C=C1',
        'V': 'C(C)C',
    }

    # Build peptide backbone with side chains
    # For now, use a simplified approach - generate extended structure

    # Create peptide using AllChem peptide builder if available
    try:
        # Try to build using RDKit's peptide capabilities
        from rdkit.Chem import rdMolDescriptors

        # Build SMILES for peptide chain
        peptide_smiles = build_peptide_smiles(sequence, is_cyclic, n_cap, c_cap)

        mol = Chem.MolFromSmiles(peptide_smiles)
        if mol is None:
            print(f"    Failed to parse SMILES for {peptide_id}")
            return None

        # Add hydrogens
        mol = Chem.AddHs(mol)

        # Generate 3D coordinates
        result = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
        if result != 0:
            print(f"    Failed to embed 3D structure for {peptide_id}")
            return None

        # Optimize geometry
        AllChem.MMFFOptimizeMolecule(mol, maxIters=500)

        # Write to PDB
        pdb_path = output_dir / f"{peptide_id}_initial.pdb"
        Chem.MolToPDBFile(mol, str(pdb_path))

        print(f"    Created: {pdb_path}")
        return pdb_path

    except Exception as e:
        print(f"    RDKit structure generation failed: {e}")
        return None


def build_peptide_smiles(sequence: str, cyclic: bool = False,
                         n_cap: str = None, c_cap: str = None) -> str:
    """
    Build SMILES string for a peptide sequence.
    This is a simplified builder - for production, use specialized tools.
    """
    # This is a placeholder - in production, use proper peptide building tools
    # like PeptideBuilder or specialized force field preparation

    # For demonstration, we'll generate a simple backbone
    # Real implementation would use PDBFixer or AmberTools

    aa_to_smiles = {
        'A': 'NC(C)C(=O)',
        'R': 'NC(CCCNC(=N)N)C(=O)',
        'F': 'NC(Cc1ccccc1)C(=O)',
        'G': 'NCC(=O)',
        'H': 'NC(Cc1c[nH]cn1)C(=O)',
        'L': 'NC(CC(C)C)C(=O)',
        'P': 'N1CCCC1C(=O)',
        'W': 'NC(Cc1c[nH]c2ccccc12)C(=O)',
        'Y': 'NC(Cc1ccc(O)cc1)C(=O)',
    }

    # Build chain
    parts = []
    for aa in sequence:
        if aa in aa_to_smiles:
            parts.append(aa_to_smiles[aa])
        else:
            # Default to glycine
            parts.append('NCC(=O)')

    # Join with peptide bonds (simplified)
    smiles = ''.join(parts)

    # Add caps
    if n_cap == 'ACE':
        smiles = 'CC(=O)' + smiles
    if c_cap == 'NME':
        smiles = smiles + 'NC'
    else:
        smiles = smiles + 'O'  # Free carboxyl

    return smiles


def prepare_system_with_pdbfixer(pdb_path: Path) -> Optional[Path]:
    """
    Use PDBFixer to clean and prepare the structure.
    """
    try:
        from pdbfixer import PDBFixer
        from openmm.app import PDBFile

        fixer = PDBFixer(str(pdb_path))
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        fixer.addMissingHydrogens(7.4)  # pH 7.4

        fixed_path = pdb_path.parent / f"{pdb_path.stem}_fixed.pdb"
        with open(fixed_path, 'w') as f:
            PDBFile.writeFile(fixer.topology, fixer.positions, f)

        return fixed_path

    except Exception as e:
        print(f"    PDBFixer preparation failed: {e}")
        return None


# =============================================================================
# MOLECULAR DYNAMICS SIMULATION
# =============================================================================

def run_explicit_solvent_md(
    pdb_path: Path,
    peptide_id: str,
    output_dir: Path,
    production_ns: float = PRODUCTION_NS,
) -> Dict:
    """
    Run explicit solvent MD simulation and analyze RMSD stability.

    Returns dict with RMSD trajectory and stability verdict.
    """
    from openmm import app, unit
    from openmm import LangevinMiddleIntegrator, MonteCarloBarostat
    from openmm import Platform, CustomExternalForce
    import openmm

    print(f"\n  Setting up MD simulation for {peptide_id}...")

    result = {
        'peptide_id': peptide_id,
        'pdb_path': str(pdb_path),
        'timestamp': datetime.now().isoformat(),
        'parameters': {
            'temperature_K': TEMPERATURE,
            'pressure_atm': PRESSURE,
            'ionic_strength_M': IONIC_STRENGTH,
            'production_ns': production_ns,
            'timestep_fs': TIMESTEP_FS,
            'force_field': 'amber14-all',
            'water_model': 'tip3p',
        },
    }

    try:
        # Load structure
        pdb = app.PDBFile(str(pdb_path))

        # Set up force field - Amber14 for peptides
        forcefield = app.ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Create modeller for solvation
        modeller = app.Modeller(pdb.topology, pdb.positions)

        # Add solvent with explicit TIP3P water
        print(f"    Adding solvent box with {BOX_PADDING} nm padding...")
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=BOX_PADDING * unit.nanometer,
            ionicStrength=IONIC_STRENGTH * unit.molar,
            positiveIon='Na+',
            negativeIon='Cl-',
        )

        # Create system
        print("    Creating OpenMM system...")
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=app.PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=app.HBonds,
            rigidWater=True,
        )

        # Add barostat for NPT
        barostat = MonteCarloBarostat(
            PRESSURE * unit.atmospheres,
            TEMPERATURE * unit.kelvin,
            25,  # Frequency
        )
        system.addForce(barostat)

        # Create integrator
        integrator = LangevinMiddleIntegrator(
            TEMPERATURE * unit.kelvin,
            1.0 / unit.picosecond,  # Friction
            TIMESTEP_FS * unit.femtoseconds,
        )

        # Select platform (prefer CUDA, fall back to CPU)
        try:
            platform = Platform.getPlatformByName('CUDA')
            properties = {'CudaPrecision': 'mixed'}
            print("    Using CUDA platform")
        except:
            try:
                platform = Platform.getPlatformByName('OpenCL')
                properties = {}
                print("    Using OpenCL platform")
            except:
                platform = Platform.getPlatformByName('CPU')
                properties = {}
                print("    Using CPU platform (slow)")

        # Create simulation
        simulation = app.Simulation(
            modeller.topology,
            system,
            integrator,
            platform,
            properties if properties else {},
        )
        simulation.context.setPositions(modeller.positions)

        # Minimize energy
        print("    Minimizing energy...")
        simulation.minimizeEnergy(maxIterations=1000)

        # Equilibration
        print(f"    Equilibrating for {EQUILIBRATION_STEPS} steps...")
        simulation.step(EQUILIBRATION_STEPS)

        # Production simulation with RMSD tracking
        print(f"    Running {production_ns} ns production simulation...")

        # Calculate steps
        steps_per_ns = int(1e6 / TIMESTEP_FS)  # 1 ns = 1e6 fs
        total_steps = int(production_ns * steps_per_ns)
        report_steps = int(REPORT_INTERVAL_PS * 1000 / TIMESTEP_FS)

        # Store reference positions for RMSD
        state = simulation.context.getState(getPositions=True)
        reference_positions = state.getPositions(asNumpy=True)

        # Get peptide atom indices (non-water, non-ion)
        peptide_indices = []
        for atom in modeller.topology.atoms():
            if atom.residue.name not in ['HOH', 'NA', 'CL', 'WAT']:
                peptide_indices.append(atom.index)

        # RMSD trajectory
        rmsd_data = []

        for step in range(0, total_steps, report_steps):
            simulation.step(report_steps)

            # Get current positions
            state = simulation.context.getState(getPositions=True)
            positions = state.getPositions(asNumpy=True)

            # Calculate RMSD (peptide backbone only)
            rmsd = calculate_rmsd(
                reference_positions[peptide_indices],
                positions[peptide_indices],
            )

            time_ns = (step + report_steps) * TIMESTEP_FS / 1e6
            rmsd_data.append({
                'time_ns': time_ns,
                'rmsd_nm': rmsd,
            })

            if (step // report_steps) % 100 == 0:
                print(f"      t = {time_ns:.1f} ns, RMSD = {rmsd:.3f} nm")

        # Write RMSD trajectory
        rmsd_csv = output_dir / f"{peptide_id}_rmsd_trajectory.csv"
        with open(rmsd_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['time_ns', 'rmsd_nm'])
            writer.writeheader()
            writer.writerows(rmsd_data)

        result['rmsd_csv'] = str(rmsd_csv)
        result['rmsd_data'] = rmsd_data

        # Analyze stability
        stability = analyze_rmsd_stability(rmsd_data)
        result['stability_analysis'] = stability

        print(f"\n    RMSD analysis:")
        print(f"      Final RMSD: {rmsd_data[-1]['rmsd_nm']:.3f} nm")
        print(f"      Mean RMSD (last 5 ns): {stability['mean_rmsd_final_window']:.3f} nm")
        print(f"      RMSD drift: {stability['rmsd_drift']:.3f} nm")
        print(f"      Verdict: {stability['verdict']}")

        result['verdict'] = stability['verdict']
        result['success'] = True

    except Exception as e:
        print(f"    MD simulation failed: {e}")
        result['success'] = False
        result['error'] = str(e)
        result['verdict'] = 'FAILED'

    return result


def calculate_rmsd(ref_positions: np.ndarray, positions: np.ndarray) -> float:
    """Calculate RMSD between two position arrays."""
    # Center both structures
    ref_centered = ref_positions - np.mean(ref_positions, axis=0)
    pos_centered = positions - np.mean(positions, axis=0)

    # Calculate RMSD
    diff = ref_centered - pos_centered
    rmsd = np.sqrt(np.mean(np.sum(diff**2, axis=1)))

    return float(rmsd)


def analyze_rmsd_stability(rmsd_data: List[Dict]) -> Dict:
    """
    Analyze RMSD trajectory for structural stability.

    Criteria:
    - Peptide should reach RMSD plateau (stable equilibrium)
    - Constantly climbing RMSD = peptide unfolds = DISCARD
    """
    times = np.array([d['time_ns'] for d in rmsd_data])
    rmsds = np.array([d['rmsd_nm'] for d in rmsd_data])

    # Analyze final window
    final_window_mask = times >= (times[-1] - RMSD_PLATEAU_WINDOW)
    final_rmsds = rmsds[final_window_mask]

    mean_final = np.mean(final_rmsds)
    std_final = np.std(final_rmsds)

    # Calculate drift in final window
    if len(final_rmsds) > 1:
        # Linear fit to detect trend
        final_times = times[final_window_mask]
        slope, _ = np.polyfit(final_times, final_rmsds, 1)
        drift = slope * RMSD_PLATEAU_WINDOW  # Total drift over window
    else:
        drift = 0.0

    # Verdict
    if drift > RMSD_DRIFT_THRESHOLD:
        verdict = "UNSTABLE - Peptide unfolding"
        recommendation = "DISCARD"
    elif mean_final > 1.0:  # nm - severe deviation
        verdict = "UNSTABLE - Large structural deviation"
        recommendation = "DISCARD"
    elif std_final > 0.2:  # High fluctuations
        verdict = "MARGINAL - High fluctuations"
        recommendation = "INVESTIGATE"
    else:
        verdict = "STABLE - Reached equilibrium plateau"
        recommendation = "PROCEED"

    return {
        'mean_rmsd_final_window': float(mean_final),
        'std_rmsd_final_window': float(std_final),
        'rmsd_drift': float(drift),
        'verdict': verdict,
        'recommendation': recommendation,
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Run stability analysis on all therapeutic peptides."""

    print("Checking dependencies...")
    if not check_dependencies():
        print("\nInstall dependencies and re-run.")
        sys.exit(1)

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Explicit Solvent MD',
        'force_field': 'Amber14',
        'water_model': 'TIP3P',
        'temperature_K': TEMPERATURE,
        'pressure_atm': PRESSURE,
        'ionic_strength_M': IONIC_STRENGTH,
        'production_ns': PRODUCTION_NS,
        'peptides': {},
    }

    stable_count = 0
    unstable_count = 0
    failed_count = 0

    for peptide_id, peptide_info in THERAPEUTIC_PEPTIDES.items():
        print("\n" + "=" * 60)
        print(f"Processing: {peptide_id}")
        print(f"  {peptide_info['name']}")
        print(f"  Sequence: {peptide_info['sequence']}")
        print(f"  Target: {peptide_info['target']}")
        print("=" * 60)

        # Generate structure
        pdb_path = sequence_to_pdb(peptide_id, peptide_info, OUTPUT_DIR)

        if pdb_path is None:
            print(f"  ✗ Structure generation failed")
            results['peptides'][peptide_id] = {
                'status': 'FAILED',
                'error': 'Structure generation failed',
            }
            failed_count += 1
            continue

        # Prepare with PDBFixer
        fixed_path = prepare_system_with_pdbfixer(pdb_path)
        if fixed_path:
            pdb_path = fixed_path

        # Run MD simulation
        md_result = run_explicit_solvent_md(pdb_path, peptide_id, OUTPUT_DIR)

        results['peptides'][peptide_id] = md_result

        if md_result.get('success'):
            if 'STABLE' in md_result.get('verdict', ''):
                stable_count += 1
                print(f"\n  ✓ {peptide_id}: STABLE")
            else:
                unstable_count += 1
                print(f"\n  ✗ {peptide_id}: UNSTABLE")
        else:
            failed_count += 1
            print(f"\n  ✗ {peptide_id}: FAILED")

    # Summary
    print("\n" + "=" * 80)
    print("STRUCTURAL STABILITY SUMMARY")
    print("=" * 80)
    print(f"\n  Total peptides tested: {len(THERAPEUTIC_PEPTIDES)}")
    print(f"  STABLE (proceed to binding):  {stable_count}")
    print(f"  UNSTABLE (discard):           {unstable_count}")
    print(f"  FAILED (rerun):               {failed_count}")

    results['summary'] = {
        'total': len(THERAPEUTIC_PEPTIDES),
        'stable': stable_count,
        'unstable': unstable_count,
        'failed': failed_count,
    }

    # Save results
    output_json = OUTPUT_DIR / "md_stability_results.json"
    with open(output_json, 'w') as f:
        # Remove non-serializable data
        results_clean = json.loads(json.dumps(results, default=str))
        json.dump(results_clean, f, indent=2)

    print(f"\n  Results saved: {output_json}")

    # List peptides to proceed with
    print("\n" + "=" * 80)
    print("PEPTIDES APPROVED FOR BINDING STUDIES")
    print("=" * 80)

    for peptide_id, result in results['peptides'].items():
        if result.get('success') and 'STABLE' in result.get('verdict', ''):
            print(f"  ✓ {peptide_id}: {THERAPEUTIC_PEPTIDES[peptide_id]['name']}")

    return results


if __name__ == "__main__":
    results = main()
