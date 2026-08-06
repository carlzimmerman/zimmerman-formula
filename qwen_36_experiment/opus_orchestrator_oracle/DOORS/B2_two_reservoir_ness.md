# DOOR B2 — A genuine two-reservoir NESS from the framework's own two temperatures
STATUS: OPEN | RANK: 6 | COST: M | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
A real non-equilibrium steady state needs **two baths at different temperatures and a current between them**.
The framework already owns exactly two temperatures: the Gibbons-Hawking `T_GH = H/2pi` and the acceleration
temperature `T_a = a/2pi`. Deser-Levin's `sqrt(a^2+H^2)/2pi` is their *equilibrated* value — a NESS is
precisely what you get when they are **not** equilibrated. Nothing in tn14-tn26 built this; the "NESS" there
is a KMS-violating ansatz inserted into a Wightman function.

## Why it works with the framework
This is the framework's own structure, not an import. The two temperatures are already there, and the object
that interpolates them (Deser-Levin) is already validated from a computed response
(`mi_circular_dS_response_2026.py`, to 1e-15). The door asks what happens *off* that equilibrated point.

## Concrete first calculation
1. Two-bath Lindblad for the detector: one bath at T_GH, one at T_a, with rates gamma_GH and gamma_a.
2. Solve for the steady state. Compute the effective occupation and the entropy production (which must be
   > 0 for a genuine NESS — that is your check that it IS one).
3. Then couple the detector to the **difference** (current) combination and compute rho.
4. Report the threshold in terms of `gamma_a / gamma_GH`, not eta.

## Settles if / refuted if
SETTLED (likely, and worth knowing in ~100 lines): the two-bath steady state has
`n_eff = (gamma_1 n_1 + gamma_2 n_2)/(gamma_1 + gamma_2) >= 0`, so no inversion ⇒ closes by theorem.
OPENS: if it escapes, **the threshold becomes gamma_a/gamma_GH, which is physical, replacing the hand-picked
eta = 0.01** that currently sets q^2_crit entirely. That alone would be progress.

## Known walls — do not rediscover
Do not call something a NESS without computing entropy production. And note the review's finding that the
linear vertex supplies **exactly zero** KMS violation — so the coupling must be composite (A3) or the sector
bounded (A2) for this to have anything to work with.
