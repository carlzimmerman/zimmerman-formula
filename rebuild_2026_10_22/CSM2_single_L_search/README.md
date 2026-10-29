# CSM2: single-L search and native estimator stress test

The target remains open: one consistent L passing the fixed corrected model's
unchanged observational criteria. No fitted parameter has been added. See
`TARGET.md` for the predeclared portfolio and finite grid.

## Completed finding: native crossing instability

Changing only radial edges exposes an earlier descending -2 crossing in two
of the three completed ng64 profiles. The prescribed first-crossing rule then
selects a different feature:

| Seed | c_f, 21 edges | c_f, primary 25 edges | c_f, 29 edges |
|---:|---:|---:|---:|
|3|3.010853|3.138159|16.803760|
|7|2.426993|2.441598|11.798147|
|8|4.068233|4.010123|4.038780|

All tested binnings pass the original synthetic c=4 control. That benchmark
and the `ok` flag alone therefore do not establish robustness on these profiles.
Independent reconstruction reproduces the original selected radii and shows:

- Seed 3: 29-edge crossings at 7.89 and 41.69 kpc, compared with one primary
  crossing at 42.27 kpc. The extra inner crossing encloses 541 particles.
- Seed 7: 29-edge crossings at 11.68 and 56.06 kpc, compared with one primary
  crossing at 56.45 kpc. The extra inner crossing encloses 984 particles.
- Seed 8 has one crossing near 33 kpc under all three tested binnings.

This does not identify which feature is physically correct or justify choosing
the outer crossing to restore a preferred L. The original primary results
remain unchanged. Their L proxies 1.972/1.535/2.521 are conditional partial
measurements, not a robust derivation. The 29-edge fixed-reference proxies
are diagnostics, not alternative recalibrated L estimates: the entire ng48
reference was not refit under each variant.

Paired ng64/ng48 c_f ratios for seeds 3/7/8 are 0.438/0.457/0.307. Multiplying
by 7.31 gives paired diagnostics 3.201/3.343/2.241; these do not replace the
prescribed ensemble-reference normalization. They show why seed variation and
resolution transfer need separate checks.

`native_diagnostic_001/` passes 4/4 controls, including reproduction of cached
ng48 and published ng64 measurements. `crossing_002/` independently reproduces
all nine profile variants with 3/3 controls. Both have bounded manifests,
input hashes, scripts, raw results and pre-computation criteria. Neither a raw
simulation nor an old measurement was changed.

The first crossing run's inherited contract text incorrectly described six
snapshots although its actual hashed inputs were the three ng64 snapshots.
That metadata record is retained in `crossing_001/`. A corrected-description
contract and fresh `crossing_002/` reproduce its scientific JSON byte for byte;
the corrected run is authoritative for this diagnostic.

## Completed necessary-constraint search: no survivor among 15 levels

`run_001/` completed with 6/6 source controls, peak RSS 0.676 GB and runtime
822 seconds. Its group-only reduction and lens score reproduced full CSM1
before new cells. The fixed grid has **no canonical necessary-test survivor**:

- Nine points from the seed-8 proxy L=2.520507 through L=3.5 fail groups.
  At the endpoints, Z=2.5143 and 2.00375; the unchanged limit is |Z|<2.
- Six points L=3.625,3.75,3.9,4.0,4.5,5.0 pass groups but fail lensing:
  delta-chi2 versus the law is +411.09,+415.28,+420.31,+423.23,+432.05,+437.33,
  against the allowed +9. No other criterion can rescue a failed necessary cut.

`reconciliation_001/scores.csv` has signed values on both footings, and its
JSON independently checks grades, actual flags and the exact L^(5/4) scaling
of columns against the validated baseline. The lower observed proxies for
seeds 3 and 7 are already below the actual canonical LG activation threshold;
the unchanged fixed UFD class is on its failing law state (Z=5.2166).

This excludes these finite levels only. It does not rule out every real L,
change the sampling criteria, or establish a robust native estimate. A viable
point found later must still pass all remaining full criteria. See
`CONTINUATION.md` and `INTERVAL_ROUTE.md` for the unresolved continuous question.

## Completed structural preflight

The explicit discrete lensing projection operator matches the original on 40
profile/tail/radius cases to maximum relative max-norm error 4.83e-15. Every
individual error is finite. A 1%-corrupted operator fails the same check.
Evidence: `operator_001/` and expected-failed `operator_002_MUTATE/`, with frozen
criteria and bounded manifests. This verifies a linear map needed to propagate
interval mass bounds; it is not an L exclusion. `INTERVAL_ROUTE.md` derives
the proposed lower-score bound and records the remaining native-matrix,
branch-event, source-solver and numerical-error obligations.


Native matrix checkpoint: `native_matrix_001/` completes the next structural
preflight (32/32 controls). Actual native radii, full covariance, four two-halo
templates and catalogue interpolation weights reproduce saved CSM1 at
L=3.75,3.9,4.0 on both footings. All181431 lenses reduce to127 positive-weight
nodes. The native projection identity passes24 cases (max error5.15e-15).
Free-amplitude projection matches independent least squares; a separate normal-
equation review agrees to1.26e-12. At alternate L=3.75 the unrestricted first
amplitude is negative: its lower score547.638 differs from the constrained
547.679, confirming why the interval route needs an inequality. A1% covariance
corruption breaks score reproduction. No new model pass or continuous-L
exclusion is claimed. `INTERVAL_001_CRITERIA.md` now freezes the first local
interval [3.75,3.751]; implementation and enclosure validation are next.

Runtime caveat: native preflight stderr preserves NumPy matmul status warnings.
All recorded arrays and errors pass explicit finiteness checks. The separate
normal-equation review uses einsum rather than matmul, emits no warning and
agrees to1.26e-12. This is floating-point preflight evidence, not rigorous
outward-rounded interval arithmetic. Reproduce with
`python3 launch_native_matrix.py NEW_OUTPUT_DIRECTORY` using the scientific
Python environment recorded in the manifest. Do not overwrite completed runs.


Checkpoint 2026-10-29 01:52 UTC: seed1 is complete and published with final
snapshot/done/log integrity checks. The inventory is now4of9 (1,3,7,8); five
remain pending. Unchanged primary measurements give seed1 c_f=6.095116807,
L_proxy=3.831000832, estimator flag ok. Prior3/7/8 values reproduce exactly;
five extension controls pass. This is one primary measurement near4, not a
robust ensemble-derived L: the previously demonstrated estimator instability
remains unresolved. No full NL1 or corrected linked-T pass is claimed.

The first local structural interval test is complete: canonical L in
[3.75,3.751],127positive-weight nodes,62active halo nodes, no switch event or
saturation. Conditional numerical score lower bound569.531694 exceeds the
unchanged cut163.343463; direct endpoint/midpoint free scores569.624481,
569.626543,569.628607 lie above it. Source stack reproduces to1.33e-15 relative
max norm; all139 run controls and8 algebraic/pinned-column review controls
pass. This is a useful local numerical enclosure, not a certified exclusion:
binary64 root comparisons and prescribed padding lack outward-rounded error
certification. It provides no global continuous-L obstruction or passing
witness. See CSM2 interval_001/ and interval_review.json for limitations.


Checkpoint 2026-10-29 02:07 UTC: seed9 is complete; published inventory is
5of9 (1,3,7,8,9), four pending. Its unchanged primary c_f=15.0898076731,
L_proxy=9.4844885801, flag ok, first selected crossing has601 particles inside.
The previous four primary measurements reproduce exactly; five extension
controls pass. This high primary proxy is not an ensemble level or a robust
inference; the estimator-instability finding remains material. See native
measurement_004_five and completed_results.json. No aggregate NL1 result yet.

Root rounding subexperiment root_sign_001 certifies directed signs for all124
saved compact-root brackets, using50-digit mpmath interval arithmetic with
saved binary64 M,R,Sigma interpreted exactly. A shifted1% bracket is rejected.
A70-digit review using outer-mass residuals and a different log expression
confirms all124 (126review checks); seven run controls pass. This removes one
scalar sign uncertainty only. It does not certify full mass-vector boxes,
projection/whitening coefficients, signed dot products or physical coefficient
construction, and interval_001 remains a conditional local numerical result.
No continuous-model obstruction or passing witness has been established.


Endpoint mass checkpoint: mass_enclosure_001 covers all446524 coordinates
(124 endpoint brackets x3601 radii;62 active halo nodes). Directed50-digit
mass enclosures and outward binary64 conversions pass9 controls. The original
relative1e-8 plus absolute1e-6Msun padding contains every endpoint enclosure;
there are zero misses and no enlarged padding. An independent80-digit refined-
root/normalized-mass review checks496 selected coordinates and passes all127
review controls. See MASS_ENCLOSURE_REVIEW.md for the short bounding argument.

This certifies fixed-coefficient endpoint mass vectors only. Constructed
columns/branches, continuum-L enclosures, projection/stacking/whitening
coefficients and signed-dot rounding still need separate treatment. The local
full-score bound remains conditional; no certified L exclusion or global
obstruction is claimed. Native inventory remains5of9; no new native final or
NL1 aggregate result was present at this check.


Signed arithmetic checkpoint: signed_dot_002_cached encloses7440 signed
projection dot bounds and directed stacking/residual/score arithmetic for an
explicit anchored fixed-coefficient map. Its lower score569.5321678519074
is corroborated by an exact-rational stored-box floor569.5321678519072.
All8 run controls and31 exact-dyadic/review controls pass. This improves the
arithmetic evidence; it does not certify the original likelihood or real-L
interval. Q=P@W construction, physical coefficients, branches and continuum
coverage remain outside the certificate. Preserved NumPy status warnings have
finite saved coefficients, explicitly checked by review.

Next structural route in DUAL_ROUTE.md uses an exactly template-orthogonal
covariance dual witness to remove approximate whitening/projector dependence.
It is prospective, adds no physical fitted parameter, and retains projection
and column/branch/continuum obligations. The uncached initial attempt remains
bounded and unpublished while incomplete; its NPZ-loading issue is documented.
Native finals remain5of9, with no new aggregate NL1 output at this check.


Exact covariance-dual checkpoint: exact_dual_001 proves SPD of the actual saved
60x60 covariance by full rational LDL reconstruction, and constructs a witness
exactly orthogonal to all four nuisance templates. Its exact conditional lower
score569.5338658431842 exceeds a feasible law upper154.34346325076024 plus9.
All12 run controls and18 review/law-solve/bit-cap controls pass. This removes
approximate whitening/projector dependence for the published native boxes;
the witness is an inequality certificate, not an added physical parameter.

The remaining gap is model membership in those boxes: projection coefficient
construction, anchor consistency and column/branch/continuum enclosures. No
real-L/global exclusion is claimed. See EXACT_DUAL_REVIEW.md and the full
rational certificate. The initial uncached signed-dot attempt ended at CPU480
(resource-limit,506.748wall seconds,no scientific result); its completed failure
record is now preserved. Its loading issue was resolved in the already-published
cached3.726-second run. Native finals remain5of9; no aggregate NL1 output yet.


Projection/anchor checkpoint: projection_anchor_001 encloses all432120 fixed-
source-primitive projection coefficients and extracts all127 positive-weight
source mass profiles, including65 previously unsaved fixed law profiles.
All60 source anchor coordinates lie in the resulting baseline boxes. Maximum
anchor deviation8.354e-9; coefficient row L1 error at most1.217e-24. Ten run,
16 exact-quadrature review and5 error-propagation controls pass.

The unchanged exact covariance dual, after coefficient/anchor inflation, still
has conditional lower569.5338657853632 versus exact feasible-law upper+9 of
163.34346325076024. This is not a real-L exclusion: original floating source
evaluation errors and column/branch/continuum box coverage remain open. Fixed
primitive tables are not an analytic-transcendental certificate. Next close
source forward-error bounds using its actual gradient/interpolation/quadrature
implementation, then the remaining domain obligations. See
PROJECTION_ANCHOR_REVIEW.md. Native finals remain5of9; no aggregate NL1 output.


Source forward-error checkpoint: source_forward_001 derives a positive
operation-path error bound for the reviewed projection implementation, using
4930operations and binary64-based roundoff/underflow allowances. Maximum
native projection error1.535e-7; no padding or fit was selected from the score.
All11 run controls (including240 stress cases),8 exact-rational review controls
and4 preparation-premise checks pass. The exact dual lower after this error
budget remains569.5338648476735 versus feasible-law upper+9=163.34346325076024.

The bound assumes inspected version-matched NumPy/IEEE semantics and covered
mass inputs, and does not authenticate the installed C binary independently.
Nonlinear mass construction, original catalogue interpolation/stacking and
column/branch/continuum coverage remain open. No real-L/global exclusion yet.
See SOURCE_FORWARD_REVIEW.md and the licensed cached implementation sources.
Native completion remains5of9; the four pending checkpoints are recent.


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


Fixed mesh continuation: group_mesh_003 completes tiles4[2.66,2.67] and5
[2.67,2.68]. Both directly fail absZ<2 across their entire registered analytic
fixed native EPS/quadrature domains;16run+13review controls per tile plus2batch
controls pass. Exact enclosures and source hashes are in GROUP_MESH_003_REVIEW.md
and results. Inventory now7of89tiles reviewed,82pending. Derivative signs are
not extrapolated, original floating/globalL remains unresolved, and no new
physical fit was added. Next GROUP_MESH_004_ROUTE.md requires runnable criteria
for fixed tiles6[2.68,2.69] and7[2.69,2.70]. Native finals9of9 are validated/copied; final seed6 primary L_proxy4.8646134988. measurement_007_nine passes5controls, exactly reproducing prior eight. NL1 aggregate/scoring pending; no robust derivedL or corrected linked-T pass.


Fixed mesh continuation: group_mesh_004 completes tiles6[2.68,2.69] and7
[2.69,2.70]. Both directly fail absZ<2 across their entire registered analytic
fixed native EPS/quadrature domains;16run+13review controls per tile plus2batch
controls pass. Exact enclosures and source hashes are in GROUP_MESH_004_REVIEW.md
and results. Inventory now9of89tiles reviewed,80pending. Derivative signs are
not extrapolated, original floating/globalL remains unresolved, and no new
physical fit was added. Next GROUP_MESH_005_ROUTE.md requires runnable criteria
for fixed tiles8[2.70,2.71] and9[2.71,2.72]. All9native finals are published; amended NL1 scoring remains in progress. No robust derivedL or corrected linked-T verdict is claimed.


Fixed mesh continuation: group_mesh_005 completes tiles8[2.70,2.71] and9
[2.71,2.72]. Both directly fail absZ<2 across their entire registered analytic
fixed native EPS/quadrature domains;16run+13review controls per tile plus2batch
controls pass. Exact enclosures and source hashes are in GROUP_MESH_005_REVIEW.md
and results. Inventory now11of89tiles reviewed,78pending. Derivative signs are
not extrapolated, original floating/globalL remains unresolved, and no new
physical fit was added. Next GROUP_MESH_006_ROUTE.md requires runnable criteria
for fixed tiles10[2.72,2.73] and11[2.73,2.74]. All9native finals are published. Completed legacy NL1 main reports NATIVE LEVEL FAILS at Lnat4.8646, but validation is partial: rerun/mutation pending; no corrected CSM1 linked-T or robustness claim.


Exact mesh coverage reconciliation: all ten reviewed direct-failure tiles0..9
cover canonical L[2.62,2.72] without gaps in the registered analytic fixed native
EPS/quadrature model. Six exact reconciliation/mutation/hash controls pass;
Zlower>=2.2470308604 throughout this union. No derivative extrapolation is
used. This is a partial-domain necessary failure, not an89tile/global or
original floating-evaluator obstruction. group_mesh_005_union.json records
all result/review hashes and common model/source identities.


Fixed mesh continuation: group_mesh_006 completes tiles10[2.72,2.73] and11
[2.73,2.74]. Both directly fail absZ<2 across their entire registered analytic
fixed native EPS/quadrature domains;16run+13review controls per tile plus2batch
controls pass. Exact enclosures and source hashes are in GROUP_MESH_006_REVIEW.md
and results. Inventory now13of89tiles reviewed,76pending. Derivative signs are
not extrapolated, original floating/globalL remains unresolved, and no new
physical fit was added. Next GROUP_MESH_007_ROUTE.md requires runnable criteria
for fixed tiles12[2.74,2.75] and13[2.75,2.76]. All9native finals and legacy NL1 main failure are published; validation monitoring continues separately, with estimator instability and corrected CSM1 scope kept explicit.


Exact twelve-tile reconciliation now covers canonical analytic fixed-native-EPS/
quadrature L[2.62,2.74] without gaps, direct Zlower>=2.2389200543. Six exact
coverage/mutation/hash controls pass; no derivative extrapolation or global/
original floating claim. The union reads its own frozen inventory snapshot.
Earlier union005's capture-time inventory is byte-identical to the immutable
batch006 input inventory, preserving its historical hash provenance.
NL1's completed normal rerun is now byte-identical to the published legacy
main JSON and final .out, with the same A1 source and8capture/validation checks
passed. NL1_RERUN_CHECKPOINT_2026-10-29 preserves completed copies and hashes.
Mutation rejection/exit validation is still pending. Legacy main failure at
Lnat4.8646 remains distinct from corrected CSM1 linked-T and robustness claims.


Fixed mesh continuation: group_mesh_007 completes tiles12[2.74,2.75] and13
[2.75,2.76]. Both directly fail absZ<2 across their entire registered analytic
fixed native EPS/quadrature domains;16run+13review controls per tile plus2batch
controls pass. Exact enclosures and source hashes are in GROUP_MESH_007_REVIEW.md
and results. Inventory now15of89tiles reviewed,74pending. Derivative signs are
not extrapolated, original floating/globalL remains unresolved, and no new
physical fit was added. Next GROUP_MESH_008_ROUTE.md requires runnable criteria
for fixed tiles14[2.76,2.77] and15[2.77,2.78]. All9native finals and byte-identical legacy NL1 failure rerun are published; mutation validation is pending. Before further mesh batches, prioritize NATIVE_CORRECTED_POINT_ROUTE.md at the originally frozen L4.8646, with separate runnable criteria and unchanged actual CSM1 definition.


Exact fourteen-tile reconciliation extends direct necessary group failure to
canonical analytic fixed-native-EPS/quadrature L[2.62,2.76] without gaps,
Zlower>=2.2308894268. Six exact coverage/mutation/hash controls pass on an
immutable input inventory. Total mesh coverage15of89tiles,74pending; no
global/original floating exclusion or derivative extrapolation.
Priority next is NATIVE_CORRECTED_POINT_ROUTE.md: separately freeze runnable
criteria and test the actual same-column corrected CSM1 calibration at the
originally frozen NL1 point L4.8646, adding no independent T or physical fit.
Legacy NL1 grades cannot substitute for this test, and estimator robustness
remains unresolved. Preserve the queued GROUP_MESH_008_ROUTE.md continuation.
NL1 mutation validation is still monitored without altering active jobs.


Native legacy validation phase is complete. NL1_FINAL_VALIDATION_2026-10-29
captures the finished mutation: exactly K1 rejects A2reference*1.1 while the
other3controls pass, nine seed measurements are unchanged, and9final audit
checks pass. The owning committed report records exit1, also confirmed by the
captured source exit condition (OS wait status not independently observed by
this capture). Normal main4controls and byte-identical rerun remain verified.
The frozen verdict is NATIVE LEVEL FAILS at Lnat4.8646,68%[3.831,5.805], not a
robust derivation or actual corrected CSM1 linked-T verdict. Immutable earlier
partial-validation snapshots retain their historical statuses. No active job
was changed or restarted. Priority next stays NATIVE_CORRECTED_POINT_ROUTE.md;
research/global feasibility remains open, and mesh continuation stays queued.


The actual corrected CSM1 native-point test is now complete at exactly frozen
L=4.8646 (NATIVE_CORRECTED_POINT_REVIEW.md). Canonical SPARC/groups pass but
G-MID-T3,G-OUT-all,G-IN-Mall overpredict and lens delta-law+435.9582717514
fails the +9 cut, on both own/basin calibration. Alt lens delta-law+461.8035053955
also fails; alt own SPARC fails.52independent review controls and all actual
column/selector checks pass; historical X43 K0/K0x38 source failures are explicitly
retained, separate from passing audited replay controls. No added fit or
independent T. This rejects that point, not every L, and does not resolve native
estimator robustness. Legacy NL1 validation is complete. Next resume separately
frozen GROUP_MESH_008_ROUTE.md tiles14and15; research target remains OPEN.


Fixed group_mesh_008 completes tiles14[2.76,2.77] and15[2.77,2.78], both direct
necessary failures of unchanged absZ<2. All2batch and16run+13independent70digit
review controls per tile pass. Six exact coverage/hash/mutation controls extend
gap-free analytic fixed-native-EPS/quadrature group failure to L[2.62,2.78],
Zlower>=2.2229376199. Inventory17of89reviewed,72pending; all prior hashes and
coverage holes are preserved. No derivative extrapolation, new fit or global/
original floating claim. Actual corrected nativeL4.8646 and frozen legacy NL1
validation are complete failures and are not repeated. Next freeze runnable
criteria/resources for GROUP_MESH_009_ROUTE.md tiles16[2.78,2.79] and17[2.79,2.80].
Continuous feasibility/robust derivedL remains OPEN. See GROUP_MESH_008_REVIEW.md
and group_mesh_008_union.json for scope and reproducible evidence.


Fixed group_mesh_009 completes tiles16[2.78,2.79] and17[2.79,2.80]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.80], Zlower>=2.2150633084. Inventory19of89reviewed,70pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_010_ROUTE.md tiles18[2.80,2.81] and
19[2.81,2.82]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_009_REVIEW.md and group_mesh_009_union.json.


Fixed group_mesh_010 completes tiles18[2.80,2.81] and19[2.81,2.82]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.82], Zlower>=2.2072651984. Inventory21of89reviewed,68pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_011_ROUTE.md tiles20[2.82,2.83] and
21[2.83,2.84]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_010_REVIEW.md and group_mesh_010_union.json.


Fixed group_mesh_011 completes tiles20[2.82,2.83] and21[2.83,2.84]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.84], Zlower>=2.1995420263. Inventory23of89reviewed,66pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_012_ROUTE.md tiles22[2.84,2.85] and
23[2.85,2.86]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_011_REVIEW.md and group_mesh_011_union.json.


Fixed group_mesh_012 completes tiles22[2.84,2.85] and23[2.85,2.86]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.86], Zlower>=2.1918925587. Inventory25of89reviewed,64pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_013_ROUTE.md tiles24[2.86,2.87] and
25[2.87,2.88]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_012_REVIEW.md and group_mesh_012_union.json.


Fixed group_mesh_013 completes tiles24[2.86,2.87] and25[2.87,2.88]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.88], Zlower>=2.1843155906. Inventory27of89reviewed,62pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_014_ROUTE.md tiles26[2.88,2.89] and
27[2.89,2.90]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_013_REVIEW.md and group_mesh_013_union.json.


Fixed group_mesh_014 completes tiles26[2.88,2.89] and27[2.89,2.90]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.90], Zlower>=2.1768099448. Inventory29of89reviewed,60pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_015_ROUTE.md tiles28[2.90,2.91] and
29[2.91,2.92]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_014_REVIEW.md and group_mesh_014_union.json.


Fixed group_mesh_015 completes tiles28[2.90,2.91] and29[2.91,2.92]; both
necessarily fail unchanged absZ<2 in analytic fixed-native-EPS/quadrature scope.
All2batch+16run/13independent70digit review controls per tile and6exact
coverage/hash/mutation controls pass. Gap-free direct group failure extends
to L[2.62,2.92], Zlower>=2.1693744711. Inventory31of89reviewed,58pending; all
holes and historical immutable evidence remain. No derivative extrapolation,
physical fit or global/original floating claim. Next freeze runnable criteria/
resources/input inventory for GROUP_MESH_016_ROUTE.md tiles30[2.92,2.93] and
31[2.93,2.94]. Corrected native point and legacy NL1 failures are complete,
not rerun; robust derivedL and continuous feasibility stay OPEN. See
GROUP_MESH_015_REVIEW.md and group_mesh_015_union.json.
