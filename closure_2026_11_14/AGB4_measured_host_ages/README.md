# AGB4 — the progenitor-age slope on published host ages (SDSS-II hosts, Pantheon+ magnitudes)

2026-11-14. Criteria: `FROZEN_CRITERIA.md` (committed alone, before any script). No amendment. Adopts nothing, edits
no ledger, grades no part of this repository's framework.

## Verdict
**On the kind of host age the published slope was measured on, with no age model, the published slope does not
hold in the Pantheon+ magnitudes. Once a host-mass step is allowed, nothing significant is left.**

| word | result |
|---|---|
| M1, slope with a mass step free | **AGE BIAS EXCLUDED AT 3 SIGMA / ROBUST**. A = +0.19 ± 0.21; Δχ² 0.86 against A = 0, 14.8 against A = 1. Same word in all four forks. |
| M0, slope with no mass step (how the published slope was measured) | **SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA / FRAGILE**. A = +0.30 ± 0.19; Δχ² 13.1 against A = 1. The larger SDSS-II sample reads HOSTS AS LARGE AS THE SLOPE NEEDS (0.70 ± 0.17). |

A = 1 is 0.030 mag/Gyr (Son et al., arXiv:2510.13121). The ages are the FSPS fits to SDSS host photometry (after
Gupta et al. 2011) released with the SDSS-II supernova table of Sako et al. (2018), for the 286 Pantheon+ SDSS
supernovae that have one.

In plain words:
- **The fork that disagrees is the one that explains the published slope.** On the 1,092 SDSS-II supernovae with the
  survey's own light-curve fits and no mass step, the slope is 0.70 ± 0.17 of the published one (0.23 by the error
  from residuals): most of the published slope is there when measured that way. Let a mass step in, and it falls to
  0.27 ± 0.20 while the step comes out at 0.098 ± 0.022 mag. **The slope without a mass step is mostly the mass
  step.** That is the reading of Wiseman et al. (arXiv:2601.13785), reproduced here from public tables.
- **In the Pantheon+ magnitudes the slope is small either way:** 0.30 ± 0.19 with no step, 0.19 ± 0.21 with one,
  0.04 ± 0.17 and 0.11 ± 0.19 in the published (already mass-corrected) magnitudes.
- **These ages do sort progenitors.** The share of low-stretch supernovae is 0.03, 0.06, 0.35, 0.50 for host ages
  under 4, 4–6, 6–8, over 8 Gyr. So the small slope is not a matter of ages that carry no information.
- **It agrees with AGB3.** Slope beyond a mass step: 0.39 ± 0.08 from DES star-formation ages, 0.19 ± 0.21 and
  0.27 ± 0.20 here. All far below 1.

## The fits
Weighted least squares inside redshift bins, template −0.030 mag/Gyr × host age; raw magnitudes with free stretch
and colour coefficients unless stated.

| configuration | M0: A (no step) | Δχ²(0) | Δχ²(1) | M1: A (step free) | Δχ²(0) | Δχ²(1) | step g (mag) |
|---|---|---|---|---|---|---|---|
| primary: Pantheon+ SDSS, 286, 8 bins | +0.297 ± 0.194 | 2.34 | 13.09 | +0.194 ± 0.210 | 0.86 | 14.76 | +0.027 ± 0.021 |
| published magnitudes | +0.043 ± 0.168 | 0.07 | 32.41 | +0.106 ± 0.189 | 0.31 | 22.45 | −0.015 ± 0.021 |
| 12 bins | +0.307 ± 0.195 | 2.49 | 12.62 | +0.188 ± 0.211 | 0.79 | 14.79 | +0.031 ± 0.021 |
| ages with a stated interval within ± 2.5 Gyr (278) | +0.344 ± 0.200 | 2.97 | 10.80 | +0.225 ± 0.214 | 1.10 | 13.11 | +0.032 ± 0.021 |
| larger SDSS-II sample, its own light-curve fits (1,092) | +0.704 ± 0.174 | 16.29 | 2.88 | +0.269 ± 0.199 | 1.83 | 13.43 | +0.098 ± 0.022 |

**Reported only.**
- Larger sample, spectroscopic supernovae only (387): M0 +0.64 ± 0.26 (0.41 from residuals), M1 +0.25 ± 0.29, step
  +0.091 ± 0.030.
- PEGASE ages from the same table: +0.11 ± 0.10 and +0.09 ± 0.10. These ages barely follow stretch (correlation
  −0.11), so they say little.
- Split at 6 Gyr, primary sample: below +0.56 ± 0.33 (M0) and +0.42 ± 0.33 (M1); above −0.18 ± 0.49 in both (86
  hosts). In the larger sample the split is noisy and goes the other way with the step free (below −0.15 ± 0.27,
  above +0.98 ± 0.47), so the shape is not settled here.
- Reliability of the FSPS age, with stretch and host mass as witnesses (AGB3's post hoc method): 0.77 ± 0.10; inside
  the fits 0.70 (M0) and 0.65 (M1). Amplitudes divided by it: +0.43 and +0.30. The published slope was measured on
  ages of this kind, noise included, so the uncorrected rows are the like-for-like comparison.
- Rose et al. (2019) ages, 66 supernovae: **NOT EVALUABLE** (check KR failed, below). As a reading: global age
  +0.35 ± 0.24 (M0), +0.20 ± 0.27 (M1); local age +0.57 ± 0.25, +0.46 ± 0.28.

## Known-answer checks
| check | result | |
|---|---|---|
| K1 the match | all 321 Pantheon+ SDSS rows found by id; 286 with an age; largest redshift difference 0.021; mass correlation 0.849 | PASS |
| K2 ages against stretch | low-stretch share 0.372 at 6 Gyr and above, 0.045 below | PASS |
| K3 twins | 8 of 8 recover the injected amplitude to 10⁻⁹ | PASS |
| K4 error bar | shuffle scatter / stated error 0.88 (M0), 0.97 (M1); error from residuals / stated 1.09, 1.04 | PASS |
| KR Rose et al.'s age step | +0.207 mag from their distance moduli and local ages, against their published 0.114 ± 0.039 (tolerance 0.04) | **FAIL** |

KR does not void the lane (frozen so); it makes the Rose rows NOT EVALUABLE. My simple split of their moduli at
8 Gyr does not reproduce their number, so I have not understood how their step was computed, and those rows stay
a reading.

## Independent checks (scratch, not part of the frozen files)
The two primary amplitudes redone with a separate loader and route: equal to four decimals. Bootstrap errors over
supernovae: 0.217 (M0) and 0.218 (M1); with them Δχ² against A = 1 is 10.5 and 13.7, the same words.

## Limits
- 286 supernovae at z < 0.4 from one survey. M0's margin is 3.6σ by the stated error and 3.2σ by the bootstrap.
- The exact table behind the published slope (Chung et al. 2025, supplementary file) could not be fetched: the
  publisher's site refused the automated request and that was not worked around. This lane uses the same family of
  ages (the Gupta-method FSPS fits) on the Pantheon+ standardisation of the spectroscopic SDSS sample, not the
  published Hubble residuals. A like-for-like re-run on their own table is still owed.
- The ages are fits to five-band photometry, about ± 1.7 Gyr each.
- A slope that vanishes when a mass step is allowed does not say which of mass or age is the cause; it says the
  data cannot tell a 0.030 mag/Gyr age law from a step in mass, and that beyond the step little is left.
- Words are read as one degree of freedom. AGB1's, AGB2's and AGB3's words stand as written.
- No blind re-grade has been run.

## Data fetched (2026-11-14, with the owner's yes; stored outside the repository)
- `sdsssn_master.dat2`, 9,420,067 bytes, sha256 fcf3c561e9a0655c5c5d8582dee680c403b237dcdf7618eee9a178fcae2803ae,
  `data.sdss.org/sas/dr10/boss/papers/supernova/` → `_external_data/agb4_sako2018_master/`.
- `results-summary.csv` (3,444 bytes), `campbell_local.tsv` (34,305), `campbell_global.tsv` (15,755),
  `gupta_global.tsv` (11,693), `github.com/benjaminrose/MC-Age` (branch master) → `_external_data/agb4_rose2019_ages/`.
- Not fetched: `staf497_supplemental_file.zip` (MNRAS 538, 3340, DOI 10.1093/mnras/staf497); HTTP 403.

## Files
`FROZEN_CRITERIA.md`; `agb4_data.py`, `agb4_run.py`, `agb4_collect.py`; outputs `agb4_{K1,K2,K3,K4,KR,M}.{json,out}`,
`agb4_results.json`, `agb4_collect.out`.

kappa = 1/2 FITTED; not theory closed.
