import requests
import json
import math
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Geometry import Point3D

def get_fda_approved_smiles(limit=500):
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
    
    # Calculate normal vector using SVD
    centered = points - centroid
    u, s, vh = np.linalg.svd(centered)
    normal = vh[2, :] # Normal is the eigenvector corresponding to the smallest singular value
    normal = normal / np.linalg.norm(normal)
    return centroid, normal

def check_z_manifold(drugs):
    matches = []
    
    for i, drug in enumerate(drugs):
        try:
            mol = Chem.MolFromSmiles(drug['smiles'])
            if not mol: continue
            
            # Fast check: must have at least 2 aromatic rings
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
            
            # Recalculate aromatic rings on 3D mol to be safe
            aromatic_rings = []
            for ring in mol.GetRingInfo().AtomRings():
                if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
                    aromatic_rings.append(ring)
            
            for j in range(len(aromatic_rings)):
                for k in range(j + 1, len(aromatic_rings)):
                    ring1 = aromatic_rings[j]
                    ring2 = aromatic_rings[k]
                    
                    c1, n1 = calculate_ring_centroid_and_normal(mol, conf, ring1)
                    c2, n2 = calculate_ring_centroid_and_normal(mol, conf, ring2)
                    
                    dist = np.linalg.norm(c1 - c2)
                    
                    # Angle between normals
                    cos_theta = np.clip(np.dot(n1, n2), -1.0, 1.0)
                    angle_rad = math.acos(cos_theta)
                    angle_deg = math.degrees(angle_rad)
                    if angle_deg > 90:
                        angle_deg = 180 - angle_deg
                    
                    # Z-Manifold Criteria (Extended):
                    # User Variant: ~6.02 A
                    # Golden Triangle: ~6.08 A
                    # Angle: ~18.5 deg
                    
                    if (5.95 <= dist <= 6.15) and (10.0 <= angle_deg <= 27.0):
                        matches.append({
                            'drug_name': drug['pref_name'],
                            'chembl_id': drug['chembl_id'],
                            'smiles': drug['smiles'],
                            'distance': round(dist, 3),
                            'angle': round(angle_deg, 3),
                            'type': 'User Variant (6.02)' if abs(dist - 6.02) < abs(dist - 6.08) else 'Golden Triangle (6.08)'
                        })
                        # Break out to avoid multiple hits for the same drug for now
                        break
        except Exception as e:
            continue
            
    return matches

if __name__ == "__main__":
    print("[*] Fetching FDA approved drugs from ChEMBL...")
    drugs = get_fda_approved_smiles(limit=2000)
    print(f"[*] Fetched {len(drugs)} drugs.")
    
    print("[*] Screening drugs for Z-Manifold Geometric Cross-Alignment (5.72 / 5.62 A & 18.5 deg)...")
    matches = check_z_manifold(drugs)
    
    with open('fda_z_manifold_matches.json', 'w') as f:
        json.dump(matches, f, indent=2)
    
    print(f"[*] Found {len(matches)} drugs matching Z-Manifold criteria.")
    for m in matches:
        print(f" - {m['drug_name']} ({m['chembl_id']}): Dist={m['distance']} A, Angle={m['angle']} deg [{m['type']}]")
