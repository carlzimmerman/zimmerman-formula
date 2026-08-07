# W11 — Ramanujan's π series and the cost of a digit
COST: S | script: `wacky_ramanujan_pi.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Compute π by: Leibniz (1 digit per ~5 terms... eventually), Machin, Ramanujan's 1914 series, and
Chudnovsky. For each, plot **digits gained per term** and per second, with mpmath at 10,000 digits.
Chudnovsky gives ~14.18 digits/term — verify that constant. Then the punchline: compare against the
**Bailey–Borwein–Plouffe** formula, which computes the *n*-th hex digit without the preceding ones, and
confirm digit 10⁶ matches a full computation. A cheap lesson in how much algorithm beats hardware.
