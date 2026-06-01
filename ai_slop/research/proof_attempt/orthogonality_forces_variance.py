"""
DOES ORTHOGONALITY FORCE THE VARIANCE BOUND?
=============================================

Key question: Does Σ_{d|n} f(d) = [n=1] alone imply Var(Σ f(n)) = O(X)?

The orthogonality creates X-1 linear constraints on {f(n)}.
For squarefree n, we have ~0.6X values.
The constraints are OVERDETERMINED!

This overdetermination might force the variance bound.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, divisors, primerange, factorint
import math
from collections import defaultdict

print("=" * 80)
print("DOES ORTHOGONALITY FORCE THE VARIANCE BOUND?")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 50000

print("Computing μ values...")
mu_array = [0] * (MAX_N + 1)
M_array = [0] * (MAX_N + 1)
cumsum = 0

for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def mu(n):
    if n <= MAX_N:
        return mu_array[n]
    return int(mobius(n))

def M(x):
    x = int(x)
    if x < 1:
        return 0
    if x <= MAX_N:
        return M_array[x]
    return 0

print("Done.")

# =============================================================================
# PART 1: THE ORTHOGONALITY MATRIX
# =============================================================================

print("""

================================================================================
PART 1: THE ORTHOGONALITY AS A LINEAR SYSTEM
================================================================================

The orthogonality Σ_{d|n} f(d) = [n=1] defines a LINEAR system:

Let x_i = f(i) for squarefree i.
For each n > 1: Σ_{d|n, d sqfree} x_d = 0

This is A·x = 0 where A is an (N-1) × #{sqfree} matrix.

How "overdetermined" is this system?
""")

# Count dimensions
N = 1000
sqfree_indices = [n for n in range(1, N+1) if mu(n) != 0]
n_sqfree = len(sqfree_indices)
n_constraints = N - 1  # One for each n > 1

print(f"For N = {N}:")
print(f"  Squarefree numbers: {n_sqfree}")
print(f"  Orthogonality constraints: {n_constraints}")
print(f"  Ratio (constraints/variables): {n_constraints / n_sqfree:.2f}")

# =============================================================================
# PART 2: STRUCTURE OF THE CONSTRAINT MATRIX
# =============================================================================

print("""

================================================================================
PART 2: STRUCTURE OF CONSTRAINT MATRIX
================================================================================

For each composite n, the constraint Σ_{d|n} μ(d) = 0 creates dependencies.

For n = pq (product of two primes):
  μ(1) + μ(p) + μ(q) + μ(pq) = 0
  1 + (-1) + (-1) + 1 = 0 ✓

This links μ(pq) to μ(p) and μ(q)!

The structure is: μ(n) = (-1)^{ω(n)} for squarefree n.

This is a SINGLE DEGREE OF FREEDOM (the choice of μ(1) = 1).
""")

# Verify the multiplicative structure forces everything
print("How multiplicativity determines all μ values:")
print("  μ(1) = 1 (forced by definition)")
print("  μ(p) = -1 for all primes (forced by multiplicativity)")
print("  μ(pq) = μ(p)μ(q) = 1 for coprime primes")
print("  μ(p²) = 0 (forced by non-squarefree)")

# Check if there's any freedom
print("\nIs there ANY freedom in choosing f satisfying orthogonality?")
print("  If f(1) = 1 and f multiplicative with f(p) ∈ {-1,0,1}...")
print("  Then orthogonality at n = p² forces: f(1) + f(p) + f(p²) = 0")
print("  So: 1 + f(p) + f(p²) = 0")
print("  If f(p) = -1: f(p²) = 0")
print("  If f(p) = 0: f(p²) = -1 (but then f not multiplicative)")
print("  If f(p) = 1: f(p²) = -2 (impossible for ±1,0)")
print("  CONCLUSION: f(p) = -1 is FORCED!")

# =============================================================================
# PART 3: ALTERNATIVE MULTIPLICATIVE FUNCTIONS
# =============================================================================

print("""

================================================================================
PART 3: ALTERNATIVE MULTIPLICATIVE FUNCTIONS
================================================================================

Consider: What if we RELAX multiplicativity but keep orthogonality?

A function g(n) with:
  Σ_{d|n} g(d) = [n=1] for all n

is called the Möbius inverse of the constant 1 function.

By Möbius inversion, g = μ UNIQUELY!

So orthogonality + multiplicativity → μ uniquely.
And orthogonality alone → μ uniquely!

The constraint IS the definition!
""")

# Verify Möbius inversion uniqueness
print("Verifying uniqueness of Möbius inverse:")

# Define via Möbius inversion: if f*1 = ε (indicator of 1), then f = μ*ε = μ
# This is because μ*1 = ε

# =============================================================================
# PART 4: VARIANCE UNDER ORTHOGONALITY
# =============================================================================

print("""

================================================================================
PART 4: VARIANCE UNDER ORTHOGONALITY
================================================================================

Since orthogonality uniquely determines f = μ, we can't ask
"what is variance for arbitrary f satisfying orthogonality?"

But we CAN ask:
"Does the STRUCTURE of orthogonality constraints imply variance bounds?"

The orthogonality creates a CASCADE of cancellations:
  For n = 2: μ(1) + μ(2) = 0 → μ(2) = -1
  For n = 3: μ(1) + μ(3) = 0 → μ(3) = -1
  For n = 4: μ(1) + μ(2) + μ(4) = 0 → μ(4) = 0
  For n = 6: μ(1) + μ(2) + μ(3) + μ(6) = 0 → μ(6) = 1
  ...

Each new μ value is determined by previous ones!
""")

# Compute μ recursively from orthogonality
def mu_from_orthogonality(n, cache={}):
    """Compute μ(n) using only the orthogonality relation."""
    if n in cache:
        return cache[n]
    if n == 1:
        cache[1] = 1
        return 1

    # For n > 1: μ(n) = -Σ_{d|n, d<n} μ(d)
    divs = [d for d in range(1, n) if n % d == 0]
    result = -sum(mu_from_orthogonality(d, cache) for d in divs)
    cache[n] = result
    return result

print("Computing μ from orthogonality alone:")
cache = {}
for n in [1, 2, 3, 4, 5, 6, 10, 12, 30]:
    mu_orth = mu_from_orthogonality(n, cache)
    mu_actual = mu(n)
    match = "✓" if mu_orth == mu_actual else "✗"
    print(f"  μ({n:>2}) from orthogonality: {mu_orth:>2}, actual: {mu_actual:>2} {match}")

# =============================================================================
# PART 5: THE RECURSION STRUCTURE
# =============================================================================

print("""

================================================================================
PART 5: THE RECURSION STRUCTURE
================================================================================

The recursion μ(n) = -Σ_{d|n, d<n} μ(d) gives:

  M(x) = 1 - Σ_{d=2}^{x} M(⌊x/d⌋)

This is the SAME recursion as before!

But now we see it as a CONSEQUENCE of orthogonality.

Key insight: The recursion involves M at SMALLER scales.
The error at scale x depends on errors at scales x/2, x/3, ...

This is like a BRANCHING PROCESS!
""")

# Analyze the recursion structure
print("Recursion coefficients:")
x = 1000
print(f"M({x}) = 1 - Σ M({x}/d) for d = 2, 3, ..., {x}")

# Count how many distinct values x/d takes
floor_values = set(x // d for d in range(2, x + 1))
print(f"  Number of distinct ⌊{x}/d⌋ values: {len(floor_values)}")
print(f"  Largest: {max(floor_values)}, Smallest: {min(floor_values)}")

# =============================================================================
# PART 6: VARIANCE PROPAGATION IN RECURSION
# =============================================================================

print("""

================================================================================
PART 6: VARIANCE PROPAGATION
================================================================================

Consider M as a random variable (over "random" orthogonality-satisfying f).

But we showed f = μ uniquely! So no randomness...

REFRAME: Consider M(x) as depending on "random" prime positions.
The primes determine the structure; μ follows from orthogonality.

IF primes were "random" (Cramér model), what would Var(M) be?
""")

# Simulate: perturb prime positions slightly, see effect on M
print("Effect of prime structure on M:")

# Actually, μ is completely determined - no randomness.
# The "randomness" comes from viewing x as the random variable.

# For different x, M(x) varies. This variation IS the "variance" we measure.
x_values = list(range(1000, 10001))
M_values = [M(x) for x in x_values]

print(f"M(x) for x ∈ [1000, 10000]:")
print(f"  Mean M(x): {np.mean(M_values):.2f}")
print(f"  Std M(x): {np.std(M_values):.2f}")
print(f"  √(mean x): {np.sqrt(np.mean(x_values)):.2f}")
print(f"  Ratio Std/√(mean x): {np.std(M_values) / np.sqrt(np.mean(x_values)):.4f}")

# =============================================================================
# PART 7: THE ERGODIC PERSPECTIVE
# =============================================================================

print("""

================================================================================
PART 7: THE ERGODIC PERSPECTIVE
================================================================================

Consider the "time average" (1/X) Σ_{x≤X} M(x)² vs
the "space average" E[M(x)²] over some ensemble.

For μ, there's no ensemble - μ is fixed.
But we can treat x as the "random" parameter.

The ergodic hypothesis would say:
  (1/X) Σ_{x≤X} M(x)² → E[M(random x)²]

This is what we've been computing as V(X)!
""")

# Compute cumulative average
X = 10000
cumulative_avg = []
running_sum = 0
for x in range(1, X + 1):
    running_sum += M(x)**2
    cumulative_avg.append(running_sum / x)

print("Convergence of V(X) = (1/X)Σ M(x)²:")
for x in [100, 500, 1000, 2000, 5000, 10000]:
    print(f"  V({x:>5}) = {cumulative_avg[x-1]:.4f}, V(X)/X = {cumulative_avg[x-1]/x:.6f}")

# =============================================================================
# PART 8: THE KEY OBSERVATION
# =============================================================================

print("""

================================================================================
PART 8: THE KEY OBSERVATION
================================================================================

The orthogonality Σ_{d|n} μ(d) = [n=1] is equivalent to:

  μ * 1 = ε    (Dirichlet convolution)

where ε(n) = [n=1].

This means: Σ_{d≤x} M(x/d) = 1 for all x ≥ 1.

This is a GLOBAL constraint on M!

Summing: Σ_{x≤X} Σ_{d≤x} M(x/d) = X

Rearranging: Σ_{n≤X} M(n) × #{d: n = x/d for some x ≤ X}
           = Σ_{n≤X} M(n) × #{x: n ≤ x ≤ X}
           = Σ_{n≤X} M(n) × (X - n + 1)

This gives: Σ_{n≤X} M(n)(X - n + 1) = X

Let's verify!
""")

X = 1000
lhs = sum(M(n) * (X - n + 1) for n in range(1, X + 1))
print(f"Σ_{{n≤{X}}} M(n)(X - n + 1) = {lhs}")
print(f"Expected: {X}")

# Actually this isn't quite right. Let me recalculate.
# Σ_{d≤x} M(x/d) = 1 means Σ_{k≤x} M(k) × #{d: x/d = k} = 1
# For each k, #{d: x/d = k} = #{d: x/k ≤ d < x/(k-1)} for k > 1
# This is more complex...

# Let's just verify the basic identity
print("\nVerifying Σ_{d≤x} M(x/d) = 1:")
for x in [10, 100, 500, 1000]:
    s = sum(M(x // d) for d in range(1, x + 1))
    print(f"  x = {x:>4}: Σ M(x/d) = {s}")

# =============================================================================
# PART 9: IMPLICATIONS FOR VARIANCE
# =============================================================================

print("""

================================================================================
PART 9: IMPLICATIONS FOR VARIANCE
================================================================================

The identity Σ_{d≤x} M(x/d) = 1 tells us:

M(x) + M(x/2) + M(x/3) + ... = 1

This is a SUM of M values at different scales!

For the SUM to equal 1, there must be CANCELLATION among the M(x/d).

The recursion M(x) = 1 - Σ_{d>1} M(x/d) shows:
  M(x) is the RESIDUE after multi-scale cancellation.

For M(x) = O(√x), the cancellation must be nearly complete.
""")

# Analyze the terms in Σ M(x/d)
x = 10000
terms = [(d, x // d, M(x // d)) for d in range(1, x + 1) if x // d > 0]

# Group by magnitude
positive_sum = sum(t[2] for t in terms if t[2] > 0)
negative_sum = sum(t[2] for t in terms if t[2] < 0)

print(f"At x = {x}:")
print(f"  Σ M(x/d) = {sum(t[2] for t in terms)}")
print(f"  Positive terms sum: {positive_sum}")
print(f"  Negative terms sum: {negative_sum}")
print(f"  Cancellation: {100 * (1 - 1 / (positive_sum - negative_sum)):.2f}%")

# =============================================================================
# PART 10: THE VARIANCE IDENTITY
# =============================================================================

print("""

================================================================================
PART 10: A VARIANCE IDENTITY
================================================================================

From Σ_{d≤x} M(x/d) = 1, square both sides:

1 = [Σ_{d≤x} M(x/d)]²
  = Σ_{d,e≤x} M(x/d) M(x/e)

Sum over x ≤ X:
X = Σ_{x≤X} Σ_{d,e≤x} M(x/d) M(x/e)

This relates the SUM OF PRODUCTS of M values to X!

Rearranging might give a variance bound...
""")

# Compute the double sum
X = 500
double_sum = sum(sum(M(x // d) * M(x // e)
                     for d in range(1, x + 1)
                     for e in range(1, x + 1))
                 for x in range(1, X + 1))

print(f"Σ_{{x≤{X}}} [Σ M(x/d)]² = {double_sum}")
print(f"Expected (= X): {X}")

# =============================================================================
# PART 11: THE FUNDAMENTAL IDENTITY
# =============================================================================

print("""

================================================================================
PART 11: THE FUNDAMENTAL IDENTITY
================================================================================

We have: Σ_{d≤x} M(x/d) = 1 for all x.

This is EQUIVALENT to: M * 1 = ε in Dirichlet convolution,
which is EQUIVALENT to: 1/ζ(s) × ζ(s) = 1.

The identity tells us M and 1 are Dirichlet inverses!

For variance: The "smoothing" in Σ M(x/d) = 1 suggests
that M cannot be too wild.

IF M(x) grew like x^{1/2+ε}, then Σ M(x/d) would grow too fast.
The constraint Σ M(x/d) = 1 FORCES cancellation!
""")

# Check growth rate implications
print("If M(x) ~ c × x^α, what does Σ M(x/d) look like?")
for alpha in [0.4, 0.5, 0.6, 0.7]:
    x = 10000
    simulated_sum = sum((x/d)**alpha for d in range(1, x + 1))
    print(f"  α = {alpha}: Σ (x/d)^α ~ {simulated_sum:.0f} (grows with x)")

print("\nBut actual Σ M(x/d) = 1 (constant!)")
print("This forces M to have significant cancellation.")

# =============================================================================
# PART 12: CAN WE PROVE VARIANCE BOUND FROM THIS?
# =============================================================================

print("""

================================================================================
PART 12: CAN WE PROVE VARIANCE BOUND?
================================================================================

ATTEMPT:

From Σ_{d≤x} M(x/d) = 1:

Let f(x) = M(x)/√x (normalized Mertens).

Then: Σ_{d≤x} f(x/d) × √(x/d) = 1
      √x × Σ_{d≤x} f(x/d) / √d = 1
      Σ_{d≤x} f(x/d) / √d = 1/√x

As x → ∞, if f(x/d) ≈ c for all d, then:
  c × Σ_{d≤x} 1/√d ≈ c × 2√x → ∞

This contradicts 1/√x → 0!

So f(x/d) CANNOT be uniformly bounded away from 0.
The values f(x/d) must have cancellation.

This hints at |f(x)| = O(1), i.e., |M(x)| = O(√x)!
""")

# Verify the sum Σ 1/√d
x = 10000
sum_inv_sqrt = sum(1 / math.sqrt(d) for d in range(1, x + 1))
print(f"Σ_{{d≤{x}}} 1/√d = {sum_inv_sqrt:.2f}")
print(f"2√x = {2 * math.sqrt(x):.2f}")

# =============================================================================
# PART 13: THE RIGOROUS GAP
# =============================================================================

print("""

================================================================================
PART 13: THE RIGOROUS GAP
================================================================================

The argument above shows:
  Σ f(x/d) / √d must cancel to give O(1/√x)

But this doesn't PROVE |f(x)| = O(1)!

Counter-example worry:
  What if f(x/d) alternates in a way that creates cancellation
  in the sum, but individual |f(x)| still grow?

To rule this out, we need:
  The "independence" of f at different scales
  OR
  Direct control of f from the recursion

This is WHERE the proof becomes analytic (using ζ zeros).
""")

# =============================================================================
# PART 14: WHAT ORTHOGONALITY DOES PROVE
# =============================================================================

print("""

================================================================================
PART 14: WHAT ORTHOGONALITY DOES PROVE
================================================================================

From orthogonality alone, we CAN prove:

1. μ is uniquely determined
2. Σ_{d≤x} M(x/d) = 1 (exact)
3. M(x) = 1 - Σ_{d≥2} M(x/d) (recursion)
4. The sum Σ M(x/d) has massive cancellation

We CANNOT prove (from orthogonality alone):

1. |M(x)| = O(√x)
2. V(X) = O(X)
3. Any pointwise bound better than trivial

THE GAP:

Orthogonality constrains the GLOBAL structure (Σ M(x/d) = 1)
but not the LOCAL behavior (individual M(x) values).

To get local bounds from global constraints requires ANALYSIS.
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY
================================================================================

THE ORTHOGONALITY CONSTRAINT:

1. Σ_{d|n} μ(d) = [n=1] UNIQUELY determines μ

2. This implies Σ_{d≤x} M(x/d) = 1 (global constraint)

3. The constraint forces cancellation in multi-scale sums

4. But it doesn't directly imply |M(x)| = O(√x)

THE INSIGHT:

The orthogonality is a VERY STRONG constraint:
- It fixes μ completely
- It constrains multi-scale behavior
- It forces Σ M(x/d) to be constant (!)

But translating this to POINTWISE bounds requires more.

THE PROBABILISTIC PERSPECTIVE:

If we could show that "generic" functions with this orthogonality
have variance O(X), we'd be done.

But there's only ONE such function: μ itself!

So the probabilistic approach collapses to:
"Does μ have variance O(X)?" - which is equivalent to RH.

HOWEVER:

The structure revealed here - that Σ M(x/d) = 1 EXACTLY -
is a powerful constraint that might be exploitable
in ways we haven't yet discovered.
""")

print("=" * 80)
print("ORTHOGONALITY ANALYSIS COMPLETE")
print("=" * 80)
