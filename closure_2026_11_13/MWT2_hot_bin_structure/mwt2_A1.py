#!/usr/bin/env python3
"""
MWT2 (AMENDMENT A1 reading; a copy of mwt2.py changed only as AMENDMENT_A1.md says) -- is RAW1's hot 30-40 kpc bin a structure? One- vs two-Gaussian per bin, identity tests, consequence.
Criteria: FROZEN_CRITERIA.md (committed alone before this script).
Usage: python3 -I -B mwt2.py <path to MWS_BHB.fits>      (the path is never printed)
Writes mwt2_A1.out, mwt2_A1_results.json, and the mutations to mwt2_A1_MUTATE.out.
RAW1's estimators are reused unchanged by MWT1's method (copied from closure_2026_11_13/MWT1_hot_bin_assumptions/
mwt1.py, lines 41-50 and 107-126): raw1.py is parsed and only its import, constant and function definitions are
executed; RAW1's files are read-only. Paths are relative to this script.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[k] = "1"
import ast, json, math, hashlib, warnings, time
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import minimize_scalar
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
RAW1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_12", "RAW1_halo_stars_direct"))
FITS = sys.argv[1]
SHA_DATA = "5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246"
B_REAL = int(os.environ.get("MWT2_B", "1000")); B_MUT = 500; B_PARERR = 200; NPERM = 2000; NSHUF = 20

OUT = open(os.path.join(HERE, "mwt2_A1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say(""); say("=" * 110); say(t); say("=" * 110)
FAILED = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAILED.append(name)
def stop_if_failed():
    if FAILED:
        say("KNOWN-ANSWER CHECK FAILED: " + ", ".join(FAILED) + ". Stopping before any label."); OUT.close(); sys.exit(2)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
T0 = time.time()

# ------------------------------------------------------------------ RAW1's functions, unchanged (MWT1's method)
sys.path.insert(0, RAW1)
src = open(os.path.join(RAW1, "raw1.py")).read()
tree = ast.parse(src)
KEEP_ASSIGN = ("K474", "BINS", "NOMINAL", "FOOT", "SG", "NGRID", "_GCACHE")
body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in KEEP_ASSIGN)]
R1 = {"FITS": FITS, "HERE": RAW1, "__name__": "raw1_functions"}
exec(compile(ast.Module(body=body, type_ignores=[]), "raw1.py", "exec"), R1)
MOD = R1["MOD"]; BINS = R1["BINS"]; NOMINAL = R1["NOMINAL"]; K474 = R1["K474"]
CASES = [("FW_census", "canonical"), ("FW_census", "alt"), ("FW_rc", "canonical"), ("FW_rc", "alt"), ("H", None), ("N", None)]
GRADED = CASES[:4]
CKEY = lambda m, f: f"{m}/{f}" if f else m
BN = ["20-30", "30-40", "40-55", "55-80"]

# ------------------------------------------------------------------ data
assert sha(FITS) == SHA_DATA, "data file hash mismatch"
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
D = R1["load"]()
_h = fits.open(FITS, memmap=False); _rv = _h["RVTAB"].data
D["feh"] = np.asarray(_rv["FEH"], float); D["feh_err"] = np.asarray(_rv["FEH_ERR"], float)
_c = SkyCoord(ra=D["ra"] * u.deg, dec=D["dec"] * u.deg, frame="icrs").galactic
D["l"], D["b"] = _c.l.deg, _c.b.deg
D["lsgr"], D["bsgr"] = R1["sgr_lat_lon"](D["l"], D["b"])
cfg = dict(NOMINAL)
S = R1["build"](D, cfg)
for k in ("l", "b", "bsgr", "lsgr", "feh", "feh_err"): S[k] = D[k][S["i"]]
S["bin"] = np.array([next((j for j, (a, b) in enumerate(BINS) if a <= x < b), -1) for x in S["r"]])
# 3D Galactocentric velocity (v_gsr along n, PMs at the catalogue distance plus the solar motion)
vea = K474 * S["d"] * S["pmra"] + S["ea"] @ S["vs"]; vno = K474 * S["d"] * S["pmdec"] + S["no"] @ S["vs"]
S["V"] = S["vgsr"][:, None] * S["n"] + vea[:, None] * S["ea"] + vno[:, None] * S["no"]
def vphi_vt(V, pos, rh):
    Rc = np.hypot(pos[:, 0], pos[:, 1]); ph = np.vstack([-pos[:, 1] / Rc, pos[:, 0] / Rc, np.zeros(len(Rc))]).T
    vr = np.sum(V * rh, axis=1); return np.sum(V * ph, axis=1), np.linalg.norm(V - vr[:, None] * rh, axis=1)

# ================================================================== K2 SI, then K0 RAW1 reproduced
sec("Known answers K0 (RAW1 reproduced, nothing removed) and K2 (SI)")
say(f"  RAW1 files read-only: raw1.py sha256 {sha(os.path.join(RAW1, 'raw1.py'))[:16]}..., raw1_model.py {sha(os.path.join(RAW1, 'raw1_model.py'))[:16]}...; data sha256 {SHA_DATA[:16]}... (matches)")
say(f"  a0 as in raw1_model.py: canonical {MOD.A0['canonical']:.3e}, alt {MOD.A0['alt']:.3e} m/s^2; no external field (RAW1's reading)")
g30 = float(MOD.g_model(30.0, "FW_census", "canonical")); Msi = g30 * (30 * 3.0857e19) ** 2 / 6.674e-11 / 1.989e30
check("K2 SI: M = g r^2 / G at 30 kpc (FW census canonical)", abs(Msi / float(MOD.M_of_g(g30, 30.0)) - 1) < 1e-9,
      f"g = {g30:.4e} m/s^2, M = {Msi:.4e} Msun, V = sqrt(g r) = {math.sqrt(g30 * 30 * 3.0857e19) / 1e3:.1f} km/s")
R = R1["measure"](S, cfg)
J = json.load(open(os.path.join(RAW1, "raw1_results.json")))["nominal"]
check("K0 counts", list(R["counts"]) == J["counts"] == [865, 264, 241, 125], f"{R['counts']}")
dd = max(abs(a["sigma"] - b["sigma"]) for a, b in zip(R["disp"], J["disp"]))
check("K0 sigma_los", dd < 5e-4, "  ".join(f"{x['sigma']:.3f}" for x in R["disp"]) + f" (max diff {dd:.1e})")
check("K0 alpha, beta", abs(R["alpha"]["alpha"] - J["alpha"]["alpha"]) < 5e-4 and abs(R["beta"] - J["beta"]) < 5e-4,
      f"alpha {R['alpha']['alpha']:.4f} +/- {R['alpha']['sig']:.4f}; beta {R['beta']:.4f} +/- {R['sbeta']:.4f}")
BASE = {}
for m, ft in CASES:
    k = CKEY(m, ft); BASE[k] = R1["f_full"](S, R, m, ft)
    dmax = max(max(abs(a["f"] - b["f"]), abs(a["s"] - b["s"])) for a, b in zip(BASE[k], J["f"][k]))
    check(f"K0 f {k}", dmax < 5e-4, "  ".join(f"{x['f']:.3f}+/-{x['s']:.3f}" for x in BASE[k]) + f" (max diff {dmax:.1e})")
stop_if_failed()
ALPHA, SALPHA, BETA = R["alpha"]["alpha"], R["alpha"]["sig"], R["beta"]

# ------------------------------------------------------------------ (a) mixture machinery
def starts_for(v):
    mu, s = float(np.mean(v)), float(np.std(v)); q = np.percentile(v, [5, 20, 35, 50, 65, 80, 95])
    med = float(np.median(v)); lo, hi = v[v < med], v[v >= med]
    st = [(0.5, float(np.mean(lo)), float(np.std(lo)) ** 2, float(np.mean(hi)), float(np.std(hi)) ** 2)]
    st += [(0.15, float(x), 15.0 ** 2, mu, s * s) for x in q]
    st += [(0.5, mu - 0.7 * s, (0.7 * s) ** 2, mu + 0.7 * s, (0.7 * s) ** 2), (0.3, mu, (0.5 * s) ** 2, mu, s * s)]
    return np.array(st)   # columns: w1, mu1, s1^2, mu2, s2^2

def xd2(v, e2, floor=5.0, maxit=600, tol=1e-7, st=None):
    """two-component extreme deconvolution, all starts at once; returns best (lnL, w1, mu1, s1, mu2, s2, q1)."""
    st = starts_for(v) if st is None else st
    K = st.shape[0]; f2 = floor * floor
    w = st[:, 0:1].copy(); m1 = st[:, 1:2].copy(); a1 = np.maximum(st[:, 2:3], f2); m2 = st[:, 3:4].copy(); a2 = np.maximum(st[:, 4:5], f2)
    vv = v[None, :]; ee = e2[None, :]; llold = np.full(K, -np.inf); active = np.ones(K, bool)
    for it in range(maxit):
        V1 = a1 + ee; V2 = a2 + ee
        l1 = np.log(np.clip(w, 1e-300, None)) - 0.5 * np.log(2 * np.pi * V1) - 0.5 * (vv - m1) ** 2 / V1
        l2 = np.log(np.clip(1 - w, 1e-300, None)) - 0.5 * np.log(2 * np.pi * V2) - 0.5 * (vv - m2) ** 2 / V2
        L = np.logaddexp(l1, l2); ll = L.sum(axis=1)
        q1 = np.exp(l1 - L); q2 = 1 - q1
        b1 = m1 + a1 / V1 * (vv - m1); B1 = a1 - a1 * a1 / V1
        b2 = m2 + a2 / V2 * (vv - m2); B2 = a2 - a2 * a2 / V2
        n1 = q1.sum(axis=1, keepdims=True); n2 = q2.sum(axis=1, keepdims=True)
        n1s = np.maximum(n1, 1e-9); n2s = np.maximum(n2, 1e-9)
        w = n1 / v.size
        m1 = (q1 * b1).sum(axis=1, keepdims=True) / n1s; m2 = (q2 * b2).sum(axis=1, keepdims=True) / n2s
        a1 = np.maximum((q1 * ((b1 - m1) ** 2 + B1)).sum(axis=1, keepdims=True) / n1s, f2)
        a2 = np.maximum((q2 * ((b2 - m2) ** 2 + B2)).sum(axis=1, keepdims=True) / n2s, f2)
        if np.all(np.abs(ll - llold) < tol): break
        llold = ll
    # final likelihood at the final parameters
    V1 = a1 + ee; V2 = a2 + ee
    l1 = np.log(np.clip(w, 1e-300, None)) - 0.5 * np.log(2 * np.pi * V1) - 0.5 * (vv - m1) ** 2 / V1
    l2 = np.log(np.clip(1 - w, 1e-300, None)) - 0.5 * np.log(2 * np.pi * V2) - 0.5 * (vv - m2) ** 2 / V2
    L = np.logaddexp(l1, l2); ll = L.sum(axis=1); kb = int(np.nanargmax(ll))
    return dict(lnL=float(ll[kb]), w1=float(w[kb, 0]), mu1=float(m1[kb, 0]), s1=float(math.sqrt(a1[kb, 0])), mu2=float(m2[kb, 0]),
                s2=float(math.sqrt(a2[kb, 0])), q1=np.exp(l1[kb] - L[kb]))

def fit1(v, e2, floor=5.0):
    def nll(s):
        var = s * s + e2; mu = np.sum(v / var) / np.sum(1 / var)
        return 0.5 * np.sum((v - mu) ** 2 / var + np.log(2 * np.pi * var))
    r = minimize_scalar(nll, bounds=(floor, 600.0), method="bounded", options=dict(xatol=1e-6))
    s = r.x; var = s * s + e2; mu = np.sum(v / var) / np.sum(1 / var)
    return dict(lnL=-float(r.fun), mu=float(mu), s=float(s))

def order(fit2, v):
    """candidate group = smaller dispersion; if the dispersions agree within 10 per cent, the lower weight."""
    c1 = dict(w=fit2["w1"], mu=fit2["mu1"], s=fit2["s1"], q=fit2["q1"]); c2 = dict(w=1 - fit2["w1"], mu=fit2["mu2"], s=fit2["s2"], q=1 - fit2["q1"])
    if abs(c1["s"] - c2["s"]) <= 0.10 * max(c1["s"], c2["s"]): g, h = (c1, c2) if c1["w"] <= c2["w"] else (c2, c1)
    else: g, h = (c1, c2) if c1["s"] < c2["s"] else (c2, c1)
    return g, h

def lr_of(v, e2, floor=5.0):
    f1 = fit1(v, e2, floor); f2 = xd2(v, e2, floor)
    return max(0.0, 2 * (f2["lnL"] - f1["lnL"])), f1, f2

def boot_null(v, e2, B, seed, floor=5.0):
    LR, f1, f2 = lr_of(v, e2, floor); rg = np.random.default_rng(seed); out = np.empty(B)
    sd = np.sqrt(f1["s"] ** 2 + e2)
    for b in range(B): out[b] = lr_of(f1["mu"] + rg.normal(0, 1, len(v)) * sd, e2, floor)[0]
    return LR, f1, f2, out

def mixture_summary(v, e2, LR, f2, null, wmin=0.10):
    p = float((1 + np.sum(null >= LR)) / (len(null) + 1))
    g, h = order(f2, v); wm = min(f2["w1"], 1 - f2["w1"])
    return dict(LR=LR, p=p, sone=fit1(v, e2)["s"], w_minor=wm, n_minor=wm * len(v), g=dict(w=g["w"], mu=g["mu"], s=g["s"]), h=dict(w=h["w"], mu=h["mu"], s=h["s"]), q_g=g["q"])
def two_comp(ms, pthr=0.01, wmin=0.10): return ms["p"] < pthr and ms["w_minor"] >= wmin and ms["n_minor"] >= 15

# ------------------------------------------------------------------ (b) identity
def ks_stat(a, b):
    a = np.sort(a); b = np.sort(b); x = np.concatenate([a, b])
    return float(np.max(np.abs(np.searchsorted(a, x, side="right") / len(a) - np.searchsorted(b, x, side="right") / len(b))))
def identity(B, qg, seed):
    """B: per-bin dict of arrays; qg responsibilities of the candidate group."""
    core_g, core_h = qg >= 0.8, qg <= 0.2
    split = "cores 0.8 / 0.2"
    if core_g.sum() < 15 or core_h.sum() < 15: core_g, core_h = qg > 0.5, qg <= 0.5; split = "split at 0.5"
    sel = core_g | core_h; lab = core_g[sel]; rg = np.random.default_rng(seed)
    def perm_p(stat_fn, ok=None):
        okk = np.ones(sel.sum(), bool) if ok is None else ok[sel]
        L = lab[okk]
        if L.sum() < 10 or (~L).sum() < 10: return float("nan"), int(L.sum()), int((~L).sum())
        obs = stat_fn(L, okk); cnt = 0
        for _ in range(NPERM):
            if stat_fn(rg.permutation(L), okk) >= obs - 1e-12: cnt += 1
        return float((1 + cnt) / (NPERM + 1)), int(L.sum()), int((~L).sum())
    n = B["n"][sel]; r = B["r"][sel]; bs = np.abs(B["bsgr"][sel]); fe = B["feh"][sel]; vp = B["vphi"][sel]; vt = B["vt"][sel]
    tests = {}
    tests["sky_meanvec"] = perm_p(lambda L, o: float(np.linalg.norm(n[o][L].mean(0) - n[o][~L].mean(0))))
    tests["sky_absBsgr"] = perm_p(lambda L, o: ks_stat(bs[o][L], bs[o][~L]))
    lsg = B["lsgr"][sel]
    def knn_stat(L, o):
        X = n[o][L]
        if len(X) < 6: return float("nan")
        c = np.clip(X @ X.T, -1, 1); np.fill_diagonal(c, -2.0)
        return -float(np.mean(np.arccos(np.sort(c, axis=1)[:, -5:])))   # larger = more clustered
    tests["sky_knn5"] = perm_p(knn_stat)
    tests["sky_lamSgr"] = perm_p(lambda L, o: ks_stat(lsg[o][L], lsg[o][~L]))
    tests["dist_r"] = perm_p(lambda L, o: ks_stat(r[o][L], r[o][~L]))
    okfe = np.zeros(len(qg), bool); okfe[:] = np.isfinite(B["feh"]) & np.isfinite(B["feh_err"]) & (B["feh_err"] < 0.5)
    tests["chem_feh"] = perm_p(lambda L, o: ks_stat(fe[o][L], fe[o][~L]), okfe)
    okpm = B["pmok"].copy()
    tests["tan_vphi"] = perm_p(lambda L, o: ks_stat(vp[o][L], vp[o][~L]), okpm)
    tests["tan_vt"] = perm_p(lambda L, o: ks_stat(vt[o][L], vt[o][~L]), okpm)
    fam = {"SKY": ["sky_meanvec", "sky_absBsgr", "sky_knn5", "sky_lamSgr"], "DISTANCE": ["dist_r"], "CHEMISTRY": ["chem_feh"], "TANGENTIAL": ["tan_vphi", "tan_vt"]}
    famp = {}
    for F, ts in fam.items():
        ps = [tests[t][0] for t in ts]
        famp[F] = float("nan") if any(not np.isfinite(x) for x in ps) else min(1.0, min(ps) * len(ps))
    extra = dict(n_core_g=int(core_g.sum()), n_core_h=int(core_h.sum()), split=split,
                 feh_med_g=float(np.nanmedian(B["feh"][core_g & okfe])) if (core_g & okfe).any() else float("nan"),
                 feh_med_h=float(np.nanmedian(B["feh"][core_h & okfe])) if (core_h & okfe).any() else float("nan"),
                 r_med_g=float(np.median(B["r"][core_g])) if core_g.any() else float("nan"), r_med_h=float(np.median(B["r"][core_h])) if core_h.any() else float("nan"),
                 absB_med_g=float(np.median(np.abs(B["bsgr"][core_g]))) if core_g.any() else float("nan"),
                 absB_med_h=float(np.median(np.abs(B["bsgr"][core_h]))) if core_h.any() else float("nan"),
                 vphi_med_g=float(np.nanmedian(B["vphi"][core_g & okpm])) if (core_g & okpm).any() else float("nan"),
                 vphi_med_h=float(np.nanmedian(B["vphi"][core_h & okpm])) if (core_h & okpm).any() else float("nan"),
                 l_med_g=float(np.median(B["l"][core_g])) if core_g.any() else float("nan"), b_med_g=float(np.median(B["b"][core_g])) if core_g.any() else float("nan"))
    return dict(tests={k: dict(p=v[0], n_g=v[1], n_h=v[2]) for k, v in tests.items()}, family_p=famp, **extra)
def distinct(idn, thr=0.01): return sum(1 for x in idn["family_p"].values() if np.isfinite(x) and x < thr) >= 2

# ------------------------------------------------------------------ (c) mixture f
def mixf_nll(f, v, e2, P, init, wfix0=False, maxit=3000, tol=1e-9):
    """-lnL of (1-w) N(mu_h, f^2 P + e^2) + w N(mu_g, s_g^2 + e^2), nuisances by EM (deterministic start)."""
    Vh = f * f * P + e2
    if wfix0:
        mu = np.sum(v / Vh) / np.sum(1 / Vh); return 0.5 * np.sum((v - mu) ** 2 / Vh + np.log(Vh)), dict(w=0.0, mu_h=mu)
    w, mh, mg, ag = init["w"], init["mu_h"], init["mu_g"], min(init["s_g"], init["cap"]) ** 2; old = -np.inf
    for _ in range(maxit):
        Vg = ag + e2
        lg = math.log(max(w, 1e-300)) - 0.5 * np.log(2 * np.pi * Vg) - 0.5 * (v - mg) ** 2 / Vg
        lh = math.log(max(1 - w, 1e-300)) - 0.5 * np.log(2 * np.pi * Vh) - 0.5 * (v - mh) ** 2 / Vh
        L = np.logaddexp(lg, lh); ll = L.sum(); qg = np.exp(lg - L); qh = 1 - qg
        w = qg.mean(); mh = np.sum(qh * v / Vh) / np.sum(qh / Vh)
        bg = mg + ag / Vg * (v - mg); Bg = ag - ag * ag / Vg; ng = max(qg.sum(), 1e-9)
        mg = np.sum(qg * bg) / ng; ag = min(max(np.sum(qg * ((bg - mg) ** 2 + Bg)) / ng, 25.0), init["cap"] ** 2)
        if abs(ll - old) < tol: break
        old = ll
    # convert to RAW1's nll convention (constant 0.5 log 2pi per star dropped)
    return -(ll + 0.5 * len(v) * math.log(2 * np.pi)), dict(w=w, mu_h=mh, mu_g=mg, s_g=math.sqrt(ag), q_g=qg)

def mixf_fit(v, e2, P, init, wfix0=False):
    nll = lambda f: mixf_nll(f, v, e2, P, init, wfix0)[0]
    fb, flo, fhi, nb = R1["prof_interval"](nll, 0.05, 5.0)
    return fb, 0.5 * (fhi - flo), mixf_nll(fb, v, e2, P, init, wfix0)[1]

def predP(r, sin2, model, ft, alpha, beta):
    return R1["sr2_at"](r, model, alpha, beta, ft, 1.0) * R1["proj"](sin2, beta)

def consequence(B, j, model, ft, init, alpha=None, salpha=None, mode="mix", keep=None):
    """f, sigma_f (stat + alpha + beta) for the smooth component of bin j. mode: mix (c1), hard (c3)."""
    a = ALPHA if alpha is None else alpha; sa = SALPHA if salpha is None else salpha
    v, e2, r, s2 = B["v"], B["e"] ** 2, B["r"], B["sin2"]
    if mode == "hard": v, e2, r, s2 = v[keep], e2[keep], r[keep], s2[keep]
    def F(aa, bb, want_s=False):
        P = predP(r, s2, model, ft, aa, bb)
        if mode == "hard":
            if want_s: return R1["fit_f"](v, np.sqrt(e2), P)
            return R1["fit_f"](v, np.sqrt(e2), P)[0], None
        if want_s:
            fb, sb, nu = mixf_fit(v, e2, P, init); return fb, sb, nu
        return minimize_scalar(lambda f: mixf_nll(f, v, e2, P, init)[0], bounds=(0.05, 5.0), method="bounded", options=dict(xatol=1e-6)).x, None
    res = F(a, BETA, True); f, ss = res[0], res[1]
    fa = F(a + sa, BETA)[0]; fb_ = F(a - sa, BETA)[0]
    blo, bhi = R["brange"][j]
    sb = 0.0 if blo == bhi else 0.5 * abs(F(a, bhi)[0] - F(a, blo)[0])
    sa_ = 0.5 * abs(fa - fb_); s = math.sqrt(ss * ss + sa_ * sa_ + sb * sb)
    out = dict(f=f, s=s, s_stat=ss, s_alpha=sa_, s_beta=sb, n=int(len(v)))
    if mode == "mix": out["nuis"] = {k: float(x) for k, x in res[2].items() if k != "q_g"}
    return out
def word(f, s):
    return "HOT" if f > 1 + 2 * s else ("COLD" if f < 1 - 2 * s else "PASS")

# ================================================================== K1 (machinery)
sec("K1 machinery: mixture f with w = 0 equals RAW1's fit_f; two-Gaussian recovery on a synthetic sample")
rng = np.random.default_rng(7); vv = rng.normal(5, 100, 300); ee = rng.uniform(2, 20, 300); PP = rng.uniform(5e3, 1.5e4, 300)
fa, sa_ = R1["fit_f"](vv, ee, PP); fbm, sbm, _ = mixf_fit(vv, ee ** 2, PP, None, wfix0=True)
check("K1a mixture f (w = 0) == RAW1 fit_f", abs(fa - fbm) < 1e-5 and abs(sa_ - sbm) < 1e-5, f"{fa:.8f}/{sa_:.8f} vs {fbm:.8f}/{sbm:.8f}")
rg = np.random.default_rng(11); Nsy = 400; lab = rg.random(Nsy) < 0.3
vs_ = np.where(lab, rg.normal(120, 20, Nsy), rg.normal(0, 90, Nsy)) + rg.normal(0, 5, Nsy); es_ = np.full(Nsy, 5.0)
fs = xd2(vs_, es_); gs, hs = order(fs, vs_)
bt = []
for b in range(B_PARERR):
    ii = rg.integers(0, Nsy, Nsy); x = xd2(vs_[ii], es_[ii]); g_, h_ = order(x, vs_[ii]); bt.append([g_["w"], g_["mu"], g_["s"], h_["mu"], h_["s"]])
bt = np.array(bt); sdv = bt.std(0); est = np.array([gs["w"], gs["mu"], gs["s"], hs["mu"], hs["s"]]); tru = np.array([0.3, 120, 20, 0, 90])
okk = bool(np.all(np.abs(est - tru) <= 3 * sdv))
check("K1b two-Gaussian recovery (w_g, mu_g, s_g, mu_h, s_h) within 3 bootstrap sigma", okk,
      "est " + ", ".join(f"{x:.2f}" for x in est) + " / true " + ", ".join(f"{x:g}" for x in tru) + " / sigma " + ", ".join(f"{x:.2f}" for x in sdv))
stop_if_failed()

# ------------------------------------------------------------------ per-bin arrays
vphi_all, vt_all = vphi_vt(S["V"], S["pos"], S["rh"])
def bin_arrays(j, vel=None, err=None):
    m = S["bin"] == j
    return dict(v=(S["vgsr"] if vel is None else vel)[m], e=(S["verr"] if err is None else err)[m], r=S["r"][m], sin2=S["sin2"][m], n=S["n"][m],
                bsgr=S["bsgr"][m], lsgr=S["lsgr"][m], feh=S["feh"][m], feh_err=S["feh_err"][m], pmok=S["pmok"][m], vphi=vphi_all[m], vt=vt_all[m],
                l=S["l"][m], b=S["b"][m], idx=np.where(m)[0])
BINARR = [bin_arrays(j) for j in range(4)]

# ================================================================== (a) per bin
sec(f"(a) one Gaussian against two, every bin (parametric bootstrap B = {B_REAL}; dispersion floor 5 km/s)")
A = []
for j in range(4):
    Bj = BINARR[j]; e2 = Bj["e"] ** 2
    LR, f1, f2, null = boot_null(Bj["v"], e2, B_REAL, 20261130 + j)
    ms = mixture_summary(Bj["v"], e2, LR, f2, null)
    rgp = np.random.default_rng(20261140 + j); pe = []
    for b in range(B_PARERR):
        ii = rgp.integers(0, len(Bj["v"]), len(Bj["v"])); x = xd2(Bj["v"][ii], e2[ii]); g_, h_ = order(x, Bj["v"][ii])
        pe.append([g_["w"], g_["mu"], g_["s"], h_["w"], h_["mu"], h_["s"]])
    pe = np.array(pe); lo, hi = np.percentile(pe, 16, axis=0), np.percentile(pe, 84, axis=0)
    ms.update(one=f1, null_q99=float(np.percentile(null, 99)), null_q95=float(np.percentile(null, 95)), null=null,
              perr=dict(lo=lo.tolist(), hi=hi.tolist()), two=two_comp(ms))
    A.append(ms)
    say(f"  {BN[j]}: N {len(Bj['v'])}; one Gaussian mu {f1['mu']:+.1f} sigma {f1['s']:.2f}; two: group w {ms['g']['w']:.3f} [{lo[0]:.2f},{hi[0]:.2f}] "
        f"mu {ms['g']['mu']:+.1f} [{lo[1]:+.0f},{hi[1]:+.0f}] s {ms['g']['s']:.1f} [{lo[2]:.0f},{hi[2]:.0f}] | halo w {ms['h']['w']:.3f} mu {ms['h']['mu']:+.1f} "
        f"[{lo[4]:+.0f},{hi[4]:+.0f}] s {ms['h']['s']:.1f} [{lo[5]:.0f},{hi[5]:.0f}]; LR {LR:.2f} (null 95/99 pct {ms['null_q95']:.2f}/{ms['null_q99']:.2f}); "
        f"p {ms['p']:.4f}; minor weight {ms['w_minor']:.3f} ({ms['n_minor']:.1f} stars) -> {'TWO COMPONENTS' if ms['two'] else 'one component'}")
say(f"  [{time.time() - T0:.0f} s]")

# floor brackets (B 300, every bin)
sec("(a) brackets: dispersion floor 3 and 10 km/s (B = 300 each), threshold 0.05 / 0.001, minor weight 0.05 / 0.15")
ABR = {}
for fl in (3.0, 10.0):
    ABR[fl] = []
    for j in range(4):
        Bj = BINARR[j]; e2 = Bj["e"] ** 2
        LR, f1, f2, null = boot_null(Bj["v"], e2, 300, 20261150 + j + int(fl), fl)
        ms = mixture_summary(Bj["v"], e2, LR, f2, null); ms["two"] = two_comp(ms); ABR[fl].append(ms)
        say(f"  floor {fl:.0f}: {BN[j]} LR {LR:.2f} p {ms['p']:.4f} w_minor {ms['w_minor']:.3f} group mu {ms['g']['mu']:+.1f} s {ms['g']['s']:.1f} -> {'TWO' if ms['two'] else 'one'}")
for j in range(4):
    say(f"  {BN[j]}: p<0.05 -> {'TWO' if two_comp(A[j], 0.05) else 'one'}; p<0.001 -> {'TWO' if two_comp(A[j], 0.001) else 'one'}; "
        f"wmin 0.05 -> {'TWO' if two_comp(A[j], 0.01, 0.05) else 'one'}; wmin 0.15 -> {'TWO' if two_comp(A[j], 0.01, 0.15) else 'one'}")
say(f"  [{time.time() - T0:.0f} s]")

# ================================================================== (b) identity, every bin (graded where (a) says TWO; forced otherwise)
sec("(b) identity of the candidate group (smaller-dispersion component), every bin; graded only where (a) says TWO COMPONENTS")
IDN = []
for j in range(4):
    idn = identity(BINARR[j], A[j]["q_g"], 20261160 + j); IDN.append(idn)
    tag = "graded" if A[j]["two"] else "forced (not TWO COMPONENTS)"
    say(f"  {BN[j]} [{tag}] {idn['split']}: group {idn['n_core_g']} / halo {idn['n_core_h']} stars; family p " +
        ", ".join(f"{F} {p:.4f}" if np.isfinite(p) else f"{F} NOT EVALUABLE" for F, p in idn["family_p"].items()) +
        f" -> {'DISTINCT GROUP' if distinct(idn) else 'not distinct'}")
    say("     tests: " + "; ".join(f"{t} p {x['p']:.4f} ({x['n_g']}/{x['n_h']})" for t, x in idn["tests"].items()))
    say(f"     medians group / halo: r {idn['r_med_g']:.1f} / {idn['r_med_h']:.1f} kpc; |B_Sgr| {idn['absB_med_g']:.1f} / {idn['absB_med_h']:.1f} deg; "
        f"[Fe/H] {idn['feh_med_g']:.2f} / {idn['feh_med_h']:.2f}; v_phi {idn['vphi_med_g']:+.0f} / {idn['vphi_med_h']:+.0f} km/s; group (l, b) median ({idn['l_med_g']:.0f}, {idn['b_med_g']:+.0f})")
DIST = [bool(A[j]["two"] and distinct(IDN[j])) for j in range(4)]
say(f"  DISTINCT GROUP per bin (graded): {dict(zip(BN, DIST))}")
say(f"  [{time.time() - T0:.0f} s]")

# ================================================================== (c) consequence, every bin
sec("(c) consequence: RAW1's statistic with the smooth component only; every bin (graded where DISTINCT GROUP, else forced)")
def init_of(ms): return dict(w=ms["g"]["w"], mu_h=ms["h"]["mu"], mu_g=ms["g"]["mu"], s_g=ms["g"]["s"], cap=0.5 * ms["sone"])
# (c2) alpha recount without the group's stars, per bin
ALPHA_RC = {}
for j in range(4):
    grp = np.zeros(len(S["r"]), bool); grp[BINARR[j]["idx"][A[j]["q_g"] > 0.5]] = True
    S2 = dict(S); S2["win_ok"] = S["win_ok"] & ~grp
    al = R1["fit_alpha"](R1["alpha_setup"](S2, cfg)); ALPHA_RC[j] = (al["alpha"], al["sig"], int(grp.sum()))
    say(f"  (c2) alpha without bin {BN[j]}'s group stars (q > 0.5: {grp.sum()} stars, {int(np.sum(grp & S['win_ok']))} in the window): {al['alpha']:.3f} +/- {al['sig']:.3f} (nominal {ALPHA:.3f})")
CONS = {}
for m, ft in CASES:
    k = CKEY(m, ft); CONS[k] = []
    for j in range(4):
        Bj = BINARR[j]; ini = init_of(A[j])
        c1 = consequence(Bj, j, m, ft, ini)
        c2 = consequence(Bj, j, m, ft, ini, alpha=ALPHA_RC[j][0], salpha=ALPHA_RC[j][1])
        c3 = consequence(Bj, j, m, ft, ini, mode="hard", keep=A[j]["q_g"] <= 0.5)
        b0 = BASE[k][j]
        CONS[k].append(dict(raw1=dict(f=b0["f"], s=b0["s"]), c1=c1, c2=c2, c3=c3, graded=DIST[j]))
    say(f"  {k:20s} " + " | ".join(f"{BN[j]}: RAW1 {x['raw1']['f']:.3f}+/-{x['raw1']['s']:.3f} {word(x['raw1']['f'], x['raw1']['s'])}; "
                                     f"c1 {x['c1']['f']:.3f}+/-{x['c1']['s']:.3f} {word(x['c1']['f'], x['c1']['s'])}; c2 {x['c2']['f']:.3f} {word(x['c2']['f'], x['c2']['s'])}; "
                                     f"c3 {x['c3']['f']:.3f} {word(x['c3']['f'], x['c3']['s'])}{' [graded]' if x['graded'] else ' [forced]'}" for j, x in enumerate(CONS[k])))
say("  graded words (RAW1's word kept where no DISTINCT GROUP):")
GW = {}
for m, ft in CASES:
    k = CKEY(m, ft)
    ws = [word(x["c1"]["f"], x["c1"]["s"]) if x["graded"] else word(x["raw1"]["f"], x["raw1"]["s"]) for x in CONS[k]]
    rw = [word(x["raw1"]["f"], x["raw1"]["s"]) for x in CONS[k]]
    GW[k] = ws
    changed = [BN[j] for j in range(4) if rw[j] == "PASS" and ws[j] != "PASS"]
    say(f"   {k:20s} RAW1 {rw} -> graded {ws}; RAW1-passing bins that change: {changed or 'none'}; row {R1['grade']([x['c1']['f'] if x['graded'] else x['raw1']['f'] for x in CONS[k]], [x['c1']['s'] if x['graded'] else x['raw1']['s'] for x in CONS[k]], BN)[0]}")
say(f"  [{time.time() - T0:.0f} s]")

# ================================================================== twin: shuffled between bins
sec(f"TWIN: velocities (with errors) shuffled among all 20-80 kpc stars, {NSHUF} seeded shuffles; graded against each bin's real-data null")
rgt = np.random.default_rng(20261170); tw_two = 0; tw_dist = 0; TW = []
for t in range(NSHUF):
    perm = rgt.permutation(len(S["r"])); vsh = S["vgsr"][perm]; esh = S["verr"][perm]
    row = []
    for j in range(4):
        Bj = bin_arrays(j, vsh, esh); e2 = Bj["e"] ** 2; LR, f1, f2 = lr_of(Bj["v"], e2)
        ms = mixture_summary(Bj["v"], e2, LR, f2, A[j]["null"]); tw = two_comp(ms); dg = False
        if tw:
            tw_two += 1; idn = identity(Bj, ms["q_g"], 20261180 + 10 * t + j); dg = distinct(idn); tw_dist += int(dg)
        row.append((round(ms["p"], 4), tw, dg))
    TW.append(row)
    say(f"  shuffle {t:2d}: " + "  ".join(f"{BN[j]} p {x[0]:.3f}{' TWO' if x[1] else ''}{' DISTINCT' if x[2] else ''}" for j, x in enumerate(row)))
check("TWIN: at most 3 of 80 bin-shuffles TWO COMPONENTS", tw_two <= 3, f"{tw_two} of {4 * NSHUF}")
check("TWIN: at most 1 of 80 bin-shuffles DISTINCT GROUP", tw_dist <= 1, f"{tw_dist} of {4 * NSHUF}")
say(f"  [{time.time() - T0:.0f} s]")

# ================================================================== mutations (separate file)
MUT = open(os.path.join(HERE, "mwt2_A1_MUTATE.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("MWT2 mutations (FROZEN_CRITERIA.md section 6), both in 40-55 kpc.")
j = 2; Bj = BINARR[j]; rgm = np.random.default_rng(20261190)
s0 = rgm.integers(0, len(Bj["v"])); angs = np.degrees(np.arccos(np.clip(Bj["n"] @ Bj["n"][s0], -1, 1))); near = np.argsort(angs)[:40]
G = {k: (np.concatenate([x, x[near]]) if isinstance(x, np.ndarray) and len(x) == len(Bj["v"]) else x) for k, x in Bj.items()}
mub = float(np.mean(Bj["v"])); nadd = len(near)
G["v"] = np.concatenate([Bj["v"], mub + 150.0 + rgm.normal(0, 15.0, nadd)])
# common 60 km/s tangential offset along the local east direction, then v_phi and v_t recomputed for the copies
ii = Bj["idx"][near]; Vc = S["V"][ii] + 60.0 * S["ea"][ii]
Vc[:, :] += (G["v"][-nadd:] - S["vgsr"][ii])[:, None] * S["n"][ii]
vpc, vtc = vphi_vt(Vc, S["pos"][ii], S["rh"][ii]); G["vphi"] = np.concatenate([Bj["vphi"], vpc]); G["vt"] = np.concatenate([Bj["vt"], vtc])
G["pmok"] = np.concatenate([Bj["pmok"], np.ones(nadd, bool)])
LRg, f1g, f2g, nullg = boot_null(G["v"], G["e"] ** 2, B_MUT, 20261191)
msg = mixture_summary(G["v"], G["e"] ** 2, LRg, f2g, nullg); twg = two_comp(msg)
idg = identity(G, msg["q_g"], 20261192); dgg = distinct(idg)
cg = consequence(G, j, "FW_census", "canonical", init_of(msg))
tru = np.zeros(len(G["v"]), bool); tru[-nadd:] = True
recov = int(np.sum(msg["q_g"][tru] > 0.5)); fp = int(np.sum(msg["q_g"][~tru] > 0.5))
f_raw = BASE["FW_census/canonical"][j]["f"]
okG = twg and dgg and abs(cg["f"] - f_raw) <= 0.03
msay(f"G moving group: 40 stars added at mu_bin + 150 +/- 15 km/s on a {np.max(angs[near]):.1f} deg patch, PMs offset 60 km/s: "
     f"LR {LRg:.2f} p {msg['p']:.4f}; group w {msg['g']['w']:.3f} mu {msg['g']['mu']:+.1f} s {msg['g']['s']:.1f}; TWO {twg}; "
     f"family p " + ", ".join(f"{F} {p:.4f}" for F, p in idg["family_p"].items()) + f"; DISTINCT {dgg}; planted stars with q > 0.5: {recov}/40, others {fp}; "
     f"f (FW census canonical) RAW1 un-mutated {f_raw:.3f}, raw on mutated {R1['fit_f'](G['v'], G['e'], predP(G['r'], G['sin2'], 'FW_census', 'canonical', ALPHA, BETA))[0]:.3f}, "
     f"smooth (c1) {cg['f']:.3f} +/- {cg['s']:.3f}: |diff| {abs(cg['f'] - f_raw):.3f} <= 0.03; bites: {okG}")
Sm = dict(Bj); Sm["v"] = Bj["v"] + np.random.default_rng(20261193).normal(0, 50.0, len(Bj["v"]))
LRs, f1s, f2s, nulls = boot_null(Sm["v"], Sm["e"] ** 2, B_MUT, 20261194)
mss = mixture_summary(Sm["v"], Sm["e"] ** 2, LRs, f2s, nulls); tws = two_comp(mss); dgs = False
if tws: dgs = distinct(identity(Sm, mss["q_g"], 20261195))
fS = R1["fit_f"](Sm["v"], Sm["e"], predP(Sm["r"], Sm["sin2"], "FW_census", "canonical", ALPHA, BETA))[0]
okS = not (tws and dgs)
msay(f"S scatter only (+N(0, 50) km/s): sigma {f1s['s']:.1f} (was {A[j]['one']['s']:.1f}); LR {LRs:.2f} p {mss['p']:.4f}; TWO {tws}; DISTINCT {dgs}; "
     f"f (FW census canonical) {f_raw:.3f} -> {fS:.3f}; not flagged as a group: {okS}")
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()
say(f"  mutations: G bites {okG}; S not flagged {okS} (details in mwt2_A1_MUTATE.out)")

# ================================================================== labels
sec("Labels (30-40 kpc bin; FW census headline per footing, FW rc by the same rule)")
def label_for(k, pthr=0.01, wmin=0.10, fthr=0.01, cmode="c1", Aset=None):
    Aj = (Aset or A)[1]; two = two_comp(Aj, pthr, wmin)
    if not okG or len(BINARR[1]["v"]) < 100: return "NO POWER"
    if not two: return "HOT BIN IS ONE POPULATION (step a: not two components)"
    idn = IDN[1] if Aset is None else identity(BINARR[1], Aj["q_g"], 20261161)
    if not distinct(idn, fthr): return "HOT BIN IS ONE POPULATION (step b: two components, not a distinct group)"
    if Aset is not None:
        c = consequence(BINARR[1], 1, *k.split("/"), init_of(Aj)); w_ = word(c["f"], c["s"])
    else:
        x = CONS[k][1][cmode]; w_ = word(x["f"], x["s"])
    return {"PASS": "HOT BIN IS A DISTINCT GROUP PLUS A SMOOTH HALO AND THE SMOOTH PART PASSES",
            "HOT": "HOT BIN HAS TWO COMPONENTS BUT THE SMOOTH PART STILL FAILS",
            "COLD": "HOT BIN IS A DISTINCT GROUP PLUS A SMOOTH HALO AND THE SMOOTH PART FAILS COLD"}[w_]
LAB = {}
for m, ft in GRADED:
    k = CKEY(m, ft); lab = label_for(k)
    br = {"p<0.05": label_for(k, pthr=0.05), "p<0.001": label_for(k, pthr=0.001), "wmin 0.05": label_for(k, wmin=0.05), "wmin 0.15": label_for(k, wmin=0.15),
          "family 0.05": label_for(k, fthr=0.05), "family 0.001": label_for(k, fthr=0.001), "c2": label_for(k, cmode="c2"), "c3": label_for(k, cmode="c3"),
          "floor 3": label_for(k, Aset=[None, ABR[3.0][1]]), "floor 10": label_for(k, Aset=[None, ABR[10.0][1]])}
    flips = [t for t, x in br.items() if x != lab]
    LAB[k] = dict(label=lab, fragile=flips, brackets=br)
    say(f"  {k:20s}: {lab}{' , FRAGILE (' + ', '.join(f'{t}: {br[t]}' for t in flips) + ')' if flips else ''}")
if FAILED: say(f"NOTE: checks failed: {FAILED} (reported; the frozen rule stops only on the known answers)")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if k not in ("q_g", "null", "q")}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o
RES = dict(base={k: [dict(f=x["f"], s=x["s"]) for x in v] for k, v in BASE.items()}, mixture=A, brackets_floor={str(k): v for k, v in ABR.items()},
           identity=IDN, distinct=DIST, alpha_recount={BN[j]: v for j, v in ALPHA_RC.items()}, consequence=CONS, graded_words=GW,
           twin=dict(rows=TW, two=tw_two, distinct=tw_dist), mutations=dict(G=dict(LR=LRg, p=msg["p"], g=msg["g"], two=twg, family_p=idg["family_p"], distinct=dgg,
           recovered=recov, false_pos=fp, f_raw=f_raw, f_smooth=cg["f"], s_smooth=cg["s"], bites=okG),
           S=dict(LR=LRs, p=mss["p"], two=tws, distinct=dgs, f_before=f_raw, f_after=fS, ok=okS)), labels=LAB, failed=FAILED, B_real=B_REAL)
json.dump(clean(RES), open(os.path.join(HERE, "mwt2_A1_results.json"), "w"), indent=1)
say(f"\nruntime {time.time() - T0:.0f} s")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
