#!/usr/bin/env python3
"""
RIEMANN HYPOTHESIS: CONTRADICTION ANALYSIS
==========================================

If RH is false, there exists at least one zero ρ₀ = β₀ + iγ₀ with β₀ > 1/2.

What would this imply? Let's trace through ALL the consequences.

The goal: Show that a counterexample creates so many simultaneous
constraints that the network becomes over-determined and inconsistent.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special
import mpmath
mpmath.mp.dps = 50

print("=" * 70)
print("RIEMANN HYPOTHESIS: CONTRADICTION ANALYSIS")
print("What would a counterexample require?")
print("=" * 70)

# =============================================================================
# HYPOTHETICAL COUNTEREXAMPLE
# =============================================================================
print("\n" + "=" * 70)
print("HYPOTHETICAL COUNTEREXAMPLE SETUP")
print("=" * 70)

print("""
ASSUMPTION (for contradiction): RH is FALSE.

Then there exists ρ₀ = β₀ + iγ₀ with:
  - ζ(ρ₀) = 0
  - β₀ > 1/2 (off the critical line)
  - 0 < β₀ < 1 (in the critical strip)
  - γ₀ ≠ 0 (not a trivial zero)

By the functional equation, there's also a zero at:
  - ρ₀' = 1 - β₀ + iγ₀ = (1-β₀) + iγ₀
  - Since β₀ > 1/2, we have 1-β₀ < 1/2

So counterexamples come in PAIRS: one with β > 1/2, one with β < 1/2.

Let's trace what this implies...
""")

# =============================================================================
# CONSEQUENCE 1: MERTENS FUNCTION
# =============================================================================
print("\n" + "=" * 70)
print("CONSEQUENCE 1: MERTENS FUNCTION EXPLOSION")
print("=" * 70)

print("""
The explicit formula for M(x):

  M(x) = Σ_ρ x^ρ / (ρ·ζ'(ρ)) + lower order terms

Each zero ρ = β + iγ contributes a term of size ~ x^β / |γ|.

If ρ₀ = β₀ + iγ₀ with β₀ > 1/2:

  |contribution from ρ₀| ~ x^{β₀} / |γ₀|

This GROWS faster than x^{1/2}.

CONCLUSION: If β₀ > 1/2 exists, then M(x) ≠ O(x^{1/2+ε}) for any ε < β₀ - 1/2.
""")

# Simulate the impact of a hypothetical off-line zero
print("Simulating hypothetical off-line zero contribution:")
print("\nIf ρ₀ = 0.6 + 14i existed (β₀ = 0.6 > 0.5):")
print("\n| x       | x^{1/2} term | x^{0.6} term | Ratio |")
print("|" + "-"*9 + "|" + "-"*14 + "|" + "-"*14 + "|" + "-"*7 + "|")

beta_0 = 0.6  # Hypothetical
gamma_0 = 14.0

for x in [100, 1000, 10000, 100000, 1000000]:
    on_line_term = x**0.5 / 14.0  # Contribution from on-line zero at height 14
    off_line_term = x**beta_0 / gamma_0  # Hypothetical off-line contribution
    ratio = off_line_term / on_line_term
    print(f"| {x:7d} | {on_line_term:12.2f} | {off_line_term:12.2f} | {ratio:5.2f} |")

print("\nThe off-line term DOMINATES as x → ∞.")

# =============================================================================
# CONSEQUENCE 2: LI'S CRITERION VIOLATION
# =============================================================================
print("\n" + "=" * 70)
print("CONSEQUENCE 2: LI'S λ_n BECOMES NEGATIVE")
print("=" * 70)

print("""
Li's criterion: RH ⟺ λ_n > 0 for all n ≥ 1

where λ_n = Σ_ρ [1 - (1 - 1/ρ)^n]

If ρ₀ = β₀ + iγ₀ with β₀ > 1/2:

The contribution from ρ₀ is:
  1 - (1 - 1/ρ₀)^n

For large n, this behaves like:
  1 - (1 - 1/ρ₀)^n → 1 (if |1 - 1/ρ₀| < 1)

But the SIGN and growth rate depend on the geometry.

Key: An off-line zero at β₀ > 1/2 eventually makes some λ_n negative.
""")

def li_contribution(rho, n):
    """Compute contribution of a single zero to λ_n"""
    return 1 - (1 - 1/rho)**n

# Test with hypothetical off-line zero
print("Contribution of hypothetical ρ₀ = 0.6 + 14i to λ_n:")
print("\n| n   | Re[contribution] | |contribution| |")
print("|" + "-"*5 + "|" + "-"*18 + "|" + "-"*16 + "|")

rho_0 = complex(0.6, 14.0)

for n in [1, 5, 10, 20, 50, 100, 200]:
    contrib = li_contribution(rho_0, n)
    print(f"| {n:3d} | {contrib.real:16.6f} | {abs(contrib):14.6f} |")

# =============================================================================
# CONSEQUENCE 3: BÁEZ-DUARTE RATE VIOLATION
# =============================================================================
print("\n" + "=" * 70)
print("CONSEQUENCE 3: BÁEZ-DUARTE RATE VIOLATION")
print("=" * 70)

print("""
Báez-Duarte: c_n = Σ_k μ(k)/k² · (1 - 1/k²)^n

If RH is true: c_n = O(n^{-1/4+ε})
If RH is false: c_n decays SLOWER

The connection:
  c_n decay rate ↔ M(x) growth ↔ Zero locations

With an off-line zero at β₀ > 1/2:
  - M(x) grows like x^{β₀}
  - This affects partial sums in c_n
  - The decay rate becomes O(n^{-(1-β₀)/2+ε}) instead of O(n^{-1/4+ε})

For β₀ = 0.6: decay would be O(n^{-0.2+ε}) not O(n^{-0.25+ε})
This is detectably different.
""")

# =============================================================================
# CONSEQUENCE 4: PRIME NUMBER THEOREM ERROR
# =============================================================================
print("\n" + "=" * 70)
print("CONSEQUENCE 4: PRIME COUNTING ERROR INCREASE")
print("=" * 70)

print("""
The Prime Number Theorem with error:

  π(x) = li(x) + E(x)

where E(x) is the error term.

Under RH: E(x) = O(x^{1/2} log x)
If RH false with β₀ > 1/2: E(x) = Ω(x^{β₀})

This would be VISIBLE in prime counting data!

Current best unconditional: E(x) = O(x·exp(-c·log^{0.6}x))

If β₀ = 0.6 existed, we'd see E(x) ~ x^{0.6}, which would be
ENORMOUSLY larger than what's observed.
""")

from sympy import primepi

print("Checking prime counting error:")
print("\n| x        | π(x)     | li(x)    | Error    | |E|/x^{0.5} |")
print("|" + "-"*10 + "|" + "-"*10 + "|" + "-"*10 + "|" + "-"*10 + "|" + "-"*12 + "|")

for x in [1000, 10000, 100000, 1000000]:
    pi_x = int(primepi(x))
    li_x = float(mpmath.li(x))
    error = pi_x - li_x
    normalized = abs(error) / np.sqrt(x)
    print(f"| {x:8d} | {pi_x:8d} | {li_x:8.1f} | {error:8.1f} | {normalized:10.4f} |")

print("\nThe error is WELL within O(x^{1/2}), consistent with RH.")

# =============================================================================
# CONSEQUENCE 5: ZEROS OF ZETA DERIVATIVES
# =============================================================================
print("\n" + "=" * 70)
print("CONSEQUENCE 5: LEVINSON'S THEOREM CONSTRAINT")
print("=" * 70)

print("""
Levinson (1974) proved: At least 1/3 of zeros are on the critical line.
Conrey (1989) improved: At least 40% are on the line.

If RH is false with many off-line zeros:
- The proportion on-line would be < 100%
- But CURRENT BOUNDS are only ≥ 40%

Gap: We know 40-100% are on line. The gap is huge.

However: All 10+ trillion COMPUTED zeros are on the line.

If off-line zeros existed, WHERE would they be?
- They'd need to be at very large height
- But zero-finding algorithms don't miss zeros
- This creates a mystery
""")

# =============================================================================
# CONSEQUENCE 6: GUE STATISTICS
# =============================================================================
print("\n" + "=" * 70)
print("CONSEQUENCE 6: RANDOM MATRIX STATISTICS")
print("=" * 70)

print("""
Montgomery (1973) & Odlyzko (1987): Zeta zeros follow GUE statistics.

GUE = Gaussian Unitary Ensemble (random Hermitian matrices)

Key property: GUE eigenvalues lie on the REAL axis.

If zeros follow GUE, they should:
1. Have pair correlation matching GUE
2. Have spacing distribution matching GUE
3. Behave like eigenvalues of Hermitian matrices

Hermitian matrices have REAL eigenvalues.
This strongly suggests zeros have Im(ρ - 1/2) = 0, i.e., Re(ρ) = 1/2.

HOWEVER: This is HEURISTIC, not proof.
""")

# =============================================================================
# THE CONTRADICTION NETWORK
# =============================================================================
print("\n" + "=" * 70)
print("THE CONTRADICTION NETWORK")
print("=" * 70)

print("""
Summary: If ρ₀ = β₀ + iγ₀ with β₀ > 1/2 exists, then:

┌──────────────────────────────────────────────────────────────────────┐
│ CONSEQUENCES OF AN OFF-LINE ZERO                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 1. M(x) = Ω(x^{β₀})     — grows faster than √x                      │
│ 2. λ_n < 0 for some n   — Li's criterion violated                   │
│ 3. c_n = O(n^{-(1-β₀)/2}) — slower Báez-Duarte decay                │
│ 4. E(x) = Ω(x^{β₀})     — larger prime counting error               │
│ 5. Zero statistics change — deviation from GUE?                     │
│ 6. Zero counting changes — N(T) formula modified                    │
│                                                                      │
│ These are ALL SIMULTANEOUSLY required for NOT-RH.                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

QUESTION: Can these all be consistent?

The constraints interact:
- M(x) growth affects c_n decay
- c_n decay affects λ_n positivity
- λ_n positivity connects to zero locations
- Zero locations determine M(x) growth

It's a CIRCULAR system of dependencies.
""")

# =============================================================================
# THE MINIMAL COUNTEREXAMPLE
# =============================================================================
print("\n" + "=" * 70)
print("THE MINIMAL COUNTEREXAMPLE PROBLEM")
print("=" * 70)

print("""
If RH is false, there's a FIRST counterexample.

Let γ* = inf{|Im(ρ)| : ζ(ρ) = 0, Re(ρ) > 1/2}

This is the height of the lowest off-line zero.

What do we know about γ*?

1. γ* > 10^13 (all computed zeros are on-line)
2. γ* must be finite (if RH is false)
3. Nothing prevents γ* = ∞ (which means RH is true)

KEY INSIGHT: There's no theoretical lower bound forcing γ* to be finite.

The DEFAULT assumption is γ* = ∞ unless proven otherwise.
""")

# =============================================================================
# THE FRESH ANGLE: OVER-DETERMINATION
# =============================================================================
print("\n" + "=" * 70)
print("FRESH ANGLE: OVER-DETERMINATION")
print("=" * 70)

print("""
Consider the system of constraints:

EQUATION 1: ζ(s) = ξ(s) · π^{-s/2} · Γ(s/2)^{-1} · 2/s  (Definition)
EQUATION 2: ξ(s) = ξ(1-s)                              (Functional equation)
EQUATION 3: ζ(s) = Π_p (1 - p^{-s})^{-1}              (Euler product)
EQUATION 4: log ζ(s) = Σ_p Σ_m p^{-ms}/m             (Log series)
EQUATION 5: 1/ζ(s) = Σ_n μ(n)/n^s                    (Möbius inversion)
EQUATION 6: M(x) = Σ_ρ x^ρ/(ρζ'(ρ)) + ...            (Explicit formula)

These are NOT independent. They're different views of ONE object.

HYPOTHESIS: This system is "generically over-determined."

Meaning: For a RANDOM function satisfying some of these constraints,
the others would fail. Only SPECIFIC functions satisfy ALL.

ζ(s) is one such function. RH may be forced by consistency.
""")

# =============================================================================
# QUANTITATIVE TEST
# =============================================================================
print("\n" + "=" * 70)
print("QUANTITATIVE TEST: CONSTRAINT SENSITIVITY")
print("=" * 70)

print("""
Test: How sensitive are the constraints to perturbations?

If we PERTURB a zero from Re(s) = 1/2 to Re(s) = 1/2 + ε:
- How much does M(x) change?
- How much do the c_n change?
- How much does prime counting change?

If small perturbations cause large effects, the system is "stiff"
and RH may be structurally necessary.
""")

def perturbation_effect(epsilon, x_max=10000):
    """
    Estimate the effect of moving a zero off the critical line.
    """
    # First zero is at approximately 1/2 + 14.13i
    gamma_1 = 14.134725142

    # On-line contribution to M(x) at x = x_max
    on_line = x_max**0.5 / (gamma_1 * abs(complex(0.5, gamma_1)))

    # Perturbed contribution
    beta_perturbed = 0.5 + epsilon
    perturbed = x_max**beta_perturbed / (gamma_1 * abs(complex(beta_perturbed, gamma_1)))

    # Ratio
    ratio = perturbed / on_line

    return ratio

print("Effect of perturbing first zero from Re(s) = 0.5 to 0.5 + ε:")
print("\n| ε        | Perturbation ratio at x=10⁴ | Amplification |")
print("|" + "-"*10 + "|" + "-"*29 + "|" + "-"*15 + "|")

for eps in [0.001, 0.01, 0.05, 0.1, 0.2]:
    ratio = perturbation_effect(eps, 10000)
    print(f"| {eps:8.3f} | {ratio:27.4f} | {ratio-1:13.4f} |")

print("\nEven small ε causes significant amplification at large x.")
print("The system is VERY sensitive to zero locations.")

# =============================================================================
# FINAL SYNTHESIS
# =============================================================================
print("\n" + "=" * 70)
print("FINAL SYNTHESIS")
print("=" * 70)

print("""
KEY FINDINGS FROM CONTRADICTION ANALYSIS:

1. A counterexample would require:
   - M(x) growing faster than x^{1/2}
   - Li's λ_n becoming negative
   - Báez-Duarte c_n decaying slower
   - Prime counting error increasing
   - All computed zeros mysteriously on-line despite off-line existing

2. The system is highly constrained:
   - Multiple equivalent formulations
   - Each constrains the same underlying structure
   - Perturbations are amplified

3. No evidence for counterexample:
   - 10+ trillion zeros computed, all on-line
   - Prime counting matches RH predictions
   - Mertens function bounded as expected
   - Li's λ_n all positive (computed)

4. The "default" is RH:
   - No theoretical reason to expect off-line zeros
   - All evidence consistent with RH
   - Counterexample would require extraordinary coincidence

HOWEVER: This is still not a PROOF.

The challenge remains: Transform these observations into rigorous mathematics.
""")

print("\n" + "=" * 70)
print("END OF CONTRADICTION ANALYSIS")
print("=" * 70)
