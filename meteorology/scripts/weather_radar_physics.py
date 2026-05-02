#!/usr/bin/env python3
"""
WEATHER RADAR PHYSICS - FIRST PRINCIPLES
=========================================

Deriving radar meteorology from electromagnetic theory:
backscatter, Doppler, dual-polarization, and signal processing.
"""

import numpy as np

print("=" * 70)
print("WEATHER RADAR PHYSICS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
c = 3e8             # Speed of light (m/s)
pi = np.pi


# =============================================================================
# PART 1: ELECTROMAGNETIC FOUNDATIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: ELECTROMAGNETIC FOUNDATIONS")
print("=" * 70)

em_text = """
RADAR = RAdio Detection And Ranging

BASIC PRINCIPLE:
1. Transmit pulse of EM radiation
2. Radiation interacts with targets
3. Scattered radiation returns to antenna
4. Measure time delay → distance
5. Measure power → target properties

WEATHER RADAR FREQUENCIES:

Band    Frequency    Wavelength    Use
─────────────────────────────────────────────────
S       2.7-3.0 GHz  10-11 cm      Long range (NWS)
C       5.3-5.7 GHz  5.3-5.6 cm    Medium range
X       9.3-9.5 GHz  3.0-3.2 cm    Short range, mobile
K       24-40 GHz    0.75-1.25 cm  Cloud radar

WHY THESE FREQUENCIES?

RAYLEIGH SCATTERING (D << λ):

For particles much smaller than wavelength:
σ_b ∝ D⁶ / λ⁴

Key insight:
- Sensitivity increases with smaller λ
- But attenuation ALSO increases with smaller λ
- S-band: Low attenuation, penetrates rain
- X-band: High resolution, but rain attenuates

THE TRADEOFF:
Longer wavelength → less attenuation, less sensitivity
Shorter wavelength → more sensitivity, more attenuation

NWS NEXRAD (WSR-88D):
- S-band (10 cm)
- Power: 750 kW peak
- Range: 460 km (reflectivity), 230 km (Doppler)
- Resolution: 1° × 250 m
"""
print(em_text)

def wavelength_to_frequency(wavelength_m):
    """Convert wavelength to frequency."""
    return c / wavelength_m

def frequency_to_wavelength(frequency_hz):
    """Convert frequency to wavelength."""
    return c / frequency_hz

print("\nRadar Frequency Bands:")
print("-" * 60)
print(f"{'Band':<8} {'Wavelength (cm)':<18} {'Frequency (GHz)'}")
print("-" * 60)

bands = [
    ("S", 0.10),
    ("C", 0.055),
    ("X", 0.032),
    ("Ka", 0.008),
]

for band, wl in bands:
    freq = wavelength_to_frequency(wl) / 1e9
    print(f"{band:<8} {wl*100:<18.1f} {freq:<.1f}")


# =============================================================================
# PART 2: RADAR EQUATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: THE RADAR EQUATION")
print("=" * 70)

radar_eq_text = """
RADAR EQUATION:
===============

The fundamental equation relating received power to target properties.

TRANSMITTED POWER:

Power density at range r:
S = P_t × G / (4πr²)

Where:
- P_t = transmitted power
- G = antenna gain

BACKSCATTERED POWER:

From target with cross-section σ:
Power intercepted and scattered

RECEIVED POWER:

P_r = (P_t × G² × λ² × σ) / ((4π)³ × r⁴)

This is the RADAR EQUATION!

Key dependencies:
- P_r ∝ 1/r⁴ (inverse fourth power!)
- P_r ∝ σ (target cross-section)
- P_r ∝ λ² (wavelength squared)

RANGE RESOLUTION:

Δr = c × τ / 2

Where τ = pulse duration

Example: τ = 1 μs → Δr = 150 m

WHY 1/r⁴?

Power goes out: 1/r²
Power comes back: another 1/r²
Total: 1/r⁴

A target at 200 km returns 16× LESS power than at 100 km!
"""
print(radar_eq_text)

def radar_received_power(P_t, G, wavelength, sigma, r):
    """
    Calculate received power from radar equation.

    P_t: Transmitted power (W)
    G: Antenna gain (linear)
    wavelength: Wavelength (m)
    sigma: Radar cross section (m²)
    r: Range (m)
    """
    P_r = (P_t * G**2 * wavelength**2 * sigma) / ((4*pi)**3 * r**4)
    return P_r

def range_resolution(pulse_duration_s):
    """Calculate range resolution from pulse duration."""
    return c * pulse_duration_s / 2

print("\nRange Dependence of Received Power:")
print("-" * 50)
print(f"{'Range (km)':<15} {'Relative power':<20} {'dB down'}")
print("-" * 50)

P_ref = 1  # Reference at 50 km
for r in [50, 75, 100, 150, 200, 300, 400]:
    P_rel = (50/r)**4
    dB = 10 * np.log10(P_rel)
    print(f"{r:<15} {P_rel:<20.4f} {dB:.1f}")


# =============================================================================
# PART 3: REFLECTIVITY AND RAIN RATE
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: REFLECTIVITY (Z) AND THE Z-R RELATIONSHIP")
print("=" * 70)

reflectivity_text = """
REFLECTIVITY (Z):
=================

For precipitation: many small targets
Need to sum over all particles in volume

RADAR REFLECTIVITY FACTOR:

Z = Σ D_i⁶  (sum over all drops)

Units: mm⁶/m³

For drop size distribution n(D):
Z = ∫ n(D) × D⁶ dD

THE RAYLEIGH APPROXIMATION:

When D << λ (most rain at S-band):
Backscatter cross-section σ_b = (π⁵/λ⁴) × |K|² × D⁶

Where |K|² ≈ 0.93 for water, 0.18 for ice

This gives the Z DEPENDENCE!

dBZ SCALE:

dBZ = 10 × log₁₀(Z / Z_ref)

Where Z_ref = 1 mm⁶/m³

Typical values:
- Light rain: 20 dBZ
- Moderate rain: 35 dBZ
- Heavy rain: 50 dBZ
- Severe storm: 55+ dBZ
- Giant hail: 70+ dBZ

Z-R RELATIONSHIP:

Z = a × R^b

Standard Marshall-Palmer:
Z = 200 × R^1.6

R = rain rate in mm/hr
Z in mm⁶/m³

PROBLEMS:
- Different relationships for different rain types
- Tropical: Z = 250R^1.2
- Snow: Z = 2000R^2.0
- Hail can't use Z-R at all!
"""
print(reflectivity_text)

def dbz_to_z(dbz):
    """Convert dBZ to linear Z (mm⁶/m³)."""
    return 10**(dbz / 10)

def z_to_dbz(z):
    """Convert linear Z to dBZ."""
    return 10 * np.log10(z)

def z_to_rainrate(z, a=200, b=1.6):
    """
    Convert Z to rain rate using Z = aR^b.

    Returns R in mm/hr
    """
    R = (z / a)**(1/b)
    return R

def rainrate_to_z(R, a=200, b=1.6):
    """Convert rain rate (mm/hr) to Z."""
    return a * R**b

print("\nReflectivity to Rain Rate Conversion:")
print("-" * 65)
print(f"{'dBZ':<10} {'Z (mm⁶/m³)':<18} {'Rain rate (mm/hr)':<20} {'Intensity'}")
print("-" * 65)

dbz_values = [0, 15, 25, 35, 45, 55, 65, 75]
intensities = ["None", "Trace", "Light", "Moderate", "Heavy", "Very heavy", "Extreme", "Hail likely"]

for dbz, intensity in zip(dbz_values, intensities):
    z = dbz_to_z(dbz)
    R = z_to_rainrate(z)
    print(f"{dbz:<10} {z:<18.1f} {R:<20.1f} {intensity}")


# =============================================================================
# PART 4: DOPPLER RADAR
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: DOPPLER RADAR")
print("=" * 70)

doppler_text = """
DOPPLER EFFECT:
===============

Moving target shifts frequency of returned signal

DOPPLER SHIFT:

f_d = 2 × v_r × f / c = 2 × v_r / λ

Where:
- f_d = Doppler frequency shift
- v_r = radial velocity (toward/away from radar)
- f = transmitted frequency
- λ = wavelength

For S-band (λ = 10 cm), v_r = 30 m/s:
f_d = 2 × 30 / 0.10 = 600 Hz

PHASE MEASUREMENT:

Change in phase between pulses:
Δφ = 2π × f_d × T_s = 4π × v_r × T_s / λ

Where T_s = pulse repetition time

NYQUIST VELOCITY (Maximum Unambiguous):

v_max = λ × PRF / 4 = λ / (4 × T_s)

Example: λ = 10 cm, PRF = 1000 Hz
v_max = 0.10 × 1000 / 4 = 25 m/s

PROBLEM: Velocities > v_max are "aliased"!
50 m/s appears as -0 m/s (folds)

SOLUTIONS:
1. Dual PRF (different Nyquist limits)
2. Velocity dealiasing algorithms
3. Lower PRF (but reduces max range!)

DOPPLER SPECTRUM:

Within each resolution volume:
- Many particles at different velocities
- Spectrum width = spread in velocities
- Gives turbulence information!

Mean velocity: first moment of spectrum
Spectrum width: second moment

VELOCITY AZIMUTH DISPLAY (VAD):
Scan at constant elevation → wind profile
"""
print(doppler_text)

def doppler_shift(v_radial, wavelength):
    """Calculate Doppler frequency shift."""
    return 2 * v_radial / wavelength

def nyquist_velocity(wavelength, prf):
    """Calculate maximum unambiguous velocity."""
    return wavelength * prf / 4

def max_unambiguous_range(prf):
    """Calculate maximum unambiguous range."""
    return c / (2 * prf)

print("\nDoppler Velocity Limits:")
print("-" * 65)
print(f"{'Wavelength (cm)':<18} {'PRF (Hz)':<12} {'v_max (m/s)':<15} {'r_max (km)'}")
print("-" * 65)

for wl_cm in [10, 5.5, 3.2]:
    wl = wl_cm / 100
    for prf in [500, 1000, 1500, 2000]:
        v_max = nyquist_velocity(wl, prf)
        r_max = max_unambiguous_range(prf) / 1000
        print(f"{wl_cm:<18} {prf:<12} {v_max:<15.0f} {r_max:<.0f}")


# =============================================================================
# PART 5: DUAL-POLARIZATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: DUAL-POLARIZATION RADAR")
print("=" * 70)

dualpol_text = """
DUAL-POLARIZATION:
==================

Transmit and receive BOTH horizontal (H) and vertical (V) polarizations

WHY? Particles have SHAPE, not just size!

- Raindrops: oblate (flattened) when large
- Hail: tumbling, various shapes
- Ice crystals: oriented, thin plates
- Snow: irregular aggregates

POLARIMETRIC VARIABLES:

1. Z_H (Horizontal reflectivity)
   - Standard reflectivity
   - Same as single-pol Z

2. Z_DR (Differential reflectivity)
   Z_DR = 10 × log₁₀(Z_H / Z_V)

   - Positive: oblate (rain)
   - Near zero: spherical (small drops, tumbling hail)
   - Negative: prolate (rare)

   Large rain: Z_DR = 2-5 dB
   Small rain: Z_DR = 0-1 dB
   Hail: Z_DR ≈ 0 dB (tumbling)

3. ρ_HV (Correlation coefficient)
   Correlation between H and V returns

   ρ_HV > 0.98: Pure rain
   ρ_HV = 0.95-0.98: Mixed phase
   ρ_HV < 0.95: Non-meteorological (birds, debris)
   ρ_HV < 0.90: Tornado debris signature!

4. K_DP (Specific differential phase)
   Phase difference accumulation per km

   K_DP > 0: Oblate particles (heavy rain)
   Insensitive to hail!
   Best for heavy rain estimation

5. LDR (Linear depolarization ratio)
   Backscatter in opposite polarization
   Sensitive to particle wobble/tumble

HYDROMETEOR CLASSIFICATION:

Use decision tree or fuzzy logic with all variables:
- Light rain
- Heavy rain
- Hail
- Dry snow
- Wet snow
- Ice crystals
- Graupel
- Biological (birds, insects)
- Ground clutter
"""
print(dualpol_text)

def differential_reflectivity(D_eq_mm, axis_ratio):
    """
    Simplified Z_DR calculation.

    D_eq_mm: Equivalent spherical diameter (mm)
    axis_ratio: b/a where b=vertical, a=horizontal
    """
    # For oblate spheroid, Z_DR depends on axis ratio
    # Z_H/Z_V ≈ (a/b)^n where n ≈ 4-6
    if axis_ratio == 1:
        return 0

    zdr_ratio = (1/axis_ratio)**5
    Z_DR = 10 * np.log10(zdr_ratio)
    return Z_DR

def raindrop_axis_ratio(D_mm):
    """
    Axis ratio of raindrop as function of diameter.

    Empirical fit (Pruppacher & Beard, 1970)
    """
    if D_mm <= 1:
        return 1.0
    else:
        # Axis ratio decreases (more oblate) with size
        return 1.03 - 0.062 * D_mm

print("\nRaindrop Shape and Z_DR:")
print("-" * 55)
print(f"{'Diameter (mm)':<18} {'Axis ratio':<15} {'Z_DR (dB)'}")
print("-" * 55)

for D in [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]:
    ar = raindrop_axis_ratio(D)
    zdr = differential_reflectivity(D, ar)
    print(f"{D:<18} {ar:<15.2f} {zdr:<.1f}")

print("\n\nHydrometeor Classification Signatures:")
print("-" * 70)
print(f"{'Type':<20} {'Z_H (dBZ)':<15} {'Z_DR (dB)':<12} {'ρ_HV':<10} {'K_DP'}")
print("-" * 70)

hydrometeors = [
    ("Light rain", "20-35", "0-1", ">0.99", "0-1"),
    ("Heavy rain", "45-55", "2-4", ">0.98", "2-6"),
    ("Large hail", "55-75", "-0.5 to 1", "0.90-0.98", "~0"),
    ("Dry snow", "15-30", "0-1", ">0.98", "~0"),
    ("Wet snow", "30-45", "1-3", "0.85-0.95", "0-2"),
    ("Graupel", "35-50", "-0.5 to 1", "0.95-0.99", "~0"),
    ("Tornado debris", "Variable", "Variable", "<0.80", "Variable"),
]

for htype, zh, zdr, rhv, kdp in hydrometeors:
    print(f"{htype:<20} {zh:<15} {zdr:<12} {rhv:<10} {kdp}")


# =============================================================================
# PART 6: RADAR SIGNATURES
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: IMPORTANT RADAR SIGNATURES")
print("=" * 70)

signatures_text = """
SEVERE WEATHER SIGNATURES:
==========================

1. HOOK ECHO
   - Hook-shaped reflectivity
   - Indicates rotating updraft wrapping precip
   - Associated with mesocyclone/tornado

2. MESOCYCLONE (Doppler)
   - Couplet: approaching/receding velocities
   - Azimuthal shear > 10⁻² s⁻¹
   - Vertical extent > 3 km
   - Duration > 10 minutes

3. TORNADO VORTEX SIGNATURE (TVS)
   - Very tight velocity couplet
   - ΔV > 40 m/s across ~ 1 km
   - Gate-to-gate shear

4. BOUNDED WEAK ECHO REGION (BWER)
   - Notch of weak echo in strong storm
   - Indicates powerful updraft
   - Precursor to hail

5. THREE-BODY SCATTER SPIKE (TBSS)
   - Linear echo extending downrange from hail core
   - Caused by radar pulse scattering:
     hail → ground → hail → radar
   - Indicates large hail

6. ZDR ARC / ZDR COLUMN
   - Arc: Size sorting at storm edge
   - Column: Large drops lofted by updraft
   - Updraft strength indicator

7. VELOCITY COUPLET (Bow Echo)
   - Rear-inflow jet signature
   - Bookend vortices

8. TORNADO DEBRIS SIGNATURE (TDS)
   - Low ρ_HV (< 0.85)
   - High Z_H
   - Collocated with rotation
   - Confirms debris lofted by tornado!
"""
print(signatures_text)

def mesocyclone_criteria(delta_v, diameter_km, vertical_extent_km):
    """
    Check if velocity couplet meets mesocyclone criteria.
    """
    # Azimuthal shear
    shear = delta_v / (diameter_km * 1000)  # s⁻¹

    criteria = {
        'shear_met': shear > 1e-3,
        'diameter_met': 2 < diameter_km < 10,
        'depth_met': vertical_extent_km > 3,
    }

    is_mesocyclone = all(criteria.values())
    return shear, is_mesocyclone, criteria

print("\nMesocyclone Detection:")
print("-" * 65)
print(f"{'ΔV (m/s)':<12} {'Diameter (km)':<15} {'Shear (s⁻¹)':<15} {'Mesocyclone?'}")
print("-" * 65)

for dv in [20, 30, 40, 50]:
    for diam in [2, 4, 6]:
        shear, is_meso, _ = mesocyclone_criteria(dv, diam, 5)
        status = "Yes" if is_meso else "No"
        print(f"{dv:<12} {diam:<15} {shear:<15.4f} {status}")


# =============================================================================
# PART 7: ATTENUATION AND BEAM EFFECTS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: ATTENUATION AND BEAM EFFECTS")
print("=" * 70)

attenuation_text = """
ATTENUATION:
============

Radar beam loses power passing through precipitation

Two-way attenuation (out and back):
A = 2 × ∫ α(r) dr  (dB)

Where α = attenuation coefficient (dB/km)

ATTENUATION COEFFICIENTS (S-band):

Rain rate (mm/hr)    α (dB/km)
─────────────────────────────────
1                    ~0.001
10                   ~0.01
50                   ~0.1
100                  ~0.3

At S-band: Attenuation usually negligible!

At X-band: 10× higher, significant in heavy rain
At C-band: 5× higher, moderate effect

MITIGATION:
- Use K_DP (differential phase) - unaffected by attenuation!
- Attenuation correction algorithms
- Network of overlapping radars

BEAM EFFECTS:

1. BEAM BROADENING
   At range r, beamwidth θ:
   Resolution = r × θ (radians)

   At 100 km, 1° beam: 1.7 km width!

2. BEAM HEIGHT
   Due to Earth curvature and refraction:
   h = r² / (2 × 4/3 × R_earth) + r × sin(θ_elev)

   Low elevation (0.5°) at 150 km: beam center ~2 km AGL!
   Can overshoot shallow precipitation

3. PARTIAL BEAM FILLING
   When only part of beam contains precipitation
   → Reflectivity underestimated

4. GROUND CLUTTER
   Beam hits terrain
   → Strong false echoes near radar
   Solution: Doppler filtering (clutter is zero velocity)
"""
print(attenuation_text)

def beam_height(range_km, elevation_deg, radar_height_m=0):
    """
    Calculate beam center height AGL.

    Includes Earth curvature and 4/3 refraction.
    """
    r = range_km * 1000
    theta = np.radians(elevation_deg)
    R_e = 6.371e6  # Earth radius
    k_e = 4/3  # Standard refraction

    # Height formula
    h = r * np.sin(theta) + r**2 / (2 * k_e * R_e) + radar_height_m
    return h / 1000  # Return km

def beam_width_at_range(range_km, beamwidth_deg=1):
    """Calculate beam width at given range."""
    return range_km * np.radians(beamwidth_deg)

print("\nBeam Height vs Range (standard refraction):")
print("-" * 60)
print(f"{'Range (km)':<15} {'0.5°':<12} {'1.0°':<12} {'2.5°':<12} {'4.0° (km)'}")
print("-" * 60)

for r in [25, 50, 100, 150, 200, 250, 300]:
    h05 = beam_height(r, 0.5)
    h10 = beam_height(r, 1.0)
    h25 = beam_height(r, 2.5)
    h40 = beam_height(r, 4.0)
    print(f"{r:<15} {h05:<12.1f} {h10:<12.1f} {h25:<12.1f} {h40:.1f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: WEATHER RADAR PHYSICS")
print("=" * 70)

summary = """
KEY RADAR PHYSICS:
=================

1. ELECTROMAGNETIC SCATTERING
   - Rayleigh scattering: σ ∝ D⁶/λ⁴
   - Longer wavelength → less attenuation, less sensitivity
   - S-band optimal for precipitation

2. RADAR EQUATION
   - P_r ∝ σ/r⁴
   - 1/r⁴ range dependence (out AND back)
   - Sensitivity crucial for distant targets

3. REFLECTIVITY (Z)
   - Z = Σ D⁶ (sum of sixth power of diameters)
   - Units: dBZ = 10 log₁₀(Z)
   - Z-R relationship: Z = 200 R^1.6

4. DOPPLER
   - f_d = 2 v_r / λ
   - Nyquist limit: v_max = λ PRF / 4
   - Tradeoff: velocity range vs distance range

5. DUAL-POLARIZATION
   - Z_DR: Shape information (oblate drops)
   - ρ_HV: Uniformity (debris detection!)
   - K_DP: Phase, immune to attenuation
   - Hydrometeor classification

6. SEVERE WEATHER SIGNATURES
   - Hook echo: Rotation
   - Mesocyclone: Velocity couplet
   - BWER: Strong updraft
   - TDS: Tornado debris (low ρ_HV)

7. LIMITATIONS
   - Beam height increases with range
   - Attenuation (worse at shorter wavelength)
   - Partial beam filling


THE PHYSICS TELLS US:
====================
- Radar probes precipitation SIZE distribution (D⁶ weighting)
- Doppler gives motion toward/away from radar only
- Dual-pol adds shape information → better classification
- Multiple radars needed to fill gaps
- Understanding physics essential for interpretation!
"""
print(summary)

print("\n" + "=" * 70)
print("END OF WEATHER RADAR PHYSICS")
print("=" * 70)
