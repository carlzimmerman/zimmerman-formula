"""CFG906: alpha door D04, unimodular asymptotic-safety f_g (frozen criteria: CFG906_PREREGISTRATION.md, commit 29fb5fdc0).

Usage (from any directory; one core, a few minutes, < 900 MB, watchdog):
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg906_d04.py                real run          -> exit 0 iff every gate passes
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg906_d04.py MUTATE_SIGN    matter traces x -1 (AS3 reproduction and the unimodular flow)
                                                                         -> K0a and K6 (matter) must FAIL, exit 1; L-SIGN must PASS
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg906_d04.py MUTATE_SPLIT   sigma kinetic block sign flipped in the flat f_g computation
                                                                         -> K3b must FAIL, exit 1; L-SPLIT must PASS
Graded trial G1: measure M-eq, CPR sigma regulator, f_g from TT + sigma at alpha_T -> 0, P-lin vertices, g_Y* at M_P, lane B one-loop downstream.
K = 72 declared variants; the other 71 are reported, not graded.  N_mech 373 -> 374.
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
import itertools
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
import as2_common as A2                  # noqa: E402  AS2/AS3 CPR machinery (unchanged)
import as3_gcpr as G3                    # noqa: E402  AS3 heat kernels (unchanged)
import as4_systematics as H4             # noqa: E402  AS3/AS4 two-loop and reduced-Planck systematics (unchanged)

FG1 = A2.FG1                             # AS1 flat-space graviton-photon action (unchanged)
C1 = A2.C1
RG = C1.RG
MODE = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
assert MODE in ("NORMAL", "MUTATE_SIGN", "MUTATE_SPLIT"), MODE
MSIGN = -1 if MODE == "MUTATE_SIGN" else 1
SPLIT = MODE == "MUTATE_SPLIT"
T0 = time.time()
TARGET = RG.ALPHA_INV0                   # 137.035999177, target only
NS, ND, NV = A2.NS, A2.ND, A2.NV
R, z, D = A2.R, A2.z, A2.D
F0, F1, F2, dF1 = A2.F0, A2.F1, A2.F2, A2.dF1
bg = A2.bg
P_, DP = A2.P, A2.DP
Q = sp.Rational
SM = {NS: Q(4), ND: Q(45, 2), NV: Q(12)}
N_MECH_BEFORE = 373
e_ = sp.Symbol("e", real=True)           # e = d_t f' / f'  (= 2 at a fixed point, eta_N = -2)
gS = sp.Symbol("g", positive=True)

fails = []
results = {"mode": MODE, "prereg_commit": "29fb5fdc0"}


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)
    return bool(ok)


def stamp(label):
    print(f"   [{label}: {time.time() - T0:.1f} s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576:.0f} MB]")


def half_unit(printed):
    s_ = printed.lstrip("-")
    dec = len(s_.split(".")[1]) if "." in s_ else 0
    return 0.5 * 10.0**(-dec)


def close_printed(val, printed):
    return val is not None and abs(val - float(printed)) <= half_unit(printed) + 1e-15


def fmt(v, spec=".6f"):
    return "None" if v is None else format(v, spec)


print(f"MODE: {MODE}")
print(f"python {sys.version.split()[0]}, numpy {np.__version__}, sympy {sp.__version__}, scipy {scipy.__version__}")

# ================================================================== (0) PRE-FLIGHT: frozen route error (CFG901's, record numbers)
REC = dict(two_loop=96.07582 - 95.57847, m_red=abs(93.82509 - 95.57847), y1=8.8e-4 * 137.036,
           scheme=abs(92.914 - 95.57847), trunc=abs(91.04527 - 96.37265))
SIGMA_ROUTE = float(np.sqrt(sum(v**2 for v in REC.values())))
SIGMA_ADM = float(np.sqrt(sum(v**2 for k, v in REC.items() if k != "trunc") + (95.57847 - 95.26961)**2))
print("\n(0) PRE-FLIGHT (rules section 1.6): route error frozen from the record (inherited from CFG901)")
for k, v in REC.items():
    print(f"   {k:9s} {v:.5f}")
print(f"   sigma_route = {SIGMA_ROUTE:.4f} (frozen 6.230); admissible-only variant {SIGMA_ADM:.4f} (frozen 3.245)")
chk("PF sigma_route", abs(SIGMA_ROUTE - 6.230) < 5e-4 and abs(SIGMA_ADM - 3.245) < 5e-4, "sigma_route and the admissible-only variant equal the frozen values")
delta_route = SIGMA_ROUTE / TARGET
print(f"   delta_route = {delta_route:.4f} -> diagnostic (< 1); 1% would need sigma <= 1.37: not reachable, ceiling CONSISTENT")
results["preflight"] = dict(components=REC, sigma_route=SIGMA_ROUTE, sigma_admissible_only=SIGMA_ADM, delta_route=delta_route)

B3 = C1.laneB_b3()
B2 = C1._exec_lane_b_script("b2_required_boundary.py")
F_NEEDED = float(B3.f_needed)


def P_of(fg):
    return C1.downstream_P(fg) if fg is not None and fg > 0 else None


def grade_value(Pv, sigma=SIGMA_ROUTE):
    zz = (Pv - TARGET) / sigma
    return ("KILLED" if abs(zz) > 3 else "CONSISTENT"), zz


def p_single(miss):
    m = abs(miss)
    lo = max(TARGET - m, 10.0)
    hi = min(TARGET + m, 1000.0)
    return float(np.log(hi / lo) / np.log(100.0))


FG_CPR_GENERAL = -5 * (8 * F0 + 4 * F1 - dF1) / (1152 * sp.pi**2 * (F0 + F1)**2)        # AS3 printed (as3_trial.out)


def fg_cpr_num(gt):
    f0, f1 = float(gt[0]), float(gt[1])
    return -5 * (8 * f0 + 4 * f1 - 2 * f1) / (1152 * np.pi**2 * (f0 + f1)**2)


# ================================================================== (1) GATE K0: AS3 reproduced (AS2 code, SM content)
print("\n(1) GATE K0: AS3 CPR-EH with SM matter (AS2/AS3 code, imported read-only)")
HK = G3.heat_kernels()
XM_SYM, XM_PARTS = A2.X_matter(HK)
XM_SM = sp.expand(XM_SYM.subs(SM))
XG1 = A2.X_gravity(HK, with_eta=True, order_f=1)
bet_k0 = A2.beta_system(XG1 + MSIGN * XM_SM, 1)
roots_k0, f_k0, J_k0 = A2.find_roots(bet_k0, 1, grid=True)
rows_k0 = []
for r_ in roots_k0:
    glb = A2.to_glb(r_)
    dom, edge = A2.in_domain(glb)
    adm = A2.admissible(glb) and dom
    fgv = fg_cpr_num(r_)
    rows_k0.append(dict(gt=[float(x) for x in r_], glb=[float(x) for x in glb], adm=adm, fg=fgv, P=(P_of(fgv) if dom else None)))
adm_k0 = [x for x in rows_k0 if x["adm"]]
ok = len(adm_k0) == 1 and close_printed(adm_k0[0]["glb"][0], "0.967159") and close_printed(adm_k0[0]["glb"][1], "-1.22293") \
    and close_printed(adm_k0[0]["fg"], "0.03883093") and close_printed(adm_k0[0]["P"], "95.57847")
chk("K0a AS3 CPR-EH (SM)", ok, (f"(g, lambda) = ({adm_k0[0]['glb'][0]:.7f}, {adm_k0[0]['glb'][1]:.6f}), f_g = {adm_k0[0]['fg']:.9f}, "
                               f"P = {fmt(adm_k0[0]['P'])}" if len(adm_k0) == 1 else f"{len(adm_k0)} admissible roots: "
                               + "; ".join(f"{np.round(x['glb'], 6)}" for x in rows_k0)) + " vs (0.967159, -1.22293), 0.03883093, 95.57847")
GT_K0 = adm_k0[0]["gt"] if len(adm_k0) == 1 else None
if len(adm_k0) == 1 and adm_k0[0]["P"] is not None:
    P2l, _ = H4.two_loop_P(C1.gY_star_from_fg(adm_k0[0]["fg"]), B2)
    Pmr = H4.reduced_planck_P(adm_k0[0]["fg"])
    chk("K0b AS3 EH systematics (SM)", close_printed(P2l, "96.07582") and close_printed(Pmr, "93.82509"),
        f"two-loop {P2l:.6f}, M_red {Pmr:.6f} vs 96.07582, 93.82509")
else:
    chk("K0b AS3 EH systematics (SM)", False, "no unique admissible K0 root")
g0ok = (abs(C1.downstream_P(B3.fg) - B3.c5) < 1e-9 and abs(C1.downstream_P(0.04795) / 92.914 - 1) < 1e-4
        and abs(C1.downstream_P(0.009805) / 137.036 - 1) < 1e-4 and abs(C1.downstream_P(B3.f_needed) - B3.c6) < 1e-9)
chk("K0c downstream G0", g0ok, f"P(0.04795) = {C1.downstream_P(0.04795):.4f}, P(0.009805) = {C1.downstream_P(0.009805):.4f}, "
    f"P(f_needed = {F_NEEDED:.6f}) = {C1.downstream_P(F_NEEDED):.6f}")
stamp("K0")

# ================================================================== (2) FLAT-SPACE f_g MACHINERY (AS1/AS2 method, traceless field space)
print("\n(2) FLAT-SPACE f_g: AS1's bilinear action, traceless h (9) + photon (4), q = kappa e_4, Litim q^2 -> P_k, eta terms d_t f'")
s = sp.Symbol("s", positive=True)
aT = sp.Symbol("a_T", positive=True)     # 1/alpha_T, TDiff gauge-fixing strength
B0, V1_AS1, V2_AS1, hm, hp, am, ap = FG1.bilinear_action(s)
kap, ee, xi = FG1.kap, FG1.e, FG1.xi
PHM = list(hm) + list(am)
PHP = list(hp) + list(ap)
NF = len(PHM)
Hm_, _ = FG1.hmat("hm")
Hp_, _ = FG1.hmat("hp")


def mat(expr):
    return sp.Matrix(NF, NF, lambda i, j: sp.diff(expr, PHM[i], PHP[j]))


B_UG = sp.expand(B0.subs(FG1.agf, 0).subs(FG1.lam, 0).subs(FG1.g, -1 / (16 * sp.pi * F1)))                 # no sqrt(g)^(2) term
B_STD = sp.expand(B0.subs(FG1.agf, 0).subs({FG1.lam: -F0 / (2 * F1)}).subs(FG1.g, -1 / (16 * sp.pi * F1)))  # cosmological term restored
GF_T = (-F1) * aT / 2 * s * sum(Hm_[3, nu] * Hp_[3, nu] for nu in range(3))                                   # (Z_N a_T/2) |F^T|^2, F^T = i|q| h_{4 nu}, nu _|_ q
MK_UG = mat(B_UG)
MK_STD = mat(B_STD)
MK_GF = mat(GF_T)
M1_LIN = mat(V1_AS1)
M2_LIN = mat(V2_AS1)

idx = {pq: i for i, pq in enumerate(FG1.pairs)}


def hv(d):
    v = [0] * NF
    for (m, n), c in d.items():
        v[idx[(min(m, n), max(m, n))]] += c
    return v


TT_COLS = [hv({(0, 1): 1}), hv({(0, 2): 1}), hv({(1, 2): 1}), hv({(0, 0): 1, (1, 1): -1}), hv({(0, 0): 1, (1, 1): 1, (2, 2): -2})]
SIG_COLS = [hv({(0, 0): 1, (1, 1): 1, (2, 2): 1, (3, 3): -3})]
XIT_COLS = [hv({(0, 3): 1}), hv({(1, 3): 1}), hv({(2, 3): 1})]
PHOT_COLS = [[0] * 10 + [1 if j == k else 0 for j in range(4)] for k in range(4)]
def frob2(col):
    """Frobenius norm^2 of the symmetric matrix encoded by a 10-component column (off-diagonal entries count twice)."""
    tot = 0
    for i, c in enumerate(col[:10]):
        m, n = FG1.pairs[i]
        tot += c * c * (1 if m == n else 2)
    return tot


# ---- vertex builder (re-implementation of AS1's construction, for the parametrisation axis and the Weyl check)
EPS = sp.Symbol("eps")
XH, _ = FG1.hmat("x")
FB = FG1.Fbar_matrix()
FSYM = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f"f{m}{n}"))
TRACELESS_X = {sp.Symbol("x33"): -(sp.Symbol("x00") + sp.Symbol("x11") + sp.Symbol("x22"))}


def TFF(ginv, sqrtg, G1m, G2m):
    return sp.expand(sqrtg * sum(ginv[m, a] * ginv[n, b] * G1m[m, n] * G2m[a, b]
                                 for m in range(4) for n in range(4) for a in range(4) for b in range(4)))


def metric_pieces(kind, H):
    I4 = sp.eye(4)
    if kind == "AS1-linear":
        tr = H.trace()
        return I4 - EPS * H + EPS**2 * H * H, 1 + EPS * tr / 2 + EPS**2 * (tr**2 / 8 - (H * H).trace() / 4)
    if kind == "exp":                      # g = exp(h), traceless: sqrt g = 1, g^-1 = 1 - h + h^2/2
        return I4 - EPS * H + EPS**2 * H * H / 2, sp.Integer(1)
    if kind == "unimodular-linear":        # g = (1 + h) det(1 + h)^(-1/4), H must be traceless here; sqrt g = 1 exactly
        det = sp.expand((I4 + EPS * H).det())
        d14 = sp.series(det**Q(1, 4), EPS, 0, 3).removeO()
        inv = I4 - EPS * H + EPS**2 * H * H
        return (d14 * inv).applyfunc(lambda x: sp.expand(sp.series(sp.expand(x), EPS, 0, 3).removeO())), sp.Integer(1)
    raise ValueError(kind)


def T12(kind, traceless_input=False):
    H = XH.subs(TRACELESS_X) if traceless_input else XH
    ginv, sqrtg = metric_pieces(kind, H)
    T1 = TFF(ginv, sqrtg, FB, FSYM).coeff(EPS, 1)
    T2 = TFF(ginv, sqrtg, FB, FB).coeff(EPS, 2)
    return sp.expand(T1), sp.expand(T2)


def polarise(T1, T2):
    def T1sub(Hx, fx):
        rep = {sp.Symbol(f"x{m}{n}"): Hx[m, n] for (m, n) in FG1.pairs}
        rep.update({sp.Symbol(f"f{m}{n}"): fx[m][n] for m in range(4) for n in range(4)})
        return T1.xreplace(rep)

    def T2sub(Hx):
        return T2.xreplace({sp.Symbol(f"x{m}{n}"): Hx[m, n] for (m, n) in FG1.pairs})
    qh = [0, 0, 0, 1]
    I_ = sp.I
    fm_v = [[-I_ * kap * (qh[m] * am[n] - qh[n] * am[m]) for n in range(4)] for m in range(4)]
    fp_v = [[I_ * kap * (qh[m] * ap[n] - qh[n] * ap[m]) for n in range(4)] for m in range(4)]
    V1 = 1 / (4 * ee**2) * 2 * Q(1, 2) * (T1sub(Hm_, fp_v) + T1sub(Hp_, fm_v))
    V2 = 1 / (4 * ee**2) * sp.expand((T2sub(Hm_ + Hp_) - T2sub(Hm_) - T2sub(Hp_)) / 2)
    return sp.expand(V1), V2


print("   building vertices (AS1 re-implementation, exp parametrisation, unimodular-linear) ...")
T1_as1, T2_as1 = T12("AS1-linear")
V1_re, V2_re = polarise(T1_as1, T2_as1)
T1_exp, T2_exp = T12("exp")
V1_exp, V2_exp = polarise(T1_exp, T2_exp)
M2_EXP = mat(V2_exp)
T1_as1_tl = sp.expand(T1_as1.subs(TRACELESS_X))
T2_as1_tl = sp.expand(T2_as1.subs(TRACELESS_X))
T1_ul_tl, T2_ul_tl = T12("unimodular-linear", traceless_input=True)
T1_exp_tl = sp.expand(T1_exp.subs(TRACELESS_X))
stamp("vertices")

print("\n   GATE K2: vertices")
chk("K2a vertex builder = AS1", sp.expand(V1_re - V1_AS1) == 0 and sp.expand(V2_re - V2_AS1) == 0,
    "the re-implemented construction reproduces AS1's V1 and V2 exactly (all 10 h components)")
chk("K2b Weyl invariance (P-lin)", sp.expand(T1_ul_tl - T1_as1_tl) == 0 and sp.expand(T2_ul_tl - T2_as1_tl) == 0,
    "g = (1 + h) det(1 + h)^(-1/4) (sqrt g = 1, det from sympy) gives AS1's vertices on traceless h to second order")
v1exp_same = sp.expand(T1_exp_tl - T1_as1_tl) == 0
print(f"   (info) exp parametrisation: first-order vertex equals AS1's on traceless h: {v1exp_same}; the second-order vertex differs "
      f"(nonzero difference: {sp.expand(sp.expand(T2_exp.subs(TRACELESS_X)) - T2_as1_tl) != 0})")


def limit_inf(expr, sym):
    expr = sp.together(expr)
    num, den = sp.fraction(expr)
    pn = sp.Poly(sp.expand(num), sym)
    pd = sp.Poly(sp.expand(den), sym)
    if pn.degree() > pd.degree():
        raise RuntimeError("limit diverges")
    if pn.degree() < pd.degree():
        return sp.Integer(0)
    return pn.LC() / pd.LC()


def restricted_K(MK, hcols, gf=None, flip_sigma=None):
    E = sp.Matrix(hcols + PHOT_COLS).T
    Mk = MK + (MK_GF.subs(aT, gf) if gf is not None else sp.zeros(NF, NF))
    Kr = sp.Matrix(sp.expand(E.T * Mk * E))                # mutable (needed by the MUTATE_SPLIT flip)
    if flip_sigma is not None:
        i = flip_sigma
        off = [Kr[i, j] for j in range(Kr.shape[0]) if j != i] + [Kr[j, i] for j in range(Kr.shape[0]) if j != i]
        assert all(sp.simplify(x) == 0 for x in off), "sigma is not kinetically decoupled"
        Kr[i, i] = -Kr[i, i]
    return E, Kr


def fg_flat(MK, M2, hcols, gf=None, flip_sigma=None, limit_aT=False):
    """f_g from the F-bar^2 coefficient of the graviton-photon trace restricted to span(hcols) + photon (AS2 fg_flat_cpr / AS3 roots report method).
    gf: None (no gauge fixing in the span), a number or the symbol a_T (then limit_aT takes a_T -> infinity)."""
    E, Kr = restricted_K(MK, hcols, gf, flip_sigma)
    nh = len(hcols)
    KP = Kr.subs(s, P_)
    dR = sp.Matrix(sp.diff(Kr, s).subs(s, P_) * DP)          # mutable copy (crash fix after run 1, no graded number had been computed)
    dR[:nh, :nh] += dF1 * (sp.diff(Kr[:nh, :nh], F1).subs(s, P_) - sp.diff(Kr[:nh, :nh], F1))
    dR = dR.subs(s, kap**2)
    n = nh + 4
    G = sp.zeros(n, n)
    G[:nh, :nh] = KP[:nh, :nh].inv()
    G[nh:, nh:] = KP[nh:, nh:].inv()
    m1 = E.T * M1_LIN * E
    m2 = E.T * M2 * E
    Tr = -Q(1, 2) * (G * m2 * G * dR).trace() + Q(1, 2) * (G * m1 * G * m1 * G * dR).trace()
    if limit_aT:
        Tr = limit_inf(Tr, aT)
    Tr = sp.expand(Tr)
    C = sp.zeros(6, 6)
    for a_, A_ in enumerate(FG1.Fs):
        C[a_, a_] = Tr.coeff(A_, 2)
        for b_, B_ in enumerate(FG1.Fs):
            if a_ != b_:
                C[a_, b_] = Tr.coeff(A_, 1).coeff(B_, 1) / 2
    dual = {0: (5, 1), 1: (4, -1), 2: (3, 1)}
    star = sp.zeros(6, 6)
    for i_, (j_, sg) in dual.items():
        star[i_, j_] = sg
        star[j_, i_] = sg
    parity_ok = sp.simplify((C * star).trace()) == 0
    trC = sp.simplify(C.trace())
    cFF = sp.integrate(sp.expand(trC / 12 * kap**3 / (8 * sp.pi**2)), (kap, 0, 1))
    fg = sp.factor(sp.simplify(2 * ee**2 * cFF))
    return fg, parity_ok


def at_fp_g(fexpr):
    """closed form in g at a fixed point: F1 = -1/(16 pi g), d_t f' = 2 f'."""
    return sp.simplify(fexpr.subs(dF1, 2 * F1).subs(F1, -1 / (16 * sp.pi * gS)))


# ---- GATE K3: flat unimodular kinetic form
print("\n   GATE K3: flat unimodular kinetic form (no gauge fixing)")
E9 = sp.Matrix(TT_COLS + SIG_COLS + XIT_COLS).T[:10, :]
K9 = sp.expand(E9.T * MK_UG[:10, :10] * E9)
null_ok = True
for k in range(3):
    v = sp.zeros(9, 1)
    v[6 + k] = 1                                  # coordinates of a TDiff pure-gauge mode h = q v + v q (v _|_ q)
    null_ok = null_ok and all(sp.simplify(x) == 0 for x in (K9 * v))
sig_null = all(sp.simplify(x) == 0 for x in (K9 * sp.Matrix([0, 0, 0, 0, 0, 1, 0, 0, 0])))
chk("K3a TDiff zero modes", null_ok and not sig_null,
    "the kinetic form annihilates h = q v + v q for v _|_ q (3 modes) and does NOT annihilate sigma (sigma is not gauge under TDiff)")
_, Kr_sig = restricted_K(MK_UG, SIG_COLS, flip_sigma=(0 if SPLIT else None))
_, Kr_tt = restricted_K(MK_UG, TT_COLS[:1])
ZN = -F1
k_sig = sp.simplify(Kr_sig[0, 0] / frob2(SIG_COLS[0]))
k_tt = sp.simplify(Kr_tt[0, 0] / frob2(TT_COLS[0]))
chk("K3b kinetic coefficients", sp.simplify(k_sig - (-ZN * s / 8)) == 0 and sp.simplify(k_tt - ZN * s / 4) == 0,
    f"per unit Frobenius norm: sigma = {sp.factor(k_sig)} (hand -Z_N s/8 = {sp.factor(-ZN * s / 8)}), TT = {sp.factor(k_tt)} (hand +Z_N s/4)")
stamp("K3")

# ---- f_g computations
print("\n   f_g computations (closed forms in f' = F1 and d_t f' = dF1; photon gauge xi kept symbolic)")
FG = {}
PAR = {}


def run_fg(label, *args, **kw):
    t_ = time.time()
    fexpr, par = fg_flat(*args, **kw)
    FG[label], PAR[label] = fexpr, par
    print(f"   {label:44s} f_g = {fexpr}    [parity {par}; xi-free {sp.diff(fexpr, xi) == 0}; {time.time() - t_:.1f} s]")
    return fexpr


run_fg("K1 standard TT (cosmological term restored)", MK_STD, M2_LIN, TT_COLS)
run_fg("UG TT only (P-lin)", MK_UG, M2_LIN, TT_COLS)
run_fg("UG sigma only (P-lin)", MK_UG, M2_LIN, SIG_COLS, flip_sigma=(0 if SPLIT else None))
if SPLIT:
    run_fg("UG sigma only, unflipped (P-lin)", MK_UG, M2_LIN, SIG_COLS)
run_fg("UG TT + sigma, alpha_T -> 0 (P-lin)", MK_UG, M2_LIN, TT_COLS + SIG_COLS, flip_sigma=(5 if SPLIT else None))
run_fg("UG 9 modes, a_T -> infinity (P-lin)", MK_UG, M2_LIN, TT_COLS + SIG_COLS + XIT_COLS, gf=aT, limit_aT=True,
       flip_sigma=(5 if SPLIT else None))
run_fg("UG 9 modes, alpha_T = 1 (P-lin)", MK_UG, M2_LIN, TT_COLS + SIG_COLS + XIT_COLS, gf=1, flip_sigma=(5 if SPLIT else None))
run_fg("UG TT only (P-exp)", MK_UG, M2_EXP, TT_COLS)
run_fg("UG TT + sigma, alpha_T -> 0 (P-exp)", MK_UG, M2_EXP, TT_COLS + SIG_COLS, flip_sigma=(5 if SPLIT else None))
run_fg("UG 9 modes, alpha_T = 1 (P-exp)", MK_UG, M2_EXP, TT_COLS + SIG_COLS + XIT_COLS, gf=1, flip_sigma=(5 if SPLIT else None))
stamp("f_g")

print("\n   GATE K1 (the K-test: TT coincidence limit) and K7 (flat consistency)")
k1a = sp.simplify(FG["K1 standard TT (cosmological term restored)"] - FG_CPR_GENERAL) == 0
fg_TT = FG["UG TT only (P-lin)"]
k1c = sp.simplify(fg_TT - FG_CPR_GENERAL.subs(F0, 0)) == 0
k1_num = None
if GT_K0 is not None:
    fnum = float(FG["K1 standard TT (cosmological term restored)"].subs({F0: GT_K0[0], F1: GT_K0[1], dF1: 2 * GT_K0[1]}).subs(xi, 1))
    k1_num = (fnum, C1.downstream_P(fnum))
chk("K1a TT + cosmological term = AS3's general formula", k1a, "-5 (8 F0 + 4 F1 - dF1)/(1152 pi^2 (F0 + F1)^2) reproduced identically")
chk("K1b AS3's committed values at K0's root", k1_num is not None and close_printed(k1_num[0], "0.03883093") and close_printed(k1_num[1], "95.57847"),
    f"f_g = {k1_num[0]:.9f}, P = {fmt(k1_num[1])} vs 0.03883093, 95.57847" if k1_num else "no K0 root")
fg_TT_g = at_fp_g(fg_TT)
chk("K1c unimodular TT = AS3's formula at f = 0", k1c and sp.simplify(fg_TT_g - 5 * gS / (36 * sp.pi)) == 0,
    f"f_g^TT = {sp.factor(fg_TT)} = 5(4 - e) g/(72 pi); at the fixed point {fg_TT_g}")
chk("K7a parity", all(PAR.values()), "self-dual and anti-self-dual F-bar components carry equal weight in every computation")
chk("K7b photon-gauge independence", all(sp.diff(v, xi) == 0 for v in FG.values()), "no f_g depends on xi")
sig_key = "UG sigma only (P-lin)"
add_ok = sp.simplify(FG["UG TT + sigma, alpha_T -> 0 (P-lin)"] - fg_TT - FG[sig_key]) == 0
chk("K7c additivity", add_ok, "f_g(TT + sigma) = f_g(TT) + f_g(sigma) at alpha_T -> 0")
chk("K7d alpha_T -> 0 limit", sp.simplify(FG["UG 9 modes, a_T -> infinity (P-lin)"] - FG["UG TT + sigma, alpha_T -> 0 (P-lin)"]) == 0,
    "the 9-mode computation with gauge parameter a_T, a_T -> infinity, equals the restriction to TT + sigma")

fg_sig = FG[sig_key]
fg_G1 = FG["UG TT + sigma, alpha_T -> 0 (P-lin)"]
fg_aT1 = FG["UG 9 modes, alpha_T = 1 (P-lin)"]
r_sig = sp.simplify(fg_sig / fg_TT)
r_xi = sp.simplify((fg_aT1 - fg_G1) / fg_TT)
r_exp = [sp.simplify(FG[a] - FG[b]) for a, b in (("UG TT only (P-exp)", "UG TT only (P-lin)"),
                                                  ("UG TT + sigma, alpha_T -> 0 (P-exp)", "UG TT + sigma, alpha_T -> 0 (P-lin)"),
                                                  ("UG 9 modes, alpha_T = 1 (P-exp)", "UG 9 modes, alpha_T = 1 (P-lin)"))]
print("\n   EXPECTATIONS (pre-registered hand values, section 10.2; reported, not gates)")
print(f"   E1 f_g^sigma / f_g^TT = {r_sig}  (hand -2/5){'  [as expected]' if r_sig == Q(-2, 5) else '  [DIFFERS from the hand value]'}")
print(f"   E2 f_g^xi(alpha_T = 1) / f_g^TT = {r_xi}  (hand +3/5){'  [as expected]' if r_xi == Q(3, 5) else '  [DIFFERS from the hand value]'}")
print(f"   E3 P-exp - P-lin (TT, TT + sigma, alpha_T = 1) = {r_exp}  (hand: all 0){'  [as expected]' if all(x == 0 for x in r_exp) else '  [DIFFERS]'}")
fg_G1_g = at_fp_g(fg_G1)
print(f"   graded f_g at a fixed point: {fg_G1_g}  (hand g/(12 pi))")
results["f_g_closed_forms"] = {k: str(v) for k, v in FG.items()}
results["expectations"] = dict(sigma_over_TT=str(r_sig), xi_over_TT=str(r_xi), exp_minus_lin=[str(x) for x in r_exp], graded_fp=str(fg_G1_g))
stamp("K1/K7")

# ================================================================== (3) S^4 BLOCKS AND THE UNIMODULAR FLOW OF g
print("\n(3) S^4: unimodular blocks from AS2's cpr_blocks with f -> f' R/2, f'' -> 0, CPR gauge term removed")
TTb, XIb, Sb = A2.cpr_blocks()
ON = {F0: F1 * R / 2, F2: 0}
H_TT = sp.expand(TTb.subs(ON))
H_SS = sp.factor(Sb[1, 1].subs(ON).subs(bg, 0))
H_HH = sp.factor(Sb[0, 0].subs(ON))
XI_ACT = sp.simplify(XIb.subs(ON).subs(bg, 0))
# Lichnerowicz endomorphism on traceless symmetric tensors of S^4 from the Riemann tensor
Rs = sp.Symbol("Rs", positive=True)
Riem = lambda a, b, c, d: Rs / 12 * (int(a == c) * int(b == d) - int(a == d) * int(b == c))
hsym = sp.Matrix(4, 4, lambda m, n: sp.Symbol(f"t{min(m, n)}{max(m, n)}"))
hsym = hsym.subs(sp.Symbol("t33"), -(sp.Symbol("t00") + sp.Symbol("t11") + sp.Symbol("t22")))
endo = sp.Matrix(4, 4, lambda m, n: -2 * sum(Riem(m, a, n, b) * hsym[a, b] for a in range(4) for b in range(4))
                 + sum(Rs / 4 * int(m == a) * hsym[a, n] + Rs / 4 * int(n == a) * hsym[a, m] for a in range(4)))
lich_ok = sp.simplify(endo - 2 * Rs / 3 * hsym) == sp.zeros(4, 4)
print("   GATE K4: S^4 blocks")
chk("K4a on-shell gauge invariance", XI_ACT == 0, "the action part of AS2's xi block vanishes identically at f = f' R/2")
chk("K4b TT = massless spin-2", sp.simplify(H_TT - (-F1 / 2) * (D + R / 6)) == 0 and lich_ok,
    f"TT block = {sp.factor(H_TT)}; Delta_L - D = 2R/3 on traceless tensors (S^4 Riemann tensor), so TT = -(f'/2)(Delta_L - 2 Lambda), Lambda = R/4")
chk("K4c sigma = D^2 x trace block", sp.simplify(H_SS - D**2 * H_HH) == 0 and sp.simplify(H_HH - Q(3, 16) * F1 * (D - R / 3)) == 0,
    f"sigma block = {H_SS}; on-shell trace block = {H_HH}")


def L_(J):
    return sp.simplify(DP * sp.diff(sp.log(J), D).subs(D, P_))


def W_block(H, with_eta):
    HP, dR = A2.dtR(sp.Matrix([[H]]), with_eta)
    return sp.simplify(dR[0, 0] / HP[0, 0])


def ug_parts(measure, sreg, with_eta=True):
    parts = [("TT", Q(1, 2), "TT", 0, W_block(H_TT, with_eta), "TT")]
    if sreg == "CPR":
        parts += [("sigma", Q(1, 2), "S", 6, W_block(H_SS, with_eta), "sigma"), ("J_S", -Q(1, 2), "S", 6, L_(D * (D - R / 3)), "sigma")]
    else:
        parts += [("sigma (normalised)", Q(1, 2), "S", 6, W_block(Q(3, 16) * F1 * D, with_eta), "sigma")]
    parts += [("xi (TDiff gauge, alpha_T -> 0)", Q(1, 2), "VT", 10, L_((D - R / 4)**2), "VT"),
              ("ghost c^T", -1, "VT", 10, L_(D - R / 4), "VT"),
              ("J_V", -Q(1, 2), "VT", 10, L_(D - R / 4), "VT")]
    if measure == "M-eq":
        parts += [("measure scalar (M-eq)", -Q(1, 2), "S", 0, L_(D), "measure")]
    return parts


def trace_parts(parts, order, nexcl_zero=False):
    out = {}
    for name, w, fld, nex, W, sector in parts:
        Wn = sp.simplify(W.subs(dF1, e_ * F1))
        c = A2.trace_R2(fld, sp.simplify(w * Wn), HK, 0 if nexcl_zero else nex, order)
        out[sector] = sp.expand(out.get(sector, 0) + c)
    return out


# ---- K5: one-loop on-shell equivalence at eta = 0 (bulk, no excluded modes)
print("\n   GATE K5: one-loop on-shell equivalence (eta = 0, bulk R^0..R^2, no excluded modes)")
phys = {"TT": sp.expand(A2.trace_R2("TT", Q(1, 2) * 2 / (1 + R / 6), HK, 0, 2)),
        "VT": sp.expand(A2.trace_R2("VT", -Q(1, 2) * 2 / (1 - R / 4), HK, 0, 2)), "S": sp.Integer(0)}
gr = {"TT": 0, "VT": 0, "S": 0}
for name, w, fld, nex, W, kind in A2.gravity_W(with_eta=False):
    Won = sp.simplify(W.subs(ON))
    gr[fld] = sp.expand(gr[fld] + A2.trace_R2(fld, sp.simplify(w * Won), HK, 0, 2))
ug_eq0 = {"TT": 0, "VT": 0, "S": 0}
ug_nv0 = {"TT": 0, "VT": 0, "S": 0}
for meas, store in (("M-eq", ug_eq0), ("M-naive", ug_nv0)):
    for name, w, fld, nex, W, sector in ug_parts(meas, "CPR", with_eta=False):
        store[fld] = sp.expand(store[fld] + A2.trace_R2(fld, sp.simplify(w * W), HK, 0, 2))
okA = all(sp.simplify(gr[k] - phys[k]) == 0 for k in phys)
okB = all(sp.simplify(ug_eq0[k] - phys[k]) == 0 for k in phys)
extra = sp.expand(A2.trace_R2("S", Q(1, 2) * 2, HK, 0, 2))
okC = all(sp.simplify(ug_nv0[k] - phys[k] - (extra if k == "S" else 0)) == 0 for k in phys)
chk("K5a GR on-shell (AS2 CPR blocks) = physical form", okA,
    "per field type: " + ", ".join(f"{k}: {sp.factor(gr[k])}" for k in ("TT", "VT", "S")))
chk("K5b unimodular M-eq = physical form", okB, "per field type equal (scalar sector cancels)")
chk("K5c M-naive - physical = (1/2) Tr_S[2/P]", okC, f"difference in the scalar sector: {sp.factor(ug_nv0['S'])} (= {sp.factor(extra)})")
zeta = 24 * sp.expand(phys["TT"] + phys["VT"]).coeff(R, 2)
print(f"   (info) 24 x R^2 coefficient of the physical form = {zeta} (expected 59/45); recalled Christensen-Duff -571/45 = {zeta} - 14"
      f" -> {zeta - 14 == Q(-571, 45)} (recalled; the integer is the excluded modes; not gating)")
results["K5"] = dict(zeta_bulk=str(zeta))
stamp("K4/K5")

# ---- the flow: R^1 coefficients by sector, K6, fixed points
print("\n   THE UNIMODULAR FLOW OF g: R^1 coefficients of X = (16 pi^2/V) d_t Gamma by sector (e = d_t f'/f')")
HAND = {"TT": -Q(5, 4) - 5 * e_ / 18, "sigma CPR": Q(1, 6) + 17 * e_ / 240, "sigma norm": Q(1, 6) + e_ / 24,
        "VT": -Q(5, 8), "measure": -Q(1, 6)}
SECT = {}
for meas in ("M-eq", "M-naive"):
    for sreg in ("CPR", "norm"):
        tp = trace_parts(ug_parts(meas, sreg), 1)
        SECT[(meas, sreg)] = {k: sp.simplify(v.coeff(R, 1)) for k, v in tp.items()}
X1_MATTER = sp.simplify(XM_SM.coeff(R, 1))
print("   sector            code R^1                   hand")
k6 = []
for lab, key, hk in (("TT", ("M-eq", "CPR"), "TT"), ("sigma + J_S (CPR)", ("M-eq", "CPR"), "sigma CPR"),
                     ("sigma normalised", ("M-eq", "norm"), "sigma norm"), ("VT (xi+ghost+J_V)", ("M-eq", "CPR"), "VT"),
                     ("M-eq scalar", ("M-eq", "CPR"), "measure")):
    sec = {"TT": "TT", "sigma CPR": "sigma", "sigma norm": "sigma", "VT": "VT", "measure": "measure"}[hk]
    code = SECT[key][sec]
    okk = sp.simplify(code - HAND[hk]) == 0
    k6.append(okk)
    print(f"   {lab:18s} {str(sp.nsimplify(code)):26s} {HAND[hk]}   {'ok' if okk else 'MISMATCH'}")
print(f"   matter (SM)        {MSIGN * X1_MATTER}                      -61/12 = (N_S - N_D - N_V)/6")
chk("K6 hand closed forms of the R^1 coefficients", all(k6), "TT, sigma (CPR and normalised), VT, M-eq scalar equal the pre-registered hand forms")
chk("K6 matter R^1 coefficient", sp.simplify(MSIGN * X1_MATTER + Q(61, 12)) == 0, f"matter R^1 = {MSIGN * X1_MATTER} vs -61/12")


def flow(meas, sreg, matter_sign=MSIGN, x1_override=None):
    sec = SECT[(meas, sreg)]
    X1e = sp.expand(sum(sec.values()) + matter_sign * X1_MATTER)
    if x1_override is not None:
        X1e = sp.sympify(x1_override)
    a_ = sp.simplify(X1e.subs(e_, 0))
    b_ = sp.simplify(sp.diff(X1e, e_))
    X1v = X1e.subs(e_, 2)
    if x1_override is None:
        X1v = sp.nsimplify(X1v)
    if X1v == 0:
        return dict(X1=X1v, g=None, adm=False, why="X1 = 0")
    gstar = -2 * sp.pi / X1v
    gv = float(gstar)
    # beta(g1) = gd1 - 2 g1, gd1 = a g1/(16 pi^2 g1 - b) (from 16 pi^2 gd1 = a + b gd1/g1); theta = -d beta/d g1 at the fixed point
    g1 = sp.Symbol("g1")
    beta = a_ * g1 / (16 * sp.pi**2 * g1 - b_) - 2 * g1
    g1s = -1 / (16 * sp.pi * gstar)
    theta = float(-sp.diff(beta, g1).subs(g1, g1s)) if gv > 0 else None
    pole_g = float(-sp.pi / b_) if b_ != 0 else None
    adm = (0 < gv < 50) and not (pole_g is not None and 0 < pole_g <= gv)
    why = "admissible" if adm else ("g* <= 0" if gv <= 0 else ("g* >= 50" if gv >= 50 else "eta pole inside (0, g*]"))
    return dict(X1=X1v, X1_e=X1e, a=a_, b=b_, g=gv, g_exact=sp.simplify(gstar), theta=theta, pole_g=pole_g, adm=adm, why=why)


FLOWS = {(m, s_): flow(m, s_) for m in ("M-eq", "M-naive") for s_ in ("CPR", "norm")}
for k_, fl in FLOWS.items():
    print(f"   {k_[0]:7s} sigma {k_[1]:4s}: X1(e) = {fl['X1_e']};  X1(2) = {fl['X1']} = {float(fl['X1']):.6f};  g* = {fl['g_exact']} = {fl['g']:.6f};"
          f"  theta_g = {fmt(fl['theta'], '.5f')};  eta pole at g = {fmt(fl['pole_g'], '.3f')};  {fl['why']}")
# cross-check of g* by AS2's beta_system (R^0 and R^1 solved together)
x_full = sp.expand(sum(trace_parts(ug_parts("M-eq", "CPR"), 1).values()) + MSIGN * XM_SM)
x_full_g = sp.expand(x_full.subs(e_, A2.gd1 / A2.g1))
bet_ug = A2.beta_system(x_full_g, 1)
g1sym = A2.g1
sol_bs = [s_ for s_ in sp.solve(sp.numer(sp.together(bet_ug[1])), g1sym) if s_ != 0]
gs_bs = [float(-1 / (16 * sp.pi * s_)) for s_ in sol_bs]
print(f"   cross-check with AS2's beta_system (M-eq, CPR): nonzero roots of beta_g1 -> g* = {gs_bs}")
chk("FP-X beta_system cross-check", len(gs_bs) == 1 and abs(gs_bs[0] - FLOWS[('M-eq', 'CPR')]['g']) < 1e-12 * max(1, abs(gs_bs[0])),
    "AS2's beta_system gives the same unique fixed point")
results["flows"] = {f"{k[0]}|{k[1]}": dict(X1=str(v["X1"]), X1_e=str(v.get("X1_e")), g=v["g"], g_exact=str(v.get("g_exact")), theta=v.get("theta"),
                                            pole_g=v.get("pole_g"), adm=v["adm"]) for k, v in FLOWS.items()}
results["X1_sectors"] = {f"{k[0]}|{k[1]}": {kk: str(vv) for kk, vv in v.items()} for k, v in SECT.items()}
results["X1_matter"] = str(MSIGN * X1_MATTER)
stamp("flow")

# ---- classifier controls and positive controls
cc = [grade_value(TARGET)[0] == "CONSISTENT", grade_value(95.57847)[0] == "KILLED",
      grade_value(TARGET + 3.01 * SIGMA_ROUTE)[0] == "KILLED", grade_value(TARGET - 3.01 * SIGMA_ROUTE)[0] == "KILLED",
      grade_value(TARGET + 2.99 * SIGMA_ROUTE)[0] == "CONSISTENT", grade_value(TARGET - 2.99 * SIGMA_ROUTE)[0] == "CONSISTENT",
      flow("M-eq", "CPR", x1_override=sp.Integer(5))["adm"] is False, P_of(-0.01) is None]
chk("CC classifier controls", all(cc), f"{sum(cc)}/{len(cc)} planted cases classified as frozen (a failed gate -> NOT COMPLETED is the verdict rule)")
Ppl = C1.downstream_P(F_NEEDED)
gpl, zpl = grade_value(Ppl)
chk("PC(i) planted f_g = f_needed", abs(Ppl - TARGET) < 1e-6 and gpl == "CONSISTENT" and abs(zpl) < 1e-6, f"P = {Ppl:.9f}, grade {gpl}, z = {zpl:.1e}")
c_G1 = float(sp.simplify(fg_G1_g / gS))
if c_G1 > 0:
    g_pl = F_NEEDED / c_G1
    fl_pl = flow("M-eq", "CPR", x1_override=sp.Float(-2 * np.pi / g_pl, 30))
    P_pl2 = C1.downstream_P(c_G1 * fl_pl["g"])
    chk("PC(ii) planted gravity", fl_pl["adm"] and abs(P_pl2 - TARGET) < 1e-6 and grade_value(P_pl2)[0] == "CONSISTENT",
        f"planted X1 = {float(fl_pl['X1']):.6f} -> g* = {fl_pl['g']:.6f} -> f_g = {c_G1 * fl_pl['g']:.6f} -> P = {P_pl2:.9f}")
else:
    chk("PC(ii) planted gravity", False, "graded f_g/g <= 0, the planted pipeline is not defined")
GATES_OK = not fails
stamp("gates")

# ================================================================== (4) GRADED TRIAL G1
print("\n(4) GRADED TRIAL G1: M-eq, CPR sigma regulator, f_g from TT + sigma at alpha_T -> 0, P-lin, g_Y* at M_P, lane B one-loop downstream")
fl = FLOWS[("M-eq", "CPR")]
G1 = dict(flow=dict(X1=str(fl["X1"]), g=fl["g"], theta=fl["theta"], adm=fl["adm"]))
fgc = {"TT": float(sp.simplify(fg_TT_g / gS)), "sigma": float(sp.simplify(at_fp_g(fg_sig) / gS)), "G1": c_G1}
print(f"   fixed point: g* = {fl['g_exact']} = {fl['g']:.6f} ({fl['why']}); critical exponent theta_g = {fmt(fl['theta'], '.5f')}; eta_N = -2")
print(f"   f_g / g: TT {fgc['TT']:.8f} (= 5/(36 pi)), sigma {fgc['sigma']:+.8f}, graded {fgc['G1']:.8f}")
if not fl["adm"]:
    g1_grade, zA = "NOT DIAGNOSTIC (" + fl["why"] + ")", None
    print(f"   selection: {g1_grade}")
else:
    fA = c_G1 * fl["g"]
    G1.update(f_g=fA, f_g_TT=fgc["TT"] * fl["g"], f_over_fTT=fgc["G1"] / fgc["TT"])
    if fA <= 0:
        g1_grade, zA = "NOT DIAGNOSTIC (f_g <= 0: no IR-attractive g_Y*)", None
        print(f"   f_g* = {fA:.8f}: {g1_grade}")
    else:
        PA = C1.downstream_P(fA)
        g1_grade, zA = grade_value(PA)
        gYs = C1.gY_star_from_fg(fA)
        aYuv = 41 / (24 * np.pi * fA)
        z_uv = (aYuv - 55.234) / SIGMA_ROUTE
        z_adm = (PA - TARGET) / SIGMA_ADM
        P2l, _ = H4.two_loop_P(gYs, B2)
        Pmr = H4.reduced_planck_P(fA)
        g_need = F_NEEDED / c_G1
        G1.update(P=PA, z=zA, z_admissible_only=z_adm, gY_star=gYs, theta_Y=-2 * fA, f_over_required=fA / F_NEEDED, inv_alphaY_MP=aYuv,
                  z_uv=z_uv, P_two_loop=P2l, P_M_red=Pmr, g_needed_for_137=g_need)
        print(f"   f_g* = {fA:.8f} (= {fA / F_NEEDED:.4f} x the required {F_NEEDED:.6f}; = {fgc['G1'] / fgc['TT']:.4f} x the TT-only value);"
              f" g_Y* = {gYs:.6f}; theta_Y = -2 f_g = {-2 * fA:.6f} (IR-attractive)")
        print(f"   P = 1/alpha(0) = {PA:.5f};  z = (P - 137.036)/sigma_route = {zA:+.3f} (admissible-only sigma: {z_adm:+.3f});"
              f"  miss {PA - TARGET:+.4f} = {(PA / TARGET - 1) * 100:+.2f}%")
        print(f"   systematics (reported): two-loop {P2l:.5f} ({P2l - PA:+.5f}); M_red {Pmr:.5f} ({Pmr - PA:+.5f})")
        print(f"   UV cross-check (no measured alpha): 41/(24 pi f_g) = {aYuv:.4f} vs 55.234 -> z_UV = {z_uv:+.3f}"
              f" ({'same verdict' if (abs(z_uv) > 3) == (abs(zA) > 3) else 'DIFFERENT verdict (disclose)'})")
        print(f"   137.036 would need g* = f_needed/(f_g/g) = {g_need:.5f} with this f_g/g (the flow gives {fl['g']:.5f});"
              f" with the TT-only f_g/g it would need {F_NEEDED / fgc['TT']:.5f} (the door's 0.222)")
        a2s = B3.a2_mz / 1.01
        d0s = RG.DELTA_0_MZ / 1.01
        Psub = B3.aY_inv_at(RG.MZ, gYs) + a2s + d0s
        ident = TARGET / 1.01 - TARGET
        print(f"   substitution test (alpha_2^-1(M_Z), Delta_0 scaled as alpha x 1.01): P -> {Psub:.5f} (shift {Psub - PA:+.4f}); an identity would"
              f" shift {ident:+.4f}; fraction {abs((Psub - PA) / ident):.3f}; the gravitational piece shifts 0")
        G1.update(substitution_shift=Psub - PA, substitution_fraction=abs((Psub - PA) / ident))
        if g1_grade == "CONSISTENT":
            ps = p_single(PA - TARGET)
            G1.update(P_single=ps, P_family=1 - (1 - ps)**(N_MECH_BEFORE + 1))
            print(f"   P_single = {ps:.3e}; P_family (N_mech = {N_MECH_BEFORE + 1}) = {G1['P_family']:.3f}")
g1_verdict = g1_grade if GATES_OK else "NOT COMPLETED (gate failure: " + ", ".join(fails) + ")"
print(f"   G1 GRADE: {g1_verdict}")
G1["grade"] = g1_verdict
results["G1"] = G1
stamp("G1")

# ================================================================== (5) REPORTED VARIANTS: the declared option space (K = 72)
print("\n(5) THE DECLARED OPTION SPACE (K = 72): every variant graded by the frozen rule; only G1 counts")
CMODE = {"TT+sigma (alpha_T->0)": ("UG TT + sigma, alpha_T -> 0 (P-lin)", "UG TT + sigma, alpha_T -> 0 (P-exp)"),
         "TT only": ("UG TT only (P-lin)", "UG TT only (P-exp)"),
         "TT+sigma+xi (alpha_T=1)": ("UG 9 modes, alpha_T = 1 (P-lin)", "UG 9 modes, alpha_T = 1 (P-exp)")}
CG = {(cm, par): float(sp.simplify(at_fp_g(FG[CMODE[cm][0 if par == "P-lin" else 1]]) / gS)) for cm in CMODE for par in ("P-lin", "P-exp")}
rows5 = []
print("   measure  sigma-reg  modes/gauge               param   matching       g*        f_g          P          z      grade")
for meas, sreg, cm, par, mt in itertools.product(("M-eq", "M-naive"), ("CPR", "norm"), CMODE, ("P-lin", "P-exp"),
                                                 ("M_P one-loop", "M_P two-loop", "M_red one-loop")):
    flv = FLOWS[(meas, sreg)]
    row = dict(measure=meas, sigma_reg=sreg, modes=cm, param=par, matching=mt, g=flv["g"], adm=flv["adm"])
    if not flv["adm"]:
        row.update(grade="NOT DIAGNOSTIC (" + flv["why"] + ")")
    else:
        fv = CG[(cm, par)] * flv["g"]
        row["f_g"] = fv
        if fv <= 0:
            row.update(grade="NOT DIAGNOSTIC (f_g <= 0)")
        else:
            if mt == "M_P one-loop":
                Pv = C1.downstream_P(fv)
            elif mt == "M_P two-loop":
                Pv, _ = H4.two_loop_P(C1.gY_star_from_fg(fv), B2)
            else:
                Pv = H4.reduced_planck_P(fv)
            gr_, zz = grade_value(Pv)
            row.update(P=Pv, z=zz, grade=gr_)
    row["graded"] = (meas, sreg, cm, par, mt) == ("M-eq", "CPR", "TT+sigma (alpha_T->0)", "P-lin", "M_P one-loop")
    rows5.append(row)
    print(f"   {meas:8s} {sreg:9s}  {cm:25s} {par:7s} {mt:14s} {row['g']:.6f}  {fmt(row.get('f_g'), '.8f'):11s}  {fmt(row.get('P'), '.5f'):9s}"
          f"  {fmt(row.get('z'), '+.3f'):7s} {row['grade']}{'   <- G1 (graded)' if row['graded'] else ''}")
n_k = sum(1 for r_ in rows5 if r_["grade"] == "KILLED")
n_c = sum(1 for r_ in rows5 if r_["grade"] == "CONSISTENT")
n_nd = len(rows5) - n_k - n_c
Ps = [r_["P"] for r_ in rows5 if "P" in r_] or [float("nan")]
zs = [r_["z"] for r_ in rows5 if "z" in r_] or [float("nan")]
print(f"   {len(rows5)} variants: {n_k} KILLED, {n_c} CONSISTENT, {n_nd} NOT DIAGNOSTIC; P range {min(Ps):.3f} .. {max(Ps):.3f}; z range {min(zs):+.3f} .. {max(zs):+.3f}")
others_cons = [r_ for r_ in rows5 if (not r_["graded"]) and r_["grade"] == "CONSISTENT"]
others_kill = [r_ for r_ in rows5 if (not r_["graded"]) and r_["grade"] == "KILLED"]
if G1["grade"] == "KILLED":
    rule_d = "KILLED across the declared option space" if not others_cons else "KILLED (graded); the option space is not uniform"
elif G1["grade"] == "CONSISTENT":
    rule_d = "CONSISTENT (graded), option-space dependent" if others_kill else "CONSISTENT across the declared option space"
else:
    rule_d = "G1 not graded as KILLED/CONSISTENT: " + G1["grade"]
print(f"   RULE D (door-level statement): {rule_d}")
results["variants"] = rows5
results["rule_D"] = rule_d
results["variant_counts"] = dict(killed=n_k, consistent=n_c, not_diagnostic=n_nd, P_min=min(Ps), P_max=max(Ps), z_min=min(zs), z_max=max(zs))
stamp("variants")

# ================================================================== (6) MUTATE checks (the prediction moves as expected)
if MODE == "MUTATE_SIGN":
    print("\n(6) MUTATE_SIGN: matter traces x -1 in the AS3 reproduction and the unimodular flow")
    X1g = sp.nsimplify(sum(SECT[("M-eq", "CPR")].values()).subs(e_, 2))
    X1m_normal = sp.nsimplify(X1_MATTER)
    g_pred = float(-2 * sp.pi / (X1g - X1m_normal))
    okL = FLOWS[("M-eq", "CPR")]["g"] is not None and abs(FLOWS[("M-eq", "CPR")]["g"] - g_pred) <= 1e-12 * abs(g_pred)
    chk("L-SIGN (MUTATE check, must PASS)", okL, f"mutated g* = {FLOWS[('M-eq', 'CPR')]['g']:.6f} = -2 pi/(X1_grav {float(X1g):.5f} - X1_matter "
        f"{float(X1m_normal):.5f}) = {g_pred:.6f} (hand -2.25): no admissible fixed point, G1 -> NOT DIAGNOSTIC")
    results["L_SIGN"] = dict(g_mut=FLOWS[("M-eq", "CPR")]["g"], g_pred=g_pred, ok=okL)
if MODE == "MUTATE_SPLIT":
    print("\n(6) MUTATE_SPLIT: sigma kinetic block sign flipped (sigma treated as positive norm)")
    fsig_normal = FG["UG sigma only, unflipped (P-lin)"]
    okL = sp.simplify(fg_G1 - (fg_TT - fsig_normal)) == 0
    Pmut = C1.downstream_P(c_G1 * FLOWS[("M-eq", "CPR")]["g"]) if c_G1 > 0 else None
    chk("L-SPLIT (MUTATE check, must PASS)", okL, f"mutated graded f_g = f_TT - f_sigma(normal) exactly: {okL}; f_g/f_TT = "
        f"{sp.simplify(fg_G1 / fg_TT)} (hand 7/5); P -> {fmt(Pmut, '.5f')} (hand 91.9)")
    results["L_SPLIT"] = dict(ok=okL, f_over_fTT=str(sp.simplify(fg_G1 / fg_TT)), P_mut=Pmut)

# ================================================================== summary
print("\nSUMMARY")
print(f"   gates: {'all PASS' if GATES_OK else 'FAILED: ' + ', '.join(fails)}")
print(f"   G1: {G1['grade']}" + (f"  (P = {G1['P']:.5f}, z = {G1['z']:+.3f})" if "P" in G1 else ""))
print(f"   door-level (rule D): {rule_d}")
print(f"   N_mech: {N_MECH_BEFORE} -> {N_MECH_BEFORE + 1} (one graded trial). Alpha stays an INPUT; kappa = 1/2 FITTED; not theory closed.")
results["gates_failed"] = list(fails)
results["N_mech"] = [N_MECH_BEFORE, N_MECH_BEFORE + 1]
results["runtime_s"] = time.time() - T0
results["peak_rss_MB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576


def _js(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (sp.Basic,)):
        return str(o)
    return str(o)


suffix = "" if MODE == "NORMAL" else "_" + MODE
with open(HERE / f"cfg906_d04{suffix}.json", "w") as fh:
    json.dump(results, fh, indent=1, default=_js)
stamp("done")
sys.exit(1 if fails else 0)
