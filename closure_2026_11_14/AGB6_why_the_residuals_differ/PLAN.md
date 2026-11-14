# AGB6 — why the claim's residuals and the Pantheon+ residuals differ for the same supernovae (PLAN, before the chain is run)

2026-11-14. Owner: "Yes, dig in". **This is a diagnosis, not a blind test.** AGB5 and its post hoc sections are
known: on 185 supernovae the claim's own residuals give an age slope of 0.84 ± 0.21 of the published size, the
Pantheon+ ones 0.26 to 0.40, and the difference between the two trends with host age at 4 to 5σ. What is not
known, and what this plan fixes before it is computed, is **which step between the two standardisations carries
that trend**. It adopts nothing and edits no ledger. No frozen verdict word.

## What was established before this plan (structure only; no age entered)
- The SDSS-II table (Sako et al. 2018) holds, for every supernova, its own SALT2 fit (x0, x1, c) and modulus, and an
  MLCS2k2 fit and modulus. Its SALT2 modulus is −2.5 log₁₀ x0 + 0.183 x1 − 2.91 c + constant (rms 0.010 mag).
- Table 2's residuals are Campbell et al.'s moduli (in the Rose file) minus a Hubble line (correlation 0.9999).
- Table 1's residuals correlate at 0.84–0.88 with the table's SALT2 residuals and 0.76–0.81 with its MLCS2k2 ones;
  table 2's at 0.76 with SALT2 and 0.85 with MLCS2k2. Neither modulus is the claim's residual; both are relatives.

## The chain
Same supernovae throughout: those in Pantheon+ and in one of the claim's tables, with every quantity present.
Every set of residuals is fitted the same way: weighted line in host age (the claim's ages), **8 redshift bins with
free offsets**, weights 1/(σ_HR,claim² + 0.10²), with and without a mass step; A in units of 0.030 mag/Gyr; errors
and the errors of differences by bootstrap over supernovae (400, seed 20261122).

| set | what it is |
|---|---|
| C | the claim's own residual |
| M | the SDSS-II table's MLCS2k2 modulus |
| S | the SDSS-II table's SALT2 modulus as given (coefficients 0.183, 2.91) |
| S′ | the SDSS-II table's SALT2 fit (x0, x1, c) with the stretch and colour coefficients free |
| P′ | the Pantheon+ fit (mB, x1, c) with the coefficients fixed at 0.183, 2.91 |
| P | the Pantheon+ fit with the coefficients free (AGB4's reading) |
| Pb | Pantheon+ as published (m_b_corr: bias corrections and its host correction) |

Steps and what each isolates:
1. **C → S**: whatever the claim's analyses did beyond the survey's own SALT2 modulus (their light-curve fits,
   their coefficients, their corrections).
2. **C → M**: the same against the survey's MLCS2k2 modulus.
3. **S → S′**: the stretch and colour coefficients (fixed against free), same light-curve fit.
4. **S′ → P**: the light-curve fit itself (the survey's SALT2 fit against the Pantheon+ one: model version,
   photometry, calibration), coefficients free in both.
5. **S → P′**: the light-curve fit itself, coefficients fixed in both.
6. **P → Pb**: the Pantheon+ bias corrections and host correction.

## Rule, fixed now
A step **carries slope** if the amplitude changes across it by at least twice the bootstrap error of the paired
difference; otherwise it **does not**. The write-up lists every step with its change and error and says which
carry slope. If no single step does, it says so.

## Reported beside the chain
- Per supernova, Pantheon+ minus the survey's fit, in stretch, in colour and in peak magnitude, each against host
  age (slope per Gyr with its error).
- The chain repeated on each of the claim's tables separately, and with equal weights.
- The five supernovae with the largest |C − P| and the slopes without them.

## Limits stated in advance
The sets are relatives of the claim's residuals, not its exact construction, which is not public. The diagnosis can
say which step holds the trend among these; it cannot say what in the claim's own pipeline produced it. Several
steps and several rows are examined, so a single 2σ change is weak evidence.

kappa = 1/2 FITTED; not theory closed.
