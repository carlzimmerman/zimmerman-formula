# W10 — Arnold's cat map: exact recurrence times
COST: S | script: `wacky_arnold_cat.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
The cat map (x,y) → (2x+y, x+y) mod 1 is the textbook chaotic system: positive Lyapunov exponent, mixing,
ergodic. But on an **N×N integer lattice** it is a permutation, so it must return every point to its start in
finite time. Those recurrence times are wildly irregular in N — and that irregularity is number theory, not
chaos.

## Do
1. Implement the map on an N×N lattice for N = 2…2000. For each N compute the **order** of the matrix
   [[2,1],[1,1]] in GL₂(ℤ/N) — the exact recurrence period.
2. Plot period vs N. It is spectacularly non-monotone. Find the N with the *shortest* period relative to N²
   and the longest.
3. Connect it to theory: the period relates to the Fibonacci sequence mod N (the Pisano period), because that
   matrix is the Fibonacci matrix. Verify that identification exactly — it should make the whole plot
   predictable.
4. Then the visual payoff: take an image on a 256×256 lattice, iterate, and confirm it returns **exactly** at
   the computed period. Save frames at 1/4, 1/2, 3/4 of the period to show it fully scrambled in between.

## Why
A system that is provably chaotic in the continuum becomes exactly periodic on a lattice, with a period given
by number theory. It is the best short lesson available in how discretisation changes a dynamical system —
which matters for every numerical result in this repo.
