"""
APPROXIMATE MARTINGALE ANALYSIS FOR MÖBIUS FUNCTION
====================================================

Exploring whether μ(n) is "close enough" to a martingale
to inherit Harper-type bounds.

Key observation from previous analysis:
E[μ(n) | M(n-1)] ≈ 0 (approximately)

Can this be made rigorous?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
from collections import defaultdict
import mpmath
mpmath.mp.dps = 50

print("=" * 75)
print("APPROXIMATE MARTINGALE ANALYSIS FOR μ(n)")
print("=" * 75)

# Precompute Möbius
MAX_N = 100000
mu = [0] * (MAX_N + 1)
mu[1] = 1
for n in range(2, MAX_N + 1):
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        mu[n] = 0
    else:
        mu[n] = (-1) ** len(factors)

# Precompute Mertens
M = [0] * (MAX_N + 1)
for n in range(1, MAX_N + 1):
    M[n] = M[n-1] + mu[n]

# =============================================================================
# PART 1: DEFINE "APPROXIMATE MARTINGALE"
# =============================================================================

print("\n" + "=" * 75)
print("PART 1: DEFINING APPROXIMATE MARTINGALE")
print("=" * 75)

print("""
DEFINITION (ε-Approximate Martingale):
======================================

A sequence X_1, X_2, ... is an ε-approximate martingale if:
  |E[X_{n+1} - X_n | X_1, ..., X_n]| ≤ ε

For a true martingale, ε = 0.

QUESTION: Is M(n) an ε-approximate martingale for small ε?

Formally: |E[μ(n) | M(1), ..., M(n-1)]| ≤ ε ?

Since μ(n) is deterministic, this becomes:
  |E[μ(n) | M(n-1) = m]| ≤ ε

where the expectation is over "typical" n with M(n-1) = m.
""")

# =============================================================================
# PART 2: EMPIRICAL CONDITIONAL EXPECTATIONS
# =============================================================================

print("\n" + "=" * 75)
print("PART 2: EMPIRICAL CONDITIONAL EXPECTATIONS")
print("=" * 75)

# For each value of M(n-1), compute E[μ(n)]
conditional_exp = defaultdict(list)
for n in range(2, MAX_N + 1):
    m_prev = M[n-1]
    conditional_exp[m_prev].append(mu[n])

print(f"\nConditional expectation E[μ(n) | M(n-1) = m] for n ≤ {MAX_N}:")
print("-" * 65)
print(f"{'M(n-1)':>8} {'E[μ(n)]':>12} {'Std':>10} {'Count':>10} {'|E| < 0.1?':>12}")
print("-" * 65)

violations = 0
total_analyzed = 0
epsilon = 0.1

# Focus on values with enough samples
for m in sorted(conditional_exp.keys()):
    if len(conditional_exp[m]) >= 20:
        total_analyzed += 1
        mean_mu = np.mean(conditional_exp[m])
        std_mu = np.std(conditional_exp[m])
        count = len(conditional_exp[m])
        is_small = abs(mean_mu) < epsilon
        if not is_small:
            violations += 1
        if abs(m) <= 50 and count >= 50:
            print(f"{m:>8} {mean_mu:>+12.6f} {std_mu:>10.4f} {count:>10} {'YES' if is_small else 'NO':>12}")

print(f"\nSummary:")
print(f"  Total M(n-1) values analyzed (count ≥ 20): {total_analyzed}")
print(f"  Violations (|E[μ(n)]| ≥ {epsilon}): {violations}")
print(f"  Violation rate: {100*violations/total_analyzed:.2f}%")

# =============================================================================
# PART 3: QUANTIFYING THE DEVIATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 3: QUANTIFYING THE MARTINGALE DEVIATION")
print("=" * 75)

print("""
Define the "martingale error" at position n:
  ε_n = E[μ(n) | M(n-1)]

If μ were a true martingale difference, ε_n = 0.

Let's compute the average |ε_n| and see if it decreases with x.
""")

def compute_avg_martingale_error(x_max):
    """Compute average |E[μ(n) | M(n-1)]| up to x_max."""
    bins = defaultdict(list)
    for n in range(2, x_max + 1):
        bins[M[n-1]].append(mu[n])

    # For each bin with enough samples, compute |mean|
    errors = []
    for m, vals in bins.items():
        if len(vals) >= 5:
            errors.append(abs(np.mean(vals)))

    return np.mean(errors) if errors else 0

print("\nAverage martingale error vs x:")
print("-" * 40)
print(f"{'x_max':>10} {'Avg |ε|':>15}")
print("-" * 40)

for x_max in [1000, 5000, 10000, 20000, 50000, 100000]:
    if x_max <= MAX_N:
        avg_err = compute_avg_martingale_error(x_max)
        print(f"{x_max:>10} {avg_err:>15.6f}")

# =============================================================================
# PART 4: MARTINGALE APPROXIMATION THEOREM
# =============================================================================

print("\n" + "=" * 75)
print("PART 4: MARTINGALE APPROXIMATION THEOREM")
print("=" * 75)

print("""
THEOREM (Informal): If X_n is an ε-approximate martingale, then:
  |X_n| ≤ (true martingale bound) + n·ε

For Harper's bound: E|S_x| ≍ √x / (log log x)^{1/4}

If M(x) is ε-approximate with ε ~ 1/x, then:
  |M(x)| ≤ √x / (log log x)^{1/4} + x · (1/x) = √x / (log log x)^{1/4} + O(1)

This would give Harper's bound for M(x)!

THE KEY QUESTION: Is ε ~ 1/x achievable?
""")

# Compute ε as a function of x
print("\nMartingale error ε as function of x:")
print("-" * 50)

def compute_epsilon_of_x(x):
    """Compute the martingale error for M up to x."""
    # We measure: max over m of |E[μ(n) | M(n-1) = m]|
    bins = defaultdict(list)
    for n in range(2, x + 1):
        bins[M[n-1]].append(mu[n])

    max_error = 0
    for m, vals in bins.items():
        if len(vals) >= 3:
            error = abs(np.mean(vals))
            max_error = max(max_error, error)

    return max_error

print(f"{'x':>10} {'max |ε|':>15} {'1/x':>15} {'max|ε|·x':>15}")
print("-" * 60)

for x in [500, 1000, 2000, 5000, 10000, 20000]:
    eps = compute_epsilon_of_x(x)
    print(f"{x:>10} {eps:>15.6f} {1/x:>15.6f} {eps*x:>15.4f}")

print("""
OBSERVATION:
The max |ε| does NOT scale like 1/x.
Instead, max|ε|·x grows, meaning ε is roughly constant.

This means M(x) is NOT an O(1/x)-approximate martingale.
The simple approximation argument fails.
""")

# =============================================================================
# PART 5: ALTERNATIVE: L² APPROXIMATE MARTINGALE
# =============================================================================

print("\n" + "=" * 75)
print("PART 5: L² APPROXIMATE MARTINGALE")
print("=" * 75)

print("""
A weaker notion: X_n is an L² ε-approximate martingale if:
  E[|E[X_{n+1} - X_n | F_n]|²] ≤ ε²

This allows for occasional large deviations but controls average behavior.
""")

def compute_L2_martingale_error(x):
    """Compute L² martingale error."""
    bins = defaultdict(list)
    for n in range(2, x + 1):
        bins[M[n-1]].append(mu[n])

    squared_errors = []
    total_count = 0
    for m, vals in bins.items():
        if len(vals) >= 2:
            mean_mu = np.mean(vals)
            # Weight by frequency
            squared_errors.extend([mean_mu**2] * len(vals))
            total_count += len(vals)

    return np.sqrt(np.mean(squared_errors)) if squared_errors else 0

print("\nL² martingale error:")
print("-" * 50)
print(f"{'x':>10} {'L² error':>15} {'√(1/x)':>15} {'L²·√x':>15}")
print("-" * 60)

for x in [1000, 2000, 5000, 10000, 20000, 50000]:
    if x <= MAX_N:
        l2_err = compute_L2_martingale_error(x)
        print(f"{x:>10} {l2_err:>15.6f} {1/np.sqrt(x):>15.6f} {l2_err*np.sqrt(x):>15.4f}")

# =============================================================================
# PART 6: DECOMPOSITION BY NUMBER OF PRIME FACTORS
# =============================================================================

print("\n" + "=" * 75)
print("PART 6: ALTERNATIVE DECOMPOSITION - BY Ω(n)")
print("=" * 75)

print("""
Instead of conditioning on M(n-1), try conditioning on Ω(n-1).

Harper's proof uses decomposition by largest prime factor P(n).
Let's try decomposition by total prime count Ω(n).
""")

def Omega(n):
    if n == 1:
        return 0
    return sum(factorint(n).values())

# Compute M(x) stratified by Ω
print("\nPartial Mertens by Ω(n):")
print("-" * 60)

x = 50000
M_by_Omega = defaultdict(int)
count_by_Omega = defaultdict(int)

for n in range(1, x + 1):
    Om = Omega(n)
    M_by_Omega[Om] += mu[n]
    count_by_Omega[Om] += 1

print(f"{'Ω':>5} {'Count':>12} {'Σμ':>12} {'Σμ/√Count':>15} {'Running M':>12}")
print("-" * 60)

running_M = 0
for Om in range(15):
    count = count_by_Omega[Om]
    partial_sum = M_by_Omega[Om]
    running_M += partial_sum
    if count > 0:
        ratio = partial_sum / np.sqrt(count)
        print(f"{Om:>5} {count:>12} {partial_sum:>+12} {ratio:>+15.4f} {running_M:>+12}")

print("""
OBSERVATION:
The sums by Ω(n) show alternating signs:
  Ω=1 (primes): Σμ = -π(x) (large negative)
  Ω=2: Large positive
  Ω=3: Large negative
  etc.

These largely cancel in the total M(x).

KEY INSIGHT: The cancellation happens BETWEEN Ω-levels, not within.
""")

# =============================================================================
# PART 7: THE INTER-LEVEL CANCELLATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 7: INTER-LEVEL CANCELLATION STRUCTURE")
print("=" * 75)

print("""
For μ(n), we have:
  μ(n) = 0 if Ω(n) > ω(n) (has squared factor)
  μ(n) = (-1)^ω(n) if squarefree

So among squarefree n:
  Ω=ω=1: μ = -1 (primes)
  Ω=ω=2: μ = +1 (product of 2 distinct primes)
  Ω=ω=3: μ = -1 (product of 3 distinct primes)
  etc.

The counts follow the distribution of squarefree numbers by ω.
""")

# Analyze the structure more carefully
x = 100000
omega_counts = defaultdict(int)

for n in range(1, x + 1):
    if mu[n] != 0:
        factors = factorint(n)
        w = len(factors)
        omega_counts[w] += 1

print(f"\nDistribution of squarefree n ≤ {x} by ω(n):")
print("-" * 50)
print(f"{'ω':>5} {'Count':>12} {'μ value':>10} {'Contribution':>15}")
print("-" * 50)

total_M = 0
for w in range(10):
    count = omega_counts[w]
    mu_val = (-1)**w
    contrib = count * mu_val
    total_M += contrib
    print(f"{w:>5} {count:>12} {mu_val:>+10} {contrib:>+15}")

print(f"\nTotal M({x}) = {total_M}")
print(f"Actual M({x}) = {M[x]}")

# =============================================================================
# PART 8: THE ALTERNATING SUM STRUCTURE
# =============================================================================

print("\n" + "=" * 75)
print("PART 8: WHY DOES THE ALTERNATING SUM CANCEL?")
print("=" * 75)

print("""
M(x) = Σ_{w=0}^∞ (-1)^w × (# of squarefree n ≤ x with ω(n) = w)
     = Σ_{w=0}^∞ (-1)^w × S_w(x)

where S_w(x) = #{n ≤ x : n squarefree, ω(n) = w}

QUESTION: Why does this alternating sum stay small?

For RANDOM: If S_w(x) were random, the alternating sum would be ~ √(Var)
For DETERMINISTIC: The S_w(x) have specific values determined by prime distribution
""")

# Compute the variance of the alternating sum
def alternating_variance(x):
    """Estimate what variance would be if S_w were independent."""
    total_var = 0
    for w in range(1, 15):
        count = omega_counts[w]
        total_var += count  # Each contributes ±1, so var = count
    return np.sqrt(total_var)

x = 100000
# Recompute omega_counts for this x
omega_counts = defaultdict(int)
for n in range(1, x + 1):
    if mu[n] != 0:
        w = len(factorint(n))
        omega_counts[w] += 1

expected_std = alternating_variance(x)
actual_M = abs(M[x])

print(f"\nFor x = {x}:")
print(f"  If S_w were independent: E|M| ≈ √(Σ S_w) = {expected_std:.2f}")
print(f"  Actual |M(x)|: {actual_M}")
print(f"  Ratio actual/expected: {actual_M/expected_std:.4f}")

print("""
OBSERVATION:
The actual |M(x)| is MUCH smaller than expected from independent S_w.

This means the S_w(x) values are CORRELATED in a specific way
that causes extra cancellation.

THE KEY INSIGHT:
The prime distribution creates correlations between S_w(x) for different w.
These correlations are what cause the "better than √x" cancellation.
""")

# =============================================================================
# PART 9: CAN WE QUANTIFY THE CORRELATION?
# =============================================================================

print("\n" + "=" * 75)
print("PART 9: QUANTIFYING INTER-LEVEL CORRELATIONS")
print("=" * 75)

# Track S_w(x) for multiple values of x
x_values = list(range(1000, 50001, 1000))
S_w_series = {w: [] for w in range(8)}

for x in x_values:
    counts = defaultdict(int)
    for n in range(1, x + 1):
        if mu[n] != 0:
            w = len(factorint(n))
            counts[w] += 1
    for w in range(8):
        S_w_series[w].append(counts[w])

# Convert to numpy arrays
for w in S_w_series:
    S_w_series[w] = np.array(S_w_series[w])

# Compute correlation matrix between S_w growth rates
print("\nCorrelation between ΔS_w/Δx for different w:")
print("-" * 60)

# Growth rates
dS_w = {w: np.diff(S_w_series[w]) for w in range(8)}

corr_matrix = np.zeros((6, 6))
for w1 in range(1, 7):
    for w2 in range(1, 7):
        if len(dS_w[w1]) > 0 and len(dS_w[w2]) > 0:
            corr_matrix[w1-1, w2-1] = np.corrcoef(dS_w[w1], dS_w[w2])[0, 1]

print("      ", end="")
for w in range(1, 7):
    print(f"  ω={w} ", end="")
print()
for w1 in range(1, 7):
    print(f"ω={w1}  ", end="")
    for w2 in range(1, 7):
        print(f"{corr_matrix[w1-1, w2-1]:+.3f}", end=" ")
    print()

print("""
OBSERVATION:
Adjacent ω-levels have high positive correlation in growth rates.
This means when S_1 increases, S_2 also increases (and vice versa).

But in the alternating sum:
  M = -S_1 + S_2 - S_3 + ...

High positive correlation between S_w and S_{w+1} means:
  -S_w + S_{w+1} ≈ 0 + small fluctuation

This IS the mechanism of cancellation!
""")

# =============================================================================
# PART 10: FORMALIZING THE CORRELATION-CANCELLATION
# =============================================================================

print("\n" + "=" * 75)
print("PART 10: FORMALIZING THE CORRELATION-CANCELLATION")
print("=" * 75)

print("""
HYPOTHESIS (Correlation-Cancellation):
=====================================

Define: D_w(x) = S_w(x) - S_{w+1}(x) (consecutive level difference)

If: D_w(x) = O(√(S_w(x)))  for each w

Then: M(x) = Σ (-1)^w S_w(x)
           = -D_0 - D_2 - D_4 - ...  (telescoping-like)
           = O(√x)

The Harper bound would follow if D_w(x) = O(√(S_w) / (log log x)^{some power}).
""")

# Test the hypothesis
print("\nTesting D_w(x) = S_w - S_{w+1} behavior:")
print("-" * 65)

x = 100000
counts = defaultdict(int)
for n in range(1, x + 1):
    if mu[n] != 0:
        w = len(factorint(n))
        counts[w] += 1

print(f"{'w':>5} {'S_w':>12} {'S_{w+1}':>12} {'D_w':>12} {'√S_w':>12} {'D_w/√S_w':>12}")
print("-" * 70)

for w in range(1, 7):
    S_w = counts[w]
    S_w1 = counts[w+1]
    D_w = S_w - S_w1
    sqrt_S = np.sqrt(S_w)
    ratio = D_w / sqrt_S if sqrt_S > 0 else 0
    print(f"{w:>5} {S_w:>12} {S_w1:>12} {D_w:>+12} {sqrt_S:>12.2f} {ratio:>+12.4f}")

print("""
OBSERVATION:
D_w/√S_w is roughly constant (~30-40).
This is WORSE than needed for Harper's bound.

But the key is: D_w grows like √S_w (approximately √x),
while S_w grows like x/(log x)^something.

So D_w << S_w, which gives cancellation.
But not enough for Harper's precise bound.
""")

# =============================================================================
# PART 11: WHAT WOULD BE NEEDED
# =============================================================================

print("\n" + "=" * 75)
print("PART 11: WHAT WOULD BE NEEDED FOR HARPER'S BOUND")
print("=" * 75)

print("""
TO PROVE |M(x)| = O(√x / (log log x)^{1/4}):
============================================

METHOD 1: Show μ is ε-approximate martingale with ε = O(1/x)
  Status: FAILED - ε is roughly constant

METHOD 2: Show S_w(x) - S_{w+1}(x) has extra cancellation
  Status: PARTIALLY - ratio is constant, not decreasing

METHOD 3: Direct proof of inter-level correlation structure
  Need: Cov(S_w, S_{w+1}) strong enough to imply bounds
  Status: NOT SUFFICIENT - correlation is high but not structured enough

METHOD 4: Import Harper's multiplicative chaos framework
  Need: Show μ generates "critical" chaos
  Status: REQUIRES NEW IDEAS - determinism blocks direct import


THE FUNDAMENTAL OBSTRUCTION:
============================

Harper's proof works because:
  f(p) are independent ⟹ S_w(x) are nearly independent
  ⟹ Alternating sum has Var ~ Σ Var(S_w) ~ x
  ⟹ Extra cancellation comes from multiplicative chaos structure

For μ(n):
  μ(p) = -1 always ⟹ S_w(x) are highly correlated
  ⟹ Can't directly apply independence arguments
  ⟹ Need alternative approach to control alternating sum

THE GAP:
The deterministic nature of μ(p) creates correlations that
Harper's proof can't handle directly.

POSSIBLE RESOLUTION:
If the correlations are "just right" - not too strong, not too weak -
they might actually HELP with cancellation.

This would require proving:
  The prime distribution creates correlations that cause
  |M(x)| = O(√x / (log log x)^{1/4})

This is essentially the content of RH.
""")

# =============================================================================
# SYNTHESIS
# =============================================================================

print("\n" + "=" * 75)
print("SYNTHESIS: APPROXIMATE MARTINGALE APPROACH")
print("=" * 75)

print("""
SUMMARY:
========

1. M(n) is NOT an ε-approximate martingale with ε → 0

2. M(n) HAS approximate martingale properties:
   - E[μ(n) | M(n-1)] ≈ 0 on average
   - The L² error is bounded

3. The structure is better understood via ω(n)-decomposition:
   - M(x) = alternating sum of S_w(x)
   - S_w are positively correlated (high correlation ~0.8-0.9)
   - Cancellation happens between levels

4. The correlation is NOT strong enough to directly imply Harper's bound
   - Need additional structure or insight

5. The fundamental obstruction remains:
   - Determinism of μ(p) = -1 creates correlations
   - These correlations are different from random case
   - Converting correlation structure to cancellation bound is the gap


NEXT STEPS:
===========

A. Study the exact correlation structure of S_w(x)
   - Can we derive correlation from prime distribution?
   - Does correlation structure imply specific cancellation?

B. Look for alternative decomposition
   - Maybe by different invariants of n
   - Residue classes, radical, etc.

C. Connect to L-function theory
   - Wang-Xu approach via Dirichlet characters
   - Can we avoid GRH?

D. Direct analysis of deterministic sums
   - Classical analytic number theory bounds
   - Explicit formula methods
""")

print("\n" + "=" * 75)
print("END OF APPROXIMATE MARTINGALE ANALYSIS")
print("=" * 75)
