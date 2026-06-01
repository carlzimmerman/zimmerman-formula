"""
RADICAL APPROACH: HIDDEN STRUCTURE IN THE MÖBIUS FUNCTION
==========================================================

Looking for deep structure that might lead to a proof.

Key idea: The Möbius function has multiplicative structure.
Can we exploit this in a new way?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, Matrix, symbols, simplify
from sympy import gcd as sym_gcd, lcm as sym_lcm
from collections import defaultdict
import math

print("=" * 80)
print("RADICAL APPROACH: HIDDEN STRUCTURE")
print("=" * 80)

# =============================================================================
# IDEA 1: THE DIRICHLET SERIES PERSPECTIVE
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 1: DIRICHLET SERIES AND EULER PRODUCTS")
print("=" * 80)

print("""
THE FUNDAMENTAL IDENTITY:
=========================

1/ζ(s) = Σ_{n=1}^∞ μ(n)/n^s = Π_p (1 - 1/p^s)

This converges for Re(s) > 1.

At s = 1: The product Π_p (1 - 1/p) diverges (to 0).
         By Mertens: Π_{p≤x} (1 - 1/p) ~ e^{-γ}/log(x)

The PARTIAL SUMS are what interest us:
  M(x) = Σ_{n≤x} μ(n)

IDEA: Can we relate M(x) to partial Euler products?
""")

# Compute partial Euler products
primes = list(primerange(2, 1000))

def partial_euler_product(y, s=1):
    """Π_{p≤y} (1 - 1/p^s)"""
    product = 1.0
    for p in primes:
        if p > y:
            break
        product *= (1 - 1/(p**s))
    return product

print("\nPartial Euler products Π_{p≤y} (1 - 1/p):")
print("-" * 50)

for y in [10, 100, 1000]:
    prod = partial_euler_product(y)
    mertens = np.exp(-0.5772156649) / np.log(y)  # Mertens approximation
    print(f"  y = {y:>5}: Product = {prod:.6f}, Mertens = {mertens:.6f}")

# =============================================================================
# IDEA 2: THE CONVOLUTION STRUCTURE
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 2: CONVOLUTION STRUCTURE")
print("=" * 80)

print("""
DIRICHLET CONVOLUTION:
======================

The Möbius function is the inverse of the constant function 1:
  μ * 1 = ε  (where ε(1) = 1, ε(n) = 0 for n > 1)

This means: Σ_{d|n} μ(d) = ε(n)

CONVOLUTION WITH OTHER FUNCTIONS:
=================================
μ * log = -Λ (von Mangoldt)
μ * τ = 1   (τ = divisor count, 1 = identity for convolution)

IDEA: Study the "algebra" of Dirichlet convolution.
Can algebraic properties give us bounds?
""")

# The convolution algebra is a ring
# Can we find "norm" structures that give bounds?

# =============================================================================
# IDEA 3: THE INCIDENCE MATRIX
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 3: THE INCIDENCE MATRIX")
print("=" * 80)

print("""
THE DIVISIBILITY MATRIX:
========================

Define A_ij = 1 if i | j, else 0.

Then the inverse of A (in the Boolean algebra sense) involves μ!

Specifically: (A^{-1})_ij = μ(j/i) if i | j, else 0.

MATRIX INTERPRETATION:
======================
M(x) = Σ μ(n) = sum of first row of certain matrix power?

Let's explore this...
""")

def build_divisibility_matrix(n):
    """Build the n×n divisibility matrix."""
    A = np.zeros((n, n))
    for i in range(1, n+1):
        for j in range(1, n+1):
            if j % i == 0:
                A[i-1, j-1] = 1
    return A

# Small example
n = 10
A = build_divisibility_matrix(n)
print(f"\nDivisibility matrix A for n = {n}:")
print(A.astype(int))

# The inverse should involve Möbius function
print("\nA^{-1} (should involve μ):")
A_inv = np.linalg.inv(A)
print(np.round(A_inv, 2))

# =============================================================================
# IDEA 4: POLYNOMIAL FACTORIZATION
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 4: POLYNOMIAL FACTORIZATION")
print("=" * 80)

print("""
THE GENERATING POLYNOMIAL:
==========================

Consider: P(z) = Σ_{n≤x} μ(n) z^n

This is a polynomial of degree x.

FACTORIZATION:
==============
P(z) factors as P(z) = Σ μ(n) z^n

At z = 1: P(1) = M(x)

Can we understand P(z) through its roots?

ROOTS OF P(z):
==============
Where does P(z) = 0?
If z₀ is a root, then Σ μ(n) z₀^n = 0.
""")

# Compute P(z) for small x
def mobius_polynomial(x_max, z):
    """Evaluate P(z) = Σ_{n≤x} μ(n) z^n"""
    # First compute μ
    mu_local = [0] * (x_max + 1)
    mu_local[1] = 1
    for n in range(2, x_max + 1):
        factors = factorint(n)
        if any(e > 1 for e in factors.values()):
            mu_local[n] = 0
        else:
            mu_local[n] = (-1) ** len(factors)

    total = 0
    for n in range(1, x_max + 1):
        total += mu_local[n] * (z ** n)
    return total

# Find where P(z) = 0 on the unit circle
print("\nSearching for roots of P(z) on unit circle (x = 100):")
x_test = 100
for theta in np.linspace(0, 2*np.pi, 37):
    z = np.exp(1j * theta)
    P_z = mobius_polynomial(x_test, z)
    if abs(P_z) < 5:  # Close to zero
        print(f"  θ = {theta:.4f}: |P(e^{{iθ}})| = {abs(P_z):.4f}")

# =============================================================================
# IDEA 5: THE PRIME SIEVE STRUCTURE
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 5: PRIME SIEVE STRUCTURE")
print("=" * 80)

print("""
THE INCLUSION-EXCLUSION PRINCIPLE:
==================================

Q(x) = Σ_{d²≤x} μ(d) · floor(x/d²)

This is an EXACT formula for squarefree count!

STRUCTURE:
==========
- We include all n ≤ x: x terms
- We exclude those divisible by 4: -x/4 terms
- We exclude those divisible by 9: -x/9 terms
- We include those divisible by 36: +x/36 terms (overcounted)
- ...

The pattern is controlled by μ!

OBSERVATION:
============
M(x) = #{n ≤ x : μ(n) = +1} - #{n ≤ x : μ(n) = -1}
     = 2·Q_even(x) - Q(x)
     = Q_even(x) - Q_odd(x)

We already knew this...
""")

# =============================================================================
# IDEA 6: QUADRATIC FORMS CONNECTION
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 6: QUADRATIC FORMS")
print("=" * 80)

print("""
QUADRATIC FORM CONNECTION:
==========================

Consider the quadratic form:
  Q_x(a, b) = Σ_{m,n≤x} μ(m)μ(n) δ(gcd(m,n) = 1)

This counts coprime pairs weighted by μ.

RELATION TO M(x):
=================
M(x)² = (Σ μ(n))² = Σ_{m,n} μ(m)μ(n)

The diagonal m = n contributes Q(x) (since μ(n)² = 1 for squarefree n, 0 otherwise).

The off-diagonal terms Σ_{m≠n} μ(m)μ(n) = M(x)² - Q(x).

For RH, we need M(x)² = O(x^{1+ε}), i.e., M(x)² - Q(x) = O(x^{1+ε}) - O(x) = O(x).

This is automatic from M(x)² = O(x).
""")

# =============================================================================
# IDEA 7: THE PRIME GAP STRUCTURE
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 7: PRIME GAP ANALYSIS")
print("=" * 80)

print("""
PRIME GAPS AND M(x):
====================

Between primes p and the next prime q, the numbers are:
p+1, p+2, ..., q-1 (all composite)
q (prime)

For these numbers:
- μ(p+1), μ(p+2), ... have various values
- μ(q) = -1

QUESTION: Does the structure of prime gaps affect M(x)?

OBSERVATION:
============
Large gaps would mean many composites in a row.
The μ values of composites depend on their factorizations.

If gaps are random-ish, the μ values might cancel.
If gaps have structure, it might affect M(x).
""")

# Compute M(x) growth near prime gaps
primes_small = list(primerange(2, 1000))
gaps = [(primes_small[i+1] - primes_small[i], primes_small[i])
        for i in range(len(primes_small)-1)]
gaps.sort(reverse=True)

print("\nLargest prime gaps up to 1000:")
for gap, p in gaps[:5]:
    print(f"  Gap of {gap}: between {p} and {p+gap}")

# =============================================================================
# IDEA 8: RECURSIVE STRUCTURE
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 8: RECURSIVE STRUCTURE")
print("=" * 80)

print("""
RECURSIVE FORMULA FOR M(x):
===========================

M(x) = 1 - Σ_{d=2}^{√x} M(floor(x/d²))

This comes from: Σ_{d²|n} μ(d) = indicator(n is squarefree)

Summing over n ≤ x:
Q(x) = Σ_{d²≤x} M(floor(x/d²))

Rearranging:
M(x) = Q(x) - Σ_{d=2}^{√x} M(floor(x/d²))

Since Q(x) = 1 + Σ_{d≥1} M(floor(x/d²)) (d=1 term is M(x)):
M(x) = 1 + Σ_{d=2} M(x/d²) - Σ_{d=2} M(x/d²)

Wait, that's not quite right. Let me reconsider...

CORRECT IDENTITY:
=================
Σ_{d=1}^{√x} M(x/d²) = 1

This is because Σ_{d²|n, d≤√n} μ(d) = [n is squarefree],
and summing the LHS over n gives Σ_d M(x/d²),
while summing the RHS gives Q(x).

Hmm, this still doesn't give the right formula...
""")

# Let's verify numerically
def M(x, cache={}):
    """Compute M(x) with caching."""
    if x < 1:
        return 0
    x = int(x)
    if x in cache:
        return cache[x]
    # Direct computation for small x
    if x <= 10000:
        result = sum(mu[n] for n in range(1, x+1) if n <= MAX_N)
    else:
        result = sum(mu[n] for n in range(1, min(x+1, MAX_N+1)))
    cache[x] = result
    return result

# Precompute mu
MAX_N = 100000
mu = [0] * (MAX_N + 1)
mu[1] = 1
for n in range(2, MAX_N + 1):
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        mu[n] = 0
    else:
        mu[n] = (-1) ** len(factors)

x = 1000
sum_Md2 = sum(M(x // (d*d)) for d in range(1, int(np.sqrt(x)) + 1))
print(f"\nVerifying: Σ_{{d=1}}^{{√{x}}} M({x}/d²) = {sum_Md2}")
print("(Should equal 1 if the identity holds)")

# =============================================================================
# IDEA 9: PRIME FACTORIZATION TREES
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 9: PRIME FACTORIZATION TREES")
print("=" * 80)

print("""
VISUALIZATION APPROACH:
=======================

Every squarefree n corresponds to a SUBSET of primes {p₁, ..., p_k}.

The set of all squarefree n ≤ x is a downward-closed set in the
lattice of subsets of primes (ordered by product ≤ x).

M(x) is an alternating sum over this structure!

LATTICE STRUCTURE:
==================
- Empty set {} → n = 1, μ = +1
- Singletons {p} → n = p, μ = -1
- Pairs {p,q} → n = pq, μ = +1
- ...

The alternating sign comes from the lattice level!
""")

# =============================================================================
# IDEA 10: WHAT IF WE COULD PROVE A WEAKER BOUND?
# =============================================================================

print("\n" + "=" * 80)
print("IDEA 10: WEAKER BOUNDS APPROACH")
print("=" * 80)

print("""
STRATEGY: Prove progressively stronger bounds.

KNOWN BOUNDS:
=============
- M(x) = O(x) [trivial]
- M(x) = o(x) [equivalent to PNT, proved 1896]
- M(x) = O(x exp(-c√(log x))) [current best unconditional]

TO PROVE RH:
============
- M(x) = O(x^{1/2+ε}) for all ε > 0

THE GAP:
========
Between O(x exp(-c√(log x))) and O(x^{1/2+ε}) is HUGE.

Can we prove ANY intermediate bound?

For example:
- M(x) = O(x^{0.99})?  Not known unconditionally!
- M(x) = O(x / log x)? Yes, follows from PNT.
- M(x) = O(x / (log x)²)? Not known!

The current bounds use zero-free regions of ζ(s).
Improving them requires wider zero-free regions.
""")

# =============================================================================
# FINAL RADICAL IDEA
# =============================================================================

print("\n" + "=" * 80)
print("FINAL RADICAL IDEA: SELF-REFERENCE")
print("=" * 80)

print("""
SELF-REFERENTIAL STRUCTURE:
===========================

The Möbius function μ satisfies:
  Σ_{d|n} μ(d) = [n = 1]

This is a SELF-CONSISTENCY condition.

OBSERVATION:
============
If there were a zero ρ with Re(ρ) > 1/2, then:
- M(x) would oscillate with amplitude ~x^{Re(ρ)}
- This would affect the Möbius sum Σ μ(d)
- But the sum must equal exactly 0 or 1!

QUESTION:
=========
Can this self-consistency force Re(ρ) ≤ 1/2?

CHALLENGE:
==========
The self-consistency holds for FINITE sums.
The zeros affect the PARTIAL sums M(x) = Σ_{n≤x} μ(n),
not the complete Möbius sum Σ_{d|n} μ(d).

The partial sums can oscillate arbitrarily (in principle)
while the complete sums remain exactly 0 or 1.

CONCLUSION:
===========
The self-referential structure is beautiful but doesn't
directly constrain the zeros.
""")

print("\n" + "=" * 80)
print("SYNTHESIS: RADICAL APPROACHES")
print("=" * 80)

print("""
SUMMARY:
========

1. DIRICHLET SERIES: Euler products diverge at s=1, can't directly bound M(x)

2. CONVOLUTION: Algebraic structure is clean but doesn't give analytic bounds

3. INCIDENCE MATRIX: Matrix inverse involves μ, but doesn't help with sums

4. POLYNOMIALS: P(z) = Σμ(n)z^n has complex structure, roots unclear

5. SIEVE METHODS: Inclusion-exclusion is exact but leads back to counting

6. QUADRATIC FORMS: M(x)² involves pair correlations, no new insight

7. PRIME GAPS: Gap structure affects μ values but irregularly

8. RECURSION: Recursive formula exists but requires controlling M(x/d²)

9. LATTICE STRUCTURE: Beautiful picture but no proof method

10. WEAKER BOUNDS: Huge gap between known and RH bounds

RADICAL CONCLUSION:
===================
Every approach we've tried - standard and radical - leads to
one of these outcomes:

A) Reduces to controlling ζ zeros (circular)
B) Requires independence we don't have
C) Gives reformulation but not proof
D) Hits an algebraic wall

The Riemann Hypothesis appears to require genuinely NEW mathematics.
Ideas that don't exist yet.

We've pushed our generating function framework to its limits.
It provides beautiful insights but not a proof.
""")

print("=" * 80)
print("RADICAL APPROACH ANALYSIS COMPLETE")
print("=" * 80)
