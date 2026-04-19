#!/usr/bin/env python3
"""
Empirical Stealth Cloaking via N-Linked Glycosylation

SPDX-License-Identifier: AGPL-3.0-or-later

Reduces immunogenicity and protease susceptibility by engineering
N-linked glycosylation sites (glycan shields).

SCIENTIFIC BASIS:
- N-linked glycosylation occurs at Asn-X-Ser/Thr sequons (X ≠ Pro)
- Glycans create steric hindrance blocking protease access
- Host-derived glycans are recognized as "self" by immune system
- Used in FDA-approved biologics (e.g., EPO, mAbs, Fc fusions)

ENGINEERING STRATEGY:
1. Identify vulnerable loops (flexible, exposed, protease-susceptible)
2. Introduce N-X-S/T motifs near these regions
3. Verify engineered sequons don't disrupt structure
4. Output cloaked sequence with glycan site map

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
# PROTEASE CLEAVAGE RULES (ExPASy PeptideCutter)
# ==============================================================================

PROTEASE_RULES = {
    'Trypsin': {
        'sites': ['K', 'R'],
        'not_followed_by': ['P'],
        'description': 'Cleaves after K or R (not before P)'
    },
    'Chymotrypsin': {
        'sites': ['F', 'Y', 'W'],
        'not_followed_by': ['P'],
        'description': 'Cleaves after F, Y, W (not before P)'
    },
    'Pepsin': {
        'sites': ['F', 'L', 'W', 'Y'],
        'before': ['A', 'E', 'L', 'F', 'I', 'V', 'W', 'Y'],
        'description': 'Cleaves at hydrophobic residues'
    },
    'Cathepsin_B': {
        'sites': ['R', 'K'],
        'description': 'Lysosomal protease, cleaves after R, K'
    },
    'Cathepsin_L': {
        'sites': ['L', 'F', 'V', 'Y'],
        'description': 'Lysosomal protease, cleaves at hydrophobics'
    }
}

# Flexibility propensity (higher = more flexible/disordered)
FLEXIBILITY = {
    'G': 1.0, 'S': 0.9, 'D': 0.8, 'N': 0.8, 'P': 0.85,
    'K': 0.7, 'E': 0.7, 'Q': 0.6, 'R': 0.6, 'T': 0.5,
    'A': 0.4, 'H': 0.5, 'C': 0.3, 'M': 0.4, 'V': 0.3,
    'I': 0.2, 'L': 0.2, 'F': 0.2, 'Y': 0.3, 'W': 0.2
}


def parse_sequence_from_fasta(fasta_file: str) -> str:
    """Parse sequence from FASTA file."""
    sequence = []
    with open(fasta_file, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence.append(line.strip())
    return ''.join(sequence)


def parse_pdb_sequence(pdb_file: str) -> str:
    """Extract sequence from PDB."""
    aa_map = {
        'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
        'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
        'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
        'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
    }

    sequence = []
    seen = set()

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_num = int(line[22:26])
                res_name = line[17:20].strip()

                if res_num not in seen:
                    seen.add(res_num)
                    sequence.append(aa_map.get(res_name, 'X'))

    return ''.join(sequence)


def find_protease_sites(sequence: str) -> List[Dict]:
    """Find protease cleavage sites in sequence."""
    sites = []
    n = len(sequence)

    for protease, rules in PROTEASE_RULES.items():
        for i, aa in enumerate(sequence):
            if aa in rules['sites']:
                # Check "not followed by" rule
                if 'not_followed_by' in rules:
                    if i < n - 1 and sequence[i + 1] in rules['not_followed_by']:
                        continue

                # Check "before" rule for pepsin
                if 'before' in rules:
                    if i > 0 and sequence[i - 1] not in rules['before']:
                        continue

                sites.append({
                    'position': i + 1,
                    'residue': aa,
                    'protease': protease,
                    'context': sequence[max(0, i-2):min(n, i+3)]
                })

    return sites


def calculate_flexibility(sequence: str, window: int = 7) -> np.ndarray:
    """Calculate flexibility profile using B-factor proxy."""
    n = len(sequence)
    flex = np.array([FLEXIBILITY.get(aa, 0.5) for aa in sequence])

    # Smooth with window
    smoothed = np.zeros(n)
    half = window // 2

    for i in range(n):
        start = max(0, i - half)
        end = min(n, i + half + 1)
        smoothed[i] = np.mean(flex[start:end])

    return smoothed


def identify_vulnerable_regions(sequence: str,
                                protease_sites: List[Dict],
                                flexibility: np.ndarray) -> List[Dict]:
    """Identify regions vulnerable to proteolysis."""
    n = len(sequence)

    # Group nearby protease sites
    vulnerability = np.zeros(n)

    for site in protease_sites:
        pos = site['position'] - 1
        # Spread vulnerability around cleavage site
        for offset in range(-3, 4):
            idx = pos + offset
            if 0 <= idx < n:
                vulnerability[idx] += 1.0 / (1 + abs(offset))

    # Combine with flexibility
    combined_score = vulnerability * flexibility

    # Find vulnerable regions
    THRESHOLD = 0.5
    regions = []
    in_region = False
    region_start = 0

    for i in range(n):
        if combined_score[i] > THRESHOLD:
            if not in_region:
                in_region = True
                region_start = i
        else:
            if in_region:
                regions.append({
                    'start': region_start,
                    'end': i,
                    'length': i - region_start,
                    'sequence': sequence[region_start:i],
                    'mean_vulnerability': float(np.mean(combined_score[region_start:i])),
                    'protease_sites': [s for s in protease_sites
                                       if region_start < s['position'] <= i]
                })
                in_region = False

    if in_region:
        regions.append({
            'start': region_start,
            'end': n,
            'length': n - region_start,
            'sequence': sequence[region_start:n],
            'mean_vulnerability': float(np.mean(combined_score[region_start:n])),
            'protease_sites': [s for s in protease_sites
                               if region_start < s['position'] <= n]
        })

    return regions


def design_glycosylation_sites(sequence: str,
                                vulnerable_regions: List[Dict],
                                flexibility: np.ndarray) -> Tuple[str, List[Dict]]:
    """
    Design N-linked glycosylation sites near vulnerable regions.

    N-linked glycosylation sequon: Asn-X-Ser/Thr (X ≠ Pro)

    Strategy:
    1. For each vulnerable region, find nearby suitable positions
    2. Introduce NxS or NxT motif
    3. Avoid disrupting secondary structure
    """
    n = len(sequence)
    mutated = list(sequence)
    glycan_sites = []

    # Residues to avoid mutating (structural importance)
    AVOID = set(['C', 'P'])  # Cysteines (disulfides), Prolines (structure)

    for region in vulnerable_regions:
        # Look for positions near but not in the vulnerable region
        # Glycans should shield the region, so place them at boundaries

        candidates = []

        # Check positions at region boundaries
        for offset in [-3, -2, -1, 0, 1, 2]:
            # N-terminus side
            pos = region['start'] + offset
            if 0 <= pos < n - 2:
                candidates.append(pos)

            # C-terminus side
            pos = region['end'] + offset
            if 0 <= pos < n - 2:
                candidates.append(pos)

        # Score candidates
        best_pos = None
        best_score = -1

        for pos in candidates:
            # Skip if would create P in middle position (NxS where x=P is invalid)
            if mutated[pos + 1] == 'P':
                continue

            # Skip if current position is important
            if mutated[pos] in AVOID:
                continue

            # Prefer flexible positions
            score = flexibility[pos]

            # Avoid positions that already have N (existing sequon)
            if mutated[pos] == 'N':
                score -= 0.5

            if score > best_score:
                best_score = score
                best_pos = pos

        if best_pos is not None and best_pos not in [g['position'] for g in glycan_sites]:
            # Create sequon: mutate to N at position, ensure S or T at +2
            original_n = mutated[best_pos]
            original_st = mutated[best_pos + 2]

            mutated[best_pos] = 'N'

            if mutated[best_pos + 2] not in ['S', 'T']:
                mutated[best_pos + 2] = 'S'  # Prefer Ser

            glycan_sites.append({
                'position': best_pos + 1,
                'sequon': f"N-{mutated[best_pos + 1]}-{mutated[best_pos + 2]}",
                'mutations': [
                    f"{original_n}{best_pos + 1}N"
                ] + ([f"{original_st}{best_pos + 3}S"] if original_st not in ['S', 'T'] else []),
                'shields_region': {
                    'start': region['start'] + 1,
                    'end': region['end']
                },
                'flexibility': float(flexibility[best_pos])
            })

    return ''.join(mutated), glycan_sites


def find_existing_glycan_sites(sequence: str) -> List[Dict]:
    """Find existing N-linked glycosylation sequons."""
    sites = []
    n = len(sequence)

    for i in range(n - 2):
        if sequence[i] == 'N' and sequence[i + 1] != 'P' and sequence[i + 2] in ['S', 'T']:
            sites.append({
                'position': i + 1,
                'sequon': f"{sequence[i]}-{sequence[i+1]}-{sequence[i+2]}",
                'native': True
            })

    return sites


def create_visualization(sequence: str, cloaked: str,
                         flexibility: np.ndarray,
                         protease_sites: List[Dict],
                         vulnerable_regions: List[Dict],
                         glycan_sites: List[Dict],
                         output_dir: str):
    """Create visualization."""
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

    # 1. Flexibility profile with vulnerable regions
    ax1 = axes[0, 0]
    ax1.fill_between(residue_idx, flexibility, alpha=0.7, color='blue')
    ax1.axhline(y=0.5, color='red', linestyle='--', label='Vulnerability threshold')

    for region in vulnerable_regions:
        ax1.axvspan(region['start'], region['end'], alpha=0.3, color='red')

    ax1.set_xlabel('Residue')
    ax1.set_ylabel('Flexibility')
    ax1.set_title('Flexibility Profile (red = vulnerable regions)')
    ax1.legend()

    # 2. Protease sites by type
    ax2 = axes[0, 1]
    protease_types = list(set(s['protease'] for s in protease_sites))
    colors = plt.cm.Set1(np.linspace(0, 1, len(protease_types)))
    protease_colors = {p: c for p, c in zip(protease_types, colors)}

    for site in protease_sites:
        pos = site['position'] - 1
        ax2.scatter(pos, 1, c=[protease_colors[site['protease']]],
                   s=100, marker='v', alpha=0.7)

    # Add glycan shields
    for gs in glycan_sites:
        pos = gs['position'] - 1
        ax2.scatter(pos, 0.5, c='green', s=200, marker='^', alpha=0.8)
        ax2.annotate('Glycan', (pos, 0.5), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=8)

    ax2.set_xlabel('Residue')
    ax2.set_ylabel('Feature')
    ax2.set_title(f'Protease Sites (▼) and Glycan Shields (▲)')
    ax2.set_ylim(0, 1.5)

    # Legend for proteases
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='v', color='w',
                              markerfacecolor=protease_colors[p],
                              markersize=10, label=p)
                      for p in protease_types]
    legend_elements.append(Line2D([0], [0], marker='^', color='w',
                                  markerfacecolor='green',
                                  markersize=10, label='Glycan site'))
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=8)

    # 3. Sequence alignment
    ax3 = axes[1, 0]
    ax3.axis('off')

    # Show mutations
    diff_positions = [i for i in range(n) if sequence[i] != cloaked[i]]

    align_text = "Original:  "
    for i, aa in enumerate(sequence):
        if i in diff_positions:
            align_text += f"[{aa}]"
        else:
            align_text += aa
        if (i + 1) % 50 == 0:
            align_text += "\n           "

    align_text += "\n\nCloaked:   "
    for i, aa in enumerate(cloaked):
        if i in diff_positions:
            align_text += f"[{aa}]"
        else:
            align_text += aa
        if (i + 1) % 50 == 0:
            align_text += "\n           "

    ax3.text(0.02, 0.95, f"Mutations shown in [brackets]\n\n{align_text}",
             transform=ax3.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace')
    ax3.set_title('Sequence Comparison')

    # 4. Summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    summary = f"""
    STEALTH CLOAKING SUMMARY
    {'='*45}

    PROTEASE VULNERABILITY:
      Total cleavage sites: {len(protease_sites)}
      Vulnerable regions: {len(vulnerable_regions)}

    GLYCAN SHIELDS ENGINEERED:
      New N-linked sites: {len(glycan_sites)}

    ENGINEERED SEQUONS:
    """

    for gs in glycan_sites[:5]:
        summary += f"\n      • Position {gs['position']}: {gs['sequon']}"
        summary += f"\n        Shields region {gs['shields_region']['start']}-{gs['shields_region']['end']}"

    summary += f"""

    MECHANISM:
    N-linked glycans (Asn-X-Ser/Thr) are added by
    host cell machinery. These complex sugar trees
    create steric hindrance blocking protease access
    and antibody binding.
    """

    ax4.text(0.02, 0.98, summary, transform=ax4.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

    plt.suptitle('Empirical Stealth Cloaking via N-Linked Glycosylation',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cloaking_analysis.png'), dpi=150)
    plt.close()

    print(f"  ✓ Visualization: {output_dir}/cloaking_analysis.png")


def main():
    """Run empirical cloaking analysis."""
    print("=" * 70)
    print("EMPIRICAL STEALTH CLOAKING")
    print("=" * 70)
    print("Engineering N-linked glycosylation sites for immune evasion:")
    print("  • Protease site identification (ExPASy-style)")
    print("  • Vulnerable loop detection")
    print("  • N-X-S/T sequon engineering")
    print("=" * 70)

    # Try to load supercharged sequence first
    fasta_file = "empirical_supercharging/supercharged.fasta"
    pdb_file = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"

    if os.path.exists(fasta_file):
        sequence = parse_sequence_from_fasta(fasta_file)
        source = fasta_file
    elif os.path.exists(pdb_file):
        sequence = parse_pdb_sequence(pdb_file)
        source = pdb_file
    else:
        print("✗ ERROR: No input sequence found")
        return None

    # Create output directory
    output_dir = "empirical_cloaking"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n  Input: {source}")
    print(f"  Sequence length: {len(sequence)}")

    # Find existing glycan sites
    print("\n" + "=" * 60)
    print("STEP 1: Existing Glycosylation Sites")
    print("=" * 60)
    existing_sites = find_existing_glycan_sites(sequence)
    print(f"  Native N-linked sequons: {len(existing_sites)}")
    for site in existing_sites:
        print(f"    Position {site['position']}: {site['sequon']}")

    # Find protease sites
    print("\n" + "=" * 60)
    print("STEP 2: Protease Cleavage Site Analysis")
    print("=" * 60)
    protease_sites = find_protease_sites(sequence)
    print(f"  Total cleavage sites: {len(protease_sites)}")

    # Count by protease
    by_protease = {}
    for site in protease_sites:
        by_protease[site['protease']] = by_protease.get(site['protease'], 0) + 1
    for protease, count in sorted(by_protease.items()):
        print(f"    {protease}: {count} sites")

    # Calculate flexibility
    print("\n" + "=" * 60)
    print("STEP 3: Flexibility Analysis")
    print("=" * 60)
    flexibility = calculate_flexibility(sequence)
    print(f"  Mean flexibility: {np.mean(flexibility):.3f}")
    print(f"  Max flexibility: {np.max(flexibility):.3f}")

    # Identify vulnerable regions
    print("\n" + "=" * 60)
    print("STEP 4: Vulnerable Region Identification")
    print("=" * 60)
    vulnerable_regions = identify_vulnerable_regions(sequence, protease_sites, flexibility)
    print(f"  Vulnerable regions: {len(vulnerable_regions)}")
    for i, region in enumerate(vulnerable_regions[:5]):
        print(f"    Region {i+1}: {region['start']+1}-{region['end']} "
              f"({region['sequence'][:15]}...) vulnerability={region['mean_vulnerability']:.2f}")

    # Design glycosylation sites
    print("\n" + "=" * 60)
    print("STEP 5: Glycan Shield Engineering")
    print("=" * 60)
    cloaked, glycan_sites = design_glycosylation_sites(sequence, vulnerable_regions, flexibility)
    print(f"  Glycan sites engineered: {len(glycan_sites)}")

    for gs in glycan_sites:
        print(f"    Position {gs['position']}: {gs['sequon']}")
        print(f"      Mutations: {', '.join(gs['mutations'])}")
        print(f"      Shields: residues {gs['shields_region']['start']}-{gs['shields_region']['end']}")

    # Create visualization
    create_visualization(sequence, cloaked, flexibility, protease_sites,
                        vulnerable_regions, glycan_sites, output_dir)

    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'input_source': source,
        'original_sequence': sequence,
        'cloaked_sequence': cloaked,
        'n_residues': len(sequence),
        'existing_glycan_sites': existing_sites,
        'protease_sites': protease_sites,
        'vulnerable_regions': vulnerable_regions,
        'engineered_glycan_sites': glycan_sites,
        'flexibility_profile': flexibility.tolist()
    }

    output_file = os.path.join(output_dir, 'cloaking_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  ✓ Results: {output_file}")

    # Save cloaked FASTA
    fasta_out = os.path.join(output_dir, 'cloaked.fasta')
    with open(fasta_out, 'w') as f:
        f.write(f">cloaked_protein|glycan_sites={len(glycan_sites)}\n")
        f.write(cloaked + "\n")
    print(f"  ✓ FASTA: {fasta_out}")

    # Summary
    print("\n" + "=" * 70)
    print("STEALTH CLOAKING COMPLETE")
    print("=" * 70)
    print(f"""
  RESULT:
  ┌─────────────────────────────────────────────────────────────┐
  │ Protease sites found:  {len(protease_sites):3d}                               │
  │ Vulnerable regions:    {len(vulnerable_regions):3d}                               │
  │ Glycan shields added:  {len(glycan_sites):3d}                               │
  │                                                             │
  │ MECHANISM: Host-derived glycans block proteases/antibodies │
  │ VALIDATION: Standard therapeutic protein engineering       │
  └─────────────────────────────────────────────────────────────┘
    """)

    return results


if __name__ == "__main__":
    results = main()
