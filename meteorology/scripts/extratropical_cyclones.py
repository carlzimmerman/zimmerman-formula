#!/usr/bin/env python3
"""
EXTRATROPICAL CYCLONE PHYSICS - FIRST PRINCIPLES
================================================

Deriving the physics of mid-latitude storms (nor'easters, etc.)
from baroclinic instability theory.
"""

import numpy as np

print("=" * 70)
print("EXTRATROPICAL CYCLONE PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
omega = 7.29e-5     # Earth rotation rate (rad/s)
R_earth = 6.371e6   # Earth radius (m)
g = 9.81            # Gravity (m/s²)
c_p = 1004          # Specific heat (J/kg/K)


# =============================================================================
# PART 1: BAROCLINIC INSTABILITY - STORM GENESIS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: BAROCLINIC INSTABILITY - HOW STORMS FORM")
print("=" * 70)

baroclinic_text = """
BAROCLINIC INSTABILITY:
=======================

The fundamental mechanism for mid-latitude storm formation.

BAROCLINIC means: Density surfaces don't align with pressure surfaces
→ There's a horizontal temperature gradient
→ Available Potential Energy exists in this gradient
→ Storms convert this to Kinetic Energy

THE PHYSICAL PICTURE:
1. Warm air over tropics, cold air over poles
2. Thermal wind → jet stream exists
3. Small perturbation in jet stream
4. Cold air sinks equatorward, warm air rises poleward
5. This RELEASES potential energy
6. Storm intensifies through feedback

EADY MODEL (1949):
Simplest model capturing baroclinic instability.

Growth rate: σ = 0.31 × f × (dU/dz) / N

Where:
- f = Coriolis parameter (2Ω sin φ)
- dU/dz = vertical wind shear (thermal wind!)
- N = Brunt-Väisälä frequency (stratification)

This gives typical growth rate of ~1/day
→ Storm doubles in intensity each day!
"""
print(baroclinic_text)

def coriolis_parameter(latitude):
    """Calculate Coriolis parameter f = 2Ω sin(φ)."""
    return 2 * omega * np.sin(np.radians(latitude))

def beta_parameter(latitude):
    """Calculate beta = df/dy at given latitude."""
    return 2 * omega * np.cos(np.radians(latitude)) / R_earth

def brunt_vaisala(dT_dz, T_mean=250):
    """
    Calculate Brunt-Väisälä frequency from lapse rate.

    N² = (g/T) × (dT/dz + g/c_p)

    dT_dz: actual lapse rate (K/m, negative for cooling with height)
    T_mean: mean temperature (K)
    """
    gamma_d = g / c_p  # Dry adiabatic lapse rate
    N_squared = (g / T_mean) * (-dT_dz + gamma_d)
    return np.sqrt(max(0, N_squared))

def eady_growth_rate(latitude, shear, N=0.01):
    """
    Calculate Eady baroclinic growth rate.

    σ = 0.31 × f × shear / N

    shear: vertical wind shear dU/dz (s⁻¹)
    N: Brunt-Väisälä frequency (s⁻¹)
    """
    f = coriolis_parameter(latitude)
    sigma = 0.31 * abs(f) * shear / N
    return sigma

def eady_wavelength(latitude, H=10000, N=0.01):
    """
    Calculate most unstable wavelength for Eady problem.

    λ ≈ 4 × NH / f

    H: tropopause height (m)
    N: Brunt-Väisälä frequency (s⁻¹)
    """
    f = coriolis_parameter(latitude)
    lambda_m = 4 * N * H / abs(f)
    return lambda_m

print("\nBrunt-Väisälä Frequency (Atmospheric Stability):")
print("-" * 60)
print(f"{'Lapse rate (K/km)':<20} {'N (s⁻¹)':<15} {'Period (min)':<15}")
print("-" * 60)

for lapse_rate in [5, 6.5, 8, 9.8]:  # K/km
    dT_dz = -lapse_rate / 1000  # Convert to K/m
    N = brunt_vaisala(dT_dz)
    period = 2 * np.pi / N / 60 if N > 0 else float('inf')
    stability = "stable" if lapse_rate < 9.8 else "neutral"
    print(f"{lapse_rate:<20.1f} {N:<15.4f} {period:<15.1f} ({stability})")


print("\n\nEady Growth Rate and Most Unstable Wavelength:")
print("-" * 70)
print(f"{'Lat':<8} {'Shear (m/s/km)':<18} {'Growth rate':<15} {'e-fold (days)':<15} {'λ (km)':<10}")
print("-" * 70)

for lat in [30, 45, 60]:
    for shear_per_km in [3, 5, 7]:  # m/s per km
        shear = shear_per_km / 1000  # Convert to s⁻¹
        N = 0.01  # Typical value
        sigma = eady_growth_rate(lat, shear, N)
        e_fold = 1 / sigma / 86400 if sigma > 0 else float('inf')
        wavelength = eady_wavelength(lat, H=10000, N=N) / 1000  # km
        print(f"{lat:<8}° {shear_per_km:<18.0f} {sigma:<15.2e} {e_fold:<15.1f} {wavelength:<10.0f}")


# =============================================================================
# PART 2: ROSSBY DEFORMATION RADIUS
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: ROSSBY DEFORMATION RADIUS - THE NATURAL SCALE")
print("=" * 70)

rossby_text = """
ROSSBY RADIUS OF DEFORMATION:
============================

This is the natural horizontal scale for geostrophic adjustment.

L_R = NH / f

Where:
- N = Brunt-Väisälä frequency (~0.01 s⁻¹)
- H = scale height or tropopause (~10 km)
- f = Coriolis parameter

For Earth's mid-latitudes: L_R ≈ 1000 km

PHYSICAL MEANING:
- Scales smaller than L_R: Gravity dominates
- Scales larger than L_R: Rotation dominates

IMPLICATIONS:
1. Synoptic scale storms are ~1000 km (Rossby radius)
2. This is why all mid-latitude cyclones are similar size!
3. Fronts occur where scale becomes smaller than L_R
"""
print(rossby_text)

def rossby_radius(latitude, N=0.01, H=10000):
    """Calculate Rossby deformation radius."""
    f = coriolis_parameter(latitude)
    L_R = N * H / abs(f)
    return L_R

print("\nRossby Deformation Radius by Latitude:")
print("-" * 50)
print(f"{'Latitude':<15} {'f (s⁻¹)':<15} {'L_R (km)':<15}")
print("-" * 50)

for lat in [20, 30, 40, 45, 50, 60, 70]:
    f = coriolis_parameter(lat)
    L_R = rossby_radius(lat)
    print(f"{lat:<15}° {f:<15.2e} {L_R/1000:<15.0f}")


# =============================================================================
# PART 3: CYCLONE STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: EXTRATROPICAL CYCLONE STRUCTURE")
print("=" * 70)

structure_text = """
EXTRATROPICAL CYCLONE ANATOMY:
==============================

Unlike tropical cyclones (symmetric, warm core):
- Extratropical cyclones are ASYMMETRIC
- They have a COLD CORE at upper levels
- Fronts are the key feature

FRONTAL ZONES:
1. COLD FRONT
   - Cold, dense air undercuts warm air
   - Steep slope (~1:50 to 1:100)
   - Sharp temperature drop
   - Heavy convective precipitation

2. WARM FRONT
   - Warm air overrides cold air
   - Gentle slope (~1:150 to 1:300)
   - Gradual temperature rise
   - Steady stratiform precipitation

3. OCCLUDED FRONT
   - Cold front catches warm front
   - Warm air lifted entirely off surface
   - Storm reaches mature stage


NORWEGIAN CYCLONE MODEL (1919):
Life cycle stages:
1. Initial perturbation on polar front
2. Open wave stage (young cyclone)
3. Mature stage (pronounced warm sector)
4. Occluded stage (wrapping up)
5. Dissipation

Total lifecycle: ~3-7 days
"""
print(structure_text)


# Frontal slopes
def frontal_slope(dT_dx, f, T_mean=280, g=9.81):
    """
    Calculate frontal slope from temperature gradient.

    Margules formula: tan(α) = f × ΔT / (g × (dT/dx))

    Actually uses thermal wind balance at the front.
    """
    # Simplified: slope ≈ f × T_mean / (g × dT_dx)
    slope = abs(f) * T_mean / (g * abs(dT_dx))
    return slope

print("\nFrontal Slopes (thermal wind balance):")
print("-" * 70)
print(f"{'Front type':<15} {'dT/dx (K/100km)':<18} {'Slope':<15} {'Rise per 100km':<15}")
print("-" * 70)

f_45 = coriolis_parameter(45)
for front_type, dT_per_100km in [("Weak", 3), ("Moderate", 5), ("Strong cold", 10), ("Intense", 15)]:
    dT_dx = dT_per_100km / 100000  # K/m
    slope = frontal_slope(dT_dx, f_45)
    rise = 100 / slope  # km rise per 100 km horizontal
    print(f"{front_type:<15} {dT_per_100km:<18.0f} 1:{1/slope:<13.0f} {rise:<15.1f} km")


# =============================================================================
# PART 4: CYCLONE ENERGETICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: CYCLONE ENERGETICS")
print("=" * 70)

energetics_text = """
ENERGY CYCLE IN EXTRATROPICAL CYCLONES:
=======================================

LORENZ ENERGY CYCLE:
1. MEAN AVAILABLE POTENTIAL ENERGY (MAPE)
   - From equator-to-pole temperature gradient
   - Maintained by differential solar heating

2. EDDY AVAILABLE POTENTIAL ENERGY (EAPE)
   - Extracted from MAPE by baroclinic instability
   - Stored in wave disturbances

3. EDDY KINETIC ENERGY (EKE)
   - Converted from EAPE by vertical motions
   - Warm air rising, cold air sinking
   - This is the storm's winds!

4. MEAN KINETIC ENERGY (MKE)
   - Cascade back to mean flow
   - Maintains jet stream

CONVERSION RATES:
MAPE → EAPE: ~2 W/m² (extraction by instability)
EAPE → EKE:  ~1 W/m² (storm intensification)

A single extratropical cyclone:
- Converts ~10¹⁸ J of potential energy
- Over ~3-5 day lifecycle
- Power: ~10¹² W (trillion watts!)
"""
print(energetics_text)

def available_potential_energy(dT, H=10000, area=1e12):
    """
    Estimate available potential energy from temperature contrast.

    APE ≈ (1/2) × g × H² × (dρ/ρ)² × Area

    Simplified using thermal expansion: dρ/ρ ≈ dT/T
    """
    T_mean = 250  # K
    rho = 0.5  # kg/m³ average

    # APE per unit volume
    ape_density = 0.5 * rho * (g * H * dT / T_mean)**2 / g

    # Total APE
    ape_total = ape_density * area * H

    return ape_total

print("\nEnergy Available for Storm Development:")
print("-" * 60)
print(f"{'ΔT (°C)':<15} {'APE (J)':<20} {'Equivalent hurricanes':<25}")
print("-" * 60)

hurricane_energy = 6e14  # Rough energy of Cat-3 hurricane

for dT in [5, 10, 15, 20]:
    ape = available_potential_energy(dT)
    n_hurricanes = ape / hurricane_energy
    print(f"{dT:<15.0f} {ape:<20.2e} {n_hurricanes:<25.0f}")


# =============================================================================
# PART 5: STORM TRACKS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: STORM TRACKS AND STEERING")
print("=" * 70)

tracks_text = """
WHERE DO EXTRATROPICAL STORMS GO?
=================================

STEERING FLOW:
Storms are steered by the mean flow at ~500 hPa level.

V_storm ≈ 0.7 × V_500hPa

Typical 500 hPa wind in jet: 30-50 m/s
→ Storm motion: ~20-35 m/s (~40-70 mph)

STORM TRACK LOCATIONS:
1. North Atlantic (Iceland-UK-Scandinavia)
2. North Pacific (Aleutians-Alaska)
3. Southern Ocean (50-60°S, circumpolar)

WHY THESE LOCATIONS?
- Maximum baroclinicity (temperature gradient)
- Jet stream exits from continents
- Warm ocean currents provide moisture

CLIMATE CHANGE EFFECTS:
- Poleward shift of storm tracks (~1° per 2°C warming)
- Possible weakening of temperature gradient
- Uncertain: Could mean fewer but more intense storms
"""
print(tracks_text)

def storm_motion(U_500, V_500, factor=0.7):
    """Estimate storm motion from 500 hPa wind."""
    U_storm = factor * U_500
    V_storm = factor * V_500
    speed = np.sqrt(U_storm**2 + V_storm**2)
    return U_storm, V_storm, speed

print("\nStorm Motion from Steering Flow:")
print("-" * 60)
print(f"{'V_500 (m/s)':<15} {'Storm speed (m/s)':<20} {'km/day':<15}")
print("-" * 60)

for V_500 in [20, 30, 40, 50, 60]:
    _, _, speed = storm_motion(V_500, 0)
    km_per_day = speed * 86.4
    print(f"{V_500:<15.0f} {speed:<20.1f} {km_per_day:<15.0f}")


# =============================================================================
# PART 6: CYCLOGENESIS AND BOMB CYCLONES
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: EXPLOSIVE CYCLOGENESIS (BOMB CYCLONES)")
print("=" * 70)

bomb_text = """
BOMB CYCLONE = EXPLOSIVE DEEPENING
==================================

Definition: Pressure drops ≥24 hPa in 24 hours
(Adjusted for latitude: ≥24 × sin(60°)/sin(φ) hPa)

PHYSICAL REQUIREMENTS:
1. Strong baroclinicity (temperature gradient)
2. Upper-level divergence (jet streak)
3. Low-level warm advection
4. Moisture (latent heat release)

QUASI-GEOSTROPHIC OMEGA EQUATION:
The vertical motion field is diagnosed from:

∇²ω ∝ -∂/∂p(v·∇ζ_g) - (R/p)∇²(v·∇T)

Terms:
1. Vorticity advection by thermal wind
2. Laplacian of temperature advection

Positive (upward) omega from:
- Increasing vorticity advection with height
- Warm advection (especially with curvature)

FAMOUS BOMB CYCLONES:
- 1978 President's Day Storm (East Coast US)
- 2019 March Bomb Cyclone (Central US)
- Regular winter storms over North Atlantic
"""
print(bomb_text)

def pressure_drop_required(latitude, hours=24):
    """
    Calculate bomb cyclone pressure drop threshold.

    Standard: 24 hPa in 24 hours at 60°N
    Adjusted: 24 × sin(60°)/sin(φ)
    """
    sin_60 = np.sin(np.radians(60))
    sin_lat = np.sin(np.radians(latitude))
    threshold = 24 * sin_60 / sin_lat * (hours / 24)
    return threshold

print("\nBomb Cyclone Threshold by Latitude:")
print("-" * 50)
print(f"{'Latitude':<15} {'Threshold (hPa/24hr)':<25}")
print("-" * 50)

for lat in [30, 35, 40, 45, 50, 55, 60]:
    threshold = pressure_drop_required(lat)
    print(f"{lat:<15}° {threshold:<25.1f}")


# =============================================================================
# PART 7: CLIMATE CHANGE AND EXTRATROPICAL STORMS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: CLIMATE CHANGE EFFECTS")
print("=" * 70)

climate_text = """
CLIMATE CHANGE AND MID-LATITUDE STORMS:
=======================================

COMPETING EFFECTS:

1. ARCTIC AMPLIFICATION
   - Arctic warms faster than tropics
   - Reduces equator-pole temperature gradient
   - → Weaker baroclinicity → fewer storms?

2. INCREASED MOISTURE
   - Warmer air holds more water (C-C)
   - More latent heat release
   - → Stronger individual storms?

3. JET STREAM CHANGES
   - Thermal wind weakens with reduced gradient
   - BUT upper tropics warm faster than surface
   - → Complex changes in jet structure

NET RESULT (Current understanding):
- Storm tracks shift poleward (~1°/2°C warming)
- Total number may decrease slightly
- Intense storms become MORE frequent
- More extreme precipitation in storms (C-C)

OBSERVATIONS (1979-present):
- Storm track intensity shows no clear trend yet
- Regional shifts are detected
- Natural variability large

This remains an active research area!
"""
print(climate_text)

# Storm intensity with moisture
def storm_intensity_scaling(dT, cc_factor=7):
    """
    Estimate storm intensity change from moisture increase.

    More moisture → more latent heat → stronger storms
    But also weaker temperature gradient...

    Simplified: intensity scales with (precip)^0.5 roughly
    """
    moisture_factor = (1 + cc_factor/100) ** dT
    intensity_factor = moisture_factor ** 0.5
    return intensity_factor

print("\nPotential Storm Intensity Change with Warming:")
print("-" * 60)
print(f"{'Warming (°C)':<15} {'Moisture ×':<15} {'Intensity ×':<15}")
print("-" * 60)

for dT in [1, 2, 3, 4]:
    moisture = (1 + 7/100) ** dT
    intensity = storm_intensity_scaling(dT)
    print(f"{dT:<15.0f} {moisture:<15.2f} {intensity:<15.2f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: EXTRATROPICAL CYCLONE PHYSICS")
print("=" * 70)

summary = """
KEY PHYSICS OF EXTRATROPICAL STORMS:
====================================

1. BAROCLINIC INSTABILITY
   - Temperature gradient → available potential energy
   - Small perturbations grow exponentially
   - Growth rate σ ≈ 0.31 × f × (dU/dz) / N
   - Typical e-folding time: 1-2 days

2. ROSSBY DEFORMATION RADIUS
   - L_R = NH/f ≈ 1000 km at mid-latitudes
   - This sets the natural storm scale
   - Why all mid-latitude cyclones are similar size

3. FRONTAL STRUCTURE
   - Asymmetric, cold-core storms
   - Cold front, warm front, occlusion
   - Frontal slopes from thermal wind balance

4. ENERGETICS
   - Convert potential energy to kinetic
   - ~10¹² W power during intensification
   - Important for global heat transport

5. STORM TRACKS
   - Steered by 500 hPa flow
   - Located where baroclinicity maximum
   - Shift poleward with warming

6. BOMB CYCLONES
   - ≥24 hPa/24hr deepening (at 60°N)
   - Require strong baroclinicity + moisture
   - Upper-level forcing crucial

7. CLIMATE CHANGE
   - Competing effects: less gradient vs more moisture
   - Likely: fewer total, but more intense
   - Poleward shift of storm tracks


THE PHYSICS TELLS US:
=====================
Mid-latitude weather is fundamentally driven by:
- Earth's rotation (Coriolis, f)
- Temperature gradient (equator to pole)
- Atmospheric stratification (N)

These combine to determine:
- Storm size (~1000 km)
- Storm intensity (baroclinic growth rate)
- Storm tracks (maximum gradient regions)

This is first-principles meteorology!
"""
print(summary)

print("\n" + "=" * 70)
print("END OF EXTRATROPICAL CYCLONE PHYSICS")
print("=" * 70)
