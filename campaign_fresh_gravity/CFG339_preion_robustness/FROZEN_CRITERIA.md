# CFG339 FROZEN CRITERIA: robustness of CFG338's post-hoc candidate

**Candidate.** M_c = R_ind · M_b / f_b, with reading M (CFG4 T5 max bookkeeping) and profile P1 (CFG313 V2 collapse shape, truncated at the collapse radius r_f(z_f)). R_ind comes from CFG317's leaky-box metallicity estimate.

**Not blind.** The central combination (yield −0.2, z_f class values 8 / 3) was SEEN in CFG338: all five populations within 2σ. This lane tests only whether that survives the a-priori uncertainty brackets that already existed in the record.
- **CFG317's yield bracket:** log y_Fe/Z_Fe,sun = −0.5, −0.2, +0.1. The keys "−0.5", "−0.2" and "0.1" in its committed RIND.
- **CFG336's z_f brackets:** UFDs 6 / 8 / 10, the others 2 / 3 / 4. The index zsel = 0 / 1 / 2.

That gives 9 combinations, each run on both footings.

## Decision
A combination PASSES if all five populations (MW UFD, MW classical, M31 Collins, M31 LVD, LV field) are within 2σ on both footings, using the harness's own error budget.
- **ROBUST:** at least 7 of 9 combinations pass.
- **PARTIAL:** 4–6 pass.
- **FRAGILE:** 3 or fewer pass.

Also reported: which population fails, and in which direction, in the failing combinations.

## Controls
- The central combination reproduces CFG338's reported M|P1 row exactly.
- **MUTATE** (CFG339_MUTATE=1): R_ind is permuted across populations (seed 339). The pass count must drop.

## Note
A ROBUST result would make this a candidate mechanism for the UFD shortfall: original baryons set the cold share; today's baryons set the law. It would still need:
- (a) per-object loss factors, not population medians;
- (b) a derivation of why the cold share tracks the pre-reionisation baryons;
- (c) independent checks on systems the candidate was not tuned on.
