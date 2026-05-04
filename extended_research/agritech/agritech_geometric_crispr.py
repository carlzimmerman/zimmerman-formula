import requests
import os
import math
import numpy as np
from Bio.PDB import PDBParser

# --- AGRITECH: GEOMETRIC CRISPR (CRISPR-Z) ---
# Objective: Upgrade crop efficiency without introducing foreign genes.
# Methodology: Use precise CRISPR base editing to swap a single amino acid 
# into an aromatic ring (F, Y, W) to synthetically build a 5.62 A Tension Lock
# or 6.08 A Water Lock into critical agricultural enzymes.

# Target: RUBISCO (The bottleneck of global photosynthesis)
# PDB 1RCX (Spinach Rubisco - Empirical X-Ray Structure)
RUBISCO_PDB = "1RCX"
Z_TENSION_TARGET = 5.62
TOLERANCE = 0.20

def get_centroid(residue):
    # Get centroid of any residue (using C-alpha and C-beta for non-aromatics)
    atoms = [a.coord for a in residue if a.name in ['CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'NE1', 'CE3', 'CZ2', 'CZ3', 'CH2']]
    if not atoms: return None
    return np.mean(np.array(atoms), axis=0)

def is_aromatic(residue):
    return residue.resname in ['PHE', 'TYR', 'TRP', 'HIS']

def download_pdb(pdb_id, save_dir="agritech_structures"):
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    filepath = os.path.join(save_dir, f"{pdb_id}.pdb")
    if os.path.exists(filepath): return filepath
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as f: f.write(response.content)
            return filepath
    except Exception: pass
    return None

def find_crispr_z_targets(pdb_filepath):
    print(f"\n[*] Scanning Rubisco (PDB: {RUBISCO_PDB}) for CRISPR-Z Insertion Points...")
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure('rubisco', pdb_filepath)
    except Exception: return
    
    chain_L = list(structure[0].get_chains())[0] # Large subunit contains active site
    
    aromatics = []
    mutatable_targets = [] # Aliphatic/neutral residues we can mutate
    
    for res in chain_L:
        c = get_centroid(res)
        if c is None: continue
        if is_aromatic(res): aromatics.append((res, c))
        elif res.resname in ['LEU', 'VAL', 'ILE', 'ALA', 'SER']: mutatable_targets.append((res, c))
            
    print(f"[*] Found {len(aromatics)} native aromatic anchors.")
    print(f"[*] Found {len(mutatable_targets)} candidate mutation sites.")
    
    successes = []
    # We are looking for a non-aromatic residue that sits exactly ~5.62 A 
    # away from a native aromatic ring. If we mutate it to Phenylalanine, 
    # we instantly snap a Z-Manifold lock into existence.
    
    for native_r, native_c in aromatics:
        for mut_r, mut_c in mutatable_targets:
            dist = np.linalg.norm(native_c - mut_c)
            if abs(dist - Z_TENSION_TARGET) <= TOLERANCE:
                successes.append({
                    "anchor": f"{native_r.resname}{native_r.id[1]}",
                    "target": f"{mut_r.resname}{mut_r.id[1]}",
                    "distance": round(dist, 3)
                })
                
    print("\n=========================================================")
    print(" CRISPR-Z: RUBISCO SUPER-YIELD MUTATION TARGETS")
    print("=========================================================")
    if successes:
        successes.sort(key=lambda x: abs(x['distance'] - Z_TENSION_TARGET))
        print(f">> Found {len(successes)} perfect Geometric Edit locations.")
        print(">> By performing a single CRISPR point mutation (e.g., LEU -> PHE) at these coordinates,")
        print(">> we synthesize a 5.62 A Tension Lock, rigidifying Rubisco to prevent photorespiration.\n")
        
        for s in successes[:5]:
            print(f"   [MUTATE] {s['target']} -> PHE | Anchors to {s['anchor']} at {s['distance']} A (Tension Lock)")
    else:
        print("[-] No strict geometric edit sites found.")

if __name__ == "__main__":
    pdb_path = download_pdb(RUBISCO_PDB)
    if pdb_path:
        find_crispr_z_targets(pdb_path)
