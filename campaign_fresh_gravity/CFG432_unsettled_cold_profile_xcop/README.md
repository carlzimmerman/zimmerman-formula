# CFG432: does the unsettled cold mass in X-COP clusters follow the gas? NO

Criteria: `FROZEN_CRITERIA.md`, committed alone first in e1abbabfd. Script: `cfg432_profile.py` (outputs `cfg432.out`, `cfg432_results.json`). MUTATE: `--mutate` (outputs `cfg432_MUTATE.out`, `cfg432_results_MUTATE.json`). kappa = 1/2 is fitted; both footings reported, never pooled. No dark-matter particle; the cold fluid's mass is still required.

**What was tested.** For the 12 X-COP clusters on disk, the unsettled cold mass is M_u(<r) = M_HSE/(1 − b) − M_b − M_ph, with M_ph from the law (nu(y) = 1/(1 − exp(−sqrt y))). The record's hypothesis (CFG371, CFG379) is that M_u tracks the depleted gas, so M_u/M_gas should be flat in r. The rival is a fixed-concentration NFW shape (c200 = 4, no fit). Slopes d ln(ratio)/d ln r were taken over 0.1–1.0 R500, tolerance 0.15.

**Frozen verdict.**
- **Gas tracking is CONTRADICTED.** The gas shape is excluded in all four cells (both footings, b = 0 and 0.3). The slope of ln(M_u/M_gas) is −0.43 to −0.60 at 6–8σ. No more than 3 of the 12 clusters are individually within 0.30 of flat.
- **Headline: DEPENDS ON b / FOOTING** for the NFW alternative:

| cell | gas slope | NFW (c = 4) slope | verdict |
|---|---|---|---|
| canonical, b = 0 | −0.547 ± 0.073 EXCLUDED | −0.176 ± 0.061 (2.9σ) inconclusive | INCONCLUSIVE |
| canonical, b = 0.3 | −0.432 ± 0.071 EXCLUDED | −0.069 ± 0.053 CONSISTENT | NFW-SHAPED |
| alt, b = 0 | −0.595 ± 0.073 EXCLUDED | −0.218 ± 0.063 EXCLUDED | NEITHER |
| alt, b = 0.3 | −0.451 ± 0.071 EXCLUDED | −0.089 ± 0.055 CONSISTENT | NFW-SHAPED |

**Reading.**
- The unsettled mass is much more centrally concentrated than the gas. Median d ln M/d ln r is 1.18 for M_u against 1.86 for the gas, 1.36 for NFW with c = 4, and 1.89 for the phantom.
- M_u/M_gas falls from about 10 at 0.1 R500 to about 2.5 at R500. So the unsettled component is not a gas-tied (baryon-tied) fluid.
- It looks like an ordinary concentrated, collisionless halo. With a 30% hydrostatic bias it matches an NFW shape within tolerance.
- This agrees with CFG440 session 05 (test K: −0.33 against gas + stars over 100–1000 kpc). It extends that result to gas alone, R500 units, b = 0.3 and an explicit tolerance.

**The NFW match is not robust (reported, not decisive).**
- It depends on the assumed concentration. With c200 = 3 the NFW shape is excluded in every cell. With c200 = 5 it is consistent in three of four cells; alt b = 0 is inconclusive.
- X-COP's own NFW-minus-baryons gives −0.08 to −0.22, but it is fitted to the same data.
- The robust result is the negative one: **the unsettled mass does not have the gas's shape**.
- The gas exclusion survives the alternative stellar convention (0.10 M_gas), c200 = 3 and 5, and the 3 relaxed clusters alone (−0.28 to −0.40, about 4σ).

**Controls.**
- C1 discrimination: the NFW and gas shapes differ by 0.50 in slope, against the 0.30 needed. PASS.
- C2 data identity: PASS.
- C3 law identity: PASS.
- Main run: rc 0.
- MUTATE: M-A (planted gas shape) returns GAS-SHAPED, as required. M-B (radii shuffled) returns NEITHER, not a shape verdict, as required. Detected, rc 1.
- M_u > 0 at every grid point in every primary cell.

**Caveats.**
- Hydrostatic masses are inherited forward models. Their radially correlated errors are not propagated into the per-cluster slopes; the stated σ is the bootstrap over clusters.
- Spherical symmetry and enclosed-mass g_b are assumed.
- 5 clusters use an imported stellar ratio.
- b is held constant in r. A bias that rises outward would raise M_u at large radii, but it would need roughly a factor 4 rise in M_u/M_gas from 0.1 to 1 R500 to make it flat. That is not tested here.
- This is a shape test only. It says nothing about the amount of cold fluid, which stays free.
