#!/usr/bin/env python3
"""
Jet Stream and Upper-Level Dynamics: First-Principles Derivations
===================================================================

Complete physics of jet streams and upper tropospheric flow.

Key phenomena:
- Thermal wind balance
- Jet stream formation
- Jet streaks and ageostrophic circulations
- Rossby waves and blocking
- Tropopause dynamics

Starting from geostrophic and thermal wind theory.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
Omega = 7.292e-5      # Earth's rotation rate [rad/s]
R_earth = 6.371e6     # Earth radius [m]
R_d = 287.05          # Gas constant for dry air [J/kg/K]
c_p = 1005            # Specific heat [J/kg/K]

print("="*70)
print("JET STREAM AND UPPER-LEVEL DYNAMICS: FIRST-PRINCIPLES PHYSICS")
print("="*70)

#############################################
# PART 1: THERMAL WIND BALANCE
#############################################
print("\n" + "="*70)
print("PART 1: THERMAL WIND DERIVATION")
print("="*70)

print("""
THERMAL WIND: WHY JETS EXIST
============================

Starting from geostrophic balance:
    fv = (1/ρ) ∂p/∂x
    fu = -(1/ρ) ∂p/∂y

Using hydrostatic equation: ∂p/∂z = -ρg
And ideal gas: p = ρRT

Differentiate geostrophic wind with height:

    ∂v_g/∂z = -(g/fT) ∂T/∂x
    ∂u_g/∂z = (g/fT) ∂T/∂y

THERMAL WIND EQUATION:
    V_T = V_g(upper) - V_g(lower)
    |V_T| = (g/f) × (ΔT/ΔL) × (Δp/p̄)

In vector form:
    V_T = (R/f) × k̂ × ∇T × ln(p₁/p₂)

KEY INSIGHT:
Horizontal temperature gradient → vertical wind shear
Warm air to right of wind (NH looking downwind)
Stronger gradient → stronger jet
""")

def coriolis_parameter(lat_deg):
    """f = 2Ω sin(φ)"""
    return 2 * Omega * np.sin(np.radians(lat_deg))

def thermal_wind_magnitude(dT_dy, delta_z, T_mean, lat_deg):
    """
    Calculate thermal wind magnitude.

    |V_T| = (g/fT) × |∂T/∂y| × Δz
    """
    f = coriolis_parameter(lat_deg)
    if abs(f) < 1e-6:
        return float('inf')

    return (g / (f * T_mean)) * abs(dT_dy) * delta_z

def geostrophic_wind_aloft(V_surface, thermal_wind):
    """
    Calculate upper-level geostrophic wind.

    V(z) = V_surface + V_T
    """
    return V_surface + thermal_wind

def temperature_gradient_for_jet(jet_speed, delta_z=10000, T_mean=250, lat_deg=45):
    """
    Invert: What dT/dy is needed to produce jet?
    """
    f = coriolis_parameter(lat_deg)
    # |V_T| = (g/fT) × |dT/dy| × Δz
    # dT/dy = V_T × f × T / (g × Δz)

    dT_dy = jet_speed * f * T_mean / (g * delta_z)
    return dT_dy

print("\nThermal wind calculation example:")
print("-" * 55)

# Typical midlatitude values
dT_dy = -2e-5  # K/m = 2°C per 100 km (equator-to-pole gradient)
delta_z = 10000  # 10 km (surface to tropopause)
T_mean = 250  # K
lat = 45  # degrees

V_T = thermal_wind_magnitude(dT_dy, delta_z, T_mean, lat)

print(f"  Latitude: {lat}°")
print(f"  Temperature gradient: {dT_dy*1e5:.1f} °C per 100 km")
print(f"  Layer thickness: {delta_z/1000:.0f} km")
print(f"  Mean temperature: {T_mean} K")
print(f"\n  Thermal wind magnitude: |V_T| = {V_T:.1f} m/s")

print("\nThermal wind vs latitude (same dT/dy):")
print("-" * 50)
print(f"{'Latitude':>10s}  {'f (×10⁴)':>12s}  {'V_T (m/s)':>12s}")
print("-" * 50)
for lat in [20, 30, 40, 50, 60, 70]:
    V_T = thermal_wind_magnitude(dT_dy, delta_z, T_mean, lat)
    f = coriolis_parameter(lat)
    print(f"{lat:>10.0f}°  {f*1e4:>12.2f}  {V_T:>12.1f}")

#############################################
# PART 2: JET STREAM STRUCTURE
#############################################
print("\n" + "="*70)
print("PART 2: JET STREAM STRUCTURE")
print("="*70)

print("""
POLAR JET AND SUBTROPICAL JET:
=============================

POLAR FRONT JET (PFJ):
    Location: ~30-60°N, follows polar front
    Height: ~9-10 km (300-200 hPa)
    Speed: 30-70 m/s typically, >100 m/s in winter
    Width: ~100-400 km
    Depth: ~3-5 km

    Forms where polar air meets midlatitude air
    → Strong baroclinicity → Strong thermal wind

SUBTROPICAL JET (STJ):
    Location: ~25-35°N
    Height: ~12-15 km (200-100 hPa)
    Speed: 30-50 m/s typically
    Width: ~500-1000 km

    Associated with poleward edge of Hadley cell
    Angular momentum conservation from tropics

JET CORE:
Where wind speed is maximum:
    ∂V/∂y = 0, ∂V/∂z = 0

Vertical profile (hyperbolic tangent approximation):
    V(z) = V_max × sech²[(z-z_jet)/H_jet]
""")

def jet_wind_profile_vertical(z_array, z_jet=10000, V_max=60, H_jet=2000):
    """
    Vertical wind profile through jet core.

    Hyperbolic secant squared profile.
    """
    return V_max * (1 / np.cosh((z_array - z_jet) / H_jet))**2

def jet_wind_profile_horizontal(y_array, y_jet=0, V_max=60, L_jet=200e3):
    """
    Horizontal (meridional) profile through jet.
    """
    return V_max * np.exp(-((y_array - y_jet) / L_jet)**2)

def jet_stream_height_from_tropopause(lat_deg, season='winter'):
    """
    Estimate jet stream height based on tropopause.

    Tropopause lower at poles, higher in tropics.
    """
    if season == 'winter':
        # Winter: polar jet dominant, lower
        if lat_deg > 50:
            return 9000  # m
        elif lat_deg > 35:
            return 10000
        else:
            return 12000  # Subtropical jet region
    else:
        # Summer: jets weaker, polar jet northward
        if lat_deg > 55:
            return 9500
        elif lat_deg > 40:
            return 11000
        else:
            return 13000

print("\nJet stream vertical profile (V_max = 60 m/s at 10 km):")
print("-" * 40)
z = np.arange(0, 16001, 2000)
print(f"{'Height (km)':>12s}  {'V (m/s)':>12s}")
print("-" * 40)
for z_val in z:
    V = jet_wind_profile_vertical(z_val, z_jet=10000, V_max=60, H_jet=2500)
    print(f"{z_val/1000:>12.0f}  {V:>12.1f}")

print("\nTypical jet stream characteristics:")
print("-" * 55)
jets = [
    ("Winter Polar Jet (strong)", 60, 75, 10, 300),
    ("Winter Polar Jet (typical)", 45, 60, 10, 300),
    ("Summer Polar Jet", 40, 25, 11, 400),
    ("Subtropical Jet", 35, 40, 13, 500),
]
print(f"{'Jet':>30s}  {'Lat':>5s}  {'V_max':>8s}  {'Height':>8s}  {'Width':>8s}")
print("-" * 55)
for name, lat, v, h, w in jets:
    print(f"{name:>30s}  {lat:>5.0f}°  {v:>6.0f} m/s  {h:>6.0f} km  {w:>6.0f} km")

#############################################
# PART 3: JET STREAKS AND AGEOSTROPHIC WIND
#############################################
print("\n" + "="*70)
print("PART 3: JET STREAKS AND SECONDARY CIRCULATIONS")
print("="*70)

print("""
JET STREAKS: Embedded wind maxima
================================

Jet streaks are localized wind maxima within the jet stream,
typically 1000-3000 km long.

AGEOSTROPHIC WIND:
    V_ag = V_actual - V_g

In jet entrance/exit regions, flow is not geostrophic.

FOUR-QUADRANT MODEL:
For straight jet streak:

    ENTRANCE          EXIT
    ┌─────┬─────┐    ┌─────┬─────┐
    │ R-D │ L-C │    │ L-D │ R-C │
    │     │  ↑  │→→→→│  ↑  │     │
    │     │     │    │     │     │
    └─────┴─────┴────┴─────┴─────┘

    L = Left (north in NH)    R = Right (south in NH)
    C = Convergence aloft     D = Divergence aloft
    ↑ = Upward motion         (↓ = implied where C)

DIVERGENCE ALOFT → SURFACE CONVERGENCE → LIFT
    Left-exit and Right-entrance: Upper divergence, rising motion
    These regions favor cyclogenesis and convection

PHYSICS:
In entrance region: Air accelerates, Coriolis lags
    → Ageostrophic component across isobars (toward low pressure)
In exit region: Air decelerates, Coriolis exceeds PGF
    → Ageostrophic component across isobars (toward high pressure)
""")

def ageostrophic_wind_entrance(V_jet, acceleration_distance, lat_deg):
    """
    Estimate ageostrophic wind in jet entrance region.

    V_ag ≈ (1/f) × dV/dt ≈ (1/f) × V × dV/dx
    """
    f = coriolis_parameter(lat_deg)
    if abs(f) < 1e-6:
        return 0

    # Acceleration
    dV_dx = V_jet / acceleration_distance
    a = V_jet * dV_dx

    # Ageostrophic wind
    V_ag = a / f

    return V_ag

def divergence_from_ageostrophic(V_ag, length_scale):
    """
    Estimate divergence from ageostrophic wind.

    div = ∂V_ag/∂x ≈ V_ag / L
    """
    return V_ag / length_scale

def vertical_velocity_from_divergence(divergence, layer_depth):
    """
    Estimate vertical velocity from divergence.

    w = -∫ div dz ≈ -div × Δz
    """
    return -divergence * layer_depth

print("\nJet streak ageostrophic circulation:")
print("-" * 60)

V_jet = 60  # m/s
acc_dist = 1000e3  # 1000 km
lat = 45  # degrees

V_ag = ageostrophic_wind_entrance(V_jet, acc_dist, lat)
div_500 = divergence_from_ageostrophic(V_ag, 500e3)
w = vertical_velocity_from_divergence(div_500, 3000)

print(f"  Jet speed: {V_jet} m/s")
print(f"  Acceleration distance: {acc_dist/1e3:.0f} km")
print(f"  Latitude: {lat}°")
print(f"\n  Ageostrophic wind: {V_ag:.1f} m/s")
print(f"  Upper-level divergence: {div_500*1e5:.2f} ×10⁻⁵ s⁻¹")
print(f"  Implied vertical velocity: {w*100:.1f} cm/s")

if w < 0:
    print(f"  → Descent (subsidence)")
else:
    print(f"  → Ascent (supports convection/cyclogenesis)")

#############################################
# PART 4: ROSSBY WAVES
#############################################
print("\n" + "="*70)
print("PART 4: ROSSBY WAVES AND PLANETARY WAVES")
print("="*70)

print("""
ROSSBY WAVES: Large-scale meanders in jet
========================================

BETA EFFECT:
Coriolis parameter varies with latitude:
    β = df/dy = (2Ω/R_earth) cos(φ)

This creates restoring force for meridional displacements.

ROSSBY WAVE DISPERSION RELATION:
    c = U - β/(k² + l² + f²/N²H²)

For barotropic case (no vertical structure):
    c = U - β/K²

Where:
    c = phase speed (can be negative = westward)
    U = mean flow
    K² = k² + l² (horizontal wavenumber squared)
    k = 2π/λ_x (zonal wavenumber)

STATIONARY WAVES (c = 0):
    U = β/K²  →  K_stationary = √(β/U)

    λ_stationary = 2π/K = 2π√(U/β)

For U = 15 m/s at 45°N:
    λ ≈ 6000-8000 km (wavenumber 4-6)

These stationary waves create persistent ridges/troughs,
controlling weather patterns for days to weeks.

GROUP VELOCITY:
    c_g = ∂ω/∂k = U + β(k² - l²)/(k² + l²)²

Energy propagates EASTWARD faster than phase!
""")

def beta_parameter(lat_deg):
    """Calculate β = df/dy = 2Ω cos(φ) / R_earth"""
    return 2 * Omega * np.cos(np.radians(lat_deg)) / R_earth

def rossby_wave_phase_speed(U, wavelength_km, lat_deg):
    """
    Calculate Rossby wave phase speed.

    c = U - β/k²
    """
    beta = beta_parameter(lat_deg)
    k = 2 * np.pi / (wavelength_km * 1000)  # Convert to 1/m

    c = U - beta / k**2
    return c

def stationary_wavelength(U, lat_deg):
    """
    Calculate wavelength of stationary Rossby wave.

    λ = 2π√(U/β)
    """
    beta = beta_parameter(lat_deg)
    return 2 * np.pi * np.sqrt(U / beta) / 1000  # km

def rossby_wave_group_velocity(U, wavelength_km, lat_deg):
    """
    Calculate group velocity for purely zonal wave.

    c_g = U + β/k² (for l=0)
    """
    beta = beta_parameter(lat_deg)
    k = 2 * np.pi / (wavelength_km * 1000)

    # For l=0: c_g = U + β/k²
    c_g = U + beta / k**2
    return c_g

print("\nRossby wave characteristics at 45°N:")
print("-" * 60)

lat = 45
beta = beta_parameter(lat)
print(f"  β = {beta:.2e} m⁻¹s⁻¹")

U = 15  # m/s mean flow
lambda_stat = stationary_wavelength(U, lat)
print(f"  Mean flow U = {U} m/s")
print(f"  Stationary wavelength = {lambda_stat:.0f} km (wavenumber ~{40000/lambda_stat:.1f})")

print("\nPhase and group velocity vs wavelength:")
print("-" * 65)
print(f"{'λ (km)':>10s}  {'c_phase':>12s}  {'c_group':>12s}  {'c_p - U':>12s}  {'Comment':>15s}")
print("-" * 65)

for lam in [3000, 4000, 5000, 6000, 8000, 10000]:
    c = rossby_wave_phase_speed(U, lam, lat)
    cg = rossby_wave_group_velocity(U, lam, lat)

    if abs(c) < 0.5:
        comment = "~Stationary"
    elif c < 0:
        comment = "Westward"
    else:
        comment = "Eastward"

    print(f"{lam:>10.0f}  {c:>10.1f} m/s  {cg:>10.1f} m/s  {c-U:>10.1f} m/s  {comment:>15s}")

#############################################
# PART 5: BLOCKING AND PERSISTENT PATTERNS
#############################################
print("\n" + "="*70)
print("PART 5: BLOCKING AND REX PATTERNS")
print("="*70)

print("""
BLOCKING: When jet flow becomes meridional
=========================================

BLOCKING HIGH:
Strong ridge amplifies and becomes cut off from main flow.
Persistent high pressure deflects storms.

CHARACTERISTICS:
- Duration: 5-30+ days
- More common in winter
- Preferred locations: NE Pacific, NE Atlantic, Urals

OMEGA BLOCK:
Shape like Greek letter Ω
High flanked by two cut-off lows

REX BLOCK:
High poleward, low equatorward
Reversed from normal: "Rex pattern"

PHYSICS OF BLOCKING:
1. Wave breaking: Rossby waves overturn
2. Nonlinear dynamics: Wave-mean flow interaction
3. Resonance: Stationary wave reinforcement
4. External forcing: Mountains, heating anomalies

IMPACTS:
- Prolonged heat waves/cold spells
- Drought (persistent ridge)
- Flooding (persistent trough)
- Disrupted storm tracks
""")

def blocking_index_1d(z500_north, z500_south, z500_middle, lat_spacing=15):
    """
    Simple 1D blocking index (Tibaldi-Molteni style).

    Blocking when:
    1. GHGN > 0 (reversed gradient to north)
    2. GHGS < -10 m/deg (normal gradient to south)

    GHGN = (Z_middle - Z_north) / Δφ
    GHGS = (Z_south - Z_middle) / Δφ
    """
    GHGN = (z500_middle - z500_north) / lat_spacing  # m/deg
    GHGS = (z500_south - z500_middle) / lat_spacing

    blocking = (GHGN > 0) and (GHGS < -10)

    return blocking, GHGN, GHGS

def block_persistence_probability(initial_days, hemisphere='NH'):
    """
    Rough probability that a block persists another day.

    Blocks tend to be self-sustaining once established.
    """
    # Simplified: ~85% chance of persisting each day after day 3
    if initial_days < 3:
        return 0.7 + 0.05 * initial_days
    else:
        return 0.85  # Mature blocks are persistent

print("\nBlocking index examples:")
print("-" * 65)
cases = [
    ("Normal westerly", 5300, 5600, 5400),
    ("Weak ridge", 5350, 5600, 5500),
    ("Strong ridge", 5400, 5600, 5600),
    ("Blocking", 5500, 5600, 5450),
    ("Strong block", 5550, 5600, 5400),
]

print(f"{'Pattern':>20s}  {'Z_N':>8s}  {'Z_mid':>8s}  {'Z_S':>8s}  {'Blocking?':>10s}")
print("-" * 65)
for name, z_n, z_s, z_mid in cases:
    blocking, GHGN, GHGS = blocking_index_1d(z_n, z_s, z_mid)
    result = "YES" if blocking else "No"
    print(f"{name:>20s}  {z_n:>8.0f}  {z_mid:>8.0f}  {z_s:>8.0f}  {result:>10s}")

#############################################
# PART 6: TROPOPAUSE DYNAMICS
#############################################
print("\n" + "="*70)
print("PART 6: TROPOPAUSE AND STRATOSPHERIC INTRUSIONS")
print("="*70)

print("""
TROPOPAUSE: Boundary between troposphere and stratosphere
========================================================

DEFINITION:
WMO: Lowest level where lapse rate < 2°C/km
    for at least 2 km above

Dynamic tropopause: Surface of constant PV
    (typically 1.5 or 2 PVU)

POTENTIAL VORTICITY (PV):
    PV = (ζ + f) × (-g ∂θ/∂p)

Units: 1 PVU = 10⁻⁶ K m² kg⁻¹ s⁻¹

TROPOPAUSE CHARACTERISTICS:
    Tropics: 16-18 km (100 hPa), T ~ -80°C
    Midlatitudes: 10-12 km (250-200 hPa), T ~ -55°C
    Poles: 8-10 km (300-250 hPa), T ~ -50°C

TROPOPAUSE FOLDS:
Upper-level troughs pull stratospheric air downward.
High PV, high ozone injected into troposphere.

STRATOSPHERIC INTRUSIONS:
- Bring dry, high-ozone air to surface
- Associated with jet stream dynamics
- Can trigger severe weather (enhanced instability)

SUBTROPICAL JET AND TROPOPAUSE BREAK:
Hadley cell rising motion at ITCZ
Air ascends to tropical tropopause (~17 km)
Hadley cell descent at ~30° → subtropical jet
Tropopause breaks between tropical and polar air
""")

def tropopause_height(lat_deg, season='annual'):
    """
    Estimate tropopause height based on latitude.
    """
    # Simple empirical fit
    if lat_deg < 15:
        return 17000 - 100 * lat_deg  # Tropical
    elif lat_deg < 40:
        # Transition zone
        return 15500 - 150 * (lat_deg - 15)
    else:
        # Polar
        return 11750 - 50 * (lat_deg - 40)

def potential_vorticity(abs_vorticity, stability_dtheta_dp):
    """
    Calculate Ertel PV.

    PV = (ζ + f) × (-g ∂θ/∂p)
    """
    return abs_vorticity * (-g * stability_dtheta_dp)

def pv_from_tropopause_fold_depth(fold_depth_m, background_pv=1.5e-6):
    """
    Estimate PV anomaly from tropopause fold depth.

    Deeper fold → stronger PV anomaly at surface.
    """
    # Very rough: PV ~ 2-4 PVU in stratosphere, ~0.5 in troposphere
    # Fold brings high PV down
    pv_anomaly = 2e-6 * (fold_depth_m / 5000)  # Scale to 5 km fold

    return background_pv + pv_anomaly

print("\nTropopause height by latitude:")
print("-" * 40)
for lat in [0, 15, 30, 45, 60, 75, 90]:
    h = tropopause_height(lat)
    print(f"  {lat:2.0f}°: {h/1000:.1f} km")

print("\nTypical PV values:")
print("-" * 45)
regions = [
    ("Stratosphere", "4-10 PVU"),
    ("Tropopause (dynamic def.)", "1.5-2 PVU"),
    ("Upper troposphere", "0.5-1 PVU"),
    ("Lower troposphere", "0.1-0.5 PVU"),
    ("Tropopause fold", "2-4 PVU at 500 hPa"),
]
for region, pv in regions:
    print(f"  {region:30s}: {pv}")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("JET STREAM DYNAMICS SUMMARY")
print("="*70)
print("""
Key Physics:

1. THERMAL WIND:
   ∂V_g/∂z = (g/fT) ∇T × k̂
   → Horizontal T gradient creates vertical wind shear
   → Warm air to right of wind (NH)

2. JET STREAMS:
   - Polar jet: 30-60°N, ~10 km, 30-70+ m/s
   - Subtropical jet: 25-35°N, ~13 km, 30-50 m/s
   - Located at polar front / Hadley cell edge

3. JET STREAKS:
   - Embedded wind maxima
   - Four-quadrant model: Left-exit / Right-entrance
     favor rising motion → cyclogenesis, convection
   - Ageostrophic circulations drive vertical motion

4. ROSSBY WAVES:
   c = U - β/k² (phase speed)
   - Stationary at λ ~ 6000-8000 km (wavenumber 4-6)
   - Energy propagates eastward (group velocity)
   - Control weather patterns

5. BLOCKING:
   - Amplified, persistent ridges
   - Rex/Omega patterns
   - 5-30+ day duration
   - Extreme weather impacts

6. TROPOPAUSE:
   - Dynamic definition: PV = 1.5-2 PVU
   - Height: 8 km (poles) to 17 km (tropics)
   - Folds inject stratospheric air into troposphere

Upper-level dynamics drive surface weather!
""")

if __name__ == "__main__":
    print("\n[Jet Stream Dynamics Module - Complete]")
