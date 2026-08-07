# W05 — Buffon's needle, and the bits-per-throw of Monte Carlo
COST: S | script: `wacky_buffon_bits.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
Drop a needle of length L on ruled paper with spacing d ≥ L; the probability of crossing a line is 2L/(πd),
so counting crossings estimates π. It is a famously *terrible* estimator. Quantify exactly how bad, then fix
it.

## Do
1. Implement the naive estimator. Run 10³, 10⁶, 10⁹ throws (vectorised). Report the estimate and its error.
2. **The interesting quantity: how many throws for k correct digits?** The error falls as 1/√N, so each digit
   costs 100× the throws. Derive the constant, then verify it empirically. Report throws-per-digit.
3. Compute the *information* content: each throw is one bit (cross / no-cross), so N throws give at most N
   bits, but you extract only ~½log₂N bits of π. Quantify the waste.
4. Then apply **variance reduction**: use the needle's angle (stratification / antithetic variates / the
   "Buffon–Laplace" grid version). Measure the variance ratio against naive. A factor of 3–10 is achievable.

## Why
It is the cleanest demonstration of why Monte Carlo convergence is the enemy, and the bits-per-sample framing
is a genuinely useful habit.
