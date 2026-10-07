# CFG422 FROZEN CRITERIA: is CFG414's confinement benefit robust across seeds and footings? (256³)
(owner 2026-10-07: "launch more computations"; committed before any run)

**Runs.** CFG414's engine (x = 0.4 cover, corrected k_J, RES with R_c = 3, MIX-A) at 256³, NSEED = 256, for seeds 359 / 360 / 361 × canonical / alt. That is 6 runs.
- Baselines: same-seed S0 (CFG359 for 359; CFG420 for 360 / 361). S0 has no a₀, so it serves both footings.
- Unconfined comparison: CFG410 BASE (seed 359) and CFG420 (360 / 361, canonical). There is no unconfined alt run for 360 / 361, so alt is reported against S0 only.

**Measure.** σ₈ ratio and max|P−1| (k ≤ 1) per run. The benefit is Δ = pdev(unconfined) − pdev(confined), where the unconfined run exists.

**Decision.**
- ROBUST BENEFIT: Δ ≥ 0.05 in every seed with an unconfined comparison, AND the confined run is never worse than the unconfined one.
- GROWTH OK count: how many of the 6 confined runs pass CFG361's cuts. This is reported, not the verdict.

**Caveat.** At 256³ the 0.4 r_ta cover is under one cell for median hosts (CFG413), so this is coarser than the 512³ CFG414. It is a robustness check, not a confirmation.
