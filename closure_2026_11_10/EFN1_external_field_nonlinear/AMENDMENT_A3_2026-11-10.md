# EFN1 amendment A3 (2026-11-10): route W differentiates the face-averaged clock flux, not the upwind one; committed alone

Post hoc with respect to the criteria (98364c8d20), A1 (c3e466efbf) and A2 (a55fd19bd0). Committed before any graded
route-W row (R2-R4) and before any graded route-D run.

## What was seen first (code tests on R0 and R1, canonical expo log M_b 9.4, g_e = 0.1 a0; not graded grids)

- The leading discrete mode: lambda / Gamma_ref^2 = 0.679 (R0), 0.764 (R1); route L's maximum on the same grids 0.752, 0.867.
  The mode sits at the route-L maximum (R1: 0.885 r_e, 138.8 degrees) and only 3 cells exceed half its peak on either grid:
  the continuum edge at the grid scale, as the criteria's section 7 expected. Eigen-residuals 1e-12; left and right
  eigenvalues agree.
- With the right-hand side as route D integrates it (upwind n in the nonlinear clock flux), the stencil gave
  c3/Gamma = -1062 (R0), -1016 (R1), and a "SATURATES-W" reading with fixed points at |a| = 0.031. **This is an artefact.**
  The upwind cell switches when the perturbation's sign flips, so N(h y) - N(-h y) carries an h^2 term, and the odd stencil
  returns it divided by the step: c3's flux part was -1017 at step 5e-4 and -1.017e4 at step 5e-5 (it scales as 1/step).
  Without the n flux term the cubic part is 2e-6 and -1e-5 at the two steps (zero to stencil precision). The quadratic
  coefficient also depends on the choice: c2/Gamma = -0.0140 (upwind flux), +0.0035 (flux term off) at R1.
- So the frozen route W, applied to route D's upwind right-hand side, has no well-defined cubic part.

## The change (reading A3)

Route W differentiates the discrete right-hand side with the nonlinear clock flux taken as the face average,
(N0_f + (n_k1 + n_k2)/2) (pi_k2 - pi_k1)/d A, which is a polynomial in the perturbation (exactly quadratic). Everything else in
route W is unchanged (eigenpair, stencil, normal form, convergence rule, readings, M4). Route D keeps the upwind flux (its
nonlinear stabiliser) as frozen. The frozen route-W reading on the upwind right-hand side is reported (it is NO VERDICT: its
cubic part does not exist as a limit; shown by the step test, which RESULT.md repeats on R3).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
