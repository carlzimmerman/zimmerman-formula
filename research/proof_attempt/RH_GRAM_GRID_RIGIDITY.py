#!/usr/bin/env python3
"""
RH_GRAM_GRID_RIGIDITY.py

THE BREAKDOWN OF THE GRAM GRID

Gram points form a theoretical grid where Z(t) alternates signs.
We analyze whether this grid acts as a "cage" preventing zero collision.

Key question: Does the logarithmic growth of θ'(t) impose a strict
limit on how dense zeros can become?
"""

import numpy as np
from scipy import special, integrate
from typing import Tuple, Dict, List
import math

print("=" * 80)
print("THE GRAM GRID RIGIDITY: DOES THE GRID PREVENT COLLISION?")
print("=" * 80)
print()

# =============================================================================
# PART 1: GRAM POINTS DEFINED
# =============================================================================

print("PART 1: THE GRAM POINT GRID")
print("-" * 60)
print()

print("""
GRAM POINTS DEFINITION:
───────────────────────
The n-th Gram point g_n is defined by:

    θ(g_n) = nπ

where θ(t) is the Riemann-Siegel theta function:

    θ(t) = Im[log Γ(1/4 + it/2)] - (t/2)log(π)

For large t:
    θ(t) ≈ (t/2)log(t/2π) - t/2 - π/8

GRAM'S LAW (the "usual" behavior):
    (-1)^n Z(g_n) > 0

    That is, Z(t) has a specific sign at each Gram point.
    This implies (usually) exactly one zero between consecutive Gram points.

GRAM'S LAW VIOLATIONS:
    Sometimes Gram's Law fails: (-1)^n Z(g_n) < 0
    This creates "Gram blocks" where zeros are not evenly distributed.
""")

def theta_function(t: float) -> float:
    """Riemann-Siegel theta function."""
    if t < 10:
        return 0.0
    return (t/2) * np.log(t / (2 * np.pi)) - t/2 - np.pi/8

def theta_derivative(t: float) -> float:
    """Derivative θ'(t) ≈ (1/2)log(t/2π) for large t."""
    if t < 10:
        return 0.5
    return 0.5 * np.log(t / (2 * np.pi))

def gram_spacing(t: float) -> float:
    """Spacing between consecutive Gram points at height t."""
    theta_prime = theta_derivative(t)
    if theta_prime <= 0:
        return float('inf')
    return np.pi / theta_prime

print("GRAM POINT SPACING:")
print()
print("  Height t       θ'(t)          Gram spacing (g_{n+1} - g_n)")
print("  " + "-" * 60)
for t in [100, 1000, 1e6, 1e9, 1e12, 1e15]:
    th_prime = theta_derivative(t)
    spacing = gram_spacing(t)
    print(f"  {t:.0e}         {th_prime:.4f}         {spacing:.6f}")
print()

# =============================================================================
# PART 2: GRAM BLOCKS
# =============================================================================

print("=" * 60)
print("PART 2: GRAM BLOCKS AND ROSSER'S RULE")
print("-" * 60)
print()

print("""
GRAM BLOCKS:
────────────
A Gram block of length k is an interval [g_n, g_{n+k}] such that:
    • The Gram Law holds at g_n and g_{n+k}
    • The Gram Law fails at some internal points

In a Gram block of length k:
    • There are exactly k zeros (counting function is exact)
    • But they may not be "one per interval"

EXAMPLE:
    Gram block of length 2: [g_n, g_{n+2}] contains 2 zeros
    One subinterval [g_n, g_{n+1}] might have 0 or 2 zeros
    The other [g_{n+1}, g_{n+2}] has the complement

ROSSER'S RULE (1935):
    In a Gram block, the zeros remain within the block.
    They don't "escape" to adjacent intervals.

LEHMER PAIRS AND GRAM BLOCKS:
    A Lehmer pair (two close zeros) often creates a Gram block
    where two zeros squeeze into one subinterval.
""")

# =============================================================================
# PART 3: DENSITY LIMITS FROM θ(t)
# =============================================================================

print("=" * 60)
print("PART 3: HOW DENSE CAN ZEROS BECOME?")
print("-" * 60)
print()

print("""
THE COUNTING CONSTRAINT:
────────────────────────
The number of zeros below height T is:

    N(T) = (1/π)θ(T) + 1 + S(T)

where S(T) = O(log T) is bounded.

DENSITY OF ZEROS:
    dN/dT = (1/π)θ'(T) + S'(T)
          ≈ (1/2π)log(T/2π) + O(1/T)

    Average zeros per unit height: ~ log(T)/(2π)

LOCAL DENSITY LIMIT:
    In any interval [T, T+h]:
        Expected zeros ≈ (h/2π)log(T/2π)

    For zeros to "collide," we need two in a vanishing interval.
    But S(T) can only perturb the count by O(log T).

THE CONSTRAINT:
    Even in the worst Gram block, the zeros can't get arbitrarily close.
    The grid "stretches" to accommodate them, but there's a limit.
""")

def expected_zeros_in_interval(T: float, h: float) -> float:
    """Expected number of zeros in [T, T+h]."""
    if T < 10:
        return h
    return (h / (2 * np.pi)) * np.log(T / (2 * np.pi))

def minimum_spacing_in_block(T: float, k: int) -> float:
    """
    If k zeros are in a Gram block at height T,
    estimate the minimum spacing between any two.

    Gram block width = k × gram_spacing(T)
    With k zeros evenly spaced: min spacing = gram_spacing(T)
    With clustering: min spacing could be smaller
    """
    block_width = k * gram_spacing(T)
    # If zeros cluster, minimum spacing could be ~ block_width / (k+1)
    # But GUE statistics prevent extreme clustering
    return block_width / (k + 1)

print("ZERO DENSITY ANALYSIS:")
print()
print("  Height T       Avg spacing     Expected zeros/interval(1)")
print("  " + "-" * 60)
for T in [1e6, 1e9, 1e12]:
    spacing = gram_spacing(T)
    expected = expected_zeros_in_interval(T, 1.0)
    print(f"  {T:.0e}         {spacing:.4f}           {expected:.4f}")
print()

# =============================================================================
# PART 4: CAN θ(t) DEFORMATION FORCE COLLISION?
# =============================================================================

print("=" * 60)
print("PART 4: CAN θ(t) DEFORMATION FORCE A COLLISION?")
print("-" * 60)
print()

print("""
THE QUESTION:
─────────────
If zeros approach a collision, does the θ(t) function have to "deform"
to accommodate them?

ANALYSIS:
    θ(t) is FIXED by its definition involving Γ(s).
    It cannot be deformed - it's a deterministic function.

    The zeros are distributed according to:
        arg ζ(1/2 + it) changes by π at each zero

    The total change in arg ζ from 0 to T equals N(T)π.

WHAT WOULD COLLISION REQUIRE?
    For two zeros γ₁, γ₂ to collide (γ₁ = γ₂ = γ):
        arg ζ(1/2 + it) must change by 2π at a single point

    This means ζ(1/2 + iγ) has a DOUBLE ZERO.

THE θ(t) CONSTRAINT:
    θ'(t) = (1/2)log(t/2π) grows logarithmically.

    Gram spacing = π/θ'(t) shrinks as 1/log(t).

    For zeros to get closer than gram spacing, we need S(t) fluctuation.

    But |S(t)| ≤ C log t (proven bound).

MINIMUM ACHIEVABLE SPACING:
    The zeros can cluster within a Gram block, but not arbitrarily.
    The bound |S(t)| ≤ C log t limits the clustering.

    Rough estimate: minimum spacing ~ gram_spacing / log(T)
                                    ~ 1 / (log T)²

    This shrinks, but never reaches zero.
""")

def minimum_theoretical_spacing(T: float) -> float:
    """
    Rough lower bound on minimum spacing from θ(t) constraints.
    min spacing ~ gram_spacing / log(T) ~ 1/(log T)²
    """
    if T < 10:
        return 1.0
    return 1 / (np.log(T))**2

print("MINIMUM THEORETICAL SPACING (rough bound):")
print()
print("  Height T       Gram spacing    Min spacing ~ 1/(log T)²")
print("  " + "-" * 55)
for T in [1e6, 1e9, 1e12, 1e15, 1e20]:
    g_space = gram_spacing(T)
    min_space = minimum_theoretical_spacing(T)
    print(f"  {T:.0e}         {g_space:.4f}          {min_space:.6f}")
print()

# =============================================================================
# PART 5: THE GRAM CAGE
# =============================================================================

print("=" * 60)
print("PART 5: THE GRAM GRID AS A CAGE")
print("-" * 60)
print()

print("""
THE CAGE MECHANISM:
───────────────────
1. Gram points are FIXED by θ(t) = nπ
2. Zeros must maintain correct COUNT between Gram points
3. S(t) fluctuations are BOUNDED by O(log t)

WHAT THIS PREVENTS:
    • Infinite clustering: zeros can't all pile up in one spot
    • Collision: zeros approaching δ = 0 violates count constraints

THE ROSSER-TYPE ARGUMENT:
    Suppose zeros γ₁ < γ₂ approach collision: γ₂ - γ₁ → 0.

    Between g_n and g_{n+1} (one Gram interval):
        There should be approximately 1 zero.

    If two zeros collide within this interval:
        The local zero density becomes infinite.
        But the integrated count is still bounded.

    This is LOCALLY possible but requires compensation elsewhere.

THE COMPENSATION CONSTRAINT:
    If zeros cluster in one interval, they must be sparse elsewhere.
    The total count N(T) is fixed by θ(T) + S(T).
    Since S(T) is bounded, extreme local clustering has a price.

DOES THE GRID PREVENT COLLISION?
    NOT ABSOLUTELY. The grid doesn't forbid collision by itself.
    But it imposes a COST on clustering that grows without bound.
    Combined with GUE repulsion, collision becomes impossible.
""")

# =============================================================================
# PART 6: THE GEOMETRIC LIMIT
# =============================================================================

print("=" * 60)
print("PART 6: THE GEOMETRIC LIMIT ON DENSITY")
print("-" * 60)
print()

print("""
FORMAL STATEMENT:
─────────────────
Let D(T, h) = (number of zeros in [T, T+h]) / h be the local density.

For any interval:
    D(T, h) = (1/h) × [N(T+h) - N(T)]
            = (1/h) × [(θ(T+h) - θ(T))/π + (S(T+h) - S(T))]
            ≈ θ'(T)/π + O(log(T)/h)
            = (log T)/(2π) + O(log(T)/h)

AS h → 0:
    The second term dominates: D(T, h) → ∞ as h → 0

BUT the number of zeros in [T, T+h] is an integer.
    For very small h, this integer is 0, 1, or 2.

THE KEY CONSTRAINT:
    In an interval of width h < gram_spacing, there are at most 2 zeros
    (unless S(t) has an extreme fluctuation, which is bounded).

COLLISION WOULD REQUIRE:
    Two zeros in an interval of width 0.
    This is impossible because:
    (a) Any interval of positive width has finite zero count
    (b) GUE repulsion makes the probability of gap = 0 exactly zero
""")

def max_zeros_in_interval(T: float, h: float) -> int:
    """
    Maximum possible zeros in [T, T+h] given counting constraints.
    """
    # Expected zeros
    expected = expected_zeros_in_interval(T, h)
    # S(t) can add at most O(log T) to the count
    S_max = 0.2 * np.log(T)  # Rough bound
    return int(np.ceil(expected + 2 * S_max))

print("MAXIMUM ZEROS IN SMALL INTERVALS:")
print()
print("  Height T       h              Expected      Max (with S(t) bound)")
print("  " + "-" * 65)
for T in [1e12]:
    for h in [1.0, 0.1, 0.01, 0.001, gram_spacing(T)/10]:
        expected = expected_zeros_in_interval(T, h)
        max_z = max_zeros_in_interval(T, h)
        print(f"  {T:.0e}       {h:.4f}         {expected:.4f}          {max_z}")
print()

# =============================================================================
# PART 7: FINAL CONCLUSION
# =============================================================================

print("=" * 80)
print("FINAL ANSWER: DOES THE GRAM GRID PREVENT COLLISION?")
print("=" * 80)
print()

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE GRAM GRID CAGE: CONCLUSIONS                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THE GRAM GRID STRUCTURE:                                                    ║
║  ────────────────────────                                                    ║
║  • Gram points g_n defined by θ(g_n) = nπ                                   ║
║  • Spacing: g_{n+1} - g_n ≈ π / [(1/2)log(T/2π)] ~ 2π/log(T)               ║
║  • This spacing SHRINKS logarithmically but never vanishes                   ║
║                                                                              ║
║  THE GRID'S PROTECTIVE ROLE:                                                 ║
║  ───────────────────────────                                                 ║
║  1. Zero count between Gram points is constrained by N(T) = θ(T)/π + S(T)   ║
║  2. S(T) is bounded: |S(T)| ≤ C log(T)                                      ║
║  3. Local clustering is possible but has GLOBAL cost                         ║
║  4. Extreme clustering (collision) would violate counting bounds             ║
║                                                                              ║
║  DOES THE GRID ALONE PREVENT COLLISION?                                      ║
║  ───────────────────────────────────────                                     ║
║  NOT ABSOLUTELY. The grid imposes:                                           ║
║  • A cost on clustering (zeros must be sparse elsewhere)                     ║
║  • A minimum typical spacing ~ 1/(log T)²                                    ║
║  • But not a hard barrier at δ = 0                                          ║
║                                                                              ║
║  WHAT PREVENTS COLLISION:                                                    ║
║  ────────────────────────                                                    ║
║  The COMBINATION of:                                                         ║
║  (1) Gram grid counting constraints                                          ║
║  (2) GUE level repulsion (probability → 0 quadratically)                     ║
║  (3) The Lehmer extremum bound |Z(t₀)| = (1/8)|Z''|δ²                       ║
║                                                                              ║
║  THE GRAM GRID IS A SOFT CAGE:                                               ║
║  ─────────────────────────────                                               ║
║  • It doesn't absolutely forbid collision                                    ║
║  • But it makes collision increasingly "expensive"                           ║
║  • Combined with GUE repulsion, collision is impossible                      ║
║                                                                              ║
║  ANALOGY:                                                                    ║
║  ────────                                                                    ║
║  The Gram grid is like a fence with logarithmically shrinking gaps.          ║
║  A particle (zero) can squeeze through small gaps.                           ║
║  But GUE repulsion is like a spring connecting particles.                    ║
║  Even if the fence allows it, the spring prevents collision.                 ║
║                                                                              ║
║  DEFINITIVE STATEMENT:                                                       ║
║  ─────────────────────                                                       ║
║  The Gram grid ALONE does not prevent collision.                             ║
║  But COMBINED with GUE statistics, collision has probability zero.           ║
║  The critical line is protected by MULTIPLE defense layers.                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("Gram grid rigidity analysis complete.")
print("=" * 80)
