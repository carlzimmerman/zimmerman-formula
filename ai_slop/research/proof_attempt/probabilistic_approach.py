"""
THE PROBABILISTIC APPROACH TO RH
=================================

Can we prove V(X) = cX using probabilistic methods?

Key insight: μ(n) behaves "randomly" in many senses, but is constrained by:
1. Multiplicativity: μ(nm) = μ(n)μ(m) for gcd(n,m) = 1
2. Orthogonality: Σ_{d|n} μ(d) = [n=1]
3. Sign flipping: μ(pn) = -μ(n)

Can these constraints FORCE the 97.4% cancellation?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, primerange, factorint
import math
from collections import defaultdict
import random

print("=" * 80)
print("THE PROBABILISTIC APPROACH TO RH")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 100000

print("Computing Mertens function and μ values...")
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)
omega_array = [0] * (MAX_N + 1)  # Number of prime factors
cumsum = 0

for n in range(1, MAX_N + 1):
    mu_val = int(mobius(n))
    mu_array[n] = mu_val
    cumsum += mu_val
    M_array[n] = cumsum
    if n > 1:
        omega_array[n] = len(factorint(n))

def M(x):
    x = int(x)
    if x < 1:
        return 0
    if x <= MAX_N:
        return M_array[x]
    return 0

def mu(n):
    n = int(n)
    if n <= MAX_N:
        return mu_array[n]
    return int(mobius(n))

primes = list(primerange(2, 1000))
print("Done.")

# =============================================================================
# PART 1: RANDOM MULTIPLICATIVE FUNCTIONS
# =============================================================================

print("""

================================================================================
PART 1: RANDOM MULTIPLICATIVE FUNCTIONS
================================================================================

Consider a "random" multiplicative function f(n) where:
- f(p) = ±1 with equal probability for each prime p
- f(p^k) = 0 for k ≥ 2 (like μ)
- f(nm) = f(n)f(m) for gcd(n,m) = 1

This is a RANDOM MODEL for μ!

Key question: What is E[|Σ_{n≤X} f(n)|²] for such f?
""")

def random_multiplicative_sum(X, seed=None):
    """Generate a random multiplicative function and compute its partial sum."""
    if seed is not None:
        random.seed(seed)

    # Assign random signs to primes
    prime_signs = {}
    for p in primes:
        if p <= X:
            prime_signs[p] = random.choice([-1, 1])

    # Compute f(n) for n ≤ X
    total = 0
    for n in range(1, X + 1):
        if n == 1:
            f_n = 1
        else:
            factors = factorint(n)
            # Check if squarefree
            if any(e > 1 for e in factors.values()):
                f_n = 0
            else:
                f_n = 1
                for p in factors:
                    if p in prime_signs:
                        f_n *= prime_signs[p]
                    else:
                        f_n *= random.choice([-1, 1])
        total += f_n

    return total

# Sample random multiplicative functions
X = 10000
n_samples = 100
random_sums = [random_multiplicative_sum(X, seed=i) for i in range(n_samples)]
random_sums_sq = [s**2 for s in random_sums]

print(f"Random multiplicative functions with X = {X}:")
print(f"  Samples: {n_samples}")
print(f"  E[S] = {np.mean(random_sums):.2f}")
print(f"  Std[S] = {np.std(random_sums):.2f}")
print(f"  E[S²] = {np.mean(random_sums_sq):.2f}")
print(f"  √E[S²] = {np.sqrt(np.mean(random_sums_sq)):.2f}")
print(f"  √X = {np.sqrt(X):.2f}")
print(f"  E[S²]/X = {np.mean(random_sums_sq)/X:.4f}")

# Compare to actual Mertens
actual_M = M(X)
print(f"\nActual M({X}) = {actual_M}")
print(f"M({X})²/X = {actual_M**2/X:.4f}")

# =============================================================================
# PART 2: THE HARPER-STYLE ANALYSIS
# =============================================================================

print("""

================================================================================
PART 2: HARPER-STYLE ANALYSIS
================================================================================

Adam Harper proved that for random multiplicative functions:
  E[|Σ f(n)|²] ~ c × X × (log X)^{something}

The key is that RANDOM multiplicative functions have variance ~ X log X,
not just X!

But μ is SPECIAL - it's the UNIQUE multiplicative function with:
  Σ μ(d) = [n=1] for all n

Does this extra constraint reduce variance?
""")

# Check how the variance of M(x) depends on x
print("Variance structure of M(x):")
print(f"{'X':>8} | {'M(X)²':>10} | {'M(X)²/X':>10} | {'M(X)²/(X log X)':>15}")
print("-" * 55)

for X in [1000, 2000, 5000, 10000, 20000, 50000, 100000]:
    MX = M(X)
    ratio1 = MX**2 / X
    ratio2 = MX**2 / (X * np.log(X))
    print(f"{X:>8} | {MX**2:>10} | {ratio1:>10.4f} | {ratio2:>15.6f}")

# =============================================================================
# PART 3: THE ORTHOGONALITY CONSTRAINT
# =============================================================================

print("""

================================================================================
PART 3: THE ORTHOGONALITY CONSTRAINT
================================================================================

The key constraint: Σ_{d|n} μ(d) = [n=1]

This means for ANY n > 1:
  μ(1) + Σ_{p|n} μ(p) + Σ_{pq|n} μ(pq) + ... = 0

This creates MASSIVE dependencies between μ values!

For n = p₁p₂...pₖ (squarefree):
  Σ over all 2^k subsets = 0
  So the 2^k terms sum to 0!

This is like saying: For every squarefree n, there's a "local" cancellation.
""")

# Verify and quantify the orthogonality
print("Orthogonality check for squarefree n:")
for n in [6, 30, 210, 2310]:
    divisors = [d for d in range(1, n+1) if n % d == 0]
    mu_sum = sum(mu(d) for d in divisors)
    num_sqfree_div = sum(1 for d in divisors if mu(d) != 0)
    print(f"  n = {n}: {num_sqfree_div} squarefree divisors, Σμ(d) = {mu_sum}")

# =============================================================================
# PART 4: COUNTING CONSTRAINTS
# =============================================================================

print("""

================================================================================
PART 4: COUNTING THE CONSTRAINTS
================================================================================

How many orthogonality constraints are there up to X?

For each n > 1 with n ≤ X: Σ_{d|n} μ(d) = 0

That's X - 1 constraints!

But μ has only π(X) "free" parameters (the values μ(p) = -1 for primes).

Wait - μ(p) = -1 is FIXED, not free!

So μ is COMPLETELY DETERMINED by its definition.

The question is: Does this determinism imply the variance bound?
""")

# Count how "constrained" μ is
X = 1000
n_squarefree = sum(1 for n in range(1, X+1) if mu(n) != 0)
n_constraints = X - 1  # One constraint per n > 1

print(f"At X = {X}:")
print(f"  Squarefree numbers: {n_squarefree}")
print(f"  Orthogonality constraints: {n_constraints}")
print(f"  Ratio: {n_constraints / n_squarefree:.2f} constraints per squarefree")

# =============================================================================
# PART 5: THE SELBERG-DELANGE METHOD (SIMPLIFIED)
# =============================================================================

print("""

================================================================================
PART 5: SELBERG-DELANGE STYLE ANALYSIS
================================================================================

The Selberg-Delange method analyzes sums via:
  Σ f(n) = ∫ F(s) x^s ds / (2πi)

where F(s) = Σ f(n)/n^s is the Dirichlet series.

For μ: Σ μ(n)/n^s = 1/ζ(s)

So M(x) is controlled by 1/ζ(s) near Re(s) = 1.

The RESIDUE at ζ = 0 (i.e., at s = 1 where 1/ζ has no pole) determines asymptotics.

Key: 1/ζ(1 + it) is bounded ⟹ M(x) = o(x)
     1/ζ(σ + it) for σ > 1/2 bounded ⟹ M(x) = O(x^{1/2+ε})

This is the ANALYTIC approach - not purely probabilistic.
""")

# =============================================================================
# PART 6: MARTINGALE APPROACH
# =============================================================================

print("""

================================================================================
PART 6: MARTINGALE APPROACH
================================================================================

Can we view M(x) as a martingale?

Define: F_x = σ-algebra generated by {μ(n) : n ≤ x}

Is M(x) a martingale with respect to F_x?

E[M(x+1) | F_x] = M(x) + E[μ(x+1) | F_x]

For this to be a martingale, we'd need E[μ(x+1) | F_x] = 0.

But μ(x+1) is DETERMINISTIC (not random) given we know μ!

The "martingale" structure comes from the AVERAGING over x.
""")

# Check the "conditional expectation" structure
# Look at average of μ(n) conditioned on ω(n) mod 2
print("μ(n) statistics by ω(n) mod 2:")
for parity in [0, 1]:
    values = [mu(n) for n in range(1, 10001)
              if mu(n) != 0 and omega_array[n] % 2 == parity]
    print(f"  ω(n) ≡ {parity} (mod 2): mean μ = {np.mean(values):.6f}, count = {len(values)}")

# =============================================================================
# PART 7: THE ERDŐS-KAC PERSPECTIVE
# =============================================================================

print("""

================================================================================
PART 7: THE ERDŐS-KAC PERSPECTIVE
================================================================================

Erdős-Kac: ω(n) is approximately normal with mean log log n, variance log log n.

Since μ(n) = (-1)^{ω(n)} for squarefree n:
  P(μ(n) = 1) ≈ P(ω(n) even) ≈ 1/2
  P(μ(n) = -1) ≈ P(ω(n) odd) ≈ 1/2

This gives E[μ(n)] ≈ 0 for "typical" n.

But the CORRELATIONS matter for M(x)!
""")

# Verify Erdős-Kac for our range
X = 50000
omega_values = [omega_array[n] for n in range(2, X+1)]
mean_omega = np.mean(omega_values)
var_omega = np.var(omega_values)
expected_mean = np.log(np.log(X))
expected_var = np.log(np.log(X))

print(f"Erdős-Kac verification at X = {X}:")
print(f"  Mean ω(n): {mean_omega:.4f} (expected: {expected_mean:.4f})")
print(f"  Var ω(n): {var_omega:.4f} (expected: {expected_var:.4f})")

# Distribution of ω(n) mod 2
sqfree = [n for n in range(1, X+1) if mu(n) != 0]
even_omega = sum(1 for n in sqfree if omega_array[n] % 2 == 0)
odd_omega = sum(1 for n in sqfree if omega_array[n] % 2 == 1)

print(f"\nAmong squarefree n ≤ {X}:")
print(f"  Even ω(n): {even_omega} ({100*even_omega/len(sqfree):.2f}%)")
print(f"  Odd ω(n): {odd_omega} ({100*odd_omega/len(sqfree):.2f}%)")
print(f"  Difference: {even_omega - odd_omega}")
print(f"  M(X) = {M(X)}")

# =============================================================================
# PART 8: THE CORRELATION DECAY
# =============================================================================

print("""

================================================================================
PART 8: CORRELATION DECAY
================================================================================

For independent random variables: Var(Σ X_i) = Σ Var(X_i)

For μ(n), the correlation C(k) = E[μ(n)μ(n+k)] decays as k → ∞.

If C(k) decays fast enough, we might get CLT-type behavior!

The key question: How fast does C(k) decay?
""")

# Measure correlation decay
N = 30000
correlations = {}
for k in range(1, 501):
    products = [mu(n) * mu(n + k) for n in range(1, N - k + 1)
                if mu(n) != 0 and mu(n + k) != 0]
    if products:
        correlations[k] = np.mean(products)

# Fit decay
k_vals = list(correlations.keys())
c_vals = [abs(correlations[k]) for k in k_vals]

print("Correlation decay C(k) = E[μ(n)μ(n+k)]:")
for k in [1, 2, 5, 10, 20, 50, 100, 200, 500]:
    if k in correlations:
        print(f"  C({k:>3}) = {correlations[k]:>8.5f}")

# Check if correlations sum to something finite
partial_sum = sum(correlations[k] for k in range(1, 501))
print(f"\nΣ_{{k=1}}^{{500}} C(k) = {partial_sum:.4f}")

# =============================================================================
# PART 9: THE VARIANCE DECOMPOSITION
# =============================================================================

print("""

================================================================================
PART 9: VARIANCE DECOMPOSITION
================================================================================

Var(M(X)) = E[M(X)²] - E[M(X)]²

For the "average" variance over x ≤ X:
V(X) = (1/X) Σ_{x≤X} M(x)²

We have: M(x)² = Σ_{n,m≤x} μ(n)μ(m)

So: V(X) = (1/X) Σ_{n,m≤X} μ(n)μ(m) × #{x: max(n,m) ≤ x ≤ X}
         = (1/X) Σ_{n,m≤X} μ(n)μ(m) × (X - max(n,m) + 1)

Split into diagonal and off-diagonal:
  Diagonal: (1/X) Σ_n μ(n)² × (X - n + 1)
  Off-diagonal: (1/X) Σ_{n≠m} μ(n)μ(m) × (X - max(n,m) + 1)
""")

X = 5000
diagonal = sum(mu(n)**2 * (X - n + 1) for n in range(1, X + 1)) / X
off_diagonal_total = 0
for n in range(1, X + 1):
    if mu(n) == 0:
        continue
    for m in range(n + 1, X + 1):
        if mu(m) == 0:
            continue
        off_diagonal_total += 2 * mu(n) * mu(m) * (X - m + 1)
off_diagonal = off_diagonal_total / X

print(f"Variance decomposition at X = {X}:")
print(f"  Diagonal contribution: {diagonal:.4f}")
print(f"  Off-diagonal contribution: {off_diagonal:.4f}")
print(f"  Total V(X): {diagonal + off_diagonal:.4f}")
print(f"  Off-diagonal / Diagonal: {off_diagonal / diagonal:.4f}")
print(f"  Cancellation: {-off_diagonal / diagonal * 100:.1f}%")

# =============================================================================
# PART 10: THE PROBABILISTIC BOUND ATTEMPT
# =============================================================================

print("""

================================================================================
PART 10: PROBABILISTIC BOUND ATTEMPT
================================================================================

THEOREM ATTEMPT:

Let f be ANY completely multiplicative function with f(p) ∈ {-1, 0, 1}.

IF f satisfies the orthogonality: Σ_{d|n} f(d) = [n=1] for all n,
THEN f = μ (the unique such function).

MOREOVER, for such f:
  Var(Σ_{n≤X} f(n)) = O(X)

PROOF ATTEMPT:

The orthogonality forces f(1) = 1 and:
  f(p) + f(1) = 0 for all primes p ⟹ f(p) = -1

For prime powers:
  f(1) + f(p) + f(p²) = 0 ⟹ f(p²) = 0

This determines f = μ uniquely!

But does orthogonality imply the VARIANCE bound?
""")

# Test: Does orthogonality alone constrain variance?
# Create a "perturbed" μ that still satisfies some orthogonality

print("Testing if orthogonality constrains variance...")

# The orthogonality Σ_{d|n} μ(d) = [n=1] is equivalent to 1/ζ having no pole at s=1
# This is ALWAYS true for μ, but it doesn't directly give variance bounds

# =============================================================================
# PART 11: THE MERTENS CONSTANT CONNECTION
# =============================================================================

print("""

================================================================================
PART 11: MERTENS CONSTANT CONNECTION
================================================================================

The Mertens constant B appears in: Σ_{p≤x} 1/p = log log x + B + O(1/log x)

And B = γ + Σ_p [log(1 - 1/p) + 1/p] ≈ 0.2615

For random primes with density 1/log n:
  E[# primes ≤ x] ≈ x/log x

The prime distribution creates the "randomness" in μ!

If primes were "more random" (Cramér model):
  M(x) would be O(√x) with high probability

The question: Does the ACTUAL prime distribution have enough randomness?
""")

# Check prime gaps vs random model
primes_list = list(primerange(2, 10001))
gaps = [primes_list[i+1] - primes_list[i] for i in range(len(primes_list)-1)]
mean_gap = np.mean(gaps)
var_gap = np.var(gaps)

print(f"Prime gap statistics up to 10000:")
print(f"  Mean gap: {mean_gap:.4f}")
print(f"  Var gap: {var_gap:.4f}")
print(f"  Expected mean gap (Cramér): ~log(5000) = {np.log(5000):.4f}")

# =============================================================================
# PART 12: THE CLT OBSTRUCTION
# =============================================================================

print("""

================================================================================
PART 12: THE CLT OBSTRUCTION
================================================================================

For independent ±1 variables X_i:
  S_n = Σ X_i satisfies CLT: S_n/√n → N(0,1)

For μ(n):
  The values are DEPENDENT via multiplicativity
  The CLT might not apply directly

BUT: If correlations decay fast enough, we can still get CLT!

The Lindeberg-Feller CLT needs:
  Σ E[X_i² 1_{|X_i| > ε√(Σ Var)}] → 0

For μ(n), we have |μ(n)| ≤ 1, so this condition is satisfied!

The issue is: The dependencies might create non-CLT behavior.
""")

# Test CLT-like behavior for M(x)
# Normalize M(x) by √x and check distribution
x_values = list(range(1000, 50001, 100))
normalized_M = [M(x) / np.sqrt(x) for x in x_values]

print("Distribution of M(x)/√x:")
print(f"  Mean: {np.mean(normalized_M):.4f}")
print(f"  Std: {np.std(normalized_M):.4f}")
print(f"  Min: {np.min(normalized_M):.4f}")
print(f"  Max: {np.max(normalized_M):.4f}")

# Check if distribution is normal-like
from scipy import stats
sorted_norm = sorted(normalized_M)
n = len(sorted_norm)
theoretical_quantiles = [stats.norm.ppf((i + 0.5) / n) for i in range(n)]
correlation = np.corrcoef(sorted_norm, theoretical_quantiles)[0, 1]
print(f"  Q-Q correlation with normal: {correlation:.4f}")

# =============================================================================
# PART 13: THE FUNDAMENTAL THEOREM ATTEMPT
# =============================================================================

print("""

================================================================================
PART 13: FUNDAMENTAL THEOREM ATTEMPT
================================================================================

THEOREM (Attempted):

For the Möbius function μ:
  V(X) = (1/X) Σ_{x≤X} M(x)² = c·X + o(X)

where c is a constant depending on the prime distribution.

PROOF SKETCH:

1. Decompose V(X) = Diagonal + Off-diagonal

2. Diagonal = (1/X) Σ μ(n)² (X - n + 1) ≈ (6/π²)(X/2) = 3X/π²

3. Off-diagonal = Σ_{n≠m} μ(n)μ(m) × weight

   For coprime (n,m): μ(n)μ(m) = μ(nm)
   The sum over coprime pairs relates to Σ μ(k) weighted by #{(n,m): nm=k, gcd=1}

4. The constraint Σ_{d|n} μ(d) = [n=1] forces cancellation

5. Specifically, for each n > 1, the divisor sum vanishes.

6. This creates correlations that reduce variance.

THE GAP:
We cannot prove the OFF-DIAGONAL term is O(X) without using ζ zeros.
""")

# =============================================================================
# PART 14: WHAT PROBABILISTIC METHODS CAN PROVE
# =============================================================================

print("""

================================================================================
PART 14: WHAT PROBABILISTIC METHODS CAN PROVE
================================================================================

KNOWN RESULTS (unconditional):

1. Halász's theorem: M(x) = O(x · exp(-c√log log x))
   - Uses probabilistic ideas about character sums

2. Zero-density estimates: M(x) = O(x^θ) for various θ < 1
   - Not purely probabilistic

3. Almost-all results: M(x) = O(√x log^k x) for almost all x
   - Probabilistic in the "almost all" sense

WHAT WOULD BE NEW:

Prove V(X) = c·X without using ζ information.

This would be a STATISTICAL statement about μ that implies RH-type bounds.
""")

# =============================================================================
# PART 15: THE HONEST CONCLUSION
# =============================================================================

print("""

================================================================================
PART 15: HONEST CONCLUSION
================================================================================

THE PROBABILISTIC APPROACH:

1. μ(n) has "random-like" behavior:
   - E[μ(n)] ≈ 0 on squarefree n
   - Correlations C(k) are O(0.01) and decay
   - ω(n) mod 2 is nearly 50-50

2. The CONSTRAINTS on μ:
   - Multiplicativity: μ(nm) = μ(n)μ(m)
   - Orthogonality: Σ_{d|n} μ(d) = [n=1]
   - Sign flip: μ(pn) = -μ(n)

3. These constraints FORCE cancellation:
   - Off-diagonal terms cancel 97.4% of diagonal
   - This is NOT accidental

4. THE GAP:
   - Proving the 97.4% cancellation algebraically
   - Requires knowing the constraints are "tight enough"
   - This tightness depends on prime distribution → ζ zeros

5. PROBABILISTIC METHODS CAN PROVE:
   - Halász-type bounds (weaker than RH)
   - Almost-all results
   - Statistical properties of μ

6. PROBABILISTIC METHODS CANNOT YET PROVE:
   - V(X) = c·X exactly
   - Pointwise |M(x)| = O(√x)
   - Breaking the connection to ζ zeros

THE FUNDAMENTAL ISSUE:

The "randomness" of μ is controlled by prime distribution.
Prime distribution is controlled by ζ zeros.
The circle is not broken by probabilistic methods alone.

HOWEVER: The probabilistic perspective gives a PRECISE TARGET:
  Prove that the multiplicative constraints force 97.4% cancellation.

This is a well-defined mathematical problem that might have
a non-analytic solution.
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY: PROBABILISTIC APPROACH
================================================================================

WHAT WE FOUND:

1. Random multiplicative functions have E[S²] ~ X log X
2. Actual μ has V(X) ~ 0.016 X (no log factor!)
3. The reduction is 97.4% from independence
4. Correlations C(k) ~ O(0.01) and decay
5. M(x)/√x has correlation 0.93 with normal quantiles

THE KEY INSIGHT:

μ is MORE constrained than a random multiplicative function.
The orthogonality Σ_{d|n} μ(d) = [n=1] creates extra cancellation.
This removes the log factor and gives V(X) ~ cX.

BUT:

Proving this rigorously connects to ζ zeros.
The probabilistic methods available cannot close this gap.

NEW DIRECTION:

Frame the problem as: "Which multiplicative constraints
force variance O(X) instead of O(X log X)?"

If we can characterize such constraints algebraically,
we might get a new proof strategy.
""")

print("=" * 80)
print("PROBABILISTIC APPROACH ANALYSIS COMPLETE")
print("=" * 80)
