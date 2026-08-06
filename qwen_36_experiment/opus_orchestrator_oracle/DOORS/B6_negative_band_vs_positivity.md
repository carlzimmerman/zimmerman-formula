# DOOR B6 — Can a negative band coexist with a stationary, normalizable state?
STATUS: OPEN | RANK: 10 | COST: S | KILLS FAST: YES | PREREQ: B1

> Read `../02_HOUSE_RULES.md` and `../04_FRAMEWORK_FACTS.md` before starting. One door per cycle.
> κ = ½ is FITTED, NOT DERIVED — nothing in this door changes that unless it says so explicitly.

## The door
Review's sharpest structural finding: **the onset of a negative band IS the loss of stationarity**, to better
than 1% (rho_min = +7.9e-3 at 0.99x threshold, -4.7e-2 at 1.01x; fitted growth rate tracks q^2 A - 2 eta to
0.1%). That is suspicious enough to be a theorem rather than a coincidence. Prove it or find the exception.

## Why it works with the framework
If it is a theorem, it tells the programme exactly where NOT to look, and it is publishable as a no-go with a
named class. If it has an exception, that exception is the mechanism.

## Concrete first calculation
1. For the linear Volterra dressing, express rho_min analytically as a function of `q^2 A - 2 eta`.
2. Show whether `rho_min < 0` and `growth rate > 0` are the same condition, or merely coincident at this
   kernel's parameters.
3. Test with a **different** kernel shape (gamma-2, boxcar, two-pole) at matched norm: does the coincidence
   persist? If it does for all of them, that is evidence for a theorem.

## Settles if / refuted if
SETTLED: same condition for every kernel tested ⇒ state it as "of the N tested" and attempt the general proof.
REFUTED: a kernel with a stationary negative band ⇒ go straight to A5 (is it CP?) and C1 (does it carry T?).

## Known walls — do not rediscover
"Of the N tested" is not a theorem (RULE R8). And do not conflate `||q^2 K||_2 > 1` (geometric growth of
partial sums) with a spectral-radius bifurcation — the spectral radius is exactly 0 for this operator.
