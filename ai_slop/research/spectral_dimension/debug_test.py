#!/usr/bin/env python3
"""
Debug test for spectral dimension calculation.
"""

import numpy as np
from scipy import sparse
from scipy.linalg import eigvalsh
import matplotlib.pyplot as plt

# Z² constants
Z_SQUARED = 32 * np.pi / 3
ALPHA_Z2 = 1 / Z_SQUARED

def build_standard_laplacian_3d(L):
    """Standard 3D Laplacian with periodic BC."""
    N = L ** 3

    def idx(x, y, z):
        return x * L * L + y * L + z

    rows, cols, data = [], [], []

    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)

                # Diagonal: -6
                rows.append(i)
                cols.append(i)
                data.append(-6.0)

                # 6 neighbors with periodic BC
                neighbors = [
                    ((x + 1) % L, y, z),
                    ((x - 1) % L, y, z),
                    (x, (y + 1) % L, z),
                    (x, (y - 1) % L, z),
                    (x, y, (z + 1) % L),
                    (x, y, (z - 1) % L),
                ]

                for nx, ny, nz in neighbors:
                    j = idx(nx, ny, nz)
                    rows.append(i)
                    cols.append(j)
                    data.append(1.0)

    return sparse.coo_matrix((data, (rows, cols)), shape=(N, N)).tocsr()


def main():
    L = 8
    N = L**3

    print(f"Building {L}x{L}x{L} Laplacian ({N} sites)...")

    # Build Laplacian
    laplacian = build_standard_laplacian_3d(L)

    # Convert to dense and compute eigenvalues
    L_dense = laplacian.toarray()
    eigenvalues = eigvalsh(L_dense)

    print(f"\nLaplacian eigenvalues:")
    print(f"  Min: {eigenvalues.min():.4f}")
    print(f"  Max: {eigenvalues.max():.4f}")
    print(f"  First 10: {eigenvalues[:10]}")

    # The Laplacian eigenvalues are non-positive
    # For the heat kernel, we use the NEGATIVE Laplacian (positive eigenvalues)
    lambda_pos = -eigenvalues  # Now these are non-negative

    print(f"\nNegative Laplacian eigenvalues (what matters for heat kernel):")
    print(f"  Min: {lambda_pos.min():.4f}")
    print(f"  Max: {lambda_pos.max():.4f}")

    # For 3D lattice with periodic BC:
    # λ(k) = 2(3 - cos(k_x) - cos(k_y) - cos(k_z))
    # Min = 0 at k=0, Max = 12 at k=(π,π,π)

    # Heat kernel: K(t) = Σ exp(-λt)
    t_values = np.logspace(-3, 2, 100)

    K = np.zeros_like(t_values)
    for i, t in enumerate(t_values):
        K[i] = np.sum(np.exp(-lambda_pos * t))

    print(f"\nHeat kernel K(t):")
    print(f"  K(t=0.001) = {K[0]:.4f} (should be ≈ N = {N})")
    print(f"  K(t=100) = {K[-1]:.6f}")

    # For short times, all eigenvalues contribute: K(t→0) → N
    # For long times, only λ=0 contributes: K(t→∞) → (multiplicity of λ=0)

    # Spectral dimension: d_s = -2 d(log K)/d(log t)
    log_t = np.log(t_values)
    log_K = np.log(K)

    # Use central differences for smoother derivative
    d_log_K = np.gradient(log_K, log_t)
    d_s = -2 * d_log_K

    print(f"\nSpectral dimension d_s(t):")
    print(f"  d_s(t=0.001) = {d_s[0]:.4f}")
    print(f"  d_s(t=0.01) = {d_s[10]:.4f}")
    print(f"  d_s(t=0.1) = {d_s[30]:.4f}")
    print(f"  d_s(t=1) = {d_s[50]:.4f}")
    print(f"  d_s(t=10) = {d_s[70]:.4f}")
    print(f"  d_s(t=100) = {d_s[-1]:.4f}")

    # For a standard 3D lattice, d_s should be:
    # - Small t: d_s → 3 (random walk explores 3D)
    # - Large t: d_s → 0 (finite size effects, reaches steady state)

    # The "true" spectral dimension is in the intermediate regime
    # where we see d_s ≈ 3

    # Find the plateau region
    mid_indices = np.where((t_values > 0.01) & (t_values < 10))[0]
    d_s_plateau = d_s[mid_indices]
    print(f"\nPlateau region (0.01 < t < 10):")
    print(f"  Mean d_s = {np.mean(d_s_plateau):.4f}")
    print(f"  Std d_s = {np.std(d_s_plateau):.4f}")

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Heat kernel
    axes[0].loglog(t_values, K)
    axes[0].set_xlabel('t')
    axes[0].set_ylabel('K(t)')
    axes[0].set_title('Heat Kernel')
    axes[0].grid(True, alpha=0.3)

    # Spectral dimension
    axes[1].semilogx(t_values, d_s)
    axes[1].axhline(y=3, color='r', linestyle='--', label='d=3')
    axes[1].axhline(y=2, color='g', linestyle='--', label='d=2')
    axes[1].set_xlabel('t')
    axes[1].set_ylabel('d_s(t)')
    axes[1].set_title('Spectral Dimension')
    axes[1].set_ylim([0, 5])
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Eigenvalue histogram
    axes[2].hist(lambda_pos, bins=30)
    axes[2].set_xlabel('λ')
    axes[2].set_ylabel('Count')
    axes[2].set_title('Eigenvalue Distribution')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('debug_spectral_dimension.png', dpi=150)
    print("\nPlot saved to debug_spectral_dimension.png")
    plt.show()


if __name__ == "__main__":
    main()
