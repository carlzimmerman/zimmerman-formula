#!/usr/bin/env python3
"""
Deep Investigation: Why TS Threshold ≈ Z²?

Finding:
    Tropical Storm threshold = 34 kt
    Z² = 32π/3 = 33.51
    Deviation = +1.46%

Questions:
1. Is this coincidence or physics?
2. How was 34 kt historically determined?
3. Does Z² appear in atmospheric physics?
4. What other thresholds relate to Z²?
"""

import numpy as np

# =============================================================================
# CONSTANTS
# =============================================================================

PI = np.pi
Z_SQUARED = 32 * PI / 3  # 33.5103
Z_VALUE = np.sqrt(Z_SQUARED)  # 5.7888
ONE_OVER_Z = 1 / Z_VALUE

# Wind speed conversions
KT_TO_MS = 0.514444  # knots to m/s
KT_TO_KMH = 1.852    # knots to km/h
KT_TO_MPH = 1.15078  # knots to mph

print("=" * 80)
print("  INVESTIGATION: WHY TS THRESHOLD ≈ Z²?")
print("=" * 80)

print(f"\n  Z² = 32π/3 = {Z_SQUARED:.6f}")
print(f"  TS threshold = 34 kt")
print(f"  Deviation = {(34 - Z_SQUARED)/Z_SQUARED*100:+.2f}%")

# =============================================================================
# BEAUFORT SCALE ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("  BEAUFORT SCALE STRUCTURE")
print("=" * 80)

print("""
The Beaufort Scale follows an empirical power law:
    v = k × B^(3/2)

Where B is Beaufort number and v is wind speed.
""")

# Beaufort scale thresholds (in knots)
beaufort = {
    0: (0, 1),      # Calm
    1: (1, 3),      # Light air
    2: (4, 6),      # Light breeze
    3: (7, 10),     # Gentle breeze
    4: (11, 16),    # Moderate breeze
    5: (17, 21),    # Fresh breeze
    6: (22, 27),    # Strong breeze
    7: (28, 33),    # Near gale
    8: (34, 40),    # Gale (TS starts here!)
    9: (41, 47),    # Strong gale
    10: (48, 55),   # Storm
    11: (56, 63),   # Violent storm
    12: (64, 999),  # Hurricane (Cat 1 starts here!)
}

# Check power law relationship
print("\n  Beaufort power law: v ≈ 0.836 × B^(3/2) m/s")
print("\n  B  | Actual (kt) | Power Law | Ratio")
print("-" * 45)

for B in range(1, 13):
    actual_low, actual_high = beaufort[B]
    actual_mid = (actual_low + actual_high) / 2 if actual_high < 100 else actual_low
    power_law_ms = 0.836 * B**1.5  # m/s
    power_law_kt = power_law_ms / KT_TO_MS
    ratio = actual_mid / power_law_kt if power_law_kt > 0 else 0
    print(f"  {B:2d} | {actual_mid:6.1f}     | {power_law_kt:6.1f}    | {ratio:.3f}")

# =============================================================================
# Z² IN BEAUFORT CONTEXT
# =============================================================================

print("\n" + "=" * 80)
print("  Z² IN BEAUFORT CONTEXT")
print("=" * 80)

print(f"\n  If Z² = {Z_SQUARED:.4f} kt corresponds to a Beaufort number:")

# Solve: Z² = 0.836 × B^(3/2) × (1/KT_TO_MS)
# Z² × KT_TO_MS = 0.836 × B^(3/2)
# B = (Z² × KT_TO_MS / 0.836)^(2/3)

z2_ms = Z_SQUARED * KT_TO_MS
B_from_z2 = (z2_ms / 0.836)**(2/3)
print(f"  Z² in m/s = {z2_ms:.4f}")
print(f"  Implied Beaufort number = {B_from_z2:.4f}")
print(f"  This is close to B = 8 (Gale)!")

# Check: what Beaufort number gives exactly Z²?
print(f"\n  Force 8 (Gale) starts at 34 kt ≈ Z² = {Z_SQUARED:.2f} kt")

# =============================================================================
# PHYSICAL QUANTITIES AT Z² kt
# =============================================================================

print("\n" + "=" * 80)
print("  PHYSICAL QUANTITIES AT Z² kt")
print("=" * 80)

v_z2_kt = Z_SQUARED
v_z2_ms = Z_SQUARED * KT_TO_MS
v_z2_kmh = Z_SQUARED * KT_TO_KMH
v_z2_mph = Z_SQUARED * KT_TO_MPH

print(f"\n  Wind speed at Z² = {Z_SQUARED:.4f}:")
print(f"    = {v_z2_kt:.2f} kt")
print(f"    = {v_z2_ms:.2f} m/s")
print(f"    = {v_z2_kmh:.2f} km/h")
print(f"    = {v_z2_mph:.2f} mph")

# Kinetic energy density: (1/2) × ρ × v²
rho_air = 1.225  # kg/m³ at sea level
KE_density = 0.5 * rho_air * v_z2_ms**2

print(f"\n  Kinetic energy density at Z² kt:")
print(f"    KE = ½ρv² = {KE_density:.2f} J/m³")

# Dynamic pressure (wind pressure)
dynamic_pressure = 0.5 * rho_air * v_z2_ms**2  # Pa
print(f"    Dynamic pressure = {dynamic_pressure:.2f} Pa")
print(f"                     = {dynamic_pressure/1000:.4f} kPa")

# Wave height estimate (fully developed sea)
# Empirical: H_s ≈ 0.024 × v² (v in m/s, H in m)
wave_height = 0.024 * v_z2_ms**2
print(f"\n  Estimated wave height (fully developed):")
print(f"    H_s ≈ {wave_height:.1f} m")

# =============================================================================
# IS Z² SPECIAL IN ATMOSPHERIC PHYSICS?
# =============================================================================

print("\n" + "=" * 80)
print("  IS Z² SPECIAL IN ATMOSPHERIC PHYSICS?")
print("=" * 80)

print("""
Exploring whether Z² = 32π/3 appears naturally in atmospheric dynamics:

1. TROPICAL CYCLONE THERMODYNAMICS
   The maximum potential intensity (MPI) involves:
   V_max² ∝ (SST - T_out) × (C_k/C_d)

   No obvious connection to 32π/3.

2. ROSSBY NUMBER
   Ro = v / (f × L) where f = Coriolis parameter
   At typical hurricane scales, this doesn't yield Z².

3. CARNOT EFFICIENCY
   The tropical cyclone acts as a Carnot heat engine:
   η = (T_s - T_out) / T_s
   No direct connection to Z².

4. BEAUFORT POWER LAW
   The 3/2 power law: v ∝ B^(3/2)
   This is empirical, not derived from first principles.
""")

# =============================================================================
# OTHER INTENSITY THRESHOLDS
# =============================================================================

print("\n" + "=" * 80)
print("  ALL INTENSITY THRESHOLDS vs Z² MULTIPLES")
print("=" * 80)

thresholds = {
    'Tropical Depression max': 33,
    'Tropical Storm (TS)': 34,
    'Strong TS': 50,
    'Category 1 Hurricane': 64,
    'Category 2': 83,
    'Category 3 (Major)': 96,
    'Category 4': 113,
    'Category 5': 137,
}

print(f"\n  Z² = {Z_SQUARED:.4f}")
print(f"\n  {'Threshold':<25} {'kt':>6} {'/ Z²':>8} {'× Z':>8} {'Nearest':>10}")
print("-" * 65)

for name, val in thresholds.items():
    ratio_z2 = val / Z_SQUARED
    ratio_z = val / Z_VALUE
    nearest_int = round(ratio_z2)
    expected = nearest_int * Z_SQUARED
    dev = (val - expected) / expected * 100 if expected > 0 else 0
    print(f"  {name:<25} {val:>6} {ratio_z2:>8.3f} {ratio_z:>8.2f} {nearest_int:>4}×Z² ({dev:+.1f}%)")

# =============================================================================
# THE 32 AND π/3 FACTORS
# =============================================================================

print("\n" + "=" * 80)
print("  DECOMPOSING Z² = 32 × π/3")
print("=" * 80)

print(f"""
  Z² = 32 × π/3 = 32 × {PI/3:.6f}

  The factor 32:
    - 2⁵ = 32 (power of 2)
    - Related to 8D compactification (8 × 4 = 32)
    - Vol(S⁷)/Vol(S⁵) × 32 = Z²

  The factor π/3:
    - π/3 = {PI/3:.6f} ≈ 1.047
    - This is 60° in radians
    - Appears in hexagonal symmetry
    - Vol(S⁷)/Vol(S⁵) = π/3

  In atmospheric context:
    - π appears in circular/spherical geometry
    - 60° appears in Coriolis dynamics
    - 32 has no obvious atmospheric significance
""")

# Check: is 32 related to anything atmospheric?
print("\n  Checking atmospheric constants:")
print(f"    Ideal gas constant R = 8.314 J/(mol·K)")
print(f"    R / (π/3) = {8.314 / (PI/3):.4f}")
print(f"    32 / R = {32 / 8.314:.4f}")

# Latent heat of vaporization
L_v = 2.5e6  # J/kg
print(f"\n    Latent heat of water L_v = {L_v:.2e} J/kg")
print(f"    L_v / Z² = {L_v / Z_SQUARED:.2e}")

# =============================================================================
# HYPOTHESIS: COINCIDENCE OR PHYSICS?
# =============================================================================

print("\n" + "=" * 80)
print("  HYPOTHESIS EVALUATION")
print("=" * 80)

print("""
EVIDENCE FOR COINCIDENCE:
  1. The 34 kt threshold predates any knowledge of Z²
  2. It was determined empirically by sailors in 1805
  3. No derivation of Z² from atmospheric physics exists
  4. The deviation (+1.46%) is small but not zero

EVIDENCE FOR PHYSICS:
  1. The match is remarkably close (within 1.5%)
  2. Beaufort scale uses 3/2 power law (related to energy?)
  3. Force 8 is precisely where TS begins
  4. Other thresholds show approximate Z² × n pattern

PROBABILITY ANALYSIS:
  If we randomly selected a threshold between 1-200 kt,
  what's the probability of landing within 1.5% of Z²?

  Range: ±0.5 kt around any value
  Probability of hitting Z² ± 1.5% = 2 × 0.015 × 33.5 / 200 = 0.5%

  This is unlikely by chance alone, BUT we're also testing
  multiple hypotheses (multiple thresholds), so we must
  apply a Bonferroni correction.

CONCLUSION:
  The TS ≈ Z² relationship is INTRIGUING but not PROVEN.
  It could be:
  1. Coincidence (most likely with current evidence)
  2. Reflecting some deeper physics we don't understand
  3. A consequence of human perception thresholds
""")

# =============================================================================
# INTERESTING OBSERVATION
# =============================================================================

print("\n" + "=" * 80)
print("  INTERESTING OBSERVATION")
print("=" * 80)

print(f"""
The Beaufort Scale power law: v ≈ 0.836 × B^(3/2) m/s

At B = 8 (Gale / TS threshold):
  v = 0.836 × 8^(3/2) = 0.836 × 22.63 = 18.92 m/s
  v = 18.92 / 0.514 = 36.8 kt (middle of Force 8)

The 3/2 power relates to energy considerations:
  - Wind force on sails ∝ v²
  - Wave height ∝ v² (energy transfer)
  - Energy flux ∝ v³

The fact that Force 8 starts at ~34 kt may relate to
when wind ENERGY crosses a critical threshold for sea state.

If we set v² ∝ Z² (energy proportional to Z²):
  v ∝ √Z² = Z = 5.79 m/s = 11.3 kt

This doesn't match. But if we use a different scaling...

If dynamic pressure P = ½ρv² = some multiple of a reference:
  At v = Z² kt = 17.2 m/s:
  P = 0.5 × 1.225 × 17.2² = 181 Pa

  This is about 0.18% of atmospheric pressure (101325 Pa).
  Not an obvious round number.
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("  SUMMARY")
print("=" * 80)

print(f"""
FINDING: TS threshold (34 kt) ≈ Z² (33.51 kt)
         Deviation: +1.46%

HISTORICAL ORIGIN:
  - 34 kt = Beaufort Force 8 (Gale)
  - Defined empirically by Admiral Beaufort in 1805
  - Based on observable sea conditions, not physics equations

PHYSICAL BASIS:
  - No known derivation of Z² from atmospheric dynamics
  - The Beaufort scale uses a 3/2 power law (empirical)
  - 34 kt marks the onset of hazardous sea conditions

ASSESSMENT:
  - The match is likely COINCIDENTAL
  - But it remains an intriguing numerical relationship
  - Further investigation of energy thresholds warranted

WHAT WOULD PROVE CAUSATION:
  1. Derive Z² from first principles of atmospheric physics
  2. Show other thresholds follow Z² × n pattern exactly
  3. Find Z² in energy or pressure relationships
  4. Demonstrate measurement independence of threshold

STATUS: INTERESTING COINCIDENCE (pending further evidence)
""")

print("=" * 80)
