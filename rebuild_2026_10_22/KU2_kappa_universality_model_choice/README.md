# KU2_kappa_universality_model_choice: UNIVERSAL on both footings. With the JAM model chosen per galaxy by lowest chi2_dof, slow minus fast at matched M* and sigma_Re is D = +0.023 +- 0.023 (canonical), +0.025 +- 0.024 (alt), about 0.01 dex; KU1's outlier models are the best fit for under 1 percent of galaxies

Criteria: `FROZEN_CRITERIA.md`, alone first, confirmed landed. `ku2.py` (KU1's code, model choice changed), `ku2.out`, `ku2.json`, `ku2_MUTATE.out`, `ku2_MUTATE.json`. No download. κ = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Register K836. 8 s.

6056 galaxies, 536 slow, 27 matched cells (same as KU1).

| | canonical | alt |
|---|---|---|
| D (ln, slow - fast) | **+0.023 +- 0.023** | **+0.025 +- 0.024** |
| sigma: stat / model (best vs second) / M* | 0.019 / 0.005 / 0.010 | 0.020 / 0.004 / 0.013 |
| D with second-best model | +0.029 | +0.029 |
| implied d ln a0 (slow - fast) | +0.075 +- 0.072 | +0.077 +- 0.072 |
| Label | **UNIVERSAL** | **UNIVERSAL** |
| beside, post-hoc: without HDUs 6-7 / only HDUs 6-7 | +0.029 / +0.251 | +0.030 / +0.251 |

Chosen model fractions: HDUs 6-7 are best for 0.4 percent of slow and 0.9 percent of fast galaxies. The classes do pick differently elsewhere (HDU 4: 20 percent of slow vs 9 percent of fast; HDU 11: 13 vs 36 percent), but best and second-best give the same D to 0.006.

## Reading
- **At matched stellar mass and dispersion, slow and fast rotators sit on the same law at r_half to 0.010 +- 0.010 dex.** VS1's +0.12 dex is 5 sigma away from this, so a rotation-driven offset of that size is out on this sample. VS1's four slow rotators were all centrals: environment or small numbers remain possible explanations for it; rotation isn't.
- **For κ:** the implied a0 is the same for both classes to 7.5 +- 7 percent (both footings). That's the precondition for κ being a single number: met at r_half, within these errors.
- **KU1's NO POWER came from two models the data rarely prefer.** HDUs 6-7 give +0.25, but they're the best fit for under 1 percent of galaxies.

## Limits
- r_half accelerations sit near a0 (median y 0.54-0.65), not deep; the boost is modest, so the a0 equality is 7 percent, not 1 percent.
- chi2_dof is very small throughout (median 0.034 for both best and second), so DynPop's errors include generous floors and the choice between nearby models is weak. What the selection does robustly is avoid HDUs 6-7.
- The absolute level is still uncalibrated (median residual +1.1 to +1.4 in ln for both classes; NSA masses stored without an h-convention). It cancels in D to first order but isn't checked. No environment control.

## Checks
C1 536 / 5520 / 27 cells. C2 law reproduced to 0. C3 +0.12 dex injection on slow: D rises 0.2763. C4 every galaxy has a finite chosen and second model. Exit 0. MUTATE (labels shuffled within cells): D -0.016 +- 0.018 and -0.014 +- 0.018, PASS; exit 1.
