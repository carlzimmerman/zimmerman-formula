# Independent statistical-method audit

Read-only examination of the scenario rules, calibration code and mask
construction, followed by this audit note. No cube/model scientific run
was executed for this review. The later scan implementation and numerical
results still require separate inspection.

**Verdict:** the proposed procedure can support a conditional descriptive
failure to isolate a robust residual in its declared finite search. It
cannot establish signal absence, a calibrated significance, an upper limit,
joint model adequacy or exclusion of a physical memory state.

## Exact finite claim

Let `T` be the frozen training bins, `B` a full search box, `y` the observed
binned cube and `m_j(a)` a scenario prediction with its three bounded
component amplitudes. Write `a_j(y_T)` for the training-only fit and

`p_j = m_j(a_j(y_T))`, `s_j(B) = sum_B p_j`, `s_y(B) = sum_B y`.

For a declared training-loss gate retain a finite set `J`. Compute the
envelope **after summing each whole scenario within the box**:

`L_B = min_{j in J} s_j(B)`, `H_B = max_{j in J} s_j(B)`.

Taking the pointwise minimum/maximum before summation would produce a
different and generally wider envelope by mixing incompatible scenarios
inside a box. Do not substitute that operation.

If `delta_B >= 0` is the stated maximum tested numerical-control discrepancy,
the nonnegative distance outside the enlarged envelope is

`d_B = max(0, s_y(B) - H_B - delta_B, L_B - delta_B - s_y(B))`.

Preserve the sign separately: positive for excess above `H_B+delta_B`,
negative for deficit below `L_B-delta_B`. A scan maximum over the frozen
boxes is a finite descriptive statistic. Retain both widths and both
validation/guarded regions with their box counts; report all chosen gates.

## What the finite envelope does not mean

Each box may select a different member at either envelope endpoint. Thus
all observed box sums lying inside their envelopes **does not imply that
one scenario fits the entire cube or all boxes simultaneously**. The valid
negative statement is: no tested box sum is beyond every retained scenario
by the declared numerical allowance and empirical comparison criterion.

The gates `1.10`, `1.25`, `1.50` times nominal weighted training RMS are
sensitivity labels. They are not confidence sets, and being near a poor
nominal fit does not establish absolute adequacy. Report absolute residual
RMS against the blank diagnostics and retained membership for every gate.

The finite scenario family is not a posterior or a continuous parameter
confidence region. The 32 deterministic Sobol points provide neither random
sampling coverage nor exhaustion of their parameter box. Published visual
one-parameter deviations are not independent Gaussian errors. Digitization,
interpolation and structural alternatives remain distinct error sources.

`delta_B` is a tested discrepancy, not a proved bound on all quadrature,
interpolation, instrument or model errors. Adding it enlarges the comparison
region conservatively with respect to those tested deviations only. Check
whether numerical alternatives materially change training gates as well as
validation predictions; a nominal-only convergence control is not uniform
over the full physical family.

## Correct blank-refit construction and its scope

For translated real-sky blank cube `e_k`, fit the same bounded calibration
problem to `y_T + e_{k,T}`. Its prediction response is

`Delta p_{j,k} = m_j(a_j(y_T + e_{k,T})) - m_j(a_j(y_T))`.

The conditional residual fluctuation is

`r_{j,k} = e_k - Delta p_{j,k}`.

This propagates a training-noise perturbation into the validation prediction,
including bound activation in the nonlinear constrained fit. Fitting the
blank alone, omitting the baseline prediction subtraction, or applying only
validation blank noise would not implement this construction. Preserve
solver status, bounds and boundary hits for the perturbed fits.

Compare scan maxima from identically shaped, identically masked boxes and
the same signed/two-sided convention. State exactly how multiple scenario
blank responses are combined: the maximum over scenarios is a conservative
enlarged reference for this diagnostic; a typical-scenario response is not
automatically calibration for the family envelope. If family membership
remains fixed under blank perturbation, label the reference conditional on
that observed retained family. A calibrated full-pipeline null distribution
would require carrying any data-dependent gating/selection through the
replicates and accounting for model fitting; this procedure does not claim
such a distribution.

Twenty translated blanks retain native beam/channel correlations and their
response to interpolation and summation. They overlap and share processing,
so they are not independent trials. Their maxima provide an empirical
comparison range, not a Gaussian significance, tail probability, coverage
guarantee or sensitive nondetection limit. The same blanks estimate fitting
weights: those weights are conditional choices, not a measured complete
covariance. Source-region CLEAN/dynamic-range residuals, spatial sensitivity
changes or emission-dependent errors need not be represented by translated
empty sky. A residual exceeding this range would still require diagnosis.

## Masks, calibration and search interpretation

The inspected `compare_model.py` uses 20-arcsec spatial and 12.36-km/s
spectral bins. Its training centers satisfy `|z|<=10`, corresponding to a
physical strip `|z|<=20` before masking. Validation centers `|z|>=50` and
guarded centers `|z|>=70` start at physical heights 40 and 60 arcsec.
This distinction is harmless if the edge/center convention is stated.
The training also has `|x|<=230`, `|u|<=105` and known-feature exclusions;
it is not the unqualified entire native cube footprint.

Search boxes must contain every required `2x2` spatial bin and `2` or `3`
spectral bins, all inside the relevant frozen mask. Reject partial boxes
at boundaries or holes rather than silently summing fewer bins. Known-feature
exclusions are expanded by bin halfwidths and declared beam/spectral guards.
These reduce direct leakage but do not make Gaussian beam wings vanish.
Training/validation are therefore protected regions, not strictly independent
noise samples. The guard variation is a useful sensitivity test.

The preferred shape parameters, component mass ranges and known-feature
locations originate in modeling this same observed cube. The present fitting
does not newly optimize those shapes in validation, but validation is not a
blind independent holdout of the original published model. An earlier look
at residuals also precludes calling this a discovery pre-registration.

A signed box sum can cancel positive and negative internal residuals. The
test has power for coherent integrated excess/deficit on its two declared
scales, not for every line-shape, velocity-shift, narrow or compensated
signal. State that resolution/search-class limitation explicitly. A symmetric
mass or memory component may change the rotation already represented in
the model and need not create a residual of this form.

## Recommended result wording

If the observed scan statistic is within the stated blank comparison range:

> This finite source/model family and protected-region scan do not isolate a
> box-integrated residual that is robust to all retained scenarios and
> distinguishable from the adopted correlated blank-sky controls. This is
> conditional on the family, masks, two box widths, numerical tests and
> existing same-cube calibration. It is not an absence theorem, formal
> significance or constraint on every memory-bearing state.

If model residuals are large absolutely, separately report inadequate
reconstruction/model adequacy. Do not use a broad family envelope or larger
training gate to certify that the physical cube has been fully explained.
