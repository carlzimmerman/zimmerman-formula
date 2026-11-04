# FN3 amendment A2, post-K2 and before any Stage 1 data: K2 failed as frozen; a population-level check is frozen now

Written after K2 ran on synthetic cubes only (`fn3_k2.out`, `fn3_k2.json`, `fn3_k2_enclosed.out`). No real cube has been fetched or read. kappa = 1/2 FITTED. Not theory closed.

## K2 as frozen
| line | result | frozen line | reading |
|---|---|---|---|
| K2a per galaxy, median abs(Delta_fit - Delta_true) | 0.177 dex | 0.05 | **FAIL** |
| K2b planted +0.30 offset, recovered as a population median difference | +0.282 | 0.30 +- 0.05 | PASS |
| bias, median (Delta_fit - Delta_true) | -0.055 (16-84 %: -0.219, +0.209) | none | reported |
| MUTATE, a0 x 2, median shift | -0.289 | -0.30 +- 0.07 | PASS, bites |

Enclosed baryons recover better per galaxy than stars (median abs error 0.111, 0.119, 0.121 dex at 1.5, 2.0, 2.5 R_e), but not to 0.05 either.

**As frozen, a failed check means no verdict. Stage 1's frozen-as-written label is therefore NO VERDICT (K2a), whatever the cubes show.** Every Stage 1 report states that label first.

## Why the line was wrong for this lane
The graded statistics are a median per z-third (about 24 galaxies) and a slope over 71 galaxies. A per-galaxy 0.05 dex line was set before the per-galaxy precision was known. At matched-filter S/N 30 the stellar mass trades against the free HI surface density and the inclination box, with chi2_red near 1.0 for every fit: a real degeneracy, not a fitter fault. The owner's rule is that tolerances come from the real errors. A2 applies it to the statistic actually graded.

## A2: what is frozen now, before any Stage 1 data
**K2' (population-level), on a fresh synthetic set:**
- Templates: all 71 primary galaxies' released geometry and SED masses, one synthetic each, in the real thirds. New seeds (20261105 + id), not K2's.
- Planted Sigma_HI drawn uniformly in [0, 15] per galaxy (seeded), so the HI degeneracy is tested across its whole prior. Noise as K2 (matched-filter S/N 30). Canonical band planted; drift R0.
- Two planted scenarios on the same templates: flat, Delta_i = 0; and rising, Delta_i = 0.6 (z_i - median z). The rising one is the size of the rise III's law would imply against the band (budget forecast: +0.30, +0.60, +0.71 dex at the thirds' median z).
- Lines: (a) abs(median bias) <= 0.07 dex in every third of the flat scenario (one third of the smallest sigma_cm, 0.206); (b) flat scenario's recovered Theil-Sen slope within 0 +- 0.10 dex per unit z (the slope budget's systematic term is 0.107); (c) rising scenario's recovered slope within 0.60 +- 0.10; (d) MUTATE, a0 x 2 on the flat scenario, median shift within -0.30 +- 0.07.
- If any K2' line fails, Stage 1 issues no A2 label either, and the README says the test can't be done at this S/N with these cubes.

**Stage 1 labels under A2:** the frozen section 7 vocabulary and rules, unchanged, computed the same way, and printed second, after "as frozen: NO VERDICT (K2a)". Each A2 label carries the tag [A2: K2 redesigned after its synthetic failure, before any data].

**Reported beside, not graded:** the enclosed-baryon offset at 2 R_e, log10 of the law's baryons over SED stars + H2 + HI at the fitted Sigma_HI.

## Power, read from the frozen budget before any data
If the cubes follow III's linear law, imposing the band needs Delta about +0.30, +0.60 and +0.71 dex in the thirds. Against sigma_cm 0.21-0.23 dex that is Z about 1.3, 2.6 and 3.1: the level test reaches TENSION, or EXCLUDED only in the top third. The slope is stronger, because the SED scale cancels in it: about 0.65 dex per unit z against sigma_s near 0.13, roughly 5 sigma. If instead the cubes follow the band, both statistics sit near zero. So Stage 1 can tell III's rise from the band through the slope, if K2' passes and the drift and gas readings agree.
