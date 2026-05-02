"""
RIEMANN HYPOTHESIS: RIGOROUS PROOF ATTEMPTS
============================================

Developing formal proof strategies based on tested hypotheses.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, isprime, prime, primerange, binomial, factorial
from sympy import log as symlog, sqrt as symsqrt
import mpmath
mpmath.mp.dps = 100  # High precision

print("=" * 70)
print("RIEMANN HYPOTHESIS: RIGOROUS PROOF ATTEMPTS")
print("=" * 70)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def mobius(n):
    if n == 1:
        return 1
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return (-1) ** len(factors)

def mertens(x):
    return sum(mobius(n) for n in range(1, int(x) + 1))

def Omega(n):
    if n == 1:
        return 0
    return sum(factorint(n).values())

def omega(n):
    if n == 1:
        return 0
    return len(factorint(n))

# =============================================================================
# PROOF ATTEMPT 1: MULTIPLICATIVE MARTINGALE APPROACH
# =============================================================================

print("\n" + "=" * 70)
print("PROOF ATTEMPT 1: MULTIPLICATIVE MARTINGALE APPROACH")
print("=" * 70)

print("""
STRATEGY:
Adapt Harper's martingale proof for random multiplicative functions
to the deterministic Möbius function.

HARPER'S KEY INSIGHT:
For random multiplicative f with f(p) = ±1 uniform:
  Define F_k(x) = Σ_{n≤x, p(n)>y_k} f(n)
  where y_k = exp(exp(k/K * log log x))

Then F_0, F_1, ..., F_K forms a martingale with bounded increments.

ADAPTATION TO μ:
Replace random f(p) with deterministic μ(p) = -1.
Check if martingale structure survives.
""")

print("\nStep 1: Define the filtration for μ")
print("-" * 50)

def partition_by_smallest_prime_factor(x, threshold):
    """
    Partition integers n ≤ x by whether smallest prime factor p(n) > threshold.
    """
    count_large = 0
    sum_large = 0
    count_small = 0
    sum_small = 0

    for n in range(1, int(x) + 1):
        if n == 1:
            count_large += 1
            sum_large += mobius(1)
        else:
            factors = factorint(n)
            smallest_prime = min(factors.keys())
            if smallest_prime > threshold:
                count_large += 1
                sum_large += mobius(n)
            else:
                count_small += 1
                sum_small += mobius(n)

    return {
        'large': {'count': count_large, 'sum': sum_large},
        'small': {'count': count_small, 'sum': sum_small}
    }

x = 10000
print(f"\nPartitioning n ≤ {x} by smallest prime factor threshold:")
for threshold in [2, 5, 10, 20, 50]:
    result = partition_by_smallest_prime_factor(x, threshold)
    print(f"  Threshold {threshold:3d}: "
          f"p(n)>{threshold}: count={result['large']['count']:5d}, Σμ={result['large']['sum']:+5d}  |  "
          f"p(n)≤{threshold}: count={result['small']['count']:5d}, Σμ={result['small']['sum']:+5d}")

print("\nStep 2: Analyze martingale increments")
print("-" * 50)

print("""
For Harper's proof to work, we need:
  |F_k - F_{k-1}| to be "small" (bounded by some function of k)

This requires showing that adding integers with p(n) in [y_{k-1}, y_k]
doesn't change the sum by much.

KEY LEMMA NEEDED:
  For μ(n), the contribution from n with p(n) ∈ [y, z] is small.
""")

def contribution_by_smallest_prime_range(x, y_low, y_high):
    """
    Sum μ(n) for n ≤ x with y_low < p(n) ≤ y_high.
    """
    total = 0
    count = 0

    for n in range(2, int(x) + 1):
        factors = factorint(n)
        smallest_prime = min(factors.keys())
        if y_low < smallest_prime <= y_high:
            total += mobius(n)
            count += 1

    return total, count

print(f"\nContributions by smallest prime factor range (x = {x}):")
ranges = [(2, 3), (3, 7), (7, 13), (13, 23), (23, 50), (50, 100)]
for y_low, y_high in ranges:
    contribution, count = contribution_by_smallest_prime_range(x, y_low, y_high)
    if count > 0:
        contrib_per_sqrt = contribution / np.sqrt(count) if count > 0 else 0
        print(f"  p(n) ∈ ({y_low:3d}, {y_high:3d}]: "
              f"count = {count:5d}, Σμ = {contribution:+5d}, "
              f"Σμ/√count = {contrib_per_sqrt:+.4f}")

print("""
OBSERVATION:
The contributions per √count are bounded, which is consistent with
martingale-type behavior. But this doesn't PROVE the bound needed.

THE GAP:
Harper's proof uses E[|F_k - F_{k-1}|²] bounds.
For random f, this is tractable because E[f(n)f(m)] = 0 for n ≠ m.
For deterministic μ, we need different techniques.
""")

# =============================================================================
# PROOF ATTEMPT 2: CONSTRAINT GEOMETRY APPROACH
# =============================================================================

print("\n" + "=" * 70)
print("PROOF ATTEMPT 2: CONSTRAINT GEOMETRY APPROACH")
print("=" * 70)

print("""
STRATEGY:
Formalize the "100+ equivalent formulations" as geometric constraints.
Show their intersection is exactly the critical line.

STEP 1: Define the configuration space
STEP 2: Define each constraint as a geometric object
STEP 3: Prove transversality/independence
STEP 4: Compute intersection
""")

print("\nStep 1: Configuration Space Definition")
print("-" * 50)

print("""
DEFINITION (Configuration Space):
Let C be the space of possible zero configurations for ζ(s).

Formally, C could be:
  (a) The space of all closed subsets of the critical strip
  (b) The space of all analytic functions with same pole/trivial zeros as ζ
  (c) A moduli space parameterizing deformations of ζ

PROBLEM: Each choice has technical issues.
  (a) Too general - includes non-analytic configurations
  (b) Infinite-dimensional, hard to do intersection theory
  (c) Most natural but needs algebraic geometry expertise

For now, let's work with FINITE approximations.
""")

print("\nStep 2: Constraint Definition (Finite Approximation)")
print("-" * 50)

print("""
Consider the first N zeros ρ₁, ..., ρ_N.
Configuration: a point in ℂ^N (or ℝ^N if we fix imaginary parts).

CONSTRAINT 1: ζ(ρ_j) = 0
  This defines a hypersurface H₁ in ℂ^N.

CONSTRAINT 2: Functional equation symmetry
  ρ_j and 1-ρ_j are both zeros.
  This defines a hypersurface H₂.

CONSTRAINT 3: Conjugate symmetry
  ρ_j and ρ̄_j are both zeros.
  This defines H₃.

CONSTRAINT 4: GUE statistics
  Pair correlation matches GUE prediction.
  This defines H₄ (probabilistic constraint).

The hypothesis: H₁ ∩ H₂ ∩ H₃ ∩ H₄ ∩ ... = {Re(ρ_j) = 1/2 for all j}
""")

print("\nStep 3: Numerical Test of Constraint Independence")
print("-" * 50)

# For each of the first few zeros, measure how multiple constraints
# behave as we vary σ away from 1/2

t_values = [float(mpmath.zetazero(k).imag) for k in range(1, 6)]

print("Testing constraint independence for first 5 zeros:")
print()

def constraint_vector(sigma, t):
    """Compute a vector of constraint violations at σ + it."""
    s = complex(sigma, t)

    # C1: |ζ(s)|
    c1 = abs(complex(mpmath.zeta(s)))

    # C2: |ζ(s) - ζ(1-s̄)| (should be 0 by functional equation at zeros)
    s_reflect = complex(1 - sigma, t)
    c2 = abs(complex(mpmath.zeta(s)) - complex(mpmath.zeta(s_reflect)))

    # C3: d|ζ|/dσ at the zero (should be 0 at critical line if minimum)
    h = 0.001
    grad = (abs(complex(mpmath.zeta(sigma + h + 1j*t))) -
            abs(complex(mpmath.zeta(sigma - h + 1j*t)))) / (2*h)
    c3 = abs(grad)

    return np.array([c1, c2, c3])

# Check if constraints are violated similarly or differently
print(f"{'t':>10} {'σ':>6} {'|ζ|':>10} {'|ζ-ζ_refl|':>12} {'|∂ζ/∂σ|':>12}")
print("-" * 55)

for t in t_values[:3]:
    for sigma in [0.4, 0.45, 0.5, 0.55, 0.6]:
        cv = constraint_vector(sigma, t)
        marker = " <--" if abs(sigma - 0.5) < 0.01 else ""
        print(f"{t:10.4f} {sigma:6.2f} {cv[0]:10.6f} {cv[1]:12.6f} {cv[2]:12.6f}{marker}")
    print()

print("""
OBSERVATION:
All three constraints minimize at σ = 0.5.
But they all measure essentially the same thing: distance from zero.

THE PROBLEM:
The constraints are NOT independent - they're all equivalent to ζ(s)=0.
This is why constraint geometry is hard to formalize.

WHAT WOULD MAKE IT WORK:
Find constraints that are:
  1. Logically independent (different mathematical content)
  2. Still all satisfied on the critical line
  3. Transverse (intersect properly)
""")

# =============================================================================
# PROOF ATTEMPT 3: POSITIVITY FROM PRIME STRUCTURE
# =============================================================================

print("\n" + "=" * 70)
print("PROOF ATTEMPT 3: POSITIVITY FROM PRIME STRUCTURE")
print("=" * 70)

print("""
STRATEGY:
The prime distribution satisfies PNT: π(x) ~ x/ln(x).
This is PROVEN. Can we derive RH-level cancellation from PNT?

KEY FACT (Proven):
  PNT ⟺ ζ(s) ≠ 0 on Re(s) = 1

We want:
  ??? ⟺ ζ(s) ≠ 0 on Re(s) > 1/2

What property of primes would give this?
""")

print("\nAnalyzing prime distribution for patterns:")
print("-" * 50)

# Look at prime gaps and their distribution
primes = list(primerange(2, 10000))
gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]

print(f"Primes up to 10000: {len(primes)}")
print(f"Mean gap: {np.mean(gaps):.4f}")
print(f"Std gap: {np.std(gaps):.4f}")
print(f"Max gap: {max(gaps)}")

# Distribution of gaps
from collections import Counter
gap_counts = Counter(gaps)
print("\nGap distribution (top 10):")
for gap, count in sorted(gap_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  Gap {gap:3d}: {count:4d} times ({100*count/len(gaps):.1f}%)")

print("""
OBSERVATION:
Prime gaps show structure (multiples of 2 dominate for obvious reasons).
But this structure doesn't obviously connect to RH.

THE CHALLENGE:
PNT gives the AVERAGE behavior of primes.
RH requires control over FLUCTUATIONS.
Converting average to fluctuation bounds is the gap.
""")

# =============================================================================
# PROOF ATTEMPT 4: DIRICHLET SERIES APPROACH
# =============================================================================

print("\n" + "=" * 70)
print("PROOF ATTEMPT 4: DIRICHLET SERIES APPROACH")
print("=" * 70)

print("""
STRATEGY:
1/ζ(s) = Σ μ(n)/n^s for Re(s) > 1.

If this series converges for Re(s) > 1/2, then ζ(s) ≠ 0 there.

Convergence at s = σ requires:
  Σ |μ(n)|/n^σ < ∞, which holds for σ > 1
  But more subtly: Σ μ(n)/n^σ needs conditional convergence for 1/2 < σ < 1

This happens iff M(x) = O(x^{1-σ+ε}), which for σ = 1/2 gives M(x) = O(x^{1/2+ε}).

So this reduces to proving M(x) bound - circular!
""")

# Numerical check of Dirichlet series convergence
print("\nNumerical check: Partial sums of Σμ(n)/n^σ")
print("-" * 50)

def partial_dirichlet_sum(x, sigma):
    """Compute Σ_{n≤x} μ(n)/n^σ."""
    return sum(mobius(n) / n**sigma for n in range(1, int(x) + 1))

print(f"{'x':>10} {'σ=0.75':>12} {'σ=1.00':>12} {'σ=1.25':>12}")
print("-" * 50)
for x in [100, 500, 1000, 5000, 10000]:
    s075 = partial_dirichlet_sum(x, 0.75)
    s100 = partial_dirichlet_sum(x, 1.00)
    s125 = partial_dirichlet_sum(x, 1.25)
    print(f"{x:10d} {s075:12.6f} {s100:12.6f} {s125:12.6f}")

print(f"\n1/ζ values for comparison:")
print(f"  1/ζ(0.75) = {float(1/mpmath.zeta(0.75)):.6f}")
print(f"  1/ζ(1.00) = 0 (pole)")
print(f"  1/ζ(1.25) = {float(1/mpmath.zeta(1.25)):.6f}")

# =============================================================================
# PROOF ATTEMPT 5: EXPLICIT FORMULA INVERSION
# =============================================================================

print("\n" + "=" * 70)
print("PROOF ATTEMPT 5: EXPLICIT FORMULA INVERSION")
print("=" * 70)

print("""
STRATEGY:
The explicit formula connects primes to zeros:
  ψ(x) = x - Σ_ρ x^ρ/ρ - log(2π) - (1/2)log(1-x^{-2})

Inverting: If we KNOW ψ(x) precisely, we can determine zero locations.

IDEA:
We can compute ψ(x) = Σ_{p^k ≤ x} log(p) directly from primes.
Can we show the sum over zeros must have Re(ρ) = 1/2?
""")

def psi_chebyshev(x):
    """Compute ψ(x) = Σ_{p^k ≤ x} log(p)."""
    total = 0
    for p in primerange(2, int(x) + 1):
        pk = p
        while pk <= x:
            total += np.log(p)
            pk *= p
    return total

print("\nComputing ψ(x) and comparing to x:")
print("-" * 50)
print(f"{'x':>10} {'ψ(x)':>15} {'x':>10} {'ψ(x)/x':>10} {'Error/√x':>12}")
print("-" * 60)

for x in [100, 500, 1000, 5000, 10000]:
    psi = psi_chebyshev(x)
    error = psi - x
    error_scaled = error / np.sqrt(x)
    print(f"{x:10d} {psi:15.4f} {x:10d} {psi/x:10.6f} {error_scaled:+12.4f}")

print("""
OBSERVATION:
|ψ(x) - x| / √x is bounded, consistent with RH.

THE PROBLEM:
This is the OBSERVATION we want to prove, not a proof technique.
To prove RH via explicit formula, we'd need to show the zero sum
can only cancel properly if Re(ρ) = 1/2.
""")

# =============================================================================
# PROOF ATTEMPT 6: MOMENT ANALYSIS
# =============================================================================

print("\n" + "=" * 70)
print("PROOF ATTEMPT 6: MOMENT ANALYSIS")
print("=" * 70)

print("""
STRATEGY:
Analyze moments of M(x):
  M_k(X) = (1/X) ∫₁^X M(x)^k dx / x^{k/2}

RH implies M_k(X) converges as X → ∞.

Can we prove convergence directly?
""")

def compute_moment(X, k, num_samples=100):
    """Approximate moment M_k(X) by sampling."""
    x_values = np.linspace(10, X, num_samples)
    integrand = []
    for x in x_values:
        M_x = mertens(x)
        integrand.append((M_x / x**(0.5))**k)
    return np.mean(integrand)

print("\nMoment analysis:")
print("-" * 50)

X = 5000
print(f"Computing moments for X = {X}")
print(f"{'k':>5} {'M_k(X)':>15}")
print("-" * 22)
for k in [1, 2, 3, 4]:
    moment = compute_moment(X, k)
    print(f"{k:5d} {moment:15.6f}")

print("""
OBSERVATION:
Moments appear bounded, consistent with RH.

THE CHALLENGE:
Proving moment bounds requires knowing M(x) doesn't have large peaks.
But that's essentially what we're trying to prove.
""")

# =============================================================================
# SYNTHESIS: ASSESSMENT OF PROOF ATTEMPTS
# =============================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: ASSESSMENT OF ALL PROOF ATTEMPTS")
print("=" * 70)

print("""
ATTEMPT 1 (Martingale):
  Status: PARTIALLY VIABLE
  Gap: Need to prove martingale concentration for deterministic μ
  Next: Study Harper's exact lemmas, check if they hold for μ

ATTEMPT 2 (Constraint Geometry):
  Status: CONCEPTUALLY PROMISING, TECHNICALLY BLOCKED
  Gap: Constraints are not truly independent
  Next: Find genuinely independent constraints if they exist

ATTEMPT 3 (Prime Structure):
  Status: BLOCKED
  Gap: PNT gives averages, we need fluctuation control
  Next: Study theorems connecting PNT to fluctuations

ATTEMPT 4 (Dirichlet Series):
  Status: CIRCULAR
  Gap: Convergence requires M(x) bound, which is RH
  Not viable as independent approach

ATTEMPT 5 (Explicit Formula):
  Status: OBSERVATIONS ONLY
  Gap: Can't prove zeros must be on line from prime sums
  Not a proof technique, just a reformulation

ATTEMPT 6 (Moments):
  Status: CIRCULAR
  Gap: Moment bounds require M(x) bounds
  Not an independent approach


MOST VIABLE: Martingale approach (Attempt 1)
MOST NOVEL: Constraint geometry (Attempt 2)

FUNDAMENTAL OBSTRUCTION:
Every approach eventually needs to prove something about M(x) or zeros
that is equivalent to RH. Breaking this circularity requires a genuinely
new insight.
""")

# =============================================================================
# THE KEY QUESTION REFINED
# =============================================================================

print("\n" + "=" * 70)
print("THE KEY QUESTION REFINED")
print("=" * 70)

print("""
After all proof attempts, the question crystallizes:

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  What is special about μ(n) = (-1)^{ω(n)} × 1_{n squarefree}       │
│  that forces Σμ(n) to be smaller than Σ(random ±1)?                │
│                                                                     │
│  We know:                                                          │
│  • Multiplicativity μ(mn) = μ(m)μ(n) for gcd(m,n) = 1              │
│  • Vanishing on squares: μ(n) = 0 if n has squared factor          │
│  • Determinism: μ(p) = -1 for ALL primes p                         │
│                                                                     │
│  These properties together cause cancellation.                      │
│  But WHY? What is the mechanism?                                   │
│                                                                     │
│  Harper showed: RANDOM multiplicative functions have cancellation   │
│  Wang-Xu showed: LIOUVILLE (under GRH+Ratios) has cancellation      │
│                                                                     │
│  The gap: Prove MÖBIUS has cancellation unconditionally             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

To close this gap, we need EITHER:
  (A) Show μ is "random enough" despite being deterministic
  (B) Find a property P of μ that implies cancellation without randomness
  (C) A completely new approach not yet conceived

Option (A) is Harper's program.
Option (B) is the holy grail.
Option (C) would be a revolution.
""")

print("\n" + "=" * 70)
print("END OF PROOF ATTEMPTS ANALYSIS")
print("=" * 70)
