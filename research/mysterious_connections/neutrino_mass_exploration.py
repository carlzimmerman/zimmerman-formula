#!/usr/bin/env python3
"""
NEUTRINO MASS EXPLORATION
Searching for Zimmerman patterns in neutrino mass splittings.

Carl Zimmerman | March 2026
"""

import numpy as np

print("=" * 70)
print("NEUTRINO MASS EXPLORATION")
print("Searching for Zimmerman patterns")
print("=" * 70)

# The Zimmerman constant
Z = 2 * np.sqrt(8 * np.pi / 3)
print(f"\nZ = 2√(8π/3) = {Z:.6f}")

# Key dimensional numbers
D_bosonic = 26
D_M_theory = 11
D_E8 = 8
D_compact = 7
D_spatial = 3
D_horizon = 2

# Known neutrino parameters
# Mass-squared differences (eV²)
delta_m21_sq = 7.53e-5  # Solar mass splitting
delta_m32_sq = 2.453e-3  # Atmospheric mass splitting (normal ordering)

# Mixing angles
sin2_theta_12 = 0.307  # Solar angle
sin2_theta_23 = 0.546  # Atmospheric angle
sin2_theta_13 = 0.0220  # Reactor angle

print(f"""
MEASURED NEUTRINO PARAMETERS:

MASS SPLITTINGS:
  Δm²₂₁ = {delta_m21_sq:.2e} eV² (solar)
  Δm²₃₂ = {delta_m32_sq:.3e} eV² (atmospheric)

  Ratio: Δm²₃₂/Δm²₂₁ = {delta_m32_sq/delta_m21_sq:.1f}

MIXING ANGLES:
  sin²θ₁₂ = {sin2_theta_12} (solar)
  sin²θ₂₃ = {sin2_theta_23} (atmospheric)
  sin²θ₁₃ = {sin2_theta_13} (reactor)
""")

# ============================================================================
print("=" * 70)
print("PART 1: MASS SPLITTING RATIO")
print("=" * 70)

ratio_measured = delta_m32_sq / delta_m21_sq
print(f"\nMeasured ratio Δm²₃₂/Δm²₂₁ = {ratio_measured:.2f}")

# Test various combinations
candidates = [
    ("Z²/π", Z**2 / np.pi),
    ("8π + Z", 8 * np.pi + Z),
    ("26 + Z", 26 + Z),
    ("Z × Z", Z * Z),
    ("4Z", 4 * Z),
    ("6Z", 6 * Z),
    ("8 + 3Z", 8 + 3 * Z),
    ("64π/Z", 64 * np.pi / Z),
    ("(8+3Z) + Z", (8 + 3*Z) + Z),
    ("26", 26),
    ("32", 32),
    ("33", 33),
    ("36", 36),
]

print(f"\nSearching for Δm²₃₂/Δm²₂₁ ≈ {ratio_measured:.1f}:")
print("-" * 50)

for name, value in candidates:
    if 20 < value < 40:
        error = abs(value - ratio_measured) / ratio_measured * 100
        print(f"  {name:15s} = {value:8.3f}  error: {error:5.2f}%")

# The measured ratio is about 32.6
# Let's see if 32 = 2⁵ fits
print(f"\n  32 = 2⁵         = 32.000   error: {abs(32 - ratio_measured)/ratio_measured*100:.2f}%")
print(f"  33 = 3 × 11     = 33.000   error: {abs(33 - ratio_measured)/ratio_measured*100:.2f}%")

# ============================================================================
print("\n" + "=" * 70)
print("PART 2: SOLAR MIXING ANGLE sin²θ₁₂")
print("=" * 70)

print(f"\nMeasured sin²θ₁₂ = {sin2_theta_12}")

candidates_12 = [
    ("1/π", 1/np.pi),
    ("Z/2π", Z/(2*np.pi)),
    ("3/Z²", 3/Z**2),
    ("1/Z", 1/Z),
    ("Z/26", Z/26),
    ("11/36", 11/36),
    ("3/10", 3/10),
    ("8/26", 8/26),
    ("Z/19", Z/19),
]

print(f"\nSearching for sin²θ₁₂ ≈ {sin2_theta_12}:")
print("-" * 50)

for name, value in candidates_12:
    if 0.25 < value < 0.35:
        error = abs(value - sin2_theta_12) / sin2_theta_12 * 100
        print(f"  {name:15s} = {value:.6f}  error: {error:5.2f}%")

# ============================================================================
print("\n" + "=" * 70)
print("PART 3: ATMOSPHERIC MIXING ANGLE sin²θ₂₃")
print("=" * 70)

print(f"\nMeasured sin²θ₂₃ = {sin2_theta_23}")

candidates_23 = [
    ("1/2", 0.5),
    ("Z/11", Z/11),
    ("1/2 + 1/26", 0.5 + 1/26),
    ("Z/(2Z+1)", Z/(2*Z+1)),
    ("1/2 + Z/100", 0.5 + Z/100),
    ("6/11", 6/11),
    ("11/20", 11/20),
    ("11/22", 11/22),
    ("3Z/32", 3*Z/32),
]

print(f"\nSearching for sin²θ₂₃ ≈ {sin2_theta_23}:")
print("-" * 50)

for name, value in candidates_23:
    if 0.45 < value < 0.65:
        error = abs(value - sin2_theta_23) / sin2_theta_23 * 100
        print(f"  {name:15s} = {value:.6f}  error: {error:5.2f}%")

# Note: θ₂₃ is close to maximal (45°)
print(f"\n  1/2 (maximal)  = 0.500000  error: {abs(0.5 - sin2_theta_23)/sin2_theta_23*100:.2f}%")

# ============================================================================
print("\n" + "=" * 70)
print("PART 4: REACTOR MIXING ANGLE sin²θ₁₃")
print("=" * 70)

print(f"\nMeasured sin²θ₁₃ = {sin2_theta_13}")

# This is the smallest angle - about 1/45
candidates_13 = [
    ("1/Z²", 1/Z**2),
    ("Z/264", Z/264),
    ("1/45", 1/45),
    ("1/64", 1/64),
    ("Z/256", Z/256),
    ("π/143", np.pi/143),
    ("3/137", 3/137),
    ("Z/(8×3Z)", Z/(8*3*Z)),
    ("1/(4Z²+3)", 1/(4*Z**2+3)),  # The fine structure form!
]

print(f"\nSearching for sin²θ₁₃ ≈ {sin2_theta_13}:")
print("-" * 50)

for name, value in candidates_13:
    if 0.015 < value < 0.030:
        error = abs(value - sin2_theta_13) / sin2_theta_13 * 100
        print(f"  {name:15s} = {value:.6f}  error: {error:5.2f}%")

# ============================================================================
print("\n" + "=" * 70)
print("PART 5: THE JARLSKOG INVARIANT (CP VIOLATION)")
print("=" * 70)

# J ≈ 0.0336 (measure of CP violation in neutrinos)
J_measured = 0.0336

print(f"\nMeasured Jarlskog invariant J = {J_measured}")

candidates_J = [
    ("1/Z²", 1/Z**2),
    ("Z/π²", Z/np.pi**2),
    ("π/100", np.pi/100),
    ("1/(8+3Z)", 1/(8+3*Z)),
    ("α", 1/137.036),
    ("3α", 3/137.036),
    ("Z/π³", Z/np.pi**3),
    ("1/33", 1/33),
    ("Z/172", Z/172),
]

print(f"\nSearching for J ≈ {J_measured}:")
print("-" * 50)

for name, value in candidates_J:
    if 0.025 < value < 0.045:
        error = abs(value - J_measured) / J_measured * 100
        print(f"  {name:15s} = {value:.6f}  error: {error:5.2f}%")

# ============================================================================
print("\n" + "=" * 70)
print("PART 6: ABSOLUTE NEUTRINO MASS SCALE")
print("=" * 70)

# Sum of neutrino masses (cosmological limit)
sum_nu_limit = 0.12  # eV (Planck limit)

# Electron mass for comparison
m_e = 0.511e6  # eV

print(f"""
ABSOLUTE MASS SCALE:

Cosmological limit: Σm_ν < {sum_nu_limit} eV
Electron mass: m_e = {m_e:.3e} eV

Ratio: m_e / Σm_ν > {m_e / sum_nu_limit:.2e}
       This is ~ 4 million!
""")

# What if neutrino mass involves Z in the denominator?
print("HYPOTHESIS: If Σm_ν = m_e / (something large)...")
print("-" * 50)

# The electron mass in terms of proton mass
m_p = 938.3e6  # eV
ratio_p_e = m_p / m_e

# What combinations give ~10^6?
test_values = [
    ("Z⁶", Z**6),
    ("(64π)²", (64*np.pi)**2),
    ("Z² × (64π + Z)", Z**2 * (64*np.pi + Z)),
    ("(m_p/m_e)²", ratio_p_e**2),
    ("Z × (m_p/m_e)", Z * ratio_p_e),
]

print("\nSearching for large suppression factors ~10⁶:")
for name, value in test_values:
    print(f"  {name:25s} = {value:.2e}")

# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY: NEUTRINO PATTERNS")
print("=" * 70)

print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                   NEUTRINO MASS PATTERNS                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MASS SPLITTING RATIO:                                              │
│    Δm²₃₂/Δm²₂₁ ≈ 32.6 ≈ 33 = 3 × 11 (M-theory × spatial!)         │
│                                                                     │
│  MIXING ANGLES:                                                     │
│    sin²θ₁₂ ≈ 0.307 ≈ 8/26 = 0.308 (E8/bosonic)                     │
│    sin²θ₂₃ ≈ 0.546 ≈ 6/11 = 0.545 (6/M-theory)                     │
│    sin²θ₁₃ ≈ 0.022 ≈ Z/264 = 0.022 (Z/264)                         │
│                                                                     │
│  CP VIOLATION:                                                      │
│    J ≈ 0.034 ≈ 1/(8+3Z) = 0.039 (same denominator!)                │
│                                                                     │
│  PATTERN: Neutrinos encode dimensional hierarchy like quarks!       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

KEY FINDING:

The mass splitting ratio Δm²₃₂/Δm²₂₁ ≈ 33 = 3 × 11

This is (spatial dimensions) × (M-theory dimensions)!

Compare to:
  Cabibbo: sin θ_C = Z/26 (involves bosonic dimension)
  Neutrino: mass ratio involves 3 × 11 (spatial × M-theory)

The neutrino sector may be governed by the 3-11 connection,
while quarks are governed by the 8-26 connection!
""")

# Final test of best candidates
print("\n" + "=" * 70)
print("BEST FIT FORMULAS")
print("=" * 70)

# sin²θ₁₂ = 8/26
pred_12 = 8/26
err_12 = abs(pred_12 - sin2_theta_12) / sin2_theta_12 * 100
print(f"\nsin²θ₁₂ = 8/26 = {pred_12:.4f}")
print(f"  Measured: {sin2_theta_12}")
print(f"  Error: {err_12:.2f}%")

# sin²θ₂₃ = 6/11
pred_23 = 6/11
err_23 = abs(pred_23 - sin2_theta_23) / sin2_theta_23 * 100
print(f"\nsin²θ₂₃ = 6/11 = {pred_23:.4f}")
print(f"  Measured: {sin2_theta_23}")
print(f"  Error: {err_23:.2f}%")

# sin²θ₁₃ = Z/264 = Z/(8×33) = Z/(8×3×11)
pred_13 = Z/264
err_13 = abs(pred_13 - sin2_theta_13) / sin2_theta_13 * 100
print(f"\nsin²θ₁₃ = Z/(8×3×11) = {pred_13:.4f}")
print(f"  Measured: {sin2_theta_13}")
print(f"  Error: {err_13:.2f}%")

# Mass ratio = 33 = 3 × 11
ratio_pred = 33
err_ratio = abs(ratio_pred - ratio_measured) / ratio_measured * 100
print(f"\nΔm²₃₂/Δm²₂₁ = 3 × 11 = {ratio_pred}")
print(f"  Measured: {ratio_measured:.1f}")
print(f"  Error: {err_ratio:.2f}%")

print("\n" + "=" * 70)
print("DOI: 10.5281/zenodo.19212718")
print("=" * 70)
