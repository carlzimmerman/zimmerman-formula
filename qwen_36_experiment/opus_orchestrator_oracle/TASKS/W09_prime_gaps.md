# W09 — Prime gaps: Cramér's model vs the actual maximal gaps
COST: S | script: `wacky_prime_gaps.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
Cramér modelled the primes as random with density 1/log n, predicting maximal gaps near (log n)². The actual
maximal gaps are consistently *smaller*, and Granville argued the true constant differs. Measure it.

## Do
1. Sieve to 10⁸ (segmented sieve — the memory engineering is the point). Find every **maximal** gap: a gap
   larger than all preceding ones.
2. For each maximal gap g after prime p, compute the merit g/log p. Plot merit vs log p.
3. Cramér predicts merit grows like log p; Shanks conjectured g ~ (log p)² exactly. Fit both and report which
   the data prefers over your range.
4. Reproduce the known record list as a correctness check (gaps 1, 2, 4, 6, 8, 14, 18, 20, 22, 34, 36, 44,
   52, 72, 86, …). If your list disagrees with the literature, your sieve is wrong — fix it before fitting.
5. Report the largest merit you find and compare to the record (~41.94 at 1.55e18, far beyond your range).

## Why
It is the cleanest case of a *random model being provably too crude* while still being the best available —
and the deviation is measurable with an afternoon of compute.
