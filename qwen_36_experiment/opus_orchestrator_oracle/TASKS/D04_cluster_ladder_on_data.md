# D04 — The cluster ladder, on real cluster data
COST: M | script: `mi_cluster_ladder_data_2026.py`

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The task
M10 identifies the cluster mass floor as the one measurement that decides the framework. This task gets the
*current* data rather than the stored ladder.
1. Find cluster samples with both X-ray and weak-lensing masses (search for published compilations; the
   corpus references η(R500) = 2.334 median on the framework's own kernel, +0.405 dex = 4.05/2.70/2.03σ).
2. Recompute η(R500) per cluster with `TOOLS/mi_constants.py` values. Report median and scatter.
3. Report the *actual* current weak-lensing mass calibration uncertainty in dex, and place it on M10's ladder
   (0.10 / 0.15 / 0.20 / 0.30 dex → 3.72 / 2.49 / 1.87 / 1.25 σ).
4. State plainly which rung we are on today.

## Known walls
The ~1.6–1.8 figure holds **only** after weak-lensing recalibration; the XRISM claim is WITHDRAWN. The
published "seventeen times" is the ratio to McGaugh's a₀ — the corpus understated its own problem by 28%.
