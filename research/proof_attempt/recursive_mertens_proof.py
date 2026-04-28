"""
RECURSIVE MERTENS PROOF ATTEMPT
================================

Key Identity Discovered:
M(y) = M_p(y) - M_p(y/p)  for any prime p

where M_p(y) = Mertens restricted to n with p ∤ n

This gives:
M_p(y) = M(y) + M(y/p) + M(y/p²) + ... = Σ_{k≥0} M(y/p^k)

CAN WE USE THIS TO PROVE RH?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
import math

print("=" * 80)
print("RECURSIVE MERTENS PROOF ATTEMPT")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 200000
primes = list(primerange(2, MAX_N))
primes_set = set(primes)

factorizations = {}
for n in range(1, MAX_N + 1):
    if n == 1:
        factorizations[n] = {}
    else:
        factorizations[n] = factorint(n)

def is_squarefree(n):
    if n > MAX_N:
        return all(e == 1 for e in factorint(n).values())
    return all(e == 1 for e in factorizations[n].values())

def omega(n):
    if n > MAX_N:
        return len(factorint(n))
    return len(factorizations[n])

def mu(n):
    if not is_squarefree(n):
        return 0
    return (-1) ** omega(n)

# Precompute Mertens function
M_cache = {}
def M(x):
    x = int(x)
    if x < 1:
        return 0
    if x in M_cache:
        return M_cache[x]
    result = sum(mu(n) for n in range(1, x + 1))
    M_cache[x] = result
    return result

# Precompute M_p (Mertens restricted to n coprime to p)
def M_p(y, p):
    """Mertens function restricted to n with gcd(n, p) = 1."""
    y = int(y)
    if y < 1:
        return 0
    return sum(mu(n) for n in range(1, y + 1) if n % p != 0)

# =============================================================================
# PART 1: VERIFY THE FUNDAMENTAL IDENTITY
# =============================================================================

print("""

================================================================================
PART 1: VERIFY M(y) = M_p(y) - M_p(y/p)
================================================================================
""")

for p in [2, 3, 5, 7]:
    print(f"\nPrime p = {p}:")
    for y in [100, 1000, 10000, 50000]:
        My = M(y)
        Mp_y = M_p(y, p)
        Mp_yp = M_p(y // p, p)
        diff = Mp_y - Mp_yp
        print(f"  y={y}: M(y)={My}, M_p(y)-M_p(y/p)={Mp_y}-{Mp_yp}={diff}, Match: {My == diff}")

# =============================================================================
# PART 2: THE RECURSIVE FORMULA
# =============================================================================

print("""

================================================================================
PART 2: VERIFY M_p(y) = Σ_{k≥0} M(y/p^k)
================================================================================
""")

for p in [2, 3, 5]:
    print(f"\nPrime p = {p}:")
    for y in [1000, 10000]:
        # Direct calculation
        Mp_y = M_p(y, p)

        # Using recursion
        recursive_sum = 0
        k = 0
        ypk = y
        while ypk >= 1:
            recursive_sum += M(ypk)
            k += 1
            ypk = y // (p ** k)

        print(f"  y={y}: M_p(y)={Mp_y}, Σ M(y/p^k)={recursive_sum}, Match: {Mp_y == recursive_sum}")

# =============================================================================
# PART 3: CAN WE BOUND M(x) USING THIS?
# =============================================================================

print("""

================================================================================
PART 3: ATTEMPTING TO BOUND M(x)
================================================================================

The identity M(y) = M_p(y) - M_p(y/p) suggests:

|M(y)| ≤ |M_p(y)| + |M_p(y/p)|

But M_p(y) = Σ_{k≥0} M(y/p^k), so:

|M_p(y)| ≤ Σ_{k≥0} |M(y/p^k)|

This is circular unless we have bounds on M at all scales!

HOWEVER: Maybe we can find a different relation...
""")

# =============================================================================
# PART 4: THE MÖBIUS INVERSION APPROACH
# =============================================================================

print("""

================================================================================
PART 4: MÖBIUS INVERSION
================================================================================

We have: M_p(y) = Σ_{k≥0} M(y/p^k)

This is a convolution! Can we invert it?

Define: f(y) = M_p(y), g(y) = M(y)

Then: f(y) = Σ_{k≥0} g(y/p^k)

Möbius inversion for this sum:
g(y) = Σ_{k≥0} (-1)^k f(y/p^k)
     = f(y) - f(y/p) + f(y/p²) - f(y/p³) + ...

Let's verify this!
""")

for p in [2, 3]:
    print(f"\nPrime p = {p}:")
    for y in [1000, 5000, 10000]:
        My = M(y)

        # Using alternating sum
        alt_sum = 0
        k = 0
        sign = 1
        ypk = y
        while ypk >= 1:
            alt_sum += sign * M_p(ypk, p)
            k += 1
            sign *= -1
            ypk = y // (p ** k)

        print(f"  y={y}: M(y)={My}, Σ (-1)^k M_p(y/p^k)={alt_sum}, Match: {My == alt_sum}")

# =============================================================================
# PART 5: MULTI-PRIME FORMULA
# =============================================================================

print("""

================================================================================
PART 5: MULTI-PRIME FORMULA
================================================================================

What if we apply the identity M(y) = M_p(y) - M_p(y/p) for MULTIPLE primes?

For primes p₁, p₂:
M(y) = M_{p₁}(y) - M_{p₁}(y/p₁)

And M_{p₁}(y) can be related to M_{p₁,p₂} etc.

This leads to inclusion-exclusion over sets of primes.
""")

def M_coprime(y, primes_list):
    """Mertens restricted to n coprime to all primes in list."""
    y = int(y)
    if y < 1:
        return 0
    total = 0
    for n in range(1, y + 1):
        if all(n % p != 0 for p in primes_list):
            total += mu(n)
    return total

# Verify inclusion-exclusion
y = 1000
M_total = M(y)
M_2 = M_coprime(y, [2])
M_3 = M_coprime(y, [3])
M_23 = M_coprime(y, [2, 3])

# M(y) should be derivable from M_2, M_3, M_23
print(f"\ny = {y}:")
print(f"  M(y) = {M_total}")
print(f"  M_2(y) = {M_2}")
print(f"  M_3(y) = {M_3}")
print(f"  M_{{2,3}}(y) = {M_23}")

# Using inclusion-exclusion:
# M = M_2 - (terms with 2)
# M_2 = M - (contribution from multiples of 2)
# The relationship is more complex...

# =============================================================================
# PART 6: THE DIRICHLET SERIES PERSPECTIVE
# =============================================================================

print("""

================================================================================
PART 6: DIRICHLET SERIES PERSPECTIVE
================================================================================

The generating function for M(x) is:
Σ M(n)/n^s = 1/(s·ζ(s))

For M_p(x), we're summing over n coprime to p:
Σ_{(n,p)=1} μ(n)/n^s = (1 - 1/p^s) · 1/ζ(s) = (p^s - 1)/(p^s · ζ(s))

The identity M(y) = M_p(y) - M_p(y/p) corresponds to:
[coefficient of 1 in series] = [coeff for coprime] - [coeff for coprime at scale p]

This is the Euler product structure of ζ(s)!
""")

# =============================================================================
# PART 7: CAN WE PROVE |M(x)| = O(√x)?
# =============================================================================

print("""

================================================================================
PART 7: PROOF STRATEGY ANALYSIS
================================================================================

STRATEGY 1: Direct recursion bound
---------------------------------
From M_p(y) = Σ_{k≥0} M(y/p^k):

If we ASSUME |M(y)| ≤ C·√y, then:
|M_p(y)| ≤ Σ_{k≥0} C·√(y/p^k) = C·√y · Σ_{k≥0} p^{-k/2} = C·√y / (1 - p^{-1/2})

And |M(y)| = |M_p(y) - M_p(y/p)| ≤ |M_p(y)| + |M_p(y/p)|
           ≤ C·√y/(1-p^{-1/2}) + C·√(y/p)/(1-p^{-1/2})
           = C/(1-p^{-1/2}) · (√y + √y/√p)
           = C/(1-p^{-1/2}) · √y · (1 + 1/√p)

For this to give |M(y)| ≤ C·√y, we need:
(1 + 1/√p)/(1 - 1/√p) ≤ 1

But (1 + 1/√p)/(1 - 1/√p) > 1 always!

So the naive bound FAILS.

STRATEGY 2: Cancellation in the sum
-----------------------------------
The sum M_p(y) = Σ_{k≥0} M(y/p^k) involves M at multiple scales.

If M(y) oscillates (as it does), maybe these terms cancel?

Let's check the oscillation structure.
""")

# Check oscillation in M_p(y)
p = 2
for y in [1000, 5000, 10000, 50000]:
    print(f"\ny = {y}, p = {p}:")
    k = 0
    ypk = y
    terms = []
    while ypk >= 1:
        terms.append((k, ypk, M(ypk)))
        k += 1
        ypk = y // (p ** k)

    for k, ypk, Mval in terms:
        print(f"  k={k}: y/p^k={ypk}, M(y/p^k)={Mval}")

    print(f"  Sum = {sum(t[2] for t in terms)}, M_p(y) = {M_p(y, p)}")

# =============================================================================
# PART 8: OSCILLATION ANALYSIS
# =============================================================================

print("""

================================================================================
PART 8: OSCILLATION ANALYSIS
================================================================================

Key observation: M(y/p^k) can have alternating signs!

Let's measure the cancellation more precisely.
""")

p = 2
for y in [10000, 50000, 100000]:
    k = 0
    ypk = y
    positive = 0
    negative = 0
    while ypk >= 1:
        Mval = M(ypk)
        if Mval > 0:
            positive += Mval
        else:
            negative += abs(Mval)
        k += 1
        ypk = y // (p ** k)

    total = positive - negative
    gross = positive + negative
    print(f"y={y}: positive={positive}, negative={negative}, net={total}, gross={gross}")
    print(f"  Cancellation ratio: {100*(gross-abs(total))/gross:.1f}%")

# =============================================================================
# PART 9: THE FUNDAMENTAL OBSERVATION
# =============================================================================

print("""

================================================================================
PART 9: FUNDAMENTAL OBSERVATION
================================================================================

THE IDENTITY M(y) = M_p(y) - M_p(y/p) is beautiful but CIRCULAR for proving RH.

Here's why:

1. M_p(y) involves M at all scales y, y/p, y/p², ...
2. To bound M_p(y), we need bounds on M at all scales
3. This is exactly what RH gives us!

HOWEVER, the identity reveals the STRUCTURE of M(x):

M(x) is determined by the way primes "filter" through scales.

The √x behavior comes from:
- Each scale y/p^k contributes √(y/p^k) fluctuation
- The fluctuations at different scales are CORRELATED
- The correlations cause cancellation
- The residual after cancellation is O(√x)

This is the SAME structure that the ζ zeros control!
""")

# =============================================================================
# PART 10: COMPARISON TO KNOWN RESULTS
# =============================================================================

print("""

================================================================================
PART 10: COMPARISON TO KNOWN RESULTS
================================================================================

Our identity M(y) = M_p(y) - M_p(y/p) is essentially:

M(x) = Σ_{n ≤ x} μ(n) = Σ_{n ≤ x, p∤n} μ(n) - Σ_{n ≤ x/p, p∤n} μ(n)

This is a known identity! It's related to:

1. BUCHSTAB'S IDENTITY: Counts primes by sieving
2. SELBERG SIEVE: Uses weighted sums over divisors
3. HYPERBOLA METHOD: Splits sums at √x

The new observation is that M_p = Σ_k M(y/p^k) gives a recursive structure.

Can we use this like the hyperbola method?
""")

# Hyperbola method comparison
# M(x) = Σ_{d ≤ √x} μ(d) ⌊x/d⌋ - (Σ_{d ≤ √x} μ(d))²  (not quite, but similar flavor)

# Our recursion:
# M_p(x) = M(x) + M(x/p) + M(x/p²) + ...
# M(x) = M_p(x) - M_p(x/p)

# =============================================================================
# PART 11: A NEW APPROACH?
# =============================================================================

print("""

================================================================================
PART 11: A POTENTIAL NEW APPROACH
================================================================================

OBSERVATION: For large p, M_p(y) ≈ M(y) since most n are coprime to large p.

Specifically, for p > √y, we have M_p(y) = M(y) + M(y/p) ≈ M(y).

IDEA: Can we bootstrap?

1. Start with trivial bound: |M(y)| ≤ y
2. For large p (p > y^0.9), we have M_p(y) = M(y) + M(y/p) ≈ M(y)
3. For smaller p, use recursion to build up bounds
4. Hope for improvement at each step?

Let me try a computational experiment.
""")

def compute_M_p_bound(y, p, M_bounds):
    """
    Given bounds on |M(z)| for z < y, compute bound on |M_p(y)|.

    M_p(y) = Σ_{k≥0} M(y/p^k)

    |M_p(y)| ≤ Σ_{k≥0} |M(y/p^k)| ≤ Σ_{k≥0} M_bounds(y/p^k)
    """
    total = 0
    k = 0
    ypk = y
    while ypk >= 1:
        total += M_bounds[int(ypk)]
        k += 1
        ypk = y // (p ** k)
    return total

# Start with actual |M(y)| values
y_values = list(range(1, 10001))
actual_M = {y: abs(M(y)) for y in y_values}

print("Computing actual |M(y)|/√y ratios:")
for y in [100, 1000, 5000, 10000]:
    ratio = actual_M[y] / math.sqrt(y)
    print(f"  |M({y})|/√{y} = {actual_M[y]}/{math.sqrt(y):.1f} = {ratio:.4f}")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY
================================================================================

KEY IDENTITY VERIFIED:
M(y) = M_p(y) - M_p(y/p)
M_p(y) = Σ_{k≥0} M(y/p^k)

WHAT THIS TELLS US:
1. M(x) has multi-scale structure controlled by primes
2. The √x behavior comes from cancellation across scales
3. The identity is CONSISTENT with RH but doesn't prove it

WHY IT DOESN'T PROVE RH:
1. Bounding M_p requires knowing M at all scales
2. The recursion is circular without external input
3. Breaking the circularity requires ζ zeros

POTENTIAL VALUE:
1. May give new proof structure if combined with other methods
2. Shows why RH implies Mertens bound (backwards implication)
3. Connects to sieve theory (Buchstab identity)

NEXT DIRECTION:
Investigate whether the CORRELATIONS between M(y/p^k) values
can be bounded without knowing individual values.
""")

print("=" * 80)
print("RECURSIVE MERTENS PROOF ATTEMPT COMPLETE")
print("=" * 80)
