#!/usr/bin/env python3
"""
Urban Meteorology: First-Principles Derivations
================================================

Complete physics of urban climate and atmospheric processes.

Key phenomena:
- Urban Heat Island (UHI)
- Urban boundary layer
- Pollution dispersion
- Urban precipitation effects
- Building aerodynamics

Starting from energy balance and turbulence theory.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
sigma = 5.67e-8       # Stefan-Boltzmann constant [W/m²/K⁴]
rho_air = 1.2         # Air density [kg/m³]
c_p = 1005            # Specific heat of air [J/kg/K]
kappa = 0.4           # von Kármán constant
L_v = 2.5e6           # Latent heat of vaporization [J/kg]

print("="*70)
print("URBAN METEOROLOGY: FIRST-PRINCIPLES PHYSICS")
print("="*70)

#############################################
# PART 1: URBAN ENERGY BALANCE
#############################################
print("\n" + "="*70)
print("PART 1: URBAN ENERGY BALANCE")
print("="*70)

print("""
URBAN SURFACE ENERGY BALANCE:
============================

Q* + Q_F = Q_H + Q_E + ΔQ_S

Where:
    Q* = Net radiation
    Q_F = Anthropogenic heat flux
    Q_H = Sensible heat flux
    Q_E = Latent heat flux
    ΔQ_S = Storage heat flux

URBAN vs RURAL DIFFERENCES:

1. NET RADIATION (Q*):
   Urban: Lower albedo (0.10-0.20) vs rural (0.15-0.25)
   More incoming solar absorbed.
   Complex geometry → multiple reflections.

2. ANTHROPOGENIC HEAT (Q_F):
   Building HVAC, vehicles, metabolism
   20-100 W/m² typical
   >200 W/m² in dense cities (winter heating)

3. SENSIBLE HEAT (Q_H):
   Higher Bowen ratio (Q_H/Q_E)
   Urban: β = 2-5 (more dry)
   Rural: β = 0.5-2

4. LATENT HEAT (Q_E):
   Reduced evapotranspiration
   Less vegetation, sealed surfaces
   Storm sewers remove water quickly

5. STORAGE (ΔQ_S):
   Large heat capacity of buildings/roads
   Absorbs heat by day, releases at night
   Key factor in nocturnal UHI
""")

def urban_net_radiation(S_in, L_in, albedo, emissivity, T_surface):
    """
    Calculate net radiation at urban surface.

    Q* = (1-α)S↓ + ε(L↓ - σT⁴)
    """
    S_absorbed = (1 - albedo) * S_in
    L_net = emissivity * (L_in - sigma * T_surface**4)
    return S_absorbed + L_net

def anthropogenic_heat(population_density, per_capita_power=200, vehicles_per_km2=1000,
                        building_fraction=0.5):
    """
    Estimate anthropogenic heat flux.

    Sources: Buildings, transport, metabolism
    """
    # Metabolism: ~100 W per person
    Q_metabolic = population_density * 100 / 1e6  # W/m²

    # Buildings: per capita power consumption
    Q_buildings = population_density * per_capita_power / 1e6

    # Vehicles: ~30 kW average dissipation per vehicle
    Q_vehicles = vehicles_per_km2 * 30000 / 1e6

    return Q_metabolic + Q_buildings * building_fraction + Q_vehicles

def bowen_ratio_urban(vegetation_fraction, soil_moisture):
    """
    Estimate urban Bowen ratio.

    β = Q_H / Q_E
    Lower vegetation → higher Bowen ratio
    """
    # Rural vegetated: β ~ 0.5-1
    # Urban sealed: β ~ 3-10
    beta_sealed = 5.0
    beta_vegetation = 0.5 + 0.5 * (1 - soil_moisture)

    return (1 - vegetation_fraction) * beta_sealed + vegetation_fraction * beta_vegetation

print("\nUrban energy balance components:")
print("-" * 55)

# Typical summer day conditions
S_in = 800  # W/m²
L_in = 350  # W/m²

print("Surface type comparison (S↓=800 W/m², midday):")
print(f"{'Surface':>15s}  {'α':>6s}  {'Q* (W/m²)':>12s}")
print("-" * 55)

surfaces = [
    ("Asphalt", 0.10, 0.95, 320),
    ("Concrete", 0.25, 0.92, 310),
    ("Dark roof", 0.08, 0.90, 325),
    ("Cool roof", 0.65, 0.90, 305),
    ("Grass", 0.25, 0.95, 298),
    ("Forest", 0.15, 0.97, 300)
]

for name, albedo, emiss, T in surfaces:
    T_K = T + 273.15
    Q_star = urban_net_radiation(S_in, L_in, albedo, emiss, T_K)
    print(f"{name:>15s}  {albedo:>6.2f}  {Q_star:>12.0f}")

print("\nAnthropogenic heat flux estimates:")
print("-" * 45)
densities = [(5000, "Suburban"), (15000, "Urban"), (50000, "Dense urban")]
for pop, desc in densities:
    Q_F = anthropogenic_heat(pop)
    print(f"  {desc:15s} ({pop:>5.0f}/km²): Q_F = {Q_F:.0f} W/m²")

#############################################
# PART 2: URBAN HEAT ISLAND PHYSICS
#############################################
print("\n" + "="*70)
print("PART 2: URBAN HEAT ISLAND (UHI)")
print("="*70)

print("""
URBAN HEAT ISLAND MECHANISMS:
============================

UHI INTENSITY: ΔT_u-r = T_urban - T_rural

MAXIMUM UHI (typically nocturnal):
    ΔT_max ≈ f(city size, rural environment, weather)

EMPIRICAL RELATIONSHIPS:

Oke (1973) for North American cities:
    ΔT_u-r,max = 2.96 log₁₀(P) - 6.41

Where P = population (not physical, but correlates with size)

Physical model (thermal admittance):
    ΔT_u-r = (Q_F + ΔQ*) / (h + h_s)

Where:
    h = convective heat transfer coefficient
    h_s = ground heat flux coefficient

KEY PHYSICAL FACTORS:

1. SKY VIEW FACTOR (ψ_s):
   Fraction of sky visible from surface.
   Street canyon: ψ_s = 0.3-0.6
   Open: ψ_s = 1.0
   Low ψ_s → reduced nocturnal cooling

2. THERMAL MASS:
   Concrete, brick have high heat capacity.
   Store daytime heat, release at night.

3. CANYON GEOMETRY (H/W ratio):
   H = building height, W = street width
   High H/W → "urban canyon"
   More shading, less sky view, trapped radiation

4. IMPERVIOUS SURFACE:
   Reduces evaporative cooling
   Dry surfaces heat more than wet

NOCTURNAL UHI (strongest):
- Clear, calm nights
- Rural areas cool rapidly (radiation)
- Urban areas stay warm (stored heat, low ψ_s)
""")

def sky_view_factor_canyon(H, W):
    """
    Sky view factor for idealized street canyon.

    ψ_s = cos(arctan(H/W))
    """
    theta = np.arctan(H / W)
    return np.cos(theta)

def uhi_oke_empirical(population):
    """
    Oke (1973) empirical UHI relationship.

    ΔT_max = 2.96 log₁₀(P) - 6.41
    """
    if population <= 0:
        return 0
    return 2.96 * np.log10(population) - 6.41

def nocturnal_cooling_rate(sky_view_factor, cloud_fraction, wind_speed):
    """
    Estimate nocturnal cooling rate.

    Radiative cooling ∝ ψ_s × (1 - cloud)
    Turbulent mixing reduces gradient.
    """
    # Maximum radiative cooling ~ 100 W/m² clear sky
    Q_rad = 100 * sky_view_factor * (1 - cloud_fraction)

    # Effective cooling reduced by mixing
    mixing_factor = 1 / (1 + 0.1 * wind_speed)

    # Temperature drop rate (K/hr)
    # Using ρ c_p h (dT/dt) ≈ Q_net
    h_mix = 100  # Mixed layer depth (m)
    dT_dt = Q_rad * mixing_factor / (rho_air * c_p * h_mix) * 3600

    return dT_dt

print("\nUrban Heat Island intensity estimates:")
print("-" * 50)
print(f"{'Population':>15s}  {'ΔT_max (°C)':>12s}")
print("-" * 50)
for pop in [10000, 100000, 500000, 1000000, 5000000, 10000000]:
    dT = uhi_oke_empirical(pop)
    print(f"{pop:>15,d}  {dT:>12.1f}")

print("\nSky view factor and nocturnal cooling:")
print("-" * 55)
print(f"{'H/W ratio':>10s}  {'ψ_s':>8s}  {'Cooling (K/hr)':>15s}  {'Environment':>15s}")
print("-" * 55)
hw_ratios = [(0, "Open rural"), (0.5, "Suburban"), (1.0, "Urban"),
             (2.0, "Dense urban"), (3.0, "Canyon")]
for hw, name in hw_ratios:
    if hw == 0:
        psi = 1.0
    else:
        psi = sky_view_factor_canyon(hw, 1)
    cooling = nocturnal_cooling_rate(psi, 0, 2)  # Clear, light wind
    print(f"{hw:>10.1f}  {psi:>8.2f}  {cooling:>15.2f}  {name:>15s}")

#############################################
# PART 3: URBAN BOUNDARY LAYER
#############################################
print("\n" + "="*70)
print("PART 3: URBAN BOUNDARY LAYER")
print("="*70)

print("""
URBAN BOUNDARY LAYER STRUCTURE:
==============================

Layers (bottom to top):

1. URBAN CANOPY LAYER (UCL):
   Height: 0 to roof level (H)
   Between buildings
   Complex flow patterns
   Influenced by street geometry

2. ROUGHNESS SUBLAYER (RSL):
   Height: H to 2-5H
   Directly influenced by individual roughness elements
   Non-equilibrium turbulence

3. INERTIAL SUBLAYER (ISL):
   Height: 2-5H to ~0.1 z_i
   Logarithmic wind profile applies
   Surface layer similarity

4. MIXED LAYER (ML):
   Height: ~0.1 z_i to z_i
   Well-mixed turbulence
   Convective during day

URBAN ROUGHNESS PARAMETERS:
   z_0 = Roughness length (0.5-2 m for cities)
   d = Displacement height (~0.7 H)

Wind profile in ISL:
   U(z) = (u*/κ) ln[(z-d)/z_0]

URBAN BOUNDARY LAYER HEIGHT:
Typically higher than rural:
- More turbulence
- Heat island effect
- May extend 1-3 km
""")

def urban_roughness_length(building_height, frontal_density):
    """
    Estimate urban roughness length.

    Based on Macdonald et al. (1998) morphometric method.

    frontal_density = frontal area / plan area
    """
    C_D = 1.2  # Drag coefficient
    lambda_f = frontal_density

    # Roughness length formula
    z_0 = building_height * (1 - np.exp(-np.sqrt(0.5 * C_D * lambda_f)))

    return z_0

def displacement_height(building_height, plan_density):
    """
    Estimate displacement height.

    d ≈ 0.7 H × λ_p for moderate densities
    """
    return 0.7 * building_height * min(plan_density, 1.0)

def urban_wind_profile(z, u_star, z_0, d):
    """
    Logarithmic wind profile for urban area.

    U(z) = (u*/κ) ln[(z-d)/z_0]
    """
    if z <= d + z_0:
        return 0
    return (u_star / kappa) * np.log((z - d) / z_0)

def urban_bl_height_convective(Q_H, u_star, f=1e-4):
    """
    Convective boundary layer height.

    z_i = A × (Q_H × t / (ρ c_p))^(1/2)   (encroachment)

    Simplified: z_i ∝ (w* t)

    For quasi-steady: z_i ≈ 0.25 u* / f (mechanical)
                  or  z_i ≈ (w*³ / f)^(1/2) (convective)
    """
    # Convective velocity scale
    w_star = (g / 300 * Q_H / (rho_air * c_p) * 1000) ** (1/3)

    # Convective BL height (simplified)
    z_i = 0.4 * w_star / abs(f)

    return min(z_i, 3000)  # Cap at 3 km

print("\nUrban roughness parameters:")
print("-" * 60)
print(f"{'Building H (m)':>15s}  {'λ_f':>8s}  {'z_0 (m)':>10s}  {'d (m)':>10s}")
print("-" * 60)

for H in [10, 15, 20, 30, 50]:
    for lam in [0.1, 0.3, 0.5]:
        z0 = urban_roughness_length(H, lam)
        d = displacement_height(H, lam)
        print(f"{H:>15.0f}  {lam:>8.1f}  {z0:>10.2f}  {d:>10.1f}")

print("\nWind speed profile (u*=0.5 m/s, H=20m, λ_f=0.3):")
z0 = urban_roughness_length(20, 0.3)
d = displacement_height(20, 0.3)
u_star = 0.5
print(f"  z_0 = {z0:.2f} m, d = {d:.1f} m")
print("-" * 35)
for z in [30, 50, 100, 200, 500]:
    U = urban_wind_profile(z, u_star, z0, d)
    print(f"  z = {z:3.0f} m: U = {U:.1f} m/s")

#############################################
# PART 4: URBAN POLLUTION DISPERSION
#############################################
print("\n" + "="*70)
print("PART 4: POLLUTION DISPERSION")
print("="*70)

print("""
ATMOSPHERIC DISPERSION PHYSICS:
==============================

GAUSSIAN PLUME MODEL:
For continuous point source at height H:

C(x,y,z) = Q/(2π σ_y σ_z U) × exp(-y²/2σ_y²) ×
           [exp(-(z-H)²/2σ_z²) + exp(-(z+H)²/2σ_z²)]

Where:
    C = concentration
    Q = emission rate
    σ_y, σ_z = dispersion coefficients
    U = wind speed
    H = effective stack height

DISPERSION COEFFICIENTS (Pasquill-Gifford):
σ_y = a x^b
σ_z = c x^d

Stability classes A-F:
A: Very unstable (sunny, calm)
D: Neutral (windy/cloudy)
F: Very stable (clear night, calm)

URBAN EFFECTS:
1. Greater roughness → more mechanical mixing
2. Heat island → enhanced convection
3. Building wakes → local high concentrations
4. Street canyon trapping

STREET CANYON DISPERSION:
Wind flow: Skimming (H/W > 1), Wake interference, Isolated roughness

Pollution ratio (canyon/above):
    C_canyon/C_roof ≈ f(H/W, wind direction)

MIXING HEIGHT:
Critical for pollution:
    Low mixing height → high concentrations
    Winter inversions → poor air quality
""")

def pasquill_gifford_sigma(x_m, stability_class='D'):
    """
    Calculate dispersion coefficients.

    Pasquill-Gifford curves (rural).
    Urban: multiply by ~1.5-2.
    """
    x_km = x_m / 1000

    # Coefficients for different stability classes
    params = {
        'A': {'a': 0.22, 'b': 0.894, 'c': 0.20, 'd': 1.0},
        'B': {'a': 0.16, 'b': 0.894, 'c': 0.12, 'd': 1.0},
        'C': {'a': 0.11, 'b': 0.894, 'c': 0.08, 'd': 0.91},
        'D': {'a': 0.08, 'b': 0.894, 'c': 0.06, 'd': 0.85},
        'E': {'a': 0.06, 'b': 0.894, 'c': 0.03, 'd': 0.85},
        'F': {'a': 0.04, 'b': 0.894, 'c': 0.016, 'd': 0.80}
    }

    p = params[stability_class]
    sigma_y = p['a'] * x_km ** p['b'] * 1000  # Convert back to m
    sigma_z = p['c'] * x_km ** p['d'] * 1000

    return sigma_y, sigma_z

def gaussian_plume(Q, U, H, x, y, z, stability='D'):
    """
    Gaussian plume concentration.

    Q: Emission rate [g/s]
    U: Wind speed [m/s]
    H: Effective stack height [m]
    x, y, z: Position [m]

    Returns concentration [g/m³]
    """
    if x <= 0:
        return 0

    sigma_y, sigma_z = pasquill_gifford_sigma(x, stability)

    # Gaussian plume formula
    C = Q / (2 * np.pi * sigma_y * sigma_z * U)
    C *= np.exp(-y**2 / (2 * sigma_y**2))
    C *= (np.exp(-(z - H)**2 / (2 * sigma_z**2)) +
          np.exp(-(z + H)**2 / (2 * sigma_z**2)))

    return C

def max_ground_concentration(Q, U, H, stability='D'):
    """
    Maximum ground-level concentration and distance.
    """
    # Maximum occurs where σ_z ≈ H/√2
    # Iterate to find
    x_max = 100  # Start guess
    C_max = 0

    for x in np.logspace(1, 5, 1000):  # 10 m to 100 km
        C = gaussian_plume(Q, U, H, x, 0, 0, stability)
        if C > C_max:
            C_max = C
            x_max = x

    return C_max, x_max

print("\nDispersion coefficients (downwind distance):")
print("-" * 55)
print(f"{'Distance':>10s}  {'Class A (unstable)':>20s}  {'Class F (stable)':>20s}")
print(f"{'':>10s}  {'σ_y    σ_z':>20s}  {'σ_y    σ_z':>20s}")
print("-" * 55)
for x in [100, 500, 1000, 5000, 10000]:
    sy_A, sz_A = pasquill_gifford_sigma(x, 'A')
    sy_F, sz_F = pasquill_gifford_sigma(x, 'F')
    print(f"{x:>10.0f} m  {sy_A:>8.0f} {sz_A:>8.0f}  {sy_F:>8.0f} {sz_F:>8.0f}")

print("\nGround-level concentration example:")
print("  Emission: 100 g/s, Stack: 50 m, Wind: 5 m/s")
print("-" * 50)
for stab in ['A', 'C', 'D', 'F']:
    C_max, x_max = max_ground_concentration(100, 5, 50, stab)
    desc = {'A': 'Very unstable', 'C': 'Slightly unstable',
            'D': 'Neutral', 'F': 'Stable'}
    print(f"  Class {stab} ({desc[stab]:16s}): C_max = {C_max*1e6:.1f} μg/m³ at {x_max/1000:.1f} km")

#############################################
# PART 5: URBAN PRECIPITATION EFFECTS
#############################################
print("\n" + "="*70)
print("PART 5: URBAN EFFECTS ON PRECIPITATION")
print("="*70)

print("""
URBAN PRECIPITATION MODIFICATION:
================================

OBSERVATIONS:
Cities typically have 5-25% more precipitation than surroundings.
Maximum enhancement often downwind of city center.

PHYSICAL MECHANISMS:

1. THERMAL EFFECT (UHI):
   - Enhanced convection over city
   - Stronger updrafts, more CAPE
   - Can initiate/intensify storms

2. MECHANICAL EFFECT:
   - Greater roughness → convergence
   - Buildings induce uplift
   - Bifurcation of flow around city

3. AEROSOL EFFECT (complex):
   - More CCN → more small droplets
   - Delays warm rain, invigorates convection
   - Can suppress or enhance precipitation

4. MOISTURE EFFECT:
   - Some cities are moisture sources (irrigation)
   - Others are sinks (less evapotranspiration)

METROMEX FINDINGS (St. Louis, 1970s):
- 10-30% increase in summer rainfall
- Enhanced downwind, not over city
- More frequent intense storms
- Thunderstorm bifurcation observed

URBAN-INDUCED CONVECTION:
Threshold conditions:
    UHI > 3°C, CAPE > 500 J/kg, weak synoptic forcing
""")

def enhanced_cape_urban(base_cape, uhi_intensity, pbl_height_ratio):
    """
    Estimate CAPE enhancement due to UHI.

    Simplified: CAPE ∝ θ_v perturbation × depth
    """
    # Very rough estimate
    # CAPE increase ~ 100-200 J/kg per °C of UHI
    delta_cape = 150 * uhi_intensity * pbl_height_ratio
    return base_cape + delta_cape

def urban_convergence(city_size_km, rural_wind, z0_ratio):
    """
    Estimate urban-induced convergence.

    Roughness increases → wind slows → convergence
    """
    # Speed reduction over city
    speed_reduction = 1 - np.sqrt(1/z0_ratio)  # Simplified

    # Convergence ~ ΔU / L
    delta_u = rural_wind * speed_reduction
    convergence = delta_u / (city_size_km * 1000)

    # Convert to updraft (integrated over depth)
    w_induced = convergence * 1000  # m/s if BL is 1 km

    return convergence, w_induced

print("\nUrban CAPE enhancement estimates:")
print("-" * 50)
base_cape = 1000  # J/kg
for uhi in [2, 4, 6]:
    enhanced = enhanced_cape_urban(base_cape, uhi, 1.2)
    print(f"  UHI = {uhi}°C: CAPE {base_cape} → {enhanced:.0f} J/kg (+{enhanced-base_cape:.0f})")

print("\nUrban-induced convergence:")
print("-" * 55)
print(f"{'City size':>10s}  {'U_rural':>10s}  {'Convergence':>12s}  {'w_induced':>12s}")
print("-" * 55)
for size in [10, 30, 50]:
    for U in [5, 10]:
        conv, w = urban_convergence(size, U, 10)  # z0 ratio of 10
        print(f"{size:>10.0f} km  {U:>10.0f} m/s  {conv*1e5:>12.2f}/s  {w:>12.2f} cm/s")

#############################################
# PART 6: BUILDING AERODYNAMICS
#############################################
print("\n" + "="*70)
print("PART 6: BUILDING AERODYNAMICS")
print("="*70)

print("""
FLOW AROUND BUILDINGS:
=====================

SINGLE BUILDING:
Flow separates creating:
1. Upwind horseshoe vortex (ground level)
2. Rooftop separation bubble
3. Building wake (turbulent)
4. Cavity zone (immediately behind)
5. Far wake (reattachment)

WAKE REGION DIMENSIONS:
Cavity length: L_c ≈ 1-2 H
Reattachment: x_r ≈ 5-10 H (depends on geometry)

BUILDING WAKE ALGORITHM:
Velocity deficit in wake:
    ΔU/U_∞ = A exp(-r²/σ_w²)

Where σ_w grows with distance (Gaussian wake).

STREET CANYON FLOW REGIMES:
Depend on H/W ratio:

1. ISOLATED ROUGHNESS (H/W < 0.3):
   - Buildings far apart
   - Wakes don't interact

2. WAKE INTERFERENCE (0.3 < H/W < 0.7):
   - Disturbed flow between buildings
   - Some wake interaction

3. SKIMMING FLOW (H/W > 0.7):
   - Stable vortex in canyon
   - Limited exchange with above
   - Worst for pollution dispersion

PRESSURE COEFFICIENT:
    C_p = (P - P_∞) / (0.5 ρ U²)

Windward face: C_p ≈ +0.8
Leeward face: C_p ≈ -0.3 to -0.5
Roof: C_p ≈ -0.8 to -1.5 (suction)

PEDESTRIAN LEVEL WINDS:
Accelerated at corners (Venturi effect)
    U_corner ≈ 1.3-2.0 U_approach
""")

def street_canyon_regime(H, W):
    """
    Classify street canyon flow regime.
    """
    ratio = H / W
    if ratio < 0.3:
        return "Isolated roughness"
    elif ratio < 0.7:
        return "Wake interference"
    else:
        return "Skimming flow"

def building_wake_length(H, W):
    """
    Estimate wake reattachment distance.
    """
    # Simplified: x_r ≈ 5-10 H for cube
    # Depends on aspect ratio
    L_x = max(H, W)
    return 6 * L_x  # Typical reattachment

def corner_wind_acceleration(approach_speed, building_width, building_height):
    """
    Estimate wind acceleration at building corner.
    """
    # Venturi effect at corner
    # Amplification factor 1.3-2.0 typical
    aspect = building_height / building_width
    amplification = 1.3 + 0.3 * min(aspect, 2)
    return approach_speed * amplification

print("\nStreet canyon flow regimes:")
print("-" * 45)
for H in [10, 20, 30]:
    for W in [10, 20, 40, 60]:
        regime = street_canyon_regime(H, W)
        print(f"  H={H}m, W={W}m (H/W={H/W:.2f}): {regime}")

print("\nPedestrian wind estimates:")
print("-" * 50)
for U in [5, 10, 15]:
    U_corner = corner_wind_acceleration(U, 30, 50)
    print(f"  Approach {U} m/s → Corner {U_corner:.1f} m/s ({U_corner/U:.1f}×)")

#############################################
# PART 7: URBAN CLIMATE MITIGATION
#############################################
print("\n" + "="*70)
print("PART 7: UHI MITIGATION STRATEGIES")
print("="*70)

print("""
COOLING STRATEGIES AND PHYSICS:
==============================

1. COOL ROOFS (high albedo):
   ΔT_surface ≈ (1-α_old)S - (1-α_new)S) / h
   For Δα = 0.4, S = 800 W/m²: ΔT ~ 20-30°C surface

2. GREEN ROOFS:
   Evapotranspiration cooling:
       Q_E = λ ET
   Typical ET: 2-5 mm/day → 50-150 W/m² cooling

3. URBAN TREES:
   - Shading (reduces S↓ to surface)
   - Evapotranspiration (latent heat)
   - Roughness change
   Combined cooling: 2-8°C local air temperature

4. COOL PAVEMENTS:
   Reflective or permeable surfaces
   Albedo: 0.35-0.40 (vs 0.05-0.10 for asphalt)

5. URBAN GEOMETRY:
   - Sky view factor optimization
   - Wind corridor design
   - Building orientation

6. WATER FEATURES:
   Evaporative cooling, thermal mass
   1 kg water evaporated = 2.5 MJ absorbed

EFFECTIVENESS:
Strategy           Typical UHI reduction
Cool roofs         0.3-1.0°C (city-wide)
Urban trees        0.5-2.0°C
Green roofs        0.3-0.8°C
Cool pavements     0.2-0.6°C
Combined           1-3°C possible
""")

def cool_roof_savings(delta_albedo, solar_flux, hours_per_day=8, COP=3):
    """
    Estimate energy savings from cool roof.

    Returns kWh/m²/year cooling energy saved.
    """
    # Reduced heat gain
    Q_reduced = delta_albedo * solar_flux  # W/m²

    # Annual energy saved (cooling)
    # Assume fraction goes to interior
    fraction_interior = 0.3
    annual_hours = hours_per_day * 90  # Cooling season ~90 days

    energy_saved = Q_reduced * fraction_interior * annual_hours / 1000  # kWh/m²
    # Divide by COP for electricity
    electricity_saved = energy_saved / COP

    return electricity_saved

def tree_cooling_estimate(tree_count, crown_diameter, et_rate=4):
    """
    Estimate cooling from urban trees.

    et_rate: mm/day evapotranspiration
    """
    crown_area = np.pi * (crown_diameter/2)**2 * tree_count  # m²

    # Evapotranspiration cooling
    Q_E = et_rate / 1000 * crown_area * L_v / 86400  # W

    # Also shading (assume 80% of solar blocked)
    Q_shade = 0.8 * 800 * crown_area  # W blocked

    return Q_E, Q_shade

print("\nMitigation strategy effectiveness:")
print("-" * 55)

# Cool roof
savings = cool_roof_savings(0.4, 800)
print(f"\nCool roof (Δα=0.4):")
print(f"  Electricity savings: {savings:.1f} kWh/m²/year")
print(f"  For 1000 m² roof: {savings*1000:.0f} kWh/year")

# Trees
Q_E, Q_shade = tree_cooling_estimate(100, 10)
print(f"\nUrban trees (100 trees, 10m crown):")
print(f"  Evaporative cooling: {Q_E/1000:.0f} kW")
print(f"  Shading: {Q_shade/1000:.0f} kW blocked")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("URBAN METEOROLOGY SUMMARY")
print("="*70)
print("""
Key Physics and Phenomena:

1. URBAN ENERGY BALANCE:
   Q* + Q_F = Q_H + Q_E + ΔQ_S
   - Higher Bowen ratio (less evaporation)
   - Anthropogenic heat: 20-200 W/m²
   - Large storage in buildings

2. URBAN HEAT ISLAND:
   - ΔT_max ≈ 2-10°C (larger cities, calm nights)
   - Low sky view factor reduces cooling
   - Thermal mass releases heat at night

3. URBAN BOUNDARY LAYER:
   - Greater roughness: z_0 ~ 0.5-2 m
   - Higher, more turbulent PBL
   - Canopy, roughness, inertial sublayers

4. POLLUTION DISPERSION:
   - Gaussian plume model
   - Stability-dependent σ_y, σ_z
   - Canyon trapping in skimming flow

5. PRECIPITATION EFFECTS:
   - 5-25% enhancement typical
   - Enhanced downwind of city
   - Thermal, mechanical, aerosol mechanisms

6. BUILDING AERODYNAMICS:
   - Canyon regimes: H/W determines flow
   - Wake and corner wind amplification
   - Skimming flow worst for air quality

7. MITIGATION:
   - Cool roofs: 1°C+ reduction
   - Urban trees: 2-8°C local cooling
   - Combined strategies: 1-3°C city-wide

Cities create their own climate!
""")

if __name__ == "__main__":
    print("\n[Urban Meteorology Module - First Principles Complete]")
