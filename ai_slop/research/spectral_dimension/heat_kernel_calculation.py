#!/usr/bin/env python3
"""
Heat Kernel and Spectral Dimension Calculation for Z² Framework

This code computes the spectral dimension d_s(t) on a Harper-modified
cubic lattice to test the conjecture:

    d_s(x) = 2 + μ(x) = (2 + 3x)/(1 + x)

Which predicts:
    - d_s → 3 in IR (large t, large scales)
    - d_s → 2 in UV (small t, Planck scales)

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh, LinearOperator
from scipy.linalg import eigvalsh
import matplotlib.pyplot as plt
from typing import Tuple, Optional, List
import warnings
from dataclasses import dataclass
from pathlib import Path

# Z² Framework Constants
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z_SQUARED)       # ≈ 5.79
ALPHA_Z2 = 1 / Z_SQUARED     # ≈ 0.0298 (Harper coupling)


@dataclass
class SpectralDimensionResult:
    """Container for spectral dimension calculation results."""
    t_values: np.ndarray
    heat_kernel: np.ndarray
    spectral_dimension: np.ndarray
    eigenvalues: np.ndarray
    lattice_size: int
    alpha: float
    boundary_condition: str

    @property
    def d_s_IR(self) -> float:
        """Spectral dimension in IR limit (large t)."""
        return self.spectral_dimension[-1]

    @property
    def d_s_UV(self) -> float:
        """Spectral dimension in UV limit (small t)."""
        # Average over small-t region to reduce noise
        n_avg = min(5, len(self.spectral_dimension) // 10)
        return np.mean(self.spectral_dimension[:n_avg])


def build_standard_laplacian_3d(L: int, bc: str = 'periodic') -> sparse.csr_matrix:
    """
    Build the standard discrete Laplacian on a 3D cubic lattice.

    Parameters
    ----------
    L : int
        Number of sites per dimension (total N = L³ sites)
    bc : str
        Boundary condition: 'periodic' or 'open'

    Returns
    -------
    sparse.csr_matrix
        The N×N Laplacian matrix in sparse format
    """
    N = L ** 3

    # Helper to convert 3D index to 1D
    def idx(x, y, z):
        return x * L * L + y * L + z

    # Build sparse matrix using COO format (efficient for construction)
    rows = []
    cols = []
    data = []

    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)

                # Diagonal term: -6 (from 6 neighbors in 3D)
                rows.append(i)
                cols.append(i)
                data.append(-6.0)

                # Neighbors in each direction
                neighbors = []

                if bc == 'periodic':
                    neighbors = [
                        ((x + 1) % L, y, z),
                        ((x - 1) % L, y, z),
                        (x, (y + 1) % L, z),
                        (x, (y - 1) % L, z),
                        (x, y, (z + 1) % L),
                        (x, y, (z - 1) % L),
                    ]
                elif bc == 'open':
                    if x + 1 < L: neighbors.append((x + 1, y, z))
                    if x - 1 >= 0: neighbors.append((x - 1, y, z))
                    if y + 1 < L: neighbors.append((x, y + 1, z))
                    if y - 1 >= 0: neighbors.append((x, y - 1, z))
                    if z + 1 < L: neighbors.append((x, y, z + 1))
                    if z - 1 >= 0: neighbors.append((x, y, z - 1))

                    # Adjust diagonal for missing neighbors
                    n_missing = 6 - len(neighbors)
                    if n_missing > 0:
                        data[-1] = -(6 - n_missing)

                for nx, ny, nz in neighbors:
                    j = idx(nx, ny, nz)
                    rows.append(i)
                    cols.append(j)
                    data.append(1.0)

    laplacian = sparse.coo_matrix((data, (rows, cols)), shape=(N, N))
    return laplacian.tocsr()


def build_harper_laplacian_3d(L: int, alpha: float, bc: str = 'periodic') -> sparse.csr_matrix:
    """
    Build Harper-modified Laplacian on a 3D cubic lattice.

    The Harper model adds magnetic phases to hopping terms:
        H = Σ [e^{2πiα·n_perp} c†_{n+μ} c_n + h.c.]

    This creates the Hofstadter butterfly spectrum when α is irrational.

    Parameters
    ----------
    L : int
        Number of sites per dimension
    alpha : float
        Magnetic flux per plaquette (in units of 2π)
        For Z² framework: α = 1/Z² ≈ 0.0298
    bc : str
        Boundary condition: 'periodic' or 'open'

    Returns
    -------
    sparse.csr_matrix
        The Harper-modified Laplacian
    """
    N = L ** 3

    def idx(x, y, z):
        return x * L * L + y * L + z

    rows = []
    cols = []
    data = []

    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)

                # Diagonal term
                rows.append(i)
                cols.append(i)
                data.append(-6.0)

                # X-direction hopping: phase depends on y
                # Peierls phase: exp(2πi α y) for +x hop
                if bc == 'periodic' or x + 1 < L:
                    nx = (x + 1) % L if bc == 'periodic' else x + 1
                    j = idx(nx, y, z)
                    phase = np.exp(2j * np.pi * alpha * y)
                    rows.append(i)
                    cols.append(j)
                    data.append(phase)

                if bc == 'periodic' or x - 1 >= 0:
                    nx = (x - 1) % L if bc == 'periodic' else x - 1
                    j = idx(nx, y, z)
                    phase = np.exp(-2j * np.pi * alpha * y)
                    rows.append(i)
                    cols.append(j)
                    data.append(phase)

                # Y-direction hopping: phase depends on z
                if bc == 'periodic' or y + 1 < L:
                    ny = (y + 1) % L if bc == 'periodic' else y + 1
                    j = idx(x, ny, z)
                    phase = np.exp(2j * np.pi * alpha * z)
                    rows.append(i)
                    cols.append(j)
                    data.append(phase)

                if bc == 'periodic' or y - 1 >= 0:
                    ny = (y - 1) % L if bc == 'periodic' else y - 1
                    j = idx(x, ny, z)
                    phase = np.exp(-2j * np.pi * alpha * z)
                    rows.append(i)
                    cols.append(j)
                    data.append(phase)

                # Z-direction hopping: phase depends on x
                if bc == 'periodic' or z + 1 < L:
                    nz = (z + 1) % L if bc == 'periodic' else z + 1
                    j = idx(x, y, nz)
                    phase = np.exp(2j * np.pi * alpha * x)
                    rows.append(i)
                    cols.append(j)
                    data.append(phase)

                if bc == 'periodic' or z - 1 >= 0:
                    nz = (z - 1) % L if bc == 'periodic' else z - 1
                    j = idx(x, y, nz)
                    phase = np.exp(-2j * np.pi * alpha * x)
                    rows.append(i)
                    cols.append(j)
                    data.append(phase)

                # Adjust diagonal for open BC
                if bc == 'open':
                    n_neighbors = sum([
                        x + 1 < L, x - 1 >= 0,
                        y + 1 < L, y - 1 >= 0,
                        z + 1 < L, z - 1 >= 0
                    ])
                    # Fix diagonal
                    data[len(data) - 1 - (6 - (6 - n_neighbors)) * 2 - n_neighbors] = -float(n_neighbors)

    laplacian = sparse.coo_matrix((data, (rows, cols)), shape=(N, N), dtype=complex)
    return laplacian.tocsr()


def compute_eigenvalues(laplacian: sparse.csr_matrix,
                        n_eigenvalues: Optional[int] = None,
                        use_sparse: bool = True) -> np.ndarray:
    """
    Compute eigenvalues of the Laplacian.

    Parameters
    ----------
    laplacian : sparse.csr_matrix
        The Laplacian matrix
    n_eigenvalues : int, optional
        Number of eigenvalues to compute (for sparse methods)
    use_sparse : bool
        If True, use sparse eigenvalue solver

    Returns
    -------
    np.ndarray
        Sorted eigenvalues (smallest to largest magnitude)
    """
    N = laplacian.shape[0]

    if not use_sparse or N <= 1000:
        # Full diagonalization for small matrices
        # Convert to dense and ensure Hermitian
        L_dense = laplacian.toarray()
        L_hermitian = 0.5 * (L_dense + L_dense.conj().T)
        eigenvalues = eigvalsh(L_hermitian)
    else:
        # Sparse eigenvalue computation
        if n_eigenvalues is None:
            n_eigenvalues = min(N - 2, 500)

        # Get smallest eigenvalues (most important for large t)
        eigenvalues_small, _ = eigsh(laplacian.real, k=n_eigenvalues, which='SM')

        # Get largest eigenvalues (important for small t)
        eigenvalues_large, _ = eigsh(laplacian.real, k=min(100, N - n_eigenvalues - 2), which='LM')

        eigenvalues = np.concatenate([eigenvalues_small, eigenvalues_large])

    # Laplacian eigenvalues should be non-positive; shift to non-negative
    # The negative Laplacian has non-negative eigenvalues
    eigenvalues = -np.sort(eigenvalues)

    # Remove any small negative values from numerical error
    eigenvalues = np.maximum(eigenvalues, 0)

    return eigenvalues


def compute_heat_kernel(eigenvalues: np.ndarray,
                        t_values: np.ndarray) -> np.ndarray:
    """
    Compute heat kernel trace K(t) = Tr(e^{-tL}) = Σ e^{-λt}

    Parameters
    ----------
    eigenvalues : np.ndarray
        Eigenvalues of the (negative) Laplacian
    t_values : np.ndarray
        Time values at which to evaluate K(t)

    Returns
    -------
    np.ndarray
        Heat kernel values K(t)
    """
    # K(t) = Σ_λ exp(-λt)
    # Use broadcasting: eigenvalues[:, None] * t_values[None, :]
    exponents = -np.outer(eigenvalues, t_values)

    # Clip to avoid overflow
    exponents = np.clip(exponents, -700, 700)

    heat_kernel = np.sum(np.exp(exponents), axis=0)

    return heat_kernel


def compute_spectral_dimension(t_values: np.ndarray,
                               heat_kernel: np.ndarray,
                               method: str = 'gradient') -> np.ndarray:
    """
    Compute spectral dimension d_s(t) = -2 × d(log K)/d(log t)

    Parameters
    ----------
    t_values : np.ndarray
        Time values
    heat_kernel : np.ndarray
        Heat kernel K(t)
    method : str
        'gradient' for numpy gradient, 'fit' for local polynomial fit

    Returns
    -------
    np.ndarray
        Spectral dimension d_s(t)
    """
    log_t = np.log(t_values)
    log_K = np.log(heat_kernel)

    if method == 'gradient':
        # Numerical gradient
        d_log_K = np.gradient(log_K, log_t)
        d_s = -2 * d_log_K
    elif method == 'fit':
        # Local polynomial fit for smoother result
        d_s = np.zeros_like(t_values)
        window = 5
        for i in range(len(t_values)):
            i_min = max(0, i - window)
            i_max = min(len(t_values), i + window + 1)
            if i_max - i_min >= 3:
                coeffs = np.polyfit(log_t[i_min:i_max], log_K[i_min:i_max], 1)
                d_s[i] = -2 * coeffs[0]
            else:
                d_s[i] = np.nan
    else:
        raise ValueError(f"Unknown method: {method}")

    return d_s


def run_spectral_dimension_analysis(
    L: int,
    alpha: float = ALPHA_Z2,
    bc: str = 'periodic',
    t_min: float = 0.001,
    t_max: float = 100.0,
    n_t: int = 200,
    use_harper: bool = True,
    verbose: bool = True
) -> SpectralDimensionResult:
    """
    Run complete spectral dimension analysis.

    Parameters
    ----------
    L : int
        Lattice size (L×L×L)
    alpha : float
        Harper coupling (default: 1/Z² ≈ 0.0298)
    bc : str
        Boundary condition
    t_min, t_max : float
        Range of diffusion times
    n_t : int
        Number of time points
    use_harper : bool
        If True, use Harper modification; else standard Laplacian
    verbose : bool
        Print progress

    Returns
    -------
    SpectralDimensionResult
        Container with all results
    """
    N = L ** 3

    if verbose:
        print(f"Building {'Harper' if use_harper else 'standard'} Laplacian...")
        print(f"  Lattice size: {L}×{L}×{L} = {N} sites")
        print(f"  Harper coupling: α = {alpha:.6f}" if use_harper else "  No Harper modification")
        print(f"  Boundary condition: {bc}")

    # Build Laplacian
    if use_harper:
        laplacian = build_harper_laplacian_3d(L, alpha, bc)
    else:
        laplacian = build_standard_laplacian_3d(L, bc)

    if verbose:
        print(f"Computing eigenvalues...")

    # Compute eigenvalues
    use_sparse = N > 1000
    eigenvalues = compute_eigenvalues(laplacian, use_sparse=use_sparse)

    if verbose:
        print(f"  Found {len(eigenvalues)} eigenvalues")
        print(f"  Range: [{eigenvalues.min():.4f}, {eigenvalues.max():.4f}]")

    # Time values (logarithmically spaced)
    t_values = np.logspace(np.log10(t_min), np.log10(t_max), n_t)

    if verbose:
        print(f"Computing heat kernel...")

    # Heat kernel
    heat_kernel = compute_heat_kernel(eigenvalues, t_values)

    if verbose:
        print(f"Computing spectral dimension...")

    # Spectral dimension
    spectral_dimension = compute_spectral_dimension(t_values, heat_kernel, method='gradient')

    # Smooth with moving average to reduce noise
    window = 5
    spectral_dimension_smooth = np.convolve(spectral_dimension,
                                             np.ones(window)/window,
                                             mode='same')

    result = SpectralDimensionResult(
        t_values=t_values,
        heat_kernel=heat_kernel,
        spectral_dimension=spectral_dimension_smooth,
        eigenvalues=eigenvalues,
        lattice_size=L,
        alpha=alpha if use_harper else 0.0,
        boundary_condition=bc
    )

    if verbose:
        print(f"\nResults:")
        print(f"  d_s(IR, t→∞) = {result.d_s_IR:.3f}  (theory: 3.0)")
        print(f"  d_s(UV, t→0) = {result.d_s_UV:.3f}  (theory: 2.0)")

    return result


def plot_results(results: List[SpectralDimensionResult],
                 save_path: Optional[str] = None):
    """
    Plot spectral dimension results.

    Parameters
    ----------
    results : list
        List of SpectralDimensionResult objects
    save_path : str, optional
        Path to save figure
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Heat kernel
    ax1 = axes[0]
    for r in results:
        label = f"L={r.lattice_size}, α={r.alpha:.4f}"
        ax1.loglog(r.t_values, r.heat_kernel, label=label)
    ax1.set_xlabel('Diffusion time t')
    ax1.set_ylabel('Heat kernel K(t)')
    ax1.set_title('Heat Kernel Trace')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Spectral dimension
    ax2 = axes[1]
    for r in results:
        label = f"L={r.lattice_size}, α={r.alpha:.4f}"
        ax2.semilogx(r.t_values, r.spectral_dimension, label=label)

    # Add theoretical predictions
    ax2.axhline(y=3.0, color='green', linestyle='--', alpha=0.7, label='IR limit (d_s=3)')
    ax2.axhline(y=2.0, color='red', linestyle='--', alpha=0.7, label='UV limit (d_s=2)')

    ax2.set_xlabel('Diffusion time t')
    ax2.set_ylabel('Spectral dimension d_s(t)')
    ax2.set_title('Spectral Dimension Flow')
    ax2.set_ylim([0, 4])
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Eigenvalue distribution
    ax3 = axes[2]
    for r in results:
        label = f"L={r.lattice_size}"
        ax3.hist(r.eigenvalues, bins=50, alpha=0.5, label=label, density=True)
    ax3.set_xlabel('Eigenvalue λ')
    ax3.set_ylabel('Density')
    ax3.set_title('Eigenvalue Distribution')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def parameter_sweep(
    L_values: List[int] = [8, 10, 12],
    alpha_values: List[float] = None,
    bc: str = 'periodic',
    verbose: bool = True
) -> dict:
    """
    Run parameter sweep to find optimal Harper coupling.

    Parameters
    ----------
    L_values : list
        Lattice sizes to test
    alpha_values : list
        Harper couplings to test (default: range around 1/Z²)
    bc : str
        Boundary condition
    verbose : bool
        Print progress

    Returns
    -------
    dict
        Results organized by (L, alpha)
    """
    if alpha_values is None:
        # Test range around theoretical value
        alpha_values = [0, 0.01, 0.02, ALPHA_Z2, 0.04, 0.05, 0.1]

    results = {}

    for L in L_values:
        for alpha in alpha_values:
            if verbose:
                print(f"\n{'='*60}")
                print(f"L = {L}, α = {alpha:.4f}")
                print('='*60)

            try:
                result = run_spectral_dimension_analysis(
                    L=L,
                    alpha=alpha,
                    bc=bc,
                    use_harper=(alpha > 0),
                    verbose=verbose
                )
                results[(L, alpha)] = result
            except Exception as e:
                print(f"Error: {e}")
                results[(L, alpha)] = None

    return results


def print_summary_table(results: dict):
    """Print summary table of results."""
    print("\n" + "="*70)
    print("SUMMARY: Spectral Dimension Results")
    print("="*70)
    print(f"{'L':>5} {'α':>10} {'d_s(UV)':>10} {'d_s(IR)':>10} {'UV error':>12}")
    print("-"*70)

    for (L, alpha), result in sorted(results.items()):
        if result is not None:
            uv_error = abs(result.d_s_UV - 2.0) / 2.0 * 100
            print(f"{L:>5} {alpha:>10.4f} {result.d_s_UV:>10.3f} {result.d_s_IR:>10.3f} {uv_error:>11.1f}%")

    print("-"*70)
    print("Theory predictions: d_s(UV) = 2.0, d_s(IR) = 3.0")
    print("="*70)


# =============================================================================
# Main execution
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("Z² Framework: Spectral Dimension Calculation")
    print("="*70)
    print(f"Z² = {Z_SQUARED:.4f}")
    print(f"Z  = {Z:.4f}")
    print(f"Harper coupling α = 1/Z² = {ALPHA_Z2:.6f}")
    print("="*70)

    # Single run with Z² parameters
    print("\n[1] Single run with Z² parameters (L=10)")
    result_z2 = run_spectral_dimension_analysis(L=10, alpha=ALPHA_Z2, use_harper=True)

    # Compare with standard lattice (no Harper)
    print("\n[2] Comparison: Standard lattice (no Harper)")
    result_std = run_spectral_dimension_analysis(L=10, alpha=0, use_harper=False)

    # Parameter sweep
    print("\n[3] Parameter sweep")
    results = parameter_sweep(
        L_values=[8, 10, 12],
        alpha_values=[0, 0.01, 0.02, ALPHA_Z2, 0.04, 0.05, 0.1],
        verbose=True
    )

    # Summary
    print_summary_table(results)

    # Plot
    print("\n[4] Generating plots...")
    plot_results([result_z2, result_std], save_path='spectral_dimension_results.png')

    print("\nDone!")
