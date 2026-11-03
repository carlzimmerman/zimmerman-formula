# KT9_sani_bulge_ml: SANI WORSENS IT, both footings. Sani et al. 2011 at its own kappa_virial = 5 makes KT8's trend larger, not smaller. It goes only if kappa_virial is 3 or 8/3, so the choice of virial factor carries the result. Brightness dependence is not needed

Criteria: `FROZEN_CRITERIA.md` (3322d03b30), alone first, confirmed landed before the run, **not blind**. `kt9.py`, `kt9.out`, `kt9.json`, `kt9_MUTATE.out`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Not a kappa route, so no register row.

32 SPARC bulges, L 2.0e9 to 1.06e11 from V_b^2 R/G at the last radius. Sani's Upsilon there: 0.54 to 1.11, median 0.862, above the standard 0.7. T2 is the slope inside galaxies, dex per dex, 95 percent.

| Bulge Upsilon | rho_DE T2 | rho_crit T2 | rho_DE rms | rho_crit rms |
|---|---|---|---|---|
| E, standard 0.7 | -0.032 [-0.055, -0.006] | -0.017 [-0.041, +0.008] | 0.1709 | 0.1685 |
| **A, Sani, k = 5** | **-0.055 [-0.078, -0.028]** | **-0.041 [-0.064, -0.014]** | 0.1718 | 0.1700 |
| D, constant 0.862 | -0.051 [-0.075, -0.023] | -0.036 [-0.061, -0.009] | 0.1710 | 0.1692 |
| B, Sani, k = 3 | -0.009 [-0.031, +0.013] | +0.005 [-0.017, +0.027] | 0.1723 | 0.1692 |
| C, Sani, k = 8/3 | +0.001 [-0.021, +0.023] | +0.015 [-0.007, +0.037] | 0.1735 | 0.1701 |

Galaxies with bulges alone, row A: -0.078 [-0.107, -0.052], rho_crit -0.062 [-0.092, -0.036].

## Reading
- **The clue isn't confirmed.** At the factor Sani adopts, Sani's bulges are heavier than 0.7, while KT8's trend wants them lighter. On ρ_DE and ρ_crit, A's interval excludes zero.
- **A is about the same as D,** so brightness dependence does almost nothing (A - D = -0.004). Only the level matters.
- **Not killed either.** kappa_virial = 3 or 8/3 removes the trend, by scaling Upsilon to about 0.5, and Sani calls the commonly used values 3 and 8/3 and adopts 5 from full dynamical models, stated good to 0.1 dex. Mdyn is total mass, so stars could be lighter by whatever else lies inside R_e. Removing the trend at k = 5 needs about 30 to 50 percent of Sani's mass to be non-stellar in these bulges (by hand from the medians, not computed). That isn't measured here.
- rms never improves on 0.7. It can't choose between the rows.

## Defect
**MUTATE failed its frozen expectation.** Slope 0.82 was expected to move T2 opposite to A relative to D. It gives MUT - D = -0.042, the same sign as A - D. The mutation is pinned at L = 1e11, so it raises Upsilon at most luminosities (the level change dominates), and D's constant isn't rescaled to its median. The control as written didn't isolate brightness dependence, so "A is about D" rests on rows A and D, not on this control. Exit 1 as designed. c0 here comes from a linear fit, so it differs from KT8's quadratic c0; T2 at 0.7 reproduces KT8's -0.0315 exactly.

L is estimated from the last radius, assuming the bulge is all enclosed there. The relation is extrapolated by SPARC's fainter bulges, and Sani's sample shares no names with the SPARC bulges I checked.
