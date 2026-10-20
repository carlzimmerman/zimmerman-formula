"""CFG901: alpha door D03, f_g evaluated with the record's own matter content (frozen criteria: CFG901_PREREGISTRATION.md, commit f1e4cb90d;
post-hoc amendments A1-A4 appended there, commit ced3bd06b, written after the first run (cfg901_d03_FIRSTRUN.out, NOT COMPLETED as frozen)).

Usage (from any directory; one core, about 3 minutes, < 300 MB):
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg901_d03.py                 real run          -> cfg901_d03.out/.json, exit 0 iff every gate passes
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg901_d03.py MUTATE_SIGN     matter traces x -1  -> K1, K2, K3, K6, K7(n_s = 1) must FAIL, exit 1
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg901_d03.py MUTATE_COUNT    3 Weyl nu_R counted as 3 Dirac -> C-DEF must FAIL, exit 1;
                                                                          L1/L2 (the prediction moves as expected) must PASS
Graded trial G1: content A = SM + 3 nu_R (N_S 4, N_D 24, N_V 12), CPR scheme (AS3 code), EH truncation, g_Y* at M_P, lane B one-loop downstream.
Reported (not graded): CPR-R^2, BMS-EH, BMS-EH+C^2+R^2 (AS4 code), EV-EH (lane B), two-loop and M_red systematics, bracket B1-B4, tuned content.
Lanes AS1-AS4 and lane B are imported read-only (bytecode writing disabled); none of their files is edited.
kappa and Z enter nowhere. The SM mass sector is walled: no mass enters or is derived. Not theory closed."""
import sys
sys.dont_write_bytecode = True
import os
import time
import json
import threading
import resource
import functools
from pathlib import Path

LIMIT = 900 * 1024 * 1024           # watchdog: abort above 900 MB peak RSS (macOS ru_maxrss is in bytes)


def _watchdog():
    while True:
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > LIMIT:
            print("WATCHDOG: peak RSS above 900 MB, aborting", flush=True)
            os._exit(3)
        time.sleep(0.3)


threading.Thread(target=_watchdog, daemon=True).start()
print = functools.partial(print, flush=True)

HERE = Path(__file__).resolve().parent
AP = HERE.parent.parent / "real_research" / "alpha_principle_2026"
for d in ("AS1_fg_r2_truncation", "AS2_fg_cpr_scheme", "AS3_fg_cpr_reanchored", "AS4_fg_weyl2"):
    p = str(AP / d)
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np                       # noqa: E402
import sympy as sp                       # noqa: E402
import scipy                             # noqa: E402
from scipy.optimize import fsolve        # noqa: E402
import as2_common as A2                  # noqa: E402  AS2/AS3 CPR machinery (unchanged)
import as3_gcpr as G3                    # noqa: E402  AS3 heat kernels (unchanged)
import as4_common as A4                  # noqa: E402  AS4 BMS machinery (unchanged)
import as4_systematics as H4             # noqa: E402  AS3/AS4 two-loop and reduced-Planck systematics (unchanged)

C1 = A2.C1
RG = C1.RG
MODE = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
assert MODE in ("NORMAL", "MUTATE_SIGN", "MUTATE_COUNT"), MODE
MSIGN = -1 if MODE == "MUTATE_SIGN" else 1
T0 = time.time()
TARGET = RG.ALPHA_INV0                  # 137.035999177, target only
NS, ND, NV = A2.NS, A2.ND, A2.NV
R = A2.R
Q = sp.Rational

SM = (Q(4), Q(45, 2), Q(12))
CONTENT_A = (Q(4), Q(24), Q(12))                       # SM + 3 right-handed Weyl neutrinos (FS11, conditional)
GRADED = (Q(4), Q(45, 2) + 3, Q(12)) if MODE == "MUTATE_COUNT" else CONTENT_A
BRACKET = {"B1 (+1 real scalar)": (Q(5), Q(24), Q(12)), "B2 (+2 real scalars)": (Q(6), Q(24), Q(12)),
           "B3 (+1 gauge vector)": (Q(4), Q(24), Q(13)), "B4 (+1 vector +1 scalar, Proca)": (Q(5), Q(24), Q(13))}
N_MECH_BEFORE = 372

fails = []
results = {"mode": MODE, "prereg_commit": "f1e4cb90d", "amendments_commit": "ced3bd06b", "content_A": [float(x) for x in CONTENT_A],
           "graded_content_used": [float(x) for x in GRADED]}


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)
    return ok


def stamp(label):
    print(f"  ... {label}: t = {time.time() - T0:.1f} s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6:.0f} MB")


def cstr(c):
    return f"(N_S, N_D, N_V) = ({float(c[0]):g}, {float(c[1]):g}, {float(c[2]):g})"


def half_unit(printed):
    """Half a unit of the last printed digit of a decimal string."""
    s = printed.lstrip("-")
    dec = len(s.split(".")[1]) if "." in s else 0
    return 0.5 * 10.0**(-dec)


def close_printed(val, printed):
    if val is None or not np.isfinite(val):
        return False
    return abs(val - float(printed)) <= half_unit(printed) * (1 + 1e-9)


def fmt(v, spec=".6f"):
    return "None" if v is None else format(v, spec)


# ------------------------------------------------------------------ section 7: frozen route error (record numbers, SM content)
print(f"MODE: {MODE}")
print(f"python {sys.version.split()[0]}, numpy {np.__version__}, sympy {sp.__version__}, scipy {scipy.__version__}")
REC = dict(two_loop=96.07582 - 95.57847,          # AS3 EH two-loop shift (AS3_REPORT systematics table)
           m_red=abs(93.82509 - 95.57847),        # AS3 EH start at M_red
           y1=8.8e-4 * 137.036,                   # Y1 running error (CFG895 rules section 1.3)
           scheme=abs(92.914 - 95.57847),         # EV (lane B C5) vs CPR EH (AS3)
           trunc=abs(91.04527 - 96.37265))        # BMS HD in-domain root vs BMS EH (AS4; root inadmissible -> conservative)
SIGMA_ROUTE = float(np.sqrt(sum(v**2 for v in REC.values())))
SIGMA_ADM = float(np.sqrt(sum(v**2 for k, v in REC.items() if k != "trunc") + (95.57847 - 95.26961)**2))
print("\n(0) PRE-FLIGHT (rules section 1.6), frozen route error from record numbers")
for k, v in REC.items():
    print(f"   {k:9s} {v:.5f}")
print(f"   sigma_route = {SIGMA_ROUTE:.4f} (frozen 6.230); admissible-only variant {SIGMA_ADM:.4f} (frozen 3.245)")
chk("PF-sigma", abs(SIGMA_ROUTE - 6.230) < 5e-4 and abs(SIGMA_ADM - 3.245) < 5e-4, "sigma_route and the admissible-only variant equal the frozen values")
delta_route = SIGMA_ROUTE / TARGET
print(f"   delta_route = sigma_route / 137.036 = {delta_route:.4f}  ->  {'diagnostic (< 1)' if delta_route < 1 else 'NOT DIAGNOSTIC (> 1)'};"
      f" 1% would need sigma <= 1.37: {'reachable' if SIGMA_ROUTE <= 1.37 else 'NOT reachable, ceiling CONSISTENT'}")
results["preflight"] = dict(components=REC, sigma_route=SIGMA_ROUTE, sigma_admissible_only=SIGMA_ADM, delta_route=delta_route)


# ------------------------------------------------------------------ f_g closed forms (AS3 / AS4 reports), downstream, classifier
F0, F1, dF1 = A2.F0, A2.F1, A2.dF1
FG_CPR_GENERAL = -5 * (8 * F0 + 4 * F1 - dF1) / (1152 * sp.pi**2 * (F0 + F1)**2)        # AS3 printed (as3_trial.out)
u0, u1, u1d, u3, u3d = A4.U0, A4.U1, A4.U1d, A4.U3, A4.U3d
FG_BMS_GENERAL = -(40 * u0 + 20 * u1 - 5 * u1d + 14 * u3d) / (1152 * sp.pi**2 * (u0 + u1 - 2 * u3)**2)   # AS4 printed (as4_trial.out)


def fg_cpr(gt):
    f0, f1 = float(gt[0]), float(gt[1])
    return -5 * (8 * f0 + 4 * f1 - 2 * f1) / (1152 * np.pi**2 * (f0 + f1)**2)


def fg_bms(gt):
    a0, a1 = float(gt[0]), float(gt[1])
    a3 = float(gt[3]) if len(gt) > 3 else 0.0
    return -(40 * a0 + 20 * a1 - 5 * (2 * a1) + 14 * 0.0) / (1152 * np.pi**2 * (a0 + a1 - 2 * a3)**2)


def fg_ev(G, L):
    return G * (1 - 4 * L) / (4 * np.pi * (1 - 2 * L)**2)      # lane B b3_forced_vs_required.py, EV f_g line (retyped; gate K3)


def P_of(fg):
    return C1.downstream_P(fg) if fg is not None and fg > 0 else None


def grade_value(Pv, sigma=SIGMA_ROUTE):
    z = (Pv - TARGET) / sigma
    return ("KILLED" if abs(z) > 3 else "CONSISTENT"), z


def select(rows):
    adm = [r for r in rows if r["adm"]]
    if len(adm) == 0:
        return "NOT DIAGNOSTIC (no admissible root)", None
    if len(adm) > 1:
        return "NOT DIAGNOSTIC (several admissible roots)", None
    if adm[0]["fg"] is None or adm[0]["fg"] <= 0:
        return "NOT DIAGNOSTIC (f_g <= 0: no IR-attractive g_Y*)", None
    return "FP", adm[0]


def p_single(miss):
    m = abs(miss)
    lo = max(TARGET - m, 10.0)
    hi = min(TARGET + m, 1000.0)
    return float(np.log(hi / lo) / np.log(100.0))


# ------------------------------------------------------------------ CPR machinery (AS3)
print("\n(1) BUILDING THE FLOWS (AS3 CPR f(R); AS4 BMS; lane B EV)")
HK3 = G3.heat_kernels()
XM_SYM, XM_PARTS = A2.X_matter(HK3)            # symbolic in N_S, N_D, N_V
XG1 = A2.X_gravity(HK3, with_eta=True, order_f=1)
XG2 = A2.X_gravity(HK3, with_eta=True, order_f=2)
stamp("CPR traces")


def cpr_rows(c, n):
    X = (XG1 if n == 1 else XG2) + MSIGN * sp.expand(XM_SYM.subs({NS: c[0], ND: c[1], NV: c[2]}))
    bet = A2.beta_system(X, n)
    roots, f, J = A2.find_roots(bet, n, grid=True)
    rows = []
    for r in roots:
        glb = A2.to_glb(r)
        dom, edge = A2.in_domain(glb)
        adm = A2.admissible(glb) and dom
        fg = fg_cpr(r)
        rows.append(dict(gt=[float(x) for x in r], glb=[float(x) for x in glb], dom=dom, edge=edge, adm=adm,
                         theta=A2.crit_exponents(J, r), fg=fg, P=(P_of(fg) if dom else None)))
    return rows


# symbolic-content CPR EH flow for the map, continuation and tuned content
X_SYM1 = XG1 + MSIGN * XM_SYM
BET_SYM = A2.beta_system(X_SYM1, 1)
_v = (A2.g0, A2.g1, NS, ND, NV)
f_cs = sp.lambdify(_v, BET_SYM, "numpy")
Jx_cs = sp.lambdify(_v, sp.Matrix(BET_SYM).jacobian([A2.g0, A2.g1]), "numpy")
JN_cs = sp.lambdify(_v, sp.Matrix(BET_SYM).jacobian([NS, ND, NV]), "numpy")
stamp("CPR symbolic-content betas")

# ------------------------------------------------------------------ BMS machinery (AS4)
HK4, okW = A4.heat_kernels_einstein()
SC4, DI4, VE4 = A4.matter_type_I(HK4)
TR_EH = A4.bms_traces(HK4, eh=True)
TR_HD = A4.bms_traces(HK4) if MODE == "NORMAL" else None
stamp("BMS traces")


def bms_mat(c):
    return {k: MSIGN * (c[0] * SC4[k] + c[1] * DI4[k] + c[2] * VE4[k]) for k in ("1", "R", "R2", "W")}


def bms_total(tr, c):
    tot = {}
    for part in (tr["S_2T"], tr["S_hh"], tr["S_1T"], tr["S_0"], bms_mat(c)):
        tot = A4.add(tot, part)
    return tot


def bms_rows(c, eh=True):
    fB = A4.beta_numeric(bms_total(TR_EH if eh else TR_HD, c), eh=eh)
    roots = A4.find_roots_num(fB, A4.grid_starts(2 if eh else 4))
    rows = []
    for r in roots:
        dom, edge = A4.in_domain(r)
        adm = A4.admissible(r) and dom
        fg = fg_bms(r)
        d2, d0 = A4.denominators(r)
        rows.append(dict(gt=[float(x) for x in r], glb=[float(x) for x in A4.to_glb(r)], dom=dom, edge=edge, adm=adm,
                         theta=A4.crit_num(fB, r), fg=fg, P=(P_of(fg) if dom else None), d2=float(d2), d0=float(d0)))
    return rows


TOT_SYM_EH = bms_total(TR_EH, (NS, ND, NV))
BET4_SYM = A4.beta_system(TOT_SYM_EH, eh=True)
_v4 = (u0, u1, NS, ND, NV)
f4_cs = sp.lambdify(_v4, BET4_SYM, "numpy")
Jx4_cs = sp.lambdify(_v4, sp.Matrix(BET4_SYM).jacobian([u0, u1]), "numpy")
JN4_cs = sp.lambdify(_v4, sp.Matrix(BET4_SYM).jacobian([NS, ND, NV]), "numpy")
stamp("BMS symbolic-content EH betas")

# ------------------------------------------------------------------ EV (lane B b3 module globals ND, NS, NV; by import)
B3 = C1.laneB_b3()


def ev_root(c, x0=(2.7, -3.8)):
    saved = (B3.ND, B3.NS, B3.NV)
    try:
        B3.ND, B3.NS, B3.NV = MSIGN * float(c[1]), MSIGN * float(c[0]), MSIGN * float(c[2])
        sol, info, ier, _ = fsolve(B3.betas, list(x0), xtol=1e-13, full_output=True)
        res = float(np.max(np.abs(B3.betas(sol))))
    finally:
        B3.ND, B3.NS, B3.NV = saved
    G_, L_ = float(sol[0]), float(sol[1])
    ok = ier == 1 and res < 1e-10
    adm = ok and G_ > 0 and (1 - 2 * L_) > 0
    fg = fg_ev(G_, L_)
    return dict(glb=[G_, L_], ok=ok, adm=adm, fg=fg, P=(P_of(fg) if adm else None), res=res)


def ev_root_cont(c, start_c=SM, steps=40):
    """EV root at content c by continuation from lane B's SM start (linear path in content space)."""
    x = (2.7, -3.8)
    r = None
    for s in np.linspace(0, 1, steps + 1):
        cc = tuple(float(a) + s * (float(b) - float(a)) for a, b in zip(start_c, c))
        r = ev_root(cc, x)
        if not r["ok"]:
            return r
        x = tuple(r["glb"])
    return r


# ------------------------------------------------------------------ continuation helpers (symbolic-content flows)
def root_cs(fun, jac, c, x0):
    cc = [float(v) for v in c]
    with np.errstate(all="ignore"):
        sol, info, ier, _ = fsolve(lambda v: np.array(fun(*v, *cc), dtype=float), np.array(x0, dtype=float),
                                   fprime=lambda v: np.array(jac(*v, *cc), dtype=float), full_output=True, xtol=1e-14, maxfev=400)
    res = float(np.max(np.abs(np.array(fun(*sol, *cc), dtype=float))))
    # Amendment A1: accept by residual (fsolve's flag 3 'xtol too small' at a residual of 1e-17 is converged); the AS2/AS4 grid searches keep ier == 1
    return sol, bool(np.all(np.isfinite(sol)) and res < 1e-12)


def continue_to(fun, jac, c_from, c_to, x0, dN=0.25):
    n = max(1, int(np.ceil(max(abs(float(b) - float(a)) for a, b in zip(c_from, c_to)) / dN)))
    x = np.array(x0, dtype=float)
    for s in np.linspace(0, 1, n + 1)[1:]:
        cc = tuple(float(a) + s * (float(b) - float(a)) for a, b in zip(c_from, c_to))
        x, ok = root_cs(fun, jac, cc, x)
        if not ok:
            return None
    return x


def ift_map(fun, jac, jacN, gt, c, fgfun):
    """Implicit-function derivatives at the root gt: d gt/dN = -Jx^-1 JN; d(g, lambda)/dN; d f_g/dN; dP/dN (one-loop chain: P = 41/(24 pi f_g) + const)."""
    cc = [float(v) for v in c]
    Jx = np.array(jac(*gt, *cc), dtype=float)
    JN = np.array(jacN(*gt, *cc), dtype=float)
    dx = -np.linalg.solve(Jx, JN)                         # 2 x 3
    g0v, g1v = gt
    T = np.array([[0.0, 1 / (16 * np.pi * g1v**2)], [-1 / (2 * g1v), g0v / (2 * g1v**2)]])   # d(g, lambda)/d(g~0, g~1)
    dglb = T @ dx
    h = 1e-7
    grad = np.array([(fgfun([g0v + h * abs(g0v), g1v]) - fgfun([g0v - h * abs(g0v), g1v])) / (2 * h * abs(g0v)),
                     (fgfun([g0v, g1v + h * abs(g1v)]) - fgfun([g0v, g1v - h * abs(g1v)])) / (2 * h * abs(g1v))])
    dfg = grad @ dx
    fgv = fgfun(gt)
    dP = -41 / (24 * np.pi * fgv**2) * dfg
    return dict(dglb=dglb, dfg=dfg, dP=dP)


# ================================================================== (2) GATES
print("\n(2) GATES")
# K1: AS3 with its own content
rows1_sm = cpr_rows(SM, 1)
r = [x for x in rows1_sm if x["adm"]]
ok = len(r) == 1 and close_printed(r[0]["glb"][0], "0.967159") and close_printed(r[0]["glb"][1], "-1.22293") \
    and close_printed(r[0]["fg"], "0.03883093") and close_printed(r[0]["P"], "95.57847")
chk("K1a AS3 CPR-EH (SM)", ok, (f"(g, lambda) = ({r[0]['glb'][0]:.7f}, {r[0]['glb'][1]:.6f}), f_g = {r[0]['fg']:.9f}, P = {fmt(r[0]['P'])}"
                               if r else f"{len(r)} admissible roots") + " vs (0.967159, -1.22293), 0.03883093, 95.57847")
P_SM_CPR = r[0]["P"] if len(r) == 1 and r[0]["P"] is not None else None
GT_SM_CPR = r[0]["gt"] if P_SM_CPR is not None else None
B2 = C1._exec_lane_b_script("b2_required_boundary.py")
if P_SM_CPR is not None:
    P2l, P1c = H4.two_loop_P(C1.gY_star_from_fg(r[0]["fg"]), B2)
    Pmr = H4.reduced_planck_P(r[0]["fg"])
    chk("K1b AS3 EH systematics (SM)", close_printed(P2l, "96.07582") and close_printed(Pmr, "93.82509"),
        f"two-loop {P2l:.6f}, M_red {Pmr:.6f} vs 96.07582, 93.82509")
rows2_sm = cpr_rows(SM, 2)
adm2 = [x for x in rows2_sm if x["adm"]]
exp2 = [(("1.006220", "-1.264456", "-0.0037661"), "0.03970669", "95.26961"), (("0.988607", "-1.297727", "0.0055494"), "0.03848093", "95.70584")]
m2 = 0
for (gp, fp, pp) in exp2:
    for x in adm2:
        if all(close_printed(x["glb"][i], gp[i]) for i in range(3)) and close_printed(x["fg"], fp) and close_printed(x["P"], pp):
            m2 += 1
chk("K1c AS3 CPR-R^2 (SM)", len(rows2_sm) == 4 and len(adm2) == 2 and m2 == 2,
    f"{len(rows2_sm)} real roots, {len(adm2)} admissible, {m2}/2 match AS3's printed roots, f_g and P")
stamp("K1")

# K2: AS4 with its own content
rows4_sm = bms_rows(SM, eh=True)
r4 = [x for x in rows4_sm if x["adm"]]
ok = len(r4) == 1 and close_printed(r4[0]["glb"][0], "0.864773") and close_printed(r4[0]["glb"][1], "-1.09006") \
    and close_printed(r4[0]["fg"], "0.03674694") and close_printed(r4[0]["P"], "96.37265")
chk("K2a AS4 BMS-EH (SM)", ok, (f"(g, lambda) = ({r4[0]['glb'][0]:.7f}, {r4[0]['glb'][1]:.6f}), f_g = {r4[0]['fg']:.9f}, P = {fmt(r4[0]['P'])}"
                               if r4 else f"{len(r4)} admissible roots") + " vs (0.864773, -1.09006), 0.03674694, 96.37265")
P_SM_BMS = r4[0]["P"] if len(r4) == 1 and r4[0]["P"] is not None else None
if P_SM_BMS is None:
    r4 = []
if r4:
    P2l, _ = H4.two_loop_P(C1.gY_star_from_fg(r4[0]["fg"]), B2)
    Pmr = H4.reduced_planck_P(r4[0]["fg"])
    chk("K2b AS4 EH systematics (SM)", close_printed(P2l, "96.86496") and close_printed(Pmr, "94.61927"),
        f"two-loop {P2l:.6f}, M_red {Pmr:.6f} vs 96.86496, 94.61927")
rowsHD_sm = None
if MODE == "NORMAL":
    rowsHD_sm = bms_rows(SM, eh=False)
    ind = [x for x in rowsHD_sm if x["dom"]]
    okr1 = len(ind) == 1 and all(close_printed(ind[0]["glb"][i], s) for i, s in enumerate(("0.863182", "-1.07628", "0.0210528", "-0.0072056"))) \
        and close_printed(ind[0]["fg"], "0.05741784") and close_printed(ind[0]["P"], "91.04527")
    r3 = [x for x in rowsHD_sm if (not x["dom"]) and x["fg"] > 0 and abs(x["glb"][0] + 2.62889) < 1e-4]
    okr3 = len(r3) == 1 and close_printed(C1.downstream_P(r3[0]["fg"]), "83.50578")
    chk("K2c AS4 BMS-HD (SM)", len(rowsHD_sm) == 3 and not any(x["adm"] for x in rowsHD_sm) and okr1 and okr3,
        f"{len(rowsHD_sm)} real roots, {sum(x['adm'] for x in rowsHD_sm)} admissible; in-domain root "
        + (f"{np.array2string(np.array(ind[0]['glb']), precision=7)}, f_g {ind[0]['fg']:.9f}, P {fmt(ind[0]['P'])}" if ind else "missing")
        + f"; root 3 P {C1.downstream_P(r3[0]['fg']) if r3 else float('nan'):.6f} (AS4: 91.04527, 83.50578)")
else:
    print("  [SKIP] K2c AS4 BMS-HD (SM): MUTATE runs skip the HD grid (pre-registered, section 9)")
stamp("K2")

# K3: lane B's EV value
ev_sm = ev_root(SM)
chk("K3 lane B EV (SM)", ev_sm["ok"] and abs(ev_sm["fg"] - B3.fg) < 1e-12 and ev_sm["P"] is not None and abs(ev_sm["P"] - B3.c5) < 1e-12
    and abs(ev_sm["P"] - 92.914) < 5e-4,
    f"f_g = {ev_sm['fg']:.10f} (b3 {B3.fg:.10f}), P = {ev_sm['P'] if ev_sm['P'] else float('nan'):.6f} (b3 c5 {B3.c5:.6f}; printed 92.914)")

# K4: downstream G0 (AS3)
g0ok = (abs(C1.downstream_P(B3.fg) - B3.c5) < 1e-9 and abs(C1.downstream_P(0.04795) / 92.914 - 1) < 1e-4
        and abs(C1.downstream_P(0.009805) / 137.036 - 1) < 1e-4 and abs(C1.downstream_P(B3.f_needed) - B3.c6) < 1e-9)
chk("K4 downstream G0", g0ok, f"P(0.04795) = {C1.downstream_P(0.04795):.4f}, P(0.009805) = {C1.downstream_P(0.009805):.4f}, "
    f"P(f_needed = {B3.f_needed:.6f}) = {C1.downstream_P(B3.f_needed):.6f}")

# K5: f_g closed forms
gS, lS = sp.symbols("g lambda_", real=True)
f1s = -1 / (16 * sp.pi * gS)
e_cpr = FG_CPR_GENERAL.subs({dF1: 2 * F1}).subs({F0: -2 * lS * f1s, F1: f1s})
ok5a = sp.simplify(e_cpr - 5 * gS * (1 - 8 * lS) / (36 * sp.pi * (1 - 2 * lS)**2)) == 0
e_bms = FG_BMS_GENERAL.subs({u3: 0, u3d: 0, u1d: 2 * u1})
ok5b = sp.simplify(e_bms - FG_CPR_GENERAL.subs({dF1: 2 * F1}).subs({F0: u0, F1: u1})) == 0
chk("K5 f_g closed forms", ok5a and ok5b, f"CPR general (d_t f' = 2 f') == 5 g (1 - 8 lambda)/(36 pi (1 - 2 lambda)^2): {ok5a}; BMS at u3 = 0 == CPR: {ok5b}")

# K6: matter traces
sc3, di3, ve3 = [MSIGN * p for p in XM_PARTS]
hand = {"scalar": (Q(1, 2), Q(1, 6)), "Dirac": (Q(-2), Q(-1, 6)), "vector": (Q(1), Q(-1, 6))}
okc = all(sp.nsimplify(sp.expand(e).coeff(R, 0)) == h[0] and sp.nsimplify(sp.expand(e).coeff(R, 1)) == h[1]
          for e, h in zip((sc3, di3, ve3), hand.values()))
okb = all(sp.nsimplify(MSIGN * d["1"]) == h[0] and sp.nsimplify(MSIGN * d["R"]) == h[1] for d, h in zip((SC4, DI4, VE4), hand.values()))
xsm = sp.expand(MSIGN * XM_SYM.subs({NS: SM[0], ND: SM[1], NV: SM[2]}))
oks3 = sp.simplify(xsm - (-31 - Q(61, 12) * R - Q(1751, 4320) * R**2)) == 0
msm = bms_mat(SM)
oks4 = all(sp.nsimplify(msm[k]) == v for k, v in {"1": -31, "R": Q(-61, 12), "R2": Q(-27, 80), "W": Q(-293, 720)}.items())
chk("K6 matter traces", okc and okb and oks3 and oks4,
    f"per field (R^0, R^1) = scalar (1/2, 1/6), Dirac (-2, -1/6), vector (1, -1/6): CPR {okc}, BMS {okb}; "
    f"SM totals: AS3 '-31 - 61R/12 - 1751R^2/4320' {oks3}, AS4 dict {oks4}")

# K7: published anchors of the content dependence
rows_pg = cpr_rows((0, 0, 0), 1)
okp = any(abs(x["gt"][0] / 0.005226 - 1) <= 1e-3 and np.iscomplexobj(x["theta"]) and abs(np.real(x["theta"][0]) / 2.382 - 1) <= 1e-3
          and abs(abs(np.imag(x["theta"][0])) / 2.168 - 1) <= 1e-3 for x in rows_pg)
chk("K7a CPR pure gravity (CPR Tables 1-2)", okp, "; ".join(f"g~0 = {x['gt'][0]:.7f}, theta = {np.array2string(x['theta'], precision=4)}" for x in rows_pg))


def bms_anchor(c, gp, lp, rp, ip):
    rows = bms_rows(c, eh=True)
    for x in rows:
        th = x["theta"]
        if close_printed(x["glb"][0], gp) and close_printed(x["glb"][1], lp) and np.iscomplexobj(th) \
                and close_printed(np.real(th[0]), rp) and close_printed(abs(np.imag(th[0])), ip):
            return True, rows
    return False, rows


okb0, rb0 = bms_anchor((0, 0, 0), "0.902", "0.109", "2.52", "1.78")
chk("K7b BMS-EH pure gravity (0.902, 0.109; 2.52 +- 1.78 i)", okb0,
    "; ".join(f"({x['glb'][0]:.5f}, {x['glb'][1]:.5f}), theta {np.array2string(x['theta'], precision=4)}" for x in rb0))
okb1, rb1 = bms_anchor((1, 0, 0), "0.860", "0.131", "2.58", "1.95")
chk("K7c BMS-EH n_s = 1 (0.860, 0.131; 2.58 +- 1.95 i)", okb1,
    "; ".join(f"({x['glb'][0]:.5f}, {x['glb'][1]:.5f}), theta {np.array2string(x['theta'], precision=4)}" for x in rb1))

# C-DEF: graded content = SM + 3 Weyl singlets
cdef = GRADED[0] == SM[0] and GRADED[2] == SM[2] and GRADED[1] - SM[1] == Q(3, 2)
chk("C-DEF graded content = SM + 3 Weyl singlets", cdef, f"graded {cstr(GRADED)}; Delta N_D = {float(GRADED[1] - SM[1]):g} (3 Weyl = 3/2 Dirac)")

# classifier controls and the planted positive control
cc = [grade_value(TARGET)[0] == "CONSISTENT", grade_value(95.57847)[0] == "KILLED",
      grade_value(TARGET + 3.01 * SIGMA_ROUTE)[0] == "KILLED", grade_value(TARGET - 3.01 * SIGMA_ROUTE)[0] == "KILLED",
      grade_value(TARGET + 2.99 * SIGMA_ROUTE)[0] == "CONSISTENT", grade_value(TARGET - 2.99 * SIGMA_ROUTE)[0] == "CONSISTENT",
      select([dict(adm=True, fg=0.04), dict(adm=True, fg=0.05)])[0].startswith("NOT DIAGNOSTIC"),
      select([dict(adm=False, fg=0.04)])[0].startswith("NOT DIAGNOSTIC"),
      select([dict(adm=True, fg=-0.01)])[0].startswith("NOT DIAGNOSTIC"),
      select([dict(adm=True, fg=0.04)])[0] == "FP"]
chk("CC classifier controls", all(cc), f"{sum(cc)}/{len(cc)} planted cases classified as frozen (NOT COMPLETED on a failed gate is the script's verdict rule)")
Ppl = C1.downstream_P(B3.f_needed)
gpl, zpl = grade_value(Ppl)
chk("PC planted answer f_g = f_needed", abs(Ppl - TARGET) < 1e-6 and gpl == "CONSISTENT" and abs(zpl) < 1e-6,
    f"P = {Ppl:.9f}, grade {gpl}, z = {zpl:.1e}")
GATES_OK = not fails
stamp("gates")

# ================================================================== (3) PRE-FLIGHT MAP (door's first computation; not graded)
print("\n(3) DIAGNOSTIC MAP d(g*, lambda*, f_g, P)/d(N_S, N_D, N_V) at SM content (implicit-function theorem; finite differences in K8)")
maps = {}
pred_shift = {}
dN_A = np.array([float(CONTENT_A[i] - SM[i]) for i in range(3)])
if GT_SM_CPR is not None:
    mp_ = ift_map(f_cs, Jx_cs, JN_cs, GT_SM_CPR, SM, fg_cpr)
    maps["CPR-EH"] = mp_
    pred_shift["CPR-EH"] = float(mp_["dP"] @ dN_A)
if r4:
    mp4 = ift_map(f4_cs, Jx4_cs, JN4_cs, r4[0]["gt"], SM, fg_bms)
    maps["BMS-EH"] = mp4
    pred_shift["BMS-EH"] = float(mp4["dP"] @ dN_A)
# EV: finite differences only (lane B's numeric betas)
ev_fd = {}
for i, (nm, h) in enumerate((("N_S", 1.0), ("N_D", 0.5), ("N_V", 1.0))):
    cp = [float(x) for x in SM]; cm = [float(x) for x in SM]
    cp[i] += h; cm[i] -= h
    rp_, rm_ = ev_root(cp, ev_sm["glb"]), ev_root(cm, ev_sm["glb"])
    ev_fd[nm] = dict(dglb=[(rp_["glb"][k] - rm_["glb"][k]) / (2 * h) for k in range(2)], dfg=(rp_["fg"] - rm_["fg"]) / (2 * h),
                     dP=((rp_["P"] - rm_["P"]) / (2 * h) if rp_["P"] and rm_["P"] else float("nan")))
maps["EV-EH"] = dict(dglb=np.array([ev_fd[k]["dglb"] for k in ("N_S", "N_D", "N_V")]).T,
                     dfg=np.array([ev_fd[k]["dfg"] for k in ("N_S", "N_D", "N_V")]),
                     dP=np.array([ev_fd[k]["dP"] for k in ("N_S", "N_D", "N_V")]))
pred_shift["EV-EH"] = float(maps["EV-EH"]["dP"] @ dN_A)
print("   scheme   | quantity     |   d/dN_S      |   d/dN_D      |   d/dN_V")
for sch, mp_ in maps.items():
    for lab, arr in (("g*", mp_["dglb"][0]), ("lambda*", mp_["dglb"][1]), ("f_g", mp_["dfg"]), ("P", mp_["dP"])):
        print(f"   {sch:8s} | {lab:12s} | {arr[0]:+.6e} | {arr[1]:+.6e} | {arr[2]:+.6e}")
for sch, v in pred_shift.items():
    print(f"   linear-map prediction for content A (Delta N_D = +3/2): Delta P = {v:+.5f}  [{sch}]")
results["map_at_SM"] = {k: dict(dglb=np.asarray(v["dglb"]).tolist(), dfg=np.asarray(v["dfg"]).tolist(), dP=np.asarray(v["dP"]).tolist())
                        for k, v in maps.items()}
results["map_linear_prediction_dP_A"] = pred_shift

# K8: map vs finite differences; continuation SM -> A equals the grid root
# Amendment A2: central differences at h and h/2; the Richardson value (4 D(h/2) - D(h))/3 must agree with the IFT derivative to
# max(1e-4 |IFT|, 1e-6); the raw error ratio (D(h) - IFT)/(D(h/2) - IFT) (about 4 for an O(h^2) error) is printed.
fd_ok = True
fd_txt = []
k8a_rows = []


def _fd(fun, jac, fgfun, x0, i, h):
    cp = [float(x) for x in SM]; cm = [float(x) for x in SM]
    cp[i] += h; cm[i] -= h
    xp, okp_ = root_cs(fun, jac, cp, x0)
    xm, okm_ = root_cs(fun, jac, cm, x0)
    return (C1.downstream_P(fgfun(xp)) - C1.downstream_P(fgfun(xm))) / (2 * h), (okp_ and okm_)


if GT_SM_CPR is not None:
    sets = [("CPR", f_cs, Jx_cs, fg_cpr, GT_SM_CPR, maps["CPR-EH"])]
    if r4:
        sets.append(("BMS", f4_cs, Jx4_cs, fg_bms, r4[0]["gt"], maps["BMS-EH"]))
    for sch, fun, jac, fgfun, x0, mp_ in sets:
        for i, (nm, h) in enumerate((("N_S", 1.0), ("N_D", 0.5), ("N_V", 1.0))):
            D1, ok1 = _fd(fun, jac, fgfun, x0, i, h)
            D2, ok2 = _fd(fun, jac, fgfun, x0, i, h / 2)
            DR = (4 * D2 - D1) / 3
            ift = mp_["dP"][i]
            tol = max(1e-4 * abs(ift), 1e-6)
            ratio = (D1 - ift) / (D2 - ift) if D2 != ift else float("inf")
            okk = ok1 and ok2 and abs(DR - ift) <= tol
            fd_ok = fd_ok and okk
            k8a_rows.append(dict(scheme=sch, N=nm, h=h, D_h=D1, D_h2=D2, richardson=DR, ift=ift, err_ratio=ratio))
            fd_txt.append(f"{sch} dP/d{nm}: IFT {ift:+.7f}, FD(h={h:g}) {D1:+.7f}, FD(h/2) {D2:+.7f}, Richardson {DR:+.7f} "
                          f"(|diff| {abs(DR - ift):.1e}, tol {tol:.1e}; error ratio {ratio:.2f})")
    results["K8a"] = k8a_rows
else:
    fd_ok = False
chk("K8a IFT map vs Richardson finite differences (A2)", fd_ok, "\n         " + "\n         ".join(fd_txt))
stamp("map")

# ================================================================== (4) GRADED TRIAL G1
print(f"\n(4) GRADED TRIAL G1: content {cstr(GRADED)} in CPR-EH (AS3 code), g_Y* at M_P, lane B one-loop downstream")
rowsA1 = cpr_rows(GRADED, 1)
for x in rowsA1:
    print(f"   root g~ = {np.array2string(np.array(x['gt']), precision=7)}  (g, lambda) = ({x['glb'][0]:.6f}, {x['glb'][1]:.6f})  in-domain {x['dom']}"
          f"  admissible {x['adm']}  theta = {np.array2string(x['theta'], precision=4)}  f_g = {x['fg']:.8f}"
          + (f"  P = {x['P']:.5f}" if x["P"] else ""))
selA, fpA = select(rowsA1)
cont = continue_to(f_cs, Jx_cs, SM, GRADED, GT_SM_CPR) if GT_SM_CPR is not None else None
okcont = fpA is not None and cont is not None and np.allclose(cont, fpA["gt"], rtol=1e-9, atol=1e-13)
chk("K8b continuation SM -> graded content lands on the grid root", okcont,
    f"continuation root {np.array2string(np.asarray(cont), precision=9) if cont is not None else 'failed'}")
GATES_OK = not fails
G1 = dict(selection=selA)
if fpA is None:
    g1_grade, zA = selA, None
    print(f"   selection: {selA}")
else:
    PA = fpA["P"]
    g1_grade, zA = grade_value(PA)
    gYs = C1.gY_star_from_fg(fpA["fg"])
    aYuv = 41 / (24 * np.pi * fpA["fg"])
    z_uv = (aYuv - 55.234) / SIGMA_ROUTE
    z_adm = (PA - TARGET) / SIGMA_ADM
    G1.update(gt=fpA["gt"], glb=fpA["glb"], theta=[str(t) for t in fpA["theta"]], f_g=fpA["fg"], gY_star=gYs, P=PA, z=zA, z_admissible_only=z_adm,
              f_g_over_required=fpA["fg"] / B3.f_needed, inv_alphaY_MP_pred=aYuv, z_uv=z_uv,
              dP_vs_SM=(PA - P_SM_CPR) if P_SM_CPR else None, theta_Y=-2 * fpA["fg"])
    print(f"   selection: unique admissible root; (g*, lambda*) = ({fpA['glb'][0]:.6f}, {fpA['glb'][1]:.6f}); f_g* = {fpA['fg']:.8f} "
          f"(= {fpA['fg'] / B3.f_needed:.4f} x the required {B3.f_needed:.6f}); theta_Y = -2 f_g = {-2 * fpA['fg']:.6f} (g_Y* IR-attractive)")
    print(f"   g_Y* = {gYs:.6f};  P = 1/alpha(0) = {PA:.5f};  P - P_SM(CPR-EH) = {fmt(PA - P_SM_CPR if P_SM_CPR else None, '+.5f')} (map predicted {pred_shift.get('CPR-EH', float('nan')):+.5f})")
    print(f"   z = (P - 137.036)/sigma_route = {zA:+.3f}  (admissible-only sigma: {z_adm:+.3f});  miss {PA - TARGET:+.4f} = {(PA / TARGET - 1) * 100:+.2f}%")
    print(f"   UV cross-check (no measured alpha): 1/alpha_Y*(M_P) = 41/(24 pi f_g) = {aYuv:.4f} vs Y1 target 55.234 -> z_UV = {z_uv:+.3f}"
          f" ({'same verdict' if (abs(z_uv) > 3) == (abs(zA) > 3) else 'DIFFERENT verdict (disclose)'})")
    # substitution test (rules section 4.2): alpha_2^-1 and Delta_0 scaled as if alpha were 1% larger
    a2s = B3.a2_mz / 1.01
    d0s = RG.DELTA_0_MZ / 1.01
    Psub = B3.aY_inv_at(RG.MZ, gYs) + a2s + d0s
    ident = TARGET / 1.01 - TARGET
    print(f"   substitution test: alpha_2^-1(M_Z) and Delta_0 scaled (alpha x 1.01): P {PA:.5f} -> {Psub:.5f} (shift {Psub - PA:+.4f});"
          f" an identity would shift {ident:+.4f}; fraction {abs((Psub - PA) / ident):.3f}; the gravitational piece 41/(24 pi f_g) shifts 0")
    G1.update(substitution_shift=Psub - PA, substitution_fraction=abs((Psub - PA) / ident))
    if g1_grade == "CONSISTENT":
        ps = p_single(PA - TARGET)
        G1.update(P_single=ps, P_family=1 - (1 - ps)**(N_MECH_BEFORE + 1))
        print(f"   P_single = {ps:.3e}; P_family (N_mech = {N_MECH_BEFORE + 1}) = {G1['P_family']:.3f}")
if not GATES_OK:
    g1_verdict = "NOT COMPLETED (gate failure: " + ", ".join(fails) + ")"
else:
    g1_verdict = g1_grade
print(f"   G1 GRADE: {g1_verdict}")
G1["grade"] = g1_verdict
results["G1"] = G1
stamp("G1")

# ================================================================== (5) REPORTED TRIALS (content A), systematics
print("\n(5) REPORTED, NOT GRADED: content A in the other schemes and truncations; systematics for every in-domain root with a value")
rep = {}


def report_rows(label, rows, kind):
    sel, fp = select(rows)
    print(f"   {label}: {len(rows)} real root(s); selection: {sel}")
    out = []
    for x in rows:
        line = (f"     {kind} {np.array2string(np.array(x['glb']), precision=6)}  in-domain {x['dom']}  admissible {x['adm']}"
                f"  theta {np.array2string(x['theta'], precision=4)}  f_g {x['fg']:.8f}")
        rec = dict(glb=x["glb"], dom=x["dom"], adm=x["adm"], fg=x["fg"], P=x["P"], theta=[str(t) for t in x["theta"]])
        if "d2" in x:
            line += f"  denominators spin-2 {x['d2']:+.5f} spin-0 {x['d0']:+.5f}"
        if x["P"] is not None:
            gY_ = C1.gY_star_from_fg(x["fg"])
            P2l_, _ = H4.two_loop_P(gY_, B2)
            Pmr_ = H4.reduced_planck_P(x["fg"])
            line += f"\n        P = {x['P']:.5f}  two-loop {P2l_:.5f}  M_red {Pmr_:.5f}" + ("" if x["adm"] else "  [not admissible: reported only]")
            rec.update(P_two_loop=P2l_, P_M_red=Pmr_)
            if x["adm"]:
                gr, z_ = grade_value(x["P"])
                line += f"  -> z {z_:+.3f} ({gr} by the frozen rule; not graded)"
                rec.update(z=z_, would_be=gr)
        print(line)
        out.append(rec)
    rep[label] = dict(selection=sel, roots=out)
    return sel, fp


report_rows("CPR-EH (G1 itself, systematics)", rowsA1, "(g, lambda)")
rowsA2 = cpr_rows(GRADED, 2)
selA2, _ = report_rows("CPR-R^2", rowsA2, "(g, lambda, b)")
rowsA4 = bms_rows(GRADED, eh=True)
selA4, fpA4 = report_rows("BMS-EH", rowsA4, "(g, lambda)")
if MODE == "NORMAL":
    rowsHDA = bms_rows(GRADED, eh=False)
    report_rows("BMS-EH+C^2+R^2", rowsHDA, "(g, lambda, g2, g3)")
else:
    print("   BMS-EH+C^2+R^2: skipped in MUTATE runs (pre-registered)")
evA = ev_root_cont(GRADED)
print(f"   EV-EH (lane B betas, flagged: not rebuildable from a published scheme, AS1): (G, L) = ({evA['glb'][0]:.6f}, {evA['glb'][1]:.6f}),"
      f" converged {evA['ok']}, admissible {evA['adm']}, f_g {evA['fg']:.8f}" + (f", P = {evA['P']:.5f} (lane B SM 92.914; shift {evA['P'] - B3.c5:+.5f})" if evA["P"] else ""))
if evA["P"]:
    gY_ = C1.gY_star_from_fg(evA["fg"])
    P2l_, _ = H4.two_loop_P(gY_, B2)
    print(f"        two-loop {P2l_:.5f}  M_red {H4.reduced_planck_P(evA['fg']):.5f};  z {(evA['P'] - TARGET) / SIGMA_ROUTE:+.3f} (not graded)")
rep["EV-EH"] = dict(glb=evA["glb"], adm=evA["adm"], fg=evA["fg"], P=evA["P"])
results["reported_content_A"] = rep
shifts = {"CPR-EH": (G1.get("P"), P_SM_CPR), "BMS-EH": (fpA4["P"] if fpA4 else None, P_SM_BMS), "EV-EH": (evA["P"], B3.c5)}
print("   content shift P_A - P_SM by scheme (EH):")
for k, (pa, ps) in shifts.items():
    if pa is not None and ps is not None:
        print(f"     {k}: {pa:.5f} - {ps:.5f} = {pa - ps:+.5f}  (linear map {pred_shift.get(k, float('nan')):+.5f}); |shift| < sigma_route: {abs(pa - ps) < SIGMA_ROUTE}")
results["content_shift_EH"] = {k: ((pa - ps) if pa is not None and ps is not None else None) for k, (pa, ps) in shifts.items()}
loophole_closed = all(v is not None and abs(v) < SIGMA_ROUTE for v in results["content_shift_EH"].values())
print(f"   content loophole closed at the computed truncations (|P_A - P_SM| < sigma_route in every EH scheme): {loophole_closed}")
results["content_loophole_closed"] = loophole_closed
stamp("reported")

# ================================================================== (6) LINEARITY: the prediction moves as expected (L1, L2)
print("\n(6) LINEARITY CHECKS L1/L2 (CPR-EH; the content-count MUTATE expectation)")
PA_true = None
xA = continue_to(f_cs, Jx_cs, SM, CONTENT_A, GT_SM_CPR) if GT_SM_CPR is not None else None
x3D = continue_to(f_cs, Jx_cs, SM, (SM[0], SM[1] + 3, SM[2]), GT_SM_CPR) if GT_SM_CPR is not None else None
xm3 = continue_to(f_cs, Jx_cs, SM, (SM[0], SM[1] - Q(3, 2), SM[2]), GT_SM_CPR) if GT_SM_CPR is not None else None
if xA is not None and x3D is not None and xm3 is not None and P_SM_CPR is not None:
    PA_true = C1.downstream_P(fg_cpr(xA))
    dA = PA_true - P_SM_CPR
    d3D = C1.downstream_P(fg_cpr(x3D)) - P_SM_CPR
    dm3 = C1.downstream_P(fg_cpr(xm3)) - P_SM_CPR
    chk("L1 (SM + 3 Dirac shift)/(content A shift) = 2 within 10%", abs(d3D / dA - 2) <= 0.2, f"{d3D:+.5f}/{dA:+.5f} = {d3D / dA:.4f}")
    chk("L2 (SM - 3 Weyl shift)/(content A shift) = -1 within 10%", abs(dm3 / dA + 1) <= 0.1, f"{dm3:+.5f}/{dA:+.5f} = {dm3 / dA:.4f}")
    results["linearity"] = dict(dP_A=dA, dP_SM_plus_3Dirac=d3D, dP_SM_minus_3Weyl=dm3)
else:
    chk("L1/L2 continuation", False, "continuation failed")

# ================================================================== (7) BRACKET (content B undefined): sensitivity only
print("\n(7) BRACKET B1-B4 (content B is NOT DEFINED by the record; sensitivity only, not graded, not counted)")
brk = {}
for lab, c in BRACKET.items():
    rc = cpr_rows(c, 1)
    s_c, f_c = select(rc)
    rb = bms_rows(c, eh=True)
    s_b, f_b = select(rb)
    ev_ = ev_root_cont(c)
    pc = f_c["P"] if f_c else None
    pb = f_b["P"] if f_b else None
    pe = ev_["P"]
    pa_c = G1.get("P")
    pa_b = fpA4["P"] if fpA4 else None
    print(f"   {lab:32s} CPR-EH {('%.5f' % pc) if pc else s_c}" + (f" ({pc - pa_c:+.5f} vs A)" if pc and pa_c else "")
          + f";  BMS-EH {('%.5f' % pb) if pb else s_b}" + (f" ({pb - pa_b:+.5f})" if pb and pa_b else "")
          + f";  EV-EH {('%.5f' % pe) if pe else 'no admissible root'}" + (f" ({pe - evA['P']:+.5f})" if pe and evA["P"] else ""))
    brk[lab] = dict(content=[float(x) for x in c], CPR_EH=pc, BMS_EH=pb, EV_EH=pe)
results["bracket"] = brk

# ================================================================== (8) TUNED CONTENT (by construction; a knob, not a prediction)


def guarded_step(x, Nfrom, Nto, i, c0):
    """Amendment A3: continue the CPR-EH root from count Nfrom to Nto in 2^k equal substeps (k = 0..10), accepting the first k for which
    every substep converges (A1 residual rule) and moves the root by at most 20% (relative norm)."""
    for k in range(11):
        xx = np.array(x, dtype=float)
        ok = True
        for Nsub in np.linspace(Nfrom, Nto, 2**k + 1)[1:]:
            cc = list(c0); cc[i] = Nsub
            xn, okn = root_cs(f_cs, Jx_cs, cc, xx)
            if not okn or np.linalg.norm(xn - xx) > 0.2 * np.linalg.norm(xx):
                ok = False
                break
            xx = xn
        if ok:
            return xx, True
    return np.array(x, dtype=float), False


print(f"\n(8) TUNED CONTENT (like lane B's C6): count at which P(CPR-EH) would reach 137.036, i.e. f_g = {B3.f_needed:.6f}; scanned upward to 1000")
tuned = {}
if GT_SM_CPR is not None:
    for i, nm in enumerate(("N_S", "N_D", "N_V")):
        c0 = [float(x) for x in SM]
        x = np.array(GT_SM_CPR, dtype=float)
        fprev = fg_cpr(x)
        found = None
        last = c0[i]
        status = "not reached below 1000"
        grid = list(np.arange(c0[i] + 0.25, 200.0, 0.25)) + list(np.arange(200.0, 1000.0 + 1e-9, 2.0))
        for Nv in grid:
            cc = list(c0); cc[i] = Nv
            # Amendment A3: halve the step (up to 10 times) if the root moves by more than 20% in one (sub)step
            xn, okn = guarded_step(x, last, Nv, i, c0)
            glb = A2.to_glb(xn)
            if not okn or not A2.admissible(glb) or not A2.in_domain(glb)[0]:
                status = f"root lost or inadmissible at {nm} = {Nv:g} (last admissible {last:g}, f_g {fprev:.6f})"
                break
            fn = fg_cpr(xn)
            if (fprev - B3.f_needed) * (fn - B3.f_needed) <= 0:
                lo, hi, xl = last, Nv, x.copy()
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    cm_ = list(c0); cm_[i] = mid
                    xm_, okm = root_cs(f_cs, Jx_cs, cm_, xl)
                    if not okm:
                        break
                    if (fg_cpr(xm_) - B3.f_needed) * (fprev - B3.f_needed) > 0:
                        lo, xl = mid, xm_
                    else:
                        hi = mid
                found = 0.5 * (lo + hi)
                status = f"{nm}* = {found:.3f} (Delta {found - c0[i]:+.3f}); there (g, lambda) = ({A2.to_glb(xl)[0]:.4f}, {A2.to_glb(xl)[1]:.4f})"
                break
            x, fprev, last = xn, fn, Nv
        if found is None and status.startswith("not reached"):
            status += f" (f_g at {nm} = {last:g}: {fprev:.6f})"
        print(f"   {nm}: {status}")
        tuned[nm] = dict(found=found, status=status)
results["tuned_content"] = tuned
stamp("tuned")

# ================================================================== SUMMARY
print("\nSUMMARY")
print(f"   gates: {'ALL PASS' if not fails else 'FAILED: ' + ', '.join(fails)}")
print(f"   G1 (content {cstr(GRADED)}, CPR-EH): {G1['grade']}" + (f"; P = {G1['P']:.5f}, z = {G1['z']:+.3f}" if G1.get("P") else ""))
print(f"   content B (canonical dark fields): NOT DEFINED by the record -> not a trial")
print(f"   N_mech: {N_MECH_BEFORE} -> {N_MECH_BEFORE + 1} (one graded trial)")
print("   Alpha stays an INPUT; kappa = 1/2 stays FITTED; kappa and Z enter nowhere; the SM mass sector stays walled; not theory closed.")
results["gates_failed"] = fails
results["N_mech_after"] = N_MECH_BEFORE + 1
results["runtime_s"] = time.time() - T0
results["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
suffix = "" if MODE == "NORMAL" else "_" + MODE


def _js(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


(HERE / f"cfg901_d03{suffix}.json").write_text(json.dumps(results, indent=1, default=_js))
stamp("done")
sys.exit(1 if fails else 0)
