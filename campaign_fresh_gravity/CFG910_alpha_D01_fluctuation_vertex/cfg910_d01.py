"""CFG910: alpha door D01, f_g from the fluctuation photon-graviton vertex, SCOPED (semi-fluctuation closure F1).
Frozen criteria: CFG910_PREREGISTRATION.md (commit c849b27e4, committed alone before any script).

Usage (one core, < 900 MB, watchdog):
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg910_d01.py                 real run      -> exit 0 iff every required gate passes
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg910_d01.py MUTATE_VERTEX   W_A (zero-graviton-momentum aah vertex) sign flipped
                                                                          -> G-COV must FAIL (exit 1); G-BF must PASS
    OMP_NUM_THREADS=1 nice -n 10 python3 -B cfg910_d01.py MUTATE_GRAV     W_h (graviton-block h_c dependence) set to zero
                                                                          -> G-COV must FAIL (exit 1); G-BF must PASS
Graded trial G1: CPR gauge (rho = 0, Landau, kernel restriction), eta_h = -2, lambda_3 = lambda_2, g_4 = g_5 = g_3, one-loop at M_P.
K = 72 declared variants; the other 71 are reported, not graded.  N_mech 375 -> 376 if G1 yields a value.
Lanes AS1-AS4 and lane B are imported read-only (bytecode writing disabled); none of their files is edited.
kappa and Z enter nowhere. The SM mass sector is walled: no mass enters or is derived. Not theory closed."""
import sys
sys.dont_write_bytecode = True
import os
import time
import json
import random
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
import mpmath as mp                      # noqa: E402
import as2_common as A2                  # noqa: E402  AS2/AS3 CPR machinery (unchanged)
import as3_gcpr as G3                    # noqa: E402  AS3 heat kernels (unchanged)
import as4_systematics as H4             # noqa: E402  AS3/AS4 two-loop and reduced-Planck systematics (unchanged)

FG1 = A2.FG1                             # AS1 flat-space graviton-photon action (unchanged)
C1 = A2.C1
RG = C1.RG
MODE = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
assert MODE in ("NORMAL", "MUTATE_VERTEX", "MUTATE_GRAV"), MODE
SGN_WA = -1 if MODE == "MUTATE_VERTEX" else 1
WH_ON = 0 if MODE == "MUTATE_GRAV" else 1
OUTSTEM = "cfg910_d01" + ("" if MODE == "NORMAL" else "_" + MODE)
T0 = time.time()
TARGET = RG.ALPHA_INV0                   # 137.035999177, target only
Q = sp.Rational
N_MECH_BEFORE = 375
fails = []
results = {"mode": MODE, "prereg_commit": "c849b27e4"}


def chk(tag, ok, msg):
    print(("  [PASS] " if ok else "  [FAIL] ") + tag + "  " + msg)
    if not ok:
        fails.append(tag)
    results.setdefault("checks", {})[tag] = {"pass": bool(ok), "msg": msg}
    return bool(ok)


def stamp(label):
    print(f"   [{label}: {time.time() - T0:.1f} s, peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576:.0f} MB]")


def half_unit(printed):
    s_ = printed.lstrip("-")
    dec = len(s_.split(".")[1]) if "." in s_ else 0
    return 0.5 * 10.0**(-dec)


def close_printed(val, printed):
    return val is not None and abs(val - float(printed)) <= half_unit(printed) + 1e-15


print(f"MODE: {MODE}")
print(f"python {sys.version.split()[0]}, numpy {np.__version__}, sympy {sp.__version__}, scipy {scipy.__version__}, mpmath {mp.__version__}")

# ================================================================== (0) PRE-FLIGHT: frozen route error (CFG901's, record numbers)
REC = dict(two_loop=96.07582 - 95.57847, m_red=abs(93.82509 - 95.57847), y1=8.8e-4 * 137.036,
           scheme=abs(92.914 - 95.57847), trunc=abs(91.04527 - 96.37265))
SIGMA_ROUTE = float(np.sqrt(sum(v**2 for v in REC.values())))
SIGMA_ADM = float(np.sqrt(sum(v**2 for k, v in REC.items() if k != "trunc") + (95.57847 - 95.26961)**2))
print("\n(0) PRE-FLIGHT (rules section 1.6): route error frozen from the record (inherited from CFG901)")
print(f"   sigma_route = {SIGMA_ROUTE:.4f} (frozen 6.230); admissible-only variant {SIGMA_ADM:.4f} (frozen 3.245)")
chk("PF sigma_route", abs(SIGMA_ROUTE - 6.230) < 5e-4 and abs(SIGMA_ADM - 3.245) < 5e-4, "sigma_route and the admissible-only variant equal the frozen values")
results["preflight"] = dict(components=REC, sigma_route=SIGMA_ROUTE, sigma_admissible_only=SIGMA_ADM)

B3 = C1.laneB_b3()
B2 = C1._exec_lane_b_script("b2_required_boundary.py")
F_NEEDED = float(B3.f_needed)


def P_of(fg):
    return C1.downstream_P(fg) if fg is not None and fg > 0 else None


def p_single(miss):
    m = abs(miss)
    lo = max(TARGET - m, 10.0)
    hi = min(TARGET + m, 1000.0)
    return float(np.log(hi / lo) / np.log(100.0))


# ================================================================== (1) G-REC: AS3 reproduced (AS2/AS3 code, SM content)
print("\n(1) GATE G-REC: AS3 CPR-EH with SM matter (AS2/AS3 code, imported read-only)")
SM = {A2.NS: Q(4), A2.ND: Q(45, 2), A2.NV: Q(12)}
HK = G3.heat_kernels()
XM_SYM, _ = A2.X_matter(HK)
XM_SM = sp.expand(XM_SYM.subs(SM))
XG1 = A2.X_gravity(HK, with_eta=True, order_f=1)
bet_k0 = A2.beta_system(XG1 + XM_SM, 1)
roots_k0, _, _ = A2.find_roots(bet_k0, 1, grid=True)


def fg_cpr_num(gt):
    f0, f1 = float(gt[0]), float(gt[1])
    return -5 * (8 * f0 + 4 * f1 - 2 * f1) / (1152 * np.pi**2 * (f0 + f1)**2)


rows_k0 = []
for r_ in roots_k0:
    glb = A2.to_glb(r_)
    dom, edge = A2.in_domain(glb)
    adm = A2.admissible(glb) and dom
    fgv = fg_cpr_num(r_)
    rows_k0.append(dict(gt=[float(x) for x in r_], glb=[float(x) for x in glb], adm=adm, fg=fgv, P=(P_of(fgv) if dom else None)))
adm_k0 = [x for x in rows_k0 if x["adm"]]
okrec = len(adm_k0) == 1 and close_printed(adm_k0[0]["glb"][0], "0.967159") and close_printed(adm_k0[0]["glb"][1], "-1.22293") \
    and close_printed(adm_k0[0]["fg"], "0.03883093") and close_printed(adm_k0[0]["P"], "95.57847")
chk("G-REC a: AS3 CPR-EH (SM)", okrec, (f"(g, lambda) = ({adm_k0[0]['glb'][0]:.7f}, {adm_k0[0]['glb'][1]:.6f}), f_g = {adm_k0[0]['fg']:.9f}, "
                                        f"P = {adm_k0[0]['P']:.6f}" if len(adm_k0) == 1 else f"{len(adm_k0)} admissible roots")
    + " vs (0.967159, -1.22293), 0.03883093, 95.57847")
if len(adm_k0) != 1:
    print("\nVERDICT: NOT COMPLETED (G-REC: no unique admissible background fixed point)")
    sys.exit(1)
GSTAR, LSTAR = adm_k0[0]["glb"]
FG_BF_CPR = adm_k0[0]["fg"]
P2l_rec, _ = H4.two_loop_P(C1.gY_star_from_fg(FG_BF_CPR), B2)
Pmr_rec = H4.reduced_planck_P(FG_BF_CPR)
chk("G-REC b: AS3 EH systematics (SM)", close_printed(P2l_rec, "96.07582") and close_printed(Pmr_rec, "93.82509"),
    f"two-loop {P2l_rec:.6f}, M_red {Pmr_rec:.6f} vs 96.07582, 93.82509")
g0ok = (abs(C1.downstream_P(B3.fg) - B3.c5) < 1e-9 and abs(C1.downstream_P(0.04795) / 92.914 - 1) < 1e-4
        and abs(C1.downstream_P(0.009805) / 137.036 - 1) < 1e-4 and abs(C1.downstream_P(B3.f_needed) - B3.c6) < 1e-9)
chk("G-DS downstream G0", g0ok, f"P(0.04795) = {C1.downstream_P(0.04795):.4f}, P(0.009805) = {C1.downstream_P(0.009805):.4f}, "
    f"P(f_needed = {F_NEEDED:.6f}) = {C1.downstream_P(F_NEEDED):.6f}")
results["background_fixed_point"] = dict(g=GSTAR, lam=LSTAR, fg_BF_CPR=FG_BF_CPR, P_BF=adm_k0[0]["P"], two_loop=P2l_rec, m_red=Pmr_rec)
stamp("G-REC")

# ================================================================== (2) MACHINERY
print("\n(2) MACHINERY: flat background + constant h_c (zero-momentum graviton) + constant F-bar; fields h (10) + a (4); q = kappa q-hat")
I_ = sp.I
kap, lam, eta, xi, ee, agf = FG1.kap, FG1.lam, FG1.eta, FG1.xi, FG1.e, FG1.agf      # AS1's symbols (lam = lambda_2, eta = eta_h)
L3 = sp.Symbol("lambda_3", real=True)
D1, D2 = sp.symbols("d1 d2", positive=True)       # d1 = 1/(1 - 2 lambda_2), d2 = 1/(1 - 4 lambda_2/3)
EPS = sp.Symbol("eps")
pairs = FG1.pairs
Hm_, hm = FG1.hmat("hm")
Hp_, hp = FG1.hmat("hp")
am = list(sp.symbols("am0:4"))
ap = list(sp.symbols("ap0:4"))
PHM = list(hm) + am
PHP = list(hp) + ap
NF = 14
ZN = 1 / (16 * sp.pi)                              # g_h = 1 in the propagator normalisation (it cancels in every class)
E4 = [0, 0, 0, 1]
I4 = sp.eye(4)
idx = {pq: i for i, pq in enumerate(pairs)}


def bil2mat(B):
    """Matrix M_ij = d^2 B / d Phi-_i d Phi+_j of a bilinear form B(Phi-, Phi+)."""
    B = sp.expand(B)
    M = sp.zeros(NF, NF)
    pos_m = {s_: i for i, s_ in enumerate(PHM)}
    pos_p = {s_: i for i, s_ in enumerate(PHP)}
    for term in sp.Add.make_args(B):
        if term == 0:
            continue
        c, fac = term.as_coeff_mul()
        im = ip = None
        rest = c
        for f_ in fac:
            if f_ in pos_m:
                assert im is None
                im = pos_m[f_]
            elif f_ in pos_p:
                assert ip is None
                ip = pos_p[f_]
            else:
                rest = rest * f_
        assert im is not None and ip is not None, f"non-bilinear term {term}"
        M[im, ip] += rest
    return M


def tr4(X, Gm):
    return sum(Gm[m, n] * X[m, n] for m in range(4) for n in range(4))


def dot4(X, Y, Gm):     # X:Y with indices raised by Gm
    return (X * Gm * Y.T * Gm).trace()


def eh_bil(X, Y, Gm, sqg, qv, s):
    """-(sqrt g R)^(2) polarised (AS1 form), on a constant metric with inverse Gm and density sqg; q_a q_b = s qv_a qv_b."""
    Gq = [sum(Gm[m, a] * qv[a] for a in range(4)) for m in range(4)]
    q2 = s * sum(qv[a] * Gq[a] for a in range(4))
    trX, trY = tr4(X, Gm), tr4(Y, Gm)
    v1 = [sum(Gq[m] * X[m, r] for m in range(4)) for r in range(4)]
    v2 = [sum(Gq[n] * Y[n, c] for n in range(4)) for c in range(4)]
    t1 = Q(1, 4) * q2 * trX * trY
    t2 = -Q(1, 4) * q2 * dot4(X, Y, Gm)
    t3 = Q(1, 2) * s * sum(v1[r] * Gm[r, c] * v2[c] for r in range(4) for c in range(4))
    t4 = -Q(1, 2) * s * trX * sum(Gq[m] * Gq[n] * Y[m, n] for m in range(4) for n in range(4))
    return -sqg * (t1 + t2 + t3 + t4)


def mass_bil(X, Y, Gm, sqg):
    return sqg * (tr4(X, Gm) * tr4(Y, Gm) / 8 - dot4(X, Y, Gm) / 4)


def gf_fdd_bil(Xm, Xp, Gm, sqg, qv, s):
    """(Z_N a_gf/2) sqrt g G^{mu nu} F_mu F_nu, F_mu = G^{nu rho} q_rho X_{nu mu} - (1/2) q_mu tr X (beta = 1), d -> -/+ i q."""
    Gq = [sum(Gm[m, a] * qv[a] for a in range(4)) for m in range(4)]
    def F(X, sg):
        trX = tr4(X, Gm)
        return [sg * I_ * (sum(Gq[n] * X[n, mu] for n in range(4)) - Q(1, 2) * qv[mu] * trX) for mu in range(4)]
    Fm, Fp = F(Xm, -1), F(Xp, +1)
    return agf / 2 * s * sqg * sum(Gm[m, n] * Fm[m] * Fp[n] for m in range(4) for n in range(4))


def fhat(a, qv, sg):
    return sp.Matrix(4, 4, lambda m, n: sg * I_ * (qv[m] * a[n] - qv[n] * a[m]))


def TFF(Gm, sqg, A, B):
    return sqg * (A.T * Gm * B * Gm).trace()


def photon_bil(Gm, sqg, qv, s, xi_v):
    fm, fp = fhat(am, qv, -1), fhat(ap, qv, +1)
    Gq = [sum(Gm[m, a] * qv[a] for a in range(4)) for m in range(4)]
    gfm = sum(-I_ * Gq[m] * am[m] for m in range(4))
    gfp = sum(I_ * Gq[m] * ap[m] for m in range(4))
    return Q(1, 4) * s * TFF(Gm, sqg, fm, fp), 1 / (2 * xi_v) * s * sqg * gfm * gfp


def eps_coeffs(M, order=1):
    """Split a matrix with entries polynomial in EPS into its EPS^0 and EPS^1 coefficients."""
    M = M.applyfunc(sp.expand)
    return [M.applyfunc(lambda x: x.coeff(EPS, k)) for k in range(order + 1)]


# ---- graded (eps, ep) algebra for the Maxwell vertex expansion: X = eps H_c + ep H, truncated at eps^1, ep^2
def gmul(A, B):
    out = {}
    for ka, Am in A.items():
        for kb, Bm in B.items():
            k = (ka[0] + kb[0], ka[1] + kb[1])
            if k[0] <= 1 and k[1] <= 2:
                out[k] = out[k] + Am * Bm if k in out else Am * Bm
    return out


def gadd(*terms):
    out = {}
    for c, A in terms:
        for k, Am in A.items():
            out[k] = out[k] + c * Am if k in out else c * Am
    return out


def gtrace(A):
    return {k: Am.trace() for k, Am in A.items()}


def metric_graded(Hc, H):
    X = {}
    if Hc is not None:
        X[(1, 0)] = Hc
    if H is not None:
        X[(0, 1)] = H
    one = {(0, 0): I4}
    X2 = gmul(X, X)
    X3 = gmul(X2, X)
    ginv = gadd((1, one), (-1, X), (1, X2), (-1, X3))
    ell = gadd((1, gtrace(X)), (Q(-1, 2), gtrace(X2)), (Q(1, 3), gtrace(X3)))
    one_s = {(0, 0): sp.Integer(1)}
    ell2 = gmul(ell, ell)
    ell3 = gmul(ell2, ell)
    sqg = gadd((1, one_s), (Q(1, 2), ell), (Q(1, 8), ell2), (Q(1, 48), ell3))
    return ginv, sqg


def TFF_graded(ginv, sqg, A, B):
    """sqrt g g^{ma} g^{nb} A_mn B_ab with graded metric pieces; A, B graded matrices."""
    t = gmul(gmul(gmul({k: v.T for k, v in A.items()}, ginv), B), ginv)
    t = gtrace(t)
    return gmul(sqg, t)


def vertex_blocks(Hc, Fb, qv_graded):
    """V1, U1 (F-bar h a), V2, U2 (F-bar F-bar h h) as matrices; q = kappa * qv (graded in eps for the covariant mode)."""
    FbG = {(0, 0): Fb}
    def fgr(avec, sg):
        out = {}
        for k, qv in qv_graded.items():
            out[k] = kap * fhat(avec, qv, sg)
        return out
    BV1 = {0: 0, 1: 0}
    for H, avec, sg in ((Hm_, ap, +1), (Hp_, am, -1)):
        ginv, sqg = metric_graded(Hc, H)
        T = TFF_graded(ginv, sqg, FbG, fgr(avec, sg))
        for e_ in (0, 1):
            BV1[e_] += Q(1, 4) * T.get((e_, 1), 0)
    BV2 = {0: 0, 1: 0}
    for H, c in ((Hm_ + Hp_, 1), (Hm_, -1), (Hp_, -1)):
        ginv, sqg = metric_graded(Hc, H)
        T = TFF_graded(ginv, sqg, FbG, FbG)
        for e_ in (0, 1):
            BV2[e_] += c * Q(1, 8) * T.get((e_, 2), 0)
    return bil2mat(BV1[0]), bil2mat(BV1[1]), bil2mat(BV2[0]), bil2mat(BV2[1])


# ---- h_c = 0 kinetic pieces (flat background delta), shared by both modes
def base_blocks(lam_v, xi_v, gauge):
    """M0 (regulated, s = 1), the kinetic-only graviton block Mkin_hh (EH + GF, s = 1), and the photon block Mkin_aa (s = 1)."""
    Bh = ZN * (Q(1, 2) * (eh_bil(Hm_, Hp_, I4, 1, E4, 1) + eh_bil(Hp_, Hm_, I4, 1, E4, 1)))
    if gauge == "FdD":
        Bh += ZN * gf_fdd_bil(Hm_, Hp_, I4, 1, E4, 1).subs(agf, 1)
    Bm = ZN * 2 * lam_v * mass_bil(Hm_, Hp_, I4, 1)
    Bk, Bg = photon_bil(I4, 1, E4, 1, xi_v)
    Mkin_hh = bil2mat(Bh)
    Mkin_aa = bil2mat(Bk + Bg)
    return Mkin_hh + bil2mat(Bm) + Mkin_aa, Mkin_hh, Mkin_aa


def hv(d):
    v = [0] * NF
    for (m, n), c in d.items():
        v[idx[(min(m, n), max(m, n))]] += c
    return v


TT_COLS = [hv({(0, 1): 1}), hv({(0, 2): 1}), hv({(1, 2): 1}), hv({(0, 0): 1, (1, 1): -1}), hv({(0, 0): 1, (1, 1): 1, (2, 2): -2})]
TRACE_COL = [hv({(0, 0): 1, (1, 1): 1, (2, 2): 1, (3, 3): 1})]          # CPR (rho = 0) kernel scalar
LDD_COL = [hv({(0, 0): 1, (1, 1): 1, (2, 2): 1, (3, 3): 3})]            # beta = 1 kernel scalar
PHOT_COLS = [[0] * 10 + [1 if j == k else 0 for j in range(4)] for k in range(4)]
EMAT = {"CPR": sp.Matrix(TT_COLS + TRACE_COL + PHOT_COLS).T, "LdD": sp.Matrix(TT_COLS + LDD_COL + PHOT_COLS).T, "FdD": sp.eye(NF)}
NGRAV = {"CPR": 6, "LdD": 6, "FdD": 10}


def restrict(M, gauge):
    E = EMAT[gauge]
    return M if gauge == "FdD" else sp.Matrix(E.T * M * E)


def to_d(expr):
    """Rewrite a rational function of lambda_2 with simple poles at 1/2 and 3/4 as a polynomial in d1, d2."""
    expr = sp.together(expr)
    if expr == 0:
        return sp.Integer(0)
    out = 0
    for term in sp.Add.make_args(sp.apart(expr, lam)):
        num, den = sp.fraction(sp.factor(term))
        pd = sp.Poly(den, lam)
        if pd.degree() == 0:
            out += term
            continue
        assert pd.degree() == 1, f"unexpected pole structure {term}"
        root = sp.solve(den, lam)[0]
        lc = pd.LC()
        if root == Q(1, 2):
            out += num / lc * (-2 * D1)                 # 1/(lam - 1/2) = -2 d1
        elif root == Q(3, 4):
            out += num / lc * (-Q(4, 3) * D2)          # 1/(lam - 3/4) = -(4/3) d2
        else:
            raise AssertionError(f"unexpected pole {root}")
    return sp.expand(out)


DSUB = {D1: 1 / (1 - 2 * lam), D2: 1 / (1 - 4 * lam / 3)}


def propagator(M0r, gauge, lam_v):
    """G = (M0r)^-1 (block diagonal graviton/photon).  Symbolic lambda: entries rewritten as polynomials in d1, d2 (checked)."""
    ng = NGRAV[gauge]
    n = M0r.shape[0]
    G = sp.zeros(n, n)
    Gh = M0r[:ng, :ng].inv()
    Ga = M0r[ng:, ng:].inv()
    if isinstance(lam_v, sp.Symbol):
        Gh = Gh.applyfunc(to_d)
        chk_ = (Gh.subs(DSUB) * M0r[:ng, :ng]).applyfunc(sp.simplify)
        assert chk_ == sp.eye(ng), "d-rewriting of the propagator failed"
    G[:ng, :ng] = Gh
    G[ng:, ng:] = Ga.applyfunc(sp.simplify)
    return G


def radial(expr):
    """int_0^1 kappa^3 dkappa/(8 pi^2) of a polynomial in kappa."""
    expr = sp.expand(expr)
    if expr == 0:
        return sp.Integer(0)
    p = sp.Poly(expr, kap)
    return sp.expand(sum(c / ((mon[0] + 4) * 8 * sp.pi**2) for mon, c in p.terms()))


# ---- invariants for the joint-rotation average (n = e_4, index 3)
def invariants(Hc, Fb):
    FF = sum(Fb[m, n]**2 for m in range(4) for n in range(4))
    trh = Hc.trace()
    A2_ = sum(Hc[a, b] * Fb[a, c] * Fb[b, c] for a in range(4) for b in range(4) for c in range(4))
    nFFn = sum(Fb[3, c]**2 for c in range(4))
    nhn = Hc[3, 3]
    B3_ = sum(Hc[3, b] * Fb[b, c] * Fb[3, c] for b in range(4) for c in range(4))
    B4_ = sum(Fb[3, a] * Hc[a, b] * Fb[3, b] for a in range(4) for b in range(4))
    return [trh * FF, A2_, trh * nFFn, nhn * FF, B3_, B4_, nhn * nFFn]


def inv2(Fb):
    return [sum(Fb[m, n]**2 for m in range(4) for n in range(4)), sum(Fb[3, c]**2 for c in range(4))]


def make_configs(n, seed):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        Hc = sp.zeros(4, 4)
        for m in range(4):
            for k in range(m, 4):
                v = Q(rng.randint(-6, 6), rng.randint(1, 4))
                Hc[m, k] = v
                Hc[k, m] = v
        Fb = sp.zeros(4, 4)
        for m in range(4):
            for k in range(m + 1, 4):
                v = Q(rng.randint(-6, 6), rng.randint(1, 4))
                Fb[m, k] = v
                Fb[k, m] = -v
        out.append((Hc, Fb))
    return out


CONFIGS = make_configs(9, 910)
PREF = sp.diag(-1, 1, 1, 1)
CONFIG_REFL = (PREF * CONFIGS[0][0] * PREF, PREF * CONFIGS[0][1] * PREF)
MINV = sp.Matrix([invariants(*c) for c in CONFIGS[:7]])
assert MINV.rank() == 7, "invariant matrix of the 7 fit configurations is singular"
results["configs_seed"] = 910


def per_config_mats(Hc, Fb, mode, lam_v, lam3_v, eta_v, xi_v):
    """All 14x14 matrices for one configuration.  mode 'fl' (delta regulator and gauge fixing) or 'cov' (FdD, g_c everywhere)."""
    if mode == "fl":
        qv_gr = {(0, 0): E4}
        V1, U1, V2, U2 = vertex_blocks(Hc, Fb, qv_gr)
        Gm = I4 - EPS * Hc
        sqg = 1 + EPS * Hc.trace() / 2
        Bh_k = ZN * Q(1, 2) * (eh_bil(Hm_, Hp_, Gm, sqg, E4, kap**2) + eh_bil(Hp_, Hm_, Gm, sqg, E4, kap**2))
        Bh_m = ZN * 2 * lam3_v * mass_bil(Hm_, Hp_, Gm, sqg)
        Wh = eps_coeffs(bil2mat(Bh_k + Bh_m))[1]
        Bk, _ = photon_bil(Gm, sqg, E4, kap**2, xi_v)
        WA = eps_coeffs(bil2mat(Bk))[1]
        z = sp.zeros(NF, NF)
        return dict(V1=V1, U1=U1, V2=V2, U2=U2, Wh=WH_ON * Wh, WA=SGN_WA * WA, dR1h=z, dR1a=z, mu=0)
    # covariant mode (FdD only): q-hat_c = g_c^{1/2} e_4, regulator, gauge fixings and measure built with g_c
    qc = [E4[a] + EPS * Hc[a, 3] / 2 for a in range(4)]
    V1, U1, V2, U2 = vertex_blocks(Hc, Fb, {(0, 0): E4, (1, 0): [Hc[a, 3] / 2 for a in range(4)]})
    Gm = I4 - EPS * Hc
    sqg = 1 + EPS * Hc.trace() / 2
    Bh_kin = ZN * (Q(1, 2) * (eh_bil(Hm_, Hp_, Gm, sqg, qc, 1) + eh_bil(Hp_, Hm_, Gm, sqg, qc, 1))
                   + gf_fdd_bil(Hm_, Hp_, Gm, sqg, qc, 1).subs(agf, 1))
    Bh_m = ZN * 2 * lam_v * mass_bil(Hm_, Hp_, Gm, sqg)
    Bk, Bg = photon_bil(Gm, sqg, qc, 1, xi_v)
    Mkh = eps_coeffs(bil2mat(Bh_kin))[1]
    Mkm = eps_coeffs(bil2mat(Bh_m))[1]
    Mka = eps_coeffs(bil2mat(Bk + Bg))[1]
    Wh = Mkh + Mkm
    WA = Mka
    dR1h = 2 * Mkh - eta_v * (1 - kap**2) * Mkh
    dR1a = 2 * Mka
    return dict(V1=V1, U1=U1, V2=V2, U2=U2, Wh=WH_ON * Wh, WA=SGN_WA * WA, dR1h=WH_ON * dR1h, dR1a=SGN_WA * dR1a, mu=Hc.trace() / 2)


def class_traces(m, G, S, gauge):
    """Two-point classes and the vertex classes (section 5.3 of the pre-registration), integrands in kappa."""
    R = {k: (restrict(v, gauge) if isinstance(v, sp.MatrixBase) else v) for k, v in m.items()}
    V1, U1, V2, U2, Wh, WA = R["V1"], R["U1"], R["V2"], R["U2"], R["Wh"], R["WA"]
    S1h = G * R["dR1h"] * G
    S1a = G * R["dR1a"] * G
    mu = R["mu"]
    GV1 = G * V1
    V1GV1 = V1 * GV1
    t_v1v1 = (V1GV1 * S).trace()
    t_v2 = (V2 * S).trace()
    out = {}
    out["2pt_V1V1"] = Q(1, 2) * t_v1v1
    out["2pt_V2"] = -Q(1, 2) * t_v2
    out["g5"] = -Q(1, 2) * (U2 * S).trace()
    out["g4h"] = Q(1, 2) * ((V2 * G * Wh * S).trace() + (Wh * G * V2 * S).trace()) - Q(1, 2) * (V2 * S1h).trace()
    out["g4"] = Q(1, 2) * ((U1 * GV1 * S).trace() + (V1 * G * U1 * S).trace()) + mu * (-Q(1, 2) * t_v2)
    def triple(W):
        GW = G * W
        return (V1GV1 * GW * S).trace() + (V1 * GW * GV1 * S).trace() + (W * GV1 * GV1 * S).trace()
    out["g3h"] = -Q(1, 2) * triple(Wh) + Q(1, 2) * (V1GV1 * S1h).trace()
    out["g3"] = -Q(1, 2) * triple(WA) + Q(1, 2) * (V1GV1 * S1a).trace() + mu * Q(1, 2) * t_v1v1
    return out


def setup_gauge(gauge, lam_v, xi_v, eta_v):
    M0, Mkh, Mka = base_blocks(lam_v, xi_v, gauge)
    dR0 = 2 * (Mkh + Mka) - eta_v * (1 - kap**2) * Mkh
    M0r, dR0r = restrict(M0, gauge), restrict(dR0, gauge)
    G = propagator(M0r, gauge, lam_v)
    S = (G * dR0r * G).applyfunc(sp.expand)
    return G, S, M0r, dR0r


VCLASSES = ["g5", "g4h", "g4", "g3h", "g3"]


def fit_vertex(vals):
    """vals: list of 9 (+1 reflected) radial-integrated values.  Returns (c_A, c_B, fit residual ok, parity ok, coefficients)."""
    c = MINV.LUsolve(sp.Matrix(vals[:7]))
    res_ok = all(sp.simplify(sum(ci * mi for ci, mi in zip(c, invariants(*CONFIGS[j]))) - vals[j]) == 0 for j in (7, 8))
    par_ok = sp.simplify(vals[9] - vals[0]) == 0
    cA = c[0] + (c[2] + c[3]) / 4 + c[6] / 24
    cB = c[1] + (c[4] + c[5]) / 4 + c[6] / 12
    return sp.simplify(cA), sp.simplify(cB), res_ok, par_ok


def fit_2pt(vals):
    """2-point: d1 F:F + d2 nFFn from configs 0, 1; check 2..8 and the reflected config."""
    M2 = sp.Matrix([inv2(CONFIGS[j][1]) for j in (0, 1)])
    d = M2.LUsolve(sp.Matrix([vals[0], vals[1]]))
    res_ok = all(sp.simplify(d[0] * inv2(CONFIGS[j][1])[0] + d[1] * inv2(CONFIGS[j][1])[1] - vals[j]) == 0 for j in range(2, 9))
    par_ok = sp.simplify(vals[9] - vals[0]) == 0
    return sp.simplify(d[0] + d[1] / 4), res_ok, par_ok


def run_classes(mode, gauge, lam_v, lam3_v, eta_v, xi_v, label):
    G, S, _, _ = setup_gauge(gauge, lam_v, xi_v, eta_v)
    allc = CONFIGS + [CONFIG_REFL]
    vals = {k: [] for k in ["2pt_V1V1", "2pt_V2"] + VCLASSES}
    for Hc, Fb in allc:
        m = per_config_mats(Hc, Fb, mode, lam_v, lam3_v, eta_v, xi_v)
        tr_ = class_traces(m, G, S, gauge)
        for k, v in tr_.items():
            if isinstance(lam_v, sp.Symbol):
                v = sp.expand(v)
            vals[k].append(radial(v))
    out = {}
    okfit = okpar = True
    for k in ("2pt_V1V1", "2pt_V2"):
        c0, rok, pok = fit_2pt(vals[k])
        out[k] = c0
        okfit &= rok
        okpar &= pok
    for k in VCLASSES:
        cA, cB, rok, pok = fit_vertex(vals[k])
        out[k] = (cA, cB)
        okfit &= rok
        okpar &= pok
    imag_ok = all(sp.simplify(sp.im(sp.expand(x if not isinstance(x, tuple) else x[0] + 7 * x[1]))) == 0
                  for x in out.values()) if not isinstance(lam_v, sp.Symbol) else True
    stamp(label)
    return out, okfit, okpar, imag_ok


# ================================================================== (3) G-VTX: the builder vs AS1 at h_c = 0
print("\n(3) GATE G-VTX: vertex builder and EH block at h_c = 0 vs AS1's bilinear action (FdD, a_gf = 1, g = 1, e = 1)")
s_ = sp.Symbol("s", positive=True)
B_as1, V1_as1, V2_as1, _, _, _, _ = FG1.bilinear_action(s_)
sub_as1 = {FG1.g: 1, ee: 1, agf: 1}
Mk_as1 = bil2mat(B_as1.subs(sub_as1))
M1_as1 = bil2mat(V1_as1.subs(sub_as1))
M2_as1 = bil2mat(V2_as1.subs(sub_as1))
Bh_mine = ZN * (Q(1, 2) * (eh_bil(Hm_, Hp_, I4, 1, E4, s_) + eh_bil(Hp_, Hm_, I4, 1, E4, s_)) + gf_fdd_bil(Hm_, Hp_, I4, 1, E4, s_).subs(agf, 1)
                + 2 * lam * mass_bil(Hm_, Hp_, I4, 1))
Bk_, Bg_ = photon_bil(I4, 1, E4, s_, xi)
Mk_mine = bil2mat(Bh_mine + Bk_ + Bg_)
FbS = FG1.Fbar_matrix()
V1m, U1m, V2m, U2m = vertex_blocks(None, FbS, {(0, 0): E4})
ok_vtx = (sp.simplify(Mk_mine - Mk_as1) == sp.zeros(NF, NF) and sp.expand(V1m - M1_as1) == sp.zeros(NF, NF)
          and sp.expand(V2m - M2_as1) == sp.zeros(NF, NF))
chk("G-VTX", ok_vtx, "kinetic matrix (EH + Lambda + FdD gauge fixing + photon), V1 and V2 equal AS1's exactly (symbolic s, lambda, xi, F-bar)")
stamp("G-VTX")

# ================================================================== (4) G-BF: the door's gate, background-field limit of the two-point function
print("\n(4) GATE G-BF (door's gate): background-field limit g_3 = g_4 = g, mu_h = -2 lambda, eta_h = eta_N; two-point f_g = 2 c_0, exact")
FG_BF_EXPECT = {"CPR": 5 * (eta - 16 * lam + 4) / (72 * sp.pi * (1 - 2 * lam)**2),
                "LdD": (eta - 16 * lam + 4) / (16 * sp.pi * (1 - 2 * lam)**2),
                "FdD": (eta - 16 * lam + 4) / (8 * sp.pi * (1 - 2 * lam)**2)}
FG_SPLIT = {}
GBF_OK = {}
for gauge in ("CPR", "LdD", "FdD"):
    G, S, _, _ = setup_gauge(gauge, lam, xi, eta)
    vals = {"2pt_V1V1": [], "2pt_V2": []}
    for Hc, Fb in CONFIGS + [CONFIG_REFL]:
        V1, _, V2, _ = vertex_blocks(None, Fb, {(0, 0): E4})
        V1r, V2r = restrict(V1, gauge), restrict(V2, gauge)
        vals["2pt_V1V1"].append(radial(sp.expand((Q(1, 2) * (V1r * G * V1r * S).trace()).subs(DSUB))))
        vals["2pt_V2"].append(radial(sp.expand((-Q(1, 2) * (V2r * S).trace()).subs(DSUB))))
    c_l, ok1, pk1 = fit_2pt(vals["2pt_V1V1"])
    c_t, ok2, pk2 = fit_2pt(vals["2pt_V2"])
    fg_bf = sp.factor(sp.simplify(2 * (c_l + c_t)))
    diff = sp.simplify(fg_bf - FG_BF_EXPECT[gauge])
    xi_free = sp.simplify(sp.diff(fg_bf, xi)) == 0
    GBF_OK[gauge] = chk(f"G-BF {gauge}", diff == 0 and xi_free and ok1 and ok2 and pk1 and pk2,
                        f"f_g^BF = {fg_bf}  (expected {sp.factor(FG_BF_EXPECT[gauge])}; difference {diff}); xi-free {xi_free}; fit {ok1 and ok2}; parity {pk1 and pk2}")
    FG_SPLIT[gauge] = (sp.factor(sp.simplify(2 * c_l)), sp.factor(sp.simplify(2 * c_t)))
    print(f"      split: loop [V1V1] 2c_0 = {FG_SPLIT[gauge][0]};  tadpole [V2] 2c_0 = {FG_SPLIT[gauge][1]}")
    stamp(f"G-BF {gauge}")
as3form = sp.simplify(FG_BF_EXPECT["CPR"].subs(eta, -2) - 5 * (1 - 8 * lam) / (36 * sp.pi * (1 - 2 * lam)**2))
chk("G-BF CPR = AS3 at eta_N = -2", as3form == 0, "5 (eta - 16 lambda + 4)/(72 pi (1 - 2 lambda)^2) at eta = -2 equals AS3's 5 (1 - 8 lambda)/(36 pi (1 - 2 lambda)^2)")
results["G_BF"] = {g_: dict(loop=str(FG_SPLIT[g_][0]), tadpole=str(FG_SPLIT[g_][1])) for g_ in FG_SPLIT}

# ================================================================== (5) G-EXP: perturbative bookkeeping vs 50-digit finite differences
print("\n(5) GATE G-EXP: f^2 eps coefficient of (1/2) Tr[(M0 + X)^-1 d_t R_k] by 60-digit finite differences vs the expansion (kappa = 1/2)")
mp.mp.dps = 60
PT = {lam: Q(-1, 2), L3: Q(1, 3), eta: Q(1, 2), xi: Q(2), kap: Q(1, 2)}


def _mpc(x):
    v = sp.N(x, 70)
    re_, im_ = v.as_real_imag()
    return mp.mpc(mp.mpf(str(sp.N(re_, 70))), mp.mpf(str(sp.N(im_, 70))))


def to_mp(M):
    return mp.matrix([[_mpc(M[i, j].subs(PT)) for j in range(M.shape[1])] for i in range(M.shape[0])])


GEXP_OK = True
for gauge in ("FdD", "CPR"):
    G, S, M0r, dR0r = setup_gauge(gauge, PT[lam], PT[xi], PT[eta])
    Hc, Fb = CONFIGS[0]
    m = per_config_mats(Hc, Fb, "fl", PT[lam], PT[L3], PT[eta], PT[xi])
    tr_ = class_traces(m, G, S, gauge)
    exp_vertex = sp.N(sum(tr_[k] for k in VCLASSES).subs(PT), 50)
    exp_2pt = sp.N((tr_["2pt_V1V1"] + tr_["2pt_V2"]).subs(PT), 50)
    R_ = {k: restrict(v, gauge) for k, v in m.items() if isinstance(v, sp.MatrixBase)}
    M0n, dRn = to_mp(M0r), to_mp(dR0r)
    V1n, V2n, U1n, U2n = to_mp(R_["V1"]), to_mp(R_["V2"]), to_mp(R_["U1"]), to_mp(R_["U2"])
    Wn = to_mp(R_["Wh"] + R_["WA"])

    def T(e_, f_):
        Mt = M0n + f_ * V1n + f_**2 * V2n + e_ * Wn + f_ * e_ * U1n + f_**2 * e_ * U2n
        return mp.re(sum((mp.inverse(Mt) * dRn)[i, i] for i in range(Mt.rows)) / 2)
    h = mp.mpf("1e-12")

    def D2f(e_):
        return (T(e_, h) - 2 * T(e_, 0) + T(e_, -h)) / h**2
    fd_vertex = (D2f(h) - D2f(-h)) / (2 * h) / 2
    fd_2pt = D2f(0) / 2
    rel_v = abs(fd_vertex - mp.mpf(str(sp.re(exp_vertex)))) / abs(fd_vertex)
    rel_2 = abs(fd_2pt - mp.mpf(str(sp.re(exp_2pt)))) / abs(fd_2pt)
    ok_ = rel_v < 1e-12 and rel_2 < 1e-12 and abs(sp.im(exp_vertex)) < 1e-40
    GEXP_OK &= chk(f"G-EXP {gauge}", ok_, f"vertex: FD {mp.nstr(fd_vertex, 15)} vs expansion {sp.N(sp.re(exp_vertex), 15)} (rel {mp.nstr(rel_v, 3)}); "
                   f"two-point: FD {mp.nstr(fd_2pt, 15)} vs {sp.N(sp.re(exp_2pt), 15)} (rel {mp.nstr(rel_2, 3)})")
stamp("G-EXP")

# ================================================================== (6) G-COV: covariant regulator -> Delta = 0 identically (FdD), and PC2
print("\n(6) GATE G-COV (FdD): regulator, gauge fixings and measure built with g_c = delta + h_c -> c_A = c_0/2, c_B = -2 c_0 (identities in lambda, eta)")
COV = {}
gcov_ok = True
for xv in (Q(1), Q(2)):
    out, okfit, okpar, _ = run_classes("cov", "FdD", lam, lam, eta, xv, f"G-COV classes xi = {xv}")
    c0 = sp.simplify((out["2pt_V1V1"] + out["2pt_V2"]).subs(DSUB))
    cA = sp.simplify(sum(out[k][0] for k in VCLASSES).subs(DSUB))
    cB = sp.simplify(sum(out[k][1] for k in VCLASSES).subs(DSUB))
    dA = sp.simplify(cA - c0 / 2)
    dB = sp.simplify(cB + 2 * c0)
    ok_ = dA == 0 and dB == 0 and okfit and okpar
    gcov_ok &= chk(f"G-COV xi = {xv}", ok_, f"c_0 = {sp.factor(c0)}; c_A - c_0/2 = {sp.factor(dA)}; c_B + 2 c_0 = {sp.factor(dB)}; fit {okfit}; parity {okpar}")
    COV[str(xv)] = {k: ((sp.simplify(v[0].subs(DSUB)), sp.simplify(v[1].subs(DSUB))) if isinstance(v, tuple) else sp.simplify(v.subs(DSUB)))
                    for k, v in out.items()}
results["G_COV"] = {k: {kk: str(vv) for kk, vv in v.items()} for k, v in COV.items()}


# ---- closure solver (section 5.5)
MONO = {  # coupling monomial of each vertex class relative to the tree aah vertex, as (power of x = sqrt(g_3), power of G = g_h3)
    "U": {"g5": (2, 0), "g4h": (1, Q(1, 2)), "g4": (2, 0), "g3h": (1, Q(1, 2)), "g3": (2, 0), "2pt_V1V1": (2, 0), "2pt_V2": (2, 0)},
    "Uprime": {"g5": (-1, Q(3, 2)), "g4h": (-1, Q(3, 2)), "g4": (0, 1), "g3h": (1, Q(1, 2)), "g3": (2, 0), "2pt_V1V1": (2, 0), "2pt_V2": (0, 1)},
}


def closure_roots(cls, Gv, eta_v, ident, matter=0):
    """cls: dict class -> c_0 (2pt) or c_B (vertex) as floats.  beta_g3/g_3 = 2 + eta_h + 2 Delta (+ 2 matter eta_A^matter).
    Delta = -2 f_g - 2 sum_class c_B * monomial;  f_g = 2 (c0_V1V1 m + c0_V2 m);  eta_A^matter = 2 f_g.  Returns admissible roots."""
    mono = MONO[ident]
    # polynomial in x after multiplying by x: collect coefficient of x^(p+1) for each term with monomial x^p G^q
    poly = {}
    def add(pw, c):
        poly[pw] = poly.get(pw, 0.0) + c
    add(1, 2.0 + eta_v)                                    # (2 + eta_h) * x
    fgterms = []
    for k in ("2pt_V1V1", "2pt_V2"):
        p_, q_ = mono[k]
        coef = 2 * cls[k] * Gv**float(q_)                  # f_g contribution: coef * x^p
        fgterms.append((p_, coef))
        add(p_ + 1, 2 * (-2) * coef)                       # 2 * Delta ⊃ 2 * (-2 f_g)
        add(p_ + 1, 2 * matter * 2 * coef)                 # matter probe: 2 * (+/- eta_A^matter), eta_A^matter = 2 f_g
    for k in VCLASSES:
        p_, q_ = mono[k]
        add(p_ + 1, 2 * (-2) * cls[k] * Gv**float(q_))
    pmin = min(poly)
    deg = max(poly) - pmin
    coeffs = [poly.get(pmin + deg - i, 0.0) for i in range(deg + 1)]
    rts = np.roots(coeffs) if deg > 0 else []
    out = []
    for r in rts:
        if abs(r.imag) < 1e-10 * max(1, abs(r)) and r.real > 1e-12:
            x = r.real
            fg = sum(c * x**p for p, c in fgterms)
            out.append(dict(x=x, g3=x * x, r=x * x / Gv, fg=fg, adm=fg > 0))
    return out, coeffs


def num_classes(out, subs):
    cls = {}
    for k, v in out.items():
        e_ = v[1] if isinstance(v, tuple) else v
        cls[k] = float(sp.N(e_.subs(subs)))
    return cls


# PC2: covariant-mode closure (FdD, U, eta_h = -2, lambda_3 = lambda_2) at the background point
pc2_cls = num_classes(COV["1"], {lam: LSTAR, eta: -2})
pc2_roots, _ = closure_roots(pc2_cls, GSTAR, -2.0, "U")
pc2_adm = [r for r in pc2_roots if r["adm"]]
chk("PC2 covariant closure r = 1", len(pc2_adm) == 1 and abs(pc2_adm[0]["r"] - 1) < 1e-9,
    f"admissible roots r = {[round(r['r'], 12) for r in pc2_adm]} (bookkeeping: block h_c dependence carries the block's 3-point coupling, "
    "the measure carries g_3; disclosed in the README)")
stamp("G-COV/PC2")

# ================================================================== (7) FLUCTUATION MODE at the background point: classes, G-XI, G-FIT, G-PAR
print("\n(7) FLUCTUATION MODE (delta regulator and gauge fixing): class coefficients at lambda_2 = lambda* (symbolic lambda_3, eta_h)")
LAM_RAT = sp.Rational(LSTAR).limit_denominator(10**12)
print(f"   lambda* = {LSTAR!r} -> rational {LAM_RAT} (difference {float(LAM_RAT) - LSTAR:.2e})")
FL = {}
for gauge in ("CPR", "LdD", "FdD"):
    per_xi = {}
    okall = True
    for xv in (Q(1), Q(2)):
        out, okfit, okpar, okim = run_classes("fl", gauge, LAM_RAT, L3, eta, xv, f"fl {gauge} xi = {xv}")
        per_xi[str(xv)] = out
        chk(f"G-FIT/G-PAR {gauge} xi = {xv}", okfit and okpar and okim, f"fit residual zero on 2 extra configs: {okfit}; reflected config identical: {okpar}; real: {okim}")
    same = all(sp.simplify((per_xi["1"][k][0] - per_xi["2"][k][0]) if isinstance(per_xi["1"][k], tuple) else (per_xi["1"][k] - per_xi["2"][k])) == 0
               and (not isinstance(per_xi["1"][k], tuple) or sp.simplify(per_xi["1"][k][1] - per_xi["2"][k][1]) == 0) for k in per_xi["1"])
    chk(f"G-XI {gauge}", same, "every class (two-point c_0, vertex c_A and c_B) identical at xi = 1 and xi = 2")
    FL[gauge] = per_xi["1"]
    # BF-limit consistency at this lambda: 2 (c0_V1V1 + c0_V2) equals the G-BF formula at lambda*
    fg_here = sp.N(2 * (FL[gauge]["2pt_V1V1"] + FL[gauge]["2pt_V2"]).subs(eta, -2), 15)
    fg_form = sp.N(FG_BF_EXPECT[gauge].subs({eta: -2, lam: LAM_RAT}), 15)
    print(f"   {gauge}: f_g^BF/g at lambda*, eta = -2: {fg_here} (G-BF formula {fg_form})")
    for k in VCLASSES:
        cA, cB = FL[gauge][k]
        print(f"      class {k:4s}: c_B = {sp.N(cB.subs(eta, -2), 10)} + lambda_3-part, full c_B(lambda_3, eta_h) = {sp.N(sp.expand(cB), 8)}")
results["fl_classes"] = {g_: {k: (str(v) if not isinstance(v, tuple) else [str(v[0]), str(v[1])]) for k, v in FL[g_].items()} for g_ in FL}

# ================================================================== (8) CLOSURES, GRADED TRIAL, VARIANTS
print("\n(8) CLOSURE F1 at the background point (g_h3, lambda_3, mu_h, eta_h) = (g*, lambda* or 0, -2 lambda*, -2 or 0)")
Ppl = P_of(F_NEEDED)
pc1 = abs(Ppl - TARGET) < 1e-6 and abs((Ppl - TARGET) / SIGMA_ROUTE) <= 3
chk("PC1 planted f_needed", pc1, f"P = {Ppl:.9f}, graded CONSISTENT (|z| = 0 for any sigma)")
REQUIRED_OK = len(fails) == 0 or (fails == ["G-BF LdD"])
if fails == ["G-BF LdD"]:
    print("   declared exception: only G-BF LdD failed -> LdD variants dropped")


def evaluate(gauge, eta_v, l3_v, ident, matter=0):
    cls = num_classes(FL[gauge], {eta: eta_v, L3: l3_v})
    rts, coeffs = closure_roots(cls, GSTAR, float(eta_v), ident, matter)
    adm = [r for r in rts if r["adm"]]
    row = dict(gauge=gauge, eta_h=float(eta_v), lambda_3=float(l3_v), ident=ident, matter=matter, roots=rts, poly=coeffs)
    if len(adm) == 1:
        r = adm[0]
        row.update(r=r["r"], g3=r["g3"], fg=r["fg"], P=P_of(r["fg"]))
        gYs = C1.gY_star_from_fg(r["fg"])
        row["P_two_loop"] = H4.two_loop_P(gYs, B2)[0]
        row["P_m_red"] = H4.reduced_planck_P(r["fg"])
    elif len(adm) == 0:
        row["status"] = "no admissible root"
    else:
        row["status"] = f"{len(adm)} admissible roots"
    # Delta coefficients for the record (U only): Delta = a g3 + b sqrt(g3 G)
    if ident == "U":
        a = -2 * 2 * (cls["2pt_V1V1"] + cls["2pt_V2"]) - 2 * (cls["g5"] + cls["g4"] + cls["g3"])
        b = -2 * (cls["g4h"] + cls["g3h"])
        row.update(a=a, b=b)
    row["cls"] = cls
    return row


LS = float(LAM_RAT)
G1 = evaluate("CPR", -2, LAM_RAT, "U")
print(f"   G1 (CPR, eta_h = -2, lambda_3 = lambda_2, U): Delta = a g_3 + b sqrt(g_3 g*), a = {G1.get('a'):.8f}, b = {G1.get('b'):.8f}")
print(f"   roots: {[(round(x['r'], 8), round(x['fg'], 8)) for x in G1['roots']]}")
if G1.get("P") is not None:
    print(f"   G1 root: r = {G1['r']:.8f}, g_3* = {G1['g3']:.8f}, f_g = {G1['fg']:.8f}, P = {G1['P']:.5f} (reported in every mode; graded only if all gates pass)")
probes = []
for eta_v in (-2, 0):
    for l3_v in (LAM_RAT, 0):
        for ident in ("U", "Uprime"):
            probes.append(evaluate("CPR", eta_v, l3_v, ident))
for mt in (+1, -1):
    probes.append(evaluate("CPR", -2, LAM_RAT, "U", matter=mt))
print("\n   CPR closure probes (one-loop at M_P):")
for pr in probes:
    lab = f"eta_h {pr['eta_h']:+.0f}, lambda_3 {'lambda*' if pr['lambda_3'] != 0 else '0':7s}, {pr['ident']:6s}, matter {pr['matter']:+d}"
    if "P" in pr and pr["P"] is not None:
        print(f"     {lab}: r = {pr['r']:.6f}, f_g = {pr['fg']:.7f}, P = {pr['P']:.4f} (two-loop {pr['P_two_loop']:.4f}, M_red {pr['P_m_red']:.4f})")
    else:
        print(f"     {lab}: {pr.get('status', 'no value')}; roots {[(round(x['r'], 6), round(x['fg'], 6)) for x in pr['roots']]}")
Pvals = [pr["P"] for pr in probes if pr.get("P") is not None]
n_excl = sum(1 for pr in probes if pr.get("P") is None)
SIGMA_FL = (max(Pvals) - min(Pvals)) / 2 if Pvals else float("nan")
SIGMA_TOT = float(np.sqrt(SIGMA_ROUTE**2 + SIGMA_FL**2))
print(f"   sigma_fl = {SIGMA_FL:.4f} (half-range over {len(Pvals)} probes; {n_excl} without an admissible root excluded); sigma_tot = {SIGMA_TOT:.4f}")

print("\n   Reported gauge variants (CPR fixed-point inputs; gauge-inconsistent, not in sigma_fl):")
gvars = []
for gauge in ("LdD", "FdD"):
    if gauge == "LdD" and not GBF_OK.get("LdD", False):
        continue
    for eta_v in (-2, 0):
        for l3_v in (LAM_RAT, 0):
            for ident in ("U", "Uprime"):
                row = evaluate(gauge, eta_v, l3_v, ident)
                gvars.append(row)
                lab = f"{gauge}: eta_h {row['eta_h']:+.0f}, lambda_3 {'lambda*' if row['lambda_3'] != 0 else '0':7s}, {row['ident']:6s}"
                if row.get("P") is not None:
                    print(f"     {lab}: r = {row['r']:.6f}, f_g = {row['fg']:.7f}, P = {row['P']:.4f}")
                else:
                    print(f"     {lab}: {row.get('status', 'no value')}; roots {[(round(x['r'], 6), round(x['fg'], 6)) for x in row['roots']]}")

# Weyl-breaking diagnostic for G1's closure: trace part 4 c_A + c_B of the generated vertex at the root
if G1.get("g3") is not None:
    clsA = {k: float(sp.N(FL["CPR"][k][0].subs({eta: -2, L3: LAM_RAT}))) for k in VCLASSES}
    x_ = np.sqrt(G1["g3"])
    mono = MONO["U"]
    cA_tot = sum(clsA[k] * x_**mono[k][0] * GSTAR**float(mono[k][1]) for k in VCLASSES)
    cB_tot = sum(G1["cls"][k] * x_**mono[k][0] * GSTAR**float(mono[k][1]) for k in VCLASSES)
    weyl = 4 * cA_tot + cB_tot
    print(f"\n   Weyl-breaking diagnostic at G1's root (per tau_3): 4 c_A + c_B = {weyl:.6f} vs c_B = {cB_tot:.6f}")
    G1["weyl_trace_part"] = weyl
    G1["cB_total_over_tau3"] = cB_tot


# ================================================================== (9) GRADE
print("\n(9) GRADE (pre-registration section 8)")
verdict = None
if not REQUIRED_OK:
    verdict = "NOT COMPLETED"
    why = f"required gate(s) failed: {fails}"
elif G1.get("P") is None:
    adm = [x for x in G1["roots"] if x["adm"]]
    if len(adm) == 1 and adm[0]["fg"] <= 0:
        verdict, why = "KILLED", "f_g <= 0 at the unique admissible root"
    else:
        verdict, why = "NOT DIAGNOSTIC", G1.get("status", "no value")
else:
    zz = (G1["P"] - TARGET) / SIGMA_TOT
    dr = SIGMA_TOT / G1["P"]
    G1.update(z=zz, delta_route=dr, sigma_fl=SIGMA_FL, sigma_tot=SIGMA_TOT, z_route_only=(G1["P"] - TARGET) / SIGMA_ROUTE,
              p_single=p_single(G1["P"] - TARGET))
    if dr > 1:
        verdict, why = "NOT DIAGNOSTIC", f"delta_route = {dr:.3f} > 1"
    elif abs(zz) > 3:
        verdict, why = "KILLED", f"z = {zz:+.3f} (|z| > 3)"
    else:
        verdict, why = "CONSISTENT", f"z = {zz:+.3f} (|z| <= 3): allowed, not predicted"
    aYuv = 41 / (24 * np.pi * G1["fg"])
    G1["aYinv_MP"] = aYuv
    G1["z_UV"] = (aYuv - 55.234) / SIGMA_TOT
    # substitution test: alpha_2^-1(M_Z) and Delta_0 scaled as if alpha were 1% larger
    saved = (B3.a2_mz, RG.DELTA_0_MZ)
    try:
        B3.a2_mz = saved[0] / 1.01
        RG.DELTA_0_MZ = saved[1] / 1.01
        Psub = C1.downstream_P(G1["fg"])
    finally:
        B3.a2_mz, RG.DELTA_0_MZ = saved
    ident_shift = G1["P"] / 1.01 - G1["P"]
    G1["substitution_shift"] = Psub - G1["P"]
    G1["substitution_fraction"] = abs((Psub - G1["P"]) / ident_shift)
    print(f"   G1: r = g_3*/g* = {G1['r']:.6f}, g_3* = {G1['g3']:.6f}, f_g = {G1['fg']:.8f} (background {FG_BF_CPR:.8f}), P = {G1['P']:.5f}")
    print(f"   miss {G1['P'] - TARGET:+.4f} ({(G1['P'] - TARGET) / TARGET * 100:+.2f}%); z = {zz:+.3f} with sigma_tot {SIGMA_TOT:.4f} "
          f"(route-only z {G1['z_route_only']:+.3f}); delta_route {dr:.4f}; P_single {G1['p_single']:.4f}")
    print(f"   systematics: two-loop {G1['P_two_loop']:.5f}, M_red {G1['P_m_red']:.5f}")
    print(f"   UV cross-check (no measured alpha): 1/alpha_Y*(M_P) = {aYuv:.4f} vs Y1 55.234 -> z_UV = {G1['z_UV']:+.3f}")
    print(f"   substitution test: P shift {G1['substitution_shift']:+.4f} vs identity {ident_shift:+.4f} -> fraction {G1['substitution_fraction']:.3f}")
print(f"\n   VERDICT (G1): {verdict}  [{why}]")
results.update(G1={k: v for k, v in G1.items() if k not in ("roots",)}, G1_roots=G1["roots"], verdict=verdict, why=why,
               probes=[{k: v for k, v in pr.items()} for pr in probes], gauge_variants=gvars, sigma_fl=SIGMA_FL, sigma_tot=SIGMA_TOT,
               n_mech=(N_MECH_BEFORE + 1 if G1.get("P") is not None else N_MECH_BEFORE), fails=fails,
               runtime_s=time.time() - T0, peak_rss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576)


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, (np.integer, int)):
        return int(o)
    if isinstance(o, sp.Basic):
        return str(o)
    return o


with open(HERE / f"{OUTSTEM}.json", "w") as fh:
    json.dump(_clean(results), fh, indent=1)
print(f"\nCHECKS FAILED: {fails if fails else 'none'}")
stamp("done")
sys.exit(1 if fails else 0)
