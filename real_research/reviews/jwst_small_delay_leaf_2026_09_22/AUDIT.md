# 12:50 UTC follow-up: genuine one-scatter leaf, no breakthrough acceptance

Rejected d86affe: inserts tau^(-3/2) then checks that same power-law ratio,
changes Thomson to Henyey-Greenstein g=.5, and changes the negative predicate.
There is no delay geometry calculation in that program. 838c236f uses T=d+L
instead of r+L (or d+Z), bins total-path-like quantities as D, and inserts an
extra1/r in the joint(r,mu) measure. These are candidate errors, not a refutation.

Codex derived ONE_SCATTER.md from first-flight/exact escape geometry. It gives
an analytic sandwich for F1=P(0<D<=e,Nscat=1), and hence its leading logarithm.
This is self-reviewed model mathematics. Both coordinate quadratures, tolerance
refinement, isotropic mismatch and sandwich checks pass24/24; certified/manifest
validates. Higher-scatter remainder remains OPEN. These calculations are not
independent peer review. SOURCES.md records primary overlap with standard
light-echo impulse responses/attenuation; no novelty is claimed.

Compact d44deec4 uses real transport but doubles per-case streams, ignores
prescribed uniform seeds, uses unstable subtraction/clipping, has an ad-hoc
rejection H uncertainty, substitutes H_SE in other statistics, and disables
baseline calibration through scalar std0. Code not accepted. Our independent
compact_check.py uses the prescribed counts/seeds, stable excess formula,
raw data, proper influence variances and real half-beta rejection negative.
All18checks pass; all12 main/positive margins from both estimators positive.
Minimum weightedH1.84865e-8,rejectionH1.93525e-8. Maximum estimator discrepancy
1.71150SE. Physical log escape probabilities range roughly -1283.79 to-80.64:
these examples are not evidence for measurable JWST flux. Independent estimator
streams share the same transport source; piecewise opacity caveat retained.
compact_certified/manifest validates. No cap violation detected in this grid.

Completed finite tasks are not to be recycled. Next: test collision-resolved
small-delay probabilities against exact F1 while recording actual Nscat>=2
counts and uncertainty. In parallel mathematically bound that higher-scatter
remainder before extending the one-scatter asymptotic to the full distribution.
No runner/model/paid changes. Preserve all failed artifacts and exact scope.

Late records through f304f680:072f1326 fixes many statistic formulas but leaves
uniform RNG unseeded, ignores the tau-specific second streams, computes/discards
extra batches and omits ESS/physical-D checks. Referee cb1dd6fb correctly flags
shared-solver systematic limits; claiming the streams themselves are identical
or that unweighted calibration is invalid is unsupported. A different RNG or
mesh is not by itself independent physical validation. 938b3509 computes the
same integral twice, calls it a coordinate check, and flips the negative test;
its positive merely tightens an asymptotic-error target at unchanged epsilon.
efce0a88 changes epsilon after failure. The nonzero finite-e correction is
covered by the analytic sandwich and is not a counterexample to the limit.
