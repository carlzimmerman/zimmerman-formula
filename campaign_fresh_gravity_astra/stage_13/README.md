# Checkpoint: three outer annuli supply the finite pressure information

2026-09-30, 07:25 UTC pass. Parent: [stage twelve](../stage_12/README.md).
This is a conditional response-model result using cached map geometry, mask
and beam. No observed pressure profile was fitted, no uncertainty calibrated,
and no force or source-mass inference performed. Physical theory remains open.

## What changed

FGF028 constructed response rows for [2,3),[3,4),[4,5) target-radius annuli,
on the inherited fifteen-pressure-node basis with p(5)=0 and offset fixed zero.
The three annuli have 13036,18240,23474 usable pixels respectively, with mask1
throughout. These are extra bins of the same cached map, not independent data
sets. The old twelve response rows reproduced bitwise exactly.

All three new rows together determine the finite-model target and all fifteen
pressure coefficients. Every single row and pair fails to determine the target.
The root verified this by independent exact full-matrix elimination and saved
strictly positive, decreasing ambiguity witnesses for the failing subsets.
This is exact for stored binary64 coefficients interpreted as rational numbers;
it does not authenticate an instrument response or a continuum pressure model.

The response reviewer independently projected one outer pressure basis along
the line of sight with 32-point quadrature, used a separate spherical-angle
formula, and applied the stated finite FFT response. It independently checked
all fifteen annular weights and coverage. The one-column check complements
source review and the old-row control; it is not a rebuild of all fifteen columns.

## Identification versus precision

With the response fixed, the target has exact dual weights r satisfying r U=L.
Their raw annular-y L1 gain is 50.26948356094382. Hence a componentwise error
bound epsilon implies |delta(dp/dx)| <=50.26948356094382 epsilon. A saved
worst-sign perturbation attains this bound. The deliberately chosen root
control epsilon=1e-9 y gives 5.026948356e-8 target change, or 1.36419% of the
synthetic baseline gradient. The worker's epsilon=1e-8 control gives ten times
that shift. Neither epsilon is an observed noise estimate or a confidence bound.
The noisy reconstructed profile is not asserted to satisfy pressure inequalities.

The reduced three-by-three response condition number is 22.88066268; the full
raw pressure matrix condition number is 1445.02547432. Row-normalized reduced
conditioning is separately 15.77045792. Units and row conventions matter.

A common offset error has a different response: sum(r)=-0.028902247822995483.
Root's negative control releases the fixed-offset assumption and constructs
strictly positive decreasing profiles with adjusted offsets that leave all
fifteen bins unchanged while changing the gradient. Thus added annuli do not
remove the need to specify/calibrate background treatment. No actual offset
was inferred. Response error adds r DeltaU p, which remains unbounded here
because no physical response-error budget is supplied.

## Evidence and remaining work

- [Worker reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-028_RECONCILIATION.md)
- [Independent target derivation](target_audit/DERIVATION.md)
- [Exact target/subset and sensitivity checks](target_audit/run_001/results.json)
- [Independent response audit](response_audit/INDEPENDENT_AUDIT.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

Finite support, pressure basis, fiducial distance, tangent-plane beam model,
background, calibration and shared-map covariance remain assumptions or gaps.
There is no claim of a calibrated electron-to-total pressure conversion or
MOND discrepancy. Any later source bridge must retain both a0 normalizations,
distinct constant-vacuum/H histories and separate Q/RAR/registered M.

Next prioritize the already-ready FGF027 quantitative full-slab stability gap.
The response result also motivates FGF029: add one pressure node at x=5 and
move the fixed-zero endpoint to6, then test whether target identification
survives this explicit relaxation of source support. That is an unlaunched
model-robustness test, not an assumed correction to the data.

Live handoff: 29 tasks, 16 reviewed and 13 ready, none running. Three bounded computation manifests validate; FGF027 next priority and FGF029 unlaunched. Primary AS228 repair retains its owner.
