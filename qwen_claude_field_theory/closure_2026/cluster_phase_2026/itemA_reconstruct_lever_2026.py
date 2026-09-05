#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
itemA_reconstruct_lever_2026.py
===============================
ITEM A of the cluster-phase workflow: RECONSTRUCT THE |Phi| HELMHOLTZ LEVER EXACTLY, re-derive every
baseline number the cluster no-go paper (CLUSTER_RESIDUAL_DENSITY_NOGO.md, Sec. 6) quotes, state
precisely what "the Helmholtz oscillation phase" is, and resolve the mu^-1 fork (1 Mpc / 22 Mpc /
4392 Mpc).  Every number below is computed here (checks that can fail), with mutation controls.

--------------------------------------------------------------------------------------------------
THE EQUATION AS ACTUALLY USED (reviews/aest_phi_cluster/*.py, Durakovic-Skordis 2024 Eq 2.40)
--------------------------------------------------------------------------------------------------
        (1/r^2) d/dr[ r^2 M(x) Phi' ] + mu^2 Phi = 4 pi G rho_b(r),     x = |Phi'|/a0
        M(x) = (sqrt(1+4x) - 1)/(sqrt(1+4x) + 1)        (M -> x deep MOND, M -> 1 Newton)
The +mu^2 Phi term is the AeST scalar mass term.  Its sign makes the operator HELMHOLTZ (oscillatory
homogeneous solutions [C1 cos(mu r) + C2 sin(mu r)]/r), not Yukawa.  Pure AQUAL is shift-invariant
(Phi -> Phi + C); the mass term breaks that, so the absolute level of Phi is physical and acts as a
phantom source rho_ph = -mu^2 Phi/(4 pi G) (positive where Phi < 0).

Canonical-momentum form (smooth through the |Phi'| = 0 nodes):
        P := r^2 M(x) Phi'      Phi' = a0 x sgn(P),   x M(x) = |P|/(a0 r^2)  =>  x = q + sqrt(q)
        P' = r^2 ( -mu^2 Phi + 4 pi G rho_b )
At mu = 0: P = G M_b(r) exactly => g = g_N + sqrt(a0 g_N) (DS24's interpolation, NOT the framework's
own a0-line g^2 = g_N^2 + a0 g_N; the difference is a mutation control below).

--------------------------------------------------------------------------------------------------
WHAT "THE PHASE" IS, PRECISELY
--------------------------------------------------------------------------------------------------
The march starts at r0 = 20 kpc with TWO data:  P(r0) = G M_b(r0)  (regularity: no phantom mass
inside r0 -- fixed) and  Phi(r0) = -a0 x0 r0 + dPhi0  (the ADDITIVE LEVEL of the potential -- FREE).
dPhi0 is the single surviving Helmholtz integration constant.  The core phantom mass is
        M_ph(<R) = P(R)/G - M_b(R) = -(mu^2/G) INT_0^R Phi r^2 dr
so the core amplitude is set DIRECTLY by the level of Phi over the core, i.e. by dPhi0 (sensitivity
dM_ph/d(dPhi0) ~ -mu^2 R^3/(3G), verified numerically).  "Phase" enters when one tries to FIX dPhi0
by an OUTER datum: the map dPhi0 -> Phi(r_match) is oscillatory (mu r_ta = 8.5 rad ~ 1.35 periods),
so a given asymptotic value chi_inf is reached by several dPhi0 (several oscillation branches), each
with a different core phantom.  Which branch = the phase.

--------------------------------------------------------------------------------------------------
THE mu^-1 FORK
--------------------------------------------------------------------------------------------------
  1 Mpc    : DS24/BS24 phenomenological AeST mass ("CMB-pinned", BS24 Eq 3.25) -- what the 28-100%
             solve used.  This is AeST's free mu, NOT a framework output.
  22 Mpc   : BS24 Fig.1 at K_B = 0.5 -- quoted in the no-go Sec. 3 loophole test only.
  4392 Mpc : THE_COMPLETION v9's OWN Q-sector Helmholtz mass (single-scale hypothesis, item 12;
             mi_condensate_vacuum_energy_a0_2026.py; nbody stages 2/4 call the Mpc-scale mu
             do-not-cite for the completion's Q-sector).
The lever scales as (mu R)^2; all three are run below on the identical solver.
"""
import json
import os
import sys
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

FAIL = []
NCHK = [0]
OUT = {}


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


# ----------------------------------------------------------------------------- constants (SI)
c = 2.99792458e8
G_N = 6.674e-11
Msun = 1.989e30
kpc = 3.0857e19
Mpc = 3.0857e22
AU = 1.495978707e11
A0 = {"canon": 9.36e-11, "alt": 1.1279e-10}
H0 = 67.4e3 / Mpc
OL, Om = 0.685, 0.315
Lam = 3.0 * OL * H0 ** 2 / c ** 2
rho_crit0 = 3.0 * H0 ** 2 / (8.0 * np.pi * G_N)
M_RESID_CORE = 1.5e14          # Msun, the core (<420 kpc) residual the no-go paper closes against
R_CORE = 420 * kpc

print(__doc__)

# =================================================================================================
print("=" * 100)
print("PART A -- the equation, symbolically (closed-form inverse, limits, shift-symmetry breaking, kernel)")
print("=" * 100)
x, q, C, mu_s = sp.symbols("x q C mu", positive=True)
Mx = (sp.sqrt(1 + 4 * x) - 1) / (sp.sqrt(1 + 4 * x) + 1)
xsol = q + sp.sqrt(q)
check(sp.simplify(xsol * Mx.subs(x, xsol) - q) == 0, "A1  x M(x) = q is solved exactly by x = q + sqrt(q)")
check(sp.limit(Mx / x, x, 0) == 1 and sp.limit(Mx, x, sp.oo) == 1,
      "A2  M(x) -> x (deep MOND) and M(x) -> 1 (Newton)")
# the mu = 0 force law implied by x = q + sqrt(q):  g = a0 x = g_N + sqrt(a0 g_N)
gN, a0s = sp.symbols("g_N a0", positive=True)
g_ds24 = a0s * xsol.subs(q, gN / a0s)
check(sp.simplify(g_ds24 - (gN + sp.sqrt(a0s * gN))) == 0,
      "A3  DS24 kernel at mu=0: g = g_N + sqrt(a0 g_N)  (deep MOND sqrt(a0 g_N), Newton g_N)")
g_fw = sp.sqrt(gN ** 2 + a0s * gN)
ratio_at_a0 = sp.simplify((g_ds24 / g_fw).subs(gN, a0s))
check(abs(float(ratio_at_a0) - np.sqrt(2)) < 1e-12,
      f"A4  DS24 kernel vs the framework's OWN a0-line g^2=g_N^2+a0 g_N: at g_N=a0 the ratio is "
      f"{float(ratio_at_a0):.4f} (2 vs sqrt2) -- NOT the same interpolation; mutation control in Part H")
# shift symmetry: Phi -> Phi + C changes the equation by mu^2 C (broken); mu = 0 restores it
Phi_f = sp.Function("Phi")
r = sp.symbols("r", positive=True)
lhs = lambda P: sp.diff(r ** 2 * Mx.subs(x, sp.Abs(sp.diff(P, r)) / a0s) * sp.diff(P, r), r) / r ** 2 + mu_s ** 2 * P
delta = sp.simplify(lhs(Phi_f(r) + C) - lhs(Phi_f(r)))
check(sp.simplify(delta - mu_s ** 2 * C) == 0,
      "A5  Phi -> Phi + C shifts the equation by exactly mu^2 C: the level of Phi is physical iff mu != 0")
# homogeneous Newtonian-regime solutions are oscillatory (Helmholtz), not Yukawa
rr = sp.symbols("r", positive=True)
for name, f in [("cos", sp.cos(mu_s * rr) / rr), ("sin", sp.sin(mu_s * rr) / rr)]:
    res = sp.simplify(sp.diff(rr ** 2 * sp.diff(f, rr), rr) / rr ** 2 + mu_s ** 2 * f)
    check(res == 0, f"A6  [{name}(mu r)]/r is an exact homogeneous solution of the M=1 (Newtonian) operator")
res_yuk = sp.simplify(sp.diff(rr ** 2 * sp.diff(sp.exp(-mu_s * rr) / rr, rr), rr) / rr ** 2 + mu_s ** 2 * sp.exp(-mu_s * rr) / rr)
check(res_yuk != 0, "A7  e^{-mu r}/r is NOT a solution (the +mu^2 sign is Helmholtz, not Yukawa)")


# =================================================================================================
# numerics: the identical solver as reviews/aest_phi_cluster/aest_phi_cluster_solve.py (vectorised)
# =================================================================================================
def xinv_ds24(qv):
    qv = np.abs(np.asarray(qv, float))
    return qv + np.sqrt(qv)


def xinv_fw(qv):
    """framework a0-line in AQUAL form: mu_M(x) = (sqrt(1+4x^2)-1)/(2x); x mu_M(x) = q  =>  x = sqrt(q^2+q)."""
    qv = np.abs(np.asarray(qv, float))
    return np.sqrt(qv ** 2 + qv)


def make_baryons_A2029(M500, R500, beta=0.67, rc_frac=0.12, fgas=0.13, fstar=0.012, a_bcg_kpc=30.0):
    rc = rc_frac * R500
    a_bcg = a_bcg_kpc * kpc
    M_bcg = fstar * M500 * Msun
    M_gas_tot = fgas * M500 * Msun

    def rho_gas_un(rv):
        return (1.0 + (rv / rc) ** 2) ** (-1.5 * beta)

    rgrid = np.geomspace(1e-3 * rc, R500, 200000)
    norm = np.trapz(4 * np.pi * rgrid ** 2 * rho_gas_un(rgrid), rgrid)
    rho_g0 = M_gas_tot / norm
    rtab = np.geomspace(1e-4 * rc, 80 * Mpc, 8000)
    integ = 4 * np.pi * rtab ** 2 * rho_g0 * rho_gas_un(rtab)
    Mgas_tab = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(rtab))])

    def Menc(rv):
        return np.interp(rv, rtab, Mgas_tab) + M_bcg * (rv ** 2 / (rv + a_bcg) ** 2)

    def rho_b(rv):
        return rho_g0 * rho_gas_un(rv) + M_bcg * a_bcg / (2 * np.pi) / (rv * (rv + a_bcg) ** 3)

    return rho_b, Menc


class Solver:
    def __init__(self, rho_b, Menc, a0, mu_t2, xinv=xinv_ds24, sign=+1.0):
        self.rho_b, self.Menc, self.a0, self.mu_t2, self.xinv, self.sign = rho_b, Menc, a0, mu_t2, xinv, sign

    def g_ref(self, rv):
        """the mu = 0 (pure interpolated-MOND) force for the same kernel."""
        rv = np.atleast_1d(rv)
        return self.a0 * self.xinv(G_N * self.Menc(rv) / (self.a0 * rv ** 2))

    def phi0_natural(self, r0):
        x0 = self.xinv(G_N * self.Menc(r0) / (self.a0 * r0 ** 2))
        return -self.a0 * x0 * r0

    def march(self, r0, r1, dPhi0=0.0, n=6000, ms=3000, t_eval=None):
        P0 = G_N * self.Menc(r0)
        Phi0 = self.phi0_natural(r0) + dPhi0
        a0, mu_t2, xinv, rho_b, sgn = self.a0, self.mu_t2, self.xinv, self.rho_b, self.sign

        def f(rv, y):
            xx = xinv(abs(y[1]) / (a0 * rv ** 2))
            return [a0 * xx * np.sign(y[1]), rv ** 2 * (-sgn * mu_t2 * y[0] + 4 * np.pi * G_N * rho_b(rv))]

        te = np.linspace(r0, r1, n) if t_eval is None else t_eval
        sol = solve_ivp(f, [r0, r1], [Phi0, P0], t_eval=te, rtol=1e-11, atol=1e-16,
                        method="DOP853", max_step=(r1 - r0) / ms)
        rv, Phi, P = sol.t, sol.y[0], sol.y[1]
        g = a0 * xinv(np.abs(P) / (a0 * rv ** 2)) * np.sign(P)
        return rv, Phi, P, g

    def core_phantom(self, rv, P, R=R_CORE):
        i = np.argmin(np.abs(rv - R))
        return (P[i] / G_N - self.Menc(rv[i])) / Msun          # Msun

    def eta(self, rv, g, R):
        i = np.argmin(np.abs(rv - R))
        return g[i] / self.g_ref(rv[i])[0]


M500, R500 = 1.0e15, 1.56 * Mpc
r0 = 0.02 * Mpc
rho_b, Menc = make_baryons_A2029(M500, R500)
z = 0.1
rho_crit_z = rho_crit0 * (Om * (1 + z) ** 3 + OL)
Delta_ta = 2.8
r_ta = (3 * M500 * Msun / (4 * np.pi * Delta_ta * rho_crit_z)) ** (1 / 3.)
chi_DE = -(1 / 6.) * Lam * c ** 2 * r_ta ** 2
chi_mean = -(1 / 2.) * (4 * np.pi / 3.) * G_N * (Om * rho_crit_z) * r_ta ** 2
v_c2 = G_N * M500 * Msun / R500


def roots_for_chi(S, chi, r_match, lo=-1.6e13, hi=1.0e13, npts=120):
    """all dPhi0 in [lo,hi] with Phi(r_match) = chi (the oscillation branches)."""
    def Phi_at(d):
        rv, Phi, P, g = S.march(r0, r_match, dPhi0=d, n=3000, ms=1500)
        return Phi[-1]
    grid = np.linspace(lo, hi, npts)
    vals = np.array([Phi_at(d) - chi for d in grid])
    out = []
    for i in range(len(grid) - 1):
        if vals[i] * vals[i + 1] < 0:
            out.append(brentq(lambda d: Phi_at(d) - chi, grid[i], grid[i + 1], xtol=1e8))
    return out, grid, vals


def branch_table(S, roots, r_match, label):
    rows = []
    for d in roots:
        rv, Phi, P, g = S.march(r0, r_match, dPhi0=d)
        rows.append(dict(dPhi0=d, eta_R500=S.eta(rv, g, R500), Mph_core=S.core_phantom(rv, P)))
    print(f"    {label}: {len(roots)} branch(es)")
    for w in rows:
        print(f"      dPhi0={w['dPhi0']:+.3e}  eta(R500)={w['eta_R500']:+.3f}  M_ph(<420kpc)={w['Mph_core']:+.3e} Msun"
              f"  = {100 * w['Mph_core'] / M_RESID_CORE:+.1f}% of the 1.5e14 core residual")
    return rows


def run_footing(a0, inv_mu_Mpc, xinv=xinv_ds24, sign=+1.0, tag="", do_roots=True):
    mu = 1.0 / (inv_mu_Mpc * Mpc)
    S = Solver(rho_b, Menc, a0, mu ** 2, xinv=xinv, sign=sign)
    res = {}
    # validation mu = 0
    S0 = Solver(rho_b, Menc, a0, 0.0, xinv=xinv, sign=sign)
    rv, Phi, P, g = S0.march(r0, 30 * Mpc)
    i = np.argmin(np.abs(rv - R500))
    res["validation_ratio"] = g[i] / S0.g_ref(rv[i])[0]
    res["Mph_core_mu0"] = S0.core_phantom(rv, P)
    # natural (untuned) boundary
    rv, Phi, P, g = S.march(r0, r_ta, dPhi0=0.0)
    res["natural"] = dict(eta_R500=S.eta(rv, g, R500), Mph_core=S.core_phantom(rv, P), Phi_rta=Phi[-1])
    # the core-integral identity M_ph = -(mu^2/G) INT Phi r^2 dr
    ic = np.argmin(np.abs(rv - R_CORE))
    integ = -(mu ** 2 / G_N) * np.trapz(Phi[:ic + 1] * rv[:ic + 1] ** 2, rv[:ic + 1]) / Msun
    inner0 = (G_N * Menc(r0) - G_N * Menc(r0)) / G_N   # P(r0) = G M_b(r0): zero phantom inside r0 by construction
    res["identity_integral"] = integ
    # sensitivity to the level: dM_ph/d(dPhi0)
    rv2, Phi2, P2, g2 = S.march(r0, r_ta, dPhi0=-1e12)
    res["slope_num"] = (S.core_phantom(rv2, P2) - res["natural"]["Mph_core"]) / (-1e12)   # Msun per (m/s)^2
    res["slope_analytic"] = -(mu ** 2) * (R_CORE ** 3 - r0 ** 3) / (3 * G_N) / Msun
    if do_roots:
        roots, grid, vals = roots_for_chi(S, chi_DE, r_ta)
        res["roots_DE"] = branch_table(S, roots, r_ta, f"{tag} chi_inf = chi_DE = {chi_DE:.3e}")
        res["n_sign_changes_map"] = int(np.sum(np.diff(np.sign(np.diff(vals))) != 0))
        rootsm, _, _ = roots_for_chi(S, chi_mean, r_ta)
        res["roots_mean"] = branch_table(S, rootsm, r_ta, f"{tag} chi_inf = chi_mean = {chi_mean:.3e}")
    # the boost branch the paper quotes (~100 %): dPhi0 = -1e13
    rv, Phi, P, g = S.march(r0, r_ta, dPhi0=-1.0e13)
    res["boost_m1e13"] = dict(eta_R500=S.eta(rv, g, R500), Mph_core=S.core_phantom(rv, P), Phi_rta=Phi[-1])
    # dPhi0 needed to land exactly +1.5e14 in the core (the per-cluster tune)
    try:
        f_need = lambda d: S.core_phantom(*[S.march(r0, R_CORE * 1.05, dPhi0=d, n=2000, ms=1000)[k] for k in (0, 2)]) - M_RESID_CORE
        res["dPhi0_for_closure"] = brentq(f_need, -3e13, 0.0, xtol=1e8)
    except ValueError:
        res["dPhi0_for_closure"] = None
    return S, res


# =================================================================================================
print("\n" + "=" * 100)
print("PART B -- BASELINE: 1/mu = 1 Mpc, a0 canonical 9.36e-11 (the no-go paper's Sec. 6 numbers)")
print("=" * 100)
info(f"cluster M500={M500:.0e} Msun, R500={R500/Mpc:.2f} Mpc, beta-model gas + Hernquist BCG; "
     f"M_b(<420kpc)={Menc(R_CORE)/Msun:.3e}, M_b(<R500)={Menc(R500)/Msun:.3e} Msun")
info(f"turnaround r_ta = {r_ta/Mpc:.2f} Mpc (mu r_ta = {r_ta/Mpc:.2f} rad = {r_ta/Mpc/(2*np.pi):.2f} oscillation periods at 1/mu=1 Mpc)")
info(f"chi_DE = -(1/6) Lambda c^2 r_ta^2 = {chi_DE:.3e} (m/s)^2 = {chi_DE/v_c2:+.3f} v_c^2;  chi_mean = {chi_mean:.3e}")
S_can, B = run_footing(A0["canon"], 1.0, tag="[1 Mpc, canon]")
OUT["baseline_1Mpc_canon"] = B
check(abs(B["validation_ratio"] - 1) < 1e-5,
      f"B1  mu=0 march reproduces the analytic interpolated-MOND force at R500: ratio = {B['validation_ratio']:.7f}")
check(abs(B["Mph_core_mu0"]) < 1e-4 * M_RESID_CORE,
      f"B2  MUTATION mu=0: core phantom = {B['Mph_core_mu0']:.2e} Msun (zero; the lever IS the mass term)")
nat = B["natural"]
check(nat["eta_R500"] < 0 and abs(nat["eta_R500"] + 1.544) < 0.03,
      f"B3  NATURAL untuned boundary (dPhi0=0): eta(R500) = {nat['eta_R500']:+.3f} -- a DEFICIT (paper: -1.54)",
      f"core phantom nevertheless +{nat['Mph_core']:.3e} Msun = {100*nat['Mph_core']/M_RESID_CORE:.0f}% (paper: +4.6e13)")
check(abs(B["identity_integral"] / nat["Mph_core"] - 1) < 0.02,
      f"B4  IDENTITY M_ph(<420kpc) = -(mu^2/G) INT Phi r^2 dr: integral {B['identity_integral']:.3e} vs "
      f"P/G - M_b {nat['Mph_core']:.3e} (ratio {B['identity_integral']/nat['Mph_core']:.4f})",
      "=> the core amplitude is literally the integrated LEVEL of Phi over the core")
check(abs(B["slope_num"] / B["slope_analytic"] - 1) < 0.35,
      f"B5  dM_ph/d(dPhi0): numerical {B['slope_num']:.3e} vs analytic -mu^2 R^3/(3G) = {B['slope_analytic']:.3e} Msun per (m/s)^2 "
      f"(ratio {B['slope_num']/B['slope_analytic']:.3f}; the excess is the MOND nonlinearity feeding the level back into g)")
rootsDE = B["roots_DE"]
etas = [w["eta_R500"] for w in rootsDE]
check(len(rootsDE) >= 3 and min(etas) < 0 < max(etas),
      f"B6  MULTIVALUED: chi_DE is reached on {len(rootsDE)} branches with eta(R500) in [{min(etas):+.2f}, {max(etas):+.2f}] "
      f"(paper: 5 roots, -2.95..+3.90) -- boosts AND deficits at the identical asymptotic value")
w_min = min(rootsDE, key=lambda w: abs(w["dPhi0"]))
check(abs(w_min["Mph_core"] / 4.187e13 - 1) < 0.05 and abs(w_min["eta_R500"] + 1.71) < 0.05,
      f"B7  the min-|dPhi0| chi_DE branch: M_ph(core) = {w_min['Mph_core']:+.3e} Msun = "
      f"{100*w_min['Mph_core']/M_RESID_CORE:.1f}% of the residual, eta(R500) = {w_min['eta_R500']:+.3f}  (paper: +4.2e13 = 28%, -1.71)")
bst = B["boost_m1e13"]
check(abs(bst["Mph_core"] / 1.458e14 - 1) < 0.05,
      f"B8  boost branch dPhi0 = -1e13: M_ph(core) = {bst['Mph_core']:+.3e} Msun = {100*bst['Mph_core']/M_RESID_CORE:.0f}% "
      f"(paper: +1.5e14 ~ 100%), eta(R500) = {bst['eta_R500']:+.2f}, Phi(r_ta) = {bst['Phi_rta']:+.3e}")
naive = abs(S_can.phi0_natural(200 * kpc)) / c ** 2 * Menc(R_CORE) / Msun
OUT["naive_phantom_Msun"] = naive
check(w_min["Mph_core"] / naive > 1e5,
      f"B9  vs the naive O(1) local |Phi|/c^2 coupling ({naive:.2e} Msun): the Helmholtz phantom is "
      f"{w_min['Mph_core']/naive:.2e}x larger (paper: ~1.7e5x)")
info(f"B10 the dPhi0 that lands exactly +1.5e14 in the core: {B['dPhi0_for_closure']:+.3e} (m/s)^2 = "
     f"{B['dPhi0_for_closure']/v_c2:+.1f} v_c^2 = {B['dPhi0_for_closure']/c**2:+.2e} c^2  "
     f"(the earlier point-mass corpus needed -4.8e13 on a different profile; same order)")
info(f"B11 for scale: the natural baryonic level at r0 is Phi(r0) = {S_can.phi0_natural(r0):+.3e}; the closure needs a level "
     f"{abs(B['dPhi0_for_closure']/S_can.phi0_natural(r0)):.0f}x deeper than the baryonic well itself -- a homogeneous "
     f"Helmholtz mode of that amplitude, not a response to the baryons")

# =================================================================================================
print("\n" + "=" * 100)
print("PART C -- the matching-radius (phase) dependence: eta(R500) on the min-|dPhi0| chi_DE branch vs r_match")
print("=" * 100)
Cres = []
for frac in [3.0, 4.0, 5.0, 5.44, 6.0, 7.0]:
    rm = frac * R500
    chi_rm = -(1 / 6.) * Lam * c ** 2 * rm ** 2
    roots, _, _ = roots_for_chi(S_can, chi_rm, rm, npts=80)
    if not roots:
        print(f"    r_match/R500={frac:5.2f}: no root"); continue
    d = min(roots, key=abs)
    rv, Phi, P, g = S_can.march(r0, rm, dPhi0=d)
    Cres.append(dict(frac=frac, mu_rm=rm / Mpc, eta=S_can.eta(rv, g, R500), Mph=S_can.core_phantom(rv, P), nroots=len(roots)))
    print(f"    r_match/R500={frac:5.2f}  mu r_match={rm/Mpc:5.2f}  eta(R500)={Cres[-1]['eta']:+.3f}  "
          f"M_ph(core)={Cres[-1]['Mph']:+.3e}  ({len(roots)} branches)")
OUT["rmatch_sweep"] = Cres
e_list = [w["eta"] for w in Cres]
check(max(e_list) - min(e_list) > 3.0,
      f"C1  eta(R500) at the SAME cosmological prescription swings over [{min(e_list):+.2f}, {max(e_list):+.2f}] "
      f"with the matching-radius convention (paper: +2.08 -> +7.37): the amplitude is set by the phase mu r_match, not by |chi|")

# =================================================================================================
print("\n" + "=" * 100)
print("PART D -- GALAXY: natural-boundary RAR shift, and the LEAK of the universally-imposed cluster level")
print("=" * 100)
Mgal, Rd = 6e10 * Msun, 3.0 * kpc


def rho_gal(rv):
    return Mgal / (8 * np.pi * Rd ** 3) * np.exp(-rv / Rd)


def Menc_gal(rv):
    xq = np.asarray(rv) / Rd
    return Mgal * (1 - (1 + xq + 0.5 * xq ** 2) * np.exp(-xq))


r0g, r1g = 0.3 * kpc, 500 * kpc
te_g = np.linspace(r0g, 300 * kpc, 12000)


def galaxy_shift(a0, inv_mu_Mpc, dphi0=0.0, xinv=xinv_ds24):
    mu = 1.0 / (inv_mu_Mpc * Mpc)
    Son = Solver(rho_gal, Menc_gal, a0, mu ** 2, xinv=xinv)
    Soff = Solver(rho_gal, Menc_gal, a0, 0.0, xinv=xinv)
    _, _, _, gon = Son.march(r0g, r1g, dPhi0=dphi0, t_eval=te_g, ms=4000)
    _, _, _, goff = Soff.march(r0g, r1g, dPhi0=0.0, t_eval=te_g, ms=4000)
    dl = []
    for rk in [5, 8, 10, 15, 20, 25, 30]:
        j = np.argmin(np.abs(te_g - rk * kpc))
        dl.append(np.log10(abs(gon[j])) - np.log10(abs(goff[j])))
    return float(np.max(np.abs(dl)))


gal_nat = galaxy_shift(A0["canon"], 1.0)
gal_leak = galaxy_shift(A0["canon"], 1.0, dphi0=-4.8e13)
gal_leak_own = galaxy_shift(A0["canon"], 1.0, dphi0=B["dPhi0_for_closure"])
OUT["galaxy"] = dict(natural_dex=gal_nat, leak_m4p8e13_dex=gal_leak, leak_own_closure_dex=gal_leak_own)
check(gal_nat < 0.05 and abs(gal_nat / 6.85e-4 - 1) < 0.1,
      f"D1  galaxy natural boundary, same mu: max|dlog10 g| (5-30 kpc) = {gal_nat:.2e} dex (paper: 6.85e-4; veto 0.05) -- SAFE")
check(gal_leak > 0.05 and abs(gal_leak / 0.275 - 1) < 0.1,
      f"D2  the cluster level -4.8e13 imposed UNIVERSALLY on the galaxy: {gal_leak:.3f} dex (paper: 0.275) -- BREAKS the RAR")
info(f"D3  and THIS profile's own closure level ({B['dPhi0_for_closure']:+.2e}) imposed on the galaxy: {gal_leak_own:.3f} dex")
info("D4  why galaxies are safe at the NATURAL level: (mu 30 kpc)^2 = 9e-4 vs (mu R500)^2 = 2.4 -- geometric; a universal "
     "level of 1e13 (m/s)^2 is ~1e3x the disk's own potential, and even (mu r)^2 ~ 1e-3 of that is a ~unity force change")

# =================================================================================================
print("\n" + "=" * 100)
print("PART E -- CASSINI (analytic Helmholtz in the deep-Newtonian regime, 60 digits)")
print("=" * 100)
mp.mp.dps = 60
r_sat = mp.mpf(9.537) * mp.mpf(AU)
GM = mp.mpf(G_N) * mp.mpf(1.989e30)
muH = 1 / mp.mpf(Mpc)
mur = muH * r_sat
frac_cos = abs(mur * mp.sin(mur) + mp.cos(mur) - 1)
frac_sin = abs(GM * (mur * mp.cos(mur) - mp.sin(mur)) / (muH * r_sat ** 2) / (GM / r_sat ** 2))
OUT["cassini"] = dict(frac_cos=float(frac_cos), frac_sin=float(frac_sin))
check(float(frac_sin) < 2.3e-5 and abs(float(frac_sin) / 1.02e-9 - 1) < 0.05,
      f"E1  Saturn fractional anomaly: boundary(sin) family {float(frac_sin):.2e}, Newton-matched(cos) {float(frac_cos):.1e} "
      f"vs |gamma-1| < 2.3e-5 (paper: 1.0e-9) -- SAFE by {2.3e-5/float(frac_sin):.1e}x")

# =================================================================================================
print("\n" + "=" * 100)
print("PART F -- THE mu^-1 FORK on the identical solver: 1 Mpc (DS24) / 22 Mpc (BS24 K_B=0.5) / 4392 Mpc (completion v9)")
print("=" * 100)
fork = {}
for invmu in [22.0, 4392.0]:
    S_f, F = run_footing(A0["canon"], invmu, tag=f"[{invmu:.0f} Mpc, canon]")
    fork[invmu] = F
    n = F["natural"]
    print(f"    1/mu = {invmu:6.0f} Mpc: (mu R500)^2 = {(R500/(invmu*Mpc))**2:.2e}; natural eta(R500) = {n['eta_R500']:+.5f}, "
          f"M_ph(core) = {n['Mph_core']:+.3e} Msun = {100*n['Mph_core']/M_RESID_CORE:.2e}% ; "
          f"chi_DE branches: {len(F['roots_DE'])}; boost branch(-1e13): {F['boost_m1e13']['Mph_core']:+.3e}")
OUT["fork"] = {str(k): v for k, v in fork.items()}
n22, n4392 = fork[22.0]["natural"], fork[4392.0]["natural"]
check(abs(n22["Mph_core"] / nat["Mph_core"] - (1 / 22.0) ** 2) < 0.4 * (1 / 22.0) ** 2,
      f"F1  22 Mpc: natural core phantom {n22['Mph_core']:.2e} Msun = {n22['Mph_core']/nat['Mph_core']:.2e} of the 1-Mpc value "
      f"(expected ~1/22^2 = {1/22**2:.2e}): the lever scales as mu^2 R^2")
check(len(fork[22.0]["roots_DE"]) == 1 and len(fork[4392.0]["roots_DE"]) == 1,
      f"F2  at 22 and 4392 Mpc the map dPhi0 -> Phi(r_ta) is MONOTONE (mu r_ta = {r_ta/22/Mpc:.2f}, {r_ta/4392/Mpc:.4f} rad): "
      "a single branch -- no phase freedom, and no boost either")
check(abs(n4392["Mph_core"]) < 1e-5 * M_RESID_CORE,
      f"F3  4392 Mpc (the completion's OWN Q-sector mass): core phantom {n4392['Mph_core']:.2e} Msun = "
      f"{100*n4392['Mph_core']/M_RESID_CORE:.1e}% of the residual -- the lever is DEAD at the completion's own mu; "
      "the 28-100% result lives ONLY at AeST's phenomenological 1/mu ~ 1 Mpc")
# the level a 4392-Mpc mass would need to reach 1.5e14 in the core (from the exact identity)
lvl4392 = -M_RESID_CORE * Msun * 3 * G_N / ((1 / (4392 * Mpc)) ** 2 * R_CORE ** 3)
info(f"F4  the mean core level a 4392-Mpc mass needs for +1.5e14: Phi_bar = {lvl4392:+.2e} (m/s)^2 = {lvl4392/c**2:+.2e} c^2 "
     f"(|Phi| > c^2: not a weak field -- the completion's mu cannot carry this lever at all)")

# =================================================================================================
print("\n" + "=" * 100)
print("PART G -- ALT a0 FOOTING (1.1279e-10) at 1/mu = 1 Mpc")
print("=" * 100)
S_alt, Galt = run_footing(A0["alt"], 1.0, tag="[1 Mpc, alt]")
OUT["baseline_1Mpc_alt"] = Galt
na = Galt["natural"]
ea = [w["eta_R500"] for w in Galt["roots_DE"]]
wa = min(Galt["roots_DE"], key=lambda w: abs(w["dPhi0"]))
check(na["eta_R500"] < 0,
      f"G1  ALT a0: natural boundary eta(R500) = {na['eta_R500']:+.3f} (deficit), M_ph(core) = {na['Mph_core']:+.3e} Msun "
      f"= {100*na['Mph_core']/M_RESID_CORE:.0f}%")
check(len(Galt["roots_DE"]) >= 3 and min(ea) < 0 < max(ea),
      f"G2  ALT a0: chi_DE branches {len(Galt['roots_DE'])}, eta in [{min(ea):+.2f}, {max(ea):+.2f}]; min-|dPhi0| branch "
      f"M_ph(core) = {wa['Mph_core']:+.3e} ({100*wa['Mph_core']/M_RESID_CORE:.0f}%); boost branch {Galt['boost_m1e13']['Mph_core']:+.3e} "
      f"({100*Galt['boost_m1e13']['Mph_core']/M_RESID_CORE:.0f}%) -- same structure, spread ~{abs(wa['Mph_core']/w_min['Mph_core']-1)*100:.0f}% on the DE branch")
gal_nat_alt = galaxy_shift(A0["alt"], 1.0)
gal_leak_alt = galaxy_shift(A0["alt"], 1.0, dphi0=-4.8e13)
OUT["galaxy_alt"] = dict(natural_dex=gal_nat_alt, leak_dex=gal_leak_alt)
check(gal_nat_alt < 0.05 and gal_leak_alt > 0.05,
      f"G3  ALT a0 galaxy: natural {gal_nat_alt:.2e} dex (safe), universal cluster level {gal_leak_alt:.3f} dex (breaks)")

# =================================================================================================
print("\n" + "=" * 100)
print("PART H -- MUTATION CONTROLS: kernel swap (framework a0-line) and sign flip (Yukawa)")
print("=" * 100)
S_fw, Hfw = run_footing(A0["canon"], 1.0, xinv=xinv_fw, tag="[1 Mpc, canon, FRAMEWORK a0-line kernel]")
OUT["kernel_framework"] = Hfw
nf = Hfw["natural"]
ef = [w["eta_R500"] for w in Hfw["roots_DE"]]
wf = min(Hfw["roots_DE"], key=lambda w: abs(w["dPhi0"]))
check(abs(Hfw["validation_ratio"] - 1) < 1e-5,
      f"H1  framework-kernel solver: mu=0 reproduces g = sqrt(g_N^2 + a0 g_N) at R500 (ratio {Hfw['validation_ratio']:.7f})")
check(nf["eta_R500"] < 0 and len(Hfw["roots_DE"]) >= 3 and min(ef) < 0 < max(ef),
      f"H2  FRAMEWORK KERNEL: natural eta = {nf['eta_R500']:+.3f}, M_ph(core) = {nf['Mph_core']:+.3e} ({100*nf['Mph_core']/M_RESID_CORE:.0f}%); "
      f"chi_DE branches {len(Hfw['roots_DE'])} with eta in [{min(ef):+.2f}, {max(ef):+.2f}]; min-|dPhi0| branch {wf['Mph_core']:+.3e} "
      f"({100*wf['Mph_core']/M_RESID_CORE:.0f}%); boost branch {Hfw['boost_m1e13']['Mph_core']:+.3e} ({100*Hfw['boost_m1e13']['Mph_core']/M_RESID_CORE:.0f}%)",
      "=> the DS24-vs-framework interpolation changes the numbers at the 10-30% level, not the verdict")
S_yuk, Hy = run_footing(A0["canon"], 1.0, sign=-1.0, tag="[1 Mpc, canon, YUKAWA sign -mu^2 Phi]")
OUT["sign_flip_yukawa"] = Hy
ny = Hy["natural"]
check(len(Hy["roots_DE"]) <= 1 and ny["Mph_core"] < 0,
      f"H3  SIGN FLIP (Yukawa -mu^2 Phi): natural core phantom {ny['Mph_core']:+.3e} Msun (NEGATIVE), eta = {ny['eta_R500']:+.3f}, "
      f"chi_DE branches = {len(Hy['roots_DE'])}: no oscillation, no boost -- the boost branches exist ONLY for the Helmholtz sign")

# =================================================================================================
print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
summary = dict(
    equation="(1/r^2)(r^2 M(x) Phi')' + mu^2 Phi = 4 pi G rho_b ; M(x)=(sqrt(1+4x)-1)/(sqrt(1+4x)+1) ; x=|Phi'|/a0 ; canonical P=r^2 M Phi', x=q+sqrt(q)",
    phase_datum="Phi(r0=20 kpc) = -a0 x0 r0 + dPhi0 with P(r0)=G M_b(r0); dPhi0 is the free Helmholtz constant; core phantom = -(mu^2/G) INT Phi r^2 dr; 'phase' = which branch of the oscillatory map dPhi0 -> Phi(r_match) lands the asymptotic chi_inf",
    mu_used_for_28_100pct="1 Mpc (AeST phenomenological, DS24/BS24); NOT the completion's 4392 Mpc",
    natural_eta_R500=nat["eta_R500"], natural_Mph_core=nat["Mph_core"],
    chiDE_min_branch_Mph_core=w_min["Mph_core"], chiDE_min_branch_eta=w_min["eta_R500"],
    chiDE_branches_eta=etas, boost_branch_Mph_core=bst["Mph_core"],
    rmatch_eta_range=[min(e_list), max(e_list)],
    galaxy_natural_dex=gal_nat, galaxy_leak_dex=gal_leak, cassini_frac=float(frac_sin),
    fork_22Mpc_natural_Mph=n22["Mph_core"], fork_4392Mpc_natural_Mph=n4392["Mph_core"],
    alt_a0_natural_eta=na["eta_R500"], alt_a0_chiDE_min_branch_Mph=wa["Mph_core"], alt_a0_boost_Mph=Galt["boost_m1e13"]["Mph_core"],
    framework_kernel_natural_eta=nf["eta_R500"], framework_kernel_chiDE_min_branch_Mph=wf["Mph_core"], framework_kernel_boost_Mph=Hfw["boost_m1e13"]["Mph_core"],
    yukawa_natural_Mph=ny["Mph_core"],
    n_checks=NCHK[0], n_fail=len(FAIL), failed=FAIL,
)
OUT["summary"] = summary
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "itemA_reconstruct_lever_2026.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
print(json.dumps(summary, indent=1, default=float))
print(f"\n{NCHK[0]} checks, {len(FAIL)} failed")
sys.exit(1 if FAIL else 0)
