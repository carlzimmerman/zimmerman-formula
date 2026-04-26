#!/usr/bin/env python3
"""Quick C2_Homodimer_A protease analysis with inhibitor"""
import numpy as np
from collections import defaultdict

Z2 = 6.015152508891966
AROMATICS = {'PHE', 'TRP', 'TYR', 'HIS'}
RING_ATOMS = {
    'PHE': ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'TYR': ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'TRP': ['CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'],
    'HIS': ['CG', 'ND1', 'CD2', 'CE1', 'NE2'],
}

def parse_pdb(path):
    atoms = []
    ligand = []
    with open(path) as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    atoms.append({
                        'name': line[12:16].strip(),
                        'res': line[17:20].strip(),
                        'chain': line[21].strip(),
                        'resnum': int(line[22:26].strip()),
                        'coords': np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                    })
                except: pass
            elif line.startswith('HETATM'):
                resname = line[17:20].strip()
                if resname not in ['HOH']:
                    try:
                        ligand.append({
                            'name': line[12:16].strip(),
                            'res': resname,
                            'coords': np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                        })
                    except: pass
    return atoms, ligand

def find_aromatics(atoms):
    residues = defaultdict(list)
    for a in atoms:
        if a['res'] in AROMATICS:
            key = (a['chain'], a['res'], a['resnum'])
            residues[key].append(a)
    
    aromatics = []
    for (chain, res, num), atoms_list in residues.items():
        ring_names = RING_ATOMS.get(res, [])
        ring_coords = [a['coords'] for a in atoms_list if a['name'] in ring_names]
        if len(ring_coords) >= 4:
            centroid = np.mean(ring_coords, axis=0)
            aromatics.append({'chain': chain, 'res': res, 'num': num, 'centroid': centroid})
    return aromatics

atoms, ligand = parse_pdb("hiv_protease_analysis/1HSG.pdb")
aromatics = find_aromatics(atoms)

print("=" * 60)
print("  C2_Homodimer_A PROTEASE (1HSG) Z² ANALYSIS")
print("=" * 60)
print(f"\nAtoms: {len(atoms)}, Ligand atoms: {len(ligand)}")
print(f"Aromatic residues: {len(aromatics)}")

print("\nAromatic inventory:")
for ar in sorted(aromatics, key=lambda x: (x['chain'], x['num'])):
    print(f"  {ar['chain']}:{ar['res']}{ar['num']}")

# All pairs
pairs = []
for i, a1 in enumerate(aromatics):
    for j, a2 in enumerate(aromatics):
        if i >= j: continue
        d = np.linalg.norm(a1['centroid'] - a2['centroid'])
        pairs.append((a1, a2, d, d - Z2))

pairs.sort(key=lambda x: abs(x[3]))

print("\nTop 15 closest to Z²:")
print(f"{'Pair':<25} {'Distance':>10} {'Δ Z² (mÅ)':>12}")
print("-" * 50)
for a1, a2, d, dev in pairs[:15]:
    r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
    r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
    print(f"{r1:<10} ↔ {r2:<10} {d:>10.4f} {dev*1000:>+12.1f}")

# Inter-chain (dimer interface)
print("\n" + "-" * 60)
print("INTER-CHAIN (Dimer Interface):")
inter = [(a1, a2, d, dev) for a1, a2, d, dev in pairs if a1['chain'] != a2['chain']]
inter.sort(key=lambda x: abs(x[3]))

for a1, a2, d, dev in inter[:10]:
    r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
    r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
    q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Mod" if abs(dev) < 0.5 else ""
    print(f"{r1:<10} ↔ {r2:<10} {d:>10.4f} {dev*1000:>+12.1f} {q}")

# Ligand proximity
if ligand:
    lig_center = np.mean([a['coords'] for a in ligand], axis=0)
    print(f"\n" + "-" * 60)
    print(f"LIGAND PROXIMITY (center at {lig_center}):")
    for ar in aromatics:
        d_lig = np.linalg.norm(ar['centroid'] - lig_center)
        dev = d_lig - Z2
        if d_lig < 15:
            print(f"  {ar['chain']}:{ar['res']}{ar['num']}: {d_lig:.3f} Å (Δ Z² = {dev*1000:+.1f} mÅ)")
