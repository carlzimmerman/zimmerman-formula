# Claude: fix the merger inference, then derive the response

Repository review, 2026-10-10, HEAD `6323b630fa51329505dc7191ee4d51218ec9d26c`. The CFG597 scripts/results reviewed here were **untracked draft work**, without a README. This is a handoff about that snapshot, not a claim about a finalized result. Source hashes and recomputed diagnostics are in [the snapshot](claude_next_2026_10_10_snapshot.json).

**Decision:** the current draft does not establish that galaxy settling is incompatible with mergers. Repair its inference before using it to reject a mechanism. The next physics task is to derive energy transport and merger response from one declared interaction and state; they need not share one scalar relaxation time.

## 1. Correct CFG597 before interpreting its physics

Claim audited: the merger grid supplies an upper bound on alpha that excludes galaxy settling. **Verdict: incomplete, with the smallest missing implication being a validated map from merger observables to the permitted relaxation-rate set.**

Dependencies: validated progenitors/kinematics → reliable observables → permitted alpha set → intersection with galaxy requirements and causality → physical interpretation.

| Obligation | Snapshot finding | Required action |
| --- | --- | --- |
| Frozen C4 control | **Failed:** isolated centroid offset 16.960 kpc exceeds 15 kpc; mass drift passes. | Section 5 requires dependent verdicts to be VOID. Preserve raw scores, but gate conclusions. |
| Upper-bound interpretation | **Failed:** L-2S canonical permits alpha = 0 and 10, yet reports alpha_max = 0.0576812. Both footings permit 10. U-2S even permits infinity while reporting a finite maximum. | Keep the full, potentially disconnected allowed set. A first crossing is not a global upper bound. |
| Interpolation endpoints | **Not justified by frozen criteria:** code substitutes 0.03 for zero and 100 for infinity in log interpolation. | Report endpoint brackets; obtain any tighter finite crossing from explicit finite nodes. |
| Kinematic calibration | **Failed for primary 10:1 L:** 3020.529 km/s lies outside 2700 ± 200. | Disclose and resolve M-6 mismatch before treating this as the declared merger. |
| Mutation checks | M1/M3 pass; **M2 fails**, mean beta = 0.124758 versus ≤ 0.10. | Diagnose the collisionless baseline; do not describe every control as passing. |

Implementation locator: [cfg597_main.py](../campaign_fresh_gravity/CFG597_merger_settling_stopwatch/cfg597_main.py), lines 267–282 returns the first crossing; 308–315 turns it into V3. [Frozen rules](../campaign_fresh_gravity/CFG597_merger_settling_stopwatch/FROZEN_CRITERIA.md), S-2/V-3 and section 5 govern the interpretation. C4 alone blocks the dependent physical verdict; this review does not invent a new frozen threshold.

**This is not a rescue by alpha = 10:** the theory separately states alpha ≲ 1. Once controls pass, compare the measured allowed set with independently established galaxy and causal ranges. Passing isolated grid points does not establish the intervals between them. Keep dated corrections separate from the frozen criteria.

## 2. Keep the useful recent empirical progress in proportion

- [CFG589](../campaign_fresh_gravity/CFG589_late_clock_matched/README.md): exact mass matching supports an early-type colour trend; the universal-clock verdict is **UNDECIDED**. Colour has not become a calibrated formation age.
- [CFG600](../campaign_fresh_gravity/CFG600_native_catchment_kids/README.md): **VOID** by frozen controls. Its descriptive inner-bin edge insensitivity makes another edge-only repair of the inner amplitude a poor next use of time.
- [CFG601](../campaign_fresh_gravity/CFG601_kids_shmr_sensitivity/README.md): changing SHMR barely matters; leakage normalization matters. Propagate uncertainty in the measured leakage, rather than select an arbitrary multiplier from the sensitivity rows.
- Leave CFG596's existing production work intact. Its eventual result tests the implemented phenomenology; it cannot identify the cold component by itself.

## 3. One bounded theory work order

Start from the [declared carrier Hamiltonian](microscopic_carrier_2026_10_10/REPORT.md) and [radial delivery audit](transport_clock_2026_10_10/REPORT.md). The massive Bose field is a candidate, not an identified substance; its contact pressure is negligible at the illustrative eV benchmark, so kinetic support is essential.

1. Specify the occupation distribution, temperature/dispersion convention, condensate fraction if any, and validity regime. Density and dispersion alone do not specify a general nonequilibrium state.
2. From one consistently normalized collision operator, calculate or bound heat-current and anisotropic-stress relaxation using the **same mass and coupling**. Include condensate exchange only where justified. Check conservation and mean free path relative to the system size. Do not equate bare scattering, condensation, conduction and drag rates.
3. Use that closure to distinguish spherical mass assembly from displacement/recentering response. The existing radial calculation already shows why one alpha does not imply one halo-wide clock. Derive the two responses rather than assigning separate fitted rates.

**Deliverable:** one short compatibility calculation, with declared galaxy/cluster states, controlled timescale bounds and the first missing input. Stop before a large simulation if the kinetic approximation is uncontrolled. Failure of this candidate is not a universal no-go.

Energy conservation permits redistribution but does not prove outward heat flow or a stable halo. Even a successful transport calculation would still need to select the observed profile and connect its normalization to vacuum energy. The present carrier does not derive kappa = 1/2 or resolve 32 pi squared.

Review scope: local source/results and arithmetic only; no merger rerun or external-data validation. A second reader confirmed the first-crossing and C4 findings. No concurrent lane, standing instruction or frozen criterion was edited.
