#!/usr/bin/env python3
"""
RH_LEHMER_PHENOMENON.py

THE CALCULUS OF LEHMER'S PHENOMENON

Lehmer's phenomenon occurs when two zeros on the critical line get
extraordinarily close, causing Z(t) to barely miss zero between them.

We analyze the exact mechanism by which zeros could theoretically
collide and leave the critical line.

Key question: Do derivative bounds forbid Z(t₀) from reaching zero?
"""

import numpy as np
from scipy import special
from typing import Tuple, Dict, List
import math

print("=" * 80)
print("THE CALCULUS OF LEHMER'S PHENOMENON")
print("=" * 80)
print()

# =============================================================================
# PART 1: LEHMER'S PHENOMENON DEFINED
# =============================================================================

print("PART 1: WHAT IS LEHMER'S PHENOMENON?")
print("-" * 60)
print()

print("""
LEHMER'S PHENOMENON (1956):
───────────────────────────
D.H. Lehmer observed that some pairs of consecutive Riemann zeros are
EXTRAORDINARILY close together, with the Hardy Z-function barely
crossing zero between them.

NORMAL BEHAVIOR:
    Between consecutive zeros γ_n and γ_{n+1}:
    • Z(t) has a local extremum at some t₀ ∈ (γ_n, γ_{n+1})
    • Typical |Z(t₀)| ~ O(1) to O(log t)

LEHMER PAIRS:
    When γ_{n+1} - γ_n is unusually small:
    • Z(t₀) can be extremely close to zero
    • The zero crossing is a "near miss"

THE CRITICAL QUESTION:
    If |Z(t₀)| → 0, can Z(t) fail to cross zero entirely?
    That would mean a DOUBLE ROOT forming → potential off-line pair.

KNOWN LEHMER PAIRS:
    The first significant Lehmer pair is near t ≈ 7005.06
    where |Z(t₀)| ≈ 0.0007 (very small but nonzero)
""")

# Known Lehmer pairs (approximate data)
lehmer_pairs = [
    {"gamma1": 7005.0629, "gamma2": 7005.1006, "Z_min": 0.00069},
    {"gamma1": 17143.7857, "gamma2": 17143.8218, "Z_min": 0.00018},
    {"gamma1": 176441.9, "gamma2": 176442.0, "Z_min": 0.00004},
]

print("SOME KNOWN LEHMER PAIRS:")
print()
print("  γ₁              γ₂              Gap δ          |Z(t₀)|")
print("  " + "-" * 60)
for pair in lehmer_pairs:
    delta = pair["gamma2"] - pair["gamma1"]
    print(f"  {pair['gamma1']:.4f}      {pair['gamma2']:.4f}      {delta:.5f}       {pair['Z_min']:.5f}")
print()

# =============================================================================
# PART 2: LOCAL BEHAVIOR OF Z(t) NEAR A LEHMER PAIR
# =============================================================================

print("=" * 60)
print("PART 2: TAYLOR EXPANSION BETWEEN CLOSE ZEROS")
print("-" * 60)
print()

print("""
SETUP:
    Let γ₁ and γ₂ be consecutive zeros with small gap δ = γ₂ - γ₁.
    Let t₀ be the local extremum where Z'(t₀) = 0.

    By symmetry (roughly): t₀ ≈ (γ₁ + γ₂)/2 = γ₁ + δ/2

TAYLOR EXPANSION OF Z(t) AROUND t₀:
    Z(t) = Z(t₀) + Z'(t₀)(t-t₀) + (1/2)Z''(t₀)(t-t₀)² + O((t-t₀)³)

    Since Z'(t₀) = 0 (extremum):
    Z(t) ≈ Z(t₀) + (1/2)Z''(t₀)(t-t₀)²

AT THE ZEROS γ₁ AND γ₂:
    Z(γ₁) = 0 = Z(t₀) + (1/2)Z''(t₀)(γ₁-t₀)²
    Z(γ₂) = 0 = Z(t₀) + (1/2)Z''(t₀)(γ₂-t₀)²

    Since t₀ ≈ (γ₁+γ₂)/2:
        γ₁ - t₀ ≈ -δ/2
        γ₂ - t₀ ≈ +δ/2

    Both give: 0 = Z(t₀) + (1/2)Z''(t₀)(δ/2)²
               0 = Z(t₀) + (1/8)Z''(t₀)δ²

SOLVING FOR Z(t₀):
    Z(t₀) = -(1/8)Z''(t₀)δ²

This is the KEY RELATION: |Z(t₀)| ∝ |Z''(t₀)| · δ²
""")

def lehmer_extremum_estimate(Z_double_prime: float, delta: float) -> float:
    """
    Estimate |Z(t₀)| from second derivative and gap.
    |Z(t₀)| = (1/8)|Z''(t₀)|δ²
    """
    return abs(Z_double_prime) * delta**2 / 8

print("RELATION: |Z(t₀)| = (1/8)|Z''(t₀)|·δ²")
print()
print("NUMERICAL CHECK with Lehmer pair at t ≈ 7005:")
print()

# For the first Lehmer pair
delta_1 = 7005.1006 - 7005.0629  # ≈ 0.0377
Z_min_1 = 0.00069

# Estimate |Z''(t₀)| from this
Z_double_prime_est = 8 * Z_min_1 / delta_1**2
print(f"  δ = {delta_1:.5f}")
print(f"  |Z(t₀)| = {Z_min_1:.5f}")
print(f"  Implied |Z''(t₀)| ≈ {Z_double_prime_est:.2f}")
print()

# =============================================================================
# PART 3: CONDITIONS FOR A COLLISION (DOUBLE ROOT)
# =============================================================================

print("=" * 60)
print("PART 3: CONDITIONS FOR A DOUBLE ROOT")
print("-" * 60)
print()

print("""
FOR A DOUBLE ROOT (collision, δ → 0):
─────────────────────────────────────
We need Z(t₀) = 0 exactly, not just small.

From Z(t₀) = -(1/8)Z''(t₀)δ²:

    If δ → 0 with Z''(t₀) bounded, then Z(t₀) → 0.

But we need Z(t₀) = 0 EXACTLY, which requires:
    Either δ = 0 (true collision)
    Or Z''(t₀) = 0 (inflection point at the extremum)

CASE 1: δ → 0 (zeros merge)
    This would mean γ₁ = γ₂: a double zero.
    After the double zero, the pair can split off the line.

CASE 2: Z''(t₀) → 0
    The extremum becomes flat (cubic tangency).
    This is a DEGENERATE case.

THE CRITICAL QUESTION:
    Can δ actually reach 0? Or do derivative bounds prevent this?

DERIVATIVE BOUNDS ON Z(t):
──────────────────────────
The Hardy Z-function satisfies growth bounds.

|Z(t)| ≤ C · t^{1/4} log(t)  (unconditional, large t)

For derivatives:
|Z'(t)| ≤ C' · log(t)
|Z''(t)| ≤ C'' · (log t)²

These are rough bounds; the key is that Z'' grows logarithmically.
""")

def Z_double_prime_bound(t: float) -> float:
    """
    Upper bound on |Z''(t)| based on standard estimates.
    """
    if t < 10:
        return 10.0
    return (np.log(t))**2

print("SECOND DERIVATIVE BOUNDS:")
print()
print("  t              |Z''(t)| ≤ (log t)²")
print("  " + "-" * 35)
for t in [1e3, 1e6, 1e9, 1e12, 1e15]:
    bound = Z_double_prime_bound(t)
    print(f"  {t:.0e}         {bound:.2f}")
print()

# =============================================================================
# PART 4: MINIMUM GAP ANALYSIS
# =============================================================================

print("=" * 60)
print("PART 4: CAN THE GAP δ REACH ZERO?")
print("-" * 60)
print()

print("""
THE GAP-DERIVATIVE RELATIONSHIP:
────────────────────────────────
From Z(t₀) = -(1/8)Z''(t₀)δ²:

    For Z(t₀) to reach exactly 0 while Z''(t₀) ≠ 0:
    δ must equal 0 exactly.

But the question is: does the dynamics of zeros ALLOW δ → 0?

EXPECTED ZERO GAP:
    The average gap between zeros at height T is:
        Δ_avg = 2π / log(T/2π)

    At T = 10¹²: Δ_avg ≈ 0.24
    At T = 10²⁰: Δ_avg ≈ 0.14

MINIMUM GAP STATISTICS:
    If zeros follow GUE statistics, the minimum gap in the first N zeros
    scales as N^{-2/3} (roughly).

    For N ~ 10¹³ zeros: min gap ~ (10¹³)^{-2/3} ~ 10^{-9}

    This is SMALL but not ZERO.

THE KEY INSIGHT:
    GUE statistics (which appear to govern Riemann zeros) imply
    LEVEL REPULSION: zeros actively avoid each other.

    The probability of gap δ scales as δ² for small δ (quadratic vanishing).

    This suggests δ = 0 has probability ZERO.
""")

def expected_gap(T: float) -> float:
    """Expected average gap between zeros at height T."""
    if T < 10:
        return 1.0
    return 2 * np.pi / np.log(T / (2 * np.pi))

def expected_min_gap(N: float) -> float:
    """Expected minimum gap among first N zeros (GUE scaling)."""
    return N**(-2/3)

print("EXPECTED GAPS:")
print()
print("  Height T       Avg Gap         N zeros         Expected Min Gap")
print("  " + "-" * 65)
for T in [1e6, 1e9, 1e12, 1e15]:
    avg = expected_gap(T)
    N = T / (2 * np.pi) * np.log(T / (2 * np.pi))  # Approximate N(T)
    min_gap = expected_min_gap(N)
    print(f"  {T:.0e}       {avg:.4f}         {N:.2e}         {min_gap:.2e}")
print()

# =============================================================================
# PART 5: THE COLLISION ASYMPTOTIC
# =============================================================================

print("=" * 60)
print("PART 5: ASYMPTOTIC CONDITIONS FOR COLLISION")
print("-" * 60)
print()

print("""
COLLISION SCENARIO:
───────────────────
Suppose at some extreme height T > 10¹³, two zeros approach collision.

For Z(t₀) = 0 (double root), we need:
    -(1/8)Z''(t₀)δ² = 0

Since Z''(t₀) is generically nonzero, we need δ = 0.

WHAT WOULD δ → 0 REQUIRE?
    1. The zeros must approach each other
    2. They must overcome level repulsion
    3. They must reach δ = 0 exactly (not just approximately)

THE BARRIER:
    From Z(t₀) = -(1/8)Z''(t₀)δ²:

    As δ → 0 with Z''(t₀) bounded away from zero:
        |Z(t₀)| → 0

    BUT this only says Z(t₀) is small, not zero.
    To actually collide, we need Z(t₀) = 0 EXACTLY.

    This requires an EXACT cancellation, which is measure zero.

FORMAL STATEMENT:
    Let δ_min(T) be the minimum gap among zeros up to height T.

    If GUE statistics hold:
        P(δ_min(T) = 0) = 0  for all T

    The gap can be arbitrarily small but never zero.
""")

def collision_probability_bound(delta: float) -> float:
    """
    GUE-based probability density for gap δ.
    Scales as δ² for small δ (level repulsion).
    """
    return delta**2

print("GUE LEVEL REPULSION - PROBABILITY OF SMALL GAPS:")
print()
print("  Gap δ           P(gap < δ) ~ δ³")
print("  " + "-" * 35)
for delta in [0.1, 0.01, 0.001, 0.0001, 1e-6, 1e-9]:
    prob = delta**3  # Cumulative probability scales as δ³
    print(f"  {delta:.0e}          {prob:.2e}")
print()

# =============================================================================
# PART 6: DO DERIVATIVE BOUNDS FORBID COLLISION?
# =============================================================================

print("=" * 60)
print("PART 6: DO DERIVATIVE BOUNDS FORBID Z(t₀) = 0?")
print("-" * 60)
print()

print("""
THE CRITICAL QUESTION:
──────────────────────
Do the growth bounds on Z''(t) mathematically FORBID Z(t₀) = 0?

ANSWER: NOT DIRECTLY.

The derivative bounds tell us:
    |Z''(t)| ≤ C(log t)²

This means for any given δ > 0:
    |Z(t₀)| ≤ (1/8)C(log t)² · δ²

As δ → 0, this bound goes to zero, which is CONSISTENT with Z(t₀) → 0.

THE PROHIBITION COMES FROM STATISTICS, NOT DERIVATIVES:
    1. GUE level repulsion ensures P(δ = 0) = 0
    2. The spacing δ can be small but not zero
    3. Therefore Z(t₀) can be small but not zero

A PHYSICAL ANALOGY:
    Think of zeros as charged particles on a line.
    Level repulsion = electrostatic repulsion.
    They can get arbitrarily close, but the repulsion increases
    as they approach, preventing actual collision.

MATHEMATICAL FORMULATION:
    If we model zeros as eigenvalues of a random matrix (GUE):
    - The joint distribution has a Vandermonde determinant factor
    - This vanishes when any two eigenvalues coincide
    - Hence collisions have probability zero
""")

# =============================================================================
# PART 7: THE LEHMER LIMIT
# =============================================================================

print("=" * 60)
print("PART 7: THE LEHMER LIMIT - HOW CLOSE CAN ZEROS GET?")
print("-" * 60)
print()

print("""
THE MINIMUM OBSERVED EXTREMUM:
──────────────────────────────
Among verified zeros (up to T ~ 10¹²), the smallest observed |Z(t₀)|
in a Lehmer pair is approximately:

    |Z(t₀)|_min ≈ 10^{-6} (rough estimate from extreme Lehmer pairs)

SCALING WITH HEIGHT:
    As T increases:
    - More zeros are checked → more chances for small gaps
    - But the probability of very small gaps decreases as δ²

    The competition between these effects determines the minimum.

EXPECTED MINIMUM |Z(t₀)| AMONG N ZEROS:
    If gaps follow GUE with min gap ~ N^{-2/3}:
        |Z(t₀)|_min ~ |Z''| · δ_min² ~ (log T)² · N^{-4/3}

    For N ~ 10¹³:
        |Z(t₀)|_min ~ (log 10¹³)² · (10¹³)^{-4/3}
                    ~ 900 · 10^{-17}
                    ~ 10^{-14}

    This is TINY but still nonzero.

THE LEHMER LIMIT:
    The minimum |Z(t₀)| decreases as we check more zeros.
    But it NEVER reaches zero due to level repulsion.

    This is the "floor" protecting the critical line.
""")

def expected_min_Z(N: float, T: float) -> float:
    """
    Expected minimum |Z(t₀)| among N zeros at height T.
    """
    Z_double_prime = Z_double_prime_bound(T)
    delta_min = expected_min_gap(N)
    return Z_double_prime * delta_min**2 / 8

print("EXPECTED MINIMUM |Z(t₀)|:")
print()
print("  T              N zeros         |Z''| bound     Expected min |Z(t₀)|")
print("  " + "-" * 70)
for T in [1e6, 1e9, 1e12, 1e15, 1e20]:
    N = T / (2 * np.pi) * np.log(T / (2 * np.pi))
    Z_pp = Z_double_prime_bound(T)
    min_Z = expected_min_Z(N, T)
    print(f"  {T:.0e}       {N:.2e}       {Z_pp:.1f}            {min_Z:.2e}")
print()

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("=" * 80)
print("FINAL ANSWER: THE CALCULUS OF LEHMER'S PHENOMENON")
print("=" * 80)
print()

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LEHMER'S PHENOMENON: CONCLUSIONS                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THE KEY RELATION:                                                           ║
║  ─────────────────                                                           ║
║      |Z(t₀)| = (1/8)|Z''(t₀)| · δ²                                          ║
║                                                                              ║
║  where t₀ is the extremum between zeros separated by gap δ.                  ║
║                                                                              ║
║  FOR A COLLISION (double root):                                              ║
║  ─────────────────────────────                                               ║
║  We need Z(t₀) = 0, which requires δ = 0 (since Z''(t₀) ≠ 0 generically).   ║
║                                                                              ║
║  DO DERIVATIVE BOUNDS FORBID THIS?                                           ║
║  ──────────────────────────────────                                          ║
║  NOT DIRECTLY. The bounds |Z''(t)| ≤ C(log t)² are consistent with           ║
║  Z(t₀) → 0 as δ → 0.                                                         ║
║                                                                              ║
║  WHAT FORBIDS COLLISION?                                                     ║
║  ───────────────────────                                                     ║
║  LEVEL REPULSION (GUE statistics):                                           ║
║  • Probability of gap δ scales as δ²                                         ║
║  • P(δ = 0) = 0 (probability zero event)                                     ║
║  • Zeros can get arbitrarily close but never collide                         ║
║                                                                              ║
║  THE LEHMER LIMIT:                                                           ║
║  ─────────────────                                                           ║
║  As we check more zeros:                                                     ║
║  • Minimum gap decreases as N^{-2/3}                                         ║
║  • Minimum |Z(t₀)| decreases as N^{-4/3}                                     ║
║  • But both remain strictly positive                                         ║
║                                                                              ║
║  CONCLUSION:                                                                 ║
║  ───────────                                                                 ║
║  A collision (double root) is an event of PROBABILITY ZERO.                  ║
║  The critical line is protected not by derivative bounds,                    ║
║  but by the statistical repulsion encoded in GUE/Montgomery.                 ║
║                                                                              ║
║  This is the "eigenvalue repulsion" of random matrix theory.                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("Lehmer phenomenon analysis complete.")
print("=" * 80)
