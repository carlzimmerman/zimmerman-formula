"""
BERRY-KEATING OPERATOR AND THE SPECTRAL CONNECTION
===================================================

Deep exploration of the Berry-Keating conjecture that ζ zeros
are eigenvalues of the operator H = xp + px (or 1/2(xp + px)).

We explore how our covariance structure might connect to this.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import linalg
from sympy import factorint, primerange, factorial
from collections import defaultdict
import mpmath
mpmath.mp.dps = 50

print("=" * 80)
print("BERRY-KEATING OPERATOR AND THE SPECTRAL CONNECTION")
print("=" * 80)

# =============================================================================
# PRECOMPUTATION
# =============================================================================

print("\nPrecomputing...")

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

def compute_S_w(x, max_omega=15):
    S = defaultdict(int)
    for n in range(1, min(x + 1, MAX_N + 1)):
        if mu[n] != 0:
            S[omega_vals[n]] += 1
    return S

def compute_M(x):
    return sum(mu[n] for n in range(1, min(x + 1, MAX_N + 1)))

print("Done.")

# =============================================================================
# PART 1: THE BERRY-KEATING CONJECTURE
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE BERRY-KEATING CONJECTURE")
print("=" * 80)

print("""
THE CONJECTURE (Berry-Keating, 1999):
=====================================

The Riemann zeros ρ = 1/2 + iγ have imaginary parts γ that are
eigenvalues of the operator:

    H = xp + px   (or equivalently H = -i(x d/dx + d/dx x)/2)

where x is position and p = -i d/dx is momentum.

This is essentially the "dilation generator" in quantum mechanics.


SEMICLASSICAL ANALYSIS:
=======================

For classical trajectories of H = xp:
    dx/dt = p,  dp/dt = -x

This gives hyperbolic motion: x(t) = x₀ e^t, p(t) = p₀ e^{-t}

The periodic orbits have periods T related to primes:
    T_p = log p

This connects classical dynamics to the explicit formula!


THE PROBLEM:
============

H = xp + px on L²(R) has continuous spectrum (all of R).
To get discrete spectrum at the ζ zeros, one needs:
    1. A specific domain/boundary condition
    2. Or a modified operator

Berry-Keating suggest the boundary should involve the primes.


OUR CONNECTION:
===============

Our covariance matrix Cov(S_w, S_{w'}) encodes prime information.
Could it be related to the boundary conditions for H?
""")

# =============================================================================
# PART 2: THE SHIFT OPERATOR ON ω-SPACE
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: THE SHIFT OPERATOR ON ω-SPACE")
print("=" * 80)

print("""
Consider operators on the ω-graded space:

    (S⁺ f)(w) = f(w+1)      (raise ω by 1)
    (S⁻ f)(w) = f(w-1)      (lower ω by 1)
    (N f)(w) = w f(w)       (number operator)

These satisfy:  [N, S⁺] = S⁺,  [N, S⁻] = -S⁻

Analogy to Berry-Keating:
    x ↔ S⁺ (exponential growth)
    p ↔ S⁻ (exponential decay)
    xp ↔ S⁺ S⁻ = shift and back

What is the "Hamiltonian" S⁺ S⁻ + S⁻ S⁺ on our space?
""")

# Construct the shift operators
max_omega = 10

S_plus = np.zeros((max_omega, max_omega))
S_minus = np.zeros((max_omega, max_omega))
N_op = np.zeros((max_omega, max_omega))

for w in range(max_omega):
    N_op[w, w] = w
    if w < max_omega - 1:
        S_plus[w, w + 1] = 1
    if w > 0:
        S_minus[w, w - 1] = 1

# The "Hamiltonian"
H_BK = S_plus @ S_minus + S_minus @ S_plus

print("Berry-Keating analog H = S⁺S⁻ + S⁻S⁺:")
print("-" * 60)
for i in range(min(8, max_omega)):
    for j in range(min(8, max_omega)):
        print(f"{H_BK[i, j]:>5.1f}", end=" ")
    print()

# Eigenvalues of H_BK
ev_HBK, vec_HBK = np.linalg.eigh(H_BK)
print(f"\nEigenvalues of H_BK: {np.sort(ev_HBK)}")

# The alternating vector
alt_vec = np.array([(-1)**w for w in range(max_omega)])
alt_norm = alt_vec / np.linalg.norm(alt_vec)

# Project onto H_BK eigenvectors
print(f"\nProjection of alternating vector onto H_BK eigenvectors:")
for i, ev in enumerate(np.sort(ev_HBK)):
    idx = np.argsort(ev_HBK)[i]
    proj = abs(np.dot(alt_norm, vec_HBK[:, idx]))
    print(f"  λ = {ev:.4f}: projection = {proj:.4f}")

# =============================================================================
# PART 3: WEIGHTED SHIFT OPERATORS
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: WEIGHTED SHIFT OPERATORS (PRIME-WEIGHTED)")
print("=" * 80)

print("""
The S_w counts involve specific prime structure.

Define WEIGHTED shift operators using prime information:
    (S_p f)(w) = α_p(w) f(w+1)

where α_p(w) depends on how prime p affects ω-level transitions.

From our data: α_p(w) ≈ (number of squarefree n with ω(n)=w divisible by p)
                       / (total in level w)
""")

# Compute weighted shifts from actual data
x = 100000
S = compute_S_w(x)

# For each prime p, compute transition weights
primes = list(primerange(2, 50))

print("\nPrime-weighted transition matrices:")

for p in primes[:5]:
    print(f"\nPrime p = {p}:")

    # Compute: of n with ω(n)=w divisible by p, what's the distribution
    # Actually: (n/p has ω = w-1) → (n has ω = w)
    # So we measure: P(p | n | ω(n) = w)

    trans = np.zeros((8, 8))
    for n in range(1, x + 1):
        if mu[n] != 0:
            w = omega_vals[n]
            if w < 8 and n % p == 0:
                # n/p has ω = w-1
                if w > 0:
                    trans[w-1, w] += 1

    # Normalize by source level
    for w in range(7):
        row_sum = trans[w, :].sum()
        if row_sum > 0:
            trans[w, :] /= row_sum

    print("  Transition probabilities (row w → col w+1):")
    for w in range(5):
        print(f"    w={w} → w+1: {trans[w, w+1]:.4f}")

# =============================================================================
# PART 4: THE "MULTIPLICATION BY n" OPERATOR
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: THE 'MULTIPLICATION BY n' PERSPECTIVE")
print("=" * 80)

print("""
Another Berry-Keating idea: the operator "multiplication by n"
on functions f(n) has eigenvalues related to ζ.

Define:
    (M_n f)(m) = δ_{n,m} × f(m)

More interesting: the operator that averages over divisors:
    (D f)(n) = (1/d(n)) Σ_{d|n} f(d)

where d(n) = number of divisors.

For Möbius:
    (D μ)(n) = (1/d(n)) Σ_{d|n} μ(d) = {1/d(n) if n=1, else 0 or small}
""")

# Compute D μ for small n
print("\n(D μ)(n) for small n:")
print("-" * 40)

for n in range(1, 31):
    if n <= MAX_N:
        divisors = [d for d in range(1, n+1) if n % d == 0]
        sum_mu_div = sum(mu[d] for d in divisors)
        d_n = len(divisors)
        D_mu_n = sum_mu_div / d_n
        print(f"  n = {n:2d}: d(n) = {d_n}, Σμ(d) = {sum_mu_div:+2d}, (Dμ)(n) = {D_mu_n:+.4f}")

# =============================================================================
# PART 5: SCALING BEHAVIOR OF λ_alt
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: DETAILED SCALING OF λ_alt / Tr(Cov)")
print("=" * 80)

print("""
From previous analysis: λ_alt / Tr(Cov) decays from 0.27 to 0.066
as x goes from 20K to 200K.

Let's fit this more precisely and understand the decay rate.
""")

def compute_covariance_matrix(x_values, max_omega=8):
    """Compute covariance matrix of S_w increments."""
    S_matrix = []
    for x_val in x_values:
        S_x = compute_S_w(x_val)
        row = [S_x[w] for w in range(max_omega)]
        S_matrix.append(row)

    S_matrix = np.array(S_matrix, dtype=float)
    delta_S = np.diff(S_matrix, axis=0)
    cov = np.cov(delta_S.T)
    return cov

# More detailed scan
x_max_values = list(range(15000, 200001, 5000))
lambda_alt_data = []
trace_data = []

for x_max in x_max_values:
    x_vals = np.arange(5000, x_max + 1, max(1000, x_max // 50))
    cov = compute_covariance_matrix(x_vals, max_omega=8)

    alt_vec = np.array([(-1)**w for w in range(8)])
    lambda_alt = alt_vec @ cov @ alt_vec / (alt_vec @ alt_vec)
    trace_cov = np.trace(cov)

    lambda_alt_data.append(lambda_alt)
    trace_data.append(trace_cov)

lambda_alt_data = np.array(lambda_alt_data)
trace_data = np.array(trace_data)
x_max_values = np.array(x_max_values)

ratios = lambda_alt_data / trace_data

print("\nDetailed scaling analysis:")
print("-" * 70)
print(f"{'x_max':>10} {'λ_alt':>12} {'Tr(Cov)':>12} {'ratio':>12} {'log(x)':>10}")
print("-" * 70)

for i in range(0, len(x_max_values), 5):
    x = x_max_values[i]
    print(f"{x:>10} {lambda_alt_data[i]:>12.2f} {trace_data[i]:>12.2f} "
          f"{ratios[i]:>12.6f} {np.log(x):>10.4f}")

# Fit: ratio = A / (log x)^α or ratio = A × x^(-β)
log_x = np.log(x_max_values)
log_ratio = np.log(ratios)

# Linear fit in log-log space: log(ratio) = log(A) - α × log(log(x))
log_log_x = np.log(log_x)
coeffs = np.polyfit(log_log_x, log_ratio, 1)
alpha = -coeffs[0]
log_A = coeffs[1]

print(f"\nFit: ratio ~ A / (log x)^α")
print(f"  α = {alpha:.4f}")
print(f"  A = {np.exp(log_A):.4f}")

# Alternative: fit to x^(-β)
coeffs2 = np.polyfit(np.log(x_max_values), log_ratio, 1)
beta = -coeffs2[0]
print(f"\nAlternative fit: ratio ~ x^(-β)")
print(f"  β = {beta:.4f}")

# =============================================================================
# PART 6: THE DISCRETIZED BERRY-KEATING
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: DISCRETIZED BERRY-KEATING OPERATOR")
print("=" * 80)

print("""
Consider the discretization:
    H = xp + px → H_discrete = n(D - D⁻¹) + (D - D⁻¹)n

where D is the shift operator: (Df)(n) = f(n+1).

On the ω-graded space, this becomes:
    H_ω = ω(S⁺ - S⁻) + (S⁺ - S⁻)ω
        = ω S⁺ - ω S⁻ + S⁺ ω - S⁻ ω
        = ω S⁺ + (ω+1) S⁺ - ω S⁻ - (ω-1) S⁻
        = (2ω + 1) S⁺ - (2ω - 1) S⁻
""")

# Construct this operator
max_omega = 12
H_omega = np.zeros((max_omega, max_omega))

for w in range(max_omega):
    if w < max_omega - 1:
        H_omega[w, w + 1] = 2*w + 1  # S⁺ coefficient
    if w > 0:
        H_omega[w, w - 1] = -(2*w - 1)  # S⁻ coefficient

print("H_ω matrix (first 8×8):")
print("-" * 60)
for i in range(8):
    for j in range(8):
        print(f"{H_omega[i, j]:>6.1f}", end=" ")
    print()

# This is antisymmetric! Eigenvalues are purely imaginary
ev_Homega = np.linalg.eigvals(H_omega)
ev_sorted = sorted(ev_Homega, key=lambda z: z.imag)

print(f"\nEigenvalues of H_ω (purely imaginary):")
for ev in ev_sorted:
    if abs(ev.real) < 0.01:
        print(f"  {ev.imag:+.4f}i")
    else:
        print(f"  {ev.real:+.4f} {ev.imag:+.4f}i")

# Make H_ω self-adjoint by adding i
H_omega_sa = 1j * H_omega

ev_sa = np.linalg.eigvals(H_omega_sa)
ev_sa_real = np.sort(ev_sa.real)

print(f"\nEigenvalues of i×H_ω (real):")
for ev in ev_sa_real:
    print(f"  {ev:+.4f}")

# =============================================================================
# PART 7: CORRELATING WITH ζ ZEROS
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: DO EIGENVALUES CORRELATE WITH ζ ZEROS?")
print("=" * 80)

print("""
The first few imaginary parts of ζ zeros are:
    γ₁ ≈ 14.13
    γ₂ ≈ 21.02
    γ₃ ≈ 25.01
    γ₄ ≈ 30.42
    γ₅ ≈ 32.94

Do our eigenvalues show any relation to these?
""")

# Known ζ zeros (imaginary parts)
zeta_zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918720, 43.327073, 48.005151, 49.773832]

print("First 10 ζ zeros (imaginary parts):")
for i, z in enumerate(zeta_zeros):
    print(f"  γ_{i+1} = {z:.4f}")

# Scale our eigenvalues to match
ev_for_comparison = ev_sa_real[ev_sa_real > 0]  # positive eigenvalues
print(f"\nOur eigenvalues (positive, from i×H_ω):")
for i, ev in enumerate(ev_for_comparison[:10]):
    print(f"  λ_{i+1} = {ev:.4f}")

# Try scaling
if len(ev_for_comparison) > 0:
    scale_factor = zeta_zeros[0] / ev_for_comparison[0] if ev_for_comparison[0] > 0 else 1
    print(f"\nIf we scale by {scale_factor:.4f}:")
    for i, ev in enumerate(ev_for_comparison[:5]):
        scaled = ev * scale_factor
        closest_zero = min(zeta_zeros, key=lambda z: abs(z - scaled))
        print(f"  {ev:.4f} × {scale_factor:.2f} = {scaled:.4f} (closest ζ zero: {closest_zero:.4f})")

# =============================================================================
# PART 8: THE "PRIME DERIVATIVE" OPERATOR
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: THE 'PRIME DERIVATIVE' OPERATOR")
print("=" * 80)

print("""
Define an operator on arithmetic functions:

    (D_P f)(n) = Σ_{p | n} f(n/p)

This "differentiates" by removing one prime factor.

For μ:
    (D_P μ)(n) = Σ_{p | n} μ(n/p)

This connects levels w and w-1 in the ω-grading!
""")

# Compute D_P μ
print("\n(D_P μ)(n) for squarefree n:")
print("-" * 50)

for n in [2, 3, 5, 6, 10, 15, 30, 42, 70, 105, 210]:
    if n <= MAX_N and mu[n] != 0:
        # Find primes dividing n
        prime_divs = [p for p in range(2, n+1) if n % p == 0 and mu[p] != 0 and all(p % q != 0 for q in range(2, int(p**0.5)+1))]
        prime_divs = [p for p in range(2, n+1) if n % p == 0 and n // p > 0 and all(p % q != 0 for q in range(2, p) if q * q <= p)]
        # Actually, for squarefree n, prime divisors are those p with μ(n) = -μ(n/p)
        from sympy import primefactors
        pf = list(primefactors(n))

        D_P_mu = sum(mu[n // p] for p in pf)
        print(f"  n = {n:4d}, ω = {len(pf)}, μ(n) = {mu[n]:+d}, "
              f"D_P μ = {D_P_mu:+d}, primes = {pf}")

# =============================================================================
# PART 9: THE LAPLACIAN ON ω-SPACE
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: THE LAPLACIAN ON ω-SPACE")
print("=" * 80)

print("""
Define a "Laplacian" on ω-space weighted by our covariance structure:

    Δ = D^T C^{-1} D

where D is the discrete derivative and C is the covariance matrix.

The eigenvalues of Δ characterize the "smoothness" in ω-space.
The alternating direction should have LARGE Laplacian eigenvalue
(it oscillates the most).
""")

# Compute covariance matrix
x_vals = np.arange(10000, 100001, 2000)
cov = compute_covariance_matrix(x_vals, max_omega=8)

# Discrete derivative matrix
max_w = 8
D = np.zeros((max_w - 1, max_w))
for i in range(max_w - 1):
    D[i, i] = -1
    D[i, i + 1] = 1

print("Discrete derivative D:")
print(D)

# Regularize covariance
cov_reg = cov + 0.01 * np.eye(max_w)
cov_inv = np.linalg.inv(cov_reg)

# Laplacian
Laplacian = D.T @ D  # Simple discrete Laplacian first

print("\nSimple discrete Laplacian D^T D:")
print("-" * 60)
for i in range(max_w):
    for j in range(max_w):
        print(f"{Laplacian[i, j]:>5.1f}", end=" ")
    print()

ev_Lap, vec_Lap = np.linalg.eigh(Laplacian)

print(f"\nEigenvalues of Laplacian:")
for i, ev in enumerate(np.sort(ev_Lap)[::-1]):
    print(f"  λ_{i+1} = {ev:.4f}")

# Alternating direction
alt_vec = np.array([(-1)**w for w in range(max_w)])
alt_norm = alt_vec / np.linalg.norm(alt_vec)

# Rayleigh quotient
rayleigh = alt_norm @ Laplacian @ alt_norm
print(f"\nRayleigh quotient for alternating direction: {rayleigh:.4f}")
print(f"Maximum eigenvalue: {max(ev_Lap):.4f}")
print(f"Ratio: {rayleigh / max(ev_Lap):.4f}")

# =============================================================================
# PART 10: SYNTHESIS - THE SPECTRAL PICTURE
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: SYNTHESIS - THE SPECTRAL PICTURE")
print("=" * 80)

print("""
WHAT WE'VE EXPLORED:
====================

1. BERRY-KEATING OPERATOR
   H = xp + px has continuous spectrum on L²(R)
   Discretization gives H_ω = (2ω+1)S⁺ - (2ω-1)S⁻
   Eigenvalues of i×H_ω are real but don't match ζ zeros directly

2. SHIFT OPERATORS
   S⁺S⁻ + S⁻S⁺ gives a simple tridiagonal operator
   The alternating vector projects onto multiple eigenvectors

3. PRIME DERIVATIVE
   D_P: f(n) ↦ Σ_{p|n} f(n/p) connects ω-levels
   Acts like a "lowering operator" on the ω-grading

4. LAPLACIAN
   The alternating direction has Rayleigh quotient = max eigenvalue
   This confirms it's the "most oscillatory" direction

5. SCALING OF λ_alt
   λ_alt / Tr(Cov) ~ 1/(log x)^α with α ≈ {alpha:.2f}
   Or equivalently ~ x^(-β) with β ≈ {beta:.4f}


THE KEY INSIGHT:
================

The alternating direction v = (1, -1, 1, -1, ...) corresponds to M(x).

In EVERY operator we studied, this direction has special properties:
- Small eigenvalue in Cov (variance reduction)
- Maximum eigenvalue in Laplacian (most oscillatory)
- Mixed projection in Berry-Keating type operators

The spectral conjecture becomes:

    There exists an operator T on ω-space (or primes × ω) such that:
    1. T has spectrum related to ζ zeros
    2. The alternating direction is an eigenvector with λ related to √x
    3. Self-adjointness of T implies RH


WHAT'S NEEDED:
==============

1. Find the correct "mass" or "potential" term to add to the
   Berry-Keating operator to get discrete spectrum

2. Connect the ω-grading to the prime structure more explicitly

3. Show that the covariance matrix IS the restriction of T²

4. Prove spectral properties imply the bound on M(x)
""")

# =============================================================================
# PART 11: A CANDIDATE OPERATOR
# =============================================================================

print("\n" + "=" * 80)
print("PART 11: A CANDIDATE OPERATOR")
print("=" * 80)

print("""
PROPOSAL:
=========

Define the operator T on L²(Z≥0) by:

    (Tf)(w) = √w × f(w+1) + √(w-1) × f(w-1) + V(w) × f(w)

where V(w) is a "potential" encoding prime information.

This is a Jacobi operator with:
    a_w = V(w)  (diagonal)
    b_w = √w    (off-diagonal)

The √w weights come from the Poisson structure of ω.


CHOICE OF V(w):
===============

From our covariance matrix, we can read off an effective potential:
    V(w) ≈ mean correlation at level w
""")

# Extract effective potential from covariance
x_vals = np.arange(10000, 100001, 2000)
cov = compute_covariance_matrix(x_vals, max_omega=10)

# Diagonal = variance at each level
diagonal = np.diag(cov)

# Normalize by typical scale
scale = np.sqrt(np.mean(diagonal[1:]))

# Effective potential
V_eff = diagonal / scale

print("\nEffective potential V(w) from covariance:")
print("-" * 40)
for w in range(len(V_eff)):
    print(f"  V({w}) = {V_eff[w]:.4f}")

# Construct the Jacobi operator with this potential
max_w = 10
T_candidate = np.zeros((max_w, max_w))

for w in range(max_w):
    T_candidate[w, w] = V_eff[w] if w < len(V_eff) else 0

    if w < max_w - 1:
        T_candidate[w, w + 1] = np.sqrt(w + 1)
        T_candidate[w + 1, w] = np.sqrt(w + 1)

print("\nCandidate operator T:")
print("-" * 80)
for i in range(min(8, max_w)):
    for j in range(min(8, max_w)):
        print(f"{T_candidate[i, j]:>7.3f}", end=" ")
    print()

# Eigenvalues
ev_T, vec_T = np.linalg.eigh(T_candidate)

print(f"\nEigenvalues of T:")
for i, ev in enumerate(np.sort(ev_T)):
    print(f"  λ_{i+1} = {ev:.4f}")

# Alternating vector projection
alt_vec = np.array([(-1)**w for w in range(max_w)])
alt_norm = alt_vec / np.linalg.norm(alt_vec)

projections = vec_T.T @ alt_norm

print(f"\nProjection of alternating vector onto T eigenvectors:")
for i, ev in enumerate(np.sort(ev_T)):
    idx = np.argsort(ev_T)[i]
    print(f"  λ = {ev:.4f}: |projection| = {abs(projections[idx]):.4f}")

print("\n" + "=" * 80)
print("END OF BERRY-KEATING ANALYSIS")
print("=" * 80)
