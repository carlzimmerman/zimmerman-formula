"""
Project Nephele: Timeline Analysis - When Was Life Possible?
============================================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

ULTRATHINK ANALYSIS: Could life predate Earth?

This script analyzes:
1. The temporal constraints on abiogenesis
2. Whether prebiotic chemistry could occur before Earth formed
3. The probability of various origin-of-life scenarios

Building on Project Protogonos validated mechanisms:
- Cosmic ray chiral seeding (works in space)
- Frank autocatalysis (works in liquid water)
"""

import numpy as np
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

# Import constants from nephele_constants
from nephele_constants import (
    TIMELINE, PREBIOTIC_ENVIRONMENTS, METEORITE_ORGANICS,
    PROTOGONOS_RESULTS, calculate_abiogenesis_window,
    could_chirality_predate_earth, GYR_TO_YR, MYR_TO_YR
)

# =============================================================================
# ULTRATHINK ANALYSIS FUNCTIONS
# =============================================================================

def analyze_fast_start_paradox() -> Dict[str, Any]:
    """
    Analyze the "fast start" paradox: life appears almost immediately after habitability.

    Returns:
        Analysis of the timing implications
    """
    window = calculate_abiogenesis_window()

    # If disputed evidence is true
    disputed_window_myr = window['window_if_disputed_myr']  # ~120 Myr
    # If only confirmed evidence
    confirmed_window_myr = window['window_if_confirmed_myr']  # ~900 Myr

    # Expected time for abiogenesis under different models
    # (These are rough estimates from literature)
    expected_times_myr = {
        'random_chemistry': 1000,  # ~1 Gyr for random assembly
        'warm_little_pond': 100,   # Darwin's warm little pond
        'hydrothermal_vent': 10,   # Rapid at vents
        'panspermia': 0,           # Life arrives already formed
    }

    analysis = {
        'paradox_statement': (
            "Life appears within ~120-900 Myr of habitability. "
            "This is surprisingly fast for a process thought to be improbable."
        ),
        'disputed_window_myr': disputed_window_myr,
        'confirmed_window_myr': confirmed_window_myr,
        'expected_times': expected_times_myr,
        'interpretations': {
            'interpretation_1': {
                'name': "Abiogenesis is Easy",
                'description': "Given the right conditions, life emerges quickly",
                'supports_fast_window': True,
                'evidence': [
                    "Life appears fast on Earth",
                    "Prebiotic chemistry is robust",
                    "Multiple independent pathways possible"
                ],
                'problems': [
                    "Why don't we see second genesis?",
                    "Lab experiments don't create life easily"
                ],
                'p_estimate': 0.3,
            },
            'interpretation_2': {
                'name': "Soft Panspermia",
                'description': "Building blocks arrive from space, reducing time needed",
                'supports_fast_window': True,
                'evidence': [
                    "Meteorites contain amino acids",
                    "Cosmic ray chiral seeding validated",
                    "Protoplanetary disk chemistry creates organics"
                ],
                'problems': [
                    "Still need abiogenesis somewhere",
                    "Survival through accretion uncertain"
                ],
                'p_estimate': 0.5,
            },
            'interpretation_3': {
                'name': "Life Predates Earth",
                'description': "Simple life formed in space, seeded Earth",
                'supports_fast_window': True,
                'evidence': [
                    "Would explain fast start",
                    "Microbes survive space conditions",
                    "Lithopanspermia is possible"
                ],
                'problems': [
                    "No direct evidence of space life",
                    "Still need origin location",
                    "LUCA phylogeny suggests Earth origin"
                ],
                'p_estimate': 0.05,
            },
            'interpretation_4': {
                'name': "Observer Selection Bias",
                'description': "We can only observe universes where life started fast",
                'supports_fast_window': True,
                'evidence': [
                    "Anthropic reasoning",
                    "N=1 sample problem"
                ],
                'problems': [
                    "Not predictive",
                    "Doesn't explain mechanism"
                ],
                'p_estimate': 0.15,
            },
        },
    }

    # Sum of p_estimates should be 1 (they're mutually exclusive interpretations)
    total_p = sum(i['p_estimate'] for i in analysis['interpretations'].values())
    analysis['note'] = f"P estimates sum to {total_p:.2f} (should normalize)"

    return analysis


def analyze_chiral_seeding_timeline() -> Dict[str, Any]:
    """
    Analyze when and where chirality could have been seeded.

    Uses Project Protogonos validated cosmic ray mechanism.
    """
    cr_data = PROTOGONOS_RESULTS['cosmic_ray_chiral_seeding']
    frank_data = PROTOGONOS_RESULTS['frank_autocatalysis']

    # Timeline of chiral seeding opportunities
    seeding_opportunities = []

    # 1. Protoplanetary disk (4.6 - 4.54 Gya)
    disk = PREBIOTIC_ENVIRONMENTS['protoplanetary_disk']
    seeding_opportunities.append({
        'location': 'Protoplanetary Disk',
        'time_range_gya': disk['time_range_gya'],
        'duration_myr': (disk['time_range_gya'][0] - disk['time_range_gya'][1]) * 1000,
        'cosmic_ray_flux': 'High (no atmosphere)',
        'amino_acids_present': disk['amino_acids'],
        'liquid_water': False,  # No Frank amplification possible
        'can_seed_chirality': True,
        'can_amplify_chirality': False,  # Needs liquid water
        'outcome': "Seeding only, no amplification",
        'p_seeding': 0.7,
    })

    # 2. Planetesimals (4.56 - 4.5 Gya)
    planetesimals = PREBIOTIC_ENVIRONMENTS['planetesimals']
    seeding_opportunities.append({
        'location': 'Planetesimals (Parent Bodies of Meteorites)',
        'time_range_gya': planetesimals['time_range_gya'],
        'duration_myr': (planetesimals['time_range_gya'][0] - planetesimals['time_range_gya'][1]) * 1000,
        'cosmic_ray_flux': 'High initially, attenuated by accretion',
        'amino_acids_present': planetesimals['amino_acids'],
        'liquid_water': planetesimals['aqueous_alteration'],  # Brief!
        'can_seed_chirality': True,
        'can_amplify_chirality': True,  # Brief aqueous alteration
        'outcome': "Seeding + partial amplification possible",
        'p_seeding': 0.8,
        'p_amplification': 0.2,  # Aqueous alteration brief
    })

    # 3. Early Earth magma ocean (4.5 - 4.4 Gya)
    magma = PREBIOTIC_ENVIRONMENTS['early_earth_magma_ocean']
    seeding_opportunities.append({
        'location': 'Early Earth (Magma Ocean)',
        'time_range_gya': magma['time_range_gya'],
        'duration_myr': (magma['time_range_gya'][0] - magma['time_range_gya'][1]) * 1000,
        'cosmic_ray_flux': 'N/A (no stable molecules)',
        'amino_acids_present': False,  # Destroyed by heat
        'liquid_water': False,
        'can_seed_chirality': False,
        'can_amplify_chirality': False,
        'outcome': "RESET: Previous chirality destroyed",
        'p_seeding': 0.0,
    })

    # 4. Early Earth cool crust (4.4 - 4.0 Gya)
    cool_crust = PREBIOTIC_ENVIRONMENTS['early_earth_cool_crust']
    seeding_opportunities.append({
        'location': 'Early Earth (Cool Crust)',
        'time_range_gya': cool_crust['time_range_gya'],
        'duration_myr': (cool_crust['time_range_gya'][0] - cool_crust['time_range_gya'][1]) * 1000,
        'cosmic_ray_flux': 'Moderate (atmosphere forming)',
        'amino_acids_present': True,  # Meteorite delivery + synthesis
        'liquid_water': True,
        'can_seed_chirality': True,
        'can_amplify_chirality': True,  # Frank model works!
        'outcome': "Full abiogenesis possible",
        'p_seeding': 0.9,
        'p_amplification': 0.6,
    })

    # Key insight from Project Protogonos
    analysis = {
        'cosmic_ray_parameters': {
            'P_mu': cr_data['P_mu'],
            'S_ciss': cr_data['S_ciss'],
            'P_net': cr_data['P_net'],
            'works_in_space': cr_data['works_in_space'],
        },
        'frank_parameters': {
            'amplification_factor': frank_data['amplification_factor'],
            'requires_liquid_water': frank_data['works_in_liquid_water'],
        },
        'seeding_opportunities': seeding_opportunities,
        'key_insight': (
            "Chirality can be SEEDED in space (cosmic rays + amino acids), "
            "but AMPLIFICATION requires liquid water (Frank model). "
            "The magma ocean RESETS any pre-existing chirality."
        ),
        'critical_question': (
            "Can chiral seeds survive the magma ocean phase, "
            "or must chirality be re-seeded on the cool crust?"
        ),
    }

    return analysis


def analyze_survival_through_accretion() -> Dict[str, Any]:
    """
    Analyze whether prebiotic molecules could survive Earth accretion.

    This is the critical question: does the magma ocean reset everything?
    """
    # Temperature during magma ocean
    T_magma_ocean_K = 2000  # Approximate

    # Decomposition temperatures of organics
    decomposition_temps_K = {
        'amino_acids': 473,     # ~200C
        'nucleobases': 573,     # ~300C
        'sugars': 433,          # ~160C
        'lipids': 573,          # ~300C
        'complex_organics': 400, # ~127C
    }

    # All organics destroyed during magma ocean phase
    survival_analysis = {
        'magma_ocean_temp_K': T_magma_ocean_K,
        'organic_survival': {},
    }

    for molecule, T_decomp in decomposition_temps_K.items():
        survives = T_decomp > T_magma_ocean_K
        survival_analysis['organic_survival'][molecule] = {
            'decomposition_temp_K': T_decomp,
            'survives_magma_ocean': survives,
        }

    # None survive
    all_destroyed = all(
        not v['survives_magma_ocean']
        for v in survival_analysis['organic_survival'].values()
    )

    survival_analysis['conclusion'] = {
        'all_organics_destroyed': all_destroyed,
        'implication': (
            "The magma ocean RESETS prebiotic chemistry. "
            "Any organics from the protoplanetary disk are destroyed. "
            "Earth's organic inventory must be rebuilt via: "
            "(1) late meteorite delivery after cool-down, "
            "(2) in-situ synthesis from inorganics, "
            "(3) or both."
        ),
        'does_this_invalidate_soft_panspermia': "NO",
        'explanation': (
            "Soft panspermia still works because meteorites continue "
            "to deliver organics AFTER the magma ocean cools. "
            "The 'late veneer' of meteoritic material is well-documented."
        ),
    }

    return survival_analysis


def analyze_late_delivery() -> Dict[str, Any]:
    """
    Analyze the late delivery of organics after magma ocean cooling.
    """
    # Mass of late veneer (estimate)
    late_veneer_mass_kg = 3.5e21  # ~0.5% Earth mass

    # Organic content of carbonaceous chondrites
    organic_fraction_cc = 0.02  # ~2% by mass

    # Fraction of late veneer that was carbonaceous
    cc_fraction = 0.1  # ~10% of impactors

    # Total organics delivered
    organics_delivered_kg = late_veneer_mass_kg * cc_fraction * organic_fraction_cc

    # Amino acid fraction of organics
    amino_acid_fraction = 0.01  # ~1% of organics

    amino_acids_delivered_kg = organics_delivered_kg * amino_acid_fraction

    # Convert to moles
    avg_amino_acid_mass = 0.1  # kg/mol (rough average)
    amino_acids_delivered_mol = amino_acids_delivered_kg / avg_amino_acid_mass

    analysis = {
        'late_veneer_mass_kg': late_veneer_mass_kg,
        'carbonaceous_chondrite_fraction': cc_fraction,
        'organic_fraction': organic_fraction_cc,
        'total_organics_delivered_kg': organics_delivered_kg,
        'amino_acids_delivered_kg': amino_acids_delivered_kg,
        'amino_acids_delivered_mol': amino_acids_delivered_mol,
        'conclusion': (
            f"Late meteorite delivery could have provided ~{organics_delivered_kg:.1e} kg "
            f"of organic material to early Earth, including ~{amino_acids_delivered_kg:.1e} kg "
            "of amino acids. This is a substantial supply of prebiotic material."
        ),
        'chirality_from_late_delivery': {
            'murchison_ee': METEORITE_ORGANICS['murchison']['ee_measured'],
            'implication': (
                "If late delivery amino acids had ~1% ee (like Murchison), "
                "this provides the initial seed for Frank amplification."
            ),
        },
    }

    return analysis


def ultrathink_could_life_predate_earth() -> Dict[str, Any]:
    """
    ULTRATHINK: Could life have originated before Earth was habitable?

    Main analysis combining all findings.
    """
    print("=" * 70)
    print("ULTRATHINK: Could Life Predate Earth?")
    print("=" * 70)

    # Run all analyses
    fast_start = analyze_fast_start_paradox()
    chiral_timeline = analyze_chiral_seeding_timeline()
    survival = analyze_survival_through_accretion()
    late_delivery = analyze_late_delivery()

    # Synthesize findings
    synthesis = {
        'question': "Could life have originated before Earth was habitable?",
        'answer': "PARTIALLY YES",
        'explanation': [
            "1. PREBIOTIC CHEMISTRY predates Earth:",
            "   - Amino acids, nucleobases form in protoplanetary disk",
            "   - Evidence: Meteorites contain these molecules",
            "   - Chirality can be seeded via cosmic rays (validated)",
            "",
            "2. BUT the magma ocean RESETS everything:",
            "   - All organics destroyed at ~2000 K",
            "   - Any pre-existing chirality erased",
            "   - Life cannot survive this phase",
            "",
            "3. LATE DELIVERY rebuilds the inventory:",
            "   - Meteorites deliver organics after cool-down",
            "   - These carry chiral seeds (~1% ee in Murchison)",
            "   - Frank autocatalysis amplifies to homochirality",
            "",
            "4. ACTUAL ABIOGENESIS happens on Earth:",
            "   - Requires liquid water (Frank model)",
            "   - Requires concentration mechanisms",
            "   - Earth provides unique environment",
        ],
        'verdict': {
            'prebiotic_chemistry_predates_earth': True,
            'chirality_can_be_seeded_in_space': True,
            'full_life_predates_earth': False,
            'life_requires_earth_like_environment': True,
            'soft_panspermia_supported': True,
            'hard_panspermia_supported': False,
        },
        'probability_estimates': {
            'P_prebiotic_chem_from_space': 0.85,
            'P_chiral_seed_from_space': 0.60,
            'P_life_from_space': 0.05,
            'P_life_originated_on_earth': 0.90,
        },
        'key_insight': (
            "The Z² framework (via Project Protogonos) shows cosmic rays can seed "
            "chirality in space. This chirality is delivered via meteorites AFTER "
            "the magma ocean cools. Earth then provides the liquid water needed "
            "for Frank autocatalysis to amplify chirality to homochirality. "
            "Thus, life's INGREDIENTS come from space, but ASSEMBLY happens on Earth."
        ),
    }

    # Print summary
    print("\n" + "-" * 70)
    print("VERDICT: " + synthesis['answer'])
    print("-" * 70)
    for line in synthesis['explanation']:
        print(line)
    print("-" * 70)

    print("\nProbability Estimates:")
    for key, value in synthesis['probability_estimates'].items():
        print(f"  {key}: {value:.0%}")

    print("\nKey Insight:")
    print(f"  {synthesis['key_insight']}")
    print("=" * 70)

    # Full results
    results = {
        'metadata': {
            'analysis': 'Project Nephele - Timeline of Life\'s Origin',
            'date': datetime.now().isoformat(),
            'author': 'Carl Zimmerman',
        },
        'fast_start_paradox': fast_start,
        'chiral_seeding_timeline': chiral_timeline,
        'survival_through_accretion': survival,
        'late_delivery': late_delivery,
        'synthesis': synthesis,
        'ultrathink_status': 'GREEN - Soft panspermia supported, mechanisms validated',
    }

    return results


def save_results(results: Dict[str, Any], filepath: str):
    """Save results to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to: {filepath}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Run ultrathink analysis
    results = ultrathink_could_life_predate_earth()

    # Save results
    save_results(
        results,
        '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/environmental/project_nephele/data/results/timeline_analysis_results.json'
    )
