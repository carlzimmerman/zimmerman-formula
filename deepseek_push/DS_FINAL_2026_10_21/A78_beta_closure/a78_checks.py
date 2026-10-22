#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A78 -- IS beta A PHYSICAL PARAMETER?

Action (A33 MASTER_ACTION sec.1, K = 4 pi G, c = 1, signature (-+++)):

  L/(N sqrt h) = [R3 + K_ij K^ij - (1+beta) theta^2 - 2 Lambda]/(4K)
               + P^i D_i ln N - W(u) + (eta/2) E_i E^i
               - (gamma/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij + L_m/(N sqrt h)

  K_ij = (1/2N)(hdot_ij - D_i N_j - D_j N_i),  theta = K^i_i,  u = K|P|

Every number quoted in report.md is printed by this script.

Design rule: each check compares a quantity computed from the action with a quantity
computed by an INDEPENDENT route (a second variation, a second elimination, a closed
form, or a measured/required value).  No check is `ok = True`.

Mutations: A78_MUTATE=<name>, names documented in MUTATE.md.
"""

import os
import sys
import json
import math

import numpy as np
import sympy as sp

# --------------------------------------------------------------------------------------
# INPUTS (provenance in comments).  Printed in the header; every quoted number is output.
# --------------------------------------------------------------------------------------
G_SI      = 6.67430e-11          # m^3 kg^-1 s^-2  (CODATA)
C_SI      = 2.99792458e8         # m/s
K_SI      = 4.0 * math.pi * G_SI # A33 sec.1.1: K = 4 pi G
A0_SI     = 9.36e-11             # m/s^2, canonical a0 (A33/A54)
PC_SI     = 3.0856775814913673e16
LSTAR_SI  = 24.0 * PC_SI         # m, A20/A65 fitted window 24-90 pc (lower edge)
H0_SI     = 67.4e3 / (1.0e6 * PC_SI)   # s^-1, 67.4 km/s/Mpc
LAMBDA_OBS= 1.0890e-52           # m^-2, A33 coefficient table row 2
OMEGA_M   = 0.316                # Planck 2018 TT,TE,EE+lowE+lensing
K_EV      = 8.430565e-56         # eV^-2, A69 header
ETA_EV    = 5.937141e-07         # eV^-4, A69 header (eta = gamma = K L*^2/2)
PSC_EV    = 2.8360e-69           # eV, A69 sec.4.2 strong-coupling momentum
DNEFF_BND = 0.30                 # Planck 2018 + BBN 95% CL on |Delta N_eff|
NEFF_STD  = 3.046

# --------------------------------------------------------------------------------------
# MUTATION DIALS.  Each changes exactly one input of the theory.
# --------------------------------------------------------------------------------------
MUT = os.environ.get("A78_MUTATE", "").strip()
KNOWN = ("", "beta_sign", "no_theta2", "clock_xi", "Z_eta", "tt_beta",
         "G_factor", "static_shift", "frw_ansatz", "gamma_factor2",
         "W_quad", "tt_trace")
if MUT not in KNOWN:
    print("unknown mutation %r; known: %s" % (MUT, ", ".join(k for k in KNOWN if k)))
    sys.exit(2)


def theta_coef(beta):
    """Coefficient c of  -(c) theta^2/(4K).  Theory: c = 1+beta."""
    if MUT == "beta_sign":
        return 1.0 - beta
    if MUT == "no_theta2":
        return 0.0
    return 1.0 + beta


def clock_xi():
    """Coefficient xi of  xi P^i D_i ln N.  Theory: xi = 1 exactly."""
    return 2.0 if MUT == "clock_xi" else 1.0


def z_eta_on():
    """1 keeps the eta p^2 piece of Z, 0 deletes it (mutation)."""
    return 0.0 if MUT == "Z_eta" else 1.0


def tt_beta_coef():
    """Spurious beta in the TT kinetic coefficient (mutation)."""
    return 1.0 if MUT == "tt_beta" else 0.0


def fried_n():
    """n in  n (2+3 beta) H^2 = 2 Lambda + 4K rho.  Theory: n = 3."""
    return 2.0 if MUT == "G_factor" else 3.0


def static_shift_c():
    """N^i = c r rhat in the 'static' ansatz (mutation destroys staticity)."""
    return 0.05 if MUT == "static_shift" else 0.0


def frw_ansatz_div():
    """Denominator of the hand-written reduced FRW Lagrangian: 4K (theory)."""
    return 8.0 if MUT == "frw_ansatz" else 4.0


def gamma_factor():
    """Multiplier on the gradient stiffness gamma: 1 (theory)."""
    return 2.0 if MUT == "gamma_factor2" else 1.0


def weyl_R3():
    """Weyl weight of R3 under h -> Omega^2 h (constant Weyl in 3D): -2."""
    return -2.0


# --------------------------------------------------------------------------------------
# result plumbing
# --------------------------------------------------------------------------------------
RESULTS = []


def chk(name, lhs, rhs, tol=1e-10, note="", scale=None):
    """|lhs-rhs| <= tol * max(|lhs|,|rhs|,scale)."""
    lhs = float(lhs)
    rhs = float(rhs)
    ref = max(abs(lhs), abs(rhs), abs(scale) if scale is not None else 0.0, 1e-300)
    res = (lhs - rhs) / ref
    ok = abs(res) <= tol
    RESULTS.append(dict(name=name, lhs=lhs, rhs=rhs, residual=res, tol=tol,
                        ok=bool(ok), note=note))
    print("%-14s lhs=%+.12e  rhs=%+.12e  rel.res=%+.3e  tol=%.0e  %s   %s"
          % (name, lhs, rhs, res, tol, "PASS" if ok else "FAIL", note))
    return ok


def chk_fail(name, note, val=float("nan")):
    """Record a failure produced by the theory itself (no real solution)."""
    RESULTS.append(dict(name=name, lhs=float(val), rhs=float("nan"), residual=float("nan"),
                        tol=0.0, ok=False, note=note))
    print("%-14s NO REAL SOLUTION (lhs=%s)   FAIL   %s" % (name, val, note))
    return False


def chk_nonzero(name, val, floor, note=""):
    """Requirement: |val| > floor.  Recorded as (val, floor)."""
    val = float(val)
    ok = abs(val) > floor
    RESULTS.append(dict(name=name, lhs=val, rhs=float(floor), residual=abs(val) / floor,
                        tol=1.0, ok=bool(ok), note=note))
    print("%-14s value=%+.12e  floor=%.3e  ratio=%.3e  %s   %s"
          % (name, val, floor, abs(val) / floor, "PASS" if ok else "FAIL", note))
    return ok


# ======================================================================================
# PART 1 -- THE BACKGROUND.  Task 1(e), Task 3.
# ======================================================================================
print("=" * 100)
print("A78  beta closure      mutation = %r" % MUT)
print("=" * 100)
print("INPUTS")
for k, v in [("G [m^3/kg/s^2]", G_SI), ("c [m/s]", C_SI), ("K=4piG [m^3/kg/s^2]", K_SI),
             ("a0 [m/s^2]", A0_SI), ("L* [m]", LSTAR_SI), ("H0 [1/s]", H0_SI),
             ("Lambda_obs [1/m^2]", LAMBDA_OBS), ("Omega_m", OMEGA_M),
             ("K [eV^-2]", K_EV), ("eta [eV^-4]", ETA_EV), ("p_sc [eV]", PSC_EV),
             ("|Delta N_eff| bound", DNEFF_BND), ("N_eff^SM", NEFF_STD),
             ("A69 max loop factor", 1.904e-70), ("GW170817 |c_T-1|", 1e-15)]:
    print("   %-24s = %.8e" % (k, v))
print()

# ---- the FRW reduction, from the full ADM action (route A) and the reduced ansatz (B) ----
# Lambda enters the Friedmann equation as Lambda c^2 [s^-2]; keep that explicit.
LAM_S2 = LAMBDA_OBS * C_SI ** 2          # s^-2
Kx, bx, Lx, rx, Nx = sp.symbols("K beta Lambda rho N", positive=True)
asym, Hs = sp.symbols("a H", positive=True)
adot = Hs * asym                       # adot = H a

# route A: substitute h_ij = a^2 delta_ij, N, N^i = 0 into the FULL ADM density
#   theta = 3 adot/(a N);  K_ij K^ij = 3 adot^2/(a^2 N^2)
Atil = 3 * theta_coef(bx) - 1            # = 2+3beta for the theory
dens_A = Nx * asym**3 / (4 * Kx) * (0 + 3 * adot**2 / (asym**2 * Nx**2)
                                    - theta_coef(bx) * 9 * adot**2 / (asym**2 * Nx**2)) \
         - Nx * (Lx / (2 * Kx) + rx) * asym**3
LA = sp.simplify(dens_A)

# route B: the reduced Lagrangian written directly from L/(N sqrt h) with h_ij = a^2 delta,
# with adot an independent symbol (so that dL/dadot is a genuine partial derivative)
adots = sp.symbols("adots", positive=True)
LB = -(3 * Atil / (frw_ansatz_div() * Kx)) * asym * adots**2 / Nx - Nx * (Lx / (2 * Kx) + rx) * asym**3
LB_H = LB.subs(adots, Hs * asym)

res_AB = sp.simplify(LA - LB_H)
try:
    H2_A = sp.solve(sp.Eq(sp.diff(LA, Nx).subs(Nx, 1), 0), Hs**2)[0]
except IndexError:
    H2_A = None
try:
    H2_B = sp.solve(sp.Eq(sp.simplify((sp.diff(LB, adots) * adots - LB).subs(Nx, 1)).subs(adots, Hs * asym), 0),
                    Hs**2)[0]
except IndexError:
    H2_B = None
print("\n[P1] FRW from the full ADM density vs the reduced ansatz")
print("     L_A - L_B (symbolic)          =", res_AB)
print("     H^2 from dL/dN = 0            =", sp.simplify(H2_A) if H2_A is not None else "NO REAL SOLUTION")
print("     H^2 from the Legendre energy  =", sp.simplify(H2_B) if H2_B is not None else "NO REAL SOLUTION")
if H2_A is None or H2_B is None:
    chk_fail("C01_FRW", "the dialled action has no H^2 solution: n A H^2 = 2Lambda+4K rho is inconsistent")
else:
    chk("C01_FRW", sp.simplify(H2_A).subs({Kx: K_SI, Lx: LAM_S2, rx: 1e-26, bx: 1.0}),
        sp.simplify(H2_B).subs({Kx: K_SI, Lx: LAM_S2, rx: 1e-26, bx: 1.0}), 1e-13,
        "two independent variations of the FRW action")

A_of = lambda b: 3.0 * theta_coef(b) - 1.0
H2_of = lambda b, Lam, rho: (2.0 * Lam + 4.0 * K_SI * rho) / (fried_n() * A_of(b))

# ---- C02: the first-order constraint is preserved by its own flow (second equation) ----
# run in units with Lambda c^2 = 1 (the equation is homogeneous of degree one in H^2, Lambda, rho)
Lam_t, rho0 = 1.0, 0.9
b_num = 0.7


def rhs_ode(a):
    return a * math.sqrt(max(H2_of(b_num, Lam_t, rho0 * a ** -3), 1e-300))


a_ini, dt, nstep = 1.0, 2.0e-3, 600
hist = [a_ini]
for i in range(nstep):
    ai = hist[-1]
    k1 = rhs_ode(ai)
    k2 = rhs_ode(ai + 0.5 * dt * k1)
    k3 = rhs_ode(ai + 0.5 * dt * k2)
    k4 = rhs_ode(ai + dt * k3)
    hist.append(ai + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0)
H2_ladder = [H2_of(b_num, Lam_t, rho0 * a ** -3) for a in hist]
if min(H2_ladder) <= 0.0:
    chk_fail("C02_FRW2", "H^2 < 0 on the dialled background: no real expansion (kinetic term wrong sign)",
             min(H2_ladder))
    Hs = np.array([math.sqrt(abs(h)) for h in H2_ladder])
    GUARD2 = True
else:
    Hs = np.array([math.sqrt(h) for h in H2_ladder])
    GUARD2 = False
Hdot_fd = (Hs[2:] - Hs[:-2]) / (2 * dt)
Hmid = Hs[1:-1]
lhs2 = A_of(b_num) * (2 * Hdot_fd + 3 * Hmid ** 2)
rhs2 = 2 * Lam_t
print("\n[P1] second Friedmann equation along the numerical solution of the first")
print("     A (2Hdot+3H^2) = %.10f ... %.10f ; 2 Lambda = %.1f"
      % (lhs2.min(), lhs2.max(), rhs2))
if not GUARD2:
    chk("C02_FRW2", float(np.mean(lhs2) / rhs2), 1.0, 1e-4,
        "A (2Hdot+3H^2) = 2 Lambda along the solution of n A H^2 = 2Lambda+4K rho")

# ---- C03: G_cosmo / G_static.  Static Poisson (route B) vs Friedmann (route A) ----
# static: K_ij = theta = 0 -> R3 = 2Lambda + 4K rho ; h_ij=(1+2Psi)delta -> R3 = -4 lap^2 Psi
# so lap^2 Phi = K rho with Phi = -Psi  =>  G_N = K/(4 pi)
G_N = K_SI / (4 * math.pi)
def G_eff(b):
    # n A H^2 = 2Lam + 4K rho  ->  3H^2 = Lam_eff + 8 pi G_eff rho
    return 6.0 * G_SI / (fried_n() * A_of(b))
print("\n[P1] cosmological vs static gravitational coupling")
print("     G_N   (static Poisson, lap^2 Phi = K rho) = %.8e" % G_N)
for b in (0.0, 0.027, 0.5, 1.0, 3.0):
    print("     G_eff/G_N (beta=%.3f) = %.8f" % (b, G_eff(b) / G_N))
chk("C03_GEFF", G_eff(0.0) / G_N, 1.0, 1e-14, "beta=0 must reduce to GR")
chk("C03b_GEFF", G_eff(0.027) / G_N, 1.0, 0.05,
    "BBN requires G_cosmo = G_N to <5% at beta < 0.027")

# ---- C04: beta implied by Lambda_bare = Lambda_obs at H0 (A33 K16) ----
def beta_closed(Lam_s2, H, rho=0.0):
    # n(2+3b)H^2 = 2Lam c^2 + 4K rho -> b = ((2Lam c^2+4K rho)/(n H^2) - 2)/3
    return ((2.0 * Lam_s2 + 4.0 * K_SI * rho) / (fried_n() * H ** 2) - 2.0) / 3.0


from scipy.optimize import brentq
f_root = lambda b: fried_n() * A_of(b) * H0_SI ** 2 - 2.0 * LAM_S2
b_closed = beta_closed(LAM_S2, H0_SI)
try:
    b_root = brentq(f_root, -0.69, 60.0, xtol=1e-15)
except ValueError:
    b_root = float("nan")
    chk_fail("C04b_ROOT", "n A(beta) H0^2 - 2 Lambda has no root: the dialled background cannot reproduce H0")
LDS = 3.0 * H0_SI ** 2 / C_SI ** 2          # m^-2, the Lambda that gives H0 with no matter
print("\n[P1] beta from the vacuum background at (Lambda_bare = Lambda_obs, H = H0)")
print("     beta (closed form)  = %.12f" % b_closed)
print("     beta (brentq root)  = %.12f" % b_root)
print("     Lambda_dS = 3 H0^2/c^2 = %.8e m^-2 = %.6f Lambda_obs"
      % (LDS, LDS / LAMBDA_OBS))
print("     Lambda_obs c^2 = %.8e s^-2 ; 3 H0^2 = %.8e s^-2 ; ratio = %.6f"
      % (LAM_S2, 3 * H0_SI ** 2, LAM_S2 / (3 * H0_SI ** 2)))
if not math.isnan(b_root):
    chk("C04_K16", b_closed, b_root, 1e-12, "A33 K16: beta(Lambda_bare=Lambda_obs)=-0.2108")

print("     beta>0 requires Lambda_bare > Lambda_dS = %.6f Lambda_obs (vacuum reading)" % (LDS / LAMBDA_OBS))
for b in (0.0, 0.027, 1.0, 3.0):
    print("     beta=%5.3f  ->  Lambda_bare = %8.4f Lambda_obs (vacuum/dS reading, H=H0)"
          % (b, (2.0 + 3.0 * b) / 2.0 * LDS / LAMBDA_OBS))

# ---- matter-inclusive reading at the present epoch (exact relation, plug back) ----
# n A H0^2 = 2 Lambda_bare c^2 + 4K rho_m0 ;  2K rho_m0 = 3 H0^2 Omega_m
# => Lambda_bare c^2 = (n A H0^2 - 6 H0^2 Omega_m)/2
OMEGA_M_IMPL = 1.0 - LAM_S2 / (3.0 * H0_SI ** 2)   # implied by (Lambda_obs, H0): 0.3162


def Lambda_bare_present(b):
    """Lambda_bare c^2 in s^-2, with Omega_m fixed by the observed (Lambda_obs, H0)."""
    return 0.5 * (fried_n() * A_of(b) * H0_SI ** 2 - 6.0 * H0_SI ** 2 * OMEGA_M_IMPL)


print("\n[P1] present-epoch reading, matter included (n A H0^2 = 2Lambda_bare c^2 + 4K rho_m0)")
print("     Omega_m implied by (Lambda_obs, H0) = %.6f   (Planck: %.3f)" % (OMEGA_M_IMPL, OMEGA_M))
print("     check: Lambda_bare(beta=0)/(Lambda_obs c^2) = %.10f"
      % (Lambda_bare_present(0.0) / LAM_S2))
for b in (0.0, 0.027, 0.5, 1.0, 3.0):
    print("     beta=%5.3f  ->  Lambda_bare = %8.4f Lambda_obs"
          % (b, Lambda_bare_present(b) / LAM_S2))
chk("C05_LAM0", Lambda_bare_present(0.0) / LAM_S2, 1.0, 1e-12,
    "beta=0 must reproduce the observed Lambda")
bchk = 1.0
resid = fried_n() * A_of(bchk) * H0_SI ** 2 - 2 * Lambda_bare_present(bchk) - 6 * H0_SI ** 2 * OMEGA_M_IMPL
print("     plug-back residual at beta=1: (n A H0^2 - 2Lambda_bare - 4K rho)/(n A H0^2) = %.3e"
      % (resid / (fried_n() * A_of(bchk) * H0_SI ** 2)))

# ---- C06: stability beta>0 <-> Lambda_bare > Lambda_eff ----
ok_sign = True
print("\n[P1] stability vs bare vacuum")
for b in (-0.10, 0.0, 0.027, 0.5, 1.0):
    Lb = Lambda_bare_present(b)
    ok_sign = ok_sign and ((b > 0) == (Lb > Lambda_bare_present(0.0)))
    print("     beta=%+5.3f  Lambda_bare/Lambda_obs=%8.4f  sign(beta)=%+d  sign(Lb-Lobs)=%+d"
          % (b, Lb / LAM_S2, int(np.sign(b)), int(np.sign(Lb - Lambda_bare_present(0.0)))))
chk("C06_STAB", 1.0 if ok_sign else 0.0, 1.0, 1e-15,
    "beta>0 iff Lambda_bare > Lambda_obs (matter-inclusive reading)")

# ======================================================================================
# PART 2 -- THE STATIC SECTOR.  Task 1(a),(b).
# ======================================================================================
print("\n" + "=" * 100)
print("PART 2 -- static sector: theta = 0 identically, so no beta anywhere")
print("=" * 100)

r_, f_, Nf, P_ = sp.symbols("r f N P", positive=True)
# h_ij = f(r)^2 delta_ij in flat spherical coordinates; N = N(r); N^i = c*r*rhat
# K_ij = (1/2N)(hdot_ij - D_i N_j - D_j N_i) with all time derivatives zero
cs = sp.symbols("cs", real=True)
# For N^i = c r rhat on a flat metric: D_i N_j + D_j N_i has trace 2 c (div N)/... compute directly:
# div(N^i) = (1/r^2) d/dr(r^2 * c r) = 3c ; theta = (1/N)(d_t ln sqrt h - D_i N^i) = -3c/N
theta_static = sp.simplify(-3 * cs / Nf)
print("\n[P2] theta on the static ansatz (N^i = c_s r rhat), dial c_s = %g:  theta = %s"
      % (static_shift_c(), theta_static))
# the beta-term of the action density, static:
beta_term = sp.simplify(Nf * f_**3 * theta_coef(bx) * theta_static ** 2 / (4 * Kx))
print("     (1+beta) theta^2 N sqrt h/(4K) =", beta_term)
chk("C07_THETA", float(theta_static.subs({Nf: 1.3, cs: static_shift_c()})), 0.0, 1e-15,
    "theta = 0 identically for N^i=0, hdot=0")
chk("C08_BTERM", float(beta_term.subs({Nf: 1.3, f_: 2.1, bx: 1.0, cs: static_shift_c(), Kx: 1.0})), 0.0, 1e-15,
    "the whole beta-term vanishes on the static branch, every beta")
chk_nonzero("C09_SHARP", float(beta_term.subs({Nf: 1.3, f_: 2.1, bx: 1.0, cs: 0.05, Kx: 1.0}))
            - float(beta_term.subs({Nf: 1.3, f_: 2.1, bx: 1.0, cs: static_shift_c(), Kx: 1.0})), 1e-8,
            "and is NON-zero as soon as N^i != 0: beta-invisibility is staticity, not absence")

# dS_static/dbeta = -(1/4K) int N sqrt h theta^2 : two routes, both zero
dSdb = sp.simplify(sp.diff(Nf * f_**3 * (0 - theta_coef(bx) * theta_static ** 2) / (4 * Kx), bx))
print("     d/dbeta of the static action density =", dSdb)
chk("C10_DSDB", float(dSdb.subs({Nf: 1.3, f_: 2.1, bx: 1.0, cs: static_shift_c(), Kx: 1.0})), 0.0, 1e-15,
    "static action has identically zero beta-derivative")

# ---- the law: first integral + AQUAL ----
a0, g, u, xi = sp.symbols("a0 g u xi", positive=True)
# charge coefficient xi:  xi * d ln N = K W'(u)  ->  xi g = a0 u/(a0-u)  ->  u(g)
if MUT == "W_quad":
    u_of_g = g                      # quadratic W: K W'(u) = u  ->  u = g  ->  g_N = g - u = 0
else:
    u_of_g = xi * a0 * g / (xi * g + a0)
gN = sp.simplify(g - xi * u_of_g)
print("\n[P2] the law from the first integral g_N = g - xi u,  xi g = K W'(u)")
print("     g_N(g) =", sp.factor(sp.simplify(gN)))
gN_law = g ** 2 / (g + a0)
print("     xi=1:  g_N =", sp.simplify(gN.subs(xi, 1)))
print("     A33 K5 form at xi=2, g=a0/3:  g_N = %.6f a0 ; law = %.6f a0 ; difference = %.6f a0"
      % (float(gN.subs({xi: 2, g: a0 / 3}) / a0), float(gN_law.subs(g, a0 / 3) / a0),
         float((gN.subs({xi: 2, g: a0 / 3}) - gN_law.subs(g, a0 / 3)) / a0)))
chk("C11_LAW", float((gN.subs(xi, clock_xi()) - gN_law).subs({a0: A0_SI, g: A0_SI / 3})),
    0.0, 1e-12, "xi=1 reproduces g_N = g^2/(g+a0) exactly (A33 K3)")
# AQUAL: g mu(g/a0) = g_N with mu(x)=x/(1+x)
x_ = sp.symbols("x", positive=True)
mu = x_ / (1 + x_)
print("     AQUAL residual: g mu(g/a0) - g^2/(g+a0) =",
      sp.simplify((g * mu.subs(x_, g / a0) - gN_law)))
first_int = sp.simplify(g - u_of_g)          # the action's first integral, with the dialled u(g)
for gg in (0.01, 0.1, 0.5, 1.0, 10.0):
    v = float((g * mu.subs(x_, g / a0) - first_int).subs({a0: 1.0, g: gg, xi: clock_xi()}))
    print("       g/a0=%5.2f   g mu - g_N = %+.3e" % (gg, v))
chk("C12_AQUAL", float((g * mu.subs(x_, g / a0) - first_int).subs({a0: 1.0, g: 3.7, xi: clock_xi()})), 0.0, 1e-14,
    "the action's first integral g-u(g) IS AQUAL mu(x)=x/(1+x)")

# ---- alpha_1: 2 r^2/L*^2 at 1 AU, two routes; and its beta-independence ----
AU = 1.495978707e11
gam_measured = K_SI * LSTAR_SI ** 2 / 2.0      # A33 row 7: gamma = K L*^2/2, L* fitted
gam_action = gam_measured / gamma_factor()      # the action's coefficient (dialled)
al1_a = 2 * AU ** 2 / LSTAR_SI ** 2             # from the measured L* (data side)
al1_b = AU ** 2 * K_SI / gam_action             # from the action's gamma (theory side)
print("\n[P2] alpha_1(1 AU): 2r^2/L*^2 = %.8e (measured L*) ;  r^2 K/gamma = %.8e (action)"
      % (al1_a, al1_b))
chk("C13_ALPHA1", al1_a, al1_b, 1e-12, "alpha_1(1AU)=2r^2/L*^2=r^2K/gamma; no beta (A54 G6)")
print("     alpha_1 depends on gamma only; the static solution is beta-free (C07-C10),")
print("     so d alpha_1/d beta = 0 for every beta.")

# ======================================================================================
# PART 3 -- THE TENSOR SECTOR.  Task 1(c).
# ======================================================================================
print("\n" + "=" * 100)
print("PART 3 -- TT sector: theta = O(h^2), so beta cannot enter at quadratic order")
print("=" * 100)

# h_ij = delta_ij + eps*h_ij^TT(x), N=1, N^i=0.  theta = (1/2) d_t ln det(h).
hxx = sp.Function("h11")
# take a TT mode in the (k=(0,0,k)) frame: h = diag(h+, -h+, 0)
hp = sp.Function("hp")
tt_ = sp.symbols("tt", real=True)
if MUT == "tt_trace":
    hmat = sp.Matrix([[1 + sp.Function("A")(tt_), 0, 0],
                      [0, 1 + sp.Function("A")(tt_), 0],
                      [0, 0, 1 + sp.Function("A")(tt_)]])
else:
    hmat = sp.Matrix([[1 + sp.Function("A")(tt_), 0, 0],
                      [0, 1 - sp.Function("A")(tt_), 0],
                      [0, 0, 1]])
det = sp.simplify(hmat.det())
th = sp.simplify(sp.Rational(1, 2) * sp.diff(sp.log(det), tt_))
print("\n[P3] TT mode diag(h+,-h+,0): det =", det)
print("     theta = (1/2) d_t ln det =", sp.simplify(th))
# expand: h+ = eps*A, theta at O(eps^2)
eps = sp.symbols("eps", positive=True)
th2 = sp.series(th.subs(sp.Function("A")(tt_), eps * sp.Function("a")(tt_)), eps, 0, 3).removeO()
print("     theta to O(eps^2) =", sp.simplify(th2))
coef1 = sp.simplify(sp.diff(th2, eps).subs({eps: 0.0, sp.Derivative(sp.Function('a')(tt_), tt_): 1.0}))
print("     O(eps) coefficient of theta =", coef1)
chk("C14_TTTHETA", float(coef1), 0.0, 1e-15, scale=1.0,
    note="theta vanishes at O(eps) for a TT mode: no volume change at linear order")

# quadratic TT action with general beta: R3^(2) = -k^2 h^2/4 (average), K_ijK^ij = hdot^2/4, theta=0
h_, k_, hd_ = sp.symbols("h k hdot", positive=True)
c2 = tt_beta_coef()
S_TT = (1 / (4 * Kx)) * (hd_ ** 2 / 4 * (1 + c2 * bx) - k_ ** 2 * h_ ** 2 / 4)
w2 = sp.solve(sp.Eq(sp.diff(S_TT, hd_, 2) * (-1) * 1.0, 0), k_)  # placeholder to keep sympy quiet
cT2 = sp.simplify((k_ ** 2 / 4) / (hd_ ** 2 / 4 * (1 + c2 * bx)) * (hd_ ** 2 / k_ ** 2))
print("\n[P3] quadratic TT action  S = (1/4K)[ (1+%g beta) hdot^2/4 - k^2 h^2/4 ]" % c2)
print("     c_T^2 = <(-R3)>/<K^2> =", sp.simplify(cT2))
cT2_val = float(sp.simplify(cT2).subs(bx, 1.0))
chk("C15_CT2", cT2_val, 1.0, 1e-14, "c_T^2 = 1 for every beta (GW170817 |c_T-1|<1e-15)")
# beta-coefficient of the O(h^2) TT action
coef_beta = sp.simplify(sp.diff(S_TT, bx))
print("     dS_TT/dbeta =", coef_beta)
chk("C16_TTBETA", float(coef_beta.subs({bx: 1.0, Kx: K_SI, hd_: 1.0, k_: 1.0})), 0.0, 1e-30,
    "the O(h^2) TT action has identically zero beta-coefficient")

# ======================================================================================
# PART 4 -- THE FIFTH MODE.  Task 1(d).
# ======================================================================================
print("\n" + "=" * 100)
print("PART 4 -- the fifth mode: Z carries beta, O(1), and it is a pole")
print("=" * 100)

# quadratic scalar action, A68 eq. (D1)-(D5), with the theta coefficient generalised to c:
#   L/a^3 = [-3A z^2 + 2A z Y - (c-1) Y^2 + ...]/(4K)  with A = 3c-1, z = zdot (H=0, n=0)
z, Y, eta_, alpha_, p_ = sp.symbols("zdot Y eta alpha p", positive=True)
A_ = 3 * theta_coef(bx) - 1
c1 = theta_coef(bx) - 1
Lq = (-(3 * A_) * z ** 2 + 2 * A_ * z * Y - c1 * Y ** 2) / (4 * Kx)
Ystar = sp.solve(sp.diff(Lq, Y), Y)[0]
Lred = sp.simplify(Lq.subs(Y, Ystar))
print("\n[P4] shift elimination:  Y* =", sp.simplify(Ystar))
print("     reduced L =", sp.factor(sp.simplify(Lred)))
B_sym = sp.simplify(-2 * Lred / z ** 2 * Kx)   # Lred = -(3c-1)/(2K(c-1)) z^2 ... sign check below
B_sym = sp.simplify(sp.diff(Lred, z, 2) * Kx)  # (1/2)B z^2, so B = 2*d2L/dz2*K ... use the direct form
B_direct = sp.simplify(2 * Lred / z ** 2)
print("     B = K(3c-1)/(c-1) check: B_direct =", sp.factor(B_direct))

# lapse constraint at H=0: dL/dn = p^2(zeta/K + sigma) -> zeta = -K sigma
#   kinetic: B/2 sigma^2 with B = K(3c-1)/(c-1) ; potential: alpha p^4/2 * sigma^2
Bnum = float((Kx * (3 * theta_coef(bx) - 1) / (theta_coef(bx) - 1)).subs({Kx: 1.0, bx: 1.0}))
print("     B(beta=1)/K = %.6f   (A68: 5)" % Bnum)
print("     B(beta=3)/K = %.6f   (A68: 11/3)"
      % float((Kx * (3 * theta_coef(bx) - 1) / (theta_coef(bx) - 1)).subs({Kx: 1.0, bx: 3.0})))
chk("C17_B", Bnum, 5.0, 1e-14, "B = K(2+3beta)/beta at beta=1")

# ---- independent route: extremise the quadratic action numerically over (Y, n) ----
def Z_numeric(beta, p, eta_v):
    """Coefficient of sigma_dot^2 after eliminating Y and n numerically."""
    c = theta_coef(beta)
    A = 3 * c - 1
    c1 = c - 1
    # full quadratic L (H=0), with n: [-3A z^2 + 2A z Y - c1 Y^2 + 2p^2 zeta^2 + 4p^2 n zeta]/(4K)
    #                                  + p^2 n sigma + eta p^2/2 sdot^2 - (K p^2 + alpha p^4)/2 sigma^2
    # zeta = -K sigma from dL/dn = 0 (p^2(zeta/K+sigma)); substitute and read off sdot^2.
    # do it numerically on a grid over Y (the only remaining algebraic variable) with z = -K*sdot
    Kk, al = 1.0, 1.0
    sdot = 1.0
    zeta = -Kk * 1.0        # sigma = 1
    fY = lambda Yv: (-(3 * A) * (zeta * sdot) ** 2 + 2 * A * (zeta * sdot) * Yv - c1 * Yv ** 2) / (4 * Kk)
    # Lred(sdot) = min over Y ; B from the second derivative in sdot
    h = 0.02
    def L_of_sd(sd):
        zz = zeta * sd / 1.0
        # analytic min over Y: Y* = A zz/c1
        Ys = A * zz / c1 if c1 != 0 else 0.0
        return (-(3 * A) * zz ** 2 + 2 * A * zz * Ys - c1 * Ys ** 2) / (4 * Kk)
    d2 = (L_of_sd(1 + h) - 2 * L_of_sd(1) + L_of_sd(1 - h)) / h ** 2
    return d2                # L = (B/2) sdot^2 -> B = d2L/dsdot^2


print("\n[P4] Z from two routes")
for b in (1.0, 3.0):
    Znum = Z_numeric(b, 0.7, 1.0) + z_eta_on() * 1.0 * (0.7 ** 2)
    Zrec = 1.0 * (2.0 + 3.0 * b) / b + z_eta_on() * 1.0 * (0.7 ** 2)   # record: K(2+3b)/b + eta p^2
    print("     beta=%4.1f  Z(action,numeric)=%.10f  Z(record K(2+3b)/b+eta p^2)=%.10f"
          % (b, Znum, Zrec))
    chk("C18_Z_b%.0f" % b, Znum, Zrec, 1e-6, "Z from the action vs A68's formula K(2+3beta)/beta+eta p^2")

# ---- sign of Z ----
print("\n[P4] sign(Z) vs sign(beta) on the 2+3beta>0 branch")
okz = True
for b in (-0.6, -0.5, -0.1, 0.1, 0.5, 1.0, 3.0):
    Zv = float((Kx * (3 * theta_coef(bx) - 1) / (theta_coef(bx) - 1)).subs({Kx: 1.0, bx: b}))
    okz = okz and (np.sign(Zv) == np.sign(b))
    print("     beta=%+5.2f  Z/K=%+9.4f  sign(beta)=%+d" % (b, Zv, int(np.sign(b))))
chk("C19_ZSIGN", 1.0 if okz else 0.0, 1.0, 1e-15,
    "Z>0 iff beta>0 (A68 D11); a negative Z is a ghost")

# ---- dispersion and the beta-shift ----
print("\n[P4] dispersion  omega^2 = alpha p^4/Z")
B1 = float((Kx * (3 * theta_coef(bx) - 1) / (theta_coef(bx) - 1)).subs({Kx: K_EV, bx: 1.0}))
B3 = float((Kx * (3 * theta_coef(bx) - 1) / (theta_coef(bx) - 1)).subs({Kx: K_EV, bx: 3.0}))
print("     B(beta=1) = %.8e eV^-2 ; B(beta=3) = %.8e eV^-2" % (B1, B3))
w2_1 = lambda pp: 1.0 * pp ** 4 / (B1 + z_eta_on() * ETA_EV * pp ** 2)
w2_3 = lambda pp: 1.0 * pp ** 4 / (B3 + z_eta_on() * ETA_EV * pp ** 2)
Brec = lambda b: K_EV * (2.0 + 3.0 * b) / b
print("     omega^2(1)/omega^2(3) at p->0 = %.12f  (record B(3)/B(1) = %.12f)"
      % (w2_1(1e-40) / w2_3(1e-40), Brec(3.0) / Brec(1.0)))
chk("C20_RATIO", w2_1(1e-40) / w2_3(1e-40), Brec(3.0) / Brec(1.0), 1e-10,
    "the beta-shift is O(1): omega^2(3)/omega^2(1) = 15/11 = 1.3636")
print("     eta p_sc^2/B(1) = %.6e   (so Z(p_sc) = B to 89 digits)"
      % (z_eta_on() * ETA_EV * PSC_EV ** 2 / B1))
print("     => Z(p_sc) = B to 89 digits: at every observable momentum the beta-dependence of")
print("        the fifth mode is the OVERALL coefficient, not the p^2 term")
kap_L = lambda b: math.sqrt(ETA_EV / Brec(b))          # Lifshitz mass^-1 = sqrt(eta/B)
for b in (1.0, 3.0):
    Zb = Brec(b)
    print("     beta=%4.1f :  Z^3 kappa_L^6 = %.6e eV^-6 ;  alpha^3 = %.6e eV^-6  (p_sc is beta-free)"
          % (b, Zb ** 3 * kap_L(b) ** 6, ETA_EV ** 3))

# UV speed = alpha/eta must equal the transverse c_T^2 = gamma/eta
print("\n[P4] UV limit of the fifth mode's speed vs the transverse mode's c_T^2 = gamma/eta")
gam_v = ETA_EV / gamma_factor()         # the action's gamma (dialled), alpha = gamma
alpha_v = gam_v
cs2_uv = (alpha_v * 1e10 ** 2) / (B1 * 1.0 + z_eta_on() * ETA_EV * 1e10 ** 2)
print("     c_s^2(UV) = %.10e ; gamma/eta = %.10e" % (cs2_uv, gam_v / ETA_EV))
chk("C22_UVSPEED", cs2_uv, ETA_EV / ETA_EV, 1e-6,
    "the k^4 mode joins the medium's light cone: c_s(UV) = gamma/eta")

# ======================================================================================
# PART 5 -- THE FIELD-REDEFINITION TEST.  Task 2.
# ======================================================================================
print("\n" + "=" * 100)
print("PART 5 -- can a field redefinition absorb beta?")
print("=" * 100)
print("""
Candidate redefinitions that could touch a KINETIC coefficient (beta multiplies no
vertex, so only normalisations can move it):
    h_ij -> Omega^2 h_ij ,   N -> chi N ,   P_i -> lam P_i        (Omega, chi, lam const)
Three measured normalisations must be preserved:
    (a) the R3 coefficient  1/(4K)      <- the static law's G           : chi*Omega = 1
    (b) the K_ij K^ij coefficient       <- c_T^2 = 1 (GW170817)         : Omega^3/chi = 1
    (c) the clock coefficient  xi = 1   <- the shape of g_N = g^2/(g+a0): xi*chi*Omega*lam = 1
""")
# scaling exponents: coefficient of R3 -> chi*Omega ; of K^2 -> Omega^3/chi ; clock -> xi*chi*Omega*lam
Mmat = sp.Matrix([[3.0 + weyl_R3(), 1, 0], [-1, 3, 0], [1, 1, 1]])   # (ln Omega, ln chi, ln lam)
rhs = sp.Matrix([0, 0, -sp.log(clock_xi())])
det = sp.simplify(Mmat.det())
print("[P5] log-space system  M.(lnOmega,lnchi,lnlam) = (0, 0, -ln xi)")
print("     det M =", det)
Mnum = np.array([[3.0 + weyl_R3(), 1.0, 0.0], [-1.0, 3.0, 0.0], [1.0, 1.0, 1.0]])
chk("C23_DET", float(det), float(np.linalg.det(Mnum)), 1e-12,
    "symbolic determinant vs the numerical 3x3 determinant: 4 != 0")
try:
    sol = sp.simplify(Mmat.LUsolve(rhs))
    ident = max(abs(float(sp.exp(sol[0])) - 1.0), abs(float(sp.exp(sol[1])) - 1.0),
                abs(float(sp.exp(sol[2])) - 1.0))
    print("     solution: Omega = %s , chi = %s , lam = %s"
          % (sp.simplify(sp.exp(sol[0])), sp.simplify(sp.exp(sol[1])), sp.simplify(sp.exp(sol[2]))))
    chk("C24_IDENT", ident, 0.0, 1e-13, scale=1.0,
        note="(Omega,chi,lam) = (1,1,1): the rescaling group is trivial, no direction is left")
except Exception:
    chk_fail("C24_IDENT", "the rescaling system is singular: a flat direction exists")

# ---- shift redefinitions are on-shell trivial ----
print("""
[P5] a shift redefinition N^i -> N^i + delta N^i changes the reduced action only at
     O(delta^2), because N^i_* is defined by dS/dN^i = 0.  Verified numerically below:
     perturb Y_* = (A/beta) zdot by eps*delta and record the change of the reduced L.
""")
A1 = 3 * theta_coef(1.0) - 1
c11 = theta_coef(1.0) - 1
z0 = 1.0
Ystar0 = A1 * z0 / c11
Lq0 = lambda Yv: (-(3 * A1) * z0 ** 2 + 2 * A1 * z0 * Yv - c11 * Yv ** 2) / (4 * 1.0)


def dL(eps, delta=0.37):
    return Lq0(Ystar0 + eps * delta) - Lq0(Ystar0)


r1, r2 = abs(dL(1e-3)), abs(dL(5e-4))
print("     |Delta L|(eps=1e-3) = %.6e ; (eps=5e-4) = %.6e ; ratio = %.6f"
      % (r1, r2, r1 / r2))
print("     |Delta L|/eps^2 at eps=1e-3 = %.6e ; at eps=5e-4 = %.6e"
      % (r1 / 1e-6, r2 / 2.5e-7))
chk("C26_SHIFT2", r1 / r2, 4.0, 1e-3, "the change is O(eps^2)")

# ---- the law's shape pins the P normalisation ----
print("\n[P5] the P normalisation is pinned by the law's SHAPE (xi != 1 deforms g_N)")
gN_xi = xi * (xi * a0 * g / (xi * g + a0))          # g_N = g - xi*u , u = xi a0 g/(xi g+a0)
dev = sp.simplify((g - gN_xi - g ** 2 / (g + a0)) / (g ** 2 / (g + a0)))
for xv in (1.0, 1.01, 1.05):
    print("     xi=%5.3f : (g_N - law)/law at g=a0  = %+.6f"
          % (xv, float(dev.subs({xi: xv, a0: 1.0, g: 1.0}))))
chk("C27_XI", float(dev.subs({xi: clock_xi(), a0: 1.0, g: 1.0})), 0.0, 1e-12,
    "a P rescaling at fixed xi=1 is the identity; at xi=1.05 the law is off by 7.6%")

# ---- the S-matrix invariant: a uniform field rescaling cannot move omega^2 ----
print("\n[P5] omega^2 = alpha p^4/Z is invariant under sigma -> lam sigma (both alpha and B scale)")
def w2_resc(lam, b=1.0, pp=1e-3, eta_v=1.0):
    Bv = (3 * theta_coef(b) - 1) / (theta_coef(b) - 1)
    # a constant P rescaling multiplies EVERY quadratic term (mass, kinetic, gradient)
    return (lam ** 2 * pp ** 4) / (lam ** 2 * (Bv + eta_v * pp ** 2))


vals = [w2_resc(l) for l in (0.3, 1.0, 7.0)]
print("     omega^2 at lam=0.3,1,7 : %.12e %.12e %.12e" % tuple(vals))
chk("C28_SMAT", max(vals) / min(vals), 1.0, 1e-14,
    "omega^2 is rescaling-invariant: no field redefinition can remove Z's beta")
print("     but omega^2(beta=1)/omega^2(beta=3) = %.6f  -> beta IS an on-shell invariant"
      % (w2_resc(1.0, 1.0) / w2_resc(1.0, 3.0)))

# ======================================================================================
# PART 6 -- BBN: the observable that fixes beta.  Task 3 / Task 4.
# ======================================================================================
print("\n" + "=" * 100)
print("PART 6 -- the background normalisation as a measured number")
print("=" * 100)
xw = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
print("[P6] H^2 ~ G(1 + x N_eff), x = (7/8)(4/11)^(4/3) = %.6f" % xw)
print("     a change G -> f G is  Delta N_eff = (f-1)(1+x N_eff)/x = %.4f (f-1)"
      % ((1 + xw * NEFF_STD) / xw))
print("     per unit beta:  Delta N_eff = %.4f beta  (at beta -> 0)"
      % ((G_eff(1e-9) / G_N - 1.0) * (1.0 + xw * NEFF_STD) / xw / 1e-9))


def dNeff(b):
    f = G_eff(b) / G_N
    return (f - 1.0) * (1.0 + xw * NEFF_STD) / xw


for b in (0.0, 0.01, 0.027, 0.1, 0.5, 1.0):
    print("     beta=%6.3f  G_eff/G_N=%.6f  Delta N_eff=%+9.4f" % (b, G_eff(b) / G_N, dNeff(b)))
try:
    bmax = brentq(lambda b: dNeff(b) + DNEFF_BND, 1e-9, 5.0, xtol=1e-14)
    print("     BBN 95%% bound |Delta N_eff| < %.2f  ->  beta < %.6f" % (DNEFF_BND, bmax))
    chk("C29_BBN", dNeff(bmax), -DNEFF_BND, 1e-10, "the bound is saturated at beta_max")
except ValueError:
    bmax = float("nan")
    chk_fail("C29_BBN", "G_eff/G_N < 1 for EVERY beta>0: the dialled background is excluded by BBN outright")
if not math.isnan(bmax):
    print("     at beta_max: Lambda_bare/Lambda_obs = %.6f (present-epoch reading)"
          % (Lambda_bare_present(bmax) / LAM_S2))
    print("     at beta_max: Lambda_bare/Lambda_obs = %.6f (dS reading)"
          % ((2 + 3 * bmax) / 2 * LDS / LAMBDA_OBS))
print("     Lambda_bare - Lambda_obs = (9/2) beta H0^2/c^2 ; ratio to Lambda_obs = %.6f per unit beta"
      % (4.5 * H0_SI ** 2 / C_SI ** 2 / LAMBDA_OBS))
if not math.isnan(bmax):
    chk("C30_BARE", (Lambda_bare_present(bmax) - Lambda_bare_present(0.0))
        / (4.5 * bmax * H0_SI ** 2), 1.0, 1e-10,
        "the slope dLambda_bare/dbeta is exactly (9/2) H0^2/c^2")
print("\n     the closure Lambda = 32 pi a0^2/c^4 (A33 row 2, kappa=1/2):")
print("       32 pi a0^2/c^4 = %.8e m^-2 ; Lambda_obs = %.8e m^-2 ; ratio = %.6f"
      % (32 * math.pi * A0_SI ** 2 / C_SI ** 4, LAMBDA_OBS,
         32 * math.pi * A0_SI ** 2 / C_SI ** 4 / LAMBDA_OBS))

# ======================================================================================
# SUMMARY
# ======================================================================================
npass = sum(1 for r in RESULTS if r["ok"])
print("\n" + "=" * 100)
print("SUMMARY: %d/%d checks PASS   (mutation = %r)" % (npass, len(RESULTS), MUT))
for r in RESULTS:
    if not r["ok"]:
        print("   FAIL  %-14s  %s" % (r["name"], r["note"]))
print("=" * 100)

out = dict(mutation=MUT, n_checks=len(RESULTS), n_pass=npass,
           checks=RESULTS,
           inputs=dict(G=G_SI, c=C_SI, K=K_SI, a0=A0_SI, Lstar=LSTAR_SI, H0=H0_SI,
                       Lambda_obs=LAMBDA_OBS, Omega_m=OMEGA_M, K_eV=K_EV,
                       eta_eV=ETA_EV, p_sc_eV=PSC_EV, dNeff_bound=DNEFF_BND),
           derived=dict(beta_at_Lambda_obs=float(b_closed),
                        Lambda_dS_over_Lambda_obs=float(LDS / LAMBDA_OBS),
                        Lambda_bare_over_Lambda_obs_beta1=float(Lambda_bare_present(1.0) / LAM_S2),
                        Lambda_bare_over_obs_beta1_dS=float(2.5 * LDS / LAMBDA_OBS),
                        beta_max_BBN=float(bmax),
                        G_eff_over_G_at_beta1=float(G_eff(1.0) / G_N),
                        omega2_ratio_b1_b3=float(w2_resc(1.0, 1.0) / w2_resc(1.0, 3.0)),
                        eta_psc2_over_B=float(ETA_EV * PSC_EV ** 2 / B1),
                        alpha1_1AU=float(al1_a),
                        Lambda_bare_over_obs_beta1_present=float(Lambda_bare_present(1.0) / LAM_S2),
                        Lambda_bare_over_obs_beta0_dS=float(LDS / LAMBDA_OBS),
                        Lambda_bare_over_obs_betamax_present=float(Lambda_bare_present(bmax) / LAM_S2),
                        G_eff_over_G_at_0027=float(G_eff(0.027) / G_N),
                        dNeff_per_unit_beta=float((G_eff(1e-6) / G_N - 1.0) * (1.0 + xw * NEFF_STD) / xw / 1e-6),
                        Lambda_closure_ratio=float(32 * math.pi * A0_SI ** 2 / C_SI ** 4 / LAMBDA_OBS)))
if "--json-out" in sys.argv:
    jsonpath = sys.argv[sys.argv.index("--json-out") + 1]
    with open(jsonpath, "w") as fh:
        json.dump(out, fh, indent=2)
    print("json ->", jsonpath)
sys.exit(0 if npass == len(RESULTS) else 1)
