#!/usr/bin/env python3
"""
Aromatic Angle Validator: Finding the Z-Manifold
================================================

This script analyzes the angular distribution (dihedral angles) of 
aromatic stacking pairs at the 5.72 Å √Z² mode. 

Goal: Refine the Aromatic Clamp design from simple distance to 
"Geometric Resonance" (Distance + Angle).

SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
import os
from Bio.PDB import PDBParser
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

PDB_CACHE = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/validation/pdb_cache"
ATTRACTOR_MODE = 5.72
TOLERANCE = 0.5  # Focus on pairs within 0.5A of the mode
AROMATIC_RESIDUES = {'PHE', 'TYR', 'TRP'}

def get_ring_plane(res):
    rn = res.get_resname()
    # Atoms that define the aromatic ring plane
    atoms = {
        'PHE': ['CG', 'CD1', 'CE1', 'CZ', 'CE2', 'CD2'],
        'TYR': ['CG', 'CD1', 'CE1', 'CZ', 'CE2', 'CD2'],
        'TRP': ['CD2', 'CE2', 'CE3', 'CZ3', 'CH2', 'CZ2'],
    }
    if rn not in atoms: return None, None
    coords = [res[a].get_vector().get_array() for a in atoms[rn] if a in res]
    if len(coords) < 3: return None, None
    
    centroid = np.mean(coords, axis=0)
    # Calculate normal vector to the plane using SVD
    centered_coords = coords - centroid
    _, _, vh = np.linalg.svd(centered_coords)
    normal = vh[2, :] # Normal vector is the last row of VH
    return centroid, normal

def analyze_angles():
    angles = []
    
    parser = PDBParser(QUIET=True)
    pdb_files = [f for f in os.listdir(PDB_CACHE) if f.endswith('.pdb')][:50]
    
    print(f"[*] Scanning {len(pdb_files)} structures for angular resonance at {ATTRACTOR_MODE} Å...")

    for pdb_file in pdb_files:
        try:
            struct = parser.get_structure('S', os.path.join(PDB_CACHE, pdb_file))
        except: continue
        
        for model in struct:
            aromatic_data = []
            for res in model.get_residues():
                if res.get_resname() in AROMATIC_RESIDUES:
                    centroid, normal = get_ring_plane(res)
                    if centroid is not None:
                        aromatic_data.append((centroid, normal))
            
            # Compare all pairs
            for i in range(len(aromatic_data)):
                for j in range(i + 1, len(aromatic_data)):
                    c1, n1 = aromatic_data[i]
                    c2, n2 = aromatic_data[j]
                    
                    dist = np.linalg.norm(c1 - c2)
                    if abs(dist - ATTRACTOR_MODE) < TOLERANCE:
                        # Calculate angle between normal vectors
                        cos_theta = np.abs(np.dot(n1, n2)) # Absolute because rings are bidirectional
                        cos_theta = np.clip(cos_theta, 0, 1)
                        angle = np.degrees(np.arccos(cos_theta))
                        angles.append(angle)

    if not angles:
        print("[!] No pairs found at this distance.")
        return

    # Statistical Summary
    mean_angle = np.mean(angles)
    median_angle = np.median(angles)
    
    print(f"\n[+] Found {len(angles)} stacking pairs at the {ATTRACTOR_MODE} Å mode.")
    print(f"[+] Mean Angle: {mean_angle:.2f}°")
    print(f"[+] Median Angle: {median_angle:.2f}°")
    
    # Histogram logic (text-based for now)
    bins = np.linspace(0, 90, 10)
    hist, _ = np.histogram(angles, bins=bins)
    
    print("\nAngular Distribution (0° to 90°):")
    for i in range(len(hist)):
        bar = "#" * int(hist[i] / max(hist) * 40)
        print(f"{bins[i]:4.1f}° | {bar} ({hist[i]})")

    print("\n[CONCLUSION]:")
    if median_angle < 30:
        print(">>> Resonant Mode: PARALLEL STACKING (Face-to-Face)")
    elif median_angle > 60:
        print(">>> Resonant Mode: T-SHAPED STACKING (Edge-to-Face)")
    else:
        print(">>> Resonant Mode: OFFSET-PARALLEL / MIXED")

if __name__ == "__main__":
    analyze_angles()
