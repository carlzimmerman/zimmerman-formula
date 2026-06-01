"""
ALTERNATIVE ATTACK: DIRECT OFF-DIAGONAL ANALYSIS
=================================================

We know: Var(M) = Σ μ(n)μ(m) × (weight)
                = (diagonal) + (off-diagonal)

The off-diagonal has 97.4% cancellation.
Can we PROVE this cancellation directly?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, gcd, factorint, divisors
from collections import defaultdict
import math

print("=" * 80)
print("ALTERNATIVE ATTACK: OFF-DIAGONAL ANALYSIS")
print("=" * 80)

# Setup
MAX_N = 20000
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
# PART 1: VARIANCE DECOMPOSITION
# =============================================================================

print("=" * 60)
print("PART 1: VARIANCE DECOMPOSITION")
print("=" * 60)

print("""
V(X) = (1/X) Σ_{x≤X} M(x)²
     = (1/X) Σ_{x≤X} [Σ_{n≤x} μ(n)]²
     = (1/X) Σ_{x≤X} Σ_{n,m ≤ x} μ(n)μ(m)

Rearranging:
V(X) = Σ_{n,m ≤ X} μ(n)μ(m) × w(n,m,X)

where w(n,m,X) = #{x : n,m ≤ x ≤ X} / X = (X - max(n,m) + 1) / X
""")

def compute_variance_decomposition(X):
    """Compute diagonal and off-diagonal contributions to V(X)."""
    diagonal = 0
    off_diagonal = 0

    for n in range(1, X + 1):
        mu_n = mu(n)
        if mu_n == 0:
            continue

        # Weight for pair (n, n)
        w_nn = (X - n + 1) / X
        diagonal += mu_n * mu_n * w_nn

        for m in range(n + 1, X + 1):
            mu_m = mu(m)
            if mu_m == 0:
                continue

            # Weight for pair (n, m)
            w_nm = (X - m + 1) / X
            off_diagonal += 2 * mu_n * mu_m * w_nm

    return diagonal, off_diagonal

print("\nVariance decomposition:")
for X in [100, 500, 1000]:
    diag, off_diag = compute_variance_decomposition(X)
    total = diag + off_diag
    actual_V = sum(M(x)**2 for x in range(1, X + 1)) / X

    print(f"\nX = {X}:")
    print(f"  Diagonal: {diag:.4f}")
    print(f"  Off-diagonal: {off_diag:.4f}")
    print(f"  Total: {total:.4f}")
    print(f"  Actual V(X): {actual_V:.4f}")
    print(f"  Off-diagonal cancellation: {100 * (1 - total/diag):.1f}%")

# =============================================================================
# PART 2: STRUCTURE OF OFF-DIAGONAL TERMS
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: OFF-DIAGONAL STRUCTURE")
print("=" * 60)

print("""
Off-diagonal term: μ(n)μ(m) for n ≠ m

When is μ(n)μ(m) = +1? When both squarefree and same parity of ω.
When is μ(n)μ(m) = -1? When both squarefree and opposite parity.

The cancellation comes from balance between these cases!
""")

def analyze_off_diagonal_signs(X):
    """Analyze the distribution of μ(n)μ(m) for n < m ≤ X."""
    plus_count = 0
    minus_count = 0
    zero_count = 0

    for n in range(1, X + 1):
        for m in range(n + 1, X + 1):
            prod = mu(n) * mu(m)
            if prod > 0:
                plus_count += 1
            elif prod < 0:
                minus_count += 1
            else:
                zero_count += 1

    return plus_count, minus_count, zero_count

print("\nOff-diagonal sign distribution:")
for X in [100, 200]:
    plus, minus, zero = analyze_off_diagonal_signs(X)
    total_nonzero = plus + minus
    print(f"\nX = {X}:")
    print(f"  μ(n)μ(m) = +1: {plus}")
    print(f"  μ(n)μ(m) = -1: {minus}")
    print(f"  μ(n)μ(m) = 0: {zero}")
    if total_nonzero > 0:
        print(f"  Ratio +/-: {plus/minus:.4f}")

# =============================================================================
# PART 3: GCD STRUCTURE
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: GCD STRUCTURE")
print("=" * 60)

print("""
Key insight: μ(n)μ(m) depends on whether n, m share prime factors.

For coprime n, m (gcd = 1):
  If n = p₁...pₐ, m = q₁...qᵦ (disjoint primes)
  Then μ(n)μ(m) = (-1)^{a+b}

The parity of ω(n) + ω(m) determines the sign.
""")

def analyze_by_gcd(X):
    """Analyze μ(n)μ(m) contribution by gcd structure."""
    coprime_sum = 0
    coprime_count = 0
    noncoprime_sum = 0
    noncoprime_count = 0

    for n in range(1, X + 1):
        for m in range(n + 1, X + 1):
            prod = mu(n) * mu(m)
            if prod == 0:
                continue

            if gcd(n, m) == 1:
                coprime_sum += prod
                coprime_count += 1
            else:
                noncoprime_sum += prod
                noncoprime_count += 1

    return coprime_sum, coprime_count, noncoprime_sum, noncoprime_count

print("\nContribution by GCD:")
for X in [100, 200, 500]:
    cp_sum, cp_cnt, ncp_sum, ncp_cnt = analyze_by_gcd(X)
    print(f"\nX = {X}:")
    print(f"  Coprime pairs: sum = {cp_sum}, count = {cp_cnt}")
    print(f"  Non-coprime pairs: sum = {ncp_sum}, count = {ncp_cnt}")
    print(f"  Total sum: {cp_sum + ncp_sum}")

# =============================================================================
# PART 4: MULTIPLICATIVE STRUCTURE
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: MULTIPLICATIVE STRUCTURE")
print("=" * 60)

print("""
For coprime n, m:
  μ(nm) = μ(n)μ(m)

This means: μ(n)μ(m) = μ(nm) for coprime n, m.

Summing over coprime pairs:
  Σ_{gcd(n,m)=1} μ(n)μ(m) = Σ_{gcd(n,m)=1} μ(nm)

This connects pair sums to sums over products!
""")

# Verify the identity
print("\nVerifying μ(n)μ(m) = μ(nm) for coprime pairs:")
verified = 0
total = 0
for n in range(1, 50):
    for m in range(1, 50):
        if gcd(n, m) == 1:
            total += 1
            if mu(n) * mu(m) == mu(n * m):
                verified += 1

print(f"  {verified}/{total} verified")

# =============================================================================
# PART 5: CORRELATION BY DISTANCE
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: CORRELATION BY DISTANCE")
print("=" * 60)

print("""
Does the correlation depend on |m - n|?

C(k) = (1/N) Σ_{n≤N-k} μ(n)μ(n+k)

If C(k) → 0 as k → ∞, the off-diagonal terms cancel.
""")

N = 10000
print(f"\nCorrelations C(k) for N = {N}:")
for k in [1, 2, 3, 5, 10, 20, 50, 100, 500, 1000]:
    C_k = sum(mu(n) * mu(n + k) for n in range(1, N - k + 1)) / (N - k)
    print(f"  C({k}) = {C_k:.6f}")

print("\nChowla's conjecture: All C(k) = 0 for k > 0")
print("(Still unproven in general!)")

# =============================================================================
# PART 6: DIRECT BOUND ATTEMPT
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: DIRECT BOUND ATTEMPT")
print("=" * 60)

print("""
ATTEMPT to prove off-diagonal cancellation directly:

Σ_{n<m} μ(n)μ(m) × w(n,m)

= Σ_{gcd(n,m)=1} μ(nm) × w(n,m) + Σ_{gcd(n,m)>1} μ(n)μ(m) × w(n,m)

For the coprime part:
  = Σ_k μ(k) × #{(n,m): nm=k, n<m, gcd=1}

The count involves factorization structure...
""")

def coprime_factorizations(k):
    """Count pairs (n,m) with nm = k, n < m, gcd(n,m) = 1."""
    count = 0
    for n in range(1, k + 1):
        if k % n == 0:
            m = k // n
            if n < m and gcd(n, m) == 1:
                count += 1
    return count

print("\nCoprime factorization counts:")
for k in [6, 12, 30, 60, 210]:
    c = coprime_factorizations(k)
    print(f"  k = {k}: #{'{'}(n,m): nm=k, n<m, gcd=1{'}'} = {c}")

# =============================================================================
# PART 7: MÖBIUS CORRELATION FUNCTION
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: MOBIUS CORRELATION FUNCTION")
print("=" * 60)

print("""
Define: R(d) = lim_{N→∞} (1/N) Σ_{n≤N, d|n} μ(n)

For squarefree d:
  R(d) = μ(d) × (density of squarefree coprime to d)
       = μ(d) × Π_{p|d} (1 - 1/p²) × (6/π²) / Π_{p|d} (1 - 1/p²)
       = μ(d) × (6/π²)

This should be 0 on average (M(N)/N → 0).
""")

# Verify R(d) empirically
N = 20000
print(f"\nMöbius restricted to multiples of d (N = {N}):")
for d in [2, 3, 5, 6, 10, 30]:
    R_d = sum(mu(n) for n in range(d, N + 1, d) if n <= N) / (N / d)
    expected = 0  # In the limit
    print(f"  d = {d}: R(d) = {R_d:.6f}")

# =============================================================================
# PART 8: QUADRATIC FORM PERSPECTIVE
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: QUADRATIC FORM PERSPECTIVE")
print("=" * 60)

print("""
V(X) = Σ_{n,m} μ(n)μ(m) × w(n,m,X)
     = μᵀ W μ

where W is the weight matrix.

For V(X) = O(X), we need:
  μᵀ W μ = O(X)

The matrix W has entries ~ 1, so naive bound gives O(X²).
The O(X) bound requires 97%+ cancellation.

Can we prove this algebraically?
""")

# Small example
N = 50
W = np.zeros((N, N))
mu_vec = np.array([mu(n) for n in range(1, N + 1)])

for n in range(N):
    for m in range(N):
        W[n, m] = (N - max(n, m)) / N

quadratic = mu_vec @ W @ mu_vec
diagonal_only = sum(mu_vec[n]**2 * W[n, n] for n in range(N))

print(f"\nFor N = {N}:")
print(f"  Quadratic form μᵀWμ = {quadratic:.4f}")
print(f"  Diagonal only: {diagonal_only:.4f}")
print(f"  Cancellation: {100 * (1 - quadratic/diagonal_only):.1f}%")

# =============================================================================
# PART 9: EIGENVALUE ANALYSIS
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: EIGENVALUE ANALYSIS OF W")
print("=" * 60)

print("""
The quadratic form μᵀWμ depends on:
1. The eigenvalues of W
2. The projections of μ onto eigenvectors

If μ is "orthogonal" to large eigenspaces, the form is small.
""")

N = 100
W = np.zeros((N, N))
for n in range(N):
    for m in range(N):
        W[n, m] = (N - max(n, m)) / N

eigenvalues = np.linalg.eigvalsh(W)
mu_vec = np.array([mu(n) for n in range(1, N + 1)])

print(f"\nEigenvalue analysis for N = {N}:")
print(f"  Max eigenvalue: {np.max(eigenvalues):.4f}")
print(f"  Min eigenvalue: {np.min(eigenvalues):.4f}")
print(f"  Sum of eigenvalues (trace): {np.sum(eigenvalues):.4f}")
print(f"  Trace of W: {np.trace(W):.4f}")

# Project μ onto eigenvectors
eigenvalues, eigenvectors = np.linalg.eigh(W)
projections = eigenvectors.T @ mu_vec
weighted_sum = np.sum(eigenvalues * projections**2)

print(f"\n  Quadratic form via eigendecomposition: {weighted_sum:.4f}")
print(f"  Direct computation: {mu_vec @ W @ mu_vec:.4f}")

# =============================================================================
# PART 10: HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("PART 10: HONEST ASSESSMENT")
print("=" * 60)

print("""
OFF-DIAGONAL ANALYSIS FINDINGS:

1. DECOMPOSITION WORKS:
   V(X) = diagonal + off-diagonal
   Off-diagonal contributes ~97% cancellation

2. GCD STRUCTURE:
   - Coprime pairs: μ(n)μ(m) = μ(nm)
   - Non-coprime: More complex

3. CORRELATIONS:
   - C(k) appears to be small for all k
   - But proving C(k) = 0 is Chowla's conjecture (open!)

4. QUADRATIC FORM:
   - μᵀWμ small relative to diagonal
   - μ has small projections onto large eigenspaces

WHY WE CAN'T PROVE CANCELLATION:

The cancellation in Σ μ(n)μ(m) depends on:
- Balance between same-parity and opposite-parity pairs
- This balance IS the Mertens bound in disguise

Proving the 97% cancellation requires either:
  (a) Chowla's conjecture (unproven)
  (b) GRH-level zero information
  (c) Something fundamentally new

The off-diagonal analysis EXPLAINS the phenomenon
but doesn't provide an independent proof route.
""")

print("=" * 80)
print("OFF-DIAGONAL ANALYSIS COMPLETE")
print("=" * 80)
