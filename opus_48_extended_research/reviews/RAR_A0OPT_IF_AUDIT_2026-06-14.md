# Front [rar_scatter_a0opt] — the IF audit on the SPARC RAR a0-optimum + scatter (2026-06-14)

Does the interpolation function (IF) move the RAR a0-optimum, the scatter, or the 9.36e-11 footing?
Recompute on the REAL 175 SPARC curves (`real_research/data/sparc_data/*_rotmod.dat`, Lelli+2016),
4 IFs × {Υ=0.50, 0.70} × {raw-rms, median-subtracted, weighted} dex-scatter. No synthetic data.
Scripts run: `AUDIT_rar_footing_recheck.py`, `HOSTILE_rar_footing_independent.py`,
`real_research/reviews/redteam_rar_framework_a0.py`, `real_research/rar_framework_a0_mlfit.py`,
plus the consolidated /tmp recompute. 2803 pts / 164–175 gal after err/V<0.1 cut.

## The IF is genuinely load-bearing here (verified, not assumed)
Spread in g_obs across the 4 IFs at fixed a0: **1.6% deep-MOND (g_bar/a0=1e-3), 27% at the transition
(g_bar~a0), 1% Newtonian (g_bar/a0=100)**. The RAR a0-optimum is set by the transition region, so it IS
IF-dependent — confirming the prompt's triage. (BTFR/deep-MOND fronts living at g_bar/a0<<1 are IF-robust.)

## (i) optimal a0 and the 9.36e-11 penalty, per IF × Υ — RAW rms dex (the banked metric)

| Υ_disk | IF | optimal a0 | 9.36e-11 offset | penalty |
|---|---|---|---|---|
| 0.50 | McGaugh | 1.128e-10 | −17.0% | +2.10% |
| 0.50 | simple | 1.101e-10 | −15.0% | +1.55% |
| 0.50 | standard | 1.573e-10 | −40.5% | +16.4% |
| 0.50 | **dS-Unruh (framework)** | 1.438e-10 | −34.9% | +11.1% |
| 0.70 | McGaugh | 7.780e-11 | +20.3% | +1.86% |
| 0.70 | simple | 7.544e-11 | +24.1% | +2.39% |
| 0.70 | standard | 1.149e-10 | −18.5% | +2.69% |
| 0.70 | **dS-Unruh (framework)** | **1.028e-10** | **−8.9%** | **+0.51%** |

The optimum spans **7.5e-11…1.6e-10** across the cells — the IF and the M/L each swing it ~20–40%.

## (ii) the banked dS-Unruh@Υ=0.70 claim — CONFIRMED on raw-rms, but METRIC-FRAGILE

On the framework's OWN dS-Unruh ν at Υ=0.70, **raw-rms** gives optimum **1.028e-10**, 9.36e-11 is
**−8.9%** (below optimal), penalty **+0.51%**. This reproduces the banked table
(`SPARC_RAR_FOOTING_BOTHWAYS_2026-06-13.md` §4: 1.03e-10 / −9% / +0.51%) **to 3 digits**, and the paper's
"within 0.3%" → the banked "within ~0.5%" is **DEFENSIBLE on this metric**. Confirmed.

**But the favorable result does not survive a change of scatter metric** (the load-bearing subtlety, both
ways — dS-Unruh@Υ=0.70):

| metric | optimal a0 | 9.36e-11 offset | penalty |
|---|---|---|---|
| RAW rms (no vertical offset) | 1.028e-10 | −8.9% | **+0.51%** |
| MEDIAN-subtracted | 1.329e-10 | −29.6% | +1.08% |
| inv-var-weighted + offset | 1.478e-10 | −36.7% | +2.82% |

Allowing a vertical normalization offset (which the HOSTILE and red-team scripts do, via median/weighted
subtraction) raises the dS-Unruh optimum to 1.33–1.48e-10 and pushes 9.36e-11 to 30–37% below it. So the
"~0.5% of optimal" win is **specific to the raw-rms-no-offset metric**; the penalty stays small (≤~2.8%)
everywhere, but the headline "−9% / 0.5%" is NOT metric-robust. The honest both-ways statement: **the
penalty of 9.36e-11 is ≤~2.8% across all IF × Υ × metric cells (small everywhere, flat-bottomed χ²); the
optimum is non-diagnostic; and neither a "~20% low" (McGaugh-Υ=0.50) NOR a "~9% / 0.5%" precision-win
(dS-Unruh-Υ=0.70-raw-rms) is robust — both are convention artifacts.** Do not manufacture either.

The mlfit script (`real_research/rar_framework_a0_mlfit.py`, the CORRECT one) sidesteps the metric issue:
fix a0=9.36e-11 on the dS-Unruh ν, fit Υ → best Υ_disk=0.70, scatter 0.108 dex, vs regular-MOND
(1.2e-10, Υ=0.5) 0.122 dex. Framework a0 IS consistent with the RAR at a plausible 3.6μm M/L. This is the
clean both-ways landing and it is IF-correct.

## (iii) which banked RAR verdicts used a normal-MOND IF labeled/used as the framework when judging a0

| script | IF used to judge the a0 | label issue | load-bearing? |
|---|---|---|---|
| `real_research/reviews/redteam_rar_framework_a0.py` | **McGaugh ν @ Υ=0.5** for the headline "~22% LOW / low edge of band" + the (C) "many-σ" profile | judges the FRAMEWORK a0 with McGaugh (normal-MOND) ν at the McGaugh M/L | **YES, MOVED** — its own table (B) shows the dS-Unruh (sqrt) row free-fits 1.279e-10 @Υ=0.5 (so −27%, even worse at that M/L); but on the framework footing Υ=0.70 the dS-Unruh row is −8.9%/0.5%. The "~22% low" verdict is the McGaugh-Υ=0.5 cell, NOT the framework's own ν+M/L. Mis-footed both in ν and M/L. |
| `opus_48_extended_research/reviews/sparc_rar_footing_bothways.py` | McGaugh ν only (script body) | the .py judges with McGaugh; the .md §4 patches in the dS-Unruh table separately | partially — the .py's "+20% high @Υ=0.70" is the McGaugh-ν artifact the .md §4 already retracted. The .py was never updated to the dS-Unruh ν. |
| `real_research/reviews/sparc_rar_honest.py` | McGaugh ν | free-fits a0 (does not force the framework value), reports magnitude consistency — not strictly a footing verdict, but uses McGaugh ν throughout | NO — free-fit + magnitude-band claim; the a0~cH0/Z O(1/6) conclusion is IF-insensitive |
| `real_research/reviews/rar_tightness_intrinsic.py` | McGaugh ν at BOTH the "Υ=0.50" and "FRAMEWORK Υ=0.70" footings | the "framework footing" row uses McGaugh ν, not dS-Unruh | NO for the headline (intrinsic≈0 is an error-budget-exceeds-observed argument, IF-insensitive); the absolute scatter floor shifts but the conclusion holds |

CLEAN (IF-correct, use dS-Unruh sqrt): `real_research/rar_framework_a0_mlfit.py`,
`real_research/reviews/predicted_a0_rar_consistency.py` (Q2), `real_research/rar_emergent_discriminate.py`,
and the dS-Unruh rows of `AUDIT_rar_footing_recheck.py` / `HOSTILE_rar_footing_independent.py`.

## Disposition (both ways)
The IF IS load-bearing on this front (transition-regime quantity). The red-team "~22% low / low edge of
band" verdict is a normal-MOND-IF + McGaugh-M/L artifact and should be read as the McGaugh-Υ=0.50 cell, not
a framework verdict. BUT correcting to the framework's own dS-Unruh ν does NOT cleanly hand the framework a
win either: the favorable "−9% / 0.5%" lands only on the raw-rms metric; allowing a vertical offset moves
9.36e-11 to 30–37% below the dS-Unruh optimum. The convention-robust truth, unchanged in spirit: **penalty
≤~2.8% everywhere (small, flat-bottomed), optimum non-diagnostic of 9.36e-11, no robust deficit and no
robust precision-win.** Quarantine held (Z never asserted from this fit; coefficient stays H0-hostage).
