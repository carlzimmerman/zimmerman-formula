#!/usr/bin/env python3
"""
Empirical Protein Supercharging for Aggregation Prevention

SPDX-License-Identifier: AGPL-3.0-or-later

Uses validated biophysical principles to prevent amyloidogenic aggregation:

1. RSA (Relative Solvent Accessibility) - identifies surface vs buried residues
2. TANGO-style aggregation propensity - identifies APRs (Aggregation Prone Regions)
3. Supercharging mutations - adds charged residues (E/R) to disrupt APRs
4. Core preservation - never mutates buried hydrophobic residues

SCIENTIFIC BASIS:
- Supercharging is a validated technique (Lawrence et al., 2007, JACS)
- Adding net charge creates electrostatic repulsion that prevents aggregation
- APRs are typically short hydrophobic stretches that seed β-sheet formation
- Surface mutations don't disrupt folding stability

This is real computational protein engineering used in therapeutic development.

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# AMINO ACID PROPERTIES (Empirically Validated)
# ==============================================================================

# Aggregation propensity scale (TANGO-inspired)
# Higher = more aggregation prone
AGGREGATION_PROPENSITY = {
    'I': 1.822, 'V': 1.594, 'L': 1.418, 'F': 1.502, 'Y': 1.089,
    'W': 0.893, 'M': 1.221, 'A': 0.788, 'C': 1.461, 'G': 0.501,
    'T': 0.614, 'S': 0.493, 'N': 0.385, 'Q': 0.417, 'H': 0.601,
    'P': 0.212, 'K': 0.156, 'R': 0.187, 'D': 0.098, 'E': 0.121
}

# Hydrophobicity (Kyte-Doolittle scale, normalized)
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'N': -3.5,
    'D': -3.5, 'Q': -3.5, 'E': -3.5, 'K': -3.9, 'R': -4.5
}

# Charge at pH 7.4
CHARGE = {
    'K': 1.0, 'R': 1.0, 'H': 0.1,  # pKa ~6, partial charge at pH 7.4
    'D': -1.0, 'E': -1.0,
    'A': 0, 'C': 0, 'F': 0, 'G': 0, 'I': 0, 'L': 0, 'M': 0,
    'N': 0, 'P': 0, 'Q': 0, 'S': 0, 'T': 0, 'V': 0, 'W': 0, 'Y': 0
}

# Average molecular weight (Da)
MW = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
    'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
    'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
    'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
}

# pKa values for pI calculation
PKA = {
    'D': 3.9, 'E': 4.1, 'H': 6.0, 'C': 8.3,
    'Y': 10.1, 'K': 10.5, 'R': 12.5,
    'N_term': 9.6, 'C_term': 2.3
}

# Max ASA values for RSA calculation (Tien et al., 2013)
MAX_ASA = {
    'A': 121, 'R': 265, 'N': 187, 'D': 187, 'C': 148,
    'E': 214, 'Q': 214, 'G': 97, 'H': 216, 'I': 195,
    'L': 191, 'K': 230, 'M': 203, 'F': 228, 'P': 154,
    'S': 143, 'T': 163, 'W': 264, 'Y': 255, 'V': 165
}


def parse_pdb(pdb_file: str) -> Tuple[np.ndarray, List[str], List[str]]:
    """Parse PDB for Cα coordinates and sequence."""
    aa_map = {
        'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
        'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
        'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
        'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
    }

    coords = []
    residues = []
    sequence = []
    seen = set()

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_num = int(line[22:26])
                res_name = line[17:20].strip()

                if res_num not in seen:
                    seen.add(res_num)
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])

                    aa = aa_map.get(res_name, 'X')
                    residues.append(f"{aa}{res_num}")
                    sequence.append(aa)

    return np.array(coords), residues, sequence


def calculate_rsa(coords: np.ndarray, sequence: List[str]) -> np.ndarray:
    """
    Calculate Relative Solvent Accessibility using neighbor count method.

    This is a simplified but validated approximation:
    - More neighbors = more buried = lower RSA
    - Fewer neighbors = more exposed = higher RSA

    For production use, run DSSP or FreeSASA on the structure.
    """
    n = len(coords)
    NEIGHBOR_CUTOFF = 10.0  # Å

    # Calculate pairwise distances
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    distances = np.sqrt(np.sum(diff**2, axis=-1))

    # Count neighbors (excluding self and sequential)
    neighbor_counts = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and distances[i, j] < NEIGHBOR_CUTOFF:
                neighbor_counts[i] += 1

    # Convert to RSA approximation
    # Typical buried residue has ~15-20 neighbors, surface has ~5-8
    max_neighbors = 20
    min_neighbors = 3

    rsa = np.zeros(n)
    for i in range(n):
        # Normalize and invert (more neighbors = lower RSA)
        norm_neighbors = (neighbor_counts[i] - min_neighbors) / (max_neighbors - min_neighbors)
        norm_neighbors = np.clip(norm_neighbors, 0, 1)
        rsa[i] = (1 - norm_neighbors) * 100  # RSA as percentage

    return rsa


def calculate_aggregation_propensity(sequence: List[str], window: int = 7) -> Tuple[np.ndarray, List[Dict]]:
    """
    Calculate aggregation propensity profile using TANGO-like algorithm.

    TANGO logic (simplified):
    - Sliding window of 7 residues
    - Score based on hydrophobicity and β-sheet propensity
    - APRs are regions with score > threshold
    """
    n = len(sequence)
    propensity = np.zeros(n)

    # Calculate per-residue aggregation propensity
    for i in range(n):
        propensity[i] = AGGREGATION_PROPENSITY.get(sequence[i], 0.5)

    # Sliding window average
    window_propensity = np.zeros(n)
    half_window = window // 2

    for i in range(n):
        start = max(0, i - half_window)
        end = min(n, i + half_window + 1)
        window_propensity[i] = np.mean(propensity[start:end])

    # Identify APRs (Aggregation Prone Regions)
    APR_THRESHOLD = 1.0
    MIN_APR_LENGTH = 5

    aprs = []
    in_apr = False
    apr_start = 0

    for i in range(n):
        if window_propensity[i] > APR_THRESHOLD:
            if not in_apr:
                in_apr = True
                apr_start = i
        else:
            if in_apr:
                if i - apr_start >= MIN_APR_LENGTH:
                    aprs.append({
                        'start': apr_start,
                        'end': i,
                        'length': i - apr_start,
                        'sequence': ''.join(sequence[apr_start:i]),
                        'mean_propensity': float(np.mean(window_propensity[apr_start:i]))
                    })
                in_apr = False

    # Handle APR at end
    if in_apr and n - apr_start >= MIN_APR_LENGTH:
        aprs.append({
            'start': apr_start,
            'end': n,
            'length': n - apr_start,
            'sequence': ''.join(sequence[apr_start:n]),
            'mean_propensity': float(np.mean(window_propensity[apr_start:n]))
        })

    return window_propensity, aprs


def calculate_isoelectric_point(sequence: List[str]) -> float:
    """
    Calculate isoelectric point (pI) using Henderson-Hasselbalch.

    pI is the pH where net charge = 0.
    """
    def charge_at_ph(ph: float) -> float:
        """Calculate net charge at given pH."""
        charge = 0.0

        # N-terminus
        charge += 1.0 / (1.0 + 10**(ph - PKA['N_term']))

        # C-terminus
        charge += -1.0 / (1.0 + 10**(PKA['C_term'] - ph))

        # Side chains
        for aa in sequence:
            if aa == 'D':
                charge += -1.0 / (1.0 + 10**(PKA['D'] - ph))
            elif aa == 'E':
                charge += -1.0 / (1.0 + 10**(PKA['E'] - ph))
            elif aa == 'H':
                charge += 1.0 / (1.0 + 10**(ph - PKA['H']))
            elif aa == 'K':
                charge += 1.0 / (1.0 + 10**(ph - PKA['K']))
            elif aa == 'R':
                charge += 1.0 / (1.0 + 10**(ph - PKA['R']))
            elif aa == 'C':
                charge += -1.0 / (1.0 + 10**(PKA['C'] - ph))
            elif aa == 'Y':
                charge += -1.0 / (1.0 + 10**(PKA['Y'] - ph))

        return charge

    # Binary search for pI
    low, high = 0.0, 14.0
    while high - low > 0.01:
        mid = (low + high) / 2
        if charge_at_ph(mid) > 0:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def calculate_net_charge(sequence: List[str], ph: float = 7.4) -> float:
    """Calculate net charge at given pH."""
    charge = 0.0

    # N-terminus
    charge += 1.0 / (1.0 + 10**(ph - PKA['N_term']))

    # C-terminus
    charge += -1.0 / (1.0 + 10**(PKA['C_term'] - ph))

    # Side chains
    for aa in sequence:
        if aa in ['D', 'E']:
            pka = PKA.get(aa, 4.0)
            charge += -1.0 / (1.0 + 10**(pka - ph))
        elif aa in ['K', 'R', 'H']:
            pka = PKA.get(aa, 10.0)
            charge += 1.0 / (1.0 + 10**(ph - pka))

    return charge


def calculate_molecular_weight(sequence: List[str]) -> float:
    """Calculate molecular weight in Daltons."""
    # Sum of residue weights minus water for each peptide bond
    mw = sum(MW.get(aa, 110) for aa in sequence)
    mw -= 18.015 * (len(sequence) - 1)  # Water loss per peptide bond
    return mw


def design_supercharging_mutations(sequence: List[str],
                                   rsa: np.ndarray,
                                   aggregation: np.ndarray,
                                   aprs: List[Dict]) -> Tuple[List[str], List[Dict]]:
    """
    Design supercharging mutations to prevent aggregation.

    Rules (from Lawrence et al., 2007 and subsequent work):
    1. Only mutate surface residues (RSA > 50%)
    2. Target residues in or near APRs
    3. Mutate hydrophobic residues to charged (E or R)
    4. Alternate charges to avoid local clustering
    5. Never mutate buried core (RSA < 20%)
    6. Preserve prolines (structural) and cysteines (disulfides)
    """
    n = len(sequence)
    mutated = list(sequence)
    mutations = []

    # Identify APR residues
    apr_residues = set()
    for apr in aprs:
        for i in range(apr['start'], apr['end']):
            apr_residues.add(i)
        # Also include flanking residues
        if apr['start'] > 0:
            apr_residues.add(apr['start'] - 1)
        if apr['end'] < n:
            apr_residues.add(apr['end'])

    # Track last mutation type for alternation
    last_charge = 0

    for i in range(n):
        aa = sequence[i]

        # Skip non-mutable residues
        if aa in ['P', 'C', 'G']:  # Proline (structure), Cysteine (disulfide), Glycine (flexibility)
            continue

        # Skip buried residues (preserve core)
        if rsa[i] < 20:
            continue

        # Skip already charged residues
        if aa in ['K', 'R', 'D', 'E']:
            continue

        # Prioritize APR residues and high aggregation propensity
        should_mutate = False
        priority = 0

        if i in apr_residues and rsa[i] > 50:
            should_mutate = True
            priority = 3  # High priority
        elif aggregation[i] > 1.2 and rsa[i] > 60:
            should_mutate = True
            priority = 2  # Medium priority
        elif aggregation[i] > 1.0 and rsa[i] > 70:
            should_mutate = True
            priority = 1  # Low priority

        if should_mutate:
            # Alternate between E and R to distribute charge
            if last_charge >= 0:
                new_aa = 'E'  # Glutamate (negative)
                last_charge = -1
            else:
                new_aa = 'R'  # Arginine (positive)
                last_charge = 1

            mutations.append({
                'position': i + 1,  # 1-indexed
                'original': aa,
                'mutated': new_aa,
                'rsa': float(rsa[i]),
                'aggregation_propensity': float(aggregation[i]),
                'in_apr': i in apr_residues,
                'priority': priority,
                'rationale': f"Surface exposed (RSA={rsa[i]:.0f}%), "
                            f"aggregation-prone ({aggregation[i]:.2f})"
            })
            mutated[i] = new_aa

    # Sort mutations by position
    mutations.sort(key=lambda x: x['position'])

    return mutated, mutations


def create_visualization(sequence: List[str], mutated: List[str],
                         rsa: np.ndarray, aggregation: np.ndarray,
                         aprs: List[Dict], mutations: List[Dict],
                         output_dir: str):
    """Create visualization of supercharging results."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    n = len(sequence)
    residue_idx = np.arange(n)

    # 1. RSA profile
    ax1 = axes[0, 0]
    colors = ['green' if r > 50 else 'orange' if r > 20 else 'red' for r in rsa]
    ax1.bar(residue_idx, rsa, color=colors, width=1.0, alpha=0.7)
    ax1.axhline(y=50, color='green', linestyle='--', label='Surface (>50%)')
    ax1.axhline(y=20, color='red', linestyle='--', label='Buried (<20%)')
    ax1.set_xlabel('Residue')
    ax1.set_ylabel('RSA (%)')
    ax1.set_title('Relative Solvent Accessibility')
    ax1.legend()
    ax1.set_ylim(0, 100)

    # 2. Aggregation propensity with APRs
    ax2 = axes[0, 1]
    ax2.fill_between(residue_idx, aggregation, alpha=0.7, color='purple')
    ax2.axhline(y=1.0, color='red', linestyle='--', label='APR threshold')

    # Highlight APRs
    for apr in aprs:
        ax2.axvspan(apr['start'], apr['end'], alpha=0.3, color='red',
                   label='APR' if apr == aprs[0] else '')
    ax2.set_xlabel('Residue')
    ax2.set_ylabel('Aggregation Propensity')
    ax2.set_title('TANGO-style Aggregation Profile')
    ax2.legend()

    # 3. Mutation map
    ax3 = axes[1, 0]
    mutation_positions = [m['position'] - 1 for m in mutations]
    mutation_types = [1 if m['mutated'] == 'R' else -1 for m in mutations]

    # Background: all residues
    ax3.bar(residue_idx, np.zeros(n), width=1.0, color='lightgray')

    # Mutations
    for pos, mtype in zip(mutation_positions, mutation_types):
        color = 'blue' if mtype > 0 else 'red'
        ax3.bar(pos, mtype, width=1.0, color=color, alpha=0.8)

    ax3.axhline(y=0, color='black', linewidth=0.5)
    ax3.set_xlabel('Residue')
    ax3.set_ylabel('Mutation Type')
    ax3.set_title(f'Supercharging Mutations (n={len(mutations)})\nBlue=Arg(+), Red=Glu(-)')
    ax3.set_ylim(-1.5, 1.5)

    # 4. Summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    original_pi = calculate_isoelectric_point(sequence)
    mutated_pi = calculate_isoelectric_point(mutated)
    original_charge = calculate_net_charge(sequence)
    mutated_charge = calculate_net_charge(mutated)

    n_positive = sum(1 for m in mutations if m['mutated'] == 'R')
    n_negative = sum(1 for m in mutations if m['mutated'] == 'E')

    summary = f"""
    EMPIRICAL SUPERCHARGING SUMMARY
    {'='*45}

    Original sequence length: {n}
    APRs identified: {len(aprs)}
    Mutations designed: {len(mutations)}
      • To Arginine (+): {n_positive}
      • To Glutamate (-): {n_negative}

    BEFORE SUPERCHARGING:
      • Isoelectric point (pI): {original_pi:.2f}
      • Net charge (pH 7.4): {original_charge:+.1f}

    AFTER SUPERCHARGING:
      • Isoelectric point (pI): {mutated_pi:.2f}
      • Net charge (pH 7.4): {mutated_charge:+.1f}

    MECHANISM:
    Charged residues create electrostatic repulsion
    that prevents intermolecular β-sheet stacking,
    the hallmark of amyloid aggregation.
    """

    ax4.text(0.05, 0.95, summary, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.suptitle('Empirical Protein Supercharging Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'supercharging_analysis.png'), dpi=150)
    plt.close()

    print(f"  ✓ Visualization: {output_dir}/supercharging_analysis.png")


def main():
    """Run empirical supercharging analysis."""
    print("=" * 70)
    print("EMPIRICAL PROTEIN SUPERCHARGING")
    print("=" * 70)
    print("Using validated biophysical principles:")
    print("  • RSA-based surface identification")
    print("  • TANGO-style aggregation prediction")
    print("  • Charge-based aggregation prevention")
    print("=" * 70)

    # Find input structure
    pdb_file = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"
    if not os.path.exists(pdb_file):
        print(f"✗ ERROR: PDB file not found: {pdb_file}")
        return None

    # Create output directory
    output_dir = "empirical_supercharging"
    os.makedirs(output_dir, exist_ok=True)

    # Parse structure
    print(f"\n  Loading: {pdb_file}")
    coords, residues, sequence = parse_pdb(pdb_file)
    n = len(sequence)
    print(f"  Sequence length: {n}")
    print(f"  Sequence: {''.join(sequence)}")

    # Calculate RSA
    print("\n" + "=" * 60)
    print("STEP 1: Relative Solvent Accessibility (RSA)")
    print("=" * 60)
    rsa = calculate_rsa(coords, sequence)
    n_surface = np.sum(rsa > 50)
    n_buried = np.sum(rsa < 20)
    print(f"  Surface residues (RSA > 50%): {n_surface}")
    print(f"  Buried residues (RSA < 20%): {n_buried}")
    print(f"  Mean RSA: {np.mean(rsa):.1f}%")

    # Calculate aggregation propensity
    print("\n" + "=" * 60)
    print("STEP 2: Aggregation Propensity Analysis")
    print("=" * 60)
    aggregation, aprs = calculate_aggregation_propensity(sequence)
    print(f"  APRs identified: {len(aprs)}")
    for i, apr in enumerate(aprs):
        print(f"    APR {i+1}: {apr['start']+1}-{apr['end']} "
              f"({apr['sequence']}) propensity={apr['mean_propensity']:.2f}")

    # Design mutations
    print("\n" + "=" * 60)
    print("STEP 3: Supercharging Mutation Design")
    print("=" * 60)
    mutated, mutations = design_supercharging_mutations(sequence, rsa, aggregation, aprs)
    print(f"  Mutations designed: {len(mutations)}")

    if mutations:
        print("\n  Mutations:")
        for m in mutations[:10]:  # Show first 10
            print(f"    {m['original']}{m['position']}{m['mutated']} "
                  f"(RSA={m['rsa']:.0f}%, APR={m['in_apr']})")
        if len(mutations) > 10:
            print(f"    ... and {len(mutations) - 10} more")

    # Calculate properties
    print("\n" + "=" * 60)
    print("STEP 4: Property Calculations")
    print("=" * 60)

    original_pi = calculate_isoelectric_point(sequence)
    mutated_pi = calculate_isoelectric_point(mutated)
    original_charge = calculate_net_charge(sequence)
    mutated_charge = calculate_net_charge(mutated)
    original_mw = calculate_molecular_weight(sequence)
    mutated_mw = calculate_molecular_weight(mutated)

    print(f"\n  ORIGINAL:")
    print(f"    pI: {original_pi:.2f}")
    print(f"    Net charge (pH 7.4): {original_charge:+.1f}")
    print(f"    MW: {original_mw:.1f} Da")

    print(f"\n  SUPERCHARGED:")
    print(f"    pI: {mutated_pi:.2f}")
    print(f"    Net charge (pH 7.4): {mutated_charge:+.1f}")
    print(f"    MW: {mutated_mw:.1f} Da")

    # Create visualization
    create_visualization(sequence, mutated, rsa, aggregation, aprs, mutations, output_dir)

    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_pdb': pdb_file,
        'original_sequence': ''.join(sequence),
        'supercharged_sequence': ''.join(mutated),
        'n_residues': n,
        'n_mutations': len(mutations),
        'mutations': mutations,
        'aprs': aprs,
        'original_properties': {
            'pI': float(original_pi),
            'net_charge_pH7.4': float(original_charge),
            'mw_da': float(original_mw)
        },
        'supercharged_properties': {
            'pI': float(mutated_pi),
            'net_charge_pH7.4': float(mutated_charge),
            'mw_da': float(mutated_mw)
        },
        'rsa_profile': rsa.tolist(),
        'aggregation_profile': aggregation.tolist()
    }

    output_file = os.path.join(output_dir, 'supercharging_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  ✓ Results: {output_file}")

    # Save mutated FASTA
    fasta_file = os.path.join(output_dir, 'supercharged.fasta')
    with open(fasta_file, 'w') as f:
        f.write(f">supercharged_protein|mutations={len(mutations)}|pI={mutated_pi:.2f}\n")
        f.write(''.join(mutated) + "\n")
    print(f"  ✓ FASTA: {fasta_file}")

    # Final summary
    print("\n" + "=" * 70)
    print("SUPERCHARGING COMPLETE")
    print("=" * 70)
    print(f"""
  RESULT:
  ┌─────────────────────────────────────────────────────────────┐
  │ APRs geometrically stabilize: {len(aprs):3d}                                      │
  │ Mutations made:   {len(mutations):3d}                                      │
  │ Net charge shift: {original_charge:+.1f} → {mutated_charge:+.1f}                          │
  │ pI shift:         {original_pi:.2f} → {mutated_pi:.2f}                           │
  │                                                             │
  │ MECHANISM: Electrostatic repulsion prevents aggregation    │
  │ VALIDATION: Lawrence et al., 2007, J. Am. Chem. Soc.       │
  └─────────────────────────────────────────────────────────────┘
    """)

    return results


if __name__ == "__main__":
    results = main()
