#!/usr/bin/env python3
"""
COMPLETE 8D YUKAWA OVERLAP CALCULATOR
======================================

Implements the full mathematical framework from FLAVOR_SECTOR_COMPLETE.md:

1. S₃ orbit structure: 1 + 1 + 3 + 3 = 8 vertices
2. CIM flux quantization: c_i = 1/2 + n_i/(2Z)
3. Jacobi theta function overlaps on T³
4. Factorized Yukawa: Y_ij = I_5D(c_i, c_j) × Ω_ij

This script provides the tools to FIND the exact integer quantum numbers
{n_i} that reproduce the Standard Model fermion masses.

Carl Zimmerman, April 16, 2026
Z² Framework v5.0.0
"""

import numpy as np
from scipy import integrate, optimize
from scipy.linalg import svd
from scipy.special import jv  # Bessel functions
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass
import itertools

# =============================================================================
# FUNDAMENTAL CONSTANTS FROM Z² FRAMEWORK
# =============================================================================

D = 4                           # Spacetime dimensions
C_F = 8 * np.pi / 3             # Friedmann coefficient
Z_SQUARED = D * C_F             # = 32π/3 ≈ 33.51
Z = np.sqrt(Z_SQUARED)          # ≈ 5.789
N_GEN = 3                       # Generations

# Randall-Sundrum parameters
K_PI_R = 37.0                   # Warp factor for hierarchy

# Flux quantization unit
DELTA_C = 1.0 / (2 * Z)         # ≈ 0.0864 (half of 1/Z for finer resolution)

print(f"Z² Framework Constants:")
print(f"  Z = {Z:.6f}")
print(f"  Δc = 1/(2Z) = {DELTA_C:.6f}")


# =============================================================================
# T³/Z₂ VERTEX STRUCTURE
# =============================================================================

@dataclass
class Vertex:
    """A fixed point on T³/Z₂"""
    index: int
    coords: Tuple[float, float, float]  # (θ¹, θ², θ³) in units of π
    orbit: str

    @property
    def position(self) -> np.ndarray:
        """Position vector in units of π"""
        return np.array(self.coords)


# The 8 vertices of T³/Z₂
VERTICES = [
    Vertex(0, (0, 0, 0), "O0"),      # Origin - singlet
    Vertex(1, (1, 0, 0), "O1"),      # Face centers - triplet 1
    Vertex(2, (0, 1, 0), "O1"),
    Vertex(3, (0, 0, 1), "O1"),
    Vertex(4, (1, 1, 0), "O2"),      # Edge centers - triplet 2
    Vertex(5, (1, 0, 1), "O2"),
    Vertex(6, (0, 1, 1), "O2"),
    Vertex(7, (1, 1, 1), "O7"),      # Far corner - singlet
]

# S₃ orbits
ORBITS = {
    "O0": [VERTICES[0]],            # Origin (Higgs)
    "O7": [VERTICES[7]],            # Far corner (Gen 3)
    "O1": [VERTICES[1], VERTICES[2], VERTICES[3]],  # (Gen 2)
    "O2": [VERTICES[4], VERTICES[5], VERTICES[6]],  # (Gen 1)
}

# Generation assignments (hypothesis)
GEN_VERTICES = {
    3: VERTICES[7],                 # Third generation at far corner
    2: VERTICES[1],                 # Second generation (use first vertex of O1)
    1: VERTICES[4],                 # First generation (use first vertex of O2)
}


# =============================================================================
# GEODESIC DISTANCE ON T³
# =============================================================================

def torus_distance(v1: Vertex, v2: Vertex) -> float:
    """
    Compute geodesic distance between two vertices on T³.

    Distance in units where the torus has period 2π in each direction.
    """
    # Coordinates in units of π
    p1 = v1.position
    p2 = v2.position

    # Minimum image distance (torus periodicity)
    delta = np.abs(p1 - p2)
    delta = np.minimum(delta, 2 - delta)  # Period is 2 (in units of π)

    # Euclidean distance (times π to get actual distance)
    return np.pi * np.linalg.norm(delta)


def print_distance_matrix():
    """Print the geodesic distance matrix between all vertices."""
    print("\nGeodesic Distance Matrix (in units of π):")
    print("    ", end="")
    for j in range(8):
        print(f"  v{j}  ", end="")
    print()

    for i, vi in enumerate(VERTICES):
        print(f"v{i}: ", end="")
        for j, vj in enumerate(VERTICES):
            d = torus_distance(vi, vj) / np.pi
            print(f"{d:5.2f} ", end="")
        print()


# =============================================================================
# JACOBI THETA FUNCTIONS FOR T³ WAVEFUNCTIONS
# =============================================================================

def jacobi_theta_3(z: complex, q: complex, n_terms: int = 50) -> complex:
    """
    Jacobi theta function ϑ₃(z, q) = Σ q^(n²) e^(2inz)

    Parameters
    ----------
    z : complex
        Argument
    q : complex
        Nome, q = exp(iπτ) where τ is the modular parameter
    n_terms : int
        Number of terms in the sum

    Returns
    -------
    theta : complex
        The theta function value
    """
    result = 1.0 + 0j
    for n in range(1, n_terms + 1):
        term = q**(n**2) * (np.exp(2j * n * z) + np.exp(-2j * n * z))
        result += term
    return result


def gaussian_wavefunction(theta: np.ndarray, theta_0: np.ndarray,
                          sigma: float = 0.3) -> float:
    """
    Approximate wavefunction as Gaussian localized at vertex theta_0.

    In the large-flux limit, theta functions become Gaussians.

    Parameters
    ----------
    theta : array (3,)
        Position on T³ (in units of π)
    theta_0 : array (3,)
        Center of wavefunction (vertex position)
    sigma : float
        Width parameter (related to Im(τ))

    Returns
    -------
    psi : float
        Wavefunction amplitude (not normalized)
    """
    # Minimum image on torus
    delta = np.abs(theta - theta_0)
    delta = np.minimum(delta, 2 - delta)

    r_squared = np.sum(delta**2)
    return np.exp(-r_squared / (2 * sigma**2))


# =============================================================================
# T³ OVERLAP INTEGRALS
# =============================================================================

def compute_T3_overlap(v_i: Vertex, v_j: Vertex, v_H: Vertex,
                       sigma: float = 0.3, n_points: int = 20) -> float:
    """
    Compute the T³ overlap integral for Yukawa coupling.

    Ω_ij = ∫_{T³} d³θ ψ_i*(θ) ψ_j(θ) φ_H(θ)

    Parameters
    ----------
    v_i, v_j : Vertex
        Fermion vertices
    v_H : Vertex
        Higgs vertex
    sigma : float
        Wavefunction width
    n_points : int
        Integration grid points per dimension

    Returns
    -------
    overlap : float
        The overlap integral (normalized)
    """
    # Integration grid
    theta_vals = np.linspace(0, 2, n_points)  # [0, 2π]/π

    # Get vertex positions
    pos_i = v_i.position
    pos_j = v_j.position
    pos_H = v_H.position

    # Numerical integration
    integral = 0.0
    norm_i = 0.0
    norm_j = 0.0
    norm_H = 0.0

    dV = (2.0 / n_points)**3  # Volume element

    for t1 in theta_vals:
        for t2 in theta_vals:
            for t3 in theta_vals:
                theta = np.array([t1, t2, t3])

                psi_i = gaussian_wavefunction(theta, pos_i, sigma)
                psi_j = gaussian_wavefunction(theta, pos_j, sigma)
                phi_H = gaussian_wavefunction(theta, pos_H, sigma)

                integral += psi_i * psi_j * phi_H * dV
                norm_i += psi_i**2 * dV
                norm_j += psi_j**2 * dV
                norm_H += phi_H**2 * dV

    # Normalize
    if norm_i > 0 and norm_j > 0 and norm_H > 0:
        return integral / np.sqrt(norm_i * norm_j * norm_H)
    return 0.0


def compute_T3_overlap_analytic(v_i: Vertex, v_j: Vertex, v_H: Vertex,
                                 sigma: float = 0.3) -> float:
    """
    Analytic approximation for T³ overlap (Gaussian case).

    For well-separated Gaussians, the overlap is:
    Ω ≈ exp(-d²/(4σ²)) where d is the mutual distance.
    """
    d_iH = torus_distance(v_i, v_H) / np.pi
    d_jH = torus_distance(v_j, v_H) / np.pi
    d_ij = torus_distance(v_i, v_j) / np.pi

    # Three-point overlap approximation
    # Use geometric mean of pairwise overlaps
    overlap = np.exp(-(d_iH**2 + d_jH**2 + d_ij**2) / (6 * sigma**2))

    return overlap


def build_T3_overlap_matrix(sigma: float = 0.3) -> np.ndarray:
    """
    Build the 3×3 T³ overlap matrix for the three generations.

    Assumes:
    - Higgs at origin O₀
    - Gen 3 at O₇ (far corner)
    - Gen 2 at O₁ (face center)
    - Gen 1 at O₂ (edge center)
    """
    Omega = np.zeros((3, 3))

    v_H = VERTICES[0]  # Higgs at origin
    gen_verts = [GEN_VERTICES[1], GEN_VERTICES[2], GEN_VERTICES[3]]

    for i in range(3):
        for j in range(3):
            Omega[i, j] = compute_T3_overlap_analytic(
                gen_verts[i], gen_verts[j], v_H, sigma
            )

    return Omega


# =============================================================================
# 5D WARPED PROFILES (IMPROVED)
# =============================================================================

def fermion_profile_normalized(y: float, c: float, k: float = 1.0,
                               pi_R: float = K_PI_R) -> float:
    """
    Normalized fermion zero-mode profile in the 5th dimension.

    f(y; c) = √[(1-2c)k / (1 - exp(-(1-2c)kπR))] × exp((1/2 - c)ky)

    For c > 1/2: UV-localized (light)
    For c < 1/2: IR-localized (heavy)
    """
    epsilon = 0.5 - c

    if abs(epsilon) < 1e-10:
        # c = 1/2: flat profile
        return 1.0 / np.sqrt(pi_R)

    # Normalization
    norm_sq = (2 * epsilon * k) / (np.exp(2 * epsilon * k * pi_R) - 1)
    if norm_sq < 0:
        norm_sq = (-2 * epsilon * k) / (1 - np.exp(2 * epsilon * k * pi_R))

    N = np.sqrt(abs(norm_sq))

    return N * np.exp(epsilon * k * y)


def higgs_profile_normalized(y: float, beta: float = 2.0, k: float = 1.0,
                             pi_R: float = K_PI_R) -> float:
    """
    Normalized Higgs profile, IR-localized for β ≈ 2.
    """
    epsilon = 2 - beta

    if abs(epsilon) < 1e-10:
        return 1.0 / np.sqrt(pi_R)

    norm_sq = (2 * epsilon * k) / (np.exp(2 * epsilon * k * pi_R) - 1)
    if norm_sq < 0:
        norm_sq = (-2 * epsilon * k) / (1 - np.exp(2 * epsilon * k * pi_R))

    N = np.sqrt(abs(norm_sq))

    return N * np.exp(epsilon * k * y)


def compute_5D_overlap(c_L: float, c_R: float, beta: float = 2.0,
                       k: float = 1.0, pi_R: float = K_PI_R) -> float:
    """
    Compute the 5D overlap integral numerically.

    I_5D = ∫₀^{πR} dy f_L(y) f_R(y) h(y)
    """
    def integrand(y):
        f_L = fermion_profile_normalized(y, c_L, k, pi_R)
        f_R = fermion_profile_normalized(y, c_R, k, pi_R)
        h = higgs_profile_normalized(y, beta, k, pi_R)
        return f_L * f_R * h

    result, _ = integrate.quad(integrand, 0, pi_R, limit=200)
    return result


# =============================================================================
# FLUX-QUANTIZED BULK MASSES
# =============================================================================

def c_from_quantum_number(n: int) -> float:
    """
    Convert flux quantum number to bulk mass parameter.

    c = 1/2 + n/(2Z)

    n > 0: UV-localized (light)
    n < 0: IR-localized (heavy)
    """
    return 0.5 + n * DELTA_C


def quantum_number_from_c(c: float) -> float:
    """
    Extract the (possibly non-integer) quantum number from bulk mass.

    n = (c - 1/2) × 2Z
    """
    return (c - 0.5) / DELTA_C


# =============================================================================
# COMPLETE YUKAWA MATRIX
# =============================================================================

def compute_yukawa_matrix(n_L: np.ndarray, n_R: np.ndarray,
                          y_5D: float = 1.0, beta: float = 2.0,
                          sigma_T3: float = 0.3) -> np.ndarray:
    """
    Compute the full 3×3 Yukawa matrix.

    Y_ij = y_5D × I_5D(c_L^i, c_R^j) × Ω_ij

    Parameters
    ----------
    n_L : array (3,)
        Flux quantum numbers for left-handed fermions
    n_R : array (3,)
        Flux quantum numbers for right-handed fermions
    y_5D : float
        Fundamental 5D Yukawa coupling
    beta : float
        Higgs bulk mass parameter
    sigma_T3 : float
        T³ wavefunction width

    Returns
    -------
    Y : ndarray (3, 3)
        The Yukawa matrix
    """
    # Convert quantum numbers to bulk masses
    c_L = np.array([c_from_quantum_number(n) for n in n_L])
    c_R = np.array([c_from_quantum_number(n) for n in n_R])

    # 5D overlaps
    I_5D = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            I_5D[i, j] = compute_5D_overlap(c_L[i], c_R[j], beta)

    # T³ overlaps
    Omega = build_T3_overlap_matrix(sigma_T3)

    # Combined Yukawa
    Y = y_5D * I_5D * Omega

    return Y


def diagonalize_yukawa(Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Diagonalize Yukawa matrix to get masses and mixing.

    Y = U · diag(y₁, y₂, y₃) · V†
    """
    U, singular_values, Vh = svd(Y)

    # Sort by mass (descending)
    idx = np.argsort(singular_values)[::-1]
    masses = singular_values[idx]
    U = U[:, idx]
    V = Vh.T[:, idx]

    return masses, U, V


# =============================================================================
# PARAMETER SEARCH
# =============================================================================

def search_quantum_numbers(target_ratios: np.ndarray,
                           n_range: range = range(-6, 7),
                           verbose: bool = True) -> Dict:
    """
    Search for integer quantum numbers that reproduce target mass ratios.

    Parameters
    ----------
    target_ratios : array (3,)
        Target mass ratios [1, m₂/m₁, m₃/m₁] (heaviest = 1)
    n_range : range
        Range of quantum numbers to search
    verbose : bool
        Print progress

    Returns
    -------
    results : dict
        Best-fit parameters and error
    """
    best_error = np.inf
    best_params = None

    # We need 6 quantum numbers: 3 for L, 3 for R
    # Constraint: third generation should be IR-localized (n < 0)

    count = 0
    total = len(n_range)**6

    for n_L in itertools.product(n_range, repeat=3):
        for n_R in itertools.product(n_range, repeat=3):
            count += 1

            # Skip if third gen not IR-localized
            if n_L[2] > 0 or n_R[2] > 0:
                continue

            # Skip if first gen not UV-localized
            if n_L[0] < 0 or n_R[0] < 0:
                continue

            n_L_arr = np.array(n_L)
            n_R_arr = np.array(n_R)

            try:
                Y = compute_yukawa_matrix(n_L_arr, n_R_arr)
                masses, _, _ = diagonalize_yukawa(Y)

                if masses[0] < 1e-20:
                    continue

                ratios = masses / masses[0]
                error = np.sum((np.log10(ratios + 1e-20) -
                               np.log10(target_ratios + 1e-20))**2)

                if error < best_error:
                    best_error = error
                    best_params = {
                        'n_L': n_L_arr.copy(),
                        'n_R': n_R_arr.copy(),
                        'masses': masses.copy(),
                        'ratios': ratios.copy(),
                        'error': error
                    }

                    if verbose:
                        print(f"\nNew best: error = {error:.4f}")
                        print(f"  n_L = {n_L_arr}")
                        print(f"  n_R = {n_R_arr}")
                        print(f"  ratios = {ratios}")

            except Exception:
                continue

    return best_params


# =============================================================================
# OBSERVED MASS RATIOS
# =============================================================================

# Quark masses (PDG 2022, MS-bar at 2 GeV for light quarks)
M_UP = 2.16e-3      # GeV
M_CHARM = 1.27      # GeV
M_TOP = 172.69      # GeV

M_DOWN = 4.67e-3    # GeV
M_STRANGE = 0.093   # GeV
M_BOTTOM = 4.18     # GeV

# Lepton masses
M_ELECTRON = 0.511e-3   # GeV
M_MUON = 0.1057         # GeV
M_TAU = 1.777           # GeV

# Mass ratios (heaviest = 1)
UP_RATIOS = np.array([1.0, M_CHARM/M_TOP, M_UP/M_TOP])
DOWN_RATIOS = np.array([1.0, M_STRANGE/M_BOTTOM, M_DOWN/M_BOTTOM])
LEPTON_RATIOS = np.array([1.0, M_MUON/M_TAU, M_ELECTRON/M_TAU])

print(f"\nTarget mass ratios:")
print(f"  Up-type:    {UP_RATIOS}")
print(f"  Down-type:  {DOWN_RATIOS}")
print(f"  Leptons:    {LEPTON_RATIOS}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPLETE 8D YUKAWA OVERLAP CALCULATOR")
    print("="*70)

    # Print vertex structure
    print("\n" + "="*70)
    print("T³/Z₂ VERTEX STRUCTURE")
    print("="*70)

    print("\nS₃ Orbits:")
    for orbit_name, verts in ORBITS.items():
        coords = [v.coords for v in verts]
        print(f"  {orbit_name}: {coords} (size {len(verts)})")

    print_distance_matrix()

    # Print T³ overlap matrix
    print("\n" + "="*70)
    print("T³ OVERLAP MATRIX (σ = 0.3)")
    print("="*70)

    Omega = build_T3_overlap_matrix(sigma=0.3)
    print("\nΩ_ij (generations 1, 2, 3):")
    print(Omega)

    # Example Yukawa calculation
    print("\n" + "="*70)
    print("EXAMPLE: UP-TYPE YUKAWA MATRIX")
    print("="*70)

    # Hypothesis: quantum numbers for up-type quarks
    n_L_up = np.array([3, 1, -2])   # (u, c, t)_L
    n_R_up = np.array([5, 0, -4])   # (u, c, t)_R

    print(f"\nQuantum numbers (hypothesis):")
    print(f"  n_L = {n_L_up} → c_L = {[c_from_quantum_number(n) for n in n_L_up]}")
    print(f"  n_R = {n_R_up} → c_R = {[c_from_quantum_number(n) for n in n_R_up]}")

    Y_up = compute_yukawa_matrix(n_L_up, n_R_up)
    print(f"\nYukawa matrix Y_u:")
    print(Y_up)

    masses_up, U_up, V_up = diagonalize_yukawa(Y_up)
    print(f"\nMass eigenvalues: {masses_up}")
    print(f"Ratios: {masses_up / masses_up[0]}")
    print(f"Target: {UP_RATIOS}")

    # Search for better quantum numbers
    print("\n" + "="*70)
    print("SEARCHING FOR OPTIMAL QUANTUM NUMBERS")
    print("="*70)
    print("\nSearching up-type quarks...")
    print("(This may take a minute...)")

    # Limited search for demonstration
    best_up = search_quantum_numbers(
        UP_RATIOS,
        n_range=range(-5, 6),
        verbose=True
    )

    if best_up:
        print(f"\n{'='*70}")
        print("BEST FIT FOR UP-TYPE QUARKS")
        print("="*70)
        print(f"n_L = {best_up['n_L']}")
        print(f"n_R = {best_up['n_R']}")
        print(f"Predicted ratios: {best_up['ratios']}")
        print(f"Target ratios:    {UP_RATIOS}")
        print(f"Log error: {best_up['error']:.4f}")

    print("\n" + "="*70)
    print("COMPUTATIONAL FRAMEWORK READY")
    print("="*70)
    print("""
The complete 8D Yukawa framework is now available:

1. T³ vertex structure with S₃ orbits
2. Jacobi theta function overlaps (Gaussian approximation)
3. 5D warped profiles with flux-quantized bulk masses
4. Full Yukawa matrix computation
5. Parameter search for optimal quantum numbers

To find the SM-matching quantum numbers:

  best = search_quantum_numbers(TARGET_RATIOS, n_range=range(-8, 9))

The hypothesis c_i = 1/2 + n_i/(2Z) is FALSIFIABLE:
  - If integers exist → theory is validated
  - If no integers work → quantization hypothesis fails
""")
