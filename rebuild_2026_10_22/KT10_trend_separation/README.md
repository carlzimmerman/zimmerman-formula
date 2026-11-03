# KT10_trend_separation: rho_DE FOLLOWS RADIUS OR RESOLUTION by the frozen rule, rho_crit NOT SEPARATED. I read both as not separated: bulge share and radius can't be told apart in SPARC, and the galaxies' own asks disagree

Criteria: `FROZEN_CRITERIA.md` (9a43f579f5), alone first, confirmed landed before the run, **not blind**. `kt10.py`, `kt10.out`, `kt10.json`, `kt10_MUTATE.out`. No download. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. No register row. **A measurement; nothing here is derived.**

| Test | rho_DE | rho_crit |
|---|---|---|
| S1 joint, x slope | -0.021 [-0.073, +0.019] | -0.007 [-0.059, +0.031] |
| S1 joint, f_b coefficient | -0.095 [-0.195, +0.038] | -0.087 [-0.186, +0.046] |
| S2 disc-side points, 7 bulge galaxies | -0.008 [-0.056, +0.085] | +0.007 [-0.040, +0.094] |
| S3 all points | -0.032 [-0.055, -0.006] | -0.017 [-0.041, +0.008] |
| S3 >= 15 arcsec | -0.023 [-0.048, +0.005] | -0.009 [-0.033, +0.018] |
| S3 >= 30 arcsec | -0.010 [-0.031, +0.014] | +0.003 [-0.018, +0.026] |
| S4 near / far, 16 each | -0.066 / -0.030 | -0.050 / -0.014 |
| S4 Inc > 75 (8) / <= 75 (24) | -0.055 / -0.045 | -0.040 / -0.029 |
| S4 Q = 1 (22) / Q > 1 (10) | -0.021 / -0.071 | -0.005 / -0.056 |
| S5 Upsilon asked, level and shape | 0.80 [0.60, 0.95], 9 at edges | 0.725 [0.55, 0.875], 8 |
| S5 Upsilon asked, shape only | 0.50 [0.40, 0.75], 9 at edges | 0.55 [0.40, 0.80], 8 |

## Reading
**The rho_DE label overreads.** The S3 clause fired, but cutting small angles also removes the bulge-dominated points, so the cut can't tell resolution from bulge. In S1 both coefficients contain zero: the two regressors are too collinear to split, though both planted tests split cleanly with mocks of known cause, so this is the data's limit and not the method's. The trend is also stronger in nearer, better-resolved galaxies, the opposite of what simple beam smearing gives, with overlapping intervals. Lower-quality rotation curves carry more of it: -0.071 against -0.021.

**The new finding is the S5 disagreement.** Slope alone asks for bulge Upsilon near 0.5. Slope plus level asks for 0.73 to 0.80, close to the standard 0.7 and within reach of Sani's 0.86. So the clue that bulges are lighter comes only from the inner slope, and the level pulls the other way. One constant bulge Upsilon doesn't naturally give both. A mass-to-light gradient inside the bulge (heavier outside, lighter in the centre, or the reverse) would be one way; not tested. About a quarter of galaxies hit a grid edge, so per-galaxy values are poorly set. S5 is what the law asks, not independent evidence.

## Controls and defects
Planted mass error: f_b -0.123 [-0.162, -0.068], S5 median 0.50. Planted radial: x -0.031 [-0.049, -0.017], f_b contains 0. MUTATE: shuffled f_b -0.005 [-0.027, +0.015], exit 1. All as stated.

The first run crashed: my fixed-column table parser failed silently, every D was nan, and S3 had no points. Fixed by splitting on whitespace. All outputs are from the fixed script.
