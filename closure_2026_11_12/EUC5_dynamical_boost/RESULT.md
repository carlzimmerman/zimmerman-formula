# EUC5 (DYNAMICAL BOOST): RESULT

2026-11-12. Criteria 7fa4e74869 (alone, before any script or lens dispersion). Amendment A1 286752fa9c (alone, before
any fit).

## Verdict: NOT EVALUABLE / NOT EVALUABLE as frozen. NOT EVALUABLE / NOT EVALUABLE under A1.

- **As frozen (SDSS pipeline dispersions):** too few lenses. 16 qualify, 7 in sample P, against the 30 required.
- **Under A1 (dispersions fitted to the DESI spectra on disk):** the sample is there (55 lenses, 32 in P), but the fit
  fails its recovery gate F1: on mock spectra at DESI's noise it reads 250 and 350 km/s dispersions 6 % and 9 % low.

What is left are readings. Two hold regardless of the dispersion scale and are stated in §4. The scale itself is
uncertain by about ±7 %, which is ±0.08 dex in `b`, so the absolute level cannot be placed against the 0.15 / 0.25 lines.

κ = ½ FITTED. Footings never pooled. No outcome favours the framework.

## 1. Instrument checks of the Jeans model (all pass; run before any lens dispersion was read)

| Check | Result |
|---|---|
| J1 Plummer sphere, projected dispersion | max error 7.1e-4 |
| J2 power-law tracer in a flat rotation curve, β = 0.3 | max error 6.4e-5 |
| J3 SLACS, lensing-calibrated masses: predicted / measured dispersion | median 0.966, mean 0.978 (A85: 0.977), scatter 0.125 |
| J4 SLACS, `b_dyn` against `b_lens` at the true source redshift | +0.085 against +0.070; median difference +0.032 dex |
| MUTATE newton | `b_med` on P −0.126 → −0.082 and −0.134 → −0.082; exit 1 |

On SLACS the law's lensing and the law's dynamics ask for the same stellar mass to 0.03 dex.

## 2. As frozen: SDSS pipeline dispersions

20 SDSS DR17 rows on the 1,240 northern lenses of S; 16 pass the cuts (15 BOSS fibres); 7 are grade A. Euclid's northern
field is mostly outside the SDSS / BOSS footprint. Readings on 16 lenses, law S: `b_dyn` median +0.051 [−0.156, +0.242]
(canonical), +0.040 [−0.165, +0.235] (alt); 9 of 16 fall below their own source-free lensing bound.

## 3. Under A1: dispersions fitted to 72 DESI spectra of 69 lenses of S

**Validation.**

| Check | Result |
|---|---|
| **F1 mock recovery at 150 / 250 / 350 km/s (gate: within 5 %)** | **0.984 / 0.937 / 0.913: FAIL** |
| F2 against SDSS on the same lens | 4 lenses: DESI / SDSS = 1.11, 0.98, 1.08, 1.52 (fewer than 5: not a gate) |
| F3 two DESI spectra of one lens | 3 lenses: median difference 16 %, rms pull 0.88 |
| F4 (post hoc) the same fitter on SDSS spectra of 30 SLACS lenses with published dispersions, S/N 14 | fitted / published median 1.068, mean 1.088, scatter 0.149 |

Five polynomial settings were then tried on the mocks only. All read 3–7 % low at 250 km/s; one (multiplicative
degree 12) passed the 5 % line at 0.971 / 0.952 / 0.960. The settings differ by less than the mock noise (3–4 % on each
median), so none was adopted: choosing the one that passed would be tuning on noise. The frozen setting stands and F1
stands failed.

So the fitter reads low on noisy mocks, high on real SLACS spectra, and 10 % above the SDSS pipeline on four shared
lenses. **The dispersion scale is not pinned to better than about ±7 %.**

**Readings (58 spectra pass the quality cuts; 55 lenses, 32 in P; median σ = 259 km/s, error 14 %, S/N 3.3 per pixel).**
Law S, β = 0, fibre 0.75″, seeing 1.1″. "Corrected" divides each σ by the F1 recovery ratio at that σ.

| Sample | `b_dyn` raw, canonical / alt | corrected, canonical / alt |
|---|---|---|
| P (N = 32) | +0.196 [+0.110, +0.270] / +0.191 [+0.105, +0.265] | +0.250 [+0.177, +0.339] / +0.243 [+0.171, +0.334] |
| S (N = 55) | +0.193 [+0.117, +0.258] / +0.187 [+0.111, +0.252] | +0.239 [+0.185, +0.321] / +0.232 [+0.180, +0.315] |

β = ±0.2 moves the median by 0.015 dex; seeing 0.9″ to 1.3″ by 0.006 dex. If F4's +7 % applied to the DESI fits, the raw
values would come down by about 0.075 dex, to +0.12.

**By Einstein radius (sample S, law S, alt):**

| θ_E | N | `b_dyn` raw [95 %] | corrected | source-free lensing bound `b∞` |
|---|---|---|---|---|
| below 1.0″ | 16 | +0.043 [−0.070, +0.207] | +0.087 | −0.173 |
| 1.0–1.3″ | 14 | +0.169 [+0.065, +0.315] | +0.236 | −0.079 |
| 1.3″ and above | 25 | +0.252 [+0.151, +0.302] | +0.315 | +0.16 to +0.24 |

Wide minus small: +0.209 [+0.018, +0.331] raw, +0.228 [+0.014, +0.360] corrected; bootstrap probability of no
difference 0.02. Spearman correlation of `b_dyn` with θ_E: 0.31, p = 0.023, N = 55.

**Dynamics against the lensing bound (S, N = 55):** median `b_dyn − b∞` = +0.103 [+0.011, +0.136] canonical, +0.119
[+0.029, +0.152] alt (raw); +0.17 to +0.19 corrected. Positive, as one potential requires.

## 4. What this says

1. **No gate.** The absolute dynamical boost of Euclid's spectroscopic lens galaxies lies somewhere between about +0.05
   (SDSS pipeline, 16 lenses) and +0.25 (DESI fits, bias-corrected). That range contains both of EUC1-F's lines.
2. **Holds whatever the scale: the boost rises with Einstein radius.** Small-separation lenses read +0.04, wide ones
   +0.25, a difference of 0.21 dex at about two sigma. A common error in the dispersion scale cancels in the difference.
   The stars in wide lenses move faster than the law plus their stellar mass allows, by more than in small lenses. So
   the extra mass EUC4 found by lensing in wide lenses is felt inside the fibre too, within about 4 kpc. It is not
   only mass seen in projection far from the galaxy.
3. **Holds whatever the scale: in small-separation lenses the stars and the law agree like SLACS.** +0.04 [−0.07, +0.21]
   against SLACS's +0.085. With a roughly Salpeter stellar mass the law accounts for the central dynamics of the
   galaxy-scale lenses. Their lensing bound is −0.17, which leaves 0.2 dex for the source redshift, a normal amount.
4. **A correction to §2's hint.** The 16 SDSS lenses suggested dynamics below the lensing bound. The larger DESI set
   does not support that: dynamics sit above the bound.
5. **Not a test of a₀ or κ; the IMF degeneracy of A70 applies.** Two sigma on 55 noisy spectra is a reading.

## 5. What would settle it

Dispersions at higher signal-to-noise for a few dozen sample-P lenses, or a fitter validated to 2–3 % on DESI-like
spectra against galaxies with known dispersions. DESI DR2 spectra of the same lenses (not public yet) would double the
exposure for many.

## 6. Files

- Frozen run: `euc5_fetch.py`, `euc5_sdss_matches.csv`, `euc5.py`, `euc5.out`, `euc5_results.json`, `euc5_per_lens.csv`,
  `euc5_MUTATE_newton.*` (exit 1).
- A1: `euc5_a1_fit.py` (default settings are A1's; `--degree`, `--mdegree`, `--f1-only` were added for the mock trials),
  `euc5_a1_fit.out` / `.json`, `euc5_a1_dispersions.csv`, the `*_asfrozen.*` copies made before the trials (identical),
  `euc5_a1.py`, `euc5_a1.out`, `euc5_a1_results.json`, `euc5_a1_per_lens.csv`.
- F4: `euc5_f4_slacs.py`, `.out`, `.json` (SDSS DR17 spectra from NOIRLab SPARCL, kept outside git).
- Spectra and templates are outside git (`_external_data/`). pPXF 9.5.2; E-MILES BaSTI, bimodal IMF 1.30.
