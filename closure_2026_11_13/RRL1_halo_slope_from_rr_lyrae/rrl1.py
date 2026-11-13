#!/usr/bin/env python3
"""
RRL1 -- the stellar halo's number-density slope from RR Lyrae (PS1 Sesar+17; DES Y6 Stringer+21 as cross-check),
then RAW1's Jeans statistic redone in every bin with the measured slope.
Criteria: FROZEN_CRITERIA.md (commit 59ab8ca9fa, alone, before this script).
Usage: python3 -I -B rrl1.py <PS1 table5_subset.tsv> <DES table1.tsv> <MWS_BHB.fits>
Writes rrl1.out, rrl1_results.json; mutations to rrl1_MUTATE.out. Data paths are never printed.
RAW1's estimators are reused unchanged: raw1.py is parsed and only its import, constant and function-definition
statements are executed (method copied from closure_2026_11_13/MWT1_hot_bin_assumptions/mwt1.py, lines 41-50);
MWT1's generalised tracer / sr2_grid / predP are copied from mwt1.py lines 58-82 (constant beta used here).
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
TAG = os.environ.get("RRL1_TAG", "")
OUT = open(os.path.join(HERE, f"rrl1{TAG}.out"), "w")
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
    idx = np.where(fp["sel"])[0]; idx = idx[fp["keep"][cell_of(T["ra"][idx], T["dec"][idx])]]
    dm = T["dm"][idx] if dm_override is None else dm_override
    d = 10 ** (dm / 5.0 - 2.0) * cfg["dscale"]   # kpc
    r, z = galpos(T["ra"][idx], T["dec"][idx], d)
    ink = (r >= cfg["rlo"]) & (r < cfg["rhi"])
    return dict(idx=idx[ink], r=r[ink], z=z[ink], dm_all=T["dm"][idx], idx_all=idx)

HB = np.linspace(math.log(5.0), math.log(250.0), 6001); HC = 0.5 * (HB[1:] + HB[:-1])
_GR = {}
def grid(cfg):
    key = (cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"], cfg["comp"], cfg["dscale"], cfg["rlo"], cfg["rhi"])
    if key in _GR: return _GR[key]
    fp = footprint(cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"])
    cells = np.where(fp["keep"])[0]
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
    key = (cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"], cfg["comp"], cfg["dscale"], cfg["rlo"], cfg["rhi"], q)
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

# ================================================================== start
sec("RRL1: inputs")
for nm, p in (("ps1", PS1F), ("des", DESF), ("bhb", FITS)):
    check(f"sha256 {nm}", sha(p) == SHA[nm], f"{sha(p)[:16]}... ({os.path.basename(p)})")
stop_if_failed()
PS1 = load_ps1(); DES = load_des()
say(f"  PS1 rows {len(PS1['ra'])}; DES rows {len(DES['ra'])}")
check("row counts", len(PS1["ra"]) == 239044 and len(DES["ra"]) == 6971, "239,044 / 6,971 expected")
stop_if_failed()

NOMC = dict(survey="ps1", score=0.8, bcut=20.0, sgr=15.0, comp="paper", dscale=1.0, rlo=20.0, rhi=80.0, q=1.0, rbr=(25.0, 75.0))
DESC = dict(survey="des", score=None, bcut=20.0, sgr=15.0, comp="flat", dscale=1.0, rlo=20.0, rhi=100.0, q=1.0, rbr=(25.0, 95.0))

sec("Footprints")
for nm, cfg in (("PS1", NOMC), ("DES", DESC)):
    fp = footprint(cfg["survey"], cfg["score"], cfg["bcut"], cfg["sgr"])
    say(f"  {nm}: {fp['ncell']} cells, {fp['area']:.0f} deg^2; RRab passing the class cut {int(fp['sel'].sum())}; clump stars {fp['nclump']}, cells masked by the clump rule {fp['nmask']}")
    for c in fp["centres"]:
        if c[2] >= 5: say(f"     clump at RA {c[0]:.2f} Dec {c[1]:.2f}: {c[2]} stars, DM {c[3]:.2f} (d {10 ** (c[3] / 5 - 2):.1f} kpc)")

# ================================================================== known answers K1, K2 (mocks)
sec("K1 / K2 known answers on mocks (nominal PS1 footprint and completeness)")
NOMFIT = run_fit(NOMC)
Nd = NOMFIT["N"]; Wn = hist_w(NOMC, 1.0)
rng = np.random.default_rng(20261113)
Xk1 = mock(NOMC, 1.0, (4.5,), Nd, rng); s1, b1 = fit_both(Xk1, Wn)
check("K1 single slope 4.5 recovered", abs(s1["a"] - 4.5) <= 2 * s1["sig"], f"{fmt_s(s1)}")
Xk2 = mock(NOMC, 1.0, (3.0, 5.0, 35.0), Nd, rng); s2, b2 = fit_both(Xk2, Wn)
say(f"  K2 mock (3.0, 5.0, 35): single {fmt_s(s2)}; broken {fmt_b(b2)}")
K2ok = abs(b2["ain"] - 3.0) <= 2 * b2["sin"] and abs(b2["aout"] - 5.0) <= 2 * b2["sout"] and (abs(b2["rb"] - 35) <= max(2 * b2["srb"], 5.0))

# null mocks for the threshold
sec("Break threshold T: 100 null mocks from the best single law (nominal PS1)")
LRn = []
for k in range(100):
    Xm = mock(NOMC, 1.0, (NOMFIT["single"]["a"],), Nd, rng); sm, bm = fit_both(Xm, Wn); LRn.append(bm["LR"])
T_PS1 = max(float(np.percentile(LRn, 99)), 6.63)
say(f"  null 2 dlnL: median {np.median(LRn):.2f}, 95th {np.percentile(LRn, 95):.2f}, 99th {np.percentile(LRn, 99):.2f}; T = {T_PS1:.2f}")
check("K1 no break detected on the single-slope mock", b1["LR"] <= T_PS1, f"2 dlnL {b1['LR']:.2f} vs T {T_PS1:.2f}")
check("K2 break detected and recovered", b2["LR"] > T_PS1 and K2ok, f"{fmt_b(b2)}; T {T_PS1:.2f}")

# ================================================================== RAW1 reproduced (K3, K4)
sec("K3 / K4 RAW1 reproduced (RAW1's sample, beta, estimator; RAW1's single slope)")
D = R1["load"]()
cfgR = dict(NOMINAL); S = R1["build"](D, cfgR); R = R1["measure"](S, cfgR)
J = json.load(open(os.path.join(RAW1, "raw1_results.json")))["nominal"]
check("K3 counts", list(R["counts"]) == J["counts"] == [865, 264, 241, 125], f"{R['counts']}")
BETA = R["beta"]; BR = R["brange"]
rr = np.linspace(20, 80, 61); worst = 0.0
for model, ft in CASES:
    for a in (3.0, 5.289):
        worst = max(worst, float(np.max(np.abs(predP(rr, np.zeros_like(rr), model, ft, 1.0, a, (BETA,) * 4) / R1["sr2_at"](rr, model, a, BETA, ft, 1.0) - 1))))
check("K3a predP (copied from MWT1) == RAW1 sr2_at at constant beta", worst < 1e-6, f"max relative difference {worst:.2e}")

def f_one(model, ft, ak, beta_override=None):
    out = []
    for j, m in enumerate(R["bsel"]):
        v, e, r, s2 = S["vgsr"][m], S["verr"][m], S["r"][m], S["sin2"][m]
        b = BETA if beta_override is None else beta_override[j]
        out.append(R1["fit_f"](v, e, predP(r, s2, model, ft, 1.0, ak, (b,) * 4)))
    return out
def f_rows(model, ft, ak, s_slope=None, avars=None):
    nom = f_one(model, ft, ak)
    lo = f_one(model, ft, ak, [x[0] for x in BR]); hi = f_one(model, ft, ak, [x[1] for x in BR])
    rows = []
    for j in range(4):
        sb = 0.5 * abs(hi[j][0] - lo[j][0])
        if avars is not None:
            sa = 0.5 * abs(f_one(model, ft, avars[1])[j][0] - f_one(model, ft, avars[0])[j][0])
        else: sa = s_slope[j] if s_slope is not None else 0.0
        rows.append(dict(f=nom[j][0], s_stat=nom[j][1], s_beta=sb, s_slope=sa, s=math.sqrt(nom[j][1] ** 2 + sb * sb + sa * sa)))
    return rows
def word(x): return "HOT" if x["f"] > 1 + 2 * x["s"] else ("COLD" if x["f"] < 1 - 2 * x["s"] else "PASS")
def fmt_rows(rows): return "  ".join(f"{x['f']:.3f}+/-{x['s']:.3f} {word(x):4s}" for x in rows)

a_raw, sa_raw = R["alpha"]["alpha"], R["alpha"]["sig"]
RAWF = {}
for m, ft in CASES:
    k = CKEY(m, ft); rows = f_rows(m, ft, a_raw, avars=(a_raw - sa_raw, a_raw + sa_raw)); RAWF[k] = rows
    dmax = max(max(abs(a["f"] - b["f"]), abs(a["s"] - b["s"])) for a, b in zip(rows, J["f"][k]))
    check(f"K3 f {k}", dmax < 5e-4, fmt_rows(rows) + f" (max diff {dmax:.1e})")
g30 = float(MOD.g_model(30.0, "FW_census", "canonical")); Msi = g30 * (30 * 3.0857e19) ** 2 / 6.674e-11 / 1.989e30
check("K4 SI: M = g r^2 / G at 30 kpc (FW census canonical)", abs(Msi / float(MOD.M_of_g(g30, 30.0)) - 1) < 1e-9,
      f"g = {g30:.4e} m/s^2, M = {Msi:.4e} Msun, V = {math.sqrt(g30 * 30 * 3.0857e19) / 1e3:.1f} km/s")
stop_if_failed()
RAW_WORDS = {k: [word(x) for x in v] for k, v in RAWF.items()}

# ================================================================== the measurement
sec("PS1 RR Lyrae density, nominal (score > 0.8, |b| > 20, Sgr band 15, paper completeness, q = 1, 20 <= r < 80)")
s_, b_ = NOMFIT["single"], NOMFIT["broken"]
say(f"  N {NOMFIT['N']}; single {fmt_s(s_)}")
say(f"  broken {fmt_b(b_)}; T {T_PS1:.2f} -> break DETECTED: {b_['LR'] > T_PS1}")
BRK = b_["LR"] > T_PS1
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
def loc_slope(ak, r):
    if not isinstance(ak, tuple): return ak
    return ak[0] if r < ak[2] else ak[1]

def second_step(fit, broken, tag, seed, ndraw=200):
    ak = prof_of(fit, broken); rng = np.random.default_rng(seed)
    dr = draws_of(fit, broken, ndraw, rng)
    res = {}
    for m, ft in CASES:
        k = CKEY(m, ft)
        fd = np.array([[x[0] for x in f_one(m, ft, a)] for a in dr])
        s_sl = list(np.std(fd, axis=0))
        rows = f_rows(m, ft, ak, s_slope=s_sl)
        sig0 = math.sqrt(rows[1]["s_stat"] ** 2 + rows[1]["s_beta"] ** 2)
        hotfrac = float(np.mean(fd[:, 1] > 1 + 2 * sig0))
        res[k] = dict(rows=rows, hotfrac=hotfrac, words=[word(x) for x in rows], f16=list(np.percentile(fd, 16, axis=0)), f84=list(np.percentile(fd, 84, axis=0)))
        _SC.clear()
    return dict(ak=ak, cases=res, tag=tag)

def label(k, res):
    c = res["cases"][k]; w = c["words"]; rw = RAW_WORDS[k]
    if 0.16 <= c["hotfrac"] <= 0.84: return "NO POWER", f"hot fraction over draws {c['hotfrac']:.2f}"
    newfail = [f"{BN[j]} {w[j]}" for j in range(4) if rw[j] == "PASS" and w[j] != "PASS"]
    if newfail: return "MEASURED SLOPE MAKES A PASSING BIN FAIL", ", ".join(newfail)
    if all(x == "PASS" for x in w): return "FAIL REMOVED BY THE MEASURED SLOPE", ""
    return "FAIL SURVIVES THE MEASURED SLOPE", ", ".join(f"{BN[j]} {w[j]}" for j in range(4) if w[j] != "PASS")

sec("Second step: RAW1's f in every bin with the measured PS1 profile (nominal)")
NOM2 = second_step(NOMFIT, BRK, "nominal", 777)
say(f"  profile used: {'broken' if BRK else 'single'} {NOM2['ak']}; local slope at bin mid-radii: " +
    ", ".join(f"{BN[j]} {loc_slope(NOM2['ak'], m):.2f}" for j, m in enumerate((25, 35, 47.5, 67.5))))
LABELS = {}
for m, ft in CASES:
    k = CKEY(m, ft); c = NOM2["cases"][k]
    say(f"  {k:20s} RAW1 slope: {fmt_rows(RAWF[k])}")
    say(f"  {'':20s} RR Lyrae  : {fmt_rows(c['rows'])}   (30-40 HOT in {c['hotfrac']:.2f} of draws; s_slope " + ", ".join(f"{x['s_slope']:.3f}" for x in c["rows"]) + ")")
    if m.startswith("FW"):
        lab = label(k, NOM2); LABELS[k] = dict(label=lab[0], detail=lab[1])
        say(f"  {'':20s} -> {lab[0]} {lab[1]}")
    else: say(f"  {'':20s} -> words {c['words']} (comparator, no label)")

# ================================================================== brackets
sec("Brackets (each redoes the PS1 fit and the second step)")
BRACK = [("completeness none", dict(comp="none")), ("completeness steeper", dict(comp="steep")),
         ("score > 0.6", dict(score=0.6)), ("score > 0.9", dict(score=0.9)), ("|b| > 30", dict(bcut=30.0)),
         ("no Sgr band", dict(sgr=None)), ("Sgr band 10", dict(sgr=10.0)), ("Sgr band 20", dict(sgr=20.0)),
         ("distances x0.95", dict(dscale=0.95)), ("distances x1.05", dict(dscale=1.05)), ("q = 0.7", dict(q=0.7)),
         ("other model", {})]
BRES = {}
for j, (tag, ch) in enumerate(BRACK):
    cfg = dict(NOMC, **ch); fit = run_fit(cfg)
    brk = (not BRK) if tag == "other model" else BRK
    s2_ = second_step(fit, brk, tag, 900 + j)
    labs = {k: label(k, s2_)[0] for k in LABELS}
    BRES[tag] = dict(single=fit["single"], broken={k: v for k, v in fit["broken"].items() if k != "cov"}, N=fit["N"], model="broken" if brk else "single",
                     ak=s2_["ak"], f={k: [x["f"] for x in v["rows"]] for k, v in s2_["cases"].items()},
                     s={k: [x["s"] for x in v["rows"]] for k, v in s2_["cases"].items()}, words={k: v["words"] for k, v in s2_["cases"].items()}, labels=labs)
    say(f"  {tag:22s} N {fit['N']}: single {fit['single']['a']:.3f}+/-{fit['single']['sig']:.3f}; broken {fmt_b(fit['broken'])} (detected at T: {fit['broken']['LR'] > T_PS1}); used {BRES[tag]['model']}")
    for m, ft in CASES:
        k = CKEY(m, ft); c = s2_["cases"][k]
        say(f"     {k:20s} {fmt_rows(c['rows'])}" + (f"  -> {labs[k]}" if k in labs else ""))
    _GR.clear(); _HW.clear()
for k in LABELS:
    flips = [t for t, b in BRES.items() if b["labels"][k] != LABELS[k]["label"]]
    LABELS[k]["fragile"] = bool(flips); LABELS[k]["flips"] = flips

# ================================================================== DES cross-check
sec("DES Y6 cross-check (own footprint; 20 <= r < 100; flat completeness)")
DESFIT = run_fit(DESC); Wd = hist_w(DESC, 1.0)
LRd = []
for k in range(100):
    Xm = mock(DESC, 1.0, (DESFIT["single"]["a"],), DESFIT["N"], rng); sm, bm = fit_both(Xm, Wd, DESC["rbr"]); LRd.append(bm["LR"])
T_DES = max(float(np.percentile(LRd, 99)), 6.63)
DBRK = DESFIT["broken"]["LR"] > T_DES
say(f"  N {DESFIT['N']}; single {fmt_s(DESFIT['single'])}; broken {fmt_b(DESFIT['broken'])}; T_DES {T_DES:.2f} -> DETECTED {DBRK}")
DESX = {}
for tag, ch in (("q = 0.7", dict(q=0.7)), ("20-80 kpc", dict(rhi=80.0, rbr=(25.0, 75.0))), ("q = 0.7, 9-100 kpc (paper's range)", dict(q=0.7, rlo=9.0, rbr=(15.0, 90.0))),
                ("RF min >= 0.9", dict(score=0.9))):
    f_ = run_fit(dict(DESC, **ch)); DESX[tag] = dict(single=f_["single"], broken={k: v for k, v in f_["broken"].items() if k != "cov"})
    say(f"  {tag:36s} N {f_['N']}: single {fmt_s(f_['single'])}; broken {fmt_b(f_['broken'])}")
DES2 = second_step(DESFIT, DBRK, "DES", 555)
say(f"  RAW1's f with the DES profile ({'broken' if DBRK else 'single'} {DES2['ak']}), reported, not graded:")
for m, ft in CASES:
    k = CKEY(m, ft); say(f"     {k:20s} {fmt_rows(DES2['cases'][k]['rows'])}")

# ================================================================== same-profile check (BHB vs RR Lyrae)
sec("Same-profile check: PS1 RR Lyrae on the BHB sample's sky cells, 20-45 kpc, against RAW1's alpha")
bcells = np.zeros(NCELL, bool); bcells[np.unique(cell_of(D["ra"][S["i"]], D["dec"][S["i"]]))] = True
fp0 = footprint("ps1", 0.8, 20.0, 15.0); saved = fp0["keep"].copy()
fp0["keep"] = saved & bcells; _GR.clear(); _HW.clear()
CHK = run_fit(dict(NOMC, rlo=20.0, rhi=45.0, rbr=(25.0, 40.0)))
fp0["keep"] = saved; _GR.clear(); _HW.clear()
cs = CHK["single"]; dif = cs["a"] - a_raw; sc = math.hypot(cs["sig"], sa_raw)
say(f"  BHB cells in the PS1 footprint: {int((saved & bcells).sum())}; RR Lyrae N {CHK['N']}: single {fmt_s(cs)}; RAW1 BHB alpha {a_raw:.3f} +/- {sa_raw:.3f}")
say(f"  difference {dif:+.3f} +/- {sc:.3f} ({dif / sc:+.2f} sigma): {'CONSISTENT' if abs(dif) <= 2 * sc else 'INCONSISTENT'} (frozen 2 sigma); broken in this window: {fmt_b(CHK['broken'])}")
SAMECHK = dict(single=cs, raw_alpha=a_raw, raw_sig=sa_raw, nsig=dif / sc, consistent=abs(dif) <= 2 * sc)

# ================================================================== twins
sec("Twins")
LRt = []
for k in range(50):
    Xm = mock(NOMC, 1.0, (NOMFIT["single"]["a"],), Nd, np.random.default_rng(5000 + k)); sm, bm = fit_both(Xm, Wn); LRt.append(bm["LR"])
nex = int(np.sum(np.array(LRt) > T_PS1))
check("T1 null mocks (new seeds) exceeding T", nex <= 3, f"{nex} of 50 (allowed 3); median 2 dlnL {np.median(LRt):.2f}")
Sx = sample(NOMC); perm = np.random.default_rng(31).permutation(len(Sx["dm_all"]))
SHF = run_fit(NOMC, dm_override=Sx["dm_all"][perm])
check("T2 distances shuffled among stars: no break beyond T", SHF["broken"]["LR"] <= T_PS1,
      f"N {SHF['N']}: single {fmt_s(SHF['single'])}; broken {fmt_b(SHF['broken'])} (expectation frozen: a break in d largely survives)")

# ================================================================== mutations (separate file)
MUT = open(os.path.join(HERE, f"rrl1{TAG}_MUTATE.out"), "w")
def msay(s): print("[MUT] " + s); MUT.write(s + "\n"); MUT.flush()
msay("RRL1 mutations (criteria FROZEN_CRITERIA.md section 8).")
mr = np.random.default_rng(41)
M1 = run_fit(NOMC, thin=lambda Sx_: (Sx_["r"] <= 40.0) | (mr.random(len(Sx_["r"])) < 0.6))
b1m = M1["broken"]; a_ref = b_["aout"] if BRK else s_["a"]
bites1 = b1m["LR"] > T_PS1 and b1m["aout"] > a_ref and abs(b1m["rb"] - 40.0) <= 10.0
msay(f"M1 keep 60% beyond 40 kpc: N {M1['N']}; single {fmt_s(M1['single'])}; broken {fmt_b(M1['broken'])}; outer vs nominal {a_ref:.3f}; bites: {bites1}")
m2 = []
for m, ft in CASES:
    k = CKEY(m, ft); fr = [x[0] for x in f_one(m, ft, 3.5)]; fn = [x["f"] for x in NOM2["cases"][k]["rows"]]
    m2.append(all(a < b for a, b in zip(fr, fn)) or all(a < b for a, b in zip(fr, [x["f"] for x in RAWF[k]])))
    msay(f"M2 n = r^-3.5 {k:20s} " + "  ".join(f"{a:.3f}" for a in fr) + f"  (measured: " + "  ".join(f"{b:.3f}" for b in fn) + ")")
msay(f"M2 bites (f falls in every bin against RAW1's slope or the measured one, every case): {all(m2)}")
msay("kappa = 1/2 FITTED; not theory closed. Adopts nothing."); MUT.close()

# ================================================================== labels
sec("LABELS (as frozen; four framework cases; H and N reported with words)")
for k, v in LABELS.items():
    say(f"  {k:20s} {v['label']}{(' [' + v['detail'] + ']') if v['detail'] else ''}{', FRAGILE (' + '; '.join(v['flips']) + ')' if v['fragile'] else ', robust'}")
for k in ("H", "N"):
    say(f"  {k:20s} words {NOM2['cases'][k]['words']} (RAW1 {RAW_WORDS[k]})")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
strip = lambda f: dict(single=f["single"], broken={k: v for k, v in f["broken"].items()}, N=f["N"])
json.dump(clean(dict(T_PS1=T_PS1, T_DES=T_DES, null_LR=LRn, ps1_nominal=strip(NOMFIT), break_detected=BRK,
                     second_step={k: dict(rows=v["rows"], words=v["words"], hotfrac=v["hotfrac"]) for k, v in NOM2["cases"].items()},
                     profile_used=NOM2["ak"], raw1_repro={k: v for k, v in RAWF.items()}, labels=LABELS, brackets=BRES,
                     des_nominal=strip(DESFIT), des_detected=DBRK, des_brackets=DESX,
                     des_second_step={k: v["rows"] for k, v in DES2["cases"].items()}, same_profile_check=SAMECHK,
                     K1=dict(single=s1, LR=b1["LR"]), K2=dict(single=s2, broken={k: v for k, v in b2.items()}),
                     T1=dict(n_exceed=nex, LR=LRt), T2=strip(SHF))),
          open(os.path.join(HERE, f"rrl1{TAG}_results.json"), "w"), indent=1)
say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
