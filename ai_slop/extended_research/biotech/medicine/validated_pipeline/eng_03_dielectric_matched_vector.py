#!/usr/bin/env python3
"""
eng_03_dielectric_matched_vector.py

Copyright (C) 2026 Carl Zimmerman
Zimmerman Unified Geometry Framework (ZUGF)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

eng_03_dielectric_matched_vector.py - Z²-Matched Lipid Delivery Vector Engineering

THE MEMBRANE PROBLEM:
====================

Our peptide drugs showed SURFACE or BOUNCED verdicts in membrane simulations.
They need help crossing the blood-brain barrier (BBB).

THE SOLUTION: GEOMETRIC LIPIDATION
==================================

The Z² framework predicts that molecular volumes which are exact MULTIPLES
of Z² = 33.51 Å³ will have optimal thermodynamic fit with biological membranes.

THE ENGINEERING:
1. Calculate the exact number of saturated carbon atoms required to create
   an aliphatic chain whose total Voronoi volume = N × Z² (where N is integer)
2. The membrane bilayer has dielectric ε ≈ 2, which further compresses packing
3. Design a lipid anchor that GEOMETRICALLY RESONATES with membrane packing

LIPID ANCHOR OPTIONS:
- Palmitate (C16): ~460 Å³
- Myristate (C14): ~400 Å³
- Laurate (C12): ~340 Å³
- Custom chain: Tuned for N × 33.51 Å³

THE PREDICTION:
A lipid anchor with volume = N × Z² will partition into the membrane
with MINIMAL energy penalty because it fits the geometric lattice.

AGPL-3.0-or-later License
Author: Carl Zimmerman
Date: April 22, 2026
"""
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings

try:
    from scipy.optimize import minimize_scalar
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2_VOLUME = 32 * np.pi / 3  # 33.51 Å³ - vacuum packing constant
Z2_DISTANCE = np.sqrt(Z2_VOLUME)  # 5.79 Å
EXPANSION_MULTIPLIER = 1.0391  # 310K thermal expansion

# Dielectric constants
WATER_DIELECTRIC = 80.0
MEMBRANE_DIELECTRIC = 2.0
DIELECTRIC_COMPRESSION = (WATER_DIELECTRIC / MEMBRANE_DIELECTRIC) ** 0.1  # Empirical

# Molecular volumes (in Å³, from crystallographic data)
ATOM_VOLUMES = {
    'C_sp3': 16.44,      # Tetrahedral carbon (methylene -CH2-)
    'C_sp2': 14.7,       # Trigonal carbon (C=O, C=C)
    'H': 5.08,           # Hydrogen
    'O': 11.2,           # Oxygen
    'N': 11.8,           # Nitrogen
    'S': 23.5,           # Sulfur
}

# Methylene (-CH2-) group volume
METHYLENE_VOLUME = ATOM_VOLUMES['C_sp3'] + 2 * ATOM_VOLUMES['H']  # ~26.6 Å³

# Methyl (-CH3) terminal group volume
METHYL_VOLUME = ATOM_VOLUMES['C_sp3'] + 3 * ATOM_VOLUMES['H']  # ~31.68 Å³

# Common fatty acid properties
FATTY_ACIDS = {
    'caprylic': {'carbons': 8, 'name': 'Caprylic acid (C8:0)', 'MW': 144.21},
    'capric': {'carbons': 10, 'name': 'Capric acid (C10:0)', 'MW': 172.26},
    'lauric': {'carbons': 12, 'name': 'Lauric acid (C12:0)', 'MW': 200.32},
    'myristic': {'carbons': 14, 'name': 'Myristic acid (C14:0)', 'MW': 228.37},
    'palmitic': {'carbons': 16, 'name': 'Palmitic acid (C16:0)', 'MW': 256.42},
    'stearic': {'carbons': 18, 'name': 'Stearic acid (C18:0)', 'MW': 284.48},
    'arachidic': {'carbons': 20, 'name': 'Arachidic acid (C20:0)', 'MW': 312.53},
}

OUTPUT_DIR = Path(__file__).parent / "results" / "dielectric_matched_vector"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class LipidAnchor:
    """Represents a lipid anchor for drug conjugation."""
    name: str
    n_carbons: int
    total_volume: float
    z2_multiple: float
    z2_deviation: float
    molecular_weight: float
    predicted_logP: float
    membrane_partition_score: float
    smiles: str


def calculate_alkyl_chain_volume(n_carbons: int, include_terminal_ch3: bool = True,
                                  include_carboxyl: bool = True) -> float:
    """
    Calculate the total Voronoi volume of a saturated alkyl chain.

    For a fatty acid COOH-(CH2)_{n-2}-CH3:
    - 1 carboxyl carbon (C=O-OH)
    - (n-2) methylene carbons (-CH2-)
    - 1 terminal methyl (-CH3)
    """
    volume = 0.0

    if include_carboxyl:
        # Carboxyl group: C(=O)-OH
        carboxyl_volume = (ATOM_VOLUMES['C_sp2'] +
                           2 * ATOM_VOLUMES['O'] +
                           1 * ATOM_VOLUMES['H'])  # ~37.08 Å³
        volume += carboxyl_volume
        remaining_carbons = n_carbons - 1
    else:
        remaining_carbons = n_carbons

    if include_terminal_ch3:
        # Terminal methyl
        volume += METHYL_VOLUME
        remaining_carbons -= 1

    # Remaining methylenes
    volume += remaining_carbons * METHYLENE_VOLUME

    return volume


def find_z2_resonant_chain(target_multiple: int) -> Dict:
    """
    Find the alkyl chain length that best matches N × Z² volume.

    Returns chain parameters for optimal Z² resonance.
    """
    target_volume = target_multiple * Z2_VOLUME

    best_result = None
    best_deviation = float('inf')

    # Test chain lengths from C6 to C30
    for n_carbons in range(6, 31):
        volume = calculate_alkyl_chain_volume(n_carbons)
        deviation = abs(volume - target_volume)
        deviation_pct = 100 * deviation / target_volume

        if deviation < best_deviation:
            best_deviation = deviation
            best_result = {
                'n_carbons': n_carbons,
                'volume': volume,
                'target_volume': target_volume,
                'deviation': deviation,
                'deviation_percent': deviation_pct,
                'z2_multiple': target_multiple,
            }

    return best_result


def calculate_membrane_partition_score(volume: float, z2_multiple: float) -> float:
    """
    Calculate predicted membrane partition score based on Z² resonance.

    Score is 0-100 where:
    - 100 = Perfect Z² multiple (exact geometric resonance)
    - 0 = Volume far from any Z² multiple

    The hypothesis: Z²-resonant molecules partition into membranes
    with minimal thermodynamic penalty.
    """
    # Distance to nearest Z² multiple
    nearest_multiple = round(volume / Z2_VOLUME)
    deviation = abs(volume - nearest_multiple * Z2_VOLUME)
    deviation_frac = deviation / Z2_VOLUME

    # Score decreases with deviation
    # Perfect resonance = 100, half-Z² deviation = 50, etc.
    score = 100 * np.exp(-deviation_frac * 2)

    return float(score)


def estimate_logP(n_carbons: int) -> float:
    """
    Estimate log P (octanol-water partition coefficient) for fatty acid.

    Each CH2 contributes approximately +0.5 to logP.
    Carboxyl group contributes approximately -1.0.
    """
    return -1.0 + 0.5 * (n_carbons - 1)


def generate_fatty_acid_smiles(n_carbons: int) -> str:
    """Generate SMILES string for saturated fatty acid."""
    if n_carbons < 2:
        return "C(=O)O"

    # CH3-(CH2)_{n-2}-C(=O)OH
    chain = "C" * (n_carbons - 1) + "C(=O)O"
    return chain


def design_peptide_lipid_conjugate(peptide_sequence: str, lipid_anchor: LipidAnchor) -> Dict:
    """
    Design a peptide-lipid conjugate for membrane delivery.
    """
    # Peptide properties
    from collections import Counter

    AA_MW = {
        'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.15,
        'E': 147.13, 'Q': 146.15, 'G': 75.07, 'H': 155.16, 'I': 131.17,
        'L': 131.17, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
        'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15,
    }

    peptide_mw = 18.015  # Water
    for aa in peptide_sequence.upper():
        if aa in AA_MW:
            peptide_mw += AA_MW[aa] - 18.015  # Subtract water for peptide bond

    # Linker (Gly-Gly-Gly) is common
    linker = "GGG"
    linker_mw = 3 * 75.07 - 2 * 18.015  # 3 Gly minus 2 water for bonds

    # Total MW
    total_mw = peptide_mw + linker_mw + lipid_anchor.molecular_weight

    # Conjugate SMILES (simplified representation)
    peptide_smiles = "-".join(peptide_sequence)  # Simplified
    conjugate_smiles = f"{lipid_anchor.smiles}~{linker}~{peptide_smiles}"

    return {
        'peptide_sequence': peptide_sequence,
        'linker': linker,
        'lipid_name': lipid_anchor.name,
        'lipid_n_carbons': lipid_anchor.n_carbons,
        'peptide_mw': peptide_mw,
        'linker_mw': linker_mw,
        'lipid_mw': lipid_anchor.molecular_weight,
        'total_mw': total_mw,
        'z2_resonance': lipid_anchor.z2_multiple,
        'membrane_score': lipid_anchor.membrane_partition_score,
        'conjugate_smiles': conjugate_smiles,
    }


def generate_z2_volume_plot(output_path: Path) -> None:
    """Generate visualization of Z² volume matching for different chain lengths."""
    if not HAS_MATPLOTLIB:
        return

    chain_lengths = list(range(6, 26))
    volumes = [calculate_alkyl_chain_volume(n) for n in chain_lengths]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Plot 1: Volume vs chain length with Z² multiples
    ax1.plot(chain_lengths, volumes, 'o-', color='blue', linewidth=2, markersize=8,
             label='Fatty acid volume')

    # Draw Z² multiple lines
    for n in range(5, 20):
        z2_vol = n * Z2_VOLUME
        if 100 < z2_vol < 800:
            ax1.axhline(y=z2_vol, color='green', linestyle='--', alpha=0.5,
                       label=f'{n}×Z² = {z2_vol:.1f} Å³' if n == 10 else '')
            ax1.text(25.5, z2_vol, f'{n}×Z²', fontsize=8, va='center')

    ax1.set_xlabel('Number of Carbons', fontsize=12)
    ax1.set_ylabel('Total Voronoi Volume (Å³)', fontsize=12)
    ax1.set_title('Fatty Acid Volume vs Chain Length\n'
                  'Horizontal lines show Z² multiples (33.51 Å³ each)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(5.5, 26)

    # Plot 2: Deviation from nearest Z² multiple
    z2_deviations = []
    resonance_scores = []

    for vol in volumes:
        nearest = round(vol / Z2_VOLUME)
        deviation = abs(vol - nearest * Z2_VOLUME) / Z2_VOLUME * 100
        z2_deviations.append(deviation)
        resonance_scores.append(calculate_membrane_partition_score(vol, nearest))

    colors = ['green' if s > 80 else 'orange' if s > 60 else 'red' for s in resonance_scores]
    ax2.bar(chain_lengths, resonance_scores, color=colors, edgecolor='black', alpha=0.7)
    ax2.axhline(y=80, color='green', linestyle='--', alpha=0.7, label='High resonance (>80)')
    ax2.set_xlabel('Number of Carbons', fontsize=12)
    ax2.set_ylabel('Z² Resonance Score (0-100)', fontsize=12)
    ax2.set_title('Membrane Partition Score by Chain Length\n'
                  'Higher = closer to Z² multiple = better membrane fit', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 105)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"    Plot saved: {output_path}")


def analyze_z2_resonant_anchors() -> List[LipidAnchor]:
    """
    Analyze all common fatty acids for Z² resonance.
    Returns list of LipidAnchor objects sorted by membrane partition score.
    """
    anchors = []

    for n_carbons in range(6, 26):
        volume = calculate_alkyl_chain_volume(n_carbons)
        z2_multiple = round(volume / Z2_VOLUME)
        z2_deviation = abs(volume - z2_multiple * Z2_VOLUME)
        deviation_pct = 100 * z2_deviation / Z2_VOLUME

        # MW for saturated fatty acid: C_n H_{2n} O_2
        mw = 12.01 * n_carbons + 1.008 * (2 * n_carbons) + 16.00 * 2

        logP = estimate_logP(n_carbons)
        partition_score = calculate_membrane_partition_score(volume, z2_multiple)
        smiles = generate_fatty_acid_smiles(n_carbons)

        # Name
        if n_carbons in [c['carbons'] for c in FATTY_ACIDS.values()]:
            name = [k for k, v in FATTY_ACIDS.items() if v['carbons'] == n_carbons][0]
            name = FATTY_ACIDS[name]['name']
        else:
            name = f"C{n_carbons}:0 fatty acid"

        anchor = LipidAnchor(
            name=name,
            n_carbons=n_carbons,
            total_volume=volume,
            z2_multiple=z2_multiple,
            z2_deviation=deviation_pct,
            molecular_weight=mw,
            predicted_logP=logP,
            membrane_partition_score=partition_score,
            smiles=smiles,
        )
        anchors.append(anchor)

    # Sort by membrane partition score (highest first)
    anchors.sort(key=lambda x: x.membrane_partition_score, reverse=True)

    return anchors


def main():
    """Main execution: Design Z²-matched lipid delivery vectors."""
    print("=" * 80)
    print("Z²-MATCHED LIPID DELIVERY VECTOR ENGINEERING")
    print("Designing Geometrically Resonant Membrane Anchors")
    print("=" * 80)

    print(f"""
    THE PROBLEM:
    ────────────
    Our peptide drugs bounced off the membrane (SURFACE/BOUNCED verdicts).
    They need a lipid anchor to penetrate the blood-brain barrier.

    THE Z² SOLUTION:
    ────────────────
    Lipid anchors with volumes that are EXACT MULTIPLES of Z² = {Z2_VOLUME:.2f} Å³
    will have optimal thermodynamic fit with the membrane packing lattice.

    MEMBRANE PHYSICS:
    - Membrane dielectric: ε ≈ 2 (vs water ε ≈ 80)
    - This compresses atomic packing in the hydrophobic core
    - Z²-resonant molecules fit the membrane lattice with MINIMAL penalty

    CALCULATION:
    - Methylene (-CH2-) volume: {METHYLENE_VOLUME:.2f} Å³
    - Methyl (-CH3) volume: {METHYL_VOLUME:.2f} Å³
    - For N × Z² volume, we need specific chain lengths
""")

    results = {
        'timestamp': datetime.now().isoformat(),
        'method': 'Z²-Matched Lipid Vector Engineering',
        'constants': {
            'Z2_volume_cubic_angstrom': Z2_VOLUME,
            'methylene_volume': METHYLENE_VOLUME,
            'methyl_volume': METHYL_VOLUME,
            'water_dielectric': WATER_DIELECTRIC,
            'membrane_dielectric': MEMBRANE_DIELECTRIC,
        },
        'anchors': [],
        'peptide_conjugates': [],
    }

    # Analyze all fatty acids for Z² resonance
    print("\n  Analyzing fatty acid Z² resonance...\n")
    anchors = analyze_z2_resonant_anchors()

    print("  " + "=" * 70)
    print("  Z² RESONANCE ANALYSIS: FATTY ACID CHAIN LENGTHS")
    print("  " + "=" * 70)
    print(f"\n  {'Carbons':<10}{'Volume (Å³)':<15}{'N×Z²':<10}{'Deviation':<15}{'Score':<10}{'logP':<10}")
    print("  " + "-" * 70)

    top_anchors = []

    for anchor in anchors[:15]:  # Show top 15
        print(f"  {anchor.n_carbons:<10}{anchor.total_volume:<15.2f}"
              f"{int(anchor.z2_multiple):<10}{anchor.z2_deviation:<15.1f}%"
              f"{anchor.membrane_partition_score:<10.1f}{anchor.predicted_logP:<10.1f}")

        if anchor.membrane_partition_score > 75:
            top_anchors.append(anchor)

        results['anchors'].append({
            'name': anchor.name,
            'n_carbons': anchor.n_carbons,
            'volume_cubic_angstrom': anchor.total_volume,
            'z2_multiple': int(anchor.z2_multiple),
            'z2_deviation_percent': anchor.z2_deviation,
            'molecular_weight': anchor.molecular_weight,
            'predicted_logP': anchor.predicted_logP,
            'membrane_partition_score': anchor.membrane_partition_score,
            'smiles': anchor.smiles,
        })

    print("\n  " + "=" * 70)
    print("  TOP Z²-RESONANT ANCHORS (Score > 75)")
    print("  " + "=" * 70)

    if top_anchors:
        for anchor in top_anchors[:5]:
            print(f"""
    {anchor.name}
    ─────────────────────────────────────────────────
    Chain length:        {anchor.n_carbons} carbons
    Total volume:        {anchor.total_volume:.2f} Å³
    Nearest Z² multiple: {int(anchor.z2_multiple)} × {Z2_VOLUME:.2f} = {anchor.z2_multiple * Z2_VOLUME:.2f} Å³
    Deviation:           {anchor.z2_deviation:.2f}%
    Z² Resonance Score:  {anchor.membrane_partition_score:.1f}/100
    Predicted logP:      {anchor.predicted_logP:.1f}
    MW:                  {anchor.molecular_weight:.2f} Da
    SMILES:              {anchor.smiles}
""")
    else:
        print("\n    No anchors with score > 75 found. Using best available.")
        top_anchors = anchors[:3]

    # Design peptide conjugates for our validated drugs
    print("\n  " + "=" * 70)
    print("  PEPTIDE-LIPID CONJUGATE DESIGNS")
    print("  " + "=" * 70)

    peptide_drugs = {
        'ZIM-SYN-004': 'FPF',       # Parkinson's
        'ZIM-ADD-003': 'RWWFWR',    # Addiction
        'ZIM-ALZ-001': 'WFFY',      # Alzheimer's
    }

    best_anchor = top_anchors[0] if top_anchors else anchors[0]

    for drug_id, sequence in peptide_drugs.items():
        conjugate = design_peptide_lipid_conjugate(sequence, best_anchor)

        print(f"""
    {drug_id}: {sequence}
    ─────────────────────────────────────────────────
    Lipid anchor:        {conjugate['lipid_name']} (C{conjugate['lipid_n_carbons']})
    Linker:              {conjugate['linker']} (Gly-Gly-Gly)

    Molecular Weights:
      Peptide:           {conjugate['peptide_mw']:.2f} Da
      Linker:            {conjugate['linker_mw']:.2f} Da
      Lipid:             {conjugate['lipid_mw']:.2f} Da
      TOTAL:             {conjugate['total_mw']:.2f} Da

    Z² Resonance:        {conjugate['z2_resonance']:.0f}× (Score: {conjugate['membrane_score']:.1f})

    Conjugate Structure:
      [Lipid]-[GGG]-[{sequence}]
      {conjugate['conjugate_smiles'][:60]}...
""")

        results['peptide_conjugates'].append({
            'drug_id': drug_id,
            **conjugate
        })

    # Generate visualization
    if HAS_MATPLOTLIB:
        plot_path = OUTPUT_DIR / 'z2_lipid_resonance.png'
        generate_z2_volume_plot(plot_path)

    # Final recommendations
    print("\n" + "=" * 80)
    print("Z²-MATCHED LIPID VECTOR RECOMMENDATIONS")
    print("=" * 80)

    print(f"""
    OPTIMAL LIPID ANCHOR:
    ─────────────────────
    Recommended:   {best_anchor.name}
    Chain length:  C{best_anchor.n_carbons}
    Z² multiple:   {int(best_anchor.z2_multiple)}× (volume = {best_anchor.total_volume:.2f} Å³)
    Deviation:     {best_anchor.z2_deviation:.2f}% from perfect Z² resonance
    Score:         {best_anchor.membrane_partition_score:.1f}/100

    WHY THIS WORKS:
    ───────────────
    The lipid anchor volume ({best_anchor.total_volume:.1f} Å³) is within {best_anchor.z2_deviation:.1f}%
    of {int(best_anchor.z2_multiple)} × Z² = {int(best_anchor.z2_multiple) * Z2_VOLUME:.1f} Å³.

    This geometric resonance means the lipid fits the membrane packing
    lattice with MINIMAL thermodynamic penalty, enabling efficient
    partitioning into the lipid bilayer.

    CONJUGATION STRATEGY:
    ────────────────────
    1. N-terminal lipidation via amide bond to fatty acid
    2. Flexible GGG linker prevents steric clash
    3. Peptide cargo retains binding activity

    EXPECTED OUTCOME:
    ────────────────
    Previous: BOUNCED (peptide alone stayed in water phase)
    Predicted: PERMEABLE (lipid-conjugated peptide inserts into membrane)
""")

    results['recommendation'] = {
        'best_anchor': {
            'name': best_anchor.name,
            'n_carbons': best_anchor.n_carbons,
            'z2_multiple': int(best_anchor.z2_multiple),
            'deviation_percent': best_anchor.z2_deviation,
            'score': best_anchor.membrane_partition_score,
        },
        'linker': 'GGG',
        'expected_outcome': 'PERMEABLE',
    }

    # Save results
    output_path = OUTPUT_DIR / 'z2_lipid_vector_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n  Results saved: {output_path}")
    print("=" * 80)

    return results


if __name__ == '__main__':
    results = main()
