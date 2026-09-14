#!/usr/bin/env python3
"""G049 -- THE SAG DECOMPOSITION: what drives the RAR's outer sag?

THE OPEN QUESTION (G036/G044 registered): the RAR residual decomposes as
per-galaxy offset + white per-point noise (0.045-0.052 dex within-galaxy) +
a small ONE-SIGN outer sag -- per-galaxy deep-regime (r/r_M > 2) slope of
delta = log10(g_obs/g_th) vs log10(r/r_M), population mean -0.13 dex/dex
(t = -4 sigma, binomial p ~ 1e-3, most galaxies negative).  G040 killed the
physics-variable reading of the OFFSET; the SAG is the remaining UNEXPLAINED
coherent structure.  This lane decomposes it.

CANDIDATES (pre-registered order in G049_preregistration.md, FROZEN before
any G049 residual was computed):
  (a) radial M/L gradient ups(r) = ups0 + ups1*(r/Rd)  -- THE STRONGEST.
      dln g_bar = dln ups pointwise (exact, multiplicative at fixed
      components).  Two-parameter per-galaxy fit: ups0 in [0.2,1.2] (the
      registered Lelli+16 population range, G013/G040) x ups1 in [-0.5,+0.5]
      per disc scale length (the pre-set plausibility band), against the
      WHOLE curve with the same pooled-dex objective as G013/G040.
      Rd from SPARC_Lelli2016c.mrt (3.6-micron disc scale length).
  (b) the G031 matched law at finite Y: g^2 = a0*C(Y)*g_N with
      C(Y) = 2(1+Y)^2/(2+Y), Y = g_bar/(2a0); C(Y->0) = 1 exactly (G031 V7).
      The frozen pre-registration logged an arithmetic correction (first
      draft C(1)=3/2, exact 8/3) BEFORE any galaxy residual was computed;
      the lane measures the C-vs-mu2 offset profile numerically.
  (c) HI truncation / outermost-point artifacts: drop the outermost 2
      DEEP-REGIME points of each curve, refit; plus the errV/V < 10% cut.
  (d) the EFE at the high-eN tail is NOT re-run (G036 V4e + G044 V2E closed
      it at SPARC amplitudes); e_N is carried as a consistency column only.

VERDICT GATES (frozen):
  (a) KILLS the sag iff  (i) |mean deep slope| < 0.05 dex/dex with the
      gradient fitted, on BOTH footings; (ii) the within-galaxy white-noise
      floor does not degrade by more than 0.005 dex; (iii) > 80% of fitted
      ups1 interior to [-0.5,+0.5].  HEADLINE if (a) fires: the sag WAS the
      radial M/L gradient and the priced RAR precision floor is the
      gradient-fit white-noise floor, stated against the registered
      0.150/0.174-dex deep totals and 0.045-0.052-dex within-galaxy floor.
  (b)/(c) absorb a MATERIAL share iff |mean| < 0.075 (more than half) with
      the floor intact.
  If NO candidate (alone or combined) reaches |mean| < 0.05 with the floor
  intact: the sag is UNEXPLAINED residual structure -- ESCALATED as the
  theory's sharpest open anomaly.  Both outcomes are findings.

CORPORA: SPARC-175 (G036's exact ingest, the V0 anchor; candidate (a) is
SPARC-only because only SPARC carries the Vgas/Vdisk/Vbul decomposition a
gradient needs) + the G044 v7 extended Tier-1 set (crossmatched curves
inherit their SPARC baryon model by registered interpolation) for (b)/(c).
"""
import glob, json, math, os, re, sys
import numpy as np
from scipy import stats as sstats
from scipy.optimize import minimize, minimize_scalar

RES, NP_, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP_ += 1
    else: NF += 1

print(__doc__)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")
CORPUS = os.path.join(HERE, "data", "rotation_curve_corpus_v7.json")
MRT = os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")
GEXT = os.path.join(REPO, "gext_vectors_2026", "data", "gext_vectors.csv")

# ------------------------------------------------------------------ constants
G = 6.674e-11
KMS = 1.0e3
kpc = 3.0857e19
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
UPS_D, UPS_B = 0.5, 0.7            # repo standing SPARC M/L convention
UPS_LO, UPS_HI = 0.2, 1.2          # Lelli+16 population range (G013/G040)
UP1_LO, UP1_HI = -0.5, 0.5         # pre-registered plausibility band
DEEP = 2.0                         # G036's deep-regime boundary
SAG_KILL = 0.05                    # |mean slope| below this = sag killed
SAG_HALF = 0.075                   # material-share threshold for (b)/(c)
FLOOR_TOL = 0.005                  # allowed white-noise-floor degradation, dex

def mu2(x): return 1.0 - (1.0 + x/2.0)**(-2.0)

def _bisect(tgt, s_val, it=200):
    """solve mu_2(g/s) g = tgt by the certified bisection."""
    tgt = np.asarray(tgt, dtype=float)
    lo = np.maximum(tgt, 1e-300)
    hi = tgt + np.sqrt(np.maximum(tgt, 0)*s_val)*3 + 1e-13
    for _ in range(it):
        mid = 0.5*(lo + hi)
        fm = mid*(1.0 - (1.0 + mid/s_val)**(-2.0)) - tgt
        lo = np.where(fm < 0, mid, lo); hi = np.where(fm < 0, hi, mid)
    return 0.5*(lo + hi)

def g_pred_mu2(gb, s_val):  return _bisect(gb, s_val)

def g_pred_C(gb, s_val):
    """finite-Y matched law: g*mu_2(g/s) = C(Y)*g_bar, Y = g_bar/s,
    C(Y) = 2(1+Y)^2/(2+Y)  [C(Y->0)=1: G031's matched-law deep branch]."""
    gb = np.asarray(gb, dtype=float)
    C = 2.0*(1.0 + gb/s_val)**2 / (2.0 + gb/s_val)
    return _bisect(C*gb, s_val)

# ------------------------------------------------------------------ Rdisk
def parse_rdisk():
    """SPARC_Lelli2016c.mrt: Rdisk = token 11 of 19 (F5.2, kpc).

    The data block sits between the LAST '----' rule and the 'Note' lines;
    every row is exactly 19 whitespace tokens (verified: 175/175, names
    contain no spaces -- ESO-style names are hyphenated), so token indexing
    beats the advertised byte columns (rows are indented; the fixed-width
    slice landed off-column and read the wrong field)."""
    lines = open(MRT, errors="replace").read().splitlines()
    idx = max(i for i, L in enumerate(lines) if L.startswith("----"))
    rd = {}
    for line in lines[idx+1:]:
        if line.startswith("Note") or not line.strip(): break
        tok = line.split()
        if len(tok) != 19: continue
        try: rd[tok[0]] = float(tok[11])
        except ValueError: rd[tok[0]] = float("nan")
    return rd

RDISK = parse_rdisk()
print(f"Rdisk parsed for {sum(np.isfinite(v) for v in RDISK.values())} SPARC galaxies")

# ------------------------------------------------------------------ ingest
def load_sparc():
    gals = []
    for path in sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat"))):
        name = os.path.basename(path).replace("_rotmod.dat", "")
        try: d = np.genfromtxt(path, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vo, ev = d[:, 0], d[:, 1], d[:, 2]
        Vg, Vd, Vb = d[:, 3], d[:, 4], d[:, 5]
        m = (R > 0) & np.isfinite(Vo) & (Vo > 0) & np.isfinite(Vg) & np.isfinite(Vd) & np.isfinite(Vb)
        if m.sum() < 5: continue
        R, Vo, ev, Vg, Vd, Vb = R[m], Vo[m], ev[m], Vg[m], Vd[m], Vb[m]
        Vg2, Vd2, Vb2 = Vg*np.abs(Vg), Vd*np.abs(Vd), Vb*np.abs(Vb)
        Vb2c = Vg2 + UPS_D*Vd2 + UPS_B*Vb2
        ok = Vb2c > 0
        if ok.sum() < 5: continue
        Menc = (np.sqrt(Vb2c[ok])*KMS)**2 * (R[ok]*kpc) / G
        gals.append(dict(name=name, R=R[ok], Vo=Vo[ok], errV=ev[ok],
                         Vg2=Vg2[ok], Vd2=Vd2[ok], Vb2s=Vb2[ok], Vb2c=Vb2c[ok],
                         Mb=float(Menc.max()), Rd=RDISK.get(name, float("nan"))))
    return gals

def norm_name(n):
    n = re.sub(r"[^A-Z0-9]", "", str(n).upper())
    return re.sub(r"(?<=[A-Z])0+", "", n)

def load_extended():
    """G044's Tier-1 extended set, harmonized to the G036 schema."""
    corpus = json.load(open(CORPUS))
    sparc_rows = {g["galaxy"]: g for g in corpus["galaxies"] if g["survey"] == "SPARC"}
    models = {}
    for name, g in sparc_rows.items():
        rows = g["data"]
        R = np.array([r["Rad"] for r in rows])
        Vg = np.array([r["Vgas"] for r in rows])
        Vd = np.array([r["Vdisk"] for r in rows])
        Vb = np.array([r["Vbul"] for r in rows])
        Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
        ok = Vb2 > 0
        if ok.sum() < 5: continue
        Menc = (np.sqrt(Vb2[ok])*KMS)**2 * (R[ok]*kpc) / G
        models[norm_name(name)] = dict(R_mod=R[ok], Vb2_mod=Vb2[ok], Mb=float(Menc.max()))
    curves = []
    for g in corpus["galaxies"]:
        sv, name, data = g["survey"], g["galaxy"], (g.get("data") or [])
        if not data: continue
        if sv == "SPARC":
            mk = models.get(norm_name(name))
            if mk is None: continue
            R = np.array([r["Rad"] for r in data]); Vo = np.array([r["Vobs"] for r in data])
            ev = np.array([r["errV"] for r in data])
            Vg = np.array([r["Vgas"] for r in data]); Vd = np.array([r["Vdisk"] for r in data])
            Vb = np.array([r["Vbul"] for r in data])
            Vg2, Vd2, Vb2s = Vg*np.abs(Vg), Vd*np.abs(Vd), Vb*np.abs(Vb)
            Vb2c = Vg2 + UPS_D*Vd2 + UPS_B*Vb2s
            ok = (Vb2c > 0) & (R > 0) & np.isfinite(Vo) & (Vo > 0)
            if ok.sum() < 5: continue
            curves.append(dict(name=name, survey="SPARC", model="own",
                               R=R[ok], Vo=Vo[ok], errV=ev[ok],
                               Vg2=Vg2[ok], Vd2=Vd2[ok], Vb2s=Vb2s[ok], Vb2c=Vb2c[ok],
                               Mb=mk["Mb"], Rd=RDISK.get(name, float("nan"))))
        elif sv in ("THINGS", "LITTLE_THINGS"):
            mk = models.get(norm_name(name))
            if mk is None: continue
            R = np.array([r["Rad"] for r in data])
            Vo = np.array([r["Vrot"] if "Vrot" in r else r["Vobs"] for r in data])
            ev = np.array([r.get("e_Vrot", r.get("errV", np.nan)) for r in data])
            ok = (R > 0) & np.isfinite(Vo) & (Vo > 0)
            if ok.sum() < 5: continue
            R, Vo, ev = R[ok], Vo[ok], ev[ok]
            Vb2_hi = np.interp(R, mk["R_mod"], mk["Vb2_mod"])  # registered: linear interp
            curves.append(dict(name=name, survey=sv, model="inherited(SPARC)",
                               R=R, Vo=Vo, errV=ev, Vb2c=Vb2_hi,
                               Mb=mk["Mb"], Rd=float("nan")))
    return curves

def join_env(names):
    env = {}
    with open(GEXT) as f:
        f.readline()
        for line in f:
            cols = line.strip().split(",")
            if len(cols) < 5: continue
            try: env[norm_name(cols[0])] = 10.0**float(cols[4])
            except ValueError: continue
    return {g: env[g] for g in env}

ENV = {}
with open(GEXT) as f:
    f.readline()
    for line in f:
        cols = line.strip().split(",")
        if len(cols) < 5: continue
        try: ENV[norm_name(cols[0])] = 10.0**float(cols[4])
        except ValueError: continue

# ------------------------------------------------------------------ residuals
def deep_seq(g, foot, law="mu2", qcut=False):
    """deep-regime (r/rM > DEEP) residual sequence, radius-ordered."""
    a0 = A0[foot]; s_val = 2.0*a0
    r = g["R"]*kpc
    gbar = g["Vb2c"]*KMS**2/r
    gobs = g["Vo"]**2*KMS**2/r
    gp = (g_pred_mu2 if law == "mu2" else g_pred_C)(gbar, s_val)
    delta = np.log10(gobs/gp)
    rM = math.sqrt(G*g["Mb"]/a0)/kpc
    sel = (g["R"]/rM > DEEP) & np.isfinite(delta)
    if qcut: sel &= (g["errV"]/g["Vo"] < 0.10)
    if sel.sum() < 3: return None
    x = np.log10(g["R"][sel]/rM)
    o = np.argsort(x)
    return x[o], delta[sel][o], rM

def slope_of(x, y):
    if len(x) < 3 or np.ptp(x) <= 0.05: return None
    return float(np.polyfit(x, y, 1)[0])

def sag_stats(gals, foot, law="mu2", drop_last=0, qcut=False):
    """population sag statistics: per-galaxy deep slopes -> mean/sd/t/binomial."""
    slopes, within = [], []
    for g in gals:
        sq = deep_seq(g, foot, law, qcut)
        if sq is None: continue
        x, dd, _ = sq
        if drop_last > 0:
            if len(x) - drop_last < 3: continue
            x, dd = x[:len(x)-drop_last], dd[:len(dd)-drop_last]
        sl = slope_of(x, dd)
        if sl is None: continue
        slopes.append(sl)
        within.append(float(np.sqrt(np.mean((dd - np.mean(dd))**2))))
    if len(slopes) < 5: return None
    sl = np.array(slopes)
    tt = sstats.ttest_1samp(sl, 0.0)
    p_tt = float(tt.pvalue) if hasattr(tt, "pvalue") else float(tt[1])
    nneg = int(np.sum(sl < 0))
    return dict(mean=float(np.mean(sl)), sd=float(np.std(sl, ddof=1)),
                t=float(np.mean(sl)/sstats.sem(sl)), p_tt=p_tt,
                nneg=nneg, n=len(sl),
                p_bin=float(sstats.binomtest(nneg, len(sl), 0.5).pvalue),
                med_within=float(np.median(within)))

# ================================================================== PART 0
print("PART 0 -- V0 CONTROL: reproduce G036's registered sag on the SPARC ingest")
sparc = load_sparc()
print(f"    SPARC ingest: {len(sparc)} galaxies, "
      f"{sum(len(g['R']) for g in sparc)} rotation points")
V0 = {}
for foot in A0:
    st = sag_stats(sparc, foot, "mu2")
    V0[foot] = st
    print(f"    [{foot}] sag mean {st['mean']:+.4f} dex/dex "
          f"({st['nneg']}/{st['n']} negative, p_bin = {st['p_bin']:.2g}), t = {st['t']:+.2f}")
v0_ok = (abs(V0["canonical"]["mean"] + 0.13) < 0.04
         and abs(V0["alt"]["mean"] + 0.14) < 0.04
         and 120 <= V0["canonical"]["n"] <= 155)
check("V0 REPRODUCE THE REGISTERED SAG (G036 anchor): mean deep-regime slope "
      "-0.13/-0.14 dex/dex, N in [120,155], on the SPARC ingest",
      f"canonical {V0['canonical']['mean']:+.4f} dex/dex (N = {V0['canonical']['n']}), "
      f"alt {V0['alt']['mean']:+.4f} (N = {V0['alt']['n']})",
      v0_ok,
      "same ingest, residual definition and slope fit as G036's V4d; a miss "
      "invalidates every downstream comparison")

# ================================================================== PART 1
print()
print("PART 1 -- candidate (a): the radial M/L gradient ups(r) = ups0 + ups1*r/Rd")

def fit_ml(g, foot, law="mu2", grad=False):
    """per-galaxy M/L fit on the WHOLE curve (the G013/G040 pooled-dex objective).

    constant: Vb2 = Vg2 + ups*Vd2 + 0.7*Vb2s.
    gradient: ups(r) = ups0 + ups1*(r/Rd) per point (kept > 0.05), two params.
    Returns dict(ups0, ups1, slope=deep slope at best fit, within=deep
    residual-about-galaxy-mean rms, rms=pooled whole-curve rms, pinned)."""
    a0 = A0[foot]; s_val = 2.0*a0
    R, Vo = g["R"], g["Vo"]
    r = R*kpc
    gobs = Vo**2*KMS**2/r
    rd = g.get("Rd", float("nan"))
    rRd = (R/rd) if (np.isfinite(rd) and rd > 0) else np.zeros_like(R)

    def delta_of(U0, U1=0.0):
        # linear gradient with a positivity floor: ups0 + ups1*r/Rd can go
        # negative in the outer disk (the cliff sits at ups1 ~ -0.06 for
        # Rmax/Rd ~ 8), which would abort every fit; the floor keeps the
        # pre-registered linear parameterization valid pointwise.  A fit
        # that WANTS to sit on the floor is scored by the plausibility gate.
        ups = np.maximum(U0 + U1*rRd, 0.05)
        Vb2 = g["Vg2"] + ups*g["Vd2"] + UPS_B*g["Vb2s"]
        kk = Vb2 > 0
        if kk.sum() < 5: return None
        gp = (g_pred_mu2 if law == "mu2" else g_pred_C)(Vb2[kk]*KMS**2/r[kk], s_val)
        dl = np.full(Vo.shape, np.nan)
        dl[kk] = np.log10(gobs[kk]) - np.log10(gp)
        return dl

    def obj(p):
        p = np.atleast_1d(np.asarray(p, dtype=float))
        dl = delta_of(p[0], p[1] if grad else 0.0)
        if dl is None: return 9.9
        m = np.isfinite(dl)
        if m.sum() < 5: return 9.9
        return float(np.sqrt(np.mean(dl[m]**2)))

    if not grad:
        res = minimize_scalar(obj, bounds=(UPS_LO, UPS_HI), method="bounded",
                              options={"xatol": 0.005})
        u0, u1 = float(res.x), 0.0
    else:
        best = None
        for u1_0 in (-0.3, -0.1, 0.0, 0.1, 0.3):
            r_ = minimize(obj, np.array([0.5, u1_0]), method="L-BFGS-B",
                          bounds=[(UPS_LO, UPS_HI), (UP1_LO, UP1_HI)],
                          options={"maxiter": 200})
            if best is None or r_.fun < best.fun: best = r_
        if best is None: return None
        u0, u1 = float(best.x[0]), float(best.x[1])
    dl = delta_of(u0, u1 if grad else 0.0)
    if dl is None: return None
    rM = math.sqrt(G*g["Mb"]/a0)/kpc
    sel = (R/rM > DEEP) & np.isfinite(dl)
    sl = within = float("nan")
    if sel.sum() >= 3:
        x = np.log10(R[sel]/rM); o = np.argsort(x)
        sl = slope_of(x[o], dl[sel][o])
        within = float(np.sqrt(np.mean((dl[sel] - np.mean(dl[sel]))**2)))
    return dict(name=g["name"], ups0=u0, ups1=u1, slope=sl, within=within, rM=rM,
                rms=float(obj(np.array([u0, u1 if grad else 0.0]))),
                deep_pts=(dl[sel] if (sel.sum() >= 3 and np.isfinite(dl).any()) else
                          np.array([])))

FITS = {}
def get_fits(foot, law="mu2", grad=False):
    key = (foot, law, grad)
    if key not in FITS:
        FITS[key] = [f for f in (fit_ml(g, foot, law, grad=grad) for g in SPARC_RD) if f]
    return FITS[key]

SPARC_RD = [g for g in sparc if np.isfinite(g["Rd"]) and g["Rd"] > 0]
print(f"    galaxies with a parsed Rdisk: {len(SPARC_RD)}/{len(sparc)} "
      f"(candidate (a) runs on these; the rest are excluded with count recorded)")

grad_res = {}
for foot in A0:
    fits_c = [f for f in (fit_ml(g, foot, "mu2", grad=False) for g in SPARC_RD) if f]
    fits_g = [f for f in (fit_ml(g, foot, "mu2", grad=True)  for g in SPARC_RD) if f]
    sc = np.array([np.nan if f["slope"] is None else f["slope"] for f in fits_c])
    sg = np.array([np.nan if f["slope"] is None else f["slope"] for f in fits_g])
    wc = np.array([f["within"] for f in fits_c])
    wg = np.array([f["within"] for f in fits_g])
    u1 = np.array([f["ups1"] for f in fits_g])
    ok_sl_c = np.isfinite(sc); ok_sl_g = np.isfinite(sg)
    def pooled_within(fits):
        arrs = [np.asarray(f["deep_pts"], float) for f in fits if len(f["deep_pts"]) >= 2]
        if not arrs: return float("nan")
        w = np.concatenate([a - a.mean() for a in arrs])
        return float(np.sqrt(np.mean(w**2)))
    pool_c, pool_g = pooled_within(fits_c), pooled_within(fits_g)
    n_g = int(ok_sl_g.sum())
    if n_g >= 5:
        tt = sstats.ttest_1samp(sg[ok_sl_g], 0.0)
        p_tt = float(tt.pvalue) if hasattr(tt, "pvalue") else float(tt[1])
    else:
        p_tt = float("nan")
    nneg = int(np.sum(sg[ok_sl_g] < 0))
    grad_res[foot] = dict(
        n_gal=len(fits_g), mean_g=float(np.mean(sg[ok_sl_g])) if n_g else float("nan"),
        sd_g=float(np.std(sg[ok_sl_g], ddof=1)) if n_g > 1 else float("nan"),
        t_g=float(np.mean(sg[ok_sl_g])/sstats.sem(sg[ok_sl_g])) if n_g > 1 else float("nan"),
        p_g=p_tt,
        nneg_g=nneg, n_slope=n_g,
        p_bin_g=float(sstats.binomtest(nneg, n_g, 0.5).pvalue) if n_g else float("nan"),
        mean_c=float(np.mean(sc[ok_sl_c])), n_slope_c=int(ok_sl_c.sum()),
        med_within_c=float(np.median(wc[ok_sl_g])),
        med_within_g=float(np.median(wg[ok_sl_g])),
        pooled_within_c=pool_c, pooled_within_g=pool_g,
        ups1_med=float(np.median(u1)), ups1_sd=float(np.std(u1, ddof=1)),
        ups1_frac_interior=float(np.mean(np.abs(u1) < 0.495)),
        ups1_pinned_lo=int(np.sum(u1 <= UP1_LO + 0.005)),
        ups1_pinned_hi=int(np.sum(u1 >= UP1_HI - 0.005)))
    r = grad_res[foot]
    print(f"    [{foot}] N = {r['n_gal']}")
    print(f"      fixed-M/L sag mean   {r['mean_c']:+.4f} dex/dex (N = {r['n_slope_c']})")
    print(f"      gradient sag mean    {r['mean_g']:+.4f} +/- {r['sd_g']/math.sqrt(max(r['n_slope'],1)):.4f}"
          f" (t = {r['t_g']:+.2f}, p = {r['p_g']:.2g}; {r['nneg_g']}/{r['n_slope']} negative,"
          f" p_bin = {r['p_bin_g']:.2g})")
    print(f"      deep within-galaxy floor: fixed {r['med_within_c']:.4f} -> gradient {r['med_within_g']:.4f} dex")
    print(f"      ups1: median {r['ups1_med']:+.3f}, sd {r['ups1_sd']:.3f}, "
          f"interior {100*r['ups1_frac_interior']:.0f}%, pinned lo/hi {r['ups1_pinned_lo']}/{r['ups1_pinned_hi']}")

# ---- candidate (a) verdict gates, both footings
grad_fits_sag = all(abs(grad_res[f]["mean_g"]) < SAG_KILL for f in A0)
floor_kept = all(grad_res[f]["med_within_g"] >= grad_res[f]["med_within_c"] - FLOOR_TOL
                 and grad_res[f]["pooled_within_g"] >= grad_res[f]["pooled_within_c"] - FLOOR_TOL
                 for f in A0)
plaus = min(grad_res[f]["ups1_frac_interior"] for f in A0) > 0.80
kill_a = grad_fits_sag and floor_kept and plaus
det_a = "; ".join(
    f"{f}: sag mean {grad_res[f]['mean_c']:+.4f} -> {grad_res[f]['mean_g']:+.4f} dex/dex "
    f"(t = {grad_res[f]['t_g']:+.2f}, p = {grad_res[f]['p_g']:.2g}); floor "
    f"{grad_res[f]['med_within_c']:.4f} -> {grad_res[f]['med_within_g']:.4f} dex; "
    f"ups1 median {grad_res[f]['ups1_med']:+.3f} +/- {grad_res[f]['ups1_sd']:.3f}, "
    f"interior {100*grad_res[f]['ups1_frac_interior']:.0f}%, "
    f"pinned {grad_res[f]['ups1_pinned_lo']}lo/{grad_res[f]['ups1_pinned_hi']}hi"
    for f in A0)
check("A1 GRADIENT-KILL: with ups(r) fitted the population-mean deep sag drops to "
      "|mean| < 0.05 dex/dex on BOTH footings",
      det_a, grad_fits_sag,
      "the pre-registered kill clause (i): the sag's population mean must vanish "
      "within errors when the two-parameter gradient model is fitted")
check("A2 NOISE-FLOOR PRESERVATION: the within-galaxy deep white-noise floor does "
      f"not degrade by more than {FLOOR_TOL} dex under the gradient model "
      "(pooled offset-removed rms, the registered statistic; median shown too)",
      "; ".join(f"{f}: pooled {grad_res[f]['pooled_within_c']:.4f} -> "
                f"{grad_res[f]['pooled_within_g']:.4f} dex "
                f"(delta {grad_res[f]['pooled_within_g']-grad_res[f]['pooled_within_c']:+.4f}); "
                f"median {grad_res[f]['med_within_c']:.4f} -> {grad_res[f]['med_within_g']:.4f}"
                for f in A0), floor_kept,
      "a gradient that 'fixes' the sag by eating the noise floor is overfitting, "
      "not physics -- the registered 0.045-0.052-dex floor must survive")
check("A3 PLAUSIBILITY: > 80% of fitted ups1 interior to [-0.5, +0.5] per Rd",
      "; ".join(f"{f}: interior {100*grad_res[f]['ups1_frac_interior']:.0f}% "
                f"(pinned at bounds: {grad_res[f]['ups1_pinned_lo']} lo / "
                f"{grad_res[f]['ups1_pinned_hi']} hi of {grad_res[f]['n_gal']})"
                for f in A0), plaus,
      "values pinned at the plausibility bound mean the fit wants unphysical "
      "gradients -- the candidate then fails its own plausibility clause")

# ---- the priced floor (headline material, measured either way)
print()
print("PART 1b -- THE PRICED RAR PRECISION (both models, whole deep ledger)")
priced = {}
for foot in A0:
    a0 = A0[foot]
    # pooled deep-regime residual about 0 at fixed M/L (the 0.174/0.150 comparator)
    pts_fix = np.concatenate([deep_seq(g, foot, "mu2")[1] for g in SPARC_RD
                              if deep_seq(g, foot, "mu2") is not None])
    # gradient-fit pooled deep residual about 0 (reuse the cached fits)
    pts_g = []
    for f_ in get_fits(foot, "mu2", grad=True):
        if not np.isfinite(f_["slope"]):
            continue
        pts_g.append(np.asarray(f_["deep_pts"], dtype=float))
    pts_g = np.concatenate(pts_g)
    # line-detrended within-galaxy floor (offset + linear drift removed)
    within_lin = []
    for g in SPARC_RD:
        sq = deep_seq(g, foot, "mu2")
        if sq is None: continue
        x, dd, _ = sq
        if len(x) < 4: continue
        b, a1 = np.polyfit(x, dd, 1)
        within_lin.append(dd - (a1 + b*x))
    within_lin = np.concatenate(within_lin)
    priced[foot] = dict(
        pooled_fixed=float(np.sqrt(np.mean(pts_fix**2))),
        pooled_grad=float(np.sqrt(np.mean(pts_g**2))),
        med_within_fixed=grad_res[foot]["med_within_c"],
        med_within_grad=grad_res[foot]["med_within_g"],
        pooled_within_lin=float(np.sqrt(np.mean(within_lin**2))),
        n_deep_fix=int(len(pts_fix)), n_deep_grad=int(len(pts_g)))
    p = priced[foot]
    print(f"    [{foot}] pooled deep rms: fixed M/L {p['pooled_fixed']:.4f} -> "
          f"gradient {p['pooled_grad']:.4f} dex (registered comparators 0.174/0.150); "
          f"within-galaxy floor {p['med_within_fixed']:.4f} -> {p['med_within_grad']:.4f}; "
          f"pooled within-galaxy (offset+line removed) {p['pooled_within_lin']:.4f} dex "
          f"(N = {p['n_deep_grad']})")

# ================================================================== PART 2
print()
print("PART 2 -- candidate (b): the G031 matched law at finite Y, C(Y)=2(1+Y)^2/(2+Y)")
ext = load_extended()
n_inh = sum(1 for c in ext if c["model"] != "own")
print(f"    Tier-1 extended set: {len(ext)} curves ({n_inh} crossmatched, inheriting "
      f"their SPARC model) -- candidate (b) runs on SPARC curves only "
      f"(component decomposition needed); crossmatched set reserved for (c)")

# the C-vs-mu2 offset profile: where does the matched law sit, at what Y?
a0 = A0["canonical"]; s_val = 2.0*a0
yy, off = [], []
for g in SPARC_RD:
    r_ = g["R"]*kpc
    gb = g["Vb2c"]*KMS**2/r_
    Y = gb/s_val
    k = (Y > 1e-4) & (Y < 30) & (g["R"]/(math.sqrt(G*g["Mb"]/a0)/kpc) > DEEP)
    if k.sum() == 0: continue
    gp_mu2 = g_pred_mu2(gb[k], s_val)
    gp_C = g_pred_C(gb[k], s_val)
    yy.append(Y[k]); off.append(np.log10(gp_C/gp_mu2))
yy = np.concatenate(yy); off = np.concatenate(off)
prof = []
for lo in (0.01, 0.1, 0.3, 1.0, 3.0, 10.0):
    k = (yy >= lo) & (yy < lo*10)
    if k.sum(): prof.append(f"Y~{lo:g}: {np.median(off[k]):+.4f} dex (n={int(k.sum())})")
print("    bare C-law vs bare mu2, deep-regime offset profile (median): " + "; ".join(prof))
print(f"    deep-regime Y range: median {np.median(yy):.3f}, "
      f"10-90th pct [{np.percentile(yy,10):.3f}, {np.percentile(yy,90):.3f}]")

match_res = {}
for foot in A0:
    s_mu2 = np.array([np.nan if f["slope"] is None else f["slope"]
                      for f in get_fits(foot, "mu2", grad=False)])
    s_C = np.array([np.nan if f["slope"] is None else f["slope"]
                    for f in get_fits(foot, "C", grad=False)])
    s_Cg = np.array([np.nan if f["slope"] is None else f["slope"]
                     for f in get_fits(foot, "C", grad=True)])
    wc = np.array([f["within"] for f in get_fits(foot, "C", grad=False)])
    wg = np.array([f["within"] for f in get_fits(foot, "C", grad=True)])
    w_mu2 = np.array([f["within"] for f in get_fits(foot, "mu2", grad=False)])
    match_res[foot] = dict(
        mean_const=float(np.nanmean(s_C)), mean_grad=float(np.nanmean(s_Cg)),
        floor_const=float(np.nanmedian(wc)), floor_grad=float(np.nanmedian(wg)),
        floor_mu2_const=float(np.nanmedian(w_mu2)))
    r = match_res[foot]
    print(f"    [{foot}] deep sag mean: mu2-fixed {np.nanmean(s_mu2):+.4f} -> "
          f"C-law fixed {r['mean_const']:+.4f} -> C-law + gradient {r['mean_grad']:+.4f} dex/dex")
    print(f"          deep within-floor: mu2 {r['floor_mu2_const']:.4f} -> C {r['floor_const']:.4f} dex")

# ================================================================== PART 3
print()
print("PART 3 -- candidate (c): HI truncation / outermost-point artifacts")
trunc_res, qcut_res = {}, {}
for foot in A0:
    st0 = sag_stats(ext, foot, "mu2")
    st2 = sag_stats(ext, foot, "mu2", drop_last=2)
    stq = sag_stats(ext, foot, "mu2", qcut=True)
    if st0 is None or st2 is None or stq is None:
        print(f"    [{foot}] insufficient sequences on the extended set -- ABORT")
        sys.exit(1)
    trunc_res[foot] = (st0, st2, stq)
    print(f"    [{foot}] Tier-1 ({len(ext)} curves): full {st0['mean']:+.4f} "
          f"({st0['nneg']}/{st0['n']} neg, p_bin {st0['p_bin']:.2g}) -> "
          f"outer-2-dropped {st2['mean']:+.4f} ({st2['nneg']}/{st2['n']} neg, "
          f"p_bin {st2['p_bin']:.2g}) -> errV<10% cut {stq['mean']:+.4f} "
          f"({stq['nneg']}/{stq['n']} neg)")

# ================================================================== PART 4
print()
print("PART 4 -- consistency column: e_N vs sag slope (NO verdict -- candidate (d) "
      "is closed by G036 V4e + G044 V2E)")
eN_reg = {}
for g in SPARC_RD:
    e = ENV.get(norm_name(g["name"]))
    if e is not None: eN_reg[g["name"]] = e
for foot in A0:
    smap = {f["name"]: f["slope"] for f in get_fits(foot, "mu2", grad=True)}
    xs, ys = [], []
    for nm, e in eN_reg.items():
        sl_ = smap.get(nm)
        if sl_ is None or not np.isfinite(sl_): continue
        xs.append(math.log10(e)); ys.append(sl_)
    if len(xs) > 10:
        sl, ic, rr, p_, se = sstats.linregress(np.array(xs), np.array(ys))
        print(f"    [{foot}] d(slope)/d log10 eN = {sl:+.4f} +/- {se:.4f} "
              f"(p = {p_:.3f}, N = {len(xs)}) -- consistency read only")

# ================================================================== PART 5
print()
print("PART 5 -- THE VERDICT")
b_abs = min(abs(match_res[f]["mean_grad"]) for f in A0)
c_abs = min(abs(trunc_res[f][1]["mean"]) for f in A0)
a_str = "KILLED" if kill_a else "SURVIVES"
b_str = "material" if b_abs < SAG_HALF else "immaterial"
c_str = "material" if c_abs < SAG_HALF else "immaterial"
verdict_txt = (f"(a) {a_str} (|mean| after gradient = "
               f"{min(abs(grad_res[f]['mean_g']) for f in A0):.4f} dex/dex, "
               f"floor kept = {floor_kept}, plausible = {plaus}); "
               f"(b) {b_str} (C-law+gradient min |mean| = {b_abs:.4f}); "
               f"(c) {c_str} (outer-2-dropped min |mean| = {c_abs:.4f})")
if kill_a:
    final_ok = True
    final_read = ("PRE-REGISTERED HEADLINE FIRES: the outer sag was the radial M/L "
                  "gradient all along. The RAR residual prices as per-galaxy M/L "
                  "surface + radial gradient + white noise, and the priced RAR "
                  "precision is the gradient-fit floor reported in PART 1b -- "
                  "tighter than the registered 0.150/0.174-dex deep totals once "
                  "the gradient is charged to the baryon model, with the "
                  "0.045-0.052-dex within-galaxy white-noise floor intact.")
elif b_abs < SAG_HALF or c_abs < SAG_HALF:
    final_ok = True
    who = "(b) matched law" if b_abs < SAG_HALF else "(c) truncation"
    final_ok = True
    final_read = (f"PRE-REGISTERED MATERIAL-SHARE OUTCOME: {who} absorbs more than "
                  f"half the sag (min |mean| = {min(b_abs, c_abs):.4f} dex/dex); the "
                  "residual unexplained share is stated in the measured line.")
else:
    final_ok = False
    final_read = ("PRE-REGISTERED ESCALATION: no candidate (gradient, matched law, "
                  "truncation) reduces the population-mean deep sag to |mean| < "
                  "0.05 dex/dex with the white-noise floor intact. The sag is "
                  "UNEXPLAINED one-sign coherent structure -- the theory's sharpest "
                  "open anomaly, escalated for the equilibrium account to absorb "
                  "(candidate (d) EFE is closed at SPARC amplitudes by G036 V4e/G044 V2E).")
check("FINAL VERDICT -- WHICH CANDIDATE OWNS THE SAG", verdict_txt, final_ok, final_read)

# ================================================================== artifact
out = dict(meta=dict(lane="G049",
                     title="the sag decomposition: radial M/L gradient vs matched law vs HI truncation",
                     preregistration="G049_preregistration.md (frozen before any residual was computed)",
                     a0={k: float(v) for k, v in A0.items()},
                     deep_regime_r_over_rM=DEEP,
                     corpora=dict(sparc_galaxies=len(sparc),
                                  sparc_with_Rdisk=len(SPARC_RD),
                                  tier1_curves=len(ext),
                                  tier1_crossmatched=n_inh),
                     ml_bounds=dict(ups0=[UPS_LO, UPS_HI], ups1=[UP1_LO, UP1_HI]),
                     verdict_gates=dict(sag_kill=SAG_KILL, sag_half=SAG_HALF,
                                        floor_tol=FLOOR_TOL)),
           v0_anchor={f: {k: v for k, v in V0[f].items()} for f in A0},
           candidate_a_gradient={f: grad_res[f] for f in A0},
           priced_precision={f: priced[f] for f in A0},
           candidate_b_matched_law={f: match_res[f] for f in A0},
           candidate_c_truncation={f: dict(full=trunc_res[f][0],
                                           drop2=trunc_res[f][1]) for f in A0},
           C_vs_mu2_offset_profile=prof,
           checks=[{k: r[k] for k in ("name", "measured", "pass", "reading")} for r in RES])
with open(os.path.join(HERE, "G049_sag_decomposition_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=float)
print("\nwrote G049_sag_decomposition_results.json")

print()
print(f"G049 COMPLETE: {NP_}/{NP_+NF} checks PASS.")
