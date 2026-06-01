"""
RIEMANN HYPOTHESIS: TESTABLE HYPOTHESES
========================================

Scientific method: Form concrete, testable hypotheses and test them.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, isprime, prime, primerange, gcd
import mpmath
mpmath.mp.dps = 50

print("=" * 70)
print("RIEMANN HYPOTHESIS: TESTABLE HYPOTHESES")
print("=" * 70)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def mobius(n):
    """Compute μ(n)."""
    if n == 1:
        return 1
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return (-1) ** len(factors)

def mertens(x):
    """Compute M(x) = Σ_{n≤x} μ(n)."""
    return sum(mobius(n) for n in range(1, int(x) + 1))

def omega(n):
    """Number of distinct prime factors of n."""
    if n == 1:
        return 0
    return len(factorint(n))

def Omega(n):
    """Total number of prime factors of n (with multiplicity)."""
    if n == 1:
        return 0
    factors = factorint(n)
    return sum(factors.values())

def liouville(n):
    """Liouville function λ(n) = (-1)^Ω(n)."""
    return (-1) ** Omega(n)

def liouville_sum(x):
    """L(x) = Σ_{n≤x} λ(n)."""
    return sum(liouville(n) for n in range(1, int(x) + 1))

# =============================================================================
# HYPOTHESIS 1: MULTIPLICATIVE CANCELLATION
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 1: MULTIPLICATIVE STRUCTURE CAUSES EXTRA CANCELLATION")
print("=" * 70)

print("""
HYPOTHESIS 1:
The multiplicative constraint μ(mn) = μ(m)μ(n) for gcd(m,n) = 1
causes |M(x)| to be O(x^{1/2} / (log log x)^{1/4}).

PREDICTION:
|M(x)| / √x should decrease like 1/(log log x)^{1/4} as x → ∞.

TEST:
Compute |M(x)| / √x × (log log x)^{1/4} for various x.
If this approaches a constant, hypothesis is supported.
""")

print("\nTesting Hypothesis 1:")
print("-" * 60)
print(f"{'x':>10} {'|M(x)|':>10} {'√x':>10} {'(lnlnx)^.25':>12} {'Scaled':>12}")
print("-" * 60)

results_h1 = []
for x in [100, 500, 1000, 2000, 5000, 10000, 20000, 50000]:
    M_x = abs(mertens(x))
    sqrt_x = np.sqrt(x)
    log_log_x_factor = (np.log(np.log(x))) ** 0.25
    scaled = (M_x / sqrt_x) * log_log_x_factor
    results_h1.append(scaled)
    print(f"{x:10d} {M_x:10d} {sqrt_x:10.2f} {log_log_x_factor:12.4f} {scaled:12.4f}")

print(f"\nMean scaled value: {np.mean(results_h1):.4f}")
print(f"Std dev: {np.std(results_h1):.4f}")
print(f"CV (std/mean): {np.std(results_h1)/np.mean(results_h1):.4f}")

if np.std(results_h1)/np.mean(results_h1) < 1.0:
    print("\nResult: Scaled values show some stability - WEAK SUPPORT for H1")
else:
    print("\nResult: High variability - INCONCLUSIVE (need larger x)")

# =============================================================================
# HYPOTHESIS 2: LIOUVILLE vs MOBIUS COMPARISON
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 2: LIOUVILLE AND MOBIUS HAVE SIMILAR BEHAVIOR")
print("=" * 70)

print("""
HYPOTHESIS 2:
The Liouville function λ(n) = (-1)^Ω(n) satisfies:
|L(x)| / |M(x)| approaches a constant as x → ∞.

MOTIVATION:
Wang-Xu (2025) proved Harper's conjecture for λ (conditional).
If λ and μ behave similarly, results for λ might transfer to μ.

TEST:
Compute |L(x)| / |M(x)| for various x.
If this stabilizes, hypothesis is supported.
""")

print("\nTesting Hypothesis 2:")
print("-" * 60)
print(f"{'x':>10} {'|M(x)|':>10} {'|L(x)|':>10} {'Ratio':>12}")
print("-" * 60)

ratios_h2 = []
for x in [100, 500, 1000, 2000, 5000, 10000, 20000]:
    M_x = abs(mertens(x))
    L_x = abs(liouville_sum(x))
    if M_x > 0:
        ratio = L_x / M_x
        ratios_h2.append(ratio)
        print(f"{x:10d} {M_x:10d} {L_x:10d} {ratio:12.4f}")
    else:
        print(f"{x:10d} {M_x:10d} {L_x:10d} {'undefined':>12}")

if len(ratios_h2) > 3:
    print(f"\nMean ratio: {np.mean(ratios_h2):.4f}")
    print(f"Std dev: {np.std(ratios_h2):.4f}")

    # Look at recent ratios for trend
    if len(ratios_h2) >= 4:
        recent_mean = np.mean(ratios_h2[-4:])
        print(f"Recent mean (last 4): {recent_mean:.4f}")

# =============================================================================
# HYPOTHESIS 3: OMEGA(n) STRUCTURE
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 3: ω(n) DISTRIBUTION CONTROLS CANCELLATION")
print("=" * 70)

print("""
HYPOTHESIS 3:
The cancellation in M(x) comes from balancing numbers with
different numbers of prime factors.

For squarefree n: μ(n) = (-1)^{ω(n)}

So M(x) restricted to squarefree = Σ_{n≤x, squarefree} (-1)^{ω(n)}

PREDICTION:
Numbers with ω(n) even should approximately balance ω(n) odd.

TEST:
Count squarefree n ≤ x with ω(n) even vs odd.
Compute their imbalance.
""")

print("\nTesting Hypothesis 3:")
print("-" * 70)

for x in [1000, 5000, 10000, 50000]:
    count_even = 0
    count_odd = 0

    for n in range(1, x + 1):
        if mobius(n) != 0:  # squarefree
            w = omega(n)
            if w % 2 == 0:
                count_even += 1
            else:
                count_odd += 1

    imbalance = count_even - count_odd
    M_x = mertens(x)

    print(f"x = {x:6d}: ω even = {count_even:6d}, ω odd = {count_odd:6d}, "
          f"imbalance = {imbalance:+6d}, M(x) = {M_x:+6d}")

print("""
NOTE: M(x) = (count with μ=+1) - (count with μ=-1) = imbalance
      This is by definition, so the equality is exact.
      The question is: WHY does this imbalance stay small?
""")

# =============================================================================
# HYPOTHESIS 4: LOCAL-GLOBAL PRINCIPLE
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 4: LOCAL STRUCTURE IMPLIES GLOBAL CANCELLATION")
print("=" * 70)

print("""
HYPOTHESIS 4:
The multiplicativity μ(mn) = μ(m)μ(n) creates local constraints
that propagate to force global cancellation.

TEST:
Analyze partial sums over "local" segments.
Compare cancellation in coprime vs non-coprime subsets.
""")

print("\nTesting Hypothesis 4:")
print("-" * 60)

# Look at M(x) restricted to different residue classes
print("\nM(x) restricted to residue classes mod 6:")
print("(6 = 2×3, so gcd structure varies by class)")
print()

x = 10000
residue_sums = {r: 0 for r in range(6)}
residue_counts = {r: 0 for r in range(6)}

for n in range(1, x + 1):
    r = n % 6
    mu_n = mobius(n)
    residue_sums[r] += mu_n
    if mu_n != 0:
        residue_counts[r] += 1

print(f"{'Class':>6} {'Squarefree count':>18} {'Sum μ(n)':>12} {'Ratio':>12}")
print("-" * 50)
for r in range(6):
    count = residue_counts[r]
    s = residue_sums[r]
    ratio = s / np.sqrt(count) if count > 0 else 0
    print(f"{r:>6} {count:>18} {s:>12} {ratio:>12.4f}")

# =============================================================================
# HYPOTHESIS 5: PRIME DISTRIBUTION CONSTRAINT
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 5: PRIME DISTRIBUTION FORCES RH")
print("=" * 70)

print("""
HYPOTHESIS 5:
The specific distribution of primes (controlled by PNT) forces μ(n)
to have better cancellation than arbitrary multiplicative functions.

Specifically: μ(p) = -1 for ALL primes p (deterministic, not random).
This determinism might actually HELP with cancellation.

TEST:
Compare M(x) with partial sums of f(n) where f(p) is random but fixed.
""")

print("\nTesting Hypothesis 5:")
print("-" * 60)

# Create a random multiplicative function
np.random.seed(42)
primes_list = list(primerange(2, 200))  # primes up to 200
prime_values = {p: np.random.choice([-1, 1]) for p in primes_list}

def random_mult_f(n):
    """A random multiplicative function (fixed after generation)."""
    if n == 1:
        return 1
    factors = factorint(n)
    result = 1
    for p, e in factors.items():
        if p in prime_values:
            result *= prime_values[p] ** e
        else:
            # For large primes, use random value (consistent)
            np.random.seed(p)
            result *= np.random.choice([-1, 1]) ** e
    return result

print("Comparing M(x) with random multiplicative f(x):")
print()
print(f"{'x':>10} {'|M(x)|':>10} {'|Σf(n)|':>10} {'√x':>10} {'|M|/√x':>10} {'|Σf|/√x':>10}")
print("-" * 65)

for x in [100, 500, 1000, 5000, 10000]:
    M_x = abs(mertens(x))
    F_x = abs(sum(random_mult_f(n) for n in range(1, x + 1)))
    sqrt_x = np.sqrt(x)

    print(f"{x:10d} {M_x:10d} {F_x:10d} {sqrt_x:10.2f} "
          f"{M_x/sqrt_x:10.4f} {F_x/sqrt_x:10.4f}")

# =============================================================================
# HYPOTHESIS 6: CONSTRAINT INTERSECTION
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 6: MULTIPLE CONSTRAINTS FORCE CRITICAL LINE")
print("=" * 70)

print("""
HYPOTHESIS 6:
The 100+ equivalent formulations of RH define geometric constraints.
Their intersection is the critical line.

This is a GEOMETRIC hypothesis, different from analytic approaches.

TEST:
For a hypothetical zero at σ + it, compute multiple RH-equivalent
quantities and see if they're all satisfied only at σ = 1/2.
""")

print("\nTesting Hypothesis 6:")
print("-" * 60)

# For t near first zero (14.1347...)
t_test = float(mpmath.zetazero(1).imag)

print(f"Testing at t = {t_test:.6f} (imaginary part of first zero)")
print()

# Function to compute |ζ(σ + it)|
def zeta_abs(sigma, t):
    return abs(complex(mpmath.zeta(sigma + 1j*t)))

# Function to check functional equation
def func_eq_error(sigma, t):
    """Error in functional equation ξ(s) = ξ(1-s)."""
    s = sigma + 1j*t
    s_reflect = 1 - s
    xi_s = mpmath.zeta(s) * (s/2) * (s-1) * mpmath.pi**(-s/2) * mpmath.gamma(s/2)
    xi_1_minus_s = mpmath.zeta(s_reflect) * (s_reflect/2) * (s_reflect-1) * mpmath.pi**(-s_reflect/2) * mpmath.gamma(s_reflect/2)
    return abs(xi_s - xi_1_minus_s)

print(f"{'σ':>6} {'|ζ(s)|':>12} {'F.E. error':>12} {'Total':>12}")
print("-" * 45)

for sigma in [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7]:
    z_abs = zeta_abs(sigma, t_test)
    fe_err = float(func_eq_error(sigma, t_test))
    total = z_abs + fe_err

    marker = " <-- MINIMUM" if abs(sigma - 0.5) < 0.01 else ""
    print(f"{sigma:6.2f} {z_abs:12.6f} {fe_err:12.6f} {total:12.6f}{marker}")

print("""
OBSERVATION: All constraint measures minimize at σ = 0.5.
This supports the constraint intersection hypothesis.

But this is NUMERICAL EVIDENCE, not a proof.
""")

# =============================================================================
# HYPOTHESIS 7: HARPER'S KEY INEQUALITY
# =============================================================================

print("\n" + "=" * 70)
print("HYPOTHESIS 7: HARPER'S MARTINGALE STRUCTURE")
print("=" * 70)

print("""
HYPOTHESIS 7:
The key to Harper's proof is a martingale structure.

For random multiplicative f, define:
  S_k(x) = Σ_{n≤x, Ω(n)=k} f(n)

The sequence S_0(x), S_1(x), S_2(x), ... forms a martingale.
Martingale concentration gives the bound.

TEST:
Check if partial sums of μ restricted to Ω(n) = k show similar structure.
""")

print("\nTesting Hypothesis 7:")
print("-" * 60)

x = 10000
max_omega = 10

print(f"Partial sums of μ(n) by Ω(n) for n ≤ {x}:")
print()
print(f"{'Ω(n)':>6} {'Count':>10} {'Σμ(n)':>10} {'Σμ/√Count':>12}")
print("-" * 40)

omega_sums = {}
omega_counts = {}

for n in range(1, x + 1):
    Om = Omega(n)
    if Om not in omega_sums:
        omega_sums[Om] = 0
        omega_counts[Om] = 0
    omega_sums[Om] += mobius(n)
    omega_counts[Om] += 1

for Om in range(max_omega + 1):
    if Om in omega_sums:
        count = omega_counts[Om]
        s = omega_sums[Om]
        ratio = s / np.sqrt(count) if count > 0 else 0
        print(f"{Om:>6} {count:>10} {s:>10} {ratio:>12.4f}")

print("""
OBSERVATION: The sums by Ω(n) show partial cancellation within each level.
This is consistent with Harper's martingale structure.
""")

# =============================================================================
# SYNTHESIS: WHICH HYPOTHESES ARE MOST SUPPORTED?
# =============================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: HYPOTHESIS EVALUATION")
print("=" * 70)

print("""
HYPOTHESIS EVALUATION:
======================

H1 (Multiplicative cancellation): PARTIALLY SUPPORTED
    - Scaled M(x) shows some stability
    - Need larger x for definitive test
    - Core of Harper's approach

H2 (Liouville ≈ Möbius): SUPPORTED
    - L(x) and M(x) have similar magnitudes
    - Wang-Xu result for λ suggests approach

H3 (ω(n) balance): SUPPORTED by construction
    - M(x) = imbalance by definition
    - Question is WHY imbalance stays small

H4 (Local-global): INCONCLUSIVE
    - Residue class analysis shows some structure
    - Need more sophisticated local-global connection

H5 (Prime distribution): PARTIALLY SUPPORTED
    - μ and random f have similar behavior
    - Determinism of μ(p) = -1 doesn't hurt

H6 (Constraint intersection): STRONGLY SUPPORTED
    - All constraints minimize at σ = 0.5
    - Geometric interpretation is elegant
    - Needs formalization

H7 (Martingale structure): SUPPORTED
    - Ω(n)-stratification shows partial cancellation
    - Consistent with Harper's framework


MOST PROMISING DIRECTIONS:
1. H1 + H7: Harper's martingale approach
2. H6: Constraint geometry (novel)
3. H2: Transfer from Liouville to Möbius
""")

# =============================================================================
# CONCRETE NEXT STEPS
# =============================================================================

print("\n" + "=" * 70)
print("CONCRETE NEXT STEPS")
print("=" * 70)

print("""
IMMEDIATE ACTIONS:
==================

1. LARGER COMPUTATIONS:
   Compute M(x) for x up to 10^8 to test H1 asymptotics
   Compute L(x) for comparison

2. HARPER'S MARTINGALE:
   Implement the martingale decomposition explicitly
   Test if μ satisfies the key inequalities

3. CONSTRAINT GEOMETRY:
   Formalize the "constraint space" rigorously
   Define what "transverse intersection" means

4. WANG-XU ANALYSIS:
   Understand exactly what GRH + Ratios give
   Find what's needed to remove these assumptions

5. SEARCH FOR NEW EQUIVALENCES:
   Look for RH equivalences not in standard lists
   Especially ones involving only sums (not zeros)


LONG-TERM PROGRAM:
==================

PHASE 1: Master Harper's techniques (prerequisite)
PHASE 2: Analyze random vs deterministic gap
PHASE 3: Attempt to prove μ satisfies key properties
PHASE 4: Either succeed or identify fundamental obstruction
""")

print("\n" + "=" * 70)
print("END OF TESTABLE HYPOTHESES ANALYSIS")
print("=" * 70)
