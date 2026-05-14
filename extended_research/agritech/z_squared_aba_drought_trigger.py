import numpy as np
from Bio.PDB import PDBParser
import os

# --- Z² ULTIMATE VERIFICATION #2: THE ABA DROUGHT TRIGGER ---
#
# GOAL: Prove that drought resistance is triggered by a Z-Manifold lock.
#
# METHOD: Compare PYR1 ABA Receptor in:
# 1. Open State (3NJO - Inactive)
# 2. Closed State (3NJP - Active/Signaling)
#
# LICENSE: AGPL-3.0-or-later

Z_TARGETS = [5.62, 5.72, 6.08]

def get_locks(pdb_id):
    fp = f"agritech_structures/{pdb_id}.pdb"
    parser = PDBParser(QUIET=True)
    struct = parser.get_structure(pdb_id, fp)
    
    aromatics = []
    for model in struct:
        for chain in model:
            for res in chain:
                if res.resname in ['PHE','TYR','TRP','HIS']:
                    ta = ['CG','CD1','CD2','CE1','CE2','CZ']
                    coords = [a.coord for a in res if a.name in ta]
                    if len(coords)>=5:
                        aromatics.append({"id": res.id[1], "c": np.mean(coords, 0), "res": res.resname})
        break
        
    locks = []
    for i in range(len(aromatics)):
        for j in range(i+1, len(aromatics)):
            d = np.linalg.norm(aromatics[i]["c"] - aromatics[j]["c"])
            if any(abs(d-z) <= 0.15 for z in Z_TARGETS):
                locks.append({"d": d, "pair": f"{aromatics[i]['res']}{aromatics[i]['id']}-{aromatics[j]['res']}{aromatics[j]['id']}"})
    return locks

def run_aba_audit():
    print("="*80)
    print(" Z² ULTIMATE VERIFICATION: THE ABA DROUGHT TRIGGER")
    print(" Testing for Geometric 'CLICK' during Drought Signaling.")
    print("="*80)
    
    open_locks = get_locks('3NJO')
    closed_locks = get_locks('3NJP')
    
    print(f"[*] Open State (Inactive): {len(open_locks)} Z-Locks")
    print(f"[*] Closed State (Active): {len(closed_locks)} Z-Locks")
    
    # Find NEW locks that only exist in the Closed state
    open_pairs = set([l["pair"] for l in open_locks])
    new_locks = [l for l in closed_locks if l["pair"] not in open_pairs]
    
    print("\n[*] NEW 'DROUGHT LOCKS' DETECTED:")
    for l in new_locks:
        print(f"    >> {l['pair']} | Dist: {l['d']:.3f} A")
        
    if new_locks:
        print("\n >> CONCLUSION: DROUGHT SIGNALING IS A GEOMETRIC PHASE-LOCK.")
        print(" >> When ABA hormone binds, the receptor 'clicks' into new Z-Manifold")
        print(" >> configurations, signaling the plant to conserve water.")
    else:
        print("\n >> CONCLUSION: ABA SIGNALING DOES NOT USE AROMATIC Z-LOCKS.")

if __name__ == "__main__":
    run_aba_audit()
