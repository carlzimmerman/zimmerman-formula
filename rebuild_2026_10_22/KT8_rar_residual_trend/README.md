# KT8_rar_residual_trend: rho_DE TREND, BULGE-DEPENDENT; rho_crit NONE. The trend is small, sits in galaxies with bulges, and disappears at bulge Upsilon 0.5. Bulgeless galaxies show none

Criteria: `FROZEN_CRITERIA.md` (ddceb424b7), alone first, confirmed landed before the run, **not blind**. `kt8.py`, `kt8.out`, `kt8.json`, `kt8_MUTATE.out`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Not a kappa route, so no register row. A pattern, not a cause.

r = log g_obs - log g_pred, x = log g_bar + 10.5, OR mu_2, nothing fitted. Intervals are 95 percent.

| Sample | c0, level at x = 0 (dex) | c1, pooled slope | T2, slope inside galaxies |
|---|---|---|---|
| **rho_DE, all 155** | +0.035 [+0.003, +0.065] | -0.007 [-0.038, +0.023] | **-0.032 [-0.055, -0.006]** |
| rho_DE, 123 bulgeless | +0.022 [-0.015, +0.060] | -0.015 [-0.064, +0.026] | +0.004 [-0.031, +0.041] |
| **rho_crit, all 155** | +0.004 [-0.029, +0.033] | +0.004 [-0.026, +0.034] | -0.017 [-0.041, +0.008] |
| rho_crit, 123 bulgeless | -0.010 [-0.047, +0.028] | -0.004 [-0.052, +0.038] | +0.014 [-0.021, +0.051] |

**How much, rho_DE:** +0.006, +0.035, -0.017 dex at x = -1.5, 0, +1.5, that is +1.4, +8.3, -3.9 percent in g. rho_crit: -0.033, +0.003, -0.020.

**T2 against mass-to-light, rho_DE:**
- bulge 0.5: -0.002 [-0.026, +0.023], trend gone
- bulge 0.7 (standard): -0.032
- bulge 1.0: -0.064 [-0.089, -0.032]
- all x 0.8: -0.007 [-0.032, +0.021]
- all x 1.25: -0.055 [-0.078, -0.030]

rho_crit: bulge 0.5 +0.013, 0.7 -0.017, 1.0 -0.050, so T2 crosses zero between 0.5 and 0.7 (by eye, not fitted). No curvature in the primary row: c2's interval contains 0 on both footings, so my table's "hump" isn't established.

## As a clue
Read the trend as a measurement error: the law wants bulge mass-to-light near 0.5 to 0.6 in place of 0.7. **That is a checkable statement, not a discovery:** an independent bulge M/L can test it, and galaxies with central dynamics would be the place. Not done, no data fetched. Bulgeless galaxies constrain inner slope only over their own range, which reaches less far up in x.

The rho_DE level +0.035 is a separate clue, 8 percent in g, barely excluding 0. It is what KT1 saw as Upsilon near x 1.25 or a higher footing; it can't be split here.

Bulge-dependent doesn't rule out a real effect tied to dense stellar centres. But nothing here separates it from M/L, gradients, beam smearing and non-circular motion.

**Controls:** planted null T2 contains 0, planted +0.03 recovered as +0.026 [0.022, 0.031], MUTATE lowers c0 by 0.12 dex, exit 1. The bootstrap on the shuffled mock is narrow since galaxy-to-galaxy slopes are destroyed; it isn't the real interval's width.
