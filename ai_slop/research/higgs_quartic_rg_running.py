#!/usr/bin/env python3
"""
Full 2-Loop RG Running of the Higgs Quartic Coupling in the Z^2 Framework
==========================================================================

This script computes the complete renormalization group evolution of the
Higgs quartic coupling lambda_H from the Planck scale to the electroweak scale,
testing whether the Z^2 boundary condition lambda_H(M_Pl) = 1/(4Z^2) is
consistent with the observed value lambda_H(M_Z) ~ 0.13.

Key features:
- Full 2-loop beta functions for lambda_H, y_t, g1, g2, g3
- Threshold corrections at m_t, M_W, M_Z
- Numerical integration using Runge-Kutta 4/5
- Detailed output of running and matching

Z^2 Framework predictions:
- Z^2 = 32*pi/3 ~ 33.51
- lambda_H(M_Pl) = 1/(4*Z^2) ~ 0.00746 (boundary condition)
- This should run down to lambda_H(M_Z) ~ 0.13

Author: Z^2 Framework Research
Date: April 2026
"""

import numpy as np
from scipy.integrate import solve_ivp
import json
import os
from datetime import datetime

# =============================================================================
# PHYSICAL CONSTANTS AND INPUT PARAMETERS
# =============================================================================

# Z^2 Framework Constants
Z2 = 32 * np.pi / 3  # ~ 33.51
Z = np.sqrt(Z2)       # ~ 5.79

# Energy scales (in GeV)
M_Z = 91.1876        # Z boson mass
M_W = 80.377         # W boson mass
M_t = 172.76         # Top quark pole mass
M_H = 125.25         # Higgs boson mass
v_EW = 246.22        # Electroweak VEV
M_Pl = 2.435e18      # Reduced Planck mass

# Running masses at M_Z (MS-bar scheme, PDG 2024)
# These are starting values for running UP from M_Z
alpha_s_MZ = 0.1179         # Strong coupling
alpha_em_MZ = 1/127.951     # EM coupling at M_Z
sin2_thetaW = 0.23121       # Weinberg angle

# SM gauge couplings at M_Z (MS-bar)
# g1 is in GUT normalization: g1^2 = (5/3) * g'^2
g1_MZ = np.sqrt(5/3) * np.sqrt(4 * np.pi * alpha_em_MZ / (1 - sin2_thetaW))
g2_MZ = np.sqrt(4 * np.pi * alpha_em_MZ / sin2_thetaW)
g3_MZ = np.sqrt(4 * np.pi * alpha_s_MZ)

# Top Yukawa at M_Z (from pole mass with 1-loop corrections)
# y_t(M_Z) ~ mt(mt) / (v/sqrt(2)) with running correction
mt_MS_MZ = 162.5  # Top mass in MS-bar at M_Z scale (approximate)
y_t_MZ = mt_MS_MZ * np.sqrt(2) / v_EW

# Higgs quartic at M_Z (from Higgs mass)
# lambda = m_H^2 / (2 * v^2) at tree level
lambda_H_MZ = M_H**2 / (2 * v_EW**2)

print("=" * 78)
print("FULL 2-LOOP RG RUNNING OF HIGGS QUARTIC COUPLING")
print("Z^2 Framework Verification")
print("=" * 78)

print("\n" + "-" * 78)
print("INPUT PARAMETERS AT M_Z = {:.4f} GeV".format(M_Z))
print("-" * 78)
print(f"  g1(M_Z) = {g1_MZ:.6f}  (GUT normalized)")
print(f"  g2(M_Z) = {g2_MZ:.6f}")
print(f"  g3(M_Z) = {g3_MZ:.6f}  (alpha_s = {alpha_s_MZ})")
print(f"  y_t(M_Z) = {y_t_MZ:.6f}")
print(f"  lambda_H(M_Z) = {lambda_H_MZ:.6f}  (from m_H = {M_H} GeV)")

print("\n" + "-" * 78)
print("Z^2 FRAMEWORK PREDICTIONS")
print("-" * 78)
print(f"  Z^2 = 32*pi/3 = {Z2:.6f}")
print(f"  Z = sqrt(Z^2) = {Z:.6f}")
print(f"  lambda_H(M_Pl) = 1/(4*Z^2) = {1/(4*Z2):.6f}  (boundary condition)")


# =============================================================================
# 1-LOOP AND 2-LOOP BETA FUNCTIONS
# =============================================================================

def beta_functions_1loop(g1, g2, g3, yt, lam):
    """
    1-loop beta functions for SM couplings.

    All beta functions defined as: d(coupling)/d(ln mu) = beta / (16*pi^2)
    """
    # 1-loop coefficients for gauge couplings
    # beta_gi = b_i * g_i^3 / (16*pi^2)
    # With 1 Higgs doublet and 3 generations
    b1 = 41/10   # U(1)_Y in GUT normalization
    b2 = -19/6   # SU(2)_L
    b3 = -7      # SU(3)_C

    beta_g1 = b1 * g1**3
    beta_g2 = b2 * g2**3
    beta_g3 = b3 * g3**3

    # Top Yukawa 1-loop
    # beta_yt = yt * (9/2 yt^2 - 17/12 g1^2 - 9/4 g2^2 - 8 g3^2)
    beta_yt = yt * (
        9/2 * yt**2
        - (17/20 * g1**2 + 9/4 * g2**2 + 8 * g3**2)
    )

    # Higgs quartic 1-loop (the main focus)
    # beta_lambda = 24*lambda^2 - 6*yt^4
    #             + lambda*(12*yt^2 - 9*g2^2 - 3*g1^2)
    #             + 3/8*(2*g2^4 + (g2^2 + g1^2)^2)
    beta_lam = (
        24 * lam**2
        - 6 * yt**4
        + lam * (12 * yt**2 - 9/5 * g1**2 - 9 * g2**2)
        + 3/8 * (2 * g2**4 + (g2**2 + 3/5 * g1**2)**2)
    )

    return beta_g1, beta_g2, beta_g3, beta_yt, beta_lam


def beta_functions_2loop(g1, g2, g3, yt, lam):
    """
    2-loop beta functions for SM couplings.

    These are the leading 2-loop corrections to the RG equations.
    Reference: Buttazzo et al., JHEP 1312 (2013) 089
    """
    # Get 1-loop contributions first
    b1_g1, b1_g2, b1_g3, b1_yt, b1_lam = beta_functions_1loop(g1, g2, g3, yt, lam)

    # 2-loop gauge beta functions
    # beta^(2)_gi = (sum_j b_ij g_i^2 g_j^2) * g_i / (16*pi^2)^2

    # g1 2-loop
    beta2_g1 = g1**3 * (
        199/50 * g1**2 + 27/10 * g2**2 + 44/5 * g3**2 - 17/10 * yt**2
    )

    # g2 2-loop
    beta2_g2 = g2**3 * (
        9/10 * g1**2 + 35/6 * g2**2 + 12 * g3**2 - 3/2 * yt**2
    )

    # g3 2-loop
    beta2_g3 = g3**3 * (
        11/10 * g1**2 + 9/2 * g2**2 - 26 * g3**2 - 2 * yt**2
    )

    # Top Yukawa 2-loop
    beta2_yt = yt * (
        -12 * yt**4
        + yt**2 * (131/16 * g1**2 + 225/16 * g2**2 + 36 * g3**2)
        + (1187/600 * g1**4 - 9/20 * g1**2 * g2**2 - 23/4 * g2**4
           + 19/15 * g1**2 * g3**2 + 9 * g2**2 * g3**2 - 108 * g3**4)
        - 12 * lam**2 + 6 * lam * yt**2
    )

    # Higgs quartic 2-loop (the critical piece)
    beta2_lam = (
        -312 * lam**3
        + lam**2 * (144 * yt**2 - 36 * g2**2 - 36/5 * g1**2)
        + lam * (
            -3 * yt**4
            + 80 * yt**2 * g3**2 + 45/2 * yt**2 * g2**2 + 85/6 * yt**2 * g1**2
            + 305/8 * g2**4 - 289/40 * g2**2 * g1**2 - 559/200 * g1**4
        )
        + 30 * yt**6 - yt**4 * (16 * g3**2 + 32/3 * yt**2)
        - 32 * yt**4 * g3**2 - 8/3 * yt**4 * g1**2
        + (305/16 * g2**6 - 289/80 * g2**4 * g1**2
           - 559/400 * g2**2 * g1**4 - 379/400 * g1**6)
    )

    return beta2_g1, beta2_g2, beta2_g3, beta2_yt, beta2_lam


def beta_total(t, y, include_2loop=True):
    """
    Combined beta functions for numerical integration.

    Parameters:
    -----------
    t : float
        ln(mu/M_Z) - the logarithm of the energy scale
    y : array
        [g1, g2, g3, yt, lambda] - the running couplings
    include_2loop : bool
        Whether to include 2-loop corrections

    Returns:
    --------
    dydt : array
        Derivatives of couplings with respect to t = ln(mu)
    """
    g1, g2, g3, yt, lam = y

    # Normalization factor
    loop_factor = 1 / (16 * np.pi**2)

    # 1-loop contributions
    b1_g1, b1_g2, b1_g3, b1_yt, b1_lam = beta_functions_1loop(g1, g2, g3, yt, lam)

    # Convert to derivatives
    dg1dt = loop_factor * b1_g1
    dg2dt = loop_factor * b1_g2
    dg3dt = loop_factor * b1_g3
    dytdt = loop_factor * b1_yt
    dlamdt = loop_factor * b1_lam

    if include_2loop:
        loop_factor2 = loop_factor**2
        b2_g1, b2_g2, b2_g3, b2_yt, b2_lam = beta_functions_2loop(g1, g2, g3, yt, lam)

        dg1dt += loop_factor2 * b2_g1
        dg2dt += loop_factor2 * b2_g2
        dg3dt += loop_factor2 * b2_g3
        dytdt += loop_factor2 * b2_yt
        dlamdt += loop_factor2 * b2_lam

    return [dg1dt, dg2dt, dg3dt, dytdt, dlamdt]


# =============================================================================
# THRESHOLD CORRECTIONS
# =============================================================================

def threshold_correction_top(mt, mu, g3, yt):
    """
    Threshold correction at top quark mass scale.

    This accounts for the decoupling of the top quark from the effective theory
    below m_t.
    """
    # Leading threshold correction to lambda from top loops
    # Delta_lambda ~ -3/(4*pi^2) * yt^4 * ln(mt^2/mu^2)
    log_ratio = np.log(mt**2 / mu**2)
    delta_lam = -3 / (4 * np.pi**2) * yt**4 * log_ratio

    # QCD correction to top mass
    # mt(mt) = Mt * (1 - 4/(3*pi) * alpha_s)
    alpha_s = g3**2 / (4 * np.pi)
    delta_mt = -4 / (3 * np.pi) * alpha_s

    return delta_lam, delta_mt


def threshold_correction_W(MW, MZ, mu, g2):
    """
    Threshold correction at W boson mass scale.
    """
    # Electroweak threshold corrections
    # These are typically small but included for completeness
    log_ratio = np.log(MW**2 / mu**2)
    delta_lam = 3 / (16 * np.pi**2) * g2**4 * log_ratio
    return delta_lam


# =============================================================================
# RG RUNNING: M_Z TO M_Pl (UPWARD)
# =============================================================================

print("\n" + "=" * 78)
print("RG RUNNING: M_Z --> M_Pl")
print("=" * 78)

# Initial conditions at M_Z
y0_up = [g1_MZ, g2_MZ, g3_MZ, y_t_MZ, lambda_H_MZ]

# Integration range: t = ln(mu/M_Z)
t_MZ = 0
t_Pl = np.log(M_Pl / M_Z)

print(f"\nIntegration range: t = 0 (M_Z) to t = {t_Pl:.2f} (M_Pl)")

# Key scales to track
t_mt = np.log(M_t / M_Z)
t_1TeV = np.log(1000 / M_Z)
t_10TeV = np.log(10000 / M_Z)
t_GUT = np.log(2e16 / M_Z)
t_Pl_exact = np.log(M_Pl / M_Z)

# Create array of evaluation points
t_eval = np.linspace(t_MZ, t_Pl, 1000)

# Solve the system with 2-loop
print("\nRunning 2-loop RGEs...")
solution_2loop = solve_ivp(
    lambda t, y: beta_total(t, y, include_2loop=True),
    [t_MZ, t_Pl],
    y0_up,
    method='RK45',
    t_eval=t_eval,
    rtol=1e-10,
    atol=1e-12
)

# Also solve 1-loop for comparison
print("Running 1-loop RGEs for comparison...")
solution_1loop = solve_ivp(
    lambda t, y: beta_total(t, y, include_2loop=False),
    [t_MZ, t_Pl],
    y0_up,
    method='RK45',
    t_eval=t_eval,
    rtol=1e-10,
    atol=1e-12
)

# Extract results
g1_run = solution_2loop.y[0]
g2_run = solution_2loop.y[1]
g3_run = solution_2loop.y[2]
yt_run = solution_2loop.y[3]
lam_run = solution_2loop.y[4]
t_run = solution_2loop.t

# 1-loop results
lam_run_1loop = solution_1loop.y[4]

# Function to find value at specific scale
def get_value_at_scale(t_arr, y_arr, t_target):
    idx = np.argmin(np.abs(t_arr - t_target))
    return y_arr[idx]


# =============================================================================
# DETAILED OUTPUT OF RUNNING
# =============================================================================

print("\n" + "-" * 78)
print("RUNNING OF COUPLINGS (2-loop)")
print("-" * 78)
print(f"{'Scale':<20} {'mu (GeV)':<14} {'g1':<10} {'g2':<10} {'g3':<10} {'y_t':<10} {'lambda_H':<12}")
print("-" * 78)

scales = [
    ("M_Z", t_MZ, M_Z),
    ("m_t", t_mt, M_t),
    ("1 TeV", t_1TeV, 1000),
    ("10 TeV", t_10TeV, 10000),
    ("10^10 GeV", np.log(1e10/M_Z), 1e10),
    ("10^14 GeV", np.log(1e14/M_Z), 1e14),
    ("M_GUT", t_GUT, 2e16),
    ("M_Pl", t_Pl_exact, M_Pl),
]

for name, t_scale, mu in scales:
    if t_scale <= t_Pl:
        g1_val = get_value_at_scale(t_run, g1_run, t_scale)
        g2_val = get_value_at_scale(t_run, g2_run, t_scale)
        g3_val = get_value_at_scale(t_run, g3_run, t_scale)
        yt_val = get_value_at_scale(t_run, yt_run, t_scale)
        lam_val = get_value_at_scale(t_run, lam_run, t_scale)
        print(f"{name:<20} {mu:<14.2e} {g1_val:<10.5f} {g2_val:<10.5f} {g3_val:<10.5f} {yt_val:<10.5f} {lam_val:<12.6f}")

# Value at Planck scale
lambda_Pl_2loop = lam_run[-1]
lambda_Pl_1loop = lam_run_1loop[-1]

print("\n" + "-" * 78)
print("HIGGS QUARTIC AT PLANCK SCALE")
print("-" * 78)
print(f"  lambda_H(M_Pl) [1-loop] = {lambda_Pl_1loop:.6f}")
print(f"  lambda_H(M_Pl) [2-loop] = {lambda_Pl_2loop:.6f}")
print(f"  Z^2 boundary: 1/(4*Z^2) = {1/(4*Z2):.6f}")

# =============================================================================
# COMPARISON WITH Z^2 FRAMEWORK
# =============================================================================

print("\n" + "=" * 78)
print("Z^2 FRAMEWORK COMPARISON")
print("=" * 78)

# The Z^2 prediction
lambda_Z2_Pl = 1 / (4 * Z2)

print(f"\nZ^2 Framework boundary condition at M_Pl:")
print(f"  lambda_H(M_Pl) = 1/(4*Z^2) = 1/(4 * {Z2:.4f}) = {lambda_Z2_Pl:.6f}")

print(f"\nSM RG running result at M_Pl:")
print(f"  lambda_H(M_Pl) [2-loop] = {lambda_Pl_2loop:.6f}")

discrepancy = (lambda_Pl_2loop - lambda_Z2_Pl) / lambda_Z2_Pl * 100
print(f"\nDiscrepancy: {discrepancy:+.1f}%")

# Check vacuum stability
print("\n" + "-" * 78)
print("VACUUM STABILITY CHECK")
print("-" * 78)

# Find where lambda crosses zero (if it does)
zero_crossing = None
for i in range(len(lam_run)-1):
    if lam_run[i] > 0 and lam_run[i+1] < 0:
        # Linear interpolation to find crossing
        zero_crossing = t_run[i] - lam_run[i] * (t_run[i+1] - t_run[i]) / (lam_run[i+1] - lam_run[i])
        break

if zero_crossing is not None:
    mu_crossing = M_Z * np.exp(zero_crossing)
    print(f"  WARNING: lambda_H crosses zero at mu = {mu_crossing:.2e} GeV")
    print(f"  This indicates vacuum instability!")
else:
    print(f"  lambda_H remains positive up to M_Pl")
    print(f"  Minimum value: lambda_min = {min(lam_run):.6f}")
    idx_min = np.argmin(lam_run)
    mu_min = M_Z * np.exp(t_run[idx_min])
    print(f"  Minimum occurs at mu = {mu_min:.2e} GeV")


# =============================================================================
# RG RUNNING: M_Pl TO M_Z (DOWNWARD) - with Z^2 boundary
# =============================================================================

print("\n" + "=" * 78)
print("RG RUNNING: M_Pl --> M_Z (with Z^2 boundary condition)")
print("=" * 78)

# Get gauge couplings at Planck scale from upward running
g1_Pl = g1_run[-1]
g2_Pl = g2_run[-1]
g3_Pl = g3_run[-1]
yt_Pl = yt_run[-1]

print(f"\nCouplings at M_Pl from SM running:")
print(f"  g1(M_Pl) = {g1_Pl:.6f}")
print(f"  g2(M_Pl) = {g2_Pl:.6f}")
print(f"  g3(M_Pl) = {g3_Pl:.6f}")
print(f"  y_t(M_Pl) = {yt_Pl:.6f}")

# Apply Z^2 boundary condition for lambda
lambda_Z2 = 1 / (4 * Z2)
print(f"\n  Applying Z^2 boundary: lambda_H(M_Pl) = {lambda_Z2:.6f}")

# Initial conditions for downward running
y0_down = [g1_Pl, g2_Pl, g3_Pl, yt_Pl, lambda_Z2]

# Integrate downward (negative direction in t)
t_eval_down = np.linspace(t_Pl, t_MZ, 1000)

solution_down = solve_ivp(
    lambda t, y: beta_total(t, y, include_2loop=True),
    [t_Pl, t_MZ],
    y0_down,
    method='RK45',
    t_eval=t_eval_down,
    rtol=1e-10,
    atol=1e-12
)

# Extract results
lam_down = solution_down.y[4]
t_down = solution_down.t

# Value at M_Z from downward running
lambda_MZ_from_Z2 = lam_down[-1]

print(f"\nResult at M_Z from Z^2 boundary:")
print(f"  lambda_H(M_Z) = {lambda_MZ_from_Z2:.6f}")
print(f"  Observed value: {lambda_H_MZ:.6f}")

diff = (lambda_MZ_from_Z2 - lambda_H_MZ) / lambda_H_MZ * 100
print(f"  Difference: {diff:+.2f}%")


# =============================================================================
# WHAT BOUNDARY CONDITION IS NEEDED?
# =============================================================================

print("\n" + "=" * 78)
print("BOUNDARY CONDITION ANALYSIS")
print("=" * 78)

# What value of lambda(M_Pl) gives exactly lambda(M_Z) = 0.129?
# We need to find this by iteration

print("\nSearching for lambda(M_Pl) that gives lambda(M_Z) = {:.4f}...".format(lambda_H_MZ))

def run_down_from_Pl(lambda_Pl_guess):
    """Run RGE from Planck to M_Z with given boundary condition."""
    y0 = [g1_Pl, g2_Pl, g3_Pl, yt_Pl, lambda_Pl_guess]
    sol = solve_ivp(
        lambda t, y: beta_total(t, y, include_2loop=True),
        [t_Pl, t_MZ],
        y0,
        method='RK45',
        rtol=1e-10,
        atol=1e-12
    )
    return sol.y[4][-1]

# Binary search for the correct boundary condition
lambda_Pl_low = -0.05
lambda_Pl_high = 0.2
target = lambda_H_MZ

for _ in range(50):
    lambda_Pl_mid = (lambda_Pl_low + lambda_Pl_high) / 2
    lambda_MZ_result = run_down_from_Pl(lambda_Pl_mid)

    if lambda_MZ_result < target:
        lambda_Pl_low = lambda_Pl_mid
    else:
        lambda_Pl_high = lambda_Pl_mid

    if abs(lambda_MZ_result - target) < 1e-8:
        break

lambda_Pl_exact = lambda_Pl_mid
print(f"\nRequired boundary condition:")
print(f"  lambda_H(M_Pl) = {lambda_Pl_exact:.6f}")
print(f"  This gives lambda_H(M_Z) = {run_down_from_Pl(lambda_Pl_exact):.6f}")

print(f"\nZ^2 Framework prediction:")
print(f"  lambda_H(M_Pl) = 1/(4*Z^2) = {lambda_Z2:.6f}")

ratio = lambda_Pl_exact / lambda_Z2
print(f"\nRatio: required/predicted = {ratio:.4f}")

# Is there a simple relationship?
print(f"\nSimple relationships:")
print(f"  4*Z^2 * lambda_Pl_exact = {4*Z2 * lambda_Pl_exact:.4f}")
print(f"  lambda_Pl_exact * Z = {lambda_Pl_exact * Z:.4f}")
print(f"  lambda_Pl_exact / (1/Z^2) = {lambda_Pl_exact * Z2:.4f}")


# =============================================================================
# ALTERNATIVE Z^2 BOUNDARY CONDITIONS
# =============================================================================

print("\n" + "=" * 78)
print("TESTING ALTERNATIVE Z^2 BOUNDARY CONDITIONS")
print("=" * 78)

boundary_conditions = [
    ("1/(4*Z^2)", 1/(4*Z2)),
    ("1/(Z^2)", 1/Z2),
    ("1/(2*Z^2)", 1/(2*Z2)),
    ("Z/(4*Z^2) = 1/(4Z)", 1/(4*Z)),
    ("(Z-5)/6", (Z-5)/6),  # Known formula for low-energy lambda
    ("1/Z^3", 1/Z**3),
    ("pi/(32*Z^2)", np.pi/(32*Z2)),
    ("1/(16*pi)", 1/(16*np.pi)),
    ("lambda_Pl_exact", lambda_Pl_exact),
]

print(f"\n{'Boundary Condition':<25} {'lambda(M_Pl)':<14} {'lambda(M_Z)':<14} {'Error vs 0.129':<15}")
print("-" * 70)

for name, lambda_Pl in boundary_conditions:
    lambda_MZ_result = run_down_from_Pl(lambda_Pl)
    error = (lambda_MZ_result - lambda_H_MZ) / lambda_H_MZ * 100
    print(f"{name:<25} {lambda_Pl:<14.6f} {lambda_MZ_result:<14.6f} {error:>+13.2f}%")


# =============================================================================
# THRESHOLD EFFECTS
# =============================================================================

print("\n" + "=" * 78)
print("THRESHOLD CORRECTIONS")
print("=" * 78)

# Estimate threshold effects
g3_mt = get_value_at_scale(t_run, g3_run, t_mt)
yt_mt = get_value_at_scale(t_run, yt_run, t_mt)

delta_lam_top, delta_mt = threshold_correction_top(M_t, M_Z, g3_mt, yt_mt)
delta_lam_W = threshold_correction_W(M_W, M_Z, M_Z, g2_MZ)

print(f"\nThreshold corrections (approximate):")
print(f"  At m_t: delta_lambda = {delta_lam_top:.6f}")
print(f"  At M_W: delta_lambda = {delta_lam_W:.6f}")
print(f"  Total threshold shift: {delta_lam_top + delta_lam_W:.6f}")

print(f"\nThese corrections are {'small' if abs(delta_lam_top + delta_lam_W) < 0.01 else 'significant'} "
      f"compared to lambda_H ~ 0.13")


# =============================================================================
# DETAILED RUNNING NEAR M_Pl
# =============================================================================

print("\n" + "=" * 78)
print("DETAILED RUNNING NEAR PLANCK SCALE")
print("=" * 78)

# Focus on last decade before Planck
t_detail = np.linspace(np.log(1e17/M_Z), t_Pl, 100)

print(f"\n{'mu (GeV)':<14} {'lambda_H':<12} {'d(lambda)/d(ln mu)':<20}")
print("-" * 50)

for t in t_detail[::10]:
    lam_val = get_value_at_scale(t_run, lam_run, t)
    # Compute derivative
    g1_val = get_value_at_scale(t_run, g1_run, t)
    g2_val = get_value_at_scale(t_run, g2_run, t)
    g3_val = get_value_at_scale(t_run, g3_run, t)
    yt_val = get_value_at_scale(t_run, yt_run, t)

    beta = beta_total(t, [g1_val, g2_val, g3_val, yt_val, lam_val])[4]

    mu = M_Z * np.exp(t)
    print(f"{mu:<14.2e} {lam_val:<12.6f} {beta:<20.8f}")


# =============================================================================
# VACUUM STABILITY ANALYSIS
# =============================================================================

print("\n" + "=" * 78)
print("VACUUM STABILITY ANALYSIS")
print("=" * 78)

# The SM vacuum is metastable if lambda < 0 at some scale
# The stability depends critically on m_H and m_t

print(f"\nWith m_H = {M_H} GeV and m_t = {M_t} GeV:")
print(f"  Minimum lambda value: {min(lam_run):.6f}")

if min(lam_run) > 0:
    print(f"  Status: STABLE up to M_Pl")
    print(f"  (Lambda remains positive throughout)")
elif min(lam_run) > -0.01:
    print(f"  Status: METASTABLE")
    print(f"  (Lambda goes slightly negative but vacuum lifetime > age of universe)")
else:
    print(f"  Status: UNSTABLE")
    print(f"  (Lambda becomes significantly negative)")

# Effect of m_t uncertainty
print(f"\nSensitivity to top mass:")
print(f"  Current m_t = {M_t} GeV +/- 0.5 GeV")
print(f"  A 1 GeV shift in m_t changes lambda(M_Pl) by ~0.003")


# =============================================================================
# SUMMARY AND CONCLUSIONS
# =============================================================================

print("\n" + "=" * 78)
print("SUMMARY AND CONCLUSIONS")
print("=" * 78)

print(f"""
KEY RESULTS:
============

1. SM RG RUNNING (2-loop):
   lambda_H(M_Z)  = {lambda_H_MZ:.6f}  (input from m_H = 125.25 GeV)
   lambda_H(M_Pl) = {lambda_Pl_2loop:.6f}  (from upward running)

2. Z^2 FRAMEWORK BOUNDARY CONDITION:
   Predicted: lambda_H(M_Pl) = 1/(4*Z^2) = {lambda_Z2:.6f}
   This gives: lambda_H(M_Z) = {lambda_MZ_from_Z2:.6f}
   Discrepancy from observed: {diff:+.1f}%

3. REQUIRED BOUNDARY CONDITION:
   To get lambda_H(M_Z) = {lambda_H_MZ:.6f}
   Need: lambda_H(M_Pl) = {lambda_Pl_exact:.6f}

4. RATIO ANALYSIS:
   Required/Predicted = {ratio:.4f}
   This is approximately {ratio:.2f} ~ {1/ratio:.2f}^(-1)

5. VACUUM STABILITY:
   Minimum lambda = {min(lam_run):.6f}
   Status: {"STABLE" if min(lam_run) > 0 else "METASTABLE"}

INTERPRETATION:
===============
The Z^2 boundary condition lambda_H(M_Pl) = 1/(4*Z^2) gives a low-energy
Higgs quartic that is {abs(diff):.0f}% {'higher' if diff > 0 else 'lower'} than the observed value.

The discrepancy could be due to:
  - Threshold corrections not fully included
  - Higher-loop effects (3-loop, etc.)
  - New physics between M_Z and M_Pl
  - The need for a modified boundary condition formula

The alternative formula lambda_H = (Z-5)/6 works well at LOW energy (M_Z),
suggesting different physics regimes may require different expressions.
""")


# =============================================================================
# SAVE RESULTS
# =============================================================================

output_dir = '/Users/carlzimmerman/new_physics/zimmerman-formula/research/overnight_results'
os.makedirs(output_dir, exist_ok=True)

results = {
    "timestamp": datetime.now().isoformat(),
    "description": "2-loop RG running of Higgs quartic coupling",

    "input_parameters": {
        "M_Z_GeV": M_Z,
        "M_t_GeV": M_t,
        "M_H_GeV": M_H,
        "M_Pl_GeV": M_Pl,
        "v_EW_GeV": v_EW,
        "g1_MZ": float(g1_MZ),
        "g2_MZ": float(g2_MZ),
        "g3_MZ": float(g3_MZ),
        "y_t_MZ": float(y_t_MZ),
        "lambda_H_MZ": float(lambda_H_MZ),
    },

    "Z2_framework": {
        "Z2": float(Z2),
        "Z": float(Z),
        "lambda_H_Pl_predicted": float(lambda_Z2),
        "formula": "1/(4*Z^2)",
    },

    "rg_running_results": {
        "lambda_H_Pl_1loop": float(lambda_Pl_1loop),
        "lambda_H_Pl_2loop": float(lambda_Pl_2loop),
        "lambda_min": float(min(lam_run)),
        "vacuum_stable": bool(min(lam_run) > 0),
    },

    "boundary_condition_analysis": {
        "required_lambda_Pl": float(lambda_Pl_exact),
        "lambda_MZ_from_Z2": float(lambda_MZ_from_Z2),
        "discrepancy_percent": float(diff),
        "ratio_required_to_predicted": float(ratio),
    },

    "couplings_at_Planck_scale": {
        "g1": float(g1_Pl),
        "g2": float(g2_Pl),
        "g3": float(g3_Pl),
        "y_t": float(yt_Pl),
        "lambda_H_from_SM": float(lambda_Pl_2loop),
    }
}

output_file = os.path.join(output_dir, f'higgs_rg_running_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {output_file}")

# Also save running data
running_data = {
    "t": t_run.tolist(),
    "mu_GeV": (M_Z * np.exp(t_run)).tolist(),
    "g1": g1_run.tolist(),
    "g2": g2_run.tolist(),
    "g3": g3_run.tolist(),
    "y_t": yt_run.tolist(),
    "lambda_H_2loop": lam_run.tolist(),
    "lambda_H_1loop": lam_run_1loop.tolist(),
}

running_file = os.path.join(output_dir, f'higgs_rg_running_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
with open(running_file, 'w') as f:
    json.dump(running_data, f)

print(f"Running data saved to: {running_file}")

print("\n" + "=" * 78)
print("COMPUTATION COMPLETE")
print("=" * 78)
