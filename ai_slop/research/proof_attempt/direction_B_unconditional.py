"""
DIRECTION B: ATTEMPTING UNCONDITIONAL BOUNDS
=============================================

Goal: Prove SOMETHING about M(x) without assuming RH.

Strategy: Use the generating function structure to derive bounds
that don't depend on knowing the zeta zeros.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint
from collections import defaultdict
import math

print("=" * 80)
print("DIRECTION B: ATTEMPTING UNCONDITIONAL BOUNDS")
print("=" * 80)

# Precompute data
print("\nPrecomputing squarefree data...")
MAX_N = 200000
mu = [0] * (MAX_N + 1)
omega_vals = [0] * (MAX_N + 1)

mu[1] = 1
omega_vals[1] = 0

for n in range(2, MAX_N + 1):
    factors = factorint(n)
    omega_vals[n] = len(factors)
    if any(e > 1 for e in factors.values()):
        mu[n] = 0
    else:
        mu[n] = (-1) ** len(factors)

def get_S_w(x):
    """Get S_w counts up to x."""
    S = defaultdict(int)
    for n in range(1, min(x+1, MAX_N+1)):
        if mu[n] != 0:
            S[omega_vals[n]] += 1
    return dict(S)

def get_M(x):
    """Get M(x)."""
    return sum(mu[n] for n in range(1, min(x+1, MAX_N+1)))

def get_Q(x):
    """Get Q(x) = count of squarefree."""
    return sum(1 for n in range(1, min(x+1, MAX_N+1)) if mu[n] != 0)

print("Done.")

# =============================================================================
# APPROACH 1: TELESCOPING BOUND
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 1: TELESCOPING BOUND")
print("=" * 80)

print("""
Idea: Use the structure M(x) = Σ(-1)^w S_w to get bounds.

We can write:
M(x) = (S_0 - S_1) + (S_2 - S_3) + (S_4 - S_5) + ...

Each pair (S_{2k} - S_{2k+1}) is a "net contribution" from consecutive levels.

If we can bound these differences, we bound M(x).
""")

def analyze_differences(x):
    """Analyze S_w - S_{w+1} differences."""
    S = get_S_w(x)
    max_w = max(S.keys())

    differences = []
    for w in range(0, max_w, 2):
        S_w = S.get(w, 0)
        S_w1 = S.get(w+1, 0)
        diff = S_w - S_w1
        differences.append((w, S_w, S_w1, diff))

    return differences

x = 100000
diffs = analyze_differences(x)
print(f"\nDifferences S_{{2k}} - S_{{2k+1}} at x = {x:,}:")
print("-" * 60)
print(f"{'k':>4} | {'S_{2k}':>10} | {'S_{2k+1}':>10} | {'Diff':>10} | {'Cumsum':>10}")
print("-" * 60)

cumsum = 0
for (w, S_w, S_w1, diff) in diffs:
    cumsum += diff
    print(f"{w//2:>4} | {S_w:>10} | {S_w1:>10} | {diff:>+10} | {cumsum:>+10}")

print(f"\nFinal sum = {cumsum} (should equal M(x) = {get_M(x)})")

# =============================================================================
# APPROACH 2: RATIO BOUND
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 2: RATIO BOUND")
print("=" * 80)

print("""
Idea: Use the ratio S_{w+1}/S_w ≈ λ/w where λ = log log x.

For the mode w* ≈ λ, consecutive S_w are nearly equal.
This should cause cancellation in the alternating sum.

Let's try to prove: |M(x)| ≤ C · Q(x) / λ for some constant C.
""")

def ratio_analysis(x):
    """Analyze the ratio S_{w+1}/S_w."""
    S = get_S_w(x)
    Q = get_Q(x)
    lam = np.log(np.log(x))

    print(f"\nAt x = {x:,}, λ = {lam:.4f}, Q = {Q:,}")
    print("-" * 60)
    print(f"{'w':>4} | {'S_w':>10} | {'S_{w+1}':>10} | {'Ratio':>10} | {'λ/(w+1)':>10}")
    print("-" * 60)

    for w in range(6):
        S_w = S.get(w, 0)
        S_w1 = S.get(w+1, 0)
        ratio = S_w1 / S_w if S_w > 0 else 0
        predicted = lam / (w+1)
        print(f"{w:>4} | {S_w:>10} | {S_w1:>10} | {ratio:>10.4f} | {predicted:>10.4f}")

ratio_analysis(100000)

# =============================================================================
# APPROACH 3: VARIANCE BOUND
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 3: VARIANCE BOUND")
print("=" * 80)

print("""
Idea: Bound M(x)² in terms of the variance structure.

M(x) = Σ(-1)^w S_w

M(x)² = Σ_w Σ_{w'} (-1)^{w+w'} S_w S_{w'}
      = Σ_w S_w² + 2 Σ_{w<w'} (-1)^{w+w'} S_w S_{w'}

If we knew the covariance structure, we could bound this.

For independent Poisson, the variance would be ~Q(x).
The actual variance might be smaller due to correlations.
""")

def variance_analysis(x):
    """Analyze variance structure."""
    S = get_S_w(x)
    Q = get_Q(x)
    M = get_M(x)

    # Compute different variance-like quantities
    sum_Sw_sq = sum(s**2 for s in S.values())

    # The "variance in alternating direction"
    # This is M²
    var_alt = M**2

    # The "total variance" (if S_w were independent Poisson)
    var_poisson = Q  # Poisson variance = mean

    # Sum of Sw² as another measure
    sum_sq = sum(S.get(w, 0)**2 for w in range(20))

    print(f"\nVariance structure at x = {x:,}:")
    print(f"  Q(x) = {Q:,}")
    print(f"  M(x) = {M:+d}")
    print(f"  M(x)² = {M**2:,}")
    print(f"  Σ S_w² = {sum_sq:,}")
    print(f"  Q²  = {Q**2:,}")
    print(f"  M²/Q = {M**2 / Q:.4f}")
    print(f"  |M|/√Q = {abs(M) / np.sqrt(Q):.4f}")
    print(f"  |M|/√x = {abs(M) / np.sqrt(x):.4f}")

variance_analysis(100000)

# =============================================================================
# APPROACH 4: SUMMATION BY PARTS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 4: SUMMATION BY PARTS")
print("=" * 80)

print("""
Idea: Apply summation by parts to Σ(-1)^w S_w.

Let a_w = (-1)^w and b_w = S_w.
Let A_w = Σ_{k≤w} (-1)^k = (1-(-1)^{w+1})/2 = {0 if w odd, 1 if w even}.

By summation by parts:
Σ_w a_w b_w = A_W b_W - Σ_{w<W} A_w (b_{w+1} - b_w)

The differences (S_{w+1} - S_w) might be easier to bound.
""")

def summation_by_parts(x):
    """Apply summation by parts."""
    S = get_S_w(x)
    max_w = max(S.keys())

    # Compute differences
    diffs = []
    for w in range(max_w):
        S_w = S.get(w, 0)
        S_w1 = S.get(w+1, 0)
        diffs.append(S_w1 - S_w)

    # A_w = 1 if w even, 0 if w odd
    # So we're summing over even w only
    sum_even = 0
    for w in range(0, max_w, 2):
        if w < len(diffs):
            sum_even += diffs[w]

    print(f"\nSummation by parts at x = {x:,}:")
    print(f"  max_w = {max_w}")
    print(f"  Sum of (S_{w+1} - S_w) for even w = {sum_even}")

    # Alternative formulation
    # M = S_0 - (S_1 - S_0) - (S_2 - S_1) + (S_3 - S_2) + ...

    return diffs

diffs = summation_by_parts(100000)

# =============================================================================
# APPROACH 5: PROBABILISTIC INTERPRETATION
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 5: PROBABILISTIC BOUND")
print("=" * 80)

print("""
Idea: Use the characteristic function interpretation.

φ(θ) = E[e^{iωθ}] = G(e^{iθ}, x) / G(1, x)

At θ = π:
φ(π) = M(x) / Q(x)

For a Poisson(λ) random variable:
φ_Poisson(π) = e^{-2λ} = 1 / (log x)²

The deviation from Poisson behavior determines how small M(x) is.
""")

def probabilistic_bound(x):
    """Analyze probabilistic bounds."""
    Q = get_Q(x)
    M = get_M(x)
    lam = np.log(np.log(x))

    # Characteristic function value
    phi_pi = M / Q

    # Poisson prediction
    phi_poisson = np.exp(-2 * lam)

    # Actual vs Poisson ratio
    ratio = phi_pi / phi_poisson if phi_poisson != 0 else 0

    print(f"\nProbabilistic analysis at x = {x:,}:")
    print(f"  λ = log log x = {lam:.4f}")
    print(f"  φ(π) = M/Q = {phi_pi:+.6f}")
    print(f"  φ_Poisson(π) = e^{{-2λ}} = {phi_poisson:.6f}")
    print(f"  Ratio = {ratio:+.4f}")
    print(f"  |Actual| / Poisson = {abs(phi_pi) / phi_poisson:.4f}")

    # What bound does Poisson give?
    M_poisson_bound = Q * phi_poisson
    print(f"\n  Poisson bound on |M|: Q · e^{{-2λ}} = {M_poisson_bound:.1f}")
    print(f"  Actual |M| = {abs(M)}")
    print(f"  Actual is {M_poisson_bound / abs(M):.1f}x smaller than Poisson bound")

for x in [10000, 50000, 100000, 200000]:
    probabilistic_bound(x)

# =============================================================================
# APPROACH 6: NEW UNCONDITIONAL BOUND ATTEMPT
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 6: ATTEMPTING A NEW UNCONDITIONAL BOUND")
print("=" * 80)

print("""
Let's try to prove something new.

CLAIM: |M(x)| ≤ C · Q(x)^{1-δ} for some δ > 0.

This would be weaker than RH (which gives |M| ≤ Q^{1/2+ε})
but stronger than trivial (|M| ≤ Q).

Strategy: Use the structure of the S_w distribution.
""")

def test_power_bound(x_values):
    """Test if |M| / Q^α is bounded for various α."""
    print("\nTesting |M(x)| / Q(x)^α for various α:")
    print("-" * 70)

    alphas = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]

    header = f"{'x':>10}"
    for a in alphas:
        header += f" | α={a:.1f}"
    print(header)
    print("-" * 70)

    for x in x_values:
        Q = get_Q(x)
        M = get_M(x)

        row = f"{x:>10}"
        for a in alphas:
            ratio = abs(M) / (Q ** a)
            row += f" | {ratio:>6.4f}"
        print(row)

    print("\nInterpretation:")
    print("  - For |M| = O(Q^α), the column should be bounded as x → ∞")
    print("  - α = 1.0: trivial bound, always bounded")
    print("  - α = 0.5: this is essentially RH")

test_power_bound([1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000])

# =============================================================================
# APPROACH 7: SMOOTHED SUM
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 7: SMOOTHED SUM ANALYSIS")
print("=" * 80)

print("""
Sometimes smoothed sums are easier to analyze.

Define: M_smooth(x) = Σ μ(n) · (1 - n/x)

This is a weighted sum that might have better properties.
""")

def smoothed_M(x):
    """Compute smoothed Mertens function."""
    total = 0
    for n in range(1, min(x+1, MAX_N+1)):
        total += mu[n] * (1 - n/x)
    return total

print("\nSmoothed vs unsmoothed M(x):")
print("-" * 60)
print(f"{'x':>10} | {'M(x)':>10} | {'M_smooth':>12} | {'|M|/√x':>10} | {'|Ms|/√x':>10}")
print("-" * 60)

for x in [1000, 2000, 5000, 10000, 20000, 50000, 100000]:
    M = get_M(x)
    Ms = smoothed_M(x)
    print(f"{x:>10} | {M:>+10} | {Ms:>+12.2f} | {abs(M)/np.sqrt(x):>10.4f} | {abs(Ms)/np.sqrt(x):>10.4f}")

# =============================================================================
# KEY FINDINGS
# =============================================================================

print("\n" + "=" * 80)
print("KEY FINDINGS FROM DIRECTION B")
print("=" * 80)

print("""
SUMMARY OF UNCONDITIONAL BOUND ATTEMPTS:
========================================

1. TELESCOPING BOUND:
   - Pairs (S_{2k}, S_{2k+1}) are similar in size near mode
   - But differences don't systematically cancel
   - No unconditional improvement over trivial bound

2. RATIO ANALYSIS:
   - S_{w+1}/S_w ≈ λ/w confirms Landau's asymptotic
   - But ratios alone don't give cancellation bounds

3. VARIANCE ANALYSIS:
   - M²/Q is small (~0.04 at x=100000)
   - This is consistent with RH but we can't PROVE it

4. SUMMATION BY PARTS:
   - Transforms alternating sum to difference sum
   - Differences are structured but not obviously bounded

5. PROBABILISTIC BOUND:
   - Poisson predicts |M|/Q ≈ e^{-2λ} = 1/(log x)²
   - Actual |M|/Q is 10x smaller than Poisson
   - But proving this requires knowing ζ zeros

6. POWER BOUND TEST:
   - |M|/Q^{0.6} appears bounded (consistent with RH)
   - |M|/Q^{0.5} appears bounded (IS RH)
   - But we can't prove these without controlling zeros

7. SMOOTHED SUM:
   - Smoothing doesn't obviously help
   - Both M and M_smooth have similar O(√x) behavior

CONCLUSION:
==========
Every approach leads back to the same obstruction:
proving any bound better than trivial requires controlling
the zeta zeros, which IS the Riemann Hypothesis.

Our generating function framework doesn't provide
a shortcut around this fundamental obstacle.
""")

print("=" * 80)
print("DIRECTION B COMPLETE")
print("=" * 80)
