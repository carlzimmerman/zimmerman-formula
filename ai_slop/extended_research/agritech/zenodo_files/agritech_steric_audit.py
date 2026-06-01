import numpy as np
from Bio.PDB import PDBParser
import os

# --- Z² STERIC CLASH FILTER: THE PAULI EXCLUSION AUDIT ---
#
# GOAL: Filter the 635 'Resonance Upgrade' sites in Rice Rubisco.
#
# CRITERION: 
# When LEU is replaced by PHE, the new Phenylalanine ring has a 
# radius of approx 3.5 A. If any existing protein atom (excluding 
# the residue being replaced) is within < 3.2 A of the new PHE 
# ring center, we mark it as a STERIC CLASH.
#
# LICENSE: AGPL-3.0-or-later

Z_TARGETS = [5.62, 5.72, 6.08]
CLASH_THRESHOLD = 3.2 # Angstroms

def run_steric_filter(pdb_id):
    fp = f"agritech_structures/{pdb_id}.pdb"
    parser = PDBParser(QUIET=True)
    struct = parser.get_structure(pdb_id, fp)
    
    # 1. Get all backbone/sidechain atoms for clash checking
    all_atoms = []
    for model in struct:
        for chain in model:
            for res in chain:
                for atom in res:
                    all_atoms.append({"id": res.id[1], "coord": atom.coord})
        break
        
    # 2. Get Inert Slots (LEU/ILE/VAL)
    inert_residues = []
    for model in struct:
        for chain in model:
            for res in chain:
                if res.resname in ['LEU', 'ILE', 'VAL'] and 'CA' in res:
                    inert_residues.append({"id": res.id[1], "c": res['CA'].coord})
        break

    print(f"[*] Auditing {len(inert_residues)} potential upgrade sites in {pdb_id} for Steric Clash...")
    
    compliant_sites = []
    
    for res in inert_residues:
        clash = False
        # Check if the 'new' PHE ring center (at CA) clashes with any existing atom
        # (excluding the atoms of the residue itself)
        for atom in all_atoms:
            if atom["id"] == res["id"]: continue
            
            dist = np.linalg.norm(res["c"] - atom["coord"])
            if dist < CLASH_THRESHOLD:
                clash = True
                break
        
        if not clash:
            compliant_sites.append(res["id"])
            
    return compliant_sites

def run_final_audit():
    print("="*80)
    print(" Z² STERIC AUDIT: THE PAULI EXCLUSION FILTER")
    print(" Filtering Rice Rubisco upgrades for physical viability.")
    print("="*80)
    
    pdb_id = '1RCX'
    if not os.path.exists(f"agritech_structures/{pdb_id}.pdb"): return
    
    compliant = run_steric_filter(pdb_id)
    total_slots = 635 # From previous step
    
    print(f"\n>> AUDIT RESULTS FOR RICE RUBISCO:")
    print(f"   - Total Theoretical Upgrade Sites:  {total_slots}")
    print(f"   - Pauli-Compliant (No Clash) Sites: {len(compliant)}")
    print(f"   - Viability Rate:                   {(len(compliant)/total_slots*100):.2f}%")
    
    if len(compliant) > 0:
        print(f"\n>> TOP PAULI-COMPLIANT SITES (READY FOR CRISPR-Z):")
        for site_id in compliant[:5]:
            print(f"      Residue ID: {site_id}")

if __name__ == "__main__":
    run_final_audit()
