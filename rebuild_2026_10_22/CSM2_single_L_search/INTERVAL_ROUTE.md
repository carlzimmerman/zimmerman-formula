# Structural continuation after the operator preflight

The discrete AQ projection is linear in enclosed mass. `operator_001`
reproduces 40 original source curves to maximum relative max-norm error
4.83e-15; the 1%-corrupted twin fails. All 40 individual errors were separately
checked finite. NumPy emitted matmul floating-status warnings despite finite
results; stderr is preserved, and later interval code must explicitly check
finiteness. This test used B21 radius labels; final bounds need actual native R.

Let C be the actual covariance, W its inverse Cholesky whitening map, and T
the fixed four-column two-halo template. Let P project orthogonally off WT.
Then, without assuming likelihood monotonicity,

    chi2_constrained(m) >= min_b(real) ||W(y-m-Tb)||^2 = ||PW(y-m)||^2.

The inequality holds because unrestricted amplitudes include the original
nonnegative allowed amplitudes. On a branch-fixed interval, the compact
Burkert mass grid is componentwise nondecreasing with Sigma under the scale-
order argument in CSM1/heldout/MW_BURKERT_MONOTONICITY.md, including saturation
and constant exterior mass. Source solver bounds and numerical errors still
need validation over this new domain. The law-branch mass profile is fixed.

Bound each halo mass vector between endpoint vectors, then propagate boxes
through signed projection, stacking and whitening coefficients. For residual
coordinate intervals [li,ui], a valid lower score bound is

    chi2_constrained >= sum_i distance(0,[li,ui])^2.

Exclude an L interval only if this lower bound exceeds the unchanged law score
plus9. Handle every branch event, equality on the law branch, both continuation
operators and uncertain threshold enclosures. An inconclusive box is subdivided
or retained, never labeled excluded by interpolating chi2 between points.

Groups can be bounded separately: positive radial weights and the mass-order
argument bound log-sigma predictions on branch-fixed intervals. Residual and
finite-difference mass-slope boxes then bound sample standard error and the
systematic term without group-Z monotonicity. Include activation events at
all three masses M, M*10^.01 and M*10^-.01.

Next executable step: construct actual native matrices/inventory weights and
reproduce the free-nuisance score at saved CSM1 points. Then test one specified
interval with conservative error allowances before attempting a covering
certificate. This is an open route, not an all-L exclusion. A claimed cover
requires separate adversarial proof review and reproducible numeric evidence.

Completed native-matrix preflight:32/32 controls, independent normal-equation
review10/10. Proceed under INTERVAL_001_CRITERIA.md; no interval arithmetic
has yet been executed. Preserve conditional versus certified bounds.

interval_001 is complete (139 controls;8 review controls). Conditional lower
score569.531694>163.343463 on[3.75,3.751]; this is NOT a certified interval
exclusion. Next: establish justified outward-rounded root/mass and signed-dot
error bounds for this local test before any covering claim. If certification
is inconclusive, preserve that outcome and freeze a separate broader branch-
event inventory experiment; do not turn floating padding into a theorem.

Scalar root signs are now certified for saved binary64 coefficients
(root_sign_001,124brackets). Independent70-digit outer-mass review agrees.
Full local score remains conditional: next outward mass-vector enclosures,
then coefficient/signed-dot bounds. Do not treat scalar certification as a
certified interval score or omit the fixed-coefficient scope.

Endpoint mass enclosures complete: mass_enclosure_001 certifies all446524
fixed-coefficient coordinates. The old padding contains every enclosure.
Next freeze signed projection/stack/whitening dot enclosures with explicit
coefficient scope and numerical error budget; continuum column/branch and
coefficient-construction obligations remain before any full-score certificate.
