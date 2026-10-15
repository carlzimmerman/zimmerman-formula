# AG3_sparc_annulus_widths — lane record

**Date:** 2026-10-15 · **Track:** argon (interactive session) · **Status: LANDED —
K3 verdict S (stable under all pre-registered robustness cuts), K4 static ball excluded,
B2 0/78 unstable; exit 1 = K2b CONDITIONAL on record (frozen tolerance miscalibrated;
scatter quantitatively explained by the law's registered precision; NOT retro-passed).**

Measures the radial extent of the A/r² phantom reading in 175 SPARC galaxies via the
exact law identity ρ(r) = √(M(r)/M_b)/(√(u+1)+√u) and compares annulus widths against
AG1's BC ladders (DF 7.4403 binding). Median w = 1.843 (4× margin), max 8.98; three
named w>7.44 candidates (UGC 06787, UGC 02953, UGC 09133) → follow-up AG3b. Interior
(r ≤ 0.62 r_M): X_ball = 0.0025 ⇒ the A/r² static ball is NOT the realized interior
state (>10σ vs every systematic); haze-vs-Newtonian undecidable at SPARC precision.
Baryon-inclusive eigen-solve (symbolically assembled, drift −GM_b/(2r²)): all lowest
eigenvalues positive.

## Files

- `FROZEN_CRITERIA.md` (commit 4560f945c) + `FROZEN_CRITERIA_AMENDMENT_A.md` (commit
  7527066a6) — both committed ALONE before any data run. Amendment A replaces the
  point-mass r_lo corollary with the exact enclosed-mass law identity (design-stage
  algebra, pre-run).
- `ag3_sparc_widths.py` / `.out` / `_results.json` — MAIN run. `python3
  ag3_sparc_widths.py` (exit 0 iff all gates incl. frozen K2b tolerance).
- `ag3_sparc_widths_MUTATE.out` / `_MUTATE_results.json` — `MUTATE=1` run: M1 (M_b
  shuffle, seed 20261015) degrades K2b as designed; M2 (baryonic band) median r_lo
  shift ×5 — frozen arm 2; M3 (role swap) zero eligible edge-runs, 20 galaxies with
  real negative-g_ph inner points (reported).
- `IDEA.md` — brief-format write-up. `HANDOFF_TO_CONDUCTOR.md` — register-row proposals
  + AG3b spawn proposal.

## Inputs (runtime reads, zero typed framework constants except the frozen robustness
variant a0_alt = 1.1279e-10 m/s², G071 precedent)

- `glm53_push/data/rotation_curve_corpus_v7.json` (175 SPARC, G071 conventions)
- `deepseek_push/G081_results.json` (a₀, α_break)
- `real_research/data/sparc_a0_environment_table.csv` (G071 isolated/low-EFE subset)
- AG1 closed forms recomputed in-script: w₁(DF), w₁(DD), ν₀ = √7/2.

## Honest notes

- K2b FAILED its frozen tolerance (0.326 vs 0.15) and stays failed on record; the
  post-hoc K2d MC (errV-only: σ_ln = 0.12, median |z| = 1.70) plus the band-region
  law-residual scatter (std 1.0, slope 0.671 ⇒ expected ≥ 0.33) show the scatter is the
  framework's own registered law precision propagating through a difference estimator —
  unbiased (signed median +0.0000). Calibration lesson registered in the handoff.
- M1's degradation margin is thin (0.3045 vs 0.3) because the K2b metric is
  law-residual-dominated: recorded, not hidden.
- Eligibility (78/165) is a finding, not a cut: the other 87 curves never robustly
  enter the factor-2 A/r² regime inside their measured range.
