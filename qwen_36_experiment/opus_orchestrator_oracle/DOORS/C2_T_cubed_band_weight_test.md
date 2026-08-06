# DOOR C2 — The T^3 test: can the mechanism produce a MOND scale at all?
STATUS: OPEN | RANK: 3 | COST: S | KILLS FAST: YES | PREREQ: C1 (same script)

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
A finite crossover r needs the gain-band weight to scale as `T^3` against the `1/omega^2` measure in
`delta_m = (2/pi) P int rho/omega^2 domega`. If the band weight is T-independent, then `c1p = 0`, `r = infinity`
and `a_0 = 0` — no acceleration scale exists. This is a one-line regression that can kill the entire
coefficient programme, or license it.

## Why it works with the framework
It is a necessary condition on any mechanism that claims to produce a0, stated in the framework's own
master-formula variables. It presupposes nothing about which mechanism.

## Concrete first calculation
1. From C1's tabulated kernel, extract for each a/H the gain band's **amplitude** and **width**.
2. Regress `log(amplitude x width)` on `log T_eff`.
3. Report the exponent with its fit error.

## Settles if / refuted if
KILLS FAST: exponent < 3 ⇒ the NESS mechanism cannot produce a MOND scale, full stop. That is a clean,
publishable no-go and it costs one script.
CONFIRMS: exponent = 3 within error ⇒ r is finite and C1's number is meaningful.

## Known walls — do not rediscover
The `1/omega^2` measure is what makes delta_m IR-divergent (`delta_m ∝ 1/omega_min` exactly — review verified
10.000x per decade). So C4 must be done before any *magnitude* from this door is quotable; the *exponent*,
however, is IR-safe and is what this door is for.
