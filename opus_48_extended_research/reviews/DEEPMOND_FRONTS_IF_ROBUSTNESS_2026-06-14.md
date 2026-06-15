# Deep-MOND fronts — interpolation-function (IF) robustness audit (both ways, 2026-06-14)

*Front 3 of the IF-contamination sweep. Question: are the "deep-MOND" fronts (BTFR, dSph, clusters) genuinely
IF-robust under the framework's dS-Unruh `g_obs=√(g_N²+g_N·a₀)` (⇔ ν(y)=√(1+1/y)), or does any of them hide a
transition-regime IF-sensitivity that was mis-stated? VERIFIED by explicit recompute, not assumed. Framework
a₀=9.36e-11.*

## Headline

Two of the three are genuinely IF-robust **by construction** (they use the y→0 asymptote, where every IF → √(g_N·a₀));
the third (clusters) has a **REAL, already-correctly-handled ~+8% transition-regime IF-sensitivity** — and correcting
to the framework's own dS-Unruh IF makes the cluster deficit **WORSE (η 2.15→2.33), not better.** No deep-MOND front
used simple-μ/McGaugh/AQUAL **labeled as the framework** in a way that mis-states a verdict. One stale published
number (scorecard row 17, η=1.92) lags the correct dS-Unruh value but is already flagged in the live FABLE ledger.

## (i) BTFR — IF-robust BY CONSTRUCTION. Confirmed.

`real_research/reviews/btfr_honest.py`, `real_research/scaling_mond_btfr_evolution.py`,
`real_research/highz_btfr_prediction.py` all use the **deep-MOND asymptote V_flat⁴ = G·M_bar·a₀** (slope EXACTLY 4,
intercept = log(1/G a₀)). No ν enters. V_flat is the *asymptotically-flat* (deepest-MOND-radius) velocity, so the
relation is the y→0 limit by definition.

**Recompute (explicit, not assumed):** inverting (g_obs,g_bar) on the flat part to recover a₀ — by gbar/a₀=0.1 the
dS-Unruh and simple-μ recovered a₀ agree to the asymptote (the simple-μ inverse formally diverges away from the deep
limit precisely *because* both collapse to √(g_N a₀) there). The btfr_honest a₀-implied-at-slope-4 is computed
directly from V⁴=GMa₀ and carries **no IF dependence** — only Υ (M/L) and the fit metric move it (1.24e-10 at
Υ=0.70, 1.52e-10 at Υ=0.50). **VERDICT: IF-robust. The IF does NOT move the BTFR slope/intercept/implied-a₀.** (The
only IF-sensitivity is a faint curvature/scatter bend at the high-V transition end — it touches the SCATTER, not the
a₀, and is sub-dominant to the M/L and metric spread already in the ledger.)

## (ii) dSph velocity dispersions — IF-robust BY CONSTRUCTION. Confirmed.

`real_research/reviews/project15_dsph_efe_thermometers.py`: isolated σ⁴=(4/81)·G·M·a₀ (deep-MOND asymptote, no ν);
EFE-suppressed G_eff = G·a₀/g_ext (the deep-MOND EFE limit, no ν). Crater II operating point:
**g_int/a₀ ≈ 3.9e-4** (100% deep-MOND internal), g_ext/a₀ ≈ 0.6. Both regimes are y≪1 → IF-free.

**Caveat already stated in the script's own "HONEST LIMITS":** denser dwarfs near g_int~a₀ are NOT captured by the
two-regime asymptotic formula and would need the full ν across the transition — but those are NOT the clean deep-MOND
cases the front rests on (Crater II, Antlia II, UDGs). **VERDICT: IF-robust for the deep-MOND dSphs that carry the
front.** *Footing note (separate from the IF, from the FABLE ledger):* this script uses a₀=1.2e-10, not 9.36e-11;
at the framework a₀ the dSph over-dispersion is WORSE (Sextans/Draco/UMi −3.7 to −4.2σ). That is a *footing* effect
(σ∝a₀^¼), NOT an IF effect, and the over-dispersed count (3/8) is unchanged.

## (iii) Clusters — a REAL +8% transition-regime IF-sensitivity, correctly handled, and it makes the deficit WORSE.

This is the one deep-MOND front where the IF is **not negligible**, and the audit must say so plainly. At the eRASS1
operating point **median g_bar/a₀ = 0.037** (96% of clusters y<0.1) — deep-MOND, but not *infinitely* deep, so the IFs
have NOT fully converged. Recomputed on the real N=9830 sample (framework a₀=9.36e-11, Υ-equiv fstar=0.20):

| IF | η median | vs deep-MOND asymptote 1/√y at y=0.037 |
|---|---|---|
| simple-μ | 2.149 | ν = +10.1% above asymptote |
| McGaugh-RAR | 2.153 | +9.9% |
| standard-μ | 2.364 | +0.9% |
| **dS-Unruh (FRAMEWORK)** | **2.334** | **+1.8%** |

The split is structured, not random: simple-μ and McGaugh-RAR sit ~+10% above the asymptote (their ν over-predicts the
boost at y~0.04), so they give a SMALLER η; dS-Unruh and standard-μ hug the asymptote (+1-2%), giving a LARGER η.
Because η = g_obs/(ν·g_bar), **a larger ν → smaller residual.** The dS-Unruh/simple-μ ratio at y=0.037 is 0.925 —
the ~−8% on ν, i.e. **+8% on the η deficit.**

**Recompute under the framework dS-Unruh IF vs what was used:**
- `real_research/clusters_framework_a0.py` (the script the paper cites) **already uses dS-Unruh** `g_obs=√(g_bar²+g_bar·a₀)` and outputs **η median = 2.334** — the correct framework value. No contamination.
- `real_research/reviews/clusters_eta_audit.py` runs all four IFs explicitly; its `sqrt(g^2+ga0)` row = 2.334 ✓.
- The paper §10.1 (L224) = 2.33 ✓, §11.5/C5 (L296) = 2.33 ✓ — both correct (dS-Unruh).
- **Scorecard ROW 17 (`ZIMMERMAN_THEORY_OF_GRAVITY.md` L261) still reads η = 1.92** — that is the regular-MOND-a₀
  (1.2e-10) value, NOT a framework-IF value, and it is the milder number. It UNDERSTATES the framework's own deficit
  by ~13%. Already logged as the top action item in `FABLE_A0_FOOTING_AUDIT_LEDGER_2026-06-14.md` (it's a *footing*
  lag — a₀=1.2e-10 vs 9.36e-11 — compounded by simple-μ; both push the same way, milder).

**Both ways, explicitly: correcting the cluster IF to the framework's dS-Unruh makes the number WORSE (2.15→2.33).**
This is the opposite of the wide-binary case (where the simple-μ→dS-Unruh correction lowered the EFE cap, a
pro-framework move there but a worse number here). No manufactured win. The cluster deficit is a ROBUST FAIL at every
IF and every a₀ (2.07 at regular MOND, 2.33 at framework, simple-2.15 to standard-2.36) — the IF moves the *severity
by ~8%*, never the *verdict*.

**One non-framework script flagged for completeness (NOT a mis-verdict):** `cluster_a0_from_density_HIS_FORMULA.py`
uses `nu = 0.5*(1+√(1+4/x))` = **simple-μ** — but its own header says "That is NOT the framework's content"; it is
the Tian-2020 density-a₀ exploration, not a framework η verdict. Named per the both-ways rule; non-load-bearing.

## Bottom line

| Front | IF used | Labeled | Deep-MOND IF-robust? | Recompute under dS-Unruh | Verdict move? |
|---|---|---|---|---|---|
| BTFR | deep-MOND asymptote V⁴=GMa₀ (no ν) | framework | YES (by construction) | a₀ unchanged by IF | NO |
| dSph | deep-MOND asymptote σ⁴=(4/81)GMa₀ + G_eff=Ga₀/g_ext (no ν) | mixed (a₀=1.2e-10) | YES for the deep-MOND dSphs | σ unchanged by IF | NO |
| Clusters | **dS-Unruh √(g²+ga₀)** in the framework script | framework ✓ | NO — +8% transition sensitivity | η 2.15(simple)→2.33(dS-Unruh) | severity +8%, **WORSE**; verdict (FAIL) unchanged |

The deep-MOND fronts are IF-robust **where claimed**, with the single honest exception that clusters sit at y~0.04
(not y→0), carry a real +8% transition IF-sensitivity, and the framework's own dS-Unruh correctly gives the LARGER
(worse) 2.33 — already used in the framework cluster script and the paper body, with only the stale 1.92 scorecard row
lagging. No deep-MOND verdict was inflated by a normal-MOND IF mislabeled as framework. Both ways, no exception.
