# SAT1 AMENDMENT A1 (2026-11-12, after run 1, before any label was printed)

## What happened

Run 1 stopped at KA1: the mean of M_app over 200,000 isotropic random mu (seed 7) at 200 kpc,
canonical, was 5.3004e11 against the quadrature 5.2642e11 (+0.69 per cent; criterion 0.5 per cent).
All other checks passed (KA2 parallel +0.5761, perpendicular +0.0137; KA3; KA4 SI agrees to better
than 1e-5; KA5 35 primary rows; KA6). No label was printed. Output kept as
`sat1_run1_KA1_failed.out`.

## Why

The check was mis-sized, not the formula. At 200 kpc the direction-dependent apparent mass runs
from -28.6e11 (along the field) to +35.2e11 (opposite), so its standard deviation over isotropic
directions is 18.24e11 and the Monte Carlo standard error with 200,000 draws is 0.041e11 = 0.77 per
cent of the mean. The run-1 offset is 0.89 standard errors. A 0.5 per cent tolerance needs about
10^7 draws.

## Change

KA1 uses 20,000,000 isotropic draws (same seed 7; standard error about 0.08 per cent). Tolerance
unchanged (0.5 per cent against 5.264e11 and against the quadrature). The script prints the Monte
Carlo standard error. Nothing else changes.

## Consequence recorded now, before the labels

The same arithmetic applies to the satellite bins: with a spread of order +-30e11 per satellite
around a mean of about 5e11, the bin ratio R_mean from 10 to 25 satellites is dominated by the
dipole (odd-in-mu) term and carries a sampling scatter of order the ratio itself. The frozen
leave-one-out FRAGILE rule and the bootstrap interval are what report this; they are unchanged.
