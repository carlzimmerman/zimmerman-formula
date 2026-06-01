#!/usr/bin/env python3
"""
Lake Effect Snow Physics: First-Principles Derivations
========================================================

Complete physics of lake-enhanced precipitation.

Key phenomena:
- Heat and moisture fluxes over lakes
- Boundary layer modification
- Convective band organization
- Fetch and wind direction effects
- Orographic enhancement

Starting from air-sea interaction and convection theory.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
c_p = 1005            # Specific heat of air [J/kg/K]
L_v = 2.5e6           # Latent heat of vaporization [J/kg]
rho_air = 1.2         # Air density [kg/m³]
kappa = 0.4           # von Kármán constant

print("="*70)
print("LAKE EFFECT SNOW: FIRST-PRINCIPLES PHYSICS")
print("="*70)

#############################################
# PART 1: AIR-LAKE HEAT AND MOISTURE EXCHANGE
#############################################
print("\n" + "="*70)
print("PART 1: AIR-LAKE HEAT AND MOISTURE FLUXES")
print("="*70)

print("""
BULK AERODYNAMIC FORMULAS:
=========================

As cold air flows over relatively warm lake:

SENSIBLE HEAT FLUX:
    H = ρ c_p C_H U (T_lake - T_air)

LATENT HEAT FLUX:
    E = ρ L_v C_E U (q_sat(T_lake) - q_air)

Where:
    C_H, C_E ~ 1.5×10⁻³ (transfer coefficients)
    U = wind speed
    T_lake = lake surface temperature
    T_air = air temperature
    q_sat = saturation specific humidity at T_lake

LAKE-AIR TEMPERATURE DIFFERENCE:
Key parameter for lake effect intensity.
ΔT = T_lake - T_air

Thresholds:
    ΔT > 13°C (23°F): Lake effect likely
    ΔT > 17°C (30°F): Intense lake effect

BOWEN RATIO over lake (winter):
    β = H/E ~ 0.3-0.5 (evaporation dominates)

TOTAL HEAT FLUX:
    Q = H + E

Typical values over Great Lakes:
    H ~ 100-500 W/m²
    E ~ 200-800 W/m²
    Q_total ~ 300-1300 W/m²
""")

def saturation_specific_humidity(T_C, p=101325):
    """
    Calculate saturation specific humidity.

    q_s = 0.622 × e_s / (p - e_s)
    """
    e_s = 611.2 * np.exp(17.67 * T_C / (T_C + 243.5))
    return 0.622 * e_s / (p - e_s)

def sensible_heat_flux(T_lake_C, T_air_C, U, C_H=1.5e-3, rho=1.25):
    """
    Calculate sensible heat flux from lake to atmosphere.
    """
    return rho * c_p * C_H * U * (T_lake_C - T_air_C)

def latent_heat_flux(T_lake_C, T_air_C, RH_air, U, C_E=1.5e-3, rho=1.25):
    """
    Calculate latent heat flux (evaporation) from lake.
    """
    q_lake = saturation_specific_humidity(T_lake_C)
    q_air = RH_air / 100 * saturation_specific_humidity(T_air_C)

    return rho * L_v * C_E * U * (q_lake - q_air)

def total_heat_flux(T_lake_C, T_air_C, RH_air, U):
    """
    Total heat flux from lake surface.
    """
    H = sensible_heat_flux(T_lake_C, T_air_C, U)
    E = latent_heat_flux(T_lake_C, T_air_C, RH_air, U)
    return H, E, H + E

print("\nLake-atmosphere heat fluxes:")
print("-" * 70)
print(f"{'T_lake':>8s}  {'T_air':>8s}  {'ΔT':>6s}  {'U':>6s}  {'H':>10s}  {'E':>10s}  {'Total':>10s}")
print("-" * 70)

T_lake = 5  # °C (typical late fall Great Lake)
RH = 60  # %

for T_air in [0, -5, -10, -15, -20]:
    for U in [10, 15]:
        H, E, Q = total_heat_flux(T_lake, T_air, RH, U)
        dT = T_lake - T_air
        print(f"{T_lake:>8.0f}  {T_air:>8.0f}  {dT:>6.0f}  {U:>6.0f}  {H:>8.0f} W/m²  {E:>8.0f} W/m²  {Q:>8.0f} W/m²")

#############################################
# PART 2: BOUNDARY LAYER MODIFICATION
#############################################
print("\n" + "="*70)
print("PART 2: ATMOSPHERIC BOUNDARY LAYER OVER LAKE")
print("="*70)

print("""
BOUNDARY LAYER TRANSFORMATION:
=============================

Cold, stable continental air mass flows over warm lake.
Surface heating destabilizes the air:

CONVECTIVE BOUNDARY LAYER (CBL) GROWTH:
    dz_i/dt = (1 + 2A) × w_*³ / (g/θ × z_i × Δθ)

Where:
    z_i = CBL depth
    w_* = convective velocity scale = (g/θ × H × z_i)^(1/3)
    Δθ = potential temperature jump at CBL top
    A ~ 0.2 (entrainment parameter)

SIMPLIFIED GROWTH:
For distance X over lake with wind speed U:
    z_i(X) ≈ √(2 × Q × X / (ρ c_p U Δθ))

Or empirically:
    z_i ≈ 0.2 × (ΔT)^0.5 × X^0.5   [km, °C, km]

FETCH EFFECT:
Longer fetch → deeper CBL → more instability → more snow

Great Lakes fetches:
    Lake Erie: 50-300 km
    Lake Ontario: 50-300 km
    Lake Michigan: 150-500 km
    Lake Superior: 200-600 km
""")

def convective_velocity_scale(H, z_i, theta=280):
    """
    Calculate convective velocity scale w*.

    w* = (g/θ × H × z_i / (ρ c_p))^(1/3)
    """
    g_over_theta = g / theta
    return (g_over_theta * H * z_i / (rho_air * c_p))**(1/3)

def cbl_depth_over_fetch(fetch_km, U, Q_total, delta_theta=10):
    """
    Estimate convective boundary layer depth over lake.

    Simplified: z_i ~ sqrt(2 Q X / (ρ c_p U Δθ))
    """
    X = fetch_km * 1000  # Convert to m

    z_i = np.sqrt(2 * Q_total * X / (rho_air * c_p * U * delta_theta))

    return z_i  # meters

def lake_effect_potential(delta_T, fetch_km, U):
    """
    Simple lake effect potential index.

    Higher values = more intense lake effect.
    """
    # Requires ΔT > ~13°C for significant effect
    if delta_T < 10:
        return 0

    # Scale with ΔT, fetch, and moderate wind
    # Too much wind can disrupt bands

    dT_factor = (delta_T - 10) / 10
    fetch_factor = min(fetch_km / 200, 2)
    wind_factor = min(U / 10, 1) * max(0, 1 - (U - 20) / 20)

    return dT_factor * fetch_factor * wind_factor * 100

print("\nConvective boundary layer depth vs fetch:")
print("-" * 50)
U = 12  # m/s
Q = 700  # W/m²
print(f"  Wind speed: {U} m/s, Heat flux: {Q} W/m²")
print("-" * 50)

for fetch in [25, 50, 100, 150, 200, 300, 400]:
    z_i = cbl_depth_over_fetch(fetch, U, Q)
    print(f"  Fetch {fetch:3.0f} km: CBL depth = {z_i/1000:.2f} km")

print("\nLake effect potential index:")
print("-" * 45)
for dT in [10, 15, 20, 25]:
    for fetch in [50, 150, 300]:
        idx = lake_effect_potential(dT, fetch, 12)
        print(f"  ΔT={dT}°C, Fetch={fetch}km: Index = {idx:.0f}")

#############################################
# PART 3: CONVECTIVE BAND ORGANIZATION
#############################################
print("\n" + "="*70)
print("PART 3: LAKE EFFECT SNOW BAND TYPES")
print("="*70)

print("""
LAKE EFFECT BAND MORPHOLOGY:
===========================

1. WIND-PARALLEL BANDS (Type I):
   - Multiple bands parallel to wind
   - Form when wind crosses lake obliquely
   - Shoreline convergence less important
   - Spacing ~ 5-20 km (related to roll aspect ratio)

2. SHORE-PARALLEL BANDS (Type II):
   - Form parallel to downwind shore
   - Shoreline friction creates convergence
   - Often intense, localized
   - Land breeze enhancement possible

3. MID-LAKE BAND (Type III):
   - Single intense band along lake axis
   - Forms when winds aligned with long axis
   - Both shores contribute convergence
   - Most intense lake effect type
   - Can produce 2-5+ in/hr rates

ORGANIZATION CRITERIA:
Wind direction relative to lake axis determines type.

For mid-lake band:
    Wind within ~20° of long axis
    Fetch > 100 km
    ΔT > 15°C

ROLL CONVECTION:
Aspect ratio: λ/z_i ~ 2-3
Where λ = roll wavelength, z_i = CBL depth

For z_i = 2 km: λ ~ 4-6 km spacing
""")

def band_type_from_wind(wind_direction, lake_axis_direction):
    """
    Predict lake effect band type from wind direction.

    wind_direction: degrees (meteorological convention)
    lake_axis_direction: degrees
    """
    angle_diff = abs(wind_direction - lake_axis_direction) % 180

    if angle_diff < 20:
        return "Mid-lake band (Type III) - most intense"
    elif angle_diff < 45:
        return "Mixed/transitional"
    else:
        return "Wind-parallel rolls (Type I)"

def roll_wavelength(z_i, aspect_ratio=2.5):
    """
    Estimate convective roll wavelength.

    λ = aspect_ratio × z_i
    """
    return aspect_ratio * z_i

def convergence_speed(U, friction_reduction=0.3):
    """
    Estimate land-induced convergence.

    Wind slows over land → convergence at coast.
    """
    delta_U = U * friction_reduction
    # Convergence ~ ΔU / L_transition
    L = 10000  # Transition zone width ~10 km
    return delta_U / L

print("\nBand type prediction:")
print("-" * 60)
lake_axis = 70  # Lake Ontario ~ 70° (SW-NE)
print(f"Lake axis direction: {lake_axis}°")
print("-" * 60)
for wind_dir in [50, 70, 90, 120, 160, 200]:
    band_type = band_type_from_wind(wind_dir, lake_axis)
    print(f"  Wind {wind_dir:3.0f}°: {band_type}")

print("\nRoll spacing (convective wavelength):")
print("-" * 40)
for z_i in [1000, 1500, 2000, 2500, 3000]:
    lam = roll_wavelength(z_i)
    print(f"  CBL {z_i/1000:.1f} km: Roll spacing = {lam/1000:.1f} km")

#############################################
# PART 4: SNOWFALL RATE PHYSICS
#############################################
print("\n" + "="*70)
print("PART 4: PRECIPITATION RATE ESTIMATION")
print("="*70)

print("""
MOISTURE BUDGET FOR LAKE EFFECT:
===============================

PRECIPITATION = EVAPORATION + CONVERGENCE

EVAPORATION RATE:
    E = ρ L_v C_E U (q_s - q_a)

Convert to water equivalent:
    P_evap = E / (ρ_w L_v) × time

For E = 500 W/m²:
    P_evap = 500 / (1000 × 2.5e6) = 2×10⁻⁷ m/s = 0.7 mm/hr

CONVERGENCE CONTRIBUTION:
Moisture convergence in band can multiply effect:
    P_total = P_evap × convergence_factor

Convergence factors:
    Weak: 2-3×
    Moderate: 3-5×
    Strong (mid-lake band): 5-10×

SNOW-TO-LIQUID RATIO:
Lake effect snow is typically:
    12:1 to 20:1 (fluffy, cold)

Can be as high as 30:1 (very cold)
Or as low as 8:1 (warmer, near 0°C)

SNOWFALL RATE:
For 2 in/hr liquid equivalent at 15:1 ratio:
    Snowfall = 2 × 15 = 30 in/hr (extreme!)

More typical: 2-5 in/hr
""")

def evaporation_rate_liquid(E_Wm2):
    """
    Convert latent heat flux to evaporation rate.

    Returns mm/hr
    """
    rho_w = 1000  # kg/m³
    rate_ms = E_Wm2 / (rho_w * L_v)  # m/s
    return rate_ms * 1000 * 3600  # mm/hr

def precipitation_with_convergence(evap_rate_mmhr, convergence_factor):
    """
    Estimate precipitation rate including convergence enhancement.
    """
    return evap_rate_mmhr * convergence_factor

def snow_liquid_ratio(T_C):
    """
    Estimate snow-to-liquid ratio from temperature.

    Colder → fluffier snow → higher ratio
    """
    if T_C > -2:
        return 8
    elif T_C > -5:
        return 10
    elif T_C > -10:
        return 12
    elif T_C > -15:
        return 15
    elif T_C > -20:
        return 18
    else:
        return 20

def snowfall_rate(liquid_rate_mmhr, T_C):
    """
    Calculate snowfall rate in cm/hr.
    """
    ratio = snow_liquid_ratio(T_C)
    return liquid_rate_mmhr * ratio / 10  # mm to cm

print("\nEvaporation to precipitation:")
print("-" * 55)
print(f"{'E (W/m²)':>10s}  {'Evap rate':>12s}  {'Conv 5×':>12s}  {'Conv 10×':>12s}")
print("-" * 55)
for E in [200, 400, 600, 800, 1000]:
    evap = evaporation_rate_liquid(E)
    p5 = precipitation_with_convergence(evap, 5)
    p10 = precipitation_with_convergence(evap, 10)
    print(f"{E:>10.0f}  {evap:>10.1f} mm/hr  {p5:>10.1f} mm/hr  {p10:>10.1f} mm/hr")

print("\nSnowfall rates at different temperatures:")
print("-" * 50)
print(f"{'Liquid (mm/hr)':>15s}  {'T (°C)':>8s}  {'Ratio':>8s}  {'Snow (cm/hr)':>14s}")
print("-" * 50)
for liquid in [2, 5, 10]:
    for T in [-5, -10, -15, -20]:
        ratio = snow_liquid_ratio(T)
        snow = snowfall_rate(liquid, T)
        print(f"{liquid:>15.0f}  {T:>8.0f}  {ratio:>8.0f}  {snow:>14.1f}")

#############################################
# PART 5: OROGRAPHIC ENHANCEMENT
#############################################
print("\n" + "="*70)
print("PART 5: OROGRAPHIC ENHANCEMENT")
print("="*70)

print("""
TERRAIN EFFECTS ON LAKE EFFECT:
==============================

Downwind terrain can greatly enhance snowfall:

TUG HILL PLATEAU (east of Lake Ontario):
    Elevation: 500-600 m above lake
    Annual snowfall: 300-400+ inches
    Single storm: 50+ inches possible

PHYSICS:
1. Upslope lift forces additional condensation
2. w_orographic = U × slope

For U = 15 m/s, slope = 5%:
    w = 15 × 0.05 = 0.75 m/s (strong lift!)

ENHANCEMENT FACTOR:
    P_total = P_lake_effect × (1 + w_oro / w_convective)

Where w_convective ~ 1-2 m/s in lake effect bands

COLD AIR DAMMING:
Appalachians can dam cold air, enhancing:
    - Lake Erie effect over western NY
    - Prolonged cold air residence

ELEVATION DEPENDENCE:
Snowfall typically increases 10-20%
per 100 m elevation in lake effect zone.
""")

def orographic_vertical_velocity(U, slope_fraction):
    """
    Calculate vertical velocity from orographic lift.

    w = U × tan(θ) ≈ U × slope for small slopes
    """
    return U * slope_fraction

def orographic_enhancement(w_oro, w_convective=1.5):
    """
    Estimate orographic enhancement factor.
    """
    return 1 + w_oro / w_convective

def elevation_snowfall_adjustment(base_snowfall, elevation_diff_m):
    """
    Adjust snowfall for elevation.

    Assume 15% increase per 100 m
    """
    factor = 1 + 0.15 * (elevation_diff_m / 100)
    return base_snowfall * factor

print("\nOrographic enhancement:")
print("-" * 55)
print(f"{'U (m/s)':>10s}  {'Slope (%)':>12s}  {'w_oro (m/s)':>14s}  {'Enhancement':>14s}")
print("-" * 55)
for U in [10, 15, 20]:
    for slope in [2, 5, 10]:
        w_oro = orographic_vertical_velocity(U, slope/100)
        enh = orographic_enhancement(w_oro)
        print(f"{U:>10.0f}  {slope:>12.0f}  {w_oro:>14.2f}  {enh:>14.1f}×")

print("\nTug Hill enhancement example:")
print("-" * 45)
base_snow = 50  # cm at lakeshore
for elev in [0, 200, 400, 600]:
    adj_snow = elevation_snowfall_adjustment(base_snow, elev)
    print(f"  Elevation +{elev:3.0f} m: {adj_snow:.0f} cm ({adj_snow/2.54:.0f} in)")

#############################################
# PART 6: GREAT LAKES CLIMATOLOGY
#############################################
print("\n" + "="*70)
print("PART 6: GREAT LAKES LAKE EFFECT CLIMATOLOGY")
print("="*70)

print("""
GREAT LAKES SNOWBELT REGIONS:
============================

LAKE SUPERIOR:
    Keweenaw Peninsula: 200-300 in/year
    Upper Michigan: 150-250 in/year
    Long fetch, but lower lake temps

LAKE MICHIGAN:
    West Michigan (Muskegon-Grand Rapids): 70-120 in/year
    NW Indiana: 60-80 in/year
    Fetch varies with wind direction

LAKE HURON:
    Georgian Bay: 100-150 in/year
    Thumb of Michigan: 40-60 in/year

LAKE ERIE:
    Buffalo, NY: 90-100 in/year
    Cleveland, OH: 60-70 in/year
    Shortest fetch, shallowest lake
    Freezes most winters → reduced late-season effect

LAKE ONTARIO:
    Tug Hill: 200-400 in/year (record US snowfall)
    Syracuse: 120 in/year
    Deepest lake, rarely freezes → season extends into spring

ICE COVER EFFECT:
Ice suppresses lake effect by:
    1. Eliminating heat flux
    2. Stopping evaporation
    3. Removing instability source

Lake Erie often freezes by February → season ends
Lake Ontario rarely freezes → effects into April
""")

print("\nGreat Lakes characteristics:")
print("-" * 70)
lakes = [
    ("Superior", 82100, 406, 147, "Nov-Mar", "Rarely"),
    ("Michigan", 57800, 282, 85, "Nov-Feb", "Partial"),
    ("Huron", 59600, 229, 59, "Nov-Feb", "Partial"),
    ("Erie", 25700, 64, 19, "Nov-Jan", "Often"),
    ("Ontario", 19000, 244, 86, "Nov-Apr", "Rarely"),
]

print(f"{'Lake':>12s}  {'Area (km²)':>12s}  {'Max depth':>12s}  {'Avg depth':>12s}  {'LES Season':>12s}  {'Ice':>10s}")
print("-" * 70)
for name, area, max_d, avg_d, season, ice in lakes:
    print(f"{name:>12s}  {area:>12,d}  {max_d:>10.0f} m  {avg_d:>10.0f} m  {season:>12s}  {ice:>10s}")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("LAKE EFFECT SNOW PHYSICS SUMMARY")
print("="*70)
print("""
Key Physics:

1. AIR-LAKE EXCHANGE:
   H = ρ c_p C_H U (T_lake - T_air)
   E = ρ L_v C_E U (q_s - q_a)
   Threshold: ΔT > 13°C for significant effect

2. BOUNDARY LAYER:
   CBL grows with fetch: z_i ∝ √(Q × X)
   Longer fetch → deeper unstable layer
   Typical CBL: 1-3 km over Great Lakes

3. BAND ORGANIZATION:
   - Wind-parallel rolls: Wind oblique to lake
   - Shore-parallel bands: Coastal friction
   - Mid-lake band: Wind along axis (most intense)

4. SNOWFALL RATES:
   - Evaporation: 0.5-3 mm/hr liquid
   - Convergence multiplier: 3-10×
   - Snow ratio: 10:1 to 20:1
   - Rates: 2-5 in/hr typical, 10+ extreme

5. OROGRAPHIC ENHANCEMENT:
   - w_oro = U × slope
   - Tug Hill: 300-400 in/year
   - 15% increase per 100 m elevation

6. CLIMATOLOGY:
   - Erie: Shallowest, often freezes
   - Ontario: Deepest, rarely freezes → longest season
   - Superior: Coldest, longest fetch

Lake effect snow is a remarkable example of
atmosphere-surface coupling at mesoscales!
""")

if __name__ == "__main__":
    print("\n[Lake Effect Snow Physics Module - Complete]")
