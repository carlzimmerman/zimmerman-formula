#!/usr/bin/env python3
"""
YUKAWA OVERLAP INTEGRAL CALCULATOR
===================================

Computes the 3x3 fermion mass matrices from the Z² framework geometry.

The Yukawa couplings arise from overlap integrals in the 8D bulk:

    Y_ij = ∫ dy ∫ d³θ  f_i(y) · f_j(y) · h(y) · Ω_ij(θ)

where:
    - f_i(y; c_i) = fermion profile in 5th dimension (Randall-Sundrum)
    - h(y) = Higgs profile (IR-localized)
    - Ω_ij(θ) = T³ vertex overlap factor (S₃ representation weights)

This script provides the numerical tools to:
    1. Compute the 5D warp factor integrals
    2. Apply the T³ flavor structure from S₃ symmetry
    3. Generate mass matrices for quarks and leptons
    4. Extract CKM and PMNS mixing matrices

Carl Zimmerman, April 16, 2026
Z² Framework v5.0.0
"""

import numpy as np
from scipy import integrate
from scipy.linalg import svd
from typing import Tuple, Dict, List
import warnings

# =============================================================================
# FUNDAMENTAL CONSTANTS FROM Z² FRAMEWORK
# =============================================================================

# Spacetime dimensions
D = 4

# Friedmann coefficient from Einstein's equations
C_F = 8 * np.pi / 3

# The geometric constant
Z_SQUARED = D * C_F  # = 32π/3 ≈ 33.51
Z = np.sqrt(Z_SQUARED)  # ≈ 5.789

# Number of generations (from index theorem)
N_GEN = 3

# Randall-Sundrum parameters (in units where k = 1)
K_PI_R = 37.0  # k·π·R₅ ≈ 37 gives the hierarchy M_Pl/M_weak ~ 10^16


# =============================================================================
# FERMION PROFILES IN THE 5TH DIMENSION
# =============================================================================

def fermion_profile(y: np.ndarray, c: float, k: float = 1.0,
                    pi_R: float = K_PI_R) -> np.ndarray:
    """
    Compute the normalized fermion zero-mode profile in the warped 5th dimension.

    The profile is:
        f(y; c) = N · exp((1/2 - c) k |y|)

    For c > 1/2: UV-localized (light fermion)
    For c < 1/2: IR-localized (heavy fermion)

    Parameters
    ----------
    y : array
        Position in the 5th dimension, y ∈ [0, π·R₅]
    c : float
        Bulk mass parameter (dimensionless, in units of k)
    k : float
        AdS curvature scale (default: 1)
    pi_R : float
        Size of the orbifold interval (default: 37 for realistic hierarchy)

    Returns
    -------
    f : array
        Normalized fermion profile at each y
    """
    exponent = (0.5 - c) * k

    # Compute normalization factor
    if abs(exponent) < 1e-10:
        # c ≈ 1/2: flat profile
        N_squared = 1.0 / pi_R
    else:
        # General case
        N_squared = (2 * exponent * k) / (np.exp(2 * exponent * pi_R) - 1)

    N = np.sqrt(abs(N_squared))

    # Profile
    f = N * np.exp(exponent * np.abs(y))

    return f


def higgs_profile(y: np.ndarray, beta: float = 2.0, k: float = 1.0,
                  pi_R: float = K_PI_R) -> np.ndarray:
    """
    Compute the Higgs profile in the 5th dimension.

    The Higgs is localized near the IR brane (y = π·R):
        h(y) = N_h · exp((2 - β) k |y|)

    For β < 2: IR-localized (standard RS Higgs)

    Parameters
    ----------
    y : array
        Position in 5th dimension
    beta : float
        Higgs bulk mass parameter (default: 2 for IR-localized)
    k : float
        AdS curvature
    pi_R : float
        Orbifold size

    Returns
    -------
    h : array
        Normalized Higgs profile
    """
    exponent = (2 - beta) * k

    if abs(exponent) < 1e-10:
        N_squared = 1.0 / pi_R
    else:
        N_squared = (2 * exponent * k) / (np.exp(2 * exponent * pi_R) - 1)

    N = np.sqrt(abs(N_squared))
    h = N * np.exp(exponent * np.abs(y))

    return h


# =============================================================================
# 5D OVERLAP INTEGRALS
# =============================================================================

def compute_5d_overlap(c_L: float, c_R: float, beta: float = 2.0,
                       k: float = 1.0, pi_R: float = K_PI_R) -> float:
    """
    Compute the 5D Yukawa overlap integral.

    This integrates the product of left-handed fermion, right-handed fermion,
    and Higgs profiles over the 5th dimension:

        I(c_L, c_R) = ∫₀^{πR} dy  f_L(y; c_L) · f_R(y; c_R) · h(y; β)

    Parameters
    ----------
    c_L : float
        Bulk mass of left-handed fermion
    c_R : float
        Bulk mass of right-handed fermion
    beta : float
        Higgs bulk mass parameter
    k : float
        AdS curvature
    pi_R : float
        Orbifold size

    Returns
    -------
    overlap : float
        The dimensionless overlap integral
    """
    def integrand(y):
        f_L = fermion_profile(np.array([y]), c_L, k, pi_R)[0]
        f_R = fermion_profile(np.array([y]), c_R, k, pi_R)[0]
        h = higgs_profile(np.array([y]), beta, k, pi_R)[0]
        return f_L * f_R * h

    # Numerical integration
    result, error = integrate.quad(integrand, 0, pi_R, limit=100)

    return result


def compute_5d_overlap_analytic(c_L: float, c_R: float, beta: float = 2.0,
                                 k: float = 1.0, pi_R: float = K_PI_R) -> float:
    """
    Compute the 5D overlap integral analytically (when possible).

    For the exponential profiles, the overlap can be computed in closed form:

        I = N_L · N_R · N_h · ∫ dy exp(α·y)

    where α = (1/2 - c_L) + (1/2 - c_R) + (2 - β)
    """
    # Combined exponent
    alpha = (0.5 - c_L) + (0.5 - c_R) + (2 - beta)
    alpha *= k

    # Normalization factors
    def get_norm(c, exponent_factor):
        exp = exponent_factor * k
        if abs(exp) < 1e-10:
            return 1.0 / np.sqrt(pi_R)
        else:
            return np.sqrt(abs(2 * exp / (np.exp(2 * exp * pi_R) - 1)))

    N_L = get_norm(c_L, 0.5 - c_L)
    N_R = get_norm(c_R, 0.5 - c_R)
    N_h = get_norm(beta, 2 - beta)

    # Integral of exp(α·y) from 0 to π·R
    if abs(alpha) < 1e-10:
        integral = pi_R
    else:
        integral = (np.exp(alpha * pi_R) - 1) / alpha

    return N_L * N_R * N_h * integral


# =============================================================================
# T³ VERTEX OVERLAP (S₃ FLAVOR STRUCTURE)
# =============================================================================

def get_S3_representation_matrix() -> np.ndarray:
    """
    Return the S₃ representation matrix for 3 generations.

    The 3 generations decompose under S₃ as 3 = 1 ⊕ 2:
        - Gen 1: trivial representation (uniform on all vertices)
        - Gen 2,3: standard 2D representation (orbit-weighted)

    This matrix encodes the T³ overlap factors Ω_ij.

    Returns
    -------
    Omega : ndarray (3, 3)
        The T³ flavor overlap matrix
    """
    # The S₃ Clebsch-Gordan coefficients for 3 = 1 ⊕ 2
    # Normalized so that Σ_i |Ω_αi|² = 1 for each generation α

    # Vertex weights for each generation
    # Gen 1 (trivial): equal weight on all 8 vertices
    w1 = np.ones(8) / np.sqrt(8)

    # Gen 2 (2D rep, x-component): O₃ - O₄ orbit structure
    # O₃ = vertices with one negative: (++-), (+-+), (-++)
    # O₄ = vertices with two negatives: (--+), (-+-), (+--)
    w2 = np.array([0, 1, 1, 0, 1, 0, 0, -1]) / np.sqrt(4)  # Simplified
    w2 = w2 / np.linalg.norm(w2)

    # Gen 3 (2D rep, y-component): body diagonal enhanced
    w3 = np.array([2, 0, 0, -1, 0, -1, -1, 2]) / np.sqrt(12)  # Simplified
    w3 = w3 / np.linalg.norm(w3)

    # Overlap matrix: Ω_ij = Σ_v w_i(v) · w_j(v)
    W = np.array([w1, w2, w3])
    Omega = W @ W.T

    return Omega


def get_T3_overlap_matrix(mixing_angle: float = np.pi/6) -> np.ndarray:
    """
    Compute the T³ overlap matrix with a mixing angle parameter.

    The S₃ structure gives a specific pattern, but small corrections
    from the actual vertex positions modify it.

    Parameters
    ----------
    mixing_angle : float
        Angle parametrizing deviations from pure S₃ (default: π/6)

    Returns
    -------
    Omega : ndarray (3, 3)
        The flavor overlap matrix
    """
    c, s = np.cos(mixing_angle), np.sin(mixing_angle)

    # Base S₃ structure (approximately democratic for Gen 1)
    Omega = np.array([
        [1.0,      c/Z,       s/Z**2],
        [c/Z,      1.0,       c*s/Z],
        [s/Z**2,   c*s/Z,     1.0]
    ])

    return Omega


# =============================================================================
# MASS MATRIX COMPUTATION
# =============================================================================

def compute_mass_matrix(c_L: np.ndarray, c_R: np.ndarray,
                        y_5d: float = 1.0, beta: float = 2.0,
                        use_S3: bool = True) -> np.ndarray:
    """
    Compute the 3x3 fermion mass matrix from overlap integrals.

    M_ij = y_5d · I_5d(c_Li, c_Rj) · Ω_ij · v

    where v is the Higgs VEV (set to 1 in dimensionless units).

    Parameters
    ----------
    c_L : array (3,)
        Bulk masses for left-handed fermions (3 generations)
    c_R : array (3,)
        Bulk masses for right-handed fermions (3 generations)
    y_5d : float
        Fundamental 5D Yukawa coupling
    beta : float
        Higgs bulk mass parameter
    use_S3 : bool
        Whether to include S₃ flavor structure from T³

    Returns
    -------
    M : ndarray (3, 3)
        The mass matrix in generation space
    """
    M = np.zeros((3, 3))

    # Compute 5D overlaps
    for i in range(3):
        for j in range(3):
            M[i, j] = compute_5d_overlap_analytic(c_L[i], c_R[j], beta)

    # Apply T³ flavor structure
    if use_S3:
        Omega = get_T3_overlap_matrix()
        M = M * Omega

    # Apply 5D Yukawa coupling
    M *= y_5d

    return M


def diagonalize_mass_matrix(M: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Diagonalize a mass matrix using SVD.

    M = U · Σ · V†

    The diagonal entries of Σ are the physical masses.
    U and V are the left and right mixing matrices.

    Parameters
    ----------
    M : ndarray (3, 3)
        The mass matrix

    Returns
    -------
    masses : array (3,)
        The physical masses (eigenvalues)
    U : ndarray (3, 3)
        Left mixing matrix
    V : ndarray (3, 3)
        Right mixing matrix
    """
    U, S, Vh = svd(M)

    # Sort by mass (descending: heaviest first)
    idx = np.argsort(S)[::-1]
    masses = S[idx]
    U = U[:, idx]
    V = Vh.T[:, idx]

    return masses, U, V


def compute_CKM_matrix(U_u: np.ndarray, U_d: np.ndarray) -> np.ndarray:
    """
    Compute the CKM matrix from quark mixing matrices.

    V_CKM = U_u† · U_d

    Parameters
    ----------
    U_u : ndarray (3, 3)
        Up-quark left mixing matrix
    U_d : ndarray (3, 3)
        Down-quark left mixing matrix

    Returns
    -------
    V_CKM : ndarray (3, 3)
        The CKM matrix
    """
    return U_u.conj().T @ U_d


def compute_PMNS_matrix(U_e: np.ndarray, U_nu: np.ndarray) -> np.ndarray:
    """
    Compute the PMNS matrix from lepton mixing matrices.

    U_PMNS = U_e† · U_ν

    Parameters
    ----------
    U_e : ndarray (3, 3)
        Charged lepton left mixing matrix
    U_nu : ndarray (3, 3)
        Neutrino left mixing matrix

    Returns
    -------
    U_PMNS : ndarray (3, 3)
        The PMNS matrix
    """
    return U_e.conj().T @ U_nu


# =============================================================================
# Z² FRAMEWORK SPECIFIC: QUANTIZED BULK MASSES
# =============================================================================

def get_quantized_bulk_masses() -> Dict[str, np.ndarray]:
    """
    Return the bulk mass parameters quantized according to the Z² hypothesis.

    Hypothesis: c_i = 1/2 + n_i/Z where n_i ∈ ℤ

    This gives discrete values tied to the geometric constant Z = √(32π/3).

    Returns
    -------
    masses : dict
        Dictionary with bulk masses for each fermion type
    """
    # Quantization unit
    delta_c = 1.0 / Z  # ≈ 0.173

    # Quark bulk masses (hypothesized quantization)
    # Larger |n| → more UV-localized → lighter fermion
    c_quarks_L = np.array([
        0.5 + 2 * delta_c,   # 1st gen (u, d)_L: UV-localized
        0.5 + 1 * delta_c,   # 2nd gen (c, s)_L
        0.5 - 1 * delta_c,   # 3rd gen (t, b)_L: IR-localized
    ])

    c_up_R = np.array([
        0.5 + 3 * delta_c,   # u_R: very UV-localized (light)
        0.5 + 0 * delta_c,   # c_R: boundary
        0.5 - 2 * delta_c,   # t_R: very IR-localized (heavy)
    ])

    c_down_R = np.array([
        0.5 + 2 * delta_c,   # d_R
        0.5 + 1 * delta_c,   # s_R
        0.5 - 1 * delta_c,   # b_R
    ])

    # Lepton bulk masses
    c_leptons_L = np.array([
        0.5 + 3 * delta_c,   # (ν_e, e)_L
        0.5 + 1 * delta_c,   # (ν_μ, μ)_L
        0.5 - 1 * delta_c,   # (ν_τ, τ)_L
    ])

    c_charged_R = np.array([
        0.5 + 4 * delta_c,   # e_R: very light
        0.5 + 1 * delta_c,   # μ_R
        0.5 - 1 * delta_c,   # τ_R
    ])

    return {
        'quarks_L': c_quarks_L,
        'up_R': c_up_R,
        'down_R': c_down_R,
        'leptons_L': c_leptons_L,
        'charged_R': c_charged_R,
    }


# =============================================================================
# PARAMETER SPACE SCANNING
# =============================================================================

def scan_parameter_space(target_masses: np.ndarray,
                         c_range: Tuple[float, float] = (-0.5, 1.5),
                         n_points: int = 20) -> Dict:
    """
    Scan over bulk mass parameters to find values matching target masses.

    Parameters
    ----------
    target_masses : array (3,)
        Target mass ratios (normalized to heaviest = 1)
    c_range : tuple
        Range of bulk masses to scan
    n_points : int
        Number of points per dimension

    Returns
    -------
    results : dict
        Best-fit parameters and achieved masses
    """
    c_values = np.linspace(c_range[0], c_range[1], n_points)

    best_error = np.inf
    best_params = None
    best_masses = None

    # Grid search over c_L values (c_R fixed for simplicity)
    for c1 in c_values:
        for c2 in c_values:
            for c3 in c_values:
                c_L = np.array([c1, c2, c3])
                c_R = c_L  # Simplification: c_L = c_R

                M = compute_mass_matrix(c_L, c_R, y_5d=1.0, use_S3=True)
                masses, _, _ = diagonalize_mass_matrix(M)

                # Normalize to heaviest
                masses_norm = masses / masses[0]

                # Compute error
                error = np.sum((masses_norm - target_masses)**2)

                if error < best_error:
                    best_error = error
                    best_params = (c_L.copy(), c_R.copy())
                    best_masses = masses_norm.copy()

    return {
        'c_L': best_params[0],
        'c_R': best_params[1],
        'masses': best_masses,
        'error': best_error
    }


# =============================================================================
# MAIN: EXAMPLE CALCULATIONS
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Z² FRAMEWORK: YUKAWA OVERLAP CALCULATOR")
    print("=" * 70)

    # Fundamental constants
    print(f"\nFundamental Constants:")
    print(f"  D = {D} (spacetime dimensions)")
    print(f"  C_F = 8π/3 = {C_F:.6f} (Friedmann coefficient)")
    print(f"  Z² = D × C_F = {Z_SQUARED:.6f}")
    print(f"  Z = √(Z²) = {Z:.6f}")
    print(f"  1/Z = {1/Z:.6f} (quantization unit)")

    # Get quantized bulk masses
    print(f"\n{'='*70}")
    print("QUANTIZED BULK MASSES (Hypothesis: c = 1/2 + n/Z)")
    print("=" * 70)

    c_params = get_quantized_bulk_masses()

    print(f"\nQuark sector:")
    print(f"  c_L (u,c,t): {c_params['quarks_L']}")
    print(f"  c_R (u,c,t): {c_params['up_R']}")
    print(f"  c_R (d,s,b): {c_params['down_R']}")

    print(f"\nLepton sector:")
    print(f"  c_L (e,μ,τ): {c_params['leptons_L']}")
    print(f"  c_R (e,μ,τ): {c_params['charged_R']}")

    # Compute up-quark mass matrix
    print(f"\n{'='*70}")
    print("UP-QUARK MASS MATRIX")
    print("=" * 70)

    M_up = compute_mass_matrix(
        c_params['quarks_L'],
        c_params['up_R'],
        y_5d=1.0,
        use_S3=True
    )

    print(f"\nMass matrix M_u:")
    print(M_up)

    masses_u, U_u, V_u = diagonalize_mass_matrix(M_up)
    print(f"\nMass eigenvalues (normalized): {masses_u / masses_u[0]}")
    print(f"Observed ratios: m_t:m_c:m_u ≈ 1 : 0.007 : 0.00001")

    # Compute down-quark mass matrix
    print(f"\n{'='*70}")
    print("DOWN-QUARK MASS MATRIX")
    print("=" * 70)

    M_down = compute_mass_matrix(
        c_params['quarks_L'],
        c_params['down_R'],
        y_5d=1.0,
        use_S3=True
    )

    print(f"\nMass matrix M_d:")
    print(M_down)

    masses_d, U_d, V_d = diagonalize_mass_matrix(M_down)
    print(f"\nMass eigenvalues (normalized): {masses_d / masses_d[0]}")
    print(f"Observed ratios: m_b:m_s:m_d ≈ 1 : 0.02 : 0.001")

    # Compute CKM matrix
    print(f"\n{'='*70}")
    print("CKM MATRIX")
    print("=" * 70)

    V_CKM = compute_CKM_matrix(U_u, U_d)
    print(f"\n|V_CKM|:")
    print(np.abs(V_CKM))

    print(f"\nObserved |V_CKM|:")
    V_CKM_obs = np.array([
        [0.974, 0.225, 0.004],
        [0.225, 0.973, 0.041],
        [0.009, 0.040, 0.999]
    ])
    print(V_CKM_obs)

    # S₃ representation matrix
    print(f"\n{'='*70}")
    print("S₃ FLAVOR STRUCTURE (T³ Overlap Matrix)")
    print("=" * 70)

    Omega = get_S3_representation_matrix()
    print(f"\nS₃ overlap matrix Ω_ij:")
    print(Omega)

    print(f"\nT³ overlap with Z-suppression:")
    print(get_T3_overlap_matrix())

    # Summary
    print(f"\n{'='*70}")
    print("STATUS: COMPUTATIONAL FRAMEWORK READY")
    print("=" * 70)
    print("""
To find the exact {c_i} values that reproduce observed masses:

1. Run parameter space scan:
   results = scan_parameter_space(target_masses, c_range, n_points)

2. Target mass ratios for up quarks:
   m_u/m_t ≈ 1.3×10⁻⁵,  m_c/m_t ≈ 7.4×10⁻³

3. Target mass ratios for down quarks:
   m_d/m_b ≈ 1.1×10⁻³,  m_s/m_b ≈ 2.2×10⁻²

4. Target mass ratios for charged leptons:
   m_e/m_τ ≈ 2.9×10⁻⁴,  m_μ/m_τ ≈ 5.9×10⁻²

The hypothesis c = 1/2 + n/Z can be TESTED by checking if integer
values of n produce the correct mass hierarchies.
""")
