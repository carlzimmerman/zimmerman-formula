#!/usr/bin/env python3
"""
OCEAN-CLIMATE COUPLING - FIRST PRINCIPLES
==========================================

Deriving ocean circulation, heat transport, and sea level physics
from fundamental equations.
"""

import numpy as np

print("=" * 70)
print("OCEAN-CLIMATE COUPLING - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL OCEAN CONSTANTS
# =============================================================================
print("\n" + "=" * 70)
print("FUNDAMENTAL OCEAN PROPERTIES")
print("=" * 70)

# Physical constants
rho_sw = 1025       # seawater density (kg/m³)
c_p_sw = 3850       # specific heat of seawater (J/kg/K)
alpha = 2.1e-4      # thermal expansion coefficient (K⁻¹)
beta_s = 7.6e-4     # haline contraction coefficient (psu⁻¹)
g = 9.81            # gravity (m/s²)
omega = 7.29e-5     # Earth rotation rate (rad/s)
R_earth = 6.371e6   # Earth radius (m)

properties = f"""
Ocean Water Properties:
-----------------------
Density (ρ):           {rho_sw} kg/m³
Specific heat (c_p):   {c_p_sw} J/kg/K
Thermal expansion (α): {alpha:.1e} K⁻¹
Haline contraction:    {beta_s:.1e} psu⁻¹

Key insight: Ocean has HUGE thermal inertia
- Top 3m of ocean has same heat capacity as ENTIRE atmosphere
- This is why oceans dominate Earth's heat budget
"""
print(properties)


# =============================================================================
# PART 1: OCEAN HEAT CONTENT AND ENERGY BUDGET
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: OCEAN HEAT CONTENT AND ENERGY BUDGET")
print("=" * 70)

heat_capacity_text = """
OCEAN AS EARTH'S HEAT RESERVOIR:
================================

Heat capacity comparison:
- Atmosphere: mass ≈ 5.15×10¹⁸ kg, c_p = 1004 J/kg/K
- Ocean:      mass ≈ 1.4×10²¹ kg,  c_p = 3850 J/kg/K

Ocean heat capacity = (1.4×10²¹ × 3850) / (5.15×10¹⁸ × 1004)
                   ≈ 1000× atmosphere!

Even top 100m of ocean ≈ 30× atmosphere heat capacity

This is why:
1. Oceans absorb >90% of warming from CO2
2. Climate system has INERTIA (decades to equilibrate)
3. "Warming in the pipeline" exists even if CO2 stops
"""
print(heat_capacity_text)

# Calculate ocean heat content change
def ocean_heat_content_change(dT, depth, area_fraction=0.71):
    """
    Calculate ocean heat content change.

    dT: temperature change (K)
    depth: depth of warmed layer (m)
    area_fraction: fraction of Earth covered by ocean
    """
    A_earth = 4 * np.pi * R_earth**2  # Earth surface area
    A_ocean = A_earth * area_fraction

    volume = A_ocean * depth
    mass = volume * rho_sw
    dQ = mass * c_p_sw * dT

    return dQ

# Ocean warming since 1970s
dT_upper = 0.6   # Upper 700m warming (K)
dT_deep = 0.1    # Below 700m warming (K)

dQ_upper = ocean_heat_content_change(dT_upper, 700)
dQ_deep = ocean_heat_content_change(dT_deep, 3000)
dQ_total = dQ_upper + dQ_deep

print(f"\nOcean Heat Content Change (1970-present):")
print("-" * 50)
print(f"Upper ocean (0-700m) warming: {dT_upper}°C")
print(f"  Heat gained: {dQ_upper:.2e} J")
print(f"Deep ocean (700-4000m) warming: {dT_deep}°C")
print(f"  Heat gained: {dQ_deep:.2e} J")
print(f"Total ocean heat gain: {dQ_total:.2e} J")

# Convert to energy imbalance
years = 50
seconds = years * 365.25 * 24 * 3600
power_imbalance = dQ_total / seconds
A_earth = 4 * np.pi * R_earth**2
flux_imbalance = power_imbalance / A_earth

print(f"\nImplied Earth Energy Imbalance:")
print(f"  Power: {power_imbalance:.2e} W")
print(f"  Flux:  {flux_imbalance:.2f} W/m²")
print(f"  (Observed: ~0.5-1.0 W/m² - matches!)")


# =============================================================================
# PART 2: THERMOHALINE CIRCULATION (AMOC)
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: THERMOHALINE CIRCULATION (AMOC)")
print("=" * 70)

thermohaline_text = """
THE GREAT OCEAN CONVEYOR BELT:
==============================

Driven by DENSITY differences from:
1. Temperature (thermal)
2. Salinity (haline)

Density equation of state:
ρ = ρ₀[1 - α(T-T₀) + β(S-S₀)]

Where:
- α ≈ 2×10⁻⁴ K⁻¹ (thermal expansion)
- β ≈ 8×10⁻⁴ psu⁻¹ (haline contraction)

Note: β/α ≈ 4, so salinity changes have 4× more
      density effect than temperature changes of same magnitude.

NORTH ATLANTIC DEEP WATER FORMATION:
1. Gulf Stream brings warm, salty water north
2. Loses heat to atmosphere (cools → denser)
3. Evaporation (saltier → denser)
4. Dense water SINKS to depth (2-4 km)
5. Flows south as deep current
6. Upwells in Southern Ocean
7. Returns at surface → closed loop

Flow rate: ~18 Sv (1 Sv = 10⁶ m³/s)
Heat transport: ~1 PW (petawatt) northward
"""
print(thermohaline_text)

def density_anomaly(dT, dS):
    """Calculate density change from T and S changes."""
    return -alpha * dT + beta_s * dS

def overturning_transport(delta_rho, depth, width):
    """
    Estimate overturning from density contrast.

    Simplified scaling from geostrophic balance + friction.
    """
    # Simplified: velocity ~ sqrt(g' * D) where g' = g*Δρ/ρ
    g_prime = g * delta_rho / rho_sw
    velocity = np.sqrt(g_prime * depth)

    # Transport = velocity × area
    transport = velocity * depth * width
    return transport / 1e6  # Convert to Sverdrups

print("\nDensity Changes from Temperature and Salinity:")
print("-" * 60)
print(f"{'Change':<30} {'Density anomaly':>15}")
print("-" * 60)

scenarios = [
    ("Cool by 5°C", -5, 0),
    ("Increase salt by 1 psu", 0, 1),
    ("Cool 5°C + salt +1 psu", -5, 1),
    ("Warm 3°C (Greenland melt)", 3, -2),  # Freshening
    ("Gulf Stream: warm, salty", 10, 2),
]

for name, dT, dS in scenarios:
    drho = density_anomaly(dT, dS)
    print(f"{name:<30} {drho:>+12.3f} kg/m³")

# AMOC stability concern
print("\n\nAMOC STABILITY AND CLIMATE CHANGE:")
print("=" * 50)
amoc_text = """
The AMOC is potentially BISTABLE:
- "On" state: current circulation
- "Off" state: greatly reduced circulation

Concern: Freshwater from Greenland ice melt reduces salinity
→ Less dense → Won't sink → Circulation slows

Evidence from past:
- Younger Dryas (12,900 years ago): AMOC shutdown
- Caused rapid cooling in North Atlantic region
- Triggered by glacial meltwater pulse

Current observations:
- Some studies suggest AMOC has weakened 15% since 1950s
- But natural variability is large
- Full shutdown unlikely this century (IPCC)
- But continued weakening is probable
"""
print(amoc_text)


# =============================================================================
# PART 3: EKMAN TRANSPORT AND WIND-DRIVEN CIRCULATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: WIND-DRIVEN CIRCULATION")
print("=" * 70)

ekman_text = """
EKMAN TRANSPORT - WIND MOVES WATER SIDEWAYS!
=============================================

Surprising result from 1905 (Nansen + Ekman):

When wind blows over ocean:
1. Surface water moves 45° to RIGHT of wind (N. Hemisphere)
2. Each layer below deflects further right
3. Average motion (Ekman transport) is 90° to wind!

Physics: Balance between friction and Coriolis

Ekman layer depth:
D_E = √(2K/f) ≈ 50-100m

Where K = eddy viscosity (~0.1 m²/s)

Transport magnitude:
M_E = τ / (ρf)

Where τ = wind stress (Pa)
"""
print(ekman_text)

def ekman_transport(wind_stress, latitude):
    """Calculate Ekman transport from wind stress."""
    f = 2 * omega * np.sin(np.radians(latitude))
    if abs(f) < 1e-10:
        return float('inf')  # Undefined at equator

    M = wind_stress / (rho_sw * abs(f))
    return M  # m²/s (volume transport per unit width)

def ekman_depth(K_eddy=0.1, latitude=30):
    """Calculate Ekman layer depth."""
    f = 2 * omega * np.sin(np.radians(latitude))
    D = np.sqrt(2 * K_eddy / abs(f))
    return D

print("\nEkman Transport and Depth:")
print("-" * 60)
print(f"{'Wind (N/m²)':<15} {'Latitude':<10} {'Transport (m²/s)':<20} {'Depth (m)':<10}")
print("-" * 60)

for tau in [0.05, 0.1, 0.2]:
    for lat in [15, 30, 45, 60]:
        M = ekman_transport(tau, lat)
        D = ekman_depth(latitude=lat)
        print(f"{tau:<15.2f} {lat:<10.0f}° {M:<20.1f} {D:<10.0f}")


# Sverdrup balance and gyres
print("\n\nSVERDRUP BALANCE - OCEAN GYRES:")
print("=" * 50)
sverdrup_text = """
The great ocean gyres (circulation patterns) arise from:

1. Wind stress curl (∇×τ) drives Ekman pumping
2. Ekman pumping → vertical velocity
3. Vorticity conservation → meridional flow

SVERDRUP RELATION:
βv = (1/ρ) ∇×τ / H

Where β = df/dy = variation of Coriolis with latitude

This explains:
- Subtropical gyres rotate CLOCKWISE (N. Hemisphere)
- Trade winds + Westerlies → convergence → downwelling
- Water piles up in center → sea level HIGH
- Geostrophic flow around the pile = GYRE

WESTERN BOUNDARY CURRENTS (Gulf Stream, Kuroshio):
- Gyres are intensified on WESTERN side
- Due to β-effect + friction balance
- Result: Narrow, fast, warm currents on west
         Broad, slow, cool currents on east
"""
print(sverdrup_text)


# =============================================================================
# PART 4: SEA LEVEL RISE - COMPLETE PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SEA LEVEL RISE PHYSICS")
print("=" * 70)

slr_text = """
SEA LEVEL RISE HAS THREE MAIN COMPONENTS:
=========================================

1. THERMAL EXPANSION (steric)
   Water expands when heated: ΔV/V = α ΔT
   α ≈ 2×10⁻⁴ K⁻¹ for seawater

2. LAND ICE MELT (eustatic)
   Glaciers + Ice sheets → ocean
   Volume → sea level: Δh = Volume / A_ocean

3. LAND WATER STORAGE (minor)
   Groundwater depletion, reservoirs
   Small but non-zero contribution
"""
print(slr_text)

def thermal_expansion_slr(dT, mixed_layer_depth=700):
    """
    Calculate sea level rise from thermal expansion.

    dT: temperature change (K)
    mixed_layer_depth: depth of warmed layer (m)
    """
    dh = alpha * dT * mixed_layer_depth
    return dh * 1000  # Convert to mm

def ice_melt_slr(ice_volume_km3):
    """
    Calculate sea level rise from ice melt.

    ice_volume_km3: volume of ice melted (km³)
    """
    A_ocean = 3.62e14  # Ocean area (m²)
    V_water = ice_volume_km3 * 1e9 * (917/1000)  # Ice → water volume (m³)
    dh = V_water / A_ocean
    return dh * 1000  # mm

print("\nSea Level Rise Components:")
print("-" * 70)

# Current observed rates
print("\nObserved rates (2006-2018):")
thermal = 1.4   # mm/yr
glaciers = 0.8  # mm/yr
greenland = 0.7 # mm/yr
antarctica = 0.4 # mm/yr
total_obs = thermal + glaciers + greenland + antarctica
print(f"  Thermal expansion:   {thermal:.1f} mm/yr")
print(f"  Glacier melt:        {glaciers:.1f} mm/yr")
print(f"  Greenland:           {greenland:.1f} mm/yr")
print(f"  Antarctica:          {antarctica:.1f} mm/yr")
print(f"  Total observed:      {total_obs:.1f} mm/yr (~3.3 mm/yr)")

# Ice sheet sea level equivalent
print("\n\nIce Sheet Sea Level Equivalent:")
print("-" * 50)
ice_sheets = [
    ("Antarctic Ice Sheet", 26.5e6),  # km³
    ("Greenland Ice Sheet", 2.85e6),
    ("All other glaciers", 0.158e6),
]

for name, volume in ice_sheets:
    slr = ice_melt_slr(volume)
    print(f"{name:<25}: {volume/1e6:.2f} million km³ → {slr/1000:.1f} m SLR")

# Thermal expansion calculation
print("\n\nThermal Expansion Calculation:")
print("-" * 50)
for depth in [100, 300, 700, 2000]:
    for dT in [0.3, 0.5, 1.0]:
        slr = thermal_expansion_slr(dT, depth)
        print(f"  {depth}m depth, {dT}°C warming → {slr:.0f} mm SLR")


# =============================================================================
# PART 5: OCEAN ACIDIFICATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: OCEAN ACIDIFICATION")
print("=" * 70)

acidification_text = """
CO2 + SEAWATER → ACIDIFICATION
==============================

Chemical reactions:
1. CO2(g) → CO2(aq)                     (dissolution)
2. CO2(aq) + H2O → H2CO3                (carbonic acid)
3. H2CO3 → H⁺ + HCO3⁻                   (first dissociation)
4. HCO3⁻ → H⁺ + CO3²⁻                   (second dissociation)

Net effect: More CO2 → more H⁺ → lower pH → MORE ACIDIC

Ocean pH change:
- Pre-industrial: pH ≈ 8.2
- Current (2024): pH ≈ 8.1
- By 2100 (RCP8.5): pH ≈ 7.8

This is a 30% increase in H⁺ concentration!
(pH is logarithmic: Δ[H⁺] = 10^(8.2-8.1) - 1 = 26%)

CARBONATE SATURATION:
The reaction CO3²⁻ + 2H⁺ → H2O + CO2 removes carbonate ions.

Less CO3²⁻ → harder for organisms to build CaCO3 shells
Affects: Corals, mollusks, plankton with shells

Saturation state: Ω = [Ca²⁺][CO3²⁻] / K_sp

Ω > 1: Supersaturated (shell formation easy)
Ω < 1: Undersaturated (shells dissolve!)
"""
print(acidification_text)

def pH_from_CO2(pCO2_ppm, base_pH=8.2, base_CO2=280):
    """
    Simple estimate of ocean pH change from CO2.

    Empirical relationship: ΔpH ≈ -0.4 × log2(pCO2/280)
    """
    dpH = -0.4 * np.log2(pCO2_ppm / base_CO2)
    return base_pH + dpH

print("\nOcean pH vs Atmospheric CO2:")
print("-" * 50)
print(f"{'CO2 (ppm)':<15} {'pH':>10} {'[H⁺] change':>15}")
print("-" * 50)

for co2 in [280, 350, 400, 450, 560, 700, 1000]:
    pH = pH_from_CO2(co2)
    H_change = (10**(8.2 - pH) - 1) * 100  # % change from preindustrial
    print(f"{co2:<15.0f} {pH:>10.2f} {H_change:>+14.0f}%")


# =============================================================================
# PART 6: OCEAN-ATMOSPHERE COUPLING (ENSO MECHANISM)
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: ENSO MECHANISM - OCEAN-ATMOSPHERE COUPLING")
print("=" * 70)

enso_physics = """
EL NIÑO-SOUTHERN OSCILLATION (ENSO):
====================================

The dominant mode of year-to-year climate variability.

NORMAL CONDITIONS (La Niña-like):
1. Trade winds blow westward across Pacific
2. Push warm water to western Pacific (warm pool)
3. Cold water upwells in eastern Pacific
4. Warm west → convection → reinforces trades
5. This is a POSITIVE FEEDBACK loop!

EL NIÑO:
1. Something weakens trade winds
2. Warm water sloshes back eastward
3. Less upwelling → eastern Pacific warms
4. Convection shifts eastward
5. Trades weaken further → FEEDBACK continues
6. Eastern Pacific can warm 2-4°C

LA NIÑA:
- Opposite: Enhanced trades, stronger upwelling
- Cold eastern Pacific
- Enhanced Walker circulation

BJERKNES FEEDBACK:
dT_E/dt = γ × (convection anomaly)
d(trades)/dt = β × T_E anomaly

This coupled feedback creates OSCILLATION (2-7 year period).

Recharge oscillator theory (Jin 1997):
- El Niño depletes warm water from equatorial Pacific
- Warm water takes time to recharge (Rossby waves)
- Once recharged → system ready for next El Niño
"""
print(enso_physics)


# =============================================================================
# PART 7: UPWELLING AND COASTAL PRODUCTIVITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: UPWELLING PHYSICS")
print("=" * 70)

upwelling_text = """
COASTAL UPWELLING - WHERE OCEAN MEETS ATMOSPHERE:
=================================================

On eastern ocean boundaries (California, Peru, Namibia):
1. Equatorward winds blow parallel to coast
2. Ekman transport moves water OFFSHORE (right of wind)
3. Surface water removed → replaced from BELOW
4. Cold, nutrient-rich water rises = UPWELLING

Upwelling velocity:
w = (1/ρf) × ∂τ/∂x

Typical: w ≈ 10-100 m/day (0.1-1 mm/s)

Consequences:
1. Cold coastal water (SST 5-10°C below offshore)
2. High biological productivity (nutrients!)
3. Fish populations (Peru anchovy, California sardine)
4. Fog (cold water + warm air = condensation)

CLIMATE SENSITIVITY:
Upwelling depends on wind stress (τ).
Climate change → changed winds → changed upwelling
→ Major ecosystem impacts possible
"""
print(upwelling_text)

def upwelling_velocity(wind_stress, latitude, coast_length=500e3):
    """Estimate coastal upwelling velocity."""
    f = 2 * omega * np.sin(np.radians(latitude))
    # Simplified: w ~ τ/(ρ f L) for coastal divergence
    w = wind_stress / (rho_sw * abs(f) * coast_length)
    return w * 86400  # Convert m/s to m/day

print("\nUpwelling Velocity Estimates:")
print("-" * 50)
for tau in [0.05, 0.1, 0.15]:
    for lat in [20, 30, 40]:
        w = upwelling_velocity(tau, lat)
        print(f"τ = {tau:.2f} N/m², lat = {lat}°: w ≈ {w:.1f} m/day")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: OCEAN-CLIMATE COUPLING")
print("=" * 70)

summary = """
KEY OCEAN-CLIMATE PHYSICS:
==========================

1. HEAT CAPACITY
   Ocean stores 1000× more heat than atmosphere
   → Climate has inertia, "warming in pipeline"

2. THERMOHALINE CIRCULATION (AMOC)
   Density-driven from T and S differences
   → Transports 1 PW of heat northward
   → Potentially bistable (ON/OFF states)

3. WIND-DRIVEN CIRCULATION
   Ekman transport 90° to wind
   → Creates gyres, upwelling, western boundary currents
   → Gulf Stream warms Europe

4. SEA LEVEL RISE
   Thermal expansion + ice melt
   → Currently ~3.4 mm/yr
   → Accelerating

5. OCEAN ACIDIFICATION
   CO2 → carbonic acid → lower pH
   → Threatens shell-forming organisms
   → 30% more acidic than preindustrial

6. ENSO
   Coupled ocean-atmosphere oscillation
   → 2-7 year period
   → Global climate impacts

7. UPWELLING
   Wind-driven cold water rises
   → High productivity zones
   → Climate-sensitive ecosystems


WHAT THIS MEANS FOR CLIMATE:
============================
- Oceans BUFFER warming (delay but don't prevent)
- Oceans STORE CO2 (but become more acidic)
- Oceans CIRCULATE heat (but circulation may change)
- Ocean-atmosphere coupling creates natural variability
- Ocean changes will persist for centuries after CO2 stops

The ocean is the "flywheel" of the climate system.
"""
print(summary)

print("\n" + "=" * 70)
print("END OF OCEAN-CLIMATE COUPLING")
print("=" * 70)
