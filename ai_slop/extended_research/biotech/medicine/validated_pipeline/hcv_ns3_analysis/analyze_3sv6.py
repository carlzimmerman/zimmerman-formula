#!/usr/bin/env python3
"""Analyze Monomeric_Cleft_C NS3/4A with Telaprevir bound"""

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
    ligand_atoms = []
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
                try:
                    ligand_atoms.append({
                        'name': line[12:16].strip(),
                        'res': line[17:20].strip(),
                        'chain': line[21].strip(),
                        'resnum': int(line[22:26].strip()),
                        'coords': np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                    })
                except: pass
    return atoms, ligand_atoms

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

def main():
    print("=" * 80)
    print("  Monomeric_Cleft_C NS3/4A + TELAPREVIR Z² ANALYSIS")
    print("=" * 80)

    atoms, ligand_atoms = parse_pdb("3SV6.pdb")
    aromatics = find_aromatics(atoms)

    print(f"\nProtein atoms: {len(atoms)}")
    print(f"Ligand atoms: {len(ligand_atoms)}")
    print(f"Aromatic residues: {len(aromatics)}")

    # Find ligand info
    ligand_res = set((a['res'], a['resnum']) for a in ligand_atoms)
    print(f"\nLigand: {ligand_res}")

    # Calculate ligand center
    if ligand_atoms:
        lig_center = np.mean([a['coords'] for a in ligand_atoms], axis=0)
        print(f"Ligand center: {lig_center}")

        # Distances from ligand to aromatics
        print("\n" + "-" * 60)
        print("DISTANCES FROM TELAPREVIR TO AROMATICS")
        print("-" * 60)

        dists = []
        for ar in aromatics:
            d = np.linalg.norm(ar['centroid'] - lig_center)
            dists.append((ar, d, d - Z2))

        dists.sort(key=lambda x: x[1])

        print(f"\n{'Residue':<20} {'Distance':>10} {'Δ from Z²':>12}")
        print("-" * 45)
        for ar, d, dev in dists[:15]:
            print(f"{ar['chain']}:{ar['res']}{ar['num']:<10} {d:>10.3f} {dev:>+12.3f}")

    # All aromatic pairs
    print("\n" + "-" * 60)
    print("ALL AROMATIC PAIRS - TOP 15 CLOSEST TO Z²")
    print("-" * 60)

    pairs = []
    for i, a1 in enumerate(aromatics):
        for j, a2 in enumerate(aromatics):
            if i >= j: continue
            d = np.linalg.norm(a1['centroid'] - a2['centroid'])
            pairs.append((a1, a2, d, d - Z2))

    pairs.sort(key=lambda x: abs(x[3]))

    z2_matches = sum(1 for _, _, _, d in pairs if abs(d) < 0.01)
    strong = sum(1 for _, _, _, d in pairs if abs(d) < 0.1)

    print(f"\nTotal pairs: {len(pairs)}")
    print(f"Z² matches (±0.01 Å): {z2_matches}")
    print(f"Strong (±0.1 Å): {strong}")

    print(f"\n{'Pair':<30} {'Distance':>10} {'Δ Z² (mÅ)':>12} {'Quality':<15}")
    print("-" * 70)

    for a1, a2, d, dev in pairs[:15]:
        q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
        r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
        print(f"{r1:<12} ↔ {r2:<12} {d:>10.4f} {dev*1000:>+12.1f} {q:<15}")

    # Summary
    print("\n" + "=" * 80)
    print("  BINDING POCKET KEY FINDINGS")
    print("=" * 80)

    if pairs:
        best = pairs[0]
        print(f"\nBest Z² match: {best[0]['res']}{best[0]['num']} ↔ {best[1]['res']}{best[1]['num']}")
        print(f"  Distance: {best[2]:.4f} Å")
        print(f"  Deviation: {best[3]*1000:+.1f} milliÅ")

if __name__ == "__main__":
    main()
