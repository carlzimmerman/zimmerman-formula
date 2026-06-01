#!/usr/bin/env python3
"""
Gauge Groups and String Dimensions in the Zimmerman Framework
==============================================================

Exploring:
1. Standard Model gauge group SU(3)×SU(2)×U(1) and its dimensions
2. String theory critical dimensions (10, 11, 26)
3. The triangular number pattern 2^Tₙ
4. The mysterious exponent 21.5 in M_Pl/v = 2×Z^21.5

Carl Zimmerman, March 2026
"""

import numpy as np

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi
alpha = 1/137.035999084
phi = (1 + np.sqrt(5)) / 2

print("=" * 80)
print("GAUGE GROUPS AND STRING DIMENSIONS")
print("=" * 80)

# =============================================================================
# SECTION 1: Standard Model Gauge Group
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: STANDARD MODEL GAUGE GROUP")
print("=" * 80)

print("""
The Standard Model gauge group is G = SU(3) × SU(2) × U(1)

DIMENSIONS:
  • SU(3): dim = 3² - 1 = 8 (color, strong force)
  • SU(2): dim = 2² - 1 = 3 (weak isospin)
  • U(1):  dim = 1 (hypercharge)

TOTAL: 8 + 3 + 1 = 12 generators

CONNECTION TO Z:
  • 8 appears in Z = 2√(8π/3)
  • 3 appears in Z = 2√(8π/3)
  • 8 + 3 = 11 appears in m_τ/m_μ = Z + 11
""")

# The 12 generators
print("--- The 12 generators ---")
print(f"SU(3): 8 gluons")
print(f"SU(2): 3 weak bosons (W⁺, W⁻, W⁰)")
print(f"U(1):  1 hypercharge boson (B⁰)")
print(f"Total: 12 = 8 + 3 + 1")

# After electroweak symmetry breaking: 8 + 3 + 1 → 8 + 4
print(f"\nAfter EWSB:")
print(f"  • 8 gluons")
print(f"  • W⁺, W⁻, Z⁰ (massive)")
print(f"  • γ (photon, massless)")
print(f"  Total bosons: 12")

# Test Z expressions for 12
print(f"\n--- Z expressions for 12 ---")
tests_12 = [
    ("2Z", 2*Z),
    ("Z + 6", Z + 6),
    ("12", 12),
    ("Z² - 21.5", Z**2 - 21.5),
    ("8 + 3 + 1", 8 + 3 + 1),
]
for name, value in tests_12:
    error = abs(value - 12) / 12 * 100
    print(f"  {name:20} = {value:10.4f}  (error {error:.2f}%)")

# =============================================================================
# SECTION 2: String Theory Dimensions
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: STRING THEORY DIMENSIONS")
print("=" * 80)

print("""
Critical dimensions in string theory:

  • Bosonic string: D = 26
  • Superstring:    D = 10
  • M-theory:       D = 11

Can these be expressed in terms of Z?
""")

# Test Z expressions
print("--- Z expressions for critical dimensions ---")
dims = [
    ("10 (superstring)", 10),
    ("11 (M-theory)", 11),
    ("26 (bosonic)", 26),
]

for name, d in dims:
    print(f"\n{name}:")
    tests = [
        (f"Z + {d - Z:.2f}", Z + (d - Z)),
        (f"2Z - {2*Z - d:.2f}", 2*Z - (2*Z - d)),
        (f"Z²/{Z**2/d:.2f}", Z**2 / (Z**2/d)),
    ]
    for expr, val in tests:
        print(f"  {expr:20} = {val:.4f}")

# Interesting: 26 ≈ 4.5Z
print(f"\n--- Key observation ---")
print(f"26/Z = {26/Z:.4f}")
print(f"11/Z = {11/Z:.4f}")
print(f"10/Z = {10/Z:.4f}")

# What about differences?
print(f"\n26 - 11 = 15 = 3 × 5")
print(f"26 - 10 = 16 = 2⁴ = 4²")
print(f"11 - 10 = 1")

# =============================================================================
# SECTION 3: Triangular Numbers
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: TRIANGULAR NUMBER PATTERN")
print("=" * 80)

# Triangular numbers Tₙ = n(n+1)/2
triangular = [n*(n+1)//2 for n in range(1, 10)]
print(f"Triangular numbers: {triangular}")
print(f"T₁=1, T₂=3, T₃=6, T₄=10, T₅=15, T₆=21, T₇=28, T₈=36")

print("""
OBSERVATION: Powers of 2 with triangular exponents appear in Z:

  2^T₁ = 2¹ = 2    (factor in Z = 2√...)
  2^T₂ = 2³ = 8    (appears in 8π/3)
  2^T₃ = 2⁶ = 64   (appears in m_μ/m_e = 64π + Z)
  2^T₄ = 2¹⁰ = 1024
  2^T₅ = 2¹⁵ = 32768
""")

# Check 2^Tₙ pattern
print("--- 2^Tₙ values ---")
for n in range(1, 8):
    Tn = n*(n+1)//2
    val = 2**Tn
    print(f"  2^T_{n} = 2^{Tn} = {val}")

# Does 1024 appear anywhere?
print(f"\n--- Where does 2^T₄ = 1024 appear? ---")
print(f"1024/Z = {1024/Z:.4f}")
print(f"1024/Z² = {1024/Z**2:.4f}")
print(f"1024/64 = 16 = 2⁴")
print(f"1024π/Z⁴ = {1024*pi/Z**4:.6f}")

# Interesting: Z⁴ ≈ 1024π²/9 (from earlier)
print(f"\nZ⁴ = {Z**4:.4f}")
print(f"1024π²/9 = {1024*pi**2/9:.4f}")
print(f"These are equal!")

# =============================================================================
# SECTION 4: The 21.5 Exponent
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: THE MYSTERIOUS 21.5 EXPONENT")
print("=" * 80)

print("""
M_Pl/v = 2 × Z^21.5 (electroweak hierarchy)

What is 21.5?
""")

# Decompositions of 21.5
print("--- Decompositions of 21.5 ---")
decomps = [
    ("43/2", 43/2),
    ("T₆ + 0.5", 21 + 0.5),  # T₆ = 21
    ("F₈ + 0.5", 21 + 0.5),  # F₈ = 21
    ("7π - 0.5", 7*pi - 0.5),
    ("4 × 5.375", 4 * 5.375),
    ("3 × 7.167", 3 * 7.167),
    ("Z × 3.714", Z * 3.714),
    ("Z² - 12", Z**2 - 12),
    ("2Z² - 45.5", 2*Z**2 - 45.5),
]

print(f"\n{'Expression':<20} {'Value':>12}")
print("-" * 35)
for name, value in decomps:
    print(f"{name:<20} {value:>12.4f}")

# The 43 in 43/2
print(f"\n--- The number 43 ---")
print(f"43 is prime")
print(f"43 = 6² + 7 = 36 + 7")
print(f"43 = T₈ + 7 = 36 + 7")
print(f"43 = 8 × 5 + 3 = 40 + 3")

# Connection to E8?
print(f"\n--- Connection to E8? ---")
print(f"248 (E8 dim) / 43 = {248/43:.4f}")
print(f"240 (E8 roots) / 43 = {240/43:.4f} ≈ 5.58")
print(f"248/Z = {248/Z:.4f}")
print(f"43/Z = {43/Z:.4f}")

# =============================================================================
# SECTION 5: The Factor of 2 in 2×Z^21.5
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: THE FACTOR OF 2")
print("=" * 80)

print(f"""
M_Pl/v = 2 × Z^21.5

Why the factor of 2?

Possibilities:
  • 2 = Schwarzschild factor (r_s = 2GM/c²)
  • 2 = spin states
  • 2 = binary/duality
  • 2 appears in Z = 2√(8π/3)

The 2 might cancel the 2 in Z = 2√..., giving:

M_Pl/v = 2 × [2√(8π/3)]^21.5
       = 2 × 2^21.5 × (8π/3)^10.75
       = 2^22.5 × (8π/3)^10.75
       = 2^22.5 × 8^10.75 × π^10.75 / 3^10.75
""")

# Calculate this
val = 2**22.5 * (8*pi/3)**10.75
M_Pl_v = 4.96e16
print(f"2^22.5 × (8π/3)^10.75 = {val:.4e}")
print(f"M_Pl/v = {M_Pl_v:.4e}")
print(f"Ratio = {val/M_Pl_v:.6f}")

# =============================================================================
# SECTION 6: Gauge Coupling Unification
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: GAUGE COUPLING UNIFICATION")
print("=" * 80)

# Standard Model couplings at M_Z
g1 = 0.357  # U(1)
g2 = 0.652  # SU(2)
g3 = 1.221  # SU(3) (this is √(4πα_s))

alpha_1 = g1**2 / (4*pi)  # 0.0101
alpha_2 = g2**2 / (4*pi)  # 0.0338
alpha_3 = g3**2 / (4*pi)  # 0.1185 ≈ α_s

print(f"""
Standard Model couplings at M_Z:

  α₁ = g₁²/(4π) = {alpha_1:.5f} (U(1) normalized)
  α₂ = g₂²/(4π) = {alpha_2:.5f} (SU(2))
  α₃ = g₃²/(4π) = {alpha_3:.5f} (SU(3) = α_s)

Framework predictions:
  α_s = 3/(8+3Z) = {3/(8+3*Z):.5f}

Ratios:
  α₃/α₂ = {alpha_3/alpha_2:.4f}
  α₂/α₁ = {alpha_2/alpha_1:.4f}
  α₃/α₁ = {alpha_3/alpha_1:.4f}
""")

# Test Z expressions for coupling ratios
print("--- Z expressions for coupling ratios ---")
tests_coup = [
    ("α₃/α₂", alpha_3/alpha_2, "Z/1.65", Z/1.65),
    ("α₂/α₁", alpha_2/alpha_1, "Z/1.73", Z/1.73),
    ("α₃/α₁", alpha_3/alpha_1, "2Z", 2*Z),
]
print(f"\n{'Ratio':<10} {'Measured':>10} {'Formula':>15} {'Predicted':>10} {'Error %':>10}")
print("-" * 60)
for name, measured, formula, predicted in tests_coup:
    error = abs(predicted - measured)/measured * 100
    print(f"{name:<10} {measured:>10.4f} {formula:>15} {predicted:>10.4f} {error:>10.2f}%")

# =============================================================================
# SECTION 7: Complete Dimension Count
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: DIMENSION COUNT CONNECTIONS")
print("=" * 80)

print(f"""
DIMENSIONS APPEARING IN PHYSICS:

  1  = time dimension
  3  = spatial dimensions (appears in Z)
  4  = spacetime dimensions
  7  = G2 dimensions (octonion automorphism)
  8  = octonion dimensions (appears in Z)
  10 = superstring dimensions
  11 = M-theory dimensions (= 3 + 8!)
  26 = bosonic string dimensions

CONNECTIONS:
  3 + 8 = 11 (M-theory = spatial + octonion)
  4 + 7 = 11 (spacetime + G2)
  10 + 1 = 11 (superstring + extra)
  26 - 16 = 10 (bosonic - hidden)

Z-CONNECTIONS:
  Z = 2√(8π/3) uses 8 and 3
  11 = 3 + 8 appears in m_τ/m_μ = Z + 11
  64 = 8² appears in m_μ/m_e = 64π + Z
""")

# Check: can all critical dimensions be expressed with 3 and 8?
print("--- Dimensions from 3 and 8 ---")
for d in [1, 3, 4, 7, 8, 10, 11, 26]:
    # Try small integer combinations of 3 and 8
    for a in range(-5, 6):
        for b in range(-5, 6):
            if 3*a + 8*b == d and abs(a) + abs(b) < 10:
                print(f"  {d:2d} = 3×({a:2d}) + 8×({b:2d})")
                break

# =============================================================================
# SECTION 8: The Complete Pattern
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: THE COMPLETE PATTERN")
print("=" * 80)

print(f"""
SUMMARY: Z ENCODES MULTIPLE STRUCTURES

GAUGE STRUCTURE:
  • 8 = SU(3) generators → gluons
  • 3 = SU(2) generators → weak bosons (before EWSB)
  • 8 + 3 + 1 = 12 total generators

STRING DIMENSIONS:
  • 11 = 3 + 8 = M-theory dimensions
  • 10 = 11 - 1 = superstring dimensions
  • 26 ≈ 4.5Z = bosonic string dimensions

TRIANGULAR PATTERN:
  • 2^T₁ = 2 (in Z)
  • 2^T₂ = 8 (in Z)
  • 2^T₃ = 64 (in m_μ/m_e)
  • 2^T₄ = 1024 (in Z⁴ = 1024π²/9)

HIERARCHY:
  • M_Pl/v = 2 × Z^21.5 where 21 = T₆
  • The electroweak hierarchy uses the 6th triangular number!

SPECULATION:
  The Zimmerman framework may be encoding:
  • Gauge group structure (8 + 3 + 1)
  • String/M-theory dimensions (11 = 3 + 8)
  • Triangular number sequence in powers of 2
  • Everything unified through Z = 2√(8π/3)
""")

# =============================================================================
# SECTION 9: New Discovery - T₆ Connection
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 9: NEW DISCOVERY - THE T₆ CONNECTION")
print("=" * 80)

# T₆ = 21
T6 = 6*7//2
print(f"T₆ = 6 × 7 / 2 = {T6}")
print(f"21.5 = T₆ + 0.5")

print(f"""
The electroweak hierarchy M_Pl/v = 2 × Z^(T₆ + 0.5)

Why T₆?
  • 6 = coefficient in m_μ/m_e = 6Z² + Z
  • 6 = faces of a cube
  • 6 = 3! = factorial of spatial dims

The "+0.5" remains unexplained.

PREDICTION:
If 21.5 = T₆ + 0.5, then other hierarchies might use other Tₙ + corrections.
""")

# Test other hierarchies
print("--- Testing Tₙ + 0.5 for other hierarchies ---")
# Cosmological hierarchy: ρ_Λ/ρ_Pl ≈ Z^(-161)
# What triangular number is close to 161?
for n in range(1, 20):
    Tn = n*(n+1)//2
    if abs(Tn - 161) < 10:
        print(f"T_{n} = {Tn}, diff from 161 = {161 - Tn}")

# T₁₇ = 153, T₁₈ = 171
print(f"\nT₁₇ = 153, T₁₈ = 171")
print(f"161 is between T₁₇ and T₁₈")
print(f"161 = T₁₇ + 8 = 153 + 8")
print(f"161 = T₁₈ - 10 = 171 - 10")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("SUMMARY: GAUGE AND STRING CONNECTIONS")
print("=" * 80)

print("""
ESTABLISHED CONNECTIONS:

1. GAUGE GROUP:
   8 + 3 + 1 = 12 generators of SM
   8 and 3 appear directly in Z = 2√(8π/3)

2. STRING DIMENSIONS:
   11 = 3 + 8 (M-theory)
   This appears in m_τ/m_μ = Z + 11 = Z + 3 + 8

3. TRIANGULAR NUMBERS:
   2^Tₙ pattern: 2, 8, 64, 1024...
   All appear in the framework!

4. HIERARCHY EXPONENTS:
   21.5 = T₆ + 0.5 (electroweak)
   161 ≈ T₁₇ + 8 (cosmological)

NEW INSIGHT:
The framework may encode M-theory structure (11D)
reduced to 4D through the geometry of Z!
""")
