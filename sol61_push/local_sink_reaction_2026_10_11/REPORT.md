# A local dark-energy sink cannot be treated as passive vacuum

2026-10-11. Criteria frozen alone at `bf2711f02`; 26/26 symbolic and limiting
checks pass. This is a necessary local-conservation gate for one proposed
receiver class, not a solution or exclusion of candidate B.

## What is already known, and what this check adds

CFG131 and CFG195 already derive that spacetime-dependent pure vacuum has an
exchange current fixed by its gradient. CFG542 gives a local settling-power
source and a canonical scalar partner; CFG630 is evaluating the cosmic ledger.
We do not repeat their background fits or claim the gradient identity is new.

The added diagnostic is the size of the local reaction: a tiny energy transfer
relative to cold REST energy can still require an order-one force relative to
halo gravity. Small cosmic-average energy transfer likewise supplies no local
force bound without the deposition volume, spatial gradients and transport.

## Exact identity and narrowly excluded construction

Use signature (-,+,+,+), coordinate x0=ct, and V as ENERGY density. For pure
vacuum `T_v^{mu nu}=-V g^{mu nu}`, metric compatibility gives

`S_v^nu = nabla_mu T_v^{mu nu} = -nabla^nu V`.

In a local inertial chart this is `(dot V/c, -grad V)`. The matter sector must
receive the opposite current. If `Q=dot V` is positive, matter loses energy
at rate Q and receives force density `+grad V`. The covariant current also
obeys `nabla_[mu S_v,nu]=0`, since it is a scalar gradient.

Therefore the prescription “deposit an arbitrary spatially varying Q locally
in pure vacuum, while giving matter no spatial reaction” is inconsistent.
In a fixed Minkowski frame, zero spatial exchange forces grad V=0 and hence
grad Q=0. This fixed-frame example is not a claim that all evolving fluid frames
or all interactions are forbidden. A homogeneous Q is an explicit allowed
control. The corresponding covariant restrictions are those already studied
in CFG131.

## Size of the missing reaction

For a smooth diagnostic deposit take

`rho_c = rho0 exp(-r^2/(2L^2))`,
`V = V0 + eta rho_c v^2 F(t)`, `F(t)=1-exp(-t/tau)`.

Then the force contribution to the nonrelativistic matter acceleration is

`a_react = grad V/rho_c = -eta F v^2 r_vector/L^2`.

Relative to the declared reference acceleration `g_ref=v^2 r/L^2`,

`|a_react|/g_ref = eta F`,
`delta V/(rho_c c^2) = eta F (v/c)^2`.

The c-squared suppression appears in the rest-energy fraction, not in the
force ratio. At eta=1 and t=tau:

| Illustrative speed | Deposited/rest energy | Reaction/reference acceleration |
|---|---:|---:|
| 200 km/s | 2.8133e-7 | 0.63212 |
| 1000 km/s | 7.0333e-6 | 0.63212 |

These speeds and the deposit are test fields, NOT galaxy/cluster predictions.
The reference is not asserted to be the Gaussian's self-gravity. Keeping rho_c
fixed while its energy changes is not a self-consistent solution; the example
computes the necessary source that any consistent matter evolution would have
to include. eta is not a proposed adjustable theory parameter. No particular
deposition fraction or distribution has been derived for the framework.

## Effective versus intrinsic equation of state

A homogeneous interacting vacuum has intrinsic p/V=-1 and dot V=Q. Rewriting
that evolution as a separately conserved fluid gives
`w_eff=-1-Q/(3HV)`. An effective value below -1 therefore does not by itself
prove a canonical field has negative kinetic energy. This bookkeeping
distinction does not provide an action or cure a singular canonical coupling.
CFG630's developing analysis already distinguishes the effective and intrinsic
equations of state; our result should be used alongside that distinction.

## Consequence for the action search

Do not replace CFG542's singular scalar receiver with a local variable vacuum
and retain the old matter equations. Such a replacement needs the mandatory
momentum reaction, with a self-consistent solution checked against the fixed
settled target. Alternatively a receiver with propagating fields, energy flux
or other non-vacuum stress must derive that stress and its transport from the
same action. Its effect cannot be inferred from the homogeneous energy ledger.
Neither option is supplied by this calculation, and neither automatically
preserves the baryon-only switch or yields a settling rate without new knobs.

The next action-level gate is therefore the **full local four-current**, not
just an integral energy balance: derive its temporal and spatial components
from the proposed action, test regularity through the relevant background,
and evolve the resulting reaction with the cold distribution. A failed pure-
vacuum shortcut does not prove that no other receiver exists.

## Evidence, attribution and limits

`check.py` differentiates the complete stress tensor with x0=ct; checks all four
components, six mixed-derivative identities, opposite matter energy/momentum,
the acceleration and rest-energy ratios, and zero/homogeneous limits. Deleting
momentum exchange, reversing its sign, and dropping an energy c factor are
MUTATE controls. Source and output hashes are in run/manifest.json. No PM job,
external halo machinery, observational fit, or changes to Claude's files.
This tensor identity is independent of a0/kernel; it applies conditionally to
either footing without pooling them. Kappa stays fitted; the full goal is open.

Primary attribution: [De-Santiago, Wands and Wang, arXiv:1209.0563v1](https://arxiv.org/pdf/1209.0563),
equations (1)–(6) and (21)–(23), explicitly give the pure-vacuum gradient exchange
and momentum reaction. The PDF identifies itself as v1 dated 4 September 2012
in its arXiv header, with a differing manuscript date in the typeset body;
the cited equations were checked directly on 2026-10-11. Their vacuum V maps
to our energy density V, with c restored explicitly here. No cosmological fit
or dark-matter particle assumption from that paper is used in this result.
Search scope was the primary interacting-vacuum literature plus local CFG131,
CFG195, CFG542 and CFG630 records. This is an application of known conservation
identities, not a novelty claim. Proof and notation self-review performed by
the same author; no independent agent review.
