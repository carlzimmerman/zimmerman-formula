# ALMA readiness assessment, 4 November 2026

Verdict: a useful, appropriately cautious pre-data working note, but not yet in its best condition. No manuscript, seal, scoring code or deposit was changed.

Scope: sequential self-review of the complete v1.3 source, its three table inputs, six rendered PDF pages, frozen AC1 criteria/addendum, and selected audit/scoring code. This is not an independent replication of the science. External reference values and current release permissions were not verified.

The existing audit passed 63/63; mutation verification caught 52/52 perturbations. These checks establish consistency of selected numbers with saved outputs and seal prefixes, not correctness of the fitting rules. The audit checks PDF recency, not source-to-PDF semantic equivalence. Visual review found a readable PDF; page 6 is mostly empty.

The main conclusion is well calibrated: U4_28473 predominantly constrains the baryonic mass budget, with weak leverage on a0. Route N retirement and mock/noise forecast corrections are disclosed. The nominal 431 km/s lower branch is an input-grid bound, not a model-independent physical floor.

## AR-1: Fit-start agreement is weaker in code than in the filed rule (major)

Location: ac1_score.py:139-147; paper section 6; ADDENDUM_G1 item 4.

The code first restricts trials to chi2-best <= 9 and computes spread only over those. If only the best trial qualifies, spread is zero regardless of the other starts. The frozen addendum does not state this restriction. No assertion is made that an existing scored mock actually changes grade.

Recommended repair: Check all three starts as filed, or explicitly document a dated pre-data amendment and rerun affected validation. Preserve the original record.

## AR-2: B0 scorecard omits the forecast condition and fit failure (moderate)

Location: paper Table 7 and B0 paragraph.

The prose forecast is conditional on the sister-unit noise and beam ratios. The scorecard omits this condition; it also omits detection followed by an unconstrained fit, although B0 predicts both detection and a scored speed.

Recommended repair: Carry the noise/beam condition into the card; separately record detection, fit validity, and a non-evaluable condition.

## AR-3: B2 counter-outcome does not negate the conditional calculation (moderate)

Location: paper Table 7, B2; Table 3.

B2 is an implication conditional on V near 430. A speed above 600 makes its premise inapplicable, not its implication false. Table 3 ends at 600, with maximum alpha 3.13, and establishes no crossing at 600. Table 2 places the lowest displayed alpha=4.36 flat branch near 676 km/s at 3 kpc.

Recommended repair: Label B2 a conditional diagnostic, give not-applicable outside its premise, and use branch-specific alpha intervals rather than a 600 km/s countercriterion.

## AR-4: The mock error floor is not matched to measured signal-to-noise (moderate)

Location: ac1_score.py:34-35,149; ADDENDUM_G1 item 6.

The addendum specifies scatter at measured S/N. The implementation loads valid compact archive-noise recoveries once and uses the resulting fixed fractional rms for every scored branch. It does not select a calibration by measured S/N, morphology or beam. This need not be anti-conservative, but calibration across those regimes has not been established.

Recommended repair: Explicitly describe the fixed floor and its tested domain, or validate a pre-data calibration across relevant regimes and record any amendment.

## Additional improvements and limits

Give B1 a radius-coverage condition and clearly distinguish its input-grid minimum from a universal bound. Clarify that the inverse gas conversion remains conditional on stellar mass, geometry, pressure support, and the adopted CO excitation ratio. Six successful smooth-disc mocks at one velocity do not establish reliable coverage over the full predicted velocity/morphology range. A larger validation grid would strengthen readiness; no new results are claimed here. Replace the abbreviated R31 notation with its explicit convention Lprime(1-0)/Lprime(3-2)=1.8. The frozen criteria already contain that definition. A compact statement of AT1's sample-level systematic-error requirements would explain what a genuinely discriminating future a0(z) observation needs, without turning this disc into such a test.

Priority: resolve the fit-start discrepancy before running the released cube; reconcile the fixed uncertainty floor with the filed rule; correct B0/B2 scorecard wording. Preserve all historical seals and use dated corrections.
