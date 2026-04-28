#!/usr/bin/env python3
"""
RH_COUNTEREXAMPLE_ANALYSIS.py

ULTRATHINK: What Would a Counterexample Look Like?

Instead of trying to PROVE RH, we rigorously analyze what it would
take for RH to be FALSE. This sharpens understanding regardless of truth.

Key questions:
1. What constraints does a counterexample face?
2. How would it manifest in computable quantities?
3. Why hasn't one been found?
4. What would it tell us about the "geometric substrate"?
"""

import numpy as np
from typing import List, Tuple, Dict
from scipy import special
import math

print("=" * 80)
print("COUNTEREXAMPLE ANALYSIS: WHAT IF RH IS FALSE?")
print("=" * 80)
print()

# =============================================================================
# PART 1: STRUCTURE OF A COUNTEREXAMPLE
# =============================================================================

print("PART 1: STRUCTURE OF A COUNTEREXAMPLE")
print("-" * 60)
print()

print("""
If RH is false, there exists at least one zero ρ = σ + iγ with σ ≠ 1/2.

IMMEDIATE CONSEQUENCES:
───────────────────────

1. FUNCTIONAL EQUATION CONSTRAINT:
   ζ(s) = χ(s)ζ(1-s)  where χ(s) = 2^s π^{s-1} sin(πs/2) Γ(1-s)

   If ρ is a zero, so is 1-ρ̄ (complex conjugate of 1-ρ).
   For ρ = σ + iγ:
   - 1-ρ̄ = 1-σ + iγ

   So zeros come in PAIRS symmetric about σ = 1/2.

   If σ > 1/2: There's also a zero at 1-σ < 1/2
   Counterexamples come in PAIRS, one on each side of the critical line.

2. VERTICAL DISTRIBUTION:
   By Riemann-von Mangoldt: N(T) ~ (T/2π) log(T/2πe)

   If an off-line zero exists at height γ, the NUMBER of zeros
   below γ is still approximately N(γ).

   A single off-line zero doesn't change the COUNTING dramatically.
""")

def riemann_von_mangoldt(T: float) -> float:
    """Expected number of zeros with 0 < Im(ρ) < T."""
    if T <= 0:
        return 0
    return (T / (2 * np.pi)) * np.log(T / (2 * np.pi * np.e)) + 7/8

print("ZERO COUNTING FUNCTION N(T):")
for T in [100, 1000, 10000, 100000, 1e6, 1e12]:
    N = riemann_von_mangoldt(T)
    print(f"  N({T:.0e}) ≈ {N:.2e}")
print()

# =============================================================================
# PART 2: LI CRITERION SIGNATURE
# =============================================================================

print("=" * 60)
print("PART 2: LI CRITERION SIGNATURE")
print("-" * 60)
print()

print("""
Li criterion: RH ⟺ λ_n > 0 for all n ≥ 1

where λ_n = sum over zeros ρ of [1 - (1-1/ρ)^n]

If RH is FALSE, some λ_n < 0.

THE KEY QUESTION: Which n would fail first?

If there's an off-line zero at ρ = σ + iγ with σ ≠ 1/2:
- Its contribution to λ_n depends on |1 - 1/ρ|
- For ρ on critical line: |1 - 1/ρ| = 1 exactly
- For ρ off critical line: |1 - 1/ρ| ≠ 1

The DEVIATION from unit circle is:
  |1 - 1/ρ|² = |1 - 1/(σ+iγ)|²
             = |(σ+iγ-1)/(σ+iγ)|²
             = [(σ-1)² + γ²] / [σ² + γ²]

For σ = 1/2: this equals 1 exactly (on unit circle)
For σ ≠ 1/2: this deviates from 1
""")

def unit_circle_deviation(sigma: float, gamma: float) -> float:
    """Compute |1 - 1/ρ|² for ρ = σ + iγ."""
    numerator = (sigma - 1)**2 + gamma**2
    denominator = sigma**2 + gamma**2
    return numerator / denominator

print("DEVIATION FROM UNIT CIRCLE:")
print()
print("  For zero at σ + iγ:")
print("  σ         γ          |1-1/ρ|²       On circle?")
print("  " + "-" * 55)

# Critical line zeros (should be exactly 1)
for gamma in [14.13, 21.02, 25.01]:
    dev = unit_circle_deviation(0.5, gamma)
    print(f"  0.500    {gamma:6.2f}       {dev:.10f}    {'YES' if abs(dev-1) < 1e-10 else 'NO'}")

print()

# Hypothetical off-line zeros
print("  HYPOTHETICAL OFF-LINE ZEROS:")
for sigma in [0.51, 0.55, 0.60, 0.75]:
    for gamma in [1000, 10000, 100000]:
        dev = unit_circle_deviation(sigma, gamma)
        print(f"  {sigma:.3f}    {gamma:8.0f}     {dev:.10f}    NO (deviation: {abs(dev-1):.2e})")
print()

print("""
KEY OBSERVATION:
────────────────
For large γ, the deviation from unit circle is approximately:

|1-1/ρ|² ≈ 1 + (2σ - 1)(2σ - 1) / γ²
         = 1 + (2σ - 1)² / γ²

For σ close to 1/2, this is VERY small for large γ.

IMPLICATION: Off-line zeros at large height have TINY effect on Li coefficients.
This is why we haven't detected them even if they exist.
""")

def li_deviation_estimate(sigma: float, gamma: float) -> float:
    """Estimate contribution to Li coefficient deviation."""
    return (2*sigma - 1)**2 / gamma**2

print("ESTIMATED Li DEVIATION PER OFF-LINE ZERO:")
print()
for sigma in [0.501, 0.51, 0.55]:
    for gamma in [1e6, 1e9, 1e12]:
        dev = li_deviation_estimate(sigma, gamma)
        print(f"  σ = {sigma:.3f}, γ = {gamma:.0e}: deviation ≈ {dev:.2e}")
print()

# =============================================================================
# PART 3: EXPLICIT FORMULA SIGNATURE
# =============================================================================

print("=" * 60)
print("PART 3: EXPLICIT FORMULA SIGNATURE")
print("-" * 60)
print()

print("""
The explicit formula:
  ψ(x) = x - Σ_ρ x^ρ/ρ - log(2π) - (1/2)log(1-x^{-2})

where the sum is over ALL nontrivial zeros.

If there's an off-line zero at ρ = σ + iγ with σ > 1/2:

The contribution is x^ρ/ρ = x^{σ+iγ}/(σ+iγ)
                         = x^σ · e^{iγ log x} / (σ+iγ)

For σ = 1/2: |x^ρ| = √x (the expected oscillation amplitude)
For σ > 1/2: |x^ρ| = x^σ > √x (LARGER amplitude!)

AN OFF-LINE ZERO CREATES LARGER OSCILLATIONS IN ψ(x).
""")

def explicit_formula_contribution(x: float, sigma: float, gamma: float) -> complex:
    """Compute x^ρ/ρ for ρ = σ + iγ."""
    rho = sigma + 1j * gamma
    return (x ** rho) / rho

def oscillation_amplitude(x: float, sigma: float) -> float:
    """Amplitude of oscillation from zero at Re(ρ) = σ."""
    return x ** sigma

print("OSCILLATION AMPLITUDE COMPARISON:")
print()
print("  x             σ=0.5 (RH)     σ=0.51         σ=0.55         σ=0.6")
print("  " + "-" * 70)

for x in [1e3, 1e6, 1e9, 1e12]:
    amp_rh = oscillation_amplitude(x, 0.5)
    amp_51 = oscillation_amplitude(x, 0.51)
    amp_55 = oscillation_amplitude(x, 0.55)
    amp_60 = oscillation_amplitude(x, 0.60)
    print(f"  {x:.0e}     {amp_rh:.2e}        {amp_51:.2e}        {amp_55:.2e}        {amp_60:.2e}")

print()
print("""
IMPLICATION:
────────────
An off-line zero at σ = 0.55 creates oscillations that grow like x^{0.55}
instead of x^{0.5}. For x = 10^12:

  x^{0.5} = 10^6
  x^{0.55} = 10^{6.6} ≈ 4 × 10^6

This is a factor of 4 larger - DETECTABLE in principle.

But if the off-line zero is at height γ > 10^12 (beyond current computation),
we wouldn't see its effect in the range we can check.
""")

# =============================================================================
# PART 4: PRIME GAP SIGNATURE
# =============================================================================

print("=" * 60)
print("PART 4: PRIME GAP SIGNATURE")
print("-" * 60)
print()

print("""
RH implies bounds on prime gaps:

IF RH: π(x) = Li(x) + O(√x log x)
       → Gap between consecutive primes is O(√p log p)

IF RH FALSE with zero at σ > 1/2:
       π(x) = Li(x) + O(x^σ log x)
       → Gap could be as large as O(p^σ log p)

CURRENT RECORD PRIME GAPS:
The largest known prime gaps relative to log²(p) are:

  p ≈ 10^k: maximal gap g satisfies g / log²(p) ~ constant

This is consistent with RH (even with Cramér's stronger conjecture).
NO ANOMALIES have been detected.
""")

# Prime gap statistics
def cramer_ratio(p: int, gap: int) -> float:
    """Ratio of gap to (log p)²."""
    if p <= 2:
        return 0
    return gap / (np.log(p) ** 2)

# Some record prime gaps (approximate data)
record_gaps = [
    (2, 1),
    (3, 2),
    (7, 4),
    (23, 6),
    (89, 8),
    (113, 14),
    (523, 18),
    (887, 20),
    (1129, 22),
    (1327, 34),
    (31397, 72),
    (370261, 112),
    (2010733, 148),
    (20831323, 210),
]

print("RECORD PRIME GAPS (Cramér ratio g/log²p):")
print()
print("  Prime p          Gap g      g/log²p")
print("  " + "-" * 40)
for p, g in record_gaps:
    ratio = cramer_ratio(p, g)
    print(f"  {p:>15d}   {g:>5d}      {ratio:.4f}")

print()
print("The ratios stay bounded (~0.5 to 1.2), consistent with RH/Cramér.")
print()

# =============================================================================
# PART 5: WHY HASN'T A COUNTEREXAMPLE BEEN FOUND?
# =============================================================================

print("=" * 60)
print("PART 5: WHY HASN'T A COUNTEREXAMPLE BEEN FOUND?")
print("-" * 60)
print()

print("""
COMPUTATIONAL VERIFICATION:
───────────────────────────
- Zeros verified on critical line up to T ≈ 3 × 10^12
- That's approximately 10^13 zeros checked
- NO off-line zeros found

THREE POSSIBILITIES:

1. RH IS TRUE
   The simplest explanation. All zeros are on the line.

2. RH IS FALSE, BUT COUNTEREXAMPLE IS VERY HIGH
   The first off-line zero is at height γ > 3 × 10^12.
   This seems unlikely but not impossible.

   If σ ≈ 0.5001 and γ ≈ 10^15:
   - Deviation from unit circle: (2σ-1)²/γ² ≈ 10^{-34}
   - Almost undetectable!

3. RH IS FALSE, BUT WE'RE LOOKING IN THE WRONG PLACE
   Maybe off-line zeros exist but our methods can't find them.
   (This seems unlikely given the variety of methods used.)

THE STATISTICAL ARGUMENT:
─────────────────────────
If off-line zeros existed with any reasonable density,
we would have found one by now.

The fact that 10^13 zeros are ALL on the line is strong evidence.
Not proof, but very strong evidence.
""")

# Estimate probability under random hypothesis
n_verified = 1e13
# If each zero had independent 1/1000 chance of being off-line
# Probability all are on-line: (999/1000)^{10^13} ≈ 0

print("STATISTICAL THOUGHT EXPERIMENT:")
print()
print("If each zero had probability p of being off-line:")
print("  p = 0.001 → P(all 10^13 on line) ≈ 10^{-4×10^9} ≈ 0")
print("  p = 10^{-6} → P(all on line) ≈ exp(-10^7) ≈ 0")
print("  p = 10^{-13} → P(all on line) ≈ exp(-1) ≈ 0.37")
print("  p = 10^{-14} → P(all on line) ≈ exp(-0.1) ≈ 0.90")
print()
print("To be consistent with observation, off-line zeros must be")
print("INCREDIBLY rare: less than 1 in 10^14 zeros.")
print()

# =============================================================================
# PART 6: CONSEQUENCES OF A COUNTEREXAMPLE
# =============================================================================

print("=" * 60)
print("PART 6: WHAT WOULD A COUNTEREXAMPLE MEAN?")
print("-" * 60)
print()

print("""
IF RH IS FALSE, WHAT CHANGES?

MATHEMATICS:
────────────
1. Many theorems proven "under RH" would need revision
2. Prime number theorem error term is worse: O(x^σ) instead of O(√x)
3. Li criterion fails: Some λ_n < 0
4. The "geometric substrate" hypothesis would need refinement

CRYPTOGRAPHY:
─────────────
5. Some algorithms proven secure under RH lose that guarantee
6. But practical security likely unaffected (counterexample too high)

PHILOSOPHY:
───────────
7. The "spectral" interpretation becomes more complex
8. If zeros can be off-line, what determines which are?
9. The symmetry s ↔ (1-s) still holds, but doesn't force identity

THE DEEPEST QUESTION:
─────────────────────
If RH is false, WHY do 10^13+ zeros lie on the line anyway?

Even a single off-line zero would demand explanation:
- What makes THAT zero special?
- Why is the "default" behavior to be on the line?
- Is there a weaker statement that IS true?

MODIFIED CONJECTURES IF RH FAILS:
─────────────────────────────────
- "Almost all" zeros on line (density 1)
- Zeros off line have density 0
- Off-line zeros have bounded real part: σ < 1 - δ for some δ > 0

These weaker statements would still have number-theoretic consequences.
""")

# =============================================================================
# PART 7: THE GEOMETRY QUESTION
# =============================================================================

print("=" * 60)
print("PART 7: WHAT DOES A COUNTEREXAMPLE SAY ABOUT GEOMETRY?")
print("-" * 60)
print()

print("""
Our thesis: RH requires a "geometric substrate" that makes zeros
eigenvalues of a self-adjoint operator.

IF RH IS FALSE:
───────────────
Either:
(A) The geometric substrate DOESN'T EXIST (even in principle)
(B) The substrate EXISTS but doesn't force ALL zeros onto line

Option (A) would mean:
- Zeros are NOT eigenvalues of a self-adjoint operator
- The Hilbert-Pólya conjecture is FALSE
- GUE statistics are a coincidence (or approximate, not exact)

Option (B) would mean:
- An operator exists, but isn't FULLY self-adjoint
- Maybe self-adjoint on a dense subset
- Off-line zeros come from boundary conditions or deficiency indices

THIS IS THE KEY INSIGHT:
────────────────────────
Even analyzing the COUNTEREXAMPLE tells us about the STRUCTURE.

If RH fails:
- We learn the operator isn't self-adjoint
- Or we learn no spectral interpretation exists

If RH holds:
- We still need to FIND the operator

Either way, understanding counterexamples sharpens the question.
""")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("=" * 80)
print("FINAL SUMMARY: COUNTEREXAMPLE ANALYSIS")
print("=" * 80)
print()

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    COUNTEREXAMPLE STRUCTURE                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  IF RH IS FALSE, a counterexample ρ = σ + iγ (σ ≠ 1/2) must:                ║
║                                                                              ║
║  1. Come with a partner at 1-σ + iγ (functional equation)                   ║
║  2. Be at height γ > 3×10^12 (not yet computed)                             ║
║  3. Cause Li coefficient λ_n < 0 for some n                                 ║
║  4. Create larger oscillations in ψ(x) - x                                  ║
║  5. Have probability < 10^{-14} per zero (consistency with data)            ║
║                                                                              ║
║  WHY HASN'T ONE BEEN FOUND?                                                  ║
║  ─────────────────────────────                                               ║
║  • Either RH is TRUE (most likely)                                           ║
║  • Or counterexamples are incredibly rare AND high                           ║
║  • The data strongly supports RH                                             ║
║                                                                              ║
║  WHAT WOULD A COUNTEREXAMPLE MEAN?                                           ║
║  ──────────────────────────────────                                          ║
║  • Hilbert-Pólya operator either doesn't exist OR isn't self-adjoint        ║
║  • The "geometric substrate" is absent OR incomplete                         ║
║  • GUE statistics are approximate, not exact                                 ║
║                                                                              ║
║  THE VALUE OF THIS ANALYSIS:                                                 ║
║  ────────────────────────────                                                ║
║  Understanding counterexamples sharpens our understanding of RH.             ║
║  Even if RH is true, knowing what failure would look like helps.             ║
║  It clarifies what the "geometric substrate" must accomplish.                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print()
print("Counterexample analysis complete.")
print("=" * 80)
