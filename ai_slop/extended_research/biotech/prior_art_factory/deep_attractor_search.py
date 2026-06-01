#!/usr/bin/env python3
"""
Deep Attractor Search: Finding Higher-Order Resonances
======================================================

This script scans the PDB for secondary and tertiary geometric 
attractors beyond the primary 5.72 Å mode.

It tests:
1. Multiples (2x, 3x)
2. Harmonics (sqrt(2), sqrt(3))
3. The Golden Ratio (phi)

SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
import os
from Bio.PDB import PDBParser
import json

PDB_CACHE = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/validation/pdb_cache"
AROMATIC_RESIDUES = {'PHE', 'TYR', 'TRP'}

def get_ring_centroid(res):
    rn = res.get_resname()
    atoms = {
        'PHE': ['CG','CD1','CD2','CE1','CE2','CZ'],
        'TYR': ['CG','CD1','CD2','CE1','CE2','CZ'],
        'TRP': ['CD2','CE2','CE3','CZ2','CZ3','CH2'],
    }
    if rn not in atoms: return None
    coords = [res[a].get_vector().get_array() for a in atoms[rn] if a in res]
    return np.mean(coords, axis=0) if len(coords) >= 3 else None

def search_resonances():
    all_dists = []
    parser = PDBParser(QUIET=True)
    pdb_files = [f for f in os.listdir(PDB_CACHE) if f.endswith('.pdb')][:100]
    
    print(f"[*] Scanning {len(pdb_files)} structures for multi-order attractors...")

    for pdb_file in pdb_files:
        try:
            struct = parser.get_structure('S', os.path.join(PDB_CACHE, pdb_file))
        except: continue
        
        for model in struct:
            centroids = []
            for res in model.get_residues():
                if res.get_resname() in AROMATIC_RESIDUES:
                    c = get_ring_centroid(res)
                    if c is not None: centroids.append(c)
            
            # Distance matrix
            for i in range(len(centroids)):
                for j in range(i + 1, len(centroids)):
                    dist = np.linalg.norm(centroids[i] - centroids[j])
                    if dist < 20.0: # Focus on local interactions
                        all_dists.append(dist)

    if not all_dists: return

    # Histogram Analysis
    bins = np.linspace(3.0, 20.0, 171) # 0.1A resolution
    hist, bin_edges = np.histogram(all_dists, bins=bins)
    
    # Find Peaks
    peaks = []
    for i in range(1, len(hist)-1):
        if hist[i] > hist[i-1] and hist[i] > hist[i+1] and hist[i] > 50:
            peaks.append((bin_edges[i], hist[i]))
            
    peaks.sort(key=lambda x: -x[1])
    
    print("\n[TOP GEOMETRIC ATTRACTORS FOUND]:")
    for dist, count in peaks[:10]:
        # Relationship to Primary 5.72A
        ratio = dist / 5.72
        note = ""
        if abs(ratio - 1.0) < 0.05: note = "(PRIMARY √Z²)"
        elif abs(ratio - 0.707) < 0.05: note = "(HARM: 1/√2)"
        elif abs(ratio - 1.414) < 0.05: note = "(HARM: √2)"
        elif abs(ratio - 1.618) < 0.05: note = "(GOLDEN: φ)"
        elif abs(ratio - 1.732) < 0.05: note = "(HARM: √3)"
        elif abs(ratio - 2.0) < 0.05: note = "(OCTAVE: 2x)"
        
        print(f"  {dist:6.2f} Å | Hits: {count:5} | {note}")

if __name__ == "__main__":
    search_resonances()
