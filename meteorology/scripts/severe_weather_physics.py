#!/usr/bin/env python3
"""
SEVERE WEATHER PHYSICS - FIRST PRINCIPLES
==========================================

Deriving the physics of thunderstorms, supercells, and tornadoes
from thermodynamics and fluid dynamics.
"""

import numpy as np

print("=" * 70)
print("SEVERE WEATHER PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81            # Gravity (m/s²)
R_d = 287.0         # Gas constant dry air (J/kg/K)
R_v = 461.5         # Gas constant water vapor (J/kg/K)
c_p = 1004          # Specific heat at constant pressure (J/kg/K)
c_v = 717           # Specific heat at constant volume (J/kg/K)
L_v = 2.5e6         # Latent heat of vaporization (J/kg)
p_0 = 100000        # Reference pressure (Pa)
T_0 = 273.15        # 0°C in Kelvin


# =============================================================================
# PART 1: ATMOSPHERIC STABILITY AND CAPE
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: CONVECTIVE AVAILABLE POTENTIAL ENERGY (CAPE)")
print("=" * 70)

cape_text = """
CAPE: THE FUEL FOR THUNDERSTORMS
================================

CAPE measures the potential energy available for convection.

CAPE = ∫(LFC to EL) g × (T_parcel - T_env) / T_env × dz

Where:
- LFC = Level of Free Convection
- EL = Equilibrium Level
- T_parcel = Temperature of rising air parcel
- T_env = Environmental temperature

Physically: How much warmer is the rising parcel than its environment?
Warmer parcel → buoyant → accelerates upward → thunderstorm!

CAPE VALUES AND STORM TYPES:
< 300 J/kg:   Marginal (weak storms possible)
300-1000:     Weak to moderate thunderstorms
1000-2500:    Strong thunderstorms likely
2500-4000:    Severe thunderstorms likely
> 4000:       Extreme (violent tornadoes possible)

MAXIMUM UPDRAFT VELOCITY:
From energy conservation: w_max = √(2 × CAPE)

CAPE 1000 J/kg → w_max = 45 m/s (100 mph)
CAPE 4000 J/kg → w_max = 89 m/s (200 mph)!
"""
print(cape_text)

def compute_cape_simple(T_surface, T_dewpoint, lapse_rate_env=6.5,
                        tropopause_height=12000):
    """
    Simplified CAPE calculation.

    Assumes:
    - Parcel rises moist adiabatically above LCL
    - Environmental lapse rate is constant
    """
    # Lifting Condensation Level (approximate)
    lcl_height = 125 * (T_surface - T_dewpoint)  # meters

    # Temperature at LCL
    T_lcl = T_surface - (g / c_p) * lcl_height

    # Moist adiabatic lapse rate (simplified)
    gamma_m = 6.0  # K/km (varies with temperature)

    # Environmental lapse rate
    gamma_e = lapse_rate_env  # K/km

    # If moist adiabat is less than environmental, parcel is warmer
    if gamma_m < gamma_e:
        # Positive buoyancy above LCL
        delta_gamma = (gamma_e - gamma_m) / 1000  # K/m

        # Approximate CAPE as triangular area
        # Height of positive buoyancy
        z_top = min(tropopause_height, lcl_height + 8000)
        dz = z_top - lcl_height

        # Average temperature excess
        avg_T_excess = delta_gamma * dz / 2

        # CAPE ≈ g × ∫(dT/T) dz ≈ g × (avg_dT/T_mean) × dz
        T_mean = T_lcl - gamma_m * dz / 2000
        cape = g * avg_T_excess / T_mean * dz

        return max(0, cape), lcl_height
    else:
        return 0, lcl_height

def max_updraft(cape):
    """Maximum updraft velocity from CAPE."""
    return np.sqrt(2 * cape)

print("\nCAPE Estimates for Different Conditions:")
print("-" * 70)
print(f"{'Surface T (°C)':<15} {'Dewpoint (°C)':<15} {'CAPE (J/kg)':<15} {'Max Updraft (m/s)'}")
print("-" * 70)

conditions = [
    (25, 15),   # Moderate instability
    (30, 20),   # Strong instability
    (35, 24),   # Extreme instability
    (32, 22),   # High plains
    (28, 26),   # Gulf coast (very moist)
]

for T_sfc, T_dp in conditions:
    cape, lcl = compute_cape_simple(T_sfc, T_dp)
    w_max = max_updraft(cape)
    print(f"{T_sfc:<15.0f} {T_dp:<15.0f} {cape:<15.0f} {w_max:<17.1f}")


# =============================================================================
# PART 2: WIND SHEAR AND STORM ORGANIZATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: WIND SHEAR AND SUPERCELL PHYSICS")
print("=" * 70)

shear_text = """
WIND SHEAR: THE ORGANIZER OF SEVERE STORMS
==========================================

Wind shear = change in wind with height.

Bulk Shear (0-6 km):
ΔV = √[(u_6km - u_sfc)² + (v_6km - v_sfc)²]

WHY SHEAR MATTERS:
1. Tilts the updraft → separates updraft from downdraft
2. Prevents storm from "raining itself out"
3. Creates rotation (vorticity) in the storm

SHEAR VALUES AND STORM TYPES:
< 20 kt:    Ordinary cells (disorganized, short-lived)
20-35 kt:   Multicells (organized, longer-lived)
35-50 kt:   Supercells possible
> 50 kt:    Supercells likely, tornadoes possible

STORM RELATIVE HELICITY (SRH):
Measures corkscrew-like rotation in the inflow layer.

SRH = ∫(0 to h) (V - C) × (∂V/∂z) × k̂ dz

Where C = storm motion vector

SRH > 150 m²/s² → Rotating storms (mesocyclone)
SRH > 300 m²/s² → Significant tornado potential
SRH > 500 m²/s² → Violent tornado potential
"""
print(shear_text)

def bulk_shear(u_sfc, v_sfc, u_6km, v_6km):
    """Calculate 0-6 km bulk wind shear."""
    du = u_6km - u_sfc
    dv = v_6km - v_sfc
    return np.sqrt(du**2 + dv**2)

def storm_relative_helicity(shear_magnitude, mean_wind_dir_change=90):
    """
    Simplified SRH estimate.

    Actual SRH requires full wind profile, this is approximate.
    """
    # SRH scales with shear and directional change
    # Simplified: SRH ∝ shear² × sin(direction_change)
    dir_factor = np.sin(np.radians(mean_wind_dir_change))
    srh = 0.15 * shear_magnitude**2 * dir_factor
    return srh

print("\nWind Shear and Storm Type:")
print("-" * 70)
print(f"{'0-6km Shear (kt)':<18} {'SRH (m²/s²)':<15} {'Expected Storm Type'}")
print("-" * 70)

for shear_kt in [15, 25, 35, 45, 55, 70]:
    shear_ms = shear_kt * 0.514  # Convert to m/s
    srh = storm_relative_helicity(shear_ms)

    if shear_kt < 20:
        storm_type = "Ordinary cells (disorganized)"
    elif shear_kt < 35:
        storm_type = "Multicells (organized)"
    elif shear_kt < 50:
        storm_type = "Supercells possible"
    else:
        storm_type = "Supercells likely, tornadoes"

    print(f"{shear_kt:<18.0f} {srh:<15.0f} {storm_type}")


# =============================================================================
# PART 3: SUPERCELL DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: SUPERCELL STRUCTURE AND ROTATION")
print("=" * 70)

supercell_text = """
SUPERCELL: THE KING OF THUNDERSTORMS
====================================

A supercell is a rotating thunderstorm with a persistent mesocyclone.

HOW ROTATION DEVELOPS:
1. Environmental shear creates horizontal vorticity
   ω_h = ∂u/∂z (horizontal spin from wind changing with height)

2. Tilting: Updraft tilts horizontal vorticity into vertical
   ∂ω_z/∂t ∝ ω_h × (∂w/∂x)

3. Stretching: Rising air stretches vortex tubes
   ∂ω_z/∂t ∝ ω_z × (∂w/∂z)

   Like figure skater pulling arms in → spins faster!

4. Result: MESOCYCLONE (rotating updraft, 2-10 km wide)

SUPERCELL SPLITTING:
In straight-line shear, storm splits into:
- Right-moving storm (cyclonic, more likely to produce tornadoes)
- Left-moving storm (anticyclonic)

Dynamic pressure perturbations favor the right-mover
in the Northern Hemisphere.
"""
print(supercell_text)

def vorticity_tilting(horizontal_vorticity, updraft_gradient):
    """
    Rate of vorticity tilting.

    ∂ω_z/∂t = ω_h × (∂w/∂x)
    """
    return horizontal_vorticity * updraft_gradient

def vorticity_stretching(vertical_vorticity, vertical_velocity_gradient):
    """
    Rate of vorticity stretching.

    ∂ω_z/∂t = ω_z × (∂w/∂z)
    """
    return vertical_vorticity * vertical_velocity_gradient

print("\nVorticity Budget in Supercells:")
print("-" * 60)

# Typical supercell values
omega_h = 0.02  # Horizontal vorticity from shear (s⁻¹)
dw_dx = 0.01    # Updraft gradient (s⁻¹)
omega_z_initial = 0.001  # Initial vertical vorticity

# Mesocyclone develops over ~20 minutes
dt = 1200  # seconds

omega_z = omega_z_initial
print(f"Initial ω_z: {omega_z_initial:.4f} s⁻¹")
print()

for t in range(0, 1201, 300):
    # Tilting contribution
    tilting = vorticity_tilting(omega_h, dw_dx)

    # Stretching contribution (increases as omega_z grows)
    dw_dz = 0.015  # Vertical gradient
    stretching = vorticity_stretching(omega_z, dw_dz)

    # Update vorticity
    if t > 0:
        omega_z += (tilting + stretching) * 300

    period = 2 * np.pi / omega_z / 60 if omega_z > 0 else float('inf')
    print(f"t = {t:4d}s: ω_z = {omega_z:.4f} s⁻¹, rotation period = {period:.1f} min")


# =============================================================================
# PART 4: TORNADO PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: TORNADO GENESIS AND INTENSITY")
print("=" * 70)

tornado_text = """
TORNADO: CONCENTRATED VORTEX FROM SUPERCELL
============================================

Tornadoes form when mesocyclone vorticity concentrates near surface.

TORNADOGENESIS PROCESS:
1. Mesocyclone rotation descends (Rear Flank Downdraft)
2. Baroclinic generation of horizontal vorticity at surface
3. Tilting by updraft at gust front
4. Stretching intensifies rotation dramatically

VORTEX INTENSIFICATION (Stretching):
As vortex tube contracts from R₁ to R₂:
ω₂/ω₁ = (R₁/R₂)²

If radius decreases 10× → vorticity increases 100×!
This is why tornadoes can spin up so fast.

CYCLOSTROPHIC BALANCE:
In a tornado, centrifugal force balances pressure gradient:
V²/r = (1/ρ) × (∂p/∂r)

WIND SPEED vs PRESSURE DROP:
For intense tornadoes:
ΔP ≈ ρV²/2

100 mph tornado → ΔP ≈ 25 mb
200 mph tornado → ΔP ≈ 100 mb
300 mph tornado → ΔP ≈ 225 mb

EF SCALE (Enhanced Fujita):
EF0: 65-85 mph  (minor damage)
EF1: 86-110 mph
EF2: 111-135 mph
EF3: 136-165 mph
EF4: 166-200 mph (violent)
EF5: >200 mph   (incredible destruction)
"""
print(tornado_text)

def vortex_stretching_amplification(initial_radius, final_radius):
    """
    Calculate vorticity amplification from stretching.

    ω₂/ω₁ = (R₁/R₂)²
    """
    return (initial_radius / final_radius) ** 2

def tornado_pressure_drop(wind_speed_mph):
    """
    Estimate pressure drop in tornado core.

    ΔP ≈ ρV²/2 (cyclostrophic balance)
    """
    V = wind_speed_mph * 0.447  # Convert to m/s
    rho = 1.2  # kg/m³
    delta_p = rho * V**2 / 2
    return delta_p / 100  # Convert to mb

print("\nVortex Stretching Amplification:")
print("-" * 60)
print(f"{'Initial radius':<18} {'Final radius':<18} {'Vorticity ×'}")
print("-" * 60)

for R1, R2 in [(5000, 500), (2000, 200), (1000, 100), (500, 50)]:
    amp = vortex_stretching_amplification(R1, R2)
    print(f"{R1:<18.0f}m {R2:<18.0f}m {amp:<15.0f}×")

print("\n\nTornado Intensity and Pressure Drop:")
print("-" * 60)
print(f"{'EF Scale':<10} {'Wind (mph)':<15} {'Pressure Drop (mb)':<20}")
print("-" * 60)

ef_scale = [
    ("EF0", 75),
    ("EF1", 100),
    ("EF2", 125),
    ("EF3", 150),
    ("EF4", 180),
    ("EF5", 250),
]

for ef, wind in ef_scale:
    dp = tornado_pressure_drop(wind)
    print(f"{ef:<10} {wind:<15.0f} {dp:<20.1f}")


# =============================================================================
# PART 5: STORM COMPOSITE PARAMETERS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: SEVERE WEATHER PARAMETERS")
print("=" * 70)

params_text = """
COMPOSITE PARAMETERS FOR SEVERE WEATHER:
========================================

1. SIGNIFICANT TORNADO PARAMETER (STP)
   STP = (CAPE/1500) × (SRH/150) × (Shear/20) × (LCL/1500)

   STP > 1: Significant tornadoes possible
   STP > 3: Significant tornadoes likely

2. SUPERCELL COMPOSITE PARAMETER (SCP)
   SCP = (CAPE/1000) × (SRH/50) × (Shear/40)

   SCP > 1: Supercells possible
   SCP > 4: Strong supercells likely

3. ENERGY-HELICITY INDEX (EHI)
   EHI = (CAPE × SRH) / 160000

   EHI > 1: Significant tornadoes possible
   EHI > 3: Violent tornadoes possible

4. DERECHO COMPOSITE PARAMETER (DCP)
   DCP considers CAPE, shear, and DCAPE (downdraft CAPE)
   For damaging straight-line wind events
"""
print(params_text)

def significant_tornado_parameter(cape, srh, shear_kt, lcl_m):
    """Calculate Significant Tornado Parameter."""
    cape_term = min(cape / 1500, 2.0)  # Capped
    srh_term = min(srh / 150, 2.0)
    shear_term = min(shear_kt / 20, 2.0)
    lcl_term = max(0, (2000 - lcl_m) / 1000)  # Lower LCL = better

    stp = cape_term * srh_term * shear_term * lcl_term
    return stp

def supercell_composite(cape, srh, shear_kt):
    """Calculate Supercell Composite Parameter."""
    cape_term = cape / 1000
    srh_term = srh / 50
    shear_term = shear_kt / 40

    return cape_term * srh_term * shear_term

def energy_helicity_index(cape, srh):
    """Calculate Energy-Helicity Index."""
    return (cape * srh) / 160000

print("\nSevere Weather Parameter Examples:")
print("-" * 80)
print(f"{'Scenario':<25} {'CAPE':<8} {'SRH':<8} {'Shear':<8} {'STP':<8} {'SCP':<8} {'EHI':<8}")
print("-" * 80)

scenarios = [
    ("Marginal", 800, 100, 25, 1200),
    ("Moderate severe", 1500, 200, 35, 1000),
    ("Significant", 2500, 300, 45, 800),
    ("High-end outbreak", 4000, 450, 55, 600),
    ("Extreme (rare)", 5000, 600, 65, 500),
]

for name, cape, srh, shear, lcl in scenarios:
    stp = significant_tornado_parameter(cape, srh, shear, lcl)
    scp = supercell_composite(cape, srh, shear)
    ehi = energy_helicity_index(cape, srh)
    print(f"{name:<25} {cape:<8.0f} {srh:<8.0f} {shear:<8.0f} {stp:<8.1f} {scp:<8.1f} {ehi:<8.2f}")


# =============================================================================
# PART 6: HAIL PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: HAIL FORMATION PHYSICS")
print("=" * 70)

hail_text = """
HAIL: ICE GROWN IN STRONG UPDRAFTS
==================================

Hail forms when:
1. Ice embryos form above freezing level
2. Strong updrafts suspend ice in cloud
3. Supercooled water accretes onto ice
4. Hail falls when too heavy for updraft

HAIL SIZE vs UPDRAFT:
The minimum updraft to support hailstone:
V_updraft ≥ V_terminal = √(2mg / ρ_air C_D A)

For spherical hail: V_t ≈ 20 × D^0.5 (D in cm)

1 cm hail → 20 m/s updraft
2.5 cm (1") → 32 m/s updraft
5 cm (2") → 45 m/s updraft
10 cm (4") → 63 m/s updraft

SIGNIFICANT HAIL PARAMETER (SHIP):
Combines CAPE, 500mb T, lapse rate, freezing level
SHIP > 1: Large hail (>2") possible
SHIP > 2: Giant hail (>3") possible
"""
print(hail_text)

def hail_terminal_velocity(diameter_cm):
    """Terminal velocity of hailstone."""
    # Empirical: V_t ≈ 20 × D^0.5 m/s
    return 20 * np.sqrt(diameter_cm)

def required_updraft_for_hail(diameter_cm):
    """Minimum updraft to grow hailstone of given size."""
    # Need updraft > terminal velocity
    V_t = hail_terminal_velocity(diameter_cm)
    # Account for ice accretion time (need sustained support)
    return V_t * 1.1

print("\nHail Size vs Required Updraft:")
print("-" * 60)
print(f"{'Diameter (cm)':<15} {'Diameter (in)':<15} {'Required Updraft (m/s)':<25}")
print("-" * 60)

for d_cm in [1, 2.5, 4, 5, 7.5, 10, 15]:
    d_in = d_cm / 2.54
    V_req = required_updraft_for_hail(d_cm)
    print(f"{d_cm:<15.1f} {d_in:<15.1f} {V_req:<25.1f}")


# =============================================================================
# PART 7: CLIMATOLOGY AND CLIMATE CHANGE
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: SEVERE WEATHER AND CLIMATE CHANGE")
print("=" * 70)

climate_text = """
SEVERE WEATHER IN A WARMING CLIMATE:
====================================

COMPETING EFFECTS:

1. THERMODYNAMICS (favors MORE severe):
   - More CAPE (warmer, more humid surface)
   - More moisture → stronger storms
   - Clausius-Clapeyron: 7% more moisture per °C

2. DYNAMICS (uncertain/mixed):
   - Less shear? (reduced pole-equator gradient)
   - Jet stream changes uncertain
   - Shear is crucial for tornadoes!

CURRENT UNDERSTANDING:
- Total tornado count: No clear trend
- Intense tornado days: May be clustering more
- Tornado alley: Possibly shifting eastward
- Hail: Uncertain, complex relationship
- Derecho/straight-line wind: Likely increasing

THE CHALLENGE:
Severe storms are small, short-lived events
→ Hard to detect climate signal
→ Observation record has issues (population bias)
→ Models don't resolve individual storms

WHAT PHYSICS SUGGESTS:
1. Maximum hail size could increase (more CAPE)
2. Precipitation rates definitely increase (C-C)
3. Flash flooding from thunderstorms increases
4. Overall severe weather "season" may lengthen
"""
print(climate_text)

# Severe weather season length
def severe_season_with_warming(dT):
    """
    Estimate change in severe weather season.

    Proxy: Number of days with surface T > threshold
    """
    # Each 1°C shifts isotherms ~100-150 km poleward
    # This translates to ~1-2 week longer warm season
    extension_weeks = 1.5 * dT
    return extension_weeks

print("\nSevere Weather Season Extension with Warming:")
print("-" * 50)
for dT in [1, 2, 3, 4]:
    extension = severe_season_with_warming(dT)
    print(f"+{dT}°C warming: Season extends ~{extension:.1f} weeks")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: SEVERE WEATHER FROM FIRST PRINCIPLES")
print("=" * 70)

summary = """
KEY PHYSICS OF SEVERE STORMS:
============================

1. CAPE (Convective Available Potential Energy)
   - Measures buoyancy (thermal energy for storms)
   - w_max = √(2×CAPE)
   - Derived from parcel theory + thermodynamics

2. WIND SHEAR
   - Organizes storms, creates rotation
   - Horizontal vorticity from ∂u/∂z
   - Tilted into vertical by updraft

3. STORM ROTATION (Mesocyclone)
   - Tilting: ω_z ∝ ω_h × (∂w/∂x)
   - Stretching: ω_z intensifies as (R₁/R₂)²
   - Conservation of angular momentum

4. TORNADOES
   - Extreme vortex stretching near surface
   - Cyclostrophic balance: V²/r = (1/ρ)(∂p/∂r)
   - EF5: >200 mph, >100 mb pressure drop

5. HAIL
   - Updraft must exceed terminal velocity
   - V_t ≈ 20×√D for hail diameter D
   - Large hail needs 40-60+ m/s updrafts

6. COMPOSITE PARAMETERS
   - STP, SCP, EHI combine ingredients
   - Higher values → higher tornado probability

7. CLIMATE CHANGE
   - More CAPE (thermodynamics)
   - Uncertain shear changes (dynamics)
   - Net effect on tornadoes: uncertain
   - Flash flooding: definitely increasing


THE PHYSICS TELLS US:
=====================
Severe storms require:
- Instability (CAPE from buoyancy)
- Lift (forcing to release instability)
- Shear (organization and rotation)
- Moisture (fuel for latent heat)

These are the "ingredients" approach.
All derivable from thermodynamics and fluid dynamics.
"""
print(summary)

print("\n" + "=" * 70)
print("END OF SEVERE WEATHER PHYSICS")
print("=" * 70)
