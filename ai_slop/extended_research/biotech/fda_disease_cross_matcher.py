import requests
import json
import math
import numpy as np
import time
from rdkit import Chem
from rdkit.Chem import AllChem

# --- TARGET PATHOGEN POCKETS (Z-Manifold Geometry) ---
DISEASE_POCKETS = {
    "COVID-19 (Spike S2 Fusion)": {"target_dist": 5.62, "type": "Mechanical Lock"},
    "COPD (Neutrophil Elastase)": {"target_dist": 5.63, "type": "Mechanical Lock"},
    "Alzheimer's (BACE1)": {"target_dist": 6.08, "type": "Golden Triangle"},
    "Stroke (Thrombin)": {"target_dist": 5.71, "type": "Resonance Lock"},
    "Heart Disease (HMG-CoA)": {"target_dist": 5.72, "type": "Resonance Lock"}
}
TOLERANCE = 0.15 # Angstrom tolerance for physical binding dynamics

def get_fda_approved_smiles(limit=3000):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule?max_phase=4&format=json&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        drugs = []
        for mol in data.get('molecules', []):
            struct = mol.get('molecule_structures')
            if struct and struct.get('canonical_smiles'):
                drugs.append({
                    'chembl_id': mol['molecule_chembl_id'],
                    'pref_name': mol.get('pref_name', 'Unknown'),
                    'smiles': struct['canonical_smiles']
                })
        return drugs
    return []

def calculate_ring_centroid_and_normal(mol, conf, ring_indices):
    points = np.array([list(conf.GetAtomPosition(idx)) for idx in ring_indices])
    centroid = np.mean(points, axis=0)
    
    centered = points - centroid
    u, s, vh = np.linalg.svd(centered)
    normal = vh[2, :]
    normal = normal / np.linalg.norm(normal)
    return centroid, normal

def check_disease_locks(drugs):
    cross_matches = {disease: [] for disease in DISEASE_POCKETS}
    
    for i, drug in enumerate(drugs):
        try:
            mol = Chem.MolFromSmiles(drug['smiles'])
            if not mol: continue
            
            ring_info = mol.GetRingInfo()
            aromatic_rings = []
            for ring in ring_info.AtomRings():
                if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
                    aromatic_rings.append(ring)
            
            if len(aromatic_rings) < 2: continue
            
            mol = Chem.AddHs(mol)
            if AllChem.EmbedMolecule(mol, randomSeed=42) != 0: continue
            AllChem.MMFFOptimizeMolecule(mol)
            
            conf = mol.GetConformer()
            
            # Recalculate aromatic rings on 3D mol
            aromatic_rings = []
            for ring in mol.GetRingInfo().AtomRings():
                if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
                    aromatic_rings.append(ring)
            
            matched = False
            for j in range(len(aromatic_rings)):
                if matched: break
                for k in range(j + 1, len(aromatic_rings)):
                    ring1 = aromatic_rings[j]
                    ring2 = aromatic_rings[k]
                    
                    c1, n1 = calculate_ring_centroid_and_normal(mol, conf, ring1)
                    c2, n2 = calculate_ring_centroid_and_normal(mol, conf, ring2)
                    
                    dist = np.linalg.norm(c1 - c2)
                    cos_theta = np.clip(np.dot(n1, n2), -1.0, 1.0)
                    angle_deg = math.degrees(math.acos(cos_theta))
                    if angle_deg > 90: angle_deg = 180 - angle_deg
                    
                    # Must be Phase-Locked (~18.5 deg, bounded 10-27)
                    if 10.0 <= angle_deg <= 27.0:
                        # Check against disease pockets
                        for disease, params in DISEASE_POCKETS.items():
                            if abs(dist - params["target_dist"]) <= TOLERANCE:
                                cross_matches[disease].append({
                                    'drug_name': drug['pref_name'],
                                    'chembl_id': drug['chembl_id'],
                                    'distance': round(dist, 3),
                                    'angle': round(angle_deg, 3),
                                    'delta_from_ideal': round(abs(dist - params["target_dist"]), 3)
                                })
                                matched = True
                                break
                    if matched: break
        except Exception as e:
            continue
            
    return cross_matches

if __name__ == "__main__":
    print("[*] Fetching up to 3000 FDA approved drugs from ChEMBL...")
    drugs = get_fda_approved_smiles(limit=3000)
    print(f"[*] Fetched {len(drugs)} drugs.")
    
    print("[*] Performing Ultrathink Cross-Matching across Disease Pockets...")
    start_time = time.time()
    matches = check_disease_locks(drugs)
    end_time = time.time()
    
    with open('disease_cross_matches.json', 'w') as f:
        json.dump(matches, f, indent=2)
        
    print(f"[*] Cross-matching complete in {round(end_time - start_time, 2)} seconds.")
    for disease, hits in matches.items():
        print(f"\n>> {disease} ({DISEASE_POCKETS[disease]['target_dist']} A) -> {len(hits)} Candidates Found")
        # Sort by closest to ideal distance
        hits.sort(key=lambda x: x['delta_from_ideal'])
        for hit in hits[:3]: # Print top 3 best fits
            print(f"   - {hit['drug_name']} [{hit['distance']} A, {hit['angle']} deg] (Delta: {hit['delta_from_ideal']} A)")
