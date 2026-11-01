# Final interpretation: a computed exchange channel, not a core-regulation result

The specified PN28 kinetic parent supports a causal, frequency-dependent
exchange of energy and angular momentum with a prescribed rotating
quadrupole in the declared fast-scalar limit. The total finite-pulse work is
positive in all fifteen final full-feedback state/frequency cases, and the
work-energy and torque-angular-momentum ledgers close. The response comes from the action's
orbital transport and reciprocal feedback, without an inserted drag or
torque efficiency. This establishes a functioning dynamical exchange
calculation beyond the earlier isotropic static response.

It does not yet establish that this exchange prevents baryonic contraction,
creates or maintains a galaxy core, selects a physical halo population, or
explains the acceleration law. Energy transfer alone is not that mechanism.

## What the available comparisons support

The table uses the final primary baseline, compact and diffuse records named
below, together with their existing bare controls. Values are total work
divided by squared forcing amplitude, in the declared
dimensionless energy units. The frequency label is pattern speed divided
by the dynamical frequency of **each column's own background state**.

| Pattern-speed ratio | Baseline, full | Baseline, bare | Compact endpoint, full | Compact endpoint, bare | Diffuse endpoint, full |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.269963 | 0.124105 | 2.557810 | 1.242450 | 0.326584 |
| 0.5 | 0.002865 | 0.001690 | 4.440691 | 3.877639 | 0.004123 |
| 1 | 6.782769 | 1.365465 | 2.301461 | 0.985099 | 6.749686 |
| 2 | 0.017796 | 0.035006 | 9.779677 | 54.138620 | 0.018643 |
| 4 | 187.534694 | 166.773737 | 6.437235 | 5.041475 | 185.429971 |

Collective feedback can enhance or suppress the supplied work, depending on
frequency. For example, the baseline response near ratio one is about five
times its bare value, whereas the compact response at ratio two is about
0.18 times its bare value. There is no frequency-independent enhancement or
suppression factor in these results.

Nonnegative work follows structurally for a zero initial perturbation and
a positive finite Hamiltonian when the source returns to zero. The new
quantitative result is the response magnitude, frequency dependence and
collective feedback, not positivity of work by itself.

The bare experiment removes self-gravitational, scalar and reciprocal
current feedback together while preserving the same background orbits.
It already has nonzero work. Thus full/bare differences demonstrate combined
collective response, not a uniquely scalar effect or a distinction from all
ordinary collisionless gravitational responses.

All three resolved finite Hamiltonians are positive: their lowest eigenvalues
are approximately 0.643288 for the baseline, 0.722884 for the compact
endpoint and 0.655094 for the diffuse endpoint.
That supports bounded unforced evolution in the tested finite kinetic
spaces. It is not a continuum nonradial stability theorem and does not
reverse the earlier dense-branch energy-saddle result.

## Robust totals and unresolved local/late diagnostics

The final short-pulse work meets the frozen 1% convergence target in all
three states. Final spatial changes are below 0.2% for the baseline,
0.08% for the compact endpoint, and 0.6% for the diffuse endpoint. The
earlier compact high-frequency basis sensitivity was resolved by the
subsequent refinements; its final work is 6.437235, not the interim value
6.116323. At the final compact spatial grid, increasing Krylov dimension
from 1152 to 1536 changes work by at most `3.5e-10` relatively. The energy
and torque ledgers are tighter than these spatial truncation differences.
The full comparison record is `summary_001/summary.json`.

The original polynomial coordinates become ill-conditioned at high radial
order, and the final compact complete feature-Gram discrepancy is about
0.104%, while the forcing sum rule is substantially more accurate. These
are floating-point convergence results, not rigorous error bounds.

Late-time coherent quadrupole amplitudes are a different matter. For the
compact state, the late/peak ratio at pattern ratios 0.25 and 0.5 moves
from approximately 0.350 and 0.468 in the 40-point/768-Krylov run to 0.012
and 0.037 in the 64-point/1152-Krylov run, despite unchanged total work.
Those changes prevent a robust decay-time, damping, recurrence or
irreversible-mixing conclusion from these records. More refined late
values are diagnostics, not a settled relaxation result.

The baseline longer-pulse comparison is resolved under its stated Krylov
refinement: doubling pulse duration changes work by factors approximately
`2.07, 0.027, 0.94, 0.044, 2.18` across the five pattern-speed ratios.
The result is frequency dependent and does not define a universal absorption
rate. The longer compact-state work remains numerically inconclusive because
it changes substantially with Krylov dimension; it is excluded from physical
duration-scaling conclusions. This unresolved longer-pulse result does not
invalidate the converged short-pulse totals above.

The core-restricted observable measures where the external source performs
work. It does not measure energy retained within the core. Energy and
angular momentum can cross that boundary, and the sharp spatial restriction
converges more slowly in orbital harmonics. Negative fractions and fractions
above one are compatible with this definition. They must not be interpreted
as negative heating, more than 100% retained heat, or a core-expansion
efficiency.

## Why no contraction-suppression conclusion follows

The computed density perturbation is first-order `l=2`; its spherical
average vanishes. A changed mean core radius or spherical density profile
is an `l=0` effect arising at second order or through nonlinear evolution.
That equation has not been solved. Quadratic total work and angular momentum
can be obtained from first-order response without determining the spatial
second-order distribution. Their signs therefore do not determine whether
the halo expands, contracts less, develops anisotropy, or retains a coherent
oscillation.

In particular, this experiment does not undo FR01's compact endpoint's
31.4% shrinkage of the radius enclosing the original core mass.
Claiming that torque now supplies the missing contraction cancellation
would require an additional calculation of redistribution and the resulting
monopole response.

## Physical comparisons that remain unavailable

The baseline and compact background dynamical frequencies are approximately 0.07049 and
0.12440 in the same parent time units. Equal pattern-speed ratios therefore
do **not** mean the same absolute bar frequency. Pulse durations also differ:
approximately 283.71 and 160.77 parent time units. These are comparisons at
equal dimensionless forcing protocols, not a common physical bar acting on
two observed populations. No dwarf/spiral/cluster selection follows from
their different responses.

The rotating source is prescribed. Its amplitude, pattern speed and pulse
envelope do not respond to the calculated torque. The finite pulse supplies
a finite measured work, but no physical finite bar reservoir, slowdown,
saturation or back-reaction has been demonstrated. The calculation is
linear in response and quadratic in its work ledger; it does not establish
permanent local heating.

The scalar is instantaneous by an explicit singular-limit assumption.
Finite propagation speed, scalar radiation and the nonuniform vacuum-edge
limit remain separate questions. The microscopic origin of the PN28
potential, the selected phase-space population and cosmological formation
remain open. No value of `B/V`, observed acceleration scale or cluster
normalization is selected here.

The remaining mechanism question is consequently precise: can this
action-derived exchange redistribute the cold component enough to suppress
the unwanted spherical contraction, using the energy and angular momentum
available in a self-consistent baryonic source? This experiment establishes
the exchange channel in a declared limit; it does not yet answer that
regulation question or connect it to a universal acceleration scale.

## Records and final authority

Final primary records are `baseline_basis12_001/result.json`,
`compact_final_k1536_001/result.json`, and `diffuse_l2_001/result.json`,
with `baseline_bare_001/result.json` and `compact_bare_001/result.json` as
bare controls. Earlier `baseline_l2_k1152_001`, `baseline_L64_001`,
`compact_l2_k768_001`, `compact_L64_001` and `compact_basis12_001` records
inform the historical resolution comparisons, not the final primary table.
`README.md` is the authoritative final status, and
`summary_001/summary.json` records the final comparisons. This synthesis
introduces no new run, fitted parameter or numerical selection.
