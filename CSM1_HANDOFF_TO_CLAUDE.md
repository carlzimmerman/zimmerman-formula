# Claude handoff: corrected core/switch results

Start with `rebuild_2026_10_22/CSM1_consistent_core_switch/README.md`, then
`MODEL.md`, `REVIEW.md`, `HANDOFF.json` and
`reconciliation_001/results.json` in that directory. This checkpoint supersedes
earlier claims of a joint calibration pass that used different concentration
coefficients for the switch and the actual core.

The correction adds no fitted parameter: each parent selector compares the
same mass-dependent unfloored column used by its local core with its own
floor. No independent T is adjusted. Own and basin masses retain the recorded
pipeline-specific meanings, and dwarfs retain their separate cooling profile.

Results on the unchanged cuts:

- L=3.75, 3.9 and 4.0: SPARC, 63 groups and all cluster keys pass on both
  footings. Lensing fails. Canonical delta-chi2 versus law is +415.281,
  +420.306 and +423.234, against an allowed +9.
- The predeclared existing-L refit is L=2.5090648745652686, defined by actual
  canonical/background-A X43 equality at logM=12.3. Lensing passes, but
  canonical groups fail at Z=+2.621919809. No joint pass was found.
- The alternate-footing fixed MW ultra-faint construction has exactly two
  possible L-independent profile states, both failing. Changing L alone
  cannot rescue that class. This is conditional on that fixed construction.
- Four tested levels do not exclude every canonical L. Do not infer likelihood
  or group-Z monotonicity from monotonic activation columns.

Old baselines reproduce; actual-flag mutation controls fail as intended.
The coordinator passes 141/141 reconciliation checks. Independent reviews
check numerical columns, actual branch decisions, raw class summaries and
primitive MW line cuts. Commands, hashes, manifests and retained unsuccessful
development runs are included. Scientific failure must not be confused with
implementation-control failure. The 2.12-ppm displayed-a0 challenge error was
corrected by rerunning the same frozen target; both records are retained.

The preceding audit and observational recovery are in
`rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/`. Its current-theory statements
are dated history; use CSM1 for the corrected-model empirical verdict.

Native progress update: seeds 3, 7 and 8 of nine have completed. Their verified
final snapshots, completion markers, final logs and hash inventory are in
`rebuild_2026_10_22/NATIVE_PARTIAL_2026-10-28/`. This is a partial ensemble,
not a new ensemble L estimate or NL1 grade; the other six remain pending. Use its
`completed_results.json` for the exact observation timestamp and seed set.

Preliminary measurements of seeds 3, 7 and 8 are in that package's
`measurement_002_three/results.json`: unchanged primary
c_f=3.138159/2.441598/4.010123 and NL1-normalized per-seed
L proxies=1.972446/1.534632/2.520507 (seeds 3/7/8). All have estimator flag
`ok`. Five implementation controls pass, including exact reproduction of the
previous seed-3/7 results. The initial two-seed evidence remains unchanged in
`measurement_001/`. Seed 8 is higher than the first two, but all three proxies
are below L near 4. Its c_f near 4 is not L near 4 under NL1's normalization.
These do not estimate the full ensemble or establish convergence. Completion
order is not a representative sample, and the NL1 mass/resolution-transfer
normalization remains conditional. No full NL1 grade has been produced here.

New robustness audit: `rebuild_2026_10_22/CSM2_single_L_search/README.md`.
Changing radial edges from 25 to 29 exposes an earlier -2 crossing: c_f moves
from 3.138 to 16.804 (seed 3), and 2.442 to 11.798 (seed 7). Seed 8 stays near
4.01--4.04. All tested binnings pass the synthetic control. Independent profile
reconstruction confirms multiple crossings and the first-crossing selection
mechanism. Original primary results remain unchanged, but their `ok` flags
alone do not establish a robust L. No alternative crossing was selected to
match a desired value. CSM2's bounded necessary group/lens grid is now complete:
none of15 predeclared levels survives. Groups fail through the sampled L=3.5;
six tested values3.625--5.0 pass groups but fail lensing by delta-chi2+411--437.
The finite result is not an all-L theorem. A validated linear-projection
preflight and `INTERVAL_ROUTE.md` record the next route to interval bounds.

The native ng64/NL1 aggregate work is still pending at this observation.
`rebuild_2026_10_22/NL1_native_level_L/` contains its scorer. Verify actual
complete outputs, seed coverage and uncertainty when they arrive. Its old
fixed-T primary grade alone cannot establish a corrected linked-T pass;
L near 4 alone would not restore CSM1 lensing. Preserve running jobs/follower.

Kappa=1/2 remains fitted, basin selection remains a posit, and there is no
new condensation field equation or covariant completion. No new temperatures,
inclination correction or hot-gas repair was folded into CSM1.

The user has authorized pushing completed results as they arrive so Claude
can retrieve them. Publish verified result packages and a clear handoff;
keep unrelated dirty work and incomplete simulation dumps out of such commits.


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
