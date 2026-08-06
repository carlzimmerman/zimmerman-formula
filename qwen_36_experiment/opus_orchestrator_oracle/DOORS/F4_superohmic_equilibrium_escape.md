# DOOR F4 — Super-ohmic coupling in EQUILIBRIUM: does the NESS detour turn out to be unnecessary?
STATUS: OPEN | RANK: 5 | COST: S | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
Carl's own audit names this and nobody computed it. The Caldeira-Leggett mass shift depends on the bath spectral
density `J(omega) ∝ omega^s`, and the **sign is exponent-dependent**. The programme assumed ohmic (s = 1). If
any admissible `s > 2` gives `delta_m < 0` in **equilibrium**, then the whole NESS detour was unnecessary and q
disappears from the theory entirely.

## Why it works with the framework
It keeps equilibrium, keeps Bunch-Davies, keeps every validated result, and changes only the assumed coupling
spectrum — which was never derived in the first place. It is the cheapest possible escape from the anti-MOND
wall.

## Concrete first calculation
1. Compute `delta_m(s) = (2/pi) P int J(omega) coth(beta omega/2) / omega^2 domega` for `s = 1, 2, 3, 4`.
2. Regularize the IR properly (see C4 — the corrected kernel `rho/omega^2` diverges for the semicircle, which
   is itself a signal that the ohmic assumption is wrong).
3. Report the sign for each s, and which s are physically admissible for a field coupled to a worldline.

## Settles if / refuted if
KILLS THE NESS PROGRAMME AS UNNECESSARY (the good outcome): some admissible s flips the sign in equilibrium ⇒
delete q, delete eta, delete q^2_crit, and the mechanism becomes far simpler and more predictive.
CLOSES: no admissible s flips it ⇒ the anti-MOND no-go **generalises to the whole ohmic family**, which
strengthens A1 considerably and is worth publishing with it.

## Known walls — do not rediscover
The equilibrium wall for the **elementary field** is state-independent (A1: `rho = omega/pi^2` exactly). So this
door is about the **coupling** `alpha(omega)`, not about the field's commutator — do not conflate them, or you
will "prove" A1 again and think you have found something.
