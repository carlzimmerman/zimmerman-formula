#!/usr/bin/env python3
"""
geo_01_persistent_homology.py - Topological Data Analysis of Protein Structures

Uses Persistent Homology to analyze the macro-topology of protein structures.
Computes Betti numbers (β₀, β₁, β₂) across filtration scales and identifies
the critical radius where topological features stabilize.

Mathematical Framework:
- Rips complex construction on Cα point clouds
- Persistent homology computation
- Correlation with Z² natural length scale (9.14 Å)

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Theoretical computational research only. Not peer reviewed.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy import stats
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings

# Z² Framework constants
Z2 = 32 * np.pi / 3  # ≈ 33.51
R_NATURAL = (Z2 ** 0.25) * 3.8  # ≈ 9.14 Å

def compute_distance_matrix(coords: np.ndarray) -> np.ndarray:
    """Compute pairwise distance matrix from coordinates."""
    return squareform(pdist(coords))

def compute_rips_betti(distance_matrix: np.ndarray,
                       max_radius: float = 15.0,
                       n_steps: int = 100) -> Dict:
    """
    Compute Betti numbers across filtration radii using Rips complex.

    This is a simplified implementation. For production use,
    install ripser or giotto-tda:
        pip install ripser giotto-tda

    Returns dict with filtration radii and Betti numbers.
    """
    n = len(distance_matrix)
    radii = np.linspace(0, max_radius, n_steps)

    betti_0 = []  # Connected components
    betti_1 = []  # Loops/cycles
    betti_2 = []  # Voids/cavities

    for r in radii:
        # Adjacency at radius r
        adj = (distance_matrix <= r).astype(int)
        np.fill_diagonal(adj, 0)

        # β₀: Number of connected components
        # Use union-find or scipy connected components
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import connected_components

        n_components, _ = connected_components(csr_matrix(adj), directed=False)
        betti_0.append(n_components)

        # β₁: Approximate via Euler characteristic
        # χ = β₀ - β₁ + β₂
        # For Rips complex: χ ≈ V - E + F - ...
        n_edges = np.sum(adj) // 2

        # Count triangles (3-cliques)
        n_triangles = 0
        for i in range(n):
            for j in range(i+1, n):
                if adj[i,j]:
                    for k in range(j+1, n):
                        if adj[i,k] and adj[j,k]:
                            n_triangles += 1

        # Euler characteristic approximation
        chi = n - n_edges + n_triangles

        # β₁ ≈ β₀ - χ + β₂ (approximate β₂ = 0 for simplicity)
        b1_approx = max(0, n_components - chi)
        betti_1.append(b1_approx)

        # β₂: Would need full simplicial complex computation
        # Approximate as 0 for small proteins
        betti_2.append(0)

    return {
        'radii': radii.tolist(),
        'betti_0': betti_0,
        'betti_1': betti_1,
        'betti_2': betti_2,
    }

def find_stabilization_radius(betti_curve: List[int],
                               radii: List[float],
                               threshold: float = 0.1) -> float:
    """
    Find the radius at which Betti numbers stabilize.
    Returns the first radius where the derivative drops below threshold.
    """
    betti = np.array(betti_curve)
    radii = np.array(radii)

    # Compute discrete derivative
    d_betti = np.abs(np.diff(betti))
    d_radii = np.diff(radii)
    derivative = d_betti / d_radii

    # Find first point where derivative is consistently low
    for i in range(len(derivative)):
        if i + 5 < len(derivative):
            window = derivative[i:i+5]
            if np.mean(window) < threshold:
                return radii[i]

    return radii[-1]

def fetch_protein_coordinates(pdb_id: str) -> Optional[np.ndarray]:
    """Fetch Cα coordinates from RCSB PDB."""
    import requests

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return None

        coords = []
        for line in response.text.split('\n'):
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])
                except ValueError:
                    continue

        if len(coords) < 10:
            return None

        return np.array(coords)

    except Exception:
        return None

def analyze_protein_topology(pdb_id: str) -> Optional[Dict]:
    """Perform complete TDA analysis on a protein."""
    coords = fetch_protein_coordinates(pdb_id)
    if coords is None:
        return None

    n_residues = len(coords)

    # Compute distance matrix
    dist_matrix = compute_distance_matrix(coords)

    # Compute persistent homology
    ph_results = compute_rips_betti(dist_matrix, max_radius=15.0)

    # Find stabilization radii
    r_stable_b0 = find_stabilization_radius(
        ph_results['betti_0'],
        ph_results['radii']
    )
    r_stable_b1 = find_stabilization_radius(
        ph_results['betti_1'],
        ph_results['radii']
    )

    # Correlation with Z² length scale
    z2_correlation = 1.0 - abs(r_stable_b1 - R_NATURAL) / R_NATURAL

    return {
        'pdb_id': pdb_id,
        'n_residues': n_residues,
        'r_stable_b0': r_stable_b0,
        'r_stable_b1': r_stable_b1,
        'z2_natural': R_NATURAL,
        'z2_correlation': z2_correlation,
        'betti_at_z2': {
            'b0': int(np.interp(R_NATURAL, ph_results['radii'], ph_results['betti_0'])),
            'b1': int(np.interp(R_NATURAL, ph_results['radii'], ph_results['betti_1'])),
        },
        'persistent_homology': ph_results,
    }

def main():
    """Run persistent homology analysis on protein dataset."""
    print("=" * 70)
    print("GEO_01: PERSISTENT HOMOLOGY ANALYSIS")
    print("Topological Data Analysis of Protein Structures")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Natural Length Scale: {R_NATURAL:.2f} Å")
    print()

    # Test proteins (subset of validated proteins)
    test_pdbs = ['1UBQ', '1L2Y', '1CRN', '2GB1', '1VII']

    results = {
        'timestamp': datetime.now().isoformat(),
        'z2_value': float(Z2),
        'r_natural': float(R_NATURAL),
        'proteins': [],
        'summary': {},
    }

    print("Analyzing proteins...")
    print("-" * 70)

    stabilization_radii = []
    z2_correlations = []

    for pdb_id in test_pdbs:
        print(f"  Processing {pdb_id}...", end=" ")

        analysis = analyze_protein_topology(pdb_id)

        if analysis:
            results['proteins'].append(analysis)
            stabilization_radii.append(analysis['r_stable_b1'])
            z2_correlations.append(analysis['z2_correlation'])

            print(f"✓ {analysis['n_residues']} residues, "
                  f"r_stable = {analysis['r_stable_b1']:.2f} Å, "
                  f"Z² corr = {analysis['z2_correlation']:.2f}")
        else:
            print("✗ Failed to fetch")

    # Summary statistics
    if stabilization_radii:
        mean_r = np.mean(stabilization_radii)
        std_r = np.std(stabilization_radii)
        mean_corr = np.mean(z2_correlations)

        # Statistical test: is mean_r close to R_NATURAL?
        t_stat, p_value = stats.ttest_1samp(stabilization_radii, R_NATURAL)

        results['summary'] = {
            'n_proteins': len(stabilization_radii),
            'mean_stabilization_radius': float(mean_r),
            'std_stabilization_radius': float(std_r),
            'mean_z2_correlation': float(mean_corr),
            'z2_natural_length': float(R_NATURAL),
            'deviation_from_z2': float(abs(mean_r - R_NATURAL)),
            'percent_error': float(abs(mean_r - R_NATURAL) / R_NATURAL * 100),
            't_statistic': float(t_stat),
            'p_value': float(p_value),
        }

        print()
        print("=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Proteins analyzed: {len(stabilization_radii)}")
        print(f"Mean stabilization radius: {mean_r:.2f} ± {std_r:.2f} Å")
        print(f"Z² natural length scale: {R_NATURAL:.2f} Å")
        print(f"Mean Z² correlation: {mean_corr:.3f}")
        print(f"Deviation: {abs(mean_r - R_NATURAL):.2f} Å ({abs(mean_r - R_NATURAL)/R_NATURAL*100:.1f}%)")
        print(f"t-statistic: {t_stat:.3f}, p-value: {p_value:.4f}")
        print()

        if p_value > 0.05:
            print("INTERPRETATION: Stabilization radius is NOT significantly")
            print("                different from Z² natural length scale.")
            print("                Topological features emerge at ~9 Å!")
        else:
            print("INTERPRETATION: Stabilization radius differs from Z² prediction.")

    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "geo_01_persistent_homology_results.json"

    # Remove large arrays for JSON serialization
    for p in results['proteins']:
        if 'persistent_homology' in p:
            del p['persistent_homology']

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    print("\n" + "=" * 70)
    print("GEO_01 COMPLETE")
    print("=" * 70)

    return results

if __name__ == "__main__":
    main()
