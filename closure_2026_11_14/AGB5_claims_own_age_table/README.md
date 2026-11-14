# AGB5 — the published age slope on the claim's own table, with a host-mass step allowed

2026-11-14. Criteria: `FROZEN_CRITERIA.md` (committed alone, before any script). One amendment, `AMENDMENT_1.md`,
**written after the numbers were seen** (it changes the error bar only, and says so). Adopts nothing, edits no
ledger, grades no part of this repository's framework.

## Verdict
**On the claim's own ages and its own residuals, the slope survives a host-mass step: 0.79 ± 0.19 of the published
size. The same supernovae standardised as in Pantheon+ give 0.15 to 0.40. The slope is in the older residuals and
largely absent from the modern ones.**

| word | result |
|---|---|
| L1, plain line with a mass step free, as frozen | **NOT EVALUABLE**: the frozen error-bar check failed on one table. The reading: A = +0.82 ± 0.17. |
| L1, amendment 1 (errors from a bootstrap over hosts) | **AGE BIAS REQUIRED AT 3 SIGMA / FRAGILE**. A = +0.79 ± 0.19; Δχ² 17.5 against A = 0, 1.2 against A = 1. Fragile forks: table 1 alone reads AGE BIAS FAVOURED (+0.53 ± 0.25); the fit with errors in both variables reads UNDECIDED (+1.65 ± 1.44). |

A = 1 is 0.030 mag/Gyr, the slope Son et al. (arXiv:2510.13121) take from Chung et al. (2025, MNRAS 538, 3340).
The tables are that paper's supplementary file, downloaded by the owner from the journal.

**This corrects a sentence in AGB4's README.** AGB4 found that on a larger SDSS-II sample the slope with no mass
step "is mostly the mass step". That holds for that sample and those light-curve fits. It does not hold on the
claim's own residuals: there the slope falls only from 1.04 ± 0.16 to 0.79 ± 0.19 when the step is allowed.

## What reproduces, and what the mass step does
| fit | table 1 (Gupta sample, 199) | table 2 (Rose sample, 102) | combined, in units of 0.030 |
|---|---|---|---|
| published, hierarchical | −0.025 ± 0.006 | −0.038 ± 0.007 | 1 (−0.030 ± 0.004) |
| plain line, no step (check KA) | −0.0246 ± 0.0051 | −0.0385 ± 0.0061 | 1.01 ± 0.13 (1.04 ± 0.16 with bootstrap errors) |
| published, errors in both variables | −0.047 ± 0.015 | −0.062 ± 0.014 | |
| structural fit, no step (check KA) | −0.0482 ± 0.0154 | −0.0626 ± 0.0136 | |
| **plain line, mass step free** | −0.0160 ± 0.0074 | −0.0354 ± 0.0090 | **0.79 ± 0.19** |
| the step beside it (mag) | +0.059 ± 0.029 | +0.041 ± 0.036 | |
| step alone, no age term (mag) | +0.099 ± 0.023 | +0.140 ± 0.029 | |
| slope inside low-mass hosts | +0.006 ± 0.015 (59) | −0.037 ± 0.019 (24) | |
| slope inside the other hosts | −0.022 ± 0.008 (128) | −0.035 ± 0.008 (77) | |

- The published numbers come back to the third decimal, so the tables and both estimators are understood.
- These residuals carry a large mass step when no age term is fitted (0.10 and 0.14 mag). With both terms the age
  slope keeps most of its size and the step halves. Inside the massive hosts alone the slope is still there.

**Forks of L1 (amended errors).**
| fork | A | Δχ²(0) | Δχ²(1) | reads |
|---|---|---|---|---|
| primary | +0.793 ± 0.190 | 17.49 | 1.20 | REQUIRED AT 3 SIGMA |
| table 1 alone | +0.532 ± 0.245 | 4.71 | 3.64 | FAVOURED |
| table 2 alone | +1.180 ± 0.299 | 15.59 | 0.36 | REQUIRED AT 3 SIGMA |
| the 33 shared hosts dropped from table 1 | +0.773 ± 0.217 | 12.71 | 1.10 | REQUIRED AT 3 SIGMA |
| table 1 with its original residuals | +0.634 ± 0.189 | 11.27 | 3.76 | REQUIRED AT 3 SIGMA |
| a redshift term added | +0.719 ± 0.200 | 12.91 | 1.97 | REQUIRED AT 3 SIGMA |
| errors in both variables (structural) | +1.648 ± 1.435 | 1.32 | 0.20 | UNDECIDED |

The structural fork is unstable under resampling: the stated age errors (mean square 4.4 and 4.8 Gyr²) are larger
than the whole variance of the ages (4.0 and 4.3 Gyr²), so that fit has almost nothing to hold on to once a step
is allowed. With stretch and host mass as witnesses the ages are in fact reliable (0.85 ± 0.14 and 1.0 ± 0.35), so
the stated errors are not random errors, and the published errors-in-both-variables slopes (−0.047, −0.062) are
inflated by them.

## Post hoc (after the numbers above were seen; no frozen word)
**1. Same supernovae, two standardisations** (`agb5_posthoc_same_hosts.py`). 185 supernovae are in one of the
claim's tables and in Pantheon+.

| on those 185 | no mass step | mass step free |
|---|---|---|
| (a) the claim's own residuals against age | +0.84 ± 0.21 | +0.67 ± 0.25 |
| (b) Pantheon+ residuals against age (two-step fit) | +0.26 ± 0.17 | +0.15 ± 0.17 |
| (b′) Pantheon+ magnitudes, age fitted jointly with stretch and colour (the frozen reported row) | +0.40 ± 0.19 | +0.27 ± 0.22 |
| (c) difference of the two residuals against age | +0.48 ± 0.11 | +0.56 ± 0.12 |

The two sets of residuals correlate at 0.86 and differ by 0.09 mag rms, and **that difference trends with host age
at 4 to 5σ**. About half of the published slope is in how the older analyses standardised these supernovae.

**2. Is it a leftover stretch or colour term?** (`agb5_posthoc_stretch.py`) No. With a linear stretch and colour
term allowed beside age on the claim's own residuals, the slope is +0.95 ± 0.19 (no step) and +0.70 ± 0.22 (step
free). So what separates the two standardisations is not a linear term in the survey's stretch and colour; it is
not identified here.

## Known-answer checks
| check | result | |
|---|---|---|
| KA published slopes | six of six within 0.002 mag/Gyr; combined −0.0304 ± 0.0039 against −0.030 ± 0.004 | PASS |
| K1 tables | 199 and 102 rows, 33 shared, every id found in the SDSS-II table | PASS |
| K3 twins | 4 of 4 | PASS |
| K4 as frozen | shuffle scatter / stated error 1.25 (table 1), **1.43 (table 2; allowed 1.25)**; bootstrap / stated 1.09, 1.16 | **FAIL** |
| K4 amended | bootstrap / stated 1.09, 1.24; shuffle with the fitted signal removed 1.20, 1.12 | PASS |

**Why K4 failed.** The plain fit assumes 0.10 mag of intrinsic scatter, the value that reproduces the published
slopes; the fits then have χ²/dof 1.35 and 1.42, so every stated error is about 10 to 25 % small. The shuffle test
also keeps the fitted signal in the residuals, which a strong signal inflates. The amendment takes errors from the
bootstrap; it was written after all amplitudes had been printed and it moves none of them.

## Limits
- 268 hosts at z < 0.4. Table 1 by itself is weaker (0.53 ± 0.25) than table 2 (1.18 ± 0.30).
- Age and mass are tied together (correlation −0.6). A slope that survives a step is not proof that age is the
  cause; star-formation state or dust inside massive hosts would look the same.
- The difference between the older residuals and the Pantheon+ ones is measured, not explained.
- The paper's method details are a web reading; the known-answer checks show its numbers reproduce.
- What matters for a correction to modern distances is the slope present in those distances: 0.15 to 0.40 here on
  Pantheon+, 0.39 ± 0.08 on DES (AGB3), 0.19 to 0.30 on Pantheon+ with the SDSS table's ages (AGB4).
- One plumbing fix after the amended scripts commit: the structural fit's error matrix falls back to a
  pseudo-inverse when a bootstrap resample makes it singular (the first bootstrap run stopped on that before
  writing any output), and its bootstrap uses 400 draws like the others. No rule changed.
- No blind re-grade has been run.

## Data
`staf497_supplemental_file.zip`, 5,118 bytes, sha256
c98883adf60efa3ead151d297e1fb1bd2067dddf997e8cf3bc6fe98044c40f04, downloaded by the owner from the journal page
(DOI 10.1093/mnras/staf497) on 2026-11-14; stored outside the repository in `_external_data/agb5_chung2025_ages/`.

## Files
`FROZEN_CRITERIA.md`, `AMENDMENT_1.md`; `agb5_data.py`, `agb5_eiv.py`, `agb5_run.py`, `agb5_collect.py`. As frozen:
`agb5_{K1,KA,K3,K4,L}.{json,out}`, `agb5_results.json`, `agb5_collect.out`. Amended: `agb5_{K4,L}_boot.{json,out}`,
`agb5_results_boot.json`, `agb5_collect_boot.out`. Post hoc: `agb5_posthoc_{same_hosts,stretch}.{py,json,out}`.

kappa = 1/2 FITTED; not theory closed.
