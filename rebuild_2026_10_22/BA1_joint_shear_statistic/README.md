# BA1_joint_shear_statistic: a joint χ² for the 15 shear keys changes two reads: MA1 at z_obs is a joint pass, and so is NZ1 on one gas scale at z_obs

Criteria: `FROZEN_CRITERIA.md` (83f8fbb8cb), committed alone first. `ba1_grade.py`, `ba1_worker_tail.py`, `ba1.out`, `ba1_results.json`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework. The per-key |Z| ≤ 2 gate stays as frozen; this sits beside it.

**Headline: worse h cell, one template, 15 modes.** p from χ²(15). Lines: JOINT PASS p ≥ 0.05, JOINT FAIL p < 0.01.

| Rule, gas scale | f★ 0.034: χ², p | f★ 0.0615: χ², p | keys over 2 | jackknife R: p | class |
|---|---|---|---|---|---|
| FC1, eRASS1's | 13.0, 0.60 | 14.4, 0.50 | 0, 1 | 0.19, 0.12 | PASS |
| **MA1, eRASS1's** | **9.5, 0.85** | **10.1, 0.81** | 0, 0 | 0.48, 0.40 | **PASS** |
| MA1 at z_obs, eRASS1's | 15.5, 0.42 | 17.2, 0.31 | 1, 2 | 0.094, 0.051 | PASS |
| NZ1, eRASS1's | 58.1, 5e-7 | 54.5, 2e-6 | 5, 4 | | FAIL |
| MA1, X-COP's | 36.3, 0.0016 | 42.2, 2e-4 | 7, 9 | | FAIL |
| MA1 at z_obs, X-COP's | 57.2, 8e-7 | 65.3, 3e-8 | 9, 11 | | FAIL |
| NZ1, X-COP's | 27.1, 0.028 | 24.5, 0.057 | 2, 2 | 0.0014, 0.013 | MARGINAL, PASS |
| **NZ1 at z_obs, X-COP's** | **24.3, 0.060** | **22.3, 0.099** | 3, 3 | 0.014, 0.026 | **PASS** |

## How this reads
1. **MA1's redshift miss is one key in a good fit.** At z_obs it misses per key on G-IN-Mall (−2.33), the band with the failing cross-shear null, and the joint χ² stays at 15.5 for 15. So "redshift takes MA1 back" was too strong as a statement about the fit, though the frozen per-key gate does fail.
2. **NZ1 on one gas scale at z_obs is a joint pass and an X-COP pass.** It's the only rule so far with both. It still misses G-OUT-M3 (+3.69 / +3.41) and G-OUT-Mall per key, and the sky-patch jackknife R is harsher (p 0.014, 0.026, MARGINAL). Groups fail if zoom r₀ goes on every path.
3. **χ² without the two INNER keys barely moves any class,** so the failing band isn't what's deciding these.

## Checks
K1 R = I gives Σ Z², |d| 0. K2 common bootstrap sd against each key's s: median 0.997; the INNER keys read 0.27 and 0.34 because their s holds the cross-shear term, as designed. K3 draws: mean χ² 14.97 for 15, p < 0.05 in 0.051. MUTATE d × 2: χ² × 4.000000.

## Limits
Correlations come from f★ 0.034 at each gas scale and are applied at both f★. The joint test can't see a shift along a low-eigenvalue mode well; R's smallest eigenvalues are 0.03–0.06. Bootstrap and jackknife disagree by up to a factor of ten in p on the marginal rows; I've kept the frozen bootstrap as the headline and report both.
