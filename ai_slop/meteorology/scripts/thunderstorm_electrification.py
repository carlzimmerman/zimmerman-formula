#!/usr/bin/env python3
"""
Thunderstorm Electrification and Lightning Physics
====================================================

First-principles derivations of charge separation and lightning.

Key phenomena:
- Charge separation mechanisms (graupel-ice)
- Electric field development
- Lightning initiation and propagation
- Thunder acoustics
- Global electric circuit

Starting from electrostatics and plasma physics.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
epsilon_0 = 8.854e-12    # Permittivity of free space [F/m]
e_charge = 1.602e-19     # Elementary charge [C]
k_B = 1.381e-23          # Boltzmann constant [J/K]
c_sound = 343            # Speed of sound [m/s]
rho_air = 1.0            # Air density [kg/m³]

print("="*70)
print("THUNDERSTORM ELECTRIFICATION AND LIGHTNING PHYSICS")
print("="*70)

#############################################
# PART 1: CHARGE SEPARATION MECHANISMS
#############################################
print("\n" + "="*70)
print("PART 1: CHARGE SEPARATION IN THUNDERSTORMS")
print("="*70)

print("""
NON-INDUCTIVE CHARGING MECHANISM:
================================

The dominant charge separation occurs during collisions between:
- Graupel (soft hail, falling)
- Ice crystals (small, rising in updraft)

TAKAHASHI/SAUNDERS MECHANISM:
The sign of charge transferred depends on:
1. Temperature
2. Liquid water content (LWC)

REVERSAL TEMPERATURE: T_r ≈ -10 to -20°C

Above T_r (warmer, more LWC):
    Graupel charges POSITIVE
    Ice crystals charge NEGATIVE

Below T_r (colder, less LWC):
    Graupel charges NEGATIVE
    Ice crystals charge POSITIVE

TYPICAL THUNDERSTORM STRUCTURE:
    Upper positive charge: +40 C at ~10 km
    Main negative charge: -40 C at ~6 km
    Lower positive charge: +10 C at ~2 km (warm rain)

CHARGING RATE:
    dQ/dt = n × A × v × q_collision

Where:
    n = number density of ice particles
    A = collision cross-section
    v = relative velocity
    q_collision = charge per collision (~10-100 fC)
""")

def charge_per_collision(T_C, LWC_gm3, diameter_mm=5):
    """
    Estimate charge transferred per graupel-ice collision.

    Based on Takahashi (1978) and Saunders et al. (1991).
    Returns charge in femtocoulombs (fC).
    """
    # Reversal temperature depends on LWC
    T_reversal = -10 - 5 * LWC_gm3  # Approximate

    # Magnitude increases with size and LWC
    q_magnitude = 10 * diameter_mm * (1 + LWC_gm3)  # fC

    # Sign depends on temperature relative to reversal
    if T_C > T_reversal:
        # Graupel charges positive
        return q_magnitude
    else:
        # Graupel charges negative
        return -q_magnitude

def charging_rate(n_ice, v_fall, q_per_collision, collection_eff=0.5):
    """
    Calculate charging rate.

    dQ/dt = n × σ × v × q × E_coll

    Returns C/m³/s
    """
    # Collision cross-section (assume 5mm graupel, 100μm crystals)
    sigma = np.pi * (2.5e-3)**2  # m²

    rate = n_ice * sigma * v_fall * q_per_collision * 1e-15 * collection_eff
    return rate  # C/m³/s

print("\nCharge transfer vs temperature and LWC:")
print("-" * 60)
print(f"{'T (°C)':>8s}  {'LWC=0.5':>12s}  {'LWC=1.0':>12s}  {'LWC=2.0':>12s}")
print("-" * 60)
for T in range(-30, 5, 5):
    q1 = charge_per_collision(T, 0.5)
    q2 = charge_per_collision(T, 1.0)
    q3 = charge_per_collision(T, 2.0)
    print(f"{T:>8.0f}  {q1:>+12.1f} fC  {q2:>+12.1f} fC  {q3:>+12.1f} fC")

print("\n  Positive = graupel gains positive charge")
print("  Note: Reversal temperature shifts with LWC")

#############################################
# PART 2: ELECTRIC FIELD DEVELOPMENT
#############################################
print("\n" + "="*70)
print("PART 2: ELECTRIC FIELD IN THUNDERSTORMS")
print("="*70)

print("""
ELECTRIC FIELD FROM CHARGE DISTRIBUTION:
=======================================

For a dipole (simplified storm):
    E_z = (1/4πε₀) × [2Q/z³] (on axis, far from charges)

More accurately, for charge layer of density ρ_q:
    dE/dz = ρ_q / ε₀

TYPICAL THUNDERSTORM FIELDS:
    Fair weather: ~100 V/m (downward)
    Under storm: 1-10 kV/m
    Inside storm: 100-400 kV/m
    Just before lightning: ~500 kV/m

BREAKDOWN THRESHOLD:
At sea level: E_breakdown ≈ 3 MV/m
At 6 km altitude: E_breakdown ≈ 1 MV/m (lower pressure)

E_breakdown(z) = E_0 × (p/p_0) ≈ E_0 × exp(-z/H)

MAXIMUM POTENTIAL:
    V = ∫ E dz

For storm with -40 C at 6 km, +40 C at 10 km:
    ΔV ≈ 100-500 MV between main charges
""")

def electric_field_dipole(Q, d, z):
    """
    Electric field from charge dipole.

    Q: charge magnitude [C]
    d: separation [m]
    z: distance from center [m]

    Returns E in V/m
    """
    k = 1 / (4 * np.pi * epsilon_0)  # Coulomb constant

    # Dipole field on axis
    E = k * 2 * Q * d / z**3
    return E

def breakdown_field(altitude_m):
    """
    Dielectric breakdown field at altitude.

    Decreases with pressure (altitude).
    """
    E_0 = 3e6  # V/m at sea level
    H = 8500   # Scale height [m]

    return E_0 * np.exp(-altitude_m / H)

def charge_layer_field(sigma_Cm2, z_layer, z_obs):
    """
    Electric field from infinite charged layer.

    E = σ / (2ε₀)  (constant above/below layer)
    """
    E = sigma_Cm2 / (2 * epsilon_0)
    if z_obs > z_layer:
        return E  # Upward
    else:
        return -E  # Downward

print("\nBreakdown field vs altitude:")
print("-" * 40)
for z in [0, 2000, 4000, 6000, 8000, 10000]:
    E_b = breakdown_field(z)
    print(f"  z = {z/1000:.0f} km: E_break = {E_b/1e6:.2f} MV/m")

print("\nElectric field from thunderstorm dipole (40 C, 4 km separation):")
print("-" * 50)
Q = 40  # Coulombs
d = 4000  # meters
for z in [5000, 6000, 8000, 10000, 15000, 20000]:
    E = electric_field_dipole(Q, d, z)
    print(f"  z = {z/1000:.0f} km: E = {E/1000:.1f} kV/m")

#############################################
# PART 3: LIGHTNING INITIATION
#############################################
print("\n" + "="*70)
print("PART 3: LIGHTNING INITIATION AND PROPAGATION")
print("="*70)

print("""
LIGHTNING INITIATION MYSTERY:
============================

Problem: Observed E fields (100-400 kV/m) are well below
breakdown threshold (~1 MV/m at altitude).

PROPOSED MECHANISMS:

1. RUNAWAY BREAKDOWN (cosmic ray initiated):
   High-energy cosmic ray creates ionization trail
   Electrons accelerate, create avalanche
   Threshold: ~100-200 kV/m (much lower!)

2. HYDROMETEOR-INITIATED:
   Ice crystals/water drops enhance local E
   Corona discharge at particle tips
   Streamers can bridge gaps

3. POSITIVE STREAMERS:
   Propagate from positive charge regions
   Speed: ~10⁵ m/s
   Connect to form leader channel

STEPPED LEADER:
Once initiated, lightning propagates as stepped leader:
    Speed: ~10⁵ - 10⁶ m/s
    Step length: 10-100 m
    Pause: 10-100 μs between steps
    Channel diameter: ~1-10 cm
    Current: 100-1000 A

RETURN STROKE:
When leader connects to ground:
    Speed: 1-2 × 10⁸ m/s (1/3 speed of light!)
    Peak current: 20-200 kA (median ~30 kA)
    Duration: ~100 μs
    Temperature: ~30,000 K (5× Sun's surface)
    Energy: ~1 GJ dissipated
""")

def leader_speed(E_field_kVm, temperature_K=250):
    """
    Estimate stepped leader propagation speed.

    v ∝ E² approximately
    """
    # Empirical: v ~ 10⁵ m/s at E ~ 100 kV/m
    v_ref = 1e5  # m/s
    E_ref = 100  # kV/m

    return v_ref * (E_field_kVm / E_ref)**2

def return_stroke_current(charge_C, channel_length_m):
    """
    Estimate peak return stroke current.

    I_peak ≈ Q × v / L
    """
    v_return = 1e8  # m/s
    # This is very simplified
    tau = channel_length_m / v_return
    I_peak = charge_C / tau
    return I_peak

def lightning_energy(I_peak, duration_s=100e-6, resistance=1):
    """
    Estimate energy dissipated in lightning channel.

    W = ∫ I²R dt ≈ I² R τ
    """
    # Effective resistance of channel ~1 Ω/m × 5000 m
    return I_peak**2 * resistance * duration_s

print("\nLightning characteristics:")
print("-" * 50)

# Stepped leader
print("Stepped Leader:")
for E in [100, 200, 300, 400]:
    v = leader_speed(E)
    print(f"  E = {E} kV/m: v = {v/1e5:.1f} × 10⁵ m/s")

# Return stroke
print("\nReturn Stroke:")
print(f"  Speed: ~1-2 × 10⁸ m/s (0.3-0.7 c)")
print(f"  Peak current: 20-200 kA")
print(f"  Temperature: ~30,000 K")
print(f"  Duration: ~100 μs")

# Energy
I_peak = 30e3  # 30 kA typical
R_channel = 5000  # 5 km channel, ~1 Ω/m effective
W = lightning_energy(I_peak, 100e-6, R_channel)
print(f"\nEnergy dissipated (30 kA, 5 km channel):")
print(f"  W ≈ {W/1e9:.1f} GJ = {W/3.6e6:.0f} kWh")

#############################################
# PART 4: THUNDER PHYSICS
#############################################
print("\n" + "="*70)
print("PART 4: THUNDER ACOUSTICS")
print("="*70)

print("""
THUNDER GENERATION:
==================

Lightning channel heats air to ~30,000 K in microseconds.

RAPID HEATING → SHOCK WAVE:
    Initial overpressure: ΔP ~ 10-100 atm
    Shock front expands at supersonic speed
    Transitions to acoustic wave at ~10 m radius

THUNDER CHARACTERISTICS:
    Frequency: 10-200 Hz (low rumble)
    Intensity at 1 km: ~120 dB
    Decay: ~10 dB per doubling of distance

WHY THUNDER RUMBLES:
1. Different parts of channel at different distances
2. Sound arrives over extended time
3. Reflections from terrain/clouds
4. Channel tortuosity

FLASH-TO-BANG:
    Distance (km) ≈ Δt (seconds) / 3

More precisely: d = c_sound × Δt
    c_sound ≈ 343 m/s at 20°C
    d (km) = Δt (s) × 0.343

AUDIBILITY LIMIT:
Thunder typically heard up to ~15-25 km.
Beyond that: "heat lightning" (visible, no thunder).
""")

def flash_to_bang_distance(delta_t_seconds, T_C=20):
    """
    Calculate distance from flash-to-bang time.

    c = 331 + 0.6×T [m/s]
    """
    c = 331 + 0.6 * T_C  # Speed of sound
    return c * delta_t_seconds / 1000  # km

def thunder_intensity(distance_m, source_dB=170):
    """
    Estimate thunder intensity at distance.

    Geometric spreading: -20 log₁₀(r)
    Absorption: ~0.01 dB/m at low frequencies
    """
    # Geometric spreading
    r_ref = 1  # Reference distance 1 m
    spreading_loss = 20 * np.log10(distance_m / r_ref)

    # Atmospheric absorption (low frequency, ~0.001 dB/m)
    absorption_loss = 0.001 * distance_m

    return source_dB - spreading_loss - absorption_loss

def thunder_duration(channel_length_m, distance_m):
    """
    Estimate thunder rumble duration.

    Duration ~ difference in arrival times from
    near and far ends of channel.
    """
    c = 343  # m/s

    # Simplified: assume channel is vertical
    # Near end at distance d, far end at √(d² + L²)
    d_near = distance_m
    d_far = np.sqrt(distance_m**2 + channel_length_m**2)

    t_near = d_near / c
    t_far = d_far / c

    return t_far - t_near

print("\nFlash-to-bang distance calculation:")
print("-" * 40)
for dt in [1, 3, 5, 10, 15, 20, 30]:
    d = flash_to_bang_distance(dt)
    print(f"  Δt = {dt:2.0f} s: Distance = {d:.1f} km")

print("\nThunder intensity vs distance:")
print("-" * 40)
for d in [100, 500, 1000, 2000, 5000, 10000]:
    I = thunder_intensity(d)
    level = "Painful" if I > 120 else "Very loud" if I > 100 else \
            "Loud" if I > 80 else "Moderate" if I > 60 else "Faint"
    print(f"  d = {d/1000:.1f} km: {I:.0f} dB ({level})")

print("\nThunder duration (5 km channel):")
print("-" * 40)
for d in [1000, 2000, 5000, 10000]:
    dur = thunder_duration(5000, d)
    print(f"  d = {d/1000:.0f} km: Duration = {dur:.1f} s")

#############################################
# PART 5: LIGHTNING TYPES
#############################################
print("\n" + "="*70)
print("PART 5: TYPES OF LIGHTNING")
print("="*70)

print("""
LIGHTNING CLASSIFICATION:
========================

1. CLOUD-TO-GROUND (CG):
   - Negative CG (90%): Brings negative charge to ground
   - Positive CG (10%): From upper positive, more powerful

   Negative CG: ~30 kA peak, 5 C transferred
   Positive CG: ~100+ kA peak, 20+ C transferred

2. INTRACLOUD (IC):
   Most common type (75% of all lightning)
   Between positive and negative regions

3. CLOUD-TO-CLOUD (CC):
   Between different storms

4. CLOUD-TO-AIR (CA):
   Branches into clear air from cloud top

5. UPWARD LIGHTNING:
   From tall structures (towers, mountains)
   Often triggered by approaching storm

SPECIAL TYPES:

SPRITES: Red luminous discharge above storm
    Altitude: 40-90 km
    Duration: 1-10 ms
    Triggered by +CG strokes

BLUE JETS: Blue cones above storm
    Altitude: 15-40 km
    Speed: ~100 km/s upward

ELVES: Expanding rings at ~90 km
    Caused by electromagnetic pulse from stroke
    Duration: <1 ms
""")

def flash_rate_estimate(updraft_volume_km3, updraft_speed_ms):
    """
    Estimate flash rate from updraft characteristics.

    Empirical: Flash rate ∝ (updraft volume × speed)^~2
    """
    # Very rough approximation
    # Based on: more ice flux → more charging
    ice_flux_proxy = updraft_volume_km3 * updraft_speed_ms / 10

    # Flash rate in flashes per minute
    return 0.5 * ice_flux_proxy**1.5

def positive_cg_fraction(shear_ms, cape_Jkg):
    """
    Estimate fraction of +CG lightning.

    Higher shear, lower CAPE → more tilted storms → more +CG
    """
    # Empirical relationship
    # Strong shear exposes upper positive charge
    base_fraction = 0.05
    shear_factor = 1 + shear_ms / 30

    return min(base_fraction * shear_factor, 0.5)

print("\nTypical lightning characteristics by type:")
print("-" * 60)
types = [
    ("-CG", "30 kA", "5 C", "Common (25% of total)"),
    ("+CG", "100+ kA", "20+ C", "Rare (2-3%), dangerous"),
    ("IC", "10-20 kA", "1-2 C", "Most common (75%)"),
    ("Sprite", "N/A", "N/A", "Mesosphere, red glow"),
    ("Blue jet", "N/A", "N/A", "Stratosphere, blue cone"),
]

print(f"{'Type':>8s}  {'Peak I':>10s}  {'Charge':>8s}  {'Notes':>30s}")
print("-" * 60)
for t, I, Q, notes in types:
    print(f"{t:>8s}  {I:>10s}  {Q:>8s}  {notes:>30s}")

#############################################
# PART 6: GLOBAL ELECTRIC CIRCUIT
#############################################
print("\n" + "="*70)
print("PART 6: GLOBAL ELECTRIC CIRCUIT")
print("="*70)

print("""
EARTH'S GLOBAL ELECTRIC CIRCUIT:
===============================

COMPONENTS:
1. Thunderstorms: ~2000 active globally at any time
2. Earth's surface: Good conductor (negative charge)
3. Ionosphere: Good conductor at ~80 km (positive)
4. Atmosphere: Poor conductor between (resistor)

FAIR WEATHER FIELD:
    E ≈ 100-150 V/m (downward)
    Current density: j ≈ 2 pA/m²
    Total current: I ≈ 1000-2000 A globally

THUNDERSTORM AS BATTERY:
    Each storm drives ~1 A upward (to ionosphere)
    ~2000 storms × 1 A = global current

CIRCUIT PARAMETERS:
    Total resistance: R ≈ 200 Ω
    Potential difference: V ≈ 250 kV (surface to ionosphere)
    Charge on Earth: Q ≈ -500,000 C

TIME CONSTANT:
    τ = ε₀ / σ ≈ 5-10 minutes (atmosphere)

Without thunderstorms, fair weather field would
discharge in ~10 minutes!

CARNEGIE CURVE:
Diurnal variation of fair weather field follows
global thunderstorm activity (peak ~19 UTC when
Africa and Americas overlap).
""")

def fair_weather_field(altitude_m, E_surface=130):
    """
    Fair weather electric field vs altitude.

    Decreases roughly exponentially.
    """
    # Scale height for conductivity increase
    H_sigma = 6000  # m

    return E_surface * np.exp(-altitude_m / H_sigma)

def atmospheric_conductivity(altitude_m):
    """
    Atmospheric conductivity vs altitude.

    Increases with altitude due to cosmic ray ionization.
    """
    sigma_0 = 1e-14  # S/m at surface
    H = 6000  # Scale height

    return sigma_0 * np.exp(altitude_m / H)

def global_resistance():
    """
    Calculate total atmospheric resistance.

    R = ∫ dz / (σ × A)
    """
    # Numerical integration
    dz = 100  # m
    z_array = np.arange(0, 80000, dz)

    A = 4 * np.pi * (6.371e6)**2  # Earth's surface area

    R_total = 0
    for z in z_array:
        sigma = atmospheric_conductivity(z)
        dR = dz / (sigma * A)
        R_total += dR

    return R_total

print("\nFair weather electric field profile:")
print("-" * 40)
for z in [0, 1000, 2000, 5000, 10000, 20000]:
    E = fair_weather_field(z)
    sigma = atmospheric_conductivity(z)
    print(f"  z = {z/1000:4.0f} km: E = {E:6.1f} V/m, σ = {sigma:.2e} S/m")

R = global_resistance()
print(f"\nGlobal atmospheric resistance: R ≈ {R:.0f} Ω")
print(f"Ionosphere-surface potential: V ≈ {1500 * R / 1000:.0f} kV")

#############################################
# PART 7: LIGHTNING SAFETY AND DETECTION
#############################################
print("\n" + "="*70)
print("PART 7: LIGHTNING DETECTION AND SAFETY")
print("="*70)

print("""
LIGHTNING DETECTION METHODS:
===========================

1. RADIO FREQUENCY (RF) DETECTION:
   Lightning emits broadband RF (1 kHz - 300 MHz)

   VLF (3-30 kHz): Long range, cloud-to-ground
   LF (30-300 kHz): Medium range, all types
   VHF (30-300 MHz): Short range, 3D mapping

   Time-of-arrival networks locate strokes to ~500 m

2. OPTICAL DETECTION:
   Satellites detect optical flash from space
   GLM (GOES-16/17): Continuous coverage

3. MAGNETIC FIELD:
   Each stroke creates distinct B-field signature
   Amplitude indicates current, polarity indicates type

LIGHTNING SAFETY:
================

30-30 RULE:
   If flash-to-bang < 30 seconds → seek shelter
   Stay sheltered until 30 minutes after last thunder

RISKY LOCATIONS:
   - Open fields
   - Under isolated trees
   - On hilltops/ridges
   - Near/in water
   - Near tall metal structures

SAFE LOCATIONS:
   - Enclosed buildings with plumbing/wiring
   - Hard-topped vehicles (Faraday cage)
   - Low ground in open areas

STEP VOLTAGE:
Ground current spreads from strike point.
Voltage between feet can be lethal.
Crouch with feet together if caught in open.
""")

def step_voltage(I_peak, distance_m, soil_resistivity=100):
    """
    Calculate step voltage from lightning strike.

    V_step = (ρ I / 2π) × (1/r₁ - 1/r₂)

    For 1 m stride at distance r:
    V_step ≈ ρ I / (2π r²)
    """
    stride = 1.0  # m

    V = soil_resistivity * I_peak * stride / (2 * np.pi * distance_m**2)
    return V

def safe_distance_from_tall_object(height_m):
    """
    Minimum distance from tall objects during storm.

    Cone of protection has ~45° half-angle.
    But ground current can spread beyond that.
    """
    # Side flash risk: stay >3 m from trunk
    # Ground current risk: stay >height distance away
    return max(height_m, 10)

print("\nStep voltage from lightning strike (30 kA):")
print("-" * 50)
I = 30e3  # 30 kA
for d in [5, 10, 20, 30, 50, 100]:
    V = step_voltage(I, d)
    lethal = "LETHAL" if V > 50 else "Dangerous" if V > 10 else "Low"
    print(f"  d = {d:3.0f} m: V_step = {V/1000:.1f} kV ({lethal})")

print("\nSafe distance from tall objects:")
for h in [5, 10, 20, 30, 50]:
    d_safe = safe_distance_from_tall_object(h)
    print(f"  Height {h} m: Stay >{d_safe:.0f} m away")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("THUNDERSTORM ELECTRIFICATION SUMMARY")
print("="*70)
print("""
Key Physics:

1. CHARGE SEPARATION:
   - Graupel-ice collisions in mixed-phase region
   - Sign reversal at T_r ≈ -10 to -20°C
   - Creates tripole: +40C (upper), -40C (middle), +10C (lower)

2. ELECTRIC FIELD:
   - Builds to 100-400 kV/m inside storm
   - Breakdown threshold ~1 MV/m at 6 km altitude
   - Requires enhancement (streamers, cosmic rays)

3. LIGHTNING:
   - Stepped leader: 10⁵-10⁶ m/s, 100-1000 A
   - Return stroke: 10⁸ m/s, 20-200 kA, 30,000 K
   - Energy: ~1 GJ per stroke

4. THUNDER:
   - Caused by rapid heating → shock wave
   - Flash-to-bang: 3 seconds per km
   - Audible to ~20-25 km

5. GLOBAL CIRCUIT:
   - ~2000 active storms maintain 250 kV potential
   - Fair weather field: ~100 V/m downward
   - Total current: ~1500 A globally

6. DETECTION:
   - VLF/LF networks: Location accuracy ~500 m
   - Satellite optical: Global coverage

Lightning is nature's most powerful electrical discharge!
""")

if __name__ == "__main__":
    print("\n[Thunderstorm Electrification Module - Complete]")
