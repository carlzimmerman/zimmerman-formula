# W06 — Collatz stopping times vs the log-normal prediction
COST: S | script: `wacky_collatz_stopping.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
For n even halve it, for n odd take 3n+1. Everything tested reaches 1. The **total stopping time** should,
heuristically, be roughly log n / log(4/3) with log-normal fluctuations, because a random odd step multiplies
by 3/2 on average in log space. Test the heuristic where it fails.

## Do
1. Compute total stopping times for all n up to 10⁷ (memoise aggressively; this is the whole engineering
   content).
2. Plot mean stopping time vs log n. Fit the slope. The prediction is 1/log₂(4/3) ≈ 2.409 steps per bit —
   check it.
3. Histogram the *residuals* around the fit. Are they log-normal? Test it (Kolmogorov–Smirnov). Report where
   the tails deviate.
4. Find the record-setters (numbers whose stopping time exceeds all smaller n). The known list starts
   1, 2, 3, 6, 7, 9, 18, 25, 27, 54, 73, 97, 129, 171, 231, 313, 327, 649, 703, 871… — reproduce it as a
   correctness check on your implementation.

## Why
An unsolved problem where the *statistics* are beautifully well-behaved, and the residual structure is where
any proof would have to bite.
