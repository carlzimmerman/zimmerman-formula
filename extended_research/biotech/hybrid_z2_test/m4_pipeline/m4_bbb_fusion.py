#!/usr/bin/env python3
"""
Blood-Brain Barrier Fusion Protein Engineering

SPDX-License-Identifier: AGPL-3.0-or-later

Engineers BBB-crossing capability using receptor-mediated transcytosis.

SCIENTIFIC BASIS:
- The BBB prevents >98% of small molecules from entering the brain
- Proteins cannot passively cross (too large, too polar)
- LRP1 receptor-mediated transcytosis is a validated crossing mechanism
- Angiopep-2 peptide binds LRP1 and shuttles cargo across BBB

ANGIOPEP-2:
- Sequence: TFFYGGSRGKRNNFKTEEY (19 aa)
- Derived from aprotinin Kunitz domain
- Binds LRP1 with high affinity
- Used in ANG1005 (Angiopep-2-paclitaxel conjugate) for brain tumors
- Published: Demeule et al., 2008, J. Neurochem.

ENGINEERING:
1. Prepend Angiopep-2 to N-terminus
2. Connect via flexible GGGGS linker
3. Calculate final fusion properties

Author: Carl Zimmerman
Date: April 2026
License: AGPL-3.0-or-later
"""

import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple

# ==============================================================================
# VALIDATED SEQUENCES
# ==============================================================================

# Angiopep-2: LRP1-binding brain-penetrating peptide
# Reference: Demeule et al., 2008, J. Neurochem. 106(4):1534-44
ANGIOPEP2 = "TFFYGGSRGKRNNFKTEEY"

# Standard flexible linkers
LINKERS = {
    'GGGGS': "GGGGS",
    'GGGGS_x2': "GGGGSGGGGS",
    'GGGGS_x3': "GGGGSGGGGSGGGGS",  # Standard flexible linker
    'GGGGS_x4': "GGGGSGGGGSGGGGSGGGGS",
    'EAAAK_x3': "EAAAKEAAAKEAAAK",  # Rigid helical linker
    'PAPAP': "PAPAP",  # Proline-rich flexible
}

# Other brain-penetrating peptides (alternatives)
ALTERNATIVE_BPPS = {
    'TAT': {
        'sequence': "YGRKKRRQRRR",
        'mechanism': "Cell-penetrating peptide (CPP)",
        'reference': "Frankel & Pabo, 1988"
    },
    'Penetratin': {
        'sequence': "RQIKIWFQNRRMKWKK",
        'mechanism': "Cell-penetrating peptide (CPP)",
        'reference': "Derossi et al., 1994"
    },
    'SynB1': {
        'sequence': "RGGRLSYSRRRFSTSTGR",
        'mechanism': "Adsorptive-mediated transcytosis",
        'reference': "Rousselle et al., 2000"
    }
}

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

MW = {
    'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
    'E': 147.1, 'Q': 146.2, 'G': 75.1, 'H': 155.2, 'I': 131.2,
    'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
    'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
}

# Kyte-Doolittle hydropathy
HYDROPATHY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'N': -3.5,
    'D': -3.5, 'Q': -3.5, 'E': -3.5, 'K': -3.9, 'R': -4.5
}

PKA = {
    'D': 3.9, 'E': 4.1, 'H': 6.0, 'C': 8.3,
    'Y': 10.1, 'K': 10.5, 'R': 12.5,
    'N_term': 9.6, 'C_term': 2.3
}


def parse_sequence_from_fasta(fasta_file: str) -> str:
    """Parse sequence from FASTA."""
    sequence = []
    with open(fasta_file, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence.append(line.strip())
    return ''.join(sequence)


def calculate_molecular_weight(sequence: str) -> float:
    """Calculate MW in Daltons."""
    mw = sum(MW.get(aa, 110) for aa in sequence)
    mw -= 18.015 * (len(sequence) - 1)  # Water loss
    return mw


def calculate_gravy(sequence: str) -> float:
    """Calculate GRAVY (Grand Average of Hydropathy)."""
    if len(sequence) == 0:
        return 0.0
    hydro_sum = sum(HYDROPATHY.get(aa, 0) for aa in sequence)
    return hydro_sum / len(sequence)


def calculate_isoelectric_point(sequence: str) -> float:
    """Calculate pI using Henderson-Hasselbalch."""
    def charge_at_ph(seq: str, ph: float) -> float:
        charge = 0.0
        charge += 1.0 / (1.0 + 10**(ph - PKA['N_term']))
        charge += -1.0 / (1.0 + 10**(PKA['C_term'] - ph))

        for aa in seq:
            if aa in ['D', 'E']:
                charge += -1.0 / (1.0 + 10**(PKA.get(aa, 4.0) - ph))
            elif aa in ['K', 'R', 'H']:
                charge += 1.0 / (1.0 + 10**(ph - PKA.get(aa, 10.0)))
        return charge

    low, high = 0.0, 14.0
    while high - low > 0.01:
        mid = (low + high) / 2
        if charge_at_ph(sequence, mid) > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def calculate_net_charge(sequence: str, ph: float = 7.4) -> float:
    """Calculate net charge at given pH."""
    charge = 0.0
    charge += 1.0 / (1.0 + 10**(ph - PKA['N_term']))
    charge += -1.0 / (1.0 + 10**(PKA['C_term'] - ph))

    for aa in sequence:
        if aa in ['D', 'E']:
            charge += -1.0 / (1.0 + 10**(PKA.get(aa, 4.0) - ph))
        elif aa in ['K', 'R', 'H']:
            charge += 1.0 / (1.0 + 10**(ph - PKA.get(aa, 10.0)))
    return charge


def calculate_composition(sequence: str) -> Dict:
    """Calculate amino acid composition."""
    composition = {}
    for aa in sequence:
        composition[aa] = composition.get(aa, 0) + 1

    # Percentages
    total = len(sequence)
    percentages = {aa: count / total * 100 for aa, count in composition.items()}

    # Categories
    positive = sum(composition.get(aa, 0) for aa in ['K', 'R', 'H'])
    negative = sum(composition.get(aa, 0) for aa in ['D', 'E'])
    hydrophobic = sum(composition.get(aa, 0) for aa in ['A', 'V', 'L', 'I', 'M', 'F', 'W', 'P'])
    polar = sum(composition.get(aa, 0) for aa in ['S', 'T', 'N', 'Q', 'Y', 'C'])
    aromatic = sum(composition.get(aa, 0) for aa in ['F', 'Y', 'W'])

    return {
        'counts': composition,
        'percentages': percentages,
        'positive_charged': positive,
        'negative_charged': negative,
        'hydrophobic': hydrophobic,
        'polar': polar,
        'aromatic': aromatic
    }


def design_fusion_protein(payload: str,
                          bpp: str = ANGIOPEP2,
                          linker: str = "GGGGS_x3") -> Tuple[str, Dict]:
    """
    Design BBB-crossing fusion protein.

    Architecture: [BPP]-[Linker]-[Payload]
    """
    linker_seq = LINKERS.get(linker, linker)

    # Build fusion
    fusion = bpp + linker_seq + payload

    design = {
        'architecture': f"[Angiopep-2]-[{linker}]-[Payload]",
        'bpp_sequence': bpp,
        'bpp_length': len(bpp),
        'linker_type': linker,
        'linker_sequence': linker_seq,
        'linker_length': len(linker_seq),
        'payload_length': len(payload),
        'total_length': len(fusion),
        'junction_1': f"...{bpp[-5:]}-{linker_seq[:5]}...",
        'junction_2': f"...{linker_seq[-5:]}-{payload[:5]}..."
    }

    return fusion, design


def assess_bbb_crossing_potential(fusion: str, design: Dict) -> Dict:
    """Assess BBB crossing potential."""
    mw = calculate_molecular_weight(fusion)
    gravy = calculate_gravy(fusion)
    pi = calculate_isoelectric_point(fusion)
    charge = calculate_net_charge(fusion)

    # Angiopep-2 properties
    ang2_mw = calculate_molecular_weight(design['bpp_sequence'])
    ang2_gravy = calculate_gravy(design['bpp_sequence'])

    # Assessment criteria
    assessment = {
        'mechanism': 'LRP1 receptor-mediated transcytosis',
        'targeting_peptide': 'Angiopep-2',
        'receptor': 'Low-density lipoprotein receptor-related protein 1 (LRP1)',
        'expression': 'Brain endothelium, neurons, astrocytes',

        'fusion_properties': {
            'molecular_weight_da': mw,
            'molecular_weight_kda': mw / 1000,
            'gravy': gravy,
            'pI': pi,
            'net_charge_pH7.4': charge,
            'total_residues': len(fusion)
        },

        'angiopep2_properties': {
            'kd_lrp1_nm': 100,  # Approximate Kd for LRP1 binding
            'molecular_weight_da': ang2_mw,
            'gravy': ang2_gravy,
            'reference': 'Demeule et al., 2008, J. Neurochem.'
        },

        'clinical_precedent': {
            'drug': 'ANG1005 (paclitaxel-Angiopep-2)',
            'indication': 'Brain metastases, glioblastoma',
            'status': 'Phase III clinical trials',
            'company': 'Angiochem/Astellas'
        },

        'crossing_prediction': {
            'can_cross': True,
            'mechanism': 'Receptor-mediated transcytosis via LRP1',
            'rate_estimate': 'Enhanced vs unmodified protein',
            'caveats': [
                'Actual crossing efficiency depends on payload size',
                'May require optimization of linker length',
                'In vivo validation required'
            ]
        }
    }

    return assessment


def create_visualization(payload: str, fusion: str, design: Dict,
                         assessment: Dict, output_dir: str):
    """Create visualization."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, FancyBboxPatch
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Fusion architecture diagram
    ax1 = axes[0, 0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 4)

    # Draw domains
    # Angiopep-2
    ang2_box = FancyBboxPatch((0.5, 1.5), 2, 1.5, boxstyle="round,pad=0.05",
                               facecolor='red', edgecolor='darkred', alpha=0.8)
    ax1.add_patch(ang2_box)
    ax1.text(1.5, 2.25, 'Angiopep-2\n(BBB targeting)', ha='center', va='center',
             fontsize=10, fontweight='bold', color='white')

    # Linker
    linker_box = FancyBboxPatch((2.7, 1.8), 1.5, 0.9, boxstyle="round,pad=0.05",
                                 facecolor='gray', edgecolor='black', alpha=0.6)
    ax1.add_patch(linker_box)
    ax1.text(3.45, 2.25, '(GGGGS)₃\nLinker', ha='center', va='center',
             fontsize=9, color='white')

    # Payload
    payload_box = FancyBboxPatch((4.4, 1.2), 4.5, 2.1, boxstyle="round,pad=0.05",
                                  facecolor='blue', edgecolor='darkblue', alpha=0.8)
    ax1.add_patch(payload_box)
    ax1.text(6.65, 2.25, f'Therapeutic Payload\n({len(payload)} aa)', ha='center', va='center',
             fontsize=11, fontweight='bold', color='white')

    ax1.set_title('Fusion Protein Architecture', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # 2. BBB crossing mechanism
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 6)

    # Draw BBB schematic
    # Blood side
    ax2.fill_between([0, 10], [4, 4], [6, 6], color='lightcoral', alpha=0.3)
    ax2.text(5, 5, 'Blood', ha='center', fontsize=12, fontweight='bold')

    # Endothelium
    ax2.fill_between([0, 10], [2.5, 2.5], [4, 4], color='lightblue', alpha=0.5)
    ax2.text(5, 3.25, 'Brain Endothelium\n(BBB)', ha='center', fontsize=10)

    # Brain side
    ax2.fill_between([0, 10], [0, 0], [2.5, 2.5], color='lightyellow', alpha=0.3)
    ax2.text(5, 1.25, 'Brain Parenchyma', ha='center', fontsize=12, fontweight='bold')

    # LRP1 receptor
    ax2.plot([3, 3], [2.5, 4], 'g-', linewidth=3)
    ax2.scatter([3], [4], s=200, c='green', marker='v', zorder=5)
    ax2.text(3, 4.3, 'LRP1', ha='center', fontsize=9, fontweight='bold', color='green')

    # Fusion protein trajectory
    ax2.annotate('', xy=(3, 2.5), xytext=(3, 5.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax2.scatter([3], [5.3], s=100, c='red', marker='o', zorder=5)
    ax2.text(4, 5.3, 'Ang2-Payload', fontsize=9, color='red')

    ax2.text(7, 3.25, 'Receptor-Mediated\nTranscytosis', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax2.set_title('BBB Crossing Mechanism', fontsize=12, fontweight='bold')
    ax2.axis('off')

    # 3. Sequence properties
    ax3 = axes[1, 0]

    # Bar chart of domain lengths
    domains = ['Angiopep-2', 'Linker', 'Payload', 'Total']
    lengths = [design['bpp_length'], design['linker_length'],
               design['payload_length'], design['total_length']]
    colors = ['red', 'gray', 'blue', 'purple']

    bars = ax3.barh(domains, lengths, color=colors, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Length (residues)')
    ax3.set_title('Domain Lengths')

    # Add values
    for bar, length in zip(bars, lengths):
        ax3.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                f'{length}', va='center', fontsize=10)

    # 4. Summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    props = assessment['fusion_properties']

    summary = f"""
    BBB FUSION PROTEIN SUMMARY
    {'='*45}

    ARCHITECTURE:
      {design['architecture']}

    DIMENSIONS:
      Total length:    {props['total_residues']} residues
      Molecular weight: {props['molecular_weight_kda']:.1f} kDa

    PROPERTIES:
      GRAVY:           {props['gravy']:.2f}
      pI:              {props['pI']:.2f}
      Net charge (7.4): {props['net_charge_pH7.4']:+.1f}

    BBB CROSSING:
      Mechanism: {assessment['mechanism']}
      Receptor:  LRP1
      Status:    {assessment['crossing_prediction']['can_cross']}

    CLINICAL PRECEDENT:
      {assessment['clinical_precedent']['drug']}
      Status: {assessment['clinical_precedent']['status']}
    """

    ax4.text(0.02, 0.98, summary, transform=ax4.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))

    plt.suptitle('Blood-Brain Barrier Fusion Protein Engineering',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bbb_fusion.png'), dpi=150)
    plt.close()

    print(f"  ✓ Visualization: {output_dir}/bbb_fusion.png")


def main():
    """Run BBB fusion engineering."""
    print("=" * 70)
    print("BLOOD-BRAIN BARRIER FUSION PROTEIN ENGINEERING")
    print("=" * 70)
    print("Using receptor-mediated transcytosis for brain delivery:")
    print("  • Angiopep-2 peptide targets LRP1 receptor")
    print("  • Flexible linker provides structural freedom")
    print("  • Validated in clinical trials (ANG1005)")
    print("=" * 70)

    # Try to load cloaked sequence first, then supercharged, then original
    sources = [
        "empirical_cloaking/cloaked.fasta",
        "empirical_supercharging/supercharged.fasta",
        "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"
    ]

    payload = None
    source = None

    for src in sources:
        if os.path.exists(src):
            if src.endswith('.fasta'):
                payload = parse_sequence_from_fasta(src)
            else:
                # Parse PDB
                aa_map = {
                    'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
                    'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
                    'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
                    'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
                }
                seq = []
                seen = set()
                with open(src, 'r') as f:
                    for line in f:
                        if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                            res_num = int(line[22:26])
                            if res_num not in seen:
                                seen.add(res_num)
                                seq.append(aa_map.get(line[17:20].strip(), 'X'))
                payload = ''.join(seq)
            source = src
            break

    if payload is None:
        print("✗ ERROR: No payload sequence found")
        return None

    # Create output directory
    output_dir = "bbb_fusion"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n  Payload source: {source}")
    print(f"  Payload length: {len(payload)} residues")

    # Display Angiopep-2 info
    print("\n" + "=" * 60)
    print("BRAIN-PENETRATING PEPTIDE: Angiopep-2")
    print("=" * 60)
    print(f"  Sequence: {ANGIOPEP2}")
    print(f"  Length: {len(ANGIOPEP2)} aa")
    print(f"  Mechanism: LRP1 receptor-mediated transcytosis")
    print(f"  Reference: Demeule et al., 2008, J. Neurochem.")

    # Design fusion
    print("\n" + "=" * 60)
    print("FUSION PROTEIN DESIGN")
    print("=" * 60)

    fusion, design = design_fusion_protein(payload, ANGIOPEP2, "GGGGS_x3")

    print(f"  Architecture: {design['architecture']}")
    print(f"  Angiopep-2: {design['bpp_length']} aa")
    print(f"  Linker: {design['linker_length']} aa ({design['linker_type']})")
    print(f"  Payload: {design['payload_length']} aa")
    print(f"  Total: {design['total_length']} aa")
    print(f"\n  Junction 1: {design['junction_1']}")
    print(f"  Junction 2: {design['junction_2']}")

    # Calculate properties
    print("\n" + "=" * 60)
    print("FUSION PROPERTIES")
    print("=" * 60)

    mw = calculate_molecular_weight(fusion)
    gravy = calculate_gravy(fusion)
    pi = calculate_isoelectric_point(fusion)
    charge = calculate_net_charge(fusion)
    composition = calculate_composition(fusion)

    print(f"  Molecular weight: {mw:.1f} Da ({mw/1000:.2f} kDa)")
    print(f"  GRAVY score: {gravy:.3f}")
    print(f"  Isoelectric point: {pi:.2f}")
    print(f"  Net charge (pH 7.4): {charge:+.1f}")
    print(f"\n  Composition:")
    print(f"    Positive charged: {composition['positive_charged']} ({composition['positive_charged']/len(fusion)*100:.1f}%)")
    print(f"    Negative charged: {composition['negative_charged']} ({composition['negative_charged']/len(fusion)*100:.1f}%)")
    print(f"    Hydrophobic: {composition['hydrophobic']} ({composition['hydrophobic']/len(fusion)*100:.1f}%)")

    # Assess BBB crossing
    print("\n" + "=" * 60)
    print("BBB CROSSING ASSESSMENT")
    print("=" * 60)

    assessment = assess_bbb_crossing_potential(fusion, design)

    print(f"  Mechanism: {assessment['mechanism']}")
    print(f"  Receptor: {assessment['receptor']}")
    print(f"  Can cross BBB: {assessment['crossing_prediction']['can_cross']}")
    print(f"\n  Clinical precedent: {assessment['clinical_precedent']['drug']}")
    print(f"  Status: {assessment['clinical_precedent']['status']}")

    # Create visualization
    create_visualization(payload, fusion, design, assessment, output_dir)

    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'payload_source': source,
        'payload_sequence': payload,
        'payload_length': len(payload),
        'angiopep2_sequence': ANGIOPEP2,
        'linker_type': "GGGGS_x3",
        'linker_sequence': LINKERS["GGGGS_x3"],
        'fusion_sequence': fusion,
        'design': design,
        'properties': {
            'molecular_weight_da': mw,
            'molecular_weight_kda': mw / 1000,
            'gravy': gravy,
            'pI': pi,
            'net_charge_pH7.4': charge,
            'composition': composition
        },
        'bbb_assessment': assessment
    }

    output_file = os.path.join(output_dir, 'bbb_fusion_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  ✓ Results: {output_file}")

    # Save fusion FASTA
    fasta_out = os.path.join(output_dir, 'bbb_fusion.fasta')
    with open(fasta_out, 'w') as f:
        f.write(f">BBB_fusion|Angiopep2-GGGGS3-Payload|{len(fusion)}aa|{mw/1000:.1f}kDa\n")
        # Wrap at 60 chars
        for i in range(0, len(fusion), 60):
            f.write(fusion[i:i+60] + "\n")
    print(f"  ✓ FASTA: {fasta_out}")

    # Summary
    print("\n" + "=" * 70)
    print("BBB FUSION COMPLETE")
    print("=" * 70)
    print(f"""
  RESULT:
  ┌─────────────────────────────────────────────────────────────┐
  │ FUSION PROTEIN: Angiopep-2 + Payload                       │
  │                                                             │
  │ Total length:    {design['total_length']:4d} residues                          │
  │ Molecular weight: {mw/1000:5.1f} kDa                               │
  │ GRAVY:           {gravy:+5.2f}                                   │
  │ pI:              {pi:5.2f}                                    │
  │                                                             │
  │ BBB CROSSING: LRP1 receptor-mediated transcytosis          │
  │ VALIDATION: ANG1005 (Phase III clinical trials)            │
  └─────────────────────────────────────────────────────────────┘
    """)

    return results


if __name__ == "__main__":
    results = main()
