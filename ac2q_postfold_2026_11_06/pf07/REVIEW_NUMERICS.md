# Independent PF07 numerical architecture review

Reviewed against criteria base 48c08b18e5. No implementation changes and no
new evolution runs. I inspected the four requested modules, CONTRACT.md,
PROJECTION.md, DEALIAS_CONTRACT.md, and existing t=.5 outputs. A small
single-thread read-only probe reconstructed their constraint residuals.

**Outcome:** no algebraic error found in the adapted coordinate or its chain
rule. Padding is a legitimate consistency strategy, with no added physical
viscosity. The projection diagnostics need stronger accounting, and the
current validation does not exercise the padded wrapper. Existing saved
t=.5 states pass the independent raw momentum check below; therefore the
diagnostic concern does not invalidate those states.

## Coordinate equivalence

Here the code's M means Mpl^2, not Mpl. With

    S=2 beta_xx+3 beta_x^2,
    c=2 M^2 exp(4beta)/p_lambda,
    p_beta=r+cS,

the kinetic contribution to h is

    (p_lambda^2-2 p_lambda r)/(4 M v^2)
      -M exp(-2lambda)S, v=exp(lambda+2beta).

It cancels the spatial-curvature contribution exactly. The implementation's
algebraic h is correct. Because c has no lambda dependence,

    rdot=p_beta,dot-c(4 beta_dot-p_lambda,dot/p_lambda)S
          -c(2 beta_dot,xx+6 beta_x beta_dot,x)

is the exact chain rule, including at finite collocation size when the same
derivative matrices define the coordinate transformation. The initial
beta=0 state has r=p_beta, so the initial conversion is also correct.
The transformation is only valid while p_lambda stays away from zero;
the explicit 1e-6 guard acknowledges this coordinate limitation.

Projection and Fourier truncation do not commute with this nonlinear
coordinate change. Thus the projected/padded method is a consistent
candidate discretization of the same continuum equations, not exactly
the original canonical finite-dimensional ODE in renamed variables.
At finite resolution its canonical reconstructed derivatives can differ
by the derivative of the constraint projection. Those corrections should
be measured and shown to decrease, not assumed to vanish identically.

## Projection: correct equation, incomplete reporting

The Newton residual is

    D_x p_lambda-beta_x(r+cs/p_lambda)+(mean(p_lambda)-target),
    cs=2M^2 exp(4beta)S.

Its Jacobian has the implemented positive diagonal term
beta_x cs/p_lambda^2. This is correct. Adding the mean equation this way
does not enforce the mean and compatibility independently: a constant
unaugmented residual can balance a mean shift. The subsequent unaugmented
1e-8 residual check is essential and is present. Report the mean shift
and mean(beta_x p_beta) separately when claiming preservation of the mean.

Let E prolong to the fine grid, R restrict, and Pi_f be the fine momentum
solve. The padded step projection is R Pi_f E, which is not generally
idempotent and need not leave the restricted state exactly constrained.
The diagnostic and RHS reproject Pi_f E y. They therefore report the
reconstructed fine-state momentum residual, not the saved state's raw
residual. This can conceal significant projection corrections in a less
resolved run. Record all of:

* coarse and prolonged raw momentum residuals before projection;
* the fine projection correction and its retained/discarded Fourier parts;
* the difference between one and two padded projections;
* momentum mean compatibility and mean p_lambda change;
* projection corrections at stages as well as accepted endpoints.

The chain-rule concern is quantitative: if projection changes the actual
p_lambda time derivative, reconstructed p_beta gains the associated
coordinate derivative even though r is held fixed. Small corrections and
refinement establish whether this is harmless truncation error.

## Independent check of existing final states

I read `padded31/result.json` and `padded63/result.json`, reconstructed
p_beta=r+cS directly without a momentum solve, then compared with
Pi_f E y. Single-thread NumPy/SciPy execution used
OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, VECLIB_MAXIMUM_THREADS=1.
No evolution was rerun.

| Quantity at t=.5 | n31 | n63 |
| --- | ---: | ---: |
| raw coarse momentum maximum | 1.24755e-9 | 1.08482e-11 |
| raw prolonged momentum maximum | 1.28308e-9 | 1.98337e-11 |
| after fine projection | 6.70226e-14 | 1.49065e-13 |
| maximum fine projection correction | 6.50119e-13 | 3.58047e-15 |
| maximum padded-state correction | 2.49800e-16 | 4.16334e-16 |
| maximum repeated-projection difference | 2.77556e-16 | 4.44089e-16 |

The raw residuals are small and decrease strongly with spatial resolution.
There is no evidence of a large projection correction stabilizing these
particular endpoint states. This endpoint test does not bound earlier RK
stage corrections or later runs.

For reproducibility, the raw residual evaluated in the probe was exactly

    max(abs(system.dx(pl)-system.dx(b)*
      (r+2*system.M**2*exp(4*b)*(2*system.dxx(b)+3*system.dx(b)**2)/pl)))

on the saved coarse state, its `s.lift(y,s.fine.n)` prolongation, and the
fine projected prolongation. Corrections were ordinary maximum vector norms.

## Padding, truncation, and action

For odd input and output grids, transfer's FFT normalization and centered
mode placement are correct. Prolongation preserves every represented
coefficient; restriction removes coefficients above the retained cutoff
without damping retained ones. This is explicit spectral truncation, not
an added physical viscosity or a postshock prescription.

However, three-times padding is not exact Galerkin evaluation of this
nonpolynomial constrained RHS. Exponentials, reciprocals, the logarithmic
hold law, and nonlinear constraint inversion generate arbitrarily high
modes. The absolute-value hold law also has only finite differentiability
at P=0. A fixed factor suppresses rather than proves elimination of all
aliasing. A small same-state RHS/constraint comparison at factors 3 and 5
would test the remaining quadrature error cheaply. State and timestep
refinement remain necessary even after the eigenvalue improvement.

The implementation also solves the auxiliary constraints on the fine grid,
then truncates their effect on the evolved variables. Calling this
"padded pseudospectral evaluation with constraint reconstruction" is more
precise than claiming an exactly variational Galerkin discretization.
No new term was inserted into the continuum action; nevertheless finite-
resolution conservation is not guaranteed simply because padding was used.

## Missing checks and stopping details

1. `evolve_padded.py` imports `validation()` from evolve_projected. Those
   controls instantiate the unpadded System and never exercise transfer,
   the padded projection, or padded RK evolution. Add direct padded FRW
   and odd-grid transfer round-trip controls. The existing controls remain
   useful but are not padded-implementation validation.
2. The frozen contract asks for transformed-versus-canonical RHS and linear
   benchmark checks. The coordinate algebra passes this review, but these
   tests are not part of the executable validation function. Preserve a
   direct numerical smooth-state comparison if one is used as evidence.
3. Only q's tail controls the underresolution stop. Other evolved fields
   and reconstructed p_beta can have high modes while q remains smooth.
   Record tails of beta, r, p_lambda, reconstructed p_beta, and preferably
   lapse/P, especially their derivative-weighted tails. Current q-tail
   sampling is correctly relative to the coarse cutoff after the initial
   record; the initial diagnostic still uses the fine-grid cutoff.
4. The gauge variable in diagnostic is computed but neither converted to
   a gauge-equation residual nor reported. Odd grids remove the even-grid
   Nyquist obstruction, but reporting the actual gauge residual is cheap.
5. The projection divides by p_lambda before fields applies its coordinate
   guard. Add a finite/nonzero check and explicit Newton convergence
   reporting inside projection for robust failure classification. This
   review did not observe that failure in the saved runs.
6. Branch, X, charge, cap, polarization, and endpoint momentum checks are
   present. Accepted endpoints must also pass raw-state/reconstruction
   checks above; reporting only the postprojection residual is insufficient
   as a general convergence diagnostic. Projection corrections are a
   discretization diagnostic, not an automatic physical failure.

## What the existing success establishes

I verified that n31, n31 half-step, and n63 outputs report completed t=.5.
Their q_min values are respectively .00752422279498, .00752422280543,
and .00752422270060; q tails are 2.19e-10, 2.19e-10, and 2.25e-16.
This and the independent raw momentum probe support a regular short-time
numerical continuation. They do not alone establish full field/gradient
convergence or correct shock selection. Matched-time comparisons must
include physical reconstructed quantities, constraint/projection error,
space and time refinement, and the nonpolynomial padding sensitivity.
Small initial Jacobian real parts are evidence about the aliasing hypothesis,
not a nonlinear stability theorem.

## Exact reviewed code revisions

SHA-256 at inspection:

    evolve_adapted.py 4b7d0cfbaf8415d59d442c5c7cc3fe7b558ea9684db24f37bd3424d7b7a1805d
    evolve_projected.py c5191bfa2eca52e24f3150ac6ce4bd2a06454abf831822d82d9563dbd548b9a0
    dealias.py 43f348bc89be51700f330d932ffcb44a8dcf8a1f57a7f438176e2795ff263b24
    evolve_padded.py 1a21280c291a5516ee7e840dcdbd51b5d83538963c6764399fb428b2dbc9a70d

Review provenance: independent delegated numerical/code review, 2026-11-06.
