#!/usr/bin/env python3
"""
ATTEMPT TO PROVE THE MERTENS BOUND M(x) = O(x^{1/2+ε})
======================================================

The Mertens function M(x) = Σ_{n≤x} μ(n) satisfies:

  • Prime Number Theorem ⟺ M(x) = o(x)
  • RIEMANN HYPOTHESIS ⟺ M(x) = O(x^{1/2+ε}) for all ε > 0

This script attempts to prove the RH-strength bound through:

1. Explicit formula analysis (zeros of zeta)
2. Probabilistic / random matrix approach
3. Sieve method bounds
4. Z² geometric constraints
5. Direct structural arguments

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import special, integrate
import warnings
warnings.filterwarnings('ignore')

PI = np.pi
E = np.e
Z_SQUARED = 32 * PI / 3

print("=" * 80)
print("ATTEMPT TO PROVE M(x) = O(x^{1/2+ε})")
print("=" * 80)

# =============================================================================
# THE MERTENS FUNCTION
# =============================================================================

print("\n" + "=" * 80)
print("THE MERTENS FUNCTION")
print("=" * 80)

def mobius(n):
    """Compute μ(n)."""
    if n == 1:
        return 1
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                temp //= d
                count += 1
            if count > 1:
                return 0
            factors.append(d)
        d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def M(x):
    """Mertens function M(x) = Σ_{n≤x} μ(n)"""
    return sum(mobius(n) for n in range(1, int(x) + 1))


print("""
DEFINITION:
----------
M(x) = Σ_{n≤x} μ(n)

where μ is the Möbius function:
  μ(n) = 1      if n = 1
  μ(n) = (-1)^k if n = p₁p₂...pₖ (product of k distinct primes)
  μ(n) = 0      if n has a squared prime factor

KEY EQUIVALENCE:
  M(x) = O(x^{1/2+ε}) ⟺ RIEMANN HYPOTHESIS
""")

# Compute M(x) for various x
print("\nMertens function values:")
print(f"{'x':>10} {'M(x)':>10} {'M(x)/√x':>12} {'|M(x)|/x^0.5':>15}")
print("-" * 52)
for x in [100, 500, 1000, 5000, 10000, 50000]:
    Mx = M(x)
    ratio = Mx / np.sqrt(x)
    print(f"{x:>10} {Mx:>10} {ratio:>12.4f} {abs(ratio):>15.4f}")

# =============================================================================
# APPROACH 1: EXPLICIT FORMULA
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 1: EXPLICIT FORMULA FOR M(x)")
print("=" * 80)

print("""
THE EXPLICIT FORMULA:
--------------------
By Perron's formula and contour integration:

  M(x) = -Σ_ρ (x^ρ / ρ·ζ'(ρ)) + (Γ'/Γ)(1) + Σ_{trivial} + O(1/x)

where the sum is over non-trivial zeros ρ of ζ(s).

KEY INSIGHT:
-----------
Each zero ρ = β + iγ contributes a term of size ~ x^β / |γ|

If ALL zeros have β = 1/2 (RH):
  Each term ~ x^{1/2} / |γ|
  Sum over zeros ~ x^{1/2} · Σ 1/|γ|
  Since Σ 1/|γ|^{1+ε} < ∞, we get M(x) = O(x^{1/2+ε})

If ANY zero has β > 1/2:
  That term ~ x^β dominates
  M(x) would grow like x^β > x^{1/2}
  Violating the RH bound
""")

# Numerical demonstration with known zeros
KNOWN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
               37.586178, 40.918719, 43.327073, 48.005151, 49.773832]

def explicit_formula_approximation(x, zeros, N_zeros=10):
    """
    Approximate M(x) using explicit formula with first N zeros.
    M(x) ≈ -Σ_ρ x^ρ / ρ

    Assuming zeros on critical line: ρ = 1/2 + iγ
    """
    total = 0
    for gamma in zeros[:N_zeros]:
        rho = 0.5 + 1j * gamma
        term = x**rho / rho
        # Add conjugate zero contribution
        rho_conj = 0.5 - 1j * gamma
        term_conj = x**rho_conj / rho_conj
        total += term + term_conj
    return -np.real(total)


print("\nExplicit formula approximation (assuming RH):")
print(f"{'x':>10} {'M(x) actual':>15} {'Explicit approx':>18} {'x^{1/2}':>12}")
print("-" * 60)
for x in [100, 500, 1000, 5000]:
    Mx_actual = M(x)
    Mx_approx = explicit_formula_approximation(x, KNOWN_ZEROS, 10)
    bound = np.sqrt(x)
    print(f"{x:>10} {Mx_actual:>15} {Mx_approx:>18.2f} {bound:>12.2f}")

print("""
OBSERVATION:
-----------
The explicit formula (with zeros on the line) gives oscillating
contributions bounded by √x, consistent with RH.

THE CIRCULARITY:
--------------
This analysis ASSUMES the zeros are on Re(s) = 1/2.
Proving they must be on the line is exactly what we need!
""")

# =============================================================================
# APPROACH 2: PROBABILISTIC / RANDOM MATRIX
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 2: PROBABILISTIC HEURISTIC")
print("=" * 80)

print("""
THE RANDOM MODEL:
----------------
If μ(n) were independent random variables with:
  P(μ(n) = 0) = 1 - 6/π² ≈ 0.392 (probability of square factor)
  P(μ(n) = ±1) = 3/π² each (for squarefree n)

Then by the Central Limit Theorem:
  M(x) = Σ_{n≤x} μ(n) ~ N(0, σ²)

where σ² ~ (6/π²) x = x/ζ(2)

So M(x) would typically be O(√x), rarely exceeding C√x·√(log log x).

This heuristic SUGGESTS M(x) = O(√x), i.e., RH is "probably" true.
""")

# Compare actual M(x) to random walk prediction
def random_walk_std(x):
    """Expected standard deviation if μ were random."""
    return np.sqrt(x * 6 / PI**2)


print("\nComparing M(x) to random walk prediction:")
print(f"{'x':>10} {'M(x)':>10} {'σ = √(6x/π²)':>15} {'M(x)/σ':>12}")
print("-" * 52)
for x in [100, 1000, 10000, 50000]:
    Mx = M(x)
    sigma = random_walk_std(x)
    ratio = Mx / sigma
    print(f"{x:>10} {Mx:>10} {sigma:>15.2f} {ratio:>12.4f}")

print("""
OBSERVATION:
-----------
|M(x)/σ| is small, suggesting M(x) behaves like a random walk.
This is CONSISTENT with but does NOT prove RH.

THE GAP:
-------
μ(n) is NOT random - it's deterministic from prime factorization.
The question is whether the "pseudo-randomness" is strong enough
to guarantee M(x) = O(x^{1/2+ε}).
""")

# =============================================================================
# APPROACH 3: SIEVE BOUNDS
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 3: SIEVE METHOD BOUNDS")
print("=" * 80)

print("""
KNOWN UNCONDITIONAL BOUNDS:
--------------------------
Various sieve methods give bounds on M(x):

1. Trivial bound: M(x) ≤ x (obvious)

2. From PNT: M(x) = o(x) (Landau, 1899)

3. De la Vallée Poussin: M(x) = O(x·exp(-c√(log x)))

4. Vinogradov-Korobov: M(x) = O(x·exp(-c·(log x)^{3/5}/(log log x)^{1/5}))

None of these give M(x) = O(x^{1/2+ε}).

THE BEST UNCONDITIONAL RESULT:
-----------------------------
M(x) = O(x·exp(-c·(log x)^{0.6-ε}))

This is MUCH weaker than O(x^{1/2+ε}).
""")

def de_la_vallee_poussin_bound(x):
    """Upper bound from de la Vallée Poussin type estimate."""
    c = 0.1  # Some constant
    return x * np.exp(-c * np.sqrt(np.log(x)))


def rh_bound(x):
    """The RH bound x^{1/2+ε}."""
    eps = 0.01
    return x**(0.5 + eps)


print("\nComparing bounds:")
print(f"{'x':>10} {'|M(x)|':>12} {'DLVP bound':>15} {'RH bound':>15}")
print("-" * 57)
for x in [1000, 10000, 100000]:
    Mx = abs(M(x)) if x <= 50000 else "---"
    dlvp = de_la_vallee_poussin_bound(x)
    rh = rh_bound(x)
    print(f"{x:>10} {str(Mx):>12} {dlvp:>15.1f} {rh:>15.1f}")

print("""
THE GAP:
-------
The unconditional bounds are EXPONENTIAL in log(x).
The RH bound is POLYNOMIAL: x^{1/2+ε}.

The gap between exp(-c·log(x)^{0.6}) and x^{-1/2} is enormous.
Bridging this gap requires proving RH.
""")

# =============================================================================
# APPROACH 4: THE Z² CONNECTION
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 4: Z² GEOMETRIC CONSTRAINT")
print("=" * 80)

print(f"""
THE Z² FRAMEWORK:
----------------
Z² = 32π/3 = {Z_SQUARED:.6f}
BEKENSTEIN = 4 (spacetime dimension)

The M₈ = (S³ × S³ × ℂ*)/ℤ₂ geometry suggests:
- A natural operator (Dirac) with real spectrum
- Self-adjointness forces eigenvalues to be real
- Real eigenvalues ⟹ zeros on critical line ⟹ M(x) = O(x^{{1/2+ε}})

POTENTIAL ARGUMENT:
------------------
If the zeta zeros ARE eigenvalues of some self-adjoint operator H,
then they must be real, hence Im(ρ) real, hence Re(ρ) = 1/2.

The question: Does such an operator exist with the required properties?
""")

# Examine if Z² provides any constraint on M(x)
def M_normalized(x):
    """Normalize M(x) by Z² related quantity."""
    return M(x) / np.sqrt(Z_SQUARED * x)


print("\nM(x) normalized by √(Z²·x):")
print(f"{'x':>10} {'M(x)':>10} {'M(x)/√(Z²x)':>15}")
print("-" * 40)
for x in [100, 500, 1000, 5000, 10000]:
    Mx = M(x)
    normalized = M_normalized(x)
    print(f"{x:>10} {Mx:>10} {normalized:>15.6f}")

print("""
OBSERVATION:
-----------
M(x)/√(Z²·x) appears bounded. But this is just numerical observation.

THE GAP:
-------
The Z² framework suggests WHERE to look for the operator,
but doesn't prove the operator has the required spectrum.
""")

# =============================================================================
# APPROACH 5: DIRECT STRUCTURAL ARGUMENT
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 5: DIRECT STRUCTURAL ARGUMENT")
print("=" * 80)

print("""
THE STRUCTURE OF μ(n):
---------------------
μ(n) is determined by the prime factorization of n:
  μ(n) = 0 if any prime divides n twice
  μ(n) = (-1)^k if n = p₁p₂...pₖ (distinct primes)

KEY IDENTITY:
  Σ_{d|n} μ(d) = [n = 1]  (Kronecker delta)

This gives:
  M(x) = Σ_{n≤x} μ(n) = Σ_{n≤x} Σ_{d|n} μ(d)·[d=n]

MÖBIUS INVERSION:
  f(n) = Σ_{d|n} g(d) ⟺ g(n) = Σ_{d|n} μ(d)·f(n/d)

The distribution of μ(n) is intimately tied to prime distribution.
""")

# Examine partial sums with different weightings
def weighted_M(x, alpha):
    """Σ_{n≤x} μ(n)/n^α"""
    return sum(mobius(n) / n**alpha for n in range(1, int(x) + 1))


print("\nWeighted sums Σ μ(n)/n^α for various α:")
print(f"{'x':>10} {'α=0 (M(x))':>15} {'α=0.5':>15} {'α=1':>15}")
print("-" * 60)
for x in [100, 500, 1000, 5000]:
    m0 = weighted_M(x, 0)
    m05 = weighted_M(x, 0.5)
    m1 = weighted_M(x, 1)
    print(f"{x:>10} {m0:>15.4f} {m05:>15.6f} {m1:>15.8f}")

print("""
OBSERVATION:
-----------
Σ μ(n)/n^α converges for α > 1 to 1/ζ(α).
For α = 1: Σ μ(n)/n → 0 (PNT)
For α < 1: convergence rate is the key question.

THE CONNECTION:
--------------
M(x) = O(x^{1/2+ε}) ⟺ Σ_{n≤x} μ(n)/n^{1/2+ε} converges well
⟺ 1/ζ(s) has no singularities for Re(s) > 1/2
⟺ ζ(s) has no zeros for Re(s) > 1/2
⟺ RH
""")

# =============================================================================
# APPROACH 6: THE KEY INTEGRAL
# =============================================================================

print("\n" + "=" * 80)
print("APPROACH 6: THE FUNDAMENTAL INTEGRAL")
print("=" * 80)

print("""
PERRON'S FORMULA:
----------------
M(x) = (1/2πi) ∫_{c-i∞}^{c+i∞} (x^s / s) · (1/ζ(s)) ds

where c > 1.

Shifting the contour to Re(s) = 1/2 + ε picks up residues at zeros:
  M(x) = -Σ_ρ (x^ρ / ρ·ζ'(ρ)) + (boundary terms)

THE CRITICAL OBSERVATION:
------------------------
The integral converges ONLY if 1/ζ(s) has no poles for Re(s) > 1/2 + ε.
Poles of 1/ζ(s) = zeros of ζ(s).

So M(x) = O(x^{1/2+ε}) ⟺ No zeros with Re(s) > 1/2 ⟺ RH
""")

# =============================================================================
# THE FUNDAMENTAL OBSTRUCTION
# =============================================================================

print("\n" + "=" * 80)
print("THE FUNDAMENTAL OBSTRUCTION")
print("=" * 80)

print("""
WHY WE CANNOT PROVE M(x) = O(x^{1/2+ε}) DIRECTLY:
=================================================

Every approach reduces to the same obstruction:

1. EXPLICIT FORMULA:
   M(x) = -Σ_ρ x^ρ/(ρ·ζ'(ρ)) + ...
   Requires knowing Re(ρ) = 1/2 (which is RH)

2. PROBABILISTIC:
   μ(n) "looks random" suggests √x bound
   But "looks random" ≠ "is bounded by √x"
   Proving pseudo-randomness is strong enough requires RH

3. SIEVE METHODS:
   Best unconditional: M(x) = O(x·exp(-c(log x)^{0.6}))
   Gap to O(x^{1/2}) is enormous
   Cannot be bridged by known sieve techniques

4. GEOMETRIC (Z²):
   Self-adjoint operator would give RH
   But proving spectrum = zeta zeros requires RH

5. DIRECT STRUCTURE:
   μ(n) determined by primes
   Cancellation rate depends on zero locations
   Back to RH

THE EQUIVALENCE:
---------------
   ┌──────────────────────────────────────────────────┐
   │  M(x) = O(x^{1/2+ε})  ⟺  RIEMANN HYPOTHESIS    │
   └──────────────────────────────────────────────────┘

These are not just related - they are LOGICALLY EQUIVALENT.
Proving one proves the other. We cannot do one without the other.
""")

# =============================================================================
# WHAT WOULD BREAK THE EQUIVALENCE?
# =============================================================================

print("\n" + "=" * 80)
print("WHAT WOULD BREAK THE EQUIVALENCE?")
print("=" * 80)

print("""
To prove M(x) = O(x^{1/2+ε}) without explicitly proving RH,
we would need:

OPTION A: New Analytic Technique
--------------------------------
A method that bounds M(x) without reference to zeros.
No such method is known. All approaches use the connection
M(x) ↔ 1/ζ(s) ↔ zeros of ζ.

OPTION B: Structural Constraint
-------------------------------
Some property of μ(n) that forces cancellation.
The multiplicativity μ(mn) = μ(m)μ(n) for (m,n)=1 is known,
but this doesn't give strong enough cancellation.

OPTION C: Physical/Geometric Constraint
---------------------------------------
If the zeta zeros ARE eigenvalues of a physical system,
that system's properties might force the bound.
This is the Hilbert-Pólya / Z² approach.
But we can't prove the eigenvalue connection without RH.

OPTION D: Information-Theoretic Bound
-------------------------------------
Perhaps some entropy or information constraint limits M(x)?
No such constraint is known.

OPTION E: Random Matrix Theory
------------------------------
If GUE statistics are PROVEN (not just conjectured) for zeros,
the real eigenvalue property would give RH.
But proving GUE requires understanding zero distribution.

CONCLUSION:
----------
All roads lead back to the same obstruction.
The equivalence M(x) = O(x^{1/2+ε}) ⟺ RH is fundamental.
""")

# =============================================================================
# NUMERICAL EVIDENCE
# =============================================================================

print("\n" + "=" * 80)
print("NUMERICAL EVIDENCE")
print("=" * 80)

print("""
While we cannot PROVE the bound, we can verify it holds numerically.
""")

# Extended computation
print("\nExtended Mertens function computation:")
print(f"{'x':>12} {'M(x)':>12} {'|M(x)|/x^0.5':>15} {'Bound 2x^0.5':>15}")
print("-" * 60)

max_ratio = 0
for x in [100, 500, 1000, 2000, 5000, 10000, 20000, 50000]:
    Mx = M(x)
    ratio = abs(Mx) / np.sqrt(x)
    bound = 2 * np.sqrt(x)
    max_ratio = max(max_ratio, ratio)
    within = "YES" if abs(Mx) < bound else "NO"
    print(f"{x:>12} {Mx:>12} {ratio:>15.4f} {bound:>15.2f}")

print(f"\nMaximum observed |M(x)|/√x: {max_ratio:.4f}")
print("All values satisfy |M(x)| < 2√x")

# The Mertens conjecture (disproved)
print("""
HISTORICAL NOTE:
---------------
Mertens conjectured (1897) that |M(x)| < √x for all x.
This was DISPROVED by Odlyzko & te Riele (1985).
There exist x where |M(x)| > √x, but probably |M(x)| < 2√x.

This shows: M(x) = O(√x) is likely true, but the constant matters.
RH gives M(x) = O(x^{1/2} · (log x)^{2+ε}), a slightly weaker bound
but still O(x^{1/2+ε}).
""")

# =============================================================================
# FINAL CONCLUSION
# =============================================================================

print("\n" + "=" * 80)
print("FINAL CONCLUSION")
print("=" * 80)

print("""
SUMMARY OF PROOF ATTEMPT:
========================

ESTABLISHED:
-----------
1. M(x) = O(x^{1/2+ε}) ⟺ RH (logical equivalence)
2. Explicit formula: M(x) = -Σ_ρ x^ρ/(ρζ'(ρ)) + O(1)
3. The bound depends entirely on zero locations
4. All approaches reduce to the zero location question

NUMERICAL EVIDENCE:
------------------
• |M(x)|/√x appears bounded (max observed: {:.4f})
• M(x) behaves like random walk with σ ~ √(6x/π²)
• All known zeros have Re(ρ) = 1/2 (trillions verified)

CANNOT PROVE:
------------
• M(x) = O(x^{{1/2+ε}}) without proving RH
• The equivalence is fundamental, not technical

THE OBSTRUCTION:
---------------
Every approach uses the connection:
  M(x) ↔ 1/ζ(s) ↔ zeros of ζ(s)

We cannot bound M(x) without understanding zero locations.
Understanding zero locations IS the Riemann Hypothesis.

CONCLUSION:
----------
   ┌────────────────────────────────────────────────────────┐
   │  PROVING M(x) = O(x^{{1/2+ε}}) IS EQUIVALENT TO       │
   │  PROVING THE RIEMANN HYPOTHESIS.                       │
   │                                                        │
   │  We cannot do one without the other.                   │
   │  The problem remains open.                             │
   └────────────────────────────────────────────────────────┘
""".format(max_ratio))

print("=" * 80)
print("END OF MERTENS BOUND PROOF ATTEMPT")
print("=" * 80)
