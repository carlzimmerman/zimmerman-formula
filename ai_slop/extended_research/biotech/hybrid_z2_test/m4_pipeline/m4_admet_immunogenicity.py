#!/usr/bin/env python3
"""
Z² ADMET & Immunogenicity Validation

SPDX-License-Identifier: AGPL-3.0-or-later

RED TEAM PROTOCOL - Vulnerability 4: "Immunogenic Reality"

Tests whether the Z² designed protein is therapeutically viable:

1. IMMUNOGENICITY PREDICTION
   - T-cell epitope prediction (MHC binding)
   - B-cell epitope prediction (surface accessibility)
   - Human similarity scoring

2. BBB PERMEABILITY
   - Molecular weight analysis
   - Charge distribution
   - Lipophilicity estimation

3. ADMET PROPERTIES
   - Aggregation propensity
   - Protease susceptibility
   - Solubility prediction

CRITICAL REALITY CHECK:
- Beautiful geometry means NOTHING if the immune system destroys it
- Therapeutic proteins must evade immune surveillance
- Novel sequences are often highly immunogenic

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
# Z² CONSTANTS
# ==============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103

# ==============================================================================
# AMINO ACID PROPERTIES
# ==============================================================================

# Hydrophobicity (Kyte-Doolittle scale)
HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# MHC-I binding propensity (simplified anchor residues)
MHC_I_ANCHORS = {
    'L': 1.5, 'M': 1.3, 'I': 1.4, 'V': 1.3, 'F': 1.2,
    'Y': 1.1, 'A': 1.0, 'K': 0.8, 'R': 0.7, 'other': 0.5
}

# MHC-II binding propensity
MHC_II_ANCHORS = {
    'L': 1.4, 'I': 1.3, 'V': 1.2, 'M': 1.1, 'F': 1.3,
    'Y': 1.2, 'W': 1.1, 'A': 0.9, 'other': 0.6
}

# B-cell epitope accessibility weights
ACCESSIBILITY = {
    'K': 1.8, 'R': 1.7, 'D': 1.6, 'E': 1.6, 'N': 1.4,
    'Q': 1.3, 'S': 1.2, 'T': 1.1, 'H': 1.3, 'G': 1.1,
    'P': 1.0, 'A': 0.8, 'M': 0.7, 'C': 0.6, 'F': 0.5,
    'Y': 0.6, 'W': 0.4, 'L': 0.3, 'I': 0.3, 'V': 0.4
}

# Aggregation propensity (Tango-like)
AGGREGATION = {
    'I': 1.8, 'V': 1.6, 'L': 1.4, 'F': 1.5, 'Y': 1.3,
    'M': 1.1, 'W': 1.2, 'A': 0.9, 'C': 1.0, 'G': 0.7,
    'T': 0.6, 'S': 0.5, 'N': 0.4, 'Q': 0.4, 'H': 0.5,
    'K': 0.2, 'R': 0.2, 'D': 0.1, 'E': 0.1, 'P': 0.3
}

# Protease cleavage sites (simplified)
PROTEASE_SITES = {
    'trypsin': ['K', 'R'],
    'chymotrypsin': ['F', 'Y', 'W'],
    'pepsin': ['F', 'L', 'W', 'Y'],
    'cathepsin': ['R', 'K', 'L', 'F']
}


def parse_pdb_sequence(pdb_file: str) -> Tuple[str, np.ndarray]:
    """Extract sequence and Cα coordinates from PDB."""
    aa_map = {
        'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
        'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
        'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
        'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
    }

    sequence = []
    coords = []
    seen_res = set()

    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_num = int(line[22:26])
                res_name = line[17:20].strip()

                if res_num not in seen_res:
                    seen_res.add(res_num)
                    aa = aa_map.get(res_name, 'X')
                    sequence.append(aa)

                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    coords.append([x, y, z])

    return ''.join(sequence), np.array(coords)


def predict_mhc_i_epitopes(sequence: str, window: int = 9) -> List[Dict]:
    """Predict MHC-I T-cell epitopes (9-mer peptides)."""
    epitopes = []

    for i in range(len(sequence) - window + 1):
        peptide = sequence[i:i+window]

        # Score based on anchor positions (P2, P9 for MHC-I)
        score = 0
        if len(peptide) >= 2:
            p2 = peptide[1]
            p9 = peptide[-1]
            score += MHC_I_ANCHORS.get(p2, MHC_I_ANCHORS['other'])
            score += MHC_I_ANCHORS.get(p9, MHC_I_ANCHORS['other'])

        # Hydrophobic core bonus
        core_hydro = np.mean([HYDROPHOBICITY.get(aa, 0) for aa in peptide[2:7]])
        if core_hydro > 1.0:
            score += 0.5

        if score > 2.0:  # Threshold for potential epitope
            epitopes.append({
                'start': i,
                'end': i + window,
                'peptide': peptide,
                'mhc_i_score': float(score),
                'risk': 'high' if score > 2.5 else 'medium'
            })

    return sorted(epitopes, key=lambda x: -x['mhc_i_score'])[:10]


def predict_mhc_ii_epitopes(sequence: str, window: int = 15) -> List[Dict]:
    """Predict MHC-II T-cell epitopes (15-mer peptides)."""
    epitopes = []

    for i in range(len(sequence) - window + 1):
        peptide = sequence[i:i+window]

        # Score based on anchor positions (P1, P4, P6, P9 for MHC-II)
        score = 0
        anchors = [0, 3, 5, 8]
        for pos in anchors:
            if pos < len(peptide):
                aa = peptide[pos]
                score += MHC_II_ANCHORS.get(aa, MHC_II_ANCHORS['other'])

        # Charged residues in flanking regions reduce binding
        flanks = peptide[:3] + peptide[-3:]
        charge_penalty = sum(1 for aa in flanks if aa in 'DEKR')
        score -= charge_penalty * 0.1

        if score > 3.5:  # Threshold for potential epitope
            epitopes.append({
                'start': i,
                'end': i + window,
                'peptide': peptide,
                'mhc_ii_score': float(score),
                'risk': 'high' if score > 4.0 else 'medium'
            })

    return sorted(epitopes, key=lambda x: -x['mhc_ii_score'])[:10]


def predict_b_cell_epitopes(sequence: str, coords: np.ndarray,
                            window: int = 6) -> List[Dict]:
    """Predict linear B-cell epitopes based on surface accessibility."""
    epitopes = []

    # Calculate SASA-like scores (simplified)
    if len(coords) > 0:
        # Use distance to center as proxy for surface accessibility
        center = np.mean(coords, axis=0)
        distances = np.linalg.norm(coords - center, axis=1)
        max_dist = np.max(distances)
        surface_scores = distances / max_dist if max_dist > 0 else np.ones(len(coords))
    else:
        surface_scores = np.ones(len(sequence))

    for i in range(len(sequence) - window + 1):
        peptide = sequence[i:i+window]

        # Base accessibility score
        access_score = np.mean([ACCESSIBILITY.get(aa, 0.5) for aa in peptide])

        # Surface position bonus
        if i + window <= len(surface_scores):
            surface_bonus = np.mean(surface_scores[i:i+window])
        else:
            surface_bonus = 0.5

        # Charged residues are often B-cell epitopes
        charge_bonus = sum(1 for aa in peptide if aa in 'DEKRH') * 0.1

        total_score = access_score + surface_bonus + charge_bonus

        if total_score > 2.5:
            epitopes.append({
                'start': i,
                'end': i + window,
                'peptide': peptide,
                'b_cell_score': float(total_score),
                'surface_exposure': float(surface_bonus),
                'risk': 'high' if total_score > 3.0 else 'medium'
            })

    return sorted(epitopes, key=lambda x: -x['b_cell_score'])[:10]


def calculate_human_similarity(sequence: str) -> Dict:
    """Estimate similarity to human proteome (simplified)."""
    # Common human protein motifs
    human_motifs = [
        'ALKS', 'VLSA', 'LGAG', 'GAGA', 'EEKK', 'DKDK',
        'LLLL', 'AAAA', 'GLGL', 'VIVI', 'MEFS', 'SMEL'
    ]

    motif_matches = 0
    for motif in human_motifs:
        if motif in sequence:
            motif_matches += 1

    # Calculate compositional similarity
    human_composition = {
        'L': 0.099, 'A': 0.074, 'G': 0.071, 'V': 0.065, 'S': 0.068,
        'E': 0.062, 'I': 0.053, 'K': 0.058, 'R': 0.053, 'D': 0.055,
        'T': 0.057, 'P': 0.048, 'N': 0.043, 'F': 0.040, 'Q': 0.040,
        'Y': 0.032, 'M': 0.024, 'H': 0.023, 'C': 0.019, 'W': 0.012
    }

    # Calculate sequence composition
    seq_composition = {}
    for aa in sequence:
        seq_composition[aa] = seq_composition.get(aa, 0) + 1

    for aa in seq_composition:
        seq_composition[aa] /= len(sequence)

    # Jensen-Shannon divergence (simplified)
    jsd = 0
    for aa in human_composition:
        p = seq_composition.get(aa, 0.001)
        q = human_composition[aa]
        m = (p + q) / 2
        if p > 0 and m > 0:
            jsd += p * np.log2(p / m)

    similarity_score = 1 - min(jsd / 2, 1)  # Normalize to 0-1

    return {
        'similarity_score': float(similarity_score),
        'motif_matches': motif_matches,
        'assessment': 'low_risk' if similarity_score > 0.8 else 'medium_risk' if similarity_score > 0.6 else 'high_risk'
    }


def predict_aggregation(sequence: str) -> Dict:
    """Predict aggregation propensity (Tango-like)."""
    # Calculate per-residue aggregation scores
    scores = [AGGREGATION.get(aa, 0.5) for aa in sequence]

    # Identify aggregation-prone regions (APRs)
    aprs = []
    window = 7
    threshold = 1.0

    for i in range(len(sequence) - window + 1):
        window_score = np.mean(scores[i:i+window])
        if window_score > threshold:
            aprs.append({
                'start': i,
                'end': i + window,
                'region': sequence[i:i+window],
                'score': float(window_score)
            })

    # Merge overlapping APRs
    merged_aprs = []
    for apr in sorted(aprs, key=lambda x: x['start']):
        if merged_aprs and apr['start'] <= merged_aprs[-1]['end']:
            merged_aprs[-1]['end'] = max(merged_aprs[-1]['end'], apr['end'])
            merged_aprs[-1]['score'] = max(merged_aprs[-1]['score'], apr['score'])
        else:
            merged_aprs.append(apr)

    mean_score = np.mean(scores)
    max_score = max(scores) if scores else 0

    return {
        'mean_aggregation_score': float(mean_score),
        'max_aggregation_score': float(max_score),
        'n_aprs': len(merged_aprs),
        'aprs': merged_aprs[:5],
        'risk': 'high' if len(merged_aprs) > 3 or max_score > 1.5 else 'medium' if len(merged_aprs) > 1 else 'low'
    }


def predict_protease_susceptibility(sequence: str) -> Dict:
    """Predict susceptibility to common proteases."""
    susceptibility = {}

    for protease, sites in PROTEASE_SITES.items():
        cleavage_positions = []
        for i, aa in enumerate(sequence):
            if aa in sites:
                # Check for accessible positions (simplified)
                cleavage_positions.append(i)

        susceptibility[protease] = {
            'n_sites': len(cleavage_positions),
            'positions': cleavage_positions[:10],  # First 10
            'density': len(cleavage_positions) / len(sequence)
        }

    # Overall stability assessment
    total_sites = sum(v['n_sites'] for v in susceptibility.values())
    site_density = total_sites / len(sequence)

    return {
        'proteases': susceptibility,
        'total_cleavage_sites': total_sites,
        'site_density': float(site_density),
        'stability': 'high' if site_density < 0.1 else 'medium' if site_density < 0.2 else 'low'
    }


def predict_bbb_permeability(sequence: str) -> Dict:
    """Predict blood-brain barrier permeability."""
    # MW estimation (average AA MW ~110 Da)
    mw = len(sequence) * 110

    # Charge at physiological pH
    positive = sum(1 for aa in sequence if aa in 'KRH')
    negative = sum(1 for aa in sequence if aa in 'DE')
    net_charge = positive - negative

    # Hydrophobicity
    mean_hydro = np.mean([HYDROPHOBICITY.get(aa, 0) for aa in sequence])

    # Lipophilicity (simplified logP)
    logp_estimate = mean_hydro * 0.5

    # BBB permeability rules
    # - MW < 500 Da preferred (IMPOSSIBLE for proteins)
    # - Low charge preferred
    # - Moderate lipophilicity

    # For proteins, BBB crossing is essentially impossible without:
    # - Receptor-mediated transcytosis
    # - Cell-penetrating peptides
    # - Nanoparticle delivery

    permeability_score = 0
    if mw < 5000:  # Very small proteins
        permeability_score += 0.2
    if abs(net_charge) < 5:
        permeability_score += 0.1
    if -1 < mean_hydro < 2:
        permeability_score += 0.1

    return {
        'molecular_weight': mw,
        'net_charge': net_charge,
        'mean_hydrophobicity': float(mean_hydro),
        'logp_estimate': float(logp_estimate),
        'permeability_score': float(permeability_score),
        'can_cross_bbb': permeability_score > 0.3,
        'delivery_required': 'receptor_mediated_transcytosis' if mw > 500 else 'direct',
        'note': 'Proteins cannot passively cross BBB. Requires specialized delivery system.'
    }


def calculate_overall_immunogenicity(mhc_i: List, mhc_ii: List, b_cell: List,
                                     human_sim: Dict) -> Dict:
    """Calculate overall immunogenicity risk."""
    # Count high-risk epitopes
    high_risk_t_cell = (
        sum(1 for e in mhc_i if e['risk'] == 'high') +
        sum(1 for e in mhc_ii if e['risk'] == 'high')
    )
    high_risk_b_cell = sum(1 for e in b_cell if e['risk'] == 'high')

    # Calculate composite score
    t_cell_score = high_risk_t_cell * 2 + len(mhc_i) + len(mhc_ii)
    b_cell_score = high_risk_b_cell * 2 + len(b_cell)

    # Human similarity bonus
    similarity_bonus = human_sim['similarity_score'] * 10

    total_risk = t_cell_score + b_cell_score - similarity_bonus

    if total_risk > 30:
        risk_level = 'CRITICAL'
        recommendation = 'Major immunogenic hotspots. Requires extensive humanization or peptide modification.'
    elif total_risk > 20:
        risk_level = 'HIGH'
        recommendation = 'Multiple immunogenic regions. Consider epitope removal or masking strategies.'
    elif total_risk > 10:
        risk_level = 'MODERATE'
        recommendation = 'Some immunogenic potential. May require immune tolerance protocols.'
    else:
        risk_level = 'LOW'
        recommendation = 'Acceptable immunogenic profile for therapeutic development.'

    return {
        'immunogenicity_score': float(total_risk),
        'risk_level': risk_level,
        't_cell_epitopes': len(mhc_i) + len(mhc_ii),
        'b_cell_epitopes': len(b_cell),
        'high_risk_regions': high_risk_t_cell + high_risk_b_cell,
        'human_similarity': human_sim['similarity_score'],
        'recommendation': recommendation
    }


def create_visualization(results: Dict, output_dir: str):
    """Create visualization of ADMET results."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  Warning: matplotlib not available")
        return

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    sequence = results['sequence']

    # 1. MHC-I epitope landscape
    ax1 = axes[0, 0]
    epitope_profile = np.zeros(len(sequence))
    for e in results['mhc_i_epitopes']:
        epitope_profile[e['start']:e['end']] = e['mhc_i_score']
    ax1.fill_between(range(len(sequence)), epitope_profile, alpha=0.7, color='red')
    ax1.axhline(y=2.0, color='black', linestyle='--', label='Risk threshold')
    ax1.set_xlabel('Residue')
    ax1.set_ylabel('MHC-I Score')
    ax1.set_title('T-Cell Epitope Landscape (MHC-I)')
    ax1.legend()

    # 2. MHC-II epitope landscape
    ax2 = axes[0, 1]
    epitope_profile = np.zeros(len(sequence))
    for e in results['mhc_ii_epitopes']:
        epitope_profile[e['start']:e['end']] = e['mhc_ii_score']
    ax2.fill_between(range(len(sequence)), epitope_profile, alpha=0.7, color='orange')
    ax2.axhline(y=3.5, color='black', linestyle='--', label='Risk threshold')
    ax2.set_xlabel('Residue')
    ax2.set_ylabel('MHC-II Score')
    ax2.set_title('T-Cell Epitope Landscape (MHC-II)')
    ax2.legend()

    # 3. B-cell epitope landscape
    ax3 = axes[0, 2]
    epitope_profile = np.zeros(len(sequence))
    for e in results['b_cell_epitopes']:
        epitope_profile[e['start']:e['end']] = e['b_cell_score']
    ax3.fill_between(range(len(sequence)), epitope_profile, alpha=0.7, color='blue')
    ax3.axhline(y=2.5, color='black', linestyle='--', label='Risk threshold')
    ax3.set_xlabel('Residue')
    ax3.set_ylabel('B-Cell Score')
    ax3.set_title('B-Cell Epitope Landscape')
    ax3.legend()

    # 4. Aggregation profile
    ax4 = axes[1, 0]
    agg_scores = [AGGREGATION.get(aa, 0.5) for aa in sequence]
    colors = ['red' if s > 1.0 else 'orange' if s > 0.7 else 'green' for s in agg_scores]
    ax4.bar(range(len(sequence)), agg_scores, color=colors, width=1.0)
    ax4.axhline(y=1.0, color='black', linestyle='--', label='APR threshold')
    ax4.set_xlabel('Residue')
    ax4.set_ylabel('Aggregation Score')
    ax4.set_title('Aggregation Propensity Profile')
    ax4.legend()

    # 5. Risk summary radar
    ax5 = axes[1, 1]
    ax5.axis('off')

    immuno = results['overall_immunogenicity']
    risk_color = {'CRITICAL': 'red', 'HIGH': 'orange', 'MODERATE': 'yellow', 'LOW': 'green'}

    text = f"""
    IMMUNOGENICITY ASSESSMENT
    {'='*40}

    Risk Level: {immuno['risk_level']}
    Score: {immuno['immunogenicity_score']:.1f}

    T-Cell Epitopes: {immuno['t_cell_epitopes']}
    B-Cell Epitopes: {immuno['b_cell_epitopes']}
    High-Risk Regions: {immuno['high_risk_regions']}

    Human Similarity: {immuno['human_similarity']:.2f}

    Recommendation:
    {immuno['recommendation'][:100]}...
    """

    ax5.text(0.1, 0.9, text, transform=ax5.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round',
                       facecolor=risk_color.get(immuno['risk_level'], 'gray'),
                       alpha=0.3))

    # 6. BBB and stability summary
    ax6 = axes[1, 2]
    ax6.axis('off')

    bbb = results['bbb_permeability']
    agg = results['aggregation']
    prot = results['protease_susceptibility']

    text = f"""
    ADMET PROPERTIES
    {'='*40}

    BBB PERMEABILITY
    MW: {bbb['molecular_weight']} Da
    Net Charge: {bbb['net_charge']:+d}
    Can Cross: {'Yes' if bbb['can_cross_bbb'] else 'No (requires delivery)'}

    AGGREGATION
    Risk: {agg['risk'].upper()}
    APRs: {agg['n_aprs']}

    PROTEASE STABILITY
    Stability: {prot['stability'].upper()}
    Cleavage Sites: {prot['total_cleavage_sites']}
    """

    ax6.text(0.1, 0.9, text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    plt.suptitle('Z² Protein ADMET & Immunogenicity Analysis',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'admet_immunogenicity.png'), dpi=150)
    plt.close()
    print(f"\n  ✓ Visualization saved: {output_dir}/admet_immunogenicity.png")


def main():
    """Run ADMET and immunogenicity analysis."""
    print("=" * 70)
    print("Z² ADMET & IMMUNOGENICITY ANALYSIS")
    print("=" * 70)
    print("RED TEAM PROTOCOL - Testing Therapeutic Viability")
    print("=" * 70)

    print("\n" + "=" * 60)
    print("THE REALITY CHECK")
    print("=" * 60)
    print("\n  Beautiful geometry means NOTHING if:")
    print("  • The immune system destroys it")
    print("  • It aggregates in solution")
    print("  • Proteases cleave it immediately")
    print("  • It can't reach its target")
    print("\n  This is honest drug development analysis.")
    print("=" * 60)

    # Find ESM-predicted structure
    pdb_file = "pipeline_output_globular80/esm_prediction/z2_globular_80_esm.pdb"
    if not os.path.exists(pdb_file):
        # Try membrane context output
        pdb_file = "membrane_context/membrane_context_structure.pdb"

    if not os.path.exists(pdb_file):
        print(f"\n✗ ERROR: No PDB file found")
        # Use sequence directly
        sequence = "GNALEMALIYRQDPSMEFLIYKRNGNALEMALVIYEKNPSMEFLIYRQDGSALEMIYVKRNPNMEFLIYEQDGSALEM"
        coords = np.array([])
        print(f"  Using sequence only: {sequence[:40]}...")
    else:
        sequence, coords = parse_pdb_sequence(pdb_file)
        print(f"\n  Loaded structure: {pdb_file}")
        print(f"  Sequence length: {len(sequence)}")

    # Create output directory
    output_dir = "admet_analysis"
    os.makedirs(output_dir, exist_ok=True)

    # Run analyses
    print("\n" + "=" * 60)
    print("IMMUNOGENICITY PREDICTION")
    print("=" * 60)

    print("\n  Predicting MHC-I epitopes...")
    mhc_i_epitopes = predict_mhc_i_epitopes(sequence)
    print(f"    Found {len(mhc_i_epitopes)} potential MHC-I epitopes")

    print("\n  Predicting MHC-II epitopes...")
    mhc_ii_epitopes = predict_mhc_ii_epitopes(sequence)
    print(f"    Found {len(mhc_ii_epitopes)} potential MHC-II epitopes")

    print("\n  Predicting B-cell epitopes...")
    b_cell_epitopes = predict_b_cell_epitopes(sequence, coords)
    print(f"    Found {len(b_cell_epitopes)} potential B-cell epitopes")

    print("\n  Calculating human similarity...")
    human_similarity = calculate_human_similarity(sequence)
    print(f"    Similarity score: {human_similarity['similarity_score']:.2f}")
    print(f"    Assessment: {human_similarity['assessment']}")

    # Overall immunogenicity
    overall_immuno = calculate_overall_immunogenicity(
        mhc_i_epitopes, mhc_ii_epitopes, b_cell_epitopes, human_similarity
    )

    print(f"\n  Overall Risk Level: {overall_immuno['risk_level']}")
    print(f"  Immunogenicity Score: {overall_immuno['immunogenicity_score']:.1f}")

    # ADMET properties
    print("\n" + "=" * 60)
    print("ADMET PROPERTIES")
    print("=" * 60)

    print("\n  Predicting aggregation propensity...")
    aggregation = predict_aggregation(sequence)
    print(f"    Aggregation risk: {aggregation['risk'].upper()}")
    print(f"    Aggregation-prone regions: {aggregation['n_aprs']}")

    print("\n  Predicting protease susceptibility...")
    protease = predict_protease_susceptibility(sequence)
    print(f"    Stability: {protease['stability'].upper()}")
    print(f"    Total cleavage sites: {protease['total_cleavage_sites']}")

    print("\n  Predicting BBB permeability...")
    bbb = predict_bbb_permeability(sequence)
    print(f"    Molecular weight: {bbb['molecular_weight']} Da")
    print(f"    Can cross BBB: {'Yes' if bbb['can_cross_bbb'] else 'No'}")
    print(f"    Note: {bbb['note']}")

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'sequence': sequence,
        'n_residues': len(sequence),
        'mhc_i_epitopes': mhc_i_epitopes,
        'mhc_ii_epitopes': mhc_ii_epitopes,
        'b_cell_epitopes': b_cell_epitopes,
        'human_similarity': human_similarity,
        'overall_immunogenicity': overall_immuno,
        'aggregation': aggregation,
        'protease_susceptibility': protease,
        'bbb_permeability': bbb
    }

    # Create visualization
    create_visualization(results, output_dir)

    # Save results
    with open(os.path.join(output_dir, 'admet_results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n  ✓ Results saved: {output_dir}/admet_results.json")

    # Final verdict
    print("\n" + "=" * 70)
    print("THERAPEUTIC VIABILITY VERDICT")
    print("=" * 70)

    # Assess overall viability
    issues = []
    if overall_immuno['risk_level'] in ['CRITICAL', 'HIGH']:
        issues.append(f"Immunogenicity: {overall_immuno['risk_level']}")
    if aggregation['risk'] == 'high':
        issues.append("High aggregation propensity")
    if protease['stability'] == 'low':
        issues.append("Poor protease stability")
    if not bbb['can_cross_bbb']:
        issues.append("Cannot cross BBB (requires delivery system)")

    if len(issues) == 0:
        print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │  VERDICT: THERAPEUTICALLY VIABLE                               │
  │                                                                  │
  │  The Z² designed protein shows acceptable ADMET properties.    │
  │  Low immunogenicity, stable, and suitable for development.     │
  └─────────────────────────────────────────────────────────────────┘
        """)
    elif len(issues) <= 2:
        print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  VERDICT: CONDITIONALLY VIABLE                                 │
  │                                                                  │
  │  The Z² protein has some issues that need addressing:          │
  │  • {issues[0] if len(issues) > 0 else 'N/A':55}│
  │  • {issues[1] if len(issues) > 1 else 'N/A':55}│
  │                                                                  │
  │  These can likely be engineered around with modifications.     │
  └─────────────────────────────────────────────────────────────────┘
        """)
    else:
        print(f"""
  ┌─────────────────────────────────────────────────────────────────┐
  │  VERDICT: REQUIRES SIGNIFICANT OPTIMIZATION                    │
  │                                                                  │
  │  Multiple issues identified:                                   │
  │  • {issues[0] if len(issues) > 0 else 'N/A':55}│
  │  • {issues[1] if len(issues) > 1 else 'N/A':55}│
  │  • {issues[2] if len(issues) > 2 else 'N/A':55}│
  │                                                                  │
  │  IMPORTANT: Z² geometry is elegant, but biology is messy.      │
  │  Therapeutic development requires extensive optimization.      │
  └─────────────────────────────────────────────────────────────────┘
        """)

    return results


if __name__ == "__main__":
    results = main()
