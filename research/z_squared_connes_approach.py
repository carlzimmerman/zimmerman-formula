#!/usr/bin/env python3
"""
THE CONNES APPROACH: Noncommutative Geometry and the Riemann Hypothesis
========================================================================

Alain Connes (Fields Medal 1982) developed a sophisticated approach to RH
using noncommutative geometry. This module attempts to understand and
implement key aspects of his framework, incorporating Z².

Key references:
- Connes, "Trace formula in noncommutative geometry and the zeros of the
  Riemann zeta function" (1999)
- Connes & Marcolli, "Noncommutative Geometry, Quantum Fields and Motives" (2008)
- Connes, "An essay on the Riemann Hypothesis" (2015)

Carl Zimmerman, 2026
"""

import numpy as np
from scipy import special, integrate
from scipy.linalg import eigvalsh
from fractions import Fraction
from functools import reduce
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

RIEMANN_ZEROS = [
    14.134725141734693, 21.022039638771555, 25.010857580145688,
    30.424876125859513, 32.935061587739189, 37.586178158825671,
    40.918719012147495, 43.327073280914999, 48.005150881167159,
    49.773832477672302, 52.970321477714460, 56.446247697063394,
]

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

print("=" * 80)
print("THE CONNES APPROACH TO THE RIEMANN HYPOTHESIS")
print("=" * 80)

# =============================================================================
# PART 1: THE ADELES AND IDELES
# =============================================================================

print("""
PART 1: THE ADELES AND IDELES
=============================

Connes' approach uses the ring of ADELES, a fundamental object in number theory.

DEFINITION: The Adeles A_Q

The adeles of Q are the restricted product:

    A_Q = R × ∏'_p Q_p

where:
- R is the real numbers
- Q_p is the p-adic numbers for each prime p
- ∏' means "restricted product": almost all components are in Z_p

An adele is a = (a_∞, a_2, a_3, a_5, ...) where:
- a_∞ ∈ R
- a_p ∈ Q_p for each prime p
- a_p ∈ Z_p for all but finitely many primes

DEFINITION: The Ideles A_Q*

The ideles are the invertible adeles:

    A_Q* = R* × ∏'_p Q_p*

An idele has |a_p|_p = 1 for almost all p.

THE IDELE CLASS GROUP:

    C_Q = A_Q* / Q*

This is the quotient of ideles by the diagonally embedded Q*.
It's a locally compact abelian group.

KEY INSIGHT: The zeros of ζ(s) appear in the spectral analysis of C_Q!
""")


# =============================================================================
# PART 2: THE ABSORPTION SPECTRUM
# =============================================================================

print("""
PART 2: THE ABSORPTION SPECTRUM
===============================

Connes discovered that Riemann zeros appear as an "absorption spectrum."

THE SETUP:
- Consider the Hilbert space H = L²(C_Q) of square-integrable functions on
  the idele class group
- Define the scaling action: for λ ∈ R*₊, (U_λ f)(x) = f(λx)
- The infinitesimal generator D of this action has spectrum related to ζ(s)

THE SPECTRAL PICTURE:

    Full spectrum of D = {ρ - 1/2 : ζ(ρ) = 0} ∪ {continuous spectrum}

The zeros appear as MISSING frequencies (absorption spectrum), not as
eigenvalues directly.

CONNES' TRACE FORMULA:

For suitable test functions h:

    Tr(h(D)) = ∫ h(t) dt + Σ_ρ h(ρ - 1/2) + (other terms)

where the sum is over Riemann zeros ρ.

This is essentially the explicit formula in operator-theoretic language!
""")


# =============================================================================
# PART 3: THE WEIL POSITIVITY CRITERION
# =============================================================================

print("""
PART 3: THE WEIL POSITIVITY CRITERION
=====================================

Connes reformulated RH as a POSITIVITY condition.

WEIL'S EXPLICIT FORMULA:

For a suitable test function f, define:

    W(f) = f̂(0) + f̂(1) - Σ_ρ f̂(ρ) - ∫₀^∞ [f(x) + f(1/x) - 2f(1)] / (x-1) × d*x

where f̂(s) = ∫ f(x) x^(s-1) dx is the Mellin transform.

WEIL POSITIVITY (equivalent to RH):

    W(f * f̃) ≥ 0 for all f

where f̃(x) = f̄(1/x) and * is convolution.

CONNES' INSIGHT:
This positivity is equivalent to the existence of a positive definite
inner product on a certain quotient space, which would imply RH.
""")


def mellin_transform(f, s, x_max=1000, n_points=10000):
    """Compute the Mellin transform f̂(s) = ∫₀^∞ f(x) x^(s-1) dx."""
    x = np.linspace(0.001, x_max, n_points)
    dx = x[1] - x[0]
    integrand = np.array([f(xi) * xi**(s-1) for xi in x])
    return np.trapz(integrand, x)


def weil_functional(f, zeros=RIEMANN_ZEROS[:10]):
    """
    Compute the Weil functional W(f).

    W(f) = f̂(0) + f̂(1) - Σ_ρ f̂(ρ) - (integral term)
    """
    # Mellin transforms at special points
    f_hat_0 = mellin_transform(f, 0.001)  # Regularized at 0
    f_hat_1 = mellin_transform(f, 1)

    # Sum over zeros (using symmetry ρ and 1-ρ)
    zero_sum = 0
    for t in zeros:
        rho = 0.5 + 1j * t
        f_hat_rho = mellin_transform(f, rho)
        f_hat_rho_conj = mellin_transform(f, np.conj(rho))
        zero_sum += (f_hat_rho + f_hat_rho_conj).real

    # Integral term (simplified)
    def integrand(x):
        if abs(x - 1) < 0.01:
            return 0
        return (f(x) + f(1/x) - 2*f(1)) / (x - 1)

    integral_term, _ = integrate.quad(integrand, 0.01, 100, limit=100)

    return f_hat_0 + f_hat_1 - zero_sum - integral_term


# Test Weil functional with a Gaussian
print("    Testing Weil positivity with Gaussian test function...")

def gaussian(x, sigma=1):
    """Gaussian test function."""
    if x <= 0:
        return 0
    return np.exp(-np.log(x)**2 / (2*sigma**2))

def gaussian_convolved(x, sigma=1):
    """f * f̃ for Gaussian (approximately)."""
    if x <= 0:
        return 0
    return np.exp(-np.log(x)**2 / (4*sigma**2))  # Simplified

W_gaussian = weil_functional(gaussian)
W_convolved = weil_functional(gaussian_convolved)

print(f"    W(gaussian) = {W_gaussian:.6f}")
print(f"    W(gaussian * gaussian~) = {W_convolved:.6f}")
print(f"    Is W(f*f~) ≥ 0? {W_convolved >= -0.01}")  # Allow small numerical error


# =============================================================================
# PART 4: THE SEMI-LOCAL TRACE FORMULA
# =============================================================================

print("""
PART 4: THE SEMI-LOCAL TRACE FORMULA
====================================

Connes developed a "semi-local" version restricted to finitely many primes.

For a finite set S of primes, define:

    C_S = ∏_{p ∈ S} Q_p* / Q_S*

where Q_S* = Q* ∩ ∏_{p ∈ S} Z_p*.

THE SEMI-LOCAL TRACE FORMULA:

    Tr_S(h) = Σ_{n coprime to S} Λ(n) h(log n)

where Λ(n) is the von Mangoldt function.

Z² CONNECTION:
    Take S = {primes ≤ Z²} = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}

    This gives a FINITE-DIMENSIONAL approximation to the full trace formula!
""")

primes_to_Z2 = [p for p in PRIMES if p <= Z_SQUARED]
print(f"    Primes up to Z² = {Z_SQUARED:.2f}: {primes_to_Z2}")
print(f"    Number of primes in S: {len(primes_to_Z2)}")


def von_mangoldt(n):
    """Compute the von Mangoldt function Λ(n)."""
    if n <= 1:
        return 0

    # Check if n is a prime power
    for p in PRIMES:
        if p > n:
            break
        k = 1
        pk = p
        while pk <= n:
            if pk == n:
                return np.log(p)
            pk *= p
            k += 1

    return 0


def is_coprime_to_S(n, S):
    """Check if n is coprime to all primes in S."""
    for p in S:
        if n % p == 0:
            return False
    return True


def semi_local_trace(h, S, N_max=1000):
    """Compute the semi-local trace Tr_S(h) = Σ_{n coprime to S} Λ(n) h(log n)."""
    total = 0
    for n in range(2, N_max):
        if is_coprime_to_S(n, S):
            Lambda_n = von_mangoldt(n)
            if Lambda_n > 0:
                total += Lambda_n * h(np.log(n))
    return total


# Test with Gaussian test function
def h_gaussian(t, sigma=5):
    """Gaussian test function on R."""
    return np.exp(-t**2 / (2*sigma**2))

trace_full = semi_local_trace(h_gaussian, [])  # No restriction
trace_Z2 = semi_local_trace(h_gaussian, primes_to_Z2)  # Z² restriction

print(f"\n    Semi-local trace (no restriction): {trace_full:.6f}")
print(f"    Semi-local trace (S = primes ≤ Z²): {trace_Z2:.6f}")
print(f"    Ratio: {trace_Z2 / trace_full:.6f}")


# =============================================================================
# PART 5: THE SCALING OPERATOR
# =============================================================================

print("""
PART 5: THE SCALING OPERATOR AND ITS SPECTRUM
==============================================

The key operator in Connes' approach is the SCALING operator D.

On H = L²(C_Q), the scaling action is:

    (U_λ f)(x) = f(λx) for λ ∈ R*₊

The infinitesimal generator D satisfies:

    U_λ = e^{i (log λ) D}

Formally: D = -i x (d/dx)

THE SPECTRUM:
    The spectrum of D on L²(C_Q) is related to the zeros of ζ(s).

    More precisely, Connes shows that the zeros appear in the
    "absorption spectrum" - frequencies that are MISSING from the
    spectrum due to the quotient by Q*.

To understand this numerically, we work with finite approximations.
""")


def construct_scaling_operator(n_grid, x_min=0.1, x_max=100):
    """
    Construct a finite-dimensional approximation to the scaling operator D.

    D = -i x d/dx

    On a grid, using finite differences.
    """
    # Logarithmic grid (natural for scaling)
    log_x = np.linspace(np.log(x_min), np.log(x_max), n_grid)
    x = np.exp(log_x)
    d_log_x = log_x[1] - log_x[0]

    # D = -i d/d(log x) in log coordinates
    # Using central differences
    D = np.zeros((n_grid, n_grid), dtype=complex)

    for i in range(1, n_grid - 1):
        D[i, i+1] = -1j / (2 * d_log_x)
        D[i, i-1] = 1j / (2 * d_log_x)

    # Boundary conditions (periodic-ish)
    D[0, 1] = -1j / (2 * d_log_x)
    D[0, n_grid-1] = 1j / (2 * d_log_x)
    D[n_grid-1, 0] = -1j / (2 * d_log_x)
    D[n_grid-1, n_grid-2] = 1j / (2 * d_log_x)

    return D, x


print("    Constructing scaling operator D...")
D, x_grid = construct_scaling_operator(200)

# Check if D is Hermitian (should be for real eigenvalues)
is_hermitian = np.allclose(D, D.conj().T)
print(f"    Is D Hermitian? {is_hermitian}")

# Compute eigenvalues
eigenvalues_D = np.linalg.eigvals(D)
eigenvalues_D = np.sort(eigenvalues_D.real)

print(f"    Eigenvalue range: [{eigenvalues_D.min():.4f}, {eigenvalues_D.max():.4f}]")
print(f"    First 10 positive eigenvalues: {eigenvalues_D[eigenvalues_D > 0][:10]}")


# =============================================================================
# PART 6: THE QUOTIENT BY Q*
# =============================================================================

print("""
PART 6: THE QUOTIENT BY Q* - WHERE ZEROS APPEAR
===============================================

The crucial step in Connes' approach is the quotient by Q*.

On A_Q*, the rationals Q* are embedded diagonally:
    q ↦ (q, q, q, q, ...) for q ∈ Q*

The idele class group C_Q = A_Q* / Q* is the quotient.

WHY THIS MATTERS:
    On L²(A_Q*), the spectrum of D is "too big" - it's all of R.

    When we quotient by Q*, we REMOVE certain frequencies.
    These removed frequencies are precisely the Riemann zeros!

ANALOGY:
    Think of a vibrating string. If you add a constraint (like pinning
    a point), certain frequencies are forbidden. The zeros are the
    "forbidden frequencies" when we impose the Q* constraint.

THE MATHEMATICAL STATEMENT:
    Let H₀ = L²(C_Q) and H₁ = L²(A_Q* / Z*).
    There's an exact sequence:

    0 → H₀ → H₁ → (something) → 0

    The zeros of ζ(s) appear in the "boundary" of this sequence.
""")


# =============================================================================
# PART 7: NUMERICAL APPROXIMATION OF THE QUOTIENT
# =============================================================================

print("""
PART 7: NUMERICAL APPROXIMATION OF THE QUOTIENT
===============================================

We cannot directly compute L²(C_Q), but we can approximate the quotient
using the semi-local approach.

IDEA: For S = {primes ≤ Z²}, consider:

    C_S = ∏_{p ∈ S} Q_p* / Q_S*

    This is a FINITE-DIMENSIONAL space!

The dimension is related to the class number and unit group of
the ring Z[1/S] = Z[1/2, 1/3, ..., 1/31].
""")


def construct_semi_local_operator(S, n_grid=50):
    """
    Construct an operator approximating the scaling action on C_S.

    For each prime p in S, we have a Z_p* component.
    The quotient by Q_S* identifies certain points.
    """
    n_primes = len(S)

    # Dimension: roughly ∏_p (p-1) for the units
    dim = 1
    for p in S:
        dim *= (p - 1)

    # This gets large quickly, so we truncate
    dim = min(dim, n_grid)

    # Construct a matrix representing the scaling action
    # This is a simplification - the actual construction is more complex

    # Use the logarithms of primes as a basis
    log_primes = np.array([np.log(p) for p in S])

    # The operator acts by multiplication by log(p) in each direction
    # For simplicity, we construct a direct sum of 1D operators

    H = np.zeros((dim, dim))

    for i, p in enumerate(S[:min(len(S), dim)]):
        for j in range(dim):
            if j < dim - 1:
                H[j, j+1] += np.log(p) / len(S)
            if j > 0:
                H[j, j-1] += np.log(p) / len(S)

    # Symmetrize
    H = (H + H.T) / 2

    return H


print(f"    Constructing semi-local operator for S = primes ≤ Z²...")
H_semi = construct_semi_local_operator(primes_to_Z2, n_grid=50)

eigenvalues_semi = np.linalg.eigvalsh(H_semi)
eigenvalues_semi = np.sort(eigenvalues_semi)[::-1]

print(f"    Dimension: {H_semi.shape[0]}")
print(f"    Eigenvalues (top 10): {eigenvalues_semi[:10]}")


# =============================================================================
# PART 8: THE SPECTRAL REALIZATION
# =============================================================================

print("""
PART 8: THE SPECTRAL REALIZATION
================================

Connes' main theorem connects the spectrum to Riemann zeros.

THEOREM (Connes, 1999):
    There exists a natural action of R*₊ on L²(C_Q) such that the
    spectrum of the infinitesimal generator D, after removing the
    continuous spectrum, consists of the numbers:

    {γ : ζ(1/2 + iγ) = 0}

    in the sense of absorption spectrum.

WHAT THIS MEANS:
    - The "full" spectrum on A_Q* is all of R
    - After quotienting by Q*, certain frequencies are "absorbed"
    - These absorbed frequencies are the imaginary parts of Riemann zeros

WHY THIS DOESN'T IMMEDIATELY PROVE RH:
    The statement is about the LOCATION of absorbed frequencies,
    not about whether all zeros have Re(ρ) = 1/2.

    Connes showed: IF RH is true, THEN the absorption spectrum is as above.

    But he also showed: The absorption spectrum formulation is EQUIVALENT to RH.

    So proving the spectral statement IS proving RH - it's just as hard!
""")


# =============================================================================
# PART 9: THE POSITIVITY CONDITION
# =============================================================================

print("""
PART 9: CONNES' POSITIVITY CONDITION
====================================

Connes reformulated RH as a positivity condition in his framework.

DEFINITION: The Sonin space S
    S consists of functions f on (0, ∞) such that:
    - f is smooth
    - f(x) = O(x^ε) as x → 0 for all ε > 0
    - f(x) = O(x^{-1-ε}) as x → ∞ for all ε > 0

DEFINITION: The quadratic form Q
    For f, g ∈ S:

    Q(f, g) = ∫∫ f(x) g(y) K(x, y) dx dy / (xy)

    where K is a kernel constructed from ζ(s).

CONNES' CRITERION:
    RH is equivalent to: Q(f, f) ≥ 0 for all f ∈ S.

This is similar to Weil's positivity but formulated in Connes' language.
""")


def connes_kernel(x, y, zeros=RIEMANN_ZEROS[:10]):
    """
    Approximate the Connes kernel K(x, y).

    K(x, y) involves a sum over Riemann zeros.
    """
    # Simplified kernel based on the explicit formula
    total = 0

    # Main term
    if x * y > 0:
        total += 1 / max(x, y)

    # Zero contributions
    for t in zeros:
        rho = 0.5 + 1j * t
        # Contribution from ρ and its conjugate
        contrib = ((x * y) ** rho + (x * y) ** np.conj(rho)).real
        total -= contrib / (2 * abs(rho)**2)

    return total


def connes_quadratic_form(f, n_points=100, x_max=10):
    """Compute Q(f, f) using numerical integration."""
    x = np.linspace(0.1, x_max, n_points)
    dx = x[1] - x[0]

    total = 0
    for i, xi in enumerate(x):
        for j, yj in enumerate(x):
            total += f(xi) * f(yj) * connes_kernel(xi, yj) * dx * dx / (xi * yj)

    return total


# Test positivity with a simple test function
def test_function(x):
    """A smooth compactly-supported-ish test function."""
    return np.exp(-x) * x

Q_value = connes_quadratic_form(test_function)
print(f"    Q(f, f) for test function: {Q_value:.6f}")
print(f"    Is Q(f, f) ≥ 0? {Q_value >= -0.01}")


# =============================================================================
# PART 10: THE Z² CUTOFF IN CONNES' FRAMEWORK
# =============================================================================

print("""
PART 10: THE Z² CUTOFF IN CONNES' FRAMEWORK
===========================================

We now incorporate Z² = 32π/3 into Connes' framework.

NATURAL Z² CUTOFF:
    Instead of working with all primes, consider:

    S = {p prime : p ≤ Z²} = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}

    The semi-local space C_S has finite dimension.

Z² SPECTRAL APPROXIMATION:
    The trace formula restricted to S gives:

    Tr_S(h) = Σ_{n: gcd(n, ∏S) = 1} Λ(n) h(log n)

    For n coprime to all primes ≤ Z², the first such n is 37.

OBSERVATION:
    The primes ABOVE Z² are 37, 41, 43, 47, ...
    These are exactly the primes that contribute to the semi-local trace!

    In a sense, Z² divides the primes into:
    - "Small" primes (≤ Z²): Part of the quotient structure
    - "Large" primes (> Z²): Part of the spectral content
""")

# First few integers coprime to all primes ≤ Z²
print("    First integers coprime to all primes ≤ Z²:")
coprime_integers = []
for n in range(2, 200):
    if is_coprime_to_S(n, primes_to_Z2):
        coprime_integers.append(n)
        if len(coprime_integers) >= 15:
            break

print(f"    {coprime_integers}")
print(f"    Note: First one is 37, the first prime > Z² = {Z_SQUARED:.2f}")


# =============================================================================
# PART 11: THE TRACE FORMULA AND ZEROS
# =============================================================================

print("""
PART 11: THE TRACE FORMULA AND ZEROS
====================================

The explicit formula can be written as a trace formula:

    Σ_ρ h(ρ) = h(1) + h(0) - Σ_p Σ_k (log p) h(1/2 + ik log p) / p^{k/2}
              + ∫ h(1/2 + it) Φ(t) dt

where Φ(t) contains the contribution from the pole at s=1.

Z² TRUNCATION:
    If we restrict to primes p ≤ Z², the sum becomes:

    Σ_{p ≤ Z²} Σ_k (log p) h(1/2 + ik log p) / p^{k/2}

    This is a FINITE sum, giving a finite-rank operator.
""")


def truncated_trace_formula(h, cutoff=Z_SQUARED, zeros=RIEMANN_ZEROS[:10]):
    """
    Compute the truncated trace formula:

    Σ_ρ h(ρ) ≈ h(1) + h(0) - Σ_{p ≤ cutoff} Σ_k (log p) h(...) / p^{k/2}
    """
    # h at special points
    result = h(1) + h(0.001)  # Regularize at 0

    # Sum over primes up to cutoff
    prime_sum = 0
    for p in PRIMES:
        if p > cutoff:
            break

        k = 1
        pk_half = np.sqrt(p)
        while pk_half < 1e6:  # Truncate the k sum
            for sign in [1, -1]:
                arg = 0.5 + sign * 1j * k * np.log(p)
                prime_sum += np.log(p) * h(arg).real / pk_half
            pk_half *= np.sqrt(p)
            k += 1

    result -= prime_sum

    # Compare to direct sum over zeros
    zero_sum = sum(h(0.5 + 1j * t) + h(0.5 - 1j * t) for t in zeros).real

    return result, zero_sum


def h_test(s, sigma=5):
    """Test function for trace formula."""
    return np.exp(-(s - 0.5)**2 / (2 * sigma**2))

trace_result, zero_sum = truncated_trace_formula(h_test, cutoff=Z_SQUARED)
print(f"\n    Truncated trace formula result: {trace_result:.6f}")
print(f"    Direct sum over zeros: {zero_sum:.6f}")
print(f"    Difference: {abs(trace_result - zero_sum):.6f}")


# =============================================================================
# PART 12: WHAT CONNES ACTUALLY PROVED
# =============================================================================

print("""
PART 12: WHAT CONNES ACTUALLY PROVED
====================================

Let's be precise about Connes' contributions:

THEOREM 1 (Spectral Realization):
    The imaginary parts of Riemann zeros appear as an absorption spectrum
    of a natural scaling operator on C_Q.

THEOREM 2 (Equivalence):
    RH is EQUIVALENT to a positivity condition for a certain quadratic form.

THEOREM 3 (Semi-local Formula):
    The trace formula can be approximated using finitely many primes.

WHAT CONNES DID NOT PROVE:
    - That the quadratic form IS positive (this would prove RH)
    - That the absorption spectrum is exactly on the line
    - Any direct statement about the location of zeros

WHY CONNES' APPROACH IS VALUABLE:
    1. It REFORMULATES RH in a new language (noncommutative geometry)
    2. It connects RH to spectral theory and operator algebras
    3. It suggests new attack vectors
    4. It makes RH part of a larger theoretical framework

BUT:
    Reformulation ≠ Proof. The hard work of proving positivity remains.
""")


# =============================================================================
# PART 13: Z² AND THE CONNES APPROACH
# =============================================================================

print("""
PART 13: Z² AND THE CONNES APPROACH
===================================

How does Z² = 32π/3 fit into Connes' framework?

OBSERVATION 1: Natural Cutoff
    Z² provides a natural cutoff for the semi-local approach.
    S = {primes ≤ Z²} has exactly 11 elements.

OBSERVATION 2: Bekenstein Connection
    BEKENSTEIN = 3Z²/(8π) = 4 spacetime dimensions.
    The "4" appears naturally in the dimension of spacetime.

OBSERVATION 3: The Number 33
    floor(Z²) = 33, and p₃₃ = 137 ≈ α⁻¹.
    In Connes' framework, 33 might relate to the number of
    "independent directions" in the semi-local space.

SPECULATION:
    Perhaps Z² determines the "right" truncation of the adelic space
    where RH becomes a finite-dimensional positivity check.

    If the positivity condition holds for the Z²-truncated quadratic form,
    and this implies full positivity, we would have a proof.

STATUS:
    This is speculation, not theorem. The connection between Z² and
    Connes' framework needs rigorous development.
""")


# =============================================================================
# PART 14: NUMERICAL CHECKS
# =============================================================================

print("""
PART 14: NUMERICAL CHECKS OF POSITIVITY
=======================================

We numerically check the positivity condition for various test functions.
""")

def check_positivity(f, name, n_points=50, x_max=10):
    """Check if Q(f, f) ≥ 0."""
    Q_val = connes_quadratic_form(f, n_points, x_max)
    status = "✓ POSITIVE" if Q_val >= -0.01 else "✗ NEGATIVE"
    print(f"    {name:30} Q(f,f) = {Q_val:12.6f}  {status}")
    return Q_val >= -0.01

print("\n    Testing positivity for various functions:")
print("    " + "-" * 70)

# Various test functions
test_functions = [
    (lambda x: np.exp(-x), "exp(-x)"),
    (lambda x: np.exp(-x**2), "exp(-x²)"),
    (lambda x: x * np.exp(-x), "x exp(-x)"),
    (lambda x: np.exp(-x) * np.sin(x), "exp(-x) sin(x)"),
    (lambda x: 1 / (1 + x**2), "1/(1+x²)"),
    (lambda x: np.exp(-np.abs(np.log(x))), "exp(-|log x|)"),
]

all_positive = True
for f, name in test_functions:
    result = check_positivity(f, name)
    all_positive = all_positive and result

print("    " + "-" * 70)
print(f"    All test functions positive: {all_positive}")


# =============================================================================
# PART 15: FINAL ASSESSMENT
# =============================================================================

print("""
═══════════════════════════════════════════════════════════════════════════════
PART 15: FINAL ASSESSMENT OF THE CONNES APPROACH
═══════════════════════════════════════════════════════════════════════════════

WHAT THE CONNES APPROACH OFFERS:

1. A beautiful reformulation of RH in terms of:
   - Adelic spaces (A_Q, C_Q)
   - Spectral theory (absorption spectrum)
   - Positivity (quadratic forms)
   - Noncommutative geometry

2. A clear equivalence: RH ⟺ Positivity of Q(f, f)

3. A semi-local approximation using finitely many primes

4. Deep connections to physics (quantum field theory, spectral geometry)

WHAT IT DOESN'T OFFER:

1. A proof of RH
2. An obvious computational approach
3. A simplification of the core difficulty

THE CORE DIFFICULTY:
    Proving Q(f, f) ≥ 0 for all f in the Sonin space.
    This is as hard as proving RH directly.

Z² CONTRIBUTION:
    Z² = 32π/3 provides a natural cutoff:
    - 11 primes ≤ Z²
    - Semi-local space C_S has manageable dimension
    - Trace formula truncates naturally

    But connecting Z² to Connes' positivity condition rigorously
    remains an open problem.

CONCLUSION:
    The Connes approach is the most sophisticated attack on RH.
    It hasn't succeeded, but it provides the deepest mathematical
    framework for understanding the problem.

    Incorporating Z² into this framework is intriguing but incomplete.

═══════════════════════════════════════════════════════════════════════════════

STATUS: The Riemann Hypothesis remains UNPROVEN.

The Connes approach reformulates RH beautifully but doesn't solve it.
Our Z² additions suggest interesting connections but don't close the gap.

The million-dollar problem is still open.

═══════════════════════════════════════════════════════════════════════════════
""")
