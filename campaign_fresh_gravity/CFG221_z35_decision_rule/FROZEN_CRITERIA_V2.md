# CFG221 v2 — FROZEN CRITERIA for a SECONDARY decision rule (v1 stays the PRIMARY rule)

Written 2026-09-30 and committed BEFORE v2 is run on anything, and before any new real disc value (GN20, REBELS-25, class B, Corpus Z1, the Dessauges-Zavadsky+20 / Jones+21 tables) is read. **The orchestrator's decision:** v1 (`FROZEN_CRITERIA.md`, lane 251985c27: one-sided in practice, noise-free control C2 failed 6 of 12, σ_required 0.15 dex with about 50 outer-radius class-A discs) stays the pre-registered PRIMARY rule with its operating characteristics recorded as they are; v2 is a separately labelled SECONDARY rule, judged by the SAME controls, C2 above all. **If v2 also fails C2 that is recorded and this stops: no v3 is iterated to chase a pass.** **κ = ½ is FITTED, not derived.** Nothing here says the data favour a framework.

## What v2 changes (and only this)
Everything in `FROZEN_CRITERIA.md` and its Addenda stays: the sample rule (class-A detections, outermost MEASURED radius), the per-disc statistic, the laws, the four cells as a REPORTED set, the marginalised calibration prior (σ_dust = σ_CO = 0.30, σ_[CII] = 0.40 dex), the mock template, scenarios, N grids, the controls' definitions. v2 changes the VERDICT only:
1. **A primary-cell verdict.** The verdict uses (ν_mono, canonical) alone. The other three cells (ν_mono alt, P2 canonical, P2 alt) and the leave-one-out fits are REPORTED as robustness (the status of each law in each cell; whether the verdict survives dropping any one disc) and are not conditions.
2. **A one-sided marginal bound for each law, B = 10,000 (in the operating-characteristics runs as well as on real discs).** In the marginal bootstrap (discs resampled and τ_k ~ N(0, σ_k²) redrawn in every resample), a law is **DISFAVOURED-under** if the 95th percentile of the resampled medians of δ is below 0, **DISFAVOURED-over** if the 5th percentile is above 0, **NOT-DISFAVOURED** otherwise (each direction is a one-sided 5% test).
3. **Verdict:** FLAT-SEPARATED(v2) = the rival (H(z)) is DISFAVOURED-under and FLAT is NOT-DISFAVOURED; RIVAL-SEPARATED(v2) = FLAT is DISFAVOURED-over and the rival is NOT-DISFAVOURED; else NO-SEPARATION(v2). The extra pairs use the same LO-/HI- machinery.

## Reporting rule
**Both verdicts are always shown side by side, and v1 governs any headline.** A v2 verdict is never quoted without the v1 verdict beside it and its operating characteristics.

## Operating characteristics and controls (same definitions as v1, on the same mock generator)
- Template, truth generation ((ν_mono, canonical); MISMATCH (P2, alt) as a sensitivity), true offsets **c ∈ {0, +0.30, −0.30, +0.60, −0.60, PRIOR}**, scenario **REAL** (the 0.25 dex total per-disc scatter of CFG220; OPT at c = 0 for N = 13 and 36), **N ∈ {6, 13, 20, 36, 50}**, K = 100 mocks, seed 221, **B = 10,000**. Plus the prior-width sweep of Addendum 3 for v2: σ scale 0.5 (0.15 dex), REAL, c ∈ {0, PRIOR}, N ∈ {13, 20, 36, 50}.
- **C1** false-separation control: the WRONG-separation rate at c = 0, ±0.30 and PRIOR is ≤ 0.094 for every N and both truths (REAL). **C2** noise-free (ε = η = 0, c = 0): the correct separation at every N for both truths. **C3** (MUTATE D × 1.5): the noise-free flat-truth mock loses FLAT-SEPARATED(v2) at every N. **C4** the machinery at σ = 0 reproduces CFG220's headline medians (flat +0.106, rival −0.203) to 1e-9 and its two-sided 95% CI edges to 0.01 (the one-sided verdict thresholds are reported beside).
- **FEASIBLE at N** and **σ_required** as defined in v1 and Addendum 3.

## Reporting of the outcome
v2's result is reported as it comes out against C1 and C2, whichever way, next to v1's; a v2 that passes C2 is a SECONDARY rule with its operating characteristics, nothing more; a v2 that fails it is recorded as failed and that is the end of the iteration.
