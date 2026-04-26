import os
import numpy as np
from Bio.PDB import PDBParser
import json

Z2_AROMATIC_CONSTANT = 6.015152508891966
TOLERANCE = 0.010 # 10 milliangstroms

def get_aromatic_centroid(residue):
    """Calculate the centroid of the aromatic ring for PHE, TYR, or TRP."""
    atoms = []
    if residue.get_resname() == 'PHE':
        atoms = ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ']
    elif residue.get_resname() == 'TYR':
        atoms = ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ']
    elif residue.get_resname() == 'TRP':
        # TRP has two rings, but the 6-member ring is often the stacker
        atoms = ['CD2', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2']
    
    coords = []
    for atom_name in atoms:
        if atom_name in residue:
            coords.append(residue[atom_name].get_coord())
    
    if len(coords) == 0:
        return None
    return np.mean(coords, axis=0)

def analyze_pdb(pdb_path):
    parser = PDBParser(QUIET=True)
    try:
        structure = parser.get_structure('protein', pdb_path)
    except:
        return []

    aromatics = []
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.get_resname() in ['PHE', 'TYR', 'TRP']:
                    centroid = get_aromatic_centroid(residue)
                    if centroid is not None:
                        aromatics.append({
                            'id': f"{chain.id}:{residue.get_resname()}{residue.id[1]}",
                            'centroid': centroid,
                            'resname': residue.get_resname()
                        })

    matches = []
    for i in range(len(aromatics)):
        for j in range(i + 1, len(aromatics)):
            dist = np.linalg.norm(aromatics[i]['centroid'] - aromatics[j]['centroid'])
            deviation = dist - Z2_AROMATIC_CONSTANT
            if abs(deviation) <= TOLERANCE:
                matches.append({
                    'pair': f"{aromatics[i]['id']} <-> {aromatics[j]['id']}",
                    'distance': float(dist),
                    'deviation_ma': float(deviation * 1000)
                })
    return matches

def main():
    cache_dir = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/validation/pdb_cache/'
    pdbs = [f for f in os.listdir(cache_dir) if f.endswith('.pdb')]
    
    results = {}
    print(f"Analyzing {len(pdbs)} structures for Z2 atomic precision...")
    
    for pdb in pdbs:
        path = os.path.join(cache_dir, pdb)
        matches = analyze_pdb(path)
        if matches:
            results[pdb] = matches
            print(f"Found {len(matches)} atomic matches in {pdb}")

    # Rank by number of matches and precision
    with open('ultrathink_z2_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Summary
    summary = []
    for pdb, matches in results.items():
        best_dev = min(abs(m['deviation_ma']) for m in matches)
        summary.append({
            'pdb': pdb,
            'match_count': len(matches),
            'best_deviation_ma': best_dev
        })
    
    summary.sort(key=lambda x: (x['match_count'], -x['best_deviation_ma']), reverse=True)
    
    print("\n--- TOP ULTRATHINK Z2 CANDIDATES ---")
    for s in summary[:10]:
        print(f"PDB: {s['pdb']} | Matches: {s['match_count']} | Best Dev: {s['best_deviation_ma']:.2f} mÅ")

if __name__ == "__main__":
    main()
