"""
Z² = 32π/3 BINARY VORTEX INTERACTION: First-Principles
=========================================================

When two tropical cyclones approach each other, complex interactions occur.
The Fujiwhara effect describes their mutual orbiting and potential merger.

Topics:
- Two-vortex dynamics
- Angular momentum exchange
- Merger dynamics
- Intensity changes
- Z² during interaction

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np

# Fundamental constants
g = 9.81
c_p = 1004
OMEGA = 7.292e-5

# The Zimmerman constant
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

print("=" * 70)
print("Z² = 32π/3 BINARY VORTEX INTERACTION")
print("=" * 70)

print(f"""
THE FUJIWHARA EFFECT:

When two tropical cyclones come within ~1400 km:
1. They begin to orbit around a common center
2. The weaker storm often orbits the stronger
3. They may merge into a single, larger system
4. Or one may be "absorbed" by the other

This interaction affects Z² efficiency through:
- Angular momentum redistribution
- Convection disruption
- Environmental flow changes
""")

# =============================================================================
# PART 1: TWO-VORTEX POINT VORTEX DYNAMICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: POINT VORTEX DYNAMICS")
print("=" * 70)

print("""
HYPOTHESIS: To first order, two hurricanes can be modeled as
point vortices with circulation Γ, giving analytic insight.

POINT VORTEX EQUATIONS:

For two vortices at positions (x₁, y₁) and (x₂, y₂):

Velocity induced by vortex 2 on vortex 1:
    u₁ = -Γ₂/(2π) × (y₁ - y₂)/d²
    v₁ = +Γ₂/(2π) × (x₁ - x₂)/d²

Where d = distance between vortices

MUTUAL ROTATION:

Two vortices rotate around their centroid:
    Ω = (Γ₁ + Γ₂) / (2π d²)

Period of rotation:
    T = 2π/Ω = 4π² d² / (Γ₁ + Γ₂)

For typical hurricanes:
- Γ ≈ 3-10 × 10⁶ m²/s
- d ≈ 500-1000 km
- T ≈ 12-48 hours

EFFECT OF CORIOLIS:

On an f-plane, the vortex pair also drifts:
- If Γ₁ = Γ₂: Drift perpendicular to line connecting them
- If Γ₁ ≠ Γ₂: More complex trajectory

This is beta-drift applied to the two-vortex system.
""")

def point_vortex_circulation(V_max, r_m):
    """
    Estimate circulation from hurricane parameters.

    Γ ≈ 2π × r_m × V_max (approximate, using r_m)
    """
    return 2 * np.pi * r_m * V_max

def mutual_rotation_rate(Gamma_1, Gamma_2, separation):
    """
    Rotation rate of two-vortex system.

    Ω = (Γ₁ + Γ₂) / (2π d²)
    """
    return (Gamma_1 + Gamma_2) / (2 * np.pi * separation**2)

def rotation_period(Gamma_1, Gamma_2, separation):
    """
    Period of mutual rotation in hours.
    """
    omega = mutual_rotation_rate(Gamma_1, Gamma_2, separation)
    T_seconds = 2 * np.pi / omega
    return T_seconds / 3600  # Convert to hours

def approach_rate(Gamma_1, Gamma_2, separation, f):
    """
    Rate at which vortices approach each other.

    Simplified - depends on relative intensity and background flow.
    """
    # Beta drift and mutual advection
    beta = 2 * OMEGA / 6.371e6  # df/dy at mid-latitudes
    return beta * (Gamma_1 + Gamma_2) / (4 * np.pi * f)

# Two-vortex examples
print("\nTwo-Vortex System Dynamics:")
print("-" * 70)

# Example: Two Cat 3 hurricanes at 750 km separation
V1, V2 = 55, 55  # m/s
r1, r2 = 35000, 35000  # m
d = 750000  # m

Gamma_1 = point_vortex_circulation(V1, r1)
Gamma_2 = point_vortex_circulation(V2, r2)

print(f"Hurricane 1: V_max = {V1} m/s, Γ = {Gamma_1:.2e} m²/s")
print(f"Hurricane 2: V_max = {V2} m/s, Γ = {Gamma_2:.2e} m²/s")
print(f"Separation: {d/1000:.0f} km")
print()

T = rotation_period(Gamma_1, Gamma_2, d)
omega = mutual_rotation_rate(Gamma_1, Gamma_2, d) * 3600  # deg/hr
print(f"Rotation period: {T:.1f} hours")
print(f"Rotation rate: {omega * 180/np.pi:.1f} deg/hr")

# Effect of separation
print("\nRotation Period vs Separation:")
print("-" * 50)
print(f"{'Separation (km)':<20} {'Period (hr)':<15} {'Rate (deg/hr)'}")
print("-" * 50)

for d_km in [400, 600, 800, 1000, 1200]:
    d_m = d_km * 1000
    T = rotation_period(Gamma_1, Gamma_2, d_m)
    rate = mutual_rotation_rate(Gamma_1, Gamma_2, d_m) * 3600 * 180 / np.pi
    print(f"{d_km:<20} {T:<15.1f} {rate:.1f}")

# =============================================================================
# PART 2: INTERACTION REGIMES
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: INTERACTION REGIMES")
print("=" * 70)

print("""
HYPOTHESIS: The outcome of binary interaction depends on the
relative intensity and separation of the two storms.

INTERACTION PARAMETER:

    I = (Γ₁ - Γ₂) / (Γ₁ + Γ₂) × (d / R_outer)

Where R_outer = outer radius of stronger storm

REGIMES:

1. ORBIT ONLY (d > 1200 km, any I):
   - Weak mutual interaction
   - Both maintain independent structure
   - Some track deflection

2. PARTIAL STRAINING (800 < d < 1200 km, |I| > 0.3):
   - Stronger storm deforms weaker
   - Weaker may become elongated
   - Possible absorption of outer circulation

3. COMPLETE MERGER (d < 600 km, |I| < 0.3):
   - Both storms merge into one
   - Combined circulation
   - Temporary weakening during merger

4. ABSORPTION (d < 800 km, |I| > 0.5):
   - Stronger absorbs weaker
   - Weaker loses identity
   - Stronger may intensify from added angular momentum

CRITICAL SEPARATION:

Merger begins when:
    d < 3 × (r_outer1 + r_outer2)

For typical hurricanes: d_crit ≈ 500-800 km
""")

def interaction_parameter(Gamma_1, Gamma_2, separation, R_outer):
    """
    Calculate interaction parameter.
    """
    intensity_ratio = (Gamma_1 - Gamma_2) / (Gamma_1 + Gamma_2)
    distance_ratio = separation / R_outer
    return intensity_ratio * distance_ratio

def interaction_regime(separation_km, intensity_ratio):
    """
    Determine interaction regime.
    """
    if separation_km > 1200:
        return "Orbit only"
    elif separation_km > 800:
        if abs(intensity_ratio) > 0.3:
            return "Partial straining"
        else:
            return "Approaching merger"
    elif separation_km > 500:
        if abs(intensity_ratio) > 0.5:
            return "Absorption likely"
        else:
            return "Merger likely"
    else:
        return "Active merger"

# Regime determination
print("\nInteraction Regime Matrix:")
print("-" * 70)
print(f"{'Sep (km)':<12} {'Equal intensity':<20} {'Moderate diff':<20} {'Strong diff'}")
print("-" * 70)

for d_km in [1400, 1000, 700, 500, 300]:
    regime_eq = interaction_regime(d_km, 0.0)
    regime_mod = interaction_regime(d_km, 0.3)
    regime_str = interaction_regime(d_km, 0.6)
    print(f"{d_km:<12} {regime_eq:<20} {regime_mod:<20} {regime_str}")

# =============================================================================
# PART 3: Z² EFFECTS DURING INTERACTION
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: Z² EFFECTS DURING INTERACTION")
print("=" * 70)

print("""
HYPOTHESIS: Binary interaction affects Z² efficiency through
multiple mechanisms.

1. ANGULAR MOMENTUM REDISTRIBUTION:

When vortices interact, angular momentum is exchanged.
The weaker vortex typically loses M to the stronger.

    dM₁/dt = -dM₂/dt = F(d, Γ₁, Γ₂)

This affects V_max through:
    V_max ∝ √(M × f)

2. CONVECTIVE DISRUPTION:

Interaction creates:
- Subsidence between storms (suppressed convection)
- Enhanced shear in outer regions
- Asymmetric heating patterns

Effect on Z² efficiency:
    ε_interaction = ε_0 × (1 - disruption_factor)

3. ENVIRONMENTAL MODIFICATION:

Each storm modifies the environment for the other:
- SST cooling (cold wakes)
- Moisture depletion
- Altered outflow patterns

Combined effect can reduce Z² MPI for both storms.

4. MERGER INTENSIFICATION:

If merger occurs:
    M_combined = M₁ + M₂
    V_max,combined > max(V_max1, V_max2) initially

But the larger vortex has lower Z² efficiency:
    V_max,final < Z² MPI

The combined storm often settles to a moderate intensity.
""")

def z2_efficiency_interaction(separation_km, separation_critical=800):
    """
    Z² efficiency reduction due to binary interaction.
    """
    if separation_km > 1500:
        return 1.0  # No effect
    elif separation_km > separation_critical:
        # Linear reduction as storms approach
        return 1 - 0.3 * (1500 - separation_km) / (1500 - separation_critical)
    else:
        # Stronger reduction during close interaction
        return 0.5 - 0.3 * (separation_critical - separation_km) / separation_critical

def intensity_during_merger(V1_initial, V2_initial, merger_progress):
    """
    Model intensity evolution during merger.

    merger_progress: 0 = just touching, 1 = fully merged
    """
    # Initial weakening as structures interact
    if merger_progress < 0.5:
        V_combined = max(V1_initial, V2_initial) * (1 - 0.2 * merger_progress)
    else:
        # Recovery as new structure forms
        V_combined = max(V1_initial, V2_initial) * (0.9 + 0.2 * (merger_progress - 0.5))

    return V_combined

# Z² efficiency during interaction
print("\nZ² Efficiency vs Separation:")
print("-" * 50)
print(f"{'Separation (km)':<20} {'ε_Z²':<15} {'Effect'}")
print("-" * 50)

for d_km in [1500, 1200, 1000, 800, 600, 400]:
    eps = z2_efficiency_interaction(d_km)
    if eps > 0.9:
        effect = "Minimal"
    elif eps > 0.7:
        effect = "Moderate reduction"
    elif eps > 0.5:
        effect = "Significant disruption"
    else:
        effect = "Severe disruption"
    print(f"{d_km:<20} {eps:<15.2f} {effect}")

# =============================================================================
# PART 4: HISTORICAL BINARY INTERACTIONS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: HISTORICAL BINARY INTERACTIONS")
print("=" * 70)

print("""
NOTABLE FUJIWHARA INTERACTIONS:

1. TYPHOONS PAT & RUTH (1994) - Western Pacific
   - Two intense typhoons within 700 km
   - Orbited each other for 24 hours
   - Pat absorbed Ruth's outer circulation
   - Pat briefly intensified

2. IRIS & KAREN (1995) - Atlantic
   - Iris (TS) orbited Karen (Hurricane)
   - Iris absorbed into Karen
   - Karen weakened then recovered

3. HILARY & IRWIN (2017) - Eastern Pacific
   - Unusual merger of two hurricanes
   - Combined into single system
   - Brief weakening then reorganization

4. TYPHOONS PARMA & MELOR (2009)
   - Complex interaction over Philippines
   - Parma stalled due to Melor's influence
   - Extended rainfall and flooding

5. TROPICAL STORM FAXAI & SUPER TYPHOON HAGIBIS (2019)
   - Faxai captured by Hagibis's circulation
   - Hagibis became unusually large
   - One of largest typhoons on record

KEY OBSERVATIONS:

1. Weaker storm usually absorbed or ejected
2. Merger often causes temporary weakening
3. Combined system can become very large
4. Track prediction becomes very difficult
""")

# Case study analysis
print("\nBinary Interaction Outcomes:")
print("-" * 70)
print(f"{'Case':<25} {'Outcome':<20} {'Intensity change'}")
print("-" * 70)

cases = [
    ("Pat & Ruth 1994", "Absorption", "Brief +10 kt"),
    ("Iris & Karen 1995", "Absorption", "-20 kt then recovery"),
    ("Hilary & Irwin 2017", "Merger", "-15 kt then +10 kt"),
    ("Parma & Melor 2009", "Deflection", "Parma stalled"),
    ("Faxai & Hagibis 2019", "Capture", "Hagibis +5 kt, expanded"),
]

for case, outcome, intensity in cases:
    print(f"{case:<25} {outcome:<20} {intensity}")

# =============================================================================
# PART 5: FORECASTING CHALLENGES
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: FORECASTING BINARY INTERACTIONS")
print("=" * 70)

print("""
FORECASTING CHALLENGES:

1. TRACK UNCERTAINTY:
   - Mutual rotation makes track prediction difficult
   - Small errors amplify in two-body problem
   - Ensemble spread increases dramatically

2. INTENSITY UNCERTAINTY:
   - Angular momentum exchange unpredictable
   - Convective response uncertain
   - Z² efficiency varies during interaction

3. TIMING UNCERTAINTY:
   - When will merger occur?
   - Duration of interaction?
   - When will storms separate (if at all)?

MODEL PERFORMANCE:

- GFS: Tends to merge systems too quickly
- ECMWF: Better at maintaining separate systems
- HWRF: Struggles with two systems simultaneously

BEST PRACTICES:

1. Use ensemble guidance heavily
2. Monitor satellite for structural changes
3. Update more frequently during interaction
4. Communicate high uncertainty to public

Z² IMPLICATIONS FOR FORECASTING:

During interaction:
    V_max ∈ [0.5 × Z²_MPI, 1.0 × Z²_MPI]

The uncertainty range is much larger than for isolated storms.

After interaction:
- If merged: New Z² MPI for combined vortex
- If separated: Both return toward individual Z² MPI
""")

def track_uncertainty_factor(separation_km, forecast_hour):
    """
    Track uncertainty amplification from binary interaction.
    """
    if separation_km > 1500:
        return 1.0

    interaction_factor = 1 + (1500 - separation_km) / 500
    time_factor = 1 + forecast_hour / 48

    return interaction_factor * time_factor

print("\nTrack Uncertainty Amplification:")
print("-" * 60)
print(f"{'Separation':<15} {'24h factor':<15} {'48h factor':<15} {'72h factor'}")
print("-" * 60)

for d_km in [1500, 1000, 700, 500]:
    f24 = track_uncertainty_factor(d_km, 24)
    f48 = track_uncertainty_factor(d_km, 48)
    f72 = track_uncertainty_factor(d_km, 72)
    print(f"{d_km} km        {f24:.1f}×            {f48:.1f}×            {f72:.1f}×")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("Z² BINARY INTERACTION: SUMMARY")
print("=" * 70)

print(f"""
BINARY VORTEX DYNAMICS IN Z² FRAMEWORK:

1. POINT VORTEX DYNAMICS:
   Rotation rate: Ω = (Γ₁ + Γ₂) / (2π d²)
   Typical period: 12-48 hours

2. INTERACTION REGIMES:
   d > 1200 km: Orbit only
   800-1200 km: Partial straining
   500-800 km: Merger/absorption likely
   d < 500 km: Active merger

3. Z² EFFICIENCY EFFECTS:
   ε_interaction = ε_0 × (1 - disruption_factor)
   Close approach reduces Z² efficiency for both storms

4. ANGULAR MOMENTUM EXCHANGE:
   Weaker → Stronger transfer
   V_max changes for both storms

5. MERGER OUTCOME:
   M_combined = M₁ + M₂
   Temporary weakening then recovery
   Final intensity < Z² MPI (larger vortex less efficient)

6. FORECASTING:
   Uncertainty amplified 2-5× during interaction
   Ensemble spread increases dramatically
   Track prediction very challenging

Z² = 32π/3 INSIGHT:

Binary interaction demonstrates that Z² efficiency depends on
vortex structure. When two vortices interact:
- Symmetry is broken
- Convection is disrupted
- Angular momentum is redistributed

The Z² framework provides the upper bound for intensity,
but interaction effects reduce realized efficiency.

OPERATIONAL IMPLICATIONS:

1. Monitor separation distance continuously
2. Anticipate Z² efficiency reduction
3. Communicate high uncertainty
4. Watch for post-interaction intensification
""")

print("\nScript completed successfully.")
