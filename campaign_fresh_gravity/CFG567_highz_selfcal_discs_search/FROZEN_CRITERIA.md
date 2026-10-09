# CFG567 FROZEN CRITERIA: census of z ~ 1.5-3 discs that could support a self-calibrated a0(z) test (CFG385), and a first score only if >= 5 qualify

Written and committed BEFORE any candidate's data are read in detail. kappa = 1/2 is FITTED. Footings: a0 = 9.3603e-11 and 1.1312e-10 m/s^2. No dark-matter particle; cold mass is required and its amount is free. Not theory closed. Nothing here says data favour the framework over LCDM.

## Why
CFG385: a per-disc free calibration costs nothing IF each disc spans the regimes itself (y = g_bar/a0 from >~3 to <~0.3, i.e. g_obs over ~6.4x) at ~5% velocity precision; 10-20 such discs separate a0 tracking rho_DE (~0.8-0.87 at z 2-2.5) from a0 ~ H(z) (~3-3.7) and from LCDM-with-feedback (CFG565: x2.8 at z 2, x4.9 at z 2.5) at 3 sigma. CFG386/475: none on disk; resolved gas SHAPES are mandatory (assumed exponential shapes made a0 absorb the mismatch, a 3-dex spread; CFG400 INVALID).

## Search scope
2022-2026 literature (plus older papers only if their data are the inner/outer half of a 2022-2026 combination). Primary window z = 1.5-3.0; z = 3.0-4.5 reported in a separate column and NOT counted toward the scoring threshold. Disc candidates already used by CFG228/270/272/273/274/277/278/280/RC100/CFG400-402 may appear in the census (flagged "in record") but are not re-scored with the same inputs.

## Qualification (every rule must hold for the SAME individual disc)
- **Q1 span.** A per-radius rotation curve (individual galaxy, not a stack) whose innermost usable point has g_obs = V^2/R >= 3.5 a0 and whose outermost point has g_obs <= 0.55 a0 (the CFG386 translation of y >= 3 and y <= 0.3), at BOTH footings. Equivalent necessary condition: g_obs spans >= 6.4x. The innermost usable point must lie at R >= the resolution HWHM (PSF/beam; source-plane resolution for lensed systems). Where only a parametric model curve is published, the span is counted between the radii actually sampled by data, not the model's extrapolation.
- **Q2 precision.** >= 5 radial points separated by >= one resolution element, with median fractional velocity error <= 10% (lenient; the CFG386 rule) — <= 5% reported as STRICT.
- **Q3 resolved gas.** A resolved molecular/neutral gas surface-density map or profile (CO, [CI], [CII], or dust continuum) with beam FWHM <= 2 kpc or <= R_e/2 (whichever is larger), with a DECLARED conversion factor, covering the radii of Q1. An assumed exponential/Sersic gas shape, or a gas shape copied from the stellar light, does NOT qualify.
- **Q4 resolved stars.** A resolved stellar-mass map or profile (JWST/NIRCam or HST multi-band pixel SED, or a rest-frame >= 0.5 micron light profile with a declared M/L) of the same disc.
- **Q5 disc.** The authors classify the system as rotation-dominated (V/sigma >= 2 at the outer radii) and publish the dispersion profile or value so pressure support can be corrected.
- **Q6 obtainable.** The Q1-Q4 quantities exist as numbers: a machine-readable table, a VizieR/data-release table, a paper table, or a public data product (cube + published model). Figure digitisation alone does NOT count as obtainable for scoring (it may be recorded as "figure-only").

A candidate meeting Q1-Q5 but not Q6 is QUALIFIED-NOT-OBTAINABLE.

## Verdicts (frozen)
- **ENOUGH TO SCORE:** >= 5 discs in z 1.5-3.0 meet Q1-Q6. Then score with CFG385's self-calibrated estimator (calibration f free per disc, kernel nu_mono primary and exp-RAR reported; pressure correction per Q5), report a0(z)/a0(0) at both footings against: framework (rho_DE-tracking) ~0.85; flat 1; LCDM-with-feedback x2-5 (CFG565); a0 ~ H(z) (~3-3.7). Discrimination per CFG385: 3 sigma between DE-tracking and the H(z) rival needs sigma(log a0) <= 0.22 dex; flat vs rival <= 0.19 dex. A pooled ratio is called CONSISTENT WITH a prediction when within 2 sigma, EXCLUDES it when > 3 sigma away; otherwise NOT DIAGNOSTIC.
- **CENSUS ONLY: FEW (1-4) or NONE (0)** qualify. Deliverable: the exact count, the near-misses (meeting >= 3 of Q1-Q5) and what each lacks, and an observing/fetch specification for the cheapest path to 10 discs.

## Conventions
- Velocities corrected for inclination as published. R in physical kpc as published (cosmology as published; differences < 3% ignored).
- When a paper gives V at radii but not the error, Q2 fails (no error = not usable).
- Figures read by eye to judge Q1 in the census are labelled "by eye, provisional" and are never scored.
- WebFetch/search summaries are provisional; a census entry is only marked PASS on a rule when the number was read from the paper's own table/text/figure axis (stated per entry).

## Controls
- **C1 (rule implementation):** the census script reproduces CFG386's conclusion for its KURVS row type (deep outer points, no inner anchor -> Q1 fail) on a synthetic row.
- **C2 (thresholds):** g_obs thresholds recomputed from y via the nu_mono kernel at y = 3 and y = 0.3 agree with 3.5 a0 / 0.55 a0 to within 10%.
- **MUTATE (census-only case):** relax Q3 (accept assumed/stellar-copied gas shapes). The qualifying count must CHANGE; if it does, the script prints DETECTED and exits 1. If it does not change, that is reported (Q3 is then not the binding rule). (Scoring case: replace observed V by the framework prediction; must recover ~0.85; exit 1 when detected.)

## Outputs
cfg567_census.csv (one row per candidate, every rule PASS/FAIL/UNKNOWN with source), cfg567_census.py, cfg567_census.out, cfg567_census_MUTATE.out, results JSON per mode, README (verdict first), FETCH_LOG.md.
