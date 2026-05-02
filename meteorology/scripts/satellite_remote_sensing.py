#!/usr/bin/env python3
"""
SATELLITE REMOTE SENSING - FIRST PRINCIPLES
=============================================

Deriving satellite meteorology from radiative transfer:
infrared, microwave, visible imaging, and retrievals.
"""

import numpy as np

print("=" * 70)
print("SATELLITE REMOTE SENSING - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
h = 6.626e-34      # Planck constant (J·s)
c = 3e8            # Speed of light (m/s)
k_B = 1.381e-23    # Boltzmann constant (J/K)
sigma = 5.67e-8    # Stefan-Boltzmann constant (W/m²/K⁴)


# =============================================================================
# PART 1: PLANCK FUNCTION AND BLACKBODY RADIATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: BLACKBODY RADIATION")
print("=" * 70)

blackbody_text = """
PLANCK FUNCTION:
================

Spectral radiance of blackbody at temperature T:

B_λ(T) = (2hc²/λ⁵) × 1/(exp(hc/λkT) - 1)

Units: W/m²/sr/m (radiance per wavelength)

Or in terms of frequency:

B_ν(T) = (2hν³/c²) × 1/(exp(hν/kT) - 1)

WIEN'S DISPLACEMENT LAW:

Peak wavelength:
λ_max × T = 2.898 × 10⁻³ m·K

Examples:
- Sun (5800 K): λ_max = 0.5 μm (visible)
- Earth (288 K): λ_max = 10 μm (thermal IR)
- Cloud tops (220 K): λ_max = 13 μm

STEFAN-BOLTZMANN LAW:

Total radiant power:
P = σ × T⁴

Integrate Planck function over all wavelengths

BRIGHTNESS TEMPERATURE:

Invert Planck function to get equivalent temperature:
T_B = (hc/λk) / ln(1 + 2hc²/(λ⁵ × B))

What temperature blackbody would emit observed radiance?
→ Key satellite measurement concept!
"""
print(blackbody_text)

def planck_wavelength(wavelength_m, temperature_K):
    """
    Planck function in wavelength form.

    Returns spectral radiance in W/m²/sr/m
    """
    x = (h * c) / (wavelength_m * k_B * temperature_K)
    B = (2 * h * c**2 / wavelength_m**5) / (np.exp(x) - 1)
    return B

def wien_peak(temperature_K):
    """Calculate peak wavelength from Wien's law."""
    return 2.898e-3 / temperature_K

def brightness_temperature(wavelength_m, radiance):
    """
    Invert Planck function to get brightness temperature.
    """
    coeff = (2 * h * c**2) / wavelength_m**5
    x = coeff / radiance + 1
    T_B = (h * c) / (wavelength_m * k_B * np.log(x))
    return T_B

def stefan_boltzmann_power(temperature_K):
    """Total radiant power from Stefan-Boltzmann."""
    return sigma * temperature_K**4

print("\nWien's Peak Wavelength:")
print("-" * 50)
print(f"{'Temperature (K)':<18} {'Peak λ (μm)':<18} {'Region'}")
print("-" * 50)

temps = [(5800, "Solar"), (320, "Hot surface"), (288, "Earth avg"),
         (260, "Warm cloud"), (220, "Cold cloud"), (180, "Tropopause")]

for T, region in temps:
    lam = wien_peak(T) * 1e6  # Convert to μm
    print(f"{T:<18} {lam:<18.1f} {region}")


# =============================================================================
# PART 2: RADIATIVE TRANSFER EQUATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: RADIATIVE TRANSFER")
print("=" * 70)

rte_text = """
RADIATIVE TRANSFER EQUATION:
============================

How radiation propagates through atmosphere

BASIC FORM:

dI_λ/ds = -κ_λ × ρ × I_λ + κ_λ × ρ × B_λ(T)

Where:
- I_λ = radiance at wavelength λ
- κ_λ = mass absorption coefficient
- ρ = density
- s = path length
- B_λ(T) = Planck function at local temperature

TERMS:
- First term: ABSORPTION (removes radiation)
- Second term: EMISSION (adds radiation)

OPTICAL DEPTH:

τ_λ = ∫ κ_λ × ρ × ds

SOLUTION (plane-parallel, looking up):

I_λ(τ=0) = I_λ(τ_s) × exp(-τ_s) + ∫₀^τs B_λ(T(τ)) × exp(-τ) dτ

For satellite looking DOWN at surface:

I = B_s × T_s + ∫_{surface}^{TOA} B(T(z)) × (dT/dz) dz

= Surface contribution + Atmospheric contribution

WEIGHTING FUNCTIONS:

W(z) = dτ/dz × exp(-τ(z))

Peaks at altitude where most radiation reaching satellite originates

Different wavelengths → different weighting functions → temperature sounding!
"""
print(rte_text)

def optical_depth_simple(absorption_coeff, column_density):
    """
    Simple optical depth calculation.

    τ = κ × m
    Where m = column density (kg/m²)
    """
    return absorption_coeff * column_density

def transmission(optical_depth):
    """Transmission through atmosphere."""
    return np.exp(-optical_depth)

def weighting_function(z_km, z_peak_km=10, width_km=5):
    """
    Simple Gaussian weighting function.

    Peaks at z_peak with given width.
    """
    return np.exp(-((z_km - z_peak_km) / width_km)**2)

print("\nAtmospheric Transmission:")
print("-" * 50)
print(f"{'Optical depth τ':<18} {'Transmission':<15} {'Absorbed %'}")
print("-" * 50)

for tau in [0.01, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0]:
    trans = transmission(tau)
    absorbed = (1 - trans) * 100
    print(f"{tau:<18} {trans:<15.3f} {absorbed:.1f}")


# =============================================================================
# PART 3: ATMOSPHERIC WINDOWS AND ABSORBERS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: ATMOSPHERIC WINDOWS")
print("=" * 70)

windows_text = """
ATMOSPHERIC ABSORPTION SPECTRUM:
================================

Not all wavelengths reach surface or space!

MAJOR ABSORBERS:

1. WATER VAPOR (H₂O)
   - Strong absorption: 2.7, 6.3 μm (vibration-rotation)
   - 5-8 μm (water vapor band)
   - Microwave: 22 GHz, 183 GHz

2. CARBON DIOXIDE (CO₂)
   - 4.3 μm (strong)
   - 15 μm (primary IR absorption)

3. OZONE (O₃)
   - UV: < 0.3 μm (protects surface!)
   - 9.6 μm (thermal IR)

4. OXYGEN (O₂)
   - 60 GHz (microwave)
   - 0.76 μm (A-band, visible)

ATMOSPHERIC WINDOWS:

Wavelength        Window?     Use
─────────────────────────────────────────────
0.4-0.7 μm       CLEAR       Visible imaging
3.5-4.0 μm       Window      Night detection, fires
8.0-9.0 μm       Window      Surface temperature
10-12 μm         Window      Primary thermal IR
Microwave        CLEAR*      All-weather (penetrates clouds)
                 (*except rain at high freq)

SATELLITE CHANNELS:

GOES-16/17 ABI:
- 16 spectral bands
- Window channels for surface/cloud tops
- Absorption channels for water vapor, CO₂
- Visible for daytime imaging

SOUNDER CHANNELS:
Select wavelengths with different optical depths
→ Sample different atmospheric levels
→ Retrieve temperature/moisture profiles
"""
print(windows_text)

# Simplified absorption data for demonstration
absorption_bands = {
    "0.4-0.7 μm (visible)": 0.05,
    "2.7 μm (H₂O strong)": 5.0,
    "3.9 μm (window)": 0.1,
    "4.3 μm (CO₂ strong)": 10.0,
    "6.3 μm (H₂O)": 3.0,
    "8.5 μm (window)": 0.2,
    "9.6 μm (O₃)": 1.5,
    "10.5 μm (window)": 0.15,
    "15 μm (CO₂ strong)": 8.0,
}

print("\nAtmospheric Absorption by Wavelength:")
print("-" * 65)
print(f"{'Wavelength region':<25} {'Optical depth':<15} {'Type'}")
print("-" * 65)

for region, tau in absorption_bands.items():
    trans = transmission(tau)
    if tau < 0.3:
        window_type = "WINDOW"
    elif tau < 2:
        window_type = "Partial"
    else:
        window_type = "OPAQUE"
    print(f"{region:<25} {tau:<15.2f} {window_type}")


# =============================================================================
# PART 4: SATELLITE ORBITS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: SATELLITE ORBITS")
print("=" * 70)

orbits_text = """
SATELLITE ORBITS:
=================

KEPLER'S LAWS APPLIED:

Orbital period:
T = 2π × √(a³ / (G × M_Earth))

For circular orbit:
v = √(G × M_Earth / r)

GEOSTATIONARY ORBIT (GEO):

T = 24 hours (matches Earth rotation)
→ a = 42,164 km (35,786 km above surface)

Properties:
- Appears stationary from Earth
- Constant view of same region
- High temporal resolution (15 min or less)
- Limited latitude coverage (±60°)
- 36,000 km distance → lower spatial resolution

EXAMPLES: GOES-E/W, Meteosat, Himawari

POLAR / SUN-SYNCHRONOUS (LEO):

Altitude: 700-850 km
Inclination: ~98° (sun-synchronous)
Period: ~100 minutes (14 orbits/day)

Properties:
- Views entire Earth daily
- High spatial resolution
- Same local time each pass
- Better polar coverage

EXAMPLES: NOAA-20, JPSS, MetOp, Terra, Aqua

SUN-SYNCHRONOUS CONDITION:

Precession rate = 360°/year = 0.986°/day

Achieved by choosing correct inclination for altitude:

cos(i) ≈ -a^(7/2) / (constant)

At 700 km: i ≈ 98.2°
At 850 km: i ≈ 98.7°
"""
print(orbits_text)

def orbital_period(altitude_km):
    """Calculate orbital period for given altitude."""
    G = 6.674e-11
    M_earth = 5.972e24
    R_earth = 6.371e6

    a = R_earth + altitude_km * 1000
    T = 2 * np.pi * np.sqrt(a**3 / (G * M_earth))
    return T / 60  # Return minutes

def geostationary_altitude():
    """Calculate geostationary altitude."""
    G = 6.674e-11
    M_earth = 5.972e24
    T = 24 * 3600  # 24 hours in seconds

    a = ((G * M_earth * T**2) / (4 * np.pi**2))**(1/3)
    R_earth = 6.371e6
    return (a - R_earth) / 1000  # km

def orbital_velocity(altitude_km):
    """Calculate orbital velocity."""
    G = 6.674e-11
    M_earth = 5.972e24
    R_earth = 6.371e6

    r = R_earth + altitude_km * 1000
    v = np.sqrt(G * M_earth / r)
    return v / 1000  # km/s

print("\nSatellite Orbit Properties:")
print("-" * 65)
print(f"{'Altitude (km)':<18} {'Period (min)':<15} {'Velocity (km/s)':<18} {'Orbits/day'}")
print("-" * 65)

for alt in [400, 700, 850, 1400, 35786]:
    T = orbital_period(alt)
    v = orbital_velocity(alt)
    orbits_per_day = 24 * 60 / T
    print(f"{alt:<18} {T:<15.1f} {v:<18.1f} {orbits_per_day:.1f}")

print(f"\nGeostationary altitude: {geostationary_altitude():.0f} km")


# =============================================================================
# PART 5: TEMPERATURE SOUNDING
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: TEMPERATURE SOUNDING")
print("=" * 70)

sounding_text = """
TEMPERATURE PROFILE RETRIEVAL:
==============================

Use multiple channels with different absorption characteristics

CO₂ SOUNDING:

CO₂ well-mixed in atmosphere
Absorption varies with wavelength in 15 μm band
→ Different channels sense different levels

Channel     Peak sensitivity    What it measures
──────────────────────────────────────────────────
15.0 μm    Upper stratosphere   Stratospheric T
14.7 μm    Lower stratosphere   Tropopause region
14.4 μm    Upper troposphere    Jet stream level
14.0 μm    Mid troposphere      ~500 hPa
13.6 μm    Lower troposphere    ~850 hPa
13.3 μm    Surface              Surface T (clear sky)

WEIGHTING FUNCTION:

W(z) ∝ dτ/dz × exp(-τ)

Peaked function:
- At surface: dτ/dz large, but exp(-τ) ≈ 0
- At TOA: exp(-τ) ≈ 1, but dτ/dz small
- Peak: Where τ ≈ 1

RETRIEVAL ALGORITHM:

Forward model: T_B = F(T_profile)

Inverse problem: T_profile = F⁻¹(T_B measurements)

Methods:
1. Statistical (regression)
2. Physical (iterative)
3. Optimal estimation (Bayesian)

MICROWAVE ADVANTAGES:
- O₂ sounding (60 GHz): all-weather!
- Less affected by clouds
- Temperature profile even through clouds
"""
print(sounding_text)

def weighting_function_simple(p_hPa, p_peak_hPa=500, width=200):
    """
    Simplified weighting function vs pressure.

    Gaussian approximation centered at p_peak.
    """
    return np.exp(-((p_hPa - p_peak_hPa) / width)**2)

print("\nSounding Channel Weighting Functions:")
print("-" * 55)
print(f"{'Pressure (hPa)':<18} {'Surface ch':<12} {'Mid-trop':<12} {'Upper trop'}")
print("-" * 55)

for p in [1000, 850, 700, 500, 300, 200, 100, 50]:
    w_sfc = weighting_function_simple(p, 900, 150)
    w_mid = weighting_function_simple(p, 500, 200)
    w_upper = weighting_function_simple(p, 250, 150)
    print(f"{p:<18} {w_sfc:<12.2f} {w_mid:<12.2f} {w_upper:.2f}")


# =============================================================================
# PART 6: WATER VAPOR RETRIEVAL
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: WATER VAPOR SENSING")
print("=" * 70)

wv_text = """
WATER VAPOR RETRIEVAL:
======================

Water vapor is highly variable → harder than temperature!

IR WATER VAPOR CHANNELS:

6.2-6.9 μm (H₂O absorption band)

Different wavelengths sense different levels:
- 6.2 μm: Upper troposphere (300-500 hPa)
- 6.5 μm: Mid troposphere
- 6.9 μm: Lower troposphere

WHAT SATELLITES "SEE":

Upper-level WV channel:
- Bright (warm) = dry upper troposphere
- Dark (cold) = moist upper troposphere

Lower-level WV channel:
- More sensitive to lower moisture
- Cloud contamination issues

TOTAL PRECIPITABLE WATER (TPW):

From microwave (23.8 GHz H₂O line):

TPW = ∫ ρ_v dz  (kg/m² = mm)

Ocean background: easy (uniform emissivity)
Land background: harder (variable emissivity)

GOES/ABI WV Products:
- 3 water vapor bands (6.2, 6.9, 7.3 μm)
- Derived motion winds
- Moisture estimates

MICROWAVE WATER VAPOR:
- 22 GHz, 183 GHz lines
- Works through non-precipitating cloud
- Key for NWP data assimilation
"""
print(wv_text)

print("\nWater Vapor Channel Interpretation:")
print("-" * 65)
print("Brightness Temperature    Upper-level moisture    Weather pattern")
print("-" * 65)
interpretations = [
    ("< 210 K", "Very moist", "Tropical moisture, convection"),
    ("210-230 K", "Moist", "Jet stream moisture transport"),
    ("230-250 K", "Moderate", "Mid-latitude normal"),
    ("250-270 K", "Dry", "Subsidence, high pressure"),
    ("> 270 K", "Very dry", "Desert regions, extreme subsidence"),
]

for tb, moisture, pattern in interpretations:
    print(f"{tb:<20} {moisture:<20} {pattern}")


# =============================================================================
# PART 7: DERIVED PRODUCTS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: DERIVED PRODUCTS")
print("=" * 70)

products_text = """
SATELLITE-DERIVED PRODUCTS:
===========================

1. ATMOSPHERIC MOTION VECTORS (AMVs)
   - Track cloud/moisture features between images
   - Height assigned from IR brightness temperature
   - Key data for NWP, especially over oceans!

2. SEA SURFACE TEMPERATURE (SST)
   - IR window channels (10-12 μm)
   - Atmospheric correction needed
   - Cloud-free pixels only
   - Microwave: through clouds!

3. CLOUD PRODUCTS
   - Cloud mask (clear/cloudy)
   - Cloud top height/pressure
   - Cloud phase (water/ice)
   - Optical depth

4. PRECIPITATION
   - IR: Cold cloud = likely rain (indirect)
   - Microwave: Emission/scattering from precip
   - Combined: GPM (Global Precipitation Mission)

5. VEGETATION/LAND
   - NDVI (Normalized Difference Vegetation Index)
   - NDVI = (NIR - Red) / (NIR + Red)
   - Soil moisture (microwave)

6. ATMOSPHERIC COMPOSITION
   - Total column ozone
   - Aerosol optical depth
   - Trace gases (CO, SO₂, NO₂)

7. RADIATION BUDGET
   - Reflected shortwave (albedo)
   - Outgoing longwave radiation
   - Net radiation balance
"""
print(products_text)

def amv_speed(displacement_km, time_diff_minutes):
    """Calculate atmospheric motion vector speed."""
    return displacement_km / (time_diff_minutes / 60)  # km/hr

def sst_brightness_temp_correction(T_11um, T_12um, viewing_angle_deg):
    """
    Simple split-window SST retrieval.

    Uses differential absorption in two channels.
    """
    # Simplified MCSST algorithm
    sec_theta = 1 / np.cos(np.radians(viewing_angle_deg))
    SST = T_11um + 1.0 * (T_11um - T_12um) + 0.5 * (T_11um - T_12um) * (sec_theta - 1)
    return SST

def ndvi(red_reflectance, nir_reflectance):
    """Calculate Normalized Difference Vegetation Index."""
    return (nir_reflectance - red_reflectance) / (nir_reflectance + red_reflectance)

print("\nAMV Speed Calculations:")
print("-" * 50)
print(f"{'Displacement (km)':<20} {'Time (min)':<15} {'Speed (km/hr)'}")
print("-" * 50)

for disp in [50, 100, 150, 200]:
    for dt in [10, 15, 30]:
        speed = amv_speed(disp, dt)
        if dt == 15:
            print(f"{disp:<20} {dt:<15} {speed:.0f}")

print("\n\nNDVI Examples:")
print("-" * 55)
print(f"{'Surface type':<20} {'Red':<10} {'NIR':<10} {'NDVI'}")
print("-" * 55)

surfaces = [
    ("Dense vegetation", 0.05, 0.50),
    ("Moderate veg", 0.10, 0.40),
    ("Sparse veg", 0.15, 0.25),
    ("Bare soil", 0.20, 0.22),
    ("Water", 0.05, 0.02),
    ("Snow/ice", 0.85, 0.85),
]

for surface, red, nir in surfaces:
    ndvi_val = ndvi(red, nir)
    print(f"{surface:<20} {red:<10} {nir:<10} {ndvi_val:+.2f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: SATELLITE REMOTE SENSING")
print("=" * 70)

summary = """
KEY SATELLITE PHYSICS:
=====================

1. BLACKBODY RADIATION
   - Planck function B_λ(T)
   - Wien's law: λ_max ∝ 1/T
   - Brightness temperature: T_B = f(measured radiance)

2. RADIATIVE TRANSFER
   - Absorption and emission along path
   - Optical depth τ = ∫ κρ ds
   - Transmission = exp(-τ)
   - Weighting functions peak where τ ≈ 1

3. ATMOSPHERIC WINDOWS
   - Visible, 3.9 μm, 10-12 μm: surface/cloud tops
   - 6.7 μm, 15 μm: atmospheric absorption → sounding
   - Microwave: all-weather capability

4. ORBITS
   - Geostationary (35,786 km): continuous viewing
   - Polar/sun-sync (700-850 km): global coverage
   - Tradeoff: temporal vs spatial resolution

5. TEMPERATURE SOUNDING
   - CO₂ 15 μm band: multiple channels
   - O₂ 60 GHz: all-weather (microwave)
   - Weighting functions at different levels

6. WATER VAPOR
   - 6-7 μm IR channels
   - 22, 183 GHz microwave
   - Upper/mid/lower troposphere sensing

7. DERIVED PRODUCTS
   - AMVs, SST, clouds, precipitation
   - NDVI, aerosols, ozone
   - Radiation budget


THE PHYSICS TELLS US:
====================
- All remote sensing based on radiative transfer
- Channel selection determines altitude sensitivity
- Microwave penetrates clouds (key advantage!)
- Multiple channels needed for profile retrieval
- Understanding physics essential for interpretation
"""
print(summary)

print("\n" + "=" * 70)
print("END OF SATELLITE REMOTE SENSING")
print("=" * 70)
