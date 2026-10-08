# CFG434: void lensing vs a smooth unsettled reservoir (door 8, open piece 5)

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 7caa5042c. Script: `cfg434_void.py` (seconds, numpy only). Outputs: `cfg434_void.out`, `cfg434_results.json`; MUTATE: `cfg434_void_MUTATE.out`, `cfg434_results_MUTATE.json`. Data: `../../../_external_data/cfg434_work/` (see FETCH_LOG.md). The data are the published UNIONS x BOSS void-lensing fits (arXiv 2507.13450v2, Table tab:fit_stats), not a new catalogue cross-correlation.

## Verdict (frozen rule, Full catalogue, REF-C)
**SMOOTH RESERVOIR CONSISTENT under reading I, DISFAVOURED (2.9 sigma) under reading II.** This is not a clean fork: reading II's smooth case is DISFAVOURED, not EXCLUDED.

Plain reading: BOSS voids lens at A = 0.81 +- 0.13 of the LCDM expectation, given how empty they are in galaxies. That matches LCDM, including the known void-selection inflation of tracer bias.
- **Reading I (piece 5's wording; CFG363 anchored row):** the clumped matter already carries LCDM contrast, and the reservoir is extra mass on top. Then the reservoir must be smooth at the void scale (50-85 Mpc). A clumpy reservoir is EXCLUDED (3.4 sigma at its most favourable corner). The bound on the reservoir's void-scale clumpiness is b_u <= 0.59 (most lenient corner) down to b_u <= 0.08 (most stringent). Void lensing therefore agrees with piece 5, and the voids' 50-180 Mpc reach is exactly the scale piece 5 names.
- **Reading II (the reservoir is part of the cosmic matter share):** a smooth reservoir would make voids too shallow. The prediction is A = 0.19-0.45, against 0.81 measured (2.9 sigma at the most favourable corner). The reservoir must then trace matter at b_u >= 0.21 (lenient) to >= 0.62 (stringent). That is a reservoir that clusters like CDM on 50+ Mpc scales.

The reservoir's void-scale contrast b_u **cannot be predicted without a new free parameter**: nothing on the record fixes how clumped the unsettled fluid is at 50 Mpc. So the lane reports the bound on b_u (above) per reading, as the brief asked.

## Key numbers
| quantity | value |
|---|---|
| b_Vg (Full, UNIONS x BOSS) | 2.47 +- 0.36 |
| b_ref REF-C = f(0.467)/0.37 (LCDM, fiducial Omega_m 0.307) | 2.009 |
| A_obs = b_ref/b_Vg (Gaussian in 1/b_Vg, +5% on b_ref) | 0.813 +- 0.125 |
| eps = reservoir share of matter contrast (f_u 0.65-0.90 x 5.364/6.364) | 0.548-0.759 |
| R_sel (LCDM void-selection bias inflation) | 1.00-1.25 |
| LCDM A = 1/R_sel | 0.80-1.00: min abs z = 0.02, CONSISTENT |
| reading I smooth / clumpy | z -0.02 CONSISTENT / -3.39 EXCLUDED |
| reading II smooth / clumpy | z +2.88 DISFAVOURED / -0.02 CONSISTENT |
| power check (smooth-vs-clumpy gap 0.438 vs 2 sigma 0.251) | PASS |

## Robustness (reported, not decisive)
| row | A | reading I smooth | reading II smooth |
|---|---|---|---|
| LOWZ | 0.75 +- 0.15 | -0.33 CONS | +1.96 CONS (edge) |
| CMASS | 0.83 +- 0.19 | 0.00 CONS | +2.01 DISF |
| Small voids (50 Mpc) | 0.71 +- 0.16 | -0.57 CONS | +1.67 CONS |
| Large voids (85 Mpc) | 0.73 +- 0.15 | -0.48 CONS | +1.78 CONS |
| REF-L (Sugiyama ratio; tests scale dependence only) | 0.74 +- 0.11 | -0.57 CONS | +2.50 DISF |
| Gaussian in b_Vg instead of 1/b_Vg | 0.81 | -0.02 CONS | **+5.18 EXCL** |
| R_sel = 1 only | 0.81 | -1.49 CONS | +2.88 DISF |
| DES Y1 (Fang+2019, figure only) | b_slope slightly above the large-scale bias, under 2 sigma: A < 1, same direction | | |

- Reading I's smooth case passes in every row.
- Reading II's smooth case sits at 1.7-2.9 sigma in every row, and at 5.2 sigma if the errors are taken as Gaussian in b_Vg. The declared choice, Gaussian in 1/b_Vg, is the conservative one, because the fit is linear in 1/b_Vg.
- No single sub-catalogue reaches 3 sigma on its own.

## Verify the fail as hard as the pass
- **Reading II's tension rests on the clumped matter having the LCDM fluctuation amplitude.** A smooth reservoir would suppress the clumped component's own growth, but the framework's phantom would boost it, and no committed run fixes the net amplitude. Reading II smooth reaches |z| <= 2 only if the clumped matter's amplitude exceeds LCDM by >= 25%. It matches fully only at x1.8. The record's own T5 over-growth (sigma8 x1.21-1.26, CFG361) sits at that threshold. So reading II smooth is **borderline, not excluded**, if the clumped growth is over-built.
- REF-C's b_ref uses LCDM f(z) and the fiducial beta = 0.37 (chosen to match the fiducial cosmology, not measured). It agrees with the lensing-anchored REF-L to 10% (C2).
- R_sel (1.00-1.25) is taken from the data paper's citations (Pollina+17, Nadathur+19b). It is the dominant systematic for reading I's clumpy exclusion: at R_sel = 1.25 the clumpy case is still -3.39.
- The test is one amplitude on a published stack, with no profile-shape or covariance re-analysis. The HSW fits in the data paper are marginal for LOWZ (chi2/dof 20.2/9).

## Controls
- C1: b_ref(Full) = 2.009, inside [1.9, 2.1]. PASS.
- C2: REF-C vs REF-L agree to 10.6%. PASS.
- C3: limits exact (eps -> 0, and reading II at b_u = 1, both equal LCDM). PASS.
- C-POW: PASS.
- C4: LCDM CONSISTENT.
- **MUTATE** (A_obs replaced by reading II's planted smooth value, 0.308): reading II smooth -> CONSISTENT (z 0.00), reading I smooth -> EXCLUDED (-3.93), headline flips to BOOKKEEPING FORK. Detected, rc 1.

## What this does NOT say
- It does not say the data favour the framework. LCDM is CONSISTENT, and reading I simply reproduces LCDM in voids.
- It does not test the CMB-lensing over-lensing of CFG363. It tests only the void-scale contrast.
- kappa = 1/2 is fitted. The cold fluid's mass is still required (no dark-matter particle is added). The reservoir's clumpiness b_u is a new free parameter, bounded here, not derived.

## FORWARD NOTE (2026-10-08, data audit)
The "borderline" escape for reading II needs clumped growth at least 25% above ΛCDM. The adopted zero-knob growth rule (CFG424/425/439) gives σ₈ at most 0.54% above the control and cancels the phantom inside each catchment, so the escape is not available under candidate B as now specified. Reading II's smooth-reservoir case therefore stays **disfavoured, 2.9σ under the frozen error model** (5.2σ under the alternative error model). This weakens reading II of the reservoir, not the growth result. See AUDIT_data_and_assumptions_2026-10-08/.
