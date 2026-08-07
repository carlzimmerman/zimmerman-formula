# W08 — Zipf's law on this repo's own commit messages
COST: S | script: `wacky_zipf_commits.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
Zipf: word frequency is inversely proportional to rank, f ∝ 1/r^s with s ≈ 1 for natural language. This repo
has a large, unusual corpus — hundreds of long technical commit messages by mixed human and model authors.
Does it obey Zipf, and does the exponent differ from ordinary English?

## Do
1. Extract all commit messages (`git log --format=%B`). Tokenise, lowercase, strip punctuation.
2. Rank-frequency plot on log-log. Fit s by maximum likelihood (not least squares on the log-log — that is
   the classic mistake; use the discrete power-law MLE).
3. Compare s against the ~1.0 typical of English prose. Report the deviation.
4. Then something genuinely diagnostic: split by author (`%an`) and compare the exponents and the top-50 word
   lists. Model-authored technical prose should be measurably more repetitive (lower entropy per token) —
   compute the per-token entropy for each author and report it.
5. Control: run the same pipeline on a chunk of ordinary English text and confirm you recover s ≈ 1.

## Why
Silly premise, real measurement — and the per-author entropy comparison is a legitimately interesting
artefact of how this corpus was written.
