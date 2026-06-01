#!/usr/bin/env python3
"""
C4_Tetramer_D N1 C4_Tetramer_D Z² Analysis
SPDX-License-Identifier: AGPL-3.0-or-later

Analyzes the C4 tetrameric C4_Tetramer_D + Oseltamivir complex.
"""

import numpy as np
from collections import defaultdict
import json

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
                resname = line[17:20].strip()
                if resname not in ['HOH', 'SO4', 'GOL']:  # Skip solvent
                    try:
                        ligand_atoms.append({
                            'name': line[12:16].strip(),
                            'res': resname,
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
    print("  C4_Tetramer_D N1 C4_Tetramer_D Z² ANALYSIS")
    print("  H5N1 Avian C4_Tetramer_D + Oseltamivir (Tamiflu)")
    print("  SPDX-License-Identifier: AGPL-3.0-or-later")
    print("=" * 80)

    atoms, ligand_atoms = parse_pdb("2HU4.pdb")
    aromatics = find_aromatics(atoms)

    print(f"\nTotal protein atoms: {len(atoms)}")
    print(f"Ligand atoms: {len(ligand_atoms)}")
    print(f"Aromatic residues: {len(aromatics)}")

    # Identify ligand
    ligand_types = set(a['res'] for a in ligand_atoms)
    print(f"Ligand types: {ligand_types}")

    # Group by chain
    by_chain = defaultdict(list)
    for ar in aromatics:
        by_chain[ar['chain']].append(ar)

    print(f"\nChains: {sorted(by_chain.keys())}")
    print(f"Symmetry: C4 tetramer (4-fold axis)")

    # Take first monomer (chain A) for detailed analysis
    chain_a = by_chain.get('A', [])
    print(f"\nChain A aromatics: {len(chain_a)}")
    for ar in sorted(chain_a, key=lambda x: x['num']):
        print(f"  {ar['res']}{ar['num']}")

    # Key active site residues in C4_Tetramer_D
    # Catalytic residues: Arg118, Asp151, Arg152, Arg224, Glu276, Arg292, Arg371
    # Aromatic framework: Tyr406, Trp178, Tyr347
    print("\n" + "-" * 60)
    print("C4_Tetramer_D ACTIVE SITE CONTEXT")
    print("-" * 60)
    print("""
    Sialic acid binding pocket:
    - TYR406: Forms hydrophobic cage around substrate
    - TRP178: Part of 150-loop, aromatic stacking
    - TYR347: Secondary aromatic contact
    - PHE294: Near active site

    Oseltamivir binds in the same pocket as sialic acid.
    """)

    # Calculate all aromatic pairs within single tetramer (chains A-D)
    print("\n" + "-" * 60)
    print("Z² ANALYSIS - SINGLE TETRAMER (Chains A-D)")
    print("-" * 60)

    tetramer_aromatics = [ar for ar in aromatics if ar['chain'] in ['A', 'B', 'C', 'D']]

    pairs = []
    for i, a1 in enumerate(tetramer_aromatics):
        for j, a2 in enumerate(tetramer_aromatics):
            if i >= j: continue
            d = np.linalg.norm(a1['centroid'] - a2['centroid'])
            pairs.append((a1, a2, d, d - Z2))

    pairs.sort(key=lambda x: abs(x[3]))

    z2_matches = sum(1 for _, _, _, d in pairs if abs(d) < 0.01)
    strong = sum(1 for _, _, _, d in pairs if abs(d) < 0.1)
    moderate = sum(1 for _, _, _, d in pairs if abs(d) < 0.5)

    print(f"\nTotal pairs (tetramer): {len(pairs)}")
    print(f"Z² matches (±0.01 Å): {z2_matches}")
    print(f"Strong (±0.1 Å): {strong}")
    print(f"Moderate (±0.5 Å): {moderate}")

    print(f"\n{'Pair':<35} {'Distance':>10} {'Δ Z² (mÅ)':>12} {'Quality':<15}")
    print("-" * 75)

    for a1, a2, d, dev in pairs[:25]:
        q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
        r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
        print(f"{r1:<15} ↔ {r2:<15} {d:>10.4f} {dev*1000:>+12.1f} {q:<15}")

    # Inter-subunit interface
    print("\n" + "-" * 60)
    print("INTER-SUBUNIT INTERFACE (C4 symmetry axis)")
    print("-" * 60)

    interface_pairs = [(a1, a2, d, dev) for a1, a2, d, dev in pairs if a1['chain'] != a2['chain']]
    interface_pairs.sort(key=lambda x: abs(x[3]))

    z2_interface = sum(1 for _, _, _, d in interface_pairs if abs(d) < 0.01)
    strong_interface = sum(1 for _, _, _, d in interface_pairs if abs(d) < 0.1)

    print(f"\nInterface pairs: {len(interface_pairs)}")
    print(f"Z² matches: {z2_interface}")
    print(f"Strong: {strong_interface}")

    print(f"\n{'Pair':<35} {'Distance':>10} {'Δ Z² (mÅ)':>12} {'Quality':<15}")
    print("-" * 75)

    for a1, a2, d, dev in interface_pairs[:15]:
        q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
        r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
        print(f"{r1:<15} ↔ {r2:<15} {d:>10.4f} {dev*1000:>+12.1f} {q:<15}")

    # Ligand proximity analysis
    if ligand_atoms:
        print("\n" + "-" * 60)
        print("OSELTAMIVIR BINDING POCKET ANALYSIS")
        print("-" * 60)

        # Get oseltamivir atoms (OTV or similar)
        oseltamivir = [a for a in ligand_atoms if a['res'] in ['OTV', 'OSE', 'G39', 'ZMR']]
        if not oseltamivir:
            # Try any non-water ligand
            oseltamivir = ligand_atoms

        if oseltamivir:
            lig_center = np.mean([a['coords'] for a in oseltamivir], axis=0)
            print(f"\nLigand center: {lig_center}")

            # Distances from ligand to aromatics
            lig_dists = []
            for ar in chain_a:  # Just chain A
                d = np.linalg.norm(ar['centroid'] - lig_center)
                lig_dists.append((ar, d, d - Z2))

            lig_dists.sort(key=lambda x: x[1])

            print(f"\n{'Residue':<15} {'Distance to Drug':>15} {'Δ from Z²':>12}")
            print("-" * 45)
            for ar, d, dev in lig_dists[:10]:
                print(f"{ar['chain']}:{ar['res']}{ar['num']:<8} {d:>15.3f} {dev:>+12.3f}")

    # Summary
    print("\n" + "=" * 80)
    print("  C4_Tetramer_D NA Z² SUMMARY")
    print("=" * 80)

    if pairs:
        best = pairs[0]
        print(f"\nBest overall Z² match:")
        print(f"  {best[0]['chain']}:{best[0]['res']}{best[0]['num']} ↔ {best[1]['chain']}:{best[1]['res']}{best[1]['num']}")
        print(f"  Distance: {best[2]:.4f} Å")
        print(f"  Deviation: {best[3]*1000:+.1f} milliÅ")

    if interface_pairs:
        best_int = interface_pairs[0]
        print(f"\nBest interface Z² match:")
        print(f"  {best_int[0]['chain']}:{best_int[0]['res']}{best_int[0]['num']} ↔ {best_int[1]['chain']}:{best_int[1]['res']}{best_int[1]['num']}")
        print(f"  Distance: {best_int[2]:.4f} Å")
        print(f"  Deviation: {best_int[3]*1000:+.1f} milliÅ")

    # Assessment
    print("\n" + "-" * 60)
    print("Z² FRAMEWORK ASSESSMENT FOR C4_Tetramer_D NA")
    print("-" * 60)

    if z2_matches > 0:
        print("\n  ✅ ATOMIC PRECISION MATCHES FOUND")
        print("     C4_Tetramer_D NA is a STRONG Z² candidate")
    elif strong > 0:
        print("\n  🟡 STRONG MATCHES FOUND")
        print("     C4_Tetramer_D NA is a GOOD Z² candidate")
    elif moderate > 0:
        print("\n  ⚠️ MODERATE MATCHES FOUND")
        print("     May benefit from Z² approach with optimization")
    else:
        print("\n  ❌ NO CLOSE Z² MATCHES")
        print("     Alternative design strategy recommended")

    # Save
    results = {
        'pdb': '2HU4',
        'target': 'H5N1 C4_Tetramer_D C4_Tetramer_D + Oseltamivir',
        'symmetry': 'C4 tetramer',
        'z2_constant': Z2,
        'total_aromatics': len(aromatics),
        'tetramer_pairs': len(pairs),
        'z2_matches': z2_matches,
        'strong_matches': strong,
        'moderate_matches': moderate,
        'best_match': {
            'res1': f"{pairs[0][0]['chain']}:{pairs[0][0]['res']}{pairs[0][0]['num']}",
            'res2': f"{pairs[0][1]['chain']}:{pairs[0][1]['res']}{pairs[0][1]['num']}",
            'distance': float(pairs[0][2]),
            'deviation_mA': float(pairs[0][3] * 1000)
        } if pairs else None
    }

    with open('2HU4_z2_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: 2HU4_z2_analysis.json")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
