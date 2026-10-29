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

Signed fixed-map dot/stack score enclosures completed: signed_dot_002_cached.
Original likelihood remains uncertified. Next DUAL_ROUTE.md eliminates the
approximate nuisance/whitening map with an exact covariance dual witness;
projection/column/branch/continuum assumptions remain explicit.

Exact covariance nuisance dual is complete (exact_dual_001). Conditional
lower569.5338658431842 exceeds exact feasible-law upper+9. No floating Q
required. Next close native-box membership: source projection coefficient
construction/anchor consistency, then column/branch/continuum enclosure.

Projection/anchor fixed-primitive enclosures completed (projection_anchor_001),
432120coefficients,60/60anchor coordinates contained. After derived error
inflation exact dual lower remains569.5338657853632. Original floating-source
forward error and column/branch/continuum coverage still need closure; fixed
primitive tables alone are not a real-L certificate.

source_forward_001 bounds reviewed projection floating evaluation for covered
mass arrays. Conditional dual lower remains569.5338648476735. Next address
nonlinear mass construction, original catalogue interpolation/stacking and
column/branch/continuum coverage. Implementation/IEEE assumptions remain
explicit; no full real-L certificate is claimed.


Catalogue stacking checkpoint: catalogue_001 bounds original per-lens
interpolation/weighted normalization against the saved map for all181431
lenses. Exact ideal weight L1 discrepancy<=1.914797023e-15; derived maximum
stack error2.607694418e-7. All29 run+16 exact-review controls pass. The unchanged
exact dual lower after this budget is569.5338626102013, above feasible-law
upper+9=163.34346325076024. Floating-status warnings are preserved; returned
stress values and all output bounds are finite. Implementation/covered-mass
assumptions remain, so this is not a real-L exclusion. Next close original
nonlinear mass/column/branch/continuum membership under NONLINEAR_DOMAIN_ROUTE.md.
Native finals remain5of9; source/copy hashes agree and pending checkpoints are
recent. No new seed set or aggregate NL1 grade is published.


Original-input nonlinear checkpoint: nonlinear_001 rebuilds coefficients from
EM1/F3/X43/A2 inputs rather than saved M,R,Sigma. All127 branches and124 compact
root brackets pass, but new mass enclosures extend outside351824of446524 old
endpoint coordinates (max0.000929490Msun). Independently,102of620 high-precision
point masses miss an old box; all620 are in the new boxes. Analytic law vectors
also differ from saved rounded vectors (max24.199471Msun). These are numerical
input-domain differences, not observational failures or new physical fits.
137run+8review controls pass. The earlier569.5338626102013 lower is conditional
on old boxes and has NOT been extended to these original-input enclosures.
Next propagate new signed-delta/law/envelope budgets under
NONLINEAR_PROPAGATION_ROUTE.md. Original floating solver/libm/continuum behavior
remains open; no real-L/global exclusion. Native completion remains5of9.


Original-input domain propagation is complete: new halo delta and65 law
profiles are covered by derived relative perturbation3.257642253e-15 and
envelope scale1.0000000000000033. Exact review strengthens the main budget to
cover exported outward arrays. All15run+9review controls pass, including
exhaustive223262halo/234065law checks and325independent70digit law values.
The reviewed conditional dual lower569.5338626095037 remains above
163.34346325076024. This now includes the original-input analytic correction;
original floating solver/libm and likelihood interpretation still need the
SOURCE_SOLVER_BRIDGE_ROUTE.md audit. No real-L/global exclusion yet.

Native seeds2and5 completed and are published with snapshot/done/final-log
integrity. Inventory7of9; only4and6 pending. Unchanged primary L proxies:
seed2=5.8050015757 (2885inside),seed5=6.2966399752 (1340inside).
measurement_005_seven passes5controls and reproduces prior five exactly.
Seven primary ok flags do not establish robust derived L, a convergence
claim or a corrected linked-T pass; binning instability remains unresolved.
