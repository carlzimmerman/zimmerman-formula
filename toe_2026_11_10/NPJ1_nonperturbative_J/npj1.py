#!/usr/bin/env python3
"""NPJ1: a non-perturbative origin for the law's function J? (T3(i) of TOE0; HZ1's open door)

Criteria: FROZEN_CRITERIA.md (committed alone, local 249f297cd0). TEST lane: adopts nothing.
Run:  python3 npj1.py                -> npj1.out / npj1.json   (known answers + graded lines + reported items)
      NPJ1_MUTATE=1 python3 npj1.py  -> npj1_MUTATE.out / npj1_MUTATE.json (twins M1-M7 must bite)
Units: natural (hbar = c = 1), energies in eV, unless a line says SI. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import resource
import time

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.optimize import differential_evolution, minimize_scalar

T_START = time.time()
MUTATE = os.environ.get("NPJ1_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    LINES.append(s)
    print(s, flush=True)


# ============================================================== constants (SI -> eV)
HBAR = 1.054571817e-34
C = 2.99792458e8
EV = 1.602176634e-19
G = 6.67430e-11
GM_SUN = 1.32712440018e20                       # m^3/s^2
KPC = 3.0856775814913673e19
AU = 1.495978707e11
HBARC = HBAR * C / EV                           # eV m
M_PL = math.sqrt(HBAR * C / G) * C**2 / EV      # unreduced Planck mass, eV
K_NAT = 4 * math.pi / M_PL**2                   # K = 4 pi G (eV^-2)
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
M_REF, M_DWARF = 6e10, 1e8                      # Msun (QG1's point mass; reported dwarf)
E_KPC = HBARC / KPC
E_AU = HBARC / AU
G4PI = 4 * math.pi


def scales(a0):
    """record scales per footing from the record's tie at kappa = 1/2 (never pooled)."""
    E_a0 = HBAR * a0 / C / EV
    rho_de = 4 * a0**2 / (C**2 * G)                       # kg/m^3
    H = math.sqrt(8 * math.pi * G * rho_de / 3)           # 1/s
    E_H = HBAR * H / EV
    S_dS = math.pi * M_PL**2 / E_H**2
    vf = (M_REF * GM_SUN * a0) ** 0.25
    vf_dw = (M_DWARF * GM_SUN * a0) ** 0.25
    return dict(E_a0=E_a0, rho_de=rho_de, H=H, E_H=E_H, S_dS=S_dS, vf=vf, vf_dw=vf_dw)


SC = {f: scales(a) for f, a in FOOT.items()}
say("NPJ1: a non-perturbative origin for J (T3(i)).  MUTATE =", MUTATE)
say(f"M_Pl = {M_PL:.5e} eV, hbar c = {HBARC:.6e} eV m, hbar c/kpc = {E_KPC:.4e} eV, hbar c/AU = {E_AU:.4e} eV")
for f, s in SC.items():
    say(f"  [{f}] a0 = {FOOT[f]:.5e} m/s^2: E_a0 = {s['E_a0']:.5e} eV; rho_DE (tie) = {s['rho_de']:.5e} kg/m^3; "
        f"hbar H_Lambda = {s['E_H']:.5e} eV (H/a0 ratio {s['E_H']/s['E_a0']:.5f} = sqrt(32 pi/3) "
        f"{math.sqrt(32*math.pi/3):.5f}); S_dS = {s['S_dS']:.4e}; v_f(6e10) = {s['vf']/1e3:.2f} km/s")
OUT["constants"] = {"M_Pl_eV": M_PL, "E_kpc_eV": E_KPC, "footings": SC}

# ==================================================================== KNOWN ANSWERS
say("\n=== KNOWN ANSWERS ===")
KA = {}
mp.mp.dps = 30

# KA1: 3-d determinant, non-analytic part -m^3/(12 pi) per real boson.
#   (1/2) Int d^3k/(2pi)^3 ln(k^2+m^2) = (1/(4 pi^2)) Int k^2 ln(k^2+m^2) dk; subtract m=0 and the cutoff-linear m^2 k:
#   (1/(4 pi^2)) Int_0^inf [k^2 ln(1 + m^2/k^2) - m^2] dk  should equal  -m^3/(12 pi).
m_t = mp.mpf("1.3")
#   with k = m/t this is m^3 Int_0^inf [ln(1 + t^2) - t^2]/t^4 dt (log1p keeps both ends stable)
ka1_int = m_t**3 * mp.quad(lambda t: (mp.log1p(t**2) - t**2) / t**4 if t > 0 else mp.mpf(-0.5), [0, 1, 10, mp.inf])
ka1_val = ka1_int / (4 * mp.pi**2)
ka1_rel = float(abs(ka1_val / (-m_t**3 / (12 * mp.pi)) - 1))
KA["KA1"] = {"value": float(ka1_val), "target": float(-m_t**3 / (12 * mp.pi)), "rel": ka1_rel, "pass": ka1_rel < 1e-6}
say(f"KA1 3-d determinant non-analytic part at m = 1.3: {float(ka1_val):.10f} vs -m^3/(12 pi) = "
    f"{float(-m_t**3/(12*mp.pi)):.10f} (rel {ka1_rel:.1e}) -> {'PASS' if KA['KA1']['pass'] else 'FAIL'}")

# KA2: Bose-Einstein closed forms
p, z, n_, u, x = sp.symbols("p z n u x", positive=True)
kk = sp.symbols("k", integer=True, nonnegative=True)
Zbe = sp.summation(p**kk, (kk, 0, sp.oo)).args[0][0]            # geometric series, |p| < 1 branch
nbar = sp.simplify(p * sp.diff(sp.log(Zbe), p))
g1_series = sp.series(-sp.log(1 - z), z, 0, 9).removeO()
g1_ok = sp.simplify(g1_series - sum(z**j / j for j in range(1, 9))) == 0
crit = mp.quad(lambda k: 4 * mp.pi / (2 * mp.pi)**3 * (k**2 / mp.expm1(k**2 / 2) if k > 0 else mp.mpf(2)),
               [0, 1, 5, mp.inf])
crit_rel = float(abs(crit / (mp.zeta(1.5) * (1 / (2 * mp.pi))**1.5) - 1))
ka2_pass = (sp.simplify(Zbe - 1 / (1 - p)) == 0) and (sp.simplify(nbar - p / (1 - p)) == 0) and g1_ok and crit_rel < 1e-8
KA["KA2"] = {"Z": str(Zbe), "nbar": str(nbar), "g1_series_ok": bool(g1_ok), "crit_rel": crit_rel, "pass": bool(ka2_pass)}
say(f"KA2 Bose-Einstein: sum p^n = {Zbe}, nbar = {nbar}, g_1 series ok {g1_ok}; ideal-gas critical density "
    f"(m = T = 1) {float(crit):.12f} vs zeta(3/2)(1/2pi)^(3/2) (rel {crit_rel:.1e}) -> {'PASS' if ka2_pass else 'FAIL'}")

# KA3: Lee-Huang-Yang integral
#   the integrand rewritten exactly (no cancellation): q^2[...] = [1 + 2q/(sqrt(q^2+2)+q)] / (2 D),
#   D = q sqrt(q^2+2) + q^2 + 1; checked against the raw form at q = 0.3, 1, 3 below
lhy_f = lambda q: (1 + 2 * q / (mp.sqrt(q**2 + 2) + q)) / (2 * (q * mp.sqrt(q**2 + 2) + q**2 + 1))
lhy_raw = lambda q: q**2 * (mp.sqrt(q**4 + 2 * q**2) - q**2 - 1 + 1 / (2 * q**2))
lhy_form_err = max(abs(lhy_f(mp.mpf(qq)) - lhy_raw(mp.mpf(qq))) for qq in ("0.3", "1", "3"))
lhy = mp.quad(lhy_f, [0, 0.5, 2, 10, mp.inf])
lhy_rel = float(max(abs(lhy / (8 * mp.sqrt(2) / 15) - 1), lhy_form_err))
# implied LHY coefficient: (1/(4 pi^2)) (8 pi a n)^(3/2) (4 pi a n/m) I  vs  (2 pi a n^2/m)(128/(15 sqrt pi)) sqrt(n a^3)
lhy_coef = float((8 * mp.pi)**1.5 * 4 * mp.pi / (4 * mp.pi**2) * lhy / (2 * mp.pi))
KA["KA3"] = {"I": float(lhy), "target": float(8 * mp.sqrt(2) / 15), "rel": lhy_rel,
             "LHY_coefficient": lhy_coef, "target_coef": float(128 / (15 * mp.sqrt(mp.pi))), "pass": lhy_rel < 1e-8}
say(f"KA3 LHY: I = {float(lhy):.12f} vs 8 sqrt2/15 = {float(8*mp.sqrt(2)/15):.12f} (rel {lhy_rel:.1e}); implied "
    f"coefficient {lhy_coef:.8f} vs 128/(15 sqrt pi) = {float(128/(15*mp.sqrt(mp.pi))):.8f} -> "
    f"{'PASS' if KA['KA3']['pass'] else 'FAIL'}")

# KA4: Legendre of W gives J; GR + (a0^2/K) J gives the law
Kk, a0s, Aa = sp.symbols("K a0 A", positive=True)
Wp = -p - sp.log(1 - p)
Jfun = u - sp.log(1 + u)
pstar = sp.solve(sp.diff(p * u - Wp, p), p)[0]
Jleg = sp.simplify((p * u - Wp).subs(p, pstar))
L_law = -Aa**2 / (2 * Kk) + (a0s**2 / Kk) * Jfun.subs(u, Aa / a0s)
mu_law_sym = sp.simplify(-(Kk / Aa) * sp.diff(L_law, Aa))
ka4_pass = sp.simplify(Jleg - Jfun) == 0 and sp.simplify(mu_law_sym - (Aa / a0s) / (1 + Aa / a0s)) == 0
KA["KA4"] = {"p_star": str(pstar), "J_from_W": str(Jleg), "mu": str(mu_law_sym), "pass": bool(ka4_pass)}
say(f"KA4 Legendre: p* = {pstar}, max_p[pu - W] = {Jleg}; mu from GR + (a0^2/K)J = {mu_law_sym} -> "
    f"{'PASS' if ka4_pass else 'FAIL'}")

# KA5a: large-N O(N) gap equation from V/N = -sigma^(3/2)/(12 pi) - (sigma - r)^2/(2 lambda)
sig, rr, lam = sp.symbols("sigma r lambda", positive=True)
V_on = -sig**sp.Rational(3, 2) / (12 * sp.pi) - (sig - rr)**2 / (2 * lam)
gap_on = sp.simplify(sp.diff(V_on, sig))           # = 0 at the saddle
mm = sp.symbols("m", positive=True)
gap_m = sp.simplify(gap_on.subs(sig, mm**2) * (-lam))   # m^2 + lambda m/(8 pi) - r = 0
gap_target = mm**2 + lam * mm / (8 * sp.pi) - rr
gap_ok = sp.simplify(gap_m - gap_target) == 0
# envelope: dV/dr at the saddle = (sigma - r)/lambda = -m/(8 pi)
env = sp.simplify((sp.diff(V_on, rr)).subs(sig, mm**2).subs(rr, mm**2 + lam * mm / (8 * sp.pi)))
env_ok = sp.simplify(env + mm / (8 * sp.pi)) == 0


def m_on(rv, lv):                 # root of m^2 + b m - r = 0 in the cancellation-free form 2r/(b + sqrt(b^2 + 4r))
    b = lv / (8 * math.pi)
    return 2 * rv / (b + math.sqrt(b * b + 4 * rv))


def dlnm_dlnr(lv, rv=1.0, h=1e-6):
    return (math.log(m_on(rv * math.exp(h), lv)) - math.log(m_on(rv * math.exp(-h), lv))) / (2 * h)


ex_lo, ex_hi = dlnm_dlnr(1e-7), dlnm_dlnr(1e7)
ka5a_pass = gap_ok and env_ok and abs(ex_lo - 0.5) < 1e-3 and abs(ex_hi - 1.0) < 1e-3

# KA5b: GN closed form (piecewise) vs numerical minimization; Cl(7) matrices
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]], complex)
s3 = np.array([[1, 0], [0, -1]], complex); I2 = np.eye(2)


def kron(*ms):
    out = ms[0]
    for mtx in ms[1:]:
        out = np.kron(out, mtx)
    return out


GAM = [kron(s1, I2, I2), kron(s2, I2, I2), kron(s3, s1, I2), kron(s3, s2, I2), kron(s3, s3, s1), kron(s3, s3, s2)]
GAM.append(kron(s3, s3, s3))                     # seventh: anticommutes with the six (Cl(7) in 8 dims)
anti = max(np.abs(GAM[i] @ GAM[j] + GAM[j] @ GAM[i] - 2 * (i == j) * np.eye(8)).max() for i in range(7) for j in range(7))
rng = np.random.default_rng(11)
detrel = []
for _ in range(5):
    kv, Av, sv, gv = rng.normal(size=3), rng.normal(size=3), rng.normal(), abs(rng.normal()) + 0.3
    D = 1j * (sum(kv[i] * GAM[i] for i in range(3)) + gv * sum(Av[i] * GAM[3 + i] for i in range(3)) + sv * GAM[6])
    detrel.append(abs(np.linalg.det(D) / (kv @ kv + gv**2 * Av @ Av + sv**2) ** 4 - 1))


def V_gn(sv, gA, M):          # leading-N GN potential per flavor (8 components), delta = -2M/pi
    return -(M / math.pi) * sv**2 + (2 / (3 * math.pi)) * (sv**2 + gA**2) ** 1.5


def V_gn_min_closed(gA, M):
    return -M**3 / (3 * math.pi) + (M / math.pi) * gA**2 if gA < M else (2 / (3 * math.pi)) * gA**3


gn_err = 0.0
for gA in (0.0, 0.2, 0.7, 0.99, 1.3, 3.0):
    res = minimize_scalar(lambda sv: V_gn(sv, gA, 1.0), bounds=(0, 3), method="bounded",
                          options={"xatol": 1e-12})
    gn_err = max(gn_err, abs(res.fun - V_gn_min_closed(gA, 1.0)))
ka5b_pass = anti < 1e-12 and max(detrel) < 1e-10 and gn_err < 1e-9
KA["KA5"] = {"gap_eq": str(gap_m), "gap_ok": bool(gap_ok), "envelope_dV_dr": str(env), "env_ok": bool(env_ok),
             "exponent_lambda_small": ex_lo, "exponent_lambda_large": ex_hi, "Cl7_anticomm": float(anti),
             "Cl7_det_rel": float(max(detrel)), "GN_min_err": gn_err, "pass": bool(ka5a_pass and ka5b_pass)}
say(f"KA5a O(N) large N: gap eq {gap_m} = 0 ({gap_ok}); dV/dr at saddle = {env} ({env_ok}); d ln m/d ln r = "
    f"{ex_lo:.6f} (lambda -> 0, free 1/2) and {ex_hi:.6f} (lambda -> inf, large-N nu = 1)")
say(f"KA5b GN: Cl(7) anticommutator error {anti:.1e}, det D/(k^2+g^2A^2+sigma^2)^4 - 1 max {max(detrel):.1e}; "
    f"closed-form V_min vs numerical minimum, max error {gn_err:.1e} -> {'PASS' if KA['KA5']['pass'] else 'FAIL'}")

# KA6: BK point mass, from the static Lagrangian by Euler-Lagrange (sympy)
r_, Lb, al, MP, Mb = sp.symbols("r Lambda alpha M_Pl M", positive=True)
th = sp.Function("theta")
rho = sp.Function("rho")
Lag = 4 * sp.pi * r_**2 * (-(2 * Lb / 3) * sp.diff(th(r_), r_)**3 - al * Lb * th(r_) * rho(r_) / MP)
EL = sp.euler_equations(Lag, th(r_), r_)[0]
# claim: r^2 theta'^2 = alpha M(r)/(8 pi M_Pl), i.e. d/dr(r^2 theta'^2) = alpha rho r^2/(2 M_Pl); check EL equivalence
lhs_EL = sp.simplify(EL.lhs - EL.rhs)
d_r2tp2 = sp.diff(r_**2 * sp.diff(th(r_), r_)**2, r_)
el_equiv2 = sp.simplify(lhs_EL / (8 * sp.pi * Lb) - (d_r2tp2 - al * rho(r_) * r_**2 / (2 * MP)))
theta_p = sp.sqrt(al * Mb / (8 * sp.pi * MP)) / r_
a_theta = al * Lb * theta_p / MP
a_N = Mb / (MP**2 * r_**2)
a0_bk = sp.simplify(a_theta**2 / a_N)
ka6_pass = sp.simplify(el_equiv2) == 0 and sp.simplify(a0_bk - al**3 * Lb**2 / (8 * sp.pi * MP)) == 0
KA["KA6"] = {"EL": str(sp.simplify(lhs_EL)), "a0_BK": str(a0_bk), "pass": bool(ka6_pass)}
say(f"KA6 BK: Euler-Lagrange = 8 pi Lambda [d/dr(r^2 theta'^2) - alpha rho r^2/(2 M_Pl)] (residual "
    f"{sp.simplify(el_equiv2)}); a_theta^2/a_N = {a0_bk} -> a = a_N + sqrt(a0' a_N) -> {'PASS' if ka6_pass else 'FAIL'}")

# KA7: the 3-d bubble Int d^3k/(2pi)^3 1/(k^2 (k+p)^2) = 1/(8|p|) (Feynman parameters done numerically)
pv = mp.mpf("0.7")
bub = mp.quad(lambda xx: 1 / (8 * mp.sqrt(xx * (1 - xx)) * pv), [0, 0.5, 1]) / mp.pi
# direct radial-angular quadrature: Int k^2 dk dcos /(4 pi^2) 1/(k^2 (k^2 + p^2 + 2 k p c))
bub2 = mp.quad(lambda k: mp.quad(lambda cth: 1 / (k**2 + pv**2 + 2 * k * pv * cth), [-1, 1]), [0, pv, 10, mp.inf]) \
    / (4 * mp.pi**2)
ka7_rel = float(max(abs(bub * 1 / (1 / (8 * pv)) - 1), abs(bub2 / (1 / (8 * pv)) - 1)))
KA["KA7"] = {"bubble": float(bub2), "target": float(1 / (8 * pv)), "rel": ka7_rel, "pass": ka7_rel < 1e-6}
say(f"KA7 3-d bubble at p = 0.7: {float(bub2):.10f} vs 1/(8p) = {float(1/(8*pv)):.10f} (rel {ka7_rel:.1e}) -> "
    f"{'PASS' if KA['KA7']['pass'] else 'FAIL'}")

KA_ALL = all(v["pass"] for v in KA.values())
OUT["known_answers"] = KA
say(f"KNOWN ANSWERS ALL PASS: {KA_ALL}")

# ==================================================================== detector (U) and identities
say("\n=== U DETECTOR (HZ1's J1/J2, re-implemented) AND THE BOSE-EINSTEIN IDENTITIES ===")


def uv_admissible(expr, var, order=13):
    ser = sp.series(expr, var, 0, order).removeO()
    co = {k: sp.nsimplify(ser.coeff(var, k)) for k in range(0, order)}
    odd = [k for k, v in co.items() if k % 2 == 1 and v != 0]
    high = [k for k, v in co.items() if k >= 7 and v != 0]
    term = sp.simplify(sp.expand(expr) - sp.expand(ser)) == 0
    return {"odd_orders": odd[:5], "orders_ge_7": high[:4], "terminates": bool(term),
            "admissible": (not odd) and (not high) and bool(term)}


DET = {"W(p)": uv_admissible(Wp, p), "J(u)": uv_admissible(Jfun, u)}
kbody = [sp.nsimplify(sp.series(Wp, p, 0, 9).removeO().coeff(p, k)) for k in range(2, 9)]
say(f"detector on W(p) = -p - ln(1-p): {DET['W(p)']}; k-body coefficients of eps(n) (k = 2..8): {kbody}")
say(f"detector on J(u): {DET['J(u)']}")
OUT["detector"] = DET
OUT["kbody"] = [str(v) for v in kbody]

# the three identities (c1) and the lead's observation 1
lnZ = -sp.log(1 - p)
id1 = sp.simplify(Wp - (lnZ - p)) == 0 and sp.simplify(sp.diff(Wp, p) - p / (1 - p)) == 0
nFD = 1 / (1 / x + 1)                               # Fermi-Dirac / Langmuir occupation at fugacity x
id2 = sp.simplify(nFD - x / (1 + x)) == 0
inv_ok = sp.simplify((x / (1 + x)).subs(x, p / (1 - p)) - p) == 0
lz = sp.symbols("l", real=True)                     # l = ln z
lnZl = -sp.log(1 - sp.exp(lz))
Nl = sp.diff(lnZl, lz)
lstar = sp.solve(sp.Eq(Nl, n_), lz)[0]
legS = sp.simplify((n_ * lz - lnZl).subs(lz, lstar))
S_be = (1 + n_) * sp.log(1 + n_) - n_ * sp.log(n_)
id3 = sp.simplify(sp.expand_log(legS + S_be, force=True)) == 0
say(f"identity (i) W = ln Z_BE(p) - p and W'(p) = nbar_BE(p) = p/(1-p): {id1}; inverse map x = p/(1-p) -> "
    f"x/(1+x) = p: {inv_ok}")
say(f"identity (ii) x/(1+x) = Fermi-Dirac / Langmuir occupation at fugacity x: {id2}  (same map, other statistics)")
say(f"identity (iii) Legendre of ln Z_BE in ln z: n ln z - ln Z = {legS}  = -S_BE(n): {id3}  (not W)")
OUT["identities"] = {"W_is_lnZBE_minus_p": bool(id1), "inverse_map": bool(inv_ok), "FD_reading": bool(id2),
                     "legendre_in_lnz_is_minus_S": bool(id3), "legendre_value": str(legS)}

# ==================================================================== shape machinery
XG = np.logspace(-2, 2, 41)
MU_LAW = XG / (1 + XG)
SLOPE_LAW = 1 / (1 + 0.01)


def shape_stats(mufun, prm):
    with np.errstate(all="ignore"):
        mu = np.asarray(mufun(XG, prm), float)
        if not np.all(np.isfinite(mu)):
            return 1e3, float("nan"), 1e6
        band = float(np.max(np.abs(mu - MU_LAW)))
        h = 1e-4
        m1 = float(mufun(np.array([0.01 * math.exp(h)]), prm)[0])
        m2 = float(mufun(np.array([0.01 * math.exp(-h)]), prm)[0])
    slope = (math.log(m1) - math.log(m2)) / (2 * h) if (m1 > 0 and m2 > 0) else float("nan")
    q = max(band / 0.1, abs(slope - SLOPE_LAW) / 0.1) if np.isfinite(slope) else 1e3 + band
    return band, slope, q


def fit(mufun, bounds, seed=0):
    if not bounds:
        band, slope, q = shape_stats(mufun, [])
        prm = []
    else:
        res = differential_evolution(lambda q_: shape_stats(mufun, q_)[2], bounds, seed=seed, tol=1e-10,
                                     maxiter=500, popsize=30, polish=True)
        prm = list(map(float, res.x))
        band, slope, q = shape_stats(mufun, prm)
    ok = bool(band <= 0.1 and np.isfinite(slope) and abs(slope - SLOPE_LAW) <= 0.1)
    return {"params": prm, "max_dmu": band, "deep_slope": slope, "Q": q, "S": "PASS" if ok else "FAIL"}


# ==================================================================== candidates: mu(x; params), derived in sympy
say("\n=== CANDIDATES: mu(x) DERIVED FROM EACH SECTOR'S FREE ENERGY (sympy), THEN FITTED ===")
Asy, Bsy, csy, al_t, Ksy, nu_, Nn, gB, gF, m0, Msy, Hsy = sp.symbols(
    "A B c alpha_t K nu N g_B g_F m0 M H", positive=True)


def mu_from_L(Lsec, var=Asy):
    """mu = -(K/A) dL/dA for L = -A^2/(2K) + (1/4K) alpha_t A^2 + Lsec."""
    Ltot = -var**2 / (2 * Ksy) + al_t * var**2 / (4 * Ksy) + Lsec
    return sp.simplify(sp.expand(-(Ksy / var) * sp.diff(Ltot, var)))


DERIV = {}

# a1 BK: two-field force law (KA6): a = a_N + sqrt(a0' a_N); x = a/a0, s^2 = a_N/a0, a0' = c a0
def mu_a1(xv, q):
    cc = 10 ** q[0]
    s = (-math.sqrt(cc) + np.sqrt(cc + 4 * xv)) / 2
    return s**2 / xv


# a2 exact-Legendre condensate: L_sec = B (a0^2/K) [u - ln(1+u)], u = A/a0
L_a2 = Bsy * (a0s**2 / Ksy) * (Asy / a0s - sp.log(1 + Asy / a0s))
mu_a2_sym = mu_from_L(L_a2)
DERIV["a2"] = str(mu_a2_sym)
f_a2 = sp.lambdify((x, al_t, Bsy), mu_a2_sym.subs(Asy, x * a0s).subs(a0s, 1), "numpy")
mu_a2 = lambda xv, q: f_a2(xv, q[0], q[1])

# a3 GP + LHY: L_sec = B (a0^2/K) [u^2/2 - beta u^(5/2)]
bet = sp.symbols("beta", positive=True)
L_a3 = Bsy * (a0s**2 / Ksy) * ((Asy / a0s)**2 / 2 - bet * (Asy / a0s)**sp.Rational(5, 2))
mu_a3_sym = mu_from_L(L_a3)
DERIV["a3"] = str(mu_a3_sym)
f_a3 = sp.lambdify((x, al_t, Bsy, bet), mu_a3_sym.subs(Asy, x * a0s).subs(a0s, 1), "numpy")
mu_a3 = lambda xv, q: f_a3(xv, q[0], q[1], 10 ** q[2])

# b1 large-N GN(Y): L_sec = -nu N V_min(A); V_min piecewise (KA5b). In units: B' = 2 K nu N M g^2/pi, s = g A/M = c x
gA_ = sp.symbols("gA", positive=True)
L_b1_lo = -nu_ * Nn * (-Msy**3 / (3 * sp.pi) + (Msy / sp.pi) * (gB * Asy)**2)
L_b1_hi = -nu_ * Nn * (2 / (3 * sp.pi)) * (gB * Asy)**3
mu_b1_lo, mu_b1_hi = mu_from_L(L_b1_lo), mu_from_L(L_b1_hi)
DERIV["b1"] = {"gA<M": str(mu_b1_lo), "gA>M": str(mu_b1_hi)}
# both reduce to 1 - alpha_t/2 + B' max(1, g A/M) with B' = 2 K nu N M g^2/pi:
Bp_ = 2 * Ksy * nu_ * Nn * Msy * gB**2 / sp.pi
b1_ok = (sp.simplify(mu_b1_lo - (1 - al_t / 2 + Bp_)) == 0 and
         sp.simplify(mu_b1_hi - (1 - al_t / 2 + Bp_ * gB * Asy / Msy)) == 0)


def mu_b1(xv, q):
    return 1 - q[0] / 2 + q[1] * np.maximum(1.0, 10 ** q[2] * xv)


# b2 interacting leaf pair: N O(N) bosons (large-N gap eq) + N Cl(6) fermions, g_B = 2 g_F.
#   dL_B/dA = -nu N dV/dr * 2 g_B^2 A = nu N g_B^2 A m(A)/(4 pi)  (envelope, KA5a)
#   L_F = -8 nu N g_F^3 A^3/(12 pi)
mA = sp.Function("m")(Asy)
dLB = nu_ * Nn * gB**2 * Asy * mA / (4 * sp.pi)
LF = -8 * nu_ * Nn * (gB / 2)**3 * Asy**3 / (12 * sp.pi)
mu_b2_sym = sp.simplify(1 - al_t / 2 - (Ksy / Asy) * (dLB + sp.diff(LF, Asy)))
DERIV["b2"] = str(mu_b2_sym)
# in units of the A = 0 boson mass m_b0: B = K nu N g_B^2 m_b0/(4 pi), s = g_B A/m_b0 = c x, lhat = lambda/(8 pi m_b0):
#   mhat^2 + lhat mhat = 1 + lhat + s^2 ; mu = 1 - alpha_t/2 - B (mhat - s)
mb0 = sp.symbols("m_b0", positive=True)
b2_ok = sp.simplify(mu_b2_sym.subs(mA, mb0 * sp.Symbol("mhat")).subs(Asy, sp.Symbol("s") * mb0 / gB)
                    - (1 - al_t / 2 - (Ksy * nu_ * Nn * gB**2 * mb0 / (4 * sp.pi)) * (sp.Symbol("mhat")
                                                                                         - sp.Symbol("s")))) == 0


def mhat_b2(s, lh):               # root of mhat^2 + lh mhat - (1 + lh + s^2) = 0, cancellation-free
    rr_ = 1 + lh + s * s
    return 2 * rr_ / (lh + np.sqrt(lh * lh + 4 * rr_))


def mu_b2(xv, q):
    s = 10 ** q[2] * xv
    return 1 - q[0] / 2 - q[1] * (mhat_b2(s, 10 ** q[3]) - s)


# c1 Bose mode, thermodynamic pairing: L_sec = n_s T_s g_1(exp((lambda_A A - eps)/T_s)), y = lambda_A A/T_s = c x
ns, Ts, lA, eps_ = sp.symbols("n_s T_s lambda_A epsilon", positive=True)
L_c1 = ns * Ts * (-sp.log(1 - sp.exp((lA * Asy - eps_) / Ts)))
mu_c1_sym = mu_from_L(L_c1)
DERIV["c1"] = str(mu_c1_sym)


def mu_c1(xv, q):
    cc = 10 ** q[2]
    e = cc * 100 * (1 + 10 ** q[3])            # level above the largest graded y (no condensation in range)
    y = cc * xv
    nb = 1 / np.expm1(e - y)
    return 1 - q[0] / 2 - 10 ** q[1] * nb / y


c1_ok = sp.simplify(mu_c1_sym - (1 - al_t / 2 - (Ksy * ns * lA**2 / Ts) / (lA * Asy / Ts)
                                 / (sp.exp((eps_ - lA * Asy) / Ts) - 1))) == 0

# c2 bath at T(A) = sqrt(A^2 + H^2)/(2 pi): P = N pi^2 T^4/90
T_A = sp.sqrt(Asy**2 + Hsy**2) / (2 * sp.pi)
L_c2 = Nn * sp.pi**2 * T_A**4 / 90
mu_c2_sym = mu_from_L(L_c2)
DERIV["c2"] = str(mu_c2_sym)
RH = math.sqrt(32 * math.pi / 3)                 # H_Lambda/a0 in energy units (footing independent at kappa 1/2)
f_c2 = sp.lambdify((x, al_t, Bsy), (1 - al_t / 2 - Bsy * (1 + (x / RH)**2)), "numpy")
c2_ok = sp.simplify(mu_c2_sym - (1 - al_t / 2 - (Ksy * Nn * Hsy**2 / (360 * sp.pi**2)) * (1 + Asy**2 / Hsy**2))) == 0
mu_c2 = lambda xv, q: f_c2(xv, q[0], q[1])

# c3 holographic leaf pair = G3's fields: L = (nu N/(12 pi)) [(m0^2 + g_B^2 A^2)^(3/2) - 8 g_F^3 A^3], g_B = 2 g_F
L_c3 = nu_ * Nn / (12 * sp.pi) * ((m0**2 + gB**2 * Asy**2)**sp.Rational(3, 2) - 8 * (gB / 2)**3 * Asy**3)
mu_c3_sym = mu_from_L(L_c3)
DERIV["c3"] = str(mu_c3_sym)
c3_ok = sp.simplify(mu_c3_sym - (1 - al_t / 2 - (Ksy * nu_ * Nn * gB**2 * m0 / (4 * sp.pi))
                                 * (sp.sqrt(1 + (gB * Asy / m0)**2) - gB * Asy / m0))) == 0


def mu_c3(xv, q):
    s = 10 ** q[2] * xv
    return 1 - q[0] / 2 - q[1] * (np.sqrt(1 + s * s) - s)


# c4 horizon dof: r_h = 1/sqrt(A^2+H^2), S = pi M_Pl^2 r_h^2, T = 1/(2 pi r_h), dE = T dS, f = (E - TS)/V
rh = sp.symbols("r_h", positive=True)
Mpl_s = sp.symbols("M_Pl", positive=True)
S_h = sp.pi * Mpl_s**2 * rh**2
T_h = 1 / (2 * sp.pi * rh)
E_h = sp.integrate(T_h * sp.diff(S_h, rh), (rh, 0, rh))
F_h = sp.simplify(E_h - T_h * S_h)
f_h = sp.simplify(F_h / (4 * sp.pi * rh**3 / 3))
f_hA = sp.simplify(f_h.subs(rh, 1 / sp.sqrt(Asy**2 + Hsy**2)))
L_c4 = -f_hA
mu_c4_sym = sp.simplify(mu_from_L(L_c4).subs(Ksy, 4 * sp.pi / Mpl_s**2))
DERIV["c4"] = {"E": str(E_h), "F": str(F_h), "f(A)": str(f_hA), "mu": str(mu_c4_sym)}
c4_const = sp.simplify(mu_c4_sym - (1 - al_t / 2))
mu_c4 = lambda xv, q: (1 - q[0] / 2 + float(c4_const)) * np.ones_like(xv)

say(f"a2: mu = {mu_a2_sym}")
say(f"a3: mu = {mu_a3_sym}")
say(f"b1: mu (gA < M) = {mu_b1_lo};  mu (gA > M) = {mu_b1_hi};  = 1 - alpha_t/2 + B' max(1, gA/M): {b1_ok}")
say(f"b2: mu = {mu_b2_sym};  reduced form 1 - alpha_t/2 - B (mhat - s): {b2_ok}")
say(f"c1: mu = {mu_c1_sym};  = 1 - alpha_t/2 - B nbar(y)/y: {c1_ok}")
say(f"c2: mu = {mu_c2_sym};  = 1 - alpha_t/2 - B(1 + A^2/H^2), B = K N H^2/(360 pi^2): {c2_ok}")
say(f"c3: mu = {mu_c3_sym};  = 1 - alpha_t/2 - B(sqrt(1+s^2) - s): {c3_ok}")
say(f"c4: E = {E_h}, F = {F_h}, f(A) = {f_hA}; mu = {mu_c4_sym} (A-independent: shift {c4_const})")
OUT["derived_mu"] = DERIV
OUT["reductions_ok"] = {"b1": bool(b1_ok), "b2": bool(b2_ok), "c1": bool(c1_ok), "c2": bool(c2_ok),
                        "c3": bool(c3_ok)}
RED_OK = all(OUT["reductions_ok"].values())

CANDS = {
    "a1 BK superfluid": dict(mu=mu_a1, bounds=[(-3, 3)], cls="a"),
    "a2 exact-Legendre condensate": dict(mu=mu_a2, bounds=[(-10, 10), (0, 10)], cls="a"),
    "a3 GP + LHY condensate": dict(mu=mu_a3, bounds=[(-10, 10), (0, 10), (-4, 2)], cls="a"),
    "b1 large-N GNY, dynamical mass": dict(mu=mu_b1, bounds=[(-10, 10), (0, 100), (-3, 3)], cls="b"),
    "b2 interacting leaf pair (large-N O(N) + Cl(6))": dict(mu=mu_b2, bounds=[(-10, 10), (0, 10), (-3, 3), (-4, 3)],
                                                            cls="b"),
    "c1 Bose mode, thermodynamic pairing": dict(mu=mu_c1, bounds=[(-10, 10), (-6, 3), (-4, 2), (-4, 3)], cls="c"),
    "c2 bath at dS-Unruh T(A)": dict(mu=mu_c2, bounds=[(-10, 10), (0, 100)], cls="c"),
    "c3 holographic leaf pair (G3 fields)": dict(mu=mu_c3, bounds=[(-10, 10), (0, 10), (-3, 3)], cls="c"),
    "c4 horizon dof": dict(mu=mu_c4, bounds=[(-10, 10)], cls="c"),
}
if MUTATE:
    CANDS["M1 twin: mu = x^2/(1+x^2)"] = dict(mu=lambda xv, q: xv**2 / (1 + xv**2), bounds=[], cls="M")
    CANDS["M1 control: the law"] = dict(mu=lambda xv, q: xv / (1 + xv), bounds=[], cls="M")

# mu(x; params) is a dimensionless function of x for every candidate (c2's H/a0 = sqrt(32 pi/3) on both footings),
# so the fit is the same on both footings; it is run on each footing anyway (same seeds) and compared.
FITS = {f: {} for f in FOOT}
for f in FOOT:
    for name, cdef in CANDS.items():
        FITS[f][name] = fit(cdef["mu"], cdef["bounds"], seed=0)
for name in CANDS:
    r = FITS["canonical"][name]
    same = FITS["alt"][name]["max_dmu"] == r["max_dmu"]
    say(f"  {name:48s} S {r['S']}: max dmu {r['max_dmu']:.4f}, deep slope {r['deep_slope']:.4f} (law 0.9901), "
        f"params {[round(v, 4) for v in r['params']]}  [alt identical: {same}]")
OUT["fits"] = FITS

# ==================================================================== C (size) per footing
say("\n=== C: SIZE (C-amp, C-loc) UNDER RULE H AND RULE W (W = holographic count + species; ASSUMPTION) ===")


def r_of_x(xv, a0, Mb):
    return math.sqrt(Mb * GM_SUN * (1 + xv) / (xv**2 * a0))


def cloc_needed(sc, a0, vf):
    return (C**2 / vf**2) / math.sqrt(1.01)


def leaf_pair_C(sc, a0, B, cc, a0_energy=None):
    """amplitude for leaf pairs (b2, c3): nu N g_B^3 = B c M_Pl^2/E_a0 (from B = K nu N g_B^2 m_b0/(4pi), m_b0 = g_B a0/c)."""
    Ea = sc["E_a0"] if a0_energy is None else a0_energy
    X = B * cc * M_PL**2 / Ea
    nuN = X / G4PI**3                                   # couplings at their bound g_B = 4 pi
    lr_H = math.log10(nuN / (1000 * M_PL))
    lr_count = math.log10(nuN / (math.pi * M_PL**2 / sc["E_H"]))
    lr_sp = math.log10(nuN / (M_PL**2 / E_KPC))
    return dict(X_eV=X, nuN_min_eV=nuN, log10R_H=lr_H, log10R_W_count=lr_count, log10R_W_species=lr_sp,
                log10R_W=max(lr_count, lr_sp), Lambda_sp_eV=M_PL**2 / nuN, N_dof=nuN / sc["E_H"])


CRES = {f: {} for f in FOOT}
for f, a0 in FOOT.items():
    sc = SC[f]
    vf = sc["vf"]
    cg_need = cloc_needed(sc, a0, vf)
    lr_loc_A = math.log10(cg_need / G4PI)                # for sectors whose gap is set by A
    m_cond = HBARC / r_of_x(0.01, a0, M_REF)             # condensate: microscopic mass with hbar/(mc) <= r(0.01)
    lr_loc_cond = math.log10(m_cond / M_PL)
    say(f"[{f}] C-loc for A-gapped sectors: c_g >= c^2/v_f^2/sqrt(1.01) = {cg_need:.4e} vs 4 pi -> log10 R_loc = "
        f"{lr_loc_A:.2f}; condensate microscopic mass >= {m_cond:.2e} eV vs M_Pl -> log10 {lr_loc_cond:.1f}")
    for name in CANDS:
        if name.startswith("M1"):
            continue
        fr = FITS[f][name]
        q = fr["params"]
        row = {}
        if name.startswith("a1"):
            a0p = 10 ** q[0] * sc["E_a0"]
            Lam_min = math.sqrt(8 * math.pi * M_PL * a0p / G4PI**3)   # alpha at 4 pi
            Lam_1 = math.sqrt(8 * math.pi * M_PL * a0p)                # alpha = 1
            lr = math.log10(Lam_min / M_PL)
            row = dict(a0prime_over_a0=10 ** q[0], Lambda_min_eV=Lam_min, Lambda_alpha1_eV=Lam_1,
                       rho_DE_quarter_eV=(sc["rho_de"] * C**2 * (HBARC)**3 / EV) ** 0.25,
                       log10R_amp_H=lr, log10R_amp_W=lr, log10R_loc=lr_loc_cond)
        elif name.startswith("a2"):
            eps0 = sc["E_a0"]**2 * M_PL**2 / (4 * math.pi)            # eV^4 (a0^2/K)
            nmax = sc["E_a0"] * M_PL**2 / (4 * math.pi)               # eV^3 (a0/K)
            lr = max(math.log10(eps0**0.25 / M_PL), math.log10(nmax**(1 / 3) / M_PL))
            row = dict(eps0_quarter_eV=eps0**0.25, nmax_third_eV=nmax**(1 / 3), log10R_amp_H=lr, log10R_amp_W=lr,
                       log10R_loc=lr_loc_cond, note="inputs are (A)'s own constants: a restatement, not an origin")
        elif name.startswith("a3"):
            row = dict(log10R_amp_H=float("nan"), log10R_amp_W=float("nan"), log10R_loc=lr_loc_cond,
                       note="S fails; C not needed for the label")
        elif name.startswith("b1"):
            X = q[1] * 10 ** q[2] * M_PL**2 / (8 * sc["E_a0"])         # nu N g^3 = B' c M_Pl^2/(8 E_a0)
            nuN = X / G4PI**3
            row = dict(X_eV=X, log10R_amp_H=math.log10(nuN / (1000 * M_PL)),
                       log10R_amp_W=max(math.log10(nuN / (math.pi * M_PL**2 / sc["E_H"])),
                                        math.log10(nuN / (M_PL**2 / E_KPC))), log10R_loc=lr_loc_A)
        elif name.startswith("b2") or name.startswith("c3"):
            lp = leaf_pair_C(sc, a0, q[1], 10 ** q[2])
            row = dict(lp, log10R_amp_H=lp["log10R_H"], log10R_amp_W=lp["log10R_W"], log10R_loc=lr_loc_A)
        elif name.startswith("c1"):
            row = dict(log10R_amp_H=float("nan"), log10R_amp_W=float("nan"), log10R_loc=float("nan"),
                       note="S fails; C not needed for the label")
        elif name.startswith("c2"):
            Nneed = 90 * math.pi * max(q[1], 1e-300) * (M_PL / sc["E_H"])**2   # from B = K N H^2/(360 pi^2)
            row = dict(N_needed=Nneed, log10R_amp_H=math.log10(Nneed / 1000),
                       log10R_amp_W=max(math.log10(Nneed / sc["S_dS"]),
                                        math.log10(E_KPC / (M_PL / math.sqrt(Nneed)))),
                       log10R_loc=math.log10(cg_need / (1 / (2 * math.pi))))
        elif name.startswith("c4"):
            row = dict(log10R_amp_H=0.0, log10R_amp_W=0.0, log10R_loc=math.log10(cg_need / 1.0),
                       note="no free input; the horizon's gap is sqrt(A^2+H^2) (c_g = 1)")
        for rule in ("H", "W"):
            amp = row.get(f"log10R_amp_{rule}", float("nan"))
            loc = row.get("log10R_loc", float("nan"))
            row[f"C_{rule}"] = "PASS" if (np.isfinite(amp) and np.isfinite(loc) and amp <= 0 and loc <= 0) else "FAIL"
        if name.startswith("b2") or name.startswith("c3"):
            row["C_W0_count_only_amp"] = "PASS" if row["log10R_W_count"] <= 0 else "FAIL"
        CRES[f][name] = row
        fmt = lambda v: f"{v:.2f}" if isinstance(v, float) and np.isfinite(v) else "n/a"
        say(f"  [{f}] {name:48s} C-amp log10 R: H {fmt(row['log10R_amp_H'])}, W {fmt(row['log10R_amp_W'])}; "
            f"C-loc {fmt(row['log10R_loc'])} -> C_H {row['C_H']}, C_W {row['C_W']}")
        if name.startswith("c3") or name.startswith("b2"):
            say(f"      nu N g_B^3 needed {row['X_eV']:.3e} eV; at g_B = 4 pi: nu N = {row['nuN_min_eV']:.3e} eV "
                f"(H ceiling {1000*M_PL:.2e}; W-count bound pi M_Pl^2/H = {math.pi*M_PL**2/sc['E_H']:.2e}; "
                f"W-species bound M_Pl^2 kpc = {M_PL**2/E_KPC:.2e}); N_dof = {row['N_dof']:.2e} vs S_dS "
                f"{sc['S_dS']:.2e}; Lambda_sp = {row['Lambda_sp_eV']:.2e} eV vs hbar c/kpc {E_KPC:.2e}; "
                f"W-count alone (W0): {row['C_W0_count_only_amp']} (amplitude only)")
        if name.startswith("a1"):
            say(f"      a0'/a0 {row['a0prime_over_a0']:.4f}; Lambda needed {row['Lambda_min_eV']:.3e} eV (alpha 4 pi), "
                f"{row['Lambda_alpha1_eV']:.3e} eV (alpha 1); rho_DE^(1/4) = {row['rho_DE_quarter_eV']:.3e} eV")
OUT["C"] = CRES
OUT["C_loc_A_gapped"] = {f: {"c_g_needed": cloc_needed(SC[f], FOOT[f], SC[f]["vf"]),
                             "log10R_loc": math.log10(cloc_needed(SC[f], FOOT[f], SC[f]["vf"]) / G4PI),
                             "dwarf_c_g_needed": (C**2 / SC[f]["vf_dw"]**2) / math.sqrt(1.01)} for f in FOOT}

# ==================================================================== U
say("\n=== U: UV ACTION (power counting + detector on anything inserted) ===")
x3 = sp.symbols("x3", positive=True)
U = {
    "a1 BK superfluid": dict(U="FAIL", why=f"three-body contact |psi|^6, z = 2, d = 3: coupling dimension 5 - 6*3/2 = "
                             f"{5 - 9}; and the inserted |grad theta|^3: {uv_admissible(x3**3, x3)}"),
    "a2 exact-Legendre condensate": dict(U="FAIL", why=f"EOS W inserted: {DET['W(p)']}; k-body tower g_k = 1/k for all k"),
    "a3 GP + LHY condensate": dict(U="FAIL", why=f"UV |phi|^4 (z = 1) renormalizable and LHY generated, but the coupling "
                                   f"mu = mu0 |A|/a0 inserted: {uv_admissible(x3, x3)}"),
    "b1 large-N GNY, dynamical mass": dict(U="PASS", why="leaf z = 3, [3-d Lagrangian] = 3: [psi] = 1, [sigma] = 1/2, "
                                           "Yukawa [y] = 1/2, [mu_sigma^2] = 2, A coupling g A_i psibar Gamma^i psi "
                                           "[g] = 0; all >= 0; nothing non-polynomial inserted"),
    "b2 interacting leaf pair (large-N O(N) + Cl(6))": dict(U="PASS", why="[lambda] = 1, [m0^2] = 2, [g_B^2] = 0, "
                                                            "[g_F] = 0 (HZ1's counting); m^2 polynomial in A"),
    "c1 Bose mode, thermodynamic pairing": dict(U="FAIL", why=f"chemical potential lambda_A |A| inserted: "
                                                f"{uv_admissible(x3, x3)}"),
    "c2 bath at dS-Unruh T(A)": dict(U="PASS", why=f"free 4-d bosons (z = 1); inserted P(T(A)) polynomial in A^2: "
                                     f"{uv_admissible(((x3**2 + 1)**2), x3)}; the thermal state at T(A) is assumed"),
    "c3 holographic leaf pair (G3 fields)": dict(U="PASS", why="HZ1 (i-p): all couplings >= 0 at z = 3"),
    "c4 horizon dof": dict(U="FAIL", why="no local action (horizon entropy counted, not a field theory)"),
}
for k, v in U.items():
    say(f"  {k:48s} U {v['U']}: {v['why']}")
OUT["U"] = U

# analyticity detector for c2 (graded statement: P(T(A)) has no odd powers of A when H > 0)
Hp = sp.symbols("Hp", positive=True)
T_c2 = sp.sqrt(x3**2 + Hp**2) / (2 * sp.pi)
det_c2_T4 = uv_admissible((T_c2**4).subs(Hp, 1), x3)
det_c2_T3 = uv_admissible((T_c2**3).subs(Hp, 1), x3)
say(f"c2 analyticity: P ~ T^4 at H > 0: odd orders {det_c2_T4['odd_orders']}; a 3-d bath P ~ T^3 at H > 0: odd orders "
    f"{det_c2_T3['odd_orders']} (no |A|^3 for any bath with T >= H/2pi > 0)")
OUT["c2_analyticity"] = {"T4": det_c2_T4, "T3": det_c2_T3}

# ==================================================================== labels
say("\n=== LABELS (worse footing; lane = best candidate) ===")
RANK = {"ORIGIN FOUND": 3, "ORIGIN UNDER ASSUMPTION": 2, "SHAPE ONLY": 1, "NONE": 0}


def label(S, CH, CW, Uv):
    if S != "PASS":
        return "NONE"
    if CH == "PASS" and Uv == "PASS":
        return "ORIGIN FOUND"
    if CW == "PASS" and Uv == "PASS":
        return "ORIGIN UNDER ASSUMPTION"
    return "SHAPE ONLY"


LAB = {}
for name in CANDS:
    if name.startswith("M1"):
        continue
    per = {}
    for f in FOOT:
        per[f] = label(FITS[f][name]["S"], CRES[f][name]["C_H"], CRES[f][name]["C_W"], U[name]["U"])
    worst = min(per.values(), key=lambda v: RANK[v])
    LAB[name] = {"per_footing": per, "label": worst}
    say(f"  {name:48s} S {FITS['canonical'][name]['S']}/{FITS['alt'][name]['S']}, "
        f"C_H {CRES['canonical'][name]['C_H']}/{CRES['alt'][name]['C_H']}, "
        f"C_W {CRES['canonical'][name]['C_W']}/{CRES['alt'][name]['C_W']}, U {U[name]['U']} -> {worst}")
best = max(LAB.values(), key=lambda v: RANK[v["label"]])["label"]
LANE = best if (KA_ALL and RED_OK) else "OPEN"
bests = [k for k, v in LAB.items() if v["label"] == best]
say(f"\nNPJ1 LANE LABEL: {LANE}   (best: {', '.join(bests)})")
OUT["labels"] = LAB
OUT["lane_label"] = LANE

# W0 reading (reported, never a label)
w0 = {}
for name in ("b2 interacting leaf pair (large-N O(N) + Cl(6))", "c3 holographic leaf pair (G3 fields)"):
    w0[name] = {f: {"amp_count_only": CRES[f][name]["C_W0_count_only_amp"],
                    "loc": "PASS" if CRES[f][name]["log10R_loc"] <= 0 else "FAIL"} for f in FOOT}
say(f"W0 (count alone; reported, not a label): {w0}")
OUT["W0_reported"] = w0

# ==================================================================== reported
say("\n=== REPORTED (not graded) ===")
REP = {}
# R2: the leaf fermion's momentum-dependent stiffness (KA7): Euclidean (g_F^2/4)|p| |dA|^2 per 8-component fermion
#   ratio to GR's |dA|^2/(2K): 2 pi nu N g_F^2 |p|/M_Pl^2 = (pi/2) B c |p|/(g_B E_a0)
for f in FOOT:
    sc = SC[f]
    q = FITS[f]["c3 holographic leaf pair (G3 fields)"]["params"]
    Bc = q[1] * 10 ** q[2]
    rM = math.sqrt(M_REF * GM_SUN / FOOT[f])
    rat = lambda pE: (math.pi / 2) * Bc * pE / (G4PI * sc["E_a0"])
    REP[f"R2_{f}"] = {"r_MOND_kpc": rM / KPC, "ratio_at_r_MOND": rat(HBARC / rM), "ratio_at_1AU": rat(E_AU),
                      "fermion_compton_at_a0_Gpc_over_gF": (C**2 / FOOT[f]) / (1e6 * KPC)}
    say(f"R2 [{f}] c3's leaf fermion (g_B = 4 pi): momentum-dependent stiffness / GR's = {rat(HBARC/rM):.2e} at the "
        f"MOND radius ({rM/KPC:.2f} kpc), {rat(E_AU):.2e} at 1 AU; its Compton length at A = a0 is "
        f"c^2/(g_F a0) = {(C**2/FOOT[f])/(1e6*KPC):.1f} Gpc/g_F")
    say(f"   dwarf (1e8 Msun): C-loc needs c_g >= {OUT['C_loc_A_gapped'][f]['dwarf_c_g_needed']:.3e}")
# R3: the lead's observations
for f in FOOT:
    sc = SC[f]
    a0 = FOOT[f]
    Jscale = a0**2 / (4 * math.pi * G)                       # J/m^3
    rhoc2 = sc["rho_de"] * C**2
    X_hz1 = CRES[f]["c3 holographic leaf pair (G3 fields)"]["X_eV"]
    REP[f"R3_{f}"] = {"J_scale_J_per_m3": Jscale, "rho_DE_c2_J_per_m3": rhoc2, "ratio": Jscale / rhoc2,
                      "one_over_16pi": 1 / (16 * math.pi), "log10_MPl_over_H": math.log10(M_PL / sc["E_H"]),
                      "log10_MPl_over_Ea0": math.log10(M_PL / sc["E_a0"]),
                      "log10_needed_over_H_ceiling": math.log10(X_hz1 / (1000 * M_PL * G4PI**3)),
                      "log10_needed_over_holo_nu_g3": math.log10(X_hz1 / (math.pi * M_PL**2 / sc["E_H"] * G4PI**3)),
                      "T_for_a0_eq_T2_over_MPl_meV": math.sqrt(sc["E_a0"] * M_PL) * 1e3}
    rr3 = REP[f"R3_{f}"]
    say(f"R3 [{f}] (2) a0^2/(4 pi G) = {Jscale:.4e} J/m^3 = {rr3['ratio']:.6f} rho_DE c^2 (1/(16 pi) = "
        f"{1/(16*math.pi):.6f}); (3) log10 M_Pl/H = {rr3['log10_MPl_over_H']:.2f}, log10 M_Pl/E_a0 = "
        f"{rr3['log10_MPl_over_Ea0']:.2f}; c3 needed / H ceiling = 10^{rr3['log10_needed_over_H_ceiling']:.2f}; "
        f"needed / holographic (pi M_Pl^2/H)(4pi)^3 = 10^{rr3['log10_needed_over_holo_nu_g3']:.2f}; "
        f"T with a0 = T^2/M_Pl: {rr3['T_for_a0_eq_T2_over_MPl_meV']:.3f} meV")
# R1: kappa
REP["R1"] = ("kappa: a1 a0' = alpha^3 Lambda^2/(8 pi M_Pl), Lambda free (not tied to rho_DE); b2/c3 a0 = c m_b0/g_B with "
             "m_b0 and Lambda_cc independent; a2 restates (A). No candidate fixes kappa; 5.41 untouched.")
say("R1 " + REP["R1"])
OUT["reported"] = REP

# ==================================================================== MUTATE twins
if MUTATE:
    say("\n=== MUTATE TWINS ===")
    TW = {}
    TW["M1"] = {"twin_S": FITS["canonical"]["M1 twin: mu = x^2/(1+x^2)"]["S"],
                "control_S": FITS["canonical"]["M1 control: the law"]["S"]}
    TW["M1"]["bites"] = TW["M1"]["twin_S"] == "FAIL" and TW["M1"]["control_S"] == "PASS"
    q3 = FITS["canonical"]["c3 holographic leaf pair (G3 fields)"]["params"]
    m2 = leaf_pair_C(SC["canonical"], FOOT["canonical"], q3[1], 10 ** q3[2], a0_energy=M_PL)
    TW["M2"] = {"log10R_H": m2["log10R_H"], "bites": m2["log10R_H"] <= 0}
    cg3 = (1 / (1 / 3)**2) / math.sqrt(1.01)
    TW["M3"] = {"c_g_needed": cg3, "bites": cg3 <= G4PI}
    TW["M4"] = {"det": uv_admissible(1 + x3**2 + x3**4 / 3 + x3**6 / 7, x3)}
    TW["M4"]["bites"] = TW["M4"]["det"]["admissible"]
    m5 = uv_admissible((x3 / (2 * sp.pi))**3, x3)                 # T = |A|/(2 pi), P ~ T^3, H = 0
    TW["M5"] = {"det": m5, "bites": 3 in m5["odd_orders"]}
    lam_sp6 = M_PL**2 / (1000 * M_PL)                              # leaf: N nu = 1000 M_Pl
    TW["M6"] = {"Lambda_sp_eV": lam_sp6, "bites": lam_sp6 >= E_KPC}
    # M7: BE W with the field linear in the fugacity: L_sec = (a0^2/K) sup_p [p u - W_BE(p)], W_BE = ln Z_BE(p) - p,
    #     maximized numerically over p; mu = 1 - Lred'(u)/u by central differences
    def Lred(uv):
        res = minimize_scalar(lambda pp: -(pp * uv - (-math.log(1 - pp) - pp)), bounds=(0, 1 - 1e-15),
                              method="bounded", options={"xatol": 1e-14})
        return -res.fun
    hh = 1e-5
    mu7 = np.array([1 - (Lred(uv * (1 + hh)) - Lred(uv * (1 - hh))) / (2 * hh * uv) / uv for uv in XG])
    TW["M7"] = {"max_dmu": float(np.max(np.abs(mu7 - MU_LAW)))}
    TW["M7"]["bites"] = TW["M7"]["max_dmu"] < 1e-6
    for k, v in TW.items():
        say(f"  {k}: {v}")
    OUT["MUTATE"] = TW
    say(f"ALL TWINS BITE: {all(v['bites'] for v in TW.values())}")

# ==================================================================== write
rt = time.time() - T_START
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9      # bytes on macOS
say(f"\nruntime {rt:.1f} s, peak memory {mem:.2f} GB")
say("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
OUT["runtime_s"] = round(rt, 1)
stem = "npj1_MUTATE" if MUTATE else "npj1"
with open(os.path.join(HERE, stem + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, stem + ".out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
