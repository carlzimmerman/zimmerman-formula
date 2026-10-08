# CFG436: T16's z-slope discriminator on CHEX-MATE (door 10)

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 1ce251561. Script: `cfg436_zslope.py` (~12 s, one niced process). Outputs: `cfg436_zslope.out`, `cfg436_results.json`; MUTATE: `cfg436_zslope_MUTATE.out`, `cfg436_results_MUTATE.json`. Data: `../../../_external_data/cfg436_work/` (FETCH_LOG.md: six arXiv source bundles, 4-11 MB each).

## Verdict: NOT POSSIBLE (primary). The indicative two-stack row is NON-DIAGNOSTIC.
DeepSeek's T16 registered one question: do cluster deficits (def-A, x = unsettled cold mass per cosmic share at R500) stay fixed with redshift (saturation), or grow toward low z (slow-rate settling)? Answering it needs per-cluster gas masses and total masses across z.
- CHEX-MATE has not published per-cluster gas masses or gas fractions. The script scanned 31 tables in 13 source files of six CHEX-MATE papers (2021 overview, HIGHMz entropy, UPP/masses, eta_T, simulations, baryonification). It found no gas-mass column in any observational table.
- The September 2026 baryonification paper (arXiv 2609.09144) states that "no gas fraction measurements or individual three-dimensional electron density profiles have been obtained for the CHEX-MATE clusters".
- The CHEX-MATE web site did not resolve, and VizieR holds only an N_H table (J/A+A/678/A181).

**What is missing:** per-cluster M_gas,500 (or f_gas) for the CHEX-MATE clusters, with a total mass (hydrostatic, weak-lensing or dynamical) on one footing whose z-dependence is calibrated.

## Registered predictions (computed; usable when data appear)
| lambda | x(bin4, z 0.43)/x(bin3, z 0.234) | x(0.6)/x(0.05) | d ln x/dz (fixed-density variant) |
|---|---|---|---|
| 0.0073 (cluster window low) | 0.862 | 0.653 | -0.77 (-1.32) |
| 0.0123 (window midpoint, PRIMARY) | 0.864 | 0.659 | -0.75 (-1.29) |
| 0.0172 (window high) | 0.867 | 0.665 | -0.74 (-1.27) |
| 0.016 (universal) | 0.866 | 0.664 | -0.74 |
| 0.028 (MW floor) | 0.873 | 0.679 | -0.70 |

- **Saturation** predicts 1.000 and slope 0.
- **Slow-rate settling** predicts that a z = 0.6 cluster carries about two-thirds of the deficit of a z = 0.05 cluster. This hardly depends on lambda, because settling is in its linear regime: lambda r tau is 0.09-0.33.
- C3 reproduces T16's rate x tau = 11.64 against its 11.74, the small gap coming from tau(0) = 10.23 against 10.3 Gyr.

## Indicative row (secondary, never decisive)
The baryonification paper gives model gas fractions for four CHEX-MATE stacks, in a figure only. They were extracted exactly from the vector PDF, calibrated on its own ticks (residuals below 0.001 pt):
- Bin 3 is the 3rd marker, M 1.19e15 and f_gas 0.109 +- 0.010.
- Bin 4 is the 4th marker, M 1.14e15 and f_gas 0.118 +- 0.010.
- The two markers are not labelled. Assignment A follows the drawing order; B swaps them.

| | x(bin3) | x(bin4) | R_obs | sigma_R | power gate (needs sigma_R <= 0.068) |
|---|---|---|---|---|---|
| A, canonical | 0.844 | 0.797 | 0.944 | 0.163 | FAIL |
| A, alt | 0.784 | 0.743 | 0.948 | 0.170 | FAIL |
| B, canonical | 0.755 | 0.886 | 1.173 | 0.206 | FAIL |
| B, alt | 0.698 | 0.831 | 1.191 | 0.219 | FAIL |

- The row is NON-DIAGNOSTIC in all 12 cells (2 assignments x 2 footings x 3 f_star values). The errors are about 2.4x too large to separate 0.864 from 1.
- Under A the data sit between the two predictions. Under B they lean the other way (deficit larger at high z), at 0.8 sigma.
- Cross-check: x is about 0.8 at these SZ masses corrected by b_SZ = -0.38. That matches the X-COP def-A level between b = 0.2 (0.70) and b = 0.3 (0.91) (CFG382 audit).

## Forecast: what a real test needs
- **Statistics:** with 122 clusters (overview tables, z std 0.145), the slope error is 0.19 at 0.3 per-cluster scatter in ln x, or 0.31 at 0.5 scatter. That gives 4.0 / 2.4 sigma on the primary slope of -0.75. CHEX-MATE alone could do it statistically.
- **Systematics (the real wall):** d ln x/d ln M_tot = 1.83, so a drift in ln(1 - b) of only 0.11 between z 0.05 and 0.6 fakes half the slope. CHEX-MATE's own weak-lensing calibration gives (1 + b_SZ) = 0.83 +- 0.09 with redshift evolution in the regression, and 0.72 +- 0.11 without it (as quoted in 2609.09144). That 0.14 spread in ln(1 - b) is already larger than the tolerance.
- So the test needs per-cluster masses whose bias is calibrated as a function of z, from weak lensing or dynamics, not SZ masses with an assumed constant bias. The Planck M_SZ also assumes self-similar evolution, which bears directly on the slope under test.

## Controls
- C1 figure calibration and 4 markers: PASS.
- C2 bin-1/2 mass ordering: PASS.
- C3 T16 reproduction and nu_mono >= 1: PASS.
- **MUTATE** (bin-4 f_gas planted at slow-rate, 0.1257, errors / 10): assignment A gives R_obs 0.864 +- 0.014, power passes, verdict FAVOURS SLOW-RATE. Detected, rc 1. With the plant, the overall indicative headline becomes NOT POSSIBLE, because B does not follow; that is the frozen assignment rule working as declared.

## Caveats
- def-A subtracts the full phantom target, so a physical settling history could map onto x differently than T16's sentence assumes. The test follows T16's registered wording.
- The stacked f_gas values are model-dependent (BFC fits with a fixed, z-independent b_SZ). The bin medians differ in M_SZ (7.83 vs 8.36e14).
- kappa = 1/2 is fitted. Both footings are reported, never pooled. The cold fluid's mass is still required (no dark-matter particle).
- Nothing here says the data favour either branch.
