#!/usr/bin/env python3
"""
Z² Aromatic Network Analysis Across Validated Targets
SPDX-License-Identifier: AGPL-3.0-or-later

Compares aromatic contact geometry across all validated Z² targets:
- HIV Protease (1HHP)
- HCV NS3 (1A1R)
- Influenza NA (2HU4)
- TNF-α (1TNF)
- SARS-CoV-2 Mpro (6LU7)
"""

import numpy as np
from collections import defaultdict
import json
import os

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
    if not os.path.exists(path):
        return atoms
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

def analyze_z2_network(aromatics, name):
    """Analyze Z² contact network for a single target"""

    pairs = []
    for i, a1 in enumerate(aromatics):
        for j, a2 in enumerate(aromatics):
            if i >= j: continue
            d = np.linalg.norm(a1['centroid'] - a2['centroid'])
            pairs.append((a1, a2, d, d - Z2))

    pairs.sort(key=lambda x: abs(x[3]))

    # Count matches at different thresholds
    z2_atomic = sum(1 for _, _, _, d in pairs if abs(d) < 0.01)
    z2_strong = sum(1 for _, _, _, d in pairs if abs(d) < 0.1)
    z2_moderate = sum(1 for _, _, _, d in pairs if abs(d) < 0.5)

    # Build contact network (edges where distance is near Z²)
    network = []
    for a1, a2, d, dev in pairs:
        if abs(dev) < 0.5:  # Moderate threshold
            network.append({
                'node1': f"{a1['chain']}:{a1['res']}{a1['num']}",
                'node2': f"{a2['chain']}:{a2['res']}{a2['num']}",
                'distance': d,
                'deviation': dev * 1000,  # mÅ
                'quality': 'atomic' if abs(dev) < 0.01 else 'strong' if abs(dev) < 0.1 else 'moderate'
            })

    # Find most connected nodes (Z² hubs)
    connections = defaultdict(int)
    for edge in network:
        connections[edge['node1']] += 1
        connections[edge['node2']] += 1

    hubs = sorted(connections.items(), key=lambda x: -x[1])[:5]

    return {
        'name': name,
        'total_aromatics': len(aromatics),
        'total_pairs': len(pairs),
        'z2_atomic': z2_atomic,
        'z2_strong': z2_strong,
        'z2_moderate': z2_moderate,
        'best_match': {
            'pair': f"{pairs[0][0]['res']}{pairs[0][0]['num']}-{pairs[0][1]['res']}{pairs[0][1]['num']}",
            'distance': pairs[0][2],
            'deviation_mA': pairs[0][3] * 1000
        } if pairs else None,
        'z2_hubs': hubs,
        'network_edges': len(network)
    }

def main():
    print("=" * 80)
    print("  Z² AROMATIC NETWORK ANALYSIS - VALIDATED TARGETS")
    print("  SPDX-License-Identifier: AGPL-3.0-or-later")
    print("=" * 80)

    # Define targets and their PDB paths
    targets = {
        'HIV_Protease': 'hiv_protease_analysis/1HHP.pdb',
        'HCV_NS3': 'hcv_ns3_analysis/1A1R.pdb',
        'Influenza_NA': 'influenza_na_analysis/2HU4.pdb',
        'SARS_CoV2_Mpro': 'sars_cov2_mpro_analysis/6LU7.pdb',
    }

    results = {}

    for name, pdb_path in targets.items():
        print(f"\n{'='*60}")
        print(f"  Analyzing: {name}")
        print(f"{'='*60}")

        atoms = parse_pdb(pdb_path)
        if not atoms:
            print(f"  Could not load {pdb_path}")
            continue

        aromatics = find_aromatics(atoms)
        print(f"  Atoms: {len(atoms)}, Aromatics: {len(aromatics)}")

        result = analyze_z2_network(aromatics, name)
        results[name] = result

        print(f"\n  Z² Contact Statistics:")
        print(f"    Atomic precision (±10 mÅ): {result['z2_atomic']}")
        print(f"    Strong (±100 mÅ):          {result['z2_strong']}")
        print(f"    Moderate (±500 mÅ):        {result['z2_moderate']}")

        if result['best_match']:
            print(f"\n  Best Z² Match:")
            print(f"    {result['best_match']['pair']}")
            print(f"    Distance: {result['best_match']['distance']:.4f} Å")
            print(f"    Deviation: {result['best_match']['deviation_mA']:+.1f} mÅ")

        if result['z2_hubs']:
            print(f"\n  Z² Network Hubs (most connected):")
            for hub, count in result['z2_hubs']:
                print(f"    {hub}: {count} Z² contacts")

    # Comparison
    print("\n" + "=" * 80)
    print("  CROSS-TARGET COMPARISON")
    print("=" * 80)

    print(f"\n{'Target':<20} {'Aromatics':>10} {'Atomic':>8} {'Strong':>8} {'Moderate':>10} {'Best (mÅ)':>12}")
    print("-" * 72)

    for name, r in results.items():
        best = r['best_match']['deviation_mA'] if r['best_match'] else 'N/A'
        if isinstance(best, float):
            best_str = f"{best:+.1f}"
        else:
            best_str = best
        print(f"{name:<20} {r['total_aromatics']:>10} {r['z2_atomic']:>8} {r['z2_strong']:>8} {r['z2_moderate']:>10} {best_str:>12}")

    # Aromatic type distribution
    print("\n" + "-" * 60)
    print("  AROMATIC RESIDUE TYPE DISTRIBUTION")
    print("-" * 60)

    for name, pdb_path in targets.items():
        atoms = parse_pdb(pdb_path)
        aromatics = find_aromatics(atoms)

        type_counts = defaultdict(int)
        for ar in aromatics:
            type_counts[ar['res']] += 1

        print(f"\n  {name}:")
        for res_type, count in sorted(type_counts.items()):
            print(f"    {res_type}: {count}")

    # Save results
    with open('z2_network_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n\nResults saved to: z2_network_analysis_results.json")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
