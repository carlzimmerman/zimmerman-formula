# Checkpoint: pressure information after offset calibration

2026-09-30, 02:22 UTC heartbeat pass. Parent: [stage seven](../stage_07/README.md).
The physical objective remains open. This pass changes one assumption in the
finite pressure model: the formerly unrestricted map offset is bounded around
its synthetic baseline, including exactly fixed offset.

The independently certified fixed-offset gradient range is
[-3.755809477804311e-6,-3.627360614306535e-6], a **3.48578956%** width relative
to baseline. The unrestricted range was 11.049571%. Thus an exact offset
calibration alone would not identify the target in this finite model. These
are synthetic pressure slopes per normalized radius, not observed physical
error bars or an adequate correction to a MOND discrepancy.

| Synthetic offset bound beta (Compton-y) | Certified width / baseline |
|---|---:|
| 0 | 3.485790% |
| 1e-6 | 4.335998% |
| 2.8093879085e-6 | 5.874356% |
| 5.6187758170e-6 | 7.640704% |
| 1.8298237703e-5 | 9.779452% |
| 3.6596475406e-5 | 11.049571% |

All twelve extrema have exact rational primal/dual certificates, independently
rechecked by root from original H,L and baseline without importing worker
code. The unique unrestricted optima require offset magnitudes
5.6187758170e-6 and 3.6596475406e-5 respectively. Exact full rank of the old
active systems makes these necessary as well as sufficient recovery thresholds.
Nesting, convexity of the minimum and concavity of the maximum hold for all
beta>=0 by feasible-set arguments. Only six selected beta values are computed;
no complete list of breakpoints is claimed.

A separate exact rank calculation found rank([H;offset])=13 and nullity3.
Root constructed strictly positive, decreasing witnesses with identical bins
and identical offset but different target slopes. A different agent verified
the proof, stored inputs and exact witnesses. Their exhibited 0.43051857%
separation is a control, not a replacement for the sharp 3.48578956% interval.
The general finite claim is: at an interior baseline, the target is identifiable
iff its row lies in the observation row space. Positivity alone does not remove
these locally admissible null directions.

## Scope and next physical obligations

The inherited finite basis, outer support, beam approximation, distance and
exact synthetic measurements remain fixed. Exact stored-coefficient certificates
do not certify actual instrument response or calibration. No covariance, real
offset uncertainty, confidence interval, source mass or force was inferred.
Any later hydrostatic bridge must retain both a0 normalizations, constant-vacuum
versus separate H(z) histories, and Q/R/registered M MOND laws.

FGF-024 now specifies the minimal missing pressure functional and criteria for
an extra observation to identify it. It is a task file, not a launched run or
an available instrument observable. FGF-023, the genuinely balanced responsive
scale–fluid slab, is the next prioritized dynamics task. AS228's previously
failed action-variation evidence remains unaccepted; its owner was sent the
repair prerequisite and this pass's checked findings. No response or repair
execution is implied. The primary catalog has 4500 authored task specifications;
its 130-result inventory was unchanged, so no duplicate intake was performed.

## Evidence and execution

- [FGF-022 root reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-022_RECONCILIATION.md).
- [Independent certificate verification](certificate_audit/run_001/results.json).
- [Fixed-offset proof](offset_audit/DERIVATION.md) and [separate audit](offset_audit/INDEPENDENT_AUDIT.md).
- [Three manifest validations](MANIFEST_VALIDATION.json) and [coordinator receipt](COORDINATOR_VERIFICATION.json).

Both actual agents completed. The shared queue now has 24 tasks: eleven
reviewed_scoped and thirteen ready; no FGF worker running. Source pins, claims,
reviews and handoff were reconciled. No primary catalog, neighboring campaign,
shared standing document, Qwen service or other researcher's work was modified.
