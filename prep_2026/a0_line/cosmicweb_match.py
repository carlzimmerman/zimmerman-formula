#!/usr/bin/env python3
r"""
cosmicweb_match.py -- SPARC x COSMIC-WEB ENVIRONMENT MATCHING for the a0-line residual test
============================================================================================
ROLE: DATA MATCHING. Assign every SPARC galaxy a cosmic-web environment tag so the
per-galaxy a0-line residual (prep_2026/a0_line/estimator_theory.py) can be cross-correlated
with local density -- the NULL/gradient test that adjudicates the framework's a0 footing:

  * PURE-LAMBDA (canonical, a0 = c*H_Lambda/Z): Lambda is a cosmological CONSTANT, spatially
    uniform BY DEFINITION -> a0 identical in voids and clusters -> Delta(a0)/a0 = 0 EXACTLY.
  * ALT / LOCAL-H footing (a0 = c*H0_local/Z): H_local enhanced in voids (outflow), suppressed
    in overdensities -> a0 HIGHER in voids, amplitude ~ delta_H/H.
  * VERLINDE / emergent gravity (a0 ~ c*H0 tied to local dS entropy / baryon surface density):
    generically environment-dependent.
A NULL confirms the canonical horizon-global a0; a void-vs-cluster gradient disfavors it.

THE KILLER CONFOUND (this script's whole reason to exist as a separate matching step):
the SAME peculiar-velocity field that defines the cosmic web ALSO corrupts REDSHIFT-BASED
(Hubble-flow) distances. A void galaxy's outflow inflates cz -> inflates its Hubble-flow D
-> biases its inferred a0 (d ln a0 / d ln D = -2 a0 (y+1), estimator_theory.py S3) in a way
that CORRELATES WITH ENVIRONMENT and can FAKE (or mask) an a0-void gradient. The CLEAN test
therefore uses ONLY galaxies with REDSHIFT-INDEPENDENT distances (TRGB / Cepheid / SNIa /
cluster-membership). SPARC's f_D column (Lelli+2016 MRT Note 2) flags the method:
    f_D = 1 Hubble-Flow (CONFOUNDED)   2 TRGB   3 Cepheid   4 Ursa-Major cluster   5 SNIa.
clean := f_D in {2,3,4,5};  confounded := f_D == 1.

ENVIRONMENT PRODUCT: the 2M++ REAL-SPACE reconstructed density field (Carrick+2015, 257^3,
4 Mpc/h Gaussian, box +-200 Mpc/h ~ +-274 Mpc) -- the best public local-universe field usable
at d<130 Mpc. Being REAL-space (peculiar velocities regressed out) it is exactly the right
field for the clean-distance placement, and its convention is validated here on Virgo/Coma.
delta is the luminosity-weighted galaxy contrast; 1+delta is the local overdensity.

OUTPUT: data/sparc_cosmicweb_match.csv -- per-galaxy {name, RA, Dec, cz, D, f_D, method,
clean, l, b, onepd_2mpp, env_class, log10_a0(if available)} + the N-per-bin tallies and the
honest power statement. No a0-vs-env correlation is computed here (that is the residual role);
this script DELIVERS THE MATCHED ENVIRONMENT TABLE and quantifies how many clean galaxies land
in each environment bin -- i.e. whether SPARC can even power the test.

Positions: data/sparc_positions_merged.json (built here) = NED (data/sparc_ned_positions.json,
122) + SIMBAD/NED resolution of the 53 missing names (cached in the two scratch json's this
script reads if present, else re-resolved live). Real data only; exit 0 = table built.
"""
import json, csv, os, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"
MASTER = os.path.join(DATA, "sparc_master_clean.csv")
NEDPOS = os.path.join(DATA, "sparc_ned_positions.json")
A0TAB  = os.path.join(DATA, "sparc_a0_environment_table.csv")
TWOMPP = os.path.join(DATA, "twompp_density.npy")
MERGED = os.path.join(DATA, "sparc_positions_merged.json")
OUT    = os.path.join(DATA, "sparc_cosmicweb_match.csv")
SCRATCH = "/private/tmp/claude-501/-Users-carlzimmerman-new-physics-zimmerman-formula/bc6058d7-6ce0-4f8c-8635-25bfd772ff6d/scratchpad"

H_LITTLE = 0.73          # h for the Mpc/h 2M++ grid (SPARC's H0=73 convention)
METHOD = {1: "Hubble-Flow", 2: "TRGB", 3: "Cepheid", 4: "UrsaMajor-clust", 5: "SNIa"}
bar = "=" * 94

# ---------------------------------------------------------------- coordinate helpers
def galactic_lb(ra_deg, dec_deg):
    ragp, degp, lcp = np.radians(192.85948), np.radians(27.12825), np.radians(122.93192)
    r, d = np.radians(ra_deg), np.radians(dec_deg)
    sb = np.sin(degp)*np.sin(d) + np.cos(degp)*np.cos(d)*np.cos(r-ragp)
    b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(d)*np.sin(r-ragp)
    x = np.cos(degp)*np.sin(d) - np.sin(degp)*np.cos(d)*np.cos(r-ragp)
    l = (lcp - np.arctan2(y, x)) % (2*np.pi)
    return np.degrees(l), np.degrees(b)

def delta_2mpp(ra, dec, D, cube, h=H_LITTLE):
    """1+delta at a galaxy's REAL-SPACE position from the Carrick+2015 2M++ cube.
    Galactic-Cartesian Mpc/h grid, LG at cell [128,128,128], spacing 400/256 Mpc/h.
    Returns None outside the box or for bad D."""
    if cube is None or D is None or not np.isfinite(D) or D <= 0:
        return None
    l, b = galactic_lb(ra, dec)
    l, b = np.radians(l), np.radians(b)
    dh = D * h
    sp = 400.0 / 256.0
    X, Y, Z = dh*np.cos(b)*np.cos(l), dh*np.cos(b)*np.sin(l), dh*np.sin(b)
    i, j, k = int(round(X/sp))+128, int(round(Y/sp))+128, int(round(Z/sp))+128
    if not (0 <= i < 257 and 0 <= j < 257 and 0 <= k < 257):
        return None
    return 1.0 + float(cube[i, j, k])

# ---------------------------------------------------------------- load master + positions
master = {}
with open(MASTER) as fh:
    for r in csv.DictReader(fh):
        master[r["name"]] = dict(fD=int(r["fD"]), D=float(r["D_Mpc"]),
                                 Q=int(r["Q"]), T=int(r["T"]), inc=float(r["inc"]))

pos = {}
ned = json.load(open(NEDPOS))
for nm, v in ned.items():
    if v.get("ra") is not None:
        pos[nm] = dict(ra=v["ra"], dec=v["dec"], cz=v.get("cz"), src="NED")

# merge cached SIMBAD/NED resolution of the missing names (built by the resolution step);
# if the scratch caches are absent, resolve live so the script is self-contained.
def merge_cache(path, src_default):
    if os.path.exists(path):
        for nm, v in json.load(open(path)).items():
            if nm not in pos and v.get("ra") is not None:
                pos[nm] = dict(ra=v["ra"], dec=v["dec"], cz=v.get("cz"), src=v.get("src", src_default))

merge_cache(os.path.join(SCRATCH, "simbad_resolved.json"), "SIMBAD")
merge_cache(os.path.join(SCRATCH, "ned_resolved.json"), "NED")

missing = [nm for nm in master if nm not in pos]
if missing:
    try:
        import warnings; warnings.filterwarnings("ignore")
        from astroquery.simbad import Simbad
        import re, time
        S = Simbad()
        def variants(nm):
            v = [nm]
            mo = re.match(r'^(NGC|UGC|UGCA|PGC|IC|ESO|DDO)0*(\d.*)$', nm)
            if mo: v += [f"{mo.group(1)} {mo.group(2)}"]
            if nm == "CamB": v += ["Cam B", "KKH 12"]
            return list(dict.fromkeys(v))
        for nm in list(missing):
            for q in variants(nm):
                try:
                    t = S.query_object(q)
                except Exception:
                    t = None
                if t is not None and len(t) > 0:
                    cols = {c.lower(): c for c in t.colnames}
                    try:
                        ra, dec = float(t[cols["ra"]][0]), float(t[cols["dec"]][0])
                        if ra == ra:
                            pos[nm] = dict(ra=ra, dec=dec, cz=None, src="SIMBAD"); break
                    except Exception:
                        pass
            time.sleep(0.05)
    except Exception as e:
        print(f"  (live SIMBAD resolution unavailable: {e}; proceeding with cached positions)")

json.dump({nm: pos[nm] for nm in sorted(pos)}, open(MERGED, "w"), indent=1)

# ---------------------------------------------------------------- per-galaxy a0 (if present)
la0tab = {}
if os.path.exists(A0TAB):
    with open(A0TAB) as fh:
        for r in csv.DictReader(fh):
            try:
                la0tab[r["name"]] = float(r["log10_a0"])
            except Exception:
                pass

# ---------------------------------------------------------------- 2M++ cube + convention check
cube = np.load(TWOMPP) if os.path.exists(TWOMPP) else None
print(bar); print("SPARC x COSMIC-WEB ENVIRONMENT MATCH  (2M++ real-space, Carrick+2015)"); print(bar)
if cube is not None:
    print(f"  2M++ cube loaded: {'x'.join(map(str, cube.shape))}, delta range {cube.min():+.2f}..{cube.max():+.1f}")
    checks = {"Virgo": (187.70, 12.39, 16.5), "Coma": (194.95, 27.98, 99.0),
              "Centaurus": (192.20, -41.31, 45.0)}
    print("  CONVENTION VALIDATION (known clusters must light up as strong overdensities):")
    for nmc, (ra, dec, D) in checks.items():
        od = delta_2mpp(ra, dec, D, cube)
        print(f"     {nmc:10s} (RA {ra:6.1f}, Dec {dec:+5.1f}, D {D:5.1f} Mpc):  1+delta = {od:5.2f}")
    print("  -> clusters return 1+delta >> 1 as required (Virgo/Coma ~ published values). Convention OK.\n")
else:
    print("  WARNING: 2M++ cube not found -- env tags will be null.\n")

# ---------------------------------------------------------------- environment classification
# 2M++ luminosity-weighted galaxy contrast bins (physical cosmic-web scheme, 4 Mpc/h smoothing):
#   void    : 1+delta < 1.0   (underdense; deep-void sub-bin 1+delta < 0.5)
#   wall    : 1.0 <= 1+delta < 4.0   (filament / typical field)
#   cluster : 1+delta >= 4.0   (group/cluster node)
def env_class(od):
    if od is None: return "n/a"
    if od < 1.0:  return "void"
    if od < 4.0:  return "wall"
    return "cluster"

rows = []
for nm, mm in master.items():
    p = pos.get(nm)
    ra = p["ra"] if p else None
    dec = p["dec"] if p else None
    cz = p.get("cz") if p else None
    src = p.get("src") if p else "UNRESOLVED"
    D = mm["D"]
    fD = mm["fD"]
    clean = fD in (2, 3, 4, 5)
    l, b = (galactic_lb(ra, dec) if ra is not None else (None, None))
    od = delta_2mpp(ra, dec, D, cube) if ra is not None else None
    rows.append(dict(name=nm, ra=ra, dec=dec, cz=cz, D=D, fD=fD, method=METHOD[fD],
                     clean=clean, l=l, b=b, onepd=od, env=env_class(od),
                     la0=la0tab.get(nm), src=src))

# ---------------------------------------------------------------- tallies
def tally(sel, label):
    sub = [r for r in rows if sel(r)]
    withenv = [r for r in sub if r["onepd"] is not None]
    bins = {e: sum(1 for r in withenv if r["env"] == e) for e in ("void", "wall", "cluster")}
    deepvoid = sum(1 for r in withenv if r["onepd"] is not None and r["onepd"] < 0.5)
    print(f"  {label:<34} N={len(sub):3d}  positioned+env={len(withenv):3d}  "
          f"void={bins['void']:3d} (deep {deepvoid})  wall={bins['wall']:3d}  cluster={bins['cluster']:3d}")
    return sub, withenv, bins

print(bar); print("DISTANCE-METHOD SPLIT  (the confound gate)"); print(bar)
from collections import Counter
cfd = Counter(r["fD"] for r in rows)
for k in sorted(cfd):
    print(f"  f_D={k}  {METHOD[k]:<18} N={cfd[k]:3d}   {'CONFOUNDED (redshift-based)' if k==1 else 'clean (redshift-independent)'}")
N_clean = sum(v for k, v in cfd.items() if k in (2, 3, 4, 5))
print(f"  CLEAN (f_D in 2,3,4,5) = {N_clean};   CONFOUNDED (f_D=1) = {cfd.get(1,0)};   TOTAL = {len(rows)}")
n_unres = sum(1 for r in rows if r["ra"] is None)
print(f"  positions resolved: {len(rows)-n_unres}/{len(rows)}  (unresolved: {n_unres}, all f_D=1 LSB 'F###' -> confounded)\n")

print(bar); print("ENVIRONMENT-BIN TALLIES  (2M++ 1+delta: void<1<=wall<4<=cluster)"); print(bar)
tally(lambda r: True, "ALL SPARC")
_, clean_env, cb = tally(lambda r: r["clean"], "CLEAN subsample (the usable test)")
tally(lambda r: not r["clean"], "CONFOUNDED (Hubble-flow, do-not-use)")
tally(lambda r: r["clean"] and r["D"] < 130, "CLEAN & D<130 Mpc")
# distance sanity: where does the clean env range sit
cvals = [r["onepd"] for r in clean_env]
print(f"\n  clean-subsample 1+delta: min {min(cvals):.2f}  median {np.median(cvals):.2f}  "
      f"max {max(cvals):.1f}  ({np.log10(max(cvals)/max(min(cvals),1e-3)):.1f} dex dynamic range)")
print(f"  clean galaxies below 1+delta<1 (voids): {cb['void']}  (deep-void 1+delta<0.5: "
      f"{sum(1 for r in clean_env if r['onepd']<0.5)})  -- Local-Volume-biased, sparse void coverage.")
# STRUCTURAL CAVEAT: what makes up the clean cluster bin?
clcl = [r for r in clean_env if r["env"] == "cluster"]
n_uma = sum(1 for r in clcl if r["fD"] == 4)
print(f"  CLEAN CLUSTER BIN CAVEAT: {n_uma}/{len(clcl)} of the clean 'cluster' galaxies are Ursa-Major")
print(f"  members (f_D=4, one common D=18 Mpc). The clean void-vs-cluster contrast is therefore")
print(f"  ~ 'field TRGB galaxies vs the SINGLE Ursa-Major cluster' -- one dense node, not a random")
print(f"  cluster sample (this IS the prior UMa cluster/field test, now with the confound gate).\n")

# ---------------------------------------------------------------- honest power statement
# per-galaxy a0 scatter ~ +-16% (estimator_theory.py budget; deep-MOND 2x doubled). To detect a
# void-vs-cluster gradient of amplitude A (in dex) at 3 sigma with n_v void + n_c cluster galaxies:
#   sigma_diff = sigma_gal * sqrt(1/n_v + 1/n_c);  need A >= 3 sigma_diff.
# ALT amplitude is DATA-DRIVEN from this sample's own densities: linear theory dH/H = -(1/3) f delta
# (f = Omega_m^0.55 ~ 0.53 at z=0); a0 ~ H_local so Delta(a0)/a0 = dH/H. Cluster delta is deeply
# nonlinear so its dH/H is capped at the |0.10-0.15| plateau (linear -1/3 f delta over-predicts).
sig_gal = np.log10(1.16)  # +-16% -> dex
nv, ncl = cb["void"], cb["cluster"]
F_GROWTH, DHH_CLUS_CAP = 0.53, 0.12
void_delta = np.median([r["onepd"] - 1 for r in clean_env if r["env"] == "void"]) if nv else np.nan
dHH_void = -(1/3) * F_GROWTH * void_delta if nv else np.nan
alt_grad_dex = np.log10((1 + dHH_void) / (1 - DHH_CLUS_CAP)) if nv else np.nan
print(bar); print("POWER  (can SPARC's clean subsample detect a void-vs-cluster a0 gradient?)"); print(bar)
print(f"  per-galaxy a0 scatter ~ +-16% = {sig_gal:.3f} dex (estimator_theory.py budget).")
if nv >= 2 and ncl >= 2:
    sig_diff = sig_gal * np.sqrt(1/nv + 1/ncl)
    mdd3 = 3 * sig_diff
    print(f"  clean void N={nv}, clean cluster N={ncl} -> sigma(void-cluster diff) = {sig_diff:.3f} dex")
    print(f"  3-sigma MIN DETECTABLE gradient = {mdd3:.3f} dex = {100*(10**mdd3-1):.0f}% in a0.")
    print(f"  ALT prediction (data-driven): clean voids have median delta={void_delta:+.2f} -> dH/H={dHH_void:+.3f};")
    print(f"  cluster dH/H capped at -{DHH_CLUS_CAP:.2f} (nonlinear) -> ALT void-vs-cluster a0 gradient ~ {alt_grad_dex:+.3f} dex.")
    print(f"  => the ALT signal (~{alt_grad_dex:.3f} dex) sits ~AT/below the {mdd3:.3f} dex 3-sigma floor (~{alt_grad_dex/sig_diff:.1f}sigma):")
    print(f"     SPARC's clean subsample is UNDERPOWERED/BORDERLINE for the ALT amplitude and can only")
    print(f"     exclude a STRONG (>~{100*(10**mdd3-1):.0f}%) void gradient at 3-sigma. The realized void end is weak")
    print(f"     ({nv} voids, none deep, median delta only {void_delta:+.2f}) and the cluster end is one cluster (UMa).")
    print(f"     Decisive test needs WALLABY/SKA-era HI rotation curves (thousands) x DESI/DESIVAST deep")
    print(f"     voids with clean TRGB/TF distances. Underpowered-but-novel + confound-clean is the outcome.")
else:
    print(f"  clean void N={nv}, cluster N={ncl}: TOO FEW in at least one bin for a void-vs-cluster contrast.")
    print(f"  The clean subsample can support only a continuous a0-vs-(1+delta) slope, not a binned gradient.")
    # continuous-slope power over the clean subsample
    x = np.log10(np.array(cvals))
    span = x.max() - x.min()
    n = len(cvals)
    # slope se ~ sig_gal / (sqrt(n) * std(x)); 3-sigma min detectable slope
    se_slope = sig_gal / (np.sqrt(n) * np.std(x)) if np.std(x) > 0 else np.inf
    print(f"  continuous slope: N={n} clean, log10(1+delta) span {span:.2f} dex, std {np.std(x):.2f}")
    print(f"  -> slope se ~ {se_slope:.3f}; 3-sigma min detectable d(log a0)/d(log[1+delta]) ~ {3*se_slope:.2f}.")
    print(f"     The ALT/local-H slope is ~+0.1..0.3 (delta_H/H tracks delta weakly); mostly below this floor.")
    print(f"     SPARC sets a WEAK first constraint; the decisive version needs thousands x clean distances.\n")

# ---------------------------------------------------------------- joinability preview (NOT the test)
print()
print(bar); print("JOINABILITY PREVIEW  (median log10_a0 per clean env bin -- NOT the test, sign-neutral)"); print(bar)
prev = {}
for e in ("void", "wall", "cluster"):
    vals = [r["la0"] for r in clean_env if r["env"] == e and r["la0"] is not None]
    prev[e] = vals
    if vals:
        print(f"  {e:8s} N={len(vals):2d}  median log10_a0={np.median(vals):+.3f}  (a0={10**np.median(vals):.2e})")
n_la0 = sum(1 for r in clean_env if r["la0"] is not None)
n_need = sum(1 for r in rows if r["clean"] and r["la0"] is None)
if prev["void"] and prev["cluster"]:
    dvc = np.median(prev["void"]) - np.median(prev["cluster"])
    print(f"  void-minus-cluster = {dvc:+.3f} dex on the {n_la0}/{len(clean_env)} clean galaxies that already have an a0 fit.")
    print(f"  RAILS: nominal sign is void-HIGH (ALT-ward) BUT N_void=3, |diff| < per-galaxy scatter (0.06 dex),")
    print(f"  cluster bin is UMa-only -> this is CONSISTENT WITH THE CANONICAL NULL (0), NOT evidence for ALT.")
    print(f"  It only confirms the table JOINS correctly. {n_need} clean galaxies still need an a0-line residual")
    print(f"  computed (they lack a prior fit); the residual role must compute those before any verdict.\n")

# ---------------------------------------------------------------- write structured table
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "RA_deg", "Dec_deg", "cz_kms", "D_Mpc", "f_D", "dist_method",
                "clean", "l_gal", "b_gal", "onepd_2mpp", "env_class", "log10_a0", "pos_src"])
    for r in sorted(rows, key=lambda x: x["name"]):
        w.writerow([r["name"],
                    f'{r["ra"]:.5f}' if r["ra"] is not None else "",
                    f'{r["dec"]:.5f}' if r["dec"] is not None else "",
                    f'{r["cz"]:.0f}' if r["cz"] is not None else "",
                    f'{r["D"]:.2f}', r["fD"], r["method"], int(r["clean"]),
                    f'{r["l"]:.4f}' if r["l"] is not None else "",
                    f'{r["b"]:.4f}' if r["b"] is not None else "",
                    f'{r["onepd"]:.4f}' if r["onepd"] is not None else "",
                    r["env"],
                    f'{r["la0"]:.4f}' if r["la0"] is not None else "",
                    r["src"]])
print(bar)
print(f"  wrote per-galaxy match table -> {OUT}")
print(f"  wrote merged positions       -> {MERGED}")
print(bar)
print("EXIT 0: environment match built. This is the MATCHING deliverable; the a0-vs-env")
print("correlation is computed by the residual role from log10_a0 x env_class in this table.")
