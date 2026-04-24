#!/usr/bin/env python3
"""
Z² Binding Pocket Geometry Analysis
SPDX-License-Identifier: AGPL-3.0-or-later

Analyzes the geometry around Z² hotspot residues.
"""

import numpy as np
from collections import defaultdict
import json

Z2 = 6.015152508891966

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

def get_residue_center(atoms, chain, resnum):
    """Get center of mass for a residue"""
    res_atoms = [a for a in atoms if a['chain'] == chain and a['resnum'] == resnum]
    if not res_atoms:
        return None
    coords = np.array([a['coords'] for a in res_atoms])
    return np.mean(coords, axis=0)

def count_atoms_in_sphere(atoms, center, radius):
    """Count atoms within radius of center"""
    count = 0
    for a in atoms:
        d = np.linalg.norm(a['coords'] - center)
        if d <= radius:
            count += 1
    return count

def analyze_pocket(atoms, center, label):
    """Analyze pocket around a center point"""

    # Count atoms at various radii
    radii = [4.0, 5.0, Z2, 7.0, 8.0, 10.0]
    counts = {}
    for r in radii:
        counts[r] = count_atoms_in_sphere(atoms, center, r)

    # Estimate pocket volume (very rough)
    # Using Z² sphere
    z2_count = counts[Z2]
    z2_volume = (4/3) * np.pi * (Z2 ** 3)  # Å³

    # Density
    z2_density = z2_count / z2_volume if z2_volume > 0 else 0

    return {
        'label': label,
        'center': center.tolist(),
        'atom_counts': {str(r): c for r, c in counts.items()},
        'z2_sphere_atoms': z2_count,
        'z2_sphere_volume': z2_volume,
        'z2_density': z2_density
    }

def main():
    print("=" * 70)
    print("  Z² BINDING POCKET GEOMETRY ANALYSIS")
    print("  SPDX-License-Identifier: AGPL-3.0-or-later")
    print("=" * 70)

    # Define hotspots for each target
    hotspots = {
        'HCV_NS3': {
            'pdb': 'hcv_ns3_analysis/1A1R.pdb',
            'residues': [('A', 79, 'TRP79'), ('A', 101, 'TYR101')]
        },
        'Influenza_NA': {
            'pdb': 'influenza_na_analysis/2HU4.pdb',
            'residues': [('A', 374, 'PHE374'), ('A', 422, 'PHE422')]
        },
        'HIV_Protease': {
            'pdb': 'hiv_protease_analysis/1HSG.pdb',
            'residues': [('A', 53, 'PHE53'), ('B', 53, 'PHE53')]
        },
        'SARS_CoV2': {
            'pdb': 'sars_cov2_mpro_analysis/6LU7.pdb',
            'residues': [('A', 140, 'PHE140'), ('A', 66, 'PHE66')]
        }
    }

    results = {}

    for target, info in hotspots.items():
        print(f"\n{'='*60}")
        print(f"  {target}")
        print(f"{'='*60}")

        atoms = parse_pdb(info['pdb'])
        if not atoms:
            print(f"  Could not load {info['pdb']}")
            continue

        print(f"  Total atoms: {len(atoms)}")

        target_results = []

        for chain, resnum, label in info['residues']:
            center = get_residue_center(atoms, chain, resnum)
            if center is None:
                print(f"  {label}: not found")
                continue

            pocket = analyze_pocket(atoms, center, label)
            target_results.append(pocket)

            print(f"\n  {label} ({chain}:{resnum}):")
            print(f"    Center: ({center[0]:.1f}, {center[1]:.1f}, {center[2]:.1f})")
            print(f"    Atoms within Z² sphere ({Z2:.2f} Å): {pocket['z2_sphere_atoms']}")
            print(f"    Z² sphere volume: {pocket['z2_sphere_volume']:.1f} Å³")
            print(f"    Atom density: {pocket['z2_density']:.4f} atoms/Å³")

            print(f"    Atom counts by radius:")
            for r_str, count in sorted(pocket['atom_counts'].items(), key=lambda x: float(x[0])):
                print(f"      {float(r_str):.1f} Å: {count} atoms")

        results[target] = target_results

    # Summary comparison
    print("\n" + "=" * 70)
    print("  POCKET DENSITY COMPARISON")
    print("=" * 70)

    print(f"\n{'Target':<20} {'Hotspot':<15} {'Z² Atoms':>10} {'Density':>12}")
    print("-" * 60)

    for target, pockets in results.items():
        for p in pockets:
            print(f"{target:<20} {p['label']:<15} {p['z2_sphere_atoms']:>10} {p['z2_density']:>12.4f}")

    # Save results
    with open('z2_pocket_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\nResults saved to: z2_pocket_analysis_results.json")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
