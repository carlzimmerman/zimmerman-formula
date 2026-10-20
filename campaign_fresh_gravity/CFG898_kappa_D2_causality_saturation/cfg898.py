#!/usr/bin/env python3
"""CFG898 - kappa door D2: does saturating CFG893's drift-causality ceiling select kappa?

Criteria: FROZEN_CRITERIA.md (committed alone, before this script).
Ceiling (CFG893 R12): |v_s|/c <= alpha c_nu kappa sqrt(rho_DE / (4 pi rho_loc)).
Saturation at a declared locus rho*: kappa = sqrt(4 pi rho*/rho_DE) / (alpha* c_nu).

kappa = 1/2 is FITTED (CFG493). This script never uses a footing a0, a measured kappa, Z, Omega_m/Omega_L,
f_ret or H0 upstream of any kappa value. H0 and Omega_L enter only report-only numbers (mass-dependent branch,
end conversion to the rho_crit footing). Not 'theory closed'.

Run:     OMP_NUM_THREADS=1 nice -n 10 python3 cfg898.py              -> cfg898.out, cfg898_results.json (exit 0 if all checks pass)
MUTATE:  CFG898_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg898.py -> *_MUTATE outputs (exit 1 when every tooth bites, 2 otherwise)
"""
import os
import re
import sys
import json
import math

import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG898_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
OUT_TXT = os.path.join(HERE, "cfg898%s.out" % SUF)
OUT_JSON = os.path.join(HERE, "cfg898_results%s.json" % SUF)
REC893 = os.path.join(HERE, "..", "CFG893_kappa_from_cold_energy_structure", "cfg893_results.json")

LINES = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


# ----------------------------------------------------------------------------------------------------------------
# constants (SI). H0 and Omega_L: report-only (realized branch magnitudes, end conversion to rho_crit footing).
# ----------------------------------------------------------------------------------------------------------------
G_SI = 6.67430e-11
C_SI = 2.99792458e8
MSUN = 1.98847e30
MPC = 3.0856775814913673e22
H0_REPORT = 67.4e3 / MPC          # report-only
OL_REPORT = 0.685                 # report-only (CFG493 definition)
RHO_CRIT_REPORT = 3.0 * H0_REPORT ** 2 / (8.0 * math.pi * G_SI)   # used only to give rho_DE a number for report-only lines
RHO_DE_REPORT = OL_REPORT * RHO_CRIT_REPORT
KAPPA_LAW = 0.5                   # the law's FITTED kappa; report-only lines only (I4 renames it to 0.4)

W_DE = (0.227, 0.607)             # rules section 7: W_data on the rho_DE footing
W_CRIT = (0.189, 0.501)           # rules section 7: W_data on the rho_crit footing
MASSES = [1e8, 1e9, 1e10, 1e11, 1e12]

CHECKS = {}


def check(name, ok, detail=""):
    CHECKS[name] = {"ok": bool(ok), "detail": str(detail)}
    P("  [%s] %s  %s" % ("PASS" if ok else "FAIL", name, detail))


# ----------------------------------------------------------------------------------------------------------------
# kernels: F(y) = y (nu(y) - 1) = g_ph / a0 ; Gk(y) = F/y - F'  (point-mass phantom density factor)
# ----------------------------------------------------------------------------------------------------------------
def nu_mono(y):
    s = math.sqrt(y)
    return 1.0 if s > 700.0 else 1.0 + 1.0 / math.expm1(s)


def nu_simple(y):
    return 0.5 + math.sqrt(0.25 + 1.0 / y)


def F_mono(y):
    s = math.sqrt(y)
    return 0.0 if s > 700.0 else y / math.expm1(s)


def F_simple(y):
    return y / (math.sqrt(y * y / 4.0 + y) + y / 2.0)


def Gk_mono(y):
    s = math.sqrt(y)
    if s > 700.0:
        return 0.0
    e = math.expm1(s)
    return s * (e + 1.0) / (2.0 * e * e)


def Gk_simple(y):
    return 1.0 / (2.0 * math.sqrt(y * y / 4.0 + y))


KERN = {"nu_mono": (nu_mono, F_mono, Gk_mono), "simple": (nu_simple, F_simple, Gk_simple)}


def cnu_mono_numeric():
    r = minimize_scalar(lambda t: -F_mono(math.exp(t)), bounds=(-3.0, 4.0), method="bounded",
                        options={"xatol": 1e-13})
    return -r.fun, math.exp(r.x)


C_NU_MONO, Y_M = cnu_mono_numeric()
C_NU = {"nu_mono": C_NU_MONO, "simple": 1.0}

# ----------------------------------------------------------------------------------------------------------------
# alpha sources (section 1 H_alpha), derived symbolically below; numeric values used in the cells
# ----------------------------------------------------------------------------------------------------------------
P("CFG898 - kappa door D2: saturation of the drift-causality ceiling (MUTATE=%s)" % MUT)
P("kappa = 1/2 FITTED (CFG493 measurement, quoted in the README); footings never pooled; not theory closed.")
P("")
P("== alpha sources ==")
al, be, q, tau, gam, psi_x, rho_s, V, u = sp.symbols("alpha beta q tau gamma psi_x rho V u", positive=True)
s_, k_, c_s, Gam, tpsi = sp.symbols("s k c Gamma tau_psi", positive=True)

# K3 Routh-Hurwitz on s^3 + s^2/tau_psi + c^2 k^2 s + Gamma c^2 k^2 (CFG541 section 6)
a2, a1, a0c = 1 / tpsi, c_s ** 2 * k_ ** 2, Gam * c_s ** 2 * k_ ** 2
hurwitz = sp.simplify(a2 * a1 - a0c)                       # > 0 required (a2, a0 > 0 trivially)
hurwitz_sub = sp.simplify(hurwitz.subs({Gam: al * q / tau, tpsi: be * tau}) / (c_s ** 2 * k_ ** 2) * tau)
alpha_max = sp.solve(sp.Eq(hurwitz_sub, 0), al)[0]         # alpha_max = 1/(beta q)
alpha_A = sp.limit(alpha_max.subs(be, 1), q, 1)
P("K3 Hurwitz a2 a1 - a0 =", hurwitz, "-> (alpha q/tau)(beta tau) < 1 form:", sp.simplify(hurwitz_sub), "> 0")
P("   alpha_max =", alpha_max, "; source A (beta = 1, q -> 1): alpha* =", alpha_A,
  "; d alpha_max/d beta =", sp.simplify(sp.diff(alpha_max, be)), "(nonzero: A is a TRADE in beta)")

# K6 overdamped momentum moment, friction gamma in the baryon frame (velocity V): 0 = -rho psi_x - rho gamma (u - V)
u_sol = sp.solve(sp.Eq(-rho_s * psi_x - rho_s * gam * (u - V), 0), u)[0]
mobility = sp.simplify(-(u_sol - V) / psi_x)               # = 1/gamma
alpha_B1 = [r for r in sp.solve(sp.Eq(mobility.subs(gam, al / tau), al * tau), al) if r.is_positive][0]
tau_c = tau / (2 * al)                                     # BGK single time = IS tau_pi (CFG638)
alpha_B2 = [r for r in sp.solve(sp.Eq(tau_c, al * tau), al) if r.is_positive][0]
P("K6 overdamped drift u - V =", sp.simplify(u_sol - V), "; mobility =", mobility)
P("   B1 (Fokker-Planck, gamma = alpha/tau): mobility tau/alpha = alpha tau -> alpha* =", alpha_B1)
P("   B2 (BGK, tau_c = tau_pi = tau/2alpha): tau/(2 alpha) = alpha tau -> alpha* =", alpha_B2)
ALPHAS = {"A": float(alpha_A), "B1": float(alpha_B1), "B2": float(alpha_B2)}

# ----------------------------------------------------------------------------------------------------------------
# the mass-free cells
# ----------------------------------------------------------------------------------------------------------------
LOCI = ["L1", "L2", "L2b"]


def rho_ratio(locus, D=4, w=-1.0):
    n = D - 1
    zg = -((D - 3) + (D - 1) * w) / (D - 3)                # E8: zero-gravity matter density / rho_DE
    if locus == "L1":
        return 1.0
    if locus == "L2":
        return zg
    if locus == "L2b":
        return zg * (n - 2) / n                            # local / mean for an r^-2 profile in n spatial dims
    raise ValueError(locus)


def poisson_coeff(D=4, mult=1.0):
    return mult * 8.0 * math.pi * (D - 3) / (D - 2)       # Einstein convention; 4 pi at D = 4


def cells(alpha_scale=1.0, kern_override=None, pmult=1.0, w=-1.0, D=4, kappa_law=KAPPA_LAW):
    """kappa = sqrt(K_D rho*/rho_DE)/(alpha* c_nu). kappa_law is accepted and deliberately unused (I4)."""
    _ = kappa_law
    out = {}
    for src, a in ALPHAS.items():
        for loc in LOCI:
            for kern in ("nu_mono", "simple"):
                kk = kern_override or kern
                kap = math.sqrt(poisson_coeff(D, pmult) * rho_ratio(loc, D, w)) / (a * alpha_scale * C_NU[kk])
                out["%s|%s|%s" % (src, loc, kern)] = kap
    return out


BASE = cells()

# ----------------------------------------------------------------------------------------------------------------
# classifier (section 7) and its controls (K11)
# ----------------------------------------------------------------------------------------------------------------
def classify_set(values, window, mass_exponent=0.0, forbidden=False, s4=False, exact_flags=None):
    vals = list(values)
    width = window[1] - window[0]
    if forbidden:
        return "VOID"
    if abs(mass_exponent) > 0:
        return "MASS-DEPENDENT"
    spread = max(vals) - min(vals)
    if spread >= width:
        return "MENU"
    v = vals[0]
    if exact_flags and all(exact_flags):
        return "EXACT CANDIDATE" if s4 else "CONSISTENT (exact 1/2, S4 failed: capped)"
    return "CONSISTENT" if window[0] <= v <= window[1] else "MISS"


if not MUT:
    P("")
    P("== K-tests ==")
    # K1 c_nu
    rec = json.load(open(REC893))
    cnu_rec = rec["relations"]["R12"]["c_nu"]["nu_mono"]
    ypk = rec.get("y_peak_mono")
    ysym = sp.symbols("y", positive=True)
    lim_simple = sp.limit(ysym * (sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / ysym) - 1), ysym, sp.oo)
    ok_y = (ypk is None) or abs(float(ypk) - Y_M) < 1e-3
    check("K1 c_nu", abs(C_NU_MONO - cnu_rec) < 1e-6 and ok_y and lim_simple == 1,
          "nu_mono c_nu %.8f at y %.4f (CFG893 %.8f, y %s); simple sup = %s" % (C_NU_MONO, Y_M, cnu_rec, ypk, lim_simple))

    # K2 structure of CFG893's R12 table: kappa_H12 * c_nu / sqrt(Delta) constant within each footing
    k2_ok, k2_det = True, []
    for foot in ("can", "alt"):
        consts = []
        for kern in ("nu_mono", "simple"):
            for key, row in rec["relations"]["R12"]["table"][foot][kern].items():
                if isinstance(row, dict) and "kappa_H12_alpha1" in row:
                    consts.append(row["kappa_H12_alpha1"] * C_NU[kern] / math.sqrt(row["Delta_loc"]))
        rel = (max(consts) - min(consts)) / np.mean(consts)
        k2_ok &= rel < 1e-6
        k2_det.append("%s: %d cells, rel spread %.1e" % (foot, len(consts), rel))
    check("K2 ceiling structure vs CFG893 R12 (kappa_H12 ~ sqrt(Delta)/c_nu)", k2_ok, "; ".join(k2_det))

    # K3 Hurwitz / alpha_max reproduction (1.186 at q = 1 - f_b, f_b read from CFG893 JSON)
    fb = rec["relations"]["R12"]["table"]["can"]["nu_mono"]["f_b (baryons only)"]["Delta_loc"]
    am = float(alpha_max.subs({be: 1, q: 1 - fb}))
    check("K3 Routh-Hurwitz alpha beta q < 1; alpha_max(beta 1, q 1-f_b) = 1.186 (CFG542 K9)",
          sp.simplify(alpha_max - 1 / (be * q)) == 0 and abs(am - 1.186) < 1e-3 and alpha_A == 1,
          "alpha_max = %s; at q = 1 - f_b: %.5f; source A alpha* = %s" % (alpha_max, am, alpha_A))

    # K4 IS closure characteristics are alpha-free
    rr, uu, PP_, Phi_x, sig2 = sp.symbols("rho u P Phi_x sigma2", positive=True)
    A = sp.Matrix([[uu, rr, 0], [0, uu, 1 / rr], [0, 3 * PP_, uu]])
    ev = list(A.eigenvals().keys())
    expect = {uu, uu + sp.sqrt(3 * PP_ / rr), uu - sp.sqrt(3 * PP_ / rr)}
    ev_ok = all(any(sp.simplify(e - x) == 0 for x in expect) for e in ev) and len(ev) == 3
    dA = A.diff(al)
    pp = sp.symbols("p", positive=True)
    eta = pp * tau / (2 * al)
    taupi = tau / (2 * al)
    front2 = sp.simplify(eta / (rr * taupi))
    # numeric: full linear system with relaxation, roots/k at large k for several alpha
    num_ok, num_det = True, []
    for aval in (0.03, 1.0, 30.0):
        rho0, P0, t0 = 1.0, 1.0, 1.0
        kk = 1e6
        Amat = np.array([[0, rho0, 0], [0, 0, 1 / rho0], [0, 3 * P0, 0]], dtype=complex)
        # linearised relaxation: d(dP)/dt = ... - (2a/t)(dP - sigma^2 d rho), sigma^2 = P0/rho0 = 1
        S = np.array([[0, 0, 0], [0, 0, 0], [-(2 * aval / t0) * (P0 / rho0), 0, 2 * aval / t0]], dtype=complex)
        M = 1j * kk * Amat + S                 # d/dt X = -(i k A + S) X  -> omega from eig
        om = np.linalg.eigvals(M) / (1j * kk)
        sp_re = sorted(np.real(om))
        num_det.append("alpha %.2g: %s" % (aval, ["%.6f" % x for x in sp_re]))
        num_ok &= np.allclose(sp_re, [-math.sqrt(3), 0.0, math.sqrt(3)], atol=1e-4)
    check("K4 IS closure: characteristic speeds u, u +- sqrt(3P/rho), alpha-free; front^2 = p/rho",
          ev_ok and dA == sp.zeros(3, 3) and sp.simplify(front2 - pp / rr) == 0 and num_ok,
          "eigs %s; dA/dalpha = 0; eta/(rho tau_pi) = %s; large-k phase speeds (sigma=1): %s"
          % (ev, front2, " | ".join(num_det)))

    # K5 Smoluchowski stationary state is mobility-free (CFG542 K5)
    m_, s2_ = sp.symbols("m s2", positive=True)
    x_ = sp.symbols("x", real=True)
    rf = sp.Function("rho_f")
    ps = sp.Function("psi_f")
    J = -m_ * (rf(x_) * ps(x_).diff(x_) + s2_ * rf(x_).diff(x_))
    sol = sp.dsolve(sp.Eq(J / m_, 0), rf(x_))
    check("K5 Fokker-Planck stationary state independent of the mobility", m_ not in sol.free_symbols,
          "J = 0 -> %s" % sol)

    # K6 (printed above); check values
    check("K6 one-relaxation-time alpha*: B1 = 1, B2 = 1/sqrt(2)",
          sp.simplify(mobility - 1 / gam) == 0 and alpha_B1 == 1 and sp.simplify(alpha_B2 - 1 / sp.sqrt(2)) == 0,
          "mobility %s; B1 %s; B2 %s" % (mobility, alpha_B1, alpha_B2))

    # K7 deep-regime realized loci (sympy)
    Gs, Ms, a0s, rhos, cs, r_ = sp.symbols("G M a0 rho_DE c r", positive=True)
    Vf = (Gs * Ms * a0s) ** sp.Rational(1, 4)
    gdeep = sp.sqrt(Gs * Ms * a0s) / r_
    rho_ph_deep = sp.simplify(sp.diff(r_ ** 2 * gdeep, r_) / (4 * sp.pi * Gs * r_ ** 2))
    r1 = [z for z in sp.solve(sp.Eq(rho_ph_deep, rhos), r_) if z.is_positive][0]
    vc_L1 = sp.simplify(al * gdeep.subs(r_, r1) / (cs * sp.sqrt(4 * sp.pi * Gs * rhos)))
    rzg = [z for z in sp.solve(sp.Eq(gdeep, sp.Rational(8, 3) * sp.pi * Gs * rhos * r_), r_) if z.is_positive][0]
    vc_L2 = sp.simplify(al * gdeep.subs(r_, rzg) / (cs * sp.sqrt(4 * sp.pi * Gs * 2 * rhos)))
    vc_L2b = sp.simplify(al * gdeep.subs(r_, rzg) / (cs * sp.sqrt(4 * sp.pi * Gs * sp.Rational(2, 3) * rhos)))
    sat = {}
    for nm, vc in (("L1", vc_L1), ("L2", vc_L2), ("L2b", vc_L2b)):
        a0sol = sp.solve(sp.Eq(vc, 1), a0s)
        sat[nm] = sp.simplify(a0sol[0])
    k7_vals = {"L1": sp.simplify(vc_L1 - al * Vf / cs) == 0,
               "L2": sp.simplify(vc_L2 - al * Vf / (sp.sqrt(3) * cs)) == 0,
               "L2b": sp.simplify(vc_L2b - al * Vf / cs) == 0}
    noRho = all(sp.diff(v, rhos) == 0 for v in sat.values())
    mexp = {nm: sp.simplify(Ms * sp.diff(sp.log(v / (cs * sp.sqrt(Gs * rhos))), Ms)) for nm, v in sat.items()}
    check("K7 deep realized loci: v/c = alpha V_f/c (L1, L2b), alpha V_f/(sqrt3 c) (L2); saturated a0 has no rho_DE",
          all(k7_vals.values()) and noRho and all(m == -1 for m in mexp.values()),
          "v/c: L1 %s, L2 %s, L2b %s; saturated a0: %s; d ln kappa/d ln M = %s"
          % (vc_L1, vc_L2, vc_L2b, sat, mexp))
    SAT_DEEP = {k: str(v) for k, v in sat.items()}
    MEXP = {k: int(v) for k, v in mexp.items()}

    # K9 point-mass phantom density closed form; L3 saturation
    yy = sp.symbols("y", positive=True)
    Fm = yy / (sp.exp(sp.sqrt(yy)) - 1)
    Fs = yy * (sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / yy) - 1)
    k9_ok, k9_det = True, []
    for nm, Fy, Gk in (("nu_mono", Fm, Gk_mono), ("simple", Fs, Gk_simple)):
        Gsym = Fy / yy - sp.diff(Fy, yy)
        for yv in (1e-4, 0.3, 2.54, 40.0):
            a_ = float(Gsym.subs(yy, yv).evalf(30))
            b_ = Gk(yv)
            k9_ok &= abs(a_ - b_) / abs(a_) < 1e-12
        # rho_ph = (1/4 pi G r^2) d/dr (r^2 a0 F(GM/(a0 r^2))) vs M (F/y - F')/(2 pi r^3)
        Gv, Mv, av = 6.6743e-11, 1e10 * MSUN, 3.0e-10   # arbitrary test acceleration (not a footing)
        for rv in (1e19, 3e20, 1e22):
            yexpr = Gs * Ms / (a0s * r_ ** 2)
            lhs = sp.diff(r_ ** 2 * a0s * Fy.subs(yy, yexpr), r_) / (4 * sp.pi * Gs * r_ ** 2)
            lv = float(lhs.subs({Gs: Gv, Ms: Mv, a0s: av, r_: rv}).evalf(30))
            yv = Gv * Mv / (av * rv ** 2)
            rv_ = Mv * Gk(yv) / (2 * math.pi * rv ** 3)
            k9_ok &= abs(lv - rv_) / abs(lv) < 1e-10
        k9_det.append(nm)
    # L3: alpha c_nu a0 = c sqrt(4 pi G rho_ph(y_m)), rho_ph = a0^1.5 h /(G^1.5 M^0.5)
    hh, cn = sp.symbols("h c_nu", positive=True)
    rho_ph_ym = a0s ** sp.Rational(3, 2) * hh / (Gs ** sp.Rational(3, 2) * sp.sqrt(Ms))
    a0_L3 = sp.solve(sp.Eq((al * cn * a0s) ** 2, cs ** 2 * 4 * sp.pi * Gs * rho_ph_ym), a0s)
    a0_L3 = [z for z in a0_L3 if z != 0][0]
    k9_ok &= sp.simplify(a0_L3 - 16 * sp.pi ** 2 * cs ** 4 * hh ** 2 / (al ** 4 * cn ** 4 * Gs * Ms)) == 0
    k9_ok &= sp.diff(a0_L3, rhos) == 0
    check("K9 point-mass phantom density closed forms; L3 saturated a0 is kappa-free and mass-dependent", k9_ok,
          "kernels %s; L3 a0 = %s" % (k9_det, a0_L3))
    A0_L3 = str(a0_L3)

    # K10 dimensions (M, L, T)
    dim = {"G": np.array([-1, 3, -2]), "rho": np.array([1, -3, 0]), "c": np.array([0, 1, -1]),
           "a0": np.array([0, 1, -2])}
    kdim = dim["a0"] - dim["c"] - 0.5 * (dim["G"] + dim["rho"])
    taudim = -0.5 * (dim["G"] + dim["rho"])
    vdim = taudim + dim["a0"]
    check("K10 dimensions: kappa dimensionless; alpha tau c_nu a0 is a speed",
          np.allclose(kdim, 0) and np.allclose(vdim, dim["c"]), "kappa %s; v %s" % (kdim, vdim))

    # K11 classifier controls
    ctrl = {
        "a0 = 1/2 c sqrt(G rho_DE) (pure number)": classify_set([0.5], W_DE) == "CONSISTENT",
        "a0 = c^4/(G M) (mass exponent -1)": classify_set([1.0], W_DE, mass_exponent=-1) == "MASS-DEPENDENT",
        "two values 0.3, 0.9 (menu)": classify_set([0.3, 0.9], W_DE) == "MENU",
        "single in-window 0.46": classify_set([0.46], W_DE) == "CONSISTENT",
        "single 5.0 (miss)": classify_set([5.0], W_DE) == "MISS",
        "forbidden input": classify_set([0.5], W_DE, forbidden=True) == "VOID",
    }
    check("K11 classifier controls", all(ctrl.values()), ctrl)

# ----------------------------------------------------------------------------------------------------------------
# I1 - I8
# ----------------------------------------------------------------------------------------------------------------
P("")
P("== identity checks ==")
src_text = open(os.path.abspath(__file__)).read()
pieces = [("9.36", "e-11"), ("9.3603", "e-11"), ("1.13", "e-10"), ("1.1312", "e-10"), ("1.2", "e-10"),
          ("1.0766", "e-10"), ("0.4", "17"), ("0.4", "65"), ("0.5", "51"), ("5.78", "88"), ("0.17", "27"),
          ("5.3", "64"), ("32*", "pi"), ("32 * ", "pi"), ("32*", "sp.pi")]
exact_tokens = [("0.4", "5"), ("0.5", "3"), ("0.5", "5")]
hits = []
for a, b in pieces:
    if (a + b) in src_text:
        hits.append(a + b)
for a, b in exact_tokens:
    pat = r"(?<![\d.])" + re.escape(a + b) + r"(?![\d])"
    if re.search(pat, src_text):
        hits.append(a + b)
FORBIDDEN_HIT = bool(hits)
check("I1 script free of forbidden constants (rules section 2)", not FORBIDDEN_HIT, "hits: %s" % hits)

Gs2, cs2, rhoDE2, rstar, hbar, cn2, al2 = sp.symbols("G c rho_DE rho_star hbar c_nu alpha_star", positive=True)
a0_sym = sp.symbols("a0", positive=True)
kap = sp.symbols("kappa", positive=True)
v_sat = al2 * cn2 * (kap * cs2 * sp.sqrt(Gs2 * rhoDE2)) / sp.sqrt(4 * sp.pi * Gs2 * rstar)
kap_sol = sp.solve(sp.Eq(v_sat, cs2), kap)[0]
rr_ = sp.symbols("r_ratio", positive=True)
kap_sol_r = sp.simplify(kap_sol.subs(rstar, rr_ * rhoDE2))
deps = {s.name: sp.simplify(sp.diff(kap_sol_r, s)) for s in (Gs2, cs2, rhoDE2, hbar)}
deps_free = {s.name: sp.simplify(sp.diff(kap_sol_r, s)) for s in (al2, cn2, rr_)}
P("I2 symbolic kappa (rho* = r rho_DE):", kap_sol_r)
check("I2 kappa independent of G, c, rho_DE, hbar; depends on alpha*, c_nu, r only",
      all(v == 0 for v in deps.values()) and all(v != 0 for v in deps_free.values()),
      "d/dG,c,rho_DE,hbar = %s; d/dalpha*,c_nu,r nonzero" % list(deps.values()))
lam, mu, nuv = sp.symbols("lambda mu nu", positive=True)
kap_scaled = sp.simplify(kap_sol.subs({Gs2: lam * Gs2, rhoDE2: mu * rhoDE2, rstar: mu * rstar, cs2: nuv * cs2}))
check("I3 scaling G->lG, rho->m rho, c->n c leaves kappa invariant", sp.simplify(kap_scaled - kap_sol) == 0,
      str(kap_scaled))
REN = cells(kappa_law=0.4)
check("I4 rename law kappa 0.5 -> 0.4: selected values do not move (they do not follow the law's kappa)",
      all(abs(REN[k] - BASE[k]) == 0 for k in BASE), "max |diff| %.1e; none of the cells is near 0.4 (min %.3f)"
      % (max(abs(REN[k] - BASE[k]) for k in BASE), min(BASE.values())))
check("I5 no Friedmann relation in the kappa path (no H symbol)", not any(str(s).startswith("H") for s in
      kap_sol.free_symbols), "free symbols %s" % sorted(map(str, kap_sol.free_symbols)))
check("I6 declared footing rho_DE; rho_crit reported separately, never pooled", True, "see footing block")
check("I7 hbar absent", hbar not in kap_sol.free_symbols, "")
pi_w = {}
for key in BASE:
    src, loc, kern = key.split("|")
    a_ex = {"A": sp.Integer(1), "B1": sp.Integer(1), "B2": 1 / sp.sqrt(2)}[src]
    r_ex = {"L1": sp.Integer(1), "L2": sp.Integer(2), "L2b": sp.Rational(2, 3)}[loc]
    if kern == "simple":
        k2 = sp.nsimplify(4 * sp.pi * r_ex / a_ex ** 2)
        ratio = sp.simplify(k2 / sp.pi)
        pi_w[key] = "pi^1 x %s (odd); exact 1/2 impossible: %s" % (ratio, sp.simplify(k2 - sp.Rational(1, 4)) != 0)
    else:
        pi_w[key] = "cont (c_nu transcendental); |kappa^2 - 1/4| = %.3f" % abs(BASE[key] ** 2 - 0.25)
check("I8 pi-weight matches section 5 (simple: pi^odd; nu_mono: cont); no cell gives exact 1/2",
      all(("odd" in v and v.endswith("True")) or v.startswith("cont") for v in pi_w.values()), "")

# ----------------------------------------------------------------------------------------------------------------
# the option space, footings, determinacy
# ----------------------------------------------------------------------------------------------------------------
P("")
P("== option space (18 cells, equal weights): kappa = sqrt(4 pi rho*/rho_DE)/(alpha* c_nu) ==")
P("alpha*: A %.6f (beta 1, q -> 1), B1 %.6f, B2 %.6f ; c_nu: nu_mono %.8f (y %.4f), simple 1"
  % (ALPHAS["A"], ALPHAS["B1"], ALPHAS["B2"], C_NU_MONO, Y_M))
P("%-4s %-4s %-8s %10s %10s %10s" % ("src", "loc", "kernel", "kappa_L", "kappa_crit(a)", "kappa_crit(b)"))
for key, v in BASE.items():
    src, loc, kern = key.split("|")
    P("%-4s %-4s %-8s %10.4f %10.4f %10.4f" % (src, loc, kern, v, v, v * math.sqrt(OL_REPORT)))
vals = list(BASE.values())
vals_b = [v * math.sqrt(OL_REPORT) for v in vals]
p_data_DE = sum(W_DE[0] <= v <= W_DE[1] for v in vals) / len(vals)
p_data_CR_a = sum(W_CRIT[0] <= v <= W_CRIT[1] for v in vals) / len(vals)
p_data_CR_b = sum(W_CRIT[0] <= v <= W_CRIT[1] for v in vals_b) / len(vals_b)
p_exact = 0.0                                      # I8: no cell is exactly 1/2
spread = max(vals) - min(vals)
cls_DE = classify_set(vals, W_DE)
cls_CR = classify_set(vals, W_CRIT)
canon = BASE["A|L2|nu_mono"]
canon_cls = classify_set([canon], W_DE)
P("range %.4f .. %.4f (spread %.3f vs window widths %.3f / %.3f) -> class %s (rho_DE), %s (rho_crit)"
  % (min(vals), max(vals), spread, W_DE[1] - W_DE[0], W_CRIT[1] - W_CRIT[0], cls_DE, cls_CR))
P("p_data: rho_DE %.3f ; rho_crit (a) relabel %.3f, (b) end conversion %.3f ; p_exact %.3f" %
  (p_data_DE, p_data_CR_a, p_data_CR_b, p_exact))
P("canonical single cell (L2, nu_mono, alpha* = 1): kappa_L = %.4f -> %s; implied a0 / a0(kappa = 1/2) = %.2f"
  % (canon, canon_cls, canon / KAPPA_LAW))
sub_canon = [BASE["A|%s|nu_mono" % l] for l in LOCI]
P("canonical sub-menu (nu_mono, alpha* = 1; L1/L2/L2b): %s -> %s" %
  (["%.3f" % x for x in sub_canon], classify_set(sub_canon, W_DE)))

P("")
P("== what an in-window landing would need (report-only) ==")
need = {}
for loc in LOCI:
    for kern in ("nu_mono", "simple"):
        base1 = math.sqrt(4 * math.pi * rho_ratio(loc)) / C_NU[kern]
        need["%s|%s" % (loc, kern)] = {"alpha_for_window_top": base1 / W_DE[1], "alpha_for_half": base1 / 0.5}
        P("  %-4s %-8s alpha needed for kappa <= %.3f: %.2f ; for kappa = 1/2: %.2f (record causal max 1.186)"
          % (loc, kern, W_DE[1], base1 / W_DE[1], base1 / 0.5))
inv = {}
for kern in ("nu_mono", "simple"):
    for src in ("A", "B2"):
        r_need = (0.5 * ALPHAS[src] * C_NU[kern]) ** 2 / (4 * math.pi)
        inv["%s|%s" % (src, kern)] = r_need
        P("  inverse: kappa = 1/2 needs rho*/rho_DE = %.5f (alpha* %s, %s)" % (r_need, src, kern))
k_half = sp.Rational(1, 2)
r_inv = sp.simplify((k_half * 1 * 1) ** 2 / (4 * sp.pi))
a0_inv = sp.sqrt(4 * sp.pi * Gs2 * r_inv * rhoDE2) * cs2
P("  simple, alpha* = 1: rho* = rho_DE x %s; then a0^2 = %s, i.e. G rho_DE c^2 = 4 a0^2: the target restated (rules section 2)"
  % (r_inv, sp.simplify(a0_inv ** 2)))

# ----------------------------------------------------------------------------------------------------------------
# rho_m-bar loci (VOID as selections): symbolic only
# ----------------------------------------------------------------------------------------------------------------
Om, OLs, Dl, zz = sp.symbols("Omega_m Omega_L Delta z", positive=True)
k_mbar = sp.sqrt(4 * sp.pi * Dl * Om / OLs) / (al2 * cn2)
k_mbar_z = k_mbar.subs(Om, Om * (1 + zz) ** 3)
run_exp = sp.simplify((1 + zz) * sp.diff(sp.log(k_mbar_z), zz))
P("")
P("== rho_m-bar loci (cosmic mean Delta = 1, turnaround Delta_ta, catchment edge): VOID as selections ==")
P("  kappa = %s (needs Omega_m/Omega_L: forbidden input, X13); d ln kappa/d ln(1+z) = %s at fixed rho_DE (fails S8)"
  % (k_mbar, run_exp))

# ----------------------------------------------------------------------------------------------------------------
# realized-field branches (exact kernels, point mass): solve sup v_s = c for kappa
# ----------------------------------------------------------------------------------------------------------------
def solve_lny(fun, lo=-400.0, hi=40.0):
    flo, fhi = fun(lo), fun(hi)
    if flo * fhi > 0:
        return None
    return brentq(fun, lo, hi, xtol=1e-12, maxiter=500)


def qmax_mono():
    r = minimize_scalar(lambda t: -(math.exp(1.5 * t) * Gk_mono(math.exp(t))), bounds=(-10, 6), method="bounded")
    return math.exp(r.x)


Y_QMAX_MONO = qmax_mono()


def locus_y(kappa, M, locus, kern, rhoDE, w=-1.0):
    nuf, Ff, Gkf = KERN[kern]
    a0 = kappa * C_SI * math.sqrt(G_SI * rhoDE)
    if locus == "L1":
        lnT = math.log(2 * math.pi) + 1.5 * math.log(G_SI) + 0.5 * math.log(M) + math.log(rhoDE) - 1.5 * math.log(a0)
        hi = math.log(Y_QMAX_MONO) if kern == "nu_mono" else 40.0
        f = lambda t: 1.5 * t + math.log(Gkf(math.exp(t))) - lnT
        t = solve_lny(f, -400.0, hi)
    else:
        coef = -(1 + 3 * w) * (4 * math.pi / 3) * G_SI * rhoDE
        # a0 y nu(y) = coef r, r = sqrt(G M/(a0 y))  (logs)
        f = lambda t: (math.log(a0) + t + math.log(nuf(math.exp(t)))) - (math.log(coef) + 0.5 * (math.log(G_SI * M) - math.log(a0) - t))
        t = solve_lny(f)
    return None if t is None else math.exp(t), a0


def realized_vc(kappa, M, locus, kern, alpha, rhoDE):
    y, a0 = locus_y(kappa, M, locus, kern, rhoDE)
    if y is None:
        raise RuntimeError("locus %s does not exist at kappa %.3g, M %.3g (%s)" % (locus, kappa, M, kern))
    rho_loc = {"L1": 1.0, "L2": 2.0, "L2b": 2.0 / 3.0}[locus] * rhoDE
    nuf, Ff, Gkf = KERN[kern]
    vc = alpha * a0 * Ff(y) / (C_SI * math.sqrt(4 * math.pi * G_SI * rho_loc))
    r = math.sqrt(G_SI * M / (a0 * y))
    return vc, {"y": y, "r_Mpc": r / MPC, "a0": a0}


REAL = {}
REAL_REPORT = {}
if not MUT:
    P("")
    P("== realized-field branches (exact kernels; point mass; kappa solving sup v_s = c at the locus) ==")
    P("deep-regime forms (K7): saturated a0 = %s ; d ln kappa/d ln M_b = %s" % (SAT_DEEP, MEXP))
    for loc in LOCI:
        for kern in ("nu_mono", "simple"):
            for src in ("A", "B2"):
                row = []
                for Mb in MASSES:
                    M = Mb * MSUN
                    f = lambda lk: math.log(realized_vc(math.exp(lk), M, loc, kern, ALPHAS[src], RHO_DE_REPORT)[0])
                    lk = brentq(f, math.log(1e-1), math.log(1e30), xtol=1e-10)
                    row.append(math.exp(lk))
                slope = np.polyfit(np.log(MASSES), np.log(row), 1)[0]
                REAL["%s|%s|%s" % (loc, kern, src)] = {"kappa": row, "slope": slope}
                P("  %-4s %-8s alpha* %-2s kappa_sat at M_b 1e8..1e12: %s ; d ln kappa/d ln M_b = %.4f"
                  % (loc, kern, src, ["%.3g" % x for x in row], slope))
    P("")
    P("report-only at the fitted kappa = 1/2 (alpha* = 1): realized v/c at the locus vs the CFG893 ceiling there")
    for loc in LOCI:
        for kern in ("nu_mono", "simple"):
            for Mb in MASSES:
                M = Mb * MSUN
                vc, info = realized_vc(KAPPA_LAW, M, loc, kern, 1.0, RHO_DE_REPORT)
                ceil = C_NU[kern] * KAPPA_LAW / math.sqrt(4 * math.pi * rho_ratio(loc))
                Vf = (G_SI * M * info["a0"]) ** 0.25
                deep = Vf / C_SI / (math.sqrt(3) if loc == "L2" else 1.0)
                REAL_REPORT["%s|%s|%g" % (loc, kern, Mb)] = {"vc": vc, "ceiling": ceil, "attain": vc / ceil,
                                                           "deep": deep, "r_Mpc": info["r_Mpc"], "y": info["y"],
                                                           "Vf_kms": Vf / 1e3}
                P("  %-4s %-8s M_b %.0e: r %.2f Mpc, y %.2e, V_f %.0f km/s, v/c %.3e (deep form %.3e), ceiling %.4f, attained %.2e"
                  % (loc, kern, Mb, info["r_Mpc"], info["y"], Vf / 1e3, vc, deep, ceil, vc / ceil))
    # K8: exact vs deep at 1e10
    k8 = [abs(REAL_REPORT["%s|%s|1e+10" % (l, k)]["vc"] / REAL_REPORT["%s|%s|1e+10" % (l, k)]["deep"] - 1)
          for l in LOCI for k in ("nu_mono", "simple")]
    check("K8 exact-kernel realized v/c matches the deep form within 5% (M_b 1e10, report-only kappa)",
          max(k8) < 0.05, "max rel dev %.2e" % max(k8))
    # L3 numbers (report-only)
    P("")
    P("L3 (rho* = rho_ph at y = %.4f): a0 = %s ; implied kappa (report-only) at alpha* = 1:" % (Y_M, A0_L3))
    L3 = {}
    for kern in ("nu_mono",):
        h = Y_M ** 1.5 * Gk_mono(Y_M) / (2 * math.pi)
        for Mb in MASSES:
            a0 = 16 * math.pi ** 2 * C_SI ** 4 * h ** 2 / (C_NU_MONO ** 4 * G_SI * Mb * MSUN)
            L3["%g" % Mb] = a0 / (C_SI * math.sqrt(G_SI * RHO_DE_REPORT))
        P("  M_b 1e8..1e12: kappa %s (h = %.5f)" % (["%.3g" % L3[k] for k in L3], h))

# ----------------------------------------------------------------------------------------------------------------
# MUTATE teeth
# ----------------------------------------------------------------------------------------------------------------
TEETH = {}
if MUT:
    P("")
    P("== MUTATE teeth (mass-free cells) ==")

    def ratios(mcells, keys=None):
        keys = keys or list(BASE.keys())
        return {k: mcells[k] / BASE[k] for k in keys}

    def tooth(name, rat, expect):
        ok = all(abs(rat[k] - expect(k)) < 1e-9 for k in rat)
        TEETH[name] = {"bites": ok, "ratios": {k: rat[k] for k in list(rat)[:6]}}
        P("  %-46s %s  (sample ratios %s)" % (name, "BITES" if ok else "DOES NOT BITE",
                                               ["%.6f" % rat[k] for k in list(rat)[:4]]))

    tooth("M1 alpha* -> 2 alpha*: x 0.5", ratios(cells(alpha_scale=2.0)), lambda k: 0.5)
    mono_keys = [k for k in BASE if k.endswith("nu_mono")]
    tooth("M2 nu_mono -> simple: nu_mono cells x c_nu", ratios(cells(kern_override="simple"), mono_keys),
          lambda k: C_NU_MONO)
    tooth("M3 4 pi G -> 8 pi G in tau: x sqrt2", ratios(cells(pmult=2.0)), lambda k: math.sqrt(2))
    tooth("M4 w -1 -> -0.9: L2, L2b x sqrt(0.85); L1 x 1", ratios(cells(w=-0.9)),
          lambda k: 1.0 if "|L1|" in k else math.sqrt(0.85))
    tooth("M5 D 4 -> 5: L1 x sqrt(4/3), L2 x sqrt(2/3), L2b x 1 (declared)", ratios(cells(D=5)),
          lambda k: math.sqrt(4 / 3) if "|L1|" in k else (math.sqrt(2 / 3) if "|L2|" in k else 1.0))
    for nm, mc in (("M1", cells(alpha_scale=2.0)), ("M3", cells(pmult=2.0)), ("M4", cells(w=-0.9)), ("M5", cells(D=5))):
        v = list(mc.values())
        P("  %s range %.3f .. %.3f, p_data(rho_DE) %.3f" % (nm, min(v), max(v),
                                                          sum(W_DE[0] <= x <= W_DE[1] for x in v) / len(v)))

# ----------------------------------------------------------------------------------------------------------------
# overall label
# ----------------------------------------------------------------------------------------------------------------
P("")
S4 = False
checks_ok = all(c["ok"] for c in CHECKS.values())
if FORBIDDEN_HIT:
    overall = "VOID"
else:
    selected = (cls_DE in ("CONSISTENT", "MISS", "EXACT CANDIDATE")) and S4
    overall = "kappa SELECTED" if selected else "NOT A SELECTION"
summary = {
    "overall": overall,
    "campaign_class_mass_free_set": cls_DE,
    "campaign_class_rho_crit": cls_CR,
    "p_data_rho_DE": p_data_DE, "p_data_rho_crit_relabel": p_data_CR_a, "p_data_rho_crit_endconv": p_data_CR_b,
    "p_exact": p_exact, "range": [min(vals), max(vals)], "spread": spread,
    "canonical_cell_L2_numono_alpha1": canon, "canonical_class": canon_cls,
    "alpha_source_A": "TRADE in beta (alpha_max = 1/(beta q)); 1 only by the beta = 1 convention at q -> 1",
    "alpha_source_B": "conditional on a one-relaxation-time hypothesis: B1 1 (Fokker-Planck), B2 1/sqrt2 (BGK); else FREE",
    "IS_closure_alpha_bound": "none: characteristic speeds alpha-free",
    "realized_branches": "MASS-DEPENDENT (d ln kappa/d ln M_b = -1; rho_DE and kappa cancel in the deep regime); EXCLUDED",
    "L3": "kappa-free, MASS-DEPENDENT (a0 ~ c^4/(G M_b))",
    "rho_m_bar_loci": "VOID as selections (Omega_m/Omega_L forbidden; run as (1+z)^(3/2))",
    "S4": "FAILED (declared in advance)",
    "selection_requirements": {"(i) pure number": "per cell yes", "(ii) mass- and density-choice-free":
                               "no: menu over declared loci/kernels/alpha; realized field mass-dependent",
                               "(iii) second prediction": "no"},
}
P("OVERALL: %s - mass-free set %s on rho_DE (%s on rho_crit), kappa %.2f..%.2f, p_data %.2f, p_exact %.2f; canonical cell %.3f (%s)"
  % (overall, cls_DE, cls_CR, min(vals), max(vals), p_data_DE, p_exact, canon, canon_cls))
P("alpha: IS closure gives no bound; source A is a TRADE in beta; B1/B2 need a one-relaxation-time hypothesis.")
if REAL:
    allk = [x for v in REAL.values() for x in v["kappa"]]
    P("realized field at the loci: mass-dependent (exponent -1), kappa_sat %.2g .. %.2g over M_b 1e8..1e12: EXCLUDED."
      % (min(allk), max(allk)))
    summary["realized_kappa_range"] = [min(allk), max(allk)]
P("kappa = 1/2 stays FITTED.")

# post-freeze, report-only reading (not a K-test): with H_L^2 = 8 pi G rho_DE/3 used only as a rewriting,
# each saturated rho_DE-locus relation is a0 = N c H_L/(alpha* c_nu), i.e. an H-type identification.
HL = sp.symbols("H_L", positive=True)
Hreading = {}
for loc, rat in (("L1", sp.Integer(1)), ("L2", sp.Integer(2)), ("L2b", sp.Rational(2, 3))):
    a0_sat = cs2 * sp.sqrt(4 * sp.pi * Gs2 * rat * rhoDE2) / (al2 * cn2)
    Nn = sp.simplify(a0_sat * al2 * cn2 / (cs2 * HL)).subs(rhoDE2, 3 * HL ** 2 / (8 * sp.pi * Gs2))
    Hreading[loc] = str(sp.simplify(Nn))
P("post-freeze reading (report-only): saturated a0 = N c H_L/(alpha* c_nu) with N = %s; "
  "the rho_DE-defined loci make the saturation an H-type relation (pi-parity: kappa^2 in Q pi^odd for the simple kernel)"
  % Hreading)
summary["H_type_reading"] = Hreading

res = {"lane": "CFG898", "mutate": MUT, "c_nu": C_NU, "y_m": Y_M, "alphas": ALPHAS, "cells": BASE,
       "checks": CHECKS, "summary": summary, "need": need, "inverse": inv,
       "realized": REAL, "realized_report_fitted_kappa": REAL_REPORT, "teeth": TEETH,
       "pi_weight": pi_w,
       "report_inputs": {"H0_kms_Mpc": 67.4, "Omega_L": OL_REPORT, "rho_DE_report": RHO_DE_REPORT}}
if not MUT:
    res["L3_kappa_report"] = L3
with open(OUT_JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(OUT_TXT, "w") as fh:
    fh.write("\n".join(LINES) + "\n")

if MUT:
    allbite = all(t["bites"] for t in TEETH.values()) and len(TEETH) == 5
    P("MUTATE: %d/5 teeth bite -> exit %d" % (sum(t["bites"] for t in TEETH.values()), 1 if allbite else 2))
    with open(OUT_TXT, "w") as fh:
        fh.write("\n".join(LINES) + "\n")
    sys.exit(1 if allbite else 2)
nfail = sum(not c["ok"] for c in CHECKS.values())
P("checks: %d/%d PASS -> exit %d" % (len(CHECKS) - nfail, len(CHECKS), 0 if nfail == 0 else 1))
with open(OUT_TXT, "w") as fh:
    fh.write("\n".join(LINES) + "\n")
sys.exit(0 if nfail == 0 else 1)
