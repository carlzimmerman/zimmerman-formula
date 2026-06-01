#!/usr/bin/env python3
"""
TROPICAL CYCLONE GENESIS - FIRST PRINCIPLES
============================================

Deriving the physics of hurricane formation:
from tropical disturbance to organized vortex.
"""

import numpy as np

print("=" * 70)
print("TROPICAL CYCLONE GENESIS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
omega = 7.29e-5    # Earth rotation (rad/s)
R_earth = 6.371e6  # Earth radius (m)
g = 9.81           # Gravity (m/s²)
c_p = 1004         # Specific heat (J/kg/K)
L_v = 2.5e6        # Latent heat of vaporization (J/kg)


# =============================================================================
# PART 1: NECESSARY CONDITIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: CONDITIONS FOR TROPICAL CYCLOGENESIS")
print("=" * 70)

conditions_text = """
NECESSARY CONDITIONS FOR TC FORMATION:
======================================

GRAY'S 6 CONDITIONS (1968):

1. SEA SURFACE TEMPERATURE ≥ 26.5°C
   - Provides energy source
   - Actually need warm ocean to depth (~50m)
   - Ocean heat content matters more than SST alone

2. SUFFICIENT CORIOLIS FORCE
   - Typically > 5° from equator
   - f = 2Ω sin(φ)
   - Needed to spin up vortex

3. LOW VERTICAL WIND SHEAR
   - |∂V/∂z| < 10-15 m/s over 850-200 hPa
   - High shear ventilates heat, tilts vortex
   - Disrupts organized convection

4. CONDITIONAL INSTABILITY
   - CAPE > 1000 J/kg typical
   - Deep convection must be possible
   - Moist mid-levels important

5. HIGH MID-LEVEL RELATIVE HUMIDITY
   - RH > 40-50% at 500 hPa
   - Dry air = entrainment kills convection
   - "Saharan Air Layer" suppresses Atlantic TCs

6. PRE-EXISTING DISTURBANCE
   - Some initial vorticity
   - Low-level convergence
   - Examples: African Easterly Waves, monsoon troughs

WHY SST > 26.5°C?

Empirical observation, but physical basis:
- Surface saturation vapor pressure: e_s(26.5°C) ≈ 35 hPa
- Enough evaporation to fuel convection
- Ocean heat content must sustain energy extraction

GENESIS POTENTIAL INDEX (GPI):

GPI ∝ |η|³ × (RH)³ × (PI)³ × (1 + 0.1 × V_shear)⁻²

Where:
- η = absolute vorticity
- RH = relative humidity (600 hPa)
- PI = potential intensity
- V_shear = wind shear
"""
print(conditions_text)

def coriolis_parameter(latitude):
    """Calculate Coriolis parameter at latitude."""
    return 2 * omega * np.sin(np.radians(latitude))

def saturation_vapor_pressure(T_celsius):
    """Clausius-Clapeyron: saturation vapor pressure (hPa)."""
    return 6.11 * 10**(7.5 * T_celsius / (237.3 + T_celsius))

def genesis_potential_index(abs_vorticity, RH_600, PI_ms, shear_ms):
    """
    Calculate Genesis Potential Index.

    Simplified from Emanuel & Nolan (2004).
    """
    # Clamp values
    eta = max(abs_vorticity, 1e-6)
    rh = max(RH_600 / 100, 0.01)
    pi = max(PI_ms, 1)
    shear = max(shear_ms, 1)

    gpi = (1e5 * eta)**3 * (rh)**3 * (pi / 70)**3 * (1 + 0.1 * shear)**(-2)
    return gpi

print("\nCoriolis Parameter by Latitude:")
print("-" * 50)
print(f"{'Latitude':<15} {'f (10⁻⁵ s⁻¹)':<20} {'Genesis possible?'}")
print("-" * 50)

for lat in [0, 3, 5, 10, 15, 20, 30]:
    f = coriolis_parameter(lat)
    genesis = "Yes" if lat >= 5 else "No (too close to equator)"
    print(f"{lat}°{'':<12} {f*1e5:<20.2f} {genesis}")


# =============================================================================
# PART 2: VORTICITY DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: VORTICITY DYNAMICS IN GENESIS")
print("=" * 70)

vorticity_text = """
VORTICITY EQUATION:
===================

D(ζ + f)/Dt = -(ζ + f)(∇·V) + tilting + friction

Where:
- ζ = relative vorticity
- f = planetary vorticity (Coriolis)
- (ζ + f) = absolute vorticity

KEY TERM: VORTEX STRETCHING

-(ζ + f)(∇·V)

When ∇·V < 0 (convergence):
Absolute vorticity INCREASES

This is how convection spins up a vortex!

CONVERGENCE FROM CONVECTION:

Mass continuity: ∂ρ/∂t + ∇·(ρV) = 0

Low-level convergence feeds updrafts
ΔV ≈ w × H / r

Typical values:
- w = 5 m/s (updraft)
- H = 10 km
- r = 200 km
- ΔV ≈ 0.25 m/s convergence

VORTICITY SPIN-UP RATE:

Dζ/Dt ≈ (ζ + f) × (-∇·V)

For f = 5×10⁻⁵ s⁻¹, convergence = 2×10⁻⁵ s⁻¹:
Dζ/Dt ≈ 10⁻⁹ s⁻² = 0.003 hr⁻¹

Time to spin up: ~1-3 days

WHY CORIOLIS MATTERS:

Without f, convergence creates ζ but it's not organized
f provides "seed" vorticity for stretching
Also deflects inflow → promotes circulation
"""
print(vorticity_text)

def vortex_stretching_rate(abs_vorticity, convergence):
    """
    Calculate vorticity tendency from stretching.

    dζ/dt = (ζ + f) × (-∇·V)
    """
    return abs_vorticity * convergence

def spinup_time(target_vorticity, initial_vorticity, stretching_rate):
    """
    Estimate time to spin up vortex.

    Assumes constant stretching rate.
    """
    if stretching_rate <= 0:
        return float('inf')
    return (target_vorticity - initial_vorticity) / stretching_rate / 3600  # hours

print("\nVorticity Spin-up Estimates:")
print("-" * 65)
print(f"{'Convergence (10⁻⁵/s)':<22} {'Initial ζ (10⁻⁵/s)':<22} {'Spinup time (hrs)'}")
print("-" * 65)

f_10N = coriolis_parameter(10)

for conv in [1, 2, 5, 10]:
    for zeta_0 in [0, 2, 5]:
        abs_vort = (zeta_0 * 1e-5 + f_10N)
        stretch = vortex_stretching_rate(abs_vort, conv * 1e-5)
        time_hrs = spinup_time(20e-5, (zeta_0 * 1e-5 + f_10N), stretch)
        if conv == 2:
            print(f"{conv:<22} {zeta_0:<22} {time_hrs:.0f}")


# =============================================================================
# PART 3: WIND-INDUCED SURFACE HEAT EXCHANGE (WISHE)
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: WISHE FEEDBACK MECHANISM")
print("=" * 70)

wishe_text = """
WISHE - WIND-INDUCED SURFACE HEAT EXCHANGE:
===========================================

The key positive feedback for TC intensification
(Emanuel, 1986)

SURFACE ENTHALPY FLUX:

F_k = ρ C_k |V| (k_s* - k)

Where:
- C_k ≈ 1.2×10⁻³ (transfer coefficient)
- |V| = surface wind speed
- k_s* = saturation enthalpy at SST
- k = actual air enthalpy

THE FEEDBACK LOOP:

1. Initial disturbance → low pressure
2. Pressure gradient → inflow winds
3. Stronger winds → more evaporation (F ∝ |V|)
4. More evaporation → more latent heat
5. Latent heat released in convection → pressure falls
6. Lower pressure → stronger winds
→ REPEAT (positive feedback!)

CRITICAL POINT:

Feedback only works if:
- SST warm enough (high k_s*)
- Air-sea disequilibrium sufficient
- Organized convection established

THRESHOLD BEHAVIOR:

Below ~15 m/s: Feedback weak
Above ~15 m/s: Runaway intensification begins
This explains why genesis is "threshold-like"

ENTROPY BUDGET:

∂s/∂t = F_k/(T×h_pbl) - s_out + sources

Steady state: Input = export through outflow
"""
print(wishe_text)

def surface_enthalpy_flux(wind_speed_ms, SST_C, air_T_C, air_RH):
    """
    Calculate surface enthalpy flux.

    Simplified WISHE calculation.
    """
    rho = 1.2  # kg/m³
    C_k = 1.2e-3  # Transfer coefficient
    c_p = 1004  # J/kg/K

    # Saturation specific humidity at SST
    e_s_sst = saturation_vapor_pressure(SST_C)
    q_s = 0.622 * e_s_sst / 1013

    # Actual specific humidity
    e_s_air = saturation_vapor_pressure(air_T_C)
    e = air_RH / 100 * e_s_air
    q = 0.622 * e / 1013

    # Enthalpy difference (simplified)
    delta_k = c_p * (SST_C - air_T_C) + L_v * (q_s - q)

    # Flux
    F = rho * C_k * wind_speed_ms * delta_k
    return F

def wishe_amplification_factor(wind_speed_ms):
    """
    Estimate WISHE amplification.

    Feedback strength increases with wind speed.
    """
    # Simplified: linear until saturation
    if wind_speed_ms < 5:
        return 1.0
    elif wind_speed_ms < 30:
        return 1 + 0.1 * (wind_speed_ms - 5)
    else:
        return 3.5  # Saturates

print("\nWISHE Surface Flux vs Wind Speed:")
print("(SST = 29°C, Air T = 27°C, RH = 80%)")
print("-" * 55)
print(f"{'Wind (m/s)':<15} {'Flux (W/m²)':<20} {'Feedback strength'}")
print("-" * 55)

for V in [5, 10, 15, 20, 25, 30, 40]:
    F = surface_enthalpy_flux(V, 29, 27, 80)
    amp = wishe_amplification_factor(V)
    print(f"{V:<15} {F:<20.0f} {amp:.1f}×")


# =============================================================================
# PART 4: PATHWAYS TO GENESIS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: PATHWAYS TO GENESIS")
print("=" * 70)

pathways_text = """
MULTIPLE PATHWAYS TO TC GENESIS:
================================

1. AFRICAN EASTERLY WAVES (AEWs)
   - Originate over Africa from thermal contrasts
   - Period: 3-5 days
   - Wavelength: 2000-4000 km
   - Track westward at 7-8 m/s
   - Seed 60% of Atlantic hurricanes
   - Provide initial vorticity + convection

2. MONSOON TROUGH / ITCZ BREAKDOWN
   - Monsoon trough becomes wavy
   - Barotropic instability
   - Creates closed circulations
   - Common in W Pacific, N Indian Ocean

3. SUBTROPICAL INTRUSION
   - Upper trough → cutoff low
   - Induces convection below
   - Can trigger genesis at higher latitudes
   - "Subtropical storm" formation

4. MESOVORTEX AGGREGATION
   - Multiple MCSs in favorable environment
   - Vortices merge → larger circulation
   - "Bottom-up" development
   - Common in W Pacific monsoon

5. EASTERLY WAVE + MJO INTERACTION
   - MJO enhances: low shear, high moisture
   - AEW provides disturbance
   - Combined effect → genesis

GENESIS TIMING:

Pre-genesis: 1-5 days
Messy convection → organization
Key milestone: "Closed low" at 850 hPa

MARSUPIAL PARADIGM (Dunkerton et al.):

Wave's "pouch" - closed circulation in co-moving frame
Protects developing vortex from:
- Dry air intrusion
- Deformation by shear

Genesis occurs when:
- Pouch is deep (extends to surface)
- Convection focused in pouch center
- WISHE feedback activates
"""
print(pathways_text)

def aew_tracking_probability(sst_C, shear_ms, rh_600):
    """
    Estimate probability of AEW developing into TC.

    Simplified genesis probability.
    """
    prob = 0.0

    # SST contribution
    if sst_C > 26.5:
        prob += 0.2 * (sst_C - 26.5)

    # Shear contribution (low is good)
    if shear_ms < 10:
        prob += 0.3
    elif shear_ms < 20:
        prob += 0.15

    # Humidity contribution
    prob += 0.3 * (rh_600 / 100)

    return min(prob, 0.8)

print("\nAEW Development Probability:")
print("-" * 65)
print(f"{'SST (°C)':<12} {'Shear (m/s)':<15} {'RH 600 (%)':<15} {'P(genesis)'}")
print("-" * 65)

for sst in [26, 27, 28, 29]:
    for shear in [5, 15, 25]:
        for rh in [40, 60, 80]:
            prob = aew_tracking_probability(sst, shear, rh)
            if shear == 15:
                print(f"{sst:<12} {shear:<15} {rh:<15} {prob:.0%}")


# =============================================================================
# PART 5: POUCH DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: POUCH DYNAMICS")
print("=" * 70)

pouch_text = """
THE MARSUPIAL POUCH:
====================

WAVE CRITICAL LAYER:

In frame moving with wave:
- Closed streamlines form at critical level
- Where phase speed = flow speed

POUCH = Protected region within wave

POUCH PROPERTIES:

1. RECIRCULATING FLOW
   Air parcels cycle within pouch
   Residence time: 1-2 days
   Allows vorticity accumulation

2. PROTECTION FROM ENVIRONMENT
   Shear can't penetrate
   Dry air stays outside
   "Incubator" for vortex

3. DEEP VS SHALLOW POUCH

   Deep pouch: Extends to surface
   → Surface fluxes feed convection
   → WISHE can operate
   → Genesis likely

   Shallow pouch: Elevated (850-700 hPa only)
   → Disconnected from surface
   → Limited energy source
   → Genesis unlikely

SWEET SPOT HYPOTHESIS:

Convection must be:
- Inside pouch (protected)
- Near pouch center (max vorticity)
- Deep (latent heat release)

POUCH TRACKING FORECAST:

Track wave in 850-600 hPa mean flow
Identify pouch center
Monitor convection within pouch
Assess pouch depth
"""
print(pouch_text)

def pouch_residence_time(wave_speed_ms, pouch_radius_km):
    """
    Estimate parcel residence time in pouch.
    """
    # Circulation time ~ 2πr / perturbation_wind
    # Perturbation wind ~ wave_speed / 3 (rough)
    v_pert = wave_speed_ms / 3
    if v_pert < 1:
        v_pert = 1
    t_hours = 2 * np.pi * pouch_radius_km * 1000 / (v_pert * 3600)
    return t_hours

print("\nPouch Characteristics:")
print("-" * 50)
print(f"{'Wave speed (m/s)':<20} {'Pouch radius (km)':<20} {'Residence (hrs)'}")
print("-" * 50)

for c in [6, 8, 10]:
    for r in [200, 300, 400]:
        t = pouch_residence_time(c, r)
        print(f"{c:<20} {r:<20} {t:.0f}")


# =============================================================================
# PART 6: GENESIS CLIMATOLOGY
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: GENESIS CLIMATOLOGY")
print("=" * 70)

climate_text = """
GLOBAL GENESIS DISTRIBUTION:
============================

ANNUAL TC FORMATION (1991-2020 average):

Basin                   TCs/year    Hurricanes/year
─────────────────────────────────────────────────────
W Pacific (WPAC)        26          16
E Pacific (EPAC)        17          9
Atlantic (ATL)          14          7
N Indian (NIO)          5           2
S Indian (SIO)          12          6
Australia (AUS)         11          5
S Pacific (SPAC)        9           4
─────────────────────────────────────────────────────
GLOBAL                  ~85         ~50

SEASONAL CYCLE:

Atlantic: Peak Aug-Sep (peak shear minimum, SST max)
E Pacific: Peak Aug (SST + waves)
W Pacific: Year-round (warm pool always active)
N Indian: May-Jun, Oct-Nov (monsoon transitions)

GENESIS DENSITY:

Highest: W Pacific warm pool, Caribbean
Lowest: S Atlantic (almost never), SE Pacific

WHY NO S ATLANTIC TCs?

1. High shear (subtropical jet)
2. Cool SST (upwelling)
3. No African waves
4. Stable SAL-like air

First recorded S Atlantic hurricane: Catarina, 2004

MJO INFLUENCE:

Active MJO phases enhance genesis
Phases 1-3: Indian Ocean
Phases 4-6: Maritime Continent
Phases 7-8: W Pacific

MJO explains 50% of intraseasonal genesis variance!
"""
print(climate_text)

def seasonal_genesis_prob(month, basin='atlantic'):
    """
    Relative genesis probability by month.
    """
    if basin == 'atlantic':
        # Peak in Sep
        probs = [0, 0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.25, 0.25, 0.12, 0.04, 0.01]
    elif basin == 'epac':
        # Peak in Aug
        probs = [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.22, 0.22, 0.12, 0.05, 0.01, 0]
    else:  # wpac
        # More uniform
        probs = [0.05, 0.05, 0.05, 0.07, 0.08, 0.1, 0.12, 0.12, 0.1, 0.1, 0.08, 0.08]

    return probs[month - 1]

print("\nMonthly Genesis Probability by Basin:")
print("-" * 55)
print(f"{'Month':<10} {'Atlantic':<15} {'E Pacific':<15} {'W Pacific'}")
print("-" * 55)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i, mon in enumerate(months, 1):
    atl = seasonal_genesis_prob(i, 'atlantic')
    epac = seasonal_genesis_prob(i, 'epac')
    wpac = seasonal_genesis_prob(i, 'wpac')
    print(f"{mon:<10} {atl:<15.0%} {epac:<15.0%} {wpac:.0%}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: TROPICAL CYCLONE GENESIS")
print("=" * 70)

summary = """
KEY GENESIS PHYSICS:
===================

1. NECESSARY CONDITIONS
   - SST > 26.5°C (energy)
   - Coriolis > 5° latitude (spin)
   - Low vertical shear (structure)
   - High mid-level humidity (convection)
   - Pre-existing disturbance (trigger)

2. VORTICITY DYNAMICS
   - Vortex stretching: dζ/dt = (ζ+f)×convergence
   - Convection provides convergence
   - Spin-up time: 1-3 days
   - Coriolis provides seed vorticity

3. WISHE FEEDBACK
   - Wind → evaporation → heat → pressure drop → more wind
   - Flux F ∝ |V| × (k*_s - k)
   - Threshold ~15 m/s for runaway
   - Key positive feedback

4. GENESIS PATHWAYS
   - African Easterly Waves (60% Atlantic)
   - Monsoon trough breakdown
   - Subtropical intrusion
   - MCS vortex merger

5. POUCH DYNAMICS
   - Protected region in wave
   - Deep pouch → surface connection → genesis
   - Shallow pouch → no genesis
   - Convection must be inside pouch

6. CLIMATOLOGY
   - ~85 TCs globally per year
   - W Pacific most active
   - Strong seasonal cycles
   - MJO modulates 50% variance


THE PHYSICS TELLS US:
====================
- Genesis is threshold-like (not gradual)
- WISHE is the key feedback
- Pouch protection enables development
- Multiple conditions must align
- Forecasting genesis remains challenging
"""
print(summary)

print("\n" + "=" * 70)
print("END OF TROPICAL CYCLONE GENESIS")
print("=" * 70)
