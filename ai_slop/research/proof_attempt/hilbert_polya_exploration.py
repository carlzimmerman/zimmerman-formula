"""
HILBERT-PÓLYA OPERATOR EXPLORATION
===================================

The Hilbert-Pólya conjecture (1914): There exists a self-adjoint operator H
whose eigenvalues are the imaginary parts of ζ zeros.

If such H exists:
  • Self-adjoint ⟹ real eigenvalues
  • Eigenvalues = {γ : ζ(1/2 + iγ) = 0}
  • Real γ ⟹ zeros on critical line ⟹ RH

This is the most direct path to proving RH.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import factorint, primerange, zeta, I, pi, exp, log, sqrt
from sympy import symbols, Sum, oo, factorial, gamma, Float, N
import scipy.linalg as la
from collections import defaultdict

print("=" * 80)
print("HILBERT-PÓLYA OPERATOR EXPLORATION")
print("=" * 80)

# =============================================================================
# PART 1: THE BASIC IDEA
# =============================================================================

print("""
================================================================================
PART 1: THE HILBERT-PÓLYA PROGRAM
================================================================================

THE GOAL:
=========
Find a self-adjoint operator H on a Hilbert space such that:
  Spec(H) = {γ : ζ(1/2 + iγ) = 0}

WHY THIS PROVES RH:
===================
Self-adjoint operators have REAL spectra.
If Spec(H) = {γ} and γ are real, then ζ zeros have form 1/2 + iγ with real γ.
This means Re(ρ) = 1/2 for all zeros ⟹ RH.

PREVIOUS ATTEMPTS:
==================
1. Berry-Keating (1999): H = (xp + px)/2
   Insight: Classical xp has orbits related to counting
   Problem: Rigorous definition fails

2. Connes (1996+): Noncommutative geometry on adeles
   Insight: Trace formula connects primes to zeros
   Problem: "Absorption spectrum" not full spectrum

3. Bender-Brody-Müller (2017): PT-symmetric approach
   Insight: Non-Hermitian operators can have real spectra
   Problem: Controversial, possibly flawed

OUR APPROACH:
=============
Use the generating function connection to construct operators.
See if any natural construction yields ζ zeros.
""")

# =============================================================================
# PART 2: THE EXPLICIT FORMULA CONNECTION
# =============================================================================

print("""
================================================================================
PART 2: THE EXPLICIT FORMULA
================================================================================

THE EXPLICIT FORMULA:
=====================
ψ(x) = Σ_{p^k ≤ x} log(p) = x - Σ_ρ x^ρ/ρ - log(2π) - (1/2)log(1-x^{-2})

Where the sum is over all nontrivial zeros ρ of ζ(s).

SPECTRAL INTERPRETATION:
========================
This is like a TRACE FORMULA:
  • Left side: sum over "primes" (geometric data)
  • Right side: sum over "zeros" (spectral data)

Compare to Selberg trace formula for hyperbolic surfaces:
  Σ (lengths of closed geodesics) ↔ Σ (Laplacian eigenvalues)

THE QUESTION:
=============
What is the "surface" or "space" whose trace formula is the explicit formula?

This is Connes' program: The space is a "noncommutative space" related to adeles.
""")

# =============================================================================
# PART 3: CONSTRUCTING OPERATORS FROM OUR FRAMEWORK
# =============================================================================

print("""
================================================================================
PART 3: OPERATORS FROM GENERATING FUNCTIONS
================================================================================

OUR KEY RELATION:
=================
G̃(-1, s) = 1/(s·ζ(s))

The poles of this are at s = 0 and s = ρ (ζ zeros).

RESOLVENT INTERPRETATION:
=========================
If H is an operator, its resolvent is R(z) = (z - H)^{-1}.
The poles of R(z) are the eigenvalues of H.

So if G̃(-1, s) were a resolvent, its poles would be eigenvalues!

PROBLEM:
========
G̃(-1, s) = 1/(s·ζ(s)) has poles at ρ = 1/2 ± iγ (COMPLEX).
A self-adjoint operator has REAL eigenvalues.

RESOLUTION:
===========
We want the IMAGINARY parts γ as eigenvalues.
Need to "extract" γ from ρ = 1/2 + iγ.

This requires a more sophisticated construction.
""")

# =============================================================================
# PART 4: THE ω-OPERATOR ON SQUAREFREE NUMBERS
# =============================================================================

print("""
================================================================================
PART 4: THE ω-OPERATOR ON SQUAREFREE NUMBERS
================================================================================

HILBERT SPACE:
==============
ℓ²(ℕ_sf) = {(a_n) : Σ_{n sqfree} |a_n|² < ∞}

Basis: |n⟩ for squarefree n, with ⟨m|n⟩ = δ_{mn}

NATURAL OPERATORS:
==================
1. H_ω: H_ω|n⟩ = ω(n)|n⟩  (number of prime factors)
2. H_log: H_log|n⟩ = log(n)|n⟩  (log of n)
3. M_μ: M_μ|n⟩ = μ(n)|n⟩  (Möbius value, ±1)
4. T_k: T_k|n⟩ = |kn⟩ if kn sqfree, 0 otherwise (shift)

Let's examine their spectra and connections to ζ.
""")

# Setup
MAX_N = 10000
primes = list(primerange(2, MAX_N))

def is_squarefree(n):
    if n == 1:
        return True
    factors = factorint(n)
    return all(e == 1 for e in factors.values())

def omega(n):
    if n == 1:
        return 0
    return len(factorint(n))

def mobius(n):
    if n == 1:
        return 1
    factors = factorint(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return (-1) ** len(factors)

# Get squarefree numbers up to N
sqfree = [n for n in range(1, MAX_N + 1) if is_squarefree(n)]
print(f"\nSquarefree numbers up to {MAX_N}: {len(sqfree)}")

# =============================================================================
# PART 5: MATRIX REPRESENTATION OF OPERATORS
# =============================================================================

print("""
================================================================================
PART 5: MATRIX REPRESENTATIONS (FINITE TRUNCATION)
================================================================================

For numerical exploration, we truncate to squarefree n ≤ N.
This gives finite matrices we can analyze.
""")

def build_H_omega(sqfree_list):
    """Build diagonal matrix H_ω."""
    N = len(sqfree_list)
    H = np.diag([omega(n) for n in sqfree_list])
    return H

def build_H_log(sqfree_list):
    """Build diagonal matrix H_log."""
    N = len(sqfree_list)
    H = np.diag([np.log(n) for n in sqfree_list])
    return H

def build_M_mu(sqfree_list):
    """Build diagonal matrix M_μ."""
    N = len(sqfree_list)
    M = np.diag([mobius(n) for n in sqfree_list])
    return M

def build_divisor_matrix(sqfree_list):
    """Build matrix D where D_{ij} = 1 if sqfree_list[j] | sqfree_list[i]."""
    N = len(sqfree_list)
    D = np.zeros((N, N))
    idx = {n: i for i, n in enumerate(sqfree_list)}
    for i, n in enumerate(sqfree_list):
        for d in range(1, n + 1):
            if n % d == 0 and d in idx:
                D[i, idx[d]] = 1
    return D

# Build matrices for small truncation
N_trunc = 500
sqfree_small = sqfree[:N_trunc]

print(f"\nBuilding matrices for {N_trunc} squarefree numbers...")

H_omega = build_H_omega(sqfree_small)
H_log = build_H_log(sqfree_small)
M_mu = build_M_mu(sqfree_small)
D = build_divisor_matrix(sqfree_small)

print(f"  H_ω: {H_omega.shape}, diagonal, eigenvalues = {set(np.diag(H_omega).astype(int))}")
print(f"  H_log: {H_log.shape}, diagonal")
print(f"  M_μ: {M_mu.shape}, diagonal, eigenvalues = {set(np.diag(M_mu).astype(int))}")
print(f"  D: {D.shape}, divisibility matrix")

# =============================================================================
# PART 6: THE MÖBIUS MATRIX
# =============================================================================

print("""
================================================================================
PART 6: THE MÖBIUS MATRIX
================================================================================

The Möbius function arises from matrix inversion:
  D · D_μ = I  (where D_μ involves μ)

Let's construct the Möbius matrix explicitly.
""")

def build_mobius_matrix(sqfree_list):
    """Build matrix M where M_{ij} = μ(sqfree_list[i]/sqfree_list[j]) if j|i."""
    N = len(sqfree_list)
    M = np.zeros((N, N))
    idx = {n: i for i, n in enumerate(sqfree_list)}
    for i, n in enumerate(sqfree_list):
        for d in range(1, n + 1):
            if n % d == 0 and d in idx:
                M[i, idx[d]] = mobius(n // d)
    return M

Mob = build_mobius_matrix(sqfree_small)

# Verify: D · Mob should be close to identity
product = D @ Mob
identity_error = np.max(np.abs(product - np.eye(N_trunc)))
print(f"\nMöbius matrix verification:")
print(f"  ||D · Mob - I||_max = {identity_error:.2e}")

# Eigenvalues of Mob
mob_eigenvalues = la.eigvals(Mob)
print(f"\nMöbius matrix eigenvalues (sample):")
print(f"  First 10: {mob_eigenvalues[:10]}")
print(f"  All equal to 1? {np.allclose(mob_eigenvalues, 1)}")

# =============================================================================
# PART 7: TRYING TO FIND ζ ZEROS IN SPECTRA
# =============================================================================

print("""
================================================================================
PART 7: SEARCHING FOR ζ ZEROS IN OPERATOR SPECTRA
================================================================================

The first few ζ zeros (imaginary parts):
  γ₁ ≈ 14.1347
  γ₂ ≈ 21.0220
  γ₃ ≈ 25.0109
  γ₄ ≈ 30.4249
  γ₅ ≈ 32.9351

Can we construct an operator whose spectrum contains these?
""")

zeta_zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271]

# Try various combinations
print("\nTrying various operator combinations...")

# Combination 1: H_log / something
# Idea: log(n) relates to "energy", maybe scaling gives zeros

# Combination 2: Something with M_μ
# The alternating signs of μ might create interesting structure

def try_combination(matrix, name):
    """Analyze eigenvalues of a matrix, looking for ζ zeros."""
    eigenvalues = la.eigvals(matrix)
    real_parts = eigenvalues.real
    imag_parts = eigenvalues.imag

    # Check if any eigenvalues are close to ζ zeros
    matches = []
    for gamma in zeta_zeros[:5]:
        closest = min(np.abs(real_parts - gamma))
        if closest < 1:
            matches.append((gamma, closest))

    print(f"\n{name}:")
    print(f"  Shape: {matrix.shape}")
    print(f"  Eigenvalue range (real): [{min(real_parts):.2f}, {max(real_parts):.2f}]")
    print(f"  Max |imag part|: {max(np.abs(imag_parts)):.4f}")
    if matches:
        print(f"  Matches to ζ zeros: {matches}")
    else:
        print(f"  No matches to first 5 ζ zeros")

# H_omega (trivial - just counts)
try_combination(H_omega, "H_ω")

# H_log (just log(n))
try_combination(H_log, "H_log")

# M_mu (just ±1)
try_combination(M_mu, "M_μ")

# D (divisibility)
try_combination(D, "D (divisibility)")

# D + D^T (symmetric version)
D_sym = (D + D.T) / 2
try_combination(D_sym, "D_symmetric")

# H_log @ M_mu (twisted)
H_twisted = H_log @ M_mu
try_combination(H_twisted, "H_log @ M_μ")

# exp(i * H_log) (unitary)
H_unitary = la.expm(1j * H_log)
try_combination(H_unitary, "exp(i·H_log)")

# =============================================================================
# PART 8: THE BERRY-KEATING APPROACH
# =============================================================================

print("""
================================================================================
PART 8: BERRY-KEATING APPROACH
================================================================================

Berry-Keating (1999) proposed: H = xp + px (symmetrized position × momentum)

CLASSICAL MECHANICS:
====================
Classical Hamiltonian H = xp has trajectories with H = constant.
On orbit with H = E: xp = E, so p = E/x.

The "action" around a periodic orbit relates to quantization:
  ∮ p dx = 2πℏ(n + 1/2)

QUANTUM VERSION:
================
In QM: [x, p] = iℏ
So xp ≠ px. The Hermitian combination is (xp + px)/2.

THE CONNECTION TO ζ:
====================
Berry-Keating showed (heuristically) that the spectrum of H = xp + px
on a suitable space should give the ζ zeros!

The key is BOUNDARY CONDITIONS:
  • Need to restrict to x > 0 (positive reals)
  • Need absorbing/reflecting boundary at x = 0
  • The specific choice determines the spectrum

PROBLEM:
========
Making this rigorous requires:
  1. Proper Hilbert space
  2. Domain of operator
  3. Self-adjoint extension

This has NOT been done rigorously.

Let's try a discrete approximation...
""")

def build_discrete_xp(N):
    """
    Build a discrete approximation to xp + px.
    On a grid x_j = j, the momentum operator p ~ i(d/dx) becomes a difference.
    """
    # Position operator: diagonal with x_j = j
    x = np.diag(np.arange(1, N + 1, dtype=float))

    # Momentum operator: i × (forward difference - backward difference)/2
    # p ≈ (i/2)(|j+1⟩⟨j| - |j-1⟩⟨j|)
    p = np.zeros((N, N), dtype=complex)
    for j in range(N):
        if j > 0:
            p[j-1, j] = -1j / 2
        if j < N - 1:
            p[j+1, j] = 1j / 2

    # xp + px
    H = x @ p + p @ x

    return H, x, p

N_grid = 200
H_xp, X, P = build_discrete_xp(N_grid)

print(f"\nDiscrete xp + px operator (grid size {N_grid}):")
print(f"  Is Hermitian? {np.allclose(H_xp, H_xp.conj().T)}")

# Eigenvalues
xp_eigenvalues = la.eigvalsh(H_xp)  # Use eigvalsh for Hermitian

print(f"  Eigenvalue range: [{min(xp_eigenvalues):.2f}, {max(xp_eigenvalues):.2f}]")
print(f"  First 10 positive eigenvalues: {sorted([e for e in xp_eigenvalues if e > 0])[:10]}")

# Check for ζ zeros
print(f"\n  Checking for ζ zeros in spectrum:")
for gamma in zeta_zeros[:5]:
    closest = min(np.abs(xp_eigenvalues - gamma))
    print(f"    γ = {gamma:.4f}: closest eigenvalue distance = {closest:.4f}")

# =============================================================================
# PART 9: MULTIPLICATIVE STRUCTURE OPERATOR
# =============================================================================

print("""
================================================================================
PART 9: MULTIPLICATIVE STRUCTURE OPERATOR
================================================================================

New idea: Use the multiplicative structure of squarefree numbers.

Define an operator that encodes how numbers multiply:
  T_{mult}|n⟩ = Σ_{d|n, d<n} |d⟩  (sum over proper divisors)

This captures the "building up" from smaller to larger squarefree numbers.
""")

def build_mult_structure(sqfree_list):
    """Build operator encoding multiplicative structure."""
    N = len(sqfree_list)
    T = np.zeros((N, N))
    idx = {n: i for i, n in enumerate(sqfree_list)}

    for i, n in enumerate(sqfree_list):
        # Sum over proper divisors
        for d in range(1, n):
            if n % d == 0 and d in idx:
                T[idx[d], i] = 1  # |d⟩ appears in T|n⟩

    return T

T_mult = build_mult_structure(sqfree_small)

# Make Hermitian
T_mult_sym = (T_mult + T_mult.T) / 2

print(f"\nMultiplicative structure operator T_mult:")
print(f"  Shape: {T_mult_sym.shape}")
print(f"  Is Hermitian? {np.allclose(T_mult_sym, T_mult_sym.T)}")

mult_eigenvalues = la.eigvalsh(T_mult_sym)
print(f"  Eigenvalue range: [{min(mult_eigenvalues):.2f}, {max(mult_eigenvalues):.2f}]")

# Check for ζ zeros
print(f"\n  Checking for ζ zeros in spectrum:")
for gamma in zeta_zeros[:5]:
    closest = min(np.abs(mult_eigenvalues - gamma))
    print(f"    γ = {gamma:.4f}: closest eigenvalue distance = {closest:.4f}")

# =============================================================================
# PART 10: WHY THIS IS SO HARD
# =============================================================================

print("""
================================================================================
PART 10: WHY THE HILBERT-PÓLYA APPROACH IS HARD
================================================================================

THE FUNDAMENTAL CHALLENGE:
==========================
The ζ zeros are NOT simple eigenvalues of "obvious" operators.

Any operator H with Spec(H) = {γ} must:
1. Know about ALL primes (since zeros encode prime distribution)
2. Be self-adjoint (for real spectrum)
3. Have a natural, non-circular construction

WHAT WE'VE TRIED:
=================
• H_ω: Spectrum = {0, 1, 2, 3, ...} (just counts)
• H_log: Spectrum = {log n} (just logs)
• M_μ: Spectrum = {±1} (just Möbius values)
• D: Divisibility structure
• xp + px: Berry-Keating (doesn't match)
• T_mult: Multiplicative structure

NONE give ζ zeros!

WHY NOT?
========
The ζ zeros come from the GLOBAL structure of primes.
They encode correlations at all scales.

Our operators encode LOCAL structure:
  • H_ω knows about each n separately
  • H_log knows about each log(n) separately
  • D knows about divisibility pairs

No LOCAL operator can capture GLOBAL correlations.

WHAT WOULD WORK:
================
An operator that simultaneously encodes:
  1. All prime logarithms (log 2, log 3, log 5, ...)
  2. Their incommensurability (log 2 / log 3 is irrational)
  3. The "randomness" of prime distribution

This is essentially ENCODING ζ(s) INTO AN OPERATOR.

THE CIRCULARITY:
================
To build H with Spec(H) = {ζ zeros}, we need to know the zeros.
But if we knew the zeros, we wouldn't need H!

A non-circular construction would derive H from:
  • First principles (arithmetic of integers)
  • Without explicitly computing zeros

This is the 100-year open problem.
""")

# =============================================================================
# PART 11: CONNES' APPROACH
# =============================================================================

print("""
================================================================================
PART 11: CONNES' APPROACH (BRIEF OVERVIEW)
================================================================================

Alain Connes' approach uses NONCOMMUTATIVE GEOMETRY.

THE KEY INGREDIENTS:
====================
1. ADELES: The ring A = ℝ × Π_p ℚ_p (product over all primes)
   This captures all "local" information at once.

2. IDELES: The group GL_1(A) of invertible adeles.

3. QUOTIENT SPACE: The space X = A*/ℚ* (adeles mod rationals)
   This is a "noncommutative space" in Connes' sense.

4. THE TRACE FORMULA:
   Tr(f on L²(X)) = "explicit formula"

   This connects:
   - Geometric side (primes)
   - Spectral side (zeros)

THE ABSORPTION SPECTRUM:
========================
Connes shows there's an operator whose "absorption spectrum"
(places where it fails to have a resolvent) includes ζ zeros.

But getting the FULL spectrum (not just absorption) is hard.

STATUS:
=======
• Partially successful: connects ζ zeros to operator theory
• Incomplete: doesn't prove RH
• Very abstract: requires deep mathematics (noncommutative geometry)
""")

# =============================================================================
# PART 12: WHAT WE CAN CONTRIBUTE
# =============================================================================

print("""
================================================================================
PART 12: WHAT OUR FRAMEWORK MIGHT CONTRIBUTE
================================================================================

Our generating function: G(z, x) = Σ_w z^w S_w(x)

Key relation: G̃(-1, s) = 1/(s·ζ(s))

NEW PERSPECTIVE:
================
The generating function encodes the ω-distribution among squarefree numbers.

The ω distribution has:
  • Mean ≈ log log x
  • Variance < mean (subPoisson)
  • Specific shape determined by primes

POTENTIAL OPERATOR INTERPRETATION:
==================================
Define: Z(β, x) = G(e^{-β}, x) = Σ_w e^{-βw} S_w(x)

This is like a partition function with:
  • "Energy levels" w = 0, 1, 2, ...
  • "Degeneracies" S_w(x)
  • "Temperature" 1/β

The "Hamiltonian" would be H_ω with spectrum {0, 1, 2, ...}.

But the TEMPERATURE DEPENDENCE (via β) connects to s in ζ(s).

At β → 0: Z → Q(x) (total count)
At β → ∞: Z → S_0(x) = 1 (ground state)
At β = iπ: Z(iπ, x) = G(-1, x) = M(x)

The IMAGINARY temperature β = iπ gives the Möbius sum!

SPECULATION:
============
Maybe the "right" operator involves:
  • H_ω for the discrete levels
  • A continuous parameter related to β (or s)
  • Boundary conditions that select ζ zeros

This connects our framework to the statistical mechanics approach
to RH (partition functions, Lee-Yang zeros, etc.)

BUT: This is speculation. We haven't found the operator.
""")

print("=" * 80)
print("HILBERT-PÓLYA EXPLORATION COMPLETE")
print("=" * 80)

print("""
SUMMARY:
========
1. Built several natural operators on ℓ²(squarefree numbers)
2. None have spectra matching ζ zeros
3. Berry-Keating xp+px doesn't give zeros in discrete approximation
4. Multiplicative structure operators also fail
5. The problem requires GLOBAL information, not just LOCAL structure
6. Our generating function connects to partition functions
7. The Hilbert-Pólya operator remains undiscovered after 110 years
""")
