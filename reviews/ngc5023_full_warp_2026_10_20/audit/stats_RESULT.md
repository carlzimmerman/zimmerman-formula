# Saved finite-scan result audit

**Outcome: implementation and finite saved-array assertion verified in the
stated range.** The original three-feature mask produces finite-family
residual excesses. It does not support a generic failure-to-detect statement.
Neither discovery significance nor novelty follows.

The completed independent record is `stats_run002/manifest.json`; its
current input/output validation passed. It uses no production module import,
raw-cube rerender or complete scenario refit. Independent explicit-offset
box sums accumulate the saved arrays in float64 rather than using the
production sliding-window summation.

## Checks executed

- All 118 saved cases and 20 translated blanks are present and finite.
- Independently reconstructed training-loss ratios differ by at most
  `4.44e-15`; all retained memberships agree exactly: 76, 83 and 95 cases
  for the three gates.
- The numerical per-bin allowance agrees exactly with the four saved
  numerical controls. Its sum over a box bounds their tested integrated
  prediction changes by the triangle inequality; this is not a uniform
  discretization/model-error bound.
- All 12 region/width/gate scans, full-box inclusion counts, signed family
  distances and worst-retained-scenario blank maxima were reconstructed.
  Maximum saved-statistic discrepancy is `1.479e-6` empirical scatter units;
  maximum blank-maximum discrepancy is `3.677e-7`. These reflect different
  summation precision/order of the saved float32 intensities.
- Three independently repeated bounded training-perturbation fits reproduce
  the saved amplitude changes exactly (nominal/blank 0,
  trace-vrot-minus/blank 7, trace-radius-plus/blank 19). This samples the
  optimizer response; it does not independently rerun all 2,360 fits.

The failed `stats_run001` is retained and excluded. Its calculations reached
serialization but a NumPy boolean was not JSON serializable; the failed
source is preserved as `stats_verify_results_v1_failed.py`. The second run
only corrects conversion of that report flag to a Python boolean.

## Actual original-mask result

Every one of the 12 original-mask search strata has a persistent absolute
peak above the maximum of the 20 corresponding blank-aperture maxima. This
is an empirical comparison, not a tail probability or Gaussian sigma.

At the 1.10 training gate and 24.72-km/s width, the validation maximum is
`6.50243` empirical-scatter units at
`(x,z,u)=(-220,-60,-49.44)` in arcsec/arcsec/km/s. Its observed box flux is
`0.0703631 Jy km/s`, versus finite-family-plus-numerical interval
`[0.0139112,0.0496675]`; blank maxima span `2.56489..3.68322`.

The corresponding guarded maximum is `3.91427` at
`(-60,+100,+61.8)`, with flux `0.0201091 Jy km/s`. The finite family predicts
essentially zero in that box, and blank maxima span `2.56489..3.34010`.
This primarily exposes the supplied model family's support there; empty
model support is not itself a new-physics prediction or an absence guarantee.

The masks exclude three specifically listed localized features and their
mirrors. That is not proof that all previously published extended HI,
spiral, lag or warp structure has been excluded. Source/figure matching of
the surviving boxes is a separate required novelty check. Any additional
known-structure mask chosen after seeing these peaks must be labeled an
unblinded diagnostic sensitivity; preserve this original result.

## Absolute adequacy and permissible interpretation

The best training RMS among the finite family is `7.92888` measured blank
scatter units; nominal is `8.19530`. Relative training gates around the
nominal therefore do not select a noise-limited reconstruction. Nominal
validation and guarded aggregate RMS values (`1.14317`, `1.05316`) include
many empty bins. The nominal-emission-selected subsets have RMS `2.22365`
over 73 validation bins and `1.53929` over only eight guarded bins. Those
subsets are supplementary and model-selected, not new confidence tests.

The supported statement is a mismatch with this finite reconstruction
family outside its three declared localized feature footprints. Whether
that mismatch is previously known extended emission, unmodeled ordinary
kinematics, source-reconstruction inadequacy, instrumental residual or a
new reproducible feature requires additional evidence. The overlapping
blanks, already examined source data, incomplete continuous model family,
and same-cube source/amplitude calibration prevent a discovery p-value,
blind-validation claim or physical memory identification.

All qualifications in `stats_METHOD.md` remain applicable. In particular,
boxwise family envelopes do not imply one globally adequate model and signed
box sums are insensitive to some compensated or finer-scale structures.
