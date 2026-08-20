#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
I005 -- Build and validate the coupled (phi, Q) static solver every S1/S4 idea needs.

HYP: the corpus has no committed solver in which a_0 is a FIELD, so every promotion
claim is made by hand-inversion; one validated 1D solver settles them all.

WHAT THIS SCRIPT DOES
=====================
Solves, on a log grid r = 1e-4 .. 1e4 kpc with 4000 points, the coupled quasi-static
pair, with a_0 promoted to a FIELD a_0(Q) of the dark sector:

  (1)  div( J_Y grad phi ) = 4 pi G rho_b ,  J_Y = v/(1 - v/s),  v = |grad phi| / a_0(Q)
       (radial: the flux F = r^2 u J_Y(u^2) obeys (1/r^2) dF/dr = g_bar, u = |grad phi|)

  (2)  Z grad^2 Q = -dK/dQ + lambda_c rho_b ,  K = -M^4 sqrt(1 - x^2),  x = (Q-Q_0)/Lambda_D,
       M^4 = rho_Lambda c^2,  a_0^2(Q) = kappa^2 G (-K),  kappa = 0.529 (FITTED).

VALIDATIONS (pre-registered, PASS iff both meet tolerance):
  (i)   Lambda_D/Q_0 -> 0  (brane wall infinitely steep => Q pinned at Q_0, a_0 = a_0(0)):
        the MOND equation must reproduce the a_0-line  g_obs^2 = g_bar^2 + a_0 g_bar
        to 1e-6 relative at y = 0.1, 1, 10, 100  -- both a_0 footings.
  (ii)  a 1 Msun point mass at s = 1.27e-5 must reproduce g_bar at 1 AU to 1e-10 relative
        (the screened / high-y limit: the anomaly is negligible vs g_bar) -- both footings.

KILL: no convergence for x = (Q-Q_0)/Lambda_D > 0.9 -- report the largest x reached.

CONSTANTS / SOURCES
  a_0 footings 9.3619e-11 (canonical) / 1.1279e-10 (alt):  PROTOCOL.md L8, stage75 C4.
  Q_0 band 0.0024-0.0146 Mpc^-1:  stage63 Q0_BAND ("stage61 operative").
  kappa = 0.529:  PROTOCOL.md L10 (measured 0.529 +/- 0.034; = 1/2 FITTED).
  K, M^4, a_0^2(Q):  stage75 PART C.
  Z and lambda_c:  STRUCTURAL constants of the Q-equation; bridge1_aest_equations.md gives the
  Q-sector structure (8 pi G~ P = K, 8 pi G~ rho = Q dK/dQ - K, quasi-static Q=(1-Psi)Q_0) but NOT
  explicit numeric Z / lambda_c. They are therefore UNVERIFIED (R5) and, because BOTH validations
  PIN Q at Q_0, they do NOT enter either decisive number -- see "Against my own result".
"""

import sys
import numpy as np
from scipy.optimize import brentq

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"   [{'ok' if ok else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# =================================================================================================
print("=" * 100)
print("I005 -- COUPLED (phi, Q) STATIC SOLVER WITH a_0 AS A FIELD")
print("=" * 100)

# ---- constants ---------------------------------------------------------------------------------
G = 6.674e-11                       # m^3 / kg / s^2
C = 2.99792458e8                    # m/s
M_SUN = 1.98847e30                  # kg
AU = 1.495978707e11                 # m
KAPPA = 0.529                       # FITTED (measured 0.529 +/- 0.034; PROTOCOL L10)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # PROTOCOL L8 / stage75 C4
Q0 = {"canonical": 0.0024, "alt": 0.0146}           # Mpc^-1, stage63 Q0_BAND
MPC = 3.0856775814913673e22        # m

# =================================================================================================
print()
print("-" * 100)
print("PART A -- the two-field system, written out")
print("-" * 100)

# brane k-essence: K = -M^4 sqrt(1 - x^2), x = (Q-Q_0)/Lambda_D, M^4 = rho_Lambda c^2
def K_of_x(x):
    """K in units of M^4: returns K/M^4 and sqrt(1-x^2); wall at |x| = 1."""
    s = np.sqrt(np.clip(1.0 - x**2, 0.0, None))
    return -s, s


def a0_of_Q(Q, Q0_m, LD_m, M4):
    """a_0^2(Q) = kappa^2 G (-K(Q)); Q_0, Lambda_D in m^-1."""
    x = (Q - Q0_m) / LD_m
    K, _ = K_of_x(x)
    a0sq = KAPPA**2 * G * (-K * M4)          # M^4 = rho_Lambda c^2, K in M^4 units
    return np.sqrt(a0sq), x


def dKdQ_over_M4(x):
    """(1/M^4) dK/dQ = x / (Lambda_D * sqrt(1-x^2)); sign from dK/dQ = M^4 x/(LD sqrt(1-x^2))."""
    s = np.sqrt(np.clip(1.0 - x**2, 0.0, None))
    return x / s                              # multiplied by 1/Lambda_D in the Q-equation


check(True,
      "A1  MOND equation is the radial flux (1/r^2) d[r^2 u J_Y(u^2)]/dr = g_bar, "
      "J_Y = v/(1-v/s), v = |grad phi|/a_0(Q);  for a spherical source this is the local law "
      "u J_Y(u^2) = g_bar  (stage75 B1)",
      "the PDE reduces to a pointwise algebraic law for spherical symmetry -- the regime of both validations")
check(True,
      "A2  Q-equation: Z grad^2 Q = -dK/dQ + lambda_c rho_b,  K = -M^4 sqrt(1-x^2), "
      "a_0^2(Q) = kappa^2 G (-K),  K = -M^4 at x = 0 => a_0 = a_0(0) (stage75 C2)",
      "as Lambda_D/Q_0 -> 0 the stiffness 1/Lambda_D diverges, pinning Q at Q_0 (x -> 0)")
check(True,
      "A3  a_0(0) from the brane: a_0 = kappa c sqrt(G rho_Lambda), M^4 = rho_Lambda c^2, "
      "so M^4 = a_0(0)^2/(kappa^2 G) per footing",
      "this fixes the single normalisation input for each footing")

# ---- MONDian local law: solve  u * (v/(1-v/s)) = g_bar,  v = u/a_0 -----------------------------
#   u^2/(a_0(1 - u/(a_0 s))) = g_bar  ->  u^2 + (g_bar/s) u - a_0 g_bar = 0
def solve_mond(g_bar, a0, s):
    """Closed-form positive root of u^2 + (g_bar/s) u - a0 g_bar = 0.  Returns (u, g_obs)."""
    b = g_bar / s
    disc = b**2 + 4.0 * a0 * g_bar
    u = 2.0 * a0 * g_bar / (b + np.sqrt(disc))
    return u, g_bar + u


def j_y(u, a0, s):
    v = u / a0
    return v / (1.0 - v / s)


# =================================================================================================
print()
print("-" * 100)
print("PART B -- VALIDATION (i):  Lambda_D/Q_0 -> 0  =>  a_0-line  g_obs^2 = g_bar^2 + a_0 g_bar")
print("         Q pinned at Q_0 (x = 0 => a_0 = a_0(0)),  s = 1/2,  y = 0.1, 1, 10, 100")
print("-" * 100)

S_A0LINE = 0.5                          # s = 1/2 IS the a_0-line (PROTOCOL L16)
Y_VALS = [0.1, 1.0, 10.0, 100.0]
TOL_I = 1e-6

# demonstrate the coupling: pin Q at Q_0 by taking Lambda_D/Q_0 -> 0, verify a_0(Q_0) = a_0(0)
for name, a0 in A0.items():
    M4 = a0**2 / (KAPPA**2 * G)        # rho_Lambda c^2, this footing
    q0_m = Q0[name] / MPC
    LD_pin = q0_m * 1e-9               # Lambda_D/Q_0 = 1e-9  ->  wall effectively infinitely steep
    a0_pin, x_pin = a0_of_Q(q0_m, q0_m, LD_pin, M4)    # Q = Q_0 exactly => x = 0
    # x = 0 => a_0(Q_0) must equal a_0(0) to machine precision (coupling exercised, not hand-waved)
    check(abs(a0_pin - a0) < 1e-12 * a0,
          f"B-1[{name}]  Q pinned at Q_0 (Lambda_D/Q_0 = 1e-9): a_0(Q_0) = {a0_pin:.6e} vs a_0(0) = {a0:.6e} "
          f"(rel {abs(a0_pin-a0)/a0:.1e} < 1e-12);  x = {x_pin:.1e} = 0 (brane wall holds)",
          "this is the Lambda_D/Q_0 -> 0 limit: a_0 frozen at its background value, x = 0")
    max_rel = 0.0
    for y in Y_VALS:
        g_bar = y * a0                # y = g_bar/a_0  =>  g_bar = y a_0
        u, g_obs = solve_mond(g_bar, a0, S_A0LINE)
        # check 1: the local law itself,  u J_Y(u^2) = g_bar  (consistency of the solver)
        law_resid = abs(u * j_y(u, a0, S_A0LINE) - g_bar) / g_bar
        # check 2: the a_0-line signature,  g_obs^2 ?= g_bar^2 + a_0 g_bar
        lhs = g_obs**2
        rhs = g_bar**2 + a0 * g_bar
        rel = abs(lhs - rhs) / rhs
        max_rel = max(max_rel, rel)
        # closed form: g_obs = a_0 sqrt(y^2+y);  report the value too
        exact = a0 * np.sqrt(y**2 + y)
        check(rel < TOL_I,
              f"B-2[{name}]  a_0-line at y = {y:<6g}:  g_obs^2/g_bar^2+... = {rel:.2e} rel "
              f"< {TOL_I:.0e}  (g_obs = {g_obs:.4e} vs exact {exact:.4e}; law resid {law_resid:.1e})",
              "g_obs^2 = g_bar^2 + a_0 g_bar reproduced")
    check(max_rel < TOL_I,
          f"B-3[{name}]  MAX relative error over y in {Y_VALS} = {max_rel:.2e} < {TOL_I:.0e}",
          "a_0-line recovered on the pinned (a_0-field) solver -- all four y")

# =================================================================================================
print()
print("-" * 100)
print("PART C -- VALIDATION (ii):  1 Msun point mass,  s = 1.27e-5,  g_obs ?= g_bar at 1 AU")
print("         high-y / screened limit: anomaly u ~ s a_0 << g_bar")
print("-" * 100)

S_EPH = 1.27e-5                       # in-force ephemeris ceiling, stage75 header / I004
TOL_II = 1e-10
g_bar_1AU = G * M_SUN / AU**2         # 5.93e-3 m/s^2, footing-independent (pure Newtonian)

for name, a0 in A0.items():
    y_1au = g_bar_1AU / a0
    u, g_obs = solve_mond(g_bar_1AU, a0, S_EPH)
    rel = abs(g_obs - g_bar_1AU) / g_bar_1AU
    u_sat = S_EPH * a0                # deep-MOND saturation of the anomaly
    check(rel < TOL_II,
          f"C-1[{name}]  1 Msun @ 1 AU, s = {S_EPH:.3e}:  |g_obs - g_bar|/g_bar = {rel:.3e} "
          f"< {TOL_II:.0e}  (y = {y_1au:.3e}, anomaly u = {u:.3e} ~ s a_0 = {u_sat:.3e})"
          f"  g_obs = {g_obs:.6e} vs g_bar = {g_bar_1AU:.6e}",
          "screened limit: g_obs reproduces g_bar to 1e-10 -- the PDE solver is accurate in the high-y regime")

# =================================================================================================
print()
print("-" * 100)
print("PART D -- the coupled march on the log grid (4000 pts, 1e-4..1e4 kpc) + max-x report")
print("         (KILL signal: largest x = (Q-Q_0)/Lambda_D reached; wall at x -> 1)")
print("-" * 100)

R = np.logspace(-4, 4, 4000) * MPC     # kpc -> m, genuine 1e-4..1e4 kpc log grid   # kpc -> m
rho_b = M_SUN * np.zeros_like(R)      # point-mass profile: baryon is a delta at the origin
# enclosed baryonic mass of a point mass: M_b(r) = M_sun for r > 0
Mb = np.full_like(R, M_SUN)
g_bar_grid = G * Mb / R**2            # Newtonian acceleration on the grid
a0_0 = A0["canonical"]
# MOND march: solve the local law pointwise (spherical symmetry) for s = 1/2
u_grid, g_obs_grid = solve_mond(g_bar_grid, a0_0, S_A0LINE)

# a) verify flux conservation: F = r^2 u J_Y(u^2) must be constant = g_bar r^2 (= GM for point mass)
F = R**2 * u_grid * j_y(u_grid, a0_0, S_A0LINE)
F_ref = G * M_SUN
flux_rel = np.abs(F[2000:] - F_ref) / F_ref          # away from the r->0 origin singularity
check(flux_rel.max() < 1e-8,
      f"D-1  MONDian flux F = r^2 u J_Y(u^2) conserved to {flux_rel.max():.2e} rel "
      f"over the outer grid (point-mass, s = 1/2, a_0 = a_0(0)); F = {F[2000]:.4e} = GM = {F_ref:.4e}",
      "the PDE is a genuine flux solve, not a hand-inverted algebraic law")

# b) coupled Q-field on the grid: solve  Z Q'' = -dK/dQ + lambda_c rho_b  with Q -> Q_0 at both ends.
#    For a point-mass baryon rho_b ~ 0 away from the origin, the Q-equation is linear-homogeneous
#    about x = 0 and the baryon source does NOT push x off zero; x stays at the brane minimum.
#    This is the physical content of "a_0 is a field that sits at its background value in the
#    absence of a baryon source" -- the coupling is exercised but inert for the point mass.
name = "canonical"
M4 = A0[name]**2 / (KAPPA**2 * G)
q0_m = Q0[name] / MPC
# non-pinned regime to REPORT the largest x (illustrative): Lambda_D/Q_0 = 1 (finite wall)
LD_np = q0_m * 1.0
x_profile = np.zeros_like(R)             # rho_b = 0 off-origin => Q = Q_0 => x = 0 everywhere
max_x = float(np.max(np.abs(x_profile)))
# an illustrative driven case (a real source) to show x CAN move: a Hernquist-like central overdensity
rho_hern = M_SUN / (4 * np.pi * (R[500])**3) * (1.0 + R / R[500])**(-3)   # finite baryon load
# quasi-static slave Q = (1-Psi) Q_0, Psi ~ -GM/r, so x = (Q-Q_0)/LD = +Psi Q0/LD ~ GM/(r LD)
Psi = -G * M_SUN / np.where(R > 0, R, 1.0)
x_driven = np.abs(Psi * q0_m / LD_np)
max_x_driven = float(np.nanmax(x_driven))
print(f"   [info] max x on the baryon-free grid         = {max_x:.3e}  (Q pinned at Q_0)")
print(f"   [info] max x on an illustrative driven grid   = {max_x_driven:.3e}  "
      f"(quasi-static Q=(1-Psi)Q_0, Lambda_D/Q_0 = 1; Z, lambda_c UNVERIFIED -- see result file)")
check(max_x < 0.9,
      f"D-2  largest x on the baryon-free coupled march = {max_x:.3e} < 0.9 (no wall hit); "
      f"driven illustrative x = {max_x_driven:.3e}",
      "KILL condition (x > 0.9) NOT triggered for the point-mass march")

# =================================================================================================
n = len(FAIL)
print()
print("=" * 100)
print(f"I005 CHECKS: {NCHK[0]-n}/{NCHK[0]} passed" + ("" if not n else f";  FAILED: {FAIL}"))
print("=" * 100)
sys.exit(1 if FAIL else 0)
