#!/usr/bin/env python3
"""
HCV NS3 Protease-Only Z² Analysis
=================================
Analyzes the protease domain specifically (1A1R - protease + NS4A cofactor)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict
import json

Z2_BIOLOGICAL_CONSTANT = 6.015152508891966
TOLERANCE_STRICT = 0.01
TOLERANCE_MODERATE = 0.10
TOLERANCE_LOOSE = 0.50

AROMATICS = {'PHE', 'TRP', 'TYR', 'HIS'}

RING_ATOMS = {
    'PHE': ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'TYR': ['CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'TRP': ['CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'],
    'HIS': ['CG', 'ND1', 'CD2', 'CE1', 'NE2'],
}

@dataclass
class Atom:
    name: str
    residue: str
    chain: str
    resnum: int
    x: float
    y: float
    z: float

    @property
    def coords(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

@dataclass
class AromaticResidue:
    resname: str
    chain: str
    resnum: int
    centroid: np.ndarray
    atoms: List[Atom]

    def __repr__(self):
        return f"{self.chain}:{self.resname}{self.resnum}"

def parse_pdb(pdb_path: str) -> List[Atom]:
    atoms = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                try:
                    atom_name = line[12:16].strip()
                    resname = line[17:20].strip()
                    chain = line[21].strip()
                    resnum = int(line[22:26].strip())
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    atoms.append(Atom(atom_name, resname, chain, resnum, x, y, z))
                except:
                    continue
    return atoms

def find_aromatics(atoms: List[Atom]) -> List[AromaticResidue]:
    aromatics = []
    residue_atoms = defaultdict(list)

    for atom in atoms:
        if atom.residue in AROMATICS:
            key = (atom.chain, atom.residue, atom.resnum)
            residue_atoms[key].append(atom)

    for (chain, resname, resnum), res_atoms in residue_atoms.items():
        ring_atom_names = RING_ATOMS.get(resname, [])
        ring_coords = [a.coords for a in res_atoms if a.name in ring_atom_names]
        if len(ring_coords) >= 4:
            centroid = np.mean(ring_coords, axis=0)
            aromatics.append(AromaticResidue(resname, chain, resnum, centroid, res_atoms))

    return aromatics

def analyze_binding_pocket(pdb_path: str):
    """Analyze the active site binding pocket specifically"""

    print("=" * 80)
    print("  HCV NS3 PROTEASE DOMAIN Z² BINDING POCKET ANALYSIS")
    print("=" * 80)
    print(f"\nPDB: {pdb_path}")
    print(f"Structure: NS3 Protease + NS4A cofactor")
    print(f"Z² constant: {Z2_BIOLOGICAL_CONSTANT:.6f} Å")

    atoms = parse_pdb(pdb_path)
    aromatics = find_aromatics(atoms)

    print(f"\nTotal atoms: {len(atoms)}")
    print(f"Aromatic residues: {len(aromatics)}")

    # Group by chain
    by_chain = defaultdict(list)
    for res in aromatics:
        by_chain[res.chain].append(res)

    print("\nAromatic inventory:")
    for chain in sorted(by_chain.keys()):
        print(f"\n  Chain {chain}:")
        for res in sorted(by_chain[chain], key=lambda r: r.resnum):
            print(f"    {res}")

    # Key active site residues in HCV NS3 protease
    # Catalytic triad: His57, Asp81, Ser139
    # S1 pocket: Phe154, Leu135
    # S2 pocket: His57, Arg155
    # S4 pocket: Phe43, Val55

    print("\n" + "-" * 60)
    print("ACTIVE SITE KEY RESIDUES")
    print("-" * 60)

    key_residues = {
        'HIS57': 'Catalytic (oxyanion hole)',
        'PHE43': 'S4 pocket',
        'TRP53': 'Near S4',
        'TYR56': 'Adjacent to catalytic',
        'PHE154': 'S1 pocket (primary specificity)'
    }

    active_aromatics = []
    for res in aromatics:
        key = f"{res.resname}{res.resnum}"
        if key in key_residues:
            print(f"  {res}: {key_residues[key]}")
            active_aromatics.append(res)

    # Calculate distances between active site aromatics
    print("\n" + "-" * 60)
    print("Z² DISTANCES IN ACTIVE SITE")
    print("-" * 60)

    pairs = []
    for i, res1 in enumerate(active_aromatics):
        for j, res2 in enumerate(active_aromatics):
            if i >= j:
                continue
            dist = np.linalg.norm(res1.centroid - res2.centroid)
            dev = dist - Z2_BIOLOGICAL_CONSTANT
            pairs.append((res1, res2, dist, dev))

    pairs.sort(key=lambda x: abs(x[3]))

    print(f"\n{'Pair':<30} {'Distance':>10} {'Δ from Z²':>12} {'Quality':<15}")
    print("-" * 70)

    for res1, res2, dist, dev in pairs:
        quality = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        print(f"{str(res1):<12} ↔ {str(res2):<12} {dist:>10.4f} {dev:>+12.4f} {quality:<15}")

    # Now calculate distances to all aromatics (for potential peptide docking)
    print("\n" + "-" * 60)
    print("DISTANCES FROM PHE154 (S1 POCKET) TO ALL AROMATICS")
    print("-" * 60)

    phe154 = None
    for res in aromatics:
        if res.resname == 'PHE' and res.resnum == 154:
            phe154 = res
            break

    if phe154:
        distances = []
        for res in aromatics:
            if res == phe154:
                continue
            dist = np.linalg.norm(phe154.centroid - res.centroid)
            dev = dist - Z2_BIOLOGICAL_CONSTANT
            distances.append((res, dist, dev))

        distances.sort(key=lambda x: abs(x[2]))

        print(f"\n{'Residue':<20} {'Distance':>10} {'Δ from Z²':>12} {'Quality':<15}")
        print("-" * 60)

        for res, dist, dev in distances[:15]:
            quality = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
            print(f"{str(res):<20} {dist:>10.4f} {dev:>+12.4f} {quality:<15}")

    # Calculate all aromatic pairs
    print("\n" + "-" * 60)
    print("ALL AROMATIC PAIRS - TOP 20 CLOSEST TO Z²")
    print("-" * 60)

    all_pairs = []
    for i, res1 in enumerate(aromatics):
        for j, res2 in enumerate(aromatics):
            if i >= j:
                continue
            dist = np.linalg.norm(res1.centroid - res2.centroid)
            dev = dist - Z2_BIOLOGICAL_CONSTANT
            all_pairs.append((res1, res2, dist, dev))

    all_pairs.sort(key=lambda x: abs(x[3]))

    z2_matches = sum(1 for _, _, _, d in all_pairs if abs(d) < 0.01)
    strong = sum(1 for _, _, _, d in all_pairs if abs(d) < 0.1)
    moderate = sum(1 for _, _, _, d in all_pairs if abs(d) < 0.5)

    print(f"\nTotal pairs: {len(all_pairs)}")
    print(f"Z² matches (±0.01 Å): {z2_matches}")
    print(f"Strong (±0.1 Å): {strong}")
    print(f"Moderate (±0.5 Å): {moderate}")

    print(f"\n{'Pair':<30} {'Distance':>10} {'Δ from Z² (mÅ)':>15} {'Quality':<15}")
    print("-" * 75)

    for res1, res2, dist, dev in all_pairs[:20]:
        quality = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        print(f"{str(res1):<12} ↔ {str(res2):<12} {dist:>10.4f} {dev*1000:>+15.2f} {quality:<15}")

    # Summary
    print("\n" + "=" * 80)
    print("  SUMMARY: HCV NS3 Z² SUITABILITY")
    print("=" * 80)

    best = all_pairs[0] if all_pairs else None

    if best:
        print(f"\nBest Z² match: {best[0]} ↔ {best[1]}")
        print(f"  Distance: {best[2]:.6f} Å")
        print(f"  Deviation: {best[3]*1000:+.2f} milliÅ")

        if abs(best[3]) < 0.01:
            print(f"\n  ✅ ATOMIC PRECISION MATCH FOUND")
            print(f"     HCV NS3 is a STRONG Z² candidate")
        elif abs(best[3]) < 0.1:
            print(f"\n  🟡 STRONG MATCH FOUND")
            print(f"     HCV NS3 is a GOOD Z² candidate")
        else:
            print(f"\n  ⚠️ Only moderate matches")
            print(f"     May need alternative design strategy")

    print("\n" + "=" * 80)

    return all_pairs

if __name__ == "__main__":
    analyze_binding_pocket("1A1R.pdb")
