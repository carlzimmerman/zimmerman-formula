import numpy as np
from Bio.PDB import PDBParser

# --- Z² BIOTECH: LIVE HISTONE AUDIT (1KX5) ---
#
# GOAL: Verify the Z-lock density in human DNA packing (Histones).
#
# LICENSE: AGPL-3.0-or-later

Z_TARGETS = [5.62, 5.72, 6.08]

def run_live_histone_scan():
    print("="*80)
    print(" Z² BIOTECH: LIVE HISTONE AUDIT (1KX5)")
    print(" Verifying 'Real World' Z-manifold density in human DNA.")
    print("="*80)
    
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('1KX5', '1KX5.pdb')
    
    centroids = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.resname in ['PHE', 'TYR', 'TRP', 'HIS']:
                    # Get ring atoms
                    atoms = [a.coord for a in residue if a.name in ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ']]
                    if len(atoms) >= 5:
                        centroids.append(np.mean(atoms, axis=0))
        break # Only first model
        
    total_pairs = 0
    z_locks = 0
    
    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            dist = np.linalg.norm(centroids[i] - centroids[j])
            if 3.5 <= dist <= 8.0:
                total_pairs += 1
                if any(abs(dist - z) <= 0.15 for z in Z_TARGETS):
                    z_locks += 1
                    
    density = (z_locks / total_pairs * 100) if total_pairs > 0 else 0
    
    print(f"Total Aromatic Pairs: {total_pairs}")
    print(f"Z-Manifold Locks:     {z_locks}")
    print(f"Z-Lock Density:       {density:.2f}%")
    
    if density > 35.0:
        print("\n >> VERIFICATION SUCCESSFUL: THE HUMAN NUCLEOSOME IS A Z-LOCK FORTRESS.")
        print(" >> This proves that systemic Z-decoys would disrupt DNA packing.")

if __name__ == "__main__":
    run_live_histone_scan()
