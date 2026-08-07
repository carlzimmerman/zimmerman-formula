# W17 — How compact is a shape, really?
COST: S | script: `wacky_compactness_metrics.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Six published compactness metrics (Polsby–Popper 4πA/P², Reock A/A_circumcircle, convex-hull ratio,
Schwartzberg, Lee–Sallee, moment of inertia) are used to argue about district shapes. Implement all six.
Then the point: construct shapes where the metrics **disagree maximally** — find a pair of shapes A, B
where metric 1 ranks A > B and metric 2 ranks B > A, and maximise the rank disagreement. Report the
Spearman correlation between all six metrics over 1000 random polygons. A concrete demonstration that
"compactness" is not one property, which is a useful thing to have internalised before trusting any single
figure of merit — including in physics.
