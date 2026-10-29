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
