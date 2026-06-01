#!/usr/bin/env python3
"""
Frontal Dynamics: First-Principles Derivations
================================================

Complete physics of atmospheric fronts and boundaries.

Key phenomena:
- Cold front structure and dynamics
- Warm front physics
- Occluded fronts
- Drylines
- Outflow boundaries
- Sea breeze fronts

Starting from density current theory and frontogenesis.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
Omega = 7.292e-5      # Earth's rotation rate [rad/s]
R_d = 287.05          # Gas constant for dry air [J/kg/K]
c_p = 1005            # Specific heat [J/kg/K]
rho_0 = 1.2           # Reference air density [kg/m³]

print("="*70)
print("FRONTAL DYNAMICS: FIRST-PRINCIPLES DERIVATIONS")
print("="*70)

#############################################
# PART 1: FRONTOGENESIS THEORY
#############################################
print("\n" + "="*70)
print("PART 1: FRONTOGENESIS FUNDAMENTALS")
print("="*70)

print("""
FRONTOGENESIS: Creation/intensification of fronts
=================================================

DEFINITION:
A front is a boundary between air masses of different density
(primarily temperature and moisture differences).

FRONTAL INTENSITY:
    |∇θ| = gradient of potential temperature

FRONTOGENESIS FUNCTION:
    F = d|∇θ|/dt

Positive F → frontogenesis (front strengthening)
Negative F → frontolysis (front weakening)

KINEMATIC FRONTOGENESIS (2D):
    F = (1/|∇θ|) × [-∂u/∂x (∂θ/∂x)² - ∂v/∂y (∂θ/∂y)²
        - (∂v/∂x + ∂u/∂y)(∂θ/∂x)(∂θ/∂y)]

COMPONENTS:
1. CONFLUENCE: Winds converging toward front
   → Packs isotherms together

2. SHEARING DEFORMATION: Wind parallel to front varies
   → Rotates isotherms toward front

3. TILTING: Vertical motion in baroclinic zone
   → Can create/destroy fronts

FRONTOGENESIS EQUATION:
    F = -[D₁ cos2β + D₂ sin2β]|∇θ|/2

Where:
    D₁ = ∂u/∂x - ∂v/∂y (stretching deformation)
    D₂ = ∂v/∂x + ∂u/∂y (shearing deformation)
    β = angle of isotherms to x-axis
""")

def frontogenesis_confluence(du_dx, dv_dy, dtheta_dx, dtheta_dy):
    """
    Calculate frontogenesis from confluent flow.

    F_conf = -du/dx (∂θ/∂x)² - dv/dy (∂θ/∂y)²
    """
    grad_theta_sq = dtheta_dx**2 + dtheta_dy**2
    if grad_theta_sq == 0:
        return 0

    return -(du_dx * dtheta_dx**2 + dv_dy * dtheta_dy**2) / np.sqrt(grad_theta_sq)

def frontogenesis_deformation(D1, D2, grad_theta, beta_deg):
    """
    Calculate frontogenesis from deformation.

    F = -[D₁ cos(2β) + D₂ sin(2β)] × |∇θ| / 2
    """
    beta = np.radians(beta_deg)
    return -(D1 * np.cos(2*beta) + D2 * np.sin(2*beta)) * grad_theta / 2

def coriolis_parameter(lat_deg):
    """f = 2Ω sin(φ)"""
    return 2 * Omega * np.sin(np.radians(lat_deg))

def thermal_wind_shear(dT_dx, depth_m, T_mean=280, lat_deg=45):
    """
    Calculate thermal wind shear from temperature gradient.

    |∂V/∂z| = (g/fT)|∇T|
    """
    f = coriolis_parameter(lat_deg)
    return g / (f * T_mean) * abs(dT_dx)

print("\nFrontogenesis from deformation:")
print("-" * 60)
print(f"{'D₁ (s⁻¹)':>12s}  {'β (deg)':>10s}  {'|∇θ| (K/km)':>12s}  {'F (K/km/hr)':>14s}")
print("-" * 60)

# Typical deformation values
for D1 in [1e-5, 2e-5, 3e-5]:
    for beta in [0, 45, 90]:
        grad_theta = 5 / 100000  # 5 K per 100 km
        F = frontogenesis_deformation(D1, 0, grad_theta, beta)
        F_hr = F * 3600 * 100000  # Convert to K/100km/hr
        print(f"{D1*1e5:>12.1f}  {beta:>10.0f}  {grad_theta*1e5:>12.1f}  {F_hr:>14.2f}")

#############################################
# PART 2: COLD FRONT DYNAMICS
#############################################
print("\n" + "="*70)
print("PART 2: COLD FRONT STRUCTURE")
print("="*70)

print("""
COLD FRONT: Dense cold air undercuts warm air
=============================================

DENSITY CURRENT MODEL:
Cold air acts like a gravity current:

    c = k √(g' H)

Where:
    c = front speed
    k ≈ 0.7-1.0 (empirical)
    g' = g Δρ/ρ = g Δθ/θ (reduced gravity)
    H = cold air depth

For ΔT = 10 K, θ = 290 K, H = 2 km:
    g' = 10 × 10 / 290 = 0.34 m/s²
    c = 0.7 × √(0.34 × 2000) = 18 m/s

COLD FRONT STRUCTURE:
    Slope: 1:50 to 1:100 (steeper than warm front)
    Width: 50-200 km (transition zone)
    Depth: 1-3 km (cold air mass)

KATABATIC COMPONENT:
Cold air "falls" under warm air.
Vertical motion at front:
    w = c × tan(slope)

For c = 15 m/s, slope = 1:75:
    w = 15 / 75 = 0.2 m/s

FRONTAL LIFTING:
Warm air forced to rise over cold dome.
Lifting rate = w_front + v_warm × tan(slope)

ANAFRONT vs KATAFRONT:
    Anafront: Upper flow toward cold air → strong lift
    Katafront: Upper flow toward warm air → weaker, more widespread
""")

def cold_front_speed(delta_theta, theta_mean, depth_m, k=0.7):
    """
    Calculate cold front speed from density current theory.

    c = k √(g' H)
    """
    g_prime = g * delta_theta / theta_mean
    return k * np.sqrt(g_prime * depth_m)

def frontal_slope_from_thermal_wind(delta_T, delta_z, lat_deg, front_normal_wind_diff):
    """
    Calculate frontal slope from thermal wind balance.

    tan(α) = f × Δu / (g × Δθ/θ)
    """
    f = coriolis_parameter(lat_deg)
    g_prime = g * delta_T / 280  # Using 280 K reference

    # Slope
    tan_alpha = f * front_normal_wind_diff / g_prime
    return np.degrees(np.arctan(tan_alpha)), tan_alpha

def lifting_rate_at_front(front_speed, slope_inverse, warm_air_speed=0):
    """
    Calculate vertical motion at cold front.

    w = (c + v_warm) × tan(slope)
    """
    tan_slope = 1 / slope_inverse
    return (front_speed + warm_air_speed) * tan_slope

print("\nCold front speed from density current theory:")
print("-" * 60)
print(f"{'ΔT (K)':>10s}  {'Depth (m)':>12s}  {'Speed (m/s)':>12s}  {'Speed (kt)':>12s}")
print("-" * 60)

for dT in [5, 8, 10, 12, 15]:
    for H in [1000, 1500, 2000, 2500]:
        c = cold_front_speed(dT, 285, H)
        print(f"{dT:>10.0f}  {H:>12.0f}  {c:>12.1f}  {c*1.944:>12.0f}")

print("\nLifting rate at cold front:")
print("-" * 50)
for c in [10, 15, 20]:
    for slope in [50, 75, 100]:
        w = lifting_rate_at_front(c, slope)
        print(f"  Speed {c} m/s, slope 1:{slope}: w = {w*100:.1f} cm/s")

#############################################
# PART 3: WARM FRONT DYNAMICS
#############################################
print("\n" + "="*70)
print("PART 3: WARM FRONT STRUCTURE")
print("="*70)

print("""
WARM FRONT: Warm air glides over retreating cold air
====================================================

STRUCTURE:
    Slope: 1:100 to 1:300 (gentler than cold front)
    Width: 200-500 km (broader transition)
    Precipitation: Stratiform, long duration

WHY GENTLER SLOPE?
1. Warm air is less dense → rises more easily
2. Friction slows surface warm air more than aloft
3. Cold air "anchored" to surface

ISENTROPIC LIFT:
Warm air rises along sloping isentropic surfaces:
    w_isen = v · ∇z_θ

Where z_θ = height of isentropic surface.

For slope 1:200 and v = 10 m/s toward front:
    w = 10 / 200 = 0.05 m/s = 5 cm/s

WARM FRONTAL PRECIPITATION:
    Distance from surface front where precip begins:
    x = H_cloud / tan(slope) = H_cloud × slope_inverse

For H_cloud = 3 km, slope 1:200:
    x = 3 × 200 = 600 km ahead of surface front

CLOUD SEQUENCE (approaching warm front):
    Cirrus (600+ km): Ice crystals at ~10 km
    Cirrostratus (400-600 km): Halos possible
    Altostratus (200-400 km): Sun obscured
    Nimbostratus (0-200 km): Steady rain/snow
""")

def warm_front_precip_distance(cloud_base_km, slope_inverse):
    """
    Distance ahead of surface front where precipitation begins.
    """
    return cloud_base_km * slope_inverse

def isentropic_lift(wind_toward_front, slope_inverse):
    """
    Calculate isentropic lifting rate.

    w = v / slope_inverse
    """
    return wind_toward_front / slope_inverse

def warm_front_precip_type(T_surface, T_850, thickness_1000_500):
    """
    Determine precipitation type at warm front.

    Based on temperature profile.
    """
    # Thickness method
    if thickness_1000_500 < 5400:
        return "Snow"
    elif thickness_1000_500 < 5460:
        # Check for warm nose
        if T_850 > 0 and T_surface < 0:
            return "Freezing rain"
        else:
            return "Snow/rain mix"
    else:
        return "Rain"

print("\nWarm front precipitation distances:")
print("-" * 55)
print(f"{'Slope':>10s}  {'Cloud base':>12s}  {'Precip distance':>16s}")
print("-" * 55)
for slope in [100, 150, 200, 250, 300]:
    for base in [2, 3, 4]:
        dist = warm_front_precip_distance(base, slope)
        print(f"  1:{slope:<6d}  {base:>10.0f} km  {dist:>14.0f} km")

print("\nIsentropic lift rates:")
print("-" * 45)
for v in [5, 10, 15, 20]:
    for slope in [100, 200, 300]:
        w = isentropic_lift(v, slope)
        print(f"  v={v} m/s, slope 1:{slope}: w = {w*100:.1f} cm/s")

#############################################
# PART 4: OCCLUDED FRONTS
#############################################
print("\n" + "="*70)
print("PART 4: OCCLUDED FRONTS")
print("="*70)

print("""
OCCLUSION: Cold front catches up to warm front
==============================================

PROCESS:
1. Cold front moves faster than warm front
2. Cold front "catches" warm front at triple point
3. Warm air lifted entirely off surface

TYPES:

COLD OCCLUSION (more common):
    Air behind cold front colder than ahead of warm front
    Cold front undercuts warm front
    Structure: Coldest → Cold → Warm (aloft)
    Common in interior continents

WARM OCCLUSION:
    Air behind cold front warmer than ahead of warm front
    Cold front rides over warm front
    Structure: Cold → Less cold → Warm (aloft)
    Common along West Coast (maritime)

TROWAL (TROugh of Warm Air ALoft):
    Ridge of warm air extending back from triple point
    Associated with enhanced precipitation
    3D structure important for forecasting

TRIPLE POINT:
    Junction of cold front, warm front, and occlusion
    Maximum baroclinicity
    Often location of new cyclone development (secondary cyclogenesis)
""")

def occlusion_type(T_cold_sector, T_cool_sector, T_warm_sector):
    """
    Determine occlusion type from temperatures.
    """
    if T_cold_sector < T_cool_sector:
        return "Cold occlusion"
    else:
        return "Warm occlusion"

def time_to_occlusion(front_separation_km, cold_front_speed, warm_front_speed):
    """
    Calculate time until occlusion.

    Time = distance / (v_cold - v_warm)
    """
    relative_speed = cold_front_speed - warm_front_speed
    if relative_speed <= 0:
        return float('inf')

    return front_separation_km / relative_speed / 3600  # hours

print("\nOcclusion type determination:")
print("-" * 55)
cases = [
    (-5, 2, 15, "Cold occlusion - Continental"),
    (5, 2, 12, "Warm occlusion - Maritime"),
    (-10, 0, 18, "Cold occlusion - Strong"),
    (8, 5, 15, "Warm occlusion - Weak"),
]
print(f"{'T_cold':>8s}  {'T_cool':>8s}  {'T_warm':>8s}  {'Type':>25s}")
print("-" * 55)
for t_cold, t_cool, t_warm, expected in cases:
    occ_type = occlusion_type(t_cold, t_cool, t_warm)
    print(f"{t_cold:>8.0f}  {t_cool:>8.0f}  {t_warm:>8.0f}  {occ_type:>25s}")

print("\nTime to occlusion:")
print("-" * 50)
for sep in [200, 400, 600]:
    for v_diff in [5, 10, 15]:
        v_cold = 15
        v_warm = 15 - v_diff
        t = time_to_occlusion(sep, v_cold, v_warm)
        print(f"  Separation {sep} km, Δv={v_diff} m/s: {t:.0f} hours")

#############################################
# PART 5: DRYLINES
#############################################
print("\n" + "="*70)
print("PART 5: DRYLINE PHYSICS")
print("="*70)

print("""
DRYLINE: Boundary between moist and dry air masses
==================================================

LOCATION:
    Primary: Southern Great Plains (TX, OK, KS)
    Secondary: Other semi-arid regions globally

FORMATION:
1. Gulf of Mexico moisture advects northward
2. Mexican Plateau air is hot and dry
3. Sharp moisture gradient develops

CHARACTERISTICS:
    Dewpoint drop: 15-30°F (8-17°C) over few km
    Temperature: Often similar on both sides
    Virtual temperature: Higher on moist side
        → Dryline is a density boundary

DIURNAL CYCLE:
    Morning: Dryline moves east (mixing, heating)
    Afternoon: Maximum eastward extent
    Evening: Retreats westward (stable layer)

CONVERGENCE:
    Density difference creates convergence
    Moist air slightly denser (higher ρ_v but lower T_v)
    Actually: moist air LESS dense at same T!
    But dryline convergence from differential heating

SEVERE WEATHER:
    Intersection with fronts = "triple point"
    Explosive convection development
    Classic tornado outbreak setup
""")

def dewpoint_gradient_dryline(Td_moist, Td_dry, distance_km):
    """
    Calculate dewpoint gradient across dryline.
    """
    return (Td_moist - Td_dry) / distance_km  # °C/km

def virtual_temperature(T_C, Td_C, p_hPa=1000):
    """
    Calculate virtual temperature.

    T_v = T × (1 + 0.61 r)
    """
    T_K = T_C + 273.15
    Td_K = Td_C + 273.15

    # Saturation vapor pressure at dewpoint
    e = 611.2 * np.exp(17.67 * Td_C / (Td_C + 243.5))

    # Mixing ratio
    r = 0.622 * e / (p_hPa * 100 - e)

    return T_K * (1 + 0.61 * r)

def dryline_density_contrast(T_moist, Td_moist, T_dry, Td_dry, p_hPa=925):
    """
    Calculate density contrast across dryline.
    """
    Tv_moist = virtual_temperature(T_moist, Td_moist, p_hPa)
    Tv_dry = virtual_temperature(T_dry, Td_dry, p_hPa)

    # Density from ideal gas law
    rho_moist = p_hPa * 100 / (R_d * Tv_moist)
    rho_dry = p_hPa * 100 / (R_d * Tv_dry)

    return rho_moist, rho_dry, (rho_moist - rho_dry) / rho_dry * 100

print("\nDryline moisture contrast:")
print("-" * 55)
print("Classic dryline scenario:")
print(f"  Moist side: T = 30°C, Td = 20°C")
print(f"  Dry side:   T = 35°C, Td = 5°C")

Tv_moist = virtual_temperature(30, 20)
Tv_dry = virtual_temperature(35, 5)
print(f"\n  Virtual T (moist): {Tv_moist:.1f} K")
print(f"  Virtual T (dry):   {Tv_dry:.1f} K")
print(f"  ΔT_v: {Tv_dry - Tv_moist:.1f} K")

rho_m, rho_d, contrast = dryline_density_contrast(30, 20, 35, 5)
print(f"\n  Density (moist): {rho_m:.4f} kg/m³")
print(f"  Density (dry):   {rho_d:.4f} kg/m³")
print(f"  Contrast: {contrast:.2f}%")

#############################################
# PART 6: OUTFLOW BOUNDARIES
#############################################
print("\n" + "="*70)
print("PART 6: OUTFLOW BOUNDARIES AND GUST FRONTS")
print("="*70)

print("""
OUTFLOW BOUNDARY: Cold air spreading from thunderstorm
======================================================

FORMATION:
Rain-cooled downdraft air reaches surface and spreads.

DENSITY CURRENT PHYSICS:
Same as cold front:
    c = k √(g' H)

Typical values:
    ΔT = 5-15 K (temperature drop)
    H = 0.5-2 km (outflow depth)
    c = 10-20 m/s (propagation speed)

STRUCTURE:
    Head: Leading edge, turbulent
    Body: Relatively steady cold air
    Wake: Mixing with environment

GUST FRONT:
    Wind shift: Often 45-90°
    Wind increase: 15-30+ kt gust
    Temperature drop: 5-15°C in minutes
    Pressure rise: 2-6 hPa (mesohigh)

RADAR SIGNATURE:
    Fine line (weak echo from insects/debris)
    Convergence on velocity
    Shelf cloud often visible

COLLISION DYNAMICS:
    Outflows collide → enhanced convergence
    Can trigger new convection
    Important for storm maintenance/propagation
""")

def outflow_speed(delta_T, depth_m, theta_mean=300, k=0.7):
    """
    Calculate outflow boundary propagation speed.
    """
    g_prime = g * delta_T / theta_mean
    return k * np.sqrt(g_prime * depth_m)

def outflow_head_height(depth_m, froude=1.0):
    """
    Calculate height of outflow head.

    Head typically 1.5-2× body depth
    """
    return depth_m * (1 + 0.5 / froude)

def time_to_collision(x_separation_km, speed1_ms, speed2_ms):
    """
    Time for two outflows to collide.
    """
    combined_speed = speed1_ms + speed2_ms
    return x_separation_km * 1000 / combined_speed / 60  # minutes

print("\nOutflow boundary characteristics:")
print("-" * 55)
print(f"{'ΔT (K)':>10s}  {'Depth (m)':>12s}  {'Speed (m/s)':>12s}  {'Speed (kt)':>12s}")
print("-" * 55)

for dT in [5, 8, 10, 12, 15]:
    for H in [500, 1000, 1500]:
        c = outflow_speed(dT, H)
        print(f"{dT:>10.0f}  {H:>12.0f}  {c:>12.1f}  {c*1.944:>12.0f}")

print("\nOutflow collision timing:")
print("-" * 50)
for sep in [10, 20, 30]:
    for c in [10, 15]:
        t = time_to_collision(sep, c, c)
        print(f"  Separation {sep} km, each at {c} m/s: Collision in {t:.0f} min")

#############################################
# PART 7: SEA BREEZE FRONTS
#############################################
print("\n" + "="*70)
print("PART 7: SEA BREEZE CIRCULATION")
print("="*70)

print("""
SEA BREEZE: Thermally-driven coastal circulation
================================================

DRIVING MECHANISM:
    Land heats faster than water during day
    → Lower pressure over land
    → Onshore flow develops

SEA BREEZE FRONT:
Leading edge of marine air advancing inland.

SPEED:
    c ≈ √(g' H) (density current)

Typical values:
    ΔT = 3-8 K
    H = 0.5-1 km
    c = 3-7 m/s

INLAND PENETRATION:
    Maximum: 20-50 km typical
    Up to 100 km in extreme cases
    Depends on synoptic flow

STRUCTURE:
    Depth: 500-1500 m
    Width: 10-30 km (frontal zone)
    Return flow: 1-2 km aloft

CONVECTION TRIGGERING:
    Sea breeze front provides lift
    Combined with daytime heating
    Florida: Sea breeze convergence → daily storms

SEA BREEZE FRONT CONVERGENCE:
Florida example: East and west coast sea breezes
    → Meet in center → intense convection
""")

def sea_breeze_speed(delta_T, depth_m=800, k=0.6):
    """
    Calculate sea breeze front speed.
    """
    g_prime = g * delta_T / 300
    return k * np.sqrt(g_prime * depth_m)

def inland_penetration(speed_ms, duration_hr):
    """
    Estimate inland penetration distance.
    """
    return speed_ms * duration_hr * 3600 / 1000  # km

def sea_breeze_return_flow_height(depth_m, ratio=2.5):
    """
    Estimate height of return flow.
    """
    return depth_m * ratio

print("\nSea breeze front characteristics:")
print("-" * 50)
for dT in [3, 5, 7, 10]:
    c = sea_breeze_speed(dT)
    penetration = inland_penetration(c, 6)
    print(f"  ΔT = {dT}°C: Speed = {c:.1f} m/s, 6-hr penetration = {penetration:.0f} km")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("FRONTAL DYNAMICS SUMMARY")
print("="*70)
print("""
Key Physics:

1. FRONTOGENESIS:
   F = d|∇θ|/dt
   Confluence + deformation → front intensification
   Tilting can create/destroy fronts

2. COLD FRONTS:
   Density current: c = k√(g'H)
   Slope: 1:50 to 1:100
   Speed: 10-25 m/s typical
   Strong lift, convective precipitation

3. WARM FRONTS:
   Isentropic lift: w = v × tan(slope)
   Slope: 1:100 to 1:300
   Stratiform precipitation, wide area
   Precip starts 400-600 km ahead

4. OCCLUDED FRONTS:
   Cold front overtakes warm front
   Cold vs warm occlusion types
   Triple point = cyclogenesis potential

5. DRYLINES:
   Moisture boundary, not temperature
   Virtual temperature contrast
   Severe weather trigger in Plains

6. OUTFLOW BOUNDARIES:
   Thunderstorm-generated density currents
   c = 10-20 m/s typical
   Collision → new convection

7. SEA BREEZE:
   Thermally-driven coastal circulation
   Inland penetration 20-50 km
   Convection triggering mechanism

Fronts are boundaries where weather happens!
""")

if __name__ == "__main__":
    print("\n[Frontal Dynamics Module - Complete]")
