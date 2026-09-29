"""
CFG108 -- independent re-derivation of CFG116 (cross-shear and near/far nulls of the KiDS early/late split) plus a power attack.
The FROZEN text is cfg108_FROZEN.txt (written before any run; its sha256 is printed).  Run: ZF_REPO=<repo root> python3 cfg108_run.py ; MUTATE=1 for the control.
"""
import os, sys, math, time, json, hashlib, warnings
import numpy as np
from scipy import stats, optimize, integrate

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
OUT = os.path.join(HERE, "cfg108_results_MUTATE.json" if MUTATE else "cfg108_results.json")
T0 = time.time()
def log(*a): print(*a, flush=True)
def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "real_research", "data", "lensing_rar")):
        return env
    for s in (HERE, os.getcwd()):
        p = s
        for _ in range(14):
            if os.path.isdir(os.path.join(p, "real_research", "data", "lensing_rar")):
                return p
            p = os.path.dirname(p)
    raise RuntimeError("set ZF_REPO to the repository root")
REPO = find_repo(); DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FSHA = hashlib.sha256(open(os.path.join(HERE, "cfg108_FROZEN.txt"), "rb").read()).hexdigest()
log("CFG108  MUTATE=%d  frozen-text sha256 %s" % (MUTATE, FSHA[:16]))
np.set_printoptions(linewidth=220, precision=3, suppress=True)
warnings.filterwarnings('ignore', category=RuntimeWarning)   # Accelerate matmul quirk (CFG77/CFG100); K3 cross-checks the algebra with einsum/solve

NP = 50
KG = 1.98847e30 / (3.0857e16) ** 2
G_MPC = 4.30091727e-9
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M
GEDGE = np.logspace(math.log10(1e-15), math.log10(5e-12), 16)
checks = {}
def check(name, ok, msg):
    checks[name] = bool(ok)
    log("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))
repro = []
def cmp(name, mine, target, tol):
    d = abs(mine - target)
    st = "REPRODUCED" if d <= tol else ("APPROXIMATE" if d <= 0.10 * abs(target) else "NOT REPRODUCED")
    repro.append((name, float(mine), float(target), float(tol), st))
    log("    %-52s mine %-10.5g CFG116 %-9.5g tol %-6.3g %s" % (name, mine, target, tol, st))
R = {}

# ------------------------------------------------------------------ inputs
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z, Mgal, typ = lens["z"], lens["Mgal"], lens["typ"]
nL = len(z)
jk = np.load(os.path.join(DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
p110 = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
p116 = np.load(os.path.join(DATA, "cfg116_perlens.npz"))
assert np.allclose(p116["gbar_edges"], GEDGE) and np.allclose(p110["gbar_edges"], GEDGE)
WGn, WWn, NNn = p116["WGn"].copy(), p116["WWn"], p116["NNn"]
WGf, WWf, NNf = p116["WGf"].copy(), p116["WWf"], p116["NNf"]
WX = p116["WX"].copy(); WGrot = p116["WGrot"]
WG_all = WGn + WGf; WW_all = WWn + WWf; NN_all = NNn + NNf

# ------------------------------------------------------------------ per-(patch, class, bin) sums
def psum(arr, cls=None, mask=None):
    """arr (nL,15) -> (NP,2,15) sums by patch and class."""
    c = typ if cls is None else cls
    key = patch * 2 + c
    w = None if mask is None else mask.astype(float)
    out = np.empty((NP * 2, arr.shape[1]))
    for k in range(arr.shape[1]):
        col = arr[:, k] if w is None else arr[:, k] * w
        out[:, k] = np.bincount(key, weights=col, minlength=NP * 2)
    return out.reshape(NP, 2, arr.shape[1])

gcen = np.sqrt(GEDGE[:-1] * GEDGE[1:]) / SI_ACC
Rmed = np.array([[np.median(np.sqrt(G_MPC * Mgal[typ == c] / g)) for g in gcen] for c in (0, 1)])
K1 = np.array([k for k in range(15) if Rmed[0, k] < 0.3 and Rmed[1, k] < 0.3])
log("== controls on inputs")
check("K2a K1 bins", list(K1) == list(range(8, 15)), "K1 = %s" % list(K1))

def build_S(WGn_, WWn_, WGf_, WWf_, WX_, cls=None, mask=None):
    S = {}
    S["WG_near"] = psum(WGn_, cls, mask); S["WW_near"] = psum(WWn_, cls, mask)
    S["WG_far"] = psum(WGf_, cls, mask); S["WW_far"] = psum(WWf_, cls, mask)
    S["WG_all"] = S["WG_near"] + S["WG_far"]; S["WW_all"] = S["WW_near"] + S["WW_far"]
    S["WX"] = psum(WX_, cls, mask)
    return S

# K1: June sums
mx = 0.0
for name, a, b in (("WG", WG_all, jk["wgE"]), ("WW", WW_all, jk["W"]), ("NN", NN_all, jk["NN"])):
    s = psum(a)
    mx = max(mx, float(np.max(np.abs(s - b) / np.maximum(np.abs(b), 1e-300))))
check("K1 near+far vs June per-(patch,class,bin)", mx <= 1e-9, "max relative deviation %.2e (<= 1e-9)" % mx)
mx2 = 0.0
for name, a, b in (("WG", WG_all, p110["WG"]), ("WW", WW_all, p110["WW"]), ("NN", NN_all, p110["NN"])):
    sc = 1e-6 * np.median(np.abs(b), axis=0)[None, :]
    mx2 = max(mx2, float(np.max(np.abs(a - b) / (np.abs(b) + sc + 1e-300))))
check("K1b near+far vs cfg110_perlens per lens per bin", mx2 <= 1e-9, "max |a-b|/(|b|+1e-6 median|b|) %.2e (<= 1e-9)" % mx2)
rowscale = np.max(np.abs(WGrot), axis=1, keepdims=True) + 1e-300
d2 = float(np.max(np.abs(WX[:2000] - WGrot) / rowscale))
dt_ = float(np.max(np.abs(WX[:2000] - WG_all[:2000]) / rowscale))
check("K2 WX[:2000] == WGrot (staging's own control) and WX != tangential", d2 <= 1e-9 and dt_ > 0.5,
      "max |WX-WGrot|/row scale %.2e; max |WX-WG|/row scale %.2f" % (d2, dt_))

if MUTATE:
    e = typ == 1
    WX[e] += 0.3 * WG_all[e]
    log("  MUTATE=1: WX[early] += 0.3 WG_all[early] (every bin)")

S = build_S(WGn, WWn, WGf, WWf, WX)
T = {k: v.sum(0) for k, v in S.items()}
Wfix = T["WW_all"].sum(0)      # (15,) fixed pair weight per bin, all lenses/sources (V1 amplitude weight)

# ------------------------------------------------------------------ statistics (vectorised over leading axes)
def ESD(Tm, s):
    return Tm["WG_" + s] / Tm["WW_" + s] / KG
def ESDx(Tm):
    return Tm["WX"] / Tm["WW_all"] / KG
def Dset(Tm, s, ks=K1):
    e = ESD(Tm, s)
    return e[..., 1, :][..., ks] - e[..., 0, :][..., ks]
def Dx(Tm, ks=K1):
    e = ESDx(Tm)
    return e[..., 1, :][..., ks] - e[..., 0, :][..., ks]
def Dnf(Tm):
    return Dset(Tm, "near") - Dset(Tm, "far")
def xclass(Tm, c, ks=K1):
    return ESDx(Tm)[..., c, :][..., ks]
def tclass(Tm, c, s="all", ks=K1):
    return ESD(Tm, s)[..., c, :][..., ks]
def xwhole(Tm):
    return Tm["WX"].sum(-2) / Tm["WW_all"].sum(-2) / KG

def jackknife(fn, T_, S_):
    full = fn(T_)
    Tm = {k: T_[k][None] - S_[k] for k in T_}
    J = fn(Tm)
    return np.asarray(full, float), np.asarray(J, float)
def covJ(J):
    d = J - J.mean(0)
    return (NP - 1) / NP * np.einsum("pi,pj->ij", d, d)
def hart(n): return (NP - n - 2) / (NP - 1)
def chi2_of(v, J):
    C = covJ(J); n = len(v)
    return float(hart(n) * v @ np.linalg.solve(C, v)), n, C
def pv(c, n): return float(stats.chi2.sf(c, n))

def jstat(fn):
    return jackknife(fn, T, S)

# ------------------------------------------------------------------ R0 first: power row
Dt, Jt = jstat(lambda Tm: Dset(Tm, "all"))
Dxv, Jx = jstat(Dx)
Dnfv, Jnf = jstat(Dnf)
Ct, Cx, Cnf = covJ(Jt), covJ(Jx), covJ(Jnf)
h7 = hart(7)
Pt, Px, Pnf = h7 * np.linalg.inv(Ct), h7 * np.linalg.inv(Cx), h7 * np.linalg.inv(Cnf)
log("== R0 POWER (printed before any cross / near-far null number).  D_t (all-source early-late, K1) = %s" % np.round(Dt, 2))
chi_t = float(Dt @ Pt @ Dt)
log("   tangential all-source split chi2 (Hartlap, 7 dof) = %.2f" % chi_t)
R0 = {}
for eps in (0.1, 0.25, 0.5, 0.75, 1.0):
    lx = eps ** 2 * float(Dt @ Px @ Dt); lnf = eps ** 2 * float(Dt @ Pnf @ Dt); lt = eps ** 2 * chi_t
    R0[eps] = dict(lam_x=lx, lam_nf=lnf, lam_t=lt)
    log("   eps %.2f  cross: lambda(A: own cov) %.2f  (7+lambda %.2f)   lambda(B: tangential cov) %.2f   near/far lambda(A) %.2f (7+lambda %.2f)" %
        (eps, lx, 7 + lx, lt, lnf, 7 + lnf))
R["R0"] = {str(k): v for k, v in R0.items()}

# ------------------------------------------------------------------ the nulls
log("== HEADLINE")
c_x, n_x, _ = chi2_of(Dxv, Jx)
log("  cross-shear early-late difference over K1: D_x = %s" % np.round(Dxv, 2))
log("  errors (sqrt diag C) %s" % np.round(np.sqrt(np.diag(Cx)), 2))
log("  chi2 = %.2f / 7  p = %.3f" % (c_x, pv(c_x, 7)))
res_cls = {}
for c, nm in ((0, "late"), (1, "early")):
    xv, Jxc = jstat(lambda Tm, c=c: xclass(Tm, c))
    cc, n, Cc = chi2_of(xv, Jxc)
    res_cls[nm] = (xv, cc, Cc)
    log("  cross profile %-5s %s  chi2 %.2f / 7 p %.3f" % (nm, np.round(xv, 1), cc, pv(cc, 7)))
xw, Jxw = jstat(xwhole)
c_w, nw, Cw = chi2_of(xw, Jxw)
log("  R4 whole-sample cross over all 15 bins: chi2 %.2f / 15  p %.3f" % (c_w, pv(c_w, 15)))
H1 = pv(c_x, 7) > 0.01 and pv(res_cls["late"][1], 7) > 0.01 and pv(res_cls["early"][1], 7) > 0.01
c_nf, _, _ = chi2_of(Dnfv, Jnf)
H2 = pv(c_nf, 7) > 0.01
log("  near-minus-far difference D_nf = %s   chi2 = %.2f / 7  p = %.3f" % (np.round(Dnfv, 2), c_nf, pv(c_nf, 7)))
log("  H1 (cross null) %s   H2 (near/far) %s" % ("PASS" if H1 else "FAIL", "PASS" if H2 else "FAIL"))

log("== R1/R2 tangential rows")
Dsets = {}
for s in ("near", "far", "all"):
    Dv, Jd = jstat(lambda Tm, s=s: Dset(Tm, s))
    cc, n, Cd = chi2_of(Dv, Jd)
    Dsets[s] = (Dv, Jd, Cd, cc)
    log("  %-4s early-late D = %s   errors %s   chi2 %.2f / 7  p %.4g" % (s, np.round(Dv, 1), np.round(np.sqrt(np.diag(Cd)), 1), cc, pv(cc, 7)))
    for c, nm in ((0, "late"), (1, "early")):
        pv_, Jp = jstat(lambda Tm, c=c, s=s: tclass(Tm, c, s))
        log("        %-5s profile %s" % (nm, np.round(pv_, 1)))
for c, nm in ((0, "late"), (1, "early")):
    log("  cross %-5s profile %s" % (nm, np.round(res_cls[nm][0], 1)))
log("  jackknife errors of the cross difference: min %.2f max %.2f" % (np.sqrt(np.diag(Cx)).min(), np.sqrt(np.diag(Cx)).max()))

# ------------------------------------------------------------------ amplitudes
w = Wfix[K1]
def amp_v1(Tm, s, cnum=1, cden=0):
    e = ESD(Tm, s)[..., K1]
    return np.log10((w * e[..., cnum, :]).sum(-1) / (w * e[..., cden, :]).sum(-1))
def amp_v2(Tm, s):
    a = Tm["WG_" + s][..., :, K1].sum(-1) / Tm["WW_" + s][..., :, K1].sum(-1)
    return np.log10(a[..., 1] / a[..., 0])
def dil_v1(Tm, c):
    return np.log10((w * ESD(Tm, "far")[..., c, K1]).sum(-1) / (w * ESD(Tm, "near")[..., c, K1]).sum(-1))
def dil_v2(Tm, c):
    a = lambda s: Tm["WG_" + s][..., c, K1].sum(-1) / Tm["WW_" + s][..., c, K1].sum(-1)
    return np.log10(a("far") / a("near"))
def scal(fn):
    f, J = jstat(fn)
    return float(f), float(np.sqrt((NP - 1) / NP * ((J - J.mean()) ** 2).sum()))
log("== amplitudes (early - late, dex)")
AMP = {}
for s in ("near", "far", "all"):
    a1 = scal(lambda Tm, s=s: amp_v1(Tm, s)); a2 = scal(lambda Tm, s=s: amp_v2(Tm, s))
    AMP[s] = (a1, a2)
    log("  %-4s V1 %+.3f +- %.3f    V2 %+.3f +- %.3f" % (s, a1[0], a1[1], a2[0], a2[1]))
log("== dilution (far over near, dex)")
DIL = {}
for c, nm in ((0, "late"), (1, "early")):
    d1 = scal(lambda Tm, c=c: dil_v1(Tm, c)); d2 = scal(lambda Tm, c=c: dil_v2(Tm, c))
    DIL[nm] = (d1, d2)
    log("  %-5s V1 %.3f +- %.3f    V2 %.3f +- %.3f" % (nm, d1[0], d1[1], d2[0], d2[1]))
share = []
for c in (0, 1):
    share.append(float(T["WW_far"][c, K1].sum() / T["WW_all"][c, K1].sum()))
log("  far share of K1 pair weight: late %.3f early %.3f" % tuple(share))

# ------------------------------------------------------------------ reproduction
log("== reproduction against CFG116's printed numbers")
if not MUTATE:
    cmp("P1 cross difference chi2 /7", c_x, 5.3, 0.05); cmp("P1 p", pv(c_x, 7), 0.63, 0.005)
    cmp("P2 late cross chi2", res_cls["late"][1], 2.2, 0.05); cmp("P2 early cross chi2", res_cls["early"][1], 4.7, 0.05)
    cmp("P3 whole-sample cross chi2 /15", c_w, 12.1, 0.05)
    cmp("P4 lambda_x(0.5), reading A (own cov)", R0[0.5]["lam_x"], 9.0, 0.5); cmp("P4 lambda_x(0.25), A", R0[0.25]["lam_x"], 2.2, 0.05)
    cmp("P4 lambda_x(0.5), reading B (tangential cov)", R0[0.5]["lam_t"], 9.0, 0.5); cmp("P4 lambda_x(0.25), B", R0[0.25]["lam_t"], 2.2, 0.05)
    cmp("P4 lambda_nf(0.5)", R0[0.5]["lam_nf"], 3.0, 0.5)
    cmp("P5 near/far chi2 /7", c_nf, 5.4, 0.05); cmp("P5 p", pv(c_nf, 7), 0.62, 0.005)
    cmp("P6 far-only chi2 /7", Dsets["far"][3], 23.2, 0.05); cmp("P6 p", pv(Dsets["far"][3], 7), 0.0016, 0.0001)
    for s, tv, te in (("near", 0.20, 0.06), ("far", 0.17, 0.05), ("all", 0.18, 0.04)):
        cmp("P7 amplitude %s (V1)" % s, AMP[s][0][0], tv, 0.005); cmp("P7 error %s (V1)" % s, AMP[s][0][1], te, 0.005)
    cmp("P8 dilution late (V1)", DIL["late"][0][0], 0.13, 0.005); cmp("P8 error late", DIL["late"][0][1], 0.08, 0.005)
    cmp("P8 dilution early (V1)", DIL["early"][0][0], 0.09, 0.005); cmp("P8 error early", DIL["early"][0][1], 0.04, 0.005)
    cmp("P9 far share late (%)", 100 * share[0], 51, 1); cmp("P9 far share early (%)", 100 * share[1], 51, 1)
    cmp("P10 min cross-diff error", np.sqrt(np.diag(Cx)).min(), 2.1, 0.06); cmp("P10 max cross-diff error", np.sqrt(np.diag(Cx)).max(), 9.7, 0.06)
    tab = {"near D": (Dsets["near"][0], [4.1, 2.8, 7.1, 3.5, 19.4, 28.5, 32.9]), "far D": (Dsets["far"][0], [2.5, 11.3, 4.2, 7.1, 4.6, 14.3, 33.3]),
           "cross late": (res_cls["late"][0], [0.2, 0.5, -3.1, 0.6, -0.8, -3.0, -6.0]), "cross early": (res_cls["early"][0], [-2.3, -0.7, 1.6, 0.1, 0.3, 0.9, -8.5])}
    for nm, (mv, tv) in tab.items():
        log("    P10 %-12s max |mine - README| = %.3f" % (nm, np.max(np.abs(mv - np.array(tv)))))
    for s, prof in (("near", {0: [6.4, 11.7, 11.7, 16.7, 13.4, 16.3, 14.4], 1: [10.5, 14.4, 18.7, 20.2, 32.8, 44.8, 47.3]}),
                    ("far", {0: [10.7, 7.5, 19.6, 21.1, 26.6, 35.1, 23.9], 1: [13.2, 18.8, 23.9, 28.2, 31.2, 49.4, 57.1]})):
        for c in (0, 1):
            mv = ESD(T, s)[c, K1]
            log("    P10 %s %s profile max |mine - README| = %.3f" % (s, ("late", "early")[c], np.max(np.abs(mv - np.array(prof[c])))))

# ------------------------------------------------------------------ controls K3..K8
log("== controls")
# K3a
v = Dt; C = Ct
c_solve = v @ np.linalg.solve(C, v)
Lc = np.linalg.cholesky(C); zz = np.linalg.solve(Lc, v); c_chol = zz @ zz
c_inv = v @ np.linalg.inv(C) @ v
eig = np.linalg.eigvalsh(C)
check("K3a chi2 solve/Cholesky/inverse; C SPD", max(abs(c_solve - c_chol), abs(c_solve - c_inv)) < 1e-8 * abs(c_solve) and eig.min() > 0 and np.allclose(C, C.T),
      "chi2 %.6f %.6f %.6f; min eig %.3e" % (c_solve, c_chol, c_inv, eig.min()))
# K3b: T C28 T^T
def v28(Tm):
    en, ef = ESD(Tm, "near")[..., K1], ESD(Tm, "far")[..., K1]
    return np.concatenate([en[..., 1, :], en[..., 0, :], ef[..., 1, :], ef[..., 0, :]], axis=-1)
_, J28 = jstat(v28)
C28 = covJ(J28)
Tm_ = np.zeros((7, 28)); Tm_[:, 0:7] = np.eye(7); Tm_[:, 7:14] = -np.eye(7); Tm_[:, 14:21] = -np.eye(7); Tm_[:, 21:28] = np.eye(7)
dev = np.max(np.abs(Tm_ @ C28 @ Tm_.T - Cnf)) / np.max(np.abs(Cnf))
check("K3b D_nf covariance == T C28 T^T", dev < 1e-9, "max relative deviation %.2e" % dev)
mdev = np.max(np.abs(Jt.mean(0) - Dt) / np.abs(Dt))
check("K3c jackknife mean vs full D", mdev < 1e-3, "max relative deviation %.2e" % mdev)
# K5 swaps
def chi_H2_from(sa, sb):
    f = lambda Tm: Dset(Tm, sa) - Dset(Tm, sb)
    v_, J_ = jstat(f); return chi2_of(v_, J_)[0]
c_sw = chi_H2_from("far", "near")
Tsw = dict(T); Ssw = dict(S)
def swapcls(dct): return {k: v[..., ::-1, :].copy() for k, v in dct.items()}
Tc, Sc = swapcls({k: v for k, v in T.items()}), swapcls(S)
Tc = {k: v for k, v in Tc.items()}; Sc = {k: v for k, v in Sc.items()}
# Tc from S reversed along class axis: T_ has no patch axis -> reverse axis -2 works for both
cx_s, _, _ = chi2_of(*jackknife(Dx, Tc, Sc)); cf_s = chi2_of(*jackknife(lambda Tm: Dset(Tm, "far"), Tc, Sc))[0]
a_s = jackknife(lambda Tm: amp_v1(Tm, "far"), Tc, Sc)[0]
check("K5a near<->far swap: H2 chi2 unchanged", abs(c_sw - c_nf) < 1e-9 * c_nf, "H2 %.9f vs swapped %.9f" % (c_nf, c_sw))
check("K5b early<->late swap: chi2 unchanged, amplitude flips", abs(cx_s - c_x) < 1e-9 * max(c_x, 1) and abs(cf_s - Dsets["far"][3]) < 1e-9 * Dsets["far"][3] and abs(a_s + AMP["far"][0][0]) < 1e-12,
      "cross %.6f/%.6f, far %.6f/%.6f, amp %+.6f/%+.6f" % (c_x, cx_s, Dsets["far"][3], cf_s, AMP["far"][0][0], a_s))
# K6 exact injection
def A_leak(Dr, Jr, shape=None, P=None):
    s = Dt if shape is None else shape
    Pm = Px if P is None else P
    a = float(s @ Pm @ Dr / (s @ Pm @ s)); sg = float((s @ Pm @ s) ** -0.5)
    return a, sg
inj = {}
ok6 = True
for eps in (0.25, 0.5):
    Sx = {k: v.copy() for k, v in S.items()}
    add = np.zeros((nL, 15)); e = typ == 1
    add[np.ix_(e, K1)] = (eps * Dt * KG)[None, :] * WW_all[np.ix_(e, K1)]
    Sx["WX"] = S["WX"] + psum(add)
    Tx = {k: v.sum(0) for k, v in Sx.items()}
    Dx_i, Jx_i = jackknife(Dx, Tx, Sx)
    c_i, _, Ci = chi2_of(Dx_i, Jx_i)
    pred = float(h7 * (Dxv + eps * Dt) @ np.linalg.solve(Cx, Dxv + eps * Dt))
    a0, sg = A_leak(Dxv, Jx); a1, _ = A_leak(Dx_i, Jx_i)
    covdev = np.max(np.abs(Ci - Cx)) / np.max(np.abs(Cx))
    # near-only injection
    addn = np.zeros((nL, 15)); addn[np.ix_(e, K1)] = (eps * Dt * KG)[None, :] * WWn[np.ix_(e, K1)]
    S2 = {k: v.copy() for k, v in S.items()}
    S2["WG_near"] = S["WG_near"] + psum(addn); S2["WG_all"] = S2["WG_near"] + S["WG_far"]
    T2 = {k: v.sum(0) for k, v in S2.items()}
    Dn_i, Jn_i = jackknife(Dnf, T2, S2); cn_i, _, Cn_i = chi2_of(Dn_i, Jn_i)
    predn = float(h7 * (Dnfv + eps * Dt) @ np.linalg.solve(Cnf, Dnfv + eps * Dt))
    an0, sgn = A_leak(Dnfv, Jnf, P=Pnf); an1, _ = A_leak(Dn_i, Jn_i, P=Pnf)
    ok6 &= abs(c_i - pred) < 1e-8 * max(pred, 1) and abs((a1 - a0) - eps) < 1e-8 and covdev < 1e-9 and abs(cn_i - predn) < 1e-8 * max(predn, 1) and abs((an1 - an0) - eps) < 1e-8
    inj[eps] = dict(cross_chi2=c_i, cross_pred=pred, cross_Ahat=a1, nf_chi2=cn_i, nf_pred=predn, nf_Ahat=an1)
    log("    injection eps %.2f: cross chi2 %.2f (pred %.2f, A_hat %.3f -> %.3f, cov dev %.1e) | near-only into H2: chi2 %.2f (pred %.2f, A_hat %.3f -> %.3f)" %
        (eps, c_i, pred, a0, a1, covdev, cn_i, predn, an0, an1))
check("K6 exact-injection recovery (cross and near-only)", ok6, "chi2 == prediction, A_hat shift == eps, C unchanged")
# K7 power machinery
rng = np.random.default_rng(1080)
lam = R0[0.5]["lam_x"]; mu_w = np.zeros(7); mu_w[0] = math.sqrt(lam)
crit = stats.chi2.ppf(0.99, 7)
zs = rng.standard_normal((200000, 7)) + mu_w
pw_mc = float(((zs ** 2).sum(1) > crit).mean()); pw_an = float(stats.ncx2.sf(crit, 7, lam))
check("K7 power machinery (ncx2 vs MC)", abs(pw_mc - pw_an) < 0.01, "analytic %.4f, MC %.4f (lambda %.2f)" % (pw_an, pw_mc, lam))
# K8 plausibility
okc = np.array_equal(NNn + NNf, p110["NN"]) and (NNn + NNf == np.round(NNn + NNf)).all()
check("K8a NNn+NNf == cfg110 NN, integer", okc, "exact equality %s" % okc)
check("K8b weights non-negative", bool((WWn >= 0).all() and (WWf >= 0).all()), "min WWn %.3e WWf %.3e" % (WWn.min(), WWf.min()))
mk = (NNn[:, K1] > 0) & (NNf[:, K1] > 0)
wpn = WWn[:, K1][mk] / NNn[:, K1][mk]; wpf = WWf[:, K1][mk] / NNf[:, K1][mk]
frac = float((wpn < wpf).mean())
check("K8c near weight per pair < far weight per pair", frac > 0.90, "fraction of lens-bins %.3f (> 0.90), N %d" % (frac, mk.sum()))
ffar = NNf[:, K1].sum(1) / np.maximum(NNn[:, K1].sum(1) + NNf[:, K1].sum(1), 1)
rho = float(stats.spearmanr(z, ffar)[0])
check("K8d far pair fraction falls with lens z", rho < 0, "Spearman rho = %.3f" % rho)
ratio = np.sqrt(np.diag(Cx)) / np.sqrt(np.diag(Ct))
check("K8e cross/tangential noise ratio per K1 bin in [0.7, 1.4]", ratio.min() >= 0.7 and ratio.max() <= 1.4, "ratios %s" % np.round(ratio, 2))

# ------------------------------------------------------------------ K4 + A7 permutation
log("== K4/A7 permutation of class labels within patch (2000 perms, seed 108)")
NPERM = int(os.environ.get("NPERM", "2000"))
rngp = np.random.default_rng(108)
base = np.argsort(patch, kind="stable")
cols = list(K1)
def perm_stats(cls):
    Sp = {}
    for nm, arr in (("WG_near", WGn), ("WW_near", WWn), ("WG_far", WGf), ("WW_far", WWf), ("WX", WX)):
        key = patch * 2 + cls
        o = np.ones((NP * 2, 15))
        for k in cols:
            o[:, k] = np.bincount(key, weights=arr[:, k], minlength=NP * 2)
        Sp[nm] = o.reshape(NP, 2, 15)
    Sp["WG_all"] = Sp["WG_near"] + Sp["WG_far"]; Sp["WW_all"] = Sp["WW_near"] + Sp["WW_far"]
    Tp = {k: v.sum(0) for k, v in Sp.items()}
    out = []
    for fn in (lambda Tm: Dset(Tm, "all"), lambda Tm: Dset(Tm, "far"), lambda Tm: Dset(Tm, "near"), Dx, Dnf):
        vv, JJ = jackknife(fn, Tp, Sp)
        out.append(chi2_of(vv, JJ)[0])
    return out
perm = np.empty((NPERM, 5))
tP = time.time()
for i in range(NPERM):
    keys = rngp.random(nL)
    order = np.lexsort((keys, patch))
    cp = np.empty(nL, int); cp[order] = typ[base]
    perm[i] = perm_stats(cp)
names5 = ["all-source split", "far-only split", "near-only split", "cross difference", "near-minus-far"]
obs5 = [Dsets["all"][3], Dsets["far"][3], Dsets["near"][3], c_x, c_nf]
PERM = {}
okperm = True
for j, nm in enumerate(names5):
    m = perm[:, j].mean(); emp = float((1 + (perm[:, j] >= obs5[j]).sum()) / (NPERM + 1))
    okperm &= 5.5 <= m <= 8.5
    PERM[nm] = dict(mean=float(m), sd=float(perm[:, j].std()), obs=float(obs5[j]), emp_p=emp, chi2_p=pv(obs5[j], 7), q99=float(np.quantile(perm[:, j], 0.99)))
    log("   %-18s perm mean %.2f sd %.2f  q99 %.2f | observed %.2f  empirical p %.4f (chi2-7dof p %.4g)" % (nm, m, perm[:, j].std(), PERM[nm]["q99"], obs5[j], emp, pv(obs5[j], 7)))
check("K4 permutation calibration (mean of each in [5.5, 8.5])", okperm, "%.0f s" % (time.time() - tP))
R["permutation"] = PERM

# half-lens subsamples
rngh = np.random.default_rng(109)
hs = []
for i in range(300):
    m = rngh.random(nL) < 0.51
    Sh = build_S(WGn, WWn, WGf, WWf, WX, mask=m)
    Th = {k: v.sum(0) for k, v in Sh.items()}
    vv, JJ = jackknife(lambda Tm: Dset(Tm, "all"), Th, Sh)
    hs.append(chi2_of(vv, JJ)[0])
hs = np.array(hs)
log("== A7 half-lens subsamples (keep prob 0.51, classes intact): all-source split chi2 median %.1f, 16-84%% [%.1f, %.1f]; observed far-only %.1f; P(sub >= far-only) = %.2f; P(sub <= 7 chi2 q99) = %.3f" %
    (np.median(hs), *np.quantile(hs, [0.16, 0.84]), Dsets["far"][3], float((hs >= Dsets["far"][3]).mean()), float((hs <= stats.chi2.ppf(0.99, 7)).mean())))
R["halfsub"] = dict(median=float(np.median(hs)), q16=float(np.quantile(hs, 0.16)), q84=float(np.quantile(hs, 0.84)), frac_ge_far=float((hs >= Dsets["far"][3]).mean()))

# ------------------------------------------------------------------ attack rows
log("== ATTACK ROWS")
def power(lam_, alpha, dof=7):
    return float(stats.ncx2.sf(stats.chi2.ppf(1 - alpha, dof), dof, lam_))
def eps_detect(lam1, alpha=0.01, dof=7, target=0.8):
    f = lambda e: power(e * e * lam1, alpha, dof) - target
    return float(optimize.brentq(f, 1e-3, 20))
lam1_x = float(Dt @ Px @ Dt); lam1_nf = float(Dt @ Pnf @ Dt)
log("  A1/A2 power (lambda A: own covariance), unit-eps lambda: cross %.1f, near/far %.1f" % (lam1_x, lam1_nf))
log("   eps    lam_x  pow(.01) pow(.05) | lam_nf pow(.01) pow(.05)")
for eps in (0.1, 0.25, 0.5, 0.75, 1.0):
    lx, ln = eps ** 2 * lam1_x, eps ** 2 * lam1_nf
    log("   %.2f  %6.2f  %.3f   %.3f  | %6.2f  %.3f   %.3f" % (eps, lx, power(lx, 0.01), power(lx, 0.05), ln, power(ln, 0.01), power(ln, 0.05)))
ex, ex1 = eps_detect(lam1_x), (2.576 + 0.8416) / math.sqrt(lam1_x)
en, en1 = eps_detect(lam1_nf), (2.576 + 0.8416) / math.sqrt(lam1_nf)
log("  detectable eps at 80%% power, alpha 0.01: cross omnibus %.2f, 1-dof %.2f | near/far omnibus %.2f, 1-dof %.2f" % (ex, ex1, en, en1))
ax, sx = A_leak(Dxv, Jx); anf, snf = A_leak(Dnfv, Jnf, P=Pnf)
log("  1-dof leak fit: cross diff A_hat = %+.3f +- %.3f (95%% UL %.3f)  |  near/far A_hat = %+.3f +- %.3f (95%% UL %.3f)" % (ax, sx, ax + 1.645 * sx, anf, snf, anf + 1.645 * snf))
for c, nm in ((0, "late"), (1, "early")):
    tcv, Jtc = jstat(lambda Tm, c=c: tclass(Tm, c)); xcv, Jxc = jstat(lambda Tm, c=c: xclass(Tm, c))
    Pc = hart(7) * np.linalg.inv(covJ(Jxc))
    a = float(tcv @ Pc @ xcv / (tcv @ Pc @ tcv)); sg = float((tcv @ Pc @ tcv) ** -0.5)
    log("   per-class leak fraction eps_%s = %+.3f +- %.3f" % (nm, a, sg))
    R.setdefault("eps_class", {})[nm] = (a, sg)
epsE = R["eps_class"]["early"]
# A3
Aall = AMP["all"][0][0]
log("  A3a additive (E~B) systematic eps = 1: lambda_x %.1f  -> p %.2g if present at the full split" % (lam1_x, stats.chi2.sf(7 + lam1_x, 7)))
log("  A3b class-dependent multiplicative shear bias needed for the whole split (V1 all): m_diff = 10^%.3f - 1 = %.2f (KiDS-1000 calibration uncertainty ~0.01-0.02: literature)" % (Aall, 10 ** Aall - 1))
Qj, Jq = jstat(lambda Tm: np.concatenate([xclass(Tm, 0), xclass(Tm, 1)], axis=-1))
Q14, n14, _ = chi2_of(Qj, Jq)
s14 = math.sqrt(Q14 / stats.chi2.ppf(0.05, 14)); s15 = math.sqrt(c_w / stats.chi2.ppf(0.05, 15)); sdiff = math.sqrt(c_x / stats.chi2.ppf(0.05, 7))
log("  A3c cross noise calibration: joint 14-vector chi2 %.2f/14 (p %.3f) -> 95%% UL on jackknife under-estimate s = %.2f; whole-sample %.2f/15 -> s <= %.2f; cross difference %.2f/7 -> s <= %.2f" %
    (Q14, pv(Q14, 14), s14, c_w, s15, c_x, sdiff))
log("  A4 covariance inflation (chi2/f^2, p):")
tab4 = {}
for f in (1.0, 1.2, 1.5, 1.81, 2.0):
    row = []
    for nm, cv in zip(names5, obs5):
        row.append((cv / f ** 2, pv(cv / f ** 2, 7)))
    tab4[f] = row
    log("   f %.2f  " % f + "  ".join("%s %.1f (p %.3g)" % (n_[:10], r[0], r[1]) for n_, r in zip(names5, row)) +
        "  | power at eps 0.5 (a=.01): cross %.3f near/far %.3f" % (power(0.25 * lam1_x / f ** 2, 0.01), power(0.25 * lam1_nf / f ** 2, 0.01)))
cf = Dsets["far"][3]
f05 = math.sqrt(cf / stats.chi2.ppf(0.95, 7)); f01 = math.sqrt(cf / stats.chi2.ppf(0.99, 7))
log("   the far-only split reaches p = 0.05 at f = %.2f and p = 0.01 at f = %.2f; all-source split: %.2f, %.2f; cross-noise 95%% UL s: %.2f (14-vector), %.2f (15-bin)" %
    (f05, f01, math.sqrt(Dsets["all"][3] / stats.chi2.ppf(0.95, 7)), math.sqrt(Dsets["all"][3] / stats.chi2.ppf(0.99, 7)), s14, s15))
R["A4"] = {str(k): v for k, v in tab4.items()}
# A5 lens z terciles
edz = np.quantile(z, [1 / 3, 2 / 3])
zb = np.searchsorted(edz, z, side="right")
Sz = [build_S(WGn, WWn, WGf, WWf, WX, mask=(zb == b)) for b in range(3)]
Tz = [{k: v.sum(0) for k, v in Sb.items()} for Sb in Sz]
Wz = [Tb["WW_all"].sum(0)[K1] for Tb in Tz]
def joint(fn_of_bin):
    # returns full and J for concatenation across the 3 z bins (independent lens sets, same patches)
    fulls, Js = [], []
    for b in range(3):
        f, J = jackknife(lambda Tm, b=b: fn_of_bin(Tm, b), Tz[b], Sz[b])
        fulls.append(np.atleast_1d(f)); Js.append(J.reshape(NP, -1))
    return np.concatenate(fulls), np.concatenate(Js, axis=1)
def ampz(Tm, b, s="far"):
    e = ESD(Tm, s)[..., K1]
    return np.log10((Wz[b] * e[..., 1, :]).sum(-1) / (Wz[b] * e[..., 0, :]).sum(-1))[..., None]
avz, Jaz = joint(lambda Tm, b: ampz(Tm, b))
Caz = covJ(Jaz)
sig = np.sqrt(np.diag(Caz))
hz = hart(3); ones = np.ones(3)
Pz = hz * np.linalg.inv(Caz)
mean_w = float(ones @ Pz @ avz / (ones @ Pz @ ones)); rz = avz - mean_w
cz = float(rz @ Pz @ rz)
log("  A5a far-source early-late amplitude in lens-z terciles (z edges %s): %s +- %s ; constancy chi2 %.2f / 2 (p %.3f)" % (np.round(edz, 3), np.round(avz, 3), np.round(sig, 3), cz, pv(cz, 2)))
for b in range(3):
    f_, J_ = jackknife(Dx, Tz[b], Sz[b])
    cc, _, _ = chi2_of(f_, J_)
    fd, Jd = jackknife(lambda Tm: Dset(Tm, "far"), Tz[b], Sz[b]); cd, _, _ = chi2_of(fd, Jd)
    log("      z tercile %d: N %d  cross difference chi2 %.2f/7 (p %.3f)   far-only split chi2 %.2f/7" % (b, int((zb == b).sum()), cc, pv(cc, 7), cd))
# A5b analytic Sigma_crit
Om_, h_ = 0.3153, 0.6736
c_kms = 299792.458
def Dc(zz): return c_kms / (100 * h_) * integrate.quad(lambda x: 1 / math.sqrt(Om_ * (1 + x) ** 3 + 1 - Om_), 0, zz)[0]
def sigc(zl, zs):
    return Dc(zs) / (Dc(zl) * (Dc(zs) - Dc(zl))) * (1 + zl)      # proportional; comoving-based constant factors cancel in ratios only at fixed zl -> keep zl dependence via (1+zl)
def sigc_phys(zl, zs):
    return (Dc(zs) / (1 + zs)) / ((Dc(zl) / (1 + zl)) * ((Dc(zs) - Dc(zl)) / (1 + zs)))
zmed = float(np.median(z))
log("  A5b Sigma_crit sensitivity to a lens redshift error dz (own flat LCDM) at z_l = %.3f:" % zmed)
for nm, zs in (("far z_s=0.8", 0.8), ("near z_s=z_l+0.35", zmed + 0.35)):
    row = []
    for dz in (-0.05, -0.02, 0.02, 0.05):
        row.append(sigc_phys(zmed + dz, zs) / sigc_phys(zmed, zs))
    log("     %-20s ESD_est/ESD_true for dz = -0.05,-0.02,+0.02,+0.05: %s" % (nm, np.round(row, 3)))
need = 10 ** Aall
for nm, zs in (("far z_s=0.8", 0.8),):
    f = lambda dz: sigc_phys(zmed + dz, zs) / sigc_phys(zmed, zs) - need
    try:
        dzn = optimize.brentq(f, 1e-4, 0.29); log("     class-dependent lens z offset that would give the whole split (ratio %.2f): dz = %+.3f (%s)" % (need, dzn, nm))
    except Exception as ex_:
        dzn = None; log("     no dz in range for ratio %.2f (%s)" % (need, ex_))
R["A5b_dz_needed"] = dzn
# A6 inner/outer
def amp_bins(Tm, s, ks):
    ww = Wfix[ks]
    e = ESD(Tm, s)[..., ks]
    return np.log10((ww * e[..., 1, :]).sum(-1) / (ww * e[..., 0, :]).sum(-1))
inn, out = [12, 13, 14], [8, 9, 10, 11]
res6 = {}
for s in ("far", "near", "all"):
    fi, Ji = jstat(lambda Tm, s=s: np.stack([amp_bins(Tm, s, inn), amp_bins(Tm, s, out)], axis=-1))
    C2 = covJ(Ji); dd = fi[0] - fi[1]; sd = math.sqrt(C2[0, 0] + C2[1, 1] - 2 * C2[0, 1])
    res6[s] = (fi.tolist(), dd, sd)
    log("  A6 %-4s amplitude inner(12-14) %+.3f +- %.3f, outer(8-11) %+.3f +- %.3f ; inner-outer %+.3f +- %.3f (%.1f sigma)" % (s, fi[0], math.sqrt(C2[0, 0]), fi[1], math.sqrt(C2[1, 1]), dd, sd, dd / sd))
R["A6"] = res6
# A8 per-bin near/far
zb_ = Dnfv / np.sqrt(np.diag(Cnf))
log("  A8 D_nf per bin %s; z-scores %s" % (np.round(Dnfv, 1), np.round(zb_, 2)))
dropped = []
for i in range(7):
    ks = [j for j in range(7) if j != i]
    cc = float(hart(6) * Dnfv[ks] @ np.linalg.solve(Cnf[np.ix_(ks, ks)], Dnfv[ks])); dropped.append(cc)
log("     drop-one-bin chi2/6: %s" % np.round(dropped, 2))
# A9 done in amplitude section (V2)
log("== A9 V2 rows: near %+.3f, far %+.3f, all %+.3f ; dilution late %.3f early %.3f" % (AMP["near"][1][0], AMP["far"][1][0], AMP["all"][1][0], DIL["late"][1][0], DIL["early"][1][0]))

# ------------------------------------------------------------------ K9 (MUTATE recovery) and result
epsEc = R["eps_class"]["early"][0]
if MUTATE:
    check("K9 MUTATE: early leak fraction recovered 0.30 +- 0.05", abs(epsEc - 0.30) < 0.05, "eps_E = %.3f" % epsEc)
    log("  K9 MUTATE: H1 %s (must FAIL)" % ("PASS -> control FAILED" if H1 else "FAIL as required"))
    checks["K9 H1 fails under MUTATE"] = not H1
else:
    log("  main run: eps_E = %.3f +- %.3f (leak fraction of early tangential profile into the cross)" % R["eps_class"]["early"])
R.update(dict(mutate=MUTATE, H1=bool(H1), H2=bool(H2), checks=checks, cross=dict(chi2=c_x, late=res_cls["late"][1], early=res_cls["early"][1], whole15=c_w),
              nearfar=dict(chi2=c_nf), far=Dsets["far"][3], near=Dsets["near"][3], allsplit=Dsets["all"][3],
              amp={k: v[0] for k, v in AMP.items()}, dil={k: v[0] for k, v in DIL.items()}, share=share, repro=repro, frozen_sha=FSHA))
json.dump(R, open(OUT, "w"), indent=1, default=float)
allok = all(checks.values())
nrep = sum(1 for r in repro if r[4] == "REPRODUCED"); napp = sum(1 for r in repro if r[4] == "APPROXIMATE"); nno = sum(1 for r in repro if r[4] == "NOT REPRODUCED")
log("== SUMMARY controls %d/%d pass; H1 %s H2 %s; reproduction lines: %d reproduced, %d approximate, %d not reproduced; %.0f s" %
    (sum(checks.values()), len(checks), "PASS" if H1 else "FAIL", "PASS" if H2 else "FAIL", nrep, napp, nno, time.time() - T0))
rc = 0 if (allok if not MUTATE else all(v for k, v in checks.items() if k != "K9 H1 fails under MUTATE")) and H1 and H2 else 1
if MUTATE and not all(checks.values()): rc = 2
log("exit code %d" % rc)
sys.exit(rc)
