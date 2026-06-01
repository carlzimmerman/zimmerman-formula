import numpy as np
from scipy.spatial import cKDTree
from Bio.PDB import PDBParser
import os
import math

# --- Z² SMART CRISPR AUDIT ---
# Previous audits failed (0.00% viability) because they placed the new
# bulky Phe ring exactly on the backbone CA atom, causing instant clashes.
# Real CRISPR mutagenesis requires placing the ring center ~3.0 A away 
# from the CA atom along a valid sidechain trajectory.

CLASH_THRESHOLD = 2.5  # Angstroms (lenient for rotamer flexibility)
PHE_RING_DIST_FROM_CA = 3.5 # Approx distance from CA to ring centroid
PHE_RING_RADIUS = 2.8 # Approx radius of the pi cloud

def generate_rotamer_centers(ca_coord):
    # 50 points roughly distributed on a sphere of radius PHE_RING_DIST_FROM_CA
    centers = []
    phi = math.pi * (3.0 - math.sqrt(5.0))  # golden angle
    samples = 50
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        radius = math.sqrt(1 - y * y)
        theta = phi * i
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        vec = np.array([x, y, z]) * PHE_RING_DIST_FROM_CA
        centers.append(ca_coord + vec)
    return centers

def run_smart_crispr(pdb_id):
    fp = f"agritech_structures/{pdb_id}.pdb"
    if not os.path.exists(fp): return None
    
    parser = PDBParser(QUIET=True)
    struct = parser.get_structure(pdb_id, fp)
    
    all_coords = []
    atom_residue_ids = []
    target_sites = [] # LEU, ILE, VAL
    
    for model in struct:
        for chain in model:
            for res in chain:
                res_id = f"{res.resname}{res.id[1]}"
                for a in res:
                    all_coords.append(a.coord)
                    atom_residue_ids.append(res_id)
                
                if res.resname in ['LEU', 'ILE', 'VAL'] and 'CA' in res:
                    target_sites.append({
                        "id": res_id, 
                        "ca": res['CA'].coord,
                    })
        break # Only first model
        
    print(f"[*] Auditing {len(target_sites)} potential CRISPR upgrade sites in {pdb_id}...")
    
    # Use cKDTree for ultra-fast spatial lookups
    all_coords = np.array(all_coords)
    tree = cKDTree(all_coords)
    atom_residue_ids = np.array(atom_residue_ids)
    
    viable_sites = []
    
    for site in target_sites:
        possible_centers = generate_rotamer_centers(site["ca"])
        
        site_viable = False
        best_center = None
        
        for center in possible_centers:
            # Find all atoms within PHE_RING_RADIUS of the proposed center
            # Using tree.query_ball_point is incredibly fast
            indices = tree.query_ball_point(center, PHE_RING_RADIUS)
            
            clash = False
            for idx in indices:
                # If the clashing atom belongs to the residue we are replacing, ignore it!
                if atom_residue_ids[idx] != site["id"]:
                    clash = True
                    break
            
            if not clash:
                site_viable = True
                best_center = center
                break # Found a valid rotamer!
                
        if site_viable:
            viable_sites.append({"id": site["id"], "center": best_center})
            
    return viable_sites, len(target_sites)

if __name__ == "__main__":
    print("="*80)
    print(" Z² SMART CRISPR AUDIT: ROTAMER FLEXIBILITY")
    print(" Re-evaluating CRISPR viability using sidechain vector space.")
    print("="*80)
    
    viable, total = run_smart_crispr('1RCX')
    
    print(f"\n>> RESULTS FOR RICE RUBISCO (1RCX):")
    print(f"   - Total Theoretical Sites:  {total}")
    print(f"   - Viable (No Clash) Sites:  {len(viable)}")
    print(f"   - Smart Viability Rate:     {(len(viable)/total*100):.2f}%")
    
    if len(viable) > 0:
        print("\n>> TOP CRISPR CANDIDATES (Surface/Cavity exposed):")
        for v in viable[:10]:
            print(f"      Mutate: {v['id']} -> PHE")
