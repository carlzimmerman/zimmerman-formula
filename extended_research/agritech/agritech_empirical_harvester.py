import requests
import os
import math
import numpy as np
from Bio.PDB import PDBParser

# --- AGRITECH EMPIRICAL PDB TARGETS ---
# Strict reliance on X-Ray Crystallography / Cryo-EM to eliminate hallucination
AGRITECH_TARGETS = {
    "Plant_Aquaporin_SoPIP2": "1Z98",  # Spinach Aquaporin (Drought Lock)
    "Plant_Chitinase": "1W9P",         # Rice Chitinase (Fungal Defense)
    "Plant_Polyphenol_Oxidase": "2P3X" # Sweet Potato PPO (Polyphenol yield)
}

Z_CONSTANTS = {
    "Tension": 5.62,
    "Resonance": 5.72,
    "Golden_Triangle": 6.08
}
TOLERANCE = 0.20

def get_aromatic_centroid(residue):
    atoms = []
    target_atoms = []
    if residue.resname == 'TRP': target_atoms = ['CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2']
    elif residue.resname in ['TYR', 'PHE']: target_atoms = ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ']
    elif residue.resname == 'HIS': target_atoms = ['CG', 'ND1', 'CD2', 'CE1', 'NE2']
    else: return None
        
    for atom in residue:
        if atom.name in target_atoms:
            atoms.append(atom.coord)
            
    if len(atoms) < 5: return None
    return np.mean(np.array(atoms), axis=0)

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
    except Exception as e:
        print(f"  [!] Failed to download: {e}")
    return None

def scan_agritech_pdb(pdb_filepath):
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure('plant', pdb_filepath)
    except Exception: return []
        
    aromatics = []
    for model in structure:
        for chain in model:
            for residue in chain:
                centroid = get_aromatic_centroid(residue)
                if centroid is not None:
                    aromatics.append((residue, centroid))
                    
    matches = []
    for i in range(len(aromatics)):
        for j in range(i + 1, len(aromatics)):
            r1, c1 = aromatics[i]
            r2, c2 = aromatics[j]
            dist = np.linalg.norm(c1 - c2)
            
            for z_name, z_val in Z_CONSTANTS.items():
                if abs(dist - z_val) <= TOLERANCE:
                    matches.append({
                        "res1": f"{r1.resname}{r1.id[1]}",
                        "res2": f"{r2.resname}{r2.id[1]}",
                        "distance": round(dist, 3),
                        "z_type": z_name
                    })
    return matches

def run_harvest():
    print("=========================================================")
    print(" AGRITECH EMPIRICAL Z-MANIFOLD HARVESTER")
    print("=========================================================")
    
    for name, pdb_id in AGRITECH_TARGETS.items():
        print(f"\n[*] Fetching Real Data for {name} (PDB: {pdb_id})...")
        pdb_path = download_pdb(pdb_id)
        if not pdb_path: continue
        
        matches = scan_agritech_pdb(pdb_path)
        if matches:
            print(f"  [+] Found {len(matches)} intrinsic Z-Manifold locks!")
            matches.sort(key=lambda x: abs(x['distance'] - Z_CONSTANTS[x['z_type']]))
            for m in matches[:3]:
                print(f"      -> {m['res1']} to {m['res2']}: {m['distance']} A ({m['z_type']})")
        else:
            print("  [-] No Z-Manifold pockets found.")

if __name__ == "__main__":
    run_harvest()
