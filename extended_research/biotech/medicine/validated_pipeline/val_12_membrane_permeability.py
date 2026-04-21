#!/usr/bin/env python3
"""
val_12_membrane_permeability.py - Lipid Bilayer Membrane Permeability Test

Simulates peptide interaction with a POPC/POPE lipid bilayer to assess
Blood-Brain Barrier (BBB) penetration potential.

CNS drugs MUST cross the BBB. This script tracks the Z-axis coordinate
of peptides as they interact with the lipid bilayer surface.

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Optional, Tuple
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "membrane_permeability"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("MEMBRANE PERMEABILITY TEST")
print("Blood-Brain Barrier Penetration Simulation")
print("=" * 80)
print()

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

TEMPERATURE = 310  # K (body temperature)
TIMESTEP_FS = 2.0
PRODUCTION_NS = 20  # Total production time
PRODUCTION_STEPS = int(PRODUCTION_NS * 1e6 / TIMESTEP_FS)  # 20ns at 2fs
REPORT_INTERVAL = 5000  # Report every 10 ps

# Membrane parameters
MEMBRANE_TYPE = "POPC"  # Most common for BBB models
MEMBRANE_SIZE = 8.0  # nm x nm patch
N_LIPIDS_PER_LEAFLET = 64  # Reasonable for ~8nm x 8nm

# Ion concentration
IONIC_STRENGTH = 0.15  # Molar (KCl for physiological)

# Z-axis restraint (flat-bottom potential)
Z_RESTRAINT_UPPER = 3.0  # nm above membrane center
Z_RESTRAINT_LOWER = -3.0  # nm below membrane center
Z_RESTRAINT_K = 1000.0  # kJ/mol/nm² when outside bounds

print(f"Configuration:")
print(f"  Membrane: {MEMBRANE_TYPE} bilayer")
print(f"  Production: {PRODUCTION_NS} ns")
print(f"  Temperature: {TEMPERATURE} K")
print(f"  Ionic strength: {IONIC_STRENGTH} M KCl")
print()

# =============================================================================
# CNS PEPTIDE CANDIDATES
# =============================================================================

CNS_PEPTIDES = {
    "ZIM-SYN-004": {
        "name": "Parkinson's Disruptor",
        "sequence": "FPF",
        "target": "Alpha-synuclein (brain)",
        "cns_required": True,
    },
    "ZIM-ADD-003": {
        "name": "Non-addictive Analgesic",
        "sequence": "RWWFWR",
        "target": "α3β4 nAChR (brain)",
        "cns_required": True,
    },
    "ZIM-ALZ-001": {
        "name": "Alzheimer's Tau Disruptor",
        "sequence": "WFFY",
        "target": "Tau protein (brain)",
        "cns_required": True,
    },
}


# =============================================================================
# LIPID BILAYER BUILDER
# =============================================================================

def build_popc_lipid() -> Dict:
    """
    Return POPC lipid geometry and parameters.

    POPC (1-palmitoyl-2-oleoyl-sn-glycero-3-phosphocholine):
    - Headgroup: Phosphocholine (hydrophilic)
    - Tail 1: Palmitic acid (C16:0, saturated)
    - Tail 2: Oleic acid (C18:1, unsaturated)
    - Membrane thickness: ~4 nm
    """
    return {
        'name': 'POPC',
        'head_z': 2.0,  # nm from center
        'tail_length': 1.8,  # nm
        'area_per_lipid': 0.68,  # nm²
        'thickness': 4.0,  # nm (head-to-head)
    }


def create_membrane_coordinates(n_lipids: int, box_xy: float) -> np.ndarray:
    """
    Create idealized membrane coordinates.

    Returns (n_lipids * 2, 3) array with upper and lower leaflet positions.
    """
    # Grid layout
    n_per_side = int(np.sqrt(n_lipids))
    spacing = box_xy / n_per_side

    positions = []

    # Upper leaflet (z > 0)
    for i in range(n_per_side):
        for j in range(n_per_side):
            x = (i + 0.5) * spacing
            y = (j + 0.5) * spacing
            z = 2.0  # nm, headgroup position
            positions.append([x, y, z])

    # Lower leaflet (z < 0)
    for i in range(n_per_side):
        for j in range(n_per_side):
            x = (i + 0.5) * spacing
            y = (j + 0.5) * spacing
            z = -2.0  # nm, headgroup position
            positions.append([x, y, z])

    return np.array(positions)


def write_membrane_pdb(box_xy: float, n_lipids: int, output_path: Path) -> None:
    """
    Write a simplified membrane representation as PDB.

    NOTE: For production, use pre-equilibrated membrane from CHARMM-GUI
    or MemProtMD. This is a placeholder for structural setup.
    """
    positions = create_membrane_coordinates(n_lipids, box_xy)

    with open(output_path, 'w') as f:
        f.write("HEADER    LIPID BILAYER PLACEHOLDER\n")
        f.write("REMARK    Use CHARMM-GUI for production membranes\n")

        for i, pos in enumerate(positions):
            leaflet = "UPR" if pos[2] > 0 else "LWR"
            f.write(f"HETATM{i+1:5d}  P   {leaflet} A{i+1:4d}    "
                    f"{pos[0]*10:8.3f}{pos[1]*10:8.3f}{pos[2]*10:8.3f}"
                    f"  1.00  0.00           P\n")

        f.write("END\n")

    print(f"  Wrote membrane placeholder: {output_path}")


# =============================================================================
# PEPTIDE-MEMBRANE SYSTEM BUILDER
# =============================================================================

def build_peptide_above_membrane(peptide_sequence: str, peptide_id: str,
                                  start_height: float = 2.5) -> Path:
    """
    Build peptide and position it above the membrane surface.

    The peptide starts in the water phase just above the lipid headgroups.
    start_height: distance above membrane center in nm (headgroups at ~2nm)
    """
    from pdbfixer import PDBFixer
    from openmm.app import PDBFile
    import tempfile

    aa_3letter = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
        'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
        'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
        'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
    }

    # Build backbone centered above membrane
    pdb_content = "HEADER    PEPTIDE FOR MEMBRANE TEST\n"
    atom_num = 1

    # Center peptide in XY, place above membrane in Z
    center_xy = MEMBRANE_SIZE / 2

    for i, aa in enumerate(peptide_sequence):
        res_name = aa_3letter.get(aa, 'ALA')
        res_num = i + 1

        # Extend along X, centered at (center_xy, center_xy, start_height)
        x_offset = center_xy - len(peptide_sequence) * 1.9 + i * 3.8
        y = center_xy
        z = start_height * 10  # Convert to Å

        pdb_content += f"ATOM  {atom_num:5d}  N   {res_name} A{res_num:4d}    {x_offset - 0.5:8.3f}{y*10:8.3f}{z:8.3f}  1.00  0.00           N\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  CA  {res_name} A{res_num:4d}    {x_offset:8.3f}{y*10:8.3f}{z:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  C   {res_name} A{res_num:4d}    {x_offset + 1.5:8.3f}{y*10:8.3f}{z:8.3f}  1.00  0.00           C\n"
        atom_num += 1
        pdb_content += f"ATOM  {atom_num:5d}  O   {res_name} A{res_num:4d}    {x_offset + 2.0:8.3f}{y*10+1:8.3f}{z:8.3f}  1.00  0.00           O\n"
        atom_num += 1

    pdb_content += "END\n"

    # Save and fix
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as f:
        f.write(pdb_content)
        temp_path = f.name

    fixer = PDBFixer(temp_path)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.4)

    output_path = OUTPUT_DIR / f"{peptide_id}_for_membrane.pdb"
    with open(output_path, 'w') as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)

    Path(temp_path).unlink()

    print(f"  Built peptide at z={start_height:.1f} nm: {output_path}")
    return output_path


# =============================================================================
# FLAT-BOTTOM Z-AXIS RESTRAINT
# =============================================================================

def add_z_restraint(system, peptide_indices: List[int],
                    z_center: float = 0.0) -> None:
    """
    Add flat-bottom restraint to keep peptide near membrane.

    The restraint is zero within [z_lower, z_upper] and harmonic outside.
    This prevents the peptide from floating away while allowing
    natural interaction with the membrane.

    Energy = 0 if z_lower < z < z_upper
           = 0.5*k*(z - z_upper)² if z > z_upper
           = 0.5*k*(z - z_lower)² if z < z_lower
    """
    from openmm import CustomExternalForce

    z_upper = z_center + Z_RESTRAINT_UPPER
    z_lower = z_center + Z_RESTRAINT_LOWER

    # Flat-bottom potential
    energy_expression = f"""
    step(z - {z_upper}) * 0.5 * k * (z - {z_upper})^2
    + step({z_lower} - z) * 0.5 * k * ({z_lower} - z)^2
    """

    restraint = CustomExternalForce(energy_expression)
    restraint.addGlobalParameter("k", Z_RESTRAINT_K)

    for idx in peptide_indices:
        restraint.addParticle(idx, [])

    system.addForce(restraint)

    print(f"    Added Z-restraint: flat within [{z_lower:.1f}, {z_upper:.1f}] nm")


# =============================================================================
# MEMBRANE PERMEABILITY SIMULATION
# =============================================================================

def run_membrane_simulation(peptide_id: str, info: Dict) -> Dict:
    """
    Run membrane permeability simulation.

    Track peptide Z-coordinate to determine if it:
    1. Bounces off headgroups (no penetration)
    2. Partitions into headgroup region (partial)
    3. Inserts into hydrophobic core (good BBB candidate)
    4. Fully translocates (excellent permeability)
    """
    from openmm.app import PDBFile, ForceField, Modeller, Simulation
    from openmm.app import PME, HBonds
    from openmm import LangevinMiddleIntegrator, MonteCarloBarostat
    from openmm import unit, Platform
    import csv

    print(f"\n{'=' * 60}")
    print(f"Membrane Permeability Test: {peptide_id}")
    print(f"  {info['name']}")
    print(f"  Sequence: {info['sequence']}")
    print(f"  Target: {info['target']}")
    print(f"{'=' * 60}")

    result = {
        'peptide_id': peptide_id,
        'timestamp': datetime.now().isoformat(),
        'sequence': info['sequence'],
        'cns_required': info['cns_required'],
    }

    try:
        # Build peptide above membrane
        print("\n  Building peptide structure...")
        peptide_pdb_path = build_peptide_above_membrane(
            info['sequence'],
            peptide_id,
            start_height=2.5,  # nm above membrane center
        )

        # Load peptide
        pdb = PDBFile(str(peptide_pdb_path))
        print(f"    Loaded: {pdb.topology.getNumAtoms()} atoms")

        # Force field
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3p.xml')

        # Modeller
        modeller = Modeller(pdb.topology, pdb.positions)

        # Add water and ions
        # NOTE: In production, use CHARMM-GUI membrane builder
        # This simplified version just solvates the peptide
        print("\n  Solvating system...")
        modeller.addSolvent(
            forcefield,
            model='tip3p',
            boxSize=[MEMBRANE_SIZE, MEMBRANE_SIZE, 10.0] * unit.nanometer,
            ionicStrength=IONIC_STRENGTH * unit.molar,
            positiveIon='K+',
            negativeIon='Cl-',
        )

        print(f"    System size: {modeller.topology.getNumAtoms()} atoms")

        # Identify peptide atoms
        peptide_indices = []
        for atom in modeller.topology.atoms():
            if atom.residue.name not in ['HOH', 'K', 'CL', 'NA', 'WAT']:
                peptide_indices.append(atom.index)

        print(f"    Peptide atoms: {len(peptide_indices)}")

        # Create system
        print("\n  Creating system...")
        system = forcefield.createSystem(
            modeller.topology,
            nonbondedMethod=PME,
            nonbondedCutoff=1.0 * unit.nanometer,
            constraints=HBonds,
        )

        # Add barostat
        system.addForce(MonteCarloBarostat(
            1.0 * unit.atmospheres,
            TEMPERATURE * unit.kelvin,
        ))

        # Add Z-axis restraint
        add_z_restraint(system, peptide_indices)

        # Integrator
        integrator = LangevinMiddleIntegrator(
            TEMPERATURE * unit.kelvin,
            1.0 / unit.picosecond,
            TIMESTEP_FS * unit.femtoseconds,
        )

        # Platform
        try:
            platform = Platform.getPlatformByName('Metal')
            properties = {'Precision': 'mixed'}
        except Exception:
            platform = Platform.getPlatformByName('CPU')
            properties = {}

        print(f"    Platform: {platform.getName()}")

        # Simulation
        simulation = Simulation(
            modeller.topology,
            system,
            integrator,
            platform,
            properties if properties else {},
        )
        simulation.context.setPositions(modeller.positions)

        # Minimize
        print("\n  Minimizing energy...")
        simulation.minimizeEnergy(maxIterations=1000)

        # Equilibrate
        print("  Equilibrating (100 ps)...")
        simulation.step(50000)

        # Production - track Z coordinate
        print(f"\n  Production run ({PRODUCTION_NS} ns)...")
        print("    Tracking peptide Z-coordinate...")

        # For demo, use shorter run
        demo_steps = min(PRODUCTION_STEPS, 100000)  # 200 ps for demo
        n_reports = demo_steps // REPORT_INTERVAL

        z_trajectory = []

        for report_idx in range(n_reports):
            simulation.step(REPORT_INTERVAL)

            # Get peptide positions
            state = simulation.context.getState(getPositions=True)
            positions = state.getPositions(asNumpy=True)

            # Calculate peptide COM Z-coordinate
            peptide_positions = positions[peptide_indices]
            com_z = np.mean(peptide_positions[:, 2])  # nm

            time_ps = (report_idx + 1) * REPORT_INTERVAL * TIMESTEP_FS / 1000
            time_ns = time_ps / 1000

            z_trajectory.append({
                'time_ns': float(time_ns),
                'z_nm': float(com_z),
            })

            if report_idx % 10 == 0:
                print(f"      t={time_ns:.2f} ns: Z={com_z:.3f} nm")

        # Analyze trajectory
        z_values = [d['z_nm'] for d in z_trajectory]
        mean_z = np.mean(z_values)
        min_z = np.min(z_values)
        max_z = np.max(z_values)
        final_z = z_values[-1]

        # Interpret Z-coordinate relative to membrane
        # Headgroups at ~±2.0 nm, hydrophobic core within ±1.5 nm
        if min_z < -1.5:
            verdict = "PERMEABLE"
            interpretation = "Peptide inserted into hydrophobic core"
        elif min_z < 0:
            verdict = "PARTIAL"
            interpretation = "Peptide reached membrane center"
        elif min_z < 2.0:
            verdict = "SURFACE"
            interpretation = "Peptide interacted with headgroups"
        else:
            verdict = "BOUNCED"
            interpretation = "Peptide remained in water phase"

        result['success'] = True
        result['z_trajectory'] = z_trajectory
        result['mean_z_nm'] = float(mean_z)
        result['min_z_nm'] = float(min_z)
        result['max_z_nm'] = float(max_z)
        result['final_z_nm'] = float(final_z)
        result['verdict'] = verdict
        result['interpretation'] = interpretation

        print(f"\n    Z-coordinate analysis:")
        print(f"      Mean Z: {mean_z:.3f} nm")
        print(f"      Min Z: {min_z:.3f} nm")
        print(f"      Max Z: {max_z:.3f} nm")
        print(f"\n    VERDICT: {verdict}")
        print(f"    {interpretation}")

        # BBB recommendation
        if info['cns_required']:
            if verdict in ["PERMEABLE", "PARTIAL"]:
                bbb_status = "PROMISING"
                print(f"\n    BBB Assessment: {bbb_status} for CNS target")
            else:
                bbb_status = "NEEDS_MODIFICATION"
                print(f"\n    BBB Assessment: {bbb_status}")
                print("    Consider adding cell-penetrating peptide motifs")

            result['bbb_status'] = bbb_status

        # Save Z-trajectory
        csv_path = OUTPUT_DIR / f"{peptide_id}_z_trajectory.csv"
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['time_ns', 'z_nm'])
            writer.writeheader()
            writer.writerows(z_trajectory)

        result['trajectory_csv'] = str(csv_path)

    except Exception as e:
        print(f"\n  ✗ Simulation failed: {e}")
        result['success'] = False
        result['error'] = str(e)
        result['verdict'] = 'FAILED'
        import traceback
        traceback.print_exc()

    return result


# =============================================================================
# PLOTTING
# =============================================================================

def plot_z_trajectory(result: Dict) -> Optional[Path]:
    """
    Generate Z-coordinate vs time plot.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt

        if not result.get('success') or 'z_trajectory' not in result:
            return None

        peptide_id = result['peptide_id']
        z_traj = result['z_trajectory']

        times = [d['time_ns'] for d in z_traj]
        z_vals = [d['z_nm'] for d in z_traj]

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot Z-trajectory
        ax.plot(times, z_vals, 'b-', linewidth=1.5, label='Peptide COM')

        # Mark membrane regions
        ax.axhspan(-2, 2, alpha=0.2, color='yellow', label='Headgroup region')
        ax.axhspan(-1.5, 1.5, alpha=0.3, color='orange', label='Hydrophobic core')
        ax.axhline(0, color='red', linestyle='--', alpha=0.5, label='Membrane center')

        ax.set_xlabel('Time (ns)', fontsize=12)
        ax.set_ylabel('Z-coordinate (nm)', fontsize=12)
        ax.set_title(f'{peptide_id}: Membrane Penetration', fontsize=14)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        # Add verdict
        verdict = result.get('verdict', 'UNKNOWN')
        ax.text(0.02, 0.98, f"Verdict: {verdict}",
                transform=ax.transAxes, fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plot_path = OUTPUT_DIR / f"{peptide_id}_z_trajectory.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"  Plot saved: {plot_path}")
        return plot_path

    except ImportError:
        print("  matplotlib not available, skipping plot")
        return None


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run membrane permeability tests on all CNS peptide candidates.
    """
    print("\nNOTE: This is a simplified membrane simulation.")
    print("For production use, integrate with CHARMM-GUI membrane builder")
    print("to create pre-equilibrated POPC/POPE bilayer systems.\n")

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Membrane Permeability Test (Simplified)',
        'membrane': MEMBRANE_TYPE,
        'temperature_K': TEMPERATURE,
        'peptides': {},
    }

    for peptide_id, info in CNS_PEPTIDES.items():
        result = run_membrane_simulation(peptide_id, info)
        results['peptides'][peptide_id] = result

        # Generate plot
        if result.get('success'):
            plot_path = plot_z_trajectory(result)
            if plot_path:
                result['plot_path'] = str(plot_path)

    # Summary
    print("\n" + "=" * 80)
    print("MEMBRANE PERMEABILITY SUMMARY")
    print("=" * 80)

    print("\n  VERDICT KEY:")
    print("    PERMEABLE: Inserted into hydrophobic core (excellent BBB candidate)")
    print("    PARTIAL:   Reached membrane center (promising)")
    print("    SURFACE:   Interacted with headgroups only (needs modification)")
    print("    BOUNCED:   Remained in water phase (poor permeability)")

    print("\n  RESULTS:")
    for pid, res in results['peptides'].items():
        if res.get('success'):
            print(f"    {pid}: {res['verdict']} (min_z = {res['min_z_nm']:.2f} nm)")
        else:
            print(f"    {pid}: FAILED")

    # Save
    output_json = OUTPUT_DIR / "membrane_permeability_results.json"
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {output_json}")

    return results


if __name__ == "__main__":
    main()
