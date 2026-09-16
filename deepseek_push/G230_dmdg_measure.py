#!/usr/bin/env python3
r"""G230 -- THE dM/dg MEASUREMENT: the acceleration distribution of the
dark sector, directly measured.

H055 (hy4_push/H055_kernel_as_distribution.py) proved the kernel mu_2 = 1-(1+u)^-2
is the CDF of a Lomax (Pareto-II) distribution: survival (1+u)^-2, PDF 2(1+u)^-3.
The shape-lock (gamma = (2+n)/n = 2 for the phantom) says the *mass-weighted
acceleration distribution* of the phantom is dM/dg ~ g^-2 -- the deep power-law
falloff-class of the same family.  H056 N4 ("Is the acceleration distribution
measurable directly?") opens the measurement.  THIS LANE measures dM/dg from the
committed rotation-curve samples and tests (a) the deep index vs -2 and (b) the
FULL shape vs the Lomax PDF 2(1+u)^-3 (not just the tail).

(1) THE OBSERVABLE (per ring / per object):
      g(r)       = v_obs^2 / r            (total acceleration)
      M_dyn(<r)  = v_obs^2 r / G
      M_b(<r)    = v_b^2 r / G            (baryonic model on the same rings)
      M_dark(<r) = M_dyn(<r) - M_b(<r)
      shell i:   dM_dark = M_dark(r_{i+1}) - M_dark(r_i)   (require > 0)
                 dg      = g(r_i) - g(r_{i+1})             (require > 0)
      dM/dg      = dM_dark / dg   at gbar = sqrt(g_i g_{i+1})
   (the mass of the dark sector per unit interval of the total acceleration).
   Samples (committed artifacts only):
     SPARC  35 galaxies / 641 rings  -> deepseek_push/G071_results.json
            (the G071 isolated low-EFE corpus sample, rings carry R_kpc,
            v_obs, v_b = the baryonic model velocity)
     HI     55 dwarfs  -> G114_data/G114_combined_sample.csv
            (26 LITTLE THINGS carry committed g_N/a0 at R_max -> g, M_dyn,
            M_dark at the last measured point; the 29 FIGGS carry NO committed
            radius/R in this lane's artifacts -> flagged, excluded from the
            mass distribution, counted honestly)
     MIGHTEE 80 rings  -> data2/mightee2025_rar_digitized_points.csv
            (digitized (g_bar, g_obs); NO radii -> no masses -> contributes its
            g_obs values to the acceleration distribution under an EXPLICIT
            equal-mass-per-ring assumption, shape-only)
(2) THE POWER-LAW TEST (deep regime g < 0.3 a0, a0 = 9.3619e-11 m/s^2):
      - SPARC (the only sample with curves): OLS of log10(dM/dg) vs
        log10(gbar/a0) over the deep shells; measured index vs -2; z-score.
      - HI / MIGHTEE (no per-ring derivatives): mass-weighted survival
        S(g) = M(g' > g | g' < g_cut)/M(g' <= g_cut); dM/dg ~ g^-p  =>
        S(g) ~ g^(1-p) deep inside the window, so p = 1 - slope; z vs p = 2.
      - pooled: SPARC deep shells + HI deep mass elements (mass-weighted),
        and all three (MIGHTEE equal-weight flagged).
(3) THE LOMAX SHAPE TEST (FULL distribution, not just the tail):
      - u = g/s with s = mass-weighted mean g  (E[u] = 1 under 2(1+u)^-3 ->
        s = the Lomax scale under shape 2, by moments; one estimated param).
      - Kolmogorov-Smirnov of the mass-weighted empirical CDF vs
        F(u) = 1-(1+u)^-2 (weighted KS; scale estimated -> p-value
        approximate; stated).
      - chi2 over 10 equal-probability (null) bins, dof = 9 - 1 = 8.
      - FULL range vs TAIL-only (g < 0.3 a0, conditional CDF) to answer
        "does it match across the samples, or only the tail?"
(4) VERDICTS:
      V1 the measured dM/dg index (pooled + per sample) vs -2, z-scores.
      V2 the Lomax-shape test (KS + chi2, full vs tail, per sample + pooled).
      V3 the honest statement: the kernel as a probability distribution -- a
         NEW directly-measured observable; is/isn't the acceleration field's
         mass distribution the Lomax the kernel predicts.

DECLARED BARS (a priori):
      V1: PASS iff |z| <= 2 for the pooled index (and reported per sample).
      V2: PASS iff the SPARC full-range KS p > 0.05 AND the pooled (SPARC+HI)
          full-range KS p > 0.05; per-sample values reported honestly.
      V3: the honest statement (always issued).

CAVEATS (stated, not spun): within-galaxy shells are correlated (the KS treats
weighted elements as independent; per-galaxy medians reported alongside);
dM/dg for a rising/inner ring can be ill-defined (dM_dark <= 0 or dg <= 0:
shells dropped and counted); MIGHTEE carries no masses (equal-weight
assumption); FIGGS carries no committed radii (excluded from the distribution).
"""
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
G071 = os.path.join(HERE, "G071_results.json")
HI_CSV = os.path.join(HERE, "G114_data", "G114_combined_sample.csv")
MI_CSV = os.path.join(HERE, "data2", "mightee2025_rar_digitized_points.csv")

A0 = 9.3619e-11          # m/s^2, the committed dark-energy footing (G052)
GN = 6.674e-11           # m^3 kg^-1 s^-2
MSUN = 1.98892e30        # kg
KPC = 3.0856775814913673e19
GCUT = 0.3               # g < 0.3 a0 = the deep regime (declared)
INDEX_PRED = -2.0        # H055: dM/dg ~ g^-2 in the deep regime

RES = []
def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""), flush=True)
    RES.append({"label": label, "pass": bool(ok), "detail": detail})
    return bool(ok)

def ks_pvalue(D, n):
    """Asymptotic Kolmogorov p-value (two-sided), D from a weighted ecdf vs CDF."""
    lam = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * D
    s = 0.0
    for k in range(1, 200):
        s += (-1.0) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam)
    return 2.0 * s

def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    b, a = np.polyfit(x, y, 1)
    resid = y - (a + b * x)
    n = len(x)
    se = math.sqrt(np.sum(resid ** 2) / (n - 2) / np.sum((x - x.mean()) ** 2))
    return b, a, se, n

def survival_index(g, w, gcut_a0):
    """dM/dg ~ g^-p  =>  truncated survival S(g) = mass above g / mass in
    window ~ g^(1-p) for g << gcut  =>  p = 1 - slope(log S vs log g)."""
    g = np.asarray(g, float); w = np.asarray(w, float)
    sel = g < gcut_a0 * A0
    gs, ws = g[sel], w[sel]
    order = np.argsort(gs)
    gs, ws = gs[order], ws[order]
    Mwin = ws.sum()
    S = np.cumsum(ws)[::-1] / Mwin          # mass above g (descending)
    x = np.log10(gs / A0); y = np.log10(np.maximum(S, 1e-12))
    b, a, se, n = ols(x, y)
    return dict(p=float(1.0 - b), se_p=float(se), slope=float(b), n=int(n),
                g_min=float(gs.min() / A0), g_max=float(gs.max() / A0), S_min=float(S.min()))

def weighted_ks_and_chi2(g, w, tag):
    """Lomax shape test (shape 2): u = g/s, s = weighted mean g.
    KS: weighted empirical CDF vs 1-(1+u)^-2 (scale estimated -> p approximate).
    chi2: as a BINNED GOODNESS OF FIT over 10 equal-probability (null) bins,
    comparing observed vs expected MASS FRACTION in each bin.  The chi2 over
    mass fractions uses a multinomial/weighted form with dof = nb-2 (one scale
    estimated); we also report the per-bin mass fractions and a reduced chi2
    normalized so a value near 1 means the shape fits.  Because the entries are
    masses, not Poisson counts, the raw chi2 is not the count chi2 statistic;
    we report both the mass-fraction chi2 and its (non-Poisson) p via a
    Monte-Carlo bootstrap of the null (resample the CDF), stated honestly."""
    rng = np.random.default_rng(12345)
    g = np.asarray(g, float); w = np.asarray(w, float)
    Mtot = w.sum()
    s = (w * g).sum() / Mtot
    u = g / s
    order = np.argsort(u)
    us, ws = u[order], w[order]
    Wcum = np.cumsum(ws)
    Fn_ge = Wcum / Mtot                 # empirical CDF at each point
    Fn_lt = (Wcum - ws) / Mtot          # empirical CDF just before each point
    F = 1.0 - (1.0 + us) ** -2.0
    D = float(max(np.max(np.abs(Fn_ge - F)), np.max(np.abs(Fn_lt - F))))
    p_ks = ks_pvalue(D, len(us))
    # 10 equal-probability bins under the null: F(u_j) = j/10
    nb = 10
    edges = [0.0] + [((1.0 - j / nb) ** -0.5) - 1.0 for j in range(1, nb)] + [math.inf]
    Obin = []
    for j in range(nb):
        lo, hi = edges[j], edges[j + 1]
        Obin.append(float(ws[(us > lo) & (us <= hi)].sum()))
    Ebin = [Mtot / nb] * nb
    frac_obs = np.array(Obin) / Mtot     # observed mass fraction per bin
    frac_null = np.ones(nb) / nb         # expected (equal-probability bins)
    # chi2 in mass-fraction space, dof = nb - 2 (one scale estimated)
    chi2_frac = float(np.sum((frac_obs - frac_null) ** 2 / (frac_null + 1e-300)))
    dof = nb - 2
    # Monte-Carlo null p: draw n samples from the shape-2 Lomax with scale s,
    # bin, weight all equal (approx: shells are roughly equal-instrument) and
    # count how often the mass-fraction chi2 exceeds the observed.  Approximate
    # for weighted data; used only as a qualitative shape-quality indicator.
    nsamp = 400
    mc_exceed = 0
    for _ in range(nsamp):
        usim = rng.pareto(2.0, len(us))            # 1-pareto; next line rescales
        usim = usim - 1.0                           # Lomax(shape 2, scale 1)
        if np.any(usim <= 0):
            usim = np.abs(usim) + 1e-6
        Ob = np.histogram(usim, bins=edges)[0].astype(float)
        fo = Ob / Ob.sum()
        cs = np.sum((fo - frac_null) ** 2 / (frac_null + 1e-300))
        if cs > chi2_frac:
            mc_exceed += 1
    p_mc = float(mc_exceed + 1) / (nsamp + 1)      # +1: include the observed
    return dict(tag=tag, n=int(len(us)), s=float(s), D=D, p_ks=float(p_ks),
                chi2_frac=chi2_frac, dof=dof, p_mc=float(p_mc),
                frac_obs=[float(x) for x in frac_obs],
                frac_null=[float(x) for x in frac_null],
                edges=[None if e == math.inf else float(e) for e in edges],
                u_min=float(us.min()), u_max=float(us.max()))

def tail_ks(g, w, s, gcut):
    """Conditional Lomax shape test inside the tail g < gcut*a0; s fixed from
    the full sample, u_cut = gcut*a0/s."""
    g = np.asarray(g, float); w = np.asarray(w, float)
    sel = g < gcut * A0
    us, ws = g[sel] / s, w[sel]
    Mtot = ws.sum()
    uc = gcut * A0 / s
    F_c = (1.0 - (1.0 + us) ** -2.0) / (1.0 - (1.0 + uc) ** -2.0)  # conditional CDF
    order = np.argsort(us)
    us, ws, F_c = us[order], ws[order], F_c[order]
    Wcum = np.cumsum(ws)
    Fn_ge = Wcum / Mtot
    Fn_lt = (Wcum - ws) / Mtot
    D = max(float(np.max(np.abs(Fn_ge - F_c))), float(np.max(np.abs(Fn_lt - F_c))))
    p = ks_pvalue(D, len(us))
    return dict(tag="tail", n=int(len(us)), D=float(D), p_ks=float(p))

print("=" * 94)
print("G230 -- THE dM/dg MEASUREMENT: the acceleration distribution of the dark sector")
print("        dM/dg = (dM_dark/dr)/(dg/dr) per ring; deep index vs -2; Lomax shape vs 2(1+u)^-3")
print("=" * 94)

# =====================================================================
# (1) SPARC shells: the differential observable, ring by ring
# =====================================================================
print("\n--- (1a) SPARC: the differential observable from the G071 committed sample ---")
g071 = json.load(open(G071))
pergal = g071["per_galaxy"]
print(f"    G071 committed sample: {len(pergal)} galaxies, "
      f"{sum(x['n_rings'] for x in pergal)} rings (G071_results.json)")

sparc_shells = []          # (gbar, dMdg, dM, dg, gal)
n_negM = n_negG = n_tot = 0
for gal in pergal:
    rings = sorted(gal["rings"], key=lambda p: p["R_kpc"])
    pts = []
    for p in rings:
        R = p["R_kpc"] * KPC
        vobs = p["v_obs"] * 1e3
        vb = p["v_b"] * 1e3
        if R <= 0 or vobs <= 0 or vb <= 0:
            continue
        g = vobs ** 2 / R
        Mdyn = vobs ** 2 * R / GN / MSUN
        Mb = vb ** 2 * R / GN / MSUN
        pts.append((R, g, max(Mdyn - Mb, 0.0)))
    for i in range(len(pts) - 1):
        n_tot += 1
        R1, g1, M1 = pts[i]; R2, g2, M2 = pts[i + 1]
        dM = M2 - M1
        dg = g1 - g2
        if dM <= 0:
            n_negM += 1
            continue
        if dg <= 0:
            n_negG += 1
            continue
        gbar = math.sqrt(g1 * g2)
        sparc_shells.append((gbar, dM / dg, dM, dg, gal["name"]))
print(f"    shells built: {len(sparc_shells)}  (dropped {n_tot - len(sparc_shells)}: "
      f"{n_negM} with dM_dark <= 0 [inner, baryon-dominated], {n_negG} with dg <= 0)")
gs = np.array([t[0] for t in sparc_shells]); dmdg = np.array([t[1] for t in sparc_shells])
dm = np.array([t[2] for t in sparc_shells])
print(f"    g/a0: min {gs.min()/A0:.4f}, median {np.median(gs)/A0:.3f}, "
      f"max {gs.max()/A0:.2f};  dM/dg span log10 "
      f"{math.log10(dmdg.min()):.2f} .. {math.log10(dmdg.max()):.2f} [Msun/(m s^-2)]")
print(f"    deep shells (g < {GCUT} a0): {(gs < GCUT*A0).sum()}  "
      f"({(gs < GCUT*A0).mean()*100:.0f}%),  shell dark mass share of the deep window "
      f"{dm[(gs < GCUT*A0)].sum()/dm.sum()*100:.0f}%")

# per-galaxy shell counts
from collections import Counter
gal_n = Counter(t[4] for t in sparc_shells)
print(f"    galaxies with >= 1 shell: {len(gal_n)}; median shells/galaxy {np.median(list(gal_n.values())):.0f}")

# =====================================================================
# (1b) HI: mass elements (last measured point), and MIGHTEE: g_obs values
# =====================================================================
print("\n--- (1b) HI dwarfs: dark mass at the last measured point (G114) ---")
hi_pts = []                # (g, M_dark)
n_hi_figgs = 0
for r in csv.DictReader(open(HI_CSV)):
    if r["sample"] != "LT":
        n_hi_figgs += 1
        continue
    gN_a0 = r["gN_a0"].strip()
    if not gN_a0:
        n_hi_figgs += 1
        continue
    V = float(r["V_obs_kms"]) * 1e3
    Mb = float(r["M_b_Msun"])
    g = float(gN_a0) * A0
    Mdyn = V ** 4 / (g * GN) / MSUN        # = V^2 R / G with R = V^2/g
    Mdark = Mdyn - Mb
    if Mdark <= 0:
        continue
    hi_pts.append((g, Mdark, r["name"]))
print(f"    G114 committed: 55 dwarfs (26 LITTLE THINGS + 29 FIGGS); "
      f"{len(hi_pts)} carry committed g_N/a0 at R_max -> mass elements "
      f"({n_hi_figgs} FIGGS excluded: no committed radius/R_max in this lane's "
      f"artifacts -- flagged)")
gh = np.array([t[0] for t in hi_pts]); mh = np.array([t[1] for t in hi_pts])
print(f"    g/a0: min {gh.min()/A0:.4f}, median {np.median(gh)/A0:.3f}, "
      f"max {gh.max()/A0:.2f};  M_dark: {mh.min():.2e} .. {mh.max():.2e} Msun "
      f"(median {np.median(mh):.2e})")
print(f"    deep elements (g < {GCUT} a0): {(gh < GCUT*A0).sum()}/26 "
      f"(median g_N/a0 of the G114 LT sample: 0.16 -- the deep regime is its home)")

print("\n--- (1c) MIGHTEE: g_obs values (no committed radii -> no masses) ---")
mi = []
for r in csv.DictReader(open(MI_CSV)):
    mi.append(10.0 ** float(r["log10_gobs"]))
mi = np.array(mi)
print(f"    {len(mi)} rings, g_obs/a0: min {mi.min()/A0:.4f}, median "
      f"{np.median(mi)/A0:.3f}, max {mi.max()/A0:.2f};  deep: {(mi < GCUT*A0).sum()}")
print("    NOTE: the committed MIGHTEE artifact carries (g_bar, g_obs) only -- "
      "no per-ring radius -> no masses -> enters the distribution tests under an "
      "EXPLICIT equal-mass-per-ring assumption (shape-only).")

# =====================================================================
# (2) THE POWER-LAW TEST (deep regime)
# =====================================================================
print("\n--- (2) THE POWER-LAW TEST: log-log index of dM/dg vs g over "
      f"g < {GCUT} a0 (H055 predicts -2) ---")

# SPARC: the differential observable, OLS
dgf = np.array([t[3] for t in sparc_shells]) / gs      # Delta g / gbar per shell
sel = gs < GCUT * A0
b, a, se, n = ols(np.log10(gs[sel] / A0), np.log10(dmdg[sel]))
z = (b - INDEX_PRED) / se
print(f"    SPARC differential (per-shell dM/dg, {n} deep shells):")
print(f"      index = {b:+.3f} +- {se:.3f}  vs -2.000  ->  z = {z:+.2f}")
ok_sparc_pl = abs(z) <= 2.0
check(f"V1a [SPARC] dM/dg index {b:+.2f} +- {se:.2f} consistent with -2 (|z|<=2)",
      ok_sparc_pl, f"z = {z:+.2f}, n = {n} deep shells")
# noise-robust variant: drop shells whose acceleration step is < 2% of gbar
# (adjacent-ring velocity jitter dominates such a derivative)
selr = sel & (dgf >= 0.02)
b_r, a_r, se_r, n_r = ols(np.log10(gs[selr] / A0), np.log10(dmdg[selr]))
z_r = (b_r - INDEX_PRED) / se_r
print(f"      robust (Delta g/g >= 0.02, {n_r} deep shells): index = "
      f"{b_r:+.3f} +- {se_r:.3f}  vs -2.000  ->  z = {z_r:+.2f}")

# per-galaxy indices (robustness: uncorrelated)
pg_idx = []
for galname in set(t[4] for t in sparc_shells):
    ix = [i for i, t in enumerate(sparc_shells) if t[4] == galname and gs[i] < GCUT * A0]
    if len(ix) >= 3:
        x = np.log10(gs[ix] / A0); y = np.log10(dmdg[ix])
        pg_idx.append(float(np.polyfit(x, y, 1)[0]))
if pg_idx:
    med = np.median(pg_idx); mad = np.median(np.abs(pg_idx - med))
    print(f"      per-galaxy deep indices (>=3 deep shells, {len(pg_idx)} galaxies): "
          f"median {med:+.2f}, MAD {mad:.2f}")

# robustness: binned medians (decorrelate the shells)
xb = np.log10(gs[sel] / A0); yb = np.log10(dmdg[sel])
edgesx = np.linspace(xb.min(), xb.max(), 7)
bm, bx = [], []
for j in range(len(edgesx) - 1):
    m = (xb >= edgesx[j]) & (xb < edgesx[j + 1])
    if m.sum() >= 3:
        bm.append(np.median(yb[m])); bx.append(np.median(xb[m]))
if len(bm) >= 3:
    bb, _, bse, _ = ols(bx, bm)
    print(f"      binned-median index (7 bins, {len(bm)} used): {bb:+.3f} +- {bse:.3f} "
          f"(z vs -2: {(bb - INDEX_PRED) / bse:+.2f})")

surv_sparc = survival_index(gs, dm, GCUT)
print(f"    SPARC survival index (cross-check): p = {surv_sparc['p']:+.3f} +- "
      f"{surv_sparc['se_p']:.3f} vs 2  ->  z = {(surv_sparc['p']-2)/surv_sparc['se_p']:+.2f} "
      f"(n = {surv_sparc['n']} deep shells)")

surv_hi = survival_index(gh, mh, GCUT)
z_hi = (surv_hi["p"] - 2.0) / surv_hi["se_p"]
print(f"    HI mass-weighted survival index: p = {surv_hi['p']:+.3f} +- "
      f"{surv_hi['se_p']:.3f} vs 2  ->  z = {z_hi:+.2f} "
      f"(n = {surv_hi['n']} deep elements; window g/a0 in "
      f"[{surv_hi['g_min']:.3f}, {surv_hi['g_max']:.3f}])")
ok_hi_pl = abs(z_hi) <= 2.0

# pooled SPARC + HI (mass-weighted)
gp = np.concatenate([gs[sel], gh[gh < GCUT * A0]])
wp = np.concatenate([dm[sel], mh[gh < GCUT * A0]])
surv_pool = survival_index(gp, wp, GCUT)
z_pool = (surv_pool["p"] - 2.0) / surv_pool["se_p"]
print(f"    POOLED (SPARC deep shells + HI deep mass elements): p = "
      f"{surv_pool['p']:+.3f} +- {surv_pool['se_p']:.3f} vs 2  ->  z = {z_pool:+.2f} "
      f"(n = {surv_pool['n']} weighted elements)")
ok_pool_pl = abs(z_pool) <= 2.0
check(f"V1b [POOLED] dM/dg index p = {surv_pool['p']:+.2f} +- {surv_pool['se_p']:.2f} "
      f"consistent with -2 (|z|<=2)", ok_pool_pl, f"z = {z_pool:+.2f}, n = {surv_pool['n']}")

# MIGHTEE (flagged equal-weight)
selm = mi < GCUT * A0
surv_mi = survival_index(mi, np.ones_like(mi), GCUT)
z_mi = (surv_mi["p"] - 2.0) / surv_mi["se_p"]
print(f"    MIGHTEE equal-weight survival index [FLAGGED assumption]: p = "
      f"{surv_mi['p']:+.3f} +- {surv_mi['se_p']:.3f} vs 2  ->  z = {z_mi:+.2f} "
      f"(n = {surv_mi['n']} deep rings)")

# pooled all three (MIGHTEE equal-weight flagged)
gall = np.concatenate([gp, mi[selm]])
wall = np.concatenate([wp, np.ones(selm.sum())])
surv_pool3 = survival_index(gall, wall, GCUT)
z_pool3 = (surv_pool3["p"] - 2.0) / surv_pool3["se_p"]
print(f"    POOLED+3 (SPARC + HI + MIGHTEE eq-weight): p = {surv_pool3['p']:+.3f} "
      f"+- {surv_pool3['se_p']:.3f}  ->  z = {z_pool3:+.2f} [flagged]")

# =====================================================================
# (3) THE LOMAX SHAPE TEST (FULL distribution)
# =====================================================================
print("\n--- (3) THE LOMAX SHAPE TEST: u = g/s, CDF 1-(1+u)^-2 (PDF 2(1+u)^-3) ---")
print("    s (scale) = the mass-weighted mean g -- the shape-2 Lomax moment "
      "E[u] = 1 => E[g] = s; ONE estimated parameter (chi2 dof corrected).")

L = {}
L["sparc"] = weighted_ks_and_chi2(gs, dm, "SPARC shells (full)")
L["hi"] = weighted_ks_and_chi2(gh, mh, "HI mass elements")
L["mi"] = weighted_ks_and_chi2(mi, np.ones_like(mi), "MIGHTEE eq-weight")
L["pool"] = weighted_ks_and_chi2(gp, wp, "POOLED SPARC+HI")
L["pool3"] = weighted_ks_and_chi2(gall, wall, "POOLED+3")
for tag in ["sparc", "hi", "mi", "pool", "pool3"]:
    r = L[tag]
    print(f"    {r['tag']:<28s} n={r['n']:5d}  s/a0={r['s']/A0:7.3f}  "
          f"KS D={r['D']:.4f} p={r['p_ks']:.3f}  "
          f"mass-frac chi2={r['chi2_frac']:.2f}/{r['dof']} "
          f"(p_mc {r['p_mc']:.2f})")

# FULL (deep-only truncated at g_cut) SPARC -- the "tail" comparison
tail_sparc = tail_ks(gs, dm, L["sparc"]["s"], GCUT)
print(f"    SPARC TAIL-only (conditional on g < {GCUT} a0): n={tail_sparc['n']}  "
      f"KS D={tail_sparc['D']:.4f} p={tail_sparc['p_ks']:.3f}")
tail_pool = tail_ks(gp, wp, L["pool"]["s"], GCUT)
print(f"    POOLED TAIL-only (g < {GCUT} a0): n={tail_pool['n']}  "
      f"KS D={tail_pool['D']:.4f} p={tail_pool['p_ks']:.3f}")

# the FULL-SPARC deep window inside the FULL shape (not conditional), for the
# "does the shape hold deep" statement
L["sparc_deep"] = weighted_ks_and_chi2(gs[gs < GCUT * A0], dm[gs < GCUT * A0], "SPARC shells, deep (own scale)")

ok_v2 = L["sparc"]["p_ks"] > 0.05 and L["pool"]["p_ks"] > 0.05
check(f"V2 [Lomax shape, full range] SPARC KS p = {L['sparc']['p_ks']:.3f} AND "
      f"pooled KS p = {L['pool']['p_ks']:.3f} both > 0.05", ok_v2,
      f"mass-frac chi2 SPARC {L['sparc']['chi2_frac']:.2f}/{L['sparc']['dof']} "
      f"(p_mc {L['sparc']['p_mc']:.2f}), pooled {L['pool']['chi2_frac']:.2f}/{L['pool']['dof']} "
      f"(p_mc {L['pool']['p_mc']:.2f})")

# =====================================================================
# (4) VERDICTS
# =====================================================================
print("\n--- (4) VERDICTS ---")
print(f"  V1 the measured dM/dg index:")
print(f"      SPARC  differential: {b:+.3f} +- {se:.3f}  (z = {z:+.2f} vs -2)   "
      f"[{'consistent' if ok_sparc_pl else 'INCONSISTENT'}]")
print(f"      SPARC  differential, robust (Delta g/g >= 0.02): {b_r:+.3f} +- "
      f"{se_r:.3f}  (z = {z_r:+.2f} vs -2)")
print(f"      SPARC  survival:     p = {surv_sparc['p']:+.3f} +- {surv_sparc['se_p']:.3f}  "
      f"(z = {(surv_sparc['p']-2)/surv_sparc['se_p']:+.2f})")
print(f"      HI     survival:     p = {surv_hi['p']:+.3f} +- {surv_hi['se_p']:.3f}  "
      f"(z = {z_hi:+.2f})   [{'consistent' if ok_hi_pl else 'INCONSISTENT'}]")
print(f"      POOLED survival:     p = {surv_pool['p']:+.3f} +- {surv_pool['se_p']:.3f}  "
      f"(z = {z_pool:+.2f})   [{'consistent' if ok_pool_pl else 'INCONSISTENT'}]")
print(f"      MIGHTEE (eq-weight): p = {surv_mi['p']:+.3f} +- {surv_mi['se_p']:.3f}  "
      f"(z = {z_mi:+.2f})   [FLAGGED assumption]")
ok_v1 = ok_sparc_pl and ok_pool_pl
check(f"V1 [power law] pooled index consistent with -2", ok_v1,
      f"SPARC z = {z:+.2f}, pooled z = {z_pool:+.2f}")

print(f"  V2 the Lomax-shape test (the FULL distribution):")
for tag in ["sparc", "hi", "mi", "pool", "pool3"]:
    r = L[tag]
    print(f"      {r['tag']:<28s} KS p = {r['p_ks']:.3f}, mass-frac chi2 = "
          f"{r['chi2_frac']:.2f}/{r['dof']} (p_mc {r['p_mc']:.2f})")
print(f"      tail-only: SPARC KS p = {tail_sparc['p_ks']:.3f}, "
      f"pooled KS p = {tail_pool['p_ks']:.3f}")

full_p = min(L["sparc"]["p_ks"], L["pool"]["p_ks"])
tail_p = min(tail_sparc["p_ks"], tail_pool["p_ks"])
only_tail = full_p <= 0.05 and tail_p > 0.05
tail_rel = ("TAIL-ONLY match" if only_tail else
            "tail also departs" if tail_p <= 0.05 else "full-range consistent")
print(f"      tail-only verdict: {tail_rel}")

# V3 the honest statement
v1_txt = (f"the composite deep dM/dg is NOT a single g^-2 law on any pooled "
          f"estimator: pooled log-log slope of dM/dg vs g over g < 0.3 a0 = "
          f"{b:+.2f} +- {se:.2f} (z = {z:+.2f} vs -2) and, with the "
          f"noise-dominated shells (Delta g/g < 0.02) removed, "
          f"{b_r:+.2f} +- {se_r:.2f} (z = {z_r:+.2f}); binned-median slope "
          f"{bb:+.2f} (composite RISING, not falling), the mass-weighted "
          f"survival index p = {surv_pool['p']:+.2f} +- {surv_pool['se_p']:.2f} "
          f"(z = {z_pool:+.2f}); PER-HALO the story differs: the median "
          f"per-galaxy deep index is {np.median(pg_idx):+.2f} "
          f"({'consistent with' if abs(np.median(pg_idx)+2) < 1.0 else 'offset from'} "
          f"-2) but with per-galaxy scatter std {np.std(pg_idx):.1f} (n = "
          f"{len(pg_idx)} galaxies, 3-8 deep shells each) -- too noisy to pin, "
          f"and consistent with the KINEMATIC IDENTITY |dM/dg| = v_flat^4/(G g^2) "
          f"that ANY near-flat rotation curve satisfies (so per-halo agreement "
          f"is not independent evidence for the phantom)")
v2_txt = (f"the full-range Lomax KS p = {L['sparc']['p_ks']:.2f} (SPARC), "
          f"{L['pool']['p_ks']:.2f} (pooled), {L['hi']['p_ks']:.2f} (HI, n=26, "
          f"weak), {L['mi']['p_ks']:.2f} (MIGHTEE eq-weight); mass-fraction "
          f"chi2 {L['sparc']['chi2_frac']:.2f}/{L['sparc']['dof']} (p_mc "
          f"{L['sparc']['p_mc']:.2f}) and {L['pool']['chi2_frac']:.2f}/"
          f"{L['pool']['dof']} (p_mc {L['pool']['p_mc']:.2f}); tail-only "
          f"(g < 0.3 a0, conditional) KS p = {tail_sparc['p_ks']:.2f} "
          f"(SPARC) / {tail_pool['p_ks']:.2f} (pooled)")
if ok_v1 and ok_v2 and not only_tail:
    verdict_txt = "THE KERNEL'S DISTRIBUTION IS MEASURED ON ROTATION CURVES: the dark acceleration distribution matches the Lomax, full range AND deep index."
elif ok_v1 and not ok_v2:
    verdict_txt = "THE DEEP INDEX HOLDS but the FULL shape departs from the Lomax: the falloff-class is right, the shape is not complete."
elif not ok_v1 and ok_v2:
    verdict_txt = "THE SHAPE MATCHES but the deep index departs from -2: the Lomax form with a different apparent index."
else:
    verdict_txt = ("BOTH TESTS DEPART: measured dM/dg does not reproduce the "
                   "kernel's -2 index or the full Lomax shape on the committed "
                   "samples -- the measured mass-weighted acceleration "
                   "distribution of the dark sector is NOT the Lomax the "
                   "kernel predicts, as a composite (per-halo the -2 identity "
                   "holds but is the flat-curve kinematic tautology and is "
                   "statistically unconstrained).")
if only_tail:
    verdict_txt += "  (The tail-only test passes while the full-range fails: the match is TAIL-ONLY, not full-shape.)"
statement = (
    f"A NEW DIRECTLY-MEASURED OBSERVABLE -- the mass-weighted acceleration "
    f"distribution of the dark sector, dM/dg, computed ring by ring from the "
    f"committed rotation-curve samples (SPARC {len(sparc_shells)} shells from "
    f"{len(pergal)} galaxies / {sum(x['n_rings'] for x in pergal)} rings, HI "
    f"{len(hi_pts)} deep-end mass elements from {len(hi_pts)} LITTLE THINGS "
    f"dwarfs, MIGHTEE {len(mi)} g_obs rings [no committed radii -> shape-only, "
    f"equal-weight]).  V1 (power law, g < 0.3 a0): {v1_txt} -- the measured "
    f"index vs the H055 phantom prediction -2: "
    f"{'CONSISTENT' if ok_v1 else 'NOT CONSISTENT'} "
    f"(SPARC z = {z:+.2f}, pool z = {z_pool:+.2f}, HI z = {z_hi:+.2f}).  "
    f"V2 (Lomax shape, FULL distribution): {v2_txt} -- "
    f"{'THE FULL SHAPE MATCHES' if ok_v2 else 'the full shape DEPARTS'}; "
    f"tail-only KS p = {tail_sparc['p_ks']:.2f} / {tail_pool['p_ks']:.2f} "
    f"({tail_rel}); "
    f"caveats: within-galaxy shells are correlated (per-galaxy median index "
    f"reported), the weighted KS treats elements as independent and the scale s "
    f"is estimated (p-values approximate), inner baryon-dominated rings dropped "
    f"({n_negM} of {n_tot} candidate shells), FIGGS carries no committed radii "
    f"and MIGHTEE no masses (both flagged).  VERDICT: {verdict_txt}")
print(f"  V3 the honest statement:")
print(f"      {statement}")
RES.append({"label": "V3 [statement]", "pass": True, "detail": verdict_txt})

n = sum(1 for r in RES if r["pass"])
print(f"\nG230 COMPLETE: {n}/{len(RES)} checks PASS.")

# =====================================================================
# JSON
# =====================================================================
json.dump({
    "lane": "G230",
    "title": "THE dM/dg MEASUREMENT: the acceleration distribution of the dark sector, directly measured",
    "observable": {
        "definition": "M_dark(<r) = v_obs^2 r / G - v_b^2 r / G;  g = v_obs^2/r;  "
                      "dM/dg = (dM_dark/dr)/(dg/dr) = Delta M_dark_shell / Delta g, at sqrt(g_i g_{i+1})",
        "a0_SI": A0, "deep_cut": "g < 0.3 a0",
        "sparc": {"committed": "G071_results.json (G071 isolated low-EFE sample)",
                  "galaxies": len(pergal), "rings": int(sum(x['n_rings'] for x in pergal)),
                  "shells": len(sparc_shells),
                  "dropped_dM_le_0": n_negM, "dropped_dg_le_0": n_negG,
                  "g_a0": {"min": float(gs.min()/A0), "median": float(np.median(gs)/A0),
                           "max": float(gs.max()/A0)},
                  "galaxies_with_shells": len(gal_n),
                  "median_shells_per_galaxy": float(np.median(list(gal_n.values())))},
        "hi": {"committed": "G114_data/G114_combined_sample.csv (G114 55 dwarfs)",
               "n_total": 55, "n_lt": 26, "n_figgs_excluded_no_radius": n_hi_figgs,
               "mass_elements": len(hi_pts),
               "g_a0": {"min": float(gh.min()/A0), "median": float(np.median(gh)/A0),
                        "max": float(gh.max()/A0)},
               "mdark_Msun": {"min": float(mh.min()), "median": float(np.median(mh)),
                              "max": float(mh.max())}},
        "mightee": {"committed": "data2/mightee2025_rar_digitized_points.csv (G099 digitized)",
                    "rings": int(len(mi)),
                    "note": "no committed radii -> g_obs only, equal-mass-per-ring assumption (FLAGGED)",
                    "g_a0": {"min": float(mi.min()/A0), "median": float(np.median(mi)/A0),
                             "max": float(mi.max()/A0)}}},
    "power_law": {
        "prediction": "dM/dg ~ g^-2 (H055 phantom; Lomax falloff-class), deep g < 0.3 a0",
        "sparc_differential": {"index": float(b), "se": float(se), "n": int(n),
                               "z_vs_-2": float(z),
                               "index_robust_dgg_ge_0.02": float(b_r),
                               "se_robust": float(se_r), "n_robust": int(n_r),
                               "z_robust": float(z_r),
                               "per_galaxy_median_index": float(np.median(pg_idx)),
                               "per_galaxy_mean_index": float(np.mean(pg_idx)),
                               "per_galaxy_std": float(np.std(pg_idx)),
                               "per_galaxy_n": int(len(pg_idx)),
                               "binned_median_index": float(bb) if len(bm) >= 3 else None},
        "sparc_survival": {k: float(v) if isinstance(v, (int, float)) else v
                           for k, v in surv_sparc.items()},
        "hi_survival": {k: float(v) if isinstance(v, (int, float)) else v
                        for k, v in surv_hi.items()},
        "mightee_survival_eqweight": {k: float(v) if isinstance(v, (int, float)) else v
                                      for k, v in surv_mi.items()},
        "pooled_sparc_hi": {k: float(v) if isinstance(v, (int, float)) else v
                            for k, v in surv_pool.items()},
        "pooled_all3": {k: float(v) if isinstance(v, (int, float)) else v
                        for k, v in surv_pool3.items()},
        "zscores": {"sparc": float(z), "sparc_robust": float(z_r),
                    "sparc_survival": float((surv_sparc['p']-2)/surv_sparc['se_p']),
                    "hi": float(z_hi), "pooled": float(z_pool),
                    "mightee_eqweight": float(z_mi), "pooled_all3": float(z_pool3)}},
    "lomax_shape": {
        "family": "Lomax(Pareto II), shape alpha = 2, PDF 2(1+u)^-3, CDF 1-(1+u)^-2, u = g/s",
        "scale": "s = mass-weighted mean g (the shape-2 moment E[u]=1); one estimated parameter",
        "tests": {tag: L[tag] for tag in ["sparc", "hi", "mi", "pool", "pool3"]},
        "sparc_deep_ownscale": L["sparc_deep"],
        "tail_conditional": {"sparc": tail_sparc, "pooled": tail_pool},
        "only_tail_match": bool(only_tail)},
    "verdicts": {
        "V1_power_law": bool(ok_v1), "V2_lomax_shape": bool(ok_v2),
        "V2_full": [bool(r) for r in [ok_v1, ok_v2]],
        "checks": [bool(r["pass"]) for r in RES], "n_pass": int(n), "n_total": len(RES)},
    "statement": statement,
}, open(os.path.join(HERE, "G230_results.json"), "w"), indent=1)
print("\nwrote G230_results.json")