# KU1_kappa_universality_rotators: NO POWER on both footings. Slow minus fast at matched M* and sigma_Re is D = +0.042 +- 0.099; the statistical error is only 0.018, but the ten JAM mass models disagree (two give +0.24, eight give -0.04 to +0.07), so the test can't see a VS1-sized offset

Criteria: `FROZEN_CRITERIA.md`, alone first, confirmed landed. `ku1.py`, `ku1.out`, `ku1.json`, `ku1_MUTATE.out`, `ku1_MUTATE.json`. No download (MaNGA DynPop on disk from LAM1). κ = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K835. 8 s.

6056 galaxies (Qual >= 1 and cuts): 536 slow, 5520 fast, 27 matched cells (0.2 dex M*, 0.1 dex sigma_Re).

| | canonical | alt |
|---|---|---|
| D (ln, slow - fast) | **+0.042 +- 0.099** | **+0.041 +- 0.100** |
| sigma: stat / JAM model / M* | 0.018 / 0.097 / 0.011 | 0.019 / 0.097 / 0.009 |
| D per JAM model (HDUs 2-11) | -0.035 -0.007 -0.002 +0.032 **+0.243 +0.260** +0.011 +0.040 +0.059 +0.066 | same to 0.002 |
| median y at r_half | 0.65 | 0.54 |
| implied d ln a0 (slow - fast) | +0.13 | +0.13 |
| Label | **NO POWER** | **NO POWER** |

## Reading
- **The data have the power; the mass models don't agree.** With any single model the statistical error (0.018) would detect a 0.12 dex offset at more than 5 sigma. Eight models put slow and fast within 0.07 of each other in ln (at most 0.03 dex); one pair of stellar-plus-halo models (HDUs 6-7) puts slow rotators +0.25 high. As frozen, the model spread is the error, so no label beyond NO POWER is issued.
- Read informally, and not as a grade: most models say slow and fast sit on the same law at r_half to about 0.03 dex, well below VS1's +0.12. That would point to VS1's offset being environment (all four were centrals) or small-number scatter, not rotation. To make that a result, the model choice has to be settled first, e.g. by which models DynPop's own quality checks prefer per galaxy.
- **The absolute level is off, beside and not graded:** the median residual is +1.2 to +1.4 in ln (g_obs about 3.5x the law's prediction) for both classes. That's probably the mass inputs (the NSA log masses are stored with no stated h-convention, worth a factor 2, and kcorrect masses run low) plus sphere-enclosed JAM mass, but it isn't checked. It cancels in D to first order, but it's a warning that the absolute inputs aren't calibrated.
- An implied a0 shift is about 3x D here (d ln g / d ln a0 0.31), because r_half accelerations sit near a0, not deep.

## Deviation from the criteria, disclosed
The criteria said NSA masses would be converted from h = 1. The file stores log masses without a stated convention, so no conversion was applied. This affects the absolute level only.

## Checks
C1 536 slow, 5520 fast, 27 cells. C2 law reproduced to 0. C3 +0.12 dex injection on slow g_obs: D rises 0.2763 (want 0.276). Exit 0. MUTATE (labels shuffled within cells): D -0.013 +- 0.024 and -0.012 +- 0.023, within 2 sigma, PASS; exit 1.
