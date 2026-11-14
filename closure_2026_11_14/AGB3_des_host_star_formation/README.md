# AGB3 — the progenitor-age slope against the DES hosts' measured star formation, and the sample's own age drift

2026-11-14. Criteria: `FROZEN_CRITERIA.md` (committed alone, before any script). No amendment. Adopts nothing, edits
no ledger, grades no part of this repository's framework.

## Verdict
**The hosts do show an age-like effect, at about 0.4 of the published size. With that slope and this sample's own
age history the expansion is accelerating today, by a margin just over the frozen line. Both statements lean on the
star-formation rates being mostly right: if half of their age contrast is noise, the published size comes back
inside the errors and the sign today is open again.**

| word | result |
|---|---|
| D2, slope from each host's measured star formation, mass step free | **NEITHER / FRAGILE**. A = +0.39 ± 0.08; Δχ² 24.1 against A = 0 and 59.3 against A = 1. Same word in six forks; with the template halved it reads AGE BIAS REQUIRED AT 3 SIGMA (Δχ² 1.95 against A = 1). |
| U, upper limit: every host effect counted as age | **SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA / FRAGILE**. A ≤ +0.40 ± 0.07; Δχ² 85.9 against A = 1. Fails two forks: template halved (2.47), and mass-only ages (0.72 ± 0.15; 3.64). |
| S2, today, published slope on this sample's own age drift | **SIGN NOT SETTLED / FRAGILE**. q0 = +0.09, Δχ² 1.26. On DES alone: ACCELERATING TODAY (7.18). |
| S3, ever, same | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** (Δχ² 79.9) |
| J2, today, slope from the hosts times drift from the hosts | **ACCELERATING TODAY / FRAGILE**. Joint amplitude 0.38 (0.30 to 0.46), q0 = −0.19, Δχ² 4.46. With the template halved: SIGN NOT SETTLED (0.28). |
| J3, ever, same | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** (Δχ² 113.6) |
| E2, today, young hosts only | **SIGN NOT SETTLED / FRAGILE**. q0 = −0.27, Δχ² 3.44 against a line of 4. Both wider selections read ACCELERATING TODAY (4.97, 9.76). |
| E3, ever, young hosts only | **NEVER-ACCELERATED EXCLUDED AT 3 SIGMA** (Δχ² 59.5) |

A = 1 is the slope of Son et al. (arXiv:2510.13121), 0.030 mag/Gyr. Every known-answer check passes.

## What the host table says before any magnitude is read
The DES team's table gives each host's mass, specific star-formation rate and colour. A two-component model (a
constant star-formation rate at the measured value plus one old burst) turns the rate into a progenitor age.
1. **Mass tracks age at least as strongly as AGB2 assumed.** The age gap between massive and small DES hosts is
   2.9 Gyr from their measured star formation, against 1.4 Gyr in AGB2's mass-only model at these redshifts.
   AGB2's stated worry ran the other way.
2. **Old and young hosts are 2 to 6 Gyr apart**, so the published slope predicts 0.07 to 0.18 mag between them.
3. **The DES hosts' mean age hardly falls with redshift**: 3.4 Gyr at z 0.2, 2.5 Gyr at z 1. The survey needs a host
   redshift, which keeps massive hosts in at high redshift. The cosmic-average curve behind the published correction
   falls from 4.5 to 1.3 Gyr over the same span.

## Part D — the slope from the hosts
Weighted least squares with free offsets in 20 redshift bins, so no cosmology enters. Primary: the 1,623 DES
supernovae, raw magnitudes with free stretch and colour coefficients.

| configuration | D2: A | Δχ²(0) | Δχ²(1) | U: A | Δχ²(1) |
|---|---|---|---|---|---|
| primary | +0.389 ± 0.079 | 24.1 | 59.3 | +0.398 ± 0.065 | 85.9 |
| published magnitudes (D2) / published corrections, mass step undone (U) | +0.383 ± 0.077 | 24.5 | 63.6 | +0.369 ± 0.060 | 109.3 |
| with the 197 legacy supernovae | +0.257 ± 0.055 | 22.0 | 184.9 | +0.299 ± 0.050 | 196.1 |
| 40 bins | +0.392 ± 0.080 | 23.8 | 57.1 | +0.397 ± 0.066 | 83.9 |
| likely core-collapse removed | +0.387 ± 0.080 | 23.6 | 59.2 | +0.405 ± 0.065 | 83.0 |
| burst at z_f = 2 | +0.442 ± 0.096 | 21.2 | 33.8 | +0.456 ± 0.078 | 49.1 |
| burst at z_f = 5 | +0.348 ± 0.069 | 25.8 | 90.2 | +0.356 ± 0.057 | 127.8 |
| template halved (half the contrast is noise) | +0.78 ± 0.16 | 24.1 | 1.95 | +0.80 ± 0.13 | 2.47 |
| mass-only ages in the place of star-formation ages (U only) | | | | +0.719 ± 0.147 | 3.64 |

- **There is a host effect beyond the mass step, in the direction age predicts**, at 4.9σ by the stated error and
  about 4σ by the errors from residuals and from a bootstrap (0.09 to 0.10). It is the same in the published
  magnitudes, so the survey's own corrections do not remove it.
- **Its size is 0.39 of what the published slope predicts** from the hosts' star-formation ages.
- **Why the mass-only fork disagrees:** at DES redshifts the mass-only model gives the two mass groups half the age
  gap that their measured star formation gives (1.4 against 2.9 Gyr), so the same step reads as twice the amplitude.
- **Steps by redshift band (young side minus old side, raw magnitudes, mag), with what the slope predicts:**

| z | mass at 10^10 | predicted | star formation at log s = −10 | predicted | colour at 1.0 | predicted |
|---|---|---|---|---|---|---|
| 0.1–0.3 | +0.034 ± 0.021 | 0.086 | +0.038 ± 0.020 | 0.147 | +0.070 ± 0.020 | 0.116 |
| 0.3–0.5 | +0.040 ± 0.015 | 0.086 | +0.051 ± 0.015 | 0.124 | +0.052 ± 0.014 | 0.101 |
| 0.5–0.7 | +0.038 ± 0.015 | 0.084 | +0.049 ± 0.014 | 0.101 | +0.041 ± 0.014 | 0.089 |
| 0.7–1.2 | +0.005 ± 0.033 | 0.073 | +0.065 ± 0.023 | 0.069 | +0.031 ± 0.023 | 0.056 |

  The steps are real and about half the predicted size below z 0.7; in the highest band the star-formation and
  colour steps reach the prediction within errors.
- **Reported.** AGB2's step-run test on this sample: +0.55 ± 0.79 (DES alone), −0.16 ± 0.44 (with the legacy set);
  DES alone combined with AGB2's Pantheon+ fit without DES: +0.25 ± 0.40 (Δχ² 0.40 at A = 0, 3.60 at A = 1), still
  undecided. Per host with mass-only ages and a free step: +0.68 ± 0.21. Short-delay delay-time distribution:
  D2 +0.388 ± 0.075, U +0.417 ± 0.066.
- Three estimates that differ in sample or in method now sit together: 0.47 ± 0.10 from the size of the Pantheon+
  mass step (AGB2, reported there), 0.39 ± 0.08 (D2) and 0.40 ± 0.07 (U) here.

## Part S — the published slope on this sample's own age drift
T_H(z) is 0.030 mag/Gyr times the fall of the hosts' mean age since the lowest redshift bin. On the whole sample it
rises to 0.096 mag by z 0.3 and stays there (AGB1's template keeps rising, to 0.151 by z 1). Almost all of it is the
difference between the legacy low-redshift hosts and the DES hosts. AGB1's model and fitter, with A_H × T_H.

| fit | Ω_m | w0 | wa | q0 | Δχ² today | word | Δχ² never |
|---|---|---|---|---|---|---|---|
| whole sample, A_H = 0 (published moduli; equals AGB1) | 0.314 | −0.843 | −0.538 | −0.367 | 18.64 | ACCELERATING TODAY | 168.1 |
| **whole sample, A_H = 1 (primary)** | 0.359 | −0.424 | −2.205 | +0.093 | 1.26 | SIGN NOT SETTLED | 79.9 |
| DES alone, its own T_H, A_H = 1 | 0.304 | −0.905 | −0.181 | −0.444 | 7.18 | ACCELERATING TODAY | 87.4 |
| whole sample, T_H from mass-only ages | 0.340 | −0.618 | −1.283 | −0.112 | 1.88 | SIGN NOT SETTLED | 91.0 |
| whole sample, z_f = 2 / z_f = 5 | 0.358 / 0.360 | | | +0.077 / +0.107 | 0.88 / 1.67 | SIGN NOT SETTLED | 75.4 / 83.2 |
| whole sample, host by host (reported) | 0.351 | −0.519 | −1.685 | −0.005 | 0.00 | SIGN NOT SETTLED | 75.7 |

- Granting the published slope in full, the sign today is not settled on the whole sample and is accelerating on
  DES alone. The difference is the legacy set: its hosts are listed as much older than the DES hosts, which puts a
  0.1 mag step between the two. The legacy hosts' star-formation rates were flagged as different before the freeze.
- The distances themselves do not want that step: A_H free is +0.14, with Δχ² 0.14 at A_H = 0 and 5.79 at A_H = 1.

## Part J — slope from the hosts times drift from the hosts
D2's amplitude as a prior on A_H.

| case | joint A_H (68 %) | q0 | Δχ² today | word | Δχ² never |
|---|---|---|---|---|---|
| **primary** (whole sample, D2 0.389 ± 0.079) | 0.38 (0.30–0.46) | −0.19 | 4.46 | ACCELERATING TODAY | 113.6 |
| DES alone | 0.40 (0.32–0.48) | −0.52 | 9.64 | ACCELERATING TODAY | 93.9 |
| D2 from the published magnitudes | 0.37 (0.30–0.45) | −0.20 | 4.60 | ACCELERATING TODAY | 114.5 |
| drift from mass-only ages | 0.40 (0.32–0.48) | −0.27 | 9.54 | ACCELERATING TODAY | 124.2 |
| U's amplitude as the prior | 0.39 (0.33–0.45) | −0.19 | 4.41 | ACCELERATING TODAY | 115.8 |
| template halved (prior 0.78 ± 0.16) | 0.67 (0.53–0.82) | −0.06 | 0.28 | SIGN NOT SETTLED | 84.1 |

## Part E — young hosts only
Supernovae in hosts with log s ≥ −9.5 (progenitors under 1.7 Gyr at every redshift in the model), published moduli,
no age term.

| subsample | n | Ω_m | w0 | wa | q0 | Δχ² today | word | Δχ² never |
|---|---|---|---|---|---|---|---|---|
| **young** | 609 | 0.323 | −0.762 | −0.764 | −0.273 | 3.44 | SIGN NOT SETTLED | 59.5 |
| blue (colour ≤ 0.8) | 733 | 0.321 | −0.772 | −0.723 | −0.286 | 4.97 | ACCELERATING TODAY | 69.8 |
| log s ≥ −10 | 1,145 | 0.319 | −0.804 | −0.741 | −0.322 | 9.76 | ACCELERATING TODAY | 118.1 |
| old (the rest; reported) | 1,211 | 0.315 | −0.838 | −0.575 | −0.362 | 16.17 | ACCELERATING TODAY | 136.5 |
| young, DES alone (reported) | 586 | 0.313 | −0.843 | −0.450 | −0.369 | 2.46 | SIGN NOT SETTLED | 49.9 |

- **Young-host and old-host supernovae give the same expansion history.** If age drove the result, the young ones,
  which do not get younger with redshift, would show the non-accelerating history. Their best fit is accelerating
  (q0 = −0.27); with 609 supernovae it falls 0.56 short of the frozen line, and the two wider selections clear it.
- Reported: both subsamples want the same amount of AGB1's redshift template (A = 0.80 young, 0.83 old). An age
  drift would be wanted by the old hosts and not by the young ones.

## Known-answer checks
| check | result | |
|---|---|---|
| KM two-component model | passive host 10.67 Gyr against burst age 10.68; constant case 1.9023 both ways; within 1.19 Gyr of the mass-only model on its own galaxies | PASS |
| K1 the table | equal to the distance file for all 1,820; column identity gives the published step, 0.0334 ± 0.0007 | PASS |
| K2 the estimator | mass step from the published standardisation: +0.0326 ± 0.0079 (published 0.033 ± 0.008). Raw: +0.035 ± 0.009; as published: −0.001 ± 0.008 | PASS |
| K3 twins | 12 of 12 recover the injected amplitude to 10⁻⁹ | PASS |
| K4 error bar | shuffle scatter / stated error 1.22, 1.10, 1.06; error from residuals / stated 1.19, 1.16, 1.12 (D1, D2, U; allowed 0.8–1.25) | PASS |
| KS cosmology harness | returns AGB1's A = 0 and A = 1 forks to 0.001, both samples | PASS |

K4 passes with the stated errors about 10 to 20 % small. No word above changes if the larger error is used
(D2 with 0.098: Δχ² 15.8 and 38.9).

## Independent checks (scratch, not part of the frozen files)
- Two-component ages by direct quadrature with separate code: equal to four decimals at seven test points.
- D2 and U with a separate loader and route: equal to four decimals. Bootstrap errors 0.098 (D2) and 0.073 (U).
- T_H rebuilt from scratch: identical. A global optimiser on the A_H = 1 fits finds the same minima (Δχ² today 1.258
  both; never 79.5 against 79.9, the optimiser's point sitting 0.0004 inside the forbidden side).

## Limits
- **The star-formation rates are fits to broad-band host photometry on a grid of templates.** Their noise mixes old
  and young hosts and shrinks any age signal. Halving the template is the frozen stress test, and three words fail
  it. Nothing in this table can say how much of the contrast is noise; measured host ages or spectra could.
- The two-component model is one burst plus a constant rate, not a fit to each galaxy. Moving the burst from z 2
  to z 5 moves D2 from 0.44 to 0.35.
- D2 and U measure a host effect and its size. They do not say age causes it; dust in star-forming hosts is the
  usual alternative and would look the same here.
- U is an upper limit only if nothing else makes supernovae in old hosts fainter.
- Part S and Part J on the whole sample rest on the legacy hosts' listed star-formation rates, which behave
  differently from the DES ones. DES alone gives ACCELERATING TODAY in both parts.
- J2's margin is thin (4.46 and 4.41 against 4).
- Part E selects by host; the survey's bias corrections were made for the whole sample.
- Cosmology words live inside the flat w0–wa family. AGB1's and AGB2's words stand as written.
- No blind re-grade has been run.

## Data fetched
`DES-Dovekie_Metadata.csv`, 1,269,831 bytes, sha256
45ad71f8470eaecfe2b386699ef66b26b0717c50f445d5f32941988d32c75388, from `github.com/des-science/DES-SN5YR` (branch
`main`, folder `4_DISTANCES_COVMAT`), 2026-11-14, with the owner's yes. Stored outside the repository in
`_external_data/agb3_des_dovekie_metadata/`.

## Files
`FROZEN_CRITERIA.md`; `agb3_twocomp.py` (two-component ages), `agb3_run.py` (checks and Part D), `agb3_cosmo.py`
(Parts S, J, E), `agb3_collect.py`; outputs `agb3_{KM,K1,K2,K3,K4,D,S,E,J}.{json,out}`, `agb3_results.json`,
`agb3_collect.out`.

Commits (local / origin): criteria 5403d1b288 / 6b0231f3a1; scripts 8e1fd5b361 / 01b873cb60; result 9c06d486f3 /
64a7b86222.

kappa = 1/2 FITTED; not theory closed.
