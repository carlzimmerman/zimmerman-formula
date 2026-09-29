"""
CFG109 -- independent re-derivation of CFG96 (do satellites drive the KiDS early/late split?) plus a power / difference-of-splits attack.
Frozen text: cfg109_FROZEN.txt (written before any run; its sha256 is printed).  Run: ZF_REPO=<repo root> python3 cfg109_run.py ; MUTATE=1 for the control.
"""
import os, sys, math, time, json, hashlib, warnings
import numpy as np
from scipy import stats, optimize
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
OUT = os.path.join(HERE, "cfg109_results_MUTATE.json" if MUTATE else "cfg109_results.json")
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
FSHA = hashlib.sha256(open(os.path.join(HERE, "cfg109_FROZEN.txt"), "rb").read()).hexdigest()
log("CFG109  MUTATE=%d  frozen-text sha256 %s" % (MUTATE, FSHA[:16]))
np.set_printoptions(linewidth=220, precision=3, suppress=True)
warnings.filterwarnings("ignore", category=RuntimeWarning)

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
    log("    %-46s mine %-11.5g CFG96 %-9.5g tol %-6.3g %s" % (name, mine, target, tol, st))
RES = {}

# ---------------------------------------------------------------- inputs
L = np.load(os.path.join(DATA, "lr_lenses.npz"))
ra, dec, z, Mgal, logM, typ, chi = (L[k] for k in ("ra", "dec", "z", "Mgal", "logM", "typ", "chi"))
nL = len(z)
JK = np.load(os.path.join(DATA, "lr_esd_jackknife.npz")); patch = JK["patch"]
P110 = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
FL = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))
STK = np.load(os.path.join(DATA, "cfg96_stack.npz"))
assert np.allclose(P110["gbar_edges"], GEDGE)
WG0, WW0, NN0 = P110["WG"], P110["WW"], P110["NN"]
f20, f30 = FL["f20"].astype(bool), FL["f30"].astype(bool)
iso = {10: np.ones(nL, bool), 20: f20, 30: f30}

# ---------------------------------------------------------------- C1 flags
log("== C1 flags")
n10, n20, n30 = nL, int(f20.sum()), int(f30.sum())
check("C1 flags boolean, length, nested", len(f20) == nL == len(f30) and not np.any(f30 & ~f20), "n10 %d  n20 %d  n30 %d ; f30 subset of f20: %s" % (n10, n20, n30, not np.any(f30 & ~f20)))
log("   counts: %d / %d / %d  (shares %.1f%% / %.1f%%)" % (n10, n20, n30, 100 * n20 / n10, 100 * n30 / n10))
log("   staged n in isoflags file (for reference): %s" % list(FL["n"]))

# ---------------------------------------------------------------- C1b lens-lens necessary-condition recomputation
log("== C1b lens-lens recomputation of the isolation rule (necessary condition only)")
th = np.radians(ra); ph = np.radians(dec)
xyz = np.column_stack([np.cos(ph) * np.cos(th), np.cos(ph) * np.sin(th), np.sin(ph)])
tree = cKDTree(xyz)
RT = 3.0
rad_phys = RT * (1 + z) / chi            # angle for 'physical 3 Mpc' (the larger)
rad_com = RT / chi
pi_, pj_, pth_ = [], [], []
CH = 20000
for a in range(0, nL, CH):
    sl = np.arange(a, min(nL, a + CH))
    chord = 2 * np.sin(rad_phys[sl] / 2)
    lst = tree.query_ball_point(xyz[sl], r=chord, return_sorted=False)
    cnt = np.array([len(x) for x in lst])
    ii = np.repeat(sl, cnt); jj = np.fromiter((v for x in lst for v in x), dtype=np.int64, count=cnt.sum())
    k = ii != jj
    ii, jj = ii[k], jj[k]
    d = np.linalg.norm(xyz[ii] - xyz[jj], axis=1)
    pi_.append(ii); pj_.append(jj); pth_.append(2 * np.arcsin(np.minimum(d / 2, 1)))
pi_, pj_, pth_ = np.concatenate(pi_), np.concatenate(pj_), np.concatenate(pth_)
dch = np.abs(chi[pj_] - chi[pi_])
log("   lens-lens pairs within the physical-3-Mpc angle: %d" % len(pi_))
Mdefs = {"Mgal": Mgal, "10^logM": 10 ** logM}
readings = {}
for rd in ("comoving", "physical"):
    tmask = pth_ <= (rad_com[pi_] if rd == "comoving" else rad_phys[pi_])
    for mname, M in Mdefs.items():
        qual = tmask & (M[pj_] > 0.1 * M[pi_])
        has = {}
        for W in (10, 20, 30):
            hh = np.zeros(nL, bool); hh[pi_[qual & (dch < W)]] = True
            has[W] = hh
        readings[(rd, mname)] = has
        log("   reading %-8s %-8s : lenses with a qualifying lens neighbour: W10 %d  W20 %d  W30 %d" % (rd, mname, has[10].sum(), has[20].sum(), has[30].sum()))
sel = [k for k, h in readings.items() if h[10].sum() == 0]
log("   readings with ZERO qualifying lens-lens pairs at W=10 (consistent with the base rule): %s" % sel)
c1b_ok = len(sel) > 0
viol = {}
for k in sel:
    h = readings[k]
    v20 = int((f20 & h[20]).sum()); v30 = int((f30 & h[30]).sum())
    viol[k] = (v20, v30)
    log("   %s: flagged-isolated with a lens neighbour: W20 %d of %d (%.3f%%), W30 %d of %d (%.3f%%);  share of ~f20 lenses with a lens nb: %.1f%%, of ~f30: %.1f%%" %
        (k, v20, n20, 100 * v20 / n20, v30, n30, 100 * v30 / n30, 100 * (h[20] & ~f20).sum() / (~f20).sum(), 100 * (h[30] & ~f30).sum() / (~f30).sum()))
    c1b_ok = c1b_ok and v20 <= 0.005 * n20 and v30 <= 0.005 * n30
check("C1b flags consistent with lens-lens necessary condition", c1b_ok, "selected readings %s" % sel)
RES["C1b"] = {"selected": [list(k) for k in sel], "viol": {"|".join(k): v for k, v in viol.items()}}
del pi_, pj_, pth_, dch

# ---------------------------------------------------------------- sums
def psum(arrs, mask=None, cls=None, wt=None):
    """dict of (nL,15) arrays -> dict of (NP,2,15) sums by patch and class, over the mask, optional per-lens weights wt (applied to WG, WW only)."""
    c = typ if cls is None else cls
    key = patch * 2 + c
    m = np.ones(nL, bool) if mask is None else mask
    out = {}
    for name, a in arrs.items():
        o = np.empty((NP * 2, 15))
        w = m.astype(float) * (wt if (wt is not None and name in ("WG", "WW")) else 1.0)
        for k in range(15):
            o[:, k] = np.bincount(key, weights=a[:, k] * w, minlength=NP * 2)
        out[name] = o.reshape(NP, 2, 15)
    return out
ARR = {"WG": WG0, "WW": WW0, "NN": NN0}
def totals(S): return {k: v.sum(0) for k, v in S.items()}

Sbase = psum(ARR)
S20 = psum(ARR, f20); S30 = psum(ARR, f30)
SG0 = psum(ARR, ~f20); SG1 = psum(ARR, f20 & ~f30); SG2 = S30
SN30 = psum(ARR, ~f30)
Sjune = {"WG": JK["wgE"], "WW": JK["W"], "NN": JK["NN"]}

log("== C2 / C3 / C4 sums")
def maxrel(A, B): return max(float(np.max(np.abs(A[k] - B[k]) / np.maximum(np.abs(B[k]), 1e-300))) for k in ("WG", "WW", "NN"))
d2 = maxrel(Sbase, Sjune)
check("C2 base sums vs June sums", d2 <= 1e-9, "max relative deviation %.2e (<=1e-9)" % d2)
pd = int(np.sum(STK["patch"] != patch))
check("C2b patch labels equal cfg96_stack's", pd == 0, "%d differing labels" % pd)
Sstk = {W: {"WG": STK["wgE_%d" % W], "WW": STK["W_%d" % W], "NN": STK["NN_%d" % W]} for W in (10, 20, 30)}
dd = {W: maxrel({"WG": None} if False else {k: v for k, v in S.items()}, Sstk[W]) for W, S in ((10, Sbase), (20, S20), (30, S30))}
check("C3 my window sums (cfg110 x flags) vs cfg96_stack", max(dd.values()) <= 1e-9, "max rel dev W10 %.2e  W20 %.2e  W30 %.2e" % (dd[10], dd[20], dd[30]))
d3 = maxrel(Sstk[10], Sjune)
check("C3b cfg96_stack window-10 sums vs June", d3 <= 1e-9, "max rel dev %.2e" % d3)
part = max(float(np.max(np.abs(SG0[k] + SG1[k] + SG2[k] - Sbase[k]) / np.maximum(np.abs(Sbase[k]), 1e-300))) for k in ("WG", "WW", "NN"))
cn = int((~f20).sum()) + int((f20 & ~f30).sum()) + n30
check("C4 shells partition the base sums", part <= 1e-12 and cn == nL, "max rel dev %.2e ; counts %d + %d + %d = %d" % (part, int((~f20).sum()), int((f20 & ~f30).sum()), n30, cn))

# K1 bins
gcen = np.sqrt(GEDGE[:-1] * GEDGE[1:]) / SI_ACC
Rmed = np.array([[np.median(np.sqrt(G_MPC * Mgal[typ == c] / g)) for g in gcen] for c in (0, 1)])
K1 = np.array([k for k in range(15) if Rmed[0, k] < 0.3 and Rmed[1, k] < 0.3])
check("K1 bins = 8..14", list(K1) == list(range(8, 15)), "K1 = %s" % list(K1))
ALL15 = np.arange(15)

# per-lens class counts / shares
NPAIRS = None

# ---------------------------------------------------------------- statistics
def hart(n): return (NP - n - 2) / (NP - 1)
def ESD(S): return S["WG"] / S["WW"] / KG
def Dof(S, ks=K1):
    e = ESD(S); return e[..., 1, :][..., ks] - e[..., 0, :][..., ks]
def covJ(J):
    d = J - J.mean(0); return (NP - 1) / NP * np.einsum("pi,pj->ij", d, d)
def LOO(S):
    T = totals(S); return {k: T[k][None] - S[k] for k in S}
def jk_of(fn, *Ss):
    """full-sample value and (NP,...) leave-one-patch-out values of fn(*sums)"""
    Tt = [totals(S) for S in Ss]; Ll = [LOO(S) for S in Ss]
    return np.asarray(fn(*Tt), float), np.asarray(fn(*Ll), float)
def chi2v(v, C):
    n = len(v); return float(hart(n) * v @ np.linalg.solve(C, v))
def pv(c, n): return float(stats.chi2.sf(c, n))
def sig(p): return float(stats.norm.isf(min(p, 1.0) / 2))
def zero_chi2(S, ks=K1):
    D, J = jk_of(lambda T: Dof(T, ks), S); C = covJ(J)
    return D, J, C, chi2v(D, C)

def apply_mutation(S):
    return {k: v[:, ::-1, :].copy() for k, v in S.items()}
S20_use, S30_use = (apply_mutation(S20), apply_mutation(S30)) if MUTATE else (S20, S30)
if MUTATE: log("  MUTATE=1: early/late labels swapped in the iso20 and iso30 sums (window 10 and the non-isolated shell sums unchanged)")
WS = {10: Sbase, 20: S20_use, 30: S30_use}

log("== main statistic per window (K1)")
D = {}; J = {}; C = {}; X2 = {}
for W in (10, 20, 30):
    D[W], J[W], C[W], X2[W] = zero_chi2(WS[W])
    log("  W%2d  D = %s" % (W, np.round(D[W], 2)))
    log("       err = %s   chi2 %.2f / 7  p %.3g (%.2f sigma)" % (np.round(np.sqrt(np.diag(C[W])), 2), X2[W], pv(X2[W], 7), sig(pv(X2[W], 7))))
C10i = np.linalg.inv(C[10])
def ampl(Dfull, Jd, D10f, J10):
    a = float(D10f @ C10i @ Dfull) / float(D10f @ C10i @ D10f)
    aj = np.einsum("pi,ij,pj->p", J10, C10i, Jd) / np.einsum("pi,ij,pj->p", J10, C10i, J10)
    return a, float(np.sqrt((NP - 1) / NP * ((aj - aj.mean()) ** 2).sum()))
A = {W: ampl(D[W], J[W], D[10], J[10]) for W in (10, 20, 30)}
for W in (20, 30):
    log("  A_%d = %.3f +- %.3f" % (W, A[W][0], A[W][1]))
# all 15
X15 = {}
for W in (10, 20, 30):
    D15, J15, C15, x = zero_chi2(WS[W], ALL15); X15[W] = x
    log("  W%2d all-15-bin chi2 (Hartlap 33/49) %.2f / 15  p %.3g" % (W, x, pv(x, 15)))
# composition
def comp(mask):
    r = {"N": int(mask.sum()), "early": float((typ[mask] == 1).mean())}
    r["medlogM_late"] = float(np.median(np.log10(Mgal[mask & (typ == 0)]))); r["medlogM_early"] = float(np.median(np.log10(Mgal[mask & (typ == 1)])))
    return r
COMP = {W: comp(iso[W]) for W in (10, 20, 30)}
for W in (10, 20, 30):
    c = COMP[W]; log("  R2 W%2d: N %d  early frac %.1f%%  median log M_gal late %.3f early %.3f" % (W, c["N"], 100 * c["early"], c["medlogM_late"], c["medlogM_early"]))
ratio20 = D[20] / D[10]; ratio30 = D[30] / D[10]
log("  R3 per-bin D_20/D_10 = %s   (min %.2f max %.2f)" % (np.round(ratio20, 2), ratio20.min(), ratio20.max()))
log("  R3 per-bin D_30/D_10 = %s" % np.round(ratio30, 2))
H1p = pv(X2[20], 7) < 0.0027; H1a = abs(A[20][0] - 1) <= 2 * A[20][1]
H1 = H1p and H1a
log("  H1: p<0.0027: %s ; |A_20-1| <= 2 sigma_A: %s  ->  H1 %s" % (H1p, H1a, "PASS" if H1 else "FAIL"))
RES["main"] = dict(chi2={W: X2[W] for W in X2}, p={W: pv(X2[W], 7) for W in X2}, A={W: A[W] for W in A}, X15=X15, COMP=COMP, D={W: D[W].tolist() for W in D}, H1=H1)

# ---------------------------------------------------------------- C5 covariance algebra
log("== C5 covariance algebra")
Dv, Jv = D[20], J[20]; Cv = C[20]
Ls = np.linalg.cholesky(Cv); w = np.linalg.solve(Ls, Dv)
c_a = float(hart(7) * Dv @ np.linalg.solve(Cv, Dv)); c_b = float(hart(7) * w @ w); c_c = float(hart(7) * Dv @ np.linalg.inv(Cv) @ Dv)
J14 = np.concatenate([J[10], J[20]], axis=1); C14 = covJ(J14)
Tm = np.hstack([-np.eye(7), np.eye(7)])
Cr_direct = covJ(J[20] - J[10]); Cr_T = Tm @ C14 @ Tm.T
check("C5 chi2 solve == Cholesky == inverse", max(abs(c_a - c_b), abs(c_a - c_c)) < 1e-8 * max(1, c_a), "%.10f %.10f %.10f" % (c_a, c_b, c_c))
check("C5 cov(D20-D10) == T C14 T^T", np.max(np.abs(Cr_direct - Cr_T)) <= 1e-9 * np.max(np.abs(Cr_T)), "max dev / max element %.2e" % (np.max(np.abs(Cr_direct - Cr_T)) / np.max(np.abs(Cr_T))))
check("C5 C symmetric, positive definite", np.allclose(C[20], C[20].T) and np.all(np.linalg.eigvalsh(C[20]) > 0) and np.all(np.linalg.eigvalsh(C14) > 0), "min eig C20 %.3e, C14 %.3e" % (np.linalg.eigvalsh(C[20]).min(), np.linalg.eigvalsh(C14).min()))
check("C5 mean of LOO D within 1e-3 of D", float(np.max(np.abs(J[20].mean(0) - D[20]) / np.abs(D[20]))) < 1e-3, "max rel %.2e" % float(np.max(np.abs(J[20].mean(0) - D[20]) / np.abs(D[20]))))

# ---------------------------------------------------------------- non-isolated groups, difference of splits
NON = {20: SG0, 30: SN30}
def gls(s, r, Cr):
    P = hart(len(r)) * np.linalg.inv(Cr); den = float(s @ P @ s)
    return float(s @ P @ r) / den, den ** -0.5, den
S_ = D[10]              # shape s = observed base split (fixed)
log("== A2 difference of splits (correct jackknife covariance)")
A2 = {}
for W in (20, 30):
    # (a) nested
    rn, Jn = jk_of(lambda a, b: Dof(a) - Dof(b), WS[W], Sbase)
    Cn = covJ(Jn); xn = chi2v(rn, Cn); amp, sg, _ = gls(S_, rn, Cn)
    # (b) disjoint (non minus iso)
    rb, Jb = jk_of(lambda a, b: Dof(a) - Dof(b), NON[W], WS[W])
    Cb = covJ(Jb); xb = chi2v(rb, Cb); dl, sd, sPs = gls(S_, rb, Cb)
    # (c) per class
    cl = {}
    for c, nm in ((0, "late"), (1, "early")):
        rc, Jc = jk_of(lambda a, b, c=c: ESD(a)[..., c, :][..., K1] - ESD(b)[..., c, :][..., K1], NON[W], WS[W])
        Cc = covJ(Jc); xc = chi2v(rc, Cc)
        ebase = ESD(totals(Sbase))[c][K1]
        bc, sc, _ = gls(ebase, rc, Cc)
        cl[nm] = dict(chi2=xc, p=pv(xc, 7), beta=bc, sbeta=sc, r=rc.tolist())
    # (d) weight shares
    wsh = {}
    for c, nm in ((0, "late"), (1, "early")):
        wsh[nm] = float(WS[W]["WW"][..., c, K1].sum() / Sbase["WW"][..., c, K1].sum()) if not MUTATE else float(S20["WW"][:, c, K1].sum() / Sbase["WW"][:, c, K1].sum()) if W == 20 else float(S30["WW"][:, c, K1].sum() / Sbase["WW"][:, c, K1].sum())
    A2[W] = dict(nested_chi2=xn, nested_p=pv(xn, 7), nested_amp_minus1=amp, nested_amp_sigma_gls=sg, A_jk=A[W], disj_chi2=xb, disj_p=pv(xb, 7), delta=dl, sigma_delta=sd, sPs=sPs, per_class=cl, wiso=wsh, r_disj=rb.tolist(), Cb=Cb.tolist())
    log("  W%d (a) nested  D_%d - D_10: chi2 %.2f/7 p %.3g ; GLS shape A-1 = %+.3f +- %.3f  (H1 jackknife A = %.3f +- %.3f)" % (W, W, xn, pv(xn, 7), amp, sg, A[W][0], A[W][1]))
    log("  W%d (b) disjoint D_non - D_iso: %s" % (W, np.round(rb, 2)))
    log("       errors %s  chi2 %.2f/7 p %.3g ;  delta (non-iso shape amp on D_10) = %+.3f +- %.3f (%.2f sigma)" % (np.round(np.sqrt(np.diag(Cb)), 2), xb, pv(xb, 7), dl, sd, dl / sd))
    for nm in ("late", "early"):
        c = cl[nm]; log("  W%d (c) %-5s E_non - E_iso chi2 %.2f/7 p %.3g ; ratio-shape beta = %+.3f +- %.3f" % (W, nm, c["chi2"], c["p"], c["beta"], c["sbeta"]))
    log("  W%d (d) K1 pair-weight share of iso: late %.3f early %.3f" % (W, wsh["late"], wsh["early"]))
RES["A2"] = A2

# ---------------------------------------------------------------- A1 power
log("== A1 power of the isolation test (contamination model, eps x eta grid)")
Dbar = float((S_ * Sbase["WW"].sum((0, 1))[K1]).sum() / Sbase["WW"].sum((0, 1))[K1].sum())
Ebar = float((ESD(totals(Sbase))[1][K1] * Sbase["WW"].sum(0)[1][K1]).sum() / Sbase["WW"].sum(0)[1][K1].sum())
log("  pair-weighted K1 means: <D> = %.2f, <ESD_early> = %.2f  (<ESD_E>/<D> = %.2f)" % (Dbar, Ebar, Ebar / Dbar))
EPS = (0.25, 0.5, 0.75, 1.0); ETA = (0.6, 0.75, 0.9, 1.0)
A1 = {}
for W in (20, 30):
    a2 = A2[W]; wi = a2["wiso"]["early"]; wn = 1 - wi; sA = A[W][1]; sd = a2["sigma_delta"]; sPs = a2["sPs"]
    log("  W%d: w_iso(early) = %.3f, w_non = %.3f, sigma_A = %.3f, sigma_delta = %.3f (delta_obs = %+.3f)" % (W, wi, wn, sA, sd, a2["delta"]))
    tab = []
    log("     eps  eta | A-shift  delta_true | power A-cond   power 1-dof   power 7-dof omnibus")
    crit7 = stats.chi2.isf(0.05, 7)
    for e in EPS:
        for h in ETA:
            shift = e * (1 - (1 - h) / wi); dt = e * (h / wn - (1 - h) / wi)
            pA = float(stats.norm.cdf(shift / sA - 2)); pD = float(stats.norm.cdf(dt / sd - 1.645)); lam = dt ** 2 * sPs
            pO = float(stats.ncx2.sf(crit7, 7, lam))
            tab.append(dict(eps=e, eta=h, shift=shift, delta=dt, pA=pA, p1=pD, p7=pO))
            log("     %.2f %.2f | %+.3f  %+.3f | %.3f         %.3f         %.3f" % (e, h, shift, dt, pA, pD, pO))
    emin = {}; ul = {}
    for h in ETA:
        k = h / wn - (1 - h) / wi
        emin[h] = (1.645 + 0.842) * sd / abs(k)
        ul[h] = (a2["delta"] + 1.645 * sd) / k
        sh = (1 - (1 - h) / wi)
        log("     eta %.2f: eps_min (80%% power, 1-dof, one-sided .05) = %.2f ;  95%% upper limit on eps from the observed delta = %.2f ;  A-condition: eps for 80%% power = %.2f (need shift >= %.2f)" %
            (h, emin[h], ul[h], (2 + 0.842) * sA / sh, (2 + 0.842) * sA))
    log("     conversion (xi = 1, satellites add their host signal equal to the early class's own ESD): f_s = eps <D>/<ESD_E> = %.2f eps" % (Dbar / Ebar))
    A1[W] = dict(tab=tab, eps_min={str(k): v for k, v in emin.items()}, eps_ul95={str(k): v for k, v in ul.items()}, fs_per_eps=Dbar / Ebar)
RES["A1"] = A1

# ---------------------------------------------------------------- A3 dose response
log("== A3 dose-response over the disjoint shells")
shells = {"G0 (nb at 10-20)": SG0, "G1 (iso20, nb at 20-30)": SG1, "G2 (iso30)": SG2}
Dsh = {}; Jsh = {}; Ash = {}
for nm, S in shells.items():
    Dsh[nm], Jsh[nm] = jk_of(lambda a: Dof(a), S)
    aa = np.einsum("i,ij,pj->p", D[10], C10i, Jsh[nm]) / np.einsum("i,ij,i->", D[10], C10i, D[10])
    a0 = float(D[10] @ C10i @ Dsh[nm]) / float(D[10] @ C10i @ D[10])
    Ash[nm] = (a0, aa)
    # error of shell amplitude: jackknife on the numerator with D10 LOO too
    aj = np.einsum("pi,ij,pj->p", J[10], C10i, Jsh[nm]) / np.einsum("pi,ij,pj->p", J[10], C10i, J[10])
    Ash[nm] = (a0, aj)
names = list(shells)
for nm in names:
    a0, aj = Ash[nm]
    log("  %-26s N=%6d  amplitude rel. to D_10 = %.3f +- %.3f   (pair-weight share K1 late/early %.3f/%.3f)" % (nm, int(np.sum(SG2["NN"][:, 0, 0] * 0)) + {names[0]: int((~f20).sum()), names[1]: int((f20 & ~f30).sum()), names[2]: n30}[nm], a0, np.sqrt((NP - 1) / NP * ((aj - aj.mean()) ** 2).sum()),
          shells[nm]["WW"][:, 0, K1].sum() / Sbase["WW"][:, 0, K1].sum(), shells[nm]["WW"][:, 1, K1].sum() / Sbase["WW"][:, 1, K1].sum()))
AJ = np.column_stack([Ash[n][1] for n in names]); A0v = np.array([Ash[n][0] for n in names])
cdiff = np.array([[-1, 1, 0], [-1, 0, 1]], float)
dv = cdiff @ A0v; Cd = covJ((cdiff @ AJ.T).T)
x_dose = float(hart(2) * dv @ np.linalg.solve(Cd, dv))
log("  equality of the three shell amplitudes: contrasts %s  chi2 %.2f / 2  p %.3g" % (np.round(dv, 3), x_dose, pv(x_dose, 2)))
RES["A3"] = dict(A={n: float(Ash[n][0]) for n in names}, err={n: float(np.sqrt((NP - 1) / NP * ((Ash[n][1] - Ash[n][1].mean()) ** 2).sum())) for n in names}, chi2_eq=x_dose, p_eq=pv(x_dose, 2))

# ---------------------------------------------------------------- A4 composition match
log("== A4 composition-matched control (class x 8 mass quantiles x 5 z bins)")
mb = np.zeros(nL, int)
for c in (0, 1):
    m = typ == c
    q = np.quantile(np.log10(Mgal[m]), np.linspace(0, 1, 9)[1:-1])
    mb[m] = np.searchsorted(q, np.log10(Mgal[m]))
zb = np.minimum(((z - 0.1) / 0.08).astype(int), 4)
cell = (typ * 8 + mb) * 5 + zb          # 80 cells
n_iso = np.bincount(cell[f20], minlength=80).astype(float); n_non = np.bincount(cell[~f20], minlength=80).astype(float)
wcell = np.where(n_non > 0, n_iso / np.maximum(n_non, 1), 0.0)
empty = int(np.sum((n_iso > 0) & (n_non == 0)))
wl = wcell[cell]
SG0w = psum(ARR, ~f20, wt=wl)
rw, Jw = jk_of(lambda a, b: Dof(a) - Dof(b), SG0w, WS[20])
Cw = covJ(Jw); xw = chi2v(rw, Cw); dw, sdw, _ = gls(S_, rw, Cw)
log("  cells with iso lenses but no non-isolated lens: %d ; effective N of reweighted G0 = %.0f" % (empty, wl[~f20].sum()**2 / (wl[~f20]**2).sum()))
log("  matched D_non - D_iso: %s  chi2 %.2f/7 p %.3g ; delta = %+.3f +- %.3f  (unmatched %+.3f +- %.3f)" % (np.round(rw, 2), xw, pv(xw, 7), dw, sdw, A2[20]["delta"], A2[20]["sigma_delta"]))
RES["A4"] = dict(chi2=xw, p=pv(xw, 7), delta=dw, sigma=sdw, empty_cells=empty)

# ---------------------------------------------------------------- A5 statement
log("== A5 isolation criterion")
log("  staged: windows |dchi| = 10, 20, 30 Mpc at fixed 3 Mpc radius and 0.1 M* ratio; radius / mass thresholds are NOT variable from the staged data.")

# ---------------------------------------------------------------- A6 error inflation
log("== A6 error inflation")
FS = (1.0, 1.2, 1.5, 1.8, 2.0)
A6 = {}
rows = {"zero W10": X2[10], "zero W20": X2[20], "zero W30": X2[30], "nested r20 (D20-D10)": A2[20]["nested_chi2"], "disjoint r20 (non-iso)": A2[20]["disj_chi2"], "disjoint r30": A2[30]["disj_chi2"]}
log("  %-24s " % "chi2 / f^2 (p)" + "".join("f=%-14.1f" % f for f in FS))
for nm, x in rows.items():
    A6[nm] = [(x / f ** 2, pv(x / f ** 2, 7)) for f in FS]
    log("  %-24s " % nm + "".join("%6.2f (%-7.2g) " % t for t in A6[nm]))
log("  H1 p-condition (p<0.0027) at each f, window 20: %s" % [pv(X2[20] / f ** 2, 7) < 0.0027 for f in FS])
log("  A_20 z-score vs 1 at each f: %s" % [round((A[20][0] - 1) / (A[20][1] * f), 2) for f in FS])
fthr = {}
for nm in ("zero W10", "zero W20", "zero W30"):
    x = rows[nm]; fthr[nm] = {str(p): math.sqrt(x / stats.chi2.isf(p, 7)) for p in (0.0027, 0.05, 0.15)}
    log("  f at which %-9s reaches p = 0.0027 / 0.05 / 0.15: %.2f / %.2f / %.2f" % (nm, fthr[nm]["0.0027"], fthr[nm]["0.05"], fthr[nm]["0.15"]))
RES["A6"] = dict(rows={k: v for k, v in A6.items()}, fthr=fthr)

# ---------------------------------------------------------------- C6 swap controls
log("== C6 swap controls")
def swapE(S): return {k: v[:, ::-1, :] for k, v in S.items()}
mx = 0.0; mxa = 0.0
for W in (10, 20, 30):
    Ds, Js, Cs, xs = zero_chi2(swapE(WS[W]))
    mx = max(mx, abs(xs - X2[W]))
Ds10, Js10, _, _ = zero_chi2(swapE(Sbase)); Ds20, Js20, _, _ = zero_chi2(swapE(WS[20]))
As = ampl(Ds20, Js20, Ds10, Js10)
mxa = max(abs(As[0] - A[20][0]), abs(As[1] - A[20][1]))
check("C6a early<->late swap: chi2 unchanged, A unchanged", mx < 1e-9 and mxa < 1e-9, "max |dchi2| %.2e, max |dA| %.2e" % (mx, mxa))
rb_s, Jb_s = jk_of(lambda a, b: Dof(a) - Dof(b), WS[20], NON[20])
xb_s = chi2v(rb_s, covJ(Jb_s)); dl_s, sd_s, _ = gls(S_, rb_s, covJ(Jb_s))
check("C6b iso<->non swap: chi2(r) unchanged, delta flips", abs(xb_s - A2[20]["disj_chi2"]) < 1e-9 and abs(dl_s + A2[20]["delta"]) < 1e-9, "dchi2 %.2e, delta %+.4f vs %+.4f" % (xb_s - A2[20]["disj_chi2"], dl_s, A2[20]["delta"]))

# ---------------------------------------------------------------- C7 injection recovery
log("== C7 injected-systematic recovery (lens-level injection into WG of early lenses)")
Sb_c = psum(ARR)              # unmutated
e = typ == 1
wk_iso = np.array([WW0[f20 & e, k].sum() / WW0[e, k].sum() for k in range(15)])
D10c, J10c = jk_of(lambda a: Dof(a), Sb_c); C10c = covJ(J10c); C10ci = np.linalg.inv(C10c)
D20c, J20c = jk_of(lambda a: Dof(a), psum(ARR, f20))
A20c = ampl(D20c, J20c, D10c, J10c)[0]
Dnon_c = Dof(totals(psum(ARR, ~f20))); Dis_c = Dof(totals(psum(ARR, f20)))
dl_c, sd_c, _ = gls(D10c, Dnon_c - Dis_c, covJ(jk_of(lambda a, b: Dof(a) - Dof(b), psum(ARR, ~f20), psum(ARR, f20))[1]))
inj_ok = True
for eps, eta in ((0.5, 1.0), (0.5, 0.75)):
    WGi = WG0.copy()
    for jn, k in enumerate(K1):
        a_k = eps * eta * D10c[jn] / (1 - wk_iso[k]); b_k = eps * (1 - eta) * D10c[jn] / wk_iso[k]
        WGi[(~f20) & e, k] += a_k * KG * WW0[(~f20) & e, k]
        WGi[f20 & e, k] += b_k * KG * WW0[f20 & e, k]
    ARi = {"WG": WGi, "WW": WW0, "NN": NN0}
    Sb_i, S20_i, SN_i = psum(ARi), psum(ARi, f20), psum(ARi, ~f20)
    D10i, J10i = jk_of(lambda a: Dof(a), Sb_i); D20i, J20i = jk_of(lambda a: Dof(a), S20_i); DNi = Dof(totals(SN_i))
    ex1 = float(np.max(np.abs(D10i - (1 + eps) * D10c) / np.abs(D10c)))
    a_exact = np.array([eps * eta * D10c[jn] / (1 - wk_iso[k]) for jn, k in enumerate(K1)]); b_exact = np.array([eps * (1 - eta) * D10c[jn] / wk_iso[k] for jn, k in enumerate(K1)])
    ex2 = float(np.max(np.abs((D20i - D20c) - b_exact) / np.abs(D10c))); ex3 = float(np.max(np.abs((DNi - Dnon_c) - a_exact) / np.abs(D10c)))
    Ai = float(D10i @ C10ci @ D20i) / float(D10i @ C10ci @ D10i)   # fixed C10 (the observed) as in the pipeline
    Ai_full = ampl(D20i, J20i, D10i, J10i)
    # analytic first-order (injection ON TOP of the observed base)
    wi = float(np.mean([wk_iso[k] for k in K1]))
    Aexp = (A20c + eps * (1 - eta) / wi) / (1 + eps)
    shift_meas = Ai - A20c; shift_exp = Aexp - A20c
    Cri = covJ(jk_of(lambda a, b: Dof(a) - Dof(b), SN_i, S20_i)[1])
    dli, sdi, _ = gls(D10c, DNi - D20i, Cri)
    dexp = dl_c + eps * (eta / (1 - wi) - (1 - eta) / wi)
    okA = abs(shift_meas - shift_exp) <= max(0.10 * abs(shift_exp), 0.02)
    okd = abs(dli - dexp) <= max(0.10 * abs(dexp - dl_c), 0.02)
    ok = ex1 < 1e-9 and ex2 < 1e-9 and ex3 < 1e-9 and okA and okd
    inj_ok = inj_ok and ok
    log("  eps %.2f eta %.2f: exact bookkeeping D10 rise %.1e, D_iso shift %.1e, D_non shift %.1e (relative, <=1e-9) ; A_20 %.3f -> %.3f (analytic %.3f; H1 A-cond: |A-1|<=2 sigma_A ? %s) ; delta %+.3f -> %+.3f (analytic %+.3f, %.1f sigma, 1-dof detect: %s)" %
        (eps, eta, ex1, ex2, ex3, A20c, Ai, Aexp, abs(Ai_full[0] - 1) <= 2 * Ai_full[1], dl_c, dli, dexp, dli / sdi, dli / sdi > 1.645))
check("C7 injection recovery", inj_ok, "exact bookkeeping and first-order analytic (10 % / 0.02 abs) for both (eps, eta)")

# ---------------------------------------------------------------- C8 power machinery
log("== C8 power machinery")
rng = np.random.default_rng(109)
a2 = A2[20]; Cb = np.array(a2["Cb"]); wi = a2["wiso"]["early"]
lam = (0.5 * (1 / (1 - wi))) ** 2 * a2["sPs"]     # eps=.5, eta=1: delta = eps/w_non
pan = float(stats.ncx2.sf(stats.chi2.isf(0.05, 7), 7, lam))
Lc = np.linalg.cholesky(Cb); dtrue = 0.5 / (1 - wi)
nmc = 200000
r_mc = dtrue * S_[None, :] + rng.standard_normal((nmc, 7)) @ Lc.T
Pb = hart(7) * np.linalg.inv(Cb)
x_mc = np.einsum("ni,ij,nj->n", r_mc, Pb, r_mc)
pmc = float(np.mean(x_mc > stats.chi2.isf(0.05, 7)))
check("C8a analytic vs MC omnibus power (eps .5, eta 1, W20)", abs(pan - pmc) <= 0.01, "analytic %.4f, MC %.4f, lambda %.2f" % (pan, pmc, lam))
dh = (r_mc @ Pb @ S_) / a2["sPs"]
zz = (dh - dtrue) / a2["sigma_delta"]
check("C8b MC GLS delta_hat unbiased and correctly scaled", abs(zz.mean()) <= 0.02 and 0.98 <= zz.std() <= 1.02, "mean %+.4f std %.4f" % (zz.mean(), zz.std()))

# ---------------------------------------------------------------- A7 permutations (main run only)
if not MUTATE:
    log("== A7 permutation calibration (seed 109, B=1000)")
    NPERM = 1000
    rng = np.random.default_rng(109)
    WGk, WWk = WG0[:, K1], WW0[:, K1]
    idx0 = np.argsort(patch, kind="stable")
    def sums7(wg, ww, key, m=None):
        if m is not None: wg, ww, key = wg[m], ww[m], key[m]
        out = np.empty((2, NP * 2, 7))
        for j in range(7):
            out[0, :, j] = np.bincount(key, weights=wg[:, j], minlength=NP * 2); out[1, :, j] = np.bincount(key, weights=ww[:, j], minlength=NP * 2)
        return out.reshape(2, NP, 2, 7)
    def d7(s):   # s (2,...,2,7) ; returns early - late
        e_ = s[0] / s[1] / KG
        return e_[..., 1, :] - e_[..., 0, :]
    def chi_from_S(s):
        T = s.sum(1); Dfull = d7(T); Jl = d7(T[:, None] - s)
        return Dfull, Jl, chi2v(Dfull, covJ(Jl))
    # observed check (must equal the analytic pipeline)
    key_o = patch * 2 + typ
    sB = sums7(WGk, WWk, key_o); sI = sums7(WGk, WWk, key_o, f20)
    _, _, xo_B = chi_from_S(sB); _, _, xo_I = chi_from_S(sI)
    check("A7 perm estimator reproduces the observed chi2 (W10, W20)", abs(xo_B - X2[10]) < 1e-8 and abs(xo_I - X2[20]) < 1e-8, "%.6f vs %.6f ; %.6f vs %.6f" % (xo_B, X2[10], xo_I, X2[20]))
    nB = np.empty(NPERM); nI = np.empty(NPERM)
    for b in range(NPERM):
        order = np.lexsort((rng.random(nL), patch)); tn = np.empty(nL, int); tn[idx0] = typ[order]
        keyp = patch * 2 + tn
        nB[b] = chi_from_S(sums7(WGk, WWk, keyp))[2]; nI[b] = chi_from_S(sums7(WGk, WWk, keyp, f20))[2]
    pB = (1 + np.sum(nB >= X2[10])) / (NPERM + 1); pI = (1 + np.sum(nI >= X2[20])) / (NPERM + 1)
    log("  (a) class-label permutations: base null mean %.2f, 99th pct %.2f, observed %.2f, empirical p %.4g ; iso20 null mean %.2f, 99th %.2f, observed %.2f, empirical p %.4g  (floor %.4g)" %
        (nB.mean(), np.percentile(nB, 99), X2[10], pB, nI.mean(), np.percentile(nI, 99), X2[20], pI, 1 / (NPERM + 1)))
    # (b) group labels
    block = (patch * 2 + typ) * 80 + (cell % 40)    # patch x class x (mass bin x z bin)
    idxb = np.argsort(block, kind="stable")
    sBase7 = sums7(WGk, WWk, key_o)
    sIso = sums7(WGk, WWk, key_o, f20)
    def r_stat(sI_):
        sN_ = sBase7 - sI_
        T_I, T_N = sI_.sum(1), sN_.sum(1)
        rfull = d7(T_N) - d7(T_I); Jl = d7(T_N[:, None] - sN_) - d7(T_I[:, None] - sI_)  # careful: LOO of totals
        return rfull, Jl
    def r_stat2(sI_):
        sN_ = sBase7 - sI_
        TI, TN = sI_.sum(1), sN_.sum(1)
        rfull = d7(TN) - d7(TI)
        Jl = d7(TN[:, None] - sN_) - d7(TI[:, None] - sI_)
        return rfull, Jl
    rf, Jl = r_stat2(sIso); Cl = covJ(Jl)
    xo_r = chi2v(rf, Cl); Pl = hart(7) * np.linalg.inv(Cl); zo = float(S_ @ Pl @ rf) / math.sqrt(float(S_ @ Pl @ S_))
    check("A7 perm (b) estimator reproduces observed disjoint chi2", abs(xo_r - A2[20]["disj_chi2"]) < 1e-8, "%.6f vs %.6f ; z(delta) %.3f vs %.3f" % (xo_r, A2[20]["disj_chi2"], zo, A2[20]["delta"] / A2[20]["sigma_delta"]))
    nX = np.empty(NPERM); nZ = np.empty(NPERM)
    for b in range(NPERM):
        order = np.lexsort((rng.random(nL), block)); fn = np.empty(nL, bool); fn[idxb] = f20[order]
        rf, Jl = r_stat2(sums7(WGk, WWk, key_o, fn)); Cl = covJ(Jl)
        nX[b] = chi2v(rf, Cl); Pl = hart(7) * np.linalg.inv(Cl); nZ[b] = float(S_ @ Pl @ rf) / math.sqrt(float(S_ @ Pl @ S_))
    pX = (1 + np.sum(nX >= xo_r)) / (NPERM + 1); pZ = (1 + np.sum(nZ >= zo)) / (NPERM + 1)
    log("  (b) group-label permutations (iso20 vs non, within patch x class x cell): null chi2 mean %.2f, 99th %.2f, observed %.2f, empirical p %.4g ; z(delta) null mean %+.3f std %.3f, observed %.2f, one-sided empirical p(>=) %.4g" %
        (nX.mean(), np.percentile(nX, 99), xo_r, pX, nZ.mean(), nZ.std(), zo, pZ))
    check("C9 permutation nulls sane", all(5.5 <= v <= 8.5 for v in (nB.mean(), nI.mean(), nX.mean())) and abs(nZ.mean()) <= 0.1 and 0.9 <= nZ.std() <= 1.1,
          "means %.2f %.2f %.2f ; z mean %+.3f std %.3f" % (nB.mean(), nI.mean(), nX.mean(), nZ.mean(), nZ.std()))
    RES["A7"] = dict(base=dict(mean=float(nB.mean()), p99=float(np.percentile(nB, 99)), p_emp=float(pB)), iso20=dict(mean=float(nI.mean()), p99=float(np.percentile(nI, 99)), p_emp=float(pI)),
                     group=dict(mean=float(nX.mean()), p99=float(np.percentile(nX, 99)), obs=xo_r, p_emp=float(pX), zmean=float(nZ.mean()), zstd=float(nZ.std()), zobs=zo, pz=float(pZ)))
else:
    log("== A7/C9 skipped in MUTATE (declared: permutation nulls are a main-run control)")

# ---------------------------------------------------------------- MUTATE teeth
if MUTATE:
    check("C10 MUTATE: difference-of-splits (b) rejects", A2[20]["disj_p"] < 0.0027, "chi2 %.2f p %.3g" % (A2[20]["disj_chi2"], A2[20]["disj_p"]))
    check("C10 MUTATE: A_20 = -A_20(main)", abs(A[20][0] + 0.97) < 0.0051, "A_20 %.4f" % A[20][0])

# ---------------------------------------------------------------- reproduction
log("== reproduction against CFG96's printed numbers")
if not MUTATE:
    for W, N_, tgt in ((10, 181477, 181477), (20, 93020, 93020), (30, 57265, 57265)):
        cmp("P0 count W%d" % W, COMP[W]["N"], tgt, 0)
    for W, t in ((10, 48.5), (20, 48.0), (30, 46.4)): cmp("P0 early fraction W%d (%%)" % W, 100 * COMP[W]["early"], t, 0.05)
    for W, t, tp, ts in ((10, 35.04, 1.1e-5, 4.4), (20, 32.02, 4.0e-5, 4.1), (30, 19.12, 7.8e-3, 2.7)):
        cmp("P1 chi2 W%d" % W, X2[W], t, 0.01)
        p = pv(X2[W], 7); cmp("P1 p W%d (2 s.f. rel.)" % W, float(f"{p:.1e}"), tp, 0.051 * tp)
        cmp("P1 sigma W%d" % W, sig(p), ts, 0.05)
    cmp("P2 A_20", A[20][0], 0.97, 0.005); cmp("P2 sigma_A20", A[20][1], 0.19, 0.005)
    cmp("P2 A_30", A[30][0], 1.17, 0.005); cmp("P2 sigma_A30", A[30][1], 0.27, 0.005)
    for W, t in ((10, 84.8), (20, 54.6), (30, 26.1)): cmp("P3 all-15 chi2 W%d" % W, X15[W], t, 0.05)
    cmp("P4 ratio min", ratio20.min(), 0.44, 0.005); cmp("P4 ratio max", ratio20.max(), 2.66, 0.005)
    check("P6 H1 passes in the main run", H1, "H1 %s" % H1)
else:
    cmp("P5 MUTATE A_20", A[20][0], -0.97, 0.005)
    check("P5 MUTATE H1 fails as required", not H1, "H1 %s" % H1)

# ---------------------------------------------------------------- verdict
ctrl = [k for k in checks if k[0] == "C" or k.startswith("K1") or k.startswith("A7")]
nfail = [k for k in ctrl if not checks[k]]
log("== summary: controls failed: %s" % nfail)
if MUTATE:
    ok = (not H1) and not nfail
    log("MUTATE exit %s" % ("1 (H1 failed as required)" if ok else "2 (control failure)"))
    rc = 1 if ok else 2
else:
    rc = 0 if (H1 and not nfail) else 1
    log("main exit %d" % rc)
RES["checks"] = checks; RES["repro"] = repro; RES["rc"] = rc
json.dump(RES, open(OUT, "w"), default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o), indent=1)
log("elapsed %.0f s" % (time.time() - T0))
sys.exit(rc)
