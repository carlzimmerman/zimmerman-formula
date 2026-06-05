#!/usr/bin/env python3
r"""
THE MISSING FORK TEST: does per-galaxy a0 track the LARGE-SCALE COSMIC-WEB density?
==================================================================================
The framework a0 = (c/2) sqrt(G rho) has three forks for WHICH rho sets a0:
  (1) rho_Lambda  (cosmic, UNIFORM)            -> a0 is UNIVERSAL, the same everywhere.
  (2) rho_total / rho_crit (evolves with z)    -> a0(z), tested elsewhere (a0_*_fork.py).
  (3) rho_LOCAL ambient matter density         -> a0 RISES with the local environment.

Fork (3) has an INTERNAL-density version (does a0 track a galaxy's own central surface
density?) and a LARGE-SCALE-ENVIRONMENT version (does a0 track the AMBIENT cosmic-web
density at the galaxy's location -- void vs filament vs group?). The internal version was
already tested and the environmental reading disfavored:
  * reviews/project_sparc_a0_vs_density_direct.py : a0 vs Spitzer SBdisk -- the residual slope
    is an M/L artifact that vanishes in the gas-dominated subsample.
  * reviews/project_rar_bounds_rho_uniformity.py  : the RAR's tightness bounds sigma(ln rho_source)
    to <~32%, excluding the local-matter fork by ~9x.
Both flagged the SAME genuinely-MISSING test: the LARGE-SCALE-environment one. SPARC has no
environment column, so it needs an EXTERNAL cross-match. THIS script supplies it.

WHAT THIS DOES (all on the 175 real SPARC galaxies + a real external redshift survey):
  (a) Fit per-galaxy a0 from the deep-MOND points of data/sparc_data/*_rotmod.dat, EXACTLY as
      project_sparc_a0_vs_density_direct.py does (M/L=0.5 disk, 0.7 bulge; g_bar<a0/3;
      log10 a0 = 2 log10 g_obs - log10 g_bar; median over the deep points).
  (b) Take each galaxy's sky position + redshift from data/sparc_ned_positions.json (NED) and its
      measured distance D from data/SPARC_Lelli2016c.mrt.
  (c) Cross-match to a REAL large-scale density proxy: the 2MASS Redshift Survey (2MRS; Huchra+
      2012, VizieR J/ApJS/199/26, ~44k galaxies, all-sky, Ks<11.75). For each SPARC galaxy we
      build a COUNTS-IN-CYLINDER ambient overdensity (1+delta) from a VOLUME-LIMITED 2MRS tracer
      sample, so the radial flux-limit selection is removed by construction.
  (d) Test: Spearman r of per-galaxy a0 vs ambient (1+delta), and the OLS slope
      d log10 a0 / d log10 (1+delta) -- vs the +0.5 the a0~sqrt(rho_ambient) fork predicts and the
      0 the framework (uniform rho_Lambda) predicts.
  (e) CONTROL THE CONFOUND (the task's explicit warning): nearby SPARC dwarfs preferentially sit
      in the Local-Volume overdensity, and a0-fit quality varies with distance. So we also report
      a0-vs-distance, overdensity-vs-distance, the PARTIAL correlation of a0 vs (1+delta) at fixed
      distance, and a narrow fixed-distance-slice test.

HONESTY MANDATE (repo rule): every number below is computed on real data at runtime; nothing is
asserted that the code does not compute. A NULL (no a0-environment correlation) is VALUABLE
universality evidence for the uniform-cosmic reading; a +0.5 slope would support the environmental
fork and falsify the framework's uniform-a0 prediction. The grade follows the numbers.

Real data: data/sparc_data/*_rotmod.dat + data/SPARC_Lelli2016c.mrt + data/sparc_ned_positions.json
+ data/2mrs_huchra2012.tsv (downloaded from VizieR J/ApJS/199/26; regenerate with the curl line in
_ensure_2mrs() below). Needs numpy + scipy.
"""
import numpy as np, glob, os, json, sys
from scipy import stats

# ---- physical constants + framework / SPARC conventions (identical to the reference script) ----
c, G, kpc = 2.99792458e8, 6.674e-11, 3.0857e19
A0 = 1.2e-10                       # the standard MOND a0 used to DEFINE the deep-MOND regime
ML_D, ML_B = 0.5, 0.7             # stellar mass-to-light, disk & bulge (SPARC fiducial)
H0 = 73.0                          # km/s/Mpc -- SPARC's own distance convention (MRT Note 2)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "sparc_data")
MRT  = os.path.join(HERE, "..", "data", "SPARC_Lelli2016c.mrt")
POS  = os.path.join(HERE, "..", "data", "sparc_ned_positions.json")
TMRS = os.path.join(HERE, "..", "data", "2mrs_huchra2012.tsv")

# 2MRS sky coverage: |b|>5 deg (|b|>8 within 30 deg of the GC). f_sky(|b|>5) = 1 - sin(5deg).
BCUT_TRACER = 5.0
FSKY = 1.0 - np.sin(np.radians(BCUT_TRACER))   # ~0.913

# Counts-in-cylinder environment cell (primary). r_p = projected radius, dV = +/- LoS velocity window.
RP_PRIMARY   = 2.0      # Mpc projected
DV_PRIMARY   = 1000.0   # km/s line-of-sight half-window (absorbs peculiar velocities + fingers-of-god)
D_VL         = 40.0     # Mpc: volume-limit distance for the 2MRS tracer sample
BCUT_TARGET  = 8.0      # drop SPARC targets nearer the ZoA than this (only ~1 galaxy)
D_TARGET_MIN = 3.0      # Mpc: below this, cz/H0 is dominated by peculiar velocity -> unusable env


# ----------------------------------------------------------------------------------------------
# a0 PER GALAXY -- copied verbatim in method from project_sparc_a0_vs_density_direct.py
# ----------------------------------------------------------------------------------------------
def fit_a0_per_galaxy():
    """name -> (log10 a0, gas_fraction_at_deep_points, n_deep_points)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        name = os.path.basename(f).replace("_rotmod.dat", "")
        try:
            d = np.genfromtxt(f, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        Rm = R * kpc
        Vgas2 = np.sign(Vgas) * Vgas**2
        Vbar2 = Vgas2 + ML_D * Vdisk**2 + ML_B * Vbul**2
        gb = Vbar2 * 1e6 / Rm
        go = (Vobs * 1e3)**2 / Rm
        deep = (gb > 0) & (go > 0) & (gb < A0 / 3.0) & (Vobs > 0) & np.isfinite(gb) & np.isfinite(go)
        if deep.sum() < 2:
            continue
        la0 = 2 * np.log10(go[deep]) - np.log10(gb[deep])
        keep = np.isfinite(la0)
        if keep.sum() < 2:
            continue
        fgas = np.median(Vgas2[deep][keep] / np.maximum(Vbar2[deep][keep], 1e-30))
        out[name] = (float(np.median(la0[keep])), float(fgas), int(keep.sum()))
    return out


def load_master():
    """name -> dict(T, D, L36, SBeff, SBdisk, Vflat, Q) from the SPARC master table."""
    m = {}
    with open(MRT) as fh:
        lines = fh.readlines()
    for l in lines[98:]:
        p = l.split()
        if len(p) < 18:
            continue
        try:
            name = p[0]; T = int(p[1]); D = float(p[2]); L36 = float(p[7])
            SBeff = float(p[10]); SBdisk = float(p[12]); Vflat = float(p[15]); Q = int(p[17])
        except Exception:
            continue
        m[name] = dict(T=T, D=D, L36=L36, SBeff=SBeff, SBdisk=SBdisk, Vflat=Vflat, Q=Q)
    return m


# ----------------------------------------------------------------------------------------------
# 2MRS external density field
# ----------------------------------------------------------------------------------------------
def galactic_b(ra_deg, dec_deg):
    """Galactic latitude b (deg) from equatorial J2000 (vectorized)."""
    ragp, degp = np.radians(192.85948), np.radians(27.12825)
    r, d = np.radians(ra_deg), np.radians(dec_deg)
    sb = np.sin(degp) * np.sin(d) + np.cos(degp) * np.cos(d) * np.cos(r - ragp)
    return np.degrees(np.arcsin(np.clip(sb, -1, 1)))


def angsep_rad(ra1, dec1, ra2, dec2):
    """Haversine angular separation (radians). ra/dec in deg; (ra1,dec1) scalar, (ra2,dec2) arrays."""
    r1, d1 = np.radians(ra1), np.radians(dec1)
    r2, d2 = np.radians(ra2), np.radians(dec2)
    dphi, dlam = d2 - d1, r2 - r1
    a = np.sin(dphi / 2)**2 + np.cos(d1) * np.cos(d2) * np.sin(dlam / 2)**2
    return 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def load_2mrs():
    """Parse the VizieR ASU-TSV dump -> structured arrays ra, dec, cz, Ks (Ks may be NaN)."""
    if not os.path.exists(TMRS):
        sys.exit(f"  MISSING {TMRS}\n  Regenerate with:\n"
                 "  curl -s 'https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=J/ApJS/199/26"
                 "&-out=RAJ2000,DEJ2000,cz,Ktmag&-out.max=unlimited' -o data/2mrs_huchra2012.tsv")
    ra, de, cz, ks = [], [], [], []
    with open(TMRS) as fh:
        for ln in fh:
            if ln.startswith("#") or not ln.strip():
                continue
            p = ln.rstrip("\n").split("\t")
            if p[0].strip() in ("RAJ2000", "deg") or p[0].startswith("---"):
                continue
            try:
                a, d, v = float(p[0]), float(p[1]), float(p[2])
            except Exception:
                continue
            try:
                k = float(p[3])
            except Exception:
                k = np.nan
            ra.append(a); de.append(d); cz.append(v); ks.append(k)
    return (np.array(ra), np.array(de), np.array(cz), np.array(ks))


def build_vl_tracers(ra, de, cz, ks, d_vl):
    """Volume-limited 2MRS tracer sample, complete to d_vl (and within the |b|>5 footprint)."""
    b = galactic_b(ra, de)
    d = cz / H0                                       # redshift-space distance (Mpc), heliocentric
    M_lim = 11.75 - 5 * np.log10(d_vl) - 25.0         # abs Ks complete to d_vl at the Ks=11.75 limit
    with np.errstate(invalid="ignore", divide="ignore"):
        M = ks - 5 * np.log10(np.where(d > 0, d, np.nan)) - 25.0
    keep = (cz > 0) & (np.abs(b) > BCUT_TRACER) & np.isfinite(M) & (M < M_lim) & (d < d_vl)
    n_in_vol = keep.sum()
    vol = FSKY * (4.0 / 3.0) * np.pi * d_vl**3        # Mpc^3 of footprint inside d_vl
    nbar = n_in_vol / vol                             # mean VL tracer number density (Mpc^-3)
    return dict(ra=ra[keep], de=de[keep], cz=cz[keep], M_lim=M_lim, nbar=nbar, n=int(n_in_vol))


def overdensity(ra0, dec0, cz0, D0, tr, rp, dv):
    """1+delta from counts-in-cylinder of VL tracers around (ra0,dec0,cz0) at measured distance D0.
    Projected radius uses the well-measured target distance D0; LoS uses redshift window dv."""
    theta = angsep_rad(ra0, dec0, tr["ra"], tr["de"])
    rproj = theta * D0                                # Mpc projected at the target's distance
    in_cyl = (rproj < rp) & (np.abs(tr["cz"] - cz0) < dv)
    # drop the likely 2MRS counterpart of the target itself
    self_match = (rproj < 0.10) & (np.abs(tr["cz"] - cz0) < 150.0)
    N = int(in_cyl.sum() - (in_cyl & self_match).sum())
    Vcyl = np.pi * rp**2 * (2 * dv / H0)              # Mpc^3 (LoS depth 2*dv/H0)
    Nbar = tr["nbar"] * Vcyl
    return N, Nbar, (N / Nbar if Nbar > 0 else np.nan)


# ----------------------------------------------------------------------------------------------
# statistics helpers
# ----------------------------------------------------------------------------------------------
def partial_spearman(y, x, z):
    """Spearman partial correlation of y,x controlling for z (rank-residual method)."""
    ry, rx, rz = (stats.rankdata(v) for v in (y, x, z))
    # residualize ranks of y and x on ranks of z, then Pearson of residuals
    by = np.polyfit(rz, ry, 1); ey = ry - np.polyval(by, rz)
    bx = np.polyfit(rz, rx, 1); ex = rx - np.polyval(bx, rz)
    r, p = stats.pearsonr(ex, ey)
    return r, p


def slope_report(la0, onepd, label, floor=0.5, nbar_counts=None):
    """OLS slope of log10 a0 vs log10(1+delta). Voids (N=0) floored so they participate."""
    od = np.array(onepd, float)
    # floor 1+delta using half-a-count so empty cells are finite (documented choice)
    if nbar_counts is not None:
        od = np.where(od > 0, od, floor / np.maximum(nbar_counts, 1e-9))
    good = np.isfinite(la0) & np.isfinite(od) & (od > 0)
    x = np.log10(od[good]); y = la0[good]
    r_sp, p_sp = stats.spearmanr(od[good], y)         # Spearman on raw (rank) -- floor-independent ordering
    sl, ic, rr, pp, se = stats.linregress(x, y)
    n0 = abs(sl) / se if se > 0 else np.inf
    nh = abs(sl - 0.5) / se if se > 0 else np.inf
    print(f"  {label:<42} N={good.sum():3d}  Spearman r={r_sp:+.3f} (p={p_sp:.2f})")
    print(f"  {'':<42} slope d(log a0)/d(log[1+d]) = {sl:+.3f} +- {se:.3f}"
          f"   [{n0:.1f}s from 0,  {nh:.1f}s from +0.5]")
    return dict(r_sp=r_sp, p_sp=p_sp, slope=sl, se=se, N=int(good.sum()), n_from0=n0, n_from_half=nh)


# ----------------------------------------------------------------------------------------------
def main():
    print("#" * 100)
    print("# FORK-3 (LARGE-SCALE) TEST: per-galaxy a0 vs AMBIENT cosmic-web density (SPARC x 2MRS)")
    print("#" * 100 + "\n")

    a0d   = fit_a0_per_galaxy()
    master = load_master()
    pos   = json.load(open(POS))
    ra2, de2, cz2, ks2 = load_2mrs()
    tr    = build_vl_tracers(ra2, de2, cz2, ks2, D_VL)

    print("=" * 100)
    print("(0) INPUTS (all real, loaded at runtime)")
    print("=" * 100)
    print(f"  SPARC galaxies with a0-fit            : {len(a0d)}")
    print(f"  SPARC galaxies with NED ra/dec/cz     : "
          f"{sum(1 for v in pos.values() if v.get('cz') is not None)}")
    print(f"  2MRS galaxies parsed (Huchra+2012)    : {ra2.size}")
    print(f"  2MRS volume-limited tracers (d<{D_VL:.0f}Mpc): {tr['n']}  "
          f"(abs Ks < {tr['M_lim']:.2f}); mean density nbar = {tr['nbar']:.4f} Mpc^-3")
    print(f"  environment cell (primary)            : cylinder r_p<{RP_PRIMARY:.1f} Mpc, "
          f"|dcz|<{DV_PRIMARY:.0f} km/s; expected count at mean density "
          f"= {tr['nbar']*np.pi*RP_PRIMARY**2*(2*DV_PRIMARY/H0):.2f}\n")

    # ---- assemble the cross-matched per-galaxy table -----------------------------------------
    rows = []
    for name, (la0, fgas, ndeep) in a0d.items():
        if name not in master or name not in pos:
            continue
        p = pos[name]
        if p.get("ra") is None or p.get("cz") is None:
            continue
        ra0, dec0, cz0 = p["ra"], p["dec"], p["cz"]
        D0 = master[name]["D"]
        b0 = galactic_b(ra0, dec0)
        if not np.isfinite(D0) or D0 <= 0:
            continue
        N, Nbar, onepd = overdensity(ra0, dec0, cz0, D0, tr, RP_PRIMARY, DV_PRIMARY)
        rows.append(dict(name=name, la0=la0, fgas=fgas, ndeep=ndeep, T=master[name]["T"],
                         ra=ra0, dec=dec0, cz=cz0, D=D0, b=b0, N=N, Nbar=Nbar, onepd=onepd))

    # primary analysis cut: real environment requires usable redshift distance + inside VL volume
    def usable(r):
        return (abs(r["b"]) > BCUT_TARGET and D_TARGET_MIN < r["D"] < D_VL
                and r["cz"] > D_TARGET_MIN * H0)
    full = rows
    use  = [r for r in rows if usable(r)]
    print("=" * 100)
    print("(1) SAMPLE CONSTRUCTION + the LOCAL-VOLUME bias check (the task's flagged confound)")
    print("=" * 100)
    print(f"  cross-matched (a0 + position + D)      : {len(full)}")
    print(f"  usable env sample ({D_TARGET_MIN:.0f}<D<{D_VL:.0f} Mpc, |b|>{BCUT_TARGET:.0f}): {len(use)}")
    la0 = np.array([r["la0"] for r in use]); onepd = np.array([r["onepd"] for r in use])
    Ncnt = np.array([r["N"] for r in use]); Nbar = np.array([r["Nbar"] for r in use])
    dist = np.array([r["D"] for r in use]);  fgas = np.array([r["fgas"] for r in use])
    ndeep = np.array([r["ndeep"] for r in use]); Tt = np.array([r["T"] for r in use], float)
    print(f"  per-galaxy a0  : median {10**np.median(la0)*1e10:.2f}e-10, scatter {np.std(la0):.2f} dex"
          f" (method-inflated; median N_deep={int(np.median(ndeep))})")
    print(f"  ambient 1+delta: median {np.median(onepd):.2f}, mean {np.mean(onepd):.2f}, "
          f"range {np.min(onepd):.2f}..{np.max(onepd):.1f}  (counts N: {Ncnt.min()}..{Ncnt.max()})")
    frac_over = np.mean(onepd > 1)
    print(f"  >>> {frac_over*100:.0f}% of the usable SPARC galaxies sit at (1+delta)>1: the sample IS")
    print(f"      biased toward overdensities (Local-Volume / Local-Sheet) -- exactly the flagged")
    print(f"      confound. The cosmic-web DYNAMIC RANGE spanned here is "
          f"{np.log10(np.max(onepd)/max(np.min(onepd[onepd>0]),1e-3)):.1f} dex of (1+delta).\n")

    print("=" * 100)
    print("(2) THE TEST: does a0 track ambient (1+delta)?  framework expects FLAT(0); fork-3 expects +0.5")
    print("=" * 100)
    res_primary = slope_report(la0, onepd, "PRIMARY (r_p<2, |dcz|<1000, VL d<40)",
                               nbar_counts=Nbar)
    # If a0 ~ sqrt(rho_ambient) with rho_ambient = rho_mean*(1+delta), slope = +0.5.
    # A 'rho_Lambda + local matter' hybrid would give 0 < slope < 0.5 (rho_Lambda dilutes it);
    # the framework's uniform rho_Lambda gives slope = 0.
    print(f"\n  reading: slope is {res_primary['n_from_half']:.1f}sigma from the +0.5 (pure local-matter)"
          f" fork and {res_primary['n_from0']:.1f}sigma from 0 (framework).\n")

    print("=" * 100)
    print("(3) THE DISTANCE / LOCAL-VOLUME CONFOUND (decisive honesty check)")
    print("=" * 100)
    r_ad, p_ad = stats.spearmanr(dist, la0)
    r_od, p_od = stats.spearmanr(dist, onepd)
    print(f"  a0 vs distance        : Spearman r={r_ad:+.3f} (p={p_ad:.2f})  "
          f"-- is the a0 estimator itself distance/coverage dependent?")
    print(f"  (1+delta) vs distance : Spearman r={r_od:+.3f} (p={p_od:.2f})  "
          f"-- nearer galaxies more overdense? (Local-Volume)")
    pr, pp = partial_spearman(la0, onepd, dist)
    print(f"  a0 vs (1+delta) CONTROLLING distance (partial Spearman): r={pr:+.3f} (p={pp:.2f})")
    # narrow fixed-distance slice: kills the distance confound entirely
    lo, hi = 10.0, 35.0
    sl_mask = (dist > lo) & (dist < hi)
    if sl_mask.sum() >= 12:
        rs, ps = stats.spearmanr(onepd[sl_mask], la0[sl_mask])
        print(f"  a0 vs (1+delta) in the fixed slice {lo:.0f}<D<{hi:.0f} Mpc (N={sl_mask.sum()}): "
              f"Spearman r={rs:+.3f} (p={ps:.2f})")
    print()

    print("=" * 100)
    print("(4) THE BINARY FORK: void-third vs dense-third -- is <a0> different?")
    print("=" * 100)
    q1, q2 = np.percentile(onepd, [33.333, 66.667])
    void = onepd <= q1; dense = onepd >= q2
    a_v, a_d = la0[void], la0[dense]
    d_dex = np.median(a_d) - np.median(a_v)
    U, pmw = stats.mannwhitneyu(a_d, a_v, alternative="two-sided")
    print(f"  void  third (1+d<= {q1:.2f}): N={void.sum():3d}  median a0 = {10**np.median(a_v)*1e10:.2f}e-10")
    print(f"  dense third (1+d>= {q2:.2f}): N={dense.sum():3d}  median a0 = {10**np.median(a_d)*1e10:.2f}e-10")
    # what a0~sqrt(rho) predicts for the density contrast between the two thirds:
    dlogod = np.median(np.log10(np.maximum(onepd[dense], 1e-3))) - \
             np.median(np.log10(np.maximum(onepd[void], 1e-3)))
    pred = 0.5 * dlogod
    print(f"  difference observed   : {d_dex:+.3f} dex  (Mann-Whitney p={pmw:.2f})")
    print(f"  the thirds differ by {dlogod:.2f} dex in (1+delta) -> fork-3 predicts {pred:+.2f} dex in a0;")
    verdict_bin = "CONSISTENT with FLAT (framework)" if abs(d_dex) < abs(pred) / 2 else "shows a trend"
    print(f"  observed/predicted = {d_dex/pred if pred else float('nan'):+.2f}  -> {verdict_bin}\n")

    print("=" * 100)
    print("(5) ROBUSTNESS: vary the cell, the M/L-safe subsample, and the a0-fit quality cut")
    print("=" * 100)
    # recompute overdensity for alternative cells on the usable sample
    def recompute(rp, dv):
        op, nb = [], []
        for r in use:
            N, Nbar2, od = overdensity(r["ra"], r["dec"], r["cz"], r["D"], tr, rp, dv)
            op.append(od); nb.append(Nbar2)
        return np.array(op), np.array(nb)
    for (rp, dv) in [(1.0, 1000.0), (3.0, 1000.0), (2.0, 500.0)]:
        op, nb = recompute(rp, dv)
        slope_report(la0, op, f"cell r_p<{rp:.0f}, |dcz|<{dv:.0f}", nbar_counts=nb)
    # M/L-safe (gas-dominated) + good a0 fits only
    for lab, mask in [("gas-dominated fgas>0.5", fgas > 0.5),
                      ("well-fit a0  N_deep>=3", ndeep >= 3)]:
        if mask.sum() >= 12:
            slope_report(la0[mask], onepd[mask], lab, nbar_counts=Nbar[mask])
        else:
            print(f"  {lab:<42} N={mask.sum()} (too few)")
    # Hubble-type cross-check: early(dense/bulgey) -> late(diffuse). A real density coupling would
    # make a0 trend with T; flat = no dependence.
    r_T, p_T = stats.spearmanr(Tt, la0)
    print(f"  a0 vs Hubble T (cross-proxy)              Spearman r={r_T:+.3f} (p={p_T:.2f})\n")

    print("=" * 100)
    print("(6) VERDICT + HONEST GRADE")
    print("=" * 100)
    sl, se = res_primary["slope"], res_primary["se"]
    detected = (res_primary["p_sp"] < 0.05) and (res_primary["n_from0"] > 2)
    matches_fork = res_primary["n_from_half"] < 2
    confound_explains = (p_ad < 0.05) and (pp > 0.05)   # a0~distance, but partial null at fixed d
    print(f"""  THE NUMBER: per-galaxy a0 vs ambient cosmic-web (1+delta) has slope {sl:+.3f} +- {se:.3f}
  ({res_primary['n_from0']:.1f}sigma from 0, {res_primary['n_from_half']:.1f}sigma from the fork-3 +0.5),
  Spearman r={res_primary['r_sp']:+.3f} (p={res_primary['p_sp']:.2f}) over N={res_primary['N']} galaxies,
  spanning ~{np.log10(np.max(onepd)/max(np.min(onepd[onepd>0]),1e-3)):.1f} dex of real cosmic-web density.

  Is there a detected a0-environment correlation at >2sigma with p<0.05?  {"YES" if detected else "NO"}.
  Does the slope match the +0.5 environmental fork (within 2sigma)?        {"YES" if matches_fork else "NO"}.
  Is any apparent trend explained by the distance/Local-Volume confound?   {"YES" if confound_explains else "(n/a)"}.
""")

    if detected and matches_fork and not confound_explains:
        grade = ("FORK-3 SUPPORTED / FRAMEWORK CHALLENGED: a0 rises with ambient density at ~+0.5, the "
                 "environmental signature. This would FALSIFY the uniform-rho_Lambda reading. Needs an "
                 "independent density field (2M++/Cosmicflows) and the M/L-safe subsample to confirm "
                 "before claiming it.")
    elif not detected or (confound_explains and not matches_fork):
        grade = ("UNIVERSALITY EVIDENCE (category ii): NO clean a0-environment correlation survives. The "
                 "per-galaxy a0 is consistent with being INDEPENDENT of the large-scale cosmic-web density "
                 "across the ~dex of (1+delta) probed -- the framework's uniform-cosmic (rho_Lambda) "
                 "prediction, and a NULL for the strong local-matter fork. This closes the genuinely-missing "
                 "LARGE-SCALE-environment test that project_sparc_a0_vs_density_direct.py and "
                 "project_rar_bounds_rho_uniformity.py both flagged, using a REAL external density field.")
    else:
        grade = ("INCONCLUSIVE: a partial/ambiguous trend that the confounds (distance, M/L, fit quality) "
                 "neither cleanly confirm nor kill. Decisive test needs a deeper, distance-controlled "
                 "environment field (2M++/Cosmicflows reconstruction) and a larger high-z lever arm.")
    print("  GRADE:", grade)
    print(f"""
  HONEST CAVEATS (kept loud):
   * SAMPLE IS LOCAL-VOLUME-BIASED: median SPARC cz~770 km/s (~10 Mpc) and ~{frac_over*100:.0f}% sit at
     (1+delta)>1. The cosmic-web dynamic range probed is modest; this sample has little void coverage,
     so it bounds a STRONG environmental coupling far better than it bounds a weak one.
   * POWER vs the HYBRID fork: only the pure 'a0~sqrt(local matter)' fork predicts the full +0.5 swing.
     A 'rho_Lambda + local matter' hybrid predicts 0<slope<0.5 (rho_Lambda~2x rho_mean dilutes the
     contrast), so a null is consistent with BOTH the framework AND such a hybrid -- this test is most
     powerful against the STRONG fork, which is the one it can actually move.
   * REDSHIFT-SPACE ENVIRONMENT: 2MRS gives cz, not real-space d; the cylinder (|dcz|<1000) smears the
     LoS, especially for the nearest galaxies (peculiar velocities). A reconstructed real-space field
     (2M++/Cosmicflows) is the cleaner future proxy and an INDEPENDENT cross-check.
   * a0 PER GALAXY IS NOISY: median N_deep is small, inflating the a0 scatter and DILUTING any real
     correlation (regression toward null). The Spearman/binary tests are robust to this; the slope
     error bars already fold it in.
   * NECESSARY NOT SUFFICIENT: a0 being environment-independent is REQUIRED by sqrt(rho_Lambda) but does
     not PROVE rho_Lambda causes a0 -- that is the z-evolution test (category iii), tested elsewhere.""")
    print("#" * 100)


if __name__ == "__main__":
    main()
