#!/usr/bin/env python3
"""
High-Resolution Mode Search: Finding the True Aromatic Peak
============================================================

Performs Kernel Density Estimation (KDE) and 10 mÅ binning to
locate the absolute mode of the aromatic stacking distribution.

This will determine if the peak is truly at √Z² = 5.7888 Å
or merely near it.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman
"""

import numpy as np
import json
import os
from scipy.stats import gaussian_kde

Z2 = 32 * np.pi / 3
SQRT_Z2 = np.sqrt(Z2)  # ≈ 5.7888 Å

def main():
    results_path = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/pocket_analysis_results.json'
    if not os.path.exists(results_path):
        print(f"Error: {results_path} not found.")
        return

    with open(results_path, 'r') as f:
        data = json.load(f)

    all_distances = []
    for target, analysis in data['results'].items():
        for pair in analysis.get('closest_pairs', []):
            all_distances.append(pair['distance'])
    
    all_distances = np.array(all_distances)
    n_total = len(all_distances)
    
    print("=" * 70)
    print("HIGH-RESOLUTION MODE SEARCH")
    print(f"√Z² Reference: {SQRT_Z2:.6f} Å")
    print("=" * 70)

    # 1. Kernel Density Estimation
    kde = gaussian_kde(all_distances)
    x_range = np.linspace(4.0, 8.0, 1000)
    y_kde = kde(x_range)
    
    mode_kde = x_range[np.argmax(y_kde)]
    
    # 2. Ultra-fine Binning (10 mÅ)
    fine_bins = np.arange(4.0, 8.01, 0.01)
    hist, edges = np.histogram(all_distances, bins=fine_bins)
    centers = (edges[:-1] + edges[1:]) / 2
    
    mode_bin = centers[np.argmax(hist)]
    mode_count = np.max(hist)

    print(f"\nDistribution Mode Analysis:")
    print(f"  KDE Estimated Mode:   {mode_kde:.4f} Å")
    print(f"  Fine Bin Mode (10mÅ): {mode_bin:.4f} Å (Count: {mode_count})")
    print(f"  Reference √Z²:        {SQRT_Z2:.4f} Å")
    print(f"  Delta (Mode - √Z²):   {mode_bin - SQRT_Z2:+.4f} Å")

    # 3. Local Statistics around √Z²
    # Check the 5.70 - 5.80 Å window
    mask = (all_distances >= 5.70) & (all_distances <= 5.85)
    local_pts = all_distances[mask]
    print(f"\nLocal Window [5.70, 5.85]:")
    print(f"  Points in window: {len(local_pts)}")
    print(f"  Local mean:       {np.mean(local_pts):.4f} Å")
    print(f"  Local median:     {np.median(local_pts):.4f} Å")

    # 4. Significance of the Global Mode
    # Use 0.1A window around global mode vs total average
    total_avg_density = n_total / (8.0 - 4.0) # points per Angstrom
    mode_window_count = np.sum((all_distances >= mode_bin - 0.05) & (all_distances <= mode_bin + 0.05))
    mode_density = mode_window_count / 0.1
    
    print(f"\nGlobal Mode Significance:")
    print(f"  Avg density:      {total_avg_density:.1f} pts/Å")
    print(f"  Peak density:     {mode_density:.1f} pts/Å")
    print(f"  Enrichment:       {mode_density / total_avg_density:.2f}x")

    # 5. Visual Check of the Peak
    print("\nLocal Fine-Grain Histogram (5.5 - 6.0 Å):")
    for i in range(len(hist)):
        c = centers[i]
        if 5.5 <= c <= 6.05:
            marker = " <== √Z²" if abs(c - SQRT_Z2) < 0.006 else (" *** PEAK ***" if i == np.argmax(hist) else "")
            bar = "█" * int(40 * hist[i] / mode_count)
            print(f"  {c:6.3f}  {hist[i]:3d}  {bar}{marker}")

if __name__ == "__main__":
    main()
