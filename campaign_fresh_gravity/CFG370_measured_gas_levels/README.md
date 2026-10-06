# CFG370: do MEASURED gas cooling times give the three retention levels? (no fit)

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 8e29c607b.

**Frozen verdict: FAIL** (as computed, with cm12's cooling copied verbatim): MW 0.79, groups 0.997, clusters 0.998, against 0.14 / 0.60 / 0.576.

## Bug found (POST-FREEZE 1, labelled): cm12's cooling normalisation is 10x too low
Tozzi & Norman's T^0.5 term is bremsstrahlung, a physical floor. At 1 keV, free-free (g_ff = 1.2) is 5.80e-24 erg cm^3 s^-1. The TN term matches it exactly with a 1e-22 unit (ratio 1.00), but is 10x BELOW the floor with cm12's 1e-23. So cm12 (sonnet55_push/cold_mass/cm12_cooling_step.py) and CFG369, which copied it, under-cool by x10. This is reported to the orchestrator (cm12 is its file and is not edited here); CFG369's README carries the forward fix.

## Corrected results (POST-FREEZE, labelled; the frozen FAIL stands)
| reading | MW (30 kpc) | groups (R500) | clusters (R500) | verdict |
|---|---|---|---|---|
| local at the anchor radius (the frozen reading) | **0.095** | 0.969 | 0.976 | FAIL (MW only) |
| enclosed average within the anchor radius | 0.017 | **0.719** | 0.747 | FAIL (groups only) |
| measured | 0.14 +- 0.05 | 0.60 +- 0.15 | 0.576 +- 0.15 | |

- **The galaxy floor comes out with no fit.** The Milky Way's measured hot halo (Miller & Bregman 2015) cools in t_cool(30 kpc) = 4.4 Gyr (2.3-6.8 over T = 1.5-2.5e6 K). So tau/t_cool = 2.36 since z = 2, and e = e^-2.36 = 0.095 (0.02-0.22 over the T bracket). That is the record's floor e^-n = 0.135, whose n = 2 was FITTED in L191, now produced by the measured gas.
- **Groups and clusters do not.** Their R500 gas is too thin to cool (t_cool ~ 330-420 Gyr corrected). Cooling predicts them almost fully unsettled (0.97), but they retain 0.6. Only the enclosed-average reading (inner gas cools) brings groups to 0.72; clusters stay at 0.75, just outside the band. No single reading passes all three.
- **CFG369 corrected (POST-FREEZE 2):** the rate pincer now passes only in the R2 / f_hot 1 cells (MW 3.2 / 2.5 H_L, cluster 0.02 H_L). Levels still fail: MW 0.15 / 0.23 is right, groups 0.96 against 0.60.

**Reading.** Cooling-keyed settling explains the GALAXY level (about e^-2) from measured gas, with no fitted number. It does NOT explain why groups and clusters hold only ~60% of their share instead of ~97%. That 40% must be fluid the groups never collected (the reservoir / accretion side, CFG365-366), not fluid that settled.

Controls: C1 (cm12 crossing reproduced) and C2 pass. MUTATE (cooling x100) moves every number (MW 0.79 -> 0.00, groups 0.997 -> 0.73) but leaves the verdict category at FAIL. So the frozen "verdict must change" premise is NOT met (disclosed). rc 1.
Sources: [Miller & Bregman 2015](https://iopscience.iop.org/article/10.1088/0004-637X/800/1/14); Lovisari+2015 (repo TSV); X-COP (repo FITS).
