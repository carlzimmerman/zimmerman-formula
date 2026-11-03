# KT10_trend_separation: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: keep going on the trend. κ = 1/2 FITTED. Footings never pooled. Not theory closed. **Not blind:** KT8 and KT9 seen. This is a measurement; nothing here is derived.

## Question
KT8's within-galaxy slope T2 (rho_DE -0.032, rho_crit -0.017, Upsilon 0.5/0.7, OR mu_2) is confined to galaxies with bulges. Does it follow bulge mass share, or radius and resolution?

## Tests, 32 bulge galaxies unless stated, 2000 galaxy bootstraps, seed 20261102
- **S1, joint:** inside galaxies, r on x and f_b together, f_b = bulge share of Vbar^2.
- **S2, disc-side points only:** T2 on points with f_b < 0.1, and all galaxies with those points.
- **S3, angular cut:** T2 keeping points with R/D >= 15 and >= 30 arcsec, all 155 galaxies.
- **S4, splits:** T2 for bulge galaxies, by distance above/below their median, by inclination above/below 75 deg, by Q = 1 against Q > 1 (from `SPARC_Lelli2016c.mrt`).
- **S5, what each galaxy asks for:** per galaxy best bulge Upsilon on a grid 0.1 to 1.5, step 0.05, minimising that galaxy's mean r^2 about zero, with disc 0.5. Report median, 16-84 percent, number at grid edges, bootstrap on the median, correlation with log L_bulge and log D. Repeat minimising within-galaxy scatter about the galaxy's own mean, which ignores level. Both footings.

## Labels, per footing
- **FOLLOWS BULGE SHARE:** S1 f_b interval excludes 0, S1 x interval contains 0, and S2's T2 contains 0.
- **FOLLOWS RADIUS OR RESOLUTION:** S1 x excludes 0, f_b contains 0, or S3 removes T2 at 15 or 30 arcsec while f_b doesn't carry it.
- **NOT SEPARATED:** otherwise.

FOLLOWS BULGE SHARE points to bulge mass, but not only to Upsilon: a gradient inside the bulge or a real effect in dense centres fit too. S5 is what the law asks for, so it's not an independent measurement.

## Controls
**Planted mass error:** mock from the law with true bulge Upsilon 0.5, analysed at 0.7, real scatter. S1 must give f_b excluding 0 and S5 must recover 0.5 inside its 68 percent range. **Planted radial error:** add -0.03 x inside galaxies with bulge Upsilon correct. S1 x must exclude 0; f_b should contain 0. **MUTATE:** shuffle f_b inside galaxies, S1 f_b must contain 0; `_MUTATE`, exit 1. If a planted test fails, NO VERDICT. No download. No register row.
