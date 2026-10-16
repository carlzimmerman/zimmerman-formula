# CFG816 FROZEN CRITERIA: Eddington bias in eRASS1 gas masses. Is the non-monotonic tercile pattern a selection effect? (committed before any script)

**Question.** Across CFG809/813/815, the eRASS1 gas-mass terciles want non-monotonic amounts of free cold energy. The light
tercile looks fine; the middle is short. eRASS1 is flux-limited, so low-mass clusters near the threshold are preferentially
up-scattered in measured M_gas. This is the Eddington bias, flagged in CFG687. This is a DATA-SIDE check: no theory change,
and no ΛCDM input.

## Method
- **Errors:** per-cluster lognormal σ_i from the catalogue's own M_gas,500 bounds, (ln hi − ln lo)/2 (erass1_main.tsv
  columns 6/7 around column 5).
- **Mass-function slope α:** from the FULL eRASS1 catalogue on disk. Fit dN/d ln M_gas ∝ M_gas^−α to the counts above the
  histogram peak (the completeness turnover), in the redshift range 0.05–0.5. Empirical; no cosmology.
- **Eddington correction:** ln M_true = ln M_obs − α σ_i² (standard lognormal result for a power-law population).
- **Model rescaling (declared approximation):** each model's ΔΣ is rescaled by (M_true/M_obs)^s, with s the model's own mass
  slope. The law-type models use s = 0.47 (CFG687 T2 law slope); the plain law and the H-EX models use the same s. Data are
  unchanged.
- **Terciles:** re-binned by the corrected M_gas.

## Readings (canonical; models from stored work files)
For the plain law, CFG809 H-EX and CFG815 P, report the tercile A_MID before and after correction.
- **SELECTION EXPLAINS PATTERN** if, after correction, CFG815 P's tercile A_MID are monotonic in mass (non-increasing or
  non-decreasing within 1σ) where they were not before.
- **NOT EXPLAINED** otherwise.

Also report: α (with a bootstrap error), the median σ per tercile, and the median correction per tercile.

## Controls
- K1: with σ_i := 0, the tercile A values reproduce CFG815 exactly.
- MUTATE (separate outputs): shuffle σ_i across clusters, which must weaken the low-mass correction trend (report).

κ fitted; not theory closed.
