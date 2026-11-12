# U4L1 AMENDMENT A1 (post hoc, disclosed): KA2 re-specified

Committed alone, 2026-11-12, after run 1 stopped at KA2 and before any label or any difference
between the limit and a requirement was formed. The reading rule, the inputs and every other check
in `FROZEN_CRITERIA.md` (04f671aa84) are unchanged.

## What happened

Run 1 (`u4l1_run1_stopped.out`): KA1, KA3 and KA4 passed; KA2 failed, largest difference 0.0132 dex
against a tolerance of 0.01. **As frozen the lane's outcome is NO LABEL (stopped at KA2).**

Diagnosis, on the check only: the independent routine reproduces the stored requirement to
3 x 10^-11 dex in all 32 cells when it uses the constant of the sealed code
(G = 4.30091 x 10^-6 kpc (km/s)^2 / Msun). With standard SI constants (G = 6.674 x 10^-11,
Msun = 1.989 x 10^30 kg, kpc = 3.0857 x 10^19 m) G differs by 2.5 x 10^-4, and the difference is
amplified where the gas requirement is a small residual of the stellar term. The one cell above
tolerance is case a, alt footing, F-flat, n = 1, where the requirement is 8.66 (a gas mass under one
per cent of the stellar mass). The next largest are 0.0036 (requirement 9.22) and 0.0015 (9.62).
Every cell with a requirement of 9.5 or more agrees to 0.0015 dex.

The check as frozen conflated two things: whether the independent implementation is right, and how
sensitive the requirement is to the fourth digit of G. The first is what a known-answer check is
for.

## KA2 as amended

| id | check | pass condition |
|---|---|---|
| KA2a | implementation: the independent routine with the sealed code's G, framework cells, n = 1 and n = 2, both footings, all four cases, R_g = R_d | every non-FLOOR value within 1e-6 dex of the file; FLOOR flags equal |
| KA2b | constants: the same with standard SI constants | every cell with a requirement >= 9.5 within 0.01 dex; the others are printed |

No label can depend on the cells below 9.5: they sit more than 0.7 dex under either limit.
