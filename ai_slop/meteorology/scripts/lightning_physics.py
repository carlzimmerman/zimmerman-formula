#!/usr/bin/env python3
"""
LIGHTNING PHYSICS - FIRST PRINCIPLES
=====================================

Deriving the physics of electrical charge separation,
lightning formation, and thunder from electrostatics.
"""

import numpy as np

print("=" * 70)
print("LIGHTNING PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
epsilon_0 = 8.854e-12   # Vacuum permittivity (F/m)
k_e = 8.99e9            # Coulomb constant (N·m²/C²)
e_charge = 1.6e-19      # Electron charge (C)
c_sound = 343           # Speed of sound (m/s at 20°C)
c_light = 3e8           # Speed of light (m/s)


# =============================================================================
# PART 1: ELECTRIFICATION OF THUNDERSTORMS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: CHARGE SEPARATION IN THUNDERSTORMS")
print("=" * 70)

electrification_text = """
HOW THUNDERSTORMS BECOME ELECTRIFIED:
=====================================

The atmosphere is normally a poor conductor, but
thunderstorms generate HUGE charge separations.

CHARGE STRUCTURE (typical):
┌─────────────────────────────┐
│  + + + + + + + + +   (Upper positive, ~10km)
│      ↑
│  Ice crystals rise
│      ↑
│  - - - - - - - - - -   (Main negative, ~6km)
│      ↓
│  Graupel/hail fall
│      ↓
│  + + + +   (Lower positive, ~3km)
│
└─────────────────────────────┘
     GROUND (induced positive)

CHARGE SEPARATION MECHANISM (Non-Inductive):
1. Ice crystals and graupel collide in mixed-phase region
2. At T ≈ -15°C, charge transfers during collision
3. Small ice crystals → positive (rise with updraft)
4. Large graupel → negative (fall with gravity)
5. Separation creates electric field

This requires:
- Strong updraft (>10 m/s)
- Mixed-phase region (-10 to -25°C)
- Coexistence of ice + supercooled water

CHARGE MAGNITUDES:
Typical thunderstorm: 20-100 Coulombs separated
Large supercell: Up to 300 Coulombs
"""
print(electrification_text)

def charge_separation_rate(updraft_speed, ice_crystal_conc):
    """
    Estimate charge separation rate in C/s.

    Simplified model based on collision charging.
    """
    # Each collision transfers ~10 fC
    charge_per_collision = 10e-15  # C

    # Collision rate proportional to updraft and concentration
    collision_rate = updraft_speed * ice_crystal_conc * 1000  # collisions/m³/s

    # Volume of charging region (simplified)
    volume = 1e9  # 1 km³

    rate = charge_per_collision * collision_rate * volume * 0.01  # Efficiency
    return rate

print("\nCharge Separation Rate:")
print("-" * 60)
print(f"{'Updraft (m/s)':<15} {'Ice conc (/L)':<15} {'Rate (C/s)':<15}")
print("-" * 60)

for updraft in [10, 20, 30, 50]:
    for ice_conc in [10, 50, 100]:
        rate = charge_separation_rate(updraft, ice_conc)
        print(f"{updraft:<15} {ice_conc:<15} {rate:<15.2f}")


# =============================================================================
# PART 2: ELECTRIC FIELDS AND BREAKDOWN
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: ELECTRIC FIELD AND DIELECTRIC BREAKDOWN")
print("=" * 70)

breakdown_text = """
ELECTRIC FIELD IN THUNDERSTORMS:
================================

Fair-weather field: ~100 V/m (downward)
Thunderstorm field: 10,000-100,000 V/m

DIELECTRIC BREAKDOWN:
Air becomes conducting when E > E_breakdown

At sea level: E_b ≈ 3 MV/m = 3,000,000 V/m
At 6 km altitude: E_b ≈ 1 MV/m (lower pressure)

BUT: Lightning initiates at only 100-400 kV/m!

THE MYSTERY: How does breakdown occur at 1/10 the expected field?

ANSWER: STEPPED LEADER
- Corona discharge from ice crystals
- Localized field enhancement
- "Runaway breakdown" from cosmic ray secondaries
- Propagating ionization front

POTENTIAL DIFFERENCE:
Between cloud base and ground: 100-500 Million Volts!

This is why lightning is so powerful.
"""
print(breakdown_text)

def electric_field(charge, distance):
    """Calculate electric field from point charge."""
    return k_e * abs(charge) / distance**2

def breakdown_field(altitude_km):
    """
    Dielectric breakdown field vs altitude.

    Decreases with pressure (lower air density).
    """
    p_0 = 101325  # Sea level pressure (Pa)
    p = p_0 * np.exp(-altitude_km / 8.5)
    E_b = 3e6 * (p / p_0)**0.9  # V/m
    return E_b

def potential_difference(charge, d_cloud_ground):
    """Potential difference between cloud and ground."""
    return k_e * charge / d_cloud_ground

print("\nBreakdown Field vs Altitude:")
print("-" * 50)
print(f"{'Altitude (km)':<15} {'E_breakdown (kV/m)':<25}")
print("-" * 50)

for alt in [0, 2, 4, 6, 8, 10]:
    E_b = breakdown_field(alt)
    print(f"{alt:<15} {E_b/1000:<25.0f}")

print("\n\nPotential Difference Examples:")
print("-" * 60)
for Q in [20, 50, 100, 200]:  # Coulombs
    for d in [2000, 3000, 5000]:  # meters
        V = potential_difference(Q, d)
        print(f"Q = {Q} C, d = {d}m: ΔV = {V/1e6:.0f} MV")


# =============================================================================
# PART 3: LIGHTNING DISCHARGE PROCESS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: LIGHTNING DISCHARGE SEQUENCE")
print("=" * 70)

discharge_text = """
LIGHTNING DISCHARGE STAGES:
===========================

1. STEPPED LEADER (1 ms)
   - Invisible ionized channel extends from cloud
   - Steps of ~50m in ~1 μs
   - Speed: ~200 km/s (slow!)
   - Current: ~100-1000 A
   - Creates conducting path toward ground

2. ATTACHMENT / RETURN STROKE (30 μs)
   - Upward leader rises from ground object
   - Connection at ~50m height
   - RETURN STROKE propagates upward
   - Speed: ~100,000 km/s (1/3 speed of light!)
   - Peak current: 30,000 A (typical), up to 300,000 A
   - This is the visible flash!

3. CONTINUING CURRENT (1-100 ms)
   - Lower current (~100 A) flows
   - Drains cloud charge
   - Can cause fires (long duration)

4. SUBSEQUENT STROKES (optional)
   - Dart leader (no steps) follows channel
   - Additional return strokes
   - 3-5 strokes typical, up to 20+
   - Causes "flickering" appearance

ENERGY:
Single stroke: ~1 billion joules (1 GJ)
But most dissipates as heat, light, sound
Only ~5% into electromagnetic radiation
"""
print(discharge_text)

def return_stroke_energy(current_peak, duration_us, channel_length):
    """
    Estimate return stroke energy.

    E ≈ ∫ I²R dt

    Simplified: E ~ I_peak² × R × t
    """
    R_per_m = 1.0  # Ohm/m for ionized channel
    R_total = R_per_m * channel_length

    # Current varies, use average ~ I_peak/3
    I_avg = current_peak / 3
    t = duration_us * 1e-6

    energy = I_avg**2 * R_total * t * 1000  # Factor for pulse shape
    return energy

print("\nReturn Stroke Properties:")
print("-" * 70)
print(f"{'I_peak (kA)':<15} {'Duration (μs)':<15} {'Channel (m)':<15} {'Energy (MJ)':<15}")
print("-" * 70)

for I in [20, 50, 100, 200]:  # kA
    for dur in [20, 50, 100]:  # μs
        E = return_stroke_energy(I * 1000, dur, 5000)
        print(f"{I:<15} {dur:<15} {5000:<15} {E/1e6:<15.1f}")


# =============================================================================
# PART 4: THUNDER
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: THUNDER PHYSICS")
print("=" * 70)

thunder_text = """
HOW THUNDER IS PRODUCED:
========================

Lightning heats air to ~30,000 K in microseconds!
(5× hotter than Sun's surface)

This extreme heating:
1. Causes explosive expansion
2. Creates shock wave (thunder)
3. Expands channel from mm to cm in μs

SHOCK WAVE ENERGY:
~1% of lightning energy goes into acoustic waves

THUNDER CHARACTERISTICS:

1. SOUND SPEED:
   c = 343 m/s at 20°C (about 0.3 km/s)

2. FLASH-TO-BANG:
   Time delay = distance / c
   3 seconds ≈ 1 km distance
   "5 seconds per mile" rule

3. WHY THUNDER RUMBLES:
   - Lightning channel is long (3-10 km)
   - Sound from different parts arrives at different times
   - Plus reflections from clouds, ground, buildings

4. MAXIMUM AUDIBLE DISTANCE:
   ~25 km (sound attenuates, refracts upward)
   "Heat lightning" = too far for thunder

PEAK OVERPRESSURE:
Near channel: ~5 atmospheres!
At 10 m: ~0.5 atm (can cause damage)
At 100 m: ~0.01 atm (loud bang)
At 1 km: ~0.0001 atm (deep rumble)
"""
print(thunder_text)

def flash_to_bang(distance_km, temperature_C=20):
    """Calculate time from flash to thunder."""
    c = 331 + 0.6 * temperature_C  # Temperature-dependent sound speed
    return distance_km * 1000 / c

def thunder_duration(channel_length_km, viewing_angle_deg=45):
    """
    Estimate thunder duration from channel geometry.

    Longer channel + oblique view = longer rumble
    """
    # Projected length difference
    proj_diff = channel_length_km * np.sin(np.radians(viewing_angle_deg))
    return flash_to_bang(proj_diff)

print("\nFlash-to-Bang Times:")
print("-" * 50)
print(f"{'Distance (km)':<15} {'Time (s)':<15} {'Rule of thumb'}")
print("-" * 50)

for d in [0.3, 1, 2, 3, 5, 8, 10, 15, 20]:
    t = flash_to_bang(d)
    rule = f"~{d:.0f} km" if d >= 1 else f"~{d*1000:.0f} m"
    print(f"{d:<15.1f} {t:<15.1f} {rule}")

print("\n\nThunder Duration vs Channel Length:")
print("-" * 50)
for length in [3, 5, 8, 10]:
    dur = thunder_duration(length)
    print(f"{length} km channel → {dur:.1f} s rumble duration")


# =============================================================================
# PART 5: LIGHTNING TYPES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: LIGHTNING TYPES")
print("=" * 70)

types_text = """
LIGHTNING CLASSIFICATION:
=========================

BY POLARITY:
1. NEGATIVE CG (-CG): 90% of cloud-to-ground
   - Transfers negative charge to ground
   - From main negative charge region
   - Typical peak current: 30 kA

2. POSITIVE CG (+CG): 10% of CG
   - Transfers positive charge to ground
   - Often from upper positive or anvil
   - Peak current: 200-300 kA (stronger!)
   - Single stroke, long continuing current
   - More dangerous, starts more fires

BY LOCATION:
1. CLOUD-TO-GROUND (CG): 20-25%
   - What we usually think of as lightning
   - Strikes objects on ground

2. INTRA-CLOUD (IC): 75-80%
   - Within single cloud
   - Most common type!
   - "Sheet lightning"

3. CLOUD-TO-CLOUD (CC): Rare
   - Between separate clouds

4. CLOUD-TO-AIR (CA)
   - Into clear air from cloud edge

SPECIAL TYPES:
- SPRITES: Above thunderstorms, red, brief
- JETS: Blue jets upward from cloud tops
- ELVES: Expanding rings at ionosphere
- BALL LIGHTNING: Mysterious, rare, disputed
"""
print(types_text)

print("\nLightning Type Characteristics:")
print("-" * 70)
print(f"{'Type':<20} {'% of total':<15} {'Peak I (kA)':<15} {'Flash/min':<15}")
print("-" * 70)

types = [
    ("-CG", 20, 30, 2),
    ("+CG", 3, 200, 0.3),
    ("IC/CC", 77, 20, 10),
]

for ltype, pct, current, rate in types:
    print(f"{ltype:<20} {pct:<15} {current:<15} {rate:<15.1f}")


# =============================================================================
# PART 6: LIGHTNING CLIMATOLOGY
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: GLOBAL LIGHTNING DISTRIBUTION")
print("=" * 70)

climate_text = """
GLOBAL LIGHTNING DISTRIBUTION:
==============================

TOTAL: ~45 flashes per second globally
       ~1.4 billion flashes per year

HOTSPOTS (flashes/km²/year):
1. Lake Maracaibo, Venezuela: ~250 (world record!)
   - Converging winds, warm water, mountain barrier
2. Democratic Republic of Congo: ~150
3. Central America
4. Florida, USA: ~15 (US hotspot)
5. Himalayan foothills

WHY TROPICS DOMINATE:
- Warm, moist air → high CAPE
- Frequent deep convection
- Diurnal cycle over land

SEASONAL PATTERNS:
- Summer maximum in each hemisphere
- Follows solar heating
- Land has 10× more lightning than ocean

OCEAN vs LAND:
- Ocean: ~0.1 flash/km²/year
- Land: ~5 flash/km²/year (50× more!)

Why? Land heats more → stronger updrafts → deeper clouds
"""
print(climate_text)

print("\nLightning Flash Rates by Region:")
print("-" * 60)
print(f"{'Region':<30} {'Flash density (km⁻²/yr)':<25}")
print("-" * 60)

regions = [
    ("Lake Maracaibo, Venezuela", 250),
    ("Central Africa (Congo)", 150),
    ("Southeast Asia", 40),
    ("Florida, USA", 15),
    ("Central USA (Plains)", 8),
    ("Northern Europe", 2),
    ("Tropical ocean", 0.5),
    ("Arctic", 0.01),
]

for region, density in regions:
    print(f"{region:<30} {density:<25}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: LIGHTNING PHYSICS")
print("=" * 70)

summary = """
KEY LIGHTNING PHYSICS:
=====================

1. CHARGE SEPARATION
   - Non-inductive ice-graupel collisions
   - Requires T ≈ -15°C, mixed phase
   - Upper +, main -, lower + structure

2. ELECTRIC FIELD
   - Cloud-ground potential: 100-500 MV
   - Breakdown field decreases with altitude
   - Initiates at ~100-400 kV/m

3. DISCHARGE SEQUENCE
   - Stepped leader: slow, invisible
   - Return stroke: fast (c/3), bright
   - Peak current: 30 kA (-CG), 200+ kA (+CG)
   - Energy: ~1 GJ per stroke

4. THUNDER
   - From 30,000 K explosive heating
   - 3 seconds per km delay
   - Rumbles due to extended channel
   - Audible to ~25 km

5. TYPES
   - 90% negative CG
   - 10% positive CG (more dangerous)
   - 75% intra-cloud

6. CLIMATOLOGY
   - 45 flashes/second globally
   - Land >> ocean (50×)
   - Tropics dominate
   - Lake Maracaibo: world record


THE PHYSICS TELLS US:
=====================
- Lightning requires vigorous convection + ice
- Charge separation is a collisional process
- Breakdown occurs via stepped leader
- Energy comes from gravitational separation of charged particles
- Climate change may affect lightning (more moisture, warmer)
"""
print(summary)

print("\n" + "=" * 70)
print("END OF LIGHTNING PHYSICS")
print("=" * 70)
