"""LAM9 core (criteria 9c1f411110, amendment A1): the graded sample, the masks, per-sum template preparation, the two-step
Gamma_b fit and the IMF mass factor alpha. Imported by lam9_fit.py, lam9_k.py and lam9_grade.py. Reads the sums and the
LAM4/LAM7 fits only. κ = ½ FITTED; not theory closed."""
import os, sys, json, glob, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.ndimage import median_filter, binary_dilation
from astropy.io import fits
from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ROOT = os.path.dirname(RB); EXT = os.path.join(ROOT, "_external_data")
TPL_NPZ = os.path.join(EXT, "lam9_templates_2026_11_04", "lam9_templates.npz")
STACK0 = os.path.join(EXT, "lam9_stage0_2026_11_04", "narrow_stack.npy")
WORK = os.path.join(EXT, "lam9_work_2026_11_04")
C = 299792.458; VELSCALE = C * np.log(10) * 1e-4
LO, HI, FT = 3900.0, 8900.0, 2.51
REG_DIM = (14, 6, 13); NT = 14 * 6 * 13
NAI_REG, NAI_FEAT, TIO2_FEAT = (8143.0, 8244.0), (8180.0, 8200.0), (6189.0, 6272.0)
NAD, JOINS = (5880.0, 5910.0), ((7395.0, 7425.0), (8335.0, 8365.0))
RESW = {"NaI8190": (8180.0, 8200.0), "CaT": (8484.0, 8682.0), "TiO1": (5936.0, 5994.0), "TiO2sdss": (6189.0, 6272.0)}
SEED = 20261105

# ---------------------------------------------------------------- the sample (criteria steps 1-4)
def sample():
    KU2 = os.path.join(RB, "KU2_kappa_universality_model_choice", "ku2.py"); argv = sys.argv; sys.argv = ["ku2.py"]
    import io, contextlib
    K = {"__file__": KU2, "__name__": "ku2"}
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(KU2).read().split("ok1 = slow.sum()")[0], "ku2.py", "exec"), K)
    sys.argv = argv
    rows = np.flatnonzero(K["sel"]); n = len(rows)
    dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
    pifu = np.char.strip(np.array(dp["plateifu"], str))[rows]; mid = np.char.strip(np.array(dp["mangaid"], str))[rows]
    absm = np.array(dp["nsa_elpetro_absmag"], float)[rows]; ur = absm[:, 2] - absm[:, 4]
    path = {}
    for d in ("lam4_integrated_2026_11_03", "lam7_integrated_2026_11_04"):
        for fn in glob.glob(os.path.join(EXT, d, "*.npz")): path[os.path.basename(fn)[:-4]] = fn
    FIT = {}
    for fn in (os.path.join(RB, "LAM4_whole_galaxy_absorption", "lam4_fit.jsonl"), os.path.join(RB, "LAM7_orbit_shape_full_sample", "lam7_fit.jsonl")):
        for l in open(fn):
            if l.strip(): r = json.loads(l); FIT[r["plateifu"]] = r
    LD = os.path.join(EXT, "lam2_sdss_lines_2026_11_03"); EW = {}
    for fn in sorted(glob.glob(os.path.join(LD, "lines_*.csv"))):
        for l in open(fn).read().splitlines()[2:]:
            c = l.split(",")
            if c[0].strip(): EW[int(c[0])] = float(c[7]) if c[7] != "" else np.nan
    m = np.loadtxt(os.path.join(LD, "dynpop_match.csv"), delimiter=",", skiprows=1, dtype=np.int64); sid = {}
    for r_, s_ in m: sid.setdefault(int(r_), int(np.int64(s_).view(np.uint64)))
    ew = np.array([-EW.get(sid.get(int(r_), -1), np.nan) for r_ in rows])
    has = np.array([p in path for p in pifu]); gas_known = np.isfinite(ew); poor = gas_known & (ew < 3); s100 = K["sig"] >= 100
    fitok = np.array([p in FIT and FIT[p]["status"] == "ok" and FIT[p]["sigma"] > 0 and abs(FIT[p]["h4"]) < 0.3 for p in pifu])
    chi2k = np.array([FIT[p]["chi2"] if p in FIT and FIT[p]["status"] == "ok" else np.nan for p in pifu])
    cand = has & poor & s100 & fitok
    counts = dict(ku2=n, with_sum=int(has.sum()), gas_known=int(gas_known.sum()), gas_poor=int((has & poor).sum()), sig100=int((has & poor & s100).sum()), fit_ok=int(cand.sum()))
    rich = has & gas_known & (ew >= 3) & s100 & fitok
    return dict(K=K, rows=rows, pifu=pifu, mid=mid, ur=ur, ew=ew, path=path, FIT=FIT, chi2k=chi2k, cand=cand, rich=rich, counts=counts)

# ---------------------------------------------------------------- the observed-frame stack (exactly as lam9_stage0.py)
def build_stack(S):
    R = None; wave = None
    for i, p in enumerate(S["pifu"]):
        if p not in S["path"]: continue
        d = np.load(S["path"][p]); w = d["wave"].astype(float); f = d["flux"].astype(float); v = d["var"].astype(float); bad = d["bad"]
        if wave is None: wave = w; R = np.full((len(S["pifu"]), len(w)), np.nan, np.float32)
        good = ~bad & (v > 0) & np.isfinite(f)
        sm = median_filter(np.where(good, f, np.nan_to_num(np.nanmedian(f))), 101, mode="nearest"); R[i] = np.where(good & (sm > 0), f / sm - 1, np.nan)
    has = np.array([p in S["path"] for p in S["pifu"]])
    stack = np.nanmedian(R[has], axis=0); narrow = stack - median_filter(np.nan_to_num(stack), 21, mode="nearest")
    return np.c_[wave, stack, narrow]
def load_stack():
    a = np.load(os.path.join(WORK, "narrow_stack.npy")); return a[:, 0], a[:, 2]

# ---------------------------------------------------------------- one sum: window and masks m1-m7 (+ variant B)
def prep(fn, narrow):
    d = np.load(fn); z = float(d["z"]); w = d["wave"].astype(float); lamf = w / (1 + z)
    fwf = 2.355 * d["lsf_sigma"].astype(float) / (1 + z)
    flux_f, var_f, bad_f = d["flux"].astype(float), d["var"].astype(float), d["bad"]
    good_f = ~bad_f & (var_f > 0) & np.isfinite(flux_f)
    e = np.where(good_f, np.sqrt(np.clip(var_f, 1e-30, None)), np.nan)
    es = median_filter(np.nan_to_num(e, nan=np.nanmedian(e)), 51, mode="nearest")
    spike = binary_dilation(np.nan_to_num(e / es, nan=0.0) > 1.5, structure=np.ones(3, bool))           # m4
    coh = binary_dilation(np.abs(narrow) > 0.01, structure=np.ones(3, bool))                             # m5
    start = lamf[np.flatnonzero((lamf >= LO) & (fwf >= FT))[0]]; s = (lamf >= start) & (lamf < HI)
    lam, fw, wobs = lamf[s], fwf[s], w[s]; flux, var, good0 = flux_f[s], var_f[s], good_f[s]
    med = np.median(flux[good0]); flux = flux / med
    noise = np.where(good0, np.sqrt(np.clip(var, 1e-30, None)) / med, 1e10)
    em = np.zeros(len(lam), bool); em[util.determine_goodpixels(np.log(lam), [3500.0, 9400.0], 0)] = True     # m2 (True = kept)
    sky = (np.abs(wobs - 5577.3) < 5) | (np.abs(wobs - 6300.3) < 5)                                      # m3
    nad = (lam >= NAD[0]) & (lam <= NAD[1])                                                               # m6
    jn = np.zeros(len(lam), bool)
    for a, b in JOINS: jn |= (lam >= a) & (lam <= b)                                                      # m7
    keepA = good0 & np.isfinite(flux) & em & ~sky & ~spike[s] & ~coh[s] & ~nad & ~jn                      # m1-m7
    keepB = keepA & ~((lam >= NAI_REG[0]) & (lam <= NAI_REG[1]))
    def cov(r):
        q = (lam >= r[0]) & (lam <= r[1]); return float(keepA[q].mean()) if q.any() else 0.0
    nai = (lam >= NAI_REG[0]) & (lam <= NAI_REG[1]) & good0
    sn_nai = float(np.median(flux[nai] / noise[nai]) / np.sqrt(np.median(lam[nai] * np.log(10) * 1e-4))) if nai.any() else float("nan")
    return dict(z=z, lam=lam, fw=fw, wobs=wobs, idx=np.flatnonzero(s), flux=flux, noise=noise, goodA=np.flatnonzero(keepA), goodB=np.flatnonzero(keepB),
                cov_nai=cov(NAI_FEAT), cov_tio2=cov(TIO2_FEAT), start=float(start), sn_nai=sn_nai)
def step5(p): return p["cov_nai"] >= 0.70 and p["cov_tio2"] >= 0.70

# ---------------------------------------------------------------- templates, broadened to one sum's rest LSF
_T = {}
def tlib():
    if not _T:
        a = np.load(TPL_NPZ)
        for k in a.files: _T[k] = a[k]
    return _T
def templates_for(p):
    T = tlib(); lt = T["lam"]
    fg = np.interp(lt, p["lam"], p["fw"])
    sig = np.sqrt(np.clip(fg ** 2 - float(T["fwhm"]) ** 2, 0, None)) / np.sqrt(4 * np.log(4))
    sb = util.varsmooth(lt, T["spec"].astype(np.float64), sig)
    tpl, ln_lt = util.log_rebin(lt, sb, velscale=VELSCALE)[:2]; lam_t = np.exp(ln_lt)
    band = (lam_t >= 5070) & (lam_t <= 5950); n_t = tpl[band].mean(0); tpl = tpl / n_t
    return tpl, lam_t, n_t

# ---------------------------------------------------------------- the fit and alpha
def kin_start(k, dh4=0.0): return [k["V"], k["sigma"], k["h3"], k["h4"] + dh4, k["h5"], k["h6"]]
def fit(p, tpl, lam_t, kin, variant, flux=None, dh4=0.0):
    good = p["goodA"] if variant == "A" else p["goodB"]; f = p["flux"] if flux is None else flux; st = kin_start(kin, dh4)
    pa = ppxf(tpl, f, p["noise"], VELSCALE, st, moments=6, fixed=[1] * 6, degree=-1, mdegree=10, goodpixels=good, lam=p["lam"], lam_temp=lam_t, quiet=True)
    chi2a = float(pa.chi2); mp = pa.mpoly
    pb = ppxf(tpl.reshape(tpl.shape[0], *REG_DIM), f / mp, p["noise"] / mp * np.sqrt(chi2a), VELSCALE, st, moments=6, fixed=[1] * 6, degree=-1,
              mdegree=0, regul=100, reg_dim=REG_DIM, goodpixels=good, lam=p["lam"], lam_temp=lam_t, quiet=True)
    return dict(wa=np.asarray(pa.weights, float).ravel(), wb=np.asarray(pb.weights, float).ravel(), chi2a=chi2a, chi2b=float(pb.chi2), mpoly=mp,
                bestfit=pb.bestfit * mp, good=good)
def summary(w, n_t):
    T = tlib(); s = w.sum()
    g = float(np.sum(w * T["gamma"]) / s); la = float(np.sum(w * np.log10(T["age"] * 1e9)) / s); mh = float(np.sum(w * T["metal"]) / s)
    edge = float(w[(np.abs(T["gamma"] - 0.30) < 1e-9) | (np.abs(T["gamma"] - 3.50) < 1e-9)].sum() / s)
    m = w / n_t; L = np.sum(m * T["Lr"]); alpha = float(np.sum(m * T["mass"]) / np.sum(m * T["Lr"] * T["ups_r13"]))
    ia = int(np.argmin(np.abs(np.log10(T["tab_age"]) + 9 - la))); im = int(np.argmin(np.abs(T["tab_mh"] - mh)))
    return dict(gamma=g, lage=la, mh=mh, edge=edge, alpha=alpha, alpha_ku2=alpha * float(T["ratio_CH"][ia, im]), alpha_tian=alpha * float(T["ratio_KU"][ia, im]),
                ref_age=float(T["tab_age"][ia]), ref_mh=float(T["tab_mh"][im]))
def window_resid(p, res):
    out = {}; good = np.zeros(len(p["lam"]), bool); good[res["good"]] = True
    for k, (a, b) in RESW.items():
        q = good & (p["lam"] >= a) & (p["lam"] <= b)
        out[k] = float(np.mean((p["flux"][q] - res["bestfit"][q]) / res["bestfit"][q])) if q.any() else float("nan")
    return out

# ---------------------------------------------------------------- safe JSONL helpers (job contract: fsync, torn last line dropped)
def read_jsonl(fn, repair=False):
    """Parsed lines; a torn line is skipped. repair=True (own file only, before appending) rewrites the file without it."""
    if not os.path.exists(fn): return []
    out, bad = [], 0
    for l in open(fn):
        if not l.strip(): continue
        try: out.append(json.loads(l))
        except Exception: bad += 1
    if bad and repair:
        tmp = fn + ".tmp"
        with open(tmp, "w") as fo:
            for r in out: fo.write(json.dumps(r) + "\n")
            fo.flush(); os.fsync(fo.fileno())
        os.replace(tmp, fn)
    return out
def append_jsonl(fo, r): fo.write(json.dumps(r, default=float) + "\n"); fo.flush(); os.fsync(fo.fileno())
def save_npz_atomic(fn, **kw):
    tmp = fn + ".part.npz"; np.savez(tmp, **kw); os.replace(tmp, fn)
