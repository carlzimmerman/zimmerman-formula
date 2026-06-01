#!/usr/bin/env python3
"""
inv_06_delaunay_z2_distance.py

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

inv_06_delaunay_z2_distance.py - Delaunay Distance Analysis for Z² Detection

Tests the Distance Hypothesis:
Does the mean Delaunay edge length (distance between packed neighbors)
equal √(Z²) = √(32π/3) ≈ 5.79 Å?

Delaunay triangulation connects atoms that are "natural neighbors" -
those that share a Voronoi boundary. In the crystalline hydrophobic
core, these distances should reveal fundamental packing constants.

CRITICAL FILTER: We exclude covalent bonds (~1.5 Å) which are fixed
by quantum chemistry. Only van der Waals contacts are analyzed.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 21, 2026
"""
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
from scipy.spatial import Delaunay
from scipy import stats
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "delaunay_z2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CORE_DATA_PATH = Path(__file__).parent / "results" / "core_isolation" / "isolated_cores.json"

print("=" * 80)
print("DELAUNAY DISTANCE ANALYSIS - Z² DETECTION")
print("Testing: Mean Neighbor Distance = √(Z²) = √(32π/3) ≈ 5.79 Å")
print("=" * 80)
print()

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.5103
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.7888 Å

# Distance targets to test
DISTANCE_TARGETS = {
    'sqrt_z2': SQRT_Z2,                     # 5.79 Å - PRIMARY TARGET
    'sqrt_z2_div_sqrt2': SQRT_Z2 / np.sqrt(2),  # 4.09 Å
    'sqrt_z2_div_2': SQRT_Z2 / 2,           # 2.89 Å
    'sqrt_z2_times_sqrt2': SQRT_Z2 * np.sqrt(2),  # 8.19 Å
    'cubert_z2': Z_SQUARED ** (1/3),        # 3.22 Å
    'vdw_contact': 3.4,                     # Typical C-C vdW contact
    'vdw_sum': 3.4,                         # Sum of vdW radii (C-C)
}

# Covalent bond cutoff (exclude these)
COVALENT_CUTOFF = 1.8  # Å - bonds below this are covalent

# Van der Waals contact range
VDW_MIN = 2.5  # Å - minimum non-bonded distance
VDW_MAX = 6.0  # Å - maximum meaningful packing distance

print(f"Z² = 32π/3 = {Z_SQUARED:.4f}")
print(f"√(Z²) = {SQRT_Z2:.4f} Å (PRIMARY TARGET)")
print(f"\nCovalent cutoff: < {COVALENT_CUTOFF} Å (excluded)")
print(f"Van der Waals range: {VDW_MIN} - {VDW_MAX} Å")
print()
print("Distance targets to test:")
for name, dist in DISTANCE_TARGETS.items():
    print(f"  {name}: {dist:.4f} Å")
print()


# =============================================================================
# DELAUNAY COMPUTATION
# =============================================================================

def compute_delaunay_edges(coords: np.ndarray) -> np.ndarray:
    """
    Compute all Delaunay triangulation edge lengths.

    Returns array of all unique edge distances.
    """
    if len(coords) < 4:
        return np.array([])

    try:
        tri = Delaunay(coords)

        edges_seen = set()
        edge_lengths = []

        # Each simplex is a tetrahedron with 4 vertices
        # Extract all 6 edges per simplex
        for simplex in tri.simplices:
            for i in range(4):
                for j in range(i + 1, 4):
                    # Create canonical edge representation
                    edge = tuple(sorted([simplex[i], simplex[j]]))

                    if edge not in edges_seen:
                        edges_seen.add(edge)

                        # Calculate distance
                        dist = np.linalg.norm(coords[edge[0]] - coords[edge[1]])
                        edge_lengths.append(dist)

        return np.array(edge_lengths)

    except Exception as e:
        print(f"    Delaunay failed: {e}")
        return np.array([])


def filter_noncovalent_distances(distances: np.ndarray) -> np.ndarray:
    """
    Filter out covalent bonds, keep only van der Waals contacts.
    """
    # Remove covalent bonds
    noncovalent = distances[distances > COVALENT_CUTOFF]

    # Remove very long distances (noise)
    noncovalent = noncovalent[noncovalent < VDW_MAX * 2]

    return noncovalent


def filter_vdw_contacts(distances: np.ndarray) -> np.ndarray:
    """
    Keep only distances in the van der Waals contact range.
    """
    return distances[(distances >= VDW_MIN) & (distances <= VDW_MAX)]


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def analyze_distance_distribution(distances: np.ndarray, label: str = "") -> Dict:
    """
    Statistical analysis of Delaunay distances.
    """
    if len(distances) == 0:
        return {'error': 'No valid distances'}

    analysis = {
        'label': label,
        'n_samples': len(distances),
        'mean': float(np.mean(distances)),
        'median': float(np.median(distances)),
        'std': float(np.std(distances)),
        'sem': float(stats.sem(distances)),
        'min': float(np.min(distances)),
        'max': float(np.max(distances)),
        'q25': float(np.percentile(distances, 25)),
        'q75': float(np.percentile(distances, 75)),
    }

    # Mode estimation (peak of distribution)
    try:
        kde = stats.gaussian_kde(distances)
        x_range = np.linspace(distances.min(), distances.max(), 1000)
        kde_values = kde(x_range)
        mode_idx = np.argmax(kde_values)
        analysis['mode'] = float(x_range[mode_idx])
    except Exception:
        analysis['mode'] = analysis['median']

    # Test against Z² targets
    analysis['z2_tests'] = {}

    for name, target in DISTANCE_TARGETS.items():
        deviation = analysis['mean'] - target
        z_score = deviation / analysis['sem'] if analysis['sem'] > 0 else float('inf')

        # One-sample t-test against target
        t_stat, p_value = stats.ttest_1samp(distances, target)

        analysis['z2_tests'][name] = {
            'target': target,
            'deviation': float(deviation),
            'deviation_pct': float(100 * deviation / target) if target > 0 else 0,
            'z_score': float(z_score),
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'match': abs(z_score) < 2.0,  # Within 2 sigma
        }

    return analysis


# =============================================================================
# PLOTTING
# =============================================================================

def plot_distance_distribution(distances: np.ndarray, analysis: Dict,
                                title_suffix: str = "") -> Optional[Path]:
    """
    Plot histogram of Delaunay distances with Z² target.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 7))

        # Histogram
        bins = np.linspace(max(0, distances.min() - 0.5),
                          min(15, distances.max() + 0.5), 100)
        ax.hist(distances, bins=bins, density=True, alpha=0.7, color='steelblue',
                edgecolor='black', linewidth=0.5, label='Delaunay distances')

        # Mark empirical statistics
        mean = analysis['mean']
        mode = analysis.get('mode', mean)

        ax.axvline(mean, color='blue', linewidth=2, linestyle='-',
                   label=f'Mean: {mean:.3f} Å')
        ax.axvline(mode, color='cyan', linewidth=2, linestyle=':',
                   label=f'Mode: {mode:.3f} Å')

        # Mark √(Z²) target
        ax.axvline(SQRT_Z2, color='red', linewidth=2.5, linestyle='--',
                   label=f'√(Z²) = {SQRT_Z2:.3f} Å')

        # Mark other targets
        ax.axvline(SQRT_Z2 / 2, color='orange', linewidth=1.5, linestyle='--',
                   alpha=0.7, label=f'√(Z²)/2 = {SQRT_Z2/2:.3f} Å')

        # Mark vdW contact distance
        ax.axvline(3.4, color='green', linewidth=1.5, linestyle=':',
                   alpha=0.7, label='vdW contact ~3.4 Å')

        ax.set_xlabel('Delaunay Edge Length (Å)', fontsize=12)
        ax.set_ylabel('Probability Density', fontsize=12)
        ax.set_title(f'Delaunay Distance Distribution in Hydrophobic Cores{title_suffix}\n'
                     f'Testing √(Z²) = √(32π/3) = {SQRT_Z2:.3f} Å', fontsize=14)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 12)

        # Statistics text box
        textstr = f'N = {analysis["n_samples"]:,}\n'
        textstr += f'Mean = {mean:.3f} ± {analysis["sem"]:.3f} Å\n'
        textstr += f'Mode = {mode:.3f} Å\n'
        textstr += f'Deviation from √(Z²): {mean - SQRT_Z2:+.3f} Å'

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax.text(0.98, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right', bbox=props)

        filename = f"delaunay_distance_distribution{title_suffix.replace(' ', '_').lower()}.png"
        plot_path = OUTPUT_DIR / filename
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()

        return plot_path

    except ImportError:
        return None


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_protein_core(core_data: Dict) -> Dict:
    """
    Analyze Delaunay distances for a single protein core.
    """
    pdb_id = core_data.get('pdb_id', 'unknown')
    coords = np.array(core_data['coords'])

    result = {
        'pdb_id': pdb_id,
        'n_atoms': len(coords),
    }

    if len(coords) < 10:
        result['error'] = 'Too few atoms'
        return result

    # Compute Delaunay edges
    all_distances = compute_delaunay_edges(coords)

    if len(all_distances) == 0:
        result['error'] = 'Delaunay triangulation failed'
        return result

    # Filter to non-covalent distances
    noncovalent = filter_noncovalent_distances(all_distances)
    vdw_contacts = filter_vdw_contacts(all_distances)

    result['n_total_edges'] = len(all_distances)
    result['n_noncovalent'] = len(noncovalent)
    result['n_vdw_contacts'] = len(vdw_contacts)
    result['distances_all'] = all_distances.tolist()
    result['distances_noncovalent'] = noncovalent.tolist()
    result['distances_vdw'] = vdw_contacts.tolist()
    result['success'] = True

    # Quick stats
    if len(noncovalent) > 0:
        result['mean_noncovalent'] = float(np.mean(noncovalent))
    if len(vdw_contacts) > 0:
        result['mean_vdw'] = float(np.mean(vdw_contacts))

    return result


def main():
    """
    Run Delaunay distance analysis on all isolated hydrophobic cores.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Delaunay Triangulation Distance Analysis',
        'target': f'√(Z²) = √(32π/3) = {SQRT_Z2:.4f} Å',
        'covalent_cutoff': COVALENT_CUTOFF,
        'vdw_range': [VDW_MIN, VDW_MAX],
        'proteins': [],
    }

    # Load isolated core data
    if not CORE_DATA_PATH.exists():
        print("Core isolation data not found. Running core isolation first...")
        import subprocess
        subprocess.run(['python', str(Path(__file__).parent / 'inv_04_core_isolation.py')])

    if not CORE_DATA_PATH.exists():
        print("Failed to generate core data. Exiting.")
        return

    with open(CORE_DATA_PATH, 'r') as f:
        core_data = json.load(f)

    cores = core_data.get('cores', [])
    print(f"Loaded {len(cores)} protein cores with {core_data.get('total_atoms', 0)} atoms")

    # Analyze each core
    all_distances = []
    all_noncovalent = []
    all_vdw = []

    for i, core in enumerate(cores):
        if (i + 1) % 10 == 0:
            print(f"  Processing core {i+1}/{len(cores)}...")

        protein_result = analyze_protein_core(core)
        results['proteins'].append(protein_result)

        if protein_result.get('success'):
            all_distances.extend(protein_result['distances_all'])
            all_noncovalent.extend(protein_result['distances_noncovalent'])
            all_vdw.extend(protein_result['distances_vdw'])

    # Convert to arrays
    all_distances = np.array(all_distances)
    all_noncovalent = np.array(all_noncovalent)
    all_vdw = np.array(all_vdw)

    print(f"\nTotal Delaunay edges: {len(all_distances):,}")
    print(f"Non-covalent edges: {len(all_noncovalent):,}")
    print(f"Van der Waals contacts: {len(all_vdw):,}")

    # Aggregate analyses
    analyses = {}

    if len(all_noncovalent) > 0:
        analyses['noncovalent'] = analyze_distance_distribution(all_noncovalent, 'Non-covalent')
        results['aggregate_noncovalent'] = analyses['noncovalent']

    if len(all_vdw) > 0:
        analyses['vdw_contacts'] = analyze_distance_distribution(all_vdw, 'VdW Contacts')
        results['aggregate_vdw'] = analyses['vdw_contacts']

    # Print results
    print("\n" + "=" * 80)
    print("DELAUNAY DISTANCE ANALYSIS RESULTS")
    print("=" * 80)

    for label, analysis in analyses.items():
        print(f"\n  {label.upper()} ({analysis['n_samples']:,} samples):")
        print(f"    Mean:   {analysis['mean']:.4f} ± {analysis['sem']:.4f} Å")
        print(f"    Mode:   {analysis['mode']:.4f} Å")
        print(f"    Median: {analysis['median']:.4f} Å")

        print(f"\n    √(Z²) TEST ({SQRT_Z2:.4f} Å):")
        z2_test = analysis['z2_tests']['sqrt_z2']
        print(f"      Deviation: {z2_test['deviation']:+.4f} Å ({z2_test['deviation_pct']:+.2f}%)")
        print(f"      Z-score: {z2_test['z_score']:.2f}")
        print(f"      p-value: {z2_test['p_value']:.2e}")

        match_str = "✓ MATCH" if z2_test['match'] else "✗ NO MATCH"
        print(f"      Verdict: {match_str}")

    # Final verdict
    print("\n" + "=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)

    if 'noncovalent' in analyses:
        z2_test = analyses['noncovalent']['z2_tests']['sqrt_z2']
        mean = analyses['noncovalent']['mean']

        if z2_test['match']:
            print(f"\n  ✓ √(Z²) DISTANCE HYPOTHESIS SUPPORTED")
            print(f"  Mean non-covalent distance ({mean:.3f} Å) ≈ √(Z²) ({SQRT_Z2:.3f} Å)")
            print(f"  Deviation: {z2_test['deviation']:+.4f} Å ({z2_test['deviation_pct']:+.2f}%)")
        else:
            print(f"\n  ? √(Z²) DISTANCE HYPOTHESIS INCONCLUSIVE")
            print(f"  Mean non-covalent distance: {mean:.3f} Å")
            print(f"  √(Z²) target: {SQRT_Z2:.3f} Å")
            print(f"  Deviation: {z2_test['deviation']:+.4f} Å ({abs(z2_test['z_score']):.1f}σ)")

            # Check if mode matches better
            mode = analyses['noncovalent']['mode']
            mode_deviation = mode - SQRT_Z2
            if abs(mode_deviation) < abs(z2_test['deviation']):
                print(f"\n  NOTE: Distribution MODE ({mode:.3f} Å) is closer to √(Z²)")
                print(f"  Mode deviation: {mode_deviation:+.4f} Å")

    print("=" * 80)

    # Plots
    plot_paths = []
    if len(all_noncovalent) > 0:
        plot_path = plot_distance_distribution(all_noncovalent, analyses['noncovalent'], "_noncovalent")
        if plot_path:
            plot_paths.append(str(plot_path))
            print(f"\n  Plot: {plot_path}")

    if len(all_vdw) > 0:
        plot_path = plot_distance_distribution(all_vdw, analyses['vdw_contacts'], "_vdw")
        if plot_path:
            plot_paths.append(str(plot_path))
            print(f"  Plot: {plot_path}")

    results['plot_paths'] = plot_paths

    # Save results (without individual distances to save space)
    for p in results['proteins']:
        p.pop('distances_all', None)
        p.pop('distances_noncovalent', None)
        p.pop('distances_vdw', None)

    json_path = OUTPUT_DIR / "delaunay_z2_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {json_path}")

    # Save raw distances for further analysis
    if len(all_noncovalent) > 0:
        np.save(OUTPUT_DIR / "all_noncovalent_distances.npy", all_noncovalent)
    if len(all_vdw) > 0:
        np.save(OUTPUT_DIR / "all_vdw_distances.npy", all_vdw)

    return results


if __name__ == "__main__":
    main()
