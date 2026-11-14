#!/usr/bin/env python3
"""
RRL3R -- blind lane: Milky Way halo stars (DESI DR1 BHB, RAW1's sample and bins) graded under ONE frozen convention:
the star-count profile measured on the full sky from PS1 RR Lyrae, and MWT1's kinematic corrections C (L logg cut,
S2 cold-group mask, X error scale, B measured anisotropy profile, F equal-hemisphere weight).
Criteria: FROZEN_CRITERIA.md in this folder (committed alone before this script).

Usage:  python3 -I -B rrl3r.py <PS1 table5_subset.tsv> <DES table1.tsv> <MWS_BHB.fits>
Writes, next to this script: rrl3r.out, rrl3r_results.json, rrl3r_MUTATE.out, and mock checkpoints mocks_*.jsonl
(resumable).

Mine: the variable-anisotropy Jeans integral, the per-bin anisotropy measurement, the estimator (with the F weight),
the sigma_f parts, twins and mutations, brackets, words.
Copied with citation from closure_2026_11_14/RRL1R_blind_halo_slope_regrade/rrl1r.py (allowed by the brief): the
RR Lyrae table reader, sky grid, masks, clustering rule, completeness, normalisation, unbinned likelihood, single and
broken fits, Hessian, mocks and profile draws (marked "[rrl1r copy]").
Read-only from RAW1 (closure_2026_11_12/RAW1_halo_stars_direct): raw1.py executed by AST for load, build, measure
(measure only for KA-1 and as a cross-check of my betas), frame_affine, sgr_lat_lon; raw1_model.py imported (g_model).
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_k] = "1"
import ast, json, math, hashlib, warnings, time
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.spatial import cKDTree
from scipy.special import logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RAW1 = os.path.join(ROOT, "closure_2026_11_12", "RAW1_halo_stars_direct")
PS1_PATH, DES_PATH, FITS = sys.argv[1:4]
rel = lambda p: os.path.relpath(os.path.abspath(p), ROOT)
SHA = dict(ps1="ab4b837f98157b4bdde82d09574ea8c62d8175580638bd46b2227df28031f813",
           des="94e3eb68aef19c94f4374ae1ab351b6552e0d3b7c1cb001622d2ddd77f898303",
           bhb="5669c8212bf122d20f681ee15d5de1a61d0a4e7d8d2cc8b061211b3317115246")
T0 = time.time()
OUT = open(os.path.join(HERE, "rrl3r.out"), "w")
def say(s=""):
    print(s, flush=True); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say(""); say("=" * 110); say(f"{t}   [t = {time.time() - T0:.0f} s]"); say("=" * 110)
FAILED = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAILED.append(name)
def stop_if_failed():
    if FAILED:
        say("KNOWN-ANSWER CHECK FAILED: " + ", ".join(FAILED) + ". Every case: NO VERDICT (KNOWN ANSWER). Stopping before any word.")
        OUT.close(); sys.exit(2)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""): h.update(blk)
    return h.hexdigest()

# ------------------------------------------------------------------ RAW1's functions, read-only (as MWT1 and RRL1R did)
sys.path.insert(0, RAW1)
_tree = ast.parse(open(os.path.join(RAW1, "raw1.py")).read())
_KEEP = ("K474", "BINS", "NOMINAL", "FOOT", "SG", "NGRID", "_GCACHE")
_body = [n for n in _tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
         or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in _KEEP)]
R1 = {"FITS": FITS, "HERE": RAW1, "__name__": "raw1_functions"}
exec(compile(ast.Module(body=_body, type_ignores=[]), "raw1.py", "exec"), R1)
MOD = R1["MOD"]; NOMINAL = R1["NOMINAL"]
KPC = 3.0857e19; K474 = 4.740470463
CASES = [("FW_census", "canonical"), ("FW_census", "alt"), ("FW_rc", "canonical"), ("FW_rc", "alt"), ("H", None), ("N", None)]
CKEY = lambda m, f: f"{m}/{f}" if f else m
CK = [CKEY(m, f) for m, f in CASES]
FWK = CK[:4]
BN = ["20-30", "30-40", "40-55", "55-80"]
A0EXACT = {"canonical": 9.3603e-11 / 9.36e-11, "alt": 1.1312e-10 / 1.13e-10, None: 1.0}
XERR = 1.3085676978624774
S2_IDX = np.array([439, 1497, 1501, 1502, 1503, 1508, 1627, 2122, 2131, 2268, 2416, 2555, 2889, 3159, 3670, 3684, 3747,
                   4409, 4414, 4525, 4555, 4975, 4978, 4982, 5713, 5722, 6088, 6092, 6163, 6303, 6305])
SLOPE_LIMIT = 1.382

# ================================================================== MY Jeans integral (variable beta, any tracer law)
JG = np.logspace(0.0, math.log10(2.0e4), 8000)
BEDGE = (30.0, 40.0, 55.0)
def ln_n(s, prof):
    s = np.asarray(s, float)
    if prof[0] == "single": return -prof[1] * np.log(s / 40.0)
    _, ai, ao, rb = prof
    x = np.log(s / rb); return np.where(s < rb, -ai * x, -ao * x)
def beta_at(r, bt):
    r = np.asarray(r, float)
    return np.where(r < BEDGE[0], bt[0], np.where(r < BEDGE[1], bt[1], np.where(r < BEDGE[2], bt[2], bt[3])))
def ln_I(s, bt):
    """ln of exp(int_1^s 2 beta(s')/s' ds') for piecewise-constant beta; exact."""
    x = np.log(np.asarray(s, float)); out = 2 * bt[0] * x
    for k, e in enumerate(BEDGE):
        out = out + 2 * (bt[k + 1] - bt[k]) * np.maximum(x - math.log(e), 0.0)
    return out
def _expseg(dx, lw0, lw1):
    """integral over a segment of length dx (in ln s) of exp(log-linear from lw0 to lw1)."""
    d = lw1 - lw0; small = np.abs(d) < 1e-8
    ratio = np.where(small, 1.0 + 0.5 * d, np.expm1(d) / np.where(small, 1.0, d))
    return dx * np.exp(lw0) * ratio
_GC = {}
def gfun_model(model, ft, a0m):
    def g(s):
        return MOD.g_model(s, model, ft, a0m)
    return g
def sr2_at(r, prof, bt, gfun):
    """sigma_r^2 [(km/s)^2] at radii r [kpc]: (1/(n I)) int_r^inf n I g ds, exponential rule per ln s segment."""
    extra = [prof[3]] if prof[0] == "broken" else []
    s = np.unique(np.concatenate([JG, BEDGE, extra])); x = np.log(s)
    lnw = ln_n(s, prof) + ln_I(s, bt) + np.log(gfun(s) * s * KPC)
    off = float(lnw.max()); lw = lnw - off
    seg = _expseg(np.diff(x), lw[:-1], lw[1:])
    cum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])          # cum[k] = int from s_k to s_end
    r = np.asarray(r, float); lr = np.log(r)
    k = np.clip(np.searchsorted(x, lr, side="right") - 1, 0, len(x) - 2)
    # the star's own partial segment [r, s_(k+1)]: integrand at r computed exactly, exponential rule to the next node
    lnnI = ln_n(r, prof) + ln_I(r, bt)
    lwr = lnnI + np.log(gfun(r) * r * KPC) - off
    part = _expseg(x[k + 1] - lr, lwr, lw[k + 1])
    return (part + cum[k + 1]) * np.exp(off - lnnI) / 1e6

# ================================================================== MY estimator
def fit_scale(v, e2, P, lo=0.05, hi=5.0):
    """v ~ N(mu, f^2 P + e^2); mu exact weighted mean for each f; f = profile-likelihood maximum; s = half the
    Delta lnL = 0.5 interval. Returns f, s, mu."""
    def nll(f):
        var = f * f * P + e2; w = 1.0 / var; mu = np.dot(w, v) / w.sum(); rr = v - mu
        return 0.5 * (np.dot(rr * rr, w) + np.log(var).sum())
    g = np.exp(np.linspace(math.log(lo), math.log(hi), 41)); vals = np.array([nll(x) for x in g]); k = int(np.argmin(vals))
    a, b = g[max(k - 1, 0)], g[min(k + 1, 40)]
    res = minimize_scalar(nll, bounds=(a, b), method="bounded", options=dict(xatol=1e-9))
    fb, nb = float(res.x), float(res.fun)
    def side(sg):
        x = fb; step = max(0.01 * fb, 1e-4)
        for _ in range(200):
            xn = x + sg * step
            if xn <= lo or xn >= hi:
                xn = lo if sg < 0 else hi
                return brentq(lambda t: nll(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-10) if nll(xn) - nb > 0.5 else xn
            if nll(xn) - nb > 0.5: return brentq(lambda t: nll(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-10)
            x = xn; step *= 1.5
        return xn
    flo, fhi = side(-1), side(+1)
    var = fb * fb * P + e2; w = 1.0 / var
    return fb, 0.5 * (fhi - flo), float(np.dot(w, v) / w.sum())
def est_bin(v, e, P, bpos, F):
    e2 = e * e
    if F:
        nN, nS = int(bpos.sum()), int((~bpos).sum())
        if nN >= 15 and nS >= 15:
            fN, sN, _ = fit_scale(v[bpos], e2[bpos], P[bpos]); fS, sS, _ = fit_scale(v[~bpos], e2[~bpos], P[~bpos])
            return 0.5 * (fN + fS), 0.5 * math.hypot(sN, sS)
    f, s, _ = fit_scale(v, e2, P); return f, s
def wordf(f, s): return "HOT" if f > 1 + 2 * s else ("COLD" if f < 1 - 2 * s else "PASS")

# ================================================================== KA-4, KA-6 (no data)
sec("RRL3R known answers without data: KA-4 (my variable-beta Jeans vs closed form), KA-6 (SI)")
say(f"  RAW1 files read-only: raw1.py sha256 {sha(os.path.join(RAW1, 'raw1.py'))[:16]}..., raw1_model.py {sha(os.path.join(RAW1, 'raw1_model.py'))[:16]}...")
V = 200e3; flat = lambda s: V ** 2 / (np.asarray(s, float) * KPC)
rr = np.array([20.0, 25.0, 30.0, 40.0, 55.0, 60.0, 80.0]); worst = 0.0
for a, b in ((4.5, 0.5), (3.5, 0.0), (5.289, 0.6586)):
    got = sr2_at(rr, ("single", a), (b,) * 4, flat); ex = (V / 1e3) ** 2 / (a - 2 * b)
    worst = max(worst, float(np.max(np.abs(got / ex - 1))))
ai_, ao_, rbk, b_ = 3.0, 5.0, 35.0, 0.6586
def broken_flat_exact(r):   # [rrl1r copy] closed form for a broken law in a flat curve at constant beta
    V2 = (V / 1e3) ** 2; outer = V2 * rbk ** (2 * b_) / (ao_ - 2 * b_)
    if r >= rbk: return V2 / (ao_ - 2 * b_)
    c = 2 * b_ - ai_; inner = V2 * rbk ** ai_ * (rbk ** c - r ** c) / c
    return (inner + outer) / ((r / rbk) ** (-ai_) * r ** (2 * b_))
got = sr2_at(rr, ("broken", ai_, ao_, rbk), (b_,) * 4, flat); ex = np.array([broken_flat_exact(x) for x in rr])
worst2 = float(np.max(np.abs(got / ex - 1)))
# also: variable beta in a flat curve, single law: closed form by direct piecewise integration (independent check)
def var_beta_flat_exact(r, a, bt):
    V2 = (V / 1e3) ** 2; edges = [0.0, 30.0, 40.0, 55.0, np.inf]
    lnnI = lambda s: -a * math.log(s / 40.0) + float(ln_I(np.array([s]), bt)[0])
    tot = 0.0
    for k in range(4):
        lo_, hi_ = max(edges[k], r), edges[k + 1]
        if hi_ <= lo_: continue
        p = 2 * bt[k] - a - 1.0   # integrand n I g ~ s^(2 b_k - a) * s^-1 in ds -> s^(p)
        c = math.exp(lnnI(lo_)) / lo_ ** (2 * bt[k] - a)
        F_ = (lambda s: s ** (p + 1) / (p + 1))
        tot += c * V2 * ((0.0 if hi_ == np.inf else F_(hi_)) - F_(lo_))
    return tot / math.exp(lnnI(r))
btv = (0.671, 0.685, 0.441, 0.441)
got3 = sr2_at(rr, ("single", 4.4), btv, flat); ex3 = np.array([var_beta_flat_exact(x, 4.4, btv) for x in rr])
worst3 = float(np.max(np.abs(got3 / ex3 - 1)))
check("KA-4 constant beta, single laws, flat curve: sigma_r^2 = V^2/(a - 2 beta)", worst < 1e-6, f"max relative difference {worst:.2e}")
check("KA-4 constant beta 0.6586, broken law 3/5/35, flat curve, exact", worst2 < 1e-6, f"max relative difference {worst2:.2e}")
check("KA-4 (extra) piecewise beta (0.671, 0.685, 0.441), single 4.4, flat curve, piecewise exact", worst3 < 1e-6, f"max relative difference {worst3:.2e}")
dr = 0.0
for m, ft in CASES:
    for a, b in ((5.289, 0.6586), (3.5, 0.2)):
        mine = sr2_at(rr, ("single", a), (b,) * 4, gfun_model(m, ft, 1.0)); raw = R1["sr2_at"](rr, m, a, b, ft, 1.0)
        dr = max(dr, float(np.max(np.abs(mine / raw - 1))))
say(f"  [INFO] my Jeans vs RAW1's sr2_profile (trapezoid, 4,000 nodes) on the real models at constant beta: max relative difference {dr:.2e} (not gated)")
G_SI, MSUN_SI = 6.674e-11, 1.989e30
g30 = float(MOD.g_model(30.0, "FW_census", "canonical")); Msi = g30 * (30 * KPC) ** 2 / G_SI / MSUN_SI
check("KA-6 SI: M = g r^2 / G at 30 kpc (FW census canonical, rounded a0)", abs(Msi / float(MOD.M_of_g(g30, 30.0)) - 1) < 1e-9,
      f"g = {g30:.5e} m/s^2, M = {Msi:.5e} Msun, V = sqrt(g r) = {math.sqrt(g30 * 30 * KPC) / 1e3:.2f} km/s")
g30e = float(MOD.g_model(30.0, "FW_census", "canonical", A0EXACT["canonical"]))
say(f"  [INFO] with a0 = 9.3603e-11 exactly: g(30) = {g30e:.5e} m/s^2, M = {g30e * (30 * KPC) ** 2 / G_SI / MSUN_SI:.5e} Msun")
stop_if_failed()

# ================================================================== RAW1's sample, KA-1
sec("RAW1's BHB sample (RAW1 load / build / measure, read-only) and KA-1")
check("BHB file sha256", sha(FITS) == SHA["bhb"], rel(FITS))
stop_if_failed()
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
D = R1["load"](); CFG0 = dict(NOMINAL); S = R1["build"](D, CFG0)
_h = fits.open(FITS, memmap=False); _rv = _h["RVTAB"].data
LOGG = np.asarray(_rv["LOGG"], float)[S["i"]]; LOGGE = np.asarray(_rv["LOGG_ERR"], float)[S["i"]]
_gal = SkyCoord(ra=D["ra"][S["i"]] * u.deg, dec=D["dec"][S["i"]] * u.deg, frame="icrs").galactic
GB = _gal.b.deg; BPOS = GB > 0
VG, VE, SR, SIN2 = S["vgsr"], S["verr"], S["r"], S["sin2"]
BIN = np.array([next((j for j, (a, b) in enumerate(R1["BINS"]) if a <= x < b), -1) for x in SR])
NS = len(SR)
R = R1["measure"](S, CFG0)
J = json.load(open(os.path.join(RAW1, "raw1_results.json")))["nominal"]
say(f"  stars {NS}, per bin {[int(np.sum(BIN == j)) for j in range(4)]}; RAW1 measure: alpha {R['alpha']['alpha']:.4f} +/- {R['alpha']['sig']:.4f}, "
    f"beta {R['beta']:.4f} +/- {R['sbeta']:.4f}, ranges {[(round(x, 4), round(y, 4)) for x, y in R['brange']]}")
check("KA-1 counts", [int(np.sum(BIN == j)) for j in range(4)] == list(R["counts"]) == J["counts"] == [865, 264, 241, 125], f"{R['counts']}")

def f_rows_plain(prof, model, ft, a0m, bt, v=None, keep=None, esc=1.0, F=False):
    v = VG if v is None else v; keep = np.ones(NS, bool) if keep is None else keep
    P = sr2_at(SR, prof, bt, gfun_model(model, ft, a0m)) * (1.0 - beta_at(SR, bt) * SIN2)
    out = []
    for j in range(4):
        m = keep & (BIN == j)
        out.append(est_bin(v[m], VE[m] * esc, P[m], BPOS[m], F))
    return out
aR, saR, bR, sbR = R["alpha"]["alpha"], R["alpha"]["sig"], R["beta"], R["sbeta"]; BRANGE = R["brange"]
dmax_all = 0.0
for (m, ft), k in zip(CASES, CK):
    nom = f_rows_plain(("single", aR), m, ft, 1.0, (bR,) * 4)
    flo = f_rows_plain(("single", aR - saR), m, ft, 1.0, (bR,) * 4); fhi = f_rows_plain(("single", aR + saR), m, ft, 1.0, (bR,) * 4)
    bv = sorted({x for br in BRANGE for x in br}); fb = {x: f_rows_plain(("single", aR), m, ft, 1.0, (x,) * 4) for x in bv}
    dm = 0.0; txt = []
    for j in range(4):
        sal = 0.5 * abs(fhi[j][0] - flo[j][0]); lo, hi = BRANGE[j]; sbe = 0.5 * abs(fb[hi][j][0] - fb[lo][j][0])
        s = math.sqrt(nom[j][1] ** 2 + sal ** 2 + sbe ** 2)
        dm = max(dm, abs(nom[j][0] - J["f"][k][j]["f"]), abs(s - J["f"][k][j]["s"])); txt.append(f"{nom[j][0]:.4f}+/-{s:.4f}")
    dmax_all = max(dmax_all, dm)
    check(f"KA-1 RAW1 reproduced with my Jeans and estimator, {k}", dm < 5e-4, "  ".join(txt) + f" (max diff {dm:.1e})")
stop_if_failed()

# ================================================================== MY anisotropy measurement, KA-3
sec("My per-bin anisotropy from the stars' own proper motions (RAW1's full per-bin sample, unscaled errors), KA-3")
PMOK = S["pmok"]
def pm_data(sel, dfrac=0.10):
    d = S["d"][sel]; vs = S["vs"]
    vta = K474 * d * S["pmra"][sel]; vtd = K474 * d * S["pmdec"][sel]
    w = np.stack([S["vgsr"][sel], vta + S["ea"][sel] @ vs, vtd + S["no"][sel] @ vs], axis=1)
    sa, sd = K474 * d * S["epmra"][sel], K474 * d * S["epmdec"][sel]
    E = np.zeros((len(d), 3, 3)); E[:, 0, 0] = S["verr"][sel] ** 2
    E[:, 1, 1] = sa ** 2 + (dfrac * vta) ** 2; E[:, 2, 2] = sd ** 2 + (dfrac * vtd) ** 2; E[:, 1, 2] = E[:, 2, 1] = S["rho"][sel] * sa * sd
    B3 = np.stack([S["n"][sel], S["ea"][sel], S["no"][sel]], axis=1)       # rows: basis vectors (Galactocentric axes)
    rh = S["rh"][sel]; pos = S["pos"][sel]; Rc = np.hypot(pos[:, 0], pos[:, 1])
    ph = np.stack([-pos[:, 1] / Rc, pos[:, 0] / Rc, np.zeros(len(d))], axis=1)
    q = np.einsum("nij,nj->ni", B3, rh); qp = np.einsum("nij,nj->ni", B3, ph)
    return dict(w=w, E=E, q=q, qp=qp, terr=np.sqrt(0.5 * (sa ** 2 + sd ** 2)), N=int(len(d)))
def pm_nll(Pd, lnsr, beta):
    sr2 = math.exp(2 * lnsr); st2 = (1.0 - beta) * sr2
    C = Pd["E"] + st2 * np.eye(3)[None, :, :] + (sr2 - st2) * Pd["q"][:, :, None] * Pd["q"][:, None, :]
    Ci = np.linalg.inv(C); det = np.linalg.det(C)
    if np.any(det <= 0): return 1e30
    a = np.einsum("nij,nj->ni", Ci, Pd["w"]); c = np.einsum("nij,nj->ni", Ci, Pd["qp"])
    vphi = np.sum(Pd["qp"] * a) / np.sum(Pd["qp"] * c)
    x = Pd["w"] - vphi * Pd["qp"]; quad = np.einsum("ni,nij,nj->n", x, Ci, x)
    return 0.5 * float(np.sum(quad + np.log(det)))
def my_beta(Pd):
    prof = lambda be: minimize_scalar(lambda t: pm_nll(Pd, t, be), bounds=(math.log(20.0), math.log(600.0)), method="bounded",
                                      options=dict(xatol=1e-8)).fun
    grid = np.linspace(-2.9, 0.98, 30); vals = [prof(x) for x in grid]; k = int(np.argmin(vals))
    res = minimize_scalar(prof, bounds=(grid[max(k - 1, 0)], grid[min(k + 1, 29)]), method="bounded", options=dict(xatol=1e-7))
    bb, nb = float(res.x), float(res.fun)
    def side(sg):
        x = bb; step = 0.005
        for _ in range(200):
            xn = x + sg * step
            if xn < -3.0 or xn > 0.99: return -3.0 if sg < 0 else 0.99
            if prof(xn) - nb > 0.5: return brentq(lambda t: prof(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-7)
            x = xn; step *= 1.4
        return x
    lo, hi = side(-1), side(+1)
    return dict(beta=bb, lo=lo, hi=hi, sig=0.5 * (hi - lo), N=Pd["N"], med_terr=float(np.median(Pd["terr"])))
MYB = []
for j in range(4):
    mbin = BIN == j; sel = mbin & PMOK
    sig_los = fit_scale(VG[mbin], VE[mbin] ** 2, np.ones(int(mbin.sum())), 1.0, 400.0)[0]
    if sel.sum() < 30: MYB.append(dict(N=int(sel.sum()), usable=False, why="fewer than 30 with PM", sig_los=sig_los)); continue
    Pd = pm_data(sel)
    if np.median(Pd["terr"]) > sig_los:
        MYB.append(dict(N=Pd["N"], usable=False, why="median PM error > LOS dispersion", med_terr=float(np.median(Pd["terr"])), sig_los=sig_los)); continue
    x = my_beta(Pd); x.update(usable=x["sig"] <= 0.3, why="" if x["sig"] <= 0.3 else "beta error > 0.3", sig_los=sig_los); MYB.append(x)
for j, x in enumerate(MYB):
    rb_ = R["pmbeta"][j]
    say(f"  {BN[j]}: PM stars {x['N']}, LOS dispersion {x['sig_los']:.2f} km/s, median tangential error {x.get('med_terr', float('nan')):.1f} km/s; "
        + (f"my beta {x['beta']:.4f} [{x['lo']:.4f}, {x['hi']:.4f}] (sigma {x['sig']:.4f}); usable {x['usable']}" if "beta" in x else f"not fitted ({x['why']})")
        + (f"; cross-check RAW1 measure {rb_['beta']:.4f} +/- {rb_['sig']:.4f}" if "beta" in rb_ else "; RAW1 measure: not fitted"))
KA3T = (0.671, 0.685, 0.441)
for j in range(3):
    ok = MYB[j].get("usable", False) and abs(MYB[j]["beta"] - KA3T[j]) <= 0.02
    check(f"KA-3 beta {BN[j]}", ok, f"{MYB[j].get('beta', float('nan')):.4f} vs {KA3T[j]} (tolerance 0.02)")
check("KA-3 55-80 not usable", not MYB[3].get("usable", False), MYB[3].get("why", ""))
stop_if_failed()
BV = tuple(MYB[j]["beta"] for j in range(3)); BS = tuple(MYB[j]["sig"] for j in range(3))
BT_C = (BV[0], BV[1], BV[2], BV[2])
BT_LO = (BV[0] - BS[0], BV[1] - BS[1], BV[2] - BS[2], BV[2] - BS[2]); BT_HI = (BV[0] + BS[0], BV[1] + BS[1], BV[2] + BS[2], BV[2] + BS[2])
BVARS_C = [(BT_LO, BT_HI)] * 3 + [((BV[0], BV[1], BV[2], 0.2), (BV[0], BV[1], BV[2], 0.8))]
say(f"  measured beta profile used in C: {tuple(round(x, 4) for x in BT_C)} (beyond 55 kpc: the 40-55 value); 2 beta_3 + 0.5 = {2 * BV[2] + 0.5:.3f} "
    f"(frozen slope limit {SLOPE_LIMIT})")
BT_CONST = (bR,) * 4
BVARS_CONST = [((x,) * 4, (y,) * 4) for x, y in BRANGE]

# ================================================================== C masks, KA-2
sec("Convention C (L, S2, X, B, F) and KA-2 (single slope 5.289, rounded a0, FW census canonical)")
KEEP_L = ~((LOGG > 3.75) & (LOGGE < 0.25) & np.isfinite(LOGG))
KEEP_S2 = ~np.isin(S["i"], S2_IDX)
say(f"  L removes {[int(np.sum(~KEEP_L & (BIN == j))) for j in range(4)]}; S2 list {len(S2_IDX)} indices, in the sample {int(np.sum(~KEEP_S2))}, "
    f"removed per bin {[int(np.sum(~KEEP_S2 & (BIN == j))) for j in range(4)]}")
KEEP_C = KEEP_L & KEEP_S2
def conv(keep, esc, F, bt, bvars, name):
    return dict(keep=keep, esc=esc, F=F, bt=bt, bvars=bvars, name=name,
                masks=[keep & (BIN == j) for j in range(4)], n=[int(np.sum(keep & (BIN == j))) for j in range(4)])
CONV_C = conv(KEEP_C, XERR, True, BT_C, BVARS_C, "C")
ka2 = f_rows_plain(("single", 5.289), "FW_census", "canonical", 1.0, BT_C, keep=KEEP_C, esc=XERR, F=True)
KA2T = (1.0901, 1.2248, 1.1645, 1.1432)
check("KA-2 star counts", CONV_C["n"] == [727, 227, 186, 115], f"{CONV_C['n']}")
for j in range(4):
    check(f"KA-2 f {BN[j]}", abs(ka2[j][0] - KA2T[j]) <= 0.01, f"{ka2[j][0]:.4f} +/- {ka2[j][1]:.4f} (stat) vs {KA2T[j]}")
stop_if_failed()

# ================================================================== [rrl1r copy] RR Lyrae tables, grid, masks, fits
def read_tsv(path):
    with open(path) as fh:
        lines = [l.rstrip("\n") for l in fh if not l.startswith("#") and l.strip() != ""]
    names = lines[0].split("\t"); cols = {n: [] for n in names}
    for l in lines[3:]:
        parts = l.split("\t") + [""] * len(names)
        for n, p in zip(names, parts): cols[n].append(p.strip())
    return cols
def fl(col): return np.array([float(x) if x not in ("",) else np.nan for x in col])
sec("RR Lyrae inputs")
check("PS1 sha256", sha(PS1_PATH) == SHA["ps1"], rel(PS1_PATH))
check("DES sha256", sha(DES_PATH) == SHA["des"], rel(DES_PATH))
stop_if_failed()
T5 = read_tsv(PS1_PATH)
P_ra, P_dec, P_s3ab, P_dm, P_ebv = fl(T5["RAJ2000"]), fl(T5["DEJ2000"]), fl(T5["S3ab"]), fl(T5["DM"]), fl(T5["E(B-V)"])
T1d = read_tsv(DES_PATH)
D_ra, D_dec, D_mu, D_ag = fl(T1d["RAJ2000"]), fl(T1d["DEJ2000"]), fl(T1d["mu"]), fl(T1d["Ag"])
D_acc = np.array([x == "True" for x in T1d["ACc"]]); D_sys = np.array([x != "" for x in T1d["Sys"]])
del T5, T1d
say(f"  PS1 rows {len(P_ra)}; DES rows {len(D_ra)} (ACc {int(D_acc.sum())}, Sys {int(D_sys.sum())})")
check("PS1 row count 239,044", len(P_ra) == 239044, f"{len(P_ra)}")
check("DES row count 6,971", len(D_ra) == 6971, f"{len(D_ra)}")
stop_if_failed()

NRA, NSD = 180, 90; NCELL = NRA * NSD; DOM_CELL = 4 * math.pi / NCELL
P0, RM = R1["frame_affine"](NOMINAL["R0"], NOMINAL["zsun"])
def unitv(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T
def cell_of(ra, dec):
    i = np.floor(np.mod(ra, 360.0) / 2.0).astype(int) % NRA
    j = np.clip(np.floor((np.sin(np.radians(dec)) + 1.0) * NSD / 2.0).astype(int), 0, NSD - 1)
    return j * NRA + i
_ii, _jj = np.meshgrid(np.arange(NRA), np.arange(NSD)); _ii, _jj = _ii.ravel(), _jj.ravel()
C_ra = 2.0 * _ii + 1.0; C_dec = np.degrees(np.arcsin(-1.0 + (2 * _jj + 1.0) / NSD))
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
    uv = unitv(ra, dec); tr = cKDTree(uv); nb = tr.query_ball_point(uv, chord(0.5))
    is_c = np.zeros(len(ra), bool)
    for k, lst in enumerate(nb):
        if len(lst) >= 5:
            lst = np.asarray(lst); is_c[k] = int(np.sum(np.abs(dm[lst] - dm[k]) < 0.25)) - 1 >= 4
    cmask = np.zeros(NCELL, bool); groups = []
    if is_c.any():
        cu = uv[is_c]; tc = cKDTree(cu)
        hit = tc.query_ball_point(C_u, chord(1.5)); cmask = np.array([len(h) > 0 for h in hit])
        par = list(range(len(cu)))
        def fnd(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a_, b2 in sorted(tc.query_pairs(chord(1.5))):
            ra_, rb2 = fnd(a_), fnd(b2)
            if ra_ != rb2: par[max(ra_, rb2)] = min(ra_, rb2)
        roots = np.array([fnd(x) for x in range(len(cu))]); cdm = dm[is_c]
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
D_cell = cell_of(D_ra, D_dec); D_cnt = np.bincount(D_cell, minlength=NCELL); D_ag_med = cell_median(D_cell, D_ag)
def neighbours_hold(cnt):
    has = (cnt > 0).reshape(NSD, NRA); tot = np.zeros((NSD, NRA), int)
    for dj in (-1, 0, 1):
        for di in (-1, 0, 1):
            if dj == 0 and di == 0: continue
            sh = np.roll(has, -di, axis=1).astype(int)
            if dj == 1: sh = np.vstack([sh[1:], np.zeros((1, NRA), int)])
            elif dj == -1: sh = np.vstack([np.zeros((1, NRA), int), sh[:-1]])
            tot += sh
    return tot.ravel()
D_cov = (D_cnt > 0) | (neighbours_hold(D_cnt) >= 5)
NB_NORM = 4000
def completeness(dm_obs, comp):
    if comp == "none": return np.ones_like(dm_obs)
    x0 = 20.57 if comp == "nominal" else 20.07
    return 1.0 / (1.0 + np.exp(4.1 * (dm_obs + 0.6 - x0)))
def set_data(smp, lnr):
    s = np.sort(lnr); smp["lnr_s"] = s; smp["cum"] = np.concatenate([[0.0], np.cumsum(s)]); smp["N"] = int(len(s))
def build_sample(survey="PS1", score=0.8, comp="nominal", bcut=20.0, sgr=15.0, dscale=1.0, q=1.0, rlo=20.0, rhi=None, verbose=True):
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
    steps = [("covered", cov)]; keep = cov.copy()
    keep &= np.abs(C_b) > bcut; steps.append((f"|b| > {bcut:g}", keep.copy()))
    keep &= ~(red == True); steps.append(("reddening", keep.copy()))
    if sgr is not None and sgr > 0: keep &= ~(np.abs(C_bsgr) < sgr)
    steps.append((f"Sgr band {sgr}", keep.copy()))
    keep &= ~MC_MASK; steps.append(("Magellanic / Fornax / Sculptor", keep.copy()))
    keep &= ~cmask; steps.append(("clump cells", keep.copy()))
    d = dscale * 10 ** (dm / 5.0 + 1.0) / 1000.0
    uv = unitv(ra, dec) @ RM.T
    pos = P0 + d[:, None] * uv; r = np.linalg.norm(pos, axis=1)
    rq = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2 + (pos[:, 2] / q) ** 2)
    instar = keep[cell]; sel = instar & (r >= rlo) & (r < rhi)
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
               ncell=int(keep.sum()), steps=[(s_, int(m_.sum())) for s_, m_ in steps], nclump=int(is_c.sum()),
               nclumpcells=int((cmask & cov).sum()), groups=groups,
               lnW=np.log(W[nz]), lnrk=L[nz] / W[nz], edges_lo=edges[:-1][nz], width=float(edges[1] - edges[0]),
               nodes=(lnrq_all, w_all))
    set_data(smp, np.log(rq[sel]))
    if verbose:
        say(f"  [{survey}] cfg {smp['cfg']}: cells " + ", ".join(f"{s_} {n_}" for s_, n_ in smp["steps"]) +
            f"; clump stars {smp['nclump']}, clump-masked covered cells {smp['nclumpcells']}; stars in kept cells (all r) {int(instar.sum())}; in r range N = {smp['N']}")
    return smp
def lnZ(smp, prof): return float(logsumexp(smp["lnW"] + ln_n(np.exp(smp["lnrk"]), prof)))
def lnZ_exact(smp, prof):
    lr, w = smp["nodes"]; return float(logsumexp(np.log(w) + ln_n(np.exp(lr), prof)))
L40 = math.log(40.0)
def nll_d(smp, prof):
    N = smp["N"]
    if prof[0] == "single":
        a = prof[1]; sdata = -a * (smp["cum"][-1] - N * L40)
    else:
        _, ai, ao, rb = prof; lrb = math.log(rb); k = int(np.searchsorted(smp["lnr_s"], lrb))
        sdata = -ai * (smp["cum"][k] - k * lrb) - ao * (smp["cum"][-1] - smp["cum"][k] - (N - k) * lrb)
    return -sdata + N * lnZ(smp, prof)
def fit_single(smp):
    f = lambda a: nll_d(smp, ("single", a))
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
    return dict(a=ab, nll=nb, sig=1.0 / math.sqrt(H) if H > 0 else float("nan"), lo=side(-1), hi=side(+1))
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
        g = lambda p: nll_d(smp, ("broken", p[0], p[1], rb))
        res = minimize(g, [a0, a0], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
        prof_g.append((float(rb), float(res.fun), res.x.copy()))
    jb = int(np.argmin([x[1] for x in prof_g])); rb0, _, p0 = prof_g[jb]
    f3 = lambda p: (nll_d(smp, ("broken", p[0], p[1], p[2])) if lo_ <= p[2] <= hi_ else np.inf)
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
        g2 = lambda pp: nll_d(smp, ("broken", pp[0], pp[1], p[2])); H2 = hess(g2, p[:2], np.array([0.02, 0.02]))
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
def draw_mock(smp, prof, rng):
    lp = smp["lnW"] + ln_n(np.exp(smp["lnrk"]), prof); p = np.exp(lp - lp.max()); p /= p.sum()
    k = rng.choice(len(p), size=smp["N"], p=p)
    return smp["edges_lo"][k] + rng.random(smp["N"]) * smp["width"]
def mock_set(name, smp, prof, base_seed, nmock, rbr):
    path = os.path.join(HERE, f"mocks_{name}.jsonl"); done = {}
    if os.path.exists(path):
        for line in open(path):
            try:
                x = json.loads(line)
                if x.get("seed") == base_seed: done[x["i"]] = x
            except Exception: pass
    fh = open(path, "a")
    for i in range(nmock):
        if i in done: continue
        rng = np.random.default_rng([base_seed, i]); m = dict(smp); set_data(m, draw_mock(smp, prof, rng))
        s1, b1, tl = fit_both(m, rbr)
        x = dict(seed=base_seed, i=i, a=s1["a"], tdl=tl, ain=b1["ain"], aout=b1["aout"], rb=b1["rb"]); done[i] = x
        fh.write(json.dumps(x) + "\n"); fh.flush()
    fh.close()
    return [done[i] for i in range(nmock)]
def prof_of(model, s1, b1):
    return ("single", s1["a"]) if model == "single" else ("broken", b1["ain"], b1["aout"], b1["rb"])
def draws_of(model, s1, b1, rng, n=200, rbr=(25.0, 75.0)):
    out = []
    if model == "single":
        for a in rng.normal(s1["a"], s1["sig"], n): out.append(("single", max(float(a), 0.0)))
    else:
        mu = np.array([b1["ain"], b1["aout"], b1["rb"]]); C = np.array(b1["cov"])
        for x in rng.multivariate_normal(mu, C, n, method="svd"):
            out.append(("broken", max(float(x[0]), 0.0), max(float(x[1]), 0.0), float(np.clip(x[2], rbr[0], rbr[1]))))
    return out
def outer_slope(prof): return prof[1] if prof[0] == "single" else prof[2]
def pstr(prof): return f"single a {prof[1]:.4f}" if prof[0] == "single" else f"broken a_in {prof[1]:.4f}, a_out {prof[2]:.4f}, rb {prof[3]:.3f}"

# ================================================================== PS1 nominal fit, T, KA-5
sec("PS1 nominal sample and density fits (RRL1 sections 1-4)")
RB_PS1, RB_DES = (25.0, 75.0), (25.0, 95.0)
NOM = build_sample("PS1")
say("  clump groups (RA, Dec, median DM, stars), largest first: " + "; ".join(f"({g[0]:.2f}, {g[1]:.2f}, {g[2]:.2f}, {g[3]})" for g in NOM["groups"]))
worstZ = max(abs(lnZ(NOM, pr) - lnZ_exact(NOM, pr)) for pr in (("single", 3.0), ("single", 5.0), ("broken", 3.0, 5.0, 35.0)))
check("KA-5 (K0n) binned normalisation == full node sum", worstZ < 1e-5, f"max |Delta ln Z| {worstZ:.2e}")
stop_if_failed()
S1, B1, TDL = fit_both(NOM, RB_PS1)
say(f"  single: a = {S1['a']:.4f} +/- {S1['sig']:.4f} (Hessian); profile interval [{S1['lo']:.4f}, {S1['hi']:.4f}]")
say(f"  broken: a_in {B1['ain']:.4f} +/- {B1['err'][0]:.4f}, a_out {B1['aout']:.4f} +/- {B1['err'][1]:.4f}, rb {B1['rb']:.3f} +/- {B1['err'][2]:.3f} kpc ({B1['how']})")
say(f"  broken covariance: {np.round(np.array(B1['cov']), 5).tolist()}")
say(f"  2 Delta ln L (broken vs single) = {TDL:.3f}")
say("  rb grid profile (rb, nll - min): " + ", ".join(f"{a_:.1f}:{b_:.2f}" for a_, b_ in B1["grid"]))
sec("Null mocks from the best single law (100, seed 331101) and the threshold T")
NULL = mock_set("null", NOM, ("single", S1["a"]), 331101, 100, RB_PS1)
tvals = np.array([x["tdl"] for x in NULL]); T99 = float(np.percentile(tvals, 99)); T = max(T99, 6.63)
say(f"  2 Delta ln L over null mocks: median {np.median(tvals):.3f}, 90th {np.percentile(tvals, 90):.3f}, 99th {T99:.3f}, max {tvals.max():.3f}; "
    f"T = {T:.3f}{' (floor 6.63)' if T99 < 6.63 else ''}; mock single slopes mean {np.mean([x['a'] for x in NULL]):.4f} sd {np.std([x['a'] for x in NULL]):.4f}")
sec("KA-5: planted single and broken profiles (nominal footprint, completeness and N)")
m1 = dict(NOM); set_data(m1, draw_mock(NOM, ("single", 4.5), np.random.default_rng(331102)))
k1s, k1b, k1t = fit_both(m1, RB_PS1)
check("KA-5 single 4.5 recovered", abs(k1s["a"] - 4.5) <= 2 * k1s["sig"], f"a = {k1s['a']:.4f} +/- {k1s['sig']:.4f}")
check("KA-5 no break in the single mock", k1t <= T, f"2 Delta ln L {k1t:.3f} vs T {T:.3f}")
m2 = dict(NOM); set_data(m2, draw_mock(NOM, ("broken", 3.0, 5.0, 35.0), np.random.default_rng(331103)))
k2s, k2b, k2t = fit_both(m2, RB_PS1)
check("KA-5 planted break detected", k2t > T, f"2 Delta ln L {k2t:.3f} vs T {T:.3f}")
_ok1 = [abs(k2b["ain"] - 3.0) <= 2 * k2b["err"][0], abs(k2b["aout"] - 5.0) <= 2 * k2b["err"][1], abs(k2b["rb"] - 35.0) <= max(2 * k2b["err"][2], 5.0)]
say(f"  [AS FROZEN, reported; replaced by AMENDMENT_A1] seed 331103: a_in {k2b['ain']:.4f} +/- {k2b['err'][0]:.4f} ({'ok' if _ok1[0] else 'outside 2 sigma'}), "
    f"a_out {k2b['aout']:.4f} +/- {k2b['err'][1]:.4f} ({'ok' if _ok1[1] else 'outside 2 sigma'}), rb {k2b['rb']:.3f} +/- {k2b['err'][2]:.3f} ({'ok' if _ok1[2] else 'outside'})")
# AMENDMENT_A1: the broken-mock parameter test over 40 seeds 331800 + k
_pb = []
for _k in range(40):
    _m = dict(NOM); set_data(_m, draw_mock(NOM, ("broken", 3.0, 5.0, 35.0), np.random.default_rng(331800 + _k)))
    _s, _b, _t = fit_both(_m, RB_PS1); _pb.append([_b["ain"], _b["aout"], _b["rb"]] + list(_b["err"]))
_pb = np.array(_pb)
_seedok = (np.abs(_pb[:, 0] - 3) <= 2 * _pb[:, 3]) & (np.abs(_pb[:, 1] - 5) <= 2 * _pb[:, 4]) & (np.abs(_pb[:, 2] - 35) <= np.maximum(2 * _pb[:, 5], 5.0))
for _i, (_nm, _tv) in enumerate((("a_in", 3.0), ("a_out", 5.0), ("rb", 35.0))):
    _pl = (_pb[:, _i] - _tv) / _pb[:, _i + 3]
    check(f"KA-5 (A1) {_nm} over 40 seeds: |mean pull| <= 0.5, pull sd in [0.6, 1.4]", abs(_pl.mean()) <= 0.5 and 0.6 <= _pl.std() <= 1.4,
          f"mean {_pb[:, _i].mean():.4f} (true {_tv}), pull mean {_pl.mean():+.3f}, pull sd {_pl.std():.3f}")
check("KA-5 (A1) seeds passing all three per-seed tests >= 34 of 40", int(_seedok.sum()) >= 34, f"{int(_seedok.sum())} of 40")
stop_if_failed()
say("  All known answers KA-1 to KA-6 passed.")

BREAK = TDL > T; MODEL = "broken" if BREAK else "single"
PROF = prof_of(MODEL, S1, B1)
DRAWS = draws_of(MODEL, S1, B1, np.random.default_rng(331107))
say(f"  Break detected: {BREAK} (2 Delta ln L {TDL:.3f} vs T {T:.3f}); profile used: {MODEL}: {pstr(PROF)}; outer slope {outer_slope(PROF):.4f} "
    f"(limit {SLOPE_LIMIT}); draws: 200 (seed 331107), outer slope 2.5-97.5 pct {np.percentile([outer_slope(p) for p in DRAWS], 2.5):.3f} to "
    f"{np.percentile([outer_slope(p) for p in DRAWS], 97.5):.3f}")

# ================================================================== grading machinery
_PC = {}
def predP(prof, model, ft, a0m, bt):
    key = (prof, model, ft, a0m, bt)
    if key not in _PC:
        _PC[key] = sr2_at(SR, prof, bt, gfun_model(model, ft, a0m)) * (1.0 - beta_at(SR, bt) * SIN2)
    return _PC[key]
def est_all(v, P, cv):
    return [est_bin(v[m], VE[m] * cv["esc"], P[m], BPOS[m], cv["F"]) for m in cv["masks"]]
def grade_case(prof, drs, model, ft, cv, v=None, a0m=None):
    v = VG if v is None else v
    a0m = A0EXACT[ft] if a0m is None else a0m
    nom = est_all(v, predP(prof, model, ft, a0m, cv["bt"]), cv)
    sb = []
    for j in range(4):
        lo, hi = cv["bvars"][j]
        flo = est_bin(v[cv["masks"][j]], VE[cv["masks"][j]] * cv["esc"], predP(prof, model, ft, a0m, lo)[cv["masks"][j]], BPOS[cv["masks"][j]], cv["F"])[0]
        fhi = est_bin(v[cv["masks"][j]], VE[cv["masks"][j]] * cv["esc"], predP(prof, model, ft, a0m, hi)[cv["masks"][j]], BPOS[cv["masks"][j]], cv["F"])[0]
        sb.append(0.5 * abs(fhi - flo))
    fd = np.array([est_all(v, predP(p, model, ft, a0m, cv["bt"]), cv) for p in drs])   # (draw, bin, 2)
    rows = []
    for j in range(4):
        f, ss = nom[j]; ssl = float(np.std(fd[:, j, 0])); s = math.sqrt(ss ** 2 + ssl ** 2 + sb[j] ** 2)
        rows.append(dict(n=int(cv["masks"][j].sum()), f=float(f), s_stat=float(ss), s_slope=ssl, s_beta=float(sb[j]), s=s, word=wordf(f, s)))
    allpass = np.all(np.abs(fd[:, :, 0] - 1.0) <= 2 * np.sqrt(fd[:, :, 1] ** 2 + np.array(sb)[None, :] ** 2), axis=1)
    return dict(rows=rows, frac_allpass=float(np.mean(allpass)))
def word_rules_3_5(res, prof):
    words = [x["word"] for x in res["rows"]]
    if outer_slope(prof) <= SLOPE_LIMIT or 0.16 <= res["frac_allpass"] <= 0.84: return "NO VERDICT (SLOPE)", []
    if all(w == "PASS" for w in words): return "ROW PASSES UNDER THE MEASURED CONVENTION", []
    return "ROW FAILS", [[BN[j], w] for j, w in enumerate(words) if w != "PASS"]
def run_conv(prof, drs, cv, cases=CASES):
    out = {}
    for m, ft in cases:
        k = CKEY(m, ft); out[k] = grade_case(prof, drs, m, ft, cv); out[k]["word35"], out[k]["bins"] = word_rules_3_5(out[k], prof)
    _PC.clear()
    return out
def show(res, indent="  "):
    for k in res:
        x = res[k]
        say(f"{indent}{k:20s} " + "  ".join(f"{r_['f']:.4f}+/-{r_['s']:.4f} {r_['word']:4s}" for r_ in x["rows"]) +
            f"  | all-PASS in draws {x['frac_allpass']:.3f} -> {x['word35']} {x['bins'] if x['bins'] else ''}")
def show_parts(res, indent="    "):
    for k in res:
        say(f"{indent}{k:20s} N, (s_stat, s_slope, s_beta): " + "  ".join(f"{r_['n']} ({r_['s_stat']:.4f}, {r_['s_slope']:.4f}, {r_['s_beta']:.4f})" for r_ in res[k]["rows"]))

RESULTS = dict(betas=MYB, beta_profile=BT_C, raw1_measure=dict(alpha=aR, salpha=saR, beta=bR, sbeta=sbR),
               ka2=[list(x) for x in ka2], fit=dict(single=S1, broken=B1, tdl=TDL, T=T, T99=T99, null_tdl=tvals.tolist(), N=NOM["N"],
               cells=NOM["ncell"], steps=NOM["steps"], nclump=NOM["nclump"], groups=NOM["groups"], model=MODEL, profile=PROF),
               ka5=dict(single=k1s, single_tdl=k1t, broken=k2b, broken_tdl=k2t))

sec("Primary: PS1 profile + C (graded footings a0 = 9.3603e-11 / 1.1312e-10); f +/- sigma_f and word per bin (20-30, 30-40, 40-55, 55-80)")
PRIM = run_conv(PROF, DRAWS, CONV_C)
show(PRIM); show_parts(PRIM)
RESULTS["primary"] = PRIM

# ================================================================== twins and mutations (gate)
MUT = open(os.path.join(HERE, "rrl3r_MUTATE.out"), "w")
def msay(s): print("[MUT] " + s, flush=True); MUT.write(s + "\n"); MUT.flush()
sec("Twins and mutations (gate the word): TW1 null, MU1 f 0.80 in 40-55, MU2 f 1.25 in 30-40; FW census, 20 seeds each")
msay("RRL3R twins and mutations (FROZEN_CRITERIA.md section 7). FW census case, primary convention, per footing, 20 seeds each.")
msay("TW1 (true f = 1): all four bins PASS in >= 12 of 20. MU1 (true f 0.80 in 40-55): COLD in >= 15 of 20. MU2 (true f 1.25 in 30-40): HOT in >= 15 of 20.")
GATE = {}; TWIN = {}
for ft in ("canonical", "alt"):
    a0m = A0EXACT[ft]; Ptrue = predP(PROF, "FW_census", ft, a0m, CONV_C["bt"]).copy()
    mu_bin = np.zeros(NS)
    for j in range(4):
        m = CONV_C["masks"][j]; w = 1.0 / (VE[m] * XERR) ** 2; mu_bin[m] = np.sum(w * VG[m]) / np.sum(w)
    TWIN[ft] = {}
    for tag, base, tvec in (("TW1", 331300, (1.0, 1.0, 1.0, 1.0)), ("MU1", 331400, (1.0, 1.0, 0.80, 1.0)), ("MU2", 331500, (1.0, 1.25, 1.0, 1.0))):
        recs = []
        for kk in range(20):
            rng = np.random.default_rng(base + kk); tt = np.array(tvec)[np.clip(BIN, 0, 3)]
            vm = mu_bin + rng.normal(0, 1, NS) * np.sqrt(tt ** 2 * Ptrue + (XERR * VE) ** 2)
            res = grade_case(PROF, DRAWS, "FW_census", ft, CONV_C, v=vm)
            recs.append([x["word"] for x in res["rows"]] + [round(x["f"], 4) for x in res["rows"]] + [round(x["s"], 4) for x in res["rows"]])
        if tag == "TW1": cnt = sum(all(w == "PASS" for w in r_[:4]) for r_ in recs); ok = cnt >= 12; need = "all four PASS"
        elif tag == "MU1": cnt = sum(r_[2] == "COLD" for r_ in recs); ok = cnt >= 15; need = "40-55 COLD"
        else: cnt = sum(r_[1] == "HOT" for r_ in recs); ok = cnt >= 15; need = "30-40 HOT"
        TWIN[ft][tag] = dict(count=int(cnt), ok=bool(ok), need=need, recs=recs)
        mf = np.mean([r_[4:8] for r_ in recs], axis=0); ms = np.mean([r_[8:12] for r_ in recs], axis=0)
        line = (f"{ft:9s} {tag}: {need} in {cnt} of 20 -> {'as required' if ok else 'GATE FAILS'}; mean f per bin {np.round(mf, 4).tolist()}, "
                f"mean sigma_f {np.round(ms, 4).tolist()}; word counts per bin " +
                str([{w: sum(r_[j] == w for r_ in recs) for w in ('PASS', 'HOT', 'COLD') if sum(r_[j] == w for r_ in recs)} for j in range(4)]))
        say("  " + line); msay(line)
    GATE[ft] = all(TWIN[ft][t]["ok"] for t in ("TW1", "MU1", "MU2"))
    say(f"  {ft}: gate {'holds (TW1 does not bite, MU1 and MU2 bite)' if GATE[ft] else 'FAILS -> NO VERDICT (NO POWER) on this footing'}")
RESULTS["twins"] = TWIN; RESULTS["gate"] = GATE

def final_word(k, res):
    ft = None if "/" not in k else k.split("/")[1]
    gate_ok = GATE[ft] if ft else (GATE["canonical"] and GATE["alt"])
    if not gate_ok: return "NO VERDICT (NO POWER)", []
    return res[k]["word35"], res[k]["bins"]

# ================================================================== brackets
sec("Brackets (each recomputes rules 3-5; rules 1-2 carried from the primary)")
BRK = {}
CONV_BA = conv(KEEP_L, XERR, True, BT_C, BVARS_C, "Ba: C without S2")
say("-- Ba: C without the S2 cold-group mask"); BRK["Ba: no S2 mask"] = dict(prof=PROF, res=run_conv(PROF, DRAWS, CONV_BA)); show(BRK["Ba: no S2 mask"]["res"], "   ")
OM = "single" if MODEL == "broken" else "broken"; OPROF = prof_of(OM, S1, B1); ODR = draws_of(OM, S1, B1, np.random.default_rng(331108 + 500))
say(f"-- Bb: the other density model ({OM}: {pstr(OPROF)}; draws seed 331608)")
BRK["Bb: other density model"] = dict(prof=OPROF, res=run_conv(OPROF, ODR, CONV_C)); show(BRK["Bb: other density model"]["res"], "   ")
CONV_BC = conv(KEEP_C, XERR, True, BT_CONST, BVARS_CONST, "Bc: constant beta")
say(f"-- Bc: one constant beta {bR:.4f} (RAW1's ranges for s_beta), the rest of C kept")
BRK["Bc: constant beta 0.6586"] = dict(prof=PROF, res=run_conv(PROF, DRAWS, CONV_BC)); show(BRK["Bc: constant beta 0.6586"]["res"], "   ")
BDFIT = {}
for sc, seed in ((0.9, 331601), (0.6, 331602)):
    smp = build_sample("PS1", score=sc); s1, b1, tl = fit_both(smp, RB_PS1); pr = prof_of(MODEL, s1, b1)
    say(f"-- Bd: score > {sc}: N {smp['N']}; single a {s1['a']:.4f} +/- {s1['sig']:.4f}; broken a_in {b1['ain']:.4f} +/- {b1['err'][0]:.4f}, "
        f"a_out {b1['aout']:.4f} +/- {b1['err'][1]:.4f}, rb {b1['rb']:.3f} +/- {b1['err'][2]:.3f}; 2 Delta ln L {tl:.3f} (T {T:.3f}); model kept: {MODEL}")
    BDFIT[sc] = dict(N=smp["N"], single=s1, broken=b1, tdl=tl)
    nm = f"Bd: score > {sc}"; BRK[nm] = dict(prof=pr, res=run_conv(pr, draws_of(MODEL, s1, b1, np.random.default_rng(seed)), CONV_C)); show(BRK[nm]["res"], "   ")
    del smp
RESULTS["brackets"] = {k: dict(profile=v["prof"], res=v["res"]) for k, v in BRK.items()}; RESULTS["bd_fits"] = {str(k): v for k, v in BDFIT.items()}
CONV_NOC = conv(np.ones(NS, bool), 1.0, False, BT_CONST, BVARS_CONST, "no C")
say(f"-- Reported, not a bracket: no C at all (constant beta {bR:.4f}, no masks, no error scale, plain estimator), same profile and draws")
NOC = run_conv(PROF, DRAWS, CONV_NOC); show(NOC, "   "); RESULTS["no_C"] = NOC

# ================================================================== words
sec("WORDS (four framework cases graded per footing; H graded by the same rules beside them; N reported)")
WORDS = {}
for k in CK:
    w, bins = final_word(k, PRIM)
    diff = {}
    for nm, b in BRK.items():
        wb = w if w in ("NO VERDICT (NO POWER)",) else b["res"][k]["word35"]
        if wb != w: diff[nm] = wb
    WORDS[k] = dict(word=w, bins=bins, fragile=bool(diff), fragile_by=diff,
                    rows=[dict(n=x["n"], f=x["f"], s=x["s"], word=x["word"]) for x in PRIM[k]["rows"]])
    say(f"  {k:20s} {w}{' ' + str(bins) if bins else ''}{', FRAGILE ' + str(diff) if diff else ''}" + ("  [reported, not graded]" if k == "N" else ""))
for ft in ("canonical", "alt"):
    ws = {k: WORDS[k]["word"] for k in FWK if k.endswith(ft)}
    same = all(x == WORDS["H"]["word"] for x in ws.values())
    say(f"  {ft}: framework words {list(ws.values())}; DESI NFW (H) {WORDS['H']['word']} -> "
        + ("the same word: the gate separates nothing between the framework and DESI's NFW under this convention" if same else "the words differ"))
RESULTS["words"] = WORDS

# ================================================================== DES cross-check (reported)
sec("DES cross-check (reported, not graded): its own fit and null mocks; FW census canonical and H under C")
DS = build_sample("DES")
dS1, dB1, dT = fit_both(DS, RB_DES)
DNULL = mock_set("des_null", DS, ("single", dS1["a"]), 331108, 100, RB_DES)
dtv = np.array([x["tdl"] for x in DNULL]); dT99 = float(np.percentile(dtv, 99)); TD = max(dT99, 6.63)
dmodel = "broken" if dT > TD else "single"; dprof = prof_of(dmodel, dS1, dB1)
say(f"  single a {dS1['a']:.4f} +/- {dS1['sig']:.4f}; broken a_in {dB1['ain']:.4f} +/- {dB1['err'][0]:.4f}, a_out {dB1['aout']:.4f} +/- {dB1['err'][1]:.4f}, "
    f"rb {dB1['rb']:.3f} +/- {dB1['err'][2]:.3f} ({dB1['how']}); 2 Delta ln L {dT:.3f}; T_DES {TD:.3f}; model {dmodel}")
DRES = run_conv(dprof, draws_of(dmodel, dS1, dB1, np.random.default_rng(331109), rbr=RB_DES), CONV_C, cases=[("FW_census", "canonical"), ("FW_census", "alt"), ("H", None)])
show(DRES, "   ")
RESULTS["des"] = dict(single=dS1, broken=dB1, tdl=dT, T=TD, model=dmodel, N=DS["N"], res=DRES)
MUT.write("kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n"); MUT.close()

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o
with open(os.path.join(HERE, "rrl3r_results.json"), "w") as fh: json.dump(clean(RESULTS), fh, indent=1)
say(f"\nInputs: {rel(PS1_PATH)}, {rel(DES_PATH)}, {rel(FITS)}; run time {time.time() - T0:.0f} s")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
