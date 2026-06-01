#!/usr/bin/env python3
"""
GRAVITY WAVES AND TURBULENCE - FIRST PRINCIPLES
================================================

Deriving the physics of atmospheric gravity waves,
clear-air turbulence, and mixing processes.
"""

import numpy as np

print("=" * 70)
print("GRAVITY WAVES AND TURBULENCE - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
g = 9.81           # Gravity (m/s²)
R_d = 287.0        # Gas constant dry air (J/kg/K)
c_p = 1004         # Specific heat (J/kg/K)
omega = 7.29e-5    # Earth rotation (rad/s)


# =============================================================================
# PART 1: ATMOSPHERIC GRAVITY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: INTERNAL GRAVITY WAVES")
print("=" * 70)

gw_text = """
INTERNAL GRAVITY WAVES:
=======================

Oscillations in stably stratified fluid
Restoring force: BUOYANCY

PHYSICS:

Displace air parcel vertically in stable atmosphere
→ Parcel experiences restoring force
→ Oscillates at Brunt-Väisälä frequency

BRUNT-VÄISÄLÄ FREQUENCY:

N² = (g/θ)(∂θ/∂z) = (g/T)(∂T/∂z + g/c_p)

Where θ = potential temperature

Typical values:
- Troposphere: N ≈ 0.01 s⁻¹ (period ~ 10 min)
- Stratosphere: N ≈ 0.02 s⁻¹ (period ~ 5 min)

DISPERSION RELATION:

ω² = N² × (k² + l²) / (k² + l² + m²)

Or: ω² = N² cos²(α)

Where α = angle from horizontal

KEY PROPERTIES:

1. ω < N always (waves slower than buoyancy frequency)
2. Horizontal propagation: ω → N
3. Vertical propagation: ω → 0
4. Group velocity ⟂ phase velocity!

WAVE SOURCES:

1. Topography (mountain waves)
2. Convection (convective gravity waves)
3. Fronts and jets (geostrophic adjustment)
4. Wind shear (Kelvin-Helmholtz)

MOMENTUM TRANSPORT:

Gravity waves transport momentum vertically
Wave breaking → momentum deposition
Crucial for stratospheric circulation!
"""
print(gw_text)

def brunt_vaisala(dT_dz, T_mean):
    """
    Calculate Brunt-Väisälä frequency.

    dT_dz: Temperature lapse rate (K/m), negative for decrease with height
    T_mean: Mean temperature (K)
    """
    gamma_d = g / c_p  # Dry adiabatic lapse rate
    N_squared = (g / T_mean) * (-dT_dz + gamma_d)
    if N_squared > 0:
        return np.sqrt(N_squared)
    return 0  # Unstable

def gravity_wave_frequency(N, k_horiz, m_vert):
    """
    Internal gravity wave frequency.

    ω² = N² × k²/(k² + m²)
    """
    k_total_sq = k_horiz**2 + m_vert**2
    if k_total_sq == 0:
        return 0
    omega_sq = N**2 * k_horiz**2 / k_total_sq
    return np.sqrt(omega_sq)

def wave_period(omega):
    """Convert angular frequency to period."""
    if omega == 0:
        return float('inf')
    return 2 * np.pi / omega

print("\nBrunt-Väisälä Frequency by Stability:")
print("-" * 60)
print(f"{'Lapse rate (°C/km)':<20} {'N (s⁻¹)':<15} {'Period (min)':<15} {'Stability'}")
print("-" * 60)

for lapse in [10, 8, 6.5, 4, 0, -2]:
    dT_dz = -lapse / 1000  # Convert to K/m
    N = brunt_vaisala(dT_dz, 270)
    if N > 0:
        T = wave_period(N) / 60
        stab = "Stable" if lapse < 9.8 else "Neutral"
    else:
        T = float('inf')
        stab = "Unstable"
    print(f"{lapse:<20} {N:<15.4f} {T:<15.1f} {stab}")


# =============================================================================
# PART 2: MOUNTAIN WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: MOUNTAIN WAVES")
print("=" * 70)

mountain_text = """
MOUNTAIN WAVE DYNAMICS:
=======================

Air forced over topography → wave generation

LINEAR THEORY:

For flow over sinusoidal terrain h(x) = h₀ cos(kx):

Vertical displacement: η = h₀ cos(kx + mz)

Where m² = (N/U)² - k²

THREE REGIMES:

1. VERTICALLY PROPAGATING (m² > 0, N/U > k)
   - Waves tilt upstream with height
   - Energy propagates upward
   - Can reach stratosphere

2. EVANESCENT (m² < 0, N/U < k)
   - Waves decay with height
   - Short wavelength terrain
   - No wave drag

3. HYDROSTATIC (k → 0)
   - m = N/U
   - Vertical wavelength λ_z = 2πU/N
   - Long terrain features

SCORER PARAMETER:

l² = N²/U² - (1/U)(d²U/dz²)

Waves trapped when l decreases with height

WAVE DRAG:

D = ρ × N × U × h₀²/2  (per unit ridge length)

Mountains exert drag on atmosphere!
Global mountain wave drag: ~10¹⁸ N

AMPLITUDE GROWTH:

Wave amplitude ∝ 1/√ρ

As density decreases with altitude:
- Amplitude increases
- Eventually → wave breaking
- Turbulence + momentum deposition
"""
print(mountain_text)

def vertical_wavenumber(N, U, k_horiz):
    """
    Calculate vertical wavenumber for mountain waves.

    m² = (N/U)² - k²
    """
    m_sq = (N/U)**2 - k_horiz**2
    if m_sq > 0:
        return np.sqrt(m_sq), "propagating"
    else:
        return np.sqrt(-m_sq), "evanescent"

def mountain_wave_drag(rho, N, U, h0):
    """
    Linear wave drag per unit ridge length.

    D = ρ N U h₀² / 2
    """
    return 0.5 * rho * N * U * h0**2

def wave_amplitude_growth(amplitude_0, rho_0, rho_z):
    """
    Wave amplitude increase with altitude.

    Amplitude ∝ 1/√ρ
    """
    return amplitude_0 * np.sqrt(rho_0 / rho_z)

print("\nMountain Wave Parameters:")
print("-" * 65)
print(f"{'U (m/s)':<12} {'N (s⁻¹)':<12} {'λ_terrain (km)':<18} {'m (rad/km)':<15} {'Type'}")
print("-" * 65)

for U in [10, 20, 30]:
    N = 0.01
    for lam_km in [10, 50, 200]:
        k = 2 * np.pi / (lam_km * 1000)
        m, wave_type = vertical_wavenumber(N, U, k)
        print(f"{U:<12} {N:<12} {lam_km:<18} {m*1000:<15.3f} {wave_type}")


# =============================================================================
# PART 3: KELVIN-HELMHOLTZ INSTABILITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: KELVIN-HELMHOLTZ INSTABILITY")
print("=" * 70)

kh_text = """
KELVIN-HELMHOLTZ INSTABILITY:
=============================

Shear-driven instability at density interface

MECHANISM:

Velocity shear creates pressure perturbations
→ Interface deforms
→ Billows develop
→ Break and mix

RICHARDSON NUMBER:

Ri = N² / (∂u/∂z)² = (g/θ)(∂θ/∂z) / (∂u/∂z)²

STABILITY CRITERION:

Ri > 0.25: STABLE (buoyancy dominates)
Ri < 0.25: UNSTABLE (shear dominates)

At Ri = 0.25 (critical):
Shear energy = 4 × Potential energy to mix

BILLOW CHARACTERISTICS:

Wavelength: λ ≈ 7 × shear layer thickness
Aspect ratio: ~3:1 (length:height)
Lifetime: ~5-10 minutes

GROWTH RATE:

σ = |∂u/∂z| × √(0.25 - Ri)  for Ri < 0.25

Maximum at Ri = 0: σ = 0.5 × |∂u/∂z|

KH IN ATMOSPHERE:

- Near jet stream (strong shear)
- Above/below inversions
- Clear-air turbulence (CAT)
- Visible as billow clouds
"""
print(kh_text)

def richardson_number(N, shear):
    """
    Calculate gradient Richardson number.

    Ri = N² / (du/dz)²
    """
    if shear == 0:
        return float('inf')
    return N**2 / shear**2

def kh_growth_rate(shear, Ri):
    """
    Kelvin-Helmholtz instability growth rate.

    σ = |du/dz| × √(0.25 - Ri)  for Ri < 0.25
    """
    if Ri >= 0.25:
        return 0
    return abs(shear) * np.sqrt(0.25 - Ri)

def kh_wavelength(layer_thickness):
    """Estimate KH billow wavelength."""
    return 7 * layer_thickness

print("\nRichardson Number and Stability:")
print("-" * 65)
print(f"{'N (s⁻¹)':<12} {'Shear (s⁻¹)':<15} {'Ri':<12} {'Status':<15} {'Growth (s⁻¹)'}")
print("-" * 65)

for N in [0.01, 0.015, 0.02]:
    for shear in [0.01, 0.02, 0.04, 0.08]:
        Ri = richardson_number(N, shear)
        status = "Stable" if Ri > 0.25 else "Unstable"
        growth = kh_growth_rate(shear, Ri)
        print(f"{N:<12} {shear:<15} {Ri:<12.2f} {status:<15} {growth:.4f}")


# =============================================================================
# PART 4: CLEAR-AIR TURBULENCE (CAT)
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: CLEAR-AIR TURBULENCE")
print("=" * 70)

cat_text = """
CLEAR-AIR TURBULENCE (CAT):
===========================

Turbulence outside of clouds - aviation hazard!

CAUSES:

1. JET STREAM SHEAR
   - Strong wind gradients at jet edges
   - Tropopause folding
   - KH instability

2. MOUNTAIN WAVES
   - Wave breaking aloft
   - Lee wave rotors
   - Can extend far downstream

3. FRONTAL ZONES
   - Strong temperature gradients
   - Associated wind shear

4. CONVECTIVELY-INDUCED
   - Above/around thunderstorms
   - Gravity waves from convection

TURBULENCE INTENSITY MEASURES:

Eddy Dissipation Rate (EDR):
ε = rate of turbulent kinetic energy dissipation (m²/s³)

Light: ε < 0.1 m²/s³
Moderate: ε = 0.1-0.3 m²/s³
Severe: ε = 0.3-0.5 m²/s³
Extreme: ε > 0.5 m²/s³

KOLMOGOROV SCALING:

In inertial subrange:
E(k) ∝ ε^(2/3) × k^(-5/3)

Velocity variance at scale l:
σ² ∝ ε^(2/3) × l^(2/3)

CAT FORECASTING:

Indices based on:
- Wind shear (jet proximity)
- Richardson number
- Deformation
- Divergence/convergence
"""
print(cat_text)

def turbulence_intensity_category(edr):
    """Categorize turbulence intensity from EDR."""
    if edr < 0.1:
        return "Light"
    elif edr < 0.3:
        return "Moderate"
    elif edr < 0.5:
        return "Severe"
    else:
        return "Extreme"

def kolmogorov_velocity(edr, length_scale):
    """
    Velocity fluctuation from Kolmogorov scaling.

    σ ∝ (ε × l)^(1/3)
    """
    return (edr * length_scale)**(1/3)

def cat_index(shear, N, deformation=0):
    """
    Simplified CAT potential index.

    Based on Richardson number and shear magnitude.
    """
    Ri = richardson_number(N, shear)

    # Index higher for lower Ri and higher shear
    if Ri > 1:
        return shear * 100  # Stable, shear-based only
    else:
        return shear * 100 * (1 + (1 - Ri) * 2)

print("\nEDR and Aircraft Response:")
print("-" * 55)
print(f"{'EDR (m²/s³)':<15} {'Category':<15} {'σ_w at 100m (m/s)':<20}")
print("-" * 55)

for edr in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8]:
    cat = turbulence_intensity_category(edr)
    sigma = kolmogorov_velocity(edr, 100)
    print(f"{edr:<15} {cat:<15} {sigma:<20.2f}")


# =============================================================================
# PART 5: TURBULENCE THEORY
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: TURBULENCE FUNDAMENTALS")
print("=" * 70)

turb_text = """
TURBULENCE PHYSICS:
===================

REYNOLDS NUMBER:

Re = UL/ν

Where:
- U = characteristic velocity
- L = characteristic length
- ν = kinematic viscosity (~1.5×10⁻⁵ m²/s for air)

Atmosphere: Re ~ 10⁸ to 10¹⁰ (highly turbulent!)

ENERGY CASCADE:

Large eddies → smaller eddies → ... → dissipation

Energy injection at large scales (L)
Dissipation at Kolmogorov scale (η)

KOLMOGOROV MICROSCALE:

η = (ν³/ε)^(1/4)

For ε = 0.1 m²/s³:
η ≈ 1 mm

INERTIAL SUBRANGE:

η << l << L

Energy spectrum: E(k) = C × ε^(2/3) × k^(-5/3)

C ≈ 1.5 (Kolmogorov constant)

TURBULENT KINETIC ENERGY (TKE):

TKE = ½(u'² + v'² + w'²)

TKE BUDGET:

∂TKE/∂t = Shear production + Buoyancy - Dissipation + Transport

Shear production: P = -u'w' × ∂U/∂z
Buoyancy: B = (g/θ) × w'θ'
Dissipation: ε

TURBULENT FLUXES:

Momentum: τ = -ρ u'w' = ρ K_m ∂U/∂z
Heat: H = ρ c_p w'θ' = -ρ c_p K_h ∂θ/∂z
"""
print(turb_text)

def reynolds_number(U, L, nu=1.5e-5):
    """Calculate Reynolds number."""
    return U * L / nu

def kolmogorov_scale(epsilon, nu=1.5e-5):
    """
    Kolmogorov microscale.

    η = (ν³/ε)^(1/4)
    """
    return (nu**3 / epsilon)**0.25

def inertial_subrange_velocity(epsilon, wavenumber, C=1.5):
    """
    Velocity from inertial subrange spectrum.

    E(k) = C × ε^(2/3) × k^(-5/3)
    """
    E = C * epsilon**(2/3) * wavenumber**(-5/3)
    return np.sqrt(E * wavenumber)

print("\nKolmogorov Microscale vs Dissipation Rate:")
print("-" * 50)
print(f"{'ε (m²/s³)':<18} {'η (mm)':<18} {'Turbulence'}")
print("-" * 50)

for eps in [0.001, 0.01, 0.1, 1.0, 10.0]:
    eta = kolmogorov_scale(eps) * 1000  # mm
    turb = "Weak" if eps < 0.01 else "Moderate" if eps < 0.1 else "Strong"
    print(f"{eps:<18} {eta:<18.2f} {turb}")


# =============================================================================
# PART 6: BOUNDARY LAYER TURBULENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: BOUNDARY LAYER TURBULENCE")
print("=" * 70)

pbl_turb_text = """
PBL TURBULENCE:
===============

SURFACE LAYER (lowest ~10%):

Monin-Obukhov Similarity Theory

Friction velocity: u* = √(τ/ρ) = √(-u'w')

Obukhov length: L = -u*³θ / (κ g w'θ')

Stability parameter: ζ = z/L

STABILITY REGIMES:

ζ < 0: Unstable (convective)
ζ = 0: Neutral
ζ > 0: Stable

WIND PROFILE:

U(z) = (u*/κ)[ln(z/z₀) - Ψ_m(ζ)]

Where Ψ_m = stability correction

CONVECTIVE BOUNDARY LAYER:

Mixed layer: ~uniform θ, q
Free convection scaling:
- Velocity scale: w* = (g w'θ' z_i / θ)^(1/3)
- Typical w* ~ 1-2 m/s

STABLE BOUNDARY LAYER:

- Suppressed turbulence
- Intermittent mixing
- Low-level jet formation
- Strong temperature inversions

TURBULENCE CLOSURE:

K-theory: Flux = -K × gradient
K ~ u* × z in surface layer
K ~ u* × z_i in mixed layer
"""
print(pbl_turb_text)

def friction_velocity(surface_stress, rho=1.2):
    """Calculate friction velocity u*."""
    return np.sqrt(abs(surface_stress) / rho)

def obukhov_length(u_star, theta, heat_flux, kappa=0.4):
    """
    Calculate Obukhov length.

    L = -u*³θ / (κ g w'θ')
    """
    if heat_flux == 0:
        return float('inf')
    return -u_star**3 * theta / (kappa * g * heat_flux)

def convective_velocity_scale(heat_flux, zi, theta=300):
    """
    Convective velocity scale w*.

    w* = (g w'θ' z_i / θ)^(1/3)
    """
    if heat_flux <= 0:
        return 0
    return (g * heat_flux * zi / theta)**(1/3)

print("\nConvective Boundary Layer Scales:")
print("-" * 60)
print(f"{'Heat flux (K·m/s)':<20} {'z_i (m)':<12} {'w* (m/s)':<15} {'Condition'}")
print("-" * 60)

for hf in [0.05, 0.1, 0.2, 0.3, 0.5]:
    for zi in [1000, 1500, 2000]:
        w_star = convective_velocity_scale(hf, zi)
        if zi == 1500:
            cond = "Weak" if w_star < 1 else "Moderate" if w_star < 2 else "Strong"
            print(f"{hf:<20} {zi:<12} {w_star:<15.2f} {cond}")


# =============================================================================
# PART 7: GRAVITY WAVE EFFECTS ON CLIMATE
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: GRAVITY WAVES AND LARGE-SCALE CIRCULATION")
print("=" * 70)

gw_climate_text = """
GRAVITY WAVE IMPACTS ON CIRCULATION:
====================================

WAVE DRAG:

Gravity waves transport momentum from sources to breaking levels

Mountain wave drag:
- Decelerates flow over mountains
- Deposits momentum in stratosphere
- ~30% of stratospheric wave driving

QUASI-BIENNIAL OSCILLATION (QBO):

Tropical stratospheric oscillation
Period: ~28 months

MECHANISM:
- Eastward + westward gravity waves from tropics
- Selective filtering by mean flow
- Momentum deposition → wind reversal
- Self-sustaining oscillation

MIDDLE ATMOSPHERE:

Gravity waves essential for:
1. Mesospheric temperature structure
2. Polar vortex strength
3. Brewer-Dobson circulation
4. Mesospheric cooling (summer pole!)

PARAMETERIZATION:

Models can't resolve all gravity waves
Must parameterize subgrid wave effects

Wave drag ~ ρ × wave stress divergence

Key parameters:
- Source spectrum
- Propagation/filtering
- Breaking levels
"""
print(gw_climate_text)

def wave_stress(rho, amplitude, N, U):
    """
    Gravity wave momentum flux (wave stress).

    τ = ρ × (amplitude)² × N × U / 2
    """
    return 0.5 * rho * amplitude**2 * N * U

def wave_drag_deceleration(stress_divergence, rho):
    """
    Deceleration from wave drag.

    du/dt = (1/ρ) × dτ/dz
    """
    return stress_divergence / rho

print("\nGravity Wave Stress and Drag:")
print("-" * 60)
print(f"{'Amplitude (m)':<15} {'N (s⁻¹)':<12} {'U (m/s)':<12} {'Stress (Pa)'}")
print("-" * 60)

for amp in [100, 200, 500, 1000]:
    stress = wave_stress(1.2, amp, 0.01, 20)
    print(f"{amp:<15} {0.01:<12} {20:<12} {stress:.3f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: GRAVITY WAVES AND TURBULENCE")
print("=" * 70)

summary = """
KEY PHYSICS:
===========

1. INTERNAL GRAVITY WAVES
   - Restoring force: buoyancy
   - Frequency: ω < N (Brunt-Väisälä)
   - Dispersion: ω = N cos(α)
   - Group velocity ⟂ phase velocity

2. MOUNTAIN WAVES
   - Vertical wavenumber: m² = (N/U)² - k²
   - Propagating vs evanescent
   - Vertical wavelength: λ_z = 2πU/N
   - Wave drag on atmosphere

3. KELVIN-HELMHOLTZ INSTABILITY
   - Richardson number: Ri = N²/(∂u/∂z)²
   - Critical: Ri < 0.25 → unstable
   - Growth rate: σ = |shear| × √(0.25 - Ri)
   - Produces CAT, mixing

4. CLEAR-AIR TURBULENCE
   - EDR classification (light to extreme)
   - Jet stream, mountain wave sources
   - Kolmogorov scaling: E(k) ∝ k^(-5/3)
   - Aviation hazard

5. TURBULENCE FUNDAMENTALS
   - Re ~ 10⁸-10¹⁰ in atmosphere
   - Energy cascade: large → small
   - Kolmogorov scale: η ~ 1 mm
   - TKE budget: production - dissipation

6. BOUNDARY LAYER
   - Surface layer: Monin-Obukhov theory
   - Convective: w* = (g w'θ' z_i / θ)^(1/3)
   - Stable: suppressed, intermittent

7. CLIMATE IMPACTS
   - Wave drag essential for circulation
   - QBO driven by gravity waves
   - Must parameterize in models


THE PHYSICS TELLS US:
====================
- Gravity waves ubiquitous, often invisible
- CAT from shear instability (Ri < 0.25)
- Turbulence cascades energy to small scales
- Waves transport momentum to stratosphere
- Small-scale processes affect large-scale climate
"""
print(summary)

print("\n" + "=" * 70)
print("END OF GRAVITY WAVES AND TURBULENCE")
print("=" * 70)
