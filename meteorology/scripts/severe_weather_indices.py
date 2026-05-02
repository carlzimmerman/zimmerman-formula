#!/usr/bin/env python3
"""
Severe Weather Indices: First-Principles Derivations
=====================================================

Complete physics of convective parameters and severe weather forecasting.

Key indices:
- CAPE and variants (MUCAPE, SBCAPE, DCAPE)
- Wind shear parameters (bulk shear, SRH, EHI)
- Composite indices (STP, SCP, SHIP)
- Stability parameters (LI, K-index, TT)
- Moisture parameters (PW, RH profiles)

Starting from parcel theory and hodograph analysis.
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81              # Gravitational acceleration [m/s²]
R_d = 287.05          # Gas constant for dry air [J/kg/K]
R_v = 461.5           # Gas constant for water vapor [J/kg/K]
c_p = 1005            # Specific heat of dry air [J/kg/K]
c_pv = 1870           # Specific heat of water vapor [J/kg/K]
L_v = 2.5e6           # Latent heat of vaporization [J/kg]
p_0 = 100000          # Reference pressure [Pa]
kappa = R_d / c_p     # Poisson constant

print("="*70)
print("SEVERE WEATHER INDICES: FIRST-PRINCIPLES DERIVATIONS")
print("="*70)

#############################################
# PART 1: CAPE - CONVECTIVE AVAILABLE POTENTIAL ENERGY
#############################################
print("\n" + "="*70)
print("PART 1: CAPE FUNDAMENTALS")
print("="*70)

print("""
CAPE DERIVATION FROM PARCEL THEORY:
==================================

A rising parcel experiences buoyancy force:
    F_b = g × (ρ_env - ρ_parcel) / ρ_env
        = g × (T_v,parcel - T_v,env) / T_v,env

CAPE is work done by buoyancy from LFC to EL:

    CAPE = ∫[LFC to EL] g × (T_v,parcel - T_v,env) / T_v,env × dz

Or in pressure coordinates:

    CAPE = -R_d ∫[p_LFC to p_EL] (T_v,parcel - T_v,env) × d(ln p)

CAPE VARIANTS:
    SBCAPE: Surface-based (parcel from surface)
    MUCAPE: Most Unstable (parcel with max θ_e in lowest 300 hPa)
    MLCAPE: Mixed Layer (parcel from lowest 100 hPa mean)

PHYSICAL INTERPRETATION:
    CAPE = (1/2) w_max²
    w_max = √(2 × CAPE)

    CAPE 1000 J/kg → w_max = 45 m/s
    CAPE 3000 J/kg → w_max = 77 m/s
    CAPE 5000 J/kg → w_max = 100 m/s

CAPE THRESHOLDS:
    < 300 J/kg: Marginally unstable
    300-1000: Moderately unstable
    1000-2500: Very unstable
    2500-4000: Extremely unstable
    > 4000: Explosive instability
""")

def saturation_vapor_pressure(T_K):
    """Calculate saturation vapor pressure [Pa] from temperature [K]."""
    T_C = T_K - 273.15
    return 611.2 * np.exp(17.67 * T_C / (T_C + 243.5))

def mixing_ratio(e, p):
    """Calculate mixing ratio from vapor pressure and total pressure."""
    return 0.622 * e / (p - e)

def virtual_temperature(T, r):
    """Calculate virtual temperature."""
    return T * (1 + 0.61 * r)

def potential_temperature(T, p, p0=100000):
    """Calculate potential temperature."""
    return T * (p0 / p) ** kappa

def equivalent_potential_temperature(T, p, r):
    """
    Calculate equivalent potential temperature.

    θ_e ≈ θ × exp(L_v × r / (c_p × T))
    """
    theta = potential_temperature(T, p)
    return theta * np.exp(L_v * r / (c_p * T))

def moist_adiabatic_lapse_rate(T, p):
    """Calculate moist adiabatic lapse rate [K/m]."""
    e_s = saturation_vapor_pressure(T)
    r_s = mixing_ratio(e_s, p)

    numerator = 1 + (L_v * r_s) / (R_d * T)
    denominator = 1 + (L_v**2 * r_s) / (c_p * R_v * T**2)

    return g / c_p * numerator / denominator

def cape_simple(T_parcel_profile, T_env_profile, z_profile, LFC_idx, EL_idx):
    """
    Calculate CAPE from temperature profiles.

    CAPE = ∫ g × (T_v,p - T_v,e) / T_v,e × dz
    """
    cape = 0
    for i in range(LFC_idx, EL_idx):
        dT = T_parcel_profile[i] - T_env_profile[i]
        T_env = T_env_profile[i]
        dz = z_profile[i+1] - z_profile[i]

        if dT > 0:  # Only positive buoyancy contributes
            cape += g * dT / T_env * dz

    return cape

def max_updraft_from_cape(cape):
    """Calculate theoretical maximum updraft speed."""
    return np.sqrt(2 * cape)

def cape_category(cape):
    """Categorize CAPE value."""
    if cape < 300:
        return "Marginally unstable"
    elif cape < 1000:
        return "Moderately unstable"
    elif cape < 2500:
        return "Very unstable"
    elif cape < 4000:
        return "Extremely unstable"
    else:
        return "Explosive"

print("\nCAPE and theoretical updraft speeds:")
print("-" * 55)
print(f"{'CAPE (J/kg)':>12s}  {'w_max (m/s)':>12s}  {'w_max (mph)':>12s}  {'Category':>18s}")
print("-" * 55)

for cape in [250, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000]:
    w = max_updraft_from_cape(cape)
    cat = cape_category(cape)
    print(f"{cape:>12.0f}  {w:>12.1f}  {w*2.237:>12.0f}  {cat:>18s}")

#############################################
# PART 2: CIN AND DCAPE
#############################################
print("\n" + "="*70)
print("PART 2: CIN AND DOWNDRAFT CAPE")
print("="*70)

print("""
CONVECTIVE INHIBITION (CIN):
===========================

CIN is negative buoyancy that must be overcome:

    CIN = -∫[SFC to LFC] g × (T_v,parcel - T_v,env) / T_v,env × dz

Where parcel is COOLER than environment (capped).

CIN THRESHOLDS:
    < 25 J/kg: Weak cap (storms initiate easily)
    25-50: Moderate cap
    50-100: Strong cap
    100-200: Very strong cap
    > 200: Extreme cap (storms unlikely without forcing)

DOWNDRAFT CAPE (DCAPE):
======================

Energy available for downdrafts (evaporative cooling):

    DCAPE = ∫[SFC to origin] g × (T_v,env - T_v,parcel) / T_v,env × dz

Parcel descends moist adiabatically with evaporative cooling.

DCAPE > 1000 J/kg: Strong downdraft potential
    → Damaging surface winds
    → Microbursts

Maximum downdraft speed: w_down = -√(2 × DCAPE)
""")

def cin_category(cin):
    """Categorize CIN value."""
    cin = abs(cin)
    if cin < 25:
        return "Weak cap"
    elif cin < 50:
        return "Moderate cap"
    elif cin < 100:
        return "Strong cap"
    elif cin < 200:
        return "Very strong cap"
    else:
        return "Extreme cap"

def downdraft_potential(dcape):
    """Assess downdraft potential from DCAPE."""
    if dcape < 500:
        return "Weak"
    elif dcape < 1000:
        return "Moderate"
    elif dcape < 1500:
        return "Strong"
    else:
        return "Extreme"

print("\nCIN thresholds and storm initiation:")
print("-" * 55)
for cin in [0, 25, 50, 75, 100, 150, 200, 300]:
    cat = cin_category(cin)
    print(f"  CIN = {cin:3.0f} J/kg: {cat}")

print("\nDCAPE and downdraft speeds:")
print("-" * 50)
for dcape in [250, 500, 750, 1000, 1250, 1500, 2000]:
    w_down = np.sqrt(2 * dcape)
    pot = downdraft_potential(dcape)
    print(f"  DCAPE = {dcape:4.0f} J/kg: w_down = {w_down:.0f} m/s ({pot})")

#############################################
# PART 3: WIND SHEAR PARAMETERS
#############################################
print("\n" + "="*70)
print("PART 3: WIND SHEAR AND HODOGRAPH ANALYSIS")
print("="*70)

print("""
BULK WIND SHEAR:
===============

Vector difference between two levels:
    Shear = V(z_top) - V(z_bottom)
    |Shear| = √[(u_top - u_bottom)² + (v_top - v_bottom)²]

KEY LAYERS:
    0-1 km: Low-level shear (tornado potential)
    0-3 km: Low-level storm organization
    0-6 km: Deep layer shear (supercell potential)

THRESHOLDS (0-6 km):
    < 20 kt: Weak (ordinary cells)
    20-35 kt: Moderate (multicells)
    35-50 kt: Strong (supercells possible)
    > 50 kt: Extreme (supercells likely)

STORM-RELATIVE HELICITY (SRH):
=============================

    SRH = -∫[0 to h] (v - v_s)(∂u/∂z) - (u - u_s)(∂v/∂z) dz

Where (u_s, v_s) = storm motion

SRH measures streamwise vorticity (rotation potential).

0-1 km SRH thresholds:
    > 100 m²/s²: Significant tornado potential
    > 200 m²/s²: Strong tornado potential
    > 300 m²/s²: Violent tornado potential

0-3 km SRH thresholds:
    > 150 m²/s²: Tornado possible
    > 250 m²/s²: Significant tornadoes
    > 400 m²/s²: Violent tornadoes
""")

def bulk_shear(u_bottom, v_bottom, u_top, v_top):
    """Calculate bulk wind shear magnitude."""
    du = u_top - u_bottom
    dv = v_top - v_bottom
    return np.sqrt(du**2 + dv**2)

def storm_relative_helicity(u_profile, v_profile, z_profile, u_storm, v_storm, z_top=3000):
    """
    Calculate storm-relative helicity.
    """
    srh = 0
    for i in range(len(z_profile) - 1):
        if z_profile[i] >= z_top:
            break

        dz = z_profile[i+1] - z_profile[i]

        # Storm-relative winds
        u_sr = 0.5 * (u_profile[i] + u_profile[i+1]) - u_storm
        v_sr = 0.5 * (v_profile[i] + v_profile[i+1]) - v_storm

        # Vertical shear
        du_dz = (u_profile[i+1] - u_profile[i]) / dz
        dv_dz = (v_profile[i+1] - v_profile[i]) / dz

        # Helicity contribution
        srh += (v_sr * du_dz - u_sr * dv_dz) * dz

    return -srh

def shear_category(shear_kt):
    """Categorize wind shear."""
    if shear_kt < 20:
        return "Weak (pulse storms)"
    elif shear_kt < 35:
        return "Moderate (multicells)"
    elif shear_kt < 50:
        return "Strong (supercells possible)"
    else:
        return "Extreme (supercells likely)"

def srh_tornado_potential(srh_0_1km, srh_0_3km):
    """Assess tornado potential from SRH."""
    if srh_0_1km > 300 or srh_0_3km > 400:
        return "Violent tornado possible"
    elif srh_0_1km > 200 or srh_0_3km > 250:
        return "Strong tornado possible"
    elif srh_0_1km > 100 or srh_0_3km > 150:
        return "Tornado possible"
    else:
        return "Tornado unlikely"

print("\n0-6 km bulk shear thresholds:")
print("-" * 55)
for shear in [10, 20, 30, 40, 50, 60, 70]:
    cat = shear_category(shear)
    print(f"  {shear:2.0f} kt ({shear*0.514:.0f} m/s): {cat}")

print("\nSRH and tornado potential:")
print("-" * 60)
print(f"{'SRH 0-1km':>12s}  {'SRH 0-3km':>12s}  {'Assessment':>30s}")
print("-" * 60)
cases = [(50, 100), (100, 200), (150, 250), (200, 300), (250, 400), (350, 500)]
for s1, s3 in cases:
    assessment = srh_tornado_potential(s1, s3)
    print(f"{s1:>12.0f}  {s3:>12.0f}  {assessment:>30s}")

#############################################
# PART 4: COMPOSITE PARAMETERS
#############################################
print("\n" + "="*70)
print("PART 4: COMPOSITE INDICES")
print("="*70)

print("""
SIGNIFICANT TORNADO PARAMETER (STP):
===================================

    STP = (SBCAPE/1500) × (SRH_eff/150) × (Shear_eff/20) ×
          ((2000-LCL)/1000) × ((CIN+200)/150)

Where:
    SBCAPE: Surface-based CAPE [J/kg]
    SRH_eff: Effective SRH [m²/s²]
    Shear_eff: Effective bulk shear [m/s]
    LCL: Lifted condensation level [m AGL]
    CIN: Convective inhibition [J/kg]

STP THRESHOLDS:
    > 1: Significant tornado possible
    > 2: Significant tornado likely
    > 5: Violent tornado possible

SUPERCELL COMPOSITE PARAMETER (SCP):
===================================

    SCP = (MUCAPE/1000) × (SRH_eff/50) × (Shear_eff/20)

SCP THRESHOLDS:
    > 1: Supercell possible
    > 4: Supercell likely
    > 10: Significant supercell

SIGNIFICANT HAIL PARAMETER (SHIP):
=================================

    SHIP = (MUCAPE × r × γ × T_500 × Shear) / 42,000,000

Where:
    r = mixing ratio at LPL
    γ = lapse rate 700-500 hPa
    T_500 = 500 hPa temperature
    Shear = 0-6 km shear

SHIP > 1: Large hail possible
SHIP > 2: Significant hail likely
""")

def significant_tornado_parameter(cape, srh, shear_ms, lcl_m, cin):
    """
    Calculate Significant Tornado Parameter.

    Normalized so STP=1 is threshold for significant tornadoes.
    """
    # Normalize each term
    cape_term = min(cape / 1500, 2)
    srh_term = min(srh / 150, 2)
    shear_term = min(shear_ms / 20, 1.5)

    # LCL term (low LCL favors tornadoes)
    if lcl_m < 1000:
        lcl_term = 1
    elif lcl_m < 2000:
        lcl_term = (2000 - lcl_m) / 1000
    else:
        lcl_term = 0

    # CIN term (less cap is better)
    cin = abs(cin)
    if cin < 50:
        cin_term = 1
    elif cin < 200:
        cin_term = (200 - cin) / 150
    else:
        cin_term = 0

    return cape_term * srh_term * shear_term * lcl_term * cin_term

def supercell_composite_parameter(mucape, srh, shear_ms):
    """
    Calculate Supercell Composite Parameter.
    """
    cape_term = mucape / 1000
    srh_term = srh / 50
    shear_term = shear_ms / 20

    return cape_term * srh_term * shear_term

def stp_category(stp):
    """Categorize STP."""
    if stp < 1:
        return "Below threshold"
    elif stp < 2:
        return "Sig tornado possible"
    elif stp < 5:
        return "Sig tornado likely"
    else:
        return "Violent tornado possible"

print("\nSignificant Tornado Parameter examples:")
print("-" * 70)
print(f"{'CAPE':>6s}  {'SRH':>5s}  {'Shear':>6s}  {'LCL':>5s}  {'CIN':>4s}  {'STP':>6s}  {'Assessment':>22s}")
print("-" * 70)

test_cases = [
    (1000, 100, 15, 1500, 50),
    (2000, 200, 20, 1000, 25),
    (2500, 250, 25, 800, 50),
    (3000, 300, 25, 700, 25),
    (4000, 400, 30, 500, 0),
]

for cape, srh, shear, lcl, cin in test_cases:
    stp = significant_tornado_parameter(cape, srh, shear, lcl, cin)
    cat = stp_category(stp)
    print(f"{cape:>6.0f}  {srh:>5.0f}  {shear:>6.0f}  {lcl:>5.0f}  {cin:>4.0f}  {stp:>6.1f}  {cat:>22s}")

#############################################
# PART 5: STABILITY INDICES
#############################################
print("\n" + "="*70)
print("PART 5: TRADITIONAL STABILITY INDICES")
print("="*70)

print("""
LIFTED INDEX (LI):
=================

    LI = T_env(500 hPa) - T_parcel(500 hPa)

Parcel lifted from surface (or mixed layer).

LI THRESHOLDS:
    > 0: Stable
    0 to -2: Marginally unstable
    -2 to -4: Moderately unstable
    -4 to -6: Very unstable
    < -6: Extremely unstable

K-INDEX:
========

    K = T_850 - T_500 + Td_850 - (T_700 - Td_700)

Combines temperature lapse rate and moisture.

K-INDEX THRESHOLDS:
    < 20: No thunderstorms
    20-25: Isolated thunderstorms
    25-30: Scattered thunderstorms
    30-35: Numerous thunderstorms
    > 35: Widespread thunderstorms

TOTAL TOTALS (TT):
=================

    TT = (T_850 - T_500) + (Td_850 - T_500)
       = VT + CT

Where:
    VT = Vertical Totals = T_850 - T_500
    CT = Cross Totals = Td_850 - T_500

TT THRESHOLDS:
    < 44: No significant convection
    44-50: Thunderstorms possible
    50-55: Severe storms possible
    > 55: Severe storms likely
""")

def lifted_index(T_env_500, T_parcel_500):
    """Calculate Lifted Index."""
    return T_env_500 - T_parcel_500

def k_index(T_850, T_700, T_500, Td_850, Td_700):
    """Calculate K-Index."""
    return (T_850 - T_500) + Td_850 - (T_700 - Td_700)

def total_totals(T_850, T_500, Td_850):
    """Calculate Total Totals index."""
    VT = T_850 - T_500  # Vertical totals
    CT = Td_850 - T_500  # Cross totals
    return VT + CT

def li_category(li):
    """Categorize Lifted Index."""
    if li > 0:
        return "Stable"
    elif li > -2:
        return "Marginally unstable"
    elif li > -4:
        return "Moderately unstable"
    elif li > -6:
        return "Very unstable"
    else:
        return "Extremely unstable"

def k_category(k):
    """Categorize K-Index."""
    if k < 20:
        return "No thunderstorms"
    elif k < 25:
        return "Isolated storms"
    elif k < 30:
        return "Scattered storms"
    elif k < 35:
        return "Numerous storms"
    else:
        return "Widespread storms"

print("\nLifted Index interpretation:")
print("-" * 45)
for li in [2, 0, -2, -4, -6, -8, -10]:
    cat = li_category(li)
    print(f"  LI = {li:+3.0f}: {cat}")

print("\nK-Index interpretation:")
print("-" * 45)
for k in [15, 20, 25, 30, 35, 40]:
    cat = k_category(k)
    print(f"  K = {k:2.0f}: {cat}")

print("\nTotal Totals example calculations:")
print("-" * 55)
print(f"{'T_850':>8s}  {'T_500':>8s}  {'Td_850':>8s}  {'TT':>6s}  {'Interpretation':>18s}")
print("-" * 55)
cases = [
    (15, -10, 10, "Marginal"),
    (18, -12, 14, "Storms possible"),
    (20, -15, 16, "Severe possible"),
    (22, -18, 18, "Severe likely"),
]
for t850, t500, td850, interp in cases:
    tt = total_totals(t850, t500, td850)
    print(f"{t850:>8.0f}  {t500:>8.0f}  {td850:>8.0f}  {tt:>6.0f}  {interp:>18s}")

#############################################
# PART 6: MOISTURE PARAMETERS
#############################################
print("\n" + "="*70)
print("PART 6: MOISTURE PARAMETERS")
print("="*70)

print("""
PRECIPITABLE WATER (PW):
=======================

Total column water vapor:

    PW = (1/g) ∫[sfc to top] q dp

Where q = specific humidity.

PW THRESHOLDS (varies by climate):
    Tropical: 50-75 mm common
    Midlatitude summer: 25-50 mm
    Midlatitude winter: 10-25 mm

High PW + high CAPE = flash flood risk

RELATIVE HUMIDITY PROFILES:
==========================

Critical levels:
    Low-level (850-700 hPa): Inflow layer moisture
    Mid-level (700-500 hPa): Entrainment

Dry mid-levels (RH < 40%) + moist low-levels:
    → Strong evaporative cooling
    → Enhanced downdrafts
    → Microburst potential

DEWPOINT DEPRESSION:
    T - Td > 15°C at mid-levels → inverted-V sounding
    → Strong downdrafts, damaging winds

LCL (LIFTED CONDENSATION LEVEL):
================================

    LCL_height ≈ 125 × (T - Td)  [meters]

Low LCL (< 1000 m): Tornado-favorable
High LCL (> 2000 m): Less tornado risk, more large hail
""")

def precipitable_water(q_profile, p_profile):
    """
    Calculate precipitable water.

    PW = (1/g) ∫ q dp
    """
    pw = 0
    for i in range(len(p_profile) - 1):
        q_avg = 0.5 * (q_profile[i] + q_profile[i+1])
        dp = abs(p_profile[i] - p_profile[i+1])
        pw += q_avg * dp / g

    return pw * 1000  # Convert to mm

def lcl_height(T_C, Td_C):
    """
    Estimate LCL height using simple formula.

    LCL ≈ 125 × (T - Td) meters
    """
    return 125 * (T_C - Td_C)

def lcl_tornado_assessment(lcl_m):
    """Assess tornado potential based on LCL."""
    if lcl_m < 800:
        return "Very favorable for tornadoes"
    elif lcl_m < 1200:
        return "Favorable for tornadoes"
    elif lcl_m < 1500:
        return "Marginal for tornadoes"
    elif lcl_m < 2000:
        return "Hail more likely than tornado"
    else:
        return "Tornado unlikely"

def microburst_potential(pw_mm, dcape, mid_level_rh):
    """
    Assess microburst potential.

    High DCAPE + dry mid-levels = high risk
    """
    if dcape < 500 or mid_level_rh > 60:
        return "Low"
    elif dcape < 1000:
        return "Moderate"
    elif dcape < 1500 and mid_level_rh < 40:
        return "High"
    else:
        return "Extreme"

print("\nLCL height and tornado potential:")
print("-" * 60)
print(f"{'T (°C)':>8s}  {'Td (°C)':>8s}  {'LCL (m)':>10s}  {'Assessment':>28s}")
print("-" * 60)
for T, Td in [(25, 22), (28, 20), (30, 18), (32, 16), (35, 12)]:
    lcl = lcl_height(T, Td)
    assess = lcl_tornado_assessment(lcl)
    print(f"{T:>8.0f}  {Td:>8.0f}  {lcl:>10.0f}  {assess:>28s}")

print("\nMicroburst potential assessment:")
print("-" * 55)
print(f"{'DCAPE':>8s}  {'Mid RH':>8s}  {'Potential':>12s}")
print("-" * 55)
for dcape in [500, 1000, 1500]:
    for rh in [30, 50, 70]:
        pot = microburst_potential(25, dcape, rh)
        print(f"{dcape:>8.0f}  {rh:>8.0f}%  {pot:>12s}")

#############################################
# PART 7: FORECASTER'S DECISION MATRIX
#############################################
print("\n" + "="*70)
print("PART 7: SEVERE WEATHER DECISION SUPPORT")
print("="*70)

print("""
HAZARD ASSESSMENT MATRIX:
========================

TORNADO:
    Required: CAPE > 500, SRH > 100, 0-1km shear > 20kt
    Favorable: Low LCL < 1000m, STP > 1, backed surface winds

SUPERCELL:
    Required: CAPE > 1000, 0-6km shear > 35kt
    Favorable: SCP > 1, curved hodograph, storm-relative inflow

LARGE HAIL (≥1"):
    Required: CAPE > 1000, strong updraft
    Favorable: High freezing level, strong shear, mid-level dry

DAMAGING WINDS:
    Required: CAPE present, organized convection
    Favorable: High DCAPE, dry mid-levels, strong 0-3km shear

FLASH FLOOD:
    Required: Training echoes or slow-moving storms
    Favorable: High PW, weak steering flow, upslope/terrain focus

PATTERN RECOGNITION:
    Inverted-V: Strong downdrafts, microbursts
    Loaded gun: Extreme instability, cap, explosive potential
    Classic supercell: Strong shear, curved hodograph
    HP supercell: Moist environment, heavy rain, embedded tornado
""")

def severe_weather_threats(cape, cin, srh_1km, srh_3km, shear_06km,
                           lcl, dcape, pw, mid_rh):
    """
    Comprehensive threat assessment.
    """
    threats = []

    # Tornado threat
    if cape > 500 and srh_1km > 100 and lcl < 1500:
        if srh_1km > 200 and lcl < 1000:
            threats.append("TORNADO - HIGH")
        else:
            threats.append("TORNADO - MODERATE")

    # Supercell threat
    if cape > 1000 and shear_06km > 18:
        if shear_06km > 25:
            threats.append("SUPERCELL - LIKELY")
        else:
            threats.append("SUPERCELL - POSSIBLE")

    # Hail threat
    if cape > 1500 and shear_06km > 15:
        threats.append("LARGE HAIL - POSSIBLE")

    # Wind threat
    if dcape > 800 or (cape > 1000 and mid_rh < 50):
        threats.append("DAMAGING WIND - POSSIBLE")

    # Flash flood
    if pw > 40 and cape > 500:
        threats.append("FLASH FLOOD - POSSIBLE")

    if not threats:
        threats.append("GENERAL THUNDERSTORMS")

    return threats

print("\nSample threat assessment:")
print("-" * 70)

# High-end tornado scenario
threats = severe_weather_threats(
    cape=3000, cin=25, srh_1km=250, srh_3km=350, shear_06km=25,
    lcl=700, dcape=800, pw=45, mid_rh=50
)
print("Scenario 1 (Tornado outbreak environment):")
for t in threats:
    print(f"  → {t}")

# Hail/wind scenario
threats = severe_weather_threats(
    cape=2500, cin=50, srh_1km=75, srh_3km=150, shear_06km=30,
    lcl=1800, dcape=1200, pw=30, mid_rh=35
)
print("\nScenario 2 (Hail and wind environment):")
for t in threats:
    print(f"  → {t}")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("SEVERE WEATHER INDICES SUMMARY")
print("="*70)
print("""
Key Parameters:

1. CAPE:
   - Integrated buoyancy energy
   - w_max = √(2×CAPE)
   - >2500 J/kg = extremely unstable

2. CIN:
   - Energy barrier to convection
   - <50 J/kg = weak cap
   - Requires trigger to overcome

3. WIND SHEAR:
   - 0-6 km > 40 kt for supercells
   - Directional shear → rotation

4. SRH:
   - Measures rotation potential
   - 0-1 km > 200 m²/s² → significant tornado

5. COMPOSITE INDICES:
   - STP > 1: Significant tornado possible
   - SCP > 1: Supercell possible
   - Combine multiple parameters

6. STABILITY INDICES:
   - LI < -4: Very unstable
   - K > 30: Numerous storms
   - TT > 50: Severe possible

7. MOISTURE:
   - Low LCL (<1000m): Tornado favorable
   - High PW + slow storms: Flash flood
   - Dry mid-levels: Strong downdrafts

These indices provide quantitative guidance for
severe weather forecasting and warning decisions!
""")

if __name__ == "__main__":
    print("\n[Severe Weather Indices Module - Complete]")
