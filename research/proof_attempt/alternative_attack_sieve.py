"""
ALTERNATIVE ATTACK: SIEVE METHODS
==================================

Sieve methods bound the number of integers with certain prime properties
WITHOUT assuming RH. Can we use them for M(x)?

Key tools:
1. Selberg sieve
2. Large sieve
3. Bombieri-Vinogradov theorem
4. Combinatorial sieves

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, primepi, prime, factorint, totient, divisors
from collections import defaultdict
import math

print("=" * 80)
print("ALTERNATIVE ATTACK: SIEVE METHODS")
print("=" * 80)

# Setup
MAX_N = 50000
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)
omega_array = [0] * (MAX_N + 1)

cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum
    if n > 1:
        omega_array[n] = len(factorint(n))

def M(x):
    return M_array[int(x)] if 1 <= int(x) <= MAX_N else 0

def mu(n):
    return mu_array[int(n)] if int(n) <= MAX_N else int(mobius(int(n)))

print("Setup complete.\n")

# =============================================================================
# PART 1: SELBERG SIEVE IDEA
# =============================================================================

print("=" * 60)
print("PART 1: SELBERG SIEVE FRAMEWORK")
print("=" * 60)

print("""
The Selberg sieve bounds:
  S(A, P, z) = #{a ∈ A : gcd(a, P(z)) = 1}

where P(z) = Π_{p<z} p.

For M(x), we need to count:
  #{n ≤ x : n squarefree, ω(n) even} - #{n ≤ x : n squarefree, ω(n) odd}

Can we sieve separately for even and odd ω?
""")

def count_by_omega_parity(x):
    """Count squarefree n ≤ x by parity of ω(n)."""
    even = 0
    odd = 0
    for n in range(1, int(x) + 1):
        if mu(n) != 0:  # squarefree
            if omega_array[n] % 2 == 0:
                even += 1
            else:
                odd += 1
    return even, odd

print("\nCounting by ω parity:")
for x in [100, 1000, 10000]:
    even, odd = count_by_omega_parity(x)
    diff = even - odd
    sqrt_x = np.sqrt(x)
    print(f"  x={x}: even={even}, odd={odd}, diff={diff}, √x={sqrt_x:.2f}")
    print(f"         M({x}) = {M(x)}")

# =============================================================================
# PART 2: BUCHSTAB'S IDENTITY
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: BUCHSTAB'S IDENTITY")
print("=" * 60)

print("""
Buchstab's identity for counting primes/squarefrees:

Let Φ(x, y) = #{n ≤ x : all prime factors of n are > y}

Then: Φ(x, y) = 1 + Σ_{y < p ≤ x} Φ(x/p, p)

This is a sieve recursion! Can we adapt it for M(x)?

Define: M(x, y) = Σ_{n ≤ x, P⁻(n) > y} μ(n)
where P⁻(n) is the smallest prime factor of n.
""")

def smallest_prime_factor(n):
    """Return smallest prime factor of n, or n if prime/1."""
    if n <= 1:
        return n
    for p in range(2, int(np.sqrt(n)) + 1):
        if n % p == 0:
            return p
    return n

def M_sieved(x, y):
    """M(x) restricted to n with smallest prime factor > y."""
    total = 0
    for n in range(1, int(x) + 1):
        if n == 1 or smallest_prime_factor(n) > y:
            total += mu(n)
    return total

print("\nM(x, y) = M restricted to P⁻(n) > y:")
for x in [100, 1000]:
    print(f"\n  x = {x}:")
    for y in [2, 5, 10, 20]:
        M_xy = M_sieved(x, y)
        print(f"    y={y}: M({x}, {y}) = {M_xy}")

# =============================================================================
# PART 3: INCLUSION-EXCLUSION BOUND
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: INCLUSION-EXCLUSION APPROACH")
print("=" * 60)

print("""
M(x) = Σ μ(n) = #{n sqfree, ω even} - #{n sqfree, ω odd}

By inclusion-exclusion on primes:
  #{sqfree ≤ x} = Σ_{d sqfree} μ(d) ⌊x/d²⌋

Can we get a similar formula for M(x)?
""")

# Verify the squarefree count formula
def count_squarefree_formula(x):
    """Count squarefree using Möbius."""
    total = 0
    d = 1
    while d * d <= x:
        total += mu(d) * int(x / (d * d))
        d += 1
    return total

print("\nSquarefree counting formula:")
for x in [100, 1000, 10000]:
    formula = count_squarefree_formula(x)
    direct = sum(1 for n in range(1, int(x) + 1) if mu(n) != 0)
    print(f"  x={x}: formula={formula}, direct={direct}, match={formula==direct}")

# =============================================================================
# PART 4: PARITY PROBLEM
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: THE PARITY PROBLEM")
print("=" * 60)

print("""
THE FUNDAMENTAL OBSTACLE:

Sieve methods suffer from the "parity problem":
They cannot distinguish between numbers with an even vs odd
number of prime factors!

This is exactly what M(x) measures:
  M(x) = #{sqfree, ω even} - #{sqfree, ω odd}

The parity problem says sieves alone cannot bound this difference!

KNOWN RESULTS:
- Selberg sieve gives: #{primes in [x, 2x]} ≥ cx/log(x)
- But cannot prove: #{primes in [x, 2x]} ≤ Cx/log(x) (upper bound)

The upper bound requires Brun-Hooley or assumptions about zeros.
""")

# Demonstrate the parity problem
print("\nDemonstrating parity balance:")
for x in [1000, 10000, 50000]:
    even, odd = count_by_omega_parity(x)
    sqfree = even + odd
    expected_sqfree = 6 * x / (np.pi**2)
    print(f"  x={x}: sqfree={sqfree}, expected={expected_sqfree:.0f}")
    print(f"         even={even}, odd={odd}, |diff|/√x = {abs(even-odd)/np.sqrt(x):.2f}")

# =============================================================================
# PART 5: BOMBIERI-VINOGRADOV
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: BOMBIERI-VINOGRADOV THEOREM")
print("=" * 60)

print("""
Bombieri-Vinogradov (unconditional!):

Σ_{q ≤ Q} max_{(a,q)=1} |π(x; q, a) - Li(x)/φ(q)| = O(x / (log x)^A)

for Q ≤ √x / (log x)^B.

This bounds errors in prime counting in arithmetic progressions
ON AVERAGE over q.

Can we adapt this for μ(n)?
""")

# Compute μ in arithmetic progressions
def mu_in_progression(x, q, a):
    """Σ_{n ≤ x, n ≡ a (mod q)} μ(n)"""
    return sum(mu(n) for n in range(a, int(x) + 1, q) if n >= 1)

print("\nμ sums in arithmetic progressions:")
x = 10000
for q in [3, 5, 7, 11]:
    total_error = 0
    print(f"\n  q = {q}:")
    for a in range(1, q):
        if math.gcd(a, q) == 1:
            mu_sum = mu_in_progression(x, q, a)
            # Expected is roughly M(x)/φ(q) if μ is equidistributed
            expected = M(x) / totient(q)
            error = abs(mu_sum - expected)
            total_error += error**2
            print(f"    a={a}: Σμ = {mu_sum}, expected ≈ {expected:.1f}, error = {error:.1f}")

# =============================================================================
# PART 6: VAUGHAN'S IDENTITY
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: VAUGHAN'S IDENTITY")
print("=" * 60)

print("""
Vaughan's identity decomposes sums over μ:

Σ μ(n)f(n) = (Type I) + (Type II) + (bilinear)

Where:
- Type I: Short sums over μ
- Type II: Sums over products
- Bilinear: Convolution-like terms

This is how unconditional results like Vinogradov's theorem work.
""")

# Simplified Vaughan-type decomposition
def vaughan_decompose(x, U, V):
    """
    Decompose M(x) using Vaughan's identity.
    U, V are cutoff parameters.
    """
    # Type I: n ≤ U
    type_I = M(U)

    # Type II: UV < n ≤ x with structure
    # This is more complex in practice

    # For now, just demonstrate the idea
    return type_I, x - U  # Simplified

print("\nVaughan-type decomposition (simplified):")
x = 10000
for U in [10, 100, 1000]:
    V = int(np.sqrt(x / U))
    type_I, remainder = vaughan_decompose(x, U, V)
    print(f"  U={U}, V≈{V}: Type I = M({U}) = {type_I}")

# =============================================================================
# PART 7: WHAT SIEVES CAN AND CANNOT DO
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: SIEVE LIMITATIONS")
print("=" * 60)

print("""
WHAT SIEVES CAN DO (unconditionally):
- Count squarefree numbers: #{sqfree ≤ x} = 6x/π² + O(√x)
- Bound prime counts in intervals (lower bounds)
- Prove primes exist in short intervals
- Handle Type I and Type II sums

WHAT SIEVES CANNOT DO (parity barrier):
- Distinguish ω even from ω odd
- Prove upper bounds on primes without extra input
- Bound M(x) directly

THE PARITY PROBLEM IS FUNDAMENTAL:
The Selberg sieve weights are all positive, so they cannot
produce cancellation between +1 and -1 values of μ.

To bound M(x), we NEED to exploit cancellation.
Sieves don't see cancellation.
""")

# =============================================================================
# PART 8: DENSITY ESTIMATES
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: DENSITY ESTIMATES")
print("=" * 60)

print("""
What CAN sieves tell us?

Density of squarefree numbers: 6/π² ≈ 0.6079
Density with ω even: ?
Density with ω odd: ?

If we could show these densities are exactly equal...
then M(x)/x → 0 (which is true but not RH-strength).
""")

# Compute densities
x = 50000
sqfree_count = sum(1 for n in range(1, x + 1) if mu(n) != 0)
even_count = sum(1 for n in range(1, x + 1) if mu(n) == 1)
odd_count = sum(1 for n in range(1, x + 1) if mu(n) == -1)

print(f"\nDensities for x = {x}:")
print(f"  Squarefree: {sqfree_count/x:.6f} (expected 6/π² = {6/np.pi**2:.6f})")
print(f"  Even ω: {even_count/x:.6f}")
print(f"  Odd ω: {odd_count/x:.6f}")
print(f"  Difference: {(even_count - odd_count)/x:.6f}")
print(f"  M(x)/x: {M(x)/x:.6f}")

# =============================================================================
# PART 9: HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: HONEST ASSESSMENT")
print("=" * 60)

print("""
SIEVE METHODS ASSESSMENT:

1. THE PARITY BARRIER is fundamental:
   - Sieves use positive weights
   - Cannot produce cancellation
   - Cannot bound M(x) = (even) - (odd)

2. WHAT'S ACHIEVABLE unconditionally:
   - M(x)/x → 0 (prime number theorem)
   - |M(x)| = O(x / exp(c√log x)) [Walfisz]
   - These use zero-free regions, not pure sieves

3. WHY PURE SIEVES FAIL:
   - Sieves bound "one-sided" quantities
   - M(x) is a signed sum
   - No sieve can distinguish signs

4. POTENTIAL USE:
   - Sieves might help bound PARTS of M(x)
   - Combined with other methods (analytic)
   - But not as standalone proof

CONCLUSION:

Pure sieve methods cannot prove |M(x)| = O(√x).
The parity problem is not a technical limitation but a fundamental
barrier that reflects the arithmetic difficulty of the problem.
""")

print("=" * 80)
print("SIEVE ANALYSIS COMPLETE")
print("=" * 80)
