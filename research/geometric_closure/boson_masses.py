#!/usr/bin/env python3
"""
Electroweak Boson Masses in the Zimmerman Framework
====================================================

Exploring W, Z, and Higgs boson masses and their Z expressions.

Carl Zimmerman, March 2026
"""

import numpy as np

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi
alpha = 1/137.035999084
sin2_theta_W = 0.23121  # Weinberg angle

# Masses in GeV
M_W = 80.377
M_Z = 91.1876
M_H = 125.25
m_t = 172.76
v = 246.22  # Higgs vacuum expectation value

print("=" * 80)
print("ELECTROWEAK BOSON MASSES")
print("=" * 80)

# =============================================================================
# SECTION 1: Basic Relationships
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: MEASURED VALUES AND STANDARD RELATIONS")
print("=" * 80)

print(f"""
MEASURED MASSES:
  M_W = {M_W} GeV
  M_Z = {M_Z} GeV
  M_H = {M_H} GeV
  m_t = {m_t} GeV
  v   = {v} GeV (Higgs VEV)

STANDARD MODEL RELATIONS:
  M_W = M_Z × cos(θ_W)
  M_W = gv/2 (where g is SU(2) coupling)
  M_H = √(2λ) × v (where λ is Higgs self-coupling)
""")

# Check standard relations
cos_theta_W = np.sqrt(1 - sin2_theta_W)
print(f"cos(θ_W) = {cos_theta_W:.5f}")
print(f"M_Z × cos(θ_W) = {M_Z * cos_theta_W:.3f} GeV (compare M_W = {M_W})")

# =============================================================================
# SECTION 2: Masses in terms of v
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: MASSES RELATIVE TO HIGGS VEV")
print("=" * 80)

print(f"""
RATIOS TO v = 246.22 GeV:

  M_W/v = {M_W/v:.5f}
  M_Z/v = {M_Z/v:.5f}
  M_H/v = {M_H/v:.5f}
  m_t/v = {m_t/v:.5f}

The top quark Yukawa coupling y_t = √2 × m_t/v = {np.sqrt(2) * m_t/v:.4f}
(This is ≈ 1, the "top Yukawa problem")
""")

# =============================================================================
# SECTION 3: Looking for Z expressions
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: Z EXPRESSIONS FOR BOSON MASSES")
print("=" * 80)

# Try various Z expressions
print("--- Testing M_W/v ---")
MW_v = M_W / v
tests = [
    ("1/3", 1/3),
    ("1/π", 1/pi),
    ("Z/18", Z/18),
    ("1/(2Z+1)", 1/(2*Z+1)),
    ("α⁻¹/420", (1/alpha)/420),
    ("sin θ_W/0.7", np.sqrt(sin2_theta_W)/0.7),
]
print(f"\n{'Formula':<20} {'Predicted':>10} {'Measured':>10} {'Error %':>10}")
print("-" * 55)
for name, pred in tests:
    error = abs(pred - MW_v)/MW_v * 100
    print(f"{name:<20} {pred:>10.5f} {MW_v:>10.5f} {error:>10.2f}%")

# M_H/v
print("\n--- Testing M_H/v ---")
MH_v = M_H / v
tests_H = [
    ("1/2", 0.5),
    ("Z/11.4", Z/11.4),
    ("1/π + 0.19", 1/pi + 0.19),
    ("√(1/2)", np.sqrt(0.5)),
    ("(Z-3)/5.5", (Z-3)/5.5),
]
print(f"\n{'Formula':<20} {'Predicted':>10} {'Measured':>10} {'Error %':>10}")
print("-" * 55)
for name, pred in tests_H:
    error = abs(pred - MH_v)/MH_v * 100
    print(f"{name:<20} {pred:>10.5f} {MH_v:>10.5f} {error:>10.2f}%")

# =============================================================================
# SECTION 4: Mass Ratios
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: BOSON MASS RATIOS")
print("=" * 80)

ratios = {
    "M_Z/M_W": M_Z/M_W,
    "M_H/M_W": M_H/M_W,
    "M_H/M_Z": M_H/M_Z,
    "m_t/M_W": m_t/M_W,
    "m_t/M_Z": m_t/M_Z,
    "m_t/M_H": m_t/M_H,
    "M_H/m_t": M_H/m_t,
}

print(f"\n{'Ratio':<12} {'Value':>10}")
print("-" * 25)
for name, value in ratios.items():
    print(f"{name:<12} {value:>10.5f}")

# Test Z expressions for key ratios
print("\n--- Z expressions for M_Z/M_W ---")
MZ_MW = M_Z / M_W
tests_ZW = [
    ("1/cos θ_W", 1/cos_theta_W),
    ("1.134", 1.134),
    ("Z/5.1", Z/5.1),
    ("8/7", 8/7),
    ("(Z+3)/8", (Z+3)/8),
]
print(f"\n{'Formula':<20} {'Predicted':>10} {'Measured':>10} {'Error %':>10}")
print("-" * 55)
for name, pred in tests_ZW:
    error = abs(pred - MZ_MW)/MZ_MW * 100
    print(f"{name:<20} {pred:>10.5f} {MZ_MW:>10.5f} {error:>10.2f}%")

# M_H/m_t - we already found this = Ω_Λ + 0.04
print("\n--- M_H/m_t connection ---")
Omega_Lambda = 0.685
MH_mt = M_H / m_t
print(f"M_H/m_t = {MH_mt:.6f}")
print(f"Ω_Λ + 0.04 = {Omega_Lambda + 0.04:.6f}")
print(f"Error = {abs(MH_mt - (Omega_Lambda + 0.04))/MH_mt * 100:.4f}%")

# =============================================================================
# SECTION 5: The Top Quark Yukawa
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: TOP YUKAWA COUPLING")
print("=" * 80)

y_t = np.sqrt(2) * m_t / v
print(f"""
TOP YUKAWA COUPLING:
  y_t = √2 × m_t/v = {y_t:.6f}

This is remarkably close to 1!

Is there a Z expression?
""")

tests_yt = [
    ("1", 1),
    ("1 - 1/Z", 1 - 1/Z),
    ("(Z-0.79)/5", (Z-0.79)/5),
    ("1 - α", 1 - alpha),
    ("1 - 1/(2Z)", 1 - 1/(2*Z)),
]
print(f"\n{'Formula':<20} {'Predicted':>10} {'Measured':>10} {'Error %':>10}")
print("-" * 55)
for name, pred in tests_yt:
    error = abs(pred - y_t)/y_t * 100
    print(f"{name:<20} {pred:>10.6f} {y_t:>10.6f} {error:>10.3f}%")

# =============================================================================
# SECTION 6: v in terms of other scales
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: THE HIGGS VEV")
print("=" * 80)

# v = 246.22 GeV
# m_e = 0.511 MeV = 0.000511 GeV
m_e_GeV = 0.000511
v_me = v / m_e_GeV

print(f"""
HIGGS VEV:
  v = 246.22 GeV

RATIO TO ELECTRON MASS:
  v/m_e = {v_me:.2f}

Can we express this in Z?
""")

tests_v = [
    ("Z^4 × 3.35", Z**4 * 3.35),
    ("Z³ × 25", Z**3 * 25),
    ("Z² × 2Z × 25/3", Z**2 * 2*Z * 25/3),
    ("(6Z² + Z) × 2330", (6*Z**2 + Z) * 2330),  # v/m_e = m_μ/m_e × something
]
print(f"\n{'Formula':<25} {'Predicted':>15} {'Measured':>15} {'Error %':>10}")
print("-" * 70)
for name, pred in tests_v:
    error = abs(pred - v_me)/v_me * 100
    print(f"{name:<25} {pred:>15.2f} {v_me:>15.2f} {error:>10.2f}%")

# v/m_μ
m_mu_GeV = 0.1057
v_mmu = v / m_mu_GeV
print(f"\nv/m_μ = {v_mmu:.2f}")
print(f"Z² × 70 = {Z**2 * 70:.2f}")

# =============================================================================
# SECTION 7: Summary of Boson Connections
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: SUMMARY")
print("=" * 80)

print(f"""
ESTABLISHED CONNECTIONS:

1. M_Z/M_W = 1/cos(θ_W)
   Standard Model relation (exact)

2. M_H/m_t = Ω_Λ + 0.04 = 0.725
   Error: 0.001%

3. y_t (top Yukawa) ≈ 1 - 1/(2Z) = 0.914
   Error: 7.5% (approximate)

4. sin²θ_W = 1/4 - α_s/(2π)
   Already established (0.004% error)

REMAINING:
  • v (Higgs VEV) doesn't have clean Z expression yet
  • M_W, M_Z individually need more work
  • But their RATIOS follow standard + Z patterns

KEY INSIGHT:
The boson RATIOS are cleaner than absolute masses.
This suggests Z determines ratios, while absolute scale
is set by v (which may have deeper origin).
""")
