#!/usr/bin/env python3
"""
DEMONSTRATION OF THE LOGICAL GAP IN THE VARIATIONAL "PROOF"

This script shows CONCRETELY why the variational argument doesn't prove RH.
"""

import numpy as np

print("="*70)
print("DEMONSTRATION: WHY THE VARIATIONAL ARGUMENT ISN'T A PROOF")
print("="*70)

# First few Riemann zeros (imaginary parts)
true_zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]

print("\n" + "="*70)
print("PART 1: What We Actually Proved")
print("="*70)

print("""
We proved that E_pair(σ) = E_n(σ) + E_n(1-σ) is:
  1. Convex in σ
  2. Symmetric: E_pair(σ) = E_pair(1-σ)
  3. Therefore minimized at σ = 1/2

This is MATHEMATICALLY CORRECT. Let's verify:
""")

def E_single(sigma, gamma, x=10.0):
    """Single zero contribution to error (simplified form)"""
    return x**(2*sigma) / (sigma**2 + gamma**2)

def E_pair(sigma, gamma, x=10.0):
    """Pair contribution: E(σ) + E(1-σ)"""
    return E_single(sigma, gamma, x) + E_single(1-sigma, gamma, x)

# Verify minimum at σ = 1/2
print("For γ = 14.134725 (first zero):")
for sigma in [0.3, 0.4, 0.5, 0.6, 0.7]:
    E = E_pair(sigma, 14.134725)
    print(f"  E_pair({sigma}) = {E:.6f}")

# Find numerical minimum
sigmas = np.linspace(0.001, 0.999, 1000)
Es = [E_pair(s, 14.134725) for s in sigmas]
min_idx = np.argmin(Es)
print(f"\nMinimum at σ = {sigmas[min_idx]:.4f}")
print("\n✓ CONFIRMED: Minimum is at σ = 1/2")

print("\n" + "="*70)
print("PART 2: The Logical Gap")
print("="*70)

print("""
HERE'S THE PROBLEM:

We showed: "E_pair(σ) is minimized at σ = 1/2"

We CLAIMED: "Therefore zeros MUST have σ = 1/2"

BUT these are DIFFERENT statements!

The zeros of ζ(s) are FIXED. They're wherever ζ(s) = 0.
They don't "choose" to minimize E_pair.

ANALOGY:
  - "The center of a room minimizes distance to all walls"
  - "Therefore all objects MUST be in the center"

  These don't follow. Objects are wherever someone put them.
""")

print("\n" + "="*70)
print("PART 3: The Explicit Formula Tautology")
print("="*70)

print("""
KEY INSIGHT: E = 0 for true zeros is TAUTOLOGICAL.

The explicit formula:
  ψ(x) = x - Σ_ρ x^ρ/ρ - log(2π) - ½log(1-x⁻²)

This is EXACT (for x not a prime power). It's not an approximation.

So E = 0 for true zeros BY DEFINITION, not because σ = 1/2.

If RH were FALSE and some zero had σ = 0.7:
  - The explicit formula would still include that zero
  - The formula would still be exact
  - E would still be 0

The variational minimum at σ = 1/2 is IRRELEVANT to where zeros actually are.
""")

print("\n" + "="*70)
print("PART 4: Concrete Counterexample Scenario")
print("="*70)

print("""
THOUGHT EXPERIMENT:

Suppose (counterfactually) that RH is false, and there exists a zero at:
  ρ = 0.6 + 100i

What would our "proof" say?

1. E = 0 for this zero (explicit formula is exact) ✓
2. E_pair(σ) for this zero would be:
   E(0.6) + E(0.4) with γ = 100

Let's compute:
""")

# Hypothetical off-line zero
gamma_hypothetical = 100.0
sigma_hypothetical = 0.6

print(f"Hypothetical zero at σ = {sigma_hypothetical}, γ = {gamma_hypothetical}")
print(f"\nE_pair values:")
for sigma in [0.3, 0.4, 0.5, 0.6, 0.7]:
    E = E_pair(sigma, gamma_hypothetical)
    print(f"  E_pair({sigma}) = {E:.6f}")

# Find minimum
Es = [E_pair(s, gamma_hypothetical) for s in sigmas]
min_idx = np.argmin(Es)
print(f"\nMinimum of E_pair still at σ = {sigmas[min_idx]:.4f}")

print("""
The minimum is STILL at σ = 1/2!

But the hypothetical zero is at σ = 0.6.

This shows: The location of E_pair's minimum tells us NOTHING about
where the actual zeros are.

The zero exists wherever ζ(s) = 0, independent of E_pair.
""")

print("\n" + "="*70)
print("PART 5: The Core Confusion")
print("="*70)

print("""
THE PROOF CONFUSES TWO DIFFERENT THINGS:

1. "The optimal σ for minimizing E_pair is σ = 1/2"
   This is a statement about a FUNCTION we constructed.

2. "The zeros of ζ(s) have σ = 1/2"
   This is a statement about where ζ(s) ACTUALLY vanishes.

These are COMPLETELY INDEPENDENT statements.

Our variational analysis proves (1) but NOT (2).

To prove (2), we would need to show that zeros of ζ(s) are somehow
CONSTRAINED to minimize E_pair. We have not shown this.
""")

print("\n" + "="*70)
print("PART 6: What Would Actually Work")
print("="*70)

print("""
TO MAKE THIS A REAL PROOF, we would need:

Option A: Show that ζ(s) = 0 ⟺ δF/δs = 0 for some functional F
          AND that F only has critical points at σ = 1/2.
          (Hilbert-Pólya approach - unsolved)

Option B: Show that OFF-LINE zeros would create a contradiction
          in the explicit formula convergence.

Option C: Show that OFF-LINE zeros would violate the functional equation
          in some subtle way we haven't captured.

Our current argument does NONE of these.
""")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)

print("""
STATUS: NOT A VALID PROOF

The variational argument shows σ = 1/2 is "optimal" for the error
functional, but this doesn't FORCE zeros to be there.

RECOMMENDATION:
  - Publish as "heuristic" or "perspective", not "proof"
  - Acknowledge the gap explicitly
  - Frame as a conjecture that could lead to progress

HONEST PROBABILITY ASSESSMENT:
  - Valid proof: < 0.1%
  - Valuable perspective: Yes
  - Could lead to progress: ~10-20%
""")

print("\n" + "="*70)
print("END OF DEMONSTRATION")
print("="*70)
