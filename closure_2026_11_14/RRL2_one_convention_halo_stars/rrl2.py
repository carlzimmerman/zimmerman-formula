#!/usr/bin/env python3
"""
RRL2 -- row 28 under one convention: the PS1 RR Lyrae density slope fitted on the kinematic tracers' own sky cells,
plus MWT1's detected corrections C (measured beta(r), logg cut, overdensity mask, error scale, hemisphere weight).
Criteria: FROZEN_CRITERIA.md (commit 2859f64033, alone, before this script).
Usage: python3 -I -B rrl2.py <PS1 table5_subset.tsv> <DES table1.tsv> <MWS_BHB.fits>
Writes rrl2.out, rrl2_results.json, rrl2_MUTATE.out. Data paths are never printed.
The first part (to the line 'END OF COPY FROM rrl1.py') is closure_2026_11_13/RRL1_halo_slope_from_rr_lyrae/rrl1.py
lines 13-305, with only: output names, and an own-cells footprint switch (keep_of; grid / hist_w cache keys).
MWT1's estimator pieces (fit_scale, est_bin, the B-data / mask / error-scale options) are copied from
closure_2026_11_13/MWT1_hot_bin_assumptions/mwt1.py lines 84-102, 184-228, with citation below.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[k] = "1"
import ast, json, math, hashlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import minimize, minimize_scalar
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
RAW1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_12", "RAW1_halo_stars_direct"))
PS1F, DESF, FITS = sys.argv[1], sys.argv[2], sys.argv[3]
SHA = dict(ps1="ab4b837f98157b4bdde82d09574ea8c62d8175580638bd46b2227df28031f813",
           des="94e3eb68aef19c94f4374ae1ab351b6552e0d3b7c1cb001622d2ddd77f898303",
           bhb="5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246")
TAG = os.environ.get("RRL2_TAG", "")
OUT = open(os.path.join(HERE, f"rrl2{TAG}.out"), "w")
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

# ------------------------------------------------------------------ RAW1's functions, unchanged (method of mwt1.py)
sys.path.insert(0, RAW1)
tree = ast.parse(open(os.path.join(RAW1, "raw1.py")).read())
KEEP_ASSIGN = ("K474", "BINS", "NOMINAL", "FOOT", "SG", "NGRID", "_GCACHE")
body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in KEEP_ASSIGN)]
R1 = {"FITS": FITS, "HERE": RAW1, "__name__": "raw1_functions"}
exec(compile(ast.Module(body=body, type_ignores=[]), "raw1.py", "exec"), R1)
MOD = R1["MOD"]; NOMINAL = R1["NOMINAL"]; SG = R1["SG"]
CASES = [("FW_census", "canonical"), ("FW_census", "alt"), ("FW_rc", "canonical"), ("FW_rc", "alt"), ("H", None), ("N", None)]
CKEY = lambda m, f: f"{m}/{f}" if f else m
BN = ["20-30", "30-40", "40-55", "55-80"]

# ------------------------------------------------------------------ copied from mwt1.py (generalised tracer; constant beta here)
BEDGE = (30.0, 40.0, 55.0)
def beta_of(r, bt):
    r = np.asarray(r, float); b = np.full(r.shape, bt[0])
    b = np.where(r >= BEDGE[0], bt[1], b); b = np.where(r >= BEDGE[1], bt[2], b); b = np.where(r >= BEDGE[2], bt[3], b)
    return b
def tracer(s, ak):
    s = np.asarray(s, float)
    if not isinstance(ak, tuple): return (s / 40.0) ** (-float(ak))
    ai, ao, rb = ak; return np.where(s < rb, (s / rb) ** (-ai), (s / rb) ** (-ao))
_SC = {}
def sr2_grid(model, footing, a0m, ak, bt):
    key = (model, footing, a0m, ak, bt)
    if key not in _SC:
        b = beta_of(SG, bt); lnS = np.log(SG)
        lnI = 2 * b[0] * lnS[0] + np.concatenate([[0.0], np.cumsum(0.5 * (2 * b[1:] + 2 * b[:-1]) * np.diff(lnS))])
        n = tracer(SG, ak); I = np.exp(lnI)
        w = n * I * R1["g_on_grid"](model, footing, a0m) * MOD.KPC
        seg = 0.5 * (w[1:] + w[:-1]) * np.diff(SG)
        cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
        _SC[key] = cum / (n * I) / 1e6
    return _SC[key]
def predP(r, sin2, model, footing, a0m, ak, bt):
    s2 = np.exp(np.interp(np.log(r), np.log(SG), np.log(np.maximum(sr2_grid(model, footing, a0m, ak, bt), 1e-30))))
    return s2 * (1.0 - beta_of(r, bt) * sin2)

# ------------------------------------------------------------------ table reader (VizieR tsv)
def read_tsv(path):
    head = None; rows = []; skip = 0
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip(): continue
            if head is None: head = line.rstrip("\n").split("\t"); skip = 2; continue
            if skip: skip -= 1; continue
            rows.append(line.rstrip("\n").split("\t"))
    cols = {h.strip(): [r[j] if j < len(r) else "" for r in rows] for j, h in enumerate(head)}
    return cols
def fcol(c):
    out = np.full(len(c), np.nan)
    for i, x in enumerate(c):
        x = x.strip()
        if x:
            try: out[i] = float(x)
            except ValueError: pass
    return out

# ------------------------------------------------------------------ sky grid (equal area)
NRA, NSD = 180, 90
DSD = 2.0 / NSD
def cell_of(ra, dec):
    i = np.clip((np.asarray(ra) % 360.0 / 2.0).astype(int), 0, NRA - 1)
    j = np.clip(((np.sin(np.radians(dec)) + 1.0) / DSD).astype(int), 0, NSD - 1)
    return j * NRA + i
CI, CJ = np.meshgrid(np.arange(NRA), np.arange(NSD)); CI, CJ = CI.ravel(), CJ.ravel()
CRA = 2.0 * CI + 1.0; CDEC = np.degrees(np.arcsin(-1.0 + (CJ + 0.5) * DSD)); NCELL = len(CRA)
from astropy.coordinates import SkyCoord
import astropy.units as u
_cg = SkyCoord(ra=CRA * u.deg, dec=CDEC * u.deg, frame="icrs").galactic
CL, CB = _cg.l.deg, _cg.b.deg
CBSGR = R1["sgr_lat_lon"](CL, CB)[1]
def unitv(ra, dec):
    ra, dec = np.radians(ra), np.radians(dec)
    return np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T
CU = unitv(CRA, CDEC)
def angsep_mask(ra0, dec0, rad):
    return CU @ unitv(np.array([ra0]), np.array([dec0]))[0] >= math.cos(math.radians(rad))
MASKS_SOUTH = [(80.89, -69.76, 27.1), (13.19, -72.83, 12.6), (39.997, -34.449, 2.0), (15.039, -33.709, 1.0)]
P0, RM = R1["frame_affine"](NOMINAL["R0"], NOMINAL["zsun"])

def clump_rule(ra, dec, dm):
    """frozen rule: >= 4 other stars within 0.5 deg and |dDM| < 0.25 -> clump star; mask cells within 1.5 deg."""
    v = unitv(ra, dec); T = cKDTree(v); ch = 2 * math.sin(math.radians(0.25))
    nb = T.query_ball_point(v, ch)
    cl = np.array([sum(1 for j in L if j != i and abs(dm[j] - dm[i]) < 0.25) >= 4 for i, L in enumerate(nb)], bool)
    mask = np.zeros(NCELL, bool)
    if cl.any():
        TC = cKDTree(CU); ch2 = 2 * math.sin(math.radians(0.75))
        for L in TC.query_ball_point(v[cl], ch2):
            mask[L] = True
    return cl, mask

# ------------------------------------------------------------------ surveys
def load_ps1():
    c = read_tsv(PS1F)
    return dict(ra=fcol(c["RAJ2000"]), dec=fcol(c["DEJ2000"]), s3ab=fcol(c["S3ab"]), dm=fcol(c["DM"]), ebv=fcol(c["E(B-V)"]))
def load_des():
    c = read_tsv(DESF)
    return dict(ra=fcol(c["RAJ2000"]), dec=fcol(c["DEJ2000"]), dm=fcol(c["mu"]), Ag=fcol(c["Ag"]),
                rf=np.vstack([fcol(c["RF1"]), fcol(c["RF2"]), fcol(c["RF3"])]).T,
                acc=np.array([x.strip() == "True" for x in c["ACc"]]), sys=np.array([x.strip() != "" for x in c["Sys"]]))

def cell_median(cells, val):
    med = np.full(NCELL, np.nan); o = np.argsort(cells); cs, vs = cells[o], val[o]
    edges = np.flatnonzero(np.diff(cs)) + 1; starts = np.concatenate([[0], edges]); ends = np.concatenate([edges, [len(cs)]])
    for a, b in zip(starts, ends):
        med[cs[a]] = np.nanmedian(vs[a:b])
    return med

_FP = {}
def footprint(survey, score, bcut, sgr):
    key = (survey, score, bcut, sgr)
    if key in _FP: return _FP[key]
    if survey == "ps1":
        T = PS1; allcells = cell_of(T["ra"], T["dec"]); cov = np.bincount(allcells, minlength=NCELL) > 0
        cov &= CDEC > -30.0
        red = cell_median(allcells, T["ebv"]) > 0.25
        sel = (T["s3ab"] > score) & np.isfinite(T["dm"])
    else:
        T = DES; allcells = cell_of(T["ra"], T["dec"]); occ = np.bincount(allcells, minlength=NCELL) > 0
        o2 = occ.reshape(NSD, NRA); nbr = np.zeros_like(o2, int)
        for dj in (-1, 0, 1):
            for di in (-1, 0, 1):
                if dj == 0 and di == 0: continue
                sh = np.roll(o2, di, axis=1)
                if dj == 1: sh = np.vstack([sh[1:], np.zeros((1, NRA), bool)])
                elif dj == -1: sh = np.vstack([np.zeros((1, NRA), bool), sh[:-1]])
                nbr += sh
        cov = occ | (nbr.ravel() >= 5)
        red = cell_median(allcells, T["Ag"]) > 0.80
        sel = np.isfinite(T["dm"]) & ~T["acc"] & ~T["sys"]
        if score is not None: sel &= np.min(T["rf"], axis=1) >= score
    keep = cov & ~(red == True) & (np.abs(CB) > bcut)
    if sgr is not None: keep &= np.abs(CBSGR) >= sgr
    for ra0, de0, rad in MASKS_SOUTH: keep &= ~angsep_mask(ra0, de0, rad)
    cl, cmask = clump_rule(T["ra"][sel], T["dec"][sel], T["dm"][sel])
    keep &= ~cmask
    cent = []
    if cl.any():
        v = unitv(T["ra"][sel][cl], T["dec"][sel][cl]); TT = cKDTree(v); seen = np.zeros(cl.sum(), bool)
        for i in range(cl.sum()):
            if seen[i]: continue
            L = TT.query_ball_point(v[i], 2 * math.sin(math.radians(1.0))); seen[L] = True
            cent.append((float(np.mean(T["ra"][sel][cl][L])), float(np.mean(T["dec"][sel][cl][L])), len(L), float(np.median(T["dm"][sel][cl][L]))))
    _FP[key] = dict(keep=keep, sel=sel, nclump=int(cl.sum()), nmask=int(cmask.sum()), centres=cent, ncell=int(keep.sum()),
                    area=float(keep.sum() * 4 * math.pi * (180 / math.pi) ** 2 / NCELL))
    return _FP[key]

OWNCELLS = None   # RRL2: cells holding RAW1's sample stars (set below)
def keep_of(cfg):
    k = footprint(cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"])["keep"]
    return (k & OWNCELLS) if cfg.get("own", False) else k

def galpos(ra, dec, d):
    n = unitv(ra, dec) @ RM.T; pos = P0 + d[:, None] * n
    return np.linalg.norm(pos, axis=1), pos[:, 2]

# ------------------------------------------------------------------ data sample and normalisation grid
def comp_ps1(kind):
    if kind == "none": return lambda dm: np.ones_like(dm)
    x0 = 20.57 if kind == "paper" else 20.07
    return lambda dm: 1.0 / (1.0 + np.exp(4.1 * (dm + 0.6 - x0)))
def comp_des(kind):
    return lambda dm: np.ones_like(dm)

def sample(cfg, dm_override=None):
    T = PS1 if cfg["survey"] == "ps1" else DES
    fp = footprint(cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"])
    idx = np.where(fp["sel"])[0]; idx = idx[keep_of(cfg)[cell_of(T["ra"][idx], T["dec"][idx])]]
    dm = T["dm"][idx] if dm_override is None else dm_override
    d = 10 ** (dm / 5.0 - 2.0) * cfg["dscale"]   # kpc
    r, z = galpos(T["ra"][idx], T["dec"][idx], d)
    ink = (r >= cfg["rlo"]) & (r < cfg["rhi"])
    return dict(idx=idx[ink], r=r[ink], z=z[ink], dm_all=T["dm"][idx], idx_all=idx)

HB = np.linspace(math.log(5.0), math.log(250.0), 6001); HC = 0.5 * (HB[1:] + HB[:-1])
_GR = {}
def grid(cfg):
    key = (cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"], cfg["comp"], cfg["dscale"], cfg["rlo"], cfg["rhi"], cfg.get("own", False))
    if key in _GR: return _GR[key]
    fp = footprint(cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"])
    cells = np.where(keep_of(cfg))[0]
    ra = np.concatenate([CRA[cells] + o for o in (-0.5, 0.5, -0.5, 0.5)])
    sd = np.concatenate([np.sin(np.radians(CDEC[cells])) + o for o in (-DSD / 4, -DSD / 4, DSD / 4, DSD / 4)])
    n = unitv(ra, np.degrees(np.arcsin(sd))) @ RM.T
    dlo, dhi = max(cfg["rlo"] - 8.2, 0.5), cfg["rhi"] + 8.5
    lnd = np.linspace(math.log(dlo), math.log(dhi), 121); lnc = 0.5 * (lnd[1:] + lnd[:-1]); dl = lnd[1] - lnd[0]
    C = (comp_ps1 if cfg["survey"] == "ps1" else comp_des)(cfg["comp"])
    R_, Z_, W_ = [], [], []
    for x in lnc:
        d = math.exp(x); pos = P0 + d * n; r = np.linalg.norm(pos, axis=1)
        dm_obs = 5 * math.log10(d / cfg["dscale"] * 1000.0) - 5
        k = (r >= cfg["rlo"]) & (r < cfg["rhi"])
        R_.append(r[k]); Z_.append(pos[k, 2]); W_.append(np.full(k.sum(), d ** 3 * dl * float(C(np.array([dm_obs]))[0])))
    G = dict(r=np.concatenate(R_), z=np.concatenate(Z_), w=np.concatenate(W_))
    _GR[key] = G
    return G

def lnrq(r, z, q): return 0.5 * np.log(r * r - z * z + (z / q) ** 2)
_HW = {}
def hist_w(cfg, q):
    key = (cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"], cfg["comp"], cfg["dscale"], cfg["rlo"], cfg["rhi"], q, cfg.get("own", False))
    if key not in _HW:
        G = grid(cfg); _HW[key] = np.histogram(lnrq(G["r"], G["z"], q), bins=HB, weights=G["w"])[0]
    return _HW[key]

# ------------------------------------------------------------------ likelihood and fits
def lnn(x, p):
    if len(p) == 1: return -p[0] * (x - math.log(40.0))
    ai, ao, rb = p; lr = math.log(rb)
    return np.where(x < lr, -ai * (x - lr), -ao * (x - lr))
def nll(p, X, W):
    l = lnn(HC, p); m = l.max(); Z = np.sum(W * np.exp(l - m))
    return -(np.sum(lnn(X, p))) + len(X) * (math.log(Z) + m)
def fit_single(X, W):
    a, lo, hi, nb = R1["prof_interval"](lambda a: nll((a,), X, W), 0.0, 10.0)
    return dict(a=a, lo=lo, hi=hi, sig=0.5 * (hi - lo), nll=nb, N=int(len(X)))
def fit_broken(X, W, rbr=(25.0, 75.0), a0=4.5):
    best = None
    for rb in np.arange(rbr[0], rbr[1] + 1e-9, 2.5):
        f = lambda p: nll((p[0], p[1], rb), X, W)
        res = minimize(f, [a0, a0], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-6, maxiter=2000))
        if best is None or res.fun < best[1]: best = (np.array([res.x[0], res.x[1], rb]), res.fun)
    def f3(p):
        if p[2] < rbr[0] or p[2] > rbr[1]: return 1e30
        return nll((p[0], p[1], p[2]), X, W)
    res = minimize(f3, best[0], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-7, maxiter=4000,
                   initial_simplex=np.array([best[0], best[0] + [0.2, 0, 0], best[0] + [0, 0.2, 0], best[0] + [0, 0, 1.0]])))
    p = res.x if res.fun <= best[1] else best[0]; fun = min(res.fun, best[1])
    h = np.array([0.05, 0.05, 0.5]); H = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            ei = np.eye(3)[i] * h[i]; ej = np.eye(3)[j] * h[j]
            fu = lambda q_: nll((q_[0], q_[1], q_[2]), X, W)
            H[i, j] = (fu(p + ei + ej) - fu(p + ei - ej) - fu(p - ei + ej) + fu(p - ei - ej)) / (4 * h[i] * h[j])
    try:
        Cv = np.linalg.inv(H)
        if np.any(np.diag(Cv) <= 0) or not np.all(np.isfinite(Cv)): raise np.linalg.LinAlgError
    except np.linalg.LinAlgError:
        Cv = np.diag(1.0 / np.maximum(np.abs(np.diag(H)), 1e-6))
    s = np.sqrt(np.diag(Cv))
    return dict(ain=float(p[0]), aout=float(p[1]), rb=float(p[2]), sin=float(s[0]), sout=float(s[1]), srb=float(s[2]),
                cov=Cv.tolist(), nll=float(fun), N=int(len(X)))
def fit_both(X, W, rbr=(25.0, 75.0)):
    s = fit_single(X, W); b = fit_broken(X, W, rbr, a0=s["a"]); b["LR"] = float(2 * (s["nll"] - b["nll"]))
    return s, b

def run_fit(cfg, q=None, dm_override=None, thin=None):
    q = cfg["q"] if q is None else q
    Sx = sample(cfg, dm_override)
    X = lnrq(Sx["r"], Sx["z"], q)
    if thin is not None: X = X[thin(Sx)]
    W = hist_w(cfg, q)
    s, b = fit_both(X, W, cfg["rbr"])
    return dict(single=s, broken=b, N=int(len(X)), X=X, rbr=cfg["rbr"])

def mock(cfg, q, p, N, rng):
    G = grid(cfg); x = lnrq(G["r"], G["z"], q)
    l = lnn(x, p); w = G["w"] * np.exp(l - l.max()); w /= w.sum()
    return x[rng.choice(len(x), size=N, p=w)]

def fmt_s(s): return f"{s['a']:.3f} [{s['lo']:.3f}, {s['hi']:.3f}] (N {s['N']})"
def fmt_b(b): return (f"in {b['ain']:.3f} +/- {b['sin']:.3f}, out {b['aout']:.3f} +/- {b['sout']:.3f}, break {b['rb']:.1f} +/- {b['srb']:.1f} kpc; "
                      f"2 dlnL vs single {b['LR']:.2f}")

# ------------------------------------------------------------------ END OF COPY FROM rrl1.py
# ------------------------------------------------------------------ copied from mwt1.py lines 84-102 (scale fit; X = ones path) and 217-228 (estimator, E off)
def fit_scale(v, e, P, lo=0.05, hi=5.0):
    X = np.ones((len(v), 1))
    def solve(f):
        var = f * f * P + e * e; w = 1.0 / var
        A = X.T @ (X * w[:, None]); bvec = X.T @ (w * v)
        th = np.linalg.lstsq(A, bvec, rcond=None)[0]; res = v - X @ th
        return var, th, res, A
    def nll(f):
        var, th, res, A = solve(f); return 0.5 * np.sum(res * res / var + np.log(var))
    fb, flo, fhi, nb = R1["prof_interval"](nll, lo, hi)
    return dict(f=fb, s=0.5 * (fhi - flo), nll=nb)
def est_bin(v, e, P, gl_b, F):
    if F:
        nN, nS = np.sum(gl_b > 0), np.sum(gl_b <= 0)
        if nN >= 15 and nS >= 15:
            rN = fit_scale(v[gl_b > 0], e[gl_b > 0], P[gl_b > 0]); rS = fit_scale(v[gl_b <= 0], e[gl_b <= 0], P[gl_b <= 0])
            return 0.5 * (rN["f"] + rS["f"]), 0.5 * math.hypot(rN["s"], rS["s"])
    r = fit_scale(v, e, P); return r["f"], r["s"]

# copied from rrl1.py lines 399-408
def prof_of(fit, broken):
    if broken: return (fit["broken"]["ain"], fit["broken"]["aout"], fit["broken"]["rb"])
    return fit["single"]["a"]
def draws_of(fit, broken, n, rng):
    if broken:
        b = fit["broken"]; mu = np.array([b["ain"], b["aout"], b["rb"]]); C = np.array(b["cov"])
        P = rng.multivariate_normal(mu, C, size=n); P[:, :2] = np.maximum(P[:, :2], 0.0)
        P[:, 2] = np.clip(P[:, 2], fit["rbr"][0], fit["rbr"][1])
        return [tuple(map(float, x)) for x in P]
    s = fit["single"]; return [float(max(x, 0.0)) for x in rng.normal(s["a"], s["sig"], n)]

A0EXACT = {"canonical": 9.3603e-11 / 9.36e-11, "alt": 1.1312e-10 / 1.13e-10}
MWT1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_13", "MWT1_hot_bin_assumptions"))
RRL1 = os.path.normpath(os.path.join(HERE, "..", "..", "closure_2026_11_13", "RRL1_halo_slope_from_rr_lyrae"))
import time
T0 = time.time()

# ================================================================== inputs
sec("RRL2: inputs")
for nm, p in (("ps1", PS1F), ("des", DESF), ("bhb", FITS)):
    check(f"sha256 {nm}", sha(p) == SHA[nm], f"{sha(p)[:16]}... ({os.path.basename(p)})")
stop_if_failed()
PS1 = load_ps1(); DES = load_des()
check("row counts", len(PS1["ra"]) == 239044 and len(DES["ra"]) == 6971, f"PS1 {len(PS1['ra'])}, DES {len(DES['ra'])} (DES loaded, not used)")
stop_if_failed()
NOMC = dict(survey="ps1", score=0.8, bcut=20.0, sgr=15.0, comp="paper", dscale=1.0, rlo=20.0, rhi=80.0, q=1.0, rbr=(25.0, 75.0))

# BHB sample (RAW1) with MWT1's extra columns
from astropy.io import fits
D = R1["load"]()
_h = fits.open(FITS, memmap=False); _rv = _h["RVTAB"].data
D["logg"] = np.asarray(_rv["LOGG"], float); D["logg_err"] = np.asarray(_rv["LOGG_ERR"], float)
_c = SkyCoord(ra=D["ra"] * u.deg, dec=D["dec"] * u.deg, frame="icrs").galactic; D["b"] = _c.b.deg
cfgR = dict(NOMINAL); S = R1["build"](D, cfgR); R = R1["measure"](S, cfgR)
for k in ("logg", "logg_err", "b"): S[k] = D[k][S["i"]]
BINS = R1["BINS"]
S["bin"] = np.array([next((j for j, (a, b) in enumerate(BINS) if a <= x < b), -1) for x in S["r"]])
J1 = json.load(open(os.path.join(RAW1, "raw1_results.json")))["nominal"]
check("RAW1 counts", list(R["counts"]) == J1["counts"] == [865, 264, 241, 125] and all(np.array_equal(R["bsel"][j], S["bin"] == j) for j in range(4)), f"{R['counts']}")
BETA = R["beta"]; BR = R["brange"]; a_raw, sa_raw = R["alpha"]["alpha"], R["alpha"]["sig"]
JM = json.load(open(os.path.join(MWT1, "mwt1_results.json")))
S2LIST = np.array(JM["combination"]["flags"]["S2"], dtype=int); SX = float(JM["combination"]["flags"]["Xerr"])
check("MWT1 flags read", len(S2LIST) == 31 and JM["combination"]["flags"]["L"] == 3.75 and JM["combination"]["flags"]["B"] and JM["combination"]["flags"]["F"]
      and not JM["combination"]["flags"]["E"] and JM["combination"]["flags"]["D"] is None, f"S2 {len(S2LIST)} stars, X-err {SX:.4f}, L 3.75, B, F; E and D off")
PMB = [(R["pmbeta"][j]["beta"], R["pmbeta"][j]["sig"]) if R["usable"][j] else (R["beta"], R["sbeta"]) for j in range(3)]
check("MWT1 per-bin beta reproduced", max(abs(PMB[j][0] - JM["diag"]["B"]["LR"]["per"][j][0]) for j in range(3)) < 1e-6,
      ", ".join(f"{b:.3f} +/- {s:.3f}" for b, s in PMB))
stop_if_failed()

def opt_C(s2=True):
    keep = ~((S["logg"] > 3.75) & (S["logg_err"] < 0.25) & np.isfinite(S["logg"]))
    if s2: keep &= ~np.isin(S["i"], S2LIST)
    v = [p[0] for p in PMB]; sg = [p[1] for p in PMB]
    bt = (v[0], v[1], v[2], v[2]); lo = tuple(x - y for x, y in zip(v, sg)) + (v[2] - sg[2],); hi = tuple(x + y for x, y in zip(v, sg)) + (v[2] + sg[2],)
    bvars = [(lo, hi)] * 3 + [((v[0], v[1], v[2], 0.2), (v[0], v[1], v[2], 0.8))]
    return dict(keep=keep, esc=SX, bt=bt, bvars=bvars, F=True, tag="C" if s2 else "C without S2")
def opt_noC():
    return dict(keep=np.ones(len(S["r"]), bool), esc=1.0, bt=(BETA,) * 4, bvars=[((x,) * 4, (y,) * 4) for x, y in BR], F=False, tag="no C (RAW1)")
OC, OC2, ON = opt_C(True), opt_C(False), opt_noC()

def f_bin(j, model, ft, a0m, ak, bt, opt, vel=None):
    m = opt["keep"] & (S["bin"] == j)
    v = (S["vgsr"] if vel is None else vel)[m]; e = S["verr"][m] * opt["esc"]
    P = predP(S["r"][m], S["sin2"][m], model, ft, a0m, ak, bt)
    return est_bin(v, e, P, S["b"][m], opt["F"])
def word(f, s): return "HOT" if f > 1 + 2 * s else ("COLD" if f < 1 - 2 * s else "PASS")
def a0mult(ft, std): return (A0EXACT[ft] if (std and ft) else 1.0)

def evaluate(ak, opt, std_a0, draws=None, avars=None):
    """rows per case: f, s_stat, s_beta, s_slope, s; words; pass fraction over draws."""
    out = {}
    for m, ft in CASES:
        k = CKEY(m, ft); a0m = a0mult(ft, std_a0); rows = []
        for j in range(4):
            f, ss = f_bin(j, m, ft, a0m, ak, opt["bt"], opt)
            lo, hi = opt["bvars"][j]
            sb = 0.0 if lo == hi else 0.5 * abs(f_bin(j, m, ft, a0m, ak, hi, opt)[0] - f_bin(j, m, ft, a0m, ak, lo, opt)[0])
            rows.append(dict(f=f, s_stat=ss, s_beta=sb, n=int(np.sum(opt["keep"] & (S["bin"] == j)))))
        pf = float("nan")
        if draws is not None:
            fd = np.array([[f_bin(j, m, ft, a0m, a, opt["bt"], opt)[0] for j in range(4)] for a in draws])
            for j in range(4): rows[j]["s_slope"] = float(np.std(fd[:, j]))
            s0 = np.array([math.hypot(x["s_stat"], x["s_beta"]) for x in rows])
            pf = float(np.mean(np.all(np.abs(fd - 1) <= 2 * s0[None, :], axis=1)))
        else:
            for j in range(4):
                a_lo, a_hi = avars
                rows[j]["s_slope"] = 0.5 * abs(f_bin(j, m, ft, a0m, a_hi, opt["bt"], opt)[0] - f_bin(j, m, ft, a0m, a_lo, opt["bt"], opt)[0])
        for x in rows:
            x["s"] = math.sqrt(x["s_stat"] ** 2 + x["s_beta"] ** 2 + x["s_slope"] ** 2); x["word"] = word(x["f"], x["s"])
        out[k] = dict(rows=rows, pass_frac=pf)
        _SC.clear()
    return out

def outer_of(ak): return ak[1] if isinstance(ak, tuple) else ak
def lane_word(c, ak):
    w = [x["word"] for x in c["rows"]]
    if outer_of(ak) <= 2 * PMB[2][0] + 0.5: return "NO VERDICT", f"outer slope {outer_of(ak):.2f} <= {2 * PMB[2][0] + 0.5:.3f} (Jeans integral not convergent)"
    if np.isfinite(c["pass_frac"]) and 0.16 <= c["pass_frac"] <= 0.84: return "NO VERDICT", f"row passes in {c['pass_frac']:.2f} of slope draws"
    if all(x == "PASS" for x in w): return "ROW 28 PASSES UNDER ONE CONVENTION", ""
    return "STILL FAILS", ", ".join(f"{BN[j]} {w[j]}" for j in range(4) if w[j] != "PASS")
def fmt_rows(rows): return "  ".join(f"{x['f']:.3f}+/-{x['s']:.3f} {x['word']:4s}" for x in rows)
def show(tag, res, ak):
    say(f"-- {tag}; profile {ak}")
    for m, ft in CASES:
        k = CKEY(m, ft); c = res[k]; lw = lane_word(c, ak)
        say(f"   {k:20s} {fmt_rows(c['rows'])}  pass frac {c['pass_frac']:.2f}  -> {lw[0]}{(' [' + lw[1] + ']') if lw[1] else ''}")
    say("   N per bin " + str([res['H']['rows'][j]['n'] for j in range(4)]) + "; s_slope (FW census can) " + ", ".join(f"{x['s_slope']:.3f}" for x in res["FW_census/canonical"]["rows"]) +
        "; s_beta " + ", ".join(f"{x['s_beta']:.3f}" for x in res["FW_census/canonical"]["rows"]) + "; s_stat " + ", ".join(f"{x['s_stat']:.3f}" for x in res["FW_census/canonical"]["rows"]))

# ================================================================== KA4 SI, KA1 RRL1 reproduced
sec("Known answers")
g30 = float(MOD.g_model(30.0, "FW_census", "canonical")); Msi = g30 * (30 * 3.0857e19) ** 2 / 6.674e-11 / 1.989e30
check("KA4 SI M = g r^2 / G at 30 kpc", abs(Msi / float(MOD.M_of_g(g30, 30.0)) - 1) < 1e-9, f"g {g30:.4e} m/s^2, M {Msi:.4e} Msun")
NOMFIT = run_fit(NOMC); bF = NOMFIT["broken"]
check("KA1a full-sky broken fit = RRL1", abs(bF["ain"] - 5.293) < 0.005 and abs(bF["aout"] - 3.934) < 0.005 and abs(bF["rb"] - 39.0) < 0.1, fmt_b(bF))
akF = (bF["ain"], bF["aout"], bF["rb"])
JR = json.load(open(os.path.join(RRL1, "rrl1_results.json")))
KA1 = evaluate(akF, ON, False, draws=draws_of(NOMFIT, True, 200, np.random.default_rng(777)))
for m, ft in CASES:
    k = CKEY(m, ft); ref = JR["second_step"][k]["rows"]
    df = max(abs(a["f"] - b["f"]) for a, b in zip(KA1[k]["rows"], ref)); ds = max(abs(a["s"] - b["s"]) for a, b in zip(KA1[k]["rows"], ref))
    check(f"KA1 RRL1 row {k}", df < 5e-4 and ds < 2e-3, fmt_rows(KA1[k]["rows"]) + f" (max diff f {df:.1e}, s {ds:.1e})")
say(f"  KA1 FW census 40-55: canonical {KA1['FW_census/canonical']['rows'][2]['f']:.3f}, alt {KA1['FW_census/alt']['rows'][2]['f']:.3f} (RRL1 0.857 / 0.820)")
# KA2 MWT1 C with RAW1's slope
KA2 = evaluate(a_raw, OC, False, avars=(a_raw - sa_raw, a_raw + sa_raw))
for k in ("FW_census/canonical", "FW_census/alt", "FW_rc/canonical", "FW_rc/alt", "H"):
    ref = JM["combination"]["C"][k]
    df = max(abs(a["f"] - b["f"]) for a, b in zip(KA2[k]["rows"], ref)); ds = max(abs(a["s"] - b["s"]) for a, b in zip(KA2[k]["rows"], ref))
    check(f"KA2 MWT1 C row {k}", df < 5e-4 and ds < 5e-4, fmt_rows(KA2[k]["rows"]) + f" (max diff f {df:.1e}, s {ds:.1e})")
say(f"  KA2 FW census canonical 40-55 under C: {KA2['FW_census/canonical']['rows'][2]['f']:.4f} (MWT1 1.164)")
# own cells
OWNCELLS = np.zeros(NCELL, bool); OWNCELLS[np.unique(cell_of(D["ra"][S["i"]], D["dec"][S["i"]]))] = True
nown = int((footprint("ps1", 0.8, 20.0, 15.0)["keep"] & OWNCELLS).sum())
check("KA5 own-cell count in [1000, 1100]", 1000 <= nown <= 1100, f"{nown} kept cells of {int(OWNCELLS.sum())} holding sample stars; {nown * 4 * math.pi * (180 / math.pi) ** 2 / NCELL:.0f} deg^2")
CHK = run_fit(dict(NOMC, own=True, rlo=20.0, rhi=45.0, rbr=(25.0, 40.0)))
check("KA3 RRL1 same-profile check reproduced", CHK["N"] == 996 and abs(CHK["single"]["a"] - 5.139) < 0.005, f"N {CHK['N']}, single {fmt_s(CHK['single'])}; broken {fmt_b(CHK['broken'])}")
stop_if_failed()
say(f"  elapsed {time.time() - T0:.0f} s")

# ================================================================== own-cells density fit (the measurement of this lane)
sec("Own-cells PS1 RR Lyrae density, 20 <= r < 80 kpc, break in [22.5, 75]")
OWNC = dict(NOMC, own=True, rbr=(22.5, 75.0))
OWNFIT = run_fit(OWNC); sO, bO = OWNFIT["single"], OWNFIT["broken"]; Nown = OWNFIT["N"]; Wo = hist_w(OWNC, 1.0)
rng = np.random.default_rng(20261114)
LRo = []
for t in range(100):
    Xm = mock(OWNC, 1.0, (sO["a"],), Nown, rng); sm, bm = fit_both(Xm, Wo, OWNC["rbr"]); LRo.append(bm["LR"])
T_OWN = max(float(np.percentile(LRo, 99)), 6.63)
BRKO = bO["LR"] > T_OWN
say(f"  N {Nown}; single {fmt_s(sO)}")
say(f"  broken {fmt_b(bO)}")
say(f"  null 2 dlnL median {np.median(LRo):.2f}, 99th {np.percentile(LRo, 99):.2f}; T_own {T_OWN:.2f} -> break DETECTED {BRKO}; edge? {abs(bO['rb'] - 22.5) < 1.0 or abs(bO['rb'] - 75.0) < 1.0}")
say(f"  full-sky (RRL1) for comparison: N {NOMFIT['N']}; single {fmt_s(NOMFIT['single'])}; broken {fmt_b(bF)}")
akO = prof_of(OWNFIT, BRKO); akO_other = prof_of(OWNFIT, not BRKO)
say(f"  elapsed {time.time() - T0:.0f} s")

# ================================================================== primary and brackets
sec("Primary P: own-cells slope + C (standing a0); brackets B1-B4; reported rows")
RUNS = {}
def go(tag, fit, brk, opt, std, seed):
    ak = prof_of(fit, brk); dr = draws_of(fit, brk, 200, np.random.default_rng(seed))
    res = evaluate(ak, opt, std, draws=dr); RUNS[tag] = dict(ak=ak, res=res, opt=opt["tag"]); show(tag, res, ak)
    say(f"   elapsed {time.time() - T0:.0f} s")
go("P own-cells + C", OWNFIT, BRKO, OC, True, 2001)
go("B1 full-sky + C", NOMFIT, True, OC, True, 2002)
go("B2 own-cells, no C", OWNFIT, BRKO, ON, True, 2003)
go("B3 own-cells + C without S2", OWNFIT, BRKO, OC2, True, 2004)
go("B4 own-cells other model + C", OWNFIT, not BRKO, OC, True, 2005)
go("R1 full-sky + C without S2 (reported)", NOMFIT, True, OC2, True, 2006)
go("R2 P at RAW1-rounded a0 (reported)", OWNFIT, BRKO, OC, False, 2001)
go("R3 full-sky, no C, standing a0 (reported; = RRL1 at standing a0)", NOMFIT, True, ON, True, 777)

sec("WORDS (per case, per footing; FRAGILE if B1-B4 differ)")
WORDS = {}
for m, ft in CASES:
    k = CKEY(m, ft); w0 = lane_word(RUNS["P own-cells + C"]["res"][k], RUNS["P own-cells + C"]["ak"])
    br = {t: lane_word(RUNS[t]["res"][k], RUNS[t]["ak"])[0] for t in RUNS if t[:2] in ("B1", "B2", "B3", "B4")}
    flips = [t for t, w in br.items() if w != w0[0]]
    WORDS[k] = dict(word=w0[0], detail=w0[1], fragile=bool(flips), flips=flips, brackets=br)
    say(f"  {k:20s} {w0[0]}{(' [' + w0[1] + ']') if w0[1] else ''}{', FRAGILE (' + '; '.join(t + ' -> ' + br[t] for t in flips) + ')' if flips else ', robust'}")

# ================================================================== field diagnostic
sec("External field diagnostic (owner's actual-field reading; reported)")
for ft, eN in (("canonical", 0.000160), ("alt", 0.000110)):
    a0 = MOD.A0[ft] * A0EXACT[ft]
    parts = []
    for rr_ in (20.0, 55.0, 80.0):
        gb = float(MOD.g_model(rr_, "N")); y = gb / a0
        parts.append(f"{rr_:.0f} kpc y {y:.4f}: nu(sqrt(y^2+e^2))/nu(y) {float(MOD.nu_fw(math.hypot(y, eN)) / MOD.nu_fw(y)):.5f}")
    say(f"  {ft} e_N {eN}: " + "; ".join(parts))

# ================================================================== twins / mutations
MUT = open(os.path.join(HERE, f"rrl2{TAG}_MUTATE.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("RRL2 twins and mutations (FROZEN_CRITERIA.md section 7). Model FW census canonical, standing a0, primary profile, C.")
kP = "FW_census/canonical"; Prow = RUNS["P own-cells + C"]["res"][kP]["rows"]
sfix = [math.hypot(x["s_slope"], x["s_beta"]) for x in Prow]
Pall = predP(S["r"], S["sin2"], "FW_census", "canonical", A0EXACT["canonical"], akO, OC["bt"])
def twin(ftrue, seed):
    rg = np.random.default_rng(seed); vel = np.zeros(len(S["r"]))
    fv = np.array([ftrue[j] if j >= 0 else 1.0 for j in S["bin"]])
    vel = rg.normal(0.0, 1.0, len(S["r"])) * np.sqrt(fv ** 2 * Pall + (SX * S["verr"]) ** 2)
    ws = []
    for j in range(4):
        f, ss = f_bin(j, "FW_census", "canonical", A0EXACT["canonical"], akO, OC["bt"], OC, vel=vel)
        ws.append(word(f, math.hypot(ss, sfix[j])))
    return ws
TW = {}
for tag, ftrue, need in (("TW1 null (f = 1 everywhere)", (1, 1, 1, 1), None), ("MU1 f = 0.80 at 40-55", (1, 1, 0.80, 1), (2, "COLD")),
                         ("MU2 f = 1.25 at 30-40", (1, 1.25, 1, 1), (1, "HOT"))):
    W = [twin(ftrue, 9000 + s) for s in range(20)]
    if need is None:
        n = sum(all(w == "PASS" for w in ws) for ws in W); ok = n >= 12; det = f"row passes in {n} of 20 (need >= 12)"
    else:
        n = sum(ws[need[0]] == need[1] for ws in W); ok = n >= 15; det = f"{BN[need[0]]} {need[1]} in {n} of 20 (need >= 15)"
    TW[tag] = dict(n=n, ok=ok); msay(f"{tag}: {det}: {'PASS' if ok else 'FAIL'}")
_SC.clear()
MD = []
rgm = np.random.default_rng(424242)
for t in range(5):
    Xm = mock(OWNC, 1.0, akF, Nown, rgm); sm, bm = fit_both(Xm, Wo, OWNC["rbr"])
    det = bm["LR"] > T_OWN; rec = abs(bm["aout"] - akF[1]) <= 2 * bm["sout"]
    MD.append(dict(LR=bm["LR"], ain=bm["ain"], aout=bm["aout"], rb=bm["rb"], sout=bm["sout"], detected=bool(det), outer_ok=bool(rec)))
    msay(f"MD mock {t}: full-sky law on own cells, N {Nown}: {fmt_b(bm)}; detected {det}; outer within 2 sigma {rec}")
msay(f"MD: detected and outer recovered in {sum(x['detected'] and x['outer_ok'] for x in MD)} of 5")
msay("kappa = 1/2 FITTED; not theory closed. Adopts nothing."); MUT.close()

# ================================================================== S2 stars vs the RR Lyrae chain (diagnostic)
sec("S2 cold-group stars in 40-55 kpc and RRL1's RR Lyrae chain (RA 219-233, Dec -4 to -13, 49-56 kpc)")
m2 = np.isin(S["i"], S2LIST) & (S["bin"] == 2)
ra2, de2, r2 = D["ra"][S["i"][m2]], D["dec"][S["i"][m2]], S["r"][m2]
sepc = np.degrees(np.arccos(np.clip(unitv(ra2, de2) @ unitv(np.array([226.0]), np.array([-8.5]))[0], -1, 1)))
near = (sepc < 10.0) & (r2 >= 45) & (r2 <= 60)
say(f"  S2 stars in 40-55: {int(m2.sum())}; RA {np.min(ra2):.1f}-{np.max(ra2):.1f}, Dec {np.min(de2):.1f}-{np.max(de2):.1f}, r {np.min(r2):.1f}-{np.max(r2):.1f}; median (RA, Dec, r) ({np.median(ra2):.1f}, {np.median(de2):.1f}, {np.median(r2):.1f})")
say(f"  within 10 deg of (226, -8.5) and 45-60 kpc: {int(near.sum())}; nearest separation {np.min(sepc):.1f} deg")
chain_own = int(np.sum(OWNCELLS & angsep_mask(226.0, -8.5, 10.0))); say(f"  own cells within 10 deg of the chain centre: {chain_own}")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(dict(own_cells=nown, own_fit=dict(single=sO, broken=bO, N=Nown, T_own=T_OWN, null_LR=LRo, detected=BRKO),
                     fullsky_fit=dict(single=NOMFIT["single"], broken=bF), KA1={k: v["rows"] for k, v in KA1.items()}, KA2={k: v["rows"] for k, v in KA2.items()},
                     KA3=dict(single=CHK["single"], N=CHK["N"]), runs={t: dict(ak=v["ak"], opt=v["opt"], cases=v["res"]) for t, v in RUNS.items()},
                     words=WORDS, twins=TW, MD=MD, S2_chain=dict(n=int(m2.sum()), near=int(near.sum())))),
          open(os.path.join(HERE, f"rrl2{TAG}_results.json"), "w"), indent=1)
say(f"\nelapsed {time.time() - T0:.0f} s")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
