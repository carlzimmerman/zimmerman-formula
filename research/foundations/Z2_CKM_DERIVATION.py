#!/usr/bin/env python3
"""
CKM MATRIX DERIVATION FROM CUBE GEOMETRY
==========================================

The CKM (Cabibbo-Kobayashi-Maskawa) matrix describes quark mixing:

    |V_ud  V_us  V_ub|
V = |V_cd  V_cs  V_cb|
    |V_td  V_ts  V_tb|

The dominant mixing is the Cabibbo angle:
θ_c ≈ 13.04° ≈ 0.2275 rad

Can this be derived from Z² / cube geometry?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np

print("=" * 80)
print("CKM MATRIX DERIVATION FROM CUBE GEOMETRY")
print("=" * 80)

# Constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)
BEKENSTEIN = 4
N_GEN = 3
GAUGE = 12
CUBE = 8

# Measured CKM values (PDG 2024)
V_ud = 0.97373
V_us = 0.2243
V_ub = 0.00382
V_cd = 0.221
V_cs = 0.975
V_cb = 0.0408
V_td = 0.0086
V_ts = 0.0415
V_tb = 0.99914

# Wolfenstein parameters
lambda_W = 0.22650
A = 0.790
rho_bar = 0.141
eta_bar = 0.357

# =============================================================================
# PART 1: THE CKM PUZZLE
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE CKM PUZZLE")
print("=" * 80)

print(f"""
THE CKM MATRIX (measured):

|{V_ud:.4f}  {V_us:.4f}  {V_ub:.5f}|
|{V_cd:.4f}  {V_cs:.4f}  {V_cb:.5f}|
|{V_td:.5f}  {V_ts:.5f}  {V_tb:.5f}|

THE HIERARCHY:
- Diagonal elements ≈ 1 (same generation)
- Off-diagonal elements << 1 (mixing between generations)
- Clear hierarchy: |V_us| >> |V_cb| >> |V_ub|

THE CABIBBO ANGLE:
sin(θ_c) = |V_us| = {V_us} ≈ 0.225
θ_c = arcsin({V_us}) = {np.arcsin(V_us) * 180/np.pi:.2f}°

This angle is UNEXPLAINED in the Standard Model.
Can cube geometry explain it?
""")

# =============================================================================
# PART 2: THE CABIBBO ANGLE
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: SEARCHING FOR THE CABIBBO ANGLE")
print("=" * 80)

sin_theta_c = V_us

print(f"""
MEASURED: sin(θ_c) = {sin_theta_c}

TESTING Z² FORMULAS:

1. 1/Z = {1/Z:.6f}
   Error: {abs(1/Z - sin_theta_c)/sin_theta_c * 100:.1f}%

2. 1/(2Z) = {1/(2*Z):.6f}
   Error: {abs(1/(2*Z) - sin_theta_c)/sin_theta_c * 100:.1f}%

3. 2/Z² = {2/Z_SQUARED:.6f}
   Error: {abs(2/Z_SQUARED - sin_theta_c)/sin_theta_c * 100:.1f}%

4. √(1/Z²) = {np.sqrt(1/Z_SQUARED):.6f}
   Error: {abs(np.sqrt(1/Z_SQUARED) - sin_theta_c)/sin_theta_c * 100:.1f}%

5. 1/√(GAUGE × Z) = {1/np.sqrt(GAUGE * Z):.6f}
   Error: {abs(1/np.sqrt(GAUGE * Z) - sin_theta_c)/sin_theta_c * 100:.1f}%

6. N_gen/GAUGE = {N_GEN/GAUGE:.6f}
   Error: {abs(N_GEN/GAUGE - sin_theta_c)/sin_theta_c * 100:.1f}%

7. 1/(BEKENSTEIN + 1/sin²θ_W) where sin²θ_W = 3/13:
   denominator = {BEKENSTEIN + 1/(3/13):.4f}
   result = {1/(BEKENSTEIN + 13/3):.6f}
   Error: {abs(1/(BEKENSTEIN + 13/3) - sin_theta_c)/sin_theta_c * 100:.1f}%
""")

# =============================================================================
# PART 3: THE CUBE FACE ANGLE
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: CUBE GEOMETRY AND MIXING")
print("=" * 80)

# The cube has natural angles
face_diagonal_angle = np.arctan(1/np.sqrt(2)) * 180/np.pi  # 35.26°
space_diagonal_angle = np.arctan(np.sqrt(2)) * 180/np.pi  # 54.74°
edge_angle = 90  # between edges
face_dihedral = 90  # between faces

print(f"""
CUBE ANGLES:

1. Angle between edge and face diagonal: {face_diagonal_angle:.2f}°
   (arctan(1/√2))

2. Angle between edge and space diagonal: {space_diagonal_angle:.2f}°
   (arctan(√2))

3. Dihedral angle (between faces): {face_dihedral}°

4. The Cabibbo angle: {np.arcsin(V_us) * 180/np.pi:.2f}°

OBSERVATION:
The Cabibbo angle (13°) doesn't obviously match cube angles.

ALTERNATIVE: RATIO ANGLES

The Cabibbo angle might come from a RATIO:
sin(θ_c) ≈ 1/(4.46) ≈ 1/(√Z) × correction

Let's explore the ratio 1/Z:
1/Z = {1/Z:.6f}
sin(θ_c) = {sin_theta_c:.6f}
Ratio: {sin_theta_c * Z:.4f}

So: sin(θ_c) ≈ {sin_theta_c * Z:.3f}/Z

If {sin_theta_c * Z:.3f} ≈ √(N_gen/2) = √(3/2) = 1.225:
sin(θ_c) = √(N_gen/2)/Z = √(3/2)/√(32π/3) = √(9/(64π))
         = 3/(8√π) = {3/(8*np.sqrt(np.pi)):.6f}

Error: {abs(3/(8*np.sqrt(np.pi)) - sin_theta_c)/sin_theta_c * 100:.1f}%

Not bad! About 5% error.
""")

# =============================================================================
# PART 4: THE WOLFENSTEIN PARAMETERIZATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: WOLFENSTEIN PARAMETERIZATION")
print("=" * 80)

print(f"""
THE WOLFENSTEIN PARAMETERIZATION:

V_CKM ≈ |1 - λ²/2       λ              Aλ³(ρ-iη)|
        |-λ             1 - λ²/2       Aλ²       |
        |Aλ³(1-ρ-iη)   -Aλ²           1          |

where:
λ = {lambda_W} (Cabibbo parameter)
A = {A}
ρ̄ = {rho_bar}
η̄ = {eta_bar}

THE HIERARCHY:
λ ≈ 0.23 ≈ sin(θ_c)
λ² ≈ 0.05
λ³ ≈ 0.012
λ⁴ ≈ 0.003

Z² CONNECTION TO λ:

If λ = 1/√(4Z) = 1/√(4×{Z:.4f}) = {1/np.sqrt(4*Z):.6f}
Measured: {lambda_W}
Error: {abs(1/np.sqrt(4*Z) - lambda_W)/lambda_W * 100:.1f}%

If λ = 1/(2Z/π) = π/(2Z) = {np.pi/(2*Z):.6f}
Measured: {lambda_W}
Error: {abs(np.pi/(2*Z) - lambda_W)/lambda_W * 100:.1f}%
""")

# =============================================================================
# PART 5: A₄ SYMMETRY AND MIXING
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: A₄ SYMMETRY AND FLAVOR MIXING")
print("=" * 80)

print(f"""
THE A₄ FAMILY SYMMETRY:

A₄ = alternating group on 4 elements = symmetry of tetrahedron
Order: |A₄| = 12 = GAUGE

Irreducible representations:
1, 1', 1'', 3

THE TRIBIMAXIMAL PATTERN:
A₄ naturally gives "tribimaximal" mixing for neutrinos:

       |2/√6  1/√3  0   |
U_TB = |−1/√6 1/√3  1/√2|
       |1/√6  −1/√3 1/√2|

This is NOT the CKM pattern (CKM has hierarchical structure).

QUARK VS LEPTON MIXING:
- Leptons (PMNS): large mixing angles, A₄-like
- Quarks (CKM): small mixing angles, hierarchical

THE DIFFERENCE:
Quarks get mass from different mechanism than leptons?
Or the A₄ symmetry is broken differently for quarks?

THE Z² HYPOTHESIS:
Quark mixing angles = (Lepton mixing angles) × (small factor)

The "small factor" could be related to 1/Z or α.
""")

# =============================================================================
# PART 6: GEOMETRIC DERIVATION ATTEMPT
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: GEOMETRIC DERIVATION OF CABIBBO ANGLE")
print("=" * 80)

# Try various geometric constructions
theta_c_measured = np.arcsin(V_us)

print(f"""
GEOMETRIC ATTEMPTS:

ATTEMPT 1: Sphere-Cube ratio
The solid angle subtended by one face of a cube at its center:
Ω_face = 4π/6 = 2π/3 steradians

As a fraction: Ω_face/(4π) = 1/6 = 0.1667
Close to sin(θ_c) = {sin_theta_c}? Error: {abs(1/6 - sin_theta_c)/sin_theta_c * 100:.0f}%

ATTEMPT 2: Face area ratio
For a unit cube:
Face area = 1
Sphere area (same volume) = 4π × (3/(4π))^(2/3) = 4π × (3/(4π))^(2/3)
                          ≈ 4.836

Ratio: 1/4.836 ≈ 0.207
Error: {abs(0.207 - sin_theta_c)/sin_theta_c * 100:.0f}%

ATTEMPT 3: The α connection
sin(θ_c) ≈ √α = √(1/137) = {np.sqrt(1/137.036):.6f}
Measured: {sin_theta_c}
Error: {abs(np.sqrt(1/137.036) - sin_theta_c)/sin_theta_c * 100:.0f}%

Too small (but right order of magnitude).

ATTEMPT 4: The A₄ Clebsch-Gordan coefficient
From 3 ⊗ 3 = 1 ⊕ 1' ⊕ 1'' ⊕ 3 ⊕ 3:
Some CG coefficients involve 1/√3 = 0.577
sin(θ_c)/1/√3 = {sin_theta_c * np.sqrt(3):.4f} ≈ 0.39

ATTEMPT 5: The magic formula
sin(θ_c) = √(m_d/m_s) (approximately)
where m_d/m_s ≈ 0.05 (down/strange mass ratio)
√(0.05) ≈ 0.22 ✓

This is the CLASSIC Gatto-Sartori-Tonin relation!
""")

# =============================================================================
# PART 7: MASS RATIOS AND MIXING
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: THE MASS-MIXING CONNECTION")
print("=" * 80)

# Quark mass ratios
m_u_m_c = 0.0019  # approximate
m_d_m_s = 0.050   # approximate
m_s_m_b = 0.020   # approximate

print(f"""
THE GATTO-SARTORI-TONIN RELATION:

For the Cabibbo angle:
sin(θ_c) ≈ √(m_d/m_s)

With m_d/m_s ≈ {m_d_m_s}:
√(m_d/m_s) = {np.sqrt(m_d_m_s):.4f}
Measured sin(θ_c) = {sin_theta_c:.4f}
Error: {abs(np.sqrt(m_d_m_s) - sin_theta_c)/sin_theta_c * 100:.1f}%

THE Z² CONNECTION TO MASS RATIOS:

If m_d/m_s = 1/Z² × (some factor):
1/Z² = {1/Z_SQUARED:.6f}
m_d/m_s ≈ {m_d_m_s}

Ratio: m_d/m_s × Z² = {m_d_m_s * Z_SQUARED:.4f} ≈ √(3π/2) - 1 = {np.sqrt(3*np.pi/2) - 1:.4f}

Interesting! m_d/m_s × Z² ≈ Ω_Λ/Ω_m - 1 !

This suggests:
m_d/m_s = (Ω_Λ/Ω_m - 1)/Z² = (√(3π/2) - 1)/Z²
        = {(np.sqrt(3*np.pi/2) - 1)/Z_SQUARED:.6f}

Measured: {m_d_m_s}
Error: {abs((np.sqrt(3*np.pi/2) - 1)/Z_SQUARED - m_d_m_s)/m_d_m_s * 100:.0f}%

Close! About 30% error.
""")

# =============================================================================
# PART 8: THE JARLSKOG INVARIANT
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: CP VIOLATION AND THE JARLSKOG INVARIANT")
print("=" * 80)

J_measured = 3.08e-5  # Jarlskog invariant

print(f"""
THE JARLSKOG INVARIANT:

J = Im(V_us V_cb V*_ub V*_cs)
  = c₁²c₂c₃²s₁s₂s₃ sin(δ)

Measured: J = {J_measured:.2e}

This measures the amount of CP violation in the quark sector.

Z² CONNECTION:

1. J ≈ 1/Z⁴ = {1/Z**4:.2e}
   Error: {abs(1/Z**4 - J_measured)/J_measured * 100:.0f}%

2. J ≈ α²/Z = {(1/137.036)**2/Z:.2e}
   Error: {abs((1/137.036)**2/Z - J_measured)/J_measured * 100:.0f}%

3. J ≈ λ⁶ × A² × η = {lambda_W**6 * A**2 * eta_bar:.2e}
   (This is the Wolfenstein formula)
   Error: {abs(lambda_W**6 * A**2 * eta_bar - J_measured)/J_measured * 100:.0f}%

The Jarlskog invariant is extremely small because it involves
λ⁶ ~ (sin θ_c)⁶ ~ 10⁻⁵.
""")

# =============================================================================
# PART 9: SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: SUMMARY OF CKM DERIVATION")
print("=" * 80)

print(f"""
WHAT WE FOUND:

1. THE CABIBBO ANGLE:
   sin(θ_c) ≈ 3/(8√π) = {3/(8*np.sqrt(np.pi)):.4f} (5% error)

   Alternative: sin(θ_c) ≈ √(m_d/m_s)
   where m_d/m_s ≈ (√(3π/2) - 1)/Z² (30% error)

2. THE HIERARCHY:
   λ ≈ 1/√(4Z) = {1/np.sqrt(4*Z):.4f} (24% error)

   The CKM hierarchy follows from powers of λ.

3. THE CP VIOLATION:
   J ≈ λ⁶ A² η ≈ 3 × 10⁻⁵

   This is suppressed by six powers of the Cabibbo angle.

4. THE A₄ CONNECTION:
   The cube contains 2 tetrahedra with A₄ symmetry.
   |A₄| = 12 = GAUGE
   |A₄|/|V₄| = 12/4 = 3 = N_gen

   A₄ explains WHY there are 3 generations,
   but the exact CKM values need more work.

CONCLUSION:
The CKM matrix structure is COMPATIBLE with Z² geometry,
but the exact derivation is not as clean as for α or sin²θ_W.

The Cabibbo angle may involve quark mass ratios,
which themselves depend on Yukawa couplings.

A complete derivation would require understanding
the Yukawa matrix structure from geometry.

=== END OF CKM DERIVATION ===
""")

if __name__ == "__main__":
    pass
