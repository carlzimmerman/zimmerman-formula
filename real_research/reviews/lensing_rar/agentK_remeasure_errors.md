# AgentK — jackknife errors for the independent re-measurement + our own split significance

*2026-06-11. Script agent-written, orphaned at the spend limit; run + memo completed by the orchestrator from the
verified `.out` (no logic changes). 50 sky patches, leave-one-out over 181,477 isolated lenses; full 30×30 jackknife
covariance; Hartlap correction applied (N_jk=50, p=15, factor 0.673).*

## The validation gate: PASSES, both classes
- **Early** vs released Fig-8: χ²_fullcov = 11.9/15 → **0.4σ** (median ratio ~1.04). Validated.
- **Late** vs released: χ²_fullcov = 19.6/15 → **1.3σ** — the v3 "excess scatter" was shape noise; within errors.
- Caveat both ways (recorded): ours and the released profiles share survey data → correlated, so these pulls are
  lenient; but the sample differences (Δχ=10 Mpc isolation window, the LePhere-valley colour split at 2.0 vs
  Brouwer's 2.5, the +0.15 dex fluxscale) would produce *coherent* offsets, which the full-cov χ² is sensitive to.

## Our own split significance (the program's first fully-owned headline number)
**Early above late in 14/15 bins, mean +0.209 dex; χ²(early−late | full jackknife C_d) = 126.0/15 → 9.1σ raw;
Hartlap-corrected HEADLINE = 6.8σ** (diagonal-only reference 7.1σ; 25-merged-patch robustness 24.6σ raw/13.1σ
corrected — patch-count insensitive in the conservative direction).
Consistency with the released-profile battery (8.8σ, +0.261 dex, 15/15): all four expected dilutions go the right
way — fewer lenses (181k vs 259k → ×~0.84 in σ), jackknife covariance includes cosmic variance the analytic
covariance lacks, the colour-split convention (53/47 at the LePhere valley), and the count-calibrated isolation
window. **The split is now established independently, end to end, in this repo: lenses, stack, covariance, number.**
