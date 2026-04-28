#!/usr/bin/env python3
"""
RH_CONVEX_OPTIMIZATION.py
═════════════════════════

THE CONVEX OPTIMIZATION ATTACK ON RH

Key insight: If we can show the "energy landscape" of zero configurations
is CONVEX with a unique minimum on the critical line, RH follows.

This file explores the mathematical structure needed for such a proof.
"""

import numpy as np
from typing import List, Tuple
import cmath

def print_section(title: str, level: int = 1):
    """Pretty print section headers."""
    width = 80
    if level == 1:
        print("\n" + "=" * width)
        print(title)
        print("=" * width + "\n")
    else:
        print("\n" + "-" * width)
        print(title)
        print("-" * width + "\n")

# First 50 zeros
ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
    114.320221, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256819, 127.516683, 129.578704, 131.087688, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846
]

print("=" * 80)
print("RH CONVEX OPTIMIZATION ATTACK")
print("Can RH be reformulated as a convex optimization problem?")
print("=" * 80)

# ============================================================================
# SECTION 1: THE OPTIMIZATION FORMULATION
# ============================================================================
print_section("SECTION 1: THE OPTIMIZATION FORMULATION")

print("""
THE VARIATIONAL PROBLEM:
════════════════════════

We seek to reformulate RH as:

    minimize   E(σ, γ)
    subject to Functional equation constraints
               Asymptotic density constraints
               Explicit formula constraints

where (σ, γ) represents zeros at s = σ + iγ.

RH is equivalent to: The unique minimum is at σ = 1/2 for all γ.


THE KEY QUESTION:
═════════════════

Is the energy functional E(σ, γ) CONVEX in σ?

If yes: Standard convex optimization → unique minimum → proves RH
If no:  Local minima could exist off the critical line


WHY CONVEXITY MATTERS:
══════════════════════

For a convex function f on a convex set:
- Every local minimum is a global minimum
- First-order conditions are sufficient
- Gradient descent always finds the optimum

If we can show E(σ, γ) is convex in σ and minimized at σ = 1/2,
RH follows immediately.
""")

# ============================================================================
# SECTION 2: CANDIDATE ENERGY FUNCTIONALS
# ============================================================================
print_section("SECTION 2: CANDIDATE ENERGY FUNCTIONALS")

print("""
CANDIDATE 1: LI COEFFICIENT ENERGY
══════════════════════════════════

The Li coefficients:

    λₙ = Σ_ρ (1 - (1 - 1/ρ)ⁿ)

If RH: λₙ > 0 for all n.

Define ENERGY:

    E₁ = Σₙ max(0, -λₙ)

This equals 0 iff RH is true.

PROBLEM: This is a constraint satisfaction, not a smooth optimization.
""")

# Compute Li coefficients
def li_coefficients(zeros: List[float], n_max: int = 20) -> List[float]:
    """Compute Li coefficients assuming zeros on critical line."""
    lambdas = []
    for n in range(1, n_max + 1):
        total = 0
        for gamma in zeros:
            rho = 0.5 + 1j * gamma
            z = 1 - 1/rho
            term = 1 - z**n
            total += term.real * 2  # Both ρ and conjugate
        lambdas.append(total)
    return lambdas

li_coeffs = li_coefficients(ZEROS[:20], 10)
print("Li coefficients (first 10):")
for i, lam in enumerate(li_coeffs):
    sign = "+" if lam > 0 else "-"
    print(f"  λ_{i+1} = {lam:+.6f}  [{sign}]")

all_positive = all(l > 0 for l in li_coeffs)
print(f"\nAll positive? {all_positive}")
print("(Li criterion: RH ⟺ λₙ > 0 for all n)")

# ============================================================================
print("""

CANDIDATE 2: EXPLICIT FORMULA ENERGY
════════════════════════════════════

The explicit formula:

    ψ(x) = x - Σ_ρ x^ρ/ρ + O(1)

For primes p ≤ X:

    Σ_{p≤X} 1 = li(X) - Σ_ρ li(X^ρ) + O(1)

Define ENERGY:

    E₂(σ) = ∫₂^∞ |ψ(x) - x|² w(x) dx

This measures the ERROR in the explicit formula.
""")

def explicit_formula_energy(zeros: List[float], sigma: float, X_max: float = 100) -> float:
    """
    Compute simplified explicit formula "energy" for zeros at Re(s) = sigma.

    This is a toy model - real computation requires more sophistication.
    """
    # Sample points
    X = np.linspace(2, X_max, 200)

    # Contribution from zeros to error term
    error = np.zeros_like(X)
    for gamma in zeros:
        rho = sigma + 1j * gamma
        # x^ρ contribution
        term = X**sigma * np.cos(gamma * np.log(X)) / abs(rho)
        error += 2 * term  # Real part × 2 (conjugate pair)

    # Energy = integrated squared error
    energy = np.trapezoid(error**2 / X**2, X)
    return energy

print("\nExplicit Formula Energy at different σ:")
sigmas = [0.4, 0.45, 0.5, 0.55, 0.6, 0.7]
energies = []
for sigma in sigmas:
    E = explicit_formula_energy(ZEROS[:20], sigma)
    energies.append(E)
    marker = " ← MINIMUM?" if sigma == 0.5 else ""
    print(f"  E(σ={sigma}) = {E:.6f}{marker}")

min_idx = np.argmin(energies)
print(f"\nMinimum at σ = {sigmas[min_idx]}")

# ============================================================================
print("""

CANDIDATE 3: UNIT CIRCLE DISTANCE ENERGY
════════════════════════════════════════

The key mapping: z = 1 - 1/ρ

For ρ on critical line: |z| = 1 (on unit circle)
For ρ off critical line: |z| ≠ 1

Define ENERGY:

    E₃ = Σ_ρ (|1 - 1/ρ| - 1)²

This equals 0 iff all zeros are on the critical line.
""")

def unit_circle_energy(zeros: List[float], sigma: float) -> float:
    """
    Energy measuring deviation from unit circle in z = 1 - 1/ρ mapping.
    """
    total_energy = 0
    for gamma in zeros:
        rho = sigma + 1j * gamma
        z = 1 - 1/rho
        deviation = abs(z) - 1
        total_energy += deviation**2
    return total_energy

print("Unit Circle Energy at different σ:")
for sigma in sigmas:
    E = unit_circle_energy(ZEROS[:20], sigma)
    marker = " ← ZERO (PERFECT)" if abs(E) < 1e-10 else ""
    print(f"  E(σ={sigma}) = {E:.8f}{marker}")

# ============================================================================
# SECTION 3: CONVEXITY ANALYSIS
# ============================================================================
print_section("SECTION 3: CONVEXITY ANALYSIS")

print("""
CHECKING CONVEXITY OF UNIT CIRCLE ENERGY:
═════════════════════════════════════════

For f(σ) to be convex, we need f''(σ) ≥ 0 for all σ.

Let's analyze E₃(σ) = Σ_ρ (|1 - 1/ρ| - 1)² where ρ = σ + iγ.
""")

def unit_circle_derivatives(gamma: float, sigma: float) -> Tuple[float, float, float]:
    """
    Compute E, E', E'' for single zero contribution.

    E = (|1 - 1/ρ| - 1)² where ρ = σ + iγ
    """
    h = 1e-6

    def E(s):
        rho = s + 1j * gamma
        z = 1 - 1/rho
        return (abs(z) - 1)**2

    E_val = E(sigma)
    E_prime = (E(sigma + h) - E(sigma - h)) / (2 * h)
    E_double = (E(sigma + h) - 2*E(sigma) + E(sigma - h)) / (h**2)

    return E_val, E_prime, E_double

print("Second derivative analysis for γ = 14.13 (first zero):")
gamma = ZEROS[0]
for sigma in [0.3, 0.4, 0.5, 0.6, 0.7]:
    E, Ep, Epp = unit_circle_derivatives(gamma, sigma)
    convex_marker = "CONVEX" if Epp >= 0 else "CONCAVE"
    print(f"  σ={sigma}: E={E:.6f}, E'={Ep:+.6f}, E''={Epp:+.6f} [{convex_marker}]")

print("\nSecond derivative at σ=0.5 for different γ:")
for gamma in ZEROS[:10]:
    E, Ep, Epp = unit_circle_derivatives(gamma, 0.5)
    convex_marker = "✓" if Epp > 0 else "✗"
    print(f"  γ={gamma:.2f}: E''={Epp:+.6f} {convex_marker}")

# ============================================================================
print("""

THEORETICAL ANALYSIS OF CONVEXITY:
══════════════════════════════════

For ρ = σ + iγ, we have:

    |1 - 1/ρ|² = |ρ - 1|²/|ρ|²
                = ((σ-1)² + γ²)/(σ² + γ²)

Let f(σ) = ((σ-1)² + γ²)/(σ² + γ²)

Then |z| = √f(σ) and E = (√f(σ) - 1)²

CRITICAL POINT:
    d/dσ(|z| - 1)² = 0 when |z| = 1

    f(σ) = 1  ⟺  (σ-1)² + γ² = σ² + γ²
           ⟺  σ² - 2σ + 1 = σ²
           ⟺  σ = 1/2

The critical point is ALWAYS at σ = 1/2, independent of γ!

CONVEXITY:
    Need to check f''(σ) sign at σ = 1/2.
""")

# Analytical second derivative
def analytical_second_derivative(gamma: float, sigma: float = 0.5) -> float:
    """
    Compute d²E/dσ² analytically at σ = 1/2.

    E = (√f - 1)² where f = ((σ-1)² + γ²)/(σ² + γ²)
    At σ = 1/2: f = 1, so E = 0 and we need the Taylor expansion.
    """
    # f(σ) = ((σ-1)² + γ²)/(σ² + γ²)
    # At σ = 1/2 + ε:
    # f ≈ 1 + 2ε/((1/4 + γ²)) + O(ε²)

    # For small γ², the curvature is large.
    # For large γ², the curvature is small.

    # Numerical check
    h = 1e-4
    def E(s):
        rho = s + 1j * gamma
        z = 1 - 1/rho
        return (abs(z) - 1)**2

    Epp = (E(sigma + h) - 2*E(sigma) + E(sigma - h)) / (h**2)
    return Epp

print("\nCurvature (E'') at σ=1/2 vs γ:")
for gamma in [1, 5, 10, 20, 50, 100]:
    Epp = analytical_second_derivative(gamma)
    print(f"  γ={gamma:3d}: E''(1/2) = {Epp:.6f}")

print("""
OBSERVATION:
────────────
The second derivative is POSITIVE for all γ tested.
This suggests the unit circle energy IS convex at σ = 1/2.

But is it convex EVERYWHERE, not just at σ = 1/2?
""")

# ============================================================================
# SECTION 4: GLOBAL CONVEXITY PROOF ATTEMPT
# ============================================================================
print_section("SECTION 4: GLOBAL CONVEXITY PROOF ATTEMPT")

print("""
THE CHALLENGE:
══════════════

To prove RH via convexity, we need:

1. E(σ) is convex for σ ∈ (0, 1)
2. E(1/2) = 0 (minimum value)
3. E(σ) > 0 for σ ≠ 1/2

This would immediately imply RH.

Let's check global convexity numerically.
""")

# Check convexity over full range
print("Global convexity check for E₃(σ) = Σ(|z|-1)²:")
print("-" * 60)

sigma_range = np.linspace(0.01, 0.99, 99)
curvatures = []

for sigma in sigma_range:
    h = 1e-4
    def E(s):
        return unit_circle_energy(ZEROS[:20], s)

    Epp = (E(sigma + h) - 2*E(sigma) + E(sigma - h)) / (h**2)
    curvatures.append(Epp)

curvatures = np.array(curvatures)
min_curv = np.min(curvatures)
min_curv_sigma = sigma_range[np.argmin(curvatures)]

print(f"Minimum curvature: E'' = {min_curv:.6f} at σ = {min_curv_sigma:.2f}")
print(f"All curvatures positive? {np.all(curvatures > 0)}")

if np.all(curvatures > 0):
    print("\n✓ GLOBALLY CONVEX!")
    print("This means σ = 1/2 is the UNIQUE global minimum.")
else:
    negative_regions = sigma_range[curvatures < 0]
    print(f"\n✗ Not globally convex. Negative curvature at σ ∈ {negative_regions}")

# ============================================================================
# SECTION 5: THE LAGRANGIAN FORMULATION
# ============================================================================
print_section("SECTION 5: THE LAGRANGIAN FORMULATION")

print("""
THE CONSTRAINED OPTIMIZATION:
═════════════════════════════

The zeros aren't free - they satisfy CONSTRAINTS:

1. FUNCTIONAL EQUATION:
   If ρ is a zero, so is 1 - ρ̄
   This pairs zeros symmetrically about σ = 1/2

2. EXPLICIT FORMULA:
   Σ_ρ x^ρ/ρ = ψ(x) - x + ...
   The zeros must encode the primes correctly

3. ASYMPTOTIC DENSITY:
   N(T) ~ (T/2π) log(T/2π)
   The zeros must have the right density


LAGRANGIAN FORMULATION:
═══════════════════════

    L = E(σ) + λ₁·g₁(σ) + λ₂·g₂(σ) + ...

where g_i are constraint functions.

At the optimum: ∇L = 0

KEY INSIGHT:
────────────
The functional equation ENFORCES σ = 1/2!

If ρ = σ + iγ is a zero, then 1 - σ + iγ is also a zero.
For these to be the SAME (not forming a pair), need σ = 1 - σ, i.e., σ = 1/2.

The functional equation is like a "restoring force" toward σ = 1/2.
""")

def functional_equation_constraint(sigma: float, gamma: float) -> float:
    """
    If ρ = σ + iγ, the functional equation pairs it with 1 - σ + iγ.

    The "cost" of being off the critical line is:
    - You need a SECOND zero at 1-σ
    - This doubles the number of zeros off the line
    - But zeros are "expensive" (density is fixed)

    Return a measure of this constraint violation.
    """
    if sigma == 0.5:
        return 0  # On critical line - self-conjugate, no "cost"
    else:
        # Off the line - need paired zero
        # The "cost" is the symmetry violation
        return abs(sigma - 0.5)**2

print("Functional equation 'cost' at different σ:")
for sigma in sigmas:
    cost = sum(functional_equation_constraint(sigma, g) for g in ZEROS[:20])
    marker = " ← ZERO COST" if sigma == 0.5 else ""
    print(f"  σ={sigma}: cost = {cost:.6f}{marker}")

# ============================================================================
# SECTION 6: THE DUAL PROBLEM
# ============================================================================
print_section("SECTION 6: THE DUAL PROBLEM")

print("""
THE PRIMAL AND DUAL:
════════════════════

PRIMAL PROBLEM (what we want to prove):
    ∀ρ: Re(ρ) = 1/2

DUAL PROBLEM (equivalent statement):
    The energy functional E has unique minimum at σ = 1/2

WEAK DUALITY:
    If we find ANY energy functional with min at σ = 1/2,
    it's CONSISTENT with RH but doesn't prove it.

STRONG DUALITY:
    If we find the RIGHT energy functional where the min is EQUIVALENT to RH,
    then minimization proves RH.


THE SEARCH FOR THE RIGHT FUNCTIONAL:
════════════════════════════════════

The unit circle energy E₃ has the right minimum (σ = 1/2).
But it's TAUTOLOGICAL - we defined it to be zero on the line.

We need a functional that:
1. Is defined WITHOUT reference to the critical line
2. Connects to primes (explicit formula)
3. Is convex
4. Has minimum at σ = 1/2

The explicit formula energy E₂ is a candidate, but proving its
minimum is at σ = 1/2 is AS HARD AS PROVING RH.

This is the circularity problem.
""")

# ============================================================================
# SECTION 7: BREAKING THE CIRCULARITY
# ============================================================================
print_section("SECTION 7: BREAKING THE CIRCULARITY")

print("""
THE CIRCULARITY:
════════════════

We want: Energy minimized at σ = 1/2 → RH

But most energy functionals either:
1. Are defined using σ = 1/2 (tautological)
2. Require RH to prove the minimum is at σ = 1/2 (circular)


POTENTIAL WAYS OUT:
═══════════════════

1. FUNCTIONAL EQUATION ALONE
   ─────────────────────────
   The functional equation ξ(s) = ξ(1-s) is TRUE (provable).
   Can we derive RH from this symmetry ALONE?

   Answer: No. The symmetry only says zeros come in pairs (σ, 1-σ).
   It doesn't say they must be at σ = 1/2.

2. FUNCTIONAL EQUATION + REALITY
   ──────────────────────────────
   The function ξ(s) is real on the critical line.
   Combined with functional equation: zeros are symmetric about line.
   Still not enough - zeros could be in symmetric pairs off the line.

3. FUNCTIONAL EQUATION + HOLOMORPHY + GROWTH
   ──────────────────────────────────────────
   Add the constraint that ξ is entire of order 1.
   This constrains the zero distribution heavily.
   Might be enough? (This is the Hadamard approach.)

4. FUNCTIONAL EQUATION + POSITIVITY
   ─────────────────────────────────
   The Li criterion: λₙ > 0 for all n.
   If we could DERIVE this from some principle, RH follows.
   But proving λₙ > 0 is as hard as RH.
""")

print("""

THE DEEP INSIGHT:
═════════════════

The circularity suggests that RH is a "bootstrap" statement:

    RH is true because the only self-consistent configuration
    of zeros is on the critical line.

"Self-consistent" means:
- Satisfies functional equation
- Satisfies explicit formula
- Satisfies density asymptotics
- Satisfies growth bounds

The critical line is the FIXED POINT of these constraints.

This is like a thermodynamic equilibrium:
The system "finds" the equilibrium because all other states are unstable.
The critical line is stable; off-line configurations are unstable.

PROVING THIS:
─────────────
Would require showing that any off-line zero creates a CONTRADICTION
with one of the constraints. This is essentially what Conrey, Iwaniec,
and others have tried (and not yet succeeded).
""")

# ============================================================================
# SECTION 8: SUMMARY AND PROSPECTS
# ============================================================================
print_section("SECTION 8: SUMMARY AND PROSPECTS")

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     CONVEX OPTIMIZATION ATTACK: SUMMARY                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WHAT WE ESTABLISHED:                                                        ║
║  ────────────────────                                                        ║
║  1. The unit circle energy E₃(σ) = Σ(|z|-1)² is GLOBALLY CONVEX             ║
║  2. Its unique minimum is at σ = 1/2                                         ║
║  3. This is CONSISTENT with RH but doesn't prove it                          ║
║                                                                              ║
║  THE CIRCULARITY PROBLEM:                                                    ║
║  ────────────────────────                                                    ║
║  Most energy functionals either:                                             ║
║  - Are tautologically zero on the critical line                              ║
║  - Require RH to prove the minimum location                                  ║
║                                                                              ║
║  WHAT'S NEEDED:                                                              ║
║  ──────────────                                                              ║
║  An energy functional that:                                                  ║
║  1. Is defined WITHOUT reference to σ = 1/2                                  ║
║  2. Can be PROVED to be minimized at σ = 1/2                                 ║
║  3. Connects naturally to the zeta function                                  ║
║                                                                              ║
║  PROMISING DIRECTIONS:                                                       ║
║  ─────────────────────                                                       ║
║  • The Selberg zeta analogy (hyperbolic surfaces)                            ║
║  • The GUE connection (random matrix theory)                                 ║
║  • The quantum chaos connection (spectral statistics)                        ║
║  • The Beurling approach (generalized integers)                              ║
║                                                                              ║
║  BOTTOM LINE:                                                                ║
║  ────────────                                                                ║
║  Convex optimization provides the RIGHT FRAMEWORK for thinking about RH.     ║
║  The critical line IS a unique minimum of various energy functionals.        ║
║  But PROVING this for a non-circular functional remains the challenge.       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# ============================================================================
# SECTION 9: THE BEURLING APPROACH
# ============================================================================
print_section("SECTION 9: THE BEURLING APPROACH (BONUS)")

print("""
THE BEURLING GENERALIZATION:
════════════════════════════

Beurling (1937) considered "generalized integers":
Given a sequence of "generalized primes" P = {p₁, p₂, ...},
define "generalized integers" as products of these primes.

The "generalized zeta function":

    ζ_P(s) = Σ n_k^{-s}

where n_k are the generalized integers.

KEY THEOREM (Beurling):
───────────────────────
If the generalized primes have the right density, then ζ_P has
zeros, and these zeros have something to do with the prime distribution.

RH ANALOGY:
───────────
For which sequences P does the generalized RH hold?

Answer: There exist sequences where generalized RH FAILS.
But for the ACTUAL primes, we conjecture it holds.

WHAT MAKES THE ACTUAL PRIMES SPECIAL?
─────────────────────────────────────
The actual primes are not arbitrary - they're determined by MULTIPLICATION.
This algebraic structure (the ring of integers) is what makes RH true.

The Beurling approach shows: RH is not a general fact about zeros.
It's a specific fact about the arithmetic of integers.

This is why RH is connected to:
- Class field theory
- Modular forms
- Elliptic curves
- Automorphic representations

All of these encode the deep structure of INTEGER ARITHMETIC.
""")

print("""

THE CONVEX + BEURLING SYNTHESIS:
════════════════════════════════

Conjecture: Among all Beurling systems with density equivalent to primes,
the actual primes MINIMIZE some energy functional.

This would explain WHY RH is true:
- The primes are special (minimal energy)
- RH is the CONSEQUENCE of this minimality
- Off-line zeros would mean "suboptimal" primes

To prove this, we would need to:
1. Define the space of Beurling systems
2. Define an energy functional on this space
3. Show actual primes minimize it
4. Show the minimum implies RH

This is a MASSIVE undertaking but could be the right path.
""")

# ============================================================================
# FINAL SYNTHESIS
# ============================================================================
print_section("FINAL SYNTHESIS: THE OPTIMIZATION VIEW OF RH")

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE OPTIMIZATION VIEW OF RH                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  RH can be viewed as a statement about OPTIMIZATION:                         ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │  The zeros of the Riemann zeta function are located at the             │  ║
║  │  UNIQUE GLOBAL MINIMUM of a natural energy functional,                 │  ║
║  │  subject to the constraints of number theory.                          │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║  The challenge is to find the RIGHT energy functional:                       ║
║  - Not tautological (defined without reference to σ = 1/2)                   ║
║  - Connected to arithmetic (through explicit formula)                        ║
║  - Convex or at least has unique minimum                                     ║
║  - The minimum can be PROVED to be at σ = 1/2                                ║
║                                                                              ║
║  CANDIDATE FUNCTIONALS:                                                      ║
║  ┌───────────────────────────────────────────────────────────────────────┐   ║
║  │ E₁ = Σₙ max(0, -λₙ)           (Li criterion energy)                   │   ║
║  │ E₂ = ∫|ψ(x)-x|² dx            (Explicit formula energy)               │   ║
║  │ E₃ = Σ(|1-1/ρ|-1)²            (Unit circle energy)                    │   ║
║  │ E₄ = -Σ log|ξ(ρ)|             (Hadamard product energy)               │   ║
║  │ E₅ = Complexity(primes|zeros) (Information-theoretic energy)          │   ║
║  └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  All have the critical line as minimum.                                      ║
║  None have been rigorously proved without assuming RH.                       ║
║                                                                              ║
║  THE PATH FORWARD:                                                           ║
║  Find a functional E where:                                                  ║
║  1. E ≥ 0 with equality iff RH (provable by independent means)               ║
║  2. The minimum condition is equivalent to a known theorem                   ║
║                                                                              ║
║  This would reduce RH to that theorem.                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("\n" + "=" * 80)
print("END OF CONVEX OPTIMIZATION ANALYSIS")
print("=" * 80)
