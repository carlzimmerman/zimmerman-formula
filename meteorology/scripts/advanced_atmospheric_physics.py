#!/usr/bin/env python3
"""
ADVANCED ATMOSPHERIC PHYSICS - DERIVED FROM FIRST PRINCIPLES
=============================================================

What else can we derive from fundamental physics?

1. Jet Stream Dynamics (thermal wind)
2. Hadley Cell and Global Circulation
3. Rossby Waves and Blocking Patterns
4. Monsoon Physics
5. Sea Breeze / Land-Sea Circulation
6. Atmospheric Tides and Gravity Waves
7. Stratospheric Dynamics
8. Predictability Limits (Lorenz)

All derived from conservation laws and thermodynamics.
"""

import numpy as np
from typing import Dict, Tuple

print("=" * 70)
print("ADVANCED ATMOSPHERIC PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL EQUATIONS
# =============================================================================
print("\n" + "=" * 70)
print("FUNDAMENTAL ATMOSPHERIC EQUATIONS")
print("=" * 70)

print("""
THE PRIMITIVE EQUATIONS (Foundation of all NWP):
================================================

These govern ALL atmospheric motion:

1. MOMENTUM (Newton's 2nd Law + rotation):
   Du/Dt = -∂Φ/∂x + fv - (1/ρ)∂p/∂x + Friction
   Dv/Dt = -∂Φ/∂y - fu - (1/ρ)∂p/∂y + Friction

   Where f = 2Ω sin(φ) = Coriolis parameter

2. HYDROSTATIC BALANCE (vertical):
   ∂p/∂z = -ρg

   Pressure decreases exponentially with height

3. CONTINUITY (mass conservation):
   ∂ρ/∂t + ∇·(ρv) = 0

   Mass can't appear or disappear

4. THERMODYNAMIC (energy conservation):
   DT/Dt = (1/cp)(Q - T∂p/∂t/ρ)

   Temperature changes from heating + compression

5. EQUATION OF STATE (ideal gas):
   p = ρRT

   Connects pressure, density, temperature


These 5 equations + boundary conditions = weather prediction!
""")


# Physical constants
OMEGA = 7.292e-5  # Earth's rotation rate (rad/s)
R_EARTH = 6.371e6  # Earth radius (m)
G = 9.81          # Gravity (m/s²)
R_AIR = 287       # Gas constant for air (J/kg/K)
C_P = 1005        # Specific heat (J/kg/K)


def coriolis_parameter(latitude_deg: float) -> float:
    """Coriolis parameter f = 2Ω sin(φ)"""
    return 2 * OMEGA * np.sin(np.radians(latitude_deg))


def rossby_number(U: float, L: float, f: float) -> float:
    """
    Rossby number Ro = U/(fL)

    Ro << 1: Rotation dominates (large-scale flow)
    Ro >> 1: Inertia dominates (small-scale, tornadoes)
    """
    return U / (f * L)


print("\nCoriolis Parameter by Latitude:")
print("-" * 40)
for lat in [0, 15, 30, 45, 60, 90]:
    f = coriolis_parameter(lat)
    print(f"  {lat:3d}°: f = {f:.2e} s⁻¹")


# =============================================================================
# PART 1: THERMAL WIND AND JET STREAMS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: THERMAL WIND AND JET STREAMS")
print("=" * 70)

print("""
THERMAL WIND RELATION:
======================

The jet stream exists because of horizontal temperature gradients!

From geostrophic balance + hydrostatic equation:

∂u_g/∂z = -(g/fT) × ∂T/∂y

This says: Wind SHEAR is proportional to temperature GRADIENT

Physical interpretation:
- Cold air is denser → pressure drops faster with height
- Warm air is less dense → pressure drops slower
- Result: Pressure gradient increases with height
- Geostrophic wind increases with height = JET STREAM

The jet stream is where polar cold meets tropical warm!
""")

def thermal_wind_shear(dT_dy: float, T_mean: float, f: float) -> float:
    """
    Calculate geostrophic wind shear (m/s per km height).

    ∂u_g/∂z = -(g/fT) × ∂T/∂y

    dT_dy: temperature gradient (K per m, negative for typical NH)
    T_mean: mean temperature (K)
    f: Coriolis parameter
    """
    if abs(f) < 1e-10:
        return 0  # No thermal wind at equator

    shear = -(G / (f * T_mean)) * dT_dy
    return shear  # m/s per m height


def jet_stream_speed(lat: float, dT_per_1000km: float, height_km: float = 10) -> float:
    """
    Estimate jet stream speed from temperature gradient.

    Typical polar front: 10-20 K per 1000 km
    """
    f = coriolis_parameter(lat)
    if abs(f) < 1e-10:
        return 0

    T_mean = 250  # K (upper troposphere)
    dT_dy = dT_per_1000km / 1e6  # Convert to K/m

    shear = thermal_wind_shear(dT_dy, T_mean, f)

    # Surface wind assumed ~5 m/s westerly
    surface_wind = 5

    # Wind at jet level
    jet_speed = surface_wind + shear * height_km * 1000

    return jet_speed


print("\nJet Stream Speed vs Temperature Gradient:")
print("-" * 60)
print(f"{'Lat':>5} | {'ΔT/1000km':>12} | {'Jet Speed':>12} | {'Description':<20}")
print("-" * 60)

scenarios = [
    (45, 5, "Weak gradient"),
    (45, 10, "Moderate gradient"),
    (45, 15, "Strong gradient"),
    (45, 25, "Extreme (blocking)"),
    (30, 15, "Subtropical jet"),
    (60, 15, "Polar jet"),
]

for lat, dT, desc in scenarios:
    speed = jet_stream_speed(lat, dT)
    print(f"{lat:>5}° | {dT:>10} K | {speed:>10.0f} m/s | {desc:<20}")

print("""

KEY INSIGHT:
- Stronger temperature gradient → faster jet stream
- Jet speed of 50-100 m/s (100-200 mph) is typical
- Waviness in jet = Rossby waves = weather patterns
- Blocking = jet stream gets "stuck" → persistent weather
""")


# =============================================================================
# PART 2: HADLEY CELL AND GLOBAL CIRCULATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: HADLEY CELL AND GLOBAL CIRCULATION")
print("=" * 70)

print("""
HADLEY CELL - DERIVED FROM FIRST PRINCIPLES:
=============================================

Start with energy balance:
1. Tropics receive more solar energy than they radiate
2. Poles radiate more than they receive
3. Heat MUST flow poleward to balance

How does it flow?

Near equator (f ≈ 0):
- Direct thermal circulation possible
- Hot air rises, flows poleward, cools, sinks
- This is the HADLEY CELL

But Earth rotates!
- Air moving poleward gains westerly momentum (Coriolis)
- By ~30°N/S, westerlies are too strong to continue poleward
- Air sinks → subtropical HIGH pressure belt
- Surface: Trade winds (equatorward) + Westerlies (poleward)


HADLEY CELL EXTENT (from angular momentum):

At surface: u ≈ 0 (roughly)
At poleward edge: u = Ωa cos(φ₀)/cos(φ) - Ωa cos(φ)

Where angular momentum is conserved.

Setting this equal to observed subtropical jet (~30 m/s at 30°):
φ_edge ≈ 30° latitude

This matches observations! The Hadley cell extends ~0-30°
""")

def hadley_cell_wind(latitude_start: float, latitude_end: float) -> float:
    """
    Estimate wind at latitude assuming angular momentum conservation.

    Start at equator with u=0, move poleward.
    """
    a = R_EARTH

    # Angular momentum per unit mass at equator surface
    # M = (Ωa + u)a cos(φ)
    # At equator with u=0: M = Ωa² cos(0) = Ωa²

    phi_start = np.radians(latitude_start)
    phi_end = np.radians(latitude_end)

    M = OMEGA * a**2 * np.cos(phi_start)  # Initial angular momentum

    # At new latitude: M = (Ωa cos(φ) + u) × a cos(φ)
    # Solve for u: u = M/(a cos(φ)) - Ωa cos(φ)

    u = M / (a * np.cos(phi_end)) - OMEGA * a * np.cos(phi_end)

    return u


print("\nAngular Momentum Conservation → Subtropical Jet:")
print("-" * 50)
print(f"{'Starting Lat':>12} | {'Ending Lat':>12} | {'Wind (m/s)':>12}")
print("-" * 50)

for start in [0, 5, 10]:
    for end in [15, 20, 25, 30, 35]:
        if end > start:
            u = hadley_cell_wind(start, end)
            print(f"{start:>12}° | {end:>12}° | {u:>12.1f}")

print("""

This shows why the Hadley cell can't extend to poles:
- By 30°, winds would be ~130 m/s (unsustainable)
- Instabilities break down direct circulation
- Eddies (storms) transport heat poleward of 30°


THREE-CELL MODEL:
=================
0-30°:   Hadley Cell (direct, thermally driven)
30-60°:  Ferrel Cell (indirect, eddy-driven)
60-90°:  Polar Cell (direct, weak)

Surface winds:
0-30°:   Trade Winds (easterly)
30-60°:  Westerlies
60-90°:  Polar Easterlies
""")


# =============================================================================
# PART 3: ROSSBY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: ROSSBY WAVES - THE WEATHER MAKERS")
print("=" * 70)

print("""
ROSSBY WAVE PHYSICS:
====================

Rossby waves are the large undulations in the jet stream.
They arise from conservation of POTENTIAL VORTICITY.

Potential Vorticity (PV):
PV = (ζ + f) / H

where:
- ζ = relative vorticity (spin from flow)
- f = planetary vorticity (Earth's rotation)
- H = layer thickness

PV MUST be conserved following the flow!

If air moves poleward:
- f increases (more planetary vorticity)
- To conserve PV, ζ must decrease (anticyclonic)
- This curves the flow back equatorward

If air moves equatorward:
- f decreases
- ζ must increase (cyclonic)
- This curves the flow back poleward

Result: WAVE MOTION with westward phase propagation!
""")

def rossby_wave_speed(U: float, L_km: float, latitude: float) -> Dict:
    """
    Calculate Rossby wave properties.

    Phase speed: c = U - β L²/4π²
    where β = df/dy = 2Ω cos(φ)/a

    Wave moves WEST relative to the mean flow!
    """
    L = L_km * 1000  # Convert to meters

    # Beta parameter
    beta = 2 * OMEGA * np.cos(np.radians(latitude)) / R_EARTH

    # Wavenumber
    k = 2 * np.pi / L

    # Rossby wave phase speed (relative to ground)
    c_phase = U - beta / k**2

    # Stationary wavelength (where c = 0)
    L_stationary = 2 * np.pi * np.sqrt(U / beta)

    return {
        'phase_speed': c_phase,
        'mean_flow': U,
        'wavelength_km': L_km,
        'stationary_wavelength_km': L_stationary / 1000,
        'beta': beta,
    }


print("\nRossby Wave Properties at 45°N:")
print("-" * 70)
print(f"{'U (m/s)':<10} | {'λ (km)':<10} | {'Phase (m/s)':<12} | {'Direction':<15}")
print("-" * 70)

for U in [10, 20, 30]:
    for L in [3000, 5000, 8000, 10000]:
        result = rossby_wave_speed(U, L, 45)
        direction = "West" if result['phase_speed'] < 0 else "East"
        print(f"{U:<10} | {L:<10} | {result['phase_speed']:<12.1f} | {direction:<15}")

print("\n")
result = rossby_wave_speed(20, 5000, 45)
print(f"Stationary wavelength at U=20 m/s: {result['stationary_wavelength_km']:.0f} km")
print("""
This is ~6000-8000 km, which matches observed planetary waves!

BLOCKING:
When Rossby waves become stationary or slow down:
- Weather patterns persist for days to weeks
- Leads to heat waves, cold spells, droughts
- Linked to jet stream waviness
""")


# =============================================================================
# PART 4: MONSOON PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: MONSOON PHYSICS")
print("=" * 70)

print("""
MONSOON: LAND-SEA THERMAL CONTRAST
==================================

Basic physics: Land heats/cools faster than ocean.

Summer:
- Land heats up → low pressure over land
- Ocean stays cooler → high pressure over ocean
- Wind blows from ocean to land (onshore)
- Moist air → RAIN

Winter:
- Land cools down → high pressure over land
- Ocean stays warmer → low pressure over ocean
- Wind blows from land to ocean (offshore)
- Dry air → DRY SEASON

The strength depends on:
1. Land-sea temperature contrast
2. Latitude (Coriolis deflection)
3. Topography (Himalayas amplify Asian monsoon)
""")

def monsoon_strength(land_temp: float, ocean_temp: float, latitude: float) -> Dict:
    """
    Estimate monsoon circulation strength from land-sea contrast.

    Simplified sea breeze / monsoon calculation.
    """
    delta_T = land_temp - ocean_temp

    # Pressure difference (simplified)
    # Δp ≈ ρ g h × ΔT/T (thermal expansion of column)
    h = 1000  # characteristic height (m)
    T_mean = (land_temp + ocean_temp) / 2 + 273.15
    rho = 1.2  # kg/m³

    delta_p = rho * G * h * abs(delta_T) / T_mean  # Pa

    # Wind speed from pressure gradient
    # Simplified: V ≈ √(2 Δp / ρ) but limited by Coriolis
    f = abs(coriolis_parameter(latitude))

    if f > 1e-10:
        # Geostrophic approximation for large-scale
        L = 500e3  # characteristic length (m)
        V = delta_p / (rho * f * L)
    else:
        # Near equator, direct circulation
        V = np.sqrt(2 * delta_p / rho) * 0.3  # Friction reduction

    direction = "Onshore (land warmer)" if delta_T > 0 else "Offshore (ocean warmer)"

    return {
        'wind_speed': abs(V),
        'direction': direction,
        'pressure_diff_hPa': delta_p / 100,
        'temp_contrast': delta_T,
    }


print("\nMonsoon/Sea Breeze Strength:")
print("-" * 70)
print(f"{'Land (°C)':<10} | {'Ocean (°C)':<10} | {'ΔT':>6} | {'Wind (m/s)':>10} | {'Direction':<20}")
print("-" * 70)

for land, ocean in [(35, 25), (30, 27), (25, 28), (10, 15), (40, 25)]:
    result = monsoon_strength(land, ocean, 20)
    print(f"{land:<10} | {ocean:<10} | {result['temp_contrast']:>6.0f} | {result['wind_speed']:>10.1f} | {result['direction']:<20}")


# =============================================================================
# PART 5: ATMOSPHERIC PREDICTABILITY LIMITS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: ATMOSPHERIC PREDICTABILITY - LORENZ LIMIT")
print("=" * 70)

print("""
WHY CAN'T WE PREDICT WEATHER BEYOND ~2 WEEKS?
=============================================

Edward Lorenz (1963) discovered CHAOS in weather equations.

The Lorenz attractor comes from simplified convection:
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz

Key property: SENSITIVE DEPENDENCE ON INITIAL CONDITIONS
Small errors grow exponentially → "Butterfly Effect"

Error growth rate:
ε(t) = ε₀ × exp(λt)

where λ ≈ 1/day for atmosphere

Starting from ε₀ = 0.01% (best observations):
- Day 1: 0.03%
- Day 3: 0.2%
- Day 5: 1.5%
- Day 7: 11%
- Day 10: 200% (saturated)

After ~10-14 days, forecast = climatology (no skill)

This is a FUNDAMENTAL LIMIT, not a technology problem!
""")

def error_growth(initial_error: float, days: float, doubling_time: float = 2.5) -> float:
    """
    Calculate forecast error growth.

    Errors double roughly every 2-3 days in atmosphere.
    """
    # λ = ln(2) / doubling_time
    lambda_rate = np.log(2) / doubling_time

    error = initial_error * np.exp(lambda_rate * days)

    # Saturate at 100% (no skill)
    return min(100, error)


print("\nForecast Error Growth (starting from 1% error):")
print("-" * 50)
print(f"{'Day':>6} | {'Error %':>10} | {'Forecast Quality':<20}")
print("-" * 50)

for day in [0, 1, 2, 3, 5, 7, 10, 14, 21]:
    error = error_growth(1.0, day)
    if error < 10:
        quality = "Excellent"
    elif error < 30:
        quality = "Good"
    elif error < 60:
        quality = "Fair"
    elif error < 100:
        quality = "Poor"
    else:
        quality = "No skill"
    print(f"{day:>6} | {error:>10.1f} | {quality:<20}")

print("""

BUT: Different scales have different limits!

Scale            | Predictability
----------------------------------------
Individual storm | 1-2 days (convective)
Synoptic systems | 3-7 days (fronts, lows)
Planetary waves  | 7-14 days
Seasonal mean    | Months (ENSO helps!)
Climate change   | Decades to centuries

The paradox: We can predict climate change better than
next month's weather because climate is forced
(by CO2), while weather is chaotic.
""")


# =============================================================================
# PART 6: WHAT ELSE CAN WE DERIVE?
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: ADDITIONAL DERIVABLE PHENOMENA")
print("=" * 70)

print("""
MORE FIRST-PRINCIPLES DERIVATIONS:
==================================

1. LAPSE RATE
   - Dry adiabatic: Γ_d = g/c_p = 9.8 K/km
   - Moist adiabatic: Γ_m ≈ 6 K/km (latent heat release)
   - Environmental > dry → unstable (storms!)

2. SCALE HEIGHT
   - H = RT/g ≈ 8.5 km for Earth
   - Pressure: p(z) = p₀ exp(-z/H)
   - 50% of atmosphere below 5.5 km

3. TROPOPAUSE HEIGHT
   - Radiative equilibrium calculation
   - Tropics: ~17 km (warm, high)
   - Poles: ~8 km (cold, low)

4. STRATOSPHERIC CIRCULATION
   - Brewer-Dobson circulation
   - Ozone transported poleward
   - Sudden Stratospheric Warmings

5. GRAVITY WAVES
   - From mountain flow, convection
   - ω = Nk_h / √(k_h² + k_z²)
   - Transport momentum vertically

6. KELVIN AND ROSSBY WAVES (TROPICS)
   - Equatorial dynamics different (f ≈ 0)
   - Kelvin waves: eastward only
   - Rossby waves: westward
   - MJO = coupled Kelvin-Rossby

7. POLAR VORTEX
   - Strong westerlies around pole
   - Thermal wind from equator-pole gradient
   - Weakens in winter → cold outbreaks
""")

# Calculate some additional quantities
print("\nDerived Atmospheric Quantities:")
print("-" * 50)

# Scale height
T_mean = 250  # K
H = R_AIR * T_mean / G
print(f"Scale height H = RT/g = {H/1000:.1f} km")

# Dry adiabatic lapse rate
gamma_d = G / C_P * 1000  # K/km
print(f"Dry adiabatic lapse rate = g/c_p = {gamma_d:.1f} K/km")

# Brunt-Väisälä frequency (stratosphere)
N_squared = (G / 300) * (0.003)  # Typical stratospheric stability
N = np.sqrt(N_squared)
period = 2 * np.pi / N
print(f"Brunt-Väisälä period (stratosphere) = {period/60:.1f} minutes")

# Deformation radius
f_45 = coriolis_parameter(45)
N_trop = 0.01  # Tropospheric value
H_trop = 10000  # m
L_d = N_trop * H_trop / f_45
print(f"Rossby deformation radius (45°) = {L_d/1000:.0f} km")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: ATMOSPHERIC PHYSICS FROM FIRST PRINCIPLES")
print("=" * 70)

print("""
WHAT WE CAN DERIVE:
===================

✓ Jet stream speed from temperature gradient (thermal wind)
✓ Hadley cell extent from angular momentum conservation
✓ Rossby wave behavior from PV conservation
✓ Monsoon strength from land-sea contrast
✓ Predictability limits from chaos theory
✓ Scale height, lapse rates, tropopause height

WHAT REQUIRES OBSERVATIONS/MODELS:
==================================
? Cloud feedback details
? Small-scale turbulence
? Convective parameterization
? Exact storm tracks
? Extreme event statistics

KEY INSIGHT:
============
The atmosphere obeys fundamental physics:
- Conservation laws (mass, momentum, energy, PV)
- Thermodynamics
- Rotating frame dynamics

We can derive qualitative behavior and scaling from physics.
Quantitative prediction requires numerical models.
But the models encode the SAME physics we derived here!

This is why physics-based models work:
They're solving the equations we just derived,
at high resolution with realistic boundary conditions.
""")

print("\n" + "=" * 70)
print("END OF ADVANCED ATMOSPHERIC PHYSICS")
print("=" * 70)
