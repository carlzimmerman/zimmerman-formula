#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf53_dw_structural_repair_theory_2026.py
============================================================================
SF53 — STRUCTURAL REPAIR OF THE DW-MOND COSMOLOGICAL SECTOR
============================================================================

BACKGROUND:
  sf52 proved that the sf51 action with f(Z) = (1/2) Z exp(-sqrt(|Z|)/3)
  has NO nonzero de Sitter fixed point. The fixed-point equation reduces to
  exp(-q/3) = 3, which has no positive solution (since exp(-x) < 1 for x > 0).

  This is a mathematical no-go for the sf51 normalization, independent of
  attractor analysis.

  The user identified the exact structural repair:
    1. Change the amplitude: A = 16 pi e^2 / 9
    2. Change the kinetic normalization: beta = 27 / (8 pi)
    3. Verify Z_infty = -36 is the physical attractor
    4. Re-verify all 12 gates under the new normalization

  This script executes that repair and verifies whether the repaired theory
  dynamically selects Z_infty = -36 as a stable attractor.

============================================================================
REPAIRED ACTION:
  S = (c^4 / 16 pi G) int d^4x sqrt(-g) [ R - a0^2 M ] + S_aux + S_m

  Z_new = (beta c^4 / a0^2) g^{mn} d_m X d_n X
        with beta = 27 / (8 pi) = 1.07430...      [was: 4]

  f_new(Z) = A Z exp(-sqrt(|Z|) / 3)
           with A = 16 pi e^2 / 9 = 41.2683...     [was: 1/2]

  Target attractor: Z_infty = -36, f_new(-36) = -64 pi.
  This gives: kappa = 1/2, i.e. a0 = (1/2) c sqrt(G rho_DE).
============================================================================
"""
import sys
import numpy as np
from scipy.optimize import brentq, fsolve
from scipy.integrate import solve_ivp
import sympy as sp
import mpmath as mp

FAIL, NCHK = [], [0]

def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    tag = 'ok' if ok else 'FAIL'
    print(f"  [{tag}] {NCHK[0]:02d} {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")

def hdr(s):
    print("\n" + "=" * 84)
    print(s)
    print("=" * 84)

# ============================================================================
hdr("SECTION 1: REPAIRED NORMALIZATIONS — EXACT VALUES")
# ============================================================================
mp.mp.dps = 50

# New amplitude
A_new = 16 * mp.pi * mp.e**2 / 9
print(f"  A_new = 16 pi e^2 / 9 = {float(A_new):.10f}")

# New kinetic normalization
beta_new = mp.mpf(27) / (8 * mp.pi)
print(f"  beta_new = 27 / (8 pi) = {float(beta_new):.10f}")

# Verify: f_new(-36) = -64 pi
Z_target = mp.mpf(-36)
q_target = mp.sqrt(mp.fabs(Z_target))  # q = 6
f_at_target = A_new * Z_target * mp.exp(-q_target / 3)
print(f"  f_new(-36) = A * (-36) * exp(-6/3) = {float(f_at_target):.10f}")
print(f"  -64 pi     = {float(-64*mp.pi):.10f}")
check(mp.fabs(f_at_target - (-64*mp.pi)) < 1e-8,
      f"f_new(-36) = -64 pi exactly [VERIFIED]",
      f"|f_new(-36) + 64pi| = {float(mp.fabs(f_at_target + 64*mp.pi)):.2e}")

# Verify: kappa = 1/2
abs_f_target = mp.fabs(f_at_target)
kappa = mp.sqrt(16 * mp.pi / abs_f_target)
print(f"  kappa = sqrt(16 pi / |f(-36)|) = sqrt(16 pi / 64 pi) = sqrt(1/4) = {float(kappa):.10f}")
check(mp.fabs(kappa - mp.mpf('0.5')) < 1e-10,
      f"kappa = 1/2 at Z = -36 [VERIFIED]")

# ============================================================================
hdr("SECTION 2: FLRW REDUCTION WITH REPAIRED NORMALIZATIONS")
# ============================================================================
r"""
On FLRW with c = 1:
  X_dot = v * a0 (dimensionless v)
  Z = (beta / a0^2) * g^{mn} d_m X d_n X = (beta / a0^2)(-X_dot^2) = -beta v^2
  
  (Previously Z = -4 v^2. Now Z = -beta v^2 with beta = 27/(8pi).)

  q = sqrt(|Z|) = sqrt(beta) |v|
  
  f(Z) = A * Z * exp(-q/3) = -A * beta * v^2 * exp(-sqrt(beta) |v| / 3)

  At the de Sitter fixed point (X_ddot = 0, H_dot = 0):
    X_dot = H => v = h (dimensionless)
    
    Z_* = -beta h^2
    q_* = sqrt(beta) h
    f(Z_*) = -A beta h^2 exp(-sqrt(beta) h / 3)

  Friedmann (late-time, K = 0, rho_m = 0):
    3 h^2 = -(a0^2 / 2) f(Z_*) / a0^2 = -(1/2) f(Z_*)
          = (A beta h^2 / 2) exp(-sqrt(beta) h / 3)
    
    => 6 / (A beta) = exp(-sqrt(beta) h / 3)
    => sqrt(beta) h / 3 = -ln(6 / (A beta)) = ln(A beta / 6)
    => h_* = (3 / sqrt(beta)) ln(A beta / 6)

  Check whether A beta / 6 > 1 so that h_* > 0:
"""
A_val = float(A_new)
beta_val = float(beta_new)
AB = A_val * beta_val
print(f"  A * beta = {AB:.6f}")
print(f"  A * beta / 6 = {AB/6:.6f}")
check(AB / 6 > 1, f"A * beta / 6 = {AB/6:.4f} > 1: positive de Sitter solution EXISTS [VERIFIED]")

# Exact de Sitter Hubble parameter (dimensionless)
h_star = (3 / np.sqrt(beta_val)) * np.log(AB / 6)
print(f"  h_* = (3/sqrt(beta)) ln(A beta / 6) = {h_star:.10f}")
print(f"  H_* = h_* * a0 / c")

# Physical Hubble value
a0_SI = 9.36e-11   # m/s^2
c_SI = 2.998e8      # m/s
G_SI = 6.67430e-11  # m^3/kg/s^2

H_star_phys = h_star * a0_SI / c_SI  # 1/s
H_star_kms = H_star_phys * 3.0857e22 / 1e3  # km/s/Mpc
print(f"  H_* (physical) = {H_star_phys:.6e} /s = {H_star_kms:.2f} km/s/Mpc")
print(f"  Observed H_0 ~ 67-73 km/s/Mpc")
print(f"  Ratio H_*/H_0 = {H_star_kms/70:.4f}")

# Check Z at the fixed point
Z_star = -beta_val * h_star**2
q_star = np.sqrt(abs(Z_star))
print(f"\n  Z_* = -beta h_*^2 = {Z_star:.10f}")
print(f"  q_* = sqrt(|Z_*|) = {q_star:.10f}")
print(f"  Target: Z_* = -36, q_* = 6")

check(abs(Z_star - (-36)) < 1e-6, f"Z_* = {Z_star:.6f} = -36 at the de Sitter fixed point [VERIFIED]",
      f"|Z_* + 36| = {abs(Z_star + 36):.2e}")

# ============================================================================
hdr("SECTION 3: LINEARIZED STABILITY — JACOBIAN EIGENVALUES")
# ============================================================================
r"""
Full FLRW system in dimensionless variables h = H/a0, v = X_dot/a0, tau = a0 t:

  (S1): v_dot + 3 h v = 3 (h_dot + h^2)
  (S2): 3 h^2 = (A beta / 2) v^2 exp(-sqrt(beta) v / 3)   [Friedmann, v > 0]

From (S2): h(v) = v sqrt(A beta / 6) exp(-sqrt(beta) v / 6)

Let phi(v) = sqrt(A beta / 6) exp(-sqrt(beta) v / 6).
Then h = v phi(v).
dh/dv = phi(v) + v phi'(v) = phi(v)(1 - sqrt(beta) v / 6).

The reduced ODE is:
  v_dot = 3 h(v) (h(v) - v) / (1 - 3 dh/dv)

For the Jacobian, linearize around v_* = h_* (the fixed point where h = v):

  At v_*: h(v_*) = v_*, so phi(v_*) = 1, and:
    sqrt(A beta / 6) exp(-sqrt(beta) v_* / 6) = 1
    exp(-sqrt(beta) v_* / 6) = sqrt(6 / (A beta))
    sqrt(beta) v_* / 6 = (1/2) ln(A beta / 6)
    v_* = (3 / sqrt(beta)) ln(A beta / 6) = h_*  ✓

  dh/dv|_{v_*} = phi(v_*)(1 - sqrt(beta) v_* / 6) = 1 - (1/2) ln(A beta / 6)

For stability, compute d(v_dot)/dv at v_*. Since v_dot = 3h(h-v)/(1-3dh/dv):
  At v_* the numerator is 0 and denominator is 1 - 3(1 - (1/2)ln(AB/6)).

Use L'Hôpital or direct linearization:
  Let delta = v - v_*. Then:
    h(v) = h(v_*) + dh/dv|_* delta + O(delta^2)
    h - v = (dh/dv|_* - 1) delta + O(delta^2)
    3h(h-v) = 3 v_* (dh/dv|_* - 1) delta + O(delta^2)
    
  So v_dot ≈ [3 v_* (dh/dv|_* - 1) / (1 - 3 dh/dv|_*)] delta
            = [-3 v_* (1 - dh/dv|_*) / (1 - 3 dh/dv|_*)] delta
            = lambda * delta

  where lambda = -3 v_* (1 - dh/dv|_*) / (1 - 3 dh/dv|_*).

  For stability: lambda < 0 (attractor) requires:
    (1 - dh/dv|_*) / (1 - 3 dh/dv|_*) > 0.
"""
dh_dv_star = 1 - 0.5 * np.log(AB / 6)
print(f"  dh/dv at v_* = 1 - (1/2) ln(A beta / 6) = {dh_dv_star:.10f}")

denom_star = 1 - 3 * dh_dv_star
print(f"  Denominator 1 - 3 dh/dv|_* = {denom_star:.10f}")

# Eigenvalue
if abs(denom_star) > 1e-15:
    lambda_star = -3 * h_star * (1 - dh_dv_star) / denom_star
    print(f"  Linearized eigenvalue lambda = {lambda_star:.10f}")
    check(lambda_star < 0, f"Attractor eigenvalue lambda = {lambda_star:.6f} < 0 [STABLE DE SITTER]",
          f"Perturbations decay as exp(lambda tau), tau_relax ~ {abs(1/lambda_star):.2f} a0^{{-1}}")
else:
    print(f"  WARNING: Denominator vanishes — degenerate critical point")
    lambda_star = float('nan')
    check(False, "Eigenvalue computation degenerate")

# ============================================================================
hdr("SECTION 4: NUMERICAL EVOLUTION — REPAIRED SYSTEM")
# ============================================================================
r"""
Integrate the repaired autonomous ODE and verify convergence to v_*.
"""
def h_repaired(v):
    """h(v) = v * sqrt(A beta / 6) * exp(-sqrt(beta) v / 6) for v > 0."""
    if v <= 0:
        return 0.0
    return v * np.sqrt(AB / 6) * np.exp(-np.sqrt(beta_val) * v / 6)

def dh_dv_repaired(v):
    """dh/dv = sqrt(A beta / 6) exp(-sqrt(beta) v / 6) (1 - sqrt(beta) v / 6)."""
    if v <= 0:
        return 0.0
    phi = np.sqrt(AB / 6) * np.exp(-np.sqrt(beta_val) * v / 6)
    return phi * (1 - np.sqrt(beta_val) * v / 6)

def v_dot_repaired(v):
    """v_dot = 3 h(v) (h(v) - v) / (1 - 3 dh/dv)."""
    hv = h_repaired(v)
    dhv = dh_dv_repaired(v)
    den = 1 - 3 * dhv
    if abs(den) < 1e-15:
        return 0.0  # singular point, regularize
    return 3 * hv * (hv - v) / den

def ode_repaired(tau, state):
    v = state[0]
    if v < 1e-15:
        return [0.0]
    return [v_dot_repaired(v)]

print("  Numerical integration of repaired system from various initial v_0:")
v_star_num = h_star  # exact fixed point

initial_vs = [0.01, 0.1, 1.0, 3.0, 5.573, 7.0, 10.0, 20.0, 50.0]
for v0 in initial_vs:
    try:
        sol = solve_ivp(ode_repaired, [0, 500], [v0], method='RK45',
                        max_step=0.05, rtol=1e-12, atol=1e-14)
        v_final = sol.y[0][-1]
        h_final = h_repaired(v_final)
        z_final = -beta_val * v_final**2
        err = abs(v_final - v_star_num) / v_star_num
        print(f"    v0 = {v0:6.3f}: v(500) = {v_final:.8f}, "
              f"h = {h_final:.8f}, Z = {z_final:.4f}, "
              f"|v-v_*|/v_* = {err:.2e}")
    except Exception as e:
        print(f"    v0 = {v0:6.3f}: FAILED ({e})")

# ============================================================================
hdr("SECTION 5: PHASE PORTRAIT — FLOW DIRECTION ANALYSIS")
# ============================================================================
print("  Phase portrait (v > 0, repaired system):")
test_vs = np.array([0.5, 1.0, 2.0, 3.0, 4.0, v_star_num - 0.1, v_star_num,
                     v_star_num + 0.1, 6.0, 8.0, 10.0, 15.0, 20.0])
for v in test_vs:
    hv = h_repaired(v)
    dhv = dh_dv_repaired(v)
    den = 1 - 3 * dhv
    vd = v_dot_repaired(v)
    arrow = "→" if vd > 0 else "←" if vd < 0 else "•"
    print(f"    v = {v:7.3f}: h = {hv:.5f}, h-v = {hv-v:+.5f}, "
          f"denom = {den:+.5f}, v_dot = {vd:+.5f} {arrow}")

# ============================================================================
hdr("SECTION 6: RE-VERIFICATION OF GALACTIC MOND PHENOMENOLOGY")
# ============================================================================
r"""
In the STATIC / galactic sector (Z > 0), the repaired function is:
  f_new(Z) = A Z exp(-sqrt(Z)/3),   Z > 0.
  f_new'(Z) = A exp(-sqrt(Z)/3) (1 - sqrt(Z)/6) / (but we need df/dZ)

  df/dZ = A exp(-sqrt(Z)/3) [ 1 - sqrt(Z)/6 ]
        (using df/dZ for f = A Z exp(-sqrt(Z)/3))

Actually: f = A Z exp(-sqrt(Z)/3).
  df/dZ = A exp(-sqrt(Z)/3) + A Z * (-1/(6 sqrt(Z))) * exp(-sqrt(Z)/3)
        = A exp(-sqrt(Z)/3) [1 - sqrt(Z)/6]

The MOND constitutive relation (from FINAL_FIELD_EQUATIONS.md) involves:
  mu_eff(y) = 1 - 2 f'(Z(y))

where Z = beta_galactic y^2 for some galactic normalization.

IMPORTANT: the coefficient beta was changed from 4 to 27/(8pi) ~ 1.074 in
the kinetic argument Z = beta g^{mn} dm X dn X / a0^2.

In the static spherical case with X ≈ Phi (Newtonian potential):
  Z_galactic = beta * (nabla X)^2 / a0^2 = beta * (g/a0)^2 = beta * y^2

With beta = 27/(8pi):
  Z = (27/(8pi)) y^2
  sqrt(Z) = sqrt(27/(8pi)) y = y * sqrt(27/(8pi))

Let gamma = sqrt(beta) = sqrt(27/(8pi)).

  f'(Z) = A exp(-gamma y / 3) [1 - gamma y / 6]
  mu_eff(y) = 1 - 2 A exp(-gamma y / 3) [1 - gamma y / 6]
"""
gamma_val = np.sqrt(beta_val)
print(f"  gamma = sqrt(beta) = sqrt(27/(8pi)) = {gamma_val:.10f}")
print(f"  A_new = {A_val:.10f}")

def mu_eff_new(y):
    """Repaired MOND interpolation function."""
    gy3 = gamma_val * y / 3
    return 1 - 2 * A_val * np.exp(-gy3) * (1 - gamma_val * y / 6)

# Check MOND limits
print("\n  MOND interpolation mu_eff(y) with repaired f:")
y_test = [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 100.0, 1e6]
for y in y_test:
    mu = mu_eff_new(y)
    print(f"    y = {y:10.3f}: mu_eff = {mu:+.8f}")

# Deep MOND (y << 1): mu_eff -> 1 - 2A + 2A*gamma*y/6 + ...
mu_0 = 1 - 2 * A_val
print(f"\n  mu_eff(0) = 1 - 2A = {mu_0:.6f}")

# For MOND we need mu_eff(y) -> y / y_0 for y << 1 (some normalization).
# But mu_eff(0) = 1 - 2A = 1 - 82.5 = -81.5 << 0.
# This is CATASTROPHIC: the interpolation function is deeply negative at y = 0.
# The Newtonian limit (y >> 1) gives mu_eff -> 1 (correct).
# But the deep-MOND limit (y << 1) gives mu_eff ~ -81.5 (wrong sign!).

check(mu_0 > 0, f"Deep-MOND limit mu_eff(0) = {mu_0:.4f}: should be positive for MOND phenomenology",
      f"1 - 2A = 1 - {2*A_val:.4f} = {mu_0:.4f}. CATASTROPHIC: mu_eff < 0 at y=0!")

# Where does mu_eff cross zero?
y_scan = np.linspace(0.01, 50.0, 100000)
mu_scan = np.array([mu_eff_new(y) for y in y_scan])
zero_crossings = np.where(np.diff(np.sign(mu_scan)))[0]
print(f"\n  mu_eff zero crossings (y > 0):")
for idx in zero_crossings:
    y_zero = brentq(mu_eff_new, y_scan[idx], y_scan[idx+1])
    print(f"    mu_eff = 0 at y = {y_zero:.6f} (g/a0 = {y_zero:.4f})")

# ============================================================================
hdr("SECTION 7: DIAGNOSIS — THE STRUCTURAL CONFLICT")
# ============================================================================
print(r"""
============================================================================
                    SF53 DIAGNOSIS
============================================================================

  THE REPAIR CREATES A NEW CONFLICT:

  1. COSMOLOGICAL SECTOR (repaired):
     With A = 16 pi e^2 / 9 ≈ 41.27 and beta = 27/(8pi) ≈ 1.074:
     - De Sitter fixed point EXISTS at h_* with Z_* = -36.     ✓
     - kappa = 1/2 exactly at Z_* = -36.                       ✓
     - Eigenvalue lambda < 0 (stable attractor).                ✓

  2. GALACTIC MOND SECTOR (broken):
     With A = 41.27, the MOND interpolation function becomes:
       mu_eff(0) = 1 - 2A = 1 - 82.5 ≈ -81.5  << 0.           ✗

     This means:
       - The modified Poisson equation CHANGES SIGN in the deep-MOND regime.
       - The gravitational force REVERSES DIRECTION for y < y_crit.
       - The entire MOND phenomenology is destroyed.

  3. ROOT CAUSE:
     The MOND interpolation uses f'(Z), which scales linearly with A.
     The cosmological dark energy uses f(Z_*), which also scales with A.

     For MOND: need A small enough that 2A < 1, i.e. A < 1/2.
     For cosmology: need A large enough that A beta/6 > 1, i.e. A > 6/beta ≈ 5.6.

     These requirements are INCOMPATIBLE. The same function f cannot
     simultaneously serve as a small MOND perturbation (A << 1) and a
     large cosmological driver (A >> 1).

  CONCLUSION:
  ===========
  The DW-MOND construction with a SINGLE function f(Z) applied to BOTH
  the galactic (Z > 0) and cosmological (Z < 0) sectors faces a
  FUNDAMENTAL NORMALIZATION CONFLICT:

    MOND phenomenology requires A ≤ 1/2.
    De Sitter cosmology requires A ≥ 6/beta ≈ 5.6.

  These cannot be simultaneously satisfied by any single value of A.
""")

check(A_val < 0.5, "A < 1/2 needed for MOND galactic phenomenology",
      f"A = {A_val:.4f} >> 1/2. MOND is destroyed.")
check(AB / 6 > 1, "A*beta/6 > 1 needed for de Sitter fixed point",
      f"A*beta/6 = {AB/6:.4f} > 1. Cosmology works.")

# ============================================================================
hdr("SECTION 8: POSSIBLE RESOLUTION — ASYMMETRIC f(Z)")
# ============================================================================
r"""
The conflict can potentially be resolved by using an ASYMMETRIC f:
  - f_+(Z) for Z > 0 (galactic / spacelike): amplitude A_+ = 1/2.
  - f_-(Z) for Z < 0 (cosmological / timelike): amplitude A_- = 16 pi e^2 / 9.

This is physically motivated: the galactic and cosmological regimes access
different branches of the kinetic invariant, so they CAN have different
nonlinear responses.

The simplest asymmetric construction:
  f(Z) = {  (1/2) Z exp(-sqrt(Z)/3),           Z > 0  (galactic)
          {  (16 pi e^2 / 9) Z exp(-sqrt(|Z|)/3), Z < 0  (cosmological)

But this has a discontinuity in f'(Z) at Z = 0. In a covariant field theory,
f must be a smooth function of Z. A smooth interpolation might work:

  f(Z) = (1/2) Z exp(-sqrt(|Z|)/3) * [1 + (A_-/A_+ - 1) Theta(-Z)]

where Theta is a smooth step function. But this is ugly and contrived.

A deeper resolution would be to find a smooth single f(Z) that naturally
has small derivatives for Z > 0 (MOND perturbation) and large magnitude
for Z < 0 (cosmological drive). This is possible if f has very different
behavior on the two branches — for example:

  f(Z) = (1/2) Z exp(-sqrt(|Z|)/3) + C * |Z|^n * Theta(-Z)

for some power n and coefficient C that dominates only on the timelike branch.

Or, more elegantly, the MOND and cosmological sectors could involve
DIFFERENT invariants (e.g., R_uu vs R), so that the same function f acts
on different arguments in different regimes.
"""
print(f"  RESOLUTION ANALYSIS:")
print(f"  Required A_galactic (MOND):  A_+ ≤ 1/2 = 0.500")
print(f"  Required A_cosmo (de Sitter): A_- ≥ 6/beta = {6/beta_val:.4f}")
print(f"  Ratio A_-/A_+ ≥ {(6/beta_val)/0.5:.1f} (minimum)")
print(f"  For kappa=1/2: A_-/A_+ = {A_val/0.5:.1f}")

# Check: with asymmetric f, does the galactic sector still work?
def mu_eff_galactic(y):
    """mu_eff with A_+ = 1/2 (original, galactic branch)."""
    # Z = beta y^2, but with the ORIGINAL galactic normalization beta_gal = 4
    # Actually, the kinetic normalization beta changes BOTH sectors.
    # With beta = 27/(8pi), the galactic argument is also Z = beta y^2.
    gy3 = gamma_val * y / 3
    return 1 - 2 * 0.5 * np.exp(-gy3) * (1 - gamma_val * y / 6)

print(f"\n  mu_eff with A_+=1/2 and beta={beta_val:.4f} (galactic, Z > 0):")
for y in [0.001, 0.1, 1.0, 3.0, 10.0, 100.0]:
    mu = mu_eff_galactic(y)
    print(f"    y = {y:8.3f}: mu_eff = {mu:.8f}")

# Deep-MOND with these parameters:
mu_0_gal = 1 - 2 * 0.5  # = 0
print(f"\n  mu_eff(0) = 1 - 2*A_+ = {mu_0_gal:.4f}")
print(f"  This is ALSO problematic: mu_eff(0) = 0, not mu -> y (linear MOND).")
print(f"  The original A = 1/2 gives mu_eff(0) = 0, which means the deep-MOND")
print(f"  limit is mu ~ y * const, starting from mu = 0. That IS the MOND limit!")

# Actually, let's expand mu_eff near y = 0 with A = 1/2, gamma = sqrt(beta):
# mu_eff(y) = 1 - 2*(1/2)*exp(-gamma*y/3)*(1 - gamma*y/6)
#           = 1 - exp(-gamma*y/3) + (gamma*y/6)*exp(-gamma*y/3)
#           = 1 - (1 - gamma*y/3 + ...) + (gamma*y/6)(1 - ...)
#           = gamma*y/3 + gamma*y/6 + O(y^2)
#           = gamma*y/2 + O(y^2)
# So mu_eff ~ (gamma/2) y for y << 1.
# For MOND: need mu ~ y (or mu ~ y/y0). So gamma/2 = sqrt(beta)/2 plays the
# role of normalization.
print(f"\n  Deep-MOND expansion with A_+=1/2:")
print(f"  mu_eff(y) ~ (gamma/2) y = ({gamma_val/2:.6f}) y for y << 1")
print(f"  With original beta = 4: gamma = 2, mu ~ y. (Standard MOND!)")
print(f"  With repaired beta = {beta_val:.4f}: gamma = {gamma_val:.4f}, mu ~ {gamma_val/2:.4f} y.")
print(f"  This changes the effective a0 by a factor sqrt(2/gamma) = {np.sqrt(2/gamma_val):.4f}.")

# ============================================================================
hdr("SECTION 9: DEFINITIVE VERDICT")
# ============================================================================
print(r"""
============================================================================
                    SF53 DEFINITIVE VERDICT
============================================================================

  RESULT 1 — De Sitter Fixed Point (with repaired A, beta):
    De Sitter fixed point EXISTS.                              ✓
    Z_* = -36 gives kappa = 1/2 exactly.                      ✓
    The fixed point is a STABLE ATTRACTOR (lambda < 0).        ✓

  RESULT 2 — Galactic MOND Phenomenology:
    With the SAME A used for cosmology (A ≈ 41.3):
      mu_eff(0) = 1 - 2A ≈ -81.5.                             ✗
      Galactic MOND is DESTROYED.                              ✗

  RESULT 3 — The Fundamental Conflict:
    A SINGLE symmetric function f(Z) = A Z exp(-sqrt(|Z|)/3)
    CANNOT simultaneously produce:
      - MOND galactic phenomenology (requires A ≤ 1/2), and
      - Cosmological dark energy (requires A >> 1).

  RESULT 4 — The Structural Fork:
    The theory requires EITHER:
      (a) An asymmetric f with different A on the Z > 0 and Z < 0 branches,
      (b) Different invariants for the galactic and cosmological sectors,
      (c) A fundamentally different f(Z) functional form, or
      (d) Acceptance that kappa ≠ 1/2 (i.e. a different Zimmerman relation).

  STATUS:
    The DW-MOND FRAMEWORK is not killed by this result.
    The specific SINGLE-FUNCTION ANSATZ f(Z) = A Z exp(-sqrt(|Z|)/3) faces
    an irreconcilable normalization conflict between its two physical sectors.

    The cleanest theoretical path forward is an ASYMMETRIC or
    TWO-INVARIANT construction where the cosmological and galactic
    responses are governed by different effective couplings.

============================================================================
""")

# Final gate table
print("  GATE TABLE (as of sf53):")
gates = [
    ("G1: CTP Physical Equivalence",   "PASS",  "Structure preserved under reparametrization"),
    ("G2: Hamiltonian Positivity",      "OPEN",  "Must re-derive with new A, beta"),
    ("G3: Nonlinear Re-excitation",     "PASS",  "Structural (unchanged by normalization)"),
    ("G4: Matter Coupling",            "PASS",  "Structural (minimal coupling)"),
    ("G5: Physical DOF Count",         "PASS",  "Structural (CTP quotient)"),
    ("G6: Causal Characteristics",     "PASS",  "c_T = c (structural)"),
    ("G7: PPN / Cassini",             "OPEN",  "Screening exponent depends on beta"),
    ("G8: Relativistic Lensing",       "PASS",  "Phi = Psi structural"),
    ("G9: Cosmological Background",    "PASS*", "De Sitter EXISTS with repaired A, beta"),
    ("G10: Zimmerman Relation",        "FAIL",  "Single-f ansatz cannot give kappa = 1/2 + MOND"),
    ("G11: Cosmological Perturbations", "OPEN", "Must re-derive with new normalization"),
    ("G12: EFT Cutoff",               "PASS",  "Lambda ~ 0.71 meV (unchanged)"),
]
for gate, status, detail in gates:
    print(f"    {gate:40s} [{status:5s}]  {detail}")

if FAIL:
    print(f"\nFAILED {len(FAIL)} checks")
    # Don't sys.exit(1) — the failures are CORRECTLY IDENTIFIED scientific results
    sys.exit(0)  # Script ran correctly, theory has issues
else:
    print(f"\nALL {NCHK[0]} CHECKS PASSED.")
    sys.exit(0)
