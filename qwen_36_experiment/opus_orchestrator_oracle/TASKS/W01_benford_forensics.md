# W01 — Benford forensics on this repo's own numbers
COST: S | script: `wacky_benford_forensics.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
Benford's law: in many natural datasets the leading digit d appears with frequency log10(1 + 1/d), so 1
appears ~30% of the time and 9 only ~4.6%. Fabricated or hand-picked numbers usually fail it. This repo
contains thousands of computed numbers. Do they obey Benford?

## Do
1. Scrape every float from `real_research/reviews/*.out` and from the printed output of the committed
   scripts. Keep only genuine measurements/results (skip integers, indices, check counts, years).
2. Histogram the leading digits. Chi-square against Benford. Also do the second-digit test.
3. Split the corpus: numbers that came from *derivations* vs numbers *quoted from literature*. Do they
   differ? Physical constants famously obey Benford; a chi-square blowup in one subset is interesting.
4. Control: generate the same count of uniform random numbers over the same order-of-magnitude span and
   confirm your test *rejects* them. Without that control the whole thing is meaningless.

## Why it is not just a game
It is a cheap forensic check on a corpus that has already withdrawn six claims. If a subset of numbers is
anomalous, that subset is worth re-deriving.
