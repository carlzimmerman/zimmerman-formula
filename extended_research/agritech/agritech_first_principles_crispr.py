import requests
import os
import math
import numpy as np
from Bio.PDB import PDBParser

# --- Z-SQUARED FIRST PRINCIPLES CRISPR-Z PIPELINE ---
# Integrating Geometric Constants (5.62 A) with Subatomic Volumetric Physics.
# Two atoms cannot occupy the same space (Pauli Exclusion Principle).
# We must scan for the geometric lock AND calculate the Free Volume of the pocket
# to ensure the massive Phenylalanine ring can physically fit without exploding the protein.

RUBISCO_PDB = "1RCX"
Z_TENSION_TARGET = 5.62
TOLERANCE = 0.20

# First Principles Constants
# A Phenylalanine ring requires a minimum clearance to avoid steric clash.
# The VDW radius of Carbon is ~1.7 A. We need the centroid to have at least 
# ~2.8 A clearance from non-participating backbone/sidechain atoms.
STERIC_CLEARANCE_RADIUS = 2.80 

def get_centroid(residue):
    atoms = [a.coord for a in residue if a.name in ['CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'NE1', 'CE3', 'CZ2', 'CZ3', 'CH2']]
    if not atoms: return None
    return np.mean(np.array(atoms), axis=0)

def get_all_atoms(chain):
    all_atoms = []
    for res in chain:
        for atom in res:
            all_atoms.append((res.id[1], atom.coord))
    return all_atoms

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

def check_steric_clash(mut_res_id, mut_centroid, anchor_res_id, all_atoms):
    """
    Scans a sphere of STERIC_CLEARANCE_RADIUS around the mutation centroid.
    If atoms (other than the backbone of the mutated residue or the target anchor)
    intrude into this sphere, it's a catastrophic steric clash.
    """
    clashes = 0
    for res_id, coord in all_atoms:
        # Ignore the target anchor (we want to touch it)
        if res_id == anchor_res_id: continue
        # Ignore the residue being mutated itself
        if res_id == mut_res_id: continue
        
        dist = np.linalg.norm(mut_centroid - coord)
        if dist < STERIC_CLEARANCE_RADIUS:
            clashes += 1
            
    return clashes

def run_first_principles_pipeline(pdb_filepath):
    print("=========================================================")
    print(" FIRST PRINCIPLES Z-SQUARED CRISPR-Z PIPELINE")
    print("=========================================================")
    print(f"[*] Target: Rubisco (PDB: {RUBISCO_PDB})")
    print(f"[*] Geometric Constraint: {Z_TENSION_TARGET} A +/- {TOLERANCE} A")
    print(f"[*] Subatomic Constraint: Pauli Exclusion Clearance > {STERIC_CLEARANCE_RADIUS} A")
    
    parser = PDBParser(QUIET=True)
    try: structure = parser.get_structure('rubisco', pdb_filepath)
    except Exception: return
    
    chain_L = list(structure[0].get_chains())[0]
    all_atoms = get_all_atoms(chain_L)
    
    aromatics = []
    mutatable_targets = [] 
    
    for res in chain_L:
        c = get_centroid(res)
        if c is None: continue
        if is_aromatic(res): aromatics.append((res, c))
        elif res.resname in ['LEU', 'VAL', 'ILE', 'ALA', 'SER', 'GLY']: mutatable_targets.append((res, c))
    
    viable_edits = []
    failed_edits = 0
    
    for native_r, native_c in aromatics:
        for mut_r, mut_c in mutatable_targets:
            dist = np.linalg.norm(native_c - mut_c)
            
            # 1. Geometric Check (Z-Manifold Distance)
            if abs(dist - Z_TENSION_TARGET) <= TOLERANCE:
                
                # 2. Subatomic Volumetric Check (Steric Clash)
                clashes = check_steric_clash(mut_r.id[1], mut_c, native_r.id[1], all_atoms)
                
                if clashes == 0:
                    viable_edits.append({
                        "anchor": f"{native_r.resname}{native_r.id[1]}",
                        "target": f"{mut_r.resname}{mut_r.id[1]}",
                        "distance": round(dist, 3)
                    })
                else:
                    failed_edits += 1

    print(f"\n[*] Pipeline Processed {len(mutatable_targets) * len(aromatics)} Combinations.")
    print(f"[*] Rejected {failed_edits} candidates due to catastrophic steric clash.")
    
    print("\n=========================================================")
    print(" SURVIVING FIRST-PRINCIPLES MUTATIONS")
    print("=========================================================")
    if viable_edits:
        print(f">> Found {len(viable_edits)} geometrically AND volumetrically perfect CRISPR-Z edits.\n")
        viable_edits.sort(key=lambda x: abs(x['distance'] - Z_TENSION_TARGET))
        for s in viable_edits:
            print(f"   [VIABLE] {s['target']} -> PHE | Anchors to {s['anchor']} at {s['distance']} A")
    else:
        print("[-] ZERO viable mutations found. The pocket architectures are too dense.")
        print("[-] Rubisco cannot be rigidified via CRISPR-Z at these specific sites without structural destruction.")

if __name__ == "__main__":
    pdb_path = download_pdb(RUBISCO_PDB)
    if pdb_path:
        run_first_principles_pipeline(pdb_path)
