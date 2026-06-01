#!/usr/bin/env python3
"""
HYDROLOGY AND FLOOD PHYSICS - FIRST PRINCIPLES
===============================================

Deriving the physics of rainfall-runoff, flood prediction,
river hydraulics, and extreme precipitation events.
"""

import numpy as np

print("=" * 70)
print("HYDROLOGY AND FLOOD PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
rho_water = 1000   # Water density (kg/m³)


# =============================================================================
# PART 1: THE HYDROLOGIC CYCLE
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: HYDROLOGIC CYCLE")
print("=" * 70)

cycle_text = """
THE HYDROLOGIC CYCLE:
=====================

CONSERVATION OF MASS (Water Budget):

dS/dt = P - ET - R

Where:
- S = Storage (soil, groundwater, snow)
- P = Precipitation
- ET = Evapotranspiration
- R = Runoff (streamflow)

GLOBAL WATER BUDGET:

                  Volume (10³ km³)    Flux (10³ km³/yr)
───────────────────────────────────────────────────────
Oceans            1,335,000           Evap: 434
Ice/glaciers      24,000              -
Groundwater       10,600              -
Lakes             176                 -
Soil moisture     16                  -
Atmosphere        13                  Precip: 113 (land)
Rivers            2                   Runoff: 45

RESIDENCE TIMES:

τ = Storage / Flux

Atmosphere: 13/500 × 365 ≈ 10 days
Rivers: 2/45 × 365 ≈ 16 days
Groundwater: 10,600/1.7 ≈ 6,000 years!
Oceans: 1,335,000/434 ≈ 3,000 years

PRECIPITATION TYPES:

1. FRONTAL (Stratiform)
   - Large area, moderate intensity
   - Hours to days duration
   - 1-10 mm/hr

2. CONVECTIVE
   - Small area, high intensity
   - Minutes to hours
   - 10-100+ mm/hr

3. OROGRAPHIC
   - Mountain-forced
   - Persistent
   - 5-50 mm/hr
"""
print(cycle_text)

def residence_time(storage, flux):
    """Calculate residence time in years."""
    return storage / flux

def water_budget(precip, et, runoff, storage_change):
    """
    Check water budget closure.

    Returns: imbalance (should be ~0)
    """
    return precip - et - runoff - storage_change

print("\nReservoir Residence Times:")
print("-" * 50)
reservoirs = [
    ("Atmosphere", 13, 500),
    ("Rivers", 2, 45),
    ("Soil moisture", 16, 70),
    ("Lakes", 176, 3),
    ("Groundwater", 10600, 1.7),
    ("Oceans", 1335000, 434),
]

print(f"{'Reservoir':<20} {'Storage (10³km³)':<18} {'Residence time'}")
print("-" * 50)

for name, storage, flux in reservoirs:
    tau = residence_time(storage, flux)
    if tau < 1:
        print(f"{name:<20} {storage:<18} {tau*365:.0f} days")
    else:
        print(f"{name:<20} {storage:<18} {tau:.0f} years")


# =============================================================================
# PART 2: RAINFALL-RUNOFF
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: RAINFALL-RUNOFF TRANSFORMATION")
print("=" * 70)

runoff_text = """
RAINFALL-RUNOFF TRANSFORMATION:
===============================

Not all rain becomes runoff!

PARTITION:

P = R + ET + ΔS + Infiltration + Interception

LOSSES:
- Interception: Rain caught by vegetation
- Infiltration: Water enters soil
- ET: Evaporation + transpiration
- Depression storage: Fills puddles

INFILTRATION (Horton's equation):

f(t) = f_c + (f_0 - f_c) × e^(-kt)

Where:
- f_0 = initial infiltration capacity
- f_c = final (saturated) capacity
- k = decay constant

RUNOFF GENERATION MECHANISMS:

1. HORTONIAN (Infiltration-excess)
   - Rainfall > infiltration capacity
   - Common in urban areas, arid lands
   - Surface runoff

2. SATURATION-EXCESS
   - Soil saturates from below
   - Water table rises to surface
   - Common in humid climates

3. SUBSURFACE STORMFLOW
   - Water moves through soil
   - Reaches stream via shallow flow
   - Slower response

RUNOFF COEFFICIENT:

C = Runoff / Rainfall

Urban (impervious): C = 0.7-0.95
Suburban: C = 0.3-0.5
Forest: C = 0.1-0.3
"""
print(runoff_text)

def horton_infiltration(t_hours, f0=50, fc=10, k=2):
    """
    Horton's infiltration equation.

    f(t) = fc + (f0 - fc) × exp(-kt)
    Returns infiltration rate in mm/hr
    """
    return fc + (f0 - fc) * np.exp(-k * t_hours)

def runoff_coefficient_estimate(impervious_fraction, soil_type='medium'):
    """
    Estimate runoff coefficient.

    Based on impervious fraction and soil type.
    """
    base = {'sand': 0.1, 'medium': 0.2, 'clay': 0.35}
    C = impervious_fraction * 0.95 + (1 - impervious_fraction) * base[soil_type]
    return C

print("\nHorton Infiltration Over Time:")
print("-" * 50)
print(f"{'Time (hr)':<12} {'Infiltration (mm/hr)':<25}")
print("-" * 50)

for t in [0, 0.5, 1, 2, 4, 8, 12]:
    f = horton_infiltration(t)
    print(f"{t:<12} {f:<25.1f}")

print("\n\nRunoff Coefficients by Land Use:")
print("-" * 55)
print(f"{'Land use':<25} {'Impervious %':<15} {'Runoff coef'}")
print("-" * 55)

land_uses = [
    ("Dense urban", 0.85),
    ("Suburban residential", 0.40),
    ("Parks / open space", 0.10),
    ("Forest", 0.05),
    ("Agricultural", 0.20),
]

for name, imperv in land_uses:
    C = runoff_coefficient_estimate(imperv)
    print(f"{name:<25} {imperv*100:<15.0f} {C:.2f}")


# =============================================================================
# PART 3: UNIT HYDROGRAPH
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: UNIT HYDROGRAPH THEORY")
print("=" * 70)

uh_text = """
UNIT HYDROGRAPH (Sherman, 1932):
================================

The response of a watershed to 1 unit of excess rainfall
in 1 unit of time.

ASSUMPTIONS:
1. Linear system (superposition valid)
2. Time-invariant
3. Rainfall uniform over basin

CONVOLUTION:

Q(t) = Σ P_i × U(t - i)

Where:
- Q(t) = discharge at time t
- P_i = excess rainfall in interval i
- U = unit hydrograph ordinates

PROPERTIES:

1. Peak discharge: q_p (m³/s per mm)
2. Time to peak: t_p (hours)
3. Base time: t_b (hours)

SNYDER'S EQUATIONS:

t_p = C_t × (L × L_ca)^0.3

q_p = C_p × A / t_p

Where:
- L = main channel length
- L_ca = distance to centroid
- A = drainage area
- C_t, C_p = regional coefficients

SCS (NRCS) DIMENSIONLESS UH:

t_p = 0.6 × t_c  (time of concentration)
t_b = 2.67 × t_p (base time)
q_p = 2.08 × A / t_p  (peak in m³/s)

Time of concentration:
t_c = L^0.8 × (S+1)^0.7 / (1140 × Y^0.5)

Where S = (1000/CN) - 10
"""
print(uh_text)

def scs_time_to_peak(tc_hours):
    """Time to peak for SCS unit hydrograph."""
    return 0.6 * tc_hours

def scs_peak_discharge(area_km2, tp_hours):
    """Peak discharge for SCS unit hydrograph (m³/s per mm)."""
    return 2.08 * area_km2 / tp_hours

def time_of_concentration(length_km, slope, cn=80):
    """
    Estimate time of concentration (hours).

    Simplified SCS method.
    """
    S = (1000 / cn) - 10
    L = length_km * 1000 * 3.28  # Convert to feet
    Y = slope * 100  # Percent
    tc = (L**0.8 * (S + 1)**0.7) / (1140 * Y**0.5)
    return tc / 60  # Convert to hours

print("\nUnit Hydrograph Parameters:")
print("-" * 65)
print(f"{'Area (km²)':<15} {'Length (km)':<15} {'tc (hr)':<12} {'tp (hr)':<12} {'qp (m³/s/mm)'}")
print("-" * 65)

for area in [10, 50, 100, 500]:
    # Assume length ~ sqrt(area) and slope ~ 0.01
    length = np.sqrt(area) * 1.5
    tc = time_of_concentration(length, 0.01)
    tp = scs_time_to_peak(tc)
    qp = scs_peak_discharge(area, tp)
    print(f"{area:<15} {length:<15.1f} {tc:<12.1f} {tp:<12.1f} {qp:.1f}")


# =============================================================================
# PART 4: FLOOD ROUTING
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: FLOOD ROUTING")
print("=" * 70)

routing_text = """
FLOOD ROUTING:
==============

How flood waves propagate down a river

CONTINUITY EQUATION:

∂A/∂t + ∂Q/∂x = q_L

Where:
- A = cross-sectional area
- Q = discharge
- q_L = lateral inflow per unit length

MOMENTUM EQUATION (Saint-Venant):

∂Q/∂t + ∂(Q²/A)/∂x + gA(∂h/∂x) = gA(S_0 - S_f)

Where:
- S_0 = bed slope
- S_f = friction slope

MANNING'S EQUATION:

Q = (1/n) × A × R^(2/3) × S^(1/2)

Where:
- n = Manning's roughness
- R = hydraulic radius = A/P
- P = wetted perimeter

TYPICAL MANNING'S n:
Clean channel: 0.025-0.035
Vegetation: 0.050-0.080
Floodplain: 0.080-0.150

MUSKINGUM ROUTING:

S = K[xI + (1-x)O]

dS/dt = I - O

O₂ = C₀I₂ + C₁I₁ + C₂O₁

Where:
- K = travel time
- x = weighting factor (0-0.5)
- C₀, C₁, C₂ = routing coefficients

WAVE CELERITY:

c = dQ/dA  (kinematic wave speed)

For Manning's: c = (5/3) × V (velocity)

Flood waves travel faster than water!
"""
print(routing_text)

def manning_discharge(area, wetted_perimeter, slope, n=0.035):
    """
    Manning's equation for discharge.
    """
    R = area / wetted_perimeter  # Hydraulic radius
    Q = (1/n) * area * R**(2/3) * slope**0.5
    return Q

def wave_celerity(velocity):
    """
    Kinematic wave celerity.

    c = (5/3) × V for Manning's equation
    """
    return (5/3) * velocity

def muskingum_routing(I1, I2, O1, K, x, dt):
    """
    Muskingum routing for one time step.
    """
    C0 = (dt - 2*K*x) / (2*K*(1-x) + dt)
    C1 = (dt + 2*K*x) / (2*K*(1-x) + dt)
    C2 = (2*K*(1-x) - dt) / (2*K*(1-x) + dt)

    O2 = C0*I2 + C1*I1 + C2*O1
    return O2

print("\nManning's Equation - Channel Discharge:")
print("-" * 65)
print(f"{'Width (m)':<12} {'Depth (m)':<12} {'Slope':<12} {'n':<10} {'Q (m³/s)'}")
print("-" * 65)

for width in [10, 20, 50]:
    for depth in [2, 3, 5]:
        A = width * depth
        P = width + 2 * depth
        Q = manning_discharge(A, P, 0.001)
        print(f"{width:<12} {depth:<12} {0.001:<12} {0.035:<10} {Q:.0f}")


# =============================================================================
# PART 5: FLOOD FREQUENCY ANALYSIS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: FLOOD FREQUENCY ANALYSIS")
print("=" * 70)

frequency_text = """
FLOOD FREQUENCY:
================

Statistical analysis of flood magnitudes and return periods

RETURN PERIOD:

T = 1 / P(X ≥ x)

100-year flood: P = 0.01 (1% annual chance)
NOT "happens every 100 years"!

P(at least one in n years) = 1 - (1 - 1/T)^n

30-year mortgage, 100-year flood:
P = 1 - (1 - 0.01)^30 = 26%!

EXTREME VALUE DISTRIBUTIONS:

1. GUMBEL (Type I):
   F(x) = exp[-exp(-(x-μ)/β)]

   Used for precipitation, temperature extremes

2. LOG-PEARSON TYPE III:
   Standard for flood frequency (US)
   Log-transform, then fit Pearson III

3. GENERALIZED EXTREME VALUE (GEV):
   F(x) = exp[-(1 + ξ(x-μ)/σ)^(-1/ξ)]

   Unifies all three extreme value types

CLIMATE CHANGE IMPACT:

Non-stationarity!
- Historical record may not predict future
- "100-year flood" may become more common
- Clausius-Clapeyron: 7% more moisture per °C
- More intense precipitation events

DESIGN FLOODS:

Use                    Return period
──────────────────────────────────────
Farm drainage          5-10 years
Urban drainage         10-25 years
Small dam spillway     100 years
Large dam spillway     PMF (10,000+ years)
Nuclear plant          PMF
"""
print(frequency_text)

def return_period_probability(years_exposed, return_period):
    """
    Probability of experiencing flood at least once.

    P = 1 - (1 - 1/T)^n
    """
    p_annual = 1 / return_period
    p_none = (1 - p_annual) ** years_exposed
    return 1 - p_none

def gumbel_quantile(return_period, mu, beta):
    """
    Gumbel distribution quantile.

    x = μ - β × ln(-ln(1 - 1/T))
    """
    F = 1 - 1/return_period
    x = mu - beta * np.log(-np.log(F))
    return x

print("\nFlood Probability Over Time:")
print("-" * 60)
print(f"{'Return period':<18} {'10 years':<15} {'30 years':<15} {'50 years'}")
print("-" * 60)

for T in [10, 50, 100, 500]:
    p10 = return_period_probability(10, T) * 100
    p30 = return_period_probability(30, T) * 100
    p50 = return_period_probability(50, T) * 100
    print(f"{T}-year flood{'':<5} {p10:<15.0f}% {p30:<15.0f}% {p50:.0f}%")

print("\n\nGumbel Flood Quantiles:")
print("(Example: μ=100 m³/s, β=30)")
print("-" * 45)
print(f"{'Return period':<18} {'Flood magnitude (m³/s)'}")
print("-" * 45)

mu, beta = 100, 30  # Example parameters
for T in [2, 5, 10, 25, 50, 100, 500]:
    Q = gumbel_quantile(T, mu, beta)
    print(f"{T:<18} {Q:.0f}")


# =============================================================================
# PART 6: FLASH FLOODS
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: FLASH FLOOD PHYSICS")
print("=" * 70)

flash_text = """
FLASH FLOODS:
=============

Rapid-onset floods from intense rainfall

CHARACTERISTICS:
- Rise in < 6 hours (often < 1 hour)
- High velocities
- Little warning time
- Leading cause of weather deaths (US)

FACTORS:

1. RAINFALL INTENSITY
   - Exceeds infiltration capacity
   - Flash floods from I > 25-50 mm/hr

2. RAINFALL DURATION
   - Accumulation matters
   - Relationship with tc (time of concentration)

3. SOIL STATE
   - Saturated soil → no infiltration
   - Previous rainfall matters

4. TOPOGRAPHY
   - Steep slopes → fast runoff
   - Valley constrictions → amplify depth

5. URBANIZATION
   - Impervious surfaces
   - Increases peak by 2-5×
   - Reduces time to peak

FLASH FLOOD GUIDANCE (FFG):

Amount of rainfall needed to cause flooding
FFG = FFG_soil + FFG_channel

UNIT STREAM POWER:

ω = ρ g Q S / w

Where:
- Q = discharge
- S = slope
- w = width

ω > 500 W/m² → Significant erosion
ω > 2000 W/m² → Catastrophic damage

TRAINING ECHOES:

Multiple storms over same location
→ Extreme totals
→ Devastating flash floods
"""
print(flash_text)

def flash_flood_potential(rainfall_rate_mmhr, soil_saturation, slope, area_km2):
    """
    Simple flash flood potential index.

    Higher = more dangerous
    """
    # Excess rainfall
    if soil_saturation > 0.8:
        infil = 5  # mm/hr when saturated
    else:
        infil = 20 * (1 - soil_saturation)

    excess = max(0, rainfall_rate_mmhr - infil)

    # Response time (smaller = faster)
    tc = np.sqrt(area_km2) * 2  # hours, rough

    # Potential index
    potential = excess * slope * 100 / tc

    return potential, excess, tc

def unit_stream_power(discharge, slope, width):
    """
    Calculate unit stream power (W/m²).
    """
    return rho_water * g * discharge * slope / width

print("\nFlash Flood Potential Index:")
print("-" * 70)
print(f"{'Rain (mm/hr)':<15} {'Saturation':<15} {'Slope':<12} {'Area (km²)':<12} {'Index'}")
print("-" * 70)

for rain in [25, 50, 75, 100]:
    for sat in [0.5, 0.9]:
        pot, _, _ = flash_flood_potential(rain, sat, 0.05, 25)
        if sat == 0.9:
            print(f"{rain:<15} {sat:<15} {0.05:<12} {25:<12} {pot:.1f}")

print("\n\nUnit Stream Power Examples:")
print("-" * 55)
print(f"{'Q (m³/s)':<15} {'Slope':<12} {'Width (m)':<12} {'Power (W/m²)'}")
print("-" * 55)

for Q in [100, 500, 1000, 5000]:
    for slope in [0.01, 0.05]:
        w = Q**0.4 * 3  # Rough width estimate
        power = unit_stream_power(Q, slope, w)
        if slope == 0.02:
            power = unit_stream_power(Q, 0.02, w)
            print(f"{Q:<15} {0.02:<12} {w:<12.0f} {power:.0f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: HYDROLOGY AND FLOOD PHYSICS")
print("=" * 70)

summary = """
KEY HYDROLOGY PHYSICS:
=====================

1. WATER BUDGET
   - P = ET + R + ΔS
   - Conservation of mass
   - Residence times: 10 days (atm) to 1000s years (ocean)

2. RAINFALL-RUNOFF
   - Infiltration: Horton's equation
   - Runoff coefficient: 0.1 (forest) to 0.95 (urban)
   - Saturation excess vs infiltration excess

3. UNIT HYDROGRAPH
   - Linear system response
   - Convolution: Q = Σ P × U
   - SCS method: tp, qp, tc relationships

4. FLOOD ROUTING
   - Saint-Venant equations
   - Manning's equation: Q = (1/n)AR^(2/3)S^(1/2)
   - Muskingum for channel routing
   - Wave celerity: c = (5/3)V

5. FLOOD FREQUENCY
   - Return period: T = 1/P
   - 100-year flood has 26% chance in 30 years!
   - Gumbel, Log-Pearson III distributions
   - Climate change: non-stationarity

6. FLASH FLOODS
   - < 6 hour rise time
   - Intense rainfall + steep terrain
   - Unit stream power: ω = ρgQS/w
   - Leading weather killer


THE PHYSICS TELLS US:
====================
- Water follows gravity and mass conservation
- Urbanization dramatically increases flood risk
- "100-year flood" doesn't mean once per century!
- Climate change = more intense precipitation = more floods
- Flash floods require intense local rainfall
- Understanding physics essential for flood management
"""
print(summary)

print("\n" + "=" * 70)
print("END OF HYDROLOGY AND FLOOD PHYSICS")
print("=" * 70)
