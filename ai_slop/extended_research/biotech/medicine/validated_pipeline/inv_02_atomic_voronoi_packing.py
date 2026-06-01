#!/usr/bin/env python3
"""
inv_02_atomic_voronoi_packing.py

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

inv_02_atomic_voronoi_packing.py - Atomic Packing Analysis via Voronoi Tessellation

Tests the hypothesis that Z² = 32π/3 governs atomic packing density
at the atomic level, which then scales up to macroscopic biology.

Instead of measuring backbone topology (H1 death radii), we measure:
- Voronoi volumes of individual atoms in hydrophobic cores
- Mean distances between neighboring heavy atoms
- Packing efficiency

The Target: Does the mean atomic neighbor distance match √(Z²) or a
mathematical derivative (√(Z²)/2, √(Z²)/√2, etc.)?

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
from scipy.spatial import Voronoi, ConvexHull, Delaunay
from scipy.spatial.distance import cdist
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "atomic_packing"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("ATOMIC VORONOI PACKING ANALYSIS")
print("Hunting for Z² at the Atomic Level")
print("=" * 80)
print()

# =============================================================================
# Z² MATHEMATICAL CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.79 Å

# Possible Z² derivatives at atomic scale
Z2_DERIVATIVES = {
    'sqrt_z2': SQRT_Z2,                    # 5.79 Å
    'sqrt_z2_div_2': SQRT_Z2 / 2,          # 2.89 Å (half)
    'sqrt_z2_div_sqrt2': SQRT_Z2 / np.sqrt(2),  # 4.09 Å
    'sqrt_z2_div_pi': SQRT_Z2 / np.pi,     # 1.84 Å
    'cubert_z2': Z_SQUARED ** (1/3),       # 3.22 Å
    'z2_div_10': Z_SQUARED / 10,           # 3.35 Å
}

print("Z² Mathematical Constants:")
print(f"  Z² = 32π/3 = {Z_SQUARED:.4f}")
print(f"  √(Z²) = {SQRT_Z2:.4f} Å")
print("\nPossible atomic-scale derivatives:")
for name, value in Z2_DERIVATIVES.items():
    print(f"  {name}: {value:.4f} Å")
print()

# =============================================================================
# HYDROPHOBIC RESIDUES (core-forming)
# =============================================================================

HYDROPHOBIC = {'ALA', 'VAL', 'LEU', 'ILE', 'MET', 'PHE', 'TRP', 'PRO', 'TYR'}

# Heavy atoms (non-hydrogen)
HEAVY_ELEMENTS = {'C', 'N', 'O', 'S', 'P'}


# =============================================================================
# PDB PARSING
# =============================================================================

def parse_pdb_heavy_atoms(pdb_path: Path) -> Tuple[np.ndarray, List[Dict]]:
    """
    Parse PDB file and extract all heavy atom coordinates.
    Returns (coordinates_array, atom_info_list).
    """
    coords = []
    atoms = []

    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                try:
                    element = line[76:78].strip()
                    if not element:
                        element = line[12:14].strip()[0]  # Fallback

                    # Skip hydrogens
                    if element == 'H':
                        continue

                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])

                    atom_name = line[12:16].strip()
                    res_name = line[17:20].strip()
                    res_num = int(line[22:26])
                    chain = line[21]

                    coords.append([x, y, z])
                    atoms.append({
                        'atom_name': atom_name,
                        'res_name': res_name,
                        'res_num': res_num,
                        'chain': chain,
                        'element': element,
                        'is_hydrophobic': res_name in HYDROPHOBIC,
                    })

                except (ValueError, IndexError):
                    continue

    return np.array(coords), atoms


def identify_hydrophobic_core(coords: np.ndarray, atoms: List[Dict],
                               core_threshold: float = 0.7) -> np.ndarray:
    """
    Identify atoms in the hydrophobic core.

    Strategy: Atoms are in the core if they have high burial
    (many neighbors within 8Å) and are in hydrophobic residues.
    """
    n_atoms = len(coords)
    if n_atoms == 0:
        return np.array([])

    # Calculate pairwise distances
    distances = cdist(coords, coords)

    # Count neighbors within 8Å for each atom
    neighbor_counts = np.sum(distances < 8.0, axis=1) - 1  # Subtract self

    # Threshold for "buried" (high neighbor count)
    burial_threshold = np.percentile(neighbor_counts, 100 * core_threshold)

    # Core atoms: buried AND in hydrophobic residues
    core_indices = []
    for i, (count, atom) in enumerate(zip(neighbor_counts, atoms)):
        if count >= burial_threshold and atom['is_hydrophobic']:
            core_indices.append(i)

    return np.array(core_indices)


# =============================================================================
# VORONOI ANALYSIS
# =============================================================================

def compute_voronoi_volumes(coords: np.ndarray) -> np.ndarray:
    """
    Compute Voronoi cell volumes for each point.
    """
    if len(coords) < 4:
        return np.array([])

    try:
        vor = Voronoi(coords)

        volumes = []
        for i, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]

            if -1 in region or len(region) == 0:
                # Infinite region (boundary atom)
                volumes.append(np.nan)
            else:
                try:
                    vertices = vor.vertices[region]
                    hull = ConvexHull(vertices)
                    volumes.append(hull.volume)
                except Exception:
                    volumes.append(np.nan)

        return np.array(volumes)

    except Exception as e:
        print(f"    Voronoi failed: {e}")
        return np.array([np.nan] * len(coords))


def compute_neighbor_distances(coords: np.ndarray,
                                max_dist: float = 6.0) -> List[float]:
    """
    Compute all pairwise distances between neighboring atoms.
    Neighbors are defined as atoms within max_dist Angstroms.
    """
    if len(coords) < 2:
        return []

    distances = cdist(coords, coords)

    # Get upper triangle (avoid duplicates and self-distances)
    neighbor_dists = []
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            d = distances[i, j]
            if d < max_dist and d > 1.0:  # Exclude bonded atoms (<1.6Å)
                neighbor_dists.append(d)

    return neighbor_dists


def compute_delaunay_edges(coords: np.ndarray) -> List[float]:
    """
    Compute edge lengths from Delaunay triangulation.
    This gives the natural neighbor distances.
    """
    if len(coords) < 4:
        return []

    try:
        tri = Delaunay(coords)

        edge_lengths = []
        edges_seen = set()

        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    edge = tuple(sorted([simplex[i], simplex[j]]))
                    if edge not in edges_seen:
                        edges_seen.add(edge)
                        dist = np.linalg.norm(coords[edge[0]] - coords[edge[1]])
                        edge_lengths.append(dist)

        return edge_lengths

    except Exception as e:
        print(f"    Delaunay failed: {e}")
        return []


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def find_best_z2_match(empirical_value: float, empirical_std: float) -> Dict:
    """
    Find which Z² derivative best matches the empirical value.
    """
    best_match = None
    best_z_score = float('inf')

    for name, predicted in Z2_DERIVATIVES.items():
        z_score = abs(empirical_value - predicted) / empirical_std
        if z_score < best_z_score:
            best_z_score = z_score
            best_match = {
                'name': name,
                'predicted': predicted,
                'z_score': z_score,
                'within_2sigma': z_score < 2.0,
            }

    return best_match


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_protein(pdb_path: Path) -> Dict:
    """
    Full atomic packing analysis on a single protein.
    """
    result = {
        'pdb_file': pdb_path.name,
        'timestamp': datetime.now().isoformat(),
    }

    try:
        # Parse structure
        coords, atoms = parse_pdb_heavy_atoms(pdb_path)
        result['n_heavy_atoms'] = len(coords)

        if len(coords) < 50:
            result['error'] = 'Too few atoms'
            return result

        # Identify hydrophobic core
        core_indices = identify_hydrophobic_core(coords, atoms)
        result['n_core_atoms'] = len(core_indices)

        if len(core_indices) < 20:
            result['error'] = 'Hydrophobic core too small'
            return result

        core_coords = coords[core_indices]

        # Compute Voronoi volumes
        volumes = compute_voronoi_volumes(core_coords)
        valid_volumes = volumes[~np.isnan(volumes)]

        if len(valid_volumes) > 0:
            result['voronoi'] = {
                'mean_volume_A3': float(np.mean(valid_volumes)),
                'std_volume_A3': float(np.std(valid_volumes)),
                'n_valid': len(valid_volumes),
            }

        # Compute neighbor distances (Delaunay)
        edge_lengths = compute_delaunay_edges(core_coords)

        if len(edge_lengths) > 10:
            mean_edge = np.mean(edge_lengths)
            std_edge = np.std(edge_lengths)

            result['delaunay_edges'] = {
                'mean_distance_A': float(mean_edge),
                'std_distance_A': float(std_edge),
                'n_edges': len(edge_lengths),
            }

            # Find best Z² match
            if std_edge > 0:
                result['z2_match'] = find_best_z2_match(mean_edge, std_edge)

        # Compute direct neighbor distances
        neighbor_dists = compute_neighbor_distances(core_coords, max_dist=5.0)

        if len(neighbor_dists) > 10:
            result['close_neighbors'] = {
                'mean_distance_A': float(np.mean(neighbor_dists)),
                'std_distance_A': float(np.std(neighbor_dists)),
                'n_pairs': len(neighbor_dists),
            }

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)
        result['success'] = False

    return result


def aggregate_results(protein_results: List[Dict]) -> Dict:
    """
    Aggregate results across all proteins.
    """
    all_delaunay_means = []
    all_voronoi_means = []
    all_neighbor_means = []

    for res in protein_results:
        if not res.get('success'):
            continue

        if 'delaunay_edges' in res:
            all_delaunay_means.append(res['delaunay_edges']['mean_distance_A'])

        if 'voronoi' in res:
            all_voronoi_means.append(res['voronoi']['mean_volume_A3'])

        if 'close_neighbors' in res:
            all_neighbor_means.append(res['close_neighbors']['mean_distance_A'])

    aggregate = {
        'n_proteins_analyzed': len([r for r in protein_results if r.get('success')]),
    }

    if all_delaunay_means:
        mean_d = np.mean(all_delaunay_means)
        std_d = np.std(all_delaunay_means)
        aggregate['delaunay_global'] = {
            'mean_A': float(mean_d),
            'std_A': float(std_d),
            'se_A': float(std_d / np.sqrt(len(all_delaunay_means))),
        }

        # Test against Z² derivatives
        print("\n  DELAUNAY EDGE ANALYSIS:")
        print(f"    Global mean: {mean_d:.4f} ± {std_d:.4f} Å")

        for name, predicted in Z2_DERIVATIVES.items():
            z_score = abs(mean_d - predicted) / std_d if std_d > 0 else float('inf')
            match_str = "✓ MATCH" if z_score < 2.0 else ""
            print(f"    vs {name} ({predicted:.4f}): z={z_score:.2f} {match_str}")

        aggregate['z2_tests'] = {}
        for name, predicted in Z2_DERIVATIVES.items():
            z_score = abs(mean_d - predicted) / std_d if std_d > 0 else float('inf')
            aggregate['z2_tests'][name] = {
                'predicted_A': predicted,
                'z_score': float(z_score),
                'match': z_score < 2.0,
            }

    if all_voronoi_means:
        aggregate['voronoi_global'] = {
            'mean_volume_A3': float(np.mean(all_voronoi_means)),
            'std_volume_A3': float(np.std(all_voronoi_means)),
        }

    if all_neighbor_means:
        aggregate['close_neighbor_global'] = {
            'mean_A': float(np.mean(all_neighbor_means)),
            'std_A': float(np.std(all_neighbor_means)),
        }

    return aggregate


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run atomic packing analysis on available protein structures.
    """
    # Find PDB files
    pdb_dirs = [
        Path(__file__).parent / "data" / "massive_pdb_set",
        Path(__file__).parent / "results" / "md_stability",
    ]

    pdb_files = []
    for pdb_dir in pdb_dirs:
        if pdb_dir.exists():
            pdb_files.extend(list(pdb_dir.glob("*.pdb")))

    if not pdb_files:
        print("No PDB files found. Downloading test structure...")

        # Download a test structure (ubiquitin)
        import urllib.request
        test_pdb = OUTPUT_DIR / "1UBQ.pdb"

        try:
            url = "https://files.rcsb.org/download/1UBQ.pdb"
            urllib.request.urlretrieve(url, test_pdb)
            pdb_files = [test_pdb]
            print(f"  Downloaded: {test_pdb}")
        except Exception as e:
            print(f"  Download failed: {e}")
            return

    print(f"\nAnalyzing {len(pdb_files)} structures...")

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Atomic Voronoi Packing Analysis',
        'hypothesis': 'Z² = 32π/3 governs atomic packing distances',
        'z2_value': Z_SQUARED,
        'sqrt_z2': SQRT_Z2,
        'proteins': [],
    }

    for i, pdb_path in enumerate(pdb_files[:100]):  # Limit for demo
        if (i + 1) % 10 == 0:
            print(f"  Processing {i+1}/{min(len(pdb_files), 100)}...")

        protein_result = analyze_protein(pdb_path)
        results['proteins'].append(protein_result)

    # Aggregate
    results['aggregate'] = aggregate_results(results['proteins'])

    # Summary
    print("\n" + "=" * 80)
    print("ATOMIC PACKING ANALYSIS SUMMARY")
    print("=" * 80)

    agg = results['aggregate']
    print(f"\n  Proteins analyzed: {agg['n_proteins_analyzed']}")

    if 'delaunay_global' in agg:
        d = agg['delaunay_global']
        print(f"\n  GLOBAL DELAUNAY EDGE LENGTH:")
        print(f"    {d['mean_A']:.4f} ± {d['std_A']:.4f} Å (SE: {d['se_A']:.4f})")

        print(f"\n  COMPARISON TO √(Z²) = {SQRT_Z2:.4f} Å:")
        if 'z2_tests' in agg:
            for name, test in agg['z2_tests'].items():
                status = "✓" if test['match'] else "✗"
                print(f"    {status} {name}: predicted={test['predicted_A']:.4f}, z={test['z_score']:.2f}")

    # Save results
    json_path = OUTPUT_DIR / "atomic_packing_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {json_path}")

    return results


if __name__ == "__main__":
    main()
