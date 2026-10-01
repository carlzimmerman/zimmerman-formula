# Checkpoint: the pressure target depends on the imposed outer boundary

2026-09-30, 09:27 UTC pass. Parent: [stage fourteen](../stage_14/README.md).
FGF029 changes one recorded assumption of the finite cluster-response model:
pressure at radius5 becomes free, and the zero endpoint moves to radius6.
The same fifteen annuli, beam, mask, geometry and fixed zero offset remain.
The original fifteen pressure columns are bitwise unchanged.

## Checked result

Let U be the former invertible15x15 response, c the new pressure-hat column,
s the new node5 pressure, and r the former exact gradient-recovery row.
The extended matrix [U,c] has rank15, while adding the target row raises rank
to16. The gradient at radius1 obeys, for the saved finite coefficients,

    gradient = r data + 0.16303084957824435 s.

The coefficient above is a rounded display of an exact nonzero rational value.
Thus the same fifteen bins no longer identify the gradient in this extended
basis. An explicit null direction changes the gradient while leaving every
modeled bin unchanged. Both signs of a sufficiently small displacement preserve
strictly positive, decreasing pressure all the way to the fixed zero endpoint.

The author supplies exponential-baseline witnesses with an exhibited gradient
width0.04023457% of that synthetic baseline. Root independently uses the
rational baseline1e-5/(1+x)^2, giving width0.06991089%. These are two feasible
examples with different synthetic data, not extremal bounds, observations,
confidence intervals, or a measured cluster discrepancy.

## Independent checks and limits

Root independently reduces the full matrix and solves its transpose; the
exact null vector, old dual row and new-coefficient sensitivity agree with the
author's inverse construction. A separate agent audits root's derivation/code.
Root and author also verify that fixing the new coefficient recovers the old
identification, an extra coordinate measurement resolves the freedom, and a
duplicate old row does not. Such a coordinate measurement is a mathematical
control, not an available calibrated observation.

A separate response audit directly integrates the new hat along the line of
sight, reconstructing actual WCS/mask weights and using an independent angular
formula and FFT implementation. Its fifteen coefficients differ from the
analytic projection by at most8.88e-16; all fifteen weight hashes match the
parent. The source patch's minimum edge radius8.83027 exceeds the new support6.
This checks the declared finite response calculation, not continuum convergence
or full instrument calibration. The inherited old columns were not recomputed.

The new column alone is changed. No support sweep, annular redesign, observed
profile fit, covariance, force or mass is inferred. Three bounded computation
manifests are checked in the reconciliation. Exact algebra means rational
arithmetic on saved binary64 response values; response-model uncertainty is
still a separate obligation.

The narrow missing datum is a scalar constraint with nonzero response along
the surviving null direction. An external interval on s would imply a target
width |0.16303084957824435| times its width before other constraints; no such
calibrated interval has been supplied. Finite-model identifiability from FGF028
therefore cannot be promoted to an instrument-calibrated pressure gradient.

## Handoff

- [Independent target derivation](target_audit/DERIVATION.md)
- [Exact root certificate](target_audit/run_001/results.json)
- [Target proof audit](target_audit/INDEPENDENT_AUDIT.md)
- [Independent response audit](response_audit/INDEPENDENT_AUDIT.md)
- [Scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-029_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

FGF030, a fixed-physical-coupling comparison of the diagnostic Q dynamics,
is next. FGF031 records a lower-priority conditional operator-error certificate;
it must not invent a calibration budget or launch another support sweep.
AS228 metric repair remains with its existing primary owner.

Both a0 normalizations, separate constant-vacuum/frozen-H histories, and distinct
Q/RAR/registered M laws remain preserved. A later pressure-to-force bridge
requires density and total/electron-pressure conversion, then the appropriate
MOND source law. No force is computed here. Physical metric/photon coupling,
conserved scale interpretation and empirical adequacy remain open. This finite
counterexample closes only the implication that the same fifteen bins identify
this gradient after the specified support assumption is released.
