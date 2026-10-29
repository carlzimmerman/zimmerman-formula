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
