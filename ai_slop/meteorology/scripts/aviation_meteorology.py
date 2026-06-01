#!/usr/bin/env python3
"""
AVIATION METEOROLOGY - FIRST PRINCIPLES
========================================

Deriving the physics of aviation weather hazards:
turbulence, icing, visibility, winds, and contrails.
"""

import numpy as np

print("=" * 70)
print("AVIATION METEOROLOGY - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
R_d = 287.0        # Gas constant dry air (J/kg/K)
c_p = 1004         # Specific heat (J/kg/K)
L_v = 2.5e6        # Latent heat vaporization (J/kg)
L_s = 2.83e6       # Latent heat sublimation (J/kg)


# =============================================================================
# PART 1: AIRCRAFT ICING
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: AIRCRAFT ICING PHYSICS")
print("=" * 70)

icing_text = """
AIRCRAFT ICING:
===============

Ice accumulation on aircraft surfaces - DEADLY hazard!

ICING CONDITIONS:

1. Temperature: 0°C to -20°C (most severe)
2. Visible moisture (clouds, precip)
3. Supercooled water droplets

TYPES OF ICING:

1. RIME ICE
   - Small droplets freeze instantly on impact
   - Milky, rough, opaque
   - Temperature: < -10°C
   - Easier to remove

2. CLEAR (GLAZE) ICE
   - Large droplets spread before freezing
   - Smooth, transparent, dense
   - Temperature: 0°C to -10°C
   - Most dangerous! Hard to see, hard to remove

3. MIXED ICE
   - Combination of rime and clear
   - Temperature: -10°C to -15°C

SUPERCOOLED LARGE DROPLETS (SLD):

Freezing drizzle / freezing rain
Droplets > 50 μm
Extremely hazardous:
- Ice beyond protected surfaces
- Rapid accumulation
- Can occur outside normal icing envelope

ICING INTENSITY:

Trace: < 0.5 cm/hr accumulation
Light: 0.5-2.5 cm/hr
Moderate: 2.5-7.5 cm/hr
Severe: > 7.5 cm/hr

ACCUMULATION PHYSICS:

Ice accretion rate:
dm/dt = β × LWC × V × A

Where:
- β = collection efficiency
- LWC = liquid water content (g/m³)
- V = airspeed
- A = collection area
"""
print(icing_text)

def collection_efficiency(droplet_diameter_um, chord_m, velocity_ms):
    """
    Estimate droplet collection efficiency.

    β depends on droplet inertia vs airflow deflection.
    """
    # Stokes number determines if droplet follows airflow
    rho_water = 1000  # kg/m³
    mu_air = 1.8e-5   # Pa·s

    D = droplet_diameter_um * 1e-6
    St = rho_water * D**2 * velocity_ms / (18 * mu_air * chord_m)

    # Collection efficiency ~ St / (St + 0.25)
    beta = St / (St + 0.25)
    return min(beta, 1.0)

def icing_rate(LWC_gm3, velocity_ms, collection_eff):
    """
    Ice accumulation rate (mm/hr).

    Rate = β × LWC × V
    """
    # Convert to mm/hr (simplified)
    rate = collection_eff * LWC_gm3 * velocity_ms * 3.6  # mm/hr
    return rate

def icing_intensity_category(rate_mm_hr):
    """Categorize icing intensity."""
    if rate_mm_hr < 5:
        return "Trace"
    elif rate_mm_hr < 25:
        return "Light"
    elif rate_mm_hr < 75:
        return "Moderate"
    else:
        return "Severe"

print("\nIcing Rate vs Conditions:")
print("-" * 70)
print(f"{'LWC (g/m³)':<12} {'Droplet (μm)':<15} {'TAS (m/s)':<12} {'Rate (mm/hr)':<15} {'Intensity'}")
print("-" * 70)

for lwc in [0.2, 0.5, 1.0]:
    for drop in [15, 30, 50]:
        beta = collection_efficiency(drop, 0.3, 100)
        rate = icing_rate(lwc, 100, beta)
        intensity = icing_intensity_category(rate)
        if drop == 30:
            print(f"{lwc:<12} {drop:<15} {100:<12} {rate:<15.1f} {intensity}")


# =============================================================================
# PART 2: AVIATION TURBULENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: AVIATION TURBULENCE")
print("=" * 70)

turb_text = """
TURBULENCE FOR AVIATION:
========================

CATEGORIES:

Light: Slight, erratic changes in attitude/altitude
       Occupants feel strain against belts
       Food service possible

Moderate: Changes in attitude/altitude, but in control
          Occupants feel definite strain
          Unsecured objects dislodged

Severe: Large, abrupt changes in attitude/altitude
        May briefly lose control
        Occupants forced violently against belts

Extreme: Aircraft practically impossible to control
         May cause structural damage

TURBULENCE SOURCES:

1. CONVECTIVE
   - In/near thunderstorms
   - Severe to extreme possible
   - Avoid by 20 nm laterally

2. MECHANICAL
   - Surface obstacles
   - Low-level, gusty winds
   - Worst: strong wind + rough terrain

3. CLEAR-AIR (CAT)
   - Jet stream regions
   - Near tropopause
   - Often unexpected

4. MOUNTAIN WAVE
   - Lee of mountains
   - Can extend far downstream
   - Rotors especially hazardous

5. WAKE TURBULENCE
   - Behind large aircraft
   - Wingtip vortices
   - Spacing standards required

RIDE QUALITY METRICS:

Derived Equivalent Vertical Gust (DEVG):
U_de = derived gust velocity for observed acceleration

DEVG Category   g-load range
─────────────────────────────
Light           0.2-0.5 g
Moderate        0.5-1.0 g
Severe          1.0-2.0 g
Extreme         > 2.0 g
"""
print(turb_text)

def gust_load_factor(gust_velocity, airspeed, wing_loading, slope=5.3):
    """
    Calculate gust load factor.

    Δn = ρ × V × U_g × slope / (2 × wing_loading)
    """
    rho = 0.5  # Approximate density at altitude (kg/m³)
    delta_n = rho * airspeed * gust_velocity * slope / (2 * wing_loading)
    return delta_n

def turbulence_category_from_g(g_load):
    """Categorize turbulence from g-load."""
    if g_load < 0.2:
        return "None"
    elif g_load < 0.5:
        return "Light"
    elif g_load < 1.0:
        return "Moderate"
    elif g_load < 2.0:
        return "Severe"
    else:
        return "Extreme"

print("\nGust Load Factor (typical transport aircraft):")
print("-" * 60)
print(f"{'Gust (m/s)':<15} {'Airspeed (m/s)':<18} {'Load factor (g)':<18} {'Category'}")
print("-" * 60)

wing_loading = 500  # kg/m², typical for transport

for gust in [3, 5, 10, 15, 20, 25]:
    for V in [150, 250]:
        n = gust_load_factor(gust, V, wing_loading)
        cat = turbulence_category_from_g(n)
        if V == 200:
            n = gust_load_factor(gust, 200, wing_loading)
            cat = turbulence_category_from_g(n)
            print(f"{gust:<15} {200:<18} {n:<18.2f} {cat}")


# =============================================================================
# PART 3: VISIBILITY AND FOG
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: VISIBILITY PHYSICS")
print("=" * 70)

visibility_text = """
VISIBILITY FOR AVIATION:
========================

VISUAL RANGE:

V = 3.9 / β_ext

Where β_ext = extinction coefficient (km⁻¹)

VISIBILITY CATEGORIES:

VFR: Visibility ≥ 5 km (3 sm), ceiling ≥ 1000 ft
MVFR: 3-5 km vis, 1000-3000 ft ceiling
IFR: 1-3 km vis, 500-1000 ft ceiling
LIFR: < 1 km vis, < 500 ft ceiling

FOG TYPES:

1. RADIATION FOG
   - Clear nights, light wind
   - Ground cools by radiation
   - Air cools to dewpoint
   - Burns off after sunrise

2. ADVECTION FOG
   - Warm moist air over cold surface
   - Coastal, over cool water
   - Can persist for days
   - Dense and extensive

3. UPSLOPE FOG
   - Air forced up terrain
   - Adiabatic cooling
   - Common in mountain areas

4. FRONTAL FOG
   - Warm rain into cold air
   - Evaporation raises dewpoint
   - Pre-frontal, post-frontal

FOG FORMATION CONDITION:

T - T_d < 2-3°C with cooling/moistening continuing

DISSIPATION:

Radiation fog: Solar heating of surface
Advection fog: Wind shift, source change
"""
print(visibility_text)

def visibility_from_lwc(lwc_gm3, droplet_radius_um=5):
    """
    Estimate visibility in fog.

    V ≈ 1.5 / (LWC × droplet_radius)  (km, very approximate)
    """
    if lwc_gm3 == 0:
        return float('inf')
    vis = 0.6 / (lwc_gm3 * droplet_radius_um / 10)
    return vis

def dewpoint_depression_forecast(T_current, Td_current, cooling_rate_C_hr, hours):
    """
    Forecast dewpoint depression.

    Assuming T drops but Td stays constant.
    """
    T_future = T_current - cooling_rate_C_hr * hours
    return T_future - Td_current

def fog_probability(dewpoint_depression, wind_ms, cloud_cover_oktas):
    """
    Simple fog probability estimate.

    Based on dew point depression, wind, and cloud cover.
    """
    prob = 0

    # Dewpoint depression
    if dewpoint_depression < 1:
        prob += 0.5
    elif dewpoint_depression < 2:
        prob += 0.3
    elif dewpoint_depression < 3:
        prob += 0.1

    # Wind (light winds favor fog)
    if wind_ms < 2:
        prob += 0.2
    elif wind_ms < 5:
        prob += 0.1
    elif wind_ms > 10:
        prob -= 0.2

    # Cloud cover (clear skies favor radiation fog)
    if cloud_cover_oktas < 2:
        prob += 0.2

    return min(max(prob, 0), 1.0)

print("\nVisibility in Fog:")
print("-" * 50)
print(f"{'LWC (g/m³)':<15} {'Visibility (m)':<20} {'Category'}")
print("-" * 50)

for lwc in [0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
    vis = visibility_from_lwc(lwc) * 1000  # meters
    if vis < 1000:
        cat = "LIFR (Dense fog)"
    elif vis < 3000:
        cat = "IFR (Fog)"
    elif vis < 5000:
        cat = "MVFR (Mist)"
    else:
        cat = "VFR"
    print(f"{lwc:<15} {vis:<20.0f} {cat}")


# =============================================================================
# PART 4: CONTRAILS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: CONTRAIL PHYSICS")
print("=" * 70)

contrail_text = """
CONTRAIL FORMATION:
===================

Condensation trails from aircraft exhaust

PHYSICS (Schmidt-Appleman Criterion):

Exhaust + ambient air → mixing line
If mixing line crosses saturation curve → contrail forms

MIXING LINE:

dq/dT = (EI_H2O × c_p) / (Q × (1 - η))

Where:
- EI_H2O = water emission index (~1.25 kg/kg fuel)
- Q = heat of combustion (~43 MJ/kg)
- η = propulsive efficiency (~0.35)
- c_p = specific heat of air

CRITICAL TEMPERATURE:

T_crit depends on ambient humidity
Higher humidity → contrails at warmer T

Approximate:
T_crit ≈ -40°C at RH_ice = 0%
T_crit ≈ -36°C at RH_ice = 100%

CONTRAIL TYPES:

1. SHORT-LIVED
   - Subsaturated environment
   - Evaporate within minutes
   - Ice crystals sublime

2. PERSISTENT
   - Ice-supersaturated environment
   - Can last hours
   - Spread to cirrus-like clouds

3. CONTRAIL-INDUCED CIRRUS
   - Persistent contrails spread
   - Natural cirrus characteristics
   - Climate impact!

CLIMATE EFFECT:

Contrails:
- SW: Reflect solar (cooling)
- LW: Trap outgoing (warming)
- Net: WARMING effect (~2× CO₂ from aviation?)

Uncertain but potentially significant!
"""
print(contrail_text)

def schmidt_appleman_threshold(pressure_hPa, RH_percent=0):
    """
    Estimate threshold temperature for contrail formation.

    Simplified Schmidt-Appleman criterion.
    """
    # Approximate relationship
    # Lower T_crit at higher altitude (lower pressure)
    # Higher T_crit at higher humidity

    T_base = -38  # °C at 300 hPa, dry
    P_ref = 300

    # Pressure correction
    T_crit = T_base - 0.02 * (P_ref - pressure_hPa)

    # Humidity correction
    T_crit += 0.04 * RH_percent

    return T_crit

def contrail_persistence(T_ambient, RH_ice):
    """
    Determine if contrail will persist.

    Persists if RH_ice > 100% (ice supersaturated)
    """
    if RH_ice > 100:
        return "Persistent"
    elif RH_ice > 80:
        return "Short-lived"
    else:
        return "None/Immediate evap"

print("\nContrail Threshold Temperature:")
print("-" * 55)
print(f"{'Pressure (hPa)':<18} {'RH_ice (%)':<15} {'T_threshold (°C)'}")
print("-" * 55)

for P in [400, 300, 250, 200]:
    for RH in [0, 50, 100]:
        T_crit = schmidt_appleman_threshold(P, RH)
        print(f"{P:<18} {RH:<15} {T_crit:.0f}")


# =============================================================================
# PART 5: WIND SHEAR
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: LOW-LEVEL WIND SHEAR")
print("=" * 70)

windshear_text = """
LOW-LEVEL WIND SHEAR (LLWS):
============================

Rapid change in wind speed/direction over short distance
Critical for takeoff/landing!

SOURCES:

1. THUNDERSTORM OUTFLOWS (Microbursts)
   - Downdraft hits surface, spreads
   - Intense shear at gust front
   - Performance-decreasing shear on approach

2. FRONTAL PASSAGES
   - Wind shift across front
   - Most hazardous: fast-moving cold fronts

3. LOW-LEVEL JET
   - Nocturnal acceleration
   - Strong shear at jet boundary

4. SEA BREEZE FRONTS
   - Convergence zone
   - Rapid wind direction change

MICROBURST PHYSICS:

Intense localized downdraft
Diameter: < 4 km
Duration: 5-15 minutes
Peak winds: 40-80 knots differential

AIRCRAFT ENCOUNTER:

Headwind → Tailwind transition:
1. Enter headwind: Airspeed increases, climb
2. Downdraft: Sink, airspeed decreases
3. Exit to tailwind: Airspeed plummets, rapid sink

LOSS: Equivalent to 50-80 knots airspeed!

DETECTION:

- Terminal Doppler Weather Radar (TDWR)
- Low-Level Wind Shear Alert System (LLWAS)
- Onboard radar
- Pilot reports (PIREPs)
"""
print(windshear_text)

def f_factor(headwind_change_kt, vertical_wind_kt, groundspeed_kt, g_accel=9.81):
    """
    Calculate F-factor for wind shear hazard.

    F = (dV_h/dt)/g - w/V

    F > 0.1 is hazardous
    """
    # Simplified: F ~ ΔV_headwind / V
    # Negative means performance decreasing
    dV_ms = headwind_change_kt * 0.514
    V_ms = groundspeed_kt * 0.514
    w_ms = vertical_wind_kt * 0.514

    F = -dV_ms / (V_ms * 10) - w_ms / V_ms
    return F

def microburst_intensity(peak_differential_kt):
    """Categorize microburst intensity."""
    if peak_differential_kt < 30:
        return "Weak"
    elif peak_differential_kt < 50:
        return "Moderate"
    elif peak_differential_kt < 80:
        return "Strong"
    else:
        return "Intense"

print("\nMicroburst Wind Shear Hazard:")
print("-" * 60)
print(f"{'Headwind loss (kt)':<20} {'Downdraft (kt)':<18} {'Hazard level'}")
print("-" * 60)

for dV in [15, 30, 45, 60]:
    for w in [5, 15, 25]:
        F = f_factor(dV, w, 140)
        hazard = "Low" if abs(F) < 0.1 else "Moderate" if abs(F) < 0.15 else "Severe"
        if w == 15:
            print(f"{dV:<20} {w:<18} {hazard}")


# =============================================================================
# PART 6: DENSITY ALTITUDE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: DENSITY ALTITUDE AND PERFORMANCE")
print("=" * 70)

density_text = """
DENSITY ALTITUDE:
=================

Pressure altitude corrected for non-standard temperature
What the airplane "feels" like

CALCULATION:

DA = PA + 120 × (T_actual - T_std)

Where:
- PA = pressure altitude (ft)
- T_std = standard temperature at PA
- T_std = 15 - 2 × (PA/1000) °C

Or from density:
ρ/ρ₀ = (1 - 0.0065h/T₀)^(g/Rd×0.0065 - 1)

PERFORMANCE IMPACTS:

High density altitude = thin air:
- Reduced lift (slower takeoff)
- Reduced thrust (engines)
- Reduced propeller efficiency
- Longer takeoff/landing rolls
- Reduced climb rate

CRITICAL LOCATIONS:

- Mountain airports (field elevation)
- Hot climates
- Summer afternoons

EXAMPLE:

Denver (5430 ft) on hot day (35°C):
T_std at 5430 ft = 15 - 2×5.43 = 4°C
DA = 5430 + 120 × (35 - 4) = 9150 ft!

Performance equivalent to 9150 ft airport!

TAKEOFF DISTANCE:

Approximately:
Distance ∝ 1/ρ ∝ DA

10% increase in DA → 10% longer takeoff roll
"""
print(density_text)

def standard_temperature(pressure_alt_ft):
    """Standard atmosphere temperature at pressure altitude."""
    return 15 - 2 * pressure_alt_ft / 1000

def density_altitude(pressure_alt_ft, temperature_C):
    """
    Calculate density altitude.

    DA = PA + 120 × (T - T_std)
    """
    T_std = standard_temperature(pressure_alt_ft)
    DA = pressure_alt_ft + 120 * (temperature_C - T_std)
    return DA

def takeoff_distance_factor(density_alt_ft, sea_level_distance):
    """
    Estimate takeoff distance at density altitude.

    Approximately proportional to 1/ρ
    """
    # ρ decreases ~3% per 1000 ft
    factor = 1 + 0.03 * density_alt_ft / 1000
    return sea_level_distance * factor

print("\nDensity Altitude Examples:")
print("-" * 70)
print(f"{'Airport':<15} {'Elev (ft)':<12} {'Temp (°C)':<12} {'DA (ft)':<12} {'Performance'}")
print("-" * 70)

airports = [
    ("Sea level", 0, 15),
    ("Sea level", 0, 35),
    ("Denver", 5430, 15),
    ("Denver", 5430, 35),
    ("Leadville", 9927, 15),
    ("Leadville", 9927, 25),
]

for name, elev, temp in airports:
    DA = density_altitude(elev, temp)
    perf = "Standard" if DA < 3000 else "Reduced" if DA < 6000 else "Significantly reduced" if DA < 9000 else "Critical"
    print(f"{name:<15} {elev:<12} {temp:<12} {DA:<12.0f} {perf}")


# =============================================================================
# PART 7: VOLCANIC ASH
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: VOLCANIC ASH HAZARD")
print("=" * 70)

ash_text = """
VOLCANIC ASH:
=============

Silicate particles from volcanic eruptions
EXTREMELY hazardous to aviation!

HAZARDS:

1. ENGINE DAMAGE
   - Ash melts in combustion chamber (~1100°C)
   - Re-solidifies on turbine blades
   - Can cause flameout!
   - Sandblasting of compressor

2. ABRASION
   - Windscreen scratching (reduced visibility)
   - Leading edge erosion
   - Pitot tube blockage

3. CONTAMINATION
   - Air data systems
   - Avionics cooling

AIRCRAFT ENCOUNTERS:

Multiple engine flameout incidents:
- BA Flight 9 (1982): All 4 engines
- KLM Flight 867 (1989): All 4 engines

Both recovered engines after descending to clear air

ASH CLOUD PROPERTIES:

- Can extend 100s of km from volcano
- Persist for days at cruise altitudes
- Often invisible (especially at night)
- Not detectable by weather radar!

AVOIDANCE:

- SIGMETs for volcanic ash
- Volcanic Ash Advisory Centers (VAACs)
- Dispersion modeling
- Satellite detection

TOLERANCE:

NO safe level established!
Recommendation: Complete avoidance
"""
print(ash_text)

print("\nVolcanic Ash Advisory Centers (VAACs):")
print("-" * 55)

vaacs = [
    ("Anchorage", "Alaska, NE Russia"),
    ("Buenos Aires", "South America"),
    ("Darwin", "Australia, Indonesia"),
    ("London", "NE Atlantic, Europe"),
    ("Montreal", "N America, Greenland"),
    ("Tokyo", "NW Pacific, Japan"),
    ("Toulouse", "Europe, Africa"),
    ("Washington", "N America, Pacific"),
    ("Wellington", "SW Pacific"),
]

print(f"{'VAAC':<18} {'Area of responsibility'}")
print("-" * 55)
for vaac, area in vaacs:
    print(f"{vaac:<18} {area}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: AVIATION METEOROLOGY")
print("=" * 70)

summary = """
KEY AVIATION METEOROLOGY:
========================

1. ICING
   - Temperature: 0 to -20°C
   - Clear ice most dangerous (0 to -10°C)
   - Rate = β × LWC × V
   - SLD extremely hazardous

2. TURBULENCE
   - Categories: Light to Extreme
   - Sources: Convective, CAT, mountain wave
   - Load factor from gust response
   - EDR as intensity metric

3. VISIBILITY/FOG
   - VFR/MVFR/IFR/LIFR categories
   - Radiation fog: clear, calm nights
   - Advection fog: warm air over cold surface
   - Dewpoint depression key predictor

4. CONTRAILS
   - Schmidt-Appleman criterion
   - Form below ~-40°C
   - Persist if ice-supersaturated
   - Climate impact (net warming)

5. WIND SHEAR
   - Microbursts most dangerous
   - F-factor > 0.1 hazardous
   - Performance-decreasing on approach
   - TDWR detection

6. DENSITY ALTITUDE
   - DA = PA + 120(T - T_std)
   - High DA = reduced performance
   - Critical at mountain airports

7. VOLCANIC ASH
   - Can cause engine flameout
   - Not radar-detectable
   - Complete avoidance required


THE PHYSICS TELLS US:
====================
- Icing rate depends on LWC, droplet size, airspeed
- CAT from shear instability (Ri < 0.25)
- Contrails require specific T/humidity combination
- Microbursts create deadly shear pattern
- Density altitude critical for performance
- Volcanic ash = no safe exposure level
"""
print(summary)

print("\n" + "=" * 70)
print("END OF AVIATION METEOROLOGY")
print("=" * 70)
