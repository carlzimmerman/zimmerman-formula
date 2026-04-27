"""
COMBINATORIAL APPROACH TO VARIANCE BOUND
=========================================

Goal: Prove Var(ω) < λ using COMBINATORIAL arguments
that don't depend on prime distribution estimates.

Key insight: The structure of squarefree numbers is highly
constrained. Can we exploit this combinatorially?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
import math

print("=" * 80)
print("COMBINATORIAL APPROACH TO VARIANCE BOUND")
print("=" * 80)

# =============================================================================
# THE KEY STRUCTURAL INSIGHT
# =============================================================================

print("\n" + "=" * 80)
print("THE KEY STRUCTURAL INSIGHT")
print("=" * 80)

print("""
STRUCTURAL CONSTRAINT:
======================

For a squarefree n ≤ x with ω(n) = w prime factors:
    n = p₁ · p₂ · ... · p_w  where p₁ < p₂ < ... < p_w

The product constraint n ≤ x means:
    p₁ · p₂ · ... · p_w ≤ x

This is HIGHLY restrictive. For example:
    - If w = 6: need p₁·p₂·p₃·p₄·p₅·p₆ ≤ x
    - The MINIMUM 6-prime product is 2·3·5·7·11·13 = 30030
    - So for x < 30030, there are NO squarefree numbers with ω = 6

THE COUNTING FORMULA:
=====================
S_w(x) = #{distinct sets {p₁,...,p_w} of w primes with product ≤ x}

This is a CONSTRAINED counting problem!
""")

# =============================================================================
# ANALYZE THE CONSTRAINT
# =============================================================================

print("\n" + "=" * 80)
print("ANALYZING THE PRODUCT CONSTRAINT")
print("=" * 80)

# Compute minimum product of w primes
primes_list = list(primerange(2, 1000))

def min_product(w):
    """Minimum product of w distinct primes."""
    if w > len(primes_list):
        return float('inf')
    return np.prod(primes_list[:w])

print("\nMinimum product of w distinct primes:")
print("-" * 40)
print(f"{'w':>4} | {'Min Product':>15} | {'log(MinProd)':>12}")
print("-" * 40)

for w in range(1, 12):
    mp = min_product(w)
    print(f"{w:>4} | {mp:>15} | {np.log(mp):>12.4f}")

print(f"""

For x = 100,000 (log x ≈ 11.5):
- w = 6: min product = 30,030 < x  ✓ (possible)
- w = 7: min product = 510,510 > x  ✗ (impossible)

So S_w(x) = 0 for w ≥ 7 when x = 100,000.
This is a HARD CONSTRAINT.
""")

# =============================================================================
# THE INDEPENDENCE VS CONSTRAINT GAP
# =============================================================================

print("\n" + "=" * 80)
print("INDEPENDENCE vs CONSTRAINT")
print("=" * 80)

print("""
THE POISSON MODEL:
==================
If prime factors were chosen independently with P(p ∈ factors) = 1/p,
then ω would be Poisson(λ) where λ = Σ_p 1/p ≈ log log x.

Poisson(λ) puts positive probability on ALL w ≥ 0.
For large w, P_Poisson(ω = w) = λʷ e^{-λ} / w!

THE CONSTRAINT:
===============
The product constraint n ≤ x forces S_w(x) = 0 for w > w_max(x).

This is NOT captured by the Poisson model!

KEY QUESTION:
=============
Does the product constraint FORCE Var(ω) < λ?
""")

# Compute w_max for various x
print("\nMaximum possible ω(n) for n ≤ x:")
print("-" * 40)
print(f"{'x':>10} | {'w_max':>6} | {'λ':>8}")
print("-" * 40)

for x in [100, 1000, 10000, 100000, 1000000]:
    w_max = 0
    while min_product(w_max + 1) <= x:
        w_max += 1
    lam = np.log(np.log(x))
    print(f"{x:>10} | {w_max:>6} | {lam:>8.4f}")

# =============================================================================
# A POTENTIAL THEOREM
# =============================================================================

print("\n" + "=" * 80)
print("A POTENTIAL THEOREM")
print("=" * 80)

print("""
OBSERVATION:
============
w_max(x) = floor(log x / log 2) approximately

Because the minimum w-prime product is 2·3·5·...·p_w ≈ e^{p_w}
and p_w ≈ w log w, so min product ≈ e^{w log w} ≈ w^w

For w^w ≤ x: w ≲ log x / log log x

THEOREM ATTEMPT:
================
Claim: For a TRUNCATED Poisson distribution (values ≤ k),
the variance is LESS than the full Poisson variance.

Proof sketch:
- Truncation removes probability mass from large values
- Variance measures spread
- Removing large values reduces spread
- Therefore variance decreases

This is TRUE! But the issue is: is the ACTUAL distribution
close enough to truncated Poisson?
""")

# =============================================================================
# TRUNCATED POISSON ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("TRUNCATED POISSON ANALYSIS")
print("=" * 80)

def poisson_pmf(w, lam):
    """Poisson probability mass function."""
    return (lam ** w) * np.exp(-lam) / math.factorial(w)

def truncated_poisson_stats(lam, k_max):
    """Statistics of Poisson truncated to [0, k_max]."""
    # Probabilities before normalization
    probs = [poisson_pmf(w, lam) for w in range(k_max + 1)]
    Z = sum(probs)  # Normalization constant

    # Normalized probabilities
    probs_norm = [p / Z for p in probs]

    # Mean and variance
    mean = sum(w * probs_norm[w] for w in range(k_max + 1))
    mean_sq = sum(w**2 * probs_norm[w] for w in range(k_max + 1))
    var = mean_sq - mean**2

    return mean, var, Z

print("\nTruncated Poisson statistics:")
print("-" * 70)
print(f"{'λ':>6} | {'k_max':>6} | {'E_trunc':>10} | {'Var_trunc':>10} | {'Var/λ':>10}")
print("-" * 70)

for lam in [2.0, 2.5, 3.0]:
    for k_max in [4, 5, 6, 7, 100]:
        mean, var, _ = truncated_poisson_stats(lam, k_max)
        print(f"{lam:>6.2f} | {k_max:>6} | {mean:>10.4f} | {var:>10.4f} | {var/lam:>10.4f}")
    print()

print("""
KEY OBSERVATION:
================
For truncated Poisson:
- When k_max is close to λ, Var/λ is significantly reduced
- When k_max >> λ, Var/λ approaches 1 (full Poisson)

But the actual distribution is NOT truncated Poisson.
It's a CONSTRAINED counting problem with product constraint.
""")

# =============================================================================
# ACTUAL vs TRUNCATED POISSON
# =============================================================================

print("\n" + "=" * 80)
print("ACTUAL vs TRUNCATED POISSON")
print("=" * 80)

# Precompute
MAX_N = 100000
mu = [0] * (MAX_N + 1)
omega_vals = [0] * (MAX_N + 1)

mu[1] = 1
omega_vals[1] = 0

for n in range(2, MAX_N + 1):
    factors = factorint(n)
    omega_vals[n] = len(factors)
    if any(e > 1 for e in factors.values()):
        mu[n] = 0
    else:
        mu[n] = (-1) ** len(factors)

def get_distribution(x):
    """Get the actual distribution of ω for squarefree n ≤ x."""
    S = defaultdict(int)
    for n in range(1, min(x+1, MAX_N+1)):
        if mu[n] != 0:
            S[omega_vals[n]] += 1
    Q = sum(S.values())
    return {w: S[w]/Q for w in S}, Q

x = 100000
actual_dist, Q = get_distribution(x)
lam = np.log(np.log(x))
k_max = max(actual_dist.keys())

print(f"\nAt x = {x:,}, λ = {lam:.4f}, k_max = {k_max}")
print("-" * 60)
print(f"{'w':>4} | {'P(actual)':>12} | {'P(trunc)':>12} | {'P(Poisson)':>12}")
print("-" * 60)

trunc_mean, trunc_var, _ = truncated_poisson_stats(lam, k_max)
for w in range(k_max + 1):
    p_actual = actual_dist.get(w, 0)
    p_trunc = poisson_pmf(w, lam) / sum(poisson_pmf(k, lam) for k in range(k_max + 1))
    p_poisson = poisson_pmf(w, lam)
    print(f"{w:>4} | {p_actual:>12.6f} | {p_trunc:>12.6f} | {p_poisson:>12.6f}")

# Compute actual mean and variance
actual_mean = sum(w * actual_dist.get(w, 0) for w in range(k_max + 1))
actual_var = sum(w**2 * actual_dist.get(w, 0) for w in range(k_max + 1)) - actual_mean**2

print(f"\nStatistics comparison:")
print(f"  Actual:  E = {actual_mean:.4f}, Var = {actual_var:.4f}, Var/λ = {actual_var/lam:.4f}")
print(f"  Trunc:   E = {trunc_mean:.4f}, Var = {trunc_var:.4f}, Var/λ = {trunc_var/lam:.4f}")
print(f"  Poisson: E = {lam:.4f}, Var = {lam:.4f}, Var/λ = 1.0000")

# =============================================================================
# THE GAP BETWEEN ACTUAL AND TRUNCATED
# =============================================================================

print("\n" + "=" * 80)
print("THE GAP: ACTUAL vs TRUNCATED POISSON")
print("=" * 80)

print("""
OBSERVATION:
============
Actual Var/λ ≈ 0.36
Truncated Poisson Var/λ ≈ 0.99 (almost no reduction from truncation)

The truncation alone doesn't explain the variance reduction!

The actual distribution is MORE CONCENTRATED than truncated Poisson.
This extra concentration comes from the PRODUCT CONSTRAINT.

THE PRODUCT CONSTRAINT:
=======================
It's not just "w ≤ k_max".
It's "the product of w primes ≤ x".

For w = 3:
- Truncated Poisson allows any 3 primes
- Actual allows only 3 primes with product ≤ x
- This is much more restrictive!

For example, {2, 3, 5} is allowed, but {97, 101, 103} is NOT
(product ≈ 10^6 > 10^5).
""")

# =============================================================================
# CAN WE PROVE THE CONSTRAINT REDUCES VARIANCE?
# =============================================================================

print("\n" + "=" * 80)
print("CAN WE PROVE PRODUCT CONSTRAINT REDUCES VARIANCE?")
print("=" * 80)

print("""
THE CHALLENGE:
==============

We want to prove: Var(ω) < λ

The product constraint n ≤ x creates dependencies:
- Choosing a large prime p means remaining primes must multiply to ≤ x/p
- Choosing small primes "uses up" less of the budget
- This creates negative correlations among indicator variables

POTENTIAL THEOREM:
==================
For any constraint that restricts product ≤ x:

Var(ω) ≤ λ - c(x)

where c(x) > 0 depends on how restrictive the constraint is.

PROBLEM:
========
To quantify c(x), we need to know HOW MANY squarefree numbers
satisfy the constraint. This brings us back to counting...

And counting squarefree numbers = Q(x) = 6x/π² + O(x^{1/2+ε}) under RH.
""")

# =============================================================================
# THE FUNDAMENTAL OBSTACLE
# =============================================================================

print("\n" + "=" * 80)
print("THE FUNDAMENTAL OBSTACLE")
print("=" * 80)

print("""
WHY COMBINATORIAL ARGUMENTS FAIL:
=================================

1. The variance reduction is REAL (Var/λ ≈ 0.36)

2. It comes from the PRODUCT CONSTRAINT (not just truncation)

3. But to PROVE it, we need to:
   a) Count how many squarefree n have each ω value
   b) Compute the exact distribution
   c) Show the variance is reduced

4. Step (a) requires counting squarefree numbers
   S_w(x) = #{n ≤ x : n squarefree, ω(n) = w}

5. Counting squarefree numbers involves the Möbius function:
   Q(x) = Σ_{d² ≤ x} μ(d) · floor(x/d²)

6. The error in this sum is controlled by ζ zeros!

THE CIRCLE:
===========
Variance bound → Counting squarefree → Möbius sum → ζ zeros → RH

Every path leads back to the same obstruction.
""")

# =============================================================================
# A FINAL OBSERVATION
# =============================================================================

print("\n" + "=" * 80)
print("A FINAL OBSERVATION")
print("=" * 80)

print("""
WHAT WE'VE LEARNED:
===================

1. The variance reduction is NOT from simple truncation
   (truncated Poisson gives Var/λ ≈ 0.99, we observe 0.36)

2. The extra reduction comes from the PRODUCT CONSTRAINT
   (choosing large primes restricts other choices)

3. This creates NEGATIVE CORRELATIONS among prime indicators

4. But proving this reduction requires counting arguments

5. Counting arguments require controlling ζ zeros

THE INSIGHT:
============
The variance reduction Var(ω)/λ ≈ 0.36 is DEEP.
It reflects fundamental structure in the primes.
This structure is encoded in the ζ zeros.

We cannot access this structure without going through ζ.

CONCLUSION:
===========
The combinatorial approach, while illuminating, does not
bypass the need for analytic number theory.

The proof of RH remains elusive.
""")

print("=" * 80)
print("COMBINATORIAL ANALYSIS COMPLETE")
print("=" * 80)
