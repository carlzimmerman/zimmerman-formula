#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B_budget_pincer -- CFG121 tests Q2, B1-B4 and the door-specific gate G1c, exactly as frozen.
Definitions (frozen): continuum |Pi| <= eps_c Q rho_D r (eps_c = 1 central; 0.3, 3 sensitivity); adiabatic tracking omega >= f_track Omega_orb
(f_track = 1 central; 0.3, 3, 10 sensitivity); omega^2 = (Q^2/kappa_I) 4 pi G rho_D / h'(g_N).  F_allow = 0.10.
MUTATE=Q10 : Q = 10 (a G4-violating value)   -> B1 (V_B) must flip toward PASS and the headline G1c cell must change (declared).
Outputs the P_star parameter set (Q*, kappa_I*) used by C_cosmology_growth.py.
"""
import math, sys, json, os
import numpy as np
import cfg121_common as C
from cfg121_common import hfun, dh, G, A0, MASSES, rM_of, target_at, target_for, nu_p2, MUTATE, HERE
from scipy.integrate import solve_ivp

R = C.Report("B_budget_pincer")
QC = 10.0 if MUTATE == "Q10" else 1.0
KAPI = 1.0
FALLOW = 0.10
X = np.geomspace(0.3, 30.0, 121)
R.banner(f"CFG121 B  (footing {C.FOOT}: a0 = {A0:.2f}; Q_central = {QC}, kappa_I = {KAPI}; MUTATE='{MUTATE}')")

RHO_CRIT = 2.775e11 * 0.6736 ** 2 / 1e9           # Msun/kpc^3
OMC = 0.1200 / 0.6736 ** 2
RHO_D_COSMIC200 = 200.0 * OMC * RHO_CRIT


def fields(M, x):
    t = target_at(M, x)
    r, rho, Mc, Mb = t["r"], t["rho"], t["Mc"], t["Mb"]
    y = G * Mb / (r ** 2 * A0)
    hp = dh(nu_p2, y)
    gtot = G * (Mb + Mc) / r ** 2
    Om2 = gtot / r
    return dict(r=r, rho=rho, Mc=Mc, Mb=Mb, y=y, hp=hp, Om2=Om2, gtot=gtot)


# ---------------------------------------------------------------------------------------------- Q2
R.banner("Q2  relaxation: omega/Omega_orb and tau/t_dyn (Q = kappa_I = 1; medium density rho_D = rho_tgt, and the cosmic mean x 200)")
for M in MASSES:
    F = fields(M, X)
    for lab, rhoD in (("rho_D = rho_tgt", F["rho"]), ("rho_D = 200 x Omega_c rho_crit", RHO_D_COSMIC200 * np.ones_like(X))):
        om2 = (QC ** 2 / KAPI) * 4 * math.pi * G * rhoD / F["hp"]
        rat = np.sqrt(om2 / F["Om2"])
        R.P(f"  M_b={M:.0e} {lab:34s}: omega/Omega_orb at x=0.3,1,3,10,30 = " + ", ".join(f"{np.interp(v, X, rat):.3g}" for v in (0.3, 1, 3, 10, 30)))

# ---------------------------------------------------------------------------------------------- B1
R.banner("B1  budget: F_req(x) = M_c/(4 pi eps_c Q r^3 rho_tgt) <= F_allow = 0.10 at every x in [0.3, 30]")
Freq1 = {}
for M in MASSES:
    F = fields(M, X)
    Freq1[M] = F["Mc"] / (4 * math.pi * F["r"] ** 3 * F["rho"])          # = F_req at eps_c Q = 1
    R.P(f"  M_b={M:.0e}: M_c/(4 pi r^3 rho_tgt) (= F_req at eps_c Q = 1): min {Freq1[M].min():.3f}, max {Freq1[M].max():.3f}; at x=0.3,1,3,10,30: "
        + ", ".join(f"{np.interp(v, X, Freq1[M]):.3f}" for v in (0.3, 1, 3, 10, 30)))
b1 = {}
for ec in (0.3, 1.0, 3.0):
    worst = max(float(Freq1[M].max()) / (ec * QC) for M in MASSES)
    b1[ec] = worst
    R.P(f"  eps_c = {ec}: worst F_req over masses and x = {worst:.3f} at Q = {QC}  ->  {'PASS' if worst <= FALLOW else 'FAIL'}")
Qstar_B1 = max(float(Freq1[M].max()) for M in MASSES) / FALLOW           # eps_c = 1
R.P(f"  Q* (eps_c = 1) that makes B1 pass at every mass and x: {Qstar_B1:.2f}   (a new constant unless it equals 1)")
R.verdict("B1_VB", "PASS" if b1[1.0] <= FALLOW else "FAIL", f"eps_c = 1, Q = {QC}: worst F_req = {b1[1.0]:.3f} vs {FALLOW}; Q* = {Qstar_B1:.2f}")
R.num("Qstar_B1", Qstar_B1)

# ---------------------------------------------------------------------------------------------- B2
R.banner("B2  V_U pincer (exact P2): largest M_D/M_c with the TOTAL dark mass within +10% of the target, compared with F_req")


def F_allow_U(Mb, Mc, r):
    k = A0 * r ** 2 / G
    Mt = -k / 2 + np.sqrt(k ** 2 / 4 + (Mb + 1.1 * Mc) ** 2)
    return np.maximum(Mt - Mb, 0.0) / Mc


def F_allow_U_point(M, x):
    r = x * rM_of(M)
    Mc = M * (np.sqrt(1 + x ** 2) - 1)
    return F_allow_U(M, Mc, r)


okB2 = True
Qstar_U = 0.0
for M in MASSES:
    F = fields(M, X)
    fa = F_allow_U(F["Mb"], F["Mc"], F["r"])
    fa_pt = F_allow_U_point(M, X)
    fr = Freq1[M] / (1.0 * QC)
    okB2 &= bool(np.all(fr <= fa))
    with np.errstate(divide="ignore"):
        ratio_pt = Freq1[M] / fa_pt
    Qstar_U = max(Qstar_U, float(np.max(ratio_pt)))
    R.P(f"  M_b={M:.0e}: F_allow_U (exp sphere, vs target) at x=0.3,1,3,10,30: " + ", ".join(f"{np.interp(v, X, fa):.3g}" for v in (0.3, 1, 3, 10, 30))
        + f";  point mass: " + ", ".join(f"{np.interp(v, X, fa_pt):.3g}" for v in (0.3, 1, 3, 10, 30))
        + f";  F_req(Q={QC}): " + ", ".join(f"{np.interp(v, X, fr):.3g}" for v in (0.3, 1, 3, 10, 30)))
Qstar_U = max(Qstar_U, Qstar_B1)
R.P(f"  deep-regime hand estimate: F_allow_U ~ 0.2/x (x = 30 -> 0.0067); Q*_U from the POINT-mass F_allow_U (the exp-sphere F_allow_U is 0 wherever the local P2 phantom already exceeds 1.1 M_c) = {Qstar_U:.1f}")
R.verdict("B2_VU", "PASS" if okB2 else "FAIL", f"F_req <= F_allow_U at every x and mass: {okB2}; Q*_U (point-mass F_allow_U) = {Qstar_U:.1f}")
R.num("Qstar_U", Qstar_U)

# ---------------------------------------------------------------------------------------------- B3
R.banner("B3  adiabatic tracking: rho_track/rho_tgt = f^2 kappa_I h' Omega_orb^2 / (4 pi G Q^2 rho_tgt) <= 0.10;  minimum Q^2/kappa_I")
XB3 = {}
for f_ in (0.3, 1.0, 3.0, 10.0):
    worst_ratio_1 = 0.0
    xmin = 0.0
    for M in MASSES:
        F = fields(M, X)
        rt = f_ ** 2 * KAPI * F["hp"] * F["Om2"] / (4 * math.pi * G * QC ** 2 * F["rho"])       # rho_track/rho_tgt at (Q, kappa_I)
        worst_ratio_1 = max(worst_ratio_1, float(rt.max()))
        xmin = max(xmin, float(np.max(rt * QC ** 2 / KAPI / FALLOW)))
    XB3[f_] = xmin
    R.P(f"  f_track = {f_}: worst rho_track/rho_tgt at (Q, kappa_I) = ({QC}, {KAPI}) = {worst_ratio_1:.3g} ({'PASS' if worst_ratio_1 <= FALLOW else 'FAIL'});  minimum Q^2/kappa_I = {xmin:.3g}")
# deep-regime check: rho_track/rho_tgt ~ f^2 x/2 for Q = kappa_I = 1
F = fields(1e11, X)
rt = F["hp"] * F["Om2"] / (4 * math.pi * G * F["rho"])
R.P(f"  deep-regime check (M_b = 1e11, f = 1, Q = kappa_I = 1): rho_track/rho_tgt at x = 10, 30 = {np.interp(10, X, rt):.2f}, {np.interp(30, X, rt):.2f} (hand: ~ x/2 = 5, 15)")
b3pass = all(float(np.max(fields(M, X)["hp"] * fields(M, X)["Om2"] * 1.0 / (4 * math.pi * G * QC ** 2 * fields(M, X)["rho"]))) <= FALLOW for M in MASSES)
R.verdict("B3", "PASS" if b3pass else "FAIL", f"f = 1, Q = {QC}, kappa_I = 1: {'passes' if b3pass else 'fails'}; minimum Q^2/kappa_I = {XB3[1.0]:.3g} (f = 1), {XB3[0.3]:.3g} (f = 0.3), {XB3[3.0]:.3g} (f = 3)")
R.num("XB3", XB3)

# ---------------------------------------------------------------------------------------------- B4
R.banner("B4  maximal polarised share phi_max(x): M' = 4 pi r^2 rho_tgt - M/(eps_c Q r)")


def phi_max(M, eq):
    t = target_for(M)
    r = t["r"]
    rho, Mc = t["rho"], t["w"] / G
    s = 1.0 / eq

    def rhs(lnr, y):
        rr = math.exp(lnr)
        rh = float(np.exp(np.interp(lnr, np.log(r), np.log(rho))))
        return [rr * (4 * math.pi * rr ** 2 * rh - y[0] / (eq * rr))]
    sol = solve_ivp(rhs, (math.log(r[0]), math.log(r[-1])), [0.0], t_eval=np.log(r), method="Radau", rtol=1e-9, atol=1e-3)
    return r / t["rM"], sol.y[0] / Mc


phi_tab = {}
for eq in (0.3, 1.0, 3.0, 10.0):
    for M in (1e10, 1e12):
        xs, ph = phi_max(M, eq)
        vals = [float(np.interp(v, xs, ph)) for v in (0.1, 0.3, 1, 3, 10, 30, 100)]
        phi_tab[(eq, M)] = vals
        R.P(f"  eps_c Q = {eq:4}, M_b = {M:.0e}: phi_max at x=0.1,0.3,1,3,10,30,100 = " + ", ".join(f"{v:.3f}" for v in vals)
            + f";  closed forms: 1/r regime 2q/(1+2q) = {2 * eq / (1 + 2 * eq):.3f}, 1/r^2 (deep) regime q/(1+q) = {eq / (1 + eq):.3f}")
R.P("  NOTE (my frozen text quoted only the 1/r-regime closed form): rho_tgt ~ 1/r for x << 1 but ~ 1/r^2 for x >> 1 (flat rotation curve), where the closed form is q/(1+q).")
R.num("phi_max", {f"{k[0]}_{k[1]:.0e}": v for k, v in phi_tab.items()})
R.verdict("B4", "FAIL" if phi_tab[(1.0, 1e12)][5] < 0.9 else "PASS", f"at eps_c Q = 1 the polarisation can carry at most phi = {phi_tab[(1.0, 1e12)][4]:.2f} (x = 10), {phi_tab[(1.0, 1e12)][5]:.2f} (x = 30) of the enclosed target; the rest must be a real cold fluid with its own closure (Gap 2 relocated, not removed)")

# ---------------------------------------------------------------------------------------------- G1c and P_star
R.banner("G1c  the medium is self-consistent: PASS only if B1, B2, B3 all pass at Q = kappa_I = 1 (central), eps_c <= 1, f_track >= 1")
b1ok = b1[1.0] <= FALLOW
R.verdict("G1c_VB", "PASS" if (b1ok and b3pass) else "FAIL", f"V_B needs B1 and B3: B1 {'pass' if b1ok else 'fail'}, B3 {'pass' if b3pass else 'fail'}")
R.verdict("G1c_VU", "PASS" if (b1ok and b3pass and okB2) else "FAIL", f"V_U needs B1, B2, B3: B2 {'pass' if okB2 else 'fail'}")
Qs_B = Qstar_B1
Qs_U = Qstar_U
kap_B = min(1.0, Qs_B ** 2 / XB3[1.0])
kap_U = min(1.0, Qs_U ** 2 / XB3[1.0])
Pstar = {"V_B": {"Q": Qs_B, "kappa_I": kap_B}, "V_U": {"Q": Qs_U, "kappa_I": kap_U}, "central": {"Q": 1.0, "kappa_I": 1.0}}
R.P(f"  P_star (used by G2): V_B: Q* = {Qs_B:.2f}, kappa_I* = min(1, Q*^2/(Q^2/kappa_I)_min) = {kap_B:.3g};  V_U: Q* = {Qs_U:.1f}, kappa_I* = {kap_U:.3g}   (any Q* != 1 or kappa_I* != 1 is a new constant: G4 FAIL)")
R.num("Pstar", Pstar)
R.finish(required_change=["B1_VB", "G1c_VB"] if MUTATE == "Q10" else None)
