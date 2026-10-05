# CFG334: can binaries inflate Pal 3's dispersion?

**Verdict (frozen rule, f75660a81): BINARIES EXPLAIN.**

Setup:
- N = 22 single-epoch velocities.
- The intrinsic σ is Newton's 0.75 km/s, at the stellar-population M/L.
- Binary fraction 30%, with Duquennoy & Mayor periods and giant-star truncation.

Result: the measured 1.70 km/s or more comes up in **26%** of draws, and the median measured value is 1.16 km/s. Across all brackets P = 8–47%, depending on binary fraction: 0.1 → ~9%, 0.3 → ~26%, 0.5 → ~44%. So Pal 3's high dispersion is fully consistent with a Newtonian cluster plus an ordinary binary population. Pal 3 is the only cluster that broke CFG332's class-E (Newtonian) fit; without it the fit is 0.27σ.

This tests plausibility, not a measurement. Multi-epoch radial velocities of Pal 3 members would settle it.

## Controls
- **C1 passes.**
- **C2 fails, kept.** With N = 22 and errors larger than σ, the ML estimator runs about 10% low (median 0.67 against 0.75). The same estimator is applied to every simulated sample, so the comparison stays like-for-like.
- **C3 fails on a slip in my frozen number.** The criterion expected K = 15.6 km/s. The correct analytic value for M₁ = 0.8, q = 1 and P = 1 yr is 17.4 km/s: a = 1.17 AU, relative orbital speed 34.85 km/s, the primary's half 17.42 km/s. The code computes it correctly, and the failed row is kept as frozen.
- **MUTATE passes:** with f = 0, P falls below 0.01.

## Run
```
python3 campaign_fresh_gravity/CFG334_pal3_binaries/cfg334_pal3_binaries.py
CFG334_MUTATE=1 python3 campaign_fresh_gravity/CFG334_pal3_binaries/cfg334_pal3_binaries.py
```
(~30 s each)
