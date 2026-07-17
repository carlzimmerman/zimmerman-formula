#!/usr/bin/env python3
"""
setup_mlpriors.py -- SETUP/DATA lane for the EXTERNAL-Upsilon-prior run on the a0-line.
=======================================================================================
GOAL of the run: the a0-line slope a0_hat := (g_obs^2 - g_bar^2)/g_bar is now
SYSTEMATICS-owned, and after the TRGB lever spent the distance budget, the two BINDING
lines are the stellar mass-to-light (Upsilon) prior sysU and the gas-mass calibration
sysG. This lane establishes, for the estimator lanes to consume:
  (1) the CURRENT Upsilon treatment in fire_common.budget (SIG_LNU=0.23 nat=0.0999 dex,
      GLOBAL/COHERENT -- verified here: it does NOT average down with N_gal);
  (2) what external per-galaxy Upsilon information is available (answer: NONE locally --
      SPARC ships a single fixed Upsilon at [3.6]; L36 is a luminosity, not an M/L; no
      per-galaxy colours or SPS M/L in the frozen repo) and the defensible literature
      decomposition to use in its place;
  (3) the DECOMPOSITION prior model -- coherent SPS/IMF zero-point floor (irreducible)
      + per-galaxy reducible part (shrinks with external colour/SPS M/L, averages 1/sqrt N)
      -- and how it injects into fire_common's budget algebra.

READ-ONLY on the frozen repo and on prep_2026/a0_line. Outputs ONLY to this directory.
Exit 0 = "setup computed + prior model handed off", NOT a verdict on the footing.

CREDITS: SPARC = Lelli-McGaugh-Schombert 2016 (AJ 152:157). M/L decomposition literature:
Schombert-McGaugh-Lelli 2019 (MNRAS 483:1496), McGaugh-Schombert 2014 (ApJ 802:18),
Meidt+2014 (ApJ 788:144), Bell-de Jong 2001 (ApJ 550:212). The [3.6] M/L is SPS-tight
(~0.1 dex total scatter, "nearly constant in the NIR"); a large share of that is a
COHERENT SPS/IMF zero-point that external per-galaxy colours CANNOT reduce.
Kernel credit: nu=sqrt(1+1/y) is Milgrom 1999 PLA 253:273 Eq.9; the framework's
distinctive content is the cH_Lambda/Z coefficient + the MI completion. a0 value and
s=-1 sign remain postulates regardless of anything measured here.
"""
import sys, os, json
import numpy as np

A0LINE = "/Users/carlzimmerman/new_physics/prep_2026/a0_line"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, A0LINE)
import fire_common as fc  # READ-ONLY import of the banked machinery

bar = "=" * 92
LN10 = np.log(10.0)
A0C, A0A = fc.A0C, fc.A0A                 # canonical 9.355e-11 / alt 1.1305e-10
DELTA = A0A - A0C
THRESH = abs(DELTA) / 2.0                 # sigma_tot needed to split footings at 2 sigma
out = {"a0_canon": A0C, "a0_alt": A0A, "delta": DELTA, "thresh_2sig": THRESH}


# ---------------------------------------------------------------------------- helpers
def budget_decomp(gals, gas_only, sig_coh_dex, sig_pg_dex):
    """fire_common.budget re-implemented with the Upsilon line SPLIT into a coherent
    SPS/IMF floor (global, does NOT average down) + a per-galaxy reducible part (RSS
    over galaxies, exactly like sysD -- averages ~1/sqrt(N_gal)). Everything else is
    byte-identical to fire_common.budget so the numbers are comparable line-for-line.

    sig_coh_dex : coherent SPS/IMF zero-point sigma in dex (irreducible)
    sig_pg_dex  : per-galaxy Upsilon sigma in dex AFTER external prior (residual);
                  pass the pre-prior value to see the un-reduced per-galaxy line.
    """
    GB, GO, FV, PHI, GAL, SLD, CTI = fc.flat(gals, gas_only)
    if len(GB) < 10:
        return None
    a0, fint, c2n, w = fc.gls(GB, GO, FV)
    med = float(np.median((GO**2 - GB**2) / GB))
    S = np.sum(w * GB**2)
    sig_stat = np.sqrt(1.0 / S)
    yq = GB / a0
    # per-galaxy D and inc (unchanged from fire_common)
    varD = varI = 0.0
    # per-galaxy Upsilon lever coefficient c_U,gal (RSS -> reducible part)
    varU_pg = 0.0
    cU_list = []
    sig_coh_nat = sig_coh_dex * LN10
    sig_pg_nat = sig_pg_dex * LN10
    for k in set(GAL.tolist()):
        m = GAL == k
        cD = a0 * np.sum(w[m] * GB[m] ** 2 * 2 * (yq[m] + 1)) / S
        cI = a0 * np.sum(w[m] * GB[m] ** 2 * 4 * (yq[m] + 1) * CTI[m]) / S
        varD += (cD * SLD[m][0]) ** 2
        varI += (cI * fc.SIG_INC) ** 2
        cU_gal = a0 * np.sum(w[m] * GB[m] ** 2 * PHI[m] * (2 * yq[m] + 1)) / S
        cU_list.append(cU_gal)
        varU_pg += (cU_gal * sig_pg_nat) ** 2
    cU = np.array(cU_list)
    # coherent Upsilon floor: the SAME KU as fire_common, x the coherent sigma only.
    KU = np.sum(w * GB**2 * PHI * (2 * yq + 1)) / S
    KG = np.sum(w * GB**2 * (1 - PHI) * (2 * yq + 1)) / S
    sU_coh = KU * a0 * sig_coh_nat            # global, does NOT average down
    sU_pg = np.sqrt(varU_pg)                   # per-galaxy, DOES average down
    sU_total = np.hypot(sU_coh, sU_pg)
    sG = KG * a0 * fc.SIG_LNG                   # gas-cal unchanged (coherent 0.10 dex)
    sEst = abs(a0 - med) / 2.0
    # reference: the banked fully-coherent sysU (0.0999 dex all-coherent) for comparison
    sU_banked = KU * a0 * fc.SIG_LNU
    tot = np.sqrt(sig_stat**2 + varD + varI + sU_total**2 + sG**2 + sEst**2)
    floor_UG = np.hypot(sU_total, sG)
    # coherence diagnostic: if the whole KU were independent-per-galaxy it would be
    # sqrt(sum cU^2)*sigma instead of (sum cU)*sigma; ratio ~ 1/sqrt(N_eff).
    coh_ratio = float(np.sqrt(np.sum(cU**2)) / np.sum(cU)) if np.sum(cU) > 0 else np.nan
    return dict(
        N=int(len(GB)), Ngal=int(len(set(GAL.tolist()))), a0hat=float(a0), a0med=med,
        stat=float(sig_stat), sysD=float(np.sqrt(varD)), sysI=float(np.sqrt(varI)),
        sysU_banked=float(sU_banked), sysU_coh=float(sU_coh), sysU_pg=float(sU_pg),
        sysU_total=float(sU_total), sysG=float(sG), sysEst=float(sEst), tot=float(tot),
        floor_UG=float(floor_UG), coh_ratio=coh_ratio, KU=float(KU), KG=float(KG),
        phibar=float(np.sum(w * GB**2 * PHI) / S), ybar=float(np.sum(w * GB**2 * yq) / S))


def tension(a0, sig, val):
    return (a0 - val) / sig


# ---------------------------------------------------------------------------- (1)
print(bar)
print("(1) CURRENT Upsilon TREATMENT in fire_common.budget -- verify COHERENT")
print(bar)
print(f"  SIG_LNU = {fc.SIG_LNU} nat = {fc.SIG_LNU/LN10:.4f} dex  (fiducial Upsilon_disk;")
print(f"  bulge = 1.4*Ud). Applied as sU = KU * a0 * SIG_LNU with KU summed over ALL")
print(f"  points -> ONE global number, i.e. FULLY COHERENT across galaxies.")
print(f"  gas-cal: SIG_LNG = {fc.SIG_LNG} dex-scale, also global/coherent.")
print(f"  footings: canonical a0 = {A0C:.4e} (cH_Lambda/Z) | alt {A0A:.4e} (cH0/Z);")
print(f"  gap |Delta| = {abs(DELTA):.3e} ({100*abs(DELTA)/A0C:.1f}%); to split at 2 sigma")
print(f"  need sigma_tot <= |Delta|/2 = {THRESH:.3e}.")
banked = {}
for Ud in (0.50, 0.70):
    b = fc.budget(fc.load(Ud), True)
    banked[Ud] = b
    print(f"\n  [banked fire_common] Ud={Ud}: N={b['N']} Ngal={b['Ngal']} a0={b['a0hat']:.4e}")
    print(f"    sysU={b['sysU']:.3e}  sysG={b['sysG']:.3e}  sysD={b['sysD']:.3e}"
          f"  sysEst={b['sysEst']:.3e}  stat={b['stat']:.3e}")
    print(f"    sqrt(sysU^2+sysG^2)={np.hypot(b['sysU'],b['sysG']):.3e}"
          f"  tot={b['tot']:.3e}  ({100*b['tot']/b['a0hat']:.1f}% of a0)")
out["banked"] = {str(k): {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv)
                          for kk, vv in v.items()} for k, v in banked.items()}

# demonstrate COHERENCE: decompose the SAME 0.0999 dex as if fully per-galaxy independent
print("\n  COHERENCE PROOF (Ud=0.70 gas-dom): apply the whole 0.0999 dex two ways --")
b_allcoh = budget_decomp(fc.load(0.70), True, fc.SIG_LNU/LN10, 0.0)
b_allpg = budget_decomp(fc.load(0.70), True, 0.0, fc.SIG_LNU/LN10)
print(f"    fully COHERENT  -> sysU = {b_allcoh['sysU_coh']:.3e}  (== banked {banked[0.70]['sysU']:.3e})")
print(f"    fully PER-GALAXY-> sysU = {b_allpg['sysU_pg']:.3e}  (averages down, ratio "
      f"{b_allpg['sysU_pg']/b_allcoh['sysU_coh']:.2f} ~ 1/sqrt(N_eff), N_gal={b_allpg['Ngal']})")
print("  => The banked treatment is the COHERENT (worst) case. The whole point of the")
print("     lever: the TRUE Upsilon error is part coherent (stuck) + part per-galaxy")
print("     (would already have averaged down, and shrinks further with external priors).")
out["coherence_proof"] = dict(fully_coherent=b_allcoh['sysU_coh'],
                              fully_pergalaxy=b_allpg['sysU_pg'],
                              ratio=float(b_allpg['sysU_pg']/b_allcoh['sysU_coh']),
                              Ngal=b_allpg['Ngal'])

# ---------------------------------------------------------------------------- (2)
print("\n" + bar)
print("(2) EXTERNAL per-galaxy Upsilon INFO -- data availability (HONEST)")
print(bar)
csv_cols = ["name", "T", "D_Mpc", "fD", "inc", "L36", "MHI", "Vflat", "Q", "ref"]
print(f"  sparc_master_clean.csv columns: {csv_cols}")
print("  -> L36 is the [3.6] LUMINOSITY (not an M/L); MHI is HI mass; NO per-galaxy")
print("     colours (no [3.6]-[4.5], no optical B-V), NO per-galaxy SPS M/L in the")
print("     frozen repo. The rotmod files carry SBdisk/SBbul (surface brightness) at a")
print("     single fixed Upsilon -- SPARC ships ONE M/L, not a per-galaxy vector.")
print("  -> SPARC_Lelli2016c.mrt (local) = same content (L[3.6], SBeff, Reff, MHI); still")
print("     NO colour / SPS M/L column.")
print("  CONCLUSION: external per-galaxy Upsilon (Schombert-McGaugh-Lelli 2019 SPS M/L,")
print("  or a Bell-de Jong colour-M/L) is NOT locally sourceable and was not fetched as a")
print("  per-galaxy vector. We therefore inject the DEFENSIBLE LITERATURE DECOMPOSITION")
print("  (below) as the prior model and flag it honestly, per the run's ground rules.")
print("  NIR CAVEAT (load-bearing): at [3.6] the M/L is 'nearly constant' (~0.1 dex TOTAL;")
print("  McGaugh-Schombert 2014, Meidt+2014, SML19), so the per-galaxy REDUCIBLE part is")
print("  intrinsically SMALL and a large share of the 0.1 dex is the COHERENT SPS/IMF")
print("  zero-point -- which external colours CANNOT reduce. The lever's ceiling is low.")
out["data_availability"] = dict(
    csv_columns=csv_cols, per_galaxy_color="none", per_galaxy_sps_ml="none",
    L36_is="luminosity_not_ML", sparc_ships="single_fixed_Upsilon_at_3.6um",
    external_source="literature_decomposition (SML19/MS14/Meidt14/BdJ01), not per-galaxy vector")

# ---------------------------------------------------------------------------- (3)
print("\n" + bar)
print("(3) DECOMPOSITION PRIOR MODEL  (dex; nat = dex*ln10)")
print(bar)
# Two defensible scenarios; both quadrature ~ the banked 0.0999 dex (calibration-preserving).
#   BALANCED (task-suggested): coherent 0.06 + per-galaxy 0.08 -> 0.100
#   NIR-REALISTIC (coherent-heavy, [3.6] M/L nearly constant): coherent 0.075 + pg 0.065 -> 0.099
# Residual per-galaxy AFTER an external colour/SPS M/L prior (Bell-de Jong at [3.6]):
#   sig_pg_res ~ 0.04 dex (colour-M/L relation precision; the reducible part shrinks to
#   this floor, not to zero) -- and it ALSO averages down over N_gal.
SCEN = {
    "balanced":       dict(coh=0.060, pg_pre=0.080, pg_res=0.040),
    "nir_realistic":  dict(coh=0.075, pg_pre=0.065, pg_res=0.035),
}
print("  sigma_coh = COHERENT SPS/IMF zero-point (IRREDUCIBLE; if the IMF/SPS zero-point")
print("    is off, every Upsilon shifts together). External per-galaxy colours do NOT")
print("    touch it. Cite: SML19, McGaugh-Schombert 2014, Meidt+2014.")
print("  sigma_pg  = PER-GALAXY reducible (SFH/metallicity-driven scatter about the")
print("    zero-point). External colour/SPS M/L shrinks pre->res AND it averages 1/sqrt(N).")
print("    Cite: Bell-de Jong 2001, SML19.")
print(f"  quadrature check: each scenario's sqrt(coh^2+pg_pre^2) ~= banked "
      f"{fc.SIG_LNU/LN10:.3f} dex (calibration-preserving).")
for nm, s in SCEN.items():
    q = np.hypot(s["coh"], s["pg_pre"])
    print(f"    {nm:14s}: coh={s['coh']:.3f}  pg_pre={s['pg_pre']:.3f}  pg_res={s['pg_res']:.3f}"
          f"  | quad(coh,pg_pre)={q:.3f} dex")

print("\n  INJECTION into the budget (see budget_decomp above):")
print("    coherent floor  sU_coh = KU * a0 * (sig_coh*ln10)          [global, stuck]")
print("    per-gal part    sU_pg  = sqrt( sum_gal (cU_gal * sig_pg*ln10)^2 )   [RSS, ~1/sqrt N]")
print("      cU_gal = a0 * sum_{pts in gal}( w * gb^2 * phi * (2y+1) ) / S")
print("      (identical algebra to fire_common's per-galaxy sysD loop; sum_gal cU_gal = KU*a0)")
print("    sysU_total = hypot(sU_coh, sU_pg);  everything else unchanged from fire_common.")

# ---- realize the residual floor the estimator lanes must beat, both scenarios/footings
print("\n" + bar)
print("  RESIDUAL FLOOR after applying external per-galaxy priors (pg -> pg_res):")
print(bar)
print(f"  target: sigma_tot <= |Delta|/2 = {THRESH:.3e} to split footings at 2 sigma\n")
res = {}
for Ud in (0.50, 0.70):
    res[str(Ud)] = {}
    for nm, s in SCEN.items():
        # BEFORE external prior (per-galaxy at pre value) and AFTER (per-galaxy at res value)
        b_pre = budget_decomp(fc.load(Ud), True, s["coh"], s["pg_pre"])
        b_post = budget_decomp(fc.load(Ud), True, s["coh"], s["pg_res"])
        res[str(Ud)][nm] = dict(pre=b_pre, post=b_post)
        print(f"  Ud={Ud} [{nm}] a0={b_post['a0hat']:.4e} N={b_post['N']} Ngal={b_post['Ngal']}")
        print(f"    sysU: banked(coherent0.10)={b_post['sysU_banked']:.3e}"
              f" -> coh_floor={b_post['sysU_coh']:.3e}"
              f" + pg_res={b_post['sysU_pg']:.3e} = {b_post['sysU_total']:.3e}")
        print(f"    sysG={b_post['sysG']:.3e}  sysEst={b_post['sysEst']:.3e}"
              f"  sysD={b_post['sysD']:.3e}  stat={b_post['stat']:.3e}")
        print(f"    floor sqrt(sysU^2+sysG^2): pre={np.hypot(b_pre['sysU_total'],b_pre['sysG']):.3e}"
              f" -> post={b_post['floor_UG']:.3e}   sigma_tot post={b_post['tot']:.3e}")
        crosses = b_post['tot'] < THRESH
        print(f"    tension: canon {tension(b_post['a0hat'],b_post['tot'],A0C):+.2f}s"
              f"  alt {tension(b_post['a0hat'],b_post['tot'],A0A):+.2f}s"
              f"  | sigma_tot<{THRESH:.2e}? {'YES-splits' if crosses else 'NO-still floored'}")
        print()
out["scenarios"] = SCEN
out["residual"] = res

# ---------------------------------------------------------------------------- summary
print(bar)
print("  HANDOFF to estimator lanes")
print(bar)
b07 = res["0.7"]["balanced"]["post"]
print("  * Upsilon in fire_common is COHERENT (proven): it is the worst case and does not")
print("    average down. The lever splits it into coh (stuck) + pg (already averaged).")
print("  * NO local per-galaxy colour/SPS M/L; use the literature decomposition:")
print("    coherent SPS/IMF floor 0.060-0.075 dex + per-galaxy 0.065-0.080 dex")
print("    (residual 0.035-0.040 dex after an external colour M/L). Quadrature preserves")
print("    the banked 0.0999 dex, so this only REDISTRIBUTES, never inflates, the budget.")
print("  * After the prior, sysU collapses toward the coherent floor; the binding line")
print("    becomes gas-cal sysG (~8.6e-12) alongside the coherent Upsilon floor.")
print(f"  * Representative (Ud=0.7, balanced, post-prior): sysU {banked[0.70]['sysU']:.2e}"
      f" -> {b07['sysU_total']:.2e}, floor(U,G) {np.hypot(banked[0.70]['sysU'],banked[0.70]['sysG']):.2e}"
      f" -> {b07['floor_UG']:.2e}, sigma_tot {banked[0.70]['tot']:.2e} -> {b07['tot']:.2e}"
      f" vs threshold {THRESH:.2e}.")
print("  * HONEST caveat to carry: per-point a0=E/g_bar DECLINES with g_bar (nu-shape")
print("    leaking into magnitude); sysEst stays a real line; do NOT read sysU collapse as")
print("    a footing detection. a0 value + s=-1 remain postulates.")

json.dump(out, open(os.path.join(HERE, "setup_mlpriors_results.json"), "w"),
          indent=1, default=float)
print("\n[setup_mlpriors_results.json written]")
print("EXIT 0: setup computed + prior model handed off. Exit code is not a verdict.")
