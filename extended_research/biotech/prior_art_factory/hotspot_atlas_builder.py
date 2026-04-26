#!/usr/bin/env python3
"""
Hotspot Atlas Builder: The Geometric Map of Medicine
====================================================

This script generates a comprehensive "Atlas" of aromatic hotspots
across major disease targets, mapping them to our Geometric Scaling 
Laws (Primary, Golden, Harmonic, Octave).

It outputs a structured JSON "Hotspot Atlas" that can be used to
generate precision therapeutics.

SPDX-License-Identifier: AGPL-3.0-or-later
"""

import numpy as np
import os
import json
from Bio.PDB import PDBParser

# ─────────────────────────────────────────────
# CONFIG & SCALING LAWS
# ─────────────────────────────────────────────

PDB_CACHE = "/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/validation/pdb_cache"
ATTRACTORS = {
    "PRIMARY": 5.72,
    "GOLDEN": 9.10,
    "HARMONIC": 10.00,
    "OCTAVE": 11.70
}

DISEASE_TARGETS = {
    "BACE1": {"pdb": "1w5o", "chain": "A"},
    "PDL1": {"pdb": "4zqk", "chain": "B"},
    "PCSK9": {"pdb": "2p4e", "chain": "A"},
    "KRAS_G12D": {"pdb": "8afb", "chain": "A"},
    "p53": {"pdb": "1tup", "chain": "B"},
    "TNF_alpha": {"pdb": "1tnf", "chain": "A"},
    "SARS_Spike": {"pdb": "6m0j", "chain": "E"},
    "HIV_gp120": {"pdb": "1gc1", "chain": "G"},
    "EGFR": {"pdb": "1ivo", "chain": "A"},
    "HER2": {"pdb": "1n8z", "chain": "A"}
}

AROMATIC_RESIDUES = {'PHE', 'TYR', 'TRP'}

# ─────────────────────────────────────────────
# GEOMETRY ENGINE
# ─────────────────────────────────────────────

def get_ring_centroid(res):
    rn = res.get_resname()
    atoms = {'PHE':['CG','CZ'], 'TYR':['CG','CZ'], 'TRP':['CD2','CH2']}
    if rn not in atoms: return None
    try:
        coords = [res[a].get_vector().get_array() for a in atoms[rn] if a in res]
        return np.mean(coords, axis=0) if len(coords) >= 1 else None
    except: return None

def build_atlas():
    atlas = {}
    parser = PDBParser(QUIET=True)
    
    print(f"[*] Building Hotspot Atlas for {len(DISEASE_TARGETS)} targets...")

    for name, info in DISEASE_TARGETS.items():
        pdb_path = os.path.join(PDB_CACHE, f"{info['pdb']}.pdb")
        if not os.path.exists(pdb_path): continue
        
        try:
            struct = parser.get_structure(name, pdb_path)
            model = struct[0]
            chain = model[info['chain']]
        except: continue
        
        target_hotspots = []
        residues = []
        for res in chain:
            if res.get_resname() in AROMATIC_RESIDUES:
                c = get_ring_centroid(res)
                if c is not None:
                    residues.append({
                        'id': f"{res.get_resname()}{res.id[1]}",
                        'centroid': c
                    })
        
        # Find matches for all attractors
        for i in range(len(residues)):
            for j in range(i + 1, len(residues)):
                r1 = residues[i]
                r2 = residues[j]
                dist = np.linalg.norm(r1['centroid'] - r2['centroid'])
                
                for mode, target_dist in ATTRACTORS.items():
                    if abs(dist - target_dist) < 0.6: # 0.6A tolerance
                        target_hotspots.append({
                            'pair': [r1['id'], r2['id']],
                            'distance': round(dist, 2),
                            'mode': mode,
                            'target_dist': target_dist,
                            'delta': round(abs(dist - target_dist), 2)
                        })
        
        atlas[name] = {
            'pdb_id': info['pdb'],
            'description': info.get('description', ''),
            'hotspot_count': len(target_hotspots),
            'mappings': target_hotspots
        }
        print(f"  [+] {name}: Found {len(target_hotspots)} geometric mappings.")

    # Save Atlas
    out_path = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/prior_art_factory/HOTSPOT_ATLAS.json'
    with open(out_path, 'w') as f:
        json.dump(atlas, f, indent=2)
    
    print(f"\n✅ Hotspot Atlas completed: {out_path}")

if __name__ == "__main__":
    build_atlas()
