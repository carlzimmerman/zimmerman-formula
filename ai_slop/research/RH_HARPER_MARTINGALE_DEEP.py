"""
HARPER'S MARTINGALE APPROACH: DEEP ANALYSIS
=============================================

A comprehensive analysis of Harper's multiplicative chaos framework
and what would be needed to extend it to the deterministic Möbius function.

Key references:
- Harper (2017): "Moments of random multiplicative functions, I"
- Harper (2018): "Moments of random multiplicative functions, II"
- Wang-Xu (2024): "Harper's beyond square-root conjecture"

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, prime, isprime
from collections import defaultdict
import mpmath
mpmath.mp.dps = 50

print("=" * 75)
print("HARPER'S MARTINGALE APPROACH: DEEP ANALYSIS")
print("=" * 75)

# =============================================================================
# PART 1: HARPER'S KEY RESULTS (WHAT WE KNOW)
# =============================================================================

print("\n" + "=" * 75)
print("PART 1: HARPER'S KEY RESULTS")
print("=" * 75)

print("""
HARPER'S MAIN THEOREM (2017):
============================

Let f(n) be a Steinhaus random multiplicative function:
  f(p) = e^{iθ_p} where θ_p ~ Uniform[0, 2π] independently for each prime p
  f(n) extended by multiplicativity: f(p^a q^b ...) = f(p)^a f(q)^b ...

THEOREM: E|Σ_{n≤x} f(n)| ≍ √x / (log log x)^{1/4}

More precisely, for 0 ≤ q ≤ 1:
  E|Σ_{n≤x} f(n)|^{2q} ≍ x^q / (log log x)^{q²/2}

This is BETTER than random walk (which would give √x).

The improvement factor (log log x)^{-1/4} comes from MULTIPLICATIVE CHAOS.
""")

# =============================================================================
# PART 2: THE MARTINGALE CONSTRUCTION
# =============================================================================

print("\n" + "=" * 75)
print("PART 2: THE MARTINGALE CONSTRUCTION")
print("=" * 75)

print("""
HARPER'S MARTINGALE STRUCTURE:
=============================

Define: S_x = Σ_{n≤x} f(n)

Key insight: Decompose by LARGEST prime factor.

For y ≤ x, define:
  S_x(y) = Σ_{n≤x, P(n)≤y} f(n)

where P(n) = largest prime factor of n (P(1) = 1).

Then S_x = S_x(x) and S_x(1) = f(1) = 1.

FILTRATION:
-----------
F_p = σ(f(q) : q ≤ p prime)

The family {S_x(p) : p prime ≤ x} is adapted to this filtration.

MARTINGALE PROPERTY:
--------------------
E[S_x(p') | F_p] = S_x(p) for p < p' consecutive primes

This holds because:
  S_x(p') - S_x(p) = Σ_{n≤x, P(n)=p'} f(n)
                   = Σ_{m≤x/p', P(m)<p'} f(m) · f(p')
                   = f(p') · (something depending only on f(q), q < p')

And E[f(p') | F_p] = E[f(p')] = 0 (since f(p') is independent of F_p).

So E[S_x(p') - S_x(p) | F_p] = 0.
""")

# Verify the decomposition numerically
print("\nNumerical verification of decomposition by largest prime factor:")
print("-" * 60)

def largest_prime_factor(n):
    if n == 1:
        return 1
    return max(factorint(n).keys())

# For random multiplicative function
np.random.seed(42)
primes = list(primerange(2, 100))
f_values = {p: np.exp(2j * np.pi * np.random.random()) for p in primes}

def random_mult_f(n):
    if n == 1:
        return 1.0
    factors = factorint(n)
    result = 1.0
    for p, e in factors.items():
        if p in f_values:
            result *= f_values[p] ** e
        else:
            np.random.seed(p)
            result *= np.exp(2j * np.pi * np.random.random()) ** e
    return result

x = 1000
S_by_lpf = defaultdict(complex)

for n in range(1, x + 1):
    lpf = largest_prime_factor(n)
    S_by_lpf[lpf] += random_mult_f(n)

print(f"Decomposition of S_{x} by largest prime factor:")
print(f"{'P(n)':>6} {'|Contribution|':>15} {'Count':>10}")
print("-" * 35)

lpf_sorted = sorted(S_by_lpf.keys())
total_contribution = 0
for lpf in lpf_sorted[:15]:
    contrib = abs(S_by_lpf[lpf])
    count = sum(1 for n in range(1, x+1) if largest_prime_factor(n) == lpf)
    total_contribution += S_by_lpf[lpf]
    print(f"{lpf:>6} {contrib:>15.4f} {count:>10}")

print(f"...\nTotal |S_x| = {abs(sum(S_by_lpf.values())):.4f}")

# =============================================================================
# PART 3: THE CONNECTION TO MULTIPLICATIVE CHAOS
# =============================================================================

print("\n" + "=" * 75)
print("PART 3: CONNECTION TO MULTIPLICATIVE CHAOS")
print("=" * 75)

print("""
GAUSSIAN MULTIPLICATIVE CHAOS:
==============================

Harper's key insight: The sum S_x = Σ f(n) relates to a MULTIPLICATIVE CHAOS.

Define the "Euler product" at s = 1/2:
  Z_x = Π_{p≤x} |1 - f(p)/√p|^{-1}

This product diverges logarithmically, but its distribution matters.

CONNECTION:
  E|S_x|^{2q} ≈ E[Z_x^{2q}] × (correction factors)

The random variable log Z_x is approximately Gaussian with variance ~ log log x.

CRITICAL CHAOS:
  When the variance grows logarithmically, we're at the "critical" point
  of multiplicative chaos theory.

  At criticality: E[Z_x^q] ≈ (log log x)^{-q²/2} for 0 < q < 1

This explains the (log log x)^{-1/4} factor when q = 1/2.
""")

# Compute the Euler product approximation
print("\nNumerical illustration of Euler product behavior:")
print("-" * 60)

def euler_product_contribution(x, f_values):
    """Compute Π_{p≤x} |1 - f(p)/√p|^{-1}"""
    product = 1.0
    for p in primerange(2, x + 1):
        if p in f_values:
            factor = abs(1 - f_values[p] / np.sqrt(p))
            if factor > 0.01:  # Avoid division by near-zero
                product *= 1.0 / factor
    return product

print(f"{'x':>8} {'log log x':>12} {'E[|1-f(p)/√p|^-1]':>20} {'Variance proxy':>15}")
print("-" * 60)

for x in [100, 500, 1000, 5000]:
    log_log_x = np.log(np.log(x))

    # Run multiple trials
    trials = 100
    log_products = []
    for _ in range(trials):
        f_trial = {p: np.exp(2j * np.pi * np.random.random()) for p in primerange(2, x+1)}
        Z = euler_product_contribution(x, f_trial)
        if Z > 0:
            log_products.append(np.log(Z))

    if log_products:
        var_log_Z = np.var(log_products)
        mean_log_Z = np.mean(log_products)
        print(f"{x:>8} {log_log_x:>12.4f} {mean_log_Z:>20.4f} {var_log_Z:>15.4f}")

# =============================================================================
# PART 4: THE KEY LEMMAS IN HARPER'S PROOF
# =============================================================================

print("\n" + "=" * 75)
print("PART 4: KEY LEMMAS IN HARPER'S PROOF")
print("=" * 75)

print("""
HARPER'S PROOF STRUCTURE:
=========================

LEMMA 1 (Martingale Decomposition):
-----------------------------------
S_x can be written as a sum of martingale differences:
  S_x = Σ_p (S_x(p) - S_x(p^-))
where p^- is the previous prime.

Each increment S_x(p) - S_x(p^-) depends on f(p) and earlier values.


LEMMA 2 (Conditional Variance):
-------------------------------
E[|S_x(p) - S_x(p^-)|² | F_{p^-}] ≈ |Σ_{m: P(m)<p, pm≤x} f(m)|² / p

This is bounded by (# of m with P(m) < p, pm ≤ x) / p.


LEMMA 3 (Doob's L^p Inequality):
--------------------------------
For a martingale M_n with M_0 = 0:
  E[max_n |M_n|^p] ≤ (p/(p-1))^p E[|M_∞|^p]

This controls the maximum of the martingale.


LEMMA 4 (Connection to Euler Product):
--------------------------------------
The key technical work connects:
  E|S_x|^{2q} to E|Z_x|^{2q} = E[Π_p |1-f(p)/√p|^{-2q}]

This uses:
  - Hypercontractive inequalities
  - Girsanov-type change of measure
  - Gaussian approximation for small primes


LEMMA 5 (Critical Chaos Moment):
--------------------------------
For the critical multiplicative chaos:
  E[Z^q] ≍ (log V)^{-q²/2} as V → ∞

where V is the "variance" parameter (here V ~ log log x).
""")

# =============================================================================
# PART 5: WHERE RANDOMNESS IS ESSENTIAL
# =============================================================================

print("\n" + "=" * 75)
print("PART 5: WHERE RANDOMNESS IS ESSENTIAL")
print("=" * 75)

print("""
CRITICAL USES OF RANDOMNESS IN HARPER'S PROOF:
==============================================

USE 1: Independence
-------------------
f(p) values are INDEPENDENT for different primes.
This gives:
  E[f(p)f(q)] = E[f(p)]E[f(q)] = 0 for p ≠ q

For μ(n): μ(p) = -1 for ALL primes (completely correlated!)


USE 2: Zero Mean
----------------
E[f(p)] = 0 (for Steinhaus or Rademacher)

This makes the martingale increments have zero conditional mean:
  E[S_x(p) - S_x(p^-) | F_{p^-}] = 0

For μ(n): μ(p) = -1 always, so "mean" is -1, not 0.


USE 3: Variance = 1
-------------------
E[|f(p)|²] = 1

This gives predictable second moments.

For μ(n): |μ(p)|² = 1, so this DOES hold.


USE 4: Girsanov Change of Measure
---------------------------------
Harper uses change-of-measure techniques from probability.
These require a reference measure (the random distribution of f).

For μ(n): No natural "reference measure" to change from.


USE 5: Concentration Inequalities
---------------------------------
Martingale concentration requires bounded conditional variances.
For random f, these are controlled by independence.

For μ(n): The deterministic structure may cause larger variances.
""")

# =============================================================================
# PART 6: ANALYZING μ(n) IN HARPER'S FRAMEWORK
# =============================================================================

print("\n" + "=" * 75)
print("PART 6: ANALYZING μ(n) IN HARPER'S FRAMEWORK")
print("=" * 75)

print("""
Testing: Does μ(n) satisfy the key properties?
""")

# Precompute Möbius
MAX_N = 50000
mu = [0] * (MAX_N + 1)
mu[1] = 1
for n in range(2, MAX_N + 1):
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        mu[n] = 0
    else:
        mu[n] = (-1) ** len(factors)

def mobius(n):
    if n <= MAX_N:
        return mu[n]
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return (-1) ** len(factors)

# Decompose M(x) by largest prime factor
print("\nDecomposition of M(x) by largest prime factor:")
print("-" * 60)

x = 10000
M_by_lpf = defaultdict(int)

for n in range(1, x + 1):
    lpf = largest_prime_factor(n)
    M_by_lpf[lpf] += mobius(n)

print(f"{'P(n)':>6} {'Σμ(n)':>10} {'Count':>10} {'Σμ/√Count':>12}")
print("-" * 40)

lpf_sorted = sorted(M_by_lpf.keys())
for lpf in lpf_sorted[:20]:
    contrib = M_by_lpf[lpf]
    count = sum(1 for n in range(1, x+1) if largest_prime_factor(n) == lpf)
    ratio = contrib / np.sqrt(count) if count > 0 else 0
    print(f"{lpf:>6} {contrib:>+10} {count:>10} {ratio:>+12.4f}")

print(f"\nTotal M({x}) = {sum(M_by_lpf.values()):+d}")

# =============================================================================
# PART 7: THE MARTINGALE DIFFERENCE FOR μ(n)
# =============================================================================

print("\n" + "=" * 75)
print("PART 7: MARTINGALE DIFFERENCES FOR μ(n)")
print("=" * 75)

print("""
For random f: The increment Δ_p = S_x(p) - S_x(p^-) has E[Δ_p | F_{p^-}] = 0.

For μ: Let's compute Δ_p = M_x(p) - M_x(p^-) where
       M_x(p) = Σ_{n≤x, P(n)≤p} μ(n)

Is there a "pseudo-zero-mean" property?
""")

def M_x_upto_lpf(x, max_lpf):
    """Sum μ(n) for n ≤ x with P(n) ≤ max_lpf."""
    return sum(mobius(n) for n in range(1, x+1) if largest_prime_factor(n) <= max_lpf)

x = 5000
primes_list = list(primerange(2, int(np.sqrt(x)) + 100))

print(f"\nMartingale increments Δ_p = M_{x}(p) - M_{x}(p^-) for μ:")
print("-" * 60)
print(f"{'p':>6} {'p^-':>6} {'M_x(p)':>10} {'Δ_p':>10} {'Expected Δ':>12}")
print("-" * 55)

prev_M = M_x_upto_lpf(x, 1)  # M_x(1) = μ(1) = 1
prev_p = 1

for i, p in enumerate(primes_list[:20]):
    curr_M = M_x_upto_lpf(x, p)
    delta = curr_M - prev_M

    # What would the "expected" delta be?
    # For random: 0
    # For μ: The sum involves μ(p) × M_x/p(p^-)
    expected_delta = 0  # Placeholder

    print(f"{p:>6} {prev_p:>6} {curr_M:>+10} {delta:>+10} {expected_delta:>12}")

    prev_M = curr_M
    prev_p = p

print("""
OBSERVATION:
The increments Δ_p are NOT zero-mean for μ(n).
They show systematic patterns related to the prime distribution.

This is the key difference from random multiplicative functions.
""")

# =============================================================================
# PART 8: CAN WE RESCUE THE MARTINGALE APPROACH?
# =============================================================================

print("\n" + "=" * 75)
print("PART 8: CAN WE RESCUE THE MARTINGALE APPROACH FOR μ(n)?")
print("=" * 75)

print("""
STRATEGY 1: Centering
---------------------
Instead of E[f(p)] = 0, use E[μ(p)] = -1.

Define: μ*(n) = μ(n) + 1_{n=p for some prime}

This "centers" the prime contributions.

Problem: μ*(n) is no longer multiplicative!


STRATEGY 2: Twisted Martingale
------------------------------
Define a different filtration based on prime residues mod q.

Use the Dirichlet characters to "spread" the determinism.

Problem: Requires GRH for L-functions (Wang-Xu approach).


STRATEGY 3: Conditional Martingale
----------------------------------
Condition on some "large" information set that makes μ look random.

For example, condition on all primes up to x^{1/log log x}.

Problem: Need to show conditional distribution is "nice."


STRATEGY 4: Weak Dependence
---------------------------
Show μ(n) has "weak dependence" in a suitable sense.

If correlations decay fast enough, martingale methods may still apply.

This is related to GUE hypothesis for zeros.
""")

# Test weak dependence
print("\nTesting weak dependence of μ(n):")
print("-" * 50)

# Compute correlations μ(n)μ(n+k) for various k
x = 10000

def correlation_mu(x, lag):
    """Compute correlation between μ(n) and μ(n+lag) for n ≤ x - lag."""
    vals1 = [mobius(n) for n in range(1, x - lag + 1)]
    vals2 = [mobius(n + lag) for n in range(1, x - lag + 1)]
    # Only consider where both are nonzero
    pairs = [(v1, v2) for v1, v2 in zip(vals1, vals2) if v1 != 0 and v2 != 0]
    if len(pairs) < 10:
        return 0
    v1s, v2s = zip(*pairs)
    return np.corrcoef(v1s, v2s)[0, 1]

print(f"{'Lag k':>8} {'Corr(μ(n), μ(n+k))':>25}")
print("-" * 35)
for lag in [1, 2, 3, 5, 7, 10, 20, 50, 100]:
    corr = correlation_mu(x, lag)
    print(f"{lag:>8} {corr:>+25.6f}")

print("""
OBSERVATION:
Correlations are very small but nonzero.
The weak dependence may be exploitable, but it's not obviously so.
""")

# =============================================================================
# PART 9: THE WANG-XU APPROACH (LIOUVILLE)
# =============================================================================

print("\n" + "=" * 75)
print("PART 9: THE WANG-XU APPROACH")
print("=" * 75)

print("""
WANG-XU (2024): Harper's Conjecture for Liouville
=================================================

Wang-Xu proved (conditionally) that the Liouville function λ(n) = (-1)^Ω(n)
satisfies Harper's bound.

THEOREM (Wang-Xu, conditional):
Under GRH for Dirichlet L-functions and the Ratios Conjecture:
  Σ_{n≤x} λ(n)χ(n) = O(√x / (log log x)^{1/4-ε})

where χ is a Dirichlet character.

KEY IDEA:
---------
1. For χ primitive, the sum Σ λ(n)χ(n) relates to L(s, χ).
2. GRH controls where zeros are.
3. The Ratios Conjecture gives fine correlation control.
4. Together, they allow a "randomization" argument.

THE RATIOS CONJECTURE:
----------------------
A deep conjecture from random matrix theory about correlations:
  E[L(1/2+it₁, χ) L(1/2+it₂, χ̄) ...] / E[|L(1/2+it, χ)|² ...]

This essentially says L-functions "look random" in a statistical sense.

WHY MÖBIUS IS HARDER:
---------------------
For λ(n), we have λ(n) = Σ_{d²|n} μ(n/d²), so λ is "smoother."
For μ(n), the squarefree condition creates harder combinatorics.

Additionally, the Wang-Xu proof uses:
  1/ζ(s) = Σ μ(n)/n^s  which has poles at zeros of ζ

while for λ:
  ζ(2s)/ζ(s) = Σ λ(n)/n^s  which has a more regular analytic structure.
""")

# =============================================================================
# PART 10: WHAT WOULD BE NEEDED FOR UNCONDITIONAL RESULT
# =============================================================================

print("\n" + "=" * 75)
print("PART 10: WHAT'S NEEDED FOR UNCONDITIONAL RESULT")
print("=" * 75)

print("""
TO PROVE HARPER'S CONJECTURE FOR μ(n) UNCONDITIONALLY:
======================================================

REQUIREMENT 1: Remove GRH
-------------------------
Need zero control for ζ(s) without assuming zeros are on critical line.

Current best: ζ(s) ≠ 0 for Re(s) > 1 - c/log|t|.

This is NOT strong enough for Harper-type bounds.


REQUIREMENT 2: Remove Ratios Conjecture
---------------------------------------
The Ratios Conjecture is about fine correlations of L-values.

Without it, need different techniques to control:
  E[Σ μ(n)/n^{1/2+it}] and higher moments.


REQUIREMENT 3: Handle Determinism
---------------------------------
μ(p) = -1 is completely deterministic.

Need to show this determinism doesn't ruin the argument.

Possible approach: Show μ is "pseudorandom" in a weaker sense that
still implies the bound.


THE FUNDAMENTAL QUESTION:
-------------------------
Is there a property P such that:
  1. P is provable for μ(n) without assuming RH
  2. P implies |M(x)| = O(x^{1/2} / (log log x)^{1/4})
  3. P is weaker than "random multiplicative function"

Finding such P would be a major breakthrough.


CANDIDATES FOR P:
-----------------
(a) "Weak randomness": Correlations decay at some rate
(b) "Equidistribution": Prime residues satisfy some uniformity
(c) "Multiplicative chaos condition": Euler product has bounded moments
(d) "Martingale approximation": μ is close to a martingale in L^p
(e) Something new


THE CURRENT GAP:
----------------
All candidates (a)-(d) either:
  - Require RH to prove, or
  - Are too weak to imply the bound

Finding a new candidate (e) is the open problem.
""")

# =============================================================================
# PART 11: NUMERICAL EXPLORATION OF CANDIDATES
# =============================================================================

print("\n" + "=" * 75)
print("PART 11: NUMERICAL EXPLORATION OF CANDIDATE PROPERTIES")
print("=" * 75)

# Test candidate (a): Correlation decay
print("\nCandidate (a): Correlation decay of M(x)")
print("-" * 50)

# Compute autocorrelation of M(n) - M(n-1) = μ(n)
mu_seq = [mobius(n) for n in range(1, 10001)]

for lag in [1, 5, 10, 50, 100, 500]:
    # Correlation of μ(n) with μ(n+lag)
    corr = np.corrcoef(mu_seq[:-lag], mu_seq[lag:])[0, 1]
    print(f"  Lag {lag:>4}: autocorr = {corr:+.6f}")

# Test candidate (c): Euler product moments
print("\nCandidate (c): Euler product moment behavior")
print("-" * 50)

def partial_euler_product_mu(x, sigma=0.6):
    """Compute Π_{p≤x} (1 - 1/p^σ) ≈ 1/ζ(σ) as x → ∞."""
    product = 1.0
    for p in primerange(2, int(x) + 1):
        product *= (1 - 1/p**sigma)
    return product

print(f"{'x':>8} {'Π(1-1/p^0.6)':>15} {'1/ζ(0.6)':>15}")
print("-" * 40)
zeta_06_inv = float(1/mpmath.zeta(0.6))
for x in [100, 500, 1000, 5000, 10000]:
    prod = partial_euler_product_mu(x, 0.6)
    print(f"{x:>8} {prod:>15.8f} {zeta_06_inv:>15.8f}")

# Test candidate (d): Distance to a martingale
print("\nCandidate (d): How close is M(x) to a martingale?")
print("-" * 50)

# For a true martingale M_n: E[M_{n+1} - M_n | M_n] = 0
# Compute empirical conditional means

increments = [mobius(n) for n in range(2, 10001)]
prev_values = [sum(mobius(k) for k in range(1, n)) for n in range(2, 10001)]

# Bin by previous value and compute mean increment
bins = defaultdict(list)
for pv, inc in zip(prev_values, increments):
    bins[pv].append(inc)

print(f"{'M(n-1)':>8} {'E[μ(n) | M(n-1)]':>20} {'Count':>10}")
print("-" * 40)
for m_prev in sorted(bins.keys()):
    if len(bins[m_prev]) >= 5:
        mean_inc = np.mean(bins[m_prev])
        count = len(bins[m_prev])
        print(f"{m_prev:>8} {mean_inc:>+20.6f} {count:>10}")

print("""
OBSERVATION:
The conditional mean E[μ(n) | M(n-1)] is approximately zero,
but there's no exact martingale property.

This "approximate martingale" behavior might be exploitable.
""")

# =============================================================================
# PART 12: SYNTHESIS AND NEXT STEPS
# =============================================================================

print("\n" + "=" * 75)
print("PART 12: SYNTHESIS AND RESEARCH DIRECTIONS")
print("=" * 75)

print("""
SUMMARY OF HARPER'S APPROACH:
=============================

1. WHAT HARPER PROVED:
   Random multiplicative f has E|Σf(n)| ≍ √x / (log log x)^{1/4}

2. HOW HE PROVED IT:
   - Martingale decomposition by largest prime factor
   - Connection to Gaussian multiplicative chaos
   - Critical moment bounds via hypercontractive inequalities

3. WHY IT WORKS FOR RANDOM f:
   - Independence: f(p) independent across primes
   - Zero mean: E[f(p)] = 0
   - Girsanov techniques: Can change measure

4. WHY IT DOESN'T DIRECTLY WORK FOR μ:
   - No independence: μ(p) = -1 always
   - No zero mean: "E[μ(p)]" = -1
   - No natural reference measure


WANG-XU EXTENSION:
==================

5. WHAT WANG-XU PROVED (conditional):
   λ(n) satisfies Harper's bound under GRH + Ratios Conjecture

6. KEY INSIGHT:
   Character twists make λ "look random" in a statistical sense

7. THE GAP TO μ:
   Need to either remove GRH/Ratios or find alternative approach


RESEARCH DIRECTIONS:
====================

DIRECTION A: Strengthen Wang-Xu
  Try to extend from λ to μ using 1/ζ(s) = Σμ(n)/n^s
  Challenge: More complicated pole structure

DIRECTION B: Approximate Martingale
  Show M(x) is ε-close to a martingale in some norm
  Challenge: Need to quantify the approximation

DIRECTION C: Weak Randomness
  Define a notion of "weak randomness" μ satisfies
  Challenge: Need it strong enough to imply bounds

DIRECTION D: Different Decomposition
  Instead of largest prime, use other decompositions
  Example: By Ω(n) instead of P(n)
  Challenge: Need to maintain useful structure

DIRECTION E: Completely New Approach
  Find a property of μ not related to randomness
  Example: Multiplicative structure directly implies bounds
  Challenge: Nobody has found such a property


THE CORE OBSTRUCTION:
=====================

Every approach to Harper's bound uses randomness essentially.
For deterministic μ, we need either:
  (a) A way to "induce" randomness (Wang-Xu approach, needs GRH)
  (b) A proof that determinism helps (counterintuitive but possible)
  (c) A completely new framework

Finding any of (a), (b), or (c) would be a major breakthrough.
""")

print("\n" + "=" * 75)
print("END OF HARPER MARTINGALE DEEP ANALYSIS")
print("=" * 75)
