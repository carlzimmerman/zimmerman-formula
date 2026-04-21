#!/usr/bin/env python3
"""
val_10_overnight_production_md.py - Production-Grade Overnight MD

PURPOSE:
Run 10-50ns explicit solvent MD simulations on therapeutic peptides.
Designed for overnight batch processing on Apple Silicon with Metal acceleration.

PROTOCOL:
1. Build peptide with proper caps (ACE/NME)
2. Solvate in TIP3P + 0.15M NaCl
3. Energy minimization
4. 1ns NVT equilibration
5. 2ns NPT equilibration
6. 10-50ns production MD
7. RMSD analysis and stability verdict

USAGE:
    nohup python val_10_overnight_production_md.py > md_overnight.log 2>&1 &

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import csv
import sys
from typing import Dict, List, Optional, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path(__file__).parent / "results" / "production_md"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Simulation parameters (STRICT PROTOCOL V1.0)
TEMPERATURE_K = 310
PRESSURE_ATM = 1.0
IONIC_STRENGTH_M = 0.15
BOX_PADDING_NM = 1.2
TIMESTEP_FS = 2.0

# Equilibration (strict 2-stage)
NVT_STEPS = 500000      # 1 ns
NPT_EQUIL_STEPS = 1000000  # 2 ns

# Production
PRODUCTION_NS = 10  # Start with 10ns, increase to 50ns for publication
PRODUCTION_STEPS = int(PRODUCTION_NS * 1e6 / TIMESTEP_FS)

# Reporting
TRAJECTORY_INTERVAL = 5000   # Every 10 ps
STATE_INTERVAL = 500         # Every 1 ps
RMSD_INTERVAL = 5000         # Every 10 ps

print("=" * 80)
print("OVERNIGHT PRODUCTION MD - PROTOCOL V1.0")
print(f"Duration: {PRODUCTION_NS} ns per peptide")
print(f"Platform: Apple Silicon Metal (preferred)")
print("=" * 80)
print()

# =============================================================================
# PEPTIDES TO PROCESS
# =============================================================================

PEPTIDES = [
    {
        "id": "ZIM-SYN-004",
        "name": "Parkinson's Disruptor",
        "sequence": "FPF",
        "n_cap": "ACE",
        "c_cap": "NME",
        "target": "Alpha-synuclein",
    },
    {
        "id": "ZIM-ADD-003",
        "name": "Non-addictive nAChR Agonist",
        "sequence": "RWWFWR",
        "n_cap": None,
        "c_cap": None,
        "target": "α3β4 nAChR",
    },
    {
        "id": "ZIM-PD6-013",
        "name": "Checkpoint Disruptor",
        "sequence": "WFFLY",
        "n_cap": "ACE",
        "c_cap": "NME",
        "target": "PD-1/PD-L1",
    },
]

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================

def check_dependencies() -> bool:
    """Verify all required packages."""
    try:
        import openmm
        from openmm import app, unit, Platform
        from pdbfixer import PDBFixer
        print(f"✓ OpenMM {openmm.__version__}")

        # Check for Metal platform
        try:
            metal = Platform.getPlatformByName('Metal')
            print(f"✓ Metal platform available (Apple GPU)")
        except:
            print("⚠ Metal not available, will use CPU")

        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False


# =============================================================================
# PEPTIDE BUILDER
# =============================================================================

def build_peptide_structure(
    sequence: str,
    peptide_id: str,
    n_cap: str = None,
    c_cap: str = None,
) -> Optional[Path]:
    """
    Build peptide PDB with proper residue names for Amber force field.
    """
    from openmm.app import PDBFile
    from pdbfixer import PDBFixer

    print(f"  Building {peptide_id}: {sequence}")

    aa_3letter = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
    }

    # Build backbone PDB
    pdb_content = "HEADER    THERAPEUTIC PEPTIDE\n"
    pdb_content += f"TITLE     {peptide_id}\n"

    atom_num = 1
    res_start = 1

    # Add ACE cap if specified
    if n_cap == "ACE":
        x_offset = -3.8
        pdb_content += f"ATOM  {atom_num:5d}  C   ACE A{res_start:4d}    {x_offset:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  O   ACE A{res_start:4d}    {x_offset + 1.2:8.3f}{1.0:8.3f}{0.0:8.3f}  1.00  0.00           O\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  CH3 ACE A{res_start:4d}    {x_offset - 1.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        res_start += 1

    # Add amino acids
    for i, aa in enumerate(sequence):
        res_name = aa_3letter.get(aa, 'ALA')
        res_num = res_start + i
        x_offset = i * 3.8

        # Backbone atoms
        pdb_content += f"ATOM  {atom_num:5d}  N   {res_name} A{res_num:4d}    {x_offset - 0.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           N\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  CA  {res_name} A{res_num:4d}    {x_offset:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  C   {res_name} A{res_num:4d}    {x_offset + 1.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  O   {res_name} A{res_num:4d}    {x_offset + 2.0:8.3f}{1.0:8.3f}{0.0:8.3f}  1.00  0.00           O\n"
        atom_num += 1

    # Add NME cap if specified
    if c_cap == "NME":
        res_num = res_start + len(sequence)
        x_offset = len(sequence) * 3.8
        pdb_content += f"ATOM  {atom_num:5d}  N   NME A{res_num:4d}    {x_offset + 2.5:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           N\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  CH3 NME A{res_num:4d}    {x_offset + 4.0:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C\n"
        atom_num += 1

    pdb_content += "END\n"

    # Save backbone
    backbone_path = OUTPUT_DIR / f"{peptide_id}_backbone.pdb"
    with open(backbone_path, 'w') as f:
        f.write(pdb_content)

    # Use PDBFixer to add missing atoms
    try:
        fixer = PDBFixer(str(backbone_path))
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        fixer.addMissingHydrogens(7.4)

        output_path = OUTPUT_DIR / f"{peptide_id}_complete.pdb"
        with open(output_path, 'w') as f:
            PDBFile.writeFile(fixer.topology, fixer.positions, f)

        print(f"    ✓ Structure saved: {output_path}")
        return output_path

    except Exception as e:
        print(f"    ✗ Structure building failed: {e}")
        return None


# =============================================================================
# MD SIMULATION ENGINE
# =============================================================================

def run_production_md(
    pdb_path: Path,
    peptide_id: str,
    production_ns: float = PRODUCTION_NS,
) -> Dict:
    """
    Run complete MD protocol: minimize → NVT → NPT → production.
    """
    from openmm.app import PDBFile, ForceField, Modeller, Simulation
    from openmm.app import PME, HBonds, DCDReporter, StateDataReporter
    from openmm import LangevinMiddleIntegrator, MonteCarloBarostat, Platform
    from openmm import unit
    import time

    print(f"\n  Starting production MD for {peptide_id}...")
    print(f"    Duration: {production_ns} ns")

    start_time = time.time()

    result = {
        'peptide_id': peptide_id,
        'timestamp': datetime.now().isoformat(),
        'production_ns': production_ns,
    }

    try:
        # Load structure
        pdb = PDBFile(str(pdb_path))
        print(f"    Loaded: {pdb.topology.getNumAtoms()} atoms")

        # Force field
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Modeller
        modeller = Modeller(pdb.topology, pdb.positions)

        # Solvate
        print(f"    Solvating (padding={BOX_PADDING_NM} nm, ions={IONIC_STRENGTH_M} M)...")
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            padding=BOX_PADDING_NM * unit.nanometer,
            ionicStrength=IONIC_STRENGTH_M * unit.molar,
            positiveIon='Na+',
            negativeIon='Cl-',
        )

        n_atoms = modeller.topology.getNumAtoms()
        print(f"    System: {n_atoms} atoms")
        result['n_atoms'] = n_atoms

        # Create system
        print("    Creating system...")
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=HBonds,
            rigidWater=True,
        )

        # Select platform
        try:
            platform = Platform.getPlatformByName('Metal')
            properties = {'Precision': 'mixed'}
            print("    Platform: Metal (Apple GPU)")
        except:
            try:
                platform = Platform.getPlatformByName('OpenCL')
                properties = {}
                print("    Platform: OpenCL")
            except:
                platform = Platform.getPlatformByName('CPU')
                properties = {}
                print("    Platform: CPU")

        result['platform'] = platform.getName()

        # =================================================================
        # STAGE 1: ENERGY MINIMIZATION
        # =================================================================
        print("\n    [STAGE 1] Energy minimization...")

        integrator = LangevinMiddleIntegrator(
            TEMPERATURE_K * unit.kelvin,
            1.0 / unit.picosecond,
            TIMESTEP_FS * unit.femtoseconds,
        )

        simulation = Simulation(
            modeller.topology,
            system,
            integrator,
            platform,
            properties,
        )
        simulation.context.setPositions(modeller.positions)

        state_before = simulation.context.getState(getEnergy=True)
        e_before = state_before.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)

        simulation.minimizeEnergy(maxIterations=1000)

        state_after = simulation.context.getState(getEnergy=True)
        e_after = state_after.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)

        print(f"      Energy: {e_before:.0f} → {e_after:.0f} kJ/mol")

        # =================================================================
        # STAGE 2: NVT EQUILIBRATION (1 ns)
        # =================================================================
        print(f"\n    [STAGE 2] NVT equilibration ({NVT_STEPS * TIMESTEP_FS / 1e6:.1f} ns)...")

        # NVT - no barostat
        simulation.step(NVT_STEPS)

        state = simulation.context.getState(getEnergy=True)
        temp = 2 * state.getKineticEnergy() / (3 * n_atoms * unit.MOLAR_GAS_CONSTANT_R)
        print(f"      Temperature: {temp.value_in_unit(unit.kelvin):.1f} K")

        # =================================================================
        # STAGE 3: NPT EQUILIBRATION (2 ns)
        # =================================================================
        print(f"\n    [STAGE 3] NPT equilibration ({NPT_EQUIL_STEPS * TIMESTEP_FS / 1e6:.1f} ns)...")

        # Add barostat
        barostat = MonteCarloBarostat(
            PRESSURE_ATM * unit.atmospheres,
            TEMPERATURE_K * unit.kelvin,
            25,
        )
        system.addForce(barostat)

        # Reinitialize
        simulation.context.reinitialize(preserveState=True)

        simulation.step(NPT_EQUIL_STEPS)

        state = simulation.context.getState(getPositions=True, getEnergy=True)
        box = state.getPeriodicBoxVectors()
        volume = box[0][0] * box[1][1] * box[2][2]
        density = n_atoms * 18.015 / (volume.value_in_unit(unit.nanometer**3) * 6.022e23 * 1e-24)

        print(f"      Density: {density:.3f} g/cm³")

        # Save reference structure for RMSD
        ref_positions = state.getPositions(asNumpy=True)

        # Get peptide indices (non-water, non-ion)
        peptide_indices = []
        for atom in modeller.topology.atoms():
            if atom.residue.name not in ['HOH', 'NA', 'CL', 'WAT']:
                peptide_indices.append(atom.index)

        # =================================================================
        # STAGE 4: PRODUCTION MD
        # =================================================================
        production_steps = int(production_ns * 1e6 / TIMESTEP_FS)

        print(f"\n    [STAGE 4] Production MD ({production_ns} ns = {production_steps} steps)...")

        # Output files
        traj_file = OUTPUT_DIR / f"{peptide_id}_trajectory.dcd"
        state_file = OUTPUT_DIR / f"{peptide_id}_state.csv"
        rmsd_file = OUTPUT_DIR / f"{peptide_id}_rmsd.csv"

        # Reporters
        simulation.reporters.append(
            DCDReporter(str(traj_file), TRAJECTORY_INTERVAL)
        )
        simulation.reporters.append(
            StateDataReporter(
                str(state_file),
                STATE_INTERVAL,
                step=True,
                time=True,
                potentialEnergy=True,
                temperature=True,
                density=True,
            )
        )

        # Run production with RMSD tracking
        rmsd_data = []
        n_reports = production_steps // RMSD_INTERVAL

        for i in range(n_reports):
            simulation.step(RMSD_INTERVAL)

            # Calculate RMSD
            state = simulation.context.getState(getPositions=True)
            positions = state.getPositions(asNumpy=True)

            ref_subset = ref_positions[peptide_indices]
            pos_subset = positions[peptide_indices]

            ref_centered = ref_subset - np.mean(ref_subset, axis=0)
            pos_centered = pos_subset - np.mean(pos_subset, axis=0)

            rmsd = np.sqrt(np.mean(np.sum((ref_centered - pos_centered)**2, axis=1)))

            time_ns = (i + 1) * RMSD_INTERVAL * TIMESTEP_FS / 1e6

            rmsd_data.append({
                'time_ns': float(time_ns),
                'rmsd_nm': float(rmsd),
            })

            # Progress report every 1 ns
            if (i + 1) % (int(1e6 / TIMESTEP_FS / RMSD_INTERVAL)) == 0:
                elapsed = time.time() - start_time
                print(f"      t={time_ns:.1f} ns, RMSD={rmsd:.3f} nm, elapsed={elapsed/60:.1f} min")

        # Save RMSD trajectory
        with open(rmsd_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['time_ns', 'rmsd_nm'])
            writer.writeheader()
            writer.writerows(rmsd_data)

        # =================================================================
        # ANALYSIS
        # =================================================================
        print("\n    [ANALYSIS]")

        rmsds = np.array([d['rmsd_nm'] for d in rmsd_data])
        times = np.array([d['time_ns'] for d in rmsd_data])

        # Use last 20% for stability assessment
        cutoff = int(0.8 * len(rmsds))
        final_rmsds = rmsds[cutoff:]
        final_times = times[cutoff:]

        mean_rmsd = np.mean(final_rmsds)
        std_rmsd = np.std(final_rmsds)

        # Linear fit for drift
        if len(final_times) > 1:
            slope, _ = np.polyfit(final_times, final_rmsds, 1)
            drift = slope  # nm/ns
        else:
            drift = 0.0

        print(f"      Mean RMSD (final 20%): {mean_rmsd:.3f} ± {std_rmsd:.3f} nm")
        print(f"      RMSD drift: {drift:.4f} nm/ns")

        # Verdict
        if mean_rmsd < 0.3 and abs(drift) < 0.05:
            verdict = "STABLE"
            recommendation = "PROCEED TO BINDING"
        elif mean_rmsd < 0.5 and abs(drift) < 0.2:
            verdict = "MARGINAL"
            recommendation = "EXTEND SIMULATION"
        else:
            verdict = "UNSTABLE"
            recommendation = "REDESIGN PEPTIDE"

        print(f"      VERDICT: {verdict}")
        print(f"      Recommendation: {recommendation}")

        elapsed_total = time.time() - start_time
        print(f"\n    Total time: {elapsed_total/3600:.2f} hours")

        result['success'] = True
        result['files'] = {
            'trajectory': str(traj_file),
            'state': str(state_file),
            'rmsd': str(rmsd_file),
        }
        result['analysis'] = {
            'mean_rmsd_nm': float(mean_rmsd),
            'std_rmsd_nm': float(std_rmsd),
            'drift_nm_per_ns': float(drift),
            'verdict': verdict,
            'recommendation': recommendation,
        }
        result['runtime_hours'] = elapsed_total / 3600

    except Exception as e:
        print(f"    ✗ MD failed: {e}")
        import traceback
        traceback.print_exc()
        result['success'] = False
        result['error'] = str(e)
        result['verdict'] = 'FAILED'

    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run overnight production MD on all peptides."""

    print(f"\nStarting at: {datetime.now()}")
    print(f"Production time per peptide: {PRODUCTION_NS} ns")
    print(f"Estimated total time: {len(PEPTIDES) * 2} - {len(PEPTIDES) * 4} hours\n")

    if not check_dependencies():
        sys.exit(1)

    results = {
        'timestamp': datetime.now().isoformat(),
        'protocol': 'MD_PROTOCOL_V1.0',
        'production_ns': PRODUCTION_NS,
        'peptides': {},
    }

    stable = []
    marginal = []
    unstable = []
    failed = []

    for peptide in PEPTIDES:
        peptide_id = peptide['id']

        print(f"\n{'=' * 70}")
        print(f"Processing: {peptide_id}")
        print(f"  {peptide['name']}")
        print(f"  Sequence: {peptide['sequence']}")
        print(f"  Caps: N={peptide.get('n_cap', 'None')}, C={peptide.get('c_cap', 'None')}")
        print(f"{'=' * 70}")

        # Build structure
        pdb_path = build_peptide_structure(
            peptide['sequence'],
            peptide_id,
            peptide.get('n_cap'),
            peptide.get('c_cap'),
        )

        if pdb_path is None:
            results['peptides'][peptide_id] = {
                'success': False,
                'error': 'Structure building failed',
                'verdict': 'FAILED',
            }
            failed.append(peptide_id)
            continue

        # Run MD
        md_result = run_production_md(pdb_path, peptide_id, PRODUCTION_NS)
        results['peptides'][peptide_id] = md_result

        if md_result.get('success'):
            verdict = md_result['analysis']['verdict']
            if verdict == 'STABLE':
                stable.append(peptide_id)
            elif verdict == 'MARGINAL':
                marginal.append(peptide_id)
            else:
                unstable.append(peptide_id)
        else:
            failed.append(peptide_id)

    # Summary
    print("\n" + "=" * 80)
    print("OVERNIGHT MD SUMMARY")
    print("=" * 80)
    print(f"\n  Total peptides: {len(PEPTIDES)}")
    print(f"  STABLE:         {len(stable)}")
    print(f"  MARGINAL:       {len(marginal)}")
    print(f"  UNSTABLE:       {len(unstable)}")
    print(f"  FAILED:         {len(failed)}")

    results['summary'] = {
        'stable': stable,
        'marginal': marginal,
        'unstable': unstable,
        'failed': failed,
    }

    # Save results
    output_json = OUTPUT_DIR / "production_md_results.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {output_json}")
    print(f"\n  Completed at: {datetime.now()}")

    # Next steps
    if stable:
        print("\n" + "=" * 80)
        print("STABLE PEPTIDES - READY FOR BINDING STUDIES")
        print("=" * 80)
        for p in stable:
            print(f"  ✓ {p}")
        print("\n  Next: Run val_09_umbrella_sampling_pmf.py on these peptides")

    return results


if __name__ == "__main__":
    main()
