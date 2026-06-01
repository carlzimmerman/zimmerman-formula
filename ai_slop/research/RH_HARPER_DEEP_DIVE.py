#!/usr/bin/env python3
"""
DEEP DIVE: HARPER'S MULTIPLICATIVE CHAOS FRAMEWORK
===================================================

Testing Harper's "better than squareroot cancellation" ideas
applied to the Möbius function.

Key Results from Literature:
1. Harper (2017): E|Σf(n)| ~ √x/(log log x)^{1/4} for random multiplicative f
2. This is BETTER than √x cancellation
3. Wintner (1944): Rademacher random multiplicative functions model μ(n)
4. Gonek-Ng Conjecture: M(x) = O(√x (log log log x)^{5/4})

The Question: Can we numerically verify Harper-style behavior for μ(n)?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange
import matplotlib.pyplot as plt
from scipy import stats

print("=" * 70)
print("HARPER'S MULTIPLICATIVE CHAOS: DEEP DIVE")
print("=" * 70)

# =============================================================================
# SECTION 1: COMPUTE MÖBIUS FUNCTION AND M(x)
# =============================================================================

def mobius(n):
    """Compute μ(n)"""
    if n == 1:
        return 1
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return (-1) ** len(factors)

def compute_M(x_max):
    """Compute M(x) = Σ_{n≤x} μ(n) for all x up to x_max"""
    mu_values = [mobius(n) for n in range(1, x_max + 1)]
    M_values = np.cumsum(mu_values)
    return mu_values, M_values

print("\n" + "=" * 70)
print("SECTION 1: Computing M(x) = Σμ(n) for x up to 50000")
print("=" * 70)

X_MAX = 50000
print(f"\nComputing μ(n) for n = 1 to {X_MAX}...")
mu_vals, M_vals = compute_M(X_MAX)
print("Done.")

# =============================================================================
# SECTION 2: TEST SQUAREROOT CANCELLATION
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 2: Testing √x Cancellation")
print("=" * 70)

print("""
RH Prediction: M(x) = O(x^{1/2+ε})
Harper's Prediction (heuristic): M(x) ~ √x / (log log x)^{1/4} typical behavior

Let's check the ratio M(x)/√x at various x values.
""")

test_points = [100, 500, 1000, 5000, 10000, 25000, 50000]

print("| x      | M(x)   | √x     | M(x)/√x  | (log log x)^{1/4} | M(x)·(log log x)^{1/4}/√x |")
print("|--------|--------|--------|----------|-------------------|---------------------------|")

for x in test_points:
    M_x = M_vals[x-1]
    sqrt_x = np.sqrt(x)
    ratio = M_x / sqrt_x
    log_log_x = np.log(np.log(x))
    correction = log_log_x ** 0.25
    corrected_ratio = abs(M_x) * correction / sqrt_x
    print(f"| {x:6d} | {M_x:6d} | {sqrt_x:6.1f} | {ratio:+8.4f} | {correction:17.4f} | {corrected_ratio:25.4f} |")

# =============================================================================
# SECTION 3: STATISTICAL ANALYSIS OF M(x)/√x
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 3: Statistical Analysis of M(x)/√x")
print("=" * 70)

# Compute normalized M(x)/√x
x_range = np.arange(100, X_MAX + 1)
M_normalized = np.array([M_vals[x-1] / np.sqrt(x) for x in x_range])

print(f"\nStatistics for M(x)/√x over x ∈ [100, {X_MAX}]:")
print(f"  Mean:     {np.mean(M_normalized):+.6f}")
print(f"  Std Dev:  {np.std(M_normalized):.6f}")
print(f"  Max:      {np.max(M_normalized):+.6f}")
print(f"  Min:      {np.min(M_normalized):+.6f}")
print(f"  Max |·|:  {np.max(np.abs(M_normalized)):.6f}")

# =============================================================================
# SECTION 4: HARPER'S (log log x)^{-1/4} CORRECTION
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 4: Testing Harper's (log log x)^{-1/4} Correction")
print("=" * 70)

print("""
Harper proved for RANDOM multiplicative functions:
  E|Σf(n)| ~ √x / (log log x)^{1/4}

If μ(n) behaves similarly, then:
  M(x) · (log log x)^{1/4} / √x should be O(1)

Let's test this.
""")

# Harper-corrected normalization
log_log_x = np.log(np.log(x_range.astype(float)))
correction_factor = log_log_x ** 0.25
M_harper_corrected = np.abs(M_normalized) * correction_factor

print(f"Statistics for |M(x)| · (log log x)^{{1/4}} / √x:")
print(f"  Mean:   {np.mean(M_harper_corrected):.6f}")
print(f"  Std:    {np.std(M_harper_corrected):.6f}")
print(f"  Max:    {np.max(M_harper_corrected):.6f}")
print(f"  Min:    {np.min(M_harper_corrected):.6f}")

# Check if it's stabilizing
n_bins = 5
bin_size = len(x_range) // n_bins
print(f"\nBehavior across ranges (checking for stability):")
print("| Range         | Mean Harper-corrected |")
print("|---------------|----------------------|")
for i in range(n_bins):
    start_idx = i * bin_size
    end_idx = (i + 1) * bin_size if i < n_bins - 1 else len(x_range)
    mean_val = np.mean(M_harper_corrected[start_idx:end_idx])
    start_x = x_range[start_idx]
    end_x = x_range[end_idx - 1]
    print(f"| {start_x:5d}-{end_x:5d} | {mean_val:20.6f} |")

# =============================================================================
# SECTION 5: GONEK-NG CONJECTURE TEST
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 5: Testing Gonek-Ng Conjecture")
print("=" * 70)

print("""
Gonek-Ng Conjecture: max_{x≤X} |M(x)| ~ √X · (log log log X)^{5/4}

This predicts the MAXIMUM fluctuation, not typical behavior.
Let's check the running maximum.
""")

# Compute running maximum of |M(x)|/√x
running_max = np.maximum.accumulate(np.abs(M_vals))

print("| X      | max|M(x)| | √X     | max/√X | (logloglogX)^{5/4} | Gonek-Ng ratio |")
print("|--------|-----------|--------|--------|--------------------|-----------------")

check_points = [1000, 5000, 10000, 25000, 50000]
for X in check_points:
    max_M = running_max[X-1]
    sqrt_X = np.sqrt(X)
    ratio = max_M / sqrt_X
    if X > np.e**np.e:  # Need log log log to be defined
        lll_X = np.log(np.log(np.log(X)))
        gonek_factor = lll_X ** 1.25 if lll_X > 0 else 0
        gonek_ratio = max_M / (sqrt_X * gonek_factor) if gonek_factor > 0 else float('nan')
    else:
        gonek_factor = float('nan')
        gonek_ratio = float('nan')
    print(f"| {X:6d} | {max_M:9d} | {sqrt_X:6.1f} | {ratio:6.3f} | {gonek_factor:18.4f} | {gonek_ratio:15.4f} |")

# =============================================================================
# SECTION 6: MULTIPLICATIVE STRUCTURE ANALYSIS
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 6: Multiplicative Structure Analysis")
print("=" * 70)

print("""
Harper's key insight: Random multiplicative functions have BETTER
cancellation than purely random sequences because of the multiplicative
constraint.

For μ(n), we can analyze:
1. The distribution of μ(n) values
2. Correlations between μ(n) and μ(m) when gcd(n,m) > 1
3. How the multiplicative structure creates cancellation
""")

# Count distribution of μ values
mu_counts = {-1: 0, 0: 0, 1: 0}
for m in mu_vals:
    mu_counts[m] += 1

total = len(mu_vals)
print(f"\nDistribution of μ(n) for n ≤ {X_MAX}:")
print(f"  μ(n) = -1: {mu_counts[-1]:6d} ({100*mu_counts[-1]/total:5.2f}%)")
print(f"  μ(n) =  0: {mu_counts[0]:6d} ({100*mu_counts[0]/total:5.2f}%)")
print(f"  μ(n) = +1: {mu_counts[1]:6d} ({100*mu_counts[1]/total:5.2f}%)")

# The proportion of squarefree numbers approaches 6/π² ≈ 0.6079
squarefree_prop = (mu_counts[-1] + mu_counts[1]) / total
print(f"\n  Squarefree proportion: {squarefree_prop:.6f}")
print(f"  Expected (6/π²):      {6/np.pi**2:.6f}")

# =============================================================================
# SECTION 7: THE KEY QUESTION FOR RH
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 7: The Key Question for RH")
print("=" * 70)

print("""
QUESTION: Can Harper's techniques prove M(x) = O(x^{1/2+ε})?

What's Known:
-------------
1. Harper PROVED: E|Σf(n)| ~ √x/(log log x)^{1/4} for RANDOM f

2. Wang-Xu (2025) PROVED: Under GRH + Ratios Conjecture,
   the Liouville function has better-than-squareroot cancellation

3. For MOBIUS function μ(n): Currently UNPROVEN

The Gap:
--------
Random multiplicative functions: Rigorously analyzed
Deterministic μ(n): The independence assumption fails

What Would Be Needed:
--------------------
To apply Harper's method to μ(n), one would need to show that
μ(n) has "sufficient randomness" in a rigorous sense.

This is the crux: μ(n) is deterministic, not random.
""")

# Numerical comparison: How does our M(x) compare to Harper's prediction?
print("\nNumerical Comparison to Harper's Prediction:")
print("---------------------------------------------")

# For random multiplicative f, E|Σf(n)| ~ C·√x/(log log x)^{1/4}
# If μ behaves similarly, |M(x)| should typically be ~ √x/(log log x)^{1/4}

# Estimate the "typical" |M(x)| in bins
print("\n| x range     | RMS |M|  | √x/(loglogx)^{1/4} | Ratio  |")
print("|-------------|---------|---------------------|--------|")

for i, x in enumerate([1000, 5000, 10000, 25000, 50000]):
    # RMS of |M| in window around x
    window = 200
    start = max(0, x - window)
    end = min(X_MAX, x + window)
    rms_M = np.sqrt(np.mean(np.array(M_vals[start:end])**2))
    harper_pred = np.sqrt(x) / (np.log(np.log(x)) ** 0.25)
    ratio = rms_M / harper_pred
    print(f"| {start:5d}-{end:5d} | {rms_M:7.2f} | {harper_pred:19.2f} | {ratio:6.3f} |")

# =============================================================================
# SECTION 8: CRITICAL MULTIPLICATIVE CHAOS CONNECTION
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 8: Critical Multiplicative Chaos Connection")
print("=" * 70)

print("""
Harper's Deep Connection:
-------------------------
The partial sums of random multiplicative functions connect to
CRITICAL MULTIPLICATIVE CHAOS - a field from probability theory.

Key Insight: The log log factor arises from the CRITICAL case
of multiplicative chaos, where correlations are logarithmic.

For Random Euler Products:
  Σ f(n)n^{-s} for Re(s) → 1/2

The behavior is governed by critical multiplicative chaos.

Why This Matters for RH:
-----------------------
Harper (2025) proved: |ζ(1/2+it)|² gives rise to critical
multiplicative chaos as t varies.

This connects:
  ζ on critical line ←→ Critical chaos ←→ Better cancellation

The Zeta-Chaos Triangle:
-----------------------
         ζ(1/2+it)
            ↕
    Critical Multiplicative Chaos
         ↙       ↘
Random Multiplicative    Better than √x
    Functions           Cancellation
         ↘       ↙
      Möbius μ(n) ???

The ??? is where the proof would need to go.
""")

# =============================================================================
# SECTION 9: WHAT WOULD A HARPER-STYLE PROOF REQUIRE?
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 9: What Would a Harper-Style RH Proof Require?")
print("=" * 70)

print("""
REQUIREMENTS FOR HARPER-STYLE APPROACH TO RH:

1. INDEPENDENCE STRUCTURE
   Need: Show μ(p) for different primes has "sufficient independence"
   Challenge: μ is deterministic, not random

2. MULTIPLICATIVE CHAOS CONNECTION
   Need: Connect Σμ(n)n^{-s} to critical multiplicative chaos
   Challenge: The Dirichlet series 1/ζ(s) is much more rigid than random

3. MOMENT BOUNDS
   Need: Control E|Σμ(n)|^{2q} for 0 < q ≤ 1
   Challenge: No probability measure for deterministic functions

4. DECORRELATION ESTIMATES
   Need: Show μ(n) and μ(m) are "almost independent" in suitable sense
   Challenge: They are exactly μ(n)μ(m) = μ(nm) when coprime

CURRENT STATUS:
- Wang-Xu (2025): Achieved for Liouville λ(n) UNDER GRH + Ratios Conj.
- For μ(n): Would need similar conditional result first
- Unconditionally: No Harper-style M(x) = O(x^{1/2+ε}) proof exists

THE FUNDAMENTAL ISSUE:
Harper's techniques require a probability space.
μ(n) lives in the deterministic world of number theory.
Bridging this gap requires new ideas.
""")

# =============================================================================
# SECTION 10: SUMMARY AND IMPLICATIONS
# =============================================================================

print("\n" + "=" * 70)
print("SECTION 10: Summary and Implications")
print("=" * 70)

print(f"""
NUMERICAL FINDINGS (for x up to {X_MAX}):
-----------------------------------------
1. |M(x)|/√x stays bounded (max = {np.max(np.abs(M_normalized)):.4f})
2. Harper-corrected ratio |M(x)|·(loglogx)^{{1/4}}/√x averages {np.mean(M_harper_corrected):.4f}
3. Data is CONSISTENT with Harper-type behavior but doesn't prove it

THEORETICAL STATUS:
------------------
1. Harper's Framework: Proven for random multiplicative functions
2. Extension to Liouville: Wang-Xu 2025 (conditional on GRH + Ratios)
3. Extension to Möbius: NOT YET PROVEN

WHAT'S NEEDED:
--------------
A. Prove GRH + Ratios ⟹ M(x) has better-than-√x cancellation
B. Then prove GRH + Ratios unconditionally
C. Or find entirely new approach that doesn't need GRH

THE HONEST ASSESSMENT:
---------------------
Harper's framework is the MOST PROMISING modern approach to RH.
But applying it to μ(n) rigorously remains an open problem.
The gap between random and deterministic is the key obstacle.

REFERENCES:
-----------
- Harper (2017): arXiv:1703.06654 - Random multiplicative functions
- Harper (2025): arXiv:2512.23681 - Better than squareroot survey
- Wang-Xu (2025): arXiv:2405.04094 - Harper's conjecture for Liouville
- Wintner (1944): Duke Math J. - Random factorizations and RH
- Gonek-Ng: Conjecture on M(x) fluctuations
""")

print("\n" + "=" * 70)
print("END OF HARPER DEEP DIVE")
print("=" * 70)

# =============================================================================
# OPTIONAL: CREATE VISUALIZATION
# =============================================================================

try:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: M(x) vs √x bounds
    ax1 = axes[0, 0]
    x_plot = np.arange(1, X_MAX + 1)
    ax1.plot(x_plot, M_vals, 'b-', linewidth=0.5, alpha=0.7, label='M(x)')
    ax1.plot(x_plot, np.sqrt(x_plot), 'r--', label='√x')
    ax1.plot(x_plot, -np.sqrt(x_plot), 'r--')
    ax1.set_xlabel('x')
    ax1.set_ylabel('M(x)')
    ax1.set_title('M(x) = Σμ(n) with ±√x bounds')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: M(x)/√x normalized
    ax2 = axes[0, 1]
    ax2.plot(x_range, M_normalized, 'b-', linewidth=0.5, alpha=0.7)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.set_xlabel('x')
    ax2.set_ylabel('M(x)/√x')
    ax2.set_title('Normalized Mertens Function')
    ax2.grid(True, alpha=0.3)

    # Plot 3: Harper-corrected
    ax3 = axes[1, 0]
    ax3.plot(x_range, M_harper_corrected, 'g-', linewidth=0.5, alpha=0.7)
    ax3.set_xlabel('x')
    ax3.set_ylabel('|M(x)|·(log log x)^{1/4}/√x')
    ax3.set_title('Harper-Corrected Normalization')
    ax3.grid(True, alpha=0.3)

    # Plot 4: Running maximum comparison
    ax4 = axes[1, 1]
    x_plot_max = np.arange(1000, X_MAX + 1)
    running_max_norm = [running_max[x-1] / np.sqrt(x) for x in x_plot_max]
    ax4.plot(x_plot_max, running_max_norm, 'r-', linewidth=1, label='max|M|/√x')
    ax4.set_xlabel('x')
    ax4.set_ylabel('max_{y≤x}|M(y)|/√x')
    ax4.set_title('Running Maximum (normalized)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/harper_analysis.png', dpi=150)
    print("\n[Figure saved to harper_analysis.png]")

except Exception as e:
    print(f"\n[Could not create visualization: {e}]")
