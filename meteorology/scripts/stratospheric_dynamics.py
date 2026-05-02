#!/usr/bin/env python3
"""
STRATOSPHERIC DYNAMICS - FIRST PRINCIPLES
==========================================

Deriving the physics of the stratosphere: QBO, polar vortex,
sudden stratospheric warmings, and stratosphere-troposphere coupling.
"""

import numpy as np

print("=" * 70)
print("STRATOSPHERIC DYNAMICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
R_d = 287.0        # Gas constant dry air (J/kg/K)
c_p = 1004         # Specific heat (J/kg/K)
omega = 7.29e-5    # Earth rotation rate (rad/s)
R_earth = 6.371e6  # Earth radius (m)


# =============================================================================
# PART 1: STRATOSPHERIC STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: STRATOSPHERIC STRUCTURE")
print("=" * 70)

structure_text = """
STRATOSPHERIC STRUCTURE:
========================

VERTICAL STRUCTURE:
- Tropopause: ~10-16 km (varies with latitude)
- Stratosphere: 10-50 km
- Stratopause: ~50 km
- Temperature INCREASES with height (inversion!)

WHY TEMPERATURE INCREASES:

OZONE ABSORPTION

O₃ + UV (λ < 320 nm) → O₂ + O

This reaction:
1. Absorbs UV radiation (protects Earth!)
2. Releases heat
3. Warms the stratosphere

Temperature profile (stratosphere):
T(z) ≈ T_tropopause + γ_strat × (z - z_trop)

Where γ_strat ≈ +2 K/km (positive!)

CONSEQUENCES OF STABLE STRATIFICATION:

1. Very little vertical mixing
2. Suppressed convection
3. Layered structure
4. Long residence times (years)
5. Horizontal transport dominates

BREWER-DOBSON CIRCULATION:

Large-scale overturning:
- Air rises in tropical tropopause
- Poleward flow in stratosphere
- Descends at high latitudes
- Driven by wave drag!

Mass flux ≈ 10⁹ kg/s
Turnover time ≈ 5 years
"""
print(structure_text)

def stratospheric_temperature(z_km, T_tropopause=220, gamma_strat=2):
    """
    Calculate stratospheric temperature profile.

    z_km: Height in km
    T_tropopause: Temperature at tropopause (K)
    gamma_strat: Stratospheric lapse rate (K/km, positive = warming with height)
    """
    z_trop = 12  # Tropopause height (km)
    if z_km < z_trop:
        return None  # Tropospheric calculation different
    z_strat = z_km - z_trop
    T = T_tropopause + gamma_strat * z_strat
    # Cap at stratopause
    T_max = 270  # Approximate stratopause temperature
    return min(T, T_max)

def brunt_vaisala_stratosphere(dT_dz_per_km=2):
    """
    Calculate N² in stratosphere.

    dT_dz_per_km: Lapse rate in K/km (positive = increasing with height)
    """
    dT_dz = dT_dz_per_km / 1000  # Convert to K/m
    T_mean = 240  # Representative stratospheric T
    gamma_d = g / c_p  # ~0.0098 K/m

    # N² = (g/T) × (dT/dz + g/c_p)
    # In stratosphere, dT/dz > 0, so very stable
    N_squared = (g / T_mean) * (dT_dz + gamma_d)
    return np.sqrt(N_squared)

print("\nStratospheric Temperature Profile:")
print("-" * 50)
print(f"{'Height (km)':<15} {'Temperature (K)':<20}")
print("-" * 50)

for z in [12, 15, 20, 25, 30, 35, 40, 45, 50]:
    T = stratospheric_temperature(z)
    if T:
        print(f"{z:<15} {T:<20.0f}")

N_strat = brunt_vaisala_stratosphere()
print(f"\nStratospheric N = {N_strat:.4f} s⁻¹")
print(f"(Compare troposphere: N ≈ 0.01 s⁻¹)")


# =============================================================================
# PART 2: QUASI-BIENNIAL OSCILLATION (QBO)
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: QUASI-BIENNIAL OSCILLATION (QBO)")
print("=" * 70)

qbo_text = """
QBO: THE STRATOSPHERIC METRONOME
================================

OBSERVATION:
Equatorial stratospheric winds alternate between
EASTERLY and WESTERLY with ~28-month period!

Discovered: 1960s (balloon observations)

CHARACTERISTICS:
- Period: 22-34 months (mean ~28)
- Altitude: 16-50 km (max amplitude ~30 km)
- Latitude: Confined to ±10-15° of equator
- Amplitude: 30-50 m/s
- Descends at ~1 km/month

THE MECHANISM - WAVE-MEAN FLOW INTERACTION:

1. Equatorial waves propagate from troposphere
   - Kelvin waves (eastward)
   - Rossby-gravity waves (westward)

2. Waves deposit momentum where they dissipate
   - Eastward waves → eastward momentum
   - Westward waves → westward momentum

3. Critical level interaction:
   - Wave is absorbed where c = U (phase speed = wind)
   - Momentum deposited, accelerates mean flow

4. FEEDBACK:
   - Eastward winds → absorb eastward waves → more eastward
   - Until westward waves break through from below
   - Then westward regime begins!

LINDZEN-HOLTON THEORY (1968):

∂U/∂t = -∂F/∂z + diffusion

Where F = wave momentum flux

Self-sustaining oscillation from wave-mean flow feedback!

QBO IMPACTS ON WEATHER:
- Modulates stratospheric polar vortex
- Affects hurricane activity (weak effect)
- Influences monsoon strength
- Used for seasonal forecasting
"""
print(qbo_text)

def qbo_descent_rate(wave_amplitude, background_N=0.02):
    """
    Estimate QBO descent rate.

    Proportional to wave momentum flux / density
    """
    # Simplified: descent rate ~ wave amplitude²
    # Typical: 1 km/month
    descent_m_per_day = 0.03 * (wave_amplitude / 10)**2 * 1000  # m/day
    return descent_m_per_day / 30  # km/month

def qbo_period_estimate(descent_rate_km_month, layer_depth_km=15):
    """
    Estimate QBO period from descent rate.

    Period = 2 × (time to traverse layer)
    Factor of 2 for both phases
    """
    traverse_time = layer_depth_km / descent_rate_km_month  # months
    period = 2 * traverse_time
    return period

print("\nQBO Dynamics:")
print("-" * 60)
print(f"{'Wave amplitude':<18} {'Descent (km/mo)':<18} {'Period (months)'}")
print("-" * 60)

for wave_amp in [5, 10, 15, 20]:
    descent = qbo_descent_rate(wave_amp)
    period = qbo_period_estimate(descent)
    print(f"{wave_amp:<18} {descent:<18.2f} {period:<.0f}")


# =============================================================================
# PART 3: POLAR VORTEX
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: POLAR VORTEX")
print("=" * 70)

vortex_text = """
STRATOSPHERIC POLAR VORTEX:
===========================

WHAT IT IS:
Large-scale cyclonic (westerly) circulation
around the winter pole in the stratosphere

FORMATION:

Winter pole receives NO solar heating
→ Extreme cooling (T < 200 K in Antarctic!)
→ Huge temperature gradient (pole to equator)
→ Thermal wind → strong westerlies

THERMAL WIND BALANCE:

∂u_g/∂z = -(g/fT) × ∂T/∂y

Strong meridional temperature gradient
→ Strong vertical wind shear
→ Westerlies increase with height

POLAR VORTEX PROPERTIES:

Arctic (NH):
- Weaker (more land, more waves)
- More variable
- Often disturbed by sudden warmings
- Centered near pole or displaced

Antarctic (SH):
- Stronger (less land, fewer waves)
- More symmetric
- More stable
- Ozone hole develops inside

POLAR NIGHT JET:

Maximum wind at vortex edge
Speed: 50-100 m/s
Height: 30-50 km

VORTEX STRENGTH INDEX:

Often measured by:
- 10 hPa geopotential height
- 60°N zonal wind
- Temperature contrast

Strong vortex → Cold, stable Arctic
Weak vortex → Warm, disturbed Arctic
"""
print(vortex_text)

def thermal_wind_vortex(dT_dy, lat, z_bottom, z_top, T_mean=230):
    """
    Calculate zonal wind at vortex edge.

    dT_dy: Meridional temperature gradient (K/m)
    """
    f = 2 * omega * np.sin(np.radians(lat))

    # Thermal wind: du/dz = -(g/fT) × dT/dy
    du_dz = -(g / (f * T_mean)) * dT_dy

    # Integrate over height
    dz = z_top - z_bottom
    u_top = du_dz * dz

    return u_top

def vortex_edge_temperature(lat):
    """
    Estimate temperature at polar vortex edge.
    """
    # Simple model: T decreases poleward
    T_equator = 260  # K at stratospheric equator
    T_pole = 200  # K at winter pole
    T = T_equator - (T_equator - T_pole) * np.sin(np.radians(lat))
    return T

print("\nPolar Vortex Thermal Wind:")
print("-" * 70)
print(f"{'ΔT (K/1000km)':<18} {'Lat':<10} {'Depth (km)':<12} {'Jet speed (m/s)'}")
print("-" * 70)

for dT_per_1000km in [20, 40, 60, 80]:  # K per 1000 km
    dT_dy = dT_per_1000km / 1e6  # K/m
    for lat in [60, 70]:
        u_jet = thermal_wind_vortex(dT_dy, lat, 15000, 35000)
        print(f"{dT_per_1000km:<18} {lat:<10} {20:<12} {u_jet:.0f}")


# =============================================================================
# PART 4: SUDDEN STRATOSPHERIC WARMING (SSW)
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SUDDEN STRATOSPHERIC WARMING")
print("=" * 70)

ssw_text = """
SUDDEN STRATOSPHERIC WARMING (SSW):
===================================

The most dramatic event in the stratosphere!

DEFINITION (WMO):
- Polar temperature increase > 25 K in a week
- At 10 hPa (~30 km)

MAJOR SSW:
- Reversal of 60°N zonal wind (westerly → easterly)
- Complete breakdown of polar vortex

MINOR SSW:
- Significant warming
- Vortex weakened but not reversed

MECHANISM - PLANETARY WAVE BREAKING:

1. Planetary waves (Rossby waves) propagate from troposphere
   - Forced by land-sea contrast, mountains
   - Wavenumber 1-2 (hemispheric scale)

2. Waves break in stratosphere
   - Deposit eastward momentum
   - DECELERATE westerly vortex

3. Wave forcing overwhelms radiative cooling
   - Net warming occurs
   - Vortex weakens or collapses

CHARNEY-DRAZIN CRITERION:

Waves can only propagate into stratosphere when:

0 < U < U_c = β / (k² + l²)

Where:
- U = zonal mean wind
- U_c = critical wind speed
- β = Rossby parameter
- k, l = wavenumbers

If U too strong: wave reflects
If U easterly: wave cannot propagate

During SSW: Waves cause U to decrease → more waves enter → positive feedback!

TYPES:
1. DISPLACEMENT: Vortex pushed off pole
2. SPLIT: Vortex breaks into two pieces

IMPACTS:

Stratospheric warming → tropospheric cooling!
- Coupling takes 2-4 weeks
- NAO/AO becomes negative
- Cold air outbreaks over continents
- Predictability enhancement!
"""
print(ssw_text)

def charney_drazin_criterion(lat=60, wavenumber=1):
    """
    Calculate critical wind speed for wave propagation.

    U_c = β / (k² + l²)

    Waves propagate when 0 < U < U_c
    """
    beta = 2 * omega * np.cos(np.radians(lat)) / R_earth
    a = R_earth * np.cos(np.radians(lat))

    k = wavenumber / a  # Zonal wavenumber
    l = 0  # Meridional (simplified)

    U_c = beta / (k**2 + l**2)
    return U_c

def wave_driving_deceleration(wave_amplitude_m, wavenumber=1, lat=60):
    """
    Estimate wind deceleration from wave drag.

    Simplified EP flux divergence.
    """
    # Wave momentum flux ~ amplitude²
    # Deceleration ~ flux divergence
    decel = 0.1 * (wave_amplitude_m / 500)**2  # m/s per day
    return decel

print("\nCharney-Drazin Critical Velocities:")
print("-" * 50)
print(f"{'Wavenumber':<15} {'Latitude':<15} {'U_c (m/s)'}")
print("-" * 50)

for wn in [1, 2, 3]:
    for lat in [50, 60, 70]:
        U_c = charney_drazin_criterion(lat, wn)
        print(f"{wn:<15} {lat:<15} {U_c:<.0f}")

print("\n\nSSW Timeline (Conceptual):")
print("-" * 60)
print("Week 0: Strong vortex, westerlies ~60 m/s")
print("Week 1: Wave forcing increases, U drops to ~40 m/s")
print("Week 2: Rapid deceleration, warming begins")
print("Week 3: Zonal wind reverses, T rises 30-50 K")
print("Week 4-8: Slow recovery, tropospheric impacts")


# =============================================================================
# PART 5: STRATOSPHERE-TROPOSPHERE COUPLING
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: STRATOSPHERE-TROPOSPHERE COUPLING")
print("=" * 70)

coupling_text = """
STRATOSPHERE-TROPOSPHERE COUPLING:
==================================

Information flows BOTH ways!

UPWARD COUPLING (Troposphere → Stratosphere):
- Planetary waves forced by topography
- Convective wave generation
- QBO driven by tropospheric waves
- Time scale: days to weeks

DOWNWARD COUPLING (Stratosphere → Troposphere):
- SSW → cold air outbreaks (2-4 weeks)
- QBO → hurricane modulation
- Polar vortex → NAO/AO
- Time scale: weeks to months

MECHANISM - WAVE REFLECTION:

After SSW:
1. Vortex weakens → U decreases
2. Charney-Drazin criterion violated
3. Waves REFLECT back to troposphere
4. Modified wave activity changes tropospheric circulation

MECHANISM - POTENTIAL VORTICITY:

Stratospheric PV anomalies can propagate downward
∂q/∂t + v·∇q = 0 (PV conservation)

Strong PV anomalies in stratosphere
→ Induce circulation in troposphere

ANNULAR MODES:

NAO / NAM (Northern Annular Mode)
- Surface pressure: Iceland vs Azores
- Connected to stratospheric vortex strength

Strong vortex → Positive NAO → mild winters (Europe)
Weak vortex → Negative NAO → cold winters (Europe)

PREDICTABILITY ENHANCEMENT:

SSW events give 2-4 weeks additional forecast skill!
- Monitoring stratosphere improves surface forecasts
- Now routinely used in extended-range prediction

TROPOSPHERIC PRECURSORS:

Before SSW:
- Enhanced wave flux from troposphere
- Often preceded by specific blocking patterns
- Pacific/Atlantic blocking → wave generation → SSW
"""
print(coupling_text)

def nao_index_from_vortex(vortex_wind_anomaly):
    """
    Estimate NAO response to vortex state.

    vortex_wind_anomaly: + = strong, - = weak (m/s)
    """
    # Rough empirical relationship
    # ~1 standard deviation NAO per 20 m/s vortex anomaly
    nao = vortex_wind_anomaly / 20
    return nao

def ssw_temperature_anomaly_surface(weeks_after_ssw):
    """
    Model surface temperature response to SSW.

    Based on observational composites.
    """
    # Maximum cold anomaly 2-4 weeks after SSW
    # Then gradual recovery
    if weeks_after_ssw < 2:
        anomaly = -0.5 * weeks_after_ssw  # Building
    elif weeks_after_ssw < 5:
        anomaly = -2  # Maximum cold
    else:
        anomaly = -2 + 0.3 * (weeks_after_ssw - 5)  # Recovery
    return min(anomaly, 0)

print("\nStratospheric Vortex → Surface NAO:")
print("-" * 55)
print(f"{'Vortex anomaly (m/s)':<25} {'Expected NAO index'}")
print("-" * 55)

for vort_anom in [-40, -20, 0, 20, 40]:
    nao = nao_index_from_vortex(vort_anom)
    sign = "Strong" if vort_anom > 0 else "Weak" if vort_anom < 0 else "Normal"
    print(f"{vort_anom:<25} {nao:+.1f} ({sign} vortex)")

print("\n\nSurface T anomaly after major SSW:")
print("-" * 50)
for week in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    T_anom = ssw_temperature_anomaly_surface(week)
    print(f"Week {week}: {T_anom:+.1f}°C")


# =============================================================================
# PART 6: OZONE AND CHEMISTRY
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: STRATOSPHERIC OZONE")
print("=" * 70)

ozone_text = """
STRATOSPHERIC OZONE:
====================

THE OZONE LAYER:

Maximum concentration at 20-25 km
Total column: ~300 DU (Dobson Units)
1 DU = 0.01 mm at STP

CHAPMAN CYCLE (Natural):

Production:
O₂ + UV (λ < 242 nm) → O + O
O + O₂ + M → O₃ + M

Destruction:
O₃ + UV (λ < 320 nm) → O₂ + O*
O + O₃ → 2 O₂

OZONE HOLE (Anthropogenic):

Polar stratospheric clouds (PSCs):
- Form when T < 195 K
- Only in Antarctic (and sometimes Arctic)
- Surface for heterogeneous chemistry

On PSC surfaces:
ClONO₂ + HCl → Cl₂ + HNO₃

Sunlight returns:
Cl₂ + hν → 2 Cl
Cl + O₃ → ClO + O₂
ClO + O → Cl + O₂
NET: O₃ + O → 2 O₂

CATALYTIC:
One Cl atom destroys ~100,000 O₃ molecules!

RECOVERY:

Montreal Protocol (1987): Phase out CFCs
Recovery ongoing:
- Antarctic hole still forms each spring
- But shrinking since ~2000
- Full recovery expected ~2060

OZONE-CLIMATE CONNECTION:

1. Ozone absorbs UV → stratospheric heating
2. Less ozone → cooler stratosphere
3. Changed temperature gradient → changed winds
4. Affects tropospheric climate!
"""
print(ozone_text)

def ozone_destruction_rate(chlorine_ppb, temperature, has_psc=False):
    """
    Estimate relative ozone destruction rate.

    Simplified model.
    """
    base_rate = chlorine_ppb / 3  # Relative to peak CFC levels

    # Temperature effect (PSC formation)
    if temperature < 195:
        has_psc = True

    if has_psc:
        rate = base_rate * 10  # Heterogeneous chemistry much faster
    else:
        rate = base_rate

    return rate

print("\nOzone Depletion Factors:")
print("-" * 60)
print(f"{'Cl (ppb)':<12} {'T (K)':<12} {'PSC?':<12} {'Relative rate'}")
print("-" * 60)

for cl in [1, 2, 3, 4]:
    for T in [200, 195, 190, 185]:
        has_psc = T < 195
        rate = ozone_destruction_rate(cl, T)
        psc_str = "Yes" if has_psc else "No"
        print(f"{cl:<12} {T:<12} {psc_str:<12} {rate:.1f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: STRATOSPHERIC DYNAMICS")
print("=" * 70)

summary = """
KEY STRATOSPHERIC PHYSICS:
=========================

1. STRATOSPHERIC STRUCTURE
   - Temperature INCREASES with height (ozone absorption)
   - Very stable (N² large)
   - Suppressed vertical mixing
   - Brewer-Dobson overturning circulation

2. QUASI-BIENNIAL OSCILLATION (QBO)
   - 28-month period of wind reversal
   - Wave-mean flow interaction
   - Kelvin + Rossby-gravity waves
   - Affects tropical weather/hurricanes

3. POLAR VORTEX
   - Winter cyclonic circulation
   - Driven by polar cooling
   - Thermal wind balance
   - Stronger in Antarctic than Arctic

4. SUDDEN STRATOSPHERIC WARMING
   - Rapid polar warming (30-50 K)
   - Vortex breakdown
   - Planetary wave breaking
   - Major impact on surface weather!

5. STRATOSPHERE-TROPOSPHERE COUPLING
   - Two-way interaction
   - SSW → cold air outbreaks (2-4 weeks)
   - Extended-range predictability
   - NAO/AO connection

6. OZONE
   - Chapman cycle (natural)
   - CFC-driven depletion (anthropogenic)
   - Polar stratospheric clouds key
   - Recovery underway (Montreal Protocol)


THE PHYSICS TELLS US:
====================
- Wave-mean flow interaction drives QBO and SSWs
- Thermal wind creates polar vortex
- Charney-Drazin criterion controls wave propagation
- Stratosphere affects surface with 2-4 week lag
- This provides predictability beyond synoptic scale!
"""
print(summary)

print("\n" + "=" * 70)
print("END OF STRATOSPHERIC DYNAMICS")
print("=" * 70)
