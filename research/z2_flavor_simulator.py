#!/usr/bin/env python3
"""
Z² FRAMEWORK FLAVOR SIMULATOR
=============================
Production-optimized code for computing fermion masses in the 8D warped framework.
Optimized for Apple M4 architecture with vectorized numpy operations.

Structure:
  Module 1: Y-dimension (warp factor) physics engine
  Module 2: T³ torus overlap integration engine
  Module 3: Mass matrix generator and parameter sweep

Carl Zimmerman, April 16, 2026
Z² Framework v5.0.0
"""

import numpy as np
from scipy import integrate, optimize
from scipy.linalg import eigh
from typing import Tuple, List, Optional, Callable
from dataclasses import dataclass
import warnings

# Suppress overflow warnings - we handle them explicitly
warnings.filterwarnings('ignore', category=RuntimeWarning)

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Randall-Sundrum hierarchy solution
K_PI_R5 = 35.0  # kπR₅ ≈ 35 gives hierarchy ~ 10^15

# Higgs VEV
V_HIGGS = 246.0  # GeV

# Electroweak scale
M_EW = 174.0  # GeV (v/√2)

# Standard Model quark masses (GeV) - PDG 2022
# MS-bar at μ = 2 GeV for light quarks, pole mass for top
SM_MASSES = {
    'up': (2.16e-3, 4.67e-3, 0.093, 1.27, 4.18, 172.69),  # u, d, s, c, b, t
    'up_type': np.array([2.16e-3, 1.27, 172.69]),    # u, c, t
    'down_type': np.array([4.67e-3, 0.093, 4.18]),   # d, s, b
    'leptons': np.array([0.511e-3, 0.1057, 1.777]),  # e, μ, τ
}

print("="*70)
print("Z² FRAMEWORK FLAVOR SIMULATOR")
print("Optimized for Apple M4 Architecture")
print("="*70)


# =============================================================================
# MODULE 1: Y-DIMENSION (WARP FACTOR) PHYSICS ENGINE
# =============================================================================

def compute_normalization(c: np.ndarray, k_pi_R: float = K_PI_R5) -> np.ndarray:
    """
    Compute the normalization factor N(c) for fermion profiles.

    The normalization condition is:
        ∫₀^{πR} dy e^{-4ky} |f(y)|² = 1

    For f(y) = N·e^{(1/2-c)ky}, this gives:
        N² ∫₀^{πR} dy e^{-4ky} e^{(1-2c)ky} = 1
        N² ∫₀^{πR} dy e^{-(3+2c-1)ky} = 1
        N² ∫₀^{πR} dy e^{-(2+2c)ky} = 1

    Actually, the standard RS normalization uses the 4D effective action:
        N² = (1-2c)k / (e^{(1-2c)kπR} - 1)  for c < 1/2
        N² = (2c-1)k / (1 - e^{-(2c-1)kπR})  for c > 1/2

    Parameters
    ----------
    c : ndarray
        Bulk mass parameters (can be array for vectorization)
    k_pi_R : float
        Warp factor kπR (default 35)

    Returns
    -------
    N : ndarray
        Normalization factors (same shape as c)

    Notes
    -----
    - Uses log-space arithmetic to avoid overflow
    - Handles c = 1/2 (flat profile) as special case
    """
    c = np.atleast_1d(np.asarray(c, dtype=np.float64))
    N = np.zeros_like(c)

    # Case 1: c < 1/2 (IR-localized, heavy fermions)
    mask_ir = c < 0.5 - 1e-10
    if np.any(mask_ir):
        eps = 0.5 - c[mask_ir]  # eps > 0
        # N² = 2·eps·k / (e^{2·eps·kπR} - 1)
        # In log space to avoid overflow:
        exponent = 2 * eps * k_pi_R
        # For large exponent: N² ≈ 2·eps·k·e^{-2·eps·kπR}
        log_N_sq = np.log(2 * eps) - exponent + np.log(k_pi_R / np.pi)
        # Correction for finite exponent
        log_N_sq = np.where(
            exponent > 50,
            log_N_sq,
            np.log(2 * eps * k_pi_R / np.pi) - np.log(np.exp(exponent) - 1)
        )
        N[mask_ir] = np.exp(0.5 * log_N_sq)

    # Case 2: c > 1/2 (UV-localized, light fermions)
    mask_uv = c > 0.5 + 1e-10
    if np.any(mask_uv):
        eps = c[mask_uv] - 0.5  # eps > 0
        # N² = 2·eps·k / (1 - e^{-2·eps·kπR})
        exponent = 2 * eps * k_pi_R
        # For large exponent: N² ≈ 2·eps·k
        N_sq = (2 * eps * k_pi_R / np.pi) / (1 - np.exp(-exponent))
        N[mask_uv] = np.sqrt(N_sq)

    # Case 3: c ≈ 1/2 (flat profile)
    mask_flat = ~mask_ir & ~mask_uv
    if np.any(mask_flat):
        # Flat profile: N = 1/√(πR)
        N[mask_flat] = np.sqrt(1.0 / np.pi)

    return N


def f_y(y: np.ndarray, c: np.ndarray, k: float = 1.0,
        k_pi_R: float = K_PI_R5) -> np.ndarray:
    """
    Compute fermion profile f(y; c) in the warped 5th dimension.

    f(y) = N(c) · e^{(1/2 - c)·k·y}

    Parameters
    ----------
    y : ndarray
        Position(s) in 5th dimension, range [0, πR]
    c : ndarray
        Bulk mass parameter(s)
    k : float
        AdS curvature scale (set to 1 in units where k=1)
    k_pi_R : float
        Total warp factor kπR

    Returns
    -------
    f : ndarray
        Profile value(s), shape broadcasts (y, c)

    Notes
    -----
    - y and c can be arrays; result broadcasts
    - Uses log-space for numerical stability
    """
    y = np.atleast_1d(np.asarray(y, dtype=np.float64))
    c = np.atleast_1d(np.asarray(c, dtype=np.float64))

    # Get normalization
    N = compute_normalization(c, k_pi_R)

    # Compute profile: f = N · exp((0.5 - c) · k · y)
    # Use broadcasting: y[:, None] vs c[None, :]
    if y.ndim == 1 and c.ndim == 1:
        y = y[:, np.newaxis]
        c = c[np.newaxis, :]
        N = N[np.newaxis, :]

    exponent = (0.5 - c) * k * y

    # Clip exponent to avoid overflow
    exponent = np.clip(exponent, -500, 500)

    return N * np.exp(exponent)


def compute_warped_overlap(c_i: np.ndarray, c_j: np.ndarray,
                           k_pi_R: float = K_PI_R5,
                           beta_H: float = 2.0) -> np.ndarray:
    """
    Compute the warped overlap integral for Yukawa coupling.

    In the standard RS convention, the effective 4D Yukawa is:
        y_ij = Y_5D · √k · F(c_i) · F(c_j)

    where F(c) is the fermion profile value at the IR brane, normalized
    so that F(c=0) = 1 (maximally IR-localized gives O(1) overlap).

    The function F(c) encodes the hierarchy:
        F(c) ≈ √[(1-2c)/(e^{(1-2c)kπR} - 1)] · e^{(1/2-c)kπR}

    For c < 1/2 (IR-localized): F → O(1)
    For c > 1/2 (UV-localized): F → exp(-(c-1/2)kπR) ≪ 1

    Parameters
    ----------
    c_i : ndarray
        Left-handed fermion bulk masses
    c_j : ndarray
        Right-handed fermion bulk masses
    k_pi_R : float
        Warp factor
    beta_H : float
        Higgs bulk mass parameter (2.0 = brane localized)

    Returns
    -------
    I_5D : ndarray
        Overlap integrals, shape (len(c_i), len(c_j))
        Normalized so I(c=0, c=0) = 1

    Notes
    -----
    - This is the RS hierarchy factor that gives m_t/m_u ~ 10^5
    - All arithmetic in log-space to handle exponentials
    """
    c_i = np.atleast_1d(np.asarray(c_i, dtype=np.float64))
    c_j = np.atleast_1d(np.asarray(c_j, dtype=np.float64))

    def F_profile(c):
        """
        Normalized fermion overlap factor at IR brane.

        F(c) = √[(1-2c)/(exp((1-2c)kπR) - 1)] × exp((1/2-c)kπR)

        Normalized so F(c→-∞) → 1 and F(c=1/2) = 1/√(kπR)
        """
        F = np.zeros_like(c)

        # Case c < 1/2 (IR-localized)
        mask_ir = c < 0.5 - 1e-10
        if np.any(mask_ir):
            eps = 0.5 - c[mask_ir]  # eps > 0
            exponent = 2 * eps * k_pi_R
            # In log space for stability
            # F² = (2eps) / (exp(2eps·kπR) - 1) × exp(2eps·kπR)
            #    = (2eps) / (1 - exp(-2eps·kπR))
            F[mask_ir] = np.sqrt(2 * eps / (1 - np.exp(-exponent) + 1e-300))

        # Case c > 1/2 (UV-localized)
        mask_uv = c > 0.5 + 1e-10
        if np.any(mask_uv):
            eps = c[mask_uv] - 0.5  # eps > 0
            exponent = 2 * eps * k_pi_R
            # F² = (2eps) / (exp(2eps·kπR) - 1)
            # For large exponent: F² ≈ 2eps × exp(-2eps·kπR)
            log_F_sq = np.log(2 * eps) - exponent
            # More accurate for smaller exponents
            log_F_sq = np.where(
                exponent > 50,
                log_F_sq,
                np.log(2 * eps) - np.log(np.exp(exponent) - 1)
            )
            F[mask_uv] = np.exp(0.5 * log_F_sq)

        # Case c ≈ 1/2 (flat profile)
        mask_flat = ~mask_ir & ~mask_uv
        if np.any(mask_flat):
            F[mask_flat] = np.sqrt(1.0 / k_pi_R)

        return F

    F_i = F_profile(c_i)
    F_j = F_profile(c_j)

    # Overlap matrix
    I_5D = F_i[:, np.newaxis] * F_j[np.newaxis, :]

    return I_5D


def compute_5D_overlap_numerical(c_L: float, c_R: float,
                                  k_pi_R: float = K_PI_R5,
                                  beta_H: float = 2.0) -> float:
    """
    Numerical integration of 5D overlap (for validation).

    I_5D = ∫₀^{πR} dy e^{-4ky} f_L(y) f_R(y) h(y)

    where h(y) is the Higgs profile (delta function at IR for beta_H=2).
    """
    def integrand(y):
        # Metric warp factor
        warp = np.exp(-4 * y)

        # Fermion profiles (without normalization, add later)
        f_L = np.exp((0.5 - c_L) * y)
        f_R = np.exp((0.5 - c_R) * y)

        # Higgs profile (exponentially localized at IR)
        # For beta_H = 2: h(y) ~ exp((2-beta_H)y) = exp(0) = 1
        h = 1.0

        return warp * f_L * f_R * h

    # Integrate from 0 to kπR
    result, _ = integrate.quad(integrand, 0, k_pi_R, limit=200)

    # Apply normalizations
    N_L = compute_normalization(np.array([c_L]), k_pi_R)[0]
    N_R = compute_normalization(np.array([c_R]), k_pi_R)[0]

    return N_L * N_R * result


# =============================================================================
# MODULE 2: T³ TORUS OVERLAP INTEGRATION ENGINE
# =============================================================================

# The 8 fixed points of T³/Z₂ (cube vertices)
FIXED_POINTS = {
    'v0': np.array([0.0, 0.0, 0.0]),  # Origin
    'v1': np.array([np.pi, 0.0, 0.0]),
    'v2': np.array([0.0, np.pi, 0.0]),
    'v3': np.array([0.0, 0.0, np.pi]),
    'v4': np.array([np.pi, np.pi, 0.0]),
    'v5': np.array([np.pi, 0.0, np.pi]),
    'v6': np.array([0.0, np.pi, np.pi]),
    'v7': np.array([np.pi, np.pi, np.pi]),  # Body diagonal
}

# S₃ orbit assignments
S3_ORBITS = {
    'O0': ['v0'],                    # Singlet (Higgs)
    'O7': ['v7'],                    # Singlet (Gen 3)
    'O1': ['v1', 'v2', 'v3'],        # Triplet (Gen 2)
    'O2': ['v4', 'v5', 'v6'],        # Triplet (Gen 1)
}

# Default generation-to-vertex mapping
GEN_VERTICES = {
    1: 'v4',  # First generation at edge center (lightest)
    2: 'v1',  # Second generation at face center
    3: 'v7',  # Third generation at far corner (heaviest)
}

# Higgs location
HIGGS_VERTEX = 'v0'  # Origin


def torus_distance(theta1: np.ndarray, theta2: np.ndarray) -> float:
    """
    Compute geodesic distance on T³ with periodic boundary conditions.

    Parameters
    ----------
    theta1, theta2 : ndarray (3,)
        Points on the torus, coordinates in [0, 2π)

    Returns
    -------
    d : float
        Geodesic distance
    """
    delta = np.abs(theta1 - theta2)
    # Minimum image convention
    delta = np.minimum(delta, 2*np.pi - delta)
    return np.sqrt(np.sum(delta**2))


def eta_gaussian(theta: np.ndarray, theta_a: np.ndarray,
                 M: float = 1.0) -> float:
    """
    Gaussian-localized wavefunction on T³.

    η_a(θ) = exp(-M/2 · |θ - θ_a|²)

    with periodic boundary conditions.

    Parameters
    ----------
    theta : ndarray (3,)
        Position on torus
    theta_a : ndarray (3,)
        Center of wavefunction (fixed point location)
    M : float
        Flux quantum number (controls localization width)

    Returns
    -------
    eta : float
        Wavefunction amplitude
    """
    d = torus_distance(theta, theta_a)
    return np.exp(-0.5 * M * d**2)


def eta_gaussian_vectorized(theta_grid: np.ndarray, theta_a: np.ndarray,
                            M: float = 1.0) -> np.ndarray:
    """
    Vectorized Gaussian wavefunction for grid evaluation.

    Parameters
    ----------
    theta_grid : ndarray (N, N, N, 3)
        Grid of positions on torus
    theta_a : ndarray (3,)
        Center of wavefunction
    M : float
        Flux quantum

    Returns
    -------
    eta : ndarray (N, N, N)
        Wavefunction values on grid
    """
    # Compute minimum image distance for each grid point
    delta = np.abs(theta_grid - theta_a)
    delta = np.minimum(delta, 2*np.pi - delta)
    d_sq = np.sum(delta**2, axis=-1)

    return np.exp(-0.5 * M * d_sq)


def compute_torus_overlap_grid(theta_i: np.ndarray, theta_j: np.ndarray,
                               theta_H: np.ndarray, M: float = 1.0,
                               n_grid: int = 32) -> float:
    """
    Compute T³ overlap integral using optimized grid summation.

    I_T³ = ∫_{T³} d³θ η_i(θ) η_j(θ) η_H(θ)

    Parameters
    ----------
    theta_i, theta_j : ndarray (3,)
        Fermion fixed point positions
    theta_H : ndarray (3,)
        Higgs fixed point position
    M : float
        Flux quantum
    n_grid : int
        Grid points per dimension

    Returns
    -------
    overlap : float
        Normalized overlap integral

    Notes
    -----
    - Uses numpy broadcasting for M4 optimization
    - Grid method is faster than tplquad for reasonable accuracy
    """
    # Create 3D grid
    theta_1d = np.linspace(0, 2*np.pi, n_grid, endpoint=False)
    dV = (2*np.pi / n_grid)**3

    # Meshgrid with indexing for broadcasting
    t1, t2, t3 = np.meshgrid(theta_1d, theta_1d, theta_1d, indexing='ij')
    theta_grid = np.stack([t1, t2, t3], axis=-1)

    # Compute wavefunctions (vectorized)
    eta_i = eta_gaussian_vectorized(theta_grid, theta_i, M)
    eta_j = eta_gaussian_vectorized(theta_grid, theta_j, M)
    eta_H = eta_gaussian_vectorized(theta_grid, theta_H, M)

    # Overlap integral
    integrand = eta_i * eta_j * eta_H
    integral = np.sum(integrand) * dV

    # Normalization (each wavefunction should integrate to 1)
    norm_i = np.sum(eta_i**2) * dV
    norm_j = np.sum(eta_j**2) * dV
    norm_H = np.sum(eta_H**2) * dV

    # Normalized overlap
    if norm_i > 0 and norm_j > 0 and norm_H > 0:
        return integral / np.sqrt(norm_i * norm_j * norm_H)
    return 0.0


def compute_torus_overlap_analytic(theta_i: np.ndarray, theta_j: np.ndarray,
                                    theta_H: np.ndarray, M: float = 1.0) -> float:
    """
    Analytic approximation for T³ overlap (Gaussian product).

    For well-localized Gaussians, the three-point overlap is:
        Ω ≈ (2π/M)^{3/2} · exp(-M·d²_eff/4)

    where d²_eff is an effective distance combination.

    This is MUCH faster than numerical integration.
    """
    d_iH = torus_distance(theta_i, theta_H)
    d_jH = torus_distance(theta_j, theta_H)
    d_ij = torus_distance(theta_i, theta_j)

    # Three-Gaussian overlap: center of mass calculation
    # Effective distance squared
    d_eff_sq = (d_iH**2 + d_jH**2 + d_ij**2) / 3

    # Prefactor from Gaussian integral
    prefactor = (2*np.pi / M)**(1.5) / (2*np.pi)**3

    # Exponential suppression
    overlap = prefactor * np.exp(-M * d_eff_sq / 4)

    return overlap


def build_torus_overlap_matrix(gen_vertices: dict = None,
                               higgs_vertex: str = None,
                               M: float = 1.0,
                               method: str = 'analytic') -> np.ndarray:
    """
    Build the 3×3 T³ overlap matrix for three generations.

    Parameters
    ----------
    gen_vertices : dict
        Mapping {1: 'v4', 2: 'v1', 3: 'v7'} generation to vertex
    higgs_vertex : str
        Higgs vertex name (default 'v0')
    M : float
        Flux quantum
    method : str
        'analytic' (fast) or 'grid' (accurate)

    Returns
    -------
    Omega : ndarray (3, 3)
        Overlap matrix Ω_ij
    """
    if gen_vertices is None:
        gen_vertices = GEN_VERTICES
    if higgs_vertex is None:
        higgs_vertex = HIGGS_VERTEX

    theta_H = FIXED_POINTS[higgs_vertex]

    Omega = np.zeros((3, 3))

    for i in range(3):
        theta_i = FIXED_POINTS[gen_vertices[i+1]]
        for j in range(3):
            theta_j = FIXED_POINTS[gen_vertices[j+1]]

            if method == 'analytic':
                Omega[i, j] = compute_torus_overlap_analytic(
                    theta_i, theta_j, theta_H, M
                )
            else:
                Omega[i, j] = compute_torus_overlap_grid(
                    theta_i, theta_j, theta_H, M
                )

    return Omega


# =============================================================================
# MODULE 3: MASS MATRIX GENERATOR AND PARAMETER SWEEP
# =============================================================================

def generate_mass_matrix(c_array: np.ndarray,
                         fixed_points: dict,
                         lambda_8: float = 1.0,
                         v: float = V_HIGGS,
                         M_flux: float = 1.0,
                         k_pi_R: float = K_PI_R5) -> np.ndarray:
    """
    Generate the 3×3 fermion mass matrix.

    M_ij = v · λ₈ · I_ij^{(y)} · I_ij^{(θ)}

    Parameters
    ----------
    c_array : ndarray (3,)
        Bulk mass parameters [c₁, c₂, c₃] for generations 1, 2, 3
    fixed_points : dict
        Mapping {1: 'v4', 2: 'v1', 3: 'v7'} of generations to vertices
    lambda_8 : float
        8D Yukawa coupling (O(1) natural value)
    v : float
        Higgs VEV in GeV
    M_flux : float
        Flux quantum for T³ localization
    k_pi_R : float
        Warp factor

    Returns
    -------
    M : ndarray (3, 3)
        Mass matrix in GeV
    """
    c_array = np.atleast_1d(np.asarray(c_array, dtype=np.float64))

    # 5D warped overlap (handles hierarchy)
    I_5D = compute_warped_overlap(c_array, c_array, k_pi_R)

    # T³ overlap (handles flavor structure)
    Omega = build_torus_overlap_matrix(fixed_points, HIGGS_VERTEX, M_flux)

    # Combined mass matrix
    # The exponential hierarchy comes from I_5D
    # The flavor mixing comes from Omega
    M = v * lambda_8 * I_5D * Omega

    return M


def compute_mass_eigenvalues(M: np.ndarray) -> np.ndarray:
    """
    Compute physical mass eigenvalues from mass matrix.

    For Hermitian M†M, eigenvalues are m²_i.

    Parameters
    ----------
    M : ndarray (3, 3)
        Mass matrix

    Returns
    -------
    masses : ndarray (3,)
        Mass eigenvalues in GeV, sorted descending
    """
    # M†M is Hermitian
    MdagM = M.conj().T @ M

    # Eigenvalues are m²
    eigenvalues = np.linalg.eigvalsh(MdagM)

    # Take sqrt for masses, sort descending
    masses = np.sqrt(np.maximum(eigenvalues, 0))
    masses = np.sort(masses)[::-1]

    return masses


def objective_function(c_array: np.ndarray,
                       target_masses: np.ndarray,
                       fixed_points: dict,
                       lambda_8: float = 1.0,
                       fit_overall_scale: bool = True) -> float:
    """
    Objective function for mass fitting.

    Minimizes log-ratio error between predicted and target masses.
    If fit_overall_scale=True, rescales predictions to match heaviest mass.

    Parameters
    ----------
    c_array : ndarray (3,)
        Bulk mass parameters to optimize
    target_masses : ndarray (3,)
        Target SM masses (descending order)
    fixed_points : dict
        Generation-to-vertex mapping
    lambda_8 : float
        8D Yukawa coupling
    fit_overall_scale : bool
        If True, fit lambda_8 to match heaviest mass (scale-free fitting)

    Returns
    -------
    error : float
        Sum of squared log-ratio errors
    """
    try:
        M = generate_mass_matrix(c_array, fixed_points, lambda_8)
        masses = compute_mass_eigenvalues(M)

        # Avoid log(0)
        masses = np.maximum(masses, 1e-20)
        target = np.maximum(target_masses, 1e-20)

        if fit_overall_scale and masses[0] > 1e-20:
            # Rescale to match heaviest mass (this determines lambda_8)
            scale = target[0] / masses[0]
            masses = masses * scale

        # Log-ratio error (scale invariant)
        log_error = np.sum((np.log10(masses) - np.log10(target))**2)

        return log_error

    except Exception:
        return 1e10  # Penalty for failed computation


def search_bulk_masses(target_masses: np.ndarray,
                       fixed_points: dict = None,
                       lambda_8: float = 1.0,
                       c_bounds: Tuple[float, float] = (0.0, 1.0),
                       n_starts: int = 20,
                       verbose: bool = True) -> dict:
    """
    Search for bulk masses {c_i} that reproduce target SM masses.

    Uses scipy.optimize.minimize with multiple random starts.

    Parameters
    ----------
    target_masses : ndarray (3,)
        Target masses [m₃, m₂, m₁] in GeV (heaviest first)
    fixed_points : dict
        Generation-to-vertex mapping
    lambda_8 : float
        8D Yukawa coupling
    c_bounds : tuple
        (min, max) bounds for c_i parameters
    n_starts : int
        Number of random starting points
    verbose : bool
        Print progress

    Returns
    -------
    result : dict
        Best-fit parameters and masses
    """
    if fixed_points is None:
        fixed_points = GEN_VERTICES

    target_masses = np.sort(target_masses)[::-1]  # Ensure descending

    best_result = None
    best_error = np.inf

    bounds = [c_bounds] * 3

    # Physical constraints:
    # Gen 1 (lightest): c > 0.5 → UV-localized
    # Gen 3 (heaviest): c < 0.5 → IR-localized
    # Gen 2 (middle): intermediate
    # ORDERING: c_1 > c_2 > c_3 (lighter = more UV-localized)

    # We'll generate ordered triplets and use penalty for violations
    physical_bounds = [
        (0.55, 0.95),  # Gen 1: UV-localized
        (0.35, 0.65),  # Gen 2: intermediate
        (0.05, 0.45),  # Gen 3: IR-localized
    ]

    for i in range(n_starts):
        # Generate ordered starting point: c1 > c2 > c3
        c_vals = sorted(np.random.uniform(0.1, 0.9, 3), reverse=True)
        # Ensure within physical bounds
        c0 = np.array([
            np.clip(c_vals[0], 0.55, 0.95),  # Gen 1 (lightest)
            np.clip(c_vals[1], 0.35, 0.65),  # Gen 2 (middle)
            np.clip(c_vals[2], 0.05, 0.45),  # Gen 3 (heaviest)
        ])

        try:
            result = optimize.minimize(
                objective_function,
                c0,
                args=(target_masses, fixed_points, lambda_8, True),
                method='L-BFGS-B',
                bounds=physical_bounds,  # Use physical constraints
                options={'maxiter': 500, 'ftol': 1e-10}
            )

            if result.fun < best_error:
                best_error = result.fun
                best_result = result

                if verbose:
                    # Compute predicted masses for display
                    M = generate_mass_matrix(result.x, fixed_points, lambda_8)
                    masses = compute_mass_eigenvalues(M)
                    print(f"\nIteration {i+1}: New best (error = {result.fun:.4f})")
                    print(f"  c = [{result.x[0]:.4f}, {result.x[1]:.4f}, {result.x[2]:.4f}]")
                    print(f"  Predicted: {masses}")
                    print(f"  Target:    {target_masses}")

        except Exception as e:
            if verbose:
                print(f"  Iteration {i+1} failed: {e}")
            continue

    if best_result is None:
        return {'success': False, 'message': 'No solution found'}

    # Final result
    M = generate_mass_matrix(best_result.x, fixed_points, lambda_8)
    masses = compute_mass_eigenvalues(M)

    # Compute fitted lambda_8 (scale factor)
    fitted_lambda_8 = lambda_8 * (target_masses[0] / masses[0]) if masses[0] > 1e-20 else lambda_8
    scaled_masses = masses * (target_masses[0] / masses[0]) if masses[0] > 1e-20 else masses

    return {
        'success': True,
        'c_values': best_result.x,
        'predicted_masses': scaled_masses,
        'raw_masses': masses,
        'target_masses': target_masses,
        'fitted_lambda_8': fitted_lambda_8,
        'error': best_error,
        'optimizer_result': best_result
    }


def grid_search_bulk_masses(target_masses: np.ndarray,
                            fixed_points: dict = None,
                            lambda_8: float = 1.0,
                            n_grid: int = 20,
                            verbose: bool = True) -> dict:
    """
    Grid search over bulk masses (slower but thorough).

    Useful when optimizer gets stuck in local minima.
    """
    if fixed_points is None:
        fixed_points = GEN_VERTICES

    target_masses = np.sort(target_masses)[::-1]

    c_values = np.linspace(0.05, 0.95, n_grid)

    best_error = np.inf
    best_c = None

    total = n_grid**3
    count = 0

    for c1 in c_values:
        for c2 in c_values:
            for c3 in c_values:
                count += 1

                c_array = np.array([c1, c2, c3])
                error = objective_function(c_array, target_masses,
                                          fixed_points, lambda_8)

                if error < best_error:
                    best_error = error
                    best_c = c_array.copy()

                    if verbose and error < 5.0:
                        M = generate_mass_matrix(best_c, fixed_points, lambda_8)
                        masses = compute_mass_eigenvalues(M)
                        print(f"\n[{count}/{total}] New best: error = {error:.4f}")
                        print(f"  c = {best_c}")
                        print(f"  masses = {masses}")

    if best_c is None:
        return {'success': False}

    M = generate_mass_matrix(best_c, fixed_points, lambda_8)
    masses = compute_mass_eigenvalues(M)

    return {
        'success': True,
        'c_values': best_c,
        'predicted_masses': masses,
        'target_masses': target_masses,
        'error': best_error
    }


# =============================================================================
# EXECUTION BLOCK
# =============================================================================

if __name__ == "__main__":

    print("\n" + "="*70)
    print("MODULE 1 TEST: Y-DIMENSION PROFILES")
    print("="*70)

    # Test normalization
    test_c = np.array([0.3, 0.5, 0.7, 0.9])
    N_test = compute_normalization(test_c)
    print(f"\nNormalization N(c) for c = {test_c}:")
    print(f"  N = {N_test}")

    # Test profiles at IR brane
    y_IR = K_PI_R5
    f_IR = f_y(np.array([y_IR]), test_c, k=1.0)
    print(f"\nProfile f(πR) at IR brane:")
    print(f"  f(πR) = {f_IR.flatten()}")

    # Test warped overlap
    I_5D = compute_warped_overlap(test_c, test_c)
    print(f"\nWarped overlap matrix I_5D:")
    print(I_5D)

    print("\n" + "="*70)
    print("MODULE 2 TEST: T³ TORUS OVERLAPS")
    print("="*70)

    # Build overlap matrix
    Omega = build_torus_overlap_matrix(method='analytic')
    print(f"\nT³ overlap matrix Ω (analytic):")
    print(Omega)

    Omega_grid = build_torus_overlap_matrix(method='grid')
    print(f"\nT³ overlap matrix Ω (grid, n=32):")
    print(Omega_grid)

    print("\n" + "="*70)
    print("MODULE 3: SEARCHING FOR UP-TYPE QUARK MASSES")
    print("="*70)

    print(f"\nTarget masses (u, c, t): {SM_MASSES['up_type']} GeV")
    print("Starting parameter sweep...")

    # Search for bulk masses
    result = search_bulk_masses(
        SM_MASSES['up_type'],
        fixed_points=GEN_VERTICES,
        lambda_8=1.0,
        n_starts=30,
        verbose=True
    )

    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)

    if result['success']:
        print(f"\nBest-fit bulk masses:")
        print(f"  c₁ (up)   = {result['c_values'][0]:.6f}")
        print(f"  c₂ (charm)= {result['c_values'][1]:.6f}")
        print(f"  c₃ (top)  = {result['c_values'][2]:.6f}")

        print(f"\nFitted 8D Yukawa coupling:")
        print(f"  λ₈ = {result['fitted_lambda_8']:.4f}")

        print(f"\nPredicted masses (with fitted λ₈):")
        print(f"  m_t = {result['predicted_masses'][0]:.4f} GeV (target: {result['target_masses'][0]:.4f})")
        print(f"  m_c = {result['predicted_masses'][1]:.4f} GeV (target: {result['target_masses'][1]:.4f})")
        print(f"  m_u = {result['predicted_masses'][2]:.6f} GeV (target: {result['target_masses'][2]:.6f})")

        print(f"\nMass ratios (key test of hierarchy):")
        pred_ratios = result['predicted_masses'] / result['predicted_masses'][0]
        targ_ratios = result['target_masses'] / result['target_masses'][0]
        print(f"  m_c/m_t: {pred_ratios[1]:.6f} (target: {targ_ratios[1]:.6f})")
        print(f"  m_u/m_t: {pred_ratios[2]:.2e} (target: {targ_ratios[2]:.2e})")

        print(f"\nLog error: {result['error']:.4f}")

        # Check if bulk masses are close to quantized values
        Z = np.sqrt(32*np.pi/3)
        delta_c = 1/(2*Z)
        print(f"\n--- Quantization Check ---")
        print(f"Δc = 1/(2Z) = {delta_c:.6f}")
        for i, c in enumerate(result['c_values']):
            n = (c - 0.5) / delta_c
            print(f"  c_{i+1} = 0.5 + {n:.2f}·Δc  (nearest integer: {round(n)})")
    else:
        print("\nNo solution found. Try increasing n_starts or grid search.")

    print("\n" + "="*70)
    print("COMPLETE")
    print("="*70)
    print("""
To search other fermion sectors, modify the target masses:

  # Down-type quarks
  result = search_bulk_masses(SM_MASSES['down_type'], n_starts=50)

  # Charged leptons
  result = search_bulk_masses(SM_MASSES['leptons'], n_starts=50)

The hypothesis c_i = 1/2 + n_i/(2Z) is FALSIFIABLE:
  - If integers n_i exist that reproduce SM masses → theory validated
  - If no integers work → quantization hypothesis fails
""")
