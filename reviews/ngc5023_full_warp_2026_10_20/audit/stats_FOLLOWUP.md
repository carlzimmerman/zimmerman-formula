# Frozen-box follow-up: independent statistical check

**Verdict:** the off-plane positive candidate remains a mismatch with the
tested finite reconstruction family and recurs in the same-observation
HR/LR imaging. The older data neither confirm nor meaningfully exclude it
at their measured sensitivity. This is an unconfirmed observational
candidate, not a novel detection or evidence for a physical memory state.
Source novelty is a separate primary-text/figure classification.

No raw cube or model was rerendered for this audit. The independent checker
uses explicit scalar-offset aperture sums on the saved arrays, with no
production imports. All 42 data/blank-mean/scatter combinations, nine
finite-family range aggregations and 21 nominal-model aperture sums pass.
The completed/current-input-validated record is
`stats_followup_run001/manifest.json`.

## Candidate and measured sensitivity

The narrow candidate is frozen at `(x,z,u)=(-20,+100,+24.72)` in
arcsec/arcsec/km/s, in a `40x40 arcsec x24.72 km/s` box. The broad positive
box has the same sky position, velocity center `+30.9 km/s` and width
`37.08 km/s`. They substantially overlap and are not two independent signals.

The entries below are **raw aperture flux minus the mean of 20 translated
blank-aperture sums**, followed by empirical blank scatter, all in Jy km/s
at common 40-arcsec angular resolution. The plus/minus notation is not a
Gaussian significance or a calibrated confidence interval.

| Frozen box | HALOGAS HR | HALOGAS LR | Older WHISP |
|---|---:|---:|---:|
| Narrow positive | 0.017802 +/- 0.003386 | 0.011388 +/- 0.001988 | 0.010183 +/- 0.016941 |
| Broad positive | 0.022012 +/- 0.004475 | 0.014306 +/- 0.002527 | -0.003624 +/- 0.022795 |
| Selected narrow negative control | -0.010502 +/- 0.002823 | -0.005810 +/- 0.001554 | -0.030420 +/- 0.016330 |
| Broad negative control | -0.005567 +/- 0.003441 | -0.003531 +/- 0.002546 | -0.001873 +/- 0.015978 |

The selected narrow negative control is at `(+140,-100,-74.16)` with
24.72-km/s width; the broad negative control is at `(+200,+100,-30.9)`.
All were selected after the original HALOGAS scan; none is a randomly
chosen blank replication trial. The older cube was already examined in
the parent phase, so freezing these boxes before reopening it does not
create a previously untouched holdout.

At the broadest declared relative-training gate, the common-40 finite-family
narrow prediction spans about `0.0000626..0.0009057 Jy km/s` for HR/LR and
`0.0000624..0.0009012` for WHISP. The broad positive model maxima are about
`0.0009621` and `0.0009576`, respectively. These are finite prediction spans,
not likelihood intervals or a complete uncertainty envelope. The follow-up
model ranges do not themselves add a newly measured common-40 numerical
error bound; retain the separate finite numerical-control qualifications.

The narrow positive measurement survives the tested native-HR aperture
translations and interpolation in sign. That is a local processing check,
not an independent data set or a new significance calculation.

## Why the older cube is inconclusive

If the HR/LR blank-corrected amplitude transferred unchanged into the older
measurement operator, it would be only `0.672..1.051` times the older
narrow-box empirical scatter. For the broad box it would be only
`0.628..0.966` times its scatter. Thus a weak, absent or opposite-signed
older measurement at these noise levels does not refute the candidate.
The observed older narrow value is only `0.601` scatter units and its broad
value `-0.159`; those do not independently establish the counterpart either.
These are descriptive sensitivity ratios, not a power calculation under
a calibrated noise distribution.

The instrument response/uv sampling, source effective line profile and
calibration also differ. The family was forwarded through each recorded
native operator, without fitting older data; that is useful but does not
authenticate an exact spectral response or eliminate all flux-transfer
uncertainty. Complete visibility disjointness has not been established.

## One-sided emission and negative controls

Positive optically thin emission is the relevant candidate direction, but
the original search included both signs and selected extrema. A one-sided
discovery probability cannot be assigned retrospectively from these ratios.
Report the positive candidate and negative residual controls separately.

The selected negative box recurs in HR and LR at about `-3.72` and `-3.74`
empirical-scatter units. This demonstrates why same-visibility recurrence
alone is insufficient confirmation: shared imaging/noise structures can
also recur. It does **not** prove that the positive candidate is an artifact.
Negative residuals can diagnose imaging/baseline problems or model
overprediction; absorption would require separate continuum/line evidence
and lies outside the adopted emission-only forward model.

HR/LR signs and morphology therefore supply a resolution/imaging consistency
check, not independent replication. Their different amplitudes must not be
combined using independent-error formulas. The surviving classification is
an exploratory off-plane intensity excess unexplained by this finite
source family, pending source-overlap checks and data with materially better
independent sensitivity or direct visibility/imaging tests.
