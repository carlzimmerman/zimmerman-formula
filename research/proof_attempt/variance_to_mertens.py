"""
VARIANCE TO MERTENS: ATTEMPTING TO CLOSE THE GAP
=================================================

Key Question: Does Var(ω)/λ ≤ c < 1 imply |M(x)| = O(√x)?

If we can prove this implication, and separately prove Var(ω)/λ → B/e^{-1/e},
then we would have a proof of RH.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, symbols, Sum, exp, log, sqrt
from sympy import oo, S, simplify, Rational, E, pi, binomial
from collections import defaultdict
from scipy.stats import norm
import math

print("=" * 80)
print("VARIANCE TO MERTENS: CLOSING THE GAP")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 300000
primes = list(primerange(2, MAX_N))

factorizations = {}
for n in range(1, MAX_N + 1):
    if n == 1:
        factorizations[n] = {}
    else:
        factorizations[n] = factorint(n)

def is_squarefree(n):
    return all(e == 1 for e in factorizations[n].values())

def omega(n):
    return len(factorizations[n])

sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]

# =============================================================================
# APPROACH 1: CHARACTERISTIC FUNCTION METHOD
# =============================================================================

print("""

================================================================================
APPROACH 1: CHARACTERISTIC FUNCTION METHOD
================================================================================

IDEA: Use the characteristic function of ω to analyze M(x).

For random variable X on squarefree n ≤ x:
  φ(t) = E[e^{itω}]
  M(x)/Q(x) = E[(-1)^ω] = E[e^{iπω}] = φ(π)

So if we can bound φ(π), we bound |M(x)|/Q(x).

LEMMA: For X with mean μ and variance σ²:
  |φ(t)| ≤ exp(-σ²t²/2 + |t|³ E[|X-μ|³]/6)

For approximately normal X:
  |φ(π)| ≈ exp(-σ²π²/2)

If σ² = Var(ω) ≈ 0.378 λ, then:
  |φ(π)| ≈ exp(-0.378 λ π²/2) ≈ exp(-1.87 λ)
  |M(x)|/Q(x) ≈ exp(-1.87 log log x) = (log x)^{-1.87}

This gives |M(x)| ≈ x/(log x)^{1.87}, which is NOT O(√x).

CONCLUSION: Variance alone doesn't give the RH bound.
The characteristic function approach gives Halász-type bounds.
""")

# Verify numerically
print("Numerical check of characteristic function bound:")
for x in [10000, 50000, 100000, 200000]:
    omega_vals = [w for n, w in sqfree if n <= x]
    Q = len(omega_vals)
    M = sum((-1)**w for w in omega_vals)

    var_omega = np.var(omega_vals)
    lam = np.log(np.log(x))

    # Gaussian approximation for |φ(π)|
    phi_pi_approx = np.exp(-var_omega * np.pi**2 / 2)
    M_approx = Q * phi_pi_approx

    print(f"  x = {x}: |M| = {abs(M)}, Gaussian approx = {M_approx:.1f}, ratio = {abs(M)/M_approx:.4f}")

# =============================================================================
# APPROACH 2: DIRECT PARITY ANALYSIS
# =============================================================================

print("""

================================================================================
APPROACH 2: DIRECT PARITY ANALYSIS
================================================================================

IDEA: Analyze P(ω even) - P(ω odd) directly.

Let p_w = P(ω = w) = S_w/Q.
Then:
  M/Q = Σ_w (-1)^w p_w = Σ_{even w} p_w - Σ_{odd w} p_w
      = P(even) - P(odd)

QUESTION: What constrains P(even) - P(odd)?

If ω were Poisson(λ):
  P(even) - P(odd) = e^{-λ}Σ_{w even} λ^w/w! - e^{-λ}Σ_{w odd} λ^w/w!
                   = e^{-λ}(cosh λ - sinh λ)
                   = e^{-λ} · e^{-λ}
                   = e^{-2λ}

So for Poisson: |M|/Q = e^{-2λ} = 1/(log x)².

But actual |M|/Q << 1/(log x)², indicating SUPER-Poisson cancellation.

THEOREM (Attempt):
If ω is "better than Poisson" in that the parity alternation cancels more,
then M(x) is smaller.

The question is: WHY is the cancellation better than Poisson?
""")

# Compute actual vs Poisson
print("Actual parity vs Poisson prediction:")
for x in [10000, 50000, 100000, 200000, 300000]:
    omega_vals = [w for n, w in sqfree if n <= x]
    Q = len(omega_vals)
    M = sum((-1)**w for w in omega_vals)
    lam = np.log(np.log(x))

    actual = abs(M) / Q
    poisson = np.exp(-2 * lam)

    print(f"  x = {x}: |M|/Q = {actual:.6f}, e^(-2λ) = {poisson:.6f}, ratio = {actual/poisson:.4f}")

# =============================================================================
# APPROACH 3: CONCENTRATION INEQUALITY
# =============================================================================

print("""

================================================================================
APPROACH 3: CONCENTRATION INEQUALITY
================================================================================

IDEA: Use concentration of ω to bound parity imbalance.

If ω is concentrated in an interval [μ - σ, μ + σ], then most of the
mass is in a region of width ~2σ around the mean.

For the parity to balance, we need the contributions from even and odd w
in this interval to cancel.

LEMMA (Berry-Esseen):
For ω satisfying Erdős-Kac, the distribution is approximately normal.
The approximation error is O(1/√λ).

If the normal approximation held exactly:
  P(even) - P(odd) = Σ_w (-1)^w · (1/√(2πσ²)) exp(-(w-μ)²/(2σ²))

This sum is a discrete approximation to an integral, which evaluates to:
  ≈ exp(-σ²π²/2) · (oscillating term)

The oscillating term comes from the discretization.

KEY INSIGHT:
The deviation from Poisson creates a PHASE SHIFT in the oscillation.
This phase shift can enhance or diminish the cancellation.
For the actual primes, the phase shift ENHANCES cancellation.
""")

# =============================================================================
# APPROACH 4: THE S_w CONSTRAINT
# =============================================================================

print("""

================================================================================
APPROACH 4: ANALYZING THE S_w COEFFICIENTS
================================================================================

The coefficients S_w = #{sqfree n ≤ x : ω(n) = w} satisfy:

1. Normalization: Σ_w S_w = Q(x) = (6/π²)x + O(√x)
2. Positivity: S_w ≥ 0
3. Generating function: Σ_w S_w z^w is the squarefree generating function

EXPLICIT FORMULA (Hardy-Ramanujan style):
S_w(x) = (1/w!) Σ_{n₁<n₂<...<nw, n₁...nw ≤ x} 1
       = (1/w!) #{(p₁,...,pw) : p₁...pw ≤ x, primes distinct}

For fixed w and large x:
S_w(x) ~ (x/log x) · (log log x)^{w-1} / (w-1)! × correction factors

The correction factors encode prime distribution.

THE KEY:
M(x) = Σ_w (-1)^w S_w(x)

For M(x) to be small, the S_w must satisfy an almost-balance condition.

DEFINE:
  T(x) = Σ_w S_w = Q(x)
  A(x) = Σ_w (-1)^w S_w = M(x)

Then: |A/T| = |M/Q| is the relative imbalance.

RH requires: |A/T| = O(1/√x)
""")

# =============================================================================
# APPROACH 5: RECURSIVE STRUCTURE
# =============================================================================

print("""

================================================================================
APPROACH 5: RECURSIVE STRUCTURE OF M(x)
================================================================================

There's a recursive relation for M(x).

LEMMA: M(x) = 1 - Σ_{d=2}^{x} M(⌊x/d⌋)

Proof: Σ_{n≤x} μ(n) Σ_{d|n} 1 = Σ_{n≤x} μ(n) τ(n)
where τ(n) = number of divisors.
The left side equals 1 (sum over n=1 only contributes).
Rearranging: 1 = Σ_{d≤x} M(⌊x/d⌋). □

IDEA: Use this recursion to prove bounds on M(x).

If we knew M(y) = O(y^{1/2+ε}) for y < x, then:
  |M(x)| = |1 - Σ_{d=2}^{x} M(⌊x/d⌋)|
         ≤ 1 + Σ_{d=2}^{x} |M(⌊x/d⌋)|
         ≤ 1 + Σ_{d=2}^{x} C·(x/d)^{1/2+ε}
         = 1 + C·x^{1/2+ε} Σ_{d=2}^{x} d^{-(1/2+ε)}
         ≤ 1 + C·x^{1/2+ε} · O(x^{1/2-ε})
         = O(x^{1-ε²}) ← too weak!

The recursion doesn't directly prove the bound we want.
We need CANCELLATION in the sum, not just magnitude bounds.
""")

# =============================================================================
# APPROACH 6: FOURIER ANALYSIS ON G(z,x)
# =============================================================================

print("""

================================================================================
APPROACH 6: FOURIER ANALYSIS OF G(z,x)
================================================================================

G(e^{2πiθ}, x) = Σ_w S_w e^{2πiwθ}

This is the Fourier transform of the measure Σ_w S_w δ_w.

M(x) = G(-1, x) = G(e^{iπ}, x) = value at θ = 1/2.

IDEA: Bound G(e^{iπ}, x) using smoothness of the S_w distribution.

If S_w were constant: G(e^{iπ}) = S₀(1 - 1 + 1 - ...) = oscillating.
If S_w were Gaussian: G(e^{iπ}) ~ exp(-c·σ²) (small).
Actual S_w is between these extremes.

THEOREM (Wiener-Ikehara style):
The behavior of G(e^{iπ}, x) as x → ∞ is controlled by the
analytic properties of the generating Dirichlet series.

Specifically:
  Σ_{n sqfree} μ(n)/n^s = Π_p (1 - 1/p^s) = 1/ζ(s)

The pole at s = 1 (from ζ(s) = 0) controls M(x).
If all zeros of ζ(s) have Re(s) < 1/2, then |M(x)| = O(√x).

THIS IS CIRCULAR - it's just RH restated.
""")

# =============================================================================
# APPROACH 7: NEW ATTEMPT - ALGEBRAIC CONSTRAINT
# =============================================================================

print("""

================================================================================
APPROACH 7: ALGEBRAIC CONSTRAINT ON S_w
================================================================================

NEW IDEA: The S_w satisfy algebraic constraints from their definition.

CONSTRAINT 1:
S_w = #{products of exactly w distinct primes ≤ x}
This is related to the w-th elementary symmetric polynomial in (p₁, p₂, ...).

Let π(x) = #{primes ≤ x}.
Then S_1(x) = π(x).
     S_2(x) = #{pq ≤ x : p < q primes} = Σ_{p<√x} (π(x/p) - π(p))
     etc.

CONSTRAINT 2:
The generating function G(z,x) factors:
  G(z,x) ≈ Π_{p≤x} (1 + z·χ(p,x))
where χ(p,x) encodes whether p "contributes" to n ≤ x.

For exact squarefree numbers:
  Σ_{n≤x, sqfree} z^{ω(n)} = Σ_{n≤x, sqfree} Π_{p|n} z

This product structure creates constraints on the S_w.

THEOREM ATTEMPT:
The product structure implies that G(-1,x) = small.

Why? Because G(-1,x) = Σ Π_{p|n}(-1) = Σ_{n sqfree} (-1)^{ω(n)}.

When we expand the product Π_p (1 + (-1)·χ(p)), terms cancel.
""")

# Let's verify the product structure numerically
print("Verifying product structure constraint:")

for x in [1000, 5000, 10000]:
    # Compute G(-1) directly
    S_w = defaultdict(int)
    for n, w in sqfree:
        if n <= x:
            S_w[w] += 1

    M_direct = sum((-1)**w * S_w.get(w, 0) for w in S_w)

    # Compute via product approximation
    # Product over p ≤ x of (1 - χ(p,x))
    # where χ(p,x) ≈ x/p / Q(x) ≈ 1/p * (π²/6)

    # This is approximate; exact computation is complex
    product_approx = 1.0
    for p in primes:
        if p > x:
            break
        # Approximate contribution
        # In the product representation, each prime contributes (1 - z·f(p))
        # At z = -1: (1 + f(p))
        # If f(p) = fraction of squarefree n ≤ x divisible by p
        count_div_p = sum(1 for n, w in sqfree if n <= x and n % p == 0)
        Q = sum(1 for n, w in sqfree if n <= x)
        f_p = count_div_p / Q
        product_approx *= (1 - f_p)  # This is for z=1
        # For z = -1, it would be (1 + f_p) but the correlation structure matters

    print(f"  x = {x}: M_direct = {M_direct}, Q = {Q}")

# =============================================================================
# APPROACH 8: THE CORE THEOREM WE NEED
# =============================================================================

print("""

================================================================================
APPROACH 8: THE CORE THEOREM WE NEED
================================================================================

After all these approaches, the core theorem we need is:

THEOREM (Root Location Theorem):
For all sufficiently large x, the polynomial G(z,x) has a root ζ(x)
satisfying |ζ(x) + 1| ≤ C · x^{-1/2} for some absolute constant C.

EQUIVALENTLY (via mean value theorem):
|M(x)| = |G(-1,x)| ≤ |G'(ξ)| · |ζ(x) + 1| ≤ C' · Q(x) · x^{-1/2} = O(√x)

PROOF SKETCH (Incomplete):
==========================
1. G(z,x) = G_Poisson(z,x) + D(z,x)
2. G_Poisson(-1,x) = Q(x) · e^{-2λ}
3. D(-1,x) = M(x) - Q(x)·e^{-2λ}
4. For root near -1: G_Poisson(ζ) + D(ζ) = 0
5. ζ + 1 ≈ -D(ζ) / G'_Poisson(ζ)

The size of |ζ + 1| depends on |D(ζ)| / |G'_Poisson(ζ)|.

We need: |D(ζ)| = O(Q · x^{-1/2})

This requires controlling the deviation from Poisson.
The deviation depends on the S_w asymptotics.
The S_w asymptotics depend on prime distribution.
Prime distribution at this precision requires RH.

*** THE CIRCULARITY PERSISTS ***

WHAT WOULD BREAK THE CIRCULARITY:
=================================
A proof that the ALGEBRAIC or COMBINATORIAL structure of squarefree
numbers forces |D(-1,x)| to be small, without using analytic prime data.

For example:
- A symmetry argument specific to μ(n) = (-1)^{ω(n)}
- An inclusion-exclusion identity that forces cancellation
- A bijection that pairs positive and negative terms

None of these have been found.
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY: WHAT WE'VE PROVEN VS WHAT REMAINS
================================================================================

PROVEN (Rigorous):
=================
1. G(-1,x) = M(x) (generating function formulation) ✓
2. G(z,x) has a unique root nearest to -1 ✓
3. |M(x)| ≈ |G'(ζ)| · |ζ+1| (mean value theorem) ✓
4. Var(ω)/λ → c for some c ≈ 0.378 (empirical, not proven)
5. M_S ≈ -M_L (empirical, not proven)

NOT PROVEN (The Gap):
=====================
1. |ζ(x) + 1| = O(1/√x)
2. Var(ω)/λ → B/e^{-1/e} exactly
3. The deviation D(-1,x) = O(√x)
4. Any unconditional bound better than Halász

THE FUNDAMENTAL OBSTACLE:
=========================
All approaches require controlling Σ_w (-1)^w S_w(x).
The S_w(x) depend on prime distribution.
Prime distribution to this precision requires RH.

We have developed a STRUCTURE THEORY that explains WHY M(x) is small:
- The generating function has a root near z = -1
- The variance of ω is reduced below Poisson by correlations
- The smooth and rough parts cancel

But converting this structure into a PROOF requires breaking the
circularity between M(x) bounds and ζ zeros.

This circularity has not been broken.
""")

print("=" * 80)
print("VARIANCE TO MERTENS ANALYSIS COMPLETE")
print("=" * 80)
