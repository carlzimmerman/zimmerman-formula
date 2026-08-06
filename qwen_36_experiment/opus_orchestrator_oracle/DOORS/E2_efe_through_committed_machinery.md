# DOOR E2 — Compute the EFE properly through the machinery the repo already owns
STATUS: OPEN | RANK: 6 | COST: M | KILLS FAST: no

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
tn26's EFE numbers are inserted, not computed (tn23 never uses a_0 at all, and the wide-binary section is
evaluated at 10^50-10^110 pc — a unit error). But the repo **already owns** a validated full-AQUAL solver on
McMillan-2017 baryons. Use it to produce a real dwarf-spheroidal and wide-binary discriminator.

## Why it works with the framework
The EFE is the framework's own prediction and the solver is already validated (M_* to 0.4%, Sigma_* 41.2 against
BR13's 38±4). a_0 is an **input** to it, never fitted — which is exactly the discipline this door needs.

## Concrete first calculation
1. Load the committed AQUAL solver and the McMillan-2017 baryon model.
2. Compute the EFE suppression for a set of dwarf spheroidals with known external fields.
3. Compare the MI realization against the MG realization — the corpus's numbers are gamma_v = 1.137 (MG) vs
   ~1.05-1.10 (MI, a_0-degenerate), so report both.
4. Then price the discriminating power: how many systems at what precision to separate them?

## Settles if / refuted if
CONFIRMS: a dSph or wide-binary observable that separates MI from MG at achievable precision.
CLOSES: MI and MG differ by less than the systematics ⇒ say so, and the EFE stops being sold as a discriminator.

## Known walls — do not rediscover
The EFE prescription **over-suppresses by 1.57x** (Crater II is the calibration) — fix that first or your
numbers inherit it. And the framework's own Crater II miss is 36%; a 38% tolerance once passed it, so pick
tolerances from method precision (hazard H6). Cassini is **not** a clean discriminator: the gamma-pass is
MOND-shared and the Q2 quadrupole is a 3-15sigma tension the AeST realization inherits.
