# EUC5 (DYNAMICAL BOOST): RESULT

2026-11-12. Criteria 7fa4e74869 (alone, before any script or lens dispersion). Amendment A1 286752fa9c (alone, before
any fit).

## Verdict: NOT EVALUABLE / NOT EVALUABLE as frozen. NOT EVALUABLE / NOT EVALUABLE under A1.

- **As frozen (SDSS pipeline dispersions):** too few lenses. 16 qualify, 7 in sample P, against the 30 required.
- **Under A1 (dispersions fitted to the DESI spectra on disk):** the sample is there (55 lenses, 32 in P), but the fit
  fails its recovery gate F1: on mock spectra at DESI's noise it reads 250 and 350 km/s dispersions 6 % and 9 % low.

What is left are readings. Two hold regardless of the dispersion scale and are stated in §4. A post hoc calibration
on real spectra (§3b) then puts the DESI fits on the scale of the published SLACS dispersions: on that scale Euclid's
spectroscopic lens galaxies read `b_dyn` = +0.14 [+0.05, +0.21] ± 0.07 (scale), against SLACS's +0.085. §3c seals what
that implies for EUC3 before EUC3 lands.

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

## 3b. Post hoc scale calibration on real spectra (`euc5_a2_scale.py`; not a gate)

F1 used mock spectra. The same question was put to real ones: the 30 SLACS SDSS spectra of F4 were refitted after
noise was added to bring them down to DESI's signal-to-noise, ten realisations each.

| Quantity | Value |
|---|---|
| σ(noisy) / σ(as observed), real spectra | median 0.997 [0.975, 1.029] (0.973 above 290 km/s, 1.025 below 240) |
| method offset, fitted / published (F4) | 1.068 [1.031, 1.122] |
| DESI-fit scale relative to the published SLACS scale | 1.064 [1.016, 1.141], i.e. ±0.066 dex in `b` |

The 6–9 % low bias of the mocks does not appear on real spectra; the mocks were the harsher case. A1 stays NOT
EVALUABLE: its gate was F1 as frozen, and it failed.

`b_dyn` with every DESI dispersion divided by 1.064 (law S, canonical / alt; statistical interval, then ±0.066 scale):

| Sample | N | `b_dyn` |
|---|---|---|
| P | 32 | +0.138 [+0.051, +0.213] / +0.133 [+0.044, +0.215] |
| S | 55 | +0.135 [+0.059, +0.200] / +0.128 [+0.054, +0.193] |
| θ_E below 1.0″ | 16 | −0.009 [−0.121, +0.156] / −0.015 [−0.128, +0.147] |
| 1.0–1.3″ | 14 | +0.117 [+0.018, +0.233] / +0.112 [+0.005, +0.272] |
| 1.3″ and above | 25 | +0.200 [+0.100, +0.249] / +0.193 [+0.093, +0.245] |

SLACS on its own published dispersions: +0.085. So on one common scale the Euclid lens galaxies with spectra need
about 1.37 × Salpeter under law S and SLACS needs 1.22 ×; the difference, +0.05 dex, is inside the errors. The
small-separation lenses need no boost at all.

## 3c. Sealed forecast for EUC3 (EUC5-F; committed before any EUC3 result exists)

Under the framework light and stars see one potential, so for each lens the boost from lensing at the true source
redshift equals the boost from dynamics. EUC3 (`../EUC3_nisp_source_redshifts/`, criteria bf72d787a8, no result yet) is
measuring source redshifts. If "law plus stars, one potential" holds, EUC3's median lensing boost `b` (law S, true source
redshift) for lenses of sample S, in each Einstein-radius class, must fall inside the dynamical band below (statistical
95 % interval widened by the scale uncertainty):

| θ_E class | band, canonical | band, alt |
|---|---|---|
| below 1.0″ | −0.19 to +0.22 | −0.19 to +0.21 |
| 1.0–1.3″ | −0.05 to +0.30 | −0.06 to +0.34 |
| 1.3″ and above | +0.03 to +0.32 | +0.03 to +0.31 |

Reading rule, per class with at least 10 EUC3 lenses: **LENSING EQUALS DYNAMICS** if EUC3's 95 % interval on the class
median overlaps the band; **LENSING EXCEEDS DYNAMICS** if its lower bound lies above the band; **LENSING BELOW
DYNAMICS** if its upper bound lies below. "Exceeds" would mean mass along the line of sight that the stars inside the
fibre do not feel: an extended component. The bands are wide because 16 to 25 noisy dispersions set them; that is
their honest size. The two subsamples are different lenses (DESI footprint against grism detections), compared class
by class. `euc5_a2_scale.json` holds the numbers; its sha256 is in the commit message.

### 3d. Status of EUC5-F after EUC3 (dated addition, 2026-11-12 evening)

**EUC5-F: NOT GRADED.** EUC3 landed NOT EVALUABLE / NOT EVALUABLE (local 7f8650cc35, origin 089271db7f): its purity
null fails at both frozen tiers (12 of 934 grade-X non-lenses pass the source rule against a limit of 2.9), so its
catalogue redshifts are not lensed-source redshifts and its printed reading is void. No Einstein-radius class has 10
lenses with a valid source redshift, so the reading rule above has nothing to act on. EUC3's files were checked against
its report (gates, counts and both mutation twins as stated).

The bands above stand exactly as sealed and are not moved. EUC3's void numbers have been seen by this lane's author
(sample P, 18 systems: +0.251 / +0.236; sample S, 35: +0.292 / +0.277); they were not split by class here and are not
compared with the bands, because by EUC3's own null most of them are wrong pairings. The forecast is to be graded on
the first set of source redshifts that passes its own purity gate and gives at least 10 lenses in a class: follow-up
spectroscopy of the ECLIPSE lenses, or a lane on the extracted grism spectra.

### 3e. Dated corrections (2026-11-12, evening). No word changes.

Two defects were found by the blind re-grade (`../EUC5R_blind_dynamical_boost_regrade/`) and by a same-code re-run in
another session. Both were checked here and are fixed forward; nothing above is rewritten.

**1. The F1 mock was not built as the amendment says.** AMENDMENT_A1.md specifies "a 10 Gyr solar template".
`euc5_a1_fit.py` built the mock from a 0.6 / 0.4 mix of two templates (12 Gyr at [M/H] +0.26 and 3 Gyr at −0.35), and
this file did not say so. F1 as the amendment words it, run now with the single template
(`euc5_a1_fit_f1literal.py`, `euc5_a1_f1literal.out`): recovery **0.981 / 0.940 / 0.916 at 150 / 250 / 350 km/s:
FAIL**, against 0.984 / 0.937 / 0.913 for the mix. A1 is NOT EVALUABLE either way.

**2. The amended readings were one lens short.** The A1 fit ran at 14:40 while EUC2's extension search was still
downloading; at 15:03 that search added a DESI spectrum for EUCL-DR1-L016656 (grade A, θ_E below 1.0″). Re-run on the
final 383-row match file (same scripts, default settings; outputs under `_final56` names beside the committed ones):

| | Committed (55 lenses) | Final inputs (56 lenses) |
|---|---|---|
| Spectra fitted / lenses | 72 / 69 | 73 / 70 |
| Fits passing the cuts / lenses / in P | 58 / 55 / 32 | 59 / 56 / 33 |
| F1 recovery (gate) | 0.984 / 0.937 / 0.913, FAIL | identical, FAIL |
| A1 reading, P, law S, raw (canonical) | +0.196 [+0.110, +0.270] | +0.193 [+0.110, +0.265] |
| A1 reading, P, corrected (canonical) | +0.250 [+0.177, +0.339] | +0.239 [+0.177, +0.332] |
| A1 reading, P, raw / corrected (alt) | +0.191 / +0.243 | +0.187 / +0.232 |
| Dispersion scale (§3b) | 1.064 [1.016, 1.141] | identical |
| SLACS scale, P (canonical / alt) | +0.138 [+0.051, +0.213] / +0.133 | +0.135 [+0.051, +0.219] / +0.128 |
| SLACS scale, S | +0.135 [+0.059, +0.200] / +0.128 | +0.127 [+0.055, +0.199] / +0.120 |
| SLACS scale, θ_E below 1.0″ | N = 16: −0.009 [−0.121, +0.156] / −0.015 | N = 17: −0.067 [−0.169, +0.156] / −0.074 |
| SLACS scale, 1.0–1.3″ (N = 14) | +0.117 [+0.018, +0.233] / +0.112 | +0.117 [+0.015, +0.275] / +0.112 |
| SLACS scale, θ_E ≥ 1.3″ (N = 25) | +0.200 [+0.100, +0.249] / +0.193 | +0.200 [+0.100, +0.249] / +0.193 |

The word under A1 stays NOT EVALUABLE. The added lens sits in the small-separation class and lowers that class's
median by 0.06 dex, so the readings of §4 hold with slightly more room: small lenses need no boost (−0.07), wide ones
+0.20. The two classes that hold the same lenses as before differ only in their bootstrap draws.

**The sealed forecast (§3c) is not touched.** Its bands were sealed on the 55-lens file (hash in the commit) and
stand as written. For the record only: the 56-lens file would give −0.24 to +0.22 (canonical) and −0.24 to +0.21
(alt) for the class below 1.0″ instead of −0.19 to +0.22 and −0.19 to +0.21; the class of 1.3″ and above is the same.

**Knock-on.** EUC7's T5 row and EUC8 read the 55-lens file; dated notes are in their RESULT.md files. No word of
either changes.

## 4. What this says

1. **No gate.** The raw readings span +0.05 (SDSS pipeline, 16 lenses) to +0.25 (DESI fits with the mock correction).
   The calibration on real spectra (§3b) narrows this to +0.14 [+0.05, +0.21] ± 0.07 on the SLACS scale: close to
   SLACS's +0.085, at or below EUC1-F's 0.15 line, with 0.25 not excluded once the scale error is added.
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
- Scale calibration and forecast: `euc5_a2_scale.py`, `.out`, `.json`.
- Spectra and templates are outside git (`_external_data/`). pPXF 9.5.2; E-MILES BaSTI, bimodal IMF 1.30.
