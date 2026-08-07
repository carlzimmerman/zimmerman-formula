# W14 — The Kelly criterion, and why everyone bets wrong
COST: S | script: `wacky_kelly_criterion.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

For a favourable bet with edge, the growth-optimal stake is f* = (bp − q)/b. Simulate 10⁴ gamblers over
10³ bets at f*/2, f*, and 2f*, on the same random sequence. Confirm: half-Kelly gives ~75% of the growth
with far less variance; **full 2×-Kelly has zero expected growth** (prove that analytically too, it is a
clean identity); and the *median* outcome diverges wildly from the *mean*. Report the median and mean
final wealth for each, and the fraction of gamblers who are down after 1000 bets even at f*. The real
lesson is about log utility and why arithmetic-mean reasoning ruins people.
