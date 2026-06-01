#!/usr/bin/env python3
"""
CLIMATE FEEDBACKS - FIRST PRINCIPLES
=====================================

Deriving the physics of climate sensitivity, feedback
mechanisms, and the response to radiative forcing.
"""

import numpy as np

print("=" * 70)
print("CLIMATE FEEDBACKS - FIRST PRINCIPLES")
print("=" * 70)


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
sigma = 5.67e-8    # Stefan-Boltzmann constant (W/m²/K⁴)
S_0 = 1361         # Solar constant (W/m²)
T_0 = 288          # Reference Earth temperature (K)


# =============================================================================
# PART 1: CLIMATE SENSITIVITY FRAMEWORK
# =============================================================================
print("\n" + "=" * 70)
print("PART 1: CLIMATE SENSITIVITY FRAMEWORK")
print("=" * 70)

sensitivity_text = """
CLIMATE SENSITIVITY:
====================

How much does Earth warm for a given forcing?

RADIATIVE FORCING:

ΔF = change in net radiation at tropopause (W/m²)
Before surface temperature responds

CO₂ FORCING:

ΔF = 5.35 × ln(C/C₀) W/m²

For doubling: ΔF₂ₓ = 5.35 × ln(2) = 3.7 W/m²

CLIMATE RESPONSE:

ΔT = λ × ΔF

Where λ = climate sensitivity parameter (K/(W/m²))

Or: ΔT = ΔF / (-λ_total)

with λ_total = sum of feedbacks

EQUILIBRIUM CLIMATE SENSITIVITY (ECS):

ΔT for CO₂ doubling at equilibrium
IPCC AR6: 2.5-4.0°C (likely range)
Best estimate: ~3°C

TRANSIENT CLIMATE RESPONSE (TCR):

ΔT at time of CO₂ doubling (1%/yr increase)
IPCC AR6: 1.4-2.2°C (likely range)
Lower than ECS (ocean thermal inertia)

NO-FEEDBACK SENSITIVITY:

Without feedbacks (Planck response only):
λ₀ = 1/(4σT³) ≈ 0.27 K/(W/m²)

ΔT₀ = 0.27 × 3.7 ≈ 1.0°C for 2×CO₂

So feedbacks roughly TRIPLE the response!
"""
print(sensitivity_text)

def co2_forcing(C_ppm, C0_ppm=280):
    """
    Calculate CO₂ radiative forcing.

    ΔF = 5.35 × ln(C/C₀) W/m²
    """
    return 5.35 * np.log(C_ppm / C0_ppm)

def planck_sensitivity(T_kelvin=288):
    """
    No-feedback (Planck) climate sensitivity.

    λ₀ = 1/(4σT³)
    """
    return 1 / (4 * sigma * T_kelvin**3)

def temperature_response(forcing, sensitivity_parameter):
    """Calculate temperature response to forcing."""
    return sensitivity_parameter * forcing

print("\nCO₂ Forcing and Temperature Response:")
print("-" * 65)
print(f"{'CO₂ (ppm)':<12} {'ΔF (W/m²)':<15} {'ΔT (no feedback)':<20} {'ΔT (ECS~3°C)'}")
print("-" * 65)

lambda_0 = planck_sensitivity()
lambda_feedback = 0.81  # K/(W/m²) for ECS = 3°C

for co2 in [300, 350, 400, 450, 560, 700, 1000]:
    dF = co2_forcing(co2)
    dT_0 = temperature_response(dF, lambda_0)
    dT_fb = temperature_response(dF, lambda_feedback)
    print(f"{co2:<12} {dF:<15.2f} {dT_0:<20.1f} {dT_fb:.1f}")


# =============================================================================
# PART 2: FEEDBACK ANALYSIS
# =============================================================================
print("\n" + "=" * 70)
print("PART 2: FEEDBACK MATHEMATICS")
print("=" * 70)

feedback_text = """
FEEDBACK FORMALISM:
===================

ENERGY BALANCE:

C × dT/dt = ΔF + λ × ΔT

At equilibrium: ΔT_eq = -ΔF / λ

FEEDBACK DECOMPOSITION:

λ = λ₀ + Σλᵢ

Where:
- λ₀ = Planck feedback (~-3.2 W/m²/K)
- λᵢ = individual feedbacks

FEEDBACK FACTOR:

f = -λ₀ / λ = 1 / (1 - Σfᵢ)

Where fᵢ = -λᵢ / λ₀

If Σfᵢ < 1: Stable (damped)
If Σfᵢ > 1: Runaway (Venus!)

GAIN:

G = 1 / (1 - f)

For ECS = 3°C, G ≈ 3

SIGN CONVENTION:

λ < 0: Negative feedback (stabilizing)
λ > 0: Positive feedback (amplifying)

Planck is always NEGATIVE (more T → more emission)
Other feedbacks can be either sign

UNCERTAINTY:

Most uncertainty is in cloud feedback!
Cloud feedback: -0.5 to +1.5 W/m²/K
This dominates ECS uncertainty
"""
print(feedback_text)

def feedback_gain(feedback_sum, lambda_0=-3.2):
    """
    Calculate feedback gain.

    G = 1 / (1 - f)  where f = -Σλᵢ/λ₀
    """
    f = -feedback_sum / lambda_0
    if f >= 1:
        return float('inf')  # Runaway
    return 1 / (1 - f)

def ecs_from_feedbacks(lambda_total):
    """
    Calculate ECS from total feedback parameter.

    ECS = -ΔF₂ₓ / λ_total
    """
    delta_F2x = 3.7  # W/m² for CO₂ doubling
    if lambda_total >= 0:
        return float('inf')
    return -delta_F2x / lambda_total

def lambda_from_ecs(ecs_K):
    """Calculate lambda from ECS."""
    delta_F2x = 3.7
    return -delta_F2x / ecs_K

print("\nFeedback Parameter and Climate Sensitivity:")
print("-" * 60)
print(f"{'λ_total (W/m²/K)':<20} {'Gain':<12} {'ECS (°C)':<15} {'Stability'}")
print("-" * 60)

for lam in [-4.0, -3.2, -2.0, -1.5, -1.0, -0.5, 0]:
    if lam < 0:
        G = feedback_gain(lam - (-3.2), -3.2)
        ecs = ecs_from_feedbacks(lam)
        stab = "Stable" if lam < -1 else "Less stable"
        print(f"{lam:<20} {G:<12.1f} {ecs:<15.1f} {stab}")


# =============================================================================
# PART 3: INDIVIDUAL FEEDBACKS
# =============================================================================
print("\n" + "=" * 70)
print("PART 3: INDIVIDUAL CLIMATE FEEDBACKS")
print("=" * 70)

individual_text = """
MAJOR CLIMATE FEEDBACKS:
========================

1. PLANCK FEEDBACK (λ₀ ≈ -3.2 W/m²/K)

   dF/dT = 4εσT³ ≈ 3.2 W/m²/K at 288 K

   NEGATIVE (stabilizing)
   Warmer surface emits more radiation
   Fundamental thermodynamic response

2. WATER VAPOR FEEDBACK (λ_wv ≈ +1.6 to +2.0 W/m²/K)

   POSITIVE (amplifying)
   Clausius-Clapeyron: 7% more vapor per °C
   More vapor → more greenhouse → more warming

   Strongest feedback!
   Well understood from observations

3. LAPSE RATE FEEDBACK (λ_lr ≈ -0.6 W/m²/K globally)

   NEGATIVE overall but spatially variable

   Tropics: Deep convection, upper troposphere warms more
   → More emission aloft → negative feedback

   Arctic: Strong inversion, surface warms more
   → Less emission increase → positive feedback

   Combined with water vapor: ~+1.0 to +1.3 W/m²/K

4. SURFACE ALBEDO FEEDBACK (λ_α ≈ +0.3 to +0.5 W/m²/K)

   POSITIVE
   Ice/snow melt → darker surface → absorb more solar

   Dominated by Arctic sea ice
   Also snow on land, ice sheets

5. CLOUD FEEDBACK (λ_cld ≈ -0.5 to +1.5 W/m²/K)

   UNCERTAIN! The big unknown.

   Low clouds (stratocumulus):
   - Cooling effect (high albedo)
   - May decrease with warming → positive feedback

   High clouds (cirrus):
   - Warming effect (greenhouse)
   - May increase with warming → positive feedback

   Net effect: Probably positive, magnitude unclear
"""
print(individual_text)

def water_vapor_feedback(delta_T, lambda_wv=1.8):
    """
    Water vapor feedback contribution.
    """
    return lambda_wv * delta_T

def albedo_feedback(delta_T, lambda_alpha=0.4):
    """
    Surface albedo feedback contribution.
    """
    return lambda_alpha * delta_T

def combined_response(delta_F, feedbacks_dict):
    """
    Calculate temperature response with all feedbacks.
    """
    lambda_0 = -3.2  # Planck
    lambda_total = lambda_0 + sum(feedbacks_dict.values())

    if lambda_total >= 0:
        return float('inf')

    return -delta_F / lambda_total

print("\nFeedback Values (IPCC AR6):")
print("-" * 60)

feedbacks = [
    ("Planck", -3.2, "Negative", "High"),
    ("Water vapor + lapse rate", 1.3, "Positive", "High"),
    ("Surface albedo", 0.4, "Positive", "Medium"),
    ("Cloud", 0.5, "Positive", "Low"),
]

print(f"{'Feedback':<28} {'λ (W/m²/K)':<15} {'Sign':<12} {'Confidence'}")
print("-" * 60)

total_lambda = 0
for name, lam, sign, conf in feedbacks:
    print(f"{name:<28} {lam:+<15.1f} {sign:<12} {conf}")
    total_lambda += lam

print("-" * 60)
print(f"{'TOTAL':<28} {total_lambda:+<15.1f}")
print(f"\nImplied ECS: {ecs_from_feedbacks(total_lambda):.1f}°C")


# =============================================================================
# PART 4: CLOUD FEEDBACK PHYSICS
# =============================================================================
print("\n" + "=" * 70)
print("PART 4: CLOUD FEEDBACK - THE BIG UNCERTAINTY")
print("=" * 70)

cloud_text = """
CLOUD RADIATIVE EFFECTS:
========================

SHORTWAVE (Albedo):
Low clouds: High albedo (~0.6), strong cooling
High clouds: Lower albedo, less cooling

LONGWAVE (Greenhouse):
Low clouds: Warm tops, weak greenhouse
High clouds: Cold tops, STRONG greenhouse

NET EFFECT BY CLOUD TYPE:

Cloud type       SW effect    LW effect    NET
─────────────────────────────────────────────────
Stratocumulus    -60 W/m²     +30 W/m²     -30 W/m² (cooling)
Deep convective  -50 W/m²     +45 W/m²     -5 W/m² (small)
Cirrus           -5 W/m²      +20 W/m²     +15 W/m² (warming)

CLOUD FEEDBACK MECHANISMS:

1. LOW CLOUD AMOUNT
   Subtropical stratocumulus
   May decrease with warming (boundary layer changes)
   → Positive feedback (less cooling)

2. LOW CLOUD OPTICAL DEPTH
   Warmer → more rain out → thinner clouds?
   OR warmer → more moisture → thicker clouds?
   UNCERTAIN

3. HIGH CLOUD ALTITUDE
   "Fixed Anvil Temperature" hypothesis
   Convective tops stay at same temperature
   → Rise to higher altitude with warming
   → Colder → more greenhouse
   → Positive feedback

4. HIGH CLOUD AMOUNT
   Could increase or decrease
   Very uncertain

OBSERVATIONAL CONSTRAINTS:

- Short satellite record
- Internal variability large
- Different responses to different forcings
- Emergent constraints from present climate
"""
print(cloud_text)

def cloud_net_forcing(low_cloud_fraction, high_cloud_fraction,
                      low_cre=-50, high_cre=+15):
    """
    Estimate cloud radiative effect.

    CRE = cloud fraction × typical effect
    """
    cre = low_cloud_fraction * low_cre + high_cloud_fraction * high_cre
    return cre

def cloud_feedback_range():
    """
    Return range of cloud feedback estimates.
    """
    return (-0.5, 0.5, 1.5)  # Low, central, high

print("\nCloud Radiative Effect Examples:")
print("-" * 60)

scenarios = [
    ("Current climate", 0.3, 0.2),
    ("More high cloud", 0.3, 0.25),
    ("Less low cloud", 0.25, 0.2),
    ("Both changes", 0.25, 0.25),
]

print(f"{'Scenario':<25} {'Low frac':<12} {'High frac':<12} {'Net CRE (W/m²)'}")
print("-" * 60)

for name, low, high in scenarios:
    cre = cloud_net_forcing(low, high)
    print(f"{name:<25} {low:<12.2f} {high:<12.2f} {cre:.0f}")


# =============================================================================
# PART 5: EARTH SYSTEM FEEDBACKS
# =============================================================================
print("\n" + "=" * 70)
print("PART 5: EARTH SYSTEM FEEDBACKS")
print("=" * 70)

earth_system_text = """
SLOW / EARTH SYSTEM FEEDBACKS:
==============================

Not included in standard ECS but operate on longer timescales

1. ICE SHEET FEEDBACK

   Timescale: 100-10,000 years
   Ice sheets shrink → lower albedo → more warming
   Additional +0.5-1.5 W/m²/K (very long term)

   Greenland: ~7m sea level in ice
   Antarctica: ~57m sea level

2. VEGETATION FEEDBACK

   Timescale: 10-1000 years
   Warming → forests expand poleward → lower albedo
   Possible desertification in subtropics
   Net: Small positive feedback (+0.1 W/m²/K?)

3. PERMAFROST CARBON FEEDBACK

   Timescale: 10-100 years
   Thaw → CO₂ + CH₃ release → more warming
   Estimated: +0.05-0.2°C additional warming per °C

4. OCEAN CARBON FEEDBACK

   Timescale: 100-1000 years
   Warmer ocean → less CO₂ uptake
   Estimated: 20-40 ppm/°C
   Positive feedback

5. WEATHERING FEEDBACK

   Timescale: 100,000+ years
   Warmer → more weathering → CO₂ drawdown
   Negative feedback (Earth's thermostat)
   Stabilizes climate on geologic time

EARTH SYSTEM SENSITIVITY (ESS):

Including ice sheet and vegetation feedbacks
ESS ≈ 1.5 × ECS ≈ 4-6°C for 2×CO₂

Relevant for paleoclimate and very long term
"""
print(earth_system_text)

def permafrost_carbon_feedback(warming_C, release_per_C=50):
    """
    Estimate additional warming from permafrost carbon.

    release_per_C: Gt C released per degree warming
    """
    co2_released = warming_C * release_per_C
    # ~2 ppm CO₂ per Gt C
    ppm_increase = co2_released * 2

    # Additional forcing
    delta_F = 5.35 * np.log((400 + ppm_increase) / 400)

    # Additional warming (using ECS sensitivity)
    additional_warming = delta_F * 0.81

    return co2_released, additional_warming

print("\nPermafrost Carbon Feedback:")
print("-" * 55)
print(f"{'Initial warming (°C)':<22} {'C released (Gt)':<18} {'Extra warming (°C)'}")
print("-" * 55)

for dT in [1, 2, 3, 4, 5]:
    c_release, extra = permafrost_carbon_feedback(dT)
    print(f"{dT:<22} {c_release:<18.0f} {extra:.2f}")


# =============================================================================
# PART 6: PATTERNS AND STATE DEPENDENCE
# =============================================================================
print("\n" + "=" * 70)
print("PART 6: PATTERN EFFECTS AND STATE DEPENDENCE")
print("=" * 70)

pattern_text = """
PATTERN EFFECT:
===============

Climate sensitivity depends on SPATIAL PATTERN of warming!

WHY?

Low clouds concentrated in specific regions
Different warming patterns activate feedbacks differently

HISTORICAL VS EQUILIBRIUM:

Historical warming pattern ≠ Equilibrium pattern
- Historical: Eastern Pacific cool (La Niña-like)
- Equilibrium: Eastern Pacific warms more

Eastern Pacific:
- Lots of low clouds
- Sensitive region for cloud feedback

IMPLICATION:

Observed λ (from historical period) ≠ True λ
Historical pattern underestimates ECS!

Correction: +0.3-0.5°C to ECS estimates

STATE DEPENDENCE:

Feedbacks may change with mean state

EXAMPLES:
- Albedo feedback: Saturates when ice is gone
- Lapse rate: Changes at high warming
- Water vapor: ~Constant (C-C doesn't care about base state)

PALEO CONSTRAINTS:

LGM (-5°C, -100 ppm CO₂, more ice):
Estimated ECS: 2.5-4.5°C

Pliocene (+3°C, 400 ppm CO₂, less ice):
Estimated ECS: 2-4°C

Consistent with modern estimates!
"""
print(pattern_text)


# =============================================================================
# PART 7: SYNTHESIS
# =============================================================================
print("\n" + "=" * 70)
print("PART 7: CLIMATE SENSITIVITY SYNTHESIS")
print("=" * 70)

synthesis_text = """
MULTIPLE LINES OF EVIDENCE:
===========================

1. PROCESS UNDERSTANDING
   - Sum of feedback parameters
   - Dominated by cloud uncertainty
   - ECS: 2.0-5.5°C (process models)

2. HISTORICAL WARMING
   - Observed ΔT, estimated ΔF
   - Ocean heat uptake correction
   - Pattern effect correction
   - ECS: 2.0-4.5°C

3. PALEOCLIMATE
   - LGM, Pliocene, deep time
   - Different forcings, same physics
   - ECS: 2.0-4.5°C

4. EMERGENT CONSTRAINTS
   - Present-day variability
   - Correlations with ECS in models
   - Helps narrow cloud feedback
   - ECS: 2.5-4.0°C

IPCC AR6 ASSESSMENT:

Very likely range: 2.5-4.0°C
Best estimate: 3.0°C

< 2°C or > 5°C now considered unlikely

KEY REMAINING UNCERTAINTIES:

1. Cloud feedback (especially low clouds)
2. Pattern effect magnitude
3. Aerosol forcing history
4. Earth system feedbacks at high warming
"""
print(synthesis_text)

print("\nECS Evidence Synthesis:")
print("-" * 55)

methods = [
    ("Process models", 2.0, 3.5, 5.5),
    ("Historical + pattern", 2.0, 3.0, 4.5),
    ("Paleoclimate (LGM)", 2.0, 3.0, 4.5),
    ("Emergent constraints", 2.5, 3.0, 4.0),
    ("IPCC AR6 assessed", 2.5, 3.0, 4.0),
]

print(f"{'Method':<25} {'Low':<10} {'Central':<10} {'High'}")
print("-" * 55)

for method, low, mid, high in methods:
    print(f"{method:<25} {low:<10.1f} {mid:<10.1f} {high:.1f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: CLIMATE FEEDBACKS")
print("=" * 70)

summary = """
KEY CLIMATE FEEDBACK PHYSICS:
============================

1. CLIMATE SENSITIVITY
   - ΔT = λ × ΔF
   - No-feedback: λ₀ = 0.27 K/(W/m²) → 1.0°C for 2×CO₂
   - With feedbacks: ECS ≈ 3°C (2.5-4.0°C likely)

2. FEEDBACK DECOMPOSITION
   - Planck: -3.2 W/m²/K (stabilizing)
   - Water vapor + lapse rate: +1.3 W/m²/K (amplifying)
   - Surface albedo: +0.4 W/m²/K (amplifying)
   - Cloud: +0.5 W/m²/K (uncertain, amplifying)

3. FEEDBACK GAIN
   - G = 1/(1-f) ≈ 3 for ECS = 3°C
   - Feedbacks TRIPLE the no-feedback response

4. CLOUD FEEDBACK
   - The dominant uncertainty
   - Low clouds: May decrease → positive
   - High clouds: Rise with warming → positive
   - Range: -0.5 to +1.5 W/m²/K

5. EARTH SYSTEM FEEDBACKS
   - Ice sheets, permafrost, vegetation
   - Operate on 100-10,000 year timescales
   - ESS ≈ 1.5 × ECS

6. PATTERN EFFECT
   - Spatial warming pattern matters
   - Historical ≠ equilibrium pattern
   - Affects ECS estimation


THE PHYSICS TELLS US:
====================
- Earth WILL warm more than 1°C for CO₂ doubling
- Best estimate ~3°C, range 2.5-4.0°C
- Cloud feedback is the key uncertainty
- Feedbacks amplify, not dampen, warming
- No evidence for feedbacks that prevent warming
"""
print(summary)

print("\n" + "=" * 70)
print("END OF CLIMATE FEEDBACKS")
print("=" * 70)
