# W20 — Arrow's theorem, made concrete
COST: S | script: `wacky_voting_paradoxes.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Implement six voting rules (plurality, Borda, Condorcet, IRV, approval, Copeland) and run them all on the
same random preference profiles. Then hunt for explicit paradoxes: (1) a profile where all six give
**different** winners; (2) a Condorcet cycle; (3) an IRV **non-monotonicity** (a voter ranking X higher
causes X to lose — this really happens, find one); (4) a Borda profile where adding an irrelevant
alternative flips the winner. For each, print the actual ballots so the paradox is inspectable by hand.
Then measure frequency: over 10⁵ random 3-candidate profiles, how often does a Condorcet cycle occur?
(Theory says ~8.8% for large electorates with impartial culture — confirm it.)
