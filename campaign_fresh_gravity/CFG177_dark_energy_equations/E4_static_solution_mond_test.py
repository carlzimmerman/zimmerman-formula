#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
E4 -- the dynamical vacuum current (E3's DYN) around baryons: its static solution, the acceleration it gives test bodies, and whether any
consequence reaches the MOND form sqrt(G M a0)/r with a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 FITTED, and no other constant.
Also (FROZEN_QUESTION Note 2): the time flow COMPACTED BY BARYONS (m proportional to Lambda^beta_b), the relation to a khronon, and the
dual-AQUAL (DAQ) scoping of what the MOND form would need.

Weak field, static, spherical; the DYN scalar phi = (M_P/sqrt s) ln Lambda, V = rho_vac c^2 e^{sqrt(s) phi/M_P}; psi = phi/M_P.
s = kappa^2 (the declared illustration of E3; every DYN force scales as s or (1+w0), so the G1 verdict does not depend on it -- E4-INVERT).
(1+w0) is read from E3's committed results JSON (main run).  Targets: P2 primary, nu_mono reported (CFG44 Bcommon, read-only); both footings;
M_b = 1e9..1e12 Msun; point mass, exponential sphere h = 0.5 r_M and h = 3 kpc; x = r/r_M in [0.1, 30].

MUTATE=1  POSITIVE CONTROL: the G1 scorer is fed the DAQ force with U built to reproduce P2 (a restatement by construction); the
          'no MOND force' headline (E4-G1-DUST) must flip, proving the scorer, the targets and the grids are live.
"""
import os
import sys
import json
import math
import numpy as np
import sympy as sp
from scipy.integrate import cumulative_trapezoid, quad
from scipy.special import gammainc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import E_common as C

R = C.Run("E4_static_solution_mond_test")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)
P("MUTATE mode = %d  (0 = the DYN current's own force; 1 = positive control: the DAQ force built to reproduce P2)" % M)
B = C.import_bcommon()
e3 = json.load(open(os.path.join(C.HERE, "E3_dynamical_vacuum_current_results.json")))
S_VAL = float(e3["numbers"]["s"])
W0 = float(e3["numbers"]["background"]["w0"])
LAM = math.sqrt(S_VAL)
P("  from E3 (main run): s = %.4f, lambda = %.4f, 1 + w0 = %.5f" % (S_VAL, LAM, 1 + W0))
R.num("s", S_VAL); R.num("one_plus_w0", 1 + W0)

# ============================================================================================ A: symbolic pieces
R.banner("A  SYMBOLIC: the linearised Klein-Gordon equation on a weak static metric; the scalar's density perturbation; the gradient energy's focusing")
tt, xx, yy, zz, e = sp.symbols('t x y z e', real=True)
Xs = (tt, xx, yy, zz)
Phi = sp.Function('Phi')(xx, yy, zz)
dph = sp.Function('dphi')(tt, xx, yy, zz)
phb = sp.Function('phib')(tt)
c0, c1, c2, c3 = sp.symbols('c0:4', real=True)
uu = sp.Symbol('u', real=True)
Vpoly = c0 + c1 * uu + c2 * uu ** 2 / 2 + c3 * uu ** 3 / 6                      # a generic cubic V (enough for first order)
Vfun = lambda arg: Vpoly.subs(uu, arg)
dVfun = lambda arg: sp.diff(Vpoly, uu).subs(uu, arg)
g = sp.diag(-(1 + 2 * e * Phi), 1 - 2 * e * Phi, 1 - 2 * e * Phi, 1 - 2 * e * Phi)
gi = g.inv()
sg = sp.sqrt(-g.det())
ph = phb + e * dph
box = sum(sp.diff(sg * gi[i, i] * sp.diff(ph, Xs[i]), Xs[i]) for i in range(4)) / sg
eom = box - dVfun(ph)
first = sp.diff(eom, e).subs(e, 0).doit()
first = first.subs(sp.Derivative(phb, (tt, 2)), -dVfun(phb))
lap = sum(sp.diff(dph, v, 2) for v in (xx, yy, zz))
Vp = dVfun(phb)
Vpp = sp.diff(Vpoly, uu, 2).subs(uu, phb)
expect = -sp.diff(dph, tt, 2) + lap - Vpp * dph - 2 * Phi * Vp
kg_ok = sp.simplify(sp.expand(first - expect)) == 0
check("E4-KG", "linearised box(phi) = V'(phi) on -(1+2Phi)dt^2 + (1-2Phi)dx^2 with a rolling background (phib'' = -V'): "
      "laplacian(dphi) - dphi_tt = V'' dphi + 2 Phi V'  (static: the baryons source the dark energy ONLY through their potential, with strength V')",
      "identity: %s" % kg_ok, kg_ok)
# density perturbation rho = -T^0_0 to first order
dd = [sp.diff(ph, v) for v in Xs]
X2 = sum(gi[i, i] * dd[i] ** 2 for i in range(4))
T00mixed = gi[0, 0] * dd[0] * dd[0] - (X2 / 2 + Vfun(ph))
rho1 = sp.diff(-T00mixed, e).subs(e, 0).doit()
rho_exp = sp.diff(phb, tt) * sp.diff(dph, tt) - Phi * sp.diff(phb, tt) ** 2 + Vp * dph
drho_ok = sp.simplify(sp.expand(rho1 - rho_exp)) == 0
# second order static gradient energy: rho + sum p_i = 0 (no focusing)
gx, gy, gz = sp.symbols('gx gy gz', real=True)
gvec = [gx, gy, gz]
Tij = [[gvec[i] * gvec[j] - (1 if i == j else 0) * (gx ** 2 + gy ** 2 + gz ** 2) / 2 for j in range(3)] for i in range(3)]
tol = sp.simplify((gx ** 2 + gy ** 2 + gz ** 2) / 2 + sum(Tij[i][i] for i in range(3)))
check("E4-DRHO", "the scalar's first-order density: delta rho = phib' dphi' - Phi phib'^2 + V' dphi (the -Phi phib'^2 term is the time-FLOW's own response, "
      "nonzero only when the dark energy rolls); a static gradient energy (grad dphi)^2/2 has rho + sum p_i = 0, i.e. it does not focus (Tolman)",
      "first-order delta rho: %s; rho + sum p of static gradient energy = %s" % (drho_ok, tol), drho_ok and tol == 0)

# ============================================================================================ B: DYN force on test baryons
R.banner("B  THE DYN VACUUM CURRENT AROUND BARYONS: (i) dust baryons only (they source it only through Phi); (ii) plus CFG43's cap fluid at CFG44's target pressure")
Gs, cs = C.G_SI, C.C_SI
LamSI = C.LAMBDA_SI
rhoL = C.RHO_L
R_far = cs / C.H_LAMBDA


def baryons(prof, Mkg, rM, h=None):
    """return functions M_b(<r), Phi(r) [m^2/s^2] (SI)."""
    if prof == "point":
        return (lambda r: Mkg * np.ones_like(r)), (lambda r: -Gs * Mkg / r)
    return (lambda r: Mkg * gammainc(3.0, r / h)), (lambda r: -Gs * Mkg * gammainc(3.0, r / h) / r - Gs * Mkg * (r + h) * np.exp(-r / h) / (2 * h * h))


def dyn_forces(prof, Mkg, rM, a0, h=None, cap=True):
    """accelerations (SI) on the x-grid: g_pot (V' dphi, normalisation giving the larger of dphi(0) = 0 or dphi(c/H) = 0), g_kin (-Phi phib'^2),
    g_cap (cap-fluid source, potential term + its gradient energy at full weight, a bound)."""
    x = np.geomspace(1e-5, 1000.0, 20001)
    r = x * rM
    Mb, Phi_ = baryons(prof, Mkg, rM, h)
    ph_ = Phi_(r)
    # (i) laplacian(dpsi) = 2 lambda Lambda Phi/c^2 ; r^2 dpsi' = Int 2 lam Lam Phi r^2/c^2 ; dpsi(0) = 0
    src = 2 * LAM * LamSI * ph_ / cs ** 2
    r2dp = cumulative_trapezoid(src * r * r, r, initial=0.0) + (src[0] * r[0] ** 3 / 3)
    dpsi_p = r2dp / r ** 2
    dpsi = cumulative_trapezoid(dpsi_p, r, initial=0.0)
    # alternative normalisation: dpsi = 0 at R_far (point-mass slope continued linearly beyond the grid)
    slope_far = dpsi_p[-1]
    dpsi_far = dpsi - (dpsi[-1] + slope_far * (R_far - r[-1]))
    out = {}
    for lab, dp in (("norm0", dpsi), ("normfar", dpsi_far)):
        drho = 3.0 * LAM * rhoL * dp                           # factor-3 allowance for the phib' dphi' term (same order in slow roll)
        Mp_ = cumulative_trapezoid(4 * math.pi * r * r * drho, r, initial=0.0)
        out[lab] = Gs * Mp_ / r ** 2
    g_pot = np.maximum(np.abs(out["norm0"]), np.abs(out["normfar"]))
    drho_kin = -(ph_ / cs ** 2) * (1 + W0) * rhoL
    g_kin = Gs * cumulative_trapezoid(4 * math.pi * r * r * drho_kin, r, initial=0.0) / r ** 2
    res = dict(x=x, r=r, g_pot=g_pot, g_kin=g_kin, g_pot_signed=out["norm0"])
    if cap:
        # (ii) target pressure P(r) = (a0/4pi) Int_r^inf M_b r'^-3 dr' (+ tail beyond the grid, point-mass form)
        integrand = Mb(r) / r ** 3
        tail = Mb(r[-1:])[0] / (2 * r[-1] ** 2)
        Pt = (a0 / (4 * math.pi)) * (np.concatenate([cumulative_trapezoid(integrand[::-1], r[::-1], initial=0.0)[::-1] * -1.0]) + tail)
        # laplacian(dpsi) = -8 pi G lambda P/c^4 ; dpsi(1000 r_M) = 0
        r2d = cumulative_trapezoid(-8 * math.pi * Gs * LAM * Pt / cs ** 4 * r * r, r, initial=0.0)
        dpc_p = r2d / r ** 2
        dpc = -(cumulative_trapezoid(dpc_p[::-1], r[::-1], initial=0.0)[::-1] * -1.0)
        drho_c = 3.0 * LAM * rhoL * np.abs(dpc) + (cs ** 2 / (16 * math.pi * Gs)) * dpc_p ** 2
        res["g_cap"] = Gs * cumulative_trapezoid(4 * math.pi * r * r * drho_c, r, initial=0.0) / r ** 2
        res["P"] = Pt
    return res


rows = {}
g1_resid = {}
worst = dict(dust=0.0, cap=0.0)
pm_check = None
for foot in ("canonical", "alt"):
    a0 = C.A0[foot]
    a0k = a0 * C.KPC_M / 1e6
    for kern in ("P2", "nu_mono"):
        for Mb_ in (1e9, 1e10, 1e11, 1e12):
            Mkg = Mb_ * C.MSUN
            rM = math.sqrt(Gs * Mkg / a0)
            rMk = rM / C.KPC_M
            for plab, prof_b, hh in (("point", B.point_mass(Mb_), None), ("exp h=0.5rM", B.exp_sphere(Mb_, 0.5 * rMk), 0.5 * rM),
                                     ("exp h=3kpc", B.exp_sphere(Mb_, 3.0), 3 * C.KPC_M)):
                F = dyn_forces("point" if plab == "point" else "exp", Mkg, rM, a0, hh)
                sel = (F["x"] >= 0.1) & (F["x"] <= 30)
                xs = F["x"][sel]
                rk = xs * rMk
                u = B.law_u(prof_b, rk, kern, a0=a0k)
                uN = prof_b.u(rk)
                boost = (u - uN) / rk ** 2 * 1e6 / C.KPC_M          # SI
                gN = uN / rk ** 2 * 1e6 / C.KPC_M
                glaw = u / rk ** 2 * 1e6 / C.KPC_M
                if M == 1:
                    # positive control: the DAQ force with U built to reproduce the kernel -- g_extra = (nu(g_N/a0) - 1) g_N as a function of the Gauss field
                    nu = B.KERNELS[kern]
                    g_extra = (nu(gN / a0) - 1.0) * gN
                    ratio_d = g_extra / boost
                    ratio_c = ratio_d
                else:
                    g_extra = F["g_pot"][sel] + np.abs(F["g_kin"][sel])
                    ratio_d = g_extra / boost
                    ratio_c = F["g_cap"][sel] / boost
                key = "%s %s %.0e %s" % (foot, kern, Mb_, plab)
                rows[key] = (float(ratio_d.max()), float(ratio_c.max()))
                g1_resid[key] = float(np.max(np.abs((gN + g_extra) / glaw - 1)))
                worst["dust"] = max(worst["dust"], float(ratio_d.max()))
                worst["cap"] = max(worst["cap"], float(ratio_c.max()))
                if foot == "canonical" and kern == "P2" and plab == "point" and Mb_ == 1e11:
                    pm_check = (F, sel, boost, rM, Mkg, a0)
P("  max over x in [0.1, 30] of (DYN extra acceleration)/(the law's boost g_law - g_N):   [dust-only | with cap fluid (bound)]")
for k, v in rows.items():
    if "canonical P2" in k or ("alt P2" in k and "point" in k):
        P("    %-38s %9.2e | %9.2e   G1 residual %.3f" % (k, v[0], v[1], g1_resid[k]))
g1max_fail = min(g1_resid.values())
# point-mass analytic cross-check (canonical, 1e11): g_pot(norm0) = -pi lam^2 G rho_L Lam G M r^2/c^2 (x3 allowance), g_kin = 2 pi (1+w0) G rho_L G M/c^2
F, sel, boost, rM, Mkg, a0 = pm_check
rr = F["r"]
i1 = np.argmin(np.abs(F["x"] - 1.0))
an_pot = 3 * math.pi * LAM ** 2 * Gs * rhoL * LamSI * Gs * Mkg * rr[i1] ** 2 / cs ** 2
an_kin = 2 * math.pi * (1 + W0) * Gs * rhoL * Gs * Mkg / cs ** 2
num_pot = abs(F["g_pot_signed"][i1])
num_kin = abs(F["g_kin"][i1])
an_ok = abs(num_pot / an_pot - 1) < 1e-3 and abs(num_kin / an_kin - 1) < 1e-3
if M == 1:
    headline = worst["dust"] < 1e-10
    txt = "POSITIVE CONTROL: the DAQ force built to reproduce the kernel gives ratio max %.3f and G1 residual %.2e: the scorer SEES a MOND force when one is fed" % (worst["dust"], max(g1_resid.values()))
else:
    headline = worst["dust"] < 1e-10 and g1max_fail > 0.10
    txt = ("max ratio over all %d rows = %.2e (dust) and %.2e (cap fluid, bound); the smallest G1 residual over rows = %.3f (> 0.10: G1 FAIL in every row); "
           "point-mass analytic cross-check at x = 1: pot %.3e vs %.3e, kin %.3e vs %.3e m/s^2" % (len(rows), worst["dust"], worst["cap"], g1max_fail,
                                                                                                  num_pot, an_pot, num_kin, an_kin))
check("E4-G1-DUST", "the DYN vacuum current (the time flow made physical) exerts on test baryons an extra acceleration < 1e-10 of the law's boost at every x in [0.1, 30], "
      "every mass, profile, kernel and footing (so G1 FAILS: the total stays Newtonian to that precision)", txt, headline and (an_ok or M == 1),
      "the flow's kinetic term does pull (delta rho = -Phi phib'^2 > 0), but with (1+w0) rho_Lambda it is ~1e-12 of a0" if M == 0 else "")
check("E4-G1-CAP", "even with CFG43's cap fluid held at CFG44's TARGET pressure (which exceeds the cap inside r_M, so this is an upper bound) sourcing the vacuum, "
      "and its gradient energy counted at full weight, the extra acceleration is < 1e-10 of the boost", "max ratio %.2e" % worst["cap"], worst["cap"] < 1e-10 or M == 1)
R.num("ratio_rows", rows)
R.num("G1_residual_rows", g1_resid)

# scalings (canonical, P2, point mass): at fixed r, d ln g/d ln M; at fixed M, d ln g/d ln r -- against the deep-MOND 1/2 and -1
def g_at(Mb_, r_m):
    Mkg = Mb_ * C.MSUN
    a0 = C.A0["canonical"]
    rM = math.sqrt(Gs * Mkg / a0)
    F = dyn_forces("point", Mkg, rM, a0, None, cap=False)
    return float(np.interp(r_m, F["r"], np.abs(F["g_pot_signed"]))), float(np.interp(r_m, F["r"], np.abs(F["g_kin"])))


r_fix = 50 * C.KPC_M
gp1, gk1 = g_at(1e11, r_fix)
gp2, gk2 = g_at(1e12, r_fix)
gp3, gk3 = g_at(1e11, 2 * r_fix)
sl = dict(pot_M=math.log10(gp2 / gp1), kin_M=math.log10(gk2 / gk1), pot_r=math.log2(gp3 / gp1), kin_r=math.log2(gk3 / gk1))
sc_ok = abs(sl["pot_M"] - 1) < 0.02 and abs(sl["kin_M"] - 1) < 0.02 and abs(sl["pot_r"] - 2) < 0.05 and abs(sl["kin_r"]) < 0.05
check("E4-SCALING", "the DYN extra acceleration scales as M^1 r^2 (potential term) and M^1 r^0 (time-flow kinetic term); deep MOND needs M^(1/2) r^-1: wrong in BOTH "
      "exponents, so no value of s or (1+w) can fit all masses", "log-slopes: %s" % {k: round(v, 3) for k, v in sl.items()}, sc_ok)
R.num("scalings", sl)
# inversion: the lambda^2 (for the potential term) and the (1+w) (for the kinetic term) needed to reach the boost at x = 1 (canonical, P2, point)
inv = {}
for Mb_ in (1e9, 1e10, 1e11, 1e12):
    Mkg = Mb_ * C.MSUN
    a0 = C.A0["canonical"]
    rM = math.sqrt(Gs * Mkg / a0)
    gN1 = a0                                                   # at x = 1, g_N = a0; P2 boost = (sqrt 2 - 1) a0
    boost1 = (math.sqrt(2) - 1) * a0
    gpot_per_lam2 = 3 * math.pi * Gs * rhoL * LamSI * Gs * Mkg * rM ** 2 / cs ** 2      # with the factor-3 allowance (generous)
    gkin_per_w = 2 * math.pi * Gs * rhoL * Gs * Mkg / cs ** 2
    inv["%.0e" % Mb_] = dict(lambda2_needed=boost1 / gpot_per_lam2, one_plus_w_needed=boost1 / gkin_per_w)
# exponential-potential scaling solution (Copeland-Liddle-Wands, from memory): verify it is a fixed point and w = -1 + lambda^2/3
xs_, ys_, lm_, gm_ = sp.symbols('x y lambda gamma', real=True)
xp = -3 * xs_ + lm_ * sp.sqrt(sp.Rational(3, 2)) * ys_ ** 2 + sp.Rational(3, 2) * xs_ * (2 * xs_ ** 2 + gm_ * (1 - xs_ ** 2 - ys_ ** 2))
yp = -lm_ * sp.sqrt(sp.Rational(3, 2)) * xs_ * ys_ + sp.Rational(3, 2) * ys_ * (2 * xs_ ** 2 + gm_ * (1 - xs_ ** 2 - ys_ ** 2))
fp = {xs_: lm_ / sp.sqrt(6), ys_: sp.sqrt(1 - lm_ ** 2 / 6)}
fp_ok = sp.simplify(xp.subs(fp)) == 0 and sp.simplify(yp.subs(fp)) == 0
w_fp = sp.simplify(((xs_ ** 2 - ys_ ** 2) / (xs_ ** 2 + ys_ ** 2)).subs(fp))
lam2_min = min(v["lambda2_needed"] for v in inv.values())
onepw_min = min(v["one_plus_w_needed"] for v in inv.values())
check("E4-INVERT", "to reach the P2 boost at x = 1 the potential term needs lambda^2 >= %.1e and the kinetic term needs 1 + w >= %.1e; the scalar-dominated fixed point of an "
      "exponential potential has w = -1 + lambda^2/3 (sympy), so lambda^2 >= 2 cannot accelerate (w >= -1/3) and 1 + w <= 2 always: NO choice of the new constant s rescues G1"
      % (lam2_min, onepw_min), "fixed point verified: %s; w = %s; needed (by mass): %s" % (fp_ok, w_fp, {k: {kk: "%.2e" % vv for kk, vv in v.items()} for k, v in inv.items()}),
      fp_ok and sp.simplify(w_fp - (-1 + lm_ ** 2 / 3)) == 0 and lam2_min > 2 and onepw_min > 2)
R.num("inversion", inv)
# Solar System (G5): the DYN anomaly at 1 AU (the Sun, point mass): tidal gradient of the potential term vs Q2 <= 5.2e-27 s^-2; the kinetic term is uniform
Ms = C.MSUN
r1 = C.AU_M
g_pot_au = 3 * math.pi * LAM ** 2 * Gs * rhoL * LamSI * Gs * Ms * r1 ** 2 / cs ** 2
Q2_au = 2 * g_pot_au / r1
g_kin_au = 2 * math.pi * (1 + W0) * Gs * rhoL * Gs * Ms / cs ** 2
check("E4-SOLAR", "Solar System: the DYN anomaly at 1 AU is far below the ephemeris bound (Q2 <= 5.2e-27 s^-2, GATES 4.01); a minimally coupled scalar leaves PPN = GR",
      "potential-term acceleration %.2e m/s^2, its gradient %.2e s^-2; kinetic-term (uniform, no tide) %.2e m/s^2" % (g_pot_au, Q2_au, g_kin_au), Q2_au < 5.2e-27)

# ============================================================================================ C: the time flow compacted by BARYONS (Note 2, 3h)
R.banner("C  THE TIME FLOW COMPACTED BY BARYONS (m proportional to Lambda^beta_b): the Gauss law gains + beta_b rho_b/rho_vac; the force it gives")
r, Mq, al_, Gq, MP_ = sp.symbols('r M alpha G M_P', positive=True)
# canonical phi coupled to baryons through ln m = alpha phi/M_P (alpha = beta_b sqrt(s)); static: laplacian(dphi) = (alpha/M_P) rho_b
dphi_s = -(al_ / MP_) * Mq / (4 * sp.pi * r)
lap_ok = sp.simplify(sp.diff(r ** 2 * sp.diff(dphi_s, r), r) / r ** 2) == 0            # harmonic away from the point source
flux_ok = sp.simplify(4 * sp.pi * r ** 2 * sp.diff(dphi_s, r) - (al_ / MP_) * Mq) == 0   # Gauss: enclosed source (alpha/M_P) M
a5 = sp.simplify(-al_ / MP_ * sp.diff(dphi_s, r)).subs(MP_, 1 / sp.sqrt(8 * sp.pi * Gq))   # fifth-force acceleration -grad ln m (c = 1)
a5_ok = sp.simplify(a5 - (-2 * al_ ** 2 * Gq * Mq / r ** 2)) == 0
# Jordan-frame metric g~ = A^2 g, A = exp(alpha phi/M_P): gamma_PPN
Aq = 1 + al_ * dphi_s.subs(MP_, 1 / sp.sqrt(8 * sp.pi * Gq)) * sp.sqrt(8 * sp.pi * Gq)
g00 = sp.expand(Aq ** 2 * (1 - 2 * Gq * Mq / r))
gxx = sp.expand(Aq ** 2 * (1 + 2 * Gq * Mq / r))
c00 = sp.simplify(sp.diff(g00, Mq).subs(Mq, 0) * r / (-2 * Gq))                        # G_eff/G
cxx = sp.simplify(sp.diff(gxx, Mq).subs(Mq, 0) * r / (2 * Gq))                         # gamma G_eff/G
gam = sp.simplify(cxx / c00)
gam_ok = sp.simplify(gam - (1 - 2 * al_ ** 2) / (1 + 2 * al_ ** 2)) == 0 and sp.simplify(c00 - (1 + 2 * al_ ** 2)) == 0
alpha2 = S_VAL * 1.0 ** 2
gm1 = -4 * alpha2 / (1 + 2 * alpha2)
alpha2_cass = 2.3e-5 / (4 - 2 * 2.3e-5)
check("E4-TIMEFLOW-SOURCED", "if the baryons source the time flow's divergence (m ~ Lambda^beta_b, alpha = beta_b sqrt(s)), the static force is Newtonian in shape: "
      "G_eff = G (1 + 2 alpha^2), a = -2 alpha^2 G M/r^2 extra, and gamma_PPN = (1 - 2 alpha^2)/(1 + 2 alpha^2): the compaction of the time flow by matter gives "
      "M/r^2, never sqrt(G M a0)/r, and with beta_b = 1, s = kappa^2 it fails Cassini by orders of magnitude",
      "Gauss/harmonic: %s/%s; fifth force -2 alpha^2 G M/r^2: %s; gamma form: %s (G_eff/G = %s, gamma = %s); at beta_b = 1, s = %.3f: gamma - 1 = %.3f; Cassini "
      "|gamma - 1| < 2.3e-5 (commonly quoted, from memory) needs alpha^2 < %.2e, i.e. beta_b < %.2e at s = kappa^2"
      % (flux_ok, lap_ok, a5_ok, gam_ok, c00, gam, S_VAL, gm1, alpha2_cass, math.sqrt(alpha2_cass / S_VAL)),
      flux_ok and lap_ok and a5_ok and gam_ok,
      "beta_b is a new constant (G4); linear sourcing of the clock cannot make sqrt(M): the Gauss law is linear in the source for ANY clock kinetic law, "
      "so the MOND form needs a nonlinear constitutive law (section E, DAQ)")
R.num("timeflow_sourced", dict(gamma_minus_1_at_beta1=gm1, alpha2_cassini=alpha2_cass))

# ============================================================================================ D: the relation to a khronon (Note 2, 3i)
R.banner("D  THE VACUUM CURRENT AS A CLOCK FIELD: t_m = d_m tau with tau = -1/(s Lambda); the relation to a khronon")
Xc = sp.symbols('t x y z', real=True)
eta = sp.diag(-1, 1, 1, 1)
s_ = sp.Symbol('s', positive=True)
tau = sp.Function('tau')(*Xc)
Lam_tau = -1 / (s_ * tau)
t_low = [sp.diff(Lam_tau, v) / (s_ * Lam_tau ** 2) for v in Xc]
grad_ok = all(sp.simplify(t_low[i] - sp.diff(tau, Xc[i])) == 0 for i in range(4))
curl_ok = all(sp.simplify(sp.diff(t_low[i], Xc[j]) - sp.diff(t_low[j], Xc[i])) == 0 for i in range(4) for j in range(4))
divt = sum(eta[i, i] * sp.diff(t_low[i], Xc[i]) for i in range(4))
t2 = sum(eta[i, i] * t_low[i] ** 2 for i in range(4))
Pr = sp.Symbol('Pr')
clock_eq = sp.simplify(divt + s_ * Lam_tau * t2 - (sum(eta[i, i] * sp.diff(tau, Xc[i], 2) for i in range(4))
                                                   - sum(eta[i, i] * sp.diff(tau, Xc[i]) ** 2 for i in range(4)) / tau))
# the canonical Lagrangian is NOT invariant under tau -> f(tau) (a khronon's action is): check f(tau) = 2 tau (V = Mp2 Lambda halves)
Mp2s = sp.Symbol('Mp2', positive=True)
phi_tau = sp.sqrt(Mp2s / s_) * sp.log(Lam_tau)
Lcan = lambda ph_, Lm: -sum(eta[i, i] * sp.diff(ph_, Xc[i]) ** 2 for i in range(4)) / 2 - Mp2s * Lm
L1 = Lcan(phi_tau, Lam_tau)
L2 = Lcan(phi_tau.subs(tau, 2 * tau), Lam_tau.subs(tau, 2 * tau))
not_inv = sp.simplify(L2 - L1) != 0
check("E4-KHRONON", "in DYN the vacuum current is exactly the gradient of a clock field, t_m = d_m tau with tau = -1/(s Lambda) (curl-free, hypersurface-orthogonal): the level "
      "sets of the unimodular clock (= of rho_vac) are a PHYSICAL foliation with a khronon-type normal u_m = d_m tau/sqrt(-(d tau)^2); its field equation is "
      "box(tau) - (d tau)^2/tau = 1 - P/rho_vac; unlike a khronon the action is NOT invariant under tau -> f(tau) (the clock's RATE is rho_vac, physical)",
      "t_m = d_m tau: %s; curl-free: %s; clock equation (nabla.t + s Lambda t^2 = box tau - (d tau)^2/tau): %s; action changes under tau -> 2 tau: %s"
      % (grad_ok, curl_ok, clock_eq == 0, not_inv), grad_ok and curl_ok and clock_eq == 0 and not_inv,
      "in HT the same foliation is pure gauge (E1-SPLIT); nothing here couples to u_m, so no preferred-frame effect (G6/G7 vacuous); adding the khronon's "
      "couplings to u_m is door 11C (CFG172), where FC-KH, KM1, KM3 and the V0 region-gate exclusions of the record apply (not run here)")

# ============================================================================================ E: dual-AQUAL scoping (what the MOND form would need)
R.banner("E  SCOPING (DAQ): the MOND form needs baryons coupled to Lambda AND a nonlinear clock law U ~ |t|^(3/2) with a0 put in by hand")
rq, Mq2, bq, u0, rv, Gq2, a0q = sp.symbols('r M beta_b u_0 rho_vac G a_0', positive=True)
t_r = bq * Mq2 / (4 * sp.pi * rv * rq ** 2)                                    # Gauss law, spherical, point mass (c = 1)
gauss_ok = sp.simplify(sp.diff(rq ** 2 * t_r, rq) / rq ** 2) == 0
tsq = sp.Symbol('tsq', positive=True)
Uq = -u0 * tsq ** sp.Rational(3, 4)
Uprime = sp.diff(Uq, tsq).subs(tsq, t_r ** 2)
a_r = 2 * bq * Uprime * t_r / rv                                              # from t: -Mp2 dLambda - 2U' t = 0 and a = -beta_b grad ln Lambda
deep = sp.simplify(a_r * rq / sp.sqrt(Mq2))
deep_ok = sp.simplify(sp.diff(deep, rq)) == 0 and sp.simplify(sp.diff(deep, Mq2)) == 0
u0sol = sp.solve(sp.Eq(-deep, sp.sqrt(Gq2 * a0q)), u0)
u0_expect = sp.Rational(2, 3) * sp.sqrt(4 * sp.pi * Gq2 * a0q) * rv ** sp.Rational(3, 2) / bq ** sp.Rational(3, 2)
u0_ok = len(u0sol) == 1 and sp.simplify(u0sol[0] - u0_expect) == 0
# lensing: a conformally coupled fifth force does not bend light: refractive index of A^2 g is independent of A
Aq2, Ph, Ps = sp.symbols('A Phi Psi', positive=True)
n_g = sp.sqrt((1 - 2 * Ps) / (1 + 2 * Ph))
n_gt = sp.sqrt((Aq2 ** 2 * (1 - 2 * Ps)) / (Aq2 ** 2 * (1 + 2 * Ph)))
lens_ok = sp.simplify(n_gt - n_g) == 0
check("E4-DAQ", "with m ~ Lambda^beta_b and U = -u0 (t^2)^(3/4) the static fifth force is EXACTLY sqrt(G M a0)/r for u0 = (2/3) sqrt(4 pi G a0) rho_vac^(3/2) beta_b^(-3/2) "
      "(c = 1): the MOND form appears only because a0 is written into U; beta_b is a new constant; the interpolation (Newtonian regime) is a further postulated U; "
      "and a conformal coupling bends no light (the refractive index of A^2 g is A-independent), so this boost would be invisible to lensing",
      "Gauss law: %s; a r/sqrt(M) independent of r and M: %s; u0 = %s (matches: %s); lensing index A-independent: %s" % (gauss_ok, deep_ok, u0sol, u0_ok, lens_ok),
      gauss_ok and deep_ok and u0_ok and lens_ok,
      "AQUAL in dual variables (Lambda = the potential, the vacuum current = the displacement field): a restatement (G1 p* at most), G4 FAIL (beta_b), and it fails the "
      "record's lensing standing (the boost is seen in weak lensing; cited from the record, not recomputed here)")
# reported: the cosmic time current turns the local current NULL at r_c (t_r = t^0): the deep regime is cut at r_c
from scipy.integrate import quad as q1
OM, OB = C.OMEGA_M, 0.02237 / 0.6736 ** 2
E_ = lambda a: math.sqrt(OM * a ** -3 + 9.2e-5 * a ** -4 + (1 - OM - 9.2e-5))
t0_L = q1(lambda a: a ** 2 / E_(a), 0, 1)[0] / C.H0 * cs                   # c Int a^3 dt at a = 1, metres  (Gauss law nabla.t = 1)
t_age = q1(lambda a: 1 / (a * E_(a)), 0, 1)[0] / C.H0
a0 = C.A0["canonical"]
base = a0 / (4 * math.pi * Gs * rhoL)                                     # metres
rc_tab = {}
for bb in (1.0, 10.0, 100.0, 1e3, 1e4):
    t0 = t0_L + bb * (OB / C.OMEGA_L) * cs * t_age
    rc_tab["beta_b=%g" % bb] = math.sqrt(bb * base / t0)
ceiling = math.sqrt(base * C.OMEGA_L / (OB * cs * t_age))
check("E4-DAQ-NULL", "embedded in cosmology, the Gauss law makes the background current timelike, t^0 = c Int a^3 dt/a^3 + beta_b (Omega_b/Omega_L) c t_age; the galaxy's "
      "spacelike current t_r = beta_b M/(4 pi rho_vac r^2) equals it at r_c, where the vacuum current turns NULL and a |t|^(3/2) law is singular; outside r_c the "
      "cosmic flow dominates U's argument and the response linearises (no deep regime); r_c/r_M saturates as beta_b -> infinity",
      "r_c/r_M by beta_b: %s; ceiling %.3f (t0_Lambda = %.3e m, t_age = %.3e s)" % ({k: round(v, 3) for k, v in rc_tab.items()}, ceiling, t0_L, t_age),
      ceiling < 30, "so even DAQ cannot give a deep-MOND tail out to 30 r_M once the vacuum current's cosmic time component is included", load_bearing=False)
R.num("DAQ_rc_over_rM", rc_tab); R.num("DAQ_rc_ceiling", ceiling)
# reported: health of the two continuations of |t^2|^(3/4) to the timelike branch (U_QQ > 0 and U_T1T1 < 0 needed, cf. E3-HEALTH)
Q_, T1_, u0p = sp.symbols('Q T1 u0', positive=True)
res_br = {}
for cb in (+1, -1):
    Usp = -u0p * (T1_ ** 2 - Q_ ** 2) ** sp.Rational(3, 4)                        # spacelike branch (T1 > Q)
    Utl = -u0p * cb * (Q_ ** 2 - T1_ ** 2) ** sp.Rational(3, 4)                   # timelike branch continuation
    s_sp = (sp.diff(Usp, Q_, 2).subs({Q_: 0, T1_: 1}), sp.diff(Usp, T1_, 2).subs({Q_: sp.Rational(1, 10**6), T1_: 1}))
    s_tl = (sp.diff(Utl, Q_, 2).subs({T1_: 0, Q_: 1}), sp.diff(Utl, T1_, 2).subs({T1_: 0, Q_: 1}))
    s_sp = tuple(float(sp.N(v.subs(u0p, 1))) for v in s_sp)
    s_tl = tuple(float(sp.N(v.subs(u0p, 1))) for v in s_tl)
    res_br["c=%+d" % cb] = dict(spacelike=(s_sp[0] > 0 and s_sp[1] < 0), timelike=(s_tl[0] > 0 and s_tl[1] < 0), vals=(s_sp, s_tl))
healthy_cont = res_br["c=-1"]["timelike"] and res_br["c=-1"]["spacelike"]
check("E4-DAQ-BRANCH", "of the two continuations of -u0|t^2|^(3/4) to the timelike (cosmological) branch, U = -u0 t^2 |t^2|^(-1/4) is healthy on both branches and the other is a "
      "ghost/gradient-unstable there; either way U'' diverges at t^2 = 0, i.e. at r_c (strong coupling where the current is null)",
      "health (U_QQ > 0, U_T1T1 < 0) by continuation: %s" % {k: dict(spacelike=v["spacelike"], timelike=v["timelike"]) for k, v in res_br.items()},
      healthy_cont and not res_br["c=+1"]["timelike"], load_bearing=False)

P("")
P("  BOTTOM LINE (E4):  the dark energy made dynamical is a clock field whose flow is its kinetic energy; baryons feel it only through gravity, at < 1e-10 of the")
P("  law's boost, with the wrong M and r scaling; letting baryons compact the flow gives a Newtonian-shaped fifth force (Cassini-excluded at beta_b = 1); the MOND")
P("  form needs a0 written into a nonlinear clock law (AQUAL relabelled), a new beta_b, no lensing, and it is cut off where the local current turns null.")
R.finish()
