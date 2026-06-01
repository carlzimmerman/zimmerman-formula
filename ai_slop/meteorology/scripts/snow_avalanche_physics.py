#!/usr/bin/env python3
"""
Snow Physics and Avalanche Dynamics: First-Principles Derivations
==================================================================

Complete physics of snow formation, metamorphism, and avalanche mechanics.

Key phenomena:
- Snow crystal growth (Nakaya diagram)
- Snow metamorphism (destructive, constructive, melt-freeze)
- Snowpack mechanics (weak layers, stress)
- Avalanche release and flow dynamics

Starting from thermodynamics and mechanics.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81               # Gravitational acceleration [m/s²]
R_v = 461.5            # Gas constant for water vapor [J/kg/K]
L_s = 2.83e6           # Latent heat of sublimation [J/kg]
rho_ice = 917          # Ice density [kg/m³]
T_melt = 273.15        # Melting point [K]

print("="*70)
print("SNOW AND AVALANCHE PHYSICS: FIRST-PRINCIPLES DERIVATIONS")
print("="*70)

#############################################
# PART 1: SNOW CRYSTAL FORMATION
#############################################
print("\n" + "="*70)
print("PART 1: SNOW CRYSTAL FORMATION")
print("="*70)

print("""
ICE CRYSTAL NUCLEATION AND GROWTH:
=================================

HETEROGENEOUS NUCLEATION:
Ice crystals form on nuclei (dust, bacteria, etc.)
Critical temperature for various nuclei:
    Silver iodide: -4°C
    Kaolinite: -9°C
    Bacteria (P. syringae): -2°C

NAKAYA DIAGRAM:
Crystal habit depends on T and supersaturation:

Temperature        Saturation        Crystal Type
-0 to -4°C        Low-High          Plates → Dendrites
-4 to -10°C       Low-High          Columns → Needles
-10 to -22°C      Low-High          Plates → Sector plates
-22 to -40°C      Low-High          Columns → Sheaths

CRYSTAL GROWTH RATE:
From diffusion of vapor to crystal:

    dm/dt = 4π C D (ρ_v - ρ_sat)

Where:
    C = capacitance factor (shape dependent)
    D = diffusion coefficient (~2×10⁻⁵ m²/s)
    ρ_v = ambient vapor density
    ρ_sat = saturation vapor density

SUPERSATURATION:
    S = (e - e_sat) / e_sat

Where e = vapor pressure, e_sat = saturation over ice.

In clouds, S typically 0.01-0.1 (1-10%)
Larger S → faster growth → more complex shapes.
""")

def saturation_vapor_pressure_ice(T_K):
    """
    Saturation vapor pressure over ice.

    Uses Murphy and Koop (2005) formula.
    """
    ln_e = 9.550426 - 5723.265/T_K + 3.53068*np.log(T_K) \
           - 0.00728332*T_K
    return np.exp(ln_e)  # Pa

def saturation_vapor_pressure_water(T_K):
    """
    Saturation vapor pressure over supercooled water.
    """
    # Bolton formula
    T_C = T_K - 273.15
    return 611.2 * np.exp(17.67 * T_C / (T_C + 243.5))

def supersaturation_ice(T_K, RH_water):
    """
    Calculate supersaturation with respect to ice.

    In mixed-phase clouds, air is saturated wrt water
    but supersaturated wrt ice.
    """
    e_water = saturation_vapor_pressure_water(T_K)
    e_ice = saturation_vapor_pressure_ice(T_K)

    # If RH wrt water is given
    e_actual = (RH_water / 100) * e_water

    S_i = (e_actual - e_ice) / e_ice

    return S_i * 100  # percent

def crystal_habit(T_C):
    """
    Predict crystal habit from temperature (Nakaya diagram).
    """
    if T_C > 0:
        return "Melting/rain"
    elif T_C > -4:
        return "Thin plates, dendrites"
    elif T_C > -10:
        return "Needles, columns"
    elif T_C > -22:
        return "Sector plates, dendrites"
    elif T_C > -40:
        return "Columns, thick plates"
    else:
        return "Columns (homogeneous nucleation)"

print("\nSupersaturation with respect to ice (when RH_water = 100%):")
print("-" * 50)
temps = [0, -5, -10, -15, -20, -25, -30, -35, -40]
print(f"{'T (°C)':>8s}  {'S_ice (%)':>10s}  {'Crystal habit':>25s}")
print("-" * 50)
for T_C in temps:
    T_K = T_C + 273.15
    S = supersaturation_ice(T_K, 100)
    habit = crystal_habit(T_C)
    print(f"{T_C:>8.0f}  {S:>10.1f}  {habit:>25s}")

print("\n  Note: Maximum supersaturation near -12°C explains")
print("  why dendrites (snowflakes) are most common there!")

#############################################
# PART 2: SNOW DENSITY AND WATER EQUIVALENT
#############################################
print("\n" + "="*70)
print("PART 2: SNOW DENSITY AND WATER EQUIVALENT")
print("="*70)

print("""
SNOW DENSITY PHYSICS:
====================

Fresh snow density depends on:
1. Crystal type (dendrites pack loosely)
2. Temperature (warm snow packs denser)
3. Wind (breaks crystals, increases packing)
4. Riming (added ice mass)

TYPICAL DENSITIES:
    Wild snow (calm, cold): 30-50 kg/m³
    Average fresh snow: 50-100 kg/m³
    Wind-packed snow: 200-400 kg/m³
    Settled snow: 200-400 kg/m³
    Firn (old snow): 400-830 kg/m³
    Ice: 917 kg/m³

SNOW WATER EQUIVALENT (SWE):
    SWE = H_snow × (ρ_snow / ρ_water)

Where H_snow = snow depth.

Typical ratios (snow:water):
    10:1 typical
    15:1 cold, fluffy
    5:1 wet, warm

SETTLING RATE:
Compaction under self-weight:
    dρ/dt = ρ σ / η

Where:
    σ = overburden stress
    η = viscosity (highly temperature dependent)
""")

def snow_water_equivalent(depth_cm, density_kg_m3):
    """
    Calculate snow water equivalent.

    Returns SWE in mm.
    """
    rho_water = 1000
    return depth_cm * 10 * (density_kg_m3 / rho_water)  # mm

def snow_density_from_temp(T_C, wind_speed=0):
    """
    Estimate fresh snow density from temperature and wind.

    Empirical relationship.
    """
    # Base density (Hedstrom and Pomeroy 1998)
    if T_C < -15:
        rho = 50
    else:
        rho = 50 + 1.7 * (T_C + 15)**1.5

    # Wind effect (increases density through crystal breakage)
    rho += 25 * np.sqrt(wind_speed)

    return min(rho, 400)  # Cap at wind slab density

def settling_rate(density, depth_m, T_C):
    """
    Estimate snow settling (densification) rate.

    Returns fractional change per day.
    """
    # Overburden stress at bottom
    sigma = density * g * depth_m  # Pa

    # Viscosity (strongly temperature dependent)
    # η ≈ η₀ exp(Q/RT) - highly simplified
    T_K = T_C + 273.15
    eta_0 = 1e6  # Reference viscosity [Pa·s]
    Q_R = 6000  # Activation energy / R [K]
    eta = eta_0 * np.exp(Q_R * (1/T_K - 1/263))

    # Strain rate
    epsilon_dot = sigma / eta  # 1/s

    # Density change rate
    drho_dt = density * epsilon_dot * 86400  # kg/m³/day

    return drho_dt

print("\nSnow density estimates:")
print("-" * 55)
print(f"{'T (°C)':>8s}  {'Wind (m/s)':>12s}  {'Density (kg/m³)':>16s}")
print("-" * 55)
for T in [-20, -10, -5, 0]:
    for wind in [0, 5, 10]:
        rho = snow_density_from_temp(T, wind)
        print(f"{T:>8.0f}  {wind:>12.0f}  {rho:>16.0f}")

print("\nSnow water equivalent (SWE):")
print("-" * 40)
for depth in [10, 30, 50, 100]:
    for rho in [50, 100, 300]:
        swe = snow_water_equivalent(depth, rho)
        print(f"  {depth} cm snow at {rho} kg/m³ = {swe:.0f} mm SWE")

#############################################
# PART 3: SNOW METAMORPHISM
#############################################
print("\n" + "="*70)
print("PART 3: SNOW METAMORPHISM")
print("="*70)

print("""
SNOW CRYSTAL TRANSFORMATION IN SNOWPACK:
=======================================

1. EQUILIBRIUM METAMORPHISM (Destructive):
   - Small temperature gradient (< 10°C/m)
   - Vapor moves from convex to concave surfaces
   - Crystals become rounded
   - Increases strength (sintering)

   Rate: dr/dt = C × exp(-Q/RT) × (1/r - 1/r₀)

2. KINETIC METAMORPHISM (Constructive):
   - Large temperature gradient (> 10°C/m)
   - Vapor flux from warm to cold
   - Forms facets, depth hoar
   - DANGEROUS - creates weak layers!

   Vapor flux: J = -D (∂ρ_v/∂z)

   Strong gradient: Snow at bottom sublimates,
   recrystallizes above → faceted crystals.

3. MELT-FREEZE METAMORPHISM:
   - Wet snow cycles above/below 0°C
   - Free water refreezes → ice clusters
   - Creates strong "corn" or weak "sun crust"

CRITICAL GRADIENT:
    dT/dz > 10°C/m → Faceting begins
    dT/dz > 20°C/m → Rapid depth hoar formation

VAPOR PRESSURE GRADIENT:
    de/dz = (de/dT)(dT/dz)

Clausius-Clapeyron: de/dT = Le/(R_v T²)
""")

def vapor_pressure_gradient(dT_dz, T_K):
    """
    Calculate vapor pressure gradient from temperature gradient.

    Using Clausius-Clapeyron relation.
    """
    e = saturation_vapor_pressure_ice(T_K)

    # de/dT from Clausius-Clapeyron
    de_dT = L_s * e / (R_v * T_K**2)

    # de/dz
    de_dz = de_dT * dT_dz

    return de_dz

def vapor_flux(dT_dz, T_K, D_eff=2e-5):
    """
    Calculate mass flux of water vapor in snow.

    J = -D_eff × (∂ρ_v/∂z)
    """
    # Vapor density from ideal gas
    e = saturation_vapor_pressure_ice(T_K)
    rho_v = e / (R_v * T_K)

    # Gradient of vapor density
    de_dz = vapor_pressure_gradient(dT_dz, T_K)
    drho_dz = de_dz / (R_v * T_K)  # Simplified

    J = -D_eff * drho_dz

    return J * 1e6  # Convert to g/m²/s for readability

def metamorphism_type(dT_dz):
    """
    Classify expected metamorphism type.
    """
    if abs(dT_dz) < 5:
        return "Equilibrium (rounding)"
    elif abs(dT_dz) < 10:
        return "Mixed (slight faceting)"
    elif abs(dT_dz) < 20:
        return "Kinetic (faceting)"
    else:
        return "Extreme kinetic (depth hoar)"

print("\nMetamorphism classification by temperature gradient:")
print("-" * 60)
print(f"{'dT/dz (°C/m)':>14s}  {'Vapor flux':>14s}  {'Type':>25s}")
print("-" * 60)
T_mean = 263  # -10°C
for dT in [2, 5, 10, 15, 20, 30]:
    J = vapor_flux(dT, T_mean)
    mtype = metamorphism_type(dT)
    print(f"{dT:>14.0f}  {J:>12.2f} g/m²/s  {mtype:>25s}")

print("\n  DANGER: Depth hoar (extreme gradient) is very weak!")
print("  Forms when thin snowpack on cold ground.")

#############################################
# PART 4: SNOWPACK MECHANICS
#############################################
print("\n" + "="*70)
print("PART 4: SNOWPACK STRESS AND STABILITY")
print("="*70)

print("""
SNOWPACK STRESS ANALYSIS:
========================

SLAB-ON-SLOPE GEOMETRY:
Consider snow slab on slope of angle θ.

STRESSES:
Normal stress: σ_n = ρ g H cos²θ
Shear stress:  τ = ρ g H sinθ cosθ

STABILITY INDEX:
    S = τ_strength / τ_load

Where:
    τ_strength = shear strength of weak layer
    τ_load = shear stress from slab

RUTSCHBLOCK SCALE:
    S > 1.5: Stable
    1.0 < S < 1.5: Marginal
    S < 1.0: Unstable (release likely)

WEAK LAYER STRENGTH:
Typical shear strengths:
    New snow: 100-500 Pa
    Facets: 200-800 Pa
    Depth hoar: 100-600 Pa
    Rounded grains: 500-5000 Pa

FRACTURE PROPAGATION:
Once initiated, crack propagates if:
    Energy release rate > Fracture energy
    G > Gc

Anticrack model: Weak layer collapses,
creating propagating fracture.
""")

def slab_shear_stress(density, depth_m, slope_deg):
    """
    Calculate shear stress on weak layer.
    """
    theta = np.radians(slope_deg)
    tau = density * g * depth_m * np.sin(theta) * np.cos(theta)
    return tau  # Pa

def slab_normal_stress(density, depth_m, slope_deg):
    """
    Calculate normal stress on weak layer.
    """
    theta = np.radians(slope_deg)
    sigma_n = density * g * depth_m * np.cos(theta)**2
    return sigma_n  # Pa

def stability_index(tau_strength, density, depth_m, slope_deg):
    """
    Calculate snow stability index.

    S = strength / load
    """
    tau_load = slab_shear_stress(density, depth_m, slope_deg)
    return tau_strength / tau_load if tau_load > 0 else float('inf')

def critical_slope(tau_strength, density, depth_m):
    """
    Find slope angle where S = 1 (critical).
    """
    # τ = ρgH sinθ cosθ = τ_s
    # sinθ cosθ = τ_s / (ρgH) = (1/2)sin(2θ)
    ratio = tau_strength / (density * g * depth_m)

    if ratio > 0.5:
        return 90  # Stable on any slope
    if ratio < 0:
        return 0  # Always unstable

    theta_crit = 0.5 * np.arcsin(2 * ratio)
    return np.degrees(theta_crit)

print("\nSlab avalanche mechanics:")
print("-" * 65)
rho_slab = 250  # kg/m³
print(f"Slab density: {rho_slab} kg/m³\n")

print(f"{'Depth (m)':>10s}  {'Slope (°)':>10s}  {'τ (Pa)':>10s}  {'S (τ_s=500 Pa)':>15s}")
print("-" * 65)
for H in [0.5, 1.0, 1.5]:
    for slope in [25, 30, 35, 38, 40]:
        tau = slab_shear_stress(rho_slab, H, slope)
        S = stability_index(500, rho_slab, H, slope)
        status = "Stable" if S > 1.5 else "Marginal" if S > 1.0 else "UNSTABLE"
        print(f"{H:>10.1f}  {slope:>10.0f}  {tau:>10.0f}  {S:>10.2f} ({status})")

print("\nCritical slope angles for different weak layer strengths:")
for tau_s in [200, 400, 600, 800, 1000]:
    theta_c = critical_slope(tau_s, 250, 1.0)
    print(f"  τ_strength = {tau_s} Pa: Critical slope = {theta_c:.0f}°")

#############################################
# PART 5: AVALANCHE DYNAMICS
#############################################
print("\n" + "="*70)
print("PART 5: AVALANCHE FLOW DYNAMICS")
print("="*70)

print("""
AVALANCHE MOTION PHYSICS:
========================

Once released, avalanche accelerates downslope.

EQUATION OF MOTION:
    M dv/dt = M g sinθ - F_friction - F_drag

FRICTION MODELS:

1. VOELLMY MODEL (most common):
    F = μ M g cosθ + (ρ g v²) / ξ

Where:
    μ = dry friction coefficient (~0.15-0.4)
    ξ = turbulence coefficient (~1000-2000 m/s²)

TERMINAL VELOCITY:
    v_t = √[ξ H (sinθ - μ cosθ)]

Typical values: 20-80 m/s for large avalanches.

RUNOUT DISTANCE:
α-β model: Runout angle correlates with track angle.
    α = 0.95 β - 1.9° (typical)

PRESSURE (destructive force):
    p = ρ v² × C_d

For dense flow (ρ ~ 300 kg/m³, v = 40 m/s):
    p = 300 × 1600 × 0.5 ≈ 240 kPa

DAMAGE THRESHOLDS:
    1 kPa: Break windows
    5 kPa: Push cars, damage wood buildings
    30 kPa: Destroy wood structures
    100 kPa: Destroy concrete structures
""")

def voellmy_terminal_velocity(H_m, slope_deg, mu=0.25, xi=1500):
    """
    Calculate terminal velocity using Voellmy model.

    v_t = √[ξ H (sinθ - μ cosθ)]
    """
    theta = np.radians(slope_deg)
    driving = np.sin(theta) - mu * np.cos(theta)

    if driving <= 0:
        return 0  # Avalanche stops

    return np.sqrt(xi * H_m * driving)

def avalanche_pressure(density, velocity, Cd=0.5):
    """
    Calculate impact pressure.

    p = ρ v² C_d
    """
    return density * velocity**2 * Cd

def runout_angle_alpha(beta_deg):
    """
    Estimate runout angle from track angle (α-β model).

    Based on statistical analysis of avalanche paths.
    """
    return 0.95 * beta_deg - 1.9

def avalanche_mass(release_area_m2, depth_m, density):
    """
    Calculate avalanche mass from release zone.
    """
    volume = release_area_m2 * depth_m
    return volume * density

print("\nAvalanche terminal velocity (Voellmy model):")
print("-" * 55)
print(f"{'Depth (m)':>10s}  {'Slope (°)':>10s}  {'v_t (m/s)':>12s}  {'v_t (km/h)':>12s}")
print("-" * 55)
for H in [1, 2, 3]:
    for slope in [25, 30, 35, 40, 45]:
        v = voellmy_terminal_velocity(H, slope)
        print(f"{H:>10.0f}  {slope:>10.0f}  {v:>12.1f}  {v*3.6:>12.0f}")

print("\nAvalanche impact pressure and damage:")
print("-" * 50)
print(f"{'v (m/s)':>10s}  {'p (kPa)':>12s}  {'Damage level':>25s}")
print("-" * 50)
rho_flow = 300  # Dense flow
for v in [5, 10, 20, 30, 40, 50]:
    p = avalanche_pressure(rho_flow, v) / 1000  # kPa
    if p < 1:
        damage = "Minor (windows)"
    elif p < 5:
        damage = "Light structures"
    elif p < 30:
        damage = "Wood buildings"
    elif p < 100:
        damage = "Reinforced structures"
    else:
        damage = "Total destruction"
    print(f"{v:>10.0f}  {p:>12.1f}  {damage:>25s}")

#############################################
# PART 6: AVALANCHE TERRAIN ANALYSIS
#############################################
print("\n" + "="*70)
print("PART 6: AVALANCHE TERRAIN FACTORS")
print("="*70)

print("""
TERRAIN FACTORS IN AVALANCHE HAZARD:
===================================

SLOPE ANGLE:
- <25°: Rarely avalanche
- 25-30°: Possible with deep weak layer
- 30-45°: PRIME AVALANCHE TERRAIN
- 35-38°: Highest frequency
- >45°: Sluffs frequently, less buildup

ASPECT:
- North-facing: Cold, preserves weak layers
- South-facing: Sun crust, wet avalanches
- Leeward: Wind loading, slabs

TERRAIN FEATURES:
- Convex rolls: Stress concentration
- Gullies: Channelize flow
- Cliff bands: Starting zones
- Trees: Anchoring (dense) or trigger (sparse)

AVALANCHE PROBLEM TYPES:
1. Dry loose: Point release, small
2. Wet loose: Point release, wet snow
3. Wind slab: Cohesive, reactive
4. Storm slab: During/after storms
5. Persistent slab: On buried weak layer
6. Deep slab: Very deep weak layer
7. Glide: Full depth on smooth ground
8. Cornice: Overhanging snow formations

SPATIAL DISTRIBUTION:
Return periods vary with terrain:
    Very frequent: Annual
    Frequent: 1-10 years
    Infrequent: 10-100 years
    Rare: >100 years
""")

def slope_hazard_rating(slope_deg):
    """
    Simple slope-based hazard classification.
    """
    if slope_deg < 25:
        return 1, "Very low"
    elif slope_deg < 30:
        return 2, "Low"
    elif slope_deg < 35:
        return 3, "Moderate"
    elif slope_deg < 40:
        return 4, "High"
    elif slope_deg < 45:
        return 5, "Very high"
    else:
        return 4, "High (frequent sluffing)"

def aspect_factor(aspect_deg, season="winter"):
    """
    Aspect contribution to hazard.

    aspect: 0=N, 90=E, 180=S, 270=W
    """
    # North-facing holds weak layers longer
    # South-facing gets wet slides in spring

    if season == "winter":
        # Cold aspects more problematic
        north_component = np.cos(np.radians(aspect_deg))
        return 1 + 0.3 * north_component  # Higher for north
    else:
        # Warm aspects problematic in spring
        south_component = -np.cos(np.radians(aspect_deg))
        return 1 + 0.3 * south_component

print("\nSlope angle hazard rating:")
print("-" * 45)
for slope in range(20, 55, 5):
    rating, desc = slope_hazard_rating(slope)
    bar = "█" * rating
    print(f"  {slope:2d}°: {bar:5s} ({rating}/5) {desc}")

print("\nAspect factor (winter - cold weak layers):")
aspects = [(0, "N"), (45, "NE"), (90, "E"), (135, "SE"),
           (180, "S"), (225, "SW"), (270, "W"), (315, "NW")]
for asp, name in aspects:
    factor = aspect_factor(asp, "winter")
    print(f"  {name:3s} ({asp:3d}°): Factor = {factor:.2f}")

#############################################
# PART 7: AVALANCHE FORECASTING PARAMETERS
#############################################
print("\n" + "="*70)
print("PART 7: FORECASTING AND WARNING SYSTEMS")
print("="*70)

print("""
KEY FORECASTING PARAMETERS:
==========================

1. NEW SNOW AMOUNT AND RATE:
   >2 cm/hr: Rapid loading, elevated hazard
   >30 cm storm total: Significant
   >60 cm: Extreme

2. SNOW WATER EQUIVALENT RATE:
   >25 mm/24hr: Critical loading

3. WIND:
   Loading rate = k × U³ (fetch dependent)
   >15 m/s: Significant transport
   >25 m/s: Extreme loading

4. TEMPERATURE:
   Rapid warming → wet instability
   Prolonged cold → preserved weak layers
   Rain on snow: Immediate danger

5. SOLAR RADIATION:
   Affects surface warming, wet loose

AVALANCHE DANGER SCALE:
1 - Low: Natural unlikely, human triggered unlikely
2 - Moderate: Natural unlikely, human possible
3 - Considerable: Natural possible, human likely
4 - High: Natural likely, human very likely
5 - Extreme: Widespread natural activity certain

STATISTICAL RELATIONSHIPS:
P(natural) = f(new snow, wind, temperature trend)
P(human) = f(weak layer, slab properties, trigger)
""")

def loading_rate_snow(precipitation_rate_mm_hr, density=100):
    """
    Calculate mass loading rate from snowfall.

    Returns Pa/hour (stress increase).
    """
    # Convert to depth at given density
    depth_rate = precipitation_rate_mm_hr / (density/1000)  # mm/hr of snow

    # Mass rate
    mass_rate = precipitation_rate_mm_hr / 1000 * 1000  # kg/m²/hr

    # Stress rate (assuming 35° slope)
    stress_rate = mass_rate * g * np.cos(np.radians(35))**2

    return stress_rate  # Pa/hr

def wind_loading_rate(wind_speed, fetch_km=1):
    """
    Estimate wind loading rate.

    Simplified model: transport ∝ U³ above threshold.
    """
    U_t = 5  # Threshold wind [m/s]

    if wind_speed < U_t:
        return 0

    # Very simplified: kg/m²/hr
    k = 0.001 * fetch_km
    transport = k * (wind_speed - U_t)**3

    return transport

def danger_level_estimate(new_snow_cm, wind_avg, temp_trend):
    """
    Very simplified danger level estimate.

    For illustration only - real forecasting is complex!
    """
    score = 0

    # New snow contribution
    if new_snow_cm > 60:
        score += 3
    elif new_snow_cm > 30:
        score += 2
    elif new_snow_cm > 15:
        score += 1

    # Wind contribution
    if wind_avg > 25:
        score += 2
    elif wind_avg > 15:
        score += 1

    # Temperature trend
    if temp_trend == "rapid_warming":
        score += 2
    elif temp_trend == "warming":
        score += 1

    # Map to danger level
    if score >= 5:
        return 5, "EXTREME"
    elif score >= 4:
        return 4, "HIGH"
    elif score >= 2:
        return 3, "CONSIDERABLE"
    elif score >= 1:
        return 2, "MODERATE"
    else:
        return 1, "LOW"

print("\nLoading rates:")
print("-" * 45)
for precip in [1, 2, 5, 10]:  # mm/hr water equivalent
    stress = loading_rate_snow(precip)
    print(f"  Precip {precip} mm/hr: Stress rate = {stress:.1f} Pa/hr")

print("\nWind transport (at ridge):")
for wind in [10, 15, 20, 25, 30]:
    transport = wind_loading_rate(wind)
    print(f"  Wind {wind} m/s: Transport = {transport:.2f} kg/m²/hr")

print("\nDanger level examples:")
scenarios = [
    (5, 5, "stable"),
    (20, 10, "stable"),
    (35, 20, "stable"),
    (45, 25, "warming"),
    (70, 30, "rapid_warming")
]
for snow, wind, temp in scenarios:
    level, name = danger_level_estimate(snow, wind, temp)
    print(f"  Snow={snow}cm, Wind={wind}m/s, {temp}: Level {level} ({name})")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("SNOW AND AVALANCHE PHYSICS SUMMARY")
print("="*70)
print("""
Key Principles and Results:

1. SNOW CRYSTAL FORMATION:
   - Habit depends on T and supersaturation
   - Max supersaturation at -12°C → dendrites
   - Nakaya diagram predicts crystal type

2. SNOW DENSITY:
   - Fresh: 50-150 kg/m³
   - Wind-packed: 200-400 kg/m³
   - SWE = depth × (ρ_snow/ρ_water)

3. METAMORPHISM:
   - dT/dz < 10°C/m: Rounding (strengthening)
   - dT/dz > 10°C/m: Faceting (weakening)
   - dT/dz > 20°C/m: Depth hoar (DANGER!)

4. SNOWPACK STABILITY:
   - S = τ_strength / τ_load
   - S < 1: Unstable
   - Critical slopes: 30-45°

5. AVALANCHE DYNAMICS (Voellmy):
   - v_t = √[ξ H (sinθ - μ cosθ)]
   - Speeds: 20-80 m/s
   - Pressures: 10-500 kPa

6. TERRAIN FACTORS:
   - Prime angles: 30-45°
   - North aspects: Cold, weak layers
   - Convex terrain: Stress concentration

7. FORECASTING:
   - 5-level danger scale
   - Key: New snow, wind, temperature trend
   - Human triggering most common

Stay safe - get avalanche training!
""")

if __name__ == "__main__":
    print("\n[Snow and Avalanche Physics Module - First Principles Complete]")
