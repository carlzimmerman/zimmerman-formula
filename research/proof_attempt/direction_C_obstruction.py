"""
DIRECTION C: IDENTIFYING AND ATTACKING THE OBSTRUCTION
=======================================================

Goal: Understand PRECISELY what blocks a proof of RH,
and explore whether any novel approach can bypass it.

This is the deepest investigation - looking for the key insight
that could unlock a proof.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, log, symbols, Sum, oo, exp, I, pi, sqrt
from sympy import Function, Eq, solve, simplify, factorial, binomial
from collections import defaultdict
import mpmath
mpmath.mp.dps = 30

print("=" * 80)
print("DIRECTION C: IDENTIFYING AND ATTACKING THE OBSTRUCTION")
print("=" * 80)

# =============================================================================
# PART 1: THE FUNDAMENTAL OBSTRUCTION
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE FUNDAMENTAL OBSTRUCTION")
print("=" * 80)

print("""
THE CORE QUESTION:
==================

We want to prove: |M(x)| = O(x^{1/2+ε})

This is equivalent to: All zeros of ζ(s) have Re(s) ≤ 1/2

WHY IS THIS HARD?
=================

The explicit formula gives:
    M(x) = -2 + Σ_ρ x^ρ / (ρ ζ'(ρ)) + O(1)

Each zero ρ = β + iγ contributes a term of size ~x^β.

To have |M(x)| = O(x^{1/2+ε}), we need:
    - Every zero has β ≤ 1/2 (this is RH)
    - OR the zeros with β > 1/2 cancel each other (unlikely)

THE CIRCULAR LOGIC:
===================

1. To bound M(x), we need to control the explicit formula sum.
2. To control the sum, we need to know where the zeros are.
3. Knowing where the zeros are IS the Riemann Hypothesis.

Every path leads back to this circle.

THE QUESTION: Is there ANY way to break this cycle?
""")

# =============================================================================
# PART 2: WHAT WOULD BREAK THE CYCLE?
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: WHAT WOULD BREAK THE CYCLE?")
print("=" * 80)

print("""
POTENTIAL CYCLE BREAKERS:
=========================

A. STRUCTURAL ARGUMENT:
   Prove that the structure of primes FORCES the zeros to be on Re(s) = 1/2.
   Example: Some symmetry or constraint that makes off-line zeros impossible.

B. PROBABILISTIC ARGUMENT:
   Show that "typical" multiplicative functions have bounded sums,
   and μ(n) is "typical enough" to inherit this bound.
   (Harper's approach, but for deterministic μ)

C. FUNCTIONAL EQUATION ARGUMENT:
   Use ζ(s) = χ(s) ζ(1-s) to derive constraints on zeros.
   The functional equation relates ρ and 1-ρ, but doesn't force β = 1/2.

D. OPERATOR ARGUMENT (Hilbert-Pólya):
   Find a self-adjoint operator with eigenvalues = zeros.
   Self-adjointness would force real eigenvalues → Re(ρ) = 1/2.

E. ARITHMETIC ARGUMENT:
   Find a property of primes that directly implies M(x) = O(√x)
   without going through the explicit formula.

Let's explore each of these.
""")

# =============================================================================
# PART 3: EXPLORING STRUCTURAL ARGUMENTS
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: STRUCTURAL ARGUMENTS")
print("=" * 80)

print("""
STRUCTURAL APPROACH:
====================

The Möbius function μ(n) has a very specific structure:
- μ(n) = 0 if n has a squared prime factor
- μ(n) = (-1)^{ω(n)} if n is squarefree

This structure comes from the MULTIPLICATIVITY of μ:
    μ(mn) = μ(m)μ(n) when gcd(m,n) = 1

Question: Does multiplicativity FORCE a bound on M(x)?

ANALYSIS:
---------
For a general multiplicative function f:
    Σ_{n≤x} f(n) = Π_{p≤x} (1 + f(p) + f(p²) + ...)

For μ(n):
    Σ_{n≤x} μ(n) is NOT a simple Euler product because of the cutoff n ≤ x.

The cutoff destroys the multiplicative structure!
This is why M(x) is hard to analyze.
""")

# Numerical verification: how does M(x) relate to Euler products?
print("\nChecking partial Euler products:")
print("-" * 60)

def partial_euler_product(x, f_p):
    """Compute Π_{p≤x} f(p) for primes p up to x."""
    from sympy import primerange
    product = 1.0
    for p in primerange(2, x+1):
        product *= f_p(p)
    return product

# For μ, the Euler product is Π_p (1 - 1/p^s) = 1/ζ(s)
# At s = 1, this diverges (ζ(1) = ∞)
# The partial product Π_{p≤x} (1 - 1/p) ~ 1/log(x)

for x in [100, 1000, 10000]:
    partial_prod = partial_euler_product(x, lambda p: 1 - 1/p)
    expected = 1 / np.log(x)  # Mertens' theorem
    print(f"x = {x:>6}: Π(1-1/p) = {partial_prod:.6f}, 1/log(x) = {expected:.6f}")

# =============================================================================
# PART 4: EXPLORING PROBABILISTIC ARGUMENTS
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: PROBABILISTIC ARGUMENTS")
print("=" * 80)

print("""
PROBABILISTIC APPROACH (Harper-style):
======================================

Harper proved for RANDOM multiplicative f:
    E|Σ f(n)| ≍ √x / (log log x)^{1/4}

Key ingredients:
1. Independence: f(p) are independent random variables
2. Multiplicativity: f(mn) = f(m)f(n)
3. Martingale structure: Filter by largest prime factor

For μ(n), we DON'T have independence: μ(p) = -1 for ALL primes.

But we DO have:
- Multiplicativity
- ω(n) distribution is "almost Poisson"
- Strong arithmetic structure

QUESTION: Can structure substitute for randomness?

The key insight from our generating function:
    M(x) = Σ_w (-1)^w S_w(x)

The S_w values are CORRELATED. These correlations arise from:
1. The constraint Σ S_w = Q(x)
2. The prime distribution (Mertens' theorem, etc.)
3. The ζ zeros (explicit formula)

The third point is the obstruction: the correlations encode the zeros.
""")

# =============================================================================
# PART 5: THE INDEPENDENCE HYPOTHESIS
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: THE INDEPENDENCE HYPOTHESIS")
print("=" * 80)

print("""
THOUGHT EXPERIMENT: What if S_w were independent?
=================================================

If S_w ~ Poisson(λ_w) independently, with λ_w = Q · Poisson(λ; w),
then:

    Var(M) = Var(Σ(-1)^w S_w) = Σ Var(S_w) = Σ λ_w ≈ Q(x)

This gives |M| ~ √Q ≈ √x typically.

But this is already known! The question is whether |M| can be
LARGER than √x, i.e., whether there's a zero with β > 1/2.

The ACTUAL correlations might make Var(M) smaller or larger than Q.
- Smaller: consistent with RH
- Larger: would suggest zeros off the line

Let's compute the actual variance-like quantity.
""")

# Compute actual vs independent variance
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

def get_S_w(x):
    S = defaultdict(int)
    for n in range(1, min(x+1, MAX_N+1)):
        if mu[n] != 0:
            S[omega_vals[n]] += 1
    return dict(S)

def get_M(x):
    return sum(mu[n] for n in range(1, min(x+1, MAX_N+1)))

def get_Q(x):
    return sum(1 for n in range(1, min(x+1, MAX_N+1)) if mu[n] != 0)

x = 100000
S = get_S_w(x)
Q = get_Q(x)
M = get_M(x)

# Independent model variance
var_independent = Q

# Actual M²
var_actual = M**2

# Ratio
ratio = var_actual / var_independent

print(f"\nVariance comparison at x = {x:,}:")
print(f"  Q(x) = {Q:,} (= Var under independence)")
print(f"  M(x)² = {M**2:,} (actual squared)")
print(f"  Ratio M²/Q = {ratio:.6f}")
print(f"  √Ratio = |M|/√Q = {np.sqrt(ratio):.4f}")

print("""
OBSERVATION:
M²/Q << 1, which means the actual "variance" is much smaller
than the independent model predicts.

This is CONSISTENT with RH: the correlations are reducing variance.
But we can't PROVE the correlations always work this way.
""")

# =============================================================================
# PART 6: A NEW ATTACK: FOURIER ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: A NEW ATTACK - FOURIER ANALYSIS")
print("=" * 80)

print("""
FOURIER APPROACH:
=================

Consider the characteristic function:
    φ(θ) = E[e^{iωθ}] = (1/Q) Σ S_w e^{iwθ}

This is the Fourier transform of the S_w sequence.

At θ = π: φ(π) = M/Q (the quantity we want to bound)

The question becomes:
    Why is |φ(π)| small?

For a Poisson distribution:
    φ_Poisson(θ) = exp(λ(e^{iθ} - 1))
    φ_Poisson(π) = exp(-2λ) = 1/(log x)²

This is LARGER than what we observe (|M|/Q ~ 1/√x under RH).

The S_w distribution is SMOOTHER than Poisson!
""")

# Compute characteristic function on unit circle
theta_values = np.linspace(0, 2*np.pi, 100)
phi_values = []

for theta in theta_values:
    z = np.exp(1j * theta)
    G_z = sum(S[w] * (z ** w) for w in S)
    phi = G_z / Q
    phi_values.append(phi)

phi_values = np.array(phi_values)

print("\nCharacteristic function behavior:")
print("-" * 50)
print(f"{'θ/π':>8} | {'|φ(θ)|':>10} | {'arg(φ)':>10}")
print("-" * 50)

for i in range(0, 100, 10):
    theta = theta_values[i]
    phi = phi_values[i]
    print(f"{theta/np.pi:>8.2f} | {abs(phi):>10.6f} | {np.angle(phi):>10.4f}")

print(f"\n|φ(π)| = {abs(phi_values[50]):.6f}")
print(f"Poisson prediction: {np.exp(-2 * np.log(np.log(x))):.6f}")

# =============================================================================
# PART 7: THE SMOOTHNESS ARGUMENT
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: THE SMOOTHNESS ARGUMENT")
print("=" * 80)

print("""
KEY INSIGHT: The S_w distribution is SMOOTHER than Poisson.

This smoothness causes rapid decay in the Fourier domain,
which is why |φ(π)| = |M|/Q is small.

QUESTION: Can we PROVE the smoothness?

The smoothness comes from:
1. S_w is constrained by the prime distribution
2. Mertens' theorem gives λ = log log x
3. Finer structure from prime gaps

If we could prove:
    "S_w is at least as smooth as a Gaussian with variance λ"

Then the Fourier transform would decay like exp(-θ² λ/2),
giving |φ(π)| ~ exp(-π² λ/2) which is even smaller than needed.
""")

# Test smoothness: compare S_w to Gaussian
import math

def gaussian_prob(w, mean, variance):
    """Gaussian probability mass approximation."""
    return np.exp(-0.5 * (w - mean)**2 / variance) / np.sqrt(2 * np.pi * variance)

def poisson_prob(w, lam):
    """Poisson probability."""
    return (lam**w) * np.exp(-lam) / math.factorial(w)

lam = np.log(np.log(x))
mean_w = sum(w * S.get(w, 0) for w in range(20)) / Q
var_w = sum((w - mean_w)**2 * S.get(w, 0) for w in range(20)) / Q

print(f"\nDistribution statistics at x = {x:,}:")
print(f"  λ = log log x = {lam:.4f}")
print(f"  E[ω] = {mean_w:.4f}")
print(f"  Var(ω) = {var_w:.4f}")
print(f"  Poisson prediction: E = Var = λ = {lam:.4f}")

print(f"\nActual vs model comparison:")
print("-" * 60)
print(f"{'w':>4} | {'P(actual)':>10} | {'P(Poisson)':>10} | {'P(Gauss)':>10}")
print("-" * 60)

for w in range(7):
    p_actual = S.get(w, 0) / Q
    p_poisson = poisson_prob(w, lam)
    p_gauss = gaussian_prob(w, mean_w, var_w)
    print(f"{w:>4} | {p_actual:>10.6f} | {p_poisson:>10.6f} | {p_gauss:>10.6f}")

# =============================================================================
# PART 8: THE CRITICAL INSIGHT
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: THE CRITICAL INSIGHT")
print("=" * 80)

print("""
CRITICAL OBSERVATION:
=====================

The actual distribution of ω(n) is:
- MORE CONCENTRATED than Poisson (lower variance)
- SHIFTED to higher mean (mean ≈ 2.4 vs λ ≈ 2.4, similar)
- More asymmetric

This higher concentration means:
- The alternating sum has MORE cancellation
- The characteristic function at θ = π is SMALLER

But here's the key question:
    WHY is the distribution more concentrated?

ANSWER: The constraint that n ≤ x restricts which products of primes appear.
- Small primes (2, 3, 5, ...) contribute most to ω(n)
- The first few prime products dominate
- This creates concentration around ω ≈ 2-3

This is the ARITHMETIC STRUCTURE we're looking for!

THE QUESTION BECOMES:
Can we prove this concentration implies |M|/Q = O(1/√x)?

This would require showing:
    Var(ω) ≤ λ - c·λ/log x  for some c > 0

The variance reduction would then give the required cancellation.
""")

# =============================================================================
# PART 9: THE VARIANCE REDUCTION ARGUMENT
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: VARIANCE REDUCTION ARGUMENT")
print("=" * 80)

print("""
PROPOSED PROOF STRATEGY:
========================

STEP 1: Prove Var(ω) < λ for squarefree n ≤ x
        (The distribution is more concentrated than Poisson)

STEP 2: Quantify: Var(ω) = λ - δ(x) where δ(x) > 0

STEP 3: Use concentration to bound |φ(π)|:
        For concentrated distributions, high-frequency Fourier
        coefficients are small.

STEP 4: Conclude |M|/Q = |φ(π)| = O(1/√x)

TESTING STEP 1:
""")

# Test variance reduction across x values
print("\nVariance reduction test:")
print("-" * 60)
print(f"{'x':>10} | {'λ':>8} | {'E[ω]':>8} | {'Var(ω)':>8} | {'Var/λ':>8}")
print("-" * 60)

for x_test in [1000, 2000, 5000, 10000, 20000, 50000, 100000]:
    S_test = get_S_w(x_test)
    Q_test = get_Q(x_test)
    lam_test = np.log(np.log(x_test))

    mean_test = sum(w * S_test.get(w, 0) for w in range(20)) / Q_test
    var_test = sum((w - mean_test)**2 * S_test.get(w, 0) for w in range(20)) / Q_test

    print(f"{x_test:>10} | {lam_test:>8.4f} | {mean_test:>8.4f} | {var_test:>8.4f} | {var_test/lam_test:>8.4f}")

print("""
OBSERVATION:
Var(ω) < λ consistently, with Var/λ ≈ 0.4-0.5

This is significant variance reduction!

The variance is about HALF of what Poisson predicts.
""")

# =============================================================================
# PART 10: THE OBSTRUCTION REMAINS
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: WHY THE OBSTRUCTION REMAINS")
print("=" * 80)

print("""
DESPITE THE PROGRESS, THE OBSTRUCTION REMAINS:
==============================================

We've shown:
1. Var(ω) < λ (concentration)
2. This is consistent with |M|/Q being small
3. The smoothness causes Fourier decay

But we CANNOT prove:
1. That this concentration ALWAYS holds (for all x)
2. That the concentration is ENOUGH to give O(1/√x)
3. That there's no other mechanism making |M| large

THE FUNDAMENTAL PROBLEM:
The variance of ω depends on HOW primes are distributed.
The prime distribution is controlled by ζ zeros.
To prove the variance bound, we need to control the zeros.
We're back to RH.

SPECIFIC OBSTRUCTION:
If there were a zero with β > 1/2, it would create
oscillations in the prime distribution that could
increase Var(ω) at certain x values.
To rule this out, we need to prove there's no such zero.

THE CIRCLE IS UNBROKEN.
""")

# =============================================================================
# PART 11: IS THERE ANY WAY FORWARD?
# =============================================================================

print("\n" + "=" * 80)
print("PART 11: IS THERE ANY WAY FORWARD?")
print("=" * 80)

print("""
POSSIBLE PATHS (all speculative):
=================================

PATH 1: UNIVERSAL VARIANCE BOUND
   Prove: Var(ω) ≤ λ/2 for ALL multiplicative contexts
   This would be a universal principle, not depending on ζ zeros.
   Status: Unknown. Would be major breakthrough.

PATH 2: SELF-IMPROVEMENT ARGUMENT
   If |M(x₀)| > √x₀ for some x₀, derive a contradiction.
   The contradiction could come from:
   - Combinatorial impossibility
   - Functional equation violation
   - Number-theoretic constraint
   Status: No known contradiction mechanism.

PATH 3: HILBERT-PÓLYA OPERATOR
   Find the operator. Prove self-adjointness.
   Status: Open for 100+ years. No candidate found.

PATH 4: RANDOM MATRIX THEORY
   Show ζ zeros statistically match GUE eigenvalues.
   GUE eigenvalues are real → zeros have Re = 1/2.
   Status: Strong numerical evidence but no proof.

PATH 5: ARITHMETIC GEOMETRY
   Find a variety whose cohomology encodes ζ zeros.
   Use Weil conjectures (proven) to constrain zeros.
   Status: This is essentially the Weil conjectures for number fields.
           Major open problem.

HONEST ASSESSMENT:
We don't have a viable path to RH from our framework.
What we have is a REFORMULATION, not a SOLUTION.
""")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("FINAL SUMMARY: DIRECTION C")
print("=" * 80)

print("""
WHAT WE LEARNED:
================

1. THE OBSTRUCTION IS FUNDAMENTAL
   Every path to bounding M(x) requires controlling ζ zeros.
   This is not a technical difficulty - it's a mathematical necessity.

2. THE GENERATING FUNCTION GIVES INSIGHT BUT NOT PROOF
   G(z,x) = Σ S_w z^w reveals structure:
   - Variance reduction: Var(ω) ≈ λ/2 < λ
   - Concentration: distribution is smoother than Poisson
   - Cancellation: |M|/Q = |φ(π)| is small

3. THE VARIANCE REDUCTION IS REAL
   We observe Var(ω)/λ ≈ 0.4-0.5 consistently.
   This explains WHY |M| is small.
   But we cannot PROVE it always holds.

4. THE ZETA ZEROS CONTROL EVERYTHING
   The explicit formula: M(x) = -2 + Σ_ρ x^ρ/(ρζ'(ρ)) + O(1)
   The zeros determine M(x), which determines the S_w distribution.
   Breaking this connection would require entirely new mathematics.

CONCLUSION:
===========
Our generating function approach is a valid REFORMULATION of RH.
It provides new INTUITION for why RH should be true.
It does NOT provide a PATH to proving RH.

The fundamental obstruction - controlling ζ zeros - remains.
""")

print("=" * 80)
print("DIRECTION C COMPLETE")
print("=" * 80)
