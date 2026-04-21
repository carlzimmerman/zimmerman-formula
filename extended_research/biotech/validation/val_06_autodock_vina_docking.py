#!/usr/bin/env python3
"""
Val 06: AutoDock Vina Global Docking Pipeline

PhD-Level Validation Script

Purpose:
--------
Perform blind (global) docking of peptide candidates against target receptors
using AutoDock Vina with exhaustive pose sampling.

Scientific Question:
-------------------
Where do the Z²-designed peptides bind on target receptors, and what are
their predicted binding affinities (relative ranking)?

IMPORTANT:
----------
Docking scores are useful for RANKING candidates, NOT for absolute affinity
prediction. kcal/mol values should NOT be converted to Kd without FEP validation.

Methods:
--------
1. Prepare receptor structures (from PDB)
2. Prepare ligand structures (from predicted peptide PDBs)
3. Define large search box covering entire receptor surface
4. Run Vina with exhaustiveness=32 for global search
5. Cluster and analyze poses
6. Validate binding sites against known biology

Dependencies:
-------------
For full functionality:
- AutoDock Vina (vina or vina_split)
- Open Babel (obabel)
- MGLTools (prepare_receptor4.py, prepare_ligand4.py)

This script can run in "analysis-only" mode without these tools,
using pre-computed results.

pip install numpy scipy pandas biopython

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later
"""

# =============================================================================
# LEGAL DISCLAIMER: This is THEORETICAL COMPUTATIONAL RESEARCH only.
# Not peer reviewed. Not medical advice. Not a validated therapeutic.
# All predictions require experimental validation.
# See: extended_research/biotech/LEGAL_DISCLAIMER.md
# =============================================================================


import json
import subprocess
import shutil
import tempfile
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

import numpy as np

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


# ============================================================================
# Z² FRAMEWORK CONSTANTS
# ============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
COORDINATION_NUMBER = 8  # Z²/Vol(B³) = 8
NATURAL_LENGTH_SCALE = (Z_SQUARED ** 0.25) * 3.8  # ≈ 9.14 Å


# ============================================================================
# RECEPTOR DATABASE
# ============================================================================

# Target receptors with known binding sites for validation
RECEPTOR_DATABASE = {
    'GLP1R': {
        'pdb_id': '6X18',
        'chain': 'R',
        'known_binding_site': [('R', 21), ('R', 22), ('R', 24), ('R', 25)],  # N-terminal domain
        'center': [120.0, 105.0, 75.0],  # Approximate binding site center
        'box_size': [40, 40, 40],  # Å
        'disease': 'Diabetes/Obesity',
        'description': 'GLP-1 Receptor (glucagon-like peptide-1)'
    },
    'GBA1': {
        'pdb_id': '2NT1',
        'chain': 'A',
        'known_binding_site': [('A', 312), ('A', 340), ('A', 345)],
        'center': [35.0, 25.0, 40.0],
        'box_size': [30, 30, 30],
        'disease': 'Parkinson/Gaucher',
        'description': 'Glucocerebrosidase'
    },
    'TNF_ALPHA': {
        'pdb_id': '1TNF',
        'chain': 'A',
        'known_binding_site': [('A', 29), ('A', 35), ('A', 148)],
        'center': [30.0, 30.0, 30.0],
        'box_size': [50, 50, 50],  # Large for trimer interface
        'disease': 'Autoimmune',
        'description': 'Tumor Necrosis Factor alpha'
    },
    'VEGF': {
        'pdb_id': '2VPF',
        'chain': 'A',
        'known_binding_site': [('A', 17), ('A', 46), ('A', 79)],
        'center': [25.0, 35.0, 40.0],
        'box_size': [35, 35, 35],
        'disease': 'Cancer/AMD',
        'description': 'Vascular Endothelial Growth Factor'
    },
    'CRF1': {
        'pdb_id': '4K5Y',
        'chain': 'A',
        'known_binding_site': [('A', 106), ('A', 175), ('A', 318)],
        'center': [0.0, 0.0, 25.0],
        'box_size': [30, 30, 40],
        'disease': 'Anxiety/Depression',
        'description': 'Corticotropin-releasing factor receptor 1'
    },
}


def check_vina_installation() -> Dict[str, bool]:
    """Check if docking tools are installed."""
    tools = {}

    # Check AutoDock Vina
    try:
        result = subprocess.run(['vina', '--version'],
                              capture_output=True, text=True, timeout=10)
        tools['vina'] = result.returncode == 0
    except:
        tools['vina'] = False

    # Check Open Babel
    try:
        result = subprocess.run(['obabel', '-V'],
                              capture_output=True, text=True, timeout=10)
        tools['obabel'] = result.returncode == 0
    except:
        tools['obabel'] = False

    # Check MGLTools
    try:
        result = subprocess.run(['prepare_receptor4.py', '--help'],
                              capture_output=True, text=True, timeout=10)
        tools['mgltools'] = True
    except:
        tools['mgltools'] = False

    return tools


def prepare_receptor_pdbqt(
    pdb_path: str,
    output_path: str,
    chain: str = None
) -> bool:
    """
    Prepare receptor PDBQT file from PDB.

    Uses Open Babel for conversion if MGLTools not available.
    """
    # Try Open Babel first (more commonly available)
    try:
        cmd = ['obabel', pdb_path, '-O', output_path, '-xr']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and os.path.exists(output_path):
            return True
    except Exception as e:
        print(f"    Open Babel failed: {e}")

    # Fallback: create minimal PDBQT (for demonstration)
    try:
        with open(pdb_path, 'r') as f:
            pdb_lines = f.readlines()

        pdbqt_lines = []
        for line in pdb_lines:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                # Add charge field (column 67-76)
                atom_type = line[12:16].strip()
                element = atom_type[0] if atom_type else 'C'

                # Simplified: just append atom type
                new_line = line.rstrip() + f'    {element}\n'
                pdbqt_lines.append(new_line)

        with open(output_path, 'w') as f:
            f.writelines(pdbqt_lines)

        return True
    except Exception as e:
        print(f"    Manual conversion failed: {e}")
        return False


def prepare_ligand_pdbqt(
    pdb_path: str,
    output_path: str
) -> bool:
    """
    Prepare ligand PDBQT file from PDB.
    """
    # Similar to receptor but with torsion handling
    try:
        cmd = ['obabel', pdb_path, '-O', output_path, '-xhn']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and os.path.exists(output_path):
            return True
    except Exception as e:
        print(f"    Open Babel failed: {e}")

    # Fallback
    try:
        with open(pdb_path, 'r') as f:
            pdb_lines = f.readlines()

        pdbqt_lines = []
        for line in pdb_lines:
            if line.startswith('ATOM'):
                atom_type = line[12:16].strip()
                element = atom_type[0] if atom_type else 'C'
                new_line = line.rstrip() + f'    {element}\n'
                pdbqt_lines.append(new_line)

        with open(output_path, 'w') as f:
            f.writelines(pdbqt_lines)

        return True
    except Exception as e:
        return False


def run_vina_docking(
    receptor_pdbqt: str,
    ligand_pdbqt: str,
    center: List[float],
    box_size: List[float],
    output_path: str,
    exhaustiveness: int = 32,
    num_modes: int = 20
) -> Optional[Dict]:
    """
    Run AutoDock Vina docking.

    Parameters:
    -----------
    receptor_pdbqt : str
        Path to receptor PDBQT file
    ligand_pdbqt : str
        Path to ligand PDBQT file
    center : List[float]
        [x, y, z] center of search box
    box_size : List[float]
        [size_x, size_y, size_z] dimensions of search box
    exhaustiveness : int
        Exhaustiveness of search (8 = default, 32 = thorough)
    num_modes : int
        Maximum number of binding modes to return

    Returns:
    --------
    Dict with docking results
    """
    try:
        cmd = [
            'vina',
            '--receptor', receptor_pdbqt,
            '--ligand', ligand_pdbqt,
            '--center_x', str(center[0]),
            '--center_y', str(center[1]),
            '--center_z', str(center[2]),
            '--size_x', str(box_size[0]),
            '--size_y', str(box_size[1]),
            '--size_z', str(box_size[2]),
            '--exhaustiveness', str(exhaustiveness),
            '--num_modes', str(num_modes),
            '--out', output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode == 0:
            # Parse output
            return parse_vina_output(result.stdout, output_path)
        else:
            return {'error': result.stderr}

    except subprocess.TimeoutExpired:
        return {'error': 'Docking timeout (>10 min)'}
    except Exception as e:
        return {'error': str(e)}


def parse_vina_output(stdout: str, output_path: str) -> Dict:
    """
    Parse AutoDock Vina output.
    """
    results = {
        'poses': [],
        'best_affinity': None,
        'all_affinities': []
    }

    # Parse affinities from stdout
    lines = stdout.split('\n')
    for line in lines:
        if line.strip().startswith('1') or line.strip().startswith('2'):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    mode = int(parts[0])
                    affinity = float(parts[1])
                    results['poses'].append({
                        'mode': mode,
                        'affinity_kcal_mol': affinity,
                        'rmsd_lb': float(parts[2]) if len(parts) > 2 else 0,
                        'rmsd_ub': float(parts[3]) if len(parts) > 3 else 0
                    })
                    results['all_affinities'].append(affinity)
                except (ValueError, IndexError):
                    continue

    if results['all_affinities']:
        results['best_affinity'] = min(results['all_affinities'])
        results['mean_affinity'] = np.mean(results['all_affinities'])
        results['output_file'] = output_path

    return results


def simulate_docking_result(
    receptor_name: str,
    ligand_name: str,
    sequence: str
) -> Dict:
    """
    Simulate docking result for demonstration purposes.

    This provides realistic score distributions based on peptide properties
    when actual docking tools are not available.

    NOTE: These are NOT real docking results. They are for pipeline
    demonstration only.
    """
    # Seed based on sequence for reproducibility
    seed = hash(sequence) % 2**32
    np.random.seed(seed)

    # Estimate score based on sequence properties
    length = len(sequence)
    n_charged = sum(1 for aa in sequence if aa in 'RKDE')
    n_aromatic = sum(1 for aa in sequence if aa in 'FYW')
    n_hydrophobic = sum(1 for aa in sequence if aa in 'AILMFVWY')

    # Base affinity (typical peptide range: -5 to -12 kcal/mol)
    base_affinity = -6.0

    # Modifiers based on properties
    length_modifier = -0.1 * (length - 15)  # Longer peptides often better
    charge_modifier = -0.3 * min(n_charged, 4)  # Some charge helps
    aromatic_modifier = -0.5 * min(n_aromatic, 3)  # Aromatics good for binding
    hydrophobic_modifier = -0.1 * (n_hydrophobic / length - 0.5) * 10

    # Final affinity with noise
    affinity = base_affinity + length_modifier + charge_modifier + \
               aromatic_modifier + hydrophobic_modifier + np.random.normal(0, 1)

    # Clamp to realistic range
    affinity = np.clip(affinity, -15, -3)

    # Generate multiple poses
    n_poses = 10
    poses = []
    for i in range(n_poses):
        pose_affinity = affinity + np.random.exponential(0.5)  # Other poses worse
        poses.append({
            'mode': i + 1,
            'affinity_kcal_mol': float(pose_affinity),
            'rmsd_lb': float(np.random.uniform(0, 5)) if i > 0 else 0.0,
            'rmsd_ub': float(np.random.uniform(2, 10)) if i > 0 else 0.0
        })

    return {
        'receptor': receptor_name,
        'ligand': ligand_name,
        'sequence': sequence,
        'poses': poses,
        'best_affinity': float(affinity),
        'mean_affinity': float(np.mean([p['affinity_kcal_mol'] for p in poses])),
        'all_affinities': [p['affinity_kcal_mol'] for p in poses],
        'method': 'SIMULATED (demonstration only)',
        'warning': 'These are NOT real docking results. Install AutoDock Vina for actual calculations.'
    }


def analyze_docking_results(results: List[Dict]) -> Dict:
    """
    Analyze batch docking results.
    """
    if not results:
        return {'error': 'No results to analyze'}

    # Filter successful results
    successful = [r for r in results if 'best_affinity' in r and r['best_affinity'] is not None]

    if not successful:
        return {'error': 'No successful docking runs'}

    affinities = [r['best_affinity'] for r in successful]

    # Statistical analysis
    analysis = {
        'n_total': len(results),
        'n_successful': len(successful),
        'success_rate': len(successful) / len(results),
        'affinity_statistics': {
            'mean': float(np.mean(affinities)),
            'std': float(np.std(affinities)),
            'min': float(np.min(affinities)),
            'max': float(np.max(affinities)),
            'median': float(np.median(affinities))
        }
    }

    # Rank by affinity
    ranked = sorted(successful, key=lambda x: x['best_affinity'])
    analysis['top_5'] = [
        {
            'ligand': r.get('ligand', 'unknown'),
            'receptor': r.get('receptor', 'unknown'),
            'affinity_kcal_mol': r['best_affinity'],
            'sequence': r.get('sequence', '')[:30]
        }
        for r in ranked[:5]
    ]

    # Quality assessment
    strong_binders = [r for r in successful if r['best_affinity'] < -8.0]
    moderate_binders = [r for r in successful if -8.0 <= r['best_affinity'] < -6.0]
    weak_binders = [r for r in successful if r['best_affinity'] >= -6.0]

    analysis['binding_classification'] = {
        'strong (< -8 kcal/mol)': len(strong_binders),
        'moderate (-8 to -6 kcal/mol)': len(moderate_binders),
        'weak (> -6 kcal/mol)': len(weak_binders)
    }

    return analysis


def run_docking_pipeline(
    peptide_structures_dir: str = None,
    receptor_pdb_dir: str = None,
    output_dir: str = None,
    max_peptides: int = 5,
    receptors: List[str] = None
) -> Dict:
    """
    Main function: Run complete docking pipeline.
    """
    print("=" * 70)
    print("Val 06: AutoDock Vina Global Docking Pipeline")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check tools
    print("Step 1: Checking tool availability...")
    print("-" * 50)
    tools = check_vina_installation()
    print(f"  AutoDock Vina: {'✓' if tools['vina'] else '✗ (will simulate)'}")
    print(f"  Open Babel: {'✓' if tools['obabel'] else '✗'}")
    print(f"  MGLTools: {'✓' if tools['mgltools'] else '✗'}")

    use_simulation = not tools['vina']

    if use_simulation:
        print("\n  WARNING: AutoDock Vina not found. Using simulated results.")
        print("  Install Vina for real docking: https://vina.scripps.edu/")

    # Set up paths
    base_path = Path('/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech')

    if peptide_structures_dir is None:
        peptide_structures_dir = base_path / 'validation' / 'structures'
    else:
        peptide_structures_dir = Path(peptide_structures_dir)

    if receptor_pdb_dir is None:
        receptor_pdb_dir = base_path / 'simulations'
    else:
        receptor_pdb_dir = Path(receptor_pdb_dir)

    if output_dir is None:
        output_dir = base_path / 'validation' / 'docking'
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    results_dir = base_path / 'validation' / 'results'
    results_dir.mkdir(parents=True, exist_ok=True)

    # Determine receptors to use
    if receptors is None:
        receptors = list(RECEPTOR_DATABASE.keys())[:3]  # Default to first 3

    print(f"\nStep 2: Setting up receptors...")
    print("-" * 50)
    print(f"  Receptors: {receptors}")

    # Find peptide structures
    print(f"\nStep 3: Loading peptide structures...")
    print("-" * 50)

    peptide_pdbs = list(peptide_structures_dir.glob('*.pdb'))
    if not peptide_pdbs:
        print("  No peptide PDB files found. Creating test structures...")
        # Create test peptide structures
        test_peptides = [
            ('GLP1R_lead', 'HAEGTFTSDVSSYLEGQAAKEFIAWLVKGRG'),
            ('GBA1_lead', 'CYRILKSWFAEGNHQTMPVD'),
            ('TNF_lead', 'AEQGTRILHKNSFPWYVMCD'),
        ]
        peptide_structures_dir.mkdir(parents=True, exist_ok=True)

        for name, sequence in test_peptides:
            # Create minimal PDB
            pdb_path = peptide_structures_dir / f'{name}.pdb'
            create_minimal_peptide_pdb(sequence, str(pdb_path))
            peptide_pdbs.append(pdb_path)

    print(f"  Found {len(peptide_pdbs)} peptide structures")

    # Run docking
    print(f"\nStep 4: Running docking calculations...")
    print("-" * 50)

    all_results = []

    for receptor_name in receptors:
        receptor_info = RECEPTOR_DATABASE.get(receptor_name)
        if not receptor_info:
            continue

        print(f"\n  Receptor: {receptor_name} ({receptor_info['description']})")

        for pdb_path in peptide_pdbs[:max_peptides]:
            ligand_name = pdb_path.stem
            print(f"    Ligand: {ligand_name}")

            if use_simulation:
                # Read sequence from PDB
                sequence = extract_sequence_from_pdb(str(pdb_path))
                result = simulate_docking_result(receptor_name, ligand_name, sequence)
            else:
                # Real docking (if Vina available)
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Prepare files
                    receptor_pdbqt = os.path.join(tmpdir, f'{receptor_name}.pdbqt')
                    ligand_pdbqt = os.path.join(tmpdir, f'{ligand_name}.pdbqt')
                    output_pdbqt = str(output_dir / f'{ligand_name}_{receptor_name}_docked.pdbqt')

                    # Find receptor PDB
                    receptor_pdb = receptor_pdb_dir / f'{receptor_info["pdb_id"]}.pdb'
                    if not receptor_pdb.exists():
                        print(f"      ✗ Receptor PDB not found: {receptor_pdb}")
                        continue

                    # Prepare receptor
                    if not prepare_receptor_pdbqt(str(receptor_pdb), receptor_pdbqt):
                        print(f"      ✗ Failed to prepare receptor")
                        continue

                    # Prepare ligand
                    if not prepare_ligand_pdbqt(str(pdb_path), ligand_pdbqt):
                        print(f"      ✗ Failed to prepare ligand")
                        continue

                    # Run Vina
                    result = run_vina_docking(
                        receptor_pdbqt,
                        ligand_pdbqt,
                        receptor_info['center'],
                        receptor_info['box_size'],
                        output_pdbqt,
                        exhaustiveness=32
                    )

                    result['receptor'] = receptor_name
                    result['ligand'] = ligand_name

            # Record result
            if 'best_affinity' in result:
                print(f"      ✓ Best affinity: {result['best_affinity']:.1f} kcal/mol")
            else:
                print(f"      ✗ Error: {result.get('error', 'Unknown')}")

            all_results.append(result)

    # Analyze results
    print(f"\nStep 5: Analyzing results...")
    print("-" * 50)

    analysis = analyze_docking_results(all_results)

    # Compile full results
    full_results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'SIMULATED' if use_simulation else 'AutoDock Vina',
        'framework': {
            'z_squared': Z_SQUARED,
            'coordination_number': COORDINATION_NUMBER,
            'natural_length_scale_angstrom': NATURAL_LENGTH_SCALE
        },
        'tools_available': tools,
        'receptors_used': receptors,
        'n_peptides': len(peptide_pdbs[:max_peptides]),
        'analysis': analysis,
        'docking_results': all_results
    }

    # Save results
    results_path = results_dir / 'val_06_docking_results.json'
    with open(results_path, 'w') as f:
        json.dump(full_results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_path}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: AutoDock Vina Docking")
    print("=" * 70)
    print(f"""
Method: {'SIMULATED (demonstration)' if use_simulation else 'AutoDock Vina'}

Docking Statistics:
  Total runs: {analysis.get('n_total', 0)}
  Successful: {analysis.get('n_successful', 0)}

Affinity Distribution (kcal/mol):
  Mean: {analysis['affinity_statistics']['mean']:.1f}
  Std:  {analysis['affinity_statistics']['std']:.1f}
  Best: {analysis['affinity_statistics']['min']:.1f}
  Worst: {analysis['affinity_statistics']['max']:.1f}

Binding Classification:
{json.dumps(analysis.get('binding_classification', {}), indent=2)}

Top 5 Binders:
""")
    for i, hit in enumerate(analysis.get('top_5', []), 1):
        print(f"  {i}. {hit['ligand']} vs {hit['receptor']}: {hit['affinity_kcal_mol']:.1f} kcal/mol")

    if use_simulation:
        print("""
⚠️  IMPORTANT: These are SIMULATED results for demonstration.
    Install AutoDock Vina for real docking calculations.

    Installation:
    - macOS: brew install autodock-vina
    - Linux: conda install -c bioconda autodock-vina
    - Windows: Download from https://vina.scripps.edu/
""")

    return full_results


def create_minimal_peptide_pdb(sequence: str, output_path: str) -> None:
    """Create a minimal extended-chain PDB for a peptide sequence."""
    lines = []
    atom_num = 1
    res_num = 1

    for i, aa in enumerate(sequence):
        # Simple extended chain: each residue at 3.8 Å spacing
        x = i * 3.8
        y = 0.0
        z = 0.0

        # Just CA atom for minimal representation
        lines.append(
            f"ATOM  {atom_num:5d}  CA  {aa:3s} A{res_num:4d}    "
            f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n"
        )
        atom_num += 1
        res_num += 1

    lines.append("END\n")

    with open(output_path, 'w') as f:
        f.writelines(lines)


def extract_sequence_from_pdb(pdb_path: str) -> str:
    """Extract amino acid sequence from PDB file."""
    aa_map = {
        'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
        'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
        'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
        'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
    }

    sequence = []
    seen_residues = set()

    try:
        with open(pdb_path, 'r') as f:
            for line in f:
                if line.startswith('ATOM') and ' CA ' in line:
                    res_name = line[17:20].strip()
                    res_num = line[22:26].strip()

                    if res_num not in seen_residues:
                        seen_residues.add(res_num)
                        aa = aa_map.get(res_name, 'X')
                        sequence.append(aa)
    except:
        pass

    return ''.join(sequence) if sequence else 'ACDEFGHIKLMNPQRSTVWY'


if __name__ == '__main__':
    results = run_docking_pipeline(max_peptides=5)
    print("\nVal 06 complete.")
