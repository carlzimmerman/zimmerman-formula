#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG320 -- recipe gate G12 (radiative stability / naturalness) for the filtered C-H/K chassis (L340: beta = 0,
alpha_c x c_2 window, nu_mono through the heat filter).  Criteria frozen first: FROZEN_CRITERIA.md (commit 7d25a59e6).

  (A) one-loop naturalness of alpha_c and c_2 by power counting, cutoff = each point's own strong-coupling scale
      Lambda_sc = sqrt(alpha_c) M_P c_s^{-1/2} (XC1), with the alpha_c = c_2 = 0 symmetry;
  (B) Lorentz-violation leakage into matter: the LV of the graviton propagator is DERIVED here (sympy, linear scalar
      sector in unitary gauge; tensor and vector sectors are GR's at beta = 0), its Euclidean phase-space average
      eps_LV feeds the Pospelov-Shang-normalised EFT estimate; a worst-case O(1)-LV UV piece at Lambda_sc is added;
      both against |delta| <= 6e-20 (Klinkhamer & Schreck 2008, PROVISIONAL);
  (C) explicit power counting for the heat filter and the kernel coefficients under loops (both footings).

Controls: Collins et al. 2004 reproduced numerically (K1), GR covariant amplitude (K2), zero-coupling limit (K3),
G_N static limit (K4), khronon pole (K5), XC1's 8.5e8 GeV (K6), sampling stability (K7).
MUTATE: CFG320_MUTATE=1 sets c_2 = 0.5 at every alpha_c; part B must fail (rc = 1); separate _MUTATE outputs.

kappa = 1/2 is FITTED; a0 enters only part C.  Run from anywhere:
    python3 campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability.py
    CFG320_MUTATE=1 python3 campaign_fresh_gravity/CFG320_radiative_stability_g12/cfg320_radiative_stability.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy import integrate
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("CFG320_MUTATE", "0") == "1"
SLUG = "cfg320_radiative_stability"
SUF = "_MUTATE" if MUTATE else ""
LINES, CH = [], []
OUT = {"lane": "CFG320", "gate": "G12", "mutate": MUTATE, "frozen_commit": "7d25a59e6", "checks": [], "numbers": {}}
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


def check(name, measured, ok, load_bearing=True, reading=""):
    CH.append((name, bool(ok), load_bearing))
    OUT["checks"].append({"name": name, "pass": bool(ok), "load_bearing": load_bearing, "measured": measured})
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")


def rel(p):
    return os.path.relpath(p, REPO)


# ---------------------------------------------------------------------------------------------------- inputs
MP = 2.435e18                                   # reduced Planck mass, GeV (XC1 convention, G = 1/(8 pi M_P^2))
HBARC = 1.973269804e-16                         # GeV m
C_SI, GM_SUN, AU, PC = 2.99792458e8, 1.32712440018e20, 1.495978707e11, 3.0856775814913673e16
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # kappa = 1/2 FITTED (canonical); alt footing
XI_PC = (0.031, 0.045)
BOUND = 6e-20                                   # Klinkhamer & Schreck 2008 eq. 16 upper side (2 sigma), PROVISIONAL
READ_BOUNDS = {"KS08 lower side": 9e-16, "PS12 'most stringent' (ref unread)": 1e-23, "LEP/Tevatron (recalled)": 1e-11}
N_G, N_M = 10, 100
L340F = os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")
XC1F = os.path.join(REPO, "real_research", "extra_crispy_2026", "XC1_strong_coupling_chk_results.json")
L340 = json.load(open(L340F)); XC1 = json.load(open(XC1F))
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
AC_GRID = np.logspace(math.log10(AC_MIN), math.log10(AC_MAX), 9)
C2_GRID = np.array([0.5]) if MUTATE else np.logspace(math.log10(C2_MIN), math.log10(C2_MAX), 9)
P(f"CFG320 G12 radiative stability{'   *** MUTATE: c_2 = 0.5 ***' if MUTATE else ''}")
P(f"  inputs ({rel(L340F)}): alpha_c in [{AC_MIN:.4e}, {AC_MAX:.3e}], c_2 in [{C2_MIN:.4e}, {C2_MAX:.4e}]; "
  f"scored c_2 grid {C2_GRID[0]:.4g}..{C2_GRID[-1]:.4g}; M_P = {MP:.4g} GeV (reduced); bound |delta| <= {BOUND:g} (PROVISIONAL)")
OUT["numbers"]["inputs"] = {"alpha_c": [AC_MIN, AC_MAX], "c2_window": [C2_MIN, C2_MAX], "c2_scored": C2_GRID.tolist(),
                            "M_P_GeV": MP, "bound": BOUND, "N_g": N_G, "N_m": N_M, "a0": A0, "xi_pc": XI_PC}


def cs2(a, c2):
    return c2 * (2 - a) / (a * (2 + 3 * c2))


def lam_sc(a, c2):
    cs = math.sqrt(cs2(a, c2))
    return math.sqrt(a) * MP * (cs ** 1.5 if cs < 1 else cs ** -0.5), cs


# ============================================================================================ K1 Collins et al.
banner("K1  CONTROL: Collins, Perez, Sudarsky, Urrutia & Vucetich 2004 (Yukawa loop, LV regulator), reproduced")
k4, K, cth, p1, p4, xx = sp.symbols('k4 K c p1 p4 x', real=True)
MF = sp.Rational(1, 100)                        # fermion mass in units of Lambda


def collins_xi(fexpr):
    """xi/g^2 = 4 (d^2/dp4^2 - d^2/dp1^2) I at p = 0, I = Int d^4k_E/(2pi)^4 (k.(k+p) - m^2) f f / ((k^2+m^2)((k+p)^2+m^2))."""
    kx = K * cth
    k2 = K**2 + k4**2
    kp = kx * p1 + k4 * p4
    G = (k2 + kp - MF**2) / ((k2 + MF**2) * (k2 + 2 * kp + p1**2 + p4**2 + MF**2)) \
        * fexpr.subs(xx, K) * fexpr.subs(xx, sp.sqrt(K**2 + 2 * kx * p1 + p1**2))
    D = sp.simplify((sp.diff(G, p4, 2) - sp.diff(G, p1, 2)).subs({p1: 0, p4: 0}))
    fn = sp.lambdify((k4, K, cth), D, 'numpy')

    def inner(K_, c_):
        return integrate.quad(lambda t: fn(t, K_, c_), -np.inf, np.inf, limit=200)[0]
    val = integrate.dblquad(lambda c_, K_: inner(K_, c_) * K_**2 * 2 * np.pi, 1e-6, 12, -1, 1, epsabs=1e-10)[0]
    return 4 * val / (2 * np.pi)**4, D


import warnings
warnings.filterwarnings("ignore")
K1rows = {}
for lab, fe in (("exp(-x^2)", sp.exp(-xx**2)), ("1/(1+x^4)", 1 / (1 + xx**4))):
    xi_num, _ = collins_xi(fe)
    Iint = float(sp.Integral(xx * sp.diff(fe, xx)**2, (xx, 0, sp.oo)).evalf())
    pred = (1 + 2 * Iint) / (6 * math.pi**2)
    K1rows[lab] = {"xi_over_g2_numeric": xi_num, "collins_formula": pred, "ratio": xi_num / pred}
    P(f"    f = {lab:10s}: xi/g^2 numeric = {xi_num:.6e}   Collins (g^2/6pi^2)(1 + 2 Int x f'^2) = {pred:.6e}   ratio {xi_num / pred:.5f}")
# LI regulator limit: f = 1, 4D ball cutoff, the integrand-level difference integrates to zero by O(4) symmetry
kx_ = K * cth; k2_ = K**2 + k4**2; kp_ = kx_ * p1 + k4 * p4
G1 = (k2_ + kp_ - MF**2) / ((k2_ + MF**2) * (k2_ + 2 * kp_ + p1**2 + p4**2 + MF**2))
D1 = sp.simplify((sp.diff(G1, p4, 2) - sp.diff(G1, p1, 2)).subs({p1: 0, p4: 0}))
fn1 = sp.lambdify((k4, K, cth), D1, 'numpy')
RB = 10.0
li_val = integrate.tplquad(lambda t, c_, K_: fn1(t, K_, c_) * K_**2 * 2 * np.pi, 1e-6, RB, -1, 1,
                           lambda K_, c_: -math.sqrt(max(RB**2 - K_**2, 0)), lambda K_, c_: math.sqrt(max(RB**2 - K_**2, 0)),
                           epsabs=1e-9)[0] * 4 / (2 * np.pi)**4
P(f"    f = 1 with a 4D-ball cutoff (Lorentz-invariant regulator): xi/g^2 = {li_val:.2e}")
OUT["numbers"]["K1"] = {"rows": K1rows, "m_over_Lambda": float(MF), "LI_limit_xi": li_val}
check("K1 Collins et al. 2004 eq. A.2 reproduced at m = 0.01 Lambda for two LV regulators (within 2%), and xi = 0 for a "
      "Lorentz-invariant regulator",
      "; ".join(f"{k_}: ratio {v_['ratio']:.4f}" for k_, v_ in K1rows.items()) + f"; LI limit {li_val:.1e}",
      all(abs(v_["ratio"] - 1) < 0.02 for v_ in K1rows.values()) and abs(li_val) < 1e-4,
      reading="the generic LV-percolation mechanism (a LV cutoff leaks O(g^2/6pi^2) LV into a LI theory, independent of "
              "Lambda) is reproduced; it is the UV-sensitivity that part B3 models")

# ============================================================================================ B1 the propagator
banner("B1  THE CHASSIS GRAVITON PROPAGATOR, scalar sector, unitary gauge (sympy); tensor/vector = GR at beta = 0")
w, k = sp.symbols('omega k', positive=True)
al, lam = sp.symbols('alpha lambda', nonnegative=True)
rho, sig = sp.symbols('rho sigma', real=True)
dt, lap = -sp.I * w, -k**2
M = sp.zeros(3, 3)                              # fields (Phi, B, Psi); action (M_P^2/2) X^dag M X


def add(c, i, si, j, sj):
    M[i, j] += c * sp.conjugate(si) * sj / 2
    M[j, i] += c * sp.conjugate(sj) * si / 2


# N sqrt(gamma)[K_ij K^ij - (1+lambda) K^2 + R3 + alpha a.a] to 2nd order, K_ij = -Psidot delta_ij - d_i d_j B
add(-6, 2, dt, 2, dt); add(-4, 2, dt, 1, lap)                                   # K_ijK^ij - K^2
add(-9 * lam, 2, dt, 2, dt); add(-6 * lam, 2, dt, 1, lap); add(-lam, 1, lap, 1, lap)  # -lambda K^2
add(2 * k**2, 2, 1, 2, 1); add(-4 * k**2, 0, 1, 2, 1)                           # N sqrt(gamma) R3
add(al * k**2, 0, 1, 0, 1)                                                     # alpha a.a, a_i = d_i Phi
q = -sp.I * w * rho / k**2                      # conservation: rho_dot + Lap q = 0
p = w**2 * rho / k**2 + 2 * k**2 * sig / 3      # conservation: q_dot_j + d_i T^ij = 0
b = sp.Matrix([-rho / 2, k**2 * q / 2, -3 * p / 2])   # L_m = (1/2) T^{mu nu} delta g_{mu nu}
W = sp.factor(sp.simplify(-(b.H * M.inv() * b)[0]))
M2 = M.extract([0, 2], [0, 2]).subs({al: 0, lam: 0}); b2 = b.extract([0, 2], [0])   # GR: B = 0 gauge
WGR = sp.factor(sp.simplify(-(b2.H * M2.inv() * b2)[0]))
Tmn = rho**2 - 2 * k**2 * sp.Abs(q)**2 + 3 * p**2 + sp.Rational(2, 3) * k**4 * sig**2
Tr = -rho + 3 * p
Wcov = sp.simplify((Tmn - Tr**2 / 2) / (k**2 - w**2))
ratio_cov = sp.simplify(WGR / Wcov)
P(f"    W_chassis = {W}")
P(f"    W_GR      = {WGR}")
P(f"    W_GR / covariant [T.T - T^2/2]/(k^2 - omega^2) = {ratio_cov}")
check("K2 GR control: the derived GR scalar-sector amplitude equals the covariant amplitude for conserved scalar-type "
      "sources up to one constant", f"ratio = {ratio_cov}", ratio_cov.is_number and ratio_cov != 0)
tt, a_, l_ = sp.symbols('t a l', positive=True)
lim0 = sp.simplify(sp.limit(W.subs({al: tt * a_, lam: tt * l_}), tt, 0) - WGR)
dW = sp.factor(sp.simplify(W - WGR))
P(f"    Delta W = W_chassis - W_GR = {dW}")
check("K3 zero-coupling limit: alpha_c, c_2 -> 0 (any ratio) gives W_chassis -> W_GR, and Delta W carries an overall "
      "alpha*lambda", f"limit difference = {lim0}; Delta W numerator has factor alpha*lambda: "
                      f"{sp.simplify(sp.numer(sp.together(dW)).subs(al, 0)) == 0 and sp.simplify(sp.numer(sp.together(dW)).subs(lam, 0)) == 0}",
      lim0 == 0 and sp.simplify(sp.numer(sp.together(dW)).subs(al, 0)) == 0)
stat = sp.simplify((W / WGR).subs(w, 0).subs(sig, 0))
check("K4 static limit (density source): W_chassis/W_GR = 1/(1 - alpha_c/2) (G_N, FP2 D1)", f"{stat}",
      sp.simplify(stat - 1 / (1 - al / 2)) == 0,
      reading="with anisotropic stress the static amplitude also has an O(alpha) stress-stress term (in the LV measure)")
den = sp.denom(sp.together(W))
roots = [r for r in sp.solve(den, w) if r.is_positive is not False]
cs2_sym = lam * (2 - al) / (al * (2 + 3 * lam))
pole_ok = any(sp.simplify(r**2 - cs2_sym * k**2) == 0 for r in roots)
check("K5 the propagator pole is the khronon, omega^2 = c_s^2 k^2 with c_s^2 = c_2 (2 - alpha_c)/(alpha_c (2 + 3 c_2)) "
      "(L340/XC1)", f"roots {roots}", pole_ok)

# Euclidean LV measure
wE = sp.symbols('omega_E', positive=True)
dWE = sp.simplify(dW.subs(w, sp.I * wE))
qE = wE * rho / k**2; pE = -wE**2 * rho / k**2 + 2 * k**2 * sig / 3
NORM = (rho**2 + 2 * k**2 * qE**2 + 3 * pE**2 + sp.Rational(2, 3) * k**4 * sig**2) / (4 * (k**2 + wE**2))
DELTA = sp.factor(sp.simplify(dWE / NORM))
P(f"    Euclidean LV measure Delta(theta) = Delta W_E / N_E, N_E = sum of squared Euclidean source components / (4 Q^2):")
P(f"      Delta = {DELTA}")
SRC = {"density (sigma = 0)": {sig: 0, rho: 1}, "stress (rho = 0)": {rho: 0, sig: 1},
       "mixed rho = +k^2 sigma": {rho: k**2, sig: 1}, "mixed rho = -k^2 sigma": {rho: -k**2, sig: 1}}
DFN = {lab: sp.lambdify((wE, k, al, lam), sp.simplify(DELTA.subs(s)), 'numpy') for lab, s in SRC.items()}


def eps_measure(a, c2, n=4000):
    cs = math.sqrt(cs2(a, c2))
    u = np.linspace(math.log(1e-2 / cs), math.log(1e4), n)     # u = ln tan(theta)
    th = np.arctan(np.exp(u))
    wgt = np.sin(th)**2 * np.sin(th) * np.cos(th)              # sin^2(theta) d theta, d theta = sin cos du
    res = {}
    for lab, fn in DFN.items():
        d = np.abs(fn(np.cos(th), np.sin(th), a, c2))
        res[lab] = (float(integrate.trapezoid(d * wgt, u) / integrate.trapezoid(wgt, u)), float(d.max()))
    eps = max(v[0] for v in res.values()); emax = max(v[1] for v in res.values())
    return eps, emax, res


# ============================================================================================ grid: A and B
banner("A + B  OVER THE GRID (cutoff = each point's own Lambda_sc)")
LOOP16 = 16 * math.pi**2
LOOP12 = 12 * math.pi**2
rows = []
for a in AC_GRID:
    for c2 in C2_GRID:
        Ls, cs = lam_sc(a, c2)
        eps, emax, res = eps_measure(a, c2)
        eps2, _, _ = eps_measure(a, c2, n=8000)
        lf = math.log(MP**2 / Ls**2)
        dA = N_G * max(a, c2) * Ls**2 / (LOOP16 * MP**2)
        d_eft = eps * Ls**2 / (LOOP12 * MP**2) * lf
        d_eft_max = emax * Ls**2 / (LOOP12 * MP**2) * lf
        d_uv = Ls**2 / (LOOP12 * MP**2) * lf
        dA_m = N_M * BOUND * Ls**2 / (LOOP16 * MP**2)
        in_win = (a <= AC_MAX * (1 + 1e-9)) and (1.5 * c2 <= 0.1 + 1e-12)
        rows.append({"alpha_c": a, "c2": c2, "c_s": cs, "Lambda_sc_GeV": Ls, "eps_LV": eps, "eps_LV_8000": eps2, "eps_max": emax,
                     "eps_by_source": res, "delta_alpha": dA, "delta_alpha_over_alpha": dA / a, "delta_c2_over_c2": dA / c2,
                     "delta_alpha_matter_feedback": dA_m, "delta_EFT": d_eft, "delta_EFT_epsmax": d_eft_max, "delta_UV": d_uv,
                     "A_ok": dA <= a and dA <= c2, "EFT_ok": d_eft <= BOUND, "UV_ok": d_uv <= BOUND, "in_window": in_win,
                     "reading_Lambda_8.5e8": {"delta_EFT": eps * (8.5e8)**2 / (LOOP12 * MP**2) * math.log(MP**2 / 8.5e8**2),
                                              "delta_alpha_over_alpha": N_G * max(a, c2) * (8.5e8)**2 / (LOOP16 * MP**2) / a},
                     "reading_Lambda_MP": {"delta_alpha_over_alpha": N_G * max(a, c2) / LOOP16 / a,
                                           "delta_EFT_no_log": eps / LOOP12}})
OUT["numbers"]["grid"] = rows
P(f"    {'alpha_c':>9s} {'c_2':>9s} {'c_s/c':>9s} {'L_sc GeV':>9s} {'eps_LV':>9s} {'eps_max':>9s} {'da/a':>9s} "
  f"{'d_EFT':>9s} {'d_UV':>9s}")
for r in rows:
    if (r["alpha_c"] in (AC_GRID[0], AC_GRID[4], AC_GRID[-1])) and (r["c2"] in (C2_GRID[0], C2_GRID[-1])):
        P(f"    {r['alpha_c']:9.2e} {r['c2']:9.2e} {r['c_s']:9.2e} {r['Lambda_sc_GeV']:9.2e} {r['eps_LV']:9.2e} "
          f"{r['eps_max']:9.2e} {r['delta_alpha_over_alpha']:9.2e} {r['delta_EFT']:9.2e} {r['delta_UV']:9.2e}")
Lmin = min(r["Lambda_sc_GeV"] for r in rows); Lmax = max(r["Lambda_sc_GeV"] for r in rows)
LHLmax = brentq(lambda x: 10**(2 * x) / (LOOP12 * MP**2) * math.log(MP**2 / 10**(2 * x)) - BOUND, 3, 18)
LHLmax = 10**LHLmax
n_uv = sum(r["UV_ok"] for r in rows)
OUT["numbers"]["summary"] = {"Lambda_sc_min": Lmin, "Lambda_sc_max": Lmax, "Lambda_HL_max_GeV": LHLmax, "UV_ok_points": n_uv,
                             "n_points": len(rows), "eps_LV_max": max(r["eps_LV"] for r in rows),
                             "eps_max_max": max(r["eps_max"] for r in rows),
                             "delta_alpha_over_alpha_max": max(r["delta_alpha_over_alpha"] for r in rows),
                             "delta_c2_over_c2_max": max(r["delta_c2_over_c2"] for r in rows),
                             "delta_EFT_max": max(r["delta_EFT"] for r in rows),
                             "delta_EFT_epsmax_max": max(r["delta_EFT_epsmax"] for r in rows),
                             "delta_UV_min": min(r["delta_UV"] for r in rows), "delta_UV_max": max(r["delta_UV"] for r in rows)}
S = OUT["numbers"]["summary"]
P(f"\n    Lambda_sc over the scored grid: {Lmin:.3e} .. {Lmax:.3e} GeV;  Pospelov-Shang hierarchy for |delta_UV| <= {BOUND:g}: "
  f"Lambda_HL <= {LHLmax:.3e} GeV;  points with delta_UV <= bound: {n_uv}/{len(rows)}")

if not MUTATE:
    check("K6 XC1 reproduced: min Lambda_sc over the window = 8.5e8 GeV (within 3%)", f"{Lmin:.4e} GeV",
          abs(Lmin / 8.5e8 - 1) < 0.03)
k7 = max(abs(r["eps_LV_8000"] / r["eps_LV"] - 1) for r in rows)
check("K7 eps_LV stable to 1% when the theta sampling is doubled", f"max relative change {k7:.2e}", k7 < 0.01)
zl, zl_max, _ = eps_measure(1e-20, 1e-20)
check("K3b zero-coupling limit, numerically: eps_LV -> 0 as alpha_c, c_2 -> 0 (alpha_c = c_2 = 1e-20)", f"eps_LV = {zl:.2e}, eps_max = {zl_max:.2e}", zl < 1e-18 and zl_max < 1e-18)

banner("A  TECHNICAL NATURALNESS of alpha_c and c_2")
P("    A0: with alpha_c = c_2 = 0 the Stueckelberg-restored khronon terms alpha_c a.a - c_2 K^2 vanish identically, the")
P("        action is GR + minimally coupled matter, diffeomorphism invariant, and the khronon drops out: an enlarged")
P("        symmetry, so loop corrections to (alpha_c, c_2) are proportional to (alpha_c, c_2) themselves. Matter couples")
P("        to g only, so pure matter loops generate diffeomorphism-invariant functionals of g (G, the vacuum energy,")
P("        R^2 ...) and never alpha or c_2. Mixed loops: generic mixing assumed (c_2 may generate alpha).")
OUT["numbers"]["A0"] = {"symmetry": "alpha_c = c_2 = 0 -> GR + decoupled khronon (full diffeomorphisms)",
                        "Delta_W_factor_alpha_lambda": True}
check("A0 the alpha_c = c_2 = 0 point is a symmetry point: the derived propagator LV Delta W vanishes when either "
      "coupling vanishes (overall alpha*lambda), and the khronon terms carry overall alpha_c, c_2",
      "Delta W numerator vanishes at alpha = 0 and at lambda = 0 (sympy)",
      sp.simplify(sp.numer(sp.together(dW)).subs(al, 0)) == 0 and sp.simplify(sp.numer(sp.together(dW)).subs(lam, 0)) == 0)
nA = sum(r["A_ok"] for r in rows)
check("A1 one-loop naturalness at Lambda = Lambda_sc(point): |delta alpha| <= alpha_c and |delta c_2| <= c_2 at every "
      "grid point (N_g = 10, generic mixing delta ~ N_g max(alpha_c, c_2) Lambda^2/(16 pi^2 M_P^2))",
      f"{nA}/{len(rows)} points; max delta alpha/alpha_c = {S['delta_alpha_over_alpha_max']:.2e}, "
      f"max delta c_2/c_2 = {S['delta_c2_over_c2_max']:.2e}; matter-LV feedback delta alpha <= "
      f"{max(r['delta_alpha_matter_feedback'] for r in rows):.1e}",
      nA == len(rows),
      reading="at Lambda = Lambda_sc the correction is delta alpha/alpha ~ N_g sqrt(c_2 alpha_c)/(16 pi^2) (analytic): "
              "self-consistently small; with Lambda = M_P (no hierarchy) delta alpha/alpha would be "
              f"{max(r['reading_Lambda_MP']['delta_alpha_over_alpha'] for r in rows):.1e} (unnatural)")
ana = max(abs(r["delta_alpha_over_alpha"] / (N_G * math.sqrt(r["c2"] * r["alpha_c"] * (2 + 3 * r["c2"]) / (2 - r["alpha_c"])) / LOOP16) - 1)
          for r in rows if r["c2"] >= r["alpha_c"])
check("A2 analytic form: delta alpha/alpha_c = N_g sqrt(c_2 alpha_c (2+3c_2)/(2-alpha_c))/(16 pi^2) at Lambda_sc",
      f"max relative deviation from the closed form {ana:.1e}", ana < 1e-6, load_bearing=False)

banner("B  LORENTZ-VIOLATION LEAKAGE INTO MATTER (photon/electron maximal-speed coefficients)")
b0 = all(r["in_window"] for r in rows)
check("B0 the scored inputs lie in the committed window (alpha_c <= 3.2e-9; BBN 1.5 c_2 <= 0.1, L340 P1)",
      f"c_2 scored {C2_GRID.min():.4g}..{C2_GRID.max():.4g}; 1.5 c_2 max = {1.5 * C2_GRID.max():.3g}", b0)
nE = sum(r["EFT_ok"] for r in rows)
check("B2 EFT leakage delta_EFT = eps_LV Lambda_sc^2/(12 pi^2 M_P^2) ln(M_P^2/Lambda_sc^2) <= 6e-20 at every point",
      f"{nE}/{len(rows)}; max delta_EFT = {S['delta_EFT_max']:.2e} (eps_max instead: {S['delta_EFT_epsmax_max']:.2e}); "
      f"eps_LV <= {S['eps_LV_max']:.2e}, eps_max <= {S['eps_max_max']:.2e}",
      nE == len(rows),
      reading="the propagator LV is O(alpha_c) over almost all of Euclidean phase space and O(c_2) only inside the "
              "khronon cone omega_E > c_s k, a 1/c_s^3 sliver")
check("B3 worst-case UV leakage (O(1) LV entering at Lambda_HL = Lambda_sc): delta_UV <= 6e-20 at every point",
      f"{n_uv}/{len(rows)}; delta_UV {S['delta_UV_min']:.2e} .. {S['delta_UV_max']:.2e}; hierarchy needed Lambda_HL <= "
      f"{LHLmax:.2e} GeV", n_uv == len(rows), load_bearing=False,
      reading="decides PASS vs CONDITIONAL under the frozen rule; not a control")
OUT["numbers"]["B_read_bounds"] = {k_: {"delta_UV_points_ok": sum(r["delta_UV"] <= v_ for r in rows),
                                        "delta_EFT_points_ok": sum(r["delta_EFT"] <= v_ for r in rows)} for k_, v_ in READ_BOUNDS.items()}
for k_, v_ in OUT["numbers"]["B_read_bounds"].items():
    P(f"    reading vs {k_} ({READ_BOUNDS[k_]:g}): EFT ok at {v_['delta_EFT_points_ok']}/{len(rows)}, worst-case UV ok at "
      f"{v_['delta_UV_points_ok']}/{len(rows)}")
LHL_read = {k_: 10**brentq(lambda x: 10**(2 * x) / (LOOP12 * MP**2) * math.log(MP**2 / 10**(2 * x)) - v_, 1, 18)
            for k_, v_ in READ_BOUNDS.items()}
OUT["numbers"]["Lambda_HL_max_read_bounds"] = LHL_read
for k_, v_ in LHL_read.items():
    P(f"    reading: hierarchy needed for {k_} ({READ_BOUNDS[k_]:g}): Lambda_HL <= {v_:.2e} GeV")
emax_changes = not all(r["delta_EFT_epsmax"] <= BOUND for r in rows)
OUT["numbers"]["eps_max_would_change_verdict"] = emax_changes
P(f"    reading: scoring the EFT piece with eps_max (the khronon-cone sliver value, not phase-space weighted) passes at "
  f"{sum(r['delta_EFT_epsmax'] <= BOUND for r in rows)}/{len(rows)} points"
  f"{' -- it would move the EFT piece onto the same sub-window/hierarchy condition as B3' if emax_changes else ''}")
# sub-window in which the worst-case UV piece passes
sub = [r for r in rows if r["UV_ok"]]
OUT["numbers"]["UV_subwindow"] = [{"alpha_c": r["alpha_c"], "c2": r["c2"], "Lambda_sc": r["Lambda_sc_GeV"]} for r in sub]
P(f"    worst-case-UV sub-window: {len(sub)} grid points pass; the condition is Lambda_sc(alpha_c, c_2) <= {LHLmax:.2e} GeV, "
  f"i.e. alpha_c^(3/4) c_2^(-1/4) <~ {LHLmax / MP:.2e}")

# R1 Pospelov-Shang reading
banner("R1  READING: the Pospelov-Shang threshold (eq. 59 coefficient) against their stated Lambda_HL <~ 1e10 GeV for 1e-20")
r1 = {"reduced, with log": 10**brentq(lambda x: 10**(2 * x) / (LOOP12 * MP**2) * math.log(MP**2 / 10**(2 * x)) - 1e-20, 3, 18),
      "reduced, no log": MP * math.sqrt(LOOP12 * 1e-20),
      "M = 1.22e19, no log": 1.2209e19 * math.sqrt(LOOP12 * 1e-20)}
for k_, v_ in r1.items():
    P(f"    {k_:22s}: Lambda_HL = {v_:.2e} GeV")
OUT["numbers"]["R1"] = r1
check("R1 (reading) the PS 1e10 GeV figure is reproduced within a factor 3 only with M = 1.22e19 GeV and no log; the "
      "lane scores the stricter reduced-M_P-with-log form", "; ".join(f"{k_} {v_:.1e}" for k_, v_ in r1.items()),
      abs(math.log10(r1["M = 1.22e19, no log"] / 1e10)) < 0.5, load_bearing=False)

# ============================================================================================ C
banner("C  THE HEAT FILTER AND THE KERNEL UNDER LOOPS (power counting, both footings, both xi floors)")
kMrows = XC1["numbers"]["A6"]["rows"]
Crows = {}
for foot, a0 in A0.items():
    kM = min(r["k_M_GeV"] for r in kMrows if r["footing"] == foot)
    alphaM = a0 / C_SI**2 * HBARC                         # a0/c^2 in GeV
    for xi in XI_PC:
        xi_g = xi * PC / HBARC
        gmax = (2 / (3 * math.e)) / (xi_g * kM)**2
        Ca = gmax / LOOP16
        g01 = GM_SUN / (0.1 * AU)**2
        dU = g01 / C_SI**2 * HBARC
        Cb = dU**2 / (LOOP16 * MP**2)
        Cb_tree = alphaM**2 / (LOOP16 * MP**2)
        Cc = max(Lmax**2 / (LOOP16 * MP**2), 1 / (LOOP16 * MP**2 * xi_g**2))
        Crows[f"{foot}, xi = {xi} pc"] = {"k_M_GeV": kM, "g_max": gmax, "C_a_kernel_loop": Ca, "C_b_unfiltered_vs_Newton_0.1AU": Cb,
                                           "C_b_vs_tree_MOND_quartic": Cb_tree, "C_c_delta_xi_over_xi": Cc}
        P(f"    {foot:9s} xi = {xi} pc: k_M = {kM:.3e} GeV; C-a filtered kernel loop <= {Ca:.1e}; C-b unfiltered (dU)^4 at 0.1 AU / "
          f"Newton = {Cb:.1e} (vs tree MOND quartic {Cb_tree:.1e}); C-c delta xi/xi <= {Cc:.1e}")
OUT["numbers"]["C"] = Crows
P("    statement: every MOND vertex acts on S U, so each external MOND leg carries e^{-xi^2 k^2/2}; loops renormalise the")
P("    kernel coefficients (q's Taylor/shape coefficients, nu_mono's delta = 0.05, alpha_M = a0/c^2) multiplicatively by")
P("    <= g_max/(16 pi^2) and cannot remove the external-leg Gaussian. The only unfiltered U vertex is C-H's quadratic")
P("    2h(DU - a)^2 (U enters through the metric only), so unfiltered operators are graviton-loop generated and M_P-")
P("    suppressed: (dU)^4/(16 pi^2), Planck-small against the Newtonian term at every Solar-System field. The filter scale")
P("    is renormalised only through its metric dependence (Delta_h), relative Lambda^2/(16 pi^2 M_P^2) at most.")
cok = all(v["C_a_kernel_loop"] <= 1e-2 and v["C_c_delta_xi_over_xi"] <= 1e-2 and v["C_b_unfiltered_vs_Newton_0.1AU"] <= 1e-10
          for v in Crows.values())
check("C the Gaussian screening and the kernel coefficients are radiatively stable (C-a, C-c <= 1e-2; C-b <= 1e-10 of "
      "the Newtonian term at 0.1 AU), both footings, both xi floors",
      f"max C-a {max(v['C_a_kernel_loop'] for v in Crows.values()):.1e}, max C-b "
      f"{max(v['C_b_unfiltered_vs_Newton_0.1AU'] for v in Crows.values()):.1e}, max C-c "
      f"{max(v['C_c_delta_xi_over_xi'] for v in Crows.values()):.1e}", cok,
      reading="stability is not a derivation: a0's value and the a0-Lambda relation are not touched (kappa = 1/2 FITTED); "
              "the vacuum-energy fine-tuning is GR's, inherited unchanged")

# ============================================================================================ verdict
banner("VERDICT (frozen rule, FROZEN_CRITERIA.md section 3)")
lb_fail = [n for n, ok, lb in CH if lb and not ok]
controls = [n for n, ok, lb in CH if lb and n.split()[0] in ("K1", "K2", "K3", "K3b", "K4", "K5", "K6", "K7")]
ctrl_fail = [n for n, ok, lb in CH if lb and not ok and n.split()[0] in ("K1", "K2", "K3", "K3b", "K4", "K5", "K6", "K7")]
A_all = all(r["A_ok"] for r in rows); E_all = all(r["EFT_ok"] for r in rows); U_all = all(r["UV_ok"] for r in rows)
A_any = any(r["A_ok"] for r in rows); E_any = any(r["EFT_ok"] and r["A_ok"] for r in rows)
if ctrl_fail:
    verdict = "OPEN"
elif MUTATE and not b0:
    verdict = "FAIL (MUTATE: inputs outside the committed window)"
elif A_all and E_all and cok and U_all:
    verdict = "PASS"
elif cok and E_any and (sub or LHLmax > 0):
    verdict = "CONDITIONAL"
else:
    verdict = "FAIL"
OUT["verdict"] = verdict
P(f"  G12 on the filtered C-H/K chassis: {verdict}")
if verdict == "CONDITIONAL":
    P(f"  (A) natural at every point at its own Lambda_sc (max delta alpha/alpha = {S['delta_alpha_over_alpha_max']:.1e}).")
    P(f"  (B) EFT leakage <= {S['delta_EFT_max']:.1e} everywhere (bound {BOUND:g}); the worst-case UV piece passes at "
      f"{n_uv}/{len(rows)} points.")
    P(f"  Condition: the UV completion (anisotropic-scaling scale M_*) enters at M_* <= {LHLmax:.1e} GeV (Pospelov-Shang")
    P(f"  hierarchy, M_* <= Lambda_sc), or the window is restricted to Lambda_sc(alpha_c, c_2) <= {LHLmax:.1e} GeV.")
    P("  (C) the heat filter and the kernel are radiatively stable.")
n_ok = sum(ok for _, ok, _ in CH)
OUT["n_checks"] = len(CH); OUT["n_pass"] = n_ok; OUT["n_fail_load_bearing"] = len(lb_fail)
P(f"\n  load-bearing failures: {len(lb_fail)} {lb_fail if lb_fail else ''}")
P(f"  Time {time.time() - T0:.0f} s.")
P(f"\n  {n_ok}/{len(CH)} checks pass")
with open(os.path.join(HERE, f"{SLUG}_results{SUF}.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
with open(os.path.join(HERE, f"{SLUG}{SUF}.out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
sys.exit(1 if lb_fail else 0)
