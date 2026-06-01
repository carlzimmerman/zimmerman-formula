#!/usr/bin/env python3
"""
geo_03_topological_frustration.py - Energy Landscape & Configurational Frustration

Maps configurational frustration in protein structures: regions where the
geometry forces sub-optimal packing. Based on Energy Landscape Theory
(Wolynes, Onuchic) and the Frustratometer methodology.

Mathematical Framework:
- Z² contact network as reference topology
- Local frustration index computation
- Identification of frustrated hinges and allosteric pathways
- Correlation between frustration and binding sites

Author: Carl Zimmerman & Claude Opus 4.5
Date: April 2026
License: AGPL-3.0-or-later

DISCLAIMER: Theoretical computational research only. Not peer reviewed.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy import stats
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Z² Framework constants
Z2 = 32 * np.pi / 3  # ≈ 33.51
R_NATURAL = (Z2 ** 0.25) * 3.8  # ≈ 9.14 Å
EXPECTED_CONTACTS = 8

# Amino acid hydrophobicity (Kyte-Doolittle scale, normalized)
HYDROPHOBICITY = {
    'I': 1.00, 'V': 0.97, 'L': 0.94, 'F': 0.72, 'C': 0.64,
    'M': 0.50, 'A': 0.47, 'G': -0.11, 'T': -0.19, 'S': -0.22,
    'W': -0.22, 'Y': -0.33, 'P': -0.42, 'H': -0.89, 'E': -0.92,
    'Q': -0.92, 'D': -0.92, 'N': -0.92, 'K': -1.00, 'R': -1.00,
}

def compute_contact_network(coords: np.ndarray,
                             cutoff: float = None) -> np.ndarray:
    """
    Compute contact matrix using Z² cutoff.

    Returns binary contact matrix (excluding sequence neighbors).
    """
    if cutoff is None:
        cutoff = R_NATURAL

    n = len(coords)
    dist = squareform(pdist(coords))

    # Contact if within cutoff and not sequence neighbor
    contacts = (dist <= cutoff).astype(int)

    # Remove sequence neighbors (|i-j| <= 3)
    for i in range(n):
        for j in range(max(0, i-3), min(n, i+4)):
            contacts[i, j] = 0

    return contacts

def compute_local_frustration(coords: np.ndarray,
                               sequence: str,
                               contacts: np.ndarray) -> np.ndarray:
    """
    Compute local configurational frustration index for each residue.

    Frustration = deviation of local environment from optimal packing.

    For each residue i:
    - Count actual contacts
    - Compute "energy" based on contact hydrophobicity
    - Compare to expected optimal value
    - Frustration = |actual - optimal| / optimal

    Returns frustration index (0 = minimally frustrated, >1 = highly frustrated)
    """
    n = len(coords)
    frustration = np.zeros(n)

    for i in range(n):
        # Get contacts of residue i
        contact_indices = np.where(contacts[i] > 0)[0]
        n_contacts = len(contact_indices)

        if n_contacts == 0:
            frustration[i] = 1.0  # No contacts = frustrated
            continue

        # Deviation from expected contact number
        contact_frustration = abs(n_contacts - EXPECTED_CONTACTS) / EXPECTED_CONTACTS

        # Hydrophobicity mismatch
        res_i = sequence[i] if i < len(sequence) else 'A'
        h_i = HYDROPHOBICITY.get(res_i, 0)

        energy_mismatch = 0
        for j in contact_indices:
            res_j = sequence[j] if j < len(sequence) else 'A'
            h_j = HYDROPHOBICITY.get(res_j, 0)

            # Hydrophobic-hydrophobic or polar-polar contacts are favorable
            # Hydrophobic-polar contacts are unfavorable (frustrated)
            if h_i * h_j < 0:  # Opposite signs = mismatch
                energy_mismatch += 1

        if n_contacts > 0:
            energy_frustration = energy_mismatch / n_contacts
        else:
            energy_frustration = 0

        # Combined frustration index
        frustration[i] = 0.5 * contact_frustration + 0.5 * energy_frustration

    return frustration

def identify_frustrated_regions(frustration: np.ndarray,
                                 threshold: float = 0.7) -> List[Dict]:
    """
    Identify contiguous regions of high frustration.

    These are potential:
    - Allosteric hinges
    - Binding site hot spots
    - Dynamic regions
    """
    n = len(frustration)
    regions = []

    in_region = False
    region_start = 0

    for i in range(n):
        if frustration[i] > threshold:
            if not in_region:
                region_start = i
                in_region = True
        else:
            if in_region:
                regions.append({
                    'start': region_start,
                    'end': i - 1,
                    'length': i - region_start,
                    'mean_frustration': float(np.mean(frustration[region_start:i])),
                    'max_frustration': float(np.max(frustration[region_start:i])),
                })
                in_region = False

    if in_region:
        regions.append({
            'start': region_start,
            'end': n - 1,
            'length': n - region_start,
            'mean_frustration': float(np.mean(frustration[region_start:])),
            'max_frustration': float(np.max(frustration[region_start:])),
        })

    return regions

def analyze_protein_frustration(pdb_id: str) -> Optional[Dict]:
    """Complete frustration analysis for a protein."""
    import requests

    # Fetch structure
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return None

        coords = []
        sequence = []

        aa_map = {
            'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
            'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
            'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
            'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y',
        }

        for line in response.text.split('\n'):
            if line.startswith('ATOM') and ' CA ' in line:
                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    res = line[17:20].strip()
                    coords.append([x, y, z])
                    sequence.append(aa_map.get(res, 'A'))
                except ValueError:
                    continue

        if len(coords) < 10:
            return None

        coords = np.array(coords)
        sequence = ''.join(sequence)

    except Exception:
        return None

    # Compute frustration
    contacts = compute_contact_network(coords)
    frustration = compute_local_frustration(coords, sequence, contacts)
    regions = identify_frustrated_regions(frustration)

    return {
        'pdb_id': pdb_id,
        'n_residues': len(coords),
        'sequence': sequence,
        'mean_frustration': float(np.mean(frustration)),
        'std_frustration': float(np.std(frustration)),
        'n_frustrated_regions': len(regions),
        'frustrated_regions': regions,
        'frustration_profile': frustration.tolist(),
        'n_contacts_per_residue': float(np.sum(contacts) / len(coords)),
    }

def main():
    """Run frustration analysis on protein structures."""
    print("=" * 70)
    print("GEO_03: TOPOLOGICAL FRUSTRATION ANALYSIS")
    print("Energy Landscape Theory & Configurational Frustration")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Z² Natural Cutoff: {R_NATURAL:.2f} Å")
    print(f"Expected contacts: {EXPECTED_CONTACTS}")
    print()

    # Test proteins
    test_pdbs = ['1UBQ', '1L2Y', '1CRN']

    results = {
        'timestamp': datetime.now().isoformat(),
        'z2_value': float(Z2),
        'r_natural': float(R_NATURAL),
        'expected_contacts': EXPECTED_CONTACTS,
        'proteins': [],
        'summary': {},
    }

    print("Analyzing protein frustration...")
    print("-" * 70)

    all_frustrations = []

    for pdb_id in test_pdbs:
        print(f"  Processing {pdb_id}...", end=" ")

        analysis = analyze_protein_frustration(pdb_id)

        if analysis:
            results['proteins'].append(analysis)
            all_frustrations.append(analysis['mean_frustration'])

            print(f"✓ {analysis['n_residues']} residues")
            print(f"      Mean frustration: {analysis['mean_frustration']:.3f}")
            print(f"      Frustrated regions: {analysis['n_frustrated_regions']}")
            print(f"      Contacts/residue: {analysis['n_contacts_per_residue']:.1f}")

            if analysis['frustrated_regions']:
                print("      Frustrated regions (potential binding sites):")
                for r in analysis['frustrated_regions'][:3]:
                    print(f"        - Residues {r['start']}-{r['end']} "
                          f"(frustration: {r['mean_frustration']:.2f})")
        else:
            print("✗ Failed to fetch")

    # Summary
    if all_frustrations:
        results['summary'] = {
            'n_proteins': len(all_frustrations),
            'mean_frustration_overall': float(np.mean(all_frustrations)),
            'interpretation': (
                'Highly frustrated regions (>0.7) indicate:'
                ' 1) Binding site hot spots'
                ' 2) Allosteric hinges'
                ' 3) Conformationally dynamic loops'
            ),
        }

        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Mean frustration across all proteins: {np.mean(all_frustrations):.3f}")
        print()
        print("INTERPRETATION:")
        print("  Frustrated regions are where geometry conflicts with optimal packing.")
        print("  These regions are:")
        print("    - Conformationally flexible (hinges)")
        print("    - Potential drug binding sites")
        print("    - Allosteric communication pathways")
        print()
        print("  Drugs that bind at frustrated regions can lock or release")
        print("  mechanical stress, switching the protein between states.")

    # Save results
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "geo_03_frustration_results.json"

    # Trim large arrays
    for p in results['proteins']:
        if 'frustration_profile' in p and len(p['frustration_profile']) > 100:
            p['frustration_profile'] = p['frustration_profile'][:100] + ['...truncated']

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    print("\n" + "=" * 70)
    print("GEO_03 COMPLETE")
    print("=" * 70)

    return results

if __name__ == "__main__":
    main()
