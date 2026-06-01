#!/usr/bin/env python3
"""
analysis_design_hotspot_alignment.py - Cross-reference Designs with Z² Hotspots

Analyzes how well designed peptides align with identified Z² hotspots
in the target binding site.

Key Questions:
1. Which designs have aromatics positioned for TRP203 stacking?
2. Do aromatic counts correlate with hotspot coverage?
3. What is the optimal aromatic spacing for Z² engagement?

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import Counter


# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z2_BIOLOGICAL = 6.015152508891966  # Å

# Aromatic residues and their properties
AROMATICS = {
    'W': {'name': 'Trp', 'ring_size': 2, 'z2_potential': 1.0, 'stacking': 'strong'},
    'Y': {'name': 'Tyr', 'ring_size': 1, 'z2_potential': 0.85, 'stacking': 'moderate'},
    'F': {'name': 'Phe', 'ring_size': 1, 'z2_potential': 0.80, 'stacking': 'moderate'},
    'H': {'name': 'His', 'ring_size': 1, 'z2_potential': 0.60, 'stacking': 'weak'},
}

# Key binding site residues from hotspot analysis
OXTR_HOTSPOT_RESIDUES = {
    'TRP203': {'z2_contacts': 188, 'rank': 1, 'type': 'aromatic'},
    'TRP99': {'z2_contacts': 114, 'rank': 2, 'type': 'aromatic'},
    'PHE91': {'z2_contacts': 93, 'rank': 3, 'type': 'aromatic'},
    'ILE313': {'z2_contacts': 82, 'rank': 4, 'type': 'hydrophobic'},
    'LEU98': {'z2_contacts': 63, 'rank': 5, 'type': 'hydrophobic'},
    'TYR209': {'z2_contacts': 49, 'rank': 8, 'type': 'aromatic'},
}

# C2_Homodimer_A Protease (1HHP) hotspot residues
HIV_PROTEASE_HOTSPOT_RESIDUES = {
    'ARG8': {'z2_contacts': 287, 'rank': 1, 'type': 'charged'},
    'PHE53': {'z2_contacts': 268, 'rank': 2, 'type': 'aromatic'},
    'ILE50': {'z2_contacts': 264, 'rank': 3, 'type': 'hydrophobic'},
    'PRO81': {'z2_contacts': 183, 'rank': 4, 'type': 'hydrophobic'},
    'ASP29': {'z2_contacts': 169, 'rank': 5, 'type': 'charged'},
    'GLY51': {'z2_contacts': 120, 'rank': 6, 'type': 'flexible'},
}

# Tau PHF6 Fibril (5O3L) hotspot residues - ELECTROSTATIC DOMINANCE
# Key discovery: Tau fibrils use charge networks, not aromatic stacking
TAU_PHF6_HOTSPOT_RESIDUES = {
    'ARG349': {'z2_contacts': 535, 'rank': 1, 'type': 'charged_positive'},
    'LYS321': {'z2_contacts': 439, 'rank': 2, 'type': 'charged_positive'},
    'LYS375': {'z2_contacts': 385, 'rank': 3, 'type': 'charged_positive'},
    'LYS340': {'z2_contacts': 375, 'rank': 4, 'type': 'charged_positive'},
    'LYS347': {'z2_contacts': 373, 'rank': 5, 'type': 'charged_positive'},
    'LYS317': {'z2_contacts': 352, 'rank': 6, 'type': 'charged_positive'},
    'PHE378': {'z2_contacts': 343, 'rank': 7, 'type': 'aromatic'},
    'VAL306': {'z2_contacts': 341, 'rank': 8, 'type': 'hydrophobic'},  # PHF6 start
    'TYR310': {'z2_contacts': 280, 'rank': 9, 'type': 'aromatic'},  # PHF6 nucleation
    'HIS329': {'z2_contacts': 250, 'rank': 10, 'type': 'aromatic'},
}

# Target-specific hotspot lookup
TARGET_HOTSPOTS = {
    'P30559': OXTR_HOTSPOT_RESIDUES,
    'P04578': HIV_PROTEASE_HOTSPOT_RESIDUES,  # C2_Homodimer_A gp120 - use protease hotspots
    'P04585': HIV_PROTEASE_HOTSPOT_RESIDUES,  # C2_Homodimer_A Protease
    'P10636': TAU_PHF6_HOTSPOT_RESIDUES,  # Tau protein
    'TAU_PHF6': TAU_PHF6_HOTSPOT_RESIDUES,  # Alias for Tau
}

# Ideal aromatic spacing for Z² stacking (in residue positions)
# At ~3.5 Å per residue (extended), Z² distance needs ~2 residue spacing
Z2_RESIDUE_SPACING = [2, 3, 4]  # Optimal spacing for Z² geometry


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_aromatic_content(sequence: str) -> Dict:
    """Analyze aromatic content of a peptide sequence."""
    aromatics = []
    positions = []

    for i, aa in enumerate(sequence):
        if aa in AROMATICS:
            aromatics.append(aa)
            positions.append(i)

    # Calculate spacings between aromatics
    spacings = []
    for i in range(len(positions) - 1):
        spacings.append(positions[i + 1] - positions[i])

    # Count Z²-optimal spacings
    z2_optimal_spacings = sum(1 for s in spacings if s in Z2_RESIDUE_SPACING)

    # Calculate total Z² potential
    z2_potential = sum(AROMATICS[aa]['z2_potential'] for aa in aromatics)

    # Trp count (most important for TRP203 stacking)
    trp_count = sequence.count('W')

    return {
        'n_aromatics': len(aromatics),
        'aromatic_residues': aromatics,
        'positions': positions,
        'spacings': spacings,
        'z2_optimal_spacings': z2_optimal_spacings,
        'z2_potential': z2_potential,
        'trp_count': trp_count,
        'tyr_count': sequence.count('Y'),
        'phe_count': sequence.count('F'),
        'aromatic_density': len(aromatics) / len(sequence) if sequence else 0
    }


def calculate_hotspot_alignment_score(aromatic_analysis: Dict,
                                      design_score: float,
                                      target: str = 'P30559',
                                      sequence: str = '') -> Dict:
    """
    Calculate how well a design aligns with Z² hotspots.

    For OXTR/C2_Homodimer_A: Scoring based on aromatic stacking
    For Tau: Scoring based on charge complementarity + aromatic cap
    """
    is_tau = target in ['P10636', 'TAU_PHF6']

    if is_tau:
        # TAU-SPECIFIC SCORING: Electrostatic dominance
        # 1. Negative charge count (for ARG349/LYS disruption) - 40%
        # 2. Aromatic count (for Tyr310 capping) - 30%
        # 3. Cage score from design - 30%

        neg_charges = sequence.count('E') + sequence.count('D')
        n_aromatics = aromatic_analysis['n_aromatics']

        # Charge score: 1-2 negative charges optimal for ARG349 disruption
        if neg_charges == 1:
            charge_score = 0.9
        elif neg_charges == 2:
            charge_score = 1.0
        elif neg_charges >= 3:
            charge_score = 0.85  # May cause solubility issues
        else:
            charge_score = 0.4  # No charge disruption

        # Aromatic score for Tyr310 cap
        if 2 <= n_aromatics <= 3:
            aromatic_score = 1.0
        elif n_aromatics == 1:
            aromatic_score = 0.7
        elif n_aromatics >= 4:
            aromatic_score = 0.8
        else:
            aromatic_score = 0.3

        # Normalize cage score (typically 0.6-1.1 range)
        normalized_design_score = (design_score - 0.5) / 0.6
        normalized_design_score = max(0, min(1, normalized_design_score))

        alignment_score = (
            0.40 * charge_score +
            0.30 * aromatic_score +
            0.30 * normalized_design_score
        )

        return {
            'alignment_score': alignment_score,
            'charge_score': charge_score,
            'aromatic_score': aromatic_score,
            'design_score_normalized': normalized_design_score,
            'hotspot_engagement': f'ARG349/LYS ({neg_charges} charges)' if neg_charges > 0 else 'TYR310 only',
            'mechanism': 'ELECTROSTATIC DISRUPTION' if neg_charges > 0 else 'AROMATIC CAP'
        }

    # STANDARD SCORING (OXTR/C2_Homodimer_A): Aromatic stacking dominance
    # 1. Trp count (for TRP203 stacking) - 40%
    # 2. Z²-optimal spacing - 25%
    # 3. Total aromatic count - 20%
    # 4. Original design score - 15%

    trp_count = aromatic_analysis['trp_count']
    if trp_count == 2:
        trp_score = 1.0
    elif trp_count == 1:
        trp_score = 0.7
    elif trp_count == 3:
        trp_score = 0.8  # Slight penalty for crowding
    elif trp_count >= 4:
        trp_score = 0.6
    else:
        trp_score = 0.3  # No Trp = poor TRP203 engagement

    # Spacing score: Z²-optimal spacings enable proper geometry
    n_aromatics = aromatic_analysis['n_aromatics']
    max_possible_spacings = max(0, n_aromatics - 1)
    if max_possible_spacings > 0:
        spacing_score = aromatic_analysis['z2_optimal_spacings'] / max_possible_spacings
    else:
        spacing_score = 0.5  # Neutral if only 1 aromatic

    # Aromatic count score: 3-4 aromatics is optimal for OXTR
    if 3 <= n_aromatics <= 4:
        aromatic_score = 1.0
    elif n_aromatics == 2:
        aromatic_score = 0.8
    elif n_aromatics == 5:
        aromatic_score = 0.85
    elif n_aromatics >= 6:
        aromatic_score = 0.7  # Too many may cause aggregation
    else:
        aromatic_score = 0.5

    # Normalize design score (typically 55-65 range)
    normalized_design_score = (design_score - 45) / 20  # Map 45-65 to 0-1
    normalized_design_score = max(0, min(1, normalized_design_score))

    # Weighted combination
    alignment_score = (
        0.40 * trp_score +
        0.25 * spacing_score +
        0.20 * aromatic_score +
        0.15 * normalized_design_score
    )

    return {
        'alignment_score': alignment_score,
        'trp_score': trp_score,
        'spacing_score': spacing_score,
        'aromatic_score': aromatic_score,
        'design_score_normalized': normalized_design_score,
        'hotspot_engagement': 'TRP203' if trp_count >= 1 else 'PHE91/TYR209'
    }


def predict_binding_mode(aromatic_analysis: Dict, target: str = 'P30559',
                        sequence: str = '') -> str:
    """Predict how the peptide will engage the binding site."""
    trp = aromatic_analysis['trp_count']
    tyr = aromatic_analysis['tyr_count']
    phe = aromatic_analysis['phe_count']
    spacings = aromatic_analysis['spacings']

    # Count negative charges for Tau (E, D)
    neg_charges = sequence.count('E') + sequence.count('D')

    # C2_Homodimer_A Protease has PHE53 as main aromatic (not Trp)
    is_hiv = target in ['P04578', 'P04585']

    # Tau PHF6 uses electrostatic networks - charge complementarity is key
    is_tau = target in ['P10636', 'TAU_PHF6']

    if is_tau:
        # Tau-specific binding modes
        n_aromatics = trp + tyr + phe
        if n_aromatics >= 2 and neg_charges >= 1:
            return f"DUAL MECHANISM: Aromatic cap on Tyr310 + {neg_charges} charge(s) disrupt ARG349/LYS network"
        elif n_aromatics >= 2 and neg_charges == 0:
            return "AROMATIC CAGE: Caps Tyr310 nucleation site (add E/D for ARG349 engagement)"
        elif n_aromatics == 1 and neg_charges >= 2:
            return f"CHARGE DISRUPTOR: {neg_charges} negative charges target ARG349/LYS clusters"
        elif n_aromatics == 1 and neg_charges == 1:
            return "SINGLE ANCHOR + CHARGE: Partial Tyr310 cap with electrostatic disruption"
        elif neg_charges >= 1:
            return f"ELECTROSTATIC ONLY: {neg_charges} charge(s) disrupt fibril network"
        else:
            return "HYDROPHOBIC CAP: Beta-strand mimic blocks steric zipper"

    if trp >= 2:
        if any(s in [2, 3] for s in spacings):
            if is_hiv:
                return "DUAL TRP CLAMP: Both Trp stack with PHE53/ILE50 at Z² distance"
            return "DUAL TRP CLAMP: Both Trp residues stack with TRP203/TRP99 at Z² distance"
        else:
            if is_hiv:
                return "DUAL TRP SEQUENTIAL: Trp residues engage PHE53 and flap region"
            return "DUAL TRP SEQUENTIAL: Trp residues engage TRP203 and PHE91 sequentially"
    elif trp == 1 and (tyr >= 1 or phe >= 1):
        if is_hiv:
            return "TRP-ANCHOR + AROMATIC: Trp stacks with PHE53, Tyr/Phe engages ARG8"
        return "TRP-ANCHOR + AROMATIC: Trp stacks with TRP203, Tyr/Phe engages TRP99"
    elif trp == 1:
        if is_hiv:
            return "SINGLE TRP ANCHOR: Primary engagement with PHE53 only"
        return "SINGLE TRP ANCHOR: Primary engagement with TRP203 only"
    elif phe >= 2:
        if is_hiv:
            return "PHE NETWORK: Phe-Phe stacking with PHE53 aromatic cluster"
        return "TYR/PHE NETWORK: Multiple weaker contacts with aromatic cluster"
    elif tyr >= 2 or phe >= 1:
        return "TYR/PHE NETWORK: Multiple weaker contacts with aromatic cluster"
    else:
        return "MINIMAL AROMATIC: Limited Z² hotspot engagement"


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_alignment_analysis(designs_file: str,
                          hotspots_file: str = None,
                          output_dir: str = "../design_alignment") -> None:
    """
    Cross-reference designs with Z² hotspots.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load designs
    with open(designs_file) as f:
        design_data = json.load(f)

    designs = design_data.get('designs', [])
    uniprot = design_data.get('target_uniprot', 'P30559')

    # Get target-specific hotspots
    hotspot_residues = TARGET_HOTSPOTS.get(uniprot, OXTR_HOTSPOT_RESIDUES)

    # Determine target name
    target_names = {
        'P30559': 'Oxytocin Receptor',
        'P04578': 'C2_Homodimer_A gp120 / Protease',
        'P04585': 'C2_Homodimer_A Protease',
        'P10636': 'Tau PHF6 Fibril (Alzheimer\'s)',
        'TAU_PHF6': 'Tau PHF6 Fibril (Alzheimer\'s)',
    }
    target_name = target_names.get(uniprot, uniprot)
    is_tau = uniprot in ['P10636', 'TAU_PHF6']

    print("=" * 80)
    print("Z² DESIGN-HOTSPOT ALIGNMENT ANALYSIS")
    print("=" * 80)
    print(f"    Target: {target_name} ({uniprot})")
    print(f"    Designs to analyze: {len(designs)}")
    print()
    print("    KEY HOTSPOT RESIDUES (from atomic analysis):")
    print("    ─" * 30)
    for res, data in sorted(hotspot_residues.items(), key=lambda x: x[1]['rank']):
        print(f"      {data['rank']}. {res}: {data['z2_contacts']} Z² contacts ({data['type']})")
    print()

    # Analyze each design
    results = []

    for design in designs:
        seq = design['sequence']
        design_id = design['id']
        # Handle different score field names
        combined_score = design.get('combined_score', design.get('cage_score', 50))
        predicted_kd = design.get('predicted_kd_nm', design.get('predicted_ki_um', 1) * 1000)

        # Aromatic analysis
        aromatic = analyze_aromatic_content(seq)

        # Hotspot alignment (pass target and sequence for Tau scoring)
        alignment = calculate_hotspot_alignment_score(aromatic, combined_score, uniprot, seq)

        # Binding mode prediction
        binding_mode = predict_binding_mode(aromatic, uniprot, seq)

        # Build result entry
        result_entry = {
            'design_id': design_id,
            'sequence': seq,
            'length': len(seq),
            'n_aromatics': aromatic['n_aromatics'],
            'trp_count': aromatic['trp_count'],
            'aromatic_residues': ''.join(aromatic['aromatic_residues']),
            'spacings': aromatic['spacings'],
            'z2_optimal_spacings': aromatic['z2_optimal_spacings'],
            'z2_potential': aromatic['z2_potential'],
            'alignment_score': alignment['alignment_score'],
            'predicted_kd_nm': predicted_kd,
            'combined_score': combined_score,
            'binding_mode': binding_mode,
            'hotspot_engagement': alignment['hotspot_engagement']
        }

        # Add Tau-specific fields
        if is_tau:
            result_entry['neg_charges'] = seq.count('E') + seq.count('D')
            result_entry['charge_score'] = alignment.get('charge_score', 0)
            result_entry['mechanism'] = alignment.get('mechanism', 'UNKNOWN')
        else:
            result_entry['trp_score'] = alignment.get('trp_score', 0)

        results.append(result_entry)

    # Sort by alignment score
    results.sort(key=lambda x: x['alignment_score'], reverse=True)

    # Print results
    print("    DESIGN ALIGNMENT RANKING (sorted by hotspot alignment)")
    print("    " + "=" * 76)

    if is_tau:
        print(f"    {'Rank':<5}{'ID':<14}{'Sequence':<10}{'E/D':<4}{'Arom':<5}{'Align':<7}{'Ki(μM)':<8}{'Mechanism'}")
        print("    " + "-" * 76)
        for i, r in enumerate(results):
            seq_display = r['sequence'][:8] + ".." if len(r['sequence']) > 8 else r['sequence']
            ki_um = r['predicted_kd_nm'] / 1000  # Convert to μM
            print(f"    {i+1:<5}{r['design_id']:<14}{seq_display:<10}{r['neg_charges']:<4}{r['n_aromatics']:<5}{r['alignment_score']:.3f}  {ki_um:<8.1f}{r['mechanism'][:25]}")
    else:
        print(f"    {'Rank':<5}{'ID':<12}{'Sequence':<15}{'Trp':<4}{'Arom':<5}{'Align':<7}{'Kd(nM)':<8}{'Binding Mode'}")
        print("    " + "-" * 76)
        for i, r in enumerate(results):
            seq_display = r['sequence'][:12] + "..." if len(r['sequence']) > 12 else r['sequence']
            print(f"    {i+1:<5}{r['design_id']:<12}{seq_display:<15}{r['trp_count']:<4}{r['n_aromatics']:<5}{r['alignment_score']:.3f}  {r['predicted_kd_nm']:<8}{r['binding_mode'][:30]}")

    # Top designs summary
    print()
    print("    " + "=" * 76)
    if is_tau:
        print("    TOP 5 DESIGNS FOR ARG349/LYS NETWORK DISRUPTION")
    else:
        print("    TOP 5 DESIGNS FOR TRP203 ENGAGEMENT")
    print("    " + "=" * 76)

    for i, r in enumerate(results[:5]):
        if is_tau:
            ki_um = r['predicted_kd_nm'] / 1000
            print(f"""
    {i+1}. {r['design_id']}: {r['sequence']}
       ├─ Aromatics: {r['aromatic_residues']} | Negative charges: {r['neg_charges']} (E/D)
       ├─ Charge Score: {r['charge_score']:.2f} | Alignment Score: {r['alignment_score']:.3f}
       ├─ Predicted Ki: {ki_um:.1f} μM
       └─ Mechanism: {r['mechanism']} → {r['binding_mode']}""")
        else:
            print(f"""
    {i+1}. {r['design_id']}: {r['sequence']}
       ├─ Aromatics: {r['aromatic_residues']} (positions create spacings: {r['spacings']})
       ├─ Z² Potential: {r['z2_potential']:.2f} | Alignment Score: {r['alignment_score']:.3f}
       ├─ Predicted Kd: {r['predicted_kd_nm']} nM
       └─ Mode: {r['binding_mode']}""")

    # Worst designs (for comparison)
    print()
    print("    " + "-" * 76)
    print("    BOTTOM 3 DESIGNS (limited hotspot engagement)")
    print("    " + "-" * 76)

    for r in results[-3:]:
        print(f"    {r['design_id']}: {r['sequence']}")
        print(f"       └─ Only {r['trp_count']} Trp, {r['n_aromatics']} aromatics → {r['binding_mode']}")

    # Statistics
    print()
    print("    " + "=" * 76)
    if is_tau:
        print("    CHARGE COMPLEMENTARITY STATISTICS")
    else:
        print("    AROMATIC STATISTICS ACROSS ALL DESIGNS")
    print("    " + "=" * 76)

    trp_counts = Counter(r['trp_count'] for r in results)
    arom_counts = Counter(r['n_aromatics'] for r in results)

    if is_tau:
        charge_counts = Counter(r['neg_charges'] for r in results)
        print(f"    Negative charge (E/D) distribution: {dict(charge_counts)}")
        print(f"    Aromatic distribution: {dict(arom_counts)}")
        print(f"    Mean alignment score: {sum(r['alignment_score'] for r in results)/len(results):.3f}")
        print(f"    Best alignment: {results[0]['design_id']} ({results[0]['alignment_score']:.3f})")

        # Charge correlation analysis
        dual_charge = [r for r in results if r['neg_charges'] >= 2]
        single_charge = [r for r in results if r['neg_charges'] == 1]
        no_charge = [r for r in results if r['neg_charges'] == 0]

        print()
        print("    CHARGE COUNT vs PREDICTED BINDING:")
        if dual_charge:
            avg_ki = sum(r['predicted_kd_nm'] for r in dual_charge) / len(dual_charge) / 1000
            print(f"      2+ charges ({len(dual_charge)} designs): Mean Ki = {avg_ki:.2f} μM")
        if single_charge:
            avg_ki = sum(r['predicted_kd_nm'] for r in single_charge) / len(single_charge) / 1000
            print(f"      1 charge ({len(single_charge)} designs):  Mean Ki = {avg_ki:.2f} μM")
        if no_charge:
            avg_ki = sum(r['predicted_kd_nm'] for r in no_charge) / len(no_charge) / 1000
            print(f"      0 charges ({len(no_charge)} designs): Mean Ki = {avg_ki:.2f} μM")

        # Dual mechanism analysis
        print()
        print("    DUAL MECHANISM (Aromatic + Charge) DESIGNS:")
        dual_mech = [r for r in results if r['n_aromatics'] >= 2 and r['neg_charges'] >= 1]
        if dual_mech:
            avg_score = sum(r['alignment_score'] for r in dual_mech) / len(dual_mech)
            print(f"      {len(dual_mech)} designs with both aromatic cap AND charge disruption")
            print(f"      Mean alignment: {avg_score:.3f}")
            print(f"      Best: {dual_mech[0]['design_id']} ({dual_mech[0]['sequence']})")
    else:
        print(f"    Trp distribution: {dict(trp_counts)}")
        print(f"    Total aromatic distribution: {dict(arom_counts)}")
        print(f"    Mean alignment score: {sum(r['alignment_score'] for r in results)/len(results):.3f}")
        print(f"    Best alignment: {results[0]['design_id']} ({results[0]['alignment_score']:.3f})")

        # Correlation analysis
        dual_trp = [r for r in results if r['trp_count'] >= 2]
        single_trp = [r for r in results if r['trp_count'] == 1]
        no_trp = [r for r in results if r['trp_count'] == 0]

        print()
        print("    TRP COUNT vs PREDICTED BINDING:")
        if dual_trp:
            avg_kd_dual = sum(r['predicted_kd_nm'] for r in dual_trp) / len(dual_trp)
            print(f"      2+ Trp ({len(dual_trp)} designs): Mean Kd = {avg_kd_dual:.0f} nM")
        if single_trp:
            avg_kd_single = sum(r['predicted_kd_nm'] for r in single_trp) / len(single_trp)
            print(f"      1 Trp ({len(single_trp)} designs):  Mean Kd = {avg_kd_single:.0f} nM")
        if no_trp:
            avg_kd_none = sum(r['predicted_kd_nm'] for r in no_trp) / len(no_trp)
            print(f"      0 Trp ({len(no_trp)} designs):  Mean Kd = {avg_kd_none:.0f} nM")

    print()
    print("=" * 80)

    # Save results
    output_file = output_path / f"design_alignment_{uniprot}.json"

    with open(output_file, 'w') as f:
        output_data = {
            'target_uniprot': uniprot,
            'target_name': target_name,
            'hotspot_residues': hotspot_residues,
            'z2_distance': Z2_BIOLOGICAL,
            'designs_analyzed': len(results),
            'results': results,
            'statistics': {
                'aromatic_distribution': dict(arom_counts),
                'mean_alignment_score': sum(r['alignment_score'] for r in results)/len(results)
            }
        }
        if is_tau:
            output_data['statistics']['charge_distribution'] = dict(charge_counts)
            output_data['mechanism'] = 'ELECTROSTATIC DISRUPTION'
        else:
            output_data['statistics']['trp_distribution'] = dict(trp_counts)
            output_data['mechanism'] = 'AROMATIC STACKING'

        json.dump(output_data, f, indent=2)

    print(f"    Saved: {output_file}")

    return results


# =============================================================================
# CLI
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-reference Z² designs with hotspot analysis"
    )
    parser.add_argument('--designs',
                       default='../validated_designs/z2_design_P30559.json',
                       help='Path to designs JSON')
    parser.add_argument('--output', default='../design_alignment',
                       help='Output directory')

    args = parser.parse_args()

    run_alignment_analysis(
        designs_file=args.designs,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
