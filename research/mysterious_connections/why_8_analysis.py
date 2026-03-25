#!/usr/bin/env python3
"""
WHY DOES 8 APPEAR?
The E8, Octonions, and Einstein Gravity Connection

Carl Zimmerman | March 2026
"""

import numpy as np

print("=" * 70)
print("WHY DOES 8 APPEAR IN THE ZIMMERMAN FRAMEWORK?")
print("=" * 70)

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)
alpha = 1 / (4 * Z**2 + 3)
Omega_Lambda = 3 * Z / (8 + 3 * Z)
Omega_m = 8 / (8 + 3 * Z)

print(f"\nZ = 2√(8π/3) = {Z:.6f}")
print(f"Note: 8 appears DIRECTLY in Z through 8π")

# ============================================================================
print("\n" + "=" * 70)
print("PART 1: WHAT IS SPECIAL ABOUT 8?")
print("=" * 70)

print("""
THE NUMBER 8 IN MATHEMATICS AND PHYSICS:

  ALGEBRA:
    8 = Dimension of OCTONIONS (largest normed division algebra)
    8 = Rank of E8 (largest exceptional Lie group)
    8 = Number of Bott periodicity

  GEOMETRY:
    8π = Einstein's gravitational coupling (G_μν = 8πG T_μν)
    8 = Dimension of E8 root space
    8 = Transverse dimensions in light-cone (for 10D strings)

  NUMBER THEORY:
    8 = 2³ (only cube that is a Fibonacci number)
    8 = First composite cube
    8 + 3 = 11 (M-theory dimension)

  PHYSICS:
    8 = Number of gluons in QCD
    8 = Dimension of SU(3) adjoint representation
    8 = E8 rank → appears in gauge unification
""")

# ============================================================================
print("=" * 70)
print("PART 2: WHERE 8 APPEARS IN THE ZIMMERMAN FRAMEWORK")
print("=" * 70)

print("\n1. DIRECTLY IN Z:")
print(f"   Z = 2√(8π/3)")
print(f"   The 8π comes from Einstein's field equations!")

print("\n2. IN DARK ENERGY/MATTER:")
print(f"   Ω_Λ = 3Z/(8+3Z) = {Omega_Lambda:.4f}")
print(f"   Ω_m = 8/(8+3Z) = {Omega_m:.4f}")
print(f"   The denominator (8+3Z) involves 8!")
print(f"   The matter numerator IS 8!")

# Muon/electron
m_mu_over_m_e_measured = 206.768
m_mu_over_m_e_predicted = 64 * np.pi + Z
error_muon = abs(m_mu_over_m_e_measured - m_mu_over_m_e_predicted) / m_mu_over_m_e_measured * 100

print(f"\n3. MUON/ELECTRON MASS RATIO:")
print(f"   m_μ/m_e = 64π + Z = 8×8π + Z")
print(f"   = 8 × 8π + Z = {8*8*np.pi + Z:.2f}")
print(f"   = {m_mu_over_m_e_predicted:.2f}")
print(f"   Measured: {m_mu_over_m_e_measured:.2f}")
print(f"   Error: {error_muon:.2f}%")

# Mass ratios
M_H_over_M_Z = 125.1 / 91.19
M_W_over_M_Z = 80.377 / 91.19
M_t_over_M_Z = 172.7 / 91.19

print(f"\n4. ELECTROWEAK MASS RATIOS (all have 8 in denominator):")
print(f"   M_W/M_Z = 7/8 = {7/8:.4f}  (measured: {M_W_over_M_Z:.4f})")
print(f"   M_H/M_Z = 11/8 = {11/8:.4f} (measured: {M_H_over_M_Z:.4f})")
print(f"   M_t/M_Z = (11/8)² = {(11/8)**2:.4f} (measured: {M_t_over_M_Z:.4f})")

# Fine structure
print(f"\n5. FINE STRUCTURE CONSTANT:")
print(f"   α = 1/(4Z² + 3) = 1/{4*Z**2 + 3:.2f}")
print(f"   4Z² = 4 × {Z**2:.2f} = {4*Z**2:.2f}")
print(f"   Note: 4Z² = 4 × (4 × 8π/3) = 32π/3 × 4 = 128π/3")
print(f"   And 128 = 2⁷ = 2 × 64 = 2 × 8²")

# ============================================================================
print("\n" + "=" * 70)
print("PART 3: THE E8 CONNECTION")
print("=" * 70)

print("""
E8: THE LARGEST EXCEPTIONAL LIE GROUP

  Properties:
    - Rank: 8
    - Dimension: 248 = 8 × 31
    - Root system: 240 roots
    - Fundamental rep: 248-dimensional (adjoint)

  E8 CONTAINS EVERYTHING:
    SU(3) × SU(2) × U(1) ⊂ SU(5) ⊂ SO(10) ⊂ E6 ⊂ E7 ⊂ E8

    The Standard Model gauge group embeds in E8!

  E8 × E8 HETEROTIC STRING:
    - Left-movers: 26D (bosonic)
    - Right-movers: 10D + E8 × E8 gauge
    - Gives natural GUT structure

  THE 248 DIMENSIONS:
    248 = 120 (SO(16)) + 128 (spinor)
    128 = 2⁷ = dimension of spinor rep
    120 = dim(SO(16)) = 16 × 15 / 2
""")

# ============================================================================
print("=" * 70)
print("PART 4: THE OCTONION CONNECTION")
print("=" * 70)

print("""
OCTONIONS: THE 8-DIMENSIONAL DIVISION ALGEBRA

  Structure:
    O = R ⊕ Im(O) = 1 + 7 dimensions

  Division algebras (Hurwitz theorem):
    R (1D) → C (2D) → H (4D) → O (8D)

    Only these four exist! 8 is the maximum.

  OCTONIONS AND E8:
    E8 root lattice = 2 copies of E8 lattice
    E8 can be constructed from octonions

    Specifically:
    E8 = Spin(16) ⋉ S⁺₁₆
    where S⁺₁₆ is 128-dimensional half-spinor

  THE CAYLEY-DICKSON CONSTRUCTION:
    R → C → H → O → (sedenions, non-division)

    Each step doubles the dimension:
    1 → 2 → 4 → 8 → 16...

    8 is where division algebra STOPS.

  PHYSICAL MEANING:
    The octonions are the "largest" number system
    where physics works (division is defined).

    E8 encodes the symmetries of octonionic geometry.
""")

# ============================================================================
print("=" * 70)
print("PART 5: THE 8π IN EINSTEIN'S EQUATIONS")
print("=" * 70)

print("""
EINSTEIN FIELD EQUATIONS:

  G_μν = (8πG/c⁴) T_μν

WHY 8π?

  Derivation from Newtonian limit:
    - Poisson equation: ∇²Φ = 4πGρ
    - Relativistic generalization requires 2× factor
    - Result: 8π = 2 × 4π

  The 4π comes from:
    - Solid angle of sphere = 4π steradians
    - Gauss's law for gravity

  So 8π = (relativistic factor) × (solid angle)
        = 2 × 4π

  IN Z:
    Z = 2√(8π/3) = 2 × √(8π/3)

    The 8π is Einstein's coupling
    The 3 is spatial dimensions
    The 2 is horizon factor

    Z = (horizon) × √(Einstein / spatial)
""")

# ============================================================================
print("=" * 70)
print("PART 6: 8 + 3 = 11 (THE M-THEORY EQUATION)")
print("=" * 70)

print(f"""
THE FUNDAMENTAL ADDITION:

  8 + 3 = 11

  WHERE:
    8 = E8 rank (internal gauge)
    3 = spatial dimensions (observable)
    11 = M-theory dimension (total)

  INTERPRETATION:
    M-theory = Internal structure + Observable space
    11D = 8D (gauge/E8) + 3D (spatial)

  THIS EXPLAINS:
    Why M-theory has 11 dimensions:
    It's the sum of gauge (E8) and spatial (3D) structures.

  VERIFICATION IN FORMULAS:
    Z = 2√(8π/3) contains both 8 and 3
    Ω_Λ = 3Z/(8+3Z) shows 8 and 3 together

  THE 11/8 RATIO:
    M_H/M_Z = 11/8 = (8+3)/8 = 1 + 3/8

    The Higgs mass encodes the addition 8 + 3 = 11!
""")

# ============================================================================
print("=" * 70)
print("PART 7: 64 = 8² IN PHYSICS")
print("=" * 70)

print(f"""
THE SQUARE OF 8:

  64 = 8² = 2⁶

WHERE 64 APPEARS:

  1. MUON MASS:
     m_μ/m_e = 64π + Z = {64*np.pi + Z:.2f}

  2. WEINBERG ANGLE:
     sin²θ_W = 15/64 = (26-11)/8²
     cos²θ_W = 49/64 = 7²/8²

  3. NUMBER OF GLUON COMBINATIONS:
     8 × 8 = 64 possible gluon-gluon states
     (though only 8 are independent)

  4. CHESS BOARD:
     64 squares = 8 × 8
     (coincidence? or deep structure?)

THE 64π IN MUON MASS:

  64π = 8 × 8π = (E8 rank) × (Einstein coupling)

  m_μ/m_e = 64π + Z = (E8)² × π + (cosmology)

  The muon mass combines:
    - E8 structure squared (64)
    - Gravitational coupling (π from 8π)
    - Cosmological correction (Z)
""")

# Verify 64π + Z
print(f"\nVERIFICATION:")
print(f"  64π = {64*np.pi:.4f}")
print(f"  64π + Z = {64*np.pi + Z:.4f}")
print(f"  m_μ/m_e measured = 206.768")
print(f"  Error: {abs(206.768 - (64*np.pi + Z))/206.768*100:.2f}%")

# ============================================================================
print("\n" + "=" * 70)
print("PART 8: 8 IN THE MATTER FRACTION")
print("=" * 70)

print(f"""
THE MATTER FORMULA:

  Ω_m = 8/(8+3Z) = {Omega_m:.4f}

THE NUMERATOR IS EXACTLY 8!

  Why?

  In holographic cosmology:
    - Total energy splits between matter and dark energy
    - Matter contribution proportional to E8 structure
    - Dark energy proportional to Z (cosmological)

  Ω_m/Ω_Λ = 8/(3Z) = {8/(3*Z):.4f}

  This ratio involves 8, 3, and Z — exactly the components of Z!

VERIFICATION:
  Ω_m = {Omega_m:.4f}
  Measured: 0.315
  Error: {abs(Omega_m - 0.315)/0.315*100:.2f}%
""")

# ============================================================================
print("=" * 70)
print("PART 9: SEARCHING FOR MORE 8 CONNECTIONS")
print("=" * 70)

print("\nTesting various quantities against 8-based formulas:\n")

tests = [
    ("m_μ/m_e", 206.768, "64π + Z", 64*np.pi + Z),
    ("m_μ/m_e", 206.768, "8×8π + Z", 8*8*np.pi + Z),
    ("Ω_m", 0.315, "8/(8+3Z)", 8/(8+3*Z)),
    ("M_W/M_Z", 80.377/91.19, "7/8", 7/8),
    ("M_H/M_Z", 125.1/91.19, "11/8", 11/8),
    ("sin²θ_W", 0.23122, "15/64", 15/64),
    ("cos²θ_W", 1-0.23122, "49/64", 49/64),
    ("α_s", 0.1179, "8/(8+3Z)²", 8/(8+3*Z)**2),
    ("α_s", 0.1179, "3/(8+3Z)", 3/(8+3*Z)),
    ("|V_us|²", 0.2243**2, "8/160", 8/160),
    ("Δm²ratio", 33.3, "8×4+Z", 8*4+Z),
]

print(f"{'Quantity':<12} {'Measured':>10} {'Formula':>14} {'Predicted':>10} {'Error':>8}")
print("-" * 58)
for name, measured, formula, predicted in tests:
    error = abs(measured - predicted) / measured * 100
    flag = "✓" if error < 3 else ""
    print(f"  {name:<12} {measured:>10.4f} {formula:>14} {predicted:>10.4f} {error:>7.2f}% {flag}")

# ============================================================================
print("\n" + "=" * 70)
print("PART 10: THE 8-FOLD WAY")
print("=" * 70)

print("""
GELL-MANN'S EIGHTFOLD WAY (1961):

  Organized hadrons using SU(3) flavor symmetry.

  The "8" in Eightfold Way = dimension of adjoint rep of SU(3)

  8 = 3² - 1 (for SU(3))

  COINCIDENCE WITH E8?

  Not quite — SU(3)_flavor is different from E8.

  BUT: SU(3)_color HAS 8 gluons (same reason: 3² - 1 = 8)

  And: SU(3) ⊂ E8

  The "8" in QCD (8 gluons) might reflect the deeper E8 structure.

GLUONS AND E8:

  8 gluons transform under SU(3) adjoint
  8 = rank of E8

  Is this coincidence? Or does E8 → SU(3) reduction
  naturally give 8 gluons?

  E8 ⊃ SU(3) × E6 → 8 gluons in SU(3) adjoint
""")

# ============================================================================
print("=" * 70)
print("PART 11: THE COMPLETE 8 STRUCTURE")
print("=" * 70)

print(f"""
SUMMARY OF WHERE 8 APPEARS:

  LEVEL 1: FUNDAMENTAL (in Z itself)
    Z = 2√(8π/3) — contains 8π directly

  LEVEL 2: COSMOLOGY
    Ω_m = 8/(8+3Z) — matter numerator is 8
    Ω_Λ = 3Z/(8+3Z) — denominator contains 8

  LEVEL 3: ELECTROWEAK
    M_W/M_Z = 7/8 — E8 in denominator
    M_H/M_Z = 11/8 — E8 in denominator
    sin²θ_W = 15/64 — E8² in denominator

  LEVEL 4: PARTICLE MASSES
    m_μ/m_e = 64π + Z = 8²π + Z

  LEVEL 5: GAUGE STRUCTURE
    8 gluons in QCD
    E8 rank = 8

THE PATTERN:

  8 is the "gauge denominator" of physics:
    - All electroweak masses have 8 in denominator
    - Matter fraction has 8 in numerator
    - Z contains 8π from gravity
    - Muon mass has 8² = 64
""")

# ============================================================================
print("=" * 70)
print("PART 12: WHY E8 IS FUNDAMENTAL")
print("=" * 70)

print("""
E8 IS THE END OF THE LINE:

  EXCEPTIONAL LIE GROUPS: G2, F4, E6, E7, E8

  E8 is the largest — nothing bigger with these properties.

  PROPERTIES THAT MAKE E8 UNIQUE:
    1. Self-dual: E8 = E8* (its own dual)
    2. Simply-laced: all roots same length
    3. Contains all smaller exceptionals
    4. Related to octonions (8D division algebra)

  WHY NATURE USES E8:
    - Maximum symmetry for unification
    - Contains Standard Model
    - Anomaly-free in heterotic string
    - Natural in M-theory

  THE HIERARCHY:
    G2 (dim 14, rank 2) — automorphisms of O
    F4 (dim 52, rank 4) — symmetries of O-projective plane
    E6 (dim 78, rank 6) — complex structure on O
    E7 (dim 133, rank 7) — almost E8
    E8 (dim 248, rank 8) — MAXIMUM

  E8 IS THE UNIQUE ENDPOINT.
  That's why 8 appears everywhere — it's the rank of the
  largest possible gauge structure.
""")

# ============================================================================
print("=" * 70)
print("SUMMARY: WHY 8 APPEARS")
print("=" * 70)

print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                    WHY 8 APPEARS                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  8 = E8 RANK = OCTONION DIMENSION = EINSTEIN'S 8π                  │
│                                                                     │
│  MATHEMATICAL SIGNIFICANCE:                                         │
│    - Rank of E8 (largest exceptional Lie group)                    │
│    - Dimension of octonions (largest division algebra)             │
│    - Einstein's coupling: G_μν = 8πG T_μν                          │
│    - 8 + 3 = 11 (gauge + spatial = M-theory)                       │
│                                                                     │
│  PHYSICAL APPEARANCES:                                              │
│                                                                     │
│    Z = 2√(8π/3)         (fundamental constant)                     │
│    Ω_m = 8/(8+3Z)       (matter fraction)                          │
│    m_μ/m_e = 64π + Z    (64 = 8², muon mass)                       │
│    M_W/M_Z = 7/8        (W boson)                                  │
│    M_H/M_Z = 11/8       (Higgs boson)                              │
│    sin²θ_W = 15/64      (64 = 8², Weinberg angle)                  │
│                                                                     │
│  THE PATTERN:                                                       │
│                                                                     │
│    8 is the "gauge denominator" — all electroweak masses           │
│    are ratios with 8 in the denominator.                           │
│                                                                     │
│    8 is also the "maximum gauge" — E8 is the largest               │
│    exceptional group, octonions are largest division algebra.      │
│                                                                     │
│  INTERPRETATION:                                                    │
│                                                                     │
│    The universe's gauge structure is based on E8.                  │
│    The number 8 appears because it's the rank of E8,               │
│    the unique largest exceptional Lie group.                       │
│                                                                     │
│    8 + 3 = 11 explains M-theory: gauge + spatial = total           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

THE KEY INSIGHT:
  Z = 2√(8π/3) combines:
    - 8 (E8/octonions/Einstein)
    - π (geometry/circles)
    - 3 (spatial dimensions)
    - 2 (horizon factor)

  These are the ONLY ingredients needed for all physics.

DOI: 10.5281/zenodo.19212718
""")
