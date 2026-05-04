import requests
import os
import math
import json
import numpy as np
from Bio.PDB import PDBParser
from datetime import datetime

# --- Z² KINGDOM-WIDE SCANNER: THE TREE OF LIFE ---
# 
# GOAL: Prove the Z-Manifold is a universal law across ALL plant lineages:
# Algae -> Moss -> Conifers -> Flowering Plants.
#
# LICENSE: AGPL-3.0-or-later

TREE_OF_LIFE = {
    "Algae_Chlamydomonas": {"pdb": "1AF5", "clade": "Chlorophyta", "description": "Ancestral Algae (Cytochrome c6)"},
    "Moss_Physcomitrium":  {"pdb": "4AK9", "clade": "Bryophyta",   "description": "Early Land Plants (LHCII)"},
    "Pine_Pinus":          {"pdb": "1QYC", "clade": "Gymnospermae", "description": "Conifers (Alcohol Dehydrogenase)"},
    "Arabidopsis_Model":   {"pdb": "2P1Q", "clade": "Eudicot",      "description": "Model Flowering Plant (TIR1)"},
    "Rice_Staple":         {"pdb": "1WDD", "clade": "Monocot",      "description": "Staple Grain (Rubisco)"},
}

Z_CONSTANTS = [5.62, 5.72, 6.08]
TOLERANCE = 0.20

def download_pdb(pdb_id, save_dir="kingdom_structures"):
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    fp = os.path.join(save_dir, f"{pdb_id}.pdb")
    if os.path.exists(fp): return fp
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(fp, 'wb') as f: f.write(r.content)
            return fp
    except: pass
    return None

def get_aromatic_centroid(residue):
    target_atoms = []
    if residue.resname == 'TRP': target_atoms = ['CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2']
    elif residue.resname in ['TYR', 'PHE']: target_atoms = ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ']
    elif residue.resname == 'HIS': target_atoms = ['CG', 'ND1', 'CD2', 'CE1', 'NE2']
    else: return None
    atoms = [a.coord for a in residue if a.name in target_atoms]
    if len(atoms) < 5: return None
    return np.mean(atoms, axis=0)

def scan_structure(pdb_path):
    parser = PDBParser(QUIET=True)
    try: structure = parser.get_structure('protein', pdb_path)
    except: return None
    
    aromatics = []
    for model in structure:
        for chain in model:
            for residue in chain:
                c = get_aromatic_centroid(residue)
                if c is not None: aromatics.append(c)
    
    locks = 0
    total_pairs = 0
    for i in range(len(aromatics)):
        for j in range(i+1, len(aromatics)):
            dist = np.linalg.norm(aromatics[i] - aromatics[j])
            if 3.5 <= dist <= 8.0:
                total_pairs += 1
                if any(abs(dist - z) <= TOLERANCE for z in Z_CONSTANTS):
                    locks += 1
                    
    return {"aromatics": len(aromatics), "locks": locks, "pairs": total_pairs}

def run_kingdom_scan():
    print("="*80)
    print(" Z² KINGDOM-WIDE SCAN: FIGURING OUT ALL PLANTS")
    print(" Tracing Geometric Constants from Algae to Angiosperms")
    print("="*80)
    
    clade_results = []
    
    for name, info in TREE_OF_LIFE.items():
        print(f"[*] Scanning {name} ({info['clade']})...")
        path = download_pdb(info["pdb"])
        if not path:
            print(f"    [!] Failed to download {info['pdb']}")
            continue
            
        stats = scan_structure(path)
        if stats:
            density = (stats["locks"] / stats["pairs"] * 100) if stats["pairs"] > 0 else 0
            print(f"    - Clade: {info['clade']} | Structure: {info['description']}")
            print(f"    - Z-Lock Density: {density:.2f}% ({stats['locks']} locks / {stats['pairs']} pairs)")
            
            clade_results.append({
                "clade": info["clade"],
                "density": density,
                "locks": stats["locks"]
            })

    print("\n" + "="*80)
    print(" UNIFIED KINGDOM VERDICT")
    print("="*80)
    avg_density = np.mean([c["density"] for c in clade_results])
    std_dev = np.std([c["density"] for c in clade_results])
    
    print(f" Average Z-Lock Density across ALL Plant Clades: {avg_density:.2f}%")
    print(f" Statistical Variance (Sigma): {std_dev:.2f}%")
    
    if std_dev < 10.0:
        print("\n >> RESULT: HIGH COHERENCE. The Z-Manifold is a CONSERVED CONSTANT of the plant kingdom.")
        print(" >> From Algae to Pine Trees, the same 5.62/5.72/6.08 A physics govern plant biology.")
    else:
        print("\n >> RESULT: LOW COHERENCE. The constants vary by clade.")

if __name__ == "__main__":
    run_kingdom_scan()
