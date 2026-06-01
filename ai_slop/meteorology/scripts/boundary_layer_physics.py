#!/usr/bin/env python3
"""
ATMOSPHERIC BOUNDARY LAYER PHYSICS - FIRST PRINCIPLES
======================================================

Deriving the physics of the planetary boundary layer (PBL):
surface fluxes, turbulence, stability, and diurnal cycles.
"""

import numpy as np

print("=" * 70)
print("ATMOSPHERIC BOUNDARY LAYER PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81            # Gravity (m/s²)
k_von = 0.4         # von Kármán constant
c_p = 1004          # Specific heat of air (J/kg/K)
rho_air = 1.2       # Air density (kg/m³)
L_v = 2.5e6         # Latent heat of vaporization (J/kg)


# =============================================================================
# PART 1: WHAT IS THE BOUNDARY LAYER?
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: THE PLANETARY BOUNDARY LAYER")
print("=" * 70)

pbl_text = """
THE PLANETARY BOUNDARY LAYER (PBL):
===================================

Definition: The lowest 1-2 km of atmosphere directly influenced
by Earth's surface on timescales of ~1 hour.

CHARACTERISTICS:
- Turbulent (unlike free atmosphere above)
- Diurnal cycle (grows during day, collapses at night)
- Where we live and breathe!
- Where weather "happens" at the surface

STRUCTURE:

FREE ATMOSPHERE (above PBL)
---------------------------- Entrainment zone
MIXED LAYER (convective, well-mixed)    } Daytime
----------------------------
SURFACE LAYER (bottom 10%, logarithmic) }
============ SURFACE ===================

At night:
RESIDUAL LAYER (remnant of daytime ML)
----------------------------
STABLE BOUNDARY LAYER (very shallow, 100-300m)
============ SURFACE ===================

PBL DEPTH:
- Daytime convective: 1-3 km
- Nighttime stable: 100-500 m
- Over ocean: ~500 m (less diurnal variation)
"""
print(pbl_text)

def pbl_depth_convective(surface_heat_flux, hours_after_sunrise):
    """
    Estimate convective PBL depth.

    Simplified: h ∝ (H × t)^(1/2) for free convection

    surface_heat_flux: W/m²
    hours_after_sunrise: hours
    """
    # Encroachment model approximation
    t_seconds = hours_after_sunrise * 3600
    gamma = 0.01  # Free atmosphere lapse rate (K/m)

    # h² ≈ (2 × H × t) / (ρ × c_p × γ)
    h_squared = 2 * surface_heat_flux * t_seconds / (rho_air * c_p * gamma)
    h = np.sqrt(max(0, h_squared))

    return min(h, 3000)  # Cap at 3 km

print("\nConvective PBL Growth:")
print("-" * 60)
print(f"{'Hours after sunrise':<22} {'H = 200 W/m²':<15} {'H = 400 W/m²':<15}")
print("-" * 60)

for hours in [1, 2, 4, 6, 8, 10]:
    h_200 = pbl_depth_convective(200, hours)
    h_400 = pbl_depth_convective(400, hours)
    print(f"{hours:<22} {h_200:<15.0f}m {h_400:<15.0f}m")


# =============================================================================
# PART 2: SURFACE LAYER AND LOG WIND PROFILE
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: SURFACE LAYER - LOGARITHMIC WIND PROFILE")
print("=" * 70)

log_profile_text = """
THE LOGARITHMIC WIND PROFILE:
=============================

In the surface layer (bottom 10% of PBL), wind increases
logarithmically with height:

u(z) = (u*/k) × ln(z/z₀)

Where:
- u* = friction velocity (characteristic turbulent velocity)
- k = von Kármán constant ≈ 0.4
- z = height above surface
- z₀ = roughness length (depends on surface)

FRICTION VELOCITY:
u* = √(τ/ρ) where τ = surface stress

Typical values: u* = 0.1-0.5 m/s

ROUGHNESS LENGTH z₀:
Surface type          z₀ (m)
---------------------------------
Ice, water            0.0001-0.001
Short grass           0.01
Crops                 0.1
Suburban              0.5
Forest                1-2
City center           2-5

Wind at 10m over grass (z₀=0.01) with u*=0.3:
u(10) = (0.3/0.4) × ln(10/0.01) = 5.2 m/s
"""
print(log_profile_text)

def log_wind_profile(z, u_star, z0):
    """
    Logarithmic wind profile (neutral stability).

    z: height (m)
    u_star: friction velocity (m/s)
    z0: roughness length (m)
    """
    if z <= z0:
        return 0
    return (u_star / k_von) * np.log(z / z0)

def friction_velocity_from_wind(u_ref, z_ref, z0):
    """Calculate friction velocity from reference wind."""
    return u_ref * k_von / np.log(z_ref / z0)

print("\nWind Profile Examples:")
print("-" * 70)

# Different surfaces
surfaces = [
    ("Water", 0.0002),
    ("Grass", 0.01),
    ("Crops", 0.1),
    ("Suburban", 0.5),
    ("Forest", 1.5),
]

u_star = 0.4  # m/s

print(f"Friction velocity u* = {u_star} m/s")
print(f"\n{'Height (m)':<12}", end="")
for name, _ in surfaces:
    print(f"{name:<12}", end="")
print()
print("-" * 70)

for z in [2, 5, 10, 20, 50, 100]:
    print(f"{z:<12}", end="")
    for name, z0 in surfaces:
        if z > z0:
            u = log_wind_profile(z, u_star, z0)
            print(f"{u:<12.1f}", end="")
        else:
            print(f"{'---':<12}", end="")
    print()


# =============================================================================
# PART 3: SURFACE ENERGY BALANCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: SURFACE ENERGY BALANCE")
print("=" * 70)

seb_text = """
SURFACE ENERGY BALANCE:
=======================

At the surface, energy must balance:

R_n = H + LE + G

Where:
- R_n = Net radiation (incoming - outgoing)
- H = Sensible heat flux (heating air)
- LE = Latent heat flux (evaporation)
- G = Ground heat flux (into soil)

NET RADIATION:
R_n = (1-α)S↓ + L↓ - L↑

- S↓ = downward solar (up to ~1000 W/m²)
- α = surface albedo
- L↓ = downward longwave from atmosphere
- L↑ = upward longwave = εσT⁴

BOWEN RATIO:
β = H / LE

Surface type      β (typical)
-----------------------------
Ocean             0.1-0.2
Wet forest        0.2-0.5
Grassland         0.5-2.0
Desert            5-10
Snow/ice          Large (little evap)

This determines how warming is partitioned!
"""
print(seb_text)

def surface_energy_balance(solar_down, albedo, T_surface, T_air,
                          wind_speed, humidity_deficit):
    """
    Calculate surface energy balance components.

    Returns H, LE, G (simplified)
    """
    # Net shortwave
    SW_net = (1 - albedo) * solar_down

    # Net longwave (simplified)
    sigma = 5.67e-8
    LW_net = -sigma * T_surface**4 + 0.8 * sigma * T_air**4

    # Net radiation
    R_n = SW_net + LW_net

    # Ground heat flux (typically 10% of R_n during day)
    G = 0.1 * R_n

    # Available for turbulent fluxes
    available = R_n - G

    # Partition based on humidity (simplified Bowen ratio approach)
    # Higher humidity deficit = more evaporation possible
    bowen = 0.5 + 2.0 * (1 - humidity_deficit)  # Simplified

    H = available * bowen / (1 + bowen)
    LE = available / (1 + bowen)

    return R_n, H, LE, G

print("\nSurface Energy Balance Examples:")
print("-" * 70)
print(f"{'Scenario':<25} {'Rn':<10} {'H':<10} {'LE':<10} {'G':<10} {'Bowen':<10}")
print("-" * 70)

scenarios = [
    ("Midday sun, wet grass", 800, 0.25, 300, 290, 0.8),
    ("Midday sun, dry grass", 800, 0.25, 310, 290, 0.3),
    ("Desert", 900, 0.35, 320, 300, 0.1),
    ("Forest", 700, 0.15, 295, 290, 0.9),
    ("Ocean", 600, 0.06, 293, 290, 0.95),
]

for name, solar, albedo, T_s, T_a, humid in scenarios:
    R_n, H, LE, G = surface_energy_balance(solar, albedo, T_s, T_a, 5, humid)
    bowen = H / LE if LE > 0 else float('inf')
    print(f"{name:<25} {R_n:<10.0f} {H:<10.0f} {LE:<10.0f} {G:<10.0f} {bowen:<10.1f}")


# =============================================================================
# PART 4: ATMOSPHERIC STABILITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: ATMOSPHERIC STABILITY")
print("=" * 70)

stability_text = """
ATMOSPHERIC STABILITY:
======================

Stability determines how turbulence behaves.

POTENTIAL TEMPERATURE:
θ = T × (p₀/p)^(R/c_p)

θ is conserved for adiabatic motions.
Temperature a parcel would have if brought to surface.

STABILITY REGIMES:

1. UNSTABLE (∂θ/∂z < 0):
   - Surface heated, air rises
   - Daytime over land
   - Vigorous turbulence, good mixing

2. NEUTRAL (∂θ/∂z ≈ 0):
   - Strong winds, weak surface heating
   - Cloudy, windy days
   - Mechanical turbulence dominates

3. STABLE (∂θ/∂z > 0):
   - Surface cooler than air
   - Nighttime, over cold surfaces
   - Suppressed turbulence, poor mixing

MONIN-OBUKHOV LENGTH (L):
L = -u*³ ρ c_p T / (k g H)

L > 0: Stable
L < 0: Unstable
|L| large: Near-neutral

z/L is the stability parameter:
- z/L << -1: Very unstable (free convection)
- z/L ≈ 0: Neutral
- z/L >> 1: Very stable
"""
print(stability_text)

def obukhov_length(u_star, T, H):
    """
    Calculate Monin-Obukhov length.

    u_star: friction velocity (m/s)
    T: temperature (K)
    H: sensible heat flux (W/m², positive = upward)
    """
    if abs(H) < 1:
        return float('inf') * np.sign(H) if H != 0 else float('inf')

    L = -u_star**3 * rho_air * c_p * T / (k_von * g * H)
    return L

print("\nMonin-Obukhov Length for Different Conditions:")
print("-" * 70)
print(f"{'Condition':<30} {'u* (m/s)':<12} {'H (W/m²)':<12} {'L (m)':<15} {'Stability'}")
print("-" * 70)

conditions = [
    ("Strong convection", 0.3, 300, 290),
    ("Moderate convection", 0.4, 150, 290),
    ("Weak convection", 0.5, 50, 290),
    ("Near-neutral", 0.5, 5, 290),
    ("Weak stable", 0.3, -30, 285),
    ("Strong stable", 0.1, -50, 280),
]

for name, u_star, H, T in conditions:
    L = obukhov_length(u_star, T, H)
    if L > 1000:
        stability = "Neutral"
    elif L > 0:
        stability = "Stable"
    elif L > -100:
        stability = "Unstable"
    else:
        stability = "Very unstable"

    L_str = f"{L:.0f}" if abs(L) < 10000 else "∞"
    print(f"{name:<30} {u_star:<12.1f} {H:<12.0f} {L_str:<15} {stability}")


# =============================================================================
# PART 5: TURBULENT FLUXES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: TURBULENT FLUXES")
print("=" * 70)

flux_text = """
TURBULENT TRANSPORT:
====================

Turbulence transports heat, moisture, and momentum vertically.

REYNOLDS DECOMPOSITION:
u = ū + u'  (mean + fluctuation)
T = T̄ + T'

FLUX = correlation of fluctuations:
H = ρ c_p × ‾w'T'‾   (sensible heat)
LE = ρ L_v × ‾w'q'‾  (latent heat)
τ = -ρ × ‾u'w'‾      (momentum)

FLUX-GRADIENT RELATIONSHIPS:
H = -ρ c_p K_H × ∂T/∂z
LE = -ρ L_v K_E × ∂q/∂z
τ = ρ K_M × ∂u/∂z

Where K = eddy diffusivity (m²/s)

In surface layer:
K_M = k u* z (neutral)

Typical values in convective PBL: K ~ 10-100 m²/s
"""
print(flux_text)

def sensible_heat_flux(dT_dz, K_H, rho=1.2, cp=1004):
    """Calculate sensible heat flux from temperature gradient."""
    return -rho * cp * K_H * dT_dz

def eddy_diffusivity_neutral(u_star, z):
    """Eddy diffusivity in neutral surface layer."""
    return k_von * u_star * z

print("\nEddy Diffusivity in Surface Layer:")
print("-" * 50)
print(f"{'Height (m)':<15} {'K (m²/s) for u*=0.3':<20} {'K (m²/s) for u*=0.5'}")
print("-" * 50)

for z in [1, 2, 5, 10, 20, 50]:
    K_03 = eddy_diffusivity_neutral(0.3, z)
    K_05 = eddy_diffusivity_neutral(0.5, z)
    print(f"{z:<15} {K_03:<20.2f} {K_05:<.2f}")


# =============================================================================
# PART 6: SEA BREEZE / LAND BREEZE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: SEA BREEZE AND LAND BREEZE CIRCULATION")
print("=" * 70)

seabreeze_text = """
SEA BREEZE / LAND BREEZE:
=========================

Classic example of thermally-driven local circulation.

PHYSICS:
1. Land heats faster than ocean during day
2. Air rises over land (low pressure)
3. Air sinks over ocean (high pressure)
4. Pressure gradient drives surface wind: SEA BREEZE

At night: Reverse circulation = LAND BREEZE

SEA BREEZE CHARACTERISTICS:
- Onset: 2-4 hours after sunrise
- Peak: Early afternoon
- Speed: 5-10 m/s
- Depth: 500-1000 m
- Inland penetration: 10-50 km
- Sea breeze FRONT: Sharp boundary with temperature drop

SCALING:
Pressure difference: Δp ∝ ρ g h ΔT/T

Where h = mixed layer height

For ΔT = 5°C, h = 1 km:
Δp ≈ 1.2 × 10 × 1000 × 5/300 ≈ 200 Pa ≈ 2 mb
"""
print(seabreeze_text)

def sea_breeze_intensity(T_land, T_ocean, h_pbl=1000):
    """
    Estimate sea breeze intensity from temperature contrast.

    Returns approximate wind speed (m/s)
    """
    dT = T_land - T_ocean
    T_mean = (T_land + T_ocean) / 2

    # Pressure difference
    dp = rho_air * g * h_pbl * dT / T_mean

    # Wind from pressure gradient (simplified)
    # Balance: friction ~ pressure gradient
    # u ~ sqrt(dp / rho)
    u = np.sqrt(abs(dp) / rho_air) * np.sign(dT) * 0.5

    return abs(u)

print("\nSea Breeze Intensity:")
print("-" * 60)
print(f"{'T_land (°C)':<15} {'T_ocean (°C)':<15} {'ΔT':<10} {'Wind (m/s)':<15}")
print("-" * 60)

for T_land in [25, 30, 35]:
    T_ocean = 20
    dT = T_land - T_ocean
    u = sea_breeze_intensity(T_land + 273, T_ocean + 273)
    print(f"{T_land:<15} {T_ocean:<15} {dT:<10} {u:<15.1f}")


# =============================================================================
# PART 7: NOCTURNAL BOUNDARY LAYER
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: NOCTURNAL BOUNDARY LAYER")
print("=" * 70)

nocturnal_text = """
NOCTURNAL (STABLE) BOUNDARY LAYER:
==================================

At night, surface cools by longwave radiation:
- Surface becomes colder than air above
- Stable layer forms (inversion)
- Turbulence suppressed
- PBL collapses to 100-300 m

CONSEQUENCES:

1. TEMPERATURE INVERSION
   Temperature increases with height (opposite of normal)
   Can trap pollutants near surface

2. LOW-LEVEL JET
   Decoupling from surface friction
   Wind accelerates above stable layer
   Peak winds: 10-30 m/s at 100-500 m

3. FOG FORMATION
   Radiative cooling → saturation → fog
   Especially in valleys, near water

4. FROST
   Clear nights, calm winds
   Surface can cool below 0°C even if air is warmer

RADIATIVE COOLING RATE:
dT/dt ≈ -1 to -3 °C/hour on clear nights
"""
print(nocturnal_text)

def nocturnal_cooling_rate(cloud_cover, wind_speed):
    """
    Estimate surface cooling rate at night.

    cloud_cover: 0-1 fraction
    wind_speed: m/s

    Returns: cooling rate in °C/hour
    """
    # Clear sky cooling potential
    max_cooling = 3.0  # °C/hour

    # Cloud factor (clouds reduce cooling)
    cloud_factor = 1 - 0.8 * cloud_cover

    # Wind factor (wind mixes heat down, reduces cooling)
    wind_factor = 1 / (1 + wind_speed / 5)

    return max_cooling * cloud_factor * wind_factor

print("\nNocturnal Cooling Rates:")
print("-" * 60)
print(f"{'Clouds':<15} {'Wind (m/s)':<15} {'Cooling (°C/hr)':<20} {'8-hr drop (°C)'}")
print("-" * 60)

for cloud in [0, 0.3, 0.7, 1.0]:
    for wind in [0, 3, 10]:
        rate = nocturnal_cooling_rate(cloud, wind)
        drop_8hr = rate * 8
        cloud_str = f"{int(cloud*100)}%"
        print(f"{cloud_str:<15} {wind:<15} {rate:<20.1f} {drop_8hr:<.0f}")


# =============================================================================
# PART 8: URBAN BOUNDARY LAYER
# =============================================================================
print("\n" + "=" * 70)
print("PART 8: URBAN HEAT ISLAND")
print("=" * 70)

uhi_text = """
URBAN HEAT ISLAND (UHI):
========================

Cities are warmer than surrounding rural areas.

CAUSES:
1. Reduced vegetation → less evaporative cooling
2. Dark surfaces → low albedo → more absorption
3. Building materials → high heat capacity
4. Anthropogenic heat (vehicles, AC, industry)
5. Reduced sky view → less radiative cooling
6. Urban canyon geometry → traps radiation

MAGNITUDE:
- Average: 1-3°C warmer than rural
- Peak (calm, clear nights): 5-10°C warmer
- Strongest at night (rural cools more)

UHI INTENSITY:
ΔT_UHI = a × ln(P) + b

Where P = population
Empirical: ΔT ≈ 2-3°C per order of magnitude in population

IMPACTS:
- Increased cooling energy demand
- Heat stress during heat waves
- Altered precipitation patterns
- Extended growing season
"""
print(uhi_text)

def uhi_intensity(population, wind_speed, cloud_cover):
    """
    Estimate Urban Heat Island intensity.

    Returns temperature difference (urban - rural) in °C
    """
    # Base UHI from population
    if population > 0:
        base_uhi = 0.5 * np.log10(population)
    else:
        base_uhi = 0

    # Weather modifiers
    wind_factor = 1 / (1 + wind_speed / 5)
    cloud_factor = 1 - 0.5 * cloud_cover

    return base_uhi * wind_factor * cloud_factor

print("\nUrban Heat Island Intensity:")
print("-" * 70)
print(f"{'Population':<15} {'Wind':<10} {'Clouds':<10} {'UHI (°C)':<15} {'Note'}")
print("-" * 70)

cities = [
    (50000, "Small city"),
    (500000, "Medium city"),
    (5000000, "Large city"),
    (20000000, "Megacity"),
]

for pop, note in cities:
    for wind, cloud in [(0, 0), (5, 0.5)]:
        uhi = uhi_intensity(pop, wind, cloud)
        cond = "Calm/clear" if wind == 0 else "Windy/cloudy"
        print(f"{pop:<15,} {wind:<10} {int(cloud*100)}%{'':<6} {uhi:<15.1f} {note} ({cond})")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: BOUNDARY LAYER PHYSICS")
print("=" * 70)

summary = """
KEY BOUNDARY LAYER PHYSICS:
===========================

1. PBL STRUCTURE
   - Daytime: Deep convective, 1-3 km
   - Nighttime: Shallow stable, 100-300 m
   - Surface layer: bottom 10%, log profile

2. LOG WIND PROFILE
   u(z) = (u*/k) × ln(z/z₀)
   - u* = friction velocity
   - z₀ = roughness length
   - k = 0.4 (von Kármán)

3. SURFACE ENERGY BALANCE
   R_n = H + LE + G
   - Bowen ratio β = H/LE
   - Determines partitioning

4. STABILITY
   - Unstable: ∂θ/∂z < 0 (day)
   - Stable: ∂θ/∂z > 0 (night)
   - Monin-Obukhov L characterizes regime

5. TURBULENT FLUXES
   - H = ρ c_p w'T'
   - K-theory: flux ∝ gradient
   - Eddy diffusivity K ~ k u* z

6. SEA BREEZE
   - From land-sea temperature contrast
   - ~5-10 m/s, 10-50 km penetration
   - Reverses at night

7. NOCTURNAL BL
   - Radiative cooling: 1-3°C/hr
   - Inversion forms
   - Low-level jet develops

8. URBAN HEAT ISLAND
   - Cities 1-10°C warmer
   - Strongest: calm, clear nights
   - UHI ∝ log(population)

THE PBL IS WHERE:
- We live
- Weather is felt
- Air quality matters
- Forecasts are verified
"""
print(summary)

print("\n" + "=" * 70)
print("END OF BOUNDARY LAYER PHYSICS")
print("=" * 70)
