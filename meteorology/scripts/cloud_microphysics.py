#!/usr/bin/env python3
"""
CLOUD MICROPHYSICS - FIRST PRINCIPLES
======================================

Deriving cloud formation, droplet growth, and precipitation
processes from thermodynamics and particle physics.
"""

import numpy as np

print("=" * 70)
print("CLOUD MICROPHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
R_v = 461.5         # Gas constant water vapor (J/kg/K)
R_d = 287.0         # Gas constant dry air (J/kg/K)
L_v = 2.5e6         # Latent heat of vaporization (J/kg)
L_s = 2.83e6        # Latent heat of sublimation (J/kg)
L_f = 3.34e5        # Latent heat of fusion (J/kg)
c_p = 1004          # Specific heat of air (J/kg/K)
g = 9.81            # Gravity (m/s²)
sigma_w = 0.073     # Surface tension of water (N/m at 20°C)
rho_w = 1000        # Water density (kg/m³)
rho_i = 917         # Ice density (kg/m³)


# =============================================================================
# PART 1: SATURATION AND CLOUD FORMATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: SATURATION AND CLOUD FORMATION")
print("=" * 70)

saturation_text = """
WHEN DO CLOUDS FORM?
====================

Clouds form when air becomes SUPERSATURATED:
Relative humidity > 100%

HOW TO ACHIEVE SUPERSATURATION:

1. COOLING (most common)
   - Adiabatic lifting (rising air expands, cools)
   - Radiative cooling (fog)
   - Contact with cold surface

2. ADDING MOISTURE (less common)
   - Evaporation from warm water into cold air
   - Mixing of air masses

LIFTING CONDENSATION LEVEL (LCL):
Height where rising air reaches saturation.

LCL ≈ 125 × (T - T_d) meters

Where T = temperature, T_d = dew point (both in °C)

Example: T = 25°C, T_d = 15°C
LCL ≈ 125 × 10 = 1250 m (cloud base)

LAPSE RATES:
- Dry adiabatic: Γ_d = g/c_p = 9.8 °C/km
- Moist adiabatic: Γ_m ≈ 5-7 °C/km (latent heat release)
"""
print(saturation_text)

def saturation_vapor_pressure(T_celsius):
    """
    Calculate saturation vapor pressure over liquid water.
    Using Bolton (1980) formula.
    """
    e_s = 6.112 * np.exp(17.67 * T_celsius / (T_celsius + 243.5))
    return e_s  # hPa

def saturation_vapor_pressure_ice(T_celsius):
    """
    Calculate saturation vapor pressure over ice.
    """
    T_K = T_celsius + 273.15
    e_i = 6.112 * np.exp(22.46 * T_celsius / (T_celsius + 272.62))
    return e_i  # hPa

def lcl_height(T_celsius, Td_celsius):
    """Calculate Lifting Condensation Level height."""
    return 125 * (T_celsius - Td_celsius)

print("\nSaturation Vapor Pressure:")
print("-" * 60)
print(f"{'T (°C)':<10} {'e_s (hPa)':<15} {'e_ice (hPa)':<15} {'Difference (%)'}")
print("-" * 60)

for T in [-40, -30, -20, -10, 0, 10, 20, 30, 40]:
    e_s = saturation_vapor_pressure(T)
    e_i = saturation_vapor_pressure_ice(T) if T <= 0 else e_s
    diff = (e_s - e_i) / e_s * 100 if T <= 0 else 0
    print(f"{T:<10} {e_s:<15.2f} {e_i:<15.2f} {diff:<15.1f}")

print("\n\nLCL Height Examples:")
print("-" * 50)
for T, Td in [(30, 25), (30, 20), (30, 15), (25, 10), (20, 5)]:
    lcl = lcl_height(T, Td)
    print(f"T = {T}°C, Td = {Td}°C → LCL = {lcl:.0f} m")


# =============================================================================
# PART 2: CLOUD CONDENSATION NUCLEI (CCN)
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: CLOUD CONDENSATION NUCLEI (CCN)")
print("=" * 70)

ccn_text = """
WHY DO WE NEED CCN?
===================

Pure water requires ~300% supersaturation to condense!
(Homogeneous nucleation - very rare in atmosphere)

CCN provide surfaces for heterogeneous nucleation:
- Only ~0.1-1% supersaturation needed
- Much easier!

KÖHLER THEORY:
Equilibrium supersaturation over a droplet:

S = exp(A/r - B/r³)

A-term (KELVIN/CURVATURE effect):
Small droplets have higher vapor pressure
A = 2σ/(ρ_w R_v T)

B-term (RAOULT/SOLUTE effect):
Dissolved solutes reduce vapor pressure
B = (3 n_s M_w)/(4π ρ_w M_s)

Competition: Curvature increases S, solute decreases S
Result: Critical radius r* and critical supersaturation S*

CCN TYPES:
- Sea salt (NaCl) - very effective, hygroscopic
- Sulfates (SO4) - from DMS, pollution
- Dust - less effective but abundant
- Organics - complex, variable

CCN CONCENTRATIONS:
- Marine: 50-300 cm⁻³
- Continental: 300-1000 cm⁻³
- Polluted: 1000-10000 cm⁻³
"""
print(ccn_text)

def critical_supersaturation(dry_radius_um, molar_mass_solute=58.44):
    """
    Calculate critical supersaturation for CCN activation.

    Simplified Köhler theory.
    dry_radius_um: dry particle radius (μm)
    molar_mass_solute: g/mol (58.44 for NaCl)
    """
    r = dry_radius_um * 1e-6  # Convert to meters
    T = 293  # K

    # A coefficient (curvature)
    A = 2 * sigma_w / (rho_w * R_v * T)

    # Approximate critical supersaturation (simplified)
    # S_c ∝ r^(-3/2) for small CCN
    S_c = 1.5 * (A / r) ** 1.5 * 100  # Convert to percent

    return min(S_c, 10)  # Cap at 10%

print("\nCritical Supersaturation for CCN Activation:")
print("-" * 60)
print(f"{'Dry radius (μm)':<20} {'S_critical (%)':<20} {'Ease of activation'}")
print("-" * 60)

for r in [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
    S_c = critical_supersaturation(r)
    if S_c < 0.2:
        ease = "Very easy (large)"
    elif S_c < 0.5:
        ease = "Easy"
    elif S_c < 1.0:
        ease = "Moderate"
    else:
        ease = "Difficult (small)"
    print(f"{r:<20.2f} {S_c:<20.2f} {ease}")


# =============================================================================
# PART 3: DROPLET GROWTH BY CONDENSATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: DROPLET GROWTH BY CONDENSATION")
print("=" * 70)

condensation_text = """
DROPLET GROWTH BY DIFFUSION:
============================

Once activated, droplets grow by vapor diffusion.

GROWTH EQUATION:
r dr/dt = (S - 1) / (F_k + F_d)

Where:
- r = droplet radius
- S = saturation ratio (RH/100)
- F_k = thermodynamic term (latent heat)
- F_d = diffusion term (vapor transport)

Solving: r² - r₀² = 2 × G × (S - 1) × t

GROWTH RATE:
- Rapid at first (small droplets)
- Slows as droplet grows (r ∝ √t)
- To grow from 1 μm to 10 μm: ~10 minutes
- To grow from 10 μm to 100 μm: ~10 hours!

THE CONDENSATION PROBLEM:
Condensation alone is TOO SLOW to make rain!
10 μm droplets don't fall (too small)
Need collision-coalescence or ice processes
"""
print(condensation_text)

def condensation_growth_time(r_initial_um, r_final_um, supersaturation_pct):
    """
    Time for droplet to grow by condensation.

    Simplified: r² - r₀² = G × S × t
    where G ≈ 10⁻¹⁰ m²/s for typical conditions
    """
    r_i = r_initial_um * 1e-6
    r_f = r_final_um * 1e-6
    S = supersaturation_pct / 100

    G = 1e-10  # Growth parameter (m²/s)

    t = (r_f**2 - r_i**2) / (G * S)
    return t / 60  # Convert to minutes

print("\nCondensation Growth Times (S = 0.5%):")
print("-" * 60)
print(f"{'From (μm)':<15} {'To (μm)':<15} {'Time (min)':<20} {'Note'}")
print("-" * 60)

growth_stages = [
    (1, 5, "Newly activated"),
    (5, 10, "Small cloud droplet"),
    (10, 20, "Typical droplet"),
    (20, 50, "Large droplet"),
    (50, 100, "Very large (drizzle)"),
]

for r_i, r_f, note in growth_stages:
    t = condensation_growth_time(r_i, r_f, 0.5)
    print(f"{r_i:<15} {r_f:<15} {t:<20.0f} {note}")


# =============================================================================
# PART 4: COLLISION-COALESCENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: COLLISION-COALESCENCE (WARM RAIN)")
print("=" * 70)

collision_text = """
COLLISION-COALESCENCE PROCESS:
==============================

How clouds make rain without ice!

TERMINAL VELOCITY:
Large drops fall faster than small drops.
v_t ∝ r² (Stokes regime, r < 40 μm)
v_t ∝ r^0.5 (larger drops)

10 μm droplet: v_t ≈ 0.01 m/s (essentially floating)
100 μm droplet: v_t ≈ 0.7 m/s
1000 μm (1 mm): v_t ≈ 6.5 m/s

COLLISION:
Large drop overtakes smaller drops
Collision efficiency E_c = f(r_large, r_small)

COALESCENCE:
Not all collisions result in merger!
Coalescence efficiency E_coal depends on:
- Surface charge
- Impact velocity
- Size ratio

COLLECTION EFFICIENCY:
E = E_c × E_coal

GROWTH EQUATION:
dr/dt = (E × w_L × Δv) / (4 ρ_w)

Where w_L = liquid water content

TIME TO RAIN:
Need ~20-30 minutes for collision-coalescence
Requires:
1. Cloud depth > 2 km (time for growth)
2. Initial "collector" drops (> 20 μm)
3. Broad droplet size distribution
"""
print(collision_text)

def terminal_velocity(radius_um):
    """
    Terminal velocity of water droplet.

    Uses empirical fit covering multiple regimes.
    """
    r = radius_um * 1e-6  # meters
    d = 2 * r  # diameter

    if d < 80e-6:
        # Stokes regime
        eta = 1.8e-5  # Dynamic viscosity of air
        v_t = (2 * rho_w * g * r**2) / (9 * eta)
    elif d < 1200e-6:
        # Intermediate regime (empirical)
        v_t = 4000 * r**0.8
    else:
        # Large drops
        v_t = 10 * np.sqrt(d * 1000)

    return v_t

print("\nTerminal Velocity of Water Drops:")
print("-" * 60)
print(f"{'Radius (μm)':<15} {'Diameter (mm)':<15} {'v_t (m/s)':<15} {'Type'}")
print("-" * 60)

for r_um in [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 3000]:
    v_t = terminal_velocity(r_um)
    d_mm = r_um * 2 / 1000
    if r_um < 20:
        drop_type = "Cloud droplet"
    elif r_um < 100:
        drop_type = "Large droplet"
    elif r_um < 250:
        drop_type = "Drizzle"
    elif r_um < 2500:
        drop_type = "Rain"
    else:
        drop_type = "Large rain"
    print(f"{r_um:<15} {d_mm:<15.2f} {v_t:<15.2f} {drop_type}")


# =============================================================================
# PART 5: ICE PROCESSES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ICE PROCESSES (COLD RAIN)")
print("=" * 70)

ice_text = """
ICE NUCLEATION AND GROWTH:
==========================

SUPERCOOLED WATER:
Pure water can remain liquid to -40°C!
Ice nucleation requires:
1. Ice nuclei (IN) - rare, special particles
2. OR homogeneous nucleation at T < -38°C

ICE NUCLEI TYPES:
- Mineral dust (most common)
- Biological (bacteria, pollen)
- Soot
- Some organics

IN CONCENTRATION:
Much rarer than CCN!
N_IN ≈ exp(-0.6 × (T + 20)) per liter (Fletcher formula)
At -20°C: ~1 IN per liter
At -30°C: ~400 IN per liter

BERGERON-FINDEISEN PROCESS:
Key to mid-latitude precipitation!

1. Mixed-phase cloud: ice + supercooled water
2. e_sat(ice) < e_sat(liquid) at T < 0°C
3. Air saturated for water is SUPERSATURATED for ice
4. Ice crystals grow rapidly at expense of droplets
5. Ice grows to precipitation size quickly

Example at -15°C:
e_liquid = 1.91 hPa
e_ice = 1.65 hPa
Supersaturation for ice = 16%!

This is why ice crystals grow so fast in mixed-phase clouds.
"""
print(ice_text)

def ice_supersaturation(T_celsius):
    """
    Calculate supersaturation with respect to ice
    when air is saturated with respect to liquid.
    """
    e_liq = saturation_vapor_pressure(T_celsius)
    e_ice = saturation_vapor_pressure_ice(T_celsius)
    if T_celsius <= 0:
        return (e_liq - e_ice) / e_ice * 100
    return 0

def ice_nuclei_concentration(T_celsius):
    """
    Fletcher formula for ice nuclei concentration.
    Returns: IN per liter
    """
    if T_celsius > -5:
        return 0
    N = np.exp(-0.6 * (T_celsius + 20))
    return N

print("\nIce Supersaturation (Bergeron Process):")
print("-" * 50)
print(f"{'T (°C)':<10} {'SS_ice (%)':<15} {'Growth driver'}")
print("-" * 50)

for T in [0, -5, -10, -15, -20, -25, -30]:
    ss = ice_supersaturation(T)
    driver = "Strong" if ss > 10 else "Moderate" if ss > 5 else "Weak"
    print(f"{T:<10} {ss:<15.1f} {driver}")

print("\n\nIce Nuclei Concentration:")
print("-" * 50)
for T in [-5, -10, -15, -20, -25, -30, -35]:
    N = ice_nuclei_concentration(T)
    print(f"T = {T}°C: {N:.1f} IN/L")


# =============================================================================
# PART 6: PRECIPITATION TYPES
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: PRECIPITATION TYPES AND PHYSICS")
print("=" * 70)

precip_text = """
PRECIPITATION TYPES:
====================

1. RAIN (warm or melted)
   - Droplets > 0.5 mm diameter
   - Terminal velocity 2-9 m/s
   - From warm clouds OR melting ice

2. DRIZZLE
   - Small droplets 0.1-0.5 mm
   - Light intensity < 1 mm/hr
   - Often from stratus clouds

3. SNOW
   - Ice crystals or aggregates
   - Falls when T < 0°C through column
   - Many crystal habits (plates, dendrites, columns)

4. SLEET (Ice Pellets)
   - Frozen raindrops
   - Warm layer aloft → cold layer below
   - Bounces on impact

5. FREEZING RAIN
   - Supercooled drops
   - Warm layer aloft, cold surface
   - Freezes on contact (ice storms!)

6. HAIL
   - Layered ice balls
   - From strong updrafts in thunderstorms
   - Can exceed 10 cm diameter!

7. GRAUPEL
   - Rimed ice crystals
   - "Snow pellets"
   - From accretion in clouds

TEMPERATURE PROFILES DETERMINE TYPE:
- All warm: Rain
- Cold aloft, warm surface: Rain (melted)
- Cold throughout: Snow
- Warm layer, cold below: Sleet or freezing rain
"""
print(precip_text)

def precip_type_from_profile(T_surface, T_max_aloft, warm_layer_depth=0):
    """
    Determine precipitation type from temperature profile.

    T_surface: surface temperature (°C)
    T_max_aloft: warmest temp in column (°C)
    warm_layer_depth: depth of warm layer (m)
    """
    if T_max_aloft > 0 and T_surface > 2:
        return "Rain"
    elif T_max_aloft < 0 and T_surface < 0:
        return "Snow"
    elif T_max_aloft > 2 and T_surface < 0:
        if warm_layer_depth > 1000:
            return "Freezing rain"
        else:
            return "Sleet"
    elif T_max_aloft > 0 and 0 < T_surface < 2:
        return "Rain/Snow mix"
    else:
        return "Snow"

print("\nPrecipitation Type from Temperature Profile:")
print("-" * 70)
print(f"{'T_surface':<12} {'T_max aloft':<15} {'Warm depth':<15} {'Precip type'}")
print("-" * 70)

profiles = [
    (10, 15, 0),
    (-5, -10, 0),
    (-2, 5, 1500),
    (-2, 5, 500),
    (1, 5, 0),
    (-3, -1, 0),
]

for T_s, T_max, depth in profiles:
    ptype = precip_type_from_profile(T_s, T_max, depth)
    print(f"{T_s:<12}°C {T_max:<15}°C {depth:<15}m {ptype}")


# =============================================================================
# PART 7: CLOUD TYPES AND CHARACTERISTICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: CLOUD CLASSIFICATION AND PROPERTIES")
print("=" * 70)

clouds_text = """
CLOUD CLASSIFICATION:
====================

BY HEIGHT:
Low (< 2 km): Stratus, Stratocumulus, Cumulus
Mid (2-6 km): Altostratus, Altocumulus
High (> 6 km): Cirrus, Cirrostratus, Cirrocumulus

BY PROCESS:
Stratiform: Layer clouds, gentle uplift
Cumuliform: Convective, vertical development
Cirriform: Ice crystals, high altitude

CLOUD MICROPHYSICS BY TYPE:

CUMULUS/CUMULONIMBUS:
- Droplet conc: 100-500 cm⁻³
- Mean radius: 5-15 μm
- LWC: 0.5-3 g/m³
- Updraft: 1-50 m/s

STRATUS/STRATOCUMULUS:
- Droplet conc: 50-400 cm⁻³
- Mean radius: 5-10 μm
- LWC: 0.1-0.5 g/m³
- Turbulent mixing

CIRRUS:
- Ice crystals only
- Number: 0.01-10 cm⁻³
- Size: 100-1000 μm
- IWC: 0.01-0.05 g/m³
"""
print(clouds_text)

print("\nTypical Cloud Properties:")
print("-" * 80)
print(f"{'Cloud type':<20} {'Base (km)':<12} {'LWC (g/m³)':<12} {'Droplets (cm⁻³)':<18} {'Precip?'}")
print("-" * 80)

cloud_types = [
    ("Fog", 0, 0.05, 100, "Drizzle"),
    ("Stratus", 0.5, 0.25, 200, "Drizzle"),
    ("Stratocumulus", 1, 0.3, 250, "Light"),
    ("Cumulus (fair)", 1.5, 0.5, 300, "No"),
    ("Cumulus (congestus)", 1.5, 1.5, 400, "Showers"),
    ("Cumulonimbus", 2, 2.5, 500, "Heavy"),
    ("Altostratus", 3, 0.3, 150, "Light/mod"),
    ("Cirrus", 8, 0.02, 0.1, "Virga"),
]

for ctype, base, lwc, drops, precip in cloud_types:
    print(f"{ctype:<20} {base:<12} {lwc:<12} {drops:<18} {precip}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: CLOUD MICROPHYSICS")
print("=" * 70)

summary = """
KEY CLOUD MICROPHYSICS:
======================

1. SATURATION
   - Clouds form at >100% RH
   - LCL ≈ 125 × (T - Td) meters
   - Clausius-Clapeyron governs e_s(T)

2. CCN ACTIVATION
   - Need particles for nucleation
   - Köhler theory: competition of curvature vs solute
   - S_c ∝ r^(-3/2) for critical supersaturation

3. CONDENSATION GROWTH
   - r² ∝ t (diffusion-limited)
   - Too slow for rain! (hours for drizzle)
   - Gets droplets to ~10-20 μm

4. COLLISION-COALESCENCE
   - Large drops collect small drops
   - v_t differential drives collisions
   - Needs collector drops + broad spectrum
   - Can produce rain in ~30 minutes

5. ICE PROCESSES (BERGERON)
   - Ice nuclei much rarer than CCN
   - e_s(ice) < e_s(liquid) at T < 0°C
   - Ice grows at expense of droplets
   - Dominant precipitation mechanism mid-latitudes

6. PRECIPITATION TYPE
   - Determined by temperature profile
   - Warm column: Rain
   - Cold column: Snow
   - Warm aloft + cold surface: Sleet/freezing rain


THE PHYSICS TELLS US:
=====================
- Pure condensation can't make rain (too slow)
- Need either collision-coalescence OR ice processes
- Warm clouds: Require broad spectrum + depth
- Cold clouds: Bergeron process is efficient
- Most mid-latitude rain starts as snow!
"""
print(summary)

print("\n" + "=" * 70)
print("END OF CLOUD MICROPHYSICS")
print("=" * 70)
