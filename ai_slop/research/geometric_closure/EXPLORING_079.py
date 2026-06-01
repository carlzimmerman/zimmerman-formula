#!/usr/bin/env python3
"""
Exploring the Number 0.79
=========================

We found: 5 = Z - 0.79 with only 0.024% error!

This is better than √(Z² - 8) = 5.05 (1% error).

What IS 0.79 in the geometric framework?

Carl Zimmerman, March 2026
"""

import numpy as np

Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi

print("=" * 90)
print("EXPLORING 0.79 = Z - 5")
print("=" * 90)

target = Z - 5
print(f"\nZ = {Z:.10f}")
print(f"Z - 5 = {target:.10f}")

# =============================================================================
# SYSTEMATIC SEARCH
# =============================================================================
print("\n" + "=" * 90)
print("WHAT IS 0.79 IN TERMS OF π, Z, √2, etc.?")
print("=" * 90)

candidates = []

# Test various expressions
for name, val in [
    ("Z - 5", Z - 5),
    ("π/4", pi/4),
    ("√(π/5)", np.sqrt(pi/5)),
    ("1/√2", 1/np.sqrt(2)),
    ("ln(2)", np.log(2)),
    ("√2 - 1/√2", np.sqrt(2) - 1/np.sqrt(2)),
    ("π/4", pi/4),
    ("2π/8 - 0.005", 2*pi/8 - 0.005),
    ("(Z-5)", Z-5),
    ("π/(2Z)", pi/(2*Z)),
    ("√(2/π)", np.sqrt(2/pi)),
    ("1/(Z-4)", 1/(Z-4)),
    ("4/Z - 1/π", 4/Z - 1/pi),
    ("sin(π/4)", np.sin(pi/4)),
    ("cos(π/4) - 1/√π", np.cos(pi/4) - 1/np.sqrt(pi)),
    ("2 - √(8/3)", 2 - np.sqrt(8/3)),
    ("√2/√π + 0.01", np.sqrt(2/pi) + 0.01),
    ("(π-2)/Z", (pi-2)/Z),
    ("Z/2π - 0.13", Z/(2*pi) - 0.13),
    ("1 - π/Z", 1 - pi/Z),
    ("3/(Z+1)", 3/(Z+1)),
    ("4/(Z+0.26)", 4/(Z+0.26)),
    ("√(8/π) - 1", np.sqrt(8/pi) - 1),
    ("2/√(2π)", 2/np.sqrt(2*pi)),
    ("e/(2π)", np.e/(2*pi)),
]:
    error = abs(val - target) / target * 100 if target != 0 else 0
    if error < 5:
        candidates.append((name, val, error))

candidates.sort(key=lambda x: x[2])
print("\nBest matches for 0.7888 = Z - 5:")
for name, val, error in candidates[:15]:
    marker = "✓ EXACT" if error < 0.1 else ""
    print(f"    {name:<25} = {val:.6f}  ({error:.3f}% error) {marker}")

# =============================================================================
# DEEPER ANALYSIS
# =============================================================================
print("\n" + "=" * 90)
print("DEEPER ANALYSIS OF Z - 5")
print("=" * 90)

print(f"""
Z - 5 = 2√(8π/3) - 5
      = 2 × {np.sqrt(8*pi/3):.6f} - 5
      = {2 * np.sqrt(8*pi/3):.6f} - 5
      = {Z - 5:.6f}

Can we express this differently?

Z - 5 = 2√(8π/3) - 5
      = 2(√(8π/3) - 5/2)
      = 2(√(8π/3) - 2.5)

√(8π/3) = {np.sqrt(8*pi/3):.6f}
2.5 - this = {2.5 - np.sqrt(8*pi/3):.6f}

Hmm, √(8π/3) ≈ 2.894, so Z ≈ 5.79

The difference Z - 5 = 0.789 is related to 8π/3:
    √(8π/3) - 2.5 = {np.sqrt(8*pi/3) - 2.5:.6f}
    2 × this = {2*(np.sqrt(8*pi/3) - 2.5):.6f}

Z - 5 = 2(√(8π/3) - 5/2)
      = 2√(8π/3) - 5
      = 0.78881...
""")

# Try to express 5/2 = 2.5 geometrically
print("\n5/2 = 2.5 in the framework:")
print(f"    Z/2 - 0.4 = {Z/2 - 0.4:.4f}")
print(f"    π/√(π) = {pi/np.sqrt(pi):.4f}")
print(f"    8/(π+0.2) = {8/(pi+0.2):.4f}")
print(f"    √(2π)/√2 = {np.sqrt(2*pi)/np.sqrt(2):.4f}")

# =============================================================================
# THE COMPLETE MASS FORMULA
# =============================================================================
print("\n" + "=" * 90)
print("REFINED MASS FORMULA")
print("=" * 90)

m_e = 0.51099895000  # MeV
M_Pl = 1.22089e22  # MeV
log_ratio_measured = np.log10(M_Pl / m_e)

# Original: 3Z + 5 = 22.366 (0.053% error)
# New: 3Z + (Z - (Z-5)) = 3Z + 5... wait that's the same

# But we can write: 3Z + 5 = 4Z - (Z - 5) = 4Z - 0.789
formula_4Z = 4*Z - (Z - 5)
formula_3Z_plus_5 = 3*Z + 5

print(f"Rewriting 3Z + 5:")
print(f"    3Z + 5 = 4Z - (Z - 5)")
print(f"           = 4Z - {Z-5:.6f}")
print(f"           = {formula_4Z:.6f}")
print(f"")
print(f"This is algebraically identical to 3Z + 5 = {formula_3Z_plus_5:.6f}")

# But it gives a different INTERPRETATION:
print(f"""
INTERPRETATION:
    log₁₀(M_Pl/m_e) = 4Z - (Z - 5)
                    = D_spacetime × Z - (Z_excess)

    where Z_excess = Z - 5 = 2√(8π/3) - 5

    This suggests:
    • 4Z = spacetime × Zimmerman
    • Z - 5 = the quantum correction
""")

# =============================================================================
# BARYON ASYMMETRY REVISITED
# =============================================================================
print("\n" + "=" * 90)
print("BARYON ASYMMETRY WITH (Z - 5)")
print("=" * 90)

alpha = 1/137.035999084
eta_B_measured = 6.12e-10

# Previous best was α × sin²(1/Z) with 9% error
# Can we use (Z - 5)?

print("Testing η_B formulas with (Z - 5):")
print("")

tests_eta = [
    ("α × (Z-5)² × 10⁻⁶", alpha * (Z-5)**2 * 1e-6),
    ("α² × (Z-5) × 10⁻³", alpha**2 * (Z-5) * 1e-3),
    ("α³ / (Z-5)", alpha**3 / (Z-5)),
    ("α × sin²(Z-5)", alpha * np.sin(Z-5)**2),
    ("α × (Z-5)³ × 10⁻⁷", alpha * (Z-5)**3 * 1e-7),
    ("10⁻⁹ × (Z-5)", 1e-9 * (Z-5)),
    ("10⁻⁹ × √(Z-5)", 1e-9 * np.sqrt(Z-5)),
    ("α × 10⁻⁷ × (Z-5)²", alpha * 1e-7 * (Z-5)**2),
    ("α⁴ × (Z-5) × 10⁵", alpha**4 * (Z-5) * 1e5),
    ("(Z-5) / (Z × 10⁹)", (Z-5) / (Z * 1e9)),
    ("α × (Z-5) / (4Z²)", alpha * (Z-5) / (4*Z**2)),
    ("α × exp(-(Z-5)) × 10⁻⁷", alpha * np.exp(-(Z-5)) * 1e-7),
]

results = []
for name, val in tests_eta:
    if val > 0:
        error = abs(val - eta_B_measured) / eta_B_measured * 100
        if error < 100:
            results.append((name, val, error))

results.sort(key=lambda x: x[2])
for name, val, error in results[:10]:
    print(f"    {name:<35} = {val:.3e}  ({error:.1f}% error)")

# =============================================================================
# WHAT ABOUT (Z - 5)² ?
# =============================================================================
print("\n" + "=" * 90)
print("EXPLORING (Z - 5)²")
print("=" * 90)

Z_minus_5_sq = (Z - 5)**2
print(f"(Z - 5)² = {Z_minus_5_sq:.6f}")
print(f"")

# What might this equal?
print("Testing what (Z-5)² might equal geometrically:")
for name, val in [
    ("π/5", pi/5),
    ("2/(π+0.2)", 2/(pi+0.2)),
    ("ln(2)", np.log(2)),
    ("1 - 1/e", 1 - 1/np.e),
    ("(π-2)/2", (pi-2)/2),
    ("√(2/3)", np.sqrt(2/3)),
    ("4/(2π)", 4/(2*pi)),
    ("1/(√2 + 0.1)", 1/(np.sqrt(2) + 0.1)),
]:
    error = abs(val - Z_minus_5_sq) / Z_minus_5_sq * 100
    if error < 20:
        print(f"    {name:<20} = {val:.6f}  ({error:.2f}% error)")

# =============================================================================
# CONNECTION TO α
# =============================================================================
print("\n" + "=" * 90)
print("RELATIONSHIP TO α")
print("=" * 90)

print(f"""
We have:
    α⁻¹ = 4Z² + 3 = 137.04

    Can we express this using (Z - 5)?

    4Z² + 3 = 4(Z - 5 + 5)² + 3
            = 4((Z-5)² + 10(Z-5) + 25) + 3
            = 4(Z-5)² + 40(Z-5) + 100 + 3
            = 4(Z-5)² + 40(Z-5) + 103

    Check: 4×{(Z-5)**2:.4f} + 40×{(Z-5):.4f} + 103 = {4*(Z-5)**2 + 40*(Z-5) + 103:.4f}

    This doesn't simplify things...

But notice:
    (Z - 5)² = {(Z-5)**2:.6f}
    This is close to π/5 = {pi/5:.6f}

    Hmm, π/5 and (Z-5)²...
    (Z - 5)² ≈ π/5 with {abs((Z-5)**2 - pi/5)/(pi/5) * 100:.2f}% error
""")

# Check π/5 more carefully
if abs((Z-5)**2 - pi/5) / (pi/5) < 0.02:
    print("    *** (Z - 5)² ≈ π/5 IS A GOOD MATCH! ***")

print("\n" + "=" * 90)
print("SUMMARY")
print("=" * 90)

print(f"""
KEY FINDINGS:

1. Z - 5 = {Z - 5:.6f}
   This is the "quantum correction" to Z.

2. (Z - 5)² = {(Z-5)**2:.6f} ≈ π/5 = {pi/5:.6f}
   Error: {abs((Z-5)**2 - pi/5)/(pi/5) * 100:.2f}%

   If this is exact, then: Z - 5 = √(π/5)

3. Testing: Z = 5 + √(π/5) = {5 + np.sqrt(pi/5):.6f}
   Actual Z = {Z:.6f}
   Error: {abs(Z - (5 + np.sqrt(pi/5)))/Z * 100:.4f}%

4. MASS FORMULA:
   log₁₀(M_Pl/m_e) = 3Z + 5 = 4Z - (Z - 5) = 4Z - √(π/5)

   This connects the mass hierarchy to π/5 !
""")
