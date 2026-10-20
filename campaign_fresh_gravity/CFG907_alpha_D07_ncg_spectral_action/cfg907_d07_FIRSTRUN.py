#!/usr/bin/env python3
"""cfg907_d07.py -- CFG907, alpha door D07 (frozen criteria: CFG907_PREREGISTRATION.md, commit 088b4e0b2).

The noncommutative-geometry spectral action Tr f(D_A/Lambda) fixes, at the cutoff scale Lambda,
    g_3^2 = g_2^2 = (5/3) g'^2 = g_U^2   and   g_U^2 f_0/(2 pi^2) = 1/4      (CCM hep-th/0610241, RECALLED; re-derived here, gates K3-K6),
with f_0 = f(0).  The entropy identification (CCvS arXiv:1809.02944, RECALLED) forces f = h, h(x) = ln(1+e^-x) + x/(1+e^x), so f_0 = ln 2 and
1/alpha_U = 8 f_0/pi = 1.7651.  Graded trial G1 (one trial): entropy function, Lambda = mu_23 (a_2 = a_3 on the self-consistent trajectory),
joint legs A (8 f_0/pi vs a_23) and Y (a_Y(mu_23) = (5/3) 8 f_0/pi shot to M_t with Y1's running, mapped to 1/alpha(0) by CFG896's map).
Reported: the other 7 configurations (characteristic function; Lambda at mu_12, mu_13, Lambda_G), R1 ratio leg alone, R2 full run-down,
R3 Lambda = M_P, R4 tuned knobs, the substitution test.

Run:          OMP_NUM_THREADS=1 nice -n 10 python3 cfg907_d07.py              (exit 0 iff every gate passes)
MUTATE:       OMP_NUM_THREADS=1 nice -n 10 python3 cfg907_d07.py MUTATE       (boundary ratio 5/3 -> 3/5: K3e/K3f must fail -> exit 1; 3 if not)
MUTATE_NORM:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg907_d07.py MUTATE_NORM  (48-state H_F, normalisation halved: K3d/K3g/K6 must fail -> exit 1)
Writes cfg907_d07.json / cfg907_d07_MUTATE.json / cfg907_d07_MUTATE_NORM.json.  Imports lane Y1 (y1_lib, y1_4_results.json) and lane B
(rg_common: lepton masses for the Delta_t bound) READ-ONLY.  No bytecode, one core, about a minute.
Nothing here derives alpha.  Measured masses and alpha_s are labelled inputs; the SM mass sector stays walled; kappa and Z play no part.
"""
import sys
sys.dont_write_bytecode = True
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import json
import math
import time
import numpy as np
from numpy.polynomial import polynomial as NP
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import sympy as sp
import mpmath as mp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
AP = os.path.join(HERE, "..", "..", "real_research", "alpha_principle_2026")
Y1DIR = os.path.join(AP, "Y1_running_precision")
sys.path.insert(0, Y1DIR)
sys.path.insert(0, os.path.join(AP, "B_rg_asymptotic_safety"))
import y1_lib as L          # noqa: E402  (read-only)
import rg_common as RG      # noqa: E402  (read-only; lepton masses for the two-loop bound of the target transport)

MODE = sys.argv[1] if len(sys.argv) > 1 else "REAL"
if MODE not in ("REAL", "MUTATE", "MUTATE_NORM"):
    raise SystemExit("mode must be REAL, MUTATE or MUTATE_NORM")
MUT_RATIO = MODE == "MUTATE"
MUT_NORM = MODE == "MUTATE_NORM"
PI = math.pi
A0INV = 137.035999177          # CODATA 2022: the TARGET only (and Delta_t, CFG896's map)
MP = 1.220890e19               # G_N^(-1/2) in GeV (Y1 X_P / lane B MPL)
IDENT = A0INV * (1.0 - 1.0 / 1.01)   # 1.3568: shift of 1/alpha(0) an identity would show under alpha x 1.01
fails = []
OUT = dict(mode=MODE, frozen_criteria="088b4e0b2")


def chk(name, ok, info=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {info}")
    if not ok:
        fails.append(name)
    return ok


def fl(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (sp.Basic,)):
        return float(x)
    if isinstance(x, dict):
        return {str(k): fl(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [fl(v) for v in x]
    if isinstance(x, np.ndarray):
        return [fl(v) for v in x.tolist()]
    return x


print("=" * 132)
print("CFG907 alpha door D07: NCG spectral action with a forced cutoff function -- mode:",
      {"REAL": "REAL RUN", "MUTATE": "MUTATE (boundary ratio 5/3 -> 3/5)", "MUTATE_NORM": "MUTATE_NORM (H_F without the antiparticle half)"}[MODE])
print("=" * 132)

# ================================================================================================ A. the boundary condition (K3-K6)
print("\nK3  the boundary condition derived from the Gilkey a_4 coefficient and the SM + nu_R content (sympy, exact)")
s1 = sp.Matrix([[0, 1], [1, 0]])
s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
s3 = sp.Matrix([[1, 0], [0, -1]])
Z2, I2 = sp.zeros(2), sp.eye(2)


def blk(a, b, c, d):
    return sp.Matrix(sp.BlockMatrix([[a, b], [c, d]]).as_explicit())


GAM = [blk(Z2, -sp.I * s, sp.I * s, Z2) for s in (s1, s2, s3)] + [blk(Z2, I2, I2, Z2)]     # Euclidean, hermitian, {g^m, g^n} = 2 delta
cliff = all(sp.simplify(GAM[m] * GAM[n] + GAM[n] * GAM[m] - (2 if m == n else 0) * sp.eye(4)) == sp.zeros(4) for m in range(4) for n in range(4))
herm = all(GAM[m].H == GAM[m] for m in range(4))
chk("K3a Euclidean gamma matrices: Clifford relations and hermiticity", cliff and herm)
rng = np.random.default_rng(907)
FM = sp.zeros(4)
for m in range(4):
    for n in range(m + 1, 4):
        FM[m, n] = sp.Rational(int(rng.integers(-9, 10)), int(rng.integers(1, 8)))
        FM[n, m] = -FM[m, n]
FF = sum(FM[m, n] ** 2 for m in range(4) for n in range(4))
GG = {(m, n): GAM[m] * GAM[n] for m in range(4) for n in range(4)}
T4 = sp.nsimplify(sum((GG[(m, n)] * GG[(r, s)]).trace() * FM[m, n] * FM[r, s] for m in range(4) for n in range(4) for r in range(4) for s in range(4)))
EF = -sp.Rational(1, 2) * sum((GG[(m, n)] * FM[m, n] for m in range(4) for n in range(4)), sp.zeros(4))
trEF2 = sp.nsimplify((EF * EF).trace())
trOm2 = 4 * FF                                       # tr_S(1) = 4 times tr_V(F_mn F_mn)
chk("K3b spinor traces: tr(g^m g^n g^r g^s) F_mn F_rs = -8 F.F and tr_S(E_F^2) = -2 F.F (random antisymmetric F)", T4 == -8 * FF and trEF2 == -2 * FF,
    f"F.F = {FF}, T4 = {T4}, tr E_F^2 = {trEF2}")
C_GAUGE = sp.Rational(1, 360) * (180 * (trEF2 / FF) + 30 * (trOm2 / FF))   # gauge part of a_4 per tr_V(F.F), x (4 pi)^-2
chk("K3c Gilkey combination (1/360)(180 tr E^2 + 30 tr Omega^2) per tr_V(F.F) = -2/3", C_GAUGE == sp.Rational(-2, 3), f"{C_GAUGE}")

GEN = [("Q_L", 3, 2, sp.Rational(1, 6)), ("u_R", 3, 1, sp.Rational(2, 3)), ("d_R", 3, 1, sp.Rational(-1, 3)),
       ("L_L", 1, 2, sp.Rational(-1, 2)), ("e_R", 1, 1, sp.Integer(-1)), ("nu_R", 1, 1, sp.Integer(0))]


def content(ndouble):
    half = sp.Rational(1, 2)
    dim = ndouble * 3 * sum(nc * ni for _, nc, ni, _ in GEN)
    c3 = ndouble * 3 * sum(ni * (half if nc == 3 else 0) for _, nc, ni, _ in GEN)
    c2 = ndouble * 3 * sum(nc * (half if ni == 2 else 0) for _, nc, ni, _ in GEN)
    cy = ndouble * 3 * sum(nc * ni * y ** 2 for _, nc, ni, y in GEN)
    return dict(dim=dim, C3=c3, C2=c2, CY=cy)


CREF = content(2)                                   # the CCM count: particles + antiparticles, 96 states
CON = content(1) if MUT_NORM else CREF              # MUTATE_NORM: the antiparticle half dropped (48 states)
anom_Y = sum(nc * ni * y for _, nc, ni, y in GEN) == 0 and sum(nc * ni * y ** 3 for _, nc, ni, y in GEN) == 0
chk("K3d content traces over H_F: dim 96, C_3 = C_2 = 12, C_Y = 20 (and sum Y = sum Y^3 = 0 per generation)",
    CON["dim"] == 96 and CON["C3"] == 12 and CON["C2"] == 12 and CON["CY"] == 20 and anom_Y,
    f"dim {CON['dim']}, C_3 {CON['C3']}, C_2 {CON['C2']}, C_Y {CON['CY']}")
RATIO_DER = CON["CY"] / CON["C2"]                   # g_U^2 / g'^2 = C_Y / C_2  ->  a_Y(Lambda) = (C_Y/C_2) a_U
RATIO_USED = 1 / RATIO_DER if MUT_RATIO else RATIO_DER
RATIO_REF = CREF["CY"] / CREF["C2"]
S2W_USED = 1 / (1 + RATIO_USED)                     # g'^2/(g^2 + g'^2) at Lambda
chk("K3e boundary ratio used = C_Y/C_2 derived = the recalled printed 5/3", RATIO_USED == RATIO_DER == sp.Rational(5, 3), f"used {RATIO_USED}, derived {RATIO_DER}")
chk("K3f sin^2 theta_W at Lambda = 3/8 (recalled printed)", S2W_USED == sp.Rational(3, 8), f"{S2W_USED}")
NORM_DER = sp.Integer(3) / CON["C2"]               # f_0 g^2/(2 pi^2) from f_0 g^2 C/(24 pi^2) = 1/4
chk("K3g normalisation f_0 g^2/(2 pi^2) = 3/C derived = the recalled printed 1/4 (SU(3), SU(2); and (5/3) f_0 g'^2/(2 pi^2) = 1/4)",
    NORM_DER == sp.Rational(1, 4) and sp.Integer(3) / CON["C3"] == sp.Rational(1, 4) and sp.Rational(5, 3) * 3 / CON["CY"] == sp.Rational(1, 4), f"{NORM_DER}")
chk("K3h C_3 = C_2 (the E1 leg g_3 = g_2 at Lambda)", CON["C3"] == CON["C2"])

print("\nK4  Gilkey coefficients checked numerically on exact spectra")
# (a) unit S^2 scalar Laplacian: t K(t) = 1 + t (1/6) R + t^2 (1/360)(5R^2 - 2Ric^2 + 2Riem^2) + ..., R = 2, |Ric|^2 = 2, |Riem|^2 = 4
g_a2 = sp.Rational(1, 6) * 2
g_a4 = sp.Rational(1, 360) * (5 * 4 - 2 * 2 + 2 * 4)
ts = np.linspace(0.004, 0.06, 22)
gv = []
for t in ts:
    lmax = int(math.sqrt(90.0 / t)) + 20
    l = np.arange(lmax + 1, dtype=float)
    K = float(np.sum((2 * l + 1) * np.exp(-t * l * (l + 1))))
    gv.append((t * K - 1.0) / t)
cS2 = NP.polyfit(ts / 0.06, np.array(gv), 6)
cS2 = [cS2[k] / 0.06 ** k for k in range(len(cS2))]
chk("K4a S^2: coefficients of t and t^2 in t K(t) equal Gilkey's 1/3 (R/6) and 1/15 (curvature^2) to 1e-6",
    abs(cS2[0] - float(g_a2)) < 1e-6 and abs(cS2[1] - float(g_a4)) < 1e-6, f"{cS2[0]:.10f} vs {float(g_a2):.10f}; {cS2[1]:.10f} vs {float(g_a4):.10f}")
# (b) 2D Landau levels, B = 1, per unit area: scalar levels (2n+1)B, degeneracy B/2pi; spinor (sigma.pi)^2 = pi^2 - B sigma_3 (E = B sigma_3)
Bs = sp.Symbol("B", positive=True)
Om12 = -sp.I * Bs
trOmOm_scalar = sp.expand(2 * Om12 ** 2)                           # Omega_12^2 + Omega_21^2
pred_scalar = sp.Rational(1, 360) * 30 * trOmOm_scalar / Bs ** 2
E_sp = sp.diag(Bs, -Bs)
pred_spinor = sp.Rational(1, 360) * (180 * (E_sp * E_sp).trace() + 30 * 2 * trOmOm_scalar) / Bs ** 2
tL = np.linspace(0.02, 0.4, 30)
ysc, ysp = [], []
for t in tL:
    n = np.arange(int(25.0 / t) + 50, dtype=float)
    ysc.append(2 * t * float(np.sum(np.exp(-t * (2 * n + 1)))))
    ysp.append(2 * t * float(np.sum(np.exp(-2 * n * t)) + np.sum(np.exp(-2 * (n + 1) * t))))
csc = NP.polyfit(tL / 0.4, np.array(ysc), 10)
csp = NP.polyfit(tL / 0.4, np.array(ysp), 10)
csc2, csp2 = csc[2] / 0.16, csp[2] / 0.16
chk("K4b Landau scalar: t^2 coefficient of 4 pi t K/area = Gilkey (30/360) tr Omega^2 = -1/6 (rel 1e-6)",
    abs(csc2 / float(pred_scalar) - 1) < 1e-6 and abs(csc[0] - 1) < 1e-9, f"{csc2:.10f} vs {pred_scalar}")
chk("K4c Landau spinor: t^2 coefficient = Gilkey (1/360)(180 tr E^2 + 30 tr Omega^2) = +2/3 (rel 1e-6)",
    abs(csp2 / float(pred_spinor) - 1) < 1e-6 and abs(csp[0] - 2) < 1e-9, f"{csp2:.10f} vs {pred_spinor}")

print("\nK5  cutoff functions and their moments")
x = sp.Symbol("x", real=True)
h_expr = sp.log(1 + sp.exp(-x)) + x / (1 + sp.exp(x))
occ = 1 / (1 + sp.exp(x))
bin_ent = -occ * sp.log(occ) - (1 - occ) * sp.log(1 - occ)
mp.mp.dps = 30
hf = sp.lambdify(x, h_expr, "mpmath")
bf = sp.lambdify(x, bin_ent, "mpmath")
pts = [mp.mpf(v) for v in ("-7.3", "-2.2", "-0.61", "-0.05", "0.013", "0.4", "1.0", "2.5", "4.75", "9.1", "15.0", "27.5")]
d_bin = max(abs(hf(p) - bf(p)) for p in pts)
d_even = max(abs(hf(p) - hf(-p)) for p in pts)
h0 = sp.simplify(h_expr.subs(x, 0))
chk("K5a h = binary entropy of the Fermi occupation 1/(1+e^x), h even, h(0) = ln 2 exactly",
    d_bin < 1e-25 and d_even < 1e-25 and sp.simplify(h0 - sp.log(2)) == 0, f"max|h - s| {mp.nstr(d_bin, 3)}, max|h(x)-h(-x)| {mp.nstr(d_even, 3)}, h(0) = {h0}")
F2_H = mp.quad(lambda v: hf(v) * v, [0, 1, 10, mp.inf])
F4_H = mp.quad(lambda v: hf(v) * v ** 3, [0, 1, 10, 40, mp.inf])
f2_h = sp.Rational(9, 4) * sp.zeta(3)
f4_h = sp.Rational(225, 8) * sp.zeta(5)
chk("K5b entropy moments: f_2 = 9 zeta(3)/4, f_4 = 225 zeta(5)/8 (quadrature, rel 1e-10)",
    abs(F2_H / mp.mpf(sp.N(f2_h, 30)) - 1) < 1e-10 and abs(F4_H / mp.mpf(sp.N(f4_h, 30)) - 1) < 1e-10,
    f"f_2 {mp.nstr(F2_H, 12)} vs {sp.N(f2_h, 12)}; f_4 {mp.nstr(F4_H, 12)} vs {sp.N(f4_h, 12)}")
v = sp.Symbol("v", positive=True)
chk("K5c characteristic function chi_[0,1]: f_0 = 1, f_2 = 1/2, f_4 = 1/4",
    sp.integrate(v, (v, 0, 1)) == sp.Rational(1, 2) and sp.integrate(v ** 3, (v, 0, 1)) == sp.Rational(1, 4))
FUNCS = {"entropy": dict(f0=math.log(2.0), f2=float(sp.N(f2_h, 20)), f4=float(sp.N(f4_h, 20)), label="entropy h, f_0 = ln 2 (forced)"),
         "char": dict(f0=1.0, f2=0.5, f4=0.25, label="characteristic chi / any f(0) = 1, f_0 = 1 (K0)")}

print("\nK6  Einstein-Hilbert coefficient and Lambda_G")
f2s, Lam, Rs = sp.symbols("f_2 Lambda R", positive=True)
NF = CON["dim"]
EH = 2 * f2s * Lam ** 2 * sp.Rational(1, 16) / sp.pi ** 2 * sp.Rational(1, 6) * (4 * NF * (6 * (-Rs / 4) + Rs))
chk("K6 2 f_2 Lambda^2 a_2|_R = -(96 f_2 Lambda^2/(24 pi^2)) R (the recalled CCM form, Majorana c neglected)",
    sp.simplify(EH + 96 * f2s * Lam ** 2 * Rs / (24 * sp.pi ** 2)) == 0, f"{sp.simplify(EH)}")


def lambda_G(f2):
    # 1/(16 pi G) = N_F f_2 Lambda^2/(24 pi^2), G = 1/M_P^2  ->  Lambda^2 = 3 pi M_P^2/(2 N_F f_2)   (N_F = 96: pi/(64 f_2))
    return MP * math.sqrt(3 * PI / (2 * float(NF) * f2))


for k in FUNCS:
    FUNCS[k]["LamG"] = lambda_G(FUNCS[k]["f2"])
    FUNCS[k]["aU"] = 2 * FUNCS[k]["f0"] * float(CON["C2"]) / (3 * PI)            # 4 pi/g_U^2 with g_U^2 = 6 pi^2/(f_0 C_2)
    FUNCS[k]["aU_ref"] = 2 * FUNCS[k]["f0"] * float(CREF["C2"]) / (3 * PI)
    FUNCS[k]["aYb"] = float(RATIO_USED) * FUNCS[k]["aU"]                           # a_Y(Lambda) = (C_Y/C_2) a_U
    FUNCS[k]["aYb_ref"] = float(RATIO_REF) * FUNCS[k]["aU_ref"]
    print(f"   {FUNCS[k]['label']}: 1/alpha_U = {FUNCS[k]['aU']:.6f}, a_Y(Lambda) = {FUNCS[k]['aYb']:.6f}, Lambda_G = {FUNCS[k]['LamG']:.5e} GeV"
          f"  (f_2 = {FUNCS[k]['f2']:.6f})")
OUT["boundary"] = dict(C=dict(dim=int(CON["dim"]), C3=float(CON["C3"]), C2=float(CON["C2"]), CY=float(CON["CY"])), ratio_used=float(RATIO_USED),
                       s2w=float(S2W_USED), norm=float(NORM_DER), funcs=fl(FUNCS), K4=dict(S2=fl(cS2[:2]), landau_scalar=csc2, landau_spinor=csp2))

# ================================================================================================ B. Y1's running (K1, K2)
with open(os.path.join(Y1DIR, "y1_4_results.json")) as fh:
    Y4 = json.load(fh)
_sxp = Y4["summary"]["X_P"]
SIG_MAP = _sxp["after_quad_pct"][3] / 100.0 * _sxp["central"][3]
THOMSON = Y4["summary"]["thomson_link_rel"] * A0INV
print(f"\nY1 error carried for the running + map: sigma_map = {SIG_MAP:.4f}, Thomson link {THOMSON:.4f}")
P = L.PDG
YB, YTAU = L.YB_MT_SMDR, L.YTAU_MT_SMDR
OPTS = L.L_default_opts()
OPTS_LO = L.Opts(gauge_loops=3, yuk_loops=2)


def bnd(Mt=None, als=None, Mh=None, MW=None, dyt=0.0, dlam=0.0, rel_g3=0.0, dg2=0.0, dgY=0.0, gY=None):
    """u0 at mu = M_t: g_3 by Y1's QCD-only route (SMDR-calibrated), y_t, lambda, g_2 (and g_Y unless given) from Buttazzo (as CFG896)."""
    Mt = P["Mt"] if Mt is None else Mt
    als = P["als"] if als is None else als
    Mh = P["Mh"] if Mh is None else Mh
    MW = P["MW"] if MW is None else MW
    g3 = L.g3_base(als, Mt) * (1 + rel_g3)
    _, c = L.buttazzo_boundary(Mt, Mh, MW, als, g3_override=g3, dg2=dg2, dgY=dgY, dyt=dyt, dlam=dlam)
    gYv = c["gY"] if gY is None else gY
    u0 = L.u_from_gY_g2_g3(gYv, c["g2"], g3, c["yt"], YB, YTAU, c["lam"])
    return u0, Mt, dict(c, gY=gYv, g3=g3)


u_c, Mt_c, c_c = bnd()
A_t = L.a_from_u(u_c)
AY_T, A2_T = float(A_t[0]), float(A_t[1])
DELTA_T = A0INV - (AY_T + A2_T)
print(f"measured point at mu = M_t = {Mt_c}: g_Y {c_c['gY']:.6f} (target only), g_2 {c_c['g2']:.6f}, g_3 {c_c['g3']:.6f}, y_t {c_c['yt']:.6f}, lambda {c_c['lam']:.6f}")
print(f"   a_Y(M_t) = {AY_T:.5f}, a_2(M_t) = {A2_T:.5f}; Delta_t = {DELTA_T:.5f} (CFG896's target transport)")

print("\nK1  reproduce Y1's validated numbers exactly")
tr_c = L.Traj(u_c, Mt_c, OPTS, mu_max=3e21)
A_P = tr_c.A(MP)
y1_printed = dict(aY=55.2342, a2=49.2026, a3=52.9713, aem=104.4368)
mine = dict(aY=A_P[0], a2=A_P[1], a3=A_P[2], aem=A_P[0] + A_P[1])
for k in y1_printed:
    chk(f"K1(i) Y1-central {k}(X_P)", abs(mine[k] - y1_printed[k]) <= 1e-4, f"mine {mine[k]:.5f} printed {y1_printed[k]}")
oB = L.Opts(gauge_loops=3, yuk_loops=3, qcd4=True)
uB, _ = L.buttazzo_boundary(173.34, 125.15, 80.384, 0.1184)
uP = L.Traj(uB, 173.34, oB, mu_max=MP * 1.001).u(MP)
rB = dict(g1=math.sqrt(uP[0]), g2=math.sqrt(uP[1]), g3=math.sqrt(uP[2]), yt=math.sqrt(uP[3]), lam=uP[6])
y1_v2 = dict(g1=0.61537, g2=0.50546, g3=0.48731, yt=0.38248, lam=-0.01437)
for k in y1_v2:
    chk(f"K1(ii) Buttazzo-input like-for-like {k}(M_P)", abs(rB[k] - y1_v2[k]) <= 1e-5, f"mine {rB[k]:+.6f} printed {y1_v2[k]:+.5f}")

print("\nK2  the SM one-scale unification failure (lane Z1) reproduced with Z1's grid")
trZ = L.run_central(mu_max=1e21)
musZ = np.exp(np.linspace(math.log(1.1 * P["Mt"]), math.log(1e21), 4000))
AZ = np.array([trZ.A(m) for m in musZ])


def spread(vals):
    return (vals.max(axis=1) - vals.min(axis=1)) / vals.mean(axis=1)


z1 = {}
for name, fac in (("Y", np.array([1.0, 1.0, 1.0])), ("GUT", np.array([0.6, 1.0, 1.0]))):
    V = AZ * fac
    S = spread(V)
    i = int(np.argmin(S))
    z1[name] = dict(spread=100 * S[i], mu=musZ[i], vals=V[i].tolist(), cross={})
    for (p, q, r, lab) in ((0, 1, 2, "a_Y=a_2"), (0, 2, 1, "a_Y=a_3"), (1, 2, 0, "a_2=a_3")):
        d = V[:, p] - V[:, q]
        idx = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
        k = idx[0]
        pair = 0.5 * (V[k, p] + V[k, q])
        z1[name]["cross"][lab] = (musZ[k], 100 * (V[k, r] - pair) / pair, musZ[k + 1])
z1_printed = {"GUT": (7.62, 1.737e14, (40.47, 43.63, 40.47)), "Y": (8.37, 3.388e19, None)}
for name, (spr, mu, vals) in z1_printed.items():
    ok = abs(z1[name]["spread"] - spr) <= 0.005 and abs(z1[name]["mu"] / mu - 1) <= 0.0005 / (mu / 10 ** math.floor(math.log10(mu)))
    if vals is not None:
        ok = ok and all(abs(a - b) <= 0.005 for a, b in zip(z1[name]["vals"], vals))
    chk(f"K2(i) {name}-normalised minimum spread", ok, f"mine {z1[name]['spread']:.3f}% at {z1[name]['mu']:.4e} ({', '.join(f'{a:.3f}' for a in z1[name]['vals'])}); Z1 {spr}% at {mu:.3e}")
z1_cross = {("Y", "a_Y=a_2"): (5.351e20, 12.0), ("Y", "a_Y=a_3"): (3.388e19, -8.1), ("Y", "a_2=a_3"): (2.785e16, 34.1),
            ("GUT", "a_Y=a_2"): (1.112e13, -11.5), ("GUT", "a_Y=a_3"): (1.718e14, 7.8), ("GUT", "a_2=a_3"): (2.785e16, -19.6)}
for (name, lab), (mu, miss) in z1_cross.items():
    m_mine, miss_mine, _ = z1[name]["cross"][lab]
    tol_mu = 0.0005 / (mu / 10 ** math.floor(math.log10(mu)))
    chk(f"K2(ii) {name} {lab} crossing and third-coupling miss", abs(m_mine / mu - 1) <= tol_mu and abs(miss_mine - miss) <= 0.05,
        f"mine {m_mine:.4e} {miss_mine:+.2f}%; Z1 {mu:.3e} {miss:+.1f}%")
MU23_M = L.crossing(trZ, "a2", "a3")
MU12_M = L.crossing(trZ, "a1", "a2")
MU13_M = L.crossing(trZ, "a1", "a3")
for lab, mref, key in (("a_2=a_3", MU23_M, ("GUT", "a_2=a_3")), ("a_1=a_2", MU12_M, ("GUT", "a_Y=a_2")), ("a_1=a_3", MU13_M, ("GUT", "a_Y=a_3"))):
    lo, _m, hi = z1[key[0]]["cross"][key[1]][0], None, z1[key[0]]["cross"][key[1]][2]
    chk(f"K2(iii) refined {lab} crossing inside Z1's grid step", lo <= mref <= hi, f"{mref:.5e} in [{lo:.5e}, {hi:.5e}]")
A23_M = trZ.A(MU23_M)
print(f"   measured trajectory: mu_23 = {MU23_M:.5e} (a_2 = a_3 = {A23_M[1]:.4f}, a_Y = {A23_M[0]:.4f}, a_1 = {0.6 * A23_M[0]:.4f}: "
      f"{100 * (0.6 * A23_M[0] / A23_M[1] - 1):+.2f}%); mu_12 = {MU12_M:.5e}; mu_13 = {MU13_M:.5e}")
OUT["K1"] = dict(mine=fl(mine), buttazzo=fl(rB))
OUT["K2"] = dict(z1=fl({k: dict(spread=v["spread"], mu=v["mu"], vals=v["vals"], cross={kk: list(vv) for kk, vv in v["cross"].items()}) for k, v in z1.items()}),
                 mu23=MU23_M, mu12=MU12_M, mu13=MU13_M, a_at_mu23=fl(A23_M))

# ================================================================================================ C. the shooting machinery
class NoReach(Exception):
    pass


def traj(u0, Mt, mu_max, o=None, rtol=1e-11):
    try:
        tr = L.Traj(u0, Mt, OPTS if o is None else o, mu_max=mu_max, rtol=rtol)
    except RuntimeError as e:
        raise NoReach(str(e))
    ue = tr.sol.y[:, -1]
    if (not np.all(np.isfinite(ue))) or np.any(ue[:3] <= 0) or ue[0] > 4 * PI * 20:
        raise NoReach("blow-up")
    return tr


def cross23(tr, mu_hi):
    lg = np.linspace(math.log(1e13), math.log(0.999 * mu_hi), 400)
    U = tr.sol.sol(lg)
    d = 4 * PI / U[1] - 4 * PI / U[2]
    idx = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
    if len(idx) == 0:
        raise NoReach("no a_2 = a_3 crossing")
    f = lambda t: float(4 * PI / tr.sol.sol(t)[1] - 4 * PI / tr.sol.sol(t)[2])
    return math.exp(brentq(f, lg[idx[0]], lg[idx[0] + 1], xtol=1e-13))


def meas_cross(kind, inp):
    u0, Mt, _ = bnd(**inp)
    trm = L.Traj(u0, Mt, OPTS, mu_max=1e21)
    return L.crossing(trm, "a1", "a2" if kind == "meas12" else "a3")


def setup(spec, inp):
    """Resolve Lambda (when it does not depend on the shot trajectory) and mu_max for a configuration."""
    s = dict(spec)
    fac = s.get("fac", 1.0)
    if s["place"] == "mu23":
        s["mu_max"] = 1.15 * max(fac, 1.0) * MU23_M
    else:
        if s["place"] in ("meas12", "meas13"):
            base = meas_cross(s["place"], inp)
        else:
            base = s["mu"]
        s["Lam"] = fac * base
        s["mu_max"] = 1.15 * s["Lam"]
    return s


def evaluate(aYMt, s, inp, o=None, rtol=1e-11):
    u0, Mt, c = bnd(gY=math.sqrt(4 * PI / aYMt), **inp)
    tr = traj(u0, Mt, s["mu_max"], o, rtol)
    if s["place"] == "mu23":
        m23 = cross23(tr, s["mu_max"])          # the crossing is searched inside the integrated range only
        Lm = s.get("fac", 1.0) * m23
    else:
        m23 = None
        Lm = s["Lam"]
    A = tr.A(Lm)
    if s["target"] == "const":
        tgt = s["val"]
    else:                                   # 'ratio': a_Y(Lambda) = r a_2(Lambda)  (R1, f_0-free)
        tgt = s["r"] * A[1]
    tgt *= s.get("bscale", 1.0)
    a2t = 4 * PI / c["g2"] ** 2
    return dict(f=A[0] - tgt, tgt=tgt, Lam=Lm, mu23=m23, A=A.tolist(), aYMt=aYMt, a2Mt=a2t, P=aYMt + a2t + DELTA_T,
                abar=0.5 * (A[1] + A[2]), dE1=A[2] - A[1], tr=tr)


GRID = [400, 300, 220, 160, 130, 110, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 46, 42, 39, 36, 33, 30, 27, 24, 21, 18, 15, 12, 9, 6]


def fval(a, s, inp, o, rtol):
    try:
        return evaluate(a, s, inp, o, rtol)["f"]
    except NoReach:
        return -math.inf


def solve(spec, inp=None, o=None, rtol=1e-11, guess=None, scan=False):
    inp = {} if inp is None else inp
    s = setup(spec, inp)
    f = lambda a: fval(a, s, inp, o, rtol)
    status = "unique"
    info = {}
    if scan or guess is None:
        pts = []
        for a in GRID:
            fa = f(a)
            pts.append((a, fa))
            if fa == -math.inf:
                break
        # refine a jump from a positive finite value straight into NoReach
        if len(pts) >= 2 and pts[-1][1] == -math.inf and pts[-2][1] > 0:
            hi, lo = pts[-2][0], pts[-1][0]
            for _ in range(60):
                mid = 0.5 * (hi + lo)
                fm = f(mid)
                if fm == -math.inf:
                    lo = mid
                elif fm > 0:
                    hi = mid
                else:
                    pts.insert(len(pts) - 1, (mid, fm))
                    break
        fin = [(a, fa) for a, fa in pts if fa != -math.inf]
        mono = all(fin[i][1] > fin[i + 1][1] for i in range(len(fin) - 1))
        sgn = [fa > 0 for _, fa in pts]
        nchg = sum(1 for i in range(len(sgn) - 1) if sgn[i] != sgn[i + 1])
        info = dict(grid=[(a, (None if fa == -math.inf else fa)) for a, fa in pts], monotone=mono, sign_changes=nchg)
        if nchg == 0:
            return dict(status="none", info=info, spec=s)
        if nchg > 1 or not mono:
            status = "multiple" if nchg > 1 else "non-monotone"
        i = next(i for i in range(len(sgn) - 1) if sgn[i] != sgn[i + 1])
        a_hi, a_lo = pts[i][0], pts[i + 1][0]
        if pts[i + 1][1] == -math.inf:
            raise RuntimeError("bracket ends in NoReach")
    else:
        w = 1.5
        for _ in range(12):
            a_hi, a_lo = guess + w, max(guess - w, 0.5)
            fh, flo = f(a_hi), f(a_lo)
            if fh > 0 and flo < 0 and flo != -math.inf:
                break
            if fh > 0 and flo == -math.inf:
                hi, lo = a_hi, a_lo
                for _ in range(60):
                    mid = 0.5 * (hi + lo)
                    fm = f(mid)
                    if fm == -math.inf:
                        lo = mid
                    elif fm > 0:
                        hi = mid
                    else:
                        a_lo = mid
                        break
                if f(a_lo) < 0 and f(a_lo) != -math.inf:
                    break
            w *= 2
        else:
            raise RuntimeError("no bracket near the guess")
    root = brentq(f, a_lo, a_hi, xtol=1e-12, rtol=4e-16, maxiter=300)
    ev = evaluate(root, s, inp, o, rtol)
    ev.update(status=status, info=info, spec=s, resid=abs(ev["f"]))
    return ev


sMt = math.hypot(P["sMt_exp"], P["sMt_th"])
SG2 = abs(0.64779 - 0.64754) * max(abs(0.64779 - 0.64754) / abs(0.64754 - 0.65294), 0.108 / PI)     # Y1 E5a (as L.mc_draws)
SG3 = math.hypot(2.62e-5, 6.72e-5 / 2)                                                                # Y1 E5b
ITEMS = [("als", "alpha_s(M_Z) +-0.0009", dict(als=P["als"] + P["sals"]), dict(als=P["als"] - P["sals"])),
         ("MW", "M_W +-0.0133", dict(MW=P["MW"] + P["sMW"]), dict(MW=P["MW"] - P["sMW"])),
         ("Mt", f"M_t +-{sMt:.3f}", dict(Mt=P["Mt"] + sMt), dict(Mt=P["Mt"] - sMt)),
         ("Mh", "M_H +-0.09", dict(Mh=P["Mh"] + P["sMh"]), dict(Mh=P["Mh"] - P["sMh"])),
         ("g3m", "g_3 matching (Y1 E5b)", dict(rel_g3=SG3), dict(rel_g3=-SG3)),
         ("g2m", "g_2 matching (Y1 E5a)", dict(dg2=SG2), dict(dg2=-SG2)),
         ("ytm", "y_t matching +-0.0005", dict(dyt=0.0005), dict(dyt=-0.0005)),
         ("lamm", "lambda matching +-0.0003", dict(dlam=0.0003), dict(dlam=-0.0003))]


def errors(spec, base, do_inputs=True):
    """The frozen route-error components for one configuration (sections 7 and 8 of the pre-registration)."""
    g = base["aYMt"]
    out = dict(items={})
    if do_inputs:
        for key, _lab, ip, im in ITEMS:
            rp = solve(spec, ip, guess=g)
            rm = solve(spec, im, guess=g)
            out["items"][key] = dict(P=0.5 * (rp["P"] - rm["P"]), abar=0.5 * (rp["abar"] - rm["abar"]), dE1=0.5 * (rp["dE1"] - rm["dE1"]))
    sin = math.sqrt(sum(v["P"] ** 2 for v in out["items"].values()))
    sinA = math.sqrt(sum(v["abar"] ** 2 for v in out["items"].values()))
    sinE = math.sqrt(sum(v["dE1"] ** 2 for v in out["items"].values()))
    covYA = sum(v["P"] * v["abar"] for v in out["items"].values())
    r2 = solve(dict(spec, fac=2.0), guess=g)
    rh = solve(dict(spec, fac=0.5), guess=g)
    sthrY = 0.5 * abs(r2["P"] - rh["P"])
    sthrA = 0.5 * abs(r2["abar"] - rh["abar"])
    sthrE = 0.5 * abs(r2["dE1"] - rh["dE1"])
    aU_eff = spec["aU"] if spec["target"] == "const" else base["A"][1]
    eps = 3.0 / (4 * PI * aU_eff)                     # 3 alpha_U/(4 pi)
    bp = solve(dict(spec, bscale=1 + eps), guess=g)
    bm = solve(dict(spec, bscale=1 - eps), guess=g)
    sbndY = 0.5 * abs(bp["P"] - bm["P"])
    sbndA = eps * aU_eff
    lo = solve(spec, o=OPTS_LO, guess=g)
    sloop = abs(base["P"] - lo["P"])
    sY = math.sqrt(SIG_MAP ** 2 + THOMSON ** 2 + sin ** 2 + sthrY ** 2 + sbndY ** 2 + sloop ** 2)
    sY1A = 0.0012 * base["abar"]
    sA = math.sqrt(sinA ** 2 + sY1A ** 2 + sthrA ** 2 + sbndA ** 2)
    sE = math.sqrt(sinE ** 2 + (0.0012 * base["A"][2]) ** 2 + (0.00021 * base["A"][1]) ** 2 + sthrE ** 2)
    out.update(sigma_in=sin, sigma_in_A=sinA, sigma_in_E1=sinE, cov_in_YA=covYA, sigma_thr_Y=sthrY, sigma_thr_A=sthrA, sigma_thr_E1=sthrE,
               eps_bnd=eps, sigma_bnd_Y=sbndY, sigma_bnd_A=sbndA, sigma_loop=sloop, P_loworder=lo["P"], sigma_Y=sY, sigma_Y1_A=sY1A, sigma_A=sA,
               sigma_E1=sE, P_fac2=r2["P"], P_fachalf=rh["P"], P_bplus=bp["P"], P_bminus=bm["P"])
    return out


def grade(zs, root_status, gates_ok, delta_route):
    if not gates_ok:
        return "NOT COMPLETED"
    if delta_route > 1:
        return "NOT DIAGNOSTIC"
    if root_status in ("multiple", "non-monotone"):
        return "NOT DIAGNOSTIC"
    if root_status == "none":
        return "KILLED"
    if any(abs(z) > 3 for z in zs if z is not None):
        return "KILLED"
    return "CONSISTENT"


def p_single(miss):
    m = abs(miss)
    if m >= A0INV - 10:
        return 1.0
    return min(1.0, math.log((A0INV + m) / (A0INV - m)) / math.log(100.0))


print("\nK7(c)  classifier controls (planted inputs)")
cc = [("z = 0 both legs", grade([0.0, 0.0], "unique", True, 0.007), "CONSISTENT"),
      ("z_Y = +3.01", grade([3.01, 0.0], "unique", True, 0.007), "KILLED"),
      ("z_Y = -3.01", grade([-3.01, 0.0], "unique", True, 0.007), "KILLED"),
      ("z_Y = +2.99", grade([2.99, 0.0], "unique", True, 0.007), "CONSISTENT"),
      ("z_Y = -2.99", grade([-2.99, 0.0], "unique", True, 0.007), "CONSISTENT"),
      ("leg A fails, leg Y passes", grade([0.0, 5.0], "unique", True, 0.007), "KILLED"),
      ("no root", grade([None, None], "none", True, 0.007), "KILLED"),
      ("two roots", grade([0.0, 0.0], "multiple", True, 0.007), "NOT DIAGNOSTIC"),
      ("delta_route > 1", grade([0.0, 0.0], "unique", True, 1.5), "NOT DIAGNOSTIC"),
      ("failed gate", grade([0.0, 0.0], "unique", False, 0.007), "NOT COMPLETED")]
chk("K7(c) classifier returns the frozen grade in all 10 planted cases", all(g == e for _, g, e in cc), "; ".join(f"{n}: {g}" for n, g, _ in cc))

# ================================================================================================ D. G1 and the gates on it
print("\n" + "=" * 132)
print("G1 (graded): entropy function, Lambda = mu_23 on the self-consistent trajectory, joint legs A and Y")
print("=" * 132)
FE = FUNCS["entropy"]
SPEC_G1 = dict(place="mu23", target="const", val=FE["aYb"], aU=FE["aU"])
g1 = solve(SPEC_G1, scan=True)
print(f"   scan over a_Y(M_t): {[(a, (round(fv, 3) if fv is not None else 'NoReach')) for a, fv in g1['info']['grid']]}")
print(f"   root: a_Y(M_t) = {g1['aYMt']:.8f} (Y1-central {AY_T:.5f}); mu_23 = {g1['mu23']:.5e} (measured trajectory {MU23_M:.5e}); "
      f"a_Y(mu_23) = {g1['A'][0]:.8f} (target {g1['tgt']:.8f}), a_2 = a_3 = {g1['A'][1]:.5f}")
print("\nK8  solver")
chk("K8a boundary residual < 1e-8 at the root", g1["resid"] < 1e-8, f"{g1['resid']:.2e}")
g1b = solve(SPEC_G1, rtol=1e-13, guess=g1["aYMt"])
chk("K8b root stable between ODE rtol 1e-11 and 1e-13 (|dP| < 1e-6)", abs(g1b["P"] - g1["P"]) < 1e-6, f"|dP| = {abs(g1b['P'] - g1['P']):.2e}")
chk("K8c f strictly monotone on the scan grid with exactly one sign change", g1["status"] == "unique" and g1["info"]["monotone"] and g1["info"]["sign_changes"] == 1,
    f"status {g1['status']}, sign changes {g1['info']['sign_changes']}")
print("\nK7(a,b)  planted known answers")
pl = solve(dict(place="mu23", target="const", val=float(A23_M[0])), guess=AY_T)
chk("K7(a) boundary planted at Y1-central a_Y(mu_23): the shooting returns P = 137.035999177 (1e-6)", abs(pl["P"] - A0INV) < 1e-6,
    f"P = {pl['P']:.10f}, a_Y(M_t) = {pl['aYMt']:.8f}")
f0_pl = 3 * PI * g1["abar"] / (2 * float(CON["C2"]))
zA_pl = (2 * f0_pl * float(CON["C2"]) / (3 * PI) - g1["abar"]) / 1.0
chk("K7(b) f_0 planted at 3 pi a_23/(2 C_2): leg A residual 0 (1e-9)", abs(zA_pl) < 1e-9, f"{zA_pl:.2e}")
print("\nK9  one-loop linearity")
s1L = dict(place="fixed", mu=MU23_M, target="const", val=FE["aYb"])
r1L = solve(s1L, o=L.Opts(gauge_loops=1, yuk_loops=1), guess=g1["aYMt"])
tr1m = L.Traj(u_c, Mt_c, L.Opts(gauge_loops=1, yuk_loops=1), mu_max=1.2 * MU23_M)
shift_pred = r1L["aYMt"] - AY_T
shift_bnd = FE["aYb"] - tr1m.A(MU23_M)[0]
chk("K9 one-loop: a_Y^pred(M_t) - a_Y^meas(M_t) = a_Y^target(Lambda) - a_Y^meas(Lambda) (1e-6)", abs(shift_pred - shift_bnd) < 1e-6,
    f"{shift_pred:.9f} vs {shift_bnd:.9f}")

do_inp = MODE == "REAL"
E_G1 = errors(SPEC_G1, g1, do_inputs=do_inp)
P_G1, a23 = g1["P"], g1["abar"]
zY = (P_G1 - A0INV) / E_G1["sigma_Y"]
zA = (FE["aU"] - a23) / E_G1["sigma_A"]
delta_route = E_G1["sigma_Y"] / A0INV
loops = {}
for lab, o in (("1-loop", L.Opts(gauge_loops=1, yuk_loops=1)), ("2-loop", L.Opts(gauge_loops=2, yuk_loops=2)),
               ("3-loop", L.Opts(gauge_loops=3, yuk_loops=3)), ("4-loop (Y1)", OPTS)):
    loops[lab] = solve(SPEC_G1, o=o, guess=g1["aYMt"])["P"]
print("\nG1 route error (frozen formulas):")
if not do_inp:
    print("   (input re-solves skipped in MUTATE modes, frozen section 9: sigma_in = 0 here)")
for key, lab, _p, _m in ITEMS:
    if key in E_G1["items"]:
        it = E_G1["items"][key]
        print(f"   {lab:28s}: dP {it['P']:+.5f}   d a_23 {it['abar']:+.5f}")
print(f"   sigma_map {SIG_MAP:.4f}, Thomson {THOMSON:.4f}, sigma_in {E_G1['sigma_in']:.4f}, sigma_thr,Y {E_G1['sigma_thr_Y']:.4f} "
      f"(P at 2 mu_23 {E_G1['P_fac2']:.4f}, at mu_23/2 {E_G1['P_fachalf']:.4f}), sigma_bnd,Y {E_G1['sigma_bnd_Y']:.4f} (eps {E_G1['eps_bnd']:.4f}), "
      f"sigma_loop {E_G1['sigma_loop']:.4f}  ->  sigma_Y = {E_G1['sigma_Y']:.4f}")
print(f"   leg A: sigma_in,A {E_G1['sigma_in_A']:.4f}, Y1 {E_G1['sigma_Y1_A']:.4f}, thr {E_G1['sigma_thr_A']:.4f}, bnd {E_G1['sigma_bnd_A']:.4f}  ->  sigma_A = {E_G1['sigma_A']:.4f}")
print(f"   P by loop order: " + ", ".join(f"{k} {v:.4f}" for k, v in loops.items()))
print(f"   pre-flight: delta_route = sigma_Y/137.036 = {delta_route:.5f} ({'diagnostic' if delta_route <= 1 else 'NOT DIAGNOSTIC'})")
corr = E_G1["cov_in_YA"] / (E_G1["sigma_in"] * E_G1["sigma_in_A"]) if do_inp and E_G1["sigma_in"] > 0 and E_G1["sigma_in_A"] > 0 else float("nan")
chi2 = zY ** 2 + zA ** 2
aY_meas23 = float(A23_M[0])
zUV = (FE["aYb"] - aY_meas23) / E_G1["sigma_Y"]

# substitution test (G1)
print("\nsubstitution test (alpha x 1.01 in every contamination slot; identity would move P by 1.3568)")
lam_tree = P["Mh"] ** 2 / (2 * L.VEV ** 2)
d_lam_sub = 0.01 * (c_c["lam"] - lam_tree)
d_yt_sub = 0.01 * 0.02 * c_c["yt"]
d_g2_sub = 0.01 * (c_c["g2"] - 2 * P["MW"] / L.VEV)
G3CAL = L.g3_cal()
d_g3_sub = 0.01 * (G3CAL - 1.0)
alpha_diag = 1.0 / A0INV
lep2 = sum(alpha_diag / (2 * PI ** 2) * math.log(Mt_c / m) for nm, m, _ in RG.fermions(1) if nm in ("e", "mu", "tau"))
d_delta_sub = 0.01 * 4.0 * lep2
dgY_sub = c_c["gY"] * (math.sqrt(1.01) - 1.0)
dAY_ident = 4 * PI / (c_c["gY"] + dgY_sub) ** 2 - AY_T
SLOTS = [("g2", dict(dg2=d_g2_sub)), ("g3", dict(rel_g3=d_g3_sub)), ("lam", dict(dlam=d_lam_sub)), ("yt", dict(dyt=d_yt_sub))]
print(f"   slots: d g_2 {d_g2_sub:+.2e} (1% of NNLO - tree), rel d g_3 {d_g3_sub:+.2e} (1% of the SMDR calibration - 1), d lambda {d_lam_sub:+.2e}, "
      f"d y_t {d_yt_sub:+.2e}, Delta_t two-loop bound {d_delta_sub:.2e}; measured-g_Y slot (placements mu_12/mu_13 only) d g_Y {dgY_sub:+.2e} "
      f"(moves a_Y^meas(M_t) by {dAY_ident:+.4f})")


def substitution(spec, base, with_gY=False):
    g = base["aYMt"]
    parts = {"Delta_t": d_delta_sub}
    for nm, ip in SLOTS:
        parts[nm] = solve(spec, ip, guess=g)["P"] - base["P"]
    tot = sum(abs(vv) for vv in parts.values())
    res = dict(parts=parts, total=tot, frac=tot / IDENT)
    if with_gY:
        dP5 = solve(spec, dict(dgY=dgY_sub), guess=g)["P"] - base["P"]
        res.update(gY=dP5, frac_gY_vs_ident=dP5 / (-IDENT), frac_gY_vs_aYshift=dP5 / dAY_ident)
    return res


SUB_G1 = substitution(SPEC_G1, g1)
print(f"   G1: shifts {', '.join(f'{k} {vv:+.2e}' for k, vv in SUB_G1['parts'].items())}; total {SUB_G1['total']:.4f} = {SUB_G1['frac']:.3f} of an identity")

# ================================================================================================ E. reported configurations (K = 8 minus G1) and R1-R4
print("\n" + "=" * 132)
print("Reported configurations (same rules, not graded)")
print("=" * 132)
PLACES = [("mu_23", dict(place="mu23")), ("mu_12", dict(place="meas12")), ("mu_13", dict(place="meas13"))]
CONF = []
for fk in ("entropy", "char"):
    F = FUNCS[fk]
    for pl_name, pl_spec in PLACES + [("Lambda_G", dict(place="fixed", mu=F["LamG"]))]:
        CONF.append((fk, pl_name, dict(pl_spec, target="const", val=F["aYb"], aU=F["aU"])))
RES = {}
for fk, pl_name, spec in CONF:
    key = f"{fk}@{pl_name}"
    if key == "entropy@mu_23":
        r, E = g1, E_G1
    else:
        r = solve(spec, scan=True)
        if r["status"] == "none":
            RES[key] = dict(status="none", grade=grade([None], "none", True, 0.0), info=r["info"])
            print(f"   {key:18s}: no root -> {RES[key]['grade']}")
            continue
        E = errors(spec, r, do_inputs=do_inp)
    zy = (r["P"] - A0INV) / E["sigma_Y"]
    za = (FUNCS[fk]["aU"] - r["abar"]) / E["sigma_A"]
    ze = None if pl_name == "mu_23" else r["dE1"] / E["sigma_E1"]
    legs = [zy, za] + ([ze] if pl_name == "Lambda_G" else [])
    gr = grade(legs, r["status"], len(fails) == 0, E["sigma_Y"] / A0INV)
    sub = substitution(spec, r, with_gY=pl_name in ("mu_12", "mu_13")) if key != "entropy@mu_23" else SUB_G1
    RES[key] = dict(P=r["P"], aYMt=r["aYMt"], Lam=r["Lam"], mu23=r["mu23"], A_at_Lam=r["A"], abar=r["abar"], dE1=r["dE1"], aU=FUNCS[fk]["aU"],
                    ratio=r["abar"] / FUNCS[fk]["aU"], z_Y=zy, z_A=za, z_E1=ze, sigma_Y=E["sigma_Y"], sigma_A=E["sigma_A"], sigma_E1=E["sigma_E1"],
                    errors={k: vv for k, vv in E.items() if k != "items"}, items=E["items"], status=r["status"], scan=r["info"], grade=gr, substitution=sub,
                    graded=(key == "entropy@mu_23"))
    print(f"   {key:18s}: Lambda {r['Lam']:.4e}  P = {r['P']:8.4f} ({r['P'] - A0INV:+8.3f}, z_Y {zy:+8.1f}, sigma_Y {E['sigma_Y']:.3f})  "
          f"leg A: 1/alpha_U {FUNCS[fk]['aU']:.4f} vs (a_2+a_3)/2 {r['abar']:.4f} (x{r['abar'] / FUNCS[fk]['aU']:.2f}, z_A {za:+8.1f})"
          + (f"  E1: a_3 - a_2 {r['dE1']:+.3f} (z {ze:+.1f})" if ze is not None else "")
          + f"  subst {sub['frac']:.3f}" + (f" / g_Y slot {sub['frac_gY_vs_aYshift']:.3f} of the a_Y^meas shift" if "gY" in sub else "")
          + f"  -> {gr}{' [GRADED]' if key == 'entropy@mu_23' else ''}")

print("\nR1  the f_0-free ratio leg alone (a_Y(Lambda) = (C_Y/C_2) a_2(Lambda); the classic sin^2 theta_W = 3/8 run-down)")
R1 = {}
for pl_name, pl_spec in PLACES:
    spec = dict(pl_spec, target="ratio", r=float(RATIO_USED))
    r = solve(spec, scan=True)
    if r["status"] == "none":
        R1[pl_name] = dict(status="none")
        print(f"   {pl_name}: no root")
        continue
    E = errors(spec, r, do_inputs=do_inp)
    zy = (r["P"] - A0INV) / E["sigma_Y"]
    sub = substitution(spec, r, with_gY=pl_name in ("mu_12", "mu_13"))
    R1[pl_name] = dict(P=r["P"], Lam=r["Lam"], z_Y=zy, sigma_Y=E["sigma_Y"], substitution=sub, status=r["status"])
    print(f"   {pl_name}: Lambda {r['Lam']:.4e}  P = {r['P']:9.4f} ({r['P'] - A0INV:+8.3f}, z {zy:+7.1f}, sigma {E['sigma_Y']:.3f}); substitution {sub['frac']:.3f}"
          + (f", g_Y slot moves P by {sub['gY']:+.4f} = {sub['frac_gY_vs_aYshift']:.3f} of the a_Y^meas(M_t) shift (1 = identity)" if "gY" in sub else ""))

print("\nR2  full NCG run-down: all three couplings at g_U at Lambda = mu_23 (G1 trajectory), run down with Y1's betas")
R2 = {}
uL = np.array(g1["tr"].u(g1["mu23"]), dtype=float)
gU2 = 4 * PI / FE["aU"]
uL[0], uL[1], uL[2] = 5.0 / 3.0 * 4 * PI / FE["aYb"], gU2, gU2
for lab, o in (("1-loop", L.Opts(gauge_loops=1, yuk_loops=1)), ("2-loop", L.Opts(gauge_loops=2, yuk_loops=2)), ("4-loop", OPTS)):
    ev3 = lambda t, y: y[2] - 4 * PI
    ev2 = lambda t, y: y[1] - 4 * PI
    ev3.terminal = ev2.terminal = True
    sol = solve_ivp(lambda t, y: 2.0 * L.rhs_lnmu2(y, o), [math.log(g1["mu23"]), math.log(Mt_c)], list(uL), method="DOP853", rtol=1e-10, atol=1e-14,
                    events=[ev3, ev2])
    hit = None
    if len(sol.t_events[0]):
        hit = ("alpha_3 = 1", math.exp(sol.t_events[0][0]))
    if len(sol.t_events[1]) and (hit is None or math.exp(sol.t_events[1][0]) > hit[1]):
        hit = ("alpha_2 = 1", math.exp(sol.t_events[1][0]))
    R2[lab] = dict(event=None if hit is None else hit[0], mu=None if hit is None else hit[1], status=int(sol.status),
                   ratio_to_Lambda=None if hit is None else hit[1] / g1["mu23"])
    if hit is not None:
        msg = f"{hit[0]} at mu = {hit[1]:.3e} GeV (Lambda/{g1['mu23'] / hit[1]:.2f}), above M_t -> NO SOLUTION with a perturbative SM"
    elif sol.status != 0:
        msg = f"integration failed at mu = {math.exp(sol.t[-1]):.3e} GeV (status {sol.status}: {sol.message})"
        R2[lab]["mu"] = math.exp(sol.t[-1])
    else:
        msg = "reached M_t without alpha_2 or alpha_3 exceeding 1"
    print(f"   {lab}: {msg}")

print("\nR3  the upper end of the allowed range: Lambda = M_P")
R3 = {}
for fk in ("entropy", "char"):
    F = FUNCS[fk]
    r = solve(dict(place="fixed", mu=MP, target="const", val=F["aYb"], aU=F["aU"]), scan=True)
    R3[fk] = dict(P=r["P"], status=r["status"])
    print(f"   {F['label']}: P(Lambda = M_P) = {r['P']:.4f} ({r['P'] - A0INV:+.3f}); P rises with Lambda, so this is the largest value any Lambda <= M_P gives")

print("\nR4  tuned knobs (by construction, not predictions)")
f0_star = 3 * PI * a23 / (2 * float(CON["C2"]))
f0Y_star = 3 * PI * aY_meas23 / (2 * float(CON["C2"]) * float(RATIO_USED))
R4 = dict(f0_star_legA=f0_star, f0_star_legY=f0Y_star, mult_legA=3 * f0_star / FE["f0"], mult_legY=3 * f0Y_star / FE["f0"],
          Lambda_star_oneloop=MP * math.exp((float(tr_c.A(MP)[0]) - FE["aYb"]) / (41.0 / (12 * PI))))
print(f"   f_0 needed by leg A: {f0_star:.4f} ({f0_star / FE['f0']:.2f} x ln 2; fermion-multiplicity equivalent {R4['mult_legA']:.1f} generations)")
print(f"   f_0 needed by leg Y: {f0Y_star:.4f} ({f0Y_star / FE['f0']:.2f} x ln 2) -- different from leg A because the couplings do not unify")
print(f"   one-loop Lambda at which the entropy boundary would meet Y1's a_Y: {R4['Lambda_star_oneloop']:.2e} GeV (far past M_P; U(1) Landau region)")

# ================================================================================================ F. MUTATE move tests, grades, output
moves = {}
if MODE != "REAL":
    print("\nMUTATE move tests (reference = the unmutated boundary, computed in this run)")
    ref_spec = dict(place="mu23", target="const", val=FE["aYb_ref"], aU=FE["aU_ref"])
    ref = solve(ref_spec, guess=g1["aYMt"] + (FE["aYb_ref"] - FE["aYb"]))
    dP = P_G1 - ref["P"]
    moves["G1"] = dict(P_mut=P_G1, P_ref=ref["P"], dP=dP)
    print(f"   G1: P mutated {P_G1:.4f} vs reference {ref['P']:.4f}: moves by {dP:+.4f}")
    if MUT_RATIO:
        rr = solve(dict(place="mu23", target="ratio", r=float(RATIO_REF)), scan=True)
        dR1 = R1["mu_23"]["P"] - rr["P"]
        moves["R1_mu23"] = dict(P_mut=R1["mu_23"]["P"], P_ref=rr["P"], dP=dR1)
        print(f"   R1 at mu_23: mutated {R1['mu_23']['P']:.4f} vs reference {rr['P']:.4f}: moves by {dR1:+.4f}")
        move_ok = dP <= -0.5 and dR1 <= -10.0
    else:
        moves["aU_ratio"] = FE["aU"] / FE["aU_ref"]
        print(f"   leg A: 1/alpha_U mutated {FE['aU']:.4f} vs reference {FE['aU_ref']:.4f} (ratio {moves['aU_ratio']:.6f})")
        move_ok = dP <= -0.5 and abs(moves["aU_ratio"] - 0.5) < 1e-12
    moves["move_ok"] = move_ok
    print(f"   move tests: {'PASS' if move_ok else 'FAIL'}")

gates_ok = len(fails) == 0
G1_grade = grade([zY, zA], g1["status"], gates_ok, delta_route)
print("\n" + "=" * 132)
print(f"GATES: {'all PASS' if gates_ok else 'FAILED: ' + ', '.join(fails)}")
print(f"G1 (graded; entropy f_0 = ln 2, Lambda = mu_23 = {g1['mu23']:.4e} GeV):")
print(f"   leg A: 1/alpha_U = 8 ln2/pi = {FE['aU']:.5f} vs a_23 = {a23:.4f}  (x{a23 / FE['aU']:.2f}; z_A = {zA:+.1f}, sigma_A {E_G1['sigma_A']:.3f})")
print(f"   leg Y: 1/alpha(0) = {P_G1:.4f} vs 137.035999  (miss {P_G1 - A0INV:+.3f} = {100 * (P_G1 / A0INV - 1):+.2f}%; z_Y = {zY:+.1f}, sigma_Y {E_G1['sigma_Y']:.3f})")
print(f"   UV cross-check: a_Y(mu_23) boundary {FE['aYb']:.4f} vs Y1-central {aY_meas23:.4f}: z_UV = {zUV:+.1f} (same verdict: {abs(zUV) > 3})")
print(f"   joint chi^2 (2 dof) = {chi2:.1f}; input correlation of the legs {corr:+.3f}; substitution fraction {SUB_G1['frac']:.3f}")
print(f"   P_single (log-uniform 1/alpha in [10, 1000], leg Y window) = {p_single(P_G1 - A0INV):.3f} (not significant at any level)")
print(f"   GRADE: {G1_grade}" + ("" if gates_ok else "  (as frozen: a gate failed)"))
print(f"   N_mech: +1 (373 -> 374 if CFG906 has not landed; otherwise CFG906's count + 1)")
print("Nothing here derives alpha. alpha stays an INPUT; kappa = 1/2 stays FITTED; the SM mass sector stays walled.")
print("=" * 132)

OUT.update(G1=dict(P=P_G1, aYMt=g1["aYMt"], mu23=g1["mu23"], a_at_mu23=g1["A"], a23=a23, aU=FE["aU"], ratio=a23 / FE["aU"], z_Y=zY, z_A=zA, z_UV=zUV,
                   chi2=chi2, corr_in=corr, delta_route=delta_route, errors={k: vv for k, vv in E_G1.items() if k != "items"}, items=E_G1["items"],
                   loops=loops, substitution=SUB_G1, grade=G1_grade, scan=g1["info"], resid=g1["resid"], P_rtol13=g1b["P"], p_single=p_single(P_G1 - A0INV)),
           K7=dict(planted_P=pl["P"], planted_zA=zA_pl, classifier=[(n, g_, e) for n, g_, e in cc]), K9=dict(shift_pred=shift_pred, shift_bnd=shift_bnd),
           reported=RES, R1=R1, R2=R2, R3=R3, R4=R4, moves=moves, fails=fails, gates_ok=gates_ok,
           sub_inputs=dict(d_g2=d_g2_sub, d_g3_rel=d_g3_sub, d_lam=d_lam_sub, d_yt=d_yt_sub, d_delta=d_delta_sub, dgY=dgY_sub, dAY_ident=dAY_ident),
           Delta_t=DELTA_T, AY_T=AY_T, A2_T=A2_T, sigma_map=SIG_MAP, thomson=THOMSON, runtime_s=time.time() - T0)
fn = {"REAL": "cfg907_d07.json", "MUTATE": "cfg907_d07_MUTATE.json", "MUTATE_NORM": "cfg907_d07_MUTATE_NORM.json"}[MODE]
with open(os.path.join(HERE, fn), "w") as fh:
    json.dump(fl(OUT), fh, indent=1, default=str)
print(f"wrote {fn}; runtime {time.time() - T0:.1f} s")

if MODE == "REAL":
    sys.exit(0 if gates_ok else 1)
expected = {"MUTATE": {"K3e boundary ratio used = C_Y/C_2 derived = the recalled printed 5/3", "K3f sin^2 theta_W at Lambda = 3/8 (recalled printed)"},
            "MUTATE_NORM": {"K3d content traces over H_F: dim 96, C_3 = C_2 = 12, C_Y = 20 (and sum Y = sum Y^3 = 0 per generation)",
                            "K3g normalisation f_0 g^2/(2 pi^2) = 3/C derived = the recalled printed 1/4 (SU(3), SU(2); and (5/3) f_0 g'^2/(2 pi^2) = 1/4)",
                            "K6 2 f_2 Lambda^2 a_2|_R = -(96 f_2 Lambda^2/(24 pi^2)) R (the recalled CCM form, Majorana c neglected)"}}[MODE]
bite = set(fails) == expected and moves.get("move_ok", False)
print(f"MUTATE control: expected failures {'exactly reproduced' if set(fails) == expected else 'NOT reproduced: ' + str(sorted(set(fails) ^ expected))}; "
      f"moves {'PASS' if moves.get('move_ok') else 'FAIL'} -> exit {1 if bite else 3}")
sys.exit(1 if bite else 3)
