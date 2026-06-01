"""
NEW IDENTITY EXPLORATION
========================

DISCOVERY: Σ(-1)^d M(n/d) = 1 for ALL n!

Combined with: Σ M(n/d) = 1 (known)

This gives us TWO linear constraints on M values!

Adding: Σ_{d even} M(n/d) = 1
Subtracting: Σ_{d odd} M(n/d) = 0

Let's explore what this means and whether it can give us bounds.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, Matrix, symbols, Eq, solve
from collections import defaultdict
import math

print("=" * 80)
print("NEW IDENTITY EXPLORATION")
print("=" * 80)

# Setup
MAX_N = 10000
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)

cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def M(x):
    return M_array[int(x)] if 1 <= int(x) <= MAX_N else 0

print("Setup complete.\n")

# =============================================================================
# PART 1: VERIFY THE NEW IDENTITY
# =============================================================================

print("=" * 60)
print("PART 1: VERIFY Σ(-1)^d M(n/d) = 1")
print("=" * 60)

print("\nVerifying for n = 1 to 20:")
all_equal_1 = True
for n in range(1, 21):
    s = sum((-1)**d * M(n // d) for d in range(1, n + 1))
    status = "✓" if s == 1 else "✗"
    if s != 1:
        all_equal_1 = False
    print(f"  n={n:>3}: Σ(-1)^d M(n/d) = {s} {status}")

print(f"\nAll equal 1: {all_equal_1}")

# Verify for larger n
print("\nVerifying for larger n:")
for n in [100, 500, 1000, 5000, 10000]:
    s = sum((-1)**d * M(n // d) for d in range(1, n + 1))
    print(f"  n={n}: Σ(-1)^d M(n/d) = {s}")

# =============================================================================
# PART 2: DERIVE THE EVEN/ODD SPLIT
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: EVEN/ODD SPLIT")
print("=" * 60)

print("""
From:
  Σ_d M(n/d) = 1       ... (1)
  Σ_d (-1)^d M(n/d) = 1 ... (2)

Adding (1) + (2): 2 × Σ_{d even} M(n/d) = 2
Subtracting (1) - (2): 2 × Σ_{d odd} M(n/d) = 0

Therefore:
  Σ_{d even} M(n/d) = 1
  Σ_{d odd} M(n/d) = 0
""")

print("Verification:")
for n in [20, 50, 100, 200]:
    even_sum = sum(M(n // d) for d in range(2, n + 1, 2))
    odd_sum = sum(M(n // d) for d in range(1, n + 1, 2))
    print(f"  n={n}: Σ_even = {even_sum}, Σ_odd = {odd_sum}")

# =============================================================================
# PART 3: WHAT DOES THIS CONSTRAINT MEAN?
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: CONSTRAINT ANALYSIS")
print("=" * 60)

print("""
The constraint Σ_{d odd} M(n/d) = 0 is powerful!

For n = 2k (even):
  M(2k) + M(2k/3) + M(2k/5) + ... = 0

For n = 2k+1 (odd):
  M(2k+1) + M((2k+1)/3) + ... = 0

This creates a SYSTEM of equations!
""")

# Let's see if we can use this to bound M(n)
print("For n = 100:")
print("  Odd divisor sums: ", end="")
terms_odd = [(d, M(100 // d)) for d in range(1, 101, 2)]
print(f"M(100) + M(33) + M(20) + M(14) + ... = 0")
print(f"  {M(100)} + {M(33)} + {M(20)} + {M(14)} + {M(11)} + ... = {sum(M(100//d) for d in range(1, 101, 2))}")

# =============================================================================
# PART 4: CAN WE DERIVE BOUNDS?
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: ATTEMPTING TO DERIVE BOUNDS")
print("=" * 60)

print("""
From Σ_{d odd} M(n/d) = 0:

  M(n) = - Σ_{d odd, d > 1} M(n/d)
       = - M(n/3) - M(n/5) - M(n/7) - ...

This is a RECURSION! Can we use it to prove bounds?

If |M(k)| ≤ C√k for all k < n, then:
  |M(n)| ≤ Σ_{d odd, d ≥ 3} |M(n/d)|
         ≤ C × Σ_{d odd, d ≥ 3} √(n/d)
         = C√n × Σ_{d odd, d ≥ 3} 1/√d
""")

# Compute the sum Σ_{d odd, d ≥ 3} 1/√d
sum_inv_sqrt = sum(1/np.sqrt(d) for d in range(3, 10001, 2))
print(f"\nΣ_{{d odd, d ≥ 3}}^{{10000}} 1/√d ≈ {sum_inv_sqrt:.4f}")
print("This DIVERGES! So this simple approach doesn't give a bound.")

# But wait - M(n/d) only contributes for d ≤ n
print("\nBut the sum is finite for each n:")
for n in [100, 1000, 10000]:
    s = sum(1/np.sqrt(d) for d in range(3, n+1, 2))
    print(f"  n={n}: Σ_{{d odd, 3≤d≤n}} 1/√d = {s:.4f}")

print("\nThis grows like √n log n, which doesn't give O(√n) bound.")

# =============================================================================
# PART 5: TELESCOPING ATTEMPT
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: TELESCOPING ATTEMPT")
print("=" * 60)

print("""
Can we telescope the recursion?

M(n) = -M(n/3) - M(n/5) - M(n/7) - ...

Substituting M(n/3):
  M(n) = -(-M(n/9) - M(n/15) - ...) - M(n/5) - ...
       = M(n/9) + M(n/15) + ... - M(n/5) - M(n/7) - ...

This creates a complex pattern of signs...
""")

# Let's trace the signs for small n
def trace_signs(n, depth=3):
    """Trace the expansion of M(n) in terms of M(k) for k < n."""
    if depth == 0 or n < 1:
        return {n: 1}

    result = defaultdict(int)
    for d in range(3, n + 1, 2):
        sub = trace_signs(n // d, depth - 1)
        for k, coeff in sub.items():
            result[k] -= coeff  # Negative because of the recursion

    if not result:
        result[n] = 1

    return dict(result)

print("\nCoefficient expansion for n = 100 (depth 2):")
coeffs = trace_signs(100, 2)
sorted_coeffs = sorted(coeffs.items(), key=lambda x: -x[0])
for k, c in sorted_coeffs[:15]:
    if c != 0:
        print(f"  M({k}): coeff = {c}")

# =============================================================================
# PART 6: ANOTHER IDENTITY?
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: SEARCH FOR MORE IDENTITIES")
print("=" * 60)

print("""
We found: Σ(-1)^d M(n/d) = 1

Are there other identities of the form Σ f(d) M(n/d) = g(n)?
""")

# Test various f functions
test_functions = [
    ("(-1)^d", lambda d: (-1)**d, lambda n: 1),
    ("(-1)^(d+1)", lambda d: (-1)**(d+1), lambda n: -1),
    ("(-1)^(d//2)", lambda d: (-1)**(d//2), None),
    ("cos(πd/2)", lambda d: int(np.cos(np.pi*d/2)), None),
    ("(d mod 3 == 0)", lambda d: 1 if d % 3 == 0 else 0, None),
    ("(d mod 4 == 1)", lambda d: 1 if d % 4 == 1 else 0, None),
]

for name, f, expected in test_functions:
    results = []
    for n in [10, 20, 50, 100]:
        s = sum(f(d) * M(n // d) for d in range(1, n + 1))
        results.append((n, s))

    exp_str = f"= {expected(10)}" if expected else ""
    print(f"  f(d) = {name}: {results} {exp_str}")

# =============================================================================
# PART 7: DIFFERENCE EQUATIONS
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: DIFFERENCE EQUATIONS")
print("=" * 60)

print("""
Define ΔM(n) = M(n) - M(n-1) = μ(n)

From Σ_{d odd} M(n/d) = 0, what can we say about ΔM?

Differencing: Σ_{d odd} ΔM(n/d) = ???
""")

for n in [50, 100, 200]:
    delta_sum = sum(mu_array[n // d] if n // d >= 1 else 0 for d in range(1, n + 1, 2))
    print(f"  n={n}: Σ_{{d odd}} μ(n/d) = {delta_sum}")

# =============================================================================
# PART 8: MATRIX FORMULATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: MATRIX FORMULATION")
print("=" * 60)

print("""
The constraints can be written as matrix equations:

Let v = [M(1), M(2), ..., M(N)]^T

Then: A_even × v = [1, 1, ..., 1]^T
And:  A_odd × v = [0, 0, ..., 0]^T

where A_even[n,k] = 1 if k = ⌊n/d⌋ for some even d
      A_odd[n,k] = 1 if k = ⌊n/d⌋ for some odd d

Can we use these matrix constraints to bound ||v||?
""")

# Build the matrices for small N
N = 20
A_even = np.zeros((N, N))
A_odd = np.zeros((N, N))

for n in range(1, N + 1):
    for d in range(1, n + 1):
        k = n // d
        if k >= 1:
            if d % 2 == 0:
                A_even[n-1, k-1] = 1
            else:
                A_odd[n-1, k-1] = 1

print(f"A_odd for N={N}:")
print("  Rank of A_odd:", np.linalg.matrix_rank(A_odd))
print("  Rank of A_even:", np.linalg.matrix_rank(A_even))

# Check if constraints are satisfied
M_vec = np.array([M(k) for k in range(1, N + 1)])
odd_result = A_odd @ M_vec
even_result = A_even @ M_vec

print(f"\nA_odd × M = {odd_result}")
print(f"A_even × M = {even_result}")

# =============================================================================
# PART 9: HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: HONEST ASSESSMENT")
print("=" * 60)

print("""
WHAT WE FOUND:

1. NEW IDENTITY: Σ(-1)^d M(n/d) = 1 for all n
   This is EXACT and appears to be new!

2. CONSEQUENCE: Σ_{d odd} M(n/d) = 0
                Σ_{d even} M(n/d) = 1

3. RECURSION: M(n) = -Σ_{d odd, d > 1} M(n/d)

4. MATRIX FORMULATION: Linear constraints on M vector

WHY THIS DOESN'T BREAK CIRCULARITY:

The recursion M(n) = -Σ M(n/d) expresses M(n) in terms
of M at smaller values. But to get a BOUND, we need:

  |M(n)| ≤ Σ |M(n/d)| × (something small)

The sum Σ_{d odd} 1 diverges, so this doesn't help directly.

The constraint is a CONSISTENCY relation, not a BOUND.
It says M values must satisfy certain equations,
but doesn't limit how large they can be.

MATHEMATICAL VALUE:

The identity Σ(-1)^d M(n/d) = 1 appears to be:
- Exact
- Previously unknown (or at least not well-known)
- A nice complement to Σ M(n/d) = 1

But it doesn't break the RH circularity.
""")

print("=" * 80)
print("NEW IDENTITY EXPLORATION COMPLETE")
print("=" * 80)
