#!/usr/bin/env python3
"""
inv_05_voronoi_z2_volume.py - Voronoi Volume Analysis for Z² Detection

Tests the Volume Hypothesis:
Does the mean Voronoi cell volume of hydrophobic core atoms
equal Z² = 32π/3 ≈ 33.51 Å³?

Each atom "owns" a Voronoi polyhedron - the region of space closer
to it than to any other atom. In the crystalline hydrophobic core,
these volumes should reveal fundamental packing constants.

AGPL-3.0-or-later License
Author: Carl Zimmerman & Claude Opus 4.5
Date: April 21, 2026
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional
from scipy.spatial import Voronoi, ConvexHull
from scipy import stats
import warnings

OUTPUT_DIR = Path(__file__).parent / "results" / "voronoi_z2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CORE_DATA_PATH = Path(__file__).parent / "results" / "core_isolation" / "isolated_cores.json"

print("=" * 80)
print("VORONOI VOLUME ANALYSIS - Z² DETECTION")
print("Testing: Mean Voronoi Volume = Z² = 32π/3 ≈ 33.51 Å³")
print("=" * 80)
print()

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.5103 Å³
SQRT_Z2 = np.sqrt(Z_SQUARED)  # ≈ 5.7888 Å

# Related volume constants to test
VOLUME_TARGETS = {
    'Z2': Z_SQUARED,                        # 33.51 Å³
    'Z2_div_2': Z_SQUARED / 2,              # 16.76 Å³
    'Z2_times_2': Z_SQUARED * 2,            # 67.02 Å³
    'sphere_r_sqrt_z2': (4/3) * np.pi * SQRT_Z2**3,  # ~810 Å³ (too big)
    'cube_sqrt_z2': SQRT_Z2**3,             # 194 Å³
    'vdw_carbon': (4/3) * np.pi * 1.7**3,   # 20.6 Å³ (C vdW sphere)
}

print(f"Z² = 32π/3 = {Z_SQUARED:.4f} Å³")
print(f"√(Z²) = {SQRT_Z2:.4f} Å")
print()
print("Volume targets to test:")
for name, vol in VOLUME_TARGETS.items():
    print(f"  {name}: {vol:.4f} Å³")
print()


# =============================================================================
# VORONOI COMPUTATION
# =============================================================================

def compute_bounded_voronoi_volumes(coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute Voronoi cell volumes, rejecting unbounded (edge) cells.

    Returns:
        volumes: Array of valid (bounded) cell volumes
        valid_mask: Boolean mask indicating which atoms have valid volumes
    """
    if len(coords) < 4:
        return np.array([]), np.array([])

    try:
        vor = Voronoi(coords)

        n_atoms = len(coords)
        volumes = np.full(n_atoms, np.nan)
        valid_mask = np.zeros(n_atoms, dtype=bool)

        for i in range(n_atoms):
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]

            # Skip unbounded regions (contain -1 vertex)
            if -1 in region or len(region) == 0:
                continue

            try:
                # Get vertices of this Voronoi cell
                vertices = vor.vertices[region]

                # Compute convex hull volume
                hull = ConvexHull(vertices)
                volumes[i] = hull.volume
                valid_mask[i] = True

            except Exception:
                continue

        return volumes[valid_mask], valid_mask

    except Exception as e:
        print(f"    Voronoi failed: {e}")
        return np.array([]), np.array([])


def compute_voronoi_with_mirror(coords: np.ndarray, padding: float = 5.0) -> np.ndarray:
    """
    Compute Voronoi volumes with mirror boundary conditions.

    This reduces edge effects by reflecting the point cloud.
    """
    if len(coords) < 4:
        return np.array([])

    n_original = len(coords)

    # Compute bounding box
    min_coords = coords.min(axis=0)
    max_coords = coords.max(axis=0)
    center = (min_coords + max_coords) / 2

    # Create mirrored points (6 reflections)
    mirrored_coords = [coords]

    for axis in range(3):
        # Reflect across min boundary
        reflected = coords.copy()
        reflected[:, axis] = 2 * min_coords[axis] - reflected[:, axis]
        mirrored_coords.append(reflected)

        # Reflect across max boundary
        reflected = coords.copy()
        reflected[:, axis] = 2 * max_coords[axis] - reflected[:, axis]
        mirrored_coords.append(reflected)

    all_coords = np.vstack(mirrored_coords)

    # Compute Voronoi on extended system
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
            except Exception:
                continue

        return volumes[~np.isnan(volumes)]

    except Exception as e:
        print(f"    Mirrored Voronoi failed: {e}")
        return np.array([])


# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def analyze_volume_distribution(volumes: np.ndarray) -> Dict:
    """
    Statistical analysis of Voronoi volumes.
    """
    if len(volumes) == 0:
        return {'error': 'No valid volumes'}

    analysis = {
        'n_samples': len(volumes),
        'mean': float(np.mean(volumes)),
        'median': float(np.median(volumes)),
        'std': float(np.std(volumes)),
        'sem': float(stats.sem(volumes)),
        'min': float(np.min(volumes)),
        'max': float(np.max(volumes)),
        'q25': float(np.percentile(volumes, 25)),
        'q75': float(np.percentile(volumes, 75)),
    }

    # Test against Z² targets
    analysis['z2_tests'] = {}

    for name, target in VOLUME_TARGETS.items():
        deviation = analysis['mean'] - target
        z_score = deviation / analysis['sem'] if analysis['sem'] > 0 else float('inf')

        # One-sample t-test against target
        t_stat, p_value = stats.ttest_1samp(volumes, target)

        analysis['z2_tests'][name] = {
            'target': target,
            'deviation': float(deviation),
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

def plot_volume_distribution(volumes: np.ndarray, analysis: Dict) -> Optional[Path]:
    """
    Plot histogram of Voronoi volumes with Z² targets.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 7))

        # Histogram
        ax.hist(volumes, bins=100, density=True, alpha=0.7, color='steelblue',
                edgecolor='black', linewidth=0.5, label='Voronoi volumes')

        # Mark empirical mean
        mean = analysis['mean']
        ax.axvline(mean, color='blue', linewidth=2, linestyle='-',
                   label=f'Empirical mean: {mean:.2f} Å³')

        # Mark Z² targets
        colors = ['red', 'orange', 'green', 'purple', 'brown']
        for i, (name, target) in enumerate(list(VOLUME_TARGETS.items())[:5]):
            if 10 < target < 100:  # Only show reasonable targets
                ax.axvline(target, color=colors[i % len(colors)], linewidth=1.5,
                           linestyle='--', alpha=0.7, label=f'{name}: {target:.2f} Å³')

        ax.set_xlabel('Voronoi Cell Volume (Å³)', fontsize=12)
        ax.set_ylabel('Probability Density', fontsize=12)
        ax.set_title('Voronoi Volume Distribution in Hydrophobic Cores\n'
                     f'Testing Z² = 32π/3 = {Z_SQUARED:.2f} Å³', fontsize=14)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Set reasonable x-limits
        ax.set_xlim(0, min(100, np.percentile(volumes, 99)))

        # Add statistics text box
        textstr = f'N = {analysis["n_samples"]:,}\n'
        textstr += f'Mean = {mean:.2f} ± {analysis["sem"]:.2f} Å³\n'
        textstr += f'Median = {analysis["median"]:.2f} Å³\n'
        textstr += f'Std = {analysis["std"]:.2f} Å³'

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax.text(0.98, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right', bbox=props)

        plot_path = OUTPUT_DIR / "voronoi_volume_distribution.png"
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
    Analyze Voronoi volumes for a single protein core.
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

    # Compute Voronoi volumes
    volumes = compute_voronoi_with_mirror(coords)

    if len(volumes) == 0:
        volumes, _ = compute_bounded_voronoi_volumes(coords)

    if len(volumes) < 5:
        result['error'] = 'Too few valid Voronoi cells'
        return result

    result['n_valid_volumes'] = len(volumes)
    result['volumes'] = volumes.tolist()
    result['mean_volume'] = float(np.mean(volumes))
    result['std_volume'] = float(np.std(volumes))
    result['success'] = True

    return result


def main():
    """
    Run Voronoi volume analysis on all isolated hydrophobic cores.
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Voronoi Volume Analysis',
        'target': f'Z² = 32π/3 = {Z_SQUARED:.4f} Å³',
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
    all_volumes = []

    for i, core in enumerate(cores):
        if (i + 1) % 10 == 0:
            print(f"  Processing core {i+1}/{len(cores)}...")

        protein_result = analyze_protein_core(core)
        results['proteins'].append(protein_result)

        if protein_result.get('success'):
            all_volumes.extend(protein_result['volumes'])

    # Aggregate analysis
    all_volumes = np.array(all_volumes)
    print(f"\nTotal Voronoi cells analyzed: {len(all_volumes)}")

    if len(all_volumes) > 0:
        analysis = analyze_volume_distribution(all_volumes)
        results['aggregate'] = analysis

        print("\n" + "=" * 80)
        print("VORONOI VOLUME ANALYSIS RESULTS")
        print("=" * 80)

        print(f"\n  Total valid Voronoi cells: {analysis['n_samples']:,}")
        print(f"\n  VOLUME STATISTICS:")
        print(f"    Mean:   {analysis['mean']:.4f} ± {analysis['sem']:.4f} Å³")
        print(f"    Median: {analysis['median']:.4f} Å³")
        print(f"    Std:    {analysis['std']:.4f} Å³")

        print(f"\n  Z² HYPOTHESIS TESTS:")
        print(f"    Target: Z² = {Z_SQUARED:.4f} Å³")

        for name, test in analysis['z2_tests'].items():
            if 10 < test['target'] < 100:
                match_str = "✓ MATCH" if test['match'] else "✗"
                sig_str = "(p < 0.05)" if test['significant'] else ""
                print(f"\n    {name} ({test['target']:.2f} Å³):")
                print(f"      Deviation: {test['deviation']:+.4f} Å³")
                print(f"      Z-score: {test['z_score']:.2f} {match_str}")
                print(f"      p-value: {test['p_value']:.2e} {sig_str}")

        # Final verdict
        z2_test = analysis['z2_tests']['Z2']
        print("\n" + "=" * 80)
        if z2_test['match']:
            print("VERDICT: Z² VOLUME HYPOTHESIS SUPPORTED")
            print(f"Mean Voronoi volume ({analysis['mean']:.2f} Å³) matches Z² ({Z_SQUARED:.2f} Å³)")
        else:
            print("VERDICT: Z² VOLUME HYPOTHESIS NOT CONFIRMED")
            print(f"Mean Voronoi volume ({analysis['mean']:.2f} Å³) ≠ Z² ({Z_SQUARED:.2f} Å³)")
            print(f"Deviation: {z2_test['deviation']:.2f} Å³ ({z2_test['z_score']:.1f}σ)")
        print("=" * 80)

        # Plot
        plot_path = plot_volume_distribution(all_volumes, analysis)
        if plot_path:
            results['plot_path'] = str(plot_path)
            print(f"\n  Plot: {plot_path}")

    # Save results (without individual volumes to save space)
    for p in results['proteins']:
        p.pop('volumes', None)

    json_path = OUTPUT_DIR / "voronoi_z2_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results: {json_path}")

    # Save raw volumes for further analysis
    if len(all_volumes) > 0:
        np.save(OUTPUT_DIR / "all_voronoi_volumes.npy", all_volumes)
        print(f"  Raw volumes: {OUTPUT_DIR / 'all_voronoi_volumes.npy'}")

    return results


if __name__ == "__main__":
    main()
