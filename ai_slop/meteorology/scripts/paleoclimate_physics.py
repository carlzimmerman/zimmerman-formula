#!/usr/bin/env python3
"""
PALEOCLIMATE PHYSICS - FIRST PRINCIPLES
========================================

Deriving ice age cycles, Milankovitch theory,
ice sheet dynamics, and past climate variability.
"""

import numpy as np

print("=" * 70)
print("PALEOCLIMATE PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
S_0 = 1361         # Solar constant (W/m²)
sigma = 5.67e-8    # Stefan-Boltzmann constant
R_earth = 6.371e6  # Earth radius (m)
g = 9.81           # Gravity (m/s²)


# =============================================================================
# PART 1: MILANKOVITCH CYCLES
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: MILANKOVITCH CYCLES - ORBITAL FORCING")
print("=" * 70)

milankovitch_text = """
MILANKOVITCH THEORY:
====================

Earth's orbital variations modulate insolation
→ Drives glacial-interglacial cycles

THREE ORBITAL PARAMETERS:

1. ECCENTRICITY (e)
   - Shape of Earth's orbit
   - Current: e ≈ 0.017 (nearly circular)
   - Range: 0.005 to 0.058
   - Periods: ~100,000 and ~400,000 years

   Effect: Varies Earth-Sun distance
   ΔS/S ≈ 2e × cos(ω)  (where ω = longitude of perihelion)
   Up to ±3% insolation variation

2. OBLIQUITY (ε)
   - Axial tilt
   - Current: ε ≈ 23.44°
   - Range: 22.1° to 24.5°
   - Period: ~41,000 years

   Effect: Seasonality!
   Higher tilt → stronger seasons
   More summer insolation at high latitudes

3. PRECESSION
   - Wobble of rotation axis
   - Period: ~23,000 years (19-26 ka range)
   - "Precession of the equinoxes"

   Effect: Timing of seasons relative to orbit
   When Northern summer at perihelion → warmer NH summers

THE KEY INSIGHT (Milankovitch):

Ice ages controlled by SUMMER insolation at 65°N!

Why 65°N?
- Most Northern Hemisphere land at high latitudes
- Ice sheets nucleate in Canada, Scandinavia
- If summer too cool to melt winter snow → ice accumulates

SUMMER INSOLATION AT 65°N:

Q_summer ≈ Q₀ × [1 + e×sin(ω)] × cos(ε - latitude)

Current: ~440 W/m² (June 21, 65°N)
Range: ~410-490 W/m²  (80 W/m² variation!)
"""
print(milankovitch_text)

def eccentricity_effect(eccentricity, longitude_perihelion_deg):
    """
    Calculate insolation variation from eccentricity.

    Returns fractional change from circular orbit.
    """
    omega = np.radians(longitude_perihelion_deg)
    delta_S = 2 * eccentricity * np.cos(omega)
    return delta_S

def obliquity_summer_insolation(obliquity_deg, latitude_deg=65):
    """
    Summer solstice insolation at latitude.

    Simplified: proportional to cos(latitude - obliquity) at noon
    """
    # Maximum solar elevation at summer solstice
    max_elevation = 90 - abs(latitude_deg - obliquity_deg)
    # Daily average factor (simplified)
    Q_factor = np.cos(np.radians(latitude_deg - obliquity_deg))
    return S_0 / 4 * Q_factor * 2  # Rough scaling

def precession_index(eccentricity, longitude_perihelion_deg):
    """
    Precession index: e × sin(ω)

    Measures timing of seasons relative to orbit.
    """
    omega = np.radians(longitude_perihelion_deg)
    return eccentricity * np.sin(omega)

print("\nMilankovitch Parameters:")
print("-" * 70)
print(f"{'Parameter':<15} {'Current':<15} {'Range':<20} {'Period (kyr)'}")
print("-" * 70)

params = [
    ("Eccentricity", "0.017", "0.005-0.058", "100, 400"),
    ("Obliquity", "23.44°", "22.1-24.5°", "41"),
    ("Precession", "~0 now", "±0.058", "23"),
]

for param, current, range_val, period in params:
    print(f"{param:<15} {current:<15} {range_val:<20} {period}")

print("\n\nSummer Insolation at 65°N vs Obliquity:")
print("-" * 50)
print(f"{'Obliquity (°)':<18} {'Q_summer (W/m²)':<20}")
print("-" * 50)

for obl in [22.0, 22.5, 23.0, 23.5, 24.0, 24.5]:
    Q = obliquity_summer_insolation(obl)
    print(f"{obl:<18} {Q:.0f}")


# =============================================================================
# PART 2: ICE AGE CYCLES
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: PLEISTOCENE ICE AGE CYCLES")
print("=" * 70)

iceage_text = """
PLEISTOCENE ICE AGE RECORD:
===========================

Past 2.6 million years: Repeated glaciations

ICE CORE AND MARINE SEDIMENT DATA:

Source                What it measures
─────────────────────────────────────────────────
Antarctic ice cores   Temperature (δ¹⁸O), CO₂, dust
Greenland ice cores   Temperature, accumulation, methane
Marine sediments      Ice volume (δ¹⁸O in forams)
Loess deposits        Dust flux, vegetation

THE 100,000 YEAR PROBLEM:

Observation: Dominant cycle is ~100 kyr
But: Eccentricity forcing is WEAK!

100 kyr cycle only emerged ~800 ka
Before: 41 kyr cycles dominated

EXPLANATIONS:
1. Nonlinear response to weak forcing
2. Ice sheet dynamics have ~100 kyr timescale
3. Carbon cycle feedbacks
4. CO₂ provides the "extra push"

GLACIAL-INTERGLACIAL CHANGES:

                        Glacial (LGM)    Interglacial
─────────────────────────────────────────────────────
Global T               -5 to -6°C        Baseline
Sea level              -120 m            Baseline
CO₂                    180 ppm           280 ppm
CH₄                    350 ppb           700 ppb
Ice sheet volume       +50×10⁶ km³       ~current

THE SEQUENCE:

Glaciation:
1. Insolation drops (Milankovitch)
2. Snow survives summer
3. Ice albedo feedback amplifies cooling
4. Ice sheets grow (takes ~90 kyr!)
5. CO₂ drops (ocean uptake, vegetation)

Deglaciation:
1. Insolation rises
2. Ice begins melting
3. CO₂ rises from ocean outgassing
4. Rapid warming (greenhouse amplification)
5. Full deglaciation in ~10 kyr (asymmetric!)
"""
print(iceage_text)

def ice_volume_proxy(insolation_anomaly, co2_ppm, lag_kyr=8):
    """
    Simple model of ice volume response.

    Ice volume responds to both insolation and CO₂
    with ~8 kyr lag for ice sheet dynamics.
    """
    # Normalize
    insol_forcing = -insolation_anomaly / 50  # Cooling → ice growth
    co2_forcing = (co2_ppm - 230) / 50  # CO₂ departure from midpoint

    # Ice volume anomaly
    ice_anomaly = insol_forcing - co2_forcing

    return ice_anomaly

def sea_level_from_ice(ice_volume_anomaly, baseline_m=0):
    """
    Sea level change from ice volume.

    ~1.5 m per 10⁶ km³ ice
    """
    return baseline_m - ice_volume_anomaly * 3

print("\nGlacial Cycle Characteristics:")
print("-" * 65)

cycles = [
    ("Last Glacial Maximum", 21, -6, 180, -120, 50),
    ("Penultimate glaciation", 140, -6, 185, -120, 48),
    ("MIS 11 (long interglacial)", 400, +1, 285, +10, 0),
    ("Pliocene (warm)", 3000, +3, 380, +25, 0),
]

print(f"{'Event':<25} {'Age (ka)':<10} {'ΔT (°C)':<10} {'CO₂ ppm':<10} {'Sea (m)'}")
print("-" * 65)

for event, age, dT, co2, sea, ice in cycles:
    print(f"{event:<25} {age:<10} {dT:<10} {co2:<10} {sea}")


# =============================================================================
# PART 3: ICE SHEET DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: ICE SHEET PHYSICS")
print("=" * 70)

icesheet_text = """
ICE SHEET DYNAMICS:
===================

Ice sheets are not static!
They flow, grow, and collapse.

ICE FLOW (GLEN'S FLOW LAW):

Strain rate: ε̇ = A × τⁿ

Where:
- A = rate factor (temperature dependent)
- τ = shear stress
- n ≈ 3 (nonlinear!)

Shear stress in ice: τ = ρ_ice × g × H × sin(α)

Ice velocity: U ∝ τⁿ × H ∝ H^(n+1) × (dh/dx)ⁿ

ICE SHEET MASS BALANCE:

∂H/∂t = ȧ - ṁ - ∇·(H×U)

Where:
- ȧ = accumulation (snowfall)
- ṁ = ablation (melting)
- ∇·(H×U) = ice flux divergence

EQUILIBRIUM LINE ALTITUDE (ELA):

Where accumulation = ablation
Below ELA: Net melting
Above ELA: Net accumulation

ELA drops 100-150 m per °C cooling!

RESPONSE TIMES:

Ice sheet shape adjustment: ~10,000 years
Volume adjustment: ~50,000-100,000 years
(This is why 100 kyr cycles exist!)

ICE SHEET INSTABILITIES:

1. MARINE ICE SHEET INSTABILITY (MISI)
   - Ice grounded below sea level
   - Deeper bed → thicker ice → faster flow
   - Positive feedback → rapid collapse

2. MARINE ICE CLIFF INSTABILITY (MICI)
   - Tall ice cliffs fail by fracture
   - If cliff > ~100 m, structurally unstable

These explain rapid deglaciation events!
"""
print(icesheet_text)

def glen_flow_law(shear_stress, A=1e-16, n=3):
    """
    Glen's flow law for ice.

    Returns strain rate (s⁻¹)
    """
    return A * shear_stress**n

def ice_velocity_estimate(thickness_m, slope, n=3):
    """
    Estimate ice sheet surface velocity.

    Simplified from integration of Glen's law.
    """
    rho_ice = 917  # kg/m³
    A = 1e-16  # Flow rate factor

    tau = rho_ice * g * thickness_m * slope
    # Velocity ∝ τⁿ × H
    U = A * tau**n * thickness_m / (n + 1) * 3.15e7  # m/year
    return U

def equilibrium_line_altitude(T_mean, precip_m_yr, baseline_ela=3000):
    """
    Estimate ELA from temperature and precipitation.
    """
    # ELA rises ~150 m per °C warming
    # ELA rises with more precip (counteracting)
    ela = baseline_ela + 150 * T_mean - 200 * (precip_m_yr - 1)
    return ela

print("\nIce Sheet Flow Velocities:")
print("-" * 60)
print(f"{'Thickness (m)':<18} {'Slope':<12} {'Velocity (m/yr)'}")
print("-" * 60)

for H in [500, 1000, 2000, 3000]:
    for slope in [0.001, 0.01, 0.05]:
        U = ice_velocity_estimate(H, slope)
        if slope == 0.01:
            print(f"{H:<18} {slope:<12} {U:.1f}")


# =============================================================================
# PART 4: CARBON CYCLE FEEDBACKS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: CARBON CYCLE IN ICE AGES")
print("=" * 70)

carbon_text = """
CO₂ AND ICE AGE CYCLES:
=======================

CO₂ varies 180-280 ppm over glacial cycles
This is NOT the initial driver but AMPLIFIER!

GLACIAL CO₂ DRAWDOWN:

Multiple mechanisms reduce CO₂:

1. OCEAN SOLUBILITY
   - Colder water holds more CO₂
   - ΔT = -5°C → ~30 ppm drop

2. OCEAN CIRCULATION
   - Reduced ventilation of deep water
   - CO₂ trapped in deep ocean
   - Most important: ~50 ppm

3. IRON FERTILIZATION
   - More dust in glacials (dry, windy)
   - Iron to Southern Ocean
   - Increased productivity
   - ~20 ppm

4. TERRESTRIAL BIOSPHERE
   - Less vegetation (smaller, drier continents)
   - But effects small for CO₂

DEGLACIAL CO₂ RISE:

Rapid rise as ocean releases CO₂:
- Southern Ocean ventilation increases
- Deep water upwells
- Absorbed CO₂ returns to atmosphere

CO₂ FORCING:

ΔF = 5.35 × ln(C₂/C₁) W/m²

180 → 280 ppm: ΔF = 2.4 W/m²

Combined with albedo: Amplification factor ~2-3
Explains why small orbital forcing → large response
"""
print(carbon_text)

def co2_forcing(co2_initial, co2_final):
    """
    CO₂ radiative forcing (W/m²).
    """
    return 5.35 * np.log(co2_final / co2_initial)

def temperature_from_co2(co2_ppm, co2_baseline=280, sensitivity=3.0):
    """
    Temperature change from CO₂.

    sensitivity: Climate sensitivity (°C per doubling)
    """
    dF = co2_forcing(co2_baseline, co2_ppm)
    dF_2x = 5.35 * np.log(2)  # Forcing for doubling
    dT = sensitivity * dF / dF_2x
    return dT

print("\nCO₂ Forcing Across Glacial Cycle:")
print("-" * 55)
print(f"{'CO₂ (ppm)':<15} {'ΔF from 280 (W/m²)':<25} {'ΔT (°C, λ=3)'}")
print("-" * 55)

for co2 in [180, 200, 220, 240, 260, 280, 300, 400, 560]:
    dF = co2_forcing(280, co2)
    dT = temperature_from_co2(co2)
    print(f"{co2:<15} {dF:<25.2f} {dT:+.1f}")


# =============================================================================
# PART 5: ABRUPT CLIMATE CHANGES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ABRUPT CLIMATE CHANGES")
print("=" * 70)

abrupt_text = """
DANSGAARD-OESCHGER EVENTS:
==========================

Rapid warmings during last glacial period

CHARACTERISTICS:
- 25+ events in last 100,000 years
- Warming: 8-15°C in decades!
- Greenland record shows sawtooth pattern
- Slow cooling over centuries, then abrupt warming

MECHANISM: ATLANTIC OVERTURNING

"Bipolar seesaw":
1. AMOC (Atlantic Meridional Overturning) weakens
2. Heat accumulates in Southern Ocean
3. Antarctic warms slowly
4. Eventually deep water formation resumes
5. Rapid transport of heat to North → abrupt warming

HEINRICH EVENTS:

Massive iceberg discharges from Laurentide Ice Sheet

- Ice-rafted debris in North Atlantic sediments
- Fresh water pulse shuts down AMOC
- Extreme cooling in North Atlantic
- ~6 major events in last glacial

YOUNGER DRYAS (12.9-11.7 ka):

Last major cold reversal during deglaciation
- Greenland: 10°C cooling
- Duration: 1,200 years
- Trigger: Lake Agassiz drainage? Cosmic impact?

LESSONS FOR FUTURE:

- Climate can change FAST
- Thresholds and tipping points exist
- AMOC is vulnerable to freshwater input
- Past is prologue (but not perfect analog)
"""
print(abrupt_text)

def amoc_shutdown_cooling(latitude_deg):
    """
    Estimate regional cooling from AMOC shutdown.

    Maximum in North Atlantic, decreases southward.
    """
    if latitude_deg > 50:
        return -10  # °C, extreme
    elif latitude_deg > 30:
        return -5
    elif latitude_deg > 10:
        return -2
    else:
        return +1  # Southern Hemisphere warming!

print("\nAMOC Shutdown Impacts:")
print("-" * 50)
print(f"{'Region':<30} {'ΔT (°C)'}")
print("-" * 50)

regions = [
    ("Greenland", 70),
    ("Northern Europe", 55),
    ("Northeast US", 45),
    ("Mediterranean", 35),
    ("Tropics", 5),
    ("Southern Ocean", -55),
]

for region, lat in regions:
    dT = amoc_shutdown_cooling(lat)
    print(f"{region:<30} {dT:+}")


# =============================================================================
# PART 6: DEEP TIME CLIMATE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: DEEP TIME CLIMATE")
print("=" * 70)

deeptime_text = """
CLIMATE OVER EARTH HISTORY:
===========================

FAINT YOUNG SUN PARADOX:

Solar luminosity: L = L₀ × (1 + 0.4 × t/4.5Gyr)

4 billion years ago: Sun 30% fainter!
Yet Earth wasn't frozen (liquid water evidence)

RESOLUTION:
- Higher CO₂ (1000s of ppm)
- Higher CH₄ (before O₂)
- Lower albedo (no continents?)

SNOWBALL EARTH (~720 and 640 Ma):

- Glaciation to equator
- Ice-albedo feedback ran away
- Escape: Volcanic CO₂ buildup (10,000+ ppm)
- Followed by extreme greenhouse

PHANEROZOIC (Last 540 Myr):

CO₂ CONTROL:
Long-term CO₂ set by balance:
Volcanism (source) vs Silicate weathering (sink)

CO₂ + CaSiO₃ → CaCO₃ + SiO₂ (weathering)

Higher T → faster weathering → CO₂ drawdown → cooling
NEGATIVE FEEDBACK → thermostat!

WARM PERIODS:
- Cretaceous (100 Ma): No ice, CO₂ ~1000 ppm
- PETM (56 Ma): +5°C, CO₂ pulse
- Pliocene (3-5 Ma): +2-3°C, CO₂ ~400 ppm

ICE AGES BEGIN:
- Antarctic: ~34 Ma (CO₂ dropped below ~750 ppm)
- Northern: ~2.6 Ma (closure of Panama)
"""
print(deeptime_text)

def solar_luminosity(time_ga):
    """
    Solar luminosity at time in past.

    time_ga: Time ago in billion years
    Returns: L/L_0 (fraction of current)
    """
    return 1 / (1 + 0.4 * time_ga / 4.5)

def equilibrium_temperature(luminosity_factor, albedo=0.3, greenhouse_effect_K=33):
    """
    Earth's equilibrium temperature.
    """
    S_effective = S_0 * luminosity_factor
    T_eff = ((S_effective * (1 - albedo)) / (4 * sigma))**0.25
    T_surface = T_eff + greenhouse_effect_K
    return T_surface

print("\nSolar Luminosity Through Time:")
print("-" * 60)
print(f"{'Time ago (Gyr)':<18} {'L/L_0':<12} {'T without GHE (K)':<20} {'T with 33K GHE'}")
print("-" * 60)

for t in [0, 0.5, 1, 2, 3, 4, 4.5]:
    L = solar_luminosity(t)
    T_no_ghe = equilibrium_temperature(L, greenhouse_effect_K=0)
    T_with_ghe = equilibrium_temperature(L, greenhouse_effect_K=33)
    print(f"{t:<18} {L:<12.2f} {T_no_ghe:<20.0f} {T_with_ghe:.0f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: PALEOCLIMATE PHYSICS")
print("=" * 70)

summary = """
KEY PALEOCLIMATE PHYSICS:
========================

1. MILANKOVITCH CYCLES
   - Eccentricity: 100, 400 kyr periods
   - Obliquity: 41 kyr period (seasonality)
   - Precession: 23 kyr period (season timing)
   - Summer insolation at 65°N: critical for ice sheets

2. ICE AGE CYCLES
   - 100 kyr dominant (last 800 kyr)
   - 41 kyr before that
   - Nonlinear response to orbital forcing
   - CO₂ provides amplification

3. ICE SHEET DYNAMICS
   - Glen's flow law: ε̇ = A τⁿ (n=3)
   - Response time: 10,000-100,000 years
   - Marine instabilities (MISI, MICI)
   - ELA: Where accumulation = ablation

4. CARBON CYCLE
   - CO₂: 180-280 ppm over cycles
   - Ocean solubility, circulation, biology
   - ΔF = 5.35 × ln(C₂/C₁) W/m²
   - Amplifies orbital forcing ~2-3×

5. ABRUPT CHANGES
   - Dansgaard-Oeschger: 25+ events
   - Heinrich events: iceberg armadas
   - AMOC instability: bipolar seesaw
   - Climate can change in DECADES

6. DEEP TIME
   - Faint young sun → strong greenhouse
   - Snowball Earth: ice-albedo runaway
   - Silicate weathering: long-term thermostat
   - Phanerozoic: CO₂ controls climate


THE PHYSICS TELLS US:
====================
- Small orbital forcing → large response via feedbacks
- Ice sheet inertia sets ~100 kyr timescale
- CO₂ amplifies but doesn't initiate ice ages
- Abrupt changes: AMOC is key vulnerability
- Earth's climate has been both much warmer and colder
- Current CO₂ (420 ppm) hasn't been seen in 3+ Myr
"""
print(summary)

print("\n" + "=" * 70)
print("END OF PALEOCLIMATE PHYSICS")
print("=" * 70)
