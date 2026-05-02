#!/usr/bin/env python3
"""
OCEAN WAVES AND AIR-SEA INTERACTION - FIRST PRINCIPLES
======================================================

Deriving the physics of wind-wave generation, wave propagation,
and air-sea fluxes of momentum, heat, and moisture.
"""

import numpy as np

print("=" * 70)
print("OCEAN WAVES AND AIR-SEA INTERACTION - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
rho_air = 1.225    # Air density (kg/m³)
rho_water = 1025   # Seawater density (kg/m³)
c_p_air = 1004     # Specific heat air (J/kg/K)
c_p_water = 3850   # Specific heat seawater (J/kg/K)
L_v = 2.5e6        # Latent heat vaporization (J/kg)
sigma_water = 0.074  # Surface tension (N/m)


# =============================================================================
# PART 1: SURFACE GRAVITY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: SURFACE GRAVITY WAVE PHYSICS")
print("=" * 70)

wave_text = """
SURFACE GRAVITY WAVES:
======================

DISPERSION RELATION:

ω² = gk × tanh(kh)

Where:
- ω = angular frequency
- k = wavenumber = 2π/λ
- h = water depth

DEEP WATER (kh >> 1, tanh(kh) → 1):

ω² = gk
c = ω/k = √(g/k) = √(gλ/2π)

Longer waves travel FASTER!

Phase speed: c = g/(2πf) = 1.56 × T (m/s, T in seconds)

Group velocity: c_g = c/2 (energy travels at half phase speed!)

SHALLOW WATER (kh << 1):

c = √(gh)

All wavelengths travel at same speed (non-dispersive)

WAVE PARAMETERS:

H = wave height (trough to crest)
T = period
λ = wavelength
f = frequency = 1/T

Steepness: H/λ < 1/7 before breaking
Significant wave height H_s = average of highest 1/3

WAVE ENERGY:

E = ρgH²/8 per unit area (J/m²)

Energy flux: P = E × c_g (W/m)
"""
print(wave_text)

def deep_water_phase_speed(wavelength_m):
    """Deep water wave phase speed."""
    return np.sqrt(g * wavelength_m / (2 * np.pi))

def deep_water_wavelength(period_s):
    """Deep water wavelength from period."""
    return g * period_s**2 / (2 * np.pi)

def wave_period_from_wavelength(wavelength_m):
    """Wave period from wavelength (deep water)."""
    return np.sqrt(2 * np.pi * wavelength_m / g)

def wave_energy(height_m, rho=1025):
    """Wave energy per unit area (J/m²)."""
    return rho * g * height_m**2 / 8

def wave_power(height_m, period_s):
    """Wave energy flux (kW/m of wave crest)."""
    wavelength = deep_water_wavelength(period_s)
    c = deep_water_phase_speed(wavelength)
    c_g = c / 2  # Group velocity
    E = wave_energy(height_m)
    return E * c_g / 1000  # kW/m

print("\nDeep Water Wave Properties:")
print("-" * 65)
print(f"{'Period (s)':<12} {'Wavelength (m)':<18} {'Phase speed (m/s)':<20} {'c_g (m/s)'}")
print("-" * 65)

for T in [2, 5, 8, 10, 12, 15, 20]:
    lam = deep_water_wavelength(T)
    c = deep_water_phase_speed(lam)
    cg = c / 2
    print(f"{T:<12} {lam:<18.0f} {c:<20.1f} {cg:.1f}")


# =============================================================================
# PART 2: WIND-WAVE GENERATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: WIND-WAVE GENERATION")
print("=" * 70)

generation_text = """
WIND-WAVE GENERATION:
=====================

MECHANISMS:

1. PHILLIPS MECHANISM (Initial generation)
   - Turbulent pressure fluctuations
   - Resonance with wave components
   - Creates initial ripples

2. MILES MECHANISM (Growth)
   - Wind shear over wavy surface
   - Pressure-wave correlation
   - Exponential growth: E ∝ exp(βt)

GROWTH RATE:

β ∝ (u*/c)² × ω

Where u* = friction velocity

Waves grow until c ≈ U (phase speed matches wind)

FETCH AND DURATION:

Fetch (F) = distance over which wind blows
Duration (t) = time wind has blown

FULLY DEVELOPED SEA:

When waves reach equilibrium with wind
No further growth possible

For U = 10 m/s:
- Fetch needed: ~100 km
- Duration needed: ~10 hours
- H_s ≈ 2.5 m
- T_p ≈ 8 s

WAVE SPECTRUM:

Pierson-Moskowitz (fully developed):
S(f) = αg²(2πf)⁻⁵ exp[-β(f/f_p)⁻⁴]

Peak frequency: f_p = 0.13g/U

JONSWAP (fetch-limited):
Adds peak enhancement factor γ
"""
print(generation_text)

def fully_developed_Hs(wind_speed_ms):
    """
    Significant wave height for fully developed sea.

    H_s ≈ 0.025 × U²  (empirical)
    """
    return 0.025 * wind_speed_ms**2

def fully_developed_period(wind_speed_ms):
    """
    Peak period for fully developed sea.

    T_p ≈ 0.8 × U  (empirical)
    """
    return 0.8 * wind_speed_ms

def fetch_limited_Hs(wind_speed_ms, fetch_km):
    """
    Significant wave height for fetch-limited conditions.

    Simplified JONSWAP relationship.
    """
    # Non-dimensional fetch
    X_tilde = g * fetch_km * 1000 / wind_speed_ms**2

    # H_s growth with fetch
    Hs = 0.0016 * wind_speed_ms**2 * X_tilde**0.5

    # Cap at fully developed
    Hs_fd = fully_developed_Hs(wind_speed_ms)
    return min(Hs, Hs_fd)

print("\nFully Developed Sea State:")
print("-" * 55)
print(f"{'Wind (m/s)':<12} {'H_s (m)':<12} {'T_p (s)':<12} {'Beaufort'}")
print("-" * 55)

beaufort = {5: 3, 10: 5, 15: 7, 20: 8, 25: 9, 30: 10}

for U in [5, 10, 15, 20, 25, 30]:
    Hs = fully_developed_Hs(U)
    Tp = fully_developed_period(U)
    B = beaufort.get(U, "")
    print(f"{U:<12} {Hs:<12.1f} {Tp:<12.0f} {B}")


# =============================================================================
# PART 3: AIR-SEA MOMENTUM FLUX
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: AIR-SEA MOMENTUM FLUX")
print("=" * 70)

momentum_text = """
WIND STRESS:
============

τ = ρ_air × C_D × U₁₀²

Where:
- C_D = drag coefficient (~1.0-2.5 × 10⁻³)
- U₁₀ = 10-m wind speed

DRAG COEFFICIENT:

Depends on:
- Wind speed (increases with U)
- Sea state (wave age)
- Stability

Empirical (Large & Pond):
C_D × 10³ = 0.49 + 0.065 × U₁₀  (for U₁₀ > 11 m/s)

At high winds (> 30 m/s):
C_D may saturate or decrease (sea spray, foam)

MOMENTUM PARTITION:

Total stress = Wave stress + Turbulent stress

Wave stress: τ_wave ≈ 0.1-0.5 × τ_total (young seas)
Turbulent stress: Direct momentum transfer

WAVE AGE:

c_p / u* = wave age

Young sea: c_p/u* < 20 (steep, actively growing)
Old sea: c_p/u* > 30 (swell, not growing)

Young seas have HIGHER drag!
"""
print(momentum_text)

def drag_coefficient(U10):
    """
    Wind stress drag coefficient.

    Large & Pond formulation.
    """
    if U10 < 11:
        Cd = 1.2e-3
    else:
        Cd = (0.49 + 0.065 * U10) * 1e-3
    return Cd

def wind_stress(U10, rho=1.225):
    """
    Wind stress on ocean surface.

    τ = ρ C_D U²
    """
    Cd = drag_coefficient(U10)
    return rho * Cd * U10**2

def friction_velocity(stress, rho=1.225):
    """Friction velocity u* from stress."""
    return np.sqrt(stress / rho)

print("\nWind Stress vs Wind Speed:")
print("-" * 60)
print(f"{'U₁₀ (m/s)':<12} {'C_D (×10⁻³)':<15} {'τ (N/m²)':<15} {'u* (m/s)'}")
print("-" * 60)

for U in [5, 10, 15, 20, 25, 30, 35, 40]:
    Cd = drag_coefficient(U)
    tau = wind_stress(U)
    ustar = friction_velocity(tau)
    print(f"{U:<12} {Cd*1000:<15.2f} {tau:<15.2f} {ustar:.2f}")


# =============================================================================
# PART 4: AIR-SEA HEAT FLUX
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: AIR-SEA HEAT FLUX")
print("=" * 70)

heat_text = """
AIR-SEA HEAT FLUXES:
====================

Net heat flux: Q_net = Q_SW - Q_LW - Q_SH - Q_LH

1. SHORTWAVE RADIATION (Q_SW)
   Solar absorbed by ocean
   Q_SW = (1 - α) × S↓
   Where α ≈ 0.06 (ocean albedo)

2. LONGWAVE RADIATION (Q_LW)
   Infrared emission from ocean
   Q_LW = εσT⁴ - Q_LW↓
   Net upward typically 40-80 W/m²

3. SENSIBLE HEAT (Q_SH)
   Direct heat transfer (conduction/convection)
   Q_SH = ρ c_p C_H U (T_s - T_a)

   C_H ≈ 1.0 × 10⁻³ (Stanton number)

4. LATENT HEAT (Q_LH)
   Evaporation cooling
   Q_LH = ρ L_v C_E U (q_s - q_a)

   C_E ≈ 1.2 × 10⁻³ (Dalton number)

TYPICAL VALUES:

Open ocean annual mean:
- Q_SW: +170 W/m²
- Q_LW: -50 W/m²
- Q_SH: -10 W/m²
- Q_LH: -100 W/m²
- Q_net: +10 W/m² (slight warming)

Tropical: Q_net > 0 (heat gain)
High latitude: Q_net < 0 (heat loss)
"""
print(heat_text)

def sensible_heat_flux(U, T_sea, T_air, Ch=1.0e-3, rho=1.225, cp=1004):
    """
    Sensible heat flux (W/m²).

    Positive = ocean gains heat
    """
    return -rho * cp * Ch * U * (T_sea - T_air)

def latent_heat_flux(U, q_sat_sea, q_air, Ce=1.2e-3, rho=1.225, Lv=2.5e6):
    """
    Latent heat flux (W/m²).

    Positive = ocean gains heat (condensation)
    Negative = ocean loses heat (evaporation)
    """
    return -rho * Lv * Ce * U * (q_sat_sea - q_air)

def saturation_specific_humidity(T_celsius, P_hPa=1013):
    """Saturation specific humidity over water."""
    e_s = 6.11 * 10**(7.5 * T_celsius / (237.3 + T_celsius))
    return 0.622 * e_s / P_hPa

print("\nSensible Heat Flux:")
print("-" * 55)
print(f"{'U (m/s)':<12} {'T_sea - T_air (°C)':<20} {'Q_SH (W/m²)'}")
print("-" * 55)

for U in [5, 10, 15]:
    for dT in [-2, 0, 2, 5]:
        Qsh = sensible_heat_flux(U, 25, 25-dT)
        if U == 10:
            print(f"{U:<12} {dT:<20} {Qsh:.0f}")

print("\n\nLatent Heat Flux (evaporation):")
print("-" * 60)

for U in [5, 10, 15, 20]:
    q_sea = saturation_specific_humidity(28)
    q_air = saturation_specific_humidity(26) * 0.8  # 80% RH
    Qlh = latent_heat_flux(U, q_sea, q_air)
    print(f"U = {U} m/s, SST = 28°C, Ta = 26°C, RH = 80%: Q_LH = {Qlh:.0f} W/m²")


# =============================================================================
# PART 5: MIXED LAYER DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: OCEAN MIXED LAYER")
print("=" * 70)

mld_text = """
OCEAN MIXED LAYER:
==================

Upper ocean layer well-mixed by:
- Wind-driven turbulence
- Surface cooling (convection)
- Breaking waves

MIXED LAYER DEPTH (MLD):

Where temperature/density changes rapidly
Typical: 20-200 m

SEASONAL CYCLE:

Summer: Shallow MLD (heating, weak winds)
Winter: Deep MLD (cooling, strong winds)
Spring: Restratification

HEAT CONTENT:

OHC = ρ c_p × MLD × ΔT

For MLD = 100 m, ΔT = 1°C:
OHC ≈ 4 × 10⁸ J/m² = 400 MJ/m²

Equivalent to ~25 days of solar heating!

TURBULENT MIXING:

TKE from:
1. Wind work: w'b' ∝ u*³
2. Breaking waves
3. Shear instability

Richardson number: Ri = N²/(∂u/∂z)²
MLD deepens when Ri < 0.25

ENTRAINMENT:

MLD deepens by entraining water below
w_e = dh/dt = f(u*, B_0, N²)

Kraus-Turner model:
w_e × Δb × h = 2m × u*³ + h × B_0

Where B_0 = surface buoyancy flux
"""
print(mld_text)

def ocean_heat_content(mld_m, T_anomaly_C, rho=1025, cp=3850):
    """
    Ocean heat content anomaly (J/m²).
    """
    return rho * cp * mld_m * T_anomaly_C

def mld_response_time(mld_m, heat_flux_Wm2, rho=1025, cp=3850):
    """
    Time to change MLD temperature by 1°C.
    """
    # Q = ρ c_p h dT/dt
    # dT/dt = Q / (ρ c_p h)
    dT_dt = heat_flux_Wm2 / (rho * cp * mld_m)  # °C/s
    return 1 / dT_dt / 86400  # days per °C

print("\nMixed Layer Heat Capacity:")
print("-" * 55)
print(f"{'MLD (m)':<12} {'OHC per °C (MJ/m²)':<22} {'Days to warm 1°C'}")
print("-" * 55)

for h in [20, 50, 100, 200, 500]:
    ohc = ocean_heat_content(h, 1) / 1e6  # MJ
    days = mld_response_time(h, 200)  # 200 W/m² net flux
    print(f"{h:<12} {ohc:<22.0f} {days:.0f}")


# =============================================================================
# PART 6: SEA SPRAY AND HIGH WINDS
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: SEA SPRAY PHYSICS")
print("=" * 70)

spray_text = """
SEA SPRAY AT HIGH WINDS:
========================

FORMATION MECHANISMS:

1. BUBBLE BURSTING
   - Whitecaps produce bubbles
   - Bubbles burst at surface
   - Jet drops + film drops
   - Dominates at U < 20 m/s

2. SPUME GENERATION
   - Wind tears droplets from wave crests
   - Large drops (> 100 μm)
   - Dominates at U > 25 m/s

SPRAY EFFECTS:

1. HEAT FLUX ENHANCEMENT
   Spray evaporation → latent heat transfer
   At U > 25 m/s: Spray flux comparable to interfacial

2. MOMENTUM MODIFICATION
   Spray removes momentum
   May cause drag saturation at high winds

3. SALT FLUX
   Sea salt aerosol production
   CCN for cloud formation

HURRICANE IMPLICATIONS:

U > 50 m/s: Intense spray
- Obscures air-sea interface
- Modifies thermodynamic fluxes
- May limit hurricane intensity

Spray heat flux:
Q_spray ~ 10³ W/m² at U = 60 m/s (comparable to Q_LH)

SPRAY GENERATION FUNCTION:

dF/dr = f(U, r) droplets per m² per s per μm

Increases rapidly with wind speed (~U³ to U⁴)
"""
print(spray_text)

def spray_flux_estimate(U10, r_um=50):
    """
    Rough estimate of spray droplet flux.

    Increases as ~U³ to U⁴
    """
    # Very approximate
    flux = 1e3 * (U10 / 10)**3.5 * np.exp(-r_um / 100)
    return flux  # droplets/m²/s/μm

def spray_heat_flux(U10):
    """
    Estimate spray-mediated heat flux.

    Becomes significant at high wind speeds.
    """
    if U10 < 15:
        return 0
    # Increases rapidly above threshold
    return 5 * (U10 - 15)**2

print("\nSpray Effects at High Wind Speeds:")
print("-" * 55)
print(f"{'U₁₀ (m/s)':<15} {'Spray Q (W/m²)':<20} {'Regime'}")
print("-" * 55)

for U in [10, 20, 30, 40, 50, 60, 70]:
    Q_spray = spray_heat_flux(U)
    if U < 20:
        regime = "Bubble-dominated"
    elif U < 35:
        regime = "Transition"
    else:
        regime = "Spume-dominated"
    print(f"{U:<15} {Q_spray:<20.0f} {regime}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: OCEAN WAVES AND AIR-SEA INTERACTION")
print("=" * 70)

summary = """
KEY PHYSICS:
===========

1. SURFACE GRAVITY WAVES
   - Deep water: c = √(gλ/2π), c_g = c/2
   - Energy: E = ρgH²/8
   - Longer waves travel faster (dispersive)

2. WIND-WAVE GENERATION
   - Phillips (initial) + Miles (growth)
   - Fully developed: H_s ≈ 0.025U²
   - Fetch and duration limited growth
   - JONSWAP/PM spectra

3. MOMENTUM FLUX
   - τ = ρ C_D U²
   - C_D ~ 1-2.5 × 10⁻³
   - Wave age affects drag
   - Saturation at high winds?

4. HEAT FLUXES
   - Q_SW (solar) + Q_LW + Q_SH + Q_LH
   - Latent heat dominates cooling
   - Bulk formulas: Q ∝ C U ΔX

5. MIXED LAYER
   - Depth: 20-200 m seasonally
   - OHC = ρ c_p h ΔT
   - Huge thermal inertia
   - Wind and buoyancy mixing

6. SEA SPRAY
   - Bubble bursting + spume
   - Modifies fluxes at U > 25 m/s
   - May limit hurricane intensity


THE PHYSICS TELLS US:
====================
- Ocean waves are dispersive (long waves faster)
- Wind-wave growth saturates (fully developed)
- Heat flux formulas work well to ~30 m/s
- Sea spray dominates at extreme winds
- Ocean mixed layer has enormous heat capacity
- Air-sea coupling crucial for weather/climate
"""
print(summary)

print("\n" + "=" * 70)
print("END OF OCEAN WAVES AND AIR-SEA INTERACTION")
print("=" * 70)
