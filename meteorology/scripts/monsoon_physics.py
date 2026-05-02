#!/usr/bin/env python3
"""
Monsoon Physics: First-Principles Derivations
==============================================

Complete physics of monsoon circulations worldwide.

Key phenomena:
- Land-sea thermal contrast
- Hadley and monsoon cell dynamics
- Cross-equatorial flow
- Intraseasonal variability (ISO)
- Orographic precipitation

Starting from thermal circulation and angular momentum theory.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
Omega = 7.292e-5      # Earth's rotation rate [rad/s]
R_earth = 6.371e6     # Earth radius [m]
c_p = 1005            # Specific heat [J/kg/K]
sigma = 5.67e-8       # Stefan-Boltzmann constant [W/m²/K⁴]
L_v = 2.5e6           # Latent heat [J/kg]

print("="*70)
print("MONSOON PHYSICS: FIRST-PRINCIPLES DERIVATIONS")
print("="*70)

#############################################
# PART 1: LAND-SEA THERMAL CONTRAST
#############################################
print("\n" + "="*70)
print("PART 1: DIFFERENTIAL HEATING - THE MONSOON ENGINE")
print("="*70)

print("""
FUNDAMENTAL MONSOON MECHANISM:
=============================

SUMMER MONSOON (wet):
    Land heats faster than ocean
    → Low pressure over land
    → Moist air drawn from ocean to land
    → Rising motion, heavy rainfall

WINTER MONSOON (dry):
    Land cools faster than ocean
    → High pressure over land
    → Dry air flows from land to ocean
    → Subsidence, dry conditions

HEATING CONTRAST:
Why does land heat/cool faster?

1. HEAT CAPACITY:
   Ocean: c × ρ × d ~ 4000 × 1025 × 100 ~ 4×10⁸ J/m²/K
   Land: c × ρ × d ~ 1000 × 1500 × 1 ~ 1.5×10⁶ J/m²/K

   Ratio: Ocean ~ 250× greater heat capacity!

2. TRANSPARENCY:
   Solar radiation penetrates ocean 10-100 m
   Land absorbs at surface

3. EVAPORATION:
   Ocean: Unlimited moisture supply (cooling)
   Land: Limited moisture (less cooling)

TEMPERATURE RESPONSE:
For same solar input Q:
    ΔT = Q × Δt / (c × ρ × d)

Land responds ~100-250× faster than ocean.
""")

def surface_temperature_response(Q_net, duration_s, heat_capacity_per_m2):
    """
    Calculate temperature change from net heating.

    ΔT = Q × Δt / C
    """
    return Q_net * duration_s / heat_capacity_per_m2

def land_ocean_contrast(Q_solar, duration_s=86400, C_land=2e6, C_ocean=4e8):
    """
    Calculate land-ocean temperature contrast.
    """
    dT_land = surface_temperature_response(Q_solar, duration_s, C_land)
    dT_ocean = surface_temperature_response(Q_solar, duration_s, C_ocean)

    return dT_land, dT_ocean, dT_land - dT_ocean

def monsoon_pressure_gradient(dT, depth_km=5, T_mean=300):
    """
    Estimate pressure gradient from temperature contrast.

    Using hydrostatic equation and ideal gas:
    dp/dx ~ (p/RT) × g × dT/dx × H
    """
    # Simplified: 1°C temperature contrast over scale L
    # creates ~1 hPa pressure contrast per 100 km per 5 km depth
    dp = dT * depth_km / 5 * 100  # Pa per 100 km

    return dp

print("\nLand-ocean heating contrast (typical summer day):")
print("-" * 55)

Q_solar = 400  # W/m² average daily insolation

dT_land, dT_ocean, contrast = land_ocean_contrast(Q_solar)

print(f"  Daily solar heating: {Q_solar} W/m²")
print(f"  Land temperature change: {dT_land:.1f}°C")
print(f"  Ocean temperature change: {dT_ocean:.2f}°C")
print(f"  Land-ocean contrast: {contrast:.1f}°C")

print("\nSeasonal contrast buildup:")
print("-" * 50)
for days in [7, 30, 90]:
    dT_land, dT_ocean, contrast = land_ocean_contrast(200, days * 86400)
    print(f"  After {days:2.0f} days: Land-ocean ΔT = {contrast:.0f}°C")

#############################################
# PART 2: MONSOON CIRCULATION THEORY
#############################################
print("\n" + "="*70)
print("PART 2: MONSOON AS A GIANT SEA BREEZE")
print("="*70)

print("""
SEA BREEZE ANALOGY:
==================

Monsoon is essentially a continental-scale sea breeze:

SEA BREEZE (diurnal):
    Scale: 10-100 km
    Period: 24 hours
    Depth: 1-2 km

MONSOON (seasonal):
    Scale: 1000-10000 km
    Period: 365 days
    Depth: 10-15 km

THERMAL WIND MONSOON:
Continental heating creates low-level thermal low.
Meridional temperature gradient drives:
    ∂u/∂z = (g/fT) ∂T/∂y

INDIAN MONSOON:
Summer: Tibetan Plateau heating
    → Upper-level high (anticyclone)
    → Low-level monsoon trough
    → Cross-equatorial Somali jet
    → Monsoon onset June 1 (Kerala)

Winter: Siberian high
    → Offshore flow from Asia
    → Northeast monsoon
    → Dry season over India

ANGULAR MOMENTUM:
Cross-equatorial flow must conserve angular momentum:
    M = (u + Ωr cos φ) × r cos φ

Air crossing equator from SH gains westerly momentum
→ Somali Jet (40+ m/s low-level jet)
""")

def coriolis_parameter(lat_deg):
    """f = 2Ω sin(φ)"""
    return 2 * Omega * np.sin(np.radians(lat_deg))

def angular_momentum(u, lat_deg):
    """
    Calculate absolute angular momentum per unit mass.

    M = (u + Ω a cos φ) × a cos φ
    """
    a = R_earth
    phi = np.radians(lat_deg)
    return (u + Omega * a * np.cos(phi)) * a * np.cos(phi)

def wind_from_angular_momentum(M, lat_deg):
    """
    Calculate wind speed given M and latitude.

    u = M / (a cos φ) - Ω a cos φ
    """
    a = R_earth
    phi = np.radians(lat_deg)

    if np.cos(phi) == 0:
        return 0

    return M / (a * np.cos(phi)) - Omega * a * np.cos(phi)

def somali_jet_speed(lat_origin=-10, lat_jet=10, u_origin=0):
    """
    Estimate Somali Jet speed from angular momentum conservation.

    Air starts at lat_origin with u=u_origin,
    moves to lat_jet conserving M.
    """
    M = angular_momentum(u_origin, lat_origin)
    u_jet = wind_from_angular_momentum(M, lat_jet)
    return u_jet

print("\nCross-equatorial flow and Somali Jet:")
print("-" * 60)

# Air starting at 10°S with u = -5 m/s (easterly)
lat_start = -10
u_start = -5

M = angular_momentum(u_start, lat_start)
print(f"  Starting point: {lat_start}°, u = {u_start} m/s")
print(f"  Angular momentum: M = {M/1e9:.2f} × 10⁹ m²/s")

print("\n  Latitude  Wind speed (if M conserved)")
print("  " + "-" * 40)
for lat in [-10, -5, 0, 5, 10, 15]:
    u = wind_from_angular_momentum(M, lat)
    print(f"  {lat:>6.0f}°   {u:>+10.1f} m/s")

print("\n  Note: Strong westerlies develop in Somali Jet (~40 m/s observed)")

#############################################
# PART 3: INDIAN MONSOON SPECIFICS
#############################################
print("\n" + "="*70)
print("PART 3: INDIAN SUMMER MONSOON")
print("="*70)

print("""
INDIAN SUMMER MONSOON (ISM):
===========================

TIMELINE:
    May: Pre-monsoon buildup, heat low intensifies
    June 1: Onset over Kerala (±7 days)
    June 15: Reaches Mumbai
    July 1: Reaches Delhi
    July 15: Reaches northwest India
    Mid-September: Withdrawal begins (NW first)
    October: Withdrawal from south India

KEY FEATURES:

1. MONSOON TROUGH:
   Low pressure axis from Pakistan to Bay of Bengal
   Position determines rainfall distribution
   North position: Good rains in central India
   South position: Heavy rains in Himalayas/NE

2. TIBETAN HIGH:
   Upper-level anticyclone over Tibet
   Maintained by elevated heating (4500+ m plateau)
   Strength affects monsoon intensity

3. CROSS-EQUATORIAL FLOW:
   Somali Jet: 40+ m/s at ~1.5 km altitude
   Largest low-level jet in global circulation

4. WEST COAST OROGRAPHIC RAINFALL:
   Western Ghats force lifting
   Cherrapunji: 11,000+ mm annual (world record region)

MONSOON STRENGTH INDEX:
All-India Rainfall as % of long-term average:
    Drought: < 90%
    Normal: 90-110%
    Excess: > 110%

TELECONNECTIONS:
    El Niño → Weak monsoon (drought risk)
    La Niña → Strong monsoon (flood risk)
    IOD positive → Weak monsoon (sometimes)
""")

def monsoon_onset_date_kerala(sst_arabian_sea, shear_200hPa):
    """
    Simplified onset date prediction.

    Warmer Arabian Sea and weaker upper shear → earlier onset.
    Typical range: May 25 - June 7 (June 1 ± 7 days)
    """
    base_date = 152  # June 1 = day 152

    # Adjustments (very simplified)
    sst_adjustment = -2 * (sst_arabian_sea - 29)  # Days per °C above 29
    shear_adjustment = 0.5 * (shear_200hPa - 15)  # Days per m/s shear

    return base_date + sst_adjustment + shear_adjustment

def monsoon_rainfall_from_enso(nino34_anomaly):
    """
    Estimate monsoon rainfall anomaly from ENSO state.

    El Niño (positive Niño3.4) → negative rainfall anomaly
    La Niña → positive rainfall anomaly
    """
    # Roughly -3% per °C of Niño3.4 anomaly
    # This is a statistical relationship, not deterministic
    return -3 * nino34_anomaly  # % anomaly

def western_ghats_rainfall(moisture_flux, windward_slope=0.05):
    """
    Estimate orographic rainfall on Western Ghats.

    Rainfall ∝ moisture flux × slope
    """
    # Simplified: 1 kg/m/s moisture flux → 10 mm/day per 5% slope
    return moisture_flux * windward_slope / 0.05 * 10  # mm/day

print("\nMonsoon onset prediction examples:")
print("-" * 50)
for sst in [28.5, 29.0, 29.5, 30.0]:
    for shear in [10, 15, 20]:
        onset = monsoon_onset_date_kerala(sst, shear)
        # Convert to date
        month = 5 if onset < 152 else 6
        day = onset - 121 if onset < 152 else onset - 151
        print(f"  SST={sst}°C, Shear={shear}m/s: Onset ~ {month}/{day:.0f}")

print("\nMonsoon-ENSO relationship:")
print("-" * 45)
for nino in [-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5]:
    anomaly = monsoon_rainfall_from_enso(nino)
    state = "La Niña" if nino < -0.5 else "El Niño" if nino > 0.5 else "Neutral"
    print(f"  Niño3.4 = {nino:+.1f}°C ({state:8s}): Rainfall anomaly = {anomaly:+.0f}%")

#############################################
# PART 4: INTRASEASONAL OSCILLATION
#############################################
print("\n" + "="*70)
print("PART 4: INTRASEASONAL VARIABILITY (ACTIVE-BREAK CYCLES)")
print("="*70)

print("""
MONSOON INTRASEASONAL OSCILLATION (MISO):
========================================

Monsoon is NOT continuous - it has active and break phases:

ACTIVE PHASE:
    - Heavy rainfall over central India
    - Monsoon trough in normal position
    - Duration: 7-10 days

BREAK PHASE:
    - Reduced rainfall over central India
    - Enhanced rainfall in Himalayas and SE
    - Monsoon trough shifts north
    - Duration: 7-14 days

PERIODICITY:
    30-60 days (similar to MJO but distinct)
    Also 10-20 day mode (westward propagating)

PHYSICAL MECHANISM:
1. Active phase builds moisture over land
2. Land surface moisture feedback
3. Boundary layer destabilization
4. Eventually becomes too dry → break
5. Ocean recharges moisture → next active

BOREAL SUMMER INTRASEASONAL OSCILLATION (BSISO):
Northward propagating mode (1-2 m/s)
Starts over equatorial Indian Ocean
Propagates to Indian subcontinent
Related to MJO but with northward component

PREDICTABILITY:
Active/break transitions predictable 2-3 weeks ahead
Major source of extended-range forecast skill
""")

def active_break_index(rainfall_central_india, climatology=8):
    """
    Simple active/break classification.

    rainfall: mm/day over central India
    climatology: long-term mean
    """
    anomaly = rainfall_central_india - climatology

    if anomaly > 3:
        return "ACTIVE", anomaly
    elif anomaly < -3:
        return "BREAK", anomaly
    else:
        return "NORMAL", anomaly

def northward_propagation_time(lat_start, lat_end, speed_ms=1.5):
    """
    Estimate time for intraseasonal mode to propagate northward.
    """
    distance = (lat_end - lat_start) * 111000  # m
    time_days = distance / speed_ms / 86400
    return time_days

print("\nActive-break classification:")
print("-" * 50)
for rain in [2, 5, 8, 11, 14, 18]:
    phase, anomaly = active_break_index(rain)
    print(f"  Rainfall {rain:2.0f} mm/day: {phase:8s} (anomaly = {anomaly:+.0f})")

print("\nISO northward propagation timing:")
print("-" * 45)
for lat_start in [0, 5]:
    for lat_end in [15, 20, 25]:
        days = northward_propagation_time(lat_start, lat_end)
        print(f"  {lat_start}°N → {lat_end}°N: {days:.0f} days")

#############################################
# PART 5: GLOBAL MONSOON SYSTEMS
#############################################
print("\n" + "="*70)
print("PART 5: GLOBAL MONSOON SYSTEMS")
print("="*70)

print("""
MAJOR MONSOON REGIONS:
=====================

1. ASIAN-AUSTRALIAN MONSOON:
   - Indian monsoon: June-September
   - East Asian monsoon: May-August
   - Australian monsoon: December-March
   - Largest monsoon system globally

2. WEST AFRICAN MONSOON:
   - Onset: April (Guinea coast), July (Sahel)
   - Retreat: September-October
   - ITCZ migration north of equator
   - Sahel rainfall highly variable

3. NORTH AMERICAN MONSOON:
   - Onset: June-July
   - Region: Arizona, New Mexico, NW Mexico
   - Driven by heating of Mexican Plateau
   - Gulf of California moisture source

4. SOUTH AMERICAN MONSOON:
   - Onset: October-November
   - Peak: December-February
   - Amazon basin focus
   - Bolivian High aloft

GLOBAL MONSOON DOMAIN:
~2/3 of global tropical precipitation
~2 billion people directly dependent
Major driver of global atmospheric circulation

MONSOON-ENSO RELATIONSHIPS:
    Indian: Strong inverse relationship
    Australian: Strong inverse relationship
    West African: Moderate relationship
    North American: Weak relationship
""")

def monsoon_season_months(region):
    """
    Return monsoon season for different regions.
    """
    seasons = {
        'Indian': ('June', 'September'),
        'East Asian': ('May', 'August'),
        'Australian': ('December', 'March'),
        'West African': ('June', 'September'),
        'North American': ('July', 'September'),
        'South American': ('November', 'March'),
    }
    return seasons.get(region, ('Unknown', 'Unknown'))

def monsoon_rainfall_typical(region):
    """
    Return typical monsoon season rainfall in mm.
    """
    rainfall = {
        'Indian': 1500,  # All-India average
        'East Asian': 1000,
        'Australian': 1200,
        'West African': 800,
        'North American': 200,
        'South American': 1800,
    }
    return rainfall.get(region, 0)

print("\nGlobal monsoon characteristics:")
print("-" * 70)
print(f"{'Region':>18s}  {'Season':>20s}  {'Typical rainfall':>18s}")
print("-" * 70)

for region in ['Indian', 'East Asian', 'Australian', 'West African',
               'North American', 'South American']:
    start, end = monsoon_season_months(region)
    rain = monsoon_rainfall_typical(region)
    print(f"{region:>18s}  {start:>8s} - {end:8s}  {rain:>15.0f} mm")

#############################################
# PART 6: MONSOON AND CLIMATE CHANGE
#############################################
print("\n" + "="*70)
print("PART 6: MONSOON IN A WARMING CLIMATE")
print("="*70)

print("""
PROJECTED MONSOON CHANGES:
=========================

THERMODYNAMIC CHANGES:
1. Clausius-Clapeyron: ~7% more water vapor per °C
2. More moisture → potentially more rainfall

3. But also:
   - Changes in circulation strength
   - Changes in SST gradients
   - Aerosol effects (regional)

INDIAN MONSOON PROJECTIONS:
- Rainfall: +5 to +15% by 2100 (CMIP6)
- But higher variability (more droughts AND floods)
- Delayed onset possible
- Shorter, more intense season

PHYSICAL MECHANISMS:

MOISTURE EFFECT (enhances monsoon):
    More evaporation from warmer ocean
    Higher atmospheric moisture content
    Clausius-Clapeyron scaling

STABILITY EFFECT (weakens monsoon):
    Upper troposphere warms faster than surface
    Increased static stability
    Weakens deep convection

LAND-SEA CONTRAST:
    Complicated by:
    - Aerosol cooling over land (India, China)
    - Snow/ice albedo feedbacks
    - Regional circulation changes

NET EFFECT:
Most models show:
    Indian monsoon: Slight intensification, higher variability
    East Asian: Shifts northward, more variable
    Australian: Uncertain, possibly weaker
""")

def monsoon_rainfall_change_cc(delta_T, base_rainfall, cc_rate=0.07):
    """
    Estimate rainfall change from Clausius-Clapeyron scaling.

    ~7% increase per °C warming
    """
    factor = 1 + cc_rate * delta_T
    return base_rainfall * factor

def monsoon_circulation_change(delta_T, circulation_weakening_rate=0.02):
    """
    Estimate circulation weakening.

    Models suggest ~2-3% weakening per °C
    """
    return 1 - circulation_weakening_rate * delta_T

def net_monsoon_change(delta_T, base_rainfall):
    """
    Combine moisture and circulation effects.
    """
    moisture_effect = monsoon_rainfall_change_cc(delta_T, base_rainfall)
    circulation_factor = monsoon_circulation_change(delta_T)

    # Net change = moisture increase × circulation change
    return moisture_effect * circulation_factor

print("\nMonsoon rainfall projections (Indian monsoon baseline: 900 mm):")
print("-" * 55)
print(f"{'Warming (°C)':>14s}  {'Moisture':>12s}  {'Circulation':>12s}  {'Net':>12s}")
print("-" * 55)

baseline = 900  # mm
for dT in [1, 2, 3, 4]:
    moisture = monsoon_rainfall_change_cc(dT, baseline)
    circ = monsoon_circulation_change(dT)
    net = net_monsoon_change(dT, baseline)
    print(f"{dT:>14.0f}  {moisture:>10.0f} mm  {circ:>12.0%}  {net:>10.0f} mm")

print("\n  Note: Higher variability (extremes) is also projected!")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("MONSOON PHYSICS SUMMARY")
print("="*70)
print("""
Key Physics:

1. FUNDAMENTAL DRIVER:
   Land-sea thermal contrast
   Land heat capacity ~250× less than ocean
   → Continental heating in summer, cooling in winter

2. CIRCULATION:
   Thermally-direct cell (land-ocean-land)
   Cross-equatorial flow → Somali Jet (angular momentum)
   Upper-level anticyclone (Tibetan High)

3. INDIAN MONSOON:
   Onset: June 1 ± 7 days (Kerala)
   Duration: June-September
   ENSO linkage: El Niño → weak, La Niña → strong

4. INTRASEASONAL VARIABILITY:
   30-60 day active-break cycles
   Northward propagating BSISO
   Critical for forecasting

5. GLOBAL MONSOONS:
   Asian, African, American systems
   ~2/3 of tropical precipitation
   2+ billion people dependent

6. CLIMATE CHANGE:
   Moisture increase (~7%/°C) vs circulation weakening
   Net: slight intensification, higher variability
   More extreme droughts AND floods

Monsoons are the pulse of tropical climate,
driving agriculture and water resources for billions!
""")

if __name__ == "__main__":
    print("\n[Monsoon Physics Module - Complete]")
