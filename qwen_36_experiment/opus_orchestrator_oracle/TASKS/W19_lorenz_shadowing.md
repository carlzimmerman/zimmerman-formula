# W19 — How long is a chaotic prediction good for?
COST: M | script: `wacky_lorenz_shadowing.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

Integrate the Lorenz system at two precisions (float64 and mpmath 50 digits) from the same initial
condition. Measure the time at which the trajectories separate by 1 unit. Then the real question: that
separation time should scale as **(1/λ)·ln(1/ε)** with λ the largest Lyapunov exponent — measure λ
independently (Benettin's algorithm) and confirm the log scaling over 6 decades of ε. Then compute the
**shadowing** distance: even though trajectories diverge, does a true orbit stay near your numerical one?
Report the practical horizon in Lyapunov times. Directly relevant to trusting any long numerical
integration, including W03's.
