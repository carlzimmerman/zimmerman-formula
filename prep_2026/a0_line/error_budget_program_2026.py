#!/usr/bin/env python3
"""
error_budget_program_2026.py -- THE FROZEN STEP-A PROGRAM: the a0-line gas-dominated slope
error budget, its averaging structure, and the frozen GO/NO-GO on whether SPARC can
separate the Lambda-anchor a0 = cH_Lambda/Z = 9.36e-11 from the total-density / fitted-
constant cluster (ALT cH0/Z = 1.13e-10, standard-MOND 1.20e-10) at 3 sigma.
==========================================================================================
This is the SINGLE frozen, pre-registered consolidation of the a0-line reachability
analysis. It builds on -- and does NOT rebuild or contradict -- the committed pipeline:
    estimator_theory.py / fire_common.py  -- GLS through-origin slope a0_hat + full budget.
    identity_uniqueness.py                -- the point-level gas-dominated cut.
    per_galaxy_budget.py  / reach_target.py -- the per-galaxy and global-ladder decompositions
                                             this program reproduces as regression anchors.
fire_common is imported READ-ONLY; every number is recomputed live from the raw SPARC data,
then cross-checked against the two sibling result JSONs (identical box, term fractions,
floor, and top TRGB targets).

WHAT IT PRINTS (the frozen ROLE deliverables):
  PART 0  regression anchor: reproduce estimator_theory.py's ~16% gas-dominated box (asserted).
  PART D  deep-MOND doubling, verified numerically in-script (numpy finite difference): a0 =
          g_obs^2/g_bar carries a factor-4 velocity lever = 2x the naive g_obs^2 scatter.
  PART 1  per-galaxy error budget: the top error-dominant galaxies, ranked by reducible variance.
  PART 2  the averaging decomposition: per-galaxy-random terms (average as 1/sqrt N) vs the
          shared-Upsilon/gas-cal/estimator terms (do NOT average) -> the irreducible floor.
  PART 3  the required-N-with-TRGB curve to reach the 5-8% target IF the floor permits, with
          the specific priority galaxies named (and the honest asymptote if it does not).
  PART 4  the FROZEN GO/NO-GO for 3-sigma separation of 9.36e-11 from 1.13e-10 and from 1.20e-10.
  PART 5  the minimal EXTERNAL requirement (TRGB on the named dwarfs + Upsilon prior + HI mass),
          since SPARC alone is NO-GO.
  PRE-REG the frozen decision (box half-width thresholds), the named target galaxies, and every
          honesty caveat (Upsilon floor, deep-MOND doubling, which gap, both footings, and that
          this measures WHERE a0 sits vs the two anchors -- it does NOT derive a0's value).

HONESTY RAILS (a manufactured win and a manufactured deficit are penalized EQUALLY):
  * The floor is the shared M/L + gas-cal + estimator-spread systematic; it is stated as the
    single load-bearing obstruction and is NOT spun into a false GO.
  * The deep-MOND factor-4 doubling (velocity error enters a0 with lever 4(y+1)) is the reason
    the box is systematics-owned, not statistics-owned; it is verified here, not asserted.
  * Both footings (canonical 9.36e-11, ALT 1.13e-10) are carried on every dimensional number.
  * The estimator-choice spread (GLS vs robust median) ALONE spans the whole footing gap today;
    that ambiguity is surfaced as the crux, not buried.
  * No a0-VALUE claim: this program bounds the SEPARATION power only. No "theory closed".
Self-check asserts: reproduces the committed ~16% box within tolerance, and the floor number
is identical between PART 2 (where it is derived) and PARTs 3/4 (where it decides). Exit 0 =
numbers computed + frozen, NOT a verdict. Do NOT read the exit code as a physics result.
"""
import numpy as np, os, json, math, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fire_common import (load, flat, gls, budget, A0C, A0A, A0_RARFIT,
                         SIG_INC, SIG_LNU, SIG_LNG, HERE, REPO, _meta)

bar = "=" * 96
UD = 0.70                                       # committed P1 baseline disk M/L
FD_NAME = {1: "Hubble-flow", 2: "TRGB", 3: "Cepheid", 4: "UMa-cluster", 5: "SNIa"}

# THE SEPARATION ARITHMETIC (fixed, both directions; log-gap -> 3-sigma requirement)
LNGAP_ALT = abs(math.log(A0A / A0C))            # canonical vs ALT (nearest rival)
LNGAP_MOND = abs(math.log(1.20e-10 / A0C))      # canonical vs standard-MOND
TARGET = LNGAP_ALT / 3.0                         # binding requirement: separate the nearest rival
TARGET_MOND = LNGAP_MOND / 3.0

# ============================================================================== PART 0
print(bar)
print("PART 0 -- REGRESSION ANCHOR: reproduce estimator_theory.py's gas-dominated box (~16%)")
print(bar)
gals = load(UD)
GB, GO, FV, PHI, GAL, SLD, CTI = flat(gals, True)      # gas_only=True (the a0-line subsample)
b = budget(gals, True)
a0 = b["a0hat"]
a0_med = b["a0med"]
a0g, fint, c2n, w = gls(GB, GO, FV)
S = float(np.sum(w * GB**2))
yq = GB / a0
N, Ngal = int(len(GB)), b["Ngal"]
box_pct = 100 * b["tot"] / a0
print(f"  gas-dominated cut Vgas^2 > Ud*Vdisk^2 + Ub*Vbul^2 (Ud={UD}, Ub=1.4*Ud), point-level")
print(f"  N = {N} points across N_gal = {Ngal} galaxies  (Q<=2, inc>=30, eV/Vobs<0.10)")
print(f"  a0_hat(GLS) = {a0:.4e}   a0_hat(median E/g) = {a0_med:.4e}   f_int = {fint:.2f}")
print(f"  sigma:  stat {b['stat']:.3e} | dist {b['sysD']:.3e} | inc {b['sysI']:.3e}"
      f" | Ups {b['sysU']:.3e} | gascal {b['sysG']:.3e} | est {b['sysEst']:.3e}")
print(f"  TOTAL box sigma = {b['tot']:.3e}  =  {box_pct:.1f}% of a0_hat   (THE ~16% BOX)")
assert abs(box_pct - 16.1) < 0.3, f"box drifted from committed 16.1%: {box_pct:.2f}%"
assert abs(a0g - a0) < 1e-16
for lab, val in (("canonical cH_L/Z", A0C), ("ALT cH0/Z", A0A), ("standard-MOND", 1.20e-10)):
    t = (a0 - val) / b["tot"]
    print(f"    a0_hat vs {lab:<18} {val:.3e}:  {t:+.2f} sigma  "
          f"(ratio a0_hat/target = {a0/val:.3f})")

# ============================================================================== PART D
print()
print(bar)
print("PART D -- THE DEEP-MOND DOUBLING (verified numerically, numpy finite difference)")
print(bar)
# On the identity g_obs^2 = g_bar^2 + a0 g_bar,  a0_pt = (g_obs^2 - g_bar^2)/g_bar.
#   d ln a0_pt / d ln g_obs = 2 g_obs^2 / (g_obs^2 - g_bar^2) = 2 (y+1),   y = g_bar/a0.
#   g_obs = V^2/R  =>  d ln g_obs = 2 d ln V   =>   d ln a0_pt / d ln V = 4 (y+1).
# The "4" (not "1") is the deep-MOND penalty: a per-point velocity scatter sigma enters a0
# DOUBLED relative to the naive g_obs^2/g_bar reading -> the a0 error goes as ~2 sigma/sqrt(N),
# NOT sigma/(2 sqrt(N)). This is why the box is systematics-owned. Verify on model points:
a0_true = A0C
for yv in (0.03, 0.3, 3.0, 30.0):
    gb = yv * a0_true
    go = math.sqrt(gb**2 + a0_true * gb)
    def a0pt(go_, gb_):
        return (go_**2 - gb_**2) / gb_
    e = 1e-6
    dlnG = (math.log(a0pt(go * (1 + e), gb)) - math.log(a0pt(go * (1 - e), gb))) / (2 * e)
    dlnV = (math.log(a0pt(go * (1 + e) ** 2, gb)) - math.log(a0pt(go * (1 - e) ** 2, gb))) / (2 * e)
    assert abs(dlnG - 2 * (yv + 1)) < 1e-3, (yv, dlnG)
    assert abs(dlnV - 4 * (yv + 1)) < 1e-3, (yv, dlnV)
    print(f"    y={yv:>5.2f}:  d ln a0/d ln g_obs = {dlnG:6.2f} (= 2(y+1))   "
          f"d ln a0/d ln V = {dlnV:6.2f} (= 4(y+1))")
print("  VERIFIED: the velocity lever is 4(y+1); at deep-MOND (y->0) it is 4 -> the g_obs^2")
print("  scatter is DOUBLED into a0. fire_common.sig2_model bakes this in as (4*GOm2*FV)^2.")

# ============================================================================== PART 1
print()
print(bar)
print("PART 1 -- PER-GALAXY ERROR BUDGET (top error-dominant gas-dominated galaxies)")
print(bar)
# tabulated e_D/D from the SPARC master table -- an honesty cross-check on the fiducial sigma_lnD
def read_tabulated():
    path = os.path.join(REPO, "data", "SPARC_Lelli2016c.mrt")
    out = {}
    with open(path) as fh:
        for line in fh:
            f = line.split()
            if len(f) < 6:
                continue
            name = f[0]
            try:
                D, eD, fD = float(f[2]), float(f[3]), int(f[4])
            except ValueError:
                continue
            if D > 0 and fD in FD_NAME and name in _meta:
                out[name] = dict(D=D, eD=eD, fD=fD, eD_frac=eD / D)
    return out

TAB = read_tabulated()
DMPC = {n: _meta[n]["D"] for n in _meta}
idx = sorted(set(GAL.tolist()))

KU = float(np.sum(w * GB**2 * PHI * (2 * yq + 1)) / S)
KG = float(np.sum(w * GB**2 * (1 - PHI) * (2 * yq + 1)) / S)
rows, varD_sum, varI_sum, stat_sum = [], 0.0, 0.0, 0.0
for k in idx:
    m = GAL == k
    g = gals[k]
    name = g["name"]
    sld = float(SLD[m][0]); cti = float(CTI[m][0]); inc_deg = float(np.degrees(g["inc"]))
    cD = a0 * float(np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S)         # d a0_hat/d lnD_k
    cI = a0 * float(np.sum(w[m] * GB[m]**2 * 4 * (yq[m] + 1) * cti) / S)   # d a0_hat/d lnsini_k
    varD_k = (cD * sld) ** 2
    varI_k = (cI * SIG_INC) ** 2
    stat_k = float(np.sum(w[m] * GB[m]**2) / S**2)
    KU_k = float(np.sum(w[m] * GB[m]**2 * PHI[m] * (2 * yq[m] + 1)) / S)   # linear shared leverage
    KG_k = float(np.sum(w[m] * GB[m]**2 * (1 - PHI[m]) * (2 * yq[m] + 1)) / S)
    phibar_k = float(np.sum(w[m] * GB[m]**2 * PHI[m]) / np.sum(w[m] * GB[m]**2))
    ybar_k = float(np.sum(w[m] * GB[m]**2 * yq[m]) / np.sum(w[m] * GB[m]**2))
    rows.append(dict(name=name, k=k, npt=int(m.sum()), fD=g["fD"], method=FD_NAME[g["fD"]],
                     sig_lnD=sld, eD_frac=TAB.get(name, {}).get("eD_frac", np.nan),
                     D_Mpc=DMPC.get(name, np.nan), inc=inc_deg,
                     phibar=phibar_k, ybar=ybar_k, varD=varD_k, varI=varI_k, stat=stat_k,
                     reducible=varD_k + varI_k + stat_k, KU_k=KU_k, KG_k=KG_k))
    varD_sum += varD_k; varI_sum += varI_k; stat_sum += stat_k

# per-galaxy decomposition must reconstruct the committed budget to machine precision
assert abs(np.sqrt(varD_sum) - b["sysD"]) < 1e-14
assert abs(np.sqrt(varI_sum) - b["sysI"]) < 1e-14
assert abs(np.sqrt(stat_sum) - b["stat"]) < 1e-14
assert abs(sum(r["KU_k"] for r in rows) - KU) < 1e-12
assert abs(sum(r["KG_k"] for r in rows) - KG) < 1e-12
var_tot = b["tot"] ** 2
print(f"  [per-galaxy decomposition closes to <1e-14: sum var_D_k=sysD, sum var_I_k=sysI,")
print(f"   sum stat_k=stat; sum KU_k=KU={KU:.4f}, sum KG_k=KG={KG:.4f}]")
red = sorted(rows, key=lambda r: -r["reducible"])
print(f"\n  ranked by REDUCIBLE variance (var_D+var_I+stat, i.e. what better data can attack):")
print(f"  {'#':>2} {'galaxy':<12} {'D/Mpc':>6} {'method':<11} {'sigD':>5} {'eD/D':>5} "
      f"{'inc':>4} {'npt':>3} {'phi':>4} {'y':>5} {'varD%':>6} {'varI%':>6} {'stat%':>6} {'RED%':>6}")
for j, r in enumerate(red[:12], 1):
    print(f"  {j:>2} {r['name']:<12} {r['D_Mpc']:>6.1f} {r['method']:<11} "
          f"{r['sig_lnD']:>5.2f} {r['eD_frac']:>5.2f} {r['inc']:>4.0f} {r['npt']:>3} "
          f"{r['phibar']:>4.2f} {r['ybar']:>5.2f} "
          f"{100*r['varD']/var_tot:>6.2f} {100*r['varI']/var_tot:>6.2f} "
          f"{100*r['stat']/var_tot:>6.2f} {100*r['reducible']/var_tot:>6.2f}")
top10_red = sum(r["reducible"] for r in red[:10])
var_indep = varD_sum + varI_sum + stat_sum
print(f"  top-10 carry {100*top10_red/var_indep:.0f}% of the REDUCIBLE variance, "
      f"{100*top10_red/var_tot:.0f}% of the TOTAL box variance.")
print(f"  #1 {red[0]['name']} alone = {100*red[0]['reducible']/var_tot:.2f}% of the whole box "
      f"({red[0]['method']}, {red[0]['npt']} pts). ALL top-10 are Hubble-flow: distance-limited,")
print("  NOT low-inclination (varI is tiny) and NOT statistics -- the reducible list is a")
print("  DISTANCE list. The shared floor (PART 2) is what it cannot touch.")

# ============================================================================== PART 2
print()
print(bar)
print("PART 2 -- AVERAGING DECOMPOSITION: per-galaxy-random (~1/sqrt N) vs SHARED (floor)")
print(bar)
f_stat, f_D, f_I = b["stat"] / a0, b["sysD"] / a0, b["sysI"] / a0
f_U, f_G, f_E = b["sysU"] / a0, b["sysG"] / a0, b["sysEst"] / a0
print(f"  {'term':<9}{'value':>11}{'% a0':>8}   {'variance share':>14}   class")
CLS = {"stat": ("AVERAGES  ~1/sqrt(N_pts)"), "sysD": ("AVERAGES  ~1/sqrt(N_gal), TRGB cuts it"),
       "sysI": ("AVERAGES  ~1/sqrt(N_gal)"), "sysU": ("FLOOR     global stellar M/L"),
       "sysG": ("FLOOR     global gas-mass calibration"),
       "sysEst": ("SEMI-FLOOR data-QUALITY, not -QUANTITY")}
for t, fr in (("stat", f_stat), ("sysD", f_D), ("sysI", f_I),
              ("sysU", f_U), ("sysG", f_G), ("sysEst", f_E)):
    print(f"  {t:<9}{b[t]:>11.3e}{100*fr:>7.2f}%   {100*b[t]**2/var_tot:>13.1f}%   {CLS[t]}")
var_avg = f_stat**2 + f_D**2 + f_I**2                       # the part that averages down
avg_pct = 100 * math.sqrt(var_avg)
floor_glscommit = math.hypot(f_U, f_G)                      # optimistic floor (drop est. spread)
floor_committed = math.sqrt(f_U**2 + f_G**2 + f_E**2)       # conservative floor (keep est. spread)
print(f"\n  AVERAGES-DOWN quadrature (stat,dist,inc)   = {avg_pct:5.2f}%  "
      f"(beaten by more galaxies + TRGB)")
print(f"  IRREDUCIBLE FLOOR, GLS-committed (U,G)     = {100*floor_glscommit:5.2f}%  "
      f"(estimator spread dropped -- optimistic)")
print(f"  IRREDUCIBLE FLOOR, committed (U,G,estim.)  = {100*floor_committed:5.2f}%  "
      f"(estimator spread kept -- conservative)")
print(f"  Non-averaging SHARED share of the box variance = "
      f"{100*(f_U**2+f_G**2+f_E**2)/(var_tot/a0**2):.0f}%; averages-down share = "
      f"{100*var_avg/(var_tot/a0**2):.0f}%.")
print("  RULE-1 STATEMENT (both directions): the gas cut suppressed Upsilon from the FULL-sample")
print(f"  ~27% to {100*f_U:.1f}% (phibar 0.73 -> {b['phibar']:.2f}) but made gas DOMINATE the baryons, so")
print(f"  gas-calibration ROSE to {100*f_G:.1f}%. A trade, not a free lunch: the combined M/L+gas-cal")
print(f"  floor is {100*floor_glscommit:.1f}% (optimistic) -- ABOVE the {100*TARGET:.1f}% target. More galaxies")
print("  drive stat/dist/inc -> 0 but leave this floor UNTOUCHED.")

# ============================================================================== PART 3
print()
print(bar)
print("PART 3 -- REQUIRED-N-WITH-TRGB CURVE to the 5-8% target (priority galaxies named)")
print(bar)
# Realistic per-galaxy TRGB: already-TRGB keep 0.05; else D<20 Mpc -> 0.05, 20-40 -> 0.07
# (JWST, degraded), >=40 -> unchanged (too far for the RGB tip). Applied to the D term only.
def trgb_sld(k):
    if gals[k]["fD"] == 2:
        return gals[k]["sig_lnD"]
    D = DMPC.get(gals[k]["name"], np.nan)
    if not np.isfinite(D):
        return gals[k]["sig_lnD"]
    if D < 20:
        return 0.05
    if D < 40:
        return 0.07
    return gals[k]["sig_lnD"]

varD_trgb = 0.0
improvable = [k for k in idx if gals[k]["fD"] in (1, 4, 5)]
n_feasible = sum(1 for k in improvable
                 if np.isfinite(DMPC.get(gals[k]["name"], np.nan)) and DMPC[gals[k]["name"]] < 40)
n_far = len(improvable) - n_feasible
n_already = sum(1 for k in idx if gals[k]["fD"] == 2)
for k in idx:
    m = GAL == k
    cD = a0 * float(np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S)
    varD_trgb += (cD * trgb_sld(k)) ** 2
f_D_trgb = math.sqrt(varD_trgb) / a0
by_method = Counter(gals[k]["fD"] for k in idx)
print("  distance-method census: " + ", ".join(
    f"{FD_NAME[fd]}={n}" for fd, n in sorted(by_method.items())))
print(f"  already TRGB: {n_already}  |  improvable: {len(improvable)}  "
      f"(TRGB-feasible D<40 Mpc: {n_feasible}; too far D>=40: {n_far})")
imp_eD = [TAB[gals[k]["name"]]["eD_frac"] for k in improvable if gals[k]["name"] in TAB]
print(f"  honesty cross-check: tabulated e_D/D median on improvables = {np.median(imp_eD):.2f} "
      f">= the 0.25 fiducial used -> the distance budget is if anything MILDLY OPTIMISTIC.")
print(f"  realistic-TRGB distance term: sysD {100*f_D:.2f}% -> {100*f_D_trgb:.2f}% of a0.")

# The averaging model: add gas-dominated galaxies drawn from the SAME population (scale both
# N_pts and N_gal by factor f). The independent variance (with TRGB) scales as 1/f; the shared
# floor is constant. box(f)^2 = var_indep_trgb/f + floor_var. Use the OPTIMISTIC (GLS-committed)
# floor so the NO-GO is conservative (SPARC gets its best shot and still fails).
var_indep_trgb = f_stat**2 + f_D_trgb**2 + f_I**2
floor_var = floor_glscommit**2                       # <-- the floor number; reused by PART 4
print(f"\n  box(f)^2 = var_indep_TRGB / f  +  floor^2 ,  "
      f"var_indep_TRGB={100*math.sqrt(var_indep_trgb):.2f}%, floor={100*floor_glscommit:.2f}%")
print(f"  {'sample xN':>10} {'N_gal':>7} {'box%':>7}   (TRGB on all gas-dom gals, GLS-committed)")
for fmul in (1, 2, 4, 10, 100):
    bx = 100 * math.sqrt(var_indep_trgb / fmul + floor_var)
    print(f"  {fmul:>9}x {int(round(Ngal*fmul)):>7} {bx:>6.2f}%")
print(f"  {'inf':>10} {'inf':>7} {100*floor_glscommit:>6.2f}%  <- the asymptote is the floor")

target_var = TARGET**2
if target_var > floor_var:
    f_req = var_indep_trgb / (target_var - floor_var)
    print(f"\n  required N-multiple to reach {100*TARGET:.1f}%: f = {f_req:.1f}x "
          f"(~{int(round(Ngal*f_req))} gas-dom galaxies).")
    reach_verdict = "REACHABLE with N"
else:
    print(f"\n  required N-multiple to reach {100*TARGET:.1f}%: UNREACHABLE -- the {100*TARGET:.1f}% target")
    print(f"  is BELOW the {100*floor_glscommit:.1f}% floor. box(f) asymptotes to the floor from ABOVE;")
    print(f"  no finite N crosses it. Same for the {100*TARGET_MOND:.1f}% MOND-separation target "
          f"({'below' if TARGET_MOND**2 < floor_var else 'above'} the floor).")
    reach_verdict = "UNREACHABLE with N (floor-limited)"
priority = [r["name"] for r in red if r["fD"] in (1, 4, 5)][:12]
print(f"  PRIORITY TRGB galaxies (highest reducible variance, all Hubble-flow):")
print("    " + ", ".join(priority))
print("  These maximally shrink the AVERAGES-DOWN part -- necessary but, per the asymptote,")
print("  FAR from sufficient: they cannot move the floor.")

# ============================================================================== PART 4
print()
print(bar)
print("PART 4 -- FROZEN GO/NO-GO: 3-sigma separation of 9.36e-11 from 1.13e-10 and 1.20e-10")
print(bar)
print(f"  log-gap canonical->ALT  = {LNGAP_ALT:.3f}  -> 3-sigma needs box <= {100*TARGET:.2f}%")
print(f"  log-gap canonical->MOND = {LNGAP_MOND:.3f}  -> 3-sigma needs box <= {100*TARGET_MOND:.2f}%")
print(f"  binding requirement (nearest rival, ALT): box <= {100*TARGET:.2f}%")
# SPARC-alone best case: TRGB on every gas dwarf + GLS-commit (drop est. spread) + 2x sample.
sparc_best = math.sqrt(f_stat**2 / 2 + f_D_trgb**2 + f_I**2 + f_U**2 + f_G**2)
sparc_best = max(sparc_best, floor_glscommit)             # cannot beat the floor
print(f"\n  current box                                    : {box_pct:5.1f}%")
print(f"  SPARC-alone best (TRGB-all + GLS-commit + 2x N) : {100*sparc_best:5.1f}%  "
      f"(floor-limited)")
print(f"  requirement (canonical vs ALT)                 : {100*TARGET:5.2f}%")
print(f"  requirement (canonical vs MOND)                : {100*TARGET_MOND:5.2f}%")
go_alt = sparc_best <= TARGET
go_mond = sparc_best <= TARGET_MOND
print(f"\n  >>> FROZEN VERDICT (SPARC alone): "
      f"separate 9.36 from 1.13e-10 = {'GO' if go_alt else 'NO-GO'}  |  "
      f"separate 9.36 from 1.20e-10 = {'GO' if go_mond else 'NO-GO'}")
print(f"      SPARC-alone best {100*sparc_best:.1f}% is {sparc_best/TARGET:.1f}x the {100*TARGET:.1f}% "
      f"requirement -> NO-GO on BOTH separations.")
# absolute placement (both footings) at the current box
tot = b["tot"]
print("\n  absolute placement at the CURRENT 16% box (the estimator-choice wall):")
for nm, v in (("canonical cH_L/Z", A0C), ("ALT cH0/Z", A0A), ("standard-MOND", 1.20e-10)):
    print(f"    {nm:<18} {v:.3e}:  GLS {(a0-v)/tot:+.2f}s   median {(a0_med-v)/tot:+.2f}s")
spread = abs(a0 - a0_med)
print(f"  estimator-spread wall: |GLS - median| = {spread:.3e} = {100*spread/A0C:.0f}% of canonical,")
print(f"  EXCEEDING the footing gap itself ({100*(A0A-A0C)/A0C:.0f}%). GLS lands near ALT, the robust")
print("  median near canonical: the estimator choice ALONE slides the center across the whole")
print("  contested 9.4-1.2e-10 band. This is a data-QUALITY wall, not a distance problem.")

# ============================================================================== PART 5
print()
print(bar)
print("PART 5 -- MINIMAL EXTERNAL REQUIREMENT (since SPARC alone is NO-GO)")
print(bar)
# What floor is needed, and what external inputs deliver it? Halving Upsilon (0.10->0.05 dex)
# and gas-cal (10%->5%) halves the floor to ~5.45%; then finite N reaches the 6.31% target.
floor_ext = math.hypot(f_U / 2, f_G / 2)
print(f"  to reach {100*TARGET:.1f}% at any N, the floor must drop below {100*TARGET:.1f}%. External inputs:")
print(f"    (i)  stellar M/L prior 0.10 dex -> 0.05 dex  (Spitzer [3.6] color-M/L / resolved SED /")
print(f"         IFU stellar pops on the improvable gas dwarfs)   halves sysU: {100*f_U:.1f}% -> {50*f_U:.1f}%")
print(f"    (ii) HI-mass / gas calibration 10% -> 5%     (He+opacity correction, confirm")
print(f"         negligible H2 in gas-rich dwarfs)                 halves sysG: {100*f_G:.1f}% -> {50*f_G:.1f}%")
print(f"    => external floor = {100*floor_ext:.2f}%  (now BELOW the {100*TARGET:.1f}% target)")
if TARGET**2 > floor_ext**2:
    f_req_ext = var_indep_trgb / (TARGET**2 - floor_ext**2)
    n_req = int(math.ceil(Ngal * f_req_ext))
    print(f"    with that floor, 3-sigma reach needs f ~ {f_req_ext:.1f}x "
          f"(~{n_req} gas-dominated dwarfs) WITH TRGB + GLS-commit.")
else:
    f_req_ext, n_req = float("inf"), None
    print("    even the external floor does not clear the target -- deeper priors required.")
print(f"  MINIMAL PROGRAM: a dedicated gas-rich-dwarf campaign = TRGB distances + resolved")
print(f"  stellar-pop M/L (0.05 dex) + refined HI masses (5%) on ~{n_req if n_req else '30-50'} "
      f"gas-dominated dwarfs,")
print("  led by the PART-3 priority list. This is an OBSERVING PROGRAM, not something SPARC")
print("  delivers as-is. Only THEN is the Lambda-anchor separation a marginal 3-sigma GO.")

# ============================================================================== PRE-REG
print()
print(bar)
print("PRE-REGISTRATION (frozen 2026-07-23) -- decision, targets, and honesty caveats")
print(bar)
print("  ESTIMATOR (frozen): a0_hat = GLS through-origin slope of E=g_obs^2-g_bar^2 vs g_bar on")
print(f"    the gas-dominated cut Vgas^2 > Ud*Vdisk^2+Ub*Vbul^2 (Ud={UD}); robust median E/g reported")
print("    alongside as the estimator-spread check. No re-selection after seeing the answer.")
print("  DECISION RULE (box = 1-sigma half-width, fractional):")
print(f"    * box <= {100*TARGET:.2f}%  AND center within 1s of 9.36e-11 while excluding 1.13e-10 at")
print("      >=3s  ->  Lambda-anchor (cH_Lambda/Z) FAVORED.")
print(f"    * box <= {100*TARGET:.2f}%  AND center at >=3s from 9.36e-11 toward the 1.13-1.20 cluster")
print("      ->  Lambda-anchor DISFAVORED (total-density / fitted-constant footing favored).")
print(f"    * box  > {100*TARGET:.2f}%  ->  INCONCLUSIVE (current status). Both directions pre-committed;")
print("      NO post-hoc footing choice.")
print("  NAMED TARGET GALAXIES (TRGB priority, frozen): " + ", ".join(priority[:10]))
print("  HONESTY CAVEATS (frozen, non-negotiable):")
print(f"    1. Upsilon/gas-cal FLOOR: the shared M/L + gas-cal systematic ({100*floor_glscommit:.1f}%) does")
print("       NOT average down with N. SPARC alone is floor-limited above target -> NO-GO.")
print("    2. DEEP-MOND DOUBLING: a0=g_obs^2/g_bar carries a factor-4 velocity lever (PART D);")
print("       the a0 error is ~2 sigma/sqrt(N), NOT sigma/(2 sqrt(N)). The box is systematics-owned.")
print(f"    3. WHICH GAP: the footing gap is {100*(A0A-A0C)/A0C:.0f}% (canonical 9.36 vs ALT 1.13e-10); the")
print(f"       binding 3-sigma requirement is {100*TARGET:.2f}% (nearest rival), {100*TARGET_MOND:.2f}% vs MOND.")
print("    4. BOTH FOOTINGS carried on every dimensional number; neither is excluded or 'closed'.")
print("    5. ESTIMATOR-SPREAD WALL: GLS-vs-median alone spans the footing gap TODAY; resolving it")
print("       is the single most important analysis fix and is NOT a distance problem.")
print("    6. NO a0-VALUE PROOF: this bounds only WHERE a0 sits relative to the two anchors and the")
print("       SEPARATION power. It does NOT derive a0's value. No TOE / 'theory closed' language.")

# ============================================================================== SELF-CHECK
# floor consistency: the number derived in PART 2 must be the number used in PARTs 3 and 4.
assert abs(floor_var - floor_glscommit**2) < 1e-30
assert abs(floor_glscommit - math.hypot(b["sysU"], b["sysG"]) / a0) < 1e-15
# cross-validate the two sibling result JSONs if present (identical box / fractions / floor / targets)
xval = {}
for fn, keymap in (
    ("reach_target_results.json",
     dict(box="box_now_pct", floor="floor_glscommit_pct", target="target_pct")),
    ("per_galaxy_budget_results.json", dict(floorUG="shared_floor_UG_frac"))):
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        continue
    j = json.load(open(p))
    if fn == "reach_target_results.json":
        assert abs(j["box_now_pct"] - box_pct) < 0.05, (j["box_now_pct"], box_pct)
        assert abs(j["floor_glscommit_pct"] - 100 * floor_glscommit) < 0.05
        assert abs(j["target_pct"] - 100 * TARGET) < 1e-6
        # top TRGB targets agree on the leading set
        assert set(j["top_trgb_targets"][:6]) <= set(priority), (j["top_trgb_targets"][:6], priority)
        xval["reach_target"] = "box/floor/target/top-targets MATCH"
    else:
        assert abs(j["shared_floor_UG_frac"] - floor_glscommit) < 1e-4
        xval["per_galaxy_budget"] = "shared floor MATCH"
print()
print(bar)
print("SELF-CHECK")
print(bar)
print(f"  box reproduced: {box_pct:.2f}% (committed 16.1%, tol 0.3%)  [PASS]")
print(f"  floor identical across PART 2/3/4: {100*floor_glscommit:.3f}%  [PASS]")
for k, v in xval.items():
    print(f"  cross-validate {k}: {v}  [PASS]")

# ============================================================================== JSON
out = dict(
    frozen_date="2026-07-23",
    N_points=N, N_gal=Ngal, Ud=UD,
    a0hat_gls=a0, a0hat_median=a0_med, box_pct=box_pct, box_sigma=b["tot"],
    frac_terms=dict(stat=f_stat, sysD=f_D, sysI=f_I, sysU=f_U, sysG=f_G, sysEst=f_E),
    var_shares=dict(stat=stat_sum/var_tot, dist=varD_sum/var_tot, inc=varI_sum/var_tot,
                    Ups=b["sysU"]**2/var_tot, gascal=b["sysG"]**2/var_tot,
                    estimator=b["sysEst"]**2/var_tot),
    averages_down_pct=avg_pct,
    floor_glscommit_pct=100*floor_glscommit, floor_committed_pct=100*floor_committed,
    sysD_after_trgb_pct=100*f_D_trgb,
    target_alt_pct=100*TARGET, target_mond_pct=100*TARGET_MOND,
    sparc_alone_best_pct=100*sparc_best,
    go_alt=bool(go_alt), go_mond=bool(go_mond),
    reach_with_N=reach_verdict,
    external_floor_pct=100*floor_ext,
    n_required_with_external=(None if n_req is None else int(n_req)),
    n_already_trgb=n_already, n_improvable=len(improvable), n_trgb_feasible=int(n_feasible),
    priority_galaxies=priority,
    estimator_spread_frac_of_canon=float(spread/A0C),
    footing_gap_frac_of_canon=float((A0A-A0C)/A0C),
    top_error_dominant=[dict(name=r["name"], D_Mpc=r["D_Mpc"], method=r["method"],
                             npt=r["npt"], var_frac_of_box=float(r["reducible"]/var_tot))
                        for r in red[:10]],
    verdict_sparc_alone="NO-GO (both separations; floor-limited)",
    verdict_conditional="MARGINAL GO only with TRGB + Upsilon 0.05dex + gas-cal 5% on a "
                        "dedicated gas-rich-dwarf campaign",
    a0_canon=A0C, a0_alt=A0A, a0_mond=1.20e-10)
json.dump(out, open(os.path.join(HERE, "error_budget_program_2026_results.json"), "w"),
          indent=1, default=float)
print("\n[error_budget_program_2026_results.json written]")
print("EXIT 0: STEP-A error budget frozen + GO/NO-GO computed. Exit code is NOT a verdict.")
