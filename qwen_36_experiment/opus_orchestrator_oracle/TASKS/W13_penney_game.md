# W13 — Penney's game: the non-transitive coin paradox
COST: S | script: `wacky_penney_game.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Two players pick length-3 coin sequences; first to appear wins. **Every** choice can be beaten by another,
non-transitively — so the second player always has an edge. Build the full 8×8 win-probability matrix using
Conway's leading-number algorithm, then verify every entry by Monte Carlo (10⁶ trials, report agreement).
Find the best response to each sequence and the worst first choice (HHH loses to THH 7:1 — confirm the
exact 7/8). Then extend to length 4 and report whether the second player's advantage grows or shrinks.
A rare case where exact combinatorics and simulation can be cross-checked to 3 digits.
