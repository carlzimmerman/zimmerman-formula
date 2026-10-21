# CFG936 AMENDMENT A1: an extra condition in the K3 code is dropped (control code only, not physics)

- **Date:** 2026-10-20.
- **Timing:** POST HOC. Written after the first K-only run (`CFG936_MODE=K`), and committed alone before the script is
  changed. Frozen criteria: 71d010099.

## What had been seen when this was written

The K-only run prints only K numbers. These are reproductions of record values:
- CFG931's TDG means, −0.6904 / −0.7276;
- CFG933's DF2/DF4 E_obs and z;
- CFG763's τ_min,95 bracket;
- CFG768's f_cap and Z;
- CFG7's C2 deviations;
- CFG804's N;
- the K7 limits.

No S1 mean, se or class was computed, and no route prediction, residual or class either.

## What failed

K3 printed max |diff| 0.0 for every frozen sub-check:
- τ_min,95 and χ²_min at −1σ and nominal ages, both footings;
- CFG763's K1 χ² (34.018 / 40.290 and 1.105);
- the upper bound 3.4744 → 3.47.

K3 still reported FAIL. The script's pass condition carried one extra clause that is **not in the frozen K3 text**:
`CFG4_common.A0 == the rounded footings`.

## Why

CFG4_common.A0 holds the unrounded FP0 values:
- canonical 9.360324825027975e-11;
- alt 1.1312035414413022e-10.

These sit 2.5e-16 and 3.5e-16 m/s² above 9.3603e-11 and 1.1312e-10, a relative 2.7e-6 and 3.1e-6. CFG4_common itself asserts
agreement only to 1e-15. CFG763 ran on those unrounded values, and K3's reproduction uses them exactly as the frozen text says
("CFG4_common.nu_mono and CFG4_common.A0"). The extra clause was a coding slip.

## Change (and nothing else)

- The clause is removed from K3's pass condition.
- The two differences are printed and stored in the K3 record.
- The main run uses the exact rounded footings, as the criteria require everywhere outside K3 (D-ii: "ν_e at the exact
  footings").
- The 3e-6 relative difference from CFG763's a0 is reported beside the D-ii numbers.

Nothing else changes: the criteria, estimators, classes, corners, variants, the other K tests and MUTATE are as frozen.

κ = ½ FITTED; footings never pooled; not theory closed.
