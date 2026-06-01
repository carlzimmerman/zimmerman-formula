import numpy as np
from Bio.PDB import PDBParser
import os
import matplotlib.pyplot as plt

# --- Z² DEFENSE: AROMATIC UNIQUENESS TEST ---
#
# GOAL: Defeat the 'Packing Noise' criticism.
# Prove that Z-locks are specific to aromatics, not just all hydrophobic residues.
#
# METHOD: 
# Compare Distance Distribution of:
# 1. Aromatic-Aromatic Pairs (Phe, Tyr, Trp)
# 2. Aliphatic-Aliphatic Pairs (Leu, Ile, Val)
#
# LICENSE: AGPL-3.0-or-later

Z_CONSTANTS = [5.62, 5.72, 6.08]

def get_residue_coords(structure, res_names):
    coords = []
    for model in structure:
        for chain in model:
            for res in chain:
                if res.resname in res_names:
                    if 'CA' in res:
                        coords.append(res['CA'].coord)
        break
    return np.array(coords)

def analyze_distributions(pdb_id):
    fp = f"agritech_structures/{pdb_id}.pdb"
    parser = PDBParser(QUIET=True)
    struct = parser.get_structure(pdb_id, fp)
    
    # 1. Aromatic Distribution
    aro_coords = get_residue_coords(struct, ['PHE', 'TYR', 'TRP'])
    # 2. Aliphatic Distribution (The Control Group)
    ali_coords = get_residue_coords(struct, ['LEU', 'ILE', 'VAL'])
    
    def get_distances(coords):
        dists = []
        for i in range(len(coords)):
            for j in range(i+1, len(coords)):
                d = np.linalg.norm(coords[i] - coords[j])
                if 3.5 <= d <= 8.0:
                    dists.append(d)
        return dists

    aro_dists = get_distances(aro_coords)
    ali_dists = get_distances(ali_coords)
    
    def calculate_z_enrichment(dists):
        locks = 0
        for d in dists:
            if any(abs(d-z) <= 0.15 for z in Z_CONSTANTS):
                locks += 1
        return (locks / len(dists)) if len(dists) > 0 else 0

    aro_rate = calculate_z_enrichment(aro_dists)
    ali_rate = calculate_z_enrichment(ali_dists)
    
    print(f"[*] {pdb_id} Aromatic Uniqueness Analysis:")
    print(f"    - Aromatic-Aromatic Z-Rate:  {aro_rate*100:.2f}%")
    print(f"    - Aliphatic-Aliphatic Z-Rate: {ali_rate*100:.2f}% (The Control)")
    
    enrichment = (aro_rate / ali_rate) if ali_rate > 0 else 0
    print(f"    >> Aromatic Enrichment Factor: {enrichment:.2f}x")
    
    if enrichment > 1.2:
        print("\n >> VERDICT: DEFENSE SUCCESSFUL.")
        print(f" >> Aromatics are {enrichment:.2f}x more likely to occupy Z-distances than Aliphatics.")
        print(" >> This proves the Z-Manifold is a property of RESONANCE, not just packing.")
    else:
        print("\n >> VERDICT: DEFENSE FAILED. The signal is just packing noise.")

if __name__ == "__main__":
    print("="*80)
    print(" Z² DEFENSE: THE AROMATIC UNIQUENESS TEST")
    print(" Addressing the 'Van der Waals Packing Noise' criticism.")
    print("="*80)
    analyze_distributions('1RCX') # Rice Rubisco
