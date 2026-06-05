#!/usr/bin/env python3
r"""
BIG-SPARC PROJECTION: the environmental a0-fork test, generalized and ready for the ~4000-galaxy release.
========================================================================================================
C. Zimmerman, June 2026.

CONTEXT (read first -- this script fabricates nothing).
  The fork for a0 = (c/2) sqrt(G rho) = cH/Z is WHICH rho: cosmic rho_Lambda (UNIVERSAL, a0 the same
  in every environment) or LOCAL ambient density (a0 ~ sqrt(rho_local), slope d log a0 / d log rho = +1/2).
  On the public 175-galaxy SPARC the local-rho fork is ALREADY dead many times over (see "CURRENT STATE"
  below). The 2024 BIG-SPARC paper (Haubner, Lelli et al., arXiv:2411.13329) describes a ~4000-galaxy
  successor -- a >20x sample that would (i) turn the underpowered cluster/field a0 contrast (N=28 in
  SPARC) into a properly-powered test, and (ii) reach the SUBTLE residual-trend regime (0.02-0.05 dex)
  that 175 galaxies cannot. As of 2026-06-05 BIG-SPARC is NOT publicly released (status/methods paper
  only; no VizieR/Zenodo/DR1 -- see reviews/BIG_SPARC_AVAILABILITY_2026-06.md).

WHAT THIS SCRIPT DOES, depending on whether BIG-SPARC data is on disk:
  * DATA ABSENT (today): it does NOT invent BIG-SPARC galaxies. It computes -- from the REAL public 175
    sample -- the POWER FORECAST: exactly how far a BIG-SPARC-sized N pushes the slope SE, the minimum
    detectable residual environmental trend, and the cluster/field offset sensitivity. Then it prints
    the drop-in instructions and exits. The forecast is real, reproducible, and is the honest deliverable.
  * DATA PRESENT (on release): it runs the GENERALIZED pipeline -- the same deep-MOND per-galaxy a0 fit,
    cross-matched to a REAL group/cluster catalog (Tempel+2017 SDSS DR12 groups; 2M++ Lavaux&Hudson 2011)
    to assign each galaxy a physical local-density / environment value, then reports the slope
    d log a0 / d log(rho_env) and the cluster-vs-field offset WITH the same artifact controls
    (gas-dominated / M/L-free subset, quality cut, M/L variation) and the same honesty discipline.

HONESTY (mandated, same discipline as a0_environmental_fork_test.py):
  - distinguish value-coincidence (a0 ~ (c/2)sqrt(G rho_Lambda) to ~20%) vs UNIVERSALITY EVIDENCE
    (a0 is the same across environments -> cosmic source) vs CAUSAL PROOF (a0 tracks rho as rho CHANGES;
    needs z~3 evolution, telescope-limited -- NOT reachable even with BIG-SPARC at z~0).
  - a NULL is a valid, reported result. BIG-SPARC does not "rescue" the already-decisive null; it tests
    a DIFFERENT, finer question (subtle residual environmental dependence + a real cluster contrast).
  - NO CIRCULARITY: a0 is fit from each galaxy's own deep-MOND points; the density axis comes from an
    EXTERNAL catalog (group multiplicity / 2M++ / kNN of independent positions), never from a0.

Run:  python3 real_research/predictions/project_bigsparc_a0_environment.py
      (no network, no BIG-SPARC needed -- prints the forecast from the public 175 sample)
      BIGSPARC_DIR=/path/to/bigsparc python3 .../project_bigsparc_a0_environment.py   (when released)
Needs numpy + scipy; the live pipeline additionally needs a downloaded group catalog (see GROUP_CATALOG).
"""
import os, sys, glob, json, math
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from a0_environmental_fork_test import (                       # reuse the audited 175-sample machinery
    load_master, build, fit_a0, A0_RAR, DATA as SPARC_DATA)

NED_CACHE = os.path.join(HERE, "..", "data", "sparc_ned_positions.json")

# ----- where BIG-SPARC will live once released (override via env vars) --------------------------------
BIGSPARC_DIR = os.environ.get("BIGSPARC_DIR", os.path.join(HERE, "..", "data", "bigsparc"))
GROUP_CATALOG = os.environ.get("GROUP_CATALOG", "")            # path to Tempel+2017 / 2M++ table; see docs

# BIG-SPARC availability, checked 2026-06-05 (arXiv:2411.13329; VizieR/Zenodo/AstroWeb all negative).
BIGSPARC = dict(arxiv="2411.13329", checked="2026-06-05", public=False,
                target_N=4000, note="status/methods paper; no public DR as of check date")


# =====================================================================================================
#  POWER FORECAST  -- computed from the REAL public 175 sample, no BIG-SPARC data required
# =====================================================================================================
def _continuous_slope_anchor(recs):
    """Recompute the continuous local-density slope SE from cached NED positions (offline) if available.
    Returns (SE_slope, N) or None. This is the tightest current a0-vs-density lever on SPARC."""
    if not os.path.exists(NED_CACHE):
        return None
    pos = json.load(open(NED_CACHE))
    by_name = {r["name"]: r for r in recs if r["la"] is not None}
    pts, a0s = [], []
    for name, r in by_name.items():
        p = pos.get(name) or {}
        ra, dec = p.get("ra"), p.get("dec")
        D = r.get("D", 0.0)
        if ra is None or dec is None or not D or D <= 0:
            continue
        rr, dr = math.radians(ra), math.radians(dec)
        pts.append((D * math.cos(dr) * math.cos(rr), D * math.cos(dr) * math.sin(rr), D * math.sin(dr)))
        a0s.append(r["la"])
    if len(pts) < 30:
        return None
    pts, a0s = np.array(pts), np.array(a0s)
    from scipy.spatial import cKDTree
    k = 5
    dist, _ = cKDTree(pts).query(pts, k=k + 1)
    rho = k / (4.0 / 3.0 * math.pi * dist[:, k] ** 3)
    res = stats.linregress(np.log10(rho), a0s)
    return res.stderr, len(pts)


def _cluster_offset_anchor(recs):
    """Bootstrap SE of the UMa-cluster (fD=4) minus field median-log-a0 offset, from the public sample."""
    uma = np.array([r["la"] for r in recs if r["fD"] == 4 and r["la"] is not None])
    fld = np.array([r["la"] for r in recs if r["fD"] != 4 and r["la"] is not None])
    if uma.size < 5 or fld.size < 5:
        return None
    rng = np.random.default_rng(0)
    b = np.array([np.median(rng.choice(uma, uma.size)) - np.median(rng.choice(fld, fld.size))
                  for _ in range(20000)])
    return float(b.std()), uma.size, fld.size


def forecast(recs):
    print("=" * 100)
    print("POWER FORECAST  --  what a BIG-SPARC-sized N buys, scaled from the REAL public 175 sample")
    print("=" * 100)

    # --- anchor 1: continuous local-density slope (the tightest current lever) ----------------------
    cont = _continuous_slope_anchor(recs)
    if cont is not None:
        se0, n0 = cont
        src = f"continuous NED kNN-density slope, N={n0}"
    else:
        se0, n0 = 0.036, 91                         # fallback: SBeff Q=1 slope SE (no network needed)
        src = f"SBeff (internal-density) slope, Q=1, N={n0} [NED cache absent -> fallback anchor]"
    print(f"\n  ANCHOR (measured on public SPARC): SE(slope d log a0/d log rho) = {se0:.3f}  [{src}]")
    print("  Forecast scaling: SE(slope) ~ SE0 * sqrt(N0/N)   (a0 scatter & density range held fixed;")
    print("  CONSERVATIVE -- BIG-SPARC's wider volume widens the density lever, shrinking SE further).\n")
    print(f"  {'BIG-SPARC N (good RCs)':>24}{'SE(slope)':>12}{'min |slope| det. @3sig':>26}{'+0.5 fork excluded at':>24}")
    print("  " + "-" * 86)
    for N in (500, 1000, 2000, 4000):
        se = se0 * math.sqrt(n0 / N)
        print(f"  {N:>24}{se:>12.4f}{3 * se:>26.3f}{0.5 / se:>21.0f}sig")
    print(f"""
  READING: the +0.5 dex local-rho fork is ALREADY excluded at ~13sig (internal density) to ~35sig
  (continuous NED density) on the 175 sample -- BIG-SPARC does not "rescue" a live question, it makes
  the exclusion overwhelming AND, more usefully, drops the minimum DETECTABLE residual trend from
  ~0.05 dex (today) to ~0.01 dex: i.e. BIG-SPARC could detect or rule out a SUBTLE environmental
  dependence (a weak EFE-like signature, a residual systematic) that 175 galaxies are blind to.""")

    # --- anchor 2: cluster-vs-field offset (the genuinely underpowered piece in SPARC) --------------
    off = _cluster_offset_anchor(recs)
    if off is not None:
        seoff, ncl, nfl = off
        print("\n  " + "-" * 96)
        print(f"  CLUSTER/FIELD OFFSET -- the underpowered test BIG-SPARC most improves.")
        print(f"  ANCHOR (Ursa Major, fD=4): SE(cluster-field median log a0) = {seoff:.3f} dex at "
              f"N_cluster={ncl}, N_field={nfl}.")
        print(f"  A real group catalog (Tempel+/2M++) on BIG-SPARC pushes N_cluster from {ncl} to hundreds.")
        print(f"  Forecast: SE(offset) ~ SE0 * sqrt(N0/N_cluster) (field stays large).\n")
        print(f"  {'N_cluster':>12}{'SE(offset)':>12}{'detect +0.5 dex':>18}{'detect +0.05 dex':>18}")
        print("  " + "-" * 60)
        for Ncl in (ncl, 100, 300, 800):
            se = seoff * math.sqrt(ncl / Ncl)
            print(f"  {Ncl:>12}{se:>12.3f}{0.5 / se:>15.0f}sig{0.05 / se:>15.1f}sig")
        print(f"""
  READING: at N_cluster={ncl} a real +0.05 dex environmental offset is invisible ({0.05/seoff:.1f}sig);
  with a few hundred grouped galaxies it becomes a {0.05/(seoff*math.sqrt(ncl/300)):.1f}sig measurement.
  THIS is BIG-SPARC's unique contribution: not killing the (already-dead) +0.5 fork, but resolving
  whether a0 is EXACTLY environment-independent or carries a small real trend.""")


# =====================================================================================================
#  LIVE PIPELINE  -- runs only if BIG-SPARC data is actually on disk (ready for release day)
# =====================================================================================================
def load_bigsparc(directory):
    """Load BIG-SPARC rotation curves + master table from `directory`.

    EXPECTED LAYOUT (adapt the two parsers below to the released schema; documented assumptions):
      <directory>/rotcurves/<NAME>_rotmod.dat   -- columns R[kpc], Vobs, eVobs, Vgas, Vdisk, Vbul
                                                    (same 6+ columns as SPARC; M/L applied to Vdisk,Vbul)
      <directory>/bigsparc_master.csv           -- per-galaxy: name, RA, Dec, cz/z, D_Mpc, SBeff, Q,
                                                    Vflat, plus environment flags if provided.
    Returns (recs, has_radec): recs is a list of dicts with keys name, la, lag, SBeff, Q, fD, RA, Dec, cz.
    Raise FileNotFoundError if absent (caller routes to forecast())."""
    master_csv = os.path.join(directory, "bigsparc_master.csv")
    rot_dir = os.path.join(directory, "rotcurves")
    if not (os.path.isdir(directory) and os.path.exists(master_csv) and os.path.isdir(rot_dir)):
        raise FileNotFoundError(directory)
    import csv
    meta = {}
    with open(master_csv) as fh:
        for row in csv.DictReader(fh):
            g = lambda k, d=None: row.get(k, d)
            meta[row["name"]] = dict(
                RA=float(g("RA", "nan")), Dec=float(g("Dec", "nan")),
                cz=(float(g("cz")) if g("cz") not in (None, "") else
                    (float(g("z")) * 299792.458 if g("z") not in (None, "") else None)),
                D=float(g("D_Mpc", "nan")), SBeff=float(g("SBeff", "nan")),
                Q=int(float(g("Q", 2))), fD=int(float(g("fD", 0))))
    recs = []
    for f in sorted(glob.glob(os.path.join(rot_dir, "*_rotmod.dat"))):
        name = os.path.basename(f).replace("_rotmod.dat", "")
        m = meta.get(name)
        if not m:
            continue
        rec = dict(name=name, la=fit_a0(f), lag=fit_a0(f, gas_dominated=True))
        rec.update(m)
        recs.append(rec)
    return recs


def assign_environment_density(recs):
    """Cross-match each galaxy to an EXTERNAL group/cluster catalog and attach a physical local density.

    Two independent, non-circular environment axes (whichever catalog is provided via GROUP_CATALOG):
      (A) Tempel+2017 (A&A 602 A100; VizieR J/A+A/602/A100) friends-of-friends groups over SDSS DR12:
          gives group membership, richness Ngal, and group luminosity density -> rho_env in Msun/Mpc^3.
      (B) 2M++ (Lavaux & Hudson 2011) reconstructed density field: smoothed delta(rho)/rho at each
          galaxy position -> a continuous large-scale environment independent of the galaxy's own light.
    Fallback if no catalog file is set: an INTERNAL kNN number-density proxy from the BIG-SPARC
    positions themselves (coarser, but still independent of a0). Sets rec['rho_env'], rec['in_group'].
    """
    if GROUP_CATALOG and os.path.exists(GROUP_CATALOG):
        # ---- real external cross-match (sky-match within a small radius + redshift window) -----------
        cat = np.genfromtxt(GROUP_CATALOG, names=True, delimiter=",")     # adapt to the catalog's format
        for r in recs:
            if not np.isfinite(r.get("RA", float("nan"))):
                r["rho_env"], r["in_group"] = None, None
                continue
            dra = (cat["RA"] - r["RA"]) * math.cos(math.radians(r["Dec"]))
            ddec = cat["Dec"] - r["Dec"]
            sky = np.hypot(dra, ddec)                                      # deg
            dz = np.abs(cat["cz"] - (r["cz"] or 0.0))                      # km/s
            j = np.argmin(sky + (dz > 1000) * 1e3)                        # nearest within ~|dz|<1000 km/s
            ok = sky[j] < 0.5 and dz[j] < 1000
            r["in_group"] = bool(ok and cat["Ngal"][j] >= 3)
            r["rho_env"] = float(cat["rho"][j]) if ok else None
        return "external catalog (" + os.path.basename(GROUP_CATALOG) + ")"
    # ---- fallback: internal kNN density from independent positions (still NOT from a0) --------------
    P = [(r, r.get("RA"), r.get("Dec"), r.get("D")) for r in recs]
    good = [(r, ra, dec, D) for r, ra, dec, D in P
            if ra is not None and np.isfinite(ra) and D and D > 0]
    if len(good) < 30:
        for r in recs:
            r["rho_env"], r["in_group"] = None, None
        return "insufficient positions"
    xyz = np.array([[D * math.cos(math.radians(dec)) * math.cos(math.radians(ra)),
                     D * math.cos(math.radians(dec)) * math.sin(math.radians(ra)),
                     D * math.sin(math.radians(dec))] for _, ra, dec, D in good])
    from scipy.spatial import cKDTree
    k = 5
    dist, _ = cKDTree(xyz).query(xyz, k=k + 1)
    rho = k / (4.0 / 3.0 * math.pi * dist[:, k] ** 3)
    thr = np.percentile(rho, 80)                                          # top quintile = "group-like"
    for (r, *_), rr in zip(good, rho):
        r["rho_env"], r["in_group"] = float(rr), bool(rr >= thr)
    for r in recs:
        r.setdefault("rho_env", None); r.setdefault("in_group", None)
    return "internal kNN proxy (no external catalog supplied)"


def run_bigsparc(recs):
    """Generalized environmental fork test on the loaded BIG-SPARC sample, with full artifact controls."""
    src = assign_environment_density(recs)
    n = sum(1 for r in recs if r["la"] is not None)
    print("#" * 100)
    print(f"# BIG-SPARC LIVE RUN -- {len(recs)} galaxies loaded, {n} with a clean per-galaxy a0; env axis: {src}")
    print("#" * 100)

    def slope(sel, akey, dlog_rho):
        s = [r for r in sel if r[akey] is not None and r.get("rho_env")]
        if len(s) < 10:
            return None
        x = np.log10(np.array([r["rho_env"] for r in s]))
        y = np.array([r[akey] for r in s])
        res = stats.linregress(x, y)
        return res.slope, res.stderr, len(s)

    print("\n  (1) SLOPE  d log a0 / d log(rho_env)   [local-rho fork: +0.5; universal: 0]")
    for tag, sel, akey in [("all (fixed M/L)", recs, "la"),
                           ("Q=1 only", [r for r in recs if r["Q"] == 1], "la"),
                           ("gas-dominated (M/L-free)", recs, "lag"),
                           ("Q=1 & gas-dominated", [r for r in recs if r["Q"] == 1], "lag")]:
        out = slope(sel, akey, True)
        if out:
            sl, se, ns = out
            print(f"     {tag:<26} N={ns:<5} slope={sl:+.3f} +- {se:.3f}   "
                  f"({abs(sl-0.5)/se:.0f}sig from +0.5, {abs(sl)/se:.1f}sig from 0)")

    print("\n  (2) CLUSTER / GROUP vs FIELD offset  [local-rho fork: cluster a0 higher by +0.5 dex per 10x]")
    for tag, sel, akey in [("all (fixed M/L)", recs, "la"), ("Q=1 only", [r for r in recs if r["Q"] == 1], "la")]:
        grp = np.array([r[akey] for r in sel if r.get("in_group") and r[akey] is not None])
        fld = np.array([r[akey] for r in sel if r.get("in_group") is False and r[akey] is not None])
        if grp.size >= 10 and fld.size >= 10:
            U, p = stats.mannwhitneyu(grp, fld, alternative="two-sided")
            print(f"     {tag:<26} group N={grp.size:<5} field N={fld.size:<5} "
                  f"d(med)={np.median(grp)-np.median(fld):+.3f} dex   p(MWU)={p:.3f}")

    print("\n  (3) M/L VARIATION control (a real density signal is M/L-independent; an artifact tracks M/L):")
    for mld in (0.2, 0.5, 0.8):
        s = []
        for r in recs:
            if not r.get("rho_env"):
                continue
            la = fit_a0(os.path.join(BIGSPARC_DIR, "rotcurves", r["name"] + "_rotmod.dat"),
                        mld=mld, mlb=mld * 1.4)
            if la is not None:
                s.append((math.log10(r["rho_env"]), la))
        if len(s) >= 10:
            x, y = np.array([a for a, _ in s]), np.array([b for _, b in s])
            rr, pp = stats.pearsonr(x, y)
            print(f"     M/L_disk={mld}:  r(a0, rho_env) = {rr:+.3f} (p={pp:.3f})  N={len(s)}")

    print("\n  VERDICT TEMPLATE (fill from the numbers above, same honesty discipline):")
    print("   - slope consistent with 0 across artifact-free subsamples  -> NULL, universal a0 confirmed at <sig>;")
    print("   - any nonzero residual slope at the 0.02-0.05 dex level     -> NEW environmental signal, investigate")
    print("     M/L / selection / EFE confounds before claiming physics;")
    print("   - still UNIVERSALITY/CONSISTENCY evidence, NOT causal proof (z~3 evolution remains the only causal test).")


# =====================================================================================================
def main():
    print("#" * 100)
    print("# BIG-SPARC environmental a0-fork test -- projection / live runner")
    print("#" * 100)
    print(f"  BIG-SPARC status (checked {BIGSPARC['checked']}): "
          f"{'PUBLIC' if BIGSPARC['public'] else 'NOT public'} "
          f"(arXiv:{BIGSPARC['arxiv']}, target ~{BIGSPARC['target_N']} galaxies; {BIGSPARC['note']}).")
    print(f"  Looking for BIG-SPARC data in: {os.path.abspath(BIGSPARC_DIR)}")

    try:
        recs_big = load_bigsparc(BIGSPARC_DIR)
        print(f"  -> FOUND BIG-SPARC ({len(recs_big)} rotation curves). Running the live pipeline.\n")
        run_bigsparc(recs_big)
        return
    except FileNotFoundError:
        print("  -> BIG-SPARC data not on disk (expected today). Running the POWER FORECAST instead.\n")

    master = load_master()
    recs = build(master)
    print(f"  Public SPARC anchor: {sum(1 for r in recs if r['la'] is not None)} galaxies with a clean a0 "
          f"({sum(1 for r in recs if r['fD']==4)} Ursa-Major cluster members).\n")
    forecast(recs)

    print("\n" + "#" * 100)
    print("# WHEN BIG-SPARC IS RELEASED -- drop-in instructions")
    print("#" * 100)
    print(f"""  1. Place the rotation curves at {os.path.join('$BIGSPARC_DIR', 'rotcurves', '*_rotmod.dat')}
     and the master at {os.path.join('$BIGSPARC_DIR', 'bigsparc_master.csv')} (schema documented in
     load_bigsparc()). Set BIGSPARC_DIR to its location.
  2. Download a group/cluster catalog for the real environment axis and point GROUP_CATALOG at it:
       - Tempel+2017 FoF groups, VizieR J/A+A/602/A100  (richness + group luminosity density), or
       - 2M++ density field, Lavaux & Hudson 2011       (continuous large-scale delta_rho/rho).
     (Without one, the script falls back to an internal kNN density proxy -- coarser but still
     independent of a0, so non-circular.)
  3. Re-run this script: it auto-detects the data and runs the generalized slope + cluster/field
     test with artifact controls (gas-dominated, Q-cut, M/L variation). Report a NULL as a result.
  HONEST EXPECTATION: the +0.5 local-rho fork is already dead (13-35sig); BIG-SPARC's payoff is the
  ~0.01-0.05 dex residual regime and a real, powered cluster contrast -- not a new shot at a dead fork.""")
    print("#" * 100)


if __name__ == "__main__":
    main()
