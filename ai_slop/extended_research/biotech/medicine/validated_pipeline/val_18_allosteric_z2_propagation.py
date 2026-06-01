#!/usr/bin/env python3
"""
val_18_allosteric_z2_propagation.py

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

val_18_allosteric_z2_propagation.py - Allosteric Z² Wave Propagation Analysis

EMPIRICAL ALLOSTERIC ANALYSIS (NO MATHEMATICAL FORCING)
========================================================

CRITICAL: This script does NOT force atoms to converge toward Z².
Instead, it OBSERVES the native Voronoi volumes in real APO vs HOLO
structures and lets the physics dictate the geometry.

THE APPROACH:
1. Download real APO (unbound) and HOLO (ligand-bound) crystal structures
2. Calculate Voronoi volumes for hydrophobic core atoms in BOTH states
3. Measure the NATIVE ΔVolume without any mathematical forcing
4. Determine if ligand binding naturally shifts packing toward Z²

This is the honest test: Does nature actually pack proteins at Z² = 33.51 Å³?

PROTEIN PAIRS TESTED:
- Hemoglobin: Deoxy (APO) vs Oxy (HOLO) - classic allosteric system
- Kinases: Inactive vs Active conformations
- GPCRs: Apo vs Agonist-bound states

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 22, 2026
"""
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import requests
import time
import warnings

try:
    from scipy.spatial import Voronoi, ConvexHull, KDTree
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    warnings.warn("scipy required: pip install scipy")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³ - vacuum packing constant
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å
EXPANSION_MULTIPLIER = 1.0391  # 310K thermal expansion
BIOLOGICAL_DISTANCE = Z2_DISTANCE * EXPANSION_MULTIPLIER  # 6.02 Å

# Hydrophobic core residues
CORE_RESIDUES = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO', 'TYR'}

# Backbone atoms to exclude (we only want side-chain packing)
BACKBONE_ATOMS = {'N', 'CA', 'C', 'O', 'OXT', 'H', 'HA', 'HN'}

# PDB download URL
PDB_DOWNLOAD_URL = "https://files.rcsb.org/download/{}.pdb"

OUTPUT_DIR = Path(__file__).parent / "results" / "allosteric_propagation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CACHE_DIR = Path(__file__).parent / "pdb_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CLASSIC ALLOSTERIC PROTEIN PAIRS (APO vs HOLO)
# ============================================================================

ALLOSTERIC_PAIRS = {
    'hemoglobin': {
        'name': 'Hemoglobin (T-state vs R-state)',
        'apo_pdb': '2HHB',   # Deoxy-hemoglobin (T-state, low affinity)
        'holo_pdb': '1HHO',  # Oxy-hemoglobin (R-state, high affinity)
        'description': 'Classic allosteric transition: O2 binding shifts quaternary structure',
    },
    'pkA': {
        'name': 'Protein Kinase A (Inactive vs Active)',
        'apo_pdb': '1J3H',   # PKA without ATP
        'holo_pdb': '1ATP',  # PKA with ATP bound
        'description': 'Kinase activation loop rearrangement upon ATP binding',
    },
    'adenylate_kinase': {
        'name': 'Adenylate Kinase (Open vs Closed)',
        'apo_pdb': '4AKE',   # Open conformation (ligand-free)
        'holo_pdb': '1AKE',  # Closed conformation (with Ap5A inhibitor)
        'description': 'Large-scale lid domain closure upon substrate binding',
    },
}


def download_pdb(pdb_id: str) -> str:
    """Download PDB file with caching."""
    cache_file = CACHE_DIR / f"{pdb_id.upper()}.pdb"

    if cache_file.exists():
        return cache_file.read_text()

    try:
        url = PDB_DOWNLOAD_URL.format(pdb_id.upper())
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content = response.text
        cache_file.write_text(content)
        time.sleep(0.1)  # Be polite to RCSB
        return content
    except Exception as e:
        print(f"    Failed to download {pdb_id}: {e}")
        return ""


def is_sidechain_atom(atom_name: str) -> bool:
    """Check if atom is a side-chain atom (not backbone)."""
    atom_name = atom_name.strip().upper()
    if atom_name in BACKBONE_ATOMS:
        return False
    if atom_name.startswith('H') and len(atom_name) <= 2:
        return False
    return True


def parse_core_sidechain_atoms(pdb_content: str) -> Tuple[np.ndarray, List[int], List[str], List[str]]:
    """
    Parse PDB and extract CORE side-chain heavy atoms for Voronoi analysis.

    NO MATHEMATICAL FORCING - just extract native coordinates.

    Returns:
        positions: Nx3 array of atom positions
        residue_numbers: List of residue numbers
        residue_names: List of residue names (3-letter code)
        atom_names: List of atom names
    """
    positions = []
    residue_numbers = []
    residue_names = []
    atom_names = []

    for line in pdb_content.split('\n'):
        if not line.startswith('ATOM'):
            continue

        try:
            res_name = line[17:20].strip()

            # Only hydrophobic core residues
            if res_name not in CORE_RESIDUES:
                continue

            atom_name = line[12:16].strip()

            # Only side-chain atoms
            if not is_sidechain_atom(atom_name):
                continue

            # Skip hydrogens
            element = line[76:78].strip() if len(line) > 76 else atom_name[0]
            if element == 'H':
                continue

            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            res_num = int(line[22:26])
            chain = line[21]

            # Use chain + res_num for unique identification
            positions.append([x, y, z])
            residue_numbers.append(res_num)
            residue_names.append(res_name)
            atom_names.append(atom_name)

        except:
            continue

    return (np.array(positions) if positions else np.array([]).reshape(0, 3),
            residue_numbers, residue_names, atom_names)


def compute_voronoi_volumes_empirical(coords: np.ndarray) -> np.ndarray:
    """
    Compute NATIVE Voronoi volumes with mirror boundary conditions.

    NO FORCING - just measure what nature gives us.

    Returns array of volumes for each coordinate (NaN for unbounded cells).
    """
    if len(coords) < 10:
        return np.full(len(coords), np.nan)

    n_original = len(coords)

    # Mirror boundaries to handle edge effects
    min_coords = coords.min(axis=0)
    max_coords = coords.max(axis=0)

    mirrored = [coords]
    for axis in range(3):
        reflected_min = coords.copy()
        reflected_min[:, axis] = 2 * min_coords[axis] - reflected_min[:, axis]
        mirrored.append(reflected_min)

        reflected_max = coords.copy()
        reflected_max[:, axis] = 2 * max_coords[axis] - reflected_max[:, axis]
        mirrored.append(reflected_max)

    all_coords = np.vstack(mirrored)

    try:
        vor = Voronoi(all_coords)
        volumes = np.full(n_original, np.nan)

        for i in range(n_original):
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]

            if -1 in region or len(region) == 0:
                continue

            try:
                vertices = vor.vertices[region]
                hull = ConvexHull(vertices)
                volumes[i] = hull.volume
            except:
                continue

        return volumes
    except:
        return np.full(n_original, np.nan)


def identify_buried_atoms(positions: np.ndarray, burial_fraction: float = 0.5) -> np.ndarray:
    """
    Identify buried (core) atoms based on distance from centroid.

    Returns boolean mask of buried atoms.
    """
    if len(positions) < 10:
        return np.ones(len(positions), dtype=bool)

    centroid = np.mean(positions, axis=0)
    distances = np.linalg.norm(positions - centroid, axis=1)
    max_dist = np.max(distances)

    # Buried = inner fraction of protein
    burial_cutoff = max_dist * burial_fraction
    return distances < burial_cutoff


def analyze_allosteric_pair(pair_name: str, pair_info: Dict) -> Dict:
    """
    Analyze Voronoi volumes for an APO/HOLO pair.

    CRITICALLY: This measures NATIVE volumes without any forcing.
    """
    print(f"\n  Analyzing: {pair_info['name']}")
    print(f"  {pair_info['description']}")

    # Download structures
    print(f"    Downloading APO ({pair_info['apo_pdb']})...")
    apo_content = download_pdb(pair_info['apo_pdb'])

    print(f"    Downloading HOLO ({pair_info['holo_pdb']})...")
    holo_content = download_pdb(pair_info['holo_pdb'])

    if not apo_content or not holo_content:
        return {'error': 'Failed to download PDB structures'}

    # Parse structures
    print("    Parsing APO structure...")
    apo_pos, apo_res_nums, apo_res_names, apo_atoms = parse_core_sidechain_atoms(apo_content)

    print("    Parsing HOLO structure...")
    holo_pos, holo_res_nums, holo_res_names, holo_atoms = parse_core_sidechain_atoms(holo_content)

    print(f"    APO: {len(apo_pos)} core side-chain atoms")
    print(f"    HOLO: {len(holo_pos)} core side-chain atoms")

    if len(apo_pos) < 20 or len(holo_pos) < 20:
        return {'error': 'Too few core atoms extracted'}

    # Identify buried atoms (most relevant for packing analysis)
    apo_buried = identify_buried_atoms(apo_pos)
    holo_buried = identify_buried_atoms(holo_pos)

    apo_buried_pos = apo_pos[apo_buried]
    holo_buried_pos = holo_pos[holo_buried]

    print(f"    APO buried: {len(apo_buried_pos)} atoms")
    print(f"    HOLO buried: {len(holo_buried_pos)} atoms")

    # Compute NATIVE Voronoi volumes (no forcing!)
    print("    Computing NATIVE Voronoi volumes (APO)...")
    apo_volumes = compute_voronoi_volumes_empirical(apo_buried_pos)

    print("    Computing NATIVE Voronoi volumes (HOLO)...")
    holo_volumes = compute_voronoi_volumes_empirical(holo_buried_pos)

    # Filter valid volumes
    apo_valid = apo_volumes[~np.isnan(apo_volumes)]
    holo_valid = holo_volumes[~np.isnan(holo_volumes)]

    if len(apo_valid) < 10 or len(holo_valid) < 10:
        return {'error': 'Too few valid Voronoi cells'}

    print(f"    Valid Voronoi cells: APO={len(apo_valid)}, HOLO={len(holo_valid)}")

    # Statistics
    apo_mean = np.mean(apo_valid)
    apo_std = np.std(apo_valid)
    apo_median = np.median(apo_valid)

    holo_mean = np.mean(holo_valid)
    holo_std = np.std(holo_valid)
    holo_median = np.median(holo_valid)

    # Distance from Z² target
    apo_z2_deviation = np.abs(apo_mean - Z2_VOLUME)
    holo_z2_deviation = np.abs(holo_mean - Z2_VOLUME)

    # Did HOLO move CLOSER to Z²?
    z2_improvement = apo_z2_deviation - holo_z2_deviation  # Positive = HOLO closer

    # Statistical test: Are the distributions different?
    t_stat, p_value = stats.ttest_ind(apo_valid, holo_valid)

    # One-sample t-tests against Z²
    _, apo_z2_pvalue = stats.ttest_1samp(apo_valid, Z2_VOLUME)
    _, holo_z2_pvalue = stats.ttest_1samp(holo_valid, Z2_VOLUME)

    result = {
        'pair_name': pair_name,
        'pair_info': pair_info,
        'apo_pdb': pair_info['apo_pdb'],
        'holo_pdb': pair_info['holo_pdb'],
        'apo_n_atoms': len(apo_valid),
        'holo_n_atoms': len(holo_valid),
        'apo_statistics': {
            'mean': float(apo_mean),
            'std': float(apo_std),
            'median': float(apo_median),
            'min': float(np.min(apo_valid)),
            'max': float(np.max(apo_valid)),
            'deviation_from_z2': float(apo_z2_deviation),
            'z2_pvalue': float(apo_z2_pvalue),
        },
        'holo_statistics': {
            'mean': float(holo_mean),
            'std': float(holo_std),
            'median': float(holo_median),
            'min': float(np.min(holo_valid)),
            'max': float(np.max(holo_valid)),
            'deviation_from_z2': float(holo_z2_deviation),
            'z2_pvalue': float(holo_z2_pvalue),
        },
        'comparison': {
            'delta_mean': float(holo_mean - apo_mean),
            'z2_improvement': float(z2_improvement),
            'holo_closer_to_z2': bool(z2_improvement > 0),
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'significant': bool(p_value < 0.05),
        },
        'z2_target': Z2_VOLUME,
    }

    return result


def generate_comparison_plot(results: List[Dict], output_path: Path) -> None:
    """Generate visualization comparing APO vs HOLO volumes."""
    if not HAS_MATPLOTLIB:
        return

    valid_results = [r for r in results if 'error' not in r]
    if not valid_results:
        return

    n_pairs = len(valid_results)
    fig, axes = plt.subplots(1, n_pairs, figsize=(6 * n_pairs, 6))
    if n_pairs == 1:
        axes = [axes]

    for ax, result in zip(axes, valid_results):
        pair_name = result['pair_name']
        apo_mean = result['apo_statistics']['mean']
        apo_std = result['apo_statistics']['std']
        holo_mean = result['holo_statistics']['mean']
        holo_std = result['holo_statistics']['std']

        # Bar plot
        x = [0, 1]
        heights = [apo_mean, holo_mean]
        errors = [apo_std, holo_std]
        colors = ['steelblue', 'coral']
        labels = [f"APO\n({result['apo_pdb']})", f"HOLO\n({result['holo_pdb']})"]

        bars = ax.bar(x, heights, yerr=errors, capsize=5, color=colors,
                      edgecolor='black', alpha=0.7)

        # Z² reference line
        ax.axhline(y=Z2_VOLUME, color='green', linestyle='--', linewidth=2,
                   label=f'Z² = {Z2_VOLUME:.2f} Å³')

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylabel('Mean Voronoi Volume (Å³)', fontsize=12)
        ax.set_title(f"{result['pair_info']['name']}\n"
                     f"ΔV = {result['comparison']['delta_mean']:+.2f} Å³",
                     fontsize=11)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Indicate if HOLO is closer to Z²
        if result['comparison']['holo_closer_to_z2']:
            ax.annotate('HOLO closer to Z²', xy=(0.5, 0.02), xycoords='axes fraction',
                       ha='center', fontsize=9, color='green', fontweight='bold')
        else:
            ax.annotate('APO closer to Z²', xy=(0.5, 0.02), xycoords='axes fraction',
                       ha='center', fontsize=9, color='red')

    plt.suptitle('EMPIRICAL Allosteric Analysis: Native Voronoi Volumes\n'
                 '(No mathematical forcing - observing natural packing)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"    Plot saved: {output_path}")


def main():
    """Main execution: Empirical allosteric Z² analysis."""
    print("=" * 80)
    print("EMPIRICAL ALLOSTERIC Z² ANALYSIS")
    print("Observing NATIVE Voronoi Volumes in APO vs HOLO Structures")
    print("=" * 80)

    if not HAS_SCIPY:
        print("\nERROR: scipy required. Install with: pip install scipy")
        return None

    print(f"""
    CRITICAL: NO MATHEMATICAL FORCING
    ─────────────────────────────────
    Previous version FORCED atoms to converge toward Z² using:
        holo_volumes = apo_volumes - (apo_volumes - Z²) × decay_function

    This was RIGGING THE PHYSICS. Of course 100% converged when we
    mathematically forced them to converge!

    THIS VERSION:
    1. Downloads REAL APO and HOLO crystal structures from the PDB
    2. Calculates NATIVE Voronoi volumes (no forcing)
    3. Asks: Does ligand binding NATURALLY shift packing toward Z²?

    The honest answer might be "no" - and that's scientifically valid.

    Z² Target: {Z2_VOLUME:.4f} Å³
""")

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Empirical Allosteric Voronoi Analysis (NO FORCING)',
        'warning': 'This analysis uses NATIVE volumes only. No mathematical forcing applied.',
        'constants': {
            'Z2_volume_cubic_angstrom': Z2_VOLUME,
            'Z2_distance_angstrom': Z2_DISTANCE,
            'expansion_multiplier': EXPANSION_MULTIPLIER,
            'biological_distance': BIOLOGICAL_DISTANCE,
        },
        'pairs_analyzed': [],
    }

    all_pair_results = []

    for pair_name, pair_info in ALLOSTERIC_PAIRS.items():
        print(f"\n  {'='*60}")
        pair_result = analyze_allosteric_pair(pair_name, pair_info)
        all_pair_results.append(pair_result)
        results['pairs_analyzed'].append(pair_result)

        if 'error' in pair_result:
            print(f"    ERROR: {pair_result['error']}")
            continue

        # Print results
        apo = pair_result['apo_statistics']
        holo = pair_result['holo_statistics']
        comp = pair_result['comparison']

        print(f"""
    NATIVE VORONOI VOLUMES (no forcing):
    ─────────────────────────────────────
    APO ({pair_result['apo_pdb']}):
      Mean: {apo['mean']:.3f} ± {apo['std']:.3f} Å³
      Distance from Z²: {apo['deviation_from_z2']:.3f} Å³

    HOLO ({pair_result['holo_pdb']}):
      Mean: {holo['mean']:.3f} ± {holo['std']:.3f} Å³
      Distance from Z²: {holo['deviation_from_z2']:.3f} Å³

    COMPARISON:
      ΔVolume (HOLO - APO): {comp['delta_mean']:+.3f} Å³
      Z² improvement: {comp['z2_improvement']:+.3f} Å³
      HOLO closer to Z²: {comp['holo_closer_to_z2']}
      Significant (p<0.05): {comp['significant']} (p={comp['p_value']:.2e})
""")

    # Generate plot
    if HAS_MATPLOTLIB:
        plot_path = OUTPUT_DIR / 'empirical_allosteric_comparison.png'
        generate_comparison_plot(all_pair_results, plot_path)

    # Summary
    print("\n" + "=" * 80)
    print("EMPIRICAL ALLOSTERIC ANALYSIS SUMMARY")
    print("=" * 80)

    valid_results = [r for r in all_pair_results if 'error' not in r]
    n_closer = sum(1 for r in valid_results if r['comparison']['holo_closer_to_z2'])
    n_total = len(valid_results)

    print(f"""
    Pairs analyzed: {n_total}
    HOLO closer to Z²: {n_closer}/{n_total}

    Z² TARGET: {Z2_VOLUME:.4f} Å³
""")

    for r in valid_results:
        arrow = "→" if r['comparison']['holo_closer_to_z2'] else "←"
        direction = "CLOSER" if r['comparison']['holo_closer_to_z2'] else "FARTHER"
        print(f"    {r['pair_name']:20} | APO: {r['apo_statistics']['mean']:.2f} {arrow} HOLO: {r['holo_statistics']['mean']:.2f} | {direction} to Z²")

    # Verdict
    print("\n    " + "=" * 60)
    if n_total > 0 and n_closer > n_total / 2:
        print(f"    VERDICT: TREND TOWARD Z² CONVERGENCE")
        print(f"    {n_closer}/{n_total} proteins showed HOLO closer to Z² = 33.51 Å³")
        results['verdict'] = 'TREND_TOWARD_Z2'
    elif n_total > 0:
        print(f"    VERDICT: NO CLEAR Z² CONVERGENCE")
        print(f"    Only {n_closer}/{n_total} proteins showed HOLO closer to Z²")
        results['verdict'] = 'NO_CLEAR_TREND'
    else:
        print("    VERDICT: INSUFFICIENT DATA")
        results['verdict'] = 'INSUFFICIENT_DATA'

    print("    " + "=" * 60)
    print("""
    NOTE: This is the HONEST result. Unlike the previous version that
    mathematically forced 100% convergence, this measures NATIVE volumes.

    If nature doesn't pack proteins at Z², that's a valid scientific finding.
""")

    # Save results
    output_path = OUTPUT_DIR / 'allosteric_z2_propagation_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"  Results saved: {output_path}")

    return results


if __name__ == '__main__':
    results = main()
