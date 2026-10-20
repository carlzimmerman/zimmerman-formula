#!/usr/bin/env python3
"""cfg896_preflight.py -- CFG896, alpha door D02 (frozen criteria: CFG896_PREREGISTRATION.md, commit cfc23448b).

A Higgs-sector boundary condition (lambda = 0, beta_lambda = 0, the one-loop Veltman condition, the multiple point principle) is read as an
equation for the hypercharge coupling g_Y(M_t); the joint pairs solve (g_Y, g_2) and would predict alpha(0) and M_W together.
  Stage 1: gates K1-K6 and the leverage pre-flight for all 13 pre-declared variants (S1-S7 singles, J1-J6 joint pairs).
  Stage 2: solving, ONLY for variants that pass the pre-flight.  K7 (planted known answers) exercises the pre-flight and both solvers.
Run:    OMP_NUM_THREADS=1 nice -n 10 python3 cfg896_preflight.py          (exit 0 iff every gate passes)
MUTATE: OMP_NUM_THREADS=1 nice -n 10 python3 cfg896_preflight.py MUTATE   (the hypercharge terms of C_c and C_d are sign-flipped; K3 and K4 must
        fail -> exit 1; exit 3 if the control does not bite)
Writes cfg896_preflight.json (real run) or cfg896_preflight_MUTATE.json.  Imports lane Y1 (y1_lib, y1_4_results.json) and lane B (rg_common:
lepton masses only) READ-ONLY.  No bytecode, one core, a few seconds.
Nothing here derives alpha.  Measured masses and alpha_s are labelled inputs; the SM mass sector stays walled; kappa and Z play no part.
"""
import sys
sys.dont_write_bytecode = True
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import json
import math
import numpy as np
from scipy.optimize import brentq, fsolve, minimize_scalar
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
AP = os.path.join(HERE, "..", "..", "real_research", "alpha_principle_2026")
Y1DIR = os.path.join(AP, "Y1_running_precision")
sys.path.insert(0, Y1DIR)
sys.path.insert(0, os.path.join(AP, "B_rg_asymptotic_safety"))
import y1_lib as L          # noqa: E402  (read-only)
import rg_common as RG      # noqa: E402  (read-only; lepton masses for the two-loop bound of the target transport)

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
P = L.PDG
A0INV = 137.035999177          # CODATA 2022: the TARGET only (and Delta_t, see section 3 of the pre-registration)
MP, MRED = 1.220890e19, 2.435e18
MUMAX = 3e21
K16 = 16 * PI ** 2
THRESH = 0.01 * A0INV          # 1.37: the frozen pre-flight threshold on sigma(1/alpha(0))
MW_THRESH = 0.80               # 1% of M_W: the joint's second leg
EPS = 2e-3                     # finite-difference step in ln g
fails = []


def chk(name, ok, info=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {info}")
    if not ok:
        fails.append(name)


print("=" * 132)
print("CFG896 alpha door D02: Higgs-sector boundary condition solved for g_Y (pre-flight, gates, controls) -- mode:",
      "MUTATE (hypercharge terms of C_c and C_d sign-flipped)" if MUT else "REAL RUN")
print("=" * 132)

# ------------------------------------------------------------------------------------------------ Y1's map error, from its JSON (margins from JSON)
with open(os.path.join(Y1DIR, "y1_4_results.json")) as fh:
    Y4 = json.load(fh)
_sxp = Y4["summary"]["X_P"]
SIG_MAP = _sxp["after_quad_pct"][3] / 100.0 * _sxp["central"][3]          # sigma(a_em) absolute at X_P, direct M_W (Y1: 8.8e-4 x 137.036)
THOMSON = Y4["summary"]["thomson_link_rel"] * A0INV                         # 0.008
print(f"Y1 error carried for the running + map: sigma_map = {SIG_MAP:.4f} (= {SIG_MAP / A0INV:.2e} x 137.036), Thomson link {THOMSON:.4f}")

# ------------------------------------------------------------------------------------------------ boundary at mu = M_t, trajectories, conditions
YB, YTAU = L.YB_MT_SMDR, L.YTAU_MT_SMDR
OPTS = L.L_default_opts()                   # gauge 4 loops, y_t / lambda 3 loops (Y1-central)
VELT = (6.0, 9.0 / 4.0, (-0.75 if MUT else 0.75), -6.0)      # coefficients of (lambda, g_2^2, g_Y^2, y_t^2) in C_d


def bnd(Mt=None, als=None, Mh=None, MW=None, dyt=0.0, dlam=0.0, rel_g3=0.0, dg2=0.0, dgY=0.0, gY=None, g2=None):
    """u0 at mu = M_t.  g_3 by Y1's QCD-only route (SMDR-calibrated), y_t, lambda (and g_2, g_Y unless given) from Buttazzo's interpolation."""
    Mt = P["Mt"] if Mt is None else Mt
    als = P["als"] if als is None else als
    Mh = P["Mh"] if Mh is None else Mh
    MW = P["MW"] if MW is None else MW
    g3 = L.g3_base(als, Mt) * (1 + rel_g3)
    _, c = L.buttazzo_boundary(Mt, Mh, MW, als, g3_override=g3, dg2=dg2, dgY=dgY, dyt=dyt, dlam=dlam)
    gYv = c["gY"] if gY is None else gY
    g2v = c["g2"] if g2 is None else g2
    u0 = L.u_from_gY_g2_g3(gYv, g2v, g3, c["yt"], YB, YTAU, c["lam"])
    return u0, Mt, dict(c, gY=gYv, g2=g2v, g3=g3)


def traj(u0, Mt, o=None):
    return L.Traj(u0, Mt, OPTS if o is None else o, mu_max=MUMAX)


def beta_cond(u, loops):
    """16 pi^2 d lambda / d ln mu as USED in condition C_c (Y1's yuk_lam_B is d/d ln mu^2, hence the factor 2)."""
    b = K16 * 2.0 * L.yuk_lam_B(u, loops)[3]
    if MUT:     # MUTATE: flip the sign of the hypercharge-containing one-loop gauge terms (27/400 g1^4 + 9/40 g1^2 g2^2, Y1 normalisation)
        b -= 2.0 * 2.0 * (27.0 * u[0] ** 2 / 400.0 + 9.0 * u[1] * u[0] / 40.0)
    return b


def cond_d(u):
    return VELT[0] * u[6] + VELT[1] * u[1] + VELT[2] * 0.6 * u[0] + VELT[3] * u[3]


LGRID = np.linspace(math.log(1e10), math.log(0.97 * MUMAX), 400)


def lam_min(tr):
    """(lambda_min, mu*) over mu in [1e10, 0.97 x 3e21]; nan if the minimum sits on an end of the range (no interior minimum)."""
    lam = tr.sol.sol(LGRID)[6]
    i = int(np.argmin(lam))
    if i == 0 or i == len(LGRID) - 1:
        return float("nan"), float("nan")
    r = minimize_scalar(lambda t: float(tr.sol.sol(t)[6]), bounds=(LGRID[i - 1], LGRID[i + 1]), method="bounded", options=dict(xatol=1e-10))
    return float(r.fun), math.exp(r.x)


CKEYS = ["a", "bP", "cP", "dP", "bR", "cR", "dR"]
PKEYS = ["aYP", "a2P"]                       # planted-control keys
OKEYS = CKEYS + PKEYS + ["invA", "MW"]


def conds(tr):
    out = {}
    for tag, M in (("P", MP), ("R", MRED)):
        u = tr.u(M)
        out["b" + tag] = float(u[6])
        out["c" + tag] = float(beta_cond(u, 3))
        out["d" + tag] = float(cond_d(u))
    out["a"], out["mustar"] = lam_min(tr)
    A = tr.A(MP)
    out["aYP"], out["a2P"] = float(A[0]), float(A[1])
    return out


# ------------------------------------------------------------------------------------------------ the measured point and the map to alpha(0)
u_c, Mt_c, c_c = bnd()
GY0, G20 = c_c["gY"], c_c["g2"]
tr_c = traj(u_c, Mt_c)
A_t = L.a_from_u(u_c)
AY_T, A2_T = float(A_t[0]), float(A_t[1])
DELTA_T = A0INV - (AY_T + A2_T)                 # Y1-central offset (pre-registration section 3)
DMW_DG2 = 0.014 / 0.00011                       # Buttazzo's g_2 formula inverted


def inv_alpha0(gY, g2):
    return 4 * PI / gY ** 2 + 4 * PI / g2 ** 2 + DELTA_T


def MW_from_g2(g2, Mt):
    return 80.384 + 0.014 * (g2 - 0.64779 - 0.00004 * (Mt - 173.34)) / 0.00011


print(f"\nmeasured point (Y1-central boundary at mu = M_t = {Mt_c} GeV): g_Y = {GY0:.6f}, g_2 = {G20:.6f}, g_3 = {c_c['g3']:.6f}, y_t = {c_c['yt']:.6f}, lambda = {c_c['lam']:.6f}")
print(f"   a_Y(M_t) = {AY_T:.4f}, a_2(M_t) = {A2_T:.4f}, a_em(M_t) = {AY_T + A2_T:.4f};  Delta_t = 137.035999177 - a_em(M_t) = {DELTA_T:.4f}  (target transport)")
print(f"   M_W from inverting Buttazzo's g_2 formula at the measured point: {MW_from_g2(G20, Mt_c):.4f} (input 80.3692)")


def evaluate(mode, sY=0.0, s2=0.0, o=None, **inp):
    """mode 'single': g_Y = GY0 e^sY fixed, g_2 from Buttazzo at the inputs (M_W measured).  'joint': g_Y = GY0 e^sY, g_2 = G20 e^s2 fixed (M_W
    not used; dg2 then shifts the M_W inversion).  'measured': g_Y and g_2 both from Buttazzo at the inputs (only for the z-test by-product)."""
    if mode == "measured":
        u0, Mt, c = bnd(**inp)
    else:
        gY = GY0 * math.exp(sY)
        g2 = None if mode == "single" else G20 * math.exp(s2)
        u0, Mt, c = bnd(gY=gY, g2=g2, **inp)
    tr = traj(u0, Mt, o)
    out = conds(tr)
    out["invA"] = inv_alpha0(c["gY"], c["g2"])
    out["MW"] = MW_from_g2(c["g2"] - (inp.get("dg2", 0.0) if mode == "joint" else 0.0), Mt)
    return out


def vec(d, keys):
    return np.array([d[k] for k in keys], dtype=float)


# ------------------------------------------------------------------------------------------------ K1, K2: reproduce Y1 exactly
print("\nK1  reproduce Y1's validated numbers exactly")
A_P = tr_c.A(MP)
y1_printed = dict(aY=55.2342, a2=49.2026, a3=52.9713, aem=104.4368)        # y1_4_budget.out, 'central (Y1-central)', X_P
mine = dict(aY=A_P[0], a2=A_P[1], a3=A_P[2], aem=A_P[0] + A_P[1])
for k in y1_printed:
    chk(f"K1(i) Y1-central {k}(X_P)", abs(mine[k] - y1_printed[k]) <= 1e-4, f"mine {mine[k]:.5f} printed {y1_printed[k]}")
uB, _ = L.buttazzo_boundary(173.34, 125.15, 80.384, 0.1184)
oB = L.Opts(gauge_loops=3, yuk_loops=3, qcd4=True)


def planck_B(Mt=173.34, Mh=125.15, MW=80.384, als=0.1184):
    u0, _ = L.buttazzo_boundary(Mt, Mh, MW, als)
    u = L.Traj(u0, Mt, oB, mu_max=MP * 1.001).u(MP)
    return dict(g1=math.sqrt(u[0]), g2=math.sqrt(u[1]), g3=math.sqrt(u[2]), yt=math.sqrt(u[3]), lam=u[6])


rB = planck_B()
y1_v2 = dict(g1=0.61537, g2=0.50546, g3=0.48731, yt=0.38248, lam=-0.01437)    # y1_2_validate_published.out, V2, mine(M_Pl = 1.22089e19)
for k in y1_v2:
    chk(f"K1(ii) Buttazzo-input like-for-like {k}(M_P)", abs(rB[k] - y1_v2[k]) <= 1e-5, f"mine {rB[k]:+.6f} printed {y1_v2[k]:+.5f}")
print("K2  lambda(M_P) sensitivities at Buttazzo's point (Y1 steps)")
sens = {}
for nm, kw, pr in (("M_t per GeV", dict(Mt=(174.34, 172.34)), -0.00649), ("alpha_3 per 0.0007", dict(als=(0.1191, 0.1177)), 0.00186),
                   ("M_h per GeV", dict(Mh=(126.15, 124.15)), 0.00281)):
    k, (up, dn) = list(kw.items())[0]
    s = (planck_B(**{k: up})["lam"] - planck_B(**{k: dn})["lam"]) / 2
    sens[nm] = s
    chk(f"K2 lambda(M_P) sensitivity {nm}", abs(s - pr) <= 2e-5, f"mine {s:+.5f} Y1 printed {pr:+.5f}")

# ------------------------------------------------------------------------------------------------ K3: Veltman coefficients from STr M^2
print("K3  Veltman coefficients from the field-dependent supertrace")
phi, g, gp, yt, lam, mu2 = sp.symbols("phi g gp y_t lambda mu2", real=True)
V = -mu2 * phi ** 2 / 2 + lam * phi ** 4 / 4             # V = lambda (H^dag H)^2 - mu^2 H^dag H, H^dag H = phi^2 / 2
mh2 = sp.diff(V, phi, 2)
mG2 = sp.simplify(sp.diff(V, phi) / phi)
STr = 6 * g ** 2 * phi ** 2 / 4 + 3 * (g ** 2 + gp ** 2) * phi ** 2 / 4 - 12 * yt ** 2 * phi ** 2 / 2 + 1 * mh2 + 3 * mG2
coef = sp.expand(STr).coeff(phi, 2)
derived = (sp.nsimplify(coef.coeff(lam)), sp.nsimplify(coef.coeff(g, 2)), sp.nsimplify(coef.coeff(gp, 2)), sp.nsimplify(coef.coeff(yt, 2)))
typed = tuple(sp.nsimplify(x) for x in VELT)
print(f"      STr M^2 phi^2-coefficient = {coef}  -> (lambda, g^2, g'^2, y_t^2) = {derived};  typed in C_d: {typed}")
chk("K3 C_d coefficients equal the supertrace derivation exactly", all(sp.simplify(a - b) == 0 for a, b in zip(derived, typed)))

# ------------------------------------------------------------------------------------------------ K4: beta_lambda in C_c
print("K4  beta_lambda used in C_c")
worst_run = 0.0
for M in (MP, MRED):
    u = tr_c.u(M)
    ref = K16 * 2.0 * L.yuk_lam_B(u, 3)[3]
    worst_run = max(worst_run, abs(beta_cond(u, 3) / ref - 1))
chk("K4(a) C_c's beta_lambda equals the beta_lambda that runs lambda (Y1, 3 loops) on the trajectory", worst_run <= 1e-12, f"worst relative difference {worst_run:.2e}")
rng = np.random.default_rng(896)
worst_tb = 0.0
for _ in range(20):
    u = np.array([rng.uniform(0.1, 0.6), rng.uniform(0.2, 0.5), rng.uniform(0.2, 1.4), rng.uniform(0.1, 1.0), 0.0, 0.0, rng.uniform(-0.05, 0.2)])
    g2s, gps, yt2, la = u[1], 0.6 * u[0], u[3], u[6]
    tb = 24 * la ** 2 - 6 * yt2 ** 2 + 3.0 / 8.0 * (2 * g2s ** 2 + (g2s + gps) ** 2) + la * (12 * yt2 - 9 * g2s - 3 * gps)
    worst_tb = max(worst_tb, abs(beta_cond(u, 1) / tb - 1))
chk("K4(b) one-loop part equals the textbook 16pi^2 beta_lambda (20 random points, y_b = y_tau = 0)", worst_tb <= 1e-12, f"worst relative difference {worst_tb:.2e}")

# ------------------------------------------------------------------------------------------------ the items and the Jacobians
SMT = math.hypot(P["sMt_exp"], P["sMt_th"])
_r2 = max(abs(0.64779 - 0.64754) / abs(0.64754 - 0.65294), 0.108 / PI)
SG2 = abs(0.64779 - 0.64754) * _r2                               # Y1 E5a
_rY = max(abs(0.35830 - 0.35940) / abs(0.35940 - 0.34972), 0.108 / PI)
SGY = abs(0.35830 - 0.35940) * _rY                               # Y1 E5a' (measured-point uncertainty only)
SMZ_GY = 0.35830 * P["MZ"] * P["sMZ"] / (P["MZ"] ** 2 - P["MW"] ** 2)   # Y1 E4b (measured-point uncertainty only)
SG3 = math.hypot(2.62e-5, 6.72e-5 / 2)                          # Y1 E5b
ITEMS = [  # key, label, plus, minus, in sigma_PF, in sigma_full, modes
    ("Mt_exp", "M_t +-0.29 (PDG exp; door set)", dict(Mt=P["Mt"] + P["sMt_exp"]), dict(Mt=P["Mt"] - P["sMt_exp"]), True, False, ("single", "joint")),
    ("Mt", "M_t +-0.42 (exp + non-pert.)", dict(Mt=P["Mt"] + SMT), dict(Mt=P["Mt"] - SMT), False, True, ("single", "joint", "measured")),
    ("als", "alpha_s +-0.0009", dict(als=P["als"] + P["sals"]), dict(als=P["als"] - P["sals"]), True, True, ("single", "joint", "measured")),
    ("Mh", "M_H +-0.09", dict(Mh=P["Mh"] + P["sMh"]), dict(Mh=P["Mh"] - P["sMh"]), True, True, ("single", "joint", "measured")),
    ("MW", "M_W +-0.0133 (singles: fixes g_2)", dict(MW=P["MW"] + P["sMW"]), dict(MW=P["MW"] - P["sMW"]), False, True, ("single", "joint", "measured")),
    ("ytm", "y_t matching +-0.0005", dict(dyt=0.0005), dict(dyt=-0.0005), False, True, ("single", "joint", "measured")),
    ("lamm", "lambda matching +-0.0003", dict(dlam=0.0003), dict(dlam=-0.0003), False, True, ("single", "joint", "measured")),
    ("g3m", "g_3 matching (Y1 E5b)", dict(rel_g3=SG3), dict(rel_g3=-SG3), False, True, ("single", "joint", "measured")),
    ("g2m", "g_2 matching (Y1 E5a)", dict(dg2=SG2), dict(dg2=-SG2), False, True, ("single", "joint", "measured")),
    ("gYm", "measured g_Y matching (Y1 E5a')", dict(dgY=SGY), dict(dgY=-SGY), False, False, ("measured",)),
    ("MZ", "measured g_Y from M_Z (Y1 E4b)", dict(dgY=SMZ_GY), dict(dgY=-SMZ_GY), False, False, ("measured",)),
]
ONE_SIDED = ["E7", "E6"]
LABEL = {k: lab for k, lab, *_ in ITEMS}
LABEL["E7"] = "y_t, lambda betas at 2 instead of 3 loops (Y1 E7)"
LABEL["E6"] = "gauge five-loop estimate D4^2/D3 (Y1 E6)"


def jacobian(mode, sY=0.0, s2=0.0):
    """Central differences of every output key w.r.t. every item (at fixed unknowns) and w.r.t. the unknowns."""
    base = evaluate(mode, sY, s2)
    out = dict(base=base, items={}, asym={}, unk={})
    for key, _lab, plus, minus, _pf, _full, modes in ITEMS:
        if mode not in modes:
            continue
        vp, vm = evaluate(mode, sY, s2, **plus), evaluate(mode, sY, s2, **minus)
        d, a = {}, {}
        for k in OKEYS:
            d[k] = (vp[k] - vm[k]) / 2
            a[k] = abs((vp[k] - base[k]) + (vm[k] - base[k])) / abs(d[k]) if abs(d[k]) > 1e-14 else 0.0
        out["items"][key], out["asym"][key] = d, a
    v4 = base
    v2 = evaluate(mode, sY, s2, o=L.Opts(gauge_loops=2, yuk_loops=3))
    v3 = evaluate(mode, sY, s2, o=L.Opts(gauge_loops=3, yuk_loops=3))
    vy2 = evaluate(mode, sY, s2, o=L.Opts(gauge_loops=4, yuk_loops=2))
    out["items"]["E7"] = {k: vy2[k] - v4[k] for k in OKEYS}
    e6 = {}
    for k in OKEYS:
        D4, D3 = v4[k] - v3[k], v3[k] - v2[k]
        e6[k] = D4 * abs(D4 / D3) if abs(D3) > 1e-14 else 0.0
    out["items"]["E6"] = e6
    if mode != "measured":
        for nm, which in (("sY", 0), ("s2", 1)):
            if nm == "s2" and mode == "single":
                continue
            res = {}
            for h in (EPS, EPS / 2):
                sh = [(h, 0.0), (0.0, h)][which]
                vp = evaluate(mode, sY + sh[0], s2 + sh[1])
                vm = evaluate(mode, sY - sh[0], s2 - sh[1])
                res[h] = ({k: (vp[k] - vm[k]) / (2 * h) for k in OKEYS},
                          {k: abs((vp[k] - base[k]) + (vm[k] - base[k])) / abs(vp[k] - vm[k]) * 2 if abs(vp[k] - vm[k]) > 1e-14 else 0.0 for k in OKEYS})
            out["unk"][nm] = dict(d=res[EPS][0], d_half=res[EPS / 2][0], asym=res[EPS][1])
    return out


print("\ncomputing the Jacobians (single, joint, measured modes) ...")
JAC = {m: jacobian(m) for m in ("single", "joint", "measured")}
B0 = JAC["single"]["base"]

# ------------------------------------------------------------------------------------------------ the variants and the propagation
VARIANTS = [
    ("S1", "single", ["a"], "lambda = beta_lambda = 0 at free mu* (lambda_min = 0)", "K2 (MPP)"),
    ("S2", "single", ["bP"], "lambda(M_P) = 0", "K1-conditional (AS) / K2"),
    ("S3", "single", ["cP"], "beta_lambda(M_P) = 0", "K2"),
    ("S4", "single", ["dP"], "Veltman at M_P", "K2"),
    ("S5", "single", ["bR"], "lambda(M_red) = 0", "K1-conditional (AS) / K2"),
    ("S6", "single", ["cR"], "beta_lambda(M_red) = 0", "K2"),
    ("S7", "single", ["dR"], "Veltman at M_red", "K2"),
    ("J1", "joint", ["bP", "cP"], "lambda = beta_lambda = 0 at M_P (door's AS pair)", "K2 (weaker leg)"),
    ("J2", "joint", ["bP", "dP"], "lambda = 0 and Veltman at M_P", "K2"),
    ("J3", "joint", ["cP", "dP"], "beta_lambda = 0 and Veltman at M_P", "K2"),
    ("J4", "joint", ["bR", "cR"], "lambda = beta_lambda = 0 at M_red", "K2"),
    ("J5", "joint", ["bR", "dR"], "lambda = 0 and Veltman at M_red", "K2"),
    ("J6", "joint", ["cR", "dR"], "beta_lambda = 0 and Veltman at M_red", "K2"),
]
DINV = {"sY": -2 * 4 * PI / GY0 ** 2, "s2": -2 * 4 * PI / G20 ** 2}       # d(1/alpha(0))/d ln g at the measured point
DMW = {"sY": 0.0, "s2": DMW_DG2 * G20}


def propagate(mode, keys, jac, gY=GY0, g2=G20):
    """Linear propagation (implicit-function theorem).  Returns per-item contributions to 1/alpha(0) (and M_W) and the sigmas."""
    dinv_u = {"sY": -2 * 4 * PI / gY ** 2, "s2": -2 * 4 * PI / g2 ** 2}
    dmw_u = {"sY": 0.0, "s2": DMW_DG2 * g2}
    unk = ["sY"] if mode == "single" else ["sY", "s2"]
    Jm = np.array([[jac["unk"][u]["d"][k] for u in unk] for k in keys])
    contrib = {}
    for key, d in jac["items"].items():
        dC = vec(d, keys)
        ds = -np.linalg.solve(Jm, dC)
        dinv = d["invA"] + sum(dinv_u[u] * ds[i] for i, u in enumerate(unk))
        dmw = d["MW"] + sum(dmw_u[u] * ds[i] for i, u in enumerate(unk))
        contrib[key] = (float(dinv), float(dmw), [float(x) for x in ds])
    pf = [k for k, _l, _p, _m, inpf, _f, _mo in ITEMS if inpf]
    full = [k for k, _l, _p, _m, _pf, infull, _mo in ITEMS if infull] + ONE_SIDED
    s_pf = math.sqrt(sum(contrib[k][0] ** 2 for k in pf if k in contrib))
    s_full = math.sqrt(sum(contrib[k][0] ** 2 for k in full if k in contrib) + SIG_MAP ** 2 + THOMSON ** 2)
    s_mw = math.sqrt(sum(contrib[k][1] ** 2 for k in full if k in contrib))
    cov_am = sum(contrib[k][0] * contrib[k][1] for k in full if k in contrib)
    return dict(Jm=Jm, contrib=contrib, s_pf=s_pf, s_full=s_full, s_mw=s_mw, cov_am=cov_am, full=full, pf=pf)


def zstat(keys):
    """Consistency of the principle with the measured world (measured mode; NOT an alpha result)."""
    jm = JAC["measured"]
    full = [k for k, _l, _p, _m, _pf, infull, mo in ITEMS if (infull or k in ("gYm", "MZ")) and "measured" in mo] + ONE_SIDED
    C = vec(jm["base"], keys)
    S = sum(np.outer(vec(jm["items"][k], keys), vec(jm["items"][k], keys)) for k in full)
    if len(keys) == 1:
        s = math.sqrt(S[0, 0])
        return float(C[0] / s), s
    return float(C @ np.linalg.solve(S, C)), [math.sqrt(S[0, 0]), math.sqrt(S[1, 1])]


# substitution numbers (pre-registration section 6.7): alpha scaled by 1.01 in every place of the contamination list
lam_tree = P["Mh"] ** 2 / (2 * L.VEV ** 2)
d_lam_sub = 0.01 * abs(c_c["lam"] - lam_tree)
d_yt_sub = 0.01 * 0.02 * c_c["yt"]
d_g2_sub = 0.01 * abs(c_c["g2"] - 2 * P["MW"] / L.VEV)
alpha_diag = 1.0 / A0INV
lep2 = sum(alpha_diag / (2 * PI ** 2) * math.log(Mt_c / m) for nm, m, _ in RG.fermions(1) if nm in ("e", "mu", "tau"))
d_delta_sub = 0.01 * 4.0 * lep2          # leptons + hadrons bounded by 3x the leptons
print(f"\nsubstitution inputs (alpha x 1.01): delta lambda(M_t) {d_lam_sub:.2e} (1% of NNLO - tree {c_c['lam'] - lam_tree:+.5f}); delta y_t {d_yt_sub:.2e};"
      f" delta g_2 {d_g2_sub:.2e} (1% of NNLO - tree {c_c['g2'] - 2 * P['MW'] / L.VEV:+.5f}); two-loop QED part of Delta_t (leptons) {lep2:.5f} -> delta Delta_t <= {d_delta_sub:.2e}")


def substitution(mode, pr):
    c = pr["contrib"]
    s = abs(c["lamm"][0]) * d_lam_sub / 0.0003 + abs(c["ytm"][0]) * d_yt_sub / 0.0005 + d_delta_sub
    if mode == "single":
        s += abs(c["g2m"][0]) * d_g2_sub / SG2
    return s


# ------------------------------------------------------------------------------------------------ K5 finite differences
print("\nK5  finite differences: linearity of the items, linearity and step stability of the unknown-derivatives")
bad_lin = []
for mode in ("single", "joint", "measured"):
    jac = JAC[mode]
    for key, a in jac["asym"].items():
        for k in CKEYS + ["invA", "MW"]:
            d = jac["items"][key][k]
            if k in CKEYS:
                sC = math.sqrt(sum(jac["items"][kk][k] ** 2 for kk in jac["items"]))
                significant = sC > 0 and abs(d) >= 0.01 * sC
            else:
                significant = abs(d) >= 1e-4
            if significant and a[k] >= 0.05:
                bad_lin.append((mode, key, k, a[k]))
    for nm, u in jac["unk"].items():
        for k in CKEYS + PKEYS + ["invA", "MW"]:
            d, dh = u["d"][k], u["d_half"][k]
            if abs(d) < 1e-12 or k in ("invA", "MW"):
                continue
            if abs(dh / d - 1) > 0.02 or u["asym"][k] >= 0.05:
                bad_lin.append((mode, nm, k, abs(dh / d - 1), u["asym"][k]))
chk("K5 every significant derivative is linear (asymmetry < 5%) and step-stable (eps vs eps/2 within 2%)", not bad_lin, f"violations: {bad_lin[:6]}")

# ------------------------------------------------------------------------------------------------ K6: M_t moved by 5 sigma
print("K6  M_t + 5 x 0.42 GeV: condition values move by 5 x their linear derivative (within 15%)")
v5 = evaluate("single", Mt=P["Mt"] + 5 * SMT)
worst6 = []
for k in CKEYS:
    pred = 5 * JAC["single"]["items"]["Mt"][k]
    got = v5[k] - B0[k]
    worst6.append((k, got / pred if abs(pred) > 0 else float("nan")))
    print(f"      {k:3s}: linear 5-sigma prediction {pred:+.5e}, actual {got:+.5e}, ratio {got / pred:.4f}")
chk("K6 every condition moves as the linear derivative predicts within 15%", all(abs(r - 1) <= 0.15 for _, r in worst6))

# ------------------------------------------------------------------------------------------------ solvers (used by K7 and by stage 2)
GRID1 = np.exp(np.linspace(math.log(0.5), math.log(2.0), 41))


def safe_eval(mode, sY, s2=0.0):
    gY = GY0 * math.exp(sY)
    if 1.0 / gY ** 2 - (41.0 / 6.0) / (8 * PI ** 2) * math.log(MUMAX / Mt_c) < 0.1:      # one-loop: hypercharge Landau pole at or below ~3e21 GeV
        return None
    try:
        r = evaluate(mode, sY, s2)
    except Exception:
        return None
    if not all(np.isfinite([r[k] for k in OKEYS if k != "a"])):
        return None
    return r


def solve_single(fun):
    """fun(r) -> condition value.  Scan g_Y in [0.5, 2] x GY0 on 41 log points, refine sign changes with brentq."""
    vals = []
    for f in GRID1:
        r = safe_eval("single", math.log(f))
        vals.append(None if r is None or not np.isfinite(fun(r)) else fun(r))
    roots, excluded = [], sum(v is None for v in vals)
    for i in range(len(GRID1) - 1):
        a, b = vals[i], vals[i + 1]
        if a is None or b is None:
            continue
        if a == 0.0:
            roots.append(math.log(GRID1[i]))
        elif a * b < 0:
            g = lambda s: fun(safe_eval("single", s))
            roots.append(brentq(g, math.log(GRID1[i]), math.log(GRID1[i + 1]), xtol=1e-13))
    uniq = []
    for s in roots:
        if all(abs(s - t) > 1e-6 for t in uniq):
            uniq.append(s)
    return uniq, excluded


def solve_joint(fun):
    """fun(r) -> 2-vector.  fsolve from a 5 x 5 grid of starts in [0.6, 1.6]^2 x (GY0, G20)."""
    starts = np.linspace(0.6, 1.6, 5)
    roots, nfail = [], 0
    for fy in starts:
        for f2 in starts:
            def F(x):
                r = safe_eval("joint", x[0], x[1])
                return np.array([1e3, 1e3]) if r is None else np.array(fun(r))
            x, info, ier, _msg = fsolve(F, [math.log(fy), math.log(f2)], full_output=True, xtol=1e-12)
            if ier != 1 or np.max(np.abs(F(x))) > 1e-9:
                nfail += 1
                continue
            if all(np.max(np.abs(x - y)) > 1e-6 for y in roots):
                roots.append(x)
    return roots, nfail


# ------------------------------------------------------------------------------------------------ K7: planted known answers
print("\nK7  positive controls (planted known answers)")
aYP_c, a2P_c = B0["aYP"], B0["a2P"]
pr_p1 = propagate("single", ["aYP"], JAC["single"])
print(f"      planted single C = a_Y(M_P) - {aYP_c:.6f}: sigma_PF {pr_p1['s_pf']:.4f}, sigma_full {pr_p1['s_full']:.4f}")
chk("K7(i) planted single condition passes the pre-flight", pr_p1["s_full"] <= THRESH and pr_p1["s_pf"] <= THRESH)
r1, ex1 = solve_single(lambda r: r["aYP"] - aYP_c)
inv_p1 = [inv_alpha0(GY0 * math.exp(s), G20) for s in r1]
print(f"      solver: {len(r1)} root(s), {ex1} grid points excluded (Landau); 1/alpha(0) = {inv_p1}")
chk("K7(i) single solver recovers 1/alpha(0) = 137.035999177 within 1e-6 relative", len(r1) == 1 and abs(inv_p1[0] / A0INV - 1) <= 1e-6,
    f"{inv_p1[0] if inv_p1 else None}")
pr_p2 = propagate("joint", ["aYP", "a2P"], JAC["joint"])
print(f"      planted joint (a_Y, a_2)(M_P) = ({aYP_c:.6f}, {a2P_c:.6f}): sigma_PF {pr_p2['s_pf']:.4f}, sigma_full {pr_p2['s_full']:.4f}, sigma(M_W) {pr_p2['s_mw']:.4f}")
chk("K7(ii) planted joint pair passes the pre-flight", pr_p2["s_full"] <= THRESH and pr_p2["s_pf"] <= THRESH)
r2, nf2 = solve_joint(lambda r: [r["aYP"] - aYP_c, r["a2P"] - a2P_c])
sol2 = [(inv_alpha0(GY0 * math.exp(x[0]), G20 * math.exp(x[1])), MW_from_g2(G20 * math.exp(x[1]), Mt_c)) for x in r2]
print(f"      joint solver: {len(r2)} distinct root(s), {nf2} of 25 starts failed; (1/alpha(0), M_W) = {sol2}")
chk("K7(ii) joint solver recovers 1/alpha(0) within 1e-6 relative and M_W = 80.3692 within 1e-4 GeV",
    len(sol2) == 1 and abs(sol2[0][0] / A0INV - 1) <= 1e-6 and abs(sol2[0][1] - P["MW"]) <= 1e-4, f"{sol2}")

# ------------------------------------------------------------------------------------------------ the measured-point values and the door's leverages
print("\n" + "=" * 132)
print("THE MEASURED POINT (Y1-central inputs, g_Y and g_2 at their Y1-central values)")
print("=" * 132)
for tag, M in (("P", MP), ("R", MRED)):
    print(f"  mu = {M:.4e}: lambda = {B0['b' + tag]:+.6f}   16pi^2 beta_lambda = {B0['c' + tag]:+.6f} (beta_lambda = {B0['c' + tag] / K16:+.3e})   Veltman = {B0['d' + tag]:+.6f}")
print(f"  lambda_min = {B0['a']:+.6f} at mu* = {B0['mustar']:.4e} GeV")
du = JAC["single"]["unk"]["sY"]["d"]
print(f"\n  door's leverages at fixed measured m_H, m_t, alpha_s, M_W:  d lambda(M_P)/d ln g_Y = {du['bP']:+.5f} ;  d beta_lambda(M_P)/d ln g_Y = {du['cP'] / K16:+.4e}"
      f" (16pi^2 x: {du['cP']:+.5f}) ;  d Veltman(M_P)/d ln g_Y = {du['dP']:+.5f} ;  d lambda_min/d ln g_Y = {du['a']:+.5f}")
dj = JAC["joint"]["unk"]["s2"]["d"]
print(f"  and per ln g_2 (joint):  d lambda(M_P) {dj['bP']:+.5f} ;  16pi^2 d beta_lambda(M_P) {dj['cP']:+.5f} ;  d Veltman(M_P) {dj['dP']:+.5f}")
print(f"  map: d(1/alpha(0))/d ln g_Y = {DINV['sY']:.3f} ; d(1/alpha(0))/d ln g_2 = {DINV['s2']:.3f} ; d M_W/d ln g_2 = {DMW['s2']:.3f} GeV")

# ------------------------------------------------------------------------------------------------ the pre-flight
print("\n" + "=" * 132)
print(f"LEVERAGE PRE-FLIGHT (frozen rule: NOT DIAGNOSTIC and stop if sigma_PF > {THRESH:.2f} or sigma_full > {THRESH:.2f})")
print("=" * 132)
RES = {}
for vid, mode, keys, desc, kern in VARIANTS:
    jac = JAC[mode]
    rec = dict(mode=mode, keys=keys, desc=desc, kernel=kern, C_measured={k: B0[k] for k in keys})
    if any(not np.isfinite(B0[k]) for k in keys):
        rec.update(grade="NOT COMPLETED", reason="no interior minimum of lambda at the measured point")
        RES[vid] = rec
        print(f"\n{vid} [{kern}] {desc}: NOT COMPLETED (no interior minimum)")
        continue
    pr = propagate(mode, keys, jac)
    z = zstat(keys)
    sub = substitution(mode, pr)
    rec.update(sigma_PF=pr["s_pf"], sigma_full=pr["s_full"], leverage={k: {u: jac["unk"][u]["d"][k] for u in jac["unk"]} for k in keys},
               contrib={k: v[0] for k, v in pr["contrib"].items()}, substitution_shift=sub)
    if mode == "joint":
        Jn = pr["Jm"] / np.array(z[1])[:, None]
        rec.update(sigma_MW=pr["s_mw"], corr_alpha_MW=pr["cov_am"] / math.sqrt(max(pr["s_full"] ** 2 - SIG_MAP ** 2 - THOMSON ** 2, 1e-300)) / max(pr["s_mw"], 1e-300),
                   cond_J_sigma_units=float(np.linalg.cond(Jn)), chi2_measured=z[0], sigma_C=z[1], contrib_MW={k: v[1] for k, v in pr["contrib"].items()})
    else:
        rec.update(z_measured=z[0], sigma_C=z[1])
    passes = pr["s_pf"] <= THRESH and pr["s_full"] <= THRESH
    rec["preflight"] = "PASS" if passes else "FAIL"
    if not passes:
        rec["grade"] = "NOT DIAGNOSTIC"
    RES[vid] = rec
    top = sorted(((abs(v[0]), k) for k, v in pr["contrib"].items() if k in pr["full"]), reverse=True)[:4]
    print(f"\n{vid} [{kern}] {desc}")
    print(f"   C at the measured point: " + ", ".join(f"{k} = {B0[k]:+.5e}" for k in keys))
    print(f"   leverage dC/d ln g_Y: " + ", ".join(f"{k} {jac['unk']['sY']['d'][k]:+.5e}" for k in keys)
          + ("" if mode == "single" else ";  dC/d ln g_2: " + ", ".join(f"{k} {jac['unk']['s2']['d'][k]:+.5e}" for k in keys)))
    print(f"   sigma_PF(1/alpha(0)) = {pr['s_pf']:.3f}  [M_t(0.29) {abs(pr['contrib']['Mt_exp'][0]):.3f}, alpha_s {abs(pr['contrib']['als'][0]):.3f}, M_H {abs(pr['contrib']['Mh'][0]):.3f}]"
          f"   sigma_full = {pr['s_full']:.3f}  (largest: " + ", ".join(f"{LABEL[k].split(' (')[0]} {v:.3f}" for v, k in top) + ")")
    if mode == "joint":
        print(f"   sigma_full(M_W) = {pr['s_mw']:.3f} GeV ; corr(1/alpha, M_W) = {rec['corr_alpha_MW']:+.3f} ; cond(J) in sigma units = {rec['cond_J_sigma_units']:.3e}")
        print(f"   by-product (not an alpha result): chi^2 (2 dof) of the principle at the measured point = {z[0]:.2f}  (sigma_C = {z[1][0]:.3e}, {z[1][1]:.3e})")
    else:
        print(f"   by-product (not an alpha result): z of the principle at the measured point = {z[0]:+.2f}  (C = {B0[keys[0]]:+.4e} +- {z[1]:.3e})")
    print(f"   substitution (alpha x 1.01 in every contamination slot): would-be shift of 1/alpha(0) <= {sub:.4f} ({sub / (0.01 * A0INV):.2%} of an identity's 1.37)")
    print(f"   PRE-FLIGHT: {'PASS -> proceeds to solving' if passes else 'FAIL -> NOT DIAGNOSTIC (stop; no solving)'}")

# ------------------------------------------------------------------------------------------------ stage 2: solving (only variants that passed)
print("\n" + "=" * 132)
print("STAGE 2: SOLVING (only variants that passed the pre-flight)")
print("=" * 132)
passed = [vid for vid in RES if RES[vid].get("preflight") == "PASS"]
N_MECH_NEW = 359 + len(VARIANTS)
RHO_A, RHO_W = 1 / math.log(100.0), 1 / math.log(30.0)
if not passed:
    print("  none passed: nothing is solved, no value of alpha(0) is produced by any variant.")
for vid in passed:
    rec = RES[vid]
    mode, keys = rec["mode"], rec["keys"]
    if mode == "single":
        roots, ex = solve_single(lambda r: r[keys[0]])
        rec["roots"] = []
        for s in roots:
            jr = jacobian("single", s)
            pr = propagate("single", keys, jr, gY=GY0 * math.exp(s))
            inv = inv_alpha0(GY0 * math.exp(s), G20)
            rec["roots"].append(dict(sY=s, invA=inv, sigma=pr["s_full"], substitution=substitution("single", pr)))
        print(f"  {vid}: roots {rec['roots']} ({ex} grid points excluded)")
        if not roots:
            rec["grade"] = "KILLED"
            rec["reason"] = "no root in g_Y in [0.5, 2] x the measured value"
        elif len(roots) > 1 and max(r["invA"] for r in rec["roots"]) - min(r["invA"] for r in rec["roots"]) > min(r["sigma"] for r in rec["roots"]):
            rec["grade"] = "NOT DIAGNOSTIC"
            rec["reason"] = "several admissible roots"
        else:
            r0 = rec["roots"][0]
            miss = r0["invA"] - A0INV
            if abs(miss) > 2 * r0["sigma"]:
                rec["grade"] = "KILLED"
            else:
                Pfam = len(VARIANTS) * 360 * 2 * RHO_A * max(abs(miss), r0["sigma"]) / A0INV
                rec["P_family_B"] = Pfam
                rec["grade"] = "CONSISTENT (pending)" if r0["substitution"] <= 0.137 else "NOT DIAGNOSTIC"
    else:
        roots, nf = solve_joint(lambda r: [r[keys[0]], r[keys[1]]])
        rec["roots"] = []
        for x in roots:
            jr = jacobian("joint", x[0], x[1])
            pr = propagate("joint", keys, jr, gY=GY0 * math.exp(x[0]), g2=G20 * math.exp(x[1]))
            inv = inv_alpha0(GY0 * math.exp(x[0]), G20 * math.exp(x[1]))
            mw = MW_from_g2(G20 * math.exp(x[1]), Mt_c)
            cov = np.array([[pr["s_full"] ** 2, pr["cov_am"]], [pr["cov_am"], pr["s_mw"] ** 2 + P["sMW"] ** 2]])
            r = np.array([inv - A0INV, mw - P["MW"]])
            rec["roots"].append(dict(sY=float(x[0]), s2=float(x[1]), invA=inv, MW=mw, sigma=pr["s_full"], sigma_MW=pr["s_mw"], chi2=float(r @ np.linalg.solve(cov, r))))
        print(f"  {vid}: roots {rec['roots']} ({nf} of 25 starts failed)")
        if not roots:
            rec["grade"] = "KILLED"
            rec["reason"] = "no root from the 5 x 5 starts"
        elif len(roots) > 1:
            rec["grade"] = "NOT DIAGNOSTIC"
            rec["reason"] = "several admissible roots"
        else:
            rec["grade"] = "KILLED" if rec["roots"][0]["chi2"] > 6.18 else "CONSISTENT (pending)"

# ------------------------------------------------------------------------------------------------ disclosure: M_Z blindness of the g_2 matching (joints)
dg2dMZ = (L.threshold1_g2(Mt_c, Mt_c, P["Mh"], P["MW"], P["MZ"] + 0.5) - L.threshold1_g2(Mt_c, Mt_c, P["Mh"], P["MW"], P["MZ"] - 0.5)) / 1.0
dMZ_per_1pct_gY = 0.01 * P["MZ"] * (GY0 ** 2 / (GY0 ** 2 + G20 ** 2))
print(f"\nM_Z blindness of Buttazzo's g_2 formula (joint variants, reported): one-loop d g_2/d M_Z = {dg2dMZ:+.3e} per GeV; a 1% change of g_Y moves M_Z by"
      f" {dMZ_per_1pct_gY:.3f} GeV (tree), i.e. an M_W bias of {abs(dg2dMZ * dMZ_per_1pct_gY * DMW_DG2):.4f} GeV per 1% of g_Y")

# ------------------------------------------------------------------------------------------------ summary
print("\n" + "=" * 132)
print("SUMMARY (grades by ALPHA_CAMPAIGN_RULES.md section 5)")
print("=" * 132)
print(f"  {'ID':4s} {'variant':52s} {'kernel':26s} {'sigma_PF':>9s} {'sigma_full':>11s} {'sig(M_W)':>9s} {'z / chi2':>9s}  grade")
for vid, mode, keys, desc, kern in VARIANTS:
    r = RES[vid]
    zz = r.get("z_measured", r.get("chi2_measured", float("nan")))
    print(f"  {vid:4s} {desc:52s} {kern:26s} {r.get('sigma_PF', float('nan')):9.3f} {r.get('sigma_full', float('nan')):11.3f} {r.get('sigma_MW', float('nan')):9.3f} {zz:9.2f}  {r['grade']}")
print(f"\n  attempt counter: post-ledger alpha attempt #1; N_mech 359 -> {N_MECH_NEW} (all 13 pre-declared variants counted, rules section 3, conservative reading)")
print(f"  precision demanded campaign-wide (single coupling): reading (A) {1e-3 / (N_MECH_NEW * 2 * RHO_A):.2e}, reading (B, stricter, applies) {1e-3 / (13 * 360 * 2 * RHO_A):.2e}")
print("  gates: " + ("all passed" if not fails else f"FAILED: {fails}"))

out = dict(mode="MUTATE" if MUT else "REAL", prereg_commit="cfc23448b", inputs=dict(PDG=P, Mt_sigma_total=SMT), sigma_map=SIG_MAP, thomson=THOMSON,
           measured_point=dict(gY=GY0, g2=G20, g3=c_c["g3"], yt=c_c["yt"], lam=c_c["lam"], aY_t=AY_T, a2_t=A2_T, Delta_t=DELTA_T),
           conditions_measured={k: B0[k] for k in CKEYS + ["mustar"]},
           door_leverages=dict(dlamMP_dlngY=du["bP"], dbetalamMP_dlngY=du["cP"] / K16, dVeltMP_dlngY=du["dP"], dlammin_dlngY=du["a"]),
           map=dict(dinv_dlngY=DINV["sY"], dinv_dlng2=DINV["s2"], dMW_dlng2=DMW["s2"]),
           K2_sensitivities=sens, K6_ratios=dict(worst6), substitution_inputs=dict(d_lam=d_lam_sub, d_yt=d_yt_sub, d_g2=d_g2_sub, lep2loop=lep2, d_delta=d_delta_sub),
           planted=dict(single=dict(s_pf=pr_p1["s_pf"], s_full=pr_p1["s_full"], invA=inv_p1),
                        joint=dict(s_pf=pr_p2["s_pf"], s_full=pr_p2["s_full"], s_MW=pr_p2["s_mw"], sol=sol2)),
           variants=RES, N_mech_new=N_MECH_NEW, gates_failed=fails,
           MZ_blindness=dict(dg2_dMZ=dg2dMZ, dMZ_per_1pct_gY=dMZ_per_1pct_gY))


def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return clean(x.tolist())
    if isinstance(x, (np.floating, float)):
        return None if not np.isfinite(x) else float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    return x


with open(os.path.join(HERE, "cfg896_preflight_MUTATE.json" if MUT else "cfg896_preflight.json"), "w") as fh:
    json.dump(clean(out), fh, indent=1)

if MUT:
    bit = any(f.startswith("K3") for f in fails) and any(f.startswith("K4") for f in fails)
    print("\nMUTATE control:", "BITES (K3 and K4 failed as required) -> exit 1" if bit else "BROKEN (K3/K4 did not both fail) -> exit 3")
    sys.exit(1 if bit else 3)
sys.exit(0 if not fails else 1)
