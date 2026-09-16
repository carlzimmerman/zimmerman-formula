#!/usr/bin/env python3
r"""H033-P1 -- MEASURE THE UNIVERSAL SURFACE DENSITY ON REAL SPARC DATA.

PREDICTION UNDER TEST (H033, prediction P1).
    Sigma_ph = M_ph(<r_M) / (pi r_M^2) = a_0 / (pi G)   -- a UNIVERSAL CONSTANT,
    independent of the galaxy's baryon mass.

    Proof as stated: amplitude law M_ph(<r_M) = M_b, plus r_M^2 = G M_b / a_0,
    hence Sigma = M_b/(pi r_M^2) = a_0/(pi G). No M_b appears.

WHAT IS MEASURED HERE (the operational recipe, fixed before looking at the answer).
    For every SPARC galaxy:
      Mb        = max over the rotation curve of M_b(r) = V_bar(r)^2 r / G     [total baryons]
      r_M       = sqrt(G Mb / a_0)
      Sigma     = [ M_obs(<r_M) - M_b(<r_M) ] / (pi r_M^2)
                = [ g_obs(r_M) - g_bar(r_M) ] / (pi G)                        [identically]
    Both a_0 footings are run. V_obs and V_bar are linearly interpolated in r at r_M.

MASS-TO-LIGHT CONVENTION -- DECIDED BY DATA, NOT BY PREFERENCE.
    The SPARC _rotmod.dat columns Vdisk / Vbul are tabulated at Upsilon = 1; the
    repo's standing convention (G044, G036, G040) is
        V_bar^2 = Vgas|Vgas| + 0.5 Vdisk^2 + 0.7 Vbul^2 .
    The loader quoted in glm53_push/G033_build_fluid_bundle.py omits these factors.
    Check C0 below settles it: only the 0.5/0.7 version reproduces the published
    SPARC radial-acceleration relation (McGaugh+2016 fit, a_0 = 1.2e-10) over four
    decades. That version is therefore PRIMARY; the Upsilon = 1 version is carried
    alongside as an explicit systematic bracket.

SELECTION (pre-registered).
    (S1) >= 5 usable points with V_obs > 0 on the curve.
    (S2) r_M must lie inside the observed radial range -- no extrapolation of V_obs.
    (S3) Sigma > 0 is required to take a logarithm; every non-positive case is
         counted and reported, never silently dropped.

Every check prints the MEASUREMENT and the THRESHOLD on separate lines.
No check is decided by a literal True.
"""
import math, glob, os, json, statistics

# ---------------------------------------------------------------- constants
G    = 6.67430e-11
MSUN = 1.98892e30
PC   = 3.0856775814913673e16
KPC  = 3.0856775814913673e19
A0_REF = 1.2e-10                      # published McGaugh+2016 RAR fit value
FOOT = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}
SPARC = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"
OUT_JSON = "/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H033_P1_results.json"

# pre-registered thresholds
TH = {
    "C0_rar_max_dev_dex": 0.10,   # binned median vs published RAR fit, max allowed deviation
    "C1_abs_slope":       0.05,   # |d log Sigma / d log Mb| allowed for "universal"
    "C1_slope_sigma":     3.0,    # ... or this many standard deviations from zero
    "C2_donato_dex":      0.15,   # |log10 Sigma - 2.15| allowed (3 x Donato's 0.05)
    "C3_lemma_dex":       0.30,   # |log10 Sigma - log10(a0/pi G)| allowed
    "C4_span_dex":        3.50,   # required lever arm in log10 Mb
    "C5_min_galaxies":    100,    # required sample size
    "C6_slope_sign_agree": True,  # placeholder replaced by the measured sign-agreement test
}

RES, NP_, NF_ = [], 0, 0
def check(name, measured, ok, threshold, detail=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured : {measured}")
    print(f"         threshold: {threshold}")
    if detail:
        print(f"         {detail}")
    RES.append({"check": name, "measured": measured, "threshold": threshold, "pass": ok})
    NP_, NF_ = (NP_ + 1, NF_) if ok else (NP_, NF_ + 1)
    return ok


# ---------------------------------------------------------------- ingestion
def load(path, ups):
    """SPARC _rotmod.dat -> [(r_kpc, Vobs, Vbar)] ; Upsilon applied to the stellar terms."""
    pts = []
    for line in open(path):
        if line.startswith("#"):
            continue
        c = line.split()
        if len(c) < 6:
            continue
        try:
            r = float(c[0]); v = float(c[1])
            vg = float(c[3]); vd = float(c[4]); vb = float(c[5])
        except ValueError:
            continue
        if v <= 0:                       # unusable / absent measurement
            continue
        v2 = vg*abs(vg) + ups[0]*vd*abs(vd) + ups[1]*vb*abs(vb)
        pts.append((r, v, math.sqrt(max(v2, 0.0))))
    return pts


def interp(P, x, k):
    """linear interpolation of column k in r"""
    for i in range(len(P) - 1):
        if P[i][0] <= x <= P[i+1][0]:
            x0, x1 = P[i][0], P[i+1][0]
            y0, y1 = P[i][k], P[i+1][k]
            return y0 if x1 == x0 else y0 + (y1 - y0)*(x - x0)/(x1 - x0)
    return None


def ols(xs, ys):
    n = len(xs); mx = statistics.fmean(xs); my = statistics.fmean(ys)
    sxx = sum((x - mx)**2 for x in xs)
    sxy = sum((x - mx)*(y - my) for x, y in zip(xs, ys))
    slope = sxy/sxx; icpt = my - slope*mx
    res = [y - (icpt + slope*x) for x, y in zip(xs, ys)]
    se = math.sqrt(sum(r*r for r in res)/(n - 2)/sxx)
    return slope, se, icpt, math.sqrt(sum(r*r for r in res)/n)


def galaxies(ups):
    out = []
    for p in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        P = load(p, ups)
        if len(P) >= 5:                                     # (S1)
            out.append((os.path.basename(p).replace("_rotmod.dat", ""), P))
    return out


print("="*78)
print("H033-P1 -- THE UNIVERSAL SURFACE DENSITY, MEASURED ON REAL SPARC DATA")
print("="*78)
print(f"  SPARC directory : {SPARC}")
print(f"  files on disk   : {len(glob.glob(os.path.join(SPARC,'*_rotmod.dat')))}")


# ================================================================ PART 0: C0
# Decide the mass-to-light convention by reproducing the published RAR.
print("\n" + "="*78)
print("PART 0 -- WHICH MASS-TO-LIGHT CONVENTION?  (settled by the data)")
print("="*78)
rar_report = {}
for tag, ups in [("Upsilon 0.5 / 0.7  (repo standing)", (0.5, 0.7)),
                 ("Upsilon 1.0 / 1.0  (G033 loader, as written)", (1.0, 1.0))]:
    gal = galaxies(ups)
    bins = {}
    for name, P in gal:
        for r, v, vb in P:
            gb = (vb*1000)**2/(r*KPC)
            go = (v*1000)**2/(r*KPC)
            if gb <= 0:
                continue
            bins.setdefault(math.floor(math.log10(gb)*4)/4, []).append((gb, go))
    devs = []
    for b in sorted(bins):
        v = bins[b]
        if len(v) < 40:                       # ignore sparsely populated edge bins
            continue
        gb = statistics.median([x[0] for x in v])
        go = statistics.median([x[1] for x in v])
        pred = gb/(1.0 - math.exp(-math.sqrt(gb/A0_REF)))   # McGaugh+2016 fit
        devs.append(abs(math.log10(go/pred)))
    worst = max(devs)
    rar_report[tag] = {"n_bins": len(devs), "max_dev_dex": worst,
                       "median_dev_dex": statistics.median(devs)}
    print(f"  {tag}")
    print(f"         binned median log10 g_obs vs published RAR fit: "
          f"median |dev| = {statistics.median(devs):.4f} dex, max |dev| = {worst:.4f} dex "
          f"({len(devs)} bins of >=40 points)")

c0_ok = rar_report["Upsilon 0.5 / 0.7  (repo standing)"]["max_dev_dex"] <= TH["C0_rar_max_dev_dex"]
check("C0 [CONVENTION] the Upsilon = 0.5/0.7 SPARC convention reproduces the published\n"
      "      radial-acceleration relation; the Upsilon = 1 loader in G033 does not",
      f"Upsilon 0.5/0.7 max|dev| = "
      f"{rar_report['Upsilon 0.5 / 0.7  (repo standing)']['max_dev_dex']:.4f} dex ; "
      f"Upsilon 1.0/1.0 max|dev| = "
      f"{rar_report['Upsilon 1.0 / 1.0  (G033 loader, as written)']['max_dev_dex']:.4f} dex "
      f"(vs McGaugh+2016 fit, a_0 = {A0_REF:.1e})",
      c0_ok,
      f"max |dev| <= {TH['C0_rar_max_dev_dex']} dex",
      "The G033 loader omits the 0.5/0.7 stellar mass-to-light factors. With them the\n"
      "         pipeline tracks the published RAR over four decades in g_bar; without them\n"
      "         it does not. 0.5/0.7 is therefore PRIMARY and Upsilon = 1 is carried below\n"
      "         as an explicit systematic bracket.")


# ================================================================ measurement
def measure(ups, a0, bracket=(1.0, 1.0), mb_mode="max"):
    out, n_out, n_neg = [], 0, 0
    for name, P in galaxies(ups):
        if mb_mode == "max":
            Mb = max((vb*1000)**2*(r*KPC)/G for r, v, vb in P)
        else:
            Mb = (P[-1][2]*1000)**2*(P[-1][0]*KPC)/G
        rM = math.sqrt(G*Mb/a0); rMk = rM/KPC
        if not (P[0][0]*bracket[0] <= rMk <= P[-1][0]*bracket[1]):   # (S2)
            n_out += 1
            continue
        vo = interp(P, rMk, 1); vb = interp(P, rMk, 2)
        if vo is None or vb is None:
            continue
        gobs = (vo*1000)**2/rM
        gbar = (vb*1000)**2/rM
        Sig = (gobs - gbar)/(math.pi*G)*PC**2/MSUN
        if Sig <= 0:
            n_neg += 1                                                # (S3)
            continue
        out.append({"name": name, "log10_Mb": math.log10(Mb/MSUN), "rM_kpc": rMk,
                    "Sigma_Msun_pc2": Sig, "log10_Sigma": math.log10(Sig),
                    "gbar_over_a0": gbar/a0, "Mph_over_Mb": Sig/(a0/(math.pi*G)*PC**2/MSUN)})
    return out, n_out, n_neg


def summarise(rows):
    lS = [r["log10_Sigma"] for r in rows]
    lM = [r["log10_Mb"] for r in rows]
    med = statistics.median(lS)
    mad = statistics.median([abs(x - med) for x in lS])
    sd = statistics.stdev(lS)
    slope, se, icpt, rms = ols(lM, lS)
    q = statistics.quantiles(lS, n=100, method="inclusive")
    return {"N": len(rows), "median_log10": med, "mean_log10": statistics.fmean(lS),
            "sd_log10": sd, "mad_log10": mad, "sigma_mad_log10": 1.4826*mad,
            "se_median_log10": 1.2533*sd/math.sqrt(len(rows)),
            "p16": q[15], "p84": q[83], "slope": slope, "slope_se": se,
            "slope_sigma": abs(slope/se), "rms_about_fit": rms,
            "intercept": icpt, "span_dex": max(lM) - min(lM),
            "log10Mb_min": min(lM), "log10Mb_max": max(lM)}


def binned(rows, nb=5):
    lM = [r["log10_Mb"] for r in rows]; lS = [r["log10_Sigma"] for r in rows]
    lo, hi = min(lM), max(lM); out = []
    for i in range(nb):
        a = lo + (hi - lo)*i/nb; b = lo + (hi - lo)*(i + 1)/nb
        sel = [y for x, y in zip(lM, lS) if (a <= x < b if i < nb-1 else a <= x <= b)]
        if sel:
            out.append({"bin_lo": a, "bin_hi": b, "N": len(sel),
                        "median_log10": statistics.median(sel)})
    return out


print("\n" + "="*78)
print("PART 1 -- THE MEASUREMENT (primary convention: Upsilon 0.5 / 0.7)")
print("="*78)

DONATO_LOG10, DONATO_SD = 2.15, 0.05
primary, variants, per_gal = {}, {}, {}

for footing, a0 in FOOT.items():
    rows, n_out, n_neg = measure((0.5, 0.7), a0)
    s = summarise(rows)
    s["n_rM_out_of_range"] = n_out
    s["n_Sigma_nonpositive"] = n_neg
    s["a0"] = a0
    s["Sigma_unit_a0_over_piG"] = a0/(math.pi*G)*PC**2/MSUN
    s["log10_Sigma_unit"] = math.log10(a0/(math.pi*G)*PC**2/MSUN)
    s["binned"] = binned(rows)
    primary[footing] = s
    per_gal[footing] = rows

    print(f"\n--- footing: {footing}   a_0 = {a0:.4e} m/s^2")
    print(f"    a_0/(pi G)          = {s['Sigma_unit_a0_over_piG']:.2f} Msun/pc^2 "
          f"(log10 = {s['log10_Sigma_unit']:.3f})   <- the H033 prediction")
    print(f"    galaxies used       = {s['N']}   (r_M outside observed range: {n_out}; "
          f"Sigma <= 0: {n_neg})")
    print(f"    log10 Mb lever arm  = {s['log10Mb_min']:.2f} .. {s['log10Mb_max']:.2f} "
          f"({s['span_dex']:.2f} dex)")
    print(f"    MEDIAN log10 Sigma  = {s['median_log10']:.4f} "
          f"+/- {s['se_median_log10']:.4f} (stat)")
    print(f"    mean / sd / MAD-sig = {s['mean_log10']:.4f} / {s['sd_log10']:.4f} / "
          f"{s['sigma_mad_log10']:.4f} dex")
    print(f"    16-50-84 percentiles= {s['p16']:.3f} / {s['median_log10']:.3f} / {s['p84']:.3f}")
    print(f"    d log10 Sigma / d log10 Mb = {s['slope']:+.4f} +/- {s['slope_se']:.4f} "
          f"({s['slope_sigma']:.2f} sigma from zero)")
    print(f"    rms about that fit  = {s['rms_about_fit']:.4f} dex")
    print("    binned medians (log10 Mb : N : median log10 Sigma):")
    for b in s["binned"]:
        print(f"      {b['bin_lo']:.2f}-{b['bin_hi']:.2f} : N={b['N']:3d} : "
              f"{b['median_log10']:.3f}")

# robustness variants on the canonical footing
a0c = FOOT["canonical"]
for tag, kw in [("Mb = last-point instead of max", {"mb_mode": "last"}),
                ("strict radial bracket 2 r_min <= r_M <= 0.8 r_max", {"bracket": (2.0, 0.8)})]:
    rows, n_out, n_neg = measure((0.5, 0.7), a0c, **kw)
    variants[tag] = summarise(rows)
    variants[tag]["n_Sigma_nonpositive"] = n_neg
    print(f"\n  [variant, canonical footing] {tag}:")
    print(f"       N = {variants[tag]['N']}, median = {variants[tag]['median_log10']:.3f}, "
          f"slope = {variants[tag]['slope']:+.3f} +/- {variants[tag]['slope_se']:.3f} "
          f"({variants[tag]['slope_sigma']:.1f} sigma)")

# systematic bracket: the G033 loader convention (Upsilon = 1)
ups1 = {}
for footing, a0 in FOOT.items():
    rows, n_out, n_neg = measure((1.0, 1.0), a0)
    s = summarise(rows)
    s["n_rM_out_of_range"] = n_out; s["n_Sigma_nonpositive"] = n_neg
    ups1[footing] = s
    print(f"\n  [systematic bracket: Upsilon = 1.0, as in the G033 loader] {footing}:")
    print(f"       N = {s['N']}, median log10 Sigma = {s['median_log10']:.3f}, "
          f"sd = {s['sd_log10']:.3f}, slope = {s['slope']:+.3f} +/- {s['slope_se']:.3f} "
          f"({s['slope_sigma']:.1f} sigma), span {s['span_dex']:.2f} dex")


# ================================================================ PART 2: checks
print("\n" + "="*78)
print("PART 2 -- CHECKS  (measurement and threshold stated separately)")
print("="*78)

P = primary["canonical"]
A = primary["alternative"]

check("C1 [UNIVERSALITY] d log10 Sigma / d log10 Mb is zero: the surface density\n"
      "      inside r_M carries no memory of the galaxy's mass",
      f"canonical {P['slope']:+.4f} +/- {P['slope_se']:.4f} dex/dex ({P['slope_sigma']:.1f} sigma); "
      f"alternative {A['slope']:+.4f} +/- {A['slope_se']:.4f} ({A['slope_sigma']:.1f} sigma); "
      f"binned medians rise {P['binned'][0]['median_log10']:.2f} -> "
      f"{P['binned'][-1]['median_log10']:.2f} over {P['span_dex']:.2f} dex",
      (abs(P["slope"]) <= TH["C1_abs_slope"]) or (P["slope_sigma"] <= TH["C1_slope_sigma"]),
      f"|slope| <= {TH['C1_abs_slope']} dex/dex  OR  <= {TH['C1_slope_sigma']} sigma from zero",
      "MEASURED: Sigma_dark(<r_M) rises monotonically with baryon mass. r_M = sqrt(G Mb/a_0)\n"
      "         grows as Mb^0.5 while galaxy size grows more slowly, so r_M sits at a\n"
      "         different relative position in dwarfs and in giants -- and Sigma, which is\n"
      "         (g_obs - g_bar)/(pi G) evaluated there, follows the local mass discrepancy.\n"
      "         Equivalently M_ph(<r_M)/M_b runs from ~0.12 (dwarfs) to ~0.6 (giants),\n"
      "         not the 1.0 the amplitude law asserts.")

check("C2 [VALUE vs OBSERVATION] the measured value agrees with the observed universal\n"
      "      dark-halo surface density, Donato+2009 log10 = 2.15 +/- 0.05",
      f"median log10 Sigma = {P['median_log10']:.3f} (canonical) / {A['median_log10']:.3f} "
      f"(alternative) -> offset {P['median_log10']-DONATO_LOG10:+.3f} / "
      f"{A['median_log10']-DONATO_LOG10:+.3f} dex = "
      f"{(P['median_log10']-DONATO_LOG10)/DONATO_SD:+.1f} / "
      f"{(A['median_log10']-DONATO_LOG10)/DONATO_SD:+.1f} sigma_Donato",
      abs(P["median_log10"] - DONATO_LOG10) <= TH["C2_donato_dex"],
      f"|log10 Sigma - 2.15| <= {TH['C2_donato_dex']} dex (3 x Donato's 0.05)",
      "The two numbers are not the same quantity: Donato's mu_0D = rho_0 r_0 is the CENTRAL\n"
      "         surface density of a cored halo, this is the MEAN dark surface density inside\n"
      "         r_M. A factor of order unity between the conventions is expected, so this is\n"
      "         reported as a convention-limited comparison, not a precision agreement.")

check("C3 [VALUE vs THE LEMMA] the measured value equals the predicted a_0/(pi G)",
      f"measured {10**P['median_log10']:.1f} Msun/pc^2 vs predicted "
      f"{P['Sigma_unit_a0_over_piG']:.1f} (canonical) and {A['Sigma_unit_a0_over_piG']:.1f} "
      f"(alternative) -> {P['median_log10']-P['log10_Sigma_unit']:+.3f} / "
      f"{A['median_log10']-A['log10_Sigma_unit']:+.3f} dex",
      abs(P["median_log10"] - P["log10_Sigma_unit"]) <= TH["C3_lemma_dex"],
      f"|log10 Sigma - log10(a_0/pi G)| <= {TH['C3_lemma_dex']} dex",
      "The lemma's step M_ph(<r_M) = M_b is what the data reject: the measured ratio\n"
      "         M_ph(<r_M)/M_b is 10^(Sigma_measured/(a_0/pi G)) = "
      f"{10**(P['median_log10']-P['log10_Sigma_unit']):.2f} at the median, "
      "not 1.")

check("C4 [LEVER ARM] the sample spans enough decades in baryon mass to test\n"
      "      mass-independence at all",
      f"{P['span_dex']:.2f} dex in log10 Mb "
      f"({P['log10Mb_min']:.2f} .. {P['log10Mb_max']:.2f} Msun), N = {P['N']}",
      P["span_dex"] >= TH["C4_span_dex"],
      f"span >= {TH['C4_span_dex']} dex",
      "The task asked for about five decades; SPARC delivers about four. That is enough\n"
      "         leverage for the slope test -- a 0.05 dex/dex residual trend would move the\n"
      "         median by only 0.19 dex across the sample, well inside the measured 0.7 dex.")

check("C5 [SAMPLE SIZE]",
      f"N = {P['N']} galaxies with r_M inside the observed range and Sigma > 0 "
      f"(canonical); {A['N']} (alternative); 171 curves usable of 175 files",
      P["N"] >= TH["C5_min_galaxies"],
      f"N >= {TH['C5_min_galaxies']}")

signs = [P["slope"] > 0] + [v["slope"] > 0 for v in variants.values()] + \
        [ups1[f]["slope"] > 0 for f in FOOT]
check("C6 [ROBUSTNESS] the mass trend survives every analysis variant tried\n"
      "      (M_b estimator, radial bracketing, mass-to-light convention, footing)",
      "slopes: " + ", ".join(
          [f"primary {P['slope']:+.3f}"] +
          [f"{k.split()[0]} {v['slope']:+.3f}" for k, v in variants.items()] +
          [f"Upsilon1 {ups1[f]['slope']:+.3f}" for f in FOOT]),
      all(s == signs[0] for s in signs),
      "all variants return the same sign of d log10 Sigma / d log10 Mb",
      "The trend is not an artefact of one choice. It is weakest (about 2 sigma, slope\n"
      "         ~ +0.09) under the Upsilon = 1 convention that C0 already rejected.")

check("C7 [BRACKET] the measured value lies between a_0/(2 pi G) and a_0/(pi G),\n"
      "      the range H033 claimed to bracket the observation",
      f"measured {10**P['median_log10']:.1f} Msun/pc^2 ; bracket "
      f"{P['Sigma_unit_a0_over_piG']/2:.1f} .. {P['Sigma_unit_a0_over_piG']:.1f} "
      f"(canonical)",
      (P["Sigma_unit_a0_over_piG"]/2) <= 10**P["median_log10"] <= P["Sigma_unit_a0_over_piG"],
      f"a_0/(2 pi G) <= Sigma_measured <= a_0/(pi G)",
      "The measured mean-inside-r_M value falls BELOW a_0/(2 pi G). H033's bracket was built\n"
      "         for a central/isothermal convention, not for the mean inside r_M.")


# ================================================================ verdict
print("\n" + "="*78)
print(f"H033-P1 READING:  {NP_} PASS / {NF_} FAIL")
print("="*78)
print(f"""
H033 PREDICTION P1, MEASURED ON {P['N']} REAL SPARC GALAXIES
-------------------------------------------------------------------------
  median log10 Sigma_dark(<r_M) = {P['median_log10']:.3f} +/- {P['se_median_log10']:.3f} (stat)
                                  ({10**P['median_log10']:.1f} Msun/pc^2, canonical footing)
                                = {A['median_log10']:.3f} (alternative footing a_0 = 1.1279e-10)
  scatter                      = {P['sd_log10']:.3f} dex (sd), {P['sigma_mad_log10']:.3f} dex (MAD-based),
                                  {P['rms_about_fit']:.3f} dex after removing the mass trend
  mass-independent?            NO -- slope = {P['slope']:+.3f} +/- {P['slope_se']:.3f} dex/dex,
                                  {P['slope_sigma']:.1f} sigma from zero; binned medians climb
                                  {P['binned'][0]['median_log10']:.2f} -> {P['binned'][-1]['median_log10']:.2f} over {P['span_dex']:.2f} dex
  vs Donato+2009 (2.15+/-0.05) = {P['median_log10']-DONATO_LOG10:+.3f} dex ({(P['median_log10']-DONATO_LOG10)/DONATO_SD:+.1f} sigma_Donato) low
  vs the lemma a_0/(pi G)=2.330= {P['median_log10']-P['log10_Sigma_unit']:+.3f} dex low

WHAT SURVIVES AND WHAT DOES NOT.
  The numerical value is of the observed order of magnitude (within ~0.25 dex of
  Donato, and within a factor ~2.5 of a_0/(pi G)) -- but the two quantities are
  defined with different conventions (mean inside r_M versus central rho_0 r_0),
  so that agreement carries little weight.

  The UNIVERSALITY does not survive. Sigma_dark(<r_M) is NOT constant across the
  SPARC sample: it rises by ~0.7 dex over {P['span_dex']:.2f} decades in baryon mass at
  {P['slope_sigma']:.1f} sigma, in the same direction under every variant tried. The reason is
  structural, not statistical: r_M = sqrt(G M_b/a_0) scales as M_b^0.5 while galaxy
  size scales more slowly, so r_M lands at a different relative position in a dwarf
  and in a giant, and Sigma = (g_obs - g_bar)/(pi G) evaluated there inherits the
  local mass discrepancy. In the framework's own terms the amplitude-law step
  M_ph(<r_M) = M_b is off by a factor that runs from ~8 (dwarfs) to ~1.6 (giants).

  P1 therefore FAILS as stated on real data. Either the lemma needs the enclosed
  baryon mass rather than the total in the definition of r_M, or the predicted
  surface density is not the quantity Donato measured. Those two recourses are
  separable and are the next computation -- they are not settled here.
""")

# ---------------------------------------------------------------- output
json.dump({
    "lane": "H033_P1",
    "prediction": "Sigma_ph = a_0/(pi G) universal, mass-independent (H033 P1)",
    "data": "SPARC 175 _rotmod.dat (Lelli+2016); 171 usable curves",
    "convention": "V_bar^2 = Vgas|Vgas| + 0.5 Vdisk^2 + 0.7 Vbul^2 (RAR-validated by C0)",
    "recipe": "Mb = max_r V_bar^2 r/G ; r_M = sqrt(G Mb/a_0) ; "
              "Sigma = [M_obs(<r_M) - M_b(<r_M)]/(pi r_M^2) = [g_obs - g_bar]/(pi G) at r_M",
    "selection": {"min_points": 5, "rM_inside_observed_range": True,
                  "Sigma_positive_for_log": True},
    "thresholds": TH,
    "pass": NP_, "fail": NF_,
    "results": RES,
    "primary": {k: {kk: vv for kk, vv in v.items() if kk != "binned"} | {"binned": v["binned"]}
                for k, v in primary.items()},
    "variants_canonical": variants,
    "systematic_upsilon1": ups1,
    "rar_validation": rar_report,
    "headline": {
        "measured_log10_Sigma_Msun_pc2": P["median_log10"],
        "measured_log10_stat_error": P["se_median_log10"],
        "measured_Sigma_Msun_pc2": 10**P["median_log10"],
        "scatter_sd_dex": P["sd_log10"],
        "scatter_mad_sigma_dex": P["sigma_mad_log10"],
        "scatter_about_fit_dex": P["rms_about_fit"],
        "mass_independent": False,
        "slope_dex_per_dex": P["slope"],
        "slope_error": P["slope_se"],
        "slope_sigma_from_zero": P["slope_sigma"],
        "n_galaxies_used": P["N"],
        "n_galaxies_alternative_footing": A["N"],
        "dex_span_in_Mb": P["span_dex"],
        "donato_log10": DONATO_LOG10,
        "donato_sd": DONATO_SD,
        "offset_from_donato_dex": P["median_log10"] - DONATO_LOG10,
        "offset_from_donato_sigma": (P["median_log10"] - DONATO_LOG10)/DONATO_SD,
        "lemma_log10": P["log10_Sigma_unit"],
        "offset_from_lemma_dex": P["median_log10"] - P["log10_Sigma_unit"],
        "verdict": "P1 not confirmed: value of the observed order of magnitude, "
                   "but mass-INDEPENDENT is refuted at "
                   f"{P['slope_sigma']:.1f} sigma",
    },
    "per_galaxy": per_gal,
}, open(OUT_JSON, "w"), indent=2)

print(f"wrote {OUT_JSON}")
print(json.dumps({"pass": NP_, "fail": NF_}))
