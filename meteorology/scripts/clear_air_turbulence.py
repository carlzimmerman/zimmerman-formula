"""
CLEAR AIR TURBULENCE (CAT): First-Principles Physics
======================================================

Physics of turbulence in cloud-free regions, critical for aviation safety.

Topics:
- Kelvin-Helmholtz instability
- Richardson number criterion
- Jet stream turbulence
- Mountain wave breaking
- Gravity wave dynamics
- Turbulence intensity indices

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np

# Physical constants
g = 9.81  # m/s²
OMEGA = 7.292e-5  # rad/s

print("=" * 70)
print("CLEAR AIR TURBULENCE: First-Principles Physics")
print("=" * 70)

# =============================================================================
# PART 1: RICHARDSON NUMBER CRITERION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: RICHARDSON NUMBER CRITERION")
print("=" * 70)

print("""
HYPOTHESIS: Turbulence develops when wind shear is strong enough to overcome
static stability. The Richardson number quantifies this balance.

DERIVATION:

Consider a stably stratified fluid with vertical wind shear.
Two competing effects:

1. STABILITY (suppresses turbulence):
   Brunt-Väisälä frequency: N² = (g/θ)(∂θ/∂z)
   Potential energy required to displace parcel

2. SHEAR (generates turbulence):
   Wind shear: S² = (∂u/∂z)² + (∂v/∂z)²
   Kinetic energy available from mean flow

GRADIENT RICHARDSON NUMBER:

    Ri = N² / S² = (g/θ)(∂θ/∂z) / [(∂u/∂z)² + (∂v/∂z)²]

STABILITY CRITERION:

Linear analysis shows:
    Ri < 1/4 (Ri_critical)  →  Kelvin-Helmholtz instability
    Ri > 1    →  Stable, no turbulence
    1/4 < Ri < 1  →  Transition zone, intermittent turbulence

PHYSICAL INTERPRETATION:
- Ri < 0.25: Shear kinetic energy exceeds potential energy barrier
- Turbulence extracts energy from mean shear
- Mixing increases Ri toward critical value (self-limiting)

PREDICTION: CAT most likely where:
1. Strong wind shear (jet stream)
2. Weak static stability (upper troposphere)
3. Ri < 0.25

VERIFICATION: Aircraft measurements confirm Ri < 0.25 in CAT regions
with 70-80% reliability.
""")

def brunt_vaisala_frequency(theta, dtheta_dz):
    """
    N² = (g/θ)(∂θ/∂z)

    Returns N² (rad²/s²) and N (rad/s)
    """
    N_squared = (g / theta) * dtheta_dz
    N = np.sqrt(np.maximum(N_squared, 0))
    return N_squared, N

def richardson_number(theta, dtheta_dz, du_dz, dv_dz):
    """
    Ri = N² / S²

    Returns Richardson number
    """
    N_squared, _ = brunt_vaisala_frequency(theta, dtheta_dz)
    S_squared = du_dz**2 + dv_dz**2
    Ri = N_squared / S_squared if S_squared > 0 else np.inf
    return Ri

def cat_probability_from_ri(Ri):
    """
    Estimate CAT probability from Richardson number.
    """
    if Ri < 0.25:
        return "High (>70%)"
    elif Ri < 0.5:
        return "Moderate (30-70%)"
    elif Ri < 1.0:
        return "Low (10-30%)"
    else:
        return "Negligible (<10%)"

# Examples
print("\nRichardson Number Examples:")
print("-" * 70)
print(f"{'Scenario':<35} {'Ri':<10} {'CAT probability'}")
print("-" * 70)

scenarios = [
    ("Strong shear, weak stability", 300, 2.0, 0.02, 0.01),
    ("Moderate shear, moderate stab.", 300, 5.0, 0.01, 0.005),
    ("Weak shear, strong stability", 300, 10.0, 0.005, 0.002),
    ("Jet stream core edge", 300, 3.0, 0.025, 0.015),
    ("Tropopause", 220, 15.0, 0.008, 0.004),
]

for name, theta, dtheta_dz, du_dz, dv_dz in scenarios:
    Ri = richardson_number(theta, dtheta_dz, du_dz, dv_dz)
    prob = cat_probability_from_ri(Ri)
    print(f"{name:<35} {Ri:<10.2f} {prob}")

# =============================================================================
# PART 2: KELVIN-HELMHOLTZ INSTABILITY
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: KELVIN-HELMHOLTZ INSTABILITY")
print("=" * 70)

print("""
HYPOTHESIS: When Ri < 1/4, shear instability creates characteristic
billows that roll up and break, generating turbulence.

DERIVATION:

Linear stability analysis for parallel shear flow with stratification.

Consider perturbations of form:
    ψ' = φ(z) exp[ik(x - ct)]

The Taylor-Goldstein equation governs φ(z):
    d²φ/dz² + [N²/(U-c)² - k² - (d²U/dz²)/(U-c)] φ = 0

For simple shear layer (hyperbolic tangent profile):
- Instability occurs when Ri < 1/4
- Fastest growing wavelength: λ ≈ 7h (where h = shear layer thickness)
- Growth rate: σ ≈ 0.2 × S (where S = max shear)

BILLOWING PROCESS:

1. Initial perturbation amplifies exponentially
2. Wave crests steepen and roll up
3. "Cat's eye" pattern forms
4. Wave breaking generates turbulence
5. Mixing increases Ri, stabilizing flow

TIME SCALES:
- Growth: τ_grow ~ 1/σ ~ 5/(S) ~ 5-10 minutes
- Breaking: τ_break ~ 1-2 minutes
- Decay: τ_decay ~ 10-20 minutes

EDDY SIZE:
- Horizontal: 100 m - 10 km
- Vertical: 100 m - 1 km
- These scales affect aircraft differently (larger is worse)
""")

def kh_growth_rate(shear, Ri):
    """
    Approximate growth rate for KH instability.

    σ ≈ 0.2 × S × √(1 - 4Ri) for Ri < 0.25
    """
    if Ri >= 0.25:
        return 0
    return 0.2 * shear * np.sqrt(1 - 4 * Ri)

def kh_wavelength(shear_layer_thickness):
    """
    Most unstable wavelength ≈ 7h
    """
    return 7 * shear_layer_thickness

# KH instability characteristics
print("\nKH Instability Growth Rates:")
print("-" * 60)
print(f"{'Shear (1/s)':<15} {'Ri':<10} {'Growth rate (1/s)':<20} {'e-folding (s)'}")
print("-" * 60)

for shear in [0.01, 0.02, 0.03, 0.05]:
    for Ri in [0.05, 0.1, 0.2, 0.24]:
        sigma = kh_growth_rate(shear, Ri)
        e_fold = 1/sigma if sigma > 0 else np.inf
        print(f"{shear:<15.3f} {Ri:<10.2f} {sigma:<20.4f} {e_fold:<.0f}")

# =============================================================================
# PART 3: JET STREAM TURBULENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: JET STREAM TURBULENCE")
print("=" * 70)

print("""
HYPOTHESIS: Clear air turbulence is most common near jet streams due to
strong vertical and horizontal wind shear.

JET STREAM STRUCTURE:

The thermal wind relationship:
    ∂V_g/∂z = (g/fT) ∇_h T

Strong horizontal temperature gradient → Strong vertical wind shear

JET STREAM WIND PROFILE:
    V(z) = V_max × exp[-(z - z_jet)²/2σ_z²]

Where:
- V_max ≈ 50-100 m/s (core wind)
- z_jet ≈ 9-12 km (core altitude)
- σ_z ≈ 2-3 km (vertical scale)

CAT LOCATIONS RELATIVE TO JET:

1. CYCLONIC SIDE (left of jet in NH):
   - Lower tropopause
   - Enhanced shear
   - Reduced stability
   - HIGHEST CAT probability (50-70% of cases)

2. JET CORE:
   - Maximum wind but reduced shear
   - Moderate CAT probability

3. ANTICYCLONIC SIDE (right of jet in NH):
   - Higher tropopause
   - Enhanced stability
   - Lower CAT probability

4. JET ENTRANCE/EXIT REGIONS:
   - Strong speed divergence
   - Ageostrophic circulations
   - Enhanced vertical motion
   - Moderate CAT probability

CRITICAL SHEAR ZONES:
1. Above jet core (wind decreases sharply)
2. Cyclonic edge (horizontal shear)
3. Tropopause (sharp stability change)
""")

def jet_stream_profile(z, z_jet=10000, sigma_z=2500, V_max=70):
    """
    Gaussian jet stream wind profile.

    z in meters, returns wind in m/s
    """
    return V_max * np.exp(-(z - z_jet)**2 / (2 * sigma_z**2))

def jet_vertical_shear(z, z_jet=10000, sigma_z=2500, V_max=70):
    """
    Vertical shear of jet stream.
    dV/dz = V × (z_jet - z) / σ_z²
    """
    V = jet_stream_profile(z, z_jet, sigma_z, V_max)
    return V * (z_jet - z) / sigma_z**2

# Demonstrate jet structure
print("\nJet Stream Profile and Shear:")
print("-" * 60)
print(f"{'Altitude (km)':<15} {'Wind (m/s)':<15} {'Shear (1/s)':<15} {'CAT risk'}")
print("-" * 60)

z_jet = 10000  # 10 km
for z_km in [6, 7, 8, 9, 10, 11, 12, 13, 14]:
    z = z_km * 1000
    V = jet_stream_profile(z, z_jet)
    S = abs(jet_vertical_shear(z, z_jet))
    # Estimate stability
    if z < 11000:
        dtheta_dz = 3  # K/km troposphere
    else:
        dtheta_dz = 15  # K/km stratosphere

    Ri = richardson_number(300, dtheta_dz/1000, S, 0)
    risk = "HIGH" if Ri < 0.25 else "MOD" if Ri < 1 else "LOW"

    print(f"{z_km:<15} {V:<15.1f} {S*1000:<15.2f} {risk}")

# =============================================================================
# PART 4: MOUNTAIN WAVE TURBULENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: MOUNTAIN WAVE TURBULENCE")
print("=" * 70)

print("""
HYPOTHESIS: Flow over mountains generates gravity waves that can propagate
upward and break, causing severe turbulence (mountain wave turbulence, MWT).

MOUNTAIN WAVE DYNAMICS:

1. GENERATION:
   Air forced over mountain, displaced from equilibrium
   Buoyancy provides restoring force
   Waves propagate upward if conditions allow

2. LINEAR THEORY:
   Vertical wavelength: λ_z = 2πU/N
   Phase tilt with height for upward energy propagation

3. WAVE AMPLITUDE:
   Amplitude increases as √(ρ₀/ρ(z)) due to density decrease
   Factor of ~3 from surface to 10 km

4. BREAKING CRITERION:
   Wave overturns when: |du'/dz| > N
   Or equivalently: amplitude > λ_z/(2π)

   Critical level: Where U = 0 (wave cannot propagate)
   Scorer parameter: l² = N²/U² - (1/U)d²U/dz²

WAVE BREAKING SCENARIOS:

1. ROTOR TURBULENCE (low level):
   Below mountain top in lee
   Extremely hazardous (severe turbulence)
   Associated with downslope windstorms

2. STRATOSPHERIC BREAKING:
   Waves reach stratosphere and break
   Deposits momentum (important for QBO)
   Severe turbulence at flight levels

3. CRITICAL LEVEL ABSORPTION:
   Wave energy absorbed where U matches wave phase speed
   Strong turbulence localized at critical level

CONDITIONS FOR SEVERE MWT:
- Strong cross-mountain wind (>25 kt)
- Stable layer near mountain top
- Weaker wind or reversal aloft (trapping layer)
- High mountains (Rockies, Andes, Alps)
""")

def vertical_wavelength_mountain(U, N):
    """
    λ_z = 2πU/N

    U: cross-mountain wind (m/s)
    N: Brunt-Väisälä frequency (rad/s)
    """
    return 2 * np.pi * U / N

def wave_amplitude_growth(z, z_ref=0, H_scale=8500):
    """
    Wave amplitude grows as √(ρ₀/ρ) = exp(z/2H)
    """
    return np.exp((z - z_ref) / (2 * H_scale))

def scorer_parameter(U, N, d2U_dz2):
    """
    l² = N²/U² - (1/U)d²U/dz²

    Waves propagate vertically where l² > k² (k = horizontal wavenumber)
    """
    return N**2 / U**2 - d2U_dz2 / U

# Mountain wave characteristics
print("\nMountain Wave Vertical Wavelengths:")
print("-" * 50)
print(f"{'Wind (m/s)':<15} {'N (rad/s)':<15} {'λ_z (m)'}")
print("-" * 50)

for U in [10, 20, 30, 40]:
    for N in [0.01, 0.015, 0.02]:
        lz = vertical_wavelength_mountain(U, N)
        print(f"{U:<15} {N:<15.3f} {lz:<.0f}")

print("\nWave Amplitude Growth with Height:")
print("-" * 50)
for z_km in [0, 3, 6, 9, 12, 15]:
    growth = wave_amplitude_growth(z_km * 1000)
    print(f"z = {z_km:2d} km: amplitude factor = {growth:.2f}")

# =============================================================================
# PART 5: TURBULENCE INTENSITY INDICES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: TURBULENCE INTENSITY INDICES")
print("=" * 70)

print("""
HYPOTHESIS: Operational CAT forecasts use empirical indices derived from
NWP model output to predict turbulence probability and intensity.

COMMON INDICES:

1. ELLROD INDEX (TI):
   TI = VWS × (DEF + CVG)

   Where:
   - VWS = vertical wind shear
   - DEF = deformation = √(stretching² + shearing²)
   - CVG = convergence = -(∂u/∂x + ∂v/∂y)

   Thresholds: TI > 4 = light, > 8 = moderate, > 12 = severe

2. FRONTOGENESIS FUNCTION:
   F = d|∇θ|/dt = -[D₁cos(2β) + D₂sin(2β)]|∇θ|/2

   Strong frontogenesis → enhanced shear → CAT

3. DUTTON INDEX (E):
   E = 1.25 × VWS + 0.25 × DEF + 10.5 × (1 - Ri/Ri_crit)

   Combines shear, deformation, and stability

4. GRAPHICAL TURBULENCE GUIDANCE (GTG):
   Ensemble of multiple indices
   Machine learning weighting
   Best operational skill currently

EDDY DISSIPATION RATE (EDR):

Physical measure of turbulence intensity:
    ε = energy dissipation per unit mass (m²/s³)

Aircraft-reported EDR:
- < 0.1: Smooth
- 0.1 - 0.2: Light
- 0.2 - 0.4: Moderate
- 0.4 - 0.6: Severe
- > 0.6: Extreme

Relation to vertical acceleration:
    Δn ≈ 0.5 × (ε/ε_ref)^(2/3)

Where Δn is acceleration in g, ε_ref ≈ 0.05 m²/s³
""")

def ellrod_ti1(vws, stretching_def, shearing_def, convergence):
    """
    Ellrod Turbulence Index 1.

    TI1 = VWS × (DEF + CVG)
    """
    deformation = np.sqrt(stretching_def**2 + shearing_def**2)
    return vws * (deformation + abs(convergence))

def ellrod_ti2(vws, stretching_def, shearing_def):
    """
    Ellrod Turbulence Index 2 (without convergence).

    TI2 = VWS × DEF
    """
    deformation = np.sqrt(stretching_def**2 + shearing_def**2)
    return vws * deformation

def edr_to_severity(edr):
    """Convert EDR to turbulence severity category."""
    if edr < 0.1:
        return "Smooth"
    elif edr < 0.2:
        return "Light"
    elif edr < 0.4:
        return "Moderate"
    elif edr < 0.6:
        return "Severe"
    else:
        return "Extreme"

def edr_to_acceleration(edr):
    """Approximate vertical acceleration from EDR."""
    return 0.5 * (edr / 0.05)**(2/3)

# EDR examples
print("\nEDR to Turbulence Severity:")
print("-" * 60)
print(f"{'EDR (m²/s³)':<15} {'Severity':<15} {'Approx accel (g)'}")
print("-" * 60)

for edr in [0.02, 0.05, 0.1, 0.15, 0.25, 0.4, 0.6, 0.8]:
    severity = edr_to_severity(edr)
    accel = edr_to_acceleration(edr)
    print(f"{edr:<15.2f} {severity:<15} {accel:<.2f}")

# =============================================================================
# PART 6: CONVECTIVELY INDUCED TURBULENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: CONVECTIVELY INDUCED TURBULENCE")
print("=" * 70)

print("""
HYPOTHESIS: Convective storms generate turbulence that extends well beyond
the visible cloud boundaries into clear air.

MECHANISMS:

1. ABOVE-CLOUD TURBULENCE:
   - Overshooting tops penetrate stratosphere
   - Gravity waves generated at anvil top
   - Can extend 50-100 km from visible cloud
   - Most hazardous because unexpected

2. ANVIL TURBULENCE:
   - Within/near anvil cloud
   - Strong updrafts/downdrafts
   - Associated with ice crystals (not truly "clear air")

3. NEAR-CLOUD TURBULENCE:
   - Enhanced shear at cloud edges
   - Gravity wave breaking
   - Extends 20-40 km from cloud

4. BELOW-CLOUD TURBULENCE:
   - Downdrafts and microbursts
   - Low-level wind shear
   - Most dangerous for takeoff/landing

GRAVITY WAVE TURBULENCE FROM CONVECTION:

Convective updrafts excite gravity waves that propagate away.
Wave breaking can occur at multiple levels:
- Near cloud top
- At tropopause
- In stratosphere

RECOMMENDED AVOIDANCE:
- 20 nm (37 km) lateral from severe storms
- 5,000 ft (1.5 km) above cloud top
- Do not fly under anvil
""")

def above_cloud_turbulence_extent(cloud_top_km, tropopause_km):
    """
    Estimate turbulence extent above penetrating convection.

    If cloud penetrates tropopause, gravity wave breaking likely.
    """
    penetration = cloud_top_km - tropopause_km
    if penetration > 0:
        # Significant above-cloud turbulence likely
        vert_extent = penetration + 2  # km above cloud
        horiz_extent = 50 + 10 * penetration  # km from cloud
        return vert_extent, horiz_extent
    return 0, 0

print("\nAbove-Cloud Turbulence Extent:")
print("-" * 50)
print(f"{'Cloud top':<12} {'Tropopause':<12} {'Vert extent':<15} {'Horiz extent'}")
print("-" * 50)

for ct in [10, 12, 14, 16]:
    for trop in [11, 12, 13]:
        ve, he = above_cloud_turbulence_extent(ct, trop)
        if ve > 0:
            print(f"{ct} km        {trop} km        {ve:.0f} km          {he:.0f} km")

# =============================================================================
# PART 7: CAT FORECASTING
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: CAT FORECASTING")
print("=" * 70)

print("""
HYPOTHESIS: Combining multiple indices with statistical post-processing
provides the best CAT forecasts.

FORECAST PRODUCTS:

1. GRAPHICAL TURBULENCE GUIDANCE (GTG):
   - NOAA/AWC operational product
   - Ensemble of 10+ indices
   - Machine learning calibration
   - 3D grid, updated hourly
   - Best available skill

2. TURBULENCE SIGMETS:
   - Pilot reports + model guidance
   - Valid for specific regions
   - Updated as needed

3. WORLD AREA FORECAST SYSTEM (WAFS):
   - ICAO global product
   - ECMWF and UK Met Office
   - 6-hour forecasts

VERIFICATION METRICS:

1. Probability of Detection (POD):
   POD = hits / (hits + misses)
   Current GTG: POD ≈ 0.7-0.8 for moderate+

2. False Alarm Rate (FAR):
   FAR = false alarms / (hits + false alarms)
   Current GTG: FAR ≈ 0.4-0.5

3. Critical Success Index (CSI):
   CSI = hits / (hits + misses + false alarms)
   Current GTG: CSI ≈ 0.3-0.4

LIMITATIONS:
- Small-scale turbulence hard to predict
- Convectively induced turbulence highly uncertain
- Mountain wave timing difficult
- Pilot reports essential for nowcasting
""")

def gtg_composite_index(ti1, ti2, ri, vws, n_squared):
    """
    Simplified GTG-like composite index.

    Real GTG uses machine learning on many indices.
    """
    # Normalize components
    ti_norm = (ti1 + ti2) / 20
    ri_factor = 1 / (1 + ri)  # High for low Ri
    vws_norm = vws / 0.02
    stability_factor = 0.02 / np.sqrt(max(n_squared, 0.0001))

    # Weighted combination (simplified)
    gtg = 0.3 * ti_norm + 0.3 * ri_factor + 0.2 * vws_norm + 0.2 * stability_factor

    return gtg

def gtg_to_probability(gtg_index):
    """Convert GTG index to turbulence probability."""
    # Simplified logistic-like conversion
    prob = 1 / (1 + np.exp(-3 * (gtg_index - 0.5)))
    return prob

print("\nGTG Performance Statistics:")
print("-" * 50)
print(f"{'Intensity':<15} {'POD':<10} {'FAR':<10} {'CSI'}")
print("-" * 50)
print(f"{'Light+':<15} {'0.85':<10} {'0.60':<10} {'0.35'}")
print(f"{'Moderate+':<15} {'0.75':<10} {'0.45':<10} {'0.40'}")
print(f"{'Severe+':<15} {'0.60':<10} {'0.30':<10} {'0.45'}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("CLEAR AIR TURBULENCE: SUMMARY")
print("=" * 70)

print("""
FUNDAMENTAL RESULTS:

1. RICHARDSON NUMBER:
   Ri = N² / S² < 1/4 → KH instability → turbulence
   Balance of stability vs shear

2. KELVIN-HELMHOLTZ INSTABILITY:
   Wavelength ≈ 7 × shear layer thickness
   Growth time ≈ 5-10 minutes
   Billows break → turbulence

3. JET STREAM TURBULENCE:
   Cyclonic side (left in NH) most turbulent
   Above jet core (strong vertical shear)
   Entrance/exit regions (ageostrophic circulation)

4. MOUNTAIN WAVE TURBULENCE:
   λ_z = 2πU/N (vertical wavelength)
   Amplitude grows with altitude
   Breaking at critical levels → severe turbulence

5. TURBULENCE INDICES:
   Ellrod TI = VWS × (DEF + CVG)
   GTG = ensemble of multiple indices
   EDR = physical measure of intensity

6. CONVECTIVELY INDUCED:
   Extends 20-50 km from visible cloud
   Above-cloud most hazardous
   Gravity wave breaking mechanism

7. FORECASTING:
   POD ≈ 0.7-0.8, FAR ≈ 0.4-0.5
   GTG best operational product
   Pilot reports essential supplement

AVIATION SAFETY:
CAT causes ~60% of weather-related injuries
Most are preventable with good forecasts + pilot awareness
Severe CAT encounters: ~1 per 100,000 flight hours

Z² = 32π/3 CONNECTION:
Hurricane outflow generates significant CAT at cruise altitudes.
The efficiency of the heat engine (Z² framework) determines
the strength of the outflow jet and associated turbulence.
""")

print("\nScript completed successfully.")
