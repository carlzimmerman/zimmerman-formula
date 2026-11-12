# EUC5 AMENDMENT A1 (a second data source; frozen before any fit)

2026-11-12. Written after EUC5's frozen run (c30faba3b4) returned NOT EVALUABLE for lack of sample: 7 lenses of sample P
have an SDSS dispersion against the 30 required. Committed alone, before any A1 script exists and before any velocity
dispersion has been fitted to any DESI spectrum. The frozen criteria are not edited and the frozen word stands.

## Why

EUC2 already retrieved 382 public DESI DR1 spectra of 369 Euclid lens galaxies; 39 of those lenses are in sample P. They
carry no pipeline dispersion. A fitting package (pPXF 9.5.2) and a stellar-population library (E-MILES, BaSTI) are
already on this machine. Nothing is downloaded or installed.

**Seen before this amendment (disclosed).** EUC5's SDSS readings (16 lenses: `b_dyn` median +0.05 / +0.04, 9 of 16 below
their lensing bound). EUC2's use of the same DESI spectra: an emission-line search on the residuals after the pipeline
model was subtracted; no stellar kinematics were measured or looked at. No DESI dispersion exists yet.

## A1.1 Spectra

Every DESI spectrum that EUC2 treats as a deflector spectrum (`euc2_matches.csv`: flagged lenses, and extension lenses
whose DESI redshift falls in the photo-z interval) for a lens of sample S, as on disk when A1 runs (EUC2's extension
search is still in flight; the count is reported). One spectrum per lens: the primary one, else the one with the
smaller fitted error.

## A1.2 The fit

- pPXF, two moments (V, σ). Templates: E-MILES BaSTI, bimodal IMF slope 1.30, 14 ages (1–14 Gyr) × 6 metallicities = 84.
- The spectrum is de-redshifted with the deflector redshift, cut to rest 3750–5600 Å inside observed 3650–9700 Å,
  and log-rebinned. Additive Legendre polynomial of degree 8, no multiplicative polynomial. Noise 1/√ivar.
- Masked: pixels with ivar ≤ 0 or a mask bit; ±10 Å (rest) around [O II] 3727/3730, [Ne III] 3870, Hδ, Hγ, Hβ,
  [O III] 4960/5008; observed 5570–5590, 6290–6310, 6860–6960 and 7590–7700 Å. One pass of 3σ clipping, then a refit.
- Resolution: the templates (FWHM 2.51 Å) are coarser than DESI in the rest frame, so
  `σ² = σ_fit² + σ_tpl² − σ_inst²`, both evaluated in km/s at the mean rest wavelength of the fit, `σ_inst` from the
  spectrum's own `wave_sigma` divided by (1 + z).
- Error: the formal error times √max(χ²/dof, 1).

## A1.3 Quality (the frozen cuts, plus two)

σ in [70, 500] km/s, error/σ ≤ 0.25 (as frozen); |V| ≤ 300 km/s; at least 800 unmasked pixels.

## A1.4 Model and aperture

EUC5's Jeans model unchanged. DESI fibre radius 0.75″, seeing FWHM 1.1″ (variants 0.9″ and 1.3″ replace the frozen
1.2″ / 1.8″).

## A1.5 Validation, before any `b` is read (F1 is a gate)

- **F1 recovery.** A 10 Gyr solar template broadened to 150, 250 and 350 km/s, placed at z = 0.45 on a real DESI
  wavelength grid with that spectrum's resolution and noise (the flagged spectrum of median signal-to-noise), 40 noise
  realisations each: the median recovered σ within 5 % of the input at all three. Failure: A1 is NOT EVALUABLE.
- **F2 against SDSS.** Lenses with both a DESI fit and an SDSS pipeline dispersion: the ratio, reported. If five or more
  exist, the median ratio must lie in 0.85–1.15, else A1 is NOT EVALUABLE.
- **F3 repeatability.** Lenses with two DESI spectra: the two fitted σ, reported.

## A1.6 Statistic and words

As frozen (§3), on the lenses of P with a qualifying DESI dispersion, N ≥ 30, with EUC1-F's lines, labelled
**"under A1"**: DYNAMICAL GATE HOLDS / FAILS / NO VERDICT; NO VERDICT if the word moves with β = ±0.2 or the seeing
variants; NOT EVALUABLE if N < 30 or F1 / F2 fails. Beside it: the reading on S, the SDSS readings, and the frozen
"reported" items (by Einstein radius; `b_dyn − b∞`; the conditional source redshift).

A1's new data were not seen before this file was committed, so its word is prospective for them. It is still an
amendment, and is reported as one.

κ = ½ FITTED. No outcome favours the framework.
