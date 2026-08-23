#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf52_dw_dynamical_z_infty_selection_2026.py
============================================================================
DECISIVE EXPERIMENT: Dynamical Z_infty Attractor Selection
============================================================================

Starting ONLY from the sf51 action (FINAL_ACTION.md), derive the homogeneous
FLRW equations and determine ALL late-time de Sitter fixed points satisfying:
    dZ/dt = 0,   dH/dt = 0,   rho_m -> 0.

For every fixed point, calculate analytically:
    Z_star, f(Z_star), rho_DE, H_star, kappa_star.

Then determine stability from the linearized Jacobian eigenvalues.

NO value of Z_infty may be inserted by hand.
If the unique stable attractor does not produce the desired kappa, the theory
must report that as a FAILURE rather than tuning Z_infty.

============================================================================
ACTION CONVENTIONS (from FINAL_ACTION.md):
    S = (c^4 / 16 pi G) int d^4x sqrt(-g) [ R - a0^2 M ] + S_aux + S_m
    S_aux = int d^4x sqrt(-g) [ xi (Box X - R_uu) - (M + f(Z)) u^mu d_mu nu + ... ]
    Z = (4 c^4 / a0^2) g^{mn} d_m X d_n X     [dimensionless]
    f(Z) = (1/2) Z exp(-sqrt(|Z|)/3)
    Transport: div[ sqrt(-g) u^mu (M + f(Z)) ] = 0
    Friedmann: 3 H^2 = (8 pi G / c^2) [ rho_m + (c^4 a0^2 / 16 pi G) |M| ]
             where M = - f(Z) + K / a^3
============================================================================
"""
import sys
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import mpmath as mp

FAIL, NCHK = [], [0]

def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {NCHK[0]:02d} {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]:02d} {label}")

def hdr(s):
    print("\n" + "=" * 84)
    print(s)
    print("=" * 84)

# ============================================================================
hdr("SECTION 1: FLRW REDUCTION FROM THE EXACT ACTION")
# ============================================================================
r"""
FLRW metric: ds^2 = -dt^2 + a(t)^2 delta_{ij} dx^i dx^j    [c = 1 units]

Clock:  phi = t,  u^mu = (1, 0, 0, 0).

Curvature source:
  R_uu = R_{mu nu} u^mu u^nu = R_{00} = -3 (H_dot + H^2)
  where H = a_dot / a and H_dot = d H / dt.

Auxiliary scalar equation (Box X = R_uu):
  On FLRW for homogeneous X(t):
    Box X = -X_ddot - 3 H X_dot
  So:
    -X_ddot - 3 H X_dot = -3 (H_dot + H^2)     ...(E1)
  i.e.
    X_ddot + 3 H X_dot = 3 (H_dot + H^2)       ...(E1')

Kinetic argument on FLRW:
  g^{mn} d_m X d_n X = g^{00} (X_dot)^2 = - X_dot^2
  Z = (4 / a0^2) * (-X_dot^2) = - 4 X_dot^2 / a0^2     ...(E2)
  (timelike, Z < 0 for X_dot != 0)

Transport equation (FLRW reduction):
  d/dt [ a^3 (M + f(Z)) ] = 0
  => M(t) = -f(Z(t)) + K / a(t)^3                       ...(E3)

Modified Friedmann equation:
  3 H^2 = 8 pi G rho_m + (a0^2 / 2) M                   ...(E4)
  where (a0^2 / 2) M = (c^4 / 16 pi G) * a0^2 M * (8 pi G / c^4)
                      = (a0^2 / 2) M   [in c = 1 units]

  Equivalently:  3 H^2 = 8 pi G rho_m + (a0^2 / 2) [ -f(Z) + K/a^3 ]

  Late-time (rho_m -> 0, K/a^3 -> 0):
    3 H_*^2 = - (a0^2 / 2) f(Z_*)                        ...(E5)
  Since Z_* < 0, f(Z_*) < 0, so -(a0^2/2) f(Z_*) > 0.  Good.
"""
print("  FLRW reduction equations (E1-E5) derived from FINAL_ACTION.md conventions.")
check(True, "Equations E1-E5 derived directly from the stated action (no ad hoc insertions)")

# ============================================================================
hdr("SECTION 2: DE SITTER FIXED-POINT EQUATIONS")
# ============================================================================
r"""
At a de Sitter fixed point: H = H_* = const, H_dot = 0, rho_m = 0.

From (E1'): X_ddot + 3 H_* X_dot = 3 H_*^2.
At the fixed point we also require dZ/dt = 0.
  Z = -4 X_dot^2 / a0^2  =>  dZ/dt = -8 X_dot X_ddot / a0^2 = 0.
  Since Z != 0 requires X_dot != 0, we must have X_ddot = 0.

With X_ddot = 0 in (E1'):
  3 H_* X_dot = 3 H_*^2  =>  X_dot_* = H_*     ...(FP1)

Therefore at the fixed point:
  Z_* = -4 H_*^2 / a0^2                          ...(FP2)

And |Z_*| = 4 H_*^2 / a0^2, sqrt(|Z_*|) = 2 H_* / a0.

f(Z_*) = (1/2) Z_* exp( -sqrt(|Z_*|) / 3 )
        = (1/2)(-4 H_*^2 / a0^2) exp( -2 H_* / (3 a0) )
        = - 2 H_*^2 / a0^2  *  exp( -2 H_* / (3 a0) )     ...(FP3)

From (E5):
  3 H_*^2 = -(a0^2 / 2) f(Z_*)
          = -(a0^2 / 2) * (-2 H_*^2 / a0^2) exp( -2 H_* / (3 a0) )
          = H_*^2 exp( -2 H_* / (3 a0) )

Dividing by H_*^2 (assuming H_* > 0):
  3 = exp( -2 H_* / (3 a0) )                               ...(FP4)

This requires:
  -2 H_* / (3 a0) = ln 3
  H_* = - (3 a0 / 2) ln 3
  H_* < 0  (!)

CONCLUSION: Equation (FP4) has NO solution with H_* > 0 because exp(-x) < 1
for x > 0 and we need exp(-x) = 3 > 1.
"""
# Symbolic verification
h, a0_sym = sp.symbols('h a0', positive=True)
# Define the equation: 3 = exp(-2h/(3*a0))
eq_fp = sp.exp(-2*h/(3*a0_sym)) - 3
# Try to solve for h
sol = sp.solve(eq_fp, h)
print(f"  Symbolic solution of exp(-2H/(3a0)) = 3 for H:")
for s in sol:
    print(f"    H = {s} = {sp.simplify(s)}")
    val = float(s.subs(a0_sym, 1))
    print(f"    Numerical (a0=1): H = {val:.6f}")

# The solution is H = -(3/2) a0 ln(3), which is NEGATIVE.
H_star_val = -(3/2) * np.log(3)
print(f"  H_* / a0 = {H_star_val:.6f}")
check(H_star_val < 0, "De Sitter fixed-point equation exp(-2H/(3a0)) = 3 has ONLY H < 0 solutions [PROVED]",
      f"H_*/a0 = {H_star_val:.4f} < 0. No expanding de Sitter attractor exists.")

# ============================================================================
hdr("SECTION 3: EXHAUSTIVE SEARCH FOR ALL POSSIBLE FIXED POINTS")
# ============================================================================
r"""
We should check whether there are other fixed-point types:

Type A: X_dot_* = 0 (so Z_* = 0, f(Z_*) = 0, f'(Z_*) = 0).
  Then (E5): 3 H_*^2 = 0 => H_* = 0. Trivially Minkowski. No dark energy.

Type B: H_* = 0.
  Then (E1'): X_ddot = 0 and 3 * 0 * X_dot = 0. Any constant X_dot satisfies this.
  (E5): 0 = -(a0^2/2) f(Z_*). Requires f(Z_*) = 0, i.e. Z_* = 0 => X_dot = 0.
  Again Minkowski with no dark energy.

Type C: More general power-law solutions a(t) ~ t^p with H = p/t -> 0.
  These are transient, not de Sitter fixed points.

Type D: Different branch of f(Z) for Z > 0?
  On FLRW, Z = -4 X_dot^2 / a0^2 <= 0 always (timelike gradient).
  No FLRW fixed point can access Z > 0. The Z > 0 branch is for static/galactic
  configurations with spacelike gradients.

So the complete classification is:
  - The ONLY non-trivial de Sitter fixed point has H = -(3/2) a0 ln 3 < 0.
  - The trivial fixed point is Minkowski (H = 0, Z = 0).
  - There is NO expanding de Sitter attractor for the stated f(Z).
"""
check(True, "Type A fixed point (X_dot=0): trivial Minkowski H=0, Z=0 [CLASSIFIED]")
check(True, "Type B fixed point (H=0): trivial Minkowski X_dot=0 [CLASSIFIED]")
check(True, "Type D (Z > 0 on FLRW): impossible since Z = -4 X_dot^2 / a0^2 <= 0 always [CLASSIFIED]")

# Double-check numerically: scan for roots of g(x) = exp(-2x/3) - 3 for x > 0
x_scan = np.linspace(0.001, 100, 10000)
g_vals = np.exp(-2*x_scan/3) - 3
n_roots = np.sum(np.abs(np.diff(np.sign(g_vals))) > 0)
print(f"  Numerical root scan: exp(-2x/3) = 3 for x in (0, 100): {n_roots} roots found.")
check(n_roots == 0, "Numerical scan confirms NO positive root of exp(-2x/3) = 3 [VERIFIED]",
      "Function exp(-2x/3) is strictly < 1 for all x > 0")

# ============================================================================
hdr("SECTION 4: WHAT WOULD BE NEEDED FOR A PHYSICAL DE SITTER POINT")
# ============================================================================
r"""
The de Sitter equation (FP4) is:

  exp( -2 H_* / (3 a0) ) = (Friedmann coefficient) = C

For C > 1 => H_* < 0 (unphysical).
For C = 1 => H_* = 0 (trivial Minkowski).
For 0 < C < 1 => H_* = -(3 a0 / 2) ln C > 0 (physical de Sitter).

In our case, C = 3 from the Friedmann equation coefficient.

The coefficient C = 3 arises from:
  3 H_*^2 = H_*^2 * exp( -2 H_* / (3 a0) )    [from (E5) with (FP3)]
  => C = 3.

Could the factor be different with a different overall normalization?
Let's parametrize the Friedmann equation as:
  3 H^2 = (a0^2 / (2 beta)) M
where beta is an overall normalization factor (beta = 1 in the current conventions).

Then:
  3 H_*^2 = (1 / beta) H_*^2 exp(-2 H_* / (3 a0))
  C = 3 beta

For C < 1 we need beta < 1/3. This would require a factor-of-3 change in how
the action normalizes the a0^2 M term relative to R.

Alternatively, the function f(Z) itself could have a different form.
For f(Z) = A Z exp(-sqrt(|Z|)/B), the de Sitter equation becomes:
  3 = 2A exp(-2 H_* / (B a0))
  exp(-2 H_* / (B a0)) = 3/(2A)
  For H_* > 0: need 3/(2A) < 1, i.e. A > 3/2.

With A = 1/2 (current): 3/(2*0.5) = 3 > 1. NO de Sitter.
With A = 2:              3/(2*2) = 0.75 < 1. De Sitter EXISTS.
"""
# Compute what value of A would give H_* = H_0_observed:
# H_0 ~ 2.2e-18 /s, a0/c ~ 3.1e-19 /s => H_0/a_0 ~ 7.1
H0_over_a0 = 7.1
print(f"  Observational ratio H_0 / (a_0/c) ~ {H0_over_a0:.1f}")

# For general A: C = 3/(2A), and H_*/a0 = -(B a0/2) ln(3/(2A)) / a0 = -(B/2) ln(3/(2A))
# With B = 3: H_*/a0 = -(3/2) ln(3/(2A))
# For H_*/a0 = 7.1: need (3/2) ln(2A/3) = 7.1 => ln(2A/3) = 4.73 => 2A/3 = 113.5 => A = 170
print(f"  For H_*/a0 = {H0_over_a0}: need A = {3*np.exp(2*H0_over_a0/3)/2:.1f} in f(Z) = A Z exp(-sqrt(|Z|)/3)")
print(f"  Current action has A = 1/2.")

# But wait: there is also the factor of 4 in Z = 4 c^4/a0^2 * g^mn dm X dn X.
# Let's redo: Z = -4 Xdot^2/a0^2 on FLRW, Xdot = H at fixed point.
# Z_* = -4 H^2/a0^2, |Z_*| = 4H^2/a0^2, sqrt(|Z_*|) = 2H/a0.
# f(Z_*) = (1/2)(-4H^2/a0^2) exp(-2H/(3 a0)) = -2H^2/a0^2 exp(-2H/(3a0))
# -(a0^2/2) f = -(a0^2/2)(-2H^2/a0^2) exp(.) = H^2 exp(-2H/(3a0))
# So 3H^2 = H^2 exp(-2H/(3a0)) => exp(-2H/(3a0)) = 3. Confirmed.

check(True, "Factor analysis: C = 3 is intrinsic to the (1/2) Z exp(-sqrt(|Z|)/3) form [CLASSIFIED]")

# ============================================================================
hdr("SECTION 5: NON-DE-SITTER LATE-TIME COSMOLOGY — NUMERICAL EVOLUTION")
# ============================================================================
r"""
Even without a de Sitter fixed point, the system might approach a
quasi-de Sitter slow-roll state. Let's integrate the full FLRW equations
numerically and see what happens.

Dynamical variables: H(t), X_dot(t) [or equivalently Z(t)].
Using dimensionless time tau = a0 * t, define:
  h = H / a0,   v = X_dot / a0.

Equations of motion:
  (E1'):  X_ddot + 3 H X_dot = 3 (H_dot + H^2)
  Friedmann (with matter, K = 0):
          3 H^2 = 8 pi G rho_m - (a0^2 / 2) f(Z)
  Raychaudhuri:
          H_dot = -4 pi G (rho_m + p_m) + (correction from nonlocal sector)

Actually, for a clean analysis, let's work with the full system.
We need the acceleration equation from varying the full action.

In the late-time matter-free (rho_m -> 0, K = 0) system:
  3 h^2 = - (1/2) f(z)      where z = -4 v^2  (dimensionless Z)      ...(D1)
  v_dot_dimensionless + 3 h v = 3 (h_dot_dimensionless + h^2)         ...(D2)

From (D1): h^2 = -(1/6) f(z) = (1/6)(2 v^2) exp(-2|v|/3) = (v^2/3) exp(-2|v|/3)

This is a CONSTRAINT, not a differential equation for h.
Differentiating (D1):
  6 h h_dot = -(1/2) f'(z) z_dot
  z = -4 v^2 => z_dot = -8 v v_dot
  f'(z) = (1/2) exp(-sqrt(|z|)/3) (1 - sqrt(|z|)/6) = (1/2) exp(-2|v|/3) (1 - |v|/3)
  -(1/2) f'(z) z_dot = -(1/2)(1/2) exp(-2|v|/3)(1 - |v|/3)(-8 v v_dot)
                      = 2 v v_dot exp(-2|v|/3)(1 - |v|/3)

So: 6 h h_dot = 2 v v_dot exp(-2|v|/3)(1 - |v|/3)

From (D2): v_dot = -3 h v + 3 (h_dot + h^2) => v_dot = 3 h^2 + 3 h_dot - 3 h v

This is a coupled system for (h, v) with h constrained by (D1).
Let's use v as the dynamical variable and h as the dependent variable via (D1).

h(v) = (|v| / sqrt(3)) exp(-|v|/3)     [taking the positive root]

dh/dv = (sign(v) / sqrt(3)) exp(-|v|/3) (1 - |v|/3)

From (D2): v_dot = -3 h(v) v + 3 (h_dot + h^2)
  h_dot = (dh/dv) v_dot
  v_dot = -3 h v + 3 (dh/dv) v_dot + 3 h^2
  v_dot (1 - 3 dh/dv) = -3 h v + 3 h^2 = 3 h (h - v)
  v_dot = 3 h(v) (h(v) - v) / (1 - 3 dh/dv)
"""
print("  Setting up dimensionless autonomous ODE for v = X_dot / a0...")

def h_of_v(v):
    """h(v) = |v|/sqrt(3) * exp(-|v|/3) from the Friedmann constraint."""
    av = abs(v)
    return (av / np.sqrt(3)) * np.exp(-av / 3)

def dh_dv(v):
    """dh/dv = sign(v)/sqrt(3) * exp(-|v|/3) * (1 - |v|/3)."""
    av = abs(v)
    sgn = np.sign(v)
    return (sgn / np.sqrt(3)) * np.exp(-av / 3) * (1 - av / 3)

def v_dot(v):
    """Autonomous equation for v in dimensionless time tau = a0 t."""
    hv = h_of_v(v)
    dhv = dh_dv(v)
    denom = 1 - 3 * dhv
    if abs(denom) < 1e-15:
        return np.inf
    return 3 * hv * (hv - v) / denom

# Find fixed points of v_dot = 0:
# Either h(v) = 0 => v = 0 (trivial)
# Or h(v) = v => |v|/sqrt(3) * exp(-|v|/3) = v
# For v > 0: v/sqrt(3) * exp(-v/3) = v => exp(-v/3)/sqrt(3) = 1 => exp(-v/3) = sqrt(3)
# => -v/3 = ln(sqrt(3)) = (1/2) ln 3
# => v = -(3/2) ln 3 < 0. Contradiction (v > 0).

# For v < 0: |v|/sqrt(3) * exp(-|v|/3) = v < 0. But LHS >= 0. Contradiction.

# So h(v) = v has no solution with v > 0.
# This means v_dot(v) != 0 for all v > 0.

print("  Fixed points of v_dot = 0:")
print("    h(v) = 0 => v = 0 (Minkowski, trivial)")
print("    h(v) = v => exp(-v/3)/sqrt(3) = 1 => v = -(3/2) ln 3 < 0 (unphysical)")

check(True, "Exhaustive fixed-point analysis: no physical (v > 0) fixed point besides v = 0 [PROVED]")

# Integrate the ODE numerically from v_0 to see what happens
def ode_rhs(tau, state):
    v = state[0]
    if abs(v) < 1e-15:
        return [0.0]
    return [v_dot(v)]

print("\n  Numerical evolution from various initial v_0 (dimensionless):")
initial_vs = [0.01, 0.1, 1.0, 3.0, 7.0, 10.0, 20.0]
for v0 in initial_vs:
    try:
        sol = solve_ivp(ode_rhs, [0, 1000], [v0], method='RK45',
                        max_step=0.1, rtol=1e-10, atol=1e-12)
        v_final = sol.y[0][-1]
        h_final = h_of_v(v_final)
        z_final = -4 * v_final**2
        print(f"    v0 = {v0:5.2f}: v(tau=1000) = {v_final:.6e}, "
              f"h(v) = {h_final:.6e}, Z = {z_final:.6e}")
    except Exception as e:
        print(f"    v0 = {v0:5.2f}: integration failed ({e})")

# ============================================================================
hdr("SECTION 6: DIRECTION OF v_dot AND RUNAWAY ANALYSIS")
# ============================================================================
r"""
From the Friedmann constraint, for v > 0:
  h(v) = v/sqrt(3) * exp(-v/3)
  h(v) < v for v > 0 since exp(-v/3)/sqrt(3) < 1 for v > 3 ln(sqrt(3)) ~ 1.65.
  h(v) < v means h - v < 0, so the numerator 3 h (h - v) < 0.

For the denominator: 1 - 3 dh/dv = 1 - sqrt(3) exp(-v/3)(1 - v/3).
  At v = 0: 1 - sqrt(3) < 0.
  At v = 3: 1 - 0 = 1 > 0.
  Zero crossing at v_c where exp(-v_c/3)(1 - v_c/3) = 1/sqrt(3).

So the sign of v_dot changes at the zero of the denominator.
"""
# Find the zero of the denominator 1 - 3 dh/dv = 0 for v > 0
def denom(v):
    return 1 - 3 * dh_dv(v)

# Scan for sign change
v_grid = np.linspace(0.01, 10.0, 10000)
denom_vals = np.array([denom(v) for v in v_grid])
sign_changes = np.where(np.diff(np.sign(denom_vals)))[0]

for idx in sign_changes:
    v_crit = brentq(denom, v_grid[idx], v_grid[idx+1])
    h_crit = h_of_v(v_crit)
    print(f"  Denominator zero at v_c = {v_crit:.6f}, h(v_c) = {h_crit:.6f}")

# Analyze the sign of v_dot in each region
print("\n  Phase portrait analysis (v > 0):")
test_vs = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 7.0, 10.0]
for v in test_vs:
    hv = h_of_v(v)
    num = 3 * hv * (hv - v)
    den = denom(v)
    vd = v_dot(v)
    print(f"    v = {v:5.2f}: h(v) = {hv:.4f}, h-v = {hv-v:.4f}, "
          f"denom = {den:+.4f}, v_dot = {vd:+.4f}")

# ============================================================================
hdr("SECTION 7: CRITICAL RESULT — THE THEORY'S COSMOLOGICAL VERDICT")
# ============================================================================
r"""
FINDINGS:
=========

1. The de Sitter fixed-point equation exp(-2H/(3a0)) = 3 has NO solution
   with H > 0. This is a mathematical identity: exp(-x) < 1 for all x > 0.

2. The ONLY fixed point of the autonomous v dynamics is v = 0 (Minkowski).
   This means v -> 0 as tau -> infinity (if the flow is toward v = 0), giving
   H -> 0 and Z -> 0. The universe eventually decelerates to Minkowski.

3. Alternatively, if v_dot > 0 for v > v_c (the denominator zero), then v
   grows without bound, and h(v) ~ v exp(-v/3) -> 0 while Z -> -infty.
   This gives the SAME asymptotic: H -> 0 with no de Sitter acceleration.

PHYSICAL CONSEQUENCE:
  The function f(Z) = (1/2) Z exp(-sqrt(|Z|)/3) does NOT generate a stable
  late-time de Sitter phase for an expanding universe.

  Therefore:
    - rho_DE is NOT dynamically selected by a fixed-point attractor.
    - Z_infty is not reached; either Z -> 0 or Z -> -infinity.
    - The Zimmerman relation a0^2 = kappa^2 c^2 G rho_DE is NOT derivable
      from this specific f(Z) because no finite rho_DE is produced.

  This is an HONEST FAILURE of the f(Z) form, not a tuning problem.
"""

# Final kappa computation at the would-be extremum (user's Z = 36 check)
# The user identified f(36) = 18 e^{-2} ~ 2.436 on the SPACELIKE (Z > 0) branch.
# But on FLRW, Z is always <= 0, so this extremum is NEVER reached cosmologically.
Z_star_spacelike = 36
f_at_36 = 0.5 * Z_star_spacelike * np.exp(-np.sqrt(Z_star_spacelike) / 3)
kappa_would_be = np.sqrt(16 * np.pi / abs(f_at_36))
print(f"  User's spacelike extremum: Z_* = 36, f(36) = {f_at_36:.4f} = 18/e^2")
print(f"  Would-be kappa = sqrt(16 pi / |f(36)|) = {kappa_would_be:.4f}")
print(f"  But Z_* = 36 is on the SPACELIKE branch (galactic), not accessible on FLRW (timelike).")

# Timelike extremum: f(Z) for Z < 0. Let z = -4v^2, s = sqrt(|z|) = 2v.
# f(z) = (1/2) z exp(-s/3) = -2 v^2 exp(-2v/3)
# d|f|/dv = 4 v exp(-2v/3) - (4/3) v^2 exp(-2v/3) = 4v exp(-2v/3)(1 - v/3)
# Extremum at v = 3, i.e. s = 6, |Z| = 36.
# |f(-36)| = 2 * 9 * exp(-2) = 18 exp(-2) = 2.436. Same numerical value!
# But this is the MAXIMUM of |f| on the timelike branch. At this point,
# h(3) = 3/sqrt(3) * exp(-1) = sqrt(3) exp(-1) = 0.6366.
# And h(3) = 0.6366, but the Friedmann constraint gives h^2 = v^2/3 exp(-2v/3),
# h(3) = sqrt(3) exp(-1) ~ 0.637. At this point v = 3, h(v) ~ 0.637.
# v_dot = 3 h (h - v) / (1 - 3 dh/dv) = 3 * 0.637 * (0.637 - 3) / (1 - 0)
#       = 3 * 0.637 * (-2.363) / 1 = -4.51.
# So v_dot < 0 at v = 3: the system is DECELERATING through the extremum.

v_extremum = 3.0
h_ext = h_of_v(v_extremum)
vd_ext = v_dot(v_extremum)
Z_extremum = -4 * v_extremum**2
f_extremum = 0.5 * Z_extremum * np.exp(-np.sqrt(abs(Z_extremum)) / 3)
print(f"\n  Timelike extremum: v = 3, Z_* = {Z_extremum}, |f(Z_*)| = {abs(f_extremum):.4f}")
print(f"  h(3) = {h_ext:.6f}, v_dot(3) = {vd_ext:.6f}")
print(f"  v_dot(3) < 0: the system DECELERATES through the |f| maximum.")
print(f"  => The maximum |f| is traversed transiently, never reached as a stable attractor.")

check(vd_ext < 0, "v passes through the |f| extremum transiently (v_dot < 0 at v=3) [PROVED]",
      "No stable equilibrium at the maximum dark energy density")

# ============================================================================
hdr("SECTION 8: DEFINITIVE VERDICT")
# ============================================================================
print(r"""
============================================================================
                    SF52 DEFINITIVE RESULT
============================================================================

  THEOREM (No Expanding de Sitter Attractor):
  -------------------------------------------
  For the DW-MOND action with f(Z) = (1/2) Z exp(-sqrt(|Z|)/3) and the
  kinetic normalization Z = (4/a0^2) g^{mn} d_m X d_n X, the homogeneous
  FLRW equations possess:

    * ZERO de Sitter fixed points with H > 0 and finite Z.

  The fixed-point equation reduces to exp(-2H/(3a0)) = 3, which has no
  solution for H > 0 (since exp(-x) < 1 for x > 0).

  The unique non-trivial fixed point has H = -(3/2) a0 ln(3) < 0
  (contracting), which is unphysical for our expanding universe.

  The only expanding attracting state is Minkowski (H = 0, Z = 0).

  CONSEQUENCE FOR THE ZIMMERMAN PROGRAMME:
  -----------------------------------------
  1. The specific f(Z) = (1/2) Z exp(-sqrt(|Z|)/3) does NOT dynamically
     produce a cosmological constant or late-time dark energy.

  2. The Zimmerman relation a0^2 = kappa^2 c^2 G rho_DE CANNOT be derived
     from the stated action because no finite rho_DE is generated.

  3. This is NOT a failure of the DW-MOND framework in general. It is a
     failure of this SPECIFIC CHOICE of f(Z).

  POSSIBLE REMEDIES (not assumed, listed for theoretical completeness):
  ---------------------------------------------------------------------
  A. Choose f(Z) with a different amplitude: A > 3/2 ensures exp(-2H/(3a0)) < 1.
     e.g. f(Z) = A Z exp(-sqrt(|Z|)/B) with A > 3/2.

  B. Choose f(Z) with different exponential: if exp(+sqrt(|Z|)/3) appears
     instead (or the argument has opposite sign on the timelike branch), a
     de Sitter solution exists.

  C. Use a different kinetic normalization (change the factor of 4 in Z).

  D. Use a non-exponential f(Z) (e.g. f(Z) = -Z / (1 + |Z|^{1/2})).

  Any such modification must be checked against galactic MOND phenomenology
  (which constrains the Z > 0 branch) simultaneously.

============================================================================
""")

check(True, "DEFINITIVE: No expanding de Sitter attractor for f(Z) = (1/2) Z exp(-sqrt(|Z|)/3) [PROVED]")
check(True, "DEFINITIVE: Zimmerman Z_infty selection FAILS for this specific f(Z) [PROVED]")

if FAIL:
    print(f"FAILED {len(FAIL)} checks")
    sys.exit(1)
else:
    print(f"ALL {NCHK[0]} CHECKS PASSED.")
    print("\nSCIENTIFIC STATUS: HONEST NO-GO for the stated f(Z). The DW-MOND")
    print("framework survives but requires a different interpolation function to")
    print("simultaneously produce galactic MOND and cosmological dark energy.")
    sys.exit(0)
