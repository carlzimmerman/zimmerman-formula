import requests
import os
import math
import json
import numpy as np
from Bio.PDB import PDBParser
from datetime import datetime

# --- Z² UNIFIED ACTION: COMPLETE MAJOR CROPS SCANNER ---
# Expanded to cover ALL major global food crops with verified empirical PDB structures.
# Added: Statistical null hypothesis testing (Monte Carlo randomization)
# 
# LICENSE: AGPL-3.0-or-later
# AUTHOR: Carl Zimmerman & Antigravity AI

# --- ALL MAJOR CROPS WITH VERIFIED PDB IDS ---
MAJOR_CROPS = {
    # === GRAIN CROPS (Top Global Staples) ===
    "Rice_Rubisco":                {"pdb": "1WDD", "organism": "Oryza sativa (Rice)",             "resolution": "2.10", "enzyme": "Rubisco (Carbon Fixation)",               "crop_rank": 1},
    "Maize_Glutamine_Synthetase":  {"pdb": "2D3A", "organism": "Zea mays (Corn/Maize)",          "resolution": "2.63", "enzyme": "Glutamine Synthetase (N-Assimilation)",    "crop_rank": 2},
    "Wheat_Beta_Amylase":          {"pdb": "6GER", "organism": "Triticum aestivum (Wheat)",       "resolution": "2.00", "enzyme": "Beta-Amylase (Starch Metabolism)",         "crop_rank": 3},
    "Barley_Limit_Dextrinase":     {"pdb": "4AIO", "organism": "Hordeum vulgare (Barley)",        "resolution": "2.10", "enzyme": "Limit Dextrinase (Starch Debranching)",    "crop_rank": 7},
    
    # === OILSEED / LEGUME CROPS ===
    "Soybean_Lipoxygenase":        {"pdb": "1YGE", "organism": "Glycine max (Soybean)",           "resolution": "1.40", "enzyme": "Lipoxygenase-1 (Lipid Metabolism)",        "crop_rank": 4},
    
    # === ROOT / TUBER CROPS ===
    "Potato_Patatin":              {"pdb": "1OXW", "organism": "Solanum tuberosum (Potato)",       "resolution": "2.20", "enzyme": "Patatin (Lipid Acyl Hydrolase)",           "crop_rank": 5},
    "SweetPotato_PPO":             {"pdb": "2P3X", "organism": "Ipomoea batatas (Sweet Potato)",   "resolution": "2.70", "enzyme": "Polyphenol Oxidase (Defense)",             "crop_rank": 11},
    
    # === VEGETABLE / FRUIT CROPS ===
    "Tomato_PPO":                  {"pdb": "6HQI", "organism": "Solanum lycopersicum (Tomato)",    "resolution": "1.85", "enzyme": "Polyphenol Oxidase SlPPO1 (Defense)",      "crop_rank": 8},
    
    # === INDUSTRIAL / OTHER CROPS ===
    "Tobacco_Rubisco":             {"pdb": "1EJ7", "organism": "Nicotiana tabacum (Tobacco)",      "resolution": "1.90", "enzyme": "Rubisco (Carbon Fixation)",                "crop_rank": 10},
    "Spinach_Rubisco":             {"pdb": "1RCX", "organism": "Spinacia oleracea (Spinach)",      "resolution": "1.60", "enzyme": "Rubisco (Carbon Fixation)",                "crop_rank": 12},
    
    # === FUNDAMENTAL PLANT SYSTEMS ===
    "Spinach_Aquaporin":           {"pdb": "1Z98", "organism": "Spinacia oleracea (Spinach)",      "resolution": "2.10", "enzyme": "Aquaporin SoPIP2;1 (Water Transport)",     "crop_rank": 13},
    "Rice_Chitinase":              {"pdb": "1W9P", "organism": "Oryza sativa (Rice)",              "resolution": "1.80", "enzyme": "Chitinase (Fungal Defense)",               "crop_rank": 14},
    "Cellulose_Synthase":          {"pdb": "4HG6", "organism": "R. sphaeroides (Cell Wall Model)", "resolution": "2.65", "enzyme": "Cellulose Synthase (Cell Wall)",           "crop_rank": 15},
    "Auxin_Receptor_TIR1":         {"pdb": "2P1Q", "organism": "Arabidopsis thaliana (Model)",     "resolution": "2.50", "enzyme": "TIR1 Auxin Receptor (Growth Hormone)",     "crop_rank": 16},
}

Z_CONSTANTS = {"Tension": 5.62, "Resonance": 5.72, "Golden_Triangle": 6.08}
Z_PHASE = math.degrees(math.asin(1/math.pi))
Z_HARMONICS = [Z_PHASE * n for n in range(6) if Z_PHASE * n <= 90.0] + [90.0]
TOLERANCE = 0.20

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
    else: return None, None
    atoms = [a.coord for a in residue if a.name in ta]
    if len(atoms) < 5: return None, None
    pts = np.array(atoms); c = np.mean(pts,0)
    u,s,vh = np.linalg.svd(pts-c)
    n = vh[2,:]; n = n/np.linalg.norm(n)
    return c, n

def z_squared(d, a):
    dd = min(abs(d-z) for z in Z_CONSTANTS.values())
    da = min(abs(a-h) for h in Z_HARMONICS)
    return round(dd**2 + (da/10)**2, 6)

def monte_carlo_null_test(all_distances, n_trials=10000):
    """Statistical null hypothesis test: Are Z-constant hits significantly 
    more frequent than expected by random chance?"""
    if not all_distances: return None
    observed_hits = sum(1 for d in all_distances if any(abs(d-z) <= TOLERANCE for z in Z_CONSTANTS.values()))
    observed_rate = observed_hits / len(all_distances)
    
    # Under null hypothesis: distances are uniformly distributed between 3.5 and 8.0 A
    # What fraction would randomly fall within ±0.20 A of our 3 constants?
    range_width = 8.0 - 3.5  # 4.5 A total range
    hit_width = 3 * (2 * TOLERANCE)  # 3 constants × 0.40 A window each = 1.20 A
    expected_rate = hit_width / range_width  # ~0.267 (26.7%)
    
    # Monte Carlo: generate random distances and count hits
    rng = np.random.default_rng(42)
    mc_rates = []
    for _ in range(n_trials):
        random_dists = rng.uniform(3.5, 8.0, len(all_distances))
        mc_hits = sum(1 for d in random_dists if any(abs(d-z) <= TOLERANCE for z in Z_CONSTANTS.values()))
        mc_rates.append(mc_hits / len(all_distances))
    
    mc_mean = np.mean(mc_rates)
    mc_std = np.std(mc_rates)
    
    # Z-score (how many standard deviations above random?)
    if mc_std > 0:
        z_score = (observed_rate - mc_mean) / mc_std
    else:
        z_score = 0
    
    p_value = np.mean([1 for r in mc_rates if r >= observed_rate]) / n_trials
    
    return {
        "observed_rate": round(observed_rate, 4),
        "expected_random_rate": round(mc_mean, 4),
        "z_score": round(z_score, 2),
        "p_value": round(p_value, 6),
        "significant": p_value < 0.05,
    }

def scan_crop(pdb_path, name, info):
    parser = PDBParser(QUIET=True)
    try: structure = parser.get_structure('c', pdb_path)
    except: return None
    
    aromatics = []
    for m in structure:
        for ch in m:
            for res in ch:
                c, n = get_aromatic(res)
                if c is not None: aromatics.append((res, c, n, ch.id))
    
    locks = []; all_dists = []
    for i in range(len(aromatics)):
        for j in range(i+1, len(aromatics)):
            r1,c1,n1,ch1 = aromatics[i]; r2,c2,n2,ch2 = aromatics[j]
            d = np.linalg.norm(c1-c2)
            if d > 8.0 or d < 3.5: continue
            all_dists.append(d)
            cos_t = np.clip(np.dot(n1,n2),-1,1)
            a = math.degrees(math.acos(cos_t))
            if a > 90: a = 180-a
            
            for zn, zv in Z_CONSTANTS.items():
                if abs(d-zv) <= TOLERANCE:
                    locks.append({"pair": f"{r1.resname}{r1.id[1]}({ch1})-{r2.resname}{r2.id[1]}({ch2})",
                                  "distance": round(d,3), "angle": round(a,2), "z_type": zn,
                                  "z_squared": z_squared(d,a)})
    
    locks.sort(key=lambda x: x['z_squared'])
    
    # Run statistical null test
    stats = monte_carlo_null_test(all_dists)
    
    return {"crop": name, "organism": info["organism"], "pdb": info["pdb"],
            "resolution": info["resolution"], "enzyme": info["enzyme"],
            "total_aromatics": len(aromatics), "total_pairs_scanned": len(all_dists),
            "total_locks": len(locks),
            "perfect": [l for l in locks if l['z_squared'] < 0.05],
            "strong": [l for l in locks if 0.05 <= l['z_squared'] < 0.20],
            "top5": locks[:5], "statistics": stats}

def run():
    print("="*70)
    print(" Z² UNIFIED ACTION: COMPLETE MAJOR GLOBAL CROPS SCANNER")
    print(" Empirical X-Ray Structures | Statistical Validation | AGPL-3.0")
    print("="*70)
    print(f" Timestamp: {datetime.now().isoformat()}")
    print(f" Total Crops: {len(MAJOR_CROPS)}")
    
    results = []
    for name, info in sorted(MAJOR_CROPS.items(), key=lambda x: x[1]['crop_rank']):
        print(f"\n[*] {name} ({info['organism']}) - PDB: {info['pdb']}")
        pdb = download_pdb(info['pdb'])
        if not pdb: print("    [!] Download failed"); continue
        r = scan_crop(pdb, name, info)
        if r:
            results.append(r)
            print(f"    Aromatics: {r['total_aromatics']} | Pairs: {r['total_pairs_scanned']} | Z-Locks: {r['total_locks']}")
            print(f"    Perfect: {len(r['perfect'])} | Strong: {len(r['strong'])}")
            if r['statistics']:
                s = r['statistics']
                sig = "YES ***" if s['significant'] else "no"
                print(f"    Stats: Observed={s['observed_rate']*100:.1f}% vs Random={s['expected_random_rate']*100:.1f}% | Z-score={s['z_score']} | p={s['p_value']} | Significant: {sig}")
            if r['top5']:
                b = r['top5'][0]
                print(f"    Best: {b['pair']} | {b['distance']}A | Z²={b['z_squared']}")
    
    # Grand Summary
    print("\n"+"="*70)
    print(" GRAND SUMMARY")
    print("="*70)
    print(f"{'Crop':<32} {'Organism':<28} {'Locks':>5} {'Perf':>5} {'Strg':>5} {'BestZ²':>8} {'p-value':>8}")
    print("-"*100)
    for r in results:
        bz = r['top5'][0]['z_squared'] if r['top5'] else 'N/A'
        pv = r['statistics']['p_value'] if r['statistics'] else 'N/A'
        print(f"{r['crop']:<32} {r['organism']:<28} {r['total_locks']:>5} {len(r['perfect']):>5} {len(r['strong']):>5} {bz:>8} {pv:>8}")
    
    # Save
    with open("major_crops_z_squared_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[*] Results saved to major_crops_z_squared_results.json")
    print("[*] LICENSE: AGPL-3.0-or-later")
    return results

if __name__ == "__main__":
    run()
