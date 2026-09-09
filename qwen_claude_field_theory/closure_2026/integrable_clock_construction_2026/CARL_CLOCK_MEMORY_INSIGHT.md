# Carl Zimmerman's paddle/wake research suggestion

Recorded 2026-09-08 during the IC11 construction and cluster/pair investigation.

## Attribution

**Carl Zimmerman supplied the paddle/wake analogy and explicitly asked that it
guide the primordial-clock investigation.** In his words:

> IF YOU PUT A PADDLE IN THE WATER AND PULL BACK AND YOU GET SWIRLS AND THEN YOU
> STOP PULLING THE WATER WILL STILL KEEP PUSHING YOUR PADDLE IN THAT DIRECTION
> IS THIS RELEVANT AT ALL

His contribution is the suggested connection between persistence of a wake
after forcing ends and a possible history-dependent gravitational contribution
from the primordial clock, particularly for clusters and binary galaxies.
Credit for this project-specific suggestion belongs to Carl, not to the coding
assistant or to a later computation that investigates it.

The assistant's mathematical translation is **a hypothesis to test**: the
clock's evolved stress tensor might depend on its initial data and assembly
history, not just the instantaneous baryon density. In a shift-symmetric local
clock action this history can reside in the conserved current and field state;
it does not require inserting a phenomenological time-memory kernel.

This attribution does not establish priority over the scientific literature,
claim that a gravitational medium or this analogy is globally novel, or show
that it explains the data. The clock architecture and its previous derivations
predate this suggestion. The direction of a real paddle's force depends on its
motion and the wake; a persistent push in one direction is not a general law.

## How the suggestion changes the work

The empirical interface must distinguish an instantaneous baryon-only force
from an **action-evolved clock source**. For a restricted Einstein-clock
pressure P(X), the equations to use are

    J^mu = P_X grad^mu T,       nabla_mu J^mu = 0,
    T_clock^(mu nu) = P_X grad^mu T grad^nu T + P g^(mu nu).

These are the conventional variation of a local shift-symmetric pressure,
not new equations attributed to the analogy. In IC11 the relevant metric in
this restricted expression is the Einstein-frame metric, and the auxiliary
equation and physical-metric matter coupling must also be varied; the above
two lines alone are not the full candidate field equations.

The next empirical construction must evolve this state from specified initial
data, solve its physical-metric force, and compare with the required cluster
profiles and galaxy-pair likelihood in
[cluster_pair_clock_target_2026](../cluster_pair_clock_target_2026/TARGET_REPORT.md).
It must also compute energy transfer, drag and orbital decay, rather than
assuming history dependence is observationally harmless. Required source
profiles are not predictions until this evolution produces them.

## Attribution policy for this checkpoint

Carl: framework, physical motivation, exact-law target, and this paddle/wake
research suggestion. Assistant/team: explicit trial pressure corrections,
derivations, software and audits, each with its reported limitations. No claim
of a completed theory or a literature-wide novelty result is made here.
