#!/usr/bin/env python3
"""
POLAR CLIMATE PHYSICS - FIRST PRINCIPLES
=========================================

Deriving the physics of Arctic amplification, sea ice,
polar vortex, and high-latitude climate processes.
"""

import numpy as np

print("=" * 70)
print("POLAR CLIMATE PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
sigma = 5.67e-8    # Stefan-Boltzmann constant
L_f = 3.34e5       # Latent heat of fusion (J/kg)
rho_ice = 917      # Sea ice density (kg/m³)
rho_water = 1025   # Seawater density (kg/m³)
c_ice = 2100       # Specific heat of ice (J/kg/K)


# =============================================================================
# PART 1: POLAR RADIATION BUDGET
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: POLAR RADIATION BUDGET")
print("=" * 70)

radiation_text = """
POLAR RADIATION BUDGET:
=======================

Unique features at high latitudes:

1. LOW SOLAR INPUT
   Annual mean solar: ~100 W/m² at poles vs ~300 W/m² at equator
   Polar night: zero solar for months
   Polar day: 24-hr sun but low angle

2. HIGH ALBEDO
   Fresh snow: α = 0.8-0.9
   Sea ice: α = 0.5-0.7
   Open ocean: α = 0.06-0.1

   This matters for energy budget!

3. THERMAL EMISSION
   Cold surface emits less:
   F = εσT⁴
   At -30°C (243 K): F = 200 W/m²
   At +15°C (288 K): F = 390 W/m²

ANNUAL ENERGY DEFICIT:

Absorbed solar - Outgoing longwave < 0
Poles have NET ENERGY DEFICIT
Compensated by atmospheric/oceanic heat transport

POLAR AMPLIFICATION MECHANISM:

1. ICE-ALBEDO FEEDBACK
   Warming → ice melts → albedo drops → absorb more solar → more warming
   This is POSITIVE FEEDBACK

2. LAPSE RATE FEEDBACK
   Tropics: Deep convection, warming distributed vertically
   Arctic: Strong inversion, warming concentrated at surface
   Positive feedback in Arctic

3. PLANCK FEEDBACK
   ∂F/∂T = 4εσT³
   Cold regions: smaller increase in emission per K warming
   Less efficient radiative cooling

4. WATER VAPOR FEEDBACK
   Less important at poles (cold = dry)
   But still positive
"""
print(radiation_text)

def stefan_boltzmann_emission(T_kelvin, emissivity=0.97):
    """Calculate thermal emission (W/m²)."""
    return emissivity * sigma * T_kelvin**4

def absorbed_solar(S_incoming, albedo):
    """Calculate absorbed solar radiation."""
    return S_incoming * (1 - albedo)

def planck_feedback_parameter(T_kelvin):
    """
    Calculate Planck feedback parameter.

    λ_P = ∂F/∂T = 4εσT³
    """
    epsilon = 0.97
    return 4 * epsilon * sigma * T_kelvin**3

print("\nPlanck Feedback by Temperature:")
print("-" * 55)
print(f"{'Temperature (°C)':<18} {'T (K)':<12} {'λ_P (W/m²/K)':<18} {'Cooling efficiency'}")
print("-" * 55)

for T_C in [-40, -20, 0, 15, 30]:
    T_K = T_C + 273.15
    lambda_P = planck_feedback_parameter(T_K)
    print(f"{T_C:<18} {T_K:<12.1f} {lambda_P:<18.2f} {'Low' if T_C < -20 else 'High'}")


# =============================================================================
# PART 2: ARCTIC AMPLIFICATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: ARCTIC AMPLIFICATION")
print("=" * 70)

amplification_text = """
ARCTIC AMPLIFICATION:
=====================

OBSERVATION:
Arctic warming at 2-4× global average rate!

1980-2020:
- Global: +1.0°C
- Arctic: +3°C (some regions +5°C)

PHYSICAL MECHANISMS:

1. ICE-ALBEDO FEEDBACK (35% of amplification)

   α_ice ≈ 0.6
   α_ocean ≈ 0.06

   1 m² ice lost → +50 W/m² absorbed

   Seasonal: Most effective in summer
   Annual: September ice minimum drives annual anomaly

2. LAPSE RATE FEEDBACK (25% of amplification)

   Strong Arctic inversion:
   Warming stays near surface
   Not mixed through troposphere

   dT_surface / dT_troposphere > 1 in Arctic
                               < 1 in tropics

3. PLANCK FEEDBACK (15% of amplification)

   Cold = less efficient radiative cooling
   λ_P smaller at low T

4. WATER VAPOR + CLOUDS (10% of amplification)

   More moisture as ice retreats
   More low clouds in autumn/winter
   Clouds trap longwave radiation

5. OCEAN HEAT TRANSPORT (15% of amplification)

   Atlantic water advection into Arctic
   Heat released when water cools/ice forms

AMPLIFICATION FACTOR:

A = ΔT_Arctic / ΔT_global ≈ 2-4

Higher for winter, lower for summer
"""
print(amplification_text)

def ice_albedo_feedback_forcing(ice_area_lost_km2, solar_input_Wm2=200):
    """
    Calculate forcing from ice-albedo feedback.

    Area lost × (α_ice - α_ocean) × solar
    """
    delta_alpha = 0.6 - 0.06  # Albedo change
    area_m2 = ice_area_lost_km2 * 1e6
    forcing = delta_alpha * solar_input_Wm2 * area_m2
    return forcing / 1e12  # TW

def arctic_amplification_factor(ice_albedo_strength=0.35, lapse_rate_strength=0.25,
                                  planck_strength=0.15):
    """
    Estimate Arctic amplification from component feedbacks.

    Simplified linear combination.
    """
    # Total feedback contribution
    total_feedback = ice_albedo_strength + lapse_rate_strength + planck_strength + 0.25

    # Amplification relative to global (crude)
    amplification = 1 + total_feedback * 3
    return amplification

print("\nArctic Amplification Components:")
print("-" * 65)
components = [
    ("Ice-albedo feedback", 35),
    ("Lapse rate feedback", 25),
    ("Ocean heat transport", 15),
    ("Planck feedback", 15),
    ("Water vapor + clouds", 10),
]

print(f"{'Mechanism':<30} {'Contribution (%)'}")
print("-" * 65)
for mech, pct in components:
    print(f"{mech:<30} {pct}")

print(f"\nEstimated amplification factor: {arctic_amplification_factor():.1f}")


# =============================================================================
# PART 3: SEA ICE THERMODYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: SEA ICE THERMODYNAMICS")
print("=" * 70)

ice_text = """
SEA ICE PHYSICS:
================

FORMATION:

Seawater freezes at T_f ≈ -1.8°C (salinity dependent)
T_f = -0.054 × S (S in psu, T in °C)

ICE GROWTH (Stefan problem):

Heat conduction through ice → ocean heat → atmosphere

Growth rate:
dh/dt = k_ice × (T_f - T_surface) / (ρ_ice × L_f × h)

Where:
- k_ice ≈ 2.0 W/m/K (thermal conductivity)
- h = ice thickness

INTEGRATED:
h² ∝ ∫ (T_f - T_air) dt = Freezing Degree Days

h ≈ 0.03 × √(FDD) meters

ICE MELT:

Surface melt: Solar absorption + warm air
Bottom melt: Ocean heat flux

Melt rate:
dh/dt = -(Q_solar + Q_sensible + Q_ocean) / (ρ_ice × L_f)

MASS BALANCE:

Annual cycle:
- Winter: Growth from bottom
- Summer: Melt from top AND bottom
- Net: Depends on climate state

Multi-year ice: Survived at least one melt season
- Thicker (2-4 m)
- Lower salinity (brine drainage)
- Higher albedo

First-year ice:
- Thinner (0.3-2 m)
- More saline
- More vulnerable
"""
print(ice_text)

def freezing_temperature(salinity_psu=35):
    """Freezing point of seawater."""
    return -0.054 * salinity_psu

def ice_growth_stefan(FDD):
    """
    Ice thickness from freezing degree days.

    h ≈ 0.03 × √(FDD) meters
    """
    return 0.03 * np.sqrt(FDD)

def ice_growth_rate(T_air_C, h_current_m, T_freeze=-1.8):
    """
    Instantaneous ice growth rate.

    dh/dt = k(Tf - Ts) / (ρ L h)
    """
    k_ice = 2.0
    if h_current_m < 0.01:
        h_current_m = 0.01  # Minimum thickness

    # Surface temperature (simplified)
    T_surface = T_air_C if T_air_C < T_freeze else T_freeze

    dh_dt = k_ice * (T_freeze - T_surface) / (rho_ice * L_f * h_current_m)
    return dh_dt * 86400  # m/day

print("\nIce Growth from Freezing Degree Days:")
print("-" * 50)
print(f"{'FDD (°C·days)':<18} {'Ice thickness (m)':<20}")
print("-" * 50)

for FDD in [100, 500, 1000, 2000, 3000, 5000]:
    h = ice_growth_stefan(FDD)
    print(f"{FDD:<18} {h:<20.2f}")

print("\n\nIce Growth Rate vs Temperature and Thickness:")
print("-" * 55)
print(f"{'T_air (°C)':<12} {'h_ice (m)':<12} {'Growth rate (cm/day)'}")
print("-" * 55)

for T in [-10, -20, -30, -40]:
    for h in [0.1, 0.5, 1.0, 2.0]:
        rate = ice_growth_rate(T, h) * 100  # cm/day
        if h == 0.5:
            print(f"{T:<12} {h:<12} {rate:.2f}")


# =============================================================================
# PART 4: SEA ICE DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SEA ICE DYNAMICS")
print("=" * 70)

dynamics_text = """
SEA ICE MOTION:
===============

FORCES ON SEA ICE:

m × dv/dt = τ_air + τ_water + F_Coriolis + F_pressure + F_tilt

1. WIND STRESS (τ_air)
   τ_air = ρ_air × C_D × U_wind²
   Ice moves ~2% of wind speed

2. OCEAN STRESS (τ_water)
   Drag from underlying ocean

3. CORIOLIS
   Deflects ice motion to right (NH)
   Ice moves ~20-40° to right of wind

4. INTERNAL ICE STRESS
   Resistance to deformation
   Rheology: viscous-plastic

FREE DRIFT:
Far from coast, ice moves freely
Rule of thumb: ~2% of wind, 20° right (NH)

BEAUFORT GYRE:
Clockwise circulation in Arctic
Accumulates multi-year ice
Driven by atmospheric high pressure

TRANSPOLAR DRIFT:
Siberia → Fram Strait → Atlantic
Ice export from Arctic

ICE DEFORMATION:

RIDGING: Compression → thick ridges (10+ m keels)
RAFTING: Thin ice slides over each other
LEADS: Divergence → open water

MECHANICAL REDISTRIBUTION:
Even without thermodynamic change,
dynamics can change ice thickness distribution
"""
print(dynamics_text)

def ice_drift_speed(wind_speed_ms):
    """
    Estimate ice drift speed from wind.

    ~2% of wind speed in free drift.
    """
    return 0.02 * wind_speed_ms

def coriolis_deflection(latitude):
    """
    Deflection angle of ice motion from wind.

    Increases at lower latitudes.
    """
    # Simplified: ~20-40° to right of wind
    return 25 + 15 * np.cos(np.radians(latitude))

print("\nIce Drift from Wind:")
print("-" * 55)
print(f"{'Wind (m/s)':<15} {'Ice drift (cm/s)':<18} {'Deflection (°)'}")
print("-" * 55)

for wind in [5, 10, 15, 20, 25]:
    drift = ice_drift_speed(wind) * 100  # cm/s
    deflect = coriolis_deflection(75)  # At 75°N
    print(f"{wind:<15} {drift:<18.0f} {deflect:.0f}")


# =============================================================================
# PART 5: POLAR VORTEX AND ARCTIC OSCILLATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: POLAR VORTEX AND AO/NAO")
print("=" * 70)

vortex_text = """
POLAR VORTEX:
=============

TROPOSPHERIC POLAR VORTEX:

Band of westerlies surrounding polar region
Contains cold Arctic air

JET STREAM:
Core of strong westerlies at tropopause
Speed: 30-70 m/s
Meanders = Rossby waves

ARCTIC OSCILLATION (AO):

Leading mode of NH extratropical variability
Sea-level pressure seesaw: Arctic vs mid-latitudes

AO+ (Positive phase):
- Strong polar vortex
- Cold air confined to Arctic
- Mild winters in mid-latitudes
- Strong westerlies

AO- (Negative phase):
- Weak polar vortex
- Cold air outbreaks to mid-latitudes
- Blocking events
- Wavy jet stream

NORTH ATLANTIC OSCILLATION (NAO):

Regional expression of AO
Iceland Low vs Azores High

NAO+ → Strong westerlies → Mild, wet Europe
NAO- → Blocked flow → Cold Europe, warm Greenland

STRATOSPHERE-TROPOSPHERE COUPLING:

Sudden Stratospheric Warming (SSW):
- Stratospheric vortex breaks down
- Signal propagates downward
- Triggers AO-/cold outbreaks
- 2-4 week lag

CLIMATE CHANGE IMPACT:

Controversial! Two competing effects:
1. Less sea ice → more heat to atmosphere → weaker vortex?
2. Tropics warm more than Arctic in upper troposphere → stronger gradient?

Observed: More variable vortex, not clearly weaker
"""
print(vortex_text)

def ao_index_impact(ao_value):
    """
    Estimate AO impact on US/European temperatures.

    ao_value: standardized AO index
    Returns: approximate T anomaly
    """
    # Rough relationship
    us_anomaly = -1.0 * ao_value  # Negative AO = cold US
    europe_anomaly = 1.5 * ao_value  # Positive AO = warm Europe
    return us_anomaly, europe_anomaly

print("\nAO Index and Temperature Anomalies:")
print("-" * 60)
print(f"{'AO Index':<12} {'US temp anomaly (°C)':<22} {'Europe anomaly (°C)'}")
print("-" * 60)

for ao in [-2, -1, 0, 1, 2]:
    us, eu = ao_index_impact(ao)
    print(f"{ao:<12} {us:<22.1f} {eu:.1f}")


# =============================================================================
# PART 6: PERMAFROST PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: PERMAFROST PHYSICS")
print("=" * 70)

permafrost_text = """
PERMAFROST:
===========

Ground that remains frozen for ≥2 consecutive years

STRUCTURE:

Active layer: Seasonal thaw (0.3-3 m)
Permafrost table: Top of permafrost
Permafrost: Frozen ground below (to hundreds of meters)

THERMAL PROFILE:

Surface: Seasonal cycle
Depth: Amplitude decreases exponentially
At depth: Constant = mean annual ground temp

Temperature at depth z:
T(z,t) = T_mean + A × exp(-z/d) × cos(ωt - z/d)

Where d = √(2κ/ω) = damping depth

DISTRIBUTION:

Continuous permafrost: MAGT < -5°C (>90% coverage)
Discontinuous: MAGT -5 to 0°C
Sporadic: MAGT near 0°C
Isolated: Marginal areas

CARBON STORAGE:

Permafrost soils contain:
- ~1,500 Gt C (twice atmospheric CO₂!)
- Frozen organic matter
- Preserved for millennia

THAW PROCESSES:

1. ACTIVE LAYER DEEPENING
   - Gradual, top-down
   - ~1-2 cm/year

2. THERMOKARST
   - Rapid collapse
   - Ice-wedge melting
   - Lake formation

3. COASTAL EROSION
   - Wave action + thermal erosion
   - Meters per year in some areas

CARBON FEEDBACK:

Thaw → Decomposition → CO₂ + CH₄
Estimated: 50-250 Gt C released by 2100
Could add 0.1-0.3°C additional warming
"""
print(permafrost_text)

def active_layer_depth(magt_C, thaw_degree_days=1500):
    """
    Estimate active layer depth.

    Simplified Stefan equation approach.
    """
    # Active layer ∝ √(thaw degree days) / soil properties
    if magt_C > 0:
        return None  # No permafrost

    n_factor = 0.7  # Surface to air temperature ratio
    effective_TDD = thaw_degree_days * n_factor

    # Typical: 0.03-0.05 m per √(TDD)
    ald = 0.04 * np.sqrt(effective_TDD)
    return ald

def permafrost_carbon_release(warming_C, time_years=80):
    """
    Estimate cumulative carbon release from permafrost.

    Simplified relationship.
    """
    # ~10-15 Gt C per °C warming per century
    release_rate = 12 * warming_C  # Gt C per century
    total = release_rate * time_years / 100
    return total

print("\nActive Layer Depth vs Temperature:")
print("-" * 55)
print(f"{'MAGT (°C)':<15} {'TDD (°C·days)':<18} {'Active layer (m)'}")
print("-" * 55)

for tdd in [500, 1000, 1500, 2000, 2500]:
    ald = active_layer_depth(-5, tdd)
    if ald:
        print(f"{-5:<15} {tdd:<18} {ald:.2f}")

print("\n\nPermafrost Carbon Release Projections:")
print("-" * 50)
for warming in [1.5, 2.0, 3.0, 4.0]:
    release = permafrost_carbon_release(warming)
    print(f"+{warming}°C warming: ~{release:.0f} Gt C released by 2100")


# =============================================================================
# PART 7: ARCTIC-MIDLATITUDE LINKAGES
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: ARCTIC-MIDLATITUDE LINKAGES")
print("=" * 70)

linkage_text = """
ARCTIC INFLUENCE ON MID-LATITUDES:
==================================

PROPOSED MECHANISMS:

1. WEAKENED JET STREAM

   Less sea ice → warmer Arctic
   → Reduced pole-equator temperature gradient
   → Weaker jet stream?
   → More persistent weather patterns?

   CONTROVERSIAL: Evidence mixed

2. STRATOSPHERIC PATHWAY

   Sea ice loss → increased wave activity
   → Weakens stratospheric vortex
   → SSW events → AO negative
   → Cold outbreaks

   Better supported by observations

3. BLOCKING PATTERN CHANGES

   Hypothesis: More blocks with less ice
   Reality: No clear increase in blocking

OBSERVATIONAL EVIDENCE:

Strong:
- SSW → cold outbreaks (2-4 weeks)
- Barents-Kara ice → Siberian cold

Weak:
- Direct jet stream weakening
- Mid-latitude extreme weather attribution

THE COMPLEXITY:

1. Many other factors influence mid-lat weather
2. Internal variability is large
3. Signal-to-noise ratio is low
4. Tropical influences often dominate

CURRENT UNDERSTANDING:

Arctic warming CAN influence mid-latitudes
BUT: Effect is small compared to:
- Tropical forcing
- Internal variability
- Stratospheric variability
"""
print(linkage_text)

print("\nArctic-Midlatitude Pathway Summary:")
print("-" * 65)

pathways = [
    ("Stratospheric", "Ice loss → wave activity → SSW → AO- → cold", "Good"),
    ("Jet stream", "Reduced gradient → weaker jet → blocks", "Weak"),
    ("Direct thermal", "Warmer Arctic → less contrast → ??", "Unclear"),
    ("Tropical", "ENSO, MJO dominate midlat variability", "Strong"),
]

print(f"{'Pathway':<15} {'Mechanism':<40} {'Evidence'}")
print("-" * 65)
for path, mech, evid in pathways:
    print(f"{path:<15} {mech:<40} {evid}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: POLAR CLIMATE PHYSICS")
print("=" * 70)

summary = """
KEY POLAR PHYSICS:
=================

1. RADIATION BUDGET
   - Low solar input, high albedo
   - Net energy deficit
   - Weak Planck feedback (cold = inefficient cooling)

2. ARCTIC AMPLIFICATION
   - Warming 2-4× global average
   - Ice-albedo feedback: 35%
   - Lapse rate feedback: 25%
   - Ocean heat transport: 15%

3. SEA ICE THERMODYNAMICS
   - Growth: h ∝ √(FDD)
   - T_freeze ≈ -1.8°C (seawater)
   - Thickness: FY 0.3-2m, MY 2-4m

4. SEA ICE DYNAMICS
   - Drift ≈ 2% of wind, 25° right
   - Beaufort Gyre, Transpolar Drift
   - Ridging and leads

5. POLAR VORTEX / AO
   - AO+: Strong vortex, mild mid-lats
   - AO-: Weak vortex, cold outbreaks
   - SSW → AO- with 2-4 week lag

6. PERMAFROST
   - 1,500 Gt C stored
   - Active layer deepening
   - Carbon feedback: +0.1-0.3°C by 2100

7. ARCTIC-MIDLATITUDE
   - Stratospheric pathway: supported
   - Direct jet weakening: unclear
   - Effect smaller than tropical forcing


THE PHYSICS TELLS US:
====================
- Ice-albedo feedback dominates Arctic amplification
- Sea ice is key climate variable
- Permafrost is large carbon reservoir
- Arctic-midlatitude links exist but are subtle
- Polar regions are sentinels of climate change
"""
print(summary)

print("\n" + "=" * 70)
print("END OF POLAR CLIMATE PHYSICS")
print("=" * 70)
