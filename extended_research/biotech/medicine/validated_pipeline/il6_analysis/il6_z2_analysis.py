#!/usr/bin/env python3
"""
IL-6/IL-6R/gp130 Hexameric Complex Z² Analysis
SPDX-License-Identifier: AGPL-3.0-or-later

Analyzes the cytokine signaling complex for Z² aromatic geometry.
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
    return atoms

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
    print("  IL-6/IL-6R/gp130 HEXAMERIC COMPLEX Z² ANALYSIS")
    print("  SPDX-License-Identifier: AGPL-3.0-or-later")
    print("=" * 80)

    atoms = parse_pdb("1P9M.pdb")
    aromatics = find_aromatics(atoms)

    print(f"\nTotal atoms: {len(atoms)}")
    print(f"Aromatic residues: {len(aromatics)}")

    # Group by chain
    by_chain = defaultdict(list)
    for ar in aromatics:
        by_chain[ar['chain']].append(ar)

    chain_names = {
        'A': 'gp130 (signal transducer)',
        'B': 'IL-6 (cytokine)',
        'C': 'IL-6R alpha (receptor)'
    }

    print("\nAromatic inventory by chain:")
    for chain in sorted(by_chain.keys()):
        name = chain_names.get(chain, 'Unknown')
        print(f"\n  Chain {chain} - {name}: {len(by_chain[chain])} aromatics")
        for ar in sorted(by_chain[chain], key=lambda x: x['num'])[:10]:
            print(f"    {ar['res']}{ar['num']}")
        if len(by_chain[chain]) > 10:
            print(f"    ... and {len(by_chain[chain]) - 10} more")

    # Calculate all aromatic pairs
    print("\n" + "-" * 60)
    print("ALL AROMATIC PAIRS - TOP 25 CLOSEST TO Z²")
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
    moderate = sum(1 for _, _, _, d in pairs if abs(d) < 0.5)

    print(f"\nTotal pairs: {len(pairs)}")
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

    # Interface analysis
    print("\n" + "-" * 60)
    print("INTER-CHAIN AROMATIC PAIRS (Interface)")
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

    for a1, a2, d, dev in interface_pairs[:20]:
        q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
        r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
        print(f"{r1:<15} ↔ {r2:<15} {d:>10.4f} {dev*1000:>+12.1f} {q:<15}")

    # IL-6 to receptor interface specifically
    print("\n" + "-" * 60)
    print("IL-6 (Chain B) TO RECEPTOR INTERFACE")
    print("-" * 60)

    il6_interface = [(a1, a2, d, dev) for a1, a2, d, dev in pairs
                     if (a1['chain'] == 'B' and a2['chain'] != 'B') or
                        (a2['chain'] == 'B' and a1['chain'] != 'B')]
    il6_interface.sort(key=lambda x: abs(x[3]))

    print(f"\nIL-6 interface pairs: {len(il6_interface)}")

    print(f"\n{'Pair':<35} {'Distance':>10} {'Δ Z² (mÅ)':>12} {'Quality':<15}")
    print("-" * 75)

    for a1, a2, d, dev in il6_interface[:15]:
        q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
        r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
        r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
        print(f"{r1:<15} ↔ {r2:<15} {d:>10.4f} {dev*1000:>+12.1f} {q:<15}")

    # Summary
    print("\n" + "=" * 80)
    print("  IL-6 COMPLEX Z² SUMMARY")
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
    print("Z² FRAMEWORK ASSESSMENT FOR IL-6")
    print("-" * 60)

    if z2_matches > 0:
        print("\n  ✅ ATOMIC PRECISION MATCHES FOUND")
        print("     IL-6 complex is a STRONG Z² candidate")
    elif strong > 0:
        print("\n  🟡 STRONG MATCHES FOUND")
        print("     IL-6 complex is a GOOD Z² candidate")
    else:
        print("\n  ⚠️ Only moderate matches")
        print("     May need alternative approach")

    # Save results
    results = {
        'pdb': '1P9M',
        'complex': 'IL-6/IL-6R/gp130 hexamer',
        'z2_constant': Z2,
        'total_aromatics': len(aromatics),
        'total_pairs': len(pairs),
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

    with open('1P9M_z2_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: 1P9M_z2_analysis.json")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
