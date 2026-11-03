# KT8_rar_residual_trend: FROZEN CRITERIA, committed alone before any script or number

Owner, 2026-11-02: is there a trend in the fit being off, and how much? κ = 1/2 FITTED. Footings never pooled. Not theory closed. **Not blind:** my binned table of median residuals is already seen: flat near +0.05 dex in the middle, lower at the top bins.

## Measurement
SPARC, L232's loader, Upsilon 0.5/0.7, kernel OR mu_2, no fitted parameter, a0 from each footing. r = log g_obs - log g_pred, x = log g_bar + 10.5.

1. **T1, pooled trend:** r = c0 + c1 x + c2 x^2, each galaxy weighted equally (point weight 1/N_gal). Error: 2000 galaxy bootstraps, seed 20261102.
2. **T2, inside galaxies:** subtract each galaxy's mean r and mean x, fit r = c1 x. This removes galaxy-wide offsets (distance, inclination, disc Upsilon as a constant), which T1 keeps. Same bootstrap.
3. **T3, bulgeless:** T1 and T2 on galaxies with no bulge at any point.
4. **T4, Upsilon:** T1 and T2 at Upsilon x 0.8, x 1.25; and with bulge Upsilon alone at 0.5 and 1.0, disc fixed.
5. **Size:** predicted offset at x = -1.5, 0, +1.5 from T1, in dex and as percent in g.

## Labels, per footing
- **TREND:** T2 c1 95 percent interval excludes 0, in T3 too.
- **TREND, BULGE-DEPENDENT:** excludes 0 overall, not in T3.
- **OFFSET ONLY:** c0 excludes 0, c1 in T1 and T2 don't.
- **NONE:** none exclude 0.

A label reports a pattern, not a cause. T2 removes constants, but radial mass-to-light gradients, beam smearing and non-circular motion all correlate with x inside a galaxy, and this lane can't separate them from kernel shape.

## Controls
**Planted null:** mock from the law with shuffled within-galaxy residuals; T2 c1 must contain 0. **Planted trend:** add 0.03 x; T2 must recover it within its 95 percent interval. **MUTATE:** Y = g/s replaced so a0 doubles; c0 must move down by at least 0.1 dex. `_MUTATE`, exit 1. If planted fails, NO VERDICT. No download. Not a kappa route, so no register row. Single thread, minutes.
