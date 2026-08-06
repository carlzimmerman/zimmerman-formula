# DOOR A5 — Is the "MOND state" a physical density matrix at all?
STATUS: OPEN | RANK: 4 | COST: S | KILLS FAST: YES

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
A negative spectral density in the Caldeira-Leggett master equation means a **negative diffusion
coefficient**, which generically means the dynamical map is not completely positive — i.e. the state that
produces MOND may not be a physical state at all. This has never been tested and it can kill or vindicate the
whole negative-band strategy in ~150 lines.

## Why it works with the framework
It is a consistency test on the mechanism, not a change to it. If it passes, the negative-band route is
legitimate and A2/A3 become much more valuable. If it fails, you have saved every future cycle spent hunting
negative bands, and you can say so publicly with a proof.

## Concrete first calculation
1. Write the CL master equation the programme uses, with a band where rho < 0.
2. Extract the Kossakowski matrix (the coefficient matrix of the dissipator).
3. Compute its eigenvalues. Complete positivity requires all >= 0.
4. Do it as a function of band depth and width, and find the boundary.

## Settles if / refuted if
SETTLED: any negative band of the depth MOND needs makes an eigenvalue negative ⇒ **not CP ⇒ the MOND state
is unphysical**, and the mechanism needs a different route entirely (not a deeper band).
OPENS: CP survives up to some band depth — report that depth and compare it to what MOND needs. That number
is directly usable in D4.

## Known walls — do not rediscover
Note the corpus already has a related bound: `mu_eff = 1 + rho/2 > 0` requires `rho > -2`, and tn18 sits at
80% of that. So there are TWO independent caps and you should report both.
