# W15 — The 15 pentagon tilings, and the 2017 proof that there are no more
COST: M | script: `wacky_pentagon_tilings.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Exactly **15** types of convex pentagon tile the plane. The 15th was found in 2015 (by computer search);
Rao proved in 2017 the list is complete. Implement the 15 types from their angle/edge constraint sets,
verify each actually tiles (place ~50 tiles per type and check no overlaps and no gaps to 1e-12), and
render them. Then the interesting bit: several types have free parameters — find the dimension of each
family and confirm the total parameter count matches the literature. The check with teeth: a deliberately
perturbed angle must produce a detectable gap.
