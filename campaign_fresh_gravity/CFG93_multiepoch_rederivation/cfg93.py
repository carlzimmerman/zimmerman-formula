"""
CFG93 -- independent re-derivation of CFG51 (Walker+2023 multi-epoch, binary-cleaned UFD dispersions) and
CFG66 (Bootes I two-Gaussian mixture; Tucana II velocity gradient).            FROZEN BEFORE THE FIRST RUN.

QUESTION. Does a fresh implementation, written from the README/docstring statements only (CFG51/CFG66/CFG46/CFG78
READMEs, the docstring of CFG51's reduce_walker.py, the Walker+2023 ReadMe and the LVD table), reproduce
  Bootes I : single-epoch offset +0.310, cleaned sigma 3.91(+0.45,-0.38), cleaned offset +0.219 +/- 0.089 (2.46 sig), rule -0.205
  Tucana II: single-epoch offset +0.730, cleaned sigma 4.06(+1.16,-0.82), cleaned offset +0.465 +/- 0.128 (3.63 sig), rule -0.165
  (sigma_law 2.36 / 1.39 km/s; single 4.82 / 7.48; all-epoch mean 3.92 / 5.30; members 55(33 multi,53 clean) / 14(9,12))
and CFG66: Boo I mixture (s_cold 2.00 [1.19,2.82], s_hot 5.09 [4.09,6.64], f_hot 0.525 [0.29,0.84], total 3.94 [3.46,4.56],
LR 2.31, bootstrap P 0.155, total offset +0.222+/-0.097 (2.29 sig), cold-only -0.072+/-0.203); Tuc II gradient 2.0+/-15.9 km/s/deg,
LR 0.020, p 0.99, gradient-removed sigma 4.060(+1.164,-0.821), offset +0.464+/-0.128 (3.62 sig)?  And how fragile are the
offsets to the membership cuts, the cleaning threshold/epoch count/error floor, the binary population, and is the per-star
likelihood unbiased at N=30-100 with the real epoch cadence?
Programme rules: nothing here says the data favour the framework; kappa=1/2 is FITTED; a non-reproduction is a valid outcome.

MODEL AS READ.  sigma_law: stars only, Upsilon_V=2 (L_V from M_V, M_V,sun=4.83), half the stellar mass inside r=(4/3)R_half
(R_half = LVD angular rhalf x LVD distance, projected pc), g_N=G(M*/2)/r^2, g=g_N nu(g_N/a0), nu(y)=1/(1-exp(-sqrt y)),
sigma^2=g r/3.  a0=9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt).  Offset = log10(sigma_obs/sigma_law).
Offset error = quadrature of (i) the mean of the up and down log10 errors of the profile-likelihood 1-sigma interval and
(ii) a 0.076 dex systematic floor (the Upsilon_V floor inherited from CFG28/46; RECIPE INFERRED from the README numbers
0.089/0.128 by arithmetic before any run; it is inherited, not derived).  Rule offsets: the sum rule is NOT re-implemented
(not in the allowed reading); sigma_rule is INFERRED from the README (sigma_clean_README x 10^0.205 / 10^0.165) so the
rule rows are a consistency check only, not an independent reproduction.

DATA / MEMBERSHIP AS READ (declared, then applied once).  Fixed-width byte ranges from the Walker ReadMe. One row = one epoch.
Quality epoch: Goodobs>0, RRL==0, AGN==0, e_Vlos>0.  Epochs pooled by (Target, Gaia DR3 id) across the 3 files; rows with
no Gaia id are never members.  Star: quality epochs sorted by HJD; mean = inverse-variance mean, e_mean=1/sqrt(sum w);
logg, PM, parallax from the first quality epoch.  UFD: lower-case Target == LVD key and M_V > -7.7.  Membership per star:
(1) logg<4.0; (2) |v_mean-v_c| < 4 sqrt(sig_seed^2+e_mean^2), sig_seed=max(LVD vlos_sigma,3) (5 if missing), v_c = LVD
vlos_systemic on pass 1, then the median of pass-1 members (one recentring, membership fully recomputed); (3) PM chi2 =
dpmra^2/(e_pmra^2+s^2)+dpmde^2/(e_pmde^2+s^2) < 11.83, s^2=0.05^2+pm_err_LVD^2+(sig_seed/(4.74 d_kpc))^2 (pm_err_LVD^2 =
mean of the squared mean(em,ep) of pmra and pmdec); stars with no PM rejected; (4) |plx-1/d_kpc| < 3 sqrt(e_plx^2+0.03^2) if plx present.
Informative = n_multi>=8 and n_multi/n_members>=0.5 (n_multi = members with >=2 quality epochs).
ESTIMATORS.  -2lnL(mu,s)=sum[ln(s^2+e_i^2)+(v_i-mu)^2/(s^2+e_i^2)], mu profiled, s in [0,60]; 1-sigma interval Delta=1;
sigma_hat<1e-3 -> 0.  SINGLE = earliest-HJD quality epoch of every member.  ALLMEAN = ivar mean over quality epochs.
CLEAN = drop members with >=2 quality epochs and chi2 about their weighted mean with p<0.01 (dof=N_ep-1, own e_Vlos), then
ALLMEAN of the rest (single-epoch stars stay).  PAPERFLAG(alt) = drop f_Vlosvar==1 on any quality row.
CFG66: Boo I common-mean two-Gaussian mixture (s_cold<=s_hot, f_hot in [0,1]) on the cleaned ALLMEAN stars; multi-start ML;
profile 1-sigma intervals; T=2(lnL_mix - lnL_1G) (also quoted as raw dlnL); parametric-bootstrap P (500 draws from the
single-Gaussian MLE, same errors); total sigma=sqrt(f s_h^2+(1-f)s_c^2); cold-only offset = log10(s_cold/sigma_law) with
the s_cold profile interval + floor.  Tuc II: gnomonic tangent plane about the LVD centre (deg), v=v0+a*xi+b*eta,
profile in (a,b) (2 dof for LR), |grad| error = mean of the two component errors from the Hessian, permutation p (2000).

PASS LINES (each evaluated once, no tuning).
 R1 counts exact: n_members, n_multi, n_clean = 55,33,53 / 14,9,12.
 R2 sigmas (single, allmean, clean +up -down) within 0.005 km/s of the README values (2-decimal precision).
 R3 offsets and errors: |delta| <= 0.0006 dex = "3 decimals reproduced"; <= 0.02 = CLOSE; else DIFFERENT (stated).  Headline
    lines: cleaned offset and error, both systems.  Significance within 0.01 sigma.
 R4 sigma_law within 0.005 km/s of 2.36 / 1.39 (else both conventions are reported; verdict lines use mine).
 R5 CFG66 numbers: parameters within 0.05 km/s (f within 0.02), interval ends within 0.1, LR within 0.05, bootstrap P within
    0.04, gradient within 0.5 km/s/deg, offsets as R3.
 H1 (CFG51's science line): both cleaned offsets > 0 at > 2 sigma on both footings.  H2: cleaning lowers each offset relative
    to single-epoch but leaves it > 0.
 C1 sigma_law closed forms: Newtonian limit (a0->1e-30) sigma^2 = G M*/(8 R_half) rtol 1e-6; deep-MOND limit (a0->1e30)
    sigma^4 = G M* a0/18 rtol 1e-6.
 C2 (synthetic, no binaries) for pool in {Boo I, Tuc II real cadence} x sigma_true {2,4} x N {30,50,100}, 1500 reps: median
    sigma_hat/sigma_true within 1 +/- 0.05 for CLEAN, and the Delta=1 interval covers sigma_true in [0.60, 0.76] (12 cells).
 C3 (synthetic, binaries; DM91 log-normal period mean logP[d]=5.03 sd 2.28, q~U[0.1,1], M1=0.8, e~U[0,0.8] for logP>1 else 0,
    isotropic inclination, random phase; orbits with periastron < 3 R1, R1=15 Rsun, resampled): flag efficiency measured in a
    3000-star calibration run per pool; the recovered binary fraction f_hat=f_flag/eff must be within 0.05 of f_true at
    N=100, f_true=0.5 (both pools); AND median sigma_hat_CLEAN/sigma_true within 1 +/- 0.10 in all 8 cells
    pool x sigma_true{2,4} x N{30,100} at f_bin=0.5 (also reported: f_bin 0.3, 0.7; SINGLE and ALLMEAN estimators).
 C4 MUTATE=1: observed Vlos multiplied by 0.5 about the LVD systemic velocity (e_Vlos unchanged).  It must FAIL R3 and H1
    (exit 1); closed-form C1 still passes.  MUTATE skips the simulations and the sensitivity block.
 Exit code: 1 if any of R1-R5, H1, H2, C1-C3 fails; the printed verdict states which.

ATTACKS (reported, no pass line; a variant "flips" if any cleaned offset < 2 sigma or changes sign).
 A1 membership: velocity window 3/4/5 sigma; logg cut 3.5/4.0/4.5/none; PM 2/3/4 sigma; no parallax cut; sig_seed = 3, LVD, 5;
    no recentring.
 A2 cleaning: p threshold 0.05/0.01/0.001; require >=3 epochs; use only the first k=2,3 epochs; PAPERFLAG.
 A3 error floor: per-epoch systematic added in quadrature 0/0.5/1/2 km/s and error scale x0.8/1.2/1.5, in cleaning and likelihood.
 A4 the epoch-error calibration: distribution of chi2-p over all matched-system multi-epoch members.
 A5 nonparametric star bootstrap of sigma_clean; binary-population variants in the simulation (flat in logP, logP mean 4,
    no periastron cut).
"""
import os, sys, gzip, json, math, time, warnings
import numpy as np
import pandas as pd
from scipy import optimize, stats
from multiprocessing import Pool
warnings.filterwarnings("ignore")

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"
HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
A0 = {"canon": 9.3603e-11, "alt": 1.1312e-10}
FLOOR = 0.076
G_PC = 4.30091e-3          # pc (km/s)^2 / Msun
PC_M = 3.0856775814913673e16
NAMES = {"bootes_1": "Boo I", "tucana_2": "Tuc II"}
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

# ---------------------------------------------------------------- parsing
COLS = {"Target": (13, 28), "Gaia": (72, 90), "pmra": (188, 195), "pmde": (197, 204), "epmra": (206, 210),
        "epmde": (212, 216), "plx": (218, 224), "eplx": (226, 232), "ra": (234, 248), "de": (250, 264),
        "hjd": (282, 292), "v": (335, 341), "e": (343, 348), "logg": (416, 420), "good": (686, 687),
        "fvar": (850, 850), "rrl": (874, 874), "agn": (876, 876)}
def fl(s):
    s = s.strip()
    try: return float(s)
    except: return np.nan
def parse():
    rows = []
    for fn in ["hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"]:
        with gzip.open(os.path.join(REPO, "walker2023", fn), "rt") as f:
            for ln in f:
                if len(ln) < 876: continue
                d = {k: ln[a - 1:b] for k, (a, b) in COLS.items()}
                g = d["Gaia"].strip()
                rows.append((d["Target"].strip(), int(g) if g else -1, fl(d["pmra"]), fl(d["pmde"]), fl(d["epmra"]),
                             fl(d["epmde"]), fl(d["plx"]), fl(d["eplx"]), fl(d["ra"]), fl(d["de"]), fl(d["hjd"]),
                             fl(d["v"]), fl(d["e"]), fl(d["logg"]), fl(d["good"]), fl(d["fvar"]), fl(d["rrl"]), fl(d["agn"])))
    df = pd.DataFrame(rows, columns=["Target", "Gaia", "pmra", "pmde", "epmra", "epmde", "plx", "eplx", "ra", "de", "hjd",
                                     "v", "e", "logg", "good", "fvar", "rrl", "agn"])
    return df

def build_stars(df, lvd, vscale=1.0):
    """quality cut, pool by (Target,Gaia); returns {system: [star dict]}"""
    q = df[(df.good > 0) & (df.rrl == 0) & (df.agn == 0) & (df.e > 0) & (df.Gaia > 0)]
    out = {}
    for tgt, g in q.groupby("Target"):
        key = tgt.lower()
        if key not in lvd.index: continue
        vsys = lvd.loc[key, "vlos_systemic"]
        stars = []
        for gid, s in g.groupby("Gaia"):
            s = s.sort_values("hjd")
            v = s.v.values.astype(float); e = s.e.values.astype(float)
            if vscale != 1.0:
                v = vsys + vscale * (v - vsys)
            w = 1 / e**2
            r0 = s.iloc[0]
            stars.append(dict(t=s.hjd.values, v=v, e=e, vm=(w * v).sum() / w.sum(), em=1 / math.sqrt(w.sum()),
                              logg=r0.logg, pmra=r0.pmra, pmde=r0.pmde, epmra=r0.epmra, epmde=r0.epmde,
                              plx=r0.plx, eplx=r0.eplx, ra=r0.ra, de=r0.de, fvar=int(s.fvar.max())))
        out[key] = stars
    return out

# ---------------------------------------------------------------- membership
def pm_thresh(k): return -2 * math.log(1 - math.erf(k / math.sqrt(2)))
DEF = dict(vwin=4.0, logg=4.0, pmk=3.0, plx=True, seed="lvd3", recentre=True, pthr=0.01, kmin=2, kmax=99, esys=0.0, escale=1.0)
def lvd_err(x, a, b):
    return np.nanmean([x[a], x[b]])
def member_idx(stars, L, p):
    d_kpc = L["distance"]
    vs = L["vlos_sigma"]
    if p["seed"] == "lvd3": sig = max(vs, 3.0) if np.isfinite(vs) else 5.0
    elif p["seed"] == "3": sig = 3.0
    elif p["seed"] == "5": sig = 5.0
    else: sig = max(vs, 3.0) if np.isfinite(vs) else 5.0
    er_ra = (L["pmra_em"] + L["pmra_ep"]) / 2; er_de = (L["pmdec_em"] + L["pmdec_ep"]) / 2
    e_lvd2 = np.nanmean([er_ra**2, er_de**2]) if np.isfinite(er_ra) else 0.0
    if not np.isfinite(e_lvd2): e_lvd2 = 0.0
    s2 = 0.05**2 + e_lvd2 + (sig / (4.74 * d_kpc))**2
    thr = pm_thresh(p["pmk"])
    def sel(vc):
        m = []
        for i, s in enumerate(stars):
            if not (s["logg"] < p["logg"]): continue          # NaN logg -> rejected
            if not (abs(s["vm"] - vc) < p["vwin"] * math.sqrt(sig**2 + s["em"]**2)): continue
            if not (np.isfinite(s["pmra"]) and np.isfinite(s["pmde"]) and np.isfinite(s["epmra"]) and np.isfinite(s["epmde"])): continue
            c = (s["pmra"] - L["pmra"])**2 / (s["epmra"]**2 + s2) + (s["pmde"] - L["pmdec"])**2 / (s["epmde"]**2 + s2)
            if not (c < thr): continue
            if p["plx"] and np.isfinite(s["plx"]):
                if not (abs(s["plx"] - 1 / d_kpc) < 3 * math.sqrt(s["eplx"]**2 + 0.03**2)): continue
            m.append(i)
        return m
    m1 = sel(L["vlos_systemic"])
    if p["recentre"] and len(m1) >= 3:
        vc = float(np.median([stars[i]["vm"] for i in m1]))
        return sel(vc)
    return m1

# ---------------------------------------------------------------- likelihood
def m2lnL(s, v, e2):
    var = s * s + e2; w = 1 / var
    mu = (w * v).sum() / w.sum()
    return np.log(var).sum() + ((v - mu)**2 * w).sum()
def fit_sigma(v, e, precise=True, smax=None):
    v = np.asarray(v, float); e2 = np.asarray(e, float)**2
    n = len(v)
    if smax is None: smax = max(15.0, 6 * (v.std() + 1e-9))
    grid = np.concatenate([[0.0], np.linspace(1e-3, smax, 1200)])
    var = grid[:, None]**2 + e2[None, :]; w = 1 / var
    mu = (w * v).sum(1) / w.sum(1)
    f = np.log(var).sum(1) + ((v[None, :] - mu[:, None])**2 * w).sum(1)
    j = int(np.argmin(f))
    if j == 0 or f[0] - f[j] < 1e-12:
        if j == 0: sh = 0.0
    if precise and 0 < j < len(grid) - 1:
        r = optimize.minimize_scalar(lambda s: m2lnL(s, v, e2), bounds=(grid[j - 1], grid[j + 1]), method="bounded",
                                     options=dict(xatol=1e-9))
        sh = float(r.x); fmin = r.fun
        if f[0] < fmin: sh, fmin = 0.0, f[0]
    else:
        sh, fmin = float(grid[j]), f[j]
        if 0 < j < len(grid) - 1:                # parabolic
            a, b, c = f[j - 1], f[j], f[j + 1]; den = a - 2 * b + c
            if den > 0:
                sh = grid[j] + 0.5 * (a - c) / den * (grid[1] - grid[0]); fmin = b - 0.125 * (a - c)**2 / den
    if sh < 1e-3: sh = 0.0; fmin = m2lnL(0.0, v, e2)
    # interval
    def h(s): return m2lnL(s, v, e2) - fmin - 1.0
    up = dn = None
    ok = np.where(grid > sh)[0]
    cr = ok[f[ok] - fmin > 1.0]
    if len(cr):
        k = cr[0]
        up = (optimize.brentq(h, max(sh, grid[k - 1]), grid[k], xtol=1e-9) if precise else grid[k - 1] + (grid[k] - grid[k - 1]) * (1 + fmin - f[k - 1]) / (f[k] - f[k - 1])) if k > 0 else None
    if sh > 0:
        lo = np.where((grid < sh) & (f - fmin > 1.0))[0]
        if len(lo):
            k = lo[-1]
            dn = optimize.brentq(h, grid[k], min(sh, grid[k + 1]), xtol=1e-9) if precise else grid[k] + (grid[k + 1] - grid[k]) * (f[k] - fmin - 1) / (f[k] - f[k + 1])
        else: dn = 0.0
    return dict(s=sh, up=None if up is None else up - sh, dn=None if dn is None else sh - dn, lo=dn, hi=up, m2=fmin, n=n)

# ---------------------------------------------------------------- estimators on a star list
def prep(star, p):
    k = p["kmax"]
    v = star["v"][:k]; e = star["e"][:k]; t = star["t"][:k]
    if p["esys"] > 0 or p["escale"] != 1.0: e = np.sqrt((e * p["escale"])**2 + p["esys"]**2)
    return t, v, e
def star_stats(v, e):
    w = 1 / e**2; m = (w * v).sum() / w.sum()
    return m, 1 / math.sqrt(w.sum()), (w * (v - m)**2).sum()
def estimators(stars, idx, p, precise=True):
    S = [prep(stars[i], p) for i in idx]
    # SINGLE
    v1 = np.array([s[1][0] for s in S]); e1 = np.array([s[2][0] for s in S])
    # ALLMEAN
    am = [star_stats(s[1], s[2]) for s in S]
    vm = np.array([a[0] for a in am]); em = np.array([a[1] for a in am])
    nep = np.array([len(s[1]) for s in S])
    pv = np.array([stats.chi2.sf(a[2], n - 1) if n >= p["kmin"] else 1.0 for a, n in zip(am, nep)])
    keep = pv >= p["pthr"]
    res = dict(n_members=len(idx), n_multi=int((nep >= 2).sum()), n_flag=int((~keep).sum()), n_clean=int(keep.sum()),
               vm=vm[keep], em=em[keep], keep=keep)
    res["single"] = fit_sigma(v1, e1, precise); res["allmean"] = fit_sigma(vm, em, precise)
    res["clean"] = fit_sigma(vm[keep], em[keep], precise)
    fv = np.array([stars[i]["fvar"] for i in idx]) == 0
    res["paperflag"] = fit_sigma(vm[fv], em[fv], precise); res["n_pf"] = int(fv.sum())
    return res

# ---------------------------------------------------------------- the law
def nu(y): return 1 / (1 - np.exp(-np.sqrt(y)))
def sigma_law(MV, rhalf_arcmin, d_kpc, a0, ups=2.0):
    Lv = 10**(0.4 * (4.83 - MV)); Ms = ups * Lv
    R = rhalf_arcmin / 60 * math.pi / 180 * d_kpc * 1e3
    r = 4 / 3 * R; Mb = Ms / 2
    gN = G_PC * Mb / r**2                       # (km/s)^2/pc
    a0p = a0 * PC_M / 1e6
    g = gN * nu(gN / a0p)
    return math.sqrt(g * r / 3), Ms, R
def off_err(fit, sl):
    s = fit["s"]
    if s <= 0: return None
    up = math.log10((s + fit["up"]) / s) if fit["up"] is not None else np.nan
    dn = math.log10(s / (s - fit["dn"])) if (fit["dn"] is not None and fit["dn"] < s) else np.nan
    stat = np.nanmean([up, dn])
    return math.log10(s / sl), math.sqrt(stat**2 + FLOOR**2), stat

# ================================================================ CFG66 follow-ups: mixture and gradient
def mix_m2(mu, sc, sh, f, v, e2):
    v1 = sc * sc + e2; v2 = sh * sh + e2
    l1 = (1 - f) * np.exp(-0.5 * (v - mu)**2 / v1) / np.sqrt(v1)
    l2 = f * np.exp(-0.5 * (v - mu)**2 / v2) / np.sqrt(v2)
    return -2 * np.log(np.maximum(l1 + l2, 1e-300)).sum() + len(v) * math.log(2 * math.pi)
def fit_mix(v, e2, nstart=36, rng=None):
    """free (mu, s_hot, r=s_cold/s_hot, f_hot) ML, multi-start"""
    mu0 = float(np.average(v, weights=1 / (v.var() + e2)))
    best = None
    starts = [(sc, sh, f) for sc in (0.3, 1.5, 3.0) for sh in (4.0, 6.0, 10.0, 20.0) for f in (0.2, 0.5, 0.8)][:nstart]
    s1 = fit_sigma(v, np.sqrt(e2), False)["s"]     # BUGFIX after first run: start at the single-Gaussian point (nested model => T>=0)
    starts = starts + [("one", s1, None)]
    for sc, sh, f in starts:
        x0 = [mu0, max(sh, 0.06), 0.999, 0.5] if sc == "one" else [mu0, sh, min(sc / sh, 1.0), f]
        r = optimize.minimize(lambda x: mix_m2(x[0], x[1] * x[2], x[1], x[3], v, e2), x0,
                              bounds=[(mu0 - 25, mu0 + 25), (0.05, 80), (0, 1), (0, 1)], method="L-BFGS-B")
        if best is None or r.fun < best.fun: best = r
    mu, sh, r_, f = best.x
    return dict(m2=best.fun, mu=mu, sh=sh, sc=sh * r_, f=f)
def prof_mix(kind, x, v, e2, mu0):
    """profile -2lnL with one derived quantity fixed"""
    best = np.inf
    if kind == "cold":
        for d0 in (0.5, 3.0, 8.0):
            for f0 in (0.3, 0.7):
                r = optimize.minimize(lambda z: mix_m2(z[0], x, x + z[1], z[2], v, e2), [mu0, d0, f0],
                                      bounds=[(mu0 - 25, mu0 + 25), (0, 80), (0, 1)], method="L-BFGS-B")
                best = min(best, r.fun)
    elif kind == "hot":
        for r0 in (0.1, 0.4, 0.8):
            for f0 in (0.3, 0.7):
                r = optimize.minimize(lambda z: mix_m2(z[0], x * z[1], x, z[2], v, e2), [mu0, r0, f0],
                                      bounds=[(mu0 - 25, mu0 + 25), (0, 1), (0, 1)], method="L-BFGS-B")
                best = min(best, r.fun)
    elif kind == "f":
        for sh0 in (4.0, 8.0):
            for r0 in (0.1, 0.4, 0.8):
                r = optimize.minimize(lambda z: mix_m2(z[0], z[1] * z[2], z[1], x, v, e2), [mu0, sh0, r0],
                                      bounds=[(mu0 - 25, mu0 + 25), (0.05, 80), (0, 1)], method="L-BFGS-B")
                best = min(best, r.fun)
    elif kind == "tot":
        for u0 in (0.1, 0.5, 0.9):
            for f0 in (0.3, 0.7, 1.0):
                def fun(z):
                    mu, u, f = z; sc = u * x; sh = x * math.sqrt(max((1 - (1 - f) * u * u) / f, 1e-12))
                    return mix_m2(mu, sc, sh, f, v, e2)
                r = optimize.minimize(fun, [mu0, u0, f0], bounds=[(mu0 - 25, mu0 + 25), (0, 1), (1e-3, 1)], method="L-BFGS-B")
                best = min(best, r.fun)
    return best
def interval_from_profile(xs, ys, ymin, xhat):
    d = ys - ymin - 1.0
    lo = None; hi = None
    for i in range(len(xs) - 1):
        if d[i] * d[i + 1] < 0 or d[i] == 0:
            xc = xs[i] + (xs[i + 1] - xs[i]) * (-d[i]) / (d[i + 1] - d[i])
            if xc < xhat and (lo is None or xc > lo): lo = xc
            if xc > xhat and hi is None: hi = xc
    if lo is None and d[0] <= 0: lo = xs[0]
    if hi is None and d[-1] <= 0: hi = xs[-1]
    return lo, hi
def _boot_one(args):
    seed, mu, sg, e2 = args
    rng = np.random.default_rng(seed)
    v = mu + rng.normal(size=len(e2)) * np.sqrt(sg**2 + e2)
    one = fit_sigma(v, np.sqrt(e2), precise=False)["m2"] + len(v) * math.log(2 * math.pi)
    mx = fit_mix(v, e2, nstart=12)["m2"]
    return one - mx
def cfg66_boo(vm, em, sl, pool):
    e2 = em**2
    one = fit_sigma(vm, em)
    one_m2 = one["m2"] + len(vm) * math.log(2 * math.pi)
    mu1 = float(np.average(vm, weights=1 / (one["s"]**2 + e2)))
    mx = fit_mix(vm, e2)
    T = one_m2 - mx["m2"]
    stot = math.sqrt(mx["f"] * mx["sh"]**2 + (1 - mx["f"]) * mx["sc"]**2)
    out = dict(one_sigma=one["s"], mix=mx, T=T, dlnL=T / 2, stot=stot)
    grids = dict(cold=np.linspace(0.0, 6.0, 61), hot=np.linspace(2.0, 25.0, 116), f=np.linspace(0.0, 1.0, 51), tot=np.linspace(2.5, 6.5, 81))
    hat = dict(cold=mx["sc"], hot=mx["sh"], f=mx["f"], tot=stot)
    for k, g in grids.items():
        ys = np.array([prof_mix(k, x, vm, e2, mx["mu"]) for x in g])
        # also allow the global minimum to be lower than mx if the profile finds better (report)
        lo, hi = interval_from_profile(g, ys, min(mx["m2"], ys.min()), hat[k])
        out[k + "_int"] = (lo, hi); out[k + "_profmin"] = float(ys.min())
    args = [(1000 + b, mu1, one["s"], e2) for b in range(500)]
    with Pool(min(16, os.cpu_count() or 4)) as pl: Tb = np.array(pl.map(_boot_one, args))
    out["boot_P"] = float((Tb >= T).mean()); out["boot_med"] = float(np.median(Tb)); out["boot_n"] = 500
    out["boot_P_raw_negatives"] = int((Tb < 0).sum())
    return out
def tangent(ra, de, ra0, de0):
    r = np.radians(ra - ra0); d = np.radians(de); d0 = math.radians(de0)
    c = np.sin(d0) * np.sin(d) + np.cos(d0) * np.cos(d) * np.cos(r)
    xi = np.cos(d) * np.sin(r) / c; eta = (np.cos(d0) * np.sin(d) - np.sin(d0) * np.cos(d) * np.cos(r)) / c
    return np.degrees(xi), np.degrees(eta)
def grad_fit(v, e, xi, eta, with_grad=True, smax=30.0):
    e2 = e**2
    X = np.column_stack([np.ones_like(v)] + ([xi, eta] if with_grad else []))
    def m2(s):
        w = 1 / (s * s + e2); A = X.T @ (X * w[:, None]); b = X.T @ (w * v)
        beta = np.linalg.solve(A, b); r = v - X @ beta
        return np.log(s * s + e2).sum() + (w * r * r).sum(), beta, np.linalg.inv(A)
    grid = np.concatenate([[0.0], np.linspace(1e-3, smax, 1500)])
    f = np.array([m2(s)[0] for s in grid]); j = int(np.argmin(f))
    if 0 < j < len(grid) - 1:
        r = optimize.minimize_scalar(lambda s: m2(s)[0], bounds=(grid[j - 1], grid[j + 1]), method="bounded", options=dict(xatol=1e-9))
        sh, fm = float(r.x), r.fun
    else: sh, fm = float(grid[j]), f[j]
    hi = None; lo = None
    ok = np.where((grid > sh) & (f - fm > 1))[0]
    if len(ok): k = ok[0]; hi = optimize.brentq(lambda s: m2(s)[0] - fm - 1, grid[k - 1], grid[k])
    if sh > 0:
        lw = np.where((grid < sh) & (f - fm > 1))[0]
        lo = optimize.brentq(lambda s: m2(s)[0] - fm - 1, grid[lw[-1]], grid[lw[-1] + 1]) if len(lw) else 0.0
    _, beta, cov = m2(sh)
    return dict(s=sh, up=None if hi is None else hi - sh, dn=None if lo is None else sh - lo, m2=fm, beta=beta, cov=cov, n=len(v))

# ================================================================ simulation
RSUN_AU = 0.00465047
def sample_orbits(rng, n, pop="dm91"):
    """returns arrays P_d, ecc, K (km/s), omega, M0 ; SB1 giant primary M1=0.8, R1=15 Rsun"""
    out = {k: np.empty(0) for k in ("P", "e", "K", "w", "M0")}
    M1 = 0.8
    while len(out["P"]) < n:
        m = 4 * (n - len(out["P"])) + 16
        if pop in ("dm91", "dm91nocut"): lp = rng.normal(5.03, 2.28, m)
        elif pop == "meanlogP4": lp = rng.normal(4.0, 2.28, m)
        elif pop == "flat": lp = rng.uniform(0.5, 8.0, m)
        else: raise ValueError(pop)
        P = 10**lp
        q = rng.uniform(0.1, 1.0, m); M2 = q * M1
        e = np.where(lp > 1.0, rng.uniform(0, 0.8, m), 0.0)
        a = ((M1 + M2) * (P / 365.25)**2)**(1 / 3)
        ok = (P > 1.0) & (P < 1e10)
        if not pop.endswith("nocut"): ok &= (a * (1 - e) > 3 * 15 * RSUN_AU)
        cosi = rng.uniform(-1, 1, m); sini = np.sqrt(1 - cosi**2)
        K = 29.78 * M2 * sini / (M1 + M2)**(2 / 3) / (P / 365.25)**(1 / 3) / np.sqrt(1 - e**2)
        w = rng.uniform(0, 2 * np.pi, m); M0 = rng.uniform(0, 2 * np.pi, m)
        for k, x in zip(("P", "e", "K", "w", "M0"), (P, e, K, w, M0)): out[k] = np.concatenate([out[k], x[ok]])
    return {k: v[:n] for k, v in out.items()}
def kepler_rv(t, o):
    Mm = o["M0"] + 2 * np.pi * t / o["P"]; e = o["e"]
    E = Mm.copy()
    for _ in range(40): E = E - (E - e * np.sin(E) - Mm) / (1 - e * np.cos(E))
    nu_ = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    return o["K"] * (np.cos(nu_ + o["w"]) + e * np.cos(o["w"]))
def sim_rep(rng, pool, N, sigma, fbin, pop="dm91", pthr=0.01, want_flags=False):
    idx = rng.integers(len(pool), size=N)
    ne = np.array([len(pool[i][1]) for i in idx]); starts = np.concatenate([[0], np.cumsum(ne)[:-1]])
    T = np.concatenate([pool[i][0] - pool[i][0][0] for i in idx]); E = np.concatenate([pool[i][1] for i in idx])
    sid = np.repeat(np.arange(N), ne)
    v0 = rng.normal(0, sigma, N)
    isb = rng.random(N) < fbin; nb = int(isb.sum())
    V = v0[sid] + rng.normal(size=len(E)) * E
    if nb:
        o = sample_orbits(rng, nb, pop)
        bmap = -np.ones(N, int); bmap[isb] = np.arange(nb)
        m = isb[sid]; bi = bmap[sid[m]]
        oo = {k: v[bi] for k, v in o.items()}
        V[m] += kepler_rv(T[m], oo)
    W = 1 / E**2
    sw = np.add.reduceat(W, starts); vm = np.add.reduceat(W * V, starts) / sw; em = 1 / np.sqrt(sw)
    chi2 = np.add.reduceat(W * (V - vm[sid])**2, starts)
    pv = np.where(ne >= 2, stats.chi2.sf(chi2, np.maximum(ne - 1, 1)), 1.0)
    keep = pv >= pthr
    v1 = V[starts]; e1 = E[starts]
    res = dict(single=fit_sigma(v1, e1, False), allmean=fit_sigma(vm, em, False), clean=fit_sigma(vm[keep], em[keep], False))
    if want_flags: res["flag"] = ~keep; res["isb"] = isb; res["ne"] = ne
    return res
def cover(fit, s):
    lo = fit["lo"] if fit["lo"] is not None else 0.0
    hi = fit["hi"] if fit["hi"] is not None else np.inf
    return lo <= s <= hi
def _cell(args):
    cell, pool, N, sigma, fbin, nrep, pop, seed = args
    rng = np.random.default_rng(seed)
    r = {k: [] for k in ("single", "allmean", "clean")}; cv = {k: 0 for k in r}
    for _ in range(nrep):
        s = sim_rep(rng, pool, N, sigma, fbin, pop)
        for k in r:
            r[k].append(s[k]["s"] / sigma); cv[k] += cover(s[k], sigma)
    return dict(cell=cell, med={k: float(np.median(v)) for k, v in r.items()}, mean={k: float(np.mean(v)) for k, v in r.items()},
                p16={k: float(np.percentile(v, 16)) for k, v in r.items()}, p84={k: float(np.percentile(v, 84)) for k, v in r.items()},
                cov={k: cv[k] / nrep for k in r})
def _calib(args):
    name, pool, pop, seed, Nstar, fbin = args
    rng = np.random.default_rng(seed)
    fl_b = fl_s = nb_ = ns_ = 0; ntest_b = ntest_s = 0; fl_b_t = fl_s_t = 0
    for _ in range(Nstar // 500):
        s = sim_rep(rng, pool, 500, 3.0, fbin, pop, want_flags=True)
        f, b, ne = s["flag"], s["isb"], s["ne"]
        fl_b += (f & b).sum(); nb_ += b.sum(); fl_s += (f & ~b).sum(); ns_ += (~b).sum()
    return name, pop, float(fl_b / nb_), float(fl_s / ns_), int(nb_), int(ns_)
def _fhat_cell(args):
    name, pool, N, sigma, fbin, nrep, pop, seed, eff, fp = args
    rng = np.random.default_rng(seed); fh = []
    for _ in range(nrep):
        s = sim_rep(rng, pool, N, sigma, fbin, pop, want_flags=True)
        ff = s["flag"].mean(); fh.append((ff - fp) / (eff - fp))
    return name, float(np.mean(fh)), float(np.std(fh))

# ================================================================ main
EXPECT = {
 "bootes_1": dict(nm=55, nmulti=33, nclean=53, single=4.82, allmean=3.92, clean=3.91, cup=0.45, cdn=0.38, law=2.36,
                  off_single=0.310, off_clean=0.219, err=0.089, sig=2.46, rule=-0.205),
 "tucana_2": dict(nm=14, nmulti=9, nclean=12, single=7.48, allmean=5.30, clean=4.06, cup=1.16, cdn=0.82, law=1.39,
                  off_single=0.730, off_clean=0.465, err=0.128, sig=3.63, rule=-0.165)}
LINES = []          # (name, passed, detail)
def line(name, ok, detail=""):
    LINES.append((name, bool(ok), detail)); P(("PASS  " if ok else "FAIL  ") + name + ("  " + detail if detail else ""))
def tier(d, exact=0.0006, close=0.02):
    d = abs(d); return "EXACT" if d <= exact else ("CLOSE" if d <= close else "DIFFERENT")
def fmt(fit):
    return f"{fit['s']:.3f} (+{fit['up'] if fit['up'] is not None else float('nan'):.3f} -{fit['dn'] if fit['dn'] is not None else float('nan'):.3f})"
def run_pipeline(stars, lvd, key, p, precise=True):
    L = lvd.loc[key]
    idx = member_idx(stars[key], L, p)
    if len(idx) < 4: return None
    res = estimators(stars[key], idx, p, precise)
    sl = {k: sigma_law(L["M_V"], L["rhalf"], L["distance"], a)[0] for k, a in A0.items()}
    res["sl"] = sl; res["idx"] = idx
    for est in ("single", "allmean", "clean", "paperflag"):
        for k in A0: res[f"off_{est}_{k}"] = off_err(res[est], sl[k])
    return res

def main():
    t0 = time.time()
    P("CFG93 main   MUTATE=%s" % MUTATE)
    lvd = pd.read_csv(os.path.join(REPO, "dsph", "lvd_dwarf_mw.csv")).set_index("key")
    df = parse()
    P("rows parsed:", len(df), " systems:", df.Target.nunique())
    stars = build_stars(df, lvd, 0.5 if MUTATE else 1.0)
    # ---------- all matched systems: members, multi-epoch, informative
    P("\n== all matched systems, frozen membership ==")
    P(f"{'system':14s}{'M_V':>7s}{'UFD':>5s}{'n_mem':>7s}{'n_multi':>8s}{'info':>6s}{'sig_single':>12s}{'sig_all':>9s}{'sig_clean':>11s}")
    table = {}
    for key in sorted(stars):
        L = lvd.loc[key]; p = dict(DEF)
        idx = member_idx(stars[key], L, p); ufd = bool(L["M_V"] > -7.7)
        nmul = sum(len(stars[key][i]["v"]) >= 2 for i in idx)
        info = ufd and nmul >= 8 and nmul / max(len(idx), 1) >= 0.5
        row = dict(ufd=ufd, n=len(idx), nmulti=nmul, info=info)
        if len(idx) >= 8:
            r = estimators(stars[key], idx, p)
            row.update(single=r["single"]["s"], allmean=r["allmean"]["s"], clean=r["clean"]["s"], n_clean=r["n_clean"])
            P(f"{key:14s}{L['M_V']:7.2f}{str(ufd):>5s}{len(idx):7d}{nmul:8d}{str(info):>6s}{r['single']['s']:12.2f}{r['allmean']['s']:9.2f}{r['clean']['s']:11.2f}")
        else:
            P(f"{key:14s}{L['M_V']:7.2f}{str(ufd):>5s}{len(idx):7d}{nmul:8d}{str(info):>6s}{'(<8 members)':>32s}")
        table[key] = row
    inf = [k for k, v in table.items() if v["info"]]
    P("informative UFDs:", inf)
    line("R0 informative set == {bootes_1, tucana_2}", sorted(inf) == ["bootes_1", "tucana_2"], str(inf))
    # ---------- the two systems
    R = {}
    P("\n== the two informative systems ==")
    for key in ("bootes_1", "tucana_2"):
        ex = EXPECT[key]; res = run_pipeline(stars, lvd, key, dict(DEF)); R[key] = res
        nm = NAMES[key]
        P(f"\n--- {nm} --- members {res['n_members']} multi {res['n_multi']} flagged {res['n_flag']} clean {res['n_clean']} paperflag-kept {res['n_pf']}")
        P("sigma_law canon/alt: %.4f / %.4f   (README %.2f)" % (res["sl"]["canon"], res["sl"]["alt"], ex["law"]))
        for est in ("single", "allmean", "clean", "paperflag"):
            P(f"  {est:9s} sigma {fmt(res[est])}   offset canon {res['off_'+est+'_canon'][0]:+.4f} +/- {res['off_'+est+'_canon'][1]:.4f} ({res['off_'+est+'_canon'][0]/res['off_'+est+'_canon'][1]:.2f} sig)   alt {res['off_'+est+'_alt'][0]:+.4f} +/- {res['off_'+est+'_alt'][1]:.4f} ({res['off_'+est+'_alt'][0]/res['off_'+est+'_alt'][1]:.2f} sig)")
        oc = res["off_clean_canon"]; os_ = res["off_single_canon"]
        # R1
        line(f"R1 counts {nm}", (res["n_members"], res["n_multi"], res["n_clean"]) == (ex["nm"], ex["nmulti"], ex["nclean"]),
             f"mine {(res['n_members'], res['n_multi'], res['n_clean'])} vs README {(ex['nm'], ex['nmulti'], ex['nclean'])}")
        # R2
        ok2 = all(abs(x - y) <= 0.005 for x, y in [(res["single"]["s"], ex["single"]), (res["allmean"]["s"], ex["allmean"]),
                  (res["clean"]["s"], ex["clean"]), (res["clean"]["up"] or 0, ex["cup"]), (res["clean"]["dn"] or 0, ex["cdn"])])
        line(f"R2 sigmas {nm}", ok2, f"single {res['single']['s']:.2f}/{ex['single']}  all {res['allmean']['s']:.2f}/{ex['allmean']}  clean {fmt(res['clean'])}/{ex['clean']}(+{ex['cup']} -{ex['cdn']})")
        line(f"R4 sigma_law {nm}", abs(res["sl"]["canon"] - ex["law"]) <= 0.005, f"{res['sl']['canon']:.4f} vs {ex['law']}")
        for nmx, mine, ref in [("offset_single", os_[0], ex["off_single"]), ("offset_clean", oc[0], ex["off_clean"]), ("err_clean", oc[1], ex["err"])]:
            t = tier(mine - ref); line(f"R3 {nmx} {nm}", t == "EXACT", f"{t}: mine {mine:+.4f} vs README {ref:+.3f} (d={mine-ref:+.4f})")
        sg = oc[0] / oc[1]; line(f"R3 significance {nm}", abs(sg - ex["sig"]) <= 0.01, f"mine {sg:.3f} vs {ex['sig']}")
        # rule (inferred sigma_rule)
        srule = ex["clean"] * 10**(-ex["rule"])
        rr = math.log10(res["clean"]["s"] / srule)
        P(f"  rule (sigma_rule INFERRED from README = {srule:.3f}): mine {rr:+.4f} vs README {ex['rule']:+.3f}  [consistency only]")
        line(f"R3 rule {nm} (inferred sigma_rule; tautological-ish)", abs(rr - ex["rule"]) <= 0.0006, f"{rr:+.4f} vs {ex['rule']}")
        for k in A0:
            o = res[f"off_clean_{k}"]; P(f"  clean offset {k}: {o[0]:+.3f} +/- {o[1]:.3f} = {o[0]/o[1]:.2f} sigma")
    h1 = all(R[k][f"off_clean_{a}"][0] / R[k][f"off_clean_{a}"][1] > 2 for k in R for a in A0)
    line("H1 both cleaned offsets > 2 sigma positive, both footings", h1)
    h2 = all(0 < R[k]["off_clean_canon"][0] < R[k]["off_single_canon"][0] for k in R)
    line("H2 cleaning lowers but does not remove the offset", h2)
    # ---------- C1 closed forms
    Msun = 4.83
    L = lvd.loc["bootes_1"]; MV, ra_, dk = L["M_V"], L["rhalf"], L["distance"]
    sN, Ms, Rh = sigma_law(MV, ra_, dk, 1e-30)
    line("C1 Newtonian limit sigma^2 = G M*/(8 R_half)", abs(sN**2 / (G_PC * Ms / (8 * Rh)) - 1) < 1e-6, f"ratio {sN**2/(G_PC*Ms/(8*Rh)):.9f}")
    sD, _, _ = sigma_law(MV, ra_, dk, 1.0)   # BUGFIX after first run: a0=1e30 overflowed 1-exp(-sqrt y) to 0 (ratio inf); a0=1 m/s^2 gives y~4e-14
    line("C1 deep-MOND limit sigma^4 = G M* a0/18 (a0=1 m/s^2)", abs(sD**4 / (G_PC * Ms * (1.0 * PC_M / 1e6) / 18) - 1) < 1e-6,
         f"ratio {sD**4/(G_PC*Ms*(1.0*PC_M/1e6)/18):.9f}")
    # ---------- CFG66
    P("\n== CFG66 follow-ups ==")
    rb = R["bootes_1"]; vm, em = rb["vm"], rb["em"]; sl = rb["sl"]
    mb = cfg66_boo(vm, em, sl, None)
    mx = mb["mix"]
    P(f"Boo I 1G sigma {mb['one_sigma']:.3f}; mixture s_cold {mx['sc']:.3f} {mb['cold_int']}, s_hot {mx['sh']:.3f} {mb['hot_int']}, f_hot {mx['f']:.3f} {mb['f_int']}, total {mb['stot']:.3f} {mb['tot_int']}")
    P(f"  T=2dlnL {mb['T']:.3f} (dlnL {mb['dlnL']:.3f}); bootstrap P(T*>=T) {mb['boot_P']:.3f} of {mb['boot_n']}; boot median {mb['boot_med']:.3f}; neg T* {mb['boot_P_raw_negatives']}; mu {mx['mu']:.2f}")
    def offint(x, lo, hi, sl_):
        up = math.log10(hi / x) if hi else np.nan; dn = math.log10(x / lo) if (lo and lo > 0) else np.nan
        stat = np.nanmean([up, dn]); return math.log10(x / sl_), math.sqrt(stat**2 + FLOOR**2)
    for k in A0:
        ot = offint(mb["stot"], *mb["tot_int"], sl[k]); oc_ = offint(mx["sc"], *mb["cold_int"], sl[k])
        P(f"  {k}: total-mixture offset {ot[0]:+.3f} +/- {ot[1]:.3f} ({ot[0]/ot[1]:.2f} sig); cold-only {oc_[0]:+.3f} +/- {oc_[1]:.3f} ({oc_[0]/oc_[1]:.2f} sig)")
        if k == "canon": ot_c, oc_c = ot, oc_
    line("R5 Boo I s_cold 2.00", abs(mx["sc"] - 2.00) <= 0.05, f"{mx['sc']:.3f}")
    line("R5 Boo I s_hot 5.09", abs(mx["sh"] - 5.09) <= 0.05, f"{mx['sh']:.3f}")
    line("R5 Boo I f_hot 0.525", abs(mx["f"] - 0.525) <= 0.02, f"{mx['f']:.3f}")
    line("R5 Boo I total sigma 3.94", abs(mb["stot"] - 3.94) <= 0.05, f"{mb['stot']:.3f}")
    line("R5 Boo I intervals cold [1.19,2.82] hot [4.09,6.64] f [0.29,0.84] tot [3.46,4.56]",
         all(a is not None and b is not None and abs(a - c) <= 0.1 and abs(b - d) <= 0.1 for (a, b), (c, d) in
             [(mb["cold_int"], (1.19, 2.82)), (mb["hot_int"], (4.09, 6.64)), (mb["f_int"], (0.29, 0.84)), (mb["tot_int"], (3.46, 4.56))]),
         f"cold {mb['cold_int']} hot {mb['hot_int']} f {mb['f_int']} tot {mb['tot_int']}")
    line("R5 Boo I LR 2.31", abs(mb["T"] - 2.31) <= 0.05, f"T {mb['T']:.3f}, dlnL {mb['dlnL']:.3f}")
    line("R5 Boo I bootstrap P 0.155", abs(mb["boot_P"] - 0.155) <= 0.04, f"{mb['boot_P']:.3f}")
    line("R5 Boo I total-mixture offset +0.222+/-0.097", abs(ot_c[0] - 0.222) <= 0.0006 and abs(ot_c[1] - 0.097) <= 0.0006, f"{ot_c[0]:+.4f} +/- {ot_c[1]:.4f}")
    line("R5 Boo I cold-only offset -0.072+/-0.203", abs(oc_c[0] + 0.072) <= 0.0006 and abs(oc_c[1] - 0.203) <= 0.0006, f"{oc_c[0]:+.4f} +/- {oc_c[1]:.4f}")
    # Tucana II
    rt = R["tucana_2"]; L = lvd.loc["tucana_2"]
    ids = rt["idx"]; kept = [ids[j] for j in range(len(ids)) if rt["keep"][j]]
    xi, eta = tangent(np.array([stars["tucana_2"][i]["ra"] for i in kept]), np.array([stars["tucana_2"][i]["de"] for i in kept]), L["ra"], L["dec"])
    vt, et = rt["vm"], rt["em"]
    g0 = grad_fit(vt, et, xi, eta, False); g1 = grad_fit(vt, et, xi, eta, True)
    a_, b_ = g1["beta"][1], g1["beta"][2]; ca, cb = math.sqrt(g1["cov"][1, 1]), math.sqrt(g1["cov"][2, 2])
    LR = g0["m2"] - g1["m2"]; pLR = float(stats.chi2.sf(max(LR, 0), 2))
    rng = np.random.default_rng(93); nperm = 2000; LRp = []; sp = []
    for _ in range(nperm):
        pi = rng.permutation(len(vt)); gp = grad_fit(vt, et, xi[pi], eta[pi], True, smax=15.0)
        LRp.append(g0["m2"] - gp["m2"]); sp.append(gp["s"])
    pperm = float((np.array(LRp) >= LR).mean())
    P(f"\nTuc II: {len(vt)} stars; 0-grad sigma {fmt(g0)}; grad sigma {fmt(g1)}; a={a_:+.2f}+/-{ca:.2f} b={b_:+.2f}+/-{cb:.2f} km/s/deg; |g|={math.hypot(a_, b_):.2f}; LR {LR:.4f} p(chi2_2) {pLR:.3f} p_perm {pperm:.3f}; perm median sigma {np.median(sp):.2f}; 1D-error candidates: mean {np.mean([ca, cb]):.1f}, quad {math.hypot(ca, cb):.1f}, geo {math.sqrt(ca*cb):.1f}")
    for k in A0:
        o = off_err(g1, rt["sl"][k]); P(f"  {k}: gradient-removed offset {o[0]:+.3f} +/- {o[1]:.3f} ({o[0]/o[1]:.2f} sig)")
        if k == "canon": og = o
    line("R5 Tuc II gradient |g| 2.0+/-15.9 km/s/deg", abs(math.hypot(a_, b_) - 2.0) <= 0.5 and abs(np.mean([ca, cb]) - 15.9) <= 0.5,
         f"|g| {math.hypot(a_, b_):.2f}; errors {ca:.1f},{cb:.1f}")
    line("R5 Tuc II LR 0.020 / p 0.99", abs(LR - 0.020) <= 0.05 and abs(pLR - 0.99) <= 0.02, f"LR {LR:.4f} p {pLR:.3f}")
    line("R5 Tuc II gradient-removed sigma 4.060 (+1.164 -0.821)", abs(g1["s"] - 4.060) <= 0.005 and abs(g1["up"] - 1.164) <= 0.005 and abs(g1["dn"] - 0.821) <= 0.005, fmt(g1))
    line("R5 Tuc II gradient-removed offset +0.464+/-0.128", abs(og[0] - 0.464) <= 0.0006 and abs(og[1] - 0.128) <= 0.0006, f"{og[0]:+.4f} +/- {og[1]:.4f}")
    OUT = dict(table=table, mix=dict(mb), grad=dict(a=a_, b=b_, ca=ca, cb=cb, LR=LR, pLR=pLR, pperm=pperm))
    OUT["R"] = {k: {kk: vv for kk, vv in R[k].items() if kk in ("n_members", "n_multi", "n_flag", "n_clean", "single", "allmean", "clean", "paperflag", "sl",
                "off_single_canon", "off_clean_canon", "off_clean_alt", "off_single_alt", "off_allmean_canon", "off_paperflag_canon")} for k in R}
    if MUTATE:
        P("\nMUTATE run: simulations and sensitivity skipped by declaration.")
        return finish(OUT, t0)
    sensitivity(stars, lvd, OUT, table)
    simulations(stars, lvd, R, OUT)
    return finish(OUT, t0)

def finish(OUT, t0):
    nfail = sum(1 for _, ok, _ in LINES if not ok)
    P("\n== verdict ==")
    P("lines failed: %d of %d" % (nfail, len(LINES)))
    for n, ok, d in LINES:
        if not ok: P("  FAILED:", n)
    P("elapsed %.1f s" % (time.time() - t0))
    tag = "_MUTATE" if MUTATE else ""
    json.dump(OUT, open(os.path.join(HERE, f"cfg93_results{tag}.json"), "w"), default=lambda o: (o.tolist() if hasattr(o, "tolist") else str(o)), indent=1)
    open(os.path.join(HERE, f"cfg93{tag}.out"), "w").write("\n".join(LOG) + "\n")
    return 1 if nfail else 0

# ================================================================ attacks on the real data
def variants():
    V = [("BASE", {})]
    V += [(f"vwin={x}", dict(vwin=x)) for x in (3.0, 5.0)]
    V += [(f"logg<{x}", dict(logg=x)) for x in (3.5, 4.5, 99.0)]
    V += [(f"PM {x} sig", dict(pmk=x)) for x in (2.0, 4.0)]
    V += [("no parallax cut", dict(plx=False)), ("sig_seed=3", dict(seed="3")), ("sig_seed=5", dict(seed="5")), ("no recentring", dict(recentre=False))]
    V += [(f"clean p<{x}", dict(pthr=x)) for x in (0.05, 0.001)]
    V += [("clean only stars with >=3 epochs", dict(kmin=3)), ("first 2 epochs only", dict(kmax=2)), ("first 3 epochs only", dict(kmax=3))]
    V += [(f"eps floor {x} km/s", dict(esys=x)) for x in (0.5, 1.0, 2.0)]
    V += [(f"err x{x}", dict(escale=x)) for x in (0.8, 1.2, 1.5)]
    return V
def sensitivity(stars, lvd, OUT, table):
    P("\n== A1-A3 sensitivity (cleaned offset, canon; flip = any cleaned offset <2 sigma or <0 on either footing) ==")
    P(f"{'variant':34s}| {'system':6s}{'nmem':>5s}{'nmul':>5s}{'ncl':>4s}{'s_single':>9s}{'s_all':>7s}{'s_clean':>8s}{'off_clean':>10s}{'err':>7s}{'sig':>6s}{'sigAlt':>7s}  paperflag_off flip")
    OUT["variants"] = {}
    for lab, ov in variants():
        p = dict(DEF); p.update(ov)
        for key in ("bootes_1", "tucana_2"):
            r = run_pipeline(stars, lvd, key, p)
            if r is None: P(f"{lab:34s}| {NAMES[key]:6s} too few members"); continue
            oc, oa, op = r["off_clean_canon"], r["off_clean_alt"], r["off_paperflag_canon"]
            flip = (oc[0] / oc[1] < 2) or (oa[0] / oa[1] < 2)
            P(f"{lab:34s}| {NAMES[key]:6s}{r['n_members']:5d}{r['n_multi']:5d}{r['n_clean']:4d}{r['single']['s']:9.2f}{r['allmean']['s']:7.2f}{r['clean']['s']:8.2f}{oc[0]:+10.3f}{oc[1]:7.3f}{oc[0]/oc[1]:6.2f}{oa[0]/oa[1]:7.2f}  {op[0]:+.3f}         {'FLIP' if flip else ''}")
            OUT["variants"][f"{lab}|{key}"] = dict(n=r["n_members"], nmulti=r["n_multi"], ncl=r["n_clean"], clean=r["clean"]["s"], off=oc[0], err=oc[1])
    # epoch structure of the members
    P("\n== epoch structure of the members (quality epochs per star; baseline in days) ==")
    for key in ("bootes_1", "tucana_2"):
        r = run_pipeline(stars, lvd, key, dict(DEF)); ne = np.array([len(stars[key][i]["v"]) for i in r["idx"]])
        base = np.array([np.ptp(stars[key][i]["t"]) for i in r["idx"]])
        P(f"  {NAMES[key]}: N_epoch histogram {dict(zip(*np.unique(ne, return_counts=True)))}; baseline (multi) median {np.median(base[ne>=2]):.0f} d, max {base.max():.0f} d; median e_Vlos first epoch {np.median([stars[key][i]['e'][0] for i in r['idx']]):.2f} km/s")
    # A4 error calibration
    P("\n== A4 epoch-error calibration: chi2 p-values of members (all matched systems, frozen membership) ==")
    ps = {"2": [], "3-4": [], ">=5": []}; rc = []
    for key in stars:
        L = lvd.loc[key]; idx = member_idx(stars[key], L, dict(DEF))
        for i in idx:
            s = stars[key][i]; n = len(s["v"])
            if n < 2: continue
            m, em_, c2 = star_stats(s["v"], s["e"]); pv = stats.chi2.sf(c2, n - 1)
            ps["2" if n == 2 else ("3-4" if n <= 4 else ">=5")].append(pv); rc.append(c2 / (n - 1))
    for k, v in ps.items():
        v = np.array(v)
        if len(v): P(f"  N_epoch {k:4s}: n={len(v):4d}  frac p<0.01 {np.mean(v<0.01):.3f}  p<0.05 {np.mean(v<0.05):.3f}  p<0.5 {np.mean(v<0.5):.3f}  (pure-Gaussian expectation 0.010 / 0.050 / 0.500)")
    P(f"  median chi2/dof of all multi-epoch members {np.median(rc):.3f} (pure-Gaussian median for N_epoch=2 is 0.455)")
    OUT["A4"] = {k: [float(np.mean(np.array(v) < 0.01)), len(v)] for k, v in ps.items() if len(v)}
    # A5 bootstrap over members including cleaning
    P("\n== A5 nonparametric bootstrap over members (cleaning re-run in each draw, 500 draws) ==")
    rng = np.random.default_rng(5)
    for key in ("bootes_1", "tucana_2"):
        r = run_pipeline(stars, lvd, key, dict(DEF)); ids = np.array(r["idx"]); sh = []
        for _ in range(500):
            b = rng.choice(ids, size=len(ids), replace=True)
            e = estimators(stars[key], list(b), dict(DEF), precise=False); sh.append(e["clean"]["s"])
        sh = np.array(sh); sl = r["sl"]["canon"]
        P(f"  {NAMES[key]}: sigma_clean bootstrap median {np.median(sh):.2f} [16,84] {np.percentile(sh,16):.2f}-{np.percentile(sh,84):.2f}; offset median {math.log10(np.median(sh)/sl):+.3f} [{math.log10(np.percentile(sh,16)/sl):+.3f}, {math.log10(np.percentile(sh,84)/sl):+.3f}]; profile interval {r['clean']['s']-r['clean']['dn']:.2f}-{r['clean']['s']+r['clean']['up']:.2f}")
        OUT["boot_" + key] = [float(np.median(sh)), float(np.percentile(sh, 16)), float(np.percentile(sh, 84))]

# ================================================================ simulations
def simulations(stars, lvd, R, OUT):
    P("\n== simulations with the real epoch cadence ==")
    pools = {}
    for key in ("bootes_1", "tucana_2"):
        pools[NAMES[key]] = [(stars[key][i]["t"], stars[key][i]["e"]) for i in R[key]["idx"]]
        ne = np.array([len(x[1]) for x in pools[NAMES[key]]])
        P(f"  pool {NAMES[key]}: {len(ne)} stars, single-epoch {int((ne==1).sum())}, epochs/star mean {ne.mean():.2f}")
    npr = min(16, os.cpu_count() or 4)
    # C2
    P("\nC2: no binaries, CLEAN estimator (1500 reps/cell); SINGLE and ALLMEAN identical in expectation")
    cells = []; sd = 100
    for nm, pool in pools.items():
        for sg in (2.0, 4.0):
            for N in (30, 50, 100):
                sd += 1; cells.append(((nm, sg, N, 0.0), pool, N, sg, 0.0, 1500, "dm91", sd))
    with Pool(npr) as pl: res = pl.map(_cell, cells)
    ok = True
    P(f"{'pool':6s}{'sig':>5s}{'N':>5s} | {'med clean':>9s}{'mean':>7s}{'p16':>6s}{'p84':>6s}{'cov clean':>10s} | med single/all  cov single/all")
    for c in res:
        nm, sg, N, _ = c["cell"]; m = c["med"]["clean"]; cv = c["cov"]["clean"]
        good = abs(m - 1) <= 0.05 and 0.60 <= cv <= 0.76; ok &= good
        P(f"{nm:6s}{sg:5.1f}{N:5d} | {m:9.3f}{c['mean']['clean']:7.3f}{c['p16']['clean']:6.2f}{c['p84']['clean']:6.2f}{cv:10.3f} | {c['med']['single']:.3f}/{c['med']['allmean']:.3f}   {c['cov']['single']:.3f}/{c['cov']['allmean']:.3f} {'' if good else '<-- outside pass line'}")
    line("C2 no-binary recovery (12 cells: median within 5%, coverage 0.60-0.76)", ok)
    OUT["C2"] = res
    # C3 calibration
    P("\nC3 calibration of the flagging (injected DM91 binaries, 20000 stars/pool at f=0.5)")
    cal = {}
    with Pool(npr) as pl:
        out = pl.map(_calib, [(nm, pool, "dm91", 7 + j, 20000, 0.5) for j, (nm, pool) in enumerate(pools.items())])
    for nm, pop, eff, fp, nb_, ns_ in out:
        cal[nm] = (eff, fp); P(f"  {nm}: P(flag|binary) = {eff:.3f} (n={nb_}); P(flag|single) = {fp:.4f} (n={ns_}); the 1% false-positive rate applies only to multi-epoch stars")
    OUT["calib"] = {k: list(v) for k, v in cal.items()}
    with Pool(npr) as pl:
        fh = pl.map(_fhat_cell, [(nm, pool, 100, 4.0, 0.5, 400, "dm91", 900 + j, cal[nm][0], cal[nm][1]) for j, (nm, pool) in enumerate(pools.items())])
    okf = True
    for nm, m, s in fh:
        good = abs(m - 0.5) <= 0.05; okf &= good
        P(f"  recovered f_hat (N=100, f_true=0.5, matching model, 400 reps) {nm}: {m:.3f} +/- {s:.3f} (sd of one realisation) {'' if good else '<-- outside'}")
    P("  (sensitivity: the same f_hat with a mismatched population is not a pass line; see A5 below)")
    # C3 sigma recovery
    P("\nC3: sigma recovery with binaries (1000 reps/cell); ratios sigma_hat/sigma_true")
    cells = []; sd = 500
    for f in (0.3, 0.5, 0.7):
        for nm, pool in pools.items():
            for sg in (2.0, 4.0):
                for N in (30, 100):
                    sd += 1; cells.append(((nm, sg, N, f), pool, N, sg, f, 1000, "dm91", sd))
    with Pool(npr) as pl: res = pl.map(_cell, cells)
    P(f"{'f':>4s}{'pool':>7s}{'sig':>5s}{'N':>5s} | {'CLEAN med':>9s}{'p16':>6s}{'p84':>6s}{'cov':>6s} | {'ALL med':>7s}{'cov':>6s} | {'SINGLE med':>10s}{'cov':>6s}")
    ok8 = True
    for c in res:
        nm, sg, N, f = c["cell"]; m = c["med"]["clean"]
        if f == 0.5: ok8 &= abs(m - 1) <= 0.10
        P(f"{f:4.1f}{nm:>7s}{sg:5.1f}{N:5d} | {m:9.3f}{c['p16']['clean']:6.2f}{c['p84']['clean']:6.2f}{c['cov']['clean']:6.2f} | {c['med']['allmean']:7.3f}{c['cov']['allmean']:6.2f} | {c['med']['single']:10.3f}{c['cov']['single']:6.2f}{'   <-- clean outside +/-10%' if (f==0.5 and abs(m-1)>0.10) else ''}")
    OUT["C3"] = res
    line("C3a recovered binary fraction within 0.05 (both pools, matching model)", okf, str([(a, round(b, 3)) for a, b, _ in fh]))
    line("C3b median sigma_clean/sigma_true within 10% in all 8 f=0.5 cells", ok8)
    # A5 population variants
    P("\nA5 binary-population variants (Boo I cadence, sigma_true 4, N=50, f=0.5, 1000 reps)")
    cells = [((pop,), pools["Boo I"], 50, 4.0, 0.5, 1000, pop, 800 + j) for j, pop in enumerate(("dm91", "dm91nocut", "meanlogP4", "flat"))]
    with Pool(npr) as pl: res = pl.map(_cell, cells)
    for c in res:
        P(f"  {c['cell'][0]:10s} CLEAN med {c['med']['clean']:.3f} [{c['p16']['clean']:.2f},{c['p84']['clean']:.2f}] cov {c['cov']['clean']:.2f} | ALL {c['med']['allmean']:.3f} | SINGLE {c['med']['single']:.3f}")
    OUT["A5pop"] = res
    P("\nA5 the same with sigma_true 2 (Tuc-like) and Tuc II cadence, N=30")
    cells = [((pop,), pools["Tuc II"], 30, 2.0, 0.5, 1000, pop, 850 + j) for j, pop in enumerate(("dm91", "dm91nocut", "meanlogP4", "flat"))]
    with Pool(npr) as pl: res = pl.map(_cell, cells)
    for c in res:
        P(f"  {c['cell'][0]:10s} CLEAN med {c['med']['clean']:.3f} [{c['p16']['clean']:.2f},{c['p84']['clean']:.2f}] cov {c['cov']['clean']:.2f} | ALL {c['med']['allmean']:.3f} | SINGLE {c['med']['single']:.3f}")

if __name__ == "__main__":
    sys.exit(main())
