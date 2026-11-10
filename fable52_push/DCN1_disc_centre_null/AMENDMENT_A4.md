# DCN1 AMENDMENT A4 (post hoc; committed alone, after the first P1 / P2 local runs and before any graded P1 / P2 number)

TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Criteria d603f1703c; A1 0a6e46fb52; A2 15f6f993e4;
A3 f5e101ba9a.

## What was seen first

- **The first P1 run (stopped).** Six of 16 backgrounds, all five resolutions each. Every solve "converged" (relative
  residual < 1e-10) in 3-9 Picard iterations, from the interpolated global field.
  - The rates were erratic with resolution: on four of the six, Q_A turned positive at N_R 108-243, at e-folding times of
    1-25 Myr.
  - Negative D.P cells appeared and multiplied with refinement.
- **The first P2 run.**
  - Two backgrounds came out smooth and negative: canonical 9.4 has Q_A = -3.51e-29 s^-2 at every resolution.
  - The run then crashed. The initial-guess interpolation was asked for r below the global grid's first cell centre.
- **Cause 1: the residual's normalisation.** The residual was ||A Phi - rhs|| / ||rhs||. rhs includes the Dirichlet terms
  c_f Phi_b, and Phi_b carries the global potential's large constant offset, so ||rhs|| is dominated by that offset. The
  stopping test was therefore met with the interior barely moved off the initial guess.
  - That initial guess is a bilinear interpolation of the global field, so its D.P carries the global grid's cell kinks.
  - Those kinks are what grew with N_R.
  - KA4 and KA5 did not show it, because their initial guess is the exact solution.
- **Cause 2: the crash.** The interpolator's bounds error for the initial guess near r = 0.
- These runs are kept in the scratchpad, not graded, and quoted only here.

## The amendment

1. **Gauge.** Phi_b and the initial guess are shifted by the mean Dirichlet value. The physics does not change; only the
   offset goes.
2. **The residual becomes ||A Phi - rhs|| / ||src||**, src = 4 pi G rho_b V (the source alone). Tolerance 1e-10.
   Additionally, at least 10 Picard iterations, and the last update's max |delta Phi| must be below 1e-10 times the range
   of Phi_b over the boundary.
3. **The initial guess** clamps r to the global grid's first cell centre. The boundary data, at r >= L, are unaffected.
4. **KA4 and KA5 are rerun** under A4 and graded as under A3 (frozen tolerances on Q_A). P1 and P2 are then run from
   scratch. Nothing else changes: labels, rule, A3's quantities.
5. **Reported:** the iteration counts and the final update size per solve.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
