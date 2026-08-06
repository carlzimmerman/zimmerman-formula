# DOOR B5 — Derive eta from de Sitter QFT instead of hardcoding it
STATUS: OPEN | RANK: 8 | COST: M | KILLS FAST: no

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
The entire claimed threshold is the hand-picked damping rate `eta = 0.01` at `tn16:114`. Review verified
`2 eta / A` tracks the published threshold exactly across four decades (0.00199 / 0.0199 / 0.199 / 1.99). So
**q^2_crit is eta in disguise.** If eta can be derived from dS QFT — it is the imaginary part of the
self-energy / the quasinormal damping rate of the relevant mode — then the threshold becomes a prediction
instead of a fit.

## Why it works with the framework
eta is a property of the dS background the framework already assumes. Deriving it adds no parameter and
removes one.

## Concrete first calculation
1. Identify what eta is meant to be physically: the retarded propagator's damping rate for the coupled mode.
2. For a scalar of mass m in dS_4, the quasinormal frequencies are known in closed form
   (`omega_n = -i H (n + 3/2 ± nu)` type). Extract the damping rate and express it in units of H.
3. Compare to the hardcoded 0.01, and recompute the threshold `2 eta / A` from the derived value.
4. Report the derived q^2_thr and whether it is above or below the sign-flip requirement.

## Settles if / refuted if
SETTLED: derived eta gives a threshold, and either it admits a stationary MOND window or it does not — either
way the number is no longer a knob.
REFUTED / BLOCKED: eta is not determined by the background alone (e.g. it depends on the coupling you were
trying to constrain) ⇒ circular; say so and close the door.

## Known walls — do not rediscover
Do not fit eta to make a window appear. That is the circularity Carl's own audit already flagged in q^2_crit.
