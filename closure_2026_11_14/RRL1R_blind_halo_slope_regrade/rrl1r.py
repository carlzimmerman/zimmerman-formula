#!/usr/bin/env python3
"""
RRL1R -- blind re-grade of RRL1: the stellar halo's number-density slope from RR Lyrae (PS1, Sesar+17; DES Y6
cross-check, Stringer+21) and RAW1's Jeans test redone with the measured profile.
Criteria: FROZEN_CRITERIA.md in this folder (committed alone before this script), which adopts RRL1's sections 0-8.
Usage: python3 -I -B rrl1r.py <PS1 table5_subset.tsv> <DES table1.tsv> <MWS_BHB.fits> <output folder>
Writes into <output folder>: rrl1r.out, rrl1r_results.json, rrl1r_MUTATE.out and mock checkpoint files (*.jsonl,
resumable). Paths are printed relative to the repository root.
Mine: table reader, sky grid, masks, clustering rule, completeness, normalisation, unbinned likelihood, single and
broken fits, Hessian errors, mocks, threshold T, draws, brackets, the Jeans integral for a general tracer profile,
labels. Reused read-only from RAW1 (raw1.py executed by AST as MWT1 did; raw1_model.py imported): load, build,
measure, fit_f, frame_affine, sgr_lat_lon, g_model.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_k] = "1"
import ast, json, math, hashlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.spatial import cKDTree
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RAW1 = os.path.join(ROOT, "closure_2026_11_12", "RAW1_halo_stars_direct")
PS1_PATH, DES_PATH, FITS, OUTDIR = sys.argv[1:5]
os.makedirs(OUTDIR, exist_ok=True)
rel = lambda p: os.path.relpath(os.path.abspath(p), ROOT)
SHA = dict(ps1="ab4b837f98157b4bdde82d09574ea8c62d8175580638bd46b2227df28031f813",
           des="94e3eb68aef19c94f4374ae1ab351b6552e0d3b7c1cb001622d2ddd77f898303",
           bhb="5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246")

OUT = open(os.path.join(OUTDIR, "rrl1r.out"), "w")
def say(s=""):
    print(s, flush=True); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say(""); say("=" * 110); say(t); say("=" * 110)
FAILED = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAILED.append(name)
def stop_if_failed():
    if FAILED:
        say("KNOWN-ANSWER CHECK FAILED: " + ", ".join(FAILED) + ". Stopping before any label."); OUT.close(); sys.exit(2)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()

# ------------------------------------------------------------------ RAW1's functions, read-only (as MWT1 did)
sys.path.insert(0, RAW1)
_src = open(os.path.join(RAW1, "raw1.py")).read()
_tree = ast.parse(_src)
_KEEP = ("K474", "BINS", "NOMINAL", "FOOT", "SG", "NGRID", "_GCACHE")
_body = [n for n in _tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
         or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in _KEEP)]
R1 = {"FITS": FITS, "HERE": RAW1, "__name__": "raw1_functions"}
exec(compile(ast.Module(body=_body, type_ignores=[]), "raw1.py", "exec"), R1)
MOD = R1["MOD"]; NOMINAL = R1["NOMINAL"]
KPC = 3.0857e19
CASES = [("FW_census", "canonical"), ("FW_census", "alt"), ("FW_rc", "canonical"), ("FW_rc", "alt"), ("H", None), ("N", None)]
CKEY = lambda m, f: f"{m}/{f}" if f else m
CK = [CKEY(m, f) for m, f in CASES]
FWK = CK[:4]
BN = ["20-30", "30-40", "40-55", "55-80"]

# ================================================================== my Jeans integral (general tracer profile)
SGM = np.logspace(0.0, math.log10(2.0e4), 6000)
def ln_n(s, prof):
    s = np.asarray(s, float)
    if prof[0] == "single": return -prof[1] * np.log(s / 40.0)
    _, ai, ao, rb = prof
    x = np.log(s / rb); return np.where(s < rb, -ai * x, -ao * x)
def sr2_of(r_eval, prof, beta, gfun):
    """sigma_r^2 in (km/s)^2 at r_eval [kpc]; gfun(s_kpc) -> m/s^2."""
    s = SGM if prof[0] == "single" else np.unique(np.append(SGM, prof[3]))
    x = np.log(s); lnw0 = ln_n(s, prof) + 2 * beta * x
    off = lnw0.max(); w0 = np.exp(lnw0 - off)
    w = w0 * gfun(s) * s * KPC                       # n s^2b g ds = n s^2b g s dln s, ds in m
    seg = 0.5 * (w[1:] + w[:-1]) * np.diff(x)
    cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    sr2 = cum / w0 / 1e6
    return np.exp(np.interp(np.log(r_eval), x, np.log(np.maximum(sr2, 1e-300))))
def gmod(model, footing):
    return lambda s: MOD.g_model(s, model, footing)

# ================================================================== K3a, K4 (no data)
sec("RRL1R known answers without data: K3a (my Jeans, analytic), K4 (SI)")
say(f"  RAW1 files read-only: raw1.py sha256 {sha(os.path.join(RAW1, 'raw1.py'))[:16]}..., raw1_model.py {sha(os.path.join(RAW1, 'raw1_model.py'))[:16]}...")
V = 200e3; flat = lambda s: V ** 2 / (np.asarray(s, float) * KPC)
rr = np.array([20.0, 30.0, 40.0, 60.0, 80.0]); worst = 0.0
for a, b in ((4.5, 0.5), (3.5, 0.0), (5.289, 0.6586)):
    got = sr2_of(rr, ("single", a), b, flat); ex = (V / 1e3) ** 2 / (a - 2 * b); worst = max(worst, float(np.max(np.abs(got / ex - 1))))
ai, ao, rbk, b = 3.0, 5.0, 35.0, 0.6586
def broken_flat_exact(r):
    V2 = (V / 1e3) ** 2; outer = V2 * rbk ** (2 * b) / (ao - 2 * b)
    if r >= rbk: return V2 / (ao - 2 * b)
    c = 2 * b - ai; inner = V2 * rbk ** ai * (rbk ** c - r ** c) / c
    return (inner + outer) / ((r / rbk) ** (-ai) * r ** (2 * b))
got = sr2_of(rr, ("broken", ai, ao, rbk), b, flat); ex = np.array([broken_flat_exact(x) for x in rr])
worst2 = float(np.max(np.abs(got / ex - 1)))
check("K3a single law, flat curve: sigma_r^2 = V^2 / (a - 2 beta)", worst < 1e-3, f"max relative difference {worst:.2e}")
check("K3a broken law (3 / 5 / 35), flat curve, exact", worst2 < 1e-3, f"max relative difference {worst2:.2e}; " + ", ".join(f"{g_:.1f}/{e_:.1f}" for g_, e_ in zip(got, ex)))
G_SI, MSUN_SI = 6.674e-11, 1.989e30
g30 = float(MOD.g_model(30.0, "FW_census", "canonical")); Msi = g30 * (30 * KPC) ** 2 / G_SI / MSUN_SI
check("K4 SI: M = g r^2 / G at 30 kpc (FW census canonical)", abs(Msi / float(MOD.M_of_g(g30, 30.0)) - 1) < 1e-9,
      f"g = {g30:.4e} m/s^2, M = {Msi:.4e} Msun, V = sqrt(g r) = {math.sqrt(g30 * 30 * KPC) / 1e3:.1f} km/s")
stop_if_failed()

# ================================================================== RAW1's sample (read-only) and K3
sec("RAW1's BHB sample (RAW1 load / build / measure, read-only) and K3")
check("BHB file sha256", sha(FITS) == SHA["bhb"], f"{rel(FITS)}")
stop_if_failed()
D = R1["load"](); CFG0 = dict(NOMINAL); S = R1["build"](D, CFG0); R = R1["measure"](S, CFG0)
J = json.load(open(os.path.join(RAW1, "raw1_results.json")))["nominal"]
say(f"  stars {len(S['r'])}, per bin {R['counts']}, beta {R['beta']:.4f} +/- {R['sbeta']:.4f}, per-bin beta ranges "
    f"{[(round(x, 4), round(y, 4)) for x, y in R['brange']]}; RAW1 alpha {R['alpha']['alpha']:.4f} +/- {R['alpha']['sig']:.4f}")
check("K3 sample counts", list(R["counts"]) == J["counts"] == [865, 264, 241, 125], f"{R['counts']}")
VG, VE, SR, SIN2 = S["vgsr"], S["verr"], S["r"], S["sin2"]
BSEL = R["bsel"]; BETA = R["beta"]; BRANGE = R["brange"]
fit_f = R1["fit_f"]

def f_bins(prof, model, ft, beta):
    s2 = sr2_of(SR, prof, beta, gmod(model, ft)); out = []
    for m in BSEL:
        out.append(fit_f(VG[m], VE[m], s2[m] * (1.0 - beta * SIN2[m])))
    return out
def f_case(prof, model, ft):
    """nominal f, s_stat and s_beta per bin for a profile."""
    nom = f_bins(prof, model, ft, BETA)
    bv = sorted({x for br in BRANGE for x in br}); fb = {x: f_bins(prof, model, ft, x) for x in bv}
    rows = []
    for j, (f, s) in enumerate(nom):
        lo, hi = BRANGE[j]
        rows.append(dict(f=float(f), s_stat=float(s), s_beta=float(0.5 * abs(fb[hi][j][0] - fb[lo][j][0]))))
    return rows
def wordf(f, s): return "HOT" if f > 1 + 2 * s else ("COLD" if f < 1 - 2 * s else "PASS")

aR, saR = R["alpha"]["alpha"], R["alpha"]["sig"]; dmax_all = 0.0
for (m, ft), k in zip(CASES, CK):
    rows = f_case(("single", aR), m, ft)
    flo = f_bins(("single", aR - saR), m, ft, BETA); fhi = f_bins(("single", aR + saR), m, ft, BETA)
    dm = 0.0; txt = []
    for j, x in enumerate(rows):
        sal = 0.5 * abs(fhi[j][0] - flo[j][0]); s = math.sqrt(x["s_stat"] ** 2 + sal ** 2 + x["s_beta"] ** 2)
        dm = max(dm, abs(x["f"] - J["f"][k][j]["f"]), abs(s - J["f"][k][j]["s"])); txt.append(f"{x['f']:.4f}+/-{s:.4f}")
    dmax_all = max(dmax_all, dm)
    check(f"K3 RAW1 reproduced with my Jeans, {k}", dm < 5e-4, "  ".join(txt) + f" (max diff {dm:.1e})")
RAWWORD = {k: [wordf(x["f"], x["s"]) for x in J["f"][k]] for k in CK}
say("  RAW1's words per bin (from raw1_results.json): " + "; ".join(f"{k}: {RAWWORD[k]}" for k in CK))
stop_if_failed()

# ================================================================== RR Lyrae tables (my reader)
def read_tsv(path):
    with open(path) as fh:
        lines = [l.rstrip("\n") for l in fh if not l.startswith("#") and l.strip() != ""]
    names = lines[0].split("\t"); cols = {n: [] for n in names}
    for l in lines[3:]:
        parts = l.split("\t") + [""] * len(names)
        for n, p in zip(names, parts): cols[n].append(p.strip())
    return cols
def fl(col): return np.array([float(x) if x not in ("",) else np.nan for x in col])

sec("Inputs")
check("PS1 sha256", sha(PS1_PATH) == SHA["ps1"], rel(PS1_PATH))
check("DES sha256", sha(DES_PATH) == SHA["des"], rel(DES_PATH))
stop_if_failed()
T5 = read_tsv(PS1_PATH)
P_ra, P_dec, P_s3ab, P_dm, P_ebv = fl(T5["RAJ2000"]), fl(T5["DEJ2000"]), fl(T5["S3ab"]), fl(T5["DM"]), fl(T5["E(B-V)"])
T1d = read_tsv(DES_PATH)
D_ra, D_dec, D_mu, D_ag = fl(T1d["RAJ2000"]), fl(T1d["DEJ2000"]), fl(T1d["mu"]), fl(T1d["Ag"])
D_acc = np.array([x == "True" for x in T1d["ACc"]]); D_sys = np.array([x != "" for x in T1d["Sys"]])
say(f"  PS1 rows {len(P_ra)}; finite RA/Dec {int(np.sum(np.isfinite(P_ra) & np.isfinite(P_dec)))}; finite S3ab, DM, E(B-V) "
    f"{int(np.sum(np.isfinite(P_s3ab) & np.isfinite(P_dm) & np.isfinite(P_ebv)))}")
say(f"  DES rows {len(D_ra)}; ACc True {int(D_acc.sum())}; non-empty Sys {int(D_sys.sum())}; kept {int(np.sum(~D_acc & ~D_sys))}")

# ================================================================== sky grid and geometry
NRA, NSD = 180, 90; NCELL = NRA * NSD; DOM_CELL = 4 * math.pi / NCELL
P0, RM = R1["frame_affine"](NOMINAL["R0"], NOMINAL["zsun"])
def unitv(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T
def cell_of(ra, dec):
    i = np.floor(np.mod(ra, 360.0) / 2.0).astype(int) % NRA
    j = np.clip(np.floor((np.sin(np.radians(dec)) + 1.0) * NSD / 2.0).astype(int), 0, NSD - 1)
    return j * NRA + i
_ii, _jj = np.meshgrid(np.arange(NRA), np.arange(NSD)); _ii, _jj = _ii.ravel(), _jj.ravel()   # index = j*NRA + i
C_ra = 2.0 * _ii + 1.0; C_dec = np.degrees(np.arcsin(-1.0 + (2 * _jj + 1.0) / NSD))
from astropy.coordinates import SkyCoord
import astropy.units as u
_cg = SkyCoord(ra=C_ra * u.deg, dec=C_dec * u.deg, frame="icrs").galactic
C_l, C_b = _cg.l.deg, _cg.b.deg
C_bsgr = R1["sgr_lat_lon"](C_l, C_b)[1]
C_u = unitv(C_ra, C_dec)
SUB = []
for di in (0.5, 1.5):
    for qj in (0.5, 1.5):
        SUB.append((2.0 * _ii + di, np.degrees(np.arcsin(-1.0 + (2 * _jj + qj) / NSD))))
def angdist_mask(ra0, dec0, rad):
    c = unitv(np.array([ra0]), np.array([dec0]))[0]
    return np.degrees(np.arccos(np.clip(C_u @ c, -1, 1))) < rad
MC_MASK = angdist_mask(80.89, -69.76, 27.1) | angdist_mask(13.19, -72.83, 12.6) | angdist_mask(39.997, -34.449, 2.0) | angdist_mask(15.039, -33.709, 1.0)
def chord(deg): return 2.0 * math.sin(math.radians(deg) / 2.0)

def clumps(ra, dec, dm):
    """frozen clustering rule; returns clump-star boolean and the cell mask (within 1.5 deg of a clump star)."""
    uv = unitv(ra, dec); tr = cKDTree(uv); nb = tr.query_ball_point(uv, chord(0.5))
    is_c = np.zeros(len(ra), bool)
    for k, lst in enumerate(nb):
        if len(lst) >= 5:
            lst = np.asarray(lst); is_c[k] = int(np.sum(np.abs(dm[lst] - dm[k]) < 0.25)) - 1 >= 4
    cmask = np.zeros(NCELL, bool); groups = []
    if is_c.any():
        cu = uv[is_c]; tc = cKDTree(cu)
        hit = tc.query_ball_point(C_u, chord(1.5)); cmask = np.array([len(h) > 0 for h in hit])
        # friends-of-friends groups, 1.5 deg linking
        par = list(range(len(cu)))
        def fnd(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a_, b_ in sorted(tc.query_pairs(chord(1.5))):
            ra_, rb_ = fnd(a_), fnd(b_)
            if ra_ != rb_: par[max(ra_, rb_)] = min(ra_, rb_)
        roots = np.array([fnd(x) for x in range(len(cu))]); cra, cdec, cdm = ra[is_c], dec[is_c], dm[is_c]
        for rt in np.unique(roots):
            mm = roots == rt; v = cu[mm].mean(axis=0); v /= np.linalg.norm(v)
            groups.append((float(np.degrees(np.arctan2(v[1], v[0])) % 360), float(np.degrees(np.arcsin(v[2]))), float(np.median(cdm[mm])), int(mm.sum())))
        groups.sort(key=lambda g: -g[3])
    return is_c, cmask, groups

def cell_median(cell, val):
    out = np.full(NCELL, np.nan); ok = np.isfinite(val); c, v = cell[ok], val[ok]
    o = np.argsort(c, kind="stable"); c, v = c[o], v[o]
    uc, st = np.unique(c, return_index=True); en = np.append(st[1:], len(c))
    for a_, s_, e_ in zip(uc, st, en): out[a_] = np.median(v[s_:e_])
    return out

P_cell = cell_of(P_ra, P_dec)
P_cnt = np.bincount(P_cell[np.isfinite(P_ra) & np.isfinite(P_dec)], minlength=NCELL)
P_ebv_med = cell_median(P_cell, P_ebv)
D_cell = cell_of(D_ra, D_dec)
D_cnt = np.bincount(D_cell, minlength=NCELL)
D_ag_med = cell_median(D_cell, D_ag)
def neighbours_hold(cnt):
    has = (cnt > 0).reshape(NSD, NRA); tot = np.zeros((NSD, NRA), int)
    for dj in (-1, 0, 1):
        for di in (-1, 0, 1):
            if dj == 0 and di == 0: continue
            sh = np.roll(has, -di, axis=1).astype(int)          # wrap in RA
            if dj == 1: sh = np.vstack([sh[1:], np.zeros((1, NRA), int)])
            elif dj == -1: sh = np.vstack([np.zeros((1, NRA), int), sh[:-1]])
            tot += sh
    return tot.ravel()
D_cov = (D_cnt > 0) | (neighbours_hold(D_cnt) >= 5)

# ------------------------------------------------------------------ one sample: masks, stars, normalisation
NB_NORM = 4000
def completeness(dm_obs, comp):
    if comp == "none": return np.ones_like(dm_obs)
    x0 = 20.57 if comp == "nominal" else 20.07
    return 1.0 / (1.0 + np.exp(4.1 * (dm_obs + 0.6 - x0)))

def build_sample(survey="PS1", score=0.8, comp="nominal", bcut=20.0, sgr=15.0, dscale=1.0, q=1.0, rlo=20.0, rhi=None,
                 only_cells=None, verbose=True):
    if rhi is None: rhi = 80.0 if survey == "PS1" else 100.0
    if survey == "PS1":
        ok = np.isfinite(P_ra) & np.isfinite(P_dec) & np.isfinite(P_s3ab) & np.isfinite(P_dm) & (P_s3ab > score)
        ra, dec, dm, cell = P_ra[ok], P_dec[ok], P_dm[ok], P_cell[ok]
        cov = (C_dec > -30.0) & (P_cnt > 0); red = P_ebv_med > 0.25
    else:
        ok = (~D_acc) & (~D_sys) & np.isfinite(D_mu)
        ra, dec, dm, cell = D_ra[ok], D_dec[ok], D_mu[ok], D_cell[ok]
        cov = D_cov.copy(); red = D_ag_med > 0.80; comp = "none"
    is_c, cmask, groups = clumps(ra, dec, dm)
    steps = [("covered", cov)]
    keep = cov.copy()
    keep &= np.abs(C_b) > bcut; steps.append((f"|b| > {bcut:g}", keep.copy()))
    keep &= ~(red == True); steps.append(("reddening", keep.copy()))
    if sgr is not None and sgr > 0: keep &= ~(np.abs(C_bsgr) < sgr)
    steps.append((f"Sgr band {sgr}", keep.copy()))
    keep &= ~MC_MASK; steps.append(("Magellanic / Fornax / Sculptor", keep.copy()))
    keep &= ~cmask; steps.append(("clump cells", keep.copy()))
    if only_cells is not None: keep &= only_cells; steps.append(("BHB cells only", keep.copy()))
    # stars
    d = dscale * 10 ** (dm / 5.0 + 1.0) / 1000.0
    uv = unitv(ra, dec) @ RM.T
    pos = P0 + d[:, None] * uv; r = np.linalg.norm(pos, axis=1)
    rq = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2 + (pos[:, 2] / q) ** 2)
    instar = keep[cell]
    sel = instar & (r >= rlo) & (r < rhi)
    # normalisation nodes
    kc = np.where(keep)[0]; lnrq_all = []; w_all = []
    t = np.linspace(0.0, 1.0, 120); tw = np.ones(120); tw[0] = tw[-1] = 0.5
    p2 = float(P0 @ P0)
    for sra, sdec in SUB:
        n = unitv(sra[kc], sdec[kc]) @ RM.T; pn = n @ P0
        root = lambda Rr: -pn + np.sqrt(pn ** 2 - p2 + Rr * Rr)
        lo, hi = np.log(root(rlo)), np.log(root(rhi)); dl = (hi - lo) / 119.0
        lnd = lo[:, None] + (hi - lo)[:, None] * t[None, :]; dd = np.exp(lnd)
        z = P0[2] + dd * n[:, 2:3]; r2 = dd ** 2 + 2 * dd * pn[:, None] + p2
        rqn = np.sqrt(np.maximum(r2 - z ** 2 + (z / q) ** 2, 1e-12))
        dmobs = 5.0 * np.log10(dd / dscale * 100.0)
        w = completeness(dmobs, comp) * dd ** 3 * dl[:, None] * tw[None, :] * (DOM_CELL / 4.0)
        lnrq_all.append(np.log(rqn).ravel()); w_all.append(w.ravel())
    lnrq_all = np.concatenate(lnrq_all); w_all = np.concatenate(w_all)
    e0, e1 = lnrq_all.min() - 1e-9, lnrq_all.max() + 1e-9; edges = np.linspace(e0, e1, NB_NORM + 1)
    k = np.clip(((lnrq_all - e0) / (e1 - e0) * NB_NORM).astype(int), 0, NB_NORM - 1)
    W = np.bincount(k, weights=w_all, minlength=NB_NORM); L = np.bincount(k, weights=w_all * lnrq_all, minlength=NB_NORM)
    nz = W > 0
    smp = dict(survey=survey, cfg=dict(score=score, comp=comp, bcut=bcut, sgr=sgr, dscale=dscale, q=q, rlo=rlo, rhi=rhi),
               keep=keep, ncell=int(keep.sum()), steps=[(s_, int(m_.sum())) for s_, m_ in steps],
               nclump=int(is_c.sum()), nclumpcells=int((cmask & cov).sum()), groups=groups,
               lnW=np.log(W[nz]), lnrk=L[nz] / W[nz], Wk=W[nz], edges_lo=edges[:-1][nz], width=float(edges[1] - edges[0]),
               nodes=(lnrq_all, w_all), r=r[sel], rq=rq[sel], dm=dm[sel], ra=ra[sel], dec=dec[sel],
               allsel=instar, all_dm=dm, all_uv=uv, rlo=rlo, rhi=rhi)
    set_data(smp, np.log(rq[sel]))
    if verbose:
        say(f"  [{survey}] cfg {smp['cfg']}: cells " + ", ".join(f"{s_} {n_}" for s_, n_ in smp["steps"]) +
            f"; clump stars {smp['nclump']}, clump-masked covered cells {smp['nclumpcells']}; stars in kept cells (all r) {int(instar.sum())}; in r range N = {smp['N']}")
    return smp

def set_data(smp, lnr):
    s = np.sort(lnr); smp["lnr_s"] = s; smp["cum"] = np.concatenate([[0.0], np.cumsum(s)]); smp["N"] = int(len(s))
def lnZ(smp, prof): return float(logsumexp(smp["lnW"] + ln_n(np.exp(smp["lnrk"]), prof)))
def lnZ_exact(smp, prof):
    lr, w = smp["nodes"]; return float(logsumexp(np.log(w) + ln_n(np.exp(lr), prof)))
L40 = math.log(40.0)
def nll(smp, prof):
    N = smp["N"]
    if prof[0] == "single":
        a = prof[1]; sdata = -a * (smp["cum"][-1] - N * L40)
    else:
        _, ai, ao, rb = prof; lrb = math.log(rb); k = int(np.searchsorted(smp["lnr_s"], lrb))
        sdata = -ai * (smp["cum"][k] - k * lrb) - ao * (smp["cum"][-1] - smp["cum"][k] - (N - k) * lrb)
    return -sdata + N * lnZ(smp, prof)

# ------------------------------------------------------------------ fits
def fit_single(smp):
    f = lambda a: nll(smp, ("single", a))
    res = minimize_scalar(f, bounds=(0.0, 10.0), method="bounded", options=dict(xatol=1e-7))
    ab, nb = float(res.x), float(res.fun)
    def side(dr):
        step = 0.01; x = ab
        for _ in range(300):
            xn = x + dr * step
            if xn < 0 or xn > 10: return 0.0 if dr < 0 else 10.0
            if f(xn) - nb > 0.5: return brentq(lambda tt: f(tt) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-7)
            x = xn; step *= 1.3
        return 0.0 if dr < 0 else 10.0
    h = 0.01; H = (f(ab + h) - 2 * nb + f(ab - h)) / h ** 2
    sig = 1.0 / math.sqrt(H) if H > 0 else float("nan")
    return dict(a=ab, nll=nb, sig=sig, lo=side(-1), hi=side(+1))

def hess(f, p, hs):
    k = len(p); H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            ei = np.zeros(k); ej = np.zeros(k); ei[i] = hs[i]; ej[j] = hs[j]
            H[i, j] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * hs[i] * hs[j])
    return H
def fit_broken(smp, a0, rbr):
    lo_, hi_ = rbr; grid = np.arange(lo_, hi_ + 1e-9, 2.5); prof_g = []
    for rb in grid:
        g = lambda p: nll(smp, ("broken", p[0], p[1], rb))
        res = minimize(g, [a0, a0], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
        prof_g.append((float(rb), float(res.fun), res.x.copy()))
    jb = int(np.argmin([x[1] for x in prof_g])); rb0, _, p0 = prof_g[jb]
    f3 = lambda p: (nll(smp, ("broken", p[0], p[1], p[2])) if lo_ <= p[2] <= hi_ else np.inf)
    res = minimize(f3, [p0[0], p0[1], rb0], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=8000))
    p = res.x.copy(); nb = float(res.fun)
    if prof_g[jb][1] < nb: p = np.array([p0[0], p0[1], rb0]); nb = prof_g[jb][1]
    cov = None; how = "Hessian (0.02, 0.02, 1.0)"
    for mult in (1.0, 2.0):
        H = hess(f3, p, np.array([0.02, 0.02, 1.0]) * mult)
        if np.all(np.isfinite(H)):
            try:
                ev = np.linalg.eigvalsh(H)
                if np.all(ev > 0): cov = np.linalg.inv(H); how = f"Hessian steps x{mult:g}"; break
            except np.linalg.LinAlgError: pass
    if cov is None:
        g2 = lambda pp: nll(smp, ("broken", pp[0], pp[1], p[2])); H2 = hess(g2, p[:2], np.array([0.02, 0.02]))
        try: c2 = np.linalg.inv(H2)
        except np.linalg.LinAlgError: c2 = np.full((2, 2), np.nan)
        rbs = np.array([x[0] for x in prof_g]); dn = np.array([x[1] for x in prof_g]) - nb
        inside = rbs[dn <= 0.5]
        srb = max(0.5 * (inside.max() - inside.min()), 1.25) if len(inside) else 1.25
        cov = np.zeros((3, 3)); cov[:2, :2] = c2; cov[2, 2] = srb ** 2; how = "fallback: slopes Hessian at fixed rb, rb from the grid profile"
    err = np.sqrt(np.maximum(np.diag(cov), 0))
    return dict(ain=float(p[0]), aout=float(p[1]), rb=float(p[2]), nll=nb, cov=cov.tolist(), err=err.tolist(), how=how,
                grid=[(x[0], x[1] - nb) for x in prof_g])
def fit_both(smp, rbr):
    s1 = fit_single(smp); b1 = fit_broken(smp, s1["a"], rbr)
    return s1, b1, max(0.0, 2 * (s1["nll"] - b1["nll"]))

# ------------------------------------------------------------------ mocks
def draw_mock(smp, prof, rng):
    lp = smp["lnW"] + ln_n(np.exp(smp["lnrk"]), prof); p = np.exp(lp - lp.max()); p /= p.sum()
    k = rng.choice(len(p), size=smp["N"], p=p)
    return smp["edges_lo"][k] + rng.random(smp["N"]) * smp["width"]
def mock_set(name, smp, prof, base_seed, nmock, rbr):
    path = os.path.join(OUTDIR, f"mocks_{name}.jsonl"); done = {}
    if os.path.exists(path):
        for line in open(path):
            try: x = json.loads(line); done[x["i"]] = x
            except Exception: pass
    fh = open(path, "a")
    for i in range(nmock):
        if i in done: continue
        rng = np.random.default_rng([base_seed, i]); m = dict(smp); set_data(m, draw_mock(smp, prof, rng))
        s1, b1, tl = fit_both(m, rbr)
        x = dict(i=i, a=s1["a"], tdl=tl, ain=b1["ain"], aout=b1["aout"], rb=b1["rb"]); done[i] = x
        fh.write(json.dumps(x) + "\n"); fh.flush()
    fh.close()
    return [done[i] for i in range(nmock)]

# ================================================================== nominal PS1 fit, T, K0n, K1, K2
sec("PS1 nominal sample and fits (no label yet)")
RB_PS1, RB_DES = (25.0, 75.0), (25.0, 95.0)
NOM = build_sample("PS1")
say(f"  clump groups (RA, Dec, median DM, stars), largest first: " + "; ".join(f"({g[0]:.2f}, {g[1]:.2f}, {g[2]:.2f}, {g[3]})" for g in NOM["groups"]))
worstZ = 0.0
for pr in (("single", 3.0), ("single", 5.0), ("broken", 3.0, 5.0, 35.0)):
    worstZ = max(worstZ, abs(lnZ(NOM, pr) - lnZ_exact(NOM, pr)))
NOMq = build_sample("PS1", q=0.7, verbose=False)
worstZ = max(worstZ, abs(lnZ(NOMq, ("single", 4.5)) - lnZ_exact(NOMq, ("single", 4.5))))
check("K0n binned normalisation == full node sum", worstZ < 1e-5, f"max |Delta ln Z| {worstZ:.2e}")
stop_if_failed()
S1, B1, TDL = fit_both(NOM, RB_PS1)
say(f"  single: a = {S1['a']:.4f} +/- {S1['sig']:.4f} (Hessian); profile interval [{S1['lo']:.4f}, {S1['hi']:.4f}]")
say(f"  broken: a_in {B1['ain']:.4f} +/- {B1['err'][0]:.4f}, a_out {B1['aout']:.4f} +/- {B1['err'][1]:.4f}, rb {B1['rb']:.3f} +/- {B1['err'][2]:.3f} kpc ({B1['how']})")
say(f"  2 Delta ln L (broken vs single) = {TDL:.3f}")
say("  rb grid profile (rb, nll - min): " + ", ".join(f"{a_:.1f}:{b_:.2f}" for a_, b_ in B1["grid"]))

sec("Null mocks from the best single law (100, seed 141101) and the threshold T")
NULL = mock_set("null", NOM, ("single", S1["a"]), 141101, 100, RB_PS1)
tvals = np.array([x["tdl"] for x in NULL]); T99 = float(np.percentile(tvals, 99)); T = max(T99, 6.63)
say(f"  2 Delta ln L over null mocks: median {np.median(tvals):.3f}, 90th {np.percentile(tvals, 90):.3f}, 99th {T99:.3f}, max {tvals.max():.3f}; "
    f"T = {T:.3f}{' (floor 6.63)' if T99 < 6.63 else ''}; mock single slopes mean {np.mean([x['a'] for x in NULL]):.4f} sd {np.std([x['a'] for x in NULL]):.4f}")

sec("K1 and K2 (mocks with the nominal footprint, completeness and N)")
m1 = dict(NOM); set_data(m1, draw_mock(NOM, ("single", 4.5), np.random.default_rng(141102)))
k1s, k1b, k1t = fit_both(m1, RB_PS1)
check("K1 single 4.5 recovered", abs(k1s["a"] - 4.5) <= 2 * k1s["sig"], f"a = {k1s['a']:.4f} +/- {k1s['sig']:.4f}")
check("K1 no break", k1t <= T, f"2 Delta ln L {k1t:.3f} vs T {T:.3f}")
m2 = dict(NOM); set_data(m2, draw_mock(NOM, ("broken", 3.0, 5.0, 35.0), np.random.default_rng(141103)))
k2s, k2b, k2t = fit_both(m2, RB_PS1)
check("K2 break detected", k2t > T, f"2 Delta ln L {k2t:.3f} vs T {T:.3f}")
check("K2 a_in", abs(k2b["ain"] - 3.0) <= 2 * k2b["err"][0], f"{k2b['ain']:.4f} +/- {k2b['err'][0]:.4f}")
check("K2 a_out", abs(k2b["aout"] - 5.0) <= 2 * k2b["err"][1], f"{k2b['aout']:.4f} +/- {k2b['err'][1]:.4f}")
check("K2 rb", abs(k2b["rb"] - 35.0) <= max(2 * k2b["err"][2], 5.0), f"{k2b['rb']:.3f} +/- {k2b['err'][2]:.3f} ({k2b['how']})")
stop_if_failed()
say("  All known answers K0n, K1, K2, K3, K3a, K4 passed.")

# ================================================================== second step machinery
def prof_of(model, s1, b1):
    return ("single", s1["a"]) if model == "single" else ("broken", b1["ain"], b1["aout"], b1["rb"])
def draws_of(model, s1, b1, rng, n=200, rbr=RB_PS1):
    out = []
    if model == "single":
        for a in rng.normal(s1["a"], s1["sig"], n): out.append(("single", max(float(a), 0.0)))
    else:
        mu = np.array([b1["ain"], b1["aout"], b1["rb"]]); C = np.array(b1["cov"])
        for x in rng.multivariate_normal(mu, C, n, method="svd"):
            out.append(("broken", max(float(x[0]), 0.0), max(float(x[1]), 0.0), float(np.clip(x[2], rbr[0], rbr[1]))))
    return out
def second_step(prof, drs):
    res = {}
    for (m, ft), k in zip(CASES, CK):
        rows = f_case(prof, m, ft)
        fdr = np.array([f_bins(p, m, ft, BETA) for p in drs], float)   # (draw, bin, (f, s_stat))
        fd = fdr[:, :, 0]; ss3040 = fdr[:, 1, 1]
        sb = rows[1]["s_beta"]
        hot = fd[:, 1] > 1 + 2 * np.sqrt(ss3040 ** 2 + sb ** 2)
        for j, x in enumerate(rows):
            x["s_slope"] = float(np.std(fd[:, j])); x["s"] = math.sqrt(x["s_stat"] ** 2 + x["s_slope"] ** 2 + x["s_beta"] ** 2)
            x["word"] = wordf(x["f"], x["s"])
        res[k] = dict(rows=rows, hot_frac_3040=float(np.mean(hot)))
        res[k]["label"], res[k]["bins"] = label_of(k, rows, res[k]["hot_frac_3040"])
    return res
def label_of(k, rows, frac):
    if 0.16 <= frac <= 0.84: return "NO POWER", []
    words = [x["word"] for x in rows]
    turned = [[BN[j], w] for j, w in enumerate(words) if RAWWORD[k][j] == "PASS" and w != "PASS"]
    if turned: return "MEASURED SLOPE MAKES A PASSING BIN FAIL", turned
    if all(w == "PASS" for w in words): return "FAIL REMOVED BY THE MEASURED SLOPE", []
    return "FAIL SURVIVES THE MEASURED SLOPE", [[BN[j], w] for j, w in enumerate(words) if w != "PASS"]
def show_step(res, indent="  "):
    for k in CK:
        x = res[k]
        say(f"{indent}{k:20s} " + "  ".join(f"{r_['f']:.3f}+/-{r_['s']:.3f} {r_['word']:4s}" for r_ in x["rows"]) +
            f"  | HOT@30-40 in draws {x['hot_frac_3040']:.3f} -> {x['label']} {x['bins'] if x['bins'] else ''}")
def show_parts(res, indent="    "):
    for k in CK:
        say(f"{indent}{k:20s} (s_stat, s_slope, s_beta) " + "  ".join(f"({r_['s_stat']:.3f}, {r_['s_slope']:.3f}, {r_['s_beta']:.3f})" for r_ in res[k]["rows"]))

RESULTS = dict(nominal_fit=dict(single=S1, broken=B1, tdl=TDL, T=T, T99=T99, null_tdl=tvals.tolist(), N=NOM["N"], cells=NOM["ncell"],
                                steps=NOM["steps"], nclump=NOM["nclump"], groups=NOM["groups"]),
               K=dict(K1=dict(single=k1s, tdl=k1t), K2=dict(broken=k2b, tdl=k2t)), raw1_words=RAWWORD)

sec("Model choice and the second step (nominal)")
BREAK = TDL > T; MODEL = "broken" if BREAK else "single"
say(f"  Break detected: {BREAK} (2 Delta ln L {TDL:.3f} vs T {T:.3f}); profile used: {MODEL} = {prof_of(MODEL, S1, B1)}")
PROF = prof_of(MODEL, S1, B1)
NOMRES = second_step(PROF, draws_of(MODEL, S1, B1, np.random.default_rng(141107)))
say("  f +/- sigma_f and word per bin (20-30, 30-40, 40-55, 55-80):"); show_step(NOMRES); show_parts(NOMRES)
RESULTS["model"] = MODEL; RESULTS["break"] = bool(BREAK); RESULTS["nominal"] = NOMRES

sec("BHB-versus-RR Lyrae slope check (section 5): PS1 single fit on the cells holding RAW1's 1,495 stars, 20-45 kpc")
bcells = np.zeros(NCELL, bool); bcells[np.unique(cell_of(D["ra"][S["i"]], D["dec"][S["i"]]))] = True
BH = build_sample("PS1", only_cells=bcells, rhi=45.0)
bs = fit_single(BH); diff = bs["a"] - 5.289; lim = 2 * math.sqrt(bs["sig"] ** 2 + 0.169 ** 2)
say(f"  BHB cells {int(bcells.sum())}; kept {BH['ncell']}; N {BH['N']}; a = {bs['a']:.4f} +/- {bs['sig']:.4f}; RAW1 5.289 +/- 0.169; "
    f"difference {diff:+.3f}, limit {lim:.3f} -> {'CONSISTENT' if abs(diff) <= lim else 'NOT CONSISTENT'}")
RESULTS["bhb_check"] = dict(a=bs["a"], sig=bs["sig"], N=BH["N"], cells=BH["ncell"], diff=diff, lim=lim, consistent=bool(abs(diff) <= lim))

# ================================================================== brackets
sec("Brackets (section 7): each redoes the PS1 fit and the second step; T is the nominal one")
BRK = [("completeness none", dict(comp="none")), ("completeness steeper x0 20.07", dict(comp="steep")),
       ("score > 0.6", dict(score=0.6)), ("score > 0.9", dict(score=0.9)), ("|b| > 30", dict(bcut=30.0)),
       ("Sgr band none", dict(sgr=None)), ("Sgr band 10", dict(sgr=10.0)), ("Sgr band 20", dict(sgr=20.0)),
       ("distances x0.95", dict(dscale=0.95)), ("distances x1.05", dict(dscale=1.05)), ("q = 0.7", dict(q=0.7)),
       ("other model", None)]
RESULTS["brackets"] = {}
for bi, (name, kw) in enumerate(BRK):
    say(f"-- bracket {name}")
    if kw is None:
        smp = NOM; s1, b1, tl = S1, B1, TDL; mdl = "single" if MODEL == "broken" else "broken"
    else:
        smp = build_sample("PS1", **kw); s1, b1, tl = fit_both(smp, RB_PS1); mdl = MODEL
    say(f"   single a {s1['a']:.4f} +/- {s1['sig']:.4f}; broken a_in {b1['ain']:.4f} +/- {b1['err'][0]:.4f}, a_out {b1['aout']:.4f} +/- {b1['err'][1]:.4f}, "
        f"rb {b1['rb']:.3f} +/- {b1['err'][2]:.3f}; 2 Delta ln L {tl:.3f} (T {T:.3f}); model used {mdl}")
    rs = second_step(prof_of(mdl, s1, b1), draws_of(mdl, s1, b1, np.random.default_rng(141200 + bi)))
    show_step(rs, "   ")
    RESULTS["brackets"][name] = dict(single=s1, broken=b1, tdl=tl, model=mdl, N=smp["N"], res=rs)

sec("Labels (four framework cases graded per footing; H and N reported)")
LAB = {}
for k in CK:
    base = NOMRES[k]["label"]; diffb = {nm: RESULTS["brackets"][nm]["res"][k]["label"] for nm, _ in BRK if RESULTS["brackets"][nm]["res"][k]["label"] != base}
    LAB[k] = dict(label=base, bins=NOMRES[k]["bins"], fragile=bool(diffb), by=diffb)
    say(f"  {k:20s} {base} {NOMRES[k]['bins'] if NOMRES[k]['bins'] else ''}" + (f"  FRAGILE: {diffb}" if diffb else "  (robust to every bracket)") +
        ("" if k in FWK else "  [reported, not graded]"))
RESULTS["labels"] = LAB

# ================================================================== DES cross-check
sec("DES cross-check (reported, not graded)")
DS = build_sample("DES")
say(f"  clump groups: " + "; ".join(f"({g[0]:.2f}, {g[1]:.2f}, {g[2]:.2f}, {g[3]})" for g in DS["groups"]))
dS1, dB1, dT = fit_both(DS, RB_DES)
DNULL = mock_set("des_null", DS, ("single", dS1["a"]), 141108, 100, RB_DES)
dtv = np.array([x["tdl"] for x in DNULL]); dT99 = float(np.percentile(dtv, 99)); TD = max(dT99, 6.63)
dmodel = "broken" if dT > TD else "single"
say(f"  single a {dS1['a']:.4f} +/- {dS1['sig']:.4f}; broken a_in {dB1['ain']:.4f} +/- {dB1['err'][0]:.4f}, a_out {dB1['aout']:.4f} +/- {dB1['err'][1]:.4f}, "
    f"rb {dB1['rb']:.3f} +/- {dB1['err'][2]:.3f} ({dB1['how']}); 2 Delta ln L {dT:.3f}; T_DES {TD:.3f} (99th {dT99:.3f}); model {dmodel}")
DRES = second_step(prof_of(dmodel, dS1, dB1), draws_of(dmodel, dS1, dB1, np.random.default_rng(141109), rbr=RB_DES))
show_step(DRES)
RESULTS["des"] = dict(single=dS1, broken=dB1, tdl=dT, T=TD, model=dmodel, N=DS["N"], cells=DS["ncell"], steps=DS["steps"], res=DRES)

# ================================================================== twins
sec("Twins")
T1M = mock_set("T1", NOM, ("single", S1["a"]), 141104, 50, RB_PS1)
nex = int(np.sum([x["tdl"] > T for x in T1M]))
say(f"  T1: {nex} of 50 further null mocks exceed T (allowed at most 3) -> {'PASS' if nex <= 3 else 'FAIL'}")
rng = np.random.default_rng(141105)
alls = NOM["allsel"]; dmall = NOM["all_dm"][alls].copy(); uvall = NOM["all_uv"][alls]; dm_sh = rng.permutation(dmall)
dsh = 10 ** (dm_sh / 5.0 + 1.0) / 1000.0; posh = P0 + dsh[:, None] * uvall; rsh = np.linalg.norm(posh, axis=1)
msh = dict(NOM); set_data(msh, np.log(rsh[(rsh >= 20.0) & (rsh < 80.0)]))
t2s, t2b, t2t = fit_both(msh, RB_PS1)
say(f"  T2 (DM shuffled among {int(alls.sum())} stars): N {msh['N']}; single {t2s['a']:.4f}; broken {t2b['ain']:.3f}/{t2b['aout']:.3f}/{t2b['rb']:.2f}; "
    f"2 Delta ln L {t2t:.3f} vs T {T:.3f} -> {'PASS (no break)' if t2t <= T else 'FAIL (break beyond T)'}")
RESULTS["twins"] = dict(T1_exceed=nex, T1_tdl=[x["tdl"] for x in T1M], T2=dict(N=msh["N"], single=t2s, broken=t2b, tdl=t2t))

# ================================================================== mutations (separate file)
MUT = open(os.path.join(OUTDIR, "rrl1r_MUTATE.out"), "w")
def msay(s): print("[MUT] " + s, flush=True); MUT.write(s + "\n"); MUT.flush()
msay("RRL1R mutations (criteria FROZEN_CRITERIA.md). M1: keep a random 60% of PS1 stars with r > 40: break near 40 detected, outer slope steepens."
     " M2: n = r^-3.5 in the Jeans step: f must fall in every bin of every case.")
rng = np.random.default_rng(141106); rN = NOM["r"]; keepm = (rN <= 40.0) | (rng.random(len(rN)) < 0.6)
mm = dict(NOM); set_data(mm, np.log(rN[keepm]))
ms1, mb1, mt = fit_both(mm, RB_PS1)
okm1 = (mt > T) and (32.5 <= mb1["rb"] <= 47.5) and (mb1["aout"] > B1["aout"])
msay(f"M1: N {mm['N']}; 2 Delta ln L {mt:.3f} (T {T:.3f}); rb {mb1['rb']:.2f}; a_out {mb1['aout']:.3f} vs nominal broken {B1['aout']:.3f}; a_in {mb1['ain']:.3f} -> bites: {okm1}")
okm2 = True
for (m, ft), k in zip(CASES, CK):
    rows = f_bins(("single", 3.5), m, ft, BETA); fn = [x["f"] for x in NOMRES[k]["rows"]]
    fall = all(r_[0] < f0 for r_, f0 in zip(rows, fn)); okm2 &= fall
    msay(f"M2 {k:20s} " + "  ".join(f"{r_[0]:.3f} (nominal {f0:.3f})" for r_, f0 in zip(rows, fn)) + f" -> falls in every bin: {fall}")
msay(f"M2 bites: {okm2}")
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()
RESULTS["mutations"] = dict(M1=dict(N=mm["N"], tdl=mt, broken=mb1, single=ms1, bites=bool(okm1)), M2=dict(bites=bool(okm2)))

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
with open(os.path.join(OUTDIR, "rrl1r_results.json"), "w") as fh: json.dump(clean(RESULTS), fh, indent=1)
say(f"\nInputs: {rel(PS1_PATH)}, {rel(DES_PATH)}, {rel(FITS)}; outputs in {rel(OUTDIR)}")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
