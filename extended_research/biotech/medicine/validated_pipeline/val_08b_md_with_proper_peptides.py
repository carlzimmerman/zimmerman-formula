#!/usr/bin/env python3
"""
val_08b_md_with_proper_peptides.py - Fixed Explicit Solvent MD

Uses proper peptide building with standard amino acid residues
that Amber force field recognizes.

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
from typing import Dict, List, Optional

OUTPUT_DIR = Path(__file__).parent / "results" / "md_stability"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Simulation parameters
TEMPERATURE = 310  # K
EQUILIBRATION_STEPS = 5000  # Reduced for testing
PRODUCTION_STEPS = 50000  # Reduced for demo (increase for real runs)
TIMESTEP_FS = 2.0
REPORT_INTERVAL = 1000

print("=" * 80)
print("EXPLICIT SOLVENT MD - PROPER PEPTIDE BUILDER")
print("=" * 80)
print()

# =============================================================================
# PEPTIDES TO TEST
# =============================================================================

PEPTIDES = {
    "ZIM-SYN-004": {
        "name": "Parkinson's Disruptor",
        "sequence": "FPF",
        "target": "Alpha-synuclein",
    },
    "ZIM-ADD-003": {
        "name": "Non-addictive nAChR Agonist",
        "sequence": "RWWFWR",
        "target": "α3β4 nAChR",
    },
    "ZIM-PD6-013": {
        "name": "Checkpoint Disruptor",
        "sequence": "WFFLY",
        "target": "PD-1/PD-L1",
    },
}

# =============================================================================
# PEPTIDE BUILDING USING MODELLER
# =============================================================================

def build_peptide_pdb(sequence: str, output_path: Path) -> bool:
    """
    Build a peptide PDB file with proper amino acid residues.
    Uses OpenMM Modeller with a template approach.
    """
    from openmm.app import PDBFile, Modeller, ForceField
    from openmm import unit
    import openmm

    # Build extended chain manually
    # We'll create a simple extended peptide structure

    # Standard amino acid templates
    aa_atoms = {
        'A': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0), ('H', -0.8, -0.8, 0.0),
              ('HA', 0.0, -0.5, 0.9), ('HB1', 0.5, 2.0, 0.0), ('HB2', -0.5, 2.0, 0.0),
              ('HB3', 0.0, 1.5, 1.0)],
        'R': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0)],
        'F': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0)],
        'P': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0)],
        'W': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0)],
        'L': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0)],
        'Y': [('N', -0.5, 0.0, 0.0), ('CA', 0.0, 0.0, 0.0), ('C', 1.5, 0.0, 0.0),
              ('O', 2.0, 1.0, 0.0), ('CB', 0.0, 1.5, 0.0)],
    }

    # Use PeptideBuilder if available, else use PDBFixer approach
    try:
        from pdbfixer import PDBFixer
        from io import StringIO

        # Create minimal PDB content with backbone
        pdb_content = "HEADER    PEPTIDE\n"

        aa_3letter = {
            'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
            'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
            'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
            'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
        }

        atom_num = 1
        for i, aa in enumerate(sequence):
            res_name = aa_3letter.get(aa, 'ALA')
            res_num = i + 1
            x_offset = i * 3.8  # ~3.8 Å between Cα atoms

            # Minimal backbone atoms
            pdb_content += f"ATOM  {atom_num:5d}  N   {res_name} A{res_num:4d}    {x_offset - 0.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           N\n"
            atom_num += 1
            pdb_content += f"ATOM  {atom_num:5d}  CA  {res_name} A{res_num:4d}    {x_offset:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
            atom_num += 1
            pdb_content += f"ATOM  {atom_num:5d}  C   {res_name} A{res_num:4d}    {x_offset + 1.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
            atom_num += 1
            pdb_content += f"ATOM  {atom_num:5d}  O   {res_name} A{res_num:4d}    {x_offset + 2.0:8.3f}{1.0:8.3f}{0.0:8.3f}  1.00  0.00           O\n"
            atom_num += 1

        pdb_content += "END\n"

        # Save initial backbone
        temp_pdb = output_path.parent / f"{output_path.stem}_backbone.pdb"
        with open(temp_pdb, 'w') as f:
            f.write(pdb_content)

        # Use PDBFixer to add missing atoms and hydrogens
        fixer = PDBFixer(str(temp_pdb))
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        fixer.addMissingHydrogens(7.4)

        # Save complete structure
        with open(output_path, 'w') as f:
            PDBFile.writeFile(fixer.topology, fixer.positions, f)

        print(f"    Built peptide: {output_path}")
        return True

    except Exception as e:
        print(f"    Peptide building failed: {e}")
        return False


# =============================================================================
# MD SIMULATION
# =============================================================================

def run_md_simulation(pdb_path: Path, peptide_id: str) -> Dict:
    """
    Run explicit solvent MD on the peptide.
    """
    from openmm.app import PDBFile, ForceField, Modeller, Simulation, PDBReporter
    from openmm.app import StateDataReporter, PME, HBonds
    from openmm import LangevinMiddleIntegrator, MonteCarloBarostat, Platform
    from openmm import unit
    import sys

    print(f"\n  Running MD simulation for {peptide_id}...")

    result = {
        'peptide_id': peptide_id,
        'timestamp': datetime.now().isoformat(),
    }

    try:
        # Load structure
        pdb = PDBFile(str(pdb_path))
        print(f"    Loaded structure: {pdb.topology.getNumAtoms()} atoms")

        # Force field
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Modeller for solvation
        modeller = Modeller(pdb.topology, pdb.positions)

        # Add solvent
        print("    Adding solvent...")
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=1.0 * unit.nanometer,
            ionicStrength=0.15 * unit.molar,
        )

        print(f"    System size: {modeller.topology.getNumAtoms()} atoms")

        # Create system
        print("    Creating system...")
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=HBonds,
        )

        # Barostat for NPT
        system.addForce(MonteCarloBarostat(
            1.0 * unit.atmospheres,
            TEMPERATURE * unit.kelvin,
        ))

        # Integrator
        integrator = LangevinMiddleIntegrator(
            TEMPERATURE * unit.kelvin,
            1.0 / unit.picosecond,
            TIMESTEP_FS * unit.femtoseconds,
        )

        # Platform
        platform = Platform.getPlatformByName('CPU')
        print(f"    Platform: {platform.getName()}")

        # Simulation
        simulation = Simulation(
            modeller.topology,
            system,
            integrator,
            platform,
        )
        simulation.context.setPositions(modeller.positions)

        # Minimize
        print("    Minimizing energy...")
        simulation.minimizeEnergy(maxIterations=500)

        # Get peptide atom indices (non-water, non-ion)
        peptide_indices = []
        for atom in modeller.topology.atoms():
            if atom.residue.name not in ['HOH', 'NA', 'CL', 'WAT']:
                peptide_indices.append(atom.index)

        # Store reference for RMSD
        state = simulation.context.getState(getPositions=True)
        ref_positions = state.getPositions(asNumpy=True)[peptide_indices]

        # Equilibration
        print(f"    Equilibrating ({EQUILIBRATION_STEPS} steps)...")
        simulation.step(EQUILIBRATION_STEPS)

        # Production with RMSD tracking
        print(f"    Production MD ({PRODUCTION_STEPS} steps)...")
        rmsd_data = []
        n_reports = PRODUCTION_STEPS // REPORT_INTERVAL

        for i in range(n_reports):
            simulation.step(REPORT_INTERVAL)

            state = simulation.context.getState(getPositions=True)
            positions = state.getPositions(asNumpy=True)[peptide_indices]

            # Calculate RMSD
            ref_centered = ref_positions - np.mean(ref_positions, axis=0)
            pos_centered = positions - np.mean(positions, axis=0)
            rmsd = np.sqrt(np.mean(np.sum((ref_centered - pos_centered)**2, axis=1)))

            time_ps = (i + 1) * REPORT_INTERVAL * TIMESTEP_FS / 1000
            rmsd_nm = float(rmsd)

            rmsd_data.append({
                'time_ps': time_ps,
                'rmsd_nm': rmsd_nm,
            })

            if (i + 1) % 10 == 0:
                print(f"      t={time_ps:.1f} ps, RMSD={rmsd_nm:.3f} nm")

        # Analyze RMSD
        rmsds = [d['rmsd_nm'] for d in rmsd_data]
        final_rmsds = rmsds[-10:]  # Last 10 samples

        mean_final = np.mean(final_rmsds)
        std_final = np.std(final_rmsds)

        # Check for drift (linear regression slope)
        times = [d['time_ps'] for d in rmsd_data[-20:]]
        vals = [d['rmsd_nm'] for d in rmsd_data[-20:]]
        if len(times) > 1:
            slope, _ = np.polyfit(times, vals, 1)
            drift_per_ns = slope * 1000  # per ns
        else:
            drift_per_ns = 0

        # Verdict
        if drift_per_ns > 0.2 or mean_final > 1.0:
            verdict = "UNSTABLE"
            recommendation = "DISCARD"
        elif mean_final > 0.5:
            verdict = "MARGINAL"
            recommendation = "INVESTIGATE"
        else:
            verdict = "STABLE"
            recommendation = "PROCEED"

        result['success'] = True
        result['rmsd_data'] = rmsd_data
        result['mean_rmsd_nm'] = float(mean_final)
        result['std_rmsd_nm'] = float(std_final)
        result['drift_nm_per_ns'] = float(drift_per_ns)
        result['verdict'] = verdict
        result['recommendation'] = recommendation

        print(f"\n    Final RMSD: {mean_final:.3f} ± {std_final:.3f} nm")
        print(f"    Drift: {drift_per_ns:.4f} nm/ns")
        print(f"    VERDICT: {verdict}")

        # Save RMSD trajectory
        csv_path = OUTPUT_DIR / f"{peptide_id}_rmsd.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['time_ps', 'rmsd_nm'])
            writer.writeheader()
            writer.writerows(rmsd_data)

        result['rmsd_csv'] = str(csv_path)

    except Exception as e:
        print(f"    MD failed: {e}")
        result['success'] = False
        result['error'] = str(e)
        result['verdict'] = 'FAILED'
        result['recommendation'] = 'FIX_STRUCTURE'

    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Explicit Solvent MD (Amber14/TIP3P)',
        'temperature_K': TEMPERATURE,
        'peptides': {},
    }

    stable = []
    unstable = []
    failed = []

    for peptide_id, peptide_info in PEPTIDES.items():
        print(f"\n{'=' * 60}")
        print(f"Processing: {peptide_id}")
        print(f"  {peptide_info['name']}")
        print(f"  Sequence: {peptide_info['sequence']}")
        print(f"{'=' * 60}")

        # Build peptide
        pdb_path = OUTPUT_DIR / f"{peptide_id}_peptide.pdb"
        if not build_peptide_pdb(peptide_info['sequence'], pdb_path):
            results['peptides'][peptide_id] = {
                'success': False,
                'error': 'Peptide building failed',
                'verdict': 'FAILED',
            }
            failed.append(peptide_id)
            continue

        # Run MD
        md_result = run_md_simulation(pdb_path, peptide_id)
        results['peptides'][peptide_id] = md_result

        if md_result.get('success'):
            if md_result['verdict'] == 'STABLE':
                stable.append(peptide_id)
                print(f"\n  ✓ {peptide_id}: STABLE")
            else:
                unstable.append(peptide_id)
                print(f"\n  ? {peptide_id}: {md_result['verdict']}")
        else:
            failed.append(peptide_id)
            print(f"\n  ✗ {peptide_id}: FAILED")

    # Summary
    print("\n" + "=" * 80)
    print("MD STABILITY SUMMARY")
    print("=" * 80)
    print(f"\n  STABLE (proceed):     {len(stable)}")
    print(f"  UNSTABLE (discard):   {len(unstable)}")
    print(f"  FAILED (fix):         {len(failed)}")

    results['summary'] = {
        'stable': stable,
        'unstable': unstable,
        'failed': failed,
    }

    # Save
    output_json = OUTPUT_DIR / "md_stability_results.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {output_json}")

    if stable:
        print("\n  STABLE PEPTIDES - Ready for binding studies:")
        for p in stable:
            print(f"    ✓ {p}")

    return results


if __name__ == "__main__":
    main()
