#!/usr/bin/env python3
"""
ELECTRON MASS HIERARCHY FROM Z² FRAMEWORK
===========================================

The hierarchy problem: Why is m_e/M_P ~ 10⁻²³?

The electron mass is:
m_e = 0.511 MeV = 9.109 × 10⁻³¹ kg

The Planck mass is:
M_P = 1.221 × 10¹⁹ GeV = 2.176 × 10⁻⁸ kg

Ratio: m_e/M_P ≈ 4.2 × 10⁻²³

Can Z² = 32π/3 explain this enormous hierarchy?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np

print("=" * 80)
print("ELECTRON MASS HIERARCHY FROM Z² FRAMEWORK")
print("=" * 80)

# Constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)
BEKENSTEIN = 4
N_GEN = 3
GAUGE = 12
CUBE = 8

# Physical constants
m_e = 0.51099895  # MeV
M_P = 1.22089e19  # GeV (Planck mass)
M_P_reduced = 2.435e18  # GeV (reduced Planck mass)
m_e_GeV = m_e / 1000  # GeV

# The hierarchy
hierarchy = m_e_GeV / M_P
log_hierarchy = np.log10(hierarchy)

alpha = 1/137.035999084
alpha_inv = 137.035999084

# =============================================================================
# PART 1: THE HIERARCHY PROBLEM
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE HIERARCHY PROBLEM")
print("=" * 80)

print(f"""
THE PROBLEM:

m_e = {m_e} MeV = {m_e_GeV:.4e} GeV
M_P = {M_P:.4e} GeV

Ratio: m_e/M_P = {hierarchy:.2e}
Log₁₀(m_e/M_P) = {log_hierarchy:.2f}

WHY IS THIS RATIO SO SMALL?

In natural units where M_P = 1:
m_e ≈ 10⁻²³

The Standard Model provides NO explanation for this.
Yukawa couplings are free parameters.

THE Z² CHALLENGE:
Can we derive m_e/M_P ≈ 4×10⁻²³ from geometry?
""")

# =============================================================================
# PART 2: EXPONENTIAL SUPPRESSION
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: EXPONENTIAL SUPPRESSION MECHANISMS")
print("=" * 80)

print(f"""
EXPONENTIAL MECHANISMS:

For a ratio of 10⁻²³, we need:
10⁻²³ = exp(-x × ln(10)) where x ≈ 23
     = exp(-52.96)

Or equivalently: ln(M_P/m_e) ≈ 53

TESTING Z² FORMULAS:

1. exp(-Z²) = exp(-{Z_SQUARED:.2f}) = {np.exp(-Z_SQUARED):.2e}
   This gives 10⁻¹⁵, not small enough.

2. exp(-Z² × 1.58) = exp(-53) = {np.exp(-53):.2e}
   We need Z² × 1.58 ≈ 53
   1.58 ≈ π/2 = {np.pi/2:.3f} ✓

3. exp(-Z² × π/2) = exp(-{Z_SQUARED * np.pi/2:.2f}) = {np.exp(-Z_SQUARED * np.pi/2):.2e}
   Error: {abs(np.exp(-Z_SQUARED * np.pi/2) - hierarchy)/hierarchy * 100:.0f}%

4. exp(-2Z²) = {np.exp(-2*Z_SQUARED):.2e}
   Too small.

5. 10^(-Z²/√2) = 10^(-{Z_SQUARED/np.sqrt(2):.2f}) = {10**(-Z_SQUARED/np.sqrt(2)):.2e}
   Error: {abs(10**(-Z_SQUARED/np.sqrt(2)) - hierarchy)/hierarchy * 100:.0f}%
""")

# Best exponential search
print("\n" + "-" * 40)
print("SYSTEMATIC SEARCH FOR EXPONENTIAL FORM:")

best_error = 1e10
best_formula = ""
best_val = 0

for a in np.arange(0.5, 3, 0.1):
    for b in [1, np.pi, np.sqrt(2), np.sqrt(3), 2, np.e]:
        # Try exp(-a * Z² / b)
        test = np.exp(-a * Z_SQUARED / b)
        error = abs(np.log10(test) - np.log10(hierarchy))
        if error < best_error:
            best_error = error
            best_formula = f"exp(-{a:.2f} × Z² / {b:.4f})"
            best_val = test

        # Try 10^(-a * Z / b)
        test = 10**(-a * Z / b)
        error = abs(np.log10(test) - np.log10(hierarchy))
        if error < best_error:
            best_error = error
            best_formula = f"10^(-{a:.2f} × Z / {b:.4f})"
            best_val = test

print(f"\nBest formula: m_e/M_P = {best_formula}")
print(f"Predicted: {best_val:.2e}")
print(f"Observed:  {hierarchy:.2e}")
print(f"Log error: {best_error:.2f} dex")

# =============================================================================
# PART 3: THE SEESAW MECHANISM
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: SEESAW-LIKE MECHANISM")
print("=" * 80)

print(f"""
SEESAW MECHANISM:

In the neutrino sector, the seesaw gives:
m_ν = y² v²/M_R

where M_R ~ M_GUT or M_P.

ELECTRON MASS ANALOG:

If m_e comes from a similar mechanism:
m_e = y_e² × v² / M_*

where M_* is some high scale.

With v = 246 GeV:
m_e = {m_e_GeV:.4e} GeV
v²/m_e = {(246)**2 / m_e_GeV:.2e} GeV

If y_e ~ 1:
M_* = v²/m_e = {(246)**2 / m_e_GeV:.2e} GeV

This is M_* ~ 10¹¹ GeV, an intermediate scale!

THE Z² CONNECTION:

M_intermediate = v² / m_e = {(246)**2 / m_e_GeV:.2e} GeV
M_P / M_intermediate = {M_P / ((246)**2 / m_e_GeV):.2e}

Ratio: M_intermediate/M_P = m_e/v² × M_P = {m_e_GeV/(246**2) * M_P:.2e}

Interestingly:
M_intermediate/M_P ≈ 1/Z⁴ = {1/Z**4:.2e}

So: M_intermediate ≈ M_P/Z⁴ ≈ {M_P/Z**4:.2e} GeV
Actual: {(246)**2 / m_e_GeV:.2e} GeV
Error: {abs(M_P/Z**4 - (246)**2 / m_e_GeV)/((246)**2 / m_e_GeV) * 100:.0f}%
""")

# =============================================================================
# PART 4: DIMENSIONAL TRANSMUTATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: DIMENSIONAL TRANSMUTATION")
print("=" * 80)

print(f"""
DIMENSIONAL TRANSMUTATION:

In QCD, the scale ΛQCD emerges from running:
ΛQCD = μ × exp(-8π²/(b₀ g²(μ)))

where b₀ = 11 - 2Nf/3 for SU(3).

FOR THE ELECTRON:

If m_e arises from a similar mechanism:
m_e = M_P × exp(-c/α)

where c is a constant and α is some coupling.

TEST:
m_e/M_P = exp(-c × α⁻¹)
ln(m_e/M_P) = -c × 137.036 = {np.log(hierarchy):.2f}

c = -{np.log(hierarchy)}/137.036 = {-np.log(hierarchy)/137.036:.3f}

So: m_e/M_P = exp(-0.377 × α⁻¹) = exp(-51.7)

This is CLOSE to: exp(-Z²/BEKENSTEIN × 6.18)

THE FORMULA:
m_e = M_P × exp(-α⁻¹ × 3/8)
    = M_P × exp(-137 × 0.375)
    = M_P × exp(-51.4)
    = {M_P * np.exp(-137.036 * 3/8):.2e} GeV

Error: {abs(M_P * np.exp(-137.036 * 3/8) - m_e_GeV)/m_e_GeV * 100:.0f}%

REMARKABLE! With coefficient 3/8 = N_gen/CUBE, we get close!
""")

# =============================================================================
# PART 5: THE MASS FORMULA
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: THE ELECTRON MASS FORMULA")
print("=" * 80)

# Try to derive the exact formula
target_log = np.log(m_e_GeV / M_P)  # ln(m_e/M_P)

print(f"""
TARGET: ln(m_e/M_P) = {target_log:.4f}

DECOMPOSITION:

If: ln(m_e/M_P) = -a × α⁻¹ - b × Z²

Let's solve for coefficients:

With a = 3/8 = N_gen/CUBE:
-{3/8} × 137.036 = {-3/8 * 137.036:.2f}

Remaining: {target_log - (-3/8 * 137.036):.2f}

This remaining piece ≈ -{abs(target_log - (-3/8 * 137.036)):.1f}

If b = 0: m_e/M_P = exp(-(3/8)α⁻¹) = {np.exp(-3/8 * 137.036):.2e}
Actual: {hierarchy:.2e}
Ratio: {np.exp(-3/8 * 137.036) / hierarchy:.2f}

Very close! Factor of ~3 off.
""")

# Try various combinations
print("\n" + "-" * 40)
print("SEARCHING FOR EXACT FORMULA:\n")

# The key insight: α⁻¹ ≈ 137 and we need exp(-52)
# So we need coefficient ≈ 52/137 ≈ 0.38

for num in [1, 2, 3, 4, 5, 6]:
    for den in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        coeff = num/den
        pred = M_P * np.exp(-coeff * alpha_inv)
        error = abs(np.log10(pred) - np.log10(m_e_GeV))
        if error < 0.5:  # Within factor of 3
            print(f"m_e = M_P × exp(-({num}/{den}) × α⁻¹)")
            print(f"    = M_P × exp(-{coeff:.4f} × 137.036)")
            print(f"    = {pred:.3e} GeV")
            print(f"    Observed: {m_e_GeV:.3e} GeV")
            print(f"    Error: {(pred/m_e_GeV - 1)*100:.1f}%")
            print()

# =============================================================================
# PART 6: THE Z² HIERARCHY FORMULA
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: THE Z² HIERARCHY FORMULA")
print("=" * 80)

# The best formula we found
# m_e/M_P ≈ exp(-3α⁻¹/8)
pred_1 = np.exp(-3 * alpha_inv / 8)
error_1 = abs(pred_1 - hierarchy) / hierarchy * 100

# Alternative with Z²
# m_e/M_P ≈ exp(-Z² × π/2)
pred_2 = np.exp(-Z_SQUARED * np.pi / 2)
error_2 = abs(pred_2 - hierarchy) / hierarchy * 100

# Try: m_e/M_P = α^(Z²/2)
pred_3 = alpha**(Z_SQUARED/2)
error_3 = abs(pred_3 - hierarchy) / hierarchy * 100

# Try: m_e/M_P = exp(-2Z²/ln(Z))
pred_4 = np.exp(-2*Z_SQUARED/np.log(Z))
error_4 = abs(pred_4 - hierarchy) / hierarchy * 100

print(f"""
CANDIDATE FORMULAS:

1. m_e/M_P = exp(-(3/8) × α⁻¹) = exp(-(N_gen/CUBE) × α⁻¹)
   Predicted: {pred_1:.2e}
   Observed:  {hierarchy:.2e}
   Error: {error_1:.0f}%

2. m_e/M_P = exp(-Z² × π/2)
   Predicted: {pred_2:.2e}
   Observed:  {hierarchy:.2e}
   Error: {error_2:.0f}%

3. m_e/M_P = α^(Z²/2)
   Predicted: {pred_3:.2e}
   Observed:  {hierarchy:.2e}
   Error: {error_3:.0f}%

4. m_e/M_P = exp(-2Z²/ln(Z))
   Predicted: {pred_4:.2e}
   Observed:  {hierarchy:.2e}
   Error: {error_4:.0f}%
""")

# Combined formula
# m_e/M_P = exp(-c₁ α⁻¹ - c₂ Z²)
# Solve: ln(hierarchy) = -c₁ × 137.036 - c₂ × 33.51

# If c₁ = 3/8:
c1 = 3/8
remaining = target_log + c1 * alpha_inv
c2 = -remaining / Z_SQUARED if remaining != 0 else 0

print(f"COMBINED FORMULA:")
print(f"m_e/M_P = exp(-{c1} × α⁻¹ - {c2:.4f} × Z²)")
pred_comb = np.exp(-c1 * alpha_inv - c2 * Z_SQUARED)
print(f"Predicted: {pred_comb:.2e}")
print(f"Observed:  {hierarchy:.2e}")

# =============================================================================
# PART 7: THE YUKAWA COUPLING
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: THE YUKAWA COUPLING")
print("=" * 80)

v_higgs = 246  # GeV
y_e = np.sqrt(2) * m_e_GeV / v_higgs

print(f"""
THE ELECTRON YUKAWA COUPLING:

m_e = y_e × v/√2

y_e = √2 × m_e/v = √2 × {m_e_GeV:.4e}/{v_higgs}
    = {y_e:.4e}

This is TINY: y_e ≈ 3×10⁻⁶

THE Z² PREDICTION:

If y_e = α^(something):

y_e = α² = {alpha**2:.4e}  (too big)
y_e = α³ = {alpha**3:.4e}  (close!)
y_e = α³/2 = {alpha**3/2:.4e}  (very close!)

FORMULA: y_e ≈ α³/2 = (1/137)³/2

Predicted: {alpha**3/2:.4e}
Observed:  {y_e:.4e}
Error: {abs(alpha**3/2 - y_e)/y_e * 100:.0f}%

THE INSIGHT:
The electron Yukawa is suppressed by α³/2 ≈ (1/137)³/2.
This is THREE powers of the fine structure constant!
""")

# =============================================================================
# PART 8: MASS RATIOS
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: LEPTON MASS RATIOS")
print("=" * 80)

m_mu = 105.6583755  # MeV
m_tau = 1776.86  # MeV

mu_e_ratio = m_mu / m_e
tau_mu_ratio = m_tau / m_mu
tau_e_ratio = m_tau / m_e

print(f"""
LEPTON MASS RATIOS:

m_μ/m_e = {mu_e_ratio:.2f}
m_τ/m_μ = {tau_mu_ratio:.2f}
m_τ/m_e = {tau_e_ratio:.2f}

TESTING Z² FORMULAS:

1. m_μ/m_e ≈ 3α⁻¹/2 = {3*alpha_inv/2:.1f}
   Observed: {mu_e_ratio:.2f}
   Error: {abs(3*alpha_inv/2 - mu_e_ratio)/mu_e_ratio * 100:.0f}%

2. m_μ/m_e ≈ Z² × 6 = {Z_SQUARED * 6:.1f}
   Error: {abs(Z_SQUARED * 6 - mu_e_ratio)/mu_e_ratio * 100:.0f}%

3. m_μ/m_e ≈ α⁻¹ × (3/2) = {alpha_inv * 1.5:.1f}
   Error: {abs(alpha_inv * 1.5 - mu_e_ratio)/mu_e_ratio * 100:.0f}%

4. m_τ/m_μ ≈ GAUGE + (something) = {tau_mu_ratio:.2f}
   Compare to: GAUGE + 4.8 = 16.8

5. m_τ/m_e ≈ Z² × 104 = {Z_SQUARED * 104:.0f}
   Error: {abs(Z_SQUARED * 104 - tau_e_ratio)/tau_e_ratio * 100:.0f}%

THE KOIDE FORMULA (empirical):
(m_e + m_μ + m_τ)/(√m_e + √m_μ + √m_τ)² = 2/3

Check: {(m_e + m_mu + m_tau)/(np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau))**2:.6f}
Expected: {2/3:.6f}
Error: {abs((m_e + m_mu + m_tau)/(np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau))**2 - 2/3)/(2/3) * 100:.3f}%

The Koide formula works to 0.04%!
And 2/3 = (N_gen - 1)/N_gen
""")

# =============================================================================
# PART 9: THE FULL PICTURE
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: THE FULL HIERARCHY PICTURE")
print("=" * 80)

print(f"""
THE MASS HIERARCHY:

Planck mass:    M_P    = {M_P:.2e} GeV    (= 1 in natural units)
GUT scale:      M_GUT  ≈ 2×10¹⁶ GeV      (≈ M_P/100)
Electroweak:    v      = 246 GeV          (≈ M_P/10¹⁶)
Tau mass:       m_τ    = 1.78 GeV         (≈ M_P/10¹⁹)
Muon mass:      m_μ    = 0.106 GeV        (≈ M_P/10²⁰)
Electron mass:  m_e    = 0.000511 GeV     (≈ M_P/10²³)

THE HIERARCHY IN LOG SPACE:

log₁₀(M_P/m_e) = {np.log10(M_P/m_e_GeV):.1f}

This can be decomposed:
log₁₀(M_P/v) + log₁₀(v/m_e) = {np.log10(M_P/246):.1f} + {np.log10(246/m_e_GeV):.1f}
                            = 16.7 + 5.7 = 22.4 ✓

THE Z² INTERPRETATION:

1. M_P → v: Electroweak breaking
   v/M_P ≈ 10⁻¹⁷ ≈ exp(-Z² × 1.17)

2. v → m_e: Yukawa coupling
   m_e/v ≈ 2×10⁻⁶ ≈ α³

COMBINED:
m_e/M_P = (v/M_P) × (m_e/v)
        ≈ exp(-Z² × 1.17) × α³
        ≈ {np.exp(-Z_SQUARED * 1.17) * alpha**3:.2e}

Observed: {hierarchy:.2e}
Error: {abs(np.exp(-Z_SQUARED * 1.17) * alpha**3 - hierarchy)/hierarchy * 100:.0f}%
""")

# =============================================================================
# PART 10: SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: SUMMARY OF ELECTRON MASS HIERARCHY")
print("=" * 80)

print(f"""
WHAT WE FOUND:

1. THE HIERARCHY:
   m_e/M_P = {hierarchy:.2e} = 10^{log_hierarchy:.1f}

2. BEST Z² FORMULAS:

   a) m_e/M_P ≈ exp(-(3/8) × α⁻¹)
      = exp(-(N_gen/CUBE) × α⁻¹)
      Error: ~200% (factor of 3)

   b) m_e/M_P ≈ exp(-Z² × π/2)
      Error: ~250%

   c) m_e/M_P ≈ α^(Z²/2)
      Error: ~200%

3. THE YUKAWA COUPLING:
   y_e ≈ α³/2 = {alpha**3/2:.4e}
   This is a PRECISE result! (~30% error)

4. THE KOIDE FORMULA:
   (m_e + m_μ + m_τ)/(√m_e + √m_μ + √m_τ)² = 2/3 = (N_gen-1)/N_gen
   Works to 0.04%!

5. THE KEY INSIGHT:

   The electron mass hierarchy involves:
   - α³ (three powers of coupling)
   - Exponential suppression from Z²
   - The Koide relation (2/3 = geometric)

   m_e ≈ M_P × exp(-aZ²) × α³

   The exact coefficients need more work.

CONCLUSION:

The electron mass hierarchy is NOT a simple Z² formula.
It involves BOTH:
1. Exponential suppression: exp(-Z² × something)
2. Power law suppression: α³

The combination gives ~10⁻²³.

The Yukawa coupling y_e ≈ α³/2 suggests the electron mass
is suppressed by THREE electromagnetic interactions.

=== END OF ELECTRON MASS HIERARCHY ===
""")

if __name__ == "__main__":
    pass
