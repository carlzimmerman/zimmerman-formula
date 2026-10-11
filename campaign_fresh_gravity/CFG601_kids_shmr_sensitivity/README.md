# CFG601: KiDS SHMR sensitivity. Swapping Moster/Behroozi changes nothing; the leaked-fraction normalisation does (SENSITIVE)

κ = ½ is fitted. The footings (9.36e-11 / 1.13e-10, written can / alt) are never pooled. The cold energy's mass is still required. This is not a closed theory. Numbers come from `cfg601_shmr_sensitivity_results.json` and `cfg601_shmr_sensitivity.out`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (488e95c0c). **Script:** `cfg601_shmr_sensitivity.py` (about 20 s, nice 10; imports `../CFG600_native_catchment_kids/cfg600_common.py`). Nothing downloaded; no PM run; CFG536 not re-run (its swap is read from its committed JSON).
- **Where the SHMR enters:** the HOD leaked-satellite environment, the stripping mix of the own profile, and the rank-one covariance term. The law's own profile (baryons + r_ta,law) uses no SHMR.

## Results (K9 = the inner nine bins; census own profile; construction A; B agrees to ±0.004 in eps)
| variant | can eps (Z) | alt eps (Z) | can census chi2 / 15 | CARRIED label (can) |
|---|---|---|---|---|
| S0 base (CFG531) | +0.366 (4.0) | +0.241 (2.9) | 45.6 | MIXED/UNRESOLVED |
| S1 Moster alone | +0.366 (4.0) | +0.241 (2.9) | 46.8 | same |
| S1 Behroozi alone | +0.372 (4.0) | +0.246 (2.9) | 49.2 | same |
| S2 leakage × 0.5 | +0.441 (4.9) | +0.309 (3.8) | 71.0 | CARRIED BY EARLY TYPES |
| S2 leakage × 1.5 | +0.291 (3.1) | +0.173 (2.0) | 30.9 | same as base |
| S3 SHMR environment removed (bound) | +0.516 (5.9) | +0.377 (4.7) | 106.5 | CARRIED BY EARLY TYPES |

- **Swap: immaterial.** Moster vs Behroozi moves eps(K9) by ≤ 0.006 and the Z by < 0.1. CFG536's held-out Z is likewise identical for the two (Z +1.71 / +1.71, from its committed JSON).
- **Normalisation: material.** A factor 2 in the leaked fraction moves eps(K9) between +0.29 and +0.44 (can) and +0.17 and +0.31 (alt). It flips the alt K9 class (Z ≥ 3) at × 0.5 and the can CARRIED label at × 0.5. Frozen verdict: **SENSITIVE on both footings** (S2 × 0.5 changes the class or label).
- **The early-minus-late difference does not move** (Z +6.1 to +7.3 in every variant): the split is robust; only the overall amplitude and the "carried by" label depend on the normalisation.
- **Removal (bound only).** With no SHMR environment the shortfall grows (K9 Z 5.9 / 4.7) and the census chi2 is 106 / 88; CFG529 showed that environment is needed for validity, so this is a bound, not a competitor.
- **What fixes the normalisation:** the measured leaked fraction (0.1686, CFG519), validated in CFG529 (G2f passes). The ×0.5 / ×1.5 rows are therefore outside the validated environment; they show the sensitivity, they are not alternatives.

## Controls: 3/3 pass
K1: S0 reproduces CFG531's committed BASE eps and its CARRIED labels. MU1 (leakage × 3 must change the class or the census chi2 by ≥ 4): passes on every cell (chi2 45.6 → 40.9 etc.; the "≥ 4" threshold is my reading of "change", stated here). MU2 (SHMR removed must move eps by > 1 sigma): passes.

## Not said
This does not test the SHMR-dependent lens masses of the supply side (that is CFG600's lane, and the law's own profile has no SHMR). It does not say the data favour the framework.
