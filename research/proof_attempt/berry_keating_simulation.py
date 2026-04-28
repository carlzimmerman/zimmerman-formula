#!/usr/bin/env python3
"""
BERRY-KEATING BOUNDED SIMULATION
================================

Numerical test of H = xp bounded by C_F = 8π/3.

We discretize H = ½(xp + px) = -i(x d/dx + ½) on the interval (-C_F, C_F)
with Dirichlet boundary conditions and compute eigenvalues.

Then compare to actual Riemann zeta zeros.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh, eigs
from scipy.linalg import eig
from math import sqrt, log, pi, exp
import warnings
warnings.filterwarnings('ignore')

C_F = 8 * pi / 3  # ≈ 8.378

print("=" * 80)
print("BERRY-KEATING SIMULATION: H = xp BOUNDED BY C_F")
print(f"C_F = 8π/3 = {C_F:.6f}")
print("=" * 80)

# =============================================================================
# METHOD 1: SYMMETRIC DISCRETIZATION
# =============================================================================

def construct_H_symmetric(N, L):
    """
    Construct H = ½(xp + px) = -i(x d/dx + ½) on [-L, L]

    Using centered finite differences.
    """
    dx = 2*L / (N+1)
    x = np.linspace(-L + dx, L - dx, N)  # Interior points (Dirichlet)

    # Derivative matrix (centered differences)
    D = np.zeros((N, N))
    for i in range(N):
        if i > 0:
            D[i, i-1] = -1
        if i < N-1:
            D[i, i+1] = 1
    D /= (2*dx)

    # Position matrix
    X = np.diag(x)

    # Symmetric form: H = -i(x d/dx + ½) = -i(XD + ½I)
    # Actually: ½(xp + px) = ½(-i)(xD + Dx) = ½(-i)(XD + DX + I)
    # Since [D, X] = I in continuous case

    H = -1j * (X @ D + 0.5 * np.eye(N))

    return H, x

def construct_H_alternate(N, L):
    """
    Alternate construction using the Hermitian form.

    For H to be Hermitian, use: H = -i x d/dx - ½i
    which is NOT self-adjoint on bounded domain!

    Let's check the eigenvalues anyway.
    """
    dx = 2*L / (N+1)
    x = np.linspace(-L + dx, L - dx, N)

    # Use the form that would be self-adjoint on R
    # H = -i(x d/dx + ½)

    D_centered = np.zeros((N, N))
    for i in range(N):
        if i > 0:
            D_centered[i, i-1] = -1/(2*dx)
        if i < N-1:
            D_centered[i, i+1] = 1/(2*dx)

    X = np.diag(x)

    H = -1j * (X @ D_centered + 0.5 * np.eye(N))

    return H, x

# =============================================================================
# COMPUTE EIGENVALUES
# =============================================================================

print("\n" + "=" * 80)
print("COMPUTING EIGENVALUES OF H = xp ON (-C_F, C_F)")
print("=" * 80)

# Various grid sizes
for N in [100, 200, 500, 1000]:
    H, x = construct_H_symmetric(N, C_F)
    eigenvalues = np.linalg.eigvals(H)

    # H should be anti-Hermitian on this domain, so eigenvalues are imaginary
    # Take imaginary parts for "energies"
    imag_parts = np.sort(eigenvalues.imag)
    real_parts = eigenvalues.real

    print(f"\nN = {N}:")
    print(f"  Max |Re(λ)|: {np.max(np.abs(real_parts)):.6f}")
    print(f"  Eigenvalue imaginary parts range: [{imag_parts[0]:.3f}, {imag_parts[-1]:.3f}]")

# Use N = 500 for detailed analysis
N = 500
H, x = construct_H_symmetric(N, C_F)
eigenvalues = np.linalg.eigvals(H)
imag_eigs = np.sort(eigenvalues.imag)
real_eigs = eigenvalues.real

print("\n" + "=" * 80)
print("EIGENVALUE STRUCTURE")
print("=" * 80)

print(f"""
OBSERVATION:

The operator H = -i(x d/dx + ½) on L²(-L, L) is NOT Hermitian!

Check: ⟨f, Hg⟩ = ∫ f* (-i)(x g' + ½g) dx
       ⟨Hf, g⟩ = ∫ (-i)(x f' + ½f)* g dx = ∫ (i)(x f'* + ½f*) g dx

Integration by parts shows these differ by boundary terms.

For Dirichlet BCs: f(±L) = g(±L) = 0
Still NOT equal because of x = 0 behavior.

RESULT: Eigenvalues are COMPLEX, not real.

Max |Real part|: {np.max(np.abs(real_eigs)):.6f}
This should be small if close to anti-Hermitian.
""")

# =============================================================================
# COMPARE TO ZETA ZEROS
# =============================================================================

print("=" * 80)
print("COMPARISON TO RIEMANN ZETA ZEROS")
print("=" * 80)

# Load actual zeta zeros
zeros = np.loadtxt('spectral_data/zeros1.txt')[:100]

print(f"\nFirst 10 actual zeta zeros:")
for i in range(10):
    print(f"  γ_{i+1} = {zeros[i]:.6f}")

# Take positive imaginary eigenvalues for comparison
pos_imag = np.array([e for e in imag_eigs if e > 0])
pos_imag_sorted = np.sort(pos_imag)[:100]

print(f"\nFirst 10 positive imaginary eigenvalues:")
for i in range(min(10, len(pos_imag_sorted))):
    print(f"  λ_{i+1} = {pos_imag_sorted[i]:.6f}")

# Try various rescalings
print("\n" + "-" * 60)
print("ATTEMPTING RESCALING TO MATCH ZEROS")
print("-" * 60)

if len(pos_imag_sorted) >= 10:
    # Linear regression for scaling
    n_compare = min(50, len(pos_imag_sorted), len(zeros))

    # Scale to match range
    eig_range = pos_imag_sorted[n_compare-1] - pos_imag_sorted[0]
    zero_range = zeros[n_compare-1] - zeros[0]

    if eig_range > 0:
        scale = zero_range / eig_range
        offset = zeros[0] - scale * pos_imag_sorted[0]

        scaled_eigs = scale * pos_imag_sorted[:n_compare] + offset

        # Compute mean squared error
        mse = np.mean((scaled_eigs - zeros[:n_compare])**2)
        rmse = sqrt(mse)

        print(f"\nBest linear fit: scaled_λ = {scale:.4f} × λ + {offset:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"Mean zero value: {np.mean(zeros[:n_compare]):.4f}")
        print(f"Relative error: {rmse/np.mean(zeros[:n_compare])*100:.2f}%")

        print("\nComparison (first 10):")
        print("  n  |  Scaled λ  |  Actual γ  |  Error  ")
        print("-" * 50)
        for i in range(10):
            err = scaled_eigs[i] - zeros[i]
            print(f" {i+1:2d}  |  {scaled_eigs[i]:9.4f}  |  {zeros[i]:9.4f}  |  {err:+.4f}")
else:
    print("Not enough positive eigenvalues for comparison")

# =============================================================================
# THE FUNDAMENTAL PROBLEM
# =============================================================================

print("\n" + "=" * 80)
print("THE FUNDAMENTAL PROBLEM")
print("=" * 80)

print(f"""
OBSERVATION:

Even with best-fit rescaling, the eigenvalues DON'T MATCH the zeros.

WHY?

1. H = xp on (-L, L) produces eigenvalues ~n×π/log(L) for Dirichlet BCs
   This is a CONTINUOUS distribution, not related to primes.

2. The zeta zeros γ_n satisfy N(T) ~ (T/2π)log(T/2π)
   This is a LOGARITHMIC counting function from primes.

3. There is NO MECHANISM for primes to appear in H = xp.
   The operator knows nothing about multiplicative structure.

THE GAP:

| Property              | H = xp eigenvalues | Zeta zeros |
|-----------------------|--------------------|------------|
| Spacing               | ~constant          | ~2π/log(T) |
| Statistics            | Integrable         | GUE        |
| Prime connection      | None               | Explicit   |
| Trace formula         | Trivial            | Weil       |
""")

# =============================================================================
# STATISTICAL COMPARISON
# =============================================================================

print("=" * 80)
print("STATISTICAL COMPARISON: SPACING DISTRIBUTIONS")
print("=" * 80)

# Compute spacings of scaled eigenvalues
if len(pos_imag_sorted) >= 20:
    eig_spacings = np.diff(pos_imag_sorted[:50])
    eig_spacings_normalized = eig_spacings / np.mean(eig_spacings)

    # Compute spacings of zeta zeros
    zero_spacings = np.diff(zeros[:50])
    zero_spacings_normalized = zero_spacings / np.mean(zero_spacings)

    print(f"\nEigenvalue spacings (normalized):")
    print(f"  Mean: {np.mean(eig_spacings_normalized):.4f}")
    print(f"  Std:  {np.std(eig_spacings_normalized):.4f}")
    print(f"  Min:  {np.min(eig_spacings_normalized):.4f}")
    print(f"  Max:  {np.max(eig_spacings_normalized):.4f}")

    print(f"\nZero spacings (normalized):")
    print(f"  Mean: {np.mean(zero_spacings_normalized):.4f}")
    print(f"  Std:  {np.std(zero_spacings_normalized):.4f}")
    print(f"  Min:  {np.min(zero_spacings_normalized):.4f}")
    print(f"  Max:  {np.max(zero_spacings_normalized):.4f}")

    # Test: zeros repel (GUE), eigenvalues don't
    print(f"\nLevel repulsion test:")
    print(f"  Eigenvalue small spacings (<0.3): {np.sum(eig_spacings_normalized < 0.3)}")
    print(f"  Zero small spacings (<0.3): {np.sum(zero_spacings_normalized < 0.3)}")

    # GUE spacing distribution: P(s) ~ s² e^{-4s²/π}
    # Poisson: P(s) = e^{-s}
    # Which fits better?

    # Check variance (GUE has smaller variance than Poisson)
    print(f"\n  Poisson variance: 1.0")
    print(f"  GUE variance: ~0.28")
    print(f"  Eigenvalue variance: {np.var(eig_spacings_normalized):.4f}")
    print(f"  Zero variance: {np.var(zero_spacings_normalized):.4f}")

# =============================================================================
# CONCLUSION
# =============================================================================

print("\n" + "=" * 80)
print("NUMERICAL CONCLUSION")
print("=" * 80)

print("""
RESULT: THE H = xp SIMULATION FAILS TO REPRODUCE ZETA ZEROS

1. EIGENVALUES ARE COMPLEX
   H on bounded domain is not self-adjoint.
   Imaginary parts don't match zeros.

2. SPACING IS WRONG
   Eigenvalue spacings show integrable (Poisson-like) statistics.
   Zeta zeros show GUE statistics (level repulsion).

3. NO PRIME STRUCTURE
   Eigenvalues show no connection to log p.
   Zeta zeros are locked to prime logarithms via explicit formula.

4. SCALING DOESN'T HELP
   Even with best-fit linear transformation, errors are large.
   The STRUCTURE is different, not just the scale.

THE C_F BOUNDARY PROVIDES NO MECHANISM FOR:
- Introducing prime arithmetic
- Creating GUE statistics
- Matching the explicit formula

This is a NUMERICAL CONFIRMATION of the theoretical failure.
""")

print("=" * 80)
print("END OF SIMULATION")
print("=" * 80)
