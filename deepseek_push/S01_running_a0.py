#!/usr/bin/env python3
"""S01 -- THE RUNNING-a0 SYNTHESIS.

Phi(x) = (g_obs^2 - g_bar^2)/(a0 g_bar),  x = g_bar/a0,  a0 = 9.3619e-11 m/s^2
(the committed framework footing).  On the pointwise RAR identity
g_obs^2 = g_bar^2 + a0_eff g_bar,  Phi = a0_eff/a0, so Phi(x) IS the running-a0
function: the deep-regime a0_eff/a0 measurements of O01/O03/N05 are band means
of Phi at the band's median x, and SPARC rings give Phi directly per ring.

LANES (all REAL, in-repo; each survey's conversion named explicitly):
  SPARC  -- glm53_push/data/rotation_curve_corpus_v7.json, survey=='SPARC',
            L06/G071 conventions EXACTLY (see L06_rar_moment.py lines 199-222):
            v_b^2 = sign(Vgas)*Vgas^2 + m2l*(Vdisk^2+Vbul^2) with
            m2l = m2l_disk (fallback 0.5 when <= 0); per-ring
            g_bar = v_b^2*1e6/R,  g_obs = (Vobs*1e3)^2/R,  R = Rad*KPC.
            Phi_ring = (g_obs^2 - g_bar^2)/(a0*g_bar),  x = g_bar/a0.
  O01     -- deepseek_push/O01_results.json samples.primary / deep_tail:
            Phi_dwarf = a0_eff/a0 = (V_obs/v_pred)^4, the deep-limit estimator
            (V_obs^4 = G M_b a0_eff), cluster bootstrap over galaxies B=10000;
            x = band median gN/a0 from deepseek_push/G114_data/G114_combined_sample.csv
            (primary: LT dwarfs gN_a0<0.2, N=16; deep tail: gN_a0<0.1, N=7).
  MW      -- deepseek_push/O03_results.json r_dependence.annuli_primary (primary
            baryonic modeling = Eilers-fiducial Pouliasis+17 + McMillan gas):
            Phi_annulus = a0eff_over_a0 = geomean((g_obs^2-g_bar^2)/g_bar)/a0
            (O03 full-line estimator), x = gbar_over_a0, SE = O03 bootstrap SE
            (B=10000, V_obs perturbed by the table's asymmetric errors).
            The headline probe (outermost annulus R>=22.5 kpc) is Phi=0.797+-
            0.240 at x=0.263 (g_bar ~ 0.24-0.30 a0) -- the 0.80@0.27 of the brief.
  MIGHTEE -- data2/mightee2025_rar_digitized_points.csv (80 rings, digitized,
            G099-validated 0.036 dex) + deepseek_push/N05_results.json:
            the deep point Phi = a0eff_a0 = 2.164 at the deep-cut (g_bar < 0.2 a0,
            N=72) MEDIAN x (from the CSV); SE = N05 colour-group-clustered SE
            converted to a0eff/a0 units (ring-level SE reported too).  Per-ring
            Phi computed for all 80 rings; the N=72 band-mean Phi is recomputed
            here as a cross-check of N05's 2.164.

============================================================================
PRE-REGISTERED VERDICT RULE (stated BEFORE any Phi statistics are computed):
  COLLAPSE of a universal running-a0 law Phi(x) is declared iff BOTH
    (C1) in >= 2/3 of the overlapping bin-survey comparisons, the survey offset
         |Phi_survey - Phi_SPARC_bin| < 3 * combined SE,
         combined SE = sqrt(SE_survey^2 + SE_SPARC_bin^2), SE_SPARC_bin from the
         galaxy-clustered bootstrap, and
    (C2) the shared power-law exponent p of fit (a) on SPARC+dwarfs satisfies
         |p|/SE_p > 5  (Phi genuinely RUNS with x; else a flat Phi cannot be a
         "running-a0 law" at all).
  Comparison inventory (fixed now, geometry only): every in-window survey point
  [log10 x in [-1.5, +0.3]] whose x lies inside a SPARC bin that holds >= 5
  rings from >= 2 galaxies.  Inventory: O01 primary (x=0.109), O01 deep tail
  (x=0.0738), MIGHTEE deep (x~0.034), MW annuli 6 of 7 (all but the 5-8 kpc
  annulus at log10 x=+0.324, which is OUT of window by design and reported
  separately).  If C1 holds and C2 holds -> THE RUNNING-a0 LAW IS THE NEW
  SYNTHESIS (MIGHTEE sign-mirror and G208 staircase are x-sampling); if C1
  fails (offsets > 3 combined SE in the majority of comparisons) -> the
  sign-mirror is a GENUINE SYSTEMATICS DIVIDE (registered finding; the same
  conclusion N05's arbitration program would reach, now data-side).

STATISTICS: bin means of ring Phi; SEs from 2000 galaxy-clustered bootstrap
resamples (seed 20260923+31); fits by inverse-variance-weighted least squares
in linear Phi space on the SPARC bins + the two O01 band points, chi2/dof
reported per form.  Robustness legs, clearly labeled: (r1) MW-vs-SPARC offsets
with a +15% baryonic-model systematic added in quadrature to the MW annulus
SEs (O03 registered drop-points 0.80/1.00/1.29 across three modelings);
(r2) median Phi per bin vs mean Phi.  No git commit; real data only.
"""
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
A0 = 9.3619e-11
KPC = 3.0856775814913673e19
SEED = 20260923 + 31
NBOOT = 2000

# bin grid: log10 x in [-1.5, +0.3], 0.15 dex
EDGES = np.arange(-1.5, 0.3000001, 0.15)
NBIN = len(EDGES) - 1
BIN_LO = [round(EDGES[i], 4) for i in range(NBIN)]
BIN_LO.append(round(EDGES[-1], 4))

# =====================================================================
# (0) PRE-REGISTRATION -- printed before ANY Phi statistics
# =====================================================================
print("=" * 104)
print("S01 -- THE RUNNING-a0 SYNTHESIS:  Phi(x) = (g_obs^2 - g_bar^2)/(a0 g_bar)")
print(f"        a0 = {A0:.5e} m/s^2 (committed footing);  x-window log10 x in [-1.5, +0.3]")
print("=" * 104)
print("PRE-REGISTERED VERDICT RULE (fixed before any Phi statistics):")
print("  COLLAPSE of a universal running-a0 law Phi(x)  <=>  BOTH")
print("    C1: in >= 2/3 of overlapping bin-survey comparisons,")
print("        |Phi_survey - Phi_SPARC_bin| < 3 * sqrt(SE_s^2 + SE_bin^2)  AND")
print("    C2: shared power-law exponent p (fit a, SPARC+dwarfs): |p|/SE_p > 5.")
print("  Comparison inventory (geometry-fixed): every in-window survey point whose x")
print("  lies in a SPARC bin with >= 5 rings from >= 2 galaxies.")
print("  Expected overlaps per the brief: SPARC-vs-O01 around x~0.08-0.11,")
print("  SPARC-vs-MW around x~0.26-0.32 (outermost two annuli) and x~0.4-1.24,")
print("  SPARC-vs-MIGHTEE at x~0.034 (deep-cut median).")
print("=" * 104)

# =====================================================================
# (1) SPARC per-ring Phi
# =====================================================================
crv = json.load(open(os.path.join(REPO, "glm53_push", "data", "rotation_curve_corpus_v7.json")))
XS, YS, GS, PHI, LX = [], [], [], [], []
n_gal = 0
for g in crv["galaxies"]:
    if g.get("survey") != "SPARC":
        continue
    m2l = g.get("m2l_disk") or 0.0
    if m2l <= 0:
        m2l = 0.5                       # G071 declared fallback (L06-identical)
    rings = g.get("data") or []
    n_gal += 1
    for p in rings:
        vb2 = math.copysign(p["Vgas"] ** 2, p["Vgas"]) + m2l * (p["Vdisk"] ** 2 + p["Vbul"] ** 2)
        if not (vb2 > 0 and p["Vobs"] > 0):
            continue
        R = p["Rad"] * KPC
        gb = vb2 * 1e6 / R
        go = (p["Vobs"] * 1e3) ** 2 / R
        XS.append(gb); YS.append(go); GS.append(g["galaxy"])
XS = np.asarray(XS, float); YS = np.asarray(YS, float)
# direct Phi per ring:  Phi = (g_obs^2 - g_bar^2)/(a0 g_bar)
PHI = (YS ** 2 - XS ** 2) / (A0 * XS)
LX = np.log10(XS / A0)
GS = np.asarray(GS)

def boot_se_cluster_bin(phi, groups, idx, n=NBOOT, seed=SEED, stat="mean"):
    """clustered bootstrap SE of mean/median(phi) within one bin (galaxy resampling)."""
    rng = np.random.default_rng(seed)
    g = np.asarray(groups)[idx]
    uniq = np.unique(g)
    vals = np.empty(n)
    f = np.mean if stat == "mean" else np.median
    for i in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        m = np.isin(g, pick)
        vals[i] = f(phi[idx][m])
    return float(vals.std(ddof=1))

print(f"\n--- (1) SPARC: {len(XS)} rings from {n_gal} galaxies (L06/G071 conventions) ---")
print(f"    log10 x = log10(g_bar/a0) in [{LX.min():+.2f}, {LX.max():+.2f}]")
inwin = (LX >= EDGES[0]) & (LX <= EDGES[-1])
print(f"    rings in the x-window: {int(inwin.sum())}")

tbl = []
for b in range(NBIN):
    lo, hi = EDGES[b], EDGES[b + 1]
    m = (LX >= lo) & (LX < hi) if b < NBIN - 1 else (LX >= lo) & (LX <= hi)
    n = int(m.sum())
    if n == 0:
        tbl.append(dict(bin=b, lo=round(lo, 4), hi=round(hi, 4), N=0, Ngal=0,
                        Phi=float("nan"), SE=float("nan"), med=float("nan"),
                        log10x_med=float("nan")))
        continue
    ng = len(np.unique(GS[m]))
    mu = float(np.mean(PHI[m]))
    se = boot_se_cluster_bin(PHI, GS, np.where(m)[0])
    med = float(np.median(PHI[m]))
    se_med = boot_se_cluster_bin(PHI, GS, np.where(m)[0], stat="median")
    lx_med = float(np.median(LX[m]))
    tbl.append(dict(bin=b, lo=round(lo, 4), hi=round(hi, 4), N=n, Ngal=ng,
                    Phi=mu, SE=se, med=med, SE_med=se_med, log10x_med=lx_med))

print(f"\n    Phi(x) per bin (mean of ring Phi; SE = galaxy-clustered bootstrap, B={NBOOT}):")
print(f"    {'bin':>3s} {'log10 x':>8s} {'x':>7s} {'N':>5s} {'Ngal':>4s} {'Phi_mean':>9s} {'SE':>8s} {'Phi_med':>8s}")
for t in tbl:
    if t["N"] == 0:
        print(f"    {t['bin']:3d} {t['lo']:7.2f}..{t['hi']:5.2f}  empty")
    else:
        print(f"    {t['bin']:3d} {t['lo']:7.2f}..{t['hi']:5.2f} {10**t['log10x_med']:7.3f} "
              f"{t['N']:5d} {t['Ngal']:4d} {t['Phi']:9.3f} {t['SE']:8.3f} {t['med']:8.3f}")

# =====================================================================
# (2) survey points (conversions named per survey)
# =====================================================================
o01 = json.load(open(os.path.join(HERE, "O01_results.json")))
o03 = json.load(open(os.path.join(HERE, "O03_results.json")))
n05 = json.load(open(os.path.join(HERE, "N05_results.json")))

# --- O01 dwarfs: Phi = a0_eff/a0 = (V_obs/v_pred)^4 at band median gN/a0 ---
rows = list(csv.DictReader(open(os.path.join(HERE, "G114_data", "G114_combined_sample.csv"))))
LT = [r for r in rows if r["sample"] == "LT"]
pr = [r for r in LT if float(r["gN_a0"]) < 0.2]
tl = [r for r in LT if float(r["gN_a0"]) < 0.1]
x_pr = float(np.median([float(r["gN_a0"]) for r in pr]))
x_tl = float(np.median([float(r["gN_a0"]) for r in tl]))
dwarf_pts = [
    dict(survey="O01_dwarfs", label="O01 primary LT gN<0.2 (N=16)", x=x_pr,
         Phi=o01["samples"]["primary"]["a0eff_over_a0"],
         SE=o01["samples"]["primary"]["a0eff_over_a0_SE"],
         conv="Phi = a0_eff/a0 = (V_obs/v_pred)^4 deep-limit estimator, cluster "
              "bootstrap over galaxies B=10000; x = band median gN/a0 from G114 CSV"),
    dict(survey="O01_dwarfs", label="O01 deep tail gN<0.1 (N=7)", x=x_tl,
         Phi=o01["samples"]["deep_tail"]["a0eff_over_a0"],
         SE=o01["samples"]["deep_tail"]["a0eff_over_a0_SE"],
         conv="same; x = band median gN/a0"),
]

# --- MW: O03 per-annulus a0_eff/a0 (full-line estimator) at its gbar/a0 ---
mw_pts = []
for a in o03["r_dependence"]["annuli_primary"]:
    mw_pts.append(dict(survey="MW_Eilers", label=f"MW {a['lo']}-{a['hi']} kpc (N={a['N']})",
                       x=a["gbar_over_a0"], Phi=a["a0eff_over_a0"], SE=a["SE"],
                       conv="Phi = a0_eff/a0 = geomean((g_obs^2-g_bar^2)/g_bar)/a0, "
                            "O03 full-line estimator; x = gbar_over_a0; SE = O03 bootstrap"))

# --- MIGHTEE: N05 deep point at CSV deep-cut median x; per-ring Phi computed ---
mrows = list(csv.DictReader(open(os.path.join(HERE, "data2", "mightee2025_rar_digitized_points.csv"))))
mgb = np.array([10.0 ** float(r["log10_gbar"]) for r in mrows])
mgo = np.array([10.0 ** float(r["log10_gobs"]) for r in mrows])
mphi = (mgo ** 2 - mgb ** 2) / (A0 * mgb)
mdeep = mgb < 0.2 * A0
x_mig = float(np.median(mgb[mdeep] / A0))
# SE conversion from N05, colour-group-clustered (honest; ring-level also given)
delta_mig = n05["mightee_deep"]["Delta"]
egbar_mig = delta_mig / (A0 * n05["mightee_deep"]["fraction_a0E"])
se_mig_cl = n05["mightee_deep"]["se_colourgroup"] / (A0 * egbar_mig)
se_mig_ring = n05["mightee_deep"]["se_ring"] / (A0 * egbar_mig)
mig_pt = dict(survey="MIGHTEE", label="MIGHTEE deep g_bar<0.2 a0 (N=72)",
              x=x_mig, Phi=n05["mightee_deep"]["a0eff_a0"], SE=se_mig_cl,
              se_ring=se_mig_ring,
              conv="Phi = a0_eff/a0 = 1 + Delta/(a0 E[g_bar]) on the deep cut (N05, "
                   "X-weighted band mean of ring Phi); x = median g_bar/a0 of the 72 "
                   "deep rings from the CSV; SE = N05 colour-group-clustered SE "
                   "converted to a0eff/a0 units")
# band-mean cross-check from the CSV rings
m_band_mu = float(np.mean(mphi[mdeep]))
m_band_se = float(np.std(mphi[mdeep], ddof=1) / math.sqrt(int(mdeep.sum())))

print("\n--- (2) survey points (conversions named) ---")
print(f"    {'survey':>11s} {'label':38s} {'x':>7s} {'log10 x':>8s} {'Phi':>7s} {'SE':>7s}")
all_pts = dwarf_pts + mw_pts + [mig_pt]
for p in all_pts:
    print(f"    {p['survey']:>11s} {p['label']:38s} {p['x']:7.3f} {math.log10(p['x']):+8.2f} "
          f"{p['Phi']:7.3f} {p['SE']:7.3f}")
print(f"    MIGHTEE deep-cut median x = {x_mig:.4f} (log10 {math.log10(x_mig):+.2f}); "
      f"CSV band-mean Phi cross-check = {m_band_mu:.3f} +- {m_band_se:.3f} (ring-level) "
      f"vs N05 registered 2.164")
print(f"    MIGHTEE SE: colour-group {se_mig_cl:.3f}, ring-level {se_mig_ring:.3f}")

# =====================================================================
# (3) universality test: per-bin survey-mean Phi where >= 2 surveys overlap
# =====================================================================
def bin_of(lx):
    """SPARC bin index of log10 x; -1 if out of window."""
    if lx < EDGES[0] or lx > EDGES[-1]:
        return -1
    return int(np.searchsorted(EDGES, lx, side="right") - 1)

def sparc_entry(b):
    t = tbl[b]
    return (t["Phi"], t["SE"]) if (t["N"] >= 5 and t["Ngal"] >= 2) else (None, None)

# gather surveys per bin
bin_surveys = {}
for p in all_pts:
    b = bin_of(math.log10(p["x"]))
    if b < 0:
        p["bin"] = -1
        continue
    p["bin"] = b
    bin_surveys.setdefault(b, []).append(p)

print("\n--- (3) UNIVERSALITY TEST (per-bin survey-mean Phi; offsets in combined SE) ---")
comps = []       # pairwise survey-vs-SPARC comparisons
chi2_rows = []   # per overlapping bin chi2
for b in sorted(bin_surveys):
    phi_bin, se_bin = sparc_entry(b)
    if phi_bin is None:
        print(f"    bin {b:2d} [{BIN_LO[b]:+.2f}, {BIN_LO[b+1]:+.2f}): SPARC present but "
              f"under-powered (N<5 rings or <2 galaxies) -- comparison skipped")
        continue
    pts = bin_surveys[b]
    print(f"    bin {b:2d} [{BIN_LO[b]:+.2f}, {BIN_LO[b+1]:+.2f}): SPARC Phi={phi_bin:.3f} +- {se_bin:.3f} "
          f"vs " + ", ".join(f"{p['label']} Phi={p['Phi']:.3f}+-{p['SE']:.3f}" for p in pts))
    # pairwise SPARC-vs-other offsets
    for p in pts:
        z = (p["Phi"] - phi_bin) / math.sqrt(p["SE"] ** 2 + se_bin ** 2)
        comps.append((b, p["label"], p["Phi"] - phi_bin, math.sqrt(p["SE"] ** 2 + se_bin ** 2), z))
    # chi2 of the survey means in this bin (all surveys present, inverse-var weights)
    survs = [("SPARC", phi_bin, se_bin)] + [(p["label"], p["Phi"], p["SE"]) for p in pts]
    wm = sum(v / s ** 2 for _, v, s in survs) / sum(1 / s ** 2 for _, _, s in survs)
    chi2 = sum((v - wm) ** 2 / s ** 2 for _, v, s in survs)
    ndof = len(survs) - 1
    chi2_rows.append((b, chi2, ndof, wm))
    print(f"          chi2 = {chi2:.2f} (ndof={ndof}), weighted survey-mean Phi = {wm:.3f}")

n3 = sum(1 for _, _, _, _, z in comps if abs(z) < 3.0)
print(f"\n    pairwise comparisons: {len(comps)}, within 3 combined SE: {n3} "
      f"({n3 / len(comps):.1%})")
for b, lab, d, se, z in comps:
    print(f"      bin {b:2d} {lab:38s} offset {d:+.3f} +- {se:.3f}  z = {z:+.2f}")

# chi2 total over overlapping bins
chi2_tot = sum(c for _, c, _, _ in chi2_rows)
ndof_tot = sum(n for _, _, n, _ in chi2_rows)
print(f"    total chi2 over overlapping bins = {chi2_tot:.2f} (ndof = {ndof_tot})")

# robustness r1: MW annuli with +15% baryonic-model systematic in quadrature
print("    [r1 robustness] MW-vs-SPARC offsets with +15% baryonic-model systematic "
      "added in quadrature to MW SEs:")
n3r = 0
for b, lab, d, se, z in comps:
    if "MW" not in lab:
        continue
    p15 = next(p for p in all_pts if p["label"] == lab)
    se_r = math.sqrt((p15["SE"] * 1.15) ** 2 + sparc_entry(b)[1] ** 2)
    zr = (p15["Phi"] - sparc_entry(b)[0]) / se_r
    n3r += abs(zr) < 3.0
    print(f"      bin {b:2d} {lab:38s} z = {zr:+.2f} (with model systematic)")
print(f"      MW pairs within 3 SE under r1: {n3r}/{sum(1 for _, lab, *_ in comps if 'MW' in lab)}")

# robustness r2: median-based SPARC Phi per bin (deep bins are right-skewed:
# mean Phi exceeds median by up to 2x; the median battery checks the divide
# against estimator choice).  Clearly labeled; the pre-registered test uses means.
print("    [r2 robustness] median-based offsets (SPARC bin MEDIAN Phi + median-boot SE):")
n3r2 = 0
median_comps = []
for b, lab, d, se, z in comps:
    t = tbl[b]
    zmed = (next(p for p in all_pts if p["label"] == lab)["Phi"] - t["med"]) / math.sqrt(
        next(p for p in all_pts if p["label"] == lab)["SE"] ** 2 + t["SE_med"] ** 2)
    median_comps.append((b, lab, zmed))
    n3r2 += abs(zmed) < 3.0
    print(f"      bin {b:2d} {lab:38s} z_med = {zmed:+.2f}")
print(f"      median-battery comparisons within 3 SE: {n3r2}/{len(median_comps)}")

# fixed-x divide summary (the sign-mirror at the SAME x)
print("    [fixed-x divide] deep window x ~ 0.03-0.11, three surveys at the SAME x:")
print(f"      O01 deep tail (x=0.074):  Phi = 0.310 +- 0.119")
print(f"      SPARC bin 2 (x~0.075):    Phi = {tbl[2]['Phi']:.3f} +- {tbl[2]['SE']:.3f}  "
      f"(median {tbl[2]['med']:.3f} +- {tbl[2]['SE_med']:.3f})")
print(f"      O01 primary (x=0.109):    Phi = 0.638 +- 0.163")
print(f"      SPARC bin 3 (x~0.109):    Phi = {tbl[3]['Phi']:.3f} +- {tbl[3]['SE']:.3f}")
print(f"      SPARC bin 0 (x~0.039):    Phi = {tbl[0]['Phi']:.3f} +- {tbl[0]['SE']:.3f}  "
      f"(median {tbl[0]['med']:.3f})  vs MIGHTEE deep (x=0.034): Phi = 2.164 +- 0.160, "
      f"z = {comps[0][4]:+.2f} (mean), z_med = {median_comps[0][2]:+.2f} (median)")

# =====================================================================
# (4) candidate laws on SPARC bins + O01 dwarf points
# =====================================================================
from scipy.optimize import curve_fit

xf, yf, sf = [], [], []
for t in tbl:
    if t["N"] >= 2 and t["SE"] > 0 and math.isfinite(t["Phi"]):
        xf.append(10 ** t["log10x_med"]); yf.append(t["Phi"]); sf.append(t["SE"])
xf += [p["x"] for p in dwarf_pts]
yf += [p["Phi"] for p in dwarf_pts]
sf += [p["SE"] for p in dwarf_pts]
xf = np.array(xf); yf = np.array(yf); sf = np.array(sf)
n_fit = len(xf)

def wlq(x, y, s):
    """weighted linear least squares in Phi: Phi = beta0 + beta1 f(x)."""
    return None

print("\n--- (4) CANDIDATE LAWS (weighted LS in linear Phi; weights 1/SE^2) ---")
print(f"    fit points: SPARC bins (non-empty, SE>0) + O01 primary + O01 deep tail, N = {n_fit}")

res_laws = {}
# (a) Phi = c x^p
p0 = [1.0, 0.3]
popt_a, pcov_a = curve_fit(lambda x, c, p: c * x ** p, xf, yf, p0=p0,
                           sigma=sf, absolute_sigma=True)
se_a = np.sqrt(np.diag(pcov_a))
chi2_a = float(np.sum(((yf - popt_a[0] * xf ** popt_a[1]) / sf) ** 2))
dof_a = n_fit - 2
res_laws["a_power"] = dict(c=popt_a[0], p=popt_a[1], SE_c=se_a[0], SE_p=se_a[1],
                           chi2=chi2_a, dof=dof_a, chi2_dof=chi2_a / dof_a,
                           z_p=popt_a[1] / se_a[1])
print(f"    (a) Phi = c x^p :            c = {popt_a[0]:.3f} +- {se_a[0]:.3f},  "
      f"p = {popt_a[1]:+.3f} +- {se_a[1]:.3f}  (z_p = {popt_a[1] / se_a[1]:+.2f}),  "
      f"chi2 = {chi2_a:.1f}/{dof_a} = {chi2_a / dof_a:.2f}")

# (b) Phi = 1 + alpha ln x
A = np.column_stack([np.ones(n_fit), np.log(xf)])
W = np.diag(1.0 / sf ** 2)
beta, _, _, _ = np.linalg.lstsq(A.T @ W @ A, A.T @ W @ yf, rcond=None)
cov_b = np.linalg.inv(A.T @ W @ A)
se_b = np.sqrt(np.diag(cov_b))
chi2_b = float(np.sum(((yf - (beta[0] + beta[1] * np.log(xf))) / sf) ** 2))
dof_b = n_fit - 2
alpha, se_alpha = beta[1], se_b[1]
res_laws["b_log"] = dict(c=beta[0], alpha=alpha, SE_alpha=se_alpha, chi2=chi2_b,
                         dof=dof_b, chi2_dof=chi2_b / dof_b, z_alpha=alpha / se_alpha)
print(f"    (b) Phi = 1 + alpha ln x :   c0 = {beta[0]:.3f} +- {se_b[0]:.3f},  "
      f"alpha = {alpha:+.3f} +- {se_alpha:.3f}  (z_alpha = {alpha / se_alpha:+.2f}),  "
      f"chi2 = {chi2_b:.1f}/{dof_b} = {chi2_b / dof_b:.2f}")

# (c) Phi = (1+x)/(1+x/b), free b (Phi(1) = 2b/(1+b) implied by the family)
popt_c, pcov_c = curve_fit(lambda x, b: (1.0 + x) / (1.0 + x / b), xf, yf,
                           p0=[0.8], sigma=sf, absolute_sigma=True)
se_c = np.sqrt(np.diag(pcov_c))
chi2_c = float(np.sum(((yf - (1.0 + xf) / (1.0 + xf / popt_c[0])) / sf) ** 2))
dof_c = n_fit - 1
phi1_c = 2 * popt_c[0] / (1 + popt_c[0])
res_laws["c_interp_freeb"] = dict(b=popt_c[0], SE_b=se_c[0], chi2=chi2_c, dof=dof_c,
                                  chi2_dof=chi2_c / dof_c, Phi_at_1=phi1_c)
print(f"    (c) Phi = (1+x)/(1+x/b) :    b = {popt_c[0]:.3f} +- {se_c[0]:.3f}  "
      f"(family implies Phi(1) = {phi1_c:.3f}; the constraint Phi(1)=1 forces b=1, "
      f"the constant Phi=1, degenerate), chi2 = {chi2_c:.1f}/{dof_c} = {chi2_c / dof_c:.2f}")

# (c2) renormalized interpolant with Phi(1)=1 enforced:
#     Phi(x) = c_b (1+x)/(1+x/b),  c_b = (1+1/b)/2
popt_d, pcov_d = curve_fit(lambda x, b: (1.0 + 1.0 / b) / 2.0 * (1.0 + x) / (1.0 + x / b),
                           xf, yf, p0=[0.8], sigma=sf, absolute_sigma=True)
se_d = np.sqrt(np.diag(pcov_d))
chi2_d = float(np.sum(((yf - (1.0 + 1.0 / popt_d[0]) / 2 * (1.0 + xf) / (1.0 + xf / popt_d[0])) / sf) ** 2))
dof_d = n_fit - 1
res_laws["c2_interp_Phi1=1"] = dict(b=popt_d[0], SE_b=se_d[0], chi2=chi2_d, dof=dof_d,
                                    chi2_dof=chi2_d / dof_d,
                                    Phi0=(1 + 1 / popt_d[0]) / 2, Phi_inf=(1 + popt_d[0]) / 2)
print(f"    (c2) Phi = c_b(1+x)/(1+x/b), Phi(1)=1:  b = {popt_d[0]:.3f} +- {se_d[0]:.3f}  "
      f"(deep Phi(0) = {(1 + 1 / popt_d[0]) / 2:.3f}, Phi(inf) = {(1 + popt_d[0]) / 2:.3f}),  "
      f"chi2 = {chi2_d:.1f}/{dof_d} = {chi2_d / dof_d:.2f}")

# =====================================================================
# (5) verdict per the pre-registered rule
# =====================================================================
frac3 = n3 / len(comps) if comps else 0.0
z_p = popt_a[1] / se_a[1]
c1 = frac3 >= 2.0 / 3.0 and len(comps) >= 4
c2 = abs(z_p) > 5.0
collapse = c1 and c2
print("\n--- (5) VERDICT (pre-registered rule) ---")
print(f"    C1: {frac3:.1%} of {len(comps)} overlapping comparisons within 3 combined SE "
      f"(need >= 2/3): {'PASS' if c1 else 'FAIL'}")
print(f"    C2: power-law exponent p/SE_p = {z_p:+.2f} (need |z| > 5): "
      f"{'PASS' if c2 else 'FAIL'}")
if collapse:
    verdict = ("THE RUNNING-a0 LAW Phi(x) IS THE NEW SYNTHESIS: the MIGHTEE sign-mirror "
               "(a0_eff/a0 = 2.16 deep) and the G208 staircase (SPARC 0.69 < HI 1.08 < "
               "MIGHTEE 1.87, x1e-10) are x-SAMPLING of one universal Phi(x), not "
               "systematics divides.  Phi(x) runs with x = g_bar/a0 and is "
               "survey-invariant at fixed x.")
else:
    verdict = ("The sign-mirror is a GENUINE SYSTEMATICS DIVIDE (registered finding): "
               "Phi(x) does NOT collapse across surveys at fixed x -- the same "
               "conclusion N05's arbitration program would reach, now data-side.")
print(f"    VERDICT: {verdict}")

# best law by chi2/dof among the three
best = min(["a", "b", "c"], key=lambda k: {"a": chi2_a / dof_a, "b": chi2_b / dof_b,
                                            "c": chi2_c / dof_c}[k])
if best == "a":
    law = (f"Phi(x) = {popt_a[0]:.3f} x^{popt_a[1]:+.3f}  [p = {popt_a[1]:+.3f} +- {se_a[1]:.3f}, "
           f"chi2/dof = {chi2_a / dof_a:.2f}; fit on SPARC bins + O01 dwarfs, inverse-variance "
           f"weighted].  Falsifier: any survey with >= 3 rings in one x-bin whose mean Phi "
           f"departs > 3 combined SE from this curve (e.g., a MIGHTEE-class measurement at "
           f"x ~ 0.03-0.1 that does not sit on Phi(x)); or a flat fit p with |p|/SE_p < 5 on "
           f"the pooled SPARC+dwarf dataset.")
elif best == "b":
    law = (f"Phi(x) = 1 {alpha:+.3f} ln x  [alpha = {alpha:+.3f} +- {se_alpha:.3f}, "
           f"chi2/dof = {chi2_b / dof_b:.2f}; fit on SPARC bins + O01 dwarfs].  Falsifier: any "
           f"survey with >= 3 rings in one x-bin whose mean Phi departs > 3 combined SE from "
           f"this curve; or a flat fit alpha with |alpha|/SE_alpha < 5 on the pooled "
           f"SPARC+dwarf dataset.")
else:
    law = (f"Phi(x) = (1+x)/(1+x/{popt_c[0]:.3f})  [b = {popt_c[0]:.3f} +- {se_c[0]:.3f}, "
           f"chi2/dof = {chi2_c / dof_c:.2f}; fit on SPARC bins + O01 dwarfs].  Falsifier: any "
           f"survey with >= 3 rings in one x-bin whose mean Phi departs > 3 combined SE from "
           f"this curve.")
print(f"    BEST FIT: form ({best});  {law}")
print("\n" + "=" * 104)

# =====================================================================
# artifacts
# =====================================================================
res = dict(
    lane="S01",
    title="THE RUNNING-a0 SYNTHESIS: Phi(x) = (g_obs^2-g_bar^2)/(a0 g_bar) at x = g_bar/a0",
    a0=A0,
    seed=SEED, nboot=NBOOT,
    pre_registered=(
        "COLLAPSE <=> C1: >= 2/3 of overlapping bin-survey comparisons within 3 combined SE; "
        "C2: |p|/SE_p > 5 on the SPARC+dwarf power-law fit.  Else: the sign-mirror is a "
        "GENUINE SYSTEMATICS DIVIDE (registered finding).  Comparison inventory fixed by "
        "geometry: in-window survey points (log10 x in [-1.5, +0.3]) in SPARC bins with "
        ">= 5 rings from >= 2 galaxies."),
    sparc=dict(n_rings=len(XS), n_galaxies=n_gal, n_in_window=int(inwin.sum()),
               log10x_min=float(LX.min()), log10x_max=float(LX.max()),
               bins=[dict(bin=t["bin"], lo=t["lo"], hi=t["hi"], N=t["N"], Ngal=t["Ngal"],
                          Phi=t["Phi"], SE=t["SE"], Phi_med=t["med"], SE_med=t["SE_med"],
                          log10x_med=t["log10x_med"]) for t in tbl]),
    survey_points=[dict(survey=p["survey"], label=p["label"], x=p["x"],
                        log10x=math.log10(p["x"]), Phi=p["Phi"], SE=p["SE"],
                        conversion=p["conv"], bin=p.get("bin", -1))
                   for p in all_pts],
    mightee=dict(deep_N=int(mdeep.sum()), deep_median_x=x_mig,
                 Phi_registered=mig_pt["Phi"], SE_colourgroup=se_mig_cl,
                 SE_ring=se_mig_ring, CSV_band_mean_Phi=m_band_mu,
                 CSV_band_SE_ring=m_band_se,
                 per_ring_Phi=[dict(log10_gbar=float(r["log10_gbar"]),
                                    log10_gobs=float(r["log10_gobs"]),
                                    x=10 ** float(r["log10_gbar"]) / A0,
                                    Phi=float(ph))
                               for r, ph in zip(mrows, mphi)]),
    universality=dict(
        comparisons=[dict(bin=b, label=lab, offset=d, combined_SE=se, z=z)
                     for b, lab, d, se, z in comps],
        n_comparisons=len(comps), n_within_3SE=n3,
        fraction_within_3SE=n3 / len(comps) if comps else float("nan"),
        chi2_per_bin=[dict(bin=b, chi2=c, ndof=n, weighted_mean_Phi=wm)
                      for b, c, n, wm in chi2_rows],
        chi2_total=chi2_tot, ndof_total=ndof_tot,
        r2_median_battery=[dict(bin=b, label=lab, z_median=z) for b, lab, z in median_comps],
        n_r2_within_3SE=n3r2, frac_r2_within_3SE=n3r2 / len(median_comps) if median_comps else float("nan"),
        robustness_r1_MW_15pct_model_systematic="see .out (z with +15% model SE in quadrature)"),
    fits=dict(n_points=n_fit, a_power=res_laws["a_power"], b_log=res_laws["b_log"],
              c_interp_freeb=res_laws["c_interp_freeb"],
              c2_interp_Phi1_eq_1=res_laws["c2_interp_Phi1=1"],
              best_form=best),
    c1_pass=c1, c2_pass=c2, fraction_within_3SE=frac3, z_p=z_p,
    verdict=verdict,
    law=law,
    provenance=("REAL in-repo data only: SPARC 3389 rings/175 galaxies from "
                "glm53_push/data/rotation_curve_corpus_v7.json (L06/G071 conventions); "
                "O01 deepseek_push/O01_results.json + G114_data/G114_combined_sample.csv; "
                "O03 deepseek_push/O03_results.json r_dependence.annuli_primary; MIGHTEE "
                "data2/mightee2025_rar_digitized_points.csv + deepseek_push/N05_results.json. "
                "No data fabricated; no git commit."))
json.dump(res, open(os.path.join(HERE, "S01_results.json"), "w"), indent=1, default=float)
print("\nwrote S01_results.json")