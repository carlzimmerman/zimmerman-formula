#!/usr/bin/env python3
"""
FIRE WEATHER PHYSICS - FIRST PRINCIPLES
========================================

Deriving the physics of wildfire behavior, fire weather indices,
fire spread, and atmosphere-fire coupling.
"""

import numpy as np

print("=" * 70)
print("FIRE WEATHER PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
c_p = 1004         # Specific heat of air (J/kg/K)
rho_air = 1.2      # Air density (kg/m³)
sigma = 5.67e-8    # Stefan-Boltzmann constant


# =============================================================================
# PART 1: FIRE TRIANGLE AND BEHAVIOR
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: FIRE BEHAVIOR FUNDAMENTALS")
print("=" * 70)

fire_text = """
THE FIRE TRIANGLE:
==================

Fire requires three elements:

1. FUEL
   - Dead vegetation (fine fuels < 3 inches)
   - Live vegetation
   - Fuel loading (tons/acre or kg/m²)
   - Fuel moisture content

2. HEAT
   - Ignition source
   - Preheating of adjacent fuels
   - Solar radiation

3. OXYGEN
   - Atmosphere provides
   - Wind supplies fresh O₂
   - Minimum ~16% O₂ required

FIRE SPREAD MECHANISMS:

1. RADIATION
   - Q = σεT⁴
   - Dominant at flame front
   - Preheats fuels ahead of fire

2. CONVECTION
   - Hot air rises, fresh air drawn in
   - Creates fire whirls
   - Spot fires from lofted embers

3. CONDUCTION
   - Through soil, tree trunks
   - Generally minor for surface fires

FIRE INTENSITY:

Byram's Fire Intensity (fireline intensity):

I = H × w × R

Where:
- I = intensity (kW/m)
- H = heat of combustion (~18,000 kJ/kg)
- w = fuel consumed (kg/m²)
- R = rate of spread (m/s)

Low: I < 350 kW/m
Moderate: I = 350-1700 kW/m
High: I = 1700-3500 kW/m
Extreme: I > 3500 kW/m
"""
print(fire_text)

def byram_intensity(fuel_consumed_kg_m2, rate_of_spread_m_min, H=18000):
    """
    Calculate Byram's fireline intensity.

    I = H × w × R (kW/m)
    """
    R_m_s = rate_of_spread_m_min / 60
    I = H * fuel_consumed_kg_m2 * R_m_s
    return I

def flame_length(intensity_kW_m):
    """
    Estimate flame length from Byram's intensity.

    L = 0.0775 × I^0.46 (meters)
    """
    return 0.0775 * intensity_kW_m**0.46

print("\nFire Intensity and Flame Length:")
print("-" * 65)
print(f"{'Fuel (kg/m²)':<15} {'Spread (m/min)':<18} {'Intensity (kW/m)':<20} {'Flame (m)'}")
print("-" * 65)

for fuel in [0.5, 1.0, 2.0, 4.0]:
    for ros in [1, 5, 20, 50]:
        I = byram_intensity(fuel, ros)
        L = flame_length(I)
        if fuel == 1.0:
            print(f"{fuel:<15} {ros:<18} {I:<20.0f} {L:.1f}")


# =============================================================================
# PART 2: FUEL MOISTURE
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: FUEL MOISTURE PHYSICS")
print("=" * 70)

moisture_text = """
FUEL MOISTURE CONTENT:
======================

M = (W_wet - W_dry) / W_dry × 100%

CRITICAL THRESHOLDS:

Dead fuel moisture:
- < 3%: Extreme fire behavior
- 3-5%: Very high
- 5-8%: High
- 8-12%: Moderate
- > 15%: Low fire danger

Live fuel moisture:
- < 80%: Critical (cured)
- 80-120%: High fire potential
- > 120%: Green, reduced flammability

EQUILIBRIUM MOISTURE CONTENT (EMC):

Dead fuels equilibrate with atmosphere
EMC depends on T and RH

Nelson model (simplified):
EMC = 0.942 × RH^0.679 + 0.0005 × (21.1 - T)

FUEL MOISTURE RESPONSE TIME:

1-hour fuels (< 0.25"): ~ 1 hour
10-hour fuels (0.25-1"): ~ 10 hours
100-hour fuels (1-3"): ~ 100 hours
1000-hour fuels (3-8"): ~ 1000 hours

Response = 1 - exp(-t/τ)

DIURNAL CYCLE:

Day: T up, RH down → fuel dries
Night: T down, RH up → fuel gains moisture
Recovery depends on fuel size class
"""
print(moisture_text)

def equilibrium_moisture_content(RH_percent, T_celsius):
    """
    Calculate equilibrium moisture content.

    Simplified Nelson model.
    """
    emc = 0.942 * (RH_percent)**0.679 + 0.0005 * (21.1 - T_celsius)
    return max(2, min(30, emc))

def fuel_moisture_response(initial_M, target_M, time_hours, timelag_hours):
    """
    Fuel moisture approaching equilibrium.

    M(t) = M_target + (M_initial - M_target) × exp(-t/τ)
    """
    return target_M + (initial_M - target_M) * np.exp(-time_hours / timelag_hours)

print("\nEquilibrium Moisture Content:")
print("-" * 55)
print(f"{'Temperature (°C)':<20} {'RH (%)':<12} {'EMC (%)':<12} {'Fire risk'}")
print("-" * 55)

for T in [15, 25, 35, 40]:
    for RH in [20, 40, 60, 80]:
        emc = equilibrium_moisture_content(RH, T)
        if emc < 5:
            risk = "Extreme"
        elif emc < 8:
            risk = "Very high"
        elif emc < 12:
            risk = "High"
        else:
            risk = "Moderate"
        if RH == 40:
            print(f"{T:<20} {RH:<12} {emc:<12.1f} {risk}")

print("\n\n1-hr Fuel Moisture Response:")
print("Initial: 8%, Target EMC: 4%")
print("-" * 40)
for t in [0, 0.5, 1, 2, 4, 8]:
    M = fuel_moisture_response(8, 4, t, 1)
    print(f"Time = {t} hr: M = {M:.1f}%")


# =============================================================================
# PART 3: WIND AND FIRE SPREAD
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: WIND-DRIVEN FIRE SPREAD")
print("=" * 70)

wind_text = """
WIND EFFECTS ON FIRE:
=====================

Wind is the PRIMARY driver of fire spread!

EFFECTS:

1. SUPPLIES OXYGEN
   - Fresh air to combustion zone
   - Increases fire intensity

2. TILTS FLAMES
   - Preheating of downwind fuels
   - Radiation heating more effective

3. CARRIES EMBERS
   - Spotting ahead of fire
   - Long-distance fire transport

ROTHERMEL SPREAD MODEL:

R = I_R × ξ × (1 + Φ_w + Φ_s) / (ρ_b × ε × Q_ig)

Where:
- I_R = reaction intensity
- ξ = propagating flux ratio
- Φ_w = wind coefficient
- Φ_s = slope coefficient
- ρ_b = bulk density
- Q_ig = heat of preignition

SIMPLIFIED WIND FACTOR:

R_wind / R_0 = 1 + c × U^b

Where:
- U = midflame wind speed
- b ≈ 1.5-2.0
- c depends on fuel type

MIDFLAME WIND:

Fire behavior uses wind at flame height!
Midflame wind ≈ 0.3-0.5 × 20-ft wind (open)
Midflame wind ≈ 0.1-0.2 × 20-ft wind (forest)

EXTREME WIND EVENTS:

- Foehn/Chinook: Downslope, dry, warm
- Santa Ana: Offshore, dry, 40-100 mph
- Sundowner: Evening wind surge
"""
print(wind_text)

def wind_factor(midflame_wind_mph, fuel_bed_depth_ft=1):
    """
    Calculate wind multiplier for fire spread.

    Simplified from Rothermel.
    """
    # Wind factor ∝ U^B where B ~ 1.5
    C = 7.47 * np.exp(-0.133 * fuel_bed_depth_ft**0.55)
    B = 0.02526 * fuel_bed_depth_ft**0.54

    if midflame_wind_mph < 0.5:
        return 1.0

    phi_w = C * (midflame_wind_mph**B)
    return 1 + phi_w

def spread_rate_with_wind(base_spread_ft_min, midflame_wind_mph, slope_percent=0):
    """
    Estimate spread rate with wind and slope.
    """
    wind_mult = wind_factor(midflame_wind_mph)

    # Slope factor: doubles spread for each 20% slope
    slope_mult = 1 + 0.05 * slope_percent

    return base_spread_ft_min * wind_mult * slope_mult

print("\nWind Effect on Spread Rate:")
print("Base spread: 5 ft/min in calm conditions")
print("-" * 60)
print(f"{'Midflame wind (mph)':<22} {'Wind factor':<15} {'Spread (ft/min)'}")
print("-" * 60)

for U in [0, 2, 5, 10, 15, 20, 30]:
    factor = wind_factor(U)
    spread = spread_rate_with_wind(5, U)
    print(f"{U:<22} {factor:<15.1f} {spread:.0f}")


# =============================================================================
# PART 4: SLOPE EFFECTS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SLOPE EFFECTS")
print("=" * 70)

slope_text = """
TOPOGRAPHY AND FIRE:
====================

SLOPE EFFECT:

Fire spreads faster UPHILL:
1. Flames tilt toward uphill fuels
2. Preheating by radiation/convection
3. Buoyancy assists spread

RULE OF THUMB:
Fire spread rate DOUBLES for each 20% increase in slope

More precisely:
Φ_s = 5.275 × β^(-0.3) × (tan θ)²

Where θ = slope angle

ASPECT:

South-facing (Northern Hemisphere):
- More solar radiation
- Drier fuels
- More fire-prone

CANYON EFFECTS:

CHIMNEY EFFECT:
- Steep narrow canyons
- Fire at bottom preheats entire slope
- Rapid upslope spread
- Extreme danger!

SADDLES AND RIDGES:
- Wind acceleration
- Enhanced fire behavior

SPOTTING DISTANCE:

Upslope: Embers lofted high, land far uphill
Flat: Embers travel with wind
Downslope: Limited spotting

DIURNAL PATTERNS:

Day: Upslope winds, fire spreads uphill
Night: Downslope drainage, reduced spread
Transition periods are DANGEROUS
"""
print(slope_text)

def slope_factor(slope_percent, packing_ratio=0.01):
    """
    Calculate slope effect on fire spread.

    Based on Rothermel.
    """
    tan_theta = slope_percent / 100
    phi_s = 5.275 * packing_ratio**(-0.3) * tan_theta**2
    return 1 + phi_s

def spread_rate_upslope(base_spread, slope_percent):
    """
    Estimate spread rate on slope.
    """
    factor = slope_factor(slope_percent)
    return base_spread * factor

print("\nSlope Effect on Spread Rate:")
print("Base spread: 5 ft/min on flat ground")
print("-" * 55)
print(f"{'Slope (%)':<15} {'Slope factor':<15} {'Spread (ft/min)':<15} {'Risk'}")
print("-" * 55)

for slope in [0, 10, 20, 30, 50, 75, 100]:
    factor = slope_factor(slope)
    spread = spread_rate_upslope(5, slope)
    if factor > 5:
        risk = "Extreme"
    elif factor > 2:
        risk = "Very high"
    elif factor > 1.5:
        risk = "High"
    else:
        risk = "Moderate"
    print(f"{slope:<15} {factor:<15.1f} {spread:<15.0f} {risk}")


# =============================================================================
# PART 5: FIRE WEATHER INDICES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: FIRE WEATHER INDICES")
print("=" * 70)

indices_text = """
FIRE WEATHER INDEX SYSTEMS:
===========================

1. US NATIONAL FIRE DANGER RATING SYSTEM (NFDRS):

Components:
- Spread Component (SC): 0-200+
- Energy Release Component (ERC): 0-100+
- Ignition Component (IC): 0-100
- Burning Index (BI): 0-200+

ERC = indicator of total energy release per unit area
High ERC → extreme fire behavior

2. CANADIAN FOREST FIRE WEATHER INDEX (FWI):

Fuel moisture codes:
- FFMC (Fine Fuel MC): 0-101
- DMC (Duff MC): 0-∞
- DC (Drought Code): 0-∞

Behavior indices:
- ISI (Initial Spread Index)
- BUI (Buildup Index)
- FWI (Fire Weather Index)

FWI interpretation:
0-5: Low
5-10: Moderate
10-20: High
20-30: Very High
>30: Extreme

3. HAINES INDEX:

Stability + dryness index (0-6):
Low: 2-3
Moderate: 4
High: 5-6

High Haines → plume-dominated fire, erratic behavior

4. HOT-DRY-WINDY INDEX (HDW):

HDW = max((T - Td) × U) over lowest 500 m

Combines:
- Vapor pressure deficit
- Wind speed
"""
print(indices_text)

def haines_index(T_850, T_700, Td_850):
    """
    Calculate Haines Index (stability + dryness).

    Low elevation version using 850 and 700 hPa.
    """
    # Stability term (A)
    delta_T = T_850 - T_700
    if delta_T < 4:
        A = 1
    elif delta_T < 8:
        A = 2
    else:
        A = 3

    # Moisture term (B)
    depression = T_850 - Td_850
    if depression < 6:
        B = 1
    elif depression < 10:
        B = 2
    else:
        B = 3

    return A + B

def hdw_index(T_C, Td_C, wind_ms):
    """
    Calculate Hot-Dry-Windy index.

    HDW = VPD × wind
    """
    # Vapor pressure deficit (simplified)
    e_s = 6.11 * 10**(7.5 * T_C / (237.3 + T_C))
    e = 6.11 * 10**(7.5 * Td_C / (237.3 + Td_C))
    VPD = e_s - e  # hPa

    hdw = VPD * wind_ms
    return hdw

print("\nHaines Index Examples:")
print("-" * 60)
print(f"{'T_850 (°C)':<12} {'T_700 (°C)':<12} {'Td_850 (°C)':<12} {'Haines':<10} {'Risk'}")
print("-" * 60)

conditions = [
    (20, 15, 15, "Moist, stable"),
    (25, 18, 10, "Moderate"),
    (30, 18, 5, "High"),
    (35, 20, 0, "Very high"),
    (35, 15, -5, "Extreme"),
]

for T850, T700, Td850, desc in conditions:
    H = haines_index(T850, T700, Td850)
    risk = "Low" if H <= 3 else "Moderate" if H == 4 else "High"
    print(f"{T850:<12} {T700:<12} {Td850:<12} {H:<10} {risk}")


# =============================================================================
# PART 6: PYROCONVECTION
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: PYROCONVECTION")
print("=" * 70)

pyro_text = """
PYROCONVECTION:
===============

Fire-generated convection - the most extreme fire behavior

FIRE PLUME DYNAMICS:

Heat release rate: Q (MW)
Buoyancy flux: F = g × Q / (ρ × c_p × T)

Plume rise: z = C × F^(1/4) × t^(3/4)

PYROCUMULUS (PyroCu):

Fire-induced cumulus cloud
Condensation of moisture from:
1. Combustion (1 kg fuel → ~0.5 kg H₂O)
2. Evaporated vegetation moisture
3. Entrained ambient moisture

Forms when smoke plume reaches LCL

PYROCUMULONIMBUS (PyroCb):

Fire-induced THUNDERSTORM!

Characteristics:
- Tops to 10-15+ km
- Lightning
- Downdraft outflows (erratic winds)
- Can inject smoke into stratosphere

Triggers:
- Large fire (>10,000 acres/hour spread)
- High Haines Index
- Unstable atmosphere
- Dry surface, moist aloft

DANGERS:
- Erratic wind shifts
- Extreme spotting (miles ahead)
- Fire whirls/tornadoes
- Lightning new starts

FEEDBACK LOOP:

Fire → Heat → Convection → Indraft → More O₂ → More fire
                ↓
           Lofted embers → Spot fires
"""
print(pyro_text)

def plume_height(heat_release_MW, ambient_stability='unstable'):
    """
    Estimate convective plume height.

    Simplified Briggs formula.
    """
    # Buoyancy flux (m⁴/s³)
    F = 9.81 * heat_release_MW * 1e6 / (1.2 * 1004 * 300)

    # Stability factor
    if ambient_stability == 'unstable':
        s_factor = 1.5
    elif ambient_stability == 'neutral':
        s_factor = 1.0
    else:
        s_factor = 0.6

    # Plume rise (simplified)
    z = s_factor * 5.0 * F**(1/4) * 1000**(3/4)

    return z / 1000  # km

def pyrocb_potential(fire_intensity_MW, haines, cape=0):
    """
    Estimate potential for pyroconvection.

    Returns: likelihood category
    """
    score = 0

    # Intensity contribution
    if fire_intensity_MW > 5000:
        score += 3
    elif fire_intensity_MW > 1000:
        score += 2
    elif fire_intensity_MW > 100:
        score += 1

    # Haines contribution
    if haines >= 6:
        score += 3
    elif haines >= 5:
        score += 2
    elif haines >= 4:
        score += 1

    # CAPE contribution
    if cape > 1500:
        score += 2
    elif cape > 500:
        score += 1

    if score >= 7:
        return "Very high"
    elif score >= 5:
        return "High"
    elif score >= 3:
        return "Moderate"
    else:
        return "Low"

print("\nPlume Height vs Fire Intensity:")
print("-" * 55)
print(f"{'Heat release (MW)':<20} {'Plume height (km)':<20} {'Column type'}")
print("-" * 55)

for Q in [10, 100, 500, 1000, 5000, 10000, 50000]:
    z = plume_height(Q)
    if z > 10:
        col_type = "PyroCb likely"
    elif z > 5:
        col_type = "PyroCu likely"
    else:
        col_type = "Smoke column"
    print(f"{Q:<20} {z:<20.1f} {col_type}")


# =============================================================================
# PART 7: CLIMATE CHANGE AND FIRE
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: CLIMATE CHANGE AND WILDFIRE")
print("=" * 70)

climate_text = """
CLIMATE-FIRE CONNECTION:
========================

OBSERVED TRENDS:

Western US:
- Fire season: 78 days longer since 1970s
- Area burned: 2-4× increase since 1980s
- Large fires: 7× more frequent

Australia, Mediterranean, Siberia: Similar trends

PHYSICAL MECHANISMS:

1. TEMPERATURE
   - Higher T → lower fuel moisture
   - Clausius-Clapeyron: 7% more VPD per °C
   - More days above fire danger thresholds

2. PRECIPITATION CHANGES
   - Less snowpack → earlier spring drying
   - Longer dry seasons
   - Flash droughts

3. VAPOR PRESSURE DEFICIT (VPD)
   VPD = e_s(T) - e
   Higher VPD → faster fuel drying
   VPD increasing ~0.1 hPa/decade

4. FIRE WEATHER DAYS
   Days with extreme fire weather increasing
   ~25% increase per °C warming

FEEDBACKS:

POSITIVE:
Fire → CO₂ → Warming → More fire
Fire → Black carbon on snow → Earlier melt → Drier fuels

NEGATIVE:
Fire → Reduced fuel load → Less fire (short term)
Fire → Vegetation shift → Changed fire regime

FUTURE PROJECTIONS:

+2°C warming:
- Fire frequency +100-200%
- Burned area +200-400%
- Fire season +20-30 days

+4°C warming:
- Much more extreme
- Novel fire regimes
"""
print(climate_text)

def fire_weather_days_increase(warming_C):
    """
    Estimate increase in extreme fire weather days.

    Based on ~25% per °C relationship.
    """
    return (1.25**warming_C - 1) * 100  # Percent increase

def vpd_from_temperature_increase(T_increase_C, baseline_T=25, baseline_RH=40):
    """
    Estimate VPD change from warming.

    Assumes constant specific humidity.
    """
    T0 = baseline_T
    T1 = T0 + T_increase_C

    e_s0 = 6.11 * 10**(7.5 * T0 / (237.3 + T0))
    e_s1 = 6.11 * 10**(7.5 * T1 / (237.3 + T1))

    # Actual vapor pressure stays same if specific humidity constant
    e = e_s0 * baseline_RH / 100

    VPD0 = e_s0 - e
    VPD1 = e_s1 - e

    return VPD0, VPD1, (VPD1 - VPD0) / VPD0 * 100

print("\nClimate Change Fire Impacts:")
print("-" * 60)
print(f"{'Warming (°C)':<15} {'Fire weather days':<20} {'VPD increase (%)'}")
print("-" * 60)

for dT in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]:
    fw_increase = fire_weather_days_increase(dT)
    _, _, vpd_inc = vpd_from_temperature_increase(dT)
    print(f"{dT:<15} +{fw_increase:<19.0f}% +{vpd_inc:.0f}%")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: FIRE WEATHER PHYSICS")
print("=" * 70)

summary = """
KEY FIRE WEATHER PHYSICS:
========================

1. FIRE TRIANGLE
   - Fuel + Heat + Oxygen
   - Byram intensity: I = H × w × R
   - Flame length ∝ I^0.46

2. FUEL MOISTURE
   - EMC from T and RH
   - Critical: <5% dead fuel moisture
   - Response time: 1-hr to 1000-hr fuels

3. WIND EFFECTS
   - Primary spread driver
   - Spread ∝ U^1.5 to U^2
   - Midflame wind = 0.3-0.5 × 20-ft wind

4. SLOPE EFFECTS
   - Doubles per 20% slope increase
   - Chimney effect in canyons
   - Upslope = upwind for fire

5. FIRE WEATHER INDICES
   - NFDRS: SC, ERC, BI
   - Canadian FWI: 0-6 scale
   - Haines: stability + dryness

6. PYROCONVECTION
   - Fire-generated clouds
   - PyroCu → PyroCb (thunderstorm)
   - Extreme/erratic behavior

7. CLIMATE CHANGE
   - +25% fire weather days per °C
   - VPD increasing rapidly
   - Fire seasons lengthening


THE PHYSICS TELLS US:
====================
- Wind > slope > fuel moisture for spread
- Fire creates its own weather
- Small moisture changes = big fire changes
- Climate change dramatically increasing risk
- Pyroconvection = game changer for fire behavior
"""
print(summary)

print("\n" + "=" * 70)
print("END OF FIRE WEATHER PHYSICS")
print("=" * 70)
