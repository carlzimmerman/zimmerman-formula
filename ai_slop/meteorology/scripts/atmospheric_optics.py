#!/usr/bin/env python3
"""
Atmospheric Optics: First-Principles Derivations
=================================================

Complete physics of light propagation through atmosphere.

Key phenomena:
- Rainbows: Refraction + internal reflection in droplets
- Halos: Ice crystal refraction (22°, 46°)
- Mirages: Refractive index gradients
- Scattering: Rayleigh (blue sky), Mie (white clouds)
- Twilight: Earth shadow, atmospheric refraction

Starting from Maxwell's equations and geometric optics.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# Physical constants
c = 2.998e8          # Speed of light [m/s]
h_planck = 6.626e-34 # Planck constant [J·s]
k_B = 1.381e-23      # Boltzmann constant [J/K]

print("="*70)
print("ATMOSPHERIC OPTICS: FIRST-PRINCIPLES PHYSICS")
print("="*70)

#############################################
# PART 1: REFRACTIVE INDEX OF AIR
#############################################
print("\n" + "="*70)
print("PART 1: REFRACTIVE INDEX OF AIR")
print("="*70)

print("""
DERIVATION FROM ELECTROMAGNETIC THEORY:
======================================

From Maxwell's equations in a medium:
    n = √(ε_r μ_r) ≈ √ε_r   (for air, μ_r ≈ 1)

For a dilute gas, polarizability α relates to:
    ε_r - 1 = N α / ε₀

Where N = number density of molecules.

Using ideal gas law: N = P/(k_B T)

REFRACTIVITY (n-1) FOR DRY AIR:
    (n-1) × 10⁶ = 77.6 P/T - 5.6 e/T + 3.75×10⁵ e/T²

Where:
    P = total pressure [hPa]
    T = temperature [K]
    e = water vapor pressure [hPa]

The last two terms account for water vapor's
higher polarizability (dipole moment).

WAVELENGTH DEPENDENCE (dispersion):
    n(λ) - 1 ∝ λ⁻² (approximately, from Cauchy formula)

At standard conditions (P=1013.25 hPa, T=273.15 K):
    n_air ≈ 1.000293 at λ=589 nm (sodium D line)
""")

def refractive_index_air(P_hPa, T_K, e_hPa=0, wavelength_nm=589):
    """
    Calculate refractive index of air.

    Uses Edlén formula for dry air with humidity correction.
    """
    # Standard refractivity at reference conditions
    # Using simplified Edlén (1966) formula
    sigma = 1e7 / wavelength_nm  # wavenumber in μm⁻¹ units

    # Refractivity of standard dry air
    n_s = 8342.54 + 2406147 / (130 - sigma**2) + 15998 / (38.9 - sigma**2)
    n_s *= 1e-8

    # Density correction
    P_std = 1013.25
    T_std = 288.15  # 15°C reference

    n_dry = 1 + n_s * (P_hPa / P_std) * (T_std / T_K)

    # Water vapor correction
    n_vapor = -e_hPa * (37345 - 2.7 * sigma**2) * 1e-10

    return n_dry + n_vapor

# Demonstrate wavelength dependence
wavelengths = [400, 500, 589, 700, 800]  # nm
print("\nRefractive index vs wavelength (P=1013 hPa, T=288 K):")
print("-" * 40)
for wl in wavelengths:
    n = refractive_index_air(1013.25, 288.15, wavelength_nm=wl)
    print(f"  λ = {wl} nm:  n = {n:.8f}")

print("\nThis dispersion causes chromatic effects in rainbows!")

#############################################
# PART 2: RAYLEIGH SCATTERING - WHY SKY IS BLUE
#############################################
print("\n" + "="*70)
print("PART 2: RAYLEIGH SCATTERING")
print("="*70)

print("""
DERIVATION FROM DIPOLE RADIATION:
================================

When light interacts with molecules (d << λ),
the oscillating E-field induces a dipole moment:
    p = α E₀ e^(iωt)

An oscillating dipole radiates power (Larmor formula):
    P_rad = (ω⁴ |p|²) / (12π ε₀ c³)

The scattering cross-section is:

    σ_Rayleigh = (8π/3) × (2π/λ)⁴ × α²

For air molecules, this gives:

    σ = (128 π⁵ α²) / (3 λ⁴)

KEY RESULT: σ ∝ λ⁻⁴

This explains:
- Blue sky: Short λ scattered more (blue 4× more than red)
- Red sunsets: Long path → all blue scattered out
- Polarization: 90° scattering is 100% polarized

PHASE FUNCTION:
    P(θ) = (3/4)(1 + cos²θ)

Forward and backward scattering equal, perpendicular minimum.
""")

def rayleigh_cross_section(wavelength_nm):
    """
    Rayleigh scattering cross-section for air molecules.

    Returns cross-section in m².
    """
    wavelength_m = wavelength_nm * 1e-9

    # Refractive index of air
    n = refractive_index_air(1013.25, 288.15, wavelength_nm=wavelength_nm)

    # Number density at STP
    N = 2.687e25  # molecules/m³ (Loschmidt constant)

    # King correction factor for anisotropic molecules
    F_k = 1.05  # approximate for air

    # Cross-section formula
    sigma = (24 * np.pi**3 / (wavelength_m**4 * N**2)) * \
            ((n**2 - 1) / (n**2 + 2))**2 * F_k

    return sigma

def rayleigh_optical_depth(wavelength_nm, zenith_angle_deg=0):
    """
    Rayleigh optical depth through atmosphere.
    """
    sigma = rayleigh_cross_section(wavelength_nm)

    # Column density of atmosphere (molecules/m²)
    # Scale height H ≈ 8 km, surface N₀ ≈ 2.5e25/m³
    column = 2.15e29  # molecules/m²

    # Air mass factor for slant path
    sec_z = 1 / np.cos(np.radians(zenith_angle_deg))

    return sigma * column * sec_z

# Calculate relative scattering
print("\nRayleigh scattering vs wavelength:")
print("-" * 50)
wavelengths = [400, 450, 500, 550, 600, 650, 700]
sigma_ref = rayleigh_cross_section(550)

for wl in wavelengths:
    sigma = rayleigh_cross_section(wl)
    tau = rayleigh_optical_depth(wl)
    relative = sigma / sigma_ref
    color = "violet" if wl < 430 else "blue" if wl < 490 else \
            "cyan" if wl < 520 else "green" if wl < 570 else \
            "yellow" if wl < 600 else "orange" if wl < 650 else "red"
    print(f"  λ={wl}nm ({color:6s}): σ_rel={relative:.2f}, τ={tau:.3f}")

print("\n  Blue scattered ~5× more than red!")
print("  At sunset (90° zenith), τ_blue > 1 → blue removed")

#############################################
# PART 3: RAINBOW PHYSICS
#############################################
print("\n" + "="*70)
print("PART 3: RAINBOW PHYSICS")
print("="*70)

print("""
GEOMETRIC OPTICS OF RAINBOWS:
============================

Light ray enters spherical water drop:
1. Refraction at entry (Snell's law: n₁ sin θ₁ = n₂ sin θ₂)
2. Internal reflection(s)
3. Refraction at exit

TOTAL DEVIATION ANGLE:
For primary rainbow (1 internal reflection):
    D = 2(θ₁ - θ₂) + (π - 2θ₂)
    D = 2θ₁ - 4θ₂ + π

Using Snell's law: sin θ₁ = n sin θ₂

MINIMUM DEVIATION (rainbow angle):
    dD/dθ₁ = 0  →  cos θ₁ = √[(n²-1)/3]

For water (n ≈ 1.333):
    θ₁ = 59.4°
    D_min = 138°
    Rainbow angle = 180° - 138° = 42°

DISPERSION creates colors:
    n_red ≈ 1.331  → θ = 42.4°
    n_blue ≈ 1.343 → θ = 40.5°

Red on outside, violet inside (primary).

SECONDARY RAINBOW (2 internal reflections):
    D = 2θ₁ - 6θ₂ + 2π
    Rainbow angle ≈ 51° (colors reversed)

ALEXANDER'S DARK BAND:
Region between 42° and 51° - no light scattered.
""")

def snells_law(theta1, n1, n2):
    """Apply Snell's law: n1 sin(θ1) = n2 sin(θ2)"""
    sin_theta2 = (n1/n2) * np.sin(theta1)
    if abs(sin_theta2) > 1:
        return None  # Total internal reflection
    return np.arcsin(sin_theta2)

def rainbow_deviation(theta1_deg, n_water, k=1):
    """
    Calculate deviation angle for rainbow.

    k=1: primary (1 internal reflection)
    k=2: secondary (2 internal reflections)
    """
    theta1 = np.radians(theta1_deg)

    # Refraction at entry
    theta2 = snells_law(theta1, 1.0, n_water)
    if theta2 is None:
        return None

    # Total deviation
    D = 2*theta1 - 2*(k+1)*theta2 + k*np.pi

    return np.degrees(D)

def find_rainbow_angle(n_water, k=1):
    """
    Find the minimum deviation angle (rainbow angle).
    """
    # Analytical formula for angle of incidence at minimum deviation
    cos_theta1_sq = (n_water**2 - 1) / (k**2 + 2*k)
    if cos_theta1_sq < 0 or cos_theta1_sq > 1:
        return None, None

    theta1_opt = np.degrees(np.arccos(np.sqrt(cos_theta1_sq)))
    D_min = rainbow_deviation(theta1_opt, n_water, k)

    # Rainbow angle (from anti-solar point)
    rainbow_angle = 180 - abs(D_min) if D_min else None

    return theta1_opt, rainbow_angle

# Calculate rainbow angles for different wavelengths
print("\nPrimary Rainbow (k=1):")
print("-" * 55)
colors = [
    ("Red", 700, 1.331),
    ("Orange", 620, 1.333),
    ("Yellow", 580, 1.333),
    ("Green", 530, 1.335),
    ("Blue", 470, 1.338),
    ("Violet", 420, 1.343)
]

for color, wl, n in colors:
    theta1, angle = find_rainbow_angle(n, k=1)
    print(f"  {color:7s} (λ={wl}nm, n={n:.3f}): Rainbow angle = {angle:.1f}°")

print("\nSecondary Rainbow (k=2):")
print("-" * 55)
for color, wl, n in colors:
    theta1, angle = find_rainbow_angle(n, k=2)
    print(f"  {color:7s} (λ={wl}nm, n={n:.3f}): Rainbow angle = {angle:.1f}°")

print("\n  Primary: 40.5° (violet) to 42.4° (red) - red outside")
print("  Secondary: 50.3° (red) to 53.5° (violet) - red inside")
print("  Alexander's dark band: 42.4° to 50.3°")

#############################################
# PART 4: ICE CRYSTAL HALOS
#############################################
print("\n" + "="*70)
print("PART 4: ICE CRYSTAL HALOS")
print("="*70)

print("""
HALO PHYSICS FROM HEXAGONAL ICE CRYSTALS:
========================================

Cirrus clouds contain hexagonal ice crystals.
Light refracts through prism faces.

MINIMUM DEVIATION THROUGH PRISM:
For prism angle A:
    D_min = 2 arcsin(n sin(A/2)) - A

For ice (n ≈ 1.31):

22° HALO: Light through adjacent faces (A = 60°)
    D_min = 2 arcsin(1.31 × sin 30°) - 60°
    D_min = 2 arcsin(0.655) - 60°
    D_min = 2 × 40.9° - 60° = 21.8°

46° HALO: Light through top and side face (A = 90°)
    D_min = 2 arcsin(1.31 × sin 45°) - 90°
    D_min = 2 × 68° - 90° = 46°

CRITICAL ANGLE FOR ICE:
    θ_c = arcsin(1/n) = arcsin(1/1.31) = 49.8°

Rays entering at >49.8° undergo total internal reflection.

CIRCUMHORIZONTAL ARC:
Sun must be >58° elevation; light enters top,
exits side face (beautiful rainbow colors).

SUNDOGS (Parhelia):
Plate crystals falling flat; 22° from sun,
at same altitude; red toward sun.
""")

def prism_minimum_deviation(prism_angle_deg, n):
    """
    Calculate minimum deviation angle for a prism.

    D_min = 2 × arcsin(n × sin(A/2)) - A
    """
    A = np.radians(prism_angle_deg)
    sin_term = n * np.sin(A/2)

    if sin_term > 1:
        return None  # No transmission

    D_min = 2 * np.arcsin(sin_term) - A
    return np.degrees(D_min)

# Refractive index of ice vs wavelength (approximate)
ice_indices = [
    ("Red", 700, 1.306),
    ("Yellow", 580, 1.309),
    ("Green", 530, 1.311),
    ("Blue", 470, 1.315),
    ("Violet", 420, 1.321)
]

print("\n22° Halo (60° prism angle):")
print("-" * 45)
for color, wl, n in ice_indices:
    D = prism_minimum_deviation(60, n)
    print(f"  {color:7s}: D_min = {D:.2f}°")

print("\n46° Halo (90° prism angle):")
print("-" * 45)
for color, wl, n in ice_indices:
    D = prism_minimum_deviation(90, n)
    if D:
        print(f"  {color:7s}: D_min = {D:.2f}°")
    else:
        print(f"  {color:7s}: No transmission (TIR)")

print("\n  Note: 46° halo is fainter - larger deflection,")
print("        fewer crystals properly oriented.")

#############################################
# PART 5: MIRAGES AND REFRACTION
#############################################
print("\n" + "="*70)
print("PART 5: MIRAGES AND ATMOSPHERIC REFRACTION")
print("="*70)

print("""
MIRAGE PHYSICS FROM REFRACTIVE INDEX GRADIENTS:
==============================================

Refractive index depends on density:
    n ≈ 1 + k ρ  (where k ≈ 0.23 cm³/g for air)

Using ideal gas: ρ = P M / (R T)
So: n - 1 ∝ P/T

In a thermal gradient, rays curve via Snell's law:
    n(z) sin θ(z) = constant along ray

RAY CURVATURE:
    1/R = -(1/n)(dn/dz) cos θ

For nearly horizontal rays:
    1/R ≈ -(1/n)(dn/dz)

TEMPERATURE GRADIENT → CURVATURE:
    dn/dz ≈ -(n-1)/T × dT/dz

INFERIOR MIRAGE (hot surface):
- Hot air near surface → lower n → rays curve upward
- Observer sees inverted image below horizon
- dT/dz < 0 (lapse) → dn/dz > 0 → curves up

SUPERIOR MIRAGE (cold surface):
- Cold air near surface → higher n → rays curve downward
- Objects appear elevated, can see beyond horizon
- Common over cold water/ice

LOOMING, TOWERING, STOOPING:
Vertical magnification/compression from n(z) gradients.

ASTRONOMICAL REFRACTION:
At horizon, R ≈ 0.58° → sun visible when
geometrically below horizon!
""")

def atmospheric_refraction(altitude_deg, P_hPa=1013.25, T_K=288.15):
    """
    Calculate atmospheric refraction correction.

    Uses Bennett formula (accurate to <0.1 arcmin).
    """
    if altitude_deg < -1:
        return 0

    a = altitude_deg

    # Bennett formula
    R_arcmin = 1.02 / np.tan(np.radians(a + 10.3/(a + 5.11)))

    # Pressure and temperature correction
    R_arcmin *= (P_hPa / 1010) * (283 / T_K)

    return R_arcmin / 60  # Convert to degrees

def mirage_ray_curvature(dT_dz, T_mean=300, P_hPa=1013.25):
    """
    Calculate ray curvature from temperature gradient.

    Parameters:
        dT_dz: Temperature gradient [K/m] (negative = lapse)
        T_mean: Mean temperature [K]

    Returns:
        Radius of curvature [m] (positive = curves upward)
    """
    # Refractivity at mean conditions
    n_minus_1 = 77.6e-6 * P_hPa / T_mean

    # dn/dz from temperature gradient
    dn_dz = -n_minus_1 * dT_dz / T_mean

    # Radius of curvature (for horizontal ray)
    R = -1 / dn_dz if dn_dz != 0 else float('inf')

    return R

print("\nAtmospheric refraction vs altitude:")
print("-" * 40)
altitudes = [90, 45, 20, 10, 5, 2, 1, 0.5, 0]
for alt in altitudes:
    R = atmospheric_refraction(alt)
    print(f"  Altitude {alt:4.1f}°: Refraction = {R*60:.2f} arcmin")

print("\n  At horizon: Sun appears ~35 arcmin higher!")
print("  Sun diameter ≈ 32 arcmin → sun visible when fully set!")

print("\nMirage ray curvature vs temperature gradient:")
print("-" * 55)
gradients = [("Strong lapse (hot road)", -10),
             ("Normal lapse", -6.5/1000),
             ("Isothermal", 0),
             ("Inversion", +10/1000),
             ("Strong inversion (arctic)", +0.1)]

for name, dT in gradients:
    R = mirage_ray_curvature(dT)
    direction = "upward" if R > 0 else "downward"
    print(f"  {name:25s}: R = {abs(R)/1000:.1f} km ({direction})")

#############################################
# PART 6: SCATTERING AND SKY COLOR
#############################################
print("\n" + "="*70)
print("PART 6: SKY COLOR AND TWILIGHT")
print("="*70)

print("""
SKY COLOR FROM MULTIPLE SCATTERING:
==================================

Single scattering approximation:
    I(λ, θ) ∝ (1/λ⁴) × (1 + cos²θ) × e^(-τ sec z)

Where:
    τ = optical depth (Rayleigh + aerosol)
    z = solar zenith angle
    θ = scattering angle

HORIZON SKY IS LIGHTER:
Long path through atmosphere → multiply scattered
light adds white appearance.

SUNSET COLORS:
Path length through atmosphere varies as sec(z).
At z = 90°, light passes through ~38× more atmosphere!

    τ_effective = τ × sec(z)

For z = 85°: sec(85°) ≈ 11.5
    Blue (τ=0.25): τ_eff = 2.9 → e⁻² ≈ 0.05 (5% transmitted)
    Red (τ=0.05):  τ_eff = 0.58 → e⁻⁰·⁵⁸ ≈ 0.56 (56% transmitted)

Red dominates at sunset!

TWILIGHT PHASES:
- Civil twilight: Sun 0-6° below horizon
  (Enough light to read, bright colors)
- Nautical twilight: 6-12° below
  (Horizon visible, stars appearing)
- Astronomical twilight: 12-18° below
  (Sky dark enough for astronomy)

EARTH'S SHADOW (Belt of Venus):
At sunset, pink arch (sunlit atmosphere)
above blue-gray band (Earth's shadow).
""")

def sky_brightness(wavelength_nm, solar_zenith_deg, view_zenith_deg, scattering_angle_deg):
    """
    Estimate relative sky brightness from single scattering.
    """
    # Rayleigh optical depth
    tau = rayleigh_optical_depth(wavelength_nm, view_zenith_deg)

    # Scattering phase function
    theta = np.radians(scattering_angle_deg)
    phase = (3/4) * (1 + np.cos(theta)**2)

    # Solar attenuation
    tau_sun = rayleigh_optical_depth(wavelength_nm, solar_zenith_deg)

    # Single scattering approximation
    I = (1/wavelength_nm**4) * phase * np.exp(-tau_sun) * (1 - np.exp(-tau))

    return I

def sunset_transmission(wavelength_nm, zenith_deg):
    """
    Calculate fraction of direct sunlight transmitted.
    """
    tau = rayleigh_optical_depth(wavelength_nm, zenith_deg)
    return np.exp(-tau)

print("\nDirect sunlight transmission vs zenith angle:")
print("-" * 60)
zeniths = [0, 60, 75, 85, 87, 89]
print(f"{'Zenith':>8s}  {'Blue(450nm)':>12s}  {'Green(550nm)':>12s}  {'Red(650nm)':>12s}")
print("-" * 60)
for z in zeniths:
    T_b = sunset_transmission(450, z)
    T_g = sunset_transmission(550, z)
    T_r = sunset_transmission(650, z)
    print(f"{z:>6.0f}°  {T_b:>12.1%}  {T_g:>12.1%}  {T_r:>12.1%}")

print("\n  At sunset (89°): Red/Blue ratio = {:.0f}×".format(
    sunset_transmission(650, 89) / sunset_transmission(450, 89)))

#############################################
# PART 7: GLORY AND CORONA
#############################################
print("\n" + "="*70)
print("PART 7: GLORY AND CORONA (DIFFRACTION)")
print("="*70)

print("""
THESE REQUIRE WAVE OPTICS (not just geometrics):

CORONA (around Sun/Moon through thin cloud):
==========================================
Diffraction by cloud droplets (d ~ λ).

For circular aperture (Airy pattern):
    θ_first_min = 1.22 λ/D

For cloud droplet diameter D ~ 10 μm:
    θ = 1.22 × 0.5 μm / 10 μm = 0.061 rad ≈ 3.5°

Larger droplets → smaller corona.
Colors: blue inside, red outside (opposite to halo).

GLORY (colored rings around shadow on cloud):
===========================================
Seen from aircraft looking at shadow on cloud below.

More complex physics involving:
- Surface waves (creeping rays)
- Edge diffraction
- Requires Mie theory for full explanation

Angular radius ≈ λ/(π r) for droplet radius r.
Typical glory: 2-5° radius.

BISHOP'S RING:
Large brown/blue corona after volcanic eruptions,
due to stratospheric sulfate aerosols.
""")

def corona_ring_angle(droplet_diameter_um, wavelength_nm=550, ring_number=1):
    """
    Calculate angular radius of corona ring.

    Uses Airy diffraction pattern.
    """
    # First few zeros of Bessel function J₁
    bessel_zeros = [1.22, 2.23, 3.24, 4.24]  # Approximate

    if ring_number < 1 or ring_number > 4:
        return None

    factor = bessel_zeros[ring_number - 1]
    wavelength_um = wavelength_nm / 1000

    theta_rad = factor * wavelength_um / droplet_diameter_um
    return np.degrees(theta_rad)

print("\nCorona ring angles for various droplet sizes:")
print("-" * 50)
print(f"{'Droplet D':>12s}  {'1st ring':>10s}  {'2nd ring':>10s}")
print("-" * 50)
for D in [5, 10, 15, 20, 30, 50]:
    r1 = corona_ring_angle(D, ring_number=1)
    r2 = corona_ring_angle(D, ring_number=2)
    print(f"{D:>10.0f} μm  {r1:>9.1f}°  {r2:>9.1f}°")

print("\n  Larger droplets → tighter corona")
print("  Color sequence (inside out): blue, green, red")

#############################################
# SUMMARY
#############################################
print("\n" + "="*70)
print("ATMOSPHERIC OPTICS SUMMARY")
print("="*70)
print("""
Key Principles and Phenomena:

1. REFRACTIVE INDEX: n-1 ∝ P/T (∝ density)
   - Wavelength dependent (dispersion)
   - Creates all refraction phenomena

2. RAYLEIGH SCATTERING: σ ∝ λ⁻⁴
   - Blue sky, red sunsets
   - Polarization at 90°

3. RAINBOWS: Refraction + internal reflection
   - Primary: 42° (red outside)
   - Secondary: 51° (red inside)
   - Alexander's dark band between

4. ICE HALOS: Hexagonal crystal refraction
   - 22° halo: Adjacent faces (60° prism)
   - 46° halo: Top/side faces (90° prism)
   - Sundogs at 22° from sun

5. MIRAGES: dn/dz from temperature gradients
   - Inferior (hot surface): Images below
   - Superior (cold surface): Images above
   - Astronomical refraction: ~35' at horizon

6. DIFFRACTION EFFECTS:
   - Corona: Airy pattern from droplets
   - Glory: Complex wave interference

The atmosphere is an optical laboratory!
""")

if __name__ == "__main__":
    print("\n[Atmospheric Optics Module - First Principles Complete]")
