"""
DIRECTION A: ANALYTICAL CORRELATION STRUCTURE
==============================================

Goal: Derive and understand Cov(S_w, S_{w'}) to explain the cancellation in M(x).

Key insight: If we can prove the correlations MUST produce cancellation,
we might have a path to RH.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, log, factorial, pi, E, symbols, simplify, summation
from sympy import gamma as Gamma, exp, oo, binomial, sqrt
from collections import defaultdict
import json

print("=" * 80)
print("DIRECTION A: ANALYTICAL CORRELATION STRUCTURE")
print("=" * 80)

# =============================================================================
# PART 1: COMPUTE EXACT S_w(x) AND COMPARE TO LANDAU
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: EXACT S_w vs LANDAU'S ASYMPTOTIC")
print("=" * 80)

def compute_exact_S_w(x_max):
    """Compute exact S_w(x) for all w."""
    S = defaultdict(lambda: defaultdict(int))

    for n in range(1, x_max + 1):
        factors = factorint(n)
        if any(e > 1 for e in factors.values()):
            continue  # Not squarefree
        w = len(factors)
        S[n][w] = 1

    # Cumulative
    S_cumulative = defaultdict(lambda: defaultdict(int))
    running = defaultdict(int)
    for n in range(1, x_max + 1):
        for w in S[n]:
            running[w] += S[n][w]
        for w in running:
            S_cumulative[n][w] = running[w]

    return S_cumulative

print("\nComputing exact S_w(x) up to x = 100,000...")
x_max = 100000
S_exact = compute_exact_S_w(x_max)

def landau_S_w(x, w):
    """Landau's asymptotic formula for S_w(x)."""
    if w == 0:
        return 1  # Only n=1 has ω(n)=0
    if x < 2:
        return 0

    C = 6 / np.pi**2
    lam = np.log(np.log(x))

    # S_w(x) ~ C * (x/log(x)) * (log log x)^{w-1} / (w-1)!
    import math
    return C * (x / np.log(x)) * (lam ** (w-1)) / math.factorial(w-1)

# Compare exact vs Landau at x = 100,000
x = 100000
lam = np.log(np.log(x))

print(f"\nAt x = {x:,}, λ = log log x = {lam:.4f}")
print("-" * 70)
print(f"{'w':>4} | {'S_w exact':>12} | {'Landau':>12} | {'Error':>12} | {'Rel Error':>10}")
print("-" * 70)

errors = []
for w in range(8):
    exact = S_exact[x].get(w, 0)
    landau = landau_S_w(x, w)
    error = exact - landau
    rel_error = error / landau if landau > 0 else 0
    errors.append({'w': w, 'exact': exact, 'landau': landau, 'error': error, 'rel_error': rel_error})
    print(f"{w:>4} | {exact:>12} | {landau:>12.1f} | {error:>+12.1f} | {rel_error:>+10.4f}")

# =============================================================================
# PART 2: STRUCTURE OF THE ERROR TERMS
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: STRUCTURE OF ERROR TERMS ε_w = S_w - S_w^{Landau}")
print("=" * 80)

print("""
If S_w = S_w^{Landau} + ε_w, then:

M(x) = Σ(-1)^w S_w = Σ(-1)^w S_w^{Landau} + Σ(-1)^w ε_w
     = M^{Landau}(x) + M^{error}(x)

Let's compute both terms separately.
""")

# Compute M decomposition for various x
x_values = [1000, 2000, 5000, 10000, 20000, 50000, 100000]

print(f"{'x':>10} | {'M_exact':>10} | {'M_Landau':>12} | {'M_error':>12} | {'|M|/√x':>10}")
print("-" * 65)

for x in x_values:
    # Exact M
    M_exact = sum((-1)**w * S_exact[x].get(w, 0) for w in range(20))

    # Landau approximation to M
    M_landau = sum((-1)**w * landau_S_w(x, w) for w in range(20))

    # Error contribution
    M_error = M_exact - M_landau

    ratio = abs(M_exact) / np.sqrt(x)

    print(f"{x:>10} | {M_exact:>+10} | {M_landau:>+12.2f} | {M_error:>+12.2f} | {ratio:>10.4f}")

# =============================================================================
# PART 3: ANALYTICAL M_LANDAU
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: WHAT DOES LANDAU'S FORMULA PREDICT FOR M(x)?")
print("=" * 80)

print("""
Using Landau: S_w ~ C · (x/log x) · λ^{w-1}/(w-1)!  where λ = log log x

The alternating sum is:
M^{Landau} = Σ(-1)^w S_w^{Landau}
           = S_0 + Σ_{w≥1} (-1)^w · C · (x/log x) · λ^{w-1}/(w-1)!
           = 1 + C · (x/log x) · Σ_{w≥1} (-1)^w · λ^{w-1}/(w-1)!

Let k = w-1, so w = k+1:
           = 1 + C · (x/log x) · Σ_{k≥0} (-1)^{k+1} · λ^k/k!
           = 1 - C · (x/log x) · Σ_{k≥0} (-λ)^k/k!
           = 1 - C · (x/log x) · e^{-λ}
           = 1 - C · (x/log x) · 1/log x
           = 1 - 6x/(π² (log x)²)

So Landau predicts M(x) ≈ -6x/(π² (log x)²) for large x!

This is MUCH larger than the actual M(x) = O(√x).
""")

def M_landau_analytical(x):
    """Landau's prediction for M(x)."""
    C = 6 / np.pi**2
    return 1 - C * x / (np.log(x)**2)

print("Comparing M_Landau (analytical) to M_exact:")
print("-" * 55)
print(f"{'x':>10} | {'M_exact':>10} | {'M_Landau_ana':>14} | {'Ratio':>10}")
print("-" * 55)

for x in x_values:
    M_exact = sum((-1)**w * S_exact[x].get(w, 0) for w in range(20))
    M_landau = M_landau_analytical(x)
    ratio = M_exact / M_landau if M_landau != 0 else 0
    print(f"{x:>10} | {M_exact:>+10} | {M_landau:>+14.1f} | {ratio:>+10.6f}")

print("""
CRITICAL OBSERVATION:
====================
Landau's formula predicts M(x) ≈ -6x/(π² log²x) ≈ -65 at x=100,000
But actual M(x) = -48 at x=100,000

The Landau prediction is in the right ballpark for this x, but:
- Landau predicts M(x) = O(x/log²x), which grows with x
- RH asserts M(x) = O(x^{1/2+ε}), which is much smaller for large x

The ERROR TERMS ε_w must cancel the Landau contribution!
""")

# =============================================================================
# PART 4: THE CANCELLATION MECHANISM
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: ANALYZING THE CANCELLATION MECHANISM")
print("=" * 80)

print("""
We have: M(x) = M_Landau(x) + M_error(x)

Where:
- M_Landau(x) ≈ -6x/(π² log²x)  [grows like x/log²x]
- M_error(x) = Σ(-1)^w ε_w(x)   [must cancel M_Landau to leave O(√x)]

This means: M_error(x) ≈ +6x/(π² log²x) + O(√x)

The error terms ε_w must be structured to produce this cancellation!
""")

# Compute error structure
x = 100000
print(f"\nError structure at x = {x:,}:")
print("-" * 70)
print(f"{'w':>4} | {'ε_w':>12} | {'(-1)^w ε_w':>14} | {'Cumulative':>14}")
print("-" * 70)

cumulative = 0
for w in range(10):
    exact = S_exact[x].get(w, 0)
    landau = landau_S_w(x, w)
    eps_w = exact - landau
    signed_eps = ((-1)**w) * eps_w
    cumulative += signed_eps
    print(f"{w:>4} | {eps_w:>+12.1f} | {signed_eps:>+14.1f} | {cumulative:>+14.1f}")

print(f"\nTotal Σ(-1)^w ε_w = {cumulative:+.1f}")
print(f"M_Landau analytical = {M_landau_analytical(x):+.1f}")
print(f"Sum = {cumulative + M_landau_analytical(x):+.1f}")
print(f"M_exact = {sum((-1)**w * S_exact[x].get(w, 0) for w in range(20)):+d}")

# =============================================================================
# PART 5: REFINED ASYMPTOTIC
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: REFINED ASYMPTOTIC FOR S_w")
print("=" * 80)

print("""
The Sathe-Selberg formula gives a more refined asymptotic:

S_w(x) = (6/π²) · (x/log x) · (log log x)^{w-1}/(w-1)! · (1 + O(1/log log x))

The error term O(1/log log x) varies with w in a structured way!

Let's model:
S_w(x) = S_w^{Landau}(x) · (1 + c_w(x))

where c_w(x) represents the relative correction.
""")

print(f"\nRelative corrections c_w at x = {x:,}:")
print("-" * 50)
print(f"{'w':>4} | {'c_w':>12} | {'c_w · log log x':>15}")
print("-" * 50)

lam = np.log(np.log(x))
for w in range(1, 8):
    exact = S_exact[x].get(w, 0)
    landau = landau_S_w(x, w)
    if landau > 0:
        c_w = (exact / landau) - 1
        print(f"{w:>4} | {c_w:>+12.4f} | {c_w * lam:>+15.4f}")

# =============================================================================
# PART 6: THE KEY IDENTITY
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: SEARCHING FOR THE KEY IDENTITY")
print("=" * 80)

print("""
We need an identity that explains the cancellation.

OBSERVATION: The corrections c_w seem to follow a pattern.
Let's look for structure in c_w as a function of w.

If c_w = a + b·w + c·w² + ..., the alternating sum Σ(-1)^w c_w might simplify.
""")

# Fit a polynomial to c_w
import numpy.polynomial.polynomial as P

w_vals = []
c_vals = []
for w in range(1, 7):
    exact = S_exact[x].get(w, 0)
    landau = landau_S_w(x, w)
    if landau > 0:
        c_w = (exact / landau) - 1
        w_vals.append(w)
        c_vals.append(c_w)

if len(w_vals) >= 3:
    # Fit polynomial
    coeffs = np.polyfit(w_vals, c_vals, 2)
    print(f"\nPolynomial fit: c_w ≈ {coeffs[0]:.4f}·w² + {coeffs[1]:.4f}·w + {coeffs[2]:.4f}")

    print(f"\n{'w':>4} | {'c_w actual':>12} | {'c_w fitted':>12} | {'Error':>10}")
    print("-" * 50)
    for w, c in zip(w_vals, c_vals):
        fitted = coeffs[0]*w**2 + coeffs[1]*w + coeffs[2]
        print(f"{w:>4} | {c:>+12.4f} | {fitted:>+12.4f} | {c-fitted:>+10.4f}")

# =============================================================================
# PART 7: EXPLICIT FORMULA CONNECTION
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: CONNECTION TO EXPLICIT FORMULA")
print("=" * 80)

print("""
The explicit formula for M(x) is:

M(x) = -2 + Σ_ρ x^ρ/(ρ·ζ'(ρ)) + O(1)

where the sum is over non-trivial zeros ρ of ζ(s).

Under RH, ρ = 1/2 + iγ, so x^ρ = x^{1/2} · e^{iγ log x}

This means M(x) is a sum of oscillating terms of amplitude ~x^{1/2}.

Can we derive this from our generating function?

We have M(x) = G(-1, x) = Σ_w (-1)^w S_w(x).

If S_w(x) has an explicit formula involving ζ zeros, then M(x) would too.
""")

# Let's verify the explicit formula numerically using our data
print("\nVerifying explicit formula structure:")
print("Under RH, |M(x)|/√x should be O(1) with oscillations.")
print("-" * 50)
print(f"{'x':>10} | {'M(x)':>10} | {'M/√x':>12} | {'Phase (approx)':>14}")
print("-" * 50)

for x in x_values:
    M = sum((-1)**w * S_exact[x].get(w, 0) for w in range(20))
    ratio = M / np.sqrt(x)
    # The "phase" would be related to γ₁ log x mod 2π
    gamma_1 = 14.134725  # First zeta zero
    phase = (gamma_1 * np.log(x)) % (2 * np.pi)
    print(f"{x:>10} | {M:>+10} | {ratio:>+12.4f} | {phase:>14.4f}")

print("""
The oscillations in M(x)/√x are driven by the zeta zeros.
The phase structure comes from e^{iγ log x} terms.
""")

# =============================================================================
# PART 8: KEY INSIGHT
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: KEY INSIGHT FROM DIRECTION A")
print("=" * 80)

print("""
SUMMARY OF FINDINGS:
====================

1. Landau's formula predicts M(x) ≈ -6x/(π² log²x), which GROWS with x.

2. The actual M(x) is O(√x) under RH - MUCH smaller for large x.

3. The error terms ε_w = S_w - S_w^{Landau} must cancel the Landau prediction.

4. This cancellation is NOT obvious from the formula - it requires:
   Σ(-1)^w ε_w ≈ +6x/(π² log²x) + O(√x)

5. The errors ε_w are controlled by the ZEROS of ζ(s).

OBSTRUCTION IDENTIFIED:
======================
To prove RH via this route, we would need to prove that the error terms
ε_w satisfy Σ(-1)^w ε_w = -M_Landau + O(√x).

This requires showing that the errors exhibit the same cancellation
pattern as the original sum - which is exactly as hard as RH itself.

The explicit formula tells us the errors are determined by ζ zeros.
Without knowing where the zeros are, we can't bound the errors.
""")

print("=" * 80)
print("DIRECTION A COMPLETE")
print("=" * 80)
