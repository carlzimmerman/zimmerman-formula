# Cold energy and horizon research checkpoint

The geometric connection is precise, but the physical conversion and baryon
selection mechanism remains unresolved. This checkpoint consolidates six
investigations completed on 14 October 2026. It preserves conditional successes,
failed routes, numerical limitations, and executable evidence.

## What the geometry establishes

For vacuum curvature length L, gravitational mass length r_g = 2GM/c², and
a₀ = αc²/L, the galaxy transition radius obeys

    r_M² = r_g L / (2α),     α = sqrt(3/(32π)).

This geometric mean relation was already in the repository. In a
Schwarzschild–de Sitter vacuum, the black hole and cosmological horizon radii
satisfy r_b² + r_b r_c + r_c² = L². Neither identity supplies a carrier,
conversion rate, or preference for particular baryons. A galaxy's formal mass
length r_g does not imply an actual black hole horizon.

The actual future event horizon and the vacuum curvature length are different.
For an expanding, spatially flat Einstein cosmology with conserved total
stress, nonnegative pressureless matter, sourced pure vacuum with nonnegative
production, and a finite future event horizon, H decreases and the event
horizon grows. Consequently a₀ proportional to sqrt(ρ_vac) cannot share the
same constant-coefficient history as a₀ proportional to 1/R_event, except in
the de Sitter limit. The conserved MD14 diagnostic gives ratios at z = 2 of
0.84987 and 1.43992 respectively. See the
[derivation and independent verification](../claude_bh_followthrough_2026_10_14/HORIZON_TREND_PROOF.md).

## Which baryons participate

The retained universal source action responds to baryon density. It does not
derive a distinction between stars, neutral or molecular gas, and hot plasma
at equal density. “Condensed baryons” is a phenomenological grouping in this
work, not a newly identified baryon species. Existing phase tags retain
history; they do not establish a microscopic selector.

Supported warm carrier profiles demonstrate conditional local attachment.
They do not establish finite halo formation, cooling, or selective attachment.
The [selection investigation](../cold_baryon_selection_2026_10_14/RESULT.txt)
retains gas participation, hot gas overlap, and the limits of light-carrier
thermal coupling. No specific baryon species has been established as the
exclusive tether anchor.

## What the transfer action achieves

The explicit candidate includes a canonical scalar, α φ times the
Gauss–Bonnet invariant, and a scalar-dependent cold particle mass, with baryons
minimally coupled. Its reciprocal energy and momentum exchange is derived.
Regularity at both future horizons selects a scalar drift in a frozen metric;
including the Gauss–Bonnet stress balances the flux difference against stored
potential energy. The zero-slope foundations are known literature results.

This does not yet supply one working theory. Controlled weak black hole
sources produce too little potential pumping in the assigned examples. A
designer cold-only background with nearly vacuum-like scalar pressure develops
large additional forces and fast growth in the tested frozen perturbation
block. Letting the vacuum scale relax freely in the local tether energy erases
the galaxy force law. A canonical gradient-controlled comparison preserves
the scale across an assigned galaxy, but uses a supplied cosmological boundary
and omits the black hole and cold-mass source terms in that patch. Different
comparisons use different potentials. See the
[full action investigation](../horizon_transfer_action_2026_10_14/REPORT.md).

## Latest Claude results

At repository commit e1cde1cf0, Claude's
[event horizon branch](../../campaign_fresh_gravity/CFG778_sealed_event_horizon_branch/README.md)
reports a z = 2 ratio near 1.46, consistent in direction and scale with the
1.44 sourced-background diagnostic. Its frozen observational predictions
remain unchanged by this checkpoint.

Claude's [FRB analysis](../../campaign_fresh_gravity/CFG779_frb_baryon_survival/README.md)
reports a fitted mean dispersion amplitude B = 1.064 with interval
[1.010, 1.122], and strong tension with the two tested baryon-consuming
histories. These are conditional likelihood results with fixed background,
diffuse fraction, and host assumptions; its 5 percent systematic floor is
assigned. Its Croker-like comparison uses an MD14 shape rather than reproducing
the Trinca history. We have inspected this result but have not independently
reproduced that likelihood here. Its cold-only comparison is post hoc and
does not establish black hole conversion.

In our conserved MD14 comparison, cold-only transfer leaves baryons intact,
uses about 10.6 percent of the initial cold reservoir, and changes the global
cold-to-baryon ratio from 5.364 to 4.7947. The partition is assumed, not derived.

## What remains to close the mechanism

One simultaneous action must select the source and receiving components,
include spatial transport and reciprocal recoil, retain the galaxy tether law,
and pass scalar, carrier, and metric stability checks. It must then derive
the cosmological normalization and finite carrier formation. Neither the
fitted κ nor the abundance has been derived. A homogeneous production history
alone cannot close this problem: a pure vacuum stress requires transfer
Q_ν = −∂_ν V, including its spatial component.

## Evidence and reproduction

[canonical_runs.json](canonical_runs.json) identifies 16 canonical runs with
888 passing checks. These count scoped algebraic and numerical assertions
across different comparisons, not independent observational confirmations or
a certificate for one complete physical theory. Earlier failed runs remain
alongside their corrections.

From the repository root, run:

    python3 sol61_push/cold_horizon_checkpoint_2026_10_14/verify_checkpoint.py

This checks recorded input and output hashes and the canonical check counts.
The three small pre-existing untracked input documents are preserved under
`input_snapshots/`, with original paths and hashes in `snapshot_index.json`;
the verifier uses those exact copies when the original path is absent. It does
not restore or overwrite other chats' work. All remaining declared inputs
belong to this checkpoint or the existing tracked repository. Hash validation
does not execute the mathematics or establish dependency closure of arbitrary
Python imports. Fresh execution receipts are in `rerun_receipt.json`.
