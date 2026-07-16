#!/usr/bin/env python3
"""
FIRST FIRING of the pre-registered directional-EFE aligned statistic (n=16)
============================================================================
EXPLORATORY ONLY. n~16, expected sensitivity ~0.2-0.5 sigma at AQUAL amplitude.
This run CANNOT trigger either pre-registered kill condition (banked: the kill
conditions require N in the hundreds-to-thousands; see
real_research/reviews/directional_efe_2026/confrontation.py section 5).
Value = pipeline proof + first number on record. The statistic is reported
AS-IS, whatever its sign and size.

WHAT IS NEW: real g_ext DIRECTIONS (gext_vectors_2026, GATE-A/B passed:
r=0.889 vs Chae amplitudes, Virgo median pointing error 11.6 deg). Every prior
run (confrontation.py) was direction-free.

INPUTS (all read-only):
  repo  = real_research/reviews/directional_efe_2026/  (FROZEN)
    laneA_predictions_results.json  banked signed A(x,e) map (gamma=0, %, BVP)
    laneA_final.out                 banked A(gamma)/A(0) rows (x=0.10) -- the
                                    gamma-attenuation shape (parsed, not typed)
    laneB_merged_catalog.csv        committed WHISP<->SPARC<->Chae crossmatch
    laneB_data/vaneymeren2011_perside.csv  70 WHISP signed per-side rows
    laneB_data/whisp_ugc_aliases.csv       crossmatch verification
    laneB_data/chae21_env.csv              Chae+21 published e_N amplitudes
  gext  = /Users/carlzimmerman/new_physics/gext_vectors_2026/data/gext_vectors.csv
  SPARC rotmod files (repo data/sparc_data) for the outer-point g_bar.

CONVENTIONS (every one stated):
  * PA: position angle on the sky measured EAST OF NORTH, of the RECEDING-side
    kinematic major axis (van Eymeren+2011a convention, their Table 3).
  * g_ext unit vector u: ICRS Cartesian, points TOWARD the net attractor
    (gext_vectors_2026: u = g_vec/|g_vec|, validated by GATE-B against known
    attractor positions). ra_dir/dec_dir = the same vector in spherical form.
  * Sky projection: at galaxy position (east unit e_hat, north unit n_hat),
    PA_gext = atan2(u.e_hat, u.n_hat), east of north.
  * psi = wrap180(PA_gext - PA_receding): angle between the SKY-PROJECTED
    g_ext direction and the receding-side major-axis direction.
    psi = 0  <=> attractor on the RECEDING side.
  * gamma = angle of g_ext to the DISK PLANE: sin(gamma) = |u . n_disk|,
    n_disk = cos(i) l_hat +/- sin(i) b_hat, b_hat = sky direction at
    PA_receding + 90 deg, i = inclination. The near-side/far-side two-fold
    ambiguity is unresolved by tilted-ring fits -> BOTH normal candidates are
    computed and the gamma-attenuation factor is AVERAGED over the two.
  * Signed asymmetry (the laneA/pre-registered definition):
    A_i = 2 (v_rec - v_appr) / (v_rec + v_appr).
    NOTE: the vanEymeren CSV column A_signed is (v_rec - v_appr)/(2 v_c),
    approximately HALF this; A_i is recomputed here from v_rec, v_appr so that
    data and prediction share one convention. The noise sigma_A is recomputed
    from the 70-galaxy WHISP set in the SAME convention (the banked
    0.048-0.092 numbers are the eps_kin convention; ~2x smaller).
  * Predictor: p_i = A_map(x_i, e_i) * G(gamma_i) * cos(psi_i), signed;
    A_map = banked laneA gamma=0 BVP map (bilinear in (log x, e), the
    committed confrontation.py interpolator, sign reversal x <~ e included);
    G(gamma) = banked A(x=0.1, e, gamma)/A(x=0.1, e, 0) shape (mean of the
    e=0.05 and e=0.20 rows), linear in gamma. Banked sign: attractor-facing
    side FASTER for x >~ 2e => p_i > 0 predicts A_i > 0.
  * x_i = g_bar/a0 at the outer RC: mean of the outermost 3 SPARC rotmod
    points, Upsilon_disk = 0.5 (SPARC; 0.70 framework-RAR variant reported),
    Upsilon_bulge = 0.7.
  * e_i = g_ext/a0 from CHAE'S PUBLISHED amplitudes (all 16 are Chae-overlap
    galaxies; the gext_vectors amplitudes are used for NOTHING but the
    direction + robust/soft flag, per the banked usage rules).
    Chae e_N is in gdagger = 1.2e-10 units -> e = 10^log_eN * 1.2e-10 / a0.
  * FOOTINGS (both run, standing rule): a0 canonical = 9.36e-11 (cH_Lambda/Z)
    and alt = 1.13e-10; environment bracket: max-clustering (primary) and
    no-clustering.
  * Stack (pre-registered form): Ahat = sum(A_i p_i / s_i^2)/sum(p_i^2 / s_i^2)
    with s_i = sigma_A (common lopsidedness noise -> cancels in Ahat, enters
    the analytic error). E[Ahat] = 1 AQUAL local-force floor (up to ~5 with
    loop-orbit amplification), ~w = 0.24-0.30 Branch B, 0 null / pure MI.
  * Errors: bootstrap over galaxies (10^4) + PERMUTATION NULL by re-drawing
    each galaxy's g_ext direction ISOTROPICALLY on the sphere (10^4 draws;
    psi AND gamma recomputed per draw). p-values from the null distribution of
    the matched-filter significance Z = sum(A p/s^2)/sqrt(sum(p^2/s^2)).

NO hard-coded results anywhere: every number is computed from the input files
at run time. Outputs land in this directory only; the repo is not touched.
"""
import csv
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
DEFE = os.path.join(REPO, "real_research/reviews/directional_efe_2026")
SPARC = os.path.join(REPO, "real_research/data/sparc_data")
GEXT_CSV = "/Users/carlzimmerman/new_physics/gext_vectors_2026/data/gext_vectors.csv"

A0_CANON = 9.36e-11          # m/s^2, canonical cH_Lambda/Z footing
A0_ALT = 1.13e-10            # m/s^2, alt rho_total/cH0 footing
GDAGGER_CHAE = 1.2e-10       # Chae+21 e_N normalization
KMS2_PER_KPC_TO_SI = 1.0e6 / 3.0856775814913673e19
UPS_DISK, UPS_BUL = 0.5, 0.7
NBOOT, NPERM = 10000, 10000

rng = np.random.default_rng(20260716)

# ----------------------------------------------------------------------------
# 1. banked laneA map (gamma=0) + banked gamma shape (parsed from laneA_final.out)
# ----------------------------------------------------------------------------
with open(os.path.join(DEFE, "laneA_predictions_results.json")) as f:
    laneA = json.load(f)
E_GRID, X_GRID = laneA["E_GRID"], laneA["X_GRID"]
A_MAP = laneA["A_fw_gamma0_pct"]          # framework nu, signed, percent
SIGN_BANKED = laneA["sign"]               # 'attractor_side_faster'
assert SIGN_BANKED == "attractor_side_faster"


def A_aqual_pct(x, e):
    """Signed AQUAL-class aligned asymmetry [%] at gamma=0 -- the committed
    confrontation.py interpolator, verbatim logic: bilinear in (log x, e),
    linear e-scaling below the e-grid (conservative), x clamped to the map
    range [0.05, 0.5] (clamp flagged)."""
    xs = sorted(X_GRID)
    clamped = (-1 if x < xs[0] else (+1 if x > xs[-1] else 0))
    xc = min(max(x, xs[0]), xs[-1])

    def col(e_):
        out = {}
        for xg in xs:
            row = A_MAP[str(xg)]
            if e_ <= E_GRID[0]:
                out[xg] = row[0] * (e_ / E_GRID[0])
            elif e_ >= E_GRID[-1]:
                out[xg] = row[-1]
            else:
                for k in range(len(E_GRID) - 1):
                    if E_GRID[k] <= e_ <= E_GRID[k + 1]:
                        t = (e_ - E_GRID[k]) / (E_GRID[k + 1] - E_GRID[k])
                        out[xg] = row[k] * (1 - t) + row[k + 1] * t
                        break
        return out

    c = col(e)
    lx = math.log(xc)
    for k in range(len(xs) - 1):
        if xs[k] <= xc <= xs[k + 1]:
            t = (lx - math.log(xs[k])) / (math.log(xs[k + 1]) - math.log(xs[k]))
            return c[xs[k]] * (1 - t) + c[xs[k + 1]] * t, clamped
    return c[xs[-1]], clamped


def parse_gamma_shape():
    """Parse the banked A(gamma) rows (x=0.10, e=0.05 and 0.20) from
    laneA_final.out -- the committed run output, not re-typed numbers."""
    txt = open(os.path.join(DEFE, "laneA_final.out")).read()
    block = txt.split("disk-inclination-to-g_ext dependence")[1]
    gline = re.search(r"gamma =\s*([\d\s.]+?)\[deg", block).group(1).split()
    gam_grid = np.array([float(g) for g in gline])
    rows = []
    for m in re.finditer(r"e=(\d\.\d+)((?:\s+[+-]\d+\.\d+)+)", block):
        vals = np.array([float(v) for v in m.group(2).split()])
        rows.append(vals / vals[0])          # normalize to gamma=0
    assert len(rows) == 2 and len(gam_grid) == len(rows[0])
    shape = np.mean(rows, axis=0)
    return gam_grid, shape, rows


GAM_GRID, GAM_SHAPE, GAM_ROWS = parse_gamma_shape()


def G_gamma(gamma_deg):
    """Banked gamma-attenuation factor A(gamma)/A(0), linear interpolation of
    the mean e=0.05/e=0.20 shape (flat-to-rising out to ~30-40 deg, 0 at 90).
    Works on arrays."""
    return np.interp(np.abs(gamma_deg), GAM_GRID, GAM_SHAPE)


# ----------------------------------------------------------------------------
# 2. noise: 70-galaxy WHISP signed asymmetries in the PRE-REGISTERED convention
# ----------------------------------------------------------------------------
whisp = list(csv.DictReader(open(os.path.join(DEFE, "laneB_data",
                                              "vaneymeren2011_perside.csv"))))
A70 = np.array([2.0 * (float(r["v_rec"]) - float(r["v_appr"]))
                / (float(r["v_rec"]) + float(r["v_appr"])) for r in whisp])
eps70 = np.array([float(r["A_signed"]) for r in whisp])   # eps_kin convention
SIG_A = float(np.sqrt(np.mean(A70 ** 2)))                 # primary noise
med = np.median(A70)
SIG_ROB = float(1.4826 * np.median(np.abs(A70 - med)))    # robust variant

# ----------------------------------------------------------------------------
# 3. the n~16 sample: committed crossmatch + directions + Chae amplitudes
# ----------------------------------------------------------------------------
cat = list(csv.DictReader(open(os.path.join(DEFE, "laneB_merged_catalog.csv"))))
gv = {r["name"]: r for r in csv.DictReader(open(GEXT_CSV))}
chae = {r["galaxy"]: r for r in
        csv.DictReader(open(os.path.join(DEFE, "laneB_data", "chae21_env.csv")))}

# alias-file verification of the committed WHISP(UGC) <-> SPARC-name crossmatch
aliases = {}
for r in csv.DictReader(open(os.path.join(DEFE, "laneB_data",
                                          "whisp_ugc_aliases.csv"))):
    key = re.sub(r"\s+", "", r["ugc"]).upper()          # e.g. UGC5079
    aliases.setdefault(key, set()).add(re.sub(r"\s+", "", r["alias"]).upper())

sample = []
for r in cat:
    if r["A_signed"] in ("", "UNSIGNED_ONLY") or not r["log_eN_maxclu"]:
        continue
    name = r["galaxy"]
    ugckey = "UGC%d" % int(r["ugc"])
    naked = re.sub(r"^UGC0+", "UGC", name).upper()
    alias_ok = (naked == ugckey) or (naked in aliases.get(ugckey, set()))
    g = gv.get(name)
    ch = chae.get(name)
    assert g is not None, f"{name}: no g_ext direction row"
    assert ch is not None, f"{name}: not in Chae's published table"
    # Chae amplitude must match what the committed catalog carries
    assert abs(float(ch["log_eN_maxclu"]) - float(r["log_eN_maxclu"])) < 1e-6
    vr, va = float(r["v_rec"]), float(r["v_appr"])
    sample.append(dict(
        name=name, ugc=ugckey, alias_ok=alias_ok,
        A=2.0 * (vr - va) / (vr + va),
        eps_kin=float(r["A_signed"]),
        pa_rec=float(r["pa_receding_deg"]), incl=float(r["incl_deg"]),
        ra=float(g["ra"]), dec=float(g["dec"]),
        u=np.array([float(g["ux_icrs"]), float(g["uy_icrs"]),
                    float(g["uz_icrs"])]),
        ra_dir=float(g["ra_dir"]), dec_dir=float(g["dec_dir"]),
        flag=g["flag"], dom=g["dom_name"], dom_share=float(g["dom_share"]),
        leN_max=float(r["log_eN_maxclu"]), leN_no=float(r["log_eN_noclu"]),
        e_leN_max=float(ch["e_log_eN_maxclu"]),
    ))
n = len(sample)

# ----------------------------------------------------------------------------
# 4. geometry: psi (sky-projected alignment) and gamma (disk-plane angle)
# ----------------------------------------------------------------------------
def basis(ra_deg, dec_deg):
    a, d = math.radians(ra_deg), math.radians(dec_deg)
    los = np.array([math.cos(d) * math.cos(a), math.cos(d) * math.sin(a),
                    math.sin(d)])
    east = np.array([-math.sin(a), math.cos(a), 0.0])
    north = np.array([-math.sin(d) * math.cos(a), -math.sin(d) * math.sin(a),
                      math.cos(d)])
    return los, east, north


def wrap180(x):
    return (x + 180.0) % 360.0 - 180.0


def sky_pa_of_vector(u, east, north):
    """Position angle (east of north, deg) of the sky projection of 3-vector u."""
    return math.degrees(math.atan2(float(u @ east), float(u @ north))) % 360.0


def psi_gamma(s, u):
    """psi (deg, wrapped to [-180,180]) and the two gamma candidates (deg)."""
    los, east, north = s["_basis"]
    pa_g = sky_pa_of_vector(u, east, north)
    psi = wrap180(pa_g - s["pa_rec"])
    # disk normal candidates (near-side two-fold ambiguity)
    qb = math.radians(s["pa_rec"] + 90.0)
    bhat = math.sin(qb) * east + math.cos(qb) * north
    ci, si = math.cos(math.radians(s["incl"])), math.sin(math.radians(s["incl"]))
    gam = []
    for sgn in (+1.0, -1.0):
        nd = ci * los + sgn * si * bhat
        gam.append(math.degrees(math.asin(min(1.0, abs(float(u @ nd))))))
    return psi, gam[0], gam[1]


for s in sample:
    s["_basis"] = basis(s["ra"], s["dec"])
    # parse check: recompute ra_dir/dec_dir from the Cartesian vector
    rd = math.degrees(math.atan2(s["u"][1], s["u"][0])) % 360.0
    dd = math.degrees(math.asin(max(-1.0, min(1.0, s["u"][2]))))
    assert abs(wrap180(rd - s["ra_dir"])) < 0.01 and abs(dd - s["dec_dir"]) < 0.01
    s["psi"], s["gam_a"], s["gam_b"] = psi_gamma(s, s["u"])
    s["Ggam"] = 0.5 * (G_gamma(s["gam_a"]) + G_gamma(s["gam_b"]))

# ----------------------------------------------------------------------------
# 5. per-galaxy x (SPARC outer g_bar) and e (Chae amplitude), both footings
# ----------------------------------------------------------------------------
def gbar_outer(name, upsilon_disk):
    path = os.path.join(SPARC, f"{name}_rotmod.dat")
    rows = []
    for line in open(path):
        if line.startswith("#"):
            continue
        p = line.split()
        if len(p) >= 6:
            R, Vg, Vd, Vb = float(p[0]), float(p[3]), float(p[4]), float(p[5])
            g = (Vg * abs(Vg) + upsilon_disk * Vd * abs(Vd)
                 + UPS_BUL * Vb * abs(Vb)) / R
            rows.append(g * KMS2_PER_KPC_TO_SI)
    assert len(rows) >= 3, f"{name}: <3 rotmod points"
    return sum(rows[-3:]) / 3.0


for s in sample:
    s["gbar"] = gbar_outer(s["name"], UPS_DISK)
    s["gbar_070"] = gbar_outer(s["name"], 0.70)

FOOTINGS = {"canonical a0=9.36e-11": A0_CANON, "alt a0=1.13e-10": A0_ALT}
EBRACKETS = ["maxclu", "noclu"]


def predictor(s, a0, ebr, gbar_key="gbar", use_gamma=True):
    """p_i = A_map(x,e)*G(gamma)*cos(psi) (fraction, signed). Returns (p, clamped)."""
    x = s[gbar_key] / a0
    leN = s["leN_max"] if ebr == "maxclu" else s["leN_no"]
    e = 10.0 ** leN * GDAGGER_CHAE / a0
    Apct, cl = A_aqual_pct(x, e)
    G = s["Ggam"] if use_gamma else 1.0
    return (Apct / 100.0) * G * math.cos(math.radians(s["psi"])), cl, x, e, Apct


# ----------------------------------------------------------------------------
# 6. the stack + bootstrap + isotropic-direction permutation null
# ----------------------------------------------------------------------------
def stack(A, p, sig):
    """Ahat, analytic sigma(Ahat), matched-filter Z. Uniform sig cancels in Ahat."""
    s2 = np.sum(p * p) / sig ** 2
    if s2 <= 0:
        return np.nan, np.nan, np.nan
    ahat = np.sum(A * p) / sig ** 2 / s2
    return ahat, 1.0 / math.sqrt(s2), np.sum(A * p) / sig ** 2 / math.sqrt(s2)


def run_config(rows, a0, ebr, sig, use_gamma=True, gbar_key="gbar",
               nboot=NBOOT, nperm=NPERM):
    A = np.array([r["A"] for r in rows])
    pr = [predictor(r, a0, ebr, gbar_key, use_gamma) for r in rows]
    p = np.array([q[0] for q in pr])
    nclamp_lo = sum(1 for q in pr if q[1] < 0)
    nclamp_hi = sum(1 for q in pr if q[1] > 0)
    ahat, sig_ahat, Z = stack(A, p, sig)

    # leave-one-out (single-galaxy dominance diagnostic)
    loo = np.array([stack(np.delete(A, i), np.delete(p, i), sig)[0]
                    for i in range(len(rows))])

    boot = np.empty(nboot)
    idx = rng.integers(0, len(rows), size=(nboot, len(rows)))
    for b in range(nboot):
        boot[b] = stack(A[idx[b]], p[idx[b]], sig)[0]
    boot = boot[np.isfinite(boot)]

    # permutation null: isotropic re-draw of each galaxy's g_ext direction;
    # psi AND gamma recomputed per draw; base amplitude A_map(x,e) unchanged.
    base = np.array([q[0] / (math.cos(math.radians(r["psi"])) *
                             (r["Ggam"] if use_gamma else 1.0))
                     for q, r in zip(pr, rows)])
    Zn = np.empty(nperm)
    An = np.empty(nperm)
    U = rng.normal(size=(nperm, len(rows), 3))
    U /= np.linalg.norm(U, axis=2, keepdims=True)
    for k in range(nperm):
        pn = np.empty(len(rows))
        for i, r in enumerate(rows):
            psi, ga, gb = psi_gamma(r, U[k, i])
            G = 0.5 * (G_gamma(ga) + G_gamma(gb)) if use_gamma else 1.0
            pn[i] = base[i] * G * math.cos(math.radians(psi))
        An[k], _, Zn[k] = stack(A, pn, sig)
    ok = np.isfinite(Zn)
    p_two = (1 + np.sum(np.abs(Zn[ok]) >= abs(Z))) / (ok.sum() + 1)
    p_one = (1 + np.sum(Zn[ok] >= Z)) / (ok.sum() + 1)
    okA = np.isfinite(An)
    pA_two = (1 + np.sum(np.abs(An[okA]) >= abs(ahat))) / (okA.sum() + 1)
    return dict(n=len(rows), Ahat=float(ahat), sig_analytic=float(sig_ahat),
                Z=float(Z), boot_std=float(np.std(boot)),
                boot_p16=float(np.percentile(boot, 16)),
                boot_p84=float(np.percentile(boot, 84)),
                p_perm_two=float(p_two), p_perm_one=float(p_one),
                p_perm_Ahat_two=float(pA_two),
                null_Z_std=float(np.std(Zn[ok])),
                null_Ahat_std=float(np.std(An[okA])),
                loo_min=float(np.nanmin(loo)), loo_max=float(np.nanmax(loo)),
                loo_min_gal=rows[int(np.nanargmin(loo))]["name"],
                loo_max_gal=rows[int(np.nanargmax(loo))]["name"],
                nclamp_lo=int(nclamp_lo), nclamp_hi=int(nclamp_hi),
                sum_p2=float(np.sum(p * p)))


def main():
    W = 88
    print("=" * W)
    print("FIRST FIRING: pre-registered directional-EFE aligned statistic, n=%d" % n)
    print("EXPLORATORY ONLY -- cannot trigger the pre-registered kill conditions")
    print("=" * W)

    print(f"\n[crossmatch] signed WHISP per-side + Chae e_N + g_ext direction: "
          f"n = {n} galaxies")
    n_alias = sum(s["alias_ok"] for s in sample)
    print(f"  committed UGC<->SPARC crossmatch re-verified via whisp_ugc_aliases.csv: "
          f"{n_alias}/{n} confirmed")
    for s in sample:
        if not s["alias_ok"]:
            print(f"  [warn] {s['name']} <-> {s['ugc']}: not confirmable from the "
                  f"alias file alone (kept; committed catalog is authoritative)")
    nr = sum(s["flag"] == "robust" for s in sample)
    print(f"  direction quality: {nr} robust / {n - nr} soft "
          f"(gext_vectors_2026 flag; GATE-A r=0.889, GATE-B Virgo 11.6 deg)")
    print(f"  Chae published amplitudes used for ALL {n} (all are Chae-overlap; "
          f"the +0.10 dex own-amplitude path is not needed)")

    print(f"\n[noise, recomputed in the pre-registered A-convention from 70 WHISP]")
    print(f"  A = 2(v_rec-v_appr)/(v_rec+v_appr):  rms = {SIG_A:.4f}   "
          f"robust (1.4826*MAD) = {SIG_ROB:.4f}")
    print(f"  (banked eps_kin=(v_rec-v_appr)/2v_c convention: rms = "
          f"{np.sqrt(np.mean(eps70**2)):.4f}, robust = "
          f"{1.4826*np.median(np.abs(eps70-np.median(eps70))):.4f} -- the "
          f"0.048-0.092 numbers; factor ~2 is pure convention)")
    print(f"  sigma_i = {SIG_A:.4f} (common) -> cancels in Ahat; enters Z and "
          f"the analytic error only")

    print(f"\n[banked gamma shape] A(gamma)/A(0) at x=0.10 from laneA_final.out:")
    print(f"  gamma grid {GAM_GRID.tolist()} deg; e=0.05 row "
          f"{np.round(GAM_ROWS[0],3).tolist()}; e=0.20 row "
          f"{np.round(GAM_ROWS[1],3).tolist()}; mean shape used "
          f"{np.round(GAM_SHAPE,3).tolist()}")

    # ---------------- per-galaxy table (primary config) ----------------
    a0p, ebrp = A0_CANON, "maxclu"
    print(f"\n[per-galaxy] primary config: canonical a0=9.36e-11, Chae max-clustering e_N,")
    print(f"  Upsilon_disk=0.5, banked gamma shape. p_i = A_map(x,e)*G(gamma)*cos(psi).")
    hdr = (f"  {'galaxy':<10}{'flag':>7}{'A_i':>9}{'psi':>8}{'cospsi':>8}"
           f"{'gam_a':>7}{'gam_b':>7}{'G':>6}{'x':>8}{'e':>8}{'Amap%':>8}"
           f"{'p_i%':>8}{'dom':>16}")
    print(hdr)
    table = []
    for s in sample:
        p, cl, x, e, Apct = predictor(s, a0p, ebrp)
        table.append(dict(name=s["name"], flag=s["flag"], A_signed=round(s["A"], 4),
                          psi_deg=round(s["psi"], 1),
                          cos_psi=round(math.cos(math.radians(s["psi"])), 3),
                          gamma_a_deg=round(s["gam_a"], 1),
                          gamma_b_deg=round(s["gam_b"], 1),
                          G_gamma=round(float(s["Ggam"]), 3),
                          x=round(x, 3), e=round(e, 4), x_clamped=int(cl),
                          A_map_pct=round(Apct, 3), p_pct=round(100 * p, 4),
                          dom=f"{s['dom']}({s['dom_share']:.2f})"))
        cltxt = {0: "", -1: "  [x clamped up to 0.05]",
                 1: "  [x clamped down to 0.5]"}[cl]
        print(f"  {s['name']:<10}{s['flag']:>7}{s['A']:>+9.4f}{s['psi']:>8.1f}"
              f"{math.cos(math.radians(s['psi'])):>8.3f}{s['gam_a']:>7.1f}"
              f"{s['gam_b']:>7.1f}{s['Ggam']:>6.3f}{x:>8.3f}{e:>8.4f}"
              f"{Apct:>+8.3f}{100*p:>+8.4f}  {table[-1]['dom']}{cltxt}")

    # ---------------- fire: primary + strata + footings ----------------
    robust = [s for s in sample if s["flag"] == "robust"]
    results = {}
    print(f"\n[THE STACK]  Ahat = sum(A p/s^2)/sum(p^2/s^2);  E[Ahat]=1 AQUAL floor "
          f"(~5 loop-orbit top), ~0.24-0.30 Branch B, 0 null/pure-MI")
    print(f"  {'config':<44}{'n':>3}{'Ahat':>9}{'boot_sd':>9}{'sig_an':>8}"
          f"{'Z':>7}{'p2':>7}{'p1':>7}{'pA2':>7}{'LOO range':>16}")
    for tag, rows in (("ALL", sample), ("ROBUST-only", robust)):
        for fn, a0 in FOOTINGS.items():
            for ebr in EBRACKETS:
                key = f"{tag} | {fn} | {ebr}"
                r = run_config(rows, a0, ebr, SIG_A)
                results[key] = r
                print(f"  {key:<44}{r['n']:>3}{r['Ahat']:>+9.2f}"
                      f"{r['boot_std']:>9.2f}{r['sig_analytic']:>8.2f}"
                      f"{r['Z']:>+7.2f}{r['p_perm_two']:>7.3f}"
                      f"{r['p_perm_one']:>7.3f}{r['p_perm_Ahat_two']:>7.3f}"
                      f"  {r['loo_min']:>+6.2f}..{r['loo_max']:<+6.2f}")

    # sensitivity variants on the primary (ALL | canonical | maxclu)
    print(f"\n[variants on the primary config] (ALL galaxies, canonical a0, maxclu)")
    var = {}
    var["gamma_off (G=1)"] = run_config(sample, A0_CANON, "maxclu", SIG_A,
                                        use_gamma=False)
    var["Upsilon_disk=0.70"] = run_config(sample, A0_CANON, "maxclu", SIG_A,
                                          gbar_key="gbar_070")
    for k, r in var.items():
        results[f"variant | {k}"] = r
        print(f"  {k:<44}{r['n']:>3}{r['Ahat']:>+9.2f}{r['boot_std']:>9.2f}"
              f"{r['sig_analytic']:>8.2f}{r['Z']:>+7.2f}{r['p_perm_two']:>7.3f}"
              f"{r['p_perm_one']:>7.3f}")
    print(f"  robust-sigma ({SIG_ROB:.3f}) rescales Z by x{SIG_A/SIG_ROB:.2f} "
          f"and the analytic error by x{SIG_ROB/SIG_A:.2f}; Ahat unchanged.")

    prim = results["ALL | canonical a0=9.36e-11 | maxclu"]
    exp_sig = 1.0 / prim["sig_analytic"]
    print(f"\n[sensitivity, computed] analytic sigma(Ahat) = "
          f"{prim['sig_analytic']:.2f} at the primary config -> an E[Ahat]=1 "
          f"AQUAL signal registers at ~{exp_sig:.2f} sigma; even the ~5x "
          f"loop-orbit top registers at ~{5*exp_sig:.2f} sigma. n={n} is "
          f"EXPLORATORY, exactly as pre-registered.")

    print(f"  [flag] x-clamps at the primary config: {prim['nclamp_lo']}/{n} "
          f"below the banked map range (clamped UP to x=0.05: deeper-MOND "
          f"galaxies whose true |A_map| is LARGER -> their p_i is "
          f"UNDERSTATED; all have x >> 2e so no sign-reversal risk), "
          f"{prim['nclamp_hi']}/{n} above (clamped down to x=0.5).")
    print(f"  [leave-one-out] primary-config Ahat range over single-galaxy "
          f"removal: {prim['loo_min']:+.2f} (drop {prim['loo_min_gal']}) to "
          f"{prim['loo_max']:+.2f} (drop {prim['loo_max_gal']}) -- reported "
          f"straight; at n={n} single galaxies matter, as expected.")

    out = dict(
        DISCLAIMER=("EXPLORATORY, n=%d, expected sensitivity ~%.2f sigma at "
                    "AQUAL amplitude; CANNOT trigger the pre-registered kill "
                    "conditions; value = pipeline proof + first number on "
                    "record." % (n, exp_sig)),
        n=n, n_robust=len(robust),
        sigma_A_preregistered_convention=SIG_A, sigma_A_robust=SIG_ROB,
        gamma_grid=GAM_GRID.tolist(), gamma_shape=GAM_SHAPE.tolist(),
        per_galaxy=table, stacks=results,
        conventions=dict(
            A="2(v_rec-v_appr)/(v_rec+v_appr), sign tied to the receding side",
            PA="east of north, receding-side kinematic major axis (vanEymeren)",
            psi="PA(sky-projected g_ext, toward attractor) - PA(receding side)",
            gamma="angle of g_ext to disk plane; both near-side candidates "
                  "averaged in G(gamma)",
            predictor="A_map(x,e; banked laneA BVP, gamma=0)*G(gamma)*cos(psi)",
            sign="attractor-facing side FASTER for x>~2e (banked), reversal "
                 "x<~e carried by the signed map",
            footings="a0 canonical 9.36e-11 primary, alt 1.13e-10; Chae "
                     "max-clustering e_N primary, no-clustering bracket",
            noise="common sigma_A from 70 WHISP, same A convention",
        ),
    )
    with open(os.path.join(HERE, "fire_aligned_n16_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results JSON -> {os.path.join(HERE, 'fire_aligned_n16_results.json')}")
    print("=" * W)
    print("FIRST FIRING COMPLETE (exit 0) -- exploratory number on record; "
          "kill conditions UNTOUCHED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
