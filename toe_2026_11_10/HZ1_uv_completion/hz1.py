#!/usr/bin/env python3
"""HZ1: gate T3 of the TOE0 battery. Is there a UV completion of action (A)?

Criteria: FROZEN_CRITERIA.md (committed alone, c1bc0c0977 local). TEST lane: adopts nothing.
Run:      python3 hz1.py                 -> hz1.out / hz1.json   (known answers + graded lines + reported items)
          HZ1_MUTATE=1 python3 hz1.py    -> hz1_MUTATE.out / hz1_MUTATE.json (twins M1-M5 must bite)
Units: natural (hbar = c = 1), energies in eV, unless a line says SI. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.interpolate import CubicSpline
from scipy.optimize import differential_evolution

MUTATE = os.environ.get("HZ1_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


# ---------------------------------------------------------------- constants (SI -> eV)
HBAR = 1.054571817e-34
C = 2.99792458e8
EV = 1.602176634e-19
G = 6.67430e-11
HBARC_EVM = HBAR * C / EV                       # eV m
M_PL = math.sqrt(HBAR * C / G) * C**2 / EV      # unreduced Planck mass, eV
MBAR = M_PL / math.sqrt(8 * math.pi)            # reduced
K_NAT = 4 * math.pi / M_PL**2                   # K = 4 pi G in natural units (eV^-2)
FOOTINGS = {"canonical": 9.3603e-11, "alt": 1.1312e-10}   # m/s^2
BETA_CMB = 369.82e3 / C
G_EARTH = 9.80665
G_GAL = (233e3) ** 2 / (8.2 * 3.0856775814913673e19)     # Sun's Galactic orbit, m/s^2
AU = 1.495978707e11
KPC = 3.0856775814913673e19


def e_of_a(a_si):
    """acceleration (m/s^2) -> energy hbar a / c (eV); A = a/c^2 as an inverse length times hbar c."""
    return HBAR * a_si / C / EV


say("HZ1: gate T3 (UV completion of action (A)).  MUTATE =", MUTATE)
say(f"M_Pl = {M_PL:.5e} eV, Mbar_P = {MBAR:.5e} eV, hbar c = {HBARC_EVM:.6e} eV m")
for f, a0 in FOOTINGS.items():
    say(f"  footing {f}: a0 = {a0:.5e} m/s^2 -> E_a0 = hbar a0/c = {e_of_a(a0):.5e} eV")
OUT["constants"] = {"M_Pl_eV": M_PL, "Mbar_eV": MBAR, "E_a0_eV": {f: e_of_a(a) for f, a in FOOTINGS.items()}}

# ==================================================================== known answers
say("\n=== KNOWN ANSWERS ===")
KA = {}

# ---- KA1 power counting
def coupling_dim(op_dim, z=3, d=3):
    return (z + d) - op_dim

ka1_kin = {z: coupling_dim(2 * z, z=z) for z in (1, 3)}       # operator K_ij K^ij has dimension 2z
proj_ops = {"Lambda": 0, "R": 2, "R^2": 4, "R_ij R^ij": 4, "(nabla R_ij)^2": 6, "R Delta R": 6, "R^3": 6,
            "R R_ij R^ij": 6, "R_i^j R_j^k R_k^i": 6}
nonproj_extra = {"a_i a^i": 2, "a^4": 4, "(nabla_i a^i)^2": 4, "R nabla_i a^i": 4, "a^i Delta a_i": 4,
                 "a^6": 6, "(Delta a_i)^2": 6, "a^2 (nabla a)^2": 6, "R a^4": 6, "R_ij a^i a^j R": 6,
                 "lapse potential V(N) [mu_K term]": 0}
proj_ok = all(coupling_dim(d) >= 0 for d in proj_ops.values())
nonproj_ok = all(coupling_dim(d) >= 0 for d in nonproj_extra.values())
KA["KA1"] = {"[1/kappa^2] z=1": ka1_kin[1], "[1/kappa^2] z=3": ka1_kin[3], "projectable list all >= 0": proj_ok,
             "pass": ka1_kin[1] == 2 and ka1_kin[3] == 0 and proj_ok}
say(f"KA1 [1/kappa^2] = d - z: z=1 -> {ka1_kin[1]} (M_P^2), z=3 -> {ka1_kin[3]} (marginal); projectable z=3 "
    f"potential couplings all >= 0: {proj_ok}; non-projectable additions (incl. V(N)) all >= 0: {nonproj_ok}"
    f"  -> {'PASS' if KA['KA1']['pass'] else 'FAIL'}")
say("    (note: the criteria file prints the formula as 'z - d'; the values it names, 0 at z = 3 and 2 at z = 1,"
    " are d - z, which is what is checked)")

# ---- KA2a: conformally flat 3-metric Ricci scalar, then static weak-field limit -> G_N = G/(1 - alpha/2)
x, y, z = sp.symbols("x y z", real=True)
psi = sp.Function("psi")(x, y, z)
crd = [x, y, z]
gmat = sp.exp(-2 * psi) * sp.eye(3)
ginv = gmat.inv()
Gam = [[[sum(ginv[i, l] * (sp.diff(gmat[l, j], crd[k]) + sp.diff(gmat[l, k], crd[j]) - sp.diff(gmat[j, k], crd[l]))
             for l in range(3)) / 2 for k in range(3)] for j in range(3)] for i in range(3)]


def ricci(i, j):
    r = 0
    for k in range(3):
        r += sp.diff(Gam[k][i][j], crd[k]) - sp.diff(Gam[k][i][k], crd[j])
        for l in range(3):
            r += Gam[k][k][l] * Gam[l][i][j] - Gam[k][j][l] * Gam[l][i][k]
    return r


R3 = sp.simplify(sum(ginv[i, j] * ricci(i, j) for i in range(3) for j in range(3)))
lap = sum(sp.diff(psi, c_, 2) for c_ in crd)
grad2 = sum(sp.diff(psi, c_) ** 2 for c_ in crd)
ka2a_res = sp.simplify(R3 - sp.exp(2 * psi) * (4 * lap - 2 * grad2))
# 1-d static weak field: N = 1 + eps Phi, gamma = exp(-2 eps psi); L = N sqrt(gamma) R3/(16 pi G) + alpha a^2/(16 pi G) - rho Phi
eps, alph, Gs, rho = sp.symbols("epsilon alpha G rho", positive=True)
X = sp.symbols("X", real=True)
Ph = sp.Function("Phi")(X)
ps = sp.Function("psi")(X)
R3_1d = sp.exp(2 * eps * ps) * (4 * sp.diff(eps * ps, X, 2) - 2 * sp.diff(eps * ps, X) ** 2)
Lgr = (1 + eps * Ph) * sp.exp(-3 * eps * ps) * R3_1d / (16 * sp.pi * Gs)
L2 = sp.series(Lgr, eps, 0, 3).removeO().coeff(eps, 2)
L2 += alph * sp.diff(Ph, X) ** 2 / (16 * sp.pi * Gs) - rho * Ph
from sympy.calculus.euler import euler_equations
eqs = euler_equations(L2, [Ph, ps], X)
sol = sp.solve([e.lhs for e in eqs], [sp.diff(Ph, X, 2), sp.diff(ps, X, 2)], dict=True)[0]
GN_ratio = sp.simplify(sol[sp.diff(Ph, X, 2)] / (4 * sp.pi * Gs * rho))
ka2a_pass = sp.simplify(ka2a_res) == 0 and sp.simplify(GN_ratio - 1 / (1 - alph / 2)) == 0
# ---- KA2b: FRW minisuperspace gives lambda = 1
t = sp.symbols("t", real=True)
a = sp.Function("a")(t)
N = sp.Function("N")(t)
lam = sp.symbols("lambda", real=True)
# Ricci scalar of -N^2 dt^2 + a^2 dx^2 (standard closed form), times sqrt(-g) = N a^3
adot, addot, Ndot = sp.diff(a, t), sp.diff(a, t, 2), sp.diff(N, t)
R4 = 6 * (addot / (a * N**2) + adot**2 / (a**2 * N**2) - adot * Ndot / (a * N**3))
L_EH = N * a**3 * R4
L_HL = N * a**3 * (3 - 9 * lam) * adot**2 / (a**2 * N**2)
e_EH = [sp.simplify(e.lhs) for e in euler_equations(L_EH, [a, N], t)]
e_HL = [sp.simplify(e.lhs) for e in euler_equations(L_HL, [a, N], t)]
lam_sol = sp.solve(sp.simplify(e_EH[1] - e_HL[1]), lam)
ka2b_pass = lam_sol == [1] and sp.simplify((e_EH[0] - e_HL[0]).subs(lam, 1)) == 0
KA["KA2"] = {"R3 conformal residual": str(ka2a_res), "G_N/G": str(GN_ratio), "lambda from FRW": [str(s) for s in lam_sol],
             "pass": bool(ka2a_pass and ka2b_pass)}
say(f"KA2 R^(3) of exp(-2psi) delta = exp(2psi)(4 Lap psi - 2|grad psi|^2): residual {ka2a_res}; "
    f"static weak field with alpha a^2: G_N/G = {GN_ratio} (BPS: 1/(1 - alpha/2)); FRW: lambda = {lam_sol}"
    f"  -> {'PASS' if KA['KA2']['pass'] else 'FAIL'}")

# ---- KA3: QX17's J with GR gives mu = x/(1+x); also (A)'s Horava coefficients
u, Kk, a0s, Aa = sp.symbols("u K a0 A", positive=True)
Jfun = u - sp.log(1 + u)
L_law = -Aa**2 / (2 * Kk) + (a0s**2 / Kk) * Jfun.subs(u, Aa / a0s)
mu_law = sp.simplify(-(Kk / Aa) * sp.diff(L_law, Aa))
ka3_pass = sp.simplify(mu_law - (Aa / a0s) / (1 + Aa / a0s)) == 0
alpha_u = sp.simplify(4 * Jfun / u**2)                    # (a0^2/K) J = (1/4K) alpha A^2
alpha_par = sp.simplify(2 * sp.diff(Jfun, u, 2))
alpha_perp = sp.simplify(2 * sp.diff(Jfun, u) / u)
a_lim0 = [sp.limit(e, u, 0) for e in (alpha_u, alpha_par, alpha_perp)]
KA["KA3"] = {"mu": str(mu_law), "pass": bool(ka3_pass)}
say(f"KA3 mu from GR + (a0^2/K) J(u): {mu_law}  -> {'PASS' if ka3_pass else 'FAIL'}")
OUT["A_as_horava"] = {"lambda": 1, "beta": 0, "xi": 1, "alpha(u)": str(alpha_u), "alpha_par(u)": str(alpha_par),
                      "alpha_perp(u)": str(alpha_perp), "alpha at A=0 (alpha, par, perp)": [str(v) for v in a_lim0]}
say(f"(A) as Horava: lambda = 1, beta = 0 (c_T = 1), xi = 1; alpha(u) = {alpha_u}, alpha_par = {alpha_par}, "
    f"alpha_perp = {alpha_perp}; at A = 0: {a_lim0}")
cchi2 = lambda al, be, la: (be + la - 1) * (2 - al) / (al * (1 - be) * (2 + be + 3 * (la - 1)))
say(f"    khronon speed^2 (khronometric form, Jacobson 1310.5115, PROVISIONAL) at (alpha 2, beta 0, lambda 1): "
    f"{cchi2(2.0, 0.0, 1.0)}; quadratic lapse-gradient coefficient 1 - alpha_par(0)/2 = {1 - a_lim0[1] / 2}")

# ---- KA4 textbook one-loop
mp.mp.dps = 30
m_t = mp.mpf("1.7")
num = mp.quad(lambda k: m_t**2 / (k**2 + m_t**2), [0, mp.inf])
ka4a_rel = float(abs(num / (m_t * mp.pi / 2) - 1))
# d V3/dm^2 = (1/(4pi^2)) Int k^2/(k^2+m^2) dk; non-analytic part = -(1/(4 pi^2)) Int m^2/(k^2+m^2) = -m/(8 pi)
# -> V3 non-analytic = -m^3/(12 pi)
coef_m3 = -float(num) / (4 * math.pi**2) / float(m_t) * (2.0 / 3.0)   # integrate -c m dm^2 = -(2/3) c m^3
ka4a_pass = ka4a_rel < 1e-6 and abs(coef_m3 / (-1 / (12 * math.pi)) - 1) < 1e-6


def JB(yv):
    return mp.quad(lambda s: s**2 * mp.log(1 - mp.exp(-mp.sqrt(s**2 + yv))), [0, 1, 5, 40])


ab = 16 * mp.pi**2 * mp.exp(mp.mpf(3) / 2 - 2 * mp.euler)
c32 = []
for yv in (mp.mpf("1e-4"), mp.mpf("4e-4"), mp.mpf("1e-3")):
    rest = JB(yv) - (-mp.pi**4 / 45 + mp.pi**2 * yv / 12 - yv**2 / 32 * mp.log(yv / ab))
    c32.append(float(rest / yv**1.5))
ka4b_rel = abs(c32[0] / (-math.pi / 6) - 1)
ka4b_pass = ka4b_rel < 1e-3
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]], complex)
s3 = np.array([[1, 0], [0, -1]], complex); I2 = np.eye(2)
kr = lambda *ms: ms[0] if len(ms) == 1 else np.kron(ms[0], kr(*ms[1:]))
GAM = [kr(s1, I2, I2), kr(s2, I2, I2), kr(s3, s1, I2), kr(s3, s2, I2), kr(s3, s3, s1), kr(s3, s3, s2)]
anti = max(np.abs(GAM[i] @ GAM[j] + GAM[j] @ GAM[i] - 2 * (i == j) * np.eye(8)).max() for i in range(6) for j in range(6))
rng = np.random.default_rng(7)
dets = []
for _ in range(5):
    kv, Av, gF = rng.normal(size=3), rng.normal(size=3), abs(rng.normal()) + 0.3
    D = 1j * (sum(kv[i] * GAM[i] for i in range(3)) + gF * sum(Av[i] * GAM[3 + i] for i in range(3)))
    dets.append(abs(np.linalg.det(D) / (kv @ kv + gF**2 * Av @ Av) ** 4 - 1))
ka4c_pass = anti < 1e-12 and max(dets) < 1e-10
KA["KA4"] = {"a_rel": ka4a_rel, "a_m3_coef": coef_m3, "b_y32_coefs": c32, "b_rel": ka4b_rel,
             "c_anticomm": float(anti), "c_det_rel_max": float(max(dets)),
             "pass": bool(ka4a_pass and ka4b_pass and ka4c_pass)}
say(f"KA4a 3-d: Int m^2/(k^2+m^2) / (pi m/2) - 1 = {ka4a_rel:.1e}; V3 non-analytic coefficient {coef_m3:.10f} "
    f"vs -1/(12 pi) = {-1/(12*math.pi):.10f} -> {'PASS' if ka4a_pass else 'FAIL'}")
say(f"KA4b thermal: y^(3/2) coefficient of J_B at y = 1e-4, 4e-4, 1e-3: {[round(v, 6) for v in c32]} vs -pi/6 = "
    f"{-math.pi/6:.6f} (rel {ka4b_rel:.1e} at the smallest y) -> {'PASS' if ka4b_pass else 'FAIL'}")
say(f"KA4c Cl(6) 8x8: anticommutator error {anti:.1e}; det D/(k^2+g^2A^2)^4 - 1 max {max(dets):.1e} -> "
    f"{'PASS' if ka4c_pass else 'FAIL'}")
KA_ALL = all(v["pass"] for v in KA.values())
OUT["known_answers"] = KA
say(f"KNOWN ANSWERS ALL PASS: {KA_ALL}")

# ==================================================================== (i) J as a UV term
say("\n=== (i) J AS A UV TERM ===")


def uv_admissible(expr, var, order=13):
    ser = sp.series(expr, var, 0, order).removeO()
    co = {n: sp.nsimplify(ser.coeff(var, n)) for n in range(0, order)}
    odd = [n for n, v in co.items() if n % 2 == 1 and v != 0]
    high = [n for n, v in co.items() if n >= 7 and v != 0]
    poly = sp.simplify(expr - ser) == 0
    return {"odd_orders": odd, "orders_ge_7": high, "terminates": bool(poly),
            "admissible": (not odd) and (not high) and bool(poly)}


det_J = uv_admissible(Jfun, u)
pW = sp.symbols("p", positive=True)
det_W = uv_admissible(-pW - sp.log(1 - pW), pW)
Pi = sp.symbols("Pi", real=True)
F_left, F_right = sp.Integer(0), Pi**2 / 2               # F = max(Pi, 0)^2 / 2
F2_jump = sp.diff(F_right, Pi, 2) - sp.diff(F_left, Pi, 2)
J_in_UV = det_J["admissible"]
say(f"J1/J2 on J(u) = u - ln(1+u): odd orders {det_J['odd_orders'][:4]}..., orders >= 7 {det_J['orders_ge_7'][:3]}..., "
    f"terminates {det_J['terminates']} -> admissible as a z = 3 UV term: {J_in_UV}")
say(f"   Legendre form W(p) = -p - ln(1-p): odd {det_W['odd_orders'][:3]}..., >= 7 {det_W['orders_ge_7'][:2]}..., "
    f"radius 1 (the flux cap) -> admissible: {det_W['admissible']}")
say(f"   stiffness F = max(Pi,0)^2/2: F'' jumps by {F2_jump} at Pi = 0 (non-analytic switch)")
OUT["J_in_UV"] = {"J": det_J, "W": det_W, "F_second_derivative_jump": str(F2_jump)}

# ==================================================================== (i) generation candidates
say("\n=== (i) GENERATION CANDIDATES (one-loop determinants) ===")
XG = np.logspace(-2, 2, 41)
MU_LAW = XG / (1 + XG)
SLOPE_LAW = 1 / (1 + 0.01)


def jb_prime_grid(fermion=False):
    sgn = -1.0 if fermion else 1.0          # boson: e^E - 1 ; fermion: e^E + 1 (both give dV/dm^2 > 0)
    ys = np.logspace(-14, 3.5, 360)
    vals = []
    for yv in ys:
        f = lambda s: 0.5 * s**2 / (math.sqrt(s * s + yv) * (math.exp(math.sqrt(s * s + yv)) - sgn))
        vals.append(quad(f, 0, 60 + math.sqrt(yv), limit=400, epsabs=0, epsrel=1e-11)[0])
    return CubicSpline(np.log(ys), np.log(np.array(vals))), ys[0], ys[-1], vals[0]


SPL_B = jb_prime_grid(False)
SPL_F = jb_prime_grid(True)


def jp(spl, yv):
    s, lo, hi, v0 = spl
    yv = np.asarray(yv, float)
    out = np.where(yv <= lo, v0, np.exp(s(np.log(np.clip(yv, lo, hi)))))
    return np.where(yv >= hi, 0.0, out)


# each candidate: mu(x; params); params bounded; sign of the |A|^3 coefficient in L (per unit positive coupling)
CANDS = {
    "G1 leaf scalar": dict(mu=lambda x, p: 1 - p[0] / 2 - 3 * p[1] * x, bounds=[(-10, 10), (0, 100)],
                           cubic_sign=+1, note="L_ind = +nu g^3 |A|^3/(12 pi)"),
    "G2 leaf Cl(6) fermion": dict(mu=lambda x, p: 1 - p[0] / 2 + 3 * p[1] * x, bounds=[(-10, 10), (0, 100)],
                                  cubic_sign=-1, note="L_ind = -8 nu g^3 |A|^3/(12 pi)"),
    "G3 leaf boson-fermion pair": dict(
        mu=lambda x, p: 1 - p[0] / 2 - p[1] * (np.sqrt(1 + (10**p[2] * x) ** 2) - 10**p[2] * x),
        bounds=[(-10, 10), (0, 10), (-3, 3)], cubic_sign=-1, note="L_ind |A|^3 part = -nu g_B^3 |A|^3/(12 pi)"),
    "G4 thermal boson": dict(mu=lambda x, p: 1 - p[0] / 2 + p[1] * jp(SPL_B, (10**p[2] * x) ** 2),
                             bounds=[(-10, 10), (0, 100), (-3, 3)], cubic_sign=+1, note="L_ind = +T g^3|A|^3/(12 pi)"),
    "G4' thermal fermion": dict(mu=lambda x, p: 1 - p[0] / 2 + p[1] * jp(SPL_F, (10**p[2] * x) ** 2),
                                bounds=[(-10, 10), (0, 100), (-3, 3)], cubic_sign=0, note="no zero mode: no |A|^3"),
    "G5 4-d CW boson": dict(mu=lambda x, p: 1 - p[0] / 2 + p[1] * x**2 * (2 * np.log(x / 10**p[2]) - 1),
                            bounds=[(-10, 10), (0, 100), (-3, 3)], cubic_sign=0, note="A^4 ln A: no |A|^3"),
    "G5' 4-d CW fermion": dict(mu=lambda x, p: 1 - p[0] / 2 - p[1] * x**2 * (2 * np.log(x / 10**p[2]) - 1),
                               bounds=[(-10, 10), (0, 100), (-3, 3)], cubic_sign=0, note="A^4 ln A: no |A|^3"),
}
if MUTATE:
    CANDS["M1 G2 with boson statistics"] = dict(mu=lambda x, p: 1 - p[0] / 2 - 3 * p[1] * x,
                                                bounds=[(-10, 10), (0, 100)], cubic_sign=+1, note="twin M1")
    CANDS["M4 G3 without its boson"] = dict(mu=lambda x, p: 1 - p[0] / 2 + p[1] * 10**p[2] * x,
                                            bounds=[(-10, 10), (0, 10), (-3, 3)], cubic_sign=-1, note="twin M4")


def shape_stats(mufun, p):
    mu = mufun(XG, p)
    band = float(np.max(np.abs(mu - MU_LAW)))
    h = 1e-4
    m1, m2 = mufun(np.array([0.01 * math.exp(h)]), p)[0], mufun(np.array([0.01 * math.exp(-h)]), p)[0]
    slope = float((math.log(m1) - math.log(m2)) / (2 * h)) if (m1 > 0 and m2 > 0) else float("nan")
    q = max(band / 0.1, abs(slope - SLOPE_LAW) / 0.1) if np.isfinite(slope) else 1e3 + band
    return band, slope, q


def fit(c):
    res = differential_evolution(lambda p: shape_stats(c["mu"], p)[2], c["bounds"], seed=0, tol=1e-10,
                                 maxiter=600, popsize=30, polish=True)
    band, slope, q = shape_stats(c["mu"], res.x)
    # also the best band alone (no slope condition), reported
    res2 = differential_evolution(lambda p: shape_stats(c["mu"], p)[0], c["bounds"], seed=1, tol=1e-10,
                                  maxiter=600, popsize=30, polish=True)
    return res.x, band, slope, q, float(res2.fun)


def needed_vs_ceiling(name, p, E_a0, a0_override=None):
    """coupling combination the fit needs vs the natural ceiling; returns log10 R_c and a description.
    p: fitted params. E_a0: a0 as an energy (eV). Natural units, 1/K = M_Pl^2/(4 pi)."""
    Ea = E_a0 if a0_override is None else a0_override
    invK = M_PL**2 / (4 * math.pi)
    nmax, gmax = 1000.0, 4 * math.pi
    if name.startswith("G3") or name.startswith("M4"):
        B, cc = p[1], 10**p[2]
        need = B * cc * invK * 4 * math.pi / Ea           # nu g_B^3 = 4 pi B c/(K a0)
        ceil = nmax * M_PL * gmax**3
        return math.log10(need / ceil), f"nu g_B^3 needed {need:.3e} eV vs ceiling N nu g^3 = {ceil:.3e} eV"
    if name.startswith("G1") or name.startswith("G2") or name.startswith("M1"):
        # match J's cubic: L coefficient 1/(3 K a0) = (8 or 1) nu g^3/(12 pi)
        mult = 8.0 if name.startswith("G2") else 1.0
        need = 12 * math.pi * invK / (3 * Ea) / mult
        ceil = nmax * M_PL * gmax**3
        return math.log10(need / ceil), f"nu g^3 needed {need:.3e} eV vs ceiling {ceil:.3e} eV"
    if name.startswith("G4"):
        # bump B4 = K g^2 T^2/pi^2 (or /2pi^2-type for fermions, same order) with T = g a0/c4: g^4 = pi^2 B c4^2/(K a0^2)
        B, c4 = max(p[1], 1e-30), 10**p[2]
        g4 = math.pi**2 * max(B, 1.0) * c4**2 * invK / Ea**2
        g_need = (g4 / nmax) ** 0.25
        T_need = g_need * Ea / c4
        r = max(g_need / gmax, T_need / M_PL)
        return math.log10(r), f"g needed {g_need:.3e} (T = {T_need:.3e} eV) for a unit bump"
    if name.startswith("G5"):
        g4 = 16 * math.pi**2 * invK / Ea**2                # |B5| = K g^4 a0^2/(16 pi^2) = 1
        g_need = (g4 / nmax) ** 0.25
        return math.log10(g_need / gmax), f"g needed {g_need:.3e} for |B5| = 1"
    return float("nan"), ""


def pc_ok(name):
    # leaf fields with leaf density [nu_0] = z = 3: [g_B^2] = 0, [m0^2] = 2, [g_F] = 0 (see criteria); thermal and CW
    # couplings A^2 chi^2 at z = 3 with [chi] = 0: coupling dimension 6 - 2 - 3 (time kinetic) ... all >= 0
    dims = {"g_B^2": 6 - 3 - 3 + 0, "m0^2": 2, "g_F": 6 - 3 - 1 - 2, "g^2 (bulk, z=3)": 6 - 2}
    return all(v >= 0 for v in dims.values()), dims


CAND_RES = {}
for name, c in CANDS.items():
    p, band, slope, q, band_only = fit(c)
    sign_ok = c["cubic_sign"] < 0
    shape_ok = q <= 1.0
    pc, dims = pc_ok(name)
    per = {}
    for f, a0 in FOOTINGS.items():
        lr, desc = needed_vs_ceiling(name, p, e_of_a(a0))
        per[f] = {"log10_Rc": lr, "desc": desc}
    coef_ok = all(v["log10_Rc"] <= 0 for v in per.values())
    passes = sign_ok and shape_ok and coef_ok and pc
    CAND_RES[name] = {"params": [float(v) for v in p], "band": band, "slope_x0.01": slope, "Q": q,
                      "best_band_without_slope": band_only, "sign_ok": sign_ok, "shape_ok": shape_ok,
                      "power_counting_ok": pc, "coefficient": per, "coef_ok": coef_ok, "passes": passes,
                      "note": c["note"]}
    say(f"{name}: [{c['note']}]")
    say(f"   sign (|A|^3 coefficient in L must be < 0): {'ok' if sign_ok else 'FAIL'} (sign {c['cubic_sign']:+d});"
        f" best fit params {np.round(p, 4).tolist()}: max|dmu| {band:.4f}, deep slope {slope:.4f} (law 0.9901), "
        f"Q {q:.3f} -> shape {'ok' if shape_ok else 'FAIL'}; best band alone {band_only:.4f}")
    for f in FOOTINGS:
        say(f"   {f}: log10 R_c = {per[f]['log10_Rc']:.2f}  ({per[f]['desc']})  -> coefficient "
            f"{'ok' if per[f]['log10_Rc'] <= 0 else 'FAIL'}")
    say(f"   power counting {dims} -> {'ok' if pc else 'FAIL'};  candidate {'PASSES' if passes else 'fails'} (i)")

OUT["candidates"] = CAND_RES
graded = {k: v for k, v in CAND_RES.items() if k.startswith("G")}
any_pass = any(v["passes"] for v in graded.values())
if not KA_ALL:
    lab_i = "OPEN"
elif any_pass:
    lab_i = "PASS"
elif not J_in_UV:
    lab_i = "FAIL"
else:
    lab_i = "OPEN"
say(f"(i) LABEL: {lab_i}  (J admissible as UV term: {J_in_UV}; any candidate passing all four tests: {any_pass})")

# ---- M3 twin: a0 -> M_Pl in G3's coefficient test
if MUTATE:
    g3 = CAND_RES["G3 leaf boson-fermion pair"]
    lr_m3, d_m3 = needed_vs_ceiling("G3", g3["params"], None, a0_override=M_PL)
    OUT["M3"] = {"log10_Rc": lr_m3, "bites": lr_m3 <= 0}
    say(f"M3 (a0 -> M_Pl in G3's coefficient): log10 R_c = {lr_m3:.2f} -> coefficient "
        f"{'PASSES (twin bites)' if lr_m3 <= 0 else 'still fails (twin does NOT bite)'}")
    m2 = uv_admissible(u**2 / 2 + u**4 / 4 + u**6 / 6, u)
    OUT["M2"] = {"detector": m2, "bites": m2["admissible"]}
    say(f"M2 (even degree-6 polynomial fed to the J1/J2 detector): admissible = {m2['admissible']} -> "
        f"{'twin bites' if m2['admissible'] else 'twin does NOT bite'}")
    m1 = CAND_RES["M1 G2 with boson statistics"]
    OUT["M1"] = {"sign_ok": m1["sign_ok"], "bites": not m1["sign_ok"]}
    say(f"M1 (G2 with boson statistics): sign {'ok' if m1['sign_ok'] else 'FAIL'} -> "
        f"{'twin bites' if not m1['sign_ok'] else 'twin does NOT bite'}")
    m4 = CAND_RES["M4 G3 without its boson"]
    OUT["M4"] = {"shape_ok": m4["shape_ok"], "Q": m4["Q"], "bites": not m4["shape_ok"]}
    say(f"M4 (G3 without its boson): shape {'ok' if m4['shape_ok'] else 'FAIL'} (Q {m4['Q']:.2f}) -> "
        f"{'twin bites' if not m4['shape_ok'] else 'twin does NOT bite'}")

# ==================================================================== (ii) percolation, (iii) window
say("\n=== (ii) PERCOLATION and (iii) WINDOW ===")
BOUNDS = {"photon kappa_tr": 1e-20, "electron c_TT": 1e-21, "proton c_TT": 1e-22,
          "neutron via boost (c_Z/beta^2)": 1e-29 / BETA_CMB**2}
if MUTATE:
    BOUNDS = {k: 1e-60 for k in BOUNDS}
say("bounds (KR v19 S2/S3, PROVISIONAL): " + ", ".join(f"{k} {v:.2e}" for k, v in BOUNDS.items()))


def m_hi(bound, Cc, alv):
    return MBAR * math.sqrt(16 * math.pi**2 * bound / (Cc * alv))


M_LO_EW = HBARC_EVM / 38.6e-6
M_LO_GW = 2 * math.pi * HBAR * 100.0 / EV * math.sqrt(1e15)
M_LO = max(M_LO_EW, M_LO_GW)
say(f"M_lo: short-range gravity hbar c/38.6 um = {M_LO_EW:.3e} eV; GW z=3 dispersion at 100 Hz -> {M_LO_GW:.3e} eV;"
    f" M_lo = {M_LO:.3e} eV")
WIN = {}
for f, a0 in FOOTINGS.items():
    u_e, u_g = G_EARTH / a0, G_GAL / a0
    al = {"A=0 (graded)": 2.0, "Earth alpha_perp": 2 / (1 + u_e), "Galaxy alpha_perp": 2 / (1 + u_g),
          "Galaxy enhanced": (2 / (1 + u_g)) / (2 - 2 / (1 + u_g) ** 2)}
    rows = {}
    for Cc in (1e-3, 1.0, 1e3):
        for an, av in al.items():
            mh = {k: m_hi(b, Cc, av) for k, b in BOUNDS.items()}
            mh["c_T (GW170817)"] = m_hi(1e-15, Cc, av)
            mh["PPN alpha_2 (pulsar)"] = m_hi(1.6e-9, Cc, av)
            mh["lambda-1 (L350)"] = m_hi(6e-4, Cc, av)
            top = min(mh.values())
            lo_uv = max(M_LO, HBARC_EVM / (1e4 * math.sqrt(1.6e-9)), HBARC_EVM / (AU * math.sqrt(1.6e-9)))
            rows[f"C={Cc:g} | {an}"] = {"M_hi_eV": top, "M_hi_GeV": top / 1e9, "binding": min(mh, key=mh.get),
                                        "caps_GeV": {k: v / 1e9 for k, v in mh.items()},
                                        "M_lo_eV": lo_uv, "nonempty": top > lo_uv,
                                        "log10_width": math.log10(top / lo_uv) if top > 0 else None}
    WIN[f] = {"u_earth": u_e, "u_gal": u_g, "alpha_LV": al, "rows": rows}
    say(f"[{f}] u_Earth {u_e:.3e} (alpha_perp {al['Earth alpha_perp']:.2e}), u_Gal {u_g:.3f} "
        f"(alpha_perp {al['Galaxy alpha_perp']:.3f}, enhanced {al['Galaxy enhanced']:.3f})")
    for k, r in rows.items():
        say(f"   {k:36s} M_hi = {r['M_hi_GeV']:.3e} GeV (binding: {r['binding']}), M_lo = {r['M_lo_eV']:.2e} eV,"
            f" window {'NON-EMPTY' if r['nonempty'] else 'EMPTY'}"
            + (f", {r['log10_width']:.1f} decades" if r['log10_width'] is not None else ""))
        if "A=0" in k and k.startswith("C=1000"):
            say("      caps at C=1e3, alpha 2 (GeV): " + ", ".join(f"{kk} {vv:.2e}" for kk, vv in r["caps_GeV"].items()))


def lab(Cpass, Cfail):
    ok = [WIN[f]["rows"][f"C={Cpass:g} | A=0 (graded)"]["nonempty"] for f in FOOTINGS]
    bad = [not WIN[f]["rows"][f"C={Cfail:g} | A=0 (graded)"]["nonempty"] for f in FOOTINGS]
    return "PASS" if all(ok) else ("FAIL" if any(bad) else "OPEN")


# (ii): percolation bounds only; (iii): with gravity's own limits. Both graded at alpha_LV = 2.
def lab_ii():
    res = []
    for f in FOOTINGS:
        for Cc in (1e3, 1e-3):
            top = min(m_hi(b, Cc, 2.0) for b in BOUNDS.values())
            res.append((f, Cc, top > M_LO))
    if all(r[2] for r in res if r[1] == 1e3):
        return "PASS"
    if any(not r[2] for r in res if r[1] == 1e-3):
        return "FAIL"
    return "OPEN"


lab_ii_v, lab_iii_v = lab_ii(), lab(1e3, 1e-3)
say(f"(ii) LABEL: {lab_ii_v};  (iii) LABEL: {lab_iii_v}")


def window_labels(bval):
    """(ii)/(iii) labels with every matter bound set to bval (alpha_LV = 2); gravity caps unchanged."""
    out = {}
    for which in ("ii", "iii"):
        ne = {}
        for Cc in (1e-3, 1e3):
            caps = [m_hi(bval, Cc, 2.0)]
            if which == "iii":
                caps += [m_hi(1e-15, Cc, 2.0), m_hi(1.6e-9, Cc, 2.0), m_hi(6e-4, Cc, 2.0)]
            ne[Cc] = min(caps) > M_LO
        out[which] = "PASS" if ne[1e3] else ("FAIL" if not ne[1e-3] else "OPEN")
        out[which + "_top_C1e-3_eV"] = min([m_hi(bval, 1e-3, 2.0)])
    return out


if MUTATE:
    m5 = window_labels(1e-60)
    m5p = window_labels(1e-70)
    OUT["M5"] = {**m5, "bites_as_frozen": m5["iii"] == "FAIL"}
    OUT["M5prime_post_hoc_A1"] = {**m5p, "bites": m5p["iii"] == "FAIL"}
    say(f"M5 (bounds 1e-60, frozen): (ii) {m5['ii']}, (iii) {m5['iii']}; top at C=1e-3 {m5['ii_top_C1e-3_eV']:.2e} eV "
        f"vs M_lo {M_LO:.2e} eV -> {'twin bites' if m5['iii'] == 'FAIL' else 'twin does NOT bite as frozen (OPEN, not FAIL)'}")
    say(f"M5' (bounds 1e-70, POST HOC, amendment A1): (ii) {m5p['ii']}, (iii) {m5p['iii']}; top at C=1e-3 "
        f"{m5p['ii_top_C1e-3_eV']:.2e} eV -> {'twin bites' if m5p['iii'] == 'FAIL' else 'twin does NOT bite'}")
OUT["window"] = WIN
OUT["M_lo"] = {"eotwash_eV": M_LO_EW, "gw_eV": M_LO_GW}
# matter's own dimension-6 LV if matter keeps z = 1: Planck-suppressed, E_QG,2 ~ 4 pi Mbar / sqrt(C)
say(f"reported: matter keeps z = 1; its one-loop dimension-6 LV scale ~ 4 pi Mbar/sqrt(C) = "
    f"{4*math.pi*MBAR/math.sqrt(1e3)/1e9:.2e}-{4*math.pi*MBAR/math.sqrt(1e-3)/1e9:.2e} GeV (Fermi GRB 090510 quadratic "
    f"bound ~1.3e11 GeV, PROVISIONAL)")
top_g = WIN["canonical"]["rows"]["C=1 | A=0 (graded)"]["M_hi_eV"]
say(f"reported, T2's ground: with alpha = 2 at A = 0 the lapse's k^2 term vanishes; if only the z = 3 term is left the "
    f"exchange is strong below ~M_*^2/Mbar_P = {top_g**2/MBAR/1e9:.2e} GeV at the window top (C = 1, canonical); "
    f"estimate only, not graded")

# ==================================================================== T3 label
if lab_i == "FAIL" or lab_ii_v == "FAIL" or lab_iii_v == "FAIL":
    T3 = "FAIL"
elif lab_i == lab_ii_v == lab_iii_v == "PASS":
    T3 = "PASS"
else:
    T3 = "OPEN"
say(f"\nT3 LABEL: {T3}   [(i) {lab_i}, (ii) {lab_ii_v}, (iii) {lab_iii_v}]")
OUT["labels"] = {"T3": T3, "i": lab_i, "ii": lab_ii_v, "iii": lab_iii_v}

# ==================================================================== reported R1, R2
say("\n=== REPORTED ===")
g3 = CAND_RES["G3 leaf boson-fermion pair"]
nu, gB, m0, Kc, Lam, Gn, cfit = sp.symbols("nu g_B m0 K Lambda G c", positive=True)
a0_uv = m0 / (cfit * gB)            # crossover: g_B a0 / m0 = c
tuning = sp.Eq(Kc * nu * gB**2 * m0 / (4 * sp.pi), 1)   # bump B = 1 (alpha = 2 at A = 0)
rho_de = Lam / (8 * sp.pi * Gn)
kappa_uv = sp.simplify(a0_uv / sp.sqrt(Gn * rho_de))
dk = [sp.simplify(sp.diff(kappa_uv, v)) for v in (Lam, m0, gB)]
say(f"R1 kappa in G3: a0 = m0/(c g_B), rho_DE = Lambda/(8 pi G), kappa = {kappa_uv}; d kappa/d(Lambda, m0, g_B) = "
    f"{[str(v) for v in dk]} (none zero; Lambda and m0 are independent relevant couplings, the tuning {tuning} "
    f"fixes nu, not Lambda) -> kappa NOT fixed. 5.41: integration constant of (E3) -> NOT fixed.")
OUT["R1"] = {"kappa_uv": str(kappa_uv), "derivs": [str(v) for v in dk], "kappa_fixed": False, "share_fixed": False}
R2 = {}
for f in FOOTINGS:
    tops = [WIN[f]["rows"][f"C={Cc:g} | A=0 (graded)"]["M_hi_eV"] for Cc in (1e-3, 1.0, 1e3)]
    for v in (100e3, 300e3):
        lens = [HBARC_EVM / M * math.sqrt(C / v) for M in (M_LO, *tops)]
        R2[f"{f} v={v/1e3:.0f} km/s"] = {"ell_m_at_[M_lo, M_hi(C=1e-3,1,1e3)]": lens,
                                         "log10_ratio_to_fold": [math.log10(l / (1e-5 * KPC)) for l in lens]}
        say(f"R2 [{f}, v = {v/1e3:.0f} km/s] z=3 dispersion length ell = (hbar c/M_*) sqrt(c/v): "
            f"{lens[0]:.2e} m at M_lo, {lens[2]:.2e} m at M_hi(C=1); COL1 fold scale 1e-5 kpc = {1e-5*KPC:.2e} m; "
            f"log10 ratio {math.log10(lens[0]/(1e-5*KPC)):.1f} to {math.log10(lens[2]/(1e-5*KPC)):.1f}")
say("R2 the z = 3 terms are terms of an action: they conserve the clock's energy and remove none of its infall energy; "
    "they turn the fold into a dispersive (wave) caustic at ell, not a standing clock. COL1's 1-4 % charge deficit is "
    "set on kpc scales and does not depend on the caustic's microphysics.")
OUT["R2"] = R2

# ==================================================================== write
tag = "hz1_MUTATE" if MUTATE else "hz1"
with open(os.path.join(HERE, tag + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, tag + ".out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
