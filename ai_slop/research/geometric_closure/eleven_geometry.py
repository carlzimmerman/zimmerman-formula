#!/usr/bin/env python3
"""
The Geometric Origin of 11 in m_τ/m_μ = Z + 11
==============================================

Exploring why 11 appears in the tau/muon mass ratio.

Candidates:
1. M-theory dimensions (10+1 = 11)
2. φ⁵ ≈ 11.09 (golden ratio)
3. 3 + 8 = spatial dims + cube vertices
4. 4 + 7 = spacetime dims + G2 dimensions
5. Some function of Z or other constants

Carl Zimmerman, March 2026
"""

import numpy as np

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)
phi = (1 + np.sqrt(5)) / 2
alpha = 1/137.035999084

# Measured mass ratios
m_tau_m_mu_measured = 16.8167
m_mu_m_e_measured = 206.768

print("=" * 70)
print("THE GEOMETRIC ORIGIN OF 11")
print("=" * 70)

# =============================================================================
# What exactly is the "11"?
# =============================================================================
print("\n--- What is the exact value needed? ---")

exact_11 = m_tau_m_mu_measured - Z
print(f"m_τ/m_μ = {m_tau_m_mu_measured}")
print(f"Z = {Z:.6f}")
print(f"m_τ/m_μ - Z = {exact_11:.6f}")
print(f"Difference from 11 = {exact_11 - 11:.6f}")

# =============================================================================
# Candidate expressions for 11
# =============================================================================
print("\n--- Candidate expressions for '11' ---")

candidates = [
    ("11 (integer)", 11),
    ("φ⁵", phi**5),
    ("3 + 8 (spatial + cube)", 3 + 8),
    ("4 + 7 (spacetime + G2)", 4 + 7),
    ("2π + 4.72", 2*np.pi + 4.72),
    ("e² + 3.61", np.e**2 + 3.61),
    ("10 + 1 (string + M)", 10 + 1),
    ("Z + 5.21", Z + 5.21),
    ("2Z - 0.58", 2*Z - 0.58),
    ("12 - 1", 12 - 1),
    ("√121", np.sqrt(121)),
    ("π² + 1.13", np.pi**2 + 1.13),
    ("7 + 4", 7 + 4),
    ("6 + 5", 6 + 5),
    ("5 + 6", 5 + 6),
    ("(3² + 2)/1", (3**2 + 2)/1),
    ("Fibonacci F₅ + F₄", 5 + 3),  # This is 8, not 11
    ("Fibonacci F₆ + F₄", 8 + 3),  # This IS 11!
    ("2³ + 3", 8 + 3),
    ("2⁴ - 5", 16 - 5),
    ("3! + 5", 6 + 5),
]

print(f"\n{'Expression':<30} {'Value':>12} {'Error from exact':>15} {'Error %':>10}")
print("-" * 70)

for name, value in candidates:
    error = value - exact_11
    error_pct = abs(error) / exact_11 * 100
    print(f"{name:<30} {value:>12.6f} {error:>+15.6f} {error_pct:>10.4f}%")

# =============================================================================
# The Fibonacci connection
# =============================================================================
print("\n" + "=" * 70)
print("THE FIBONACCI CONNECTION")
print("=" * 70)

print("\nFibonacci numbers: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...")
print("\n11 = F₆ + F₄ = 8 + 3")
print("11 = F₇ - F₃ = 13 - 2")

fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
print("\nFibonacci sums and differences near 11:")
for i in range(len(fib)):
    for j in range(len(fib)):
        if abs(fib[i] + fib[j] - 11) < 0.01:
            print(f"  F_{i+1} + F_{j+1} = {fib[i]} + {fib[j]} = {fib[i]+fib[j]}")
        if abs(fib[i] - fib[j] - 11) < 0.01:
            print(f"  F_{i+1} - F_{j+1} = {fib[i]} - {fib[j]} = {fib[i]-fib[j]}")

# =============================================================================
# The 3 + 8 interpretation
# =============================================================================
print("\n" + "=" * 70)
print("THE 3 + 8 INTERPRETATION")
print("=" * 70)

print("""
11 = 3 + 8

Where:
  3 = spatial dimensions (also in Friedmann 8πG/3)
  8 = cube vertices (also in Einstein 8πG)

Both 3 and 8 appear in Z = 2√(8π/3)!

So: m_τ/m_μ = Z + 3 + 8
            = 2√(8π/3) + 3 + 8

This connects the tau/muon ratio to the SAME geometric elements
that appear in the Zimmerman constant!
""")

# Verification
print("Verification:")
print(f"  Z + 3 + 8 = {Z + 3 + 8:.6f}")
print(f"  m_τ/m_μ  = {m_tau_m_mu_measured:.6f}")
print(f"  Error = {abs(Z + 11 - m_tau_m_mu_measured)/m_tau_m_mu_measured * 100:.4f}%")

# =============================================================================
# The M-theory interpretation
# =============================================================================
print("\n" + "=" * 70)
print("THE M-THEORY INTERPRETATION")
print("=" * 70)

print("""
11 = 10 + 1 (spacetime dimensions in M-theory)

M-theory unifies the 5 superstring theories in 11 dimensions:
  - 10 spatial dimensions
  - 1 time dimension

Or alternatively:
  - The 5 string theories each have 10 dimensions
  - M-theory adds 1 more dimension

The appearance of 11 in a mass ratio could suggest a deep
connection between particle masses and the geometry of
compactified extra dimensions.
""")

# =============================================================================
# The 4 + 7 interpretation (Spacetime + G2)
# =============================================================================
print("\n" + "=" * 70)
print("THE 4 + 7 INTERPRETATION")
print("=" * 70)

print("""
11 = 4 + 7

Where:
  4 = spacetime dimensions (in GR)
  7 = dimension of G2 (exceptional Lie group)

G2 is the automorphism group of the octonions!
It has dimension 14 = 2 × 7

M-theory on a G2 manifold gives 4D N=1 supergravity.
The 7-dimensional G2 manifold "compactifies" 7 of the 11 dimensions.

So: 11 = 4 (observable) + 7 (compactified)
""")

# =============================================================================
# Testing all interpretations
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: BEST INTERPRETATIONS OF 11")
print("=" * 70)

best = [
    ("11 = 3 + 8 (spatial + cube)", 3 + 8, "Both appear in Z = 2√(8π/3)"),
    ("11 = 10 + 1 (M-theory dims)", 10 + 1, "Suggests extra dimensions"),
    ("11 = 4 + 7 (spacetime + G2)", 4 + 7, "M-theory compactification"),
    ("11 = F₆ + F₄ (Fibonacci)", 8 + 3, "Fibonacci structure"),
    ("11 = φ⁵ ≈ 11.09", phi**5, "Golden ratio connection"),
]

print(f"\n{'Interpretation':<35} {'Value':>10} {'Error %':>10} {'Note':<30}")
print("-" * 90)

for name, value, note in best:
    error_pct = abs(value - exact_11) / exact_11 * 100
    print(f"{name:<35} {value:>10.4f} {error_pct:>10.4f}% {note:<30}")

# =============================================================================
# The complete lepton mass pattern
# =============================================================================
print("\n" + "=" * 70)
print("THE COMPLETE LEPTON MASS PATTERN")
print("=" * 70)

print(f"""
m_μ/m_e = 6Z² + Z = 64π + Z
        = {6*Z**2 + Z:.4f} (predicted)
        = {m_mu_m_e_measured:.4f} (measured)
        = Error: {abs(6*Z**2 + Z - m_mu_m_e_measured)/m_mu_m_e_measured * 100:.4f}%

m_τ/m_μ = Z + 11 = Z + 3 + 8
        = {Z + 11:.4f} (predicted)
        = {m_tau_m_mu_measured:.4f} (measured)
        = Error: {abs(Z + 11 - m_tau_m_mu_measured)/m_tau_m_mu_measured * 100:.4f}%

m_τ/m_e = (Z + 11)(6Z² + Z)
        = {(Z + 11) * (6*Z**2 + Z):.2f} (predicted)
        = {m_tau_m_mu_measured * m_mu_m_e_measured:.2f} (measured)

Pattern:
  - m_μ/m_e involves Z² (second power)
  - m_τ/m_μ involves Z¹ (first power)
  - Coefficients: 6, 1, 11 = 6, 1, (3+8)
""")

# Connection between the two ratios
print("\n--- Connection between ratios ---")
print(f"m_μ/m_e = 6Z² + Z = Z(6Z + 1)")
print(f"m_τ/m_μ = Z + 11")
print(f"\nRatio of ratios:")
print(f"(m_μ/m_e)/(m_τ/m_μ) = Z(6Z + 1)/(Z + 11)")
print(f"                    = {(6*Z**2 + Z)/(Z + 11):.6f}")
print(f"                    ≈ {m_mu_m_e_measured/m_tau_m_mu_measured:.6f} (measured)")
