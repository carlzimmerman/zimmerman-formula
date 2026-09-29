
# ======================================================================================================================================
import os, sys, json, math, time, hashlib, warnings
import numpy as np
from scipy import stats, optimize
warnings.filterwarnings("ignore", category=RuntimeWarning)      # numpy/Accelerate spurious matmul warnings (CFG77/CFG100); K4 cross-checks the algebra
import cfg107_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE") == "1"
OUTJSON = os.path.join(HERE, "cfg107_results_MUTATE.json" if MUTATE else "cfg107_results.json")
T0 = time.time()
def log(*a): print(*a, flush=True)
FROZEN_SHA = hashlib.sha256(open(os.path.join(HERE, "cfg107_FROZEN.txt"), "rb").read()).hexdigest()
log("CFG107  MUTATE=%d  frozen-text sha256 %s" % (MUTATE, FROZEN_SHA[:16]))
np.set_printoptions(linewidth=200, precision=4, suppress=True)
NP = 50
KG = 1.98847e30 / (3.0857e16) ** 2
checks = {}
def check(name, ok, msg):
    checks[name] = bool(ok)
    log("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))
R = {}          # results json
repro = []      # (name, mine, target, tol, status)
def cmp(name, mine, target, tol):
    d = abs(mine - target)
    st = "REPRODUCED" if d <= tol else ("APPROXIMATE" if d <= 0.10 * abs(target) else "NOT REPRODUCED")
    repro.append((name, float(mine), float(target), float(tol), st))
    log("    %-46s mine %-11.5g CFG115 %-9.5g tol %-7.3g  %s" % (name, mine, target, tol, st))
def hart(p): return (NP - p - 2) / (NP - 1)

# ------------------------------------------------------------------ inputs
lens = np.load(os.path.join(L.DATA, "lr_lenses.npz"))
ra, dec, z, Mgal, typ = lens["ra"], lens["dec"], lens["z"], lens["Mgal"], lens["typ"]
logMs = lens["logM"]; lmg = np.log10(Mgal)
jk = np.load(os.path.join(L.DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
pl = np.load(os.path.join(L.DATA, "cfg110_perlens.npz")); WG0, WW, NN = pl["WG"].copy(), pl["WW"], pl["NN"]
assert np.allclose(pl["gbar_edges"], L.GEDGE) and np.allclose(jk["gbar_edges"], L.GEDGE)
nL = len(z)
gcen = np.sqrt(L.GEDGE[:-1] * L.GEDGE[1:]) / L.SI_ACC

log("== controls on inputs")
mx = 0.0
for name, a, b in (("WG", WG0, jk["wgE"]), ("WW", WW, jk["W"]), ("NN", NN, jk["NN"])):
    for c in (0, 1):
        for p in range(NP):
            m = (patch == p) & (typ == c)
            s = a[m].sum(0); r = b[p, c]
            mx = max(mx, float(np.max(np.abs(s - r) / np.maximum(np.abs(r), 1e-300))))
check("K1 per-patch sums vs June", mx <= 1e-9, "max relative deviation %.2e (<= 1e-9)" % mx)

Rmed = np.array([[np.median(np.sqrt(L.G_MPC * Mgal[typ == c] / g)) for g in gcen] for c in (0, 1)])
K1 = [k for k in range(15) if Rmed[0, k] < 0.3 and Rmed[1, k] < 0.3]
check("K2a K1 bins", K1 == list(range(8, 15)), "K1 = %s" % K1)
K1 = np.array(K1)

# ------------------------------------------------------------------ colour join (LePhare rest-frame u-r), exact (RA,Dec)
from astropy.io import fits
def fits_cols(fn, cols):
    with fits.open(os.path.join(L.DATA, fn), memmap=True) as h:
        d = h[1].data
        return {c: np.array(d[c]) for c in cols}
br = fits_cols("KiDS_DR4_brightsample.fits", ["ID", "RAJ2000", "DECJ2000"])
lp = fits_cols("KiDS_DR4_brightsample_LePhare.fits", ["ID", "RAJ2000", "DECJ2000", "MAG_ABS_u", "MAG_ABS_r"])
id_equal = bool(np.array_equal(br["ID"], lp["ID"])) and bool(np.array_equal(br["RAJ2000"], lp["RAJ2000"])) and bool(np.array_equal(br["DECJ2000"], lp["DECJ2000"]))
cat = br["RAJ2000"].astype(np.float64) + 1j * br["DECJ2000"].astype(np.float64)
order = np.argsort(cat, kind="stable"); cs = cat[order]
q = ra.astype(np.float64) + 1j * dec.astype(np.float64)
lo = np.searchsorted(cs, q, side="left"); hi = np.searchsorted(cs, q, side="right")
found = (hi - lo) >= 1
mult = hi - lo
row = order[np.minimum(lo, len(cs) - 1)]
ur_all = lp["MAG_ABS_u"].astype(np.float64) - lp["MAG_ABS_r"].astype(np.float64)
u = ur_all[row]
cls_ok = bool(np.all((u > 2.0).astype(int) == typ))
check("K3 LePhare join", bool(found.all()) and id_equal and cls_ok and np.isfinite(u).all(),
      "matched %d/%d exactly (multiple catalogue rows for %d lenses); IDs+positions row-aligned %s; (u-r>2.0)==typ for all: %s; finite u-r %d" %
      (int(found.sum()), nL, int((mult > 1).sum()), id_equal, cls_ok, int(np.isfinite(u).sum())))
R["join"] = dict(matched=int(found.sum()), multi=int((mult > 1).sum()), id_equal=id_equal, cls_ok=cls_ok)

# ------------------------------------------------------------------ binning
def binning(cuts, split=2.0, uu=None):
    uu = u if uu is None else uu
    cl = (uu > split).astype(int)
    lab = -np.ones(nL, int); cls = []; ub = []; ucl = []; edges = []; nb = 0
    for c in (0, 1):
        m = cl == c
        qv = np.quantile(uu[m], cuts)
        idx = np.searchsorted(qv, uu, side="right")
        for j in range(len(cuts) + 1):
            mm = m & (idx == j); lab[mm] = nb; cls.append(c); ub.append(float(np.median(uu[mm]))); nb += 1
        ucl.append(float(np.median(uu[m]))); edges.append(qv)
    return dict(lab=lab, cls=np.array(cls), u=np.array(ub), uclass=np.array(ucl), nb=nb, edges=edges, cl=cl,
                masks=[lab == j for j in range(nb)])
B6 = binning([1 / 3, 2 / 3])
names6 = ["L1", "L2", "L3", "E1", "E2", "E3"]
ed = np.concatenate(B6["edges"])
check("K3b tertile edges", np.allclose(ed, [1.507, 1.749, 2.228, 2.351], atol=0.002), "edges %s (expected 1.507 1.749 2.228 2.351 +-0.002)" % np.round(ed, 4))
Nbin = np.array([m.sum() for m in B6["masks"]])
log("  bin N %s   (CFG115: 31030 31222 31146 29313 29135 29631)" % Nbin)
log("  bin median u-r %s (CFG115: 1.344 1.632 1.870 2.128 2.297 2.401); class medians %s" % (np.round(B6["u"], 3), np.round(B6["uclass"], 3)))
allm = np.ones(nL, bool)

# ------------------------------------------------------------------ K2b partition
def psum(mask, arr, ks, w=None):
    idx = np.flatnonzero(mask)
    out = np.zeros((NP, len(ks)))
    ww = None if w is None else w[idx]
    for j, k in enumerate(ks):
        a = arr[idx, k] if ww is None else arr[idx, k] * ww
        out[:, j] = np.bincount(patch[idx], weights=a, minlength=NP)
    return out
cover = sum(m.astype(int) for m in B6["masks"])
sm = sum(psum(m, WG0, K1) for m in B6["masks"]); sf = psum(allm, WG0, K1)
smw = sum(psum(m, WW, K1) for m in B6["masks"]); sfw = psum(allm, WW, K1)
scl = max(np.max(np.abs(sm - sf) / np.abs(sf).max()), np.max(np.abs(smw - sfw) / np.abs(sfw).max()))
scls = 0.0
for c in (0, 1):
    a = sum(psum(m, WG0, K1) for j, m in enumerate(B6["masks"]) if B6["cls"][j] == c); b = psum(typ == c, WG0, K1)
    scls = max(scls, np.max(np.abs(a - b)) / np.abs(b).max())
check("K2b partition / sums", bool(np.all(cover == 1)) and scl < 1e-12 and scls < 1e-12, "each lens in exactly one bin: %s; six-bin vs full K1 sums %.1e; vs class sums %.1e (both <1e-12)" % (bool(np.all(cover == 1)), scl, scls))

# ------------------------------------------------------------------ amplitudes
ALL_W = psum(allm, WW, list(range(15)))          # (50,15) full-sample pair-weight sums per patch (unmodified)
def amps(masks, refs, WGa, WWa, ks, kind="jkref", wk=None, refWG=None, refWW=None, lin=False):
    """masks, refs: lists (same length) of boolean lens masks; returns A_full (nb,), A_loo (NP,nb).
    kind: jkref | fixref | jkw.  w_k default: sum over the ref sample of WWa (fixed) -- for the primary the ref is all lenses."""
    ks = list(ks); nb = len(masks)
    cacheref = {}
    def refstats(rm):
        key = id(rm)
        if key not in cacheref:
            wg = psum(rm, WGa if refWG is None else refWG, ks); w = psum(rm, WWa if refWW is None else refWW, ks)
            cacheref[key] = (wg, w)
        return cacheref[key]
    Afull = np.zeros(nb); Aloo = np.zeros((NP, nb))
    if lin:
        tf = lambda x: x - 1.0
    else:
        def tf(x):
            x = np.asarray(x, float)
            if np.any(x <= 0): raise ValueError("non-positive weighted ESD ratio: log amplitude undefined")
            return np.log10(x)
    for c in range(nb):
        wgc = psum(masks[c], WGa, ks); wc = psum(masks[c], WWa, ks)
        wgr, wr = refstats(refs[c])
        tg, tw = wgc.sum(0), wc.sum(0); rg, rw = wgr.sum(0), wr.sum(0)
        e_full = tg / tw; e_loo = (tg[None] - wgc) / (tw[None] - wc)
        r_full = rg / rw; r_loo = (rg[None] - wgr) / (rw[None] - wr)
        if wk is None:
            wfix = rw.copy(); wloo = rw[None] - wr
        else:
            wfix = wk; wloo = None
        Afull[c] = float(tf((wfix * e_full).sum() / (wfix * r_full).sum()))
        if kind == "jkref":
            Aloo[:, c] = tf((e_loo * wfix[None]).sum(1) / (r_loo * wfix[None]).sum(1))
        elif kind == "fixref":
            Aloo[:, c] = tf((e_loo * wfix[None]).sum(1) / (wfix * r_full).sum())
        elif kind == "jkw":
            wl = wloo if wloo is not None else np.repeat(wfix[None], NP, 0)
            Aloo[:, c] = tf((e_loo * wl).sum(1) / (r_loo * wl).sum(1))
    return Afull, Aloo
def jkcov(Aloo):
    d = Aloo - Aloo.mean(0)
    return (NP - 1) / NP * d.T @ d

# ------------------------------------------------------------------ models / fits
def designs(cls, ub, ucl):
    cls = np.asarray(cls); nb = len(cls)
    ind0 = (cls == 0).astype(float); ind1 = (cls == 1).astype(float)
    return dict(M0=np.zeros((nb, 0)), M0off=np.ones((nb, 1)), step=np.c_[ind0, ind1], grad=np.c_[np.ones(nb), ub - 2.0],
                stepslope=np.c_[ind0, ind1, ub - np.asarray(ucl)[cls]])
def gls(X, A, P):
    if X.shape[1] == 0:
        return np.zeros(0), np.zeros((0, 0)), float(A @ P @ A), A.copy()
    F = X.T @ P @ X; Fi = np.linalg.inv(F); b = Fi @ (X.T @ P @ A); r = A - X @ b
    return b, Fi, float(r @ P @ r), r
def fit_all(A, C, cls, ub, ucl, f=1.0, use_h=True):
    nb = len(A); h = hart(nb) if use_h else 1.0
    P = h * np.linalg.inv(C) / f ** 2
    D = designs(cls, ub, ucl); out = {}
    for k, X in D.items():
        b, Fi, chi, r = gls(X, A, P)
        out[k] = dict(beta=b, err=np.sqrt(np.diag(Fi)) if X.shape[1] else np.zeros(0), chi2=chi, dof=nb - X.shape[1])
    out["dchi_slope"] = out["step"]["chi2"] - out["stepslope"]["chi2"]
    out["dchi_step_grad"] = out["step"]["chi2"] - out["grad"]["chi2"]
    return out, P, D
def pv(chi, dof): return float(stats.chi2.sf(chi, dof)) if dof > 0 else float("nan")

def power_row(A, C, cls, ub, ucl, ucls_lens, label="primary", verbose=True):
    F, P, D = fit_all(A, C, cls, ub, ucl)
    sL, sE = F["step"]["beta"]
    bt = (sE - sL) / (ucls_lens[1] - ucls_lens[0])
    mu = bt * ub
    _, _, lam, _ = gls(D["step"], mu, P)
    sig = F["stepslope"]["err"][2]
    return bt, lam, sig

# ------------------------------------------------------------------ analysis driver
def analyse(WGa, tag, B=B6, verbose=True):
    ks = K1
    res = {}
    Afull = {}; C = {}
    for kind in ("jkref", "fixref", "jkw"):
        Af, Al = amps(B["masks"], [allm] * B["nb"], WGa, WW, ks, kind, wk=psum(allm, WW, ks).sum(0) if kind != "jkw" else None)
        Afull[kind] = Af; C[kind] = jkcov(Al); res[kind + "_Aloo"] = Al
    return Afull, C, res

# ==================================================================================================================================
def main_analysis(WGa, verbose=True):
    """primary results on the data array WGa; returns dict"""
    Afull, C, res = analyse(WGa, "main")
    A = Afull["jkref"]; Cp = C["jkref"]
    out = dict(A=A, C=Cp, Afull=Afull, Cs=C, res=res)
    F, P, D = fit_all(A, Cp, B6["cls"], B6["u"], B6["uclass"])
    out["F"] = F
    ucls_l = B6["uclass"]
    bt, lam, sig = power_row(A, Cp, B6["cls"], B6["u"], B6["uclass"], ucls_l)
    out.update(bt=bt, lam=lam, sig_bw=sig)
    return out

log("== main analysis (unmodified data)")
W0 = main_analysis(WG0)
A0, C0 = W0["A"], W0["C"]
F0 = W0["F"]
sig0 = np.sqrt(np.diag(C0))
log("  amplitudes A_c (dex): %s" % np.round(A0, 4))
log("  errors sqrt(diag C) : %s" % np.round(sig0, 4))
h6 = hart(6)
log("  Hartlap h(p=6) = %.5f" % h6)
log("  R0/R1-R2 fits (Hartlap P = h C^-1):")
for k in ("M0", "M0off", "step", "grad", "stepslope"):
    f = F0[k]; log("    %-9s chi2 %8.3f / %d  p %.3g   beta %s +- %s" % (k, f["chi2"], f["dof"], pv(f["chi2"], f["dof"]), np.round(f["beta"], 4), np.round(f["err"], 4)))
log("    dchi2(step - step+slope) = %.3f   chi2(step) - chi2(grad) = %.3f" % (F0["dchi_slope"], F0["dchi_step_grad"]))
log("  power row: beta_true = %.4f dex/mag, sigma(beta_w) = %.4f, lambda = %.3f (threshold 9); 1-dof power at alpha 0.05 = %.3f" %
    (W0["bt"], W0["sig_bw"], W0["lam"], float(stats.ncx2.sf(stats.chi2.ppf(0.95, 1), 1, W0["lam"]))))
if MUTATE:
    bt_inj = W0["bt"]; bw_main = F0["stepslope"]["beta"][2]; sig_main = F0["stepslope"]["err"][2]
    log("== MUTATE: injecting per-lens factor 10^(beta_inj (u-r - ubar_class)), beta_inj = %.4f, into WG (K1 bins)" % bt_inj)
    ucl_lens = np.where(typ == 0, B6["uclass"][0], B6["uclass"][1])
    # class assignment by colour (equal to typ, control K3)
    fac = 10.0 ** (bt_inj * (u - np.where(u > 2.0, B6["uclass"][1], B6["uclass"][0])))
    WGm = WG0.copy(); WGm[:, K1] *= fac[:, None]
    Wm = main_analysis(WGm)
    Fm = Wm["F"]
    log("  MUTATED amplitudes: %s" % np.round(Wm["A"], 4))
    for k in ("M0off", "step", "grad", "stepslope"):
        f = Fm[k]; log("    %-9s chi2 %8.3f / %d  p %.3g  beta %s +- %s" % (k, f["chi2"], f["dof"], pv(f["chi2"], f["dof"]), np.round(f["beta"], 4), np.round(f["err"], 4)))
    bw_m = Fm["stepslope"]["beta"][2]
    inc = bw_m - bw_main
    H1m = (pv(Fm["step"]["chi2"], 4) > 0.05) and (Fm["dchi_slope"] < 4)
    H1u = (pv(F0["step"]["chi2"], 4) > 0.05) and (F0["dchi_slope"] < 4)
    log("  beta_w main %.4f +- %.4f -> MUTATE %.4f +- %.4f (increase %.4f vs injected %.4f)" % (bw_main, sig_main, bw_m, Fm["stepslope"]["err"][2], inc, bt_inj))
    check("K7 MUTATE recovery", abs(inc - bt_inj) <= 0.30 * bt_inj, "increase %.3f within +-30%% of injected %.3f" % (inc, bt_inj))
    log("  H1 main: %s;  H1 MUTATE: %s" % ("PASS" if H1u else "FAIL", "PASS" if H1m else "FAIL"))
    cmp("P8 MUTATE beta_w", bw_m, 0.739, 0.005)
    log("  MUTATE: H1 %s (must FAIL for the control to be informative-by-failure; main run H1 %s => %s)" % ("FAILS" if not H1m else "PASSES", "fails" if not H1u else "passes",
        "uninformative for H1" if not H1u else "informative for H1"))
    R["mutate"] = dict(beta_inj=bt_inj, bw_main=bw_main, bw_mut=bw_m, H1_mut=bool(H1m), H1_main=bool(H1u))
    json.dump(R, open(OUTJSON, "w"), indent=1, default=float)
    nfail = sum(not v for v in checks.values())
    log("  controls: %d/%d pass;  elapsed %.0fs" % (len(checks) - nfail, len(checks), time.time() - T0))
    rc = 1 if (not H1m or nfail) else 0
    log("RC %d" % rc); sys.exit(rc)

# ------------------------------------------------------------------ MAIN ONLY BELOW
H1_step = pv(F0["step"]["chi2"], 4) > 0.05
H1_slope = F0["dchi_slope"] < 4
H1 = bool(H1_step and H1_slope)
log("  H1 (step: p(step)>0.05 [%s] and dchi2<4 [%s]) -> %s" % (H1_step, H1_slope, "PASS" if H1 else "FAIL"))
R["A"] = A0.tolist(); R["err"] = sig0.tolist(); R["H1"] = H1
R["fits"] = {k: dict(chi2=F0[k]["chi2"], dof=F0[k]["dof"], beta=F0[k]["beta"].tolist(), err=F0[k]["err"].tolist()) for k in ("M0", "M0off", "step", "grad", "stepslope")}
R["power"] = dict(beta_true=W0["bt"], lam=W0["lam"], sig=W0["sig_bw"])

log("== reproduction lines (main data, primary definitions)")
for j, (nm, tA, tE) in enumerate(zip(names6, [-0.165, -0.267, -0.049, -0.049, 0.050, 0.123], [0.077, 0.077, 0.039, 0.034, 0.031, 0.024])):
    cmp("P1 A(%s)" % nm, A0[j], tA, 0.002); cmp("P1 err(%s)" % nm, sig0[j], tE, 0.002)
cmp("P2 chi2 step", F0["step"]["chi2"], 18.1, 0.06); cmp("P2 chi2 gradient", F0["grad"]["chi2"], 6.3, 0.06)
cmp("P2 chi2 step+slope", F0["stepslope"]["chi2"], 5.34, 0.06); cmp("P2 dchi2 slope", F0["dchi_slope"], 12.77, 0.06)
cmp("P2 chi2 B null (free offset)", F0["M0off"]["chi2"], 36.3, 0.1)
cmp("P3 lambda", W0["lam"], 4.8, 0.05); cmp("P3 beta_true", W0["bt"], 0.270, 0.002)
cmp("P4 gradient slope", F0["grad"]["beta"][1], 0.34, 0.005); cmp("P4 gradient slope err", F0["grad"]["err"][1], 0.06, 0.005)
cmp("P4 within-class slope", F0["stepslope"]["beta"][2], 0.441, 0.005); cmp("P4 within-class slope err", F0["stepslope"]["err"][2], 0.123, 0.005)
cmp("P6 M0 zero offset (jk ref)", F0["M0"]["chi2"], 305.0, 1.0)

# ---- R6 / A1 amplitude definition table
log("== R6 / A1: amplitude-definition attack")
DEF = {}
for kind in ("jkref", "fixref", "jkw"):
    C = W0["Cs"][kind]; ev = np.linalg.eigvalsh(C); cond = ev[-1] / ev[0]
    Fk, Pk, Dk = fit_all(A0, C, B6["cls"], B6["u"], B6["uclass"])
    Fk_noh, _, _ = fit_all(A0, C, B6["cls"], B6["u"], B6["uclass"], use_h=False)
    DEF[kind] = dict(cond=cond, evmin=ev[0], evmax=ev[-1], err=np.sqrt(np.diag(C)), F=Fk)
    log("  [%s] cond %.1f  eig min %.3g max %.3g  errors %s" % (kind, cond, ev[0], ev[-1], np.round(np.sqrt(np.diag(C)), 4)))
    log("      chi2: M0 %.2f  M0off %.2f  step %.3f  grad %.3f  stepslope %.3f  dchi2 %.3f  | beta_grad %.4f+-%.4f beta_w %.4f+-%.4f" %
        (Fk["M0"]["chi2"], Fk["M0off"]["chi2"], Fk["step"]["chi2"], Fk["grad"]["chi2"], Fk["stepslope"]["chi2"], Fk["dchi_slope"],
         Fk["grad"]["beta"][1], Fk["grad"]["err"][1], Fk["stepslope"]["beta"][2], Fk["stepslope"]["err"][2]))
R["defs"] = {k: dict(cond=float(v["cond"]), evmin=float(v["evmin"]), evmax=float(v["evmax"]), err=v["err"].tolist(),
             chi2={m: v["F"][m]["chi2"] for m in ("M0", "M0off", "step", "grad", "stepslope")}) for k, v in DEF.items()}
cmp("P5 cond jkref", DEF["jkref"]["cond"], 3200, 160); cmp("P5 cond fixref", DEF["fixref"]["cond"], 10.8, 0.1); cmp("P5 eigmin jkref", DEF["jkref"]["evmin"], 2.2e-6, 1.1e-7)
# pseudo-inverse (post hoc row in CFG115; reported)
C = W0["Cs"]["jkref"]; ev, V = np.linalg.eigh(C); Vk = V[:, 1:]
Ppi = h6 * (Vk / ev[1:]) @ Vk.T
D6 = designs(B6["cls"], B6["u"], B6["uclass"])
cs, cslope = gls(D6["step"], A0, Ppi)[2], gls(D6["stepslope"], A0, Ppi)[2]
log("  pseudo-inverse dropping the smallest eigen-direction of C_jkref: step chi2 %.3f, step+slope %.3f, dchi2 %.3f (CFG115 post hoc: 0.19)" % (cs, cslope, cs - cslope))
R["pinv"] = dict(step=cs, stepslope=cslope, d=cs - cslope)

# ---- K4 closed-form projection limits
log("== K4 closed-form controls")
P0 = h6 * np.linalg.inv(C0)
maxd = 0.0
for nm in ("step", "grad", "stepslope"):
    X = D6[nm]
    b1 = np.linalg.solve(X.T @ P0 @ X, X.T @ P0 @ A0)
    Lc = np.linalg.cholesky(P0); Xw = Lc.T @ X; Aw = Lc.T @ A0
    b2 = np.linalg.lstsq(Xw, Aw, rcond=None)[0]
    fun = lambda b: float((A0 - X @ b) @ P0 @ (A0 - X @ b))
    b3 = optimize.minimize(fun, b1 * 0.5 + 0.01, method="BFGS", options=dict(gtol=1e-12)).x
    dchol = max(np.max(np.abs(b1 - b2)), abs(fun(b1) - F0[nm]["chi2"])); dbfgs = np.max(np.abs(b1 - b3))
    log("    K4a %-9s |normal-eq - Cholesky-lstsq| %.2e ; |normal-eq - BFGS| %.2e" % (nm, dchol, dbfgs))
    # post hoc: BFGS in whitened coordinates, tighter
    b4 = optimize.minimize(lambda b: float(np.sum((Aw - Xw @ b) ** 2)), b1 * 0.5 + 0.01, jac=lambda b: -2 * Xw.T @ (Aw - Xw @ b), method="BFGS", options=dict(gtol=1e-14)).x
    log("    K4a %-9s post hoc BFGS on the whitened problem with analytic gradient: %.2e" % (nm, np.max(np.abs(b1 - b4))))
    maxd = max(maxd, np.max(np.abs(b1 - b2)), np.max(np.abs(b1 - b3)), abs(fun(b1) - F0[nm]["chi2"]))
check("K4a GLS = Cholesky = BFGS (frozen 1e-8)", maxd < 1e-8, "max deviation %.2e (see the per-model lines: the BFGS leg is a numerical-optimiser limit, the algebraic legs agree to ~1e-12; post hoc row above)" % maxd)
sbw = F0["stepslope"]["err"][2]; bw = F0["stepslope"]["beta"][2]
check("K4b nested identity", abs(F0["dchi_slope"] - (bw / sbw) ** 2) < 1e-9, "dchi2 %.9f vs (beta_w/sigma)^2 %.9f" % (F0["dchi_slope"], (bw / sbw) ** 2))
check("K4c power identity", abs(W0["lam"] - W0["bt"] ** 2 / sbw ** 2) < 1e-9, "lambda %.9f vs beta_true^2/sigma^2 %.9f" % (W0["lam"], W0["bt"] ** 2 / sbw ** 2))
Fj = DEF["jkref"]["F"]; Ff = DEF["fixref"]["F"]
dd = max(abs(Fj[m]["chi2"] - Ff[m]["chi2"]) for m in ("M0off", "step", "grad", "stepslope"))
check("K4d free-offset chi2 identical, jk ref vs fixed ref", dd < 1e-9, "max |delta chi2| %.2e over M0off, step, grad, step+slope" % dd)
# exact pure step / pure gradient
Ast = np.where(B6["cls"] == 0, -0.15, 0.05).astype(float); Agr = 0.1 + 0.3 * (B6["u"] - 2.0)
e1 = fit_all(Ast, C0, B6["cls"], B6["u"], B6["uclass"])[0]; e2 = fit_all(Agr, C0, B6["cls"], B6["u"], B6["uclass"])[0]
check("K4e exact step / gradient", e1["step"]["chi2"] < 1e-18 + 1e-9 and abs(e1["dchi_slope"]) < 1e-9 and e2["grad"]["chi2"] < 1e-9,
      "pure step: step chi2 %.1e dchi2 %.1e; pure gradient: grad chi2 %.1e" % (e1["step"]["chi2"], e1["dchi_slope"], e2["grad"]["chi2"]))
# K5 swap
perm = [2, 1, 0, 5, 4, 3]
As = A0[perm]; Cs = C0[np.ix_(perm, perm)]
Fs = fit_all(As, Cs, B6["cls"], B6["u"], B6["uclass"])[0]
check("K5 swap control", abs(Fs["step"]["chi2"] - F0["step"]["chi2"]) < 1e-9 and Fs["stepslope"]["beta"][2] * bw < 0 and Fs["grad"]["chi2"] - F0["grad"]["chi2"] > 10,
      "step chi2 %.6f -> %.6f; beta_w %.3f -> %.3f; gradient chi2 %.2f -> %.2f" % (F0["step"]["chi2"], Fs["step"]["chi2"], bw, Fs["stepslope"]["beta"][2], F0["grad"]["chi2"], Fs["grad"]["chi2"]))

# ---- K6 null
log("== K6 calibration null: 200 random equal-count thirds per class")
rng = np.random.default_rng(107)
wk_full = psum(allm, WW, K1).sum(0)
wall = psum(allm, WG0, K1); wallw = psum(allm, WW, K1)
tg, tw = wall.sum(0), wallw.sum(0); r_full = tg / tw; r_loo = (tg[None] - wall) / (tw[None] - wallw)
den_loo = (r_loo * wk_full[None]).sum(1)
cl = (u > 2.0).astype(int)
idx_cl = [np.flatnonzero(cl == c) for c in (0, 1)]
chis = []
for rep in range(200):
    lab = np.zeros(nL, int)
    for c in (0, 1):
        pi = rng.permutation(idx_cl[c]); n = len(pi)
        for j in range(3): lab[pi[(j * n) // 3:((j + 1) * n) // 3]] = 3 * c + j
    Al = np.zeros((NP, 6)); Af = np.zeros(6)
    for b in range(6):
        ii = np.flatnonzero(lab == b)
        wg = np.zeros((NP, len(K1))); w = np.zeros((NP, len(K1)))
        for j, k in enumerate(K1):
            wg[:, j] = np.bincount(patch[ii], weights=WG0[ii, k], minlength=NP); w[:, j] = np.bincount(patch[ii], weights=WW[ii, k], minlength=NP)
        t1, t2 = wg.sum(0), w.sum(0)
        Af[b] = math.log10(((t1 / t2) * wk_full).sum() / (r_full * wk_full).sum())
        Al[:, b] = np.log10((((t1[None] - wg) / (t2[None] - w)) * wk_full[None]).sum(1) / den_loo)
    Cn = jkcov(Al)
    chis.append(fit_all(Af, Cn, B6["cls"], B6["u"], B6["uclass"])[0]["step"]["chi2"])
chis = np.array(chis)
check("K6 null calibration", 2.5 <= chis.mean() <= 5.5, "mean step chi2 %.3f (4 dof; expected 4, CFG115 3.76), fraction p<0.05: %.3f, sd %.2f" % (chis.mean(), (stats.chi2.sf(chis, 4) < 0.05).mean(), chis.std()))
R["null"] = dict(mean=float(chis.mean()), frac=float((stats.chi2.sf(chis, 4) < 0.05).mean()))

# ---- R3 outer contrasts
log("== R3 outer-tertile contrasts")
T = np.zeros((2, 6)); T[0, 0], T[0, 1] = 1, -1; T[1, 5], T[1, 4] = 1, -1
cv = T @ A0; Cc = T @ C0 @ T.T
chi3 = hart(2) * cv @ np.linalg.solve(Cc, cv); chi3b = h6 * cv @ np.linalg.solve(Cc, cv)
log("  A(L1)-A(L2) = %+.4f +- %.4f ; A(E3)-A(E2) = %+.4f +- %.4f ; chi2(2 dof) = %.3f p %.3f (h p'=2) ; %.3f p %.3f (h p=6)" %
    (cv[0], math.sqrt(Cc[0, 0]), cv[1], math.sqrt(Cc[1, 1]), chi3, pv(chi3, 2), chi3b, pv(chi3b, 2)))
cmp("P7 A(L1)-A(L2)", cv[0], 0.10, 0.006); cmp("P7 err", math.sqrt(Cc[0, 0]), 0.10, 0.01)
cmp("P7 A(E3)-A(E2)", cv[1], 0.07, 0.006); cmp("P7 err", math.sqrt(Cc[1, 1]), 0.05, 0.006); cmp("P7 chi2 outer", chi3, 3.25, 0.06)
R["R3"] = dict(contrast=cv.tolist(), chi2=chi3, chi2_h6=chi3b)

# ---- R4 per-bin table
log("== R4 per-bin table")
esdK = []
for j, m in enumerate(B6["masks"]):
    s = psum(m, WG0, K1).sum(0) / psum(m, WW, K1).sum(0) / KG
    esdK.append(s)
    log("  %s N %6d  med u-r %.3f  med log10 Mgal %.3f  med z %.3f  ESD_K1 %s" % (names6[j], m.sum(), B6["u"][j], np.median(lmg[m]), np.median(z[m]), np.round(s, 2)))
esd_allK = psum(allm, WG0, K1).sum(0) / psum(allm, WW, K1).sum(0) / KG
log("  all    ESD_K1 %s" % np.round(esd_allK, 2))

# ---- R0 power variants (A5)
log("== A5 power variants (which alternative gives 4.8)")
uc_med = B6["uclass"]; uc_mean = np.array([u[cl == 0].mean(), u[cl == 1].mean()])
Fp, Pp, Dp = fit_all(A0, C0, B6["cls"], B6["u"], B6["uclass"])
Fn, Pn, _ = fit_all(A0, C0, B6["cls"], B6["u"], B6["uclass"], use_h=False)
sL, sE = Fp["step"]["beta"]
variants = {}
def lam_of(bt, P): return gls(Dp["step"], bt * B6["u"], P)[2]
Pnoh = np.linalg.inv(C0)
variants["V1 primary (step-fit s, class median colour, Hartlap)"] = lam_of((sE - sL) / (uc_med[1] - uc_med[0]), Pp)
variants["V2 no Hartlap h"] = lam_of((sE - sL) / (uc_med[1] - uc_med[0]), Pnoh)
# class-level amplitudes from the two-class ESDs (own class amplitude, relative to full sample)
Acl = []
for c in (0, 1):
    m = typ == c
    e = psum(m, WG0, K1).sum(0) / psum(m, WW, K1).sum(0); r = psum(allm, WG0, K1).sum(0) / psum(allm, WW, K1).sum(0)
    Acl.append(math.log10((wk_full * e).sum() / (wk_full * r).sum()))
variants["V3 s from class-level amplitudes (%.3f, %.3f)" % tuple(Acl)] = lam_of((Acl[1] - Acl[0]) / (uc_med[1] - uc_med[0]), Pp)
variants["V4 class MEAN colour"] = lam_of((sE - sL) / (uc_mean[1] - uc_mean[0]), Pp)
uE = B6["u"][3:].mean(); uL = B6["u"][:3].mean()
variants["V5 mean of bin-median colours"] = lam_of((sE - sL) / (uE - uL), Pp)
variants["V6 truth = gradient-fit slope %.3f" % Fp["grad"]["beta"][1]] = lam_of(Fp["grad"]["beta"][1], Pp)
variants["V7 truth = observed within-class slope %.3f (=> observed dchi2)" % Fp["stepslope"]["beta"][2]] = lam_of(Fp["stepslope"]["beta"][2], Pp)
variants["V8 primary at half class difference"] = lam_of(0.5 * (sE - sL) / (uc_med[1] - uc_med[0]), Pp)
for k, v in variants.items(): log("  %-72s lambda = %.3f" % (k, v))
bt = W0["bt"]
crit1 = stats.chi2.ppf(0.95, 1)
log("  power of the 1-dof slope test at alpha 0.05 for lambda %.2f: %.3f ; sigma_beta_w %.4f => detectable slope at 80%% power %.3f dex/mag = %.2f x beta_true; at 50%% %.3f" %
    (W0["lam"], stats.ncx2.sf(crit1, 1, W0["lam"]), sbw, 2.8016 * sbw, 2.8016 * sbw / bt, 1.96 * sbw))
cmp("P3 lambda (POST HOC reading V3: s from class-level amplitudes)", [v for k, v in variants.items() if k.startswith("V3")][0], 4.8, 0.05)
cmp("P3 beta_true (POST HOC reading V3)", (Acl[1] - Acl[0]) / (uc_med[1] - uc_med[0]), 0.270, 0.002)
R["power_variants"] = {k: float(v) for k, v in variants.items()}

# ---- A2 error inflation
log("== A2 error inflation")
for f in (1.0, 1.2, 1.5, 2.0):
    Ff, _, _ = fit_all(A0, C0, B6["cls"], B6["u"], B6["uclass"], f=f)
    log("  x%.1f: step %.2f/4 (p %.3g)  grad %.2f/4 (p %.3g)  stepslope %.2f  dchi2 %.2f (p %.3g)  M0off %.2f/5  | beta_grad %.3f+-%.3f  beta_w %.3f+-%.3f" %
        (f, Ff["step"]["chi2"], pv(Ff["step"]["chi2"], 4), Ff["grad"]["chi2"], pv(Ff["grad"]["chi2"], 4), Ff["stepslope"]["chi2"], Ff["dchi_slope"], pv(Ff["dchi_slope"], 1),
         Ff["M0off"]["chi2"], Ff["grad"]["beta"][1], Ff["grad"]["err"][1], Ff["stepslope"]["beta"][2], Ff["stepslope"]["err"][2]))
fneed1 = math.sqrt(F0["step"]["chi2"] / stats.chi2.isf(0.05, 4)); fneed2 = math.sqrt(F0["dchi_slope"] / 3.84)
log("  inflation for step p=0.05: x%.2f; for dchi2(slope)=3.84: x%.2f; for M0off p=0.05: x%.2f" % (fneed1, fneed2, math.sqrt(F0["M0off"]["chi2"] / stats.chi2.isf(0.05, 5))))

# ---- A3 tertile edges
log("== A3 tertile-edge / class-split sensitivity (jackknifed-reference definition)")
wk1 = psum(allm, WW, K1).sum(0)
def bins_report(Bx, label, WGa=WG0, ks=K1, wkk=None, lin=False):
    try:
        Af, Al = amps(Bx["masks"], [allm] * Bx["nb"], WGa, WW, ks, "jkref", wk=wkk, lin=lin)
    except ValueError:
        log("  %-30s log amplitude UNDEFINED (a weighted bin numerator or jackknife-sample ratio is <= 0)" % label)
        if not lin:
            log("      POST HOC linear-ratio amplitude (A = ratio - 1, same covariance recipe) for the same set:")
            return bins_report(Bx, label + " [lin]", WGa, ks, wkk, lin=True)
        return None
    if not np.all(np.isfinite(Al)):
        log("  %-30s a jackknife-sample ratio <= 0: log amplitude undefined" % label)
        return bins_report(Bx, label + " [lin]", WGa, ks, wkk, lin=True) if not lin else None
    Cx = jkcov(Al)
    Fx, Px, Dx = fit_all(Af, Cx, Bx["cls"], Bx["u"], Bx["uclass"])
    log("  %-30s nb %d step %.2f/%d (p %.3g)  dchi2 %.2f  beta_w %.3f+-%.3f  grad %.2f/%d beta_g %.3f+-%.3f  M0off %.1f" %
        (label, Bx["nb"], Fx["step"]["chi2"], Fx["step"]["dof"], pv(Fx["step"]["chi2"], Fx["step"]["dof"]), Fx["dchi_slope"], Fx["stepslope"]["beta"][-1], Fx["stepslope"]["err"][-1],
         Fx["grad"]["chi2"], Fx["grad"]["dof"], Fx["grad"]["beta"][1], Fx["grad"]["err"][1], Fx["M0off"]["chi2"]))
    return dict(step=Fx["step"]["chi2"], dstep=Fx["step"]["dof"], dchi=Fx["dchi_slope"], bw=Fx["stepslope"]["beta"][-1], sbw=Fx["stepslope"]["err"][-1], grad=Fx["grad"]["chi2"], bg=Fx["grad"]["beta"][1], A=Af.tolist())
R["edges"] = {}
for nm, cuts in (("1/3,2/3 (main)", [1 / 3, 2 / 3]), ("0.30,0.70", [0.30, 0.70]), ("0.25,0.75", [0.25, 0.75]), ("0.40,0.60", [0.40, 0.60]), ("0.35,0.65", [0.35, 0.65]),
                 ("halves (2 per class)", [0.5]), ("quartiles (4 per class)", [0.25, 0.5, 0.75]), ("quintiles (5 per class)", [0.2, 0.4, 0.6, 0.8])):
    R["edges"][nm] = bins_report(binning(cuts), nm)
for sp in (1.9, 2.1):
    R["edges"]["split %.1f" % sp] = bins_report(binning([1 / 3, 2 / 3], split=sp), "class split at u-r=%.1f" % sp)

# ---- A4
log("== A4 colour-dependent systematic vs lensing signal")
# (a) mass/z matching
log("  (a) mass/z matching within class (cells 0.2 dex log10 Mgal x 0.1 in z; bin cells with < 20 lenses dropped)")
zi = np.floor(z / 0.1).astype(int); mi = np.floor(lmg / 0.2).astype(int)
cell = mi * 1000 + zi
om = np.zeros(nL); keep_frac = []
for j, m in enumerate(B6["masks"]):
    c = B6["cls"][j]; mc = cl == c
    uc_cells, inv_c, cnt_c = np.unique(cell[mc], return_inverse=True, return_counts=True)
    pc = dict(zip(uc_cells, cnt_c / mc.sum()))
    ub_cells, inv_b, cnt_b = np.unique(cell[m], return_inverse=True, return_counts=True)
    pb = cnt_b / m.sum()
    tgt = np.array([pc[c_] for c_ in ub_cells])
    wcell = np.where(cnt_b >= 20, tgt / pb, 0.0)
    idx = np.flatnonzero(m)
    om[idx] = wcell[inv_b]
    keep_frac.append(float((cnt_b[cnt_b >= 20]).sum() / m.sum()))
log("      fraction of lenses kept per bin: %s" % np.round(keep_frac, 3))
def matched_run(omega, label):
    WGr = WG0 * omega[:, None]; WWr = WW * omega[:, None]
    neff = [float(omega[m].sum() ** 2 / (omega[m] ** 2).sum()) for m in B6["masks"]]
    log("      %s: max omega per bin %s ; Kish effective N per bin %s (raw %s)" % (label, np.round([omega[m].max() for m in B6["masks"]], 1), np.round(neff, 0), Nbin))
    try:
        Af, Al = amps_w(WGr, WWr, B6["masks"], K1, wk1)
    except ValueError:
        log("      %s: a weighted bin numerator sum_k w_k ESD_ck is <= 0 => the amplitude (a log) is UNDEFINED; row not computable as specified" % label)
        return None
    Cm = jkcov(Al); Fm, _, _ = fit_all(Af, Cm, B6["cls"], B6["u"], B6["uclass"])
    log("      matched amplitudes %s" % np.round(Af, 3))
    log("      step %.2f/4 (p %.3g)  grad %.2f/4  stepslope %.2f  dchi2 %.2f  beta_w %.3f+-%.3f  beta_grad %.3f+-%.3f  M0off %.1f" %
        (Fm["step"]["chi2"], pv(Fm["step"]["chi2"], 4), Fm["grad"]["chi2"], Fm["stepslope"]["chi2"], Fm["dchi_slope"], Fm["stepslope"]["beta"][2], Fm["stepslope"]["err"][2], Fm["grad"]["beta"][1], Fm["grad"]["err"][1], Fm["M0off"]["chi2"]))
    return dict(A=Af.tolist(), step=Fm["step"]["chi2"], dchi=Fm["dchi_slope"], bw=Fm["stepslope"]["beta"][2], sbw=Fm["stepslope"]["err"][2], bg=Fm["grad"]["beta"][1])
def amps_w(WGa, WWa, masks, ks, wk):
    return amps(masks, [allm] * len(masks), WGa, WWa, ks, "jkref", wk=wk, refWG=WG0, refWW=WW)
R["A4a"] = matched_run(om, "as frozen (cells with <20 lenses dropped)")
# POST HOC (disclosed): the frozen matching gives weights up to 35-64 and L1's weighted numerator goes negative -> use the common support
# (cells with >= 200 lenses in every bin of the class), target = the mean of the three bins' cell distributions on that support
om2 = np.zeros(nL); 
for c in (0, 1):
    js = [j for j in range(6) if B6["cls"][j] == c]
    cells_all = np.unique(cell[cl == c])
    cnts = np.array([[np.sum(cell[B6["masks"][j]] == cc) for cc in cells_all] for j in js])
    sup = (cnts >= 200).all(0)
    pbs = cnts / cnts.sum(1, keepdims=True)
    tgt = np.where(sup, pbs.mean(0), 0.0); tgt = tgt / tgt.sum()
    lut = {cc: i for i, cc in enumerate(cells_all)}
    for jj, j in enumerate(js):
        idx = np.flatnonzero(B6["masks"][j]); ci = np.array([lut[x] for x in cell[idx]])
        om2[idx] = np.where(sup[ci], tgt[ci] / pbs[jj, ci], 0.0)
R["A4a_posthoc"] = matched_run(om2, "POST HOC common-support matching (>=200 lenses per bin per cell)")
# (b) radial
log("  (b) radial sets")
R["A4b"] = {}
for nm, ks in (("inner 12-14", [12, 13, 14]), ("outer 8-11", [8, 9, 10, 11]), ("2-halo 0-7", list(range(8))), ("all 0-14", list(range(15))), ("K1 8-14", list(range(8, 15)))):
    wkk = psum(allm, WW, ks).sum(0)
    R["A4b"][nm] = bins_report(B6, nm, ks=ks, wkk=wkk)
# (c) redshift split
log("  (c) redshift split (joint 12-vector jackknife)")
zmed = float(np.median(z)); zl = z < zmed
masks12 = [m & zl for m in B6["masks"]] + [m & ~zl for m in B6["masks"]]
refs12 = [zl] * 6 + [~zl] * 6
Af12, Al12 = amps(masks12, refs12, WG0, WW, K1, "jkref")
C12 = jkcov(Al12)
cls12 = np.r_[B6["cls"], B6["cls"]]
Flo, _, _ = fit_all(Af12[:6], C12[:6, :6], B6["cls"], B6["u"], B6["uclass"]); Fhi, _, _ = fit_all(Af12[6:], C12[6:, 6:], B6["cls"], B6["u"], B6["uclass"])
# slope difference via joint model: 12-vector, step per (z half, class) + common within-class slopes (2 slopes)
X12 = np.zeros((12, 6))
for j in range(12):
    hh = j // 6; c = B6["cls"][j % 6]
    X12[j, hh * 2 + c] = 1
    X12[j, 4 + hh] = B6["u"][j % 6] - B6["uclass"][c]
P12 = hart(12) * np.linalg.inv(C12)
b12, Fi12, chi12, _ = gls(X12, Af12, P12)
dsl = b12[4] - b12[5]; sdsl = math.sqrt(Fi12[4, 4] + Fi12[5, 5] - 2 * Fi12[4, 5])
log("      z median %.3f. low-z: beta_w %.3f+-%.3f, grad %.3f+-%.3f, dchi2 %.2f ; high-z: beta_w %.3f+-%.3f, grad %.3f+-%.3f, dchi2 %.2f" %
    (zmed, Flo["stepslope"]["beta"][2], Flo["stepslope"]["err"][2], Flo["grad"]["beta"][1], Flo["grad"]["err"][1], Flo["dchi_slope"],
     Fhi["stepslope"]["beta"][2], Fhi["stepslope"]["err"][2], Fhi["grad"]["beta"][1], Fhi["grad"]["err"][1], Fhi["dchi_slope"]))
log("      12-vector joint fit (h p=12): beta_w(low) - beta_w(high) = %+.3f +- %.3f (%.2f sigma)   [amps low %s | high %s]" % (dsl, sdsl, dsl / sdsl, np.round(Af12[:6], 3), np.round(Af12[6:], 3)))
R["A4c"] = dict(dsl=dsl, sdsl=sdsl, low=Flo["stepslope"]["beta"][2], high=Fhi["stepslope"]["beta"][2])
# (d) leave-one-K1-bin-out
log("  (d) K1 subsets")
R["A4d"] = {}
for drop in list(K1) + [None]:
    ks = [k for k in K1 if k != drop]
    if drop is None: ks = list(K1[:3])
    wkk = psum(allm, WW, ks).sum(0)
    R["A4d"]["drop %s" % drop if drop is not None else "lowest-3 K1 (8-10)"] = bins_report(B6, "drop bin %s" % drop if drop is not None else "lowest-3 K1 bins (8-10)", ks=ks, wkk=wkk)
# (e) M/L-equivalent
log("  (e) M/L-equivalent: local ESD slope in K1 and the stellar-mass bias that would mimic the gradient")
slopes = {}
gl = np.log10(gcen[K1])
for c, nm in ((0, "late"), (1, "early"), (None, "all")):
    m = allm if c is None else typ == c
    e = psum(m, WG0, K1).sum(0) / psum(m, WW, K1).sum(0) / KG
    pos = e > 0
    sl = np.polyfit(gl[pos], np.log10(e[pos]), 1)[0]
    slopes[nm] = sl
    log("      %s: d log ESD / d log g_bar over K1 = %+.3f  (ESD %s)" % (nm, sl, np.round(e, 2)))
span = B6["u"][5] - B6["u"][0]
grad_amp = F0["grad"]["beta"][1] * span
sl = abs(slopes["all"])
log("      gradient amplitude across E3-L1 (%.3f mag) = %.3f dex => a colour-dependent bias in log g_bar (equivalently log Mgal) of %.2f dex across the span would mimic it (%.3f dex/mag);"
    " the class step (s_E - s_L = %.3f) needs %.2f dex" % (span, grad_amp, grad_amp / sl, grad_amp / sl / span, sE - sL, (sE - sL) / sl))
R["A4e"] = dict(slopes=slopes, span=span, grad_amp=grad_amp, delta_dex=grad_amp / sl)
# (f) blurred step
log("  (f) smooth-transition (blurred step) model a_L + Delta <Phi((u-2)/sigma)>, weights sum_K1 WW per lens")
wl = WW[:, K1].sum(1)
Pf = h6 * np.linalg.inv(C0); R["A4f"] = {}
for sg in (0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5):
    mc = np.array([(wl[m] * stats.norm.cdf((u[m] - 2.0) / sg)).sum() / wl[m].sum() for m in B6["masks"]])
    Xb = np.c_[np.ones(6), mc]
    b, Fi, chi, _ = gls(Xb, A0, Pf)
    R["A4f"][sg] = dict(chi2=chi, aL=float(b[0]), Delta=float(b[1]))
    log("      sigma %.2f: chi2 %.2f /4 (p %.3g)  a_L %+.3f  Delta %+.3f +- %.3f   bin fractions %s" % (sg, chi, pv(chi, 4), b[0], b[1], math.sqrt(Fi[1, 1]), np.round(mc, 2)))

# ---- R5 model stacks
log("== R5 model amplitudes (model stacks through grouped cells; building tables ...)")
key = typ.astype(np.int64) * 10 ** 9 + np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
uk, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
NG = len(cnt)
mean_ = lambda x: np.bincount(gi, weights=x) / cnt
GR = dict(Mgal=10 ** mean_(lmg), logM=mean_(logMs), z=mean_(z), typ=np.bincount(gi, weights=typ) / cnt)
log("  groups %d" % NG)
tabs = {}
for kind in ("B_canonical", "L", "Mo"):
    t = time.time(); tab = np.zeros((NG, 15))
    for g in range(NG): tab[g] = L.v_one(kind, GR["Mgal"][g], GR["logM"][g], GR["z"][g], int(round(GR["typ"][g])))
    tabs[kind] = tab; log("  table %-12s %.0fs" % (kind, time.time() - t))
def stack_m(tab, mask):
    w = np.bincount(gi[mask], weights=Mgal[mask], minlength=NG); return (w @ tab) / w.sum()
def stack_pw(tab, mask):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG); out[k] = (w @ tab[:, k]) / w.sum()
    return out
def model_amp(tab, stackf):
    e_all = stackf(tab, allm)
    return np.array([math.log10((wk1 * stackf(tab, m)[K1]).sum() / (wk1 * e_all[K1]).sum()) for m in B6["masks"]])
Cj = W0["Cs"]["jkref"]; Cf = W0["Cs"]["fixref"]
R["R5"] = {}
tgtR5 = {"B_canonical": (304, 36.2), "L": (77.6, 21.1), "Mo": (29.2, 12.2)}
for kind in ("B_canonical", "L", "Mo"):
    for sname, sf in (("Mgal-weighted", stack_m), ("pair-weighted", stack_pw)):
        Am = model_amp(tabs[kind], sf); r = A0 - Am
        Pj = h6 * np.linalg.inv(Cj); Pf_ = h6 * np.linalg.inv(Cf)
        ca = r @ Pj @ r; cb = r @ Pf_ @ r
        one = np.ones(6); cc = r @ Pj @ r - (one @ Pj @ r) ** 2 / (one @ Pj @ one)
        R["R5"][kind + "|" + sname] = dict(A=Am.tolist(), a=ca, b=cb, c=cc)
        log("  %-12s %-13s model A %s  chi2 (a) jk-ref zero-offset %.1f | (b) fixed-ref zero-offset %.1f | (c) free offset %.1f /5" % (kind, sname, np.round(Am, 3), ca, cb, cc))
    d = R["R5"][kind + "|Mgal-weighted"]
    tol_a = 1.0 if kind != "Mo" else 0.05 * tgtR5[kind][0]; tol_c = 0.1 if kind != "Mo" else 0.05 * tgtR5[kind][1]
    cmp("P6 R5(a) %s (Mgal-wtd)" % kind, d["a"], tgtR5[kind][0], tol_a); cmp("P6 R5(c) %s free offset" % kind, d["c"], tgtR5[kind][1], tol_c)

# ==================================================================================================================================
log("== summary of reproduction lines")
cnts = {}
for r in repro: cnts[r[4]] = cnts.get(r[4], 0) + 1
log("  %s" % cnts)
for r in repro:
    if r[4] != "REPRODUCED": log("    %-46s mine %.5g CFG115 %.5g tol %.3g  %s" % (r[0], r[1], r[2], r[3], r[4]))
R["repro"] = repro
nfail = sum(not v for v in checks.values())
log("controls: %d/%d pass" % (len(checks) - nfail, len(checks)))
for k, v in checks.items(): log("   %s %s" % ("PASS" if v else "FAIL", k))
json.dump(R, open(OUTJSON, "w"), indent=1, default=float)
log("elapsed %.0fs" % (time.time() - T0))
rc = 1 if ((not H1) or nfail) else 0
log("H1 %s ; RC %d" % ("PASS" if H1 else "FAIL", rc))
sys.exit(rc)
