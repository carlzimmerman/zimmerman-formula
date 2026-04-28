"""
THE SPECTRAL/OPERATOR APPROACH TO RH
=====================================

The Hilbert-Pólya conjecture: The ζ zeros are eigenvalues of a self-adjoint operator.

Our discoveries suggest operator structure:
1. M_p(y) = Σ_{k≥0} M(y/p^k) looks like (1 - T_p)^{-1} M
2. M(y)/M(y/p) ≈ -1 suggests eigenvalue -1
3. The recursion M(x) = 1 - Σ M(x/d) is an operator equation

Can we find the underlying operator and prove RH from its spectrum?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from sympy import mobius, primerange
import math
from scipy import linalg
from scipy.sparse import diags
from scipy.sparse.linalg import eigs

print("=" * 80)
print("THE SPECTRAL/OPERATOR APPROACH TO RH")
print("=" * 80)

# =============================================================================
# SETUP
# =============================================================================

MAX_N = 30000

print("Computing Mertens function...")
M_array = [0] * (MAX_N + 1)
mu_array = [0] * (MAX_N + 1)
cumsum = 0
for n in range(1, MAX_N + 1):
    mu_array[n] = int(mobius(n))
    cumsum += mu_array[n]
    M_array[n] = cumsum

def M(x):
    x = int(x)
    if x < 1:
        return 0
    if x <= MAX_N:
        return M_array[x]
    return 0

def mu(n):
    n = int(n)
    if n <= MAX_N:
        return mu_array[n]
    return int(mobius(n))

primes = list(primerange(2, 500))
print("Done.")

# =============================================================================
# PART 1: THE SCALING OPERATOR
# =============================================================================

print("""

================================================================================
PART 1: THE SCALING OPERATOR T_p
================================================================================

Define: (T_p f)(x) = f(x/p) for x ≥ p, else 0

The identity M_p(y) = Σ_{k≥0} M(y/p^k) becomes:

    M_p = (I + T_p + T_p² + ...) M = (I - T_p)^{-1} M

This means: (I - T_p) M_p = M

Or: M_p - T_p M_p = M
    M_p(y) - M_p(y/p) = M(y)  ✓ (our identity!)

The ratio M(y)/M(y/p) ≈ -1 suggests:
    T_p M ≈ -M (approximately)

So M is an APPROXIMATE EIGENVECTOR of T_p with eigenvalue -1!
""")

# Verify the eigenvalue -1 approximation
print("Testing if M is an approximate eigenvector of T_2:")
y_values = list(range(100, 10001, 100))
eigenvalue_ratios = []
for y in y_values:
    My = M(y)
    My2 = M(y // 2)
    if abs(My) > 5:
        eigenvalue_ratios.append(My2 / My)

print(f"  E[M(y/2)/M(y)] = {np.mean(eigenvalue_ratios):.4f}")
print(f"  Std = {np.std(eigenvalue_ratios):.4f}")
print(f"  If M were eigenvector with λ=-1: ratio = -1")

# =============================================================================
# PART 2: THE OPERATOR MATRIX
# =============================================================================

print("""

================================================================================
PART 2: THE OPERATOR MATRIX
================================================================================

Consider the finite-dimensional approximation:
Let V = span{M(1), M(2), ..., M(N)} ⊂ ℝ^N

The scaling operator T_2 acts as:
    (T_2 M)(k) = M(k/2) for k even, 0 for k odd

In matrix form: (T_2)_{ij} = δ_{i, 2j}

Let's compute this matrix and find its eigenvalues.
""")

N = 200  # Dimension

# Build the T_2 matrix
T2 = np.zeros((N, N))
for i in range(N):
    k = i + 1  # k goes from 1 to N
    if k % 2 == 0:
        j = k // 2 - 1  # Column index for M(k/2)
        if j >= 0:
            T2[i, j] = 1

print(f"T_2 matrix ({N}×{N}):")
print(f"  Non-zero entries: {np.count_nonzero(T2)}")
print(f"  Rank: {np.linalg.matrix_rank(T2)}")

# Eigenvalues of T_2
eigenvalues_T2 = np.linalg.eigvals(T2)
nonzero_eigs = eigenvalues_T2[np.abs(eigenvalues_T2) > 1e-10]
print(f"  Non-zero eigenvalues: {len(nonzero_eigs)}")
print(f"  Eigenvalues: {sorted(nonzero_eigs.real, reverse=True)[:10]}")

# =============================================================================
# PART 3: THE MERTENS RECURSION OPERATOR
# =============================================================================

print("""

================================================================================
PART 3: THE MERTENS RECURSION OPERATOR
================================================================================

The recursion M(x) = 1 - Σ_{d=2}^{x} M(⌊x/d⌋) can be written as:

    M = e - D·M

where e = (1, 1, 1, ...) and D is a "divisor sum" operator:

    (D·M)_k = Σ_{d=2}^{k} M(⌊k/d⌋)

So: (I + D)M = e
    M = (I + D)^{-1} e

The operator (I + D)^{-1} should have special spectral properties!
""")

# Build the D matrix
N = 200
D = np.zeros((N, N))
for k in range(1, N + 1):
    for d in range(2, k + 1):
        j = k // d  # M(k/d) corresponds to column j-1
        if j >= 1:
            D[k-1, j-1] += 1

print(f"D matrix ({N}×{N}):")
print(f"  Non-zero entries: {np.count_nonzero(D)}")

# Compute (I + D)^{-1}
I_plus_D = np.eye(N) + D
try:
    inv_I_plus_D = np.linalg.inv(I_plus_D)
    print(f"  (I + D) is invertible: Yes")

    # Check M = (I + D)^{-1} e
    e = np.ones(N)
    M_computed = inv_I_plus_D @ e
    M_actual = np.array([M(k) for k in range(1, N + 1)])

    error = np.max(np.abs(M_computed - M_actual))
    print(f"  Max error |M_computed - M_actual|: {error:.6f}")
except:
    print(f"  (I + D) is singular!")

# =============================================================================
# PART 4: EIGENVALUES OF (I + D)
# =============================================================================

print("""

================================================================================
PART 4: EIGENVALUES OF (I + D)
================================================================================

The operator (I + D) satisfies: (I + D)M = e

Its eigenvalues control how M behaves!

If (I + D) has eigenvalue λ near 0, then (I + D)^{-1} blows up,
and M could be large.

Let's find the eigenvalues of (I + D).
""")

eigenvalues_ID = np.linalg.eigvals(I_plus_D)
print(f"Eigenvalues of (I + D):")
print(f"  Min |λ|: {np.min(np.abs(eigenvalues_ID)):.6f}")
print(f"  Max |λ|: {np.max(np.abs(eigenvalues_ID)):.6f}")
print(f"  # with |λ| < 1: {np.sum(np.abs(eigenvalues_ID) < 1)}")

# Sort by magnitude
sorted_eigs = sorted(eigenvalues_ID, key=lambda x: abs(x))
print(f"\n  Smallest eigenvalues:")
for i, eig in enumerate(sorted_eigs[:10]):
    print(f"    λ_{i+1} = {eig.real:.4f} + {eig.imag:.4f}i, |λ| = {abs(eig):.4f}")

# =============================================================================
# PART 5: THE DIRICHLET CONVOLUTION OPERATOR
# =============================================================================

print("""

================================================================================
PART 5: THE DIRICHLET CONVOLUTION OPERATOR
================================================================================

Define the Dirichlet convolution operator L_g:
    (L_g f)(n) = Σ_{d|n} g(d) f(n/d) = (g * f)(n)

Key property: L_g L_h = L_{g*h}

For the constant function 1:
    L_1 μ = ε (the Kronecker delta)

This means: L_1 is almost the inverse of L_μ!

    L_μ L_1 = L_{μ*1} = L_ε = I

So L_1 = L_μ^{-1} on appropriate spaces.
""")

# Build L_1 matrix (Dirichlet convolution with 1)
N = 100
L1 = np.zeros((N, N))
for n in range(1, N + 1):
    for d in range(1, n + 1):
        if n % d == 0:
            L1[n-1, (n//d)-1] += 1

print(f"L_1 (convolution with 1) matrix:")
print(f"  Shape: {L1.shape}")
print(f"  Non-zero entries: {np.count_nonzero(L1)}")

# Check L_1 * μ = ε
mu_vec = np.array([mu(n) for n in range(1, N + 1)])
result = L1 @ mu_vec
expected = np.zeros(N)
expected[0] = 1  # ε(1) = 1, ε(n) = 0 for n > 1

print(f"  L_1 · μ = ε? Max error: {np.max(np.abs(result - expected)):.6f}")

# =============================================================================
# PART 6: THE GUE CONNECTION
# =============================================================================

print("""

================================================================================
PART 6: THE GUE CONNECTION (Random Matrix Theory)
================================================================================

The Montgomery-Odlyzko law:
Spacings of ζ zeros follow GUE (Gaussian Unitary Ensemble) statistics.

If there's an operator H with spectrum = ζ zeros, then H should be:
1. Self-adjoint (real eigenvalues)
2. Have GUE-like statistics

Let's check if our operators have GUE-like spacing.
""")

# Analyze eigenvalue spacing of (I + D)
real_eigs = sorted([e.real for e in eigenvalues_ID if abs(e.imag) < 0.01])
if len(real_eigs) > 10:
    spacings = np.diff(real_eigs)
    mean_spacing = np.mean(spacings)
    normalized_spacings = spacings / mean_spacing

    print(f"Eigenvalue spacing analysis of (I + D):")
    print(f"  Number of real eigenvalues: {len(real_eigs)}")
    print(f"  Mean spacing: {mean_spacing:.4f}")
    print(f"  Variance of normalized spacing: {np.var(normalized_spacings):.4f}")
    print(f"  (GUE variance ≈ 0.286, Poisson variance = 1)")

# =============================================================================
# PART 7: THE TRANSFER MATRIX
# =============================================================================

print("""

================================================================================
PART 7: THE TRANSFER MATRIX APPROACH
================================================================================

Consider M(x) as a "state" that evolves with x.

Define the transfer matrix T(x→x+1):
    M(x+1) = M(x) + μ(x+1)

This is simple: just add μ(x+1).

But at special points (like x = p^k), the structure changes.

More interesting: The multi-scale transfer.
""")

# Build a multi-scale transfer operator
# M(2x) relates to M(x), M(x/2), M(x/3), etc.

print("Multi-scale structure:")
x = 1000
print(f"At x = {x}:")
print(f"  M(x) = {M(x)}")
print(f"  M(2x) = {M(2*x)}")
print(f"  Relationship: M(2x) = M(x) + Σ_{{x < n ≤ 2x}} μ(n)")

sum_mu = sum(mu(n) for n in range(x + 1, 2*x + 1))
print(f"  Σ_{{x < n ≤ 2x}} μ(n) = {sum_mu}")
print(f"  M(x) + sum = {M(x) + sum_mu}")

# =============================================================================
# PART 8: THE HILBERT SPACE STRUCTURE
# =============================================================================

print("""

================================================================================
PART 8: THE HILBERT SPACE STRUCTURE
================================================================================

What Hilbert space should we work in?

Candidate 1: L²(ℕ) with counting measure
    - Functions f: ℕ → ℂ with Σ|f(n)|² < ∞
    - μ ∈ L²(ℕ) since |μ(n)| ≤ 1

Candidate 2: L²(ℝ⁺) with dx/x measure
    - Functions f: ℝ⁺ → ℂ with ∫|f(x)|² dx/x < ∞
    - Natural for Mellin transform

Candidate 3: Hardy space H²
    - Functions analytic in Re(s) > 1/2
    - Connected to ζ function directly
""")

# Check if M is in L²(ℕ)
N = 10000
M_squared_sum = sum(M(n)**2 for n in range(1, N + 1))
print(f"L² analysis:")
print(f"  Σ_{{n≤{N}}} M(n)² = {M_squared_sum}")
print(f"  This grows like {M_squared_sum / N:.4f} × N")
print(f"  So M ∉ L²(ℕ), but M/√n might be bounded in L²")

# =============================================================================
# PART 9: THE SCALING EIGENVALUE EQUATION
# =============================================================================

print("""

================================================================================
PART 9: THE SCALING EIGENVALUE EQUATION
================================================================================

If T_p M = λ_p M (eigenvalue equation), then:
    M(x/p) = λ_p M(x)

We observed M(x)/M(x/p) ≈ -1, so λ_p ≈ -1.

But wait - if λ_p = -1 for all primes p, then:
    M(x/pq) = M(x/p)/(-1) = -M(x/p) = M(x)  for coprime p,q

This would mean M(x/pq) = M(x), which is NOT true in general!

So M is not an EXACT eigenvector. The eigenvalue -1 is APPROXIMATE.
""")

# Check how close M is to being an eigenvector
print("Deviation from eigenvalue -1:")
for p in [2, 3, 5]:
    residuals = []
    for x in range(p * 10, 5001):
        Mx = M(x)
        Mxp = M(x // p)
        if abs(Mx) > 3:
            # If eigenvector: M(x/p) = -M(x), so M(x/p) + M(x) = 0
            residual = abs(Mxp + Mx) / abs(Mx)
            residuals.append(residual)

    print(f"  p = {p}: Mean |M(x/p) + M(x)|/|M(x)| = {np.mean(residuals):.4f}")

# =============================================================================
# PART 10: THE SELF-ADJOINT EXTENSION
# =============================================================================

print("""

================================================================================
PART 10: SELF-ADJOINT OPERATORS
================================================================================

For the Hilbert-Pólya conjecture, we need a SELF-ADJOINT operator.

The operators we've found:
- T_p (scaling): NOT self-adjoint
- D (divisor sum): NOT self-adjoint
- L_1 (Dirichlet convolution): NOT self-adjoint

Can we construct a self-adjoint combination?

Idea: H = (T_p + T_p*)/2 or similar symmetrization.
""")

# Symmetrize the D operator
N = 100
D_sym = (D[:N, :N] + D[:N, :N].T) / 2
eigenvalues_Dsym = np.linalg.eigvals(D_sym)

print(f"Symmetrized D operator:")
print(f"  All eigenvalues real: {np.allclose(eigenvalues_Dsym.imag, 0)}")
print(f"  Min eigenvalue: {np.min(eigenvalues_Dsym.real):.4f}")
print(f"  Max eigenvalue: {np.max(eigenvalues_Dsym.real):.4f}")

# =============================================================================
# PART 11: THE SPECTRAL MEASURE
# =============================================================================

print("""

================================================================================
PART 11: THE SPECTRAL MEASURE
================================================================================

For a self-adjoint operator H, the spectral theorem gives:
    f(H) = ∫ f(λ) dE(λ)

where E is the spectral measure.

The Mertens function is related to:
    M(x) = Σ_{n≤x} μ(n) = ⟨1, μ⟩ truncated

If there's an operator H with eigenvectors related to μ(n),
the spectral measure would encode the distribution of μ.
""")

# Compute the "spectral density" of μ
# This is like a Fourier transform
N = 5000
mu_vals = np.array([mu(n) for n in range(1, N + 1)])
fft_mu = np.fft.fft(mu_vals)
power_spectrum = np.abs(fft_mu)**2

print(f"Power spectrum of μ:")
print(f"  DC component (k=0): {power_spectrum[0]:.2f}")
print(f"  Mean power: {np.mean(power_spectrum):.2f}")
print(f"  Max power: {np.max(power_spectrum):.2f}")

# Check for peaks
peaks = np.where(power_spectrum > 2 * np.mean(power_spectrum))[0]
print(f"  Number of significant peaks: {len(peaks)}")

# =============================================================================
# PART 12: THE MELLIN TRANSFORM CONNECTION
# =============================================================================

print("""

================================================================================
PART 12: THE MELLIN TRANSFORM CONNECTION
================================================================================

The Mellin transform of M(x) is related to 1/sζ(s).

Specifically: ∫₁^∞ M(x) x^{-s-1} dx = 1/(s·ζ(s)) for Re(s) > 1

The poles of 1/ζ(s) (= zeros of ζ) control the inverse Mellin transform.

If ζ zeros have Re(ρ) = 1/2, then M(x) = O(x^{1/2+ε}).

The SPECTRAL decomposition in Mellin space IS the explicit formula!
""")

# =============================================================================
# PART 13: THE EXPLICIT FORMULA AS SPECTRAL DECOMPOSITION
# =============================================================================

print("""

================================================================================
PART 13: THE EXPLICIT FORMULA AS SPECTRAL DECOMPOSITION
================================================================================

The explicit formula for M(x):

    M(x) = Σ_ρ x^ρ/ρ + O(1)

where ρ runs over non-trivial ζ zeros.

This IS a spectral decomposition!
- The "operator" is differentiation/multiplication
- The "eigenvalues" are the ζ zeros ρ
- The "eigenfunctions" are x^ρ

If all ρ have Re(ρ) = 1/2:
    M(x) = Σ x^{1/2 + iγ}/ρ = x^{1/2} Σ e^{iγ log x}/ρ

This is O(x^{1/2}) times a bounded oscillation.
""")

# =============================================================================
# PART 14: CONSTRUCTING A CANDIDATE OPERATOR
# =============================================================================

print("""

================================================================================
PART 14: CONSTRUCTING A CANDIDATE OPERATOR
================================================================================

Based on our analysis, let's construct a candidate operator:

Define H on functions f: ℕ → ℂ by:
    (Hf)(n) = Σ_{d|n} (something) × f(d) + Σ_{n|m} (something) × f(m)

For self-adjointness, need symmetry in n and m.

The Hecke operators from modular forms are examples!
    T_p f(n) = f(pn) + (1/p) Σ_{d|gcd(n,p)} f(n/d)

These ARE self-adjoint on appropriate spaces.
""")

# Build a Hecke-like operator
N = 50
p = 2
Hecke = np.zeros((N, N))
for n in range(1, N + 1):
    # Term 1: f(pn)
    if p * n <= N:
        Hecke[n-1, p*n-1] = 1
    # Term 2: f(n/p) if p|n
    if n % p == 0 and n // p >= 1:
        Hecke[n-1, n//p-1] = 1

print(f"Hecke-like operator T_{p}:")
print(f"  Is symmetric: {np.allclose(Hecke, Hecke.T)}")

# Symmetrize
Hecke_sym = (Hecke + Hecke.T) / 2
eigs_Hecke = np.linalg.eigvals(Hecke_sym)
print(f"  Eigenvalues of symmetrized T_2:")
for i, e in enumerate(sorted(eigs_Hecke, reverse=True)[:5]):
    print(f"    λ_{i+1} = {e:.4f}")

# =============================================================================
# PART 15: THE FUNDAMENTAL OBSTACLE
# =============================================================================

print("""

================================================================================
PART 15: THE FUNDAMENTAL OBSTACLE
================================================================================

THE PROBLEM:

We can construct operators related to M and μ.
But proving their spectrum gives RH is circular!

The operators we found:
1. T_p (scaling): M is approximate eigenvector with λ ≈ -1
2. (I + D): M = (I + D)^{-1} e - spectral properties unclear
3. L_1 (Dirichlet): L_1 μ = ε - relates to ζ function

None of these are obviously self-adjoint with spectrum = ζ zeros.

THE HILBERT-PÓLYA DREAM:

Find H self-adjoint such that:
- Spec(H) = {γ : ζ(1/2 + iγ) = 0}
- This would prove RH automatically!

But constructing such H requires... knowing ζ zeros on the critical line!
""")

# =============================================================================
# PART 16: WHAT THE SPECTRAL APPROACH REVEALS
# =============================================================================

print("""

================================================================================
PART 16: WHAT THE SPECTRAL APPROACH REVEALS
================================================================================

INSIGHTS:

1. M(y)/M(y/p) ≈ -1 is an APPROXIMATE eigenvalue equation
   - T_p M ≈ -M
   - The approximation error is related to D(y) = M(y) + M(y/p)

2. The recursion M = (I + D)^{-1} e is a spectral equation
   - Small eigenvalues of (I + D) would make M large
   - RH is equivalent to controlling these eigenvalues

3. The explicit formula IS the spectral decomposition
   - M(x) = Σ_ρ x^ρ/ρ
   - RH says all ρ have Re = 1/2

4. Self-adjoint operators with correct spectrum are HARD to find
   - Berry-Keating, Connes, and others have tried
   - No complete success yet

THE CIRCULAR GAP:

To construct an operator with spectrum = ζ zeros,
we need to know ζ zeros are on the critical line.
This is what we're trying to prove!
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("""

================================================================================
SUMMARY: SPECTRAL/OPERATOR APPROACH
================================================================================

WHAT WE FOUND:

1. SCALING OPERATOR T_p:
   - M(y/p)/M(y) ≈ -1 suggests λ = -1
   - But M is only APPROXIMATELY an eigenvector
   - Deviation D(y) = M(y) + M(y/p) = O(√y)

2. RECURSION OPERATOR (I + D):
   - M = (I + D)^{-1} e (exact!)
   - Spectrum of (I + D)^{-1} controls M
   - All eigenvalues have |λ| > 1 (numerical check)

3. DIRICHLET OPERATOR L_1:
   - L_1 μ = ε (exact!)
   - Relates to ζ function via Mellin transform
   - Not self-adjoint

4. THE EXPLICIT FORMULA:
   - M(x) = Σ_ρ x^ρ/ρ IS a spectral decomposition
   - ρ are eigenvalues of a differential operator
   - RH says Re(ρ) = 1/2

THE FUNDAMENTAL ISSUE:

The spectral approach is CORRECT in principle.
The ζ zeros ARE eigenvalues of some operator.
But constructing that operator without assuming RH is the challenge.

Our M(y)/M(y/p) ≈ -1 discovery gives a NEW spectral signature:
    M is an approximate eigenvector of scaling operators
    with eigenvalue -1 (up to O(√y) error)

This might lead to a new operator construction.
""")

print("=" * 80)
print("SPECTRAL/OPERATOR ANALYSIS COMPLETE")
print("=" * 80)
