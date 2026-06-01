#!/usr/bin/env python3
"""
================================================================================
EXOPLANET Ω_Z SURVEY - Deep Sweep of All Confirmed Exoplanets
================================================================================

Project Nephele / Protogonos Extension
Author: Carl Zimmerman + Claude
Date: May 2026

This script analyzes ALL confirmed exoplanets from the NASA Exoplanet Archive
and calculates their Ω_Z (Omega-Z) abiogenesis probability scores.

METHODOLOGY:
Since we cannot directly measure exoplanet mineralogy or magnetic fields,
we use proxies based on:
- Equilibrium temperature → thermal score, liquid water potential
- Stellar metallicity → likely mineralogy richness
- Planet mass/radius → magnetic field potential
- Stellar age → time available for abiogenesis
- Stellar type → energy availability, cosmic ray environment
- Orbital parameters → tidal heating, habitability zone

================================================================================
"""

import json
import math
import urllib.request
import urllib.parse
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z_CONSTANT = math.sqrt(32 * math.pi / 3)  # 5.7888 Å
CISS_THRESHOLD_GAUSS = 245
EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_KM = 6371
SOLAR_LUMINOSITY = 3.828e26  # Watts

# =============================================================================
# NASA EXOPLANET ARCHIVE QUERY
# =============================================================================

def fetch_exoplanet_data() -> List[Dict]:
    """
    Fetch confirmed exoplanets from NASA Exoplanet Archive TAP service.
    Returns list of planet dictionaries with key parameters.
    """

    # TAP query for confirmed planets with useful parameters
    query = """
    SELECT
        pl_name, hostname, sy_dist,
        pl_bmasse, pl_bmassj, pl_rade, pl_radj,
        pl_orbper, pl_orbsmax, pl_eqt,
        st_teff, st_rad, st_mass, st_age, st_met,
        pl_insol, sy_snum, sy_pnum,
        disc_year, discoverymethod
    FROM ps
    WHERE default_flag = 1
    AND pl_eqt IS NOT NULL
    ORDER BY pl_eqt ASC
    """

    # URL encode the query
    base_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": query,
        "format": "json"
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    print("Fetching exoplanet data from NASA Exoplanet Archive...")
    print(f"Query URL: {url[:100]}...")

    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = json.loads(response.read().decode())
            print(f"Retrieved {len(data)} confirmed exoplanets with temperature data")
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Using cached/fallback notable exoplanet list...")
        return get_notable_exoplanets()


def get_notable_exoplanets() -> List[Dict]:
    """
    Fallback list of notable potentially habitable exoplanets
    with manually curated data from NASA Exoplanet Archive.
    """
    return [
        # TRAPPIST-1 system - most promising
        {"pl_name": "TRAPPIST-1 d", "hostname": "TRAPPIST-1", "pl_bmasse": 0.388, "pl_rade": 0.788,
         "pl_eqt": 288, "st_teff": 2566, "st_age": 7.6, "st_met": 0.04, "pl_insol": 1.143,
         "pl_orbper": 4.05, "st_mass": 0.089, "disc_year": 2017},
        {"pl_name": "TRAPPIST-1 e", "hostname": "TRAPPIST-1", "pl_bmasse": 0.692, "pl_rade": 0.910,
         "pl_eqt": 251, "st_teff": 2566, "st_age": 7.6, "st_met": 0.04, "pl_insol": 0.662,
         "pl_orbper": 6.10, "st_mass": 0.089, "disc_year": 2017},
        {"pl_name": "TRAPPIST-1 f", "hostname": "TRAPPIST-1", "pl_bmasse": 1.039, "pl_rade": 1.045,
         "pl_eqt": 219, "st_teff": 2566, "st_age": 7.6, "st_met": 0.04, "pl_insol": 0.382,
         "pl_orbper": 9.21, "st_mass": 0.089, "disc_year": 2017},
        {"pl_name": "TRAPPIST-1 g", "hostname": "TRAPPIST-1", "pl_bmasse": 1.321, "pl_rade": 1.127,
         "pl_eqt": 199, "st_teff": 2566, "st_age": 7.6, "st_met": 0.04, "pl_insol": 0.258,
         "pl_orbper": 12.35, "st_mass": 0.089, "disc_year": 2017},

        # Proxima Centauri b - nearest
        {"pl_name": "Proxima Cen b", "hostname": "Proxima Cen", "pl_bmasse": 1.07, "pl_rade": 1.08,
         "pl_eqt": 234, "st_teff": 3042, "st_age": 4.85, "st_met": 0.21, "pl_insol": 0.65,
         "pl_orbper": 11.19, "st_mass": 0.122, "disc_year": 2016},

        # LHS 1140 b - super-Earth in HZ
        {"pl_name": "LHS 1140 b", "hostname": "LHS 1140", "pl_bmasse": 5.6, "pl_rade": 1.73,
         "pl_eqt": 235, "st_teff": 3216, "st_age": 5.0, "st_met": -0.24, "pl_insol": 0.43,
         "pl_orbper": 24.74, "st_mass": 0.179, "disc_year": 2017},

        # Kepler-442 b - high ESI
        {"pl_name": "Kepler-442 b", "hostname": "Kepler-442", "pl_bmasse": 2.34, "pl_rade": 1.34,
         "pl_eqt": 233, "st_teff": 4402, "st_age": 2.9, "st_met": -0.37, "pl_insol": 0.70,
         "pl_orbper": 112.3, "st_mass": 0.61, "disc_year": 2015},

        # Kepler-452 b - "Earth's cousin"
        {"pl_name": "Kepler-452 b", "hostname": "Kepler-452", "pl_bmasse": 5.0, "pl_rade": 1.63,
         "pl_eqt": 265, "st_teff": 5757, "st_age": 6.0, "st_met": 0.21, "pl_insol": 1.11,
         "pl_orbper": 384.8, "st_mass": 1.037, "disc_year": 2015},

        # K2-18 b - water vapor detected
        {"pl_name": "K2-18 b", "hostname": "K2-18", "pl_bmasse": 8.63, "pl_rade": 2.61,
         "pl_eqt": 284, "st_teff": 3457, "st_age": 2.4, "st_met": 0.12, "pl_insol": 1.0,
         "pl_orbper": 32.94, "st_mass": 0.495, "disc_year": 2015},

        # TOI-700 d - first TESS HZ Earth-size
        {"pl_name": "TOI-700 d", "hostname": "TOI-700", "pl_bmasse": 1.72, "pl_rade": 1.19,
         "pl_eqt": 269, "st_teff": 3480, "st_age": 1.5, "st_met": -0.06, "pl_insol": 0.86,
         "pl_orbper": 37.42, "st_mass": 0.415, "disc_year": 2020},

        # Teegarden's Star b
        {"pl_name": "Teegarden's Star b", "hostname": "Teegarden's Star", "pl_bmasse": 1.05, "pl_rade": 1.02,
         "pl_eqt": 264, "st_teff": 2904, "st_age": 8.0, "st_met": -0.19, "pl_insol": 1.15,
         "pl_orbper": 4.91, "st_mass": 0.089, "disc_year": 2019},

        # Ross 128 b
        {"pl_name": "Ross 128 b", "hostname": "Ross 128", "pl_bmasse": 1.40, "pl_rade": 1.11,
         "pl_eqt": 280, "st_teff": 3192, "st_age": 9.45, "st_met": -0.02, "pl_insol": 1.38,
         "pl_orbper": 9.87, "st_mass": 0.168, "disc_year": 2017},

        # GJ 667 C c
        {"pl_name": "GJ 667 C c", "hostname": "GJ 667 C", "pl_bmasse": 3.81, "pl_rade": 1.54,
         "pl_eqt": 277, "st_teff": 3350, "st_age": 6.0, "st_met": -0.55, "pl_insol": 0.88,
         "pl_orbper": 28.14, "st_mass": 0.33, "disc_year": 2011},

        # Kepler-186 f - first Earth-size in HZ
        {"pl_name": "Kepler-186 f", "hostname": "Kepler-186", "pl_bmasse": 1.71, "pl_rade": 1.17,
         "pl_eqt": 188, "st_teff": 3755, "st_age": 4.0, "st_met": -0.26, "pl_insol": 0.32,
         "pl_orbper": 129.9, "st_mass": 0.478, "disc_year": 2014},

        # Wolf 1061 c
        {"pl_name": "Wolf 1061 c", "hostname": "Wolf 1061", "pl_bmasse": 3.41, "pl_rade": 1.51,
         "pl_eqt": 223, "st_teff": 3342, "st_age": 7.2, "st_met": -0.02, "pl_insol": 1.3,
         "pl_orbper": 17.87, "st_mass": 0.294, "disc_year": 2015},

        # Gliese 12 b (recent discovery)
        {"pl_name": "Gliese 12 b", "hostname": "Gliese 12", "pl_bmasse": 1.0, "pl_rade": 1.0,
         "pl_eqt": 315, "st_teff": 3066, "st_age": 5.0, "st_met": 0.0, "pl_insol": 1.6,
         "pl_orbper": 12.76, "st_mass": 0.24, "disc_year": 2024},

        # LP 890-9 c (SPECULOOS)
        {"pl_name": "LP 890-9 c", "hostname": "LP 890-9", "pl_bmasse": 1.25, "pl_rade": 1.37,
         "pl_eqt": 272, "st_teff": 2850, "st_age": 7.2, "st_met": -0.03, "pl_insol": 0.906,
         "pl_orbper": 8.46, "st_mass": 0.118, "disc_year": 2022},

        # Some comparison planets (not in HZ)
        {"pl_name": "55 Cnc e", "hostname": "55 Cnc", "pl_bmasse": 8.0, "pl_rade": 1.88,
         "pl_eqt": 2573, "st_teff": 5196, "st_age": 10.2, "st_met": 0.31, "pl_insol": 2590,
         "pl_orbper": 0.74, "st_mass": 0.905, "disc_year": 2004},

        {"pl_name": "HD 189733 b", "hostname": "HD 189733", "pl_bmasse": 364, "pl_rade": 12.74,
         "pl_eqt": 1201, "st_teff": 5040, "st_age": 6.0, "st_met": -0.03, "pl_insol": 27.0,
         "pl_orbper": 2.22, "st_mass": 0.846, "disc_year": 2005},
    ]


# =============================================================================
# Ω_Z FACTOR CALCULATIONS
# =============================================================================

@dataclass
class ExoplanetOmegaZ:
    """Omega-Z calculation results for an exoplanet."""
    name: str
    host_star: str

    # Raw parameters
    mass_earth: Optional[float]
    radius_earth: Optional[float]
    eq_temp_K: Optional[float]
    stellar_age_gyr: Optional[float]
    stellar_metallicity: Optional[float]
    stellar_teff: Optional[float]
    insolation_earth: Optional[float]
    orbital_period_days: Optional[float]

    # Calculated Ω_Z factors
    thermal_score: float
    solvent_score: float
    magnetic_score: float
    mineral_score: float
    time_score: float
    energy_score: float
    chiral_score: float

    # Final scores
    omega_z_geometric: float
    omega_z_weighted: float
    omega_z_minimum: float

    # Category
    probability_category: str
    notes: str


def estimate_magnetic_field(mass_earth: float, radius_earth: float,
                            orbital_period_days: float) -> Tuple[float, float]:
    """
    Estimate planetary magnetic field strength.

    Based on scaling laws:
    - Magnetic field ~ (core mass) × (rotation rate) × (convection vigor)
    - Earth's field ~ 0.5 Gauss (surface average)
    - Tidally locked planets have weak/no fields

    Returns (field_gauss, magnetic_score)
    """
    if mass_earth is None or radius_earth is None:
        return 0.5, 0.5  # Earth-like default

    # Tidally locked planets (P < 30 days around M-dwarfs) have weak fields
    tidal_locked = orbital_period_days < 30

    # Core mass fraction scales with planet mass (roughly)
    # Super-Earths may have larger cores
    core_factor = min(2.0, mass_earth ** 0.5)

    # Rotation factor - tidally locked = slow rotation
    if tidal_locked:
        rotation_factor = 0.1
    else:
        rotation_factor = 1.0

    # Estimate surface field in Gauss
    # Earth = 0.5 Gauss
    field_gauss = 0.5 * core_factor * rotation_factor

    # For CISS, we need local mineral fields, not planetary
    # Assume magnetite inclusions can provide 4000+ Gauss locally
    # Score based on whether planet can have geologically active interior

    if mass_earth < 0.1:
        # Too small for sustained geology
        magnetic_score = 0.1
    elif mass_earth > 10:
        # Super-Earth - likely thick atmosphere, may have active interior
        magnetic_score = 0.6
    elif tidal_locked:
        # Tidally locked - weaker global field but may have crustal anomalies
        magnetic_score = 0.5
    else:
        # Earth-like mass and rotation
        magnetic_score = 0.8

    return field_gauss, magnetic_score


def estimate_mineral_score(stellar_metallicity: float) -> float:
    """
    Estimate likelihood of Z-resonant minerals based on stellar metallicity.

    Higher metallicity = more heavy elements = better chance of PbS, FeS, etc.
    Solar metallicity [Fe/H] = 0
    """
    if stellar_metallicity is None:
        return 0.5  # Unknown, assume average

    # Metallicity in dex (log scale relative to Sun)
    # [Fe/H] = -1 means 1/10th solar metals
    # [Fe/H] = +0.5 means ~3× solar metals

    # Z-resonant minerals need heavy elements (Pb, Fe, S)
    # Score peaks at slightly super-solar metallicity

    if stellar_metallicity < -0.5:
        # Metal-poor - unlikely to have galena, jarosite, etc.
        return 0.3
    elif stellar_metallicity < 0:
        # Sub-solar - still possible
        return 0.5 + stellar_metallicity * 0.4
    elif stellar_metallicity < 0.3:
        # Solar to moderately enhanced - optimal
        return 0.7 + stellar_metallicity * 0.5
    else:
        # Very metal-rich - excellent mineral potential
        return min(0.95, 0.8 + stellar_metallicity * 0.3)


def estimate_thermal_score(eq_temp_K: float) -> float:
    """
    Calculate thermal score based on equilibrium temperature.

    Optimal range: 250-320 K (liquid water, protein stability)
    """
    if eq_temp_K is None:
        return 0.0

    # Optimal temperature for life: ~280 K (Earth average)
    optimal = 280
    sigma = 50  # Width of habitable range

    # Gaussian scoring
    score = math.exp(-((eq_temp_K - optimal) ** 2) / (2 * sigma ** 2))

    # Hard cutoffs
    if eq_temp_K < 150 or eq_temp_K > 450:
        score *= 0.1  # Too extreme

    return min(1.0, score)


def estimate_solvent_score(eq_temp_K: float, insolation: float) -> float:
    """
    Estimate likelihood of liquid water or alternative solvent.
    """
    if eq_temp_K is None:
        return 0.0

    # Liquid water range: 273-373 K at 1 atm
    # But with pressure, can extend to 200-500 K

    if 200 <= eq_temp_K <= 350:
        # Good range for liquid water
        # Score peaks at ~280 K
        water_score = math.exp(-((eq_temp_K - 280) ** 2) / (2 * 40 ** 2))
        return max(0.3, water_score)
    elif 350 < eq_temp_K <= 450:
        # Possible water under pressure, or alternative solvents
        return 0.3
    elif 150 <= eq_temp_K < 200:
        # Possible cryogenic solvents (ammonia, methane)
        return 0.2
    else:
        # Too extreme
        return 0.05


def estimate_time_score(stellar_age_gyr: float) -> float:
    """
    Score based on time available for abiogenesis.

    Earth life took ~0.5-1.0 Gyr to emerge.
    More time = higher probability.
    """
    if stellar_age_gyr is None:
        return 0.5  # Unknown

    if stellar_age_gyr < 0.5:
        # Too young - not enough time
        return stellar_age_gyr / 0.5 * 0.3
    elif stellar_age_gyr < 1.0:
        # Possible but tight
        return 0.3 + (stellar_age_gyr - 0.5) * 0.8
    elif stellar_age_gyr < 4.0:
        # Good amount of time
        return 0.7 + (stellar_age_gyr - 1.0) / 3.0 * 0.2
    else:
        # Plenty of time
        return min(1.0, 0.9 + (stellar_age_gyr - 4.0) / 10.0 * 0.1)


def estimate_energy_score(stellar_teff: float, insolation: float) -> float:
    """
    Score based on energy availability for chemistry.

    Considers stellar type and insolation level.
    """
    if stellar_teff is None or insolation is None:
        return 0.5

    # Insolation relative to Earth
    if insolation < 0.2:
        # Very low energy - chemistry will be slow
        energy_from_star = 0.3
    elif insolation < 0.5:
        energy_from_star = 0.5
    elif insolation < 2.0:
        # Earth-like to moderately higher
        energy_from_star = 0.8
    else:
        # Very high - may be too intense (UV damage)
        energy_from_star = 0.6

    # M-dwarf flaring can provide UV energy
    if stellar_teff < 3500:
        flare_bonus = 0.1
    else:
        flare_bonus = 0

    return min(1.0, energy_from_star + flare_bonus)


def estimate_chiral_score(stellar_teff: float, orbital_period_days: float) -> float:
    """
    Score based on cosmic ray environment for chiral seeding.

    M-dwarfs have stronger stellar winds.
    Close-in planets get more particle flux.
    """
    if stellar_teff is None:
        return 0.7  # Default moderate

    # M-dwarfs (Teff < 4000 K) have more flares and particles
    if stellar_teff < 3000:
        stellar_factor = 1.0
    elif stellar_teff < 4000:
        stellar_factor = 0.9
    elif stellar_teff < 5500:
        stellar_factor = 0.8  # Sun-like
    else:
        stellar_factor = 0.7  # Hotter stars

    # Close-in planets get more flux (but also more radiation damage)
    if orbital_period_days and orbital_period_days < 10:
        proximity_factor = 0.9
    else:
        proximity_factor = 0.8

    return min(1.0, stellar_factor * proximity_factor / 0.8)


def calculate_omega_z(planet: Dict) -> ExoplanetOmegaZ:
    """
    Calculate complete Ω_Z score for an exoplanet.
    """
    name = planet.get("pl_name", "Unknown")
    host = planet.get("hostname", "Unknown")

    # Extract parameters
    mass = planet.get("pl_bmasse")
    radius = planet.get("pl_rade")
    eq_temp = planet.get("pl_eqt")
    age = planet.get("st_age")
    metallicity = planet.get("st_met")
    teff = planet.get("st_teff")
    insolation = planet.get("pl_insol")
    period = planet.get("pl_orbper")

    # Calculate individual factors
    thermal = estimate_thermal_score(eq_temp)
    solvent = estimate_solvent_score(eq_temp, insolation or 1.0)
    _, magnetic = estimate_magnetic_field(mass or 1.0, radius or 1.0, period or 30)
    mineral = estimate_mineral_score(metallicity)
    time = estimate_time_score(age)
    energy = estimate_energy_score(teff, insolation or 1.0)
    chiral = estimate_chiral_score(teff, period)

    # Aggregate scores
    factors = [thermal, solvent, magnetic, mineral, time, energy, chiral]

    # Geometric mean
    product = 1.0
    for f in factors:
        product *= max(0.01, f)  # Prevent zero
    geometric = product ** (1.0 / len(factors))

    # Weighted (thermal and solvent most important)
    weights = [0.20, 0.20, 0.15, 0.15, 0.10, 0.10, 0.10]
    weighted = sum(w * f for w, f in zip(weights, factors))

    # Minimum (bottleneck)
    minimum = min(factors)

    # Categorize
    if geometric >= 0.7:
        category = "HIGH (70-90%)"
    elif geometric >= 0.5:
        category = "MODERATE (50-70%)"
    elif geometric >= 0.3:
        category = "LOW (30-50%)"
    else:
        category = "VERY LOW (<30%)"

    # Notes
    notes_parts = []
    if eq_temp and 250 <= eq_temp <= 310:
        notes_parts.append("In habitable temperature range")
    if age and age > 4:
        notes_parts.append(f"Old system ({age:.1f} Gyr)")
    if metallicity and metallicity > 0.2:
        notes_parts.append("Metal-rich star")
    if mass and 0.5 <= mass <= 2.0:
        notes_parts.append("Earth-like mass")
    if period and period < 20:
        notes_parts.append("Likely tidally locked")

    notes = "; ".join(notes_parts) if notes_parts else "Limited data"

    return ExoplanetOmegaZ(
        name=name,
        host_star=host,
        mass_earth=mass,
        radius_earth=radius,
        eq_temp_K=eq_temp,
        stellar_age_gyr=age,
        stellar_metallicity=metallicity,
        stellar_teff=teff,
        insolation_earth=insolation,
        orbital_period_days=period,
        thermal_score=round(thermal, 3),
        solvent_score=round(solvent, 3),
        magnetic_score=round(magnetic, 3),
        mineral_score=round(mineral, 3),
        time_score=round(time, 3),
        energy_score=round(energy, 3),
        chiral_score=round(chiral, 3),
        omega_z_geometric=round(geometric, 3),
        omega_z_weighted=round(weighted, 3),
        omega_z_minimum=round(minimum, 3),
        probability_category=category,
        notes=notes
    )


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_exoplanet_survey():
    """Run the complete exoplanet Ω_Z survey."""

    print("=" * 80)
    print("EXOPLANET Ω_Z SURVEY - Z² Framework Deep Sweep")
    print("=" * 80)

    # Fetch data
    planets = fetch_exoplanet_data()

    # Calculate Ω_Z for each planet
    results = []
    for planet in planets:
        try:
            omega_z = calculate_omega_z(planet)
            results.append(omega_z)
        except Exception as e:
            print(f"Error processing {planet.get('pl_name', 'Unknown')}: {e}")

    # Sort by geometric Ω_Z score
    results.sort(key=lambda x: x.omega_z_geometric, reverse=True)

    # Print top candidates
    print("\n" + "=" * 80)
    print("TOP 20 EXOPLANETS BY Ω_Z SCORE")
    print("=" * 80)
    print(f"{'Rank':<5} {'Name':<25} {'Ω_Z':<8} {'Temp(K)':<8} {'Age(Gyr)':<10} {'Category':<20}")
    print("-" * 80)

    for i, r in enumerate(results[:20], 1):
        temp_str = f"{r.eq_temp_K:.0f}" if r.eq_temp_K else "?"
        age_str = f"{r.stellar_age_gyr:.1f}" if r.stellar_age_gyr else "?"
        print(f"{i:<5} {r.name:<25} {r.omega_z_geometric:<8.3f} {temp_str:<8} {age_str:<10} {r.probability_category:<20}")

    # Detailed breakdown for top 5
    print("\n" + "=" * 80)
    print("DETAILED Ω_Z BREAKDOWN - TOP 5 CANDIDATES")
    print("=" * 80)

    for i, r in enumerate(results[:5], 1):
        print(f"\n{i}. {r.name} (Host: {r.host_star})")
        print("-" * 50)
        print(f"   Ω_Z (geometric): {r.omega_z_geometric:.3f}")
        print(f"   Ω_Z (weighted):  {r.omega_z_weighted:.3f}")
        print(f"   Ω_Z (minimum):   {r.omega_z_minimum:.3f}")
        print(f"   Category:        {r.probability_category}")
        print(f"   Notes:           {r.notes}")
        print(f"\n   Factor Breakdown:")
        print(f"     Thermal:   {r.thermal_score:.3f}  (Eq. temp: {r.eq_temp_K or '?'} K)")
        print(f"     Solvent:   {r.solvent_score:.3f}  (Liquid water potential)")
        print(f"     Magnetic:  {r.magnetic_score:.3f}  (CISS activation)")
        print(f"     Mineral:   {r.mineral_score:.3f}  (Z-resonant minerals)")
        print(f"     Time:      {r.time_score:.3f}  (Age: {r.stellar_age_gyr or '?'} Gyr)")
        print(f"     Energy:    {r.energy_score:.3f}  (Stellar flux)")
        print(f"     Chiral:    {r.chiral_score:.3f}  (Cosmic ray environment)")

    # Statistics
    print("\n" + "=" * 80)
    print("SURVEY STATISTICS")
    print("=" * 80)

    high = sum(1 for r in results if r.omega_z_geometric >= 0.7)
    moderate = sum(1 for r in results if 0.5 <= r.omega_z_geometric < 0.7)
    low = sum(1 for r in results if 0.3 <= r.omega_z_geometric < 0.5)
    very_low = sum(1 for r in results if r.omega_z_geometric < 0.3)

    print(f"Total planets analyzed: {len(results)}")
    print(f"HIGH (Ω_Z ≥ 0.7):      {high} ({100*high/len(results):.1f}%)")
    print(f"MODERATE (0.5-0.7):    {moderate} ({100*moderate/len(results):.1f}%)")
    print(f"LOW (0.3-0.5):         {low} ({100*low/len(results):.1f}%)")
    print(f"VERY LOW (<0.3):       {very_low} ({100*very_low/len(results):.1f}%)")

    # Compare to solar system
    print("\n" + "=" * 80)
    print("COMPARISON TO SOLAR SYSTEM")
    print("=" * 80)
    print("Solar System Ω_Z scores for reference:")
    print("  Mars (Noachian):     0.95  - HIGHEST known")
    print("  Earth (Vents):       0.87")
    print("  Europa:              0.77")
    print("  Venus (Clouds):      0.74")
    print("  Enceladus:           0.38")
    print("  Titan:               0.22")

    top_exo = results[0] if results else None
    if top_exo:
        print(f"\nTop exoplanet {top_exo.name}: Ω_Z = {top_exo.omega_z_geometric:.3f}")
        if top_exo.omega_z_geometric >= 0.87:
            print("  → EXCEEDS Earth habitability!")
        elif top_exo.omega_z_geometric >= 0.74:
            print("  → Comparable to Venus clouds")
        elif top_exo.omega_z_geometric >= 0.5:
            print("  → Moderate potential")
        else:
            print("  → Below solar system habitable bodies")

    # Prepare output data
    output = {
        "metadata": {
            "analysis": "Exoplanet Ω_Z Survey",
            "date": datetime.now().isoformat(),
            "total_planets": len(results),
            "z_constant": Z_CONSTANT,
            "methodology": "Estimated factors based on available exoplanet parameters"
        },
        "statistics": {
            "high_probability": high,
            "moderate_probability": moderate,
            "low_probability": low,
            "very_low_probability": very_low
        },
        "top_candidates": [asdict(r) for r in results[:50]],
        "all_results": [asdict(r) for r in results],
        "solar_system_comparison": {
            "mars_noachian": 0.95,
            "earth": 0.87,
            "europa": 0.77,
            "venus": 0.74,
            "enceladus": 0.38,
            "titan": 0.22
        }
    }

    # Save results
    results_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(os.path.dirname(results_dir), "data", "results")
    os.makedirs(results_dir, exist_ok=True)

    output_path = os.path.join(results_dir, "exoplanet_omega_z_survey.json")
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return output


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_exoplanet_survey()
