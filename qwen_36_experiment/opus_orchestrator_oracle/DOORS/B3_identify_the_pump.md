# DOOR B3 — Identify the pump: what physically drives the NESS, and how hard?
STATUS: OPEN | RANK: 7 | COST: S | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
The programme needs `q^2 > q^2_crit ~ 3e-2` to flip the sign. Nothing says what supplies it. Meanwhile the
corpus's own committed script measures the actual KMS violation available from orbital motion:
**8.6e-07 at the galactic v/c ~ 1e-3**, scaling as (v/c)^2 with spread/(v/c)^2 constant to 1.34. That is a
factor ~1e6-1e7 short. Either something else is the pump, or the mechanism does not operate in galaxies.

## Why it works with the framework
Galaxies are where the phenomenology lives, so this is the framework's own consistency question. It uses only
committed machinery.

## Concrete first calculation
1. Substitute the committed circular-worldline retarded Green's function from
   `mi_circular_dS_response_2026.py` for tn22's toy `exp(-dtau/0.1)`.
2. Fit the KMS-violation amplitude `delta_KMS` against v/c across 3 decades.
3. Report the exponent and the amplitude at v/c = 1e-3, and compare to the q^2 the sign flip needs.

## Settles if / refuted if
SETTLED: delta_KMS ∝ (v/c)^2 with amplitude ~1e-6 ⇒ orbital motion is NOT the pump, and q^2 = 3e-2 is a fit
parameter with no physical source. State that plainly.
OPENS / FORKS: if delta_KMS is **v/c-independent**, the driver must be cosmological — which forks into
`a_0(rho_local)`, and that is **already a decisive 13-34sigma null on 175 SPARC galaxies**. So this branch is
falsifiable with data already on disk. Either way you learn something in one script.

## Known walls — do not rediscover
`a_0 ∝ sqrt(G rho_local)` is dead: 1076x too large in the solar neighbourhood, and the environmental fork is
a 13-34sigma null. If your pump requires local density, it is already refuted.
