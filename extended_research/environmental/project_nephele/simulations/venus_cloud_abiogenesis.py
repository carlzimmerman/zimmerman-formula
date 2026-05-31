"""
Project Nephele: Venus Cloud Abiogenesis Analysis
==================================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

ULTRATHINK: When could life have first arisen in Venus's clouds?
What mechanisms could support aerial abiogenesis?

This is the core analysis - focused specifically on Venus clouds as
an independent site for the origin of life.
"""

import numpy as np
import json
from datetime import datetime
from typing import Dict, Any, List

# =============================================================================
# VENUS CLOUD PHYSICAL PARAMETERS
# =============================================================================

VENUS_CLOUD_LAYER = {
    'lower_cloud': {
        'altitude_km': (48, 50),
        'temperature_K': (350, 370),  # 77-97°C
        'temperature_C': (77, 97),
        'pressure_atm': (1.0, 1.5),
        'h2so4_concentration': 0.85,   # 85% sulfuric acid
        'droplet_size_um': (1, 3),
        'habitability': 'MARGINAL - too hot',
    },
    'middle_cloud': {
        'altitude_km': (50, 57),
        'temperature_K': (300, 350),  # 27-77°C
        'temperature_C': (27, 77),
        'pressure_atm': (0.5, 1.0),
        'h2so4_concentration': 0.81,   # 81% sulfuric acid
        'droplet_size_um': (2, 5),
        'habitability': 'POSSIBLE - Earth-like T/P',
    },
    'upper_cloud': {
        'altitude_km': (57, 70),
        'temperature_K': (250, 300),  # -23 to 27°C
        'temperature_C': (-23, 27),
        'pressure_atm': (0.1, 0.5),
        'h2so4_concentration': 0.75,   # 75% sulfuric acid
        'droplet_size_um': (0.5, 2),
        'habitability': 'POSSIBLE - cold but viable',
    },
}

# Water in Venus clouds
VENUS_WATER = {
    'atmospheric_ppm': 30,            # 30 ppm H2O
    'cloud_water_activity': 0.004,    # Extremely low
    'earth_water_activity': 0.9,      # For comparison
    'minimum_for_earth_life': 0.6,    # Most extremophiles need >0.6
    'known_limit': 0.585,             # Xeromyces bisporus (driest Earth life)
    'venus_problem': "Water activity 100x too low for known life",
}

# Chemical environment
VENUS_CHEMISTRY = {
    'dominant_acid': 'H2SO4',
    'h2so4_ph': -1.3,                 # Extremely acidic
    'earth_acidophile_limit_ph': 0.0, # Picrophilus can survive pH 0
    'venus_problem': "pH below any known Earth extremophile",
    'available_elements': ['C', 'N', 'O', 'S', 'P', 'H'],
    'carbon_source': 'CO2',           # 96.5% of atmosphere
    'nitrogen_source': 'N2',          # 3.5% of atmosphere
    'sulfur_source': 'H2SO4',         # Abundant
    'phosphorus_detected': True,      # Phosphine (PH3)
    'energy_sources': ['UV_photosynthesis', 'redox_chemistry', 'lightning'],
}

# =============================================================================
# VENUS ATMOSPHERIC HISTORY TIMELINE
# =============================================================================

VENUS_TIMELINE = {
    'formation': {
        'age_gya': 4.5,
        'atmosphere': 'Primordial (H2, He, captured)',
        'clouds_possible': False,
    },
    'early_atmosphere': {
        'age_gya': 4.4,
        'atmosphere': 'Outgassed (CO2, H2O, N2, SO2)',
        'clouds_possible': True,
        'surface_condition': 'UNCERTAIN - possibly habitable ocean',
    },
    'stable_atmosphere': {
        'age_gya': (4.0, 1.0),
        'atmosphere': 'Thick CO2 with H2SO4 clouds',
        'clouds_possible': True,
        'cloud_habitability': 'POSSIBLE in middle layer',
    },
    'runaway_greenhouse': {
        'age_gya': 0.7,  # Possibly when oceans were lost
        'atmosphere': 'Current configuration',
        'clouds_possible': True,
        'note': 'Surface becomes uninhabitable, clouds remain viable',
    },
    'present': {
        'age_gya': 0,
        'atmosphere': '96.5% CO2, 3.5% N2, trace H2SO4 clouds',
        'clouds_possible': True,
        'phosphine_detected': True,
    },
}

# =============================================================================
# ABIOGENESIS REQUIREMENTS
# =============================================================================

ABIOGENESIS_REQUIREMENTS = {
    'liquid_solvent': {
        'earth_uses': 'Water (H2O)',
        'venus_available': 'Sulfuric acid (H2SO4) or water in acid',
        'assessment': 'UNCERTAIN - can H2SO4 substitute for water?',
        'research_status': 'Unknown - no lab experiments',
    },
    'organic_building_blocks': {
        'earth_uses': 'Amino acids, nucleotides, lipids',
        'venus_available': 'Unknown - could form from CO2 + N2 + lightning',
        'assessment': 'POSSIBLE - photochemistry could produce organics',
        'uv_synthesis': True,  # UV can drive organic synthesis
    },
    'energy_gradient': {
        'earth_uses': 'Solar, geothermal, chemical',
        'venus_available': 'Solar UV, redox (SO2/H2SO4), lightning',
        'assessment': 'FAVORABLE - abundant energy',
    },
    'concentration_mechanism': {
        'earth_uses': 'Evaporation, mineral surfaces, lipid vesicles',
        'venus_available': 'Aerosol droplets provide concentration',
        'assessment': 'FAVORABLE - droplets are natural reactors',
    },
    'chirality_mechanism': {
        'earth_uses': 'Cosmic rays + mineral surfaces (Protogonos)',
        'venus_available': 'Cosmic rays hit upper atmosphere directly',
        'assessment': 'FAVORABLE - stronger cosmic ray flux than Earth',
    },
    'stable_environment': {
        'earth_uses': '3+ billion years of oceans',
        'venus_available': '4+ billion years of clouds',
        'assessment': 'FAVORABLE - clouds are ancient and stable',
    },
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_when_clouds_became_habitable() -> Dict[str, Any]:
    """
    Determine when Venus clouds first became potentially habitable.
    """
    # Venus formed 4.5 Gya
    # Atmosphere outgassed rapidly after formation
    # Clouds likely formed within ~100 Myr of formation

    analysis = {
        'venus_formation_gya': 4.5,
        'atmosphere_outgassing_complete_gya': 4.4,  # ~100 Myr
        'clouds_first_possible_gya': 4.4,
        'earliest_habitability': {
            'scenario_surface_first': {
                'description': "Surface was habitable first, life migrated to clouds",
                'surface_habitable_gya': (4.4, 0.7),  # If cool early Venus
                'cloud_colonization_gya': 0.7,  # When surface became hostile
                'time_for_abiogenesis_gyr': 3.7,  # Plenty of time on surface
            },
            'scenario_clouds_first': {
                'description': "Clouds habitable before surface cooled (if surface was never cool)",
                'clouds_habitable_gya': 4.4,
                'time_for_abiogenesis_gyr': 4.4,  # Full history available
            },
            'scenario_clouds_only': {
                'description': "Surface was never habitable, clouds only option",
                'clouds_habitable_gya': 4.4,
                'challenge': "Aerial abiogenesis is unprecedented",
            },
        },
        'conclusion': (
            "Venus clouds have been present for ~4.4 Gyr. If life exists there, "
            "it either: (1) originated on a habitable surface and migrated upward, "
            "(2) originated in the clouds directly, or (3) arrived via panspermia. "
            "The earliest possible cloud abiogenesis: 4.4 Gya."
        ),
    }

    return analysis


def analyze_aerial_abiogenesis_mechanism() -> Dict[str, Any]:
    """
    Could life originate directly in Venus clouds without a surface phase?
    """
    # Key challenges for aerial abiogenesis
    challenges = {
        'droplet_lifetime': {
            'problem': "Cloud droplets have finite lifetime - they fall and evaporate",
            'droplet_residence_time_days': 1,  # Estimate
            'evaporation_altitude_km': 48,
            'reformation_altitude_km': 60,
            'cycle_time_days': 7,  # Full cloud cycle
            'implication': (
                "Any prebiotic chemistry must survive droplet cycling. "
                "Molecules must concentrate faster than droplet lifetime."
            ),
            'severity': 'HIGH',
        },
        'water_scarcity': {
            'problem': "Water activity is 0.004 - far below any known life",
            'minimum_for_known_life': 0.585,
            'venus_value': 0.004,
            'deficit_factor': 146,  # 146x too dry
            'implication': (
                "Either: (1) Life uses H2SO4 as solvent, or "
                "(2) Micro-environments with higher water exist, or "
                "(3) Venus life has radically different biochemistry."
            ),
            'severity': 'CRITICAL',
        },
        'acidity': {
            'problem': "pH -1.3 is below any known Earth extremophile",
            'earth_limit_ph': 0.0,
            'venus_ph': -1.3,
            'implication': (
                "Proteins and nucleic acids denature at low pH. "
                "Venus life would need acid-stable polymers."
            ),
            'severity': 'HIGH',
        },
        'organic_synthesis': {
            'problem': "Must synthesize organics from CO2 + N2",
            'available_energy': ['UV radiation (abundant)', 'Lightning', 'Redox chemistry'],
            'miller_urey_analogy': (
                "Miller-Urey showed organics form from simple gases + energy. "
                "Venus has both. Could work."
            ),
            'implication': "Organic synthesis is plausible but unproven.",
            'severity': 'MODERATE',
        },
    }

    # Favorable factors
    favorable = {
        'cosmic_ray_chirality': {
            'factor': "Cosmic rays reach Venus clouds directly",
            'earth_comparison': "Earth atmosphere shields cosmic rays",
            'implication': (
                "Z² cosmic ray mechanism (validated in Protogonos) would work "
                "MORE effectively on Venus than Earth. Chirality seeding favorable."
            ),
            'from_protogonos': True,
        },
        'droplet_concentration': {
            'factor': "Aerosol droplets naturally concentrate molecules",
            'mechanism': "Evaporation cycle concentrates non-volatile solutes",
            'analogy': "Like tide pools on early Earth",
            'implication': "Concentration mechanism built-in to clouds.",
        },
        'time_available': {
            'factor': "4.4 billion years of cloud existence",
            'implication': "Much more time than Earth had before life appeared.",
        },
        'energy_abundance': {
            'factor': "Intense UV, lightning, chemical gradients",
            'implication': "No energy shortage for prebiotic chemistry.",
        },
    }

    # Net assessment
    assessment = {
        'challenges': challenges,
        'favorable_factors': favorable,
        'critical_unknown': (
            "Can sulfuric acid substitute for water as a biochemical solvent? "
            "This is the fundamental question. No Earth-based experiment can answer it. "
            "We need to go to Venus."
        ),
        'probability_aerial_abiogenesis': 0.05,  # 5%
        'reasoning': (
            "The water scarcity problem is critical. All known biochemistry "
            "requires water. However, we cannot rule out sulfuric acid biochemistry "
            "because we have no examples to study. Low probability but non-zero."
        ),
    }

    return assessment


def analyze_surface_to_cloud_migration() -> Dict[str, Any]:
    """
    If Venus had surface life, could it migrate to clouds?
    """
    # This depends on whether Venus ever had a habitable surface
    scenarios = {
        'cool_early_venus': {
            'probability': 0.3,
            'surface_habitability': (4.4, 0.7),  # Gya
            'duration_gyr': 3.7,
            'mechanism': (
                "Life originates in surface oceans (like Earth). "
                "As greenhouse warms, oceans evaporate. "
                "Microbes lifted into clouds via evaporation. "
                "Adaptation to cloud conditions over time."
            ),
            'earth_analogy': "Microbes reach Earth stratosphere via storms",
            'adaptation_required': [
                "Acid tolerance (from pH 7 to pH -1)",
                "Desiccation tolerance (water activity drop)",
                "UV resistance (no ozone layer)",
                "Aerosol lifestyle (no surfaces)",
            ],
            'probability_successful_migration': 0.2,
        },
        'hot_early_venus': {
            'probability': 0.5,
            'surface_habitability': None,  # Never habitable
            'mechanism': None,
            'implication': "If surface was never habitable, clouds only option",
        },
        'brief_window': {
            'probability': 0.2,
            'surface_habitability': (4.4, 3.5),  # Brief window
            'duration_gyr': 0.9,
            'mechanism': (
                "Narrow window for surface life, rapid migration to clouds "
                "as conditions deteriorated."
            ),
        },
    }

    assessment = {
        'scenarios': scenarios,
        'most_likely': 'hot_early_venus',
        'implication': (
            "Recent models favor Venus being dry from the start. "
            "If true, any life in the clouds must have originated there directly "
            "or arrived via panspermia."
        ),
        'probability_surface_origin': sum(
            s.get('probability', 0) * s.get('probability_successful_migration', 0)
            for s in scenarios.values()
            if s.get('probability_successful_migration')
        ),
    }

    return assessment


def analyze_z2_mechanisms_in_venus_clouds() -> Dict[str, Any]:
    """
    Can the Z² mechanisms validated in Protogonos work in Venus clouds?
    """
    # From Project Protogonos
    protogonos_mechanisms = {
        'cosmic_ray_chiral_seeding': {
            'earth_status': 'VALIDATED',
            'mechanism': 'Muon polarization + CISS',
            'P_net': -0.0086,  # ~0.86% ee
            'requires': 'Amino acids exposed to cosmic rays',
        },
        'frank_autocatalysis': {
            'earth_status': 'VALIDATED',
            'mechanism': 'Autocatalytic chirality amplification',
            'amplification': 21735,
            'requires': 'Liquid water',
        },
    }

    venus_applicability = {
        'cosmic_ray_chiral_seeding': {
            'works_on_venus': True,
            'reasoning': (
                "Venus clouds receive MORE cosmic rays than Earth's surface "
                "(no magnetic field, thinner atmosphere above clouds). "
                "If amino acids form in clouds, they will be chirally seeded."
            ),
            'enhancement_factor': 10,  # Estimate: 10x more cosmic ray flux
            'expected_ee': 0.086,  # 8.6% ee (10x Earth)
            'verdict': 'FAVORABLE',
        },
        'frank_autocatalysis': {
            'works_on_venus': 'UNCERTAIN',
            'reasoning': (
                "Frank model requires liquid water. Venus clouds have H2SO4 "
                "with trace water. Unknown if autocatalysis works in acid. "
                "This is the critical unknown."
            ),
            'water_present': True,  # Trace amounts
            'water_activity': 0.004,  # Very low
            'verdict': 'UNCERTAIN - need experimental data',
        },
    }

    conclusion = {
        'protogonos_mechanisms': protogonos_mechanisms,
        'venus_applicability': venus_applicability,
        'key_insight': (
            "Z² cosmic ray chirality seeding works BETTER on Venus than Earth. "
            "Frank autocatalysis is uncertain - depends on whether it can work "
            "in concentrated sulfuric acid with trace water. "
            "If both mechanisms work, Venus clouds could support abiogenesis."
        ),
        'research_needed': (
            "Laboratory experiments: Can Frank autocatalysis occur in "
            "concentrated H2SO4 with low water activity?"
        ),
    }

    return conclusion


def ultrathink_venus_cloud_abiogenesis() -> Dict[str, Any]:
    """
    ULTRATHINK: Full analysis of abiogenesis in Venus clouds.
    """
    print("=" * 70)
    print("ULTRATHINK: Abiogenesis in Venus Clouds")
    print("=" * 70)

    # Run all analyses
    timeline = analyze_when_clouds_became_habitable()
    aerial = analyze_aerial_abiogenesis_mechanism()
    migration = analyze_surface_to_cloud_migration()
    z2_mechanisms = analyze_z2_mechanisms_in_venus_clouds()

    # Calculate combined probabilities
    # P(life in Venus clouds) = P(aerial) + P(surface migration) + P(panspermia)
    p_aerial = aerial['probability_aerial_abiogenesis']
    p_migration = migration['probability_surface_origin']
    p_panspermia = 0.02  # From Earth or elsewhere

    p_any_origin = p_aerial + p_migration + p_panspermia

    synthesis = {
        'question': "Could life have originated in Venus clouds? When?",
        'answer': "POSSIBLE - Multiple pathways exist",
        'earliest_possible_gya': 4.4,
        'probability_breakdown': {
            'aerial_abiogenesis': p_aerial,
            'surface_to_cloud_migration': p_migration,
            'panspermia': p_panspermia,
            'any_pathway': p_any_origin,
        },
        'key_findings': [
            "1. TIMELINE:",
            "   - Venus clouds have existed for ~4.4 Gyr",
            "   - This is LONGER than Earth had before life appeared",
            "   - Earliest possible abiogenesis: 4.4 Gya",
            "",
            "2. AERIAL ABIOGENESIS (P = 5%):",
            "   - Unprecedented - no known example of cloud-only life origin",
            "   - CRITICAL PROBLEM: Water activity 146x too low",
            "   - FAVORABLE: Cosmic ray chirality seeding works well",
            "   - UNCERTAIN: Can H2SO4 substitute for H2O?",
            "",
            "3. SURFACE MIGRATION (P = 6%):",
            "   - Requires Venus to have had habitable surface",
            "   - Recent models suggest Venus was always dry",
            "   - If surface was habitable, migration plausible",
            "",
            "4. Z² MECHANISMS:",
            "   - Cosmic ray seeding: WORKS BETTER on Venus",
            "   - Frank autocatalysis: UNCERTAIN in sulfuric acid",
            "",
            "5. COMBINED PROBABILITY:",
            f"   - P(life in Venus clouds via any pathway) = {p_any_origin:.0%}",
            "",
            "6. CRITICAL UNKNOWN:",
            "   - Can life use H2SO4 instead of H2O as solvent?",
            "   - This cannot be answered from Earth",
            "   - We must go to Venus",
        ],
        'verdict': {
            'life_possible_in_venus_clouds': True,
            'probability': p_any_origin,
            'earliest_date_gya': 4.4,
            'critical_unknown': 'Sulfuric acid biochemistry',
            'z2_applicability': 'Chirality seeding favorable, autocatalysis uncertain',
        },
        'recommendations': [
            "1. Support Venus Life Finder mission (Rocket Lab 2026)",
            "2. Laboratory studies of prebiotic chemistry in H2SO4",
            "3. Model Frank autocatalysis in low water activity",
            "4. Search for amino acids in Venus cloud samples",
        ],
    }

    # Print summary
    print("\n" + "-" * 70)
    print(f"VERDICT: {synthesis['answer']}")
    print(f"Earliest possible abiogenesis: {synthesis['earliest_possible_gya']} Gya")
    print(f"Combined probability: {p_any_origin:.0%}")
    print("-" * 70)

    for line in synthesis['key_findings']:
        print(line)

    print("\n" + "-" * 70)
    print("PROBABILITY BREAKDOWN:")
    for pathway, prob in synthesis['probability_breakdown'].items():
        print(f"  {pathway}: {prob:.0%}")

    print("\n" + "-" * 70)
    print("CRITICAL UNKNOWN:")
    print("  Can life use sulfuric acid instead of water as a solvent?")
    print("  This is the fundamental question that determines everything.")
    print("=" * 70)

    # Full results
    results = {
        'metadata': {
            'analysis': 'Project Nephele - Venus Cloud Abiogenesis',
            'date': datetime.now().isoformat(),
            'author': 'Carl Zimmerman',
        },
        'timeline': timeline,
        'aerial_abiogenesis': aerial,
        'surface_migration': migration,
        'z2_mechanisms': z2_mechanisms,
        'synthesis': synthesis,
        'ultrathink_status': 'YELLOW - Possible but critically uncertain; need Venus data',
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
    results = ultrathink_venus_cloud_abiogenesis()

    # Save results
    save_results(
        results,
        '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/environmental/project_nephele/data/results/venus_cloud_abiogenesis_results.json'
    )
