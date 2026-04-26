#!/usr/bin/env python3
"""
Refined Statistical Test: Is √Z² = 5.789 Å the true aromatic peak?
===================================================================

Using the 2,583 aromatic pairs extracted from 169 PDB structures,
we perform a high-resolution (50 mÅ) binning to determine if
√Z² = 5.7888 Å is a statistically significant peak.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman
"""

import numpy as np
import json
import os
from scipy import stats

Z2 = 32 * np.pi / 3
SQRT_Z2 = np.sqrt(Z2)  # ≈ 5.7888 Å
BIN_WIDTH = 0.05  # 50 mÅ

def main():
    results_path = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/pocket_analysis_results.json'
    if not os.path.exists(results_path):
        print(f"Error: {results_path} not found. Run pocket_analyzer.py first.")
        return

    with open(results_path, 'r') as f:
        data = json.load(f)

    # Extract all distances
    all_distances = []
    for target, analysis in data['results'].items():
        for pair in analysis.get('closest_pairs', []):
            all_distances.append(pair['distance'])
    
    all_distances = np.array(all_distances)
    n_total = len(all_distances)
    
    print("=" * 70)
    print("REFINED STATISTICAL TEST: √Z² PEAK ANALYSIS")
    print(f"√Z² Target: {SQRT_Z2:.6f} Å")
    print(f"Total pairs: {n_total}")
    print("=" * 70)

    # Histogram with 0.05 Å bins
    bins = np.arange(4.0, 8.0 + BIN_WIDTH, BIN_WIDTH)
    hist, bin_edges = np.histogram(all_distances, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Find bin for SQRT_Z2
    z_bin_idx = np.argmin(np.abs(bin_centers - SQRT_Z2))
    z_count = hist[z_bin_idx]
    z_center = bin_centers[z_bin_idx]

    # Local background (±0.5 Å excluding the target bin)
    window = 10 # ±0.5 Å for 0.05 bins
    lo = max(0, z_bin_idx - window)
    hi = min(len(hist), z_bin_idx + window + 1)
    neighbors = np.concatenate([hist[lo:z_bin_idx], hist[z_bin_idx+1:hi]])
    
    bg_mean = np.mean(neighbors)
    bg_std = np.std(neighbors)
    z_score = (z_count - bg_mean) / bg_std if bg_std > 0 else 0

    print(f"\nBin Analysis (width={BIN_WIDTH*1000:.0f} mÅ):")
    print(f"  Target Bin Center: {z_center:.3f} Å")
    print(f"  Target Bin Count:  {z_count}")
    print(f"  Local BG Mean:     {bg_mean:.2f}")
    print(f"  Local BG StdDev:   {bg_std:.2f}")
    print(f"  Z-Score:           {z_score:+.2f}σ")

    # Significance
    if z_score > 3:
        print("\n✅ SIGNIFICANT PEAK DETECTED at √Z².")
    elif z_score > 1.96:
        print("\n🟡 MARGINAL ELEVATION detected at √Z².")
    else:
        print("\n❌ NO SIGNIFICANT PEAK at √Z².")

    # Show distribution around the peak
    print("\nLocal Distribution (±0.5 Å around √Z²):")
    print(f"{'Bin (Å)':>10} {'Count':>8} {'Bar':>30}")
    max_local = max(hist[lo:hi]) if any(hist[lo:hi]) else 1
    for i in range(lo, hi):
        marker = " <== √Z²" if i == z_bin_idx else ""
        bar = "█" * int(30 * hist[i] / max_local)
        print(f"  {bin_centers[i]:>8.3f}  {hist[i]:>6d}  {bar}{marker}")

    # Percentile check
    matches_10ma = np.sum(np.abs(all_distances - SQRT_Z2) <= 0.01)
    matches_50ma = np.sum(np.abs(all_distances - SQRT_Z2) <= 0.05)
    print(f"\nExact matches (±10 mÅ): {matches_10ma} ({100*matches_10ma/n_total:.2f}%)")
    print(f"Exact matches (±50 mÅ): {matches_50ma} ({100*matches_50ma/n_total:.2f}%)")

    # Save summary
    summary = {
        "sqrt_z2": SQRT_Z2,
        "n_total": n_total,
        "z_score": z_score,
        "bin_width": BIN_WIDTH,
        "matches_10ma": int(matches_10ma),
        "matches_50ma": int(matches_50ma),
        "license": "AGPL-3.0-or-later"
    }
    
    with open('/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/sqrt_z2_validation_results.json', 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
