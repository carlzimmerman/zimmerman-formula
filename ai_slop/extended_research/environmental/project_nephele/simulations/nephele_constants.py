"""
Project Nephele: Core Constants and Timeline Data
==================================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

Timeline of life's origin - when was abiogenesis possible?

References:
- Mojzsis et al. (2019): Revised LHB timing
- Dodd et al. (2017): Nuvvuagittuq microfossils
- Wilde et al. (2001): Jack Hills zircons
- Krot et al. (2002): CAI dating
"""

import numpy as np
from typing import Dict, Any, Tuple
from dataclasses import dataclass

# =============================================================================
# COSMIC TIMELINE (Billions of Years Ago - Gya)
# =============================================================================

@dataclass
class TimelineEvent:
    """A dated event in the history of the solar system."""
    name: str
    age_gya: float
    uncertainty_gyr: float
    description: str
    habitable: bool = False
    life_possible: bool = False


# Major timeline events
TIMELINE = {
    'solar_nebula_collapse': TimelineEvent(
        name="Solar Nebula Collapse",
        age_gya=4.6,
        uncertainty_gyr=0.01,
        description="Protoplanetary disk forms from molecular cloud",
        habitable=False,
        life_possible=False  # Too hot, but prebiotic chemistry occurs
    ),
    'cai_formation': TimelineEvent(
        name="CAI Formation",
        age_gya=4.567,
        uncertainty_gyr=0.001,
        description="Calcium-Aluminum-rich Inclusions - oldest solar system solids",
        habitable=False,
        life_possible=False
    ),
    'earth_accretion_begins': TimelineEvent(
        name="Earth Accretion Begins",
        age_gya=4.54,
        uncertainty_gyr=0.02,
        description="Planetesimals coalesce into proto-Earth",
        habitable=False,
        life_possible=False
    ),
    'theia_impact': TimelineEvent(
        name="Theia Impact (Moon Formation)",
        age_gya=4.5,
        uncertainty_gyr=0.05,
        description="Giant impact melts Earth's surface, forms Moon",
        habitable=False,
        life_possible=False  # Surface sterilization
    ),
    'lhb_revised': TimelineEvent(
        name="Late Heavy Bombardment (Revised)",
        age_gya=4.48,
        uncertainty_gyr=0.1,
        description="Main bombardment ends earlier than classically thought",
        habitable=False,
        life_possible=False
    ),
    'oldest_zircons': TimelineEvent(
        name="Oldest Zircons (Liquid Water)",
        age_gya=4.404,
        uncertainty_gyr=0.008,
        description="Jack Hills zircons indicate liquid water on surface",
        habitable=True,  # First confirmed habitability
        life_possible=True
    ),
    'lhb_classic_end': TimelineEvent(
        name="LHB Classic End",
        age_gya=3.8,
        uncertainty_gyr=0.1,
        description="Traditional LHB end date (now disputed)",
        habitable=True,
        life_possible=True
    ),
    'nuvvuagittuq_fossils': TimelineEvent(
        name="Nuvvuagittuq Microfossils (Disputed)",
        age_gya=4.28,
        uncertainty_gyr=0.1,
        description="Claimed earliest microfossils in hydrothermal vent precipitates",
        habitable=True,
        life_possible=True
    ),
    'luca_molecular_clock': TimelineEvent(
        name="LUCA (Molecular Clock Estimate)",
        age_gya=4.2,  # Midpoint of 4.33-4.09 range
        uncertainty_gyr=0.15,
        description="Last Universal Common Ancestor from molecular clocks",
        habitable=True,
        life_possible=True
    ),
    'isua_carbon': TimelineEvent(
        name="Isua Biogenic Carbon",
        age_gya=3.7,
        uncertainty_gyr=0.05,
        description="Carbon isotope signatures suggest biological origin",
        habitable=True,
        life_possible=True
    ),
    'earliest_stromatolites': TimelineEvent(
        name="Earliest Confirmed Stromatolites",
        age_gya=3.5,
        uncertainty_gyr=0.1,
        description="Oldest undisputed fossil evidence of life",
        habitable=True,
        life_possible=True
    ),
    'recent_biosignatures': TimelineEvent(
        name="Recent Biosignature Analysis",
        age_gya=3.3,
        uncertainty_gyr=0.05,
        description="2025 study: oxygen-producing photosynthesis signatures",
        habitable=True,
        life_possible=True
    ),
}

# =============================================================================
# HABITABILITY CONSTRAINTS
# =============================================================================

# Temperature constraints for life
T_MIN_LIFE_K = 233  # -40C (extremophiles)
T_MAX_LIFE_K = 395  # 122C (Methanopyrus kandleri)
T_OPTIMAL_LIFE_K = 310  # 37C (mesophiles)

# Water constraints
WATER_REQUIRED = True
LIQUID_WATER_MIN_K = 273
LIQUID_WATER_MAX_K = 373  # at 1 atm

# Energy source requirements
ENERGY_SOURCES = {
    'solar_uv': True,
    'geothermal': True,
    'chemical_redox': True,
    'cosmic_rays': True,  # From Project Protogonos
}

# =============================================================================
# PREBIOTIC CHEMISTRY TIMELINE
# =============================================================================

# Where could prebiotic chemistry occur?
PREBIOTIC_ENVIRONMENTS = {
    'protoplanetary_disk': {
        'time_range_gya': (4.6, 4.54),
        'temperature_range_k': (10, 1500),  # Varies with distance
        'organics_form': True,
        'amino_acids': True,  # Evidence from meteorites
        'nucleobases': True,
        'chirality_possible': True,  # Cosmic ray seeding
    },
    'planetesimals': {
        'time_range_gya': (4.56, 4.5),
        'temperature_range_k': (100, 500),
        'organics_form': True,
        'amino_acids': True,
        'aqueous_alteration': True,  # Brief liquid water
        'chirality_possible': True,
    },
    'early_earth_magma_ocean': {
        'time_range_gya': (4.5, 4.4),
        'temperature_range_k': (1500, 2500),
        'organics_form': False,  # Too hot
        'amino_acids': False,
        'chirality_possible': False,
    },
    'early_earth_cool_crust': {
        'time_range_gya': (4.4, 4.0),
        'temperature_range_k': (280, 400),
        'organics_form': True,
        'amino_acids': True,
        'nucleobases': True,
        'liquid_water': True,
        'chirality_possible': True,
    },
    'hydrothermal_vents': {
        'time_range_gya': (4.4, 0),  # Still active today
        'temperature_range_k': (275, 673),  # Gradient
        'organics_form': True,
        'amino_acids': True,
        'nucleobases': True,
        'chirality_possible': True,
        'concentration_mechanism': True,  # Thermal cycling
    },
}

# =============================================================================
# METEORITE DATA (Evidence for Pre-Earth Chemistry)
# =============================================================================

METEORITE_ORGANICS = {
    'murchison': {
        'year_fell': 1969,
        'location': 'Australia',
        'type': 'CM2 carbonaceous chondrite',
        'amino_acids_count': 70,
        'includes_non_terrestrial': True,
        'ee_measured': 0.01,  # ~1% enantiomeric excess
        'nucleobases': True,
        'sugars': True,
    },
    'tagish_lake': {
        'year_fell': 2000,
        'location': 'Canada',
        'type': 'C2 ungrouped',
        'amino_acids_count': 20,
        'pristine': True,
        'ee_measured': 0.0,  # Racemic
    },
    'ryugu': {
        'year_sampled': 2020,
        'location': 'Asteroid',
        'mission': 'Hayabusa2',
        'amino_acids_count': 14,  # of 20 protein AAs
        'nucleobases': True,
        'dna_rna_components': True,
    },
    'bennu': {
        'year_sampled': 2023,
        'location': 'Asteroid',
        'mission': 'OSIRIS-REx',
        'complex_organics': True,
        'hydrated_minerals': True,
    },
}

# =============================================================================
# PROJECT PROTOGONOS RESULTS (Validated Mechanisms)
# =============================================================================

PROTOGONOS_RESULTS = {
    'cosmic_ray_chiral_seeding': {
        'status': 'VALIDATED',
        'mechanism': 'Muon polarization + CISS',
        'P_mu': -0.255,  # Muon polarization
        'S_ciss': 0.2,   # CISS selectivity
        'P_net': -0.0086,  # ~0.86% ee generation
        'works_in_space': True,
    },
    'frank_autocatalysis': {
        'status': 'VALIDATED',
        'mechanism': 'Autocatalytic chirality amplification',
        'amplification_factor': 21735,
        'ee_initial': 1e-8,
        'ee_final': 0.000217,
        'works_in_liquid_water': True,
    },
    'bekenstein_bound': {
        'status': 'FALSIFIED',
        'cells_use_fraction': 9.58e-19,
        'conclusion': 'No information limit on biology',
    },
}

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Time units
GYR_TO_YR = 1e9
MYR_TO_YR = 1e6

# Age of universe
UNIVERSE_AGE_GYR = 13.8

# Age of solar system
SOLAR_SYSTEM_AGE_GYR = 4.6

# Age of Earth
EARTH_AGE_GYR = 4.54

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_habitability_window() -> Tuple[float, float]:
    """
    Return the time window when Earth was habitable (Gya).

    Returns:
        Tuple of (earliest_habitable, present)
    """
    # Earliest: oldest zircons with liquid water signature
    earliest = TIMELINE['oldest_zircons'].age_gya
    return (earliest, 0.0)


def get_life_window() -> Tuple[float, float]:
    """
    Return the time window when life has existed (Gya).

    Returns:
        Tuple of (earliest_life, present)
    """
    # Disputed earliest
    earliest_disputed = TIMELINE['nuvvuagittuq_fossils'].age_gya
    # Confirmed earliest
    earliest_confirmed = TIMELINE['earliest_stromatolites'].age_gya

    return (earliest_disputed, earliest_confirmed, 0.0)


def calculate_abiogenesis_window() -> Dict[str, float]:
    """
    Calculate the time available for abiogenesis.

    Returns:
        Dictionary with window calculations
    """
    habitable_start = TIMELINE['oldest_zircons'].age_gya
    earliest_life_disputed = TIMELINE['nuvvuagittuq_fossils'].age_gya
    earliest_life_confirmed = TIMELINE['earliest_stromatolites'].age_gya

    window_disputed = habitable_start - earliest_life_disputed
    window_confirmed = habitable_start - earliest_life_confirmed

    return {
        'habitable_start_gya': habitable_start,
        'earliest_life_disputed_gya': earliest_life_disputed,
        'earliest_life_confirmed_gya': earliest_life_confirmed,
        'window_if_disputed_myr': window_disputed * 1000,
        'window_if_confirmed_myr': window_confirmed * 1000,
        'window_disputed_gyr': window_disputed,
        'window_confirmed_gyr': window_confirmed,
    }


def could_chirality_predate_earth() -> Dict[str, Any]:
    """
    Analyze whether chirality could have been seeded before Earth formed.

    Based on Project Protogonos findings.
    """
    # Cosmic ray chiral seeding works in space
    cr_seeding = PROTOGONOS_RESULTS['cosmic_ray_chiral_seeding']

    # Check if mechanism works in protoplanetary disk
    disk = PREBIOTIC_ENVIRONMENTS['protoplanetary_disk']
    planetesimals = PREBIOTIC_ENVIRONMENTS['planetesimals']

    return {
        'mechanism_works_in_space': cr_seeding['works_in_space'],
        'amino_acids_in_disk': disk['amino_acids'],
        'amino_acids_in_planetesimals': planetesimals['amino_acids'],
        'chirality_possible_in_disk': disk['chirality_possible'],
        'meteorite_ee_evidence': METEORITE_ORGANICS['murchison']['ee_measured'],
        'conclusion': "Chirality could have been seeded before Earth formed",
        'p_estimate': 0.6,  # 60% probability
    }


def print_timeline_summary():
    """Print a summary of the timeline."""
    print("=" * 70)
    print("PROJECT NEPHELE: Timeline of Life's Origin")
    print("=" * 70)

    # Sort events by age
    sorted_events = sorted(TIMELINE.items(), key=lambda x: x[1].age_gya, reverse=True)

    print("\nCosmic Timeline (oldest to youngest):")
    print("-" * 70)

    for key, event in sorted_events:
        hab = "[H]" if event.habitable else "   "
        life = "[L]" if event.life_possible else "   "
        print(f"{event.age_gya:.3f} Gya {hab}{life} {event.name}")
        print(f"              {event.description}")

    print("\n" + "-" * 70)
    print("Legend: [H] = Habitable, [L] = Life possible")

    # Abiogenesis window
    window = calculate_abiogenesis_window()
    print("\nAbiogenesis Window:")
    print(f"  Habitability begins: {window['habitable_start_gya']:.3f} Gya")
    print(f"  Earliest life (disputed): {window['earliest_life_disputed_gya']:.3f} Gya")
    print(f"  Earliest life (confirmed): {window['earliest_life_confirmed_gya']:.3f} Gya")
    print(f"  Window (if disputed): {window['window_if_disputed_myr']:.0f} Myr")
    print(f"  Window (if confirmed): {window['window_if_confirmed_myr']:.0f} Myr")

    # Pre-Earth chirality
    chiral = could_chirality_predate_earth()
    print("\nPre-Earth Chirality Analysis:")
    print(f"  Cosmic ray seeding works in space: {chiral['mechanism_works_in_space']}")
    print(f"  Amino acids present in disk: {chiral['amino_acids_in_disk']}")
    print(f"  Murchison meteorite ee: {chiral['meteorite_ee_evidence']:.1%}")
    print(f"  Conclusion: {chiral['conclusion']}")
    print(f"  Probability estimate: {chiral['p_estimate']:.0%}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    print_timeline_summary()
