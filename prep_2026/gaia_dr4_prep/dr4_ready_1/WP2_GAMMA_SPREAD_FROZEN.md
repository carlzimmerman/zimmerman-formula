# WP2-γ — FROZEN QUESTION: the build-to-build scatter of γ̂ at the builder's real settings (N_SHIFT = 30)

Written 2026-09-30 and committed BEFORE the script that answers it exists or runs. **DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.** Nothing frozen is touched: `catalog_builder/build_catalog.py`, `wide_binary_pipeline.py`, the pre-registration and all `*_HASH.txt` files are imported or read only; the only edits are in memory. Requested by the orchestrator after the WP2 noise floor (bd780ea41).

## Why
The WP2 noise floor showed that the frozen builder draws random numbers in three streams (the stage-E shifted realisations, the `r_chance` leave-10%-out fold, the stage-G velocity-error Monte Carlo) and that, at the smoke setting N_SHIFT = 3, rebuilding the same base with other seeds changes about 2.8% of the final pairs (152 to 187 one-way flips of about 6,175). If that is also true at the real setting, DR4's primary γ̂ carries a build-to-build scatter that the pre-registration (σ_tot = √(σ_fit² + 0.02²)) does not list.

## The question (Q1 to Q3)
For the PRIMARY base (the frozen DR3 extract, all twelve chunks), at **N_SHIFT = 30** (the builder's default and the real setting), with all three random streams re-seeded and nothing else changed:
- **Q1.** How large are the SD of the final pair count and the one-way flips between builds?
- **Q2.** How large is the SD of γ̂ across builds, for both footings, **in units of σ_fit (the fit's own statistical error, mean over builds) and of σ_tot = √(σ_fit² + 0.02²)** (pre-registration §1.3 / the error model quoted there)?
- **Q3.** How much of that SD is the fit's own bootstrap noise (the same catalog refitted with other fit-RNG seeds)?

## Design (fixed here)
- **Builds:** seed sets k = 0, 1, …, 9 (ten). k = 0 is the builder's own frozen seeds (the real thing). For k: `B.SEED = SEED0 + k` (stage-E mask and `r_chance` folds), the stage-E shift seeds `r + 1 + 100 k`, the stage-G velocity-error seed `SEED0 + k`. `N_SHIFT = 30` (asserted equal to the builder's own default). Stages A to D are shared (symlinked from the WP2 caches: the streams do not touch them, checked by C2); E, F, G are recomputed per build in their own gitignored work dirs. Offline, socket guard, `nice`.
- **γ̂ (as the pipeline's own validation does, `catalog_builder/validate_dr3.py::v4_gamma`):** each build's final table is written as a CSV and read by `wide_binary_pipeline.ingest_csv`; the fit is `run_fit` against the DR3-noise forward model (population 3,000,000, seed 20261216, `dr4 = False`), **both footings** (canonical 9.36e-11 and alt 1.13e-10); γ̂ = the returned γ_inf and σ_fit = its returned error. The fit RNG seed of build k is 20261217 + k. NON-SCORING: no comparison with any prediction, no label.
- **Fit-only control:** the k = 0 catalog refitted with ten other fit seeds (20261217 + 100 + j, j = 1…10); its SD is the part of the build SD that is the fit's own bootstrap.
- **Reported, nothing else:** per build: the final pair count, the one-way flips against k = 0, γ̂ and σ_fit for both footings; across the ten builds: mean and SD (ddof = 1) of the count and of the flips; SD(γ̂) and **SD(γ̂)/mean σ_fit and SD(γ̂)/mean σ_tot** per footing; the fit-only SD and the ratio of the two SDs; the implied build-only SD = √(max(0, SD_build² − SD_fitonly²)) and its ratio to mean σ_fit. No threshold is declared and no word such as pass, fail, negligible or significant is used; the orchestrator's 10%-of-σ_fit figure is the reader's yardstick, not a criterion here.

## Controls (all reported; a failure is reported plainly)
- **C1** the builder's own N_SHIFT default is 30. **C2** every build has the same stage-C and stage-D counts as the WP2 run (initial pairs 380,438; clean 214,002). **C3 MUTATE** (`MUTATE=1`, outputs `*_MUTATE`): v_perp × 1.05 on the k = 0 catalog moves γ̂ by more than three times the fit-only SD in both footings (the fit responds to the catalog). **C4** the flip counter returns exactly 100 when 100 pairs are removed from a build's set.

## Limits (written before the run)
The DR3 stand-in has about 6,200 final pairs, so σ_fit is larger than at DR4's N ≈ 30,000 (σ_fit scales as √(30000/N)); the quantity here is the RATIO SD(γ̂)/σ_fit, and its value at DR4's N is not measured (random replacement of a fixed fraction of pairs would leave the ratio unchanged to first order, which is a statement about a model, not a measurement). The three streams are varied together; the one-stream-at-a-time decomposition is not run. The forward model is the DR3 validation's, not DR4's. Ten builds give an SD with a relative error of about 24%.
