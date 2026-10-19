# CFG841 — calibration-free shape test of the law's form on SPARC (Codex ZAR-D1)

Criteria: `FROZEN_CRITERIA.md` (d35ad36ab) + Amendment A1 (e4cbf0d3e, before any real-data statistic).
Idea: Codex's analytic review (`real_research/analytic_review_2026_10_18_codex/SHAPE_NULL.md`). Run: `python3 cfg841.py`
(power controls `CFG841_MUTATE=S` / `Q`). Seconds.

## Result — CLASS (primary): **NOT DIAGNOSTIC** (the power controls fail: SPARC cannot separate the two law shapes)
- **Run 1 (z-space estimator):** MUTATE-S classed synthetic simple-law data QUADRATIC FAVOURED — an estimator defect
  (asymmetric error propagation). Fixed by Amendment A1 before any real-data statistic (velocity-space fits, same errors);
  run-1 outputs kept (`*_run1_zspace.*`).
- **Run 2 power controls (velocity space):** primary (10 gas-dominated galaxies): synthetic simple → NEITHER (ΣΔχ² +0.2),
  synthetic quadratic → NEITHER (+0.1). The gas-dominated discs all sit deep in the low-acceleration regime
  (g_bar/a0 = 0.01–0.06), where both laws reduce to g² = a0 b; they carry no shape information. Secondary (131 galaxies,
  fixed-composition template, approximate): synthetic simple → NEITHER (ΣΔχ² +72.8, frac 0.47); synthetic quadratic →
  QUADRATIC FAVOURED (−39.2). Partial power only.
- **Real data:** primary ΣΔχ² +0.0 (NEITHER, as the controls predict); secondary ΣΔχ² **+194.2**, frac > 0 = 0.53 → would read
  SIMPLE FAVOURED, larger than the synthetic simple-law value (+72.8). Reported as an approximate lean toward the framework's
  simple action law, NOT a verdict: the secondary's template assumes fixed stellar/gas composition, and its own simple-law
  control did not pass the class bar.
- **Reading:** Codex's elimination is correct and clean, but SPARC's gas-only systems lack transition-regime leverage; a
  decisive version needs gas-dominated systems that span g_bar/a0 ~ 0.1–3 (or resolved stellar M/L to make the full template
  exact). The full-template lean toward the simple law is worth a follow-up with a declared composition model.

## Controls
- K1 PASS (hand example D_s = 0, D_q = 1/12 exactly).

κ = ½ fitted (cancels here); cold energy mass required; not theory closed.
