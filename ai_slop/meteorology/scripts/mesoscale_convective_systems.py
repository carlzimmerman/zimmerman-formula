#!/usr/bin/env python3
"""
MESOSCALE CONVECTIVE SYSTEMS - FIRST PRINCIPLES
================================================

Deriving the physics of squall lines, derechos, MCCs,
and organized convection from fundamental dynamics.
"""

import numpy as np

print("=" * 70)
print("MESOSCALE CONVECTIVE SYSTEMS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS AND PARAMETERS
# =============================================================================
g = 9.81           # Gravity (m/s²)
R_d = 287.0        # Gas constant dry air (J/kg/K)
c_p = 1004         # Specific heat (J/kg/K)
L_v = 2.5e6        # Latent heat of vaporization (J/kg)
rho_0 = 1.225      # Reference air density (kg/m³)


# =============================================================================
# PART 1: MCS CLASSIFICATION AND STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: MCS CLASSIFICATION")
print("=" * 70)

classification_text = """
MESOSCALE CONVECTIVE SYSTEM (MCS):
==================================

Definition: Organized convective complex
- Scale: 100-1000 km
- Duration: 6-24+ hours
- Contains multiple thunderstorms

TYPES:

1. SQUALL LINE (Linear MCS)
   - Linear convective region
   - Trailing stratiform region
   - Cold pool driven propagation
   - Length: 100-1000 km
   - Width: 20-50 km (convective)

2. MCC (Mesoscale Convective Complex)
   - Circular or elliptical
   - Cloud shield > 100,000 km²
   - Duration > 6 hours
   - Nocturnal maximum (US Great Plains)
   - Produces 30-70% of summer rainfall

3. BOW ECHO
   - Bowed segment in squall line
   - Strong rear-inflow jet
   - Damaging straight-line winds
   - Precursor to derecho

4. DERECHO
   - Widespread damaging winds
   - Swath > 400 km long
   - Gusts > 26 m/s (58 mph)
   - Duration > 3 hours
   - "Progressive" vs "Serial"

STRUCTURE (Classic Squall Line):

       Anvil spreading ←─────────────────────
       ╔═══════════════════════════════════════╗
       ║   Stratiform Region (Light Rain)      ║
       ║      ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓               ║
       ║        Melting level                  ║
       ╠═══════════════════════════════════════╣
       ║                                       ║
       ║  ↑ ↑ ↑ ↑ ↑                            ║
       ║  Convective ║  Cold Pool              ║
       ║   Updraft   ║  (Dense, cold)          ║
       ║     ↑       ║                         ║
       ╚═════╩═══════╩═════════════════════════╝
    ──────────────────────────────────────────────
           ← Motion                 GROUND

THE PHYSICS: Cold pool dynamics + wind shear balance
"""
print(classification_text)


# =============================================================================
# PART 2: COLD POOL DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: COLD POOL DYNAMICS")
print("=" * 70)

coldpool_text = """
COLD POOL FORMATION:
====================

Evaporation of rain cools air below cloud base
Cooled air descends as downdraft
Spreads along surface as DENSITY CURRENT

DENSITY CURRENT SPEED:

For density current (gravity current):

c = k √(g' × H)

Where:
- c = propagation speed
- k ≈ 0.7-1.0 (depends on current shape)
- g' = reduced gravity = g × (Δρ/ρ) ≈ g × (ΔT/T)
- H = cold pool depth

DERIVATION:
From Bernoulli's equation along streamline:
½ρc² = (Δρ) × g × H

c = √(2gH × Δρ/ρ) ≈ √(2g'H)

For typical cold pool:
- ΔT = 5-15 K
- T = 300 K
- H = 1-3 km
- g' = 9.81 × (10/300) = 0.33 m/s²

c = √(2 × 0.33 × 2000) = 36 m/s (too fast!)

With drag and mixing: c ≈ 10-25 m/s

COLD POOL INTENSITY (C):

C² = 2 × ∫₀ᴴ g(Θ̄ - Θ)/Θ̄ dz

Where Θ = potential temperature

Strong cold pool: C > 30 m/s
Moderate: C = 20-30 m/s
Weak: C < 20 m/s
"""
print(coldpool_text)

def cold_pool_speed(delta_T, depth_m, T_env=300, k=0.8):
    """
    Calculate cold pool propagation speed.

    Parameters:
    - delta_T: Temperature deficit (K)
    - depth_m: Cold pool depth (m)
    - T_env: Environmental temperature (K)
    - k: Empirical coefficient
    """
    g_prime = g * delta_T / T_env  # Reduced gravity
    c = k * np.sqrt(2 * g_prime * depth_m)
    return c

def cold_pool_intensity(delta_T, depth_m, T_env=300):
    """
    Calculate cold pool intensity C.
    Simplified assuming uniform ΔT.
    """
    C_squared = 2 * g * (delta_T / T_env) * depth_m
    return np.sqrt(C_squared)

print("\nCold Pool Propagation Speed:")
print("-" * 60)
print(f"{'ΔT (K)':<12} {'Depth (m)':<12} {'Speed (m/s)':<15} {'Intensity C'}")
print("-" * 60)

for dT in [5, 8, 10, 12, 15]:
    for H in [1000, 1500, 2000, 2500]:
        c = cold_pool_speed(dT, H)
        C = cold_pool_intensity(dT, H)
        print(f"{dT:<12} {H:<12} {c:<15.1f} {C:.1f}")
        break  # Just show one depth per dT


# =============================================================================
# PART 3: RKW THEORY - OPTIMAL SQUALL LINE STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: RKW THEORY (Rotunno-Klemp-Weisman)")
print("=" * 70)

rkw_text = """
RKW THEORY (1988):
==================

Key insight: Cold pool and wind shear must BALANCE
for optimal MCS structure and longevity

THE BALANCE:

Cold pool circulation (horizontal vorticity from buoyancy):
∂ω/∂t = -∂B/∂x  (buoyancy gradient generates vorticity)

Wind shear (environmental vorticity):
ω_env = ∂u/∂z

AT THE GUST FRONT:

Cold pool generates negative vorticity (clockwise)
Low-level shear generates positive vorticity (counter-clockwise)

OPTIMAL CONDITION (c/Δu ≈ 1):

C / Δu ≈ 1

Where:
- C = cold pool intensity (m/s)
- Δu = low-level wind shear magnitude (0-3 km)

THREE REGIMES:

1. C/Δu < 1: SHEAR DOMINANT
   - Updraft tilts downshear (over cold pool)
   - Discrete propagation, weaker system

2. C/Δu ≈ 1: OPTIMAL BALANCE
   - Deep upright updraft
   - Strongest, longest-lived system
   - Continuous propagation

3. C/Δu > 1: COLD POOL DOMINANT
   - Updraft tilts rearward (upshear)
   - Leading stratiform, weaker convection

IMPLICATION:
MCS intensity self-regulates!
Strong convection → strong cold pool → more balance needed
"""
print(rkw_text)

def rkw_ratio(cold_pool_intensity, shear_0_3km):
    """
    Calculate RKW ratio C/Δu.

    Optimal: ~1.0
    """
    if shear_0_3km == 0:
        return float('inf')
    return cold_pool_intensity / shear_0_3km

def rkw_regime(ratio):
    """Classify MCS regime based on RKW ratio."""
    if ratio < 0.7:
        return "Shear dominant"
    elif ratio < 1.3:
        return "Optimal balance"
    else:
        return "Cold pool dominant"

print("\nRKW Ratio Analysis:")
print("-" * 70)
print(f"{'C (m/s)':<12} {'Shear (m/s)':<15} {'C/Δu':<12} {'Regime':<20}")
print("-" * 70)

for C in [15, 20, 25, 30, 35]:
    for shear in [10, 15, 20, 25, 30]:
        ratio = rkw_ratio(C, shear)
        regime = rkw_regime(ratio)
        if C == 25:  # Show all shears for one C value
            print(f"{C:<12} {shear:<15} {ratio:<12.2f} {regime:<20}")


# =============================================================================
# PART 4: REAR-INFLOW JET
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: REAR-INFLOW JET")
print("=" * 70)

rij_text = """
REAR-INFLOW JET (RIJ):
======================

A key feature of mature MCSs is the REAR-INFLOW JET:
Strong mid-level flow entering from behind the system

FORMATION MECHANISM:

1. Latent heating in stratiform region
   - Creates warm anomaly aloft

2. Evaporative cooling below melting level
   - Creates cold anomaly at mid-levels

3. Hydrostatic response:
   - Low pressure behind convective line (from heating)
   - Horizontal pressure gradient drives rear inflow

STRENGTH:

From thermal wind balance:
∂u_RIJ/∂z ≈ -(g/fT) × ∂T/∂y

Typical RIJ: 15-30 m/s at 3-5 km altitude

IF RIJ DESCENDS TO SURFACE:
→ Damaging straight-line winds (derecho!)

DESCENT MECHANISM:
- Evaporative cooling makes RIJ air negatively buoyant
- Precipitation loading
- Downward directed pressure gradient

BOW ECHO FORMATION:
- Strong RIJ momentum brought to surface
- Pushes convective line into bow shape
- Rear-inflow notch visible on radar
"""
print(rij_text)

def rear_inflow_strength(delta_T_stratiform, depth_km, length_km):
    """
    Estimate rear-inflow jet strength.

    Simplified from pressure gradient force.
    """
    # Pressure perturbation from heating
    # Δp'/Δx ≈ ρ × g × (ΔT/T) × H / L
    delta_p_per_x = rho_0 * g * (delta_T_stratiform / 300) * (depth_km * 1000) / (length_km * 1000)

    # Acceleration: a = (1/ρ) × dp/dx
    # Over time t: u = a × t, where t ≈ L/u (self-consistent)
    # u² ≈ Δp / ρ
    u_rij = np.sqrt(abs(delta_p_per_x) * length_km * 1000 / rho_0)

    return u_rij

print("\nRear-Inflow Jet Estimates:")
print("-" * 60)

for dT in [3, 5, 8]:  # Heating anomaly (K)
    for depth in [3, 5, 7]:  # km
        u_rij = rear_inflow_strength(dT, depth, 100)
        print(f"ΔT = {dT} K, depth = {depth} km: RIJ ≈ {u_rij:.0f} m/s")


# =============================================================================
# PART 5: DERECHO PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: DERECHO DYNAMICS")
print("=" * 70)

derecho_text = """
DERECHO REQUIREMENTS:
=====================

Definition: Widespread convective windstorm
- Damage swath > 400 km (250 miles)
- Multiple gusts > 26 m/s (58 mph)
- Many reports > 33 m/s (74 mph)

TYPES:

1. PROGRESSIVE DERECHO
   - Single MCS moves along mean wind
   - Common in weak synoptic flow
   - Summer, often nocturnal

2. SERIAL DERECHO
   - Multiple bowing segments
   - Along strong synoptic boundary
   - More common in spring
   - More widespread damage

FAVORABLE CONDITIONS:

1. HIGH INSTABILITY
   - CAPE > 2000 J/kg
   - Deep tropospheric warmth

2. MODERATE-STRONG SHEAR
   - 0-6 km shear > 15 m/s
   - Low-level shear for rotation

3. DRY MID-LEVELS
   - Strong evaporative cooling
   - Enhanced cold pool / RIJ

4. AXIS OF MAXIMUM THETA-E
   - Concentrated moisture/instability
   - "Warm tongue" pattern

PEAK GUST ESTIMATION:

Surface gust ≈ RIJ + cold pool speed + turbulent enhancement

V_max ≈ √(V_RIJ² + C² + 2×DCAPE/ρ)

Where DCAPE = downdraft CAPE (convective potential for downdraft)

DCAPE = ∫(g × (T_env - T_parcel)/T_env) dz  (over negative buoyancy layer)
"""
print(derecho_text)

def derecho_gust_estimate(rij_speed, cold_pool_speed, dcape):
    """
    Estimate peak derecho surface gust.

    Combines RIJ, cold pool, and downdraft acceleration.
    """
    downdraft_contrib = np.sqrt(2 * dcape)  # From DCAPE

    # Not simply additive - use vector combination estimate
    v_max = np.sqrt(rij_speed**2 + cold_pool_speed**2) + 0.5 * downdraft_contrib

    return v_max

print("\nDerecho Gust Estimates:")
print("-" * 70)
print(f"{'RIJ (m/s)':<12} {'C (m/s)':<12} {'DCAPE (J/kg)':<15} {'Gust (m/s)':<12} {'mph'}")
print("-" * 70)

for rij in [20, 25, 30]:
    for C in [20, 25, 30]:
        for dcape in [500, 800, 1200]:
            gust = derecho_gust_estimate(rij, C, dcape)
            gust_mph = gust * 2.237
            if dcape == 800:  # Show one DCAPE per combination
                print(f"{rij:<12} {C:<12} {dcape:<15} {gust:<12.0f} {gust_mph:.0f}")


# =============================================================================
# PART 6: NOCTURNAL MCS / LLJ INTERACTION
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: NOCTURNAL CONVECTION AND LOW-LEVEL JET")
print("=" * 70)

nocturnal_text = """
WHY MCSs PEAK AT NIGHT (Central US):
====================================

OBSERVATION: MCCs and MCSs maximize between midnight and 6 AM!

This seems counterintuitive (no solar heating)

EXPLANATION: LOW-LEVEL JET (LLJ)

1. DAYTIME:
   - Surface heating creates turbulent mixing
   - Momentum mixed down, winds weaker at surface
   - PBL deep (1-2 km), well-mixed

2. EVENING:
   - Surface cools, stable layer forms
   - Turbulent mixing ceases
   - Residual layer (former PBL) decouples from surface

3. NOCTURNAL:
   - Inertial oscillation begins
   - Geostrophic departure from daytime friction
   - Wind ACCELERATES above stable layer
   - Peak LLJ at 500-1000 m

4. LLJ CHARACTERISTICS:
   - Speed: 15-30 m/s (often > 50 mph)
   - Height: 300-1000 m AGL
   - Peak: 2-4 hours after sunset
   - Southerly over Great Plains (moisture transport!)

INERTIAL OSCILLATION:

After decoupling, wind undergoes inertial oscillation:
V(t) = V_g + (V_0 - V_g) × exp(ift)

Where f = Coriolis parameter

Period = 2π/f ≈ 17 hours at 40°N
So LLJ peaks before dawn (half period ~8-9 hours after sunset)

CONSEQUENCE FOR MCSs:

- LLJ transports massive moisture northward
- Convergence at LLJ terminus
- Lifts air in presence of elevated instability
- Feeds existing MCSs from below
- MCS can persist / intensify all night!
"""
print(nocturnal_text)

def llj_speed(V_geo, V_sfc_day, lat, hours_after_sunset):
    """
    Simple model of LLJ speed evolution.

    Based on inertial oscillation after decoupling.
    """
    f = 2 * 7.29e-5 * np.sin(np.radians(lat))
    T_inertial = 2 * np.pi / abs(f) / 3600  # hours

    # Friction-induced departure (daytime)
    V_departure = V_sfc_day - V_geo

    # Oscillation phase
    phase = 2 * np.pi * hours_after_sunset / T_inertial

    # Speed (simplified - actually should be vector rotation)
    V_llj = V_geo + abs(V_departure) * np.sin(phase)

    return V_llj, T_inertial

print("\nLow-Level Jet Evolution:")
print("-" * 60)
print("Lat = 40°N, V_geo = 15 m/s, V_sfc_day = 8 m/s")
print("-" * 60)
print(f"{'Hours after sunset':<22} {'LLJ speed (m/s)':<20}")
print("-" * 60)

for hours in [0, 2, 4, 6, 8, 10, 12]:
    v_llj, T = llj_speed(15, 8, 40, hours)
    print(f"{hours:<22} {v_llj:<20.1f}")

print(f"\nInertial period at 40°N: {T:.1f} hours")


# =============================================================================
# PART 7: MCS PROPAGATION MECHANISMS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: MCS PROPAGATION")
print("=" * 70)

propagation_text = """
MCS PROPAGATION MECHANISMS:
===========================

MCSs often move DIFFERENT from mean wind!

1. COLD POOL PROPAGATION (Primary)
   - Density current spreading
   - Lifts unstable air at leading edge
   - Creates new cells
   - Speed: C ≈ √(2g'H)

2. DISCRETE PROPAGATION
   - New cells form ahead of existing line
   - Triggered by:
     - Gravity waves from existing storms
     - Outflow boundaries
     - Convergence ahead of system
   - Can be faster than cold pool!

3. STEERING-LEVEL FLOW
   - Deep-layer mean wind (850-300 hPa)
   - Advects entire system
   - Typically 60-70% of system motion

SYSTEM VELOCITY:

V_sys = α × V_mean + β × V_cold_pool + V_discrete

Where:
- α ≈ 0.6-0.8 (mean wind contribution)
- β ≈ 0.2-0.4 (cold pool contribution)
- V_discrete depends on instability field

FORWARD PROPAGATING vs BACK-BUILDING:

FORWARD: Cold pool pushes leading edge outward
- Common mode
- Cold pool > shear

BACK-BUILDING: New cells form on upwind side
- Quasi-stationary or slowly moving
- Can produce extreme rainfall (training effect!)
- Often where cold pool and inflow meet
- Flash flood producer!
"""
print(propagation_text)

def mcs_speed(mean_wind_speed, cold_pool_speed, propagation_angle=0):
    """
    Estimate MCS propagation speed.

    Simplified combination of steering flow and cold pool.
    """
    alpha = 0.7  # Mean wind contribution
    beta = 0.3   # Cold pool contribution

    # Assume same direction for simplicity
    v_sys = alpha * mean_wind_speed + beta * cold_pool_speed

    # With discrete propagation component
    v_discrete = 3  # m/s typical

    return v_sys + v_discrete

print("\nMCS Speed Estimation:")
print("-" * 55)
print(f"{'Mean wind (m/s)':<18} {'Cold pool (m/s)':<18} {'System (m/s)'}")
print("-" * 55)

for v_mean in [10, 15, 20, 25]:
    for c_pool in [15, 20, 25]:
        v_sys = mcs_speed(v_mean, c_pool)
        if c_pool == 20:
            print(f"{v_mean:<18} {c_pool:<18} {v_sys:.1f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: MESOSCALE CONVECTIVE SYSTEMS")
print("=" * 70)

summary = """
KEY MCS PHYSICS:
===============

1. COLD POOL DYNAMICS
   - Evaporatively-cooled downdraft spreads as density current
   - Speed: C = k√(2g'H), typically 15-30 m/s
   - Lifts air at leading edge, triggers new convection

2. RKW BALANCE (C/Δu ≈ 1)
   - Cold pool circulation vs wind shear vorticity
   - Optimal: upright updraft, longest-lived MCS
   - Self-regulating system

3. REAR-INFLOW JET
   - Mid-level flow from stratiform region
   - Driven by pressure gradients from latent heating
   - Strength: 15-30 m/s
   - Descent = damaging winds (derecho!)

4. DERECHO FORMATION
   - Strong RIJ + cold pool + DCAPE
   - Requires instability + moderate-strong shear + dry mid-levels
   - Progressive vs serial types

5. NOCTURNAL ENHANCEMENT
   - Low-level jet from inertial oscillation
   - Peaks 6-10 hours after sunset
   - Massive moisture transport
   - Feeds overnight MCSs

6. PROPAGATION
   - Steering flow (60-70%) + cold pool (20-30%)
   - Discrete propagation from gravity waves
   - Back-building = flash flood threat


THE PHYSICS TELLS US:
====================
- MCSs are fundamentally driven by cold pool dynamics
- Balance with wind shear determines structure and longevity
- RIJ controls severe wind potential
- Nocturnal LLJ enables overnight intensification
- Simple equations (density current, thermal wind) explain behavior
"""
print(summary)

print("\n" + "=" * 70)
print("END OF MESOSCALE CONVECTIVE SYSTEMS")
print("=" * 70)
