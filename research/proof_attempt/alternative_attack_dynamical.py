"""
ALTERNATIVE ATTACK: DYNAMICAL SYSTEMS / ERGODIC THEORY
========================================================

The Möbius function has natural dynamical interpretations:
1. The map n → n/p for primes p
2. Multiplicative structure as a dynamical system
3. Ergodic averages and equidistribution

Can ergodic theory give us bounds on M(x)?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, factorint, prime, primepi
from collections import defaultdict
import math

print("=" * 80)
print("ALTERNATIVE ATTACK: DYNAMICAL SYSTEMS")
print("=" * 80)

# Setup
MAX_N = 30000
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
# PART 1: MULTIPLICATIVE CASCADE
# =============================================================================

print("=" * 60)
print("PART 1: MULTIPLICATIVE CASCADE")
print("=" * 60)

print("""
View the integers as a tree:
  1 → 2 → 4 → 8 → ...
        → 6 → 12 → ...
    → 3 → 6 → ...
        → 9 → ...

Each multiplication by a prime is a "step" in the cascade.
μ(n) = (-1)^{steps from 1 to n} for squarefree n.

M(x) counts the parity of paths in this tree.
""")

def tree_depth(n):
    """Number of prime factors with multiplicity = Ω(n)"""
    if n <= 1:
        return 0
    return sum(factorint(n).values())

# Verify μ(n) = (-1)^Ω(n) for squarefree n
print("\nVerifying μ(n) = (-1)^Ω(n) for squarefree n:")
mismatches = 0
for n in range(1, 101):
    if mu(n) != 0:
        omega = tree_depth(n)
        expected = (-1)**omega
        if mu(n) != expected:
            mismatches += 1
            print(f"  Mismatch at n={n}: μ(n)={mu(n)}, (-1)^Ω={expected}")
print(f"  Total mismatches: {mismatches}")

# =============================================================================
# PART 2: ERGODIC AVERAGE
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: ERGODIC AVERAGES")
print("=" * 60)

print("""
The Birkhoff ergodic theorem says:

  (1/N) Σ_{n=1}^{N} f(T^n x) → ∫ f dμ

for ergodic systems. Can we view μ(n) as an ergodic sequence?

Consider: μ(n) as a function on the "space of integers"
with the dynamics given by multiplication.
""")

# Compute running averages of μ
print("\nRunning averages of μ(n):")
running_avg = 0
print(f"{'N':>8} | {'M(N)/N':>12} | {'√N':>8}")
print("-" * 35)
for N in [100, 500, 1000, 5000, 10000, 20000]:
    avg = M(N) / N
    sqrt_N = np.sqrt(N)
    print(f"{N:>8} | {avg:>12.6f} | {sqrt_N:>8.2f}")

print("\nM(N)/N → 0 as N → ∞ (Prime Number Theorem)")
print("But the rate of convergence is the question!")

# =============================================================================
# PART 3: MIXING PROPERTIES
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: MIXING PROPERTIES")
print("=" * 60)

print("""
A dynamical system is "mixing" if:
  Corr(f(T^n x), g(x)) → 0 as n → ∞

For μ(n), consider:
  C(k) = (1/N) Σ μ(n)μ(n+k)

If this decays fast, the system is mixing, and M(N) should grow slowly.
""")

def correlation(N, k):
    """Compute correlation of μ(n) and μ(n+k)"""
    total = 0
    count = 0
    for n in range(1, N - k + 1):
        total += mu(n) * mu(n + k)
        count += 1
    return total / count if count > 0 else 0

print("\nCorrelation C(k) = E[μ(n)μ(n+k)] for N = 10000:")
N = 10000
for k in [1, 2, 3, 5, 10, 20, 50, 100]:
    C_k = correlation(N, k)
    print(f"  C({k}) = {C_k:.6f}")

# Expected: C(k) ≈ 0 for all k > 0 (Chowla's conjecture)

# =============================================================================
# PART 4: SYMBOLIC DYNAMICS
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: SYMBOLIC DYNAMICS")
print("=" * 60)

print("""
Encode integers by their prime factorization:
  n = p₁^{a₁} p₂^{a₂} ... → (a₁, a₂, ...)

This maps Z⁺ to sequences of non-negative integers.
The "shift" in this space corresponds to division by primes.

μ(n) ≠ 0 iff all aᵢ ∈ {0, 1}
μ(n) = (-1)^{Σ aᵢ} for such n

M(x) is a sum over the "corner" {0,1}^∞ ∩ [encoded ≤ x].
""")

# Encode some numbers
print("\nSymbolic encoding (first 5 primes):")
primes = [2, 3, 5, 7, 11]
for n in [30, 60, 72, 105, 210]:
    factors = factorint(n)
    encoding = tuple(factors.get(p, 0) for p in primes)
    print(f"  {n} = {dict(factors)} → {encoding}, μ({n}) = {mu(n)}")

# =============================================================================
# PART 5: RANDOM MATRIX CONNECTION
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: RANDOM MATRIX CONNECTION")
print("=" * 60)

print("""
Montgomery-Odlyzko law: The zeros of ζ(s) on the critical line
have spacing statistics matching GUE random matrices!

This suggests: ζ zeros behave like eigenvalues of random Hermitian matrices.

For M(x):
  M(x) = Σ_ρ x^ρ / (ρ ζ'(ρ)) + ...

The oscillations of M(x) are controlled by ζ zeros.
If zeros are "random-like" (GUE), M(x) has specific statistics.
""")

# Compute statistics of M(x)
print("\nStatistics of M(x)/√x:")
M_normalized = [M(n) / np.sqrt(n) for n in range(1, 20001)]

mean = np.mean(M_normalized)
std = np.std(M_normalized)
skew = np.mean([(x - mean)**3 for x in M_normalized]) / std**3
kurt = np.mean([(x - mean)**4 for x in M_normalized]) / std**4 - 3

print(f"  Mean: {mean:.4f}")
print(f"  Std: {std:.4f}")
print(f"  Skewness: {skew:.4f} (Gaussian = 0)")
print(f"  Excess Kurtosis: {kurt:.4f} (Gaussian = 0)")

# =============================================================================
# PART 6: EQUIDISTRIBUTION
# =============================================================================

print("\n" + "=" * 60)
print("PART 6: EQUIDISTRIBUTION")
print("=" * 60)

print("""
Is μ(n) "equidistributed" in some sense?

Define: ρ₊ = lim (1/N) #{n ≤ N : μ(n) = +1}
        ρ₋ = lim (1/N) #{n ≤ N : μ(n) = -1}

Both should equal 3/π² ≈ 0.304.
Their equality is part of why M(N)/N → 0.
""")

N = 20000
count_plus = sum(1 for n in range(1, N+1) if mu(n) == 1)
count_minus = sum(1 for n in range(1, N+1) if mu(n) == -1)
count_zero = sum(1 for n in range(1, N+1) if mu(n) == 0)

print(f"\nDistribution for N = {N}:")
print(f"  ρ₊ = {count_plus/N:.6f} (expected 3/π² = {3/np.pi**2:.6f})")
print(f"  ρ₋ = {count_minus/N:.6f} (expected 3/π² = {3/np.pi**2:.6f})")
print(f"  ρ₀ = {count_zero/N:.6f} (expected 1 - 6/π² = {1 - 6/np.pi**2:.6f})")
print(f"  ρ₊ - ρ₋ = {(count_plus - count_minus)/N:.6f}")

# =============================================================================
# PART 7: TRANSFER OPERATOR APPROACH
# =============================================================================

print("\n" + "=" * 60)
print("PART 7: TRANSFER OPERATOR")
print("=" * 60)

print("""
In dynamical systems, the transfer operator L encodes dynamics:
  (Lf)(x) = Σ_{Ty = x} f(y) / |T'(y)|

For the Gauss map T(x) = {1/x}, this connects to continued fractions.

Is there a transfer operator for the multiplicative structure
whose spectral properties give bounds on M(x)?

The operator (I+D) from before is similar!
  (I+D) has all eigenvalues = 1
  Its inverse gives M via Neumann series
""")

# Recall our nilpotent operator structure
print("\nRecall: The divisor-sum operator D gives")
print("  M = (I+D)^{-1} e = e - De + D²e - ...")
print("  All eigenvalues of (I+D) = 1")
print("\nThis IS a transfer operator perspective!")

# =============================================================================
# PART 8: ENTROPY CONSIDERATIONS
# =============================================================================

print("\n" + "=" * 60)
print("PART 8: ENTROPY CONSIDERATIONS")
print("=" * 60)

print("""
The entropy of the μ sequence:
  H = -Σ p(μ) log p(μ)

where p(+1) = p(-1) ≈ 3/π², p(0) ≈ 1 - 6/π².

H ≈ -2(3/π²)log(3/π²) - (1-6/π²)log(1-6/π²)
  ≈ 0.92 bits per symbol

This bounds the "complexity" of μ.
But entropy doesn't directly give bounds on partial sums!
""")

p_plus = 3 / np.pi**2
p_minus = 3 / np.pi**2
p_zero = 1 - 6 / np.pi**2

H = -p_plus * np.log2(p_plus) - p_minus * np.log2(p_minus) - p_zero * np.log2(p_zero)
print(f"\nEntropy of μ sequence: H ≈ {H:.4f} bits/symbol")

# =============================================================================
# PART 9: INVARIANT MEASURES
# =============================================================================

print("\n" + "=" * 60)
print("PART 9: INVARIANT MEASURES")
print("=" * 60)

print("""
For a dynamical system, invariant measures are crucial.

On (Z⁺, ×), what's the "natural" measure?
- Counting measure gives M(N)/N → 0
- Logarithmic measure: Σ 1/n diverges
- Dirichlet series: Σ μ(n)/n^s = 1/ζ(s)

The Dirichlet series is the "spectral" version.
At s = 1: Σ μ(n)/n diverges (conditionally)
This divergence/convergence encodes M(x) growth!
""")

# Compute partial sums of μ(n)/n
print("\nPartial sums of μ(n)/n:")
for N in [100, 1000, 10000, 20000]:
    S = sum(mu(n) / n for n in range(1, N + 1))
    print(f"  N = {N}: Σ μ(n)/n = {S:.6f}")

print("\nThese should oscillate (conditionally convergent to 0)")

# =============================================================================
# PART 10: HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 60)
print("PART 10: HONEST ASSESSMENT")
print("=" * 60)

print("""
DYNAMICAL SYSTEMS ASSESSMENT:

1. MULTIPLICATIVE STRUCTURE as dynamics:
   - Tree structure of integers under multiplication
   - μ(n) tracks parity of depth
   - M(x) counts signed vertices

2. ERGODIC PROPERTIES:
   - M(N)/N → 0 (ergodic theorem)
   - Correlations C(k) → 0 (mixing)
   - But rate of mixing encodes prime distribution!

3. RANDOM MATRIX CONNECTION:
   - GUE statistics for ζ zeros
   - M(x) oscillations governed by zeros
   - But this IS the analytic connection!

4. TRANSFER OPERATOR:
   - (I+D) with all eigenvalues = 1
   - M = Neumann series of nilpotent
   - Beautiful structure, but same circularity

WHY DYNAMICS DOESN'T BREAK CIRCULARITY:

The dynamical viewpoint is EQUIVALENT to the analytic one.
- Mixing rate ↔ Prime distribution
- Spectral gap ↔ Zero-free region
- Transfer operator spectrum ↔ ζ zeros

Ergodic theory gives us another language for the same problem,
not a new route to the solution.

POTENTIAL VALUE:

- Conceptual clarity
- Connection to physics (quantum chaos)
- Possible new invariants to discover
""")

print("=" * 80)
print("DYNAMICAL SYSTEMS ANALYSIS COMPLETE")
print("=" * 80)
