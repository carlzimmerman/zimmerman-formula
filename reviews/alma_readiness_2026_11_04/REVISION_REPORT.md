# PAPER66 v1.4 repair and verification, 4 November 2026

The local manuscript and PDF are revised to v1.4. No Zenodo deposit or release-data access occurred. All 35 protected historical files, including AC1 predictions, the four seals, frozen criteria, G1 addendum, historical mock outputs and numerical table inputs, retain their original full SHA-256 hashes. The old source/PDF/scorer are preserved in revision_v1_4/.

## Disposition of review findings

- AR-1 repaired: all three starts must agree within 15% on both pressure branches at the scored radius. No chi-square-based removal is allowed. Individual starts and their chi-square values are saved.
- AR-2 repaired: B0's scorecard preserves the sister-noise/beam condition and separately reports detection and fit validity.
- AR-3 repaired: B2 is a conditional inverse-mass diagnostic; the unsupported >600 km/s countercriterion is removed. The frozen physical values do not change.
- AR-4 reconciled by explicit dated operational amendment G2: retain the archived 0.088731 fractional RMS floor, report its source/hash and calculation, and remove the claim of S/N-matched calibration. Fresh validation exposes limitations rather than claiming statistically calibrated confidence. This is a documented error prescription, not a solved universal coverage problem.
- Additional clarity: B1 is a grid minimum; R31 is explicitly defined; the inherited 0.5-kpc minimum and any resulting extrapolation are disclosed. Historical forecasts and corrected validation are distinct. Reproducibility now includes full preservation hashes and source-to-PDF binding.

## Verification

| Check | Result |
|---|---|
| Paper audit | 64/64 pass |
| Number mutation | 52/52 perturbed checks fail as intended |
| Revision/build/preservation verification | 15/15 pass |
| Scorer regression tests | 6/6 pass |
| Five-class end-to-end selftest | 10/10 checks pass, including velocity-axis mutation |
| Power validation | 36 cases completed, six seeds per class at each of two noise/beam settings |
| Publication dry check | passes; no token read or Zenodo contact |
| PDF | seven pages rendered and visually inspected; no clipping/overlap or unresolved references |

At archive noise, smooth primary fits score 0/6; compact primary fits fall from historical 4/6 to corrected 3/6. In the rejected compact seed 0, a high-chi-square start gives a P0 speed near 1 km/s versus about 411 for the other two starts; the old subset gate discarded it. Sister-like primary smooth and compact fits remain 6/6. Both suites have zero noise-only detections. The selftest uses a separate seed and is not pooled into those six-seed counts.

## What the uncertainty tests actually show

Metrics compare the recovered speed with the generating curve at each scored radius, separately for pressure and inclination. For the primary Tadaki P-B branch, sister-like RMS is 2.6% (smooth) and 2.2% (compact), with truth within the reported error in 6/6 accepted fits in each group. Archive compact primary fits have 9.0% RMS and only 1/3 covered. Moment-0 inclination can remain biased: archive compact P-B RMS 30.2% (1/2 covered); sister-like compact 13.7% (4/6 covered). The paper now states these numbers and treats consistent/in-tension labels as operational diagnostics, not confidence-calibrated rejection statements. The floor was not enlarged after inspecting outcomes merely to cover the validation sample.

## Provenance and remaining limits

Exact commands, software versions and source hashes are in revision_v1_4/run_sources.json. Detailed recovery metrics and artifact hashes are in validation_summary.json. New mock files were generated temporarily and deleted by the existing harness. Python scientific dependencies and the Tectonic compiler were staged under /tmp; the initial missing-Astropy launch was resolved before successful runs. The historical power record does not retain its exact sister-beam CLI: this suite records its chosen beam factors and is described as sister-like, not an exact historical reproduction. Archive default beam values are also the present generator's rounded values (.0699705 by .0620208 arcsec), versus .070 by .062 in the historical selftest.

The separate code reviewer found no blocking defect; its radius-minimum comment was incorporated and it confirmed the generating-curve summary calculations. Source proofreading covered changed material and reference consistency. All seven final pages were inspected. Two normal h-to-ht float placement warnings remain; no overfull boxes or undefined references were found.

The revised paper is ready as a transparent pre-data working note. It is not a demonstration of universal error coverage or a discriminating one-galaxy test of the acceleration law. No independent rederivation of all astrophysical inputs or new real-cube replication is claimed. The v1.4 metadata is prepared separately; the published v1.3 record remains unchanged.
