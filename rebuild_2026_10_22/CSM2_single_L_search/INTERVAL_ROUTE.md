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


Original solver/scope audit completed:186 unchanged scalar solves at3 levels,
14run+10review controls, nine90digit selected root checks. All sampled solves
converge within nominal mixed log tolerance (max observed log error2.946e-15).
147callbacks return exact0 with tiny nonzero analytic residual; this is rounding,
not a demonstrated large error. Finite traces do not prove uniform libm/optimizer
coverage, so the original floating-evaluator bridge remains INCONCLUSIVE.
Version-matched source/license and observed binary fingerprints are published.
The fixed numerical law comparator covers all127nodes; the65 hybrid law-node
correction does not establish an analytic comparator upper. Next freeze
ANALYTIC_COMPARATOR_ROUTE.md. Prior conditional lower569.5338626095037 is not
upgraded. No real-L/global exclusion. Native finals remain7of9, pending4and6.


All-node analytic comparator checkpoint: comparator_001 reconstructs127nodes
and457327mass coordinates with exact ideal weights/certified fixed primitives.
All11run+9review controls pass, including all60 exact signed dots and65
independent90digit law values. The unchanged feasible-candidate upper is now
154.34346325076598. Reviewed hybrid lower569.5338626095037 still exceeds
upper+9=163.34346325076598 within the registered local analytic numerical-grid
scope on[3.75,3.751]. No new fit or regrade. Original floating solver/libm
continuum and globalL remain unresolved; no unqualified exclusion is claimed.
Next GROUP_INTERVAL_PREFLIGHT_ROUTE.md targets actual189group cells and the
changing variance/slope denominator, rather than assuming monotonic group Z.
Native inventory remains7of9, pending4and6.


Group preflight and first interval complete. Actual189cells/63groups reproduce
savedL3.5 Z2.003748352852046;14run+9review controls validate the positive native
quadrature and changing statistic. X53 coarse-column substitution differs by
up to0.258278% and is rejected. The separately frozen group_interval_001 has
9run+9review controls,378directed root signs and18independent70digit endpoint
velocities. Z is enclosed in[2.00347780276279,2.00398877201976] throughout
[3.5,3.5001], so the original absZ<2 necessary cut fails in the registered
analytic fixed-EPS/quadrature scope. No monotonicZ assumption or added fit.
Rounded source endpoints miss the narrow analytic boxes by at most4.885e-15dex;
this is recorded, not padded away. Original floating/globalL certification
remains open. Next GROUP_DERIVATIVE_ROUTE.md targets the actual statistic's
velocity/variance/slope derivatives and regional coverage with branch jumps.
Native completion remains7of9; pending4and6.


Local group derivative checkpoint: group_derivative_001 passes8run+8review
controls. On[3.5,3.5001], all189 velocity derivatives and the full changing
variance/systematic-slope statistic give Z' in[-.302567149462260,-.301119418216813].
Nine70-digit normalized-root/Richardson controls and full statistic recomposition
agree. This is local analytic fixed-EPS/quadrature scope only; the earlier
Z lower2.00347780276279 still fails absZ<2. No regional/global monotonicity,
original floating certificate or new physical fit. Next GROUP_REGIONAL_ROUTE.md
requires a separately frozen whole-region[2.62,3.5001] branch/derivative attempt,
retaining inconclusive bounds and all coverage holes. Native finals remain7of9,
with4and6 unfinished.


Whole-region group checkpoint: group_regional_001 completes16run+13review
controls on the unsplit canonical[2.62,3.5001] domain. All189 branches stay halo
and378compact-root signs are independently confirmed, but Z in[.8429465086,
4.9595703846] and Z' in[-293.3285751,233.3162002] are INCONCLUSIVE. The changing
variance/systematic slope is included. No regional failure or sign is claimed.
Prior local results stand. Next GROUP_SUBDIVISION_ROUTE.md requires a separately
frozen two-tile preflight of the fixed .01 uniform mesh, preserving all pending
and inconclusive coverage holes. No new physical fit or original floating/global
certificate. Native finals remain7of9;4and6 pending.


Fixed group mesh checkpoint: tiles0[2.62,2.63] and1[2.63,2.64] directly fail
absZ<2 throughout in the registered analytic native EPS/quadrature scope,
with Z lower2.284559831278903 and2.280304225351651. Both16run+13review sets
and2batch controls pass. Their Z derivatives are negative, but no sign is
extrapolated. GROUP_MESH_INVENTORY.json marks3of89tiles reviewed (including
prior tile88),86pending; whole-region/global/original floating scope remains
open. Next GROUP_MESH_CONTINUATION.md targets fixed tiles2and3 under new
frozen runnable criteria, with all holes retained.
Native final seed4 is now validated/copied: primary L_proxy9.1112209981,
c_f14.4959394876,995particles inside first crossing,1180steps. Inventory8of9
passes72completion checks; measurement_006_eight passes5controls and exactly
reproduces prior seven. Only6pending. No robust derivedL, ensemble or corrected
linked-T pass; the documented estimator instability remains unresolved.


Fixed mesh continuation: group_mesh_002 completes tiles2[2.64,2.65] and3
[2.65,2.66]. Both directly fail absZ<2 across their entire registered analytic
fixed native EPS/quadrature domains;16run+13review controls per tile plus2batch
controls pass. Exact enclosures and source hashes are in GROUP_MESH_002_REVIEW.md
and results. Inventory now5of89tiles reviewed,84pending. Derivative signs are
not extrapolated, original floating/globalL remains unresolved, and no new
physical fit was added. Next GROUP_MESH_003_ROUTE.md requires runnable criteria
for fixed tiles4[2.66,2.67] and5[2.67,2.68]. Native finals remain8of9;6pending.
