#!/usr/bin/env python3
"""
inv_04_core_isolation.py - Hydrophobic Core Isolation Engine

Strips away noisy surface atoms and isolates the vacuum-like
hydrophobic cores of proteins where Z² mathematics should emerge.

Strategy:
1. Calculate Relative Solvent Accessible Surface Area (rSASA)
2. Keep only atoms with rSASA < 0.05 (5%) - completely buried
3. Remove hydrogen atoms (unreliable X-ray positions)
4. Output pure crystalline core coordinates

The hydrophobic core is a quasi-solid state where water is excluded
and atoms pack under thermodynamic pressure. If Z² governs atomic
packing, its fingerprint is here.

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "core_isolation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Where to find PDB files
PDB_DIRS = [
    Path(__file__).parent / "data" / "massive_pdb_set",
    Path(__file__).parent / "data" / "pdb_topology",
]

print("=" * 80)
print("HYDROPHOBIC CORE ISOLATION ENGINE")
print("Stripping Surface Noise, Exposing Crystalline Cores")
print("=" * 80)
print()

# =============================================================================
# CONSTANTS
# =============================================================================

# Solvent accessibility threshold
SASA_THRESHOLD = 0.05  # 5% - atoms more exposed than this are "surface"

# Van der Waals radii for SASA calculation (Å)
VDW_RADII = {
    'C': 1.70, 'N': 1.55, 'O': 1.52, 'S': 1.80, 'P': 1.80,
    'H': 1.20,  # Will be excluded anyway
    'FE': 1.40, 'ZN': 1.39, 'MG': 1.73, 'CA': 1.97, 'MN': 1.39,
}

# Probe radius for SASA (water molecule)
PROBE_RADIUS = 1.4  # Å

# Reference SASA values for fully exposed residues (Å²)
# From Miller et al. (1987) or Chothia (1976)
REF_SASA = {
    'ALA': 113, 'ARG': 241, 'ASN': 158, 'ASP': 151, 'CYS': 140,
    'GLN': 189, 'GLU': 183, 'GLY': 85, 'HIS': 194, 'ILE': 182,
    'LEU': 180, 'LYS': 211, 'MET': 204, 'PHE': 218, 'PRO': 143,
    'SER': 122, 'THR': 146, 'TRP': 259, 'TYR': 229, 'VAL': 160,
}

# Hydrophobic residues (for core identification)
HYDROPHOBIC = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO', 'TYR', 'CYS'}

print(f"SASA threshold: {SASA_THRESHOLD * 100}%")
print(f"Probe radius: {PROBE_RADIUS} Å")
print()


# =============================================================================
# PDB PARSING
# =============================================================================

def parse_pdb_atoms(pdb_path: Path) -> Tuple[np.ndarray, List[Dict]]:
    """
    Parse PDB file and extract all atom data.
    Returns (coordinates, atom_info_list).
    """
    coords = []
    atoms = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    atom_name = line[12:16].strip()
                    res_name = line[17:20].strip()
                    chain = line[21]
                    res_num = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])

                    # Element (from columns 77-78 or infer from atom name)
                    element = line[76:78].strip()
                    if not element:
                        element = atom_name[0]

                    coords.append([x, y, z])
                    atoms.append({
                        'atom_name': atom_name,
                        'res_name': res_name,
                        'res_num': res_num,
                        'chain': chain,
                        'element': element,
                        'is_hydrogen': element == 'H',
                        'is_hydrophobic_res': res_name in HYDROPHOBIC,
                    })

                except (ValueError, IndexError):
                    continue

    return np.array(coords), atoms


# =============================================================================
# SOLVENT ACCESSIBLE SURFACE AREA (SHRAKE-RUPLEY)
# =============================================================================

def shrake_rupley_sasa(coords: np.ndarray, elements: List[str],
                        n_points: int = 100) -> np.ndarray:
    """
    Calculate Solvent Accessible Surface Area using Shrake-Rupley algorithm.

    For each atom:
    1. Generate sphere of test points at (radius + probe_radius)
    2. Count how many points are NOT occluded by other atoms
    3. SASA = (n_exposed / n_total) * 4π(r + probe)²
    """
    n_atoms = len(coords)
    sasa = np.zeros(n_atoms)

    # Generate Fibonacci sphere points (uniform distribution)
    golden_ratio = (1 + np.sqrt(5)) / 2
    indices = np.arange(n_points)
    theta = 2 * np.pi * indices / golden_ratio
    phi = np.arccos(1 - 2 * (indices + 0.5) / n_points)

    # Unit sphere points
    unit_sphere = np.column_stack([
        np.sin(phi) * np.cos(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(phi)
    ])

    # Get radii
    radii = np.array([VDW_RADII.get(e, 1.70) for e in elements])

    for i in range(n_atoms):
        r_i = radii[i] + PROBE_RADIUS

        # Test points for atom i
        test_points = coords[i] + r_i * unit_sphere

        # Check occlusion by other atoms
        exposed = np.ones(n_points, dtype=bool)

        for j in range(n_atoms):
            if i == j:
                continue

            r_j = radii[j] + PROBE_RADIUS

            # Distance from test points to atom j center
            dist_sq = np.sum((test_points - coords[j])**2, axis=1)

            # Occluded if inside atom j's sphere
            exposed &= (dist_sq > r_j**2)

        # Calculate SASA
        n_exposed = np.sum(exposed)
        surface_area = 4 * np.pi * r_i**2
        sasa[i] = (n_exposed / n_points) * surface_area

    return sasa


def calculate_relative_sasa(sasa: np.ndarray, atoms: List[Dict]) -> np.ndarray:
    """
    Calculate relative SASA (fraction of max possible).
    """
    rsasa = np.zeros(len(sasa))

    for i, atom in enumerate(atoms):
        res_name = atom['res_name']
        ref = REF_SASA.get(res_name, 200)  # Default reference

        # Scale by atom type (approximate)
        if atom['atom_name'] in ['CA', 'C', 'N', 'O']:
            ref_atom = ref * 0.25  # Backbone atoms
        else:
            ref_atom = ref * 0.5  # Sidechain atoms

        rsasa[i] = sasa[i] / ref_atom if ref_atom > 0 else 0

    return rsasa


def fast_burial_approximation(coords: np.ndarray, atoms: List[Dict],
                               cutoff: float = 10.0) -> np.ndarray:
    """
    Fast approximation of burial using neighbor counting.

    Atoms with many neighbors within cutoff are likely buried.
    This is much faster than full SASA for large datasets.
    """
    from scipy.spatial.distance import cdist

    n_atoms = len(coords)

    # Pairwise distances
    distances = cdist(coords, coords)

    # Count neighbors within cutoff
    neighbor_counts = np.sum(distances < cutoff, axis=1) - 1  # Subtract self

    # Normalize to [0, 1] range (higher = more buried)
    max_neighbors = np.max(neighbor_counts)
    if max_neighbors > 0:
        burial_score = neighbor_counts / max_neighbors
    else:
        burial_score = np.zeros(n_atoms)

    return burial_score


# =============================================================================
# CORE ISOLATION
# =============================================================================

def isolate_hydrophobic_core(coords: np.ndarray, atoms: List[Dict],
                              use_fast_method: bool = True) -> Tuple[np.ndarray, List[Dict], np.ndarray]:
    """
    Isolate the buried hydrophobic core atoms.

    Returns:
        core_coords: Coordinates of core atoms
        core_atoms: Atom info for core atoms
        burial_scores: Burial score for each original atom
    """
    n_atoms = len(coords)

    # Remove hydrogens first
    non_h_mask = np.array([not atom['is_hydrogen'] for atom in atoms])
    heavy_coords = coords[non_h_mask]
    heavy_atoms = [atoms[i] for i in range(n_atoms) if non_h_mask[i]]

    if len(heavy_coords) == 0:
        return np.array([]), [], np.array([])

    # Calculate burial
    if use_fast_method:
        # Fast neighbor-count method
        burial = fast_burial_approximation(heavy_coords, heavy_atoms)
        # Convert to rsasa-like metric (inverted: high burial = low rsasa)
        rsasa = 1 - burial
    else:
        # Full SASA calculation
        elements = [atom['element'] for atom in heavy_atoms]
        sasa = shrake_rupley_sasa(heavy_coords, elements)
        rsasa = calculate_relative_sasa(sasa, heavy_atoms)

    # Select buried atoms (rsasa < threshold)
    buried_mask = rsasa < SASA_THRESHOLD

    # Additionally filter for hydrophobic residues (optional, for purer core)
    hydrophobic_mask = np.array([atom['is_hydrophobic_res'] for atom in heavy_atoms])

    # Core = buried AND (optionally) hydrophobic
    core_mask = buried_mask  # Use all buried atoms for now

    core_coords = heavy_coords[core_mask]
    core_atoms = [heavy_atoms[i] for i in range(len(heavy_atoms)) if core_mask[i]]

    return core_coords, core_atoms, rsasa


# =============================================================================
# PROCESS SINGLE PROTEIN
# =============================================================================

def process_protein(pdb_path: Path) -> Optional[Dict]:
    """
    Process a single protein and extract its hydrophobic core.
    """
    result = {
        'pdb_file': pdb_path.name,
        'pdb_id': pdb_path.stem[:4].upper(),
    }

    try:
        # Parse structure
        coords, atoms = parse_pdb_atoms(pdb_path)

        if len(coords) < 50:
            result['error'] = 'Too few atoms'
            return result

        result['n_total_atoms'] = len(coords)
        result['n_heavy_atoms'] = sum(1 for a in atoms if not a['is_hydrogen'])

        # Isolate core
        core_coords, core_atoms, burial = isolate_hydrophobic_core(coords, atoms)

        result['n_core_atoms'] = len(core_coords)
        result['core_fraction'] = len(core_coords) / result['n_heavy_atoms'] if result['n_heavy_atoms'] > 0 else 0

        if len(core_coords) < 10:
            result['error'] = 'Core too small'
            return result

        # Save core coordinates
        result['core_coords'] = core_coords.tolist()
        result['success'] = True

        # Statistics
        result['stats'] = {
            'mean_burial': float(np.mean(1 - burial)),
            'core_density': len(core_coords) / (4/3 * np.pi * (np.max(np.linalg.norm(core_coords - np.mean(core_coords, axis=0), axis=1)) + 1)**3) if len(core_coords) > 0 else 0,
        }

    except Exception as e:
        result['error'] = str(e)
        result['success'] = False

    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Process all PDB files and isolate hydrophobic cores.
    """
    # Find PDB files
    pdb_files = []
    for pdb_dir in PDB_DIRS:
        if pdb_dir.exists():
            pdb_files.extend(list(pdb_dir.glob("*.pdb")))

    # Also check for downloaded test structures
    test_dir = OUTPUT_DIR.parent / "thermal_bridge"
    if test_dir.exists():
        pdb_files.extend(list(test_dir.glob("*.pdb")))

    # Download sample if none found
    if not pdb_files:
        print("No PDB files found. Downloading sample structures...")
        import urllib.request

        sample_pdbs = ['1UBQ', '1CRN', '1L2Y', '2GB1', '1VII']
        for pdb_id in sample_pdbs:
            try:
                url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
                pdb_path = OUTPUT_DIR / f"{pdb_id}.pdb"
                urllib.request.urlretrieve(url, pdb_path)
                pdb_files.append(pdb_path)
                print(f"  Downloaded: {pdb_id}")
            except Exception as e:
                print(f"  Failed to download {pdb_id}: {e}")

    print(f"\nProcessing {len(pdb_files)} structures...")

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Hydrophobic Core Isolation (Burial Analysis)',
        'sasa_threshold': SASA_THRESHOLD,
        'proteins': [],
        'all_core_coords': [],  # Aggregated coordinates
    }

    successful = 0
    total_core_atoms = 0

    for i, pdb_path in enumerate(pdb_files):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i+1}/{len(pdb_files)}...")

        protein_result = process_protein(pdb_path)

        if protein_result and protein_result.get('success'):
            successful += 1
            total_core_atoms += protein_result['n_core_atoms']

            # Store core coordinates
            core_coords = np.array(protein_result['core_coords'])
            results['all_core_coords'].append({
                'pdb_id': protein_result['pdb_id'],
                'coords': core_coords.tolist(),
                'n_atoms': len(core_coords),
            })

            # Don't store full coords in protein results (save space)
            protein_result.pop('core_coords', None)

        results['proteins'].append(protein_result)

    # Summary
    print("\n" + "=" * 80)
    print("CORE ISOLATION SUMMARY")
    print("=" * 80)

    print(f"\n  Structures processed: {len(pdb_files)}")
    print(f"  Successful isolations: {successful}")
    print(f"  Total core atoms extracted: {total_core_atoms}")

    if successful > 0:
        core_fractions = [p['core_fraction'] for p in results['proteins']
                         if p.get('success') and 'core_fraction' in p]
        print(f"  Mean core fraction: {np.mean(core_fractions):.1%}")

    results['summary'] = {
        'n_proteins': len(pdb_files),
        'n_successful': successful,
        'total_core_atoms': total_core_atoms,
        'mean_core_fraction': float(np.mean(core_fractions)) if core_fractions else 0,
    }

    # Save core coordinates for Voronoi/Delaunay analysis
    core_data_path = OUTPUT_DIR / "isolated_cores.json"
    with open(core_data_path, 'w') as f:
        json.dump({
            'timestamp': results['timestamp'],
            'n_proteins': successful,
            'total_atoms': total_core_atoms,
            'cores': results['all_core_coords'],
        }, f, indent=2)

    print(f"\n  Core data: {core_data_path}")

    # Save full results (without coords)
    results.pop('all_core_coords', None)
    json_path = OUTPUT_DIR / "core_isolation_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"  Results: {json_path}")

    print("\n  NEXT: Run inv_05_voronoi_z2_volume.py on isolated cores")
    print("        Run inv_06_delaunay_z2_distance.py on isolated cores")

    return results


if __name__ == "__main__":
    main()
