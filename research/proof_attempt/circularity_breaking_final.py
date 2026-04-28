"""
FINAL CIRCULARITY BREAKING ATTEMPT
==================================

We've found that every approach leads back to prime distribution.
Let's make one final attempt to find structure that bypasses primes.

APPROACHES TO TRY:
1. Random walk / martingale perspective
2. Combinatorial identity for divisor chains
3. Spectral gap argument
4. Convexity / concentration inequality
5. Information-theoretic bound

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, divisors, factorint
import math
from collections import defaultdict

print("=" * 80)
print("FINAL CIRCULARITY BREAKING ATTEMPT")
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

def mu(n):
    return mu_array[int(n)] if int(n) <= MAX_N else int(mobius(int(n)))

print("Setup complete.\n")

# =============================================================================
# APPROACH 1: RANDOM WALK PERSPECTIVE
# =============================================================================

print("=" * 60)
print("APPROACH 1: RANDOM WALK / MARTINGALE")
print("=" * 60)

print("""
View M(n) as a random walk: M(n) = M(n-1) + μ(n)

For a random walk with steps ±1:
  Var(S_n) = n → σ ≈ √n

For μ(n), the steps are {-1, 0, +1} with:
  P(μ=+1) ≈ 3/π² (squarefree, even ω)
  P(μ=-1) ≈ 3/π² (squarefree, odd ω)
  P(μ=0) ≈ 1 - 6/π² (non-squarefree)

Expected increment: E[μ] ≈ 0
Variance per step: Var(μ) ≈ 6/π² ≈ 0.608

If steps were INDEPENDENT: Var(M_n) ≈ 0.608n → σ ≈ 0.78√n

PROBLEM: Steps are NOT independent!
  Correlations: Cov(μ(n), μ(m)) ≠ 0 when gcd(n,m) > 1

These correlations REDUCE variance to ~0.016n (97% reduction).
But proving this reduction requires prime distribution!
""")

# Verify the variance
print("Variance check:")
n_max = 5000
m_vals = [M(n) for n in range(1, n_max + 1)]
var_M = np.var(m_vals)
print(f"  Var(M) over [1, {n_max}]: {var_M:.2f}")
print(f"  Var/n: {var_M/n_max:.4f}")
print(f"  Expected if independent: 0.608")
print(f"  Reduction: {100*(1 - var_M/n_max/0.608):.1f}%")

# =============================================================================
# APPROACH 2: COMBINATORIAL IDENTITY
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 2: COMBINATORIAL IDENTITY")
print("=" * 60)

print("""
Is there a combinatorial identity for Σ_k (-1)^k C(n,k)?

where C(n,k) = (D^k e)_n = # divisor chains of length k from n

Known: Σ_k C(n,k) relates to hyperbola method
       Alternating sum = M(n)

SEARCHING for structure in C(n,k)...
""")

def compute_Dk_e_at_n(n, k, memo={}):
    if (n, k) in memo:
        return memo[(n, k)]
    if k == 0:
        return 1
    if n < 2:
        return 0
    total = 0
    for d in range(2, n + 1):
        total += compute_Dk_e_at_n(n // d, k - 1, memo)
    memo[(n, k)] = total
    return total

# Look for generating function structure
print("\nC(n,k) for n = 2^m (powers of 2):\n")
for m in range(1, 8):
    n = 2**m
    row = []
    for k in range(m + 2):
        c = compute_Dk_e_at_n(n, k)
        if c == 0 and len(row) > 0:
            break
        row.append(c)
    print(f"  n=2^{m}={n:>3}: C(n,k) = {row}")

print("\nLooking for pattern...")
print("  For n = 2^m, max k = m + 1")
print("  C(2^m, k) seems related to Stirling numbers?")

# =============================================================================
# APPROACH 3: SPECTRAL GAP ARGUMENT
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 3: SPECTRAL GAP")
print("=" * 60)

print("""
The operator (I+D) has all eigenvalues = 1 (no spectral gap).
But the nilpotent part D has specific structure.

CAN WE USE: ||D^k|| decays with k?

For nilpotent D with index m:
  D^m = 0
  ||D^k|| may still be large for k < m

The issue: ||D|| ~ N (very large!) even though ρ(D) = 0

Without a "small" operator norm, we can't get good bounds from
the Neumann series expansion.
""")

# Check operator norms for small N
print("\nOperator norms for D:")
for N in [20, 50, 100]:
    D = np.zeros((N, N))
    for k in range(1, N + 1):
        for d in range(2, k + 1):
            j = k // d
            if j >= 1:
                D[k-1, j-1] += 1

    spectral_radius = max(abs(e) for e in np.linalg.eigvals(D))
    operator_norm = np.linalg.norm(D, 2)

    print(f"  N={N}: ρ(D)={spectral_radius:.6f}, ||D||={operator_norm:.2f}, ||D||/N={operator_norm/N:.4f}")

# =============================================================================
# APPROACH 4: CONCENTRATION INEQUALITY
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 4: CONCENTRATION INEQUALITY")
print("=" * 60)

print("""
Could we use Azuma-Hoeffding or McDiarmid?

For M(n) = Σ_{k≤n} μ(k):
  Each μ(k) ∈ {-1, 0, 1}
  Changing one μ(k) changes M(n) by at most 2

If μ(k) were independent:
  P(|M(n) - E[M(n)]| > t) ≤ 2 exp(-t²/2n)

This gives |M(n)| = O(√n log n) with high probability.

PROBLEM: μ(k) are NOT independent.
  The dependence structure encodes prime distribution.

Martingale concentration requires bounded differences.
The differences ARE bounded, but the FILTRATION matters.
""")

# =============================================================================
# APPROACH 5: INFORMATION THEORETIC
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 5: INFORMATION THEORY")
print("=" * 60)

print("""
Entropy of the Möbius sequence?

The sequence μ(1), μ(2), ..., μ(n) has low entropy per symbol
because of the deterministic structure (squarefree, factorization).

BUT: The partial sums M(n) could still fluctuate.

The information-theoretic approach would bound:
  H(M(n) | M(n-1)) = H(μ(n))

This is bounded, but doesn't directly give M(n) bounds.
""")

# =============================================================================
# APPROACH 6: WHAT IF WE DON'T NEED √n?
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 6: WEAKER BOUNDS")
print("=" * 60)

print("""
Can we prove ANY non-trivial bound without prime distribution?

From the nilpotent structure alone:
  M(n) = Σ_{k=0}^{m} (-1)^k (D^k e)_n  where m ~ log₂(n)

Trivial bound: |M(n)| ≤ Σ_k (D^k e)_n

What is Σ_k (D^k e)_n?
""")

# Compute Σ_k (D^k e)_n
print("\nΣ_k (D^k e)_n for various n:\n")
for n in [20, 50, 100, 200, 500]:
    total = 0
    for k in range(30):
        c = compute_Dk_e_at_n(n, k)
        if c == 0:
            break
        total += c
    print(f"  n={n:>3}: Σ_k C(n,k) = {total}, n*log(n) = {n * np.log(n):.1f}")

print("\n  Σ_k C(n,k) ~ n log n (hyperbola method)")
print("  This gives |M(n)| ≤ O(n log n) - USELESS")

# =============================================================================
# APPROACH 7: THE MÖBIUS INVERSION STRUCTURE
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 7: MÖBIUS INVERSION STRUCTURE")
print("=" * 60)

print("""
The identity μ * 1 = ε (Dirichlet convolution) gives:

  Σ_{d|n} μ(d) = ε(n) = [n=1]

This is exact for all n. But for M(n) = Σ_{k≤n} μ(k), we need:

  Σ_{k≤n} Σ_{d|k} μ(d) = 1 + Σ_{k≤n, k>1} 0 = 1

Rearranging (hyperbola method):
  Σ_{d≤n} M(n/d) = 1

This gives: M(n) = 1 - Σ_{d=2}^{n} M(n/d)

Iterating gives the Neumann series... back to where we started!
""")

# =============================================================================
# APPROACH 8: FUNCTIONAL EQUATION
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 8: FUNCTIONAL EQUATION")
print("=" * 60)

print("""
Is there a functional equation for M(n)?

From M(n) = 1 - Σ_{d=2}^{n} M(⌊n/d⌋):

For n → ∞, heuristically:
  M(n) ≈ 1 - ∫₂^n M(n/t) dt/t
       ≈ 1 - M(n) ∫₂^n dt/t
       ≈ 1 - M(n) log(n/2)

This gives M(n) ≈ 1/(1 + log(n/2)) → 0

But this misses the oscillations!
The integral approximation loses the number-theoretic structure.
""")

# =============================================================================
# APPROACH 9: EXPLICIT FORMULA PERSPECTIVE
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 9: EXPLICIT FORMULA")
print("=" * 60)

print("""
The Mertens function has an explicit formula:

  M(x) = Σ_ρ x^ρ/ρζ'(ρ) + lower order terms

where ρ runs over nontrivial zeros of ζ(s).

IF all ρ have Re(ρ) = 1/2, then:
  |x^ρ/ρ| = x^{1/2}/|ρ| = O(x^{1/2})

This is the STANDARD proof direction:
  RH → |M(x)| = O(x^{1/2+ε})

GOING BACKWARDS:
  |M(x)| = O(x^{1/2+ε}) for all ε → RH

Our nilpotent structure is a REFORMULATION of this:
  The alternating sum structure encodes the zero distribution.
""")

# =============================================================================
# FINAL VERDICT
# =============================================================================

print("\n" + "=" * 60)
print("FINAL VERDICT")
print("=" * 60)

print("""
EVERY APPROACH LEADS BACK TO PRIME DISTRIBUTION:

1. Random walk: Independence fails due to prime structure
2. Combinatorics: Divisor chains encode prime factorization
3. Spectral gap: None exists without RH
4. Concentration: Dependencies come from primes
5. Information: Structure comes from factorization
6. Weak bounds: Only get O(n log n), useless
7. Möbius inversion: Leads back to Neumann series
8. Functional equation: Misses oscillations
9. Explicit formula: Requires zero information

THE FUNDAMENTAL OBSTRUCTION:

The Möbius function μ(n) is defined via prime factorization.
ANY property of Σμ(n) connects to prime distribution.
Prime distribution is controlled by ζ zeros.
ζ zeros are what RH describes.

THERE IS NO WAY AROUND THIS.

The nilpotent structure M = Σ(-D)^k e is beautiful.
The two-level cancellation (D⁺ ≈ -D⁻) is remarkable.
But it's a REFORMULATION, not a PROOF.

WHAT WE ACCOMPLISHED:

✓ New perspective: Nilpotent operator representation
✓ Quantification: 99.9%+ cancellation in paired differences
✓ Connection: Spectral structure ↔ Mertens bound
✓ Understanding: WHY |M(n)| = O(√n) should hold

✗ Proof of RH: Not achieved
✗ Breaking circularity: Not possible without new mathematics

CONCLUSION:

The Riemann Hypothesis cannot be proved by repackaging
existing relationships. It requires either:
  (a) A fundamentally new idea, or
  (b) A breakthrough in understanding ζ zeros directly

Our work provides INSIGHT, not PROOF.
The mathematics is beautiful and potentially useful,
but the central problem remains open.
""")

print("=" * 80)
print("CIRCULARITY ANALYSIS COMPLETE")
print("=" * 80)
