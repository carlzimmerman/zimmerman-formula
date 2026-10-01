# Checkpoint: the weak-field quadratic approximation has a shrinking window

2026-09-30, 15:30 UTC pass. Parent: [stage twenty](../stage_20/README.md).
FGF007 tests the inherited Q and RAR scalar gradient energies, separately,
with positive K=2. It does not test the filtered-MONO metric action or prove
nonlinear stability of the coupled matter system.

Let g0 be background gradient magnitude and h the perturbation gradient.
Subtract the exact linear energy term, then compare the remaining increment
D with its quadratic Taylor energy H2. The controlling amplitude is |h|/g0,
not merely |h|/a. Both dimensional scale normalizations are restored in the
worker output; constant-vacuum and frozen/evolving-H cases remain separate.

The finite computation covers72 cases: two laws, three g0/a values
(.1,.01,.001), four amplitude ratios(.001,.03,.3,1), and parallel-plus,
parallel-minus and transverse directions. At those points the largest error
|H2/D-1| is approximately0.0333443%,1.010097%,11.11107%,49.99988%, respectively.
These are finite high-precision results, not a certified uniform error box.
Using D/H2-1 as the denominator convention gives different numbers; both are
reported explicitly. A30%-of-background perturbation therefore already permits
about11% error in the specified finite test, even at very small absolute field.

## Exact limiting distinction

For both laws W~g³/(3a) near zero. At fixed epsilon=|h|/g0<=1, as g0/a->0,

    D/H2 -> 1+epsilon/3       (parallel plus),
    D/H2 -> 1-epsilon/3       (parallel minus),
    D/H2 -> 2[(1+epsilon²)^(3/2)-1]/(3epsilon²) (transverse).

The leading relative remainder is O(epsilon) parallel and O(epsilon²)
transverse. At exactly zero background, the leading spatial energy is cubic
and the spatial Hessian vanishes. K=2 still has a positive time kinetic term.
This does not prove a ghost, nonlinear ill-posedness or a global branch failure.

There is a precise nonuniformity: for independent positive absolute background
and perturbation amplitudes, shrinking the perturbation first gives relative
ratio1; shrinking the background first gives an unbounded ratio. The ratio
is undefined exactly at zero background. BOTH iterated raw energy limits
are zero. The phrase 'noncommuting limits' must not be applied to the raw
energy, or confused with different fixed-ratio paths.

Author and auditor use separate high-precision implementations and convergence
checks, with direct/primitive representations and a separately audited root
asymptotic proof. Shared constitutive identities are disclosed; matching
precision is not a rigorous interval certificate. Two bounded manifests,
source hashes, code and detailed audits supply the computation provenance.
No observational or empirical significance is attached to this finite test.

- [Root energy and limits proof](zero_field/ROOT_DERIVATION.md)
- [Root-only proof audit](zero_field/INDEPENDENT_AUDIT.md)
- [Independent numerical audit](independent_audit/INDEPENDENT_AUDIT.md)
- [Scoped reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-007_RECONCILIATION.md)
- [Coordinator receipt](COORDINATOR_VERIFICATION.json)

The next distinct question is whether a genuinely coupled hydrostatic
configuration can pass through zero signed MOND flux with finite energy,
and what regularity or coercivity is then lost. FGF035 records that new spatial
crossing problem. Its proposed flux-coordinate construction is unproved work,
not an extension already supplied by this uniform-background calculation.
It must not be mistaken for the regular H2 branch theorem of FGF034.

Both a0 hypotheses and Q/RAR/registered M distinctions remain intact. No
source mass or discrepancy is computed; any later inference must use the
appropriate MOND flux and calibrated matter/pressure data. Physical V,
local covariant scale-vacuum dynamics, metric/photon coupling and theory
closure remain open. FGF031's finite robustness route stays stopped pending
actual calibration. AS188 is a different filtered-action interaction target;
AS228 metric repair remains with its primary owner.
