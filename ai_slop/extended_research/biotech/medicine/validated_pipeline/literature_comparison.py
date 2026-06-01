#!/usr/bin/env python3
"""
Literature Comparison: Z² Peptides vs Known Inhibitors
========================================================
Author: Carl Zimmerman
Date: 2026-04-24
License: AGPL-3.0

Compares our Z²-designed peptides to existing approved drugs and
research compounds for each target. This provides context for
whether our designs are novel, competitive, or redundant.

THEORETICAL/COMPUTATIONAL ONLY - NOT FOR CLINICAL USE
"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

# =============================================================================
# KNOWN INHIBITORS DATABASE
# =============================================================================

KNOWN_INHIBITORS = {
    'C2_Protease_B C2_Protease_B': {
        'approved_drugs': [
            {
                'name': 'Nirmatrelvir (Paxlovid)',
                'type': 'Small molecule (peptidomimetic)',
                'kd_or_ic50': 'Ki = 3.1 nM',
                'mechanism': 'Covalent inhibitor, binds Cys145',
                'approval': 'FDA EUA 2021, full approval 2023',
                'notes': 'Gold standard for C2_Protease_B geometrically stabilize',
            },
            {
                'name': 'Ensitrelvir (Xocova)',
                'type': 'Small molecule (non-covalent)',
                'kd_or_ic50': 'IC50 = 13 nM',
                'mechanism': 'Non-covalent, S1/S2 pocket binding',
                'approval': 'Japan 2022',
                'notes': 'Non-covalent alternative',
            },
        ],
        'research_compounds': [
            {
                'name': 'GC376',
                'type': 'Small molecule (peptidomimetic)',
                'kd_or_ic50': 'IC50 = 0.15 μM',
                'mechanism': 'Covalent inhibitor',
                'status': 'Veterinary approved, human trials',
            },
            {
                'name': 'Boceprevir',
                'type': 'Small molecule',
                'kd_or_ic50': 'IC50 = 4.1 μM',
                'mechanism': 'Covalent inhibitor (Monomeric_Cleft_C drug repurposed)',
                'status': 'FDA approved for Monomeric_Cleft_C, tested for COVID',
            },
        ],
        'peptide_inhibitors': [
            {
                'name': 'N3 (substrate-based)',
                'type': 'Peptide (Michael acceptor)',
                'kd_or_ic50': 'IC50 = 16.8 μM',
                'mechanism': 'Covalent, substrate-mimetic',
                'status': 'Research tool',
            },
        ],
        'our_design': {
            'name': 'MPRO_Z2_SEL_K2R6',
            'sequence': 'WKLWTRQWLQ',
            'type': 'Peptide (non-covalent)',
            'predicted_mechanism': 'Z² aromatic stacking with PHE140',
            'predicted_kd': 'UNKNOWN - not measured',
            'novelty_assessment': 'Novel mechanism (aromatic Z²) vs covalent Cys145',
        },
        'comparison': {
            'vs_nirmatrelvir': 'Nirmatrelvir is 3 nM; we need to be <100 nM to compete',
            'advantage_claimed': 'Non-covalent may have better safety profile',
            'disadvantage': 'Peptides have poor oral bioavailability',
            'honest_assessment': 'Unlikely to compete with Paxlovid without major advances',
        },
    },

    'C2_Homodimer_A': {
        'approved_drugs': [
            {
                'name': 'Darunavir (Prezista)',
                'type': 'Small molecule',
                'kd_or_ic50': 'Ki = 4.5 pM',
                'mechanism': 'Non-covalent, transition state mimic',
                'approval': 'FDA 2006',
                'notes': 'Best-in-class, extremely potent',
            },
            {
                'name': 'Atazanavir (Reyataz)',
                'type': 'Small molecule',
                'kd_or_ic50': 'Ki = 2.7 nM',
                'mechanism': 'Non-covalent',
                'approval': 'FDA 2003',
                'notes': 'Once-daily dosing',
            },
            {
                'name': 'Lopinavir (Kaletra component)',
                'type': 'Small molecule',
                'kd_or_ic50': 'Ki = 1.3 nM',
                'mechanism': 'Non-covalent',
                'approval': 'FDA 2000',
                'notes': 'Ritonavir-boosted',
            },
        ],
        'research_compounds': [
            {
                'name': 'GRL-142',
                'type': 'Small molecule',
                'kd_or_ic50': 'Ki = 2.9 pM',
                'mechanism': 'Non-covalent, multi-drug resistant strains',
                'status': 'Preclinical',
            },
        ],
        'peptide_inhibitors': [
            {
                'name': 'Various substrate-based peptides',
                'type': 'Peptide',
                'kd_or_ic50': 'IC50 = 0.1-10 μM range',
                'mechanism': 'Competitive',
                'status': 'Research only',
            },
        ],
        'our_design': {
            'name': 'HIV_Z2_OPT_001',
            'sequence': 'RLEWTWEKILTE',
            'type': 'Peptide (non-covalent)',
            'predicted_mechanism': 'Z² stacking with PHE53 + ASP25 salt bridges',
            'predicted_kd': 'UNKNOWN - not measured',
            'novelty_assessment': 'Novel dual-W Z² geometry claim',
        },
        'comparison': {
            'vs_darunavir': 'Darunavir is 4.5 pM (!); we need to be <1 nM to be relevant',
            'advantage_claimed': 'May work against darunavir-resistant strains',
            'disadvantage': 'Competing with picomolar drugs is extremely difficult',
            'honest_assessment': 'C2_Homodimer_A PR inhibitors are HIGHLY optimized. Very hard to improve.',
        },
    },

    'TNF-α': {
        'approved_drugs': [
            {
                'name': 'Adalimumab (Humira)',
                'type': 'Monoclonal antibody',
                'kd_or_ic50': 'Kd = 100 pM',
                'mechanism': 'Binds TNF-α, blocks receptor binding',
                'approval': 'FDA 2002',
                'notes': 'Best-selling drug ever ($20B/year peak)',
            },
            {
                'name': 'Etanercept (Enbrel)',
                'type': 'Fusion protein (TNFR2-Fc)',
                'kd_or_ic50': 'Kd = 0.8 nM',
                'mechanism': 'Decoy receptor',
                'approval': 'FDA 1998',
                'notes': 'First TNF inhibitor',
            },
            {
                'name': 'Infliximab (Remicade)',
                'type': 'Chimeric antibody',
                'kd_or_ic50': 'Kd = 44 pM',
                'mechanism': 'Binds TNF-α',
                'approval': 'FDA 1998',
                'notes': 'IV infusion',
            },
        ],
        'research_compounds': [
            {
                'name': 'Small molecule TNF inhibitors',
                'type': 'Various',
                'kd_or_ic50': 'IC50 = 1-50 μM (weak)',
                'mechanism': 'Various (trimer disruption, etc.)',
                'status': 'Generally failed - hard target for small molecules',
            },
        ],
        'peptide_inhibitors': [
            {
                'name': 'WP9QY',
                'type': 'Peptide',
                'kd_or_ic50': 'Kd = 8 μM',
                'mechanism': 'Blocks TNF-TNFR1 interaction',
                'status': 'Research',
            },
            {
                'name': 'Various TNF-derived peptides',
                'type': 'Peptide',
                'kd_or_ic50': 'IC50 = 1-100 μM',
                'mechanism': 'Competitive',
                'status': 'Research',
            },
        ],
        'our_design': {
            'name': 'TNF_Z2_SEL_DUAL',
            'sequence': 'DDWEYTWEQELTD',
            'type': 'Peptide (non-covalent)',
            'predicted_mechanism': 'Z² stacking with TYR151 + ARG/LYS salt bridges',
            'predicted_kd': 'UNKNOWN - not measured',
            'novelty_assessment': 'Peptide approach to a target dominated by biologics',
        },
        'comparison': {
            'vs_adalimumab': 'Adalimumab is 100 pM with $20B/year sales. Hard to compete.',
            'advantage_claimed': 'Peptide may be cheaper than antibody, oral potential',
            'disadvantage': 'Small molecules have largely failed for TNF-α',
            'honest_assessment': 'TNF-α is a VERY difficult target for non-antibodies. Peptide is risky.',
        },
    },

    'Metabolic_Receptor_E': {
        'approved_drugs': [
            {
                'name': 'Sitagliptin (Januvia)',
                'type': 'Small molecule',
                'kd_or_ic50': 'IC50 = 18 nM',
                'mechanism': 'Competitive inhibitor',
                'approval': 'FDA 2006',
                'notes': 'First Metabolic_Receptor_E inhibitor, Merck',
            },
            {
                'name': 'Linagliptin (Tradjenta)',
                'type': 'Small molecule',
                'kd_or_ic50': 'IC50 = 1 nM',
                'mechanism': 'Competitive inhibitor',
                'approval': 'FDA 2011',
                'notes': 'Most potent gliptin',
            },
            {
                'name': 'Saxagliptin (Onglyza)',
                'type': 'Small molecule',
                'kd_or_ic50': 'Ki = 1.3 nM',
                'mechanism': 'Covalent-reversible',
                'approval': 'FDA 2009',
                'notes': 'AstraZeneca',
            },
            {
                'name': 'Vildagliptin (Galvus)',
                'type': 'Small molecule',
                'kd_or_ic50': 'IC50 = 3.5 nM',
                'mechanism': 'Covalent-reversible',
                'approval': 'EU 2007 (not US)',
                'notes': 'Novartis',
            },
        ],
        'research_compounds': [
            {
                'name': 'Various next-gen gliptins',
                'type': 'Small molecule',
                'kd_or_ic50': 'IC50 = 0.1-10 nM',
                'mechanism': 'Competitive',
                'status': 'Several in development',
            },
        ],
        'peptide_inhibitors': [
            {
                'name': 'Diprotin A (Ile-Pro-Ile)',
                'type': 'Tripeptide',
                'kd_or_ic50': 'Ki = 2-5 μM',
                'mechanism': 'Competitive substrate analog',
                'status': 'Research tool',
            },
        ],
        'our_design': {
            'name': 'DPP4_Z2_SEL_RK',
            'sequence': 'RWPKWGELTK',
            'type': 'Peptide (non-covalent)',
            'predicted_mechanism': 'Z² stacking with TRP629 + GLU205/206 selectivity',
            'predicted_kd': 'UNKNOWN - not measured',
            'novelty_assessment': 'Novel selectivity mechanism via charge reversal',
        },
        'comparison': {
            'vs_linagliptin': 'Linagliptin is 1 nM oral. We need <10 nM to compete.',
            'advantage_claimed': 'Better DPP-8/9 selectivity than some gliptins',
            'disadvantage': 'Oral gliptins work well. Why inject a peptide?',
            'honest_assessment': 'Metabolic_Receptor_E is SOLVED by oral small molecules. Peptide offers no clear advantage.',
        },
    },

    'EGFR': {
        'approved_drugs': [
            {
                'name': 'Erlotinib (Tarceva)',
                'type': 'Small molecule TKI',
                'kd_or_ic50': 'IC50 = 2 nM',
                'mechanism': 'ATP-competitive kinase inhibitor',
                'approval': 'FDA 2004',
                'notes': 'First-gen TKI',
            },
            {
                'name': 'Gefitinib (Iressa)',
                'type': 'Small molecule TKI',
                'kd_or_ic50': 'IC50 = 33 nM',
                'mechanism': 'ATP-competitive',
                'approval': 'FDA 2003',
                'notes': 'First-gen TKI',
            },
            {
                'name': 'Osimertinib (Tagrisso)',
                'type': 'Small molecule TKI',
                'kd_or_ic50': 'IC50 = 1 nM (T790M)',
                'mechanism': 'Third-gen, covalent, T790M active',
                'approval': 'FDA 2015',
                'notes': 'Best-in-class, $5B/year',
            },
            {
                'name': 'Cetuximab (Erbitux)',
                'type': 'Monoclonal antibody',
                'kd_or_ic50': 'Kd = 0.39 nM',
                'mechanism': 'Blocks EGF binding',
                'approval': 'FDA 2004',
                'notes': 'Extracellular domain binder',
            },
        ],
        'research_compounds': [
            {
                'name': 'Fourth-gen EGFR TKIs',
                'type': 'Small molecule',
                'kd_or_ic50': 'IC50 < 1 nM',
                'mechanism': 'Allosteric, C797S active',
                'status': 'Clinical trials',
            },
        ],
        'peptide_inhibitors': [
            {
                'name': 'EGF-derived peptides',
                'type': 'Peptide',
                'kd_or_ic50': 'IC50 = 1-100 μM',
                'mechanism': 'Competitive with EGF',
                'status': 'Research',
            },
        ],
        'our_design': {
            'name': 'EGFR_Z2_EGF_001',
            'sequence': 'YWLQWNRELTL',
            'type': 'Peptide (non-covalent)',
            'predicted_mechanism': 'EGF-competitive, Z² with PHE357',
            'predicted_kd': 'UNKNOWN - not measured',
            'novelty_assessment': 'Extracellular peptide vs kinase TKIs',
        },
        'comparison': {
            'vs_osimertinib': 'Osimertinib is 1 nM oral TKI. Hard to compete.',
            'vs_cetuximab': 'Cetuximab is 0.39 nM antibody at same site. Very hard.',
            'advantage_claimed': 'May avoid kinase domain resistance mutations',
            'disadvantage': 'Competing with $5B/year drugs is difficult',
            'honest_assessment': 'EGFR is HEAVILY competed. Need unique angle (resistance, selectivity).',
        },
    },
}


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_competitive_landscape():
    """
    Analyze where our Z² peptides fit in the competitive landscape.
    """

    analysis = {
        'overall_assessment': {
            'targets_with_approved_drugs': 5,
            'targets_where_peptides_competitive': 0,
            'targets_where_peptides_may_add_value': 2,
            'targets_where_peptides_unlikely_useful': 3,
        },
        'by_target': {},
        'honest_conclusions': [],
    }

    for target, data in KNOWN_INHIBITORS.items():
        best_approved = data['approved_drugs'][0]
        our_design = data['our_design']
        comparison = data['comparison']

        target_analysis = {
            'best_approved_drug': best_approved['name'],
            'best_approved_potency': best_approved['kd_or_ic50'],
            'our_design': our_design['sequence'],
            'our_predicted_potency': our_design['predicted_kd'],
            'honest_assessment': comparison['honest_assessment'],
            'competitive_gap': 'LARGE' if 'nM' in best_approved['kd_or_ic50'] or 'pM' in best_approved['kd_or_ic50'] else 'MODERATE',
        }

        analysis['by_target'][target] = target_analysis

    analysis['honest_conclusions'] = [
        {
            'conclusion': 'ALL 5 TARGETS HAVE APPROVED DRUGS',
            'implication': 'We are not addressing unmet medical needs',
        },
        {
            'conclusion': 'EXISTING DRUGS ARE HIGHLY OPTIMIZED',
            'implication': 'pM to nM potency is standard; our peptides are unmeasured',
        },
        {
            'conclusion': 'PEPTIDES FACE DRUGABILITY CHALLENGES',
            'implication': 'Oral small molecules dominate where available (Metabolic_Receptor_E, EGFR TKI)',
        },
        {
            'conclusion': 'ANTIBODIES DOMINATE EXTRACELLULAR TARGETS',
            'implication': 'TNF-α, EGFR extracellular are antibody territory',
        },
        {
            'conclusion': 'POSSIBLE NICHE: RESISTANCE/SELECTIVITY',
            'implication': 'May add value for drug-resistant variants or improved selectivity',
        },
    ]

    return analysis


def generate_gap_analysis():
    """
    Quantify the gap between our designs and existing drugs.
    """

    gaps = {
        'C2_Protease_B C2_Protease_B': {
            'best_existing': '3.1 nM (Nirmatrelvir)',
            'our_status': 'Unmeasured',
            'minimum_to_compete': '<100 nM',
            'likelihood_of_achieving': 'UNKNOWN',
        },
        'C2_Homodimer_A': {
            'best_existing': '4.5 pM (Darunavir)',
            'our_status': 'Unmeasured',
            'minimum_to_compete': '<1 nM',
            'likelihood_of_achieving': 'LOW (pM drugs are exceptional)',
        },
        'TNF-α': {
            'best_existing': '44-100 pM (antibodies)',
            'our_status': 'Unmeasured',
            'minimum_to_compete': '<10 nM',
            'likelihood_of_achieving': 'LOW (small molecules have failed)',
        },
        'Metabolic_Receptor_E': {
            'best_existing': '1 nM (Linagliptin)',
            'our_status': 'Unmeasured',
            'minimum_to_compete': '<10 nM',
            'likelihood_of_achieving': 'MODERATE (peptides can reach nM)',
        },
        'EGFR': {
            'best_existing': '0.39 nM (Cetuximab), 1 nM (Osimertinib)',
            'our_status': 'Unmeasured',
            'minimum_to_compete': '<10 nM',
            'likelihood_of_achieving': 'LOW (crowded space)',
        },
    }

    return gaps


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 80)
    print("  LITERATURE COMPARISON: Z² PEPTIDES VS KNOWN INHIBITORS")
    print("=" * 80)
    print()
    print("HONEST ASSESSMENT OF COMPETITIVE LANDSCAPE")
    print()

    for target, data in KNOWN_INHIBITORS.items():
        print(f"\n{'='*60}")
        print(f"  {target}")
        print(f"{'='*60}")

        print("\nAPPROVED DRUGS:")
        for drug in data['approved_drugs'][:2]:  # Top 2
            print(f"  {drug['name']}: {drug['kd_or_ic50']}")
            print(f"    {drug['mechanism']}")

        print(f"\nOUR DESIGN: {data['our_design']['name']}")
        print(f"  Sequence: {data['our_design']['sequence']}")
        print(f"  Predicted Kd: {data['our_design']['predicted_kd']}")

        print(f"\nHONEST ASSESSMENT:")
        print(f"  {data['comparison']['honest_assessment']}")

    # Gap analysis
    gaps = generate_gap_analysis()

    print("\n")
    print("=" * 80)
    print("  COMPETITIVE GAP ANALYSIS")
    print("=" * 80)

    for target, gap in gaps.items():
        print(f"\n{target}:")
        print(f"  Best existing: {gap['best_existing']}")
        print(f"  Our status: {gap['our_status']}")
        print(f"  Minimum to compete: {gap['minimum_to_compete']}")
        print(f"  Likelihood: {gap['likelihood_of_achieving']}")

    # Overall analysis
    analysis = analyze_competitive_landscape()

    print("\n")
    print("=" * 80)
    print("  OVERALL CONCLUSIONS")
    print("=" * 80)

    for conclusion in analysis['honest_conclusions']:
        print(f"\n{conclusion['conclusion']}")
        print(f"  → {conclusion['implication']}")

    # Save results
    output_dir = Path(__file__).parent

    output = {
        'known_inhibitors': KNOWN_INHIBITORS,
        'gap_analysis': gaps,
        'competitive_analysis': analysis,
    }

    # Convert to serializable format
    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(i) for i in obj]
        else:
            return obj

    output_file = output_dir / "literature_comparison_results.json"
    with open(output_file, 'w') as f:
        json.dump(make_serializable(output), f, indent=2)
    print(f"\n\nResults saved: {output_file}")

    print("\n")
    print("=" * 80)
    print("  BOTTOM LINE")
    print("=" * 80)
    print("""
Our Z² peptides are entering HIGHLY COMPETITIVE spaces:

  C2_Homodimer_A Protease: Competing with 4.5 pM drugs (Darunavir)
  TNF-α: Competing with $20B/year antibodies (Humira)
  Metabolic_Receptor_E: Competing with 1 nM oral drugs (Linagliptin)
  EGFR: Competing with $5B/year TKIs (Osimertinib)
  C2_Protease_B: Competing with approved oral drug (Paxlovid)

The Z² mechanism might be real, but being "real" is not enough.
We need to demonstrate:
  1. Actual binding affinity (Kd measurement)
  2. Competitive potency (<10-100 nM range)
  3. Advantage over existing drugs (resistance, selectivity, safety)

Without experimental validation, these remain interesting hypotheses
competing against proven, optimized therapeutics.
""")


if __name__ == "__main__":
    main()
