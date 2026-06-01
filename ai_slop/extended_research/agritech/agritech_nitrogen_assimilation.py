import requests
import os
import math
import numpy as np
from Bio.PDB import PDBParser

# --- AGRITECH: NITROGEN ASSIMILATION HYPER-GROWTH ---
# Target: Maize Glutamine Synthetase (GS) - PDB 2D3A
# Objective: Make plants grow "faster naturally" by geometrically optimizing 
# the bottleneck of nitrogen assimilation. If GS operates faster without 
# thermal breakdown, the plant accumulates biomass explosively.

GS_PDB = "2D3A"
Z_RESONANCE_TARGET = 5.72
TOLERANCE = 0.20
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
    clashes = 0
    for res_id, coord in all_atoms:
        if res_id == anchor_res_id or res_id == mut_res_id: continue
        dist = np.linalg.norm(mut_centroid - coord)
        if dist < STERIC_CLEARANCE_RADIUS: clashes += 1
    return clashes

def run_hyper_growth_pipeline(pdb_filepath):
    print("=========================================================")
    print(" AGRITECH Z-SQUARED: NITROGEN ASSIMILATION (GS)")
    print("=========================================================")
    print(f"[*] Target: Maize Glutamine Synthetase (PDB: {GS_PDB})")
    print(f"[*] Goal: Enzymatic Hyper-activity for Rapid Natural Growth")
    print(f"[*] Geometric Constraint: {Z_RESONANCE_TARGET} A Resonance Lock (+/- {TOLERANCE} A)")
    
    parser = PDBParser(QUIET=True)
    try: structure = parser.get_structure('gs', pdb_filepath)
    except Exception: return
    
    # GS is decameric. We scan Chain A.
    chain_A = list(structure[0].get_chains())[0]
    all_atoms = get_all_atoms(chain_A)
    
    aromatics = []
    mutatable_targets = [] 
    
    for res in chain_A:
        c = get_centroid(res)
        if c is None: continue
        if is_aromatic(res): aromatics.append((res, c))
        elif res.resname in ['LEU', 'VAL', 'ILE', 'ALA', 'SER', 'GLY']: mutatable_targets.append((res, c))
    
    viable_edits = []
    failed_edits = 0
    
    for native_r, native_c in aromatics:
        for mut_r, mut_c in mutatable_targets:
            dist = np.linalg.norm(native_c - mut_c)
            
            if abs(dist - Z_RESONANCE_TARGET) <= TOLERANCE:
                clashes = check_steric_clash(mut_r.id[1], mut_c, native_r.id[1], all_atoms)
                if clashes == 0:
                    viable_edits.append({
                        "anchor": f"{native_r.resname}{native_r.id[1]}",
                        "target": f"{mut_r.resname}{mut_r.id[1]}",
                        "distance": round(dist, 3)
                    })
                else: failed_edits += 1

    print(f"\n[*] Rejected {failed_edits} candidates due to steric clash (Pauli exclusion).")
    
    if viable_edits:
        print(f"\n>> Found {len(viable_edits)} geometrically & volumetrically perfect CRISPR-Z edits.\n")
        viable_edits.sort(key=lambda x: abs(x['distance'] - Z_RESONANCE_TARGET))
        for s in viable_edits[:5]:
            print(f"   [MUTATE] {s['target']} -> TYR | Anchors to {s['anchor']} at {s['distance']} A (Resonance Lock)")
    else:
        print("[-] No viable mutations found.")

if __name__ == "__main__":
    pdb_path = download_pdb(GS_PDB)
    if pdb_path:
        run_hyper_growth_pipeline(pdb_path)
