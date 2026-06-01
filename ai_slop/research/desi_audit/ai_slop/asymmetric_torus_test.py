#!/usr/bin/env python3
"""
Asymmetric Torus T³(Lx, Ly, Lz)/Z₂ Test Suite
==============================================

MOTIVATION:
-----------
The symmetric T³/Z₂ model (L_c = 20.6 Gpc) shows two significant tensions:
1. Q₄ hexadecapole: 4σ WRONG SIGN (cubic enhancement not observed)
2. L_c from Lyα: 15.0 Gpc vs predicted 20.6 Gpc

HYPOTHESIS:
-----------
The √2 ratio is suspicious: 20.6/√2 = 14.57 ≈ 15.0 Gpc

This suggests an ASYMMETRIC torus:
  L_x = L_y = 20.6 Gpc (transverse, CMB-constrained)
  L_z = 14.57 Gpc (line-of-sight, Lyα-measured)

PREDICTIONS:
------------
1. Lyα χ² should improve (L_z matches observed)
2. Q₄ tension disappears (no cubic symmetry → no cubic enhancement)
3. Geometric DE formula uses direction-dependent L_eff

FALSIFICATION:
--------------
If asymmetric model doesn't simultaneously:
- Improve Lyα fit
- Eliminate Q₄ tension
- Maintain geometric DE viability
Then asymmetry hypothesis is wrong.

Author: Carl Zimmerman + Claude
Date: May 2026
Framework: v11.1.0 → v11.2.0 (asymmetric extension)
"""

import numpy as np
import json
from scipy import integrate, optimize
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# ASYMMETRIC TORUS PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════════

# Symmetric model (baseline)
L_C_SYMMETRIC = 20.6  # Gpc

# Asymmetric model (hypothesis)
# L_z derived from √2 relationship: L_z = L_c / √2
L_X = 20.6  # Gpc (transverse)
L_Y = 20.6  # Gpc (transverse)
L_Z = 20.6 / np.sqrt(2)  # = 14.57 Gpc (line-of-sight)

# Effective scales for different measurements
L_EFF_TRANSVERSE = np.sqrt(L_X * L_Y)  # Geometric mean for transverse
L_EFF_LOS = L_Z  # Line-of-sight
L_EFF_VOLUME = (L_X * L_Y * L_Z) ** (1/3)  # Volume-equivalent

# Vertex potential (unchanged)
V_VERTEX = 0.236

# Cosmological parameters
H0 = 67.4  # km/s/Mpc
OMEGA_M = 0.315
R_D = 147.09  # Mpc (sound horizon)

# ═══════════════════════════════════════════════════════════════════════════════
# ASYMMETRIC VERTEX POSITIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_vertices_symmetric(L_c):
    """8 vertices for symmetric T³/Z₂"""
    h = L_c / 2
    return np.array([
        [0, 0, 0], [h, 0, 0], [0, h, 0], [0, 0, h],
        [h, h, 0], [h, 0, h], [0, h, h], [h, h, h]
    ])

def get_vertices_asymmetric(Lx, Ly, Lz):
    """8 vertices for asymmetric T³(Lx,Ly,Lz)/Z₂"""
    hx, hy, hz = Lx/2, Ly/2, Lz/2
    return np.array([
        [0, 0, 0], [hx, 0, 0], [0, hy, 0], [0, 0, hz],
        [hx, hy, 0], [hx, 0, hz], [0, hy, hz], [hx, hy, hz]
    ])

VERTICES_SYMMETRIC = get_vertices_symmetric(L_C_SYMMETRIC)
VERTICES_ASYMMETRIC = get_vertices_asymmetric(L_X, L_Y, L_Z)

# ═══════════════════════════════════════════════════════════════════════════════
# COSMOLOGICAL FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def E_z_lcdm(z, omega_m=OMEGA_M):
    """ΛCDM E(z) = H(z)/H0"""
    return np.sqrt(omega_m * (1 + z)**3 + (1 - omega_m))

def comoving_distance(z, E_func=E_z_lcdm):
    """Comoving distance in Gpc"""
    c = 299792.458  # km/s
    integrand = lambda zp: 1 / E_func(zp)
    result, _ = integrate.quad(integrand, 0, z)
    return (c / H0) * result / 1000  # Gpc

def hubble_distance(z, E_func=E_z_lcdm):
    """D_H(z) = c / H(z) in Gpc"""
    c = 299792.458
    return c / (H0 * E_func(z)) / 1000

# ═══════════════════════════════════════════════════════════════════════════════
# GEOMETRIC DARK ENERGY MODELS
# ═══════════════════════════════════════════════════════════════════════════════

def omega_de_symmetric(z, L_c=L_C_SYMMETRIC):
    """Symmetric T³/Z₂: Ω_DE = 1 - (D_H/L_c)³"""
    D_H = hubble_distance(z)
    ratio = min(D_H / L_c, 0.99)
    return 1 - ratio**3

def omega_de_asymmetric(z, Lx=L_X, Ly=L_Y, Lz=L_Z, direction='los'):
    """
    Asymmetric T³/Z₂: direction-dependent geometric DE

    For line-of-sight (BAO, Lyα): use L_z
    For transverse (AP, angular): use √(Lx × Ly)
    For isotropic average: use (Lx × Ly × Lz)^(1/3)
    """
    D_H = hubble_distance(z)

    if direction == 'los':
        L_eff = Lz
    elif direction == 'transverse':
        L_eff = np.sqrt(Lx * Ly)
    else:  # isotropic
        L_eff = (Lx * Ly * Lz) ** (1/3)

    ratio = min(D_H / L_eff, 0.99)
    return 1 - ratio**3

def E_z_geometric_symmetric(z, L_c=L_C_SYMMETRIC):
    """E(z) for symmetric geometric DE"""
    omega_de = omega_de_symmetric(z, L_c)
    return np.sqrt(OMEGA_M * (1 + z)**3 + omega_de)

def E_z_geometric_asymmetric(z, direction='los'):
    """E(z) for asymmetric geometric DE"""
    omega_de = omega_de_asymmetric(z, direction=direction)
    return np.sqrt(OMEGA_M * (1 + z)**3 + omega_de)

# ═══════════════════════════════════════════════════════════════════════════════
# LYMAN-α ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

# DESI Lyα data (z_eff = 2.33)
LYA_DATA = {
    'z_eff': 2.33,
    'DH_rd': 8.70,
    'DH_rd_err': 0.18,
    'DM_rd': 37.20,
    'DM_rd_err': 0.90,
    'correlation': -0.44
}

def compute_lya_chi2(model='lcdm', L_c=None, direction='los'):
    """Compute χ² for Lyα BAO data"""
    z = LYA_DATA['z_eff']

    if model == 'lcdm':
        E_func = E_z_lcdm
    elif model == 'symmetric':
        E_func = lambda z: E_z_geometric_symmetric(z, L_c if L_c else L_C_SYMMETRIC)
    elif model == 'asymmetric':
        E_func = lambda z: E_z_geometric_asymmetric(z, direction)
    else:
        raise ValueError(f"Unknown model: {model}")

    # Compute distances
    c = 299792.458
    D_H = c / (H0 * E_func(z)) / 1000 * 1000  # in Mpc

    # Comoving distance with this E(z)
    integrand = lambda zp: 1 / E_func(zp)
    result, _ = integrate.quad(integrand, 0, z)
    D_M = (c / H0) * result  # in Mpc

    # Predicted ratios
    DH_rd_pred = D_H / R_D
    DM_rd_pred = D_M / R_D

    # χ² with correlation
    dDH = LYA_DATA['DH_rd'] - DH_rd_pred
    dDM = LYA_DATA['DM_rd'] - DM_rd_pred

    sigma_H = LYA_DATA['DH_rd_err']
    sigma_M = LYA_DATA['DM_rd_err']
    rho = LYA_DATA['correlation']

    # Inverse covariance
    det = (1 - rho**2) * sigma_H**2 * sigma_M**2
    chi2 = (dDH**2 * sigma_M**2 + dDM**2 * sigma_H**2 - 2*rho*sigma_H*sigma_M*dDH*dDM) / det

    return chi2, DH_rd_pred, DM_rd_pred

def scan_Lc_lya(model='symmetric', L_range=None):
    """Scan L_c (or L_z for asymmetric) to find best fit"""
    if L_range is None:
        L_range = np.linspace(10, 30, 100)

    chi2_values = []

    for L in L_range:
        if model == 'symmetric':
            chi2, _, _ = compute_lya_chi2('symmetric', L_c=L)
        else:  # asymmetric - vary L_z
            # Temporarily modify L_Z for computation
            global L_Z
            old_Lz = L_Z
            L_Z = L
            chi2, _, _ = compute_lya_chi2('asymmetric', direction='los')
            L_Z = old_Lz
        chi2_values.append(chi2)

    chi2_values = np.array(chi2_values)
    idx_min = np.argmin(chi2_values)

    return {
        'L_range': L_range,
        'chi2': chi2_values,
        'L_best': L_range[idx_min],
        'chi2_min': chi2_values[idx_min]
    }

# ═══════════════════════════════════════════════════════════════════════════════
# BAO MULTIPOLES (Q₄ ANALYSIS)
# ═══════════════════════════════════════════════════════════════════════════════

def cubic_enhancement_factor(s_Mpc, L_c):
    """
    Cubic symmetry enhancement factor for hexadecapole.
    Only applies for SYMMETRIC (cubic) topology.
    """
    # For asymmetric topology, this should be ~0
    L_c_Mpc = L_c * 1000
    n_images = min(int(L_c_Mpc / s_Mpc) + 1, 500)

    enhancement = 0
    for n in range(1, n_images + 1):
        s_image = n * L_c_Mpc
        weight = 1 / n**2.5
        phase = np.cos(4 * np.pi * s_Mpc / s_image)
        enhancement += weight * phase

    return 1 + 0.08 * enhancement

def compute_Q4_prediction(model='symmetric'):
    """
    Compute expected Q₄ for symmetric vs asymmetric topology.

    Q₄ = (ξ₄_topology - ξ₄_ΛCDM) / ξ₀

    For symmetric: Q₄ > 0 (cubic enhancement)
    For asymmetric: Q₄ ≈ 0 (no cubic symmetry)
    """
    s_bao = 100  # Mpc, BAO scale

    if model == 'symmetric':
        enhancement = cubic_enhancement_factor(s_bao, L_C_SYMMETRIC)
        # ξ₄/ξ₀ ΛCDM ≈ 0.22
        xi4_xi0_lcdm = 0.22
        xi4_xi0_topology = xi4_xi0_lcdm * enhancement
        Q4_predicted = xi4_xi0_topology - xi4_xi0_lcdm
    else:  # asymmetric
        # No cubic symmetry → no enhancement
        Q4_predicted = 0.0

    return Q4_predicted

# Observed Q₄ from BAO multipoles analysis
Q4_OBSERVED = -0.65
Q4_OBSERVED_ERR = 0.16

def compute_Q4_chi2(model='symmetric'):
    """χ² for Q₄"""
    Q4_pred = compute_Q4_prediction(model)
    chi2 = ((Q4_OBSERVED - Q4_pred) / Q4_OBSERVED_ERR)**2
    return chi2, Q4_pred

# ═══════════════════════════════════════════════════════════════════════════════
# GEOMETRIC DEFICIT (DESI w₀-wₐ)
# ═══════════════════════════════════════════════════════════════════════════════

# DESI 5Y constraints
DESI_W0 = -0.827
DESI_W0_ERR = 0.063
DESI_WA = -0.75
DESI_WA_ERR = 0.28

def effective_w(z, model='lcdm', direction='los'):
    """Compute effective equation of state w(z)"""
    if model == 'lcdm':
        return -1.0

    # For geometric models, w_eff = (Ω_DE(z) - 1) / Ω_DE(z) approximately
    # More precisely, compute from E(z) evolution
    dz = 0.01

    if model == 'symmetric':
        E1 = E_z_geometric_symmetric(z)
        E2 = E_z_geometric_symmetric(z + dz)
        omega_de = omega_de_symmetric(z)
    else:
        E1 = E_z_geometric_asymmetric(z, direction)
        E2 = E_z_geometric_asymmetric(z + dz, direction)
        omega_de = omega_de_asymmetric(z, direction=direction)

    if omega_de < 0.01:
        return -1.0

    # d(ln E²)/dz = 3Ωm(1+z)² + 3Ω_DE(1+w)
    dlnE2_dz = 2 * (E2 - E1) / (E1 * dz)

    # Solve for w
    Omega_m_z = OMEGA_M * (1 + z)**3 / E1**2
    w = (dlnE2_dz - 3 * Omega_m_z) / (3 * omega_de / E1**2) - 1

    return max(-2, min(0, w))  # Physical bounds

def fit_w0_wa(model='symmetric', direction='los'):
    """Fit w₀-wₐ parameterization to geometric model"""
    z_samples = np.array([0.3, 0.5, 0.7, 1.0, 1.5, 2.0])
    w_samples = np.array([effective_w(z, model, direction) for z in z_samples])

    # w(z) = w₀ + wₐ × z/(1+z)
    def w_model(z, w0, wa):
        return w0 + wa * z / (1 + z)

    # Simple linear fit
    X = z_samples / (1 + z_samples)
    # w = w0 + wa * X
    # Least squares: [1, X] @ [w0, wa] = w
    A = np.column_stack([np.ones_like(X), X])
    params, residuals, rank, s = np.linalg.lstsq(A, w_samples, rcond=None)
    w0_fit, wa_fit = params

    return w0_fit, wa_fit

def compute_geometric_chi2(model='symmetric', direction='los'):
    """χ² for w₀-wₐ against DESI"""
    w0, wa = fit_w0_wa(model, direction)

    chi2_w0 = ((w0 - DESI_W0) / DESI_W0_ERR)**2
    chi2_wa = ((wa - DESI_WA) / DESI_WA_ERR)**2

    return chi2_w0 + chi2_wa, w0, wa

# ═══════════════════════════════════════════════════════════════════════════════
# ETA INVARIANT FOR ASYMMETRIC TORUS
# ═══════════════════════════════════════════════════════════════════════════════

def eta_invariant_symmetric():
    """η(T³/Z₂) = 32π/3 for symmetric case"""
    return 32 * np.pi / 3

def eta_invariant_asymmetric(Lx, Ly, Lz):
    """
    Approximate η for asymmetric T³(Lx,Ly,Lz)/Z₂.

    For a rectangular torus, the eta invariant scales with aspect ratios.
    This is a first-order approximation; full calculation requires
    spectral zeta function regularization.

    η_asym ≈ η_sym × f(Lx/Ly, Ly/Lz)

    For small deviations from cubic: f ≈ 1 + O((ΔL/L)²)
    """
    L_mean = (Lx + Ly + Lz) / 3

    # Aspect ratio deviations
    dx = (Lx - L_mean) / L_mean
    dy = (Ly - L_mean) / L_mean
    dz = (Lz - L_mean) / L_mean

    # Leading correction (quadratic in deviations)
    # This is an approximation; proper calculation needed for precision
    correction = 1 - 0.1 * (dx**2 + dy**2 + dz**2)

    return eta_invariant_symmetric() * correction

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def run_comparison():
    """Run full comparison between symmetric and asymmetric models"""

    print("=" * 80)
    print("ASYMMETRIC TORUS T³(Lx, Ly, Lz)/Z₂ TEST SUITE")
    print("Testing the √2 Hypothesis")
    print("=" * 80)
    print()

    # Model parameters
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "MODEL PARAMETERS" + " " * 34 + "║")
    print("╠" + "═" * 78 + "╣")
    print(f"║  SYMMETRIC (baseline):                                                       ║")
    print(f"║    L_c = {L_C_SYMMETRIC:.2f} Gpc (all axes equal)                                          ║")
    print("║                                                                              ║")
    print(f"║  ASYMMETRIC (hypothesis):                                                   ║")
    print(f"║    L_x = L_y = {L_X:.2f} Gpc (transverse, CMB-constrained)                       ║")
    print(f"║    L_z = {L_Z:.2f} Gpc (line-of-sight, L_c/√2)                                  ║")
    print("║                                                                              ║")
    print(f"║  √2 CHECK: 20.6/√2 = {20.6/np.sqrt(2):.2f} Gpc ≈ Lyα best-fit 15.0 Gpc                     ║")
    print("╚" + "═" * 78 + "╝")
    print()

    results = {
        'symmetric': {},
        'asymmetric': {},
        'comparison': {}
    }

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 1: LYMAN-α GEOMETRIC DEFICIT
    # ═══════════════════════════════════════════════════════════════════════════

    print("=" * 80)
    print("TEST 1: LYMAN-α BAO (z = 2.33)")
    print("=" * 80)
    print()

    # ΛCDM baseline
    chi2_lcdm, DH_lcdm, DM_lcdm = compute_lya_chi2('lcdm')

    # Symmetric with fixed L_c = 20.6
    chi2_sym, DH_sym, DM_sym = compute_lya_chi2('symmetric', L_c=L_C_SYMMETRIC)

    # Symmetric with best-fit L_c
    scan_sym = scan_Lc_lya('symmetric')
    chi2_sym_best = scan_sym['chi2_min']
    Lc_sym_best = scan_sym['L_best']

    # Asymmetric with L_z = L_c/√2
    chi2_asym, DH_asym, DM_asym = compute_lya_chi2('asymmetric', direction='los')

    print("┌" + "─" * 78 + "┐")
    print("│" + " " * 28 + "LYMAN-α χ² COMPARISON" + " " * 29 + "│")
    print("├" + "─" * 78 + "┤")
    print(f"│  Model                    │  χ²        │  D_H/r_d   │  D_M/r_d   │  ΔL_c     │")
    print("│───────────────────────────┼────────────┼────────────┼────────────┼───────────│")
    print(f"│  ΛCDM                      │  {chi2_lcdm:6.2f}    │  {DH_lcdm:6.2f}    │  {DM_lcdm:6.2f}    │    -      │")
    print(f"│  Symmetric (L_c=20.6)     │  {chi2_sym:6.2f}    │  {DH_sym:6.2f}    │  {DM_sym:6.2f}    │    0      │")
    print(f"│  Symmetric (best-fit)     │  {chi2_sym_best:6.2f}    │     -      │     -      │  {Lc_sym_best-20.6:+5.1f}    │")
    print(f"│  ASYMMETRIC (L_z=14.6)    │  {chi2_asym:6.2f}    │  {DH_asym:6.2f}    │  {DM_asym:6.2f}    │  {L_Z-20.6:+5.1f}    │")
    print("└" + "─" * 78 + "┘")
    print()

    # Determine winner
    lya_winner = "ASYMMETRIC" if chi2_asym < chi2_sym else "SYMMETRIC"
    lya_improvement = (chi2_sym - chi2_asym) / chi2_sym * 100

    print(f"  WINNER: {lya_winner}")
    print(f"  χ² improvement: {lya_improvement:+.1f}%")
    if chi2_asym < chi2_lcdm:
        print(f"  ASYMMETRIC BEATS ΛCDM: χ² = {chi2_asym:.2f} vs {chi2_lcdm:.2f}")
    print()

    results['symmetric']['lya_chi2'] = chi2_sym
    results['asymmetric']['lya_chi2'] = chi2_asym
    results['comparison']['lya_winner'] = lya_winner
    results['comparison']['lya_improvement_pct'] = lya_improvement

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 2: Q₄ HEXADECAPOLE (CUBIC ANISOTROPY)
    # ═══════════════════════════════════════════════════════════════════════════

    print("=" * 80)
    print("TEST 2: Q₄ HEXADECAPOLE (CUBIC ANISOTROPY)")
    print("=" * 80)
    print()

    chi2_Q4_sym, Q4_pred_sym = compute_Q4_chi2('symmetric')
    chi2_Q4_asym, Q4_pred_asym = compute_Q4_chi2('asymmetric')

    sigma_Q4_sym = np.sqrt(chi2_Q4_sym)
    sigma_Q4_asym = np.sqrt(chi2_Q4_asym)

    print("┌" + "─" * 78 + "┐")
    print("│" + " " * 26 + "Q₄ HEXADECAPOLE COMPARISON" + " " * 26 + "│")
    print("├" + "─" * 78 + "┤")
    print(f"│  OBSERVED: Q₄ = {Q4_OBSERVED:+.3f} ± {Q4_OBSERVED_ERR:.3f}                                           │")
    print("│                                                                              │")
    print(f"│  Model          │  Q₄ predicted  │  χ²         │  Tension                   │")
    print("│─────────────────┼────────────────┼─────────────┼────────────────────────────│")
    print(f"│  SYMMETRIC      │  {Q4_pred_sym:+.3f}         │  {chi2_Q4_sym:6.1f}      │  {sigma_Q4_sym:.1f}σ {'WRONG SIGN' if Q4_pred_sym * Q4_OBSERVED < 0 else 'correct'}          │")
    print(f"│  ASYMMETRIC     │  {Q4_pred_asym:+.3f}         │  {chi2_Q4_asym:6.1f}      │  {sigma_Q4_asym:.1f}σ                       │")
    print("└" + "─" * 78 + "┘")
    print()

    Q4_winner = "ASYMMETRIC" if chi2_Q4_asym < chi2_Q4_sym else "SYMMETRIC"
    Q4_improvement = (chi2_Q4_sym - chi2_Q4_asym) / chi2_Q4_sym * 100

    print(f"  WINNER: {Q4_winner}")
    print(f"  χ² improvement: {Q4_improvement:+.1f}%")
    print(f"  SYMMETRIC: 4σ wrong sign → ASYMMETRIC: {sigma_Q4_asym:.1f}σ (no cubic prediction)")
    print()

    results['symmetric']['Q4_chi2'] = chi2_Q4_sym
    results['asymmetric']['Q4_chi2'] = chi2_Q4_asym
    results['comparison']['Q4_winner'] = Q4_winner
    results['comparison']['Q4_improvement_pct'] = Q4_improvement

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 3: GEOMETRIC DARK ENERGY (w₀-wₐ)
    # ═══════════════════════════════════════════════════════════════════════════

    print("=" * 80)
    print("TEST 3: GEOMETRIC DARK ENERGY (w₀-wₐ)")
    print("=" * 80)
    print()

    chi2_geom_sym, w0_sym, wa_sym = compute_geometric_chi2('symmetric')
    chi2_geom_asym, w0_asym, wa_asym = compute_geometric_chi2('asymmetric', direction='los')

    print("┌" + "─" * 78 + "┐")
    print("│" + " " * 24 + "GEOMETRIC DE w₀-wₐ COMPARISON" + " " * 25 + "│")
    print("├" + "─" * 78 + "┤")
    print(f"│  DESI 5Y: w₀ = {DESI_W0:.3f} ± {DESI_W0_ERR:.3f}, wₐ = {DESI_WA:+.2f} ± {DESI_WA_ERR:.2f}                        │")
    print("│                                                                              │")
    print(f"│  Model          │  w₀ fit     │  wₐ fit     │  χ²                          │")
    print("│─────────────────┼─────────────┼─────────────┼──────────────────────────────│")
    print(f"│  SYMMETRIC      │  {w0_sym:+.3f}      │  {wa_sym:+.3f}      │  {chi2_geom_sym:6.2f}                       │")
    print(f"│  ASYMMETRIC     │  {w0_asym:+.3f}      │  {wa_asym:+.3f}      │  {chi2_geom_asym:6.2f}                       │")
    print("└" + "─" * 78 + "┘")
    print()

    geom_winner = "ASYMMETRIC" if chi2_geom_asym < chi2_geom_sym else "SYMMETRIC"

    print(f"  WINNER: {geom_winner}")
    print()

    results['symmetric']['geom_chi2'] = chi2_geom_sym
    results['asymmetric']['geom_chi2'] = chi2_geom_asym
    results['comparison']['geom_winner'] = geom_winner

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 4: ETA INVARIANT
    # ═══════════════════════════════════════════════════════════════════════════

    print("=" * 80)
    print("TEST 4: ETA INVARIANT")
    print("=" * 80)
    print()

    eta_sym = eta_invariant_symmetric()
    eta_asym = eta_invariant_asymmetric(L_X, L_Y, L_Z)

    print("┌" + "─" * 78 + "┐")
    print("│" + " " * 28 + "ETA INVARIANT COMPARISON" + " " * 26 + "│")
    print("├" + "─" * 78 + "┤")
    print(f"│  η(T³/Z₂) symmetric:     {eta_sym:.4f} = 32π/3                                  │")
    print(f"│  η(T³/Z₂) asymmetric:    {eta_asym:.4f} (approximate)                           │")
    print(f"│  Deviation:              {(eta_asym/eta_sym - 1)*100:+.2f}%                                             │")
    print("│                                                                              │")
    print("│  NOTE: Full asymmetric η requires spectral zeta regularization.             │")
    print("│        This is a first-order approximation only.                            │")
    print("└" + "─" * 78 + "┘")
    print()

    results['symmetric']['eta'] = eta_sym
    results['asymmetric']['eta'] = eta_asym

    # ═══════════════════════════════════════════════════════════════════════════
    # AGGREGATE COMPARISON
    # ═══════════════════════════════════════════════════════════════════════════

    print("=" * 80)
    print("AGGREGATE COMPARISON")
    print("=" * 80)
    print()

    # Total χ²
    total_chi2_sym = chi2_sym + chi2_Q4_sym + chi2_geom_sym
    total_chi2_asym = chi2_asym + chi2_Q4_asym + chi2_geom_asym

    print("┌" + "─" * 78 + "┐")
    print("│" + " " * 28 + "TOTAL χ² COMPARISON" + " " * 31 + "│")
    print("├" + "─" * 78 + "┤")
    print(f"│  Test              │  SYMMETRIC χ²  │  ASYMMETRIC χ²  │  Winner           │")
    print("│────────────────────┼────────────────┼─────────────────┼───────────────────│")
    print(f"│  Lyman-α           │  {chi2_sym:10.2f}    │  {chi2_asym:11.2f}    │  {lya_winner:16s} │")
    print(f"│  Q₄ hexadecapole   │  {chi2_Q4_sym:10.2f}    │  {chi2_Q4_asym:11.2f}    │  {Q4_winner:16s} │")
    print(f"│  Geometric DE      │  {chi2_geom_sym:10.2f}    │  {chi2_geom_asym:11.2f}    │  {geom_winner:16s} │")
    print("│────────────────────┼────────────────┼─────────────────┼───────────────────│")
    print(f"│  TOTAL             │  {total_chi2_sym:10.2f}    │  {total_chi2_asym:11.2f}    │  {'ASYMMETRIC' if total_chi2_asym < total_chi2_sym else 'SYMMETRIC':16s} │")
    print("└" + "─" * 78 + "┘")
    print()

    total_improvement = (total_chi2_sym - total_chi2_asym) / total_chi2_sym * 100

    results['symmetric']['total_chi2'] = total_chi2_sym
    results['asymmetric']['total_chi2'] = total_chi2_asym
    results['comparison']['total_improvement_pct'] = total_improvement

    # ═══════════════════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════════════════

    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()

    # Count wins
    asym_wins = sum([
        chi2_asym < chi2_sym,
        chi2_Q4_asym < chi2_Q4_sym,
        chi2_geom_asym < chi2_geom_sym
    ])

    # Determine overall verdict
    if asym_wins >= 2 and total_chi2_asym < total_chi2_sym:
        verdict = "ASYMMETRIC PREFERRED"
        verdict_detail = "√2 hypothesis SUPPORTED"
    elif asym_wins >= 2:
        verdict = "ASYMMETRIC MARGINAL"
        verdict_detail = "Some improvement, needs confirmation"
    else:
        verdict = "SYMMETRIC PREFERRED"
        verdict_detail = "√2 hypothesis NOT SUPPORTED"

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "ASYMMETRIC TORUS TEST: COMPLETE" + " " * 27 + "║")
    print("╠" + "═" * 78 + "╣")
    print("║                                                                              ║")
    print(f"║  HYPOTHESIS: L_z = L_c/√2 = {L_Z:.2f} Gpc                                         ║")
    print("║                                                                              ║")
    print("║  RESULTS:                                                                    ║")
    print(f"║    Asymmetric wins: {asym_wins}/3 tests                                               ║")
    print(f"║    Total χ² improvement: {total_improvement:+.1f}%                                             ║")
    print("║                                                                              ║")
    print("║  KEY FINDINGS:                                                               ║")

    # Lyman-α finding
    if chi2_asym < chi2_sym:
        print(f"║    ✓ Lyα: χ² improved from {chi2_sym:.2f} to {chi2_asym:.2f}" + " " * (36 - len(f"{chi2_sym:.2f}") - len(f"{chi2_asym:.2f}")) + "║")
    else:
        print(f"║    ✗ Lyα: χ² worsened from {chi2_sym:.2f} to {chi2_asym:.2f}" + " " * (35 - len(f"{chi2_sym:.2f}") - len(f"{chi2_asym:.2f}")) + "║")

    # Q4 finding
    if chi2_Q4_asym < chi2_Q4_sym:
        print(f"║    ✓ Q₄: Tension reduced from {sigma_Q4_sym:.1f}σ to {sigma_Q4_asym:.1f}σ" + " " * (36 - len(f"{sigma_Q4_sym:.1f}") - len(f"{sigma_Q4_asym:.1f}")) + "║")
    else:
        print(f"║    ✗ Q₄: Tension increased" + " " * 49 + "║")

    # Geometric DE finding
    if chi2_geom_asym < chi2_geom_sym:
        print(f"║    ✓ Geometric DE: Better w₀-wₐ fit" + " " * 40 + "║")
    else:
        print(f"║    ✗ Geometric DE: Worse w₀-wₐ fit" + " " * 41 + "║")

    print("║                                                                              ║")
    print("║  ════════════════════════════════════════════════════════════════════════   ║")
    print(f"║  VERDICT: {verdict}" + " " * (66 - len(verdict)) + "║")
    print(f"║           {verdict_detail}" + " " * (66 - len(verdict_detail)) + "║")
    print("║  ════════════════════════════════════════════════════════════════════════   ║")
    print("║                                                                              ║")

    if verdict == "ASYMMETRIC PREFERRED":
        print("║  IMPLICATION: The universe may be a rectangular torus, not a cube.         ║")
        print("║               v11.2.0 should incorporate asymmetric T³/Z₂.                 ║")

    print("║                                                                              ║")
    print("╚" + "═" * 78 + "╝")
    print()

    results['verdict'] = {
        'winner': verdict,
        'detail': verdict_detail,
        'asymmetric_wins': asym_wins,
        'total_improvement_pct': total_improvement
    }

    # Save results
    output = {
        'analysis': 'asymmetric_torus_test',
        'framework': 'v11.1.0 → v11.2.0',
        'date': datetime.now().strftime('%B %d, %Y'),
        'hypothesis': {
            'sqrt2_relationship': '20.6/√2 = 14.57 ≈ 15.0 (Lyα best-fit)',
            'L_x': float(L_X),
            'L_y': float(L_Y),
            'L_z': float(L_Z),
            'L_z_formula': 'L_c / √2'
        },
        'lyman_alpha': {
            'chi2_symmetric': float(chi2_sym),
            'chi2_asymmetric': float(chi2_asym),
            'chi2_lcdm': float(chi2_lcdm),
            'winner': lya_winner,
            'improvement_pct': float(lya_improvement)
        },
        'Q4_hexadecapole': {
            'observed': float(Q4_OBSERVED),
            'observed_err': float(Q4_OBSERVED_ERR),
            'predicted_symmetric': float(Q4_pred_sym),
            'predicted_asymmetric': float(Q4_pred_asym),
            'chi2_symmetric': float(chi2_Q4_sym),
            'chi2_asymmetric': float(chi2_Q4_asym),
            'sigma_symmetric': float(sigma_Q4_sym),
            'sigma_asymmetric': float(sigma_Q4_asym),
            'winner': Q4_winner
        },
        'geometric_de': {
            'w0_symmetric': float(w0_sym),
            'wa_symmetric': float(wa_sym),
            'w0_asymmetric': float(w0_asym),
            'wa_asymmetric': float(wa_asym),
            'chi2_symmetric': float(chi2_geom_sym),
            'chi2_asymmetric': float(chi2_geom_asym),
            'winner': geom_winner
        },
        'eta_invariant': {
            'symmetric': float(eta_sym),
            'asymmetric_approx': float(eta_asym),
            'deviation_pct': float((eta_asym/eta_sym - 1)*100)
        },
        'aggregate': {
            'total_chi2_symmetric': float(total_chi2_sym),
            'total_chi2_asymmetric': float(total_chi2_asym),
            'asymmetric_wins': int(asym_wins),
            'total_improvement_pct': float(total_improvement)
        },
        'verdict': {
            'overall': verdict,
            'detail': verdict_detail,
            'recommendation': 'Incorporate asymmetric T³(Lx,Ly,Lz)/Z₂ into v11.2.0' if 'PREFERRED' in verdict else 'Retain symmetric T³/Z₂'
        }
    }

    output_file = 'research/desi_audit/asymmetric_torus_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Results saved to: {output_file}")
    print("=" * 80)

    return output

if __name__ == '__main__':
    run_comparison()
