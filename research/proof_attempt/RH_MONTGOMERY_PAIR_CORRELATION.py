#!/usr/bin/env python3
"""
RH_MONTGOMERY_PAIR_CORRELATION.py

MONTGOMERY'S PAIR CORRELATION AND GUE LEVEL REPULSION

We analyze the statistical probability of a zero-collision using
Montgomery's Pair Correlation Conjecture and the GUE level repulsion.

Key question: Does the quadratic vanishing near x=0 mathematically
guarantee that a double root has probability strictly zero?
"""

import numpy as np
from scipy import special, integrate
from typing import Tuple, Dict, List
import math

print("=" * 80)
print("MONTGOMERY'S PAIR CORRELATION AND LEVEL REPULSION")
print("=" * 80)
print()

# =============================================================================
# PART 1: THE PAIR CORRELATION CONJECTURE
# =============================================================================

print("PART 1: MONTGOMERY'S PAIR CORRELATION CONJECTURE (1973)")
print("-" * 60)
print()

print("""
MONTGOMERY'S DISCOVERY:
───────────────────────
In 1973, Hugh Montgomery studied the pair correlation of Riemann zeros.

Define normalized zeros:
    γ̃_n = γ_n · (log γ_n / 2π)    (so average spacing is 1)

PAIR CORRELATION FUNCTION:
    R₂(x) = lim_{N→∞} (1/N) Σ_{n,m ≤ N, n≠m} δ(x - (γ̃_m - γ̃_n))

For independent random points on a line:
    R₂(x) = 1  (constant)

MONTGOMERY'S CONJECTURE:
    For Riemann zeros, the pair correlation is:

    R₂(x) = 1 - (sin(πx) / πx)²

This is EXACTLY the pair correlation of GUE eigenvalues!

THE CRITICAL FEATURE:
    As x → 0:
        R₂(x) = 1 - (sin(πx)/πx)² → 1 - 1 = 0

    The pair correlation VANISHES at x = 0.
    This is LEVEL REPULSION.
""")

def pair_correlation(x: float) -> float:
    """
    GUE pair correlation function R₂(x) = 1 - (sin(πx)/πx)².
    """
    if abs(x) < 1e-10:
        return 0.0  # Limit at x = 0
    return 1 - (np.sin(np.pi * x) / (np.pi * x))**2

print("PAIR CORRELATION R₂(x) = 1 - (sin(πx)/πx)²:")
print()
print("  x              R₂(x)")
print("  " + "-" * 30)
for x in [0.0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]:
    r2 = pair_correlation(x)
    print(f"  {x:.1f}            {r2:.6f}")
print()

# =============================================================================
# PART 2: LEVEL REPULSION - THE ENERGY BARRIER
# =============================================================================

print("=" * 60)
print("PART 2: LEVEL REPULSION AS AN ENERGY BARRIER")
print("-" * 60)
print()

print("""
PHYSICAL INTERPRETATION:
────────────────────────
If we think of zeros as particles on a line:

    R₂(x) ~ probability density of finding two zeros at distance x

The fact that R₂(0) = 0 means:
    The probability of two zeros being at the SAME POINT is ZERO.

ENERGY BARRIER INTERPRETATION:
    Define an effective "repulsion potential":

    V(x) = -log R₂(x)

    As x → 0:
        R₂(x) ~ (πx)² / 3  (Taylor expansion)
        V(x) ~ -log(x²) = -2 log|x| → +∞

    There is an INFINITE energy barrier preventing collision.

THE SINC² REPULSION:
    Near x = 0:
        sin(πx) ≈ πx - (πx)³/6 + ...
        (sin(πx)/πx)² ≈ 1 - (πx)²/3 + O(x⁴)
        R₂(x) ≈ (πx)²/3 = (π²/3) x²

    This is QUADRATIC VANISHING: R₂(x) ~ x² for small x.
""")

def taylor_R2(x: float) -> float:
    """Taylor approximation R₂(x) ≈ (π²/3)x² for small x."""
    return (np.pi**2 / 3) * x**2

def effective_potential(x: float) -> float:
    """Effective repulsion potential V(x) = -log R₂(x)."""
    r2 = pair_correlation(x)
    if r2 <= 0:
        return float('inf')
    return -np.log(r2)

print("QUADRATIC VANISHING OF R₂(x) NEAR x = 0:")
print()
print("  x              R₂(x) exact     R₂(x) ≈ (π²/3)x²    V(x) = -log R₂")
print("  " + "-" * 70)
for x in [0.5, 0.2, 0.1, 0.05, 0.01, 0.001]:
    r2_exact = pair_correlation(x)
    r2_taylor = taylor_R2(x)
    V = effective_potential(x)
    print(f"  {x:.3f}          {r2_exact:.6f}         {r2_taylor:.6f}            {V:.2f}")
print()

print("Note: V(x) → ∞ as x → 0 (infinite energy barrier).")
print()

# =============================================================================
# PART 3: PROBABILITY OF COLLISION
# =============================================================================

print("=" * 60)
print("PART 3: PROBABILITY OF A COLLISION (x → 0)")
print("-" * 60)
print()

print("""
THE FORMAL CALCULATION:
───────────────────────

Probability of finding TWO zeros with normalized gap < ε:

    P(gap < ε) = ∫₀^ε R₂(x) dx
               ≈ ∫₀^ε (π²/3) x² dx    (for small ε)
               = (π²/3) · ε³/3
               = (π²/9) ε³

KEY RESULT: P(gap < ε) ~ ε³  (CUBIC vanishing)

AS ε → 0:
    P(gap = 0) = lim_{ε→0} P(gap < ε) = 0

    A collision (gap exactly zero) has probability STRICTLY ZERO.

COMPARISON TO POISSON (independent points):
    For Poisson: P(gap < ε) ~ ε  (linear)
    For GUE:     P(gap < ε) ~ ε³ (cubic)

    GUE has MUCH STRONGER suppression of small gaps.
""")

def probability_gap_less_than(epsilon: float) -> float:
    """
    Probability that two normalized zeros have gap < ε.
    P(gap < ε) = ∫₀^ε R₂(x) dx ≈ (π²/9) ε³ for small ε.
    """
    if epsilon <= 0:
        return 0.0
    # Numerical integration for exact value
    result, _ = integrate.quad(pair_correlation, 0, epsilon)
    return result

def probability_gap_approx(epsilon: float) -> float:
    """Taylor approximation: P(gap < ε) ≈ (π²/9) ε³."""
    return (np.pi**2 / 9) * epsilon**3

print("PROBABILITY OF SMALL GAPS:")
print()
print("  ε              P(gap < ε) exact    P ≈ (π²/9)ε³      Ratio")
print("  " + "-" * 70)
for epsilon in [0.5, 0.2, 0.1, 0.05, 0.01, 0.001]:
    p_exact = probability_gap_less_than(epsilon)
    p_approx = probability_gap_approx(epsilon)
    ratio = p_exact / p_approx if p_approx > 0 else 0
    print(f"  {epsilon:.3f}          {p_exact:.6e}          {p_approx:.6e}         {ratio:.3f}")
print()

# =============================================================================
# PART 4: THE VANDERMONDE DETERMINANT
# =============================================================================

print("=" * 60)
print("PART 4: THE VANDERMONDE BARRIER (GUE MATHEMATICS)")
print("-" * 60)
print()

print("""
GUE EIGENVALUE DISTRIBUTION:
────────────────────────────
For an N×N GUE matrix, the joint probability density of eigenvalues is:

    P(λ₁, λ₂, ..., λ_N) ∝ |Δ(λ)|² · exp(-Σ λ_i²/2)

where Δ(λ) is the VANDERMONDE DETERMINANT:

    Δ(λ) = Π_{i<j} (λ_j - λ_i)

THE KEY PROPERTY:
    If ANY two eigenvalues coincide (λ_i = λ_j for i ≠ j):
        Δ(λ) = 0

    Therefore:
        P(..., λ_i = λ_j, ...) = 0

    Collisions have EXACTLY ZERO probability density.

TRANSLATION TO RIEMANN ZEROS:
    If Riemann zeros follow GUE statistics (Montgomery's conjecture):
        P(γ_n = γ_m) = 0 for n ≠ m

    This is not an approximation - it's EXACT within the GUE model.

THE VANDERMONDE "CAGE":
    The Vandermonde factor acts as an infinitely strong cage
    that prevents any two eigenvalues from ever coinciding.

    This is why level repulsion is FUNDAMENTAL to random matrix theory.
""")

def vandermonde(eigenvalues: np.ndarray) -> float:
    """
    Compute Vandermonde determinant Π_{i<j} (λ_j - λ_i).
    """
    n = len(eigenvalues)
    det = 1.0
    for i in range(n):
        for j in range(i+1, n):
            det *= (eigenvalues[j] - eigenvalues[i])
    return det

print("VANDERMONDE DETERMINANT EXAMPLES:")
print()

# Example with well-separated eigenvalues
lambda_sep = np.array([1.0, 2.0, 3.0, 4.0])
V_sep = vandermonde(lambda_sep)
print(f"  λ = [1, 2, 3, 4]:    |Δ|² = {V_sep**2:.0f}")

# Example with close eigenvalues
lambda_close = np.array([1.0, 1.01, 3.0, 4.0])
V_close = vandermonde(lambda_close)
print(f"  λ = [1, 1.01, 3, 4]: |Δ|² = {V_close**2:.4f}")

# Example with very close eigenvalues
lambda_very_close = np.array([1.0, 1.001, 3.0, 4.0])
V_very_close = vandermonde(lambda_very_close)
print(f"  λ = [1, 1.001, 3, 4]:|Δ|² = {V_very_close**2:.6f}")

# Example with coinciding eigenvalues
lambda_coincide = np.array([1.0, 1.0, 3.0, 4.0])
V_coincide = vandermonde(lambda_coincide)
print(f"  λ = [1, 1, 3, 4]:    |Δ|² = {V_coincide**2:.0f}  (EXACTLY ZERO)")
print()

# =============================================================================
# PART 5: IS COLLISION PROBABILITY STRICTLY ZERO?
# =============================================================================

print("=" * 60)
print("PART 5: IS COLLISION PROBABILITY STRICTLY ZERO?")
print("-" * 60)
print()

print("""
THE FORMAL ANSWER:
──────────────────

WITHIN THE GUE MODEL:
    P(λ_i = λ_j) = 0  EXACTLY

    This follows from the Vandermonde factor in the joint density.

FOR RIEMANN ZEROS (CONDITIONAL ON MONTGOMERY'S CONJECTURE):
    If zeros follow GUE pair correlation exactly:
        P(γ_n = γ_m) = 0  EXACTLY

    The zeros are "trapped" by level repulsion.

WHAT THIS MEANS FOR RH:
    1. If GUE statistics hold:
       - Zeros cannot collide
       - No double roots can form
       - Off-line pairs cannot be "born" from collision

    2. This does NOT prove RH directly:
       - It shows collision mechanism is forbidden IF GUE holds
       - GUE statistics are ASSUMED (Montgomery's conjecture)
       - We haven't proven GUE statistics hold

THE LOGICAL STRUCTURE:
    (Montgomery's Conjecture) ⟹ (No collisions possible) ⟹ (No off-line pairs)

    This is a CONDITIONAL result, not an unconditional proof.
""")

# =============================================================================
# PART 6: THE ENERGY BARRIER QUANTIFIED
# =============================================================================

print("=" * 60)
print("PART 6: QUANTIFYING THE ENERGY BARRIER")
print("-" * 60)
print()

print("""
TRANSLATING LEVEL REPULSION TO AN ENERGY SCALE:
───────────────────────────────────────────────

Define the "collision energy" needed to overcome level repulsion:

    E_collision(x) = -log(R₂(x))  for normalized spacing x

As x → 0:
    R₂(x) ~ (π²/3) x²
    E_collision(x) ~ -log(x²) = -2 log(x)

FOR UNNORMALIZED SPACING δ AT HEIGHT T:
    Normalized spacing: x = δ · (log T) / (2π)

    E_collision(δ, T) ~ -2 log(δ · log T / 2π)
                      = -2 log δ - 2 log(log T / 2π)

AT T = 10¹², δ = 10⁻⁶:
    log(T) / 2π ≈ 27.6 / 6.28 ≈ 4.4
    x ≈ 10⁻⁶ · 4.4 ≈ 4.4 × 10⁻⁶
    E_collision ≈ -2 log(4.4 × 10⁻⁶) ≈ 24.6

This is a LARGE energy barrier - collision is extremely suppressed.
""")

def collision_energy(x: float) -> float:
    """Energy barrier to bring zeros to normalized spacing x."""
    if x <= 0:
        return float('inf')
    return -2 * np.log(x)

def unnormalized_to_normalized(delta: float, T: float) -> float:
    """Convert unnormalized gap δ to normalized gap x."""
    return delta * np.log(T) / (2 * np.pi)

print("COLLISION ENERGY BARRIER:")
print()
print("  T              δ             x (normalized)    E_collision")
print("  " + "-" * 65)

for T in [1e6, 1e12]:
    for delta in [0.01, 0.001, 1e-6, 1e-9]:
        x = unnormalized_to_normalized(delta, T)
        E = collision_energy(x)
        print(f"  {T:.0e}       {delta:.0e}       {x:.2e}             {E:.1f}")
    print()

# =============================================================================
# PART 7: FINAL THEOREM
# =============================================================================

print("=" * 80)
print("FINAL ANSWER: THE GUE PROTECTION THEOREM")
print("=" * 80)
print()

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE GUE PROTECTION THEOREM                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THEOREM (Conditional on Montgomery's Conjecture):                           ║
║  ─────────────────────────────────────────────────                           ║
║  If Riemann zeros follow GUE pair correlation statistics, then:              ║
║                                                                              ║
║      P(γ_n = γ_m for some n ≠ m) = 0   (EXACTLY ZERO)                       ║
║                                                                              ║
║  PROOF:                                                                      ║
║  ──────                                                                      ║
║  1. GUE pair correlation: R₂(x) = 1 - (sin πx / πx)²                        ║
║  2. At x = 0: R₂(0) = 0 (quadratic vanishing)                               ║
║  3. Probability of gap < ε: P ~ ε³ (cubic vanishing)                        ║
║  4. As ε → 0: P → 0                                                         ║
║  5. Therefore P(gap = 0) = 0  □                                             ║
║                                                                              ║
║  ALTERNATIVE PROOF VIA VANDERMONDE:                                          ║
║  ──────────────────────────────────                                          ║
║  1. GUE joint density has factor |Δ(λ)|²                                    ║
║  2. Vandermonde Δ(λ) = Π_{i<j}(λ_j - λ_i)                                   ║
║  3. If λ_i = λ_j for any i ≠ j, then Δ = 0                                  ║
║  4. Therefore P(collision) = 0  □                                           ║
║                                                                              ║
║  PHYSICAL INTERPRETATION:                                                    ║
║  ────────────────────────                                                    ║
║  • Level repulsion creates infinite energy barrier at x = 0                  ║
║  • E_collision(x) ~ -2 log(x) → ∞ as x → 0                                  ║
║  • Zeros "repel" each other like charges                                     ║
║  • Collision requires infinite energy                                        ║
║                                                                              ║
║  CONSEQUENCE FOR RH:                                                         ║
║  ───────────────────                                                         ║
║  If GUE statistics hold:                                                     ║
║  • Zeros cannot collide to form double roots                                 ║
║  • Off-line pairs cannot be "born" from critical line collision             ║
║  • The critical line is protected by a statistical cage                      ║
║                                                                              ║
║  CAVEAT:                                                                     ║
║  ───────                                                                     ║
║  This is CONDITIONAL on Montgomery's Conjecture.                             ║
║  We have not proven GUE statistics hold for all zeros.                       ║
║  Numerical evidence strongly supports it, but it remains a conjecture.       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("Montgomery pair correlation analysis complete.")
print("=" * 80)
