#!/usr/bin/env python3
"""
Z² Intensity Quantization Analysis

Exploring whether hurricane intensity thresholds follow Z² × n pattern:
    TS:   34 kt ≈ 1×Z² (33.5)  → +1.5%
    Cat1: 64 kt ≈ 2×Z² (67.0)  → -4.5%
    Cat3: 96 kt ≈ 3×Z² (100.5) → -4.5%
    Cat5: 137 kt ≈ 4×Z² (134.0) → +2.2%

Questions:
1. Is this pattern statistically significant?
2. Does the pattern hold in other wind scales?
3. Is there a physical basis for energy quantization?
"""

import numpy as np
from scipy import stats

# =============================================================================
# CONSTANTS
# =============================================================================

PI = np.pi
Z_SQUARED = 32 * PI / 3  # 33.5103

print("=" * 80)
print("  Z² INTENSITY QUANTIZATION ANALYSIS")
print("=" * 80)

print(f"\n  Z² = 32π/3 = {Z_SQUARED:.4f}")

# =============================================================================
# SAFFIR-SIMPSON SCALE ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("  SAFFIR-SIMPSON SCALE vs Z² × n")
print("=" * 80)

# Official thresholds (kt)
ss_thresholds = {
    'TD max': 33,
    'TS min': 34,
    'TS max': 63,
    'Cat 1 min': 64,
    'Cat 1 max': 82,
    'Cat 2 min': 83,
    'Cat 2 max': 95,
    'Cat 3 min': 96,
    'Cat 3 max': 112,
    'Cat 4 min': 113,
    'Cat 4 max': 136,
    'Cat 5 min': 137,
}

# Find best-fit n for each threshold
print(f"\n  {'Threshold':<15} {'Value':>6} {'Best n':>8} {'Z²×n':>8} {'Dev':>8} {'Fit':>6}")
print("-" * 60)

deviations = []
for name, val in ss_thresholds.items():
    best_n = round(val / Z_SQUARED)
    if best_n == 0:
        best_n = 1
    expected = best_n * Z_SQUARED
    dev = (val - expected) / expected * 100
    deviations.append(abs(dev))
    fit = "✓" if abs(dev) < 5 else ""
    print(f"  {name:<15} {val:>6} {best_n:>8} {expected:>8.1f} {dev:>+7.1f}% {fit:>6}")

print(f"\n  Mean |deviation| = {np.mean(deviations):.1f}%")

# =============================================================================
# STATISTICAL TEST: Is Z² better than random?
# =============================================================================

print("\n" + "=" * 80)
print("  STATISTICAL TEST: Z² vs RANDOM")
print("=" * 80)

# Key thresholds that define category boundaries
key_thresholds = [34, 64, 83, 96, 113, 137]  # TS, C1, C2, C3, C4, C5

# Calculate deviations from nearest Z² × n
z2_deviations = []
for val in key_thresholds:
    best_n = round(val / Z_SQUARED)
    expected = best_n * Z_SQUARED
    dev = abs(val - expected) / expected
    z2_deviations.append(dev)

mean_z2_dev = np.mean(z2_deviations)
print(f"\n  Key thresholds: {key_thresholds}")
print(f"  Mean deviation from Z²×n: {mean_z2_dev*100:.2f}%")

# Monte Carlo: What's the probability of getting this fit by chance?
n_simulations = 100000
random_fits = []

for _ in range(n_simulations):
    # Generate random "thresholds" in same range
    random_thresh = np.random.uniform(30, 150, len(key_thresholds))
    random_thresh.sort()

    devs = []
    for val in random_thresh:
        best_n = max(1, round(val / Z_SQUARED))
        expected = best_n * Z_SQUARED
        dev = abs(val - expected) / expected
        devs.append(dev)
    random_fits.append(np.mean(devs))

# P-value: fraction of random fits as good or better
p_value = np.mean([f <= mean_z2_dev for f in random_fits])
print(f"\n  Monte Carlo test (n={n_simulations:,}):")
print(f"    P(random ≤ observed deviation) = {p_value:.4f}")
print(f"    Result: {'SIGNIFICANT' if p_value < 0.05 else 'NOT significant'} at α=0.05")

# =============================================================================
# TEST WITH OTHER WIND SCALES
# =============================================================================

print("\n" + "=" * 80)
print("  OTHER WIND SCALES vs Z²")
print("=" * 80)

# Australian scale (different from Saffir-Simpson!)
australian = {
    'Cat 1': 34,   # 34-47 kt (same as TS)
    'Cat 2': 48,   # 48-63 kt
    'Cat 3': 64,   # 64-85 kt (severe)
    'Cat 4': 86,   # 86-107 kt
    'Cat 5': 108,  # 108+ kt
}

print("\n  Australian Tropical Cyclone Scale:")
for name, val in australian.items():
    best_n = round(val / Z_SQUARED)
    expected = best_n * Z_SQUARED
    dev = (val - expected) / expected * 100
    print(f"    {name}: {val} kt, nearest Z²×{best_n} = {expected:.1f} kt ({dev:+.1f}%)")

# Japan Meteorological Agency scale
jma = {
    'Tropical Storm': 34,      # 34-47 kt
    'Severe TS': 48,           # 48-63 kt
    'Typhoon': 64,             # 64-84 kt
    'Very Strong Typhoon': 85, # 85-104 kt
    'Violent Typhoon': 105,    # 105+ kt
}

print("\n  Japan Meteorological Agency Scale:")
for name, val in jma.items():
    best_n = round(val / Z_SQUARED)
    expected = best_n * Z_SQUARED
    dev = (val - expected) / expected * 100
    print(f"    {name}: {val} kt, nearest Z²×{best_n} = {expected:.1f} kt ({dev:+.1f}%)")

# =============================================================================
# ENERGY CONSIDERATIONS
# =============================================================================

print("\n" + "=" * 80)
print("  ENERGY QUANTIZATION HYPOTHESIS")
print("=" * 80)

print("""
If intensity quantizes in units of Z², this suggests energy scaling:

  Kinetic energy density: KE = ½ρv²

  At v = n × Z² kt (converting to m/s):
    v_ms = n × Z² × 0.5144 m/s
    KE = ½ × 1.225 × (n × Z² × 0.5144)²
    KE = ½ × 1.225 × (n × 17.24)² J/m³
    KE = 182 × n² J/m³

  The energy goes as n², not n.

  Power dissipation goes as v³ ∝ n³.

  Neither gives simple quantization in n.
""")

# Calculate actual energy at each threshold
print("  Energy density at category thresholds:")
print(f"  {'Category':<10} {'Wind (kt)':>10} {'Wind (m/s)':>12} {'KE (J/m³)':>12} {'KE/182':>10}")
print("-" * 60)

rho = 1.225  # kg/m³
KE_unit = 182  # J/m³ at Z² kt

for name, val in [('TS', 34), ('Cat 1', 64), ('Cat 2', 83), ('Cat 3', 96), ('Cat 4', 113), ('Cat 5', 137)]:
    v_ms = val * 0.5144
    KE = 0.5 * rho * v_ms**2
    ratio = KE / KE_unit
    n_approx = val / Z_SQUARED
    print(f"  {name:<10} {val:>10} {v_ms:>12.2f} {KE:>12.1f} {ratio:>10.2f}")

# =============================================================================
# THE COINCIDENCE ARGUMENT
# =============================================================================

print("\n" + "=" * 80)
print("  EVALUATING THE COINCIDENCE ARGUMENT")
print("=" * 80)

print("""
Arguments that TS ≈ Z² is COINCIDENCE:

1. HISTORICAL: The 34 kt threshold was set in 1805 by Admiral Beaufort
   based on empirical observations of sea state, not physics equations.

2. HUMAN-DEFINED: The Saffir-Simpson scale (1971) inherited this threshold.
   The Cat 1-5 boundaries were chosen based on damage potential.

3. NO DERIVATION: Z² = 32π/3 has no known connection to atmospheric dynamics.
   It comes from 8D sphere geometry (string theory mathematics).

4. MULTIPLE TESTING: We're testing many thresholds against Z² × n.
   Some will match by chance. Our Monte Carlo p-value helps quantify this.

Arguments that it might be PHYSICS:

1. CLOSE MATCH: TS = 34 kt is within 1.5% of Z² = 33.51 kt.

2. PATTERN: Several thresholds approximately match Z² × n:
   - TS (34) ≈ 1×Z² (+1.5%)
   - Cat 1 (64) ≈ 2×Z² (-4.5%)
   - Cat 3 (96) ≈ 3×Z² (-4.5%)
   - Cat 5 (137) ≈ 4×Z² (+2.2%)

3. HUMAN PERCEPTION: Perhaps human perception of "hazardous" wind
   corresponds to some fundamental energy or stress threshold.

4. BEAUFORT 3/2 LAW: The empirical v ∝ B^(3/2) might hide physics.
""")

# =============================================================================
# FINAL ASSESSMENT
# =============================================================================

print("\n" + "=" * 80)
print("  FINAL ASSESSMENT")
print("=" * 80)

print(f"""
FINDING: TS threshold (34 kt) ≈ Z² (33.51 kt), deviation +1.46%

PATTERN: Several thresholds fit Z² × n with <5% error:
  - TS:   34 kt ≈ 1×Z² (dev: +1.5%)
  - Cat1: 64 kt ≈ 2×Z² (dev: -4.5%)
  - Cat3: 96 kt ≈ 3×Z² (dev: -4.5%)
  - Cat5: 137 kt ≈ 4×Z² (dev: +2.2%)

Monte Carlo p-value = {p_value:.4f}

INTERPRETATION:
  The p-value suggests the fit is {'better' if p_value < 0.05 else 'NOT better'}
  than random chance at the 5% significance level.

  However, this does NOT prove causation.
  The thresholds were defined historically without knowledge of Z².

CONCLUSION:
  STATUS: INTRIGUING PATTERN, UNPROVEN PHYSICS

  The TS ≈ Z² relationship and the Z² × n pattern for some thresholds
  is NOTEWORTHY but likely COINCIDENTAL with current evidence.

  To prove causation would require:
  1. Derivation of Z² from atmospheric physics
  2. Explanation of why Cat 2 and Cat 4 don't fit
  3. Independent prediction validated by observation
""")

print("=" * 80)
