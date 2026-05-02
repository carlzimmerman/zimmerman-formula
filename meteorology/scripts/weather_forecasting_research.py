#!/usr/bin/env python3
"""
WEATHER FORECASTING RESEARCH - FIRST PRINCIPLES
=================================================

Extending beyond hurricanes to other severe weather phenomena.
Using physics-based approaches with honest assessment.

Topics:
1. Severe Thunderstorm/Tornado Potential
2. Winter Storm Intensity
3. Derecho/Straight-line Wind Events
4. Atmospheric Rivers and Precipitation
5. Synthesis: What Physics Actually Predicts Well

Philosophy: Understand what's predictable vs chaotic
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, List

print("=" * 70)
print("WEATHER FORECASTING RESEARCH - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# PART 1: SEVERE THUNDERSTORM / TORNADO PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: SEVERE THUNDERSTORM / TORNADO PHYSICS")
print("=" * 70)

print("""
CONVECTIVE AVAILABLE POTENTIAL ENERGY (CAPE)
============================================

CAPE is the thermodynamic fuel for thunderstorms.
It measures buoyant energy available to lift air parcels.

Physics:
CAPE = ∫[LFC to EL] g × (T_parcel - T_env) / T_env × dz

Where:
- LFC = Level of Free Convection
- EL = Equilibrium Level
- T_parcel = temperature of rising parcel (moist adiabatic)
- T_env = environmental temperature

Units: J/kg (energy per unit mass)

CAPE Categories:
- < 1000 J/kg: Weak instability
- 1000-2500 J/kg: Moderate instability
- 2500-4000 J/kg: Strong instability
- > 4000 J/kg: Extreme instability
""")

def estimate_cape(
    surface_temp_c: float,
    surface_dewpoint_c: float,
    lapse_rate_c_per_km: float,
    tropopause_height_km: float = 12,
) -> float:
    """
    Simplified CAPE estimation.

    Real CAPE calculations require full soundings.
    This is an approximation based on surface conditions.
    """
    g = 9.81  # m/s²

    # Temperature excess (crude approximation)
    # Warmer surface + higher dewpoint = more lift potential
    surface_theta_e = surface_temp_c + 2.5 * surface_dewpoint_c / 10

    # Steeper lapse rate = more instability
    # Moist adiabatic is ~6.5°C/km, steeper = more CAPE
    lapse_excess = max(0, lapse_rate_c_per_km - 6.5)

    # Integration depth (LFC to EL, roughly)
    depth_km = min(tropopause_height_km - 2, 8)  # Cap at 8 km

    # Approximate CAPE
    cape = 20 * surface_theta_e * lapse_excess * depth_km

    return max(0, cape)


print("\nCAPE estimates for different environments:")
print("-" * 60)

environments = [
    ("Cool, dry (Canada winter)", 5, -5, 5.5),
    ("Mild, moderate (Spring)", 20, 12, 6.5),
    ("Warm, humid (Gulf Coast)", 30, 22, 7.0),
    ("Hot, very humid (Tornado Alley)", 35, 24, 8.0),
    ("Extreme (pre-outbreak)", 38, 26, 9.0),
]

print(f"{'Environment':<30} | {'Temp':>5} | {'Dew':>5} | {'Lapse':>6} | {'CAPE':>8}")
print("-" * 60)
for name, temp, dew, lapse in environments:
    cape = estimate_cape(temp, dew, lapse)
    print(f"{name:<30} | {temp:>5}°C | {dew:>5}°C | {lapse:>5.1f}°/km | {cape:>7.0f} J/kg")


print("""

WIND SHEAR AND ROTATION (HELICITY)
==================================

Tornadoes require ROTATION, not just instability.
Rotation comes from wind shear (wind changing with height).

Storm-Relative Helicity (SRH):
SRH = ∫[0 to h] (v × ∂u/∂z - u × ∂v/∂z) dz

Where u,v are storm-relative wind components.

SRH Categories (0-3 km):
- < 100 m²/s²: Weak rotation potential
- 100-250 m²/s²: Moderate (some tornadoes)
- 250-400 m²/s²: Strong (significant tornadoes)
- > 400 m²/s²: Extreme (violent tornadoes)
""")

def estimate_helicity(
    surface_wind_kt: float,
    surface_wind_dir: float,
    wind_500m_kt: float,
    wind_500m_dir: float,
    wind_3km_kt: float,
    wind_3km_dir: float,
) -> float:
    """
    Simplified helicity estimation from wind profile.

    Real helicity requires hodograph integration.
    """
    # Convert to m/s
    def kt_to_ms(kt):
        return kt * 0.514

    # Shear vector in 0-3km layer
    # Simplified: use directional change and speed shear

    # Speed shear
    speed_shear = abs(kt_to_ms(wind_3km_kt) - kt_to_ms(surface_wind_kt))

    # Directional shear (degrees to radians)
    dir_change = abs(wind_3km_dir - surface_wind_dir)
    if dir_change > 180:
        dir_change = 360 - dir_change

    # Veering (clockwise turn with height) is key for tornadoes
    # Southern Great Plains: typical 30-90° veering
    dir_change_rad = np.radians(dir_change)

    # Approximate helicity
    # SRH ≈ speed_shear × sin(directional_change) × depth
    helicity = speed_shear * np.sin(dir_change_rad) * 3000 * 0.3

    return max(0, helicity)


print("\nHelicity estimates for different wind profiles:")
print("-" * 70)

wind_profiles = [
    ("Weak shear", 10, 180, 15, 190, 25, 200),
    ("Moderate shear", 15, 180, 25, 210, 40, 240),
    ("Strong shear (supercell)", 20, 160, 35, 200, 55, 250),
    ("Extreme shear (outbreak)", 25, 150, 40, 200, 70, 270),
]

print(f"{'Profile':<25} | {'Sfc':>8} | {'3km':>8} | {'SRH':>10}")
print("-" * 70)
for name, sw, sd, w5, d5, w3, d3 in wind_profiles:
    srh = estimate_helicity(sw, sd, w5, d5, w3, d3)
    print(f"{name:<25} | {sw:>3}kt/{sd:>3}° | {w3:>3}kt/{d3:>3}° | {srh:>8.0f} m²/s²")


print("""

SIGNIFICANT TORNADO PARAMETER (STP)
===================================

Combined index that multiplies favorable ingredients:

STP = (CAPE/1500) × (SRH/150) × (Bulk_Shear/20) × (LCL_factor)

STP > 1: Significant tornadoes possible
STP > 4: Violent tornadoes possible
STP > 8: Major outbreak conditions

This is how operational meteorology works:
- Combine well-understood physics
- Create composite indices
- Calibrate against observed events
""")

def significant_tornado_parameter(
    cape: float,
    srh: float,
    bulk_shear_kt: float,
    lcl_height_m: float,
) -> float:
    """
    Simplified STP calculation.

    Real STP has additional terms and thresholds.
    """
    # Normalize components
    cape_term = cape / 1500
    srh_term = srh / 150
    shear_term = bulk_shear_kt / 20

    # LCL factor (low LCL = better for tornadoes)
    # LCL < 1000m is favorable
    if lcl_height_m < 1000:
        lcl_factor = 1.0
    elif lcl_height_m < 2000:
        lcl_factor = (2000 - lcl_height_m) / 1000
    else:
        lcl_factor = 0

    stp = cape_term * srh_term * shear_term * lcl_factor

    return max(0, stp)


print("\nSTP for different scenarios:")
print("-" * 60)

scenarios = [
    ("Weak afternoon storms", 1000, 50, 20, 1500),
    ("Isolated supercells", 2000, 150, 35, 1200),
    ("Significant tornadoes", 3000, 300, 50, 900),
    ("Major outbreak (April 27, 2011-like)", 5000, 500, 65, 700),
]

print(f"{'Scenario':<35} | {'CAPE':>6} | {'SRH':>6} | {'STP':>6}")
print("-" * 60)
for name, cape, srh, shear, lcl in scenarios:
    stp = significant_tornado_parameter(cape, srh, shear, lcl)
    print(f"{name:<35} | {cape:>6} | {srh:>6} | {stp:>6.1f}")


# =============================================================================
# PART 2: WINTER STORM PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: WINTER STORM PHYSICS")
print("=" * 70)

print("""
WINTER STORM INTENSITY
======================

Winter storms derive energy from temperature gradients (baroclinicity),
unlike tropical systems which use latent heat.

Key parameters:

1. BAROCLINIC ZONE
   Horizontal temperature gradient (°C per 100km)
   - Weak: < 3°C/100km
   - Moderate: 3-6°C/100km
   - Strong: 6-10°C/100km (intense cyclogenesis)

2. JET STREAM DYNAMICS
   Upper-level divergence drives surface low pressure
   Jet streak entrance/exit regions matter

3. MOISTURE AVAILABILITY
   Water vapor from oceans or Gulf of Mexico
   Limited by cold air temperatures

4. SNOW RATIO
   How fluffy the snow is (depends on temperature)
   - 10:1 ratio at 32°F → 10" snow per 1" liquid
   - 15:1 ratio at 15°F → fluffier snow
   - 20:1+ ratio at 0°F → very fluffy
""")

def miller_snowfall_equation(
    liquid_equivalent_in: float,
    surface_temp_f: float,
    column_temp_avg_c: float = -10,
) -> float:
    """
    Estimate snowfall from liquid equivalent.

    Uses temperature-dependent snow ratio.
    """
    # Snow ratio increases with colder temps
    if surface_temp_f > 30:
        ratio = 10
    elif surface_temp_f > 20:
        ratio = 12
    elif surface_temp_f > 10:
        ratio = 15
    elif surface_temp_f > 0:
        ratio = 18
    else:
        ratio = 20

    # Column temperature adjustment
    if column_temp_avg_c < -15:
        ratio *= 1.2  # Very fluffy
    elif column_temp_avg_c > -5:
        ratio *= 0.9  # Wet/heavy snow

    snowfall_in = liquid_equivalent_in * ratio

    return snowfall_in


print("\nSnowfall estimates for 1 inch liquid equivalent:")
print("-" * 50)
print(f"{'Surface Temp':>15} | {'Snow Ratio':>12} | {'Snowfall':>10}")
print("-" * 50)

for temp in [35, 30, 25, 20, 15, 10, 5, 0]:
    snow = miller_snowfall_equation(1.0, temp)
    ratio = snow / 1.0
    print(f"{temp:>12}°F | {ratio:>11.0f}:1 | {snow:>9.1f}\"")


print("""

BOMB CYCLONE CRITERION
======================

A "bomb" is a rapidly intensifying extratropical cyclone.

Definition: Pressure drop of ≥ 24 mb in 24 hours
            (adjusted for latitude: 24 × sin(lat)/sin(60°))

Physics: Strong baroclinicity + jet stream interaction
         = extreme divergence aloft = rapid surface deepening

Examples:
- 1993 Storm of the Century: 28 mb/24hr
- 2018 "Bomb Cyclone": 54 mb/24hr (rare!)
- 2022 Buffalo blizzard: 32 mb/24hr
""")


def bomb_cyclone_potential(
    temp_gradient_c_per_100km: float,
    jet_speed_kt: float,
    latitude: float = 40,
) -> Dict:
    """
    Estimate bomb cyclone potential.

    This is HIGHLY simplified. Real bomb forecasting
    requires full NWP model integration.
    """
    # Latitude adjustment for Bergeron criterion
    lat_factor = np.sin(np.radians(latitude)) / np.sin(np.radians(60))

    # Strong temperature gradient = fuel for cyclogenesis
    baroclinic_score = min(10, temp_gradient_c_per_100km)

    # Jet stream provides divergence mechanism
    jet_score = min(10, jet_speed_kt / 15)

    # Combined potential
    potential = baroclinic_score * jet_score / 10 * lat_factor

    # Expected deepening rate
    expected_mb_24hr = potential * 5  # Very crude

    if expected_mb_24hr > 24:
        category = "BOMB likely"
    elif expected_mb_24hr > 18:
        category = "Near-bomb possible"
    elif expected_mb_24hr > 12:
        category = "Significant deepening"
    else:
        category = "Weak to moderate"

    return {
        'deepening_rate': expected_mb_24hr,
        'category': category,
        'baroclinic_score': baroclinic_score,
        'jet_score': jet_score,
    }


print("\nBomb cyclone potential scenarios:")
print("-" * 65)
print(f"{'Scenario':<30} | {'ΔT grad':>8} | {'Jet':>6} | {'mb/24h':>8} | {'Category':<18}")
print("-" * 65)

bomb_scenarios = [
    ("Weak system", 2, 60),
    ("Moderate Nor'easter", 5, 100),
    ("Strong Nor'easter", 7, 130),
    ("Extreme bomb", 10, 180),
]

for name, grad, jet in bomb_scenarios:
    result = bomb_cyclone_potential(grad, jet)
    print(f"{name:<30} | {grad:>5}°C/100km | {jet:>5}kt | {result['deepening_rate']:>7.0f} | {result['category']:<18}")


# =============================================================================
# PART 3: ATMOSPHERIC RIVERS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: ATMOSPHERIC RIVERS")
print("=" * 70)

print("""
ATMOSPHERIC RIVER PHYSICS
=========================

Atmospheric rivers (ARs) are narrow corridors of concentrated
water vapor transport from tropics to mid-latitudes.

Key metric: INTEGRATED VAPOR TRANSPORT (IVT)
IVT = ∫[surface to top] (q × V) dp / g

Where:
- q = specific humidity (kg/kg)
- V = wind speed (m/s)
- dp = pressure layer

Units: kg/m/s (mass transport per unit width)

AR Categories (Ralph et al. scale):
- Cat 1 (Weak): IVT 250-500 kg/m/s
- Cat 2 (Moderate): IVT 500-750 kg/m/s
- Cat 3 (Strong): IVT 750-1000 kg/m/s
- Cat 4 (Extreme): IVT 1000-1250 kg/m/s
- Cat 5 (Exceptional): IVT > 1250 kg/m/s

Impact depends on DURATION and TERRAIN:
- Long-duration AR + mountains = major flooding
- Short-duration AR = beneficial precipitation
""")

def atmospheric_river_impact(
    ivt: float,
    duration_hr: float,
    terrain_enhancement: float = 1.5,
) -> Dict:
    """
    Estimate AR precipitation impact.

    Physics: IVT indicates moisture flux.
    Terrain forces uplift and precipitation.
    Duration determines total accumulation.
    """
    # Precipitation efficiency (simplified)
    # Higher IVT = more condensation potential
    precip_rate_mm_hr = ivt / 200  # Very crude

    # Terrain multiplier
    enhanced_rate = precip_rate_mm_hr * terrain_enhancement

    # Total precipitation
    total_mm = enhanced_rate * duration_hr

    # Impact category
    if ivt > 1250:
        ar_cat = 5
        label = "Exceptional"
    elif ivt > 1000:
        ar_cat = 4
        label = "Extreme"
    elif ivt > 750:
        ar_cat = 3
        label = "Strong"
    elif ivt > 500:
        ar_cat = 2
        label = "Moderate"
    elif ivt > 250:
        ar_cat = 1
        label = "Weak"
    else:
        ar_cat = 0
        label = "None"

    # Flood potential
    if total_mm > 400:
        flood = "EXTREME"
    elif total_mm > 200:
        flood = "HIGH"
    elif total_mm > 100:
        flood = "MODERATE"
    else:
        flood = "LOW"

    return {
        'ar_category': ar_cat,
        'ar_label': label,
        'total_precip_mm': total_mm,
        'flood_potential': flood,
    }


print("\nAtmospheric River Impact Scenarios:")
print("-" * 70)
print(f"{'Scenario':<30} | {'IVT':>6} | {'Duration':>10} | {'Precip':>8} | {'Flood':>10}")
print("-" * 70)

ar_scenarios = [
    ("Weak AR, short", 300, 12, 1.0),
    ("Moderate AR, 24hr", 600, 24, 1.5),
    ("Strong AR, 36hr, mountains", 800, 36, 2.0),
    ("Cat 5 AR, 48hr, mountains", 1300, 48, 2.5),  # Like Oroville 2017
]

for name, ivt, duration, terrain in ar_scenarios:
    result = atmospheric_river_impact(ivt, duration, terrain)
    print(f"{name:<30} | {ivt:>6} | {duration:>7}hr | {result['total_precip_mm']:>6.0f}mm | {result['flood_potential']:>10}")


# =============================================================================
# PART 4: WHAT PHYSICS ACTUALLY PREDICTS WELL
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: HONEST ASSESSMENT - PREDICTABILITY LIMITS")
print("=" * 70)

print("""
WHAT'S PREDICTABLE VS CHAOTIC IN WEATHER FORECASTING
====================================================

HIGH PREDICTABILITY (Days to Weeks):
------------------------------------
1. Large-scale patterns (jet stream, ridges, troughs)
2. Temperature trends (warm front passage, cold air outbreak)
3. Precipitation type (rain vs snow boundaries)
4. Tropical cyclone track (well-constrained by steering flow)
5. Atmospheric river arrival time

MODERATE PREDICTABILITY (1-3 Days):
-----------------------------------
1. Precipitation amounts (factor of 2 uncertainty)
2. Severe weather threat areas (100-200 km scale)
3. Winter storm totals (general categories)
4. TC intensity (inherent limits ~10-15 kt)

LOW PREDICTABILITY (Hours):
---------------------------
1. Exact tornado location (10 km scale)
2. Precise precipitation rates (mm/hr)
3. Exact timing of convective initiation
4. Small-scale wind gusts

ESSENTIALLY CHAOTIC:
--------------------
1. Which specific storm produces a tornado
2. Exact snowfall at specific address
3. Individual thunderstorm cell evolution
4. Precise TC intensity at landfall (± 15 kt)


WHY THESE LIMITS EXIST:
-----------------------
1. ATMOSPHERE IS CHAOTIC
   - Small perturbations grow exponentially
   - "Butterfly effect" is real
   - Predictability horizon: ~2 weeks for global patterns

2. OBSERVATION LIMITATIONS
   - Sparse data over oceans
   - Sub-grid scale processes
   - Unknown initial conditions

3. MODEL LIMITATIONS
   - Finite resolution (can't resolve individual thunderstorms)
   - Parameterization of unresolved processes
   - Computational constraints

4. INHERENT UNCERTAINTY
   - Some processes (turbulence, convection) are stochastic
   - No amount of computing can eliminate uncertainty
   - Ensembles quantify but don't eliminate uncertainty
""")


# =============================================================================
# PART 5: WHAT FIRST-PRINCIPLES APPROACH TEACHES US
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: LESSONS FROM FIRST-PRINCIPLES APPROACH")
print("=" * 70)

print("""
LESSONS LEARNED FROM THIS RESEARCH:
===================================

1. PHYSICS-BASED REASONING IS VALUABLE
   ✓ Understanding WHY storms work helps intuition
   ✓ Conservation laws constrain possible behavior
   ✓ Thermodynamics determines energy budget
   ✓ Can identify key parameters without simulating

2. BUT QUANTIFICATION IS HARD
   ✗ Translating physics to numbers requires calibration
   ✗ Multiple effects interact nonlinearly
   ✗ Empirical coefficients dominate formulas
   ✗ Without validation, numbers are meaningless

3. COMPOSITE INDICES WORK WHEN CALIBRATED
   ✓ CAPE + shear → tornado potential (validated)
   ✓ IVT + duration → AR impact (validated)
   ✓ Temperature gradient + jet → bomb potential (validated)

4. RANKING IS MORE RELIABLE THAN PREDICTION
   ✓ "A is more dangerous than B" (useful)
   ✗ "A will produce exactly X" (often wrong)

5. OPERATIONAL MODELS EXIST FOR A REASON
   - 50+ years of calibration and validation
   - Continuous improvement from forecast verification
   - Ensemble approaches quantify uncertainty
   - Don't reinvent the wheel


WHAT THIS RESEARCH IS GOOD FOR:
-------------------------------
✓ Building intuition about weather processes
✓ Understanding what makes extreme weather
✓ Risk ranking and comparative analysis
✓ Educational tool for physics concepts

WHAT THIS RESEARCH IS NOT:
--------------------------
✗ Replacement for NWP models
✗ Operational forecasting tool
✗ Validated prediction system
✗ Source for life-safety decisions


RECOMMENDED APPROACH:
--------------------
1. Use first-principles to understand mechanisms
2. Leverage validated operational products for forecasts
3. Focus research on calibration and validation
4. Quantify uncertainty always
5. Be honest about limitations
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("RESEARCH SUMMARY")
print("=" * 70)

print("""
WEATHER PHENOMENA COVERED:
--------------------------
1. SEVERE THUNDERSTORMS / TORNADOES
   - CAPE provides instability (fuel)
   - Wind shear provides rotation
   - STP combines both for risk assessment
   - Individual tornado prediction is chaotic

2. WINTER STORMS
   - Temperature gradients drive cyclogenesis
   - Jet stream provides energy extraction mechanism
   - Snow ratios depend on temperature
   - Bomb cyclones from extreme baroclinicity

3. ATMOSPHERIC RIVERS
   - IVT quantifies moisture transport
   - Duration × IVT × terrain = flood potential
   - California floods from extreme ARs

4. FLASH FLOODS (covered earlier)
   - Rainfall rate × duration × coverage = total
   - Terrain amplifies, saturation maximizes runoff
   - Slow storms most dangerous

COMMON THREAD:
--------------
All severe weather requires:
1. ENERGY SOURCE (instability, temperature gradient, moisture)
2. TRIGGER MECHANISM (lift, fronts, jet dynamics)
3. FAVORABLE ENVIRONMENT (shear, moisture, terrain)

First-principles helps understand these requirements.
Operational models quantify them with validated algorithms.
Research should bridge intuition and validation.

NEXT RESEARCH DIRECTIONS:
-------------------------
1. Validation against historical events
2. Calibration of empirical coefficients
3. Comparison with operational model output
4. Ensemble/probabilistic extensions
5. Machine learning on parameter relationships
""")

print("\n" + "=" * 70)
print("END OF WEATHER FORECASTING RESEARCH")
print("=" * 70)
