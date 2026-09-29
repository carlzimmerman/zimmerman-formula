#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
A3 -- HOW THE CAP ENTERS THE FLUID LAGRANGIAN: minimality, the constraint entry, the saturating-EOS entry and its OBSTRUCTION, and the
EOS-independent consequence of a bounded pressure (the maximum dark column a0/(2 pi G)).  Companion to A1 (action, dof) and A2 (FRW).

The two entries the task lists, and one more, are examined:
  N1  DIMENSIONAL ANALYSIS (sympy nullspace): with (Mp2, Lambda, m, n, P) and c = 1 the only invariant of the fluid state is nu = m n/(Mp2 Lambda);
      so any Lambda-tied, hbar-free, single-current fluid has P = P_cap(Lambda) F(nu), P_cap = eps Mp2 Lambda.  ONLY F is free.  (DERIVED)
  N2  CONSTRAINT ENTRY (Lagrange multiplier imposing P = P_cap): solves to rho = -P_cap + C n: dust plus a shift of Lambda by -P_cap/Mp2 = -eps Lambda.
      The cap is then ALWAYS saturated: it renormalises Lambda (0.0022 dex in a0, absorbed by kappa) and carries no physics.  (DERIVED)
  N3  SATURATING-EOS ENTRY (POSTULATED, the entry used in A1/A2): F(x) = x^2/(1+x^2), x = nu/nu_s.
      (i)   nu_s = 1 (no new number): c_s^2(z=0) ~ 6e-3 and the linear growth is suppressed to 5-14%: EXCLUDED by orders of magnitude.
      (ii)  nu_s free: two-fluid linear growth with the EOS's c_s^2(z) gives nu_min(k) (smallest nu_s with growth within 5% / 20% / 50% of LCDM
            at scale k); nu_min propto k^{3/2}.
      (iii) engagement: the cap is reached (F >= 1/2) at the radius r_M where g_N = a0 (P2 point-mass phantom, P_d = P_cap exactly there) iff
            nu_M(M_b) >= nu_s, with nu_M propto M_b^{-1/2} (exact).  Since nu_min(k(M)) is ALSO propto M^{-1/2}, the ratio g0 = nu_M/nu_min is a PURE NUMBER
            and the mass window in which the cap is engaged AND the structure is un-suppressed has width M_max/M_min = g0^2, independent of nu_s.
  N4  EOS-INDEPENDENT CONSEQUENCE of P <= P_cap (self-gravitating plane-symmetric slab): P + g^2/(8 pi G) = const  =>  Sigma <= a0/(2 pi G).  (DERIVED)
  N5  the cap here is a HARD bound; the CFG2 hydrostatic medium has P_d = sqrt(P_Lambda P_N) = y P_cap > P_cap for y = g_N/a0 > 1: a different object.

MUTATE=1  the multiplier is replaced by a thawing scalar: the derived column bound Sigma_max(z) = a0(z)/(2 pi G) is no longer flat (must FAIL).
MUTATE=2  the tie is dropped (cap reads a constant Lc): Sigma_max does not follow Lambda_0 across universes (must FAIL).
N1-N3 concern the ENTRY FORM and are the same in every mode (they test the entry, not the tie).
Run:  python3 A3_cap_entry_form_and_obstruction.py     (MUTATE=1 or 2 for the controls)
"""
import os
import sys
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import A_common as C

R = C.Run("A3_cap_entry_form_and_obstruction")
P, check = R.P, R.check
M_ = C.MUTATE
P(__doc__)
P("MUTATE mode = %d" % M_)
EPS = float(C.EPS)
c_kms = C.C_SI / 1e3

# ---------------------------------------------------------------------------------------------- declared conventions
H0, Oc, Ob, OL, Or_ = 67.4, 0.265, 0.050, 0.685, 9.1e-5           # km/s/Mpc; Planck-like, Omega_c = the harness's 0.265 [declared inputs, not fitted here]
Om = Oc + Ob
nu0 = Oc / OL                                                     # rho_c0/rho_Lambda
rho_crit = 2.775e11 * (H0 / 100.0) ** 2                           # Msun / Mpc^3
rho_m = Om * rho_crit
FB_GAL = 0.05                                                     # baryonic mass / halo mass [declared; sensitivity below]

# ================================================================================================= N1
R.banner("N1  DIMENSIONAL ANALYSIS: what can P depend on?  (sympy nullspace, c = 1, dimensions in (mass, length))")
names = ["Mp2", "Lambda", "m", "n", "P"]
dims = {"Mp2": (1, -1), "Lambda": (0, -2), "m": (1, 0), "n": (0, -3), "P": (1, -3)}         # [Mp2] = 1/G = M/L (c=1); [Lambda] = L^-2; [P] = M/L^3
Dm = sp.Matrix([[dims[k][0] for k in names], [dims[k][1] for k in names]])
ns = Dm.nullspace()
rk = Dm.rank()
P("  dimension matrix rank %d, %d variables -> %d independent dimensionless groups" % (rk, len(names), len(names) - rk))
for v in ns:
    P("    group exponents (Mp2, Lambda, m, n, P): " + str(list(v.T)))
nu_sym, Pi1 = sp.symbols('nu Pi1')
# the state variable is n (m only rescales n: J -> lambda J, m -> m/lambda leaves rho(n) redundant); groups containing P: P/(Mp2 Lambda) and the fluid ratio nu
g_P = sp.Matrix([sp.Rational(-1), sp.Rational(-1), 0, 0, 1])                # P/(Mp2 Lambda)
g_nu = sp.Matrix([sp.Rational(-1), sp.Rational(-1), 1, 1, 0])               # m n/(Mp2 Lambda)
ok_groups = (Dm * g_P == sp.zeros(2, 1)) and (Dm * g_nu == sp.zeros(2, 1))
third = [v for v in ns if v[4] == 0 and v[3] == 0]                          # a group without P and n: Mp2/(m sqrt(Lambda)) (a mass ratio; m is a conventional normalisation)
check("N1", "the invariants of a Lambda-tied, hbar-free, single-current fluid are u = n/Lambda^(3/2) (state), P/(Mp2 Lambda) (response) and the rest-mass ratio mu = m sqrt(Lambda)/Mp2 "
      "(a constant coefficient); nu = m n/(Mp2 Lambda) = mu u.  Hence EVERY such EOS is P = Mp2 Lambda [u f' - f](u) and the cap can enter ONLY as an amplitude P_cap = eps Mp2 Lambda "
      "times a shape F(nu/nu_s)",
      "nullspace dimension %d (groups printed above); P/(Mp2 Lambda) and nu are dimensionless: %s; the mass ratio is a third independent group: %s" % (len(ns), ok_groups, len(third) > 0),
      ok_groups and len(ns) == 3,
      "MINIMAL: no other pressure scale exists without adding a constant.  What is NOT fixed by dimensions: the shape F and every dimensionless number inside it (the scale nu_s)")

# ================================================================================================= N2
R.banner("N2  CONSTRAINT ENTRY: a Lagrange multiplier imposing P = P_cap")
nn, Pc, Cc = sp.symbols('n P_c C', positive=True)
rf = sp.Function('rho')
sol = sp.dsolve(sp.Eq(nn * rf(nn).diff(nn) - rf(nn), Pc), rf(nn))
rho_sol = sp.simplify(sol.rhs)
Mp2s, Ls, es = sp.symbols('Mp2 Lambda epsilon', positive=True)
Leff = sp.simplify((Mp2s * Ls - Pc.subs(Pc, es * Mp2s * Ls)) / Mp2s)                       # 3 H^2 = Mp2 Lambda + rho = (Mp2 Lambda - P_c) + C1 n
dlog_a0 = 0.5 * math.log10(1.0 / (1.0 - EPS))
n2_ok = sp.simplify(Leff - Ls * (1 - es)) == 0
check("N2", "P == P_cap gives rho = -P_cap + C1 n (dust + a constant): T_mn = C1 n u u + P_cap g_mn... i.e. Lambda_eff = Lambda (1 - eps): the always-saturated cap only "
      "renormalises Lambda", "rho = %s ; Lambda_eff = %s (%s); a0 shifts by %+.4f dex (absorbed in the FITTED kappa)" % (rho_sol, Leff, n2_ok, dlog_a0), n2_ok,
      "no cap PHYSICS: the constraint entry either binds everywhere (this) or is the unconstrained fluid (multiplier zero, pressure a free function)")

# ================================================================================================= N3
R.banner("N3  SATURATING-EOS ENTRY: P = P_cap F(nu/nu_s), F = x^2/(1+x^2)  (POSTULATED).  Cold-FRW growth and engagement")


def E2f(a):
    return Om / a ** 3 + Or_ / a ** 4 + OL


def cs2_eos(nus, a):
    nu = nu0 / a ** 3
    x = nu / nus
    Fp = 2 * x / (1 + x ** 2) ** 2
    drho = 1 + EPS * (np.arctan(x) + x / (1 + x ** 2))
    return EPS * Fp / nus / drho


def growth(nus, k, zi=1000.0, cs2fn=None):
    """two-fluid sub-horizon linear growth (cold fluid with c_s^2(z) of the EOS + pressureless baryons), returns delta_matter(z=0);
    nus=None and cs2fn=None: pressureless.  cs2fn(a): an alternative c_s^2(a) (used for the DBI/tachyon entry)."""
    def rhs(x, y):
        a = math.exp(x); e2 = E2f(a); Hh = H0 * math.sqrt(e2)
        dlnE = -(3 * Om / a ** 3 + 4 * Or_ / a ** 4) / (2 * e2)
        Omc = Oc / a ** 3 / e2; Omb = Ob / a ** 3 / e2
        dc, dcx, db, dbx = y
        src = 1.5 * (Omc * dc + Omb * db)
        if cs2fn is not None:
            pr = cs2fn(a) * (c_kms * k / (a * Hh)) ** 2
        else:
            pr = (cs2_eos(nus, a) * (c_kms * k / (a * Hh)) ** 2) if nus is not None else 0.0
        return [dcx, -(2 + dlnE) * dcx - pr * dc + src, dbx, -(2 + dlnE) * dbx + src]
    a_i = 1 / (1 + zi)
    s = solve_ivp(rhs, [math.log(a_i), 0], [a_i, a_i, a_i, a_i], rtol=1e-9, atol=1e-14, method='LSODA')
    dc, dcx, db, dbx = s.y[:, -1]
    return (Oc * dc + Ob * db) / Om


BASE = {}


def suppression(nus, k):
    if k not in BASE:
        BASE[k] = growth(None, k)
    return growth(nus, k) / BASE[k]


# (i) zero new number
cs0 = float(cs2_eos(1.0, 1.0))
S1 = {k: suppression(1.0, k) for k in (0.1, 0.5, 2.0, 10.0)}
bound0 = 1.5 * (Oc / E2f(1.0)) * (H0 / (c_kms * 10.0)) ** 2
check("N3-i", "nu_s = 1 (no new number): c_s^2(z=0) = eps F'(nu0) ~ 6e-3 and the linear growth is crushed",
      "c_s^2(0) = %.3e (c_s = %.0f km/s; the Jeans bound at k = 10/Mpc is %.2e: excess factor %.1e); growth ratio to LCDM at k = 0.1, 0.5, 2, 10 /Mpc: %s"
      % (cs0, c_kms * math.sqrt(cs0), bound0, cs0 / bound0, ", ".join("%.3f" % S1[k] for k in S1)), max(S1.values()) < 0.2 and cs0 / bound0 > 1e6,
      "OBSTRUCTION 1: with only (kappa, Lambda, G, c) the cap is 1% of rho_Lambda and a barotropic fluid that reaches it near rho ~ rho_Lambda has c_s^2 ~ eps")

# (i-b) the DBI / tachyon entry: L = -P_cap sqrt(1 - X): the one bounded-stress fluid with NO second scale
cs2_dbi = lambda a: EPS ** 2 / (EPS ** 2 + (nu0 / a ** 3) ** 2)                # rho = sqrt(V^2 + J^2), P = -V^2/rho, c_s^2 = (V/rho)^2, V = P_cap
S_dbi = {k: growth(None, k, cs2fn=cs2_dbi) / BASE.setdefault(k, growth(None, k)) for k in (0.01, 0.05, 0.1, 0.5, 2.0)}
cs0_dbi = float(cs2_dbi(1.0))
check("N3-i-b", "DBI/tachyon entry L = -P_cap sqrt(1 - X) (tension P_cap = eps Mp2 Lambda, |P| <= P_cap, NO second scale): P = -P_cap^2/rho (Chaplygin), c_s^2 = (P_cap/rho)^2",
      "c_s^2(z=0) = %.2e (c_s = %.0f km/s); growth ratio to LCDM at k = 0.01, 0.05, 0.1, 0.5, 2 /Mpc: %s; the cap binds where rho ~ P_cap = 0.01 rho_Lambda (VOIDS), and P < 0"
      % (cs0_dbi, c_kms * math.sqrt(cs0_dbi), ", ".join("%.3f" % S_dbi[k] for k in S_dbi)), max(S_dbi[k] for k in (0.1, 0.5, 2.0)) < 0.5 and cs0_dbi > 1e-4,
      "OBSTRUCTION 1b: the only bounded-stress fluid that needs no new number has the WRONG SIGN (tension), binds in voids (not in bound regions) and its c_s^2(0) ~ 7e-4 kills growth")

# (ii) nu_min(k)
kgrid = [0.5, 2.0, 10.0, 30.0]
nugrid = np.geomspace(1e3, 3e8, 70)
NUMIN = {}
S_ARR = {k: np.array([suppression(v, k) for v in nugrid]) for k in kgrid}
for thr in (0.5, 0.8, 0.95):
    for k in kgrid:
        good = S_ARR[k] >= thr
        idx = len(good)
        for i in range(len(good) - 1, -1, -1):          # smallest nu_s such that suppression >= thr for ALL larger nu_s on the grid (conservative)
            if good[i]:
                idx = i
            else:
                break
        NUMIN[(thr, k)] = nugrid[idx] if idx < len(good) else float('inf')
P("  nu_min(k): smallest nu_s with linear growth at z=0 within (1-thr) of LCDM, k in 1/Mpc  [conservative: all larger nu_s also pass]")
P("     thr \\ k   " + "  ".join("%9g" % k for k in kgrid))
for thr in (0.5, 0.8, 0.95):
    P("     %.2f      " % thr + "  ".join("%9.2e" % NUMIN[(thr, k)] for k in kgrid))
ex = math.log(NUMIN[(0.8, 30.0)] / NUMIN[(0.8, 2.0)]) / math.log(30.0 / 2.0)
ex2 = math.log(NUMIN[(0.95, 10.0)] / NUMIN[(0.95, 2.0)]) / math.log(10.0 / 2.0)
rho_L_msunpc3 = C.RHO_L / C.MSUN_PC3
sig_star = lambda nus: c_kms * math.sqrt(EPS / nus)
P("  meaning of nu_s: the cap is reached at rho_* = nu_s rho_Lambda (rho_Lambda = %.3e Msun/pc^3) and corresponds to a velocity scale sigma_* = c sqrt(eps/nu_s):" % rho_L_msunpc3)
for thr in (0.8, 0.95):
    P("     thr %.2f: " % thr + "; ".join("k=%g/Mpc: nu_min=%.2e -> rho_*=%.3f Msun/pc^3, sigma_*=%.0f km/s" % (k, NUMIN[(thr, k)], NUMIN[(thr, k)] * rho_L_msunpc3, sig_star(NUMIN[(thr, k)])) for k in kgrid))
check("N3-ii", "with nu_s free the cold-FRW growth is restored above nu_min(k) propto k^(3/2)  (the EOS's c_s^2 peaks at c_s^2 ~ 0.65 eps/nu_s at the redshift nu_cos = nu_s)",
      "fitted exponents %.2f (thr 0.8), %.2f (thr 0.95); e.g. nu_min(k = 2/Mpc) = %.2e, nu_min(10/Mpc) = %.2e (5%% growth criterion)"
      % (ex, ex2, NUMIN[(0.95, 2.0)], NUMIN[(0.95, 10.0)]), abs(ex - 1.5) < 0.25 and abs(ex2 - 1.5) < 0.25,
      "nu_s is a NEW dimensionless constant; its size is set by the smallest structure that must survive: it is FITTED/declared, not derived from kappa")

# (iii) engagement and the pure number g0


def nu_M(Mb_msun):
    """local dark density of the P2 point-mass phantom at r_M (g_N = a0), over rho_Lambda.  M(r) = M_b sqrt(1 + r^2/r_M^2)  (CFG2 A2)."""
    Mb = Mb_msun * C.MSUN
    rM = math.sqrt(C.G_SI * Mb / C.A0["canonical"])
    rho_d = Mb / (4 * math.sqrt(2) * math.pi * rM ** 3)
    return rho_d / C.RHO_L, rM


def k_of_M(Mh_msun, kconv=math.pi):
    Rl = (3 * Mh_msun / (4 * math.pi * rho_m)) ** (1.0 / 3.0)               # Mpc
    return kconv / Rl


def g0(thr, fh, kconv, Mb=3e10):
    kk = k_of_M(fh * Mb, kconv)
    # nu_min(k) scaled with the measured k^{3/2} law from the anchor at k = 2/Mpc
    nu_min_k = NUMIN[(thr, 2.0)] * (kk / 2.0) ** 1.5
    return nu_M(Mb)[0] / nu_min_k, kk, nu_min_k


# the exactness of the M-scalings
nuM_a, rM_a = nu_M(1e9)
nuM_b, rM_b = nu_M(1e11)
scal = math.log(nuM_b / nuM_a) / math.log(1e11 / 1e9)
check("N3-iii-a", "nu_M(M_b) (local dark density at r_M over rho_Lambda) scales as M_b^(-1/2) exactly", "nu_M(1e9) = %.3e, nu_M(1e11) = %.3e, exponent %.6f (expect -0.5); r_M(1e9) = %.2f kpc"
      % (nuM_a, nuM_b, scal, rM_a / (C.PC * 1e3)), abs(scal + 0.5) < 1e-9,
      "the cap is reached (P_d = P_cap) exactly at r_M for the P2 phantom (P_d = sqrt(P_Lambda P_N) = y P_cap at y = 1)")
P("  g0 = nu_M(M_b)/nu_min(k(M_h)) at M_b = 3e10 (M_h = f_h M_b); window in baryonic mass covered by ONE nu_s: M_max/M_min = g0^2:")
P("     thr   f_h   k-convention    k(M_h)[1/Mpc]   nu_min(k)     nu_M(3e10)     g0      M_max/M_min")
rows = []
for thr in (0.5, 0.8, 0.95):
    for fh in (10, 20, 40):
        for kconv, kn in ((math.pi, "pi/R"), (2 * math.pi, "2pi/R")):
            g, kk, nmk = g0(thr, fh, kconv)
            rows.append((thr, fh, kn, g))
            P("     %.2f  %3d   %-8s       %8.3f      %.3e     %.3e   %6.3f     %8.3f" % (thr, fh, kn, kk, nmk, nu_M(3e10)[0], g, g * g))
gvals = [r[3] for r in rows]
g_ref = g0(0.95, 20, math.pi)[0]
g_ref2 = g0(0.8, 20, math.pi)[0]
g_best = max(gvals)
# M-independence tested DIRECTLY (independent of the fitted exponent): re-solve nu_min at the k of a 1e9 and a 3e11 Msun baryonic mass
fine = np.geomspace(1e3, 3e8, 140)


def nu_min_direct(k, thr):
    b = growth(None, k)
    sarr = np.array([growth(v, k) / b for v in fine])
    good = sarr >= thr
    idx = len(good)
    for i in range(len(good) - 1, -1, -1):
        if good[i]:
            idx = i
        else:
            break
    return fine[idx]


g_dir = {}
for Mb_ in (1e9, 3e11):
    kk_ = k_of_M(20 * Mb_, math.pi)
    g_dir[Mb_] = (nu_M(Mb_)[0] / nu_min_direct(kk_, 0.8), kk_)
P("  direct check of the M-independence (thr 0.8, f_h = 20, k = pi/R): M_b = 1e9: k = %.2f/Mpc, g0 = %.3f;  M_b = 3e11: k = %.2f/Mpc, g0 = %.3f"
  % (g_dir[1e9][1], g_dir[1e9][0], g_dir[3e11][1], g_dir[3e11][0]))
scale_free = abs(g_dir[1e9][0] / g_dir[3e11][0] - 1) < 0.30
check("N3-iii-b", "g0 = nu_M/nu_min(k(M)) does not depend on M_b (both propto M^(-1/2)); so one nu_s engages the cap over a mass window of ratio g0^2 only, whatever nu_s is",
      "g0 (5%% growth, f_h = 20, k = pi/R) = %.2f, (20%%) = %.2f; most generous corner of the grid (50%% suppression allowed, f_h = 40, k = pi/R) g0 = %.2f -> window %.1fx in mass; "
      "M-independence (direct re-solves at 1e9 and 3e11 Msun, agree within 30%%): %s; needed window for the BTFR (1e8 - 1e12): 1e4" % (g_ref, g_ref2, g_best, g_best ** 2, scale_free),
      scale_free and g_best ** 2 < 1e2,
      "OBSTRUCTION 2 (screening estimate: the convention grid moves g0 over 0.08-3.3, a factor ~40, but even its most generous corner gives ONE decade in mass, not the 4-5 of the BTFR): "
      "no nu_s makes the saturating-EOS cap engaged at r_M across the BTFR mass range while the structures of those masses keep their linear growth")

# ================================================================================================= N4
R.banner("N4  EOS-INDEPENDENT CONSEQUENCE of P <= P_cap: the maximum dark column of a self-gravitating slab")
z_, G_ = sp.symbols('z G', positive=True)
Pf = sp.Function('P')(z_); gf = sp.Function('g')(z_); rhof = sp.Function('rho')(z_)
inv = sp.simplify(sp.diff(Pf + gf ** 2 / (8 * sp.pi * G_), z_).subs({sp.diff(Pf, z_): -rhof * gf, sp.diff(gf, z_): 4 * sp.pi * G_ * rhof}))
slab_ok = inv == 0
Sig_can = C.A0["canonical"] / (2 * math.pi * C.G_SI) / C.MSUN_PC2
Sig_alt = C.A0["alt"] / (2 * math.pi * C.G_SI) / C.MSUN_PC2
check("N4", "hydrostatic plane slab (dP/dz = -rho g, dg/dz = 4 pi G rho): d/dz [P + g^2/(8 pi G)] = 0, so with P(inf) = 0 and P(0) <= P_cap: g_inf <= a0 and the total column "
      "Sigma <= a0/(2 pi G)", "invariant %s; Sigma_max = %.1f (canonical) / %.1f (alt) Msun/pc^2  (CFG2 A4 quotes 106.9 / 129.2; Donato+09: 10^(2.15 +- 0.2) = 141)" % (slab_ok, Sig_can, Sig_alt),
      slab_ok and abs(Sig_can - 106.9) < 0.5 and abs(Sig_alt - 129.2) < 0.7,
      "DERIVED for ANY EOS: it needs only P <= P_cap.  This is what the cap DOES; the entry form only decides whether it binds")

# tie consequences of the bound: flatness in z and across universes -- the checks the mutations hit
R.banner("T  the column bound follows the tie: Sigma_max(z) = a0(z)/(2 pi G), and across universes Sigma_max propto sqrt(Lambda_0)")


def thawing_a0_ratio(zs, lam_v=1.27):
    """MUTATE=1: thawing exponential scalar U = U0 exp(-lam psi), Mp2 = 1, matter rho_m = rho_m0 a^-3; a0 = sqrt(eps U)."""
    rho_m0 = 1.0

    def run(psi_i):
        def rhs(x, y):
            psi, phi = y
            a = math.exp(x)
            U = math.exp(-lam_v * psi)
            rm = rho_m0 / a ** 3
            H2 = (U + rm) / (3 - phi ** 2 / 2)
            dlnH = -(rm / H2 + phi ** 2) / 2
            return [phi, -(3 + dlnH) * phi + lam_v * U / H2]
        s = solve_ivp(rhs, [math.log(1e-3), 0], [psi_i, 0.0], rtol=1e-11, atol=1e-13, dense_output=True, method='DOP853')
        return s
    def om0(psi_i):
        s = run(psi_i); psi, phi = s.y[:, -1]
        U = math.exp(-lam_v * psi); H2 = (U + rho_m0) / (3 - phi ** 2 / 2)
        return rho_m0 / (3 * H2) - 0.315
    psi_i = brentq(om0, -2.0, 8.0, xtol=1e-12)
    s = run(psi_i)
    U0 = math.exp(-lam_v * s.y[0, -1])
    out = {}
    for z in zs:
        psi = s.sol(math.log(1.0 / (1.0 + z)))[0]
        out[z] = math.sqrt(math.exp(-lam_v * psi) / U0)
    return out


ZT = [0.5, 1.0, 2.5]
import json
import subprocess
tag = "" if M_ == 0 else "_MUTATE%d" % M_
a2json = os.path.join(C.HERE, "A2_frw_flat_a0_and_dust_limit_results" + tag + ".json")
if not os.path.exists(a2json):
    subprocess.run([sys.executable, os.path.join(C.HERE, "A2_frw_flat_a0_and_dust_limit.py")], env=dict(os.environ, MUTATE=str(M_)), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
dl = json.load(open(a2json))["dlog_a0_dex"]                     # a0(z)/a0(0) read from A2's INTEGRATED solution of the same mode (Lambda from the geometry)
Sig_z = {z: 10 ** dl[str(z)] for z in ZT}                       # Sigma_max = a0/(2 pi G) tracks a0 exactly
txt = ("Sigma_max(z)/Sigma_max(0) from A2's integrated solution (%s): " % ("thawing scalar" if M_ == 1 else "HT + fluid")
       + ", ".join("z=%g: %.12f" % (z, Sig_z[z]) for z in ZT) + " (%+.4f dex at z = 2.5)" % dl["2.5"])
ok = all(abs(v - 1) < 1e-9 for v in Sig_z.values())
check("T-flat", "Sigma_max(z) = a0(z)/(2 pi G) is flat in z (the cap does not run)", txt, ok, "DERIVED via H-CONST (A1) and confirmed on the integrated geometry (A2-a); MUTATE=1 replaces the multiplier and the bound rises toward high z")
Lam_list = (0.5, 1.0, 2.0, 7.0)
Sig_u = []
for Lam0 in Lam_list:
    Lfl = 1.0 if M_ == 2 else Lam0                             # MUTATE=2: the cap reads the constant Lc = 1
    Sig_u.append(math.sqrt(EPS * Lfl) / math.sqrt(EPS * Lam0))
check("T-tie", "across universes the column bound follows the HT constant: Sigma_max(Lambda_0)/[kappa sqrt(Lambda_0/8 pi)/(2 pi G)] = 1", "ratios " + ", ".join("%.6f" % v for v in Sig_u),
      all(abs(v - 1) < 1e-12 for v in Sig_u), "MUTATE=2: the fluid's cap reads Lc, so Sigma_max is decoupled from Lambda_0")

# ================================================================================================= N5
R.banner("N5  HARD BOUND vs CFG2's hydrostatic medium")
y_ = np.array([0.1, 0.5, 1.0, 3.0, 10.0])
Pd_over_Pc = y_                                                     # P_d = sqrt(P_Lambda P_N) with P_N/P_Lambda = y^2  =>  P_d/P_cap = y
check("N5", "CFG2 A2's settled medium has P_d = sqrt(P_Lambda P_N) = y P_cap: it EXCEEDS the cap for y = g_N/a0 > 1 (inside r_M); a hard-bound EOS cannot supply it",
      "P_d/P_cap at y = %s: %s" % (list(y_), list(Pd_over_Pc)), bool(np.all(Pd_over_Pc[y_ > 1] > 1)),
      "the action written here realises the CFG5-type cap (a bound on the stress), NOT the CFG2 stress law (a scale in a geometric mean); the latter depends on the BARYONS' field and has no local fluid EOS (CFG2 A6, N20)",
      load_bearing=False)

R.finish()
