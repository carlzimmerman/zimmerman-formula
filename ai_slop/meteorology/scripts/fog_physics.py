#!/usr/bin/env python3
"""
Fog Physics: First-Principles Derivations
==========================================

Complete physics of fog formation, persistence, and dissipation.

Key phenomena:
- Radiation fog
- Advection fog
- Upslope fog
- Steam fog
- Fog microphysics
- Visibility relationships

Starting from thermodynamics and microphysics.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
R_v = 461.5           # Gas constant for water vapor [J/kg/K]
R_d = 287.05          # Gas constant for dry air [J/kg/K]
c_p = 1005            # Specific heat of air [J/kg/K]
L_v = 2.5e6           # Latent heat of vaporization [J/kg]
rho_water = 1000      # Water density [kg/m³]
g = 9.81              # Gravitational acceleration [m/s²]
sigma = 5.67e-8       # Stefan-Boltzmann constant [W/m²/K⁴]

print("="*70)
print("FOG PHYSICS: FIRST-PRINCIPLES DERIVATIONS")
print("="*70)

#############################################
# PART 1: FOG FORMATION THERMODYNAMICS
#############################################
print("\n" + "="*70)
print("PART 1: FOG FORMATION THERMODYNAMICS")
print("="*70)

print("""
FOG DEFINITION AND BASIC PHYSICS:
================================

Fog = Cloud at the surface (visibility < 1000 m)
Mist = Visibility 1000-5000 m

SATURATION CONDITION:
Fog forms when T → T_d (temperature approaches dewpoint)

Two pathways:
1. Cool air to dewpoint (radiative, advective)
2. Add moisture (evaporative, mixing)

CLAUSIUS-CLAPEYRON EQUATION:
    de_s/dT = L_v e_s / (R_v T²)

Integrated form (Tetens):
    e_s(T) = 6.11 × exp[17.27 T / (T + 237.3)]

Where T in °C, e_s in hPa.

DEWPOINT DEPRESSION:
    T - T_d = (a/b) × ln(e_s(T)/e) ≈ (T - T_d) × 0.12 per 10%RH

COOLING RATE FOR FOG FORMATION:
    (T - T_d) = initial dewpoint depression
    Fog forms when T ≈ T_d (RH → 100%)

Required cooling depends on initial humidity.
""")

def saturation_vapor_pressure(T_C):
    """
    Saturation vapor pressure using Tetens formula.

    T_C: Temperature in Celsius
    Returns: e_s in Pa
    """
    return 611.2 * np.exp(17.67 * T_C / (T_C + 243.5))

def dewpoint_from_rh(T_C, RH):
    """
    Calculate dewpoint from temperature and relative humidity.
    """
    e = RH / 100 * saturation_vapor_pressure(T_C)
    # Invert Tetens formula
    T_d = 243.5 * np.log(e / 611.2) / (17.67 - np.log(e / 611.2))
    return T_d

def rh_from_dewpoint(T_C, T_d):
    """
    Calculate RH from temperature and dewpoint.
    """
    e_s = saturation_vapor_pressure(T_C)
    e = saturation_vapor_pressure(T_d)
    return 100 * e / e_s

def cooling_needed_for_fog(T_C, RH):
    """
    Calculate cooling required for fog formation.
    """
    T_d = dewpoint_from_rh(T_C, RH)
    return T_C - T_d  # Cooling needed in °C

print("\nCooling required for fog formation:")
print("-" * 50)
print(f"{'T (°C)':>8s}  {'RH (%)':>8s}  {'T_d (°C)':>10s}  {'Cooling (°C)':>12s}")
print("-" * 50)
for T in [15, 20]:
    for RH in [60, 70, 80, 90, 95]:
        T_d = dewpoint_from_rh(T, RH)
        cooling = T - T_d
        print(f"{T:>8.0f}  {RH:>8.0f}  {T_d:>10.1f}  {cooling:>12.1f}")

print("\n  Note: Higher humidity → less cooling needed!")

#############################################
# PART 2: RADIATION FOG
#############################################
print("\n" + "="*70)
print("PART 2: RADIATION FOG")
print("="*70)

print("""
RADIATION FOG FORMATION:
=======================

Forms on clear, calm nights through radiative cooling.

RADIATIVE COOLING RATE:
Surface energy balance at night:
    L↑ - L↓ - Q_G = ρ c_p h (dT/dt)

Net longwave loss: L_net = εσT⁴ - L↓

Clear sky L↓ approximation:
    L↓ ≈ εσT_air⁴ × (0.82 - 0.25 × 10^(-0.077 e))

Where e = vapor pressure [hPa]

COOLING RATE:
    dT/dt = (L↑ - L↓) / (ρ c_p h)

Typical nocturnal cooling: 2-5°C/night (clear, calm)

CONDITIONS FAVORING RADIATION FOG:
1. Clear sky (maximum L_net loss)
2. Light winds (0.5-3 m/s optimal)
3. High humidity (less cooling needed)
4. Long nights (more cooling time)
5. Moist soil (moisture source)

FOG FORMATION SEQUENCE:
1. Surface cools first
2. Ground fog forms
3. Deepens through turbulent mixing
4. "Lifts" at sunrise (becomes stratus)

TAYLOR (1917) FOG DEPTH:
    h_fog ≈ √(2 K_h t)

Where K_h = eddy diffusivity (~1 m²/s calm)
After 10 hours: h ~ 250 m
""")

def radiative_cooling_rate(T_surface, T_air, emissivity=0.95, vapor_pressure=10, h_layer=10):
    """
    Calculate nocturnal radiative cooling rate.

    Returns dT/dt in K/hour
    """
    T_s_K = T_surface + 273.15
    T_a_K = T_air + 273.15

    # Outgoing longwave
    L_up = emissivity * sigma * T_s_K**4

    # Incoming longwave (Brunt formula)
    e_hPa = vapor_pressure
    L_down = 0.96 * sigma * T_a_K**4 * (0.82 - 0.25 * 10**(-0.077 * e_hPa))

    # Net loss
    L_net = L_up - L_down

    # Cooling rate of layer
    rho = 1.2
    dT_dt = L_net / (rho * c_p * h_layer)  # K/s

    return dT_dt * 3600  # K/hour

def fog_depth_taylor(time_hours, K_h=1.0):
    """
    Taylor's fog depth model.

    h = √(2 K_h t)
    """
    t_s = time_hours * 3600
    return np.sqrt(2 * K_h * t_s)

def time_to_fog(T_initial, T_d, cooling_rate_per_hour):
    """
    Estimate time for fog formation.
    """
    depression = T_initial - T_d
    if cooling_rate_per_hour <= 0:
        return float('inf')
    return depression / cooling_rate_per_hour

print("\nRadiative cooling rates:")
print("-" * 55)
print(f"{'T_surface':>10s}  {'Humidity':>10s}  {'Cooling (°C/hr)':>16s}")
print("-" * 55)
for T in [10, 15, 20]:
    for e in [5, 10, 15]:
        rate = radiative_cooling_rate(T, T+5, vapor_pressure=e)
        print(f"{T:>10.0f}°C  {e:>10.0f} hPa  {rate:>16.2f}")

print("\nFog depth growth (Taylor model):")
print("-" * 40)
for t in [1, 2, 4, 6, 8, 10, 12]:
    h = fog_depth_taylor(t)
    print(f"  After {t:2.0f} hours: h = {h:.0f} m")

print("\nTime to fog formation:")
depression = 5  # °C dewpoint depression
for rate in [0.5, 1.0, 2.0]:
    t = time_to_fog(20, 15, rate)
    print(f"  Cooling {rate} °C/hr, T-Td={depression}°C: {t:.1f} hours")

#############################################
# PART 3: ADVECTION FOG
#############################################
print("\n" + "="*70)
print("PART 3: ADVECTION FOG")
print("="*70)

print("""
ADVECTION FOG PHYSICS:
=====================

Forms when warm, moist air flows over cold surface.

HEAT TRANSFER TO COLD SURFACE:
    Q_H = ρ c_p C_H U (T_air - T_surface)

Where C_H = heat transfer coefficient (~0.001-0.01)

COOLING OF AIR MASS:
    dT/dt = -Q_H / (ρ c_p h)
          = -C_H U (T_air - T_surface) / h

AIR MASS MODIFICATION:
As air travels distance x:
    T(x) = T_surface + (T_0 - T_surface) exp(-x/L)

Where L = h / C_H = fetch for temperature adjustment

SEA FOG (most common advection fog):
- Warm air over cold water (upwelling zones, cold currents)
- SST < T_d of incoming air → fog
- Very persistent (SST changes slowly)

Examples:
- San Francisco fog (California Current)
- Grand Banks fog (Labrador Current)
- Haar (North Sea, UK east coast)

DURATION:
Advection fog persists until:
1. Air mass changes
2. Wind increases (mixes fog away)
3. Surface warms (rare for ocean)
""")

def air_temperature_over_surface(x_km, T_initial, T_surface, C_H=0.002, U=5, h=500):
    """
    Air temperature modification as it travels over surface.

    T(x) = T_s + (T_0 - T_s) exp(-x/L)
    """
    L = h / C_H  # Adjustment length scale [m]
    x_m = x_km * 1000

    T = T_surface + (T_initial - T_surface) * np.exp(-x_m / L)
    return T

def distance_to_fog(T_air, T_d, T_surface, C_H=0.002, h=500):
    """
    Distance for air to cool to dewpoint (fog formation).
    """
    if T_air <= T_d:
        return 0  # Already saturated
    if T_surface >= T_d:
        return float('inf')  # Won't reach dewpoint

    L = h / C_H  # km
    # T_d = T_s + (T_0 - T_s) exp(-x/L)
    # exp(-x/L) = (T_d - T_s) / (T_0 - T_s)

    ratio = (T_d - T_surface) / (T_air - T_surface)
    if ratio <= 0:
        return float('inf')

    x = -L * np.log(ratio)
    return x / 1000  # Convert to km

print("\nAir temperature modification over cold surface:")
print("  T_air = 20°C, T_surface = 10°C, h = 500 m")
print("-" * 45)
for x in [0, 10, 50, 100, 200, 500]:
    T = air_temperature_over_surface(x, 20, 10)
    print(f"  x = {x:3.0f} km: T_air = {T:.1f}°C")

print("\nDistance to fog formation:")
print("  T_air = 20°C, T_d = 15°C")
print("-" * 45)
for T_s in [14, 12, 10, 8, 5]:
    x = distance_to_fog(20, 15, T_s)
    if x < float('inf'):
        print(f"  T_surface = {T_s}°C: x = {x:.0f} km")
    else:
        print(f"  T_surface = {T_s}°C: No fog (surface too warm)")

#############################################
# PART 4: UPSLOPE AND STEAM FOG
#############################################
print("\n" + "="*70)
print("PART 4: UPSLOPE AND STEAM FOG")
print("="*70)

print("""
UPSLOPE FOG:
============

Forms when air rises along terrain, cooling adiabatically.

DRY ADIABATIC LAPSE RATE:
    Γ_d = g/c_p ≈ 9.8°C/km

SATURATED (MOIST) ADIABATIC:
    Γ_s = Γ_d [1 + L_v q_s / (R_d T)] / [1 + L_v² q_s / (c_p R_v T²)]
    Γ_s ≈ 5-7°C/km (temperature dependent)

LIFTING CONDENSATION LEVEL (LCL):
Height at which rising air reaches saturation:
    z_LCL ≈ 125 × (T - T_d)  [meters]

If terrain forces air above LCL, fog/cloud forms.

STEAM FOG (SEA SMOKE):
======================

Forms when cold air moves over warm water.
Opposite of advection fog!

MECHANISM:
1. Water evaporates rapidly into cold air
2. Evaporation rate: E = C_E U (q_s(T_water) - q_air)
3. Mixing of warm, saturated air with cold air → supersaturation

CONDITIONS:
    T_water - T_air > 10°C typically
    Also called "Arctic sea smoke" or "steam devils"

MIXING FOG DIAGRAM:
When two air masses mix:
- Mixing is linear in (T, q)
- Saturation curve is convex
- Mixing line can cross saturation → fog

T_mix = (T_1 m_1 + T_2 m_2) / (m_1 + m_2)
q_mix = (q_1 m_1 + q_2 m_2) / (m_1 + m_2)

If q_mix > q_s(T_mix) → fog!
""")

def lifting_condensation_level(T_C, T_d_C):
    """
    Calculate LCL height.

    z_LCL ≈ 125 × (T - T_d) meters
    """
    return 125 * (T_C - T_d_C)

def moist_adiabatic_lapse_rate(T_C, p_hPa=1000):
    """
    Calculate saturated adiabatic lapse rate.
    """
    T_K = T_C + 273.15
    e_s = saturation_vapor_pressure(T_C)
    q_s = 0.622 * e_s / (p_hPa * 100 - e_s)

    gamma_d = g / c_p

    numerator = 1 + L_v * q_s / (R_d * T_K)
    denominator = 1 + L_v**2 * q_s / (c_p * R_v * T_K**2)

    return gamma_d * numerator / denominator * 1000  # K/km

def steam_fog_condition(T_water, T_air, RH_air):
    """
    Check if steam fog will form.

    Requires large air-water temperature difference.
    """
    T_d = dewpoint_from_rh(T_air, RH_air)
    diff = T_water - T_air

    if diff > 10:
        return True, f"Likely (ΔT = {diff:.0f}°C)"
    elif diff > 5:
        return True, f"Possible (ΔT = {diff:.0f}°C)"
    else:
        return False, f"Unlikely (ΔT = {diff:.0f}°C)"

print("\nLifting Condensation Level (LCL):")
print("-" * 40)
for T in [20, 25]:
    for RH in [50, 70, 90]:
        T_d = dewpoint_from_rh(T, RH)
        z = lifting_condensation_level(T, T_d)
        print(f"  T={T}°C, RH={RH}%: LCL = {z:.0f} m")

print("\nMoist adiabatic lapse rate:")
print("-" * 35)
for T in [0, 10, 20, 30]:
    gamma_s = moist_adiabatic_lapse_rate(T)
    print(f"  T = {T}°C: Γ_s = {gamma_s:.1f} °C/km")

print("\nSteam fog conditions (T_air = 0°C, RH = 80%):")
print("-" * 50)
for T_w in [5, 10, 15, 20]:
    fog, msg = steam_fog_condition(T_w, 0, 80)
    print(f"  T_water = {T_w}°C: {msg}")

#############################################
# PART 5: FOG MICROPHYSICS
#############################################
print("\n" + "="*70)
print("PART 5: FOG MICROPHYSICS")
print("="*70)

print("""
FOG DROPLET PHYSICS:
===================

FOG CHARACTERISTICS:
- Droplet diameter: 2-50 μm (typically 5-15 μm)
- Droplet concentration: 50-500 cm⁻³
- Liquid water content (LWC): 0.05-0.5 g/m³

NUMBER-SIZE DISTRIBUTION:
Often follows modified gamma or lognormal:
    n(D) = N_t × (D/D_m)^α × exp[-α(D/D_m)]

Where:
    N_t = total concentration
    D_m = modal diameter
    α = shape parameter

LIQUID WATER CONTENT:
    LWC = (π/6) ρ_w ∫ D³ n(D) dD
    LWC = (π/6) ρ_w N_t D_v³

Where D_v = volume mean diameter ≈ 1.2 D_m

DROPLET GROWTH:
Condensation rate on existing droplets:
    dm/dt = 4π r D_v (S - 1) F(r)

Where:
    S = supersaturation ratio
    D_v = diffusion coefficient
    F(r) = ventilation factor

FOG THICKENING:
As fog deepens, LWC increases:
    LWC ≈ 0.15 × (h/100)^0.5 g/m³

Where h = fog depth in meters.
""")

def fog_lwc_from_depth(h_m):
    """
    Estimate LWC from fog depth.

    Empirical relationship for mature radiation fog.
    """
    return 0.15 * (h_m / 100)**0.5

def droplet_fall_speed(diameter_um):
    """
    Stokes fall velocity for fog droplets.

    v = (ρ_w - ρ_a) g d² / (18 μ)
    """
    d = diameter_um * 1e-6  # Convert to m
    mu = 1.8e-5  # Dynamic viscosity of air
    rho_drop = 1000
    rho_air = 1.2

    v = (rho_drop - rho_air) * g * d**2 / (18 * mu)
    return v * 100  # cm/s

def lwc_from_droplets(N_cm3, D_v_um):
    """
    Calculate LWC from droplet properties.

    LWC = (π/6) ρ_w N D_v³
    """
    N = N_cm3 * 1e6  # Convert to /m³
    D = D_v_um * 1e-6  # Convert to m

    lwc = (np.pi / 6) * rho_water * N * D**3
    return lwc * 1000  # g/m³

print("\nFog droplet characteristics:")
print("-" * 50)
print(f"{'Diameter':>10s}  {'Fall speed':>12s}  {'Settling':>12s}")
print(f"{'(μm)':>10s}  {'(cm/s)':>12s}  {'(m/hr)':>12s}")
print("-" * 50)
for d in [5, 10, 15, 20, 30, 50]:
    v = droplet_fall_speed(d)
    settling = v / 100 * 3600  # m/hr
    print(f"{d:>10.0f}  {v:>12.4f}  {settling:>12.2f}")

print("\nLWC from droplet population:")
print("-" * 45)
for N in [100, 200, 300]:
    for D in [8, 12, 16]:
        lwc = lwc_from_droplets(N, D)
        print(f"  N={N}/cm³, D_v={D}μm: LWC = {lwc:.2f} g/m³")

print("\nLWC vs fog depth:")
print("-" * 30)
for h in [10, 50, 100, 200, 500]:
    lwc = fog_lwc_from_depth(h)
    print(f"  h = {h:3.0f} m: LWC = {lwc:.2f} g/m³")

#############################################
# PART 6: VISIBILITY IN FOG
#############################################
print("\n" + "="*70)
print("PART 6: VISIBILITY RELATIONSHIPS")
print("="*70)

print("""
VISIBILITY PHYSICS:
==================

EXTINCTION COEFFICIENT:
Light attenuation: I = I_0 exp(-β x)

Where β = extinction coefficient [1/m]

KOSCHMIEDER EQUATION:
Visibility (meteorological range):
    V = -ln(ε) / β ≈ 3.912 / β

Where ε = contrast threshold (typically 0.02-0.05)
Using ε = 0.02: V = 3.912 / β

EXTINCTION FROM DROPLETS:
    β = π/4 × N × D² × Q_ext

Where Q_ext ≈ 2 for fog droplets (geometric optics)

    β ≈ π/2 × N × D²

VISIBILITY-LWC RELATIONSHIP:
Empirical (Kunkel, 1984):
    V = 0.024 / LWC^0.65

Where V in km, LWC in g/m³

Or inversely:
    LWC = (0.024 / V)^1.54

FOG CATEGORIES:
Dense fog: V < 200 m
Thick fog: V < 400 m
Moderate fog: 400-1000 m
Mist: 1000-5000 m
""")

def visibility_from_lwc(LWC_gm3):
    """
    Calculate visibility from liquid water content.

    Kunkel (1984) empirical formula.
    V = 0.024 / LWC^0.65 (V in km)
    """
    if LWC_gm3 <= 0:
        return float('inf')
    return 0.024 / (LWC_gm3**0.65) * 1000  # Return in meters

def lwc_from_visibility(V_m):
    """
    Calculate LWC from visibility.

    Inverse of Kunkel formula.
    """
    V_km = V_m / 1000
    return (0.024 / V_km)**1.54

def extinction_from_droplets(N_cm3, D_um):
    """
    Calculate extinction coefficient from droplets.

    β = π/2 × N × D²
    """
    N = N_cm3 * 1e6  # /m³
    D = D_um * 1e-6  # m

    beta = (np.pi / 2) * N * D**2
    return beta

def visibility_from_extinction(beta):
    """
    Koschmieder equation.
    V = 3.912 / β
    """
    if beta <= 0:
        return float('inf')
    return 3.912 / beta

def fog_category(visibility_m):
    """
    Classify fog by visibility.
    """
    if visibility_m < 50:
        return "Very dense fog"
    elif visibility_m < 200:
        return "Dense fog"
    elif visibility_m < 400:
        return "Thick fog"
    elif visibility_m < 1000:
        return "Moderate fog"
    elif visibility_m < 5000:
        return "Mist"
    else:
        return "No fog"

print("\nVisibility-LWC relationship:")
print("-" * 50)
print(f"{'LWC (g/m³)':>12s}  {'Visibility (m)':>15s}  {'Category':>18s}")
print("-" * 50)
for lwc in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
    V = visibility_from_lwc(lwc)
    cat = fog_category(V)
    print(f"{lwc:>12.2f}  {V:>15.0f}  {cat:>18s}")

print("\nVisibility from droplet properties:")
print("-" * 55)
print(f"{'N (cm⁻³)':>10s}  {'D (μm)':>10s}  {'β (1/km)':>12s}  {'V (m)':>12s}")
print("-" * 55)
for N in [100, 300]:
    for D in [8, 12, 16]:
        beta = extinction_from_droplets(N, D)
        V = visibility_from_extinction(beta)
        print(f"{N:>10.0f}  {D:>10.0f}  {beta*1000:>12.2f}  {V:>12.0f}")

#############################################
# PART 7: FOG DISSIPATION
#############################################
print("\n" + "="*70)
print("PART 7: FOG DISSIPATION MECHANISMS")
print("="*70)

print("""
FOG DISSIPATION PHYSICS:
=======================

1. SOLAR HEATING (BURN-OFF):
   Solar radiation heats surface and fog top.
   Warming → RH drops → evaporation

   Heating rate in fog:
   dT/dt = (1-α) S_absorbed / (ρ c_p h)

   Where α = fog albedo (~0.2-0.4)

   TIME TO BURN-OFF:
   Depends on fog depth, LWC, solar intensity.
   Typical: 2-4 hours after sunrise for shallow fog.

2. TURBULENT MIXING (LIFTING):
   Increased wind → mixing with drier air above
   Fog "lifts off" to become stratus

   Critical wind threshold: ~3-5 m/s
   (Too much wind prevents fog forming; once formed,
   this wind will lift/mix it away)

3. ADVECTION:
   Replacement by drier air mass
   Or fog bank moves away

4. SURFACE WARMING:
   Ground heats faster than fog
   Creates superadiabatic layer
   Convective erosion from below

FOG PERSISTENCE FACTORS:
- Marine fog: Very persistent (cold SST maintains)
- Valley fog: Can persist for days (cold air drainage)
- Radiation fog: Usually clears by mid-morning
""")

def fog_burnoff_time(lwc_gm3, depth_m, solar_flux, albedo=0.3):
    """
    Estimate time for fog to burn off.

    Simplified: time = energy to evaporate / heating rate
    """
    # Energy needed to evaporate LWC
    total_lwc = lwc_gm3 * depth_m / 1000  # kg/m²
    energy_evap = total_lwc * L_v  # J/m²

    # Also need to warm the air
    rho = 1.2
    dT_needed = 3  # °C - approximate warming to break saturation
    energy_warm = rho * c_p * depth_m * dT_needed

    total_energy = energy_evap + energy_warm

    # Absorbed solar flux
    S_abs = (1 - albedo) * solar_flux

    # Time
    time_s = total_energy / S_abs
    return time_s / 3600  # hours

def mixing_dissipation_rate(wind_speed, fog_depth, zi=1000):
    """
    Estimate fog dissipation rate from turbulent mixing.

    Entrainment velocity: w_e ≈ 0.01 u*

    Returns: rate of fog depth decrease (m/hr)
    """
    # Friction velocity (simplified)
    u_star = 0.04 * wind_speed

    # Entrainment velocity
    w_e = 0.01 * u_star

    # But this mixes drier air from above, not direct depth reduction
    # Simplified: fog clears faster with more wind
    clearance_rate = w_e * 3600  # m/hr

    return clearance_rate

print("\nFog burn-off time estimates:")
print("-" * 60)
print(f"{'LWC':>8s}  {'Depth':>8s}  {'Solar flux':>12s}  {'Burn-off time':>15s}")
print("-" * 60)
for lwc in [0.1, 0.2, 0.3]:
    for h in [50, 100, 200]:
        for S in [200, 400, 600]:
            t = fog_burnoff_time(lwc, h, S)
            print(f"{lwc:>8.1f}  {h:>8.0f} m  {S:>10.0f} W/m²  {t:>13.1f} hr")

print("\nWind effect on fog (mixing dissipation):")
print("-" * 45)
for U in [1, 2, 3, 5, 7, 10]:
    rate = mixing_dissipation_rate(U, 100)
    if U <= 3:
        status = "Fog can persist"
    elif U <= 5:
        status = "Fog lifting likely"
    else:
        status = "Fog dissipates"
    print(f"  Wind {U} m/s: {status} (mix rate {rate:.0f} m/hr)")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("FOG PHYSICS SUMMARY")
print("="*70)
print("""
Key Physics and Relationships:

1. FOG FORMATION:
   - T → T_d (saturation required)
   - Cooling or moisture addition pathways
   - RH > 95-100% typically

2. RADIATION FOG:
   - Clear, calm nights
   - Cooling rate: 1-3 °C/hr typical
   - Depth grows: h ≈ √(2 K_h t)

3. ADVECTION FOG:
   - Warm moist air over cold surface
   - T_s < T_d triggers fog
   - Very persistent over ocean

4. UPSLOPE & STEAM FOG:
   - LCL ≈ 125 × (T - T_d) meters
   - Steam fog: T_water - T_air > 10°C

5. MICROPHYSICS:
   - Droplets: 5-15 μm typical
   - N: 100-300 cm⁻³
   - LWC: 0.05-0.5 g/m³

6. VISIBILITY:
   - V ≈ 0.024 / LWC^0.65 (V in km)
   - Dense fog: V < 200 m
   - Koschmieder: V = 3.912/β

7. DISSIPATION:
   - Solar burn-off (2-4 hr after sunrise)
   - Wind mixing (lifts to stratus)
   - Air mass change

Fog significantly impacts aviation, transportation,
and can persist for extended periods!
""")

if __name__ == "__main__":
    print("\n[Fog Physics Module - First Principles Complete]")
