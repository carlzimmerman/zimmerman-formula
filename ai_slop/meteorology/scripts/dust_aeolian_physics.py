#!/usr/bin/env python3
"""
Dust Storms and Aeolian Processes: First-Principles Derivations
================================================================

Complete physics of wind-blown particles and dust.

Key phenomena:
- Threshold wind speed for particle motion
- Saltation (bouncing grains)
- Suspension and dust devils
- Haboobs and dust storms
- Saharan dust transport

Starting from fluid mechanics and particle dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
rho_air = 1.225       # Air density at sea level [kg/m³]
nu = 1.5e-5           # Kinematic viscosity of air [m²/s]
rho_quartz = 2650     # Quartz density [kg/m³]
rho_mineral = 2500    # Typical mineral density [kg/m³]

print("="*70)
print("DUST STORMS AND AEOLIAN PROCESSES: FIRST-PRINCIPLES PHYSICS")
print("="*70)

#############################################
# PART 1: THRESHOLD WIND FOR PARTICLE MOTION
#############################################
print("\n" + "="*70)
print("PART 1: THRESHOLD WIND FOR PARTICLE ENTRAINMENT")
print("="*70)

print("""
DERIVATION FROM FORCE BALANCE:
=============================

Forces on particle resting on surface:

AERODYNAMIC FORCES:
1. Drag force: F_D = (1/2) ρ C_D A u²
2. Lift force: F_L = (1/2) ρ C_L A u²

RESISTING FORCES:
1. Weight: W = (4/3)π r³ ρ_p g
2. Cohesion: F_c (significant for d < 100 μm)

THRESHOLD CONDITION:
Particle moves when:
    Moment(lift+drag) > Moment(weight+cohesion)

BAGNOLD'S THRESHOLD FRICTION VELOCITY:
For dry, loose particles (d > 100 μm):

    u*_t = A √[(ρ_p - ρ_a)/ρ_a × g d]

Where:
    u* = friction velocity = √(τ/ρ)
    A ≈ 0.1 (empirical, Bagnold constant)
    d = particle diameter

THRESHOLD WIND SPEED (at 10m height):
Using log wind profile:
    U_10 = (u*/κ) ln(10/z₀)

Where κ = 0.4 (von Kármán), z₀ = roughness length.

FOR FINE PARTICLES (d < 100 μm):
Cohesive forces dominate → higher threshold.
Iversen-White modification includes cohesion.
""")

def threshold_friction_velocity(d_m, rho_p=rho_mineral, rho_a=rho_air):
    """
    Calculate threshold friction velocity for particle entrainment.

    Uses Bagnold formula with Shao-Lu modification for fine particles.

    Parameters:
        d_m: Particle diameter [m]
        rho_p: Particle density [kg/m³]
        rho_a: Air density [kg/m³]

    Returns:
        u*_t: Threshold friction velocity [m/s]
    """
    # Particle Reynolds number at threshold (iterative, use approximation)
    # For particles > 100 μm, Bagnold constant A ≈ 0.1

    # Shao-Lu (2000) scheme includes cohesion
    A_N = 0.0123  # Coefficient
    gamma = 3e-4  # Cohesion parameter [kg/s²]

    # Gravitational term
    grav_term = A_N * (rho_p * g * d_m + gamma/d_m) / rho_a

    u_star_t = np.sqrt(grav_term)

    return u_star_t

def wind_speed_from_ustar(u_star, z_m=10, z0=1e-4):
    """
    Convert friction velocity to wind speed at height z.

    Uses logarithmic wind profile (neutral stability).
    """
    kappa = 0.4  # von Kármán constant
    return (u_star / kappa) * np.log(z_m / z0)

def threshold_wind_speed(d_m, z_m=10, z0=1e-4, rho_p=rho_mineral):
    """
    Calculate threshold wind speed for entrainment.
    """
    u_star_t = threshold_friction_velocity(d_m, rho_p)
    return wind_speed_from_ustar(u_star_t, z_m, z0)

# Calculate threshold for various particle sizes
print("\nThreshold friction velocity and wind speed:")
print("-" * 65)
print(f"{'Diameter':>12s}  {'Category':>15s}  {'u*_t (m/s)':>12s}  {'U_10 (m/s)':>12s}")
print("-" * 65)

particle_sizes = [
    (10e-6, "Clay"),
    (50e-6, "Silt"),
    (100e-6, "Fine sand"),
    (200e-6, "Medium sand"),
    (500e-6, "Coarse sand"),
    (1000e-6, "Very coarse"),
    (2000e-6, "Granule")
]

for d, name in particle_sizes:
    u_star = threshold_friction_velocity(d)
    U_10 = threshold_wind_speed(d)
    print(f"{d*1e6:>10.0f} μm  {name:>15s}  {u_star:>12.3f}  {U_10:>12.1f}")

print("\n  Note: Fine particles need higher winds due to cohesion!")
print("  Optimal size for entrainment: ~80-100 μm")

#############################################
# PART 2: SALTATION PHYSICS
#############################################
print("\n" + "="*70)
print("PART 2: SALTATION - BOUNCING GRAIN TRANSPORT")
print("="*70)

print("""
SALTATION MECHANICS:
===================

Once entrained, sand grains follow ballistic trajectories:

EQUATIONS OF MOTION:
    m dv_x/dt = F_drag,x
    m dv_z/dt = F_drag,z - mg

DRAG FORCE:
    F_drag = (1/2) ρ_a C_D A |v_rel|² (in direction of v_rel)

CHARACTERISTIC SALTATION HEIGHT:
    h_salt ≈ u*²/g

For u* = 0.5 m/s: h ≈ 0.025 m = 2.5 cm

SALTATION LENGTH:
    L_salt ≈ 10-15 × h_salt

IMPACT VELOCITY:
Grains impact at ~10× u*, causing splash entrainment.

REPTATION:
Surface creep of larger particles pushed by saltation impacts.

SALTATION FLUX (Bagnold, 1941):
    q = C_B (ρ_a/g) u*³ √(d/D)

Where:
    C_B ≈ 1.5-2.8 (coefficient)
    D = 250 μm (reference diameter)
    q = mass flux [kg/m/s]

WHITE (1979) IMPROVED FORMULA:
    q = C_W (ρ_a/g) u*³ (1 - u*_t/u*)(1 + u*_t²/u*²)
""")

def saltation_height(u_star):
    """
    Characteristic saltation hop height.

    h = u*²/g (approximation from ballistic trajectory)
    """
    return u_star**2 / g

def saltation_length(u_star, coeff=12):
    """
    Characteristic saltation hop length.

    L ≈ 10-15 × h
    """
    h = saltation_height(u_star)
    return coeff * h

def saltation_flux_bagnold(u_star, d_m=200e-6, rho_a=rho_air):
    """
    Bagnold saltation flux formula.

    q = C (ρ/g) × (d/D)^0.5 × u*³

    Returns mass flux [kg/m/s]
    """
    C_B = 1.8  # Typical coefficient
    D_ref = 250e-6  # Reference diameter

    q = C_B * (rho_a / g) * np.sqrt(d_m / D_ref) * u_star**3

    return q

def saltation_flux_white(u_star, u_star_t, rho_a=rho_air):
    """
    White (1979) saltation flux formula.

    Accounts for threshold effects.
    """
    if u_star <= u_star_t:
        return 0

    C_W = 2.61  # White coefficient

    q = C_W * (rho_a / g) * u_star**3 * \
        (1 - u_star_t/u_star) * (1 + (u_star_t/u_star)**2)

    return q

print("\nSaltation characteristics vs friction velocity:")
print("-" * 60)
print(f"{'u* (m/s)':>10s}  {'Height (cm)':>12s}  {'Length (cm)':>12s}  {'Flux (kg/m/s)':>14s}")
print("-" * 60)

u_star_t = threshold_friction_velocity(200e-6)
for u_star in [0.25, 0.35, 0.5, 0.75, 1.0, 1.5]:
    h = saltation_height(u_star) * 100  # cm
    L = saltation_length(u_star) * 100  # cm
    q = saltation_flux_white(u_star, u_star_t)
    print(f"{u_star:>10.2f}  {h:>12.2f}  {L:>12.1f}  {q:>14.4f}")

print(f"\n  Threshold u*_t = {u_star_t:.3f} m/s for 200 μm sand")

#############################################
# PART 3: SUSPENSION AND DUST CONCENTRATION
#############################################
print("\n" + "="*70)
print("PART 3: SUSPENSION - DUST IN THE ATMOSPHERE")
print("="*70)

print("""
SUSPENSION CRITERION:
====================

Particle remains suspended when:
    Turbulent vertical velocity > Fall velocity
    w' > w_s

STOKES SETTLING VELOCITY (laminar flow, Re < 1):
    w_s = (ρ_p - ρ_a) g d² / (18 μ)

For d = 10 μm (dust): w_s ≈ 0.003 m/s
For d = 100 μm (fine sand): w_s ≈ 0.7 m/s

SUSPENSION PARAMETER:
    z_s = w_s / (κ u*)

Suspension occurs when z_s < 1
(Turbulent mixing faster than settling)

DUST CONCENTRATION PROFILE:
Rouse equation for equilibrium:

    C(z)/C_a = [(H-z)/z × a/(H-a)]^(w_s/κu*)

Where:
    C_a = concentration at reference height a
    H = mixing layer height

DUST EMISSION FLUX:
DPM (Dust Production Model):
    F = α × q × (1 - A_s)

Where:
    q = saltation flux
    α = sandblasting efficiency (~10⁻⁵ for sand)
    A_s = soil armoring factor
""")

def stokes_settling_velocity(d_m, rho_p=rho_mineral, rho_a=rho_air, mu=1.8e-5):
    """
    Stokes law settling velocity for small particles.

    Valid for Re < 1 (roughly d < 100 μm)
    """
    w_s = (rho_p - rho_a) * g * d_m**2 / (18 * mu)
    return w_s

def settling_velocity(d_m, rho_p=rho_mineral, rho_a=rho_air):
    """
    Settling velocity with drag coefficient correction.

    Uses iterative solution for larger particles.
    """
    mu = 1.8e-5  # Dynamic viscosity

    # Start with Stokes
    w_s = stokes_settling_velocity(d_m, rho_p, rho_a, mu)

    # Check Reynolds number and iterate
    for _ in range(10):
        Re = rho_a * w_s * d_m / mu

        if Re < 1:
            # Stokes regime
            C_D = 24 / Re
        elif Re < 1000:
            # Transition regime
            C_D = 24/Re * (1 + 0.15 * Re**0.687)
        else:
            # Newton regime
            C_D = 0.44

        # Update velocity
        w_s_new = np.sqrt(4 * (rho_p - rho_a) * g * d_m / (3 * C_D * rho_a))

        if abs(w_s_new - w_s) / w_s < 0.01:
            break
        w_s = w_s_new

    return w_s

def suspension_parameter(d_m, u_star, rho_p=rho_mineral):
    """
    Calculate Rouse number / suspension parameter.

    z_s = w_s / (κ u*)

    z_s < 0.8: Wash load (well mixed)
    0.8 < z_s < 1.2: Suspended load
    1.2 < z_s < 2.5: Saltation/suspension
    z_s > 2.5: Bedload only
    """
    w_s = settling_velocity(d_m, rho_p)
    kappa = 0.4

    return w_s / (kappa * u_star)

print("\nSettling velocity and suspension behavior:")
print("-" * 70)
print(f"{'Diameter':>10s}  {'w_s (m/s)':>12s}  {'z_s (u*=0.5)':>14s}  {'Transport mode':>18s}")
print("-" * 70)

particle_data = [
    (1e-6, "PM1"),
    (2.5e-6, "PM2.5"),
    (10e-6, "PM10"),
    (20e-6, "Fine dust"),
    (50e-6, "Coarse dust"),
    (100e-6, "Fine sand"),
    (200e-6, "Medium sand"),
    (500e-6, "Coarse sand")
]

u_star_ref = 0.5
for d, name in particle_data:
    w_s = settling_velocity(d)
    z_s = suspension_parameter(d, u_star_ref)

    if z_s < 0.8:
        mode = "Wash load"
    elif z_s < 1.2:
        mode = "Suspension"
    elif z_s < 2.5:
        mode = "Mixed"
    else:
        mode = "Saltation/bedload"

    print(f"{d*1e6:>8.1f} μm  {w_s:>12.4f}  {z_s:>14.2f}  {mode:>18s}")

#############################################
# PART 4: DUST DEVILS AND CONVECTIVE VORTICES
#############################################
print("\n" + "="*70)
print("PART 4: DUST DEVILS")
print("="*70)

print("""
DUST DEVIL PHYSICS:
==================

Dust devils form from:
1. Strong surface heating → superadiabatic layer
2. Ambient vertical vorticity (background rotation)
3. Stretching of vortex tube

THERMAL CIRCULATION:
Hot surface → buoyant plume → convergence at base

ANGULAR MOMENTUM CONSERVATION:
    r₁ v₁ = r₂ v₂

As air converges (r decreases), v increases.

CYCLOSTROPHIC BALANCE:
In the vortex:
    v²/r = (1/ρ) ∂p/∂r

TANGENTIAL VELOCITY PROFILE:
    v(r) = Γ/(2πr) × [1 - exp(-(r/r₀)²)]

Rankine vortex model (solid body core + potential flow outer).

PRESSURE DROP:
    Δp = ρ v_max² / 2

For v_max = 20 m/s: Δp ≈ 250 Pa (2.5 hPa)

TYPICAL DUST DEVIL:
- Diameter: 1-10 m (up to 100 m for large ones)
- Height: 10-1000 m
- Lifetime: 1-20 minutes
- Tangential speed: 10-25 m/s
""")

def dust_devil_pressure_drop(v_max, rho_a=rho_air):
    """
    Estimate central pressure drop in dust devil.

    From cyclostrophic balance.
    """
    return 0.5 * rho_a * v_max**2

def dust_devil_radius_from_intensity(v_max, circulation):
    """
    Estimate radius of maximum winds from circulation.

    v = Γ/(2πr) at outer edge → r = Γ/(2πv)
    """
    return circulation / (2 * np.pi * v_max)

def surface_sensible_heat_flux(T_surface, T_air, u_star=0.3, rho=1.2, cp=1005):
    """
    Surface sensible heat flux driving convection.

    H = ρ c_p C_H U (T_s - T_a)
    """
    C_H = 0.01  # Heat transfer coefficient (unstable)
    U = u_star * 25  # Approximate wind at reference height

    return rho * cp * C_H * U * (T_surface - T_air)

print("\nDust devil characteristics:")
print("-" * 50)
print(f"{'v_max (m/s)':>12s}  {'Δp (Pa)':>10s}  {'Δp (hPa)':>10s}")
print("-" * 50)
for v_max in [5, 10, 15, 20, 25, 30]:
    dp = dust_devil_pressure_drop(v_max)
    print(f"{v_max:>12.0f}  {dp:>10.1f}  {dp/100:>10.2f}")

print("\nTypical formation conditions:")
print(f"  Surface heat flux: {surface_sensible_heat_flux(60+273, 35+273):.0f} W/m²")
print(f"  (T_surface = 60°C, T_air = 35°C)")

#############################################
# PART 5: HABOOBS AND DUST STORMS
#############################################
print("\n" + "="*70)
print("PART 5: HABOOBS AND MAJOR DUST STORMS")
print("="*70)

print("""
HABOOB PHYSICS (Thunderstorm-driven dust wall):
==============================================

Cold pool from thunderstorm downdraft spreads at surface:

COLD POOL DENSITY CURRENT:
    c = k √(g' h)

Where:
    g' = g Δθ/θ (reduced gravity)
    h = cold pool depth
    k ≈ 0.7-1.0

GUST FRONT WIND SPEED:
Peak winds at leading edge can exceed 25 m/s.
Sharp pressure rise, temperature drop.

DUST WALL:
Vertical extent: 500-2000 m
Horizontal extent: 10-100 km wide
Visibility: <100 m in severe cases

SYNOPTIC DUST STORMS:
=====================
Large-scale pressure gradients drive:
- Strong geostrophic winds
- Frontal passages
- Shamal (Iraq/Kuwait summer)
- Harmattan (West Africa)

SAHARAN DUST TRANSPORT:
Dust lifted over Sahara transported by:
1. Saharan Air Layer (SAL): 850-500 hPa
2. African Easterly Jet (AEJ)
3. Trade wind inversion traps dust

Travel 5000+ km across Atlantic.
~500 million tons/year fertilize Amazon!
""")

def cold_pool_speed(delta_theta, theta_mean, depth_m):
    """
    Cold pool propagation speed from density current theory.

    c = k √(g' h) where g' = g Δθ/θ
    """
    k = 0.75  # Empirical coefficient
    g_prime = g * delta_theta / theta_mean

    return k * np.sqrt(g_prime * depth_m)

def haboob_visibility(dust_concentration_mg_m3, extinction_coeff=0.1):
    """
    Estimate visibility in dust storm.

    Koschmieder equation: V = 3.912 / β
    Where β = extinction coefficient [1/km]
    """
    # Extinction ~ concentration × mass extinction efficiency
    # Typical k_ext ~ 0.5-1.0 m²/g for dust
    k_ext = 0.7  # m²/g

    beta = k_ext * dust_concentration_mg_m3 / 1000  # 1/m
    beta_km = beta * 1000  # 1/km

    visibility_km = 3.912 / beta_km

    return visibility_km * 1000  # Return in meters

def dust_transport_rate(wind_speed_10m, fetch_km, erodibility=1e-5):
    """
    Simplified dust emission based on wind speed.

    Returns g/m²/s
    """
    # Threshold (approximately)
    u_t = 6.5  # m/s at 10m

    if wind_speed_10m < u_t:
        return 0

    # Simplified emission proportional to u*³ above threshold
    u_star = wind_speed_10m * 0.04  # Rough approximation
    u_star_t = u_t * 0.04

    emission = erodibility * (u_star - u_star_t)**3 * np.sqrt(fetch_km)

    return emission

print("\nCold pool / haboob gust front speed:")
print("-" * 50)
print(f"{'ΔT (K)':>8s}  {'Depth (m)':>10s}  {'Speed (m/s)':>12s}")
print("-" * 50)
theta_mean = 310  # K
for dT in [5, 8, 10, 12, 15]:
    for h in [500, 1000]:
        c = cold_pool_speed(dT, theta_mean, h)
        print(f"{dT:>8.0f}  {h:>10.0f}  {c:>12.1f}")

print("\nVisibility vs dust concentration:")
print("-" * 40)
for conc in [0.1, 0.5, 1, 2, 5, 10, 20]:
    vis = haboob_visibility(conc)
    print(f"  {conc:>5.1f} mg/m³:  Visibility = {vis/1000:.2f} km")

#############################################
# PART 6: SAHARAN AIR LAYER
#############################################
print("\n" + "="*70)
print("PART 6: SAHARAN AIR LAYER AND LONG-RANGE TRANSPORT")
print("="*70)

print("""
SAHARAN AIR LAYER (SAL) CHARACTERISTICS:
=======================================

A hot, dry, dust-laden layer over tropical Atlantic:

VERTICAL STRUCTURE:
- Base: ~850 hPa (trade wind inversion top)
- Top: ~500-600 hPa
- Thickness: 2-4 km

THERMODYNAMIC PROPERTIES:
- θ ≈ 40-45°C (very warm)
- RH: 10-30% (extremely dry)
- Strong inversion caps layer

DUST LOADING:
- AOD (Aerosol Optical Depth): 0.3-1.0+
- Mass concentration: 100-1000 μg/m³

TRANSPORT MECHANISM:
1. Surface heating lifts dust to 5-6 km over Sahara
2. Harmattan / trade winds transport westward
3. African Easterly Jet (~650 hPa) provides momentum
4. Takes 5-7 days to cross Atlantic

IMPACTS:
- Hurricane suppression (dry air entrainment, shear)
- Reduced visibility in Caribbean/SE USA
- Ocean fertilization (iron)
- Coral reef impacts
- Amazon fertilization (phosphorus)
""")

def saharan_dust_optical_depth(dust_column_mg_m2, mass_ext_eff=0.6):
    """
    Calculate aerosol optical depth from dust column.

    AOD = column × mass extinction efficiency
    """
    # Typical mass extinction efficiency for Saharan dust
    # ~0.5-0.8 m²/g at 550 nm
    return dust_column_mg_m2 * 1e-6 * mass_ext_eff * 1e3  # Account for units

def dust_settling_distance(particle_diameter_m, wind_speed, layer_height=3000):
    """
    Estimate how far dust can travel before settling out.

    Distance = wind_speed × residence_time
    residence_time = layer_height / settling_velocity
    """
    w_s = settling_velocity(particle_diameter_m)
    residence_time = layer_height / w_s  # seconds
    distance = wind_speed * residence_time  # meters

    return distance / 1000  # km

print("\nDust travel distance by particle size:")
print("-" * 55)
print(f"{'Diameter (μm)':>15s}  {'w_s (m/s)':>12s}  {'Travel dist (km)':>18s}")
print("-" * 55)

wind = 10  # m/s average
for d_um in [1, 2, 5, 10, 20, 50, 100]:
    d_m = d_um * 1e-6
    w_s = settling_velocity(d_m)
    dist = dust_settling_distance(d_m, wind)
    print(f"{d_um:>15.0f}  {w_s:>12.5f}  {dist:>18.0f}")

print("\n  Only particles < 20 μm can cross Atlantic (~5000 km)!")
print("  PM10 and PM2.5 travel farthest.")

#############################################
# PART 7: DUST RADIATIVE EFFECTS
#############################################
print("\n" + "="*70)
print("PART 7: RADIATIVE EFFECTS OF DUST")
print("="*70)

print("""
DUST-RADIATION INTERACTIONS:
===========================

Dust affects climate through:

1. SHORTWAVE (Solar) SCATTERING AND ABSORPTION:
   - Scattering: Cools surface (like aerosol indirect effect)
   - Absorption: Warms dust layer, cools surface

   Radiative forcing: ΔF ≈ -25 × AOD [W/m²] (globally averaged)

2. LONGWAVE (Thermal) ABSORPTION AND EMISSION:
   - Absorbs surface LW radiation
   - Re-emits at dust layer temperature (cooler)
   - Net effect: Warms surface at night

3. SEMI-DIRECT EFFECT:
   - Warming of dust layer changes stability
   - Can suppress or enhance convection

DUST RADIATIVE FORCING ESTIMATE:
Direct forcing at TOA:
    ΔF ≈ -Q_ext × S × (1-A_c) × [β(1-R_s)² - 4R_s × ω₀(1-ω₀)]

Where:
    Q_ext = extinction efficiency
    S = solar flux (~1361/4 W/m²)
    A_c = cloud fraction
    β = upscatter fraction
    R_s = surface reflectivity
    ω₀ = single scattering albedo

Over bright desert: Can be positive (warming)!
Over ocean: Strongly negative (cooling)
""")

def dust_shortwave_forcing(AOD, surface_albedo=0.1, omega=0.92, asym_param=0.7):
    """
    Estimate shortwave radiative forcing from dust.

    Simplified Charlson/Haywood formula.
    """
    S0 = 1361  # Solar constant [W/m²]
    f_s = 0.5  # Daylight fraction
    T_atm = 0.76  # Atmospheric transmittance

    # Upscatter fraction
    beta = 0.5 * (1 - asym_param)

    # Forcing per unit AOD
    delta_F = -S0/4 * f_s * T_atm**2 * (1 - 0.5) * AOD * \
              (omega * (1 - surface_albedo)**2 * beta - \
               4 * surface_albedo * (1 - omega))

    return delta_F

def dust_heating_rate(AOD, layer_thickness=3000, omega=0.92):
    """
    Estimate heating rate in dust layer.

    dT/dt = (1/ρcp) × (absorbed flux / layer thickness)
    """
    S0 = 1361 / 4  # Average solar flux
    T_atm = 0.76

    # Absorbed fraction
    absorbed = S0 * T_atm * AOD * (1 - omega)

    # Heating rate (K/day)
    rho_cp = 1.2 * 1005 * layer_thickness  # J/m²/K
    dT_dt = absorbed / rho_cp * 86400  # K/day

    return dT_dt

print("\nDust shortwave radiative forcing:")
print("-" * 55)
print(f"{'AOD':>6s}  {'Ocean (alb=0.06)':>18s}  {'Desert (alb=0.35)':>18s}")
print("-" * 55)
for aod in [0.1, 0.2, 0.3, 0.5, 1.0]:
    f_ocean = dust_shortwave_forcing(aod, surface_albedo=0.06)
    f_desert = dust_shortwave_forcing(aod, surface_albedo=0.35)
    print(f"{aod:>6.1f}  {f_ocean:>16.1f} W/m²  {f_desert:>16.1f} W/m²")

print("\n  Dust cools ocean but can warm bright desert!")

print("\nDust layer heating rate:")
for aod in [0.3, 0.5, 1.0]:
    dT = dust_heating_rate(aod)
    print(f"  AOD = {aod}: Heating = {dT:.2f} K/day")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("DUST AND AEOLIAN PHYSICS SUMMARY")
print("="*70)
print("""
Key Principles and Results:

1. THRESHOLD FOR MOTION: u*_t = A√[(ρ_p/ρ_a)gd]
   - Minimum for ~100 μm sand
   - Fines need more wind (cohesion)
   - Coarse needs more wind (weight)

2. SALTATION: Bouncing grain transport
   - Height h ≈ u*²/g
   - Flux q ∝ u*³
   - Drives dust emission via sandblasting

3. SUSPENSION: When w_s < κu*
   - PM10 stays suspended for days
   - Larger particles settle quickly
   - Concentration profile follows Rouse equation

4. DUST DEVILS: Convective vortices
   - Form in superadiabatic layer
   - v ∝ 1/r (angular momentum)
   - Δp ≈ ρv²/2 central drop

5. HABOOBS: Thunderstorm-driven dust walls
   - Cold pool speeds: 10-25 m/s
   - Visibility can drop to <100 m
   - Density current dynamics

6. SAHARAN AIR LAYER: Long-range transport
   - Only fine particles (< 20 μm) cross Atlantic
   - ~500 Mt/year leave Sahara
   - Fertilizes Amazon, affects hurricanes

7. RADIATIVE EFFECTS:
   - Cooling over ocean (scattering)
   - Possible warming over desert (absorption)
   - Heats dust layer 1-3 K/day

Dust is a major player in Earth system!
""")

if __name__ == "__main__":
    print("\n[Dust and Aeolian Physics Module - First Principles Complete]")
