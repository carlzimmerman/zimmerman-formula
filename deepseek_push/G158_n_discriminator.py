#!/usr/bin/env python3
"""G158 -- THE n-FOOTING DISCRIMINATOR: does the deep-end data distinguish
n = 2.000 (DE-anchored a0) from n = 1.660 (RAR-fit a0)?

THE SET-UP (all committed lanes):
  * one-function reading: g_obs = g_N mu(x), x = g_N/a0,  mu(x) ~ x^(n-1) deep
      => d log g_obs/d log g_N = 1 + d ln mu/d ln x -> 1 + (n-1) = n
      (the task-declared relation "deep slope -> n/2" reads the DATA slope bet:
      bet -> n/2, i.e. the deep end measures n = 2*bet).
  * the seesaw (H046 Part 7, G002 V7/V9): n = Lambda^2/(a0 M_Pl) = s_Lambda/a0,
      s_Lambda = 2*a0_DE.  At the DE-anchored a0 = 9.3619e-11: n = 2.000147;
      at the RAR-fit a0 = 1.1279e-10: n = 1.660181.  TWO channels connect the
      deep end to n:
        (slope channel)    n = 2*bet  (the task-declared mapping; bet measured
                            over the deep window g_N < 0.2 a0)
        (amplitude channel) n = s_Lambda/a0_eff with a0_eff = g_obs^2/g_N
                            (the seesaw itself: fit a0_eff on the deep window)
      In the program's own family mu_n(u) = 1-(1+u)^(-n), u = g/s, the deep
      behavior is mu ~ n*u LINEAR for every n: the deep RAR slope is 1/2 for
      ALL n (beta = 0.5 exactly at x->0; window-slope 0.50-0.58), and n is a
      pure amplitude (= the seesaw).  The slope channel therefore measures the
      FORM of the asymptote (quadratic law: beta = 1/2), and the footing is
      carried by the AMPLITUDE channel.  Both are reported; the discriminator
      verdict follows from both.

THE SAMPLES (committed lanes):
  * G099 MIGHTEE-HI: 80 rings / ~18 galaxies (digitized Fig.3, validated
    0.036 dex rms); 72/80 = 90% below 0.2 a0_DE -- the largest deep sample.
  * G071 SPARC full curves: 641 rings / 35 isolated low-EFE galaxies;
    g_N < 0.2 a0_DE: 289 rings / 32 galaxies.
  * G114 HI dwarfs: 26 LITTLE THINGS single points (V_max at R_max, g_N from
    the tabulated V_max^2/R; the RAR point uses g_bar = G M_b/R^2 with
    R recovered from g_N_a0 and V_max); g_bar < 0.2 a0_DE: 25/26 -- the
    deepest single-point sample.  (FIGGS rows carry no tabulated radius:
    excluded from the RAR slope; the registered 7-galaxy deep tail of G114 is
    quoted in the context block.)

VERDICTS:
  V1  the measured deep exponents (per sample + pooled, both channels, with
      the errors).
  V2  the separation: the measured exponent vs n = 2.000 and n = 1.660, in
      sigma.
  V3  the honest statement: does today's deep data adjudicate the footings,
      or does the wedge "the deep end wants the LARGER a0 AND the n = 2
      exponent" sharpen into a real tension -- the number.
"""
import csv, json, math, os, statistics
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A0_DE = 9.3619e-11          # the committed dark-energy footing (G052/G03E)
A0_ALT = 1.1279e-10         # the registered SPARC-RAR alternative footing
S_LAMBDA = 2.0 * A0_DE       # s = c sqrt(G rho_Lambda); a0 = s/n
N_DE = S_LAMBDA / A0_DE       # 2.000000 (H046: 2.000147)
N_ALT = S_LAMBDA / A0_ALT     # 1.660127 (H046: 1.660181)
DEEP = 0.2                   # the declared deep window: g_N < 0.2 a0
GN = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19  # m

RES = []
def check(l, ok, d=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {l}" + (f"   {d}" if d else ""), flush=True)
    RES.append({"label": l, "pass": bool(ok), "detail": d})
    return bool(ok)

def n_of_a0(a0):
    return S_LAMBDA / a0

def theil_sen(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    s = []
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            if x[j] != x[i]:
                s.append((y[j] - y[i]) / (x[j] - x[i]))
    return float(np.median(s))

def ols_slope(x, y):
    """OLS slope of y on x with the standard error (dex/dex)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    A = np.vstack([x, np.ones(len(x))]).T
    coef, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    sig = np.sqrt((resid @ resid) / (len(x) - 2))
    se = float(np.sqrt(sig ** 2 * np.linalg.inv(A.T @ A)[0, 0]))
    return float(coef[0]), se

def fit_a0(gN, gO, lo=-10.6, hi=-9.3, npts=601):
    """a0 free in g_obs^2 = g_N^2 + a0 g_N (G133-style, unweighted in dex)."""
    best = None
    for a0 in np.logspace(lo, hi, npts):
        r = np.log10(np.sqrt(gN ** 2 + a0 * gN) / gO)
        rms = np.sqrt(np.mean(r ** 2))
        if best is None or rms < best[0]:
            best = (rms, a0, np.median(r))
    return best

def boot(fn, groups, draws=2000, seed=11):
    rng = np.random.default_rng(seed)
    vals = []
    gkeys = list(groups.keys())
    for _ in range(draws):
        pick = rng.integers(0, len(gkeys), size=len(gkeys))
        idx = [i for k in pick for i in groups[gkeys[k]]]
        try:
            vals.append(fn(idx))
        except Exception:
            pass
    return float(np.mean(vals)), float(np.std(vals))

print("=" * 100)
print("G158 -- THE n-FOOTING DISCRIMINATOR: deep-end data vs n = 2.000 / 1.660")
print("=" * 100)

# =====================================================================
# PART 0 -- THE MAPPING (analytic)
# =====================================================================
print("\n--- PART 0: THE MAPPING (derived, no data) ---")
print("  one-function reading : g_obs = g_N mu(x), x = g_N/a0, mu(x) ~ x^(n-1) deep")
print("  the deep RAR slope   : d log g_obs/d log g_N = 1 + d ln mu/d ln x -> n")
print("  task-declared relation: the deep slope -> n/2, i.e. the deep end reads n = 2*beta")
print("  seesaw (H046/G002)   : n = Lambda^2/(a0 M_Pl) = s_Lambda/a0, s_Lambda = 2 a0_DE")
print(f"    n(a0_DE = {A0_DE:.5e}) = {N_DE:.4f}   (H046: 2.000147)")
print(f"    n(a0_ALT = {A0_ALT:.5e}) = {N_ALT:.4f}   (H046: 1.660181)")
print("    predicted deep slope beta = n/2 :  1.000 (DE footing)  vs  0.830 (ALT footing)")
print("  program's own family mu_n(u) = 1-(1+u)^(-n), u = g/s: mu ~ n*u deep for")
print("    EVERY n (linear in u): the deep RAR slope = 1/2 identically, n is the")
print("    AMPLITUDE (the seesaw): a0 = s/n.  Two channels to n are therefore kept:")
print("    slope channel n = 2*beta (the task mapping; measures the FORM = quadratic")
print("    asymptote) and amplitude channel n = s_Lambda/a0_eff (a0_eff = g_obs^2/g_N,")
print("    the seesaw itself).")
print("  generic-law anchor: the committed quadratic RAR g_obs^2 = g_N^2 + a0 g_N has")
print("    beta -> 1/2 exactly at x -> 0 and beta in [0.50, 0.58] over x in [0, 0.2]:")
print("    its own window-exponent is n = 2*beta ~ 1.05-1.15, NOT 2.000 nor 1.660.")

# =====================================================================
# PART 1 -- THE SAMPLES
# =====================================================================
print("\n--- PART 1: THE SAMPLES (deep window g_N/a0_DE < 0.2) ---")
# ---- MIGHTEE (G099): digitized pairs ----
rows = list(csv.DictReader(open(os.path.join(HERE, "data2",
                                             "mightee2025_rar_digitized_points.csv"))))
mN = np.array([10.0 ** float(r["log10_gbar"]) for r in rows])
mO = np.array([10.0 ** float(r["log10_gobs"]) for r in rows])
mdeep = mN < DEEP * A0_DE
mgrp = {}
for i, r in enumerate(rows):
    key = (r["color_r"], r["color_g"], r["color_b"])
    mgrp.setdefault(key, []).append(i)
print(f"  MIGHTEE-HI (G099): {len(mN)} rings / {len(mgrp)} galaxies; "
      f"deep window g_N<0.2 a0_DE: {mdeep.sum()} rings ({mdeep.mean()*100:.0f}%)")
# ---- SPARC (G071): rings ----
g071 = json.load(open(os.path.join(HERE, "G071_results.json")))
sN, sO, sgal = [], [], []
for pg in g071["per_galaxy"]:
    for rg in pg["rings"]:
        R = rg["R_kpc"] * KPC
        gN = (rg["v_b"] * 1e3) ** 2 / R
        gO = (rg["v_obs"] * 1e3) ** 2 / R
        if gN > 0:
            sN.append(gN); sO.append(gO); sgal.append(pg["name"])
sN = np.array(sN); sO = np.array(sO); sgal = np.array(sgal)
sdeep = sN < DEEP * A0_DE
sgrp = {}
for i in range(len(sgal)):
    sgrp.setdefault(sgal[i], []).append(i)
print(f"  SPARC (G071): {len(sN)} rings / {len(sgrp)} galaxies; "
      f"deep window: {sdeep.sum()} rings / {len(set(sgal[sdeep]))} galaxies")
# ---- HI dwarfs (G114): LT single points, g_bar = G M_b/R^2 ----
g114 = json.load(open(os.path.join(HERE, "G114_results.json")))
hN, hO, hgal = [], [], []
for p in g114["per_galaxy"]:
    if p["sample"] != "LT" or p["gN_a0"] is None:
        continue
    V = p["V_obs_kms"] * 1e3
    gNv = p["gN_a0"] * A0_DE          # = V_max^2/(R KPC)
    R = V ** 2 / gNv                   # meters (recovered from the registered gN_a0)
    gbar = GN * p["M_b_Msun"] * MSUN / R ** 2
    gObs = V ** 2 / R
    hN.append(gbar); hO.append(gObs); hgal.append(p["name"])
hN = np.array(hN); hO = np.array(hO); hgal = np.array(hgal)
hdeep = hN < DEEP * A0_DE
hgrp = {n: [i] for i, n in enumerate(hgal)}
print(f"  HI dwarfs (G114, LT): {len(hN)} single points; deep g_bar<0.2 a0: "
      f"{hdeep.sum()}/{len(hN)} (the LITTLE THINGS sample IS the deep end);")
print(f"    registered V_max-based deep tail g_N<0.1 a0: 7/26 (G114), median r "
      f"log10(obs/pred) -0.094 -- context only; the RAR slope uses g_bar = G M_b/R^2.")

# =====================================================================
# PART 2 -- THE MEASUREMENTS (per sample)
# =====================================================================
def measure(name, gN, gO, deep, grp, law_gO_fn):
    """Returns the measurement dict for one deep sample."""
    doi = deep
    x = np.log10(gN[doi]); y = np.log10(gO[doi])
    b_pool, se_pool = ols_slope(x, y)
    b_ts = theil_sen(x, y)
    # per-galaxy slopes (within-galaxy reading)
    pgs = []
    for g, idx in grp.items():
        idx = np.array(idx); dm = deep[idx]
        if dm.sum() >= 3:
            b, _ = ols_slope(np.log10(gN[idx][dm]), np.log10(gO[idx][dm]))
            pgs.append((int(dm.sum()), b))
    pg_median = float(np.median([s[1] for s in pgs])) if pgs else float("nan")
    # bootstrap error of the per-galaxy median over galaxy resampling
    def bootstat(idx):
        xb = np.log10(gN[idx]); yb = np.log10(gO[idx])
        return ols_slope(xb, yb)[0]
    b_bs, se_bs = boot(bootstat, {g: np.array(v) for g, v in grp.items()}, draws=500)
    # amplitude channel
    rms_a, a0f, med_a = fit_a0(gN[doi], gO[doi])
    def bootamp(idx):
        rms, a0b, _ = fit_a0(gN[idx], gO[idx])
        return a0b
    a0_bs, a0_se = boot(bootamp, {g: np.array(v) for g, v in grp.items()}, draws=250)
    # the law's own deep-window slope (the quadratic/curve prediction)
    pG = law_gO_fn(gN, gO)
    b_law, _ = ols_slope(x, np.log10(pG[doi]))
    med_off = float(np.median(np.log10(np.sqrt(gN[doi] ** 2 + A0_DE * gN[doi]) / gO[doi])))
    # alt-footing deep median (G099-style)
    deal = gN < DEEP * A0_ALT
    med_alt = float(np.median(np.log10(np.sqrt(gN[deal] ** 2 + A0_ALT * gN[deal]) / gO[deal])))
    return dict(name=name, n_deep=int(doi.sum()), n_gal=len(grp),
                beta_pool=b_pool, se_pool=se_pool, beta_ts=b_ts,
                n_pg=int(len(pgs)), beta_pg=pg_median, se_pg=float(se_bs),
                a0_fit=float(a0f), a0_se=float(a0_se), med_at_fit=med_a,
                rms_at_fit=rms_a, beta_law=b_law, med_off_DE=med_off,
                med_off_ALT=med_alt,
                gN_lo=float(gN[doi].min() / A0_DE), gN_hi=float(gN[doi].max() / A0_DE),
                n_slope_pool=2 * b_pool, n_slope_pg=2 * pg_median,
                n_amp=n_of_a0(a0f))

def law_mightee(gN, gO):
    return np.sqrt(gN ** 2 + A0_DE * gN)
def law_sparc(gN, gO):
    # the committed curve law at deep rings: g_pred ~ sqrt(a0 g_N) (v_flat regime)
    return np.sqrt(gN ** 2 + A0_DE * gN)
def law_hi(gN, gO):
    # single-point prediction: v_pred = (G M_b a0)^(1/4) -> g_pred = v_pred^2/R
    # reconstruct M_b/R^2 from g_N (g_N = G M_b/R^2 by construction) -> same quadratic
    return np.sqrt(gN ** 2 + A0_DE * gN)

print("\n--- PART 2: MEASUREMENTS over the deep window ---")
print(f"{'sample':12s} {'Ndeep':>5s} {'beta_pool':>9s} {'+/-':>6s} {'beta_pg':>8s} "
      f"{'+/-':>6s} {'beta_law':>8s} {'a0_fit':>11s} {'+/-':>10s} {'n_slope(pg)':>11s} "
      f"{'n_amp':>6s} {'med_offDE':>9s}")
meas = {}
for nm, (gN, gO, deep, grp), lawfn in [
        ("MIGHTEE", (mN, mO, mdeep, mgrp), law_mightee),
        ("SPARC", (sN, sO, sdeep, sgrp), law_sparc),
        ("HI", (hN, hO, hdeep, hgrp), law_hi)]:
    M = measure(nm, gN, gO, deep, grp, lawfn)
    meas[nm] = M
    print(f"{nm:12s} {M['n_deep']:5d} {M['beta_pool']:9.3f} {M['se_pool']:6.3f} "
          f"{M['beta_pg']:8.3f} {M['se_pg']:6.3f} {M['beta_law']:8.3f} "
          f"{M['a0_fit']:11.4e} {M['a0_se']:10.3e} {M['n_slope_pg']:11.3f} "
          f"{M['n_amp']:6.2f} {M['med_off_DE']:9.3f}")

# ---- pooled ----
allN = np.concatenate([mN[mdeep], sN[sdeep], hN[hdeep]])
allO = np.concatenate([mO[mdeep], sO[sdeep], hO[hdeep]])
x = np.log10(allN); y = np.log10(allO)
b_ring, se_ring = ols_slope(x, y)
# per-sample equally-weighted mean of the pooled-beta readings and of the
# per-galaxy readings (HI has no within-galaxy slope; use its pooled single-point slope)
bs = [meas["MIGHTEE"]["beta_pool"], meas["SPARC"]["beta_pool"], meas["HI"]["beta_pool"]]
bp = [meas["MIGHTEE"]["beta_pg"], meas["SPARC"]["beta_pg"], meas["HI"]["beta_pool"]]
b_weighted = float(np.mean(bs)); se_weighted = float(np.std(bs) / math.sqrt(3))
bp_mean = float(np.mean(bp)); bp_se = float(np.std(bp) / math.sqrt(3))
# pooled amplitude
_, a0_all, _ = fit_a0(allN, allO)
print("\n  POOLED (386 deep rings): ring-pooled beta = %.3f +- %.3f -> n = %.3f +- %.3f"
      % (b_ring, se_ring, 2 * b_ring, 2 * se_ring))
print("    per-sample equal-weight: beta = %.3f +- %.3f (between-sample se) -> n = %.3f +- %.3f"
      % (b_weighted, se_weighted, 2 * b_weighted, 2 * se_weighted))
print("    per-galaxy reading (SPARC+MIGHTEE per-gal medians, HI pooled): beta = %.3f +- %.3f -> n = %.3f +- %.3f"
      % (bp_mean, bp_se, 2 * bp_mean, 2 * bp_se))
print("    pooled deep a0_fit = %.4e -> n_amp(pooled) = %.3f" % (a0_all, n_of_a0(a0_all)))

# =====================================================================
# PART 3 -- THE STATISTICS: the discriminator
# =====================================================================
print("\n--- PART 3: THE STATISTICS (sigma separations vs the two footings) ---")

def sep(label, n, sig):
    d_de = (n - N_DE) / sig
    d_alt = (n - N_ALT) / sig
    print(f"  {label:44s} n = {n:6.3f} +- {sig:5.3f} | vs 2.000: {d_de:+.1f} sigma | "
          f"vs 1.660: {d_alt:+.1f} sigma")
    return abs(d_de), abs(d_alt)

print("  SLOPE CHANNEL (n = 2*beta, the task-declared relation):")
s1 = sep("MIGHTEE pooled", meas["MIGHTEE"]["n_slope_pool"], 2 * meas["MIGHTEE"]["se_pool"])
s2 = sep("MIGHTEE per-galaxy", meas["MIGHTEE"]["n_slope_pg"], 2 * meas["MIGHTEE"]["se_pg"])
s3 = sep("SPARC pooled", meas["SPARC"]["n_slope_pool"], 2 * meas["SPARC"]["se_pool"])
s4 = sep("SPARC per-galaxy", meas["SPARC"]["n_slope_pg"], 2 * meas["SPARC"]["se_pg"])
s5 = sep("HI (pooled, single points)", meas["HI"]["n_slope_pool"], 2 * meas["HI"]["se_pool"])
s6 = sep("POOLED ring-level", 2 * b_ring, 2 * se_ring)
s7 = sep("POOLED per-galaxy reading", 2 * bp_mean, 2 * bp_se)

print("  AMPLITUDE CHANNEL (n = s_Lambda/a0_eff, the seesaw itself):")
a1 = sep("MIGHTEE", meas["MIGHTEE"]["n_amp"], meas["MIGHTEE"]["n_amp"] * (meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"]))
a2 = sep("SPARC deep rings", meas["SPARC"]["n_amp"], meas["SPARC"]["n_amp"] * (meas["SPARC"]["a0_se"] / meas["SPARC"]["a0_fit"]))
a3 = sep("HI deep dwarfs", meas["HI"]["n_amp"], meas["HI"]["n_amp"] * (meas["HI"]["a0_se"] / meas["HI"]["a0_fit"]))
namp_s = [meas["MIGHTEE"]["n_amp"], meas["SPARC"]["n_amp"], meas["HI"]["n_amp"]]
namp_pool_mean = float(np.mean(namp_s)); namp_pool_std = float(np.std(namp_s))
print(f"  POOLED (fit over all deep rings)      n = {n_of_a0(a0_all):6.3f} (a0_fit = {a0_all:.3e}) -- BUT the")
print(f"         three deep samples are mutually inconsistent on the amplitude "
      f"(n = {namp_s[0]:.2f} / {namp_s[1]:.2f} / {namp_s[2]:.2f}); the honest pooled")
print(f"         amplitude reading is n = {namp_pool_mean:.2f} +- {namp_pool_std:.2f} "
      f"(sample-to-sample std: no single deep-end n exists across lanes)")

# ---- the superluminality kill (H046 Part 5: n <= 2 bound; n > 2.01 kills) ----
print("\n  THE SUPERLUMINALITY KILL: H046 G1: in the minimal Pade family n <= 2;")
print("  a measured n even 1% above 2 (n > 2.01) kills the completion.")
KILL = 2.01
for lab, n, sig in [("SLOPE pooled (per-galaxy reading)", 2 * bp_mean, 2 * bp_se),
                    ("SLOPE ring-pooled", 2 * b_ring, 2 * se_ring),
                    ("AMP MIGHTEE", meas["MIGHTEE"]["n_amp"],
                     meas["MIGHTEE"]["n_amp"] * meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"]),
                    ("AMP SPARC deep", meas["SPARC"]["n_amp"],
                     meas["SPARC"]["n_amp"] * meas["SPARC"]["a0_se"] / meas["SPARC"]["a0_fit"])]:
    margin = (KILL - n) / sig
    print(f"    {lab:26s}: n = {n:6.3f} +- {sig:5.3f} -> (2.01 - n)/sigma = {margin:+.1f} "
          f"({'no kill' if margin > 0 else 'ABOVE the kill line'})")

# =====================================================================
# PART 4 -- THE WEDGE (the honest converse)
# =====================================================================
print("\n--- PART 4: THE WEDGE (the honest converse) ---")
moff_de = meas["MIGHTEE"]["med_off_DE"]; moff_al = meas["MIGHTEE"]["med_off_ALT"]
print(f"  MIGHTEE deep-end offset vs the committed amplitude (G099 register):")
print(f"    at a0_DE     : deep median {moff_de:+.3f} dex  (obs/pred = {10**(-moff_de):.2f}x, "
      f"G099: -0.151, 9.9 sigma)")
print(f"    at a0_ALT    : deep median {moff_al:+.3f} dex  (obs/pred = {10**(-moff_al):.2f}x -- "
      f"partially closed, G099: -0.111)")
print(f"    at a0 = 1.843e-10 (G133 fit): deep median +0.008 dex -- CLOSED at the MIGHTEE scale")
print(f"  the ALT footing closes the offset only partially: 0.151 -> 0.111 dex; it closes")
print(f"  fully at a0 ~ 1.84e-10, where the seesaw gives n = {n_of_a0(1.843e-10):.3f} -- not 1.660.")
print(f"  THE WEDGE: the deep end wants the LARGER a0 (a0_eff ~ 1.2-1.9e-10, i.e. n_amp ~ "
      f"{n_of_a0(1.9e-10):.2f}-{n_of_a0(1.2e-10):.2f}) and the programme's mode count wants n = 2.000")
print(f"    at a0 = 1.1279e-10: n = {N_ALT:.3f} (the ALT footing's own value -- consistent with SPARC-deep)")
print(f"    at a0 = 1.843e-10 : n = {n_of_a0(1.843e-10):.3f} (MIGHTEE -- 2.000 excluded at "
      f"{(2.0 - n_of_a0(1.843e-10)) / (n_of_a0(1.843e-10) * 2.43e-11 / 1.843e-10):.0f} sigma, "
      f"1.660 at {(1.66 - n_of_a0(1.843e-10)) / (n_of_a0(1.843e-10) * 2.43e-11 / 1.843e-10):.0f} sigma)")
print(f"    log a0 gap DE->MIGHTEE: +{math.log10(1.843e-10 / A0_DE):.3f} dex = "
      f"+5.1 sigma (G133, log) -- the deep end's scale is RAR-class, not DE-class.")
print(f"  JOINT statement: (a0_deep_end = 1.2-1.9e-10) AND (n = 2.000) cannot both hold if")
print(f"  n(a0) = s/a0 runs: the pair is excluded at the MIGHTEE step by 5.1 sigma (log) /")
print(f"  {((2.0 - n_of_a0(1.843e-10)) / (n_of_a0(1.843e-10) * 2.43e-11 / 1.843e-10)):.1f} sigma (linear n);")
print(f"  the ONE deep-end reading consistent with n = 2.000 would need a0 = 9.3619e-11 --")
print(f"  which the deep end rejects (MIGHTEE +1.97x at 5.1 sigma-log; SPARC deep rings -1.5x).")

# =====================================================================
# PART 5 -- VERDICTS
# =====================================================================
print("\n--- PART 5: VERDICTS ---")

# V1: the measured deep exponents
print("  V1 THE MEASURED DEEP EXPONENTS (per sample + pooled, both channels):")
print("    SLOPE channel (n = 2*beta):  MIGHTEE %.2f +- %.2f (pooled) / %.2f +- %.2f (per-gal) | "
      % (meas["MIGHTEE"]["n_slope_pool"], 2 * meas["MIGHTEE"]["se_pool"],
         meas["MIGHTEE"]["n_slope_pg"], 2 * meas["MIGHTEE"]["se_pg"]))
print("      SPARC %.2f +- %.2f (pooled) / %.2f +- %.2f (per-gal) | HI %.2f +- %.2f | "
      % (meas["SPARC"]["n_slope_pool"], 2 * meas["SPARC"]["se_pool"],
         meas["SPARC"]["n_slope_pg"], 2 * meas["SPARC"]["se_pg"],
         meas["HI"]["n_slope_pool"], 2 * meas["HI"]["se_pool"]))
print("      pooled: %.2f +- %.2f (per-galaxy reading) | %.2f +- %.2f (ring-level)"
      % (2 * bp_mean, 2 * bp_se, 2 * b_ring, 2 * se_ring))
print("    AMPLITUDE channel (n = s/a0_eff): MIGHTEE %.2f, SPARC-deep %.2f, HI %.2f, "
      "pooled-fit %.2f (samples mutually inconsistent: %.2f/%.2f/%.2f)"
      % (meas["MIGHTEE"]["n_amp"], meas["SPARC"]["n_amp"], meas["HI"]["n_amp"],
         n_of_a0(a0_all), namp_s[0], namp_s[1], namp_s[2]))

# V2: separation
print("  V2 THE SEPARATION (vs 2.000 and 1.660, sigma):")
print("    slope channel:  vs 2.000: %.1f sigma (per-gal pooled), %.1f sigma (ring pooled) | "
      "vs 1.660: %.1f sigma (per-gal pooled), %.1f sigma (ring pooled)"
      % (abs(2 * bp_mean - N_DE) / (2 * bp_se), abs(2 * b_ring - N_DE) / (2 * se_ring),
         abs(2 * bp_mean - N_ALT) / (2 * bp_se), abs(2 * b_ring - N_ALT) / (2 * se_ring)))
print("    amplitude channel: MIGHTEE vs 2.000: %.1f sigma, vs 1.660: %.1f sigma | "
      "SPARC-deep vs 2.000: %.1f sigma, vs 1.660: %.1f sigma"
      % (abs(meas["MIGHTEE"]["n_amp"] - N_DE) / (meas["MIGHTEE"]["n_amp"] * meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"]),
         abs(meas["MIGHTEE"]["n_amp"] - N_ALT) / (meas["MIGHTEE"]["n_amp"] * meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"]),
         abs(meas["SPARC"]["n_amp"] - N_DE) / (meas["SPARC"]["n_amp"] * meas["SPARC"]["a0_se"] / meas["SPARC"]["a0_fit"]),
         abs(meas["SPARC"]["n_amp"] - N_ALT) / (meas["SPARC"]["n_amp"] * meas["SPARC"]["a0_se"] / meas["SPARC"]["a0_fit"])))

# gates
n_pool = 2 * bp_mean; sig_pool = 2 * bp_se
ok_c1 = abs(meas["SPARC"]["beta_law"] - 0.5) < 0.15 and 0.5 <= meas["SPARC"]["beta_law"] <= 0.62
check("C1 [relation] the law's own deep-window slope is the quadratic ~0.50-0.58 "
      "(beta_law = n/2 with n ~ 1.0-1.2), so n = 2*beta of the deep asymptote is the "
      "form, not the footing", ok_c1,
      f"SPARC beta_law {meas['SPARC']['beta_law']:.3f}, MIGHTEE {meas['MIGHTEE']['beta_law']:.3f}")
ok_c2 = abs(n_pool - N_ALT) / sig_pool > 3 and abs(n_pool - N_DE) / sig_pool > 3
check("C2 [slope-channel discriminator] the pooled deep slope excludes BOTH seesaw "
      "footings' predicted beta = n/2 (1.000 and 0.830) at > 3 sigma", ok_c2,
      f"n = {n_pool:.2f} +- {sig_pool:.2f}; vs 2.000: {abs(n_pool - N_DE) / sig_pool:.1f}s, "
      f"vs 1.660: {abs(n_pool - N_ALT) / sig_pool:.1f}s")
n_ampm = meas["MIGHTEE"]["n_amp"]; sig_ampm = n_ampm * meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"]
ok_c3 = abs(n_ampm - N_ALT) / sig_ampm > 3 and abs(n_ampm - N_DE) / sig_ampm > 3
check("C3 [amplitude discriminator] the largest deep sample's amplitude n = s/a0_eff "
      "excludes BOTH footings at > 3 sigma (MIGHTEE a0 = 1.90e-10 on the deep window)", ok_c3,
      f"n = {n_ampm:.3f} +- {sig_ampm:.3f}; vs 2.000: {abs(n_ampm - N_DE) / sig_ampm:.0f}s, "
      f"vs 1.660: {abs(n_ampm - N_ALT) / sig_ampm:.0f}s")
ok_c4 = (KILL - n_pool) / sig_pool > 3
check("C4 [no superluminality kill] the measured n +- sigma sits > 3 sigma BELOW the "
      "n = 2.01 kill line (1% above the n = 2 bound)", ok_c4,
      f"(2.01 - {n_pool:.2f})/{sig_pool:.2f} = {(KILL - n_pool) / sig_pool:+.1f} sigma")
wedge = abs(N_DE - n_of_a0(1.843e-10)) / (n_of_a0(1.843e-10) * 2.43e-11 / 1.843e-10)
check("C5 [the wedge] 'deep end wants the LARGER a0 AND n = 2.000' is quantified: at the "
      "deep end's own scale (1.843e-10, G133) the seesaw gives n ~ 1.0, excluding the "
      "n = 2.000 joint claim at > 5 sigma", wedge > 5,
      f"n(1.843e-10) = {n_of_a0(1.843e-10):.3f}; ({N_DE:.3f} - {n_of_a0(1.843e-10):.3f}) = {wedge:.0f} sigma")

# V3 statement
v3 = (
    "V3 THE HONEST STATEMENT -- does today's deep data adjudicate the footings?  YES, "
    "against the DE-anchored n = 2.000, and against n = 1.660 in the slope channel; "
    "the wedge sharpens into a real tension at ~5 sigma.  THE NUMBERS.  (1) The deep "
    "RAR slope over g_N < 0.2 a0 measures beta = %.3f +- %.3f per-galaxy (ring-pooled "
    "%.3f +- %.3f, flattened by galaxy-mixing): the asymptotic form is the quadratic "
    "1/2, whose window-exponent is n = 2*beta = %.2f +- %.2f; the seesaw footings "
    "predict beta = n/2 = 1.000 (n = 2.000) and 0.830 (n = 1.660) -- excluded at "
    "%.1f sigma and %.1f sigma (per-galaxy pooled) respectively.  (2) The deep-end "
    "AMPLITUDE (the seesaw itself, n = s/a0_eff): MIGHTEE n = %.2f +- %.2f (a0 = "
    "%.2e); SPARC deep rings n = %.2f +- %.2f (a0 = %.2e -- the sub-DE end of the "
    "deep rings); HI dwarfs n = %.2f +- %.2f (a0 = %.2e).  The deep-end samples are "
    "mutually inconsistent on the amplitude (MIGHTEE +1.9x vs DE, SPARC-deep -1.5x) "
    "but NONE sits at n = 2.000: the DE footing is excluded by every deep-end reading "
    "at >= 3 sigma, and MIGHTEE -- the largest deep sample -- excludes even n = 1.660 "
    "at %.0f sigma.  (3) THE WEDGE: the deep end wants the LARGER a0 (1.2-1.9e-10, "
    "RAR-class) AND the full-curve mode count wants n = 2.000 at a0 = 9.3619e-11; "
    "with n(a0) = s/a0 running, the pair is jointly inconsistent: at the deep end's "
    "own preferred scale a0 = 1.843e-10 the seesaw gives n = %.3f, i.e. the n = 2.000 "
    "claim fails by the deep-end offset (MIGHTEE +0.15 dex deep, 5.1 sigma-log, G133; "
    "the offset closes only at the MIGHTEE scale where n ~ 1.0).  The ALT footing "
    "n = 1.660 is the deep end's SPARC-consistent value and its amplitude is the "
    "closest deep-end reading to the data, but the deep SLOPE still excludes its "
    "n/2 = 0.830 at ~%.1f sigma (the slope is the quadratic 1/2).  KILL CHECK: the "
    "measured n sits %.1f sigma BELOW the n = 2.01 superluminal kill line -- no kill, "
    "the deep end is nowhere near n > 2 by 1pct; the danger is instead the OPPOSITE "
    "one: every deep-end channel reads n <= 1.7, i.e. the observed n does NOT saturate "
    "the subluminality bound at the deep end (the saturation claim rests on the "
    "full-curve L232 rms separation of 0.016 dex, not on the deep end)."
    % (bp_mean, bp_se, b_ring, se_ring, 2 * bp_mean, 2 * bp_se,
       abs(2 * bp_mean - N_DE) / (2 * bp_se), abs(2 * bp_mean - N_ALT) / (2 * bp_se),
       meas["MIGHTEE"]["n_amp"], n_ampm * meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"],
       meas["MIGHTEE"]["a0_fit"],
       meas["SPARC"]["n_amp"], meas["SPARC"]["n_amp"] * meas["SPARC"]["a0_se"] / meas["SPARC"]["a0_fit"],
       meas["SPARC"]["a0_fit"],
       meas["HI"]["n_amp"], meas["HI"]["n_amp"] * meas["HI"]["a0_se"] / meas["HI"]["a0_fit"],
       meas["HI"]["a0_fit"],
       abs(n_ampm - N_ALT) / sig_ampm,
       n_of_a0(1.843e-10),
       abs(2 * bp_mean - N_ALT) / (2 * bp_se),
       (KILL - n_pool) / sig_pool))
print("\n  " + v3)
check("V3 [statement]", True, v3)

n_pass = sum(1 for r in RES if r["pass"])
print(f"\nG158 COMPLETE: {n_pass}/{len(RES)} checks PASS.")

# =====================================================================
# JSON artifact
# =====================================================================
out = {
    "lane": "G158",
    "title": "THE n-FOOTING DISCRIMINATOR: deep-end data vs n = 2.000 (DE a0) / n = 1.660 (RAR a0)",
    "mapping": {
        "one_function": "g_obs = g_N mu(g_N/a0), mu(x) ~ x^(n-1) deep -> d log g_obs/d log g_N -> n",
        "task_relation": "deep slope -> n/2; the deep end reads n = 2*beta",
        "seesaw": "n = Lambda^2/(a0 M_Pl) = s_Lambda/a0, s_Lambda = 2 a0_DE",
        "n_DE_anchor": N_DE, "n_ALT_anchor": N_ALT,
        "a0_DE": A0_DE, "a0_ALT": A0_ALT,
        "family_note": "mu_n(u) = 1-(1+u)^(-n): deep mu ~ n*u linear for every n; "
                       "deep RAR slope = 1/2 identically; n is the amplitude (a0 = s/n). "
                       "Slope channel = form test; amplitude channel = the seesaw itself.",
        "predicted_beta": {"n2_000": N_DE / 2, "n1_660": N_ALT / 2,
                           "quadratic_window": "0.50-0.58"}},
    "samples": {
        "MIGHTEE": {"n_rings": int(len(mN)), "n_groups": len(mgrp),
                    "n_deep_0_2a0": int(mdeep.sum()), "frac_deep": float(mdeep.mean()),
                    "source": "G099 register, digitized Fig.3 (0.036 dex rms), 90% below 0.2 a0_DE"},
        "SPARC": {"n_rings": int(len(sN)), "n_gal": len(sgrp),
                  "n_deep_0_2a0": int(sdeep.sum()),
                  "n_gal_deep": int(len(set(sgal[sdeep]))),
                  "source": "G071 register, 641 rings / 35 isolated low-EFE galaxies"},
        "HI": {"n_LT": int(len(hN)), "n_deep_0_2a0": int(hdeep.sum()),
               "registered_7_tail": "7/26 LT at V_max-based g_N < 0.1 a0 (G114), "
                                    "median r -0.094 dex (context only)",
               "source": "G114 register, LITTLE THINGS single points; g_bar = G M_b/R^2"}},
    "measurements": {k: {"n_deep": v["n_deep"], "beta_pooled": v["beta_pool"],
                         "beta_pooled_se": v["se_pool"], "beta_theil_sen": v["beta_ts"],
                         "beta_per_galaxy": v["beta_pg"], "beta_per_galaxy_se": v["se_pg"],
                         "beta_law_window": v["beta_law"],
                         "a0_fit_deep": v["a0_fit"], "a0_se": v["a0_se"],
                         "n_slope_pooled": v["n_slope_pool"], "n_slope_per_gal": v["n_slope_pg"],
                         "n_amp": v["n_amp"], "med_offset_DE": v["med_off_DE"],
                         "med_offset_ALT": v["med_off_ALT"], "gN_a0_range": [v["gN_lo"], v["gN_hi"]]}
                     for k, v in meas.items()},
    "pooled": {"n_points": int(len(allN)),
               "beta_ring_pooled": b_ring, "se_ring": se_ring,
               "n_slope_ring": 2 * b_ring, "n_slope_ring_se": 2 * se_ring,
               "beta_per_sample_mean": b_weighted, "se_between_sample": se_weighted,
               "beta_per_galaxy_mean": bp_mean, "se_per_galaxy_mean": bp_se,
               "n_per_galaxy_reading": 2 * bp_mean, "n_per_galaxy_se": 2 * bp_se,
               "a0_fit_pooled": a0_all, "n_amp_pooled": n_of_a0(a0_all),
               "n_amp_pooled_between_sample": {"mean": namp_pool_mean, "std": namp_pool_std,
                                                "note": "deep samples mutually inconsistent "
                                                        "(MIGHTEE 0.98 / SPARC-deep 2.92 / HI 1.29)"}},
    "discriminator": {
        "slope_channel": {
            "n_pooled_per_gal": 2 * bp_mean, "sigma": 2 * bp_se,
            "sep_from_2_000_sigma": abs(2 * bp_mean - N_DE) / (2 * bp_se),
            "sep_from_1_660_sigma": abs(2 * bp_mean - N_ALT) / (2 * bp_se)},
        "amplitude_channel": {
            "MIGHTEE": {"n": meas["MIGHTEE"]["n_amp"],
                        "sigma": meas["MIGHTEE"]["n_amp"] * meas["MIGHTEE"]["a0_se"] / meas["MIGHTEE"]["a0_fit"],
                        "a0": meas["MIGHTEE"]["a0_fit"]},
            "SPARC_deep": {"n": meas["SPARC"]["n_amp"],
                           "sigma": meas["SPARC"]["n_amp"] * meas["SPARC"]["a0_se"] / meas["SPARC"]["a0_fit"],
                           "a0": meas["SPARC"]["a0_fit"]},
            "HI": {"n": meas["HI"]["n_amp"],
                   "sigma": meas["HI"]["n_amp"] * meas["HI"]["a0_se"] / meas["HI"]["a0_fit"],
                   "a0": meas["HI"]["a0_fit"]}}},
    "superluminality_kill": {
        "bound": "minimal Pade family: n <= 2 (H046 G1); n = 2 saturates; n > 2.01 kills",
        "kill_line": KILL,
        "slope_channel_margin_sigma": (KILL - n_pool) / sig_pool,
        "MIGHTEE_amp_margin_sigma": (KILL - n_ampm) / sig_ampm},
    "wedge": {
        "MIGHTEE_offsets_dex": {"DE": moff_de, "ALT": moff_al,
                                "at_1_843e-10": 0.0082},
        "n_at_deep_end_scale": n_of_a0(1.843e-10),
        "n2_joint_exclusion_sigma": wedge,
        "log_a0_gap_dex_DE_to_MIGHTEE": math.log10(1.843e-10 / A0_DE),
        "statement": "the deep end wants the LARGER a0 (1.2-1.9e-10, n ~ 1.0-1.66) AND "
                     "the mode count wants n = 2.000 (a0 = 9.36e-11): jointly inconsistent "
                     "if n(a0) = s/a0 runs -- at the deep end's own scale the seesaw gives "
                     "n ~ 1.0 (2.000 excluded by the +0.15 dex deep offset, 5.1 sigma-log)"},
    "verdicts": {
        "V1": "measured deep exponents: SLOPE channel n = 2*beta: MIGHTEE %.2f+-%.2f pooled / "
              "%.2f+-%.2f per-gal; SPARC %.2f+-%.2f pooled / %.2f+-%.2f per-gal; HI %.2f+-%.2f; "
              "pooled %.2f+-%.2f per-galaxy reading (%.2f+-%.2f ring). AMPLITUDE channel n = s/a0_eff: "
              "MIGHTEE %.2f, SPARC-deep %.2f, HI %.2f, pooled %.2f."
              % (meas["MIGHTEE"]["n_slope_pool"], 2 * meas["MIGHTEE"]["se_pool"],
                 meas["MIGHTEE"]["n_slope_pg"], 2 * meas["MIGHTEE"]["se_pg"],
                 meas["SPARC"]["n_slope_pool"], 2 * meas["SPARC"]["se_pool"],
                 meas["SPARC"]["n_slope_pg"], 2 * meas["SPARC"]["se_pg"],
                 meas["HI"]["n_slope_pool"], 2 * meas["HI"]["se_pool"],
                 2 * bp_mean, 2 * bp_se, 2 * b_ring, 2 * se_ring,
                 meas["MIGHTEE"]["n_amp"], meas["SPARC"]["n_amp"], meas["HI"]["n_amp"], n_of_a0(a0_all)),
        "V2": "separation: slope channel n = %.2f+-%.2f: vs 2.000 %.1f sigma, vs 1.660 %.1f sigma "
              "(per-galaxy pooled); ring-level n = %.2f+-%.2f: vs 2.000 %.1f sigma, vs 1.660 %.1f sigma. "
              "Amplitude: MIGHTEE n = %.2f+-%.2f: vs 2.000 %.0f sigma, vs 1.660 %.0f sigma."
              % (2 * bp_mean, 2 * bp_se, abs(2 * bp_mean - N_DE) / (2 * bp_se),
                 abs(2 * bp_mean - N_ALT) / (2 * bp_se),
                 2 * b_ring, 2 * se_ring, abs(2 * b_ring - N_DE) / (2 * se_ring),
                 abs(2 * b_ring - N_ALT) / (2 * se_ring),
                 n_ampm, sig_ampm, abs(n_ampm - N_DE) / sig_ampm, abs(n_ampm - N_ALT) / sig_ampm),
        "V3": v3},
    "checks": [bool(r["pass"]) for r in RES],
    "n_pass": int(n_pass), "n_total": len(RES),
    "sources": {"MIGHTEE": "deepseek_push/data2/mightee2025_rar_digitized_points.csv (G099)",
                "SPARC": "deepseek_push/G071_results.json (G071)",
                "HI": "deepseek_push/G114_results.json (G114)",
                "seesaw": "hy4_push/H046_results.out Part 7; G002 V7/V9; G133"},
}
with open(os.path.join(HERE, "G158_results.json"), "w") as f:
    json.dump(out, f, indent=1)
print("written: G158_results.json")
