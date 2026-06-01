"""
SYMMETRY AND BIJECTION APPROACH
================================

The function f(p) = -1 for all primes creates MAXIMUM SYMMETRY.
f(n) = (-1)^ω(n) depends ONLY on the number of prime factors, not which ones.

Can we exploit this symmetry to prove cancellation?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
from itertools import combinations
import math

print("=" * 80)
print("SYMMETRY AND BIJECTION APPROACH")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 100000
primes = list(primerange(2, MAX_N))
primes_set = set(primes)

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

def prime_factors(n):
    return set(factorizations[n].keys())

sqfree = [(n, omega(n)) for n in range(1, MAX_N + 1) if is_squarefree(n)]

# =============================================================================
# BIJECTION ATTEMPT 1: PAIRING BY ADDING A PRIME
# =============================================================================

print("""

================================================================================
BIJECTION ATTEMPT 1: PAIRING BY ADDING/REMOVING A PRIME
================================================================================

IDEA: Try to pair squarefree n with (-1)^ω(n) = +1
      against squarefree m with (-1)^ω(m) = -1.

If n is squarefree with ω(n) = w (even), we want a bijection to some m
with ω(m) = w+1 or w-1 (odd).

ATTEMPT: For each squarefree n, pair it with np for the smallest prime p ∤ n
such that np ≤ x.

PROBLEM: This isn't a bijection because:
1. Different n may pair to the same np
2. Some np may exceed x
3. The boundary effects are significant
""")

def attempt_bijection_1(x):
    """Try to pair squarefree numbers by adding a prime."""
    even_omega = [(n, w) for n, w in sqfree if n <= x and w % 2 == 0]
    odd_omega = [(n, w) for n, w in sqfree if n <= x and w % 2 == 1]

    # Try to pair each even-ω number with an odd-ω number
    paired_even = set()
    paired_odd = set()
    pairs = []

    for n, w in even_omega:
        # Find smallest prime not dividing n
        pf = prime_factors(n)
        for p in primes:
            if p not in pf and n * p <= x:
                m = n * p
                if is_squarefree(m) and m not in paired_odd:
                    pairs.append((n, m))
                    paired_even.add(n)
                    paired_odd.add(m)
                    break

    n_even = len(even_omega)
    n_odd = len(odd_omega)
    n_paired = len(pairs)

    print(f"At x = {x}:")
    print(f"  Even-ω numbers: {n_even}")
    print(f"  Odd-ω numbers: {n_odd}")
    print(f"  Successfully paired: {n_paired}")
    print(f"  Unpaired even: {n_even - n_paired}")
    print(f"  Unpaired odd: {n_odd - n_paired}")
    print(f"  M(x) = even - odd = {n_even - n_odd}")

    return n_even - n_paired, n_odd - n_paired

for x in [1000, 5000, 10000]:
    attempt_bijection_1(x)
    print()

# =============================================================================
# BIJECTION ATTEMPT 2: INVOLUTION ON PRODUCTS
# =============================================================================

print("""

================================================================================
BIJECTION ATTEMPT 2: INVOLUTION ON FACTORIZATIONS
================================================================================

IDEA: Define an involution σ on squarefree n such that ω(σ(n)) = ω(n) ± 1.

For most n, σ(n) ≠ n, so they cancel.
M(x) = # fixed points of σ within [1,x].

CHALLENGE: Defining σ consistently.

ATTEMPT: For n = p₁p₂...p_w, define σ(n) based on lexicographic
ordering of prime factors.

Let's try: σ(n) = n · q / p where p is the largest prime factor
and q is the smallest prime NOT dividing n.

This would give ω(σ(n)) = ω(n) (same) unless q or p creates boundary issues.
""")

def attempt_involution(x):
    """Try to define an involution that swaps parity."""
    # For each squarefree n, try to pair with another

    numbers = [n for n, w in sqfree if n <= x]
    contributions = {n: (-1)**omega(n) for n in numbers}

    # Try: n → n × (smallest new prime) / (largest current prime)
    # This keeps ω the same, so doesn't help.

    # Alternative: n → n × (smallest new prime) if that's ≤ x
    #              n → n / (smallest current prime) if n is composite

    paired = set()
    for n in numbers:
        if n in paired:
            continue

        pf = sorted(prime_factors(n))

        # If n = 1, no prime factors, so we can't remove
        # Try to add the smallest prime
        if len(pf) == 0:  # n = 1
            for p in primes:
                if p <= x:
                    m = p
                    if m in contributions and m not in paired:
                        paired.add(1)
                        paired.add(m)
                        break
            continue

        # For n > 1, try to pair with n/p₁ where p₁ is smallest factor
        p1 = pf[0]
        m = n // p1
        if m > 0 and m in contributions and m not in paired:
            # This pairs n (ω = w) with m (ω = w-1)
            # contributions[n] + contributions[m] = (-1)^w + (-1)^{w-1} = 0
            paired.add(n)
            paired.add(m)
            continue

    # Count unpaired
    unpaired = [n for n in numbers if n not in paired]
    M_from_unpaired = sum(contributions[n] for n in unpaired)

    print(f"At x = {x}:")
    print(f"  Total squarefree: {len(numbers)}")
    print(f"  Paired (cancel): {len(paired)}")
    print(f"  Unpaired: {len(unpaired)}")
    print(f"  M from unpaired: {M_from_unpaired}")
    print(f"  Actual M(x): {sum(contributions.values())}")

for x in [1000, 5000, 10000]:
    attempt_involution(x)
    print()

# =============================================================================
# BIJECTION ATTEMPT 3: SWAPPING TWO PRIMES
# =============================================================================

print("""

================================================================================
BIJECTION ATTEMPT 3: LOCAL PRIME SWAPS
================================================================================

IDEA: For n = p₁p₂...p_w, define a "swap" operation.

OBSERVATION: If we swap prime pᵢ for prime q (not in factorization),
we get m = n × q / pᵢ.

ω(m) = ω(n) (unchanged), so this doesn't help with parity.

WHAT WOULD HELP:
We need an operation that changes ω by 1 (add or remove a prime).

The problem is that adding a prime p to n gives np, which may exceed x.
And removing a prime from n requires n to have that prime factor.

BOUNDARY EFFECTS:
The reason M(x) ≠ 0 is precisely these boundary effects:
- Numbers near x may not have a "partner" within x
- The primes near √x create imbalance

These boundary effects accumulate to give |M(x)| ~ √x.
""")

# =============================================================================
# PARTIAL BIJECTION ANALYSIS
# =============================================================================

print("""

================================================================================
PARTIAL BIJECTION ANALYSIS
================================================================================

Let's analyze WHERE the pairing fails.

For each squarefree n with ω(n) = w, define its "partner" as:
  - If w is even: partner(n) = n × (smallest prime not dividing n)
  - If w is odd: partner(n) = n / (largest prime dividing n)

Count: How many n have partner(n) ≤ x vs > x?
""")

def analyze_pairing_failure(x):
    """Analyze where pairing fails."""
    even_success = 0  # Even-ω with partner ≤ x
    even_fail = 0     # Even-ω with partner > x
    odd_success = 0
    odd_fail = 0

    for n, w in sqfree:
        if n > x:
            break

        pf = sorted(prime_factors(n))

        if w % 2 == 0:  # Even ω - try to add a prime
            # Find smallest prime not dividing n
            partner = None
            for p in primes:
                if p not in pf:
                    partner = n * p
                    break

            if partner is not None and partner <= x:
                even_success += 1
            else:
                even_fail += 1

        else:  # Odd ω - try to remove a prime
            if len(pf) > 0:
                largest_p = pf[-1]
                partner = n // largest_p
                if partner >= 1:
                    odd_success += 1
                else:
                    odd_fail += 1
            else:
                odd_fail += 1

    print(f"At x = {x}:")
    print(f"  Even-ω with partner ≤ x: {even_success}")
    print(f"  Even-ω with partner > x: {even_fail}")
    print(f"  Odd-ω with partner ≤ x: {odd_success}")
    print(f"  Odd-ω with partner > x: {odd_fail}")
    print(f"  Net imbalance from failures: {even_fail - odd_fail}")

    # The actual M(x)
    S_w = defaultdict(int)
    for n, w in sqfree:
        if n <= x:
            S_w[w] += 1
    M = sum((-1)**w * S_w[w] for w in S_w)
    print(f"  Actual M(x): {M}")

    return even_fail, odd_fail

for x in [1000, 5000, 10000, 50000]:
    analyze_pairing_failure(x)
    print()

# =============================================================================
# KEY INSIGHT
# =============================================================================

print("""

================================================================================
KEY INSIGHT FROM BIJECTION ANALYSIS
================================================================================

The pairing failure comes from BOUNDARY EFFECTS:

1. For even-ω numbers n near x, the partner np > x.
   These contribute +1 to M(x) without cancellation.

2. For odd-ω numbers, removing a prime always gives partner ≤ n ≤ x.
   So odd numbers mostly find partners.

3. The imbalance is:
   # of even-ω numbers whose partner exceeds x
   MINUS
   # of odd-ω numbers without partners

THEOREM (Informal):
M(x) ≈ #{even-ω squarefree n ≤ x : n × (smallest new prime) > x}

These are the even-ω numbers n where n × 2 > x (if 2 ∤ n)
                              or n × 3 > x (if 2|n, 3 ∤ n)
                              etc.

For n in (x/2, x], 2|n means we look at n×3 > x, i.e., n > x/3.
So the "unpaired even" numbers are concentrated in (x/2, x].

This is a band of width x/2, containing ~ (6/π²)(x/2) = 3x/π² numbers.
Half are even-ω, half odd-ω.
But the even-ω ones may lack partners while odd-ω ones have partners.

The NET imbalance is ~ √x from fluctuations in this boundary region.

THIS EXPLAINS THE √x BEHAVIOR but doesn't prove it rigorously.
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY: BIJECTION APPROACH
================================================================================

FINDINGS:
=========
1. Perfect bijection between even-ω and odd-ω is impossible
   due to boundary effects.

2. The "failed pairings" occur for large n near x.

3. The number of failures is related to primes and their products
   near the boundary x.

4. This gives an intuitive explanation for |M(x)| ~ √x
   (fluctuations in the boundary region).

WHAT'S MISSING:
===============
A rigorous argument that the boundary failures sum to O(√x).

The boundary region (x/2, x] has ~x/2 squarefree numbers.
The fluctuation in their parity balance is the key.
By Erdős-Kac, ω is normally distributed, suggesting balance.
But the EXACT balance requires prime distribution data.

CONCLUSION:
===========
The bijection approach provides intuition but not a proof.
The boundary effects encode the same information as ζ zeros.
""")

print("=" * 80)
print("BIJECTION ANALYSIS COMPLETE")
print("=" * 80)
