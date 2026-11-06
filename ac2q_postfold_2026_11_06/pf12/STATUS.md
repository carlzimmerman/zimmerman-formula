# PF12 — incoming regularity survives to breakdown; continuation remains open

The packet evolution supplies significantly more of the incoming data than was
previously explicit. It does not supply evolution through the first strong
breakdown. No remaining singular escape has been constructed or proved uniquely
selected, and no universal necessity of an extension is established.

## What the evolution itself preserves

[Independent terminal-trace derivation](review/TERMINAL_TRACE_AUDIT.md) applies
to each fixed sufficiently narrow packet in the PF09 family, up to its first
strong-evolution endpoint. The width-independent compact/variation estimates
remain valid there despite divergence of clock-gradient variables.

| Quantity | Incoming terminal result | Not supplied after breakdown |
| --- | --- | --- |
| r, rapidity | Compact values; unique L1 terminal traces in BV | Continuity or a selected weak evolution |
| A, P | Joint Lipschitz extension; cap and positivity margins | Matching to unknown outgoing fields |
| Clock phi | Uniform Lipschitz extension, bounded timelike gradient | Regular future interface gradient traces |
| Metric | Nondegenerate; incoming continuous first-derivative traces from the null wave equations | A regular future Einstein junction geometry |
| Stress and specified current | Uniformly bounded on the incoming solution | Convergent outgoing side fluxes |
| Layer charge | Shrinking incoming slice charge is O(width), hence zero | A postbreak approximation and side-balance limit |

The metric conclusion uses bounded wave sources and null integration, not merely
bounded first derivatives. The r/rapidity trace uses bounded total variation
and an L1 time-Lipschitz estimate. No new simulation is needed for these analytic
consequences of the previously audited bootstrap.

Thus cap escape, divergent boost/clock magnitude, pre-existing finite sheet
charge, or an incoming metric singularity are not what causes the proved first
breakdown in this family. These quantities remain controlled on the incoming
side. The divergence is in the strong solution's derivatives.

## Two additional tests of possible continuations

[Bounded-positive rough clock](ROUGH_CLOCK_NONACTIVATION.md)
([independent audit](review/MEASURABLE_CLOCK_NONACTIVATION.md)): if the other
PF11 balances and trace identities hold, the no-fed-layer conclusion survives
with an almost-everywhere clock speed bounded above and away from zero. Clock
speed continuity is unnecessary. Losing that continuity alone does not rescue
the layer. This does not prove the remaining side-flux or matching identities.

[Small acoustic corners](SMALL_ACOUSTIC_CORNERS.md)
([independent audit](review/SMALL_ACOUSTIC_CORNERS_AUDIT.md)): at fixed D0=0 backgrounds
with 0<gamma r0²<=1/10, the acoustic interface frame lies strictly inside the
previous exact corner-obstruction range. Sufficiently small regular acoustic
shocks have same-sign flow and cannot satisfy all native scalar, polarization
and normal-stress flux conditions. The u=.001 fixture is in this range.
This excludes that ordinary shock repair, not every BV or continuous weak limit.

## The exact unclosed implication

[Weak-continuation audit trail](WEAK_CONTINUATION_GAP.md) identifies why the
prebreak auxiliary inverse cannot simply be applied beyond breakdown:
its differentiated forcing equations used smooth chain rules. Their measure
products at a jump must be derived from the original native equations, and
the actual corner test is obstructed. An entropy prescription for a selected
subset of equations does not automatically conserve the full coupled stress.

The terminal data are now controlled. What is missing is an existence and
uniqueness theorem for all native equations starting from those data in a
specified singular class. A continuous non-Lipschitz solution or a limit with
irregular side currents, nonmatching fields, or diffuse defects has not been
excluded generally. Neither has one been exhibited. The incoming estimates do
not authorize assuming those future bounds, nor interpreting a missing estimate
as proof of failure.

## Route status and continuation

R1 resolved for the incoming endpoint, not through it. R2 excludes the stated
small regular acoustic corners and removes clock-speed continuity from the fed
sheet theorem. R3 remains open: the full weak formulation, existence and
selection problem cannot be replaced by the prebreak differentiated system.
Next work must either construct such a native continuation with all constraints
and stress balance, or prove every continuation of this packet must enter an
already excluded class. These are deferred open proof obligations, not exhausted
routes. No same-data nonuniqueness or universal action-failure claim is made.

Base research commit 62d56e38ee. This is a partial research checkpoint. Analytic
review records and exact document hashes accompany it; no new numerical run,
physical regularizer, or modified action was introduced. The corner reviewer
also reports a supplementary symbolic derivative check; it is not a new
runner-provenanced experiment or a substitute for the analytic argument.
