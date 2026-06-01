#!/usr/bin/env python3
"""
Z² Statistical Validation: Is 6.015 Å special?
================================================

Measures ALL aromatic centroid-centroid distances in a large sample
of high-resolution PDB structures and tests whether Z² = 6.015 Å
is a statistically significant peak in the distribution.

SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2026 Carl Zimmerman
"""

import os
import numpy as np
from Bio.PDB import PDBParser
import json

Z2 = 6.015152508891966
BIN_WIDTH = 0.020  # 20 mÅ bins for histogram

def ring_centroid(res):
    rn = res.get_resname()
    atoms = {'PHE':['CG','CD1','CD2','CE1','CE2','CZ'],
             'TYR':['CG','CD1','CD2','CE1','CE2','CZ'],
             'TRP':['CD2','CE2','CE3','CZ2','CZ3','CH2']}
    if rn not in atoms: return None
    coords = [res[a].get_vector().get_array() for a in atoms[rn] if a in res]
    return np.mean(coords, axis=0) if len(coords) >= 3 else None

def collect_aromatic_distances(pdb_path, max_dist=8.0):
    """Collect all aromatic centroid-centroid distances < max_dist from a PDB."""
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure('p', pdb_path)
    except:
        return []
    
    distances = []
    model = list(structure)[0]  # First model only
    
    for chain in model:
        aromatics = []
        for res in chain:
            if res.get_resname() in ['PHE', 'TYR', 'TRP']:
                c = ring_centroid(res)
                if c is not None:
                    aromatics.append(c)
        
        # Intra-chain pairs
        for i in range(len(aromatics)):
            for j in range(i + 1, len(aromatics)):
                d = np.linalg.norm(aromatics[i] - aromatics[j])
                if d <= max_dist:
                    distances.append(d)
    
    # Inter-chain pairs too
    all_aromatics = []
    for chain in model:
        for res in chain:
            if res.get_resname() in ['PHE', 'TYR', 'TRP']:
                c = ring_centroid(res)
                if c is not None:
                    all_aromatics.append((chain.id, c))
    
    for i in range(len(all_aromatics)):
        for j in range(i + 1, len(all_aromatics)):
            if all_aromatics[i][0] != all_aromatics[j][0]:  # Different chains
                d = np.linalg.norm(all_aromatics[i][1] - all_aromatics[j][1])
                if d <= max_dist:
                    distances.append(d)
    
    return distances

def main():
    cache_dir = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/validation/pdb_cache/'
    pdbs = [f for f in os.listdir(cache_dir) if f.endswith('.pdb')]
    
    print(f"Z² STATISTICAL VALIDATION")
    print(f"========================")
    print(f"Z² = {Z2:.6f} Å")
    print(f"Scanning {len(pdbs)} PDB structures...")
    print()
    
    all_distances = []
    structures_with_aromatics = 0
    
    for pdb in pdbs:
        dists = collect_aromatic_distances(os.path.join(cache_dir, pdb))
        if dists:
            structures_with_aromatics += 1
            all_distances.extend(dists)
    
    all_distances = np.array(all_distances)
    print(f"Structures with aromatics: {structures_with_aromatics}")
    print(f"Total aromatic centroid-centroid distances (< 8 Å): {len(all_distances)}")
    print()
    
    if len(all_distances) == 0:
        print("No data collected!")
        return
    
    # Build histogram
    bins = np.arange(4.0, 8.0 + BIN_WIDTH, BIN_WIDTH)
    hist, bin_edges = np.histogram(all_distances, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Find the bin containing Z²
    z2_bin_idx = np.argmin(np.abs(bin_centers - Z2))
    z2_count = hist[z2_bin_idx]
    z2_bin_center = bin_centers[z2_bin_idx]
    
    # Local background: average of neighboring bins (±5 bins, excluding Z² bin)
    neighbor_range = 10
    lo = max(0, z2_bin_idx - neighbor_range)
    hi = min(len(hist), z2_bin_idx + neighbor_range + 1)
    neighbors = np.concatenate([hist[lo:z2_bin_idx], hist[z2_bin_idx+1:hi]])
    bg_mean = np.mean(neighbors)
    bg_std = np.std(neighbors)
    
    # Z-score
    z_score = (z2_count - bg_mean) / bg_std if bg_std > 0 else 0
    
    print(f"HISTOGRAM ANALYSIS (bin width = {BIN_WIDTH*1000:.0f} mÅ)")
    print(f"-----------------------------------------------")
    print(f"Z² bin center: {z2_bin_center:.3f} Å")
    print(f"Z² bin count:  {z2_count}")
    print(f"Local background mean: {bg_mean:.1f}")
    print(f"Local background std:  {bg_std:.1f}")
    print(f"Z-score at Z²: {z_score:+.2f}")
    print()
    
    if z_score > 3.0:
        print(f"✅ SIGNIFICANT: Z² = 6.015 Å shows a {z_score:.1f}σ peak!")
        print(f"   This suggests Z² IS a preferred aromatic stacking distance.")
    elif z_score > 2.0:
        print(f"🟡 MARGINAL: Z² shows a {z_score:.1f}σ elevation.")
        print(f"   Suggestive but not conclusive.")
    else:
        print(f"❌ NOT SIGNIFICANT: Z² shows only {z_score:.1f}σ elevation.")
        print(f"   6.015 Å is NOT a statistically special stacking distance.")
        print(f"   The Influenza NA match may be coincidental.")
    
    # Print the full distribution around Z²
    print()
    print(f"DISTRIBUTION AROUND Z² (4.5-7.5 Å range):")
    print(f"{'Bin (Å)':>10} {'Count':>8} {'Bar':>30}")
    max_count = max(hist[hist > 0]) if any(hist > 0) else 1
    for i in range(len(hist)):
        if 4.5 <= bin_centers[i] <= 7.5:
            bar_len = int(30 * hist[i] / max_count) if max_count > 0 else 0
            marker = " ◄── Z²" if i == z2_bin_idx else ""
            print(f"  {bin_centers[i]:>7.3f}  {hist[i]:>6d}  {'█' * bar_len}{marker}")
    
    # Count exact matches at various thresholds
    print()
    print(f"MATCHES AT Z² = {Z2:.4f} Å:")
    for threshold in [10, 50, 100, 500]:
        n = np.sum(np.abs(all_distances - Z2) * 1000 <= threshold)
        pct = 100 * n / len(all_distances) if len(all_distances) > 0 else 0
        print(f"  Within ±{threshold:>4d} mÅ: {n:>5d} ({pct:.2f}%)")
    
    # Save results
    results = {
        'z2_constant': Z2,
        'total_structures': len(pdbs),
        'structures_with_aromatics': structures_with_aromatics,
        'total_distances': int(len(all_distances)),
        'z_score': float(z_score),
        'z2_bin_count': int(z2_count),
        'background_mean': float(bg_mean),
        'background_std': float(bg_std),
        'distribution': {f"{bin_centers[i]:.3f}": int(hist[i]) for i in range(len(hist))},
        'license': 'AGPL-3.0-or-later'
    }
    
    out = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/z2_statistical_validation.json'
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out}")

if __name__ == "__main__":
    main()
