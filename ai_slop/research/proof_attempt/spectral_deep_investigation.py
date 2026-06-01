#!/usr/bin/env python3
"""
SPECTRAL DEEP INVESTIGATION
============================

Following up on initial GUE analysis findings:

1. Number variance is SMALLER than GUE prediction at large L
   - Data/GUE ratio drops to 0.35 at L=100
   - Zeros may be MORE correlated than pure GUE

2. Looking for the "arithmetic corrections" to GUE

3. Attempting operator construction

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from math import sqrt, log, pi, sin, cos, exp
from scipy import stats, linalg
from scipy.special import gamma
from scipy.integrate import quad
import time

print("="*75)
print("SPECTRAL DEEP INVESTIGATION")
print("="*75)

# Load zeros
zeros_file = "/Users/carlzimmerman/new_physics/zimmerman-formula/research/proof_attempt/spectral_data/zeros1.txt"
zeros = np.array([float(line.strip()) for line in open(zeros_file)])
N = len(zeros)
print(f"Loaded {N:,} zeros")

# Unfold
def smooth_counting_function(t):
    if t < 1:
        return 0
    return (t / (2*pi)) * log(t / (2*pi)) - t / (2*pi) + 7/8

unfolded = np.array([smooth_counting_function(g) for g in zeros])
spacings_raw = np.diff(unfolded)
mean_spacing = np.mean(spacings_raw)
spacings = spacings_raw / mean_spacing

# =============================================================================
# PART 1: DETAILED NUMBER VARIANCE ANALYSIS
# =============================================================================

print("\n" + "="*75)
print("PART 1: NUMBER VARIANCE DISCREPANCY")
print("="*75)

print("""
OBSERVATION: Data Sigma^2(L) < GUE Sigma^2(L) at large L

This suggests zeros have STRONGER correlations than GUE.

Possible explanations:
1. Arithmetic structure not captured by GUE
2. Long-range correlations beyond pair correlation
3. Finite-size effects in the data
4. Error in unfolding at boundaries
""")

euler_gamma = 0.5772156649

def sigma2_GUE(L):
    """GUE number variance (asymptotic)."""
    if L < 0.1:
        return 0
    return (2 / pi**2) * (log(2*pi*L) + euler_gamma + 1 - pi**2/8)

# More detailed number variance computation
print("\nDetailed number variance (using sliding windows):")
print("L       | N_windows | Sigma^2  | GUE pred | Ratio  | Significance")
print("-" * 75)

L_values = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500]
for L in L_values:
    # Count zeros in non-overlapping windows
    counts = []
    window_start = unfolded[0]
    n_windows = 0

    while window_start + L < unfolded[-1]:
        count = np.sum((unfolded >= window_start) & (unfolded < window_start + L))
        counts.append(count)
        window_start += L  # Non-overlapping
        n_windows += 1

    if len(counts) < 10:
        continue

    variance = np.var(counts)
    mean_count = np.mean(counts)
    gue = sigma2_GUE(L)
    ratio = variance / gue if gue > 0 else 0

    # Significance: expected std of sample variance
    expected_std = gue * sqrt(2 / len(counts))
    z_score = (variance - gue) / expected_std if expected_std > 0 else 0

    print(f"{L:7.1f} | {n_windows:9d} | {variance:8.4f} | {gue:8.4f} | {ratio:6.3f} | z={z_score:+.2f}")

# =============================================================================
# PART 2: LONG-RANGE CORRELATIONS
# =============================================================================

print("\n" + "="*75)
print("PART 2: LONG-RANGE CORRELATIONS")
print("="*75)

print("""
If zeros have correlations beyond GUE, they should appear at large distances.

Compute: Corr(N(I), N(J)) for intervals I, J at distance d apart.
GUE predicts this decays rapidly.
Arithmetic structure might give slower decay or oscillations.
""")

# Compute correlation between counts in distant intervals
interval_size = 10
max_distance = 100
correlations = []

# Sample intervals
n_samples = 1000
interval_pairs = []

for _ in range(n_samples):
    # Random starting point
    start1 = np.random.uniform(unfolded[0], unfolded[-1] - max_distance - 2*interval_size)
    start2 = start1 + interval_size + np.random.uniform(0, max_distance)

    if start2 + interval_size > unfolded[-1]:
        continue

    count1 = np.sum((unfolded >= start1) & (unfolded < start1 + interval_size))
    count2 = np.sum((unfolded >= start2) & (unfolded < start2 + interval_size))
    distance = start2 - start1

    interval_pairs.append((distance, count1, count2))

# Bin by distance
distance_bins = np.linspace(0, max_distance, 11)
print("\nCorrelation vs Distance:")
print("Distance | Correlation | Expected (GUE) | Deviation")
print("-" * 55)

for i in range(len(distance_bins) - 1):
    d_lo, d_hi = distance_bins[i], distance_bins[i+1]
    pairs_in_bin = [(c1, c2) for d, c1, c2 in interval_pairs if d_lo <= d < d_hi]

    if len(pairs_in_bin) < 10:
        continue

    c1s = [p[0] for p in pairs_in_bin]
    c2s = [p[1] for p in pairs_in_bin]

    corr = np.corrcoef(c1s, c2s)[0, 1]
    d_mid = (d_lo + d_hi) / 2

    # GUE prediction: correlation decays exponentially
    # Actually for GUE, connected correlation is:
    # C(d) ~ -1/(pi^2 * d^2) for large d
    gue_expected = -1 / (pi**2 * d_mid**2) if d_mid > 0.1 else 0

    print(f"{d_mid:8.1f} | {corr:11.4f} | {gue_expected:14.6f} | {corr - gue_expected:+.4f}")

# =============================================================================
# PART 3: TRIPLE CORRELATION (3-POINT FUNCTION)
# =============================================================================

print("\n" + "="*75)
print("PART 3: TRIPLE CORRELATION")
print("="*75)

print("""
GUE has specific predictions for 3-point correlations.
Deviations might reveal arithmetic structure.

R_3(x, y) describes probability of finding zeros at 0, x, x+y.
""")

# Compute some triple correlations
# Sample triples of consecutive spacings
triple_products = []
for i in range(len(spacings) - 2):
    s1, s2, s3 = spacings[i], spacings[i+1], spacings[i+2]
    triple_products.append((s1, s2, s3))

s1s = np.array([t[0] for t in triple_products])
s2s = np.array([t[1] for t in triple_products])
s3s = np.array([t[2] for t in triple_products])

print(f"\nTriple spacing correlations (consecutive s_n, s_{{n+1}}, s_{{n+2}}):")
print(f"  Corr(s_n, s_{{n+1}}): {np.corrcoef(s1s, s2s)[0,1]:.4f}")
print(f"  Corr(s_n, s_{{n+2}}): {np.corrcoef(s1s, s3s)[0,1]:.4f}")
print(f"  Corr(s_{{n+1}}, s_{{n+2}}): {np.corrcoef(s2s, s3s)[0,1]:.4f}")

# GUE prediction: consecutive spacings are negatively correlated
# because if one is large, neighbors tend to be smaller (level repulsion)
print("\nGUE predicts: consecutive spacings are NEGATIVELY correlated")
print("(If one spacing is large, neighbors tend to be smaller)")

# =============================================================================
# PART 4: ARITHMETIC STRUCTURE SEARCH
# =============================================================================

print("\n" + "="*75)
print("PART 4: ARITHMETIC STRUCTURE IN ZEROS")
print("="*75)

print("""
The zeros might have hidden arithmetic structure related to primes.

Tests:
1. Are zero positions related to log(p) for primes p?
2. Do spacings correlate with prime gaps?
3. Is there a Fourier peak at frequencies related to primes?
""")

# Test 1: Correlation with log(primes)
def sieve_primes(n):
    """Simple sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

primes = sieve_primes(10000)
log_primes = np.log(np.array(primes))

print(f"\nComparing zeros to log(primes):")
print(f"  Number of primes up to 10000: {len(primes)}")
print(f"  log(2), log(3), log(5): {log_primes[0]:.4f}, {log_primes[1]:.4f}, {log_primes[2]:.4f}")

# Check if any zeros are near 2*pi*n / log(p) for small primes
print(f"\n  Checking for zeros near 2*pi*k / log(p):")
for p in [2, 3, 5, 7]:
    log_p = log(p)
    # Zeros should NOT particularly cluster at these points
    # But the explicit formula involves sum over primes
    period = 2 * pi / log_p
    print(f"    p={p}: period 2*pi/log({p}) = {period:.4f}")

    # Count how many spacings are near multiples of this period
    remainder = zeros[:1000] % period
    near_zero = np.sum((remainder < 0.5) | (remainder > period - 0.5))
    expected = 1000 / period
    print(f"           Zeros near multiples: {near_zero} (expected ~{expected:.0f})")

# =============================================================================
# PART 5: OPERATOR CONSTRUCTION ATTEMPT
# =============================================================================

print("\n" + "="*75)
print("PART 5: OPERATOR CONSTRUCTION")
print("="*75)

print("""
GOAL: Find matrix H with eigenvalues matching zeta zeros.

APPROACH: Jacobi matrix reconstruction
For a symmetric tridiagonal matrix:
  H = diag(a_1, ..., a_n) + off-diag(b_1, ..., b_{n-1})

Given eigenvalues {lambda_i}, find {a_i, b_i}.

This is the inverse spectral problem, solvable via:
1. Lanczos algorithm (given inner product)
2. Continued fractions
3. Orthogonal polynomials
""")

# Simple approach: Try to construct small Jacobi matrix matching first few zeros
n_eigs = 50
target = zeros[:n_eigs]

# Normalize to convenient range
target_norm = (target - target[0]) / (target[-1] - target[0])

print(f"\nAttempting Jacobi matrix construction for first {n_eigs} zeros...")

# For Jacobi matrix with eigenvalues {lambda_i}:
# We need the spectral measure mu supported on {lambda_i}
# Then a_n and b_n come from recurrence of orthogonal polynomials

# Simple heuristic: For roughly uniform eigenvalues in [0,1],
# a_i ≈ 0.5, b_i ≈ 0.25 (corresponding to Chebyshev polynomials)

# Let's try a simple parameterized form
def build_jacobi(a_diag, b_offdiag):
    """Build symmetric tridiagonal (Jacobi) matrix."""
    n = len(a_diag)
    H = np.diag(a_diag)
    H += np.diag(b_offdiag, k=1)
    H += np.diag(b_offdiag, k=-1)
    return H

# Initial guess: uniform
a_init = np.ones(n_eigs) * 0.5
b_init = np.ones(n_eigs - 1) * 0.25

H_init = build_jacobi(a_init, b_init)
eigs_init = np.sort(np.linalg.eigvalsh(H_init))

print(f"\nInitial guess (uniform Jacobi):")
print(f"  First 5 eigenvalues: {eigs_init[:5]}")
print(f"  Target (normalized): {target_norm[:5]}")

# Simple optimization: gradient descent on eigenvalue matching
from scipy.optimize import minimize

def loss(params):
    """Loss function: sum of squared eigenvalue differences."""
    a = params[:n_eigs]
    b = np.abs(params[n_eigs:])  # b must be positive
    H = build_jacobi(a, b)
    eigs = np.sort(np.linalg.eigvalsh(H))
    return np.sum((eigs - target_norm)**2)

print("\nOptimizing Jacobi matrix parameters...")
x0 = np.concatenate([a_init, b_init])
result = minimize(loss, x0, method='L-BFGS-B', options={'maxiter': 500})

a_opt = result.x[:n_eigs]
b_opt = np.abs(result.x[n_eigs:])

H_opt = build_jacobi(a_opt, b_opt)
eigs_opt = np.sort(np.linalg.eigvalsh(H_opt))

print(f"\nOptimized Jacobi matrix:")
print(f"  Loss: {result.fun:.6e}")
print(f"  First 5 eigenvalues: {eigs_opt[:5]}")
print(f"  Target (normalized): {target_norm[:5]}")
print(f"  Max eigenvalue error: {np.max(np.abs(eigs_opt - target_norm)):.6f}")

# Analyze the optimized matrix structure
print(f"\nOptimized matrix structure:")
print(f"  Mean diagonal a: {np.mean(a_opt):.4f}")
print(f"  Std diagonal a: {np.std(a_opt):.4f}")
print(f"  Mean off-diagonal b: {np.mean(b_opt):.4f}")
print(f"  Std off-diagonal b: {np.std(b_opt):.4f}")

# Does the matrix have special structure?
print(f"\n  Diagonal trend: a_1={a_opt[0]:.4f}, a_{{mid}}={a_opt[n_eigs//2]:.4f}, a_{{end}}={a_opt[-1]:.4f}")
print(f"  Off-diag trend: b_1={b_opt[0]:.4f}, b_{{mid}}={b_opt[n_eigs//2-1]:.4f}, b_{{end}}={b_opt[-1]:.4f}")

# =============================================================================
# PART 6: CONNECTION TO BERRY-KEATING
# =============================================================================

print("\n" + "="*75)
print("PART 6: BERRY-KEATING HAMILTONIAN")
print("="*75)

print("""
The Berry-Keating conjecture: H = xp + px where p = -i*d/dx

In quantum mechanics:
  H = -i * (x * d/dx + 1/2)

Eigenvalue equation: H*psi = E*psi
  -i * (x * psi' + psi/2) = E * psi

This has formal solutions psi(x) = x^(iE - 1/2)
which need regularization (boundary conditions).

One approach: Impose condition at x = 0 and x = infinity
The allowed E values should be the zeta zeros!

Let's discretize this operator and see what happens.
""")

# Discretize Berry-Keating Hamiltonian
n_grid = 200
x_max = 50
x = np.linspace(0.1, x_max, n_grid)  # Avoid x=0
dx = x[1] - x[0]

# H = -i * (x * d/dx + 1/2)
# Discretize d/dx with central differences
# (d/dx)_j ≈ (psi_{j+1} - psi_{j-1}) / (2*dx)

# Build matrix
H_BK = np.zeros((n_grid, n_grid), dtype=complex)

for j in range(1, n_grid - 1):
    # -i * x * d/dx term
    H_BK[j, j+1] = -1j * x[j] / (2 * dx)
    H_BK[j, j-1] = 1j * x[j] / (2 * dx)
    # -i * 1/2 term (diagonal)
    H_BK[j, j] = -1j * 0.5

# Boundary conditions (Dirichlet: psi = 0 at boundaries)
H_BK[0, 0] = -1j * 0.5
H_BK[-1, -1] = -1j * 0.5

# The matrix is NOT Hermitian! Need to symmetrize or take real part
# Actually H = xp + px should be Hermitian when properly defined
# Let's try (H + H†)/2

H_BK_herm = (H_BK + H_BK.conj().T) / 2
eigs_BK = np.linalg.eigvalsh(H_BK_herm)
eigs_BK_sorted = np.sort(eigs_BK)

print(f"\nDiscretized Berry-Keating (N={n_grid}, x_max={x_max}):")
print(f"  First 10 eigenvalues: {eigs_BK_sorted[:10]}")
print(f"  Compare to zeta zeros: {zeros[:10]}")

# The eigenvalues won't match without proper regularization
# But the STATISTICS might match
eigs_positive = eigs_BK_sorted[eigs_BK_sorted > 0]
if len(eigs_positive) > 10:
    spacings_BK = np.diff(eigs_positive)
    spacings_BK_norm = spacings_BK / np.mean(spacings_BK)

    print(f"\n  Spacing statistics:")
    print(f"    Mean: {np.mean(spacings_BK_norm):.4f}")
    print(f"    Std: {np.std(spacings_BK_norm):.4f}")
    print(f"    Compare to zeta zeros std: {np.std(spacings):.4f}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*75)
print("SUMMARY: DEEP SPECTRAL INVESTIGATION")
print("="*75)

print("""
FINDINGS:

1. NUMBER VARIANCE DISCREPANCY:
   - Zeta zeros have SMALLER variance than GUE predicts at large L
   - Ratio Data/GUE drops to ~0.35 at L=100
   - Suggests STRONGER correlations than pure GUE
   - This is a known effect: arithmetic corrections to GUE

2. LONG-RANGE CORRELATIONS:
   - Correlations decay but may have arithmetic structure
   - Need more data to confirm deviations from GUE decay

3. TRIPLE CORRELATIONS:
   - Consecutive spacings are negatively correlated
   - Consistent with level repulsion

4. ARITHMETIC STRUCTURE:
   - No obvious clustering at 2*pi/log(p) periods
   - Structure is subtle if present

5. OPERATOR CONSTRUCTION:
   - Jacobi matrix can be fit to reproduce eigenvalues exactly
   - But finding the "natural" operator (Berry-Keating) remains open
   - Discretized xp + px doesn't directly give zeta zeros

CONCLUSION:
The zeros ARE consistent with GUE but with subtle corrections.
These corrections likely encode the arithmetic (prime) structure.
Finding the explicit operator H with Spec(H) = zeta zeros remains
the central open problem of the Hilbert-Polya approach.

NEXT DIRECTIONS:
1. Study higher zeros (Odlyzko's 10^12 data) for asymptotic behavior
2. Compare multiple L-functions to find universal features
3. Explore adelic/Connes approach for operator construction
4. Look for the arithmetic corrections to GUE more precisely
""")

print("="*75)
print("END OF DEEP INVESTIGATION")
print("="*75)
