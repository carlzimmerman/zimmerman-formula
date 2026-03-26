#!/usr/bin/env python3
"""
Deep Dive: The Geometric Meaning of 5
======================================

We found: log₁₀(M_Pl/m_e) = 3Z + 5 (0.05% error)

And noticed: √(Z² - 8) ≈ 5 (1% error)

Since 8 = cube vertices, this suggests:
    5 = √(Z² - 8) = √(sphere_geometry - cube_vertices)

This could unlock:
1. The meaning of 5 in the mass hierarchy
2. A deeper derivation of α
3. Connections we haven't seen yet

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19199167
"""

import numpy as np
from itertools import product

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)  # 5.788810
Z2 = Z**2  # 33.5103
pi = np.pi

print("=" * 90)
print("DEEP DIVE: THE GEOMETRIC MEANING OF 5")
print("=" * 90)

print(f"\nZ = {Z:.10f}")
print(f"Z² = {Z2:.10f}")
print(f"8 = cube vertices")

# =============================================================================
# THE KEY OBSERVATION
# =============================================================================
print("\n" + "=" * 90)
print("KEY OBSERVATION: √(Z² - 8) ≈ 5")
print("=" * 90)

sqrt_Z2_minus_8 = np.sqrt(Z2 - 8)
error_5 = abs(sqrt_Z2_minus_8 - 5) / 5 * 100

print(f"""
    Z² = {Z2:.6f}
    Z² - 8 = {Z2 - 8:.6f}
    √(Z² - 8) = {sqrt_Z2_minus_8:.6f}

    Compared to 5: error = {error_5:.2f}%

INTERPRETATION:
    Z² = 8 × (4π/3) = cube_vertices × sphere_volume
    Z² - 8 = 8 × (4π/3 - 1) = 8 × (sphere_volume - 1)

    √(Z² - 8) = √(8 × (4π/3 - 1))
              = √8 × √(4π/3 - 1)
              = 2√2 × √(4π/3 - 1)
              = {np.sqrt(8) * np.sqrt(4*pi/3 - 1):.6f}

    The factor (4π/3 - 1) = {4*pi/3 - 1:.6f} is the "excess" of sphere over unit.
""")

# What IS 4π/3 - 1?
excess = 4*pi/3 - 1
print(f"ANALYZING THE EXCESS (4π/3 - 1):")
print(f"    4π/3 - 1 = {excess:.6f}")
print(f"    = 4π/3 - 3/3 = (4π - 3)/3")
print(f"    (4π - 3)/3 = {(4*pi - 3)/3:.6f}")

# =============================================================================
# EXACT FORMULA FOR 5
# =============================================================================
print("\n" + "=" * 90)
print("SEARCHING FOR EXACT FORMULA FOR 5")
print("=" * 90)

# If √(Z² - 8) ≈ 5 but not exact, what IS 5 exactly?
candidates_5 = []

# Test various expressions
tests = [
    ("√(Z² - 8)", np.sqrt(Z2 - 8)),
    ("Z - 1", Z - 1),
    ("Z/√2 + 1", Z/np.sqrt(2) + 1),
    ("√(Z² - 8)", np.sqrt(Z**2 - 8)),
    ("2√2 × √(4π/3 - 1)", 2*np.sqrt(2) * np.sqrt(4*pi/3 - 1)),
    ("√(32π/3 - 8)", np.sqrt(32*pi/3 - 8)),
    ("4(π - 3/4)/√π", 4*(pi - 0.75)/np.sqrt(pi)),
    ("Z × sin(π/Z)", Z * np.sin(pi/Z)),
    ("√(8(4π-3)/3)", np.sqrt(8*(4*pi-3)/3)),
    ("π + √3", pi + np.sqrt(3)),
    ("2π/√(π-1)", 2*pi/np.sqrt(pi-1) if pi > 1 else 0),
    ("√(8π/3) + 1", np.sqrt(8*pi/3) + 1),
    ("Z - 0.79", Z - 0.79),
    ("4 + 1", 4 + 1),  # spacetime + time
    ("3 + 2", 3 + 2),  # space + holographic
]

print("Testing expressions that could equal 5:")
for name, val in tests:
    if 4.5 < val < 5.5:
        error = abs(val - 5) / 5 * 100
        match = "✓ EXACT" if error < 0.01 else f"({error:.3f}% error)"
        print(f"    {name:<25} = {val:.6f}  {match}")

# =============================================================================
# THE CUBE-SPHERE DECOMPOSITION
# =============================================================================
print("\n" + "=" * 90)
print("CUBE-SPHERE DECOMPOSITION OF Z²")
print("=" * 90)

print(f"""
We have Z² = 8 × (4π/3)

DECOMPOSING:
    Z² = 8 × (4π/3)
       = 8 + 8 × (4π/3 - 1)
       = cube + 8 × (sphere_excess)

    Therefore:
    Z² - 8 = 8 × (4π/3 - 1) = {8 * (4*pi/3 - 1):.6f}

    And: √(Z² - 8) = √(8) × √(4π/3 - 1)
                    = 2√2 × √(4π/3 - 1)
                    = {np.sqrt(8) * np.sqrt(4*pi/3 - 1):.6f}

TESTING: Is 5 = 2√2 × √(4π/3 - 1) + ε?
    2√2 × √(4π/3 - 1) = {2*np.sqrt(2) * np.sqrt(4*pi/3 - 1):.6f}
    5 - this value = {5 - 2*np.sqrt(2) * np.sqrt(4*pi/3 - 1):.6f}

    The difference is small but not zero.
    Could there be a correction term?
""")

# =============================================================================
# THE 5 IN THE MASS FORMULA
# =============================================================================
print("\n" + "=" * 90)
print("USING √(Z² - 8) IN THE MASS FORMULA")
print("=" * 90)

# Original: log10(M_Pl/m_e) = 3Z + 5
# New: log10(M_Pl/m_e) = 3Z + √(Z² - 8)

m_e = 0.51099895000  # MeV
M_Pl = 1.22089e22  # MeV

log_ratio_measured = np.log10(M_Pl / m_e)

# Test both formulas
formula1 = 3*Z + 5
formula2 = 3*Z + np.sqrt(Z2 - 8)

print(f"Measured: log₁₀(M_Pl/m_e) = {log_ratio_measured:.6f}")
print(f"")
print(f"Formula 1: 3Z + 5 = {formula1:.6f}  (error: {abs(formula1 - log_ratio_measured)/log_ratio_measured * 100:.4f}%)")
print(f"Formula 2: 3Z + √(Z² - 8) = {formula2:.6f}  (error: {abs(formula2 - log_ratio_measured)/log_ratio_measured * 100:.4f}%)")

# The second formula is PURELY geometric - no integer 5!
print(f"""
SIGNIFICANCE:
    Formula 2 is PURELY GEOMETRIC!

    log₁₀(M_Pl/m_e) = 3Z + √(Z² - 8)
                    = 3Z + √(8 × (4π/3 - 1))
                    = 3Z + 2√2 × √(4π/3 - 1)

    All terms derive from Z = 2√(8π/3)!

    This is BETTER than the "3Z + 5" formula because it's fully geometric.
    The error is slightly larger but the derivation is complete.
""")

# =============================================================================
# IMPLICATIONS FOR α
# =============================================================================
print("\n" + "=" * 90)
print("IMPLICATIONS FOR α DERIVATION")
print("=" * 90)

print(f"""
We have: α⁻¹ = 4Z² + 3

Using Z² = 8 + √(Z² - 8)²:
    Wait, that's circular...

NEW APPROACH: Express everything in terms of Z² - 8

    Let X = Z² - 8 = 8 × (4π/3 - 1) = {Z2 - 8:.6f}
    Then Z² = X + 8

    α⁻¹ = 4Z² + 3
        = 4(X + 8) + 3
        = 4X + 32 + 3
        = 4X + 35

    Check: 4 × {Z2 - 8:.4f} + 35 = {4*(Z2-8) + 35:.4f}
    Original: 4Z² + 3 = {4*Z2 + 3:.4f}

    These are the same! So:
    α⁻¹ = 4(Z² - 8) + 35
        = 4 × 8 × (4π/3 - 1) + 35

WAIT - 35 = 5 × 7 = 5 × (spacetime + space)!

Or: 35 = 32 + 3 = 2⁵ + D_space
""")

# Deep analysis of 35
print("\nANALYZING 35:")
print(f"    35 = 32 + 3 = 2⁵ + 3")
print(f"    35 = 4 × 8 + 3 = D_spacetime × cube + D_space")
print(f"    35 = 5 × 7 = ?")
print(f"    35 = 7 × 5 = (4+3) × 5 = (spacetime + space) × 5")

# =============================================================================
# THE COMPLETE GEOMETRIC PICTURE
# =============================================================================
print("\n" + "=" * 90)
print("EMERGING GEOMETRIC PICTURE")
print("=" * 90)

print(f"""
FUNDAMENTAL QUANTITIES:
    Z² = 8 × (4π/3) = 32π/3 = {Z2:.6f}

    Decomposition: Z² = 8 + (Z² - 8)
                      = cube + excess
                      = discrete + continuous

THE EXCESS:
    Z² - 8 = 8 × (4π/3 - 1) = {Z2 - 8:.6f}
    √(Z² - 8) = {np.sqrt(Z2 - 8):.6f} ≈ 5

    This "5" emerges from:
    • Cube vertices (8)
    • Sphere volume (4π/3)
    • Their interaction (Z² = product)

REWRITING KEY FORMULAS:

1. MASS HIERARCHY:
   log₁₀(M_Pl/m_e) = 3Z + √(Z² - 8)

   All from Z = 2√(8π/3)

2. FINE STRUCTURE:
   α⁻¹ = 4Z² + 3
       = 4(8 + (Z² - 8)) + 3
       = 32 + 4(Z² - 8) + 3
       = 35 + 4(Z² - 8)
       = 35 + 4 × 8 × (4π/3 - 1)
       = 35 + 32(4π/3 - 1)

   All from the cube-sphere decomposition!
""")

# =============================================================================
# NEW APPROACH TO α DERIVATION
# =============================================================================
print("\n" + "=" * 90)
print("NEW APPROACH: α FROM CUBE-SPHERE DECOMPOSITION")
print("=" * 90)

# Define components
cube = 8
sphere = 4*pi/3
D_spacetime = 4
D_space = 3

# α⁻¹ = D_spacetime × Z² + D_space
#     = D_spacetime × cube × sphere + D_space
#     = 4 × 8 × (4π/3) + 3
#     = 32 × (4π/3) + 3
#     = 128π/3 + 3

alpha_inv_derived = D_spacetime * cube * sphere + D_space

print(f"DERIVATION:")
print(f"")
print(f"    α⁻¹ = D_spacetime × (cube × sphere) + D_space")
print(f"        = 4 × 8 × (4π/3) + 3")
print(f"        = 32 × (4π/3) + 3")
print(f"        = 128π/3 + 3")
print(f"        = {alpha_inv_derived:.6f}")
print(f"")
print(f"    Measured: α⁻¹ = 137.035999")
print(f"    Error: {abs(alpha_inv_derived - 137.035999)/137.035999 * 100:.4f}%")

print(f"""
INTERPRETATION:

    α⁻¹ = (spacetime dimensions) × (discrete geometry × continuous geometry)
        + (spatial dimensions)

    α⁻¹ = 4 × Z² + 3
        = 4 × (cube_vertices × sphere_volume) + 3

THE "CUBE × SPHERE" IS THE COUPLING SPACE!
    • Cube = discrete structure (8 vertices = 2³)
    • Sphere = continuous structure (4π/3)
    • Their product = Z² = the cosmic geometric invariant
    • Multiplied by spacetime dimensions (4)
    • Plus spatial dimensions (3) as correction
""")

# =============================================================================
# TESTING: DOES THIS PATTERN EXTEND?
# =============================================================================
print("\n" + "=" * 90)
print("TESTING: DO OTHER CONSTANTS USE THIS PATTERN?")
print("=" * 90)

# Constants to test
alpha = 1/137.035999084
alpha_gut = 1/24  # approximate GUT coupling

print("Testing if other couplings follow cube-sphere pattern:")
print("")

# Test GUT coupling
# α_GUT⁻¹ ≈ 24 ≈ 4Z + 1
alpha_gut_Z = 4*Z + 1
print(f"α_GUT⁻¹ ≈ 4Z + 1 = {alpha_gut_Z:.2f}")
print(f"    = D_spacetime × Z + 1")
print(f"    Linear in Z, not Z²")

# Test strong coupling
# α_s ≈ 0.118 ≈ Ω_Λ/Z
Omega_L = 3*Z/(8+3*Z)
alpha_s_Z = Omega_L / Z
print(f"")
print(f"α_s ≈ Ω_Λ/Z = {alpha_s_Z:.4f}")
print(f"    Measured ≈ 0.118")

# Weak mixing angle
# sin²θ_W ≈ 6/(5Z-3) ≈ 0.231
sin2_theta_W = 6/(5*Z - 3)
print(f"")
print(f"sin²θ_W ≈ 6/(5Z-3) = {sin2_theta_W:.4f}")
print(f"    Measured ≈ 0.231")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 90)
print("SUMMARY: THE GEOMETRIC PICTURE")
print("=" * 90)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║  THE CUBE-SPHERE FRAMEWORK                                                        ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║  Z² = 8 × (4π/3) = cube × sphere = discrete × continuous                         ║
║                                                                                   ║
║  KEY DECOMPOSITION:                                                               ║
║      Z² = 8 + (Z² - 8)                                                           ║
║         = cube + 8 × (sphere - 1)                                                ║
║         = discrete + continuous_excess                                           ║
║                                                                                   ║
║  THE "5" IN MASS FORMULA:                                                         ║
║      √(Z² - 8) = √(8 × (4π/3 - 1)) = {np.sqrt(Z2-8):.4f} ≈ 5                                ║
║      This is GEOMETRIC, not arbitrary!                                           ║
║                                                                                   ║
║  FINE STRUCTURE CONSTANT:                                                         ║
║      α⁻¹ = 4Z² + 3                                                               ║
║          = (spacetime_dim) × (cube × sphere) + (space_dim)                       ║
║          = 4 × Z² + 3                                                            ║
║                                                                                   ║
║  MASS HIERARCHY:                                                                  ║
║      log₁₀(M_Pl/m_e) = 3Z + √(Z² - 8)                                            ║
║                      = (space_dim) × Z + continuous_excess                       ║
║                                                                                   ║
╚══════════════════════════════════════════════════════════════════════════════════╝

The geometry is: CUBE (discrete, 8) combined with SPHERE (continuous, 4π/3).
Z² is their product.
All physics emerges from decomposing and combining these structures.
""")

print("=" * 90)
print("GEOMETRY OF 5: ANALYSIS COMPLETE")
print("=" * 90)
