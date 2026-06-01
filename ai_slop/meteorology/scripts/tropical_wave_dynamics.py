#!/usr/bin/env python3
"""
TROPICAL WAVE DYNAMICS - FIRST PRINCIPLES
==========================================

Deriving the physics of tropical waves: MJO, Kelvin waves,
equatorial Rossby waves, and African Easterly Waves.
"""

import numpy as np

print("=" * 70)
print("TROPICAL WAVE DYNAMICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81            # Gravity (m/s²)
omega = 7.29e-5     # Earth rotation rate (rad/s)
R_earth = 6.371e6   # Earth radius (m)
c_p = 1004          # Specific heat (J/kg/K)


# =============================================================================
# PART 1: EQUATORIAL DYNAMICS - THE BETA PLANE
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: EQUATORIAL DYNAMICS")
print("=" * 70)

equatorial_text = """
THE EQUATOR IS SPECIAL:
=======================

At the equator, f = 2Ω sin(0) = 0

This changes EVERYTHING about wave dynamics!

THE EQUATORIAL BETA-PLANE:
Near the equator, linearize f:
f ≈ βy where β = 2Ω/a = 2.3 × 10⁻¹¹ m⁻¹s⁻¹

y = distance from equator

THE EQUATORIAL DEFORMATION RADIUS:
L_eq = √(c/β)

Where c = gravity wave speed ≈ √(g'H) ≈ 20-50 m/s for tropics
This gives L_eq ≈ 1000-1500 km

EQUATORIAL WAVEGUIDE:
The tropics act as a waveguide - waves are trapped within
~15° latitude of equator (about 1500 km).

This is why tropical waves have such distinctive character!
"""
print(equatorial_text)

def beta_parameter_equator():
    """Calculate equatorial beta parameter."""
    return 2 * omega / R_earth

def equatorial_deformation_radius(c=30):
    """
    Calculate equatorial deformation radius.

    c: equivalent gravity wave speed (m/s)
    """
    beta = beta_parameter_equator()
    return np.sqrt(c / beta)

beta = beta_parameter_equator()
print(f"\nEquatorial β = {beta:.2e} m⁻¹s⁻¹")
print(f"\nEquatorial Deformation Radius:")
print("-" * 50)
for c in [20, 30, 40, 50]:
    L_eq = equatorial_deformation_radius(c) / 1000  # km
    print(f"c = {c} m/s: L_eq = {L_eq:.0f} km")


# =============================================================================
# PART 2: KELVIN WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: KELVIN WAVES - EASTWARD PROPAGATION")
print("=" * 70)

kelvin_text = """
KELVIN WAVES: THE EASTWARD MOVERS
=================================

Kelvin waves are special equatorial waves:
- Propagate EASTWARD only
- No meridional (N-S) velocity component
- Trapped near equator

DISPERSION RELATION:
ω = ck (non-dispersive!)

Wave speed c ≈ 15-50 m/s depending on mode

STRUCTURE:
- Maximum amplitude at equator
- Decays exponentially away from equator
- Geostrophic balance in y-direction

OCEANIC KELVIN WAVES:
- c ≈ 2-3 m/s (much slower than atmospheric)
- Take ~2 months to cross Pacific
- Critical for ENSO dynamics!

ATMOSPHERIC KELVIN WAVES:
- Convectively coupled: c ≈ 15-20 m/s
- Dry: c ≈ 40-50 m/s
- Period: days to weeks
- Modulate tropical convection
"""
print(kelvin_text)

def kelvin_wave_speed_oceanic(H_thermocline=150, g_prime=0.03):
    """
    Oceanic Kelvin wave speed.

    H: thermocline depth (m)
    g': reduced gravity (m/s²)
    """
    return np.sqrt(g_prime * H_thermocline)

def kelvin_wave_speed_atmospheric(H_tropopause=15000, T_mean=250):
    """
    Atmospheric Kelvin wave speed (dry mode).

    Equivalent depth formulation.
    """
    N = 0.01  # Brunt-Väisälä frequency
    c = N * H_tropopause / np.pi  # First baroclinic mode
    return c

def kelvin_crossing_time(basin_width_km, wave_speed_ms):
    """Time to cross basin in days."""
    distance_m = basin_width_km * 1000
    time_s = distance_m / wave_speed_ms
    return time_s / 86400

print("\nKelvin Wave Properties:")
print("-" * 60)

# Oceanic
c_ocean = kelvin_wave_speed_oceanic()
pacific_crossing = kelvin_crossing_time(15000, c_ocean)
print(f"Oceanic Kelvin wave: c = {c_ocean:.1f} m/s")
print(f"  Pacific crossing time: {pacific_crossing:.0f} days (~{pacific_crossing/30:.1f} months)")

# Atmospheric
c_atm_dry = kelvin_wave_speed_atmospheric()
c_atm_coupled = 17  # Convectively coupled
print(f"\nAtmospheric Kelvin wave (dry): c = {c_atm_dry:.0f} m/s")
print(f"Atmospheric Kelvin wave (coupled): c = {c_atm_coupled:.0f} m/s")
circumference_km = 2 * np.pi * R_earth / 1000
period_dry = kelvin_crossing_time(circumference_km, c_atm_dry)
period_coupled = kelvin_crossing_time(circumference_km, c_atm_coupled)
print(f"  Circumference crossing (dry): {period_dry:.0f} days")
print(f"  Circumference crossing (coupled): {period_coupled:.0f} days")


# =============================================================================
# PART 3: EQUATORIAL ROSSBY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: EQUATORIAL ROSSBY WAVES - WESTWARD PROPAGATION")
print("=" * 70)

rossby_text = """
EQUATORIAL ROSSBY WAVES: THE WESTWARD MOVERS
=============================================

Rossby waves at the equator:
- Propagate WESTWARD
- Much slower than Kelvin waves
- Paired circulation cells (gyres)

DISPERSION RELATION:
ω = -βk / (k² + (2n+1)β/c)

Where n = 0, 1, 2, ... is the meridional mode number

For long waves: c_rossby ≈ -c_kelvin / (2n+1)

n=1 mode: c_rossby ≈ c_kelvin / 3 (westward)

STRUCTURE:
- Two symmetric gyres straddling equator
- Maximum winds off-equator (at ±L_eq)
- Important for ENSO: reflect off western boundary

MIXED ROSSBY-GRAVITY WAVE (n=0):
- Westward for short wavelengths
- Eastward for long wavelengths
- Important in MJO dynamics
"""
print(rossby_text)

def rossby_wave_speed(kelvin_speed, n=1):
    """
    Equatorial Rossby wave phase speed.

    Long wave limit: c_R = -c_K / (2n+1)
    """
    return -kelvin_speed / (2*n + 1)

print("\nEquatorial Rossby Wave Speeds:")
print("-" * 60)
print(f"{'Mode n':<10} {'c_Rossby (m/s)':<20} {'Direction'}")
print("-" * 60)

c_k = 30  # Kelvin wave speed
for n in range(1, 6):
    c_r = rossby_wave_speed(c_k, n)
    print(f"{n:<10} {c_r:<20.1f} Westward")

# Oceanic Rossby waves
print("\n\nOceanic Rossby Waves (ENSO-relevant):")
c_ocean = 2.5
pacific_width = 15000  # km
for n in [1, 2, 3]:
    c_r = rossby_wave_speed(c_ocean, n)
    crossing_time = kelvin_crossing_time(pacific_width, abs(c_r))
    print(f"  n={n}: c = {c_r:.2f} m/s, Pacific crossing = {crossing_time:.0f} days")


# =============================================================================
# PART 4: MADDEN-JULIAN OSCILLATION (MJO)
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: MADDEN-JULIAN OSCILLATION (MJO)")
print("=" * 70)

mjo_text = """
THE MJO: DOMINANT INTRASEASONAL VARIABILITY
============================================

The MJO is the largest source of intraseasonal (30-90 day)
variability in the tropics.

OBSERVED PROPERTIES:
- Eastward propagation: ~5 m/s
- Period: 30-60 days (average ~45 days)
- Wavelength: ~12,000-20,000 km (planetary scale)
- Amplitude: Modulates convection by 50-100%

STRUCTURE:
- Large-scale envelope of enhanced convection
- Convectively coupled Kelvin wave signature
- Rossby gyres to the west of convection
- MJO = Kelvin + Rossby coupled to convection

WHY SO SLOW?
Free Kelvin waves: 30-50 m/s
MJO: 5 m/s

MOISTURE-MODE THEORY:
MJO is a "moisture wave" - propagation controlled by:
1. Gross moist stability (convection-circulation feedback)
2. Moisture advection
3. Surface flux feedbacks

IMPACTS:
1. Modulates tropical cyclone genesis (~50% of variance!)
2. Affects monsoon active/break periods
3. Triggers extratropical responses
4. MJO phase 1-2: Enhanced Pacific TC formation
   MJO phase 6-7: Enhanced Atlantic TC formation
"""
print(mjo_text)

def mjo_properties():
    """MJO characteristics."""
    speed = 5.0  # m/s
    period = 45  # days
    wavelength = speed * period * 86400 / 1000  # km

    return {
        'speed': speed,
        'period': period,
        'wavelength': wavelength,
        'circumference_time': 2 * np.pi * R_earth / (speed * 86400)  # days
    }

mjo = mjo_properties()
print(f"\nMJO Properties (from observations):")
print("-" * 50)
print(f"Propagation speed: {mjo['speed']:.1f} m/s (eastward)")
print(f"Period: {mjo['period']:.0f} days")
print(f"Wavelength: {mjo['wavelength']:.0f} km")
print(f"Time around equator: {mjo['circumference_time']:.0f} days")

print("\n\nMJO Phase and Tropical Cyclone Activity:")
print("-" * 60)
mjo_phases = [
    ("1-2", "Western Pacific", "Enhanced W Pacific TCs"),
    ("2-3", "Maritime Continent", "Suppressed Atlantic"),
    ("4-5", "Maritime Cont. exit", "Transition"),
    ("6-7", "Indian Ocean", "Enhanced Atlantic TCs"),
    ("8-1", "Africa/W Indian", "Variable"),
]
for phase, location, effect in mjo_phases:
    print(f"Phase {phase}: Convection over {location}")
    print(f"         → {effect}")


# =============================================================================
# PART 5: AFRICAN EASTERLY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: AFRICAN EASTERLY WAVES (AEWs)")
print("=" * 70)

aew_text = """
AFRICAN EASTERLY WAVES: HURRICANE SEEDS
=======================================

AEWs are the precursors to most Atlantic hurricanes (~60%).

ORIGIN: African Easterly Jet (AEJ)
- Maximum: ~15°N, 600 hPa, ~12 m/s easterly
- Baroclinic AND barotropic instability
- Grows from temperature/moisture gradients

WAVE PROPERTIES:
- Wavelength: 2000-4000 km
- Period: 3-5 days
- Phase speed: ~7-8 m/s westward
- Peak season: July-September

STRUCTURE (typical):
- Trough axis tilts NE-SW
- Low-level cyclonic vorticity
- Mid-level jet streak
- Convection near/ahead of trough

HURRICANE DEVELOPMENT:
AEW provides:
1. Low-level vorticity (rotation)
2. Organized convection
3. Reduced shear (trough axis)

Not all AEWs develop - need:
- Warm SST (>26.5°C)
- Low shear environment
- Mid-level moisture
- Distance from equator (f ≠ 0)
"""
print(aew_text)

def aew_properties():
    """African Easterly Wave characteristics."""
    return {
        'wavelength_km': 3000,
        'period_days': 4,
        'speed_ms': 7.5,
        'season': 'July-September',
        'per_season': 60,
        'develop_rate': 0.15  # 15% become named storms
    }

aew = aew_properties()
print(f"\nAEW Properties:")
print("-" * 50)
print(f"Wavelength: {aew['wavelength_km']} km")
print(f"Period: {aew['period_days']} days")
print(f"Phase speed: {aew['speed_ms']} m/s westward")
print(f"Waves per season: ~{aew['per_season']}")
print(f"Development rate: ~{aew['develop_rate']*100:.0f}% become named storms")
print(f"→ Produces ~{aew['per_season'] * aew['develop_rate']:.0f} Atlantic TCs from AEWs")

# Transit time Africa to Caribbean
distance_km = 5000  # Africa to Caribbean
transit_days = distance_km / (aew['speed_ms'] * 86.4)
print(f"\nTransit time (Africa → Caribbean): {transit_days:.0f} days")


# =============================================================================
# PART 6: CONVECTIVELY COUPLED EQUATORIAL WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: CONVECTIVELY COUPLED EQUATORIAL WAVES")
print("=" * 70)

ccew_text = """
CONVECTIVELY COUPLED EQUATORIAL WAVES (CCEWs):
=============================================

When equatorial waves interact with convection, they slow down
and modify tropical rainfall patterns.

WHEELER-KILADIS DIAGRAM:
Spectral analysis reveals distinct wave types:

1. KELVIN WAVES
   - Eastward, c ≈ 15-17 m/s (coupled)
   - Dry mode: c ≈ 40-50 m/s
   - Period: 2.5-20 days

2. EQUATORIAL ROSSBY (ER) WAVES
   - Westward, c ≈ 5-7 m/s
   - n=1 mode dominant
   - Period: 10-40 days

3. MIXED ROSSBY-GRAVITY (MRG)
   - Westward for short λ, period 3-6 days
   - Also called "Yanai wave"

4. INERTIO-GRAVITY (IG) WAVES
   - Both directions
   - High frequency, period < 3 days

5. TROPICAL DEPRESSION (TD) TYPE
   - Westward, period 3-5 days
   - Includes AEWs

WHY COUPLING SLOWS WAVES:
Convective heating provides positive feedback but
introduces phase lag → reduced effective phase speed.

"Gross moist stability" determines how much convection
opposes vs amplifies wave motion.
"""
print(ccew_text)

print("\nConvectively Coupled Wave Summary:")
print("-" * 70)
print(f"{'Wave Type':<25} {'Direction':<12} {'Speed (m/s)':<15} {'Period (days)'}")
print("-" * 70)

ccew_types = [
    ("Kelvin (dry)", "East", 45, "3-10"),
    ("Kelvin (coupled)", "East", 16, "2.5-20"),
    ("MJO", "East", 5, "30-60"),
    ("Eq. Rossby n=1", "West", 6, "10-40"),
    ("Mixed Rossby-Gravity", "West", 8, "3-6"),
    ("TD-type / AEW", "West", 7, "3-5"),
]

for wave, direction, speed, period in ccew_types:
    print(f"{wave:<25} {direction:<12} {speed:<15} {period}")


# =============================================================================
# PART 7: ENSO AND WAVE DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: ENSO - WAVES IN ACTION")
print("=" * 70)

enso_waves_text = """
ENSO: COUPLED OCEAN-ATMOSPHERE WAVE DYNAMICS
=============================================

ENSO involves oceanic Kelvin and Rossby waves!

EL NIÑO DEVELOPMENT:
1. Weakening trade winds
2. Eastward-propagating oceanic Kelvin wave
3. Deepens thermocline in eastern Pacific
4. Warm water surfaces → El Niño

KELVIN WAVE ROLE:
- Oceanic Kelvin wave: c ≈ 2-3 m/s
- Crosses Pacific in ~2 months
- Deepens thermocline as it passes

ROSSBY WAVE ROLE:
- Oceanic Rossby wave: c ≈ 0.5-1 m/s (westward)
- Reflects off western boundary → Kelvin wave
- Takes 6-12 months to cross Pacific
- This sets the ~2-7 year ENSO period!

RECHARGE OSCILLATOR THEORY (Jin 1997):
1. El Niño depletes warm water (pycnocline shoals)
2. Rossby waves carry signal westward
3. Reflect as upwelling Kelvin wave
4. Thermocline shoals in east → La Niña
5. Process reverses

The period is set by wave transit times!
"""
print(enso_waves_text)

def enso_wave_timescales():
    """Calculate ENSO-relevant wave timescales."""
    pacific_km = 15000  # km

    c_kelvin = 2.5  # m/s
    c_rossby_1 = c_kelvin / 3  # First mode

    t_kelvin = pacific_km * 1000 / (c_kelvin * 86400)  # days
    t_rossby = pacific_km * 1000 / (c_rossby_1 * 86400)  # days

    return {
        'kelvin_crossing': t_kelvin,
        'rossby_crossing': t_rossby,
        'total_cycle': (t_kelvin + t_rossby) / 365 * 2  # Rough period
    }

timescales = enso_wave_timescales()
print(f"\nENSO Wave Timescales:")
print("-" * 50)
print(f"Kelvin wave (east): {timescales['kelvin_crossing']:.0f} days (~{timescales['kelvin_crossing']/30:.1f} months)")
print(f"Rossby wave (west): {timescales['rossby_crossing']:.0f} days (~{timescales['rossby_crossing']/30:.0f} months)")
print(f"Implied ENSO period: ~{timescales['total_cycle']:.1f} years")
print(f"(Observed: 2-7 years, average ~4 years)")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: TROPICAL WAVE DYNAMICS")
print("=" * 70)

summary = """
KEY TROPICAL WAVE PHYSICS:
=========================

1. EQUATORIAL BETA-PLANE
   - f ≈ βy near equator (β = 2Ω/a)
   - Equatorial waveguide traps waves within ~15°
   - Deformation radius L_eq = √(c/β) ~ 1000 km

2. KELVIN WAVES
   - Eastward only, no meridional motion
   - Non-dispersive: ω = ck
   - Ocean: ~2 m/s (ENSO dynamics)
   - Atmosphere: 15-50 m/s

3. EQUATORIAL ROSSBY WAVES
   - Westward, slower than Kelvin
   - c_R = -c_K / (2n+1) for mode n
   - Critical for ENSO termination

4. MADDEN-JULIAN OSCILLATION
   - 30-60 day period, ~5 m/s eastward
   - Coupled Kelvin-Rossby-convection
   - Modulates TC activity by ~50%

5. AFRICAN EASTERLY WAVES
   - Seed ~60% of Atlantic hurricanes
   - Period 3-5 days, ~8 m/s westward
   - From instability of African Easterly Jet

6. CONVECTIVE COUPLING
   - Slows all wave types
   - Creates coherent rainfall patterns
   - Wheeler-Kiladis diagram shows spectral peaks

7. ENSO AS WAVE PROBLEM
   - Kelvin + Rossby wave reflection
   - Wave transit times set ENSO period
   - ~2-7 years from ocean wave dynamics


THE PHYSICS TELLS US:
=====================
Tropical waves are fundamental to:
- Day-to-day tropical weather
- Hurricane genesis and activity
- Seasonal monsoon variability
- Interannual (ENSO) climate
- Global teleconnections

All from shallow-water equations on rotating sphere!
"""
print(summary)

print("\n" + "=" * 70)
print("END OF TROPICAL WAVE DYNAMICS")
print("=" * 70)
