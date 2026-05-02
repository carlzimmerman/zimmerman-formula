"""
Z² = 32π/3 EXTRATROPICAL TRANSITION: First-Principles
========================================================

When hurricanes move poleward, they undergo extratropical transition (ET),
transforming from a warm-core Z² heat engine to a cold-core baroclinic system.

Topics:
- Structural transformation
- Energy source transition
- Z² decay and baroclinic amplification
- Post-tropical impacts
- Reintensification cases

Author: Carl Zimmerman
Framework: Z² = 32π/3 hurricane intensity research
"""

import numpy as np

# Fundamental constants
g = 9.81
c_p = 1004
L_v = 2.5e6
R_d = 287.05
OMEGA = 7.292e-5

# The Zimmerman constant
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

print("=" * 70)
print("Z² = 32π/3 EXTRATROPICAL TRANSITION")
print("=" * 70)

print(f"""
EXTRATROPICAL TRANSITION (ET):

The end of Z² efficiency occurs when:
1. SST drops below ~26°C (fuel cutoff)
2. Vertical wind shear increases (structure disruption)
3. Baroclinic zone interaction (new energy source)

~40-50% of Atlantic hurricanes undergo ET.
Post-ET storms can be MORE dangerous than tropical phase!
""")

# =============================================================================
# PART 1: THE STRUCTURAL TRANSFORMATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: STRUCTURAL TRANSFORMATION")
print("=" * 70)

print("""
HYPOTHESIS: During ET, the warm-core symmetric structure transforms
into a cold-core asymmetric baroclinic system.

TROPICAL STRUCTURE (Z² regime):
- Warm core (ΔT > 0 at center)
- Symmetric wind field
- Energy from ocean (enthalpy flux)
- Axisymmetric convection
- Z² efficiency: High (0.8-1.0)

EXTRATROPICAL STRUCTURE:
- Cold core (ΔT < 0 at center)
- Asymmetric wind field
- Energy from baroclinicity (thermal wind)
- Frontal precipitation
- Z² efficiency: Zero (different physics)

TRANSFORMATION PROCESS:

1. ONSET PHASE (0-24 hours):
   - Storm enters baroclinic zone
   - SST drops below threshold
   - Frontal structure begins developing
   - Asymmetries grow

2. COMPLETION PHASE (24-48 hours):
   - Warm core erodes
   - Fronts fully developed
   - Cold core established
   - Now an extratropical cyclone

STRUCTURAL METRICS:

1. Thermal symmetry parameter B:
   B = (Z_900 - Z_600)_R - (Z_900 - Z_600)_L

   B < 10 m: Symmetric (tropical)
   B > 10 m: Asymmetric (extratropical)

2. Thermal wind parameter -V_T^L:
   -V_T^L < 0: Warm core
   -V_T^L > 0: Cold core
""")

def thermal_symmetry_B(thickness_right, thickness_left):
    """
    Calculate thermal symmetry parameter B.

    B = (Z_900 - Z_600)_R - (Z_900 - Z_600)_L

    Returns B in meters.
    """
    return thickness_right - thickness_left

def thermal_wind_parameter(T_center, T_environment, p_upper=600, p_lower=900):
    """
    Simplified thermal wind parameter.

    Warm core: T_center > T_environment → negative V_T
    Cold core: T_center < T_environment → positive V_T
    """
    delta_T = T_center - T_environment
    return -delta_T

def et_phase(B, V_T_lower):
    """
    Determine ET phase from structural parameters.
    """
    if B < 10 and V_T_lower < 0:
        return "Tropical"
    elif B >= 10 and V_T_lower < 0:
        return "Onset"
    elif B >= 10 and V_T_lower >= 0:
        return "Completion"
    else:
        return "Complex"

# Demonstrate ET phases
print("\nET Phase Classification:")
print("-" * 60)
print(f"{'B (m)':<12} {'V_T':<12} {'Core type':<15} {'Phase'}")
print("-" * 60)

cases = [
    (5, -10, "Warm"),
    (15, -5, "Warm"),
    (25, 0, "Neutral"),
    (30, 5, "Cold"),
    (35, 10, "Cold"),
]

for B, V_T, core in cases:
    phase = et_phase(B, V_T)
    print(f"{B:<12} {V_T:<12} {core:<15} {phase}")

# =============================================================================
# PART 2: ENERGY SOURCE TRANSITION
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: ENERGY SOURCE TRANSITION")
print("=" * 70)

print("""
HYPOTHESIS: During ET, the energy source transitions from latent heat
release (Z² framework) to baroclinic conversion.

Z² ENERGY SOURCE (TROPICAL):

    Ė_Z² = Z² × η × F_enthalpy

Where:
- η = Carnot efficiency
- F_enthalpy = surface enthalpy flux

This requires:
- SST > 26°C
- Low vertical wind shear
- Symmetric structure

BAROCLINIC ENERGY SOURCE (EXTRATROPICAL):

    Ė_baroclinic = ∫∫ (-ω × α) dA dp

Where:
- ω = vertical velocity in pressure coords
- α = specific volume
- Warm air rising, cold air sinking

AVAILABLE POTENTIAL ENERGY (APE):

    APE ∝ ∫∫ (T')² / σ dA

Where T' = temperature anomaly, σ = static stability

CONVERSION:
    APE → KE through baroclinic instability

THE TRANSITION:

Time 0:  Z² dominant, baroclinic weak
Time 12h: Z² weakening, baroclinic growing
Time 24h: Z² minimal, baroclinic dominant
Time 36h: Fully baroclinic system

KEY INSIGHT:

If baroclinic energy > Z² energy at SST threshold:
    → Storm maintains or increases intensity

If baroclinic energy < Z² energy:
    → Storm weakens during transition
""")

def z_squared_energy_rate(V_max, T_s, T_out):
    """
    Estimate Z² energy generation rate.
    """
    eta = (T_s - T_out) / T_s
    # Proportional to V_max² (kinetic energy)
    return V_max**2 * eta

def baroclinic_energy_rate(thermal_gradient, jet_strength, latitude):
    """
    Estimate baroclinic energy generation rate.

    Proportional to thermal gradient and jet strength.
    """
    f = 2 * OMEGA * np.sin(np.radians(latitude))
    # Simplified: E_baroclinic ∝ f × |∇T| × V_jet
    return f * thermal_gradient * jet_strength

def energy_ratio_during_et(t_hours, et_start=0, transition_time=24):
    """
    Model the Z² to baroclinic energy transition.
    """
    if t_hours < et_start:
        z2_fraction = 1.0
    elif t_hours > et_start + transition_time:
        z2_fraction = 0.0
    else:
        # Linear transition
        z2_fraction = 1 - (t_hours - et_start) / transition_time

    return z2_fraction, 1 - z2_fraction

# Energy transition
print("\nEnergy Source Transition During ET:")
print("-" * 60)
print(f"{'Time (hr)':<12} {'Z² fraction':<15} {'Baroclinic':<15} {'Dominant'}")
print("-" * 60)

for t in range(0, 49, 6):
    z2_frac, baro_frac = energy_ratio_during_et(t, et_start=0, transition_time=36)
    dominant = "Z²" if z2_frac > 0.5 else "Baroclinic"
    print(f"{t:<12} {z2_frac:<15.2f} {baro_frac:<15.2f} {dominant}")

# =============================================================================
# PART 3: Z² DECAY PROCESS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: Z² EFFICIENCY DECAY")
print("=" * 70)

print("""
HYPOTHESIS: Z² efficiency decays as the storm moves over cooler water
and encounters vertical wind shear.

SST EFFECT ON Z²:

Recall: V_max² = Z² × η(T_s) × Δk(T_s) / c_p

As T_s decreases:
1. η decreases (lower Carnot efficiency)
2. Δk decreases (less enthalpy disequilibrium)
3. Both effects reduce V_max

Below ~26°C: Z² framework no longer applies
(Ocean cannot provide sufficient enthalpy)

SHEAR EFFECT ON Z²:

Vertical wind shear disrupts the Z² efficiency through:

1. Ventilation: Advects warm core away from center
2. Tilt: Displaces upper and lower circulations
3. Asymmetry: Breaks axisymmetric structure

Effective Z² with shear:
    Z²_eff = Z² × exp(-shear/shear_critical)

Where shear_critical ≈ 10-15 m/s

COMBINED DECAY:

    ε(t) = ε_sst(t) × ε_shear(t)

    V_max(t) = √(ε(t) × Z² × thermo_terms)

Intensity decays as both factors worsen.
""")

def z2_efficiency_sst(T_s, T_threshold=26):
    """
    Z² efficiency factor from SST.

    Above threshold: 1.0
    Below threshold: Decays exponentially
    """
    if T_s >= T_threshold:
        return 1.0
    else:
        return np.exp(-(T_threshold - T_s) / 3)

def z2_efficiency_shear(shear_ms, shear_critical=12):
    """
    Z² efficiency factor from vertical wind shear.
    """
    return np.exp(-shear_ms / shear_critical)

def combined_z2_efficiency(T_s, shear_ms, T_threshold=26, shear_critical=12):
    """
    Combined Z² efficiency from SST and shear.
    """
    eps_sst = z2_efficiency_sst(T_s, T_threshold)
    eps_shear = z2_efficiency_shear(shear_ms, shear_critical)
    return eps_sst * eps_shear

# Z² decay during ET
print("\nZ² Efficiency Decay:")
print("-" * 60)
print(f"{'SST (°C)':<12} {'Shear (m/s)':<15} {'ε_sst':<12} {'ε_shear':<12} {'ε_total'}")
print("-" * 60)

for T_s in [28, 26, 24, 22, 20]:
    for shear in [5, 10, 15, 20]:
        eps = combined_z2_efficiency(T_s, shear)
        eps_sst = z2_efficiency_sst(T_s)
        eps_shear = z2_efficiency_shear(shear)
        print(f"{T_s:<12} {shear:<15} {eps_sst:<12.2f} {eps_shear:<12.2f} {eps:.2f}")

# =============================================================================
# PART 4: BAROCLINIC REINTENSIFICATION
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: BAROCLINIC REINTENSIFICATION")
print("=" * 70)

print("""
HYPOTHESIS: Post-tropical storms can reintensify through baroclinic
processes, sometimes becoming more powerful than their tropical phase.

REINTENSIFICATION MECHANISM:

1. Storm encounters strong jet stream
2. Upper-level divergence enhances lift
3. Baroclinic energy extraction accelerates
4. Central pressure drops, winds increase

NECESSARY CONDITIONS:

1. Strong thermal gradient (polar front)
2. Jet stream interaction (favorable diffluence)
3. Residual moisture from tropical phase
4. Surface flux over warm Gulf Stream

CASE STUDIES:

Hurricane Sandy (2012):
- Tropical V_max: 110 kt
- Post-tropical V_max: 90 kt (maintained)
- Size expanded dramatically
- $65 billion damage

Hurricane Hazel (1954):
- Tropical V_max: 150 kt
- Maintained hurricane intensity to Toronto!
- Merged with frontal system

Super Typhoon Nuri (2014):
- Rapidly transitioned to intense extratropical
- Central pressure: 924 hPa as extratropical
- Disrupted jet stream across hemisphere

DANGER OF POST-TROPICAL STORMS:

1. Larger wind field (more area affected)
2. Faster forward speed (less warning time)
3. Cold core = stronger winds at surface
4. Heavy rainfall continues (moisture supply)
5. Still can have hurricane-force winds
""")

def baroclinic_intensification_potential(thermal_gradient_K_per_1000km,
                                         jet_strength_ms,
                                         moisture_factor):
    """
    Estimate baroclinic intensification potential.
    """
    # Stronger gradient and jet = more potential
    potential = thermal_gradient_K_per_1000km * jet_strength_ms * moisture_factor / 1000
    return potential

def post_tropical_central_pressure(pre_et_pressure, baroclinic_potential,
                                   time_hours, max_drop=50):
    """
    Estimate post-tropical pressure evolution.
    """
    # Initial adjustment then potential deepening
    adjustment = 10  # Typically rises ~10 hPa initially

    if baroclinic_potential > 0.5:
        # Reintensification
        deepening = min(baroclinic_potential * time_hours, max_drop)
        return pre_et_pressure + adjustment - deepening
    else:
        # Gradual fill
        return pre_et_pressure + adjustment + time_hours * 0.5

# Reintensification scenarios
print("\nPost-Tropical Evolution Scenarios:")
print("-" * 70)

scenarios = [
    ("Weak baro.", 950, 5, 30, 0.3),
    ("Moderate baro.", 960, 10, 50, 0.5),
    ("Strong baro.", 940, 15, 70, 0.8),
    ("Sandy-like", 945, 12, 60, 0.7),
]

print(f"{'Scenario':<15} {'p_trop':<10} {'Gradient':<12} {'Jet':<8} {'p at 24h':<12} {'Trend'}")
print("-" * 70)

for name, p_trop, grad, jet, moist in scenarios:
    baro_pot = baroclinic_intensification_potential(grad, jet, moist)
    p_24h = post_tropical_central_pressure(p_trop, baro_pot, 24)
    trend = "Deepening" if p_24h < p_trop else "Filling"
    print(f"{name:<15} {p_trop:<10} {grad} K/1000km  {jet} m/s {p_24h:<12.0f} {trend}")

# =============================================================================
# PART 5: ET IMPACTS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: IMPACTS OF TRANSITIONING STORMS")
print("=" * 70)

print("""
EXPANDED IMPACT AREA:

During and after ET:
1. Wind field expands 2-4× in radius
2. Hurricane-force winds at greater distances
3. Heavy rain over larger area
4. Longer duration of hazards

IMPACT COMPARISON:

                    Tropical Phase    Post-Tropical
Wind field radius   200 km            500-800 km
Forward speed       15-25 kt          30-50 kt
Rain rate          Intense, narrow    Moderate, broad
Storm surge        High, localized    Moderate, widespread
Duration at point  6-12 hours         12-24 hours

WHY ET STORMS ARE DANGEROUS:

1. PUBLIC PERCEPTION:
   "It's just post-tropical" → False sense of security

2. FORECAST CHALLENGES:
   Models struggle with hybrid systems
   Timing uncertainty increases

3. INFRASTRUCTURE:
   Northern regions less prepared for hurricane-force winds

4. COASTAL SURGE:
   Large wind field → extensive surge area
   Fast forward speed → less warning time

HISTORICAL ET IMPACTS:

- Hurricane Hazel (1954): 81 deaths in Canada
- Hurricane Agnes (1972): $3B damage from flooding
- Hurricane Juan (2003): Halifax, NS
- Hurricane Sandy (2012): $65B damage
- Hurricane Fiona (2022): Atlantic Canada devastation
""")

def wind_field_expansion_factor(et_progress):
    """
    Wind field expands during ET.

    et_progress: 0-1 (0=tropical, 1=fully ET)
    """
    return 1 + 2 * et_progress  # Up to 3× expansion

def impact_area_ratio(et_progress):
    """
    Area affected grows as square of radius.
    """
    r_factor = wind_field_expansion_factor(et_progress)
    return r_factor**2

print("\nWind Field Expansion During ET:")
print("-" * 50)
print(f"{'ET Progress':<15} {'R factor':<15} {'Area factor'}")
print("-" * 50)

for progress in [0, 0.25, 0.5, 0.75, 1.0]:
    r = wind_field_expansion_factor(progress)
    a = impact_area_ratio(progress)
    print(f"{progress:<15.2f} {r:<15.1f}× {a:.1f}×")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("Z² EXTRATROPICAL TRANSITION: SUMMARY")
print("=" * 70)

print(f"""
ET IN THE Z² FRAMEWORK:

1. Z² REGIME END:
   SST < 26°C → Enthalpy flux insufficient
   Shear > 15 m/s → Structure disruption
   Z² efficiency decays exponentially

2. STRUCTURAL TRANSFORMATION:
   Warm core → Cold core
   Symmetric → Asymmetric
   Ocean-driven → Baroclinic

3. ENERGY TRANSITION:
   Ė_Z² = Z² × η × F_enthalpy (tropical)
   Ė_baro = ∫(-ω α) dA dp (extratropical)

   If Ė_baro > Ė_Z²: Reintensification possible

4. EFFICIENCY DECAY:
   ε_total = ε_sst × ε_shear
   Both factors worsen during ET

5. REINTENSIFICATION:
   Strong jet + thermal gradient → Baroclinic deepening
   Sandy: Maintained hurricane-force as post-tropical

6. EXPANDED IMPACTS:
   Wind field: 2-4× larger
   Area affected: 4-16× larger
   Northern regions vulnerable

KEY INSIGHT:

ET marks the end of Z² physics and the beginning of baroclinic physics.
The storm doesn't "die" - it transforms.

Post-tropical ≠ Post-dangerous!

FORECASTING IMPLICATIONS:

1. Track Z² efficiency decay (SST, shear)
2. Assess baroclinic potential (gradient, jet)
3. Predict timing of energy source transition
4. Communicate expanded hazards to public
""")

print("\nScript completed successfully.")
