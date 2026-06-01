#!/usr/bin/env python3
"""
Tornado and Mesocyclone Physics: First-Principles Derivations
==============================================================

Complete physics of supercell thunderstorms and tornadoes.

Key phenomena:
- Mesocyclone formation (tilting and stretching)
- Tornado vortex dynamics
- Pressure deficit and wind speed
- Fujita/EF scale physics
- Tornado climatology

Starting from vorticity dynamics and fluid mechanics.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
rho_air = 1.1         # Air density [kg/m³]
Omega = 7.292e-5      # Earth's rotation rate [rad/s]

print("="*70)
print("TORNADO AND MESOCYCLONE PHYSICS: FIRST-PRINCIPLES DERIVATIONS")
print("="*70)

#############################################
# PART 1: VORTICITY FUNDAMENTALS
#############################################
print("\n" + "="*70)
print("PART 1: VORTICITY DYNAMICS")
print("="*70)

print("""
VORTICITY EQUATION:
==================

Vorticity ω = ∇ × v (curl of velocity)

For vertical vorticity ζ in atmosphere:

    Dζ/Dt = (ζ + f) ∂w/∂z - ∂w/∂x ∂v/∂z + ∂w/∂y ∂u/∂z + friction

Terms:
1. STRETCHING: (ζ + f) ∂w/∂z
   Convergence beneath updraft stretches vortex tubes

2. TILTING: -∂w/∂x ∂v/∂z + ∂w/∂y ∂u/∂z
   Horizontal vorticity tilted into vertical by updraft gradient

3. SOLENOIDAL: From baroclinicity (density gradients)

SUPERCELL MESOCYCLONE FORMATION:
================================

Step 1: Environmental horizontal vorticity from vertical wind shear
    ω_h = ∂u/∂z  (streamwise component)

Step 2: Tilting by updraft
    Updraft gradient tilts ω_h into ω_z

Step 3: Stretching
    Convergence amplifies ζ: ζ_final = ζ_initial × (r_initial/r_final)²

HELICITY:
    H = ∫ ω · v dz

Storm-relative helicity (SRH) measures rotation potential.
SRH > 150 m²/s² → significant tornado potential
SRH > 300 m²/s² → strong tornado potential
""")

def tilting_term(du_dz, dv_dz, dw_dx, dw_dy):
    """
    Calculate tilting contribution to vertical vorticity.

    Tilting = ∂w/∂y × ∂u/∂z - ∂w/∂x × ∂v/∂z
    """
    return dw_dy * du_dz - dw_dx * dv_dz

def stretching_term(zeta, w_convergence):
    """
    Calculate stretching contribution.

    Stretching = ζ × ∂w/∂z ≈ -ζ × ∇_h · v (by continuity)
    """
    return zeta * w_convergence

def storm_relative_helicity(u_profile, v_profile, z_profile, storm_motion_u, storm_motion_v, z_top=3000):
    """
    Calculate storm-relative helicity.

    SRH = -∫₀ᴴ (v - v_storm) × (∂u/∂z) - (u - u_storm) × (∂v/∂z) dz
    """
    # Storm-relative winds
    u_sr = np.array(u_profile) - storm_motion_u
    v_sr = np.array(v_profile) - storm_motion_v

    # Integrate
    SRH = 0
    for i in range(1, len(z_profile)):
        if z_profile[i] > z_top:
            break

        dz = z_profile[i] - z_profile[i-1]
        du_dz = (u_profile[i] - u_profile[i-1]) / dz
        dv_dz = (v_profile[i] - v_profile[i-1]) / dz

        # Average storm-relative wind
        u_sr_avg = 0.5 * (u_sr[i] + u_sr[i-1])
        v_sr_avg = 0.5 * (v_sr[i] + v_sr[i-1])

        # Helicity integrand
        SRH += (v_sr_avg * du_dz - u_sr_avg * dv_dz) * dz

    return -SRH  # Negative sign convention

def vorticity_from_shear(du_dz):
    """
    Horizontal vorticity from vertical wind shear.

    ω_h = |∂V/∂z|
    """
    return du_dz

# Example: Typical severe weather shear profile
z = [0, 500, 1000, 2000, 3000, 6000]  # meters
u = [0, 5, 10, 15, 20, 25]  # m/s (increasing with height)
v = [5, 8, 10, 10, 10, 10]  # m/s

# Storm motion (Bunkers method gives ~75% of mean wind)
storm_u = 15  # m/s
storm_v = 8   # m/s

SRH = storm_relative_helicity(u, v, z, storm_u, storm_v, z_top=3000)

print("\nExample wind profile and helicity:")
print("-" * 50)
print(f"{'Height (m)':>12s}  {'u (m/s)':>10s}  {'v (m/s)':>10s}")
print("-" * 50)
for i in range(len(z)):
    print(f"{z[i]:>12.0f}  {u[i]:>10.0f}  {v[i]:>10.0f}")

print(f"\nStorm motion: ({storm_u}, {storm_v}) m/s")
print(f"0-3 km Storm Relative Helicity: SRH = {SRH:.0f} m²/s²")

# Interpret
if SRH > 300:
    print("  → HIGH tornado potential")
elif SRH > 150:
    print("  → MODERATE tornado potential")
else:
    print("  → LOW tornado potential")

#############################################
# PART 2: MESOCYCLONE DYNAMICS
#############################################
print("\n" + "="*70)
print("PART 2: MESOCYCLONE FORMATION AND STRUCTURE")
print("="*70)

print("""
MESOCYCLONE: Rotating updraft in supercell thunderstorm
=======================================================

FORMATION PROCESS:

1. ENVIRONMENTAL SHEAR creates horizontal vortex tubes:
   Shear 0-6 km: 15-25 m/s typical for supercells
   ω_h = Δv/Δz ~ 20 m/s / 6000 m = 3.3×10⁻³ s⁻¹

2. TILTING by updraft:
   Strong updraft (30-50 m/s) tilts horizontal vorticity
   Creates rotating updraft/downdraft pair

3. SPLITTING:
   Storm splits into right-moving and left-moving cells
   In Northern Hemisphere, right-mover dominates (cyclonic)

MESOCYCLONE CHARACTERISTICS:
   Diameter: 3-10 km
   Rotation rate: ω ~ 10⁻² s⁻¹
   Tangential velocity: 15-30 m/s
   Vertical velocity: 30-50 m/s

HOOK ECHO:
Radar signature of precipitation wrapped around mesocyclone.
Indicates tornado potential.

FORWARD FLANK / REAR FLANK DOWNDRAFTS:
   FFD: Precipitation-driven, ahead of mesocyclone
   RFD: Behind mesocyclone, critical for tornadogenesis
""")

def mesocyclone_circulation(radius_m, tangential_velocity):
    """
    Calculate circulation Γ = 2πr × v
    """
    return 2 * np.pi * radius_m * tangential_velocity

def mesocyclone_vorticity(circulation, radius_m):
    """
    Calculate average vorticity from circulation.

    ζ = Γ / (π r²)
    """
    return circulation / (np.pi * radius_m**2)

def updraft_stretching_amplification(initial_radius, final_radius):
    """
    Vorticity amplification from stretching.

    ζ_f / ζ_i = (r_i / r_f)²
    """
    return (initial_radius / final_radius)**2

def supercell_parameters(shear_0_6km, CAPE):
    """
    Assess supercell potential from shear and CAPE.

    Supercell Composite Parameter (SCP) simplified.
    """
    # Effective bulk shear > 15 m/s needed
    # CAPE > 1000 J/kg typically needed

    shear_factor = shear_0_6km / 20  # Normalized to 20 m/s
    cape_factor = CAPE / 2000  # Normalized to 2000 J/kg

    SCP = shear_factor * cape_factor

    return SCP

print("\nMesocyclone stretching dynamics:")
print("-" * 55)
print(f"{'Initial r (km)':>15s}  {'Final r (km)':>15s}  {'ζ amplification':>16s}")
print("-" * 55)

for r_i in [5, 3, 2]:
    for r_f in [2, 1, 0.5]:
        if r_f < r_i:
            amp = updraft_stretching_amplification(r_i * 1000, r_f * 1000)
            print(f"{r_i:>15.0f}  {r_f:>15.1f}  {amp:>16.0f}×")

print("\nSupercell potential assessment:")
print("-" * 55)
cases = [
    ("Marginal", 15, 1000),
    ("Moderate", 20, 1500),
    ("High", 25, 2500),
    ("Extreme", 30, 4000),
]
for name, shear, cape in cases:
    SCP = supercell_parameters(shear, cape)
    print(f"  {name:12s}: Shear={shear} m/s, CAPE={cape} J/kg → SCP={SCP:.1f}")

#############################################
# PART 3: TORNADO VORTEX PHYSICS
#############################################
print("\n" + "="*70)
print("PART 3: TORNADO VORTEX STRUCTURE")
print("="*70)

print("""
TORNADO: Violently rotating column of air
=========================================

FORMATION (Tornadogenesis):
Multiple hypotheses:
1. Dynamic pipe effect (stretching of mesocyclone)
2. Baroclinic boundaries (outflow interactions)
3. Descending vortex from aloft

VORTEX MODELS:

1. RANKINE VORTEX (solid body core + potential flow):
   r < R_max: v(r) = v_max × (r/R_max)     [solid body]
   r > R_max: v(r) = v_max × (R_max/r)     [potential]

2. BURGERS-ROTT VORTEX (includes radial inflow):
   More realistic, has radial and vertical flow

PRESSURE DEFICIT:
From cyclostrophic balance: ∂p/∂r = ρv²/r

Integrating Rankine vortex:
   Δp = ρ v_max² × [1 + ln(r_outer/R_max)]

For v_max = 100 m/s: Δp ≈ 100 hPa (10% of atmospheric!)

SWIRL RATIO:
   S = (Γ × r) / (Q × z)

Where Γ = circulation, Q = radial volume flux
S < 1: Single vortex
S > 1: Multiple vortices (suction vortices)
""")

def rankine_vortex(r, r_max, v_max):
    """
    Rankine combined vortex model.

    Solid body rotation inside r_max,
    Potential vortex outside.
    """
    r = np.atleast_1d(r)
    v = np.zeros_like(r, dtype=float)

    inner = r <= r_max
    outer = r > r_max

    v[inner] = v_max * r[inner] / r_max
    v[outer] = v_max * r_max / r[outer]

    return v

def tornado_pressure_deficit(v_max, r_max=100, r_outer=1000, rho=1.1):
    """
    Calculate central pressure deficit from cyclostrophic balance.

    Δp = ρ v² integrated from center to outer radius.
    """
    # Rankine vortex pressure deficit
    # Inner core: Δp = ρ v_max² / 2
    # Outer region: Δp = ρ v_max² × ln(r_outer/r_max)

    delta_p_inner = 0.5 * rho * v_max**2
    delta_p_outer = rho * v_max**2 * np.log(r_outer / r_max)

    return delta_p_inner + delta_p_outer

def cyclostrophic_wind(pressure_deficit_Pa, r_max, rho=1.1):
    """
    Invert: calculate max wind from pressure deficit.

    Assuming Rankine, approximately:
    Δp ≈ 1.5 × ρ × v_max²
    """
    return np.sqrt(pressure_deficit_Pa / (1.5 * rho))

print("\nRankine vortex wind profile (v_max = 100 m/s, r_max = 100 m):")
print("-" * 45)
r_values = [10, 25, 50, 100, 200, 500, 1000]
v_max = 100
r_max = 100

print(f"{'r (m)':>10s}  {'v (m/s)':>12s}  {'v (mph)':>12s}")
print("-" * 45)
for r in r_values:
    v = rankine_vortex(r, r_max, v_max)
    print(f"{r:>10.0f}  {v[0]:>12.1f}  {v[0]*2.237:>12.0f}")

print("\nTornado pressure deficit vs intensity:")
print("-" * 50)
for v in [50, 75, 100, 125, 150, 200]:
    dp = tornado_pressure_deficit(v)
    print(f"  v_max = {v:3.0f} m/s ({v*2.237:.0f} mph): Δp = {dp/100:.0f} hPa")

#############################################
# PART 4: ENHANCED FUJITA (EF) SCALE
#############################################
print("\n" + "="*70)
print("PART 4: TORNADO INTENSITY SCALES")
print("="*70)

print("""
ENHANCED FUJITA (EF) SCALE:
==========================

Based on DAMAGE INDICATORS, not direct wind measurement.

EF0: 65-85 mph (29-38 m/s)
     Light damage: branches broken, signs damaged

EF1: 86-110 mph (38-49 m/s)
     Moderate damage: roofs peeled, mobile homes overturned

EF2: 111-135 mph (50-60 m/s)
     Considerable: roofs torn off, large trees uprooted

EF3: 136-165 mph (61-74 m/s)
     Severe: entire stories destroyed, trains derailed

EF4: 166-200 mph (74-89 m/s)
     Devastating: well-built homes leveled

EF5: >200 mph (>89 m/s)
     Incredible: strong frame homes swept away

DAMAGE PHYSICS:
Wind force F = 0.5 × ρ × Cd × A × v²

At 200 mph (89 m/s):
    Dynamic pressure q = 0.5 × 1.1 × 89² = 4.4 kPa
    On 1 m² wall (Cd=1.5): F = 6.6 kN = 1500 lbf

TORNADO STATISTICS (US):
    ~1200 tornadoes per year
    ~60 deaths per year
    EF0-EF1: 75% of all tornadoes
    EF4-EF5: <1% but cause most deaths
""")

def ef_scale_winds():
    """Return EF scale wind speed ranges in m/s."""
    return {
        'EF0': (29, 38),
        'EF1': (38, 49),
        'EF2': (50, 60),
        'EF3': (61, 74),
        'EF4': (74, 89),
        'EF5': (89, 150)  # Upper bound theoretical
    }

def wind_force(v_ms, area_m2, Cd=1.5, rho=1.1):
    """
    Calculate wind force on structure.

    F = 0.5 ρ Cd A v²
    """
    return 0.5 * rho * Cd * area_m2 * v_ms**2

def dynamic_pressure(v_ms, rho=1.1):
    """
    Dynamic pressure q = 0.5 ρ v²
    """
    return 0.5 * rho * v_ms**2

print("\nEF Scale and associated forces:")
print("-" * 70)
print(f"{'Rating':>6s}  {'v_low':>8s}  {'v_high':>8s}  {'q (kPa)':>10s}  {'Force/m² (kN)':>14s}")
print("-" * 70)

ef = ef_scale_winds()
for rating, (v_low, v_high) in ef.items():
    q = dynamic_pressure(v_high)
    F = wind_force(v_high, 1.0)
    print(f"{rating:>6s}  {v_low:>6.0f}  {v_high:>8.0f}  {q/1000:>10.2f}  {F/1000:>14.2f}")

print("\n  At EF5 (89 m/s): Pressure ~4.4 kPa = 90 psf")
print("  Wood frame buildings designed for ~30-50 psf")

#############################################
# PART 5: TORNADO CLIMATOLOGY
#############################################
print("\n" + "="*70)
print("PART 5: TORNADO CLIMATOLOGY")
print("="*70)

print("""
US TORNADO CLIMATOLOGY:
======================

TORNADO ALLEY: Central US concentration
    Peak region: OK, KS, NE, TX Panhandle

WHY TORNADO ALLEY EXISTS:
1. Gulf moisture source to south
2. Rocky Mountains create dryline
3. Strong jet stream provides shear
4. Cold fronts from Canada
5. Flat terrain (no disruption)

SEASONAL VARIATION:
    March-May: Peak in southern Plains
    May-June: Peak moves north to northern Plains
    Nov-Dec: Secondary peak in Southeast

DIURNAL VARIATION:
    Peak: 4-8 PM local time
    Minimum: 6-10 AM
    Reason: Maximum heating → CAPE → convection

LIFETIME AND SIZE:
    Duration: 1-20 minutes typical (some >1 hr)
    Path width: 50-500 m typical (max ~4 km)
    Path length: 0.1-50 km typical (max >200 km)

GLOBAL DISTRIBUTION:
    US: ~1200/year (most in world)
    Canada: ~100/year
    Bangladesh: ~50/year (highest per capita deaths)
    Europe: ~200-300/year
    Argentina: ~50/year
""")

def tornado_probability(cape, srh, shear_0_6):
    """
    Simplified tornado probability estimate.

    Based on Significant Tornado Parameter (STP) proxy.
    """
    # Very simplified
    if cape < 500 or srh < 50 or shear_0_6 < 10:
        return 0

    cape_factor = min(cape / 2000, 2)
    srh_factor = min(srh / 200, 2)
    shear_factor = min(shear_0_6 / 20, 2)

    STP = cape_factor * srh_factor * shear_factor

    # Convert to rough probability
    prob = min(0.05 * STP, 0.5)  # Cap at 50%

    return prob

def tornado_motion(storm_motion_u, storm_motion_v, deviation_right=7.5):
    """
    Estimate tornado motion from supercell motion.

    Tornadoes typically move slightly right of storm motion.
    """
    # Convert to speed and direction
    speed = np.sqrt(storm_motion_u**2 + storm_motion_v**2)
    direction = np.degrees(np.arctan2(storm_motion_v, storm_motion_u))

    # Deviate right
    new_direction = direction + deviation_right
    new_u = speed * np.cos(np.radians(new_direction))
    new_v = speed * np.sin(np.radians(new_direction))

    return new_u, new_v, speed

print("\nTornado probability estimates:")
print("-" * 60)
environments = [
    ("Weak instability", 800, 100, 15),
    ("Moderate", 1500, 150, 20),
    ("Strong", 2500, 250, 25),
    ("Extreme", 4000, 400, 35),
]

print(f"{'Environment':>20s}  {'CAPE':>6s}  {'SRH':>6s}  {'Shear':>6s}  {'P(tor)':>8s}")
print("-" * 60)
for name, cape, srh, shear in environments:
    prob = tornado_probability(cape, srh, shear)
    print(f"{name:>20s}  {cape:>6.0f}  {srh:>6.0f}  {shear:>6.0f}  {prob:>8.1%}")

#############################################
# PART 6: TORNADO DETECTION AND WARNING
#############################################
print("\n" + "="*70)
print("PART 6: DETECTION AND WARNING")
print("="*70)

print("""
RADAR DETECTION:
===============

1. HOOK ECHO: Precipitation wrapping around mesocyclone
   Indicates potential tornado

2. MESOCYCLONE DETECTION:
   Doppler velocity shows rotation
   Azimuthal shear > 10⁻² s⁻¹ significant

3. TORNADO VORTEX SIGNATURE (TVS):
   Strong rotation in small area
   ΔV > 50 m/s across ~1 km gate separation

4. DEBRIS BALL:
   High reflectivity (>60 dBZ) in tornado
   Debris lofted into circulation

DUAL-POL SIGNATURES:
    Low correlation coefficient (ρhv < 0.8)
    Random differential reflectivity (Zdr)
    Due to tumbling debris

WARNING LEAD TIME:
    Average: ~13 minutes
    Goal: >20 minutes
    Challenge: Small tornadoes, rapid development

FALSE ALARM RATIO:
    ~75% of warnings don't verify
    Challenge: Over-warning leads to complacency
""")

def mesocyclone_shear(delta_v, gate_spacing_m):
    """
    Calculate azimuthal shear from Doppler velocities.

    shear = Δv / (2 × r × Δθ) ≈ Δv / gate_spacing
    """
    return delta_v / gate_spacing_m

def probability_of_detection(lead_time_minutes, intensity_ef):
    """
    Rough POD based on intensity and lead time need.

    Stronger tornadoes more likely to be warned.
    """
    base_pod = {0: 0.3, 1: 0.5, 2: 0.7, 3: 0.85, 4: 0.95, 5: 0.98}

    return base_pod.get(intensity_ef, 0.5)

print("\nRadar shear thresholds for tornado detection:")
print("-" * 50)
print(f"{'Δv (m/s)':>10s}  {'Gate (m)':>10s}  {'Shear (s⁻¹)':>12s}  {'Significance':>15s}")
print("-" * 50)

for dv in [20, 30, 50, 70, 100]:
    for gate in [250, 500, 1000]:
        shear = mesocyclone_shear(dv, gate)
        sig = "Marginal" if shear < 0.01 else "Moderate" if shear < 0.02 else \
              "Strong" if shear < 0.04 else "Violent"
        print(f"{dv:>10.0f}  {gate:>10.0f}  {shear:>12.4f}  {sig:>15s}")

#############################################
# PART 7: Z² CONNECTION TO TORNADO INTENSITY
#############################################
print("\n" + "="*70)
print("PART 7: ENERGY PHYSICS OF TORNADOES")
print("="*70)

print("""
TORNADO ENERGY FROM FIRST PRINCIPLES:
====================================

KINETIC ENERGY:
For Rankine vortex:
    KE = ∫ (1/2)ρv² dV

    KE ≈ π ρ v_max² R_max² H × [0.5 + ln(R_outer/R_max)]

For EF5 tornado (v=90 m/s, R=150m, H=500m):
    KE ≈ 3.14 × 1.1 × 90² × 150² × 500 × 2
    KE ≈ 2 × 10¹⁰ J = 20 GJ

POWER:
For 10-minute tornado:
    P = KE / τ ≈ 33 MW

COMPARISON TO MESOCYCLONE:
Mesocyclone (v=30 m/s, R=3km, H=10km):
    KE ≈ 10¹³ J = 10 TJ

Tornado is ~0.1% of mesocyclone energy,
but concentrated in tiny volume → extreme intensity.

Z² = 32π/3 CONNECTION:
The Zimmerman constant may relate to optimal
energy concentration in rotating systems.
""")

def tornado_kinetic_energy(v_max, r_max, height, r_outer=1000, rho=1.1):
    """
    Calculate kinetic energy of Rankine vortex.
    """
    # Simplified: KE ≈ 1.5 × 0.5 × ρ × v² × π × r² × H
    # The 1.5 accounts for outer region contribution

    factor = 0.5 + np.log(r_outer / r_max)
    KE = np.pi * rho * v_max**2 * r_max**2 * height * factor

    return KE

def tornado_power(KE, duration_s):
    """
    Average power of tornado.
    """
    return KE / duration_s

print("\nTornado energy by intensity:")
print("-" * 65)
print(f"{'Rating':>6s}  {'v (m/s)':>10s}  {'r (m)':>8s}  {'KE (GJ)':>10s}  {'Power (MW)':>12s}")
print("-" * 65)

tornado_specs = [
    ('EF1', 45, 75, 300),
    ('EF2', 55, 100, 400),
    ('EF3', 70, 125, 500),
    ('EF4', 82, 150, 500),
    ('EF5', 95, 200, 500),
]

for rating, v, r, h in tornado_specs:
    KE = tornado_kinetic_energy(v, r, h)
    P = tornado_power(KE, 600)  # 10 minute duration
    print(f"{rating:>6s}  {v:>10.0f}  {r:>8.0f}  {KE/1e9:>10.1f}  {P/1e6:>12.1f}")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("TORNADO AND MESOCYCLONE PHYSICS SUMMARY")
print("="*70)
print("""
Key Physics:

1. VORTICITY DYNAMICS:
   - Tilting: Horizontal vorticity → vertical by updraft
   - Stretching: ζ_f/ζ_i = (r_i/r_f)² - huge amplification!
   - SRH > 150 m²/s² indicates tornado potential

2. MESOCYCLONE:
   - 3-10 km diameter rotating updraft
   - Forms from environmental shear + tilting
   - Right-moving supercells dominate in NH

3. TORNADO STRUCTURE:
   - Rankine vortex: solid body + potential flow
   - Pressure deficit: Δp ~ ρv² (100+ hPa for EF5)
   - v_max at r_max (50-200 m typically)

4. EF SCALE:
   - EF0: 29-38 m/s (65-85 mph)
   - EF5: >89 m/s (>200 mph)
   - Wind force ∝ v² (4× speed = 16× force)

5. CLIMATOLOGY:
   - ~1200/year in US (Tornado Alley peak)
   - Peak: April-June, 4-8 PM local time
   - EF4-5: <1% but most deadly

6. DETECTION:
   - Mesocyclone: Δv rotation on radar
   - TVS: Strong rotation, small area
   - Dual-pol: Debris signature (low ρhv)

7. ENERGY:
   - KE ~ 1-50 GJ per tornado
   - Power ~ 10-100 MW
   - Concentrated energy → extreme damage

Understanding vorticity dynamics is key to tornado physics!
""")

if __name__ == "__main__":
    print("\n[Tornado and Mesocyclone Physics Module - Complete]")
