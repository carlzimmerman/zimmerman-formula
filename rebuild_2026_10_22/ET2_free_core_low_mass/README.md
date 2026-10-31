# ET2_free_core_low_mass: the low-mass rise survives without M200; the fit checks need the caveats below

Criteria: `FROZEN_CRITERIA.md` (e936b7bbe8, committed alone). Numbers: `et2.out`, `et2_results.json`. Post-result diagnostics: `et2_post.py`, `et2_post.out`. κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

## Frozen result, Υ 0.50, free S and r₀
| V_flat | n | S, M☉/pc² [95 %] | ET1 with M200 |
|---|---|---|---|
| 20–60 | 12 | 70.2 [52.8, 77.3] | 68.6 |
| 60–100 | 35 | 107.7 [89.0, 136.6] | 102.7 |
| 100–150 | 23 | 157.5 [136.6, 190.5] | 143.2 |

- **Rise: RISE SURVIVES**, ρ +0.556, p < 5e-5; same at Υ 0.40 and 0.60.
- **Floor: MIXED on both footings** at Υ 0.50: 20–60 below, 60–100 inside, 100–150 above. Not rejected by the frozen rule, which needs two bins on one side. At Υ 0.60, alt is below, inside, inside.
- **M200-INDEPENDENT** by interval overlap, a weak test.
- ET1's M200 × 0.5 stress admitted canonical's 107 at 20–60 ([60.9, 118.3]). The free fit does not ([52.8, 77.3]), and 20–60 barely moves with Υ (70.2, 70.2, 66.9).

## Two frozen items did not work
- **K2 FAILED**, script exit 1. Planted (50, 1) and (200, 3) returned S ratios 1.056 and 1.050 against the limit 1.0487; (800, 10) passed. Post-result: those plants sat between grid points, and on-grid plants return exactly. K1 is the identity of one formula, so it tests little.
- **The guard is empty: 0 of 123 CONSTRAINED.** Δ = 1/N_eff (median 0.056 dex²) is far above the median best mse (0.0009 dex²), because the mse is not in error units. This was a design error in the criteria, so GUARD-DEPENDENT could not be tested.

## Post-result only, not verdicts
- A relative guard, mse ≤ 1.25 × minimum with S span under 0.5 dex, passes 116 of 123. Below 150 km/s it gives 70.2, 107.7, 165.4 and ρ +0.545.
- Flat truth S = 100 plus each galaxy's real residuals shuffled over its points, 8 seeds: medians 98–103, ρ −0.04 to +0.18, none significant. Scatter and degeneracy do not fake this rise. Shuffling destroys radially correlated errors, so this says nothing about systematics that vary smoothly with radius.
- The noiseless frozen MUTATE also reads RISE GONE, exit 0.

## Limits
One Υ for all; chosen core shape; distance, inclination, beam smearing and pressure-support errors not modelled here, and those matter most in the smallest galaxies. 20–60 has 12 galaxies. Intervals cover sample scatter only. No parameter is derived, and no curve enters another lane.
