# W18 — The birthday problem's ugly cousins
COST: S | script: `wacky_birthday_variants.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Everyone knows 23 people for a 50% shared birthday. Compute exactly, and verify by simulation:
(1) the **near**-birthday problem (within 1 day) — the answer drops to 14, confirm it;
(2) the **triple**-birthday problem (three people share) — 88, and it needs care;
(3) the **strong** birthday problem (everyone shares with someone) — 3064;
(4) the version with **real** birth-date distributions rather than uniform (September is overrepresented) —
does non-uniformity help or hurt? Prove the direction, then measure the size.
Report each exactly and by Monte Carlo, and state the sample size needed for 3-digit agreement.
