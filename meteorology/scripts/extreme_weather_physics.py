#!/usr/bin/env python3
"""
EXTREME WEATHER PHYSICS - FIRST PRINCIPLES
==========================================

Deriving how extreme precipitation, heat waves, and storms
change with climate warming using fundamental physics.
"""

import numpy as np

print("=" * 70)
print("EXTREME WEATHER PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL THERMODYNAMIC CONSTANTS
# =============================================================================
R_v = 461.5     # Gas constant for water vapor (J/kg/K)
R_d = 287.0     # Gas constant for dry air (J/kg/K)
L_v = 2.5e6     # Latent heat of vaporization (J/kg)
c_p = 1004      # Specific heat of air (J/kg/K)
g = 9.81        # Gravity (m/s²)


# =============================================================================
# PART 1: CLAUSIUS-CLAPEYRON - THE MASTER EQUATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: CLAUSIUS-CLAPEYRON - THE MASTER EQUATION")
print("=" * 70)

cc_text = """
THE CLAUSIUS-CLAPEYRON EQUATION:
================================

This is THE key equation for understanding extreme precipitation.

d(ln e_s)/dT = L_v / (R_v T²)

Where:
- e_s = saturation vapor pressure
- L_v = latent heat of vaporization (2.5×10⁶ J/kg)
- R_v = gas constant for water vapor (461.5 J/kg/K)
- T = temperature (K)

Integrating gives:
e_s(T) = e_s0 × exp[L_v/R_v × (1/T₀ - 1/T)]

At typical temperatures, this yields:
→ 7% increase in e_s per 1°C warming

This is FUNDAMENTAL PHYSICS, not a model assumption!
"""
print(cc_text)

def saturation_vapor_pressure(T_celsius):
    """Calculate saturation vapor pressure using Clausius-Clapeyron."""
    T = T_celsius + 273.15
    T0 = 273.15
    e_s0 = 611.2  # Pa at 0°C

    e_s = e_s0 * np.exp((L_v / R_v) * (1/T0 - 1/T))
    return e_s

def cc_scaling(dT):
    """Calculate fractional increase in e_s for given warming."""
    T_base = 288  # K (~15°C)
    factor = np.exp((L_v / R_v) * dT / (T_base * (T_base + dT)))
    return (factor - 1) * 100  # Percent increase

print("\nClausius-Clapeyron Scaling:")
print("-" * 50)
print(f"{'Warming (°C)':<15} {'Vapor increase (%)':<20}")
print("-" * 50)
for dT in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]:
    increase = cc_scaling(dT)
    print(f"{dT:<15.1f} {increase:<20.1f}")


# =============================================================================
# PART 2: EXTREME PRECIPITATION SCALING
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: EXTREME PRECIPITATION PHYSICS")
print("=" * 70)

precip_text = """
EXTREME PRECIPITATION AND CLAUSIUS-CLAPEYRON:
==============================================

For extreme precipitation (short, intense):
- Atmosphere near saturation
- Precipitation ≈ moisture convergence
- Moisture limited by Clausius-Clapeyron

Theoretical expectation:
→ Extreme precipitation increases ~7%/°C

OBSERVATIONS MATCH THIS!
- Observed: 6-8% increase per °C globally
- Some regions exceed 7% ("super-CC scaling")
- Due to enhanced dynamics/convergence in warmer climate

WHY EXTREMES SCALE WITH CC:
1. More moisture available to precipitate
2. Convection draws moisture from larger area
3. Latent heat release intensifies updrafts
4. More intense storms = more extreme precipitation


SUPER-CC SCALING (>7%/°C):
When storms become more intense, they can:
1. Draw moisture from larger areas
2. Have stronger updrafts
3. Achieve higher precipitation efficiency

Result: Some extreme events increase 10-14% per °C!
"""
print(precip_text)

def precipitation_rate(moisture_flux, efficiency=0.5):
    """
    Estimate precipitation rate from moisture flux.

    moisture_flux: kg/m²/s of water vapor convergence
    efficiency: fraction that actually precipitates
    """
    return moisture_flux * efficiency * 3600  # mm/hr

def extreme_precip_scaling(dT, cc_factor=7, super_cc_factor=1.0):
    """
    Calculate change in extreme precipitation with warming.

    dT: warming in °C
    cc_factor: Clausius-Clapeyron rate (%/°C)
    super_cc_factor: multiplier for dynamic enhancement (1.0-2.0)
    """
    return (1 + cc_factor * super_cc_factor / 100) ** dT

print("\nExtreme Precipitation Scaling with Warming:")
print("-" * 70)
print(f"{'Warming':<10} {'CC scaling':<15} {'Super-CC (1.5x)':<20} {'Super-CC (2x)':<15}")
print("-" * 70)
for dT in [1.0, 1.5, 2.0, 3.0, 4.0]:
    cc = extreme_precip_scaling(dT, 7, 1.0)
    super_1 = extreme_precip_scaling(dT, 7, 1.5)
    super_2 = extreme_precip_scaling(dT, 7, 2.0)
    print(f"{dT:<10.1f}°C {cc:<15.2f}× {super_1:<20.2f}× {super_2:<15.2f}×")


# =============================================================================
# PART 3: HEAT WAVE PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: HEAT WAVE PHYSICS")
print("=" * 70)

heatwave_text = """
HEAT WAVES AND PROBABILITY DISTRIBUTIONS:
=========================================

Key concept: Extreme heat is on the TAIL of a distribution.

If daily temperatures are normally distributed:
P(T > T_threshold) depends on mean AND variance

With warming:
1. Mean shifts higher → more hot days
2. BUT: Variance might also change

SHIFT IN DISTRIBUTION:
If we shift a normal distribution by Δ (warming):
- Days that used to be "1 in 100" become more common
- A 1-in-100 event might become 1-in-10

Example calculation:
- Standard deviation of summer max T ≈ 3-5°C
- 2°C warming shifts mean
- Events 2σ above old mean are now only 1.3σ above new mean
- Probability jumps from 2.3% to 9.7%!


SOIL MOISTURE FEEDBACK:
Hot → dry soil → less evaporative cooling → HOTTER
This amplifies heat waves through positive feedback.

WET BULB TEMPERATURE (human survival limit):
T_w = T × arctan(0.151977(RH + 8.313659)^0.5) + ...
Human body cannot cool if T_w > 35°C
This is a HARD LIMIT from physics
"""
print(heatwave_text)

def probability_ratio(dT, sigma=3.0, threshold_sigma=2.0):
    """
    Calculate how probability of exceeding threshold changes.

    dT: mean warming (°C)
    sigma: standard deviation of temperature distribution (°C)
    threshold_sigma: threshold in units of sigma above current mean
    """
    from scipy import stats
    # Probability of exceeding threshold before warming
    p_before = 1 - stats.norm.cdf(threshold_sigma)

    # New position of threshold relative to new mean
    new_sigma = (threshold_sigma * sigma - dT) / sigma

    # Probability after warming
    p_after = 1 - stats.norm.cdf(new_sigma)

    return p_after / p_before if p_before > 0 else float('inf')

try:
    from scipy import stats
    print("\nHeat Wave Probability Changes:")
    print("-" * 70)
    print(f"{'Event type':<25} {'Warming':<10} {'Prob ratio':<15} {'New frequency'}")
    print("-" * 70)

    for threshold_name, threshold_sigma in [("1-in-10 year", 1.28),
                                            ("1-in-50 year", 2.05),
                                            ("1-in-100 year", 2.33)]:
        for dT in [1.0, 2.0, 3.0]:
            ratio = probability_ratio(dT, sigma=3.0, threshold_sigma=threshold_sigma)
            if threshold_name == "1-in-10 year":
                new_freq = f"1-in-{10/ratio:.1f} year"
            elif threshold_name == "1-in-50 year":
                new_freq = f"1-in-{50/ratio:.1f} year"
            else:
                new_freq = f"1-in-{100/ratio:.1f} year"
            print(f"{threshold_name:<25} {dT:<10.1f}°C {ratio:<15.1f}× {new_freq}")
except ImportError:
    print("\n(scipy not available for detailed probability calculations)")


# Wet bulb temperature
def wet_bulb_temperature(T_celsius, RH_percent):
    """
    Approximate wet bulb temperature.
    Stull (2011) formula.
    """
    T = T_celsius
    RH = RH_percent

    T_w = T * np.arctan(0.151977 * (RH + 8.313659)**0.5)
    T_w += np.arctan(T + RH) - np.arctan(RH - 1.676331)
    T_w += 0.00391838 * RH**1.5 * np.arctan(0.023101 * RH)
    T_w -= 4.686035

    return T_w

print("\n\nWet Bulb Temperature (Human Survival Limit):")
print("-" * 60)
print("T_w > 35°C = physiological limit (body cannot cool)")
print()
print(f"{'T (°C)':<10} {'RH (%)':<10} {'T_wet (°C)':<15} {'Status':<25}")
print("-" * 60)

scenarios = [
    (35, 80),   # Hot and humid
    (40, 50),   # Very hot, moderate humidity
    (45, 50),   # Extreme heat
    (50, 30),   # Desert extreme
    (35, 100),  # Saturated at 35°C
    (40, 75),   # Dangerous conditions
]

for T, RH in scenarios:
    T_w = wet_bulb_temperature(T, RH)
    status = "DANGEROUS" if T_w > 32 else ("SURVIVABLE" if T_w < 28 else "CAUTION")
    if T_w > 35:
        status = "LETHAL (cannot cool)"
    print(f"{T:<10.0f} {RH:<10.0f} {T_w:<15.1f} {status:<25}")


# =============================================================================
# PART 4: TROPICAL CYCLONE INTENSITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: TROPICAL CYCLONE POTENTIAL INTENSITY")
print("=" * 70)

tc_text = """
MAXIMUM POTENTIAL INTENSITY (MPI):
==================================

From Emanuel (1986), a thermodynamic upper bound:

V_max² = (C_k/C_D) × (T_s - T_o)/T_o × (k_s* - k)

Where:
- C_k = enthalpy exchange coefficient
- C_D = drag coefficient
- T_s = sea surface temperature
- T_o = outflow temperature (tropopause)
- k_s* = saturation enthalpy at SST
- k = ambient air enthalpy

SIMPLIFIED SCALING:
V_max ∝ √(SST - 26.5°C)  [approximately]

Or equivalently:
dV_max/dSST ≈ 3-5 m/s per °C of SST increase

OUR Z² = 32π/3 FORMULA:
This derived the storm structure.
Intensity depends on available energy (Carnot efficiency).
"""
print(tc_text)

def potential_intensity(SST_celsius, T_tropopause=200):
    """
    Simplified potential intensity calculation.

    Based on Carnot efficiency and thermodynamic bounds.
    """
    T_s = SST_celsius + 273.15
    T_o = T_tropopause  # Outflow temperature (K)

    # Carnot efficiency
    eta = (T_s - T_o) / T_s

    # Enthalpy difference (simplified)
    e_s = saturation_vapor_pressure(SST_celsius)
    e_a = saturation_vapor_pressure(SST_celsius - 2)  # Assume slight undersaturation
    delta_k = 0.622 * L_v * (e_s - e_a) / (1e5)  # Approximate enthalpy diff

    # Simplified V_max
    Ck_Cd = 1.0  # Ratio ≈ 1
    V_max_squared = Ck_Cd * eta * delta_k * 1000
    V_max = np.sqrt(max(0, V_max_squared))

    return V_max

print("\nPotential Intensity vs SST:")
print("-" * 50)
print(f"{'SST (°C)':<15} {'V_max (m/s)':<15} {'Category'}")
print("-" * 50)

for SST in range(26, 34):
    V = potential_intensity(SST)
    if V < 33:
        cat = "TS/Cat-1"
    elif V < 50:
        cat = "Cat-2/3"
    elif V < 70:
        cat = "Cat-4"
    else:
        cat = "Cat-5"
    print(f"{SST:<15.0f} {V:<15.1f} {cat}")


# =============================================================================
# PART 5: DROUGHT PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: DROUGHT AND ARIDITY PHYSICS")
print("=" * 70)

drought_text = """
DROUGHT: SUPPLY vs DEMAND IMBALANCE
====================================

Aridity Index = Precipitation / Potential Evapotranspiration

Potential Evapotranspiration (PET) increases with warming:
- More energy available
- Higher saturation vapor pressure
- Faster drying rate

SIMPLIFIED PET (Thornthwaite):
PET = 16 × (10T/I)^a × (days/12) × (hours/12)

Where I = heat index, a = function of I

More physics-based (Penman-Monteith):
PET depends on:
- Net radiation
- Vapor pressure deficit
- Wind speed
- Surface resistance

KEY INSIGHT:
Even with CONSTANT precipitation, aridity INCREASES with warming
because PET increases faster than precipitation.

This is why:
- Mediterranean regions drying
- Expansion of subtropical dry zones
- Flash droughts becoming more common
"""
print(drought_text)

def pet_thornthwaite(T_monthly_avg, day_length_hours=12):
    """
    Simplified Thornthwaite PET calculation.
    Returns mm/month.
    """
    if T_monthly_avg <= 0:
        return 0

    # Heat index (simplified annual average)
    I = 12 * (T_monthly_avg / 5) ** 1.514

    # Exponent
    a = 6.75e-7 * I**3 - 7.71e-5 * I**2 + 1.792e-2 * I + 0.49239

    # PET in mm/month
    pet = 16 * (10 * T_monthly_avg / I) ** a * day_length_hours / 12

    return pet * 30  # Convert to monthly

def vapor_pressure_deficit(T_celsius, RH_percent):
    """Calculate vapor pressure deficit."""
    e_s = saturation_vapor_pressure(T_celsius)
    e_a = e_s * RH_percent / 100
    vpd = e_s - e_a
    return vpd / 1000  # kPa

print("\nVapor Pressure Deficit (VPD) - Evaporative Demand:")
print("-" * 60)
print(f"{'T (°C)':<10} {'RH (%)':<10} {'VPD (kPa)':<15} {'Stress level'}")
print("-" * 60)

for T in [20, 25, 30, 35, 40]:
    for RH in [60, 40, 20]:
        vpd = vapor_pressure_deficit(T, RH)
        if vpd < 1.5:
            stress = "Low"
        elif vpd < 3.0:
            stress = "Moderate"
        elif vpd < 4.5:
            stress = "High"
        else:
            stress = "Extreme"
        print(f"{T:<10.0f} {RH:<10.0f} {vpd:<15.2f} {stress}")


# =============================================================================
# PART 6: FLOOD PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: FLOOD HYDROLOGY")
print("=" * 70)

flood_text = """
RAINFALL-RUNOFF RELATIONSHIP:
=============================

Peak discharge from extreme rainfall:

Q_peak = C × i × A

Where:
- C = runoff coefficient (0-1)
- i = rainfall intensity (mm/hr)
- A = catchment area (km²)

With climate change:
1. i increases (Clausius-Clapeyron)
2. C might increase (saturated soils, urbanization)
3. Result: Q_peak increases faster than rainfall

RETURN PERIOD SHIFT:
If 100-year rainfall becomes 50-year rainfall:
- The old 100-year flood becomes more frequent
- The new 100-year flood is MORE INTENSE

This is the "new normal" problem.
"""
print(flood_text)

def rational_method_discharge(intensity_mm_hr, area_km2, runoff_coeff=0.5):
    """
    Rational method for peak discharge.
    Q = C × i × A
    """
    # Convert units: mm/hr × km² → m³/s
    Q = runoff_coeff * intensity_mm_hr * area_km2 * 1e6 / (3600 * 1e3)
    return Q

print("\nPeak Discharge vs Rainfall Intensity:")
print("-" * 70)
print(f"{'Intensity (mm/hr)':<20} {'Area (km²)':<15} {'Q_peak (m³/s)':<15}")
print("-" * 70)

for intensity in [25, 50, 75, 100, 150]:
    for area in [10, 50, 100]:
        Q = rational_method_discharge(intensity, area, 0.5)
        print(f"{intensity:<20.0f} {area:<15.0f} {Q:<15.1f}")

# Climate-scaled flood increase
print("\n\nFlood Magnitude Change with Warming:")
print("-" * 50)
for dT in [1.0, 2.0, 3.0]:
    precip_factor = extreme_precip_scaling(dT, 7, 1.5)  # Super-CC
    # Runoff increases even more (nonlinear response)
    runoff_factor = precip_factor ** 1.2
    print(f"{dT:.1f}°C warming: rainfall {precip_factor:.2f}×, runoff ~{runoff_factor:.2f}×")


# =============================================================================
# PART 7: COMPOUND EVENTS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: COMPOUND EXTREME EVENTS")
print("=" * 70)

compound_text = """
COMPOUND EVENTS: WHEN EXTREMES COMBINE
======================================

Climate change increases COMPOUND events:

1. HEAT + DROUGHT
   - Higher temperatures → more evaporation
   - Drought → less evaporative cooling
   - Positive feedback → amplification

2. STORM SURGE + RAIN FLOODING
   - Hurricane brings both
   - Sea level rise worsens surge
   - Heavier rain worsens flooding
   - Combined effect is multiplicative

3. WILDFIRE WEATHER
   - Hot + Dry + Windy
   - All three becoming more common
   - Joint probability increasing

DEPENDENCE STRUCTURE:
If events are independent: P(A and B) = P(A) × P(B)
If events are correlated:  P(A and B) > P(A) × P(B)

Climate change may INCREASE correlation between extremes!
Example: Heat waves cause drought, both increase fire risk

TAIL DEPENDENCE:
Extremes may be MORE correlated than moderate events.
This means compound extremes increase faster than
individual extremes.
"""
print(compound_text)


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: EXTREME WEATHER PHYSICS")
print("=" * 70)

summary = """
FIRST-PRINCIPLES CONSTRAINTS ON EXTREMES:
=========================================

1. CLAUSIUS-CLAPEYRON
   - 7% more moisture per 1°C warming
   - Extreme precipitation scales similarly
   - Some events exceed this ("super-CC")

2. HEAT WAVES
   - Tail of distribution shifts more than mean
   - Small warming → big increase in rare events
   - Wet bulb T=35°C is hard human survival limit

3. TROPICAL CYCLONES
   - Intensity limited by thermodynamics
   - SST increase → higher potential intensity
   - ~5% intensity increase per °C

4. DROUGHT
   - Evaporative demand increases with T
   - Even constant precip → more arid
   - VPD increase stresses vegetation

5. FLOODS
   - More intense rainfall → more runoff
   - Runoff increases faster than rainfall
   - Return periods shrinking

6. COMPOUND EVENTS
   - Multiple hazards co-occurring
   - May increase faster than individual extremes
   - Especially concerning for adaptation


THE PHYSICS IS CLEAR:
=====================
Warming increases most weather extremes.
The mechanisms are understood.
The quantitative scaling comes from:
- Clausius-Clapeyron (moisture)
- Probability distributions (rare events)
- Thermodynamics (energy available)
- Hydrology (runoff response)

This is not speculation - it's physics.
"""
print(summary)

print("\n" + "=" * 70)
print("END OF EXTREME WEATHER PHYSICS")
print("=" * 70)
