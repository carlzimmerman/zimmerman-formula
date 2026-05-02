#!/usr/bin/env python3
"""
MOUNTAIN METEOROLOGY - FIRST PRINCIPLES
========================================

Deriving the physics of orographic effects, lee waves,
downslope windstorms, foehn warming, and mountain circulations.
"""

import numpy as np

print("=" * 70)
print("MOUNTAIN METEOROLOGY - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
R_d = 287.0        # Gas constant dry air (J/kg/K)
c_p = 1004         # Specific heat (J/kg/K)
L_v = 2.5e6        # Latent heat of vaporization (J/kg)


# =============================================================================
# PART 1: OROGRAPHIC LIFTING
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: OROGRAPHIC LIFTING AND PRECIPITATION")
print("=" * 70)

orographic_text = """
OROGRAPHIC LIFTING:
===================

Air forced to rise over mountains (mechanical lifting)

VERTICAL VELOCITY:

w = U × tan(α) = U × (dh/dx)

Where:
- U = horizontal wind speed
- α = terrain slope angle
- dh/dx = terrain gradient

For typical mountain:
- U = 15 m/s
- slope = 10% = 0.1
- w = 15 × 0.1 = 1.5 m/s

THAT'S 10× STRONGER than typical frontal lifting (~0.1 m/s)!

PRECIPITATION ENHANCEMENT:

Clausius-Clapeyron: More moisture condenses at higher altitude

P_orog / P_flat ≈ exp(w × z_crest / H_scale)

Where H_scale = moisture scale height ≈ 2-3 km

OROGRAPHIC PRECIPITATION DISTRIBUTION:
- Maximum on WINDWARD slopes
- "Rain shadow" on leeward side
- Wet side can get 5-10× more rain than dry side

EXAMPLES:
- Hawaii: 10,000 mm/year on Mt. Waialeale (windward)
         250 mm/year on west side (leeward)
- Cascades: 3000 mm in mountains
           250 mm in eastern WA

MASS BUDGET:

Moisture flux in = Moisture flux out + Precipitation

∂(ρq)/∂t + ∇·(ρqV) = E - C

At steady state over mountain:
P ≈ ∫ ρ q U dz × (width) × lifting efficiency
"""
print(orographic_text)

def orographic_lift_velocity(wind_speed, terrain_slope):
    """Calculate vertical velocity from terrain forcing."""
    return wind_speed * terrain_slope

def orographic_precip_enhancement(w_vertical, crest_height, H_scale=2500):
    """
    Estimate precipitation enhancement factor.

    Simplified: More lifting = more condensation
    """
    # Time to ascend to crest
    if w_vertical > 0:
        t_ascent = crest_height / w_vertical
    else:
        return 1.0

    # Condensation increases with altitude
    enhancement = 1 + (crest_height / H_scale) * (w_vertical / 1.0)
    return min(enhancement, 10)  # Cap at 10×

print("\nOrographic Lifting by Terrain Slope:")
print("-" * 60)
print(f"{'Wind (m/s)':<12} {'Slope (%)':<12} {'w (m/s)':<12} {'Enhancement'}")
print("-" * 60)

for U in [10, 15, 20]:
    for slope_pct in [5, 10, 20, 30]:
        slope = slope_pct / 100
        w = orographic_lift_velocity(U, slope)
        enh = orographic_precip_enhancement(w, 2000)
        print(f"{U:<12} {slope_pct:<12} {w:<12.1f} {enh:.1f}×")


# =============================================================================
# PART 2: LEE WAVES AND MOUNTAIN WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: LEE WAVES (MOUNTAIN WAVES)")
print("=" * 70)

leewave_text = """
LEE WAVE PHYSICS:
=================

Mountain displaces air upward → oscillation → wave pattern downstream

GOVERNING EQUATION:

∂²w/∂z² + (N² - U²k²)/U² × w = 0

Where:
- N = Brunt-Väisälä frequency (stability)
- U = wind speed
- k = horizontal wavenumber

SCORER PARAMETER:

l² = N²/U² - (1/U)(∂²U/∂z²)

Simplified (constant U):  l = N/U

LEE WAVELENGTH:

λ = 2π/l = 2πU/N

For typical conditions:
- U = 20 m/s
- N = 0.01 s⁻¹
- λ = 2π × 20 / 0.01 = 12.6 km

WAVE TYPES:

1. VERTICALLY PROPAGATING (l² > k²)
   - Waves propagate upward
   - Can reach stratosphere
   - Clear air turbulence aloft

2. TRAPPED (l decreases with height)
   - Waves trapped below inversion
   - Horizontal propagation only
   - Rotor clouds below crests

VISUAL SIGNATURES:
- Lenticular clouds (lens-shaped)
- Rotor clouds (rolling beneath wave crests)
- Wave clouds parallel to mountain

AMPLITUDE:

Wave amplitude ≈ Mountain height × (N/U) × decay factor

Stronger waves when:
- Higher mountains
- Stronger stability (N)
- Moderate wind (not too fast)
"""
print(leewave_text)

def brunt_vaisala_frequency(dT_dz, T_mean):
    """
    Calculate Brunt-Väisälä frequency.

    N² = (g/T) × (dT/dz + g/c_p)

    dT_dz: Environmental lapse rate (K/m), negative for temperature decrease
    """
    gamma_d = g / c_p  # Dry adiabatic lapse rate
    N_squared = (g / T_mean) * (-dT_dz + gamma_d)
    if N_squared > 0:
        return np.sqrt(N_squared)
    else:
        return 0  # Unstable - no waves

def lee_wavelength(U, N):
    """Calculate lee wave wavelength."""
    if N == 0:
        return float('inf')
    return 2 * np.pi * U / N

def froude_number(U, N, h_mtn):
    """
    Mountain Froude number.

    Fr = U / (N × h)

    Fr << 1: Flow blocked
    Fr >> 1: Flow goes over easily
    Fr ≈ 1: Maximum wave amplitude
    """
    if N * h_mtn == 0:
        return float('inf')
    return U / (N * h_mtn)

print("\nLee Wave Characteristics:")
print("-" * 70)
print(f"{'Lapse (°C/km)':<15} {'N (s⁻¹)':<12} {'U (m/s)':<10} {'λ (km)':<12} {'Fr (1km mtn)'}")
print("-" * 70)

for lapse in [4, 6, 8, 10]:  # °C/km (6.5 is standard)
    dT_dz = -lapse / 1000  # Convert to K/m
    N = brunt_vaisala_frequency(dT_dz, 270)
    for U in [15, 25]:
        wavelength = lee_wavelength(U, N) / 1000  # km
        Fr = froude_number(U, N, 1000)
        print(f"{lapse:<15} {N:<12.4f} {U:<10} {wavelength:<12.1f} {Fr:.2f}")


# =============================================================================
# PART 3: DOWNSLOPE WINDSTORMS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: DOWNSLOPE WINDSTORMS")
print("=" * 70)

downslope_text = """
DOWNSLOPE WINDSTORM PHYSICS:
============================

The most violent mountain weather phenomenon!

EXAMPLES:
- Chinook (Rocky Mountains)
- Foehn (Alps)
- Bora (Adriatic)
- Santa Ana (California)

MECHANISM - HYDRAULIC THEORY:

Flow over mountain behaves like water over dam!

Bernoulli's equation along streamline:
P/ρ + gz + ½V² = constant

As air descends (z decreases):
- Potential energy converts to kinetic
- Velocity INCREASES

CRITICAL LAYER INTERACTION:

Key insight: Wave breaking at critical level

When mountain wave overturns (wave breaks) in stratosphere:
→ Creates "dividing streamline"
→ Flow below is hydraulically controlled
→ SEVERE acceleration on lee side

MAXIMUM WIND SPEED:

From energy conservation (simplified):

V_lee² = V_upwind² + 2g × Δz × (T_diff/T_mean)

Where Δz = descent from crest to valley

More complete (with wave breaking):
V_max ≈ √(2 × N × h_crest × U_crest)

For severe events:
- h = 3000 m
- N = 0.015 s⁻¹
- U = 25 m/s

V_max ≈ √(2 × 0.015 × 3000 × 25) = 47 m/s = 105 mph!

CONDITIONS FOR SEVERE DOWNSLOPE WINDS:
1. Strong cross-mountain flow (20-40 m/s)
2. Stable layer near crest level (inversion)
3. Weak stability above (allows wave breaking)
4. Critical level in mid-troposphere
"""
print(downslope_text)

def downslope_wind_estimate(h_crest, N, U_crest):
    """
    Estimate maximum downslope wind speed.

    Based on hydraulic jump analog with wave breaking.
    """
    # Simplified formula
    V_max = np.sqrt(2 * N * h_crest * U_crest)
    return V_max

def bernoulli_acceleration(V_initial, delta_z, T_warm=None, T_cold=None):
    """
    Wind acceleration from Bernoulli effect on descent.

    If warm/cold given, include temperature effect.
    """
    # Pure elevation change
    V_squared = V_initial**2 + 2 * g * delta_z

    # With temperature (density) effect
    if T_warm and T_cold:
        buoyancy_factor = (T_warm - T_cold) / T_cold
        V_squared += 2 * g * delta_z * buoyancy_factor

    return np.sqrt(max(V_squared, 0))

print("\nDownslope Wind Estimates:")
print("-" * 65)
print(f"{'Crest (m)':<12} {'N (s⁻¹)':<12} {'U_crest (m/s)':<15} {'V_max (m/s)':<12} {'mph'}")
print("-" * 65)

for h in [1500, 2000, 2500, 3000, 3500]:
    for N in [0.01, 0.015]:
        for U in [20, 30]:
            V_max = downslope_wind_estimate(h, N, U)
            V_mph = V_max * 2.237
            if N == 0.015 and U == 25:
                V_max = downslope_wind_estimate(h, N, 25)
                V_mph = V_max * 2.237
                print(f"{h:<12} {N:<12} {25:<15} {V_max:<12.0f} {V_mph:.0f}")


# =============================================================================
# PART 4: FOEHN WARMING
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: FOEHN WARMING (CHINOOK EFFECT)")
print("=" * 70)

foehn_text = """
FOEHN WARMING:
==============

Air arrives on lee side WARMER and DRIER than it started!

THE MECHANISM:

1. ASCENT (windward):
   - Air rises, cools at dry adiabatic rate: 9.8°C/km
   - Reaches saturation (LCL)
   - Above LCL: cools at moist adiabatic rate: ~6°C/km
   - Moisture condenses → precipitation on windward side

2. CREST:
   - Air has lost moisture
   - Now has lower mixing ratio

3. DESCENT (leeward):
   - Air descends, warms at DRY adiabatic rate: 9.8°C/km
   - Because moisture was removed, stays unsaturated
   - Warms faster than it cooled!

TEMPERATURE CHANGE:

ΔT_foehn = (Γ_d - Γ_m) × Δz_condensation

Where:
- Γ_d = 9.8°C/km (dry adiabatic)
- Γ_m ≈ 6°C/km (moist adiabatic)
- Δz_condensation = height from LCL to crest

For typical case:
- LCL at 1 km AGL
- Crest at 3 km AGL
- Δz = 2 km

ΔT = (9.8 - 6) × 2 = 7.6°C warming!

Plus: Precipitation on windward side → permanent moisture loss

RELATIVE HUMIDITY DROP:

Starting: 80%
After foehn: 20-30%

This is why chinook winds can rapidly melt snow
(January 1972, Loma Montana: -48°C to +9°C in 24 hours!)
"""
print(foehn_text)

def foehn_warming(h_lcl, h_crest, gamma_d=9.8, gamma_m=6.0):
    """
    Calculate foehn warming.

    Temperature increase on lee side due to asymmetric cooling/warming.
    """
    if h_crest <= h_lcl:
        return 0

    delta_z = h_crest - h_lcl  # Height above LCL (moist ascent)
    delta_T = (gamma_d - gamma_m) * delta_z / 1000  # Convert to km
    return delta_T

def lee_temperature(T_start, h_start, h_crest, h_lee, lcl_height):
    """
    Calculate temperature on lee side after foehn process.
    """
    # 1. Dry ascent to LCL
    if lcl_height > h_start:
        T_lcl = T_start - 9.8 * (lcl_height - h_start) / 1000
        h_current = lcl_height
    else:
        T_lcl = T_start
        h_current = h_start

    # 2. Moist ascent to crest
    T_crest = T_lcl - 6.0 * (h_crest - h_current) / 1000

    # 3. Dry descent to lee
    T_lee = T_crest + 9.8 * (h_crest - h_lee) / 1000

    return T_lee

print("\nFoehn Warming Examples:")
print("-" * 60)
print(f"{'LCL (m)':<12} {'Crest (m)':<12} {'ΔT warming (°C)':<20}")
print("-" * 60)

for lcl in [500, 1000, 1500, 2000]:
    for crest in [2000, 2500, 3000, 3500]:
        if crest > lcl:
            dT = foehn_warming(lcl, crest)
            print(f"{lcl:<12} {crest:<12} {dT:<20.1f}")

print("\n\nComplete Foehn Example:")
print("-" * 60)
print("Air starts at 1000m, T = 20°C, LCL = 1500m, Crest = 3500m, Lee = 500m")
T_lee = lee_temperature(20, 1000, 3500, 500, 1500)
print(f"Lee-side temperature: {T_lee:.1f}°C")
print(f"Net warming from start: {T_lee - 20:.1f}°C")


# =============================================================================
# PART 5: VALLEY AND SLOPE CIRCULATIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: THERMALLY-DRIVEN MOUNTAIN CIRCULATIONS")
print("=" * 70)

circulation_text = """
DIURNAL MOUNTAIN CIRCULATIONS:
==============================

Differential heating creates local wind systems

1. SLOPE WINDS:

ANABATIC (upslope) - Daytime:
- Slopes heat faster than free air
- Warm air rises along slope
- Convergence at ridge top
- Triggers afternoon thunderstorms!

KATABATIC (downslope) - Nighttime:
- Slopes cool by radiation
- Cold air drains downhill
- Pools in valleys (cold air lake)

SPEED ESTIMATE:
From buoyancy: w ≈ √(g × ΔT/T × L × sin(α))

Where:
- ΔT = temperature excess
- L = slope length
- α = slope angle

Typical: 2-5 m/s

2. VALLEY WINDS:

DAYTIME (Up-valley):
- Valley heats more than plains (enclosed volume)
- Pressure lower in valley
- Wind blows INTO valley
- Speed: 5-10 m/s

NIGHTTIME (Down-valley):
- Opposite process
- Cold air drains down-valley
- Speed: 2-5 m/s

3. GLACIER WIND:
- Persistent katabatic flow over ice
- Cold air always sinks off glacier
- Can be very strong and steady

4. MOUNTAIN-PLAIN CIRCULATION:
- Mountains act as "elevated heat source"
- Large-scale convergence in daytime
- Enhances thunderstorm development
"""
print(circulation_text)

def katabatic_speed(delta_T, slope_length, slope_angle_deg, T_env=280):
    """
    Estimate katabatic (downslope) wind speed.

    From integration of buoyancy along slope.
    """
    alpha = np.radians(slope_angle_deg)

    # Simplified: terminal velocity estimate
    # Balance friction vs buoyancy
    buoyancy = g * (delta_T / T_env) * np.sin(alpha)

    # Assuming friction balances over length L
    # v² ≈ 2 × buoyancy × L × efficiency
    efficiency = 0.2  # Friction reduces speed

    v = np.sqrt(2 * buoyancy * slope_length * efficiency)
    return v

def valley_pressure_deficit(delta_T, valley_depth, T_env=290):
    """
    Pressure deficit in heated valley.

    From hydrostatic integration.
    """
    # Δp ≈ ρ × g × h × (ΔT/T)
    rho = 1.225
    delta_p = rho * g * valley_depth * (delta_T / T_env)
    return delta_p

print("\nKatabatic Wind Speeds:")
print("-" * 60)
print(f"{'ΔT (°C)':<12} {'Slope (km)':<12} {'Angle (°)':<12} {'Speed (m/s)'}")
print("-" * 60)

for dT in [3, 5, 8, 10]:
    for length in [1, 3, 5]:
        for angle in [5, 10, 20]:
            v = katabatic_speed(dT, length*1000, angle)
            if length == 3:  # Show one length per dT
                print(f"{dT:<12} {length:<12} {angle:<12} {v:<.1f}")


# =============================================================================
# PART 6: GAP WINDS AND CHANNELING
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: GAP WINDS AND TERRAIN CHANNELING")
print("=" * 70)

gap_text = """
GAP WINDS (Channel Winds):
==========================

Wind accelerates through gaps in mountain barriers

VENTURI EFFECT:

Mass conservation: ρ₁A₁V₁ = ρ₂A₂V₂

If gap narrows: V₂ = V₁ × (A₁/A₂)

Speed increase = Area ratio

PLUS: Pressure gradient enhancement

Total gap wind speed:

V_gap ≈ √(V_approach² + 2ΔP/ρ)

Where ΔP = pressure difference across barrier

FAMOUS GAP WINDS:

1. SANTA ANA (California)
   - High pressure in Great Basin
   - Flow through mountain passes
   - Enhanced by downslope acceleration
   - Fire weather hazard!

2. MISTRAL (France)
   - Rhône Valley channeling
   - Persistent, strong (30-60 mph)

3. TEHUANTEPECER (Mexico)
   - Gap in Sierra Madre
   - Cold air outbreaks to Pacific
   - Creates oceanic wind jets

4. COLUMBIA GORGE (PNW)
   - Sea-level passage through Cascades
   - Pressure-driven flow
   - Winter: East wind (cold)
   - Summer: West wind (cool)

CHANNELING FACTOR:

V_channel / V_ambient ≈ 1.5-3.0 depending on geometry
"""
print(gap_text)

def gap_wind_speed(V_approach, delta_P, area_ratio=2, rho=1.225):
    """
    Calculate gap wind speed.

    Combines Venturi effect and pressure gradient.
    """
    # Venturi contribution
    V_venturi = V_approach * area_ratio

    # Pressure gradient contribution
    V_pressure = np.sqrt(2 * abs(delta_P) / rho)

    # Combined (not simply additive)
    V_gap = np.sqrt(V_venturi**2 + V_pressure**2)

    return V_gap, V_venturi, V_pressure

print("\nGap Wind Enhancement:")
print("-" * 70)
print(f"{'V_in (m/s)':<12} {'ΔP (hPa)':<12} {'Area ratio':<12} {'V_gap (m/s)':<15} {'Enhancement'}")
print("-" * 70)

for V_in in [5, 10, 15]:
    for dP in [2, 5, 10]:  # hPa = 100 Pa
        for ratio in [1.5, 2, 3]:
            V_gap, _, _ = gap_wind_speed(V_in, dP * 100, ratio)
            enhancement = V_gap / V_in
            if ratio == 2:
                print(f"{V_in:<12} {dP:<12} {ratio:<12} {V_gap:<15.1f} {enhancement:.1f}×")


# =============================================================================
# PART 7: BLOCKED FLOW AND BARRIER JETS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: BLOCKED FLOW AND BARRIER JETS")
print("=" * 70)

blocked_text = """
BLOCKED FLOW:
=============

When air can't go OVER the mountain, it goes AROUND!

FROUDE NUMBER CRITERION:

Fr = U / (N × h)

Fr < 1: Flow blocked (can't overcome stability)
Fr > 1: Flow goes over

For blocked flow (Fr < 1):
- Air piles up on windward side
- Pressure rise upstream
- Flow diverts around mountain
- Barrier jet forms parallel to terrain

BARRIER JET:

Strong wind parallel to mountain barrier

Caused by:
1. Blocked cross-barrier flow
2. Coriolis deflection
3. Pressure gradient along barrier

Speed can exceed approach flow!

V_jet ≈ U × (1/Fr) for Fr < 1

COLD AIR DAMMING (Eastern US):

- Cold air trapped against Appalachians
- Ageostrophic northeasterly flow
- Maintains cold air mass
- Delays warming in spring
- Creates freezing rain setup

COASTAL MOUNTAINS:

- Onshore flow blocked by terrain
- Convergence along coast
- Enhanced precipitation
- Marine layer effects
"""
print(blocked_text)

def blocking_criterion(U, N, h_mountain):
    """
    Determine if flow is blocked.

    Returns Froude number and blocking status.
    """
    Fr = froude_number(U, N, h_mountain)
    blocked = Fr < 1
    return Fr, blocked

def barrier_jet_speed(U_approach, Fr):
    """
    Estimate barrier jet speed for blocked flow.
    """
    if Fr >= 1:
        return U_approach  # Not blocked
    return U_approach / Fr  # Amplification for blocked flow

print("\nFlow Blocking Analysis:")
print("-" * 70)
print(f"{'U (m/s)':<10} {'N (s⁻¹)':<10} {'h (m)':<10} {'Fr':<10} {'Blocked?':<12} {'V_jet (m/s)'}")
print("-" * 70)

for U in [5, 10, 15, 20]:
    for N in [0.01, 0.015]:
        for h in [1500, 3000]:
            Fr, blocked = blocking_criterion(U, N, h)
            V_jet = barrier_jet_speed(U, Fr)
            status = "Yes" if blocked else "No"
            if N == 0.01:
                print(f"{U:<10} {N:<10} {h:<10} {Fr:<10.2f} {status:<12} {V_jet:.1f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: MOUNTAIN METEOROLOGY")
print("=" * 70)

summary = """
KEY MOUNTAIN METEOROLOGY PHYSICS:
=================================

1. OROGRAPHIC LIFTING
   - w = U × terrain_slope
   - 10× stronger than frontal lift
   - Precipitation enhancement on windward side
   - Rain shadow on leeward side

2. LEE WAVES
   - Wavelength λ = 2πU/N
   - Scorer parameter l² = N²/U²
   - Lenticular clouds mark wave crests
   - Can propagate to stratosphere

3. DOWNSLOPE WINDSTORMS
   - Hydraulic theory: water over dam analog
   - Wave breaking at critical level
   - V_max ≈ √(2 × N × h × U) → 50+ m/s possible!
   - Chinook, Foehn, Bora, Santa Ana

4. FOEHN WARMING
   - Moist ascent, dry descent
   - Net warming = (Γ_d - Γ_m) × Δz_condensation
   - Can warm 10°C+ crossing mountains
   - Rapid snowmelt, fire danger

5. DIURNAL CIRCULATIONS
   - Anabatic (upslope) by day
   - Katabatic (downslope) by night
   - Valley winds: up-valley by day, down-valley at night
   - Critical for thunderstorm initiation

6. GAP WINDS
   - Venturi effect + pressure gradient
   - Speed amplification 1.5-3×
   - Santa Ana, Mistral, Tehuantepecer

7. FLOW BLOCKING
   - Froude number Fr = U/(N×h)
   - Fr < 1: blocked, flow goes around
   - Barrier jets parallel to terrain


THE PHYSICS TELLS US:
====================
- Mountains create asymmetric precipitation (wet/dry sides)
- Stability and wind speed determine wave behavior
- Energy conversion (potential → kinetic) drives downslope winds
- Phase changes create foehn warming
- Differential heating drives local circulations
- Simple dimensionless numbers (Fr) predict behavior
"""
print(summary)

print("\n" + "=" * 70)
print("END OF MOUNTAIN METEOROLOGY")
print("=" * 70)
