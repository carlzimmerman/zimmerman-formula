# CFG342: foreground contamination of the UFD samples

**Verdict (frozen): NOT.**

With the standard membership window, W = max(3 sigma, 10 km/s), a median UFD would need **29%** of its velocity sample to be foreground interlopers to fake the excess. Typical residual contamination after Gaia proper-motion and metallicity cuts is a few percent (provisional). Only 10% of the UFDs need 5% or less.

With a wider window (W = 5 sigma) the need drops to about 10%. But interlopers that far out are exactly what the published sigma-clipping removes, so that case does not apply to clipped published dispersions.

The estimator is the most favourable to the escape: a second-moment mix with no clipping.

Controls: C1 and C2 pass (the synthetic mix is recovered exactly). MUTATE passes.

Run: `python3 campaign_fresh_gravity/CFG342_ufd_contamination/cfg342_contamination.py` (CFG342_MUTATE=1 for the control).
