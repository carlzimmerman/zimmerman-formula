# CFG700 — early-type age signal on RAW lensing only

(owner chat; criteria cc3a6a7cf, committed alone first.) Re-test of CFG585–589's core claim under the owner's 10-10
raw-data rule: no law, no environment model, no ΛCDM or standard-MOND ingredient. Only the raw KiDS excess surface
density of two groups of f30 early types at identical stellar mass (CFG589's stratified tertiles).

| | N | median u−r | median log M* | median z |
|---|---|---|---|---|
| OLD | 8860 | 2.406 | 10.800 | 0.341 |
| YOUNG | 8854 | 2.131 | 10.800 | 0.349 |

A = log10(OLD/YOUNG raw ESD), common inverse-variance weights; empirical σ from 200 within-mass-bin relabellings:

| band | A | ratio | Z (empirical) | Z (jackknife) |
|---|---|---|---|---|
| **K9 (primary)** | **+0.166** | **×1.46** | **+2.33** (0/200 nulls ≥ A) | +2.04 |
| K-in | +0.217 | ×1.65 | +1.57 | +1.66 |
| K-mid | +0.232 | ×1.70 | +2.42 | +2.06 |
| K-out | +0.107 | ×1.28 | +0.86 | +0.89 |

**VERDICT: AGE SIGNAL ON RAW DATA** (K9, A > 0, Z ≥ 2). Controls 4/4 (mass match 0.0001 dex, lens-z 0.008, exact
closure, unbiased null); MUTATE 4/4 (exact log10 0.8 linearity).

What this does and does not say:
- The old-vs-young difference is in the raw lensing itself, not produced by the ΛCDM-built environment term used in
  CFG585–589. At the same stellar mass, older early types carry ~1.5× the lensing signal. A law that reads only the
  present baryons predicts ×1.00.
- Here the jackknife did NOT understate (empirical/jackknife σ 0.85–1.06), unlike CFG589's ε statistic.
- Significance is modest (Z 2.3; one band set). Per-bin ratios scatter strongly (0.8–2.6), so the radial shape (ACE P2)
  is not measured: K-out alone is not significant.
- Measurement nuisance not excluded: if LePhare stellar masses of the reddest galaxies are biased low, the OLD group is
  truly heavier and the difference is a baryon mismatch, not extra cold energy. That is a survey calibration question,
  to be checked against an independent mass estimator before any physical reading.
- No law, κ or footing entered. Cold energy's mass still required; not theory closed.
