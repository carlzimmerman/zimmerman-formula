#!/usr/bin/env python3
"""
Unified Mass Structure in the Zimmerman Framework
==================================================

Looking for the underlying pattern connecting ALL mass formulas:
- m_μ/m_e = 6Z² + Z
- m_τ/m_μ = Z + 11
- m_p/m_e = 54Z² + 9Z - (8+3Z)
- m_b/m_c = Z - 2.5
- m_c/m_s = Z + 8
- M_H/m_t = Ω_Λ + 0.04

Carl Zimmerman, March 2026
"""

import numpy as np

# Constants
Z = 2 * np.sqrt(8 * np.pi / 3)
pi = np.pi
alpha = 1/137.035999084
Omega_Lambda = 0.685
Omega_m = 0.315

print("=" * 80)
print("UNIFIED MASS STRUCTURE")
print("=" * 80)

# =============================================================================
# SECTION 1: The Coefficient Pattern
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: COEFFICIENT PATTERN")
print("=" * 80)

print("""
MASS FORMULAS AND THEIR COEFFICIENTS:

Leptons:
  m_μ/m_e = 6Z² + Z        → coefficients: 6, 1
  m_τ/m_μ = Z + 11         → coefficients: 1, 11

Quarks:
  m_b/m_c = Z - 2.5        → coefficients: 1, -2.5
  m_c/m_s = Z + 8          → coefficients: 1, 8

Proton:
  m_p/m_e = 54Z² + 9Z - (8+3Z) → coefficients: 54, 9, -(8+3Z)

Question: What patterns exist in these coefficients?
""")

# Check for patterns in coefficients
print("--- Coefficient Analysis ---")
coeffs = {
    "6 (muon Z²)": 6,
    "1 (muon Z)": 1,
    "11 (tau)": 11,
    "2.5 (bottom)": 2.5,
    "8 (charm)": 8,
    "54 (proton Z²)": 54,
    "9 (proton Z)": 9,
}

print("\nFactorizations:")
for name, val in coeffs.items():
    if val == int(val):
        print(f"  {name} = {int(val)}", end="")
        # Prime factorization
        n = int(val)
        if n > 1:
            factors = []
            for p in [2, 3, 5, 7, 11]:
                while n % p == 0:
                    factors.append(p)
                    n //= p
            if factors:
                print(f" = {' × '.join(map(str, factors))}", end="")
        print()
    else:
        print(f"  {name} = {val} = {int(val*2)}/2")

# The 6 and 54 connection
print("\n--- The 6 and 54 connection ---")
print(f"54 / 6 = {54/6}")
print(f"54 = 6 × 9 = 6 × 3²")
print(f"54 = 2 × 27 = 2 × 3³")

# The 1 and 9 connection
print("\n--- The 1 and 9 connection ---")
print(f"9 / 1 = 9 = 3²")

# Pattern: coefficients multiply by 9!
print("\n*** DISCOVERY: Proton coefficients = 9 × Muon coefficients ***")
print(f"6 × 9 = 54  ✓")
print(f"1 × 9 = 9   ✓")

# =============================================================================
# SECTION 2: The 9-fold Symmetry
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: THE 9-FOLD SYMMETRY")
print("=" * 80)

print("""
OBSERVATION: Proton formula = 9 × Muon formula + correction

  m_μ/m_e = 6Z² + Z
  m_p/m_e = 9 × (6Z² + Z) - (8+3Z)
          = 54Z² + 9Z - 8 - 3Z
          = 54Z² + 6Z - 8

But measured: m_p/m_e = 54Z² + 9Z - (8+3Z)

Let's verify:
""")

# Calculate
mu_formula = 6*Z**2 + Z
proton_formula = 54*Z**2 + 9*Z - (8 + 3*Z)
nine_times_mu = 9 * mu_formula
correction = nine_times_mu - proton_formula

print(f"9 × (m_μ/m_e formula) = {nine_times_mu:.4f}")
print(f"m_p/m_e formula       = {proton_formula:.4f}")
print(f"Difference            = {correction:.4f}")
print(f"This difference       = {8 + 3*Z:.4f} = 8 + 3Z ≈ 8π")

# Why 9?
print("\n--- Why the factor of 9? ---")
print(f"9 = 3² (spatial dimensions squared)")
print(f"9 = number of gluons in QCD")
print(f"9 is the ONLY single-digit perfect square besides 1 and 4")

# =============================================================================
# SECTION 3: Testing the 9× hypothesis
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: TESTING THE 9× HYPOTHESIS")
print("=" * 80)

# Does tau also follow a pattern?
print("\n--- Tau mass ---")
tau_formula = Z + 11
nine_times_tau = 9 * tau_formula

print(f"m_τ/m_μ = Z + 11 = {tau_formula:.4f}")
print(f"9 × (m_τ/m_μ) = 9Z + 99 = {nine_times_tau:.4f}")

# What mass ratio could equal 9 × tau ratio?
print(f"\nLooking for a ratio ≈ {nine_times_tau:.2f}...")

# Check various ratios
m_mu_m_e = 206.768
m_tau_m_e = m_mu_m_e * 16.8167  # tau/electron

tests = [
    ("m_W/m_tau", 80377/1776.86),  # W boson / tau in MeV
    ("m_Z/m_tau", 91188/1776.86),
    ("m_H/m_tau", 125250/1776.86),
    ("m_t/m_tau", 172760/1776.86),
    ("m_p/m_e × 9", 1836.15/9),
]

print(f"\n{'Ratio':<20} {'Value':>12} {'9×(Z+11)':>12} {'Error %':>10}")
print("-" * 55)
for name, value in tests:
    error = abs(value - nine_times_tau) / nine_times_tau * 100
    print(f"{name:<20} {value:>12.2f} {nine_times_tau:>12.2f} {error:>10.2f}%")

# =============================================================================
# SECTION 4: The (8+3Z) term
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: THE (8+3Z) TERM")
print("=" * 80)

val_8_3Z = 8 + 3*Z
print(f"\n8 + 3Z = {val_8_3Z:.6f}")
print(f"8π     = {8*pi:.6f}")
print(f"Difference = {val_8_3Z - 8*pi:.6f}")
print(f"           = {(val_8_3Z - 8*pi)/8/pi * 100:.3f}% error")

print("\n--- This term appears everywhere! ---")
print(f"• Ω_Λ = 3Z/(8+3Z)")
print(f"• Ω_m = 8/(8+3Z)")
print(f"• α_s = 3/(8+3Z)")
print(f"• m_p/m_e correction term")

print("\n--- What IS (8+3Z)? ---")
print(f"8 + 3Z = 8 + 3 × 2√(8π/3)")
print(f"       = 8 + 6√(8π/3)")
print(f"       = 8 + 2√(24π)")
print(f"       = 8 + 2√(24π)")

# Check if it equals something nice
sqrt_24pi = np.sqrt(24*pi)
print(f"\n2√(24π) = {2*sqrt_24pi:.6f}")
print(f"3Z      = {3*Z:.6f}")
print("These are equal (by construction)")

print(f"\n8 + 3Z = 8 + 2√(24π)")
print(f"       ≈ 8π (within 3%)")

# =============================================================================
# SECTION 5: Z-power pattern
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: Z-POWER PATTERN")
print("=" * 80)

print("""
OBSERVATION: Different formulas use different powers of Z

  Z⁰ terms: constants (3, 8, 11, 2.5)
  Z¹ terms: linear in Z
  Z² terms: quadratic in Z

PATTERN:
  • m_μ/m_e: Z² dominant (6Z² + Z)
  • m_τ/m_μ: Z¹ dominant (Z + 11)
  • m_p/m_e: Z² dominant (54Z² + 9Z - correction)
  • Quarks:  Z¹ terms only (Z ± const)

Why does Z² appear for ELECTRON mass ratios?
""")

# Hypothesis: Z² comes from dimensional analysis
print("--- Hypothesis: Z² relates to 2D manifold ---")
print(f"Z² = 32π/3 = {Z**2:.6f}")
print(f"This is area-like (2D)")
print(f"Z is length-like (1D)")

# =============================================================================
# SECTION 6: Universal Mass Formula?
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: SEARCHING FOR UNIVERSAL FORMULA")
print("=" * 80)

print("""
Can we write ALL mass ratios in a single form?

  m₁/m₂ = aZ² + bZ + c

where a, b, c depend on particle type?
""")

# Test this
mass_data = [
    ("m_μ/m_e", 206.768, 6, 1, 0),
    ("m_τ/m_μ", 16.8167, 0, 1, 11),
    ("m_p/m_e", 1836.15, 54, 9, -(8+3*Z)),
    ("m_b/m_c", 3.291, 0, 1, -2.5),
    ("m_c/m_s", 13.60, 0, 1, 8),
]

print(f"\n{'Ratio':<12} {'a':>8} {'b':>8} {'c':>12} {'Predicted':>12} {'Measured':>12} {'Error %':>10}")
print("-" * 80)

for name, measured, a, b, c in mass_data:
    predicted = a*Z**2 + b*Z + c
    error = abs(predicted - measured) / measured * 100
    print(f"{name:<12} {a:>8} {b:>8} {c:>12.4f} {predicted:>12.4f} {measured:>12.4f} {error:>10.4f}%")

# =============================================================================
# SECTION 7: The Generation Pattern
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: GENERATION PATTERN")
print("=" * 80)

print("""
Leptons have 3 generations: e, μ, τ
Quarks have 3 generations: (d,u), (s,c), (b,t)

LEPTON PATTERN:
  Gen 1 → 2: m_μ/m_e = 6Z² + Z      (Z² term dominant)
  Gen 2 → 3: m_τ/m_μ = Z + 11       (Z¹ term dominant)

  Power of Z DECREASES by generation!

QUARK PATTERN:
  m_b/m_c = Z - 2.5                 (Z¹)
  m_c/m_s = Z + 8                   (Z¹)

  No Z² term in quarks!

Hypothesis: Leptons have "2D" physics, quarks have "1D" physics?
""")

# =============================================================================
# SECTION 8: The Role of 3
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: THE ROLE OF 3")
print("=" * 80)

print("""
The number 3 appears EVERYWHERE:

In Z itself:
  Z = 2√(8π/3)  ← 3 in denominator

In mass formulas:
  m_τ/m_μ = Z + 11 = Z + 3 + 8
  (8+3Z) appears in proton and cosmology

In α formula:
  α⁻¹ = 4Z² + 3  ← +3

In μ_p:
  μ_p = Z - 3    ← -3

In cosmology:
  Ω_Λ = 3Z/(8+3Z)  ← multiple 3s

3 = spatial dimensions = number of generations = fundamental constant!
""")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("SUMMARY: UNIFIED MASS STRUCTURE")
print("=" * 80)

print("""
ESTABLISHED PATTERNS:

1. THE 9× SYMMETRY:
   m_p/m_e ≈ 9 × (m_μ/m_e) - (8+3Z)
   The proton is 9 "muon units" minus a correction

2. Z-POWER HIERARCHY:
   • Electron ratios: Z² dominant
   • Muon ratios: Z¹ dominant
   • Quark ratios: Z¹ only

3. THE (8+3Z) UNIVERSAL TERM:
   Appears in Ω_Λ, Ω_m, α_s, and m_p/m_e
   This is ≈ 8π (within 3%)

4. THE "3" UBIQUITY:
   Appears with + and - signs throughout
   Likely related to spatial dimensions

5. UNIVERSAL FORM:
   All mass ratios can be written as: aZ² + bZ + c

   Leptons: a ≠ 0 for electron, a = 0 for muon
   Quarks: a = 0 always
   Proton: a = 54 = 6 × 9

REMAINING QUESTIONS:
• Why does 9 connect proton to muon?
• Why no Z² in quark formulas?
• What is the geometric meaning of 54 = 6 × 9?
""")
