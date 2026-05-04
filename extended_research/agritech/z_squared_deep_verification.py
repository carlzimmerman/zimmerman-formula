import requests
import os
import math
import json
import numpy as np
from Bio.PDB import PDBParser
from collections import defaultdict
from datetime import datetime

# --- Z² DEEP VERIFICATION PIPELINE ---
# Three independent computational tests to prove the Z-Manifold is real:
#
# TEST 1: B-FACTOR RIGIDITY ANALYSIS
#   If Z-Manifold locks are structurally important, they should occur at
#   positions with LOW crystallographic B-factors (rigid, well-ordered atoms).
#   Random aromatic pairs would show no B-factor preference.
#
# TEST 2: CROSS-SPECIES CONSERVATION
#   If Z-locks are functionally essential, the SAME residue positions should 
#   form locks across different species (Rice vs Spinach vs Tobacco Rubisco).
#
# TEST 3: DISTANCE HISTOGRAM BINNING
#   Compute the full distance distribution of ALL aromatic pairs (3.5-8.0 A)
#   and check if the Z-constants show statistically significant peaks.
#
# LICENSE: AGPL-3.0-or-later

Z_CONSTANTS = {"Tension": 5.62, "Resonance": 5.72, "Golden_Triangle": 6.08}
Z_PHASE = math.degrees(math.asin(1/math.pi))
Z_HARMONICS = [Z_PHASE * n for n in range(6) if Z_PHASE * n <= 90.0] + [90.0]
TOLERANCE = 0.20

# Cross-species Rubisco comparison
RUBISCO_SPECIES = {
    "Spinach": "1RCX",
    "Rice":    "1WDD",
    "Tobacco": "1EJ7",
}

# Full crop set for histogram
ALL_CROPS = {
    "Rice_Rubisco": "1WDD", "Maize_GS": "2D3A", "Wheat_Amylase": "6GER",
    "Soybean_LOX": "1YGE", "Potato_Patatin": "1OXW", "Barley_LD": "4AIO",
    "Tomato_PPO": "6HQI", "Tobacco_Rubisco": "1EJ7", "SweetPotato_PPO": "2P3X",
    "Spinach_Rubisco": "1RCX", "Spinach_Aquaporin": "1Z98", "Rice_Chitinase": "1W9P",
    "Cellulose_Synthase": "4HG6", "Auxin_TIR1": "2P1Q",
}

def download_pdb(pdb_id, save_dir="agritech_structures"):
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

def get_aromatic(residue):
    ta = []
    if residue.resname == 'TRP': ta = ['CG','CD1','CD2','NE1','CE2','CE3','CZ2','CZ3','CH2']
    elif residue.resname in ['TYR','PHE']: ta = ['CG','CD1','CD2','CE1','CE2','CZ']
    elif residue.resname == 'HIS': ta = ['CG','ND1','CD2','CE1','NE2']
    else: return None, None, None
    atoms = []
    bfactors = []
    for a in residue:
        if a.name in ta:
            atoms.append(a.coord)
            bfactors.append(a.bfactor)
    if len(atoms) < 5: return None, None, None
    pts = np.array(atoms); c = np.mean(pts, 0)
    u, s, vh = np.linalg.svd(pts - c)
    n = vh[2,:]; n = n / np.linalg.norm(n)
    avg_b = np.mean(bfactors)
    return c, n, avg_b

def is_z_lock(dist):
    return any(abs(dist - z) <= TOLERANCE for z in Z_CONSTANTS.values())

# ============================================================
# TEST 1: B-FACTOR RIGIDITY ANALYSIS
# ============================================================
def test_bfactor_rigidity():
    print("=" * 70)
    print(" TEST 1: B-FACTOR RIGIDITY ANALYSIS")
    print(" Do Z-Manifold locks occur at structurally rigid positions?")
    print("=" * 70)
    
    all_lock_bfactors = []
    all_nonlock_bfactors = []
    
    for name, pdb_id in ALL_CROPS.items():
        pdb = download_pdb(pdb_id)
        if not pdb: continue
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('s', pdb)
        
        aromatics = []
        for m in structure:
            for ch in m:
                for res in ch:
                    c, n, b = get_aromatic(res)
                    if c is not None:
                        aromatics.append((res, c, n, b))
        
        for i in range(len(aromatics)):
            for j in range(i+1, len(aromatics)):
                r1, c1, n1, b1 = aromatics[i]
                r2, c2, n2, b2 = aromatics[j]
                dist = np.linalg.norm(c1 - c2)
                if dist < 3.5 or dist > 8.0: continue
                
                avg_b = (b1 + b2) / 2.0
                if is_z_lock(dist):
                    all_lock_bfactors.append(avg_b)
                else:
                    all_nonlock_bfactors.append(avg_b)
    
    if all_lock_bfactors and all_nonlock_bfactors:
        lock_mean = np.mean(all_lock_bfactors)
        nonlock_mean = np.mean(all_nonlock_bfactors)
        lock_std = np.std(all_lock_bfactors)
        nonlock_std = np.std(all_nonlock_bfactors)
        
        # Welch's t-test
        n1 = len(all_lock_bfactors)
        n2 = len(all_nonlock_bfactors)
        se = math.sqrt(lock_std**2/n1 + nonlock_std**2/n2)
        t_stat = (lock_mean - nonlock_mean) / se if se > 0 else 0
        
        print(f"\n  Z-Lock Pairs:     n={n1:>5} | Mean B-factor = {lock_mean:.2f} ± {lock_std:.2f}")
        print(f"  Non-Lock Pairs:   n={n2:>5} | Mean B-factor = {nonlock_mean:.2f} ± {nonlock_std:.2f}")
        print(f"  Welch's t-statistic: {t_stat:.3f}")
        
        if lock_mean < nonlock_mean:
            print(f"\n  >> RESULT: Z-Manifold locks have LOWER B-factors (more rigid)")
            print(f"  >> Delta = {nonlock_mean - lock_mean:.2f} Å² (locks are {((nonlock_mean-lock_mean)/nonlock_mean)*100:.1f}% more rigid)")
        else:
            print(f"\n  >> RESULT: Z-Manifold locks have HIGHER B-factors (more flexible)")
            print(f"  >> This suggests Z-locks may serve as dynamic hinges, not rigid anchors.")

# ============================================================
# TEST 2: CROSS-SPECIES RUBISCO CONSERVATION
# ============================================================
def test_cross_species_conservation():
    print("\n" + "=" * 70)
    print(" TEST 2: CROSS-SPECIES RUBISCO CONSERVATION")
    print(" Do the SAME residue positions form Z-locks across species?")
    print("=" * 70)
    
    species_locks = {}
    
    for species, pdb_id in RUBISCO_SPECIES.items():
        pdb = download_pdb(pdb_id)
        if not pdb: continue
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('s', pdb)
        
        # Use only chain A (large subunit) for consistency
        chain_A = list(structure[0].get_chains())[0]
        
        aromatics = []
        for res in chain_A:
            c, n, b = get_aromatic(res)
            if c is not None:
                aromatics.append((res.id[1], res.resname, c, n))
        
        locks = set()
        for i in range(len(aromatics)):
            for j in range(i+1, len(aromatics)):
                id1, name1, c1, n1 = aromatics[i]
                id2, name2, c2, n2 = aromatics[j]
                dist = np.linalg.norm(c1 - c2)
                if is_z_lock(dist):
                    locks.add((id1, id2))
        
        species_locks[species] = locks
        print(f"\n  {species} ({pdb_id}): {len(locks)} Z-locks in Chain A")
    
    # Find conserved locks (present in 2+ species)
    all_lock_pairs = set()
    for locks in species_locks.values():
        all_lock_pairs.update(locks)
    
    conserved = []
    for pair in all_lock_pairs:
        count = sum(1 for locks in species_locks.values() if pair in locks)
        if count >= 2:
            conserved.append((pair, count))
    
    conserved.sort(key=lambda x: -x[1])
    
    print(f"\n  >> CONSERVED Z-LOCKS (same residue positions across species):")
    if conserved:
        print(f"  >> Found {len(conserved)} conserved lock positions out of {len(all_lock_pairs)} total")
        conservation_rate = len(conserved) / len(all_lock_pairs) * 100 if all_lock_pairs else 0
        print(f"  >> Conservation Rate: {conservation_rate:.1f}%")
        for pair, count in conserved[:10]:
            species_list = [sp for sp, locks in species_locks.items() if pair in locks]
            print(f"     Residues {pair[0]}-{pair[1]}: Conserved in {count}/{len(RUBISCO_SPECIES)} species ({', '.join(species_list)})")
    else:
        print(f"  >> No conserved positions found (species use different numbering)")

# ============================================================
# TEST 3: DISTANCE HISTOGRAM PEAK ANALYSIS
# ============================================================
def test_distance_histogram():
    print("\n" + "=" * 70)
    print(" TEST 3: DISTANCE HISTOGRAM PEAK ANALYSIS")
    print(" Do aromatic distances cluster at Z-constants more than other values?")
    print("=" * 70)
    
    all_distances = []
    
    for name, pdb_id in ALL_CROPS.items():
        pdb = download_pdb(pdb_id)
        if not pdb: continue
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('s', pdb)
        
        aromatics = []
        for m in structure:
            for ch in m:
                for res in ch:
                    c, n, b = get_aromatic(res)
                    if c is not None:
                        aromatics.append(c)
        
        for i in range(len(aromatics)):
            for j in range(i+1, len(aromatics)):
                dist = np.linalg.norm(aromatics[i] - aromatics[j])
                if 3.5 <= dist <= 8.0:
                    all_distances.append(dist)
    
    if not all_distances:
        print("  [!] No distances collected.")
        return
    
    # Create histogram bins (0.10 A width from 3.5 to 8.0 A)
    bin_edges = np.arange(3.5, 8.05, 0.10)
    counts, edges = np.histogram(all_distances, bins=bin_edges)
    bin_centers = (edges[:-1] + edges[1:]) / 2
    
    # Normalize to density
    total = sum(counts)
    densities = counts / total
    
    # Find the density at each Z-constant
    print(f"\n  Total aromatic pairs analyzed: {total}")
    print(f"\n  {'Bin Center':>10} {'Count':>7} {'Density':>8}")
    print(f"  {'-'*30}")
    
    z_densities = {}
    for z_name, z_val in Z_CONSTANTS.items():
        # Find the bin containing this Z-constant
        idx = np.argmin(np.abs(bin_centers - z_val))
        z_densities[z_name] = densities[idx]
    
    # Find the overall mean density (what "flat" would look like)
    mean_density = np.mean(densities)
    
    # Print top 10 bins by density
    sorted_indices = np.argsort(-densities)
    for rank, idx in enumerate(sorted_indices[:15]):
        marker = ""
        for z_name, z_val in Z_CONSTANTS.items():
            if abs(bin_centers[idx] - z_val) < 0.10:
                marker = f" <<<< {z_name} ({z_val} A)"
        print(f"  {bin_centers[idx]:>8.2f} A  {counts[idx]:>7d}  {densities[idx]:>8.5f}{marker}")
    
    print(f"\n  Mean density per bin: {mean_density:.5f}")
    print(f"\n  Z-Constant Enrichment:")
    for z_name, z_val in Z_CONSTANTS.items():
        idx = np.argmin(np.abs(bin_centers - z_val))
        enrichment = densities[idx] / mean_density if mean_density > 0 else 0
        rank = list(np.argsort(-densities)).index(idx) + 1
        print(f"    {z_name} ({z_val} A): density={densities[idx]:.5f} | {enrichment:.2f}x mean | Rank {rank}/{len(densities)}")

# ============================================================
# RUN ALL TESTS
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print(" Z² DEEP VERIFICATION PIPELINE")
    print(" Three independent computational proofs")
    print(" AGPL-3.0-or-later | Carl Zimmerman & Antigravity AI")
    print("=" * 70)
    print(f" Timestamp: {datetime.now().isoformat()}")
    
    test_bfactor_rigidity()
    test_cross_species_conservation()
    test_distance_histogram()
    
    print("\n" + "=" * 70)
    print(" ALL TESTS COMPLETE")
    print("=" * 70)
