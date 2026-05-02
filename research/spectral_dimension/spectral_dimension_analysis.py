#!/usr/bin/env python3
"""
Spectral Dimension Analysis for Z² Framework

This code properly computes and compares spectral dimensions for:
1. Standard 3D cubic lattice
2. Harper-modified lattice with α = 1/Z²

Key insight: On a finite lattice, spectral dimension varies with diffusion time t:
- t → 0: d_s → 0 (lattice discreteness dominates)
- Intermediate t: d_s ≈ d (true dimension)
- t → ∞: d_s → 0 (finite size dominates)

The Harper modification changes the eigenvalue spectrum, which should show
as a modified spectral dimension curve, especially at intermediate scales.

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
from scipy import sparse
from scipy.linalg import eigvalsh
import matplotlib.pyplot as plt
from typing import Tuple, List

# Z² Framework Constants
Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z = np.sqrt(Z_SQUARED)       # ≈ 5.79
ALPHA_Z2 = 1 / Z_SQUARED     # ≈ 0.0298


def build_laplacian_3d(L: int, alpha: float = 0.0) -> np.ndarray:
    """
    Build 3D Laplacian with optional Harper modification.

    Parameters
    ----------
    L : int
        Lattice size (L×L×L)
    alpha : float
        Harper coupling (0 = standard lattice)

    Returns
    -------
    np.ndarray
        The Laplacian matrix
    """
    N = L ** 3

    def idx(x, y, z):
        return x * L * L + y * L + z

    # Use dense matrix for small lattices
    laplacian = np.zeros((N, N), dtype=complex if alpha != 0 else float)

    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)

                # Diagonal: -6 (coordination number)
                laplacian[i, i] = -6.0

                # X-direction hopping with Harper phase (depends on y)
                nx_plus = (x + 1) % L
                nx_minus = (x - 1) % L
                j_plus = idx(nx_plus, y, z)
                j_minus = idx(nx_minus, y, z)

                if alpha != 0:
                    phase_x = np.exp(2j * np.pi * alpha * y)
                    laplacian[i, j_plus] = phase_x
                    laplacian[i, j_minus] = np.conj(phase_x)
                else:
                    laplacian[i, j_plus] = 1.0
                    laplacian[i, j_minus] = 1.0

                # Y-direction hopping with Harper phase (depends on z)
                ny_plus = (y + 1) % L
                ny_minus = (y - 1) % L
                j_plus = idx(x, ny_plus, z)
                j_minus = idx(x, ny_minus, z)

                if alpha != 0:
                    phase_y = np.exp(2j * np.pi * alpha * z)
                    laplacian[i, j_plus] = phase_y
                    laplacian[i, j_minus] = np.conj(phase_y)
                else:
                    laplacian[i, j_plus] = 1.0
                    laplacian[i, j_minus] = 1.0

                # Z-direction hopping with Harper phase (depends on x)
                nz_plus = (z + 1) % L
                nz_minus = (z - 1) % L
                j_plus = idx(x, y, nz_plus)
                j_minus = idx(x, y, nz_minus)

                if alpha != 0:
                    phase_z = np.exp(2j * np.pi * alpha * x)
                    laplacian[i, j_plus] = phase_z
                    laplacian[i, j_minus] = np.conj(phase_z)
                else:
                    laplacian[i, j_plus] = 1.0
                    laplacian[i, j_minus] = 1.0

    return laplacian


def compute_spectral_dimension(eigenvalues: np.ndarray,
                                t_values: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute heat kernel and spectral dimension.

    The spectral dimension is defined as:
        d_s(t) = -2 × d(log K)/d(log t)

    where K(t) = Tr(exp(-tL)) = Σ exp(-λt)

    Parameters
    ----------
    eigenvalues : np.ndarray
        Eigenvalues of the negative Laplacian (non-negative)
    t_values : np.ndarray
        Diffusion time values

    Returns
    -------
    K : np.ndarray
        Heat kernel values
    d_s : np.ndarray
        Spectral dimension values
    """
    # Heat kernel: K(t) = Σ exp(-λt)
    K = np.zeros(len(t_values))
    for i, t in enumerate(t_values):
        K[i] = np.sum(np.exp(-eigenvalues * t))

    # Spectral dimension: d_s = -2 d(log K)/d(log t)
    log_t = np.log(t_values)
    log_K = np.log(K)

    # Smooth derivative using Savitzky-Golay-like approach
    d_s = np.zeros(len(t_values))
    window = 5

    for i in range(len(t_values)):
        # Local linear fit
        i_min = max(0, i - window)
        i_max = min(len(t_values), i + window + 1)

        if i_max - i_min >= 3:
            coeffs = np.polyfit(log_t[i_min:i_max], log_K[i_min:i_max], 1)
            d_s[i] = -2 * coeffs[0]
        else:
            d_s[i] = np.nan

    return K, d_s


def find_plateau_dimension(t_values: np.ndarray, d_s: np.ndarray,
                           t_min: float = 0.1, t_max: float = 5.0) -> Tuple[float, float]:
    """
    Find the spectral dimension in the plateau region.

    Parameters
    ----------
    t_values : np.ndarray
        Time values
    d_s : np.ndarray
        Spectral dimension values
    t_min, t_max : float
        Plateau region bounds

    Returns
    -------
    mean_d_s : float
        Mean spectral dimension in plateau
    std_d_s : float
        Standard deviation in plateau
    """
    mask = (t_values >= t_min) & (t_values <= t_max)
    plateau_d_s = d_s[mask]
    return np.mean(plateau_d_s), np.std(plateau_d_s)


def analyze_lattice(L: int, alpha: float, name: str) -> dict:
    """
    Complete analysis for one lattice configuration.

    Parameters
    ----------
    L : int
        Lattice size
    alpha : float
        Harper coupling
    name : str
        Label for this configuration

    Returns
    -------
    dict
        Results dictionary
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {name}")
    print(f"  L = {L}, α = {alpha:.6f}")
    print(f"{'='*60}")

    # Build Laplacian
    laplacian = build_laplacian_3d(L, alpha)

    # Make Hermitian and compute eigenvalues
    if np.iscomplexobj(laplacian):
        laplacian = 0.5 * (laplacian + laplacian.conj().T)
        eigenvalues = np.real(eigvalsh(laplacian))
    else:
        eigenvalues = eigvalsh(laplacian)

    # Eigenvalues of Laplacian are ≤ 0; use negative Laplacian
    lambda_pos = -eigenvalues
    lambda_pos = np.maximum(lambda_pos, 0)  # Remove numerical noise

    print(f"  Eigenvalue range: [{lambda_pos.min():.4f}, {lambda_pos.max():.4f}]")

    # Compute spectral dimension
    t_values = np.logspace(-2, 2, 200)
    K, d_s = compute_spectral_dimension(lambda_pos, t_values)

    # Find plateau
    d_s_mean, d_s_std = find_plateau_dimension(t_values, d_s, t_min=0.1, t_max=5.0)
    print(f"  Plateau d_s: {d_s_mean:.3f} ± {d_s_std:.3f}")

    # Find dimension at different scales
    idx_small = np.argmin(np.abs(t_values - 0.05))
    idx_mid = np.argmin(np.abs(t_values - 1.0))
    idx_large = np.argmin(np.abs(t_values - 20.0))

    print(f"  d_s(t=0.05) = {d_s[idx_small]:.3f} (small scale)")
    print(f"  d_s(t=1.0)  = {d_s[idx_mid]:.3f} (intermediate)")
    print(f"  d_s(t=20)   = {d_s[idx_large]:.3f} (large scale)")

    return {
        'name': name,
        'L': L,
        'alpha': alpha,
        'eigenvalues': lambda_pos,
        't_values': t_values,
        'K': K,
        'd_s': d_s,
        'd_s_plateau': d_s_mean,
        'd_s_std': d_s_std
    }


def compare_lattices(L: int = 12):
    """
    Compare standard vs Harper-modified lattices.

    Parameters
    ----------
    L : int
        Lattice size
    """
    print("="*70)
    print("SPECTRAL DIMENSION COMPARISON: Standard vs Harper Lattice")
    print("="*70)
    print(f"Z² = {Z_SQUARED:.4f}, α_Z² = {ALPHA_Z2:.6f}")

    # Run analyses
    results = []

    # Standard lattice
    results.append(analyze_lattice(L, 0.0, "Standard (α=0)"))

    # Harper with Z² coupling
    results.append(analyze_lattice(L, ALPHA_Z2, f"Harper (α=1/Z²={ALPHA_Z2:.4f})"))

    # Harper with other couplings for comparison
    results.append(analyze_lattice(L, 0.1, "Harper (α=0.1)"))
    results.append(analyze_lattice(L, 0.2, "Harper (α=0.2)"))

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"{'Configuration':<30} {'d_s(plateau)':<15} {'d_s(t=0.05)':<15}")
    print("-"*70)

    for r in results:
        idx_small = np.argmin(np.abs(r['t_values'] - 0.05))
        print(f"{r['name']:<30} {r['d_s_plateau']:<15.3f} {r['d_s'][idx_small]:<15.3f}")

    print("-"*70)

    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Spectral dimension vs time
    ax = axes[0, 0]
    for r in results:
        ax.semilogx(r['t_values'], r['d_s'], label=r['name'], linewidth=2)

    ax.axhline(y=3, color='green', linestyle='--', alpha=0.5, label='d=3')
    ax.axhline(y=2, color='red', linestyle='--', alpha=0.5, label='d=2')
    ax.set_xlabel('Diffusion time t', fontsize=12)
    ax.set_ylabel('Spectral dimension d_s(t)', fontsize=12)
    ax.set_title('Spectral Dimension Flow', fontsize=14)
    ax.set_ylim([0, 4])
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 2: Heat kernel
    ax = axes[0, 1]
    for r in results:
        ax.loglog(r['t_values'], r['K'], label=r['name'], linewidth=2)

    ax.set_xlabel('Diffusion time t', fontsize=12)
    ax.set_ylabel('Heat kernel K(t)', fontsize=12)
    ax.set_title('Heat Kernel Trace', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Eigenvalue distributions
    ax = axes[1, 0]
    for r in results:
        ax.hist(r['eigenvalues'], bins=50, alpha=0.5, label=r['name'], density=True)

    ax.set_xlabel('Eigenvalue λ', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('Eigenvalue Distribution', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: Difference from standard
    ax = axes[1, 1]
    standard = results[0]
    for r in results[1:]:
        diff = r['d_s'] - standard['d_s']
        ax.semilogx(r['t_values'], diff, label=f"Δd_s ({r['name']})", linewidth=2)

    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.set_xlabel('Diffusion time t', fontsize=12)
    ax.set_ylabel('Δd_s (Harper - Standard)', fontsize=12)
    ax.set_title('Harper Modification Effect', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('spectral_dimension_comparison.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to spectral_dimension_comparison.png")
    plt.show()

    return results


def size_scaling_analysis(alpha: float = ALPHA_Z2):
    """
    Study how spectral dimension changes with lattice size.

    Parameters
    ----------
    alpha : float
        Harper coupling
    """
    print("\n" + "="*70)
    print("FINITE-SIZE SCALING ANALYSIS")
    print("="*70)

    L_values = [6, 8, 10, 12, 14]
    results = []

    for L in L_values:
        r = analyze_lattice(L, alpha, f"L={L}, α={alpha:.4f}")
        results.append(r)

    # Plot scaling
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Spectral dimension vs time for different L
    ax = axes[0]
    for r in results:
        ax.semilogx(r['t_values'], r['d_s'], label=f"L={r['L']}", linewidth=2)

    ax.axhline(y=3, color='green', linestyle='--', alpha=0.5)
    ax.axhline(y=2, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Diffusion time t')
    ax.set_ylabel('Spectral dimension d_s(t)')
    ax.set_title(f'Finite-Size Scaling (α={alpha:.4f})')
    ax.set_ylim([0, 4])
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plateau dimension vs 1/L
    ax = axes[1]
    L_arr = np.array([r['L'] for r in results])
    d_s_arr = np.array([r['d_s_plateau'] for r in results])
    d_s_std_arr = np.array([r['d_s_std'] for r in results])

    ax.errorbar(1/L_arr, d_s_arr, yerr=d_s_std_arr, fmt='o-', markersize=8, capsize=5)
    ax.axhline(y=3, color='green', linestyle='--', alpha=0.5, label='d=3')

    # Extrapolate to L→∞
    coeffs = np.polyfit(1/L_arr, d_s_arr, 1)
    x_extrap = np.linspace(0, 1/min(L_arr), 50)
    ax.plot(x_extrap, np.polyval(coeffs, x_extrap), 'r--',
            label=f'Extrapolation: d_s(L→∞) = {coeffs[1]:.3f}')

    ax.set_xlabel('1/L')
    ax.set_ylabel('Plateau d_s')
    ax.set_title('Extrapolation to Infinite Volume')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('finite_size_scaling.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to finite_size_scaling.png")
    plt.show()

    print(f"\nExtrapolated d_s(L→∞) = {coeffs[1]:.3f}")

    return results


if __name__ == "__main__":
    # Main comparison
    results = compare_lattices(L=12)

    # Finite-size scaling
    scaling_results = size_scaling_analysis(alpha=ALPHA_Z2)

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("""
Key observations:

1. STANDARD LATTICE: d_s ≈ 3 in plateau region (as expected for 3D)

2. HARPER MODIFICATION: Changes the spectral dimension curve, particularly
   at small and intermediate times. The effect depends on α.

3. FINITE-SIZE EFFECTS: The "true" spectral dimension is only seen in the
   plateau region. At t→0 and t→∞, finite-size effects dominate.

4. UV LIMIT: On a finite lattice, d_s → 0 as t → 0 (not d_s → 2).
   The prediction d_s → 2 at Planck scales is for the continuum limit
   with quantum gravity corrections, not for a classical lattice.

5. HARPER EFFECT: The Z² coupling α = 1/Z² ≈ 0.03 produces subtle
   modifications to the spectral dimension. Whether this approaches
   d_s = 2 in the continuum limit requires further analysis.
""")
