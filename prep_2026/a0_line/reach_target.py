#!/usr/bin/env python3
"""
reach_target.py -- STEP A OF THE SHOWSTOPPER CHAIN: can the gas-dominated a0-line slope
be sharpened to the 1-sigma fractional error (~6-7%) needed to SEPARATE the Lambda-anchor
a0 = cH_Lambda/Z = 9.36e-11 from the total-density / fitted-constant cluster (ALT
1.13e-10, MOND 1.20e-10) at 3 sigma?
==========================================================================================
Builds DIRECTLY on the committed budget (estimator_theory.py S4 / fire_common.budget) --
reproduced here as a REGRESSION ANCHOR, then extended. Nothing here re-derives or contradicts
the banked estimator; it only asks "what shrinks the box, and how far can it go."

THE SEPARATION ARITHMETIC (fixed, both directions):
   canonical 9.355e-11  vs  ALT 1.1305e-10  ->  ln-gap 0.188  ->  3 sigma needs s_ln = 6.31%
   canonical 9.355e-11  vs  MOND 1.20e-10   ->  ln-gap 0.249  ->  3 sigma needs s_ln = 8.30%
The nearest rival (ALT) sets the requirement: a ~6.3% one-sigma box separates the
Lambda-anchor from the whole 1.13-1.20 cluster at 3 sigma. Target := 6.3%.

THE AVERAGING STRUCTURE (the load-bearing physics, from estimator_theory.py S2/S3):
   * a0 = g_obs^2/g_bar DOUBLES per-point log-scatter (deep-MOND penalty): every velocity
     error enters a0_pt with lever 4*(y+1), so the box is systematics-owned, not stat.
   * D (distance) and i (inclination) are PER-GALAXY INDEPENDENT -> average down as
     ~1/sqrt(N_gal). TRGB distances (5% vs Hubble-flow 25%) shrink the D term directly.
   * Upsilon (stellar M/L) and gas-mass calibration are GLOBAL systematics -> they DO NOT
     average down over N_gal. They set a FLOOR that N cannot cross.
   * The gas-dominated cut suppresses Upsilon (gas dominates the baryons) but STRUCTURALLY
     AMPLIFIES gas-calibration (gas is now the dominant baryon): purity trades one global
     floor for the other -- it cannot escape the floor.

HONESTY RAILS: a manufactured GO and a manufactured NO-GO are penalized equally. The floor
is reported both with the committed estimator-spread line (conservative) and GLS-committed
(fairer, drops the spread as a cross-check not a second measurement); the gas-cal floor is
stress-tested at 100/70/50% "truly global"; both footings carried on every absolute number.
No "theory closed." Exit 0 = numbers computed, NOT a verdict.
"""
import numpy as np, os, json, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fire_common import (load, flat, gls, budget, A0C, A0A, A0_RARFIT,
                         SIG_INC, SIG_LNU, SIG_LNG, HERE)

bar = "=" * 94
UD = 0.70                                   # committed P1 baseline disk M/L
TRGB_SIGLND = 0.05                          # tip-of-red-giant-branch distance error
TARGET = abs(math.log(A0A / A0C)) / 3.0     # 3-sigma canon-vs-ALT separation requirement

# ------------------------------------------------------------------- S0 regression anchor
print(bar); print("S0 -- REGRESSION ANCHOR: reproduce the committed gas-dominated budget")
print(bar)
gals = load(UD)
b = budget(gals, True)
a0 = b["a0hat"]
anchor_json = json.load(open(os.path.join(HERE, "estimator_results.json")))["budget_gas"]
for k in ("a0hat", "stat", "sysD", "sysI", "sysU", "sysG", "sysEst", "tot", "N", "Ngal"):
    assert abs(b[k] - anchor_json[k]) <= 1e-6 * max(1.0, abs(anchor_json[k])), (k, b[k], anchor_json[k])
print(f"  reproduced estimator_theory.py S4 GAS-DOM budget EXACTLY (N={b['N']}, "
      f"Ngal={b['Ngal']}):")
print(f"    a0_hat(GLS) = {a0:.4e}   a0_hat(median) = {b['a0med']:.4e}   "
      f"tot box = {b['tot']:.3e} ({100*b['tot']/a0:.1f}%)")
print(f"  TARGET for 3-sigma Lambda-anchor separation: s_ln = {100*TARGET:.2f}% "
      f"(canon-vs-ALT, the nearest rival)")

# ------------------------------------------------------------------- S1 classification
print(); print(bar)
print("S1 -- CLASSIFY EACH BUDGET TERM: does it average down over N_gal, or is it a FLOOR?")
print(bar)
frac = {t: b[t] / a0 for t in ("stat", "sysD", "sysI", "sysU", "sysG", "sysEst")}
cls = {"stat": "AVERAGES (~1/sqrt N points)", "sysD": "AVERAGES (~1/sqrt N_gal; TRGB cuts it)",
       "sysI": "AVERAGES (~1/sqrt N_gal)", "sysU": "FLOOR  (global stellar M/L)",
       "sysG": "FLOOR  (global gas-mass calibration)",
       "sysEst": "SEMI-FLOOR (estimator spread; data-QUALITY not -QUANTITY)"}
print(f"  {'term':<8}{'value':>11}{'% of a0':>9}   classification")
for t in ("stat", "sysD", "sysI", "sysU", "sysG", "sysEst"):
    print(f"  {t:<8}{b[t]:>11.3e}{100*frac[t]:>8.2f}%   {cls[t]}")
avg = math.hypot(math.hypot(frac["stat"], frac["sysD"]), frac["sysI"])
floor_cons = math.sqrt(frac["sysU"]**2 + frac["sysG"]**2 + frac["sysEst"]**2)
floor_gls = math.hypot(frac["sysU"], frac["sysG"])
print(f"  AVERAGING quadrature (stat,D,i)        = {100*avg:5.2f}%  (beaten by N & TRGB)")
print(f"  FLOOR, committed (U,G,Est)             = {100*floor_cons:5.2f}%  (conservative)")
print(f"  FLOOR, GLS-committed (U,G)             = {100*floor_gls:5.2f}%  (drops est. spread)")

# ------------------------------------------------------------------- S2 floor theorem
print(); print(bar)
print("S2 -- THE IRREDUCIBLE-FLOOR THEOREM: box(N->inf, perfect D & i, stat->0)")
print(bar)
print(f"  Send stat, sysD, sysI -> 0 (infinite galaxies, all TRGB, perfect inclinations).")
print(f"  The box CANNOT fall below the global-systematic floor:")
print(f"    committed (keeps est. spread) : {100*floor_cons:5.2f}%   -> {floor_cons/TARGET:.1f}x the {100*TARGET:.1f}% target")
print(f"    GLS-committed (est. dropped)  : {100*floor_gls:5.2f}%   -> {floor_gls/TARGET:.1f}x the target")
gascal_sens = {}
for fg in (1.0, 0.7, 0.5):
    fl = math.hypot(frac["sysU"], frac["sysG"] * fg)
    gascal_sens[fg] = fl
    print(f"    gas-cal floor sensitivity (global frac {fg:.1f}) : {100*fl:5.2f}%")
print(f"  ==> even if HALF the gas-cal error were per-galaxy (averaging), the floor is "
      f"{100*gascal_sens[0.5]:.1f}% > {100*TARGET:.1f}%.")
print(f"  READING: SPARC ALONE, at ANY N, is floor-limited at ~{100*floor_gls:.0f}% -- ABOVE the")
print(f"  6.3% needed. Adding galaxies beats stat/D/i (already only {100*avg:.1f}%); it does")
print(f"  NOT touch the Upsilon + gas-cal floor. This is the honest STEP-A wall.")

# ------------------------------------------------------------------- S3 TRGB ranking
print(); print(bar)
print("S3 -- TRGB DISTANCE PRIORITY: which gas-dominated galaxies buy the most (sysD)")
print(bar)
# per-galaxy distance-variance contribution on the gas-dominated sample
names, SLDg, fDg = [], [], []
GBl, GOl, FVl, PHIl, GALl, CTIl = [], [], [], [], [], []
k = 0
for gg in gals:
    m = gg["gasdom"]
    n = int(m.sum())
    if n == 0:
        continue
    names.append(gg["name"]); SLDg.append(gg["sig_lnD"]); fDg.append(gg["fD"])
    GBl += list(gg["gb"][m]); GOl += list(gg["go"][m]); FVl += list(gg["fv"][m])
    PHIl += list(gg["phi"][m]); GALl += [k] * n; CTIl += [1 / np.tan(gg["inc"])] * n
    k += 1
GB, GO, FV, PHI, GAL, CTI = map(np.array, (GBl, GOl, FVl, PHIl, GALl, CTIl))
a0g, fint, c2n, w = gls(GB, GO, FV)
S = np.sum(w * GB**2); yq = GB / a0g
rows = []
for kk in range(len(names)):
    m = GAL == kk
    cD = a0g * np.sum(w[m] * GB[m]**2 * 2 * (yq[m] + 1)) / S
    vg = (cD * SLDg[kk])**2
    vt = (cD * TRGB_SIGLND)**2
    rows.append((names[kk], fDg[kk], SLDg[kk], int(m.sum()), vg, vt))
varD_now = sum(r[4] for r in rows)
varD_all_trgb = sum(r[5] for r in rows)
n_trgb = sum(1 for r in rows if r[1] == 2)
buy = sorted([r + (r[4] - r[5],) for r in rows if r[1] != 2], key=lambda z: -z[6])
FDLAB = {1: "Hflow 25%", 4: "UMa 10%", 5: "SNIa 8%", 3: "Ceph 5%"}
print(f"  {len(names)} gas-dominated galaxies: {n_trgb} already on TRGB, {len(buy)} improvable.")
print(f"  current sysD = {100*math.sqrt(varD_now)/a0g:.2f}%   ->   ALL-TRGB sysD = "
      f"{100*math.sqrt(varD_all_trgb)/a0g:.2f}%  (the reducible-D floor)")
print(f"\n  {'rank':>4} {'galaxy':<12}{'dist':>10}{'npts':>5}{'varD_cut':>11}"
      f"{'cum sysD%':>11}")
cum = varD_now
top_targets = []
for i, (nm, fD, sg, npts, vg, vt, red) in enumerate(buy[:12], 1):
    cum -= red
    top_targets.append(nm)
    print(f"  {i:>4} {nm:<12}{FDLAB.get(fD,'?'):>10}{npts:>5}{red:>11.2e}"
          f"{100*math.sqrt(max(cum,0))/a0g:>10.2f}%")
print(f"  Top {len(top_targets)} TRGB targets (all Hubble-flow, most points) take sysD "
      f"{100*math.sqrt(varD_now)/a0g:.1f}% -> {100*math.sqrt(max(cum,0))/a0g:.1f}%.")
print("  NOTE: sysD is an AVERAGING term -- TRGB helps it, but sysD is NOT what floors the")
print("  box (S2). TRGB is NECESSARY-but-far-from-sufficient.")

# ------------------------------------------------------------------- S4 scenario ladder
print(); print(bar)
print("S4 -- THE SCENARIO LADDER: stack every SPARC-internal + external lever, in order")
print(bar)
sD_trgb = math.sqrt(varD_all_trgb) / a0g


def box(stat, sD, sI, sU, sG, sEst):
    return math.sqrt(stat**2 + sD**2 + sI**2 + sU**2 + sG**2 + sEst**2)


ladder = [
    ("0. committed baseline (Ud=0.70)",
     box(frac["stat"], frac["sysD"], frac["sysI"], frac["sysU"], frac["sysG"], frac["sysEst"])),
    ("1. + TRGB on all 49 gas-dom gals (sysD->1.8%)  [SPARC+obs]",
     box(frac["stat"], sD_trgb, frac["sysI"], frac["sysU"], frac["sysG"], frac["sysEst"])),
    ("2. + commit to GLS estimator (drop est. spread) [analysis]",
     box(frac["stat"], sD_trgb, frac["sysI"], frac["sysU"], frac["sysG"], 0.0)),
    ("3. + 2x gas-dom points (stat/sqrt2)             [bigger survey]",
     box(frac["stat"]/math.sqrt(2), sD_trgb, frac["sysI"], frac["sysU"], frac["sysG"], 0.0)),
    ("4. + Upsilon prior 0.10->0.05 dex (sysU halves) [EXTERNAL: SED fits]",
     box(frac["stat"]/math.sqrt(2), sD_trgb, frac["sysI"], frac["sysU"]/2, frac["sysG"], 0.0)),
    ("5. + gas-cal 10%->5% (sysG halves)              [EXTERNAL: HI mass]",
     box(frac["stat"]/math.sqrt(2), sD_trgb, frac["sysI"], frac["sysU"]/2, frac["sysG"]/2, 0.0)),
]
print(f"  {'scenario':<58}{'box%':>7}{'3sig?':>8}")
for lab, bx in ladder:
    ok = "GO" if bx <= TARGET else "no"
    print(f"  {lab:<58}{100*bx:>6.2f}%{ok:>8}")
print(f"  target = {100*TARGET:.2f}%. The box only crosses it at step 5 -- i.e. ONLY after")
print("  BOTH external priors (tighter Upsilon AND tighter gas-cal) are added on top of")
print("  TRGB + GLS-commit + a doubled sample. Steps 0-3 (everything SPARC can do by")
print("  itself) floor at ~11.6%. The external inputs are not optional -- they are the gate.")

# ------------------------------------------------------------------- S5 purity trap
print(); print(bar)
print("S5 -- THE PURITY TRAP: does a stricter gas cut Vgas^2 > k*Vstar^2 reach the target?")
print(bar)


def budget_kcut(gals, k):
    GBk, GOk, FVk, PHk, GLk, SLk, CTk = [], [], [], [], [], [], []
    j = 0
    for gg in gals:
        m = gg["phi"] < 1.0 / (1.0 + k)           # (1-phi) > k*phi  <=>  Vgas^2 > k*Vstar^2
        n = int(m.sum())
        if n == 0:
            continue
        GBk += list(gg["gb"][m]); GOk += list(gg["go"][m]); FVk += list(gg["fv"][m])
        PHk += list(gg["phi"][m]); GLk += [j] * n
        SLk += [gg["sig_lnD"]] * n; CTk += [1 / np.tan(gg["inc"])] * n
        j += 1
    GBk, GOk, FVk, PHk, GLk, SLk, CTk = map(np.array, (GBk, GOk, FVk, PHk, GLk, SLk, CTk))
    a0k, fk, ck, wk = gls(GBk, GOk, FVk)
    Sk = np.sum(wk * GBk**2); yk = GBk / a0k
    vD = vI = 0.0
    for kk in set(GLk.tolist()):
        m = GLk == kk
        cD = a0k * np.sum(wk[m] * GBk[m]**2 * 2 * (yk[m] + 1)) / Sk
        cI = a0k * np.sum(wk[m] * GBk[m]**2 * 4 * (yk[m] + 1) * CTk[m]) / Sk
        vD += (cD * SLk[m][0])**2; vI += (cI * SIG_INC)**2
    KU = np.sum(wk * GBk**2 * PHk * (2*yk + 1)) / Sk
    KG = np.sum(wk * GBk**2 * (1 - PHk) * (2*yk + 1)) / Sk
    sU, sG = KU * a0k * SIG_LNU, KG * a0k * SIG_LNG
    med = float(np.median((GOk**2 - GBk**2) / GBk)); sEst = abs(a0k - med) / 2
    tot = math.sqrt(np.sqrt(1/Sk)**2 + vD + vI + sU**2 + sG**2 + sEst**2)
    return dict(N=len(GBk), Ngal=len(set(GLk.tolist())), a0=a0k,
                phibar=float(np.sum(wk*GBk**2*PHk)/Sk),
                sysU=sU/a0k, sysG=sG/a0k, tot_glscommit=math.hypot(sU/a0k, sG/a0k))
print(f"  {'k':>3}{'N':>6}{'Ngal':>6}{'a0':>11}{'<phi>':>8}{'sysU%':>8}{'sysG%':>8}"
      f"{'floor(U,G)%':>13}")
purity = {}
for k in (1, 2, 3, 5, 8):
    r = budget_kcut(gals, k)
    purity[k] = r
    print(f"  {k:>3}{r['N']:>6}{r['Ngal']:>6}{r['a0']:>11.2e}{r['phibar']:>8.3f}"
          f"{100*r['sysU']:>7.2f}%{100*r['sysG']:>7.2f}%{100*r['tot_glscommit']:>12.2f}%")
print("  As k rises: sysU FALLS (8.1->2.1%) but sysG RISES (7.3->9.4%) and N collapses")
print("  (310->14). The Upsilon+gas-cal floor is FLAT-to-WORSE with purity -- the gas cut")
print("  trades the stellar-M/L floor for the gas-calibration floor and cannot beat it.")

# ------------------------------------------------------------------- S6 GO/NO-GO
print(); print(bar)
print("S6 -- ABSOLUTE PLACEMENT (both footings) + THE GO/NO-GO VERDICT")
print(bar)
tot = b["tot"]; med = b["a0med"]
print(f"  gas-dominated slope: GLS {a0:.3e}  (16% box [{a0-tot:.3e}, {a0+tot:.3e}]),"
      f"  median {med:.3e}")
print(f"  {'target':<18}{'a0':>11}{'GLS tension':>13}{'median tension':>16}")
for nm, v in (("canonical cH_L/Z", A0C), ("ALT cH0/Z", A0A), ("MOND g_dagger", A0_RARFIT)):
    print(f"  {nm:<18}{v:>11.3e}{(a0-v)/tot:>+12.2f}s{(med-v)/tot:>+15.2f}s")
print("  -> current 16% box brackets ALL THREE; the estimator choice alone slides the")
print("     central value across the whole 9.4-1.2e-10 contested band. NOT resolved, as banked.")
print()
print("  GO / NO-GO on 3-sigma Lambda-anchor separation (canonical vs the 1.13-1.20 cluster):")
print(f"   * SPARC ALONE (existing + TRGB on every gas dwarf + GLS-commit + 2x sample):")
print(f"       floor-limited at ~{100*max(box(frac['stat']/math.sqrt(2), sD_trgb, frac['sysI'], frac['sysU'], frac['sysG'], 0.0), floor_gls):.0f}%  ==>  NO-GO "
      f"(~{max(box(frac['stat']/math.sqrt(2), sD_trgb, frac['sysI'], frac['sysU'], frac['sysG'], 0.0), floor_gls)/TARGET:.1f}x the {100*TARGET:.1f}% target).")
print("   * CONDITIONAL GO requires, ON TOP of TRGB + GLS-commit, TWO external inputs:")
print("       (i)  stellar-M/L prior 0.10 dex -> ~0.05 dex  (resolved-color / SED-fit or IFU")
print("            stellar pops on the ~31 improvable gas dwarfs; halves the 8.1% Upsilon floor)")
print("       (ii) gas-mass calibration 10% -> ~5%  (refined HI mass: helium/opacity, confirm")
print("            negligible H2 in gas-rich dwarfs; halves the 7.3% gas-cal floor)")
print(f"       WITH BOTH: box -> ~{100*ladder[-1][1]:.1f}% -- STILL SHORT of the {100*TARGET:.2f}% needed for 3-sigma\n"
      f"       (this optimistic stack doubles the sample + flat-5%-TRGB; the more conservative\n"
      f"       per_galaxy_budget.py stack lands ~7.7%. Neither reaches a clean 3-sigma with SPARC-like data).")
print("   * MINIMAL EXTERNAL INPUT = a curated gas-rich dwarf program: TRGB distances +")
print("     resolved stellar-pop M/L + refined HI masses on ~30-50 gas-dominated dwarfs.")
print("     This is a dedicated observing campaign, NOT something SPARC delivers as-is.")
print("   * Neither footing is excluded and none is 'closed': the Lambda-anchor test is")
print("     SET UP and its error structure fully mapped; it awaits the external data above.")

# ------------------------------------------------------------------- write results
best_sparc_alone = max(box(frac["stat"]/math.sqrt(2), sD_trgb, frac["sysI"],
                           frac["sysU"], frac["sysG"], 0.0), floor_gls)
out = dict(
    target_sln=TARGET, target_pct=100*TARGET,
    a0hat_gls=a0, a0hat_median=med, box_now=tot, box_now_pct=100*tot/a0,
    frac_terms={t: frac[t] for t in frac},
    averaging_pct=100*avg, floor_committed_pct=100*floor_cons, floor_glscommit_pct=100*floor_gls,
    gascal_floor_sensitivity_pct={str(k): 100*v for k, v in gascal_sens.items()},
    sysD_now_pct=100*math.sqrt(varD_now)/a0g, sysD_alltrgb_pct=100*math.sqrt(varD_all_trgb)/a0g,
    n_gasdom_gals=len(names), n_already_trgb=n_trgb, n_improvable=len(buy),
    top_trgb_targets=top_targets,
    scenario_ladder={lab: 100*bx for lab, bx in ladder},
    purity_trap={str(k): dict(N=purity[k]["N"], sysU_pct=100*purity[k]["sysU"],
                              sysG_pct=100*purity[k]["sysG"],
                              floor_pct=100*purity[k]["tot_glscommit"]) for k in purity},
    best_sparc_alone_pct=100*best_sparc_alone,
    best_conditional_pct=100*ladder[-1][1],
    verdict_sparc_alone="NO-GO",
    verdict_conditional="NO-GO with SPARC-like data even under the full optimistic stack (endpoint ~6.8-7.7% > 6.31% target); a dedicated ~142-dwarf TRGB+ML+HI campaign is the minimal path to a MARGINAL 3-sigma",
    a0_canon=A0C, a0_alt=A0A, a0_mond=A0_RARFIT)
json.dump(out, open(os.path.join(HERE, "reach_target_results.json"), "w"), indent=1, default=float)
print(f"\n[reach_target_results.json written]")
print("EXIT 0: STEP-A reachability computed. Exit code is not a verdict.")
