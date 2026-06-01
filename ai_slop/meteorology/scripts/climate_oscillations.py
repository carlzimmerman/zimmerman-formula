#!/usr/bin/env python3
"""
Climate Oscillations: First-Principles Derivations
===================================================

Complete physics of major climate variability modes.

Key phenomena:
- ENSO (El Niño - Southern Oscillation)
- PDO (Pacific Decadal Oscillation)
- AMO (Atlantic Multidecadal Oscillation)
- NAO (North Atlantic Oscillation)
- IOD (Indian Ocean Dipole)
- MJO (Madden-Julian Oscillation)
- QBO (Quasi-Biennial Oscillation)

Starting from ocean-atmosphere dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
Omega = 7.292e-5      # Earth's rotation rate [rad/s]
rho_water = 1025      # Seawater density [kg/m³]
rho_air = 1.2         # Air density [kg/m³]
c_p_water = 4000      # Specific heat of water [J/kg/K]
R_earth = 6.371e6     # Earth radius [m]

print("="*70)
print("CLIMATE OSCILLATIONS: FIRST-PRINCIPLES PHYSICS")
print("="*70)

#############################################
# PART 1: FUNDAMENTAL OCEAN-ATMOSPHERE COUPLING
#############################################
print("\n" + "="*70)
print("PART 1: OCEAN-ATMOSPHERE COUPLING FUNDAMENTALS")
print("="*70)

print("""
COUPLED SYSTEM DYNAMICS:
=======================

The ocean and atmosphere form a coupled system where:

1. ATMOSPHERE FORCES OCEAN:
   - Wind stress drives currents
   - Heat/freshwater fluxes modify SST/salinity
   - Pressure gradients affect sea level

2. OCEAN FORCES ATMOSPHERE:
   - SST patterns modify atmospheric heating
   - Evaporation provides moisture/latent heat
   - Ocean heat transport affects climate

TIMESCALES:
   Atmosphere: Days to weeks (fast adjustment)
   Mixed layer: Weeks to months
   Thermocline: Months to years
   Deep ocean: Decades to centuries

KEY COUPLING MECHANISMS:

WIND-EVAPORATION-SST (WES) FEEDBACK:
   Wind → Evaporation → SST cooling
   SST gradient → Wind change → Amplification

BJERKNES FEEDBACK (ENSO):
   Warm SST → Weak trades → Weaker upwelling
   → Warmer SST → Amplification (positive feedback)

EKMAN TRANSPORT:
   τ_x → V_Ekman = τ_x / (ρ_w f)   (perpendicular to wind)

   Convergence/divergence → upwelling/downwelling
""")

def coriolis_parameter(latitude_deg):
    """
    Calculate Coriolis parameter f = 2Ω sin(φ)
    """
    return 2 * Omega * np.sin(np.radians(latitude_deg))

def ekman_transport(wind_stress, latitude_deg):
    """
    Calculate Ekman mass transport.

    M_E = τ / f   [kg/m/s] perpendicular to wind
    """
    f = coriolis_parameter(latitude_deg)
    if abs(f) < 1e-6:
        return float('inf')  # Undefined at equator
    return wind_stress / f

def mixed_layer_response_time(depth_m, latitude_deg):
    """
    Estimate mixed layer adjustment time.

    From Ekman pumping timescale.
    """
    f = coriolis_parameter(latitude_deg)
    if abs(f) < 1e-6:
        return float('inf')

    # Inertial period
    T_inertial = 2 * np.pi / abs(f) / 86400  # days

    # Mixed layer response ~ few inertial periods
    return 5 * T_inertial  # days

def rossby_wave_speed(latitude_deg, baroclinic_mode=1):
    """
    Calculate baroclinic Rossby wave phase speed.

    c_R = -β R²_d   (westward propagation)
    """
    lat = np.radians(latitude_deg)
    beta = 2 * Omega * np.cos(lat) / R_earth

    # Rossby radius of deformation (first baroclinic mode)
    c_n = 2.5 if baroclinic_mode == 1 else 1.0  # m/s internal gravity wave speed
    f = coriolis_parameter(latitude_deg)

    if abs(lat) < np.radians(5):
        # Near equator, use equatorial Rossby radius
        R_d = np.sqrt(c_n / beta)
    else:
        R_d = c_n / abs(f)

    # Rossby wave speed
    c_R = -beta * R_d**2

    return c_R  # m/s (negative = westward)

print("\nOcean-atmosphere coupling parameters:")
print("-" * 55)
print(f"{'Latitude':>10s}  {'f (×10⁵)':>12s}  {'M_E (kg/m/s)':>14s}  {'T_resp (days)':>14s}")
print("-" * 55)
tau = 0.1  # N/m² typical wind stress
for lat in [5, 15, 30, 45, 60]:
    f = coriolis_parameter(lat)
    M_E = ekman_transport(tau, lat)
    T = mixed_layer_response_time(50, lat)
    print(f"{lat:>10.0f}°  {f*1e5:>12.2f}  {M_E:>14.1f}  {T:>14.1f}")

print("\nBaroclinic Rossby wave speeds:")
print("-" * 40)
for lat in [5, 10, 15, 20, 30]:
    c = rossby_wave_speed(lat)
    # Time to cross Pacific (~15000 km)
    time_months = 15e6 / abs(c) / 86400 / 30
    print(f"  {lat}°: c = {c*100:.1f} cm/s, Pacific crossing: {time_months:.0f} months")

#############################################
# PART 2: ENSO - EL NIÑO SOUTHERN OSCILLATION
#############################################
print("\n" + "="*70)
print("PART 2: ENSO PHYSICS")
print("="*70)

print("""
ENSO: THE DOMINANT MODE OF INTERANNUAL VARIABILITY
=================================================

NORMAL CONDITIONS:
- Trade winds blow westward across Pacific
- Warm pool in west, cold tongue in east
- Thermocline deep in west, shallow in east
- Walker circulation: Rising in west, sinking in east

EL NIÑO:
- Trade winds weaken
- Warm water sloshes eastward (Kelvin wave)
- Thermocline flattens
- Upwelling reduced → SST warms in east
- Walker circulation weakens

LA NIÑA:
- Trade winds strengthen
- Stronger upwelling in east → cold anomaly
- Enhanced Walker circulation

BJERKNES FEEDBACK (positive):
   +SST(east) → -ΔP(east-west) → -Trades
   → +SST(east) (amplification)

DELAYED OSCILLATOR MODEL:
   dT/dt = a T - b T(t - τ)

Where:
   a = Bjerknes feedback coefficient
   b = Delayed negative feedback (oceanic waves)
   τ = Wave transit time (~6-9 months)

RECHARGE-DISCHARGE MODEL:
   dT/dt = a T + b h
   dh/dt = -c T - ε h

Where:
   T = Eastern Pacific SST anomaly
   h = Warm water volume (thermocline depth)

Period: T = 2π / √(bc - a²/4) ≈ 3-7 years
""")

def delayed_oscillator(T0, a, b, tau_months, duration_years):
    """
    Simple delayed oscillator model for ENSO.

    dT/dt = a T - b T(t-τ)
    """
    dt = 0.1  # months
    n_steps = int(duration_years * 12 / dt)
    delay_steps = int(tau_months / dt)

    T = np.zeros(n_steps)
    T[:delay_steps] = T0  # Initial condition

    for i in range(delay_steps, n_steps):
        dTdt = a * T[i-1] - b * T[i - delay_steps]
        T[i] = T[i-1] + dTdt * dt

    time = np.arange(n_steps) * dt / 12  # years
    return time, T

def recharge_discharge_model(T0, h0, a, b, c, epsilon, duration_years):
    """
    Recharge-discharge model for ENSO.

    dT/dt = a T + b h
    dh/dt = -c T - ε h
    """
    dt = 0.1  # months
    n_steps = int(duration_years * 12 / dt)

    T = np.zeros(n_steps)
    h = np.zeros(n_steps)
    T[0] = T0
    h[0] = h0

    for i in range(1, n_steps):
        dTdt = a * T[i-1] + b * h[i-1]
        dhdt = -c * T[i-1] - epsilon * h[i-1]

        T[i] = T[i-1] + dTdt * dt
        h[i] = h[i-1] + dhdt * dt

    time = np.arange(n_steps) * dt / 12  # years
    return time, T, h

def enso_period(a, b, c):
    """
    Calculate ENSO period from recharge-discharge parameters.
    """
    discriminant = b*c - a**2/4
    if discriminant > 0:
        omega = np.sqrt(discriminant)
        period = 2 * np.pi / omega / 12  # years
        return period
    else:
        return None  # Overdamped

# Run delayed oscillator model
print("\nDelayed Oscillator simulation:")
time, T = delayed_oscillator(T0=0.5, a=0.5, b=0.6, tau_months=6, duration_years=20)
# Find approximate period
peaks = np.where((T[1:-1] > T[:-2]) & (T[1:-1] > T[2:]))[0]
if len(peaks) > 2:
    period = np.mean(np.diff(time[peaks]))
    print(f"  Simulated period: {period:.1f} years")

# ENSO indices
print("\nENSO characterization:")
print("-" * 50)
print("""
NINO REGIONS:
  Niño 1+2: 0-10°S, 90°-80°W (far eastern Pacific)
  Niño 3:   5°N-5°S, 150°-90°W (central-eastern)
  Niño 3.4: 5°N-5°S, 170°-120°W (central Pacific)
  Niño 4:   5°N-5°S, 160°E-150°W (central-western)

THRESHOLDS (Niño 3.4 SST anomaly):
  El Niño:  > +0.5°C for 5+ consecutive months
  La Niña:  < -0.5°C for 5+ consecutive months
  Strong:   > ±1.5°C
  Very strong: > ±2.0°C (1997-98, 2015-16 El Niños)

GLOBAL IMPACTS:
  - Drought in Indonesia/Australia
  - Floods in Peru/Ecuador
  - Weak Indian monsoon
  - Atlantic hurricane suppression
  - Global temperature anomaly +0.1-0.2°C
""")

#############################################
# PART 3: PDO - PACIFIC DECADAL OSCILLATION
#############################################
print("\n" + "="*70)
print("PART 3: PACIFIC DECADAL OSCILLATION (PDO)")
print("="*70)

print("""
PDO: LEADING MODE OF NORTH PACIFIC SST VARIABILITY
=================================================

SPATIAL PATTERN:
- Warm phase: Cool central North Pacific, warm eastern Pacific
- Cool phase: Opposite pattern
- Like ENSO extended to higher latitudes

TIMESCALE: 20-30 year cycles
   (Much longer than ENSO's 3-7 years)

PHYSICAL MECHANISMS:
1. Tropical-extratropical teleconnections (ENSO forcing)
2. Midlatitude air-sea interaction
3. Ocean gyre adjustments (decadal timescale)
4. Subduction of temperature anomalies

ROSSBY WAVE MECHANISM:
Wind stress curl anomalies generate baroclinic Rossby waves.
These propagate westward, adjusting thermocline.
At western boundary: Kelvin waves carry signal equatorward.

SUBDUCTION PATHWAY:
Surface anomalies subduct along isopycnals.
Travel equatorward in thermocline (years to decades).
Re-emerge to affect tropical SST.

PDO INDEX:
First EOF of North Pacific SST anomalies (north of 20°N).
Positive phase: Warm eastern Pacific, cool central.

KNOWN REGIME SHIFTS:
  1925, 1947, 1977, 1998 (approximate)
""")

def wind_stress_curl_sverdrup(tau_x, tau_y, dx, dy, latitude_deg):
    """
    Calculate Sverdrup transport from wind stress curl.

    ∇ × τ = ∂τ_y/∂x - ∂τ_x/∂y
    ψ = (1/ρβ) ∫ (∇×τ) dx
    """
    beta = 2 * Omega * np.cos(np.radians(latitude_deg)) / R_earth

    # Wind stress curl (simplified)
    curl = tau_y / dx - tau_x / dy  # Approximate

    # Sverdrup transport
    transport = curl / (rho_water * beta)

    return transport

def gyre_adjustment_time(basin_width_km, latitude_deg):
    """
    Estimate gyre adjustment time via Rossby waves.
    """
    c_R = abs(rossby_wave_speed(latitude_deg))
    time_years = (basin_width_km * 1000) / c_R / (86400 * 365)
    return time_years

print("\nPDO-related timescales:")
print("-" * 55)
print(f"{'Latitude':>10s}  {'Rossby wave speed':>18s}  {'Pacific crossing':>16s}")
print("-" * 55)
pacific_width = 12000  # km
for lat in [20, 30, 40, 50]:
    c = rossby_wave_speed(lat)
    time = gyre_adjustment_time(pacific_width, lat)
    print(f"{lat:>10.0f}°  {abs(c)*100:>15.1f} cm/s  {time:>14.1f} years")

print("\n  Mid-latitude Rossby waves take 10-20 years to cross Pacific!")
print("  This sets the decadal timescale of PDO.")

#############################################
# PART 4: AMO - ATLANTIC MULTIDECADAL OSCILLATION
#############################################
print("\n" + "="*70)
print("PART 4: ATLANTIC MULTIDECADAL OSCILLATION (AMO)")
print("="*70)

print("""
AMO: BASIN-WIDE NORTH ATLANTIC SST VARIABILITY
=============================================

SPATIAL PATTERN:
Uniform warming/cooling of entire North Atlantic (0-70°N).
Unlike PDO, pattern is more spatially uniform.

TIMESCALE: 60-80 year cycle
   (Longer than PDO due to thermohaline circulation)

PHYSICAL MECHANISM:
Atlantic Meridional Overturning Circulation (AMOC)

1. Strong AMOC → More heat transport northward
   → Warm North Atlantic (positive AMO)

2. Warm AMO → More freshwater (precip, ice melt)
   → Reduced deep water formation
   → Weakened AMOC

3. Weak AMOC → Less heat transport
   → Cool North Atlantic (negative AMO)

4. Cool AMO → Denser surface water
   → Enhanced deep water formation
   → Strengthened AMOC

AMOC TRANSPORT:
   Q ≈ 17 Sv at 26°N (1 Sv = 10⁶ m³/s)
   Heat transport: ~1.3 PW northward

AMO INDEX:
Detrended, area-weighted North Atlantic SST anomaly.

KNOWN PHASES:
   Cool: 1900-1925, 1965-1995
   Warm: 1925-1965, 1995-present

IMPACTS:
- Sahel rainfall (positive correlation)
- Atlantic hurricanes (more in warm phase)
- European summer climate
- North American drought patterns
""")

def amoc_heat_transport(volume_transport_Sv, delta_T=10):
    """
    Calculate AMOC heat transport.

    Q = ρ c_p V ΔT
    """
    V = volume_transport_Sv * 1e6  # m³/s
    Q = rho_water * c_p_water * V * delta_T  # W
    return Q / 1e15  # PW

def amoc_response_time(latitude_deg=50):
    """
    Estimate AMOC response timescale.

    Related to deep water transit time.
    """
    # Approximate: Deep water takes 100-1000 years
    # for full circuit, but relevant timescale is
    # overturning time ~ volume/transport

    # Atlantic volume above 1000m: ~4e16 m³
    # AMOC: ~17 Sv = 5e14 m³/year
    volume = 4e16  # m³
    transport = 17e6 * 86400 * 365  # m³/year

    return volume / transport  # years

print("\nAMOC characteristics:")
print("-" * 45)
for V_Sv in [10, 15, 17, 20, 25]:
    Q = amoc_heat_transport(V_Sv)
    print(f"  AMOC = {V_Sv} Sv: Heat transport = {Q:.2f} PW")

print(f"\n  Overturning timescale: ~{amoc_response_time():.0f} years")
print("  This sets the multidecadal AMO period (60-80 years)")

#############################################
# PART 5: NAO - NORTH ATLANTIC OSCILLATION
#############################################
print("\n" + "="*70)
print("PART 5: NORTH ATLANTIC OSCILLATION (NAO)")
print("="*70)

print("""
NAO: DOMINANT MODE OF ATMOSPHERIC VARIABILITY
============================================

PATTERN:
Sea level pressure seesaw between:
- Icelandic Low (65°N)
- Azores High (35°N)

NAO+ (strong pressure gradient):
- Strong westerlies over North Atlantic
- Mild, wet winters in Northern Europe
- Cold, dry in Mediterranean/Southern Europe
- Cold in Eastern Canada/Greenland

NAO- (weak pressure gradient):
- Weak westerlies, more blocking
- Cold winters in Northern Europe
- Wet in Mediterranean
- Mild in Eastern Canada/Greenland

PHYSICAL MECHANISM:
Internal atmospheric dynamics:
- Eddy-mean flow interaction
- Rossby wave breaking
- Stratospheric coupling

NAO INDEX:
Normalized SLP difference: Azores - Iceland
or: First EOF of Atlantic sector SLP

TIMESCALES:
- Intrinsic timescale: ~10-14 days
- Longer persistence from:
  * Ocean memory (SST feedback)
  * Snow cover feedback
  * Stratospheric coupling

PREDICTABILITY:
- Week 2: Some skill from stratosphere
- Seasonal: Limited (chaotic atmospheric dynamics)
- Decadal: May be influenced by ocean/external forcing
""")

def geostrophic_wind(delta_p, distance, latitude_deg, rho=1.2):
    """
    Calculate geostrophic wind from pressure gradient.

    U_g = (1/ρf) × (∂p/∂n)
    """
    f = coriolis_parameter(latitude_deg)
    if abs(f) < 1e-6:
        return float('inf')

    dp_dn = delta_p / distance
    return dp_dn / (rho * abs(f))

def nao_index_from_pressures(p_azores, p_iceland, p_azores_clim=1020, p_iceland_clim=1010,
                              std_azores=10, std_iceland=15):
    """
    Calculate NAO index from station pressures.

    NAO = (P_azores - P_azores_clim)/σ - (P_iceland - P_iceland_clim)/σ
    """
    z_azores = (p_azores - p_azores_clim) / std_azores
    z_iceland = (p_iceland - p_iceland_clim) / std_iceland

    return z_azores - z_iceland

print("\nNAO and associated circulation:")
print("-" * 55)
# Distance Iceland to Azores ~ 3000 km
distance = 3e6  # m
avg_lat = 50

for delta_p_hPa in [10, 20, 30, 40]:  # Azores - Iceland
    delta_p_Pa = delta_p_hPa * 100
    U_g = geostrophic_wind(delta_p_Pa, distance, avg_lat)
    print(f"  ΔP = {delta_p_hPa} hPa: Geostrophic wind = {U_g:.1f} m/s")

print("\nNAO index examples:")
print("-" * 55)
cases = [
    ("Strong NAO+", 1030, 990),
    ("Moderate NAO+", 1025, 1000),
    ("Neutral", 1020, 1010),
    ("Moderate NAO-", 1015, 1020),
    ("Strong NAO-", 1010, 1025)
]
for name, p_az, p_ic in cases:
    idx = nao_index_from_pressures(p_az, p_ic)
    print(f"  {name:15s}: Azores={p_az}, Iceland={p_ic}, NAO={idx:+.2f}")

#############################################
# PART 6: IOD - INDIAN OCEAN DIPOLE
#############################################
print("\n" + "="*70)
print("PART 6: INDIAN OCEAN DIPOLE (IOD)")
print("="*70)

print("""
IOD: ZONAL SST GRADIENT IN TROPICAL INDIAN OCEAN
===============================================

PATTERN:
East-west SST gradient across tropical Indian Ocean.

IOD+ (positive):
- Cool eastern Indian Ocean (off Sumatra/Java)
- Warm western Indian Ocean
- Weakened Walker circulation over Indian Ocean
- Enhanced upwelling off Sumatra

IOD- (negative):
- Opposite pattern
- Warm eastern, cool western
- Enhanced convection over Indonesia

PHYSICAL MECHANISM:
Bjerknes-like feedback (similar to ENSO):
- Wind-thermocline-SST feedback
- Weaker than Pacific (smaller basin)

SEASONALITY:
- Develops: May-June
- Peak: September-November
- Decays: December (monsoon transition)

DIPOLE MODE INDEX (DMI):
SST(western box) - SST(eastern box)
Western: 50-70°E, 10°S-10°N
Eastern: 90-110°E, 10°S-0°

RELATIONSHIP WITH ENSO:
- Often co-varies with ENSO
- But can occur independently
- IOD+ often accompanies El Niño

IMPACTS:
- Australian drought (IOD+)
- East African floods (IOD+)
- Indonesian fires/haze (IOD+)
- Indian monsoon modulation
""")

def iod_index(sst_west, sst_east, west_clim=28.0, east_clim=28.5):
    """
    Calculate Indian Ocean Dipole Mode Index.

    DMI = SST(west) - SST(east)
    """
    return (sst_west - west_clim) - (sst_east - east_clim)

print("\nIOD characterization:")
print("-" * 55)
print(f"{'SST West':>10s}  {'SST East':>10s}  {'DMI':>8s}  {'Phase':>15s}")
print("-" * 55)
cases = [
    (29.5, 26.5, "Strong IOD+"),
    (28.5, 27.5, "Moderate IOD+"),
    (28.0, 28.5, "Neutral"),
    (27.5, 29.5, "Moderate IOD-"),
    (27.0, 30.0, "Strong IOD-")
]
for sst_w, sst_e, phase in cases:
    dmi = iod_index(sst_w, sst_e)
    print(f"{sst_w:>10.1f}  {sst_e:>10.1f}  {dmi:>+8.1f}  {phase:>15s}")

#############################################
# PART 7: MJO - MADDEN-JULIAN OSCILLATION
#############################################
print("\n" + "="*70)
print("PART 7: MADDEN-JULIAN OSCILLATION (MJO)")
print("="*70)

print("""
MJO: DOMINANT INTRASEASONAL VARIABILITY
======================================

CHARACTERISTICS:
- Eastward-propagating tropical convection
- Period: 30-60 days
- Zonal wavenumber 1-3
- Propagation speed: ~5 m/s

STRUCTURE:
Large-scale envelope of convection with:
- Active phase: Enhanced rainfall
- Suppressed phase: Reduced rainfall
- Moves east at ~5 m/s
- Circumnavigates tropics in 30-60 days

VERTICAL STRUCTURE:
- Deep convection in active region
- Low-level convergence ahead (east)
- Upper-level divergence
- Kelvin wave structure to east
- Rossby wave structure to west

PHYSICAL MECHANISM:
Still debated! Leading theories:
1. Moisture-mode: Moisture recycling
2. Wave-CISK: Convection-wave interaction
3. Cloud-radiation feedback

KEY EQUATIONS:
Moisture-mode framework:
   ∂q/∂t = -M ω - (q-q*)/τ

Where:
   q = column moisture
   M = gross moist stability
   τ = moisture relaxation time

IMPACTS:
- Tropical cyclone activity (active/suppressed)
- Monsoon breaks and onsets
- Teleconnections to midlatitudes
- Week 2-4 predictability source
""")

def mjo_propagation_speed():
    """
    Estimate MJO propagation speed.

    Based on moisture mode theory: c ~ M/∂q/∂z
    Typically 4-8 m/s observed.
    """
    # Simplified estimate
    c_kelvin = 15  # m/s dry Kelvin wave
    reduction_factor = 0.3  # Moisture slows propagation
    return c_kelvin * reduction_factor

def mjo_period(propagation_speed_ms):
    """
    Calculate MJO period from propagation speed.

    Period = Circumference / Speed
    """
    circumference = 2 * np.pi * R_earth * np.cos(np.radians(10))  # At 10°
    period_days = circumference / propagation_speed_ms / 86400
    return period_days

def mjo_phase(longitude_deg):
    """
    Approximate MJO phase from convective center longitude.

    Standard 8-phase definition.
    """
    # Simplified phase mapping
    if 80 < longitude_deg < 100:
        return 2, "Indian Ocean"
    elif 100 <= longitude_deg < 120:
        return 3, "Maritime Continent"
    elif 120 <= longitude_deg < 140:
        return 4, "Maritime Continent"
    elif 140 <= longitude_deg < 160:
        return 5, "Western Pacific"
    elif 160 <= longitude_deg < 180:
        return 6, "Western Pacific"
    elif -180 <= longitude_deg < -150:
        return 7, "Western Hemisphere"
    elif -150 <= longitude_deg < -120:
        return 8, "Africa"
    else:
        return 1, "Western Indian Ocean"

c_mjo = mjo_propagation_speed()
period = mjo_period(c_mjo)

print(f"\nMJO characteristics:")
print(f"  Propagation speed: ~{c_mjo:.1f} m/s")
print(f"  Period: ~{period:.0f} days")
print(f"  Wavelength: ~{40000:.0f} km (wavenumber 1)")

print("\nMJO phases and typical locations:")
print("-" * 45)
for phase in range(1, 9):
    lons = [60, 80, 100, 120, 140, 160, 180, 40]
    p, region = mjo_phase(lons[phase-1])
    print(f"  Phase {phase}: {region}")

#############################################
# PART 8: INTERACTIONS AND PREDICTABILITY
#############################################
print("\n" + "="*70)
print("PART 8: MODE INTERACTIONS AND PREDICTABILITY")
print("="*70)

print("""
INTERACTIONS BETWEEN CLIMATE MODES:
==================================

ENSO ↔ PDO:
- ENSO projects onto PDO pattern
- PDO modulates ENSO amplitude
- PDO warm phase: Stronger El Niños
- PDO cool phase: Stronger La Niñas

ENSO ↔ IOD:
- Often co-occur (not independent)
- El Niño favors positive IOD
- La Niña favors negative IOD
- But independent events exist

ENSO ↔ AMO:
- Less direct coupling
- Both affect global mean temperature
- AMO may modulate Atlantic response to ENSO

MJO ↔ ENSO:
- MJO can trigger/influence ENSO events
- Westerly wind bursts from MJO
- ENSO state modulates MJO activity

NAO ↔ Stratosphere:
- Polar vortex disruptions → negative NAO
- Strong vortex → positive NAO
- 2-4 week downward coupling

PREDICTABILITY SOURCES:
======================

Timescale      Source              Skill horizon
Hours-days     Initial conditions   1-2 weeks
Weeks          MJO, stratosphere    2-4 weeks
Months         ENSO                 6-12 months
Years          AMO, PDO             Limited

ENSO is the largest source of seasonal predictability!
""")

print("\nPredictability estimates by mode:")
print("-" * 55)
modes = [
    ("Weather (initial cond.)", "10-14 days"),
    ("MJO", "2-4 weeks"),
    ("ENSO", "6-9 months"),
    ("IOD", "3-6 months"),
    ("NAO", "~2 weeks"),
    ("PDO", "Limited (decadal)"),
    ("AMO", "Limited (multidecadal)")
]
for mode, horizon in modes:
    print(f"  {mode:25s}: {horizon}")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("CLIMATE OSCILLATIONS SUMMARY")
print("="*70)
print("""
Major Climate Variability Modes:

1. ENSO (3-7 years):
   - Bjerknes feedback, delayed oscillator
   - Largest interannual signal globally
   - Pacific basin coupled mode

2. PDO (20-30 years):
   - North Pacific SST pattern
   - Rossby wave adjustment timescale
   - ENSO-like but decadal

3. AMO (60-80 years):
   - Atlantic basin SST
   - AMOC-related variability
   - Influences hurricanes, Sahel rainfall

4. NAO (days to weeks):
   - Atmospheric internal mode
   - Iceland-Azores pressure seesaw
   - European winter climate driver

5. IOD (annual):
   - Indian Ocean dipole
   - Bjerknes-like feedback
   - Australian/East African impacts

6. MJO (30-60 days):
   - Intraseasonal propagating convection
   - Week 2-4 predictability source
   - Influences TCs, monsoons

Key Physics:
- Ocean-atmosphere coupling
- Rossby/Kelvin wave dynamics
- Delayed feedback oscillators
- Thermohaline circulation

Understanding these modes is crucial for
seasonal prediction and climate projections!
""")

if __name__ == "__main__":
    print("\n[Climate Oscillations Module - First Principles Complete]")
