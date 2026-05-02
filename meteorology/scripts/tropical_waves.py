"""
TROPICAL WAVES: First-Principles Physics
==========================================

Equatorial wave dynamics from shallow water equations on equatorial β-plane.

Key wave types:
- Kelvin waves (eastward, trapped to equator)
- Rossby waves (westward, long wavelength)
- Mixed Rossby-gravity (Yanai) waves
- Inertio-gravity waves
- African Easterly Waves (AEWs)

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g = 9.81  # m/s², gravity
OMEGA = 7.292e-5  # rad/s, Earth's rotation rate
R_EARTH = 6.371e6  # m, Earth's radius
BETA_EQ = 2 * OMEGA / R_EARTH  # β at equator ≈ 2.29e-11 1/(m·s)

print("=" * 70)
print("TROPICAL WAVES: First-Principles Derivations")
print("=" * 70)

# =============================================================================
# PART 1: EQUATORIAL β-PLANE SHALLOW WATER EQUATIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: EQUATORIAL β-PLANE SHALLOW WATER EQUATIONS")
print("=" * 70)

print("""
HYPOTHESIS: Tropical waves can be understood from linearized shallow water
equations on an equatorial β-plane, where f = βy.

DERIVATION:

The shallow water equations on an equatorial β-plane:

    ∂u/∂t - βyv = -g ∂h/∂x
    ∂v/∂t + βyu = -g ∂h/∂y
    ∂h/∂t + H(∂u/∂x + ∂v/∂y) = 0

Where:
- (u, v) = horizontal velocity components
- h = surface height perturbation
- H = mean fluid depth (equivalent depth)
- β = df/dy at equator = 2Ω/R ≈ 2.29 × 10⁻¹¹ 1/(m·s)

KEY SCALING:

Define the equatorial Rossby radius of deformation:
    L_eq = √(c / β)   where c = √(gH)

This is the fundamental length scale for equatorial waves.

For equivalent depth H = 50 m (typical baroclinic mode):
    c = √(gH) = √(9.81 × 50) ≈ 22 m/s
    L_eq = √(22 / 2.29×10⁻¹¹) ≈ 980 km ≈ 1000 km

The equatorial radius of deformation sets the meridional trapping scale.
""")

def equatorial_rossby_radius(H_equiv):
    """
    Calculate equatorial Rossby radius of deformation.

    L_eq = √(c/β) where c = √(gH)

    This is the meridional e-folding scale for equatorial waves.
    """
    c = np.sqrt(g * H_equiv)
    L_eq = np.sqrt(c / BETA_EQ)
    return L_eq, c

# Test for different equivalent depths
print("Equatorial Rossby Radius for different modes:")
print("-" * 50)
for H in [10, 25, 50, 100, 200, 500]:
    L_eq, c = equatorial_rossby_radius(H)
    print(f"H = {H:4d} m: c = {c:6.1f} m/s, L_eq = {L_eq/1000:7.1f} km")

# =============================================================================
# PART 2: KELVIN WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: KELVIN WAVES")
print("=" * 70)

print("""
HYPOTHESIS: Eastward-propagating Kelvin waves exist when v = 0 identically.

DERIVATION:

Setting v = 0 in the shallow water equations:

    ∂u/∂t = -g ∂h/∂x         (1) Zonal momentum
    βyu = -g ∂h/∂y           (2) Meridional balance
    ∂h/∂t + H ∂u/∂x = 0      (3) Continuity

From (1) and (3): Classic 1D wave equation
    ∂²h/∂t² = c² ∂²h/∂x²     where c = √(gH)

Solution: h = h₀(y) exp[i(kx - ωt)]  with ω = ck (EASTWARD only)

From (2): The meridional structure
    βyu = -g ∂h/∂y

For geostrophic balance to work with eastward propagation:
    h₀(y) ∝ exp(-βy²/2c) = exp(-y²/2L_eq²)

PREDICTION: Kelvin waves are:
1. Eastward propagating at phase speed c = √(gH)
2. Gaussian-trapped to equator with e-folding scale L_eq
3. Have u and h in phase, v = 0
4. Non-dispersive (all wavelengths same speed)

VERIFICATION:
The Madden-Julian Oscillation (MJO) has a convectively-coupled Kelvin wave
component propagating eastward at ~5 m/s (slower than dry wave due to
moisture effects reducing equivalent depth).
""")

def kelvin_wave_structure(y_km, H_equiv):
    """
    Calculate Kelvin wave meridional structure.

    h(y) ∝ exp(-y²/2L_eq²)
    """
    L_eq, c = equatorial_rossby_radius(H_equiv)
    y = y_km * 1000  # convert to meters

    amplitude = np.exp(-y**2 / (2 * L_eq**2))

    return amplitude

def kelvin_wave_2d(x_km, y_km, t_hr, H_equiv, wavelength_km):
    """
    Full 2D Kelvin wave structure.

    h(x, y, t) = h₀ exp(-y²/2L_eq²) cos(kx - ωt)
    """
    L_eq, c = equatorial_rossby_radius(H_equiv)

    x = x_km * 1000  # m
    y = y_km * 1000  # m
    t = t_hr * 3600  # s

    k = 2 * np.pi / (wavelength_km * 1000)
    omega = c * k  # Kelvin wave dispersion

    meridional = np.exp(-y**2 / (2 * L_eq**2))
    zonal = np.cos(k * x - omega * t)

    return meridional * zonal

# Demonstrate Kelvin wave trapping
print("\nKelvin Wave Meridional Trapping (H = 50 m):")
print("-" * 50)
y_values = np.array([0, 500, 1000, 1500, 2000, 2500])
for y in y_values:
    amp = kelvin_wave_structure(y, 50)
    print(f"y = {y:5d} km from equator: amplitude = {amp:.4f}")

# =============================================================================
# PART 3: EQUATORIAL ROSSBY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: EQUATORIAL ROSSBY WAVES")
print("=" * 70)

print("""
HYPOTHESIS: Westward-propagating Rossby waves exist for long wavelengths.

DERIVATION:

For equatorial Rossby waves, seek solutions with parabolic cylinder functions.
The dispersion relation is:

    ω³ - (k²c² + βc)ω - k β c² = 0

For long waves (k → 0), the lowest-order Rossby mode:

    ω ≈ -kc / (2n + 1)     for mode number n = 1, 2, 3, ...

Phase speed: c_phase = ω/k = -c/(2n+1) < 0 (WESTWARD)

For n = 1 (first Rossby mode):
    c_phase = -c/3 ≈ -7.3 m/s (for c = 22 m/s)

MERIDIONAL STRUCTURE:
Rossby waves have Hermite function structures:
    φ_n(y) = H_n(y/L_eq) exp(-y²/2L_eq²)

Where H_n are Hermite polynomials:
    H₀ = 1, H₁ = 2y, H₂ = 4y² - 2, ...

PREDICTION: Equatorial Rossby waves:
1. Propagate WESTWARD
2. Have slower phase speed for higher modes
3. Are dispersive (speed depends on wavelength)
4. Have characteristic north-south velocity patterns

VERIFICATION:
Satellite observations show Rossby wave trains propagating westward across
the Pacific at ~5-10° longitude per day, consistent with theory.
""")

def rossby_wave_dispersion(k, n, H_equiv):
    """
    Equatorial Rossby wave dispersion relation (long wave limit).

    ω ≈ -kc/(2n+1) for Rossby waves

    Returns angular frequency ω (rad/s)
    """
    L_eq, c = equatorial_rossby_radius(H_equiv)
    omega = -k * c / (2 * n + 1)
    return omega

def rossby_phase_speed(n, H_equiv):
    """
    Phase speed of equatorial Rossby waves.

    c_phase = -c/(2n+1) (westward)
    """
    L_eq, c = equatorial_rossby_radius(H_equiv)
    return -c / (2 * n + 1)

# Test Rossby wave phase speeds
print("\nEquatorial Rossby Wave Phase Speeds (H = 50 m, c = 22 m/s):")
print("-" * 50)
L_eq, c = equatorial_rossby_radius(50)
print(f"Gravity wave speed c = {c:.1f} m/s")
for n in range(1, 6):
    c_phase = rossby_phase_speed(n, 50)
    deg_per_day = c_phase * 86400 / 111000  # convert to deg/day
    print(f"n = {n}: c_phase = {c_phase:6.2f} m/s = {deg_per_day:6.2f} °/day")

# =============================================================================
# PART 4: MIXED ROSSBY-GRAVITY (YANAI) WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: MIXED ROSSBY-GRAVITY (YANAI) WAVES")
print("=" * 70)

print("""
HYPOTHESIS: The n = 0 mode is a special "mixed" wave with properties of both
Rossby and gravity waves.

DERIVATION:

For n = 0, the dispersion relation gives:

    ω = k c / 2 ± √[(kc/2)² + βc]

Taking the physical root:
    ω = k c / 2 + √[(kc/2)² + βc]

PROPERTIES:
- For k > 0 (eastward): behaves like inertio-gravity wave
- For k < 0 (westward): behaves like Rossby wave
- Has westward group velocity for all k

Phase speed (always eastward):
    c_phase = ω/k = c/2 + √[(c/2)² + βc/k²]/k

At k = 0: singularity, but group velocity remains finite

MERIDIONAL STRUCTURE:
For n = 0, the structure is simply Gaussian:
    v ∝ exp(-y²/2L_eq²)

With u = 0 at the equator (antisymmetric about equator).

VERIFICATION:
Yanai waves are observed in the tropical Pacific with periods of 4-5 days,
important for transferring momentum across the equator.
""")

def yanai_dispersion(k, H_equiv):
    """
    Mixed Rossby-gravity (Yanai) wave dispersion.

    ω = kc/2 + √[(kc/2)² + βc]
    """
    L_eq, c = equatorial_rossby_radius(H_equiv)

    term1 = k * c / 2
    term2 = np.sqrt((k * c / 2)**2 + BETA_EQ * c)

    omega = term1 + term2
    return omega

# Yanai wave properties
print("\nYanai Wave Properties (H = 50 m):")
print("-" * 50)
wavelengths = [1000, 2000, 3000, 5000, 10000]  # km
for wl in wavelengths:
    k = 2 * np.pi / (wl * 1000)
    omega = yanai_dispersion(k, 50)
    period = 2 * np.pi / omega / 86400  # days
    c_phase = omega / k
    print(f"λ = {wl:5d} km: period = {period:5.1f} days, c_phase = {c_phase:5.1f} m/s (eastward)")

# =============================================================================
# PART 5: AFRICAN EASTERLY WAVES (AEWs)
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: AFRICAN EASTERLY WAVES (AEWs)")
print("=" * 70)

print("""
HYPOTHESIS: African Easterly Waves arise from barotropic-baroclinic instability
of the African Easterly Jet (AEJ).

DERIVATION:

The AEJ exists at ~650 hPa (~3 km) over North Africa:
- Peak wind: ~10-15 m/s at ~15°N
- Caused by thermal contrast: hot Sahara vs cooler Gulf of Guinea

INSTABILITY MECHANISM:

The necessary condition for barotropic instability (Rayleigh-Kuo):
    ∂²U/∂y² - β < 0 somewhere

The AEJ satisfies this due to strong horizontal shear.

Combined barotropic-baroclinic instability gives:

Growth rate σ ≈ √[(∂U/∂y)² + (f/N)²(∂U/∂z)²] - β

AEW CHARACTERISTICS:
- Wavelength: ~2000-4000 km
- Period: ~3-5 days
- Phase speed: ~7-8 m/s westward (embedded in AEJ)
- Growth region: 10°N-20°N over Africa

TROPICAL CYCLOGENESIS:

AEWs are precursors to ~60% of Atlantic hurricanes because:
1. They provide initial vorticity (positive at 700 hPa trough)
2. Northerly flow brings dry Saharan air, southerly brings moist
3. The trough provides upward motion and convection

PREDICTION: AEWs should have:
- ~3000 km wavelength
- ~4 day period
- Maximum amplitude near 15°N
- Northerly wind ahead of trough, southerly behind

VERIFICATION: Satellite tracks show ~50-60 AEWs per season (June-October),
with ~10% developing into tropical cyclones.
""")

def aew_characteristics(jet_speed=12, wavelength_km=3000):
    """
    Estimate AEW characteristics based on AEJ properties.
    """
    phase_speed = jet_speed * 0.6  # AEWs move slower than jet
    wavelength_m = wavelength_km * 1000

    period_s = wavelength_m / phase_speed
    period_days = period_s / 86400

    # Approximate growth rate from barotropic instability
    shear = 12 / (500 * 1000)  # rough estimate of ∂U/∂y
    growth_rate = np.sqrt(shear**2) - BETA_EQ * 2

    return phase_speed, period_days, growth_rate

print("\nAfrican Easterly Wave Properties:")
print("-" * 50)
for wl in [2000, 2500, 3000, 3500, 4000]:
    c_phase, period, growth = aew_characteristics(12, wl)
    print(f"λ = {wl} km: c_phase = {c_phase:.1f} m/s, period = {period:.1f} days")

print("\nAEW-Hurricane Connection:")
print("-" * 50)
print("""
~60 AEWs per season (June-October)
~10% develop into named storms
Famous examples:
- Hurricane Katrina (2005): AEW origin August 19
- Hurricane Maria (2017): AEW origin September 12
- Hurricane Dorian (2019): AEW origin August 24
""")

# =============================================================================
# PART 6: INERTIO-GRAVITY WAVES
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: INERTIO-GRAVITY WAVES")
print("=" * 70)

print("""
HYPOTHESIS: High-frequency gravity waves modified by rotation exist for all
mode numbers n ≥ 1.

DERIVATION:

From the full dispersion relation, for high frequencies:

    ω² = k²c² + βc(2n + 1)     for n = 1, 2, 3, ...

Or equivalently:
    ω² = c²(k² + (2n+1)/L_eq²)

This gives BOTH eastward and westward propagating waves.

Phase speed:
    c_phase = ±c√[1 + (2n+1)/(kL_eq)²]

PROPERTIES:
1. Always faster than pure gravity wave speed c
2. Propagate both east and west
3. Minimum frequency at k = 0: ω_min = √[βc(2n+1)]
4. Higher modes oscillate faster (larger meridional structure)

For n = 1, H = 50 m:
    ω_min = √(2.29×10⁻¹¹ × 22 × 3) = 1.23×10⁻⁵ rad/s
    Period_min = 2π/ω_min = 5.1 × 10⁵ s ≈ 6 days

VERIFICATION:
Inertio-gravity waves are observed in radiosonde data with periods of
1-10 days, and are important for momentum transport in the stratosphere.
""")

def inertio_gravity_dispersion(k, n, H_equiv, direction='east'):
    """
    Inertio-gravity wave dispersion.

    ω² = c²(k² + (2n+1)/L_eq²)
    """
    L_eq, c = equatorial_rossby_radius(H_equiv)

    omega_squared = c**2 * (k**2 + (2*n + 1) / L_eq**2)
    omega = np.sqrt(omega_squared)

    if direction == 'west':
        omega = -omega

    return omega

print("\nInertio-Gravity Wave Minimum Frequencies (H = 50 m):")
print("-" * 50)
L_eq, c = equatorial_rossby_radius(50)
for n in range(1, 5):
    omega_min = np.sqrt(BETA_EQ * c * (2*n + 1))
    period_days = 2 * np.pi / omega_min / 86400
    print(f"n = {n}: ω_min = {omega_min:.2e} rad/s, T_max = {period_days:.1f} days")

# =============================================================================
# PART 7: CONVECTIVELY COUPLED EQUATORIAL WAVES (CCEWs)
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: CONVECTIVELY COUPLED EQUATORIAL WAVES (CCEWs)")
print("=" * 70)

print("""
HYPOTHESIS: When equatorial waves couple with convection, their phase speeds
are reduced and equivalent depths become smaller.

PHYSICAL MECHANISM:

1. Wave-induced convergence triggers convection
2. Convective heating acts as a forcing term
3. Feedback between dynamics and heating

Modified dispersion - Reduced equivalent depth:
    H_eff ≈ 12-50 m (compared to 200-400 m dry modes)

This gives:
    c_eff = √(gH_eff) ≈ 12-22 m/s (vs 50-60 m/s dry)

WAVE-CONVECTION COUPLING STRENGTH:

Define the gross moist stability M:
    M = (MSE_outflow - MSE_inflow) / Δp

When M is small (weak stability), coupling is strong.
In deep tropics: M ≈ 5-10 K, giving strong coupling.

KEY CCEWs:

1. Convectively coupled Kelvin waves
   - Period: 3-10 days
   - Phase speed: 12-18 m/s eastward
   - Contribute to MJO

2. Convectively coupled Rossby waves
   - Period: 10-40 days
   - Phase speed: 5-8 m/s westward
   - Important for monsoon breaks

3. Convectively coupled MRG waves
   - Period: 4-5 days
   - Cross-equatorial flow patterns

4. Tropical Depression (TD) type
   - Period: 3-5 days
   - Phase speed: 5-8 m/s westward
   - Related to AEWs

VERIFICATION: Wheeler-Kiladis (1999) spectral analysis of OLR shows
clear spectral peaks along theoretical dispersion curves with H_eff ≈ 25 m.
""")

def ccew_equivalent_depth(H_dry=200, coupling_factor=0.2):
    """
    Estimate effective equivalent depth for CCEWs.

    Coupling reduces the effective equivalent depth.
    """
    return H_dry * coupling_factor

def ccew_phase_speed(wave_type='kelvin', H_eff=25):
    """
    Phase speed for convectively coupled waves.
    """
    c = np.sqrt(g * H_eff)

    if wave_type == 'kelvin':
        return c  # eastward
    elif wave_type == 'rossby_n1':
        return -c / 3  # westward
    elif wave_type == 'mrg':
        return c * 0.5  # complex, approximately
    else:
        return c

print("\nConvectively Coupled Wave Phase Speeds:")
print("-" * 50)
for H_eff in [12, 25, 50]:
    c_kelvin = ccew_phase_speed('kelvin', H_eff)
    c_rossby = ccew_phase_speed('rossby_n1', H_eff)
    print(f"H_eff = {H_eff:2d} m: Kelvin = {c_kelvin:5.1f} m/s, Rossby-1 = {c_rossby:5.1f} m/s")

# =============================================================================
# PART 8: MADDEN-JULIAN OSCILLATION (MJO) WAVE DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 8: MADDEN-JULIAN OSCILLATION (MJO)")
print("=" * 70)

print("""
HYPOTHESIS: The MJO is a planetary-scale convectively coupled disturbance
with Kelvin-Rossby wave structure.

OBSERVATIONS:
- Period: 30-60 days
- Phase speed: 4-8 m/s eastward
- Wavelength: ~40,000 km (wavenumber 1-2)
- Strongest over Indian Ocean and western Pacific

THEORETICAL FRAMEWORK:

The MJO couples:
1. Eastward-propagating Kelvin wave component (leading)
2. Westward-propagating Rossby wave component (trailing)
3. Large-scale convective envelope

Horizontal structure:
- Enhanced convection in center
- Low-level convergence (Kelvin) to east
- Twin cyclones (Rossby) to west
- Upper-level divergence

REDUCED PHASE SPEED:

The MJO is slower than pure Kelvin waves because:
1. Wave-convection interaction (moisture quasi-equilibrium)
2. Multi-scale interactions
3. Air-sea interaction

Effective dispersion:
    c_MJO ≈ 5 m/s << c_Kelvin (dry) ≈ 20-50 m/s

This requires very small effective equivalent depth: H_eff ~ 5 m

TELECONNECTIONS:

MJO modulates:
1. Atlantic hurricane activity (phase 1-2 suppress, 4-6 enhance)
2. West coast atmospheric rivers (phase 6-7 enhance)
3. Monsoon active/break cycles
4. Extratropical weather via Rossby wave trains

PREDICTABILITY:
MJO provides 2-4 weeks predictability for tropical and extratropical patterns.
""")

def mjo_phase_speed_estimate(H_eff=5):
    """
    Estimate MJO phase speed from effective equivalent depth.
    """
    return np.sqrt(g * H_eff)

def mjo_hurricane_modulation(mjo_phase):
    """
    Qualitative MJO modulation of Atlantic hurricane activity.

    Returns: 'suppress', 'neutral', or 'enhance'
    """
    if mjo_phase in [1, 2, 8]:
        return 'suppress'
    elif mjo_phase in [3, 7]:
        return 'neutral'
    else:  # phases 4, 5, 6
        return 'enhance'

print("\nMJO Properties:")
print("-" * 50)
c_mjo = mjo_phase_speed_estimate(5)
wavelength = 40000e3  # m
period = wavelength / c_mjo / 86400
print(f"Phase speed: {c_mjo:.1f} m/s")
print(f"Wavelength: ~40,000 km")
print(f"Period: {period:.0f} days")

print("\nMJO Atlantic Hurricane Modulation:")
print("-" * 50)
for phase in range(1, 9):
    effect = mjo_hurricane_modulation(phase)
    print(f"Phase {phase}: {effect}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("TROPICAL WAVES: SUMMARY")
print("=" * 70)

print("""
FUNDAMENTAL RESULTS:

1. EQUATORIAL ROSSBY RADIUS: L_eq = √(c/β)
   The meridional trapping scale for all equatorial waves

2. KELVIN WAVES: ω = ck (eastward, non-dispersive)
   - Trapped to equator, v = 0
   - Important for MJO, intraseasonal variability

3. ROSSBY WAVES: c_phase = -c/(2n+1) (westward)
   - Slower for higher modes
   - Carry info about tropical heating to midlatitudes

4. YANAI (MRG) WAVES: Special n = 0 mode
   - Connects Rossby and gravity wave behavior
   - Important for cross-equatorial momentum transport

5. AFRICAN EASTERLY WAVES: Barotropic-baroclinic instability
   - ~3000 km wavelength, ~4 day period
   - Precursors to 60% of Atlantic hurricanes

6. CONVECTIVE COUPLING: Reduces effective equivalent depth
   - H_eff ≈ 12-50 m vs 200+ m dry
   - Slower phase speeds, enhanced predictability

7. MJO: Planetary-scale coupled Kelvin-Rossby structure
   - 30-60 day period, ~5 m/s eastward
   - Major source of intraseasonal tropical predictability

Z² = 32π/3 CONNECTION:
Tropical waves, especially AEWs and CCEWs, provide the initial vorticity
perturbations that can develop into hurricanes. The wave-convection coupling
is a key feedback in hurricane intensification dynamics.
""")

print("\nScript completed successfully.")
