#!/usr/bin/env python3
"""
Z² Complete Validation - All Claimed Targets
SPDX-License-Identifier: AGPL-3.0-or-later

Honest analysis of ALL 5 originally claimed Z² targets with proper PDB paths.
"""

import numpy as np
from collections import defaultdict
import json
import os

Z2 = 6.015152508891966  # Angstroms
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

def analyze_z2(aromatics, name):
    if not aromatics:
        return None

    pairs = []
    for i, a1 in enumerate(aromatics):
        for j, a2 in enumerate(aromatics):
            if i >= j: continue
            d = np.linalg.norm(a1['centroid'] - a2['centroid'])
            pairs.append((a1, a2, d, d - Z2))

    if not pairs:
        return None

    pairs.sort(key=lambda x: abs(x[3]))

    atomic = sum(1 for _, _, _, d in pairs if abs(d) < 0.01)
    strong = sum(1 for _, _, _, d in pairs if abs(d) < 0.1)
    moderate = sum(1 for _, _, _, d in pairs if abs(d) < 0.5)

    best = pairs[0]
    return {
        'name': name,
        'total_aromatics': len(aromatics),
        'total_pairs': len(pairs),
        'atomic': atomic,
        'strong': strong,
        'moderate': moderate,
        'best_pair': f"{best[0]['chain']}:{best[0]['res']}{best[0]['num']} - {best[1]['chain']}:{best[1]['res']}{best[1]['num']}",
        'best_distance': best[2],
        'best_deviation_mA': best[3] * 1000,
    }

def main():
    print("=" * 80)
    print("  Z² COMPLETE VALIDATION - ALL 5 CLAIMED TARGETS")
    print("  Z² = 6.015152508891966 Å")
    print("=" * 80)

    # Define ALL claimed targets with correct paths
    base = "/Users/carlzimmerman/new_physics/zimmerman-formula"
    pipeline = f"{base}/extended_research/biotech/medicine/validated_pipeline"
    validation = f"{base}/extended_research/biotech/validation/simulations"

    targets = {
        'TNF-α (C3 trimer)': f"{validation}/1TNF.pdb",
        'Influenza NA (C4 tetramer)': f"{pipeline}/influenza_na_analysis/2HU4.pdb",
        'HIV Protease (C2 dimer)': f"{pipeline}/hiv_protease_analysis/1HHP.pdb",
        'SARS-CoV-2 Mpro (C2 dimer)': f"{pipeline}/sars_cov2_mpro_analysis/6LU7.pdb",
        'HCV NS3 (monomeric)': f"{pipeline}/hcv_ns3_analysis/1A1R.pdb",
    }

    results = []

    for name, pdb_path in targets.items():
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"  PDB: {os.path.basename(pdb_path)}")
        print(f"{'='*60}")

        if not os.path.exists(pdb_path):
            print(f"  ❌ PDB file not found: {pdb_path}")
            continue

        atoms = parse_pdb(pdb_path)
        aromatics = find_aromatics(atoms)

        print(f"  Atoms: {len(atoms)}, Aromatics: {len(aromatics)}")

        result = analyze_z2(aromatics, name)
        if result:
            results.append(result)

            # Determine validation status
            if result['atomic'] > 0:
                status = "✅ ATOMIC PRECISION"
            elif result['strong'] > 0:
                status = "🟡 STRONG"
            elif result['moderate'] > 0:
                status = "⚠️  MODERATE"
            else:
                status = "❌ NOT VALIDATED"

            print(f"\n  Best Z² match: {result['best_pair']}")
            print(f"  Distance: {result['best_distance']:.4f} Å")
            print(f"  Deviation from Z²: {result['best_deviation_mA']:+.1f} mÅ")
            print(f"\n  Atomic (±10 mÅ): {result['atomic']}")
            print(f"  Strong (±100 mÅ): {result['strong']}")
            print(f"  Moderate (±500 mÅ): {result['moderate']}")
            print(f"\n  Status: {status}")

    # Summary
    print("\n" + "=" * 80)
    print("  HONEST VALIDATION SUMMARY")
    print("=" * 80)

    print(f"\n{'Target':<35} {'Best Pair':<25} {'Deviation':>12} {'Status':<20}")
    print("-" * 95)

    validated = 0
    for r in sorted(results, key=lambda x: abs(x['best_deviation_mA'])):
        if abs(r['best_deviation_mA']) < 10:
            status = "✅ ATOMIC"
            validated += 1
        elif abs(r['best_deviation_mA']) < 100:
            status = "🟡 STRONG"
        elif abs(r['best_deviation_mA']) < 500:
            status = "⚠️  MODERATE"
        else:
            status = "❌ NOT VALIDATED"

        print(f"{r['name']:<35} {r['best_pair']:<25} {r['best_deviation_mA']:>+10.1f} mÅ {status:<20}")

    print("-" * 95)
    print(f"\n  VALIDATED AT ATOMIC PRECISION: {validated} / {len(results)}")

    # Final honest assessment
    print("\n" + "=" * 80)
    print("  HONEST ASSESSMENT")
    print("=" * 80)

    atomic_targets = [r for r in results if abs(r['best_deviation_mA']) < 10]
    not_validated = [r for r in results if abs(r['best_deviation_mA']) >= 100]

    print(f"""
WHAT IS VALIDATED:
  - {len(atomic_targets)} target(s) show atomic precision Z² aromatic geometry
  - These have aromatic pairs at 6.015 ± 0.010 Å
""")

    for r in atomic_targets:
        print(f"    • {r['name']}: {r['best_pair']} ({r['best_deviation_mA']:+.1f} mÅ)")

    if not_validated:
        print(f"""
WHAT IS NOT VALIDATED:
  - {len(not_validated)} target(s) do NOT show Z² aromatic geometry
  - Previous claims about these targets were incorrect
""")
        for r in not_validated:
            print(f"    • {r['name']}: {r['best_pair']} ({r['best_deviation_mA']:+.1f} mÅ)")

    print("""
METHODOLOGY NOTE:
  - This measures distance between aromatic ring centroids
  - Z² = 6.015 Å is the target distance
  - Atomic precision: ±10 mÅ (0.01 Å)
  - This is a LOCAL geometric property, not a global structural claim
""")

    # Save results
    output = {
        'z2_constant': Z2,
        'results': results,
        'validated_count': validated,
        'total_count': len(results),
    }
    with open('z2_complete_validation_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to: z2_complete_validation_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
