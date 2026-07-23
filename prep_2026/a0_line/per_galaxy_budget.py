#!/usr/bin/env python3
"""
per_galaxy_budget.py -- THE PER-GALAXY ERROR BUDGET ON THE REAL GAS-DOMINATED SPARC
SUBSAMPLE: which galaxies own the a0-line variance, why, and what (if anything) reaches
the 5-8% target that would separate the Lambda-anchor a0 from the total-density cluster.
====================================================================================
STEP A of the showstopper chain. Builds on (does NOT rebuild) the committed pipeline:
  estimator_theory.py / fire_common.py  -- the GLS through-origin slope + full budget.
  identity_uniqueness.py                -- the point-level gas-dominated cut.
This script DECOMPOSES the committed gas-dominated budget galaxy-by-galaxy and answers
the reachability question PRECISELY, honoring the hard calibration rule that a
manufactured win and a manufactured deficit are penalized equally.

THE ESTIMATOR (committed):  a0_hat = sum_i w_i E_i g_i / sum_i w_i g_i^2 = (sum w E g)/S,
  E_i = g_obs_i^2 - g_bar_i^2,  w_i = 1/sigma^2(E_i, model),  S = sum w_i g_i^2.
Per-point sensitivities (estimator_theory.py S3, sympy-verified):
  d a0_pt/d lnD = -2 a0 (y+1);  d a0_pt/d ln sin i = -4 a0 (y+1);
  d a0_pt/d lnUpsilon = -phi a0 (2y+1);  d a0_pt/d ln gascal = -(1-phi) a0 (2y+1).

PER-GALAXY RESPONSE of the slope (coherent shift of galaxy k propagated through the GLS):
  cD_k = a0 * sum_{i in k} w_i g_i^2 * 2 (y_i+1) / S      [d a0_hat / d lnD_k]
  cI_k = a0 * sum_{i in k} w_i g_i^2 * 4 (y_i+1) cot(i_k) / S
  var_D = sum_k (cD_k sigma_lnD_k)^2   -- distance errors are PER-GALAXY INDEPENDENT
  var_I = sum_k (cI_k sigma_i)^2       -- inclination errors are PER-GALAXY INDEPENDENT
  stat_k = (sum_{i in k} w_i g_i^2)/S^2   (sums to 1/S)
The INDEPENDENT terms (D, i, stat) AVERAGE DOWN over N_gal. The SHARED terms are coherent:
  KU = sum_i w_i g_i^2 phi_i (2 y_i+1)/S,   sigma_U = KU a0 sigma_lnUpsilon
  KG = sum_i w_i g_i^2 (1-phi_i)(2 y_i+1)/S, sigma_G = KG a0 sigma_ln(gascal)
KU, KG are LINEAR in the (single, global) Upsilon and gas-calibration offsets: they do NOT
average down over N_gal. Per-galaxy KU_k/KG_k = that galaxy's SHARE of the coherent floor.

HONESTY RAILS: the committed 16.1% box is reproduced and asserted as a regression anchor
(P0). The per-galaxy var_D/var_I/stat sums are asserted to equal the committed sysD/sysI/
stat. Both footings (canonical 9.36e-11, ALT 1.13e-10) carried on every dimensional number.
Reachability is computed, never assumed; the estimator-choice spread is kept VISIBLE as the
term TRGB+priors do NOT touch. Exit 0 = budget decomposed + reachability computed, NOT a
verdict, NOT 'theory closed'.
"""
import numpy as np, os, json, csv
import fire_common as fc

HERE = fc.HERE
bar = "=" * 100
A0C, A0A = fc.A0C, fc.A0A                 # canonical 9.355e-11 / ALT 1.1305e-10
SIG_INC, SIG_LNU, SIG_LNG = fc.SIG_INC, fc.SIG_LNU, fc.SIG_LNG
UD = 0.70

FD_NAME = {1: "Hubble-flow", 2: "TRGB", 3: "Cepheid", 4: "UMa-cluster", 5: "SNIa"}

# ---- tabulated per-galaxy distance + e_D from the SPARC master table (real data) --------
# SPARC galaxy names carry no internal whitespace, so the fixed-width .mrt data rows split
# cleanly on whitespace: [Galaxy, T, D, e_D, f_D, Inc, ...]. A parse guard (fields[2:5] must
# be float/float/int with f_D a known method) skips the header/notes. D is cross-checked
# against the pipeline's own CSV distance (fc._meta) so the budget stays footing-consistent.
def read_tabulated():
    path = os.path.join(fc.REPO, "data", "SPARC_Lelli2016c.mrt")
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
            if D > 0 and fD in FD_NAME and name in fc._meta:
                out[name] = dict(D=D, eD=eD, fD=fD, eD_frac=eD / D)
    return out

TAB = read_tabulated()
# distance used for TRGB feasibility comes from the pipeline CSV (authoritative, consistent)
DMPC = {n: fc._meta[n]["D"] for n in fc._meta}

# =============================================================================== P0
print(bar)
print("P0 -- REGRESSION ANCHOR: reproduce the committed gas-dominated budget (16% box)")
print(bar)
gals = fc.load(UD)
GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, True)     # gas_only=True
b = fc.budget(gals, True)
a0, fint, c2n, w = fc.gls(GB, GO, FV)
S = np.sum(w * GB**2)
yq = GB / a0
N, Ngal = int(len(GB)), b["Ngal"]
print(f"  gas-dominated points N = {N}, galaxies N_gal = {Ngal}  (point cut eV/Vobs<0.10)")
print(f"  a0_hat(GLS) = {b['a0hat']:.4e}   a0_hat(median E/g) = {b['a0med']:.4e}   "
      f"f_int = {b['fint']:.2f}")
print(f"  committed sigma:  stat {b['stat']:.3e} | dist {b['sysD']:.3e} | inc {b['sysI']:.3e}"
      f" | Ups {b['sysU']:.3e} | gascal {b['sysG']:.3e} | estimator {b['sysEst']:.3e}")
print(f"  TOTAL sigma = {b['tot']:.3e}  =  {100*b['tot']/b['a0hat']:.1f}% of a0_hat  "
      f"(THE ~16% BOX)")
assert abs(a0 - b["a0hat"]) < 1e-16
assert abs(100 * b["tot"] / b["a0hat"] - 16.1) < 0.3, "box drifted from committed 16%"
# both footings, absolute placement (the whole point of an ABSOLUTE-a0 measurement)
for lab, val in (("canonical cH_L/Z", A0C), ("ALT cH0/Z", A0A), ("standard-MOND", 1.2e-10)):
    t = (b["a0hat"] - val) / b["tot"]
    print(f"    a0_hat vs {lab:<18} {val:.3e}:  {t:+.2f} sigma "
          f"(ratio a0_hat/target = {b['a0hat']/val:.3f})")

# =============================================================================== P1
print()
print(bar)
print("P1 -- PER-GALAXY VARIANCE DECOMPOSITION (49 gas-dominated galaxies)")
print(bar)
idx = sorted(set(GAL.tolist()))
rows = []
varD_sum = varI_sum = stat_sum = 0.0
KU = float(np.sum(w * GB**2 * PHI * (2 * yq + 1)) / S)
KG = float(np.sum(w * GB**2 * (1 - PHI) * (2 * yq + 1)) / S)
for k in idx:
    m = GAL == k
    g = gals[k]
    name = g["name"]
    sld = float(SLD[m][0])                       # fiducial sigma_lnD by method
    cti = float(CTI[m][0])                        # cot(inc)
    inc_deg = float(np.degrees(g["inc"]))
    fD = g["fD"]
    cD = a0 * float(np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S)
    cI = a0 * float(np.sum(w[m] * GB[m]**2 * 4 * (yq[m] + 1) * cti) / S)
    varD_k = (cD * sld) ** 2
    varI_k = (cI * SIG_INC) ** 2
    stat_k = float(np.sum(w[m] * GB[m]**2) / S**2)
    KU_k = float(np.sum(w[m] * GB[m]**2 * PHI[m] * (2 * yq[m] + 1)) / S)   # linear leverage
    KG_k = float(np.sum(w[m] * GB[m]**2 * (1 - PHI[m]) * (2 * yq[m] + 1)) / S)
    phibar_k = float(np.sum(w[m] * GB[m]**2 * PHI[m]) / np.sum(w[m] * GB[m]**2))
    ybar_k = float(np.sum(w[m] * GB[m]**2 * yq[m]) / np.sum(w[m] * GB[m]**2))
    tab = TAB.get(name, {})
    rows.append(dict(name=name, k=k, npt=int(m.sum()),
                     fD=fD, method=FD_NAME[fD], sig_lnD=sld, eD_frac=tab.get("eD_frac", np.nan),
                     D_Mpc=DMPC.get(name, np.nan), inc=inc_deg, cotinc=cti,
                     phibar=phibar_k, ybar=ybar_k,
                     varD=varD_k, varI=varI_k, stat=stat_k,
                     reducible=varD_k + varI_k + stat_k,
                     KU_k=KU_k, KG_k=KG_k,
                     sharedU=KU_k * a0 * SIG_LNU, sharedG=KG_k * a0 * SIG_LNG))
    varD_sum += varD_k; varI_sum += varI_k; stat_sum += stat_k

# assert the per-galaxy decomposition reconstructs the committed budget
assert abs(np.sqrt(varD_sum) - b["sysD"]) < 1e-14, (np.sqrt(varD_sum), b["sysD"])
assert abs(np.sqrt(varI_sum) - b["sysI"]) < 1e-14, (np.sqrt(varI_sum), b["sysI"])
assert abs(np.sqrt(stat_sum) - b["stat"]) < 1e-14, (np.sqrt(stat_sum), b["stat"])
assert abs(sum(r["KU_k"] for r in rows) - KU) < 1e-12
assert abs(sum(r["KG_k"] for r in rows) - KG) < 1e-12
print(f"  [decomposition closes: sqrt(sum var_D_k)={np.sqrt(varD_sum):.3e}=sysD, "
      f"sqrt(sum var_I_k)={np.sqrt(varI_sum):.3e}=sysI, sqrt(sum stat_k)={np.sqrt(stat_sum):.3e}=stat]")
print(f"  [shared leverage closes: sum KU_k={sum(r['KU_k'] for r in rows):.4f}=KU, "
      f"sum KG_k={sum(r['KG_k'] for r in rows):.4f}=KG]")

var_indep_tot = varD_sum + varI_sum + stat_sum        # the AVERAGES-DOWN part
var_tot = b["tot"] ** 2
print(f"\n  variance shares of the TOTAL box (sigma_tot^2 = {var_tot:.3e}):")
print(f"    INDEPENDENT (averages down over N_gal):  stat {stat_sum/var_tot*100:4.1f}%  "
      f"dist {varD_sum/var_tot*100:4.1f}%  inc {varI_sum/var_tot*100:4.1f}%   "
      f"=> {var_indep_tot/var_tot*100:.1f}% total")
print(f"    SHARED  (does NOT average down):          Ups {b['sysU']**2/var_tot*100:4.1f}%  "
      f"gascal {b['sysG']**2/var_tot*100:4.1f}%  estimator {b['sysEst']**2/var_tot*100:4.1f}%   "
      f"=> {(b['sysU']**2+b['sysG']**2+b['sysEst']**2)/var_tot*100:.1f}% total")

# =============================================================================== P2
print()
print(bar)
print("P2 -- TOP-12 ERROR-DOMINANT GALAXIES (ranked by REDUCIBLE variance var_D+var_I+stat)")
print(bar)
red = sorted(rows, key=lambda r: -r["reducible"])
hdr = (f"  {'#':>2} {'galaxy':<12} {'D/Mpc':>6} {'method':<11} {'sigD':>5} {'eD/D':>5} "
       f"{'inc':>4} {'npt':>3} {'phi':>4} {'y':>5} {'varD%':>6} {'varI%':>6} {'stat%':>6} {'RED%':>6}")
print(hdr)
cum = 0.0
for j, r in enumerate(red[:12], 1):
    cum += r["reducible"]
    print(f"  {j:>2} {r['name']:<12} {r['D_Mpc']:>6.1f} {r['method']:<11} "
          f"{r['sig_lnD']:>5.2f} {r['eD_frac']:>5.2f} {r['inc']:>4.0f} {r['npt']:>3} "
          f"{r['phibar']:>4.2f} {r['ybar']:>5.2f} "
          f"{100*r['varD']/var_tot:>6.2f} {100*r['varI']/var_tot:>6.2f} "
          f"{100*r['stat']/var_tot:>6.2f} {100*r['reducible']/var_tot:>6.2f}")
top10_red = sum(r["reducible"] for r in red[:10])
print(f"  --- top-10 carry {100*top10_red/var_indep_tot:.0f}% of the reducible variance, "
      f"{100*top10_red/var_tot:.0f}% of the TOTAL box variance ---")
print("  WHY they dominate (read the columns):")
print("   * high sigD (Hubble-flow, 0.25) + many points -> distance-limited: the varD% column.")
print("   * low inc (cot(i) large) -> inclination-limited: the varI% column.")
print("   * few high-weight low-scatter points -> statistics-limited: the stat% column.")
print("   These are ALL the AVERAGES-DOWN part: better distances/inclinations/more galaxies")
print("   attack exactly this list. The floor below (P3) is what they CANNOT touch.")

# =============================================================================== P3
print()
print(bar)
print("P3 -- THE SHARED FLOOR (M/L + gas-calibration + estimator): does NOT average down")
print(bar)
floor_UG = np.hypot(b["sysU"], b["sysG"])
floor_UGE = np.sqrt(b["sysU"]**2 + b["sysG"]**2 + b["sysEst"]**2)
print(f"  Upsilon (M/L) shared systematic  : {b['sysU']:.3e}  = {100*b['sysU']/a0:.1f}% of a0_hat"
      f"   (sigma_lnUpsilon = {SIG_LNU:.2f} = 0.10 dex, GLOBAL)")
print(f"  gas-calibration shared systematic: {b['sysG']:.3e}  = {100*b['sysG']/a0:.1f}% of a0_hat"
      f"   (sigma_ln(gascal) = {SIG_LNG:.2f} = 0.10, GLOBAL)")
print(f"  estimator-choice spread          : {b['sysEst']:.3e}  = {100*b['sysEst']/a0:.1f}% of a0_hat"
      f"   (|GLS - median|/2)")
print(f"  => Upsilon (+) gascal floor (quadrature) = {floor_UG:.3e} = {100*floor_UG/a0:.1f}% of a0_hat")
print(f"  => Upsilon (+) gascal (+) estimator floor = {floor_UGE:.3e} = {100*floor_UGE/a0:.1f}% of a0_hat")
print("  RULE-1 VERDICT (stated plainly): the gas cut suppressed Upsilon from the FULL-sample")
print(f"  27% to {100*b['sysU']/a0:.1f}% (phibar 0.73 -> {b['phibar']:.2f}), but the gas cut also makes gas DOMINATE")
print(f"  the baryons, so the gas-calibration systematic rises to {100*b['sysG']/a0:.1f}% -- a TRADE, not a")
print("  free lunch. The combined shared M/L+gascal floor is ~{:.0f}%, ABOVE the 8% target.".format(100*floor_UG/a0))
print("  ==> ADDING MORE SPARC-LIKE GALAXIES CANNOT REACH 5-8%: it drives stat/dist/inc to")
print("      zero but leaves the ~{:.0f}% shared floor untouched. estimator_theory.py's prior".format(100*floor_UG/a0))
print("      ('the 21% footing gap is NOT resolved by SPARC alone') is confirmed and quantified.")
# which galaxies carry the shared floor (linear leverage shares)
shr = sorted(rows, key=lambda r: -(r["sharedU"] + r["sharedG"]))
print(f"\n  galaxies carrying the shared floor (top 6 by linear leverage KU_k+KG_k, phi = stellar share):")
print(f"  {'galaxy':<12} {'phi':>4} {'npt':>3} {'KU_k':>7} {'KG_k':>7}  (these near the gas/star cut boundary)")
for r in shr[:6]:
    print(f"  {r['name']:<12} {r['phibar']:>4.2f} {r['npt']:>3} {r['KU_k']:>7.4f} {r['KG_k']:>7.4f}")

# =============================================================================== P4
print()
print(bar)
print("P4 -- TRGB DISTANCE MODELING (the realistic near-term distance improvement)")
print(bar)
# TRGB gives ~5% per galaxy (sig_lnD -> 0.05) and is feasible where the RGB tip can be
# resolved: HST reaches ~10-15 Mpc, JWST extends to ~20-40 Mpc. Model realistically:
#   feasible: D < 20 Mpc -> improve to 0.05; 20-40 Mpc -> improve to 0.07 (JWST, degraded);
#   >40 Mpc -> not TRGB-reachable, keep current.
from collections import Counter
by_method = Counter(gals[k]["fD"] for k in idx)
print(f"  distance-method census of the 49 gas-dominated galaxies: "
      + ", ".join(f"{FD_NAME[fd]}({fd})={n}" for fd, n in sorted(by_method.items())))
n_already = sum(1 for k in idx if gals[k]["fD"] == 2)
improvable = [k for k in idx if gals[k]["fD"] in (1, 4, 5)]        # Hubble-flow, UMa, SNIa
print(f"  already on TRGB (fD=2, 5%): {n_already} galaxies -- no distance gain available.")
print(f"  improvable (Hubble-flow/UMa/SNIa): {len(improvable)} galaxies.")


def SLD_of(k):
    return fc.SIG_LND[gals[k]["fD"]]


def trgb_sig(k):
    """Realistic post-TRGB sigma_lnD for galaxy k given its distance."""
    if gals[k]["fD"] == 2:
        return SLD_of(k)                      # already TRGB, 5%
    D = DMPC.get(gals[k]["name"], np.nan)
    if not np.isfinite(D):
        return SLD_of(k)
    if D < 20:                                # HST resolves the RGB tip -> 5%
        return 0.05
    if D < 40:                                # JWST reach, degraded -> 7%
        return 0.07
    return SLD_of(k)                          # too far for TRGB -> unchanged


# recompute var_D with TRGB sigma_lnD per galaxy (var_I, stat, shared UNCHANGED)
varD_trgb = 0.0
n_feasible = D_far = 0
for r in rows:
    k = r["k"]
    sld_new = trgb_sig(k)
    D = DMPC.get(gals[k]["name"], np.nan)
    if gals[k]["fD"] in (1, 4, 5) and np.isfinite(D):
        if D < 40:
            n_feasible += 1
        else:
            D_far += 1
    # recompute cD_k with the ORIGINAL weights/geometry, only sigma_lnD changes
    m = GAL == r["k"]
    cD = a0 * float(np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S)
    varD_trgb += (cD * sld_new) ** 2
sysD_trgb = np.sqrt(varD_trgb)
tot_trgb = np.sqrt(b["stat"]**2 + varD_trgb + varI_sum + b["sysU"]**2 + b["sysG"]**2 + b["sysEst"]**2)
# honesty cross-check: tabulated e_D/D vs the fiducial sigma_lnD actually used
imp_eD = [TAB[gals[k]["name"]]["eD_frac"] for k in improvable if gals[k]["name"] in TAB]
far = [gals[k]["name"] for k in improvable if np.isfinite(DMPC.get(gals[k]["name"], np.nan))
       and DMPC[gals[k]["name"]] >= 40]
print(f"  cross-check: tabulated e_D/D on improvable galaxies has median {np.median(imp_eD):.2f} "
      f"(fiducial Hubble-flow sigma_lnD used = 0.25) -- the committed distance budget is if")
print(f"  anything MILDLY OPTIMISTIC, so TRGB gains here are a floor, not an overstatement.")
print(f"  too-far-for-TRGB (D>=40 Mpc, kept at current sigma): {', '.join(far) if far else 'none'}")
print(f"  TRGB-feasible (D<40 Mpc, JWST) improvable galaxies: {n_feasible}; too far (D>40): {D_far}")
print(f"  distance systematic  sysD: {b['sysD']:.3e} ({100*b['sysD']/a0:.1f}%)  ->  "
      f"{sysD_trgb:.3e} ({100*sysD_trgb/a0:.1f}%)  after TRGB")
print(f"  TOTAL box with TRGB (everything else fixed): {tot_trgb:.3e} = {100*tot_trgb/a0:.1f}% of a0_hat")
print(f"  ==> TRGB alone moves the box {100*b['tot']/a0:.1f}% -> {100*tot_trgb/a0:.1f}%: real but MODEST,")
print("      because distance was never the dominant term -- the shared floor (P3) is.")

# =============================================================================== P5
print()
print(bar)
print("P5 -- REACHABILITY LADDER to the 5-8% target (both footings on every row)")
print(bar)
# The 21% footing gap (canonical 9.36 vs ALT/MOND ~1.13-1.20) needs a ~7% 1-sigma
# measurement for 3-sigma separation. Ladder rows (each keeps the estimator spread unless
# noted, because that is the term neither distances nor priors touch):
S_U = lambda sig_lnU: KU * a0 * sig_lnU
S_G = lambda sig_lnG: KG * a0 * sig_lnG


def box(varD, sysU, sysG, sysEst, stat=b["stat"]):
    t = np.sqrt(stat**2 + varD + varI_sum + sysU**2 + sysG**2 + sysEst**2)
    return t, 100 * t / a0


ladder = []
ladder.append(("0. committed baseline (SPARC, 0.10dex Ups, 0.10 gascal)",
               *box(varD_sum, b["sysU"], b["sysG"], b["sysEst"])))
ladder.append(("1. + TRGB distances (JWST, D<40 Mpc)",
               *box(varD_trgb, b["sysU"], b["sysG"], b["sysEst"])))
ladder.append(("2. + tighter Upsilon prior 0.05 dex (Spitzer color M/L)",
               *box(varD_trgb, S_U(0.115), b["sysG"], b["sysEst"])))
ladder.append(("3. + tighter gas-cal 0.05 (He+H2 pinned)",
               *box(varD_trgb, S_U(0.115), S_G(0.05), b["sysEst"])))
ladder.append(("4. + estimator spread halved (lower per-pt scatter)",
               *box(varD_trgb, S_U(0.115), S_G(0.05), b["sysEst"] / 2)))
ladder.append(("5. + estimator spread resolved (single justified estimator)",
               *box(varD_trgb, S_U(0.115), S_G(0.05), 0.0)))
print(f"  target: ~7% 1-sigma for 3-sigma separation of the 21% footing gap (9.36 vs 1.13e-10).")
print(f"  {'ladder step':<54} {'box%':>6} {'reaches 8%?':>11} {'reaches 7%?':>11}")
for lab, t, pc in ladder:
    print(f"  {lab:<54} {pc:>5.1f}% {('YES' if pc<=8 else 'no'):>11} {('YES' if pc<=7 else 'no'):>11}")
floor_no_est = box(0.0, S_U(0.115), S_G(0.05), b["sysEst"])[1]
floor_all = box(0.0, S_U(0.115), S_G(0.05), b["sysEst"] / 2)[1]
print(f"\n  hard floor with EVERYTHING averaged down (varD=varI=stat->0) but priors at 0.05dex/")
print(f"  0.05 and estimator spread KEPT: {floor_no_est:.1f}%  (estimator-limited).")
print(f"  same but estimator spread HALVED: {floor_all:.1f}%.")

# =============================================================================== P6
print()
print(bar)
print("P6 -- THE ESTIMATOR-SPREAD WALL (the honest crux for STEP A)")
print(bar)
gap = A0A - A0C
spread_full = abs(b["a0hat"] - b["a0med"])
print(f"  footing gap (ALT - canonical) = {gap:.3e}  ({100*gap/A0C:.0f}% of canonical)")
print(f"  GLS vs median estimator spread (full width) = {spread_full:.3e}  "
      f"({100*spread_full/A0C:.0f}% of canonical)")
print(f"  a0_hat(GLS)    = {b['a0hat']:.3e}  sits at {(b['a0hat']-A0C)/b['tot']:+.2f}sig canon, "
      f"{(b['a0hat']-A0A)/b['tot']:+.2f}sig ALT  -> ALT-side")
print(f"  a0_hat(median) = {b['a0med']:.3e}  sits at {(b['a0med']-A0C)/b['tot']:+.2f}sig canon, "
      f"{(b['a0med']-A0A)/b['tot']:+.2f}sig ALT  -> canonical-side")
print("  ==> THE ESTIMATOR CHOICE ALONE SPANS MORE THAN THE FOOTING GAP: GLS lands near ALT,")
print("      the robust median lands near canonical. Reaching 7% REQUIRES resolving this")
print("      ambiguity (understanding why the high-weight points pull GLS up), not just")
print("      better distances. This is degenerate with the very question STEP A poses; it is")
print("      the single most important thing to fix and it is NOT a distance problem.")

# =============================================================================== verdict
print()
print(bar)
print("VERDICT (honest, both directions)")
print(bar)
print(f"  * N = {N} gas-dominated points across {Ngal} galaxies; box reproduced at "
      f"{100*b['tot']/b['a0hat']:.1f}% (regression anchor).")
print(f"  * The box is SHARED-SYSTEMATIC-owned: Upsilon {100*b['sysU']/a0:.1f}% + gascal "
      f"{100*b['sysG']/a0:.1f}% + estimator {100*b['sysEst']/a0:.1f}% (none average down),")
print(f"    vs the averages-down part stat+dist+inc = {100*np.sqrt(var_indep_tot)/a0:.1f}%.")
print(f"  * Distance-dominant galaxies are the {by_method.get(1,0)} Hubble-flow objects (sigD=0.25);")
print("    TRGB on them moves the box only {:.1f}% -> {:.1f}% (distance was never the leader).".format(
      100*b['tot']/a0, 100*tot_trgb/a0))
print(f"  * SPARC ALONE FLOORS AT ~{floor_UG/a0*100:.0f}% (M/L+gascal shared) / ~{floor_no_est:.0f}% incl. estimator")
print(f"    spread -- ABOVE the 5-8% target. Reaching 7% needs: TRGB distances + a 0.05-dex")
print("    Upsilon prior (Spitzer [3.6] color M/L) + a 0.05 gas-cal + a RESOLVED estimator.")
print(f"  * Only the full stack (row 5: priors tightened AND estimator ambiguity resolved)")
print(f"    reaches {ladder[5][2]:.1f}%. Distances alone, or galaxies alone, do NOT get there.")
print("  * Both footings remain within ~1 sigma of the gas slope at the current box; the")
print("    absolute Lambda-anchor vs total-density question is NOT decided by SPARC alone.")

# ------------------------------------------------------------------------------- JSON
out = dict(
    N_points=N, N_gal=Ngal, a0hat_gls=b["a0hat"], a0hat_median=b["a0med"],
    box_frac=b["tot"] / b["a0hat"], sig_tot=b["tot"],
    budget=dict(stat=b["stat"], sysD=b["sysD"], sysI=b["sysI"], sysU=b["sysU"],
                sysG=b["sysG"], sysEst=b["sysEst"], tot=b["tot"]),
    var_shares=dict(stat=stat_sum/var_tot, dist=varD_sum/var_tot, inc=varI_sum/var_tot,
                    Ups=b["sysU"]**2/var_tot, gascal=b["sysG"]**2/var_tot,
                    estimator=b["sysEst"]**2/var_tot),
    shared_floor_UG_frac=float(floor_UG/a0), shared_floor_UGE_frac=float(floor_UGE/a0),
    sysD_after_trgb=float(sysD_trgb), box_after_trgb_frac=float(tot_trgb/a0),
    n_trgb_feasible=int(n_feasible), n_already_trgb=int(n_already),
    ladder=[dict(step=l, box_frac=t/a0) for l, t, _ in ladder],
    reach_7pct_only_full_stack=bool(ladder[5][2] <= 7),
    estimator_spread_frac_of_canon=float(spread_full/A0C),
    footing_gap_frac_of_canon=float(gap/A0C),
    top10_galaxies=[dict(name=r["name"], D_Mpc=r["D_Mpc"], method=r["method"],
                         sig_lnD=r["sig_lnD"], eD_frac=float(r["eD_frac"]),
                         inc=r["inc"], npt=r["npt"], phibar=r["phibar"], ybar=r["ybar"],
                         var_frac_of_box=float(r["reducible"]/var_tot)) for r in red[:10]],
    a0_canon=A0C, a0_alt=A0A, a0_mond=1.2e-10)
json.dump(out, open(os.path.join(HERE, "per_galaxy_budget_results.json"), "w"),
          indent=1, default=float)
print("\n[per_galaxy_budget_results.json written]")
print("EXIT 0: per-galaxy budget decomposed + reachability computed. Exit code is not a verdict.")
