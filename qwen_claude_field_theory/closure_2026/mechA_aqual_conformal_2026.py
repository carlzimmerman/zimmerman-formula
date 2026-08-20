#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mechA_aqual_conformal_2026.py
=============================
MECHANISM A -- the AQUAL / TeVeS route: the scalar sources gravity through its COUPLING to
matter, not through its own energy density.  Worked out for CARL'S OWN kernel, the a0-line
    g_obs^2 = g_bar^2 + a_0 g_bar    <=>    mu(x) = (sqrt(1+4x^2)-1)/(2x),  x = |grad Phi|/a_0
and NOT for standard MOND's.  Both footings on every dimensional number.

WHAT THIS FILE DOES, IN ORDER
  PART A  The AQUAL action for Carl's mu.  F(z) in closed form; the modified Poisson equation.
  PART B  rho_eff = (1/4 pi G) lap(Phi) - rho_b.  Exact closed form; the 1/r^2 scaling AND the
          coefficient.  Numerics.
  PART C  Is it an attractor?  (Answer: it is stronger than an attractor and that has a price.)
  PART D  LENSING.  Conformal-only vs the TeVeS disformal vector, weak field, symbolic.
  PART E  THE STANDING OBSTRUCTION.  What does the free function eat, in the scalar formulation?
          Exact inversion of the a0-line -> mu_s(s) = k s/(1-2s).  The contrast bookkeeping.
  PART F  THE KERNEL FORK.  Whether the OPERATIVE MS08 kernel is realisable in this class at all.
  PART G  Solar system.  Both kernels, both footings, against Sereno-Jetzer 2006.
  PART H  Verdict table.

PRACTICE: every number was COMPUTED FIRST and the check written around the computed value.
Exit 0 = all numbered checks pass.
"""
import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)


def densqrt(e):
    """sympy will not denest sqrt(4y^2+4y+1) -> 2y+1 on its own.  Factor every sqrt argument."""
    return sp.simplify(e.replace(
        lambda a: a.is_Pow and a.exp == sp.Rational(1, 2),
        lambda a: sp.sqrt(sp.factor(sp.expand(a.base)))))


# ---------------------------------------------------------------- constants / footings
G_ = 6.6743e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
MPC = 1000.0 * KPC
AU = 1.495978707e11
C = 2.99792458e8
GMSUN = 1.32712440018e20

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
MGAL = 1.0e11 * MSUN          # the standing reference spiral
# Sereno & Jetzer 2006 (astro-ph/0606197) Tab.1 via their Eq.(9), as banked in STANDING.md
SJ_BOUND = {"Earth": 3.66e-14, "Mars": 3.72e-14}   # m/s^2, 2 sigma constant radial anomaly
# lensing-vs-dynamics tolerance banked by the Phase-1 dust run (Brouwer+2021 full covariance)
LENS_TOL_DEX = 0.01027
LENS_TOL_DEX_REALISTIC = 0.5382 / np.log(10) * np.log(10)  # placeholder, replaced below
LENS_TOL_DEX_REALISTIC = 0.10147

head("PART 0 -- the target, both footings (COMPUTED FIRST)")
for f, a0 in A0.items():
    rM = np.sqrt(G_ * MGAL / a0)
    vc = (G_ * MGAL * a0) ** 0.25
    rho_asym_rM = np.sqrt(G_ * MGAL * a0) / (4 * np.pi * G_ * rM ** 2)
    info(f"{f:9s} a0 = {a0:.4e} m/s^2",
         f"r_M = {rM/KPC:8.3f} kpc   v_c = {vc/1e3:7.3f} km/s   "
         f"rho_target(r_M) = {rho_asym_rM:.4e} kg/m^3")
    info("", f"          a0/2 = {a0/2:.4e} m/s^2   (the alpha=1 landmine, PART G)")

# =====================================================================================
head("PART A -- the AQUAL action with CARL'S mu, and the modified Poisson equation")
# =====================================================================================
r"""
Bekenstein-Milgrom AQUAL, nonrelativistic:

    S = - int d^3x [ rho_b Phi  +  (a_0^2 / 8 pi G) F( |grad Phi|^2 / a_0^2 ) ]

Varying Phi:   div[ F'(z) grad Phi ] = 4 pi G rho_b,  z = |grad Phi|^2/a_0^2
so the interpolation function is  mu(x) = F'(x^2),  x = |grad Phi|/a_0.
"""
x, z, y, s_, a0s, GM, r, Gs, k_ = sp.symbols("x z y s a_0 GM r G k", positive=True)

mu_carl = (sp.sqrt(1 + 4 * x ** 2) - 1) / (2 * x)

# A1 -- Carl's mu IS the inverse of the a0-line, symbolically.
#   a0-line: g^2 = gb^2 + a0 gb  with gb = mu(g/a0) g.  Put x=g/a0, y=gb/a0 -> y = mu(x) x,
#   and the line reads  x^2 = y^2 + y.
y_of_x = sp.simplify(mu_carl * x)
line_resid = sp.simplify(sp.expand(x ** 2 - (y_of_x ** 2 + y_of_x)))
check(sp.simplify(line_resid) == 0,
      "A1  mu(x)=(sqrt(1+4x^2)-1)/(2x) is EXACTLY the inverse of the a0-line x^2 = y^2 + y",
      f"y(x) = mu*x = {sp.simplify(y_of_x)}")

# A2 -- and the forward form nu(y) = sqrt(1+1/y)
nu_carl = sp.sqrt(1 + 1 / y)
x_of_y = sp.simplify(nu_carl * y)
check(sp.simplify(sp.expand(x_of_y ** 2 - (y ** 2 + y))) == 0,
      "A2  nu(y) = sqrt(1+1/y) is the same law read forwards", f"x(y) = {x_of_y}")

# A3 -- round trip
rt = y_of_x.subs(x, x_of_y)
check(densqrt(rt - y) == 0,
      "A3  mu and nu are exact mutual inverses (round trip is the identity)",
      f"mu(nu(y)*y)*nu(y)*y = {densqrt(rt)}")

# A4 -- the free function F(z) in CLOSED FORM (this is the action, written down)
Fp = mu_carl.subs(x, sp.sqrt(z))              # F'(z) = mu(sqrt(z))
F_closed = sp.integrate(Fp, z)
F_closed = sp.simplify(F_closed)
check(sp.simplify(sp.diff(F_closed, z) - Fp) == 0,
      "A4  *** THE AQUAL FREE FUNCTION FOR THE a0-LINE, IN CLOSED FORM ***",
      f"F(z) = {F_closed}")

# A5 -- deep-MOND limit of F must be (2/3) z^{3/2}  (the AQUAL deep-MOND Lagrangian)
ser = sp.series(F_closed, z, 0, 2).removeO()
lead = sp.simplify(sp.limit(F_closed / z ** sp.Rational(3, 2), z, 0))
check(sp.simplify(lead - sp.Rational(2, 3)) == 0,
      "A5  deep-MOND limit F(z) -> (2/3) z^(3/2) EXACTLY -- the standard AQUAL deep limit",
      f"lim F/z^(3/2) = {lead};  series = {sp.simplify(ser)}")

# A6 -- Newtonian limit F' -> 1 - 1/(2x) : the alpha=1 signature, read off the ACTION
mu_large = sp.series(mu_carl, x, sp.oo, 3).removeO()
check(sp.simplify(sp.limit(mu_carl, x, sp.oo) - 1) == 0
      and sp.simplify(sp.limit((1 - mu_carl) * 2 * x, x, sp.oo) - 1) == 0,
      "A6  mu -> 1 - 1/(2x) + O(1/x^2):  the a0-line IS the alpha=1 class, from the action",
      f"asymptotic mu = {sp.simplify(mu_large)}")

info("MODIFIED POISSON EQUATION (the deliverable of PART A):",
     "div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho_b,   mu(x)=(sqrt(1+4x^2)-1)/(2x)")
info("equivalently, in first-integral form for any spherical rho_b:",
     "mu(g/a0) g = g_bar(r) = G M_b(<r)/r^2   =>   g^2 = g_bar^2 + a0 g_bar   (the a0-line)")

# A7 -- verify the spherical first integral IS the a0-line, from the divergence form
g_sym = sp.Function("g")
gb_sym = GM / r ** 2
g_sol = sp.sqrt(gb_sym ** 2 + a0s * gb_sym)
lhs = sp.simplify(sp.powsimp(mu_carl.subs(x, g_sol / a0s) * g_sol, force=True))
check(densqrt(lhs - gb_sym) == 0,
      "A7  the spherical first integral mu(g/a0) g = G M/r^2 is solved EXACTLY by the a0-line",
      f"mu(g/a0)*g = {densqrt(lhs)}")

# =====================================================================================
head("PART B -- rho_eff = (1/4 pi G) lap(Phi) - rho_b:  the SCALING and the COEFFICIENT")
# =====================================================================================
# Outside the baryons, lap(Phi_N) = 0, so rho_eff = (1/4 pi G) (1/r^2) d/dr [ r^2 (g - g_bar) ].
dg = sp.simplify(g_sol - gb_sym)
rho_eff = sp.simplify(sp.diff(r ** 2 * dg, r) / (4 * sp.pi * Gs * r ** 2))
rho_eff = sp.simplify(sp.powsimp(rho_eff, force=True))
info("EXACT rho_eff(r):", f"{rho_eff}")

rho_target = sp.sqrt(Gs * GM / Gs * a0s * Gs) / (4 * sp.pi * Gs * r ** 2)  # careful below
# write the target unambiguously: sqrt(G M_b a0)/(4 pi G r^2) with GM = G*M_b
Mb = sp.symbols("M_b", positive=True)
rho_target = sp.sqrt(Gs * Mb * a0s) / (4 * sp.pi * Gs * r ** 2)

ratio = sp.simplify((rho_eff / rho_target).subs(GM, Gs * Mb))
ratio = sp.simplify(sp.powsimp(sp.radsimp(ratio), force=True))
info("rho_eff / [ sqrt(G M_b a0)/(4 pi G r^2) ] =", f"{ratio}")

# B1 -- the ratio is exactly 1/sqrt(1+y), y = G M_b/(a0 r^2)
y_expr = Gs * Mb / (a0s * r ** 2)
check(sp.simplify(ratio - 1 / sp.sqrt(1 + y_expr)) == 0,
      "B1  *** rho_eff(r) = [ sqrt(G M_b a0) / (4 pi G r^2) ] * (1+y)^(-1/2)  EXACTLY, "
      "y = G M_b/(a0 r^2) ***")

# B2 -- deep-MOND limit: coefficient EXACTLY 1, no pure number
lim_ratio = sp.limit(ratio, r, sp.oo)
check(sp.simplify(lim_ratio - 1) == 0,
      "B2  *** THE COEFFICIENT IS EXACTLY 1.000000 -- NOT off by any pure number. "
      "rho_eff -> sqrt(G M_b a0)/(4 pi G r^2), the sf36 amplitude law, verbatim ***",
      f"lim_{{r->inf}} rho_eff/rho_target = {lim_ratio}")

# B3 -- the 1/r^2 scaling (logarithmic slope -> -2 exactly)
slope = sp.simplify(sp.limit(sp.diff(sp.log(rho_eff.subs(GM, Gs * Mb)), sp.log(r)).doit()
                             if False else r * sp.diff(rho_eff.subs(GM, Gs * Mb), r)
                             / rho_eff.subs(GM, Gs * Mb), r, sp.oo))
check(sp.simplify(slope + 2) == 0,
      "B3  logarithmic slope d ln rho_eff / d ln r -> -2 EXACTLY (isothermal, as sf36 says)",
      f"slope = {slope}")

# B4 -- numeric confirmation of the exact closed form against a finite-difference Laplacian
def g_obs_line(gb, a0):
    return np.sqrt(gb * gb + a0 * gb)


def rho_eff_num(rr, M, a0, h=1e-6):
    """(1/4 pi G) (1/r^2) d/dr[r^2 (g_obs - g_bar)] by central differences."""
    def f(rx):
        gb = G_ * M / rx ** 2
        return rx ** 2 * (g_obs_line(gb, a0) - gb)
    dr = h * rr
    return (f(rr + dr) - f(rr - dr)) / (2 * dr) / (4 * np.pi * G_ * rr ** 2)


def rho_eff_closed(rr, M, a0):
    yv = G_ * M / (a0 * rr ** 2)
    return np.sqrt(G_ * M * a0) / (4 * np.pi * G_ * rr ** 2) / np.sqrt(1 + yv)


print()
for f, a0 in A0.items():
    rM = np.sqrt(G_ * MGAL / a0)
    worst = 0.0
    for mult in [0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]:
        rr = mult * rM
        num, cl = rho_eff_num(rr, MGAL, a0), rho_eff_closed(rr, MGAL, a0)
        worst = max(worst, abs(num / cl - 1))
    check(worst < 1e-7,
          f"B4[{f}] closed form matches a finite-difference Laplacian at 7 radii",
          f"max frac deviation = {worst:.2e}")

print()
info("APPROACH TO THE COEFFICIENT (both footings identical, since the ratio depends only on y):")
for mult in [1.0, 2.0, 3.0, 10.0, 30.0, 100.0]:
    yv = 1.0 / mult ** 2
    info(f"   r = {mult:6.1f} r_M  ->  y = {yv:.4e}",
         f"rho_eff / [sqrt(G M a0)/(4 pi G r^2)] = {1/np.sqrt(1+yv):.6f}")

# B5 -- the coefficient is a THEOREM OF THE DEEP-MOND LIMIT, not of Carl's kernel.
#       Check with a completely different kernel that shares the deep limit (MS08 exponential).
def nu_ms08(yv):
    return 1.0 / (1.0 - np.exp(-np.sqrt(yv)))


def rho_eff_num_kernel(rr, M, a0, nu, h=1e-6):
    def f(rx):
        gb = G_ * M / rx ** 2
        return rx ** 2 * gb * (nu(gb / a0) - 1.0)
    dr = h * rr
    return (f(rr + dr) - f(rr - dr)) / (2 * dr) / (4 * np.pi * G_ * rr ** 2)


a0c = A0["canonical"]
rMc = np.sqrt(G_ * MGAL / a0c)
rr = 300.0 * rMc
coef_ms08 = rho_eff_num_kernel(rr, MGAL, a0c, nu_ms08) / (
    np.sqrt(G_ * MGAL * a0c) / (4 * np.pi * G_ * rr ** 2))
coef_line = rho_eff_num(rr, MGAL, a0c) / (
    np.sqrt(G_ * MGAL * a0c) / (4 * np.pi * G_ * rr ** 2))
check(abs(coef_ms08 - 1) < 1e-4 and abs(coef_line - 1) < 1e-4,
      "B5  the COEFFICIENT 1 is a theorem of the deep-MOND limit, NOT of Carl's kernel "
      "(MS08 exponential gives the same 1)",
      f"at r=300 r_M: a0-line {coef_line:.6f}, MS08 {coef_ms08:.6f}")

# B6 -- the total inferred dynamical mass
info("", "")
info("EQUIVALENTLY: M_dyn(<r) = r^2 g_obs/G = nu(y) M_b, and rho_eff is its radial derivative /4 pi r^2.")
Mdyn_over_Mb = sp.simplify(g_sol * r ** 2 / (Gs * Mb)).subs(GM, Gs * Mb)
check(sp.simplify(Mdyn_over_Mb - sp.sqrt(1 + 1 / y_expr)) == 0,
      "B6  M_dyn(<r)/M_b = nu(y) = sqrt(1+1/y) exactly", f"{sp.simplify(Mdyn_over_Mb)}")

# =====================================================================================
head("PART C -- is the amplitude law an ATTRACTOR?  (it is something stronger, and it costs)")
# =====================================================================================
r"""
The AQUAL equation is a quasilinear ELLIPTIC equation.  For mu(x) x monotone increasing in x
(true for the a0-line: d(mu x)/dx = dy/dx > 0), the action functional
    E[Phi] = int [ (a0^2/8 pi G) F(|grad Phi|^2/a0^2) + rho_b Phi ]
is strictly convex in grad Phi, so with the boundary condition grad Phi -> 0 at infinity the
solution EXISTS and is UNIQUE (Bekenstein & Milgrom 1984).  There is no free data at all.
"""
dydx = sp.simplify(sp.diff(y_of_x, x))
check(sp.simplify(sp.limit(dydx, x, 0)) >= 0 and all(
        float(dydx.subs(x, v)) > 0 for v in [1e-6, 1e-3, 0.1, 1.0, 10.0, 1e3, 1e6]),
      "C1  d(mu x)/dx > 0 on (0,inf) => the AQUAL functional is strictly convex => "
      "the solution is UNIQUE, not merely attracting",
      f"d(mu x)/dx = {sp.simplify(dydx)}")

# C2 -- convexity of F in the right variable: F'(z) > 0 and (mu x)' > 0
check(all(float(Fp.subs(z, v)) > 0 for v in [1e-8, 1e-4, 1.0, 1e4, 1e8]),
      "C2  F'(z) = mu > 0 everywhere (no ghost branch in the nonrelativistic functional)")

info("", "")
info("*** ANSWER TO 'WHAT MAKES THE a0-LINE AN ATTRACTOR' ***",
     "In Mechanism A it is NOT an attractor -- it is a CONSTRAINT.  rho_eff is an instantaneous "
     "algebraic functional of rho_b with ZERO free data; there is nothing to relax toward.")
info("THE PRICE, stated plainly:",
     "rho_eff is PHANTOM.  It carries no energy, no momentum and no entropy.  It therefore "
     "CANNOT be the Omega_dm the CMB measures.  Mechanism A is a SECOND sector alongside the "
     "DBI condensate, not a replacement for it.")

# C3 -- how much energy does the AQUAL scalar itself actually carry?  (Phase-1 banked ~1.3e-7)
def rho_phi_aqual(rr, M, a0):
    """Energy density of the AQUAL field itself, deep-MOND: u = (a0^2/8 pi G) [ z F' - F ]
    evaluated on the solution.  Deep limit F=(2/3)z^{3/2}, zF'-F = (1/3) z^{3/2} = (1/3)(g/a0)^3."""
    gb = G_ * M / rr ** 2
    g = g_obs_line(gb, a0)
    zz = (g / a0) ** 2
    # use the EXACT F, not the deep limit
    Fnum = sp.lambdify(z, F_closed, "numpy")
    Fpnum = sp.lambdify(z, Fp, "numpy")
    return (a0 ** 2 / (8 * np.pi * G_)) * (zz * Fpnum(zz) - Fnum(zz))


print()
for f, a0 in A0.items():
    rM = np.sqrt(G_ * MGAL / a0)
    vals = []
    for mult in [0.5, 1.0, 3.0]:
        rr = mult * rM
        vals.append(rho_phi_aqual(rr, MGAL, a0) / (rho_eff_closed(rr, MGAL, a0) * C ** 2))
    info(f"C3[{f}] rho_phi/(rho_eff c^2) at 0.5/1/3 r_M",
         f"{vals[0]:.4e} / {vals[1]:.4e} / {vals[2]:.4e}")
    check(all(0 < v < 1e-5 for v in vals),
          f"C3[{f}] the scalar's OWN energy density is <1e-5 of the phantom density "
          "(so the phantom really is a coupling effect, not an energy effect)")

# =====================================================================================
head("PART D -- LENSING.  Conformal-only vs the TeVeS disformal vector (weak field, symbolic)")
# =====================================================================================
Phi, Psi, ph = sp.symbols("Phi Psi varphi")
eps = sp.symbols("epsilon", positive=True)


def weak(expr, order=2):
    """Linearise in the bookkeeping parameter eps."""
    return sp.series(expr, eps, 0, order).removeO()


# metric g = diag(-(1+2Phi), (1-2Psi) x3), all potentials O(eps)
gtt = -(1 + 2 * eps * Phi)
gxx = (1 - 2 * eps * Psi)
phi_e = eps * ph

# ---- D1: PURE CONFORMAL  g~ = e^{2 phi} g
gt_tt = sp.simplify(weak(sp.exp(2 * phi_e) * gtt))
gt_xx = sp.simplify(weak(sp.exp(2 * phi_e) * gxx))
Phi_t = sp.simplify(sp.expand(-(gt_tt + 1) / 2 / eps))
Psi_t = sp.simplify(sp.expand((1 - gt_xx) / 2 / eps))
check(sp.simplify(Phi_t - (Phi + ph)) == 0 and sp.simplify(Psi_t - (Psi - ph)) == 0,
      "D1  PURE CONFORMAL: Phi~ = Phi + varphi  and  Psi~ = Psi - varphi",
      f"Phi~={Phi_t}, Psi~={Psi_t}")

lens_conf = sp.simplify(Phi_t + Psi_t)
check(sp.simplify(lens_conf - (Phi + Psi)) == 0,
      "D2  *** PURE CONFORMAL: the lensing potential Phi~+Psi~ = Phi+Psi -- the scalar CANCELS. "
      "Light does not see the MOND field AT ALL. ***", f"Phi~+Psi~ = {lens_conf}")

# ---- D3: TeVeS disformal  g~ = e^{-2phi}(g + U U) - e^{2phi} U U,  U_mu = (-(1+eps Phi),0,0,0)
Ut = -(1 + eps * Phi)
UU_tt = sp.simplify(Ut * Ut)
gd_tt = sp.simplify(weak(sp.exp(-2 * phi_e) * (gtt + UU_tt) - sp.exp(2 * phi_e) * UU_tt))
gd_xx = sp.simplify(weak(sp.exp(-2 * phi_e) * gxx))
Phi_d = sp.simplify(sp.expand(-(gd_tt + 1) / 2 / eps))
Psi_d = sp.simplify(sp.expand((1 - gd_xx) / 2 / eps))
check(sp.simplify(Phi_d - (Phi + ph)) == 0 and sp.simplify(Psi_d - (Psi + ph)) == 0,
      "D3  TeVeS DISFORMAL: Phi~ = Phi + varphi AND Psi~ = Psi + varphi (SAME sign)",
      f"Phi~={Phi_d}, Psi~={Psi_d}")

lens_dis = sp.simplify(Phi_d + Psi_d)
check(sp.simplify(lens_dis - (Phi + Psi + 2 * ph)) == 0,
      "D4  *** TeVeS DISFORMAL: Phi~+Psi~ = 2(Phi_N + varphi) = 2 Phi~_dyn -- lensing tracks "
      "dynamics EXACTLY, for ANY free function. ***", f"Phi~+Psi~ = {lens_dis}")

# unit-norm check on U so D3 is not an accident of normalisation
gm = sp.diag(gtt, gxx, gxx, gxx)
ginv = gm.inv()
norm = sp.simplify(weak(ginv[0, 0] * Ut * Ut, 3))
check(sp.simplify(sp.limit(norm, eps, 0) + 1) == 0,
      "D5  control: U_mu is unit timelike to the order used (g^{mu nu}U_mu U_nu -> -1)",
      f"norm = {sp.simplify(norm)}")

# ---- D6: how badly does conformal-only fail, in sigma?
print()
info("HOW BADLY conformal-only fails, quantified on the framework's own lensing datum:")
info("  tolerance (Phase-1 dust run, Brouwer+2021 full covariance):",
     f"{LENS_TOL_DEX:.5f} dex (tightest) / {LENS_TOL_DEX_REALISTIC:.5f} dex (realistic)")
worst_sig = 0.0
for f, a0 in A0.items():
    rM = np.sqrt(G_ * MGAL / a0)
    row = []
    for rr, nm in [(40 * KPC, "40 kpc"), (rM, "r_M"), (2.2 * MPC, "2.2 Mpc")]:
        gb = G_ * MGAL / rr ** 2
        yv = gb / a0
        nu = np.sqrt(1 + 1 / yv)
        dex = np.log10(nu)                       # M_lens/M_dyn = 1/nu  ->  deficit in dex
        sig = dex / LENS_TOL_DEX
        sig_r = dex / LENS_TOL_DEX_REALISTIC
        worst_sig = max(worst_sig, sig)
        row.append((nm, yv, nu, dex, sig, sig_r))
    for nm, yv, nu, dex, sig, sig_r in row:
        info(f"  {f:9s} r={nm:>8s}: y={yv:.3e}",
             f"nu={nu:8.3f}  M_lens/M_dyn = 1/nu = {1/nu:.5f} = -{dex:.4f} dex "
             f"=> {sig:7.1f} sigma (tightest) / {sig_r:6.1f} sigma (realistic)")
check(worst_sig > 100,
      "D6  *** PURE CONFORMAL COUPLING IS DEAD: it predicts M_lens = M_b exactly, a deficit of "
      f"up to {worst_sig:.0f} sigma at the outer KiDS radius.  (This re-derives Bekenstein & "
      "Sanders 1994; it is not new.) ***")
check(np.log10(np.sqrt(2)) / LENS_TOL_DEX > 10,
      "D7  the kill does not depend on the outer bin: even AT the MOND radius (y=1, nu=sqrt2) "
      f"the deficit is {np.log10(np.sqrt(2))/LENS_TOL_DEX:.1f} sigma")

# D8 -- the ACTUAL stress the surviving realisation carries (this is what sf34 constrains).
#   Relativistic k-essence P(X), X = -g^{mu nu} d_mu phi d_nu phi / 2; static radial phi:
#     rho_phi = -P,  p_r = P_X phi'^2 + P,  p_t = P  ->  p_r + 2 p_t = P_X phi'^2 + 3P.
#   *** ERROR I MADE AND THE CHECK CAUGHT (logged; it ran AGAINST the framework): I first wrote
#   P_X phi'^2 = +3P for the deep-MOND power P = -A(-X)^{3/2}.  It is -3P, so p_r + 2 p_t = 0
#   EXACTLY, not 6P.  I had manufactured a stress that is not there. ***
Xr, As = sp.symbols("X_r A", positive=True)
w_, sig = sp.symbols("w sigma", positive=True)
P_deep = -As * (w_ / 2) ** sp.Rational(3, 2)             # P as a function of w = phi'^2 = -2X
combo_deep = sp.simplify(-2 * w_ * sp.diff(P_deep, w_) + 3 * P_deep)   # P_X phi'^2 + 3P
check(sp.simplify(combo_deep) == 0,
      "D8  *** DEEP-MOND k-essence: p_r + 2 p_t = 0 EXACTLY.  The MOND scalar's own stress "
      "sits precisely at sf34's R-LENS condition -- this IS the 'n = 3/2 traceless' point the "
      "standing obstruction names. ***", f"p_r+2p_t = {combo_deep}")

# D8b -- and it is EXACTLY the 3/2 power that does it, nothing else
n_ = sp.symbols("n", positive=True)
P_gen = -As * w_ ** n_
check(sp.solve(sp.simplify(-2 * w_ * sp.diff(P_gen, w_) + 3 * P_gen), n_) == [sp.Rational(3, 2)],
      "D8b p_r + 2 p_t = 0 iff P ~ w^(3/2) -- the deep-MOND power and no other",
      f"solutions n = {sp.solve(sp.simplify(-2*w_*sp.diff(P_gen, w_) + 3*P_gen), n_)}")

# D8c -- so for CARL'S FULL kernel (not just its deep limit) the stress is nonzero.  Compute it.
#   mu_s(s) = k s/(1-2s)  and  P_X = -2 dP/dw  gives  dP/dw = -(N/2) mu_s_hat(s), s = sqrt(w)/a0.
#   In units a0 = 1 and dropping the overall normalisation N (which cancels in every ratio):
#   sp.integrate picks the log(2s-1) branch (complex on 0<s<1/2), which silently poisoned this
#   block with NaN on the first run.  Write the antiderivative explicitly on the real branch and
#   VERIFY it by differentiation instead.
P_hat = s_ ** 2 / 2 + s_ / 2 + sp.log(1 - 2 * s_) / 4                # = P(s), up to a positive norm
dPdw_hat = sp.simplify(sp.diff(P_hat, s_) / (2 * s_))                # w = s^2 => dw = 2s ds
check(sp.simplify(dPdw_hat + s_ / (1 - 2 * s_)) == 0,
      "D8c normalisation control: the constructed P(s) reproduces dP/dw = -mu_s_hat(s) exactly "
      "(explicit real-branch antiderivative; sympy's own integrate returned the complex branch "
      "and NaN-poisoned this block on the first run -- logged)",
      f"P(s) = {P_hat}")
rho_hat = sp.simplify(-P_hat)
check(sp.simplify(sp.series(rho_hat, s_, 0, 4).removeO() - sp.Rational(2, 3) * s_ ** 3) == 0,
      "D8c2 rho_phi = -P > 0 and -> (2/3)s^3 in the deep limit (positive energy, correct power)",
      f"rho_phi(s) = {rho_hat}, series = {sp.series(rho_hat, s_, 0, 4)}")
ratio_stress = sp.simplify((-2 * s_ ** 2 * dPdw_hat + 3 * P_hat) / (-P_hat))   # (p_r+2p_t)/rho_phi
check(abs(float(sp.limit(ratio_stress, s_, 0))) < 1e-12,
      "D8d (p_r+2p_t)/rho_phi -> 0 as s -> 0, recovering D8 in the deep limit",
      f"(p_r+2p_t)/rho_phi = {sp.simplify(ratio_stress)}")

print()
LENS_TOL_EPS = 0.0489     # Phase-1 dust run, tightest defensible |p_r+2p_t|/(rho c^2)
rs_num = sp.lambdify(s_, ratio_stress, "numpy")
rho_hat_num = sp.lambdify(s_, rho_hat, "numpy")       # rho_phi = -P, in units a0^2/(8 pi G)
worst_head = np.inf
finite_all = True
for f, a0 in A0.items():
    rM = np.sqrt(G_ * MGAL / a0)
    for mult, nm in [(0.5, "0.5 r_M"), (1.0, "1.0 r_M"), (3.0, "3.0 r_M")]:
        rr = mult * rM
        yv = G_ * MGAL / (a0 * rr ** 2)
        sv = np.sqrt(yv * yv + yv) - yv        # y = O(1) here, float64 is exact enough
        rat = float(rs_num(sv))
        rho_phi = (a0 ** 2 / (8 * np.pi * G_)) * float(rho_hat_num(sv))   # J/m^3
        share = rho_phi / (rho_eff_closed(rr, MGAL, a0) * C ** 2)
        epsA = abs(rat) * share
        head_ = LENS_TOL_EPS / epsA
        finite_all = finite_all and np.isfinite(rat) and np.isfinite(share) and np.isfinite(head_)
        worst_head = min(worst_head, head_)
        info(f"D9[{f}] {nm}: s={sv:.5f}",
             f"(p_r+2p_t)/rho_phi = {rat:+.4f} | rho_phi/(rho_eff c^2) = {share:.4e} | "
             f"eps = {epsA:.4e} | headroom {head_:.3e}x = {np.log10(head_):.2f} orders")
check(finite_all,
      "D9a NON-VACUITY GUARD: every D9 number is finite.  (On the first run they were all NaN "
      "and min(inf, nan) let the headroom check PASS VACUOUSLY -- caught, logged, guarded.)")
check(finite_all and worst_head > 1e4,
      "D9  *** Mechanism A's REAL stress is at least "
      f"{np.log10(worst_head):.2f} orders inside the tightest lensing tolerance (0.0489). "
      "sf34's p_r = -2 p_t is satisfied not because the equation of state is tuned but because "
      "the carrier holds almost no energy -- and in the deep limit it is satisfied EXACTLY. ***")

info("", "")
info("*** THEREFORE MECHANISM A REQUIRES THE VECTOR. ***",
     "The scalar alone cannot do it.  The disformal U_mu piece is not optional dressing; it is "
     "what carries the MOND field into the null cone.  This is exactly the AeST structure the "
     "framework already names as its completion -- so Mechanism A is CONSISTENT with, and "
     "in fact IMPLIED BY, the standing relativistic completion.")

# =====================================================================================
head("PART E -- THE STANDING OBSTRUCTION.  What does the free function actually eat?")
# =====================================================================================
r"""
Two inequivalent formulations produce the SAME spherical phenomenology:

 (A) SINGLE-POTENTIAL (Bekenstein-Milgrom AQUAL):
       div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho_b
     free function eats the TOTAL field |grad Phi|.

 (B) TWO-POTENTIAL (TeVeS / conformal-coupled scalar), Phi_dyn = Phi_N + varphi :
       lap Phi_N = 4 pi G rho_b ,   div[ mu_s(|grad varphi|/a0) grad varphi ] = 4 pi G k rho_b
     free function eats the SCALAR'S OWN gradient |grad varphi|.

(B) is the one Mechanism A is about, because only in (B) does the scalar couple through the
metric.  R-LENS and R-SCREEN are questions about (B)'s mu_s.  Settle them with algebra.
"""
# E1 -- R-LENS is answered by PART D and does NOT constrain mu_s at all.
#   NOTE the hypothesis, stated explicitly: this needs Psi_E = Phi_E in the Einstein frame,
#   i.e. NO net anisotropic stress from the gravitational sector.  See E1b for what that costs.
check(sp.simplify((lens_dis - 2 * Phi_d).subs(Psi, Phi)) == 0,
      "E1  *** R-LENS DISSOLVES IN MECHANISM A.  Given Psi_E = Phi_E, Phi~+Psi~ = 2 Phi~ "
      "identically, for ANY mu_s.  The lensing requirement places NO condition on the free "
      "function's argument. ***")
check(sp.simplify(lens_dis - 2 * Phi_d) == sp.simplify(Psi - Phi),
      "E1b HYPOTHESIS MADE EXPLICIT: the residual is exactly (Psi_E - Phi_E), i.e. the Einstein-"
      "frame slip.  The AQUAL scalar contributes <2e-7 of it (C3); the VECTOR's stress was NOT "
      "computed here -- taken from the framework's banked AeST result gamma_PPN = 1.",
      f"Phi~+Psi~ - 2 Phi~ = {sp.simplify(lens_dis - 2*Phi_d)}")
info("    Contrast with the five dead realisations:",
     "there the halo was carried by a STRESS, so lensing constrained the equation of state and "
     "hence the free function.  Here the halo is carried by a COUPLING, so it does not.")

# E2 -- exact inversion: what is mu_s for the a0-line?
#   varphi' = g_obs - g_bar = a0 [ sqrt(y^2+y) - y ],  s := varphi'/a0
s_of_y = sp.simplify(sp.sqrt(y ** 2 + y) - y)
# invert
sol = sp.solve(sp.Eq(s_, s_of_y), y, dict=True)
y_of_s = sp.simplify(sol[0][y])
check(sp.simplify(y_of_s - s_ ** 2 / (1 - 2 * s_)) == 0,
      "E2  *** EXACT INVERSION:  y = s^2/(1-2s),  s = varphi'/a0 ***",
      f"y(s) = {y_of_s}")

mu_s = sp.simplify(k_ * y_of_s / s_)
check(sp.simplify(mu_s - k_ * s_ / (1 - 2 * s_)) == 0,
      "E3  *** THE TeVeS FREE FUNCTION FOR CARL'S a0-LINE, IN CLOSED FORM: "
      "mu_s(s) = k s/(1-2s), a SIMPLE POLE AT s = 1/2 ***", f"mu_s = {mu_s}")

# E4 -- deep-MOND limit of mu_s
check(sp.simplify(sp.limit(mu_s / s_, s_, 0) - k_) == 0,
      "E4  deep-MOND: mu_s -> k s (the AQUAL-scalar deep limit), so the a0-line's deep behaviour "
      "is standard")

# E5 -- the RANGE of s is bounded: s in (0, 1/2)
check(sp.simplify(sp.limit(s_of_y, y, sp.oo) - sp.Rational(1, 2)) == 0
      and sp.simplify(sp.limit(s_of_y, y, 0)) == 0,
      "E5  *** s = varphi'/a0 is BOUNDED: s -> 0 as y -> 0 and s -> 1/2 as y -> infinity. "
      "The scalar's own gradient NEVER exceeds a0/2. ***")

ds_dy = sp.simplify(sp.diff(s_of_y, y))
# PROVE positivity symbolically -- float cancels catastrophically at large y
# ds/dy = [ (y+1/2) - sqrt(y(y+1)) ] / sqrt(y(y+1)) ; numerator > 0 iff (y+1/2)^2 > y(y+1)
num_e6 = sp.simplify(sp.together(ds_dy) * sp.sqrt(y) * sp.sqrt(y + 1))
gap = sp.expand((y + sp.Rational(1, 2)) ** 2 - y * (y + 1))
check(sp.simplify(num_e6 - (y + sp.Rational(1, 2) - sp.sqrt(y * (y + 1)))) == 0
      and gap == sp.Rational(1, 4),
      "E6  s(y) is strictly MONOTONE INCREASING => the map s <-> y is a bijection "
      "(0,1/2)<->(0,inf).  PROOF: ds/dy > 0 iff (y+1/2)^2 - y(y+1) > 0, and that difference "
      "is the CONSTANT 1/4 > 0.",
      f"ds/dy = {ds_dy};  (y+1/2)^2 - y(y+1) = {gap}")
import mpmath as mpm
mpm.mp.dps = 60
_ds = lambda v: (mpm.mpf(v) + mpm.mpf(1) / 2 - mpm.sqrt(mpm.mpf(v) * (v + 1))) / mpm.sqrt(
    mpm.mpf(v) * (v + 1))
check(all(_ds(v) > 0 for v in [1e-12, 1e-4, 1.0, 1e4, 1e8, 1e12]),
      "E6b high-precision numeric confirmation of E6 at 6 decades incl. y=1e12 "
      "(float64 gives 0 here: the FAILURE at first run was a cancellation artifact, "
      "and it ran AGAINST the framework)",
      f"ds/dy(1e8) = {mpm.nstr(_ds(1e8), 8)}, ds/dy(1e12) = {mpm.nstr(_ds(1e12), 8)}")

# E7 -- THE CONTRAST BOOKKEEPING.  This is the whole question.
head("PART E (cont) -- the contrast bookkeeping: does eating |grad varphi| carry the "
     "total field's contrast?")


def y_of_r_sun(rr, a0):
    return (GMSUN / rr ** 2) / a0


# THE STABLE FORM.  mu_s(s) s = k y  =>  mu_s/k = y/s IDENTICALLY.  Computing mu_s as
# s/(1-2s) in float64 divides by zero at 1 AU (1-2s underflows); y/s does not.
check(sp.simplify(sp.simplify(mu_s / k_).subs(s_, s_of_y) - y / s_of_y) == 0,
      "E6c IDENTITY used for the numerics: mu_s/k = y/s exactly (avoids the 1-2s underflow)")


def s_hi(yv):
    """s(y) = sqrt(y^2+y) - y at 60 digits."""
    yv = mpm.mpf(yv)
    return mpm.sqrt(yv * yv + yv) - yv


print()
CONTRASTS = {}
for f, a0 in A0.items():
    y_1au = y_of_r_sun(AU, a0)
    # Galactic field at the solar circle: sf06's environment.  g_gal ~ v_c^2/R0
    v0, R0 = 233e3, 8.2 * KPC
    y_gal = (v0 ** 2 / R0) / a0
    s1, sg = s_hi(y_1au), s_hi(y_gal)
    m1, mg = mpm.mpf(y_1au) / s1, mpm.mpf(y_gal) / sg          # mu_s/k = y/s
    info(f"{f:9s} 1 AU  : y = {y_1au:.4e}",
         f"s = {mpm.nstr(s1, 12)}   1/2 - s = {mpm.nstr(mpm.mpf(0.5)-s1, 6)}   "
         f"mu_s/k = {mpm.nstr(m1, 6)}")
    info(f"{'':9s} solar-circle env: y = {y_gal:.4e}",
         f"s = {mpm.nstr(sg, 12)}   1/2 - s = {mpm.nstr(mpm.mpf(0.5)-sg, 6)}   "
         f"mu_s/k = {mpm.nstr(mg, 6)}")
    C_total = y_1au / y_gal
    C_s = float(s1 / sg)
    C_mus = float(m1 / mg)
    CONTRASTS[f] = (C_total, C_s, C_mus)
    info(f"{'':9s} CONTRASTS 1 AU / environment:",
         f"total field y: {C_total:.4e}   |  s itself: {C_s:.4f}   |  mu_s: {C_mus:.4e}")
    check(C_s < 1.2,
          f"E7[{f}] the scalar's gradient s ITSELF has contrast only {C_s:.3f} -- "
          "sf06's theorem applies to it with full force, exactly as the obstruction feared")
    check(abs(np.log10(C_mus) - np.log10(C_total)) < 0.05,
          f"E8[{f}] *** BUT mu_s CARRIES THE FULL TOTAL-FIELD CONTRAST: "
          f"mu_s ratio {C_mus:.4e} vs total-field ratio {C_total:.4e} "
          f"({abs(np.log10(C_mus)-np.log10(C_total)):.4f} dex apart, = the bounded factor "
          f"s_env/s_sun = {float(sg/s1):.4f}) ***")

# E9 -- and the reason is GENERAL, not special to the a0-line
info("E9  THE GENERAL LEMMA behind E8:",
     "mu_s/k = y/s exactly.  So contrast(mu_s) = contrast(y) x [s_env/s_local].  If s is "
     "BOUNDED (as it is here, s<1/2), the bracket is O(1) and mu_s inherits the ENTIRE dynamic "
     "range of the total field.  Boundedness of the scalar's gradient is not the obstruction -- "
     "it is the mechanism.")
check(all(abs(np.log10(v[2]) - np.log10(v[0])) < 0.05 for v in CONTRASTS.values()),
      "E9  the lemma holds on both footings")

info("", "")
info("*** SETTLEMENT OF THE OBSTRUCTION, BY ALGEBRA ***", "")
info("  R-LENS:", "dissolves.  Phi~+Psi~ = 2 Phi~ identically (D4/E1).  No condition on mu_s.")
info("  R-SCREEN:", "EVADED, and the prompt's intuition is CORRECT but for a subtler reason. "
                    "The scalar's own gradient s is bounded in (0,1/2) and has contrast ~1.1 "
                    "between 1 AU and the galaxy -- so s ALONE does not carry the contrast. "
                    "But s(y) is a strict BIJECTION, so mu_s(s) = k y(s)/s = k s/(1-2s) is an "
                    "exact re-encoding of y: the entire 1e7-8 dynamic range lives in the "
                    "approach to the pole.  Eating |grad varphi| IS eating the total field.")
info("  => THE ONE-FREE-FUNCTION OBSTRUCTION DOES NOT BIND MECHANISM A.",
     "The two masters are served by two DIFFERENT structures: lensing by the disformal vector, "
     "screening by mu_s.  There is no competition for the same free function.")

# =====================================================================================
head("PART F -- THE KERNEL FORK.  Is the OPERATIVE MS08 kernel realisable in this class?")
# =====================================================================================
r"""
Realisability condition for a two-potential conformal scalar, derived above:
     mu_s(s) s = k y  requires  y to be a single-valued function of s,
i.e. s(y) = varphi'(y)/a0 must be INJECTIVE.  s is continuous with s(0)=0, so injective
<=> strictly monotone increasing.  This is a hard constraint on the interpolation function,
and it is INDEPENDENT of everything else.
"""
u = sp.symbols("u", positive=True)
# MS08 / Route A:  nu(y) = 1/(1-exp(-sqrt y)) ;  s = y (nu-1) = u^2/(e^u - 1),  u = sqrt y
s_ms08 = u ** 2 / (sp.exp(u) - 1)
check(sp.simplify(sp.limit(s_ms08, u, 0)) == 0 and sp.simplify(sp.limit(s_ms08, u, sp.oo)) == 0,
      "F1  MS08: s(y) -> 0 at BOTH ends (y->0 and y->inf).  The anomalous force genuinely "
      "SWITCHES OFF in the Newtonian regime -- which is why the kernel was adopted.")

ds_du = sp.simplify(sp.diff(s_ms08, u))
crit = sp.nsolve(sp.numer(sp.together(ds_du)), u, 1.6)
s_max = float(s_ms08.subs(u, crit))
info("F2  MS08 interior maximum:", f"u* = {float(crit):.6f} (y* = {float(crit)**2:.6f}), "
                                  f"s_max = {s_max:.6f}")
check(s_max > 0,
      "F2  *** MS08's s(y) IS NON-MONOTONE: it rises to a maximum and falls back to zero. "
      "Therefore y is a DOUBLE-VALUED function of s, and NO single-valued mu_s(s) exists. ***")

# explicit two-root demonstration
uu = np.linspace(1e-4, 40, 400000)
ss = uu ** 2 / (np.expm1(uu))
target = 0.5 * s_max
roots = np.where(np.diff(np.sign(ss - target)))[0]
info("F3  explicit degeneracy:",
     f"s = {target:.6f} is attained at y = {uu[roots[0]]**2:.6e} AND y = {uu[roots[-1]]**2:.6e} "
     f"-- a factor {(uu[roots[-1]]/uu[roots[0]])**2:.3e} apart in the total field")
check(len(roots) >= 2,
      "F3  two distinct total fields give the SAME scalar gradient => mu_s would need two values")

# F4 -- the escape: a linear G-renormalising piece.  s -> kappa_s y + s_MS08(y).
#      monotone iff kappa_s >= -min(ds/dy).
ds_dy_ms08 = sp.simplify(ds_du / (2 * u))          # ds/dy = (ds/du)(du/dy), du/dy = 1/(2u)
f_ds = sp.lambdify(u, ds_dy_ms08, "numpy")
uu2 = np.linspace(1e-3, 60, 600000)
vals = f_ds(uu2)
kappa_min = -np.min(vals)
u_at = uu2[np.argmin(vals)]
info("F4  THE ESCAPE (stated in the framework's favour):",
     "s(y) may be shifted by a linear piece kappa_s * y, which is a pure renormalisation of "
     "Newton's constant G_N = G(1+kappa_s) and is locally unobservable in dynamics.")
info("    minimum of ds/dy for MS08:",
     f"{np.min(vals):.6e} at y = {u_at**2:.4f}  =>  REQUIRED kappa_s >= {kappa_min:.6f}")
check(0.001 < kappa_min < 1.0,
      "F4  *** MS08 IS REALISABLE AFTER ALL, but only if the scalar carries a fixed fraction "
      f"kappa_s >= {kappa_min:.4f} ({100*kappa_min/(1+kappa_min):.2f}% of the total force) "
      "EVERYWHERE, absorbed into G_N. ***")

# F5 -- and that fraction is Cassini-constrained IF the coupling is conformal-only
gamma_bound = 2.3e-5     # Bertotti-Iess-Tortora 2003, |gamma-1| < 2.3e-5
kappa_cassini = gamma_bound / 2.0
info("F5  in the CONFORMAL-ONLY case light misses the scalar, so a force fraction kappa_s "
     "shows up as |gamma_PPN - 1| ~ kappa_s:",
     f"Cassini allows kappa_s < {kappa_cassini:.3e}; MS08 needs {kappa_min:.4f} "
     f"= {kappa_min/kappa_cassini:.3e}x over")
check(kappa_min / kappa_cassini > 1e3,
      "F5  conformal-only + MS08 is excluded by Cassini by "
      f"{kappa_min/kappa_cassini:.2e}x -- but this is MOOT, since conformal-only is already "
      "dead by D6.  With the disformal vector, gamma_PPN = 1 and kappa_s is unconstrained here.")

# F6 -- the a0-line needs no such patch (proved at E6; re-checked at high precision)
check(all(_ds(v) > 0 for v in [1e-8, 1e-4, 1e-2, 1.0, 1e2, 1e6, 1e10, 1e14]),
      "F6  by contrast the a0-line needs kappa_s = 0 EXACTLY: its s(y) is already monotone "
      "(E6's 1/4 > 0 proof), verified to y = 1e14 at 60 digits")

info("", "")
info("*** THE FORK, STATED HONESTLY ***", "")
info("  a0-line (this task's kernel):",
     "natively realisable as a TeVeS scalar, mu_s = k s/(1-2s).  Price: varphi' saturates at "
     "a0/2 and NEVER turns off -> the alpha=1 ephemeris liability (PART G).")
info("  MS08 (the operative DR4 kernel):",
     f"screens the solar system perfectly, but is realisable only with kappa_s >= {kappa_min:.4f} "
     "of the force carried by the scalar at all radii (a G-renormalisation).  Not free, not fatal.")
info("  GENERAL STATEMENT (proved above, worth keeping):",
     "for a TeVeS-type scalar, varphi'(g_N) must be strictly monotone increasing.  So the "
     "anomalous force can saturate or grow, but it can never DECAY -- unless a linear "
     "G-renormalising piece is added to hold monotonicity.  Screening is not free in this class.")

# =====================================================================================
head("PART G -- SOLAR SYSTEM.  Both kernels, both footings, vs Sereno & Jetzer 2006")
# =====================================================================================
print()
for f, a0 in A0.items():
    y_1au = y_of_r_sun(AU, a0)
    y_mars = y_of_r_sun(2.27939e11, a0)
    # a0-line
    dphi_line_e = a0 * float(s_hi(y_1au))
    dphi_line_m = a0 * float(s_hi(y_mars))
    # MS08
    def s_ms(yv):
        uu_ = np.sqrt(yv)
        return uu_ ** 2 / np.expm1(uu_) if uu_ < 700 else 0.0
    dphi_ms_e = a0 * s_ms(y_1au)
    dphi_ms_m = a0 * s_ms(y_mars)
    info(f"{f:9s} a0-line  varphi' at Earth = {dphi_line_e:.5e} m/s^2",
         f"= {dphi_line_e/(a0/2):.8f} x (a0/2);  vs SJ06 Earth bound {SJ_BOUND['Earth']:.3e} "
         f"=>  {dphi_line_e/SJ_BOUND['Earth']:.1f}x OVER")
    info(f"{'':9s} a0-line  varphi' at Mars  = {dphi_line_m:.5e} m/s^2",
         f"vs SJ06 Mars bound {SJ_BOUND['Mars']:.3e}  =>  {dphi_line_m/SJ_BOUND['Mars']:.1f}x OVER")
    info(f"{'':9s} MS08     varphi' at Earth = {dphi_ms_e:.5e} m/s^2",
         f"=>  {dphi_ms_e/SJ_BOUND['Earth']:.3e}x the bound  (utterly screened)")
    check(1000 < dphi_line_e / SJ_BOUND["Earth"] < 2000,
          f"G1[{f}] the a0-line's TeVeS scalar reproduces the banked alpha=1 liability exactly: "
          f"{dphi_line_e/SJ_BOUND['Earth']:.0f}x the Earth bound")
    check(dphi_ms_e / SJ_BOUND["Earth"] < 1e-30,
          f"G2[{f}] MS08's scalar gradient at 1 AU is {dphi_ms_e:.2e} m/s^2 -- "
          "screened to machine zero")

info("", "")
info("*** THE RESTATEMENT THIS RUN ADDS ***",
     "In TeVeS language the alpha=1 liability IS the simple pole of mu_s at s=1/2.  The pole is "
     "not a defect of the realisation; it is what makes the a0-line realisable at all.  The "
     "liability and the realisability are the SAME algebraic fact.")

# =====================================================================================
head("PART H -- controls, and things that would have made the above wrong")
# =====================================================================================
# H1 -- negative control: a kernel with the WRONG deep limit must NOT give coefficient 1
def nu_wrong(yv):
    return np.sqrt(1 + 4.0 / yv)      # deep limit g = 2 sqrt(a0 g_b): coefficient should be 2


rr = 300.0 * rMc
coef_wrong = rho_eff_num_kernel(rr, MGAL, a0c, nu_wrong) / (
    np.sqrt(G_ * MGAL * a0c) / (4 * np.pi * G_ * rr ** 2))
check(abs(coef_wrong - 2.0) < 1e-3,
      "H1  NEGATIVE CONTROL: a kernel with deep limit g = 2 sqrt(a0 g_b) gives coefficient 2, "
      "not 1 -- so B2's '1' is a real measurement of the kernel, not a tautology of the algebra",
      f"coefficient = {coef_wrong:.6f}")

# H2 -- negative control on the lensing algebra: a DIFFERENT disformal sign must break D4
gd_tt_bad = sp.simplify(weak(sp.exp(-2 * phi_e) * (gtt + UU_tt) - sp.exp(-2 * phi_e) * UU_tt))
Phi_bad = sp.simplify(sp.expand(-(gd_tt_bad + 1) / 2 / eps))
check(sp.simplify(Phi_bad - (Phi + ph)) != 0,
      "H2  NEGATIVE CONTROL: replacing e^{+2phi} by e^{-2phi} in the U U term destroys "
      "Phi~ = Phi + varphi -- so D3 is testing the structure, not passing vacuously",
      f"broken Phi~ = {Phi_bad}")

# H3 -- control that rho_eff is positive everywhere (no phantom voids for this kernel)
ok_pos = all(rho_eff_closed(m * rMc, MGAL, a0c) > 0 for m in np.logspace(-2, 3, 60))
check(ok_pos, "H3  rho_eff > 0 at all radii for the a0-line (no negative phantom density)")

# H4 -- control: the total enclosed phantom mass diverges logarithmically? No -- linearly in r
Mph = sp.simplify(sp.integrate(4 * sp.pi * r ** 2 * rho_eff.subs(GM, Gs * Mb), r))
info("H4  enclosed phantom mass M_ph(<r) =", f"{sp.simplify(Mph)}")
check(sp.simplify(sp.limit(sp.diff(Mph, r) / r ** 0, r, sp.oo)
                  - sp.sqrt(Mb * a0s / Gs)) == 0,
      "H4  dM_ph/dr -> sqrt(M_b a0/G) = const, so M_ph grows LINEARLY in r "
      "(the flat-rotation-curve mass profile)")

# H5 -- the one place a sign error would flip the verdict: check varphi' > 0 (outward-adding)
check(all(float(s_of_y.subs(y, v)) > 0 for v in [1e-8, 1.0, 1e8]),
      "H5  varphi' > 0 everywhere: the scalar force is ATTRACTIVE and ADDS to Newtonian "
      "(a sign error here would have inverted PART G)")

# =====================================================================================
head("VERDICT")
# =====================================================================================
rows = [
    ("1. AQUAL action for Carl's mu, closed form F(z)", "DONE",
     "F(z) = sqrt(z)sqrt(1+4z)/2 + asinh(2 sqrt z)/4 - sqrt z;  F -> (2/3)z^{3/2} deep"),
    ("2. rho_eff scaling", "1/r^2 EXACT (slope -> -2)", "isothermal, as sf36"),
    ("2. rho_eff COEFFICIENT", "EXACTLY 1.000000", "rho_eff = sqrt(G M_b a0)/(4 pi G r^2) x (1+y)^{-1/2}"),
    ("   is the coefficient off by a pure number?", "NO", "the pure number is 1"),
    ("   is it dynamical or an initial condition?", "DYNAMICAL AND UNIQUE",
     "elliptic + convex => zero free data; stronger than an attractor"),
    ("3a. R-LENS, pure conformal", "DEAD", f"{worst_sig:.0f} sigma; Phi~+Psi~ = Phi+Psi identically"),
    ("3b. R-LENS, disformal (TeVeS/AeST)", "AUTOMATIC", "Phi~+Psi~ = 2 Phi~ for ANY free function"),
    ("   sf34's p_r + 2 p_t = 0, deep limit", "SATISFIED EXACTLY", "P ~ w^{3/2} is the unique zero"),
    ("   sf34's eps at 0.5-3 r_M, full kernel", f">= {np.log10(worst_head):.2f} orders of headroom",
     "eps = 1.7e-8 .. 3.2e-7 vs tolerance 0.0489"),
    ("3c. R-SCREEN", "EVADED", "mu_s = k s/(1-2s); s bounded in (0,1/2) but mu_s carries the "
                               "full ~1e8 total-field contrast"),
    ("3d. the one-free-function obstruction", "DOES NOT BIND",
     "two masters, two structures: vector for lensing, mu_s for screening"),
    ("4. the price, a0-line kernel", "alpha=1 ephemeris liability",
     "varphi' -> a0/2 = pole of mu_s at s=1/2; ~1279x / ~1544x the SJ06 Earth bound"),
    ("5. the price, MS08 kernel", f"kappa_s >= {kappa_min:.4f} G-renormalisation",
     "s(y) non-monotone => not natively realisable"),
    ("6. does this replace the DBI condensate?", "NO",
     "rho_eff is phantom: no energy, cannot be Omega_dm.  Mechanism A is a SECOND sector."),
]
w = max(len(a) for a, _, _ in rows)
for a, b, c in rows:
    print(f"  {a:<{w}s}  {b:<34s}  {c}")

head("WHAT THIS RUN COULD NOT DETERMINE (first-class, not an afterthought)")
for t_ in [
    "1. THE VECTOR'S OWN STRESS.  D4 gives Phi~+Psi~ = 2 Phi~ only if Psi_E = Phi_E in the "
    "Einstein frame.  I bounded the AQUAL SCALAR's contribution to the slip (D9, <=3.2e-7) but "
    "did NOT compute the aether vector's.  I took gamma_PPN = 1 from the framework's banked AeST "
    "result.  If the vector's anisotropic stress is not negligible, D4 weakens.",
    "2. WHETHER k IS FREE.  mu_s(s) = k s/(1-2s) carries a normalisation k that I never pinned. "
    "In TeVeS k also fixes G_N/G and enters the cosmological background.  Everything above is "
    "k-independent because every claim is a RATIO -- but the theory is not specified until k is.",
    "3. NON-SPHERICAL / EXTERNAL-FIELD CASE.  E2-E9's bijection argument is a one-body spherical "
    "statement.  With an external field the scalar equation is genuinely vectorial, "
    "|grad phi_int + grad phi_ext|, and I did not check that the bijection survives.  The EFE "
    "targets (Amendment 10's 1.1614-1.1814 / 1.1917-1.2267 band) were NOT recomputed here.",
    "4. THE COSMOLOGICAL SECTOR.  Mechanism A says nothing about Omega_dm.  rho_eff is phantom, "
    "so the DBI condensate is still doing all the CMB work, and whether the two sectors coexist "
    "without double-counting the galactic mass is untested here.",
    "5. WHETHER THE a0-LINE SURVIVES ITS OWN SOLAR-SYSTEM PRICE.  PART G reproduces the banked "
    "1279x/1541x liability; it does not resolve it.  This run makes the liability sharper "
    "(it is the pole of mu_s), not smaller.",
    "6. QUMOND-TYPE COUPLING was not worked out.  If the free function eats |grad Phi_N| "
    "(the BARYONIC field, contrast 6e7) instead of |grad phi|, F1-F6's realisability question "
    "evaporates and MS08 needs no kappa_s.  But that class is bimetric, not conformal-scalar, "
    "and its relativistic completion is a different problem.",
]:
    print("  * " + t_)

print()
print("=" * 100)
if FAIL:
    print(f"FAILED {len(FAIL)}/{NCHK[0]}:")
    for f_ in FAIL:
        print("   -", f_)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED.")
sys.exit(0)
