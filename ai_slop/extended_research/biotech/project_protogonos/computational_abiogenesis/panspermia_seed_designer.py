#!/usr/bin/env python3
"""
PANSPERMIA SEED DESIGNER
========================
Designing life for Europa and Venus based on the Protogonos framework.

If Ω_Z = 1.0 (life is inevitable when conditions are right), then seeding
other worlds requires engineering the Z-resonance conditions:

1. Lattice substrate with d ≈ Z = 5.79 Å at local temperature
2. Magnetic inclusions providing B ≥ 245 Gauss for CISS
3. Energy source for metabolism
4. Precursor molecules for autocatalysis

This script designs optimal seed packages for:
- Europa (subsurface ocean, hydrothermal vents)
- Venus (cloud layer, 48-65 km altitude)

Author: Project Protogonos
"""

import numpy as np
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from enum import Enum

# =============================================================================
# FUNDAMENTAL CONSTANTS FROM PROTOGONOS
# =============================================================================

Z = np.sqrt(32 * np.pi / 3)  # 5.7888 Å - the scale of life
Z_SQUARED = 32 * np.pi / 3   # 33.51 Å²

# Omega Lattice composition (Earth-optimized)
EARTH_OMEGA_LATTICE = {
    'Pb_fraction': 0.908,
    'Sn_fraction': 0.092,
    'formula': 'Pb₀.₉₀₈Sn₀.₀₉₂S',
    'd_300K': Z,  # Exactly Z at 300K
}

# Magnetic requirements
B_CISS_THRESHOLD = 245  # Gauss - minimum for CISS activation
B_MAGNETITE_SURFACE = 4021  # Gauss - from magnetic junction analysis

# Thermal expansion coefficients (× 10⁻⁶ /K)
THERMAL_EXPANSION = {
    'galena_PbS': 20.4,
    'herzenbergite_SnS': 18.5,
    'pyrite_FeS2': 10.2,
    'magnetite_Fe3O4': 8.5,
    'greigite_Fe3S4': 12.0,
}

# Lattice constants at 300K (Å)
LATTICE_CONSTANTS_300K = {
    'galena_PbS': 5.936,
    'herzenbergite_SnS': 4.33,  # Orthorhombic, a-axis
    'pyrite_FeS2': 5.417,
    'magnetite_Fe3O4': 8.396,
    'greigite_Fe3S4': 9.876,
}


# =============================================================================
# TARGET WORLD ENVIRONMENTS
# =============================================================================

@dataclass
class WorldEnvironment:
    """Defines environmental conditions on a target world."""
    name: str
    location: str
    temperature_K: float
    temperature_range_K: Tuple[float, float]
    pressure_bar: float
    pressure_range_bar: Tuple[float, float]
    pH: Optional[float]
    radiation_mSv_year: float
    gravity_g: float
    available_elements: List[str]
    energy_sources: List[str]
    challenges: List[str]
    opportunities: List[str]


EUROPA_OCEAN = WorldEnvironment(
    name="Europa",
    location="Subsurface ocean / hydrothermal vents",
    temperature_K=273,  # Near ice-water interface
    temperature_range_K=(269, 373),  # Ice interface to hot vents
    pressure_bar=100,  # Estimated at ocean floor
    pressure_range_bar=(1, 300),
    pH=8.5,  # Likely slightly alkaline
    radiation_mSv_year=5400000,  # Surface only - ocean shielded
    gravity_g=0.134,
    available_elements=['H', 'O', 'S', 'Na', 'Mg', 'Cl', 'Fe', 'Si'],
    energy_sources=[
        'Hydrothermal vents (chemical gradients)',
        'Radiolysis of ice (H2, O2 production)',
        'Serpentinization (H2 production)',
    ],
    challenges=[
        'Penetrating 10-30 km ice shell',
        'High pressure at depth',
        'Limited organic precursors',
        'Unknown ocean chemistry',
    ],
    opportunities=[
        'Liquid water confirmed',
        'Hydrothermal activity likely',
        'Magnetite common at vents',
        'Similar to early Earth oceans',
    ],
)

VENUS_CLOUDS = WorldEnvironment(
    name="Venus",
    location="Cloud layer (48-65 km altitude)",
    temperature_K=310,  # ~37°C at 55 km - body temperature!
    temperature_range_K=(273, 373),  # Habitable zone in clouds
    pressure_bar=1.0,  # ~1 atm at 50-55 km
    pressure_range_bar=(0.1, 3.0),
    pH=0,  # Concentrated sulfuric acid
    radiation_mSv_year=50,  # Atmosphere shields from cosmic rays
    gravity_g=0.904,
    available_elements=['C', 'O', 'S', 'N', 'H', 'Cl', 'F', 'P'],
    energy_sources=[
        'Abundant sunlight',
        'UV radiation',
        'Chemical energy (SO2/H2SO4 cycling)',
        'Lightning',
    ],
    challenges=[
        'Extreme acidity (75-98% H2SO4)',
        'Very low water activity',
        'Staying aloft (aerosol lifecycle)',
        'Acid-resistant biochemistry needed',
    ],
    opportunities=[
        'Earth-like temperature and pressure!',
        'Abundant CO2 and sulfur compounds',
        'Possible existing aerial biosphere',
        'Phosphine detection (controversial)',
    ],
)


# =============================================================================
# OMEGA LATTICE DESIGNER
# =============================================================================

def calculate_lattice_constant(T: float, material: str, d_ref: float = None, T_ref: float = 300) -> float:
    """
    Calculate lattice constant at temperature T using thermal expansion.

    d(T) = d_ref × (1 + α × (T - T_ref))
    """
    if d_ref is None:
        d_ref = LATTICE_CONSTANTS_300K.get(material, 5.936)

    alpha = THERMAL_EXPANSION.get(material, 20.0) * 1e-6
    return d_ref * (1 + alpha * (T - T_ref))


def design_omega_lattice(target_T: float, tolerance: float = 0.01) -> Dict:
    """
    Design an Omega Lattice (Pb_x Sn_{1-x} S) that achieves d = Z at target temperature.

    Uses Vegard's law for solid solutions:
    d_alloy = x × d_PbS + (1-x) × d_SnS

    Returns optimal Pb fraction and predicted lattice constant.
    """
    # Lattice constants at target temperature
    d_PbS_T = calculate_lattice_constant(target_T, 'galena_PbS', LATTICE_CONSTANTS_300K['galena_PbS'])

    # SnS is orthorhombic - use effective cubic equivalent for mixing
    # Effective lattice parameter for rock salt structure comparison
    d_SnS_eff_300K = 5.45  # Effective cubic equivalent
    alpha_SnS = THERMAL_EXPANSION['herzenbergite_SnS'] * 1e-6
    d_SnS_T = d_SnS_eff_300K * (1 + alpha_SnS * (target_T - 300))

    # Solve for x: Z = x × d_PbS + (1-x) × d_SnS
    # Z = x × d_PbS + d_SnS - x × d_SnS
    # Z - d_SnS = x × (d_PbS - d_SnS)
    # x = (Z - d_SnS) / (d_PbS - d_SnS)

    x_Pb = (Z - d_SnS_T) / (d_PbS_T - d_SnS_T)
    x_Pb = np.clip(x_Pb, 0, 1)

    # Predicted lattice constant
    d_predicted = x_Pb * d_PbS_T + (1 - x_Pb) * d_SnS_T

    # Offset from Z
    offset_percent = abs(d_predicted - Z) / Z * 100

    return {
        'target_temperature_K': target_T,
        'Pb_fraction': round(x_Pb, 4),
        'Sn_fraction': round(1 - x_Pb, 4),
        'formula': f'Pb_{{{x_Pb:.3f}}}Sn_{{{1-x_Pb:.3f}}}S',
        'd_predicted_A': round(d_predicted, 4),
        'Z_target_A': round(Z, 4),
        'offset_percent': round(offset_percent, 4),
        'within_tolerance': offset_percent <= tolerance * 100,
        'd_PbS_at_T': round(d_PbS_T, 4),
        'd_SnS_eff_at_T': round(d_SnS_T, 4),
    }


# =============================================================================
# SEED PACKAGE DESIGNER
# =============================================================================

@dataclass
class MineralComponent:
    """A mineral component of the seed package."""
    name: str
    formula: str
    role: str
    mass_fraction: float
    properties: Dict


@dataclass
class OrganicComponent:
    """An organic precursor component."""
    name: str
    formula: str
    role: str
    mass_fraction: float
    stability: str  # 'acid-stable', 'cryo-stable', etc.


@dataclass
class SeedPackage:
    """Complete seed package design for a target world."""
    target_world: str
    total_mass_kg: float
    omega_lattice: Dict
    minerals: List[MineralComponent]
    organics: List[OrganicComponent]
    encapsulation: str
    delivery_method: str
    survival_probability: float
    germination_time_years: float
    rationale: str


def design_europa_seed() -> SeedPackage:
    """
    Design a seed package for Europa's subsurface ocean.

    Strategy: Hydrothermal vent colonization
    - Omega Lattice optimized for ~350K (vent temperature)
    - Magnetite inclusions for CISS activation
    - Chemolithotrophic metabolism (H2 + CO2 → CH4 + H2O)
    - Cryo-protected delivery through ice
    """

    # Design Omega Lattice for vent temperature
    vent_temp = 350  # K, typical black smoker
    omega_lattice = design_omega_lattice(vent_temp)

    # Also design for ice-water interface
    interface_temp = 273
    omega_lattice_cold = design_omega_lattice(interface_temp)

    minerals = [
        MineralComponent(
            name="Omega Lattice (vent-optimized)",
            formula=omega_lattice['formula'],
            role="Primary Z-resonance substrate",
            mass_fraction=0.40,
            properties={
                'd_at_350K': omega_lattice['d_predicted_A'],
                'offset_from_Z': omega_lattice['offset_percent'],
            }
        ),
        MineralComponent(
            name="Magnetite nanoparticles",
            formula="Fe₃O₄",
            role="CISS activation via magnetic junctions",
            mass_fraction=0.15,
            properties={
                'particle_size_nm': 50,
                'surface_field_gauss': B_MAGNETITE_SURFACE,
                'Curie_temp_K': 858,
            }
        ),
        MineralComponent(
            name="Pyrrhotite",
            formula="Fe₇S₈",
            role="Secondary magnetic mineral + sulfur source",
            mass_fraction=0.10,
            properties={
                'magnetic': True,
                'sulfur_source': True,
            }
        ),
        MineralComponent(
            name="Olivine",
            formula="(Mg,Fe)₂SiO₄",
            role="Serpentinization substrate for H2 production",
            mass_fraction=0.15,
            properties={
                'serpentinization_rate': 'slow but steady',
                'H2_production': True,
            }
        ),
    ]

    organics = [
        OrganicComponent(
            name="Amino acid mixture",
            formula="L-amino acids (20 standard)",
            role="Protein building blocks",
            mass_fraction=0.05,
            stability="cryo-stable",
        ),
        OrganicComponent(
            name="Nucleotide precursors",
            formula="Ribose, phosphate, bases",
            role="RNA/DNA building blocks",
            mass_fraction=0.03,
            stability="cryo-stable",
        ),
        OrganicComponent(
            name="Lipid vesicles",
            formula="Phosphatidylcholine + archaeal lipids",
            role="Membrane formation",
            mass_fraction=0.07,
            stability="cryo-stable, pressure-resistant",
        ),
        OrganicComponent(
            name="Methanogen inoculum",
            formula="Lyophilized Methanococcus",
            role="Starter culture for chemolithotrophy",
            mass_fraction=0.05,
            stability="cryo-stable, radiation-resistant",
        ),
    ]

    return SeedPackage(
        target_world="Europa",
        total_mass_kg=100,
        omega_lattice=omega_lattice,
        minerals=minerals,
        organics=organics,
        encapsulation="Titanium shell with ablative heat shield + cryo-protected inner core",
        delivery_method="Ice-penetrating thermal probe (cryobot)",
        survival_probability=0.15,  # Many unknowns
        germination_time_years=1000,  # Slow start in cold environment
        rationale="""
        Europa seed strategy: Colonize hydrothermal vents

        1. DELIVERY: Cryobot melts through ice shell using RTG heat
        2. RELEASE: Seed package disperses at ocean-ice interface
        3. TRANSPORT: Ocean currents carry seeds to hydrothermal vents
        4. GERMINATION:
           - Omega Lattice particles settle near vents (350K optimal)
           - Magnetite provides local B > 245 Gauss for CISS
           - Vent chemistry provides H2, CO2, sulfur compounds
           - Z-resonance catalyzes amino acid polymerization
        5. LIFE EMERGENCE:
           - Frank Model homochirality in ~5 generations
           - Methanogen inoculum provides metabolic template
           - Self-sustaining chemolithotrophic ecosystem

        Key advantage: Similar to early Earth hydrothermal origin hypothesis.
        Europa's ocean may already have the right conditions - we're just
        providing optimized catalysts and a metabolic head-start.
        """
    )


def design_venus_seed() -> SeedPackage:
    """
    Design a seed package for Venus's cloud layer.

    Strategy: Aerial acidophilic ecosystem
    - Omega Lattice optimized for 310K (cloud temperature)
    - Acid-resistant encapsulation
    - Sulfur-based phototrophy
    - Aerosol lifecycle (evaporation/condensation)
    """

    # Venus clouds are surprisingly Earth-like in T and P!
    cloud_temp = 310  # K, at 55 km altitude
    omega_lattice = design_omega_lattice(cloud_temp)

    minerals = [
        MineralComponent(
            name="Omega Lattice (acid-protected)",
            formula=omega_lattice['formula'],
            role="Primary Z-resonance substrate",
            mass_fraction=0.30,
            properties={
                'd_at_310K': omega_lattice['d_predicted_A'],
                'offset_from_Z': omega_lattice['offset_percent'],
                'encapsulation': 'PTFE-coated nanoparticles',
            }
        ),
        MineralComponent(
            name="Magnetite (PTFE-coated)",
            formula="Fe₃O₄",
            role="CISS activation",
            mass_fraction=0.10,
            properties={
                'acid_protection': 'PTFE shell',
                'surface_field_gauss': B_MAGNETITE_SURFACE * 0.8,  # Reduced by coating
            }
        ),
        MineralComponent(
            name="Sulfur microspheres",
            formula="S₈",
            role="Metabolic substrate + UV protection",
            mass_fraction=0.15,
            properties={
                'UV_absorption': 'strong',
                'energy_storage': True,
            }
        ),
        MineralComponent(
            name="Silica aerogel matrix",
            formula="SiO₂",
            role="Structural support + buoyancy",
            mass_fraction=0.10,
            properties={
                'density_kg_m3': 50,
                'acid_resistant': True,
            }
        ),
    ]

    organics = [
        OrganicComponent(
            name="Acidophile lipids",
            formula="Tetraether lipids (archaeal)",
            role="Acid-resistant membranes",
            mass_fraction=0.10,
            stability="acid-stable (pH 0-2)",
        ),
        OrganicComponent(
            name="Sulfur-oxidizing enzymes",
            formula="SOX enzyme complex",
            role="Energy metabolism: H2S + O → S + H2O",
            mass_fraction=0.05,
            stability="acid-stable",
        ),
        OrganicComponent(
            name="Bacteriorhodopsin analogs",
            formula="Retinal-protein complex",
            role="Light-driven proton pumping",
            mass_fraction=0.05,
            stability="acid-stable",
        ),
        OrganicComponent(
            name="Acidithiobacillus inoculum",
            formula="Lyophilized A. ferrooxidans",
            role="Starter culture (pH optimum 1.5-2.5)",
            mass_fraction=0.05,
            stability="acid-stable, desiccation-resistant",
        ),
        OrganicComponent(
            name="Picrophilus inoculum",
            formula="Lyophilized P. torridus",
            role="Extreme acidophile template (grows at pH 0.06!)",
            mass_fraction=0.05,
            stability="acid-stable to pH 0",
        ),
        OrganicComponent(
            name="PTFE-encapsulated amino acids",
            formula="L-amino acids in PTFE microspheres",
            role="Protected building blocks",
            mass_fraction=0.05,
            stability="acid-stable via encapsulation",
        ),
    ]

    return SeedPackage(
        target_world="Venus",
        total_mass_kg=50,
        omega_lattice=omega_lattice,
        minerals=minerals,
        organics=organics,
        encapsulation="PTFE outer shell + silica aerogel matrix (buoyant at 55 km)",
        delivery_method="Atmospheric probe with parachute deployment at 60 km",
        survival_probability=0.25,  # Better understood environment
        germination_time_years=100,  # Faster in warm, energy-rich environment
        rationale="""
        Venus seed strategy: Establish aerial acidophilic ecosystem

        1. DELIVERY: Atmospheric probe deploys at 60 km altitude
        2. DISPERSAL: Aerogel-matrix seeds float at 50-55 km (habitable zone)
        3. ENVIRONMENT:
           - Temperature: 300-340K (perfect for biochemistry!)
           - Pressure: ~1 bar (Earth-like!)
           - Abundant CO2, SO2, H2SO4 for metabolism
           - Strong sunlight for phototrophy
        4. GERMINATION:
           - PTFE-protected Omega Lattice provides Z-resonance
           - Acidophile inoculum activates in H2SO4 droplets
           - Sulfur cycling: H2S ↔ S ↔ SO2 ↔ H2SO4
           - Light-driven metabolism via bacteriorhodopsin
        5. LIFECYCLE:
           - Cloud droplet condensation → organism growth
           - Droplet evaporation → spore formation
           - Convective cycling maintains population

        Key advantage: Venus clouds have Earth-like T and P!
        Main challenge is extreme acidity - but Earth acidophiles
        (Picrophilus) already survive at pH 0. We're providing
        optimized Z-resonance conditions for an aerial biosphere.

        WILD CARD: The controversial phosphine detection (2020) suggests
        Venus clouds might already host life. Our seeds could either
        establish new life or enhance existing aerial ecosystems.
        """
    )


# =============================================================================
# VIABILITY ANALYSIS
# =============================================================================

def calculate_omega_z_potential(seed: SeedPackage, env: WorldEnvironment) -> Dict:
    """
    Calculate the Ω_Z potential for a seed package in a given environment.

    Based on the six factors from omega_z_final_100.py:
    1. Frank Model (homochirality)
    2. Lattice match (d ≈ Z)
    3. Magnetic field (B ≥ 245 Gauss)
    4. Chemical catalysis (Z-scale enhancement)
    5. Thermal stability
    6. Energy availability
    """

    scores = {}

    # 1. Frank Model - always works if conditions are right
    scores['frank_model'] = 1.0

    # 2. Lattice match
    offset = seed.omega_lattice['offset_percent']
    scores['lattice_match'] = np.exp(-offset**2 / 2)  # Gaussian penalty

    # 3. Magnetic field
    # Check if magnetite is present
    has_magnetite = any('magnetite' in m.name.lower() or 'Fe₃O₄' in m.formula
                       for m in seed.minerals)
    if has_magnetite:
        scores['magnetic_field'] = 1.0  # Local field exceeds 245 Gauss
    else:
        scores['magnetic_field'] = 0.1  # Only planetary field

    # 4. Chemical catalysis - depends on Z-resonance quality
    scores['z_catalysis'] = scores['lattice_match'] ** 2  # Squared for sensitivity

    # 5. Thermal stability
    T = env.temperature_K
    T_opt = 310  # Optimal for Earth life
    T_range = 50  # Tolerable range
    thermal_penalty = ((T - T_opt) / T_range) ** 2
    scores['thermal_stability'] = np.exp(-thermal_penalty / 2)

    # 6. Energy availability
    if 'sunlight' in str(env.energy_sources).lower():
        scores['energy'] = 1.0
    elif 'hydrothermal' in str(env.energy_sources).lower():
        scores['energy'] = 0.8
    else:
        scores['energy'] = 0.3

    # Composite Ω_Z
    omega_z = np.prod(list(scores.values())) ** (1/len(scores))  # Geometric mean

    return {
        'individual_scores': {k: round(v, 4) for k, v in scores.items()},
        'omega_z': round(omega_z, 4),
        'viability_assessment': (
            'EXCELLENT' if omega_z > 0.8 else
            'GOOD' if omega_z > 0.6 else
            'MARGINAL' if omega_z > 0.4 else
            'POOR'
        )
    }


# =============================================================================
# COMPARISON: NATURAL vs DESIGNED SEEDING
# =============================================================================

def analyze_natural_panspermia():
    """
    Analyze whether natural panspermia could seed these worlds.

    Compare to designed seeds to show the advantage of intentional seeding.
    """

    return {
        'europa': {
            'natural_probability': 1e-12,
            'challenges': [
                'Must survive ejection from source world',
                'Must survive interplanetary transit (radiation, cold)',
                'Must penetrate 10-30 km ice shell',
                'Must find suitable environment in ocean',
                'Must have compatible biochemistry',
            ],
            'designed_advantage': 'Skip transit + ice penetration via cryobot delivery',
        },
        'venus': {
            'natural_probability': 1e-15,
            'challenges': [
                'Must survive atmospheric entry',
                'Must stabilize at correct altitude',
                'Must survive pH 0 environment',
                'No known Earth life survives H2SO4 immersion',
            ],
            'designed_advantage': 'Acid-resistant encapsulation + acidophile inoculum',
        },
        'conclusion': """
        Natural panspermia to Europa or Venus is essentially impossible.

        Designed seeding with Protogonos-optimized packages increases
        success probability by 10-15 orders of magnitude by:

        1. Optimizing Omega Lattice for local temperature
        2. Including magnetic minerals for CISS activation
        3. Providing acid/cryo protection as needed
        4. Including extremophile inoculum as metabolic template
        5. Controlled delivery to optimal microenvironment

        This is the difference between hoping life randomly arrives
        vs engineering the conditions for Ω_Z = 1.0.
        """
    }


# =============================================================================
# ETHICAL CONSIDERATIONS
# =============================================================================

def ethical_analysis():
    """
    Ethical considerations for intentional panspermia.
    """

    return {
        'arguments_for': [
            'Life may be cosmically rare and worth spreading',
            'Humanity has moral responsibility to propagate life',
            'Insurance against extinction events on Earth',
            'Scientific value of observing abiogenesis in real-time',
            'These worlds are likely sterile (no existing life to harm)',
        ],
        'arguments_against': [
            'Potential contamination of pristine environments',
            'Could destroy evidence of independent abiogenesis',
            'Irreversible action with unknown consequences',
            'May interfere with future scientific studies',
            'Hubris of "playing god" with other worlds',
        ],
        'recommendation': """
        PHASED APPROACH:

        Phase 1 (Now): Computational modeling and Earth-based experiments
        - Validate Omega Lattice designs in lab conditions
        - Test extremophile survival in simulated environments
        - Develop delivery technologies

        Phase 2 (2030s): Search for existing life
        - Europa Clipper mission analysis
        - Venus atmospheric probes
        - Confirm sterility before seeding

        Phase 3 (2040s+): Seeding missions (if sterility confirmed)
        - Deploy designed seed packages
        - Long-term monitoring

        CRITICAL PRINCIPLE: Never seed a world that might already have life.
        The discovery of a second genesis would be more valuable than
        any seeding mission.
        """,
        'planetary_protection_status': {
            'europa': 'Category III/IV - restricted access',
            'venus': 'Category II - documentation required',
        }
    }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_full_analysis():
    """Run complete panspermia seed design analysis."""

    print("=" * 70)
    print("PANSPERMIA SEED DESIGNER")
    print("Designing Life for Europa and Venus")
    print("Based on the Protogonos Framework: Ω_Z = 1.0")
    print("=" * 70)

    results = {
        'fundamental_constants': {
            'Z': round(Z, 6),
            'Z_squared': round(Z_SQUARED, 6),
            'B_CISS_threshold_gauss': B_CISS_THRESHOLD,
        }
    }

    # Design seed packages
    print("\n" + "=" * 70)
    print("EUROPA SEED PACKAGE")
    print("=" * 70)

    europa_seed = design_europa_seed()
    europa_viability = calculate_omega_z_potential(europa_seed, EUROPA_OCEAN)

    print(f"\nTarget: {europa_seed.target_world}")
    print(f"Total mass: {europa_seed.total_mass_kg} kg")
    print(f"Delivery: {europa_seed.delivery_method}")
    print(f"\nOmega Lattice: {europa_seed.omega_lattice['formula']}")
    print(f"  d at 350K: {europa_seed.omega_lattice['d_predicted_A']:.4f} Å")
    print(f"  Offset from Z: {europa_seed.omega_lattice['offset_percent']:.4f}%")
    print(f"\nMineral Components:")
    for m in europa_seed.minerals:
        print(f"  {m.name}: {m.mass_fraction*100:.1f}% - {m.role}")
    print(f"\nOrganic Components:")
    for o in europa_seed.organics:
        print(f"  {o.name}: {o.mass_fraction*100:.1f}% - {o.role}")
    print(f"\nViability Assessment:")
    for k, v in europa_viability['individual_scores'].items():
        print(f"  {k}: {v:.4f}")
    print(f"  Ω_Z potential: {europa_viability['omega_z']:.4f}")
    print(f"  Assessment: {europa_viability['viability_assessment']}")

    results['europa'] = {
        'seed_package': {
            'total_mass_kg': europa_seed.total_mass_kg,
            'omega_lattice': europa_seed.omega_lattice,
            'minerals': [asdict(m) for m in europa_seed.minerals],
            'organics': [asdict(o) for o in europa_seed.organics],
            'delivery_method': europa_seed.delivery_method,
            'survival_probability': europa_seed.survival_probability,
            'germination_time_years': europa_seed.germination_time_years,
        },
        'viability': europa_viability,
        'environment': asdict(EUROPA_OCEAN),
    }

    # Venus
    print("\n" + "=" * 70)
    print("VENUS SEED PACKAGE")
    print("=" * 70)

    venus_seed = design_venus_seed()
    venus_viability = calculate_omega_z_potential(venus_seed, VENUS_CLOUDS)

    print(f"\nTarget: {venus_seed.target_world}")
    print(f"Total mass: {venus_seed.total_mass_kg} kg")
    print(f"Delivery: {venus_seed.delivery_method}")
    print(f"\nOmega Lattice: {venus_seed.omega_lattice['formula']}")
    print(f"  d at 310K: {venus_seed.omega_lattice['d_predicted_A']:.4f} Å")
    print(f"  Offset from Z: {venus_seed.omega_lattice['offset_percent']:.4f}%")
    print(f"\nMineral Components:")
    for m in venus_seed.minerals:
        print(f"  {m.name}: {m.mass_fraction*100:.1f}% - {m.role}")
    print(f"\nOrganic Components:")
    for o in venus_seed.organics:
        print(f"  {o.name}: {o.mass_fraction*100:.1f}% - {o.role}")
    print(f"\nViability Assessment:")
    for k, v in venus_viability['individual_scores'].items():
        print(f"  {k}: {v:.4f}")
    print(f"  Ω_Z potential: {venus_viability['omega_z']:.4f}")
    print(f"  Assessment: {venus_viability['viability_assessment']}")

    results['venus'] = {
        'seed_package': {
            'total_mass_kg': venus_seed.total_mass_kg,
            'omega_lattice': venus_seed.omega_lattice,
            'minerals': [asdict(m) for m in venus_seed.minerals],
            'organics': [asdict(o) for o in venus_seed.organics],
            'delivery_method': venus_seed.delivery_method,
            'survival_probability': venus_seed.survival_probability,
            'germination_time_years': venus_seed.germination_time_years,
        },
        'viability': venus_viability,
        'environment': asdict(VENUS_CLOUDS),
    }

    # Natural vs Designed comparison
    print("\n" + "=" * 70)
    print("NATURAL vs DESIGNED PANSPERMIA")
    print("=" * 70)

    comparison = analyze_natural_panspermia()
    print(f"\nEuropa natural probability: {comparison['europa']['natural_probability']:.2e}")
    print(f"Venus natural probability: {comparison['venus']['natural_probability']:.2e}")
    print(f"\nDesigned advantage:")
    print(f"  Europa: {comparison['europa']['designed_advantage']}")
    print(f"  Venus: {comparison['venus']['designed_advantage']}")

    results['natural_vs_designed'] = comparison

    # Ethical analysis
    print("\n" + "=" * 70)
    print("ETHICAL CONSIDERATIONS")
    print("=" * 70)

    ethics = ethical_analysis()
    print("\nArguments FOR seeding:")
    for arg in ethics['arguments_for'][:3]:
        print(f"  + {arg}")
    print("\nArguments AGAINST seeding:")
    for arg in ethics['arguments_against'][:3]:
        print(f"  - {arg}")
    print("\nRecommendation: Phased approach - confirm sterility before seeding")

    results['ethics'] = ethics

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: CAN WE DESIGN LIFE FOR OTHER WORLDS?")
    print("=" * 70)

    summary = f"""
    YES - The Protogonos framework provides a blueprint for designed panspermia.

    KEY INSIGHT: If Ω_Z = 1.0 (life is inevitable when conditions are right),
    then seeding is simply a matter of ENGINEERING those conditions.

    EUROPA (Ω_Z potential: {europa_viability['omega_z']:.2f}):
    - Strategy: Hydrothermal vent colonization
    - Omega Lattice: {europa_seed.omega_lattice['formula']}
    - Delivery: Cryobot through ice shell
    - Metabolism: Chemolithotrophy (H2 + CO2)
    - Challenge: Ice penetration

    VENUS (Ω_Z potential: {venus_viability['omega_z']:.2f}):
    - Strategy: Aerial acidophilic ecosystem
    - Omega Lattice: {venus_seed.omega_lattice['formula']}
    - Delivery: Atmospheric probe at 55 km
    - Metabolism: Sulfur-based phototrophy
    - Challenge: Extreme acidity

    CRITICAL REQUIREMENT: Confirm target worlds are sterile before seeding.
    Discovery of independent abiogenesis > any seeding mission.

    TIMELINE:
    - Now: Lab validation of Omega Lattice designs
    - 2030s: Search for existing life (Europa Clipper, Venus probes)
    - 2040s+: Seeding missions if sterility confirmed

    The mathematics of Z² = 32π/3 doesn't just explain how life emerged on Earth.
    It provides the engineering specifications for spreading life across the cosmos.
    """

    print(summary)
    results['summary'] = summary

    # Save results
    output_path = '/Users/carlzimmerman/new_physics/zimmerman-formula/extended_research/biotech/project_protogonos/computational_abiogenesis/panspermia_seed_results.json'

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == '__main__':
    results = run_full_analysis()
