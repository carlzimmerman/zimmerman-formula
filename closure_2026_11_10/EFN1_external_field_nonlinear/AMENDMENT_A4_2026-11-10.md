# EFN1 amendment A4 (2026-11-10): what "no growth" means in KA-c; committed alone, before any graded run

Post hoc with respect to the criteria (98364c8d20) and A1-A3 (c3e466efbf, a55fd19bd0, 94c54483a9). Committed before any
graded route-D or route-W run.

## What was seen first (a code test on R1, not a graded grid)

The isolated twin of alt kuzmin log M_b 10.9 (external field off, same grid, region and seed as its 0.1 a0 twin), route D
to 30 e-folds of the twin's rate: no stop line; c(t) rose from 3.0e-4 to 3.5e-3 within 2 e-folds and then wandered between
2.6e-3 and 9.6e-3 to 30 e-folds, with its maximum always in the off-plane cells next to the static plane rows
(theta 89.8-90.2 degrees, 0.42-1.04 r_e). max |v| stayed 2-5e-3 km/s. The leading discrete eigenvalue of this twin (R0 test)
is 2e-12 Gamma_ref^2 (the constant-pi zero mode of the closed region). So the isolated twin does not grow, but the seed's
oscillation collects next to the plane wall, and the frozen line "c(t) <= 2 c(0) to t_end" fails for a reason that is not
growth.

## The change (reading A4)

KA-c's route-D line becomes: **no exponential growth**, i.e. the log-linear fit of c(t) over [2, t_end] e-folds has a rate
<= 0.1 Gamma_ref, and max c(t) over the run stays <= 0.1 (the perturbation stays linear). The eigenvalue line (Gamma^2 <=
1e-3 Gamma_ref^2) is unchanged. The frozen line (c(t) <= 2 c(0)) is reported beside it. RESULT.md also reports, for every
external-field run, where c(t) peaks (next to the plane wall or in the negative-D.P shell), so the wall's share of any
outcome is visible.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
