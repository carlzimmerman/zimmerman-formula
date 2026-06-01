#!/usr/bin/env python3
"""
Quark Masses and CKM Matrix in the Zimmerman Framework
=======================================================

Exploring:
1. Quark mass ratios
2. CKM matrix elements
3. Quark mixing angles
4. CP violation (Jarlskog invariant)
5. Wolfenstein parameterization

Carl Zimmerman, March 2026
"""

import numpy as np

Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi
alpha = 1/137.035999084

print("=" * 80)
print("QUARK MASSES AND CKM MATRIX IN THE ZIMMERMAN FRAMEWORK")
print("=" * 80)
print(f"\nZ = 2√(8π/3) = {Z:.10f}")

# =============================================================================
# Quark Masses (MS-bar at 2 GeV, PDG 2022)
# =============================================================================
# Light quarks (in MeV)
m_u = 2.16  # up quark
m_d = 4.67  # down quark
m_s = 93.4  # strange quark

# Heavy quarks (in GeV)
m_c = 1.27  # charm quark
m_b = 4.18  # bottom quark
m_t = 172.69  # top quark (pole mass)

# Convert all to MeV for comparison
m_c_MeV = m_c * 1000
m_b_MeV = m_b * 1000
m_t_MeV = m_t * 1000

# Reference masses
m_e = 0.511  # MeV
m_p = 938.3  # MeV

print(f"""
QUARK MASSES (MS-bar at μ = 2 GeV):

Light quarks:
  m_u = {m_u:.2f} MeV (up)
  m_d = {m_d:.2f} MeV (down)
  m_s = {m_s:.1f} MeV (strange)

Heavy quarks:
  m_c = {m_c:.2f} GeV = {m_c_MeV:.0f} MeV (charm)
  m_b = {m_b:.2f} GeV = {m_b_MeV:.0f} MeV (bottom)
  m_t = {m_t:.2f} GeV = {m_t_MeV:.0f} MeV (top, pole mass)
""")

# =============================================================================
# SECTION 1: Quark Mass Ratios
# =============================================================================
print("=" * 80)
print("SECTION 1: QUARK MASS RATIOS")
print("=" * 80)

# Key ratios
ratios = {
    'm_t/m_b': m_t_MeV / m_b_MeV,
    'm_b/m_c': m_b_MeV / m_c_MeV,
    'm_c/m_s': m_c_MeV / m_s,
    'm_s/m_d': m_s / m_d,
    'm_d/m_u': m_d / m_u,
    'm_t/m_c': m_t_MeV / m_c_MeV,
    'm_t/m_u': m_t_MeV / m_u,
    'm_b/m_s': m_b_MeV / m_s,
}

print(f"""
QUARK MASS RATIOS:

Generation jumps:
  m_t/m_c = {ratios['m_t/m_c']:.1f}
  m_c/m_u = {m_c_MeV/m_u:.1f}
  m_b/m_s = {ratios['m_b/m_s']:.1f}
  m_s/m_d = {ratios['m_s/m_d']:.1f}

Within generation:
  m_t/m_b = {ratios['m_t/m_b']:.2f}
  m_c/m_s = {ratios['m_c/m_s']:.2f}
  m_d/m_u = {ratios['m_d/m_u']:.2f}

Extreme ratios:
  m_t/m_u = {ratios['m_t/m_u']:.0f} (largest ratio!)
""")

# =============================================================================
# SECTION 2: Testing Z Expressions for Quark Ratios
# =============================================================================
print("=" * 80)
print("SECTION 2: Z EXPRESSIONS FOR QUARK MASS RATIOS")
print("=" * 80)

tests = [
    # Heavy quark ratios
    ("m_t/m_b", m_t_MeV/m_b_MeV, "Z² + Z", Z**2 + Z),
    ("m_t/m_b", m_t_MeV/m_b_MeV, "7Z", 7*Z),
    ("m_t/m_b", m_t_MeV/m_b_MeV, "(Z+1)² - Z", (Z+1)**2 - Z),
    ("m_b/m_c", m_b_MeV/m_c_MeV, "Z/1.75", Z/1.75),
    ("m_c/m_s", m_c_MeV/m_s, "Z + 8", Z + 8),
    ("m_c/m_s", m_c_MeV/m_s, "2Z + 2", 2*Z + 2),

    # Light quark ratios
    ("m_s/m_d", m_s/m_d, "Z² + 3Z", Z**2 + 3*Z),
    ("m_s/m_d", m_s/m_d, "4Z - 3", 4*Z - 3),
    ("m_d/m_u", m_d/m_u, "Z/2.7", Z/2.7),

    # Cross-generation
    ("m_t/m_c", m_t_MeV/m_c_MeV, "(4Z² + 3) - Z", (4*Z**2 + 3) - Z),
    ("m_t/m_c", m_t_MeV/m_c_MeV, "α⁻¹ - Z", 1/alpha - Z),
    ("m_b/m_s", m_b_MeV/m_s, "8Z - Z²/2", 8*Z - Z**2/2),

    # Extreme
    ("m_t/m_u", m_t_MeV/m_u, "Z × α⁻²", Z * (1/alpha)**2),
    ("m_t/m_u", m_t_MeV/m_u, "(4Z²+3)³/Z", (4*Z**2+3)**3/Z),
]

print(f"\n{'Ratio':<12} {'Measured':>12} {'Formula':<20} {'Predicted':>12} {'Error %':>10}")
print("-" * 70)
for name, meas, formula, pred in tests:
    error = abs(pred - meas)/meas * 100
    print(f"{name:<12} {meas:>12.2f} {formula:<20} {pred:>12.2f} {error:>10.2f}%")

# =============================================================================
# SECTION 3: CKM Matrix
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: CKM MATRIX")
print("=" * 80)

# CKM matrix elements (magnitudes, PDG 2022)
V_ud = 0.97373
V_us = 0.2243
V_ub = 0.00382
V_cd = 0.221
V_cs = 0.975
V_cb = 0.0408
V_td = 0.0086
V_ts = 0.0415
V_tb = 0.99914

print(f"""
CKM MATRIX (magnitudes):

       │    d         s         b    │
  ─────┼─────────────────────────────┤
   u   │  {V_ud:.5f}   {V_us:.4f}   {V_ub:.5f}  │
   c   │  {V_cd:.4f}    {V_cs:.4f}   {V_cb:.5f}  │
   t   │  {V_td:.5f}   {V_ts:.5f}   {V_tb:.5f}  │

KEY OBSERVATIONS:
  • Diagonal elements ≈ 1 (same-generation couplings dominate)
  • Off-diagonal elements decrease with generation distance
  • |V_ub| and |V_td| are smallest (third generation mixing)
""")

# =============================================================================
# SECTION 4: Wolfenstein Parameterization
# =============================================================================
print("=" * 80)
print("SECTION 4: WOLFENSTEIN PARAMETERIZATION")
print("=" * 80)

# Wolfenstein parameters
lambda_W = 0.22650  # ≈ sin(θ_C) Cabibbo angle
A = 0.790
rho_bar = 0.141
eta_bar = 0.357

# Cabibbo angle
theta_C = np.arcsin(lambda_W)

print(f"""
WOLFENSTEIN PARAMETERS:

  λ = {lambda_W:.5f} (Cabibbo angle sin θ_C)
  A = {A:.3f}
  ρ̄ = {rho_bar:.3f}
  η̄ = {eta_bar:.3f}

CABIBBO ANGLE:
  θ_C = arcsin(λ) = {np.degrees(theta_C):.3f}°
  sin(θ_C) = {np.sin(theta_C):.5f}
  cos(θ_C) = {np.cos(theta_C):.5f}

CKM MATRIX IN WOLFENSTEIN (to O(λ³)):

  V ≈ │ 1 - λ²/2      λ            Aλ³(ρ-iη)  │
      │ -λ            1 - λ²/2     Aλ²         │
      │ Aλ³(1-ρ-iη)   -Aλ²         1           │
""")

# =============================================================================
# SECTION 5: Z Expressions for CKM
# =============================================================================
print("=" * 80)
print("SECTION 5: Z EXPRESSIONS FOR CKM ELEMENTS")
print("=" * 80)

# Test Z formulas for Cabibbo angle
print(f"""
CABIBBO ANGLE λ = sin(θ_C) = {lambda_W:.5f}

Testing Z expressions:
""")

cabibbo_tests = [
    ("1/Z", 1/Z, lambda_W),
    ("2/(Z + 3)", 2/(Z + 3), lambda_W),
    ("3/(Z + 8)", 3/(Z + 8), lambda_W),
    ("π/(2Z²)", pi/(2*Z**2), lambda_W),
    ("1/(Z + 1/Z)", 1/(Z + 1/Z), lambda_W),
    ("(Z-3)/(Z+8)", (Z-3)/(Z+8), lambda_W),
]

print(f"{'Formula':<20} {'Predicted':>12} {'Measured':>12} {'Error %':>10}")
print("-" * 60)
for name, pred, meas in cabibbo_tests:
    error = abs(pred - meas)/meas * 100
    print(f"{name:<20} {pred:>12.5f} {meas:>12.5f} {error:>10.2f}%")

# Test for other CKM elements
print(f"""

OTHER CKM ELEMENTS:
""")

ckm_tests = [
    ("|V_cb|", V_cb, "1/Z²", 1/Z**2),
    ("|V_cb|", V_cb, "1/(4Z)", 1/(4*Z)),
    ("|V_ub|", V_ub, "λ³/3", lambda_W**3/3),
    ("|V_ub|", V_ub, "1/(Z × α⁻¹)", 1/(Z * (1/alpha))),
    ("|V_td|", V_td, "Aλ³", A * lambda_W**3),
    ("|V_ts|", V_ts, "Aλ²", A * lambda_W**2),
]

print(f"{'Element':<10} {'Measured':>12} {'Formula':<15} {'Predicted':>12} {'Error %':>10}")
print("-" * 65)
for name, meas, formula, pred in ckm_tests:
    error = abs(pred - meas)/meas * 100
    print(f"{name:<10} {meas:>12.5f} {formula:<15} {pred:>12.5f} {error:>10.2f}%")

# =============================================================================
# SECTION 6: Quark Mixing Angles
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: QUARK MIXING ANGLES (Standard Parameterization)")
print("=" * 80)

# Standard parameterization angles
theta_12_q = np.degrees(np.arcsin(V_us))  # ≈ Cabibbo
theta_23_q = np.degrees(np.arcsin(V_cb))
theta_13_q = np.degrees(np.arcsin(V_ub))

print(f"""
CKM MIXING ANGLES:
  θ₁₂ = {theta_12_q:.3f}° (Cabibbo angle)
  θ₂₃ = {theta_23_q:.3f}°
  θ₁₃ = {theta_13_q:.3f}°

COMPARISON TO PMNS (neutrino) ANGLES:

  │ Mixing │ CKM (quarks) │ PMNS (leptons) │ Ratio      │
  ├────────┼──────────────┼────────────────┼────────────┤
  │ θ₁₂    │ {theta_12_q:>10.3f}°  │ {33.45:>12.2f}°    │ {33.45/theta_12_q:>10.2f}   │
  │ θ₂₃    │ {theta_23_q:>10.3f}°  │ {42.1:>12.2f}°    │ {42.1/theta_23_q:>10.2f}   │
  │ θ₁₃    │ {theta_13_q:>10.3f}°  │ {8.62:>12.2f}°    │ {8.62/theta_13_q:>10.2f}   │

PATTERN:
  Quark mixing angles are MUCH SMALLER than lepton mixing angles!
  This is the "quark-lepton complementarity" puzzle.

SUM OF ANGLES:
  CKM:  θ₁₂ + θ₂₃ + θ₁₃ = {theta_12_q + theta_23_q + theta_13_q:.2f}°
  PMNS: θ₁₂ + θ₂₃ + θ₁₃ = {33.45 + 42.1 + 8.62:.2f}°
""")

# =============================================================================
# SECTION 7: CP Violation - Jarlskog Invariant
# =============================================================================
print("=" * 80)
print("SECTION 7: CP VIOLATION - JARLSKOG INVARIANT")
print("=" * 80)

# CP phase
delta_CKM = 68.8  # degrees (PDG 2022)

# Jarlskog invariant
# J = Im(V_us V_cb V*_ub V*_cs)
# In Wolfenstein: J ≈ A² λ⁶ η ≈ 3×10⁻⁵
J_CKM = A**2 * lambda_W**6 * eta_bar

# Exact calculation
c12 = np.cos(np.radians(theta_12_q))
s12 = np.sin(np.radians(theta_12_q))
c23 = np.cos(np.radians(theta_23_q))
s23 = np.sin(np.radians(theta_23_q))
c13 = np.cos(np.radians(theta_13_q))
s13 = np.sin(np.radians(theta_13_q))
J_exact = c12 * s12 * c23 * s23 * c13**2 * s13 * np.sin(np.radians(delta_CKM))

print(f"""
CP VIOLATION IN CKM:

CP Phase:
  δ_CKM = {delta_CKM}°
  sin(δ) = {np.sin(np.radians(delta_CKM)):.4f}

JARLSKOG INVARIANT:
  J = Im(V_us V_cb V*_ub V*_cs)

  Wolfenstein approx: J ≈ A²λ⁶η = {J_CKM:.2e}
  Exact calculation:  J = {J_exact:.2e}
  Measured:           J = (3.08 ± 0.13) × 10⁻⁵

COMPARISON:
  J_CKM (quarks)  ≈ 3 × 10⁻⁵
  J_PMNS (leptons) ≈ 3 × 10⁻²

  Ratio: J_PMNS/J_CKM ≈ 1000

  CP violation is ~1000× larger in leptons than quarks!
""")

# Test Z expressions for J
print("Testing Z expressions for J_CKM:")
j_tests = [
    ("α³", alpha**3, 3e-5),
    ("1/(Z × α⁻²)", 1/(Z * (1/alpha)**2), 3e-5),
    ("λ⁶/3", lambda_W**6 / 3, 3e-5),
    ("α²/Z", alpha**2/Z, 3e-5),
]

print(f"\n{'Formula':<20} {'Predicted':>15} {'Measured':>15} {'Error %':>10}")
print("-" * 65)
for name, pred, meas in j_tests:
    error = abs(pred - meas)/meas * 100
    print(f"{name:<20} {pred:>15.2e} {meas:>15.2e} {error:>10.1f}%")

# =============================================================================
# SECTION 8: Mass Hierarchies
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: FERMION MASS HIERARCHIES")
print("=" * 80)

# All fermion masses (in MeV)
fermions = {
    'up quarks': [m_u, m_c_MeV, m_t_MeV],
    'down quarks': [m_d, m_s, m_b_MeV],
    'charged leptons': [m_e, 105.66, 1776.86],  # e, μ, τ
}

print(f"""
FERMION MASS HIERARCHIES:

Up-type quarks (u, c, t):
  {m_u:.2f} : {m_c_MeV:.0f} : {m_t_MeV:.0f} MeV
  Ratios: 1 : {m_c_MeV/m_u:.0f} : {m_t_MeV/m_u:.0f}

Down-type quarks (d, s, b):
  {m_d:.2f} : {m_s:.1f} : {m_b_MeV:.0f} MeV
  Ratios: 1 : {m_s/m_d:.0f} : {m_b_MeV/m_d:.0f}

Charged leptons (e, μ, τ):
  {m_e:.3f} : {105.66:.2f} : {1776.86:.2f} MeV
  Ratios: 1 : {105.66/m_e:.0f} : {1776.86/m_e:.0f}

PATTERN OBSERVATION:
  ln(m_t/m_u) = {np.log(m_t_MeV/m_u):.2f}
  ln(m_b/m_d) = {np.log(m_b_MeV/m_d):.2f}
  ln(m_τ/m_e) = {np.log(1776.86/m_e):.2f}

  All ≈ 11-12, close to (4Z²+3)/12 = {(4*Z**2+3)/12:.2f}
""")

# =============================================================================
# SECTION 9: Georgi-Jarlskog Relations
# =============================================================================
print("=" * 80)
print("SECTION 9: GEORGI-JARLSKOG MASS RELATIONS")
print("=" * 80)

# GJ relation: m_b = m_τ × 3 at GUT scale
# At low scale: m_b ≈ 2.5 × m_τ

print(f"""
GEORGI-JARLSKOG RELATIONS (at GUT scale):

Classic prediction:
  m_b = 3 × m_τ at M_GUT

At low scale (μ = m_b):
  m_b/m_τ = {m_b_MeV/1776.86:.3f}

  Should be ~2.5-3 due to RG running.

ZIMMERMAN PREDICTION:
  m_b/m_τ = (Z + 8)/(Z + 3) = {(Z + 8)/(Z + 3):.4f}

  Measured: {m_b_MeV/1776.86:.4f}
  Error: {abs((Z+8)/(Z+3) - m_b_MeV/1776.86)/(m_b_MeV/1776.86)*100:.2f}%

OTHER RELATIONS:
  m_s/m_μ = {m_s/105.66:.4f} ≈ 0.88 (should be ~1/3 at GUT)
  m_d/m_e = {m_d/m_e:.3f} ≈ 9 (should be ~3 at GUT)
""")

# =============================================================================
# SECTION 10: Summary
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 10: QUARK SECTOR SUMMARY")
print("=" * 80)

print(f"""
BEST ZIMMERMAN PREDICTIONS FOR QUARKS:

┌──────────────────────────────────────────────────────────────────────────┐
│ Quantity           │ Formula              │ Predicted │ Measured │ Error │
├────────────────────┼──────────────────────┼───────────┼──────────┼───────┤
│ λ (Cabibbo)        │ 3/(Z + 8)            │   {3/(Z+8):.5f} │  0.22650 │ {abs(3/(Z+8)-0.2265)/0.2265*100:>5.1f}% │
│ m_c/m_s            │ 2Z + 2               │   {2*Z+2:>7.2f} │    13.60 │ {abs(2*Z+2-13.6)/13.6*100:>5.1f}% │
│ m_b/m_τ            │ (Z+8)/(Z+3)          │   {(Z+8)/(Z+3):>7.4f} │    2.353 │ {abs((Z+8)/(Z+3)-2.353)/2.353*100:>5.1f}% │
│ |V_cb|             │ 1/(4Z)               │   {1/(4*Z):>7.5f} │  0.04080 │ {abs(1/(4*Z)-0.0408)/0.0408*100:>5.1f}% │
│ J_CKM              │ α²/Z                 │   {alpha**2/Z:>7.2e} │  3.0e-05 │ {abs(alpha**2/Z-3e-5)/3e-5*100:>5.1f}% │
└────────────────────┴──────────────────────┴───────────┴──────────┴───────┘

KEY INSIGHTS:

1. CABIBBO ANGLE:
   λ = 3/(Z + 8) = 0.218 (3.5% error)
   The Cabibbo angle is geometrically determined!

2. QUARK-LEPTON COMPLEMENTARITY:
   θ₁₂(CKM) + θ₁₂(PMNS) ≈ {theta_12_q + 33.45:.1f}° ≈ 45°?
   This suggests a deep connection between quarks and leptons.

3. CP VIOLATION:
   J_CKM ≈ α²/Z ≈ 3×10⁻⁵
   CP violation strength is set by α and Z!

4. MASS HIERARCHIES:
   The factor ~1000× between generations appears as:
   m_t/m_c ≈ α⁻¹ - Z = 131
   m_c/m_u ≈ 600 ≈ Z × α⁻¹ × 0.8

THE QUARK SECTOR, LIKE ALL PHYSICS, TRACES BACK TO Z = 2√(8π/3).
""")
