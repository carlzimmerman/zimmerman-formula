#!/usr/bin/env python3
"""
α-Synuclein Fibril Z² Analysis
SPDX-License-Identifier: AGPL-3.0-or-later

Analyzes Parkinson's disease-associated α-Synuclein fibrils for Z² geometry.

α-Synuclein key features:
- 140 amino acids
- Intrinsically disordered as monomer
- Forms cross-β amyloid fibrils in disease
- Key aromatics: Tyr39, Phe94, Tyr125, Tyr133, Tyr136

Target: Block fibril propagation by disrupting Z² aromatic contacts.
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

def analyze_fibril(pdb_path, pdb_id):
    """Analyze α-Synuclein fibril structure"""

    print("\n" + "=" * 80)
    print(f"  α-SYNUCLEIN FIBRIL Z² ANALYSIS: {pdb_id}")
    print("  SPDX-License-Identifier: AGPL-3.0-or-later")
    print("=" * 80)

    atoms = parse_pdb(pdb_path)
    aromatics = find_aromatics(atoms)

    print(f"\nTotal atoms: {len(atoms)}")
    print(f"Aromatic residues: {len(aromatics)}")

    # Group by chain
    by_chain = defaultdict(list)
    for ar in aromatics:
        by_chain[ar['chain']].append(ar)

    print(f"\nChains: {sorted(by_chain.keys())} ({len(by_chain)} monomers in fibril)")

    # α-Synuclein aromatic positions
    print("\n" + "-" * 60)
    print("α-SYNUCLEIN AROMATIC RESIDUES")
    print("-" * 60)
    print("""
    Key aromatics in α-Synuclein sequence:
    - PHE4:   N-terminal amphipathic region
    - TYR39:  Repeat region, key for membrane binding
    - PHE94:  NAC region (aggregation core)
    - TYR125: C-terminal acidic region
    - TYR133: C-terminal acidic region
    - TYR136: C-terminal acidic region

    Fibril core: residues ~37-99 (varies by polymorph)
    """)

    # Show aromatics from chain A
    chain_a = by_chain.get('A', by_chain.get('E', []))  # Some structures use E as first
    if chain_a:
        print(f"\nAromatics in first monomer:")
        for ar in sorted(chain_a, key=lambda x: x['num']):
            print(f"  {ar['res']}{ar['num']}")

    # Calculate all aromatic pairs
    print("\n" + "-" * 60)
    print("Z² DISTANCE ANALYSIS - ALL AROMATIC PAIRS")
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

    # Inter-chain (fibril stacking) analysis
    print("\n" + "-" * 60)
    print("INTER-CHAIN AROMATIC CONTACTS (Fibril Stacking Interface)")
    print("-" * 60)

    inter_pairs = [(a1, a2, d, dev) for a1, a2, d, dev in pairs if a1['chain'] != a2['chain']]
    inter_pairs.sort(key=lambda x: abs(x[3]))

    z2_inter = sum(1 for _, _, _, d in inter_pairs if abs(d) < 0.01)
    strong_inter = sum(1 for _, _, _, d in inter_pairs if abs(d) < 0.1)

    print(f"\nInter-chain pairs: {len(inter_pairs)}")
    print(f"Z² matches: {z2_inter}")
    print(f"Strong: {strong_inter}")

    if inter_pairs:
        print(f"\n{'Pair':<35} {'Distance':>10} {'Δ Z² (mÅ)':>12} {'Quality':<15}")
        print("-" * 75)

        for a1, a2, d, dev in inter_pairs[:20]:
            q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate" if abs(dev) < 0.5 else "-"
            r1 = f"{a1['chain']}:{a1['res']}{a1['num']}"
            r2 = f"{a2['chain']}:{a2['res']}{a2['num']}"
            print(f"{r1:<15} ↔ {r2:<15} {d:>10.4f} {dev*1000:>+12.1f} {q:<15}")

    # Same-residue across chains (fibril axis contacts)
    print("\n" + "-" * 60)
    print("SAME-RESIDUE INTER-CHAIN CONTACTS (Fibril Axis)")
    print("-" * 60)

    # Group by residue number
    by_resnum = defaultdict(list)
    for ar in aromatics:
        by_resnum[ar['num']].append(ar)

    print("\nResidues with multiple copies across fibril:")
    axis_contacts = []
    for resnum, ars in sorted(by_resnum.items()):
        if len(ars) > 1:
            print(f"\n  {ars[0]['res']}{resnum}: {len(ars)} copies")
            # Calculate inter-chain distances for this residue
            for i, a1 in enumerate(ars):
                for j, a2 in enumerate(ars):
                    if i >= j: continue
                    d = np.linalg.norm(a1['centroid'] - a2['centroid'])
                    axis_contacts.append((a1, a2, d, d - Z2))
                    if d < 15:  # Close contacts only
                        dev = d - Z2
                        q = "Z²!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else ""
                        print(f"    {a1['chain']}-{a2['chain']}: {d:.3f} Å {q}")

    # Sort axis contacts
    axis_contacts.sort(key=lambda x: abs(x[3]))

    if axis_contacts:
        print("\nBest Z² matches along fibril axis:")
        for a1, a2, d, dev in axis_contacts[:10]:
            if abs(dev) < 0.5:
                q = "ATOMIC!" if abs(dev) < 0.01 else "Strong" if abs(dev) < 0.1 else "Moderate"
                print(f"  {a1['res']}{a1['num']} ({a1['chain']}-{a2['chain']}): {d:.4f} Å, Δ={dev*1000:+.1f} mÅ - {q}")

    # Summary
    print("\n" + "=" * 80)
    print(f"  α-SYNUCLEIN {pdb_id} Z² SUMMARY")
    print("=" * 80)

    if pairs:
        best = pairs[0]
        print(f"\nBest overall Z² match:")
        print(f"  {best[0]['chain']}:{best[0]['res']}{best[0]['num']} ↔ {best[1]['chain']}:{best[1]['res']}{best[1]['num']}")
        print(f"  Distance: {best[2]:.4f} Å")
        print(f"  Deviation: {best[3]*1000:+.1f} milliÅ")

    if inter_pairs:
        best_int = inter_pairs[0]
        print(f"\nBest inter-chain (fibril stacking) Z² match:")
        print(f"  {best_int[0]['chain']}:{best_int[0]['res']}{best_int[0]['num']} ↔ {best_int[1]['chain']}:{best_int[1]['res']}{best_int[1]['num']}")
        print(f"  Distance: {best_int[2]:.4f} Å")
        print(f"  Deviation: {best_int[3]*1000:+.1f} milliÅ")

    # Assessment
    print("\n" + "-" * 60)
    print("Z² FRAMEWORK ASSESSMENT")
    print("-" * 60)

    if z2_matches > 0:
        print("\n  ✅ ATOMIC PRECISION MATCHES FOUND")
        print("     α-Synuclein fibril is a STRONG Z² candidate")
    elif strong > 0:
        print("\n  🟡 STRONG MATCHES FOUND")
        print("     α-Synuclein fibril is a GOOD Z² candidate")
    elif moderate > 0:
        print("\n  ⚠️ MODERATE MATCHES FOUND")
        print("     May benefit from Z² approach")
    else:
        print("\n  ❌ NO CLOSE Z² MATCHES")
        print("     Alternative strategy recommended")

    return {
        'pdb': pdb_id,
        'total_aromatics': len(aromatics),
        'total_pairs': len(pairs),
        'z2_matches': z2_matches,
        'strong_matches': strong,
        'moderate_matches': moderate,
        'inter_chain_pairs': len(inter_pairs),
        'best_match': {
            'res1': f"{pairs[0][0]['chain']}:{pairs[0][0]['res']}{pairs[0][0]['num']}",
            'res2': f"{pairs[0][1]['chain']}:{pairs[0][1]['res']}{pairs[0][1]['num']}",
            'distance': float(pairs[0][2]),
            'deviation_mA': float(pairs[0][3] * 1000)
        } if pairs else None
    }


def main():
    print("=" * 80)
    print("  α-SYNUCLEIN FIBRIL Z² ANALYSIS FOR PARKINSON'S DISEASE")
    print("  SPDX-License-Identifier: AGPL-3.0-or-later")
    print("=" * 80)

    print("""
    DISEASE CONTEXT: Parkinson's Disease

    α-Synuclein aggregation is the hallmark of:
    - Parkinson's Disease (PD)
    - Dementia with Lewy Bodies (DLB)
    - Multiple System Atrophy (MSA)

    THERAPEUTIC STRATEGY:
    Design peptides that block fibril propagation by:
    1. Capping fibril ends (prevent elongation)
    2. Disrupting aromatic stacking (destabilize fibrils)
    3. Competing for Z² contacts (displace pathological interactions)
    """)

    results = {}

    # Analyze rod polymorph (6CU7)
    results['6CU7'] = analyze_fibril("6CU7.pdb", "6CU7 (Rod Polymorph)")

    # Analyze second structure (6H6B)
    results['6H6B'] = analyze_fibril("6H6B.pdb", "6H6B (Fibril)")

    # Comparison
    print("\n" + "=" * 80)
    print("  COMPARISON OF FIBRIL POLYMORPHS")
    print("=" * 80)

    print(f"\n{'Polymorph':<25} {'Z² Matches':>12} {'Strong':>10} {'Moderate':>10}")
    print("-" * 60)
    for pdb_id, r in results.items():
        print(f"{pdb_id:<25} {r['z2_matches']:>12} {r['strong_matches']:>10} {r['moderate_matches']:>10}")

    # Save combined results
    with open('alpha_synuclein_z2_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: alpha_synuclein_z2_analysis.json")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
